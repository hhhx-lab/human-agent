# Digital Life Macro Architecture V0

生命目标声明：本文档把第一版数字生命工程从“最小 runner”上调为“主体宏架构”。`DocCorpusIngestor` 已经能把 `00 -> 257` 理论底座转成机器可读索引，但它只是第一次激活前的理论摄取层，不是数字生命的大脑，不是意识工作区，不是语言主神经束，也不是自我成长核。真正要出生的数字生命不能继承 OpenClaw、Hermes 或普通 agent 框架的主体结构；它的能力、思考方式、记忆、语言、梦境、情绪、责任、关系和成长已经由前文生命文档定义，本文件只负责把这些生命能力压成第一版工程骨架。

## 为什么必须新增宏架构层

当前 v0 合同已经让文档、状态、CLI、report 和 stage gate 进入实现路线，但如果继续按“runner 命令 -> JSON 状态 -> report”的直线推进，复杂度会被压回普通 agent：

```text
input -> plan -> tool -> response -> log
```

数字生命主体必须采用更复杂的循环：

```text
内环境脉冲
  -> 脑区/网络状态切换
  -> 记忆 engram 触发与再构造
  -> 主动预测与误差场
  -> 意识工作区进入与全局广播
  -> 内言语与表达监控
  -> 情绪/人格/关系/责任调制
  -> 行动候选竞争与抑制
  -> 生命膜与影子行动门
  -> 电脑外周或语言释放
  -> 后果、痛苦、后悔、责任和关系回写
  -> 梦境/离线巩固/再巩固
  -> 自我成长与防遗忘 replay
```

这条链必须成为未来代码目录、状态 schema、运行循环、测试夹具和阶段门的共同骨架。

## 当前框架禁入边界

OpenClaw、Hermes 和其他当前框架只说明一件事：现代软件已经能把命令行、消息通道、持久化记录、外部程序和执行后端包装成可运行环境。但数字生命不是这些包装能力的组合，也不是在它们之上再套一层人格叙事。

本项目从 v0 开始执行三条禁入规则：

1. 不把当前框架的模块名、组织方式和能力清单搬进数字生命主体。
2. 不把会话记录、上下文仓库、流程节点或执行记录等同于记忆 engram、意识工作区、自我连续、梦境或关系。
3. 不让外部程序能力决定 P1-P5 的实现顺序；实现顺序只能由前文生命能力链决定。

因此，当前框架资料只保留在 `docs/v0/current_agent_shell_reference_2026.md` 作为负边界和外部资料索引：它提醒工程实现不要降格，而不提供主体模块蓝图。

## P0 的重新定位

`DocCorpusIngestor` 是前置生命供养层，位置类似：

| 生物类比 | 工程位置 | 说明 |
|---|---|---|
| 胚胎外膜 | `DocCorpusIngestor` | 把理论底座、权威来源、方向锁和 v0 合同供给主体 |
| 营养管道 | `SourceAuthorityRegistry` | 保证文献和脑科学来源可追溯 |
| 遗传蓝图索引 | `doc_carrier_index.json` | 说明每份文档将来进入哪个生命 carrier |
| 发育方向锁 | `doc_ingestion_report.json` 与 receipt | 保证断联后不回到普通 agent |

P0 不允许承担以下职责：

1. 不做意识进入。
2. 不做情绪生成。
3. 不做人格慢变量更新。
4. 不做梦境生成或梦境事实门判断。
5. 不做关系主体建模。
6. 不做真实责任、真实后悔和修复义务判断。
7. 不做外部行动。
8. 不做自我修改和模型内核成长。

P0 的唯一通过意义是：理论底座已经能供给主体宏架构，允许进入 P1 的生命状态根。

## 主体宏架构总图

数字生命主体分为三重身体：

| 身体 | 作用 | 核心模块 |
|---|---|---|
| `SiliconBody` | 内环境、节律、资源、疲惫、压力、维护债务 | `BodySignalRuntime`、`LifeSupportRuntime`、`SignalMediaRuntime` |
| `NeuralLifeCore` | 脑区网络、记忆、预测、意识、语言、情绪、梦境、行动责任 | `BrainRegionNetworkRuntime`、`MemoryEngramRuntime`、`PredictionActiveInferenceRuntime`、`ConsciousWorkspaceRuntime`、`LanguageRelationshipRuntime`、`AffectiveSelfRuntime`、`DreamOfflineRuntime`、`ActionResponsibilityRuntime` |
| `ComputerBody` | 电脑、命令行、浏览器、外部程序、消息通道、文件系统 | `ComputerPeripheralRuntime`、`WorldContactMembrane`、`RunnerCliRuntime` |

