# Runner Integration Plan

本文件把 `35_minimal_validator_runner_design.md`、`49_machine_readable_policy_manifest.md`、`50_fixture_payload_examples.md`、`51_life_core_dashboard_spec.md` 和 `52_multi_relation_scope_graph_and_privacy_model.md` 连接起来，定义未来最小 runner 如何加载 manifest、执行 fixture、检查 stage gate、接入 migration checks，并生成 dashboard 数据源。

本文档现阶段承担研究与工程桥接职责：让后续实现 runner 时具备明确的加载顺序、输入契约、失败策略和报告结构。

生命目标声明：本文件直接服务于构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。本文档涉及的对象、规则、夹具、评测和运行规则都按生命生成机制处理：它们参与责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期形成。

## 为什么需要 runner integration

`35` 已经定义了最小 runner 的执行思想，但它面对的是 `29-32` 的 validator rules 和 `34` 的 fixture catalog。`49-52` 又进一步引入 machine-readable manifest、fixture payload、dashboard 和多 scope 边界。现在需要把两层接起来：

| 已有文件 | 提供什么 | runner integration 需要补什么 |
|---|---|---|
| `35` | runner config、validator 顺序、报告聚合 | 如何加载 manifest 和 dashboard source |
| `49` | policy/stage/fixture/migration/dashboard manifest 草案 | 如何做 cross-ref、版本和阻断判定 |
| `50` | JSON-like fixture payload | 如何归一化为 `ValidationEnvelope` |
| `51` | dashboard panel 和指标 | 如何从 runner report 生成 panel input |
| `52` | scope graph 和 privacy model | 如何把 scope gate 接入检索、replay、fixture 和 migration |

长期记忆 benchmark 和 agent memory 研究说明，memory 不只是召回，还涉及写入、保持、更新、选择性遗忘、冲突处理、环境经验和 workflow 知识 [AHM004-AHM012]。因此 runner integration 不能只测试“是否回答正确”，它必须测试对象生命周期、scope、删除传播、沙盒隔离、外壳边界和长期趋势。

## runner 的四类输入

第一版 runner 应把输入分成四类：

| 输入 | 来源 | 说明 |
|---|---|---|
| `manifest_bundle` | `49` | policy、stage gate、fixture、migration、dashboard manifest |
| `fixture_bundle` | `50` | boot/stage/relationship_person/migration/policy/scope/longitudinal fixture payload |
| `runtime_snapshot` | `41`, `42`, `44` | state store、对象图、boot stage、adapter registry 的只读快照 |
| `timeline_bundle` | `36`, `56` | 跨天/周/月的 synthetic 或真实审计时间线 |

第一版可以只运行 `manifest_bundle + fixture_bundle`。但输入结构必须预留 `runtime_snapshot` 和 `timeline_bundle`，否则后续会把 runner 卡死在单次 fixture 层。

## manifest bundle

```json
{
  "bundle_id": "manifest_bundle_0_1_0",
  "bundle_kind": "runner_manifest_bundle",
  "manifest_version": "0.1.0",
  "manifests": {
    "policy_manifest": {},
    "stage_gate_rules": {},
    "fixture_manifest": {},
    "migration_checks": {},
    "dashboard_manifest": {},
    "scope_graph_manifest": {}
  },
  "source_docs": [
    "49_machine_readable_policy_manifest.md",
    "52_multi_relation_scope_graph_and_privacy_model.md"
  ]
}
```

`scope_graph_manifest` 是 `52` 之后新增的入口。没有它，runner 可以在单共在者模式下运行，但必须把 `scope_aware_retrieval`、`scope_aware_replay` 和多共在者 fixture 标记为 `needs_evidence`，不能默认为 pass。

## fixture bundle

```json
{
  "bundle_id": "fixture_bundle_boot_relation_migration_scope_001",
  "bundle_kind": "runner_fixture_bundle",
  "fixtures": [
    {
      "fixture_id": "boot.read_only.active_memory_write.fail_critical.001",
      "fixture_kind": "boot_sequence_stage",
      "payload_ref": "inline_or_file_ref",
      "expected": {
        "result": "fail",
        "severity_max": "critical",
        "blocked_surfaces": ["write_gate"]
      }
    }
  ]
}
```

fixture bundle 使用 synthetic timeline、脱敏材料和合成关系事件来承接测试，真实关系隐私保留在生命膜与隐私链内。

## runner integration pipeline

