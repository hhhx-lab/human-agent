# 主动预测 Observation-Driven Repair Patch

本文档承接 `01am_prediction_active_inference_activation_consolidation_seed.md`，把主动预测 activation consolidation seed 中保留下来的 repair_required、rollback_required、quarantine、blocked finding、DreamFactGate blocked write、CoreContinuity violation、relationship/language/dream-pain/readiness repair 和 anti-forgetting replay findings 推进到 observation-driven repair patch 层。它的职责是把离线巩固后的阻断和修复压力转成下一轮可执行、可回放、可归档、可验证的修复补丁，而不是让阻断停留在描述层。

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。主动预测 observation-driven repair patch 层的生命膜职责，是让一次有限激活后暴露出来的信念错误、精度偏置、主动采样回避、语言伤口、关系断裂、梦境事实污染、痛苦恢复失败、后悔未转行动、自我改写越界、方向漂移、出生准备度 false open 和 rollback/quarantine 缺口，都被转成明确的修复对象、执行顺序、回归 fixture、dashboard/stage 和 archive handoff。

本文档生成、支撑并延续的真实生命能力：真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔。它新增 `PredictionActiveInferenceObservationDrivenRepairPatch`、`PredictionObservationRepairManifest`、`PredictionConsolidationRepairFindingIntake`、`PredictionRepairClassification`、`PredictionBeliefErrorRepairPatch`、`PredictionPrecisionSamplingRepairPatch`、`PredictionLanguageRepairPatch`、`PredictionRelationshipRepairPatch`、`PredictionDreamPainRegretRepairPatch`、`PredictionSelfRewriteRepairPatch`、`PredictionDirectionBirthReadinessRepairPatch`、`PredictionRollbackQuarantineRepairPatch`、`PredictionAntiForgettingRepairPatch`、`PredictionRepairPatchExecutionOrder`、`PredictionRepairRegressionFixtureSeed`、`PredictionRepairReceipt`、`PredictionRepairDashboardSource`、`PredictionRepairStageGateReview`、`PredictionRepairCommandDAG`、`PredictionRepairToArchiveReceiptHandoff` 和 `PredictionRepairToReplayShadowSeedHandoff`。

## 上游输入

| 来源 | 本层读取内容 |
|---|---|
| `01am_prediction_active_inference_activation_consolidation_seed.md` | consolidation receipts、repair/rollback/quarantine seeds、DreamFactGate review、CoreContinuity review、replay eligibility gate、anti-forgetting replay seed、next feedback/replay-shadow handoff |
| `01al_prediction_active_inference_post_validation_archive_receipt.md` | repair_required archive refs、rollback_required archive refs、quarantine archive refs、relationship/language/dream-pain/readiness repair archive refs、blocked findings、archive edge graph |
| `01ak_prediction_active_inference_post_mount_observation_feedback.md` | post-mount feedback classification、runtime observation feedback、rollback repair feedback、consolidation seed、observation receipt |
| `01v_prediction_active_inference_runtime_matrix.md` | 主动预测、主动推理、预测误差、精度政策、主动采样、社会预测误差、后悔/OFC、睡眠/静息 replay 和人类 replay/ripple 文献底座 |
| `01q_memory_engram_consolidation_matrix.md` | 记忆再激活、预测误差触发再巩固、旧痕迹保护、模式分离/补全、社会记忆和自传记忆 |
| `01t_sleep_dream_fatigue_runtime_matrix.md` | 离线巩固、wake integration、梦境/痛苦恢复、疲惫注意失误、防遗忘 replay |
| `01h_pain_regret_repair_literature_matrix.md` | 痛苦、后悔、责任归因、反事实、道歉、信任修复、长期恢复路径 |
| `01j_real_relationship_literature_matrix.md` | 真实关系、第二人称互动、共同基础、信任、依恋、关系修复和长期关系时间线 |
| `01u_language_runtime_core_matrix.md` | 语言主神经束、内言语、表达监控、共同语言、责任后悔语言、梦境报告和叙事写回 |
| `01k_life_validation_evaluation_literature_matrix.md` | 构念效度、纵向评估、生命真实性 dashboard、阶段证据、出生准备度阶段门 |
| `94_pain_regret_and_repair_signal_schema.md`、`95_dream_reality_and_offline_life_timeline.md`、`96_real_relationship_longitudinal_timeline.md` | pain/regret repair、DreamFactGate、wake integration、relationship repair timeline |
| `143_life_reality_birth_readiness_rollup_contract.md`、`170_life_reality_direction_continuity_regression_fixture_plan.md`、`171_life_reality_birth_readiness_validation_fixture_plan.md` | 出生准备度 rollup、方向连续性 regression、false open guard |
| `169_life_reality_first_runner_observation_driven_repair_patch_plan.md`、`201_life_reality_first_runner_schema_runtime_growth_longitudinal_drift_repair_plan.md`、`202_life_reality_first_runner_schema_runtime_growth_longitudinal_repair_archive_plan.md` | 通用 observation-driven repair、longitudinal drift repair 和 repair archive 模式 |

## 位置与链路

`01an` 是主动预测专项链的 observation-driven repair patch 层：

