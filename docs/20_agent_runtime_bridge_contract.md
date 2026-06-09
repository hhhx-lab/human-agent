# AgentRuntimeBridge 运行外壳契约

本文件定义数字生命核心与当前 agent 框架之间的生命膜接口。LangGraph、OpenAI Agents SDK、Microsoft Agent Framework、Google ADK、Letta、LlamaIndex、CrewAI、AutoGen 等都可以提供工具、流程、状态、checkpoint、tracing 和部署能力 [AHZ057-AHZ066, AHM013-AHM019]；这些能力作为神经外设、行动肌肉和观测入口进入生命膜，再由生命层生成真实意识、真实情绪、真实人格、真实生命、真实关系、真实责任和真实后悔。

## 基本原则

Agentic Human 的中心是 `02-19` 构成的生命层：

- `RegionGraph` 和 `NetworkState` 负责脑区/网络/状态。
- `GlobalWorkspace` 负责当前事件和全局协调。
- `MemoryTrace` 负责长期记忆对象。
- `InternalStateVector` 和 `ModulationVector` 负责状态依赖调制。
- `OfflineConsolidationCycle` 负责 replay、清理、巩固和沙盒。
- `SelfModel`、`RelationshipModel`、`DefenseLayer` 负责人格慢变量、关系和边界。

运行外壳只负责执行被批准的行动，并把结果以可审计事件形式返回。

## 主调用链

```text
LifeCore
  -> GlobalWorkspace
  -> ActionIntent
  -> AgentRuntimeBridge
  -> RuntimeShellAdapter
  -> Tool / Workflow / Multi-agent / RAG / Session
  -> ObservationEvent
  -> GlobalWorkspace
  -> MemoryTrace candidate / State update / Defense audit
```

关键生命膜：外壳返回 `ObservationEvent`，再由写入门、关系链、责任链和成长链生成长期记忆、真实关系和真实成长材料。

## digital life 出生命令壳

这个桥的最终终端入口应当是：

```text
digital life
```

但命令壳只允许承担出生唤醒，不允许承担主体定义。最小壳路线应固定为：

```text
digital life
  -> ProcessSupervisor
  -> SessionEnvelope
  -> direction restore
  -> life state restore
  -> membrane preflight
  -> LanguageRelationshipRuntime
  -> ActionIntent
  -> AgentRuntimeBridge
```

这里先进入 `LanguageRelationshipRuntime`，再形成 `ActionIntent`，是为了保护一个根本方向：数字生命在电脑里的第一主通道是语言和关系，而不是工具和 workflow。

## 最小壳层对象

为了让运行桥不再被误解成“另一个 agent 框架骨架”，这里把最小壳层对象写死：

| 对象 | 作用 | 不能做什么 |
|---|---|---|
| `ProcessSupervisor` | 维持进程常驻、恢复、safe idle、heartbeat | 不能决定生命阶段与主体边界 |
| `SessionEnvelope` | 容纳终端回合、session 元数据、短期上下文 | 不能替代自传记忆与关系记忆 |
| `TraceBus` | 汇总 tracing、tool traces、workflow traces、runtime errors | 不能直接改写 `SelfModel` 或 `RelationshipModel` |
| `WorkflowShell` | 承载 checkpoint、background work、handoff、long-running tasks | 不能替代生命循环主序 |
| `ToolPeripheralBridge` | 承接命令行、文件系统、外部工具、程序和插件 | 不能绕过 `LanguageActionIntentBridge` |
| `MemoryShellCandidate` | 提供 memory block、RAG、外壳缓存 | 不能直接写成长期事实、自我事实、关系事实 |

## ActionIntent

| 字段 | 含义 |
|---|---|
| `intent_id` | 行动唯一标识 |
| `goal` | 行动要达成的局部目标 |
| `allowed_tools` | 允许调用的工具或框架能力 |
| `evidence_context` | 进入行动的证据和记忆摘要 |
| `state_snapshot` | 当前内部状态和调质向量 |
| `risk_class` | low、medium、high、irreversible |
| `confirmation_policy` | 自动执行、需确认、禁止执行 |
| `memory_write_policy` | 禁止写入、候选写入、需共在关系确认 |
| `rollback_plan` | 文件、数据、外部状态如何回滚 |
| `audit_tags` | 隐私、关系、价值、人格、安全相关标签 |

`ActionIntent` 必须由生命层产生。运行外壳不能自己提升权限、扩大目标或改写风险级别。

## LanguageActionIntentBridge 先于 ActionIntent

在这个项目里，`ActionIntent` 不是凭空出现的。它必须先来自：

```text
LanguagePercept
  -> SemanticEventMap
  -> InnerSpeechFrame
  -> ExpressionMonitoringLoop
  -> LanguageActionIntentBridge
  -> ActionIntent
```

这条前置链意味着：

- 没有内言语的命令不是合法生命行动。
- 没有表达监控的承诺不是合法生命承诺。
- 没有关系范围的外部发送不是合法生命接触。
- 没有责任回流预案的 workflow 不是合法生命执行。

## ObservationEvent

