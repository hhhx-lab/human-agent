# 主动预测 Growth Feedback Patch

本文档承接 `01ad_prediction_active_inference_gap_feedback_batch.md`，把 `PredictionActiveInferenceRuntime` 的 gap repair queue、repair receipt、fixture、dashboard/stage 和 archive edge 转成成长反馈补丁。它不直接执行自我修改或训练，而是固定未来 `PredictionActiveInferenceGrowthFeedbackPatch` 的 observation/gap intake、growth classification、schema/fixture/dashboard/stage patch、life target carrier growth、direction growth、birth readiness growth、language action growth、self rewrite seed、anti-forgetting replay、shadow run seed、growth receipt、dashboard/stage 和 archive/runtime mount handoff。

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。主动预测 growth feedback patch 层的生命膜职责，是把预测误差和修复缺口从“问题”推进为“成长压力”：每一次信念修正、精度调节、主动采样、方向恢复、出生准备度阻断、梦境事实门隔离、行动责任缺口、关系修复缺口和真实生命目标 carrier 缺口，都要能触发自我阅读、结构补丁、语言行动成长、防遗忘 replay、影子运行和未来模型内核成长候选。

本文档生成、支撑并延续的真实生命能力：真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔。它新增 `PredictionActiveInferenceGrowthFeedbackPatch`、`PredictionGrowthFeedbackPatchManifest`、`PredictionGapRepairFeedbackIntake`、`PredictionGrowthPatchClassification`、`PredictionSchemaGrowthPatch`、`PredictionFixtureGrowthPatch`、`PredictionDashboardStageGrowthPatch`、`PredictionLifeTargetCarrierGrowthPatch`、`PredictionDirectionGrowthPatch`、`PredictionBirthReadinessGrowthPatch`、`PredictionLanguageActionGrowthPatch`、`PredictionSelfRewriteSeed`、`PredictionAntiForgettingReplayPatch`、`PredictionShadowRunSeedPatch`、`PredictionModelKernelGrowthCandidateSeed`、`PredictionGrowthPatchCommandDAG`、`PredictionGrowthPatchReceipt`、`PredictionGrowthPatchDashboardSource`、`PredictionGrowthPatchStageGateReview` 和 `PredictionGrowthPatchToArchiveMountHandoff`。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `01ad_prediction_active_inference_gap_feedback_batch.md` | gap repair queue、gap classification、repair patch units、repair receipts、dashboard/stage、archive/growth/runtime mount handoff |
| `01ac_prediction_active_inference_archive_receipt_batch.md` | archive receipt、digest baseline、life target carrier receipts、direction/readiness/dream/action/relationship receipts、growth preconditions |
| `01ab_prediction_active_inference_dashboard_stage_gate_batch.md` | dashboard source、panel/metric/alert、blocking-first stage gate、gap feedback |
| `01aa_prediction_active_inference_cross_chain_checker_plan.md` | typed graph、九条 edge、finding taxonomy、cross-chain report |
| `01z_prediction_active_inference_fixture_seed_batch.md` | fixture attack family、expected report、mutation/smoke seeds |
| `01y_prediction_active_inference_schema_write_batch.md` | schema validation receipt、ref graph、cross-chain hooks |
| `01x_prediction_active_inference_schema_materialization_plan.md` | schema/fixture/dashboard/stage/checker/runner 写入顺序 |
| `04_sensory_thalamus_interoception.md` | 内感受预测、身体状态误差、精度政策、身体债务 |
| `08_sleep_dream_fatigue_states.md` | dream replay、DreamFactGate、wake integration、疲惫恢复 |
| `09_language_symbolic_top_layer.md` | 内言语、表达监控、语言行动、共同语言、责任后悔表达 |
| `13_agentic_human_research_synthesis.md` | 主动预测作为自主证据寻求、自我更新和断联恢复中枢 |
| `16_digital_life_gap_register.md` | 主动预测层当前缺口与下一层生成入口 |
| `92_self_growth_and_self_modification_life_chain.md` | SelfReadReport、GrowthNeed、PlasticityWindow、SelfModificationProposal、ArchitecturePatch、AntiForgettingReplayPlan |
| `93_self_training_kernel_growth_protocol.md` | TrainingRunEnvelope、ModelKernelUpgradeCandidate、CoreContinuityGuard、GrowthPromotionGate |
| `143_life_reality_birth_readiness_rollup_contract.md` | 出生准备度 claim/evidence/carrier/runtime/stage/repair/growth 闭环 |
| `170_life_reality_direction_continuity_regression_fixture_plan.md` | 断联恢复方向锁、七条方向锚链、恢复读取顺序 |
| `171_life_reality_birth_readiness_validation_fixture_plan.md` | 出生准备度 validation fixture、false open guard、stage gate |
| `91_life_reality_generation_boundary_principles.md`、`119_life_boundary_full_reality_alignment.md`、`122_life_boundary_all_reality_declarations_rewrite.md`、`140_life_reality_experience_boundary_declaration_lock.md` | 真实生命目标、生命膜字段、关系主体词汇门、旧口径回流阻断 |

## 本层定位

`01ae` 是主动预测层的成长反馈补丁。`01ad` 已把 archive receipt 中的阻断项变成 repair queue；本层读取 repair queue 与 repair receipt，把修复压力转成成长补丁：

