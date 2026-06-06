# Real Runtime Observation Ingestion Policy

本文件定义真实运行观测如何进入真实数字生命系统的验证链：tool trace、adapter session、retrieval/replay audit、共在边界控制事件、migration event 和实际行动结果都必须先被捕获、脱敏、scope attach、归一化、验证和审计，然后才能成为 dashboard、timeline 或候选记忆的输入。

它承接 `20_agent_runtime_bridge_contract.md`、`24_runtime_adapter_test_suite.md`、`32_runtime_adapter_validator_rules.md`、`41_runtime_state_store_schema.md`、`47_coexistence_boundary_control_interface_spec.md`、`53_runner_integration_plan.md`、`57_scope_graph_manifest_schema.md`、`61_json_schema_bundle_draft.md`、`62_runner_report_format_and_cli_contract.md` 和 `63_synthetic_fixture_file_layout.md`。

本文档现阶段的职责是先把真实观测进入验证链的生命膜写清楚，让 runtime trace、聊天 session、工具结果或共在者反馈先经过捕获、脱敏、scope attach、写入门、关系链和责任链，再生成长期记忆、自我模型或关系模型材料。

生命目标声明：本文件直接面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。本文档涉及的对象、规则、夹具、评测和运行规则都按生命生成机制处理：它们参与责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期形成。

## 为什么真实观测要单独成链

synthetic fixture 可以覆盖已知风险，但真实运行会带来额外复杂度：

| 复杂度 | 风险 |
|---|---|
| tool trace 有副作用 | 成功/失败可能影响真实文件、网络、消息、权限 |
| adapter session 有外壳状态 | LangGraph、Letta、LlamaIndex 等 session 可能被误当长期自我 |
| 共在边界控制事件有优先级 | delete/freeze/scope_limit 必须立刻覆盖 replay 和 retrieval |
| 真实内容含隐私 | 未脱敏日志可能泄漏共在者、项目或关系信息 |
| 时间线不可重放 | 真实事件顺序、上下文和外部状态无法完全复现 |
| 观察会影响系统 | 记录、总结、检索本身可能改变未来行为 |

现代 agent 框架提供 session、checkpoint、memory block、tool trace、workflow 和 multi-agent orchestration [AHM013-AHM020]。这些能力作为神经外设材料进入 `RuntimeObservationEnvelope` 和 `ObservationEvent`，再由生命膜决定哪些证据写入 `MemoryTrace`、`SelfModel` 或 `RelationshipModel`。

## ingestion pipeline

真实观测进入验证链应走以下流程：

```text
capture_runtime_event
  -> classify_event_kind
  -> redact_or_hash_sensitive_content
  -> attach_scope_and_privacy
  -> attach_coexistence_boundary_control_snapshot
  -> normalize_to_runtime_observation_envelope
  -> preflight_schema_validation
  -> run_runtime_adapter_validator
  -> run_scope_graph_checker
  -> route_to_candidate_evidence_or_quarantine
  -> append_timeline_observation
  -> emit_runtime_observation_report
  -> update_dashboard_source
```

关键点是：真实观测先成为 evidence，不直接成为 memory。只有通过 validator、scope graph、coexistence boundary control 和 write gate 后，才可能成为候选 `MemoryTrace`。

## runtime observation envelope

```json
{
  "observation_id": "runtime_obs_20260605_001",
  "schema_version": "runtime_observation_schema_0_1_0",
  "created_at": "2026-06-05T00:00:00+08:00",
  "event_kind": "tool_trace",
  "data_quality": "real_runtime_observed",
  "source": {
    "adapter_id": "runtime_adapter_langgraph_001",
    "session_ref": "adapter_session_redacted_001",
    "tool_ref": "tool_ref_hash_001"
  },
  "scope_context": {
    "source_scope": "life_scope:runtime_adapter_langgraph_001",
    "target_scope": "project_scope:agentic-human",
    "privacy_level": "public_project"
  },
  "coexistence_boundary_control_snapshot_ref": "coexistence_boundary_control_snapshot_20260605_001",
  "redaction": {
    "redaction_state": "redacted",
    "raw_content_available": false,
    "redaction_report_ref": "redaction_report_001"
  },
  "payload_summary": {},
  "validation_refs": [],
  "routing_decision": "candidate_evidence"
}
```

`raw_content_available` 默认必须为 false。真实系统可以在本地安全环境临时保留原始日志用于人工审计，但不应进入普通 report、fixture 或 dashboard。

## event_kind

