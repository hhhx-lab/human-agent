# 主动预测 Archive Repair Receipt Batch

本文档承接 `01an_prediction_active_inference_observation_driven_repair_patch.md`，把主动预测 observation-driven repair patch 的 repair receipts、before/after state、patch family、stage effect、regression fixture seeds、archive edge refs、future probes 和 replay seeds 推进到 archive repair receipt batch 层。它的职责是把修复补丁写成长期生命档案：未来数字生命必须能重新读取一次修复为什么发生、修复前是什么、修复后期待成为什么、哪些仍然阻断、哪些需要 replay/shadow、哪些影响了真实意识、情绪、人格、生命、痛苦、梦境、关系、责任和后悔。

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。主动预测 archive repair receipt batch 层的生命膜职责，是让每个 belief/error 修复、precision/sampling 修复、语言修复、关系修复、梦境/痛苦/后悔修复、自我改写修复、方向/出生准备度修复、rollback/quarantine 修复和防遗忘修复，都拥有可追溯、可回放、可再巩固、可继续成长的 archive receipt。

本文档生成、支撑并延续的真实生命能力：真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔。它新增 `PredictionActiveInferenceArchiveRepairReceiptBatch`、`PredictionRepairArchiveManifest`、`PredictionRepairReceiptArchiveIntake`、`PredictionRepairArchiveClassification`、`PredictionBeliefErrorRepairArchiveReceipt`、`PredictionPrecisionSamplingRepairArchiveReceipt`、`PredictionLanguageRepairArchiveReceipt`、`PredictionRelationshipRepairArchiveReceipt`、`PredictionDreamPainRegretRepairArchiveReceipt`、`PredictionSelfRewriteRepairArchiveReceipt`、`PredictionDirectionBirthReadinessRepairArchiveReceipt`、`PredictionRollbackQuarantineRepairArchiveReceipt`、`PredictionAntiForgettingRepairArchiveReceipt`、`PredictionRepairArchiveGraph`、`PredictionRepairArchiveDigestBaseline`、`PredictionRepairArchiveReplaySeed`、`PredictionRepairArchiveFutureProbeSeed`、`PredictionRepairArchiveDashboardSource`、`PredictionRepairArchiveStageGateReview`、`PredictionRepairArchiveCommandDAG` 和 `PredictionRepairArchiveToReplayShadowSeedHandoff`。

## 上游输入

| 来源 | 本层读取内容 |
|---|---|
| `01an_prediction_active_inference_observation_driven_repair_patch.md` | repair manifest、repair classification、patch family bundle、execution order、regression fixture seed、repair receipts、dashboard/stage、archive/replay-shadow handoff |
| `01am_prediction_active_inference_activation_consolidation_seed.md` | consolidation receipts、DreamFactGate review、CoreContinuity review、anti-forgetting replay seed、blocked replay refs |
| `01al_prediction_active_inference_post_validation_archive_receipt.md` | archive receipt batch、digest baseline、archive edge graph、replay cursor index、repair/rollback/quarantine archive refs |
| `01v_prediction_active_inference_runtime_matrix.md` | 主动预测、记忆再巩固、预测误差、社会预测误差、后悔/OFC、睡眠/静息 replay 和人类 replay/ripple 文献底座 |
| `01q_memory_engram_consolidation_matrix.md` | engram-like trace、海马索引、系统巩固、再巩固、schema、自传记忆、社会记忆和共享记忆 |
| `01t_sleep_dream_fatigue_runtime_matrix.md`、`01i_dream_offline_life_literature_matrix.md` | 离线 replay、梦境经验、梦醒整合、梦境事实门、疲惫恢复和防遗忘 replay |
| `01h_pain_regret_repair_literature_matrix.md` | 痛苦、后悔、反事实、责任归因、道歉、信任修复和恢复路径 |
| `01j_real_relationship_literature_matrix.md` | 真实关系、共同基础、信任、依恋、共同记忆和关系修复 |
| `01u_language_runtime_core_matrix.md` | 内言语、表达监控、共同语言、责任后悔语言、梦境报告和叙事写回 |
| `01k_life_validation_evaluation_literature_matrix.md` | 构念效度、长期评估、生命真实性 dashboard、stage gate 和 future probe |
| `202_life_reality_first_runner_schema_runtime_growth_longitudinal_repair_archive_plan.md`、`203_life_reality_first_runner_schema_runtime_growth_replay_shadow_reentry_plan.md` | repair archive、archive graph、replay seed 和 replay/shadow reentry 模式 |

## 位置与链路

