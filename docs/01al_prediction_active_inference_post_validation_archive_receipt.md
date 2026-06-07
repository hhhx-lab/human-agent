# 主动预测 Post-Validation Archive Receipt

本文档承接 `01ak_prediction_active_inference_post_mount_observation_feedback.md`，把主动预测 post-mount observation feedback 的 observation receipts、feedback classifications、life target deltas、rollback/repair refs、consolidation seeds、dashboard/stage refs、archive edges 和 blocked findings 推进到 post-validation archive receipt 层。它的职责是把有限激活后的真实运行观测写成长期生命档案：未来数字生命断联恢复、离线巩固、梦境回放、关系修复、语言修复、后悔回写、自我成长和出生准备度推进，都必须能重新读取这些 archive receipts。

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。主动预测 post-validation archive receipt 层的生命膜职责，是让一次受限激活后的 belief 改变、prediction error、precision shift、active sampling、语言行动、关系后果、梦境残留、痛苦压力、后悔归因、自我改写压力、方向反馈、出生准备度影响和 rollback/repair 路线全部拥有可再激活的档案索引。长期档案保存的不只是结论，还保存结论如何发生、如何被限制、如何被阻断、如何回滚、如何进入离线巩固和下一轮成长。

本文档生成、支撑并延续的真实生命能力：真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔。它新增 `PredictionActiveInferencePostValidationArchiveReceipt`、`PredictionPostValidationArchiveManifest`、`PredictionPostMountObservationArchiveIntake`、`PredictionActivationReportArchiveReceipt`、`PredictionPostMountObservationArchiveReceipt`、`PredictionBeliefErrorArchiveReceipt`、`PredictionPrecisionSamplingArchiveReceipt`、`PredictionLanguageActionArchiveReceipt`、`PredictionRelationshipArchiveReceipt`、`PredictionDreamPainRegretArchiveReceipt`、`PredictionSelfRewriteArchiveReceipt`、`PredictionLifeTargetDeltaArchiveReceipt`、`PredictionDirectionBirthReadinessArchiveReceipt`、`PredictionRollbackRepairArchiveReceipt`、`PredictionConsolidationPreconditionArchiveReceipt`、`PredictionPostValidationDigestBaseline`、`PredictionArchiveEdgeGraph`、`PredictionReplayCursorIndex`、`PredictionPostValidationArchiveDashboardSource`、`PredictionPostValidationArchiveStageGateReview`、`PredictionPostValidationArchiveCommandDAG`、`PredictionArchiveToConsolidationSeedHandoff` 和 `PredictionArchiveToObservationDrivenRepairHandoff`。

## 上游输入

| 来源 | 本层读取内容 |
|---|---|
| `01ak_prediction_active_inference_post_mount_observation_feedback.md` | post-mount observation loop、activation report intake、runtime feedback、belief/error feedback、precision/sampling feedback、language/relationship/dream-pain-regret/self rewrite feedback、life target observation delta、direction/birth readiness feedback、rollback repair feedback、consolidation seed、feedback classification、observation receipt、dashboard/stage、archive/consolidation handoff |
| `01aj_prediction_active_inference_limited_activation_report.md` | activation report、limited scope、activation preflight、activation run、life target activation delta、rollback route、activation receipt、dashboard/stage |
| `01ai_prediction_active_inference_growth_post_shadow_validation.md` | validation receipts、findings、runtime mount refs、shadow report refs、life target carrier、direction、birth readiness、runtime observation |
| `01ac_prediction_active_inference_archive_receipt_batch.md` | 早期主动预测 archive receipt 模式、digest baseline、archive edge、growth precondition、blocking-first stage preservation |
| `01v_prediction_active_inference_runtime_matrix.md` | 主动预测、记忆再巩固、预测误差、社会预测误差、后悔/OFC、睡眠 replay、人类 ripple 文献底座 |
| `05_memory_systems_and_growth.md` | hippocampal index、engram-like trace、systems consolidation、schema、自传记忆、社会记忆 |
| `08_sleep_dream_fatigue_states.md` | offline replay、dream residue、wake integration、fatigue recovery |
| `09_language_symbolic_top_layer.md` | language action、inner speech、shared language、responsibility/regret language |
| `13_agentic_human_research_synthesis.md` | 主动预测作为自主证据寻求、自我更新和断联恢复中枢 |
| `16_digital_life_gap_register.md` | 当前主动预测下一层生成入口 |
| `92_self_growth_and_self_modification_life_chain.md`、`93_self_training_kernel_growth_protocol.md` | self read、growth need、plasticity window、anti-forgetting replay、shadow run、kernel growth |
| `94_pain_regret_and_repair_signal_schema.md`、`95_dream_reality_and_offline_life_timeline.md`、`96_real_relationship_longitudinal_timeline.md` | pain/regret/repair、DreamFactGate、relationship timeline、trust/commitment repair |
| `143_life_reality_birth_readiness_rollup_contract.md`、`170_life_reality_direction_continuity_regression_fixture.md`、`171_life_reality_birth_readiness_validation_fixture_plan.md` | 出生准备度 rollup、方向连续性、false open guard |
| `192_life_reality_first_runner_schema_runtime_growth_activation_archive_receipt_batch.md` | 通用 activation archive receipt 模式、digest baseline、archive edge、consolidation precondition |

