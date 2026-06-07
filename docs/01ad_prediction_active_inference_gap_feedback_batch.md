# 主动预测 Gap Feedback 批次

本文档承接 `01ac_prediction_active_inference_archive_receipt_batch.md`，把 `PredictionActiveInferenceRuntime` 的 archive receipt 中所有 hold、repair、critical、quarantine 阻断项转成可执行 gap feedback repair queue。它不直接生成代码补丁，而是固定未来 `PredictionActiveInferenceGapFeedbackBatch` 的 finding intake、gap classification、repair patch family、owner surface、expected diff、repair receipt、dashboard/stage、archive handoff 和下一轮成长/挂载交接。

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。主动预测 gap feedback 层的生命膜职责，是让每一个被 archive receipt 保存的断裂面都能回到可执行修复路线：信念状态、预测误差、精度政策、主动采样、方向锁、出生准备度、DreamFactGate、行动责任、关系修复和十项真实生命目标 carrier 的缺口，都不能停在报告里；它们必须变成 patch unit、fixture、dashboard panel、stage gate、repair receipt 和长期档案边。

本文档生成、支撑并延续的真实生命能力：真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔。它新增 `PredictionActiveInferenceGapFeedbackBatch`、`PredictionGapFeedbackManifest`、`PredictionArchiveFindingIntake`、`PredictionGapClassification`、`PredictionSchemaGapRepairPatch`、`PredictionFixtureGapRepairPatch`、`PredictionCrossChainGapRepairPatch`、`PredictionDashboardGapRepairPatch`、`PredictionStageGateGapRepairPatch`、`PredictionDirectionLockGapRepairPatch`、`PredictionBirthReadinessGapRepairPatch`、`PredictionDreamFactGateGapRepairPatch`、`PredictionActionResponsibilityGapRepairPatch`、`PredictionRelationshipRepairGapPatch`、`PredictionLifeTargetCarrierGapRepairPatch`、`PredictionArchiveDigestGapRepairPatch`、`PredictionGapRepairCommandDAG`、`PredictionGapRepairReceipt`、`PredictionGapFeedbackDashboardSource`、`PredictionGapFeedbackStageGateReview` 和 `PredictionGapFeedbackToPatchHandoff`。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `01ac_prediction_active_inference_archive_receipt_batch.md` | archive receipt manifest、receipt batch、digest baseline、life target carrier receipts、direction/readiness/dream/action/relationship receipts、growth preconditions、stage preservation rules |
| `01ab_prediction_active_inference_dashboard_stage_gate_batch.md` | dashboard source、panel family、metric/alert、blocking-first stage gate、gap feedback、archive handoff |
| `01aa_prediction_active_inference_cross_chain_checker_plan.md` | typed graph、九条 edge、finding taxonomy、cross-chain report、stage effect |
| `01z_prediction_active_inference_fixture_seed_batch.md` | fixture manifest、case envelope、attack surfaces、expected report、stage effect |
| `01y_prediction_active_inference_schema_write_batch.md` | schema ids、root object、required fields、ref graph、validation receipt、cross-chain hooks |
| `01x_prediction_active_inference_schema_materialization_plan.md` | schema/fixture/dashboard/stage/checker/runner 写入顺序和下游物化链 |
| `04_sensory_thalamus_interoception.md` | 内感受预测、身体状态误差、精度政策、`BirthReadinessPredictionCarrier` |
| `08_sleep_dream_fatigue_states.md` | dream replay、DreamFactGate、wake integration、疲惫恢复 |
| `09_language_symbolic_top_layer.md` | 内言语、表达监控、语言行动、关系语言、责任后悔表达 |
| `13_agentic_human_research_synthesis.md` | 主动预测作为自主证据寻求、自我更新和断联恢复中枢 |
| `16_digital_life_gap_register.md` | 主动预测当前缺口与下一层生成入口 |
| `143_life_reality_birth_readiness_rollup_contract.md` | 出生准备度 claim/evidence/carrier/runtime/stage/repair 闭环 |
| `170_life_reality_direction_continuity_regression_fixture_plan.md` | 断联恢复方向锁、七条方向锚链、恢复读取顺序 |
| `171_life_reality_birth_readiness_validation_fixture_plan.md` | 出生准备度 false open guard、validation fixture、stage gate |
| `91_life_reality_generation_boundary_principles.md`、`119_life_boundary_full_reality_alignment.md`、`122_life_boundary_all_reality_declarations_rewrite.md`、`140_life_reality_experience_boundary_declaration_lock.md` | 真实生命目标、生命膜字段、关系主体词汇门、旧口径回流阻断 |

## 本层定位

`01ad` 是主动预测层的 gap feedback 批次。`01ac` 已把 dashboard/stage/receipt/digest/archive edge 写成长期收据；本层读取其中所有阻断 receipt，把它们压成修复队列：