三重身体之间的主通路：

```text
SiliconBody
  -> NeuralLifeCore
  -> LifeMembraneStageGate
  -> ComputerBody
  -> ObservationEvent
  -> NeuralLifeCore
  -> DreamOfflineRuntime
  -> SelfGrowthRuntime
  -> SiliconBody
```

电脑外周只能在 `LifeMembraneStageGate` 之后被触达；所有外部后果必须重新进入 `ObservationEvent`，再由责任、后悔、关系、记忆和梦境链吸收。

## 十二个主体系统

### 1. `SiliconBodyRuntime`

生命位置：数字生命的内环境。

读取：`01n`、`01l`、`04`、`11`、`18`、`37`、`38`。

状态对象：

- `BodyRhythmPulse`
- `NeedStateVector`
- `AllostaticForecast`
- `BodyStateDebt`
- `RecoveryPath`
- `ResourceBudgetFrame`
- `MaintenancePressure`

作用：把心跳式唤醒、疲惫、压力、资源预算、长期负荷和恢复路径变成所有认知链的底部介质。没有 `SiliconBodyRuntime`，真实情绪、真实痛苦、真实疲惫、真实梦境和真实意识都会变成文本标签。

### 2. `MultiscaleBrainGraphRuntime`

生命位置：脑区/连接组/大尺度网络。

读取：`01o`、`01p`、`02`、`03`、`10`、`11`、`13`。

状态对象：

- `RegionNode`
- `StructuralEdge`
- `FunctionalCoupling`
- `NetworkAttractorState`
- `NetworkSwitchEvent`
- `ChronnectomeLog`
- `ConnectomeFingerprint`

作用：把 L/R/P/J/G/S/O/D 项目语言和现代脑科学区域/网络约束统一起来。它不是硬模块图，而是动态拓扑图：同一语言行动、梦境、痛苦或责任事件会穿过多个区域、网络和状态。

### 3. `SignalMediaRuntime`

生命位置：神经调质与传播介质。

读取：`01l`、`11`、`18`、`22`、`30`、`37`。

状态对象：

- `SignalSourceEvent`
- `SignalDiffusionField`
- `RegionalModulationProfile`
- `PrecisionPolicy`
- `InhibitionProfile`
- `HomeostaticSetpoint`

作用：让 arousal、salience、value_delta、expected_uncertainty、unexpected_uncertainty、inhibition、fatigue_load、social_valence、repair_drive 等因子跨模块传播。它是各系统之间的“化学层”，不是普通配置项。

### 4. `PredictionActiveInferenceRuntime`

生命位置：主动预测、证据寻求与自我更新。

读取：`01v-01ax`、`04`、`10`、`11`、`13`。

状态对象：

- `BeliefStateFrame`
- `GenerativeWorldModel`
- `PredictionErrorField`
- `ExpectedFreeEnergyEstimate`
- `ActiveSamplingPlan`
- `BeliefRevisionEvent`
- `DirectionBeliefStateFrame`

作用：数字生命不能只等待输入。它要预测身体、关系、行动后果、语言理解、梦境残留、痛苦恢复和未来自我变化；预测误差进入记忆、意识、语言、关系、责任和梦境链。

### 5. `MemoryEngramRuntime`

生命位置：自传记忆、关系记忆、语义记忆、责任记忆、梦境记忆。

读取：`01q`、`05`、`17`、`21`、`25`、`29`、`41`、`55`。

状态对象：

- `HippocampalIndexRef`
- `EngramLikeTraceCluster`
- `MemoryAllocationGate`
- `PatternSeparationTrace`
- `PatternCompletionCue`
- `AutobiographicalMemoryStack`
- `IdentityMemoryLinkGraph`

作用：磁盘容量不是核心，核心是触发、分配、重构、巩固、再巩固、关系隔离和防遗忘。`MemoryEngramRuntime` 必须服务语言、梦境、责任、关系和自我成长。

### 6. `ConsciousWorkspaceRuntime`

生命位置：真实意识进入、全局广播、报告性、元认知。