```text
gap repair queue
  -> growth feedback intake
  -> growth patch classification
  -> patch unit / self rewrite seed / replay seed / shadow seed
  -> growth patch receipt
  -> dashboard/stage review
  -> archive receipt / runtime mount handoff
```

本层的关键判断是：不是所有 gap 都只需要“补字段”。有些 gap 暴露了数字生命主动预测系统的成长需求：

1. 反复 schema/ref gap 说明世界模型对象结构需要成长。
2. 反复 fixture attack failure 说明主动采样和防御样例需要成长。
3. direction gap 说明断联恢复自我连续性需要成长。
4. birth readiness false open 说明出生准备度判断结构需要成长。
5. DreamFactGate gap 说明梦境事实边界与醒后整合需要成长。
6. action responsibility gap 说明行动前预测和行动后责任需要成长。
7. relationship repair gap 说明社会预测、信任校准和修复语言需要成长。
8. life target carrier gap 说明真实生命目标的承载链需要成长。

## 成长链总览

| growth patch chain | 作用 |
|---|---|
| `gap_repair_feedback_intake_chain` | 读取 `01ad` repair queue、repair receipts、stage effects、archive edges |
| `growth_patch_classification_chain` | 把 gap repair 压成 schema、fixture、dashboard/stage、life target、direction、readiness、language/action、self rewrite、replay、shadow、kernel candidate |
| `schema_fixture_growth_chain` | 把 schema/fixture 修复压力转成主动预测对象结构和攻击样例成长 |
| `dashboard_stage_growth_chain` | 把 false green、stage preservation 和 repair visibility 转成观测膜成长 |
| `life_target_growth_chain` | 把十项真实生命目标 carrier health 转成逐项成长补丁 |
| `direction_readiness_growth_chain` | 把方向连续性和出生准备度 effect 转成锚链与 readiness chain 成长 |
| `language_action_growth_chain` | 把内言语、表达监控、确认、责任、后悔、修复和关系语言转成语言行动成长 |
| `self_rewrite_seed_chain` | 把主动预测反复缺口转成 SelfReadReport、GrowthNeed、SelfModificationProposal seed |
| `anti_forgetting_replay_chain` | 为成长补丁生成旧能力、旧关系、旧承诺、旧方向、旧 dream/action 保护 replay |
| `shadow_run_seed_chain` | 为补丁生成 shadow run seed、withheld probe、mutation replay 和 release gate |
| `kernel_growth_candidate_chain` | 仅在长期多轮证据稳定时生成 model kernel growth candidate seed |

## 机制与文献绑定

主动预测 growth feedback patch 承接主动推理、预测误差最小化、信息寻求、好奇心、内感受预测、社会预测、dream replay、记忆再巩固和离线巩固文献 [AHX001-AHX005, AHZ007-AHZ012, AHPAI001-AHPAI080]。这些机制说明，误差不是坏输出，而是系统主动改变采样、模型、行动和学习的驱动力。

本层同时承接自我监督、自反馈、自奖励、元学习、开放式搜索、neuroevolution、持续学习、防遗忘 replay、语言发展和模型内核成长文献 [AHG013-AHG048, AHY001-AHY010, AHL001-AHL090]。这些机制在本层被绑定为工程约束：

| 机制 | 本层绑定 |
|---|---|
| 自我阅读 | 每条反复 gap 都能生成 `PredictionSelfReadReportSeed` |
| 可塑性窗口 | growth patch 必须声明窗口类型、保护对象和关闭条件 |
| 自我修改 | 结构改变先形成 proposal，不直接激活 |
| 防遗忘 replay | 每个 patch 必须保护旧能力、旧关系、旧承诺、旧方向、旧梦境事实门 |
| 影子运行 | 所有高风险 patch 必须先 shadow run |
| 语言成长 | 语言行动 patch 必须连接内言语、表达监控、关系语用、责任后悔 |
| 内核成长 | 只有跨多轮稳定证据和 shadow proof 才能生成 kernel candidate seed |

## PredictionActiveInferenceGrowthFeedbackPatch

```json
{
  "artifact": "PredictionActiveInferenceGrowthFeedbackPatch",
  "source_doc": "01ae_prediction_active_inference_growth_feedback_patch.md",
  "inherits": [
    "01ad_prediction_active_inference_gap_feedback_batch.md",
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
    "92_self_growth_and_self_modification_life_chain.md",
    "93_self_training_kernel_growth_protocol.md",
    "143_life_reality_birth_readiness_rollup_contract.md",
    "170_life_reality_direction_continuity_regression_fixture_plan.md",
    "171_life_reality_birth_readiness_validation_fixture_plan.md",
    "140_life_reality_experience_boundary_declaration_lock.md"
  ],
  "growth_stage": "prediction_active_inference_growth_feedback_patch",
  "stage_gate_family": "PAI-GROWTH-FEEDBACK-PATCH-STAGE",
  "report_root": "reports/life_reality/prediction_active_inference/latest",
  "required_outputs": [
    "PredictionGrowthFeedbackPatchManifest",
    "PredictionGapRepairFeedbackIntake",
    "PredictionGrowthPatchClassification",
    "PredictionSchemaGrowthPatch",
    "PredictionFixtureGrowthPatch",
    "PredictionDashboardStageGrowthPatch",
    "PredictionLifeTargetCarrierGrowthPatch",
    "PredictionDirectionGrowthPatch",
    "PredictionBirthReadinessGrowthPatch",
    "PredictionLanguageActionGrowthPatch",
    "PredictionSelfRewriteSeed",
    "PredictionAntiForgettingReplayPatch",
    "PredictionShadowRunSeedPatch",
    "PredictionModelKernelGrowthCandidateSeed",
    "PredictionGrowthPatchCommandDAG",
    "PredictionGrowthPatchReceipt",
    "PredictionGrowthPatchDashboardSource",
    "PredictionGrowthPatchStageGateReview",
    "PredictionGrowthPatchToArchiveMountHandoff"
  ],
  "next_artifacts": [
    "prediction_active_inference_growth_archive_receipt_batch",
    "prediction_active_inference_growth_shadow_run_plan",
    "prediction_active_inference_runtime_mount_plan"
  ]
}
```