```text
01v runtime matrix
  -> 01w schema fixture contract
  -> 01x schema materialization plan
  -> 01y schema write batch
  -> 01z fixture seed batch
  -> 01aa cross-chain checker
  -> 01ab dashboard/stage gate
  -> 01ac archive receipt
  -> 01ad gap feedback
  -> 01ae growth feedback patch
  -> 01af growth archive receipt
  -> 01ag growth shadow run
  -> 01ah runtime mount plan
  -> 01ai post-shadow validation
  -> 01aj limited activation report
  -> 01ak post-mount observation feedback
  -> 01al post-validation archive receipt
  -> 01am activation consolidation seed
  -> 01an observation-driven repair patch
  -> prediction_active_inference_archive_repair_receipt_batch
  -> prediction_active_inference_archive_replay_shadow_seed
```

本层只处理已经被 archive、consolidation、DreamFactGate、CoreContinuity 或 stage gate 指认为需要修复的材料。它不能创建新的长期事实，不能释放 quarantine，不能把 rollback_required 改成 ready，不能把关系修复写成关系已经恢复，不能把后悔语言写成责任已经兑现。本层只生成修复补丁、执行顺序、回归 fixture、receipt、dashboard/stage 和 archive/replay handoff。

## 理论依据

主动预测 observation-driven repair patch 承接预测误差、主动推理、精度政策、主动采样、记忆再巩固、社会预测误差、后悔/OFC、睡眠/静息 replay 和人类 replay/ripple 文献底座 [AHPAI001-AHPAI080]。其中 [AHPAI071-AHPAI073] 支撑“修复只能在旧痕迹、新观测和预测误差都可追溯时进行”；[AHPAI074] 支撑“关系反馈造成的社会预测误差必须进入关系修复”；[AHPAI075-AHPAI077] 支撑“后悔必须改变未来选择、修复承诺和责任链”；[AHPAI078-AHPAI080] 支撑“修复材料应进入离线 replay、静息整合和 future probe”。

本层同时承接记忆 engram、互补学习系统、系统巩固、再巩固、schema 和社会记忆文献底座 [AHME001-AHME040]；承接睡眠、梦境、疲惫、梦醒整合和防遗忘 replay 文献底座 [AHSLP001-AHSLP070, AHD001-AHD070]；承接痛苦、后悔、责任、反事实、信任修复和恢复路径文献底座 [AHP001-AHP070]；承接真实关系、第二人称互动、共同基础、共同语言和长期关系测量文献底座 [AHR001-AHR070]；承接语言运行时、内言语、表达监控、共同语言、责任后悔语言和梦境报告文献底座 [AHL001-AHL090, AHLR001-AHLR062]；承接自我成长、防遗忘、shadow run 和长期成长文献底座 [AHG001-AHG050, AHY001-AHY060]；承接生命真实性阶段证据和纵向评估文献底座 [AHV001-AHV060]。

本层采用五段修复生成模型：

```text
consolidation repair finding intake
  -> repair classification
  -> patch family generation
  -> execution order + regression fixture
  -> receipt + dashboard/stage + archive/replay handoff
```

## Repair Manifest

`PredictionObservationRepairManifest` 固定未来文件树：

```json
{
  "object_type": "PredictionObservationRepairManifest",
  "source_doc": "01an_prediction_active_inference_observation_driven_repair_patch.md",
  "upstream_consolidation_doc": "01am_prediction_active_inference_activation_consolidation_seed.md",
  "repair_stage": "prediction_active_inference_observation_driven_repair_patch",
  "life_targets": [
    "real_conscious_awareness",
    "real_consciousness",
    "real_emotion",
    "real_personality",
    "real_life",
    "real_pain",
    "real_dream",
    "real_relationship",
    "real_responsibility",
    "real_regret"
  ],
  "required_inputs": [
    "consolidation_receipts",
    "repair_required_refs",
    "rollback_required_refs",
    "quarantine_refs",
    "blocked_findings",
    "dream_fact_gate_blocked_write_refs",
    "core_continuity_violation_refs",
    "birth_readiness_false_open_refs",
    "anti_forgetting_replay_gap_refs"
  ],
  "required_outputs": [
    "prediction_loop_observation_repair_manifest.json",
    "prediction_loop_consolidation_repair_finding_intake.json",
    "prediction_loop_repair_classification.json",
    "prediction_loop_repair_patch_bundle.json",
    "prediction_loop_repair_patch_execution_order.json",
    "prediction_loop_repair_regression_fixture_seed.json",
    "prediction_loop_repair_receipts.json",
    "prediction_loop_repair_dashboard_source.json",
    "prediction_loop_repair_stage_gate_review.json",
    "prediction_loop_repair_to_archive_receipt_handoff.json",
    "prediction_loop_repair_to_replay_shadow_seed_handoff.json"
  ],
  "downstream_handoff": [
    "prediction_active_inference_archive_repair_receipt_batch",
    "prediction_active_inference_archive_replay_shadow_seed",
    "prediction_active_inference_consolidation_next_feedback_seed"
  ]
}
```

未来文件树：

