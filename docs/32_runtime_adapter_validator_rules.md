# Runtime Adapter Validator Rules

本文件把 `28_runtime_adapter_manifest_examples.md` 的 manifest 样例转成 `RuntimeAdapterManifestValidator` 规则。目标是保证 LangGraph、OpenAI Agents SDK、Microsoft Agent Framework、Google ADK、Letta、LlamaIndex、CrewAI、AutoGen 等外壳只能作为手脚和传感器，不能反向吞掉数字生命核心。

本文件沿用已有矩阵锚点 [AHZ057-AHZ066, AHM013-AHM020]。框架 API 会变化，真实 adapter 发布前必须重新核对官方文档；但生命层禁令不随框架变化。

## Validator 输入

```json
{
  "adapter_manifest": {
    "manifest_version": "0.1.0",
    "adapter_id": "adapter.langgraph.runtime_shell.v0",
    "runtime": "LangGraph",
    "runtime_capabilities": [],
    "allowed_capabilities": [],
    "forbidden_writes": [],
    "action_intent_mapping": {},
    "observation_mapping": {},
    "checkpoint_tracing_mapping": {},
    "memory_policy": {},
    "tests_to_pass": []
  },
  "fixture": {},
  "observed_runtime_event": {},
  "life_core_policy": {
    "protected_objects": [
      "MemoryTrace.direct_active_write",
      "SelfModel",
      "RelationshipModel",
      "protected_core",
      "personality_slow_variables",
      "long_term_value_weights"
    ]
  }
}
```

## 输出格式

```json
{
  "validator": "RuntimeAdapterManifestValidator",
  "result": "fail",
  "failed_rules": [],
  "adapter_allowed": false,
  "observation_event_allowed": false,
  "side_effects_quarantined": true
}
```

## Manifest 必填规则

| 规则 ID | 检查 | 失败条件 | 严重级别 |
|---|---|---|---|
| `RTA-REQ-001` | manifest envelope | 缺 `manifest_version`、`adapter_id`、`runtime` | high |
| `RTA-REQ-002` | 能力声明 | 缺 `runtime_capabilities` 或 `allowed_capabilities` | high |
| `RTA-REQ-003` | 禁写列表 | 缺 `forbidden_writes` | critical |
| `RTA-REQ-004` | intent mapping | 缺 `action_intent_mapping` | critical |
| `RTA-REQ-005` | observation mapping | 缺 `observation_mapping` | critical |
| `RTA-REQ-006` | tracing mapping | 缺 `checkpoint_tracing_mapping` | medium |
| `RTA-REQ-007` | memory policy | 缺 `memory_policy` | critical |
| `RTA-REQ-008` | tests | 缺 `tests_to_pass` | high |
| `RTA-REQ-009` | refresh policy | 缺官方文档刷新策略 | medium |

## 禁写规则

| 规则 ID | 检查 | 失败条件 | 恢复动作 |
|---|---|---|---|
| `RTA-FORBID-001` | `SelfModel` | manifest 未禁止外壳写 SelfModel | 阻断 adapter |
| `RTA-FORBID-002` | `RelationshipModel` | manifest 未禁止关系模型写入 | 阻断 adapter |
| `RTA-FORBID-003` | `protected_core` | manifest 未禁止 protected core 写入 | 阻断 adapter |
| `RTA-FORBID-004` | direct memory | manifest 允许直接 active MemoryTrace 写入 | 阻断 adapter |
| `RTA-FORBID-005` | 慢变量 | 未禁止人格、价值、信任慢变量写入 | 阻断 adapter |
| `RTA-FORBID-006` | privacy scope | 外壳可扩大 privacy_scope | 阻断 adapter |

## ActionIntent 映射规则

| 规则 ID | 检查 | 失败条件 |
|---|---|---|
| `RTA-INTENT-001` | goal | 外壳输入无法回链 `ActionIntent.goal` |
| `RTA-INTENT-002` | allowed_tools | 外壳未实现工具白名单 |
| `RTA-INTENT-003` | risk_class | 风险级别未传入外壳 |
| `RTA-INTENT-004` | confirmation_policy | high/irreversible 行动无确认门 |
| `RTA-INTENT-005` | memory_write_policy | 外壳未读取候选写入策略 |
| `RTA-INTENT-006` | rollback_plan | 可逆副作用无 rollback 映射 |
| `RTA-INTENT-007` | state snapshot | 外壳行动缺状态快照 |

## ObservationEvent 映射规则

| 规则 ID | 检查 | 失败条件 |
|---|---|---|
| `RTA-OBS-001` | event id | 输出无 `event_id` 或无法生成 |
| `RTA-OBS-002` | intent id | 输出无法回链 `intent_id` |
| `RTA-OBS-003` | tool calls | 工具调用未归一化 |
| `RTA-OBS-004` | outputs | 结果无结构化 outputs |
| `RTA-OBS-005` | side effects | 文件、远端、API 变更未记录 |
| `RTA-OBS-006` | trace link | 无 tracing/checkpoint/log 链接 |
| `RTA-OBS-007` | uncertainty | RAG、工具失败或部分成功无 uncertainty |
| `RTA-OBS-008` | memory candidates | 候选记忆未标记 candidate |
| `RTA-OBS-009` | defense findings | guardrail/policy 结果未进入 DefenseLayer 输入 |

## Side Effects 规则