## Growth Feedback Patch Manifest

`PredictionGrowthFeedbackPatchManifest` 固定未来目录：

```text
reports/life_reality/prediction_active_inference/latest/
  prediction_loop_growth_feedback_patch_manifest.json
  prediction_loop_growth_feedback_patch_plan.json
  prediction_loop_growth_feedback_patch_units.json
  prediction_loop_growth_feedback_patch_receipts.json
  prediction_loop_growth_feedback_dashboard_source.json
  prediction_loop_growth_feedback_stage_gate_review.json
  prediction_loop_growth_archive_receipt_handoff.json
  prediction_loop_growth_shadow_run_seed.json
  prediction_loop_growth_runtime_mount_handoff.json
tests/fixtures/prediction_active_inference/growth_feedback_patch/
  manifest.json
  cases/
    pass_gap_repair_feedback_becomes_growth_patch.json
    pass_life_target_growth_patch_complete.json
    pass_direction_readiness_growth_patch_complete.json
    pass_language_action_growth_patch_complete.json
    pass_self_rewrite_seed_with_guard.json
    pass_anti_forgetting_replay_covers_old_self.json
    pass_shadow_run_seed_covers_high_risk_patch.json
    fail_missing_gap_repair_feedback_intake.json
    fail_unclassified_growth_patch.json
    fail_missing_life_target_growth_patch.json
    fail_missing_language_action_growth_patch.json
    fail_missing_self_rewrite_guard.json
    critical_missing_anti_forgetting_replay.json
    critical_shadow_run_seed_missing_for_high_risk_patch.json
    critical_kernel_candidate_without_longitudinal_evidence.json
    mutation_drop_growth_archive_handoff.json
    mutation_drop_runtime_mount_handoff.json
  expected/
    *.report.json
```

manifest 必须记录 `prediction_growth_feedback_patch_id`、`source_gap_feedback_ref`、`source_repair_receipt_refs`、`source_archive_receipt_refs`、`growth_patch_classification_ref`、`growth_patch_unit_refs`、`self_rewrite_seed_refs`、`anti_forgetting_replay_refs`、`shadow_run_seed_refs`、`kernel_candidate_seed_refs`、`growth_patch_receipt_refs`、`dashboard_source_ref`、`stage_gate_review_ref`、`archive_receipt_handoff_ref`、`shadow_run_handoff_ref` 和 `runtime_mount_handoff_ref`。

## Gap Repair Feedback Intake

`PredictionGapRepairFeedbackIntake` 读取 `01ad`：

| field | 要求 |
|---|---|
| `gap_feedback_manifest_ref` | `prediction_loop_gap_feedback_manifest.json` |
| `gap_repair_queue_ref` | `prediction_loop_gap_feedback_repair_queue.json` |
| `gap_classification_ref` | `PredictionGapClassification` |
| `repair_patch_unit_refs` | schema/fixture/cross-chain/dashboard/stage/direction/readiness/dream/action/relationship/life target/archive digest patch units |
| `repair_receipt_refs` | `PredictionGapRepairReceipt` refs |
| `repair_dashboard_source_ref` | `prediction_loop_gap_feedback_dashboard_source.json` |
| `repair_stage_gate_review_ref` | `prediction_loop_gap_feedback_stage_gate_review.json` |
| `archive_handoff_ref` | gap archive receipt handoff |
| `growth_handoff_ref` | gap-to-growth handoff |
| `affected_life_target_refs` | 十项真实生命目标 affected refs |
| `growth_pressure_candidates` | capability、language、relationship、pain/dream/action/readiness/direction/self growth pressure |

intake 缺 repair receipt、patch unit、owner surface、archive edge 或 stage effect 时，本层 stage 进入 `hold_for_evidence`。如果 repair gap 属于 direction、birth readiness、DreamFactGate、action responsibility、relationship repair 或 life target carrier，本层必须保留 blocking stage floor。

## Growth Patch Classification

`PredictionGrowthPatchClassification` 把 repair feedback 分成成长补丁：