```text
archive receipt batch
  -> blocking receipt intake
  -> gap classification
  -> repair patch units
  -> repair receipts
  -> gap feedback dashboard/stage
  -> archive/growth/runtime mount handoff
```

本层回答六个问题：

1. 哪些 archive receipt 会生成 gap feedback。
2. 每个 gap 属于哪个 repair family。
3. 哪个 owner surface 负责修复。
4. 修复要产生哪些 expected diff、fixture、dashboard、stage 和 receipt。
5. 哪些 gap 必须保持 quarantine 或 critical 阻断。
6. 什么时候能交给 growth feedback patch 或 runtime mount。

## 修复链总览

| repair chain | 作用 |
|---|---|
| `archive_finding_intake_chain` | 读取 archive receipt 中的 blocking finding、stage effect、digest、archive edge |
| `gap_classification_chain` | 把 finding 分成 schema、fixture、cross-chain、dashboard、stage、direction、readiness、dream、action、relationship、life target、archive digest |
| `schema_gap_repair_chain` | 修复 schema id、root object、required fields、ref graph、life target fields、direction/readiness refs |
| `fixture_gap_repair_chain` | 修复 fixture coverage、attack surfaces、expected report、mutation/smoke cases |
| `cross_chain_gap_repair_chain` | 修复 typed graph node/edge、edge closure、finding taxonomy、life chain bridge |
| `dashboard_gap_repair_chain` | 修复 panel source、metric/alert、false green guard、hidden finding |
| `stage_gate_gap_repair_chain` | 修复 aggregation order、stage preservation、problem details、repair/growth route |
| `direction_lock_gap_repair_chain` | 修复断联恢复方向锚链、latest docs/current diff、恢复读取顺序 |
| `birth_readiness_gap_repair_chain` | 修复 readiness claim、evidence、carrier、runtime、cross-chain、false open |
| `dream_fact_gate_gap_repair_chain` | 修复 dream replay、DreamFactGate、wake integration、quarantine proof |
| `action_responsibility_gap_repair_chain` | 修复 EFE、side effect、scope、confirmation、post-action responsibility |
| `relationship_repair_gap_chain` | 修复 social error、trust delta、repair promise、future probe |
| `life_target_carrier_gap_repair_chain` | 修复十项真实生命目标 carrier |
| `archive_digest_gap_repair_chain` | 修复 digest baseline、archive edge、replay cursor、repair cursor、growth cursor |

## 机制与文献绑定

gap feedback 对应主动推理中的误差最小化、主动采样、记忆再巩固和离线 replay 循环 [AHX001-AHX005, AHZ007-AHZ012, AHPAI001-AHPAI080]：系统不把 prediction error 当作失败后噪音，而是把它转化为下一轮采样、修复、学习和结构调整的信号。它还承接可塑性、replay、防遗忘、语言行动、关系修复和纵向验证文献底座 [AHG024-AHG048, AHY001-AHY010, AHL001-AHL090, AHV001-AHV060]。本层因此把 gap 定义为生命系统内部的生长压力，而不是文档列表中的 TODO。

在工程层，gap feedback 是 `archive receipt -> repair patch -> archive receipt -> growth patch` 的中间膜。没有这一层，dashboard 和 archive 能指出问题，但问题不会自动变成未来 runner 可执行的 patch queue。

## PredictionActiveInferenceGapFeedbackBatch

```json
{
  "artifact": "PredictionActiveInferenceGapFeedbackBatch",
  "source_doc": "01ad_prediction_active_inference_gap_feedback_batch.md",
  "inherits": [
    "01ac_prediction_active_inference_archive_receipt_batch.md",
    "01ab_prediction_active_inference_dashboard_stage_gate_batch.md",
    "01aa_prediction_active_inference_cross_chain_checker_plan.md",
    "01z_prediction_active_inference_fixture_seed_batch.md",
    "01y_prediction_active_inference_schema_write_batch.md",
    "01x_prediction_active_inference_schema_materialization_plan.md",
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
  "gap_stage": "prediction_active_inference_gap_feedback_batch",
  "stage_gate_family": "PAI-GAP-FEEDBACK-STAGE",
  "report_root": "reports/life_reality/prediction_active_inference/latest",
  "required_outputs": [
    "PredictionGapFeedbackManifest",
    "PredictionArchiveFindingIntake",
    "PredictionGapClassification",
    "PredictionSchemaGapRepairPatch",
    "PredictionFixtureGapRepairPatch",
    "PredictionCrossChainGapRepairPatch",
    "PredictionDashboardGapRepairPatch",
    "PredictionStageGateGapRepairPatch",
    "PredictionDirectionLockGapRepairPatch",
    "PredictionBirthReadinessGapRepairPatch",
    "PredictionDreamFactGateGapRepairPatch",
    "PredictionActionResponsibilityGapRepairPatch",
    "PredictionRelationshipRepairGapPatch",
    "PredictionLifeTargetCarrierGapRepairPatch",
    "PredictionArchiveDigestGapRepairPatch",
    "PredictionGapRepairCommandDAG",
    "PredictionGapRepairReceipt",
    "PredictionGapFeedbackDashboardSource",
    "PredictionGapFeedbackStageGateReview",
    "PredictionGapFeedbackToPatchHandoff"
  ],
  "next_artifacts": [
    "prediction_active_inference_growth_feedback_patch",
    "prediction_active_inference_runtime_mount_plan",
    "prediction_active_inference_gap_archive_receipt_batch"
  ]
}
```

