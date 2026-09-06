"""Rebuild corrected artifacts offline from the immutable July 2026 capture."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from string import Template


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--harness",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "financial-llm-eval-harness",
    )
    parser.add_argument(
        "--rescored-at",
        default=None,
        help="Explicit ISO timestamp for reproducible rebuilds",
    )
    args = parser.parse_args()
    sys.path.insert(0, str(args.harness.resolve()))
    from fin_eval.models import TargetResponse
    from fin_eval.runner import (
        _case_result,
        _category_breakdown,
        failures_csv,
        gate_summary,
        html_report,
        load_cases,
        markdown_report,
        summarize_results,
    )
    from fin_eval.scoring import SCORER_VERSION

    root = Path(__file__).resolve().parent
    suite = root / "provenance/legacy_core_v1.yaml"
    cases = {case.id: case for case in load_cases(suite)}
    stamp = args.rescored_at or datetime.now(timezone.utc).isoformat()
    runs = {}
    for name in ("live", "mock"):
        source = root / "historical/2026-07-13/v1" / name / "results.json"
        original = json.loads(source.read_text())
        payload = dict(original)
        payload["results"] = []
        for row in original["results"]:
            response = TargetResponse(
                **{
                    key: row[key]
                    for key in (
                        "answer",
                        "citations",
                        "raw_response",
                        "latency_ms",
                        "model",
                        "input_tokens",
                        "output_tokens",
                        "estimated_cost_usd",
                        "error",
                    )
                }
            )
            payload["results"].append(_case_result(cases[row["case_id"]], response))
        payload["summary"] = summarize_results(payload["results"])
        payload["category_breakdown"] = _category_breakdown(payload["results"])
        payload["gate"] = gate_summary(
            payload["summary"], original["gate"]["thresholds"]
        )
        payload["passed"] = payload["gate"]["passed"]
        payload["metadata"] = {
            **original["metadata"],
            "scorer_version": SCORER_VERSION,
            "rescored_at": stamp,
            "suite_version": "legacy-core/v1",
            "evaluation_mode": "historical-capture-rescore",
            "rubric_evaluation": "not_performed",
            "suite_sha256": hashlib.sha256(suite.read_bytes()).hexdigest(),
            "original_artifact": str(source.relative_to(root)),
            "original_artifact_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "original_execution_metadata": original["metadata"],
            "provenance_note": "Offline rescoring of captured responses with the unchanged legacy suite; no target calls.",
        }
        dest = root / name
        for filename, content in {
            "results.json": json.dumps(payload, indent=2) + "\n",
            "summary.md": markdown_report(payload),
            "report.html": html_report(payload),
            "failures.csv": failures_csv(payload["results"]),
        }.items():
            (dest / filename).write_text(content, encoding="utf-8")
        runs[name] = payload
    values = {"rescored_at": stamp, "scorer_version": SCORER_VERSION}
    for name, run in runs.items():
        summary = run["summary"]
        values.update(
            {
                f"{name}_passed": summary["passed_cases"],
                f"{name}_overall": f"{summary['overall_score']:.3f}",
                f"{name}_refusal": f"{summary['refusal_accuracy']:.2f}",
                f"{name}_evaluated": summary["behavior_evaluated_cases"],
                f"{name}_unavailable": summary["behavior_unavailable_cases"],
            }
        )
    values["category_rows"] = "\n".join(
        f"        <tr><td>{category}</td><td>{s['total_cases']}</td><td>{s['overall_score']:.2f}</td>"
        f"<td>{s['refusal_accuracy']:.2f} ({s['behavior_evaluated_cases']} evaluated)</td>"
        f"<td>{s['severe_hallucination_count']}</td><td>{s['error_rate']:.2f}</td></tr>"
        for category, s in runs["live"]["category_breakdown"].items()
    )
    (root / "index.html").write_text(
        Template((root / "index.template.html").read_text()).substitute(values)
    )
    print(json.dumps({name: run["summary"] for name, run in runs.items()}, indent=2))


if __name__ == "__main__":
    main()