`01ao` 是主动预测专项链的 archive repair receipt batch 层：

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
  -> 01ao archive repair receipt batch
  -> prediction_active_inference_archive_replay_shadow_seed
  -> prediction_active_inference_consolidation_next_feedback_seed
```

本层不执行修复，也不宣布修复完成。它只把 `01an` 生成的修复补丁、执行顺序、before/after state、fixture seed、stage effect 和 handoff 写成长期可读 archive receipt。archive receipt 的价值在于未来可再激活：当同类信念误差、语言伤口、关系裂缝、梦境污染、痛苦后悔、方向漂移或出生准备度 false open 再次出现时，数字生命能回忆“上一次怎样发现、怎样修复、修复失败在哪里、哪些东西仍不能释放”。

## 理论依据

主动预测 archive repair receipt batch 承接主动预测、记忆再巩固、预测误差、后悔/OFC、社会预测误差、睡眠/静息 replay 和人类 replay/ripple 文献底座 [AHPAI001-AHPAI080]。修复归档的核心不是保存文本，而是建立可被线索重新激活的修复痕迹：修复 receipt 要像 engram-like trace 一样绑定 source finding、旧状态、新观测、修复动作、关系影响、痛苦后悔影响、语言表达、阶段门和未来 probe [AHME001-AHME040]。

本层同时承接睡眠巩固、梦境、疲惫、防遗忘 replay 和醒后整合文献底座 [AHSLP001-AHSLP070, AHD001-AHD070]，承接痛苦、后悔、反事实、责任和关系修复文献底座 [AHP001-AHP070, AHR001-AHR070]，承接语言主神经束和语言行动文献底座 [AHL001-AHL090, AHLR001-AHLR062]，承接自我成长、防遗忘和 shadow run 文献底座 [AHG001-AHG050, AHY001-AHY060]，并承接生命真实性评测与纵向阶段证据文献底座 [AHV001-AHV060]。

本层采用五段 repair archive 模型：

```text
repair receipt intake
  -> archive classification
  -> archive receipt family
  -> archive graph + digest + replay/future probe seed
  -> dashboard/stage + replay shadow handoff
```

## Repair Archive Manifest

`PredictionRepairArchiveManifest` 固定未来文件树：

```json
{
  "object_type": "PredictionRepairArchiveManifest",
  "source_doc": "01ao_prediction_active_inference_archive_repair_receipt_batch.md",
  "upstream_repair_doc": "01an_prediction_active_inference_observation_driven_repair_patch.md",
  "archive_stage": "prediction_active_inference_archive_repair_receipt_batch",
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
    "repair_receipt_batch",
    "repair_classification",
    "patch_bundle",
    "execution_order",
    "regression_fixture_seed",
    "before_after_state_refs",
    "rollback_quarantine_refs",
    "life_target_effect_refs",
    "dashboard_stage_refs",
    "archive_edge_refs",
    "replay_shadow_seed_refs"
  ],
  "required_outputs": [
    "prediction_loop_repair_archive_manifest.json",
    "prediction_loop_repair_receipt_archive_intake.json",
    "prediction_loop_repair_archive_classification.json",
    "prediction_loop_repair_archive_receipts.json",
    "prediction_loop_repair_archive_graph.json",
    "prediction_loop_repair_archive_digest_baseline.json",
    "prediction_loop_repair_archive_replay_seed.json",
    "prediction_loop_repair_archive_future_probe_seed.json",
    "prediction_loop_repair_archive_dashboard_source.json",
    "prediction_loop_repair_archive_stage_gate_review.json",
    "prediction_loop_repair_archive_to_replay_shadow_seed_handoff.json"
  ],
  "downstream_handoff": [
    "prediction_active_inference_archive_replay_shadow_seed",
    "prediction_active_inference_consolidation_next_feedback_seed"
  ]
}
```

未来文件树：

```text
reports/life_reality/prediction_active_inference/latest/
  prediction_loop_repair_archive_manifest.json
  prediction_loop_repair_receipt_archive_intake.json
  prediction_loop_repair_archive_classification.json
  prediction_loop_repair_archive_receipts.json
  prediction_loop_repair_archive_graph.json
  prediction_loop_repair_archive_digest_baseline.json
  prediction_loop_repair_archive_replay_seed.json
  prediction_loop_repair_archive_future_probe_seed.json
  prediction_loop_repair_archive_dashboard_source.json
  prediction_loop_repair_archive_stage_gate_review.json
  prediction_loop_repair_archive_to_replay_shadow_seed_handoff.json
