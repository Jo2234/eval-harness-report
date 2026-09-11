"""Fresh HTTP Copilot and lexical baseline captures; requires harness 0.2.0.

Targets receive questions and company scopes, never evaluator facts or reference
responses. Full local source snapshots must match the current evidence manifest.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx
import yaml

STOPWORDS = set("a an and are as at be by did do does for from how in is it of on or that the their this to was were what which with".split())
BASELINE_CONFIG = {
    "algorithm": "unique lowercase alphanumeric query-token overlap, stopwords removed",
    "chunk_characters": 1200,
    "stride_characters": 1200,
    "top_k": 3,
    "answer_characters_per_chunk": 400,
    "ties": "document ID then character offset ascending",
    "scope": "all documents for requested company tickers, no case-specific document filter",
    "refusal": "only when every chunk has zero query-token overlap",
    "model": "none",
}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n")


def verified_sources(source_dir: Path, manifest: dict) -> tuple[list[dict], list[dict]]:
    """Reject drift before a target can access a source. Facts are not returned."""
    documents, provenance = [], []
    for doc in manifest["documents"]:
        doc_id = doc["document_id"]
        candidates = [source_dir / (doc_id + suffix) for suffix in (".html", ".pdf")]
        raw = next((path for path in candidates if path.exists()), None)
        if raw is None or sha(raw.read_bytes()) != doc["sha256"]:
            raise ValueError(f"Missing or changed raw source: {doc_id}")
        text = (source_dir / (doc_id + ".txt")).read_text()
        evidence = [row for row in manifest["evidence"] if row["document_id"] == doc_id]
        if not evidence:
            raise ValueError(f"No source provenance for {doc_id}")
        for row in evidence:
            pos = row["context_start_character"]
            if sha(text.encode()) != row["normalized_text_sha256"]:
                raise ValueError(f"Changed normalized source: {doc_id}")
            if sha(text[pos:pos + 1200].encode()) != row["context_sha256"]:
                raise ValueError(f"Changed pinned context: {row['evidence_id']}")
        documents.append({"document_id": doc_id, "company": doc_id.split("_")[0].upper(), "text": text})
        provenance.append({**doc, "normalized_text_sha256": sha(text.encode()),
                           "normalized_characters": len(text), "verified_contexts": len(evidence),
                           "origin": "previously fetched primary-source snapshot; independently hash-verified for this run"})
    return documents, provenance


def tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower())) - STOPWORDS


class LexicalBaseline:
    def __init__(self, documents: list[dict]):
        self.chunks = []
        for doc in sorted(documents, key=lambda row: row["document_id"]):
            for offset in range(0, len(doc["text"]), BASELINE_CONFIG["stride_characters"]):
                text = doc["text"][offset:offset + BASELINE_CONFIG["chunk_characters"]]
                self.chunks.append((doc["company"], doc["document_id"], offset, text, tokens(text)))

    def answer(self, question: str, company_ids: list[str]) -> dict:
        query = tokens(question)
        scope = {company.upper() for company in company_ids}
        ranked = [(len(query & terms), doc, offset, text)
                  for company, doc, offset, text, terms in self.chunks if company in scope]
        ranked.sort(key=lambda row: (-row[0], row[1], row[2]))
        selected = [row for row in ranked[:BASELINE_CONFIG["top_k"]] if row[0] > 0]
        return {
            "answer": "\n\n".join(row[3][:BASELINE_CONFIG["answer_characters_per_chunk"]] for row in selected)
                      if selected else "I do not have enough cited context to answer that.",
            "citations": [{"document_id": doc, "chunk_id": f"{doc}:{offset}",
                           "excerpt": text[:BASELINE_CONFIG["answer_characters_per_chunk"]],
                           "label": f"{doc}, character {offset}", "overlap": overlap}
                          for overlap, doc, offset, text in selected],
            "model": "lexical-overlap-extractive-v1-no-llm",
            "usage": {"provider": "local-baseline", "model": "none", "estimated_cost_usd": 0.0},
        }


def request_for(case) -> dict:
    # Deliberately exclude documents, evidence, IDs, rubric and reference answers.
    return {"question": case.question, "company_ids": case.company_ids, "top_k": 8}


def normalized_payload(raw: dict, mapping: dict[str, str]) -> dict:
    # Preserve the unmodified UUID-bearing response separately; only canonicalize
    # document identity for the scorer, using the recorded upload response map.
    result = json.loads(json.dumps(raw))
    for citation in result.get("citations", []):
        original = citation.get("document_id")
        citation["document_id"] = mapping.get(original, original)
    return result


def git_revision(path: Path) -> dict:
    def git(*args):
        return subprocess.check_output(["git", "-C", str(path), *args], text=True).strip()
    return {"head": git("rev-parse", "HEAD"), "worktree_status": git("status", "--porcelain")}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--harness", type=Path, required=True)
    parser.add_argument("--copilot", type=Path, required=True)
    parser.add_argument("--sources", type=Path, required=True)
    parser.add_argument("--ingestion", type=Path, required=True, help="Source-faithful API ingestion manifest")
    parser.add_argument("--api", default="http://127.0.0.1:8766")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.out.exists():
        raise SystemExit("Output already exists; choose a new capture directory rather than overwriting a run")
    sys.path.insert(0, str(args.harness.resolve()))
    from fin_eval.adapters import normalize_target_response
    from fin_eval.runner import (_case_result, _category_breakdown, artifact_manifest,
                                 cases_jsonl, failures_csv, gate_summary, html_report,
                                 load_suite, markdown_report, metrics_csv, summarize_results, validate_cases)
    from fin_eval.scoring import SCORER_VERSION

    suite_path = args.harness / "evals/core.yaml"
    evidence_path = args.harness / "evals/evidence/manifest.yaml"
    manifest = yaml.safe_load(evidence_path.read_text())
    documents, provenance = verified_sources(args.sources, manifest)
    suite = load_suite(suite_path)
    validate_cases(suite.cases, quality=True)
    ingestion = json.loads(args.ingestion.read_text())
    mapping = ingestion["document_uuid_to_canonical"]
    derived = {row["canonical_id"]: row for row in ingestion["documents"]}
    for doc in documents:
        row = derived[doc["document_id"]]
        original = next(item for item in provenance if item["document_id"] == doc["document_id"])
        if row["raw_sha256"] != original["sha256"]:
            raise ValueError("Ingested source differs from pinned raw source")
        text = Path(row["derived_text_path"]).read_text()
        if sha(text.encode()) != row["derived_text_sha256"]:
            raise ValueError("Baseline text differs from actual production extraction")
        doc["text"] = text
    if set(mapping.values()) != {doc["document_id"] for doc in documents} or len(mapping) != len(documents):
        raise ValueError("Document upload mapping must cover exactly the verified source corpus")
    baseline = LexicalBaseline(documents)
    config = {
        "capture_started_at": datetime.now(timezone.utc).isoformat(),
        "suite_sha256": sha(suite_path.read_bytes()), "evidence_manifest_sha256": sha(evidence_path.read_bytes()),
        "runner_sha256": sha(Path(__file__).read_bytes()), "harness": git_revision(args.harness),
        "copilot": git_revision(args.copilot), "scorer_version": SCORER_VERSION,
        "python": platform.python_version(), "api_base_url": args.api,
        "api_provider": "local", "api_model": "local-deterministic-grounded-v1",
        "provider_selection": "Ollama 127.0.0.1:11434 unavailable; explicitly selected AIERC_LLM_PROVIDER=local. No LLM or paid API was used.",
        "api_request_fields": ["question", "company_ids", "top_k"],
        "api_top_k": 8, "baseline": BASELINE_CONFIG,
        "source_documents": len(documents), "source_scope": "complete primary documents via production HTML/PDF extraction, not selected answer passages",
        "source_retrieved_on": manifest["retrieved_on"],
        "source_provenance_sha256": sha(json.dumps(provenance, sort_keys=True).encode()),
        "document_map_sha256": sha(json.dumps(mapping, sort_keys=True).encode()),
        "ingestion_manifest_sha256": sha(args.ingestion.read_bytes()),
        "copilot_backend_tree": subprocess.check_output(["git", "-C", str(args.copilot), "rev-parse", "HEAD:backend"], text=True).strip(),
        "api_settings": ingestion["settings"],
        "api_chunk_count": sum(row["chunk_count"] for row in ingestion["documents"]),
        "ordering": "suite order; sequential API call followed by baseline for each case; no retries or warmup",
        "latency": "wall time of each answer call; API includes loopback HTTP and persistence, baseline is in-process; excludes corpus ingestion and baseline indexing",
        "rubric_review": "not performed by scorer; selected responses receive separate qualitative review",
    }
    args.out.mkdir(parents=True)
    write_json(args.out / "config.json", config)
    write_json(args.out / "sources.json", provenance)
    write_json(args.out / "document-map.json", mapping)
    public_ingestion = {key: value for key, value in ingestion.items() if key not in {"source_dir", "documents"}}
    public_ingestion["documents"] = [{key: value for key, value in row.items() if not key.endswith("_path")} for row in ingestion["documents"]]
    write_json(args.out / "ingestion.json", public_ingestion)
    traces, scored = [], {"copilot-local": [], "lexical-baseline": []}
    target_durations = {name: 0 for name in scored}
    with httpx.Client(timeout=90, trust_env=False) as client:
        for case in suite.cases:
            for name in scored:
                request = request_for(case)
                started = time.perf_counter()
                try:
                    if name == "copilot-local":
                        response = client.post(args.api.rstrip("/") + "/research/chat", json=request)
                        response.raise_for_status()
                        raw = response.json()
                        if raw.get("usage", {}).get("provider") != "local":
                            raise ValueError("Copilot provider differs from declared local benchmark configuration")
                        value = normalized_payload(raw, mapping)
                    else:
                        raw = baseline.answer(request["question"], request["company_ids"])
                        value = raw
                except Exception as exc:
                    raw = value = {"error": f"{type(exc).__name__}: {exc}"}
                latency = int((time.perf_counter() - started) * 1000)
                target_durations[name] += latency
                traces.append({"case_id": case.id, "target": name, "request": request,
                               "captured_at": datetime.now(timezone.utc).isoformat(),
                               "latency_ms": latency, "raw_response": raw,
                               "response_sha256": sha(json.dumps(raw, sort_keys=True).encode())})
                scored[name].append(_case_result(case, normalize_target_response(value, latency)))
            (args.out / "captures.jsonl").write_text("".join(json.dumps(row, ensure_ascii=False) + "\n" for row in traces))
            print(case.id, flush=True)
    for name, details in scored.items():
        out = args.out / name
        out.mkdir()
        summary = summarize_results(details)
        gate = gate_summary(summary)
        payload = {"metadata": {"suite": "evals/core.yaml", "suite_version": suite.schema_version,
                                 "suite_kind": "quality", "target": name, "case_count": len(details),
                                 "evaluation_mode": "fresh execution; deterministic no-LLM comparison",
                                 "started_at": config["capture_started_at"], "duration_ms": target_durations[name],
                                 "scorer_version": SCORER_VERSION, "rubric_evaluation": "not_performed",
                                 "rubric_review_required_cases": len(details),
                                 "configuration_sha256": sha((args.out / "config.json").read_bytes())},
                   "summary": summary, "category_breakdown": _category_breakdown(details),
                   "passed": gate["passed"], "gate": gate, "results": details, "target": name}
        write_json(out / "results.json", payload)
        (out / "summary.md").write_text(markdown_report(payload))
        (out / "report.html").write_text(html_report(payload))
        (out / "failures.csv").write_text(failures_csv(details))
        (out / "metrics.csv").write_text(metrics_csv(payload))
        (out / "cases.jsonl").write_text(cases_jsonl(details))
        write_json(out / "manifest.json", artifact_manifest(out))
        print(name, json.dumps(summary), flush=True)
    inventory = {str(path.relative_to(args.out)): sha(path.read_bytes()) for path in args.out.rglob("*") if path.is_file()}
    write_json(args.out / "SHA256SUMS.json", inventory)


if __name__ == "__main__":
    main()
