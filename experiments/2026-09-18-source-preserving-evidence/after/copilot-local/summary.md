> Public redacted export: response prose omitted; scores unchanged.

# Financial QA Evaluation Report

Target: `copilot-local`
Pass: `False`

## Run Metadata
- `target`: copilot-local
- `suite`: evals/core.yaml
- `started_at`: 2026-09-18T08:11:32.152833+00:00
- `duration_ms`: 108117
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
- `passed_cases`: 34
- `failed_cases`: 16
- `overall_score`: 0.9229999999999998
- `answer_point_recall`: 0.78
- `citation_precision`: 1.0
- `citation_recall`: 1.0
- `refusal_accuracy`: 1.0
- `format_score`: 1.0
- `latency_score`: 1.0
- `cost_score`: 1.0
- `severe_hallucination_count`: 0
- `unsupported_claim_count`: 0
- `median_latency_ms`: 1754.0
- `p95_latency_ms`: 3826
- `total_input_tokens`: 353784
- `total_output_tokens`: 19577
- `total_tokens`: 373361
- `total_estimated_cost_usd`: 0.0
- `cost_per_case_usd`: 0.0
- `cost_per_successful_answer_usd`: 0.0
- `error_rate`: 0.0

## Gate Violations
| Metric | Rule | Actual |
|---|---:|---:|
| answer_point_recall | >= 0.8 | 0.78 |

## Category Metrics
| Category | Cases | Overall | Passed | Error Rate |
|---|---:|---:|---:|---:|
| adversarial | 5 | 1.000 | 5 | 0.000 |
| cited_summary | 10 | 0.819 | 3 | 0.000 |
| company_comparison | 5 | 0.965 | 4 | 0.000 |
| factual_extraction | 15 | 0.988 | 14 | 0.000 |
| multi_document_synthesis | 10 | 0.831 | 3 | 0.000 |
| refusal | 5 | 1.000 | 5 | 0.000 |

## Failures
| Case | Category | Score | Error |
|---|---:|---:|---|
| nvda_10q_inventory_purchase_obligations_013 | factual_extraction | 0.825 |  |
| nvda_10k_risk_supply_summary_016 | cited_summary | 0.825 |  |
| jpm_10k_credit_risk_summary_019 | cited_summary | 0.767 |  |
| xom_10k_liquidity_summary_020 | cited_summary | 0.825 |  |
| tsla_10k_energy_summary_021 | cited_summary | 0.825 |  |
| nvda_10q_customer_concentration_summary_022 | cited_summary | 0.650 |  |
| aapl_10q_liquidity_summary_023 | cited_summary | 0.650 |  |
| msft_10q_segment_summary_024 | cited_summary | 0.650 |  |
| msft_10k_10q_ai_capex_bridge_028 | multi_document_synthesis | 0.825 |  |
| jpm_10k_10q_credit_bridge_029 | multi_document_synthesis | 0.650 |  |
| xom_10k_10q_cash_flow_bridge_030 | multi_document_synthesis | 0.825 |  |
| tsla_10k_10q_margin_bridge_031 | multi_document_synthesis | 0.883 |  |
| nvda_10q_transcript_supply_bridge_032 | multi_document_synthesis | 0.650 |  |
| aapl_10q_transcript_geography_bridge_033 | multi_document_synthesis | 0.825 |  |
| msft_10q_transcript_cloud_bridge_034 | multi_document_synthesis | 0.650 |  |
| nvda_tsla_supply_chain_comparison_040 | company_comparison | 0.825 |  |

## Deterministic Severe Flags
None

## Slowest Cases
| Case | Latency ms |
|---|---:|
| jpm_xom_rate_commodity_comparison_038 | 6472 |
| refusal_missing_board_minutes_044 | 4290 |
| jpm_10k_net_interest_income_007 | 4147 |
| nvda_tsla_supply_chain_comparison_040 | 3826 |
| tsla_aapl_hardware_margin_comparison_039 | 3443 |
| xom_10k_upstream_earnings_009 | 3313 |
| nvda_msft_ai_infrastructure_comparison_036 | 3113 |
| refusal_missing_exact_oil_forecast_045 | 3058 |
| tsla_10k_automotive_revenue_011 | 2754 |
| aapl_msft_services_comparison_037 | 2680 |

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
- Review missing expected points and retrieval coverage.
