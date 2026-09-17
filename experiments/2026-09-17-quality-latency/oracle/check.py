"""Evaluate source-backed cases through the production upload and chat APIs."""
import argparse,hashlib,json,os,re,sys,tempfile,time,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--ticker',required=True);p.add_argument('--company',required=True);p.add_argument('--copilot',type=Path,required=True);p.add_argument('--sources',type=Path,required=True);p.add_argument('--cases',type=Path,required=True);p.add_argument('--out',type=Path,required=True);args=p.parse_args()
assert not args.out.exists(),'Capture is immutable; select a new output path'
sys.path.insert(0,str(args.copilot.resolve()/'backend'));os.environ['AIERC_LLM_PROVIDER']='local'
with tempfile.TemporaryDirectory() as temp:
 os.environ['AIERC_DATA_DIR']=str(Path(temp)/'import')
 from fastapi.testclient import TestClient
 from ai_equity_research_copilot_backend.main import create_app
 client=TestClient(create_app(Path(temp)/'corpus',seed=False))
 company=client.post('/companies',json={'ticker':args.ticker,'name':args.company}).json();mapping={};source_rows=json.loads((args.sources/'sources.json').read_text())
 for row in source_rows:
  data=(args.sources/(row['id']+'.pdf')).read_bytes();assert hashlib.sha256(data).hexdigest()==row['sha256']
  metadata={k:str(row[k]) for k in ['title','fiscal_year','fiscal_quarter','document_type'] if k in row};metadata['source_url']=row['url']
  response=client.post(f"/companies/{company['id']}/documents",data=metadata,files={'file':(row['id']+'.pdf',data,'application/pdf')});response.raise_for_status();doc=response.json();assert doc['status']=='ready',doc
  mapping[doc['id']]=row['id']
 results=[]
 for case in json.loads(args.cases.read_text()):
  started=time.perf_counter();response=client.post('/research/chat',json={'company_ids':[company['id']],'question':case['question'],'top_k':8});response.raise_for_status();payload=response.json()
  missing=[pattern for pattern in case['patterns'] if not re.search(pattern,payload['answer'],re.I)]
  actual=sorted({mapping[c['document_id']] for c in payload['citations']});expected=sorted(case['documents'])
  correct_refusal=not case.get('refusal') or (not actual and payload['confidence']=='low' and not payload['key_points'])
  results.append({'id':case['id'],'passed':not missing and actual==expected and correct_refusal,'missing_patterns':missing,'documents':actual,'expected_documents':expected,'latency_ms':round((time.perf_counter()-started)*1000,3),'answer':payload['answer'],'citations':payload['citations'],'limitations':payload['limitations'],'key_points':payload['key_points'],'confidence':payload['confidence']})
 result={'copilot_commit':subprocess.check_output(['git','-C',str(args.copilot),'rev-parse','HEAD'],text=True).strip(),'company':{'ticker':args.ticker,'name':args.company},'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'method':'Frozen source-backed numerical fact-presence, exact source-document coverage and explicit-refusal checks; not semantic entailment or independent held-out accuracy. No reference facts or document IDs enter chat requests.','cases_sha256':hashlib.sha256(args.cases.read_bytes()).hexdigest(),'sources':source_rows,'passed':sum(r['passed'] for r in results),'total':len(results),'results':results}
 args.out.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['passed','total','cases_sha256']}))
