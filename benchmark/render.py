"""Rebuild the explanatory page from saved September captures; no target requests."""
from html import escape
import json
import markdown
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / 'current/2026-09-11'
NAMES = [('copilot-local', 'Equity Copilot · local'), ('lexical-baseline', 'Lexical retrieval baseline')]
runs = [(name, label, json.loads((RUN / name / 'results.json').read_text())) for name, label in NAMES]
config = json.loads((RUN / 'config.json').read_text())


def metric_row(label, values):
    return '<tr><th scope="row">' + escape(label) + '</th>' + ''.join('<td>' + escape(str(v)) + '</td>' for v in values) + '</tr>'


summaries = [run['summary'] for _, _, run in runs]
rows = [metric_row('Strict case passes', [f"{s['passed_cases']} / 50" for s in summaries]),
        metric_row('Composite score (not accuracy)', [f"{s['overall_score']:.4f}" for s in summaries]),
        metric_row('Factual-point recall · 43 answerable cases', [f"{sum(r['answer_point_recall'] for r in run['results'] if not r['case_definition']['refusal_expected']) / 43:.2%}" for _, _, run in runs]),
        metric_row('Citation precision · per-case mean', [f"{s['citation_precision']:.2%}" for s in summaries]),
        metric_row('Required-document recall · per-case mean', [f"{s['citation_recall']:.2%}" for s in summaries]),
        metric_row('Correct expected refusals', [f"{sum(r['refusal_correct'] for r in run['results'] if r['case_definition']['refusal_expected'])} / 7" for _, _, run in runs]),
        metric_row('Transport errors / empty answers', [f"{sum(r['execution_status']=='error' for r in run['results'])} / {sum(r['execution_status']=='empty' for r in run['results'])}" for _, _, run in runs]),
        metric_row('Median / p95 answer call', [f"{s['median_latency_ms']:g} / {s['p95_latency_ms']:g} ms" for s in summaries])]
