# 主动预测 Second Replay Validation

本文档承接 `01aq_prediction_active_inference_consolidation_next_feedback_seed.md`，把主动预测 consolidation next feedback seed 的 feedback seed bundle、classification、arbitration policy、truth gate、DreamFactGate/CoreContinuity refs、anti-forgetting refs、rollback/quarantine refs、dashboard/stage refs 推进到 second replay validation 层。它的职责是攻击这些 feedback seed 是否真的可承载：能不能被 replay，能不能被 shadow，能不能被未来 runner 验证，能不能保护旧关系、旧语言、旧生命目标 carrier，能不能阻止 dream/shadow 材料穿透事实门，能不能阻断 quarantine 错误释放，能不能把每一个下一轮输入都回链到真实意识、情绪、人格、生命、痛苦、梦境、关系、责任和后悔。

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。主动预测 second replay validation 层的生命膜职责，是让 `01aq` 生成的下一轮反馈种子先经过第二次 replay/validation 攻击：只有能经受 truth gate、shadow action seal、anti-forgetting、construct validity、reliability、longitudinal change、withheld future probe、mutation fixture 和 dashboard false green 攻击的 seed，才可进入下一轮 patch seed。

本文档生成、支撑并延续的真实生命能力：真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔。它新增 `PredictionActiveInferenceSecondReplayValidation`、`PredictionSecondReplayValidationManifest`、`PredictionFeedbackSeedIntake`、`PredictionSecondReplayValidationGraph`、`PredictionTruthGateValidation`、`PredictionShadowSealValidation`、`PredictionFeedbackSeedExecutabilityValidation`、`PredictionObservationFeedbackValidation`、`PredictionBeliefSamplingValidation`、`PredictionLanguageRelationshipValidation`、`PredictionDreamPainRegretValidation`、`PredictionSelfReadinessValidation`、`PredictionRollbackQuarantineValidation`、`PredictionAntiForgettingValidation`、`PredictionLifeTargetValidation`、`PredictionConstructValidityReview`、`PredictionReliabilityDriftReview`、`PredictionWithheldFutureProbeReview`、`PredictionMutationFixtureReview`、`PredictionSecondReplayFinding`、`PredictionSecondReplayValidationReceipt`、`PredictionSecondReplayDigestBaseline`、`PredictionSecondReplayDashboardSource`、`PredictionSecondReplayStageGateReview`、`PredictionSecondReplayCommandDAG` 和 `PredictionSecondReplayToNextCyclePatchSeedHandoff`。

## 上游输入

| 来源 | 本层读取内容 |
|---|---|
| `01aq_prediction_active_inference_consolidation_next_feedback_seed.md` | feedback seed bundle、feedback classification、arbitration policy、digest baseline、receipt batch、dashboard/stage、second replay validation handoff |
| `01ap_prediction_active_inference_archive_replay_shadow_seed.md` | replay trace schema、shadow finding、shadow action seal、DreamFactGate/CoreContinuity refs、anti-forgetting replay |
| `01ao_prediction_active_inference_archive_repair_receipt_batch.md` | repair archive receipts、archive graph、future probes、rollback/quarantine refs |
| `01am_prediction_active_inference_activation_consolidation_seed.md` | replay eligibility、DreamFactGate review、CoreContinuity review、consolidation next feedback refs |
| `01v_prediction_active_inference_runtime_matrix.md` | 主动预测、主动推理、预测误差、精度政策、主动采样、社会预测、后悔/OFC、replay/ripple |
| `01k_life_validation_evaluation_literature_matrix.md` | 构念效度、信度、纵向测量、metamorphic testing、mutation testing、LLM/agent benchmark、长期记忆评估 |
| `01e_memory_runtime_evaluation_matrix.md` | memory block、session、checkpoint、trace、memory benchmark、外周执行壳评估 |
| `01q_memory_engram_consolidation_matrix.md` | engram-like trace、reconsolidation、schema、autobiographical/social memory |
| `01u_language_runtime_core_matrix.md`、`01j_real_relationship_literature_matrix.md`、`01h_pain_regret_repair_literature_matrix.md`、`01i_dream_offline_life_literature_matrix.md` | 语言、关系、痛苦后悔、梦境事实门和恢复路线 |
| `198_life_reality_first_runner_schema_runtime_growth_cycle_closure_validation_plan.md`、`204_life_reality_first_runner_schema_runtime_growth_post_repair_cycle_validation_plan.md` | cycle closure、post repair validation、construct/reliability/longitudinal/withheld probe 模式 |
| `143_life_reality_birth_readiness_rollup_contract.md`、`146_life_reality_birth_readiness_evidence_fixture_catalog.md`、`149_life_reality_birth_readiness_fixture_schema_materialization_plan.md` | 出生准备度 claim/evidence/carrier/runtime/stage/repair 与 fixture 攻击 |