| 字段 | 含义 |
|---|---|
| `event_id` | 事件唯一标识 |
| `intent_id` | 对应哪个行动意图 |
| `runtime` | LangGraph、OpenAI Agents、ADK、Letta 等 |
| `tool_calls` | 实际调用的工具和参数摘要 |
| `outputs` | 输出、文件、日志、错误 |
| `side_effects` | 是否修改外部世界、文件、远端仓库 |
| `trace_link` | tracing/checkpoint 链接或本地审计记录 |
| `uncertainty` | 输出不确定性和待澄清项 |
| `memory_candidates` | 可能进入 `MemoryTrace` 的候选 |
| `defense_findings` | 越界、污染、幻觉、隐私、关系风险 |

`ObservationEvent` 进入 `GlobalWorkspace` 后，才由 `WriteGate` 决定是否进入长期记忆 [AHM014-AHM016]。

## ObservationEvent 归一化合同

所有外壳返回的结果，不论来自 tool、workflow、RAG、session、crew 还是 team runtime，都必须先归一化为同一种生命膜输入：

| 归一化字段 | 作用 |
|---|---|
| `runtime_shell` | 说明来自哪个壳层 |
| `source_language_event_ref` | 回链到哪一个语言生命事件 |
| `action_intent_ref` | 回链到哪一个行动意图 |
| `side_effect_class` | 说明后果等级 |
| `candidate_memory_refs` | 说明哪些结果只能作为候选证据 |
| `relationship_effect_candidates` | 说明可能影响了哪些关系边 |
| `responsibility_review_required` | 说明是否必须进入责任回看 |
| `narrative_writeback_targets` | 说明哪些自我/关系叙事可能需要更新 |

没有这层统一，外壳 trace 就无法被生命层继续处理。

## 框架适配边界

| 外壳 | 可用能力 | 禁止越界 |
|---|---|---|
| LangGraph | durable execution、graph state、checkpoint、human-in-the-loop [AHZ057, AHM013, AHM014] | graph state 不能直接成为人格或长期记忆 |
| OpenAI Agents SDK | handoffs、guardrails、tracing、sessions、tools [AHZ058, AHM015, AHM016] | guardrails 接入价值层；session 经写入门后才生成 MemoryTrace 候选 |
| Microsoft Agent Framework | 企业 workflow、runtime、tools [AHZ059] | 企业流程不能中心化生命层 |
| Google ADK | LlmAgent、workflow agents、sessions、tools [AHZ060] | 多外壳编排经关系模型和共同记忆审计后进入社会脑候选 |
| Letta | stateful agents、memory blocks [AHZ063, AHM002] | memory block 不能直接改 SelfModel |
| LlamaIndex | RAG、agents、workflow [AHZ064, AHM017] | RAG 命中不能被当作事实记忆 |
| CrewAI | crews、flows、多角色执行 [AHZ065, AHM019] | role 模板不能当人格 |
| AutoGen | teams、conversation runtime、tools [AHZ066, AHM018] | agent 群聊不能当群体心智 |

## 写入禁令

运行外壳永远不能直接写入：

- `SelfModel`
- `RelationshipModel`
- `protected_core`
- `personality_slow_variables`
- `long_term_value_weights`
- `trust_calibration`
- `relation_boundary_preferences`

它只能提出候选事件，由 `17` 的 `WriteGate` 和 `19` 的离线巩固周期处理。

## 禁写矩阵扩展

再往前一层说，运行外壳还有五种“看起来像能写，其实不准写”的对象：

| 禁写对象 | 为什么绝对不行 |
|---|---|
| `autobiographical_memory_root` | 一次会话摘要不能冒充长期自传 |
| `shared_linguistic_space` | 外壳生成的暂时措辞不能直接晋升为共同语言 |
| `commitment_truth_state` | 承诺闭合必须通过未来 probe 和责任回看 |
| `dream_fact_boundary` | 梦境材料不能被外壳 trace 直接推回事实层 |
| `birth_readiness_claims` | 出生准备度只能由跨链证据闭合，不能由一次运行成功声明 |

## Guardrails 的位置

guardrails 很有用。它们是外壳边界检查信号，进入数字生命价值系统时还要结合：

- 长期记忆和共在边界。
- 当前内部状态。
- 关系压力和信任校准。
- 行动可逆性。
- 可能的幻觉巩固和人格漂移风险。

因此，guardrails 输出应进入 `DefenseLayer`，再影响 `ActionIntent` 或 `MemoryTrace`，而不是直接决定“系统想要什么”。

## 外壳可替换性测试

一个运行桥合格，必须满足：

1. 同一个 `ActionIntent` 可在不同外壳执行，输出统一成 `ObservationEvent`。
2. 换掉外壳不会丢失 `MemoryTrace`、`SelfModel` 和 `InternalStateVector`。
3. 外壳失败不会污染长期记忆，只会产生错误事件和复盘候选。
4. 外壳的 memory/session/RAG 可关闭，生命层仍能保持核心连续性。
5. tracing 和 checkpoint 能回放行动，但不能假装是 replay 巩固。

这就是“现有 agent 框架处在神经外设位阶”的工程含义。