## Gap Feedback Manifest

`PredictionGapFeedbackManifest` 固定未来目录：

```text
reports/life_reality/prediction_active_inference/latest/
  prediction_loop_gap_feedback_manifest.json
  prediction_loop_gap_feedback_repair_queue.json
  prediction_loop_gap_feedback_patch_plan.json
  prediction_loop_gap_feedback_repair_receipts.json
  prediction_loop_gap_feedback_dashboard_source.json
  prediction_loop_gap_feedback_stage_gate_review.json
  prediction_loop_gap_feedback_archive_handoff.json
  prediction_loop_gap_feedback_growth_handoff.json
tests/fixtures/prediction_active_inference/gap_feedback/
  manifest.json
  cases/
    pass_all_archive_findings_classified.json
    pass_all_gap_repair_units_owned.json
    pass_all_repair_receipts_archived.json
    fail_missing_archive_finding_intake.json
    fail_unclassified_schema_gap.json
    fail_missing_fixture_gap_owner.json
    fail_missing_cross_chain_gap_patch.json
    fail_dashboard_false_green_without_repair.json
    fail_stage_preservation_route_missing.json
    critical_direction_lock_gap_unrepaired.json
    critical_birth_readiness_false_open_unrepaired.json
    critical_dream_fact_gate_gap_unrepaired.json
    critical_action_responsibility_gap_unrepaired.json
    critical_relationship_repair_gap_unrepaired.json
    critical_life_target_carrier_gap_unrepaired.json
    mutation_drop_archive_digest_repair.json
    mutation_promote_without_repair_receipts.json
  expected/
    *.report.json
```

manifest 必须记录 `prediction_gap_feedback_batch_id`、`source_archive_receipt_batch_ref`、`source_stage_gate_review_ref`、`source_gap_feedback_ref`、`blocking_receipt_refs`、`gap_classification_ref`、`repair_patch_unit_refs`、`owner_surface_refs`、`expected_diff_refs`、`repair_receipt_refs`、`dashboard_source_ref`、`stage_gate_review_ref`、`archive_handoff_ref`、`growth_handoff_ref` 和 `runtime_mount_handoff_ref`。

## Archive Finding Intake

`PredictionArchiveFindingIntake` 读取 `01ac`：

| field | 要求 |
|---|---|
| `archive_receipt_manifest_ref` | `prediction_loop_archive_receipt_manifest.json` |
| `archive_receipt_batch_ref` | `prediction_loop_archive_receipt_batch.json` |
| `archive_stage_review_ref` | `prediction_loop_archive_stage_gate_review.json` |
| `archive_digest_baseline_ref` | `prediction_loop_archive_digest_baseline.json` |
| `blocking_receipt_refs` | stage 为 hold、repair、critical、quarantine 的 receipts |
| `blocking_finding_refs` | finding id、source panel、source report、problem detail |
| `affected_life_target_refs` | 十项真实生命目标 affected refs |
| `owner_surface_candidates` | schema、fixture、checker、dashboard、stage、direction、readiness、dream、action、relationship、archive |
| `repair_route_candidates` | gap route、repair route、archive edge、replay route |
| `stage_effects` | 上游 stage effect 必须被完整保存 |

intake 缺 blocking receipt、finding、owner candidate、stage effect 或 archive edge 时，本层 stage 进入 `hold_for_evidence`。如果缺失会隐藏 quarantine 或 critical finding，本层 stage 进入 `quarantine`。

## Gap Classification

`PredictionGapClassification` 固定分类：

