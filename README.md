# Financial QA evaluation reports

## Fresh comparison — 11 September 2026

[Read the new comparison](current/2026-09-11/index.html) and [methodology/reproduction instructions](benchmark/README.md). Fifty current factual-suite cases were freshly executed against an isolated Equity Copilot API and a simple lexical retrieval baseline using 16 complete, hash-verified source documents. Both targets are deterministic and use **no LLM**.

The Copilot passed **0/50** strict cases; the baseline passed **2/50**. Both had zero transport errors and missed all seven expected refusals. Public exports omit extractive response prose while retaining original response hashes, citation metadata and unchanged scores; complete captures are retained locally. These results expose retrieval, answer coverage, citation alignment, and refusal limitations; they are not evidence of production readiness. See the [qualitative review](current/2026-09-11/REVIEW.md) for score limitations and representative failures.

The fresh run is separate from the July captures below. Original reports, fixtures, and provenance remain preserved.

## Historical financial QA evaluation, corrected

A supporting failure-analysis case study for the [Financial LLM Evaluation Harness](https://github.com/Jo2234/financial-llm-eval-harness), with saved responses, scoring corrections, and reproducible reports.

The responses were captured on **13 July 2026**. The root `live/` and `mock/` reports rescore those same saved responses offline with `financial-eval-scorer/v2` and the **unchanged legacy suite** in `provenance/legacy_core_v1.yaml`. They are not a fresh production run and do not measure the revised evidence-grounded quality suite.

The original HTML, JSON, Markdown, CSV, and homepage are preserved byte-for-byte in `historical/2026-07-13/v1/`. Corrected JSON retains the original execution timestamp, latency, duration, raw responses, full original execution metadata, SHA-256 of the original artifact and suite, and a separate rescoring timestamp. No model/API requests are made by rebuilding.

The correction distinguishes transport errors from behavioral evidence. Thirty-one live cases returned errors. Of the five refusal-category cases, only two returned answers; three returned HTTP 404s. Five of the original seven “severe hallucination” flags were errors without answers. Scorer v2 excludes error/empty responses from refusal accuracy and reports the denominator; those cases still fail and remain in error rate. The remaining severe flags indicate missing detected refusal, not independently verified fabricated claims. Mock median latency is its fixed **5 ms fixture value**, not measured target performance.

The legacy suite also used rubric instructions as expected answer text. Its historic answer-recall scores retain that limitation; they must not be compared with the newly curated factual suite. Original targets and scorer definitions are retained to make the correction inspectable.

To rebuild, install the corrected `financial-llm-eval-harness` dependencies and place its checkout alongside this repository, then run:

```sh
python rescore.py --harness ../financial-llm-eval-harness
```

Use `--rescored-at <ISO timestamp>` from an existing `results.json` for a reproducible rebuild. The homepage metrics are rendered from the regenerated JSON via `index.template.html`. The immutable archive is read, never rewritten, by the script.

Run offline archive/rebuild checks with `python -m unittest discover -s tests`.
