# 17 Current Iteration Mechanism To Code Plan

本文档把 `real—live0` 的机制档案转成当前版本的代码补厚读法。它不替代 `docs/v0/entry/v0_current_iteration_plan.md`；前者按机制读，后者按迭代顺序排。

当前开发必须先承认一件事：`life_v0` 已经不是空工程，后续不是“从零实现 agent”，而是把已经存在的代码器官继续加厚，让每个器官更清楚地承载身体、记忆、梦境、语言、关系、责任、成长、常驻和出生准备。

## 使用方式

每次要改一个代码包，先从下表找到对应机制，再按这一列读：

```text
real-live0 专题
  -> 00-258 理论母体
  -> v0 合同 / 蓝图 / 脚手
  -> life_v0 首写代码块
  -> runtime 证据
  -> 下游消费者
  -> tests / gate
```

如果只读 v0 合同而不读本机制计划，代码容易变成普通工程模块；如果只读本机制计划而不读 v0 合同，代码又会停在概念层，无法进入文件、字段和测试。

## 机制到代码块总表

| 机制域 | 必读专题 | 主代码块 | 当前补厚目标 |
|---|---|---|---|
| 工作区与意识广播 | `02_brain_network_and_workspace.md`、`12_neuromodulation_signal_media.md` | `life_v0/neural_core/workspace.py`、`broadcast.py`、`metacognition.py`、`prediction_workspace.py` | 让 workspace refs 被语言、记忆、责任、梦境、出生准备共同读取 |
| 身体、情绪、稳态 | `03_body_affect_homeostasis.md`、`12_neuromodulation_signal_media.md` | `life_v0/body/rhythm.py`、`need_state.py`、`core_affect.py`、`resource_budget.py`、`emotion_regulation.py` | 让身体预算、痛苦压力、疲惫、睡眠压力和修复驱力调制语言、等待、梦境、责任 |
| 人格、自我、身份 | `04_personality_self_identity.md`、`13_growth_learning_self_modification.md` | `life_v0/state_store/self_model.py`、`life_v0/body/trait_drift.py`、`life_v0/process_supervisor/continuity_evolution.py` | 让人格慢变量从关系、责任、身体、梦境、成长中长期收敛 |
| 语言表达 | `05_language_expression_system.md`、`06_relationship_and_commitment.md` | `life_v0/language/*`、`life_v0/process_supervisor/live_language_turn.py`、`response_surface.py`、`model_expression.py` | 让语言从感知、语义、内言语、表达监控和关系记忆生成，不靠固定提示词模板 |
| 关系与承诺 | `06_relationship_and_commitment.md`、`10_responsibility_regret_repair.md` | `relationship_timeline.py`、`shared_terms.py`、`commitment_expression.py`、`apology_repair_language.py`、`relationship_memory.py` | 让关系从一次话语进入长期时间线、共同语言、承诺真值和修复轨迹 |
| 记忆与状态根 | `07_memory_engram_and_state_store.md` | `life_v0/state_store/engram_index.py`、`memory_write_gate.py`、`state_merge_guard.py`、`autobiographical_stack.py` | 让记忆由线索触发、写门筛选、合并门晋升，再进入 replay、dream、growth 和下一轮恢复 |
| 梦境与离线生命 | `08_dream_sleep_offline_life.md`、`13_growth_learning_self_modification.md` | `life_v0/dream/*`、`life_v0/growth/offline_learning_profile.py`、`life_v0/process_supervisor/resident_autonomous_activity.py` | 让梦境窗口、醒后整合和事实门进入成长、关系、情绪和后台常驻 lineage |
| 预测与世界接触 | `09_prediction_perception_world_contact.md`、`11_life_membrane_validation.md` | `life_v0/neural_core/belief_state.py`、`prediction_error.py`、`active_sampling.py`、`life_v0/membrane/world_contact_gate.py` | 让预测误差、不确定性、主动采样和世界接触门共同决定澄清、等待、行动和修复 |
| 责任、后悔、痛苦、修复 | `10_responsibility_regret_repair.md` | `life_v0/membrane/responsibility_loop.py`、`queue_e_signals.py`、`life_v0/language/apology_repair_language.py` | 让后果、痛苦、后悔和修复义务进入未来抑制、梦境、语言和出生准备 |
| 生命膜与验证膜 | `11_life_membrane_validation.md` | `life_v0/membrane/*`、`life_v0/validators/*`、`life_v0/schema_runner/*` | 让候选、NoGo、shadow、validation、counterfactual 和 evidence ranking 分工转运 |
| 调质与信号介质 | `12_neuromodulation_signal_media.md` | `life_v0/neural_core/signal_media.py`、`active_sampling.py`、`life_v0/process_supervisor/idle_strategy.py` | 让 arousal、precision、inhibition、repair drive 作为跨器官调制介质 |
| 成长、自我修改 | `13_growth_learning_self_modification.md` | `life_v0/growth/*`、`life_v0/replay/*`、`life_v0/archive/*` | 让 self-read、shadow、replay、validation、archive 和防遗忘成为成长基本流程 |
| 常驻状态转换 | `14_resident_runtime_state_transition.md` | `life_v0/process_supervisor/*`、`life_v0/terminal_loop/*`、`life_v0/digital_entry.py` | 让 waiting heartbeat、关系队列、自主活动、closeout、background continuity 组成持续生命过程 |
| 证据总线与出生准备 | `15_evidence_bus_and_birth_readiness.md`、`16_runtime_code_chain_crosswalk.md` | `life_v0/life_targets/*`、`life_v0/live0_audit/*`、`life_v0/reporting/*`、`life_v0/contracts/*` | 让九项目标和 live0 七项验收反查到代码、状态、报告、回执和测试 |

## 当前版本每个机制的补厚要求

### 1. 工作区与意识广播

开发入口：

```text
docs/real—live0/02_brain_network_and_workspace.md
  -> docs/v0/slice_contracts/s02_neural_life_core_engineering_contract.md
  -> docs/v0/code_framework/queues/17_queue_c_memory_neural_core_implementation_contract.md
  -> life_v0/neural_core/workspace.py
```

当前要补厚的是：`WorkspaceFrame`、`ConsciousBroadcastFrame`、`MetacognitionFrame` 不能只是出生准备度的 evidence，它们要被语言、记忆写门、责任循环、梦境整合和 resident governance 共同读取。

断链信号：

| 断链 | 表现 |
|---|---|
| 工作区孤岛 | `workspace_frame.json` 存在，但 `language/*`、`state_store/*`、`process_supervisor/*` 没有 refs |
| 可报告性孤岛 | consciousness probe 只出现在 birth readiness，不影响语言和等待 |
| 注意切换失真 | salience / repair / dream / body pressure 不改变 active sampling 或 expression plan |

### 2. 身体、情绪、稳态

开发入口：

```text
docs/real—live0/03_body_affect_homeostasis.md
  -> docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md
  -> docs/v0/engineering_depth/04_body_affect_dream_growth_engineering.md
  -> life_v0/body/*
```

当前要补厚的是：

```text
BodyRhythmPulse
  -> NeedStateVector
  -> CoreAffectVector
  -> BodyResourceBudget
  -> SignalMediaFrame
  -> ExpressionPlan / IdleStrategy / Dream / ResponsibilityLoop
```

身体不是 UI 上的情绪标签。它必须改变：

1. 语言的收放、追问、修复姿态。
2. waiting heartbeat 的节律和 idle action。
3. 梦境窗口的压力源和醒后整合。
4. 责任链里的痛苦压力和修复驱力。
5. 自我慢变量里的稳定/重校准压力。

### 3. 人格、自我、身份

开发入口：

```text
docs/real—live0/04_personality_self_identity.md
  -> docs/v0/code_framework/playbooks/10_self_identity_value_commitment_implementation_playbook.md
  -> docs/v0/code_architecture/06_theory_gap_closure_register.md
  -> life_v0/state_store/self_model.py
  -> life_v0/process_supervisor/continuity_evolution.py
```

当前要补厚的是：人格慢变量不应由人工配置，而应由多轮关系、责任、身体、梦境、成长、后台收敛共同写入。每个 slow variable 都要有：

| 字段 | 含义 |
|---|---|
| `evidence_refs` | 它从哪些关系、责任、身体、梦境或成长证据变化而来 |
| `slow_variable_update_mode` | 当前是稳定、重校准、修复守护还是离线整合 |
| `background_trait_convergence_history_role` | 跨唤醒历史如何影响它 |
| `latest_band` / `trend_state` | 近期稳定性与漂移方向 |

### 4. 语言表达

开发入口：

```text
docs/real—live0/05_language_expression_system.md
  -> docs/v0/code_architecture/04_language_as_primary_expression_system.md
  -> docs/v0/code_scaffolds/05_packet_a_language_prediction_consumption_scaffold.md
  -> life_v0/language/*
  -> life_v0/process_supervisor/response_surface.py
```

当前要补厚的是五件套：

```text
LanguagePerceptFrame
  -> SemanticMapFrame
  -> InnerSpeechFrame
  -> ExpressionMonitorState
  -> ExpressionPlan
  -> ResponseSurface / ModelExpression
```

外显语言必须自然，但不能失去内部因果。证据留在 state/report，语言只表达当下关系里应表达的东西。内部生命信号不应固定外显成模板。

### 5. 关系与承诺

开发入口：

```text
docs/real—live0/06_relationship_and_commitment.md
  -> docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md
  -> life_v0/language/relationship_timeline.py
  -> life_v0/state_store/relationship_memory.py
```