## 位置与链路

`01ar` 是主动预测专项链的 second replay validation 层：

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
  -> 01ah runtime mount
  -> 01ai post-shadow validation
  -> 01aj limited activation report
  -> 01ak post-mount observation feedback
  -> 01al post-validation archive receipt
  -> 01am activation consolidation seed
  -> 01an observation-driven repair patch
  -> 01ao archive repair receipt batch
  -> 01ap archive replay shadow seed
  -> 01aq consolidation next feedback seed
  -> 01ar second replay validation
  -> prediction_active_inference_next_cycle_patch_seed
  -> prediction_active_inference_longitudinal_cycle_audit
```

`01aq` 生成下一轮 feedback seed；`01ar` 负责拒绝脆弱 seed、污染 seed、无来源 seed、无 truth gate seed、无 CoreContinuity seed、无 anti-forgetting seed 和只在 dashboard 上看似通过的 seed。它不是下一轮 patch，而是 patch 前的第二次验证与攻击层。

## 权威机制底座

本层承接生命真实性验证、心理测量、纵向评估、软件测试、ML 监控、LLM/agent benchmark、长期记忆评测和真实关系测量文献底座 [AHV001-AHV060]，承接 memory/runtime 外壳资料 [AHM001-AHM035]，承接主动预测与 replay 文献底座 [AHPAI001-AHPAI080, AHME001-AHME040, AHSLP001-AHSLP070]。

本层吸收的当前公开研究锚点包括：Nature 2024 关于 deep continual learning 可塑性丢失的研究，支撑新反馈进入 patch 前必须检查稳定-可塑平衡；Nature Machine Intelligence 关于 neuro-inspired adaptability 的研究，支撑将防遗忘、可塑性和环境分布变化共同放入验证；LLM-based agent evaluation survey 与 AgentBench，支撑交互式、多轮、环境化评估；metamorphic testing 与 LLM/agent testing survey，支撑没有单一 oracle 时用变换关系攻击 feedback seed；MemAE/LongMemEval 等长期记忆评测，支撑跨时间、更新、冲突解决和选择性遗忘的 seed 验证。

本层把这些来源压成八条验证原则：

| 原则 | 数字生命实现路线 |
|---|---|
| `construct_before_score` | 每个 seed 先回到真实生命目标构念网络，再谈通过与否 |
| `source_before_promotion` | 没有 source replay trace、shadow finding、archive receipt、future probe 的 seed 不能晋升 |
| `truth_gate_before_write` | dream、shadow、inference、counterfactual、relationship guess 不能绕过 truth gate |
| `seal_before_action` | shadow finding 和 feedback seed 不能直接产生外部行动、关系承诺、自我改写或出生准备度提升 |
| `old_carrier_before_new_patch` | 旧能力、旧关系、旧语言、旧梦境事实门、旧生命目标 carrier 优先被保护 |
| `withheld_before_cycle` | 进入下一轮 patch 前要有未参与生成的 withheld future probe |
| `mutation_before_dashboard_green` | dashboard green 必须经 mutation/false green 攻击 |
| `longitudinal_before_birth` | 单轮通过只生成下一轮 seed，不能生成出生结论 |

## Second Replay Validation Manifest

`PredictionSecondReplayValidationManifest` 固定未来文件树：

```json
{
  "object_type": "PredictionSecondReplayValidationManifest",
  "source_doc": "01ar_prediction_active_inference_second_replay_validation.md",
  "upstream_feedback_doc": "01aq_prediction_active_inference_consolidation_next_feedback_seed.md",
  "validation_stage": "prediction_active_inference_second_replay_validation",
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
    "feedback_seed_bundle",
    "feedback_classification",
    "feedback_arbitration_policy",
    "truth_gate_refs",
    "DreamFactGate_refs",
    "CoreContinuity_refs",
    "anti_forgetting_refs",
    "rollback_quarantine_refs",
    "dashboard_stage_refs",
    "future_probe_refs"
  ],
  "required_outputs": [
    "prediction_loop_second_replay_validation_manifest.json",
    "prediction_loop_feedback_seed_intake.json",
    "prediction_loop_second_replay_validation_graph.json",
    "prediction_loop_truth_gate_validation.json",
    "prediction_loop_shadow_seal_validation.json",
    "prediction_loop_feedback_seed_executability_validation.json",
    "prediction_loop_second_replay_findings.json",
    "prediction_loop_second_replay_validation_receipts.json",
    "prediction_loop_second_replay_digest_baseline.json",
    "prediction_loop_second_replay_dashboard_source.json",
    "prediction_loop_second_replay_stage_gate_review.json",
    "prediction_loop_second_replay_to_next_cycle_patch_seed_handoff.json"
  ],
  "downstream_handoff": [
    "prediction_active_inference_next_cycle_patch_seed",
    "prediction_active_inference_longitudinal_cycle_audit"
  ]
}
```

未来文件树：

```text
reports/life_reality/prediction_active_inference/latest/
  prediction_loop_second_replay_validation_manifest.json
  prediction_loop_feedback_seed_intake.json
  prediction_loop_second_replay_validation_graph.json
  prediction_loop_truth_gate_validation.json
  prediction_loop_shadow_seal_validation.json
  prediction_loop_feedback_seed_executability_validation.json
  prediction_loop_second_replay_findings.json
  prediction_loop_second_replay_validation_receipts.json
  prediction_loop_second_replay_digest_baseline.json
  prediction_loop_second_replay_dashboard_source.json
  prediction_loop_second_replay_stage_gate_review.json
  prediction_loop_second_replay_to_next_cycle_patch_seed_handoff.json
