"""Offline checks of archive integrity and the corrected published artifacts."""

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HARNESS = ROOT.parent / "financial-llm-eval-harness"


def hashes(directory):
    return {
        str(path.relative_to(directory)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in directory.rglob("*")
        if path.is_file()
    }


class RescoreTests(unittest.TestCase):
    def test_offline_rescore_preserves_capture_and_is_reproducible(self):
        with tempfile.TemporaryDirectory() as temp:
            copy = Path(temp) / "report"
            shutil.copytree(
                ROOT, copy, ignore=shutil.ignore_patterns(".git", "__pycache__")
            )
            archive = copy / "historical/2026-07-13/v1"
            before = hashes(archive)
            cmd = [
                sys.executable,
                str(copy / "rescore.py"),
                "--harness",
                str(HARNESS),
                "--rescored-at",
                "2026-09-06T00:00:00+00:00",
            ]
            subprocess.run(cmd, check=True, capture_output=True)
            self.assertEqual(hashes(archive), before)
            for name in ("live", "mock"):
                old = json.loads((archive / name / "results.json").read_text())
                new = json.loads((copy / name / "results.json").read_text())
                self.assertEqual(
                    new["metadata"]["original_execution_metadata"], old["metadata"]
                )
                self.assertEqual(
                    new["metadata"]["started_at"], old["metadata"]["started_at"]
                )
                self.assertEqual(
                    [r["raw_response"] for r in new["results"]],
                    [r["raw_response"] for r in old["results"]],
                )
                self.assertEqual(
                    [r["answer"] for r in new["results"]],
                    [r["answer"] for r in old["results"]],
                )
                for filename in ("summary.md", "report.html"):
                    report = (copy / name / filename).read_text()
                    self.assertIn("Historical response rescore", report)
                    self.assertIn("2026-09-06T00:00:00+00:00", report)
                    self.assertIn("no new target requests", report)
            live = json.loads((copy / "live/results.json").read_text())["summary"]
            self.assertEqual(live["behavior_evaluated_cases"], 19)
            self.assertEqual(live["behavior_unavailable_cases"], 31)
            self.assertEqual(live["severe_hallucination_count"], 2)
            self.assertAlmostEqual(live["refusal_accuracy"], 17 / 19)
            generated = hashes(copy / "live") | {
                "index": (copy / "index.html").read_text()
            }
            subprocess.run(cmd, check=True, capture_output=True)
            self.assertEqual(
                generated,
                hashes(copy / "live") | {"index": (copy / "index.html").read_text()},
            )
            self.assertEqual(hashes(archive), before)


if __name__ == "__main__":
    unittest.main()