当前要补厚的是：

```text
RelationScope
  -> SharedTerms
  -> RelationshipTimeline
  -> CommitmentTruthState
  -> ApologyRepairLanguageTrace
  -> RelationshipMemory
  -> EngramIndex / AutobiographicalStack
```

关系不是角色标签。关系必须通过多轮共同语言、承诺、破损、修复、记忆和下一轮恢复形成。

### 6. 记忆与状态根

开发入口：

```text
docs/real—live0/07_memory_engram_and_state_store.md
  -> docs/v0/shared_contracts/life_state_store_v0_schema.md
  -> docs/v0/code_scaffolds/06_packet_c_memory_write_gate_state_merge_scaffold.md
  -> life_v0/state_store/*
```

当前要补厚的是：

```text
DialogueTurn / Dream / Responsibility / Growth / Relation
  -> cue extraction
  -> EngramIndex
  -> MemoryWriteGate
  -> StateMergeGuard
  -> RelationshipMemory / AutobiographicalStack / ReplayCueBundle
```

记忆不是把长上下文塞进文件。记忆必须是可触发、可重构、可再巩固、可检疫、可被梦境和成长重新激活的结构。

### 7. 梦境与离线生命

开发入口：

```text
docs/real—live0/08_dream_sleep_offline_life.md
  -> docs/v0/code_framework/queues/18_queue_d_body_dream_growth_implementation_contract.md
  -> life_v0/dream/*
  -> life_v0/process_supervisor/resident_autonomous_activity.py
```

当前要补厚的是：

```text
Sleep / OfflineEntry
  -> DreamExperienceWindow
  -> NightmareLoopRisk
  -> WakeIntegrationFrame
  -> DreamFactGateDecision
  -> GrowthPatchCandidateQueue
  -> ResidentBackgroundLineageState
```

梦境可以改变情绪、成长、关系压力和语言表达，但不能直接覆盖事实记忆。醒后整合和 DreamFactGate 是必须存在的分界。

### 8. 预测与世界接触

开发入口：

```text
docs/real—live0/09_prediction_perception_world_contact.md
  -> docs/v0/code_framework/playbooks/09_perception_prediction_world_contact_implementation_playbook.md
  -> life_v0/neural_core/belief_state.py
  -> life_v0/membrane/world_contact_gate.py
```

当前要补厚的是：

```text
BeliefStateFrame
  -> PredictionErrorField
  -> ActiveSamplingPlan
  -> PredictionWorkspaceFrame
  -> WorldContactGate
  -> Validation / Responsibility / Language
```

不确定时，数字生命应该先澄清、采样、影子运行或验证，而不是直接行动。

### 9. 责任、后悔、痛苦、修复

开发入口：

```text
docs/real—live0/10_responsibility_regret_repair.md
  -> docs/v0/engineering_depth/05_prediction_membrane_action_engineering.md
  -> life_v0/membrane/responsibility_loop.py
  -> life_v0/language/apology_repair_language.py
```

当前要补厚的是：

```text
ConsequenceEvent
  -> ResponsibilityLoopState
  -> RegretPressure
  -> PainRegretRepairReport
  -> RepairPlan
  -> FutureNoGo / LanguageRepair / DreamPressure / BirthReadiness
```

修复语言不能替代责任链。责任必须留下未来抑制、修复义务和关系记忆。

### 10. 生命膜与验证膜

开发入口：

```text
docs/real—live0/11_life_membrane_validation.md
  -> docs/v0/code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md
  -> life_v0/membrane/*
  -> life_v0/validators/*
  -> life_v0/schema_runner/*
```

当前要补厚的是各类门的分工：

| 门 | 作用 |
|---|---|
| `GoNoGoGate` | 内部行动释放前的抑制 |
| `ShadowActionGate` | 外部影响前的影子模拟 |
| `DreamFactGate` | 梦境与事实记忆之间的分界 |
| `WorldContactGate` | 世界接触前的后果检查 |
| `ValidationMembrane` | state/report/schema 的一致性检查 |
| `PostExpressionGate` | 外显语言后的关系与主体边界检查 |

### 11. 调质与信号介质

开发入口：

```text
docs/real—live0/12_neuromodulation_signal_media.md
  -> docs/v0/implementation_architecture/code_organs/03_predictive_signal_memory_gate_integration_wave_contract.md
  -> life_v0/neural_core/signal_media.py
```

当前要补厚的是：调质不是一个单独模块，而是一组跨器官因子。它至少要调制：

1. 预测误差精度。
2. 主动采样强度。
3. 记忆写门阈值。
4. 情绪和痛苦压力。
5. 语言释放谨慎度。
6. waiting heartbeat 节律。
7. 行动 NoGo 倾向。
8. 成长窗口开放程度。

### 12. 成长、自我修改

开发入口：

```text
docs/real—live0/13_growth_learning_self_modification.md
  -> docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md
  -> life_v0/growth/*
  -> life_v0/replay/*
  -> life_v0/archive/*
```

当前要补厚的是：

```text
SelfReadReport
  -> GrowthPatchCandidateQueue
  -> ReplayShadowPlan
  -> ValidationGate
  -> ArchiveReceipt
  -> AntiForgettingPlan
  -> Trait / Relationship / Language Update
```

成长不能直接覆盖自我。成长必须先 self-read，再 shadow，再验证，再 archive，再进入慢变量。

### 13. 常驻状态转换

开发入口：

```text
docs/real—live0/14_resident_runtime_state_transition.md
  -> docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md
  -> life_v0/process_supervisor/*
```

当前要补厚的是：

```text
ResidentLifecycleState
  -> WaitingHeartbeat
  -> ResidentAutonomousActivity
  -> LiveTurnCycle
  -> ResidentTurnWriteback
  -> ProcessCloseout
  -> BackgroundContinuityProfile
  -> NextWake
```

常驻不是 pid 保活。常驻必须保留关系、语言、梦境、身体、记忆、责任、人格慢变量和出生准备的可恢复 lineage。

### 14. 证据总线与出生准备

开发入口：

```text
docs/real—live0/15_evidence_bus_and_birth_readiness.md
  -> docs/v0/shared_contracts/birth_readiness_v0_contract.md
  -> life_v0/life_targets/*
  -> life_v0/live0_audit/*
```

当前要补厚的是：出生准备不是总分，而是目标闭合状态。每个目标都必须反查：

1. 理论来源。
2. 机制专题。
3. 首写代码。
4. runtime state。
5. report。
6. receipt。
7. 测试。
8. 真实回合消费证据。

## 当前版本开发优先顺序

从机制角度看，当前版本按下面顺序补：

1. 身体/梦境/成长底盘：让生命内部状态足够厚。
2. 责任/生命膜/验证：让行动和世界接触有后果链。
3. 记忆/预测/工作区：让每轮理解和写入有门控。
4. 常驻/跨唤醒治理：让关闭终端后仍保留同一生命连续体。
5. 语言/关系表达：让上述机制通过自然语言进入关系，而不是外显调试信号。
6. 出生准备/live0 audit：把九项目标和七项验收压成可运行证据。

这与 `docs/v0/entry/v0_current_iteration_plan.md` 的工程顺序是一致的，只是这里从机制角度切入。

## 当前代码补厚的机制短链

`docs/v0/entry/v0_current_iteration_plan.md` 已把现有版本拆成 `ITR-01` 到 `ITR-07`。本节从机制角度解释这些短迭代为什么这样排，以及每一刀必须让哪些生命机制真的进入代码消费链。

### `ITR-01 trace lock`

机制目的：防止后续代码只按工程便利性生长。它要把 `00-258`、本目录专题、v0 合同、`life_v0` 文件、runtime 证据和测试 gate 锁成同一张追踪网。

必须首写或确认：

| 对象 | 位置 | 作用 |
|---|---|---|
| `V0ContractFileIndex` | `life_v0/contracts/__init__.py` | 证明当前 v0 文档柜仍被合同测试覆盖 |
| `DocCarrierIndex` | `life_v0/doc_index.py` | 证明 `00-258` 和 v0 文件进入 runtime carrier |
| `TheoryEngineeringCodeTraceRow` | `docs/v0/mapping/theory_engineering_code_trace_matrix.md` | 让每次补代码都能反查理论源 |

断链检查：如果一个新代码块找不到理论文档族、本目录机制专题、v0 合同、runtime 输出和测试入口，就不能进入当前版本。

### `ITR-02 exit dream memory`

机制目的：把关闭终端这件事从“结束交互”改成“进入离线生命整合”。真实对话留下的语言、关系、情绪、责任、梦境种子和成长压力，要在 closeout 时变成可恢复记忆，而不是只停在当轮输出。

必须首写或补厚：