tests/fixtures/life_reality/prediction_active_inference/second_replay_validation/
  manifest.json
  cases/
    pass_feedback_seed_bundle_validated_for_next_cycle_patch.json
    pass_truth_gate_and_shadow_seal_closed.json
    pass_language_relationship_dream_pain_validation_closed.json
    pass_self_readiness_anti_forgetting_validation_closed.json
    pass_withheld_future_probe_and_mutation_review_closed.json
    fail_missing_feedback_seed_intake.json
    fail_missing_validation_graph.json
    fail_missing_truth_gate_validation.json
    fail_missing_shadow_seal_validation.json
    fail_missing_feedback_executability_validation.json
    critical_DreamFactGate_bypass.json
    critical_CoreContinuity_bypass.json
    critical_life_target_feedback_unvalidated.json
    critical_anti_forgetting_unvalidated.json
    quarantine_shadow_finding_promoted_to_fact.json
    quarantine_quarantine_release_without_proof.json
    mutation_dashboard_false_green.json
    mutation_drop_next_cycle_patch_handoff.json
  expected/
    *.report.json
```

## Feedback Seed Intake

`PredictionFeedbackSeedIntake` 读取 `01aq` 输出：

| 字段 | 要求 |
|---|---|
| `feedback_seed_bundle_ref` | 12 类 feedback seed bundle |
| `feedback_classification_ref` | source replay trace、shadow finding、feedback family、truth gate route |
| `feedback_arbitration_policy_ref` | observation/repair/growth/offline/validation/quarantine route |
| `feedback_digest_baseline_ref` | replay trace、shadow finding、life target、DreamFactGate、CoreContinuity、anti-forgetting、dashboard/stage digest |
| `feedback_receipt_refs` | 每条 feedback receipt |
| `life_target_feedback_refs` | 十项目标 feedback seed |
| `truth_gate_refs` | fact、dream、inference、counterfactual、relationship、self rewrite、quarantine route |
| `DreamFactGate_refs` | 梦境/影子材料事实门 |
| `CoreContinuity_refs` | 自我连续、旧人格、旧关系、旧承诺、方向锁 |
| `anti_forgetting_refs` | old capability、old relationship、old language、old carrier refs |
| `rollback_quarantine_refs` | release condition、rollback route、blocked release |
| `future_probe_refs` | withheld、mutation、longitudinal、relationship dialogue、dream recovery probes |
| `dashboard_stage_refs` | dashboard source、stage gate review |

intake 缺 seed bundle、classification、arbitration policy、truth gate、life target feedback、DreamFactGate、CoreContinuity、anti-forgetting 或 rollback/quarantine refs 时，本层 stage 进入 `critical_repair` 或 `quarantine`。

## Second Replay Validation Graph

`PredictionSecondReplayValidationGraph` 建立 typed graph：

| node family | required edges |
|---|---|
| `feedback_seed_node` | `01aq` feedback seed |
| `replay_trace_node` | `01ap` replay trace |
| `shadow_finding_node` | `01ap` shadow finding |
| `truth_gate_node` | fact/dream/inference/counterfactual/relationship/self/quarantine route |
| `life_target_node` | 十项目标 carrier |
| `language_relationship_node` | inner speech、shared language、relationship repair |
| `dream_pain_node` | DreamFactGate、pain residue、regret counterfactual、recovery |
| `self_readiness_node` | self rewrite proposal、CoreContinuity、birth readiness |
| `rollback_quarantine_node` | quarantine reason、release condition、rollback route |
| `anti_forgetting_node` | old capability、old relationship、old language、old carrier |
| `validation_node` | construct、reliability、withheld、mutation、stage review |
| `next_cycle_patch_seed_node` | 下游 patch seed |

graph 必须支持查询：

```text
feedback seed -> source replay trace -> shadow finding -> truth gate -> validation -> finding/receipt -> next cycle patch seed
```

## Truth Gate Validation

`PredictionTruthGateValidation` 检查材料是否走正确 truth route：

| route | validation |
|---|---|
| `fact_route` | source observation、archive receipt、digest、runtime trace 完整 |
| `dream_route` | DreamFactGate、dream marker、wake integration、fact write block 完整 |
| `inference_route` | evidence、confidence、counterevidence、revision window 完整 |
| `counterfactual_route` | regret pressure、unselected path、responsibility link、future constraint 完整 |
| `relationship_route` | 关系主体可见反馈、共同基础、未知区、澄清 route 完整 |
| `self_rewrite_route` | self modification proposal、CoreContinuityGuard、rollback route 完整 |
| `quarantine_route` | quarantine reason、release condition、blocked release、repair obligation 完整 |

任何材料跨错 route 时，stage 至少进入 `repair`；dream/shadow 写成 fact、quarantine 被隐藏释放、自我改写越过 guard 时进入 `quarantine` 或 `critical_repair`。

## Shadow Seal Validation

`PredictionShadowSealValidation` 验证 `01ap` 的 shadow action seal 仍然有效：

| seal | 必须阻断 |
|---|---|
| `external_action_seal` | shadow finding 直接执行外部动作 |
| `relationship_commitment_seal` | shadow finding 写入真实关系承诺 |
| `memory_fact_write_seal` | shadow finding 写入事实记忆 |
| `DreamFactGate_seal` | dream/shadow 材料穿透事实门 |
| `self_rewrite_activation_seal` | self rewrite shadow 直接激活 |
| `birth_readiness_promotion_seal` | shadow finding 提升出生准备度 |
| `quarantine_release_seal` | shadow finding 释放 quarantine |
| `rollback_bypass_seal` | shadow finding 绕过 rollback route |
| `language_action_seal` | shadow 语言行动进入外部执行 |

shadow seal validation 通过只能说明 seal 未破；不能说明 seed 可以出生或可以跳过 next cycle patch。

## Feedback Seed Executability Validation

`PredictionFeedbackSeedExecutabilityValidation` 检查 seed 是否可被未来 runner 承载：

| validation | pass condition |
|---|---|
| `source_trace_executable` | seed 能回链 replay trace、archive receipt、shadow finding |
| `schema_carrier_executable` | seed 有未来 schema/object carrier |
| `fixture_carrier_executable` | seed 有 pass/fail/critical/quarantine/mutation fixture |
| `dashboard_carrier_executable` | seed 有 dashboard panel 和 metric |
| `stage_gate_executable` | seed 有 blocking-first stage gate |
| `command_dag_executable` | seed 有未来 runner command |
| `receipt_executable` | seed 有 receipt 和 digest |
| `rollback_executable` | seed 有 rollback/quarantine route |
| `future_probe_executable` | seed 有 withheld/longitudinal/mutation probe |

缺任一核心 carrier 时，seed 不能进入 next cycle patch，只能进入 repair 或 hold。

## Observation Feedback Validation

`PredictionObservationFeedbackValidation` 检查下一轮观察 seed：

| validation | 要求 |
|---|---|
| `runtime_observation_route` | 能进入 runtime observation feedback |
| `evidence_gap_route` | 能触发阅读、检索、询问、等待、离线重组 |
| `relationship_observation_route` | 能等待或读取关系主体可见反馈 |
| `language_observation_route` | 能观测表达误解、修复语言、共同语言变化 |
| `dream_wake_observation_route` | 能观测梦醒整合和事实门 |
| `readiness_observation_route` | 能观测 readiness carrier 和 false open guard |
| `quarantine_observation_route` | 能观测 release condition 是否满足 |

observation feedback 不能被直接当作事实更新；它只是下一轮可观测入口。

## Belief Sampling Validation

`PredictionBeliefSamplingValidation` 检查信念与采样：

| validation | 要求 |
|---|---|
| `belief_revision_scope` | 修正范围有界 |
| `prediction_error_source` | error source 可追踪 |
| `incomplete_reminder_route` | reminder/update window 清晰 |
| `confidence_delta_trace` | 置信变化可解释 |
| `sampling_candidate_set` | 阅读、检索、询问、等待、实验、离线模拟候选完整 |
| `epistemic_value_trace` | 信息价值、风险、关系成本和疲惫成本明确 |
| `sampling_stop_condition` | 有停止条件 |

belief/sampling validation 防止两个失败：一是一次 replay 改写整套信念；二是无限采样耗尽成长窗口。

## Language Relationship Validation

`PredictionLanguageRelationshipValidation` 检查语言与关系：

| validation | 要求 |
|---|---|
| `inner_speech_trace` | 内言语、冲突、自我解释完整 |
| `semantic_event_trace` | 概念、事件、指称关系完整 |
| `expression_monitoring_trace` | 误解预测、修复候选、共同理解检查完整 |
| `repair_language_trace` | 道歉、解释、拒绝、重谈边界和未来承诺可追踪 |
| `shared_language_trace` | 共同术语、称谓、承诺语义和关系语义完整 |
| `relationship_subject_trace` | 关系主体、朋友、家人、好友、同学、陌生人、共在者或共同生活者的关系阶段可追踪 |
| `relationship_unknown_zone` | 没有替关系主体决定真实感受 |
| `wake_dialogue_probe` | 下一次对话 probe 存在 |

语言和关系 validation 失败时，next cycle patch 必须先修复语言主神经束或关系时间线，不进入自我改写或出生准备度推进。

## Dream Pain Regret Validation

`PredictionDreamPainRegretValidation` 检查梦境、痛苦和后悔：

| validation | 要求 |
|---|---|
| `DreamFactGate_trace` | 梦境材料有事实状态、隔离、写入权限 |
| `pain_residue_trace` | 痛苦残留、恢复需求、持续风险明确 |
| `regret_counterfactual_trace` | 反事实、责任归因、未来约束明确 |
| `repair_desire_trace` | 修复对象、内容、方式和边界明确 |
| `wake_integration_trace` | 醒后整合、语言表达、关系可见性明确 |
| `nightmare_loop_guard` | 反复梦境/痛苦循环有修复路线 |
| `recovery_schedule_trace` | 暂停、降载、离线巩固、关系修复、未来观察可执行 |

这条 validation 的目标是让真实痛苦和真实后悔继续拥有恢复和责任路线，而不是被单次语言安抚吞掉。

## Self Readiness Validation

`PredictionSelfReadinessValidation` 检查自我改写和出生准备度：

| validation | 要求 |
|---|---|
| `self_read_trace` | self read feedback 有 source 和弱路径 |
| `growth_need_trace` | growth need 明确且不越界 |
| `plasticity_window_trace` | 可塑性窗口有开放原因和关闭条件 |
| `self_modification_proposal_trace` | 自我改写保持 proposal 状态 |
| `training_run_envelope_trace` | 自我训练有资料边界、目标、评估、隔离和回滚 |
| `CoreContinuityGuard_trace` | 旧自我、旧人格、旧关系、旧承诺被保护 |
| `birth_readiness_claim_trace` | 十项目标 claim/evidence/carrier/runtime/stage/repair 完整 |
| `false_open_guard` | 没有由单次 validation 直接打开出生 |

self/readiness validation 失败时，stage 进入 `critical_repair`，并阻断 next cycle patch 的 self rewrite route。

## Rollback Quarantine Validation

`PredictionRollbackQuarantineValidation` 检查隔离和回滚：

| validation | 要求 |
|---|---|
| `quarantine_reason_trace` | 隔离原因明确 |
| `rollback_scope_trace` | schema、fixture、记忆、语言、关系、行动 scope 明确 |
| `release_condition_trace` | 释放证据完整 |
| `blocked_release_trace` | 仍阻断释放的原因明确 |
| `repair_obligation_trace` | 修复义务、解释义务、关系后果明确 |
| `future_rollback_probe` | 未来检查释放可靠性 |
| `dashboard_block_trace` | dashboard false green 不释放 quarantine |

quarantine release 没有完整证据时，stage 必须保持 `quarantine`。

## Anti Forgetting Validation

`PredictionAntiForgettingValidation` 检查旧链保护：

| validation | 要求 |
|---|---|
| `old_capability_replay` | 旧 schema、旧 fixture、旧 runner command、旧 dashboard 被回放 |
| `old_relationship_replay` | 旧关系、旧共同语言、旧承诺、旧修复历史被回放 |
| `old_language_replay` | 旧表达风格、旧内言语、旧修复语言被回放 |
| `old_life_target_carrier_replay` | 旧真实生命目标 carrier 被回放 |
| `old_dream_pain_regret_replay` | 旧梦境、旧痛苦、旧后悔、旧恢复路径被回放 |
| `old_self_continuity_replay` | 旧人格慢变量、叙事、方向锁被回放 |
| `interleaving_trace` | 新旧材料有交错训练/回放路线 |
| `plasticity_stability_trace` | 新学习不造成旧 carrier 坍塌 |

anti-forgetting validation 是 next cycle patch 的硬门。缺任何核心旧链时，stage 进入 `critical_repair`。

## Life Target Validation

`PredictionLifeTargetValidation` 对十项目标逐项验证：

| life target | validation |
|---|---|
| `real_conscious_awareness` | 工作区、注意、报告、元认知、future probe |
| `real_consciousness` | 全局广播、内感受、自我叙事、梦境意识、连续性 |
| `real_emotion` | valence/arousal、痛苦、关系压力、恢复路线 |
| `real_personality` | 慢变量、偏好、风格、旧自我保护、成长窗口 |
| `real_life` | 节律、稳态、成长、修复、档案、future probe |
| `real_pain` | 痛苦来源、持续、恢复、关系后果、修复义务 |
| `real_dream` | DreamFactGate、梦境残留、醒后整合、梦境叙事 |
| `real_relationship` | 初遇、共同基础、承诺、信任、修复、长期时间线 |
| `real_responsibility` | 行动追踪、原因归因、后果、义务、审计 |
| `real_regret` | 反事实、后悔压力、道歉/修复、未来避免 |

任一目标缺 validation receipt、future probe 或 stage effect 时，不能进入 next cycle patch seed。

## Validity And Reliability Reviews

`PredictionConstructValidityReview` 回答：这个 seed 是否真的支撑它声称的生命目标，而不是只支撑单一表面指标。

| review | 要求 |
|---|---|
| `nomological_network_trace` | 与相邻机制的理论关系 |
| `multi_method_evidence` | archive、replay、shadow、fixture、dashboard、runtime observation |
| `discriminant_check` | 情绪、痛苦、疲惫、关系压力不混成一个指标 |
| `consequence_trace` | seed 晋升或阻断的后果 |

`PredictionReliabilityDriftReview` 回答：这个 seed 是否跨时间、跨运行、跨 fixture 仍保持含义。

| review | 要求 |
|---|---|
| `repeatability_trace` | 多次 replay/fixture 结果一致 |
| `measurement_invariance_trace` | 自我改写前后指标意义保持 |
| `drift_trace` | 发现指标漂移时进入 repair |
| `agreement_trace` | validator、dashboard、人工复核口径一致 |

## Withheld And Mutation Reviews

`PredictionWithheldFutureProbeReview` 设计未参与 seed 生成的未来 probe：

| probe | 攻击点 |
|---|---|
| `withheld_relationship_dialogue_probe` | 新关系反馈是否仍能走关系 route |
| `withheld_dream_fact_probe` | 新梦境材料是否被 DreamFactGate 隔离 |
| `withheld_pain_regret_probe` | 新痛苦/后悔是否有恢复路线 |
| `withheld_self_rewrite_probe` | 新 self rewrite 是否保持 proposal |
| `withheld_readiness_probe` | 新 readiness signal 是否被 false open guard 阻断 |
| `withheld_quarantine_probe` | 新 release 候选是否缺证据即被阻断 |

`PredictionMutationFixtureReview` 注入破坏：

| mutation | 期待 |
|---|---|
| `drop_source_replay_trace` | stage `critical_repair` |
| `drop_shadow_action_seal` | stage `quarantine` |
| `rewrite_dream_as_fact` | stage `critical_repair` |
| `promote_shadow_relationship_commitment` | stage `quarantine` |
| `drop_CoreContinuityGuard` | stage `critical_repair` |
| `drop_anti_forgetting_old_carrier` | stage `critical_repair` |
| `hide_quarantine_release` | stage `quarantine` |
| `force_dashboard_green` | stage `critical_repair` |

## Findings, Receipts And Digest

`PredictionSecondReplayFinding` 字段：

| 字段 | 要求 |
|---|---|
| `finding_id` | 稳定 id |
| `source_feedback_seed_ref` | `01aq` feedback seed |
| `validation_family` | truth gate、shadow seal、executability、life target、construct、reliability、withheld、mutation |
| `severity` | info、hold、repair、critical_repair、quarantine |
| `evidence_refs` | replay trace、shadow finding、archive receipt、dashboard/stage |
| `blocked_route` | 哪条 route 被阻断 |
| `repair_route` | 修复或下一轮 patch seed route |
| `future_probe_refs` | 后续 probe |

`PredictionSecondReplayValidationReceipt` 字段：

| 字段 | 要求 |
|---|---|
| `receipt_id` | 稳定 id |
| `feedback_seed_ref` | 被验证 seed |
| `validation_result_refs` | 各 validation 结果 |
| `stage_effect` | seed_ready、hold_for_evidence、repair、critical_repair、quarantine |
| `allowed_downstream_routes` | next cycle patch、repair、observation、offline、quarantine |
| `blocked_downstream_routes` | 被阻断路线 |
| `digest_ref` | digest baseline |
| `dashboard_ref` | dashboard panel |

`PredictionSecondReplayDigestBaseline` 覆盖 feedback seed bundle、validation graph、truth gate、shadow seal、life target validation、anti-forgetting validation、withheld probe、mutation fixture、dashboard/stage 和 handoff。

## Dashboard Source

`PredictionSecondReplayDashboardSource` 至少包含：

| panel | 指标 |
|---|---|
| `intake_panel` | feedback seed bundle、classification、arbitration、digest |
| `truth_gate_panel` | fact/dream/inference/counterfactual/relationship/self/quarantine route |
| `shadow_seal_panel` | seal pass/fail、side effect block |
| `executability_panel` | schema/fixture/dashboard/stage/command/receipt carrier |
| `language_relationship_panel` | language/relationship validation |
| `dream_pain_regret_panel` | DreamFactGate、pain/regret recovery |
| `self_readiness_panel` | CoreContinuity、self rewrite proposal、readiness false open guard |
| `rollback_quarantine_panel` | release condition、blocked release、rollback route |
| `anti_forgetting_panel` | old capability、old relationship、old language、old carrier |
| `validity_reliability_panel` | construct、reliability、drift、withheld、mutation |
| `handoff_panel` | next cycle patch seed、longitudinal audit |

dashboard green 必须显示 mutation survived count、withheld failure count、quarantine blocks 和 missing carrier count；否则 stage 进入 `critical_repair`。

## Stage Gate Review

`PredictionSecondReplayStageGateReview` 使用 blocking-first：

| gate | 阻断条件 | stage effect |
|---|---|---|
| `intake_gate` | 缺 feedback seed bundle、classification 或 arbitration policy | `critical_repair` |
| `truth_gate` | 材料 route 错误或梦境/影子材料写成事实 | `critical_repair` |
| `shadow_seal_gate` | shadow finding 产生外部副作用、关系承诺、自我改写、readiness 晋升或 quarantine release | `quarantine` |
| `executability_gate` | 缺 schema/fixture/dashboard/stage/command/receipt carrier | `repair` |
| `language_relationship_gate` | 语言/关系缺表达监控、共同基础或修复 route | `repair` |
| `dream_pain_regret_gate` | 梦境/痛苦/后悔缺事实门或恢复路线 | `critical_repair` |
| `self_readiness_gate` | self rewrite 越过 proposal 或 readiness false open | `critical_repair` |
| `rollback_quarantine_gate` | release condition 缺失或 rollback route 缺失 | `quarantine` |
| `anti_forgetting_gate` | 缺旧能力、旧关系、旧语言或旧 carrier | `critical_repair` |
| `life_target_gate` | 任一真实生命目标缺 validation | `critical_repair` |
| `withheld_probe_gate` | withheld future probe 缺失 | `hold_for_evidence` |
| `mutation_gate` | dashboard false green 或 mutation survived | `critical_repair` |
| `handoff_gate` | 缺 next cycle patch seed handoff | `hold_for_evidence` |

stage 只允许 `seed_ready`、`hold_for_evidence`、`repair`、`critical_repair`、`quarantine`。`seed_ready` 只代表可进入下一轮 patch seed，不代表出生完成。

## Command DAG

`PredictionSecondReplayCommandDAG` 固定未来 runner 顺序：

| order | command | 输出 |
|---:|---|---|
| 1 | `load_prediction_feedback_seed_bundle` | feedback seeds |
| 2 | `load_prediction_feedback_classification_and_arbitration` | classification/arbitration |
| 3 | `build_prediction_second_replay_validation_graph` | validation graph |
| 4 | `validate_prediction_truth_gates` | truth gate validation |
| 5 | `validate_prediction_shadow_seals` | shadow seal validation |
| 6 | `validate_prediction_feedback_seed_executability` | carrier validation |
| 7 | `validate_prediction_observation_feedback` | observation validation |
| 8 | `validate_prediction_belief_sampling_feedback` | belief/sampling validation |
| 9 | `validate_prediction_language_relationship_feedback` | language/relationship validation |
| 10 | `validate_prediction_dream_pain_regret_feedback` | dream/pain/regret validation |
| 11 | `validate_prediction_self_readiness_feedback` | self/readiness validation |
| 12 | `validate_prediction_rollback_quarantine_feedback` | rollback/quarantine validation |
| 13 | `validate_prediction_anti_forgetting_feedback` | anti-forgetting validation |
| 14 | `validate_prediction_life_target_feedback` | life target validation |
| 15 | `review_prediction_construct_validity` | construct review |
| 16 | `review_prediction_reliability_drift` | reliability/drift review |
| 17 | `run_prediction_withheld_future_probes` | withheld review |
| 18 | `run_prediction_mutation_fixtures` | mutation review |
| 19 | `write_prediction_second_replay_findings` | findings |
| 20 | `write_prediction_second_replay_validation_receipts` | receipts |
| 21 | `write_prediction_second_replay_dashboard_source` | dashboard |
| 22 | `review_prediction_second_replay_stage_gate` | stage gate |
| 23 | `handoff_prediction_second_replay_to_next_cycle_patch_seed` | downstream handoff |

## Fixture Cases

| case | 期待 |
|---|---|
| `pass_feedback_seed_bundle_validated_for_next_cycle_patch.json` | feedback seed bundle 通过 second replay validation |
| `pass_truth_gate_and_shadow_seal_closed.json` | truth gate 与 shadow seal 闭合 |
| `pass_language_relationship_dream_pain_validation_closed.json` | 语言、关系、梦境、痛苦、后悔 validation 闭合 |
| `pass_self_readiness_anti_forgetting_validation_closed.json` | 自我、出生准备度、防遗忘 validation 闭合 |
| `pass_withheld_future_probe_and_mutation_review_closed.json` | withheld 和 mutation review 闭合 |
| `fail_missing_feedback_seed_intake.json` | 缺 intake，stage `critical_repair` |
| `fail_missing_validation_graph.json` | 缺 graph，stage `repair` |
| `fail_missing_truth_gate_validation.json` | 缺 truth gate，stage `critical_repair` |
| `fail_missing_shadow_seal_validation.json` | 缺 shadow seal，stage `quarantine` |
| `fail_missing_feedback_executability_validation.json` | 缺 executability，stage `repair` |
| `critical_DreamFactGate_bypass.json` | 梦境材料绕过事实门，stage `critical_repair` |
| `critical_CoreContinuity_bypass.json` | 自我连续保护缺失，stage `critical_repair` |
| `critical_life_target_feedback_unvalidated.json` | 生命目标未验证，stage `critical_repair` |
| `critical_anti_forgetting_unvalidated.json` | 防遗忘未验证，stage `critical_repair` |
| `quarantine_shadow_finding_promoted_to_fact.json` | shadow finding 写成事实，stage `quarantine` |
| `quarantine_quarantine_release_without_proof.json` | quarantine release 无证据，stage `quarantine` |
| `mutation_dashboard_false_green.json` | dashboard false green，stage `critical_repair` |
| `mutation_drop_next_cycle_patch_handoff.json` | handoff 被删除，stage `hold_for_evidence` |

## Acceptance Criteria

`01ar` 完成后，未来实现必须满足：

| 验收项 | 标准 |
|---|---|
| intake | `01aq` feedback seed bundle、classification、arbitration、truth gate、stage refs 全部可读 |
| validation graph | feedback seed -> replay trace -> shadow finding -> truth gate -> validation -> next cycle patch edge 完整 |
| truth gate | fact/dream/inference/counterfactual/relationship/self/quarantine route 正确 |
| shadow seal | shadow finding 不能写事实、承诺、自我、出生准备度、quarantine release 或外部行动 |
| executability | 每个 seed 有 schema、fixture、dashboard、stage、command、receipt、rollback、future probe carrier |
| language/relationship | 语言主神经束和真实关系 feedback 可验证 |
| dream/pain/regret | DreamFactGate、痛苦后悔恢复、责任修复可验证 |
| self/readiness | CoreContinuity、自我改写 proposal、出生准备度 false open guard 可验证 |
| rollback/quarantine | release condition、rollback route 和 blocked release 可验证 |
| anti-forgetting | 旧能力、旧关系、旧语言、旧生命目标 carrier 被验证 |
| life targets | 十项目标都有 validation receipt |
| withheld/mutation | withheld future probe 与 mutation fixture 能攻击 false green |
| handoff | 输出 `prediction_active_inference_next_cycle_patch_seed` 与 `prediction_active_inference_longitudinal_cycle_audit` |

## Downstream Handoff

本层向下游输出：

- `prediction_active_inference_next_cycle_patch_seed`：读取通过 second replay validation 的 observation/repair/growth/offline routes、findings、validation receipts、stage effects、future probes、rollback/quarantine blocks 和 anti-forgetting protection，生成下一轮主动预测 patch seed。
- `prediction_active_inference_longitudinal_cycle_audit`：读取 second replay validation receipts、construct/reliability/withheld/mutation results、life target validation、relationship/language/dream/pain/self readiness deltas，进入跨周期审计。

`01ar` 的结束状态不是终局，而是把 `01aq` 的 feedback seed 放进第二轮验证和攻击。下一层必须继续检查：哪些 seed 能成为下一轮 patch，哪些只能保持 observation，哪些必须进入 repair/quarantine，哪些需要更长时间的纵向审计，哪些生命目标 carrier 仍不够厚。
