"""Offline display rebuilds preserve measured data and use the durable renderer."""

import hashlib
import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "current/2026-09-11"
HARNESS = ROOT.parent / "financial-llm-eval-harness"


class PresentationTests(unittest.TestCase):
    def test_display_rebuild_is_repeatable_and_preserves_data_and_archive(self):
        paths = [
            p
            for p in RUN.rglob("*")
            if p.is_file() and p.suffix != ".html" and p.name != "SHA256SUMS.json"
        ]
        paths += [p for p in (ROOT / "historical").rglob("*") if p.is_file()]
        before = {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        spec = importlib.util.spec_from_file_location(
            "display_render", ROOT / "benchmark/render.py"
        )
        renderer = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(renderer)
        renderer.render(HARNESS)
        first = (RUN / "index.html").read_bytes()
        renderer.render(HARNESS)
        self.assertEqual(first, (RUN / "index.html").read_bytes())
        self.assertEqual(
            before, {p: hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
        )
        sys.path.insert(0, str(HARNESS))
        from fin_eval.runner import html_report

        for target in ["copilot-local", "lexical-baseline"]:
            data = json.loads((RUN / target / "results.json").read_text())
            self.assertEqual(
                (RUN / target / "report.html").read_text(), html_report(data)
            )
            self.assertEqual(len(data["results"]), 50)
        inventory = json.loads((RUN / "SHA256SUMS.json").read_text())
        for name, digest in inventory.items():
            self.assertEqual(
                hashlib.sha256((RUN / name).read_bytes()).hexdigest(), digest
            )


if __name__ == "__main__":
    unittest.main()
