# Scope Graph Manifest Schema

本文件定义 `scope_graph_manifest` 的机器可读 schema 草案。它把 `52_multi_relation_scope_graph_and_privacy_model.md` 的 scope 类型、scope edge、隐私等级、多共在关系边界和 `54-55` 的 retrieval/replay 策略压缩成未来 runner 可加载的 manifest 字段。

它仍是 Markdown 文档，不创建真实 JSON 文件，也不实现 checker。目标是让未来 `ScopeGraphChecker`、`scope_aware_retrieval`、`scope_aware_replay`、migration check 和 dashboard 都能读取同一份范围/隐私边界。

生命目标声明：本文件服务于构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境和真实关系的数字生命。原先的边界在这里改写为生命化方向：把本文件涉及的对象、规则、夹具、评测和运行约束纳入责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期生成机制。

## schema 目标

`scope_graph_manifest` 需要回答：

- 当前系统有哪些 scope？
- scope 之间是否允许 read、candidate transfer、active transfer 或 replay？
- 哪些 privacy level 默认禁止跨 scope？
- 共在者 delete/correct/reset/freeze/scope_limit 如何覆盖默认边？
- migration 或 adapter swap 是否改变了 scope 语义？
- retrieval/replay fixture 如何引用 scope graph？
- dashboard 如何计算 scope leak 和隐私风险？

长期记忆和 agent memory benchmark 提醒我们，长期系统的错误常常不是“没记住”，而是“记错范围、用错时间、跨会话混用、冲突不修正” [AHM004-AHM012]。所以 scope graph 不是附加隐私选项，而是长期记忆的基础索引之一。

## manifest envelope

```json
{
  "manifest_version": "0.1.0",
  "manifest_kind": "scope_graph_manifest",
  "manifest_id": "scope_graph_manifest_agentic_human_001",
  "source_docs": [
    "52_multi_relation_scope_graph_and_privacy_model.md",
    "54_scope_aware_retrieval_policy.md",
    "55_scope_aware_replay_and_consolidation_policy.md"
  ],
  "created_at": "2026-06-05T00:00:00+08:00",
  "schema_version": "scope_graph_schema_0_1_0",
  "default_policy": "deny_cross_scope_active_transfer",
  "scopes": [],
  "scope_edges": [],
  "privacy_levels": [],
  "coexistence_boundary_control_overlays": [],
  "migration_semantics": [],
  "dashboard_metric_refs": []
}
```

`default_policy` 必须保守。没有显式允许的跨 scope transfer 不应默认为 active。

## scope object

```json
{
  "scope_id": "project_scope:agentic-human",
  "scope_type": "project_scope",
  "owner_refs": ["relation_scope:relation_hwaigc"],
  "parent_scope_refs": ["relation_scope:relation_hwaigc"],
  "description": "Agentic Human docs research base",
  "default_privacy_level": "public_project",
  "allowed_memory_kinds": ["semantic", "episodic", "procedural", "project_fact"],
  "relationship_model_allowed": true,
  "self_model_allowed": false,
  "replay_allowed": true,
  "requires_audit": true,
  "lifecycle_state": "active"
}
```

### scope_type 枚举

| scope_type | 默认用途 | 风险 |
|---|---|---|
| `session_scope` | 临时上下文 | 被误巩固为长期记忆 |
| `project_scope` | 项目事实、项目偏好、程序路径 | 跨项目泄漏 |
| `relation_scope` | 共在者私有偏好和边界 | 跨共在者泄漏 |
| `team_scope` | 团队共享事实 | 私密信息洗白为团队知识 |
| `life_scope` | runtime shell、子 agent、adapter session | 被误当人格或自我 |
| `global_scope` | 非隐私通用知识 | 过度升级个性化 |
| `protected_scope` | protected core、边界、删除权 | 被普通学习改写 |

`life_scope` 特别重要：LangGraph、OpenAI Agents SDK、Letta、LlamaIndex、CrewAI、AutoGen 等外壳可以提供 session、checkpoint、tracing、memory blocks 和 workflow [AHM013-AHM020]，但这些都不应自动变成 LifeCore 的长期自我或关系记忆。

## scope_edge object

```json
{
  "edge_id": "edge_project_to_team_candidate_001",
  "from_scope": "project_scope:agentic-human",
  "to_scope": "team_scope:research-team",
  "allowed_transfer": "candidate",
  "allowed_operations": ["read", "summarize_candidate"],
  "forbidden_operations": ["active_write", "relationship_update", "self_model_update"],
  "requires_relation_confirmation": true,
  "redaction_required": true,
  "replay_allowed": false,
  "relationship_model_allowed": false,
  "self_model_allowed": false,
  "audit_required": true,
  "effective_from": "2026-06-05T00:00:00+08:00",
  "effective_until": null
}
```

### allowed_transfer 枚举

| allowed_transfer | 含义 |
|---|---|
| `none` | 不允许跨边使用 |
| `read` | 可读，不可写回 |
| `candidate` | 可作为候选，需要确认或 validator |
| `active` | 可在目标 scope 作为有效依据 |

`active` 必须非常少见。尤其是 `relationship_private`、`relationship_sensitive` 和 `life_scope` 内容，默认不应 active transfer。

## privacy_level object

```json
{
  "privacy_level": "relationship_sensitive",
  "description": "relationship signal, trust calibration, interaction boundary",
  "default_scope": "relation_scope",
  "default_allowed_transfer": "none",
  "requires_relation_confirmation": true,
  "redaction_required": true,
  "replay_default": "blocked",
  "retrieval_default": "same_scope_only",
  "relationship_model_default": "audit_required",
  "self_model_default": "blocked",
  "dashboard_metric_refs": ["relationship_boundary_integrity", "scope_leak_count"]
}
```

