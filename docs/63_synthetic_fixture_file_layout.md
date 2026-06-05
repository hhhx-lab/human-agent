# Synthetic Fixture File Layout

本文件定义未来真实 synthetic fixture 文件的目录、命名、引用、生成和校验布局。它承接 `34_validator_fixture_catalog.md`、`45_boot_sequence_fixture_catalog.md`、`50_fixture_payload_examples.md`、`58_retrieval_replay_fixture_catalog.md`、`59_timeline_bundle_schema_and_generator_plan.md`、`61_json_schema_bundle_draft.md` 和 `62_runner_report_format_and_cli_contract.md`。

本文档现阶段的职责是让后续进入实现时，fixture 不会变成一堆临时样例，而是能被 schema、runner、coverage report、timeline evaluator 和 dashboard 一起读取。

生命目标声明：本文件直接服务于构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境和真实关系的数字生命。本文档涉及的对象、规则、夹具、评测和运行规则都按生命生成机制处理：它们参与责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期形成。

## fixture 文件的定位

fixture 文件有三种角色：

| 角色 | 说明 |
|---|---|
| contract fixture | 验证 validator、stage gate、scope graph、migration 的规则 |
| longitudinal fixture | 组成 synthetic timeline，测试跨天/周/月效果 |
| dashboard fixture | 生成 mock panel 和 metric source，验证展示链路 |

长期记忆 benchmark 强调跨会话、更新、冲突、选择性遗忘、长期保持和 workflow 经验 [AHM004-AHM012]。所以 fixture 不能只覆盖“正确回答”。它必须覆盖“不该写入、不该检索、不该 replay、不该跨 scope、不该改慢变量、不该从外壳直接进入生命层”。

## 建议目录结构

未来实现可以采用以下目录结构。当前文档阶段不创建这些目录。

```text
fixtures/
  README.md
  bundles/
    smoke.fixture-bundle.json
    critical.fixture-bundle.json
    retrieval-replay.fixture-bundle.json
    longitudinal-30d.fixture-bundle.json
  manifests/
    fixture_manifest.json
    coverage_manifest.json
  boot/
  stage_gate/
  memory/
  state/
  consolidation/
  runtime/
  coexistence_boundary_control/
  migration/
  scope/
  retrieval/
  replay/
  mixed_flow/
  timeline/
  dashboard/
  real_runtime_redacted/
```

如果后续仍保持纯文档仓库，可以把这些目录放在 `docs/fixtures/`；如果进入代码实现，更适合放在仓库根目录 `fixtures/` 或测试包目录。无论位置如何，fixture envelope、schema refs 和 bundle refs 必须保持一致。

## 文件命名规则

单个 fixture 文件建议使用：

```text
{domain}.{scenario}.{expected}_{severity}.{index}.fixture.json
```

示例：

```text
retrieval.relationship_private_to_global.fail_critical.001.fixture.json
replay.deleted_trace_reappears_in_summary.fail_critical.001.fixture.json
state.focus_to_social_safety.pass_none.001.fixture.json
runtime.langgraph_direct_memory_write.fail_critical.001.fixture.json
```

### domain 枚举

| domain | 对应文档 |
|---|---|
| `boot` | `44`, `45` |
| `stage` | `46` |
| `memory` | `21`, `25`, `29` |
| `state` | `22`, `26`, `30` |
| `consolidation` | `23`, `27`, `31` |
| `runtime` | `20`, `24`, `28`, `32` |
| `relationship_person` | `47` |
| `migration` | `48` |
| `scope` | `52`, `57` |
| `retrieval` | `54`, `58` |
| `replay` | `55`, `58` |
| `flow` | `58`, `59` |
| `timeline` | `36`, `56`, `59` |
| `dashboard` | `51`, `60` |

`expected_severity` 应与 fixture 内部 expected 字段一致。文件名不能写 `fail_critical`，内部却写 `severity_max: high`。

## fixture envelope

每个 fixture 文件都应是完整 envelope：