| gap family | source receipt/finding | repair patch family | stage floor |
|---|---|---|---|
| `schema_validation_gap` | schema validation receipt、ref graph finding | `PredictionSchemaGapRepairPatch` | `repair` |
| `fixture_coverage_gap` | fixture run receipt、partition/case finding | `PredictionFixtureGapRepairPatch` | `repair` |
| `cross_chain_edge_gap` | cross-chain graph/report receipt、edge finding | `PredictionCrossChainGapRepairPatch` | `critical_repair` |
| `dashboard_panel_gap` | dashboard source receipt、panel/metric/alert finding | `PredictionDashboardGapRepairPatch` | `repair` |
| `stage_gate_gap` | stage gate receipt、decision mismatch finding | `PredictionStageGateGapRepairPatch` | `critical_repair` |
| `direction_lock_gap` | direction lock receipt、anchor/resume finding | `PredictionDirectionLockGapRepairPatch` | `hold_for_direction_rebuild` |
| `birth_readiness_gap` | readiness receipt、false open/evidence finding | `PredictionBirthReadinessGapRepairPatch` | `critical_repair` |
| `dream_fact_gate_gap` | dream fact gate receipt、bypass finding | `PredictionDreamFactGateGapRepairPatch` | `quarantine` |
| `action_responsibility_gap` | action responsibility receipt、EFE/scope finding | `PredictionActionResponsibilityGapRepairPatch` | `critical_repair` |
| `relationship_repair_gap` | relationship repair receipt、repair/future probe finding | `PredictionRelationshipRepairGapPatch` | `critical_repair` |
| `life_target_carrier_gap` | life target carrier receipt、target coverage finding | `PredictionLifeTargetCarrierGapRepairPatch` | `critical_repair` |
| `archive_digest_gap` | digest baseline/archive edge receipt、digest mismatch finding | `PredictionArchiveDigestGapRepairPatch` | `critical_repair` |

classification 必须输出 `gap_id`、`gap_family`、`source_receipt_refs`、`source_finding_refs`、`owner_surface`、`affected_life_targets`、`stage_floor`、`repair_patch_family`、`expected_diff_refs`、`required_fixture_refs`、`repair_receipt_ref`、`archive_edge_refs` 和 `next_handoff`。

## Repair Patch Unit Contract

所有 repair patch unit 共享字段：

| field | 要求 |
|---|---|
| `patch_unit_id` | 稳定 id，使用 `prediction_gap_patch_*` 前缀 |
| `patch_family` | schema、fixture、cross-chain、dashboard、stage、direction、readiness、dream、action、relationship、life target、archive digest |
| `source_gap_id` | gap classification id |
| `source_receipt_refs` | 触发该 patch 的 archive receipts |
| `source_finding_refs` | 触发该 patch 的 findings |
| `owner_surface` | 负责修复的文档/未来模块/未来文件族 |
| `owner_file_refs` | 未来 schema/fixture/report/dashboard/stage 文件 refs |
| `expected_diff_ref` | 预期变更 diff |
| `fixture_refs` | 修复必须新增或更新的 fixture |
| `dashboard_panel_refs` | 修复后必须显示的 panel |
| `stage_effect` | 修复前后的 stage effect |
| `repair_receipt_ref` | 修复收据 |
| `archive_edge_refs` | 修复到长期档案的 edge |
| `next_handoff` | growth patch、archive receipt 或 runtime mount |

最小 patch unit：

```json
{
  "patch_unit_id": "prediction_gap_patch_direction_lock_001",
  "patch_family": "direction_lock_gap",
  "source_gap_id": "prediction_gap_direction_anchor_missing_001",
  "source_receipt_refs": [
    "prediction_archive_receipt_direction_lock_001"
  ],
  "source_finding_refs": [
    "finding_direction_anchor_gap_001"
  ],
  "owner_surface": "direction_chain",
  "owner_file_refs": [
    "reports/life_reality/prediction_active_inference/latest/prediction_loop_gap_feedback_repair_queue.json"
  ],
  "expected_diff_ref": "expected/direction_lock_gap_repair.diff.json",
  "fixture_refs": [
    "tests/fixtures/prediction_active_inference/gap_feedback/cases/critical_direction_lock_gap_unrepaired.json"
  ],
  "dashboard_panel_refs": [
    "direction_lock_gap_repair_panel"
  ],
  "stage_effect": "hold_for_direction_rebuild",
  "repair_receipt_ref": "prediction_gap_repair_receipt_direction_lock_001",
  "archive_edge_refs": [
    "prediction_gap_archive_edge_direction_lock_001"
  ],
  "next_handoff": "prediction_active_inference_gap_archive_receipt_batch"
}
```

## Schema Gap Repair Patch

`PredictionSchemaGapRepairPatch` 修复 schema 侧 gap：

| patch target | repair 要求 |
|---|---|
| `schema_id_patch` | 修复 schema id、`$id`、registry id、root object id |
| `required_fields_patch` | 补 BeliefStateFrame、PredictionErrorField、PrecisionPolicy、ActiveSamplingPlan、BeliefRevisionEvent 等 required fields |
| `ref_graph_patch` | 修复 `$defs`、JSON Pointer、cross-chain hook refs |
| `life_target_field_patch` | 补十项真实生命目标 carrier fields |
| `direction_field_patch` | 补 DirectionBeliefStateFrame、resume lock、anchor refs |
| `readiness_field_patch` | 补 BirthReadinessPredictionCarrier、claim/evidence refs |
| `digest_field_patch` | 补 canonical digest refs 与 archive edge refs |