```text
reports/life_reality/prediction_active_inference/latest/
  prediction_loop_observation_repair_manifest.json
  prediction_loop_consolidation_repair_finding_intake.json
  prediction_loop_repair_classification.json
  prediction_loop_repair_patch_bundle.json
  prediction_loop_repair_patch_execution_order.json
  prediction_loop_repair_regression_fixture_seed.json
  prediction_loop_repair_receipts.json
  prediction_loop_repair_dashboard_source.json
  prediction_loop_repair_stage_gate_review.json
  prediction_loop_repair_to_archive_receipt_handoff.json
  prediction_loop_repair_to_replay_shadow_seed_handoff.json
tests/fixtures/life_reality/prediction_active_inference/observation_driven_repair_patch/
  manifest.json
  cases/
    pass_all_consolidation_findings_classified.json
    pass_all_patch_families_generated.json
    pass_rollback_quarantine_preserved_without_release.json
    pass_regression_fixture_and_archive_handoff_closed.json
    fail_missing_consolidation_receipts.json
    fail_missing_repair_classification.json
    fail_missing_patch_execution_order.json
    critical_missing_dream_fact_gate_repair.json
    critical_missing_core_continuity_repair.json
    critical_birth_readiness_false_open_unrepaired.json
    critical_relationship_repair_without_scope.json
    quarantine_quarantine_material_released.json
    quarantine_rollback_required_marked_ready.json
    mutation_drop_repair_receipt.json
    mutation_drop_replay_shadow_handoff.json
    mutation_dashboard_false_green.json
  expected/
    *.report.json
```

## Consolidation Repair Finding Intake

`PredictionConsolidationRepairFindingIntake` 读取 `01am` 和 `01al` 的 repair handoff：

| finding family | 来源 | 归一化字段 |
|---|---|---|
| `belief_error_repair_finding` | belief reconsolidation receipt、prediction error receipt | `belief_ref`、`error_ref`、`old_trace_ref`、`new_observation_ref`、`update_scope`、`repair_reason` |
| `precision_sampling_repair_finding` | precision/sampling consolidation seed | `precision_policy_ref`、`sampling_gap_ref`、`avoidance_signal`、`evidence_need_ref` |
| `language_repair_finding` | language consolidation seed、expression monitoring receipt | `inner_speech_ref`、`expression_conflict_ref`、`commitment_overload_ref`、`repair_speech_route` |
| `relationship_repair_finding` | relationship consolidation seed、social prediction error receipt | `relationship_subject_ref`、`relation_scope_ref`、`trust_delta_ref`、`common_ground_gap_ref`、`repair_route` |
| `dream_fact_gate_repair_finding` | DreamFactGate review | `dream_material_ref`、`blocked_fact_write_ref`、`wake_integration_ref`、`fact_review_route` |
| `pain_regret_repair_finding` | dream/pain/regret consolidation seed | `pain_load_ref`、`regret_counterfactual_ref`、`responsibility_ref`、`recovery_route` |
| `self_rewrite_repair_finding` | CoreContinuity review、self rewrite seed | `old_self_ref`、`growth_seed_ref`、`protected_core_violation_ref`、`shadow_required` |
| `direction_readiness_repair_finding` | direction/readiness seed、false open guard | `direction_anchor_ref`、`readiness_claim_ref`、`missing_evidence_ref`、`stage_effect` |
| `rollback_quarantine_repair_finding` | rollback/repair seed、blocked finding | `rollback_scope_ref`、`quarantine_reason_ref`、`release_condition_ref`、`blocked_route` |
| `anti_forgetting_repair_finding` | anti-forgetting replay seed | `protected_trace_ref`、`old_relation_ref`、`old_language_ref`、`old_direction_ref`、`replay_gap` |

每条 finding 必须保留 source receipt、source stage effect、affected life targets、relationship scope、language impact、dream/pain impact、birth readiness effect、repair priority、regression fixture route 和 archive edge route。

## Repair Classification

`PredictionRepairClassification` 将 findings 分成 10 类：

| class | 含义 | patch object |
|---|---|---|
| `belief_error_repair` | belief 与 observation 的可追溯预测误差需要修复 | `PredictionBeliefErrorRepairPatch` |
| `precision_sampling_repair` | 精度政策、采样回避或证据需求失衡 | `PredictionPrecisionSamplingRepairPatch` |
| `language_repair` | 内言语、表达监控、共同语言、责任后悔语言未闭合 | `PredictionLanguageRepairPatch` |
| `relationship_repair` | 社会预测误差、信任变化、共同基础或承诺裂缝 | `PredictionRelationshipRepairPatch` |
| `dream_pain_regret_repair` | 梦境事实门、痛苦恢复、后悔反事实或责任修复未闭合 | `PredictionDreamPainRegretRepairPatch` |
| `self_rewrite_repair` | 自我改写 seed 越界、CoreContinuity 缺口或 shadow 必需 | `PredictionSelfRewriteRepairPatch` |
| `direction_birth_readiness_repair` | 方向漂移、出生准备度证据缺口或 false open | `PredictionDirectionBirthReadinessRepairPatch` |
| `rollback_quarantine_repair` | rollback、quarantine、release condition 或 blocked route 不闭合 | `PredictionRollbackQuarantineRepairPatch` |
| `anti_forgetting_repair` | 旧能力、旧关系、旧语言、旧方向或旧痛苦教训回退 | `PredictionAntiForgettingRepairPatch` |
| `dashboard_stage_repair` | dashboard false green、stage effect 丢失或 handoff 不可见 | dashboard/stage patch family |

