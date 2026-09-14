"""Validate against the pinned srelens host; never connect to a cluster."""
import argparse
import json
from pathlib import Path
import subprocess
ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--host', type=Path, default=ROOT / '.host')
args = parser.parse_args()
metadata = json.loads((ROOT / 'compatibility.json').read_text())
manifest = json.loads((ROOT / 'manifest.json').read_text())
if manifest['id'] != metadata['extensionId']:
    raise SystemExit('Changing the extension ID breaks existing installations')
revision = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=args.host, text=True).strip()
if revision != metadata['hostRevision']:
    raise SystemExit('Host checkout does not match compatibility.json')
subprocess.run(['cargo', 'run', '--locked', '-p', 'srelens-plugin-host', '--example', 'extension_host', '--', str(ROOT / 'manifest.json'), *['--grant=' + grant for grant in manifest['permissions']]], cwd=args.host, check=True)
