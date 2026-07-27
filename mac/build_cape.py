#!/usr/bin/env python3
"""Build a Mousecape-swiftUI compatible .cape theme from source PNGs."""

from __future__ import annotations

import argparse
import plistlib
import sys
from io import BytesIO
from pathlib import Path

import pillow_heif
from PIL import Image

pillow_heif.register_heif_opener()

ROOT = Path(__file__).resolve().parent.parent
SOURCES = ROOT / "sources" / "pngs" / "animated"
DIST = Path(__file__).resolve().parent / "dist"

CAPE_IDENTIFIER = "local.happycadogt.cat-cursor"

CURSOR_MAPPINGS: dict[str, str] = {
    "com.apple.coregraphics.Arrow": "default",
    "com.apple.coregraphics.IBeam": "text",
    "com.apple.coregraphics.IBeamForVerticalLayout": "text",
    "com.apple.coregraphics.PointingHand": "pointer",
    "com.apple.coregraphics.Wait": "wait",
    "com.apple.coregraphics.BusyButClickable": "progress",
    "com.apple.coregraphics.ResizeLeftRight": "size_hor",
    "com.apple.coregraphics.ResizeEastWest": "size_hor",
    "com.apple.coregraphics.ResizeLeft": "size_hor",
    "com.apple.coregraphics.ResizeRight": "size_hor",
    "com.apple.coregraphics.ResizeUpDown": "size_ver",
    "com.apple.coregraphics.ResizeNorthSouth": "size_ver",
    "com.apple.coregraphics.ResizeUp": "size_ver",
    "com.apple.coregraphics.ResizeDown": "size_ver_2",
    "com.apple.coregraphics.ResizeNorth": "size_ver",
    "com.apple.coregraphics.ResizeSouth": "size_ver_2",
    "com.apple.coregraphics.OpenHand": "pointer",
    "com.apple.coregraphics.ClosedHand": "pointer_2",
    "com.apple.coregraphics.DragCopy": "pointer",
    "com.apple.coregraphics.DragLink": "pointer",
    "com.apple.coregraphics.OperationNotAllowed": "wait",
    "com.apple.coregraphics.Move": "default",
    "com.apple.coregraphics.Crosshair": "default",
    "com.apple.coregraphics.ContextualMenu": "pointer",
    "com.apple.coregraphics.DisappearingItem": "default",
    "com.apple.coregraphics.Help": "pointer",
    "com.apple.coregraphics.ZoomIn": "pointer",
    "com.apple.coregraphics.ZoomOut": "pointer",
}


def parse_conf(conf_path: Path) -> list[tuple[int, int, int, Path, int]]:
    frames: list[tuple[int, int, int, Path, int]] = []
    conf_dir = conf_path.parent

    for line in conf_path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        parts = stripped.split()
        if len(parts) < 5:
            continue

        size = int(parts[0])
        xhot = int(parts[1])
        yhot = int(parts[2])
        png_ref = parts[3]
        delay = int(parts[4])

        png_path = Path(png_ref)
        if not png_path.is_file():
            png_path = conf_dir / png_path.name

        if not png_path.is_file():
            raise FileNotFoundError(f"Missing PNG for {conf_path.name}: {png_ref}")

        frames.append((size, xhot, yhot, png_path, delay))

    if not frames:
        raise ValueError(f"No frames found in {conf_path}")

    return frames


def downsample_frames(
    frames: list[tuple[int, int, int, Path, int]],
    max_frames: int,
) -> list[tuple[int, int, int, Path, int]]:
    if len(frames) <= max_frames:
        return frames

    total_duration = sum(frame[4] for frame in frames)
    selected: list[tuple[int, int, int, Path, int]] = []

    for index in range(max_frames):
        source_index = min(
            int(index * len(frames) / max_frames),
            len(frames) - 1,
        )
        frame = frames[source_index]
        delay = max(1, int(total_duration / max_frames))
        selected.append((frame[0], frame[1], frame[2], frame[3], delay))

    return selected


def load_scaled_frames(
    frames: list[tuple[int, int, int, Path, int]],
    target_size: int,
    max_frames: int,
) -> tuple[list[Image.Image], float, float, float]:
    frames = downsample_frames(frames, max_frames)
    orig_size = frames[0][0]
    scale = target_size / orig_size
    xhot = round(frames[0][1] * scale, 1)
    yhot = round(frames[0][2] * scale, 1)
    frame_duration = frames[0][4] / 1000.0

    images: list[Image.Image] = []
    for _, _, _, png_path, _ in frames:
        with Image.open(png_path) as image:
            rgba = image.convert("RGBA")
            resized = rgba.resize((target_size, target_size), Image.Resampling.LANCZOS)
            images.append(resized)

    return images, xhot, yhot, frame_duration


def stack_frames_heif(images: list[Image.Image]) -> bytes:
    width, height = images[0].size
    stacked = Image.new("RGBA", (width, height * len(images)), (0, 0, 0, 0))

    for index, image in enumerate(images):
        stacked.paste(image, (0, index * height))

    buffer = BytesIO()
    stacked.save(buffer, format="HEIF", quality=85)
    return buffer.getvalue()


def build_cursor_entry(
    source_name: str,
    target_size: int,
    max_frames: int,
) -> dict[str, object]:
    conf_path = SOURCES / source_name / f"{source_name}.conf"
    if not conf_path.is_file():
        raise FileNotFoundError(f"Missing source config: {conf_path}")

    frames = parse_conf(conf_path)
    images, xhot, yhot, frame_duration = load_scaled_frames(
        frames,
        target_size,
        max_frames,
    )
    heif_bytes = stack_frames_heif(images)
    size = float(target_size)

    return {
        "FrameCount": len(images),
        "FrameDuration": float(frame_duration),
        "HotSpotX": float(xhot),
        "HotSpotY": float(yhot),
        "PointsWide": size,
        "PointsHigh": size,
        "Representations": [heif_bytes],
    }


def build_cape(target_size: int, max_frames: int, output_path: Path) -> None:
    source_entries: dict[str, dict[str, object]] = {}

    for source_name in dict.fromkeys(CURSOR_MAPPINGS.values()):
        print(f"Building source cursor: {source_name}")
        source_entries[source_name] = build_cursor_entry(
            source_name,
            target_size,
            max_frames,
        )

    cursors = {
        mac_id: source_entries[source_name]
        for mac_id, source_name in CURSOR_MAPPINGS.items()
    }

    cape = {
        "Author": "HappyCadogt / Ryan / macOS port",
        "CapeName": "猫标 Cat Cursor",
        "CapeVersion": 3.0,
        "Cloud": False,
        "HiDPI": True,
        "Identifier": CAPE_IDENTIFIER,
        "MinimumVersion": 2.0,
        "Version": 2.0,
        "Cursors": cursors,
    }

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("wb") as handle:
        plistlib.dump(cape, handle, fmt=plistlib.FMT_XML)

    size_kb = output_path.stat().st_size // 1024
    print(f"Wrote {output_path.name} ({size_kb} KB, Mousecape-swiftUI HEIF format)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--size",
        type=int,
        default=64,
        help="Cursor size in macOS points (default: 64)",
    )
    parser.add_argument(
        "--max-frames",
        type=int,
        default=24,
        help="Maximum animation frames per cursor (default: 24)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DIST / "Cat-Cursor.cape",
        help="Output .cape path",
    )
    args = parser.parse_args()

    if not SOURCES.is_dir():
        print(f"Missing sources directory: {SOURCES}", file=sys.stderr)
        return 1

    build_cape(args.size, args.max_frames, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