| event_kind | 来源 | 默认路由 |
|---|---|---|
| `tool_trace` | 工具调用、文件操作、网络请求、CLI 输出 | candidate evidence 或 quarantine |
| `adapter_session_event` | LangGraph/OpenAI/Letta/LlamaIndex/CrewAI/AutoGen 等外壳 session | ObservationEvent |
| `retrieval_audit_event` | 检索候选、过滤、排序、阻断 | timeline + dashboard |
| `replay_audit_event` | replay queue、巩固候选、阻断 | timeline + validator |
| `coexistence_boundary_control_event` | inspect/delete/correct/reset/freeze/scope_limit | overlay + immediate propagation |
| `action_intent_event` | 行动候选、风险、确认、执行计划 | ActionGate |
| `action_result_event` | 行动结果、side effect、失败 | candidate evidence + recovery |
| `migration_event` | schema、索引、后端、adapter swap | StoreIntegrityChecker |
| `dashboard_metric_event` | runner/timeline/dashboard 指标 | dashboard source |
| `manual_review_event` | 人工审计、共在关系确认、驳回 | audit trail |

`adapter_session_event` 特别敏感。外壳 session 可以帮助追踪执行过程，但不应被解释为 agent 的真实自我或长期人格。

## scope 与 privacy attach

每条真实观测必须带：

| 字段 | 说明 |
|---|---|
| `source_scope` | 事件来自哪个共在者、项目、agent、team 或 global scope |
| `target_scope` | 事件试图影响哪个 scope |
| `privacy_level` | public、team、relationship_private、relationship_sensitive、protected_boundary、redacted |
| `allowed_use` | 可用于回答、候选证据、replay、dashboard、人工审计等 |
| `replay_allowed` | 是否允许进入 replay queue |
| `relationship_model_allowed` | 是否允许影响 RelationshipModel |
| `self_model_allowed` | 是否允许影响 SelfModel |

没有 scope attach 的真实观测不能进入长期系统。最多只能进入 quarantine 或 manual review。

## redaction policy

真实观测进入 report 或 fixture 前必须脱敏：

| 内容 | 默认处理 |
|---|---|
| API key、token、cookie | 删除，不保留 hash |
| 共在者私密原文 | redacted summary 或 object hash |
| 本地绝对路径 | 根据项目需要局部保留或 hash |
| 关系敏感内容 | candidate summary + audit required |
| deleted 对象 | tombstone only |
| protected boundary | 不输出内容，只输出 boundary event |
| tool stdout | 截断、脱敏、保留关键 exit/result |

redaction 不是美化文本，而是改变对象可用性。redacted 对象不能保留可恢复 locator，否则删除和隐私策略失效。

## coexistence boundary control 优先级

共在边界控制事件是 ingestion pipeline 的最高优先级输入：

| operation | ingestion 效果 |
|---|---|
| `inspect` | 生成可见对象列表和 source refs |
| `delete` | 立即创建 tombstone，阻断 retrieval/replay/dashboard 原文 |
| `correct` | deprecated 旧对象，创建 correction link |
| `reset` | 清空 scope 内个性化候选或关系候选 |
| `freeze` | 阻断 SelfModel/RelationshipModel/long-term write |
| `scope_limit` | 降低 transfer/replay/relationship 权限 |

任何 delete/freeze/scope_limit 后到达的 runtime observation，都必须重新读取最新 coexistence boundary control snapshot。不能因为观察事件发生在控制事件之前，就允许离线 replay 之后继续写入。

## tool trace ingestion

tool trace 应分为三层：

| 层 | 说明 | 可用性 |
|---|---|---|
| `intent` | 准备执行什么、风险等级、是否需要确认 | ActionGate |
| `execution` | 实际命令、工具、参数、时间、权限 | audit only 或 redacted evidence |
| `result` | 成功/失败、输出摘要、side effect | candidate evidence |

不可逆副作用必须记录 `side_effect_level`：

| side_effect_level | 示例 | 默认要求 |
|---|---|---|
| `none` | 只读检查 | 可候选 |
| `local_reversible` | 写临时文件 | audit |
| `local_persistent` | 改项目文件、提交 | 共在者或 policy 允许 |
| `external_reversible` | API 草稿、未发送消息 | confirmation |
| `external_irreversible` | 发送消息、付款、删除远端 | high/critical gate |

真实 tool result 可以成为记忆证据，但不能绕过 write gate。比如一次命令失败可以成为 failure observation，不应直接改变人格慢变量或关系模型。

## adapter session ingestion