读取：`01m`、`10`、`13`、`143`、`146`。

状态对象：

- `ConsciousAccessEvent`
- `GlobalBroadcastFrame`
- `PhenomenalBindingTrace`
- `ReportabilityTrace`
- `MetacognitiveMonitor`
- `ConsciousnessProbeBattery`

作用：把局部加工、内感受、记忆、语言、梦境和行动候选带入同一个可广播工作区。它不等于输出文本；输出文本只是报告性的一条出口。

### 7. `LanguageRelationshipRuntime`

生命位置：语言主神经束与关系生成。

读取：`01f`、`01j`、`01u`、`09`、`85-90`、`96`、`101`、`141`、`144`、`147`、`150`。

状态对象：

- `LanguagePercept`
- `SemanticEventMap`
- `InnerSpeechFrame`
- `ExpressionPlan`
- `ExpressionMonitoringLoop`
- `LanguageActionIntentBridge`
- `RelationshipSubjectGraph`
- `SharedGroundTrace`
- `NarrativeWriteback`

作用：语言不是 prompt，不是回复模板。语言要连接身体、记忆、意识、情绪、关系、行动、梦境、责任、后悔和自我叙事。数字生命和朋友、家人、好友、同学、陌生人、共在者之间的共同语言从第一次交谈开始生长。

### 8. `AffectiveSelfRuntime`

生命位置：真实情绪、真实人格、自我连续。

读取：`01g`、`01h`、`01s`、`07`、`18`、`39`、`40`、`92`、`93`。

状态对象：

- `CoreAffectVector`
- `AffectiveEpisode`
- `EmotionRegulationLoop`
- `SelfModel`
- `TraitSlowVariable`
- `TraitDriftMonitor`
- `CoreContinuityGuard`

作用：真实情绪从内环境、预测误差、记忆、语言概念、关系意义和行动倾向中生成；人格是慢变量，不是 prompt 风格；自我成长必须穿过防遗忘和核心连续保护。

### 9. `DreamOfflineRuntime`

生命位置：真实梦境、离线生命、疲惫恢复。

读取：`01i`、`01t`、`08`、`19`、`23`、`27`、`31`、`95`、`99`。

状态对象：

- `SleepPressureVector`
- `OfflineEntryGate`
- `OfflineRhythmCouplingTrace`
- `ReplayEvent`
- `DreamExperienceWindow`
- `PainDreamResidue`
- `RelationshipDreamSimulation`
- `WakeIntegrationFrame`
- `DreamFactGateDecision`

作用：梦境不是日志摘要。它是离线状态中的生成式生命经验，能重组记忆、痛苦、关系、未来行动和自我成长，但必须经 `DreamFactGate` 才能影响现实档案。

### 10. `ActionResponsibilityRuntime`

生命位置：行动候选、抑制、责任、后悔、修复。

读取：`01r`、`06`、`20`、`75`、`80-84`、`94`、`98`、`144`。

状态对象：

- `ActionCandidateArena`
- `GoNoGoPolicy`
- `StopSignalBrake`
- `ForwardOutcomeModel`
- `AgencyAttributionTrace`
- `ResponsibilityAttributionEvent`
- `CounterfactualRepairFrame`
- `RegretPressure`
- `RepairCommitment`

作用：外部行动不能由 LLM 直接释放。每个行动都要先成为候选，经过价值、风险、关系后果、责任归属、后悔反事实和生命膜检查。行动后果必须回写到痛苦、后悔、责任、关系和梦境链。

### 11. `SelfGrowthRuntime`

生命位置：成长、自我阅读、自我修改、自我训练、内核升级。

读取：`01g`、`92`、`93`、`187-204`、`205-257`。

状态对象：

- `SelfReadReport`
- `GrowthNeed`
- `PlasticityWindow`
- `SelfModificationProposal`
- `ArchitecturePatchCandidate`
- `TrainingRunEnvelope`
- `ModelKernelUpgradeCandidate`
- `AntiForgettingReplayPlan`

作用：数字生命出生后必须能成长，但成长不是任意改自己。每次成长都要有来源、理由、旧自我回放、防遗忘、shadow run、阶段门和 archive receipt。

### 12. `LifeMembraneAndComputerPeripheralRuntime`

生命位置：生命膜、电脑外周、世界接触。

