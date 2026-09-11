"""Synthetic regression checks for benchmark isolation and source provenance."""
import hashlib
import json
import importlib.util
from pathlib import Path
from types import SimpleNamespace
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("benchmark_run", Path(__file__).parents[1] / "benchmark/run.py")
benchmark = importlib.util.module_from_spec(spec)
spec.loader.exec_module(benchmark)


class BenchmarkTests(unittest.TestCase):
    def test_saved_capture_integrity_and_denominators(self):
        run = Path(__file__).parents[1] / "current/2026-09-11"
        inventory = json.loads((run / "SHA256SUMS.json").read_text())
        for name, digest in inventory.items():
            self.assertEqual(hashlib.sha256((run / name).read_bytes()).hexdigest(), digest, name)
        traces = [json.loads(line) for line in (run / "captures.jsonl").read_text().splitlines()]
        self.assertEqual(len(traces), 100)
        mapping = json.loads((run / "document-map.json").read_text())
        for target, passes in [("copilot-local", 0), ("lexical-baseline", 2)]:
            rows = json.loads((run / target / "results.json").read_text())["results"]
            captures = {row["case_id"]: row for row in traces if row["target"] == target}
            self.assertEqual(len(rows), 50)
            self.assertEqual(len(captures), 50)
            self.assertEqual(sum(row["passed"] for row in rows), passes)
            expected_refusals = [row for row in rows if row["case_definition"]["refusal_expected"]]
            self.assertEqual(len(expected_refusals), 7)
            self.assertEqual(sum(row["refusal_correct"] for row in expected_refusals), 0)
            self.assertTrue(all(row["execution_status"] == "answered" for row in rows))
            for row in rows:
                capture = captures[row["case_id"]]
                raw = capture["raw_response"]
                self.assertEqual(benchmark.sha(json.dumps(raw, sort_keys=True).encode()), capture["public_response_sha256"])
                self.assertEqual(capture["response_sha256"], capture["public_export"]["original_response_sha256"])
                self.assertNotIn("answer", raw)
                self.assertEqual(set(capture["request"]), {"question", "company_ids", "top_k"})
                self.assertEqual(capture["request"]["question"], row["question"])
                self.assertEqual(capture["public_export"]["answer_sha256"], row["answer_sha256"])
                self.assertIn("omitted", row["answer"])
                self.assertNotIn("excerpt", str(raw.keys()))
                if target == "copilot-local":
                    self.assertEqual(raw["usage"]["provider"], "local")
                    self.assertEqual([mapping[c["document_id"]] for c in raw["citations"]],
                                     [c["document_id"] for c in row["citations"]])

    def test_public_export_removes_nested_response_prose_without_mutating_original(self):
        export_spec = importlib.util.spec_from_file_location("public_export", Path(__file__).parents[1] / "benchmark/export_public.py")
        export = importlib.util.module_from_spec(export_spec)
        export_spec.loader.exec_module(export)
        original = {"answer": "source prose", "key_points": ["copied prose"],
                    "citations": [{"document_id": "doc", "excerpt": "source excerpt", "score": 0.4}],
                    "retrieval_debug": {"chunks": [{"id": "chunk", "excerpt": "more source"}]}}
        public = export.redact(original)
        self.assertEqual(public, {"citations": [{"document_id": "doc", "score": 0.4}],
                                  "retrieval_debug": {"chunks": [{"id": "chunk"}]}})
        self.assertEqual(original["answer"], "source prose")
        self.assertEqual(original["citations"][0]["excerpt"], "source excerpt")

    def test_target_request_does_not_include_evaluator_answers_or_selected_documents(self):
        case = SimpleNamespace(question="What changed?", company_ids=["EXAMPLE"],
                               documents=["secret_selection"], expected_answer_points=["secret_answer"],
                               judge_rubric="secret_rubric", source_evidence=["secret_facts"], id="case1")
        self.assertEqual(benchmark.request_for(case), {"question": "What changed?", "company_ids": ["EXAMPLE"], "top_k": 8})

    def test_baseline_has_company_scope_and_stable_document_ties(self):
        baseline = benchmark.LexicalBaseline([
            {"company": "OTHER", "document_id": "a", "text": "revenue profit unrelated company"},
            {"company": "EXAMPLE", "document_id": "z", "text": "revenue profit later"},
            {"company": "EXAMPLE", "document_id": "b", "text": "revenue profit first"},
        ])
        answer = baseline.answer("revenue profit", ["EXAMPLE"])
        self.assertEqual([row["document_id"] for row in answer["citations"]], ["b", "z"])
        self.assertNotIn("unrelated", answer["answer"])
        self.assertEqual(baseline.answer("zzzz", ["EXAMPLE"])["citations"], [])

    def test_citation_mapping_preserves_raw_response_and_unknown_ids(self):
        raw = {"answer": "unchanged", "citations": [{"document_id": "uuid"}, {"document_id": "unknown"}]}
        mapped = benchmark.normalized_payload(raw, {"uuid": "canonical"})
        self.assertEqual(mapped["citations"][0]["document_id"], "canonical")
        self.assertEqual(mapped["citations"][1]["document_id"], "unknown")
        self.assertEqual(raw["citations"][0]["document_id"], "uuid")

    def test_source_hash_drift_is_rejected_before_target_execution(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "example.html").write_text("original source")
            (root / "example.txt").write_text("source text")
            manifest = {"documents": [{"document_id": "example", "sha256": benchmark.sha(b"original source")}],
                        "evidence": [{"document_id": "example", "evidence_id": "one", "context_start_character": 0,
                                      "normalized_text_sha256": benchmark.sha(b"source text"),
                                      "context_sha256": benchmark.sha(b"source text"), "facts": ["never supplied"]}]}
            documents, _ = benchmark.verified_sources(root, manifest)
            self.assertEqual(documents[0]["text"], "source text")
            self.assertNotIn("facts", documents[0])
            (root / "example.txt").write_text("changed source")
            with self.assertRaisesRegex(ValueError, "Changed normalized source"):
                benchmark.verified_sources(root, manifest)


if __name__ == "__main__":
    unittest.main()
