# Reproduce the fresh comparison

The September 11 run evaluates the existing deterministic Equity Copilot API against a simple lexical retrieval baseline on the current 50-case factual suite. **Neither target uses an LLM.** No expected answer, rubric, source-evidence facts, selected-document list, or reference fixture is sent to either target. The API receives only question text, company ticker scope, and `top_k=8`.

## Inputs and provenance

The run uses 16 complete primary documents already fetched on September 6 and pinned by the harness. All 16 raw files, 16 normalized source texts, and 40 evidence-context hashes were independently checked before execution. The normalization used to verify curation provenance is not used as the API upload format.

For the actual corpus, HTML passes through the unmodified Copilot `sec.html_to_text`; PDFs pass through its ordinary upload/parser path. The resulting paragraph-preserving corpus has 1,311 API chunks. The baseline receives those same complete extracted document texts, with separate extraction hashes in `ingestion.json`. No source passages were selected based on answer keys. An initial preparation using flattened normalized text was abandoned before any benchmark calls; only the source-faithful ingestion was measured. Complete documents are uploaded; the SEC network downloader's 600,000-character limit is not invoked.

The API is a fresh `create_app(..., seed=False)` instance with six companies and no seeded demo documents. Import-time demo creation is isolated in another data directory. Settings: 128 embedding dimensions, target 800 tokens per chunk, 80-token overlap, retrieval threshold 0.04, 10 MB upload limit. The provider is explicitly `local`, model label `local-deterministic-grounded-v1`; the unavailable local Ollama endpoint prompted this choice, and no automatic provider fallback or paid request occurs during the run.

`config.json` records source/config/runner hashes, clean harness and Copilot commit SHAs, and the unchanged Copilot backend tree. The original local `captures.jsonl` retains all 100 fresh calls with requests, timestamps, raw responses, and response hashes. The public file is an explicitly redacted export: extractive answer text, key points, and source excerpts are omitted, while original response/answer hashes, requests, timing and citation metadata remain. The common request envelope in the trace includes `top_k=8`; the baseline ignores that API-only field and uses its fixed top-three rule. API document UUIDs are mapped to suite IDs only for scoring using the recorded upload map; local raw captures retain original UUIDs; public records retain those IDs but omit source prose. Scored cases include full case definitions and fingerprints. `ORIGINAL_SHA256SUMS.json` preserves hashes of the original captured files; those hashes do not describe the redacted public files. `SHA256SUMS.json` instead covers the explicit public export, including its policy and original hash inventory. Explanatory pages and review notes are editorial derivatives outside those inventories. Public redacted data cannot independently rescore answer text without original local or newly reproduced captures. Scores were computed on complete original responses and were not changed by export.

The `ingestion_manifest_sha256` in config identifies the original local ingestion manifest, including local file paths. Published `ingestion.json` removes those paths and has its own hash in `SHA256SUMS.json`; these two hashes intentionally differ. The source-provenance and document-map hashes use canonical sorted JSON as implemented by the runner. Public capture records keep the original `response_sha256` and provide a separate `public_response_sha256` for their redacted payload; these are intentionally different.

Raw full filings stay outside this repository; their URLs, fiscal periods, hashes, and extraction details are published. SEC filings and issuer-hosted transcripts retain their source attribution and third-party rights. NVIDIA's issuer-hosted call is a FactSet corrected transcript, not a claim of issuer authorship. Do not treat a later changed web page as the pinned snapshot.

## Baseline fixed before the run

Split complete extracted text into non-overlapping 1,200-character chunks. Score each chunk by the number of distinct lowercase alphanumeric question tokens it contains after removing a fixed stopword list. Restrict to the same requested company tickers, then select the top three positive-overlap chunks; ties use document ID and character offset. Concatenate the first 400 characters of each selected chunk and cite their document IDs. Refuse only when all overlaps are zero. This is an intentionally simple extractive baseline, without a model, synthesis, period filtering, or a financial refusal policy. The exact configuration and stopwords are in `run.py`.

## Running again

Use the source commits recorded in the published `config.json`. Install harness 0.2.0 and the Equity backend requirements into a virtual environment; the source-fetch helper additionally needs `beautifulsoup4==4.13.4` and `pymupdf==1.26.7` (the normalization versions checked against all 16 saved raw sources). Keep the three repositories adjacent. Paths below are relative to this report repository.

Obtain the exact raw and normalized snapshots. If they are unavailable locally, the optional fetch helper downloads the manifest URLs and rejects changed raw or normalized hashes:

```sh
python benchmark/fetch_sources.py \
  --manifest ../financial-llm-eval-harness/evals/evidence/manifest.yaml \
  --out /tmp/financial-sources --user-agent 'Your Name your-contact@example.com'
```

Issuer markup or extraction-library changes can prevent a byte-identical download. A failed hash is an explicit reproducibility obstacle; retain the old run and deliberately curate/version any replacement corpus. Never substitute the reference answers for missing sources.

Start the actual API in one terminal:

```sh
python benchmark/serve.py --copilot ../ai-equity-research-copilot \
  --state /tmp/financial-eval-api-new --port 8766
```

In another terminal:

```sh
python benchmark/ingest.py --copilot ../ai-equity-research-copilot \
  --harness ../financial-llm-eval-harness --sources /tmp/financial-sources \
  --work /tmp/financial-eval-ingestion-new
python benchmark/run.py --harness ../financial-llm-eval-harness \
  --copilot ../ai-equity-research-copilot --sources /tmp/financial-sources \
  --ingestion /tmp/financial-eval-ingestion-new/equity-ingestion.json \
  --out /tmp/financial-eval-run-new
```

Every state/output directory must be new. Questions run in suite order, API then baseline, once each, with no warmup or retries. Responses and latencies are newly captured; do not overwrite the September run. Source retrieval and corpus ingestion time are excluded from answer latency. Each answer call is measured with `perf_counter`; API timing includes local HTTP and conversation persistence, while baseline timing is in-process and quantized to integer milliseconds. A 0 ms baseline median means sub-millisecond measurements rounded down, not zero execution time. These timings are not an apples-to-apples service speedup or a model inference benchmark.

To create an explicit public export of a newly captured run without changing its scores:

```sh
python benchmark/export_public.py --captured /tmp/financial-eval-run-new \
  --out /tmp/financial-eval-public-new --harness ../financial-llm-eval-harness
```

Keep the original run outside the public repository. The export removes source/answer prose from all targets, including filings and transcripts; it does not replace or alter any measured score.

For an offline display rebuild of the saved public run:

```sh
python -m pip install -r benchmark/requirements-render.txt
python benchmark/render.py
python -m unittest discover -s tests
```

Tests check target-input isolation, source drift rejection, baseline scope/ties, citation identity mapping, public-export integrity/denominators, and original July archive/rebuild behavior. Original response text, all baseline answers and per-case scoring were independently reproduced locally before export; that full text audit cannot be repeated from public redacted records alone. They do not issue target requests. The original `rescore.py` still rebuilds the separate July rescore; it cannot regenerate fresh September responses.
