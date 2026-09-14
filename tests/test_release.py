import hashlib
import json
from pathlib import Path
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
class ReleaseTests(unittest.TestCase):
    def test_packages_exact_source_bytes_and_matching_checksum(self):
        raw = (ROOT / 'manifest.json').read_bytes()
        version = json.loads(raw)['version']
        subprocess.run([sys.executable, 'scripts/package.py', '--version', version], cwd=ROOT, check=True, capture_output=True)
        self.assertEqual((ROOT / 'dist/manifest.json').read_bytes(), raw)
        self.assertEqual((ROOT / 'dist/SHA256SUMS').read_text(), hashlib.sha256(raw).hexdigest() + '  manifest.json\n')

    def test_rejects_a_release_version_that_does_not_match_manifest(self):
        result = subprocess.run([sys.executable, 'scripts/package.py', '--version', '9999.0.0'], cwd=ROOT, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('does not match', result.stderr)