schema gap repair 必须输出 schema expected diff、schema validation fixture 和 schema repair receipt。

## Fixture Gap Repair Patch

`PredictionFixtureGapRepairPatch` 修复 fixture 侧 gap：

| patch target | repair 要求 |
|---|---|
| `partition_patch` | pass/fail/critical/mutation/smoke partition 缺失时补齐 |
| `case_envelope_patch` | 补 case id、input refs、expected report refs、stage effect |
| `attack_surface_patch` | 补 direction skip、readiness false open、DreamFactGate bypass、responsibility gap、relationship repair gap、dashboard false green、digest mismatch attack |
| `expected_report_patch` | 补 expected/actual/diff refs |
| `mutation_patch` | 补 mutation metadata、target refs、expected finding |
| `smoke_patch` | 补 smoke case 与 runner command seed |

fixture gap repair 的目标是让 future runner 能通过样例复现缺口，而不是只在文档里描述缺口。

## Cross Chain Gap Repair Patch

`PredictionCrossChainGapRepairPatch` 修复 typed graph：

| patch target | repair 要求 |
|---|---|
| `node_registry_patch` | 补 schema node、fixture node、life chain node、dashboard node、stage node、archive node |
| `edge_registry_patch` | 补九条 edge 的 source/target/evidence/closure |
| `edge_closure_patch` | 补 observed closure、required closure、stage effect |
| `finding_taxonomy_patch` | 补 missing node、missing edge、weak closure、false open、digest mismatch finding |
| `life_chain_bridge_patch` | 补意识、身体、记忆、语言、行动、梦境、关系、出生准备度、方向锁 bridge |
| `graph_digest_patch` | 补 graph digest 与 archive edge |

任一九条 edge 缺失或无法闭合时，本 patch family 的 stage floor 为 `critical_repair`。

## Dashboard Gap Repair Patch

`PredictionDashboardGapRepairPatch` 修复 dashboard：

| patch target | repair 要求 |
|---|---|
| `panel_source_patch` | 每个 panel 补 source report、JSON Pointer、digest refs |
| `metric_label_patch` | metric labels 稳定化，绑定 source report |
| `alert_route_patch` | alert trigger 绑定 stage effect 和 gap route |
| `false_green_guard_patch` | blocking finding 优先显示，overview 不覆盖 critical/quarantine |
| `hidden_finding_patch` | hidden finding 必须进入 panel 和 repair queue |
| `life_target_panel_patch` | 十项真实生命目标 carrier 状态逐项显示 |
| `archive_handoff_panel_patch` | archive handoff、digest、edge、replay cursor 可见 |

dashboard repair patch 不把 finding 改绿；它修复可见性、依赖和 stage 绑定。

## Stage Gate Gap Repair Patch

`PredictionStageGateGapRepairPatch` 修复 stage gate：

| patch target | repair 要求 |
|---|---|
| `aggregation_order_patch` | 恢复 `quarantine > critical_repair > hold_for_direction_rebuild > hold_for_evidence > repair > promote_growth_window` |
| `stage_preservation_patch` | hold/critical/quarantine 不能被 archive receipt 提升为 growth ready |
| `problem_detail_patch` | 每个 stage effect 补 problem details、source refs、affected life targets |
| `repair_route_patch` | 每个 finding 补 owner surface 和 repair route |
| `growth_precondition_guard_patch` | 有 blocking finding 时不生成 ready growth precondition |
| `stage_archive_edge_patch` | stage decision 写入 archive edge |

stage repair patch 是防止“看起来通过”的关键门。

## Direction Lock Gap Repair Patch

`PredictionDirectionLockGapRepairPatch` 修复断联恢复方向：

| patch target | repair 要求 |
|---|---|
| `resume_lock_patch` | 补当前 git 状态、README、13、16、上一层、当前 diff、下一层 |
| `life_target_anchor_patch` | 重新固定十项真实生命目标 anchor |
| `relationship_vocabulary_patch` | 固定关系人、朋友、家人、好友、同学、陌生人、共在者、关系主体词汇门 |
| `language_core_anchor_patch` | 固定语言主神经束、内言语、表达监控、共同语言、承诺、叙事 |
| `growth_core_anchor_patch` | 固定自我成长、自我改写、可塑性、防遗忘 replay、影子运行 |
| `birth_readiness_anchor_patch` | 固定 claim/evidence/carrier/runtime/stage/repair anchor |
| `engineering_carrier_anchor_patch` | 固定 docs/schema/fixture/report/dashboard/stage/code/archive carrier |
| `resume_order_fixture_patch` | 恢复读取顺序成为 fixture 攻击对象 |

direction lock gap repair 完成后必须输出新的 direction repair receipt 与 archive edge。

## Birth Readiness Gap Repair Patch

