# Reproduce the table-evidence comparison

Follow the [previous environment and source setup](../2026-09-16-copilot-grounding/REPRODUCE.md), using its pinned `requirements.txt`, Python 3.11, and the exact raw source snapshots. Use these two Copilot worktrees instead:

```sh
git -C ../ai-equity-research-copilot worktree add --detach ../equity-table-before af7e62bdcaeae2c8becec0652c2395be6fce44ff
git -C ../ai-equity-research-copilot worktree add --detach ../equity-table-after 5b5cb23b77d679cf29a91ab8fecd9044471c9a24
```

Start `benchmark/serve.py` against each worktree using fresh state directories on ports 8766 and 8767. Run the unchanged `benchmark/ingest.py` and `benchmark/run.py` from the linked instructions, substituting these worktree paths and a new absolute run directory. Run both complete 50-case suites before timing. Original captured directories must never be overwritten.

The source production code at the baseline merge is identical to the earlier report's `a481543` candidate. Verify suite/scorer/source hashes and case compatibility before interpreting deltas. The CLI comparison is:

```sh
.venv/bin/fin-eval compare --baseline experiments/2026-09-16-table-evidence/before --candidate experiments/2026-09-16-table-evidence/after --gate
```

Run the additional synthetic checks from the report root:

```sh
.venv/bin/python experiments/2026-09-16-table-evidence/check-fresh.py --copilot ../equity-table-before --cases experiments/2026-09-16-table-evidence/fresh-cases.json --out /tmp/fresh-before.json
.venv/bin/python experiments/2026-09-16-table-evidence/check-fresh.py --copilot ../equity-table-after --cases experiments/2026-09-16-table-evidence/fresh-cases.json --out /tmp/fresh-after.json
```

The frozen synthetic case hash is `094699874cf167d1dbf0c19a18b64a76f348285feb4263f3766f33b9623417da`. Dynamic document UUIDs differ across runs; checks compare values and distinct-document counts, not fixed UUIDs. No reference output enters the model or retrieval API.

Use the unchanged `benchmark/export_public.py` for new redacted filing exports. The original runner's provider description mentions unavailable Ollama; this run explicitly used local deterministic mode and made no model calls. Fresh availability must be checked separately for another environment; provider fallback must not be enabled for a comparable run.

For a balanced timing check, first run the full suite on both APIs, then use equivalent warmup/history counts. The saved check used one additional earlier timing round on both targets; record any setup difference. Run:

```sh
.venv/bin/python experiments/2026-09-16-table-evidence/check-timing.py --before-ingestion "$RUN_DIR/before-ingestion/equity-ingestion.json" --after-ingestion "$RUN_DIR/after-ingestion/equity-ingestion.json" --results "$RUN_DIR/before/copilot-local/results.json" --out "$RUN_DIR/timing-check.json"
```
