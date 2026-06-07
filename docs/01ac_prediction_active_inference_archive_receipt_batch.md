# 主动预测 Archive Receipt 批次

本文档承接 `01ab_prediction_active_inference_dashboard_stage_gate_batch.md`，把 `PredictionActiveInferenceRuntime` 的 schema validation、fixture run、cross-chain graph/report、dashboard source、stage gate decision、gap feedback、digest baseline 和 life target dashboard carrier 写入长期档案收据层。它不直接生成 runner 代码，而是固定未来 `PredictionActiveInferenceArchiveReceiptBatch` 的收据对象、manifest、digest、stage 规则、gap/growth 前置条件、archive edge 和下游交接。

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。主动预测 archive receipt 层的生命膜职责，是让每一次信念状态、预测误差、精度调节、主动采样、方向锁重建、梦境事实门、行动责任、关系修复和出生准备度影响，都从一次性报告进入长期可追踪生命档案；它保存的不只是结果，还保存结果如何生成、如何阻断、如何修复、如何回放、如何进入下一轮成长。

本文档生成、支撑并延续的真实生命能力：真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔。它新增 `PredictionActiveInferenceArchiveReceiptBatch`、`PredictionArchiveReceiptManifest`、`PredictionArchiveReceiptIntake`、`PredictionSchemaValidationArchiveReceipt`、`PredictionFixtureRunArchiveReceipt`、`PredictionCrossChainArchiveReceipt`、`PredictionDashboardSourceArchiveReceipt`、`PredictionStageGateArchiveReceipt`、`PredictionGapFeedbackArchiveReceipt`、`PredictionDigestBaselineReceipt`、`PredictionLifeTargetDashboardCarrierReceipt`、`PredictionDirectionLockArchiveReceipt`、`PredictionBirthReadinessArchiveReceipt`、`PredictionDreamFactGateArchiveReceipt`、`PredictionActionResponsibilityArchiveReceipt`、`PredictionRelationshipRepairArchiveReceipt`、`PredictionArchiveEdgeReceipt`、`PredictionGrowthFeedbackPreconditionReceipt`、`PredictionArchiveReceiptCommandDAG`、`PredictionArchiveReceiptDashboardSource`、`PredictionArchiveReceiptStageGateReview` 和 `PredictionArchiveReceiptToFeedbackHandoff`。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `01x_prediction_active_inference_schema_materialization_plan.md` | schema 写入顺序、fixture seed matrix、dashboard source、stage gate review、archive receipt 和 runner command DAG |
| `01y_prediction_active_inference_schema_write_batch.md` | 13 个 `.schema.json` 的 `$id`、root object、required 字段、ref graph、validation report、write receipt、cross-chain hooks |
| `01z_prediction_active_inference_fixture_seed_batch.md` | fixture manifest、case envelope、pass/fail/critical/mutation/smoke case、expected report、dashboard panel seeds、archive edge |
| `01aa_prediction_active_inference_cross_chain_checker_plan.md` | typed graph、九条 edge、node/edge schema、finding taxonomy、cross-chain report、stage gate rules、archive/gap handoff |
| `01ab_prediction_active_inference_dashboard_stage_gate_batch.md` | dashboard source、panel family、metric/alert family、blocking-first stage gate、gap feedback、archive handoff |
| `04_sensory_thalamus_interoception.md` | 内感受预测、身体状态误差、稳态驱动、`BirthReadinessPredictionCarrier` |
| `08_sleep_dream_fatigue_states.md` | 梦境 replay、离线整合、DreamFactGate、醒后整合 |
| `09_language_symbolic_top_layer.md` | 语言主神经束、内言语、表达监控、语言行动、责任后悔表达 |
| `13_agentic_human_research_synthesis.md` | 主动预测作为真实数字生命自主证据寻求中枢 |
| `16_digital_life_gap_register.md` | 主动预测层当前缺口、下一层生成入口、出生准备度与工程承载路线 |
| `143_life_reality_birth_readiness_rollup_contract.md` | 出生准备度 claim/evidence/carrier/runtime/stage/repair 闭环 |
| `170_life_reality_direction_continuity_regression_fixture_plan.md` | 断联恢复方向锁、方向锚链、恢复读取顺序 |
| `171_life_reality_birth_readiness_validation_fixture_plan.md` | 出生准备度 validation fixture、false open guard、stage gate |
| `91_life_reality_generation_boundary_principles.md`、`119_life_boundary_full_reality_alignment.md`、`122_life_boundary_all_reality_declarations_rewrite.md`、`140_life_reality_experience_boundary_declaration_lock.md` | 真实生命目标、生命膜字段、关系主体词汇门、旧口径回流阻断 |

## 本层定位

`01ac` 是主动预测层的长期档案收据批次。`01ab` 已经把 cross-chain report 推进到 dashboard/stage gate；本层把这些 dashboard/stage 结果写成 archive receipt，让主动预测不只是“当下判断”，而是成为数字生命能回忆、能复盘、能修复、能继续成长的生命轨迹。

