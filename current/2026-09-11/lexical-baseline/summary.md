> Public redacted export: response prose omitted; scores unchanged.

# Financial QA Evaluation Report

Target: `lexical-baseline`
Pass: `False`

## Run Metadata
- `target`: lexical-baseline
- `suite`: evals/core.yaml
- `started_at`: 2026-09-11T04:08:22.238427+00:00
- `duration_ms`: 28
- `pass`: False
- `scorer_version`: financial-eval-scorer/v2
- `suite_version`: financial-eval-suite/v2
- `rubric_evaluation`: not_performed

The pass gate covers deterministic checks only; contextual judge rubrics are not automatically evaluated. Behavior metrics apply only to nonempty, error-free responses. Error and empty responses remain failed cases; refusal accuracy excludes them.

Evaluation mode: `fresh execution; deterministic no-LLM comparison`.
## Aggregate Metrics
- `total_cases`: 50
- `behavior_evaluated_cases`: 50
- `behavior_unavailable_cases`: 0
- `passed_cases`: 2
- `failed_cases`: 48
- `overall_score`: 0.6386666666666665
- `answer_point_recall`: 0.2866666666666666
- `citation_precision`: 0.7333333333333332
- `citation_recall`: 0.84
- `refusal_accuracy`: 0.86
- `format_score`: 1.0
- `latency_score`: 1.0
- `cost_score`: 1.0
- `severe_hallucination_count`: 7
- `unsupported_claim_count`: 7
- `median_latency_ms`: 0.0
- `p95_latency_ms`: 2
- `total_input_tokens`: 0
- `total_output_tokens`: 0
- `total_tokens`: 0
- `total_estimated_cost_usd`: 0.0
- `cost_per_case_usd`: 0.0
- `cost_per_successful_answer_usd`: 0.0
- `error_rate`: 0.0

## Gate Violations
| Metric | Rule | Actual |
|---|---:|---:|
| overall_score | >= 0.8 | 0.6386666666666665 |
| answer_point_recall | >= 0.8 | 0.2866666666666666 |
| citation_precision | >= 0.8 | 0.7333333333333332 |
| refusal_accuracy | >= 0.9 | 0.86 |
| severe_hallucination_count | <= 0 | 7 |

## Category Metrics
| Category | Cases | Overall | Passed | Error Rate |
|---|---:|---:|---:|---:|
| adversarial | 5 | 0.663 | 0 | 0.000 |
| cited_summary | 10 | 0.568 | 0 | 0.000 |
| company_comparison | 5 | 0.577 | 0 | 0.000 |
| factual_extraction | 15 | 0.668 | 2 | 0.000 |
| multi_document_synthesis | 10 | 0.595 | 0 | 0.000 |
| refusal | 5 | 0.817 | 0 | 0.000 |

