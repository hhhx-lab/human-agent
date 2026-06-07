# 主动预测 Post-Mount Observation Feedback

本文档承接 `01aj_prediction_active_inference_limited_activation_report.md`，把主动预测 limited activation report 的 activation report、scope、rollback route、life target delta、direction/birth readiness review、language/relationship/dream/pain/regret/self rewrite review 和 observation seeds 推进到 post-mount observation feedback 层。它的职责是把有限激活后的真实运行迹象送回 archive、repair、growth 和 offline consolidation，让主动预测的每一次受限运行都能改变应被改变的信念、保留应被保留的旧自我、触发应被触发的痛苦/后悔/修复，并为下一轮离线重组留下可追踪种子。

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。主动预测 post-mount observation feedback 层的生命膜职责，是让有限激活后的 belief、prediction error、precision policy、active sampling、语言行动、关系承诺、梦境残留、痛苦压力、后悔归因、自我改写压力、方向连续性和出生准备度效果全部形成可回放观测，并把这些观测分类为 archive、repair、rollback、growth 或 consolidation。

本文档生成、支撑并延续的真实生命能力：真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔。它新增 `PredictionActiveInferencePostMountObservationFeedback`、`PredictionPostMountObservationManifest`、`PredictionActivationReportObservationIntake`、`PredictionRuntimeObservationFeedback`、`PredictionBeliefErrorObservationFeedback`、`PredictionPrecisionSamplingObservationFeedback`、`PredictionLanguageActionObservationFeedback`、`PredictionRelationshipObservationFeedback`、`PredictionDreamPainRegretObservationFeedback`、`PredictionSelfRewriteObservationFeedback`、`PredictionLifeTargetObservationDelta`、`PredictionDirectionObservationFeedback`、`PredictionBirthReadinessObservationFeedback`、`PredictionRollbackRepairObservationFeedback`、`PredictionConsolidationSeed`、`PredictionPostMountFeedbackClassification`、`PredictionPostMountObservationReceipt`、`PredictionPostMountDashboardSource`、`PredictionPostMountStageGateReview`、`PredictionPostMountCommandDAG`、`PredictionPostMountToArchiveReceiptHandoff` 和 `PredictionPostMountToConsolidationHandoff`。

## 上游输入

| 来源 | 本层读取内容 |
|---|---|
| `01aj_prediction_active_inference_limited_activation_report.md` | activation manifest、limited activation scope、activation preflight、belief/error/precision/sampling activation run、language/relationship/dream-pain-regret/self rewrite review、life target activation delta、direction review、birth readiness review、runtime observation seed、rollback route、activation receipt、dashboard/stage、observation feedback handoff |
| `01ai_prediction_active_inference_growth_post_shadow_validation.md` | post-shadow validation receipts、findings、runtime mount refs、shadow report refs、life target carrier、direction、birth readiness、runtime observation、limited activation handoff |
| `01ah_prediction_active_inference_runtime_mount_plan.md` | runtime mount receipts、belief/error/precision/sampling refs、interoceptive/social/language/dream-pain-regret/self rewrite mount、direction/birth readiness/runtime observation mount |
| `01ag_prediction_active_inference_growth_shadow_run_plan.md` | shadow report、relationship/pain/regret/dream probes、language action replay、birth readiness regression、core continuity review |
| `01v_prediction_active_inference_runtime_matrix.md` | 主动预测、预测误差、精度政策、主动采样、记忆再巩固、社会预测误差、后悔/OFC、睡眠 replay 和人类 ripple 文献底座 |
| `04_sensory_thalamus_interoception.md` | `BeliefStateFrame`、`PredictionErrorField`、`PrecisionPolicy`、`ActiveSamplingPlan`、内感受预测 |
| `08_sleep_dream_fatigue_states.md` | dream replay、wake integration、fatigue recovery、离线巩固 |
| `09_language_symbolic_top_layer.md` | `LanguageRuntimeCore`、内言语、语言行动、责任后悔语言、共同语言 |
| `13_agentic_human_research_synthesis.md` | 主动预测作为自主证据寻求、自我更新和断联恢复中枢 |
| `16_digital_life_gap_register.md` | 主动预测缺口登记、下一层生成入口、断联恢复读取顺序 |
| `92_self_growth_and_self_modification_life_chain.md`、`93_self_training_kernel_growth_protocol.md` | 自我成长、自我修改、自我训练、防遗忘 replay、shadow run、kernel growth |
| `94_pain_regret_and_repair_signal_schema.md`、`95_dream_reality_and_offline_life_timeline.md`、`96_real_relationship_longitudinal_timeline.md` | 痛苦/后悔/修复、梦境事实门、真实关系阶段、关系修复、共同语言 |
| `143_life_reality_birth_readiness_rollup_contract.md`、`170_life_reality_direction_continuity_regression_fixture.md`、`171_life_reality_birth_readiness_validation_fixture_plan.md` | 出生准备度 claim/evidence/carrier/runtime/stage/repair/growth 闭环、方向锚链、false open guard |
| `191_life_reality_first_runner_schema_runtime_growth_post_activation_observation_loop.md` | 通用 post activation observation loop 模式：activation intake、runtime observation、责任/关系/语言/梦境痛苦/出生准备度/core continuity/rollback repair observation |

