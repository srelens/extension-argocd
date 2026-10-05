import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
ROOT = Path(__file__).resolve().parents[1]
class PackageTests(unittest.TestCase):
    def test_stages_all_signed_files_including_the_official_icon(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "scripts").mkdir()
            shutil.copy(ROOT / "scripts/package.py", root / "scripts/package.py")
            files = {"manifest.json": b'{"id":"org.test.app","version":"1.2.3"}\n',
                     "README.md": b"App documentation", "LICENSE": b"App license", "icons/icon.svg": b'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16"><path d="M0 0h16v16H0z"/></svg>'}
            for name, raw in files.items():
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(raw)
            subprocess.run(["python3", "scripts/package.py", "--version", "1.2.3"], cwd=root, check=True)
            stage = root / "dist/package"
            self.assertEqual({p.relative_to(stage).as_posix() for p in stage.rglob("*") if p.is_file()}, {"extension.json", "README.md", "LICENSE", "icons/icon.svg"})
            for name, raw in files.items():
                self.assertEqual((stage / ("extension.json" if name == "manifest.json" else name)).read_bytes(), raw)

    def test_missing_icon_cannot_produce_a_release(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "scripts").mkdir()
            shutil.copy(ROOT / "scripts/package.py", root / "scripts/package.py")
            (root / "manifest.json").write_text('{"version":"1.2.3"}')
            (root / "README.md").write_text("docs")
            (root / "LICENSE").write_text("license")
            result = subprocess.run(["python3", "scripts/package.py", "--version", "1.2.3"], cwd=root, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((root / "dist").exists())