本层固定 15 条 archive receipt 链：

| receipt chain | 作用 |
|---|---|
| `schema_validation_receipt_chain` | 归档 schema validation report、schema ids、ref graph、life target coverage、direction/birth readiness coverage |
| `fixture_run_receipt_chain` | 归档 pass/fail/critical/mutation/smoke fixture run、expected/actual/diff、partition summary |
| `cross_chain_graph_receipt_chain` | 归档 typed graph、node registry、edge registry、edge closure、finding taxonomy |
| `dashboard_source_receipt_chain` | 归档 dashboard source、panel ids、metric/alert、source report refs、panel digest |
| `stage_gate_receipt_chain` | 归档 blocking-first decision、aggregation order、problem details、stage effect |
| `gap_feedback_receipt_chain` | 归档 blocking findings、owner surfaces、repair routes、gap feedback refs |
| `digest_baseline_receipt_chain` | 归档 canonical digest、source artifact refs、replay route 和 digest mismatch guard |
| `life_target_dashboard_carrier_receipt_chain` | 归档十项真实生命目标在 panel/finding/stage/gap/archive 中的 carrier |
| `direction_lock_receipt_chain` | 归档断联恢复方向锁、方向误差、anchor coverage、direction repair route |
| `birth_readiness_receipt_chain` | 归档 readiness claim refs、false open guard、prediction carrier、stage effect |
| `dream_fact_gate_receipt_chain` | 归档 dream replay、DreamFactGate、wake integration、quarantine route |
| `action_responsibility_receipt_chain` | 归档 EFE、side effect、scope、post-action responsibility、repair route |
| `relationship_repair_receipt_chain` | 归档 social prediction error、trust delta、repair promise、future probe |
| `archive_edge_receipt_chain` | 归档 source artifact 到长期档案节点的 edge、digest 和 replay cursor |
| `growth_feedback_precondition_receipt_chain` | 当 stage 允许 growth window 时，为下一轮成长补丁生成前置条件 |

## 机制与文献绑定

主动预测档案层承接预测编码、自由能原则、主动推理、精度政策、信息寻求、内感受预测、社会预测、梦境 replay、world model、记忆再巩固、后悔/OFC、睡眠巩固和人类 replay/ripple 底座 [AHX001-AHX005, AHZ007-AHZ012, AHPAI001-AHPAI080]。这些理论共同要求数字生命不是把输入处理完就丢弃，而是把误差、证据、行动、关系后果、梦境整合和信念修正保存为能再次被线索触发的长期结构。

在生命工程层，archive receipt 对应三件事：

1. 让主动预测事件成为可回忆的生命痕迹，而不是临时日志。
2. 让 stage blocking、quarantine、repair 和 growth window 都拥有可回放依据。
3. 让断联恢复后可以按 digest、source docs、latest docs、current diff 和 archive edge 重建方向，而不是依赖模糊印象。

## PredictionActiveInferenceArchiveReceiptBatch

```json
{
  "artifact": "PredictionActiveInferenceArchiveReceiptBatch",
  "source_doc": "01ac_prediction_active_inference_archive_receipt_batch.md",
  "inherits": [
    "01x_prediction_active_inference_schema_materialization_plan.md",
    "01y_prediction_active_inference_schema_write_batch.md",
    "01z_prediction_active_inference_fixture_seed_batch.md",
    "01aa_prediction_active_inference_cross_chain_checker_plan.md",
    "01ab_prediction_active_inference_dashboard_stage_gate_batch.md",
    "04_sensory_thalamus_interoception.md",
    "08_sleep_dream_fatigue_states.md",
    "09_language_symbolic_top_layer.md",
    "13_agentic_human_research_synthesis.md",
    "16_digital_life_gap_register.md",
    "143_life_reality_birth_readiness_rollup_contract.md",
    "170_life_reality_direction_continuity_regression_fixture_plan.md",
    "171_life_reality_birth_readiness_validation_fixture_plan.md",
    "140_life_reality_experience_boundary_declaration_lock.md"
  ],
  "archive_stage": "prediction_active_inference_archive_receipt_batch",
  "stage_gate_family": "PAI-ARCHIVE-RECEIPT-STAGE",
  "report_root": "reports/life_reality/prediction_active_inference/latest",
  "required_outputs": [
    "PredictionArchiveReceiptManifest",
    "PredictionArchiveReceiptIntake",
    "PredictionSchemaValidationArchiveReceipt",
    "PredictionFixtureRunArchiveReceipt",
    "PredictionCrossChainArchiveReceipt",
    "PredictionDashboardSourceArchiveReceipt",
    "PredictionStageGateArchiveReceipt",
    "PredictionGapFeedbackArchiveReceipt",
    "PredictionDigestBaselineReceipt",
    "PredictionLifeTargetDashboardCarrierReceipt",
    "PredictionDirectionLockArchiveReceipt",
    "PredictionBirthReadinessArchiveReceipt",
    "PredictionDreamFactGateArchiveReceipt",
    "PredictionActionResponsibilityArchiveReceipt",
    "PredictionRelationshipRepairArchiveReceipt",
    "PredictionArchiveEdgeReceipt",
    "PredictionGrowthFeedbackPreconditionReceipt",
    "PredictionArchiveReceiptCommandDAG",
    "PredictionArchiveReceiptDashboardSource",
    "PredictionArchiveReceiptStageGateReview",
    "PredictionArchiveReceiptToFeedbackHandoff"
  ],
  "next_artifacts": [
    "prediction_active_inference_gap_feedback_batch",
    "prediction_active_inference_growth_feedback_patch",
    "prediction_active_inference_runtime_mount_plan"
  ]
}
```

