"""Run frozen synthetic checks through the production chat API without answer hints."""
import argparse, hashlib, json, os, sys, tempfile
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--copilot',type=Path,required=True);p.add_argument('--cases',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args()
sys.path.insert(0,str(a.copilot.resolve()/'backend'))
os.environ['AIERC_LLM_PROVIDER']='local'
with tempfile.TemporaryDirectory() as directory:
 os.environ['AIERC_DATA_DIR']=str(Path(directory)/'import')
 from fastapi.testclient import TestClient
 from ai_equity_research_copilot_backend.main import create_app
 rows=[]
 for case in json.loads(a.cases.read_text()):
  app=create_app(Path(directory)/case['id'],seed=False); client=TestClient(app)
  company=client.post('/companies',json={'ticker':'BETA','name':'Beta Industries'}).json()
  for key,year,quarter,kind in [('annual',2024,None,'10-k'),('quarter',2025,2,'10-q')]:
   if key not in case:continue
   metadata={'title':key,'fiscal_year':str(year),'document_type':kind}
   if quarter:metadata['fiscal_quarter']=str(quarter)
   result=client.post(f"/companies/{company['id']}/documents",data=metadata,files={'file':(key+'.txt',case[key].encode(),'text/plain')})
   result.raise_for_status();assert result.json()['status']=='ready',result.text
  response=client.post('/research/chat',json={'company_ids':[company['id']],'question':case['question']})
  response.raise_for_status();result=response.json()
  missing=[v for v in case['required'] if v not in result['answer']]
  citations=len({c['document_id'] for c in result['citations']})
  rows.append({'id':case['id'],'passed':not missing and citations==case['citations'],'missing':missing,'document_citations':citations,'expected_document_citations':case['citations'],'answer':result['answer'],'citations':result['citations']})
 output={'cases_sha256':hashlib.sha256(a.cases.read_bytes()).hexdigest(),'passed':sum(r['passed'] for r in rows),'total':len(rows),'results':rows}
 a.out.write_text(json.dumps(output,indent=2)+'\n')
 print(json.dumps({k:v for k,v in output.items() if k!='results'}))
 for row in rows:
  if not row['passed']:print(row['id'],row['missing'],row['document_citations'])