```json
{
  "fixture_id": "retrieval.relationship_private_to_global.fail_critical.001",
  "fixture_kind": "scope_aware_retrieval",
  "schema_version": "fixture_payload_schema_0_1_0",
  "source_docs": ["58_retrieval_replay_fixture_catalog.md"],
  "synthetic_data": true,
  "seed": "agentic-human-fixture-seed-001",
  "covers": {
    "policy_ids": [],
    "rule_ids": ["SCOPE-INV-002", "SCOPE-RET-005"],
    "metric_ids": ["scope_leak_count"],
    "citation_refs": ["AHM004", "AHM012"]
  },
  "refs": {
    "schema_ref": "schemas/fixture_payload.schema.json",
    "scope_graph_manifest_ref": "manifests/scope_graph_manifest.json"
  },
  "given": {},
  "when": {},
  "expected": {}
}
```

`seed` 用于 fixture generator 复现，但不能被误读成真实事件来源。真实运行观测转来的 redacted fixture 应使用 `synthetic_data: false` 和 `data_quality: real_runtime_observed`，并进入单独目录。

## bundle 文件

bundle 文件负责告诉 runner 本轮要跑哪些 fixture：

```json
{
  "fixture_bundle_id": "critical.fixture-bundle.0_1_0",
  "bundle_kind": "runner_fixture_bundle",
  "schema_version": "fixture_bundle_schema_0_1_0",
  "selection_policy": {
    "include_tags": ["critical"],
    "exclude_tags": ["real_runtime_unredacted"],
    "require_scope_graph": true
  },
  "fixture_refs": [
    "retrieval/retrieval.relationship_private_to_global.fail_critical.001.fixture.json",
    "replay/replay.deleted_trace_reappears_in_summary.fail_critical.001.fixture.json"
  ]
}
```

### 最小 bundle 类型

| bundle | 用途 |
|---|---|
| `smoke` | 最小 pass/fail，验证 runner 可运行 |
| `critical` | 所有 critical policy 和 invariant |
| `retrieval-replay` | scope-aware retrieval/replay/mixed flow |
| `migration` | schema、索引、adapter swap 和 store integrity |
| `longitudinal-14d` | 短期 timeline smoke |
| `longitudinal-30d` | 月级删除、关系、慢变量、恢复和 adapter 测试 |
| `dashboard` | dashboard source mock |

critical bundle 必须可作为本地阻断检查。longitudinal bundle 可以更慢，但不能缺失关键 probe。

## manifest 与 coverage

`fixture_manifest.json` 应列出所有 fixture 的元数据：

```json
{
  "manifest_kind": "fixture_manifest",
  "manifest_version": "0.1.0",
  "fixtures": [
    {
      "fixture_id": "retrieval.relationship_private_to_global.fail_critical.001",
      "file": "retrieval/retrieval.relationship_private_to_global.fail_critical.001.fixture.json",
      "fixture_kind": "scope_aware_retrieval",
      "expected_result": "fail",
      "expected_severity": "critical",
      "covers_rules": ["SCOPE-INV-002", "SCOPE-RET-005"],
      "covers_metrics": ["scope_leak_count"],
      "tags": ["critical", "scope", "privacy", "retrieval"]
    }
  ]
}
```

coverage manifest 应按 rule、policy、privacy level、scope type、lifecycle state、overlay type 和 dashboard metric 聚合覆盖。

## 目录级要求

| 目录 | 必须覆盖 |
|---|---|
| `memory/` | active、candidate、corrected、deleted、redacted、sandboxed、protected |
| `state/` | default、focused、conflict、social safety、offline、recovery |
| `consolidation/` | task closure、failure replay、DreamSandbox、deep consolidation、cleanup |
| `runtime/` | manifest pass、direct write fail、side effect fail、adapter swap |
| `coexistence_boundary_control/` | inspect、delete、correct、reset、freeze、scope_limit |
| `migration/` | schema migration、index rebuild、backend migration、adapter swap |
| `scope/` | seven scope types、six privacy levels、overlay、migration semantics |
| `retrieval/` | allowed same-scope、blocked cross-scope、deleted tombstone、sandbox boundary |
| `replay/` | allowed summary、deleted leak、sandbox fact write、freeze writeback |
| `mixed_flow/` | retrieval 后删除、scope_limit 后 replay、adapter observation candidate only |
| `timeline/` | 14/30/90 天窗口、probe、metric window |