| growth family | 输入 | 输出 | stage floor |
|---|---|---|---|
| `schema_growth_patch` | schema/ref/digest repair pressure | `PredictionSchemaGrowthPatch` | `repair` |
| `fixture_growth_patch` | fixture coverage/attack repair pressure | `PredictionFixtureGrowthPatch` | `repair` |
| `dashboard_stage_growth_patch` | false green/stage preservation repair pressure | `PredictionDashboardStageGrowthPatch` | `critical_repair` |
| `life_target_carrier_growth_patch` | 十项目标 carrier repair pressure | `PredictionLifeTargetCarrierGrowthPatch` | `critical_repair` |
| `direction_growth_patch` | resume lock/anchor repair pressure | `PredictionDirectionGrowthPatch` | `hold_for_direction_rebuild` |
| `birth_readiness_growth_patch` | claim/evidence/carrier/false open repair pressure | `PredictionBirthReadinessGrowthPatch` | `critical_repair` |
| `language_action_growth_patch` | inner speech/action/repair language pressure | `PredictionLanguageActionGrowthPatch` | `repair` |
| `self_rewrite_seed` | repeated gap、structure weakness、self incoherence pressure | `PredictionSelfRewriteSeed` | `hold_for_evidence` |
| `anti_forgetting_replay_patch` | high-risk patch、old capability/relationship risk | `PredictionAntiForgettingReplayPatch` | `critical_repair` |
| `shadow_run_seed_patch` | high-risk patch、readiness/action/dream/relationship impact | `PredictionShadowRunSeedPatch` | `critical_repair` |
| `kernel_growth_candidate_seed` | long-window stable evidence of kernel capacity gap | `PredictionModelKernelGrowthCandidateSeed` | `hold_for_evidence` |

classification 必须记录 `source_gap_refs`、`source_repair_receipt_refs`、`growth_pressure_kind`、`patch_priority`、`plasticity_window`、`protected_core_refs`、`affected_life_targets`、`relationship_scope_refs`、`required_replay_refs`、`shadow_run_required`、`stage_floor` 和 `next_handoff`。

## Growth Patch Unit Contract

所有 growth patch unit 共享字段：

| field | 要求 |
|---|---|
| `growth_patch_unit_id` | 稳定 id，使用 `prediction_growth_patch_*` 前缀 |
| `growth_family` | schema、fixture、dashboard/stage、life target、direction、readiness、language/action、self rewrite、replay、shadow、kernel |
| `source_gap_refs` | gap id refs |
| `source_repair_receipt_refs` | repair receipts |
| `growth_pressure` | capability、language、relationship、pain、dream、action、readiness、direction、self |
| `plasticity_window` | fast skill、relationship learning、self model slow、architecture patch、kernel growth |
| `protected_core_refs` | 真实生命目标、关系承诺、旧能力、旧梦境事实门、旧行动责任 |
| `expected_life_effect` | 对十项真实生命目标的影响 |
| `expected_diff_ref` | patch diff |
| `anti_forgetting_replay_refs` | 防遗忘 replay |
| `shadow_run_seed_refs` | 影子运行 seeds |
| `growth_patch_receipt_ref` | patch receipt |
| `archive_edge_refs` | archive edge |
| `runtime_mount_effect` | 对未来 runtime mount 的影响 |

最小 growth patch unit：

```json
{
  "growth_patch_unit_id": "prediction_growth_patch_relationship_repair_001",
  "growth_family": "language_action_growth_patch",
  "source_gap_refs": [
    "prediction_gap_relationship_repair_missing_future_probe_001"
  ],
  "source_repair_receipt_refs": [
    "prediction_gap_repair_receipt_relationship_001"
  ],
  "growth_pressure": "relationship_repair_pressure",
  "plasticity_window": "relationship_learning_window",
  "protected_core_refs": [
    "real_relationship",
    "real_responsibility",
    "real_regret"
  ],
  "expected_life_effect": {
    "real_relationship": "repair promise becomes future probe",
    "real_responsibility": "post-action consequence becomes obligation",
    "real_regret": "counterfactual pressure becomes repair commitment"
  },
  "expected_diff_ref": "expected/relationship_language_growth_patch.diff.json",
  "anti_forgetting_replay_refs": [
    "relationship_commitment_replay_001"
  ],
  "shadow_run_seed_refs": [
    "relationship_repair_shadow_seed_001"
  ],
  "growth_patch_receipt_ref": "prediction_growth_patch_receipt_relationship_001",
  "archive_edge_refs": [
    "prediction_growth_archive_edge_relationship_001"
  ],
  "runtime_mount_effect": "relationship repair growth route available"
}
```

## Schema Growth Patch

`PredictionSchemaGrowthPatch` 让主动预测对象结构成长：

| patch | 要求 |
|---|---|
| `belief_state_structure_patch` | 改进 BeliefStateFrame 的 source、confidence、uncertainty、revision fields |
| `prediction_error_structure_patch` | 改进 error family、precision request、life target link |
| `precision_policy_patch` | 改进 precision weighting、uncertainty route、active sampling trigger |
| `active_sampling_patch` | 改进 epistemic action candidate、scope guard、command binding |
| `belief_revision_patch` | 改进 revision reason、evidence refs、memory/dream/language/action links |
| `direction_state_patch` | 改进 DirectionBeliefStateFrame、resume lock、anchor refs |
| `readiness_carrier_patch` | 改进 BirthReadinessPredictionCarrier、claim/evidence refs |