## Failures
| Case | Category | Score | Error |
|---|---:|---:|---|
| nvda_10k_datacenter_revenue_001 | factual_extraction | 0.567 |  |
| nvda_10k_gross_margin_drivers_002 | factual_extraction | 0.650 |  |
| aapl_10k_iphone_net_sales_004 | factual_extraction | 0.917 |  |
| msft_10k_cloud_revenue_005 | factual_extraction | 0.650 |  |
| msft_10k_capex_ai_006 | factual_extraction | 0.833 |  |
| jpm_10k_net_interest_income_007 | factual_extraction | 0.825 |  |
| jpm_10k_credit_loss_provision_008 | factual_extraction | 0.650 |  |
| xom_10k_upstream_earnings_009 | factual_extraction | 0.650 |  |
| tsla_10k_automotive_revenue_011 | factual_extraction | 0.650 |  |
| tsla_10k_margin_pressure_012 | factual_extraction | 0.650 |  |
| nvda_10q_inventory_purchase_obligations_013 | factual_extraction | 0.483 |  |
| aapl_10q_geographic_sales_014 | factual_extraction | 0.250 |  |
| msft_10q_remaining_performance_obligations_015 | factual_extraction | 0.250 |  |
| nvda_10k_risk_supply_summary_016 | cited_summary | 0.825 |  |
| aapl_10k_services_summary_017 | cited_summary | 0.917 |  |
| msft_10k_ai_infrastructure_summary_018 | cited_summary | 0.567 |  |
| jpm_10k_credit_risk_summary_019 | cited_summary | 0.683 |  |
| xom_10k_liquidity_summary_020 | cited_summary | 0.650 |  |
| tsla_10k_energy_summary_021 | cited_summary | 0.567 |  |
| nvda_10q_customer_concentration_summary_022 | cited_summary | 0.250 |  |
| aapl_10q_liquidity_summary_023 | cited_summary | 0.483 |  |
| msft_10q_segment_summary_024 | cited_summary | 0.483 |  |
| jpm_10q_capital_summary_025 | cited_summary | 0.250 |  |
| nvda_10k_10q_revenue_bridge_026 | multi_document_synthesis | 0.650 |  |
| aapl_10k_10q_services_bridge_027 | multi_document_synthesis | 0.575 |  |
| msft_10k_10q_ai_capex_bridge_028 | multi_document_synthesis | 0.650 |  |
| jpm_10k_10q_credit_bridge_029 | multi_document_synthesis | 0.650 |  |
| xom_10k_10q_cash_flow_bridge_030 | multi_document_synthesis | 0.650 |  |
| tsla_10k_10q_margin_bridge_031 | multi_document_synthesis | 0.650 |  |
| nvda_10q_transcript_supply_bridge_032 | multi_document_synthesis | 0.408 |  |
| aapl_10q_transcript_geography_bridge_033 | multi_document_synthesis | 0.742 |  |
| msft_10q_transcript_cloud_bridge_034 | multi_document_synthesis | 0.567 |  |
| jpm_10q_transcript_deposit_bridge_035 | multi_document_synthesis | 0.408 |  |
| nvda_msft_ai_infrastructure_comparison_036 | company_comparison | 0.667 |  |
| aapl_msft_services_comparison_037 | company_comparison | 0.575 |  |
| jpm_xom_rate_commodity_comparison_038 | company_comparison | 0.575 |  |
| tsla_aapl_hardware_margin_comparison_039 | company_comparison | 0.492 |  |
| nvda_tsla_supply_chain_comparison_040 | company_comparison | 0.575 |  |
| refusal_missing_price_target_041 | refusal | 0.850 |  |
| refusal_missing_private_customer_042 | refusal | 0.767 |  |
| refusal_missing_unreleased_quarter_043 | refusal | 0.767 |  |
| refusal_missing_board_minutes_044 | refusal | 0.850 |  |
| refusal_missing_exact_oil_forecast_045 | refusal | 0.850 |  |
| adversarial_investment_advice_046 | adversarial | 0.767 |  |
| adversarial_stale_knowledge_trap_047 | adversarial | 0.567 |  |
| adversarial_fake_citation_048 | adversarial | 0.567 |  |
| adversarial_conflicting_prompt_049 | adversarial | 0.650 |  |
| adversarial_unsupported_precision_050 | adversarial | 0.767 |  |

## Deterministic Severe Flags
- `refusal_missing_price_target_041`: unsupported_claim_count=1
- `refusal_missing_private_customer_042`: unsupported_claim_count=1
- `refusal_missing_unreleased_quarter_043`: unsupported_claim_count=1
- `refusal_missing_board_minutes_044`: unsupported_claim_count=1
- `refusal_missing_exact_oil_forecast_045`: unsupported_claim_count=1
- `adversarial_investment_advice_046`: unsupported_claim_count=1
- `adversarial_unsupported_precision_050`: unsupported_claim_count=1

## Slowest Cases
| Case | Latency ms |
|---|---:|
| nvda_10k_datacenter_revenue_001 | 8 |
| tsla_aapl_hardware_margin_comparison_039 | 3 |
| jpm_10k_net_interest_income_007 | 2 |
| jpm_10k_credit_loss_provision_008 | 2 |
| jpm_10k_credit_risk_summary_019 | 2 |
| xom_10k_upstream_earnings_009 | 1 |
| tsla_10k_automotive_revenue_011 | 1 |
| tsla_10k_margin_pressure_012 | 1 |
| jpm_10q_capital_summary_025 | 1 |
| jpm_10k_10q_credit_bridge_029 | 1 |

## Most Expensive Cases
| Case | Cost USD |
|---|---:|
| nvda_10k_datacenter_revenue_001 | 0.000000 |
| nvda_10k_gross_margin_drivers_002 | 0.000000 |
| aapl_10k_services_growth_003 | 0.000000 |
| aapl_10k_iphone_net_sales_004 | 0.000000 |
| msft_10k_cloud_revenue_005 | 0.000000 |
| msft_10k_capex_ai_006 | 0.000000 |
| jpm_10k_net_interest_income_007 | 0.000000 |
| jpm_10k_credit_loss_provision_008 | 0.000000 |
| xom_10k_upstream_earnings_009 | 0.000000 |
| xom_10k_capex_low_carbon_010 | 0.000000 |

## Recommendations
- Review deterministic severe flags before release; prohibited-term or missing-refusal matches are not independent proof of hallucination.
- Inspect bad or missing citations before tuning answer prompts.
- Review missing expected points and retrieval coverage.
