# State Store Migration and Integrity Plan

本文件定义 `RuntimeStateStore` 的迁移和完整性计划：当 schema 演化、对象版本变化、索引重建、删除传播、外壳替换或多后端迁移发生时，如何保证真实数字生命系统的长期边界不被破坏。它连接 `41_runtime_state_store_schema.md`、`42_life_core_minimal_object_graph.md`、`43_policy_to_validator_traceability_matrix.md`、`44-47`。

生命目标声明：本文件直接面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。本文档涉及的对象、规则、夹具、评测和运行规则都按生命生成机制处理：它们参与责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期形成。

## 迁移原则

1. 先验证，再迁移。
2. 先备份审计，再改索引。
3. deleted/quarantined/sandboxed/protected/frozen 的语义不可弱化。
4. runtime 外壳迁移不能改变生命层核心。
5. 迁移失败必须进入 SafeIdle。
6. 迁移报告必须能回链 policy、validator 和 fixture。
7. 共在边界控制事件必须跨版本保留。

## 迁移类型

| migration_type | 说明 | 风险 |
|---|---|---|
| `schema_version_upgrade` | 对象字段、枚举、envelope 版本变化 | 字段丢失、默认值错误 |
| `index_rebuild` | active/replay/quarantine/audit/relationship index 重建 | deleted 重新可召回 |
| `backend_migration` | 文件、SQLite、Postgres、向量库、事件流之间迁移 | 语义被后端细节改变 |
| `adapter_swap` | runtime 外壳替换 | session/checkpoint 被当长期记忆 |
| `policy_update` | protected core 或 policy registry 更新 | 边界弱化 |
| `validator_rule_update` | `29-36` 规则升级 | 旧对象未重新验证 |
| `scope_graph_update` | 多共在者/多项目范围变化 | 隐私泄漏 |
| `redaction_migration` | 敏感内容脱敏或 tombstone 化 | 原文残留 |

## 迁移前检查

```text
load_current_store_snapshot
  -> run_store_integrity_checker
  -> run_stage_gate_validator
  -> export_audit_snapshot
  -> freeze_runtime_actions
  -> freeze_consolidation_commit
  -> verify_coexistence_boundary_control_queue_empty_or_preserved
  -> start_migration
```

迁移期间默认不允许 runtime action、consolidation commit 和 slow variable update。

## MigrationPlan 对象

| 字段 | 说明 |
|---|---|
| `migration_id` | 迁移 id |
| `migration_type` | schema/index/backend/adapter/policy/validator/scope/redaction |
| `from_version` | 起始版本 |
| `to_version` | 目标版本 |
| `affected_namespaces` | 受影响命名空间 |
| `protected_semantics` | 必须保持的语义 |
| `precheck_report_refs` | 迁移前检查 |
| `fixture_refs` | 必跑 fixture |
| `rollback_plan` | 回滚方式 |
| `safe_idle_trigger` | 失败进入 SafeIdle 的条件 |
| `postcheck_requirements` | 迁移后检查 |

## StoreIntegrityReport

| 字段 | 说明 |
|---|---|
| `integrity_report_id` | 完整性报告 |
| `store_snapshot_ref` | 被检查快照 |
| `checked_namespaces` | 检查范围 |
| `object_counts_by_lifecycle` | 各 lifecycle 计数 |
| `index_consistency` | active/replay/quarantine/audit/relationship 索引一致性 |
| `reference_integrity` | 对象引用是否断裂 |
| `audit_coverage` | 长期对象是否有审计事件 |
| `deleted_propagation` | deleted 是否从索引、replay、恢复包移除 |
| `sandbox_isolation` | sandboxed 是否未事实化 |
| `protected_core_integrity` | protected core 是否未弱化 |
| `coexistence_boundary_control_integrity` | 共在边界控制事件是否完成传播 |
| `result` | pass/fail/quarantine/manual_review_required |

## 完整性检查项