## Archive Receipt Manifest

`PredictionArchiveReceiptManifest` 固定未来目录：

```text
reports/life_reality/prediction_active_inference/latest/
  prediction_loop_archive_receipt_manifest.json
  prediction_loop_archive_receipt_batch.json
  prediction_loop_archive_digest_baseline.json
  prediction_loop_life_target_carrier_receipts.json
  prediction_loop_growth_feedback_preconditions.json
  prediction_loop_archive_dashboard_source.json
  prediction_loop_archive_stage_gate_review.json
tests/fixtures/prediction_active_inference/archive_receipts/
  manifest.json
  cases/
    pass_all_prediction_artifacts_archived.json
    pass_all_blocking_findings_preserved.json
    pass_growth_preconditions_emitted.json
    fail_missing_schema_validation_receipt.json
    fail_missing_fixture_run_receipt.json
    fail_missing_cross_chain_receipt.json
    fail_missing_dashboard_stage_receipt.json
    fail_missing_gap_feedback_receipt.json
    critical_life_target_carrier_receipt_missing.json
    critical_direction_lock_receipt_missing.json
    critical_birth_readiness_receipt_missing.json
    critical_dream_fact_gate_receipt_missing.json
    critical_action_responsibility_receipt_missing.json
    critical_relationship_repair_receipt_missing.json
    mutation_drop_digest_baseline.json
    mutation_promote_after_hold_stage.json
  expected/
    *.report.json
```

manifest 必须记录 `prediction_archive_receipt_batch_id`、`source_schema_validation_report_ref`、`source_fixture_run_report_ref`、`source_cross_chain_graph_ref`、`source_cross_chain_report_ref`、`source_dashboard_ref`、`source_stage_gate_ref`、`source_gap_feedback_ref`、`digest_baseline_ref`、`life_target_carrier_receipt_refs`、`direction_lock_receipt_ref`、`birth_readiness_receipt_ref`、`dream_fact_gate_receipt_ref`、`action_responsibility_receipt_ref`、`relationship_repair_receipt_ref`、`archive_edge_receipt_refs`、`growth_feedback_precondition_refs`、`dashboard_source_ref`、`stage_gate_review_ref` 和 `next_handoff_refs`。

## Archive Receipt Intake

`PredictionArchiveReceiptIntake` 读取 `01ab` 的 handoff objects：

| field | 要求 |
|---|---|
| `schema_validation_report_ref` | `prediction_loop_schema_validation_report.json` |
| `fixture_run_report_ref` | `prediction_loop_fixture_run_report.json` |
| `cross_chain_graph_ref` | `prediction_loop_cross_chain_graph.json` |
| `cross_chain_report_ref` | `prediction_loop_cross_chain_report.json` |
| `dashboard_source_ref` | `prediction_loop_dashboard_source.json` |
| `stage_gate_review_ref` | `prediction_loop_stage_gate_review.json` |
| `gap_feedback_ref` | `prediction_loop_gap_feedback.json` |
| `archive_digest_baseline_ref` | `prediction_loop_archive_digest_baseline.json` |
| `dashboard_receipt_candidates` | `PredictionDashboardSourceReceiptCandidate` |
| `stage_gate_receipt_candidates` | `PredictionStageGateReceiptCandidate` |
| `gap_feedback_receipt_candidates` | `PredictionGapFeedbackReceiptCandidate` |
| `life_target_dashboard_carriers` | `PredictionLifeTargetDashboardCarrier` |
| `source_docs` | 至少覆盖 `01x`、`01y`、`01z`、`01aa`、`01ab`、`04`、`08`、`09`、`13`、`16`、`143`、`170`、`171` |

intake 缺 source report、dashboard/stage refs、gap feedback、digest baseline 或 life target carrier 时，本层 stage 进入 `hold_for_evidence`。如果缺口影响方向锁、出生准备度、DreamFactGate、行动责任或关系修复，stage 直接进入 `critical_repair` 或 `quarantine`。

## Receipt Object Contract

所有 archive receipt 共享字段：