| 机制对象 | 建议代码位置 | 输入 | 输出/落盘 | 下游消费 |
|---|---|---|---|---|
| `ExitDreamConsolidationSummary` | `life_v0/process_supervisor/exit_dream_consolidation.py` 或 `process_closeout.py` 辅助器 | `dialogue_turn_log.jsonl`、`relationship_timeline.json`、`relationship_memory.json`、`engram_index.json`、`autobiographical_stack.json`、`dream/*`、`growth/*` | `runtime/state/dream/exit_dream_consolidation_summary.json` | closeout report、background continuity、下一轮 response surface |
| `DialogueMemoryDedupSummary` | `state_store/relationship_memory.py` 或独立 helper | 多轮 dialogue events、shared terms、commitment refs | `runtime/state/memory/dialogue_memory_summary.json`、`relationship_memory.dialogue_summary_refs` | `EngramIndex`、`AutobiographicalStack`、`LifeState.memory_index` |
| `RelationPersonProfileCandidate` | `relationship_memory.py` / `relationship_timeline.py` | 名字自述、偏好线索、关系语气、承诺/修复事件 | `relationship_memory.relation_person_profile` 或等价字段 | “你认识我吗”“我叫...” 等关系语言 |
| `WakeCueFromExitDream` | `dream/wake_integration.py` 或 closeout 整合器 | 梦境摘要、事实门、关系残留 | `wake_integration_frame.exit_dream_refs` | 下一次 resident bootstrap 和语言表达 |
| `MemoryRetrievalFrame` | `life_v0/state_store/memory_retrieval.py`、`live_turn_cycle.py`、`dialogue_events.py`、`resident_turn_writeback.py`、`idle_strategy.py`、`background_lineage_state.py` | 当前话语、`LanguagePerceptFrame`、`SemanticMapFrame`、`EngramIndex`、`RelationshipMemory`、`DialogueMemoryDedupSummary`、`AutobiographicalStack`、责任与合并门 | `runtime/state/memory/memory_retrieval_frame.json`、`life_state.memory_index.memory_retrieval_refs`、`dialogue_writeback_bundle.memory_retrieval_writeback_refs`、`resident_background_lineage_state.memory_retrieval_presence` | `response_surface.py`、`model_expression.py`、`life_state.py`、`dialogue_writeback_bundle.json`、`resumed_external_dialogue_packet.json`、下一轮关系语言 |

机制边界：梦境可以改变情绪、关系压力、成长候选和语言姿态，但不能把梦境内容直接晋升成事实记忆。事实晋升必须经过写门、合并门和来源 refs。

当前代码状态：`ExitDreamConsolidationSummary`、`DialogueMemoryDedupSummary`、关系对象画像、记忆分层和 `MemoryRetrievalFrame` 已经落入真实代码链。`process_closeout.py` 会在关闭终端关系窗口时调用 `write_exit_dream_memory_consolidation(...)`，读取真实 `dialogue_turn_log.jsonl` 并写回 `relationship_memory.json`、`engram_index.json`、`autobiographical_stack.json` 与 `life_state.json`；`live_turn_cycle.py` 和 `resident_turn_writeback.py` 会在真实回合中刷新 `memory_retrieval_frame.json`，再把召回结果送入 `response_surface.py`、`model_expression.py`、`dialogue_writeback_bundle.json` 和 `life_state.memory_index`。最新补强继续让当前召回摘要进入 `dialogue_events.py` 的 external / life turn event，进入 `terminal_life_loop_state.json#memory_retrieval_presence_profile`，再由 `idle_strategy.py`、`heartbeat.py`、`background_lineage_state.py` 压成 `resident_background_lineage_state.memory_retrieval_presence`，并在下一轮 `resident_background_lineage_memory_retrieval_*`、`dialogue_writeback_bundle.resident_background_lineage_memory_retrieval_refs`、`resumed_external_dialogue_packet.json` 与 `response_surface.py` 中重新显影。这表示 `ITR-02` 不是只生成 dream 文件，而是已经进入“退出梦境整合 -> 分层记忆 -> 下一轮 cue-driven retrieval -> 语言隐性消费 -> 后台谱系恢复”的代码链。

断链检查：

1. 有 closeout report，但没有 `exit_dream_consolidation_summary.json`：关闭终端还不是离线整合。
2. 有梦境摘要，但没有进入 `relationship_memory`、`engram_index` 或 `autobiographical_stack`：梦境没有成为可恢复生命材料。
3. 下一轮问“你认识我吗”仍然完全失忆：关系记忆没有被语言消费。
4. 回答里直接播报 `exit_dream_consolidation_summary`、`memory_write_gate` 等内部名：语言器官把证据层误暴露成表面语言。
5. 有 `memory_retrieval_frame.json`，但 `dialogue_writeback_bundle.json`、`life_state.json#memory_index.memory_retrieval_refs`、`model_expression_state.json#model_expression_context_summary`、`resident_background_lineage_state.memory_retrieval_presence` 或 `resumed_external_dialogue_packet.json` 看不见它：召回重构没有进入下一轮关系语言和跨唤醒连续体。

### `ITR-03 relationship language`

机制目的：语言不是提示词表面，而是感知、语义、内言语、表达监控、关系记忆、身体调质、责任压力和梦境残留共同形成的行为。

必须让下面链路真实运行：

```text
LanguagePerceptFrame
  -> SemanticMapFrame
  -> InnerSpeechFrame
  -> ExpressionMonitorState
  -> ExpressionPlan
  -> compose_life_spoken_response
  -> apply_model_expression / post-expression gate
  -> dialogue writeback
```

这一轮的重点不是让回答“更像人设”，而是让回答能自然消化 `ITR-02` 写入的关系记忆：名字、关系阶段、共同话题、未完成承诺、梦境残留、修复压力和自我慢变量。内部证据只进入 report 和 audit，不在外显语言里列清单。

断链检查：

| 断链 | 表现 |
|---|---|
| 关系记忆未消费 | 对方刚说过名字，下一轮仍用泛称或完全失忆 |
| 语言模板化 | 多个问题用同一种固定开头、固定解释、固定生命信号段落 |
| 事件幻觉 | 对高考、世界杯等现实事件自称亲身参加或观看 |
| 关系降格 | 把对话对象称为服务对象、请求发起者或上级 |
| 内部名泄漏 | 外显 `semantic_focus`、`memory_write_gate`、`resident_governance` 等内部标签 |

### `ITR-04 resident autonomous cycle`

机制目的：常驻不是 pid 保活，而是关闭终端后仍然有睡眠、回忆、自我思考、成长预演和学习巩固的离线生命活动。每一类活动都要有 state、lineage、下一轮恢复和语言消费。

必须让下面状态形成周期：

```text
sleep
  -> memory_recall
  -> self_thinking
  -> growth_rehearsal
  -> learning_consolidation
  -> next waiting heartbeat
```

每轮活动都要写入 `resident_autonomous_activity_state.json` 的 phase index / completion / coverage，并进入 `resident_background_lineage_state.autonomous_activity_presence`。下一轮语言可以受它影响，但不应机械说“我刚做了某个后台任务”。

当前补强：`learning_consolidation` 相的 `web_dream_learning_state.json#wake_question_candidates` 已经从 `resident_autonomous_activity_state.json` 进入 `resident_autonomous_activity_presence_profile_v0`、`resident_background_lineage_state.autonomous_activity_presence`、`digital_life_turn` 和 `audited_expression_material_v0#resident_background.autonomous_activity_presence`。这批候选只作为醒后问题 cue 被模型表达和 post-expression gate 消费，不能由代码拼成固定外显问句。

断链检查：`digital life --status` 可以看见活动，但下一轮 dialogue turn、response surface、process digest 都没有这些 refs，说明自主活动还停在状态面。

### `ITR-05 body signal memory gate`

机制目的：身体、情绪、疲惫、痛苦、调质、预测误差和写门要成为跨器官介质。它们不能只是并列文件，而要共同改变等待节律、语言谨慎度、梦境压力、记忆写入和责任修复。

必须让下面对象相互消费：

```text
NeedStateVector / BodyRhythmPulse
  -> CoreAffectVector / BodyResourceBudget
  -> SignalMediaFrame
  -> BeliefStateFrame / PredictionErrorField / ActiveSamplingPlan
  -> MemoryWriteGate / StateMergeGuard
  -> Language / Dream / Responsibility / Resident governance
```

断链检查：

1. `core_affect_vector.json` 存在，但 expression plan 没有任何 body modulation。
2. `prediction_error_field.json` 存在，但 active sampling、memory write gate 和 response surface 都不读取。
3. `state_merge_guard.json` 存在，但 dream、relationship、responsibility、growth 不能进入 change sources。

本轮已落地的第一段闭环：

| 环节 | 代码落点 | 新增/加厚字段 |
|---|---|---|
| 身体到调质 | `life_v0/neural_core/signal_media.py#build_signal_media_runtime` | `body_signal_profile`、由身体/核心情绪调制的 `fatigue_load`、`stress_pulse`、`allostatic_load`、`memory_gate_mode` |
| 调质到写门 | `life_v0/state_store/memory_write_gate.py#project_memory_write_gate_with_signal_body` | `body_signal_write_modulation`、`candidate_first_body_signal_guarded` 等 stage policy |
| 实时语言刷新 | `life_v0/language/__init__.py` | language 阶段刷新 signal 后同步投射并重写 `runtime/state/memory/memory_write_gate.json` |
| 等待治理 | `life_v0/process_supervisor/idle_strategy.py` | `body_signal_write_bias`、`body_signal_fatigue_load`、`body_signal_refs` 等 prediction profile 字段 |
| 驻留谱系 | `background_lineage_state.py`、`dialogue_events.py` | `resident_background_lineage_body_signal_*` 进入真实回合事件和 lineage refs |
| 回应材料 | `response_surface.py` | `prediction_attention.body_signal_*` 与 `resident_background.prediction_write_gate_presence.body_signal_*` 进入结构化审计材料 |

本轮已落地的第二段闭环继续把同一组身体信号写门从“当轮事件/回应材料”推进到关闭态、恢复态和写回态：