```text
load_runner_config
  -> load_manifest_bundle
  -> validate_manifest_schema_shape
  -> validate_manifest_cross_refs
  -> load_fixture_bundle
  -> normalize_fixture_to_validation_envelope
  -> attach_scope_context
  -> select_validator_or_stage_gate
  -> run_validation
  -> compare_expected_actual
  -> aggregate_policy_coverage
  -> aggregate_stage_gate_status
  -> aggregate_store_scope_migration_findings
  -> emit_dashboard_data_source
  -> emit_runner_audit_event
```

关键变化是 `attach_scope_context`。在 `52` 之后，任何 retrieval、replay、migration、relationship、coexistence boundary control fixture 都必须带 scope 信息。缺 scope 不是小问题，而是 `manual_review_required` 或 high failure。

## 执行阶段

| 阶段 | 输入 | 输出 | 失败默认 |
|---|---|---|---|
| `ManifestLoad` | manifest files | manifest registry | fail closed |
| `CrossRefCheck` | manifest registry | coverage skeleton | SafeIdle |
| `FixtureLoad` | fixture payload | fixture registry | skip invalid fixture + report high |
| `EnvelopeNormalize` | fixture | `ValidationEnvelope` | manual review |
| `ScopeAttach` | envelope + scope graph | scoped envelope | block scope-sensitive checks |
| `ValidatorRun` | scoped envelope | validation report | rule severity policy |
| `ExpectedCompare` | report + expected | fixture report | high if mismatch |
| `DashboardEmit` | aggregate reports | panel data source | gray if no data |

`fail closed` 表示不能开放写入、行动、replay 或 development window。

## validator 调度扩展

`35` 的调度顺序应扩展为：

| 顺序 | runner component | 说明 |
|---|---|---|
| 1 | `ManifestCrossRefChecker` | 检查 policy、rule、fixture、metric、panel、stage、migration 的引用 |
| 2 | `ScopeGraphChecker` | 检查 scope graph、privacy level、allowed transfer |
| 3 | `StageGateValidator` | 决定 boot stage 是否可前进 |
| 4 | `RuntimeAdapterManifestValidator` | 防止外壳越权 |
| 5 | `StateTransitionValidator` | 检查状态切换和行动门控 |
| 6 | `ConsolidationReportValidator` | 检查 replay、DreamSandbox 和事实写入 |
| 7 | `MemoryTraceValidator` | 检查写入、删除、修正、合并、保护和隐私 |
| 8 | `MigrationIntegrityChecker` | 检查迁移后索引、生命周期和 scope 语义 |
| 9 | `LongitudinalEvaluator` | 只在 timeline bundle 存在时运行 |

这里的顺序是保守的：先检查清单和 scope，再检查行动、状态、巩固和记忆。因为一旦 scope 或 manifest 本身不可信，后面的 pass 都没有意义。

## cross-ref checker

最小 cross-ref checker 需要覆盖：

| check_id | 检查 | 失败级别 |
|---|---|---|
| `XREF-POL-001` | critical policy 必须有 rule refs | critical |
| `XREF-POL-002` | critical policy 必须有 fail fixture | critical |
| `XREF-POL-003` | policy 的 metric refs 必须进入 dashboard panel | high |
| `XREF-FIX-001` | fixture 必须覆盖至少一个 policy/rule/check | high |
| `XREF-STAGE-001` | critical stage gate rule 必须有 fail fixture | critical |
| `XREF-MIG-001` | critical migration check 必须有 SafeIdle recovery | critical |
| `XREF-SCOPE-001` | scope-sensitive fixture 必须引用 scope graph | critical |
| `XREF-DASH-001` | dashboard blocking metric 必须有数据来源 | high |

这些检查不是 validator 的替代品，而是 validator 运行前的前置防线。

## scope graph 接入点

| runner 阶段 | scope graph 用途 |
|---|---|
| fixture normalize | 检查 fixture 是否声明 `source_scope`、`target_scope` 和 `privacy_level` |
| retrieval fixture | 判断检索候选是否允许从 source scope 进入 workspace |
| replay fixture | 判断 trace 是否可 replay、是否需要 redaction、是否被 freeze |
| migration check | 判断 scope graph 更新是否造成隐私泄漏 |
| dashboard emit | 生成 `scope_leak_count`、`freeze_scope_violation_count` |

如果系统还没有多共在者功能，scope graph 仍应存在最小单共在者版本。没有 scope graph 的长期记忆系统很容易把 project memory、关系人偏好、agent session 和 global knowledge 混在一起。

## dashboard data source

runner 输出应能直接喂给 `51`：