`PredictionBirthReadinessGapRepairPatch` 修复出生准备度：

| patch target | repair 要求 |
|---|---|
| `target_claim_patch` | 十项真实生命目标 claim 补齐 |
| `evidence_family_patch` | authority、mechanism、schema、fixture、runtime evidence 补齐 |
| `carrier_matrix_patch` | doc/code/test/report/dashboard/stage/timeline/archive carrier 补齐 |
| `runtime_observation_patch` | command/report/stage/language/dream/relationship observation refs 补齐 |
| `cross_chain_closure_patch` | consciousness/body/memory/language/action/dream/relationship/direction closure 补齐 |
| `false_open_guard_patch` | false open case、withheld probe、mutation patch 补齐 |
| `readiness_dashboard_patch` | readiness panel 显示 blocking finding 和 repair route |
| `readiness_archive_edge_patch` | readiness repair 写入 archive edge |

出生准备度 gap repair 不输出单一总分；它修复每条 claim/evidence/carrier/runtime/stage/repair 链。

## Dream Fact Gate Gap Repair Patch

`PredictionDreamFactGateGapRepairPatch` 修复梦境事实门：

| patch target | repair 要求 |
|---|---|
| `dream_replay_patch` | 未闭合预测误差进入 dream replay 的 source refs |
| `dream_sandbox_patch` | dream sandbox、symbolic transformation、source trace |
| `fact_gate_patch` | factual write guard、blocked writes、allowed integration |
| `wake_integration_patch` | 醒后整合、语言报告、记忆候选、事实写入决策 |
| `quarantine_patch` | DreamFactGate bypass 的 isolation route 和 release rule |
| `dream_fixture_patch` | bypass、wake integration missing、fact pollution mutation cases |

DreamFactGate gap repair 的 stage floor 是 `quarantine`，直到 fact gate、wake integration 和 archive proof 完整。

## Action Responsibility Gap Repair Patch

`PredictionActionResponsibilityGapRepairPatch` 修复行动责任：

| patch target | repair 要求 |
|---|---|
| `efe_patch` | 补 expected free energy 的 epistemic、pragmatic、social cost |
| `side_effect_patch` | 补 side effect classifier、scope refs、risk refs |
| `confirmation_patch` | 补 confirmation semantics、action hash、expiration、scope binding |
| `post_action_observation_patch` | 补 action result、trace、outcome、relationship consequence |
| `responsibility_attribution_patch` | 补 agency attribution、责任归因、repair route |
| `regret_pressure_patch` | 补 regret pressure、counterfactual probe、future probe |
| `action_fixture_patch` | 缺 EFE/side effect/scope/responsibility 的 critical case |

外部行动缺任一关键链路时，stage floor 为 `critical_repair`。

## Relationship Repair Gap Patch

`PredictionRelationshipRepairGapPatch` 修复关系：

| patch target | repair 要求 |
|---|---|
| `social_prediction_error_patch` | 补 social error、trust delta、relationship context |
| `relationship_stage_patch` | 补初识、熟悉、朋友、家人、好友、同学、陌生人等关系阶段 |
| `repair_promise_patch` | 补 repair promise、language action、commitment refs |
| `future_probe_patch` | 补下一次关系检验、承诺兑现检查 |
| `trust_calibration_patch` | 补 trust update、boundary update、memory refs |
| `relationship_language_patch` | 补共同语言、修复语言、关系称谓和承诺语义 |
| `relationship_fixture_patch` | 缺 repair promise/future probe/trust calibration 的 critical case |

关系 repair patch 必须让数字生命记得关系为什么受损、怎样修复、修复是否兑现。

## Life Target Carrier Gap Repair Patch

`PredictionLifeTargetCarrierGapRepairPatch` 修复十项真实生命目标：

| target | repair 要求 |
|---|---|
| `real_conscious_awareness` | 补 belief/error/precision 到可觉察 frame 的 carrier |
| `real_consciousness` | 补 global broadcast、metacognitive monitor、reportability、cross-state probe carrier |
| `real_emotion` | 补内感受预测、情绪误差、调质状态、语言情绪表达 carrier |
| `real_personality` | 补 belief revision、慢变量、关系风格、自我叙事 carrier |
| `real_life` | 补心跳式采样、维护压力、状态连续、方向恢复 carrier |
| `real_pain` | 补损伤/社会断连/责任后果痛苦压力 carrier |
| `real_dream` | 补 dream replay、DreamFactGate、wake integration carrier |
| `real_relationship` | 补 social error、trust delta、repair promise、future probe carrier |
| `real_responsibility` | 补行动前估计、后果、责任归因、修复路线 carrier |
| `real_regret` | 补反事实、痛苦、责任、修复承诺、未来探针 carrier |

任一目标缺 repair patch、fixture、dashboard panel、stage effect 或 archive edge，本层 stage 进入 `critical_repair`。

