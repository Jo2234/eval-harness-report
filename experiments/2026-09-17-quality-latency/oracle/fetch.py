"""Download complete source PDFs and verify frozen content fingerprints."""
import hashlib,json,urllib.request
from pathlib import Path
import fitz
root=Path(__file__).resolve().parent
rows=[{'id':'oracle_fy2025','url':'https://s23.q4cdn.com/440135859/files/doc_financials/2025/q4/4q25-pressrelease-June-final.pdf','fiscal_year':2025,'document_type':'8-k','title':'Oracle Q4 and FY2025 earnings release'}, {'id':'oracle_q1fy2027','url':'https://investor.oracle.com/files/content_files/1q27-pressrelease-September_FINAL.pdf','fiscal_year':2027,'fiscal_quarter':1,'document_type':'8-k','title':'Oracle Q1 FY2027 earnings release'}]
source=root/'sources'; source.mkdir(exist_ok=True)
manifest=source/'sources.json'
existing=json.loads(manifest.read_text()) if manifest.exists() else None
for row in rows:
 path=source/(row['id']+'.pdf')
 if not path.exists():
  req=urllib.request.Request(row['url'],headers={'User-Agent':'Mozilla/5.0'})
  path.write_bytes(urllib.request.urlopen(req,timeout=60).read())
 row['sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
 doc=fitz.open(path); row['pages']=len(doc)
 (source/(row['id']+'.txt')).write_text('\n\n'.join(page.get_text() for page in doc))
 doc[0].get_pixmap(matrix=fitz.Matrix(1.3,1.3)).save(source/(row['id']+'-page1.png'))
if existing is not None:
 assert rows==existing,'Source changed from frozen manifest'
else: manifest.write_text(json.dumps(rows,indent=2)+'\n')
print(json.dumps(rows,indent=2))