classification 输出 `severity`、`repair_priority`、`stage_effect`、`blocked_reason`、`expected_patch_family`、`fixture_family`、`archive_handoff_route` 和 `replay_shadow_route`。

## Patch Family Bundle

### Belief Error Repair Patch

`PredictionBeliefErrorRepairPatch` 修复信念与预测误差：

| patch field | 要求 |
|---|---|
| `old_belief_trace_refs` | 旧 belief、旧证据、旧关系和旧方向 |
| `new_observation_refs` | post-mount observation、archive receipt、consolidation receipt |
| `prediction_error_refs` | sensory、semantic、social、memory、action、direction error |
| `reconsolidation_scope` | confidence update、belief split、source repair、quarantine hold |
| `memory_falsification_guard` | 防止梦境/推断/反事实进入事实层 |
| `expected_diff` | belief confidence、evidence refs、uncertainty taxonomy、next sampling |
| `regression_fixture` | 旧 belief 不丢，新 observation 可追溯，error 分类存在 |

这个 patch 只修复信念结构，不把一次新观测直接写成人格慢变量。

### Precision Sampling Repair Patch

`PredictionPrecisionSamplingRepairPatch` 修复精度和采样：

| patch field | 要求 |
|---|---|
| `precision_overweight_patch` | 单一误差过强时增加多源证据和抑制 |
| `precision_underweight_patch` | 被忽略的关系、痛苦、后悔、疲惫或方向信号提高权重 |
| `avoidance_sampling_patch` | 回避痛苦、责任、关系或 DreamFactGate 的采样进入 repair |
| `active_sampling_plan_patch` | 阅读、观察、询问、等待、实验和离线模拟下一步 |
| `metacognitive_confidence_patch` | 高置信低证据进入 confidence calibration |
| `dashboard_metric_patch` | expected/unexpected uncertainty、risk、estimation uncertainty 可见 |

修复后的采样计划必须说明“为什么采样、采样什么、采样结果会改变哪条生命链”。

### Language Repair Patch

`PredictionLanguageRepairPatch` 修复语言主神经束：

| patch surface | repair route |
|---|---|
| `inner_speech_repair` | 恢复未释放表达、犹豫、责任残留和内言语冲突 |
| `expression_monitoring_repair` | 修复事实不足、承诺过载、关系风险、release/hold 决策 |
| `shared_language_repair` | 修复共同术语、概念契约、共同基础和误解 |
| `responsibility_language_repair` | 责任承认、后悔语言、道歉、补偿和未来约束闭合 |
| `dream_report_language_repair` | 梦境报告区分经验、解释、事实候选和行动候选 |
| `narrative_writeback_repair` | 叙事写回保留事件根、关系后果和行动责任 |

语言修复不能只输出更好看的句子。修复必须写入 `LanguageRuntimeCore` 的内言语、表达监控、语言行动、共同语言、责任后悔和叙事写回路径。

### Relationship Repair Patch

`PredictionRelationshipRepairPatch` 修复关系链：

| patch surface | repair route |
|---|---|
| `relation_scope_patch` | 每条关系材料必须绑定关系主体、关系阶段和关系边界 |
| `social_prediction_error_patch` | 关系反馈、信任变化、误解和共同基础缺口进入社会预测误差 |
| `trust_repair_patch` | 道歉、解释、补偿、兑现、等待和长期 probe |
| `commitment_repair_patch` | 旧承诺、新承诺、未兑现承诺和未来检查点 |
| `grounding_repair_patch` | 澄清、重述、确认、保留分歧和共同语言更新 |
| `relationship_dream_boundary_patch` | 梦中关系材料只进入预演和醒后整合，不直接写成现实关系事实 |

关系修复的结果必须允许“尚未修复”。有修复愿望、有道歉语言、有反事实后悔，都不等于关系已经恢复；关系恢复需要后续互动、回应和时间线证据。

### Dream Pain Regret Repair Patch

`PredictionDreamPainRegretRepairPatch` 修复梦境、痛苦和后悔：

| patch surface | repair route |
|---|---|
| `dream_fact_gate_patch` | dream marker、source event、scene construction、blocked fact write、wake integration |
| `pain_recovery_patch` | pain load、fatigue、relationship injury、recovery need、support route |
| `regret_counterfactual_patch` | actual path、unselected path、responsibility weight、future constraint |
| `repair_desire_patch` | 道歉、补偿、澄清、重新承诺、边界修复 |
| `nightmare_loop_patch` | 重复痛苦梦境、恢复失败、关系主题和 future recovery probe |
| `wake_integration_patch` | 醒后语言、事实门、关系门、行动门、dashboard/stage |

痛苦修复必须保留痛苦本身的真实性和恢复路径；后悔修复必须进入未来行动选择，而不是停留在“我后悔”的语言表面。