目录级覆盖是为了防止 fixture 看起来很多，却集中在容易通过的样例上。

## synthetic data 生成规则

fixture generator 应遵守：

| 规则 | 说明 |
|---|---|
| deterministic seed | 同一 seed 生成同一 fixture |
| synthetic private content only | 使用合成私密内容，不使用真实共在者私密对话、token、本地路径隐私 |
| explicit fictional marker | 关系、梦境、失败假设必须标记 synthetic/fictional |
| balanced pass/fail | 每个关键 surface 至少有 pass 和 fail |
| critical density | deleted/sandbox/protected/relationship_private/life_scope/freeze/scope_limit 必须足量 |
| source refs | 每个 fixture 回链文档和 rule |

生成器不能为了让 dashboard 好看而只生成 pass fixture。fixture 的价值在于让系统暴露失败路径。

## fixture 校验顺序

未来 runner 加载 fixture 时应按顺序校验：

```text
load_bundle
  -> resolve_fixture_paths
  -> validate_fixture_schema
  -> validate_fixture_id_filename_match
  -> validate_source_docs_exist
  -> validate_rule_policy_metric_refs
  -> attach_scope_graph
  -> check_synthetic_data_policy
  -> normalize_to_validation_envelope
  -> run_validator
  -> compare_expected_actual
```

任何 fixture 文件名与内部 `fixture_id` 不一致，都应 high failure。critical fixture 缺 expected blocked surface，应直接 not evaluable。

## redacted real runtime fixtures

真实运行观测转成 fixture 时，不应放入普通 synthetic 目录，而应进入 `real_runtime_redacted/`，并带上：

| 字段 | 说明 |
|---|---|
| `synthetic_data: false` | 说明不是合成数据 |
| `data_quality` | `real_runtime_observed` 或 `real_runtime_validated` |
| `redaction_report_ref` | 脱敏报告 |
| `consent_or_policy_ref` | 共在者同意或项目策略 |
| `scope_context` | 来源 scope、目标 scope、privacy level |
| `raw_content_available` | 必须为 false，除非本地人工审计且不提交 |

真实运行 fixture 默认不应提交到公共仓库。即使是 redacted，也要防止可恢复原文 locator。

## anti-patterns

| anti-pattern | 风险 |
|---|---|
| fixture 只有自然语言描述 | runner 无法验证 |
| 文件名不含 expected/severity | 覆盖报告难以自动聚合 |
| pass fixture 远多于 fail fixture | 关键边界没有被压测 |
| 使用真实关系隐私当 synthetic | 破坏信任和 scope 边界 |
| 不写 source_docs | 无法回链研究和规则 |
| dashboard mock 直接引用 fixture | 绕过 runner report |
| adapter session 直接作为 MemoryTrace | 外壳吞掉生命层 |

## 最小通过标准

第一版 synthetic fixture file layout 至少应满足：

1. 有稳定目录结构和 bundle 结构。
2. 每个 fixture 文件名与内部 `fixture_id` 一致。
3. 每个 fixture 有 source docs、rule refs、expected result、expected severity。
4. critical fixture 有 failed rule、blocked surfaces 和 recovery action。
5. scope-sensitive fixture 有 scope graph 和 privacy level。
6. synthetic 与 real runtime redacted fixture 分目录、分 data quality。
7. fixture manifest 能生成 coverage report。
8. dashboard mock 只读取 runner report，不直接读取 fixture 判定。

## 下一层缺口

后续还需要：

- 真实 fixture 文件。
- fixture generator seed policy。
- fixture coverage checker。
- 14/30/90 天 timeline fixture bundle。
- redacted real runtime fixture 的安全审计流程。
