"""Ingest complete pinned raw sources using production extraction; never use evidence facts or answer labels."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import httpx
import yaml

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--copilot', type=Path, required=True)
parser.add_argument('--harness', type=Path, required=True)
parser.add_argument('--sources', type=Path, required=True)
parser.add_argument('--work', type=Path, required=True)
parser.add_argument('--api', default='http://127.0.0.1:8766')
args = parser.parse_args()
BASE = args.work.resolve()
BASE.mkdir(parents=True, exist_ok=True)
if (BASE / 'equity-ingestion.json').exists():
    raise SystemExit('Use a new work directory; existing ingestion evidence is immutable')
REPO = args.copilot.resolve()
MANIFEST = args.harness.resolve() / 'evals/evidence/manifest.yaml'
SOURCE = args.sources.resolve()
DOCS=yaml.safe_load(MANIFEST.read_text())['documents']
sys.path.insert(0, str(REPO/'backend'))
from ai_equity_research_copilot_backend.sec import html_to_text
from ai_equity_research_copilot_backend.parsing import parse_document
DERIVED=BASE/'source-faithful-extraction'
DERIVED.mkdir(exist_ok=True)
NAMES={'NVDA':'NVIDIA Corporation','AAPL':'Apple Inc.','MSFT':'Microsoft Corporation','JPM':'JPMorgan Chase & Co.','XOM':'Exxon Mobil Corporation','TSLA':'Tesla, Inc.'}
TYPES={'10-K':'10-k','10-Q':'10-q','earnings_call':'earnings_transcript','earnings_release':'8-k'}
report={'timestamp_utc':datetime.now(timezone.utc).isoformat(),'equity_base_sha':subprocess.check_output(['git','-C',str(REPO),'rev-parse','HEAD'],text=True).strip(),'endpoint':args.api,'provider':'local','model':'local-deterministic-grounded-v1','seed':False,'settings':{'embedding_dimensions':128,'chunk_target_tokens':800,'chunk_overlap_tokens':80,'retrieval_min_score':0.04,'max_upload_mb':10},'manifest_sha256':hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),'source_dir':str(SOURCE),'documents':[],'companies':{},'document_uuid_to_canonical':{}}
with httpx.Client(base_url=report['endpoint'],timeout=180,trust_env=False) as client:
    health=client.get('/health');health.raise_for_status();assert health.json()['companies']==0, 'Refuse to mix with existing corpus'
    for ticker,name in NAMES.items():
        response=client.post('/companies',json={'ticker':ticker,'name':name});response.raise_for_status();report['companies'][ticker]=response.json()['id']
    for doc in DOCS:
        canonical=doc['document_id'];ticker,year,*_=canonical.split('_');ticker=ticker.upper()
        raw_path=next(path for suffix in ('.html','.pdf') if (path:=SOURCE/f'{canonical}{suffix}').exists())
        raw=raw_path.read_bytes()
        assert hashlib.sha256(raw).hexdigest()==doc['sha256'], f'Raw hash mismatch: {canonical}'
        if raw_path.suffix=='.html':
            extracted=html_to_text(raw.decode('utf-8'))
            path=DERIVED/f'{canonical}.txt'
            path.write_text(extracted)
            content=path.read_bytes();mime='text/plain';method='sec.html_to_text, complete text without SEC download truncation'
        else:
            path=raw_path;content=raw;mime='application/pdf';method='raw PDF through production parse_document'
            extracted='\n\n'.join(page.text for page in parse_document(path))
            (DERIVED/f'{canonical}.txt').write_text(extracted)
        derived_path=DERIVED/f'{canonical}.txt'
        metadata={'title':canonical,'document_type':TYPES[doc['document_type']],'fiscal_year':year,'source_url':doc['url'],'period_end_date':doc['period_end']}
        if '_q1_' in canonical: metadata['fiscal_quarter']='1'
        response=client.post(f"/companies/{report['companies'][ticker]}/documents",data=metadata,files={'file':(path.name,content,mime)});response.raise_for_status();result=response.json()
        assert result['status']=='ready',result
        report['document_uuid_to_canonical'][result['id']]=canonical
        report['documents'].append({'canonical_id':canonical,'uuid':result['id'],'company_uuid':report['companies'][ticker],'source_path':str(raw_path),'raw_sha256':hashlib.sha256(raw).hexdigest(),'upload_path':str(path),'upload_sha256':hashlib.sha256(content).hexdigest(),'extraction_method':method,'derived_text_path':str(derived_path),'derived_text_sha256':hashlib.sha256(derived_path.read_bytes()).hexdigest(),'byte_count':len(content),'metadata':metadata,'chunk_count':result['chunk_count']})
        (BASE/'equity-ingestion.json').write_text(json.dumps(report,indent=2)+'\n')
        print(canonical,result['chunk_count'],flush=True)
    report['health']=client.get('/health').json()
(BASE/'equity-ingestion.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report['health']))