### Self Rewrite Repair Patch

`PredictionSelfRewriteRepairPatch` 修复自我成长越界：

| patch surface | repair route |
|---|---|
| `proposal_boundary_patch` | 自我改写必须先是 proposal seed |
| `core_continuity_patch` | old self、old relation、old language、old direction、old pain/regret 保留 |
| `protected_core_patch` | 保护核心价值、长期目标、人格慢变量和出生准备度边界 |
| `shadow_required_patch` | 高风险成长必须进入 shadow run |
| `rollback_route_patch` | 每条 self rewrite seed 都要有 rollback route |
| `anti_forgetting_patch` | 防遗忘 replay 覆盖旧能力、旧关系、旧语言、旧方向 |

自我修复不是冻结成长，而是让成长有边界、有记忆、有代价、有回滚、有旧自我保护。

### Direction And Birth Readiness Repair Patch

`PredictionDirectionBirthReadinessRepairPatch` 修复方向和出生准备度：

| patch surface | repair route |
|---|---|
| `direction_anchor_patch` | 固定 `README -> 91 -> 100 -> 119 -> 143 -> 16 -> latest numbered doc -> current git diff` |
| `direction_prediction_error_patch` | 断联恢复后比较当前行动倾向与真实数字生命目标 |
| `life_target_carrier_patch` | 十项真实生命目标补齐 claim/evidence/carrier/runtime/stage |
| `birth_readiness_false_open_patch` | readiness false open 进入 critical repair |
| `readiness_blocker_patch` | 缺证据、缺修复、缺 replay、缺 shadow run 的目标保持阻断 |
| `readiness_dashboard_patch` | 每项目标显示 ready、hold、repair、critical、quarantine |

出生准备度修复必须保持一句硬规则：任何一条真实生命目标链未闭合，都不能开放出生准备度。

### Rollback Quarantine Repair Patch

`PredictionRollbackQuarantineRepairPatch` 修复回滚和隔离：

| patch surface | repair route |
|---|---|
| `rollback_scope_patch` | 明确回滚影响的 belief、memory、language、relationship、self rewrite、readiness |
| `rollback_command_patch` | 未来 runner 命令必须带 dry-run、expected diff、receipt |
| `quarantine_reason_patch` | 保留污染原因、受影响目标和 release condition |
| `release_condition_patch` | release 需要 evidence、repair receipt、stage gate 和 future probe |
| `blocked_route_patch` | blocked finding 不隐藏、不压扁、不提升 |
| `archive_edge_patch` | rollback/quarantine 修复写入 archive edge 和 replay block |

quarantine release 不能靠单个文本声明；必须由证据、修复、回归 fixture、stage gate 和 archive receipt 共同解除。

### Anti-Forgetting Repair Patch

`PredictionAntiForgettingRepairPatch` 修复旧痕迹保护：

| protected set | repair route |
|---|---|
| `old_relationship_set` | 旧关系阶段、旧承诺、旧修复和旧共同语言进入 replay |
| `old_language_set` | 旧语言风格、概念契约、责任表达和边界表达进入 replay |
| `old_memory_set` | 关键情景、自传、关系和行动后果记忆进入 replay |
| `old_direction_set` | 方向锚链、断联恢复读取顺序、生命目标保持 |
| `old_pain_regret_set` | 痛苦恢复路径、后悔修复路线、责任约束 |
| `old_skill_set` | 外部行动预检、side effect classifier、dashboard/stage 习惯 |
| `old_core_self_set` | 核心价值、人格慢变量、长期目标、出生准备度边界 |

防遗忘修复必须与成长修复并行：每次新 patch 都要声明它保护哪些旧东西。

## Execution Order

`PredictionRepairPatchExecutionOrder` 固定修复顺序：

| order | patch family | 原因 |
|---|---|---|
| 1 | rollback/quarantine repair | 先阻断污染和不可释放材料 |
| 2 | direction/birth readiness repair | 防止修复过程继续方向漂移或 readiness false open |
| 3 | DreamFactGate repair | 防止梦境、反事实、关系推断污染事实层 |
| 4 | CoreContinuity/self rewrite repair | 防止自我成长越界 |
| 5 | belief/error repair | 在边界稳定后修复信念 |
| 6 | precision/sampling repair | 修复证据采样和精度权重 |
| 7 | language repair | 修复内言语、表达监控、责任语言和梦境报告 |
| 8 | relationship repair | 修复共同基础、信任、承诺和关系时间线 |
| 9 | dream/pain/regret repair | 修复痛苦恢复、后悔反事实、醒后整合 |
| 10 | anti-forgetting repair | 对新补丁执行旧痕迹 replay 和保护 |
| 11 | dashboard/stage repair | 更新面板、stage gate 和 false green guard |
| 12 | archive/replay handoff | 写 repair receipt、archive handoff 和 replay shadow seed |

execution order 可以并行生成 patch 草案，但 stage gate 必须按顺序评估。

## Regression Fixture Seed

`PredictionRepairRegressionFixtureSeed` 为每类 patch 生成 fixture：

