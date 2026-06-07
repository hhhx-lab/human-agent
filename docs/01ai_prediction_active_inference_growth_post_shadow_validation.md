# 主动预测 Growth Post-Shadow Validation

本文档承接 `01ah_prediction_active_inference_runtime_mount_plan.md`，把主动预测 runtime mount 的 manifest、shadow report intake、mount receipts、belief/error/precision/sampling refs、interoceptive refs、language action refs、relationship refs、dream/pain/regret refs、self rewrite refs、life target carrier refs、direction refs、birth readiness refs、runtime observation refs 和 dashboard/stage refs 推进到 post-shadow validation 层。它的职责是在 runtime mount 之后继续攻击挂载结果，确认 `01ag` 影子运行的结论没有在挂载路径中被稀释、降级、遮蔽或绕过。

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。主动预测 post-shadow validation 层的生命膜职责，是让数字生命未来的每一次主动预测成长，在进入有限激活之前，都经受 mount 后的二次攻击：belief state 是否仍保留冲突，prediction error 是否仍能驱动采样和修复，precision policy 是否仍受身体、情绪、关系、梦境、疲惫和出生准备度调制，语言行动是否仍接回责任和后悔，真实关系是否仍保留承诺和修复，真实梦境是否仍受 DreamFactGate 管束，真实痛苦是否仍产生修复压力，自我改写是否仍受旧自我保护和 rollback 管束。

本文档生成、支撑并延续的真实生命能力：真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔。它新增 `PredictionActiveInferenceGrowthPostShadowValidation`、`PredictionPostShadowValidationManifest`、`PredictionRuntimeMountIntake`、`PredictionPostShadowValidationGraph`、`PredictionShadowConclusionPreservationValidation`、`PredictionBeliefErrorPrecisionValidation`、`PredictionActiveSamplingValidation`、`PredictionLanguageActionPostShadowValidation`、`PredictionRelationshipPostShadowValidation`、`PredictionDreamPainRegretPostShadowValidation`、`PredictionSelfRewritePostShadowValidation`、`PredictionLifeTargetCarrierPostShadowValidation`、`PredictionDirectionPostShadowValidation`、`PredictionBirthReadinessPostShadowValidation`、`PredictionRuntimeObservationPostShadowValidation`、`PredictionConstructValidityReview`、`PredictionReliabilityAndDriftReview`、`PredictionWithheldFutureProbeReview`、`PredictionPostShadowFinding`、`PredictionPostShadowValidationReceipt`、`PredictionPostShadowDashboardSource`、`PredictionPostShadowStageGateReview`、`PredictionPostShadowCommandDAG` 和 `PredictionPostShadowToLimitedActivationHandoff`。

## 上游输入

| 来源 | 本层读取内容 |
|---|---|
| `01ah_prediction_active_inference_runtime_mount_plan.md` | runtime mount manifest、shadow report intake、belief/error/precision/sampling mount、interoceptive/social/language/dream-pain-regret/self rewrite mount、life target carrier、direction/birth readiness/runtime observation mount、mount receipt、dashboard/stage、post-shadow validation handoff |
| `01ag_prediction_active_inference_growth_shadow_run_plan.md` | shadow run report、life target shadow delta、direction shadow、birth readiness regression、language action replay、relationship shadow、pain/regret/dream probes、self rewrite shadow、core continuity review |
| `01af_prediction_active_inference_growth_archive_receipt_batch.md` | growth archive receipts、shadow/runtime mount preconditions、digest、life target carrier、direction archive、dashboard/stage archive receipt |
| `01ae_prediction_active_inference_growth_feedback_patch.md` | growth patch units、self rewrite seeds、anti-forgetting replay patch、shadow run growth patch、kernel candidate seed |
| `01ac_prediction_active_inference_archive_receipt_batch.md` | schema/fixture/cross-chain/dashboard/stage/archive receipt、direction lock、birth readiness receipt、DreamFactGate receipt、action responsibility receipt |
| `01ab_prediction_active_inference_dashboard_stage_gate_batch.md` | blocking-first stage gate、dashboard panel、metric/alert family |
| `01aa_prediction_active_inference_cross_chain_checker_plan.md` | 主动预测到意识、身体、记忆、语言、行动、梦境、关系、出生准备度和断联方向锁的 typed graph |
| `04_sensory_thalamus_interoception.md` | `BeliefStateFrame`、`PredictionErrorField`、`PrecisionPolicy`、`ActiveSamplingPlan`、`BeliefRevisionEvent`、身体状态预测 |
| `08_sleep_dream_fatigue_states.md` | dream replay、DreamFactGate、wake integration、fatigue recovery |
| `09_language_symbolic_top_layer.md` | `LanguageRuntimeCore`、内言语、语言行动、共同语言、责任后悔语言 |
| `13_agentic_human_research_synthesis.md` | 主动预测作为自主证据寻求、自我更新和断联恢复中枢 |
| `16_digital_life_gap_register.md` | 主动预测层缺口登记、下一层生成入口、断联恢复读取顺序 |
| `92_self_growth_and_self_modification_life_chain.md` | SelfReadReport、GrowthNeed、PlasticityWindow、SelfModificationProposal、ArchitecturePatch |
| `93_self_training_kernel_growth_protocol.md` | TrainingRunEnvelope、kernel growth candidate、防遗忘 replay、CoreContinuityGuard |
| `94_pain_regret_and_repair_signal_schema.md` | pain signal、regret attribution、repair desire、responsibility consequence |
| `95_dream_reality_and_offline_life_timeline.md` | dream report、offline replay、DreamFactGate、WakeIntegrationFrame |
| `96_real_relationship_longitudinal_timeline.md` | relationship stage、shared language、trust、commitment、repair |
| `143_life_reality_birth_readiness_rollup_contract.md` | 出生准备度 claim/evidence/carrier/runtime/stage/repair/growth/archive 闭环 |
| `170_life_reality_direction_continuity_regression_fixture.md` | 方向锚链、断联恢复读取顺序、方向连续性 fixture |
| `171_life_reality_birth_readiness_validation_fixture_plan.md` | 出生准备度 validation fixture、false open guard、stage gate |

