"""Create a version-checked manifest release and its checksum."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--version', required=True)
args = parser.parse_args()
raw = (ROOT / 'manifest.json').read_bytes()
manifest = json.loads(raw)
if args.version != manifest['version']:
    raise SystemExit('Requested release version does not match manifest.json')
files = {"extension.json": ROOT / "manifest.json", "README.md": ROOT / "README.md",
         "LICENSE": ROOT / "LICENSE", "icons/icon.svg": ROOT / "icons/icon.svg"}
for source in files.values():
    if not source.is_file():
        raise SystemExit(f"Required package asset is missing: {source.name}")
out = ROOT / 'dist'
out.mkdir(exist_ok=True)
(out / 'manifest.json').write_bytes(raw)
(out / 'SHA256SUMS').write_text(hashlib.sha256(raw).hexdigest() + '  manifest.json\n')
print(out)
stage = out / "package"
if stage.exists():
    shutil.rmtree(stage)
for name, source in files.items():
    target = stage / name
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
