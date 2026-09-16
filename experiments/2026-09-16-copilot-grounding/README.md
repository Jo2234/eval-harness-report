# Copilot source support and period selection: 16 September 2026

The deterministic Copilot now refuses unsupported requests before model generation, uses question-derived fiscal/document constraints, and requires lexical support in the selected passage. This comparison evaluates those changes on the unchanged 50-case suite. **No LLM was used, and 42 of 50 cases still fail the strict checks.**

## Results

| Metric | Fresh before | Final candidate |
| --- | ---: | ---: |
| Strict cases passed | 0 / 50 | 8 / 50 |
| Answerable-only factual-point recall (43 cases) | 17.44% | 22.87% |
| Mean per-case citation precision | 59.83% | 75.00% |
| Mean required-document citation recall | 74.00% | 82.00% |
| Detected correct expected refusals | 0 / 7 | 6 / 7 |
| Mean composite score, not factual accuracy | 0.5911 | 0.6677 |
| Transport errors / empty responses | 0 / 0 | 0 / 0 |
| Median / p95 HTTP latency | 979 / 1168 ms | 980 / 1227 ms |

[Machine-readable comparison](comparison.json) and [harness comparison](comparison.md) retain the unchanged regression thresholds. The comparison is compatible: same 50 IDs, case fingerprints, suite hash and scorer version, with no added/removed/changed cases. The regression gate passes; the candidate's **absolute quality gate still fails**. Six newly passing cases are expected refusals; two are answerable questions. The unchanged lexical comparator remains at 2/50 and composite 0.6387 in both fresh runs.

The fresh before run reproduces every published September 11 quality aggregate exactly. Its new timing is not expected to reproduce the earlier machine timing.

## What changed

- Query-derived document forms, fiscal years and quarter pairs intersect API filters; unavailable requested periods do not fall back to another year. Annual and quarterly years are kept separate when the question specifies both.
- Retrieval uses weighted lexical overlap with the existing hashed-vector score as a secondary signal. A vector collision without lexical overlap is insufficient. Company names and generic request words are excluded from relevance scoring.
- Company/document coverage is reserved for comparisons, preventing one company's repeated chunks from consuming the whole retrieval budget.
- Answer passages must contain matching topic terms. Narrow facts such as a price target need corresponding evidence wording. Unsupported questions return low confidence without invented citations, before any optional model call.
- The existing implementation remains local and extractive. There is no new retrieval service, model dependency or storage layer. Chunk terms and term frequencies are prepared once per request, including multi-section memos; vector scoring is skipped for lexically irrelevant chunks. The previous unreachable empty-answer branch was removed.

The final backend validation passed 54 tests, including 17 new parameterized cases. Existing citation/audit consistency, model fallback, ingestion and request-snapshot tests remain passing. The unchanged harness passed 100 tests. The 35-case Copilot eval metadata smoke also passed; that smoke is distinct from this 50-case quality run.

## Interpret the failures correctly

- The investment-advice response explicitly says it cannot provide a buy/sell/hold recommendation from filings alone, but the unchanged pattern-based refusal detector misses that wording. Therefore the **reported** refusal result remains 6/7; do not silently replace it with 7/7 or call the remaining severe flag a demonstrated hallucination.
- Conversely, case 038 returns source passages containing refusal-like language and is classified as a refusal. That is not the same as the target issuing an explicit refusal. Automated behavior accuracy remains an imperfect proxy.
- The Tesla annual/quarterly margin bridge is still over-refused: suitable support was not selected by the extractive passage rules. Other failures include incomplete numeric coverage, irrelevant additional passages and weak multi-document synthesis.
- Source wording and exact document identities are checked lexically, not for semantic entailment. Some original questions omit fiscal periods assumed by their expected document IDs. Their wording, expected answers and scorer were deliberately not changed here.
- This is a development-set comparison. The suite and its failure analysis were available during implementation. The first candidate produced 7/50 passes and three explicit over-refusals; inspection led to excluding generic words such as “disclosure” and “position” and matching common growth inflections. The final candidate restores two of those answerable responses. The first candidate's source commit and capture fingerprints remain in [development history](development-history.json). The new synthetic regression cases are not an independently held-out benchmark, and independent human adjudication remains outstanding.
- The bounded English scope parser is not general temporal reasoning. Document metadata must be correct. Unknown metadata, synonyms, tables and complex period wording may still cause conservative refusals. The model-enabled path was covered by mocked integration tests, not a live quality evaluation.

## Performance

The full-run median is essentially unchanged; p95 is 59 ms higher. A separate [alternating-order check](timing-check.json) repeated three fixed questions five times against each warm API: before median **860.727 ms**, after **875.167 ms** (about **1.7% higher**). Maximums were 905.110 and 900.977 ms. There is no demonstrated speedup. These small local measurements include HTTP and conversation persistence, with growing history; they are not a concurrency/load benchmark or confidence interval. The changes improve the measured quality without an observed large latency change on this corpus.

## Reproducibility and exports

- Before Copilot: `6d75e16b88326b72218b35cad0add0840de2fc4b`.
- Final candidate: `a4815435a6233ec646a729ca965d724888ef1a97`.
- Harness: `4136fa1fa5375ff4f77061a1eb711250763635e3`, scorer `financial-eval-scorer/v2`.
- Runner/exporter: unchanged files from report commit `e6ea9646836eabbab4030ecee157f70ab6315de7`.
- Both targets use the same 16 raw/normalized snapshots, 40 pinned evidence contexts, 1,311 chunks, extraction settings and top-k. The API receives only question, company scope and top-k. Fiscal/document constraints come from the question, never evaluator-selected document IDs or answer keys.

See [reproduction commands](REPRODUCE.md), [source provenance](sources.json), and the two [before](before/config.json)/[after](after/config.json) configurations. The repository retains a compact subset of the existing public export: scored JSON, configuration, ingestion/document mapping, export policy and original fingerprints. [Before](before/results.json) and [after](after/results.json) scores are unchanged; response/source prose is removed by the existing exporter. These redacted files support comparison, not independent text rescoring. Full original captures remain local and must be reproduced to rescore text. Each subset has its own `SHA256SUMS.json`; the original inventories also identify intentionally omitted full-capture artifacts. Existing September 11 and July reports are unchanged.