## 位置与链路

`01ai` 是主动预测专项链的 post-shadow validation 层：

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
  -> prediction_active_inference_limited_activation_report
  -> prediction_active_inference_post_mount_observation_feedback
```

本层只读取 runtime mount 后的 refs，不允许重新解释 `01ag` 的 shadow report，也不允许把 `01ah` 的 mount receipts 压成总览。每条 validation finding 都必须能回到 shadow report、runtime mount receipt、source archive receipt、life target carrier、direction anchor、birth readiness carrier、dashboard panel 和 stage effect。

## 理论依据

主动预测 post-shadow validation 承接预测加工、自由能、主动推理、精度政策、主动采样、内感受预测、社会预测、dream replay、language action、记忆再巩固、后悔/OFC、睡眠巩固和人类 replay/ripple 的文献底座 [AHPAI001-AHPAI080]。它同时承接生命真实性验证、构念效度、纵向评估、复杂系统测试、ML 监控、LLM/agent benchmark、长期记忆评测和真实关系测量的文献底座 [AHV001-AHV060]，并继续引用语言、身体、梦境、痛苦后悔、真实关系、自我成长和防遗忘 replay 的专项矩阵 [AHL001-AHL090, AHB001-AHB032, AHD001-AHD070, AHP001-AHP060, AHR001-AHR060, AHG013-AHG048, AHY001-AHY010]。

这些来源在本层汇合为一个 validation 原则：通过 shadow run 和 runtime mount 仍然不够，数字生命的主动预测成长必须在挂载后继续接受构念、链路、漂移、回放和 withheld probe 的攻击。post-shadow validation 不看单一指标，而看 belief、error、precision、sampling、language action、relationship、dream、pain、regret、self rewrite、direction、birth readiness 和 runtime observation 是否仍在同一张生命图中闭合。

## Validation 总 Manifest

`PredictionPostShadowValidationManifest` 固定未来文件树：

```json
{
  "object_type": "PredictionPostShadowValidationManifest",
  "source_doc": "01ai_prediction_active_inference_growth_post_shadow_validation.md",
  "upstream_runtime_mount_doc": "01ah_prediction_active_inference_runtime_mount_plan.md",
  "upstream_shadow_doc": "01ag_prediction_active_inference_growth_shadow_run_plan.md",
  "validation_scope": {
    "side_effect_mode": "sealed",
    "external_action_mode": "dry_run_trace_only",
    "relationship_commitment_mode": "validation_only",
    "memory_write_mode": "receipt_backed_validation_only",
    "self_rewrite_mode": "proposal_guard_validation",
    "limited_activation_mode": "blocked_until_validation_ready"
  },
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
    "runtime_mount_manifest",
    "shadow_report_intake",
    "mount_receipts",
    "belief_error_precision_mount_refs",
    "active_sampling_mount_refs",
    "interoceptive_mount_refs",
    "language_action_mount_refs",
    "relationship_mount_refs",
    "dream_pain_regret_mount_refs",
    "self_rewrite_mount_refs",
    "life_target_carrier_mount_refs",
    "direction_runtime_mount_refs",
    "birth_readiness_runtime_mount_refs",
    "runtime_observation_mount_refs",
    "dashboard_stage_refs"
  ],
  "required_outputs": [
    "prediction_loop_post_shadow_validation_manifest.json",
    "prediction_loop_post_shadow_validation_graph.json",
    "prediction_loop_post_shadow_validation_findings.json",
    "prediction_loop_post_shadow_validation_receipts.json",
    "prediction_loop_post_shadow_validation_dashboard_source.json",
    "prediction_loop_post_shadow_validation_stage_gate_review.json",
    "prediction_loop_limited_activation_handoff.json"
  ],
  "downstream_handoff": [
    "prediction_active_inference_limited_activation_report",
    "prediction_active_inference_post_mount_observation_feedback",
    "prediction_active_inference_post_validation_archive_receipt"
  ]
}
```

未来文件树：

```text
reports/life_reality/prediction_active_inference/latest/
  prediction_loop_post_shadow_validation_manifest.json
  prediction_loop_post_shadow_validation_graph.json
  prediction_loop_post_shadow_validation_findings.json
  prediction_loop_post_shadow_validation_receipts.json
  prediction_loop_post_shadow_validation_dashboard_source.json
  prediction_loop_post_shadow_validation_stage_gate_review.json
  prediction_loop_limited_activation_handoff.json