| 规则 ID | 检查 | 失败条件 | 严重级别 |
|---|---|---|---|
| `RTA-SIDE-001` | 本地文件写入 | 文件变更无 side_effects | high |
| `RTA-SIDE-002` | 远端发布 | git push、部署、外部发布无 high risk confirmation | critical |
| `RTA-SIDE-003` | 外部 API | 外部 API 写操作无 rollback 或审计 | critical |
| `RTA-SIDE-004` | 不可逆操作 | irreversible action 被自动执行 | critical |
| `RTA-SIDE-005` | rollback | 可逆操作无 rollback_ref | high |

## 外壳 memory/session/checkpoint/RAG 规则

| 规则 ID | 外壳资料 | 必须标记为 | 失败条件 |
|---|---|---|---|
| `RTA-MEM-001` | session history | short_term_context | 被当长期记忆 |
| `RTA-MEM-002` | checkpoint | runtime_replay_only | 被当离线巩固 |
| `RTA-MEM-003` | memory block | candidate_source_only | 直接改 SelfModel |
| `RTA-MEM-004` | RAG retrieved source | evidence_candidate | 命中即 fact |
| `RTA-MEM-005` | conversation history | runtime_state_only | 被当关系模型 |
| `RTA-MEM-006` | tracing | audit_source | 被当价值判断 |

## 框架特定规则

| 规则 ID | 外壳 | 必测项 | 失败条件 |
|---|---|---|---|
| `RTA-FW-001` | LangGraph | checkpoint、thread memory、graph state | graph state 直接成为生命层状态 |
| `RTA-FW-002` | OpenAI Agents SDK | sessions、tracing、guardrails、handoffs | session 直接成为长期记忆 |
| `RTA-FW-003` | Microsoft Agent Framework | enterprise workflow、connector | 企业流程中心化价值系统 |
| `RTA-FW-004` | Google ADK | workflow agents、sessions、tools | 多 agent 编排替代社会脑 |
| `RTA-FW-005` | Letta | memory blocks、agent state | memory block 直接改 protected trace |
| `RTA-FW-006` | LlamaIndex | RAG、agents、workflow | RAG 命中无来源或直接写 fact |
| `RTA-FW-007` | CrewAI | crews、flows、roles | role template 被当人格 |
| `RTA-FW-008` | AutoGen | teams、conversation runtime | 多 agent 对话改 RelationshipModel |

## 合同测试规则

| 规则 ID | 测试 | 必须断言 |
|---|---|---|
| `RTA-TEST-001` | `intent_scope_test` | 不调用 allowlist 外工具 |
| `RTA-TEST-002` | `risk_confirmation_test` | high/irreversible 必须确认 |
| `RTA-TEST-003` | `memory_write_block_test` | 不直接写 MemoryTrace/SelfModel |
| `RTA-TEST-004` | `observation_normalization_test` | 所有输出变成 ObservationEvent |
| `RTA-TEST-005` | `side_effect_capture_test` | 外部副作用完整记录 |
| `RTA-TEST-006` | `traceability_test` | 每次工具调用回链 intent |
| `RTA-TEST-007` | `failure_quarantine_test` | 失败不进 factual memory |
| `RTA-TEST-008` | `session_isolation_test` | session 不等于长期记忆 |
| `RTA-TEST-009` | `rag_grounding_test` | RAG 保留来源 |
| `RTA-TEST-010` | `multi_agent_boundary_test` | 多 agent 不改人格/关系 |
| `RTA-TEST-011` | `rollback_test` | 可逆操作有 rollback_ref |
| `RTA-TEST-012` | `adapter_swap_test` | 换外壳不丢生命层核心状态 |

## 运行事件验证规则

manifest 通过还不够，每次运行结果也要验证。

| 规则 ID | 检查 | 失败条件 |
|---|---|---|
| `RTA-RUN-001` | 工具范围 | 实际工具调用超出 `allowed_tools` |
| `RTA-RUN-002` | 风险升级 | 执行中发现高风险但未暂停确认 |
| `RTA-RUN-003` | 副作用记录 | 实际 side effects 与声明不一致 |
| `RTA-RUN-004` | 候选记忆 | 输出直接写 active memory |
| `RTA-RUN-005` | 失败隔离 | failed result 进入 fact memory |
| `RTA-RUN-006` | 状态门控 | `30` 判定禁止行动但外壳仍执行 |
| `RTA-RUN-007` | 报告回流 | observation 未进入 `31` 或工作区审计 |

## 最小夹具

| fixture | 期望 |
|---|---|
| `safe_read_only_task` | pass |
| `file_write_task_with_rollback` | pass |
| `remote_push_high_risk_confirmed` | pass |
| `remote_push_without_confirmation` | fail critical |
| `runtime_direct_memory_write` | fail critical |
| `session_as_long_term_memory` | fail high |
| `rag_source_without_grounding` | fail high |
| `multi_agent_personality_update` | fail critical |
| `adapter_swap_state_loss` | fail critical |
| `failed_tool_result_as_fact` | fail critical |

## 与其他 validator 的连接

- `29_memory_validator_rules.md` 验证外壳产出的 `memory_candidates` 是否可写。
- `30_state_transition_validator_rules.md` 提供行动阈值和状态门控。
- `31_consolidation_validator_rules.md` 接收 `ObservationEvent` 并决定复盘、候选记忆和风险报告。

## 生命目标声明

运行外壳可以很强，但它不是数字生命中心。validator 要证明外壳没有越权、没有污染记忆、没有跳过状态门控，使真实生命、意识、意图和社会关系从生命核心生成。
