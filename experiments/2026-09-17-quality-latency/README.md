# PDF evidence, answer selection and repeated-query latency

The [Copilot improvement](https://github.com/Jo2234/ai-equity-research-copilot/pull/8) preserves PDF paragraphs and nearby continuation lines, improves coverage of requested topics, respects explicit passage periods, and reuses prepared document corpora. **The measured API median is 23.95% faster, while strict passes remain 11/50.** Adobe checks improve; the broader quality gains are modest and citation precision slips.

| Measure | Before | After |
| --- | ---: | ---: |
| Strict passes | 11/50 | 11/50 |
| Strict answerable passes | 5/43 | 5/43 |
| Answerable factual-point recall | 37.21% | 38.76% |
| Citation precision | 80.67% | 79.83% |
| Citation recall | 91.00% | 94.00% |
| Composite score, not accuracy | 0.745367 | 0.752450 |
| Expected refusals detected | 6/7 | 6/7 |
| API errors | 0 | 0 |
| Adobe checks | 5/8 | 8/8 |
| Oracle checks | 5/8 | 5/8 |
| Alternating API median | 973.458 ms | 740.321 ms |

No previously passing case is lost, and the unchanged regression gate passes. **The absolute quality gate still fails: 39 cases fail, and citation precision now also falls just below its 80% threshold.** Five answerable questions pass strictly. The existing refusal detector still misses the explicit investment-advice refusal; the severe flag is not independent evidence of a buy recommendation.

Apple Services and JPMorgan credit disclosures gain factual coverage, while NVIDIA supply-risk and NVIDIA/Microsoft infrastructure comparisons lose some. Five cases lose citation precision and one gains it. Several questions omit a period while the reference requires a particular annual source; quoting another sourced period can therefore lower citation precision. This is a limitation of the measure, not a reason to claim all extra citations are correct. Extra figures, irrelevant context and incomplete comparisons remain possible. The changes do not perform arithmetic or guarantee semantic correctness.

## Changes and review

- Preserve PDF text-block boundaries through chunking, including pages with a single block. Some PDF producers create a block per physical line; nearby lowercase continuations of unfinished prose are rejoined conservatively, retaining source order and separating columns and completed sentences. Page boundaries are preserved. Existing uploads must be reingested to benefit from this parser change.
- Accept common financial prose such as “achieved” and “generated,” while keeping unlabelled numeric rows and colon-terminated headings out of prose answers.
- Match query phrases and cover multiple requested topics without letting overlapping passages crowd them out. Keep overlap when it supplies necessary causal explanation for a single-topic question. Remove source-type instructions from financial topic terms. Generic quarterly metrics continue to accept earnings releases.
- Reject positively identified mismatched section periods; explicit period wording in a passage overrides an inherited heading. Unknown periods stay unknown. Combined annual/quarterly releases still expose metadata-filter limitations.
- Cache up to eight company-scope corpora and lazy passage terms. Corpus changes and external file replacement invalidate the cache; chat-history writes preserve it. Locks protect shared caches. The write records its own inode through an open handle so a second writer cannot hide an immediate external document replacement. This does not make the JSON repository a general multiprocess database.

Three agents separately worked on answer selection, performance, and fresh-source validation/review. Independent review caught overly broad quarterly type filtering, a cache invalidation race, and acceptance of known wrong-period evidence; each received a regression test. The final version passes **88 backend/API tests**, targeted fatal-error lint, and GitHub backend/frontend/eval checks. No dependency or LLM was added.

## Real-document checks and development history

The unchanged eight Adobe cases improve from 5 to 8 passes ([before](adobe-before.json), [after](adobe-after.json)). They check numerical patterns and exact source-document coverage, not complete answer meaning or number-to-label binding.

A separate agent froze eight Oracle cases and full official PDF hashes before inspecting a candidate. The first candidate fell from 5/8 to 3/8 because physical lines appeared as individual PDF blocks. A continuation fix recovered one case; allowing an explicit annual period to override an inherited quarter heading recovered another. Final Oracle results return to 5/8 ([before](oracle/before.json), [after](oracle/after.json)). Three cases still fail because the combined Q4/FY2025 release has no single-quarter metadata and is excluded by quarter-scoped requests. Source metadata and cases were not changed to improve scores.

Oracle failures subsequently informed debugging, so these final results are **development validation, not independently held-out accuracy**. [Frozen cases](oracle/cases.json), [freeze record](oracle/freeze.json), [source manifest](oracle/sources/sources.json) and [development history](development-history.json) are retained. Both complete issuer PDFs enter the production upload API; only the question, company UUID and top-k enter chat requests. Reference facts and evaluator document IDs remain outside the product.

## Performance and provenance

The [alternating timing check](timing-check.json) measured **233.137 ms less latency (23.95%)** across 15 requests per target. Both APIs first processed the same 50 questions, then one excluded warmup round and five measured rounds of three questions with alternating order. Histories grow equally; the candidate cache is warm. This small local sample is not a concurrency benchmark or confidence interval. Full-suite median/p95 were 1,010.5/1,735 ms before and 786.5/1,400 ms after.

An exploratory [retrieval-only microbenchmark](retrieval-microbenchmark.json) measured 149.98 ms cold versus 1.11 ms warm for one Microsoft query over 1,311 chunks, with identical results and scores. It excludes chat persistence and API costs and was collected before the final robustness refinements. Use the final alternating API check for the end-to-end claim. Cold queries still prepare data, and the cache uses extra memory. Full JSON history writes remain an overhead.

- Baseline: `62c121cbb60d8a488bcaa9a8ad7a0ddcbc7f0820`.
- Final candidate: `d25da954e316736bb4615e613c13cf54c493153e`.
- Harness: `4136fa1fa5375ff4f77061a1eb711250763635e3`; scorer `financial-eval-scorer/v2`.
- Main suite SHA-256: `1eaf08f68d6df324e95df38f6b6ac87850d2125c0602f61249ea467caaf9e0cb`.
- Oracle case SHA-256: `98035d4846c178bf37ca100f776fd934ad9758e3b8f435f9a254c6e881d733b1`.

The same 16 complete, pinned raw sources and 40 evidence contexts were verified. The production parser intentionally changes chunk boundaries: 1,311 baseline chunks versus 1,319 candidate chunks. Embedding dimensions, chunk target/overlap, top-k 8, questions, scorer and thresholds remain unchanged. Both targets run the explicit local deterministic provider, with no LLM calls.

[Reproduction instructions](REPRODUCE.md), [full measured comparison](comparison.md), [before](before/results.json) and [after](after/results.json) are included. Compact public exports preserve unchanged scores, provenance and answer hashes while omitting extractive answer/source prose. Original captures remain local; redacted records cannot independently rescore text. Each compact results directory has a verified hash inventory. Historical reports remain unchanged.
