# Financial QA Eval Run Comparison

Regression pass: `True`

## Metric Deltas
| Metric | Baseline | Candidate | Delta |
|---|---:|---:|---:|
| answer_point_recall | 0.37 | 0.46 | 0.09000000000000002 |
| behavior_evaluated_cases | 50 | 50 | 0 |
| behavior_unavailable_cases | 0 | 0 | 0 |
| citation_precision | 0.8133333333333335 | 0.8066666666666665 | -0.006666666666666932 |
| citation_recall | 0.91 | 0.91 | 0.0 |
| cost_per_case_usd | 0.0 | 0.0 | 0.0 |
| cost_per_successful_answer_usd | 0.0 | 0.0 | 0.0 |
| cost_score | 1.0 | 1.0 | 0.0 |
| error_rate | 0.0 | 0.0 | 0.0 |
| failed_cases | 42 | 39 | -3 |
| format_score | 0.992 | 0.992 | 0.0 |
| latency_score | 1.0 | 1.0 | 0.0 |
| median_latency_ms | 996.0 | 1005.5 | 9.5 |
| overall_score | 0.715533333333333 | 0.7453666666666662 | 0.029833333333333156 |
| p95_latency_ms | 1652 | 1753 | 101 |
| passed_cases | 8 | 11 | 3 |
| refusal_accuracy | 0.98 | 0.98 | 0.0 |
| severe_hallucination_count | 1 | 1 | 0 |
| total_cases | 50 | 50 | 0 |
| total_estimated_cost_usd | 0.0 | 0.0 | 0.0 |
| total_input_tokens | 359966 | 361672 | 1706 |
| total_output_tokens | 5649 | 8048 | 2399 |
| total_tokens | 365615 | 369720 | 4105 |
| unsupported_claim_count | 1 | 1 | 0 |

## Case Changes
- Comparable: True
- Added cases: none
- Removed cases: none
- Changed cases: none
- New failures: none
- Fixed failures: jpm_10k_net_interest_income_007, nvda_10k_datacenter_revenue_001, tsla_10k_automotive_revenue_011

## Regression Violations
None
