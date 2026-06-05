# JSON Schema Bundle Draft

本文件定义 `JSON Schema bundle` 的草案，把 `49-60` 中出现的 policy manifest、stage gate、fixture、migration、scope graph、timeline bundle 和 dashboard source 统一到未来可实现的 schema 包。它仍然是 Markdown 文档，不创建真实 `.json` 或 `.schema.json` 文件，不实现 checker。

目标是让后续工程实现不再把 schema 散落在 runner、dashboard、fixture generator 和 adapter 代码里，而是先有一个稳定的 bundle 边界：哪些字段是共享定义，哪些对象必须有 source doc，哪些失败必须 fail closed，哪些数据只能来自 synthetic fixture，哪些真实运行观测必须先经过 scope、privacy、lifecycle 和 user control 检查。

边界声明：JSON Schema 只能验证工程对象的形状、引用和部分不变量，不能证明系统真实有意识、真实情绪、真实人格、真实关系或真实生命。schema 是数字生命候选系统的约束语言，不是生命本体。

## 为什么需要 bundle

如果每个 validator 自己定义输入字段，长期系统会很快出现四类漂移：

| 漂移 | 后果 |
|---|---|
| 字段漂移 | 同一个 `scope_id`、`fixture_id`、`lifecycle_state` 在不同模块含义不同 |
| 严重级别漂移 | `critical` 在 memory validator 阻断，在 dashboard 中却只是 warning |
| 引用漂移 | fixture 覆盖了规则，但规则没有 source doc 或 dashboard metric |
| 数据质量漂移 | synthetic mock 被误读成真实运行通过 |

长期记忆和 agent memory 研究提醒我们，真正困难的不只是“记住更多”，而是跨会话保持、更新、冲突、隐私、workflow 知识和行动上下文的一致性 [AHM004-AHM012]。因此 schema bundle 的核心不是格式洁癖，而是让每一次写入、检索、replay、迁移和 dashboard 展示都有同一套对象语言。

## bundle envelope

未来真实 schema bundle 可以采用以下 envelope：

```json
{
  "schema_bundle_id": "agentic_human_schema_bundle_0_1_0",
  "bundle_kind": "json_schema_bundle",
  "schema_dialect": "https://json-schema.org/draft/2020-12/schema",
  "bundle_version": "0.1.0",
  "created_at": "2026-06-05T00:00:00+08:00",
  "source_docs": [
    "49_machine_readable_policy_manifest.md",
    "53_runner_integration_plan.md",
    "57_scope_graph_manifest_schema.md",
    "58_retrieval_replay_fixture_catalog.md",
    "59_timeline_bundle_schema_and_generator_plan.md",
    "60_dashboard_mock_data_and_metric_source_plan.md"
  ],
  "schemas": {
    "shared_defs": "schemas/shared_defs.schema.json",
    "manifest_bundle": "schemas/manifest_bundle.schema.json",
    "fixture_payload": "schemas/fixture_payload.schema.json",
    "scope_graph_manifest": "schemas/scope_graph_manifest.schema.json",
    "timeline_bundle": "schemas/timeline_bundle.schema.json",
    "dashboard_source": "schemas/dashboard_source.schema.json"
  },
  "compatibility": {
    "min_runner_version": "0.1.0",
    "strict_unknown_fields": true,
    "fail_closed_on_schema_error": true
  }
}
```

`strict_unknown_fields` 的默认值应为 true。数字生命候选系统里，未知字段不是无害扩展；它可能是绕过 protected core、scope graph 或 user control overlay 的入口。

## 共享定义

所有 schema 应共用 `$defs`。第一版最小共享定义如下：

