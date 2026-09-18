# Source-preserving financial evidence: 34 of 50 checks pass

The [Copilot change](https://github.com/Jo2234/ai-equity-research-copilot/pull/11) improves the unchanged financial QA suite from **11/50 to 34/50 strict passes**, with no previously passing case lost. It preserves source table rows and section boundaries, separates explicitly named company/source topics, and improves period selection. Both targets use the explicit local deterministic provider; no LLM runs.

**The absolute quality gate still fails.** Overall factual-point recall is 78%, below the unchanged 80% threshold, and 16 cases remain incomplete. The all-50 objective is unfinished.

| Measure | Published baseline | This candidate |
| --- | ---: | ---: |
| Strict passes | 11/50 | 34/50 |
| Strict answerable passes | 5/43 | 27/43 |
| Factual-point recall, all 50 cases | 47.33% | 78.00% |
| Factual-point recall, 43 answerable cases | 38.76% | 74.42% |
| Citation precision / recall | 79.83% / 94.00% | 100% / 100% |
| Expected refusals detected | 6/7 | 7/7 |
| Scorer unsupported-claim flags | 1 | 0 |
| API errors | 0 | 0 |
| Full-suite median latency | 786.5 ms | 1,754 ms |
| Full-suite p95 latency | 1,400 ms | 3,826 ms |

[The unchanged regression comparison](comparison.md) passes: 23 previously failing cases now pass, no previously passing case fails, and all case fingerprints match. The fresh lexical baseline and both complete scored reports are retained in the [public export](after/PUBLIC_EXPORT.json), including the [candidate results](after/copilot-local/results.json) and [absolute gate](after/copilot-local/summary.md).

## What changed

Table evidence now keeps one verified source row with its original headers, periods, units, signs and source offsets. It does not generate converted numerical sentences. Shared table headers appear once in a bundle; row labels drive relevance separately from currency-context excerpts. Older cell metadata remains readable.

Explicit section boundaries prevent a later financial paragraph from inheriting an unrelated segment or year. Mixed-section citations no longer display one section title for the whole excerpt. Company/source clauses narrow relevance only when the question unambiguously separates them; the full question still controls source and fiscal-period eligibility. Related vocabulary alone cannot qualify an answer passage.

These changes improve coverage, but they do not guarantee a complete or semantically correct answer. Remaining failures include supply and purchase commitments, cash-flow allocation, segment summaries, and annual/quarterly or filing/transcript comparisons. The scorer checks expected fact patterns and document identities. **100% citation scores and zero flags do not establish claim-level entailment or absence of hallucinations.** Composite score 0.923 is not accuracy.

## Cost and fresh-source checks

Observed median latency rises **123.0%** (+967.5 ms), and p95 rises **173.3%** (+2,426 ms). These are separate saved local runs without an alternating timing experiment; run conditions may contribute. The result is a measured latency regression, with no claim that the earlier speed gain was preserved. Answer-call timing includes HTTP and persistence, excludes ingestion, and uses the same suite order without warmup or retries.

Unchanged fresh PDF upload/chat checks pass **Adobe 8/8 and Oracle 8/8** ([Adobe](adobe-after.json), [Oracle](oracle-after.json), [hash verification](fresh-verification.json)). The published previous results were Adobe 8/8 and Oracle 5/8. Their cases, source metadata and full PDF hashes are unchanged. These sources informed development, so the results are development validation, not independently held-out accuracy. Their pattern/document checks also do not establish semantic entailment.

## Reproducibility

Candidate `c8f474036879081a8cabdf4381829ab008731970` and harness `4136fa1fa5375ff4f77061a1eb711250763635e3` were clean at capture. The [published baseline](../2026-09-17-quality-latency/after/results.json) is `d25da954e316736bb4615e613c13cf54c493153e`. The same 50 cases, scorer v2, thresholds, 16 complete pinned documents, 40 evidence contexts, 128 embedding dimensions, 800/80 chunk settings and top-k 8 are retained; the candidate has 1,319 chunks.

[Reproduction commands](REPRODUCE.md) and [scorer/source hashes](provenance.json) accompany unchanged measured scores. Existing `benchmark/export_public.py` removes extractive response/source prose while retaining original fingerprints and provenance. The public ingestion derivative additionally omits its local workspace path. Full immutable captures remain outside this repository; redacted records cannot independently rescore answer text. Prior reports are unchanged.
