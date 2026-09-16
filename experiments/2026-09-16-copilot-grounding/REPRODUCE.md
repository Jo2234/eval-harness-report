# Reproduce the before/after comparison

Use Python 3.11 and keep the three repositories adjacent. Fetch the candidate branch from `Jo2234/ai-equity-research-copilot`. Start from the report repository root. Use a **new** `RUN_DIR`; scripts refuse to overwrite existing state/capture directories.

```sh
git -C ../financial-llm-eval-harness checkout 4136fa1fa5375ff4f77061a1eb711250763635e3
git -C ../ai-equity-research-copilot worktree add --detach ../equity-before 6d75e16b88326b72218b35cad0add0840de2fc4b
git -C ../ai-equity-research-copilot worktree add --detach ../equity-after a4815435a6233ec646a729ca965d724888ef1a97
python3.11 -m venv .venv
.venv/bin/pip install -r experiments/2026-09-16-copilot-grounding/requirements.txt
.venv/bin/pip install --no-deps -e ../financial-llm-eval-harness
```

`requirements.txt` pins the evaluation environment, including PyMuPDF 1.26.7 and BeautifulSoup 4.13.4 used to verify source normalization. Markdown 3.10.2 is only needed to run the report repository's separate display tests. Use the unchanged benchmark scripts from report commit `e6ea9646836eabbab4030ecee157f70ab6315de7`; this report's branch does not modify them.

Set `SOURCE_DIR` to the directory containing the exact 16 raw `.html`/`.pdf` snapshots and normalized `.txt` files. If unavailable, follow [the existing source-fetch instructions](../../benchmark/README.md). Fetching changed issuer pages is not an acceptable substitute: the runner rejects hash drift. No source or reference-answer substitution is permitted.

In two terminals, from the report repository root, start the APIs using the same absolute run directory:

```sh
RUN_DIR=/absolute/path/to/new-copilot-comparison
.venv/bin/python benchmark/serve.py --copilot ../equity-before --state "$RUN_DIR/before-state" --port 8766
```

```sh
RUN_DIR=/absolute/path/to/new-copilot-comparison
.venv/bin/python benchmark/serve.py --copilot ../equity-after --state "$RUN_DIR/after-state" --port 8767
```

In a third terminal, run ingestion and capture sequentially. Both servers explicitly use the deterministic local provider; do not enable auto fallback or inject benchmark references.

```sh
RUN_DIR=/absolute/path/to/new-copilot-comparison
SOURCE_DIR=/absolute/path/to/verified-sources
.venv/bin/python benchmark/ingest.py --copilot ../equity-before --harness ../financial-llm-eval-harness --sources "$SOURCE_DIR" --work "$RUN_DIR/before-ingestion" --api http://127.0.0.1:8766
.venv/bin/python benchmark/run.py --copilot ../equity-before --harness ../financial-llm-eval-harness --sources "$SOURCE_DIR" --ingestion "$RUN_DIR/before-ingestion/equity-ingestion.json" --api http://127.0.0.1:8766 --out "$RUN_DIR/before"
.venv/bin/python benchmark/ingest.py --copilot ../equity-after --harness ../financial-llm-eval-harness --sources "$SOURCE_DIR" --work "$RUN_DIR/after-ingestion" --api http://127.0.0.1:8767
.venv/bin/python benchmark/run.py --copilot ../equity-after --harness ../financial-llm-eval-harness --sources "$SOURCE_DIR" --ingestion "$RUN_DIR/after-ingestion/equity-ingestion.json" --api http://127.0.0.1:8767 --out "$RUN_DIR/after"
.venv/bin/fin-eval compare --baseline "$RUN_DIR/before/copilot-local" --candidate "$RUN_DIR/after/copilot-local" --gate --out "$RUN_DIR/comparison"
```

Compare the source/suite/scorer hashes before interpreting deltas. UUIDs and timings vary. Quality scores should reproduce with these pinned inputs. Keep both original directories immutable. Use `benchmark/export_public.py` to create new, explicitly redacted public exports; never replace captured scores by rescoring redacted prose. The existing runner's provider-selection description includes an unavailable local Ollama endpoint; that condition was checked for this capture. For a different environment, disclose its actual availability separately while retaining explicit local mode.

To inspect the committed export without making target calls:

```sh
.venv/bin/fin-eval compare --baseline experiments/2026-09-16-copilot-grounding/before --candidate experiments/2026-09-16-copilot-grounding/after --gate
```
