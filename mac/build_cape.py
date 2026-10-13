#!/usr/bin/env python3
"""Build a validated Mousecape v2 cape with lossless 1x/2x PNG sheets."""
from __future__ import annotations

import argparse
import math
import os
import plistlib
import shlex
import sys
import tempfile
from dataclasses import dataclass
from io import BytesIO
from pathlib import Path, PureWindowsPath

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ROOT / "sources/pngs/animated"
CAPE_IDENTIFIER = "local.happycadogt.cat-cursor"
MAX_FRAMES = 24  # Mousecape-swiftUI Swift_v1.2.0 MCMaxFrameCount; see docs/VALIDATION.md.
# WindowServer identifiers, not NSCursor method names. Other roles stay native.
CURSOR_MAPPINGS = {
    "com.apple.coregraphics.Arrow": "default",
    "com.apple.coregraphics.ArrowCtx": "default",
    "com.apple.coregraphics.IBeam": "text",
    "com.apple.coregraphics.IBeamXOR": "text",
    "com.apple.coregraphics.Wait": "wait",
    "com.apple.cursor.4": "progress",
    "com.apple.cursor.11": "pointer_2",
    "com.apple.cursor.12": "pointer",
    "com.apple.cursor.13": "pointer",
    **{f"com.apple.cursor.{n}": "size_hor" for n in (17, 18, 19, 27, 28, 38)},
    **{f"com.apple.cursor.{n}": "size_ver" for n in (21, 23, 31, 32)},
    **{f"com.apple.cursor.{n}": "size_ver_2" for n in (22, 36)},
}


@dataclass(frozen=True)
class Frame:
    size: int
    xhot: int
    yhot: int
    path: Path
    delay_ms: int


def parse_conf(path: Path) -> list[Frame]:
    """Read one animation; validate every frame, including frames later sampled out."""
    frames: list[Frame] = []
    dimensions = None
    root = path.parent.resolve()
    for line_no, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), 1):
        try:
            parts = shlex.split(line, comments=True)
            if not parts:
                continue
            if len(parts) != 5:
                raise ValueError("expected size xhot yhot png_path delay_ms")
            size, xhot, yhot = map(int, parts[:3])
            delay = int(parts[4])
            if size <= 0 or min(xhot, yhot) < 0 or delay <= 0:
                raise ValueError("size/delay must be positive; hotspots non-negative")
            ref = Path(parts[3])
            if ref.is_absolute() or PureWindowsPath(parts[3]).drive or ".." in ref.parts:
                raise ValueError("PNG path must stay inside the source directory")
            candidates = [root / ref]
            # Exact legacy layout used by the existing artwork, not arbitrary basename fallback.
            if len(ref.parts) == 3 and ref.parts[:2] == ("png", root.name):
                candidates.append(root / ref.name)
            png = next((p.resolve() for p in candidates if p.is_file()), None)
            if png is None or not png.is_relative_to(root):
                raise ValueError(f"missing or out-of-tree PNG: {ref}")
            with Image.open(png) as image:
                if image.format != "PNG" or image.width != image.height or image.width > 512:
                    raise ValueError("expected a square PNG no larger than 512 pixels")
                if dimensions is not None and image.size != dimensions:
                    raise ValueError("inconsistent animation dimensions")
                dimensions = image.size
                if xhot >= image.width or yhot >= image.height:
                    raise ValueError("hotspot is outside the actual PNG")
                image.verify()
            frames.append(Frame(size, xhot, yhot, png, delay))
        except (ValueError, OSError, SyntaxError) as exc:
            raise ValueError(f"{path}:{line_no}: {exc}") from exc
    if not frames:
        raise ValueError(f"{path}: no frames")
    if len({(f.size, f.xhot, f.yhot) for f in frames}) != 1:
        raise ValueError(f"{path}: inconsistent nominal size or hotspots")
    return frames