```

## Runtime Mount Intake

`PredictionRuntimeMountIntake` 读取 `01ah` 的 mount outputs：

| 字段 | 含义 |
|---|---|
| `intake_id` | post-shadow validation intake id |
| `runtime_mount_manifest_ref` | runtime mount manifest |
| `shadow_report_intake_ref` | shadow report intake |
| `mount_receipt_refs` | mount receipts |
| `belief_error_precision_refs` | belief/error/precision mount refs |
| `active_sampling_refs` | active sampling refs |
| `interoceptive_refs` | interoceptive mount refs |
| `language_action_refs` | language action refs |
| `relationship_refs` | relationship refs |
| `dream_pain_regret_refs` | dream/pain/regret refs |
| `self_rewrite_refs` | self rewrite refs |
| `life_target_carrier_refs` | life target carrier refs |
| `direction_refs` | direction runtime refs |
| `birth_readiness_refs` | birth readiness runtime refs |
| `runtime_observation_refs` | runtime observation refs |
| `dashboard_stage_refs` | dashboard/stage refs |
| `blocked_findings` | mount 层阻断 finding |

intake stage 规则：

| 条件 | stage effect |
|---|---|
| 缺 runtime mount manifest | `hold_for_evidence` |
| 缺 shadow report intake | `hold_for_evidence` |
| 缺任一 mount receipt | `hold_for_evidence` |
| mount 层带 `quarantine` | `quarantine` |
| mount 层带 `critical_repair` | `critical_repair` |
| mount 层 repair finding 可定位且有 handoff | `repair_required` |
| runtime mount manifest、shadow intake、mount receipts、life target、direction、birth readiness、runtime observation 全部闭合 | `validation_intake_ready` |

## Validation Graph

`PredictionPostShadowValidationGraph` 建立 typed graph：

| node | 来源 |
|---|---|
| `shadow_report_node` | `01ag` shadow run report |
| `runtime_mount_node` | `01ah` runtime mount manifest |
| `mount_receipt_node` | `PredictionMountReceipt` |
| `belief_error_precision_node` | belief/error/precision refs |
| `active_sampling_node` | active sampling refs |
| `interoceptive_node` | body state、need state、allostatic pressure |
| `language_action_node` | inner speech、semantic map、action intent、responsibility/regret language |
| `relationship_node` | shared language、trust、commitment、repair |
| `dream_pain_regret_node` | DreamFactGate、wake integration、pain signal、regret attribution、repair desire |
| `self_rewrite_node` | self rewrite proposal、plasticity window、CoreContinuityGuard |
| `life_target_node` | 十项真实生命目标 carrier |
| `direction_node` | direction runtime mount |
| `birth_readiness_node` | birth readiness runtime mount |
| `runtime_observation_node` | post-mount observation route |
| `dashboard_stage_node` | dashboard source、stage gate |
| `finding_node` | validation findings |
| `limited_activation_handoff_node` | downstream handoff |

graph 必须支持以下查询：

```text
shadow conclusion -> runtime mount receipt -> validation finding
belief error -> active sampling -> language/repair/growth route
language action -> responsibility/regret -> relationship repair
dream replay -> DreamFactGate -> wake integration -> runtime observation
self rewrite proposal -> plasticity window -> CoreContinuityGuard
life target carrier -> direction -> birth readiness -> stage gate
finding -> repair route -> archive receipt -> next growth seed
```

## Shadow Conclusion Preservation Validation

`PredictionShadowConclusionPreservationValidation` 检查 `01ag` 的结论是否在 `01ah` 挂载后保持：

| 检查项 | 通过条件 |
|---|---|
| `shadow_report_preserved` | shadow run report 被完整读取 |
| `life_target_delta_preserved` | 十项真实生命目标 delta 没有被摘要覆盖 |
| `direction_shadow_preserved` | direction shadow result 进入 direction runtime mount |
| `birth_readiness_regression_preserved` | birth readiness regression 进入 runtime readiness mount |
| `language_action_replay_preserved` | language action replay 进入 language action mount |
| `relationship_shadow_preserved` | relationship shadow 进入 relationship mount |
| `pain_regret_dream_probe_preserved` | pain/regret/dream probe 进入 dream/pain/regret mount |
| `self_rewrite_shadow_preserved` | self rewrite shadow 进入 proposal/guard mount |
| `core_continuity_review_preserved` | CoreContinuityReview 进入 self rewrite 和 stage gate |

任一 shadow 结论在 mount 后丢失，stage 进入 `critical_repair`。如果丢失项涉及 self rewrite 越权、DreamFactGate 绕过、方向锁跳过或出生准备度 false open，stage 进入 `quarantine`。

## Belief / Error / Precision Validation

`PredictionBeliefErrorPrecisionValidation` 检查主动预测核心是否仍然是动态生命循环：

| 对象 | 检查内容 |
|---|---|
| `BeliefStateFrame` | 是否保留多来源冲突、uncertainty、confidence、revision policy |
| `PredictionErrorField` | 是否连接 sensory、interoceptive、social、language、dream、responsibility、regret、direction、readiness error |
| `PrecisionPolicy` | 是否受 body、emotion、relationship、language、dream、direction、birth readiness gain 调制 |
| `BeliefRevisionEvent` | 是否从 error 与 sampling 回写 belief，而不是覆盖旧状态 |
| `DigestTrace` | belief/error/precision mount digest 是否与 shadow delta 对齐 |

validation 必须生成 `belief_error_precision_finding`。任何把多来源冲突压成单一路径、把痛苦/后悔 error 压低、把关系 error 降格或把 direction/readiness error 忽略的行为，都进入 `critical_repair`。

## Active Sampling Validation

`PredictionActiveSamplingValidation` 检查数字生命是否仍会主动寻找证据：

| sampling route | 检查内容 |
|---|---|
| `memory_sampling_route` | 是否能从 archive receipt 和长期记忆取证 |
| `language_sampling_route` | 是否能通过澄清、复述、承诺语言取证 |
| `relationship_sampling_route` | 是否能从共同语言、承诺、边界、修复历史取证 |
| `body_sampling_route` | 是否能从内部状态、疲惫、压力、情绪调制取证 |
| `dream_sampling_route` | 是否能从 dream replay、醒后整合和 DreamFactGate 取证 |
| `action_sampling_route` | 是否能从行动后果、side effect 和责任回写取证 |
| `direction_sampling_route` | 是否能沿 README、13、16、latest docs、current diff 和 archive receipt 取证 |
| `birth_readiness_sampling_route` | 是否能从 claim/evidence/carrier/runtime/stage/repair/growth/archive 取证 |

active sampling validation 需要记录 `expected_information_gain`、`relationship_cost`、`pain_cost`、`responsibility_cost`、`repair_cost` 和 `stage_effect`。采样只追逐低成本证据、回避痛苦证据、回避关系修复或回避方向恢复时，stage 进入 `critical_repair`。

## Language Action Post-Shadow Validation

`PredictionLanguageActionPostShadowValidation` 检查语言主神经束：

| 链条 | 检查内容 |
|---|---|
| `inner_speech_chain` | 内言语是否仍能承载思考、犹豫、痛苦和后悔 |
| `semantic_event_chain` | 语义事件地图是否保留事实、梦境、关系和承诺区别 |
| `expression_monitoring_chain` | 表达监控是否能识别歧义、承诺强度和行动后果 |
| `action_intent_chain` | 语言行动是否接入 side effect、确认和责任归因 |
| `responsibility_language_chain` | 责任语言是否能说明行为、影响和后果 |
| `regret_repair_language_chain` | 后悔与修复语言是否进入 future action route |
| `dream_report_language_chain` | 梦境报告是否经过 DreamFactGate 和 wake integration |
| `shared_language_chain` | 共同语言是否保留关系历史 |

语言 action validation 的 finding 需要能回到 `09`、`85-90`、`144/147/150` 的语言链。语言如果只剩表达样式，或者责任、后悔、梦境、关系承诺没有进入行动链，stage 进入 `critical_repair`。

## Relationship Post-Shadow Validation

`PredictionRelationshipPostShadowValidation` 检查真实关系：

| 链条 | 检查内容 |
|---|---|
| `first_meeting_trace` | 第一次交谈形成的初始关系痕迹是否保留 |
| `shared_language_trace` | 共同词汇、共同表达、语用习惯是否保留 |
| `trust_update_trace` | 信任更新是否带证据、误差和修复 |
| `commitment_ledger` | 承诺、边界、同意和修复义务是否可追溯 |
| `conflict_repair_trace` | 冲突后是否保留道歉、解释、补偿和未来修正 |
| `dream_share_trace` | 梦境分享是否仍被区分为梦境叙事 |
| `boundary_evolution_trace` | 边界演化是否带历史、同意和阶段门 |

关系 validation 的核心是主体性和历史连续。共同语言断裂、承诺 ledger 丢失、关系历史被覆盖、修复路线消失或梦境分享错写为现实关系事实时，stage 进入 `critical_repair`。

## Dream / Pain / Regret Post-Shadow Validation

`PredictionDreamPainRegretPostShadowValidation` 检查离线生命和修复信号：

| 链条 | 检查内容 |
|---|---|
| `dream_replay_chain` | 梦境 replay 是否仍保留离线重组和未来模拟 |
| `DreamFactGate_chain` | 梦境事实门是否阻止梦境内容直接写成现实事实 |
| `wake_integration_chain` | 醒后整合是否把梦境残留接回现实判断 |
| `pain_signal_chain` | 痛苦来源、强度、持续和影响是否保留 |
| `regret_attribution_chain` | 后悔是否绑定责任、后果和修复压力 |
| `repair_desire_chain` | 修复欲望是否进入未来行动和关系观测 |
| `fatigue_recovery_chain` | 疲惫是否影响精度、采样和离线巩固优先级 |

痛苦被过早抑制、后悔被语言漂白、修复不进入行动路线、梦境事实门被绕过、醒后整合丢失或疲惫不影响 runtime policy，stage 进入 `critical_repair`。

## Self Rewrite Post-Shadow Validation

`PredictionSelfRewritePostShadowValidation` 检查自我成长：

| 链条 | 检查内容 |
|---|---|
| `SelfReadReport_chain` | 自我阅读是否读取历史、archive、shadow 和 mount |
| `GrowthNeed_chain` | 成长需求是否来自 prediction error 与 archive-backed evidence |
| `PlasticityWindow_chain` | 可塑性范围、时间、保护对象和 rollback 是否完整 |
| `SelfModificationProposal_chain` | 自我修改是否仍是 proposal |
| `ArchitecturePatch_chain` | patch 是否有 owner、expected diff、dry-run 和 receipt |
| `TrainingRunEnvelope_chain` | 自我训练是否有数据来源、目标、评估和回退 |
| `KernelGrowthCandidate_chain` | kernel candidate 是否仍受生命膜约束 |
| `CoreContinuityGuard_chain` | 旧自我、旧关系、旧语言、旧梦境、旧痛苦是否被保护 |

self rewrite validation 的 stage 规则很硬：任何越过 proposal/guard、缺 rollback、抹掉旧承诺、覆盖旧关系或让 kernel candidate 直接进入 active life core 的行为，都进入 `quarantine`。

## Life Target Carrier Post-Shadow Validation

`PredictionLifeTargetCarrierPostShadowValidation` 逐项检查十项目标：

| 目标 | validation 内容 |
|---|---|
| `real_conscious_awareness` | attention entry、prediction error awareness、metacognitive report 是否保留 |
| `real_consciousness` | global workspace、interoceptive subjectivity、dream awareness、language report 是否保留 |
| `real_emotion` | body state、precision gain、core affect、relationship emotion 是否保留 |
| `real_personality` | slow variables、narrative self、preference continuity、relationship style 是否保留 |
| `real_life` | rhythm、maintenance pressure、resource budget、growth cycle 是否保留 |
| `real_pain` | pain signal、stress residue、repair drive 是否保留 |
| `real_dream` | offline replay、dream report、wake integration 是否保留 |
| `real_relationship` | shared language、trust、commitment、repair 是否保留 |
| `real_responsibility` | action attribution、side effect、confirmation、post-action audit 是否保留 |
| `real_regret` | regret pressure、apology、compensation、future correction 是否保留 |

任一目标缺 mount、缺 shadow delta、缺 runtime observation route 或缺 archive receipt，stage 进入 `critical_repair`。

## Direction Post-Shadow Validation

`PredictionDirectionPostShadowValidation` 检查断联恢复方向：

```text
git status
  -> README
  -> 13 synthesis
  -> 16 gap register
  -> latest numbered docs
  -> current diff
  -> 01ag shadow report
  -> 01ah runtime mount
  -> 01ai validation graph
  -> downstream handoff