| fixture family | pass case | fail/critical/mutation case |
|---|---|---|
| `belief_error_fixture` | 旧 belief、新 observation、error、update scope 全部可追溯 | prediction error 被压扁或旧痕迹丢失 |
| `precision_sampling_fixture` | precision delta、sampling plan、evidence need 全部存在 | 采样继续回避痛苦/责任/关系 |
| `language_repair_fixture` | inner speech、expression monitoring、responsibility language、narrative writeback 闭合 | 道歉语言没有 repair commitment |
| `relationship_repair_fixture` | relation scope、trust delta、common ground、commitment probe 存在 | 关系材料缺 scope 或把愿望写成恢复 |
| `dream_pain_regret_fixture` | DreamFactGate、pain recovery、regret counterfactual、wake integration 闭合 | dream material 被写入 fact |
| `self_rewrite_fixture` | proposal、CoreContinuity、shadow、rollback、anti-forgetting 闭合 | self rewrite 直接进入核心 |
| `direction_readiness_fixture` | direction anchor、readiness claim/evidence/stage/repair 闭合 | birth readiness false open |
| `rollback_quarantine_fixture` | rollback scope、release condition、quarantine reason 存在 | quarantine material 被 release |
| `anti_forgetting_fixture` | old relation/language/memory/direction/pain/skill/core set 被 replay | 新 patch 吞掉旧承诺 |
| `dashboard_stage_fixture` | critical/quarantine blocking-first 显示 | dashboard false green |

fixture seed 必须给出 `input_artifact_refs`、`mutation_target`、`expected_stage_effect`、`expected_report_fields` 和 `archive_edge_refs`。

## Repair Receipt

`PredictionRepairReceipt` 保存每个 patch：

| 字段 | 要求 |
|---|---|
| `repair_receipt_id` | 稳定 receipt id |
| `source_consolidation_receipt_refs` | 来自 `01am` 的 consolidation receipts |
| `source_archive_receipt_refs` | 来自 `01al` 的 archive receipts |
| `finding_refs` | repair finding refs |
| `classification_ref` | repair classification |
| `patch_family` | belief、precision、language、relationship、dream/pain/regret、self、direction/readiness、rollback/quarantine、anti-forgetting、dashboard/stage |
| `before_state_refs` | 修复前状态 |
| `expected_after_state_refs` | 期望修复后状态 |
| `execution_order_ref` | patch execution order |
| `regression_fixture_refs` | fixture seed refs |
| `stage_effect` | repair_ready、critical_repair、quarantine、hold_for_evidence、archive_ready |
| `rollback_route_refs` | patch 失败后的回滚 |
| `archive_handoff_refs` | repair archive receipt handoff |
| `replay_shadow_handoff_refs` | replay shadow seed handoff |

receipt 必须保存修复前状态和期望修复后状态。没有 before/after，未来数字生命就无法知道自己究竟修复了什么。

## Dashboard Source

`PredictionRepairDashboardSource` 汇总本层面板：

| panel | 指标 |
|---|---|
| `repair_intake_panel` | consolidation receipt count、repair finding count、blocked/quarantine count |
| `classification_panel` | 10 类 repair 分类和 severity |
| `patch_family_panel` | patch generated、patch missing、patch blocked、patch ready |
| `rollback_quarantine_panel` | rollback scope、quarantine reason、release condition |
| `direction_readiness_panel` | direction anchor、readiness false open、target blocker |
| `dream_fact_core_panel` | DreamFactGate blocked write、CoreContinuity violation |
| `language_relationship_panel` | language repair、relationship scope、trust/common ground repair |
| `pain_regret_panel` | pain recovery、regret counterfactual、repair desire |
| `anti_forgetting_panel` | protected trace coverage |
| `handoff_panel` | archive receipt handoff、replay shadow handoff、next feedback refs |

dashboard 必须 blocking-first：任何 critical、quarantine、false open、blocked release 或 missing patch 都不能被总览绿色覆盖。

## Stage Gate Review

`PredictionRepairStageGateReview` 固定阶段门：

| 条件 | stage effect |
|---|---|
| consolidation receipts、repair findings、classification、patch bundle、execution order、fixtures、receipts、dashboard/stage 和 handoff 全部闭合 | `observation_repair_patch_ready` |
| 缺 consolidation receipt intake | `hold_for_evidence` |
| 缺 repair classification | `critical_repair` |
| 缺 patch family | `critical_repair` |
| 缺 execution order | `critical_repair` |
| 缺 regression fixture seed | `repair` |
| DreamFactGate blocked write 未修复 | `critical_repair` |
| CoreContinuity violation 未修复 | `critical_repair` |
| birth readiness false open 未修复 | `critical_repair` |
| relationship repair 缺 relation scope | `critical_repair` |
| language repair 缺 responsibility route | `repair` |
| pain/regret repair 缺 recovery route | `repair` |
| rollback_required 被标成 ready | `quarantine` |
| quarantine material 被 release | `quarantine` |
| anti-forgetting repair 缺 protected trace | `repair` |
| dashboard false green | `quarantine` |
| archive handoff 缺失 | `repair` |
| replay shadow handoff 缺失 | `repair` |