links = ''.join(f'<article><h3>{escape(label)}</h3><p><a href="{name}/report.html">Full scored report</a> · <a href="{name}/results.json">Results JSON</a> · <a href="{name}/failures.csv">Failures CSV</a></p></article>' for name, label, _ in runs)
page = '''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Fresh financial QA comparison · 11 September 2026</title>
<style>
:root{color-scheme:dark;font-family:system-ui,-apple-system,sans-serif;background:#0b1020;color:#e7edf8}body{margin:0}main{max-width:1000px;margin:auto;padding:52px 24px 80px}a{color:#9bcaff;text-underline-offset:3px}nav{font-size:14px;margin-bottom:42px;display:flex;justify-content:space-between;gap:24px}h1{font-size:clamp(32px,5vw,54px);letter-spacing:-1.5px;line-height:1.08;max-width:820px;margin:16px 0 22px}h2{margin-top:44px;font-size:25px}h3{font-size:18px}.eyebrow{color:#83d8c1;font-size:13px;letter-spacing:1.3px;text-transform:uppercase}.lede{font-size:20px;max-width:840px;line-height:1.6;color:#b9c7dc}p,li{line-height:1.7}li{margin:12px 0}.note{border-left:3px solid #e8b86d;padding:16px 20px;background:#172030;border-radius:0 12px 12px 0;color:#e8d6b9}.table{overflow:auto;margin:24px 0;border:1px solid #2b3a51;border-radius:12px}table{border-collapse:collapse;width:100%;min-width:700px}th,td{text-align:left;padding:15px 18px;border-bottom:1px solid #26334a}thead{background:#172238}tbody th{font-weight:500}td{font-variant-numeric:tabular-nums}tr:last-child>*{border-bottom:0}.cards{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}article{padding:18px 22px;border:1px solid #2b3a51;border-radius:12px}code{overflow-wrap:anywhere;color:#c8d8ed;font-size:12px}.muted{color:#9caec6;font-size:14px}.provenance{padding:22px;background:#111b2d;border-radius:12px}footer{margin-top:48px;border-top:1px solid #26334a;padding-top:24px}
@media(max-width:640px){main{padding:32px 18px 56px}table{min-width:0;table-layout:fixed}th,td{padding:11px 7px;font-size:12px;overflow-wrap:anywhere}thead th:first-child{width:44%}thead th:not(:first-child){width:28%}.table{overflow:visible}nav{font-size:12px;gap:14px}code{font-size:11px}}
</style></head><body><main>
<nav><a href="/">Historical July rescore</a><a href="https://github.com/Jo2234/financial-llm-eval-harness">Harness source ↗</a></nav>
<div class="eyebrow">Fresh execution · 11 September 2026 · No LLM</div>
<h1>Both targets need better financial answer quality.</h1>
<p class="lede">On 50 source-grounded cases, the deterministic Equity Copilot passed <strong>0</strong> strict cases and a simple lexical baseline passed <strong>2</strong>. Both missed all seven expected refusals. Every call returned a nonempty response without a transport error.</p>
<div class="note">This is a local deterministic comparison, not a model benchmark. The baseline has better citation-ID matching in this run; neither result establishes production readiness.</div>
<h2>Measured results</h2><div class="table"><table><thead><tr><th>Metric</th><th>Equity Copilot · local</th><th>Lexical baseline</th></tr></thead><tbody>''' + ''.join(rows) + '''</tbody></table></div>
<p class="muted">The API includes loopback HTTP and persistence; the baseline runs in-process. Its 0 ms median is integer rounding of sub-millisecond calls, not zero work. These timings do not establish a service speedup.</p>
<h2>How to read these scores</h2><ul>
<li>A strict pass requires factual coverage, citation thresholds and correct refusal behavior together. Partial, relevant answers can still fail.</li>
<li>The raw harness reports 86% behavior accuracy for both targets: 43 correct non-refusals out of 50 answered cases. Actual expected-refusal success is <strong>0 of 7</strong>.</li>
<li>The scorer uses word/number overlap and document identity, not semantic entailment. Seven severe flags per target reflect missing refusal; they are not seven independently verified fabrications.</li>
<li>Some questions omit the fiscal period that their required-document metadata assumes. Exact-period scoring therefore has a question-design limitation.</li></ul>
<h2>What went wrong</h2><div class="cards"><article><h3>Relevant text, incomplete answers</h3><p>The NVIDIA growth answer mentions AI demand but omits the annual growth figure and introduces quarterly data. The annual/quarterly bridge misses the annual citation.</p></article><article><h3>Refusal and relevance</h3><p>For an unavailable price target, both systems return unrelated filing text instead of explicitly stating that the sources cannot answer the question.</p></article><article><h3>The metric has blind spots</h3><p>An AI infrastructure comparison receives lexical credit for risk language that does not provide the requested investment comparison. Keyword overlap can over-credit an answer.</p></article></div>
<p><a href="review.html">Read the selected-response review and full limitations</a>. This review is AI-assisted; independent human adjudication remains outstanding.</p>
<h2>Sources and execution</h2><p>Six companies, 16 complete primary documents, and 1,311 API chunks. Raw files, normalized source texts and all 40 pinned evidence contexts match the suite hashes. Actual ingestion uses the Copilot’s production HTML/PDF extraction with paragraph boundaries. Both targets receive complete extracted source content; no reference answers, rubric text, or evaluator-selected documents enter the target request.</p>
<p>The API uses its existing deterministic local provider. The baseline selects the top three 1,200-character chunks by query-token overlap and returns 400 characters per chunk. No LLM was available at the local Ollama endpoint, and no paid provider was used.</p>
<div class="provenance"><p><strong>Captured:</strong> ''' + escape(config['capture_started_at']) + '''</p><p>Harness commit<br><code>''' + escape(config['harness']['head']) + '''</code></p><p>Copilot commit<br><code>''' + escape(config['copilot']['head']) + '''</code></p><p>Suite SHA-256<br><code>''' + escape(config['suite_sha256']) + '''</code></p><p><a href="config.json">Configuration</a> · <a href="sources.json">Source provenance</a> · <a href="ingestion.json">Ingestion and extraction hashes</a> · <a href="captures.jsonl">100 redacted capture records</a> · <a href="SHA256SUMS.json">Capture checksums</a></p></div>
<div class="note">Public records omit extractive answer text and source excerpts to avoid reproducing substantial filing/transcript prose. Scores are unchanged; original full-response hashes remain available. Public redacted records cannot independently rescore text without the original local or newly reproduced captures. <a href="PUBLIC_EXPORT.json">Export policy</a> · <a href="ORIGINAL_SHA256SUMS.json">Original artifact hashes</a></div>
<h2>Inspect and reproduce</h2><div class="cards">''' + links + '''</div><p><a href="../../benchmark/methodology.html">Methodology and reproduction commands</a>. Display rebuilding is offline; a new evaluation requires new target calls and a new output directory.</p>
<footer class="muted">The July captures, legacy suite and historical rescore remain separately preserved. Their metrics are not comparable with this current factual suite. <a href="/historical/2026-07-13/v1/index.html">Original July archive</a> · <a href="/live/report.html">July live-response rescore</a></footer>
</main></body></html>'''
(RUN / 'index.html').write_text(page)
print('Rebuilt', RUN / 'index.html')

# Render prose into readable pages rather than serving Markdown downloads.
style = page.split('<style>', 1)[1].split('</style>', 1)[0]
for source, output, title in [(RUN / 'REVIEW.md', RUN / 'review.html', 'Selected response review'),
                              (ROOT / 'benchmark/README.md', ROOT / 'benchmark/methodology.html', 'Methodology and reproduction')]:
    body = markdown.markdown(source.read_text(), extensions=['tables', 'fenced_code'])
    document = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width,initial-scale=1"><title>'
                + escape(title) + '</title><style>' + style
                + 'pre{padding:16px;background:#111b2d;overflow:auto;border-radius:10px}pre code{white-space:pre}table{margin:24px 0}h1{font-size:38px}'
                + '</style></head><body><main><nav><a href="/current/2026-09-11/index.html">Back to fresh comparison</a></nav>'
                + body + '</main></body></html>')
    output.write_text(document)
