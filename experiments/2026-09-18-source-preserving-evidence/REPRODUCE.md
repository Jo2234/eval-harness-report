# Reproduce the source-preserving evidence check

Use Python 3.11 and the [pinned environment and full-corpus setup](../2026-09-16-copilot-grounding/REPRODUCE.md). Commands are relative to this report repository, with repositories adjacent. Check out harness `4136fa1fa5375ff4f77061a1eb711250763635e3` and create the candidate worktree:

```sh
git -C ../ai-equity-research-copilot worktree add --detach ../equity-c8f4740 c8f474036879081a8cabdf4381829ab008731970
```

Obtain the exact 16 raw/normalized snapshots using [the existing fetch instructions](../../benchmark/README.md). Hash mismatches are reproducibility failures; do not substitute changed sources. Use new absolute paths for `SOURCE_DIR` and `RUN_DIR` (the latter must not contain an earlier run). Start the API in one terminal:

```sh
python benchmark/serve.py --copilot ../equity-c8f4740 --state "$RUN_DIR/api-state" --port 8773
```

In another terminal, upload complete documents through the production parser and run the unchanged suite:

```sh
python benchmark/ingest.py --copilot ../equity-c8f4740 --harness ../financial-llm-eval-harness --sources "$SOURCE_DIR" --work "$RUN_DIR/ingestion" --api http://127.0.0.1:8773
python benchmark/run.py --copilot ../equity-c8f4740 --harness ../financial-llm-eval-harness --sources "$SOURCE_DIR" --ingestion "$RUN_DIR/ingestion/equity-ingestion.json" --api http://127.0.0.1:8773 --out "$RUN_DIR/capture"
python benchmark/export_public.py --captured "$RUN_DIR/capture" --out "$RUN_DIR/public" --harness ../financial-llm-eval-harness
```

The capture records API and lexical-baseline calls in suite order, with no retries or warmup. Only question, company scope and top-k enter chat requests. Source IDs and expected facts remain in the evaluator. The runner preserves the 50-case suite SHA-256 `1eaf08f68d6df324e95df38f6b6ac87850d2125c0602f61249ea467caaf9e0cb` and unchanged scorer/thresholds. A failing absolute gate must stay visible.

Compare saved scores against the published previous candidate:

```sh
fin-eval compare --baseline experiments/2026-09-17-quality-latency/after --candidate "$RUN_DIR/capture/copilot-local" --gate --out "$RUN_DIR/comparison"
```

This compares case fingerprints and scores; it does not rescore the baseline's redacted answer text. To rerun that implementation, use a separate worktree at `d25da954e316736bb4615e613c13cf54c493153e` and fresh directories. No controlled alternating timing experiment was performed for this report.

For Adobe, use the frozen [fetcher/checker and cases](../2026-09-17-financial-evidence/REPRODUCE.md), passing `../equity-c8f4740` and new output paths. For Oracle, follow the frozen [Oracle instructions](../2026-09-17-quality-latency/REPRODUCE.md) with the same candidate. Both checkers create temporary unseeded corpora and verify full PDF hashes. Preserve source metadata, including Oracle's combined annual/fourth-quarter release without single-quarter metadata.

The public fresh-check files were created by applying the existing `benchmark.export_public.redact` helper recursively to the original captures, then adding SHA-256 fingerprints of original answers and capture bytes. Adobe's local checker has the same Python AST as the published formatted checker; Oracle's checker is byte-identical. Their full hashes are in [fresh-verification.json](fresh-verification.json). Do not publish original response prose or PDFs.

Public exports retain unchanged scores. `ORIGINAL_SHA256SUMS.json` fingerprints local originals; `SHA256SUMS.json` fingerprints public derivatives. This report also removes `ingestion.health.data_dir` from its public derivative and records that additional path-only redaction in `PUBLIC_EXPORT.json`; the corresponding public hashes were updated. Scores and source hashes were not changed.