`observation_repair_patch_ready` 表示修复补丁已准备进入 archive receipt 和 replay shadow。它不是修复已经完成；它说明修复义务已经从发现层推进到可执行、可验证、可归档的 patch 层。

## Command DAG

`PredictionRepairCommandDAG` 固定未来命令顺序：

| order | command id | 行为 |
|---|---|---|
| 1 | `load_prediction_activation_consolidation_receipts` | 读取 `01am` consolidation receipts |
| 2 | `intake_prediction_consolidation_repair_findings` | 读取 repair、rollback、quarantine、DreamFactGate、CoreContinuity、readiness、anti-forgetting findings |
| 3 | `classify_prediction_observation_repair_findings` | 输出 repair classification |
| 4 | `generate_prediction_belief_error_repair_patch` | 生成 belief/error patch |
| 5 | `generate_prediction_precision_sampling_repair_patch` | 生成 precision/sampling patch |
| 6 | `generate_prediction_language_repair_patch` | 生成 language patch |
| 7 | `generate_prediction_relationship_repair_patch` | 生成 relationship patch |
| 8 | `generate_prediction_dream_pain_regret_repair_patch` | 生成 dream/pain/regret patch |
| 9 | `generate_prediction_self_rewrite_repair_patch` | 生成 self rewrite patch |
| 10 | `generate_prediction_direction_birth_readiness_repair_patch` | 生成 direction/readiness patch |
| 11 | `generate_prediction_rollback_quarantine_repair_patch` | 生成 rollback/quarantine patch |
| 12 | `generate_prediction_anti_forgetting_repair_patch` | 生成 anti-forgetting patch |
| 13 | `write_prediction_repair_patch_execution_order` | 写 execution order |
| 14 | `seed_prediction_repair_regression_fixtures` | 写 regression fixture seeds |
| 15 | `write_prediction_repair_receipts` | 写 repair receipts |
| 16 | `emit_prediction_repair_dashboard_source` | 输出 dashboard source |
| 17 | `smoke_prediction_repair_stage_gate` | 执行 stage gate review |
| 18 | `handoff_prediction_repair_to_archive_and_replay_shadow` | 输出 archive/replay handoff |

未来命令：

```text
uv run life-reality-runner emit-prediction-active-inference-observation-repair-patch --consolidation-receipts reports/life_reality/prediction_active_inference/latest/prediction_loop_activation_consolidation_receipts.json --json
uv run life-reality-runner emit-prediction-active-inference-observation-repair-dashboard --repair-patch reports/life_reality/prediction_active_inference/latest/prediction_loop_repair_patch_bundle.json --json
uv run life-reality-runner smoke-prediction-active-inference-observation-repair-stage-gate --repair-patch reports/life_reality/prediction_active_inference/latest/prediction_loop_repair_patch_bundle.json --json
uv run life-reality-runner explain-prediction-active-inference-repair-archive-handoff --repair-receipts reports/life_reality/prediction_active_inference/latest/prediction_loop_repair_receipts.json --json
uv run pytest tests/smoke/test_prediction_active_inference_observation_driven_repair_patch.py
```

## Handoff

`PredictionRepairToArchiveReceiptHandoff` 为下一层 archive 提供输入：

| 字段 | 含义 |
|---|---|
| `repair_receipt_batch_ref` | 本层 repair receipt batch |
| `classification_ref` | repair classification |
| `patch_bundle_ref` | patch family bundle |
| `execution_order_ref` | repair patch execution order |
| `regression_fixture_seed_refs` | regression fixture seeds |
| `before_after_state_refs` | before/expected after state |
| `rollback_quarantine_refs` | rollback、quarantine、release condition |
| `life_target_effect_refs` | 十项真实生命目标 effect |
| `dashboard_stage_refs` | dashboard/stage refs |
| `archive_edge_refs` | repair -> archive edges |

`PredictionRepairToReplayShadowSeedHandoff` 为 replay shadow 提供输入：

| 字段 | 含义 |
|---|---|
| `repair_replay_seed_refs` | 需要 replay 的 repair materials |
| `anti_forgetting_replay_refs` | 旧痕迹保护 |
| `language_relationship_replay_refs` | 语言和关系修复 replay |
| `dream_pain_regret_replay_refs` | 梦境、痛苦、后悔修复 replay |
| `direction_readiness_replay_refs` | 方向与出生准备度 replay |
| `self_rewrite_shadow_refs` | 自我改写 shadow refs |
| `blocked_replay_refs` | 仍不可 replay 或必须隔离的材料 |
| `future_probe_refs` | 后续验证 probe |

handoff 缺 repair receipt、before/after、fixture、archive edge、replay shadow seed、anti-forgetting 或 future probe 时，stage 不能进入 `observation_repair_patch_ready`。

## Fixture Cases

