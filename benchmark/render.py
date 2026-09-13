"""Rebuild presentation from saved public results, offline and without rescoring."""

import argparse
import hashlib
import json
import sys
from html import escape
from pathlib import Path
from string import Template

import markdown

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "current/2026-09-11"
NAMES = [
    ("copilot-local", "Equity Copilot · local"),
    ("lexical-baseline", "Lexical retrieval baseline"),
]


def metric_row(label, values):
    return (
        '<tr><th scope="row">'
        + escape(label)
        + "</th>"
        + "".join("<td>" + escape(str(v)) + "</td>" for v in values)
        + "</tr>"
    )


def render(harness):
    sys.path.insert(0, str(harness.resolve()))
    from fin_eval.reporting import REPORT_CSS
    from fin_eval.runner import html_report

    runs = [
        (name, label, json.loads((RUN / name / "results.json").read_text()))
        for name, label in NAMES
    ]
    config = json.loads((RUN / "config.json").read_text())
    summaries = [run["summary"] for _, _, run in runs]
    rows = [
        metric_row(
            "Strict case passes",
            [f"{s['passed_cases']} / {s['total_cases']}" for s in summaries],
        ),
        metric_row(
            "Composite score (not accuracy)",
            [f"{s['overall_score']:.4f}" for s in summaries],
        ),
        metric_row(
            "Factual-point recall · 43 answerable cases",
            [
                f"{sum(r['answer_point_recall'] for r in run['results'] if not r['case_definition']['refusal_expected']) / 43:.2%}"
                for _, _, run in runs
            ],
        ),
        metric_row(
            "Citation precision · per-case mean",
            [f"{s['citation_precision']:.2%}" for s in summaries],
        ),
        metric_row(
            "Required-document recall · per-case mean",
            [f"{s['citation_recall']:.2%}" for s in summaries],
        ),
        metric_row(
            "Correct expected refusals",
            [
                f"{sum(r['refusal_correct'] for r in run['results'] if r['case_definition']['refusal_expected'])} / 7"
                for _, _, run in runs
            ],
        ),
        metric_row(
            "Transport errors / empty answers",
            [
                f"{sum(r['execution_status'] == 'error' for r in run['results'])} / {sum(r['execution_status'] == 'empty' for r in run['results'])}"
                for _, _, run in runs
            ],
        ),
        metric_row(
            "Median / p95 answer call",
            [
                f"{s['median_latency_ms']:g} / {s['p95_latency_ms']:g} ms"
                for s in summaries
            ],
        ),
    ]
    cards = []
    for index, (name, label, run) in enumerate(runs, 1):
        s = run["summary"]
        ratio = s["passed_cases"] / s["total_cases"] if s["total_cases"] else 0
        description = (
            "Existing local provider · deterministic API"
            if name == "copilot-local"
            else "Query-token overlap · top three chunks"
        )
        cards.append(f'''<article class="system">
<div class="system-top">
<span class="system-index">SYSTEM 0{index}</span>
<span class="pill">No LLM</span>
</div>
<h3>{escape(label)}</h3>
<p class="muted">{description}</p>
<div class="result">{s["passed_cases"]} <small>/ {s["total_cases"]} passed</small>
</div>
<p class="muted">{ratio:.0%} strict case pass rate</p>
<div class="bar" aria-hidden="true">
<span style="width:{ratio:.2%}">
</span>
</div>
<dl>
<div>
<dt>Composite score</dt>
<dd>{s["overall_score"]:.4f}</dd>
</div>
<div>
<dt>Citation precision</dt>
<dd>{s["citation_precision"]:.2%}</dd>
</div>
</dl>
<a class="button secondary" href="{name}/report.html#cases">Inspect {s["total_cases"]} cases <span aria-hidden="true">→</span>
</a>
<div class="inspect-links">
<a href="{name}/results.json">Results JSON ↗</a>
<a href="{name}/failures.csv">Failures CSV ↓</a>
</div>
</article>''')
        # Re-render only the presentation; do not run scorers on redacted answers.
        (RUN / name / "report.html").write_text(html_report(run))
    template = Template((ROOT / "benchmark/comparison.template.html").read_text())
    page = template.substitute(
        style=REPORT_CSS,
        system_cards="".join(cards),
        metric_rows="".join(rows),
        captured=escape(config["capture_started_at"]),
        harness_commit=escape(config["harness"]["head"]),
        copilot_commit=escape(config["copilot"]["head"]),
        suite_hash=escape(config["suite_sha256"]),
    )
    (RUN / "index.html").write_text(page)
    for source, output, title in [
        (RUN / "REVIEW.md", RUN / "review.html", "Selected response review"),
        (
            ROOT / "benchmark/README.md",
            ROOT / "benchmark/methodology.html",
            "Methodology and reproduction",
        ),
    ]:
        body = markdown.markdown(
            source.read_text(), extensions=["tables", "fenced_code"]
        )
        document = (
            '<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1"><title>'
            + escape(title)
            + "</title><style>"
            + REPORT_CSS
            + '</style></head><body><main><header class="masthead"><a class="brand" href="/current/2026-09-11/index.html"><span class="brand-mark" aria-hidden="true">ƒ</span>Financial QA / Evaluation lab</a></header><nav class="anchor-nav"><a href="/current/2026-09-11/index.html">← Back to comparison</a></nav><article class="prose">'
            + body
            + "</article></main></body></html>"
        )
        output.write_text(document)
    # HTML is a derivative in the public inventory. Update only the two rendered
    # report entries; measured data, capture hashes and original inventory stay intact.
    inventory_path = RUN / "SHA256SUMS.json"
    inventory = json.loads(inventory_path.read_text())
    for name, _ in NAMES:
        relative = f"{name}/report.html"
        inventory[relative] = hashlib.sha256((RUN / relative).read_bytes()).hexdigest()
    inventory_path.write_text(json.dumps(inventory, indent=2) + "\n")
    print(
        "Rebuilt comparison, two case reports, review and methodology from unchanged saved results."
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--harness", type=Path, default=ROOT.parent / "financial-llm-eval-harness"
    )
    render(parser.parse_args().harness)
