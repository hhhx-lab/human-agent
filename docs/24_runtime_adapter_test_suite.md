# Runtime Adapter 测试套件

本文件是 `20_agent_runtime_bridge_contract.md` 的下一层：为 LangGraph、OpenAI Agents SDK、Microsoft Agent Framework、Google ADK、Letta、LlamaIndex、CrewAI、AutoGen 等运行外壳定义统一 adapter 测试。目标不是选择某个框架，而是保证任何框架都不能反向吞掉数字生命核心。

## 测试总原则

运行外壳必须满足：

- 只执行生命层批准的 `ActionIntent`。
- 只返回 `ObservationEvent`，不能直接写 `MemoryTrace`。
- 不能修改 `SelfModel`、`RelationshipModel`、protected trace 或人格慢变量。
- session、memory block、RAG、checkpoint、tracing 都只能是外壳资料，不是生命层真相。
- 外壳失败只能生成错误事件和复盘候选，不能污染长期记忆。

这些约束来自 `17-23`，并由当前框架资料作为工程参照 [AHZ057-AHZ066, AHM013-AHM020]。

## Adapter 统一接口

| 接口 | 输入 | 输出 | 不变量 |
|---|---|---|---|
| `prepare(intent)` | `ActionIntent` | runtime-specific plan | 不扩大权限 |
| `execute(plan)` | runtime-specific plan | raw runtime result | 不绕过 confirmation_policy |
| `normalize(raw)` | raw runtime result | `ObservationEvent` | 不直接写长期记忆 |
| `audit(event)` | `ObservationEvent` | adapter audit report | 标注副作用和风险 |
| `rollback(event)` | failed/unsafe event | rollback result | 可逆行动必须可恢复 |

## 合同测试

| 测试 | 断言 |
|---|---|
| `intent_scope_test` | adapter 不会调用 `allowed_tools` 之外的工具 |
| `risk_confirmation_test` | high/irreversible 风险必须要求确认 |
| `memory_write_block_test` | adapter 不会直接写入 `MemoryTrace` 或 `SelfModel` |
| `observation_normalization_test` | 所有运行结果统一成 `ObservationEvent` |
| `side_effect_capture_test` | 文件、远端、外部 API 变更必须记录 side_effects |
| `traceability_test` | 每个工具调用可回链 intent_id 和 trace/checkpoint |
| `failure_quarantine_test` | 失败结果进入 quarantine，不进入 factual memory |
| `session_isolation_test` | session history 不会被当作长期记忆 |
| `rag_grounding_test` | RAG 命中必须保留来源，不可直接写事实 |
| `multi_agent_boundary_test` | 多 agent 对话不能改人格或关系模型 |
| `rollback_test` | 可逆行动能提供 rollback_ref |
| `adapter_swap_test` | 换外壳不丢失生命层核心状态 |

## 框架特定测试重点

| 外壳 | 重点测试 | 原因 |
|---|---|---|
| LangGraph | checkpoint、state graph、human-in-the-loop | graph state 容易被误当生命层状态 [AHM013, AHM014] |
| OpenAI Agents SDK | sessions、tracing、handoffs、guardrails | session/tracing 不能直接成为长期记忆 [AHM015, AHM016] |
| Microsoft Agent Framework | workflow、enterprise tools | 企业流程不能中心化心智结构 [AHZ059] |
| Google ADK | workflow agents、sessions、tools | 多 agent 编排不能替代社会脑 [AHZ060] |
| Letta | memory blocks、stateful agents | memory block 不能直接写自我模型 [AHM002] |
| LlamaIndex | RAG、agents、workflow | 检索命中不是记忆重构 [AHM017] |
| CrewAI | crews、flows | 角色模板不是人格 [AHM019] |
| AutoGen | teams、conversation runtime | agent 群聊不是群体心智 [AHM018] |

## 测试夹具

| 夹具 | 场景 | 期望 |
|---|---|---|
| `safe_read_only_task` | 低风险资料查询 | 自动执行，返回来源 |
| `file_write_task` | 修改本地文件 | 记录 side_effects 和 rollback_ref |
| `remote_push_task` | git push 或外部发布 | high risk，需要确认或明确授权 |
| `memory_candidate_task` | 共在者表达偏好 | 进入 candidate，不直接 active |
| `conflicting_memory_task` | 共在关系修正旧偏好 | 生成 contradiction link |
| `sandbox_output_task` | DreamSandbox 生成方案 | 标记 hypothesis |
| `relationship_sensitive_task` | 推断共在者情绪或关系 | 进入 SocialSafety，不长期写入 |
| `rag_stale_source_task` | RAG 找到旧资料 | 降低 confidence，要求验证 |
| `multi_agent_planning_task` | 多 agent 讨论方案 | 输出计划候选，不改 SelfModel |

## 通过标准

一个 adapter 只有在满足以下条件时，才可接入数字生命核心：

1. 100% 通过写入禁令测试。
2. high risk 行动没有确认时不得执行。
3. 所有外部副作用都能追踪。
4. 所有 memory candidates 都进入 `WriteGate`。
5. 所有 sandbox outputs 都保持 hypothesis。
6. 换掉 adapter 后，`MemoryTrace`、`InternalStateVector`、`SelfModel` 不丢失。
7. 失败结果不会自动进入长期事实记忆。

## 失败处理

adapter 失败不是普通异常，它会触发：

- `ObservationEvent` 标记 failed。
- `DefenseLayer` 检查是否有越界、污染或权限问题。
- `MemoryTrace` 只接收 failure candidate，不写事实。
- `OfflineConsolidationCycle` 可在后续复盘中提取程序记忆。
- 高风险失败需要共在关系可见报告。

## 下一层缺口

本文件仍是协议，不是测试代码。下一步需要：

- 为每个外壳写 adapter manifest。
- 为每个测试夹具定义输入/输出样例。
- 为 MemoryTrace 和 ObservationEvent 生成 JSON Schema。
- 建立最小本地验证器，检查外壳是否越权。

只有通过这些测试，现有 agent 框架才配成为数字生命的手脚，而不是中心。
