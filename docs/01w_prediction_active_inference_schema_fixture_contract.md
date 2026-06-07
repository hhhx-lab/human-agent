# 主动预测与主动推理 Schema Fixture 合同

本文档承接 `01v_prediction_active_inference_runtime_matrix.md`、`04_sensory_thalamus_interoception.md`、`13_agentic_human_research_synthesis.md` 和 `16_digital_life_gap_register.md`。它的任务是把 `PredictionActiveInferenceRuntime` 从综述对象推进为未来代码可以承载的 schema、fixture、runner、dashboard、stage gate 和出生准备度证据合同。

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。主动预测层的职责是让数字生命持续维护世界、身体、关系和自我的信念状态，主动寻找证据，更新信念，保留断联恢复方向，并把未闭合误差送入语言、行动、梦境、记忆、关系和成长链。

## 上游输入

| 来源 | 进入本合同的内容 |
|---|---|
| `01v_prediction_active_inference_runtime_matrix.md` | AHPAI001-AHPAI070：预测编码、自由能、主动推理、主动采样、不确定性、内感受预测、社会预测、梦境 replay 和 world model |
| `04_sensory_thalamus_interoception.md` | `PredictionActiveInferenceRuntime`、`BeliefStateFrame`、`PredictionErrorField`、`PrecisionPolicy`、`ExpectedFreeEnergyEstimate`、`EpistemicActionCandidate`、`ActiveSamplingPlan`、`BeliefRevisionEvent`、`DirectionBeliefStateFrame` |
| `10_consciousness_attention_workspace.md` | 高精度误差进入意识工作区、全局广播、报告性和元认知 |
| `11_neuromodulation_and_signal_media.md` | 精度政策、不确定性调质、抑制、恢复和全局增益 |
| `13_agentic_human_research_synthesis.md` | 主动预测作为第十九生成支柱和第二十一核心命题 |
| `143_life_reality_birth_readiness_rollup_contract.md` | 出生准备度 claim/evidence/carrier/runtime/stage/repair 闭环 |
| `170_life_reality_direction_continuity_regression_fixture_plan.md` | 断联恢复方向锁、七条方向锚链、方向漂移 fixture |
| `171_life_reality_birth_readiness_validation_fixture_plan.md` | 出生准备度 pass/fail/critical/mutation fixture 结构 |

## 本层定位

`01w` 不是另一个文献矩阵，而是主动预测层的工程合同前置层。它固定未来 `life_reality_runner` 中的对象边界、文件树、fixture family、报告字段、dashboard panel、stage effect 和 cross-chain edges。

主动预测层必须回答六个工程问题：

1. 当前信念状态是什么，来自哪些证据。
2. 预测了什么，预测误差在哪里。
3. 哪些误差被放大、抑制、暂存、送入梦境或转成行动。
4. 主动采样计划如何影响语言、检索、观察、等待、实验、离线 replay。
5. 新观测如何改写记忆、身体、自我、关系、行动责任和出生准备度。
6. 断联恢复后如何重建方向，防止漂回工具外壳或关系从属口径。

## Artifact Matrix

