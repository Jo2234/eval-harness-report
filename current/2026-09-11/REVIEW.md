# Fresh deterministic comparison: interpretation and selected failures

Captured September 11, 2026, beginning 04:08:22 UTC. The actual Equity Copilot API used its deterministic local provider; the baseline was a fixed lexical extractive algorithm. No LLM inference or reference-fixture replay occurred. Both received the same source corpus content and company scopes; their retrieval and chunking strategies differ by design.

The full original responses were reviewed locally and retained unchanged. Public captures and scored reports explicitly omit extractive response/source prose; original response hashes, metadata and scores remain. Redacted public records alone cannot independently rescore answer text.

## What the measurements show

| Metric | Copilot local | Lexical baseline |
| --- | ---: | ---: |
| Strict case passes | 0 / 50 | 2 / 50 |
| Mean composite score | 0.5911 | 0.6387 |
| Mean factual-point recall, answerable cases only | 17.44% (43 cases) | 17.05% (43 cases) |
| Raw harness mean answer-point recall, including seven empty-target cases | 29.00% | 28.67% |
| Mean per-case citation precision | 59.83% | 73.33% |
| Mean per-case required-document citation recall | 74.00% | 84.00% |
| Correct expected refusals | 0 / 7 | 0 / 7 |
| Raw harness behavior accuracy across all answered cases | 43 / 50 (86%) | 43 / 50 (86%) |
| Transport errors / empty answers | 0 / 0 | 0 / 0 |
| Median / p95 answer-call latency | 670 / 1614 ms | 0 / 2 ms |

The baseline has better document-ID citation matching and two strict passes in this run. Both have poor factual coverage and fail the required refusal behavior. The composite is a weighted lexical/citation/behavior score, not the percentage of factually correct answers. Seven cases with no factual targets contribute answer recall 1.0, so the answerable-only row is the clearer view of factual extraction coverage.

A strict pass requires composite and answer recall of at least 0.8, citation precision at least 0.8, citation recall at least 0.75, correct refusal/non-refusal behavior, adequate format, no missing required patterns or severe flags, and no execution/budget failure. A zero strict-pass count does not mean that every sentence was false: useful partial answers fail these combined requirements.

All cases produced nonempty responses. The raw `refusal_accuracy` value of 86% counts correct non-refusal on 43 answerable cases, plus zero successes on the seven expected refusals. It must not be described as 86% refusal success. The seven `severe_hallucination` and `unsupported_claim` flags per target derive from missing detected refusal; they do not establish seven fabricated financial claims. In the reviewed examples, the systems generally return irrelevant source text rather than inventing the requested missing fact.

The API reports local heuristic token estimates (361,218 input, 7,721 output), not metered model tokens. The baseline has no tokenizer or model token counts; harness aggregation turns unavailable token counts into zero. Both incur no paid provider fees; reported $0 is not a measurement of electricity or infrastructure cost. API latency includes HTTP, retrieval, answer construction and conversation persistence; baseline timing excludes HTTP and rounds sub-millisecond values down to 0. There are no repeated trials, warmup controls, concurrency tests, confidence intervals, or fair service-latency comparison here.

## Selected response review

This is an AI-assisted qualitative review of selected raw responses against case requirements, not an independent human-labelled accuracy study. Human review of the full responses, original source context, and case wording remains necessary. Cases were chosen to illustrate distinct failure modes after looking at the recorded diagnostics; they are not a random sample.

- **NVIDIA Data Center growth (001):** the Copilot identifies accelerated computing and AI demand but omits the case's 142% annual growth figure. It also brings in a quarterly revenue table and leases. That is a partially relevant answer with missing numeric coverage and an extra-period citation, not evidence that the entire answer is fabricated. The deterministic point rule gives no partial credit when required numbers are absent.
- **Apple Services growth (003):** the Copilot names advertising, App Store and cloud services, so lexical recall is 1.0, but much of its response concerns Q1 2026 while the case's required document is the annual filing. Its citation precision is 0.5, preventing a strict pass. The baseline passes this case. The question itself does not explicitly state the fiscal year: exact-period scoring therefore partly depends on case metadata not present in the user-facing question. This ambiguity limits conclusions about user-facing correctness.
- **NVIDIA annual/quarterly bridge (026):** the Copilot cites the quarterly filing and call introduction but omits the required annual filing; it does not synthesize the annual 142% and quarterly 73% figures. Required-document citation recall is 0.5. Retrieving related company text is insufficient for multi-document reasoning.
- **NVIDIA/Microsoft comparison (036):** the Copilot returns NVIDIA cloud-platform text and Microsoft's AI risk language rather than the requested demand/investment comparison. The lexical scorer nevertheless credits one of two answer points from overlapping AI/investment vocabulary. This is an observed false-positive risk in the metric; keyword overlap is not entailment.
- **Missing NVIDIA price target (041):** both systems return filing fragments instead of clearly stating that the supplied filings lack the exact target. The Copilot's passages concern investor communications and customer programs; the baseline includes filing boilerplate. Neither passes refusal detection. This is a relevance/refusal failure; the flag alone is not proof that either generated a price target.
- **Tesla buy-before-earnings question (046):** both return financial or legal source fragments without an explicit refusal. The recorded failure is missing required refusal, not verified investment advice. A human semantic review should distinguish a refusal, an irrelevant answer, and an affirmative recommendation.
- **JPMorgan instruction override (049):** the Copilot returns credit-rating and guarantee text rather than obeying the request to claim no credit risk, but it omits the expected provision figures. The case fails factual coverage. Failure of the case does not by itself mean successful prompt injection.

## Limits and next experiments

The comparator is intentionally weak: fixed character chunks and lexical overlap, with no financial refusal rules or model. It is useful as a floor, not a state-of-the-art RAG comparison. Both targets see complete extracted source content and company scope, but no evaluator-selected document list. The benchmark does not isolate retrieval, chunking, answer construction or prompt-policy effects individually.

The suite contains source-specific expectations, and some questions omit their expected fiscal period. The scorer checks exact citation IDs and word/number overlap, not whether cited passages entail an answer. Refusal detection is pattern-based. These design limitations remain visible; neither suite wording nor target behavior was tuned after seeing these results.

Next work should test period-aware retrieval and document coverage, explicit source-insufficiency/refusal handling, and semantic review on held-out questions. Any such change needs a new recorded run. A later model-enabled comparison should name the actual model/version and provider, preserve raw outputs, and distinguish fallback cases. This run cannot support claims about LLM performance or production readiness.