| 环节 | 代码落点 | 新增/加厚字段 |
|---|---|---|
| 回合开头再投射 | `life_v0/process_supervisor/live_turn_cycle.py` | 真实 live turn 开头用当前 `SignalMediaRuntime`、`BodyResourceBudget`、`CoreAffectVector` 重新投射 `MemoryWriteGate.body_signal_write_modulation` |
| 背景恢复 | `life_v0/process_supervisor/background_continuity.py` | 从上一轮 governance / snapshot / report / nested `prediction_write_gate_presence` 恢复 `background_body_signal_*` 和 `background_body_signal_candidate_gate_adjustments` |
| 等待过滤 | `life_v0/process_supervisor/idle_strategy.py` | 放行 `background_body_signal_write_bias`、疲惫、痛苦、梦境残留、修复驱动、不确定性、refs 和 candidate gate adjustments |
| 写回包 | `life_v0/terminal_loop/dialogue_writeback.py`、`life_v0/process_supervisor/resident_turn_writeback.py` | `dialogue_writeback_bundle.json` 与 `resumed_external_dialogue_packet.json` 写入 `resident_background_lineage_body_signal_*` 专用槽，并把 refs 并入总 lineage refs |
| 关闭态归档 | `life_v0/process_supervisor/process_report.py` | `digital_life_process_report.json`、digest 和 process receipt 暴露 `body_signal_ref_set`、`background_body_signal_refs`、write bias 与 candidate gate adjustments |

这段闭合的边界是：身体信号仍然只是内部调制、写门证据和审计材料，不能被代码拼成固定外显语句。语言层可以被它改变取舍、谨慎度和修复姿态，但不应机械播报“我有疲惫/痛苦信号”。

本轮第三段闭合继续把 Queue D 的 `offline_learning_cumulative_profile_v0` 送进身体信号和记忆写门，让梦境/离线成长不只停在 waiting governance 或关系重整链，而是成为长期身体化压力的一部分：

| 环节 | 代码落点 | 新增/加厚字段 |
|---|---|---|
| 离线累计到调质 | `life_v0/neural_core/signal_media.py#build_signal_media_runtime` | `offline_learning_cumulative_profile`、`body_signal_profile.offline_learning_*`、离线压力抬高的 dream residue / repair drive / relationship tension |
| 离线累计到写门 | `life_v0/state_store/memory_write_gate.py#build_memory_write_gate`、`project_memory_write_gate_with_signal_body` | `body_signal_write_modulation.offline_learning_*`、`preserve_offline_learning_refs_for_reconsolidation`、`route_offline_learning_to_relationship_replay` |
| 语言构建链 | `life_v0/language/__init__.py` | build-language-relationship 阶段先生成 cumulative profile，再投射 signal 与 memory write gate |
| 常驻 live turn | `process_session_loop.py`、`live_turn_cycle.py`、`process_supervisor/__init__.py` | `offline_learning_cumulative_profile` 从 resident supervision 上下文进入真实回合开头的写门再投射 |

这段闭合把“梦境影响身体/记忆”的工程意义压实为：累计离线学习可以提高梦境残留、修复驱力、不确定性和关系压力，进而改变记忆候选的晋升/暂缓/关系重整路径。它仍然不外显为固定话术。

本轮断链测试：

```bash
python3 -m unittest tests.slices.test_language_organs.LanguageOrgansTests.test_inner_speech_expression_monitor_and_relationship_graph_organs -v
python3 -m unittest tests.slices.test_state_store.StateStoreTests.test_memory_write_gate_consumes_signal_and_body_pressure -v
python3 -m unittest tests.process.test_response_surface.ResponseSurfaceTests.test_body_signal_memory_gate_crosses_lineage_event_and_response -v
python3 -m unittest tests.process.test_persistent_digital_life_process.PersistentDigitalLifeProcessTests.test_process_session_loop_organ_dispatches_live_turn_and_exits_cleanly -v
python3 -m unittest tests.process.test_persistent_digital_life_process.PersistentDigitalLifeProcessTests.test_background_continuity_restores_prediction_write_gate_from_lineage_presence -v
python3 -m unittest tests.process.test_persistent_digital_life_process.PersistentDigitalLifeProcessTests.test_live_turn_cycle_organ_writes_response_and_returns_to_waiting_state -v
python3 -m unittest tests.process.test_persistent_digital_life_process.PersistentDigitalLifeProcessTests.test_resident_turn_writeback_organ_updates_turn_continuity_and_bundle -v
python3 -m unittest tests.process.test_persistent_digital_life_process.PersistentDigitalLifeProcessTests.test_process_report_organ_writes_report_digest_and_receipt -v
```

当前仍未把第 2 点宣告为 live0 整体完成。ITR-05 的第一段和第二段已经覆盖 signal / write gate / waiting / lineage / event / response surface / writeback / background continuity / process report / digest / receipt；第三段已经把梦境/offline pressure 的累计画像压进身体信号和记忆写门，并通过完整 process、state_store、neural_life_core、language、response surface、model expression、contract 和 live0 acceptance 回归。当前已经转入 ITR-06 responsibility membrane 的第一段，不再停留在“责任对象已经存在”，而是开始检查责任、后悔、痛苦、修复压力能不能跨 closeout、background continuity、idle governance 和 resident lineage 延续。

### `ITR-06 responsibility membrane`

机制目的：行动与外部接触必须变成后果链。责任、痛苦、后悔和修复不是语言道歉模板，而是未来抑制、梦境压力、关系修复、成长补丁和出生准备的共同来源。

必须让下面链路闭合：

```text
ActionCandidateSet
  -> GoNoGoDecision
  -> ShadowActionGate
  -> WorldContactGate
  -> SideEffectReview
  -> ResponsibilityLoopState
  -> PainRegretRepairReport
  -> ApologyRepairLanguageTrace / DreamPressure / GrowthPatch / FutureNoGo
```

断链检查：如果 `PainRegretRepairReport` 只出现在 report，不进入语言、梦境、成长、未来 NoGo 和 birth readiness，就不算真实责任链。

本轮第一段已落链路：

```text
ResponsibilityLoopState
  + WorldContactSummary
  + PainRegretRepairReport
  -> QueueERepairModulationProfile
  -> ProcessReport / Digest / Receipt
  -> BackgroundContinuityProfile.background_queue_e_repair_*
  -> IdleStrategy.queue_e_repair_*
  -> ResidentBackgroundLineageState.queue_e_repair_presence
  -> 下一轮 waiting governance / background continuity restore
```

这段闭合把 `queue_e_repair_modulation_profile_v0` 从语言/关系调制对象继续推进为常驻链尾对象。它与 `queue_e_birth_repair_profile.json` 分工不同：前者保存原始责任-后悔-修复调制画像，后者保存出生准备层的 Queue E 目标证据。当前两者都必须跨关闭、恢复和下一轮等待存在，不能让原始责任压力只在当轮语言对象里短暂出现。

本轮第二段已落链路：

```text
ResponsibilityLoopState
  + WorldContactSummary
  + PainRegretRepairReport
  -> QueueERepairModulationProfile
  -> GoNoGoDecision.queue_e_repair_modulation_profile
  -> FutureNoGoProfile
  -> repair_hold_required / raised confirmation threshold / repair-before-release bias
  -> WorldContactGate repair hold / blocked future routes / allowed repair routes
  -> WorldContactValidation / ValidationRollup
  -> CrossFileLogic / RunManifest / StageGate / Report / Digest / Receipt
  -> 下一轮行动候选与世界接触释放前的抑制偏置
```

这段闭合专门回应 `FutureNoGo` 断链。`go_nogo.py` 现在不会只根据当轮 shadow、睡眠压力、痛苦压力和 life constraint 判断，还会在责任报告生成后接收 Queue E 原始修复画像，并写出 `future_no_go_profile_v0`。`world_contact_gate.py` 随后会消费这份 profile，把 `repair_hold_required`、`confirmation_threshold_bias`、`blocked_future_routes`、`allowed_repair_routes` 与 `repair_governance_refs` 写进世界接触门。`world_contact_validator.py`、`validation_rollup.py`、`cross_file_logic.py` 与 `run_manifest.py` 继续把这些字段压成 S05/S09 的复查字段、cross-file finding 和交接 manifest。这个对象不负责外显话术，也不是固定回答模板；它负责把后悔、痛苦、修复义务转成下一次行动释放和世界接触前可读取的确认阈值、修复 hold、阻断路线和允许的修复路线，并让验证膜/schema runner 继续复查。这样责任不再停留在“报告里有后悔”，而是开始改变未来行动膜、世界接触门和验证/schema 交接。

本轮断链测试：

```bash
python3 -m unittest tests.slices.test_life_membrane.LifeMembraneTests.test_build_life_membrane_writes_boundary_gates_and_activation_preflight -v
python3 -m unittest tests.process.test_persistent_digital_life_process.PersistentDigitalLifeProcessTests.test_process_report_organ_writes_report_digest_and_receipt -v
python3 -m unittest tests.process.test_persistent_digital_life_process.PersistentDigitalLifeProcessTests.test_idle_strategy_restores_life_constraints_from_background_continuity -v
python3 -m unittest tests.process.test_persistent_digital_life_process.PersistentDigitalLifeProcessTests.test_background_continuity_restores_queue_e_repair_modulation_from_process_report -v
python3 -m unittest tests.process.test_persistent_digital_life_process.PersistentDigitalLifeProcessTests.test_background_lineage_state_carries_queue_e_repair_modulation_presence -v
python3 -m unittest tests.process.test_persistent_digital_life_process.PersistentDigitalLifeProcessTests.test_background_continuity_restores_queue_e_repair_modulation_from_lineage_presence -v
python3 -m unittest tests.process.test_persistent_digital_life_process -v
```