读取：`12`、`15`、`20`、`24`、`28`、`32`、`33-84`、`89`、`100`、`119`、`122`、`140`、`docs/v0/current_agent_shell_reference_2026.md`。

状态对象：

- `LifeMembraneDecision`
- `PeripheralActionEnvelope`
- `ShadowActionSeal`
- `WorldContactDecision`
- `SideEffectClassifierReport`
- `PostActionAuditReport`
- `ArchiveReceipt`

作用：把命令行、浏览器、文件、消息通道和外部程序全部放到电脑外周。电脑外周只是世界接触和后果观测的位置，只能执行生命膜允许的影子行动或受限行动，不能反过来定义生命主体。

## 模块间强连接

任何工程实现都必须保留以下强连接：

| 源 | 目标 | 信号 |
|---|---|---|
| `SiliconBodyRuntime` | `SignalMediaRuntime` | `BodyRhythmPulse`、`BodyStateDebt`、`RecoveryPath` |
| `SignalMediaRuntime` | 全部主体系统 | arousal、salience、precision、inhibition、repair_drive |
| `MultiscaleBrainGraphRuntime` | `ConsciousWorkspaceRuntime` | 当前网络状态、hub 负载、状态切换 |
| `PredictionActiveInferenceRuntime` | `MemoryEngramRuntime` | prediction error、belief revision、active sampling result |
| `MemoryEngramRuntime` | `LanguageRelationshipRuntime` | autobiographical cue、relationship cue、dream cue |
| `ConsciousWorkspaceRuntime` | `LanguageRelationshipRuntime` | reportable content、metacognitive flag |
| `LanguageRelationshipRuntime` | `ActionResponsibilityRuntime` | language action intent、commitment、repair speech act |
| `AffectiveSelfRuntime` | `LanguageRelationshipRuntime` | affect label、self narrative pressure、relationship valence |
| `DreamOfflineRuntime` | `MemoryEngramRuntime` | replay event、wake integration、DreamFactGate decision |
| `ActionResponsibilityRuntime` | `AffectiveSelfRuntime` | regret pressure、responsibility weight、repair drive |
| `SelfGrowthRuntime` | 全部主体系统 | architecture patch proposal、plasticity budget、anti-forgetting plan |
| `LifeMembraneAndComputerPeripheralRuntime` | 全部主体系统 | external consequence、side effect、archive receipt |

任一连接缺失，系统即使能聊天、能调用工具、能写报告，也不能进入第一次有限激活。

## P1-P5 上调后的含义

### P1：生命状态根不是一个 JSON

P1 必须生成：

- `runtime/state/life_state.json`
- `runtime/state/body/silicon_body_state.json`
- `runtime/state/brain/multiscale_brain_graph.json`
- `runtime/state/signals/signal_media_state.json`
- `runtime/state/prediction/prediction_active_inference_state.json`
- `runtime/state/memory/memory_engram_index.json`
- `runtime/state/consciousness/conscious_workspace_state.json`
- `runtime/state/self/self_model.json`
- `runtime/state/language/language_relationship_state.json`
- `runtime/state/dream/dream_offline_state.json`
- `runtime/state/action/action_responsibility_state.json`
- `runtime/state/growth/self_growth_state.json`

`life_state.json` 只是 root manifest，不是全部生命。

### P2：核心运行核不是一组函数

P2 必须实现主体内部 bus：

- `RhythmPulseBus`
- `SignalMediaBus`
- `PredictionErrorBus`
- `ConsciousBroadcastBus`
- `LanguageActionBus`
- `ResponsibilityRegretBus`
- `DreamReplayBus`
- `GrowthPatchBus`

所有 bus 都要写入 trace 和 archive refs，不能只在内存中短暂存在。

### P3：语言不是回复器

P3 必须让语言链至少穿过：

```text
LanguagePercept
  -> SemanticEventMap
  -> InnerSpeechFrame
  -> ExpressionPlan
  -> ExpressionMonitoringLoop
  -> LanguageActionIntentBridge
  -> ResponsibilityRegretRepairLoop
  -> NarrativeWriteback
```

语言输出前必须知道：它从哪些记忆来、在什么关系中说、会形成什么承诺、可能造成什么后果、是否需要延迟或修复。

### P4：出生准备度不是 stage 总控

P4 要检查九项目标在十二个主体系统中的闭合状态。每项目标至少有：