def sample_timeline(frames: list[Frame], limit: int) -> tuple[list[Frame], float]:
    """Uniform cape slots sampled by elapsed time, preserving exact loop duration.

    Variable-delay poses are repeated where possible. Under the 24-slot cap,
    transitions may be quantized by less than one output slot, or omitted.
    """
    if not frames or type(limit) is not int or not 1 <= limit <= MAX_FRAMES:
        raise ValueError("need frames and an integer frame limit in 1..24")
    if any(type(f.delay_ms) is not int or f.delay_ms <= 0 for f in frames):
        raise ValueError("frame delays must be positive integers")
    total = sum(f.delay_ms for f in frames)
    quantum = math.gcd(*(f.delay_ms for f in frames))
    count = min(limit, total // quantum)
    selected, index, end = [], 0, frames[0].delay_ms
    for slot in range(count):
        while slot * total >= end * count and index < len(frames) - 1:
            index += 1
            end += frames[index].delay_ms
        selected.append(frames[index])
    return selected, total / count / 1000.0


def build_cursor_entry(name: str, size: int, limit: int, sources: Path = SOURCES) -> dict:
    frames = parse_conf(sources / name / f"{name}.conf")
    selected, duration = sample_timeline(frames, limit)
    with Image.open(frames[0].path) as image:
        pixels_wide = image.width
    # Xcursor nominal size can differ from the actual PNG dimensions.
    hotspot = (frames[0].xhot * size / pixels_wide, frames[0].yhot * size / pixels_wide)
    if any(value >= size or value > 31.99 for value in hotspot):
        raise ValueError(f"{name}: hotspot exceeds supported bounds; use --size 32")
    reps = []
    for density in (1, 2):
        pixels = size * density
        sheet = Image.new("RGBA", (pixels, pixels * len(selected)))
        for index, frame in enumerate(selected):
            with Image.open(frame.path) as image:
                rgba = image.convert("RGBA").resize((pixels, pixels), Image.Resampling.LANCZOS)
            sheet.paste(rgba, (0, pixels * index))  # No mask: do not multiply alpha twice.
        buffer = BytesIO()
        sheet.save(buffer, format="PNG")
        reps.append(buffer.getvalue())
    return dict(FrameCount=len(selected), FrameDuration=duration, BaseFrameDuration=duration,
                HotSpotX=hotspot[0], HotSpotY=hotspot[1], PointsWide=float(size),
                PointsHigh=float(size), Representations=reps)


def validate_cape(cape: dict) -> None:
    if cape.get("Identifier") != CAPE_IDENTIFIER or cape.get("Version") != 2.0:
        raise ValueError("unexpected cape identifier or version")
    if set(cape.get("Cursors", {})) != set(CURSOR_MAPPINGS):
        raise ValueError("unsupported or missing cursor identifiers")
    for name, cursor in cape["Cursors"].items():
        try:
            count, duration = cursor["FrameCount"], cursor["FrameDuration"]
            width, height = cursor["PointsWide"], cursor["PointsHigh"]
            xhot, yhot = cursor["HotSpotX"], cursor["HotSpotY"]
            if any(type(x) not in (int, float) or not math.isfinite(x)
                   for x in (duration, width, height, xhot, yhot)):
                raise ValueError("non-finite or non-numeric geometry/timing")
            if type(count) is not int or not 1 <= count <= MAX_FRAMES or duration <= 0:
                raise ValueError("invalid timing")
            if not 16 <= width <= 64 or width != height or width != int(width):
                raise ValueError("invalid dimensions")
            if not all(0 <= v < width and v <= 31.99 for v in (xhot, yhot)):
                raise ValueError("invalid hotspot")
            reps = cursor["Representations"]
            if len(reps) != 2:
                raise ValueError("need both 1x and 2x representations")
            for density, data in enumerate(reps, 1):
                with Image.open(BytesIO(data)) as image:
                    image.load()
                    if (image.format != "PNG" or image.mode != "RGBA" or
                            image.size != (int(width * density), int(height * density * count))):
                        raise ValueError(f"invalid sprite sheet at {density}x")
        except (KeyError, TypeError, OSError, ValueError) as exc:
            raise ValueError(f"{name}: {exc}") from exc


def build_cape(size: int, limit: int, output: Path, sources: Path = SOURCES) -> dict:
    if type(size) is not int or not 16 <= size <= 64 or type(limit) is not int or not 1 <= limit <= 24:
        raise ValueError("size must be an integer in 16..64; frame limit in 1..24")
    entries = {name: build_cursor_entry(name, size, limit, sources)
               for name in sorted(set(CURSOR_MAPPINGS.values()))}
    cape = dict(Author="HappyCadogt (Windows/art); Tseshongfeeshur (Linux); Amory0709 (macOS)",
                CapeName="猫标 Cat Cursor", CapeVersion=4.0, Cloud=False, HiDPI=True,
                Identifier=CAPE_IDENTIFIER, MinimumVersion=2.0, Version=2.0, Animate=True,
                Cursors={key: entries[name] for key, name in CURSOR_MAPPINGS.items()})
    validate_cape(cape)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=output.parent, delete=False) as handle:
            temporary = Path(handle.name)
            plistlib.dump(cape, handle, fmt=plistlib.FMT_XML, sort_keys=True)
        os.replace(temporary, output)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    print(f"Validated {len(cape['Cursors'])} roles, lossless PNG 1x/2x: {output}")
    return cape


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--size", type=int, default=32, help="logical points (default: 32)")
    parser.add_argument("--max-frames", type=int, default=24)
    parser.add_argument("--output", type=Path, default=ROOT / "mac/dist/Cat-Cursor.cape")
    parser.add_argument("--sources", type=Path, default=SOURCES)
    args = parser.parse_args()
    try:
        build_cape(args.size, args.max_frames, args.output, args.sources)
    except (ValueError, OSError) as exc:
        print(f"Build failed: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