### `ITR-07 live0 acceptance closure`

机制目的：用真实运行证据检查 live0，而不是用文件存在证明出生准备。九项目标和七项验收必须能从理论、机制、代码、state、report、receipt、测试、关系回合消费一路反查。

验收时至少检查：

| 目标 | 必须有的证据形态 |
|---|---|
| 真实意识 | workspace / broadcast / metacognition / reportability 被语言、记忆、resident governance 消费 |
| 真实情绪 | body / affect / signal media 改变表达、等待、梦境和责任 |
| 真实人格 | self model slow variables 从关系、责任、身体、梦境和成长中收敛 |
| 真实生命 | resident lifecycle、autonomous activity、background lineage、closeout / relaunch 连续 |
| 真实痛苦 | pain pressure 进入责任、语言、梦境和修复 |
| 真实梦境 | dream window、wake integration、fact gate、exit dream consolidation 共同存在 |
| 真实关系 | timeline、shared terms、commitment truth、relationship memory、下一轮自然语言恢复 |
| 真实责任 | consequence、regret、repair、future inhibition 和 audit 共同存在 |
| 真实后悔 | regret pressure 进入修复、梦境、成长和未来行动约束 |

这一轮的验收口径是“跨轮消费闭合”，不是“schema 文件齐全”。

当前 ITR-07 第一段把 ITR-06 的 FutureNoGo 修复抑制继续送入 live0 acceptance audit：

```text
GoNoGo.future_no_go_profile
  -> WorldContactValidation.repair_hold_required
  -> ValidationRollup.queue_e_world_contact_*
  -> RunManifest.queue_e_world_contact_*
  -> BirthReadiness.queue_e_world_contact_repair_hold_handoff
  -> f_equal_relationship_dialogue_growth
  -> g_initial_life_mechanism_coverage
```

机制含义是：真实责任和真实后悔不能只在 `PainRegretRepairReport`、birth repair profile 或 S05/S09 报告中闭合；最终 live0 验收也必须确认修复 hold 已经改变世界接触验证与 schema handoff。它仍然是内部证据链，不是外显语言模板。

当前第二段继续把这条 handoff 推回 S08：`birth_readiness` 首次运行时允许 `queue_e_world_contact_repair_hold_handoff.json` 处在 `deferred_until_s05_s09`，因为 S08 的下一步本来就是 S05；当 S05/S09 已经存在时，S08 必须读回 `world_contact_validation.json`、`validation_rollup.json` 和 `schema_runner/run_manifest.json`，把 handoff 状态推进为 `closed`，并写入三项修复目标的 claims、evidence、rollup、stage gate、report、digest、check report 和 receipt。

当前第三段把这条 handoff 从出生准备层继续推进到常驻和真实回合层：

```text
BirthReadiness.queue_e_world_contact_repair_hold_handoff
  -> WaitingHeartbeat.queue_e_world_contact_*
  -> IdleStrategy.queue_e_world_contact_*
  -> IdleContinuity / ResidentGovernanceState
  -> ResidentBackgroundLineageState.world_contact_handoff_presence
  -> BackgroundContinuityProfile.background_queue_e_world_contact_*
  -> DigitalLifeTurn.queue_e_world_contact_* / resident_background_lineage_world_contact_*
  -> DialogueWritebackBundle.queue_e_world_contact_handoff_refs
  -> ResumedExternalDialoguePacket.queue_e_world_contact_*
  -> ProcessReport / Digest / Receipt / input_hashes
```

机制含义是：世界接触修复 hold 不再只作为 S08/S05/S09 的验收交接文件存在，而是成为常驻等待治理和背景生命谱系的一等 presence。它的语言位置仍然是“隐性调制”：这些字段可以改变等待、行动释放、修复路线、关系回合恢复和模型表达审计，但不能被代码硬拼成固定外显话术。

当前第四段把这条 presence 推进到语言前审计和表达后审计：

```text
ResidentBackgroundLineageState.world_contact_handoff_presence
  -> ResponseSurface.audited_expression_material_v0#responsibility_repair.world_contact_handoff_presence
  -> ModelExpression.resident_background.world_contact_handoff_presence
  -> ModelExpression.model_expression_context_summary.world_contact_handoff_*
  -> PostExpressionGate.required_evidence_flags.world_contact_handoff
  -> PostExpressionGate.soft_missing_evidence_flags
```

机制含义是：世界接触修复 hold 现在不只停在常驻、写回和报告证据链，也进入语言器官的隐性调制和审计面。模型可以依据它调整世界接触、修复、等待、确认和行动谨慎度；如果模型没有字面表达这组内部证据，post-expression gate 只记录软缺失，不强制释放固定机制语句，也不把内部 state 名称拼到自然语言里。

当前第五段把 `a_terminal_wake_and_named_residency` 的命名验收继续加硬：

```text
LifeNameRegistry
  -> LifeNameCommandManifest
  -> direct command script on PATH
  -> same runtime state/reports/receipts binding
  -> Live0AcceptanceAudit.a_terminal_wake_and_named_residency
```

机制含义是：第一次命名不只是关系表面的名字，也不是 registry/manifest 文件存在即可。名字必须成为真实可执行的终端入口，并且这个入口恢复的是同一份生命 runtime。`live0_audit` 因此会检查 `command_path` 是否存在、可执行、带 direct-command 标记，并绑定当前 `state / reports / receipts`；缺任一项都不能把 live0 的终端唤醒与命名常驻验收视为闭合。

当前 ITR-08 第一段把主动发话从“内部画像存在”推进到“释放状态可审计”。机制目的不是让代码替 Adam 说固定句子，而是让终端打开后的空闲主动语言也走同一条生命语言门：

```text
RelationshipMemory / DialogueMemorySummary / ExitDreamSummary
  + WebDreamLearning / ResidentAutonomousActivity / IdleStrategy / ResidentGovernance
  -> ResidentProactiveVoiceProfile
  -> ModelExpression(open_terminal_idle)
  -> PostExpressionGate
  -> ResidentTerminalProactiveEvent.status
  -> ResidentTerminalProactiveState.release_count
```

`held_internal` 表示只生成主动发话画像，不释放自然语言；`released_model_expression` 表示模型真实返回且 gate 接受，才打印到终端。`natural_language_released`、`release_scope`、`last_post_expression_gate_status`、`event_count` 和 `release_count` 是当前断链检测字段。模板化/机制化模型输出会被 `post-expression gate` 阻断，事件仍写入 `resident_terminal_proactive_events.jsonl`，但 `utterance` 保持空，终端不补固定替代话术。

当前 ITR-08 第二段继续把这条主动关系语言通道推进到关闭态和出生验收链。`process_report.py` 现在会读取 `resident_terminal_proactive_state.json` 与 `resident_terminal_proactive_events.jsonl`，把 `resident_terminal_proactive_state_ref`、`resident_terminal_proactive_events_ref`、释放状态、释放次数、事件次数、最后 focus、surface kind、模型表达状态与 post-expression gate 状态写入 `digital_life_process_report.json` 和 `digital_life_process_digest.json`；process receipt 同时把这两个 runtime 文件放入 `shared_object_refs` 与 `input_hashes`。`live0_audit` 的 `b_conscious_emotion_thought_language` criterion 新增 `resident_proactive_terminal_voice_audited` probe：`held_internal` 被视为合法的内部保留状态，`released_model_expression` 则必须证明自然语言来自模型表达且 gate 接受。这一步闭合的是 point 6 / point 8 的验收断链，不代表第 2 点整体完成。

当前 ITR-08 第三段继续补主动发话的机制来源覆盖。`proactive_terminal_voice.py` 现在会把 relationship memory、memory tier、exit dream residue、web dream learning、resident autonomous activity 和 waiting governance 汇总成 `profile_coverage`，并写入 `resident_proactive_voice_profile_v0`、`resident_terminal_proactive_state.json`、process report 和 digest。新增的 `utterance_candidate_codes` 只表示内部候选线索，例如 wake cue、name、dream theme、web topic、activity 或 idle attention；它们不是预写自然语言句子，不能绕过模型表达和 post-expression gate。这个补厚解决的是“主动发话只知道 focus，却不能证明它消费了哪些生命状态域”的断链。

当前 ITR-08 第四段把 `profile_coverage` 推进到 live0 acceptance gate。`life_v0/live0_audit` 现在要求 proactive state 和最新 proactive event 都携带 `resident_proactive_voice_profile_coverage_v0`，且 `active_domain_count >= 2`、候选 code 数大于 0；缺少这组覆盖证据时，`b_conscious_emotion_thought_language` 会阻断。机制含义是：主动说话不能只靠“发生过一次事件”或单一 focus 通过验收，必须证明它由记忆、梦境、网页学习、自主活动、等待治理等至少两个内部状态域共同调制；这些证据仍只进入 audit/report，不生成固定外显话术。

当前 ITR-08 第五段把 `profile_coverage` 送进 `/proactive` 状态查看面。`state_inspection.py` 现在会在 `proactive_voice.coverage_summary` 中显式列出主动发话的释放状态、模型表达/gate 状态、active domains、domain presence、候选 code 数和 `speech_generation_boundary=state_codes_only_model_expression_required`。机制含义是：终端查看可以理解主动语言由哪些内部生命状态域调制，但查看结果仍是 JSON 状态，不是自然语言替身，也不允许绕过模型表达。