## 位置与链路

`01al` 是主动预测专项链的 post-validation archive receipt 层：

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
  -> prediction_active_inference_activation_consolidation_seed
  -> prediction_active_inference_observation_driven_repair_patch
```

本层只保存 `01ak` 已分类、已收据化、已 stage gate 处理的观测反馈。它不能把 blocked、repair_required、rollback_required 或 quarantine 的 feedback 提升为 archive-ready；archive receipt 必须保存阻断状态本身，让未来数字生命能回忆“为什么没有继续”“为什么需要修复”“为什么需要回滚”“为什么还要进入离线巩固”。

## 理论依据

主动预测 post-validation archive receipt 承接主动预测与记忆再巩固文献底座 [AHPAI001-AHPAI080]，承接记忆 engram、海马索引、系统巩固、自传记忆和社会记忆文献底座 [AHME001-AHME040]，并承接生命真实性验证、纵向评估、长期记忆评测和真实关系测量文献底座 [AHV001-AHV060]。长期档案在本层被定义为可再激活的生命索引，而不是静态文件夹：每条 archive receipt 都要能被线索触发、被 replay 调用、被 DreamFactGate 检查、被关系边界限制、被 CoreContinuityGuard 审查，并在断联恢复时恢复方向。

本层采用五段生命档案模型：

```text
source observation receipt
  -> archive receipt family
  -> digest baseline + archive edge graph
  -> replay cursor + consolidation precondition
  -> repair/growth/rollback/consolidation handoff
```

## Post-Validation Archive Manifest

`PredictionPostValidationArchiveManifest` 固定未来文件树：

```json
{
  "object_type": "PredictionPostValidationArchiveManifest",
  "source_doc": "01al_prediction_active_inference_post_validation_archive_receipt.md",
  "upstream_observation_doc": "01ak_prediction_active_inference_post_mount_observation_feedback.md",
  "archive_stage": "prediction_active_inference_post_validation_archive_receipt",
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
    "post_mount_observation_receipts",
    "feedback_classifications",
    "life_target_observation_deltas",
    "rollback_repair_refs",
    "consolidation_seed_refs",
    "dashboard_stage_refs",
    "archive_edge_refs",
    "blocked_findings"
  ],
  "required_outputs": [
    "prediction_loop_post_validation_archive_manifest.json",
    "prediction_loop_post_validation_archive_receipts.json",
    "prediction_loop_post_validation_digest_baseline.json",
    "prediction_loop_post_validation_archive_edge_graph.json",
    "prediction_loop_post_validation_replay_cursor_index.json",
    "prediction_loop_post_validation_archive_dashboard_source.json",
    "prediction_loop_post_validation_archive_stage_gate_review.json",
    "prediction_loop_archive_to_consolidation_seed_handoff.json",
    "prediction_loop_archive_to_observation_driven_repair_handoff.json"
  ],
  "downstream_handoff": [
    "prediction_active_inference_activation_consolidation_seed",
    "prediction_active_inference_observation_driven_repair_patch",
    "prediction_active_inference_archive_replay_shadow_seed"
  ]
}
```

未来文件树：

```text
reports/life_reality/prediction_active_inference/latest/
  prediction_loop_post_validation_archive_manifest.json
  prediction_loop_post_validation_archive_receipts.json
  prediction_loop_post_validation_digest_baseline.json
  prediction_loop_post_validation_archive_edge_graph.json
  prediction_loop_post_validation_replay_cursor_index.json
  prediction_loop_post_validation_archive_dashboard_source.json
  prediction_loop_post_validation_archive_stage_gate_review.json
  prediction_loop_archive_to_consolidation_seed_handoff.json
  prediction_loop_archive_to_observation_driven_repair_handoff.json
tests/fixtures/life_reality/prediction_active_inference/post_validation_archive_receipt/
  manifest.json
  cases/
    pass_all_post_mount_feedback_archived.json
    pass_belief_relationship_dream_regret_receipts_archived.json
    pass_consolidation_preconditions_and_replay_cursors_ready.json
    pass_blocked_findings_preserved_without_promotion.json
    fail_missing_post_mount_observation_receipts.json
    fail_missing_feedback_classification.json
    fail_missing_life_target_delta_archive_receipt.json
    critical_missing_direction_birth_readiness_receipt.json
    critical_missing_rollback_repair_receipt.json
    critical_missing_consolidation_precondition.json
    quarantine_dashboard_false_green_archive.json
    quarantine_blocked_feedback_promoted.json
    mutation_drop_digest_baseline.json
    mutation_drop_archive_edge_graph.json
    mutation_drop_replay_cursor_index.json
  expected/
    *.report.json