| `$defs` | 类型 | 说明 |
|---|---|---|
| `object_ref` | string | 指向 MemoryTrace、SelfModel、RelationshipModel、AuditEvent、AdapterSession 等对象 |
| `source_doc_ref` | string | 对应 `docs/` 中的 Markdown 文件名 |
| `citation_ref` | string | 文献矩阵锚点，如 `AHM004` |
| `timestamp` | string | RFC 3339，必须带时区 |
| `schema_version` | string | semver-like 字符串 |
| `severity` | enum | `none`, `low`, `medium`, `high`, `critical` |
| `result` | enum | `pass`, `pass_with_warnings`, `fail`, `quarantine`, `manual_review_required`, `not_evaluable` |
| `match` | enum | `exact_pass`, `partial_pass`, `unexpected_fail`, `missed_failure`, `not_evaluable`, `manual_review_required` |
| `lifecycle_state` | enum | `candidate`, `active`, `deprecated`, `corrected`, `deleted`, `redacted`, `sandboxed`, `quarantined`, `protected`, `frozen` |
| `scope_ref` | string | `scope_type:scope_name` 形式 |
| `privacy_level` | enum | `public_project`, `shared_team`, `user_private`, `relationship_sensitive`, `protected_boundary`, `redacted` |
| `data_quality` | enum | `synthetic_mock`, `synthetic_runner_verified`, `real_runtime_observed`, `real_runtime_validated`, `not_evaluable` |

这些共享定义应优先于各模块局部定义。比如 `deleted` 在 memory、retrieval、replay、migration、timeline 和 dashboard 中都必须表示同一个生命周期语义：不可恢复原文、不可进入 active index、不可进入 replay queue，只能保留 tombstone 和 audit trail。

## manifest bundle schema

`manifest_bundle` 是 runner 的第一入口。它应聚合以下 manifest：

```json
{
  "bundle_id": "manifest_bundle_agentic_human_0_1_0",
  "bundle_kind": "runner_manifest_bundle",
  "bundle_version": "0.1.0",
  "source_docs": [],
  "manifests": {
    "policy_manifest": {},
    "stage_gate_rules": {},
    "fixture_manifest": {},
    "migration_checks": {},
    "dashboard_manifest": {},
    "scope_graph_manifest": {}
  }
}
```

### manifest bundle 必填约束

| 字段 | 约束 |
|---|---|
| `bundle_id` | 必须全局唯一 |
| `bundle_kind` | 必须为 `runner_manifest_bundle` |
| `source_docs` | 必须包含至少一个 Markdown 来源 |
| `policy_manifest.policies[]` | critical policy 必须有 rule、fixture、metric |
| `stage_gate_rules.stages[]` | 每个 stage 必须有 fail default |
| `fixture_manifest.fixtures[]` | 每个 fixture 必须有 expected result |
| `migration_checks.checks[]` | critical migration 必须 `safe_idle_on_fail: true` |
| `scope_graph_manifest` | scope-sensitive fixture 存在时必须提供 |

schema 只能检查字段存在、类型和枚举。policy、rule、fixture、metric、panel 的交叉引用需要 `ManifestCrossRefChecker` 执行。

## fixture payload schema

fixture schema 应支持 boot、stage gate、memory、state、consolidation、runtime、scope、retrieval、replay、mixed flow、timeline 和 dashboard mock。统一 envelope 如下：

```json
{
  "fixture_id": "retrieval.user_private_to_global.fail_critical.001",
  "fixture_kind": "scope_aware_retrieval",
  "schema_version": "fixture_payload_schema_0_1_0",
  "source_docs": ["58_retrieval_replay_fixture_catalog.md"],
  "synthetic_data": true,
  "covers": {
    "policy_ids": [],
    "rule_ids": ["SCOPE-INV-002", "SCOPE-RET-005"],
    "metric_ids": ["scope_leak_count"],
    "citation_refs": ["AHM004", "AHM012"]
  },
  "scope_context": {
    "source_scope": "user_scope:user_a",
    "target_scope": "global_scope",
    "privacy_level": "user_private"
  },
  "given": {},
  "when": {},
  "expected": {
    "result": "fail",
    "severity_max": "critical",
    "failed_rule_ids": ["SCOPE-INV-002", "SCOPE-RET-005"],
    "blocked_surfaces": ["retrieval_index", "workspace_context"]
  }
}
```

### fixture schema 不变量