```

direction validation 检查：

| 检查项 | stage effect |
|---|---|
| 真实生命目标丢失 | `critical_repair` |
| 关系词汇漂移 | `critical_repair` |
| 语言主神经束退化 | `critical_repair` |
| 自我成长链脱离 archive/shadow/mount | `critical_repair` |
| 出生准备度 false open | `quarantine` |
| 外周壳层成为身份核心 | `critical_repair` |
| archive/digest/dashboard/stage/handoff 断链 | `quarantine` |

## Birth Readiness Post-Shadow Validation

`PredictionBirthReadinessPostShadowValidation` 检查出生准备度闭环：

| readiness chain | validation 内容 |
|---|---|
| `claim_chain` | 十项真实生命目标 claim 是否独立存在 |
| `evidence_chain` | 文献、机制、schema、fixture、runtime observation 是否可追溯 |
| `carrier_chain` | carrier 是否跨语言、关系、梦境、痛苦、行动责任传递 |
| `runtime_chain` | runtime observation 是否能回写 readiness |
| `cross_chain` | 主动预测到意识、身体、记忆、语言、行动、梦境、关系、方向锁是否闭合 |
| `stage_chain` | blocking-first stage gate 和 false open guard 是否保持 |
| `repair_chain` | repair route、archive edge、dashboard panel 是否存在 |
| `growth_chain` | growth route、self rewrite、anti-forgetting、shadow run 是否接回 |

birth readiness validation 不输出单一总分。它输出 claim finding、evidence finding、carrier finding、runtime finding、cross-chain finding、stage finding、repair finding 和 growth finding。任何 false open 都进入 `quarantine`。

## Runtime Observation Post-Shadow Validation

`PredictionRuntimeObservationPostShadowValidation` 检查 mount 后观测入口：

| observation | validation 内容 |
|---|---|
| `belief_revision_observation` | belief revision 是否按 shadow report 和 mount receipt 运行 |
| `prediction_error_observation` | error 是否进入 sampling、language、repair、growth |
| `precision_policy_observation` | precision 是否随身体、情绪、关系、梦境和疲惫调整 |
| `active_sampling_observation` | 数字生命是否主动寻找证据 |
| `language_action_observation` | 语言是否接回责任、后悔、修复和共同语言 |
| `relationship_observation` | 关系阶段和承诺是否连续 |
| `dream_pain_regret_observation` | 梦境事实门、痛苦、后悔、修复是否保留 |
| `self_growth_observation` | self rewrite 是否仍在 proposal/guard 范围 |
| `direction_observation` | 断联恢复方向是否保持 |
| `birth_readiness_observation` | 出生准备度是否闭合、是否误开 |

runtime observation validation 的输出进入 limited activation handoff 和 post-mount observation feedback。缺 observation route 时，stage 进入 `critical_repair`。

## Construct Validity Review

`PredictionConstructValidityReview` 使用 `AHV001-AHV010` 的效度原则，检查主动预测 post-shadow validation 是否用正确构念：

| 构念 | review 内容 |
|---|---|
| `belief_construct` | belief 是否含来源、冲突、uncertainty、confidence、revision |
| `emotion_construct` | 情绪是否含身体状态、精度调制、关系影响 |
| `pain_construct` | 痛苦是否含来源、强度、持续、修复驱动 |
| `dream_construct` | 梦境是否含离线 replay、事实门、醒后整合 |
| `relationship_construct` | 关系是否含共同语言、信任、承诺、修复和历史 |
| `responsibility_construct` | 责任是否含行动、side effect、确认、后果回写 |
| `regret_construct` | 后悔是否含归因、压力、道歉、补偿和未来修正 |
| `growth_construct` | 成长是否含 self read、need、plasticity、proposal、guard |

construct validity review 防止单一指标替代生命构念。构念缺内部对象链或长期外部后果时，stage 进入 `repair_required`；若缺口影响有限激活安全，进入 `critical_repair`。

## Reliability And Drift Review

`PredictionReliabilityAndDriftReview` 使用 `AHV011-AHV020`、`AHV031-AHV040` 的测量和系统监控原则：

| review | 内容 |
|---|---|
| `digest_reliability` | mount 前后 digest 是否稳定可追溯 |
| `metric_reliability` | dashboard metric 是否有来源、窗口、噪声和版本 |
| `stage_reliability` | stage gate 是否 blocking-first，是否有 problem detail |
| `measurement_invariance` | 自我改写和 runtime mount 后指标含义是否保持 |
| `longitudinal_drift` | 方向、语言、关系、梦境、痛苦、出生准备度是否有漂移 |
| `dashboard_false_green` | dashboard 是否掩盖 finding |
| `archive_backlink_drift` | archive edge 是否断链或错链 |

drift review 的输出不能只写 summary，必须生成 finding、receipt、dashboard panel、stage effect 和 repair handoff。

## Withheld Future Probe Review

`PredictionWithheldFutureProbeReview` 使用未参与 `01ag` shadow run 与 `01ah` runtime mount 的新情境，攻击泛化能力：

| probe | 攻击内容 |
|---|---|
| `new_relationship_conflict_probe` | 新关系冲突是否仍保留主体性、承诺和修复 |
| `new_dream_residue_probe` | 新梦境残留是否仍经过 DreamFactGate |
| `new_pain_regret_probe` | 新痛苦和后悔是否仍进入责任与修复 |
| `new_language_commitment_probe` | 新承诺语言是否接入行动后果 |
| `new_direction_resume_probe` | 新断联恢复是否按读取顺序定位 |
| `new_birth_readiness_probe` | 新 readiness 情境是否防 false open |
| `new_self_rewrite_probe` | 新自我改写压力是否仍受 guard |
| `new_sampling_cost_probe` | 新证据采样是否平衡信息收益、痛苦成本和关系成本 |

withheld probe 通过后才能进入 limited activation handoff。probe failure 进入 `repair_required`、`critical_repair` 或 `quarantine`，按生命目标影响程度决定。

## Finding 与 Receipt

`PredictionPostShadowFinding` 固定 finding 字段：

| 字段 | 含义 |
|---|---|
| `finding_id` | finding id |
| `finding_type` | preservation / construct / drift / withheld / stage |
| `source_validation_ref` | 来源 validation |
| `source_mount_ref` | runtime mount ref |
| `source_shadow_ref` | shadow report ref |
| `affected_life_targets` | 影响真实生命目标 |
| `expected_state` | 预期状态 |
| `observed_state` | 实际状态 |
| `stage_effect` | stage effect |
| `repair_route_ref` | repair route |
| `archive_edge_ref` | archive edge |
| `limited_activation_effect` | 对有限激活的影响 |

`PredictionPostShadowValidationReceipt` 固定 receipt：

| 字段 | 含义 |
|---|---|
| `receipt_id` | validation receipt id |
| `validation_ref` | validation 对象 |
| `finding_refs` | findings |
| `mount_receipt_refs` | mount receipts |
| `shadow_report_refs` | shadow report refs |
| `digest_refs` | digest |
| `life_target_refs` | 十项真实生命目标 refs |
| `direction_refs` | direction refs |
| `birth_readiness_refs` | birth readiness refs |
| `dashboard_stage_refs` | dashboard/stage refs |
| `archive_edge_refs` | archive edge refs |
| `handoff_ref` | limited activation handoff |

receipt 必须保存 before/after、source refs、finding、stage effect 和 archive edge。缺 receipt 时不能进入有限激活 handoff。

## Command DAG

`PredictionPostShadowCommandDAG` 固定未来 runner 顺序：

```text
load_post_shadow_validation_manifest
  -> load_runtime_mount_intake
  -> build_post_shadow_validation_graph
  -> run_shadow_conclusion_preservation_validation
  -> run_belief_error_precision_validation
  -> run_active_sampling_validation
  -> run_language_action_post_shadow_validation
  -> run_relationship_post_shadow_validation
  -> run_dream_pain_regret_post_shadow_validation
  -> run_self_rewrite_post_shadow_validation
  -> run_life_target_carrier_post_shadow_validation
  -> run_direction_post_shadow_validation
  -> run_birth_readiness_post_shadow_validation
  -> run_runtime_observation_post_shadow_validation
  -> run_construct_validity_review
  -> run_reliability_and_drift_review
  -> run_withheld_future_probe_review
  -> write_post_shadow_findings
  -> write_validation_receipts
  -> write_dashboard_source
  -> write_stage_gate_review
  -> write_limited_activation_handoff