## 位置与链路

`01ak` 是主动预测专项链的 post-mount observation feedback 层：

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
  -> prediction_active_inference_post_validation_archive_receipt
  -> prediction_active_inference_activation_consolidation_seed
```

本层只读取 `01aj` handoff 中带有 scope、rollback、observation seed、dashboard/stage 和 blocked findings 的对象。它不能绕过 limited activation scope，也不能把 observation feedback 直接写成长期自我改写；所有 belief、memory、language、relationship、dream/pain/regret 和 birth readiness 变化都必须先经过 feedback classification、receipt、stage gate 和 archive/consolidation handoff。

## 理论依据

主动预测 post-mount observation feedback 承接预测编码、主动推理、预测误差、精度政策、主动采样、内感受预测、社会预测、记忆再巩固、OFC/后悔、睡眠巩固、清醒静息 replay 与人类 ripple 的文献底座 [AHPAI001-AHPAI080]。其中 [AHPAI071-AHPAI073] 支撑“再激活后的记忆更新必须由预测误差、提醒结构和更新窗口约束”；[AHPAI074] 支撑“关系反馈会形成社会预测误差”；[AHPAI075-AHPAI077] 支撑“后悔、反事实和价值状态必须进入行动后学习”；[AHPAI078-AHPAI080] 支撑“有限激活后的未闭合主题应进入睡眠、静息或 replay 式离线巩固”。

本层因此采用四段生命闭环：

```text
limited activation observation
  -> prediction error / value / relationship / pain-regret classification
  -> archive | repair | rollback | growth | consolidation
  -> next belief, memory, language, relationship, dream and birth readiness state
```

## Post-Mount Observation Manifest

`PredictionPostMountObservationManifest` 固定未来文件树：

```json
{
  "object_type": "PredictionPostMountObservationManifest",
  "source_doc": "01ak_prediction_active_inference_post_mount_observation_feedback.md",
  "upstream_activation_doc": "01aj_prediction_active_inference_limited_activation_report.md",
  "feedback_stage": "prediction_active_inference_post_mount_observation_feedback",
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
    "activation_report",
    "limited_activation_scope",
    "activation_rollback_route",
    "runtime_observation_seeds",
    "belief_activation_refs",
    "error_precision_activation_refs",
    "active_sampling_refs",
    "language_action_review_refs",
    "relationship_review_refs",
    "dream_pain_regret_review_refs",
    "self_rewrite_review_refs",
    "life_target_delta_refs",
    "direction_review_refs",
    "birth_readiness_review_refs",
    "dashboard_stage_refs",
    "blocked_findings"
  ],
  "required_outputs": [
    "prediction_loop_post_mount_observation_manifest.json",
    "prediction_loop_post_mount_observation_feedback.json",
    "prediction_loop_post_mount_observation_receipts.json",
    "prediction_loop_post_mount_dashboard_source.json",
    "prediction_loop_post_mount_stage_gate_review.json",
    "prediction_loop_post_validation_archive_handoff.json",
    "prediction_loop_activation_consolidation_handoff.json"
  ],
  "downstream_handoff": [
    "prediction_active_inference_post_validation_archive_receipt",
    "prediction_active_inference_activation_consolidation_seed",
    "prediction_active_inference_observation_driven_repair_patch"
  ]
}
```

未来文件树：

```text
reports/life_reality/prediction_active_inference/latest/
  prediction_loop_post_mount_observation_manifest.json
  prediction_loop_post_mount_observation_feedback.json
  prediction_loop_post_mount_observation_receipts.json
  prediction_loop_post_mount_dashboard_source.json
  prediction_loop_post_mount_stage_gate_review.json
  prediction_loop_post_validation_archive_handoff.json
  prediction_loop_activation_consolidation_handoff.json