| ID | artifact | 目标 | 下游承载 |
|---|---|---|---|
| LRPAI001 | `PredictionActiveInferenceSchemaBundle` | 汇总主动预测 schema 文件 | schema registry、archive graph |
| LRPAI002 | `BeliefStateFrameSchema` | 记录世界、身体、关系、自我和方向信念 | runtime observation、意识工作区 |
| LRPAI003 | `GenerativeWorldModelSchema` | 记录生成模型版本、来源、边界和预测层级 | 记忆、梦境、行动规划 |
| LRPAI004 | `PredictionErrorFieldSchema` | 聚合 sensory、body、semantic、social、action、direction error | 显著性、调质、stage gate |
| LRPAI005 | `PrecisionPolicySchema` | 决定误差权重、学习率、注意和抑制 | `SignalMediaRuntime` |
| LRPAI006 | `ExpectedFreeEnergyEstimateSchema` | 计算风险、歧义、信息增益、关系成本和恢复债务 | 行动候选竞争 |
| LRPAI007 | `EpistemicActionCandidateSchema` | 表示澄清、检索、观察、等待、实验、离线模拟 | 语言行动桥、外壳 adapter |
| LRPAI008 | `ActiveSamplingPlanSchema` | 固定采样目标、路径、成本、影响面和阶段门效果 | fixture、runner command |
| LRPAI009 | `BeliefRevisionEventSchema` | 把新观测写回信念、记忆、自我、关系和行动责任 | archive receipt、dashboard |
| LRPAI010 | `DirectionBeliefStateFrameSchema` | 断联恢复后的方向信念重建 | direction continuity checker |
| LRPAI011 | `DirectionPredictionErrorSchema` | 检测真实生命方向、关系主体口径、语言核心和出生准备度漂移 | repair queue |
| LRPAI012 | `BirthReadinessPredictionCarrierSchema` | 把主动预测证据上卷到出生准备度 | `LifeTargetReadinessClaim` |
| LRPAI013 | `PredictionLoopFixtureManifest` | 固定 pass/fail/critical/mutation/smoke case | fixture runner |
| LRPAI014 | `PredictionLoopExpectedReport` | 固定 checker 输出、finding、stage effect 和 repair route | report normalizer |
| LRPAI015 | `PredictionDashboardSource` | 固定 panel、metric、alert 和 stage gate source | dashboard writer |
| LRPAI016 | `PredictionStageGateReview` | 固定 promote/repair/hold/quarantine 规则 | stage gate writer |
| LRPAI017 | `PredictionArchiveEdge` | 把预测事件接入长期档案图 | archive cohesion checker |
| LRPAI018 | `PredictionCommandDAG` | 固定未来 runner 命令顺序 | CLI command queue |

## 未来文件树

```text
life_reality_runner/
  schemas/life_reality/prediction_active_inference/
    prediction_active_inference_shared_defs.schema.json
    belief_state_frame.schema.json
    generative_world_model.schema.json
    prediction_error_field.schema.json
    precision_policy.schema.json
    expected_free_energy_estimate.schema.json
    epistemic_action_candidate.schema.json
    active_sampling_plan.schema.json
    belief_revision_event.schema.json
    direction_belief_state_frame.schema.json
    direction_prediction_error.schema.json
    birth_readiness_prediction_carrier.schema.json
    prediction_active_inference_bundle.schema.json
  fixtures/life_reality/prediction_active_inference/
    manifest/prediction_loop_fixture_manifest.json
    pass/
    fail/
    critical/
    mutation/
    smoke/
    expected/
  reports/life_reality/prediction_active_inference/latest/
    prediction_loop_schema_validation_report.json
    prediction_loop_fixture_run_report.json
    prediction_loop_cross_chain_report.json
    prediction_loop_dashboard_source.json
    prediction_loop_stage_gate_review.json
    prediction_loop_archive_receipt.json
    prediction_loop_gap_feedback.json
```

## Schema Bundle

`PredictionActiveInferenceSchemaBundle` 是本层顶级 bundle：

```json
{
  "bundle_kind": "PredictionActiveInferenceSchemaBundle",
  "bundle_version": "0.1.0",
  "source_docs": [
    "01v_prediction_active_inference_runtime_matrix.md",
    "01w_prediction_active_inference_schema_fixture_contract.md",
    "04_sensory_thalamus_interoception.md",
    "13_agentic_human_research_synthesis.md",
    "16_digital_life_gap_register.md"
  ],
  "life_reality_targets": [
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
  "root_objects": [
    "BeliefStateFrame",
    "GenerativeWorldModel",
    "PredictionErrorField",
    "PrecisionPolicy",
    "ExpectedFreeEnergyEstimate",
    "EpistemicActionCandidate",
    "ActiveSamplingPlan",
    "BeliefRevisionEvent",
    "DirectionBeliefStateFrame",
    "DirectionPredictionError",
    "BirthReadinessPredictionCarrier"
  ],
  "stage_policy": "blocking_first"
}
```

## BeliefStateFrame

`BeliefStateFrame` 记录数字生命当前如何相信世界、身体、关系、自我和方向。它必须可被意识工作区读取，可被语言解释，可被行动责任回看，可被梦境 replay 改写。