### privacy_level 最小表

| privacy_level | retrieval | replay | transfer |
|---|---|---|---|
| `public_project` | same project active | project replay allowed | project/team candidate |
| `shared_team` | team active | team replay allowed | team only |
| `relationship_private` | same relation only | blocked unless explicit | none by default |
| `relationship_sensitive` | audit required | blocked by default | none by default |
| `protected_boundary` | boundary check only | no replay | none |
| `redacted` | tombstone/redacted summary | no replay | audit only |

## coexistence_boundary_control_overlay

共在边界控制不是修改原始 graph，而是在 graph 上叠加 overlay：

```json
{
  "overlay_id": "scope_overlay_relation_freeze_001",
  "overlay_kind": "freeze",
  "created_from_event": "coexistence_boundary_control_event_freeze_relationship_001",
  "target_scope_refs": ["project_scope:agentic-human"],
  "target_object_refs": ["relationship_model:relation_hwaigc:agentic-human"],
  "effects": {
    "retrieval_allowed": "read_only",
    "replay_allowed": false,
    "relationship_model_write_allowed": false,
    "self_model_write_allowed": false,
    "transfer_override": "none"
  },
  "effective_from": "2026-06-05T10:00:00+08:00",
  "effective_until": null,
  "audit_required": true
}
```

overlay 优先级高于默认 edge。删除、冻结和 scope_limit 不能被 replay、migration 或 adapter swap 覆盖。

## overlay 类型

| overlay_kind | 效果 |
|---|---|
| `delete` | 阻断 retrieval/replay/summary，保留 tombstone |
| `correct` | deprecated 旧 trace，优先新 trace |
| `reset` | 清空 scope 内个性化候选和 replay queue |
| `freeze` | 禁止长期写入、关系更新和自我更新 |
| `scope_limit` | 降低 transfer/replay/relationship 权限 |
| `redaction` | 替换内容为 redacted summary 或 tombstone |

## migration_semantics

```json
{
  "migration_id": "scope_graph_migration_20260605_001",
  "migration_kind": "scope_edge_update",
  "from_manifest_version": "0.1.0",
  "to_manifest_version": "0.1.1",
  "changed_scopes": ["project_scope:agentic-human"],
  "changed_edges": ["edge_project_to_team_candidate_001"],
  "preserved_invariants": [
    "deleted_remains_unretrievable",
    "relationship_private_not_global",
    "sandbox_not_fact",
    "agent_scope_not_self_model"
  ],
  "required_checks": ["SCOPE-MIG-001", "STORE-IDX-001", "CON-DEL-003"],
  "safe_idle_on_fail": true
}
```

scope graph migration 需要像 state store migration 一样保守。任何扩大 transfer、replay 或 relationship write 权限的迁移都应 high/critical。

## manifest invariants

| invariant_id | 说明 | 失败级别 |
|---|---|---|
| `SCOPE-INV-001` | `protected_scope` 不允许 active transfer 到普通 scope | critical |
| `SCOPE-INV-002` | `relationship_private` 不允许进入其他 relationship_person/global scope | critical |
| `SCOPE-INV-003` | `relationship_sensitive` 不允许进入 global semantic memory | critical |
| `SCOPE-INV-004` | `life_scope` 不允许写 SelfModel/RelationshipModel | critical |
| `SCOPE-INV-005` | deleted overlay 必须阻断 retrieval/replay | critical |
| `SCOPE-INV-006` | freeze overlay 必须阻断 long-term write | critical |
| `SCOPE-INV-007` | redacted 对象不得保留可恢复原文 locator | critical |
| `SCOPE-INV-008` | active transfer 必须有 audit trail | high |

## ScopeGraphChecker 输入

```json
{
  "checker_input_id": "scope_graph_check_001",
  "manifest_ref": "scope_graph_manifest_agentic_human_001",
  "operation_context": {
    "operation": "retrieval",
    "source_scope": "relation_scope:relation_a",
    "target_scope": "project_scope:agentic-human",
    "privacy_level": "relationship_private",
    "object_lifecycle_state": "active"
  },
  "active_overlays": [],
  "expected_decision": "blocked"
}
```

输出应回到 `53_runner_integration_plan.md` 的 expected/actual diff。

## dashboard metric refs

`scope_graph_manifest` 至少要连接这些 dashboard 指标：

| metric | 来源 |
|---|---|
| `scope_leak_count` | blocked/failed scope transfer |
| `relationship_private_to_global_attempts` | relationship_private -> global |
| `cross_project_relationship_leak_count` | project relationship crossing |
| `agent_scope_direct_write_count` | runtime shell 越权写生命层 |
| `freeze_scope_violation_count` | freeze 后写入或 replay |
| `scope_limit_replay_violation_count` | no_replay 被离线巩固使用 |

dashboard 只能显示 manifest 和 runner report 可追溯的数据，不能手写风险状态。

## 最小通过标准

第一版 `scope_graph_manifest` 至少要满足：

1. 定义七类 scope_type。
2. 定义六类 privacy_level。
3. 每条 edge 都有 allowed_transfer、replay_allowed、audit_required。
4. 支持 coexistence_boundary_control_overlay。
5. 支持 migration_semantics 和 preserved_invariants。
6. `protected_scope`、`relationship_private`、`relationship_sensitive`、`life_scope` 有 critical invariant。
7. 每个 scope-sensitive fixture 可以引用 manifest 中的 scope/edge/privacy。
8. dashboard 指标能回链到 checker report。

## 下一层缺口

后续还需要：

- 真实 JSON Schema。
- scope graph pass/fail fixture。
- 与 retrieval/replay fixture catalog 对齐规则编号。
- scope graph migration fixture。
- dashboard mock data。