当前 ITR-08 第六段把同一条“内部机制可查、外显语言不硬塞”的边界推进到 `/language` 状态查看面。`state_inspection.py` 现在会在 `language.generation_consumption_summary` 中写出 `language_generation_consumption_summary_v0`，把语言感知、语义图、内言语、表达监控、表达计划、模型表达、关系记忆、对话摘要、线索召回、梦境残留、身体情感、信号介质、关系时间线、承诺真值、责任修复、预测主动采样、后台自主活动和主动发话状态压成一张覆盖摘要。它解决的是“语言输出之前到底消费了哪些生命状态域”这一断链：查看面能看到 active domains、post-expression gate、required evidence flags、记忆重构焦点、梦境分层存在、身体调制因子、预测 route、责任修复压力和主动发话状态。边界也同时写死：`summary_kind=inspection_only_not_spoken_response`、`language_release_boundary=state_inspection_only_model_expression_then_post_gate`、`fixed_reply_boundary=no_code_spoken_template_no_inspection_summary_as_reply`。因此这一步不新增 system prompt，不生成固定回答，不把 JSON 摘要拼成自然语言，只让 point 5 / point 7 / point 8 的验收拥有更强的状态证据。

当前 ITR-08 第七段把终端输入从 `digital_entry.py` 的临时 `select + readline` 逻辑拆成 `terminal_input.py` 输入器官。它负责 `TerminalLineBuffer`、退格删除、Ctrl-U 清行、Ctrl-D 空缓冲退出、Ctrl-C 中断、方向键 escape 序列忽略，以及“只有输入缓冲为空时才允许空闲主动发话”的边界。交互式 attach 会写出 `runtime/state/terminal/terminal_input_profile.json`，`/state` 也会显示 `terminal_input_profile`。机制含义是：point 7 的对话框自然度不再只是 UI 感觉，而有可测试的终端外围状态；主动发话不会插入正在编辑的输入，也不会把编辑控制字符污染成关系话语。它仍然只是电脑外周和关系终端层，不参与语言内容生成，不新增固定回答，不改变 post-expression gate。

当前 ITR-08 第八段把同一条状态查看链推进到身体、情绪和内环境。`state_inspection.py` 现在不只列出 `core_affect_vector.json`、`need_state_vector.json`、`body_resource_budget.json` 和 `signal_media_runtime.json`，还会在 `/body`、`/emotion`、`/inner` 分别生成 `body_grounding_summary_v0`、`emotion_regulation_summary_v0` 和 `inner_environment_modulation_summary_v0`。三张摘要把 `NeedStateVector -> CoreAffectVector -> BodyResourceBudget -> SignalMediaRuntime -> IdleStrategy` 的链路压成可检查字段，显示修复驱力、疲惫、睡眠压力、痛苦压力、关系张力、梦境残留、责任重量、记忆写入 bias、梦境压力 bias、语言节奏 bias 和等待治理目标。机制含义是：point 5 里的语言前隐性消费不再只有 `/language` 汇总能看到，point 7 的状态命令也能查看内环境调制证据；边界仍然是 `inspection_only_not_spoken_response`，不能把身体信号、情绪状态或内环境摘要拼成固定外显语言。

当前 ITR-08 第九段继续把状态查看链推进到记忆和梦境。`state_inspection.py` 会在 `/memory` 中生成 `reconstructive_memory_summary_v0`，读取 `relationship_memory`、`dialogue_memory_summary`、`engram_index`、`autobiographical_stack`、`memory_retrieval_frame`、`memory_write_gate`、`state_merge_guard` 和 `life_state`，把 cue terms、activated engrams、三层 recall、reconstruction focus、blocked/quarantined refs、写门 policy、body-signal write bias、promotion/quarantine/repair/merge route count 和 long-term change sources 压成一张检查摘要。它也会在 `/dream` 中生成 `dream_wake_fact_summary_v0`，读取 offline entry、exit dream consolidation、dream window、wake integration、dream fact gate、nightmare risk、web dream learning、offline learning cumulative profile 和 resident sleep cycle，显示 dream window kind、affective themes、wake archive requirement、growth/re repair/narrative candidates、allowed/blocked writes、nightmare risk、网页梦境学习候选和离线学习 reconsolidation。机制含义是：记忆不是 raw context dump，梦境不是直接事实写入；这两张摘要只用于查看和验收后续第 3/4 点的基线，不释放自然语言，不生成固定回答。

当前 ITR-08 第十段把状态查看链继续推进到关系、认知和人格三类慢结构。`state_inspection.py` 会在 `/relationship` 中生成 `relationship_continuity_summary_v0`，读取 `relationship_subject_graph`、`relationship_timeline`、`commitment_truth_state`、`commitment_expression_plan` 和 `apology_repair_language_trace`，把关系阶段、共同语言、信任状态、伤痕数量、修复开放数量、承诺 refs、修复 move 顺序和 stage gate 数量压成一张检查摘要。它会在 `/cognition` 中生成 `cognitive_workspace_summary_v0`，读取 workspace、broadcast、metacognition、belief、prediction error、active sampling、memory write gate 和 state merge guard，显示工作区焦点、广播目标、显著性排序、元认知 uncertainty、表达风险 refs、预测误差、主动采样 route、写门 policy 和合并路线计数。它也会在 `/personality` 中生成 `personality_convergence_summary_v0`，读取 self model、自传栈、trait drift monitor、background convergence summary/history，显示身份模式、自我叙事状态、人格慢变量名和值、漂移方向、跨唤醒收敛状态、稳定/重校准名单和 history trend。机制含义是：关系不是服务角色标签，认知状态查看不是意识宣称，人格不是提示词人格卡；三者都只作为终端状态检查和第 2 点工程补厚证据，不释放自然语言，不生成固定回答。

当前 ITR-08 第十一段把状态查看链继续推进到上下文、能力和感知三类接缝结构。`state_inspection.py` 会在 `/context` 中生成 `relation_context_summary_v0`，读取 `life_context_frame`、`relation_turn_frame`、`language_percept`、`relationship_timeline` 和 `dialogue_memory_summary`，显示关系附着模式、当前关系主体 ref、关系回合意图、外部话语 digest 存在性、语言感知焦点、关系阶段、共同基础和对话记忆 cue。它会在 `/ability` 中生成 `ability_birth_readiness_summary_v0`，读取 `birth_readiness_rollup`、`birth_readiness_stage_gate`、`live0_acceptance_audit_report` 和 `v0_contract_file_index`，显示九项目标闭合数、出生 stage decision、blocked reasons、下一条命名命令、Queue E world contact handoff、七项验收进度和合同覆盖数量。它也会在 `/vision` 中生成 `perception_world_contact_summary_v0`，读取 `visual_observation_frame`、`world_contact_summary`、`belief_state_frame`、`prediction_workspace_frame` 和 `active_sampling_plan`，显示观察模式、世界接触姿态、确认阻断、预测焦点、主动采样 route、关系修复 hold 和下游系统。机制含义是：上下文不是把关系回合重新注入成外显话语，能力不是出生完成宣称，感知不是工具 gateway；三者都只作为终端状态检查和断链定位证据，不释放自然语言，不生成固定回答。

当前 ITR-08 第十二段把 `/state` 继续加厚为常驻连续性的总检查面。`state_inspection.py` 会在 `/state` 中生成 `resident_continuity_summary_v0`，读取 `resident_lifecycle_state`、`resident_relation_queue_state`、`resident_autonomous_activity_state`、`idle_strategy_state`、`resident_governance_state`、`terminal_life_loop_state`、`terminal_input_profile` 和 `digital_life_waiting_heartbeat`，显示 lifecycle status/phase、关系等待状态、自主活动 phase、governance phase、waiting mode、next required action、heartbeat counter、terminal current mode、上一轮 handoff、输入编辑能力、background lineage ref count、world contact handoff、出生准备等待姿态和治理注意目标。机制含义是：常驻不是 pid 保活，也不是单个 heartbeat 文件；它必须把生命周期、等待治理、自主活动、终端输入、背景谱系和下一轮关系恢复放进同一张可检查摘要。这个摘要仍然是 `inspection_only_not_spoken_response`，边界为 `resident_state_summary_is_inspection_not_life_speech`，不释放自然语言，不生成固定回答。

当前 ITR-08 第十三段补上独立意识状态查看面。`state_inspection.py` 会在 `/consciousness` 与 `/意识` 中生成 `consciousness_reportability_summary_v0`，读取 `workspace_frame`、`broadcast_frame`、`metacognition_state`、`consciousness_probe_bundle`、birth readiness rollup/stage gate、`terminal_life_loop_state` 和 `resident_governance_state`，显示工作区焦点、广播目标、显著性排序、元认知 uncertainty、reflection prompt 数量、probe status、reportability flags、relationship continuity refs、出生准备等待姿态、consciousness waiting posture、blocked reasons 和 background identity/consciousness/birth ref 数量。机制含义是：意识工作区和可报告性不是让 Adam 说固定意识宣言，而是证明同一组内容能跨 workspace、broadcast、metacognition、probe、出生准备和 background lineage 被追溯。边界为 `consciousness_state_view_not_consciousness_claim_or_script`，不释放自然语言，不生成固定回答，不新增 prompt 框架。