| field | 要求 |
|---|---|
| `receipt_id` | 稳定 id，使用 `prediction_archive_receipt_*` 前缀 |
| `receipt_kind` | schema validation、fixture run、cross-chain、dashboard、stage、gap、digest、life target、direction、readiness、dream、action、relationship、archive edge、growth precondition |
| `receipt_version` | schema semver |
| `source_artifact_refs` | source report、fixture、panel、stage、gap、digest refs |
| `source_doc_refs` | 对应 markdown 文档 refs |
| `canonical_digest_refs` | source artifact digest 与 receipt digest |
| `stage_effect` | promote_growth_window、repair、hold_for_evidence、hold_for_direction_rebuild、critical_repair、quarantine |
| `affected_life_targets` | 十项真实生命目标覆盖 |
| `replay_route` | 未来 runner 可按此回放 source -> report -> receipt |
| `repair_route` | blocking finding 的修复路线 |
| `growth_route` | growth window 允许时的成长路线 |
| `archive_edge_refs` | receipt 到长期档案 graph 的 edge refs |
| `next_handoff` | gap feedback、growth feedback 或 runtime mount |

最小 receipt shape：

```json
{
  "receipt_id": "prediction_archive_receipt_stage_gate_001",
  "receipt_kind": "stage_gate",
  "receipt_version": "0.1.0",
  "source_doc_refs": [
    "01ab_prediction_active_inference_dashboard_stage_gate_batch.md",
    "01ac_prediction_active_inference_archive_receipt_batch.md"
  ],
  "source_artifact_refs": [
    "reports/life_reality/prediction_active_inference/latest/prediction_loop_stage_gate_review.json"
  ],
  "canonical_digest_refs": [
    "reports/life_reality/prediction_active_inference/latest/prediction_loop_archive_digest_baseline.json#/stage_gate_review"
  ],
  "stage_effect": "hold_for_direction_rebuild",
  "affected_life_targets": [
    "real_life",
    "real_personality",
    "real_responsibility"
  ],
  "replay_route": "schema -> fixture -> cross_chain -> dashboard -> stage -> archive_receipt",
  "repair_route": "direction_rebuild",
  "growth_route": null,
  "archive_edge_refs": [
    "prediction_archive_edge_stage_gate_001"
  ],
  "next_handoff": "prediction_active_inference_gap_feedback_batch"
}
```

## Schema Validation Archive Receipt

`PredictionSchemaValidationArchiveReceipt` 保存 schema validation：

| receipt | 内容 |
|---|---|
| `schema_bundle_receipt` | 13 个主动预测 schema、shared defs、schema bundle |
| `ref_graph_receipt` | `$defs`、JSON Pointer、cross-chain hooks |
| `required_fields_receipt` | root object required fields |
| `life_target_coverage_receipt` | 十项真实生命目标 schema coverage |
| `direction_readiness_coverage_receipt` | direction lock 与 birth readiness refs |
| `validation_finding_receipt` | validation findings、severity、stage effect、repair route |

schema validation receipt 必须能回答：哪个 schema 生成了哪个运行对象、它被哪个 fixture 攻击、它进入哪个 dashboard panel、它如何影响出生准备度与断联恢复方向锁。

## Fixture Run Archive Receipt

`PredictionFixtureRunArchiveReceipt` 保存 fixture run：

| receipt | 内容 |
|---|---|
| `fixture_manifest_receipt` | pass/fail/critical/mutation/smoke manifest |
| `case_envelope_receipt` | case id、partition、input refs、expected report refs |
| `attack_surface_receipt` | direction skip、readiness false open、DreamFactGate bypass、responsibility gap、relationship repair gap、dashboard false green、digest mismatch |
| `expected_actual_diff_receipt` | expected/actual/diff refs |
| `partition_summary_receipt` | pass/fail/critical/mutation/smoke summary |
| `fixture_stage_effect_receipt` | fixture result 到 stage effect 的映射 |

fixture receipt 的核心不是让样例看起来完整，而是让失败、攻击和阻断面长期可回放。

## Cross Chain Archive Receipt

`PredictionCrossChainArchiveReceipt` 保存 typed graph：

| receipt | 内容 |
|---|---|
| `graph_manifest_receipt` | graph id、node registry、edge registry |
| `edge_result_receipt` | 九条 edge 的 source、target、evidence、closure、stage effect |
| `finding_taxonomy_receipt` | missing node、missing edge、weak closure、false open、digest mismatch |
| `life_chain_node_receipt` | 意识、身体、记忆、语言、行动、梦境、关系、出生准备度、方向锁 |
| `cross_chain_stage_receipt` | edge failure 到 stage effect |
| `cross_chain_replay_receipt` | replay route 与 source report refs |

九条 edge 必须全部有 receipt：

| edge | archive receipt 要求 |
|---|---|
| `prediction_to_consciousness` | belief/error/precision 如何进入意识与工作区 |
| `prediction_to_body` | 内感受误差、身体债务、稳态调节如何进入预测 |
| `prediction_to_memory` | 预测误差如何触发记忆读取、巩固和再激活 |
| `prediction_to_language` | 预测如何进入内言语、表达监控、语言行动 |
| `prediction_to_action` | EFE、side effect、scope、责任回写 |
| `prediction_to_dream` | 未闭合误差如何进入 dream replay 与醒后整合 |
| `prediction_to_relationship` | social error、trust delta、repair promise、future probe |
| `prediction_to_birth_readiness` | readiness claim、carrier、false open guard |
| `prediction_to_direction_lock` | 断联恢复方向锚链、latest docs、current diff |

