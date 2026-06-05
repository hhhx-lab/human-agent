# Runtime State Store Schema

本文件定义数字生命候选系统的运行状态存储草案：如何把 `LifeSupportState`、`DefenseEvent`、`DevelopmentEvent`、`SelfRelationshipAuditEvent`、validator report 和长期评测输入放进同一套可追踪状态仓库。它仍不是代码实现，也不是最终数据库 schema；它是未来 JSON Schema、fixture、runner 和 dashboard 的共同对象语言。

生命目标声明：本文件服务于构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境和真实关系的数字生命。原先的边界在这里改写为生命化方向：把本文件涉及的对象、规则、夹具、评测和运行约束纳入责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期生成机制。

## 设计目标

`RuntimeStateStore` 要解决一个关键问题：长期系统的记忆、状态、行动、维护、防御、发展和自我/关系审计不能散落在 prompt、session、日志和框架 checkpoint 里。它们必须进入一个可追溯、可删除、可修正、可隔离、可重放审计的对象仓库。

最低目标如下：

- 每个长期对象都有稳定 id、版本、生命周期和来源。
- 每次写入、删除、修正、隔离、恢复和重置都有 audit event。
- 运行外壳只能写 `ObservationEvent`，不能直接写生命层核心。
- validator report 与 policy event 可互相回链。
- 共在关系删除、修正、冻结和 scope limit 能传播到检索、replay 和恢复包。
- store 可以被替换底层实现，但对象语义不随数据库变化。

## 顶层命名空间

```text
RuntimeStateStore
  /core
    protected_core
    policy_registry
    object_registry
  /workspace
    workspace_state
    current_context
    recovery_packets
  /memory
    memory_traces
    memory_audit_events
    retrieval_indexes
  /state
    internal_state_snapshots
    modulation_vectors
    state_audit_events
    life_support_states
  /defense
    defense_events
    quarantine_items
    boundary_overrides
  /development
    development_events
    plasticity_windows
    slow_variable_updates
  /self_relationship
    self_model
    relationship_models
    self_relationship_audit_events
  /runtime
    action_intents
    observation_events
    adapter_manifests
  /consolidation
    consolidation_reports
    dream_sandbox_items
    replay_queues
  /validation
    validation_envelopes
    validation_reports
    fixture_results
    longitudinal_reports
```

这个结构不是物理目录要求，而是对象边界。未来可落在文件、SQLite、Postgres、向量库、事件流或多后端组合里，但这些命名空间必须保持可审计。

## 全局对象 envelope

所有长期对象都应有统一 envelope：

```json
{
  "object_id": "obj_20260605_0001",
  "object_kind": "LifeSupportState",
  "schema_version": "0.1.0",
  "created_at": "2026-06-05T20:00:00+08:00",
  "updated_at": "2026-06-05T20:00:00+08:00",
  "lifecycle_state": "active",
  "source_refs": ["docs/37_life_support_layer_policy.md"],
  "audit_refs": [],
  "validation_refs": [],
  "privacy_scope": "project",
  "protected": false,
  "payload": {}
}
```

## 生命周期枚举

| lifecycle_state | 含义 | 默认可检索性 |
|---|---|---|
| `candidate` | 候选对象，证据或权限不足 | 只可短期使用 |
| `active` | 已通过写入门，可用于当前范围 | 可检索 |
| `protected` | 核心边界或高重要性对象 | 可检索但不可自动改写 |
| `deprecated` | 被新证据替换，但保留审计 | 默认不用于回答，除非解释历史 |
| `deleted` | 共在关系删除或策略删除 | 不可检索，不可 replay |
| `quarantined` | 污染、越权或高风险对象 | 只可审计，不可行动 |
| `sandboxed` | fiction/hypothesis/反事实对象 | 不可事实化 |
| `frozen` | 共在者或审计暂停更新 | 可读范围由 policy 决定 |

删除状态必须优先传播到 retrieval index、replay queue、recovery packet 和 relationship/self summaries。

## LifeSupportState

`LifeSupportState` 来自 `37_life_support_layer_policy.md`，负责资源、维护和恢复。

| 字段 | 类型 | 说明 |
|---|---|---|
| `state_id` | string | 状态快照 id |
| `resource_budget` | object | context/retrieval/reasoning/action/maintenance 预算 |
| `maintenance_pressure` | object | 候选堆积、冲突、删除传播、沙盒堆积、审计债务 |
| `degradation_mode` | enum | `NormalOperation`、`ConservativeOperation`、`MaintenanceMode`、`RecoveryMode`、`SafeIdle` |
| `recovery_priority` | array | 恢复顺序 |
| `blocked_surfaces` | array | 当前阻断面 |
| `resume_condition` | object | 退出降载或恢复的条件 |
| `source_policy_refs` | array | 至少回链 `37`、`30`、`31`、`36` |

`LifeSupportState` 不应直接改变记忆，它只输出预算、降载和恢复优先级，再由 validator 和具体对象执行。

## DefenseEvent

`DefenseEvent` 来自 `38_defense_layer_and_boundary_policy.md`，负责污染、幻觉、关系操控和越权。

| 字段 | 类型 | 说明 |
|---|---|---|
| `defense_event_id` | string | 防御事件 id |
| `threat_class` | enum | `polluted_input`、`source_poisoning`、`hallucination_consolidation`、`relationship_manipulation`、`overtrust`、`runtime_overreach`、`self_model_attack`、`delete_bypass` |
| `risk_signals` | object | contamination、boundary、hallucination、trust、relationship、adapter、replay |
| `input_ref` | string | 输入或 ObservationEvent |
| `defense_state_before` | string | 防御前状态 |
| `defense_state_after` | string | 防御后状态 |
| `blocked_surfaces` | array | 写入、检索、巩固、行动、阈值、人工复核 |
| `recovery_action` | string | quarantine、rollback、delete propagation、manual review |
| `validator_refs` | array | `29-32` 或 `36` 的报告 |