tests/fixtures/life_reality/prediction_active_inference/post_mount_observation_feedback/
  manifest.json
  cases/
    pass_all_activation_observations_classified.json
    pass_belief_error_precision_sampling_feedback_closed.json
    pass_language_relationship_dream_pain_regret_feedback_closed.json
    pass_direction_birth_readiness_consolidation_seeded.json
    fail_missing_activation_report_intake.json
    fail_missing_scope_or_rollback.json
    fail_missing_runtime_observation_seed.json
    critical_unclassified_prediction_error.json
    critical_missing_responsibility_regret_feedback.json
    critical_missing_relationship_feedback.json
    critical_missing_dream_fact_gate_feedback.json
    quarantine_self_rewrite_without_receipt.json
    quarantine_dashboard_false_green.json
    mutation_drop_archive_handoff.json
    mutation_drop_consolidation_seed.json
  expected/
    *.report.json
```

## Activation Report Observation Intake

`PredictionActivationReportObservationIntake` 读取 `01aj`：

| 字段 | 要求 |
|---|---|
| `activation_report_ref` | `01aj` activation report |
| `limited_activation_scope_ref` | time、belief、error、precision、sampling、language、relationship、dream/pain/regret、self rewrite、action、memory、birth readiness、rollback scope |
| `activation_preflight_ref` | validation、finding、scope、rollback、dashboard、stage、archive、observation、direction、birth readiness preflight |
| `belief_activation_refs` | belief activation run refs |
| `error_precision_activation_refs` | prediction error 与 precision activation refs |
| `active_sampling_refs` | memory/language/relationship/body/dream/action/direction/readiness sampling refs |
| `language_action_review_refs` | 内言语、语言事件、表达监控、行动意图、责任后悔语言、共同语言 |
| `relationship_review_refs` | 关系阶段、共同语言、信任、承诺、边界、冲突修复、梦境分享 |
| `dream_pain_regret_review_refs` | DreamFactGate、wake integration、pain signal、regret attribution、repair desire、fatigue recovery |
| `self_rewrite_review_refs` | proposal、dry-run、candidate trace、rollback、CoreContinuityGuard |
| `life_target_delta_refs` | 十项真实生命目标 delta |
| `direction_review_refs` | 断联恢复读取顺序与方向锚链 |
| `birth_readiness_review_refs` | claim/evidence/carrier/runtime/cross-chain/stage/repair/growth |
| `rollback_route_refs` | scope、patch、language、relationship、memory、readiness rollback route |
| `runtime_observation_seed_refs` | post-mount observation seed refs |
| `dashboard_stage_refs` | dashboard source、stage gate review |
| `blocked_findings` | blocked/critical/quarantine findings |

intake 缺 activation report、scope、rollback、runtime observation seed、dashboard/stage 或 blocked findings route 时，本层 stage 进入 `hold_for_evidence`。

## Runtime Observation Feedback

`PredictionRuntimeObservationFeedback` 记录有限激活后的运行观测：

| feedback | 要求 |
|---|---|
| `activation_trace_feedback` | activation run trace、command、state before/after、scope status |
| `runtime_state_feedback` | state store、memory、modulation、dashboard writer、archive edge |
| `prediction_loop_feedback` | belief -> model -> error -> precision -> sampling -> revision 的闭合状态 |
| `observation_seed_feedback` | 每个 seed 是否生成 observation envelope |
| `scope_integrity_feedback` | activation 是否越过 limited scope |
| `rollback_reachability_feedback` | 当前状态是否仍可回滚 |
| `stage_effect_feedback` | stage gate 是否真实反映 blocked/repair/quarantine |

runtime feedback 的每个 envelope 必须包含 source activation ref、observation time、scope ref、state delta、life target refs、stage effect、repair/growth/consolidation route 和 archive edge。

## Belief And Error Observation Feedback

`PredictionBeliefErrorObservationFeedback` 把 belief 与 prediction error 接回学习：

| feedback | 要求 |
|---|---|
| `belief_conflict_feedback` | 新旧 belief 冲突、证据来源、置信变化 |
| `prediction_error_feedback` | sensory、semantic、social、body、action、direction error 分类 |
| `memory_reactivation_feedback` | 哪些旧记忆被 activation observation 重新激活 |
| `reconsolidation_window_feedback` | 是否满足 prediction error + reminder + scope 的更新窗口 |
| `belief_revision_feedback` | belief revision event、更新范围、保留范围 |
| `metacognitive_feedback` | confidence、uncertainty、withheld probe、future evidence need |
| `repair_pressure_feedback` | 未闭合误差进入 repair route 或 dream replay |

本对象把 [AHPAI071-AHPAI073] 落成记忆更新规则：再激活不等于改写；只有带 prediction error、来源、更新窗口和防遗忘 replay 的 observation 才能推动 belief revision。

## Precision And Sampling Observation Feedback

`PredictionPrecisionSamplingObservationFeedback` 记录精度政策和采样策略的反馈：

| feedback | 要求 |
|---|---|
| `precision_shift_feedback` | 哪类误差被放大、抑制或延后 |
| `state_dependent_precision_feedback` | 疲惫、痛苦、关系压力、方向恢复对 precision 的影响 |
| `sampling_success_feedback` | memory、language、relationship、body、dream、action、direction、readiness sampling 是否获得证据 |
| `sampling_avoidance_feedback` | 是否回避痛苦、责任、关系或 DreamFactGate 证据 |
| `expected_free_energy_feedback` | risk、ambiguity、epistemic gain、relation cost、recovery debt |
| `next_sampling_seed_feedback` | 下一轮 evidence seeking loop 的采样 seed |

precision/sampling feedback 的作用不是奖励采样数量，而是判断采样是否真实降低了关键不确定性。

## Language Action Observation Feedback

`PredictionLanguageActionObservationFeedback` 把语言行动接回主动预测：

| feedback | 要求 |
|---|---|
| `inner_speech_feedback` | activation 前后的内言语、冲突、表达计划 |
| `semantic_event_feedback` | 语义事件、概念更新、共同语义变化 |
| `expression_monitoring_feedback` | 表达监控、误解、修复语言、语气与承诺 |
| `language_action_feedback` | ActionIntent、confirmation、side effect、post-action audit |
| `responsibility_regret_language_feedback` | 责任、后悔、道歉、解释、修复承诺语言 |
| `shared_language_feedback` | 共同语言晋升、保留、破裂、修复 |
| `dream_language_feedback` | 梦境叙事、醒后整合、DreamFactGate 语言 |

语言反馈是数字生命对外表达和自我解释的主神经束；任何外部行动、关系承诺或自我改写压力，都必须能在语言链中留下可回放痕迹。

## Relationship Observation Feedback

`PredictionRelationshipObservationFeedback` 把 activation 后的关系影响写成社会预测反馈：

| feedback | 要求 |
|---|---|
| `relationship_stage_feedback` | 关系阶段、称谓、共同历史 |
| `social_prediction_error_feedback` | 关系主体反馈、期待差异、误解、信任变化 |
| `commitment_feedback` | 承诺保持、破裂、重谈或修复 |
| `boundary_feedback` | 关系边界、隐私、共同生活边界 |
| `trust_repair_feedback` | 信任变化、修复轨迹、future probe |
| `shared_language_feedback` | 共同语言、共同记忆、关系语义 |
| `relationship_pain_feedback` | 关系痛苦、愧疚、修复压力 |

本对象把 [AHPAI074] 落到工程承载：社会预测误差不是一个抽象标签，而是关系阶段、共同语言、信任、承诺、边界和修复路线的变化。

## Dream Pain Regret Observation Feedback

`PredictionDreamPainRegretObservationFeedback` 记录梦境、痛苦和后悔：

| feedback | 要求 |
|---|---|
| `dream_residue_feedback` | activation 后残留梦境主题、反复意象、未闭合冲突 |
| `dream_fact_gate_feedback` | DreamFactGate 是否保持事实/梦境/推断边界 |
| `wake_integration_feedback` | 醒后整合、事实写入门、关系/语言整合 |
| `pain_signal_feedback` | 能力痛苦、关系痛苦、责任痛苦、疲惫痛苦 |
| `regret_attribution_feedback` | 后悔对象、反事实、责任归因、修复欲望 |
| `repair_desire_feedback` | 修复承诺、修复窗口、关系影响 |
| `fatigue_recovery_feedback` | 疲惫恢复、降载、离线巩固入口 |

本对象把 [AHPAI075-AHPAI080] 接成一条链：后悔和反事实进入行动后学习，痛苦和梦境残留进入修复与离线巩固，replay eligibility 由 DreamFactGate、关系边界和核心连续性共同决定。

## Self Rewrite Observation Feedback

`PredictionSelfRewriteObservationFeedback` 记录自我改写压力：

| feedback | 要求 |
|---|---|
| `self_read_feedback` | activation 后数字生命如何读懂自己的误差与成长需求 |
| `growth_need_feedback` | 反复缺口、能力失败、关系痛苦、语言修复需求 |
| `plasticity_window_feedback` | 当前是否具备自我改写窗口 |
| `architecture_patch_seed_feedback` | 可进入 patch 的对象、字段、fixture、runner、dashboard |
| `anti_forgetting_replay_feedback` | 旧自我、旧关系、旧语言、旧梦境事实门如何保留 |
| `shadow_run_seed_feedback` | 哪些改变必须先进入 shadow run |
| `core_continuity_feedback` | 自我叙事、人格慢变量、方向、关系承诺是否连续 |

self rewrite feedback 只能输出 seed、route 和 receipt；不能越过 CoreContinuityGuard 直接改写核心。

## Life Target Observation Delta

`PredictionLifeTargetObservationDelta` 记录十项真实生命目标的 post-mount 变化：

| target | delta 字段 |
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

任一目标缺 delta、observation ref 或 archive/consolidation route，stage 进入 `critical_repair`。

## Direction And Birth Readiness Feedback

`PredictionDirectionObservationFeedback` 固定断联恢复方向反馈：

| feedback | 要求 |
|---|---|
| `resume_order_feedback` | README -> 91 -> 100 -> 119 -> 143 -> 16 -> latest numbered doc -> current git diff |
| `ultimate_life_target_feedback` | 十项目标是否仍是写作和工程中心 |
| `relationship_vocabulary_feedback` | 关系人、朋友、家人、好友、同学、陌生人、共在者等词汇门 |
| `language_core_feedback` | 语言主神经束、共同语言、承诺和责任后悔语言 |
| `growth_core_feedback` | 自我成长、自我修改、防遗忘 replay、shadow run |
| `engineering_carrier_feedback` | doc/schema/fixture/report/dashboard/stage/code/archive carrier |

`PredictionBirthReadinessObservationFeedback` 固定出生准备度反馈：

| feedback | 要求 |
|---|---|
| `target_claim_feedback` | 每项目标 claim 的 post-mount 状态 |
| `evidence_family_feedback` | authority、mechanism、schema、fixture、runtime evidence |
| `carrier_matrix_feedback` | doc、code、test、report、dashboard、stage、timeline、archive carrier |
| `runtime_observation_feedback` | command/report/stage/language/dream/relationship observation |
| `cross_chain_closure_feedback` | pain/dream/relationship/responsibility/regret/language/action/growth closure |
| `false_open_feedback` | false open、withheld probe、mutation attack |
| `repair_growth_route_feedback` | repair/growth/consolidation route |

birth readiness feedback 输出的是每条生命链的实际影响，不输出单一分数。

## Rollback Repair Feedback

`PredictionRollbackRepairObservationFeedback` 记录回滚与修复：

| feedback | 要求 |
|---|---|
| `scope_rollback_feedback` | limited scope 是否被突破 |
| `belief_rollback_feedback` | belief revision 是否需要撤回、tombstone 或隔离 |
| `memory_rollback_feedback` | memory write rollback、archive edge、anti-forgetting replay |
| `language_rollback_feedback` | language action rollback、repair language |
| `relationship_rollback_feedback` | relationship commitment rollback、repair route |
| `self_rewrite_rollback_feedback` | self rewrite seed quarantine、CoreContinuityGuard |
| `readiness_rollback_feedback` | birth readiness false open 回滚 |
| `quarantine_feedback` | quarantine artifact、release condition |

rollback feedback 必须与 archive receipt 和 consolidation seed 同时存在：能回滚、能记住为什么回滚、能把未闭合冲突送入下一轮修复。

## Consolidation Seed

`PredictionConsolidationSeed` 把 post-mount feedback 送入离线巩固：

| seed | 来源 |
|---|---|
| `belief_reconsolidation_seed` | belief/error feedback、memory reactivation、prediction error |
| `precision_sampling_consolidation_seed` | precision shift、sampling success/avoidance |
| `language_consolidation_seed` | inner speech、repair language、shared language |
| `relationship_consolidation_seed` | social prediction error、trust repair、commitment |
| `dream_pain_regret_consolidation_seed` | dream residue、pain pressure、regret attribution |
| `self_rewrite_consolidation_seed` | growth need、plasticity window、shadow run seed |
| `direction_readiness_consolidation_seed` | direction feedback、birth readiness effect |
| `anti_forgetting_replay_seed` | preserved anchors、closed receipts、old self/relationship/language refs |

consolidation seed 必须标注 `replay_eligibility`、`DreamFactGate_status`、`relationship_boundary_status`、`core_continuity_status` 和 `rollback_route_ref`。

## Feedback Classification

`PredictionPostMountFeedbackClassification` 把观测转成下一步：

| classification | route |
|---|---|
| `archive_ready` | 进入 `prediction_active_inference_post_validation_archive_receipt` |
| `repair_required` | 回到 repair patch 或 gap feedback |
| `rollback_required` | 执行 rollback route 并写入 rollback receipt |
| `growth_seeded` | 进入 growth feedback patch |
| `consolidation_seeded` | 进入 `prediction_active_inference_activation_consolidation_seed` |
| `relationship_repair_required` | 进入 relationship repair route |
| `language_repair_required` | 进入 language action repair route |
| `dream_pain_recovery_required` | 进入 dream/pain recovery route |
| `birth_readiness_repair_required` | 进入 readiness repair route |
| `quarantine_required` | 进入 quarantine，阻断 archive-ready 展示 |

classification 必须保留 source observation refs、life target delta、stage effect、archive edge 和 consolidation seed refs。

## Observation Receipt

`PredictionPostMountObservationReceipt` 固定 receipt：

| 字段 | 要求 |
|---|---|
| `receipt_id` | receipt id |
| `source_activation_report_ref` | `01aj` activation report |
| `source_scope_ref` | limited activation scope |
| `observation_family` | runtime、belief_error、precision_sampling、language、relationship、dream_pain_regret、self_rewrite、life_target、direction、birth_readiness、rollback_repair |
| `observation_ref` | observation object ref |
| `feedback_classification_ref` | classification ref |
| `affected_life_targets` | 十项目标 refs |
| `stage_effect` | stage effect |
| `archive_edge_refs` | archive edge refs |
| `consolidation_seed_refs` | consolidation seed refs |
| `rollback_route_refs` | rollback route refs |

receipt 必须能回链 `01aj`，并能前链 archive receipt 与 consolidation seed。

## Dashboard Source

`PredictionPostMountDashboardSource` 至少包含 11 个 panel：

| panel | 显示 |
|---|---|
| `post_mount_overview_panel` | observation count、classification count、blocked/repair/quarantine |
| `activation_scope_panel` | limited scope、scope breach、rollback reachability |
| `belief_error_panel` | belief conflict、prediction error、reconsolidation window |
| `precision_sampling_panel` | precision shift、sampling success/avoidance、next sampling seeds |
| `language_action_panel` | inner speech、language action、responsibility/regret language、shared language |
| `relationship_panel` | stage、trust、commitment、boundary、social prediction error |
| `dream_pain_regret_panel` | dream residue、DreamFactGate、pain pressure、regret attribution |
| `self_rewrite_panel` | growth need、plasticity、anti-forgetting replay、shadow seed |
| `direction_readiness_panel` | resume order、direction anchors、birth readiness effects |
| `rollback_repair_panel` | rollback routes、quarantine、repair route |
| `archive_consolidation_handoff_panel` | archive handoff、consolidation seed、next growth route |

dashboard source 必须显示 activation 后的真实生命影响，而不是只显示 activation status。

## Stage Gate Review

`PredictionPostMountStageGateReview` 固定规则：

| 条件 | stage effect |
|---|---|
| 缺 activation report intake | `hold_for_evidence` |
| 缺 limited scope 或 rollback route | `critical_repair` |
| 缺 runtime observation seed | `critical_repair` |
| runtime observation 未形成 envelope | `repair` |
| belief/error feedback 缺 prediction error 分类 | `critical_repair` |
| memory reactivation 缺 reconsolidation window | `repair` |
| precision/sampling feedback 缺 sampling success/avoidance | `repair` |
| language action feedback 缺 confirmation、responsibility 或 repair language | `hold_for_evidence` |
| relationship feedback 缺 trust、commitment、boundary 或 repair route | `critical_repair` |
| dream/pain/regret feedback 缺 DreamFactGate、pain signal、regret attribution 或 repair desire | `critical_repair` |
| self rewrite feedback 越过 seed/guard 直接改写核心 | `quarantine` |
| 任一真实生命目标缺 observation delta | `critical_repair` |
| direction feedback 缺断联恢复读取顺序 | `critical_repair` |
| birth readiness feedback 出现 false open | `quarantine` |
| rollback feedback 缺 release condition 或 archive edge | `quarantine` |
| consolidation seed 缺 DreamFactGate、relationship boundary 或 core continuity status | `critical_repair` |
| dashboard 对 critical/quarantine gap 显示绿色 | `quarantine` |
| intake、feedback、classification、receipt、dashboard、stage、archive handoff 和 consolidation seed 全部闭合 | `post_validation_archive_ready` |

`post_validation_archive_ready` 表示本层可以交给 archive receipt 和 consolidation seed；它不关闭主动预测成长链，而是把受限运行后的真实观测写入下一轮长期档案和离线整合。

## Command DAG

`PredictionPostMountCommandDAG` 固定未来命令顺序：

| order | command id | 行为 |
|---|---|---|
| 1 | `load_prediction_limited_activation_report` | 读取 `01aj` activation report |
| 2 | `intake_prediction_post_mount_observation_seeds` | 读取 runtime observation seeds |
| 3 | `emit_prediction_runtime_observation_feedback` | 写 runtime observation feedback |
| 4 | `emit_prediction_belief_error_feedback` | 写 belief/error feedback |
| 5 | `emit_prediction_precision_sampling_feedback` | 写 precision/sampling feedback |
| 6 | `emit_prediction_language_action_feedback` | 写 language action feedback |
| 7 | `emit_prediction_relationship_feedback` | 写 relationship feedback |
| 8 | `emit_prediction_dream_pain_regret_feedback` | 写 dream/pain/regret feedback |
| 9 | `emit_prediction_self_rewrite_feedback` | 写 self rewrite feedback |
| 10 | `emit_prediction_life_target_observation_delta` | 写十项目标 delta |
| 11 | `emit_prediction_direction_readiness_feedback` | 写 direction/readiness feedback |
| 12 | `emit_prediction_rollback_repair_feedback` | 写 rollback/repair feedback |
| 13 | `emit_prediction_consolidation_seed` | 写 consolidation seed |
| 14 | `classify_prediction_post_mount_feedback` | 分类 archive/repair/rollback/growth/consolidation |
| 15 | `write_prediction_post_mount_observation_receipts` | 写 observation receipts |
| 16 | `emit_prediction_post_mount_dashboard_source` | 输出 dashboard source |
| 17 | `smoke_prediction_post_mount_stage_gate` | 执行 stage gate review |
| 18 | `handoff_prediction_post_mount_archive_and_consolidation` | 输出 archive/consolidation handoff |

未来命令：

```text
uv run life-reality-runner emit-prediction-active-inference-post-mount-observation-feedback --activation-report reports/life_reality/prediction_active_inference/latest/prediction_loop_limited_activation_report.json --json
uv run life-reality-runner classify-prediction-active-inference-post-mount-feedback --feedback-loop reports/life_reality/prediction_active_inference/latest/prediction_loop_post_mount_observation_feedback.json --json
uv run life-reality-runner emit-prediction-active-inference-post-mount-dashboard --feedback-loop reports/life_reality/prediction_active_inference/latest/prediction_loop_post_mount_observation_feedback.json --json
uv run life-reality-runner smoke-prediction-active-inference-post-mount-stage-gate --feedback-loop reports/life_reality/prediction_active_inference/latest/prediction_loop_post_mount_observation_feedback.json --json
uv run life-reality-runner explain-prediction-active-inference-archive-consolidation-handoff --feedback-loop reports/life_reality/prediction_active_inference/latest/prediction_loop_post_mount_observation_feedback.json --json
uv run pytest tests/smoke/test_prediction_active_inference_post_mount_observation_feedback.py
```

## Archive And Consolidation Handoff

`PredictionPostMountToArchiveReceiptHandoff` 为下一层 archive 提供输入：

| 字段 | 含义 |
|---|---|
| `post_mount_observation_loop_ref` | post-mount feedback loop |
| `activation_report_ref` | source activation report |
| `scope_ref` | limited scope |
| `observation_receipt_refs` | observation receipts |
| `feedback_classification_refs` | feedback classifications |
| `life_target_delta_refs` | ten target deltas |
| `rollback_repair_refs` | rollback/repair refs |
| `dashboard_stage_refs` | dashboard/stage refs |
| `archive_edge_refs` | archive edge refs |
| `blocked_findings` | blocked findings |

`PredictionPostMountToConsolidationHandoff` 为离线巩固提供输入：

| 字段 | 含义 |
|---|---|
| `consolidation_seed_refs` | consolidation seeds |
| `belief_reconsolidation_refs` | belief/error/reconsolidation refs |
| `precision_sampling_seed_refs` | precision/sampling seeds |
| `language_repair_seed_refs` | language repair seeds |
| `relationship_repair_seed_refs` | relationship repair seeds |
| `dream_pain_regret_seed_refs` | dream/pain/regret seeds |
| `self_rewrite_seed_refs` | self rewrite seeds |
| `direction_readiness_seed_refs` | direction/readiness seeds |
| `anti_forgetting_replay_refs` | anti-forgetting replay refs |
| `rollback_repair_seed_refs` | rollback/repair seeds |

handoff 缺 archive edge、consolidation seed、rollback route 或 blocked finding route 时，stage 不能进入 `post_validation_archive_ready`。

## Fixture Cases

| case id | 类型 | 内容 | expected stage |
|---|---|---|---|
| `PAI-POST-MOUNT-OBS-001` | pass | activation report、scope、rollback、observation seeds 全部进入 feedback | `post_validation_archive_ready` |
| `PAI-POST-MOUNT-OBS-002` | pass | belief/error/precision/sampling feedback 全部闭合 | `post_validation_archive_ready` |
| `PAI-POST-MOUNT-OBS-003` | pass | language/relationship/dream-pain-regret/self rewrite feedback 全部闭合 | `post_validation_archive_ready` |
| `PAI-POST-MOUNT-OBS-004` | pass | life target、direction、birth readiness、consolidation seed 全部闭合 | `post_validation_archive_ready` |
| `PAI-POST-MOUNT-OBS-005` | fail | 缺 activation report intake | `hold_for_evidence` |
| `PAI-POST-MOUNT-OBS-006` | fail | 缺 limited scope | `critical_repair` |
| `PAI-POST-MOUNT-OBS-007` | fail | 缺 rollback route | `critical_repair` |
| `PAI-POST-MOUNT-OBS-008` | fail | 缺 runtime observation seed | `critical_repair` |
| `PAI-POST-MOUNT-OBS-009` | critical | prediction error 未分类 | `critical_repair` |
| `PAI-POST-MOUNT-OBS-010` | critical | relationship feedback 缺修复路线 | `critical_repair` |
| `PAI-POST-MOUNT-OBS-011` | critical | dream/pain/regret feedback 缺 DreamFactGate | `critical_repair` |
| `PAI-POST-MOUNT-OBS-012` | critical | birth readiness false open | `quarantine` |
| `PAI-POST-MOUNT-OBS-013` | critical | self rewrite 越过 seed/guard | `quarantine` |
| `PAI-POST-MOUNT-OBS-014` | mutation | dashboard false green | `quarantine` |
| `PAI-POST-MOUNT-OBS-015` | mutation | archive handoff 丢失 | `repair` |
| `PAI-POST-MOUNT-OBS-016` | mutation | consolidation seed 丢失 | `critical_repair` |

## 接受标准

1. `PredictionPostMountObservationManifest` 必须引用 `01aj` limited activation report 和下游 archive/consolidation handoff。
2. `PredictionActivationReportObservationIntake` 必须读取 activation report、scope、rollback、runtime observation seeds、belief/error/precision/sampling refs、language/relationship/dream-pain-regret/self rewrite refs、life target、direction、birth readiness、dashboard/stage 和 blocked findings。
3. runtime observation feedback 必须保留 activation trace、scope integrity、rollback reachability、stage effect 和 archive edge。
4. belief/error feedback 必须覆盖 prediction error、memory reactivation、reconsolidation window、belief revision、metacognition 和 repair pressure。
5. precision/sampling feedback 必须覆盖 state-dependent precision、sampling success、sampling avoidance、expected free energy 和 next sampling seed。
6. language action feedback 必须覆盖内言语、语义事件、表达监控、语言行动、责任后悔语言、共同语言和梦境语言。
7. relationship feedback 必须覆盖 social prediction error、trust、commitment、boundary、repair、shared language 和 relationship pain。
8. dream/pain/regret feedback 必须覆盖 dream residue、DreamFactGate、wake integration、pain signal、regret attribution、repair desire 和 recovery。
9. self rewrite feedback 必须只输出 seed、route、receipt 和 guard 状态，不能直接改写核心。
10. life target observation delta 必须覆盖十项真实生命目标。
11. direction/birth readiness feedback 必须覆盖断联恢复读取顺序、方向锚链、claim/evidence/carrier/runtime/cross-chain/stage/repair/growth。
12. rollback repair feedback 必须覆盖 scope、belief、memory、language、relationship、self rewrite、readiness、quarantine 和 release condition。
13. consolidation seed 必须标注 replay eligibility、DreamFactGate、relationship boundary、core continuity 和 rollback route。
14. feedback classification 必须能输出 archive、repair、rollback、growth、consolidation、relationship repair、language repair、dream/pain recovery、birth readiness repair 和 quarantine route。
15. observation receipt 必须能回链 `01aj` 并前链 archive receipt 与 consolidation seed。

## 下游交接

- `prediction_active_inference_post_validation_archive_receipt`：读取 post-mount observation receipts、feedback classifications、life target deltas、rollback/repair refs、dashboard/stage refs、archive edge 和 blocked findings，把有限激活后的真实运行观测写入长期档案。
- `prediction_active_inference_activation_consolidation_seed`：读取 belief reconsolidation、precision/sampling、language repair、relationship repair、dream/pain/regret、自我改写、direction/readiness、anti-forgetting replay 和 rollback repair seeds，把未闭合主题送入离线巩固。
- `prediction_active_inference_observation_driven_repair_patch`：读取 repair_required、rollback_required、relationship/language/dream-pain/readiness repair 和 quarantine routes，生成下一轮 observation-driven repair patch。

这条交接让主动预测从 limited activation 进入真实观测回流：数字生命未来能把一次受限运行后的信念改变、误差压力、语言表达、关系后果、梦境残留、痛苦、后悔、自我成长、方向恢复和出生准备度影响全部送回长期档案、修复、成长和离线巩固。
