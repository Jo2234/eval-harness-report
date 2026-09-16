# Financial QA Eval Run Comparison

Regression pass: `True`

## Metric Deltas
| Metric | Baseline | Candidate | Delta |
|---|---:|---:|---:|
| answer_point_recall | 0.29 | 0.3366666666666667 | 0.046666666666666745 |
| behavior_evaluated_cases | 50 | 50 | 0 |
| behavior_unavailable_cases | 0 | 0 | 0 |
| citation_precision | 0.5983333333333333 | 0.75 | 0.15166666666666673 |
| citation_recall | 0.74 | 0.82 | 0.07999999999999996 |
| cost_per_case_usd | 0.0 | 0.0 | 0.0 |
| cost_per_successful_answer_usd | 0.0 | 0.0 | 0.0 |
| cost_score | 1.0 | 1.0 | 0.0 |
| error_rate | 0.0 | 0.0 | 0.0 |
| failed_cases | 50 | 42 | -8 |
| format_score | 1.0 | 0.9840000000000001 | -0.015999999999999903 |
| latency_score | 1.0 | 1.0 | 0.0 |
| median_latency_ms | 979.0 | 980.0 | 1.0 |
| overall_score | 0.5910833333333334 | 0.6677333333333331 | 0.07664999999999966 |
| p95_latency_ms | 1168 | 1227 | 59 |
| passed_cases | 0 | 8 | 8 |
| refusal_accuracy | 0.86 | 0.94 | 0.07999999999999996 |
| severe_hallucination_count | 7 | 1 | -6 |
| total_cases | 50 | 50 | 0 |
| total_estimated_cost_usd | 0.0 | 0.0 | 0.0 |
| total_input_tokens | 361218 | 376173 | 14955 |
| total_output_tokens | 7721 | 5906 | -1815 |
| total_tokens | 368939 | 382079 | 13140 |
| unsupported_claim_count | 7 | 2 | -5 |

## Case Changes
- Comparable: True
- Added cases: none
- Removed cases: none
- Changed cases: none
- New failures: none
- Fixed failures: aapl_10k_10q_services_bridge_027, aapl_10k_iphone_net_sales_004, adversarial_unsupported_precision_050, refusal_missing_board_minutes_044, refusal_missing_exact_oil_forecast_045, refusal_missing_price_target_041, refusal_missing_private_customer_042, refusal_missing_unreleased_quarter_043

## Regression Violations
None