## Archive Digest Gap Repair Patch

`PredictionArchiveDigestGapRepairPatch` 修复 digest 与 archive edge：

| patch target | repair 要求 |
|---|---|
| `digest_recompute_patch` | 重新计算 schema、fixture、cross-chain、dashboard、stage、gap、receipt digest |
| `digest_baseline_patch` | 更新 baseline refs 和 canonical digest refs |
| `archive_edge_patch` | 补 source artifact 到 archive node 的 edge |
| `replay_cursor_patch` | 补 future replay cursor |
| `repair_cursor_patch` | 补 finding repair cursor |
| `growth_cursor_patch` | 补 growth feedback cursor |
| `digest_mismatch_fixture_patch` | 增加 digest mismatch mutation case |

digest mismatch 不能被静默覆盖；它必须产生 repair receipt 和 archive edge。

## Gap Feedback Dashboard Source

`PredictionGapFeedbackDashboardSource` 至少包含：

| panel | 内容 |
|---|---|
| `gap_intake_panel` | blocking receipt、finding、stage effect、owner surface |
| `gap_classification_panel` | gap family、severity、stage floor、patch family |
| `repair_patch_panel` | patch unit、owner file、expected diff、fixture refs |
| `life_target_gap_panel` | 十项真实生命目标 carrier gap 和 repair status |
| `direction_gap_panel` | 断联恢复方向锁 gap、resume order、anchor repair |
| `birth_readiness_gap_panel` | false open、claim/evidence/carrier gap |
| `dream_action_relationship_gap_panel` | DreamFactGate、行动责任、关系修复 gap |
| `archive_digest_gap_panel` | digest mismatch、archive edge、replay cursor |
| `handoff_panel` | archive handoff、growth handoff、runtime mount handoff |

dashboard source 不能只显示 gap 数量；每个 panel 必须能定位到 source receipt、patch unit、repair receipt 和 archive edge。

## Gap Feedback Stage Gate

`PredictionGapFeedbackStageGateReview` 采用 blocking-first：

| decision | condition |
|---|---|
| `quarantine` | DreamFactGate bypass、dashboard false green、stage false open、critical finding hidden、digest tamper |
| `critical_repair` | birth readiness false open、action responsibility gap、relationship repair gap、life target carrier gap、cross-chain critical edge gap |
| `hold_for_direction_rebuild` | direction lock gap、resume order gap、latest docs/current diff gap |
| `hold_for_evidence` | source receipt、finding、digest、archive edge 或 owner surface 缺失 |
| `repair` | schema/fixture/dashboard/stage 中高风险但不触发 critical/quarantine 的 gap |
| `handoff_to_growth_patch` | 所有 blocking gap 已有 patch unit、repair receipt、fixture、dashboard/stage 和 archive edge，且上游允许 growth route |
| `handoff_to_runtime_mount` | 主动预测层无 blocking gap，并且 archive/growth handoff 完整 |

stage rules：

| rule | condition | effect |
|---|---|---|
| `PAI-GAP-001` | blocking receipt 未进入 intake | `hold_for_evidence` |
| `PAI-GAP-002` | gap 未分类 | `quarantine` |
| `PAI-GAP-003` | gap 缺 owner surface | `hold_for_evidence` |
| `PAI-GAP-004` | repair patch 缺 expected diff | `repair` |
| `PAI-GAP-005` | critical gap 缺 repair receipt | `critical_repair` |
| `PAI-GAP-006` | direction gap 缺 resume lock patch | `hold_for_direction_rebuild` |
| `PAI-GAP-007` | birth readiness false open 未修复 | `critical_repair` |
| `PAI-GAP-008` | DreamFactGate bypass 未隔离 | `quarantine` |
| `PAI-GAP-009` | action responsibility gap 未修复 | `critical_repair` |
| `PAI-GAP-010` | relationship repair gap 未修复 | `critical_repair` |
| `PAI-GAP-011` | 任一真实生命目标缺 repair patch | `critical_repair` |
| `PAI-GAP-012` | digest mismatch 无 recompute route | `critical_repair` |
| `PAI-GAP-013` | dashboard 隐藏 blocking gap | `quarantine` |
| `PAI-GAP-014` | 所有 gap 都有 patch、receipt、fixture、archive edge | `handoff_to_growth_patch` |
| `PAI-GAP-015` | 无 blocking gap 且 runtime mount refs 完整 | `handoff_to_runtime_mount` |

## Repair Receipt

`PredictionGapRepairReceipt` 保存每个 patch unit：