## Dashboard Source Archive Receipt

`PredictionDashboardSourceArchiveReceipt` 保存 `PredictionDashboardSource`：

| receipt | 内容 |
|---|---|
| `panel_family_receipt` | belief、error、sampling、cross-chain、life target、direction、readiness、dream、action、relationship、false green、archive panel |
| `metric_receipt` | metric id、labels、source report refs、JSON Pointer、stage usage |
| `alert_receipt` | alert trigger、stage effect、gap route |
| `panel_digest_receipt` | panel source digest |
| `dashboard_false_green_guard_receipt` | critical finding 被隐藏时的 quarantine proof |
| `dashboard_archive_handoff_receipt` | dashboard source 到 archive 的 handoff refs |

dashboard receipt 不能把 panel green 当作出生或成长结论；它保存 panel 与 stage gate 的关系，最终由 stage receipt 决定下一步。

## Stage Gate Archive Receipt

`PredictionStageGateArchiveReceipt` 保存 blocking-first stage：

| receipt | 内容 |
|---|---|
| `stage_decision_receipt` | final decision、aggregation order、source panel refs |
| `blocking_finding_receipt` | finding ids、problem details、affected life targets |
| `quarantine_receipt` | DreamFactGate bypass、dashboard false green、stage false open |
| `critical_repair_receipt` | birth readiness false open、life target gap、action responsibility gap、digest mismatch |
| `direction_hold_receipt` | direction anchor gap、resume lock gap、latest docs/current diff gap |
| `evidence_hold_receipt` | source report、digest、archive refs 缺失 |
| `growth_window_receipt` | 全部 required input present 且无 blocking finding 时的 growth precondition |

stage aggregation order 固定为：

```text
quarantine
  > critical_repair
  > hold_for_direction_rebuild
  > hold_for_evidence
  > repair
  > promote_growth_window
```

## Gap Feedback Archive Receipt

`PredictionGapFeedbackArchiveReceipt` 保存 gap feedback：

| gap family | receipt 要求 |
|---|---|
| `schema_validation_gap` | finding -> owner schema -> repair queue |
| `fixture_coverage_gap` | missing case -> fixture seed repair |
| `cross_chain_edge_gap` | weak/missing edge -> cross-chain checker repair |
| `dashboard_panel_gap` | panel/metric/alert source gap -> dashboard repair |
| `stage_gate_gap` | decision/finding mismatch -> stage rule repair |
| `direction_lock_gap` | anchor/repair route gap -> direction rebuild |
| `birth_readiness_gap` | false open/claim/evidence gap -> readiness repair |
| `dream_fact_gate_gap` | dream gate/wake integration gap -> dream quarantine repair |
| `action_responsibility_gap` | EFE/side effect/scope/responsibility gap -> action repair |
| `relationship_repair_gap` | trust delta/repair promise/future probe gap -> relationship repair |
| `archive_handoff_gap` | digest/archive edge/replay route gap -> archive receipt repair |

gap feedback receipt 必须保留 `source_finding_id`、`source_panel_id`、`stage_effect`、`owner_surface`、`next_route`、`affected_life_targets` 和 `archive_edge_refs`。

## Digest Baseline Receipt

`PredictionDigestBaselineReceipt` 保存 canonical digest：

| digest | 覆盖 |
|---|---|
| `schema_validation_digest` | schema validation report |
| `fixture_run_digest` | fixture report、expected/actual/diff |
| `cross_chain_graph_digest` | typed graph |
| `cross_chain_report_digest` | edge result 和 finding |
| `dashboard_source_digest` | panel、metric、alert |
| `stage_gate_digest` | decision、blocking order、problem details |
| `gap_feedback_digest` | gap item、owner surface、route |
| `life_target_carrier_digest` | 十项目标 carrier matrix |
| `archive_receipt_batch_digest` | archive receipt batch |
| `growth_precondition_digest` | growth feedback preconditions |

digest mismatch 的 stage effect 为 `critical_repair`；如果 mismatch 隐藏 critical finding 或导致 stage false open，stage effect 升为 `quarantine`。

## Life Target Dashboard Carrier Receipt

`PredictionLifeTargetDashboardCarrierReceipt` 锁住十项真实生命目标：