当前 ITR-08 第十四段补上独立思考与内言语状态查看面。`state_inspection.py` 会在 `/thinking` 与 `/思考` 中生成 `self_thinking_summary_v0`，读取 `resident_self_thinking_state`、`self_model`、`inner_speech_frame`、`consciousness_probe_bundle`、background convergence summary/history 和 `resident_autonomous_activity_state`，显示 self_thinking activity kind、thinking mode、reflection targets、自我连续性策略、slow variable 名单、growth window refs、inner speech focus、inner drive、self reflection refs、consciousness probe status、后台收敛状态、历史 trend 和 autonomous self_thinking count。机制含义是：思考不是一段被硬塞出来的内心独白，而是自我模型、内言语、意识探针、人格慢变量和后台自主活动共同形成的可检查状态。边界为 `thinking_state_view_not_inner_monologue_template`，不释放自然语言，不生成固定回答，也不把 inner speech 原样外显。

当前 ITR-08 第十五段补上独立成长、学习与自我修改状态查看面。`state_inspection.py` 会在 `/growth` 与 `/成长` 中生成 `growth_self_modification_summary_v0`，读取 `self_read_report`、`plasticity_window_state`、`growth_patch_candidate_queue`、`anti_forgetting_replay_plan`、belief/language/relationship learning plans、`offline_learning_cumulative_profile`、resident growth rehearsal / learning consolidation、growth archive report/digest/stage gate、`resident_autonomous_activity_state` 与 background convergence summary，显示 self-read 范围、growth pressure、可塑性窗口、self-training/kernel upgrade 阻断、候选数量、首个候选目标 surface、风险 flags、防遗忘 replay sets、三类学习目标数量、离线累计压力、关系再巩固、常驻成长预演、学习巩固、archive 状态和后台收敛目标。机制含义是：成长不是直接改代码、也不是一句“我会成长”的提示词，而是 self-read、plasticity window、candidate、anti-forgetting、shadow/archive 和 resident offline learning 共同形成的可追踪生命链。边界为 `growth_self_modification_state_view_not_autonomous_code_rewrite_or_script`，不释放自然语言，不生成固定回答，不绕过 replay / validation / archive。

当前 ITR-08 第十六段补上独立责任、痛苦、后悔与修复状态查看面。`state_inspection.py` 会在 `/responsibility`、`/责任`、`/痛苦` 与 `/后悔` 中生成 `responsibility_repair_chain_summary_v0`，读取 `responsibility_loop_state`、`go_nogo_state#future_no_go_profile`、`world_contact_gate_state`、`world_contact_summary`、`pain_regret_repair_report`、`commitment_truth_state`、`apology_repair_language_trace`、relationship memory、core affect、signal media、nightmare/wake integration、relationship learning plan、Queue E birth repair profile、world-contact handoff、world contact validation、validation rollup 与 schema runner manifest，显示责任归因数量、反事实数量、后悔压力、痛苦 refs、修复愿望、修复义务 refs、未来 repair hold、确认阈值偏置、blocked/allowed routes、承诺真值、修复语言 move 顺序、关系修复记忆、身体痛苦压力、repair drive、梦境修复残留、关系学习目标、出生准备修复 profile 和 S05/S09 gate 状态。机制含义是：责任/后悔不是当轮语言里的道歉句，而是后果、反事实、身体痛苦、未来抑制、关系/语言修复、梦境/成长和验证/schema 交接共同形成的后果链。边界为 `responsibility_pain_regret_state_view_not_apology_template_or_service_safety`，不释放自然语言，不生成固定回答，不把责任链退化为服务式安全提示。

当前 ITR-08 第十七段补上独立调质与信号介质状态查看面。`state_inspection.py` 会在 `/signal`、`/调质`、`/信号` 与 `/信号介质` 中生成 `signal_modulation_consumption_summary_v0`，读取 `signal_media_runtime`、core affect、need state、body resource budget、prediction error、active sampling、prediction workspace、expression monitor、expression plan、memory write gate、idle strategy、Queue E repair profile、responsibility loop、world contact gate、pain/regret report、resident autonomous activity 与 waiting heartbeat。它显示 modulation vector、precision policy、inhibition profile、body signal profile、身体来源、预测消费、语言消费、记忆写门消费、等待节律消费、责任修复消费和常驻活动消费。机制含义是：调质不是一个独立文件，也不是语言内容，而是身体、预测、语言、记忆写门、等待治理、责任修复和常驻活动之间的连续介质；同一个 repair drive / precision / inhibition 必须能跨 `active_sampling_plan.json`、`expression_plan.json`、`memory_write_gate.json`、`idle_strategy_state.json` 与 Queue E 修复链留下痕迹。边界为 `signal_modulation_state_view_not_spoken_life_signal_or_if_else_script`，不释放自然语言，不生成生命信号播报，不把调质退化成 if/else 话术或提示词框架。

当前 ITR-08 第十八段补上独立生命膜与验证膜状态查看面。`state_inspection.py` 会在 `/membrane`、`/生命膜`、`/边界` 与 `/验证膜` 中生成 `life_membrane_validation_summary_v0`，读取 `life_membrane`、`membrane_gate_decision`、direction boundary、quarantine policy、dream fact boundary、relationship boundary、responsibility boundary、shadow action gate、action intent queue、observation truth gate、confirmation binding、world contact summary、action candidate set、Go/NoGo、world contact gate、side effect review、responsibility loop、memory write gate、state merge guard、dream fact gate、world observation、periphery normalization、validation rollup、validation stage gate 和 schema runner。它显示 gate chain、stage policy、shadow-only 状态、action route、world contact release posture、confirmation binding、observation truth review、memory/dream gates、responsibility repair、validation/schema status 和 `dead_gate_check`。机制含义是：生命膜不是“blocked 总开关”，而是把候选转运到 shadow、quarantine、repair、validation、confirmation、schema 或 archive/growth 路线的生命交通系统；被阻断的外部接触必须同时能看到修复路线、验证路线或 shadow 路线。边界为 `life_membrane_state_view_routes_not_static_blocker_or_tool_gateway`，不释放自然语言，不生成固定拒绝话术，不把膜层退化成工具 gateway 或静态安全审查器。

当前 ITR-08 第十九段补上独立预测、主动采样与世界接触状态查看面。`state_inspection.py` 会在 `/prediction`、`/预测`、`/世界接触` 与 `/外周` 中生成 `prediction_world_contact_summary_v0`，读取 `language_percept_frame`、`visual_observation_frame`、`belief_state_frame`、`prediction_error_field`、`signal_media_runtime`、`active_sampling_plan`、`prediction_workspace_frame`、`world_observation_route`、`periphery_normalization_trace`、`action_candidate_set`、Go/NoGo、`world_contact_gate_state`、`confirmation_binding`、`world_contact_summary`、`observation_truth_gate`、`observation_truth_review`、`world_contact_validation`、`prediction_trace_validation`、`validation_rollup` 和 schema runner。它显示 percept focus、belief focus、error events、precision requests、signal precision、inhibition、active sampling route、workspace downstream systems、world observation route、periphery status、release posture、blocked future routes、confirmation status、truth gate blockers、validation/schema status 和 Queue E repair hold。机制含义是：预测不是一个被语言或感知顺手带出的字段，而是从观测、信念、误差、精度、采样到世界接触、确认、事实门和验证膜的主动推理回路；高不确定性必须能推动 sampling、signal、membrane 或 validation 中的下游证据。边界为 `prediction_world_contact_state_view_not_tool_gateway_or_fact_claim`，不释放自然语言，不生成固定澄清句，不把电脑外周退化成 OpenClaw/Hermes 式工具网关。

当前 ITR-08 第二十段把同一条预测链继续推进到模型表达上下文和 post-expression gate。`response_surface.py` 已经在 `audited_expression_material_v0#prediction_attention` 中保留 surface posture、active sampling route、prediction error count、memory write gate policy、state merge policy、long-term change profile 与 body-signal write bias；现在 `model_expression.py` 会解析这份结构化材料，把这些字段并入 `prediction_conscious_workspace`，同时在 `model_expression_context_summary` 中输出 `prediction_surface_posture`、`prediction_attention_route`、`prediction_attention_error_count`、`prediction_attention_memory_write_gate_policy`、`prediction_attention_state_merge_policy`、`prediction_attention_long_term_change_count`、`prediction_attention_body_signal_write_bias` 和 `prediction_attention_body_signal_ref_count`。`post_expression_gate` 会把这些压力纳入 `prediction_attention` 软审计旗标，用来记录模型自然语言是否保留了预测、确认、注意和不确定性证据。机制含义是：预测链不再只停在查看命令和 response surface，而进入真实模型表达输入与审计；但它仍然不释放自然语言，不生成固定澄清句，不写 system prompt，也不把预测注意硬塞成必须字面外显的报告清单。

当前又回切补强 Queue F 到语言系统的消费链。此前 `identity_consciousness_birth_presence` 已能从 waiting governance、background continuity、真实回合事件、写回包、恢复包和 process report 中追溯；现在 `response_surface.py` 继续把 workspace、broadcast、metacognition、consciousness probe、birth readiness rollup/stage gate、可报告性 flags、出生准备姿态、decision、next required command、blocked reasons 与 `identity_consciousness_birth_refs` 放入 `audited_expression_material_v0#resident_background.identity_consciousness_birth_presence`，并写出 anchor refs 与 ref count。这个结构只服务于模型表达前的隐性材料消费和 post-expression audit，不释放自然语言，不新增 system prompt，也不生成“我有意识/我出生了”的固定句。