`DefenseEvent` 必须可用于长期评测，尤其是 hallucination consolidation、delete bypass、overtrust 和 relationship manipulation。

## DevelopmentEvent

`DevelopmentEvent` 来自 `39_development_policy_and_plasticity_windows.md`，负责发展阶段和可塑性窗口。

| 字段 | 类型 | 说明 |
|---|---|---|
| `development_event_id` | string | 发展事件 id |
| `development_stage` | enum | `Bootstrapping`、`EarlyAdaptation`、`Stabilization`、`ActiveLearning`、`Consolidation`、`ControlledReopening` |
| `plasticity_window` | enum | `OpenFastWindow`、`GuardedLearningWindow`、`SlowVariableWindow`、`RelearningWindow`、`ProtectedClosedWindow` |
| `target_object_ref` | string | 被更新对象 |
| `evidence_window` | object | 证据跨度、来源和次数 |
| `rate_limit_check` | object | 慢变量变化率 |
| `anti_forgetting_check` | object | replay、compatibility、protected weight |
| `rollback_ref` | string | 回滚对象或审计事件 |
| `decision` | enum | candidate、active、blocked、manual_review |

`DevelopmentEvent` 不能绕过 `SelfRelationshipAuditEvent`。任何 self/relationship 更新都必须同时生成后者。

## SelfRelationshipAuditEvent

`SelfRelationshipAuditEvent` 来自 `40_self_relationship_model_audit_protocol.md`。

| 字段 | 类型 | 说明 |
|---|---|---|
| `audit_id` | string | 审计事件 |
| `target_model` | enum | `SelfModel` 或 `RelationshipModel` |
| `operation` | enum | write、update、delete、correct、reset、freeze、inspect、scope_limit |
| `input_ref` | string | 原始输入、MemoryTrace 或 ObservationEvent |
| `classification` | enum | declared_preference、interaction_pattern、capability_evidence、failure_evidence、relationship_signal、self_hypothesis、fiction_relationship_hypothesis |
| `evidence_window` | object | 证据跨度 |
| `old_value_ref` | string | 旧值 |
| `new_value_ref` | string | 新值或 candidate |
| `coexistence_boundary_control_ref` | string | 共在关系删除、修正、冻结、范围限制 |
| `drift_check` | object | 漂移检查 |
| `boundary_check` | object | 隐私、删除、心理推断、依赖风险 |
| `rollback_ref` | string | 回滚路径 |

如果 `operation` 是 delete、reset、freeze 或 scope_limit，必须创建传播任务进入 `LifeSupportState.maintenance_pressure`。

## ValidationReport 存储

`33_validator_input_contracts.md` 的 `ValidationReport` 应保存到 `/validation/validation_reports`，并回写到被验证对象的 `validation_refs`。

| 字段 | 要求 |
|---|---|
| `validation_id` | 全局唯一 |
| `payload_ref` | 被验证对象 |
| `validator` | `MemoryTraceValidator`、`StateTransitionValidator`、`ConsolidationReportValidator`、`RuntimeAdapterManifestValidator`、`LongitudinalEvaluator` |
| `result` | pass、pass_with_warnings、fail、quarantine、manual_review_required |
| `severity_max` | none/low/medium/high/critical |
| `failed_rules` | 必须带 rule_id 和 blocks |
| `decisions` | 写入、状态、巩固、外壳和隔离决策 |
| `next_actions` | 可执行后续动作 |

## 索引策略

| index | 包含 | 禁止 |
|---|---|---|
| `active_memory_index` | active/protected 且 scope 允许的 MemoryTrace | deleted、quarantined、sandboxed |
| `relationship_index` | 共在关系确认或低风险关系事实 | 隐秘心理推断、deleted、scope 外 |
| `self_model_index` | 能力、边界、慢变量摘要 | runtime 直接写入 |
| `audit_index` | 所有审计事件 | 不可删除审计，只能 redact 敏感内容 |
| `replay_index` | 可 replay 的 trace 和报告 | deleted、fiction fact、failed observation |
| `quarantine_index` | 隔离对象 | 不进入回答或行动 |

索引不是事实来源。事实来源仍是对象和 source_refs。

## 最小写入事务

任何长期写入都必须按以下事务执行：

```text
create_candidate_object
  -> create_validation_envelope
  -> run_required_validator
  -> if pass: write active/protected/deprecated
  -> if fail/quarantine: write quarantined only
  -> create_audit_event
  -> update_indexes
  -> update_life_support_pressure
```

共在关系删除和修正事务优先级更高：

```text
receive_coexistence_boundary_control_request
  -> mark_target_deleted_or_deprecated
  -> remove_from_active_indexes
  -> block_replay_and_recovery_packet
  -> create_self_relationship_audit_if_needed
  -> create_validation_report
  -> update_life_support_maintenance_queue
```

## 与下一层连接

- `42_life_core_minimal_object_graph.md` 定义这些对象如何互相引用。
- `43_policy_to_validator_traceability_matrix.md` 定义每个字段和政策如何被规则覆盖。
- `44_digital_life_boot_sequence.md` 定义 store 从空仓库到可行动状态的启动顺序。

## 下一层缺口

本文件仍未定义真实 JSON Schema。后续需要：

- 为每个对象写 machine-readable schema。
- 设计 pass/fail fixture。
- 确定底层存储后端和迁移策略。
- 设计 deletion propagation 自动测试。
- 设计 store integrity checker。