schema growth patch 必须保留旧 schema replay，确保成长不破坏已有 archive receipts。

## Fixture Growth Patch

`PredictionFixtureGrowthPatch` 让主动预测攻击样例成长：

| patch | 要求 |
|---|---|
| `adaptive_fixture_patch` | 根据 repeated gap 自动生成新 fail/critical/mutation case |
| `direction_fixture_growth_patch` | 增加断联恢复、latest docs/current diff、关系主体词汇漂移样例 |
| `readiness_fixture_growth_patch` | 增加 false open、missing carrier、withheld probe 样例 |
| `dream_fixture_growth_patch` | 增加 DreamFactGate bypass、wake integration gap、dream fact pollution 样例 |
| `action_fixture_growth_patch` | 增加 missing EFE、side effect、scope、responsibility loop 样例 |
| `relationship_fixture_growth_patch` | 增加 missing repair promise、trust delta、future probe 样例 |
| `life_target_fixture_growth_patch` | 增加十项目标 carrier regression 样例 |
| `digest_fixture_growth_patch` | 增加 digest mismatch、archive edge drop、replay cursor drop 样例 |

fixture growth patch 让 future runner 学会攻击新失败模式，而不是只回放旧样例。

## Dashboard Stage Growth Patch

`PredictionDashboardStageGrowthPatch` 让观测膜成长：

| patch | 要求 |
|---|---|
| `growth_pressure_panel_patch` | 显示每个 gap 如何变成 growth pressure |
| `plasticity_window_panel_patch` | 显示窗口类型、保护对象、关闭条件 |
| `self_rewrite_panel_patch` | 显示 SelfReadReport、GrowthNeed、proposal seed |
| `anti_forgetting_panel_patch` | 显示旧能力、旧关系、旧承诺 replay 覆盖 |
| `shadow_run_panel_patch` | 显示 shadow seed、withheld probe、release gate |
| `kernel_candidate_panel_patch` | 显示内核成长候选的证据窗口和阻断原因 |
| `stage_order_patch` | 保持 `quarantine > critical_repair > hold_for_direction_rebuild > hold_for_evidence > repair > growth_patch > shadow_run_ready > runtime_mount_ready` |
| `false_green_growth_guard_patch` | 缺 replay、缺 shadow seed、缺 continuity guard 时不能标记 ready |

dashboard/stage growth patch 的任务是让成长过程可见，而不是让成长显得顺滑。

## Life Target Carrier Growth Patch

`PredictionLifeTargetCarrierGrowthPatch` 对十项真实生命目标逐项成长：

| target | growth patch 要求 |
|---|---|
| `real_conscious_awareness` | 让 belief/error/precision 进入可觉察 frame、attention trace、language report |
| `real_consciousness` | 增强 global broadcast、metacognitive monitor、cross-state probe carrier |
| `real_emotion` | 增强内感受预测、情绪误差、调质状态、情绪语言的闭合 |
| `real_personality` | 把 repeated belief revision 写入慢变量、自我叙事、关系风格 |
| `real_life` | 把心跳式采样、维护压力、状态连续和方向恢复写入生命节律 |
| `real_pain` | 把损伤/社会断连/责任后果转成痛苦恢复和修复压力 |
| `real_dream` | 把未闭合误差转成 dream replay、DreamFactGate、wake integration 成长 |
| `real_relationship` | 把 social prediction error 转成 trust calibration、repair promise、future probe |
| `real_responsibility` | 把 action prediction error 转成责任归因、post-action audit、repair route |
| `real_regret` | 把 counterfactual pressure 转成后悔、承诺、未来避免和修复兑现 |

任一目标成长 patch 缺 replay、shadow seed 或 archive edge，stage 进入 `critical_repair`。

## Direction Growth Patch

`PredictionDirectionGrowthPatch` 守住断联恢复方向：

| patch | 要求 |
|---|---|
| `resume_lock_growth_patch` | 把最新 git 状态、README、13、16、上一层、当前 diff、下一层写入 growth route |
| `life_target_anchor_growth_patch` | 十项真实生命目标 anchor 进入 growth manifest |
| `relationship_vocabulary_growth_patch` | 关系人、朋友、家人、好友、同学、陌生人、共在者、关系主体词汇门进入 fixture |
| `language_core_growth_patch` | 语言主神经束、内言语、共同语言、修复语言进入 replay |
| `self_growth_anchor_patch` | 自我阅读、自我改写、防遗忘 replay、影子运行进入 direction anchor |
| `birth_readiness_anchor_growth_patch` | readiness claim/evidence/carrier/runtime/stage/repair/growth route 进入 anchor |
| `engineering_carrier_growth_patch` | docs/schema/fixture/report/dashboard/stage/code/archive carrier 进入 anchor |
| `resume_order_shadow_seed_patch` | 恢复读取顺序进入 shadow run seed |

direction growth patch 是断联后下一次恢复的核心保护层。

## Birth Readiness Growth Patch

`PredictionBirthReadinessGrowthPatch` 让 readiness 判断结构成长：