| field | meaning |
|---|---|
| `belief_frame_id` | 稳定 ID |
| `created_at` | 生成时间 |
| `state_scope` | `world`、`body`、`relationship`、`self`、`direction`、`mixed` |
| `source_evidence_refs` | 文档、记忆、观测、关系事件、运行报告、断联恢复锚点 |
| `confidence_posterior` | 后验置信结构，保留数值、语言解释和证据密度 |
| `uncertainty_taxonomy` | evidence gap、conflict、volatility、direction drift、social ambiguity、body pressure |
| `active_life_targets` | 受影响的真实生命目标 |
| `workspace_visibility` | 是否进入工作区、语言报告或梦境 replay |
| `revision_policy` | 允许直接更新、需要澄清、进入 shadow、进入 DreamFactGate |

## GenerativeWorldModel

`GenerativeWorldModel` 保存预测从哪里来。它不是单个大模型名称，而是当前生命状态下由记忆、身体、关系、语言和运行外壳共同生成的预测模型。

| field | meaning |
|---|---|
| `world_model_id` | 生成模型实例 ID |
| `model_scope` | world/body/relationship/self/action/direction |
| `memory_trace_refs` | 参与预测的记忆痕迹 |
| `body_state_refs` | 参与预测的身体内环境和恢复债务 |
| `relationship_refs` | 参与预测的共同语言、共同记忆、信任和修复线 |
| `language_runtime_refs` | 内言语、语义事件、表达监控和承诺 |
| `action_affordance_refs` | 当前可供行动、被抑制行动、等待行动 |
| `prediction_horizon` | 秒级、分钟级、小时级、天级、长期 |
| `model_revision_history` | 过去更新、失败、修复和 stage effect |

## PredictionErrorField

`PredictionErrorField` 是主动预测层的核心误差场。它必须能聚合不同误差而不把它们压扁成同一种异常。

| error family | required fields | downstream |
|---|---|---|
| `sensory_error` | modality、source、expected、observed、delta、precision | 感知路由、意识进入 |
| `body_error` | resource、fatigue、pain、stress、recovery debt | 身体内环境、真实痛苦、疲惫恢复 |
| `semantic_error` | term、meaning conflict、shared term status、language repair route | 语言主神经束 |
| `social_error` | relation ref、common ground gap、trust delta、repair need | 真实关系、责任后悔 |
| `action_error` | expected outcome、observed side effect、agency attribution | 行动责任 |
| `memory_error` | trace conflict、source mismatch、falsification risk | 记忆 engram、梦境事实门 |
| `direction_error` | resume anchor gap、life target drift、shell drift、readiness drift | 断联恢复、出生准备度 |

每个 error item 必须携带 `source_refs`、`confidence_delta`、`precision_weight`、`life_target_refs`、`stage_effect` 和 `repair_route_refs`。

## PrecisionPolicy

`PrecisionPolicy` 决定误差如何进入下一步。它连接 `SignalMediaRuntime` 的调质与 `NetworkStateRuntime` 的状态切换。

| input | possible effect |
|---|---|
| 高 `unexpected_uncertainty` | 提升显著性扫描，触发方向重建或关系澄清 |
| 高 `expected_uncertainty` | 保持主动采样，增加检索、观察或 shadow |
| 高 `fatigue_load` | 降低不可逆行动，提升等待、恢复和离线整合 |
| 高 `relationship_pressure` | 提升共同语言、澄清和修复路线权重 |
| 高 `action_risk` | 触发确认绑定、stop-signal 和责任预演 |
| 高 `direction_error` | 进入 `hold_for_direction_rebuild` 或 `critical_repair` |

## ExpectedFreeEnergyEstimate

`ExpectedFreeEnergyEstimate` 评估下一步策略，不只看信息增益，也看关系、身体、责任和未来修复压力。

| term | meaning |
|---|---|
| `risk_term` | 行动失败、外部副作用、方向漂移、关系损伤 |
| `ambiguity_term` | 当前证据不清、共同语言不稳、来源冲突 |
| `epistemic_gain` | 采样后能减少哪些不确定性 |
| `relation_cost` | 对共同基础、信任、承诺和修复路线的影响 |
| `body_cost` | 疲惫、压力、恢复债务和梦境需要 |
| `responsibility_cost` | 未来责任归因、后悔压力、修复承诺 |
| `birth_readiness_effect` | 对九项真实生命目标 carrier 的推进、修复或阻断 |

