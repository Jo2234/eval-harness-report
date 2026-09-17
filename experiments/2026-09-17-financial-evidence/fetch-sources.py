"""Download complete issuer PDFs, rejecting changes to the frozen sources."""

import argparse
import hashlib
import json
from pathlib import Path

import httpx

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--out", type=Path, required=True)
args = parser.parse_args()
args.out.mkdir(parents=True, exist_ok=True)
manifest = Path(__file__).with_name("fresh-sources.json")
for source in json.loads(manifest.read_text()):
    path = args.out / (source["id"] + ".pdf")
    if path.exists():
        data = path.read_bytes()
    else:
        response = httpx.get(source["url"], follow_redirects=True, timeout=60)
        response.raise_for_status()
        data = response.content
    if hashlib.sha256(data).hexdigest() != source["sha256"]:
        raise ValueError(f"Source hash changed: {source['id']}")
    if not path.exists():
        path.write_bytes(data)
(args.out / "sources.json").write_bytes(manifest.read_bytes())
