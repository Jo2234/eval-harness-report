# Reproduce financial evidence checks

Use Python 3.11 and the [pinned environment and full-corpus setup](../2026-09-16-copilot-grounding/REPRODUCE.md). Start from this report repository. Replace that experiment's worktrees with:

```sh
git -C ../ai-equity-research-copilot worktree add --detach ../equity-before d4dfb2041adddd31e1e3071a286f9188b25415b1
git -C ../ai-equity-research-copilot worktree add --detach ../equity-after 9d40cb7d995490eab481c09bef200086e6a0c827
```

Run the unchanged `benchmark/serve.py`, `ingest.py` and `run.py` as documented there, with fresh state, ingestion and capture directories. Both full suites must finish before the timing check. Do not reuse the earlier experiment's additional timing calls. Use a new absolute `RUN_DIR` and ports 8766/8767:

```sh
EXPERIMENT=experiments/2026-09-17-financial-evidence
.venv/bin/fin-eval compare --baseline "$RUN_DIR/before/copilot-local" --candidate "$RUN_DIR/after/copilot-local" --gate --out "$RUN_DIR/comparison"
.venv/bin/python "$EXPERIMENT/check-timing.py" --before-ingestion "$RUN_DIR/before-ingestion/equity-ingestion.json" --after-ingestion "$RUN_DIR/after-ingestion/equity-ingestion.json" --results "$RUN_DIR/before/copilot-local/results.json" --out "$RUN_DIR/timing-check.json"
```

For the separate Adobe check, fetch complete official PDFs. Hash drift is rejected; do not substitute new source content or change the frozen cases. The 8-K metadata identifies earnings releases, not annual 10-K filings. Each checker run uses its own temporary, unseeded corpus and the production upload/chat APIs:

```sh
.venv/bin/python "$EXPERIMENT/fetch-sources.py" --out "$RUN_DIR/adobe-sources"
.venv/bin/python "$EXPERIMENT/check-fresh-documents.py" --copilot ../equity-before --sources "$RUN_DIR/adobe-sources" --cases "$EXPERIMENT/fresh-cases.json" --out "$RUN_DIR/fresh-before.json"
.venv/bin/python "$EXPERIMENT/check-fresh-documents.py" --copilot ../equity-after --sources "$RUN_DIR/adobe-sources" --cases "$EXPERIMENT/fresh-cases.json" --out "$RUN_DIR/fresh-after.json"
```

Quality scores should reproduce with pinned inputs; UUIDs and timings vary. Preserve complete captures locally. Use unchanged `benchmark/export_public.py` for the 50-case public exports. Published Adobe records omit answer text and citation excerpts while retaining answer hashes and unchanged checks. Do not rescore redacted text. Neither this report nor these runs use a live LLM.