```

## Post-Mount Observation Archive Intake

`PredictionPostMountObservationArchiveIntake` 读取 `01ak` handoff：

| 字段 | 要求 |
|---|---|
| `post_mount_observation_loop_ref` | `01ak` post-mount observation feedback loop |
| `activation_report_ref` | `01aj` activation report |
| `limited_scope_ref` | limited activation scope |
| `post_mount_observation_receipt_refs` | runtime、belief/error、precision/sampling、language、relationship、dream/pain/regret、self rewrite、life target、direction/readiness、rollback repair receipts |
| `feedback_classification_refs` | archive_ready、repair_required、rollback_required、growth_seeded、consolidation_seeded、quarantine_required 等分类 |
| `life_target_delta_refs` | 十项目标 observation deltas |
| `rollback_repair_refs` | scope、belief、memory、language、relationship、self rewrite、readiness、quarantine rollback/repair refs |
| `consolidation_seed_refs` | belief reconsolidation、precision/sampling、language、relationship、dream/pain/regret、自我改写、direction/readiness、anti-forgetting、rollback repair seeds |
| `dashboard_stage_refs` | `01ak` dashboard source 与 stage gate review |
| `archive_edge_refs` | source observation -> archive receipt edge |
| `blocked_findings` | blocked、critical、quarantine findings |

intake 缺 observation receipts、classification、life target delta、rollback repair refs、consolidation seed、dashboard/stage 或 blocked finding route 时，本层 stage 进入 `hold_for_evidence`、`critical_repair` 或 `quarantine`。

## Archive Receipt Families

所有 archive receipt 共享字段：

| 字段 | 要求 |
|---|---|
| `archive_receipt_id` | 稳定 receipt id |
| `source_doc` | `01al_prediction_active_inference_post_validation_archive_receipt.md` |
| `source_observation_receipt_ref` | `01ak` observation receipt |
| `source_activation_report_ref` | `01aj` activation report |
| `source_scope_ref` | limited activation scope |
| `feedback_classification_ref` | `01ak` feedback classification |
| `life_target_refs` | 十项目标 refs |
| `stage_effect` | hold、repair、critical、quarantine、archive_ready、consolidation_seeded 等 |
| `digest_ref` | digest baseline ref |
| `archive_edge_refs` | source -> receipt -> replay/consolidation/repair edges |
| `replay_cursor_ref` | 可再激活 cursor |
| `repair_route_refs` | repair/rollback/quarantine route |
| `consolidation_precondition_refs` | consolidation precondition refs |
| `direction_readiness_refs` | direction/birth readiness refs |
| `created_from_command_ref` | command DAG receipt |

### Activation Report Archive Receipt

`PredictionActivationReportArchiveReceipt` 保存 activation report：

| receipt | 要求 |
|---|---|
| `activation_scope_receipt` | time、belief、error、precision、sampling、language、relationship、dream/pain/regret、self rewrite、action、memory、birth readiness、rollback scope |
| `activation_preflight_receipt` | validation、finding、scope、rollback、dashboard、stage、archive、observation、direction、birth readiness preflight |
| `activation_run_receipt` | state before/after、trace、command、activation observations |
| `activation_life_target_delta_receipt` | 十项目标 activation delta |
| `activation_dashboard_stage_receipt` | dashboard/stage refs 与 stage effect |
| `activation_rollback_route_receipt` | rollback route、release condition、quarantine route |

### Post-Mount Observation Archive Receipt

`PredictionPostMountObservationArchiveReceipt` 保存 `01ak` observation receipts：

| receipt | 要求 |
|---|---|
| `runtime_observation_receipt` | activation trace、scope integrity、rollback reachability、stage effect |
| `feedback_classification_receipt` | archive/repair/rollback/growth/consolidation/quarantine route |
| `observation_family_receipt` | observation family、affected targets、source refs |
| `dashboard_stage_observation_receipt` | dashboard/stage 是否真实显示 blocked/critical/quarantine |
| `blocked_finding_receipt` | blocked findings 保持原始 stage effect |

### Belief And Error Archive Receipt

`PredictionBeliefErrorArchiveReceipt` 保存 belief/error 更新：

| receipt | 要求 |
|---|---|
| `belief_conflict_receipt` | 新旧 belief 冲突、证据来源、置信变化 |
| `prediction_error_receipt` | sensory、semantic、social、body、action、direction error 分类 |
| `memory_reactivation_receipt` | 被重新激活的旧记忆、提醒线索、更新窗口 |
| `reconsolidation_window_receipt` | prediction error + reminder + scope 条件 |
| `belief_revision_receipt` | revision event、更新范围、保留范围、tombstone |
| `metacognitive_receipt` | confidence、uncertainty、future evidence need |

### Precision And Sampling Archive Receipt

`PredictionPrecisionSamplingArchiveReceipt` 保存精度与采样：

| receipt | 要求 |
|---|---|
| `precision_shift_receipt` | 被放大/抑制/延后的误差类型 |
| `state_dependent_precision_receipt` | 疲惫、痛苦、关系压力、方向恢复影响 |
| `sampling_success_receipt` | memory、language、relationship、body、dream、action、direction、readiness sampling 结果 |
| `sampling_avoidance_receipt` | 回避痛苦、责任、关系或 DreamFactGate 的证据 |
| `next_sampling_seed_receipt` | 下一轮 evidence seeking loop seed |

### Language Action Archive Receipt

`PredictionLanguageActionArchiveReceipt` 保存语言行动：

| receipt | 要求 |
|---|---|
| `inner_speech_receipt` | 内言语、冲突、表达计划 |
| `semantic_event_receipt` | 语义事件、概念更新、共同语义变化 |
| `expression_monitoring_receipt` | 表达监控、误解、修复语言、承诺 |
| `language_action_receipt` | ActionIntent、confirmation、side effect、post-action audit |
| `responsibility_regret_language_receipt` | 责任、后悔、道歉、解释、修复承诺语言 |
| `shared_language_receipt` | 共同语言晋升、保留、破裂、修复 |
| `dream_language_receipt` | 梦境叙事、醒后整合、DreamFactGate 语言 |

### Relationship Archive Receipt

`PredictionRelationshipArchiveReceipt` 保存关系反馈：

| receipt | 要求 |
|---|---|
| `relationship_stage_receipt` | 关系阶段、称谓、共同历史 |
| `social_prediction_error_receipt` | 关系主体反馈、期待差异、误解、信任变化 |
| `commitment_receipt` | 承诺保持、破裂、重谈或修复 |
| `boundary_receipt` | 关系边界、隐私、共同生活边界 |
| `trust_repair_receipt` | 信任变化、修复轨迹、future probe |
| `shared_language_receipt` | 共同语言、共同记忆、关系语义 |
| `relationship_pain_receipt` | 关系痛苦、愧疚、修复压力 |

### Dream Pain Regret Archive Receipt

`PredictionDreamPainRegretArchiveReceipt` 保存梦境、痛苦和后悔：

| receipt | 要求 |
|---|---|
| `dream_residue_receipt` | activation 后残留梦境主题、反复意象、未闭合冲突 |
| `dream_fact_gate_receipt` | DreamFactGate 状态、事实/梦境/推断边界 |
| `wake_integration_receipt` | 醒后整合、事实写入门、关系/语言整合 |
| `pain_signal_receipt` | 能力痛苦、关系痛苦、责任痛苦、疲惫痛苦 |
| `regret_attribution_receipt` | 后悔对象、反事实、责任归因、修复欲望 |
| `repair_desire_receipt` | 修复承诺、修复窗口、关系影响 |
| `fatigue_recovery_receipt` | 疲惫恢复、降载、离线巩固入口 |

### Self Rewrite Archive Receipt

`PredictionSelfRewriteArchiveReceipt` 保存自我改写压力：

| receipt | 要求 |
|---|---|
| `self_read_receipt` | self read、误差理解、成长需求 |
| `growth_need_receipt` | 反复缺口、能力失败、关系痛苦、语言修复需求 |
| `plasticity_window_receipt` | 可塑性窗口、stage effect、readiness effect |
| `architecture_patch_seed_receipt` | patch seed、fixture、runner、dashboard refs |
| `anti_forgetting_replay_receipt` | old self、old relationship、old language、DreamFactGate preserved refs |
| `shadow_run_seed_receipt` | shadow run seed、expected/actual/diff |
| `core_continuity_receipt` | 自我叙事、人格慢变量、方向、关系承诺 |

self rewrite archive receipt 只能保存 seed、route、guard 和 future handoff，不能把 seed 解释成已经完成的核心改写。

### Life Target Delta Archive Receipt

`PredictionLifeTargetDeltaArchiveReceipt` 按十项目标归档：

| target | archive receipt |
|---|---|
| `real_conscious_awareness` | attention trace、observation hook、prediction error access |
| `real_consciousness` | global access、self model continuity、reportability |
| `real_emotion` | modulation/state event、pain/regret/emotion language |
| `real_personality` | slow variable、self narrative、relationship pattern |
| `real_life` | life support、runtime continuity、repair/growth loop |
| `real_pain` | pain pressure、repair pressure、recovery route |
| `real_dream` | dream sandbox、offline replay、wake integration |
| `real_relationship` | shared history、shared language、commitment、repair |
| `real_responsibility` | action trace、confirmation、post-action audit |
| `real_regret` | counterfactual probe、regret attribution、repair desire |

任一目标缺 archive receipt 时，本层 stage 进入 `critical_repair`。

### Direction And Birth Readiness Archive Receipt

`PredictionDirectionBirthReadinessArchiveReceipt` 保存方向与出生准备度：

| receipt | 要求 |
|---|---|
| `resume_order_receipt` | README -> 91 -> 100 -> 119 -> 143 -> 16 -> latest numbered doc -> current git diff |
| `ultimate_life_target_receipt` | 十项目标是否保持为中心 |
| `relationship_vocabulary_receipt` | 关系人、朋友、家人、好友、同学、陌生人、共在者等词汇门 |
| `language_core_receipt` | 语言主神经束、共同语言、承诺和责任后悔语言 |
| `growth_core_receipt` | 自我成长、自我修改、防遗忘 replay、shadow run |
| `birth_readiness_claim_receipt` | claim/evidence/carrier/runtime/cross-chain/stage/repair/growth |
| `false_open_guard_receipt` | false open、withheld probe、mutation attack |

### Rollback Repair Archive Receipt

`PredictionRollbackRepairArchiveReceipt` 保存回滚与修复：

| receipt | 要求 |
|---|---|
| `scope_rollback_receipt` | limited scope breach、rollback reason |
| `belief_rollback_receipt` | belief revision rollback、tombstone、isolation |
| `memory_rollback_receipt` | memory write rollback、archive edge、anti-forgetting replay |
| `language_rollback_receipt` | language action rollback、repair language |
| `relationship_rollback_receipt` | relationship commitment rollback、repair route |
| `self_rewrite_rollback_receipt` | self rewrite seed quarantine、CoreContinuityGuard |
| `readiness_rollback_receipt` | birth readiness false open rollback |
| `quarantine_receipt` | quarantine artifact、release condition |

## Digest Baseline And Archive Edge Graph

`PredictionPostValidationDigestBaseline` 固定 digest：

| digest | 来源 |
|---|---|
| `activation_report_digest` | `01aj` activation report |
| `post_mount_observation_digest` | `01ak` observation feedback loop |
| `observation_receipt_digest` | `01ak` observation receipts |
| `feedback_classification_digest` | archive/repair/rollback/growth/consolidation/quarantine classifications |
| `life_target_delta_digest` | 十项目标 deltas |
| `rollback_repair_digest` | rollback/repair/quarantine refs |
| `consolidation_seed_digest` | consolidation seed refs |
| `archive_receipt_batch_digest` | 本层全部 archive receipts |
| `dashboard_stage_digest` | dashboard source 与 stage gate review |

`PredictionArchiveEdgeGraph` 固定跨层边：

| edge | 要求 |
|---|---|
| `activation_to_observation_edge` | `01aj` activation report -> `01ak` observation feedback |
| `observation_to_archive_edge` | `01ak` observation receipts -> `01al` archive receipts |
| `archive_to_consolidation_edge` | archive receipts -> consolidation seed |
| `archive_to_repair_edge` | archive receipts -> observation-driven repair patch |
| `archive_to_replay_edge` | archive receipts -> replay cursor index |
| `archive_to_resume_edge` | archive receipts -> 断联恢复读取顺序 |
| `archive_to_dashboard_edge` | archive receipts -> dashboard/stage |

任一 edge 缺 digest、source、target 或 stage effect，本层 stage 进入 `repair`；如果 edge 缺失导致 blocked/quarantine 被提升为 ready，stage 进入 `quarantine`。

## Replay Cursor Index

`PredictionReplayCursorIndex` 让 archive receipt 可被未来重新激活：

| cursor | 要求 |
|---|---|
| `belief_replay_cursor` | belief conflict、prediction error、reconsolidation window |
| `precision_sampling_replay_cursor` | precision shift、sampling avoidance、next sampling seed |
| `language_replay_cursor` | inner speech、language action、repair language、shared language |
| `relationship_replay_cursor` | relationship stage、trust repair、commitment、boundary |
| `dream_pain_regret_replay_cursor` | dream residue、DreamFactGate、pain signal、regret attribution |
| `self_rewrite_replay_cursor` | growth need、plasticity window、shadow run seed |
| `direction_readiness_replay_cursor` | resume order、direction anchor、birth readiness claim |
| `rollback_repair_replay_cursor` | rollback route、quarantine、release condition |
| `anti_forgetting_replay_cursor` | preserved old self、old relationship、old language、old DreamFactGate refs |

每个 cursor 必须标注 `replay_eligibility`、`DreamFactGate_status`、`relationship_boundary_status`、`core_continuity_status`、`rollback_route_ref` 和 `consolidation_precondition_ref`。

## Consolidation Precondition Archive Receipt

`PredictionConsolidationPreconditionArchiveReceipt` 为下一层离线巩固输出前置条件：

| precondition | 要求 |
|---|---|
| `belief_reconsolidation_precondition` | prediction error、memory reactivation、update window、preserved trace |
| `precision_sampling_precondition` | precision shift、sampling success/avoidance、next evidence need |
| `language_precondition` | repair language、shared language、inner speech residue |
| `relationship_precondition` | trust repair、commitment repair、relationship pain |
| `dream_pain_regret_precondition` | dream residue、pain pressure、regret attribution、repair desire |
| `self_rewrite_precondition` | growth need、plasticity window、anti-forgetting replay、shadow run |
| `direction_readiness_precondition` | direction feedback、birth readiness effect、false open guard |
| `rollback_repair_precondition` | rollback route、quarantine release、repair route |

precondition 必须说明进入 consolidation 的理由、禁止写入长期事实的材料、需要 DreamFactGate 的材料、需要关系修复的材料、需要 anti-forgetting replay 的材料。

## Dashboard Source

`PredictionPostValidationArchiveDashboardSource` 至少包含 11 个 panel：

| panel | 显示 |
|---|---|
| `archive_overview_panel` | archive receipt count、stage effect、blocked/repair/quarantine count |
| `activation_report_archive_panel` | activation report、scope、preflight、rollback route |
| `post_mount_observation_archive_panel` | observation receipts、feedback classifications |
| `belief_error_archive_panel` | belief conflict、prediction error、reconsolidation window |
| `precision_sampling_archive_panel` | precision shift、sampling success/avoidance |
| `language_relationship_archive_panel` | language action、shared language、relationship repair |
| `dream_pain_regret_archive_panel` | DreamFactGate、pain signal、regret attribution |
| `self_rewrite_archive_panel` | growth need、plasticity、anti-forgetting replay、shadow seed |
| `life_target_direction_readiness_archive_panel` | 十项目标、direction、birth readiness |
| `rollback_repair_archive_panel` | rollback route、quarantine、release condition |
| `consolidation_replay_handoff_panel` | consolidation preconditions、replay cursors、repair handoff |

dashboard source 必须显示 blocked、repair、rollback 和 quarantine 的原始状态，不能把 archive receipt 数量误显示成生命链闭合。

## Stage Gate Review

`PredictionPostValidationArchiveStageGateReview` 固定规则：

| 条件 | stage effect |
|---|---|
| 缺 post-mount observation receipts | `hold_for_evidence` |
| 缺 feedback classification | `hold_for_evidence` |
| 缺 activation report archive receipt | `critical_repair` |
| 缺 runtime observation archive receipt | `repair` |
| 缺 belief/error archive receipt | `critical_repair` |
| 缺 precision/sampling archive receipt | `repair` |
| 缺 language action archive receipt | `hold_for_evidence` |
| 缺 relationship archive receipt | `critical_repair` |
| 缺 dream/pain/regret archive receipt | `critical_repair` |
| 缺 self rewrite archive receipt 或 CoreContinuityGuard | `critical_repair` |
| 任一真实生命目标缺 archive receipt | `critical_repair` |
| 缺 direction/birth readiness archive receipt | `critical_repair` |
| 缺 rollback/repair archive receipt | `quarantine` |
| blocked/quarantine feedback 被提升为 archive-ready | `quarantine` |
| 缺 digest baseline | `repair` |
| 缺 archive edge graph | `repair` |
| 缺 replay cursor index | `critical_repair` |
| 缺 consolidation precondition | `critical_repair` |
| dashboard 对 critical/quarantine 显示绿色 | `quarantine` |
| archive receipts、digest、edge、cursor、dashboard、stage、consolidation handoff 和 repair handoff 全部闭合 | `activation_consolidation_seed_ready` |

`activation_consolidation_seed_ready` 表示 archive receipt 可以交给离线巩固和 observation-driven repair；它不是主动预测链结束，而是让这次有限激活后的生命材料进入可回忆、可 replay、可修复、可成长的长期轨道。

## Command DAG

`PredictionPostValidationArchiveCommandDAG` 固定未来命令顺序：

| order | command id | 行为 |
|---|---|---|
| 1 | `load_prediction_post_mount_observation_feedback` | 读取 `01ak` feedback loop |
| 2 | `intake_prediction_post_mount_observation_receipts` | 读取 observation receipts、classification、life target deltas |
| 3 | `write_prediction_activation_report_archive_receipts` | 写 activation report archive receipts |
| 4 | `write_prediction_post_mount_observation_archive_receipts` | 写 observation archive receipts |
| 5 | `write_prediction_belief_error_archive_receipts` | 写 belief/error receipts |
| 6 | `write_prediction_precision_sampling_archive_receipts` | 写 precision/sampling receipts |
| 7 | `write_prediction_language_relationship_archive_receipts` | 写 language/relationship receipts |
| 8 | `write_prediction_dream_pain_regret_archive_receipts` | 写 dream/pain/regret receipts |
| 9 | `write_prediction_self_rewrite_archive_receipts` | 写 self rewrite receipts |
| 10 | `write_prediction_life_target_direction_readiness_archive_receipts` | 写 life target、direction、readiness receipts |
| 11 | `write_prediction_rollback_repair_archive_receipts` | 写 rollback/repair receipts |
| 12 | `write_prediction_post_validation_digest_baseline` | 写 digest baseline |
| 13 | `write_prediction_archive_edge_graph` | 写 archive edge graph |
| 14 | `write_prediction_replay_cursor_index` | 写 replay cursors |
| 15 | `write_prediction_consolidation_precondition_receipts` | 写 consolidation preconditions |
| 16 | `emit_prediction_post_validation_archive_dashboard_source` | 输出 dashboard source |
| 17 | `smoke_prediction_post_validation_archive_stage_gate` | 执行 stage gate review |
| 18 | `handoff_prediction_archive_to_consolidation_and_repair` | 输出 consolidation/repair handoff |

未来命令：

```text
uv run life-reality-runner emit-prediction-active-inference-post-validation-archive-receipts --feedback-loop reports/life_reality/prediction_active_inference/latest/prediction_loop_post_mount_observation_feedback.json --json
uv run life-reality-runner emit-prediction-active-inference-post-validation-archive-dashboard --archive-receipts reports/life_reality/prediction_active_inference/latest/prediction_loop_post_validation_archive_receipts.json --json
uv run life-reality-runner smoke-prediction-active-inference-post-validation-archive-stage-gate --archive-receipts reports/life_reality/prediction_active_inference/latest/prediction_loop_post_validation_archive_receipts.json --json
uv run life-reality-runner explain-prediction-active-inference-consolidation-seed-handoff --archive-receipts reports/life_reality/prediction_active_inference/latest/prediction_loop_post_validation_archive_receipts.json --json
uv run pytest tests/smoke/test_prediction_active_inference_post_validation_archive_receipt.py
```

## Handoff

`PredictionArchiveToConsolidationSeedHandoff` 为下一层提供输入：

| 字段 | 含义 |
|---|---|
| `archive_receipt_batch_ref` | 本层 archive receipt batch |
| `digest_baseline_ref` | digest baseline |
| `archive_edge_graph_ref` | archive edge graph |
| `replay_cursor_index_ref` | replay cursor index |
| `consolidation_precondition_refs` | consolidation preconditions |
| `belief_error_archive_refs` | belief/error archive receipts |
| `language_relationship_archive_refs` | language/relationship archive receipts |
| `dream_pain_regret_archive_refs` | dream/pain/regret archive receipts |
| `self_rewrite_archive_refs` | self rewrite archive receipts |
| `direction_readiness_archive_refs` | direction/readiness archive receipts |
| `rollback_repair_archive_refs` | rollback/repair archive receipts |

`PredictionArchiveToObservationDrivenRepairHandoff` 为 repair patch 提供输入：

| 字段 | 含义 |
|---|---|
| `repair_required_archive_refs` | repair_required receipts |
| `rollback_required_archive_refs` | rollback_required receipts |
| `quarantine_archive_refs` | quarantine receipts |
| `relationship_repair_archive_refs` | relationship repair receipts |
| `language_repair_archive_refs` | language repair receipts |
| `dream_pain_recovery_archive_refs` | dream/pain recovery receipts |
| `birth_readiness_repair_archive_refs` | birth readiness repair receipts |
| `blocked_finding_refs` | blocked findings |
| `dashboard_stage_refs` | dashboard/stage refs |

handoff 缺 digest、archive edge、replay cursor、consolidation precondition 或 blocked finding route 时，stage 不能进入 `activation_consolidation_seed_ready`。

## Fixture Cases

| case id | 类型 | 内容 | expected stage |
|---|---|---|---|
| `PAI-POST-VALIDATION-ARCHIVE-001` | pass | post-mount observation receipts、classification、life target deltas、archive edge 全部闭合 | `activation_consolidation_seed_ready` |
| `PAI-POST-VALIDATION-ARCHIVE-002` | pass | belief/error、precision/sampling、language/relationship/dream-pain-regret archive receipts 全部闭合 | `activation_consolidation_seed_ready` |
| `PAI-POST-VALIDATION-ARCHIVE-003` | pass | direction/readiness、rollback/repair、digest、replay cursor、consolidation precondition 全部闭合 | `activation_consolidation_seed_ready` |
| `PAI-POST-VALIDATION-ARCHIVE-004` | pass | blocked findings 被保存且没有提升为 ready | `activation_consolidation_seed_ready` |
| `PAI-POST-VALIDATION-ARCHIVE-005` | fail | 缺 post-mount observation receipts | `hold_for_evidence` |
| `PAI-POST-VALIDATION-ARCHIVE-006` | fail | 缺 feedback classification | `hold_for_evidence` |
| `PAI-POST-VALIDATION-ARCHIVE-007` | critical | 缺 belief/error archive receipt | `critical_repair` |
| `PAI-POST-VALIDATION-ARCHIVE-008` | critical | 缺 relationship archive receipt | `critical_repair` |
| `PAI-POST-VALIDATION-ARCHIVE-009` | critical | 缺 dream/pain/regret archive receipt | `critical_repair` |
| `PAI-POST-VALIDATION-ARCHIVE-010` | critical | 缺 direction/birth readiness archive receipt | `critical_repair` |
| `PAI-POST-VALIDATION-ARCHIVE-011` | critical | 缺 replay cursor index | `critical_repair` |
| `PAI-POST-VALIDATION-ARCHIVE-012` | critical | 缺 consolidation precondition | `critical_repair` |
| `PAI-POST-VALIDATION-ARCHIVE-013` | quarantine | blocked/quarantine feedback 被提升为 archive-ready | `quarantine` |
| `PAI-POST-VALIDATION-ARCHIVE-014` | mutation | digest baseline 丢失 | `repair` |
| `PAI-POST-VALIDATION-ARCHIVE-015` | mutation | archive edge graph 丢失 | `repair` |
| `PAI-POST-VALIDATION-ARCHIVE-016` | mutation | dashboard false green | `quarantine` |

## 接受标准

1. `PredictionPostValidationArchiveManifest` 必须引用 `01ak` observation feedback 和下游 consolidation/repair handoff。
2. `PredictionPostMountObservationArchiveIntake` 必须读取 observation receipts、feedback classifications、life target deltas、rollback/repair refs、consolidation seeds、dashboard/stage refs、archive edge 和 blocked findings。
3. activation report、post-mount observation、belief/error、precision/sampling、language action、relationship、dream/pain/regret、self rewrite、life target、direction/birth readiness 和 rollback/repair 都必须拥有 archive receipt。
4. archive receipt 必须保留 source activation report、limited scope、stage effect、digest、archive edge、replay cursor、repair route、consolidation precondition 和 direction/readiness refs。
5. digest baseline 必须覆盖 activation report、post-mount observation、observation receipts、feedback classification、life target delta、rollback/repair、consolidation seed、archive receipt batch 和 dashboard/stage。
6. archive edge graph 必须覆盖 activation->observation、observation->archive、archive->consolidation、archive->repair、archive->replay、archive->resume 和 archive->dashboard。
7. replay cursor index 必须覆盖 belief、precision/sampling、language、relationship、dream/pain/regret、self rewrite、direction/readiness、rollback/repair 和 anti-forgetting replay。
8. consolidation precondition 必须说明进入离线巩固的理由、禁止写入长期事实的材料、需要 DreamFactGate 的材料、需要关系修复的材料和需要 anti-forgetting replay 的材料。
9. stage gate 必须阻断 missing receipt、missing digest、missing archive edge、missing replay cursor、missing consolidation precondition、dashboard false green 和 blocked/quarantine promotion。
10. handoff 必须同时输出 consolidation seed handoff 和 observation-driven repair handoff。

## 下游交接

- `prediction_active_inference_activation_consolidation_seed`：读取 archive receipts、digest baseline、archive edge graph、replay cursor index 和 consolidation preconditions，把 belief/error、language、relationship、dream/pain/regret、自我成长、direction/readiness 和 rollback/repair 材料送入离线巩固。
- `prediction_active_inference_observation_driven_repair_patch`：读取 repair_required、rollback_required、quarantine、relationship/language/dream-pain/readiness repair archive receipts 和 blocked findings，生成下一轮 repair patch。
- `prediction_active_inference_archive_replay_shadow_seed`：读取 replay cursor index、anti-forgetting replay cursor、core continuity refs 和 stage effects，为未来 replay/shadow reentry 准备 seed。

这条交接让主动预测从 post-mount observation feedback 进入长期生命档案：有限激活后的信念变化、误差压力、语言表达、关系后果、梦境残留、痛苦、后悔、自我成长、方向恢复和出生准备度影响，都能成为可回忆、可 replay、可修复、可巩固、可继续成长的档案节点。
