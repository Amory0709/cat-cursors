# Cat Cursor — macOS port

[中文](./README.md) | English

**Original Windows project and all original artwork: HappyCadogt's 猫标 / Cat Cursor.** This repository is a macOS conversion, not the original Windows project.

| Platform / contribution | Author / project |
| --- | --- |
| **Windows original** | [HappyCadogt, Bilibili UID 406949928](https://space.bilibili.com/406949928) · [Original showcase](https://www.bilibili.com/video/BV1S2itBHEJH/). Follow the creator's published Windows download instructions. |
| GNU/Linux source port | [Tseshongfeeshur / Ryan — cat-cursors](https://github.com/Tseshongfeeshur/cat-cursors), upstream for the PNG/config sources |
| macOS conversion | [Amory0709](https://github.com/Amory0709/cat-cursors) |

See [CREDITS.md](./CREDITS.md). The original MIT text is retained; this port does not claim ownership or grant new permissions over the artist's work.

## Get the repaired candidate

Open a successful [Validate and package](https://github.com/Amory0709/cat-cursors/actions/workflows/validate.yml) run for the repair commit and download **Cat-Cursor-macOS-candidate** (GitHub may require sign-in). It contains a ZIP, DMG, and standalone cape.

**Existing Releases are not updated by a source commit.** A new `v*` tag and successful checks are required to publish a new [Release](https://github.com/Amory0709/cat-cursors/releases). Generated capes are no longer committed to `mac/dist/` as conflicting stale copies.

## Install without scripts

1. Install [Mousecape-swiftUI](https://github.com/sdmj76/Mousecape-swiftUI/releases/latest). Its current README lists macOS 14+ and Intel/Apple Silicon; follow the requirements for the version you download.
2. Open Mousecape and import or drag **Cat-Cursor.cape** into its window.
3. Confirm import, select **猫标 Cat Cursor**, then click **Apply**.
4. Open **Cursor Test.html** in Safari to check actual system cursor roles and click positioning.

When upgrading, optionally reset the current theme with **File > Reset System Cursor (Cmd+R)** before importing the new file. Resolve any overwrite prompt in the manager yourself; do not delete the whole theme library.

The optional unsigned `.command` scripts only request import. They never directly call mousecloak, write the manager's private library, or claim that Apply succeeded. If macOS blocks a script, skip it and import the cape data manually. Do not disable Gatekeeper, recursively clear quarantine, or use sudo.

## Repair details

21 actual WindowServer identifiers use nine source animations. Incorrect NSCursor-style names have been replaced for pointing, grabbing, and horizontal/vertical resizing. Roles without suitable artwork remain native instead of disguising forbidden operations as waiting or replacing precision crosshairs with arrows.

The default canvas is **32 logical points**, with lossless **1x/2x PNG** representations and validated pixel-based hotspots. Animation is sampled by elapsed time with exact loop duration and at most **24 frames**. Long sequences necessarily lose poses/frame rate; full Windows animation smoothness is not promised.

The upstream decoder accepts PNG; HEIF is not required for import. PNG removes an encoding dependency and preserves transparency without lossy encoding.

ZIP, DMG, CI, and Windows-host packaging share one manifest, including quick-start instructions, import helpers, a manual test page, credits, and SHA256SUMS. Checksums detect corruption, not publisher authenticity.

![Representative source frames](./docs/previews/showcase.png)

These previews are not proof of interactive macOS application testing.

## Troubleshooting and restore

Import is not Apply. Confirm the imported theme and animation settings in Mousecape. Use manual import for a renamed app, or set `MOUSECAPE_APP` to its path.

The manager's [troubleshooting guide](https://github.com/sdmj76/Mousecape-swiftUI#troubleshooting) documents custom pointer-color interference and apps that override system cursors. Test in Finder and Safari. Grant permissions only in response to actual manager/macOS prompts.

Restore with **Mousecape > File > Reset System Cursor (Cmd+R)**. Login reapplication is an optional manager setting.

## Build and verify

Python 3.10+; CI uses 3.12. End users importing a theme do not need Python.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r mac/requirements.txt
python -m unittest discover -s tests -v
python scripts/build_release.py --version candidate
# On macOS only, add --dmg.
```

On Windows, `scripts/build-release.ps1` builds a **macOS ZIP**, not a Windows installer. For the Windows original, use the creator links above.

See [build parameters](./mac/README.md) and [validation evidence/limits](./docs/VALIDATION.md). Automated builds and AppKit decoding do not certify interactive Apply, every macOS version, sleep/wake, or all applications.
