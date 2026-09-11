"""Fetch exact pinned public sources, failing closed on raw or normalized drift."""
import argparse
import hashlib
from pathlib import Path
import re
import time

from bs4 import BeautifulSoup
import fitz
import httpx
import yaml

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--manifest', type=Path, required=True)
parser.add_argument('--out', type=Path, required=True)
parser.add_argument('--user-agent', required=True, help='Identifying contact User-Agent for SEC fair access')
args = parser.parse_args()
manifest = yaml.safe_load(args.manifest.read_text())
args.out.mkdir(parents=True, exist_ok=True)
with httpx.Client(headers={'User-Agent': args.user_agent}, timeout=60, follow_redirects=True) as client:
    for document in manifest['documents']:
        doc_id = document['document_id']
        response = client.get(document['url'])
        response.raise_for_status()
        raw = response.content
        if hashlib.sha256(raw).hexdigest() != document['sha256']:
            raise SystemExit(f'Raw source drift for {doc_id}; obtain the pinned snapshot or explicitly curate a new suite')
        suffix = '.pdf' if raw.startswith(b'%PDF') else '.html'
        if suffix == '.pdf':
            with fitz.open(stream=raw, filetype='pdf') as pdf:
                text = ' '.join(page.get_text() for page in pdf)
        else:
            soup = BeautifulSoup(raw.decode('utf-8'), 'html.parser')
            for element in soup(['script', 'style']):
                element.decompose()
            text = soup.get_text(' ')
        text = re.sub(r'\s+', ' ', text).strip()
        expected = {row['normalized_text_sha256'] for row in manifest['evidence'] if row['document_id'] == doc_id}
        if expected != {hashlib.sha256(text.encode()).hexdigest()}:
            raise SystemExit(f'Normalization drift for {doc_id}; do not silently substitute extraction libraries')
        (args.out / (doc_id + suffix)).write_bytes(raw)
        (args.out / (doc_id + '.txt')).write_text(text)
        print(doc_id)
        time.sleep(0.2)