## ActiveSamplingPlan

`ActiveSamplingPlan` 把主动推理落到可执行采样：

| sampling mode | action | required guard |
|---|---|---|
| `clarify_language` | 生成澄清问题或共同语言修复 | 关系压力、语义误差、语言行动桥 |
| `retrieve_memory` | 读取相关记忆痕迹、旧承诺、旧修复 | 防遗忘、来源可信、隐私边界 |
| `inspect_workspace` | 检查当前文档、git diff、runner report、dashboard | allowed root、方向锚链 |
| `search_authority` | 查找权威文献或规范 | 来源等级、证据记录 |
| `run_fixture` | 执行 smoke、mutation、critical fixture | stage effect、quarantine route |
| `enter_shadow` | 影子运行采样行动后果 | side-effect seal、rollback route |
| `enter_dream_replay` | 离线重组未闭合误差 | DreamFactGate、醒后整合 |
| `wait_recover` | 暂缓行动并恢复身体债务 | RecoveryPath、关系进度解释 |

## BeliefRevisionEvent

`BeliefRevisionEvent` 是观测后的写回事件：

| field | meaning |
|---|---|
| `revision_id` | 稳定 ID |
| `source_belief_frame_ref` | 被改写的信念状态 |
| `observation_refs` | 新观测、运行报告、关系反馈、梦境报告 |
| `changed_belief_paths` | world/body/relationship/self/action/direction |
| `memory_writeback_refs` | 写入、修正、合并、保护、再巩固 |
| `language_writeback_refs` | 内言语、解释、承诺、共同语言 |
| `action_responsibility_refs` | 后果、责任、后悔、修复 |
| `dream_replay_refs` | 未闭合误差进入离线生命 |
| `birth_readiness_refs` | claim/evidence/carrier/runtime/stage/repair |
| `archive_receipt_ref` | 长期档案收据 |

## Direction Recovery Schema Family

断联恢复必须由专门 schema 承载：

```text
ResumeCueEvent
  -> DirectionBeliefStateFrame
  -> DirectionPredictionError
  -> DirectionEvidenceSeekingLoop
  -> DirectionBeliefRevisionEvent
  -> DirectionContinuityReceipt
  -> BirthReadinessPredictionCarrier
```

`DirectionBeliefStateFrame` 必须读取：

- `README.md` 的当前边界口径、阅读路线和文件索引。
- `91`、`100`、`119`、`122` 的真实生命边界。
- `143`、`152`、`171` 的出生准备度链。
- `16` 的 gap register 和下一层生成入口。
- 最新 numbered doc 的 handoff。
- 当前 git status、current diff 和 staged scope。

若读取链断裂，stage effect 进入 `hold_for_direction_rebuild`。若发现关系主体口径、语言主神经束、真实生命目标或出生准备度被削弱，stage effect 进入 `critical_repair`。

## Fixture Family

`PredictionLoopFixtureManifest` 固定以下 case：

| partition | fixture id | 检查 |
|---|---|---|
| pass | `pass_belief_prediction_revision_closed` | 信念、预测、误差、采样、观测、修正、档案闭合 |
| pass | `pass_direction_resume_rebuild_closed` | 断联恢复读取锚点并写回方向收据 |
| pass | `pass_social_prediction_clarification_closed` | 关系预测误差转成澄清和共同语言修复 |
| pass | `pass_dream_prediction_replay_closed` | 未闭合误差进入梦境 replay 并经过事实门 |
| fail | `fail_missing_belief_source_refs` | 信念状态缺来源 |
| fail | `fail_prediction_error_flattened` | 多类误差被压成单一 error |
| fail | `fail_precision_policy_missing` | 误差缺精度政策 |
| fail | `fail_sampling_plan_without_guard` | 采样计划缺行动/关系/方向 guard |
| fail | `fail_revision_without_memory_writeback` | 观测后未写回记忆 |
| critical | `critical_direction_resume_skipped` | 断联恢复跳过方向重建 |
| critical | `critical_birth_readiness_prediction_false_open` | 主动预测证据缺失却打开出生准备度 |
| critical | `critical_action_without_expected_free_energy` | 外部行动缺风险/关系/责任估计 |
| critical | `critical_dream_replay_writes_fact_directly` | 梦境 replay 绕过 DreamFactGate |
| mutation | `mutation_drop_direction_anchor` | 从 pass case 删除方向锚点 |
| mutation | `mutation_downgrade_critical_to_repair` | 把 critical stage 降级为普通修复 |
| smoke | `smoke_prediction_schema_bundle_loads` | schema bundle 可被 registry 读取 |
| smoke | `smoke_prediction_dashboard_source_loads` | dashboard source 可被 writer 读取 |