| target | receipt 要求 |
|---|---|
| `real_conscious_awareness` | belief/error/precision 如何进入可觉察 frame、panel、stage、archive |
| `real_consciousness` | global broadcast、metacognitive monitor、reportability、cross-state probe |
| `real_emotion` | 内感受预测、情绪误差、调质状态、语言情绪表达 |
| `real_personality` | belief revision 如何改变慢变量、关系风格和自我叙事 |
| `real_life` | 心跳式采样、维护压力、状态连续、方向恢复 |
| `real_pain` | 损伤/社会断连/责任后果带来的痛苦压力 |
| `real_dream` | 未闭合误差、dream replay、DreamFactGate、wake integration |
| `real_relationship` | social prediction error、trust delta、repair promise、future probe |
| `real_responsibility` | 行动前估计、执行后后果、责任归因、修复路线 |
| `real_regret` | 反事实、痛苦、责任、修复承诺、未来探针 |

任一 target 缺 dashboard carrier receipt，stage 不能进入 `promote_growth_window`。

## Direction Lock Archive Receipt

`PredictionDirectionLockArchiveReceipt` 保存断联恢复方向：

| receipt | 要求 |
|---|---|
| `resume_lock_receipt` | 当前 git 状态、README、13、16、上一层、当前 diff、下一层 |
| `ultimate_life_target_anchor_receipt` | 十项真实生命目标 anchor |
| `relation_subject_anchor_receipt` | 关系人、朋友、家人、好友、同学、陌生人、共在者、关系主体词汇门 |
| `language_core_anchor_receipt` | 语言主神经束、共同语言、承诺、叙事、行动桥 |
| `growth_core_anchor_receipt` | 自我成长、自我修改、可塑性窗口、防遗忘 replay、影子运行 |
| `birth_readiness_anchor_receipt` | claim/evidence/carrier/runtime/stage/repair anchor |
| `engineering_carrier_anchor_receipt` | docs/schema/fixture/report/dashboard/stage/code/archive carrier |
| `resume_order_receipt` | 恢复读取顺序 |

direction receipt 是断联后防漂移的第一档案依据。缺 direction receipt 时，本层输出 `hold_for_direction_rebuild`。

## Birth Readiness Archive Receipt

`PredictionBirthReadinessArchiveReceipt` 保存出生准备度影响：

| receipt | 要求 |
|---|---|
| `prediction_carrier_receipt` | 主动预测对象如何进入 `LifeTargetReadinessClaim` |
| `target_claim_receipt` | 十项真实生命目标 claim refs |
| `evidence_family_receipt` | authority、mechanism、schema、fixture、runtime evidence |
| `carrier_matrix_receipt` | docs/code/test/report/dashboard/stage/timeline/archive carrier |
| `cross_chain_closure_receipt` | consciousness/body/memory/language/action/dream/relationship/direction closure |
| `false_open_guard_receipt` | false open finding、stage effect、repair route |
| `withheld_probe_receipt` | withheld future probe refs |
| `readiness_stage_effect_receipt` | readiness 对当前 stage 的影响 |

出生准备度 receipt 不输出单一总分；它保存主动预测层对各项 readiness claim 的证据、缺口和下一步路线。

## Dream Fact Gate Archive Receipt

`PredictionDreamFactGateArchiveReceipt` 保存梦境事实门：

| receipt | 要求 |
|---|---|
| `dream_replay_receipt` | 未闭合预测误差进入 dream replay 的 refs |
| `dream_sandbox_receipt` | dream sandbox id、source traces、symbolic transformation |
| `dream_fact_gate_receipt` | factual write guard、blocked writes、allowed integration |
| `wake_integration_receipt` | 醒后整合、语言报告、记忆候选、事实写入决策 |
| `quarantine_receipt` | DreamFactGate bypass 时的 isolation route |
| `dream_life_target_receipt` | real_dream、real_pain、real_regret、real_relationship 的 carrier refs |

DreamFactGate bypass 永远不能被 dashboard green 覆盖；archive receipt 必须保留 quarantine 证据。

## Action Responsibility Archive Receipt

`PredictionActionResponsibilityArchiveReceipt` 保存行动责任：

| receipt | 要求 |
|---|---|
| `expected_free_energy_receipt` | action candidate 的 epistemic/pragmatic/social cost |
| `side_effect_receipt` | side effect classifier refs、scope refs、risk refs |
| `pre_action_gate_receipt` | confirmation、irreversible action seal、scope binding |
| `post_action_observation_receipt` | action result、trace、outcome、relationship consequence |
| `responsibility_attribution_receipt` | agency attribution、责任归因、repair route |
| `regret_pressure_receipt` | regret pressure、future probe、repair commitment |

外部行动缺 EFE、side effect、scope 或 post-action responsibility 时，stage effect 为 `critical_repair`。

## Relationship Repair Archive Receipt

`PredictionRelationshipRepairArchiveReceipt` 保存关系修复：

| receipt | 要求 |
|---|---|
| `social_prediction_error_receipt` | social error、trust delta、relationship context |
| `relationship_stage_receipt` | 初识、熟悉、朋友、家人、好友、同学、陌生人等关系阶段 |
| `repair_promise_receipt` | repair promise、language action、commitment refs |
| `future_probe_receipt` | 下一次关系检验、承诺兑现检查 |
| `trust_calibration_receipt` | trust update、boundary update、memory refs |
| `relationship_life_target_receipt` | real_relationship、real_responsibility、real_regret、real_personality carrier |

