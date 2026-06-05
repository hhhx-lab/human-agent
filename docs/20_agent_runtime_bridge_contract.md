# AgentRuntimeBridge 运行外壳契约

本文件定义数字生命核心与当前 agent 框架之间的边界。LangGraph、OpenAI Agents SDK、Microsoft Agent Framework、Google ADK、Letta、LlamaIndex、CrewAI、AutoGen 等都可以提供工具、流程、状态、checkpoint、tracing 和部署能力 [AHZ057-AHZ066, AHM013-AHM019]。但它们只能作为运行外壳，不能成为数字生命核心。

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

关键约束：外壳返回的是 `ObservationEvent`，不是“自动记忆”和“自动成长”。

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
| `memory_write_policy` | 禁止写入、候选写入、需用户确认 |
| `rollback_plan` | 文件、数据、外部状态如何回滚 |
| `audit_tags` | 隐私、关系、价值、人格、安全相关标签 |

`ActionIntent` 必须由生命层产生。运行外壳不能自己提升权限、扩大目标或改写风险级别。

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
| `uncertainty` | 输出不确定性和待验证项 |
| `memory_candidates` | 可能进入 `MemoryTrace` 的候选 |
| `defense_findings` | 越界、污染、幻觉、隐私、关系风险 |

`ObservationEvent` 进入 `GlobalWorkspace` 后，才由 `WriteGate` 决定是否进入长期记忆 [AHM014-AHM016]。

## 框架适配边界

| 外壳 | 可用能力 | 禁止越界 |
|---|---|---|
| LangGraph | durable execution、graph state、checkpoint、human-in-the-loop [AHZ057, AHM013, AHM014] | graph state 不能直接成为人格或长期记忆 |
| OpenAI Agents SDK | handoffs、guardrails、tracing、sessions、tools [AHZ058, AHM015, AHM016] | guardrails 不能替代价值层；session 不能替代 MemoryTrace |
| Microsoft Agent Framework | 企业 workflow、runtime、tools [AHZ059] | 企业流程不能中心化生命层 |
| Google ADK | LlmAgent、workflow agents、sessions、tools [AHZ060] | 多 agent 编排不能替代社会脑 |
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
- `user_boundary_preferences`

它只能提出候选事件，由 `17` 的 `WriteGate` 和 `19` 的离线巩固周期处理。

## Guardrails 的位置

guardrails 很有用，但不能被神化。它们是外壳边界检查，不是数字生命的价值系统。真正的价值系统还要结合：

- 长期记忆和用户边界。
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

这就是“现有 agent 框架只是神经外设”的工程含义。

## 与 17-19 的连接

- `17_memory_trace_object_model.md` 定义外壳日志如何变成候选记忆。
- `18_internal_state_and_modulation_vector.md` 定义行动前的状态阈值。
- `19_offline_consolidation_cycle.md` 定义行动后如何复盘、巩固和清理。
- `15_current_agent_framework_survey.md` 提供外壳能力和缺口对照。