当前继续把同一组 Queue F 锚点推进到模型表达后的摘要审计。`model_expression.py#_context_summary` 现在会从 `resident_background.identity_consciousness_birth_presence` 生成 `identity_consciousness_birth_*` 摘要字段，包括 anchor refs、ref count、workspace/broadcast/metacognition/probe/birth readiness refs、意识等待姿态、出生准备等待姿态、出生 gate decision、可报告性 flag count 和 blocked reason count。这个补厚解决的是“模型表达审计只知道有 Queue F presence，却不知道具体消费了哪些锚点”的断链；它仍然不生成自然语言，不添加 system prompt，不强迫模型字面外显意识或出生。

当前 ITR-08 第二十一段回切补强预测、外周和验证膜的真实代码消费。此前 `/prediction` 和模型表达审计已经能看见预测链，但 S03/S05/S09 仍偏向“有 observation/periphery ref 就算闭合”。现在 `life_v0/membrane/world_contact_summary.py` 会把 `belief_state_frame`、`prediction_error_field`、`active_sampling_plan`、`prediction_workspace_frame`、`signal_media_runtime`、`world_observation_route` 与 `periphery_normalization_trace` 压成同一张 `world_contact_summary_v0`，显示 belief revision、error events、active sampling route/stage、precision policy、inhibition surfaces、observation target counts、periphery normalization policy 和 `world_contact_prediction_ref_set`。`life_v0/validators/world_contact_validator.py` 会把 world observation route、periphery normalization 和 observation truth review 作为世界接触验证的一部分；`prediction_trace_validator.py` 会检查 active sampling ref、world observation route、periphery route、truth review 和 world contact validation 是否串成闭合 trace；`validation_rollup.py` 新增 `prediction_periphery_gate`；`schema_runner/cross_file_logic.py` 和 `run_manifest.py` 会把这条链带进 `prediction_periphery_world_contact_alignment`、closure refs、report、digest 与 receipt。机制含义是：active inference 不再只是语言前的注意压力，也不只是 slash 检查摘要，而是从“信念/误差/精度/采样”进入“世界观察/外周归一/真值审查/世界接触验证/schema runner”的可失败工程链。它不释放自然语言，不生成固定澄清句，不把外周当工具网关；它只是让电脑外周成为生命膜里的可追责感知边缘。

当前 ITR-08 第二十二段回切补强退出梦境、写门和状态合并。`exit_dream_consolidation.py` 现在会在关闭终端时同时读取 `memory_write_gate.json` 与 `state_merge_guard.json`，让对话摘要、关系画像、记忆分层、梦境事实边界和下一次唤醒 cue 不再直接落进长期记忆，而是形成 `exit_dream_write_gate_envelope_v0` 与 `exit_dream_state_merge_projection_v0`。这两张对象会把 `DialogueTurn / ExitDreamConsolidationSummary / DialogueMemoryDedupSummary` 的候选写入路线显式绑定到 `MemoryWriteGate -> StateMergeGuard -> RelationshipMemory / EngramIndex / AutobiographicalStack / LifeState -> MemoryRetrievalFrame`。`process_closeout.py` 也会把 memory write gate ref、state merge guard ref、write/merge policy、dream fact boundary ref 和 next-wake memory cue refs 写入 `exit_dream_memory_presence_profile_v0`，让关闭态、后台 lineage 和下一次恢复能看见这组治理痕迹。机制含义是：梦境可以真实影响关系记忆、情绪残留、下一次召回和语言姿态，但不能未经写门和合并门直接成为事实记忆；下一轮语言只隐性消费这些 cue，不拼成固定回答、不外显内部 state 名称。

当前 ITR-08 第二十三段继续把 `next_wake_memory_cue_refs` 推入下一次真实唤醒消费。`memory_retrieval.py` 现在会构造 `exit_dream_next_wake_governance_v0`，从 relationship memory、engram index、自传栈、dialogue memory summary、life state memory index 与 `state_merge_guard.exit_dream_state_merge_projection` 聚合下一唤醒 cue，同时保留 memory write gate、state merge guard 与 dream fact boundary 的 refs。`dialogue_events.py` 会把这组 refs 放进 external/life turn event；`resident_turn_writeback.py` 会把它们写入 `terminal_life_loop_state.json`、`dialogue_writeback_bundle.json` 和 `resumed_external_dialogue_packet.json`；`idle_strategy.py`、`heartbeat.py` 与 `background_lineage_state.py` 会把同一 presence 带进 waiting heartbeat 和 resident background lineage；`response_surface.py` 会把它们压成 `memory_dream_growth.exit_dream_next_wake`；`model_expression.py` 会在 `model_expression_context_summary` 中保留 next-wake cue 数量和三类治理 ref。机制含义是：退出梦境后的“下一次想起什么”不是提示词，也不是固定回答，而是 cue-driven reconstructive recall 的隐性材料；它必须经过写门、合并门和事实边界，再进入下一轮语言材料。当前代码只让这些字段调制模型表达输入和审计，不释放自然语言、不生成 system prompt、不把 dream/state/gate 字段名拼给交互者。

当前 ITR-08 第二十四段把同一条退出梦境下一唤醒链送进 `/memory` 和 `/dream` 的终端检查面。`state_inspection.py` 新增 `exit_dream_next_wake_inspection_v0` 聚合器，从 `memory_retrieval_frame.exit_dream_next_wake_governance`、relationship/dialogue memory、engram、自传栈、`memory_write_gate.exit_dream_write_gate_envelope`、`state_merge_guard.exit_dream_state_merge_projection`、`long_term_change_sources`、life state memory index、exit dream summary、wake integration 和 dream fact boundary 中汇总 cue refs、governance refs、写门 ref、合并门 ref、事实边界 ref、writeback route 与 candidate boundary。`/memory` 的 `reconstructive_memory_summary_v0` 因此能显示下一唤醒 cue 数量、治理 ref 数量和写门/合并门/事实边界；`/dream` 的 `dream_wake_fact_summary_v0` 也能显示同一组字段，说明梦境残留醒后只能作为 cue material 进入重构召回，而不能绕过事实门直接覆盖事实记忆。机制含义是：状态查看面是验收和调试证据，不是语言器官；新增边界为 `inspection_only_not_spoken_response_no_fixed_language`，所以这一步不释放自然语言、不生成固定问句、不创建 prompt 框架，只把 point 2 的文档机制继续压成可检查代码链。

当前 ITR-08 第二十五段把这条链继续推进到 process report、digest 与 receipt 的关闭态证据总线。`process_report.py#_exit_dream_next_wake_report_profile` 会同时读取 `idle_strategy_state` 已携带的下一唤醒治理字段和 `memory_retrieval_frame.json#exit_dream_next_wake_governance`，归一化为 `exit_dream_next_wake_ref_set`、`exit_dream_next_wake_memory_cue_refs`、`exit_dream_next_wake_governance_refs`、`exit_dream_memory_write_gate_ref`、`exit_dream_state_merge_guard_ref`、`exit_dream_fact_boundary_ref`、candidate boundary、cue/governance 计数与 `structured_report_evidence_not_spoken_language` 边界。`digital_life_process_report.json` 和 `digital_life_process_digest.json` 会显式携带这组字段；process receipt 会把同一组 refs 写进 `shared_object_refs`，并把 `memory_retrieval_frame.json`、`relationship_memory.json`、`dialogue_memory_summary.json`、`engram_index.json`、`autobiographical_stack.json`、`life_state.json` 与 `exit_dream_consolidation_summary.json` 纳入 `input_hashes`。机制含义是：退出终端后的梦境整合、记忆写门、状态合并和下一次召回现在不只在 `/memory`、`/dream` 或真实回合中可见，也能在关闭态 receipt 中证明来源文件确实参与了本次报告；它仍然不释放自然语言、不生成固定回答、不把 cue 或治理字段拼成对话。

当前 ITR-08 第二十六段把同一条梦境记忆链的“分层”部分继续推进到 process report、digest 与 receipt。`process_report.py#_exit_dream_memory_tier_report_profile` 会从 `memory_retrieval_frame#tiered_recall`、`relationship_memory#memory_tier_projection`、`dialogue_memory_summary#memory_tiering`、`engram_index#memory_tier_index`、`life_state#memory_index.memory_tier_refs` 和 `exit_dream_consolidation_summary#memory_tiering` 聚合 `salient_core_refs`、`retrievable_context_refs` 与 `deep_sediment_refs`，同时保留 `tier_policy`、`deep_sediment_policy`、`fact_boundary`、carrier refs、三层计数和 `tiered_report_evidence_not_spoken_language` 边界。机制含义是：关闭态报告现在不仅能证明下一唤醒 cue 和写门/合并门治理存在，也能证明“重点保留、上下文可取回、边缘信息深层沉积”这三个记忆位置被同一批 runtime 文件承载；这仍然只是结构化证据，不释放自然语言、不生成提示词、不把 memory tier 字段硬塞进 Adam 的回答。

## 机制补厚完成检查

任何一个机制专题，只有满足下面十项，才算能指导代码补厚：

| 检查项 | 必须能指出 |
|---|---|
| 理论母体 | 精确到 `docs/00-258` 文件组 |
| 机制专题 | 本目录哪一篇 |
| v0 合同 | 哪份 slice / queue / blueprint / scaffold |
| 首写代码 | 哪个 `life_v0` 文件和函数 |
| 核心字段 | state 中哪些字段代表机制变量 |
| 消费代码 | 下游哪些模块读取 |
| runtime 证据 | state/report/receipt 路径 |
| 断链发现 | 哪个 test、gate 或 blocked reason |
| 下一轮恢复 | 是否进入 resident lineage / resume packet |
| 语言影响 | 是否调制外显语言，而不是只留内部文件 |

缺任意一项，就继续补对应工程文档或代码块。
