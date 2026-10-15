#!/usr/bin/env python3
"""One validated manifest for ZIP/DMG, local, Windows, and CI builds."""
from __future__ import annotations

import argparse
import hashlib
import os
from pathlib import Path
import plistlib
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "mac"))
from build_cape import build_cape, validate_cape

PACKAGE_FILES = {
    "mac/package/Install Cat Cursor.command": "Install Cat Cursor.command",
    "mac/package/手动导入.command": "手动导入.command",
    "mac/package/请先阅读.txt": "请先阅读.txt",
    "mac/package/README.txt": "README.txt",
    "mac/lib/install_core.sh": "lib/install_core.sh",
    "docs/cursor-test.html": "Cursor Test.html",
    "CREDITS.md": "CREDITS.md",
    "LICENSE": "LICENSE",
}


def stage_package(stage: Path, cape: Path, root: Path = ROOT) -> None:
    validate_cape(plistlib.loads(cape.read_bytes()))
    stage.mkdir(parents=True, exist_ok=False)
    shutil.copyfile(cape, stage / "Cat-Cursor.cape")
    for source, target in PACKAGE_FILES.items():
        destination = stage / target
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(root / source, destination)
    paths = sorted(p for p in stage.rglob("*") if p.is_file())
    for path in paths:
        path.chmod(0o755 if path.suffix in (".sh", ".command") else 0o644)
    lines = [f"{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.relative_to(stage).as_posix()}"
             for p in paths]
    (stage / "SHA256SUMS").write_bytes(("\n".join(lines) + "\n").encode("utf-8"))


def write_zip(stage: Path, output: Path) -> None:
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in sorted(p for p in stage.rglob("*") if p.is_file()):
            info = zipfile.ZipInfo(f"Cat-Cursor-macOS/{path.relative_to(stage).as_posix()}")
            info.create_system = 3
            mode = 0o755 if path.suffix in (".command", ".sh") else 0o644
            info.external_attr = (0o100000 | mode) << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default="candidate")
    parser.add_argument("--dmg", action="store_true")
    args = parser.parse_args()
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", args.version):
        parser.error("version must be a safe filename component")
    if args.dmg and sys.platform != "darwin":
        parser.error("DMG creation requires macOS")
    dist = ROOT / "dist"
    dist.mkdir(exist_ok=True)
    cape = ROOT / "mac/dist/Cat-Cursor.cape"
    build_cape(32, 24, cape)
    with tempfile.TemporaryDirectory(prefix="cat-cursor-") as directory:
        stage = Path(directory) / "Cat-Cursor-macOS"
        stage_package(stage, cape)
        output = dist / f"Cat-Cursor-macOS-v{args.version}.zip"
        temporary = dist / f".{output.name}.tmp"
        try:
            write_zip(stage, temporary)
            os.replace(temporary, output)
        finally:
            temporary.unlink(missing_ok=True)
        if args.dmg:
            subprocess.run(["hdiutil", "create", "-volname", "Cat Cursor", "-srcfolder",
                            str(stage), "-ov", "-format", "UDZO",
                            str(dist / "Cat-Cursor-Installer.dmg")], check=True)
    print(f"Created {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