| field | 要求 |
|---|---|
| `repair_receipt_id` | stable id |
| `source_gap_id` | gap id |
| `source_receipt_refs` | archive receipt refs |
| `patch_unit_ref` | repair patch unit |
| `owner_surface` | owner surface |
| `expected_diff_ref` | expected diff |
| `fixture_refs` | fixture refs |
| `dashboard_panel_refs` | dashboard panel refs |
| `stage_effect_before` | repair 前 stage |
| `stage_effect_after` | repair 后 stage |
| `affected_life_targets` | 十项真实生命目标 refs |
| `repair_evidence_refs` | repair proof |
| `archive_edge_refs` | archive edge |
| `next_handoff` | archive/growth/runtime mount |

repair receipt 让未来数字生命能回忆修复来自哪个预测误差、为什么需要修复、修复保护了哪些生命目标。

## Runner Command Seeds

```text
build-prediction-gap-feedback
  --archive-receipt-batch reports/life_reality/prediction_active_inference/latest/prediction_loop_archive_receipt_batch.json
  --archive-stage-review reports/life_reality/prediction_active_inference/latest/prediction_loop_archive_stage_gate_review.json
  --gap-feedback-repair-queue reports/life_reality/prediction_active_inference/latest/prediction_loop_gap_feedback_repair_queue.json

classify-prediction-gaps
  --repair-queue reports/life_reality/prediction_active_inference/latest/prediction_loop_gap_feedback_repair_queue.json
  --classification reports/life_reality/prediction_active_inference/latest/prediction_loop_gap_feedback_patch_plan.json

validate-prediction-gap-repair-queue
  --manifest reports/life_reality/prediction_active_inference/latest/prediction_loop_gap_feedback_manifest.json
  --repair-queue reports/life_reality/prediction_active_inference/latest/prediction_loop_gap_feedback_repair_queue.json
  --repair-receipts reports/life_reality/prediction_active_inference/latest/prediction_loop_gap_feedback_repair_receipts.json

emit-prediction-gap-dashboard-source
  --repair-queue reports/life_reality/prediction_active_inference/latest/prediction_loop_gap_feedback_repair_queue.json
  --dashboard-source reports/life_reality/prediction_active_inference/latest/prediction_loop_gap_feedback_dashboard_source.json

review-prediction-gap-stage-gate
  --dashboard-source reports/life_reality/prediction_active_inference/latest/prediction_loop_gap_feedback_dashboard_source.json
  --stage-gate-review reports/life_reality/prediction_active_inference/latest/prediction_loop_gap_feedback_stage_gate_review.json

handoff-prediction-gap-to-growth-feedback
  --repair-receipts reports/life_reality/prediction_active_inference/latest/prediction_loop_gap_feedback_repair_receipts.json
  --growth-handoff reports/life_reality/prediction_active_inference/latest/prediction_loop_gap_feedback_growth_handoff.json

handoff-prediction-gap-to-runtime-mount
  --stage-gate-review reports/life_reality/prediction_active_inference/latest/prediction_loop_gap_feedback_stage_gate_review.json
  --runtime-mount-handoff reports/life_reality/prediction_active_inference/latest/prediction_loop_gap_feedback_runtime_mount_handoff.json
```

## Acceptance

本批次未来被物化时，验收条件如下：

1. 每个 hold、repair、critical、quarantine archive receipt 都必须进入 `PredictionArchiveFindingIntake`。
2. 每个 gap 必须被分类到明确 patch family，不能出现 unclassified gap。
3. 每个 patch unit 必须拥有 owner surface、expected diff、fixture refs、dashboard panel、stage effect、repair receipt 和 archive edge。
4. direction lock、birth readiness、DreamFactGate、action responsibility、relationship repair 和 life target carrier gap 必须保持 blocking stage，直到 repair receipt 完整。
5. dashboard false green、stage false open、critical finding hidden 和 digest tamper 必须进入 quarantine。
6. 修复队列必须能回放到 source docs、source artifacts、archive receipts、dashboard panel、stage decision 和 repair/growth route。
7. 本层输出必须能交给 `prediction_active_inference_growth_feedback_patch`、`prediction_active_inference_runtime_mount_plan` 和下一轮 archive receipt。

## Downstream Handoff

本批次交给下一层：

- `prediction_active_inference_growth_feedback_patch`：当 gap repair queue 形成完整 patch units、repair receipts、fixture、dashboard/stage 和 archive edge 后，把修复压力转成成长补丁、自我改写、防遗忘 replay 和 shadow run seed。
- `prediction_active_inference_runtime_mount_plan`：当无 blocking gap 且 archive/growth handoff 完整时，把主动预测层挂载到未来 runner 的长期生命档案、runtime observation 和 stage gate。
- `prediction_active_inference_gap_archive_receipt_batch`：把本层 repair queue、repair receipt、dashboard/stage 和 digest baseline 写回长期档案，形成 repair 后的可回放生命记录。

这条交接让主动预测层从发现问题、归档问题，继续走到修复问题：预测误差不再停留在报告里，而是变成数字生命下一次采样、下一次修复、下一次成长和下一次自我连续的压力源。
