from __future__ import annotations

import copy
import hashlib
from io import BytesIO
import os
from pathlib import Path
import plistlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
import zipfile

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "mac"), str(ROOT / "scripts")]
import build_cape as build
import build_release as package


def fixture(root: Path, name="default", delays=(100, 300), nominal=32) -> Path:
    folder = root / name
    folder.mkdir(parents=True, exist_ok=True)
    lines = []
    for index, delay in enumerate(delays, 1):
        Image.new("RGBA", (32, 32), (index * 40 % 256, 100, 200, 128)).save(folder / f"{index}.png")
        lines.append(f"{nominal} 8 12 png/{name}/{index}.png {delay}")
    conf = folder / f"{name}.conf"
    conf.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return conf


class BuildTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.sources = self.root / "sources"
        for name in set(build.CURSOR_MAPPINGS.values()):
            fixture(self.sources, name)
        self.conf = self.sources / "default/default.conf"

    def cape(self):
        return build.build_cape(32, 24, self.root / "theme.cape", self.sources)

    def test_conf_comments_bom_and_legacy_path(self):
        self.conf.write_text('\ufeff# Comment\n\n32 8 12 "png/default/1.png" 100 # End\n', encoding="utf-8")
        frames = build.parse_conf(self.conf)
        self.assertEqual(len(frames), 1)
        self.assertEqual(frames[0].path, self.conf.parent / "1.png")

    def test_relative_path(self):
        self.conf.write_text("32 8 12 1.png 100\n", encoding="utf-8")
        self.assertEqual(build.parse_conf(self.conf)[0].path, self.conf.parent / "1.png")

    def test_bad_conf_reports_file_and_line(self):
        for line in ("bad", "32 8 12 1.png", "0 8 12 1.png 100", "32 -1 12 1.png 100",
                     "32 8 -1 1.png 100", "32 32 12 1.png 100", "32 8 32 1.png 100",
                     "32 8 12 1.png 0", "32 8 12 1.png -1", "32 8 12 missing.png 100",
                     "32 8 12 ../1.png 100", "32 8 12 /tmp/1.png 100",
                     "32 8 12 C:/1.png 100", '32 8 12 "unclosed 100'):
            with self.subTest(line=line):
                self.conf.write_text("# Header\n" + line, encoding="utf-8")
                with self.assertRaisesRegex(ValueError, r"default.conf:2:"):
                    build.parse_conf(self.conf)

    def test_empty_conf_is_an_error(self):
        self.conf.write_text("# Empty\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "no frames"):
            build.parse_conf(self.conf)

    def test_no_arbitrary_basename_fallback(self):
        self.conf.write_text("32 8 12 unrelated/1.png 100\n", encoding="utf-8")
        with self.assertRaises(ValueError):
            build.parse_conf(self.conf)

    def test_source_resolution_is_independent_of_cwd(self):
        shadow = self.root / "other/png/default"
        shadow.mkdir(parents=True)
        (shadow / "1.png").write_bytes(b"not a PNG")
        previous = Path.cwd()
        try:
            os.chdir(self.root / "other")
            self.assertEqual(build.parse_conf(self.conf)[0].path, self.conf.parent / "1.png")
        finally:
            os.chdir(previous)

    def test_corrupt_unsampled_frame_is_rejected(self):
        (self.conf.parent / "2.png").write_bytes(b"corrupt")
        with self.assertRaises(ValueError):
            build.build_cursor_entry("default", 32, 1, self.sources)

    def test_mixed_dimensions_are_rejected(self):
        Image.new("RGBA", (16, 16)).save(self.conf.parent / "2.png")
        with self.assertRaisesRegex(ValueError, "inconsistent animation dimensions"):
            build.parse_conf(self.conf)

    def test_non_square_and_non_png_rejected(self):
        for image, fmt in ((Image.new("RGBA", (32, 16)), "PNG"),
                           (Image.new("RGB", (32, 32)), "JPEG")):
            image.save(self.conf.parent / "1.png", format=fmt)
            with self.assertRaises(ValueError):
                build.parse_conf(self.conf)

    def test_mixed_hotspots_rejected(self):
        self.conf.write_text("32 8 12 1.png 100\n32 9 12 2.png 100\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "inconsistent nominal size or hotspots"):
            build.parse_conf(self.conf)

    def test_hotspot_uses_actual_pixels_not_nominal_size(self):
        fixture(self.sources, nominal=256)
        cursor = build.build_cursor_entry("default", 32, 24, self.sources)
        self.assertEqual((cursor["HotSpotX"], cursor["HotSpotY"]), (8, 12))

    def test_large_hotspot_rejected_not_clamped(self):
        self.conf.write_text("32 20 20 1.png 100\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "hotspot exceeds"):
            build.build_cursor_entry("default", 64, 24, self.sources)

    def test_variable_delay_held_pose_is_repeated(self):
        sampled, duration = build.sample_timeline(build.parse_conf(self.conf), 24)
        self.assertEqual([f.path.name for f in sampled], ["1.png", "2.png", "2.png", "2.png"])
        self.assertAlmostEqual(duration, 0.1)

    def test_130_frames_preserve_4_29_second_loop(self):
        frames = [build.Frame(32, 0, 0, Path(str(i)), 33) for i in range(130)]
        sampled, duration = build.sample_timeline(frames, 24)
        self.assertEqual(len(sampled), 24)
        self.assertAlmostEqual(duration * len(sampled), 4.29)
        self.assertEqual(sampled[0], frames[0])

    def test_all_frame_limits_preserve_duration(self):
        frames = [build.Frame(32, 0, 0, Path(str(i)), d) for i, d in enumerate((40, 50, 900, 33))]
        for limit in range(1, 25):
            sampled, duration = build.sample_timeline(frames, limit)
            self.assertLessEqual(len(sampled), limit)
            self.assertAlmostEqual(len(sampled) * duration, 1.023)

    def test_invalid_frame_limits(self):
        for limit in (0, -1, 25, 1.5, True):
            with self.subTest(limit=limit), self.assertRaises(ValueError):
                build.sample_timeline(build.parse_conf(self.conf), limit)
        with self.assertRaises(ValueError):
            build.sample_timeline([], 24)

    def test_png_retina_geometry_alpha_and_frame_order(self):
        cursor = build.build_cursor_entry("default", 32, 24, self.sources)
        for density, data in enumerate(cursor["Representations"], 1):
            with Image.open(BytesIO(data)) as image:
                self.assertEqual((image.format, image.mode), ("PNG", "RGBA"))
                self.assertEqual(image.size, (32 * density, 128 * density))
                self.assertEqual(image.getpixel((16 * density, 16 * density))[3], 128)
                self.assertLess(image.getpixel((16 * density, 16 * density))[0],
                                image.getpixel((16 * density, 48 * density))[0])

    def test_real_identifiers_and_native_semantic_fallback(self):
        mappings = build.CURSOR_MAPPINGS
        for key, value in ((13, "pointer"), (11, "pointer_2"), (19, "size_hor"), (23, "size_ver")):
            self.assertEqual(mappings[f"com.apple.cursor.{key}"], value)
        self.assertNotIn("com.apple.coregraphics.PointingHand", mappings)
        self.assertNotIn("com.apple.cursor.3", mappings)
        self.assertNotIn("com.apple.cursor.7", mappings)
        self.assertEqual(len(mappings), 21)

    def test_plist_roundtrip_and_repeatable_build(self):
        cape = self.cape()
        data = (self.root / "theme.cape").read_bytes()
        self.assertEqual(cape, plistlib.loads(data))
        self.assertTrue(cape["Animate"])
        self.cape()
        self.assertEqual(data, (self.root / "theme.cape").read_bytes())

    def test_invalid_metadata_and_missing_retina_rejected(self):
        original = self.cape()
        changes = {"FrameCount": [0, 25, True], "FrameDuration": [0, float("nan"), "1"],
                   "HotSpotX": [-1, 32, float("inf")], "PointsWide": [0, 32.5, 65],
                   "Representations": [[], [b"invalid", b"invalid"]]}
        for field, values in changes.items():
            for value in values:
                with self.subTest(field=field, value=value):
                    cape = copy.deepcopy(original)
                    cape["Cursors"]["com.apple.coregraphics.Arrow"][field] = value
                    with self.assertRaises(ValueError):
                        build.validate_cape(cape)

    def test_wrong_identifier_or_roles_rejected(self):
        original = self.cape()
        for field, value in (("Identifier", "wrong"), ("Version", 1), ("Cursors", {})):
            cape = copy.deepcopy(original)
            cape[field] = value
            with self.assertRaises(ValueError):
                build.validate_cape(cape)

    def test_failed_build_preserves_previous_output(self):
        output = self.root / "theme.cape"
        output.write_bytes(b"previous")
        with self.assertRaises(ValueError):
            build.build_cape(0, 24, output, self.sources)
        self.assertEqual(output.read_bytes(), b"previous")
        with patch.object(build.os, "replace", side_effect=OSError("test failure")):
            with self.assertRaises(OSError):
                build.build_cape(32, 24, output, self.sources)
        self.assertEqual(output.read_bytes(), b"previous")
        self.assertEqual(sorted(p.name for p in self.root.iterdir()), ["sources", "theme.cape"])

    def test_zip_manifest_permissions_checksums_and_repeatability(self):
        self.cape()
        stage = self.root / "stage"
        package.stage_package(stage, self.root / "theme.cape")
        output = self.root / "theme.zip"
        package.write_zip(stage, output)
        prefix = "Cat-Cursor-macOS/"
        with zipfile.ZipFile(output) as archive:
            self.assertIsNone(archive.testzip())
            expected = {prefix + p for p in package.PACKAGE_FILES.values()} | {prefix + "Cat-Cursor.cape", prefix + "SHA256SUMS"}
            self.assertEqual(set(archive.namelist()), expected)
            for info in archive.infolist():
                executable = info.filename.endswith((".sh", ".command"))
                self.assertEqual((info.external_attr >> 16) & 0o777, 0o755 if executable else 0o644)
            for line in archive.read(prefix + "SHA256SUMS").decode("utf-8").splitlines():
                digest, name = line.split("  ", 1)
                self.assertEqual(hashlib.sha256(archive.read(prefix + name)).hexdigest(), digest)
        data = output.read_bytes()
        package.write_zip(stage, output)
        self.assertEqual(data, output.read_bytes())

    def test_package_refuses_invalid_cape_and_dirty_stage(self):
        cape = self.root / "invalid.cape"
        cape.write_bytes(plistlib.dumps({}))
        with self.assertRaises(ValueError):
            package.stage_package(self.root / "stage", cape)
        self.cape()
        stage = self.root / "stage"
        stage.mkdir()
        with self.assertRaises(FileExistsError):
            package.stage_package(stage, self.root / "theme.cape")

    def test_unsafe_release_version_rejected(self):
        result = subprocess.run([sys.executable, str(ROOT / "scripts/build_release.py"), "--version", "../../escape"], capture_output=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn(b"safe filename", result.stderr)

    def test_shell_files_have_lf_line_endings(self):
        for path in (ROOT / "mac").rglob("*"):
            if path.suffix in (".sh", ".command"):
                self.assertNotIn(b"\r", path.read_bytes())


@unittest.skipIf(os.name == "nt" or shutil.which("bash") is None, "POSIX shell integration tests")
class InstallerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="cat's space ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        (self.root / "Cat-Cursor.cape").write_text("mock plist")
        self.app = self.root / "User Apps/Mousecape.app"
        self.app.mkdir(parents=True)
        self.env = {**os.environ, "HOME": str(self.root), "MOUSECAPE_APP": str(self.app), "OPEN_LOG": str(self.root / "opened")}

    def run_installer(self, overrides=""):
        script = '''source "$1"
is_macos() { return 0; }
validate_plist() { return 0; }
bundle_id() { echo com.sdmj76.mousecape; }
open_theme() { printf '%s\\n' "$1" "$2" > "$OPEN_LOG"; }
notify_import() { return 0; }
''' + overrides + '\nmain "$2"\n'
        return subprocess.run(["bash", "-c", script, "test", str(ROOT / "mac/lib/install_core.sh"), str(self.root)], env=self.env, capture_output=True, text=True)

    def test_import_only_handles_quoted_paths(self):
        result = self.run_installer()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("NOT yet confirmed", result.stdout)
        self.assertEqual((self.root / "opened").read_text().splitlines(), [str(self.app), str(self.root / "Cat-Cursor.cape")])
        self.assertFalse((self.root / "Library").exists())

    def test_failed_checks_never_launch_or_report_success(self):
        for override in ("is_macos() { return 1; }", "validate_plist() { return 1; }",
                         "verify_package() { return 1; }", "resolve_app() { return 1; }",
                         "bundle_id() { echo com.alexzielenski.mousecape; }",
                         "bundle_id() { echo unknown; }"):
            with self.subTest(override=override):
                result = self.run_installer(override)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((self.root / "opened").exists())
                self.assertNotIn("Open request sent", result.stdout)

    def test_open_failure_propagates(self):
        result = self.run_installer("open_theme() { return 1; }")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Could not open", result.stderr)
        self.assertNotIn("Open request sent", result.stdout)

    def test_missing_cape(self):
        (self.root / "Cat-Cursor.cape").unlink()
        self.assertNotEqual(self.run_installer().returncode, 0)

    def test_repo_dist_path(self):
        (self.root / "dist").mkdir()
        (self.root / "Cat-Cursor.cape").rename(self.root / "dist/Cat-Cursor.cape")
        self.assertEqual(self.run_installer().returncode, 0)

    def test_shell_syntax(self):
        for path in (ROOT / "mac").rglob("*"):
            if path.suffix in (".sh", ".command"):
                result = subprocess.run(["bash", "-n", str(path)], capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)


class RealSourceTests(unittest.TestCase):
    def test_complete_repository_artwork(self):
        if not build.SOURCES.is_dir():
            if os.environ.get("CATCURSOR_REQUIRE_SOURCES") == "1":
                self.fail("CI requires the real source artwork")
            self.skipTest("real artwork unavailable in this local environment")
        with tempfile.TemporaryDirectory() as directory:
            cape = build.build_cape(32, 24, Path(directory) / "Cat-Cursor.cape")
            for role, name in build.CURSOR_MAPPINGS.items():
                cursor = cape["Cursors"][role]
                frames = build.parse_conf(build.SOURCES / name / f"{name}.conf")
                self.assertAlmostEqual(cursor["FrameCount"] * cursor["FrameDuration"],
                                       sum(f.delay_ms for f in frames) / 1000)
                print(f"REAL SOURCE {role}: {len(frames)} -> {cursor['FrameCount']} frames, "
                      f"{cursor['PointsWide']}pt, hotspot=({cursor['HotSpotX']},{cursor['HotSpotY']})")


if __name__ == "__main__":
    unittest.main()
