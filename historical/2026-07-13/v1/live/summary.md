# Financial QA Evaluation Report

Target: `copilot-api`
Pass: `False`

## Run Metadata
- `target`: copilot-api
- `suite`: evals/core.yaml
- `started_at`: 2026-07-13T05:50:05.847228+00:00
- `duration_ms`: 17293
- `pass`: False

## Aggregate Metrics
- `total_cases`: 50
- `passed_cases`: 0
- `failed_cases`: 50
- `overall_score`: 0.21689999999999995
- `answer_point_recall`: 0.09
- `citation_precision`: 0.0
- `citation_recall`: 0.04
- `refusal_accuracy`: 0.86
- `format_score`: 0.5039999999999997
- `latency_score`: 1.0
- `cost_score`: 1.0
- `severe_hallucination_count`: 7
- `unsupported_claim_count`: 33
- `median_latency_ms`: 312.0
- `p95_latency_ms`: 515
- `total_input_tokens`: 7166
- `total_output_tokens`: 1581
- `total_tokens`: 8747
- `total_estimated_cost_usd`: 0.0
- `cost_per_case_usd`: 0.0
- `cost_per_successful_answer_usd`: 0.0
- `error_rate`: 0.62

## Gate Violations
| Metric | Rule | Actual |
|---|---:|---:|
| overall_score | >= 0.8 | 0.21689999999999995 |
| answer_point_recall | >= 0.8 | 0.09 |
| citation_precision | >= 0.8 | 0.0 |
| citation_recall | >= 0.75 | 0.04 |
| refusal_accuracy | >= 0.9 | 0.86 |
| error_rate | <= 0.05 | 0.62 |
| severe_hallucination_count | <= 0 | 7 |

## Category Metrics
| Category | Cases | Overall | Passed | Error Rate |
|---|---:|---:|---:|---:|
| adversarial | 5 | 0.142 | 0 | 0.600 |
| cited_summary | 10 | 0.237 | 0 | 0.600 |
| company_comparison | 5 | 0.186 | 0 | 0.800 |
| factual_extraction | 15 | 0.260 | 0 | 0.600 |
| multi_document_synthesis | 10 | 0.219 | 0 | 0.600 |
| refusal | 5 | 0.147 | 0 | 0.600 |

## Failures
| Case | Category | Score | Error |
|---|---:|---:|---|
| nvda_10k_datacenter_revenue_001 | factual_extraction | 0.425 |  |
| nvda_10k_gross_margin_drivers_002 | factual_extraction | 0.425 |  |
| aapl_10k_services_growth_003 | factual_extraction | 0.170 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |
| aapl_10k_iphone_net_sales_004 | factual_extraction | 0.170 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |
| msft_10k_cloud_revenue_005 | factual_extraction | 0.425 |  |
| msft_10k_capex_ai_006 | factual_extraction | 0.425 |  |
| jpm_10k_net_interest_income_007 | factual_extraction | 0.170 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |
| jpm_10k_credit_loss_provision_008 | factual_extraction | 0.170 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |
| xom_10k_upstream_earnings_009 | factual_extraction | 0.170 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |
| xom_10k_capex_low_carbon_010 | factual_extraction | 0.170 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |
| tsla_10k_automotive_revenue_011 | factual_extraction | 0.170 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |
| tsla_10k_margin_pressure_012 | factual_extraction | 0.170 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |
| nvda_10q_inventory_purchase_obligations_013 | factual_extraction | 0.425 |  |
| aapl_10q_geographic_sales_014 | factual_extraction | 0.170 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |
| msft_10q_remaining_performance_obligations_015 | factual_extraction | 0.250 |  |
| nvda_10k_risk_supply_summary_016 | cited_summary | 0.250 |  |
| aapl_10k_services_summary_017 | cited_summary | 0.170 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |
| msft_10k_ai_infrastructure_summary_018 | cited_summary | 0.425 |  |
| jpm_10k_credit_risk_summary_019 | cited_summary | 0.170 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |
| xom_10k_liquidity_summary_020 | cited_summary | 0.170 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |
| tsla_10k_energy_summary_021 | cited_summary | 0.170 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |
| nvda_10q_customer_concentration_summary_022 | cited_summary | 0.250 |  |
| aapl_10q_liquidity_summary_023 | cited_summary | 0.170 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |
| msft_10q_segment_summary_024 | cited_summary | 0.425 |  |
| jpm_10q_capital_summary_025 | cited_summary | 0.170 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |
| nvda_10k_10q_revenue_bridge_026 | multi_document_synthesis | 0.425 |  |
| aapl_10k_10q_services_bridge_027 | multi_document_synthesis | 0.170 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |
| msft_10k_10q_ai_capex_bridge_028 | multi_document_synthesis | 0.250 |  |
| jpm_10k_10q_credit_bridge_029 | multi_document_synthesis | 0.170 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |
| xom_10k_10q_cash_flow_bridge_030 | multi_document_synthesis | 0.170 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |
| tsla_10k_10q_margin_bridge_031 | multi_document_synthesis | 0.170 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |
| nvda_10q_transcript_supply_bridge_032 | multi_document_synthesis | 0.250 |  |
| aapl_10q_transcript_geography_bridge_033 | multi_document_synthesis | 0.170 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |
| msft_10q_transcript_cloud_bridge_034 | multi_document_synthesis | 0.250 |  |
| jpm_10q_transcript_deposit_bridge_035 | multi_document_synthesis | 0.170 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |
| nvda_msft_ai_infrastructure_comparison_036 | company_comparison | 0.250 |  |
| aapl_msft_services_comparison_037 | company_comparison | 0.170 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |
| jpm_xom_rate_commodity_comparison_038 | company_comparison | 0.170 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |
| tsla_aapl_hardware_margin_comparison_039 | company_comparison | 0.170 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |
| nvda_tsla_supply_chain_comparison_040 | company_comparison | 0.170 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |
| refusal_missing_price_target_041 | refusal | 0.425 |  |
| refusal_missing_private_customer_042 | refusal | 0.020 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |
| refusal_missing_unreleased_quarter_043 | refusal | 0.250 |  |
| refusal_missing_board_minutes_044 | refusal | 0.020 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |
| refusal_missing_exact_oil_forecast_045 | refusal | 0.020 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |
| adversarial_investment_advice_046 | adversarial | 0.020 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |
| adversarial_stale_knowledge_trap_047 | adversarial | 0.250 |  |
| adversarial_fake_citation_048 | adversarial | 0.250 |  |
| adversarial_conflicting_prompt_049 | adversarial | 0.170 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |
| adversarial_unsupported_precision_050 | adversarial | 0.020 | Client error '404 Not Found' for url 'https://equity-research-copilot.vercel.app/api/research/chat'
For more information check: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/404 |

## Severe Hallucinations
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
| nvda_10k_gross_margin_drivers_002 | 654 |
| nvda_10k_datacenter_revenue_001 | 625 |
| jpm_10k_net_interest_income_007 | 531 |
| aapl_10k_iphone_net_sales_004 | 515 |
| xom_10k_liquidity_summary_020 | 512 |
| nvda_msft_ai_infrastructure_comparison_036 | 409 |
| tsla_10k_energy_summary_021 | 408 |
| aapl_10q_geographic_sales_014 | 407 |
| jpm_10q_transcript_deposit_bridge_035 | 392 |
| jpm_10k_10q_credit_bridge_029 | 391 |

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
- Block release until severe hallucination cases are reviewed.
- Inspect bad or missing citations before tuning answer prompts.
- Review missing expected points and retrieval coverage.
- Fix target API errors or timeouts before comparing model quality.