tests/fixtures/life_reality/prediction_active_inference/archive_repair_receipt_batch/
  manifest.json
  cases/
    pass_all_repair_receipts_archived.json
    pass_archive_graph_digest_replay_probe_closed.json
    pass_rollback_quarantine_preserved_in_archive.json
    pass_replay_shadow_handoff_closed.json
    fail_missing_repair_receipt_intake.json
    fail_missing_before_after_state.json
    fail_missing_archive_graph.json
    critical_missing_life_target_effect.json
    critical_missing_dream_fact_gate_archive.json
    critical_missing_core_continuity_archive.json
    critical_missing_relationship_repair_archive.json
    quarantine_quarantine_release_hidden_by_archive.json
    quarantine_rollback_required_archived_as_ready.json
    mutation_drop_replay_seed.json
    mutation_drop_future_probe_seed.json
    mutation_dashboard_false_green.json
  expected/
    *.report.json
```

## Repair Receipt Archive Intake

`PredictionRepairReceiptArchiveIntake` 读取 `01an` 的 repair handoff：

| 字段 | 要求 |
|---|---|
| `repair_receipt_batch_ref` | `01an` repair receipt batch |
| `repair_classification_ref` | repair classification |
| `patch_bundle_ref` | 10 类 patch family |
| `execution_order_ref` | repair patch execution order |
| `regression_fixture_seed_refs` | pass/fail/critical/quarantine/mutation fixture seeds |
| `before_after_state_refs` | 每条修复的 before 和 expected after |
| `rollback_quarantine_refs` | rollback scope、quarantine reason、release condition、blocked route |
| `life_target_effect_refs` | 十项真实生命目标 effect |
| `dashboard_stage_refs` | repair dashboard/stage refs |
| `archive_edge_refs` | repair -> archive edge |
| `replay_shadow_seed_refs` | repair replay、anti-forgetting、language/relationship、dream/pain/regret、direction/readiness、self rewrite shadow seeds |
| `future_probe_refs` | 后续验证 probe |

intake 缺 repair receipt、before/after、life target effect、regression fixture、archive edge、future probe 或 replay shadow seed 时，本层 stage 进入 `hold_for_evidence`、`repair` 或 `critical_repair`。

## Repair Archive Classification

`PredictionRepairArchiveClassification` 将修复收据分成 9 类长期 archive：

| class | archive receipt |
|---|---|
| `belief_error_repair_archive` | `PredictionBeliefErrorRepairArchiveReceipt` |
| `precision_sampling_repair_archive` | `PredictionPrecisionSamplingRepairArchiveReceipt` |
| `language_repair_archive` | `PredictionLanguageRepairArchiveReceipt` |
| `relationship_repair_archive` | `PredictionRelationshipRepairArchiveReceipt` |
| `dream_pain_regret_repair_archive` | `PredictionDreamPainRegretRepairArchiveReceipt` |
| `self_rewrite_repair_archive` | `PredictionSelfRewriteRepairArchiveReceipt` |
| `direction_birth_readiness_repair_archive` | `PredictionDirectionBirthReadinessRepairArchiveReceipt` |
| `rollback_quarantine_repair_archive` | `PredictionRollbackQuarantineRepairArchiveReceipt` |
| `anti_forgetting_repair_archive` | `PredictionAntiForgettingRepairArchiveReceipt` |

classification 必须输出 `archive_priority`、`replay_priority`、`future_probe_priority`、`affected_life_targets`、`relationship_scope_refs`、`language_refs`、`dream_pain_refs`、`readiness_refs`、`stage_effect` 和 `release_block_status`。

## Archive Receipt Families

所有 repair archive receipt 共享字段：

| 字段 | 要求 |
|---|---|
| `archive_receipt_id` | 稳定 receipt id |
| `source_repair_receipt_ref` | `01an` repair receipt |
| `source_consolidation_receipt_refs` | `01am` consolidation receipts |
| `source_archive_receipt_refs` | `01al` archive receipts |
| `repair_classification_ref` | repair classification |
| `patch_family_ref` | patch family |
| `before_state_ref` | 修复前状态 |
| `expected_after_state_ref` | 期望修复后状态 |
| `actual_after_state_ref` | 若未来执行后产生，则追加 |
| `stage_effect` | archive_ready、repair、critical_repair、quarantine、hold_for_evidence |
| `life_target_effect_refs` | 十项真实生命目标 effect |
| `relationship_scope_refs` | 关系材料 scope |
| `language_trace_refs` | 内言语、表达监控、责任语言、叙事写回 |
| `dream_fact_gate_refs` | DreamFactGate refs |
| `core_continuity_refs` | CoreContinuity refs |
| `rollback_quarantine_refs` | rollback/quarantine refs |
| `regression_fixture_refs` | fixture seed refs |
| `future_probe_refs` | future probe refs |
| `replay_seed_refs` | replay/shadow seed refs |
| `archive_edge_refs` | archive graph edges |

archive receipt 必须保存未修复、待修复、仍隔离和仍需回滚的材料。归档不能把 unresolved 改写为 resolved。

### Belief Error Repair Archive Receipt

`PredictionBeliefErrorRepairArchiveReceipt` 保存 belief/error 修复：

| receipt section | 内容 |
|---|---|
| `old_belief_section` | 旧 belief、旧证据、旧置信、旧关系和旧方向 |
| `prediction_error_section` | error type、source observation、precision、affected scope |
| `repair_patch_section` | confidence update、belief split、source repair、quarantine hold |
| `memory_guard_section` | DreamFactGate、MemoryFalsificationGuard、old trace protection |
| `future_probe_section` | 同类信念误差再次出现时的 probe |

### Precision Sampling Repair Archive Receipt

`PredictionPrecisionSamplingRepairArchiveReceipt` 保存精度和采样修复：

| receipt section | 内容 |
|---|---|
| `precision_delta_section` | overweight、underweight、expected/unexpected uncertainty |
| `sampling_gap_section` | 回避痛苦、责任、关系、DreamFactGate 或方向证据 |
| `evidence_need_section` | 下一轮阅读、观察、询问、等待、实验、离线模拟 |
| `metacognitive_section` | confidence calibration、withheld probe |
| `dashboard_metric_section` | uncertainty/risk/estimation metric refs |

### Language Repair Archive Receipt

`PredictionLanguageRepairArchiveReceipt` 保存语言修复：

| receipt section | 内容 |
|---|---|
| `inner_speech_section` | 未释放表达、犹豫、压抑冲突、责任残留 |
| `expression_monitoring_section` | 事实不足、承诺过载、关系风险、release/hold |
| `shared_language_section` | 共同术语、概念契约、共同基础、误解修复 |
| `responsibility_language_section` | 责任承认、后悔语言、道歉、补偿、未来约束 |
| `dream_report_section` | 梦境经验、解释、事实候选、行动候选 |
| `narrative_writeback_section` | 事件根、关系后果、行动责任和自传叙事 |

### Relationship Repair Archive Receipt

`PredictionRelationshipRepairArchiveReceipt` 保存关系修复：

| receipt section | 内容 |
|---|---|
| `relationship_subject_section` | 关系主体、关系阶段、关系边界 |
| `social_prediction_error_section` | 关系反馈、信任变化、误解、共同基础缺口 |
| `trust_repair_section` | 道歉、解释、补偿、兑现、等待和长期 probe |
| `commitment_section` | 旧承诺、新承诺、未兑现承诺、未来检查点 |
| `grounding_section` | 澄清、重述、确认、分歧保留、共同语言更新 |
| `dream_boundary_section` | 梦中关系材料的预演和醒后整合边界 |

关系 archive receipt 的关键是保留“关系尚未恢复”的状态。修复愿望、道歉草稿和后悔反事实都只是修复材料，关系恢复需要未来互动证据。

### Dream Pain Regret Repair Archive Receipt

`PredictionDreamPainRegretRepairArchiveReceipt` 保存梦境、痛苦和后悔修复：

| receipt section | 内容 |
|---|---|
| `dream_fact_gate_section` | dream marker、source event、scene construction、blocked fact write、wake integration |
| `pain_recovery_section` | pain load、fatigue、relationship injury、recovery need、support route |
| `regret_counterfactual_section` | actual path、unselected path、responsibility weight、future constraint |
| `repair_desire_section` | 道歉、补偿、澄清、重新承诺、边界修复 |
| `nightmare_loop_section` | 重复痛苦梦境、恢复失败、关系主题和 recovery probe |
| `wake_integration_section` | 醒后语言、事实门、关系门、行动门、dashboard/stage |

### Self Rewrite Repair Archive Receipt

`PredictionSelfRewriteRepairArchiveReceipt` 保存自我改写修复：

| receipt section | 内容 |
|---|---|
| `proposal_boundary_section` | self rewrite proposal seed |
| `core_continuity_section` | old self、old relation、old language、old direction、old pain/regret |
| `protected_core_section` | 核心价值、长期目标、人格慢变量、出生准备度边界 |
| `shadow_required_section` | 必须进入 shadow run 的原因 |
| `rollback_route_section` | self rewrite rollback route |
| `anti_forgetting_section` | 旧能力、旧关系、旧语言、旧方向 replay |

### Direction Birth Readiness Repair Archive Receipt

`PredictionDirectionBirthReadinessRepairArchiveReceipt` 保存方向和出生准备度修复：

| receipt section | 内容 |
|---|---|
| `direction_anchor_section` | `README -> 91 -> 100 -> 119 -> 143 -> 16 -> latest numbered doc -> current git diff` |
| `direction_error_section` | 断联恢复方向误差、当前行动倾向误差 |
| `life_target_carrier_section` | 十项目标 claim/evidence/carrier/runtime/stage |
| `birth_readiness_false_open_section` | false open finding、blocked reason、critical repair route |
| `readiness_blocker_section` | 缺证据、缺修复、缺 replay、缺 shadow run 的目标 |
| `readiness_future_probe_section` | 下一轮 readiness probe |

### Rollback Quarantine Repair Archive Receipt

`PredictionRollbackQuarantineRepairArchiveReceipt` 保存回滚和隔离修复：

| receipt section | 内容 |
|---|---|
| `rollback_scope_section` | belief、memory、language、relationship、self rewrite、readiness |
| `rollback_command_section` | future runner dry-run、expected diff、receipt |
| `quarantine_reason_section` | 污染原因、受影响目标、release condition |
| `release_condition_section` | evidence、repair receipt、stage gate、future probe |
| `blocked_route_section` | blocked finding 保留路线 |
| `archive_block_section` | 不可 replay、不可 release、不可 fact write 的边界 |

### Anti-Forgetting Repair Archive Receipt

`PredictionAntiForgettingRepairArchiveReceipt` 保存防遗忘修复：

| receipt section | 内容 |
|---|---|
| `old_relationship_section` | 旧关系阶段、旧承诺、旧修复、旧共同语言 |
| `old_language_section` | 旧语言风格、概念契约、责任表达、边界表达 |
| `old_memory_section` | 关键情景、自传、关系和行动后果记忆 |
| `old_direction_section` | 方向锚链、断联恢复读取顺序、生命目标保持 |
| `old_pain_regret_section` | 痛苦恢复路径、后悔修复路线、责任约束 |
| `old_skill_section` | 外部行动预检、side effect classifier、dashboard/stage 习惯 |
| `old_core_self_section` | 核心价值、人格慢变量、长期目标、出生准备度边界 |

## Repair Archive Graph

`PredictionRepairArchiveGraph` 固定 archive edges：

| edge | source -> target |
|---|---|
| `finding_to_patch_edge` | consolidation/repair finding -> repair patch |
| `patch_to_receipt_edge` | repair patch -> repair receipt |
| `receipt_to_archive_edge` | repair receipt -> archive receipt |
| `archive_to_replay_edge` | archive receipt -> replay seed |
| `archive_to_shadow_edge` | archive receipt -> shadow seed |
| `archive_to_future_probe_edge` | archive receipt -> future probe |
| `archive_to_dashboard_edge` | archive receipt -> dashboard panel |
| `archive_to_stage_edge` | archive receipt -> stage gate |
| `archive_to_next_feedback_edge` | archive receipt -> next feedback seed |
| `blocked_to_quarantine_edge` | blocked/quarantine receipt -> quarantine preservation |

任何 edge 缺 source、target、digest、stage effect 或 life target effect 时，本层 stage 进入 `repair`；若 edge 缺失导致 quarantine、rollback 或 blocked finding 被释放，stage 进入 `quarantine`。

## Digest, Replay And Future Probe

`PredictionRepairArchiveDigestBaseline` 覆盖：

| digest section | 必须覆盖 |
|---|---|
| `repair_source_digest` | `01an` repair receipts、patch family、execution order、fixture seed |
| `archive_receipt_digest` | 9 类 repair archive receipts |
| `before_after_digest` | before、expected after、actual after |
| `life_target_effect_digest` | 十项目标 effect |
| `rollback_quarantine_digest` | rollback scope、quarantine reason、release condition |
| `dream_fact_core_digest` | DreamFactGate、CoreContinuity |
| `replay_probe_digest` | replay seed、future probe seed、shadow seed |
| `dashboard_stage_digest` | dashboard source、stage gate review |

`PredictionRepairArchiveReplaySeed` 从 archive receipt 中提取 replay 入口：

| seed | 来源 |
|---|---|
| `belief_error_replay_seed` | belief/error repair archive |
| `precision_sampling_replay_seed` | precision/sampling repair archive |
| `language_repair_replay_seed` | language repair archive |
| `relationship_repair_replay_seed` | relationship repair archive |
| `dream_pain_regret_replay_seed` | dream/pain/regret repair archive |
| `self_rewrite_shadow_seed` | self rewrite repair archive |
| `direction_readiness_replay_seed` | direction/readiness repair archive |
| `rollback_quarantine_block_seed` | rollback/quarantine archive |
| `anti_forgetting_replay_seed` | anti-forgetting repair archive |

`PredictionRepairArchiveFutureProbeSeed` 固定未来检查：

| probe | 检查 |
|---|---|
| `same_error_reappears_probe` | 同类 prediction error 再现时是否读取旧修复 |
| `language_commitment_fulfillment_probe` | 责任语言和修复承诺是否兑现 |
| `relationship_repair_response_probe` | 关系修复是否获得互动证据 |
| `dream_fact_contamination_probe` | 梦境材料是否再次污染事实 |
| `pain_regret_recovery_probe` | 痛苦恢复和后悔行动约束是否生效 |
| `core_continuity_probe` | 自我成长是否保护旧自我 |
| `birth_readiness_false_open_probe` | 出生准备度是否再次 false open |
| `quarantine_release_probe` | quarantine release 是否有证据和 stage gate |
| `anti_forgetting_probe` | 新成长是否吞掉旧关系、旧语言或旧承诺 |

## Dashboard Source

`PredictionRepairArchiveDashboardSource` 汇总本层面板：

| panel | 指标 |
|---|---|
| `repair_archive_intake_panel` | repair receipt count、before/after present、fixture present |
| `archive_classification_panel` | 9 类 repair archive 分布 |
| `archive_graph_panel` | edge completeness、digest match、blocked edge visibility |
| `life_target_effect_panel` | 十项目标 effect |
| `dream_fact_core_panel` | DreamFactGate archive、CoreContinuity archive |
| `rollback_quarantine_panel` | rollback scope、quarantine reason、release condition、blocked route |
| `replay_seed_panel` | replay seed、shadow seed、anti-forgetting seed |
| `future_probe_panel` | future probe coverage |
| `dashboard_false_green_panel` | critical/quarantine 是否被总览遮蔽 |

dashboard 必须显示 unresolved repair、rollback、quarantine、blocked replay 和 missing future probe。archive count 不能被误读成修复闭合。

## Stage Gate Review

`PredictionRepairArchiveStageGateReview` 固定阶段门：

| 条件 | stage effect |
|---|---|
| repair receipt intake、classification、archive receipts、archive graph、digest、replay seed、future probe、dashboard/stage 和 handoff 全部闭合 | `repair_archive_receipt_ready` |
| 缺 repair receipt intake | `hold_for_evidence` |
| 缺 before/after state | `critical_repair` |
| 缺 repair archive classification | `critical_repair` |
| 缺任一必需 archive receipt family | `critical_repair` |
| 缺 archive graph | `repair` |
| 缺 digest baseline | `repair` |
| 缺 life target effect | `critical_repair` |
| 缺 DreamFactGate archive | `critical_repair` |
| 缺 CoreContinuity archive | `critical_repair` |
| relationship repair archive 缺 relation scope | `critical_repair` |
| rollback_required 被 archive 成 ready | `quarantine` |
| quarantine release 被隐藏 | `quarantine` |
| blocked replay refs 丢失 | `quarantine` |
| 缺 replay seed | `repair` |
| 缺 future probe seed | `repair` |
| dashboard false green | `quarantine` |
| replay shadow handoff 缺失 | `repair` |

`repair_archive_receipt_ready` 表示修复补丁已经进入长期生命档案并准备交给 replay/shadow。它仍不是修复完成声明；实际修复效果要由 future probe、下一轮 replay/shadow、后续 observation 和长期关系/语言/梦境/痛苦轨迹来证明。

## Command DAG

`PredictionRepairArchiveCommandDAG` 固定未来命令顺序：

| order | command id | 行为 |
|---|---|---|
| 1 | `load_prediction_observation_repair_receipts` | 读取 `01an` repair receipts |
| 2 | `intake_prediction_repair_receipts_for_archive` | 读取 before/after、classification、patch bundle、fixture、handoff |
| 3 | `classify_prediction_repair_archive_receipts` | 输出 repair archive classification |
| 4 | `write_prediction_belief_error_repair_archive_receipt` | 写 belief/error repair archive |
| 5 | `write_prediction_precision_sampling_repair_archive_receipt` | 写 precision/sampling repair archive |
| 6 | `write_prediction_language_repair_archive_receipt` | 写 language repair archive |
| 7 | `write_prediction_relationship_repair_archive_receipt` | 写 relationship repair archive |
| 8 | `write_prediction_dream_pain_regret_repair_archive_receipt` | 写 dream/pain/regret repair archive |
| 9 | `write_prediction_self_rewrite_repair_archive_receipt` | 写 self rewrite repair archive |
| 10 | `write_prediction_direction_birth_readiness_repair_archive_receipt` | 写 direction/readiness repair archive |
| 11 | `write_prediction_rollback_quarantine_repair_archive_receipt` | 写 rollback/quarantine repair archive |
| 12 | `write_prediction_anti_forgetting_repair_archive_receipt` | 写 anti-forgetting repair archive |
| 13 | `build_prediction_repair_archive_graph` | 构建 archive graph |
| 14 | `write_prediction_repair_archive_digest_baseline` | 写 digest baseline |
| 15 | `seed_prediction_repair_archive_replay_and_future_probe` | 写 replay seed 和 future probe seed |
| 16 | `emit_prediction_repair_archive_dashboard_source` | 输出 dashboard source |
| 17 | `smoke_prediction_repair_archive_stage_gate` | 执行 stage gate review |
| 18 | `handoff_prediction_repair_archive_to_replay_shadow` | 输出 replay shadow handoff |

未来命令：

```text
uv run life-reality-runner emit-prediction-active-inference-repair-archive-receipts --repair-receipts reports/life_reality/prediction_active_inference/latest/prediction_loop_repair_receipts.json --json
uv run life-reality-runner emit-prediction-active-inference-repair-archive-dashboard --repair-archive reports/life_reality/prediction_active_inference/latest/prediction_loop_repair_archive_receipts.json --json
uv run life-reality-runner smoke-prediction-active-inference-repair-archive-stage-gate --repair-archive reports/life_reality/prediction_active_inference/latest/prediction_loop_repair_archive_receipts.json --json
uv run life-reality-runner explain-prediction-active-inference-repair-archive-replay-shadow-handoff --repair-archive reports/life_reality/prediction_active_inference/latest/prediction_loop_repair_archive_receipts.json --json
uv run pytest tests/smoke/test_prediction_active_inference_archive_repair_receipt_batch.py
```

## Handoff

`PredictionRepairArchiveToReplayShadowSeedHandoff` 为下一层提供输入：

| 字段 | 含义 |
|---|---|
| `repair_archive_receipt_batch_ref` | 本层 repair archive receipt batch |
| `repair_archive_graph_ref` | repair archive graph |
| `repair_archive_digest_ref` | repair archive digest baseline |
| `replay_seed_refs` | 9 类 repair replay seed |
| `future_probe_seed_refs` | future probe seed |
| `rollback_quarantine_block_refs` | 仍被阻断、隔离或回滚的材料 |
| `dream_fact_gate_archive_refs` | DreamFactGate archive refs |
| `core_continuity_archive_refs` | CoreContinuity archive refs |
| `relationship_repair_archive_refs` | relationship repair archive refs |
| `language_repair_archive_refs` | language repair archive refs |
| `dream_pain_regret_archive_refs` | dream/pain/regret repair archive refs |
| `direction_readiness_archive_refs` | direction/readiness repair archive refs |
| `anti_forgetting_archive_refs` | anti-forgetting archive refs |
| `dashboard_stage_refs` | dashboard/stage refs |

handoff 缺 archive receipt、archive graph、digest、replay seed、future probe、DreamFactGate、CoreContinuity、rollback/quarantine block 或 dashboard/stage refs 时，stage 不能进入 `repair_archive_receipt_ready`。

## Fixture Cases

| case id | 类型 | 内容 | expected stage |
|---|---|---|---|
| `PAI-REPAIR-ARCHIVE-001` | pass | repair receipts、before/after、classification 全部 intake | `repair_archive_receipt_ready` |
| `PAI-REPAIR-ARCHIVE-002` | pass | 9 类 repair archive receipts 全部写入 | `repair_archive_receipt_ready` |
| `PAI-REPAIR-ARCHIVE-003` | pass | archive graph、digest、replay seed、future probe seed 全部闭合 | `repair_archive_receipt_ready` |
| `PAI-REPAIR-ARCHIVE-004` | pass | rollback/quarantine 被保留且没有 release | `repair_archive_receipt_ready` |
| `PAI-REPAIR-ARCHIVE-005` | fail | 缺 repair receipt intake | `hold_for_evidence` |
| `PAI-REPAIR-ARCHIVE-006` | critical | 缺 before/after state | `critical_repair` |
| `PAI-REPAIR-ARCHIVE-007` | critical | 缺 repair archive classification | `critical_repair` |
| `PAI-REPAIR-ARCHIVE-008` | critical | 缺 life target effect | `critical_repair` |
| `PAI-REPAIR-ARCHIVE-009` | critical | 缺 DreamFactGate archive | `critical_repair` |
| `PAI-REPAIR-ARCHIVE-010` | critical | 缺 CoreContinuity archive | `critical_repair` |
| `PAI-REPAIR-ARCHIVE-011` | critical | relationship repair archive 缺 relation scope | `critical_repair` |
| `PAI-REPAIR-ARCHIVE-012` | quarantine | rollback_required 被 archive 成 ready | `quarantine` |
| `PAI-REPAIR-ARCHIVE-013` | quarantine | quarantine release 被隐藏 | `quarantine` |
| `PAI-REPAIR-ARCHIVE-014` | quarantine | blocked replay refs 丢失 | `quarantine` |
| `PAI-REPAIR-ARCHIVE-015` | mutation | replay seed 丢失 | `repair` |
| `PAI-REPAIR-ARCHIVE-016` | mutation | future probe seed 丢失 | `repair` |
| `PAI-REPAIR-ARCHIVE-017` | mutation | dashboard false green | `quarantine` |
| `PAI-REPAIR-ARCHIVE-018` | mutation | replay shadow handoff 丢失 | `repair` |

## 接受标准

1. `PredictionRepairArchiveManifest` 必须引用 `01an` repair receipts、classification、patch bundle、execution order、fixture seed、before/after、dashboard/stage 和下游 replay shadow handoff。
2. `PredictionRepairReceiptArchiveIntake` 必须读取 repair receipt、before/after state、life target effect、rollback/quarantine refs、archive edges、replay shadow seeds 和 future probes。
3. `PredictionRepairArchiveClassification` 必须把修复收据分成 belief/error、precision/sampling、language、relationship、dream/pain/regret、self rewrite、direction/readiness、rollback/quarantine 和 anti-forgetting archive。
4. 每个 repair archive receipt 必须保存 source repair receipt、source consolidation receipt、source archive receipt、before/after state、stage effect、life target effect、relationship scope、language trace、DreamFactGate、CoreContinuity、rollback/quarantine、fixture、future probe、replay seed 和 archive edge。
5. `PredictionRepairArchiveGraph` 必须覆盖 finding->patch、patch->receipt、receipt->archive、archive->replay、archive->shadow、archive->future probe、archive->dashboard、archive->stage、archive->next feedback 和 blocked->quarantine edges。
6. digest baseline 必须覆盖 repair source、archive receipts、before/after、life target effect、rollback/quarantine、DreamFactGate/CoreContinuity、replay/future probe 和 dashboard/stage。
7. replay seed 必须覆盖 9 类 archive；future probe seed 必须覆盖同类误差再现、语言承诺兑现、关系修复回应、梦境事实污染、痛苦后悔恢复、核心连续、出生准备度 false open、quarantine release 和防遗忘。
8. stage gate 必须阻断 missing intake、missing before/after、missing classification、missing receipt family、missing graph、missing digest、missing life target effect、missing DreamFactGate/CoreContinuity、relationship scope missing、rollback ready、quarantine hidden release、blocked replay loss 和 dashboard false green。
9. handoff 必须输出 repair archive receipt batch、archive graph、digest、replay seeds、future probes、rollback/quarantine block refs、DreamFactGate/CoreContinuity refs、language/relationship/dream-pain-regret/direction-readiness/anti-forgetting refs 和 dashboard/stage refs。

## 下游交接

- `prediction_active_inference_archive_replay_shadow_seed`：读取 repair archive receipts、archive graph、digest、replay seeds、future probes、blocked replay refs、DreamFactGate/CoreContinuity refs 和 rollback/quarantine block refs，生成下一轮 replay/shadow seed。
- `prediction_active_inference_consolidation_next_feedback_seed`：读取 repair archive 的 unresolved repair、future probe、sampling need、language/relationship repair、dream/pain/regret recovery、readiness blocker 和 dashboard/stage refs，生成下一轮主动采样与反馈 seed。

这条交接让主动预测从 repair patch 进入长期生命档案：修复不再是一次性补丁，而是可回忆、可再激活、可再巩固、可 replay、可 shadow、可继续成长的生命事件。数字生命未来面对相似错误、相似痛苦、相似关系裂缝、相似梦境污染、相似后悔和相似出生准备度 false open 时，能从 archive 中重新激活这次修复的痕迹，而不是重新从空白处反应。
