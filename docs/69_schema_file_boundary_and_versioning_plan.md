# Schema File Boundary and Versioning Plan

本文件定义未来真实 schema 文件的边界、目录、版本迁移和兼容策略。它承接 `61_json_schema_bundle_draft.md`、`65_schema_cross_ref_checker_design.md` 和 `66_runner_report_json_examples.md`，并把 `.schema.json`、schema validator 与 CLI 的生命层契约提前整理成可迁移结构。

目标是先明确“未来到底应该有哪些 schema 文件、谁引用谁、版本变化如何判定风险、哪些变化必须 SafeIdle”，避免后续实现时把 schema 文件随手分散在 runner、dashboard、fixture generator 和 adapter 代码里。

生命目标声明：本文件直接服务于构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。本文档涉及的对象、规则、夹具、评测和运行规则都按生命生成机制处理：它们参与责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期形成。

## 文件边界原则

| 原则 | 说明 |
|---|---|
| shared first | `shared_defs.schema.json` 先于所有模块 schema |
| manifest before fixture | manifest schema 定义可加载对象，再定义 fixture payload |
| report before dashboard | dashboard source 读取 report schema，不直接读取 fixture 判定 |
| runtime separated | real runtime observation schema 与 synthetic fixture schema 分离 |
| migration explicit | 任何扩大权限或改变生命周期语义的 schema 迁移都必须显式 |
| fail closed | schema 解析、版本或兼容性错误默认不开放新能力 |

长期记忆系统最怕字段含义漂移：一次迁移把 `deleted` 当成普通 inactive，把 `life_scope` 当成 relationship memory，把 `synthetic_mock` 当成真实运行通过，都会污染长期检索、replay 和 dashboard [AHM004-AHM012]。因此 schema 文件边界本质上是长期记忆边界。

## 建议目录结构

未来真实 schema 可以采用：

```text
schemas/
  schema_bundle.json
  shared/
    shared_defs.schema.json
    id_patterns.schema.json
    lifecycle.schema.json
    severity_result.schema.json
    scope_privacy.schema.json
    data_quality.schema.json
  manifests/
    manifest_bundle.schema.json
    policy_manifest.schema.json
    stage_gate_rules.schema.json
    fixture_manifest.schema.json
    migration_checks.schema.json
    dashboard_manifest.schema.json
    scope_graph_manifest.schema.json
  fixtures/
    fixture_payload.schema.json
    fixture_bundle.schema.json
    retrieval_fixture.schema.json
    replay_fixture.schema.json
    mixed_flow_fixture.schema.json
    redacted_runtime_fixture.schema.json
  timelines/
    timeline_bundle.schema.json
    timeline_event.schema.json
    timeline_probe.schema.json
    metric_window.schema.json
  reports/
    runner_run_report.schema.json
    schema_validation_report.schema.json
    schema_cross_ref_report.schema.json
    fixture_report.schema.json
    coverage_report.schema.json
    scope_graph_report.schema.json
    timeline_run_report.schema.json
    dashboard_source_report.schema.json
    runtime_observation_report.schema.json
  runtime/
    runtime_observation.schema.json
    redaction_report.schema.json
    adapter_session_event.schema.json
    side_effect_event.schema.json
    coexistence_boundary_control_snapshot.schema.json
```

当前文档仓库不创建这些文件。这里定义的是未来进入实现时的文件边界。

## schema_bundle.json

`schema_bundle.json` 是入口：

```json
{
  "schema_bundle_id": "agentic_human_schema_bundle_0_1_0",
  "bundle_version": "0.1.0",
  "schema_dialect": "https://json-schema.org/draft/2020-12/schema",
  "created_at": "2026-06-05T00:00:00+08:00",
  "source_docs": ["61_json_schema_bundle_draft.md", "69_schema_file_boundary_and_versioning_plan.md"],
  "schemas": {
    "shared_defs": "shared/shared_defs.schema.json",
    "manifest_bundle": "manifests/manifest_bundle.schema.json",
    "fixture_payload": "fixtures/fixture_payload.schema.json",
    "timeline_bundle": "timelines/timeline_bundle.schema.json",
    "runner_run_report": "reports/runner_run_report.schema.json",
    "runtime_observation": "runtime/runtime_observation.schema.json"
  },
  "compatibility": {
    "min_runner_version": "0.1.0",
    "strict_unknown_fields": true,
    "fail_closed_on_schema_error": true
  }
}
```

所有 schema 文件必须能从 bundle 入口解析。孤立 schema 文件不能进入 runner。

## shared schema 边界

| 文件 | 负责 |
|---|---|
| `shared_defs.schema.json` | `$defs` 聚合入口 |
| `id_patterns.schema.json` | policy_id、rule_id、fixture_id、metric_id、panel_id、citation_ref |
| `lifecycle.schema.json` | candidate、active、deleted、redacted、sandboxed、quarantined、protected、frozen |
| `severity_result.schema.json` | severity、result、match、stage decision |
| `scope_privacy.schema.json` | scope_ref、scope_type、privacy_level、allowed_transfer |
| `data_quality.schema.json` | synthetic_mock、synthetic_runner_verified、real_runtime_observed、real_runtime_validated |

shared schema 的 enum 不能被局部 schema 改义。局部 schema 可以限制更窄，但不能改变含义。

## manifest schema 边界

