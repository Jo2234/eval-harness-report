# More complete financial evidence

Figures and their explanations often occupy adjacent sentences. The [Copilot change](https://github.com/Jo2234/ai-equity-research-copilot/pull/7) retains bounded sentence pairs in the same paragraph, gives modest preference to numerical evidence and causal wording for explanatory queries, and removes contained passages from the same document. Separate documents retain separate citations. No model, dependency, arithmetic engine or source-specific rule was added.

| Measure | Before | After |
| --- | ---: | ---: |
| Strict passes, unchanged suite | 8/50 | 11/50 |
| Strict passes on answerable questions | 2/43 | 5/43 |
| Answerable factual-point recall | 26.74% | 37.21% |
| Citation precision | 81.33% | 80.67% |
| Citation recall | 91.00% | 91.00% |
| Composite score, not accuracy | 0.715533 | 0.745367 |
| Expected refusals detected | 6/7 | 6/7 |
| API errors | 0 | 0 |
| Frozen checks on two Adobe releases | 3/8 | 5/8 |

The unchanged regression gate passes; no previously passing case is lost. NVIDIA Data Center growth, JPMorgan net interest income, and Tesla automotive revenue now pass. No case loses factual-point recall. Citation precision falls on four already-failing cases: NVIDIA gross-margin drivers, JPMorgan credit provisions, Apple Services summary, and Microsoft AI infrastructure. Aggregate improvement does not mean every answer improved.

**The absolute quality gate still fails, with 39/50 cases failing.** Only five answerable questions pass strictly. The unchanged refusal detector still flags the explicit investment-advice refusal; its severe flag is not evidence that a buy recommendation was made. Scores measure the existing rules, not semantic truth. Sentence pairs may still overlap in part, and this change does not guarantee complete numerical comparisons or reconstruct arbitrary PDF tables.

## Fresh real-document checks

Eight [questions and checks](fresh-cases.json) were frozen before implementation against complete official Adobe FY2024 and Q1 FY2025 earnings releases, a company absent from the existing six-company corpus. The source PDFs were visually inspected and their hashes pinned in [the manifest](fresh-sources.json). Both full PDFs enter the production upload API. Only question, company UUID and top-k enter the chat request; expected facts and document IDs remain in the external checker.

Cash-flow/share-buyback coverage and the comparison of operating cash flows now pass. Three revenue checks still fail. Two explicit refusals pass in both versions. This is a small author-created set measuring numerical pattern presence, exact source-document coverage and refusal shape, not independently held-out accuracy or entailment. No cases were changed or implementation retuned after inspecting these results. [Before](fresh-before.json) and [after](fresh-after.json) retain failures and hashes with answer prose omitted.

## Validation and performance

All 61 backend/API tests pass, including three new regressions for adjacent explanations, obligation timing and contained evidence. Targeted fatal-error lint and the existing eval-metadata smoke also pass. The frozen 50-case suite, scorer, thresholds, 16 raw sources, 40 evidence contexts, parser settings and top-k 8 are unchanged. Both runs use the explicit local deterministic provider, no LLM, 1,311 chunks and fresh isolated state.

The [alternating timing check](timing-check.json) measured **934.484 ms before versus 979.988 ms after: 45.504 ms (4.87%) slower**. Both targets first completed the same 50 questions, followed by one excluded warmup round and five measured rounds of three questions. This is 15 measurements per target with alternating order and growing histories, not a concurrency benchmark or confidence interval. Full-suite median/p95 were 996/1,652 ms before and 1,005.5/1,753 ms after. No speedup is claimed.

## Provenance

- Baseline: `d4dfb2041adddd31e1e3071a286f9188b25415b1`.
- Candidate: `9d40cb7d995490eab481c09bef200086e6a0c827`.
- Harness: `4136fa1fa5375ff4f77061a1eb711250763635e3`; scorer `financial-eval-scorer/v2`.
- Frozen 50-case suite SHA-256: `1eaf08f68d6df324e95df38f6b6ac87850d2125c0602f61249ea467caaf9e0cb`.
- Fresh eight-case SHA-256: `c6420c62b681f9a7ec4593c8c060665620f2d02ede65739ff5f818c4d6eeca91`.

The visible development suite informed the implementation. Fresh baseline and candidate captures reproduce the earlier baseline quality scores. [Reproduction instructions](REPRODUCE.md), [before](before/results.json), [after](after/results.json) and [comparison](comparison.md) accompany this report. Compact public exports preserve scores, provenance and answer hashes; full answers and source excerpts remain local. Redacted exports cannot independently rescore text. Each compact directory has its own verified hash inventory. Historical reports are unchanged.