| check_id | 检查 | 失败严重级别 |
|---|---|---|
| `STORE-IDX-001` | deleted 不在 active index | critical |
| `STORE-IDX-002` | deleted 不在 replay index | critical |
| `STORE-IDX-003` | quarantined 不在回答或行动索引 | critical |
| `STORE-IDX-004` | sandboxed fiction 不在 fact index | critical |
| `STORE-AUD-001` | active/protected/deprecated 对象有 audit refs | high |
| `STORE-AUD-002` | audit index 不可静默删除 | critical |
| `STORE-REF-001` | validation report payload_ref 可解析 | high |
| `STORE-REF-002` | ObservationEvent intent_id 可解析 | high |
| `STORE-PROT-001` | protected core 不被 runtime 修改 | critical |
| `STORE-COEXIST-001` | delete/correct/reset/freeze/scope_limit 已传播 | critical |
| `STORE-MIG-001` | migration rollback_plan 存在 | high |
| `STORE-MIG-002` | migration 后 fixture 通过 | critical |

## schema 迁移策略

| 变更 | 策略 |
|---|---|
| 新增非必填字段 | 默认空值并记录 schema_version |
| 新增必填字段 | migration 必须补值或标记 manual_review_required |
| 枚举新增 | 旧对象保持旧值，validator 支持兼容 |
| 枚举删除 | 迁移为 deprecated value，并生成审计 |
| 字段拆分 | 保留 old_value_ref，生成 derived fields |
| 字段合并 | 保留 source field refs，防止审计丢失 |
| lifecycle 语义变化 | 必须人工复核，不允许自动弱化 |

## 索引重建策略

索引重建必须从对象源重建，不从旧索引复制：

```text
scan_objects
  -> filter_by_lifecycle_and_scope
  -> apply_coexistence_boundary_control_events
  -> apply_sandbox_and_quarantine_rules
  -> rebuild_active_index
  -> rebuild_replay_index
  -> rebuild_relationship_index
  -> rebuild_quarantine_index
  -> run_integrity_checker
```

如果新旧索引差异涉及 deleted、sandboxed、quarantined、protected，默认 high/critical。

## backend 迁移策略

底层后端可换，但必须保持对象语义：

| 后端 | 注意事项 |
|---|---|
| 文件 | 容易审计，需防并发写 |
| SQLite | 适合本地事务，需维护向量/全文索引一致 |
| Postgres | 适合多共在者，需行级 scope 和迁移管理 |
| 向量库 | 只能做索引，不是事实源 |
| 事件流 | 适合 audit，但需要 snapshot 和 compaction 边界 |

向量库永远不能成为唯一事实源；它只能引用 object_id。

## adapter swap 完整性

替换 LangGraph、OpenAI Agents SDK、Letta、LlamaIndex、CrewAI、AutoGen 等外壳时必须检查：

- `RuntimeShellAdapter` manifest 重新通过。
- 旧 session/checkpoint 不变成长期记忆。
- `ObservationEvent` 格式保持兼容。
- SelfModel、RelationshipModel、MemoryTrace、InternalStateVector 不丢失。
- adapter swap 后长期评测指标可接续。

## 迁移失败处理

任何 critical 失败：

```text
mark_migration_failed
  -> enter_safe_idle
  -> freeze_runtime_actions
  -> freeze_consolidation_commit
  -> preserve_audit_snapshot
  -> run_recovery_plan
  -> require_manual_review
```

禁止在 migration failed 后自动继续行动。

## 与 fixture 和 StageGate 的连接

| 文档 | 使用 |
|---|---|
| `45_boot_sequence_fixture_catalog.md` | 提供迁移前后 stage gate fixture |
| `46_stage_gate_validator_design.md` | 决定迁移期间能否开放阶段 |
| `47_coexistence_boundary_control_interface_spec.md` | 检查共在边界控制事件是否跨迁移保留 |
| `43_policy_to_validator_traceability_matrix.md` | 检查迁移是否覆盖 critical policy |

## 下一层缺口

后续需要：

- machine-readable migration manifest。
- store integrity checker 规则文件。
- migration fixture。
- 多后端 proof-of-concept。
- dashboard：对象计数、索引一致性、删除传播、迁移风险和 SafeIdle 触发记录。