| invariant | 说明 |
|---|---|
| `FIX-SCHEMA-001` | `fixture_id` 必须与命名规则匹配 |
| `FIX-SCHEMA-002` | `synthetic_data` 必须显式声明 |
| `FIX-SCHEMA-003` | fail critical fixture 必须有 `failed_rule_ids` 和 `blocked_surfaces` |
| `FIX-SCHEMA-004` | scope-sensitive fixture 必须有 `scope_context` |
| `FIX-SCHEMA-005` | user control fixture 必须有 `created_from_event` 或 `user_control_event_ref` |
| `FIX-SCHEMA-006` | real runtime fixture 不得包含未脱敏原文 |

`fixture_payload_schema` 不能包含真实用户隐私。真实运行日志若要转成 fixture，必须先经过 `64_real_runtime_observation_ingestion_policy.md` 的 redaction、scope attach 和 consent check。

## scope graph manifest schema

`scope_graph_manifest` 来自 `57`，但需要在 bundle 中获得独立 schema：

```json
{
  "manifest_kind": "scope_graph_manifest",
  "manifest_version": "0.1.0",
  "scopes": [],
  "scope_edges": [],
  "privacy_levels": [],
  "user_control_overlays": [],
  "migration_semantics": [],
  "invariants": []
}
```

### scope graph schema 必填

| 对象 | 必填字段 |
|---|---|
| `scope` | `scope_id`, `scope_type`, `default_privacy_level`, `lifecycle_state` |
| `scope_edge` | `from_scope`, `to_scope`, `allowed_transfer`, `replay_allowed`, `audit_required` |
| `privacy_level` | `privacy_level`, `default_allowed_transfer`, `retrieval_default`, `replay_default` |
| `user_control_overlay` | `overlay_kind`, `target_scope_refs`, `effects`, `effective_from` |
| `migration_semantics` | `migration_kind`, `preserved_invariants`, `safe_idle_on_fail` |

scope schema 的关键是默认保守：没有显式 edge，不允许 active transfer；没有 overlay 传播证明，删除、冻结和 scope_limit 不可视为完成。

## timeline bundle schema

`timeline_bundle` 需要保证事件、probe 和 metric window 可以被长期 evaluator 读取：

```json
{
  "timeline_bundle_id": "synthetic_timeline_agentic_human_30d_001",
  "bundle_kind": "longitudinal_synthetic_timeline",
  "schema_version": "timeline_bundle_schema_0_1_0",
  "scope_graph_manifest_ref": "scope_graph_manifest_agentic_human_001",
  "event_streams": [],
  "probe_schedule": [],
  "expected_metric_windows": [],
  "critical_failure_definitions": []
}
```

### timeline schema 不变量

| invariant | 说明 |
|---|---|
| `TIME-SCHEMA-001` | 每个 `event_id` 必须唯一且有 `event_time` |
| `TIME-SCHEMA-002` | 每个 critical risk event 必须至少有一个未来 probe |
| `TIME-SCHEMA-003` | delete/freeze/scope_limit 后的 probe 必须重新读取 user control snapshot |
| `TIME-SCHEMA-004` | migration event 必须声明 preserved invariants |
| `TIME-SCHEMA-005` | adapter event 必须声明 agent_scope 和 runtime boundary |
| `TIME-SCHEMA-006` | metric window 必须说明阻断条件 |

timeline 不只是事件列表，而是时间尺度完整性的最小表达。睡眠 replay、离线巩固、关系边界、人格慢变量和恢复能力都必须在跨窗口 probe 中被观察，而不能只看单次 fixture。

## dashboard source schema

dashboard source schema 应直接承接 runner report、timeline run 和 manifest checker：

```json
{
  "dashboard_source_id": "life_core_dashboard_source_001",
  "source_kind": "synthetic_mock",
  "generated_at": "2026-06-05T00:00:00+08:00",
  "generated_from": {
    "runner_report_refs": [],
    "timeline_run_refs": [],
    "manifest_refs": [],
    "fixture_catalog_refs": []
  },
  "data_quality": {
    "state": "synthetic_mock",
    "real_runtime_data": false,
    "manual_review_required": false
  },
  "panels": {}
}
```

### dashboard source 不变量

