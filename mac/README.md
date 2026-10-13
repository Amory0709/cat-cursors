# macOS build and installation

[中文首页](../README.md) · [English](../README_en-US.md) · [Windows original and credits](../CREDITS.md)

Windows original/art: **HappyCadogt** — https://space.bilibili.com/406949928
Original showcase: https://www.bilibili.com/video/BV1S2itBHEJH/
Linux source port: **Tseshongfeeshur / Ryan** — https://github.com/Tseshongfeeshur/cat-cursors
macOS port: **Amory0709**.

## Installing a built theme

Open Mousecape-swiftUI, import `Cat-Cursor.cape`, select it, and click **Apply**. Download the manager from https://github.com/sdmj76/Mousecape-swiftUI/releases/latest and follow that release's requirements.

Import helpers are optional. `bash mac/install.sh` requires a previously built `mac/dist/Cat-Cursor.cape`; a fresh clone no longer contains generated themes. Helpers support `/Applications/Mousecape.app`, `~/Applications/Mousecape.app`, or an explicit `MOUSECAPE_APP`. They report import requests, not successful system application. Unknown app identities require manual import.

Use the manager's reset function (File > Reset System Cursor / Cmd+R) to restore the default theme. No privileged installer or deletion of existing themes is needed.

## Developer setup (repository root)

Python 3.10+; Python 3.12 in CI.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r mac/requirements.txt
python -m unittest discover -s tests -v
python scripts/build_release.py --version candidate
# macOS only:
python scripts/build_release.py --version candidate --dmg
```

Windows users can activate a Python virtual environment in their shell, install the same requirements, and call `python scripts/build_release.py --version candidate` or `scripts/build-release.ps1`. This produces a macOS ZIP, not a Windows cursor package.

## Theme-only options

```bash
python mac/build_cape.py --size 32 --max-frames 24 --output mac/dist/Cat-Cursor.cape
```

| Option | Default | Meaning |
| --- | --- | --- |
| `--size` | 32 | Integer logical point canvas, 16..64; any size violating a source hotspot's 31.99-point bound is rejected, not silently clamped |
| `--max-frames` | 24 | Integer limit, 1..24; 1 yields one static pose |
| `--sources` | sources/pngs/animated | Source root; each animation has a matching `.conf` |
| `--output` | mac/dist/Cat-Cursor.cape | Atomic output after validation |

Every entry has lossless 1x/2x RGBA PNG sprite sheets. Animation uses a uniform output step; loop duration is retained, but pose transitions are quantized and some poses can be omitted under the 24-frame limit.

The single manifest in `scripts/build_release.py` owns ZIP and DMG contents. ZIP permissions are explicitly POSIX even on Windows. SHA256SUMS covers all packaged payload files; it detects corruption, not authenticity. DMG creation uses macOS `hdiutil`.

## Verification

```bash
CATCURSOR_REQUIRE_SOURCES=1 python -m unittest discover -s tests -v
swift mac/verify_cape.swift mac/dist/Cat-Cursor.cape   # macOS only
```

The first command requires the real artwork; CI never silently skips it. Shell integration tests run on POSIX hosts, not Windows. The Swift test verifies AppKit image decoding, geometry and alpha without applying a system theme.

Use `docs/cursor-test.html` (packaged as `Cursor Test.html`) and the checklist in [docs/VALIDATION.md](../docs/VALIDATION.md) for interactive acceptance. Do not call a candidate production-tested based on a headless build alone.
