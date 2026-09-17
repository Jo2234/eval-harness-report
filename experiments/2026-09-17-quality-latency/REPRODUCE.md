# Reproduce PDF, answer-selection and cache validation

Use Python 3.11, the [pinned environment and corpus setup](../2026-09-16-copilot-grounding/REPRODUCE.md), and the unchanged benchmark scripts. Create these worktrees instead of the old experiment's revisions:

```sh
git -C ../ai-equity-research-copilot worktree add --detach ../equity-before 62c121cbb60d8a488bcaa9a8ad7a0ddcbc7f0820
git -C ../ai-equity-research-copilot worktree add --detach ../equity-after d25da954e316736bb4615e613c13cf54c493153e
```

Run the linked `serve.py`, `ingest.py` and `run.py` commands on ports 8766/8767 with new state, ingestion and capture directories. Reingest all 16 hash-verified raw sources through each revision's production parser; do not copy one version's chunks into the other. Provider remains explicitly local, without an LLM. Source bytes, cases, scorer, thresholds, embedding dimensions, chunk target/overlap and top-k are unchanged; PDF paragraph handling intentionally differs.

After both targets have completed exactly the same 50 requests and no extra chat requests, run:

```sh
EXPERIMENT=experiments/2026-09-17-quality-latency
.venv/bin/fin-eval compare --baseline "$RUN_DIR/before/copilot-local" --candidate "$RUN_DIR/after/copilot-local" --gate --out "$RUN_DIR/comparison"
.venv/bin/python "$EXPERIMENT/check-timing.py" --before-ingestion "$RUN_DIR/before-ingestion/equity-ingestion.json" --after-ingestion "$RUN_DIR/after-ingestion/equity-ingestion.json" --results "$RUN_DIR/before/copilot-local/results.json" --out "$RUN_DIR/timing-check.json"
```

The timing script excludes one warmup round, then alternates target order for five rounds of three fixed questions. Both servers retain growing chat histories. It is a small local sample, not a concurrency or load benchmark. The corpus cache is bounded to eight company scopes and is warm after the full suite. Cold preparation still costs work; do not present warm-cache speed as first-request latency.

For Adobe, use the [prior experiment's frozen sources and checker](../2026-09-17-financial-evidence/REPRODUCE.md), substituting these worktrees and new capture filenames.

For Oracle, fetch the complete official PDFs, keeping the frozen manifest in place. The fetcher rejects source drift. The combined Q4/FY2025 release intentionally has fiscal year metadata without a single quarter; do not relabel it to improve results.

```sh
.venv/bin/python "$EXPERIMENT/oracle/fetch.py"
.venv/bin/python "$EXPERIMENT/oracle/check.py" --copilot ../equity-before --sources "$EXPERIMENT/oracle/sources" --cases "$EXPERIMENT/oracle/cases.json" --ticker ORCL --company 'Oracle Corporation' --out "$RUN_DIR/oracle-before.json"
.venv/bin/python "$EXPERIMENT/oracle/check.py" --copilot ../equity-after --sources "$EXPERIMENT/oracle/sources" --cases "$EXPERIMENT/oracle/cases.json" --ticker ORCL --company 'Oracle Corporation' --out "$RUN_DIR/oracle-after.json"
```

Oracle's runner and questions were frozen before candidate inspection; hashes are recorded in `oracle/freeze.json`. Its failures later informed the continuation-line and explicit-period fixes, so final results are development validation, not independently held-out accuracy. No reference fact or source-document identifier enters chat requests. The checks measure numerical pattern presence, source coverage and refusal shape, not semantic entailment or precise number-to-label binding.

Preserve original captures. Use `benchmark/export_public.py` for the main suite and `oracle/export.py` for Oracle public exports; published answers and source excerpts are omitted, scores and fingerprints retained. Redacted exports cannot independently rescore answer text. Quality should reproduce with pinned inputs; UUIDs and timings vary.