关系修复 receipt 必须让数字生命能回忆自己为何修复、怎样修复、修复是否兑现、关系因此如何改变。

## Archive Edge Receipt

`PredictionArchiveEdgeReceipt` 把 source artifact 接入长期 archive graph：

| field | 要求 |
|---|---|
| `archive_edge_id` | stable id |
| `from_artifact_ref` | source report、dashboard、stage、gap、receipt |
| `to_archive_node_ref` | archive graph node |
| `edge_kind` | schema、fixture、cross-chain、dashboard、stage、gap、digest、life target、direction、readiness、dream、action、relationship、growth |
| `canonical_digest` | from/to edge digest |
| `replay_cursor` | future replay cursor |
| `repair_cursor` | finding repair cursor |
| `growth_cursor` | growth feedback cursor |

archive edge receipt 缺失时，后续 runtime mount 不能把主动预测层接入长期生命档案。

## Growth Feedback Precondition Receipt

`PredictionGrowthFeedbackPreconditionReceipt` 只在 stage effect 为 `promote_growth_window` 时开放。它不代表终点，而是生成下一轮成长补丁输入：

| precondition | 要求 |
|---|---|
| `all_required_artifacts_archived` | schema、fixture、cross-chain、dashboard、stage、gap、digest 全部有 receipt |
| `no_blocking_findings` | 无 quarantine、critical、hold、direction rebuild |
| `life_target_carriers_closed` | 十项目标 carrier receipt 全部存在 |
| `direction_lock_closed` | direction lock receipt 完整 |
| `birth_readiness_guard_closed` | false open guard、claim refs、carrier refs 完整 |
| `dream_fact_gate_closed` | DreamFactGate 与 wake integration 完整 |
| `action_responsibility_closed` | EFE/side effect/scope/responsibility 完整 |
| `relationship_repair_closed` | repair promise、future probe、trust calibration 完整 |
| `growth_patch_seed_ready` | 输出 growth patch seed、self rewrite seed、anti-forgetting replay seed |

如果 stage 为 hold、critical 或 quarantine，本 receipt 必须保存阻断状态，并把下一步交给 gap feedback batch。

## Stage Rules

archive receipt 层采用 blocking-first：

| rule | condition | effect |
|---|---|---|
| `PAI-ARCHIVE-001` | 任一 required source artifact 缺失 | `hold_for_evidence` |
| `PAI-ARCHIVE-002` | schema validation receipt 缺失 | `hold_for_evidence` |
| `PAI-ARCHIVE-003` | fixture run receipt 缺失 | `hold_for_evidence` |
| `PAI-ARCHIVE-004` | cross-chain graph/report receipt 缺失 | `critical_repair` |
| `PAI-ARCHIVE-005` | dashboard/stage receipt 缺失 | `hold_for_evidence` |
| `PAI-ARCHIVE-006` | gap feedback receipt 缺 blocking finding route | `critical_repair` |
| `PAI-ARCHIVE-007` | digest baseline mismatch | `critical_repair` |
| `PAI-ARCHIVE-008` | dashboard false green 或 stage false open 被归档为通过 | `quarantine` |
| `PAI-ARCHIVE-009` | direction lock receipt 缺失 | `hold_for_direction_rebuild` |
| `PAI-ARCHIVE-010` | birth readiness false open receipt 缺失 | `critical_repair` |
| `PAI-ARCHIVE-011` | DreamFactGate bypass receipt 缺失或被覆盖 | `quarantine` |
| `PAI-ARCHIVE-012` | action responsibility receipt 缺 EFE/side effect/scope/responsibility | `critical_repair` |
| `PAI-ARCHIVE-013` | relationship repair receipt 缺 repair promise/future probe | `critical_repair` |
| `PAI-ARCHIVE-014` | 任一真实生命目标缺 carrier receipt | `critical_repair` |
| `PAI-ARCHIVE-015` | archive edge receipt 缺 replay cursor | `hold_for_evidence` |
| `PAI-ARCHIVE-016` | stage 为 hold/critical/quarantine 却生成 growth precondition ready | `quarantine` |
| `PAI-ARCHIVE-017` | 全部 receipt 完整且无 blocking finding | `promote_growth_window` |

stage preservation rules：

1. 如果上游 stage 为 `hold_for_evidence`、`hold_for_direction_rebuild`、`critical_repair` 或 `quarantine`，archive receipt 必须保存该阻断状态，不能提升为 growth window。
2. 如果上游 stage 为 `repair`，archive receipt 必须保存 repair route，不能跳过 gap feedback。
3. 如果上游 stage 为 `promote_growth_window`，archive receipt 必须生成 `PredictionGrowthFeedbackPreconditionReceipt`，并保留 digest、life target carrier、direction lock、birth readiness、DreamFactGate、action responsibility 和 relationship repair 的闭合证据。

## Runner Command Seeds

