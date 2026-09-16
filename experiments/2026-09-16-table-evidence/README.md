# Table context and reporting-period evidence

This follow-up to [the grounding change](../2026-09-16-copilot-grounding/README.md) improves source selection and table readability without a model, new dependency, or changed evaluator. It fixes the explicit false refusal on the Tesla annual/quarterly margin question, but **strict passes remain 8/50 and the absolute quality gate still fails**.

| Measure | Merged grounding baseline | Table evidence candidate |
| --- | ---: | ---: |
| Strict passes | 8/50 | 8/50 |
| Answerable factual-point recall (43 cases) | 22.87% | 26.74% |
| Citation precision | 75.00% | 81.33% |
| Citation recall | 82.00% | 91.00% |
| Composite score, not accuracy | 0.667733 | 0.715533 |
| Expected refusals detected | 6/7 | 6/7 |
| API errors | 0 | 0 |
| Additional synthetic API checks | 6/8 | 8/8 |

The unchanged regression gate passes, with no previously passing case lost. The automotive margin comparison now cites both periods and covers two of its three expected points, rather than refusing. One already-failing Exxon capital-spending case loses a factual point (recall 1.0 to 0.5); aggregate gains do not mean every answer improved. Forty-two cases still fail, and only two strictly passing cases are answerable questions. The unchanged detector still misses the explicit investment-advice refusal; its severe flag is not evidence that a buy recommendation was actually given.

## Implementation and checks

Retrieval ranks matching terms in usable passages, rather than relying on topic words scattered across a chunk. Passage terms are prepared only for eligible chunks and reused within a request. Compact table rows retain source year headers and adjacent units; ellipses mark omitted rows. Missing column labels are not invented. Explanatory queries prefer prose to numeric tables. Comparisons identify each document's period and preserve separate citations when different documents repeat the same words. These are heuristics: no arithmetic, general PDF-table reconstruction, forecast synthesis, or semantic entailment guarantee is added.

The final implementation passes **58 backend/API tests**, targeted lint, the existing metadata smoke, and hosted backend/frontend/eval-smoke checks. Four added regression tests cover table headers/units/signs, headerless rows, duplicate wording across periods, and direct evidence versus scattered terms. [Eight additional synthetic cases](fresh-cases.json), frozen before the implementation, pass 8/8 versus 6/8 on the baseline. Their [runner](check-fresh.py) supplies only the question and synthetic source documents to the production API; expected output checks stay outside it. This is a small, author-created regression set, not independently held-out accuracy. It was rerun after development refinements, without changing the cases.

The first candidate removed the false refusal but repeated table sections; [development history](development-history.json) records that result. The final iteration quotes individual rows and prioritizes explanatory prose. The visible 50-case suite informed these changes. No live LLM was evaluated.

## Performance

The balanced [alternating timing check](timing-check.json) recorded **834.622 ms before versus 927.552 ms after: 92.930 ms (11.13%) slower**. Each target processed the same 50 benchmark questions and 18 earlier timing calls before this check; one warmup round was then excluded, followed by five repetitions of three questions (15 measured calls per target). Maximums were 851.890 and 975.058 ms. This is a small local sample with growing persistence history, not a concurrency benchmark or confidence interval. The quality gains have a measured latency cost; **no speedup is claimed**.

The first exploratory timing comparison had unequal history lengths and showed a larger gap; it is retained in [exploratory timing](timing-exploratory.json) rather than silently discarded. Full-suite runs recorded median/p95 845/976 ms before and 966.5/1584 ms after, but began with different history lengths. Use the balanced comparison for the more controlled latency observation. Passage computation is scoped to eligible chunks and reused for memo sections; the remaining overhead is not asserted to be eliminated.

## Provenance and reproduction

- Baseline source: `af7e62bdcaeae2c8becec0652c2395be6fce44ff`, the merge of the previous candidate `a4815435a6233ec646a729ca965d724888ef1a97`; production code is identical.
- Candidate: `5b5cb23b77d679cf29a91ab8fecd9044471c9a24`.
- Harness: `4136fa1fa5375ff4f77061a1eb711250763635e3`; scorer `financial-eval-scorer/v2`.
- Suite SHA-256: `1eaf08f68d6df324e95df38f6b6ac87850d2125c0602f61249ea467caaf9e0cb`.
- Same 16 pinned raw sources, 40 verified evidence contexts, 1,311 chunks, extraction, top-k 8 and local deterministic provider. No case, reference answer, source, runner, scorer or threshold was changed. The API never receives evaluation document IDs or answer keys.

[Reproduction commands](REPRODUCE.md), [before results](before/results.json), [after results](after/results.json) and [comparison](comparison.md) accompany the report. Scores are preserved by the unchanged public exporter; answers/source prose are redacted and original hashes retained. Public exports support comparison, not independent text rescoring. Original full captures remain local. Each compact export has a verified SHA-256 inventory. Historical reports remain unchanged.