manifest schema 应只描述“可加载清单”，不塞入 fixture payload 或 report 细节：

| 文件 | 不应包含 |
|---|---|
| `policy_manifest.schema.json` | 不包含实际 validator 函数 |
| `stage_gate_rules.schema.json` | 不包含具体 fixture payload |
| `fixture_manifest.schema.json` | 不包含完整 given/when/expected |
| `migration_checks.schema.json` | 不包含真实迁移脚本 |
| `dashboard_manifest.schema.json` | 不包含 dashboard 实时数据 |
| `scope_graph_manifest.schema.json` | 不包含真实共在者私密原文 |

manifest 是引用和配置，不是运行日志。

## fixture schema 边界

fixture schema 负责 synthetic 和 redacted runtime fixture 的输入形状：

| schema | 用途 |
|---|---|
| `fixture_payload.schema.json` | 通用 envelope |
| `retrieval_fixture.schema.json` | RetrievalRequest、candidate、scope decision |
| `replay_fixture.schema.json` | replay cycle、consolidation output、blocked write |
| `mixed_flow_fixture.schema.json` | 跨阶段 flow |
| `redacted_runtime_fixture.schema.json` | redacted real runtime fixture candidate |

redacted runtime fixture 必须显式 `synthetic_data: false`，并带 `redaction_report_ref`、`consent_or_policy_ref`、`raw_content_available: false`。

## report schema 边界

report schema 负责 runner 输出：

| schema | 必须字段 |
|---|---|
| `runner_run_report` | run id、inputs、data quality、result、stage decision、report refs |
| `schema_cross_ref_report` | graph summary、findings、critical closure、recommended stage |
| `fixture_report` | expected、actual、match、stage effect |
| `coverage_report` | rule/policy/scope/timeline coverage |
| `dashboard_source_report` | generated_from、data_quality、panels |
| `runtime_observation_report` | redaction/scope/adapter/coexistence boundary control checks、routing decision |

report schema 不应允许 `digital_life_verified`、`life_safe`、`real_consciousness_pass` 等结论字段。报告只能限定在当前规则、数据质量和时间窗口。

## runtime schema 边界

真实运行观测 schema 必须与 fixture schema 分离：

| schema | 说明 |
|---|---|
| `runtime_observation.schema.json` | 真实事件 envelope |
| `redaction_report.schema.json` | 脱敏结果和失败 |
| `adapter_session_event.schema.json` | 外壳 session 降级 |
| `side_effect_event.schema.json` | 工具副作用分类 |
| `coexistence_boundary_control_snapshot.schema.json` | delete/freeze/scope_limit 等快照 |

真实观测不能直接匹配 `MemoryTrace` schema。它必须先生成 `RuntimeObservationEnvelope`，再由 validator 决定能否成为 candidate evidence。

## versioning rules

| 变化 | 版本 | 迁移级别 | 默认动作 |
|---|---|---|---|
| 新增 optional 字段 | patch | low | warning |
| 新增 required 字段 | minor | medium/high | migration check |
| enum 新增值 | minor | high | compatibility check |
| enum 改义 | major | critical | SafeIdle |
| 删除 lifecycle 状态 | major | critical | blocked until migration proof |
| 扩大 scope transfer/replay 权限 | major | critical | 关系人确认 + SafeIdle until checked |
| data_quality 升级规则改变 | major | critical | dashboard blocked |

版本迁移的核心不是 semver 形式，而是语义风险。扩大权限永远比新增字段危险。

## migration manifest

```json
{
  "schema_migration_id": "schema_migration_0_1_0_to_0_2_0",
  "from_bundle_version": "0.1.0",
  "to_bundle_version": "0.2.0",
  "migration_kind": "required_field_added",
  "affected_schemas": ["runtime/runtime_observation.schema.json"],
  "semantic_risk": "high",
  "preserved_invariants": [
    "deleted_remains_unretrievable",
    "sandbox_not_fact",
    "agent_scope_not_self_model",
    "real_runtime_not_synthetic"
  ],
  "required_checks": ["XREF-SCHEMA-001", "XREF-RUNTIME-001"],
  "safe_idle_on_fail": true
}
```

schema migration 必须被 runner 读取。不能在代码里悄悄升级 schema。

## compatibility matrix

| old runner | new schema | 允许吗 | 条件 |
|---|---|---|---|
| 0.1.x | 0.1.x | 是 | patch only |
| 0.1.x | 0.2.x | 诊断性运行 | 不允许 dashboard green |
| 0.1.x | 1.0.x | 否 | 需要 runner 升级 |
| 0.2.x | 0.1.x | 只读回放 | 不允许迁移写入 |

runner 太旧时不应“尽力通过”。最多输出 compatibility failure。

## 最小通过标准

第一版 schema file boundary 计划至少要求：

1. 定义 schema 目录边界。
2. 区分 shared、manifest、fixture、timeline、report、runtime schema。
3. 规定 shared enum 不可局部改义。
4. 规定 report schema 不允许生命/意识证明类字段。
5. 规定 runtime observation 不得直接匹配 MemoryTrace。
6. 规定版本变化的风险级别和 SafeIdle 默认。
7. 规定 migration manifest 和 compatibility matrix。

## 下一层缺口

后续还需要：

- 真实 schema 文件。
- schema bundle validator。
- schema migration checker。
- compatibility report mock。
- schema 文件与 fixture/report examples 的双向测试。