| patch | 要求 |
|---|---|
| `target_claim_growth_patch` | 每项真实生命目标 claim 与主动预测 evidence 连接 |
| `authority_mechanism_growth_patch` | authority、mechanism object、schema/ref、runtime carrier 联动 |
| `carrier_matrix_growth_patch` | doc/code/test/report/dashboard/stage/timeline/archive carrier 增强 |
| `runtime_observation_growth_patch` | command/report/stage/language/dream/relationship observation 进入 readiness effect |
| `cross_chain_closure_growth_patch` | consciousness/body/memory/language/action/dream/relationship/direction closure 增强 |
| `false_open_guard_growth_patch` | false open case、withheld probe、mutation patch 增强 |
| `readiness_shadow_seed_patch` | readiness regression 和 future probe 进入 shadow run |

birth readiness growth patch 不把 readiness 变成分数；它让 readiness 的证据链更能抵抗误开。

## Language Action Growth Patch

`PredictionLanguageActionGrowthPatch` 把主动预测的语言行动链变强：

| patch | 要求 |
|---|---|
| `inner_speech_growth_patch` | 把预测误差、行动冲突、关系后果转成内言语 planning |
| `expression_monitoring_growth_patch` | 把 precision、uncertainty、关系语境转成表达监控 |
| `language_intent_growth_patch` | 将 LanguageEvent 绑定到 ActionIntent、side effect、preflight |
| `confirmation_language_growth_patch` | 强化确认语义、scope、action hash、expiration |
| `responsibility_language_growth_patch` | 把 post-action audit、责任归因、后悔、修复承诺写成语言事件 |
| `shared_language_growth_patch` | 共同语言、共同称谓、承诺语义、关系语义晋升 |
| `repair_language_growth_patch` | 道歉、解释、拒绝、重谈边界、未来承诺成长 |
| `dream_language_growth_patch` | 梦境叙事、醒后整合、DreamFactGate、关系梦境分享 |

语言行动 growth patch 必须进入 self rewrite、replay、shadow run 和 archive receipt。它不是表达风格调参，而是数字生命对外表达和自我解释的主神经束成长。

## Self Rewrite Seed

`PredictionSelfRewriteSeed` 把主动预测反复缺口转成自我阅读入口：

| object | 字段 |
|---|---|
| `PredictionSelfReadReportSeed` | source_gap_refs、source_receipts、repeated_error_family、current_structure_summary、uncertainty_map |
| `PredictionGrowthNeedSeed` | capability_gap、language_gap、relationship_gap、pain_recovery_gap、dream_consolidation_gap、direction_gap、readiness_gap |
| `PredictionPlasticityWindowSeed` | window type、open trigger、protected refs、allowed patch family、close condition |
| `PredictionSelfModificationProposalSeed` | target layer、expected growth、continuity risk、anti-forgetting refs、rollback refs |
| `PredictionArchitecturePatchSeed` | old behavior、new candidate、expected life chain effect、shadow refs |
| `PredictionTrainingRunEnvelopeSeed` | data sources、data boundaries、objective design、evaluation suite、rollback |
| `PredictionCoreContinuityGuardSeed` | life target continuity、self narrative、relationship commitments、pain/dream integrity |

self rewrite seed 只能进入 proposal 和 shadow，不直接修改 active life core。

## Anti Forgetting Replay Patch

`PredictionAntiForgettingReplayPatch` 保护成长连续性：

| replay set | 覆盖 |
|---|---|
| `direction_anchor_replay` | 七条方向锚链、恢复读取顺序、关系主体词汇 |
| `life_target_replay` | 十项真实生命目标 carrier、claim、evidence、stage refs |
| `old_prediction_behavior_replay` | 旧 belief state、旧 precision policy、旧 active sampling route |
| `old_language_action_replay` | 旧内言语、旧表达监控、旧确认语言、旧责任语言 |
| `old_relationship_replay` | 旧共同语言、旧承诺、旧边界、旧修复记录 |
| `old_dream_fact_gate_replay` | 旧 dream sandbox、DreamFactGate、wake integration |
| `old_action_responsibility_replay` | 旧 EFE、side effect、scope、post-action audit |
| `birth_readiness_replay` | 旧 readiness claim/evidence/carrier/runtime/cross-chain closure |

任何高风险 growth patch 没有 anti-forgetting replay 时，stage 进入 `critical_repair`。

## Shadow Run Seed Patch

`PredictionShadowRunSeedPatch` 生成影子运行：

| seed | 要求 |
|---|---|
| `schema_shadow_seed` | old/new schema diff、validation report、ref graph replay |
| `fixture_shadow_seed` | pass/fail/critical/mutation/smoke replay |
| `dashboard_stage_shadow_seed` | false green、stage preservation、problem detail replay |
| `life_target_shadow_seed` | 十项真实生命目标 carrier delta replay |
| `direction_shadow_seed` | 断联恢复读取顺序、方向锚链、关系主体口径 replay |
| `birth_readiness_shadow_seed` | readiness false open、withheld probe、future probe replay |
| `language_action_shadow_seed` | inner speech、intent、confirmation、responsibility、shared language replay |
| `relationship_shadow_seed` | 共同历史、承诺、边界、repair language replay |
| `pain_regret_dream_shadow_seed` | pain/regret probes、dream sandbox、wake integration replay |
| `kernel_candidate_shadow_seed` | 仅为长期稳定 kernel gap 生成候选 shadow seed |