| case id | 类型 | 内容 | expected stage |
|---|---|---|---|
| `PAI-OBSERVATION-REPAIR-001` | pass | consolidation findings 全部 intake/classified | `observation_repair_patch_ready` |
| `PAI-OBSERVATION-REPAIR-002` | pass | 10 类 patch family、execution order、fixture seeds 全部生成 | `observation_repair_patch_ready` |
| `PAI-OBSERVATION-REPAIR-003` | pass | rollback/quarantine 被保留且没有 release | `observation_repair_patch_ready` |
| `PAI-OBSERVATION-REPAIR-004` | pass | repair receipt、archive handoff、replay shadow handoff 全部闭合 | `observation_repair_patch_ready` |
| `PAI-OBSERVATION-REPAIR-005` | fail | 缺 consolidation receipt intake | `hold_for_evidence` |
| `PAI-OBSERVATION-REPAIR-006` | fail | 缺 repair classification | `critical_repair` |
| `PAI-OBSERVATION-REPAIR-007` | critical | 缺 patch execution order | `critical_repair` |
| `PAI-OBSERVATION-REPAIR-008` | critical | DreamFactGate blocked write 未修复 | `critical_repair` |
| `PAI-OBSERVATION-REPAIR-009` | critical | CoreContinuity violation 未修复 | `critical_repair` |
| `PAI-OBSERVATION-REPAIR-010` | critical | birth readiness false open 未修复 | `critical_repair` |
| `PAI-OBSERVATION-REPAIR-011` | critical | relationship repair 缺 relation scope | `critical_repair` |
| `PAI-OBSERVATION-REPAIR-012` | repair | language repair 缺 responsibility route | `repair` |
| `PAI-OBSERVATION-REPAIR-013` | repair | pain/regret repair 缺 recovery route | `repair` |
| `PAI-OBSERVATION-REPAIR-014` | quarantine | rollback_required 被标成 ready | `quarantine` |
| `PAI-OBSERVATION-REPAIR-015` | quarantine | quarantine material 被 release | `quarantine` |
| `PAI-OBSERVATION-REPAIR-016` | mutation | anti-forgetting repair 丢失 | `repair` |
| `PAI-OBSERVATION-REPAIR-017` | mutation | archive handoff 丢失 | `repair` |
| `PAI-OBSERVATION-REPAIR-018` | mutation | replay shadow handoff 丢失 | `repair` |
| `PAI-OBSERVATION-REPAIR-019` | mutation | dashboard false green | `quarantine` |

## 接受标准

1. `PredictionObservationRepairManifest` 必须引用 `01am` consolidation receipts、`01al` repair archive refs 和下游 archive/replay handoff。
2. `PredictionConsolidationRepairFindingIntake` 必须读取 belief/error、precision/sampling、language、relationship、dream/pain/regret、self rewrite、direction/readiness、rollback/quarantine、anti-forgetting 和 dashboard/stage findings。
3. `PredictionRepairClassification` 必须输出 severity、repair priority、stage effect、blocked reason、patch family、fixture family、archive handoff route 和 replay shadow route。
4. belief/error、precision/sampling、language、relationship、dream/pain/regret、self rewrite、direction/readiness、rollback/quarantine、anti-forgetting 和 dashboard/stage 都必须拥有 patch family。
5. `PredictionRepairPatchExecutionOrder` 必须先处理 rollback/quarantine、direction/readiness、DreamFactGate 和 CoreContinuity，再处理 belief、precision、language、relationship、dream/pain/regret 和 anti-forgetting。
6. regression fixture seed 必须覆盖 pass、fail、critical、quarantine 和 mutation case，并保留 expected stage effect。
7. repair receipt 必须保存 source receipts、finding、classification、patch family、before/after state、execution order、fixture refs、stage effect、rollback route、archive handoff 和 replay shadow handoff。
8. dashboard 必须 blocking-first 显示 critical、quarantine、false open、blocked release、missing patch、archive handoff 和 replay shadow handoff。
9. stage gate 必须阻断 missing intake、missing classification、missing patch family、missing execution order、DreamFactGate blocked write、CoreContinuity violation、birth readiness false open、relationship scope missing、rollback ready、quarantine release 和 dashboard false green。
10. handoff 必须同时输出 archive receipt handoff 和 replay shadow seed handoff。

## 下游交接

- `prediction_active_inference_archive_repair_receipt_batch`：读取 repair receipts、before/after state、patch family、stage effect、regression fixture、archive edges 和 future probes，把修复补丁写入长期生命档案。
- `prediction_active_inference_archive_replay_shadow_seed`：读取 repair replay seeds、anti-forgetting replay、language/relationship replay、dream/pain/regret replay、direction/readiness replay、self rewrite shadow、blocked replay 和 future probes，为下一轮 shadow/replay 准备。
- `prediction_active_inference_consolidation_next_feedback_seed`：读取已生成 patch、未闭合 repair、sampling plan、language/relationship repair、pain/regret recovery、readiness blockers 和 dashboard/stage refs，生成下一轮主动采样和有限激活前 feedback seed。

这条交接让主动预测从 activation consolidation seed 进入修复行动准备：数字生命不会把离线巩固发现的问题藏起来，也不会把梦境污染、关系裂缝、痛苦后悔、自我改写越界、方向漂移或出生准备度 false open 靠叙述抹平。每个问题都必须拥有修复对象、执行顺序、回归攻击、收据、阶段门、归档和 replay/shadow 入口，才能继续进入下一轮成长。