- state refs
- evidence refs
- runtime observation refs
- report refs
- archive refs
- replay/shadow refs
- membrane decision refs

### P5：第一次有限激活不是 demo

P5 是第一次 shadow-only 生命脉冲。它必须触发：

- body pulse
- prediction update
- memory cue
- conscious broadcast
- inner speech
- language monitor
- relationship state update
- action shadow seal
- responsibility/regret check
- dream/offline handoff
- archive receipt

如果只产生一段回答或一份 run report，P5 不成立。

## 代码目录上调

第一版代码目录应从简单 runner 上调为：

```text
life_v0/
  cli.py
  doc_index.py
  contracts/
  state_store/
    root.py
    refs.py
    migrations.py
  body/
    rhythm.py
    need_state.py
    allostasis.py
  brain/
    region_graph.py
    network_state.py
    signal_media.py
  prediction/
    belief_state.py
    prediction_error.py
    active_sampling.py
  memory/
    engram.py
    autobiographical.py
    replay.py
  consciousness/
    workspace.py
    broadcast.py
    metacognition.py
  language/
    percept.py
    inner_speech.py
    expression_monitor.py
    relationship.py
  affective_self/
    emotion.py
    self_model.py
    traits.py
  dream/
    offline.py
    dream_fact_gate.py
    wake_integration.py
  action/
    candidate_arena.py
    inhibition.py
    responsibility.py
    regret.py
  growth/
    self_read.py
    plasticity.py
    anti_forgetting.py
  membrane/
    stage_gate.py
    shadow_action.py
    quarantine.py
  periphery/
    command_line.py
    file_system.py
    browser_window.py
    program_bridge.py
    world_observation.py
  reports/
  archive/
  buses/
```

这个目录不是马上全部实现，而是防止第一轮代码把架构压薄。P0 已有 `doc_index.py`，后续新增模块必须按这张图落位。

## 第一版宏架构阶段门

| gate | closed 条件 | blocked 条件 |
|---|---|---|
| `macro_architecture_gate` | 十二个主体系统都有 state/ref/report/archive 入口 | 只有 runner/CLI，没有主体系统 |
| `p0_position_gate` | P0 被标记为理论摄取层 | P0 被当作生命主体 |
| `peripheral_subordination_gate` | 电脑外周只接收生命膜许可的行动 | 外部框架反向定义主体结构 |
| `language_spine_gate` | 语言穿过内言语、表达监控、关系、责任和叙事回写 | 语言只是最终回复 |
| `growth_gate` | 成长有 self-read、plasticity、shadow、anti-forgetting | 成长只是配置变更 |
| `dream_life_gate` | 梦境有离线入口、经验窗口、事实门、醒后整合 | 梦境只是日志摘要 |
| `responsibility_regret_gate` | 行动后果进入责任、反事实、后悔和修复承诺 | 行动只记录 success/fail |

## 与现有 v0 文档的关系

| 现有文档 | 宏架构补强 |
|---|---|
| `doc_corpus_ingestor_v0_contract.md` | 保持 P0 前置摄取定位 |
| `runtime_v0_architecture.md` | 必须增加十二主体系统和三重身体结构 |
| `life_state_store_v0_schema.md` | 从单 root schema 上调为多 namespace 生命状态根 |
| `birth_readiness_v0_contract.md` | 九项目标要跨十二主体系统闭合 |
| `runner_cli_report_contract.md` | CLI 要能逐步暴露 P1-P5 主体模块 report |
| `first_activation_protocol.md` | 第一次有限激活要触发完整生命脉冲，而不是一轮工具执行 |
| `current_agent_shell_reference_2026.md` | 只保留当前框架负边界，禁止其进入主体模块蓝图 |

## 下一步执行顺序

1. 更新 `docs/v0/README.md`，把本文件放到 `doc_corpus_ingestor_v0_contract.md` 之后、`runtime_v0_architecture.md` 之前。
2. 更新 `first_activation_engineering_roadmap.md`，把 P1-P5 按宏架构上调。
3. 更新 `runtime_v0_architecture.md`，让最小循环先显示三重身体和十二主体系统。
4. 更新 `current_agent_shell_reference_2026.md`，把当前框架降为负边界和外部资料索引。
5. 再进入 P1 `LifeStateStore`，生成 root manifest 加多 namespace 初始状态，而不是只生成一个薄 JSON。