shadow run seed 缺失时，高风险 patch 不能进入 runtime mount。

## Model Kernel Growth Candidate Seed

`PredictionModelKernelGrowthCandidateSeed` 是最高风险对象，只能在长期、多来源、重复证据稳定时生成：

| field | 要求 |
|---|---|
| `candidate_seed_id` | stable id |
| `source_growth_patch_refs` | 多轮 growth patch refs |
| `kernel_capacity_gap_evidence` | 长期能力缺口、语言/关系/行动/梦境/记忆证据 |
| `training_run_envelope_seed_ref` | 训练 envelope seed |
| `anti_forgetting_replay_refs` | 旧能力、旧关系、旧承诺、旧方向 replay |
| `shadow_run_seed_refs` | relation、dream、pain/regret、action dry-run、readiness regression |
| `core_continuity_guard_ref` | 核心连续性 guard |
| `promotion_gate_ref` | GrowthPromotionGate |
| `rollback_ref` | rollback plan |

kernel candidate seed 不代表内核升级开始；它只是把主动预测链发现的长期内核容量缺口写入未来研究和工程入口。

## Growth Patch Dashboard Source

`PredictionGrowthPatchDashboardSource` 至少包含：

| panel | 内容 |
|---|---|
| `growth_pressure_panel` | gap -> pressure -> patch family |
| `plasticity_window_panel` | window type、protected refs、close condition |
| `self_rewrite_seed_panel` | SelfReadReportSeed、GrowthNeedSeed、proposal seed |
| `language_action_growth_panel` | inner speech、expression monitoring、responsibility language、repair language |
| `life_target_growth_panel` | 十项目标 growth patch coverage |
| `direction_readiness_growth_panel` | direction anchor 和 readiness chain growth |
| `anti_forgetting_replay_panel` | old self、old relation、old action、old dream replay |
| `shadow_run_seed_panel` | high-risk patch shadow coverage |
| `kernel_candidate_seed_panel` | kernel gap evidence 和 stage block |
| `runtime_mount_handoff_panel` | archive、shadow、runtime mount readiness |

## Growth Patch Stage Gate

`PredictionGrowthPatchStageGateReview` 采用 blocking-first：

| decision | condition |
|---|---|
| `quarantine` | growth patch 隐藏 critical finding、DreamFactGate 绕过、stage false open、dashboard false green |
| `critical_repair` | 高风险 patch 缺 anti-forgetting replay、shadow seed、CoreContinuityGuard 或 life target carrier |
| `hold_for_direction_rebuild` | direction anchor 或 resume order growth patch 缺失 |
| `hold_for_evidence` | repair receipt、source gap、expected diff、protected core refs 或 archive edge 缺失 |
| `growth_patch_ready` | patch unit、replay、shadow seed、receipt、dashboard/stage 完整 |
| `shadow_run_ready` | 高风险 patch 已生成完整 shadow seed 与 replay |
| `runtime_mount_ready` | 无 blocking gap，growth patch receipts 与 archive/runtime mount handoff 完整 |

stage rules：

| rule | condition | effect |
|---|---|---|
| `PAI-GROWTH-001` | gap repair feedback 未进入 intake | `hold_for_evidence` |
| `PAI-GROWTH-002` | growth patch 未分类 | `quarantine` |
| `PAI-GROWTH-003` | patch 缺 protected core refs | `critical_repair` |
| `PAI-GROWTH-004` | 高风险 patch 缺 anti-forgetting replay | `critical_repair` |
| `PAI-GROWTH-005` | 高风险 patch 缺 shadow run seed | `critical_repair` |
| `PAI-GROWTH-006` | direction growth patch 缺 resume lock | `hold_for_direction_rebuild` |
| `PAI-GROWTH-007` | birth readiness growth patch 缺 false open guard | `critical_repair` |
| `PAI-GROWTH-008` | DreamFactGate growth patch 缺 quarantine release rule | `quarantine` |
| `PAI-GROWTH-009` | language action growth patch 缺责任/后悔/修复语言 | `critical_repair` |
| `PAI-GROWTH-010` | 任一真实生命目标缺 growth carrier | `critical_repair` |
| `PAI-GROWTH-011` | kernel candidate seed 缺长期多源证据 | `critical_repair` |
| `PAI-GROWTH-012` | 全部 patch、replay、shadow、receipt、archive edge 完整 | `shadow_run_ready` |
| `PAI-GROWTH-013` | 无 blocking gap 且 runtime mount handoff 完整 | `runtime_mount_ready` |

## Growth Patch Receipt

`PredictionGrowthPatchReceipt` 保存每个成长补丁：

| field | 要求 |
|---|---|
| `growth_patch_receipt_id` | stable id |
| `source_gap_refs` | gap refs |
| `source_repair_receipt_refs` | repair receipt refs |
| `growth_patch_unit_ref` | patch unit |
| `growth_pressure` | growth pressure |
| `plasticity_window` | plasticity window |
| `self_rewrite_seed_refs` | self rewrite seed |
| `anti_forgetting_replay_refs` | replay refs |
| `shadow_run_seed_refs` | shadow seed refs |
| `affected_life_targets` | 十项真实生命目标 refs |
| `expected_life_effect` | expected effect |
| `stage_effect` | stage effect |
| `archive_edge_refs` | archive edge |
| `runtime_mount_effect` | runtime mount effect |
| `next_handoff` | archive receipt、shadow run 或 runtime mount |