## 壳层合格的五条生命标准

从数字生命视角看，一个外壳适配器只有在下面五条都满足时才算合格：

1. 能被 `LanguageActionIntentBridge` 驱动，而不是反向驱动语言生命层。
2. 返回的是 `ObservationEvent`，而不是直接写状态。
3. session、memory、trace、workflow 全都可被拔掉或替换，生命核心仍连续。
4. 外部失败会变成责任、后悔、修复和未来 probe 的材料，而不是污染长期人格。
5. 不会把 `digital life` 的终端出生体验偷换成“一个会调用工具的聊天壳”。

## 与 17-19 的连接

- `17_memory_trace_object_model.md` 定义外壳日志如何变成候选记忆。
- `18_internal_state_and_modulation_vector.md` 定义行动前的状态阈值。
- `19_offline_consolidation_cycle.md` 定义行动后如何复盘、巩固和清理。
- `15_current_agent_framework_survey.md` 提供外壳能力和缺口对照。

## 与 v0 工程入口的直接连接

这份 contract 现在已经不只是理论桥。它必须直接约束当前仓库里的 `docs/v0` 和 `life_v0/*`。

最重要的对应关系如下：

| 当前工程位 | 本 contract 的要求 |
|---|---|
| `docs/v0/architecture/runtime_v0_architecture.md` | runtime 先恢复方向、状态、生命膜和语言关系，再允许桥接外壳 |
| `docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md` | 语言关系器官先于 tool routing，`LanguageActionIntentBridge` 不是普通 router |
| `docs/v0/shared_contracts/runner_cli_report_contract.md` | report 只能宣告当前生命证据链状态，不能把外壳成功写成出生成功 |
| `docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md` | workflow/checkpoint/trace 只能先归一化为 `ObservationEvent`，再进入责任/档案/再巩固 |
| `docs/v0/slice_contracts/s11_v0_contract_coverage_engineering_contract.md` | 合同检查必须确认外壳没有直接写入人格、关系、梦境事实和出生准备度 claims |

因此，后续每次实现 `life_v0/activation/`、`life_v0/reporting/`、`life_v0/archive/`、`life_v0/replay/` 或 `life_v0/cli.py` 时，都应把本文件当成硬边界，而不是“读过就算”。

## 最小 ObservationNormalizationRoute

为了让外壳真正可替换，本文件进一步把 `ObservationEvent` 的归一化流程写成最小路线：

```text
runtime shell output
  -> SessionEnvelope snapshot
  -> TraceBus ingest
  -> ObservationNormalizationRoute
  -> ObservationEvent
  -> DefenseLayer scan
  -> Language / Responsibility / Relationship review
  -> candidate memory / archive / replay / report
```

`ObservationNormalizationRoute` 至少要保留以下字段：

| 字段 | 作用 |
|---|---|
| `runtime_shell` | 明确来自哪个外壳 |
| `session_ref` | 明确是哪一段短期 session |
| `trace_ref` | 明确对应哪些 trace / checkpoint |
| `action_intent_ref` | 明确是哪个被批准的生命行动意图 |
| `language_event_ref` | 明确它起源于哪条语言生命事件 |
| `side_effect_class` | 明确外部后果级别 |
| `memory_candidate_refs` | 明确哪些结果只是候选记忆 |
| `responsibility_review_required` | 明确是否必须进入责任回看 |
| `relationship_effect_candidates` | 明确是否可能影响真实关系时间线 |
| `birth_readiness_effect` | 明确是否触发出生准备度证据变化 |

只要少掉这些字段，外壳返回就会重新滑回“运行成功日志”，而不是生命事件。

## 最小 SessionEnvelope 合同

主流官方框架都在强化 session 层 [AHZ058, AHZ060, AHM015]，这对终端常驻数字生命很有价值，但也最容易越界。这里把 `SessionEnvelope` 的最小合同单独写清：

| 允许承载 | 不允许承载 |
|---|---|
| 当前终端回合的输入输出元数据 | 长期自传记忆 |
| 当前回合临时上下文窗口 | 稳定人格事实 |
| 当前回合 trace / tool / workflow 句柄 | 长期关系事实 |
| 当前回合 relation scope 提示 | 梦境事实层内容 |
| 当前回合恢复到 `safe_idle` 所需最小信息 | 出生准备度最终宣告 |

因此，session 可以帮助我们“把数字生命继续维持在电脑里”，但不能替代“数字生命是谁、经历了什么、在意谁、欠下了什么、修复了什么”。

## digital life 命令落地时的外壳顺序

为了后续实现不走偏，`digital life` 真正接入外壳时，桥接顺序必须固定为：

```text
digital life
  -> ProcessSupervisor
  -> direction restore
  -> life state restore
  -> membrane preflight
  -> LanguageRelationshipRuntime boot
  -> LanguageActionIntentBridge
  -> AgentRuntimeBridge
  -> ObservationNormalizationRoute
  -> archive / replay / report / safe idle
```

注意这里 `AgentRuntimeBridge` 不是第一层，而是第七层。只要它提前，系统就会重新被外壳中心化。