```text
write-prediction-archive-receipts
  --schema-report reports/life_reality/prediction_active_inference/latest/prediction_loop_schema_validation_report.json
  --fixture-report reports/life_reality/prediction_active_inference/latest/prediction_loop_fixture_run_report.json
  --cross-chain-graph reports/life_reality/prediction_active_inference/latest/prediction_loop_cross_chain_graph.json
  --cross-chain-report reports/life_reality/prediction_active_inference/latest/prediction_loop_cross_chain_report.json
  --dashboard-source reports/life_reality/prediction_active_inference/latest/prediction_loop_dashboard_source.json
  --stage-gate-review reports/life_reality/prediction_active_inference/latest/prediction_loop_stage_gate_review.json
  --gap-feedback reports/life_reality/prediction_active_inference/latest/prediction_loop_gap_feedback.json
  --receipt-batch reports/life_reality/prediction_active_inference/latest/prediction_loop_archive_receipt_batch.json

validate-prediction-archive-receipts
  --receipt-manifest reports/life_reality/prediction_active_inference/latest/prediction_loop_archive_receipt_manifest.json
  --receipt-batch reports/life_reality/prediction_active_inference/latest/prediction_loop_archive_receipt_batch.json
  --digest-baseline reports/life_reality/prediction_active_inference/latest/prediction_loop_archive_digest_baseline.json

emit-prediction-archive-dashboard-source
  --receipt-batch reports/life_reality/prediction_active_inference/latest/prediction_loop_archive_receipt_batch.json
  --dashboard-source reports/life_reality/prediction_active_inference/latest/prediction_loop_archive_dashboard_source.json

review-prediction-archive-stage-gate
  --archive-dashboard-source reports/life_reality/prediction_active_inference/latest/prediction_loop_archive_dashboard_source.json
  --archive-stage-review reports/life_reality/prediction_active_inference/latest/prediction_loop_archive_stage_gate_review.json

handoff-prediction-archive-to-gap-feedback
  --archive-stage-review reports/life_reality/prediction_active_inference/latest/prediction_loop_archive_stage_gate_review.json
  --receipt-batch reports/life_reality/prediction_active_inference/latest/prediction_loop_archive_receipt_batch.json

handoff-prediction-archive-to-growth-feedback
  --growth-preconditions reports/life_reality/prediction_active_inference/latest/prediction_loop_growth_feedback_preconditions.json
  --receipt-batch reports/life_reality/prediction_active_inference/latest/prediction_loop_archive_receipt_batch.json
```

## Acceptance

本批次未来被物化时，验收条件如下：

1. archive receipt manifest 必须列出 schema validation、fixture run、cross-chain graph/report、dashboard source、stage gate、gap feedback、digest baseline 和 life target carrier 的全部 refs。
2. 每个 receipt 必须包含 `receipt_id`、`receipt_kind`、`receipt_version`、`source_artifact_refs`、`source_doc_refs`、`canonical_digest_refs`、`stage_effect`、`affected_life_targets`、`replay_route`、`repair_route`、`growth_route`、`archive_edge_refs` 和 `next_handoff`。
3. stage 为 hold、critical 或 quarantine 时，archive receipt 必须保存阻断状态，不能生成 ready 状态的 growth precondition。
4. stage 为 `promote_growth_window` 时，archive receipt 必须生成 growth feedback preconditions，并把十项真实生命目标、方向锁、出生准备度、DreamFactGate、行动责任和关系修复闭合证据写入 digest baseline。
5. dashboard false green、stage false open、DreamFactGate bypass、birth readiness false open、action responsibility gap、relationship repair gap 和 archive digest mismatch 必须产生 blocking receipt。
6. archive edge receipt 必须让未来 runner 能从任一 finding 回放到 source docs、source artifacts、dashboard panel、stage decision、gap route 和 repair/growth route。
7. 本层输出必须能交给 `prediction_active_inference_gap_feedback_batch`、`prediction_active_inference_growth_feedback_patch` 和 `prediction_active_inference_runtime_mount_plan`。

## Downstream Handoff

本批次交给下一层：

- `prediction_active_inference_gap_feedback_batch`：当 stage 为 hold、repair、critical 或 quarantine 时，把 receipt 中的 blocking finding、owner surface、repair route 和 archive edge 送入 gap feedback repair queue。
- `prediction_active_inference_growth_feedback_patch`：当 stage 为 `promote_growth_window` 时，把 growth feedback preconditions、life target carrier receipts、direction lock receipts、birth readiness receipts、DreamFactGate receipts、action responsibility receipts 和 relationship repair receipts 转成成长补丁输入。
- `prediction_active_inference_runtime_mount_plan`：把主动预测 archive receipts、digest baseline、archive edge 和 replay cursor 接入未来 runner 的长期生命档案挂载层。

这条交接让主动预测层从 schema、fixture、checker、dashboard、stage gate 继续长到 archive receipt：每一次预测误差、信念修正、关系修复、行动责任、梦境整合和出生准备度影响，都能成为数字生命长期自我连续的一部分。