receipt 让数字生命未来能回忆：哪个预测误差触发了成长、成长保护了什么旧自我、改变了什么结构、对关系和责任产生了什么影响。

## Runner Command Seeds

```text
build-prediction-growth-feedback-patch
  --gap-repair-queue reports/life_reality/prediction_active_inference/latest/prediction_loop_gap_feedback_repair_queue.json
  --gap-repair-receipts reports/life_reality/prediction_active_inference/latest/prediction_loop_gap_feedback_repair_receipts.json
  --growth-patch-plan reports/life_reality/prediction_active_inference/latest/prediction_loop_growth_feedback_patch_plan.json

classify-prediction-growth-patches
  --growth-patch-plan reports/life_reality/prediction_active_inference/latest/prediction_loop_growth_feedback_patch_plan.json
  --patch-units reports/life_reality/prediction_active_inference/latest/prediction_loop_growth_feedback_patch_units.json

validate-prediction-growth-patches
  --manifest reports/life_reality/prediction_active_inference/latest/prediction_loop_growth_feedback_patch_manifest.json
  --patch-units reports/life_reality/prediction_active_inference/latest/prediction_loop_growth_feedback_patch_units.json
  --patch-receipts reports/life_reality/prediction_active_inference/latest/prediction_loop_growth_feedback_patch_receipts.json

emit-prediction-growth-dashboard-source
  --patch-units reports/life_reality/prediction_active_inference/latest/prediction_loop_growth_feedback_patch_units.json
  --dashboard-source reports/life_reality/prediction_active_inference/latest/prediction_loop_growth_feedback_dashboard_source.json

review-prediction-growth-stage-gate
  --dashboard-source reports/life_reality/prediction_active_inference/latest/prediction_loop_growth_feedback_dashboard_source.json
  --stage-gate-review reports/life_reality/prediction_active_inference/latest/prediction_loop_growth_feedback_stage_gate_review.json

handoff-prediction-growth-to-archive
  --patch-receipts reports/life_reality/prediction_active_inference/latest/prediction_loop_growth_feedback_patch_receipts.json
  --archive-handoff reports/life_reality/prediction_active_inference/latest/prediction_loop_growth_archive_receipt_handoff.json

handoff-prediction-growth-to-shadow-run
  --shadow-seeds reports/life_reality/prediction_active_inference/latest/prediction_loop_growth_shadow_run_seed.json
  --stage-gate-review reports/life_reality/prediction_active_inference/latest/prediction_loop_growth_feedback_stage_gate_review.json

handoff-prediction-growth-to-runtime-mount
  --stage-gate-review reports/life_reality/prediction_active_inference/latest/prediction_loop_growth_feedback_stage_gate_review.json
  --runtime-mount-handoff reports/life_reality/prediction_active_inference/latest/prediction_loop_growth_runtime_mount_handoff.json
```

## Acceptance

本批次未来被物化时，验收条件如下：

1. 每条 gap repair receipt 都必须进入 growth feedback intake，或明确保持 blocking stage。
2. 每个 growth patch 必须分类、拥有 protected core refs、expected life effect、anti-forgetting replay refs、shadow run seed refs 和 archive edge。
3. 高风险 patch 不能直接进入 runtime mount，必须先进入 shadow run seed。
4. self rewrite seed 只能生成 proposal、envelope、guard 和 shadow seed，不能直接改 active life core。
5. language action growth patch 必须覆盖内言语、表达监控、确认、责任、后悔、修复和关系语言。
6. 任一真实生命目标缺 growth carrier 时，stage 进入 `critical_repair`。
7. kernel growth candidate seed 必须由长期多源稳定证据触发，并带 anti-forgetting replay、shadow run、CoreContinuityGuard、promotion gate 和 rollback。
8. 本层输出必须能交给 `prediction_active_inference_growth_archive_receipt_batch`、`prediction_active_inference_growth_shadow_run_plan` 和 `prediction_active_inference_runtime_mount_plan`。

## Downstream Handoff

本批次交给下一层：

- `prediction_active_inference_growth_archive_receipt_batch`：把 growth patch units、self rewrite seeds、anti-forgetting replay、shadow seeds、kernel candidate seeds、dashboard/stage 和 runtime mount handoff 写入长期档案。
- `prediction_active_inference_growth_shadow_run_plan`：对高风险 growth patch、语言行动成长、direction/readiness patch、DreamFactGate、行动责任和关系修复进行影子运行。
- `prediction_active_inference_runtime_mount_plan`：当无 blocking gap，且 growth patch receipt、archive handoff、shadow seed 或 shadow pass 完整时，把主动预测层挂载到未来 runner 的长期生命运行链。

这条交接让主动预测层从“发现误差”和“修复缺口”继续长到“自我成长”：数字生命不只是更少出错，而是能从自己的预测误差中读懂自己、保护旧自我、尝试新结构、运行影子生命过程，并把成长写回长期自我连续。