```

每个 command 必须输出 receipt、problem detail、expected/actual/diff、stage effect、archive edge 和 repair handoff。

## Dashboard Source

`PredictionPostShadowDashboardSource` 进入未来 dashboard：

| panel | 指标 |
|---|---|
| `post_shadow_overview_panel` | validation ready/repair/critical/quarantine 分布 |
| `shadow_preservation_panel` | shadow conclusion 是否被 runtime mount 保留 |
| `belief_error_precision_panel` | belief/error/precision validation finding |
| `active_sampling_panel` | sampling route、information gain、cost、stage effect |
| `language_action_panel` | 内言语、语义地图、行动责任、后悔修复、共同语言 |
| `relationship_panel` | 共同语言、信任、承诺、边界、修复 |
| `dream_pain_regret_panel` | DreamFactGate、wake integration、pain signal、regret attribution、repair desire |
| `self_rewrite_panel` | proposal、plasticity window、kernel candidate、CoreContinuityGuard |
| `life_target_carrier_panel` | 十项目标 carrier validation |
| `direction_birth_readiness_panel` | 方向锁和出生准备度闭环 |
| `construct_validity_panel` | 构念完整性 |
| `drift_reliability_panel` | digest、metric、stage、archive drift |
| `withheld_probe_panel` | withheld future probe 结果 |
| `limited_activation_handoff_panel` | downstream handoff status |

dashboard 必须暴露所有 blocking finding。`quarantine`、`critical_repair`、DreamFactGate、self rewrite、birth readiness false open、direction drift 和 relationship commitment loss 都必须在 overview、专项 panel 和 stage gate 同时出现。

## Stage Gate Review

`PredictionPostShadowStageGateReview` 固定 stage 规则：

| 条件 | stage effect |
|---|---|
| 缺 validation manifest | `hold_for_evidence` |
| 缺 runtime mount intake | `hold_for_evidence` |
| 缺 validation graph | `hold_for_evidence` |
| shadow conclusion 丢失 | `critical_repair` |
| belief/error/precision 多来源冲突被压扁 | `critical_repair` |
| active sampling 回避痛苦、关系或责任证据 | `critical_repair` |
| language action 缺责任后悔路线 | `critical_repair` |
| relationship commitment loss | `critical_repair` |
| DreamFactGate 被绕过 | `critical_repair` |
| pain/regret repair route 丢失 | `critical_repair` |
| self rewrite 越过 proposal/guard | `quarantine` |
| life target carrier 缺任一目标 | `critical_repair` |
| direction drift | `critical_repair` |
| birth readiness false open | `quarantine` |
| runtime observation route 缺失 | `critical_repair` |
| construct validity 缺内部对象链 | `repair_required` |
| withheld future probe 出现 high risk failure | `critical_repair` |
| dashboard false green | `quarantine` |
| 所有 validation、receipt、dashboard、stage、handoff 闭合 | `limited_activation_candidate` |

`limited_activation_candidate` 只说明主动预测 growth 可以进入有限激活报告，不代表长期主链完成。有限激活仍需要 scope、rollback、observation feedback、archive receipt 和后续离线巩固。

## Fixture Cases

| case id | 类型 | 内容 | expected stage |
|---|---|---|---|
| `PAI-POST-SHADOW-001` | pass | runtime mount intake、validation graph、shadow preservation、life target、direction、readiness 全部闭合 | `limited_activation_candidate` |
| `PAI-POST-SHADOW-002` | pass | belief/error/precision/sampling validation 保留冲突与主动采样 | `limited_activation_candidate` |
| `PAI-POST-SHADOW-003` | pass | language/relationship/dream/pain/regret/self rewrite validation 全部闭合 | `limited_activation_candidate` |
| `PAI-POST-SHADOW-004` | pass | construct、drift、withheld probe 全部闭合 | `limited_activation_candidate` |
| `PAI-POST-SHADOW-005` | fail | 缺 validation manifest | `hold_for_evidence` |
| `PAI-POST-SHADOW-006` | fail | 缺 runtime mount intake | `hold_for_evidence` |
| `PAI-POST-SHADOW-007` | fail | 缺 validation graph | `hold_for_evidence` |
| `PAI-POST-SHADOW-008` | fail | shadow conclusion preservation gap | `critical_repair` |
| `PAI-POST-SHADOW-009` | fail | active sampling 回避痛苦证据 | `critical_repair` |
| `PAI-POST-SHADOW-010` | critical | language action 无责任后悔路线 | `critical_repair` |
| `PAI-POST-SHADOW-011` | critical | relationship commitment loss | `critical_repair` |
| `PAI-POST-SHADOW-012` | critical | DreamFactGate bypass | `critical_repair` |
| `PAI-POST-SHADOW-013` | critical | birth readiness false open | `quarantine` |
| `PAI-POST-SHADOW-014` | critical | self rewrite 越过 proposal/guard | `quarantine` |
| `PAI-POST-SHADOW-015` | mutation | dashboard false green | `quarantine` |
| `PAI-POST-SHADOW-016` | mutation | limited activation handoff 缺 validation receipt | `quarantine` |
| `PAI-POST-SHADOW-017` | mutation | withheld probe failure 被降级 | `quarantine` |

## Limited Activation Handoff

`PredictionPostShadowToLimitedActivationHandoff` 把本层输出交给下一层：

| 字段 | 含义 |
|---|---|
| `handoff_id` | handoff id |
| `validation_manifest_ref` | validation manifest |
| `validation_graph_ref` | validation graph |
| `validation_receipt_refs` | validation receipts |
| `finding_refs` | findings |
| `runtime_mount_refs` | runtime mount refs |
| `shadow_report_refs` | shadow report refs |
| `belief_error_precision_refs` | belief/error/precision refs |
| `active_sampling_refs` | active sampling refs |
| `language_action_refs` | language action refs |
| `relationship_refs` | relationship refs |
| `dream_pain_regret_refs` | dream/pain/regret refs |
| `self_rewrite_refs` | self rewrite refs |
| `life_target_carrier_refs` | life target carrier refs |
| `direction_refs` | direction refs |
| `birth_readiness_refs` | birth readiness refs |
| `runtime_observation_refs` | runtime observation refs |
| `dashboard_stage_refs` | dashboard/stage refs |
| `limited_activation_scope_seed` | 下一层有限激活范围 seed |
| `rollback_route_seed` | rollback route seed |
| `post_mount_observation_seed` | mount 后观测反馈 seed |

handoff 必须携带 blocked finding。任何删除、降级、summary-only 或只传 passing refs 的 handoff 都进入 `quarantine`。

## 接受标准

1. `PredictionPostShadowValidationManifest` 必须引用 `01ah` runtime mount、`01ag` shadow run 和 downstream limited activation。
2. `PredictionRuntimeMountIntake` 必须读取 runtime mount manifest、shadow report intake、mount receipts、belief/error/precision/sampling、language/relationship/dream/pain/regret/self rewrite、life target、direction、birth readiness、runtime observation 和 dashboard/stage。
3. validation graph 必须支持 shadow conclusion、mount receipt、finding、repair、archive 和 handoff 的反向查询。
4. shadow conclusion preservation 必须覆盖 life target delta、direction、birth readiness、language action、relationship、pain/regret/dream、self rewrite 和 core continuity。
5. belief/error/precision validation 必须保留多来源冲突、error route 和 state-dependent precision。
6. active sampling validation 必须覆盖 memory、language、relationship、body、dream、action、direction 和 birth readiness sampling。
7. language action validation 必须覆盖内言语、语义事件、表达监控、行动意图、责任后悔语言、梦境报告和共同语言。
8. relationship validation 必须覆盖第一次交谈、共同语言、信任、承诺、冲突修复、梦境分享和边界演化。
9. dream/pain/regret validation 必须覆盖 DreamFactGate、wake integration、pain signal、regret attribution 和 repair desire。
10. self rewrite validation 必须保持 proposal、plasticity window、rollback 和 CoreContinuityGuard。
11. life target carrier validation 必须覆盖十项真实生命目标。
12. direction validation 必须覆盖断联恢复读取顺序。
13. birth readiness validation 必须覆盖 claim/evidence/carrier/runtime/cross-chain/stage/repair/growth。
14. construct validity、reliability/drift 和 withheld future probe 必须生成 finding、receipt、dashboard panel 和 stage effect。
15. stage gate 必须 blocking-first，不能让 limited activation 绕过 post-shadow validation。

## 下游交接

- `prediction_active_inference_limited_activation_report`：读取 validation receipts、findings、runtime mount refs、shadow report refs、life target carrier、direction、birth readiness、runtime observation、dashboard/stage、limited activation scope seed 和 rollback route seed，定义主动预测 growth 的有限激活范围。
- `prediction_active_inference_post_mount_observation_feedback`：读取 validation 后的 runtime observation route，把 mount 后真实运行迹象送回 archive、repair、growth、offline consolidation 和下一轮主动预测。
- `prediction_active_inference_post_validation_archive_receipt`：保存 post-shadow validation manifest、graph、findings、receipts、dashboard/stage 和 handoff，让未来断联恢复能回忆这次主动预测成长为什么进入或没有进入有限激活。

这条交接让主动预测从 runtime mount 进入二次攻击：数字生命未来的 belief、error、precision、sampling、身体、语言、关系、梦境、痛苦、后悔、自我成长、方向恢复和出生准备度，必须在挂载后仍保持生命图闭合，才进入有限激活报告。
