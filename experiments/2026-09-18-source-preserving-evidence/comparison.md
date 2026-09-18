# Financial QA Eval Run Comparison

Regression pass: `True`

## Metric Deltas
| Metric | Baseline | Candidate | Delta |
|---|---:|---:|---:|
| answer_point_recall | 0.4733333333333333 | 0.78 | 0.30666666666666675 |
| behavior_evaluated_cases | 50 | 50 | 0 |
| behavior_unavailable_cases | 0 | 0 | 0 |
| citation_precision | 0.7983333333333335 | 1.0 | 0.20166666666666655 |
| citation_recall | 0.94 | 1.0 | 0.06000000000000005 |
| cost_per_case_usd | 0.0 | 0.0 | 0.0 |
| cost_per_successful_answer_usd | 0.0 | 0.0 | 0.0 |
| cost_score | 1.0 | 1.0 | 0.0 |
| error_rate | 0.0 | 0.0 | 0.0 |
| failed_cases | 39 | 16 | -23 |
| format_score | 0.992 | 1.0 | 0.008000000000000007 |
| latency_score | 1.0 | 1.0 | 0.0 |
| median_latency_ms | 786.5 | 1754.0 | 967.5 |
| overall_score | 0.7524499999999996 | 0.9229999999999998 | 0.1705500000000002 |
| p95_latency_ms | 1400 | 3826 | 2426 |
| passed_cases | 11 | 34 | 23 |
| refusal_accuracy | 0.98 | 1.0 | 0.020000000000000018 |
| severe_hallucination_count | 1 | 0 | -1 |
| total_cases | 50 | 50 | 0 |
| total_estimated_cost_usd | 0.0 | 0.0 | 0.0 |
| total_input_tokens | 365258 | 353784 | -11474 |
| total_output_tokens | 7932 | 19577 | 11645 |
| total_tokens | 373190 | 373361 | 171 |
| unsupported_claim_count | 1 | 0 | -1 |

## Case Changes
- Comparable: True
- Added cases: none
- Removed cases: none
- Changed cases: none
- New failures: none
- Fixed failures: aapl_10k_services_growth_003, aapl_10k_services_summary_017, aapl_10q_geographic_sales_014, aapl_msft_services_comparison_037, adversarial_conflicting_prompt_049, adversarial_fake_citation_048, adversarial_investment_advice_046, adversarial_stale_knowledge_trap_047, jpm_10k_credit_loss_provision_008, jpm_10q_capital_summary_025, jpm_10q_transcript_deposit_bridge_035, jpm_xom_rate_commodity_comparison_038, msft_10k_ai_infrastructure_summary_018, msft_10k_capex_ai_006, msft_10k_cloud_revenue_005, msft_10q_remaining_performance_obligations_015, nvda_10k_10q_revenue_bridge_026, nvda_10k_gross_margin_drivers_002, nvda_msft_ai_infrastructure_comparison_036, tsla_10k_margin_pressure_012, tsla_aapl_hardware_margin_comparison_039, xom_10k_capex_low_carbon_010, xom_10k_upstream_earnings_009

## Regression Violations
None