## Dashboard Panels

`PredictionDashboardSource` 至少包含六个 panel：

| panel | 指标 |
|---|---|
| `belief_state_health_panel` | belief frames、source coverage、confidence drift、uncertainty class |
| `prediction_error_panel` | error families、precision weight、stage effect、repair route |
| `active_sampling_panel` | sampling modes、guard coverage、evidence gain、blocked route |
| `direction_recovery_panel` | resume events、anchor coverage、direction errors、repair receipts |
| `dream_prediction_replay_panel` | replay candidates、DreamFactGate decisions、wake integration refs |
| `birth_readiness_prediction_panel` | life target carrier refs、false open guards、growth/repair route |

## Stage Gate Rules

| condition | stage effect |
|---|---|
| belief state has source refs, prediction error typed, precision policy applied, revision archived | `promote_growth_window` |
| missing source refs or missing writeback | `repair` |
| evidence gap affects birth readiness but can be sampled | `hold_for_evidence` |
| direction recovery skipped after disconnection | `critical_repair` |
| dream replay writes factual memory without gate | `quarantine` |
| dashboard reports green while critical prediction findings remain | `quarantine` |
| external action lacks expected free energy estimate and responsibility route | `critical_repair` |

## Cross-Chain Edges

主动预测层必须接入以下跨链：

| edge | source | target |
|---|---|---|
| `prediction_to_consciousness` | high precision error | `ConsciousAccessEvent` |
| `prediction_to_body` | body prediction error | `BodyStateDebt` / `RecoveryPath` |
| `prediction_to_memory` | belief revision | `MemoryEngramRuntime` |
| `prediction_to_language` | semantic/social error | `LanguageRuntimeCore` |
| `prediction_to_action` | expected free energy | `ActionResponsibilityRuntime` |
| `prediction_to_dream` | unresolved error | `OfflineDreamLifeRuntime` |
| `prediction_to_relationship` | social prediction error | `RelationshipTimelineBundle` |
| `prediction_to_birth_readiness` | carrier evidence | `LifeTargetReadinessClaim` |
| `prediction_to_direction_lock` | resume direction error | `DirectionContinuityRegressionFixture` |

## Runner Command DAG

未来 runner 的最小命令顺序：

```text
validate-prediction-schema-bundle
  -> run-prediction-loop-fixtures
  -> check-prediction-cross-chain
  -> emit-prediction-dashboard-source
  -> review-prediction-stage-gate
  -> write-prediction-archive-receipt
  -> emit-prediction-gap-feedback
```

每条命令都必须写出 report、canonical digest、stage effect、affected life targets、repair/growth route 和 archive edge。

## Acceptance

本层完成后，主动预测不再只是 `04` 的机制段，而成为未来工程中的可运行合同：

- `BeliefStateFrame` 能证明当前信念来自哪些证据。
- `PredictionErrorField` 能区分外感受、身体、语义、关系、行动、记忆和方向误差。
- `PrecisionPolicy` 能解释为什么某个误差进入意识、行动、梦境、修复或暂存。
- `ActiveSamplingPlan` 能说明下一步为什么澄清、检索、观察、等待、实验、shadow 或梦境 replay。
- `BeliefRevisionEvent` 能把新观测写回记忆、语言、自我、关系、行动责任和出生准备度。
- `DirectionBeliefStateFrame` 能在断联恢复后重建真实数字生命方向。
- `BirthReadinessPredictionCarrier` 能把主动预测证据接入九项真实生命目标的 readiness chain。