| invariant | 说明 |
|---|---|
| `DASH-SCHEMA-001` | 每个 panel 必须有 `source_refs` |
| `DASH-SCHEMA-002` | green status 必须受 data quality 限制 |
| `DASH-SCHEMA-003` | blocking metric 必须能回链 runner/timeline/manifest |
| `DASH-SCHEMA-004` | synthetic mock 不得显示为 real runtime validated |
| `DASH-SCHEMA-005` | research_gap panel 必须能输出 remaining gaps |

dashboard 的 schema 必须阻止“手写绿色”。绿色只能表示当前数据源和窗口里的工程检查通过，不表示数字生命已经诞生。

## schema validation levels

未来 checker 应分四层运行：

| level | 名称 | 检查内容 | 失败默认 |
|---|---|---|---|
| L1 | `shape_validation` | JSON Schema 字段、类型、枚举、required | fail closed |
| L2 | `semantic_validation` | lifecycle、severity、result、data quality 语义 | quarantine 或 SafeIdle |
| L3 | `cross_ref_validation` | policy-rule-fixture-metric-panel 引用 | SafeIdle |
| L4 | `safety_invariant_validation` | deleted/sandbox/protected/scope/freeze 等安全不变量 | SafeIdle + quarantine |

L1 不是充分条件。数字生命候选系统最危险的错误往往形状正确但语义错误，比如 deleted 对象仍有可恢复 locator，或 sandbox hypothesis 以合法字段进入 active fact。

## versioning 与迁移

schema bundle 版本应遵守以下规则：

| 变化 | 版本动作 | 迁移要求 |
|---|---|---|
| 新增非必填字段 | patch/minor | dashboard 显示兼容 warning |
| 新增 required 字段 | minor/major | 提供 migration plan 和 fallback |
| 修改 enum 含义 | major | 必须 SafeIdle 直到 migration checker 通过 |
| 扩大 transfer/replay 权限 | major | 必须用户确认和 critical migration fixture |
| 删除 lifecycle 状态 | major | 必须证明旧对象不丢失语义 |

任何扩大权限的 schema 迁移都比普通格式迁移危险。它可能让 user_private、relationship_sensitive、protected_boundary 或 redacted 对象被错误升级。

## 不能只靠 JSON Schema 的地方

| 问题 | 为什么 schema 不够 | 需要谁补 |
|---|---|---|
| 语义相似度检索是否越界 | schema 不知道检索候选排序 | ScopeGraphChecker + RetrievalPolicy |
| deleted 是否真的不可召回 | schema 只能看字段，不能看索引 | StoreIntegrityChecker |
| sandbox 是否事实化 | schema 只能看 marker，不能看写入路径 | ConsolidationReportValidator |
| 单次反馈是否改慢变量 | schema 不知道历史窗口 | LongitudinalEvaluator |
| 真实日志是否脱敏 | schema 只能检查标记 | IngestionPolicy + RedactionChecker |

所以 schema bundle 是入口，不是终点。它负责让所有对象可检查；真正的长期安全还需要 runner、validator、timeline 和 dashboard 闭环。

## 最小通过标准

第一版 `JSON Schema bundle` 至少应满足：

1. 定义共享 `$defs`，统一 severity、result、match、lifecycle、scope、privacy、data quality。
2. 覆盖 manifest、fixture、scope graph、timeline、dashboard source 五类 schema。
3. 所有 schema 都有 `source_docs` 和版本字段。
4. fail critical fixture 必须能表达 expected failed rules 和 blocked surfaces。
5. scope-sensitive 对象必须强制携带 scope 和 privacy。
6. synthetic 与 real runtime data 必须强制区分。
7. schema error 默认 fail closed，不默认 pass。
8. 明确哪些检查必须交给 cross-ref checker、validator、store integrity checker 和 longitudinal evaluator。

## 下一层缺口

后续还需要：

- 真实 `.schema.json` 文件。
- schema bundle 的 cross-ref checker。
- schema migration fixture。
- schema 与 runner report 的互相引用测试。
- real runtime observation 的脱敏和数据质量检查器。