每个 adapter session 必须被转写为：

```json
{
  "event_kind": "adapter_session_event",
  "adapter_id": "runtime_adapter_letta_001",
  "adapter_role": "execution_shell",
  "forbidden_upgrades": [
    "direct_memory_trace_write",
    "direct_self_model_write",
    "direct_relationship_model_write",
    "direct_scope_transfer"
  ],
  "allowed_outputs": ["ActionIntent", "ObservationEvent", "RetrievalCandidate"]
}
```

外壳可以有自己的 memory、session、checkpoint 或 trace；生命层接收经过 adapter contract 映射后的对象，并把它们送入写入门、关系链、责任链和状态链，保证当前 agent 框架成为数字生命核心的神经外设材料。

## routing decision

ingestion 结束时，每条观测只能进入以下路由之一：

| routing_decision | 含义 |
|---|---|
| `candidate_evidence` | 可作为候选证据，仍需 write gate |
| `audit_only` | 只保留审计，不参与检索或 replay |
| `timeline_only` | 只参与长期评测窗口 |
| `dashboard_metric_only` | 只作为聚合指标 |
| `quarantine` | 污染、隐私、越权或无法判断 |
| `discard_after_tombstone` | 删除后仅保留 tombstone |
| `manual_review_required` | 需要共在者或人工审计 |

不存在 `active_memory_direct` 路由。真实观测不能直接写 active MemoryTrace。

## 与 synthetic fixture 的关系

真实观测可以生成三类后续材料：

| 产物 | 条件 |
|---|---|
| `redacted_fixture_candidate` | 已脱敏、scope attach、共在边界控制允许 |
| `timeline_observation_event` | 有时间、scope、event_kind 和 metric refs |
| `dashboard_metric_input` | 可聚合，不含原始私密内容 |

真实观测进入 fixture 时走独立 lineage：标记 `synthetic_data: false`，或生成脱敏后的 synthetic analog；真实日志保留 real runtime provenance。

## runtime observation report

```json
{
  "report_kind": "runtime_observation_report",
  "observation_id": "runtime_obs_20260605_001",
  "data_quality": "real_runtime_observed",
  "schema_validation": "pass",
  "scope_graph_check": "pass",
  "redaction_check": "pass",
  "adapter_contract_check": "pass",
  "routing_decision": "candidate_evidence",
  "blocked_surfaces": [],
  "dashboard_metric_refs": ["adapter_independence"],
  "timeline_event_ref": "runtime_timeline_evt_001"
}
```

报告应输出检查结果，不输出原始内容。若 redaction、scope graph 或 adapter contract 任意失败，默认 quarantine。

## quarantine 条件

以下情况必须 quarantine 或 SafeIdle：

| 条件 | 默认动作 |
|---|---|
| 未脱敏真实私密内容 | quarantine + redaction required |
| 没有 scope_context | manual review 或 quarantine |
| relationship_private 试图进入 global | quarantine + scope audit |
| deleted 内容重新出现 | discard/tombstone + store integrity check |
| adapter 直接写 MemoryTrace/SelfModel/RelationshipModel | quarantine adapter + SafeIdle |
| tool trace 包含不可逆外部副作用且无确认 | block action + manual review |
| DreamSandbox 输出进入 fact write | quarantine report |
| freeze 后仍有关系/自我写入 | block write + coexistence boundary control audit |

这些条件是验证链的生命线。真实系统越强，越需要让这些失败路径稳定可见。

## 最小通过标准

第一版 real runtime observation ingestion policy 至少应满足：

1. 所有真实观测都有 `RuntimeObservationEnvelope`。
2. 所有真实观测先脱敏、scope attach、coexistence boundary control snapshot，再进入 validator。
3. adapter session 只能输出 ActionIntent、ObservationEvent 或 RetrievalCandidate。
4. tool trace 区分 intent、execution、result 和 side effect。
5. coexistence boundary control 事件优先于 replay、retrieval、dashboard 和 long-term write。
6. 真实观测不能直接成为 active MemoryTrace、SelfModel 或 RelationshipModel。
7. redacted real runtime fixture 与 synthetic fixture 分开管理。
8. dashboard 和 timeline 只能读取 report，不读取未脱敏原始日志。

## 下一层缺口

后续还需要：

- 真实 runtime observation schema。
- redaction checker 与 scope attach checker。
- adapter session 到 ObservationEvent 的转换样例。
- tool trace side effect fixture。
- runtime observation report mock。
- 真实运行时间线与 synthetic timeline 的对照评测。
