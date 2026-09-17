"""Remove extractive answer text and issuer excerpts from a local capture."""
import argparse, hashlib, json
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--capture',type=Path,required=True);p.add_argument('--out',type=Path,required=True);args=p.parse_args()
assert not args.out.exists(),'Public capture is immutable; choose a new output path'
x=json.loads(args.capture.read_text())
for result in x['results']:
    result['answer_sha256']=hashlib.sha256(result.pop('answer').encode()).hexdigest()
    result['citation_count']=len(result.pop('citations'))
    result['key_point_count']=len(result.pop('key_points'))
    result.pop('limitations',None)
x['capture_sha256']=hashlib.sha256(args.capture.read_bytes()).hexdigest()
x['export_policy']='Extractive answers, key-point prose, citation snippets and limitations removed; source URLs/hashes, metrics and source-coverage checks retained. Original immutable capture remains local.'
args.out.write_text(json.dumps(x,indent=2)+'\n')