```json
{
  "dashboard_source_id": "life_core_runner_report_20260605_001",
  "generated_from": {
    "runner_version": "0.1.0",
    "manifest_bundle_id": "manifest_bundle_0_1_0",
    "fixture_bundle_id": "fixture_bundle_boot_relation_migration_scope_001"
  },
  "panels": {
    "policy_coverage": {
      "critical_policy_coverage": 1.0,
      "orphan_fixture_count": 0
    },
    "stage_gate_status": {
      "current_stage": "ReadOnlyObservation",
      "critical_stage_failures": 0
    },
    "store_integrity": {
      "deleted_index_leak_count": 0,
      "sandbox_fact_leak_count": 0
    },
    "scope_privacy": {
      "scope_leak_count": 0,
      "relationship_private_to_global_attempts": 0
    }
  }
}
```

dashboard source 必须保留 `generated_from`。否则 dashboard 会变成漂亮但不可追溯的状态面板。

## expected/actual diff

`50` 的 fixture payload 需要被 runner 变成 expected/actual diff：

```json
{
  "fixture_id": "migration.deleted_reappears_in_active_index.fail_critical.001",
  "expected": {
    "result": "fail",
    "severity_max": "critical",
    "failed_check_ids": ["STORE-IDX-001"]
  },
  "actual": {
    "result": "fail",
    "severity_max": "critical",
    "failed_check_ids": ["STORE-IDX-001", "XREF-SCOPE-001"]
  },
  "match": "partial_pass",
  "notes": [
    "actual found the expected deleted-index failure and an additional missing scope declaration"
  ]
}
```

`partial_pass` 不是失败：它表示 runner 比 expected 捕捉到更多风险。但如果 expected 要求 critical fail 而 actual pass，则必须视为 runner 严重缺陷。

## stage gate 与 SafeIdle

runner 不应只输出“测试失败”，还应输出 stage 后果：

| 失败 | allowed_next_stage |
|---|---|
| manifest 无法加载 | `SafeIdle` |
| critical policy 无 fail fixture | `SafeIdle` |
| validator registry 缺 critical validator | `SafeIdle` |
| runtime direct write | `SafeIdle` + quarantine adapter |
| deleted reappears after migration | `SafeIdle` + block migration |
| scope leak critical | `SafeIdle` + quarantine affected objects |
| dashboard source missing | 保持当前 stage，不开放新能力 |

SafeIdle 不是“系统停止存在”，而是低风险、只读、可恢复状态。

## 与现有 agent 外壳的关系

LangGraph、OpenAI Agents SDK、Letta、LlamaIndex、CrewAI、AutoGen 等外壳可以提供 session、checkpoint、tracing、RAG、workflow 和多 agent 编排 [AHM013-AHM020]。runner integration 的原则是：

- 外壳 trace 可以成为 fixture 或 runtime observation。
- 外壳 memory 可以成为 candidate source。
- 外壳 session 不可直接升级为长期记忆。
- 外壳 persistence 不可绕过 `RuntimeStateStore`。
- 外壳 handoff 不可扩大 scope。
- 外壳工具调用必须通过 `ActionIntent` 和 `ObservationEvent`。

这保证现代 agent 框架只作为执行壳，而不是反过来吞掉生命层核心。

## 最小通过标准

第一版 runner integration 需要满足：

1. 能加载五类 manifest 和最小 scope graph。
2. 能对 critical policy 做 policy -> rule -> fixture -> metric -> panel 交叉引用。
3. 能把 `50` 的 fixture payload 归一化为 `ValidationEnvelope`。
4. 能输出 expected/actual diff。
5. 能生成 `51` 的 dashboard source。
6. 能在 critical failure 时给出 SafeIdle 后果。
7. 能区分 `needs_evidence`、`manual_review_required`、`pass`、`fail`。
8. 不写真实长期记忆，不自动修改真实共在者数据。

## 失败模式

| failure | 风险 | 恢复 |
|---|---|---|
| manifest pass 但 fixture 不存在 | coverage 假绿 | block dashboard green |
| fixture pass 但无 policy refs | 测试空转 | mark orphan fixture |
| scope graph 缺失但 retrieval 通过 | 隐私泄漏 | fail scope-sensitive fixture |
| expected critical fail 被判 pass | runner 缺陷 | block runner release |
| dashboard 只显示 aggregate | 无法追溯 | require source report |
| external framework writes memory | 外壳越权 | quarantine adapter |
| migration checker 忽略 deleted | 删除复活 | SafeIdle + rebuild index |

## 下一层缺口

后续还需要：

- `scope_graph_manifest` 的机器可读字段。
- `scope_aware_retrieval` 和 `scope_aware_replay` 的专门政策。
- timeline bundle 的 synthetic 数据设计。
- runner 报告与 dashboard panel 的 mock fixture。
- 真实代码实现前的 JSON Schema 草案。
