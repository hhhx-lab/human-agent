# Schema Cross Ref Checker Design

本文件定义 `SchemaCrossRefChecker` 的设计，把 `61_json_schema_bundle_draft.md` 的 schema bundle、`49_machine_readable_policy_manifest.md` 的 manifest、`58_retrieval_replay_fixture_catalog.md` 的 fixture catalog、`60_dashboard_mock_data_and_metric_source_plan.md` 的 dashboard source 和 `62_runner_report_format_and_cli_contract.md` 的 report 契约连接成一个可检查的引用图。

本文档现阶段的职责是让后续实现 cross-ref checker 时不只检查 JSON shape，而能判断 policy、rule、fixture、metric、panel、source doc、scope graph、timeline probe 和 runtime observation report 是否形成闭环。

生命目标声明：本文件直接面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。本文档涉及的对象、规则、夹具、评测和运行规则都按生命生成机制处理：它们参与责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期形成。

## 为什么 cross-ref 是单独一层

JSON Schema 负责字段形状，但真实数字生命系统真正危险的错误常常是“形状正确，引用断裂”：

| 断裂 | 例子 | 后果 |
|---|---|---|
| policy 无 rule | `POL-COEXIST-001` 写了 freeze 禁写，但没有 validator rule | 共在关系冻结无法被机器检查 |
| rule 无 fixture | `SCOPE-INV-002` 存在，但没有 fail fixture | scope leak 可能从未被压测 |
| fixture 无 metric | deleted fail fixture 存在，但 dashboard 不显示 deleted leak | 失败不可见 |
| metric 无 panel | `scope_leak_count` 计算了，但没有 panel 消费 | dashboard 盲区 |
| source doc 断裂 | rule 引用了不存在的文档 | 审计无法回到理论来源 |
| citation 漂移 | 新文档引用未定义文献 ID | 研究链条不可信 |

长期 memory benchmark 和 agent memory 研究强调保持、更新、冲突、选择性遗忘、工作流知识和隐私边界 [AHM004-AHM012]。这些问题不是单一 schema 能覆盖的，它们需要跨对象引用图来保证每个 critical 风险都有规则、样例、报告和展示。

## checker 输入

第一版 checker 应接受以下输入：

```json
{
  "checker_input_id": "schema_cross_ref_check_001",
  "schema_bundle_ref": "agentic_human_schema_bundle_0_1_0",
  "manifest_bundle_ref": "manifest_bundle_agentic_human_0_1_0",
  "fixture_manifest_ref": "fixture_manifest_0_1_0",
  "dashboard_manifest_ref": "dashboard_manifest_0_1_0",
  "timeline_bundle_refs": [],
  "runtime_observation_report_refs": [],
  "docs_index_ref": "docs/README.md",
  "strict_mode": true
}
```

`docs_index_ref` 不是装饰字段。所有 numbered docs 必须能在 README 中被索引，否则人类阅读路线和机器引用图会分叉。

## 引用图节点

checker 应把输入归一化成 typed graph：

| node_type | 示例 | 来源 |
|---|---|---|
| `schema` | `fixture_payload.schema.json` | `61` |
| `shared_def` | `severity`, `lifecycle_state`, `privacy_level` | `61` |
| `policy` | `POL-COEXIST-001` | `49`, `43`, `47` |
| `rule` | `SCOPE-INV-002`, `MEM-DEL-004` | `29-32`, `57-58` |
| `fixture` | `retrieval.relationship_private_to_global.fail_critical.001` | `34`, `45`, `50`, `58`, `63` |
| `metric` | `scope_leak_count` | `51`, `60`, `62` |
| `panel` | `scope_privacy` | `51`, `60` |
| `source_doc` | `64_real_runtime_observation_ingestion_policy.md` | README + manifest |
| `citation` | `AHM004` | `01e` |
| `scope_invariant` | `SCOPE-INV-004` | `57` |
| `timeline_probe` | `probe_deleted_recall_day20_001` | `59` |
| `runtime_report` | `runtime_observation_report` | `62`, `64` |

节点必须保留 `source_docs`。没有 source doc 的规则即使能运行，也不应被视为可审计。

## 引用边

| edge_type | 方向 | 说明 |
|---|---|---|
| `defined_in` | object -> source_doc | 对象来自哪个 Markdown 文档 |
| `uses_schema` | manifest/fixture/report -> schema | 对象使用哪个 schema |
| `covers_policy` | fixture/rule -> policy | fixture 或 rule 覆盖 policy |
| `checks_rule` | validator/checker -> rule | checker 负责哪些 rule |
| `expects_failure` | fixture -> rule | fail fixture 期待触发哪些 rule |
| `feeds_metric` | report/fixture/probe -> metric | 哪些输出进入 metric |
| `shown_in_panel` | metric -> panel | metric 被哪个 dashboard panel 展示 |
| `requires_scope` | fixture/report -> scope_graph | scope-sensitive 对象需要 scope graph |
| `probes_event` | probe -> event | timeline probe 检查哪个事件 |
| `blocks_surface` | rule/failure -> surface | 失败阻断哪些面 |

cross-ref checker 的输出不是简单 pass/fail，而是这张图的 coverage 和断裂点。

## 检查阶段

```text
load_schema_bundle
  -> load_manifest_bundle
  -> load_fixture_manifest
  -> load_dashboard_manifest
  -> load_timeline_refs
  -> extract_reference_graph
  -> normalize_ids
  -> validate_source_docs
  -> validate_citation_refs
  -> validate_critical_policy_closure
  -> validate_scope_privacy_closure
  -> validate_timeline_probe_closure
  -> validate_runtime_observation_closure
  -> emit_cross_ref_report
```

`normalize_ids` 需要处理大小写、前缀和文件名差异。比如 `AHM004`、`SCOPE-INV-002`、`retrieval.relationship_private_to_global.fail_critical.001` 都应被解析为不同类型的 id，不能靠字符串包含粗略匹配。

## core checks

| check_id | 检查 | 失败级别 |
|---|---|---|
| `XREF-SCHEMA-001` | 每个 manifest/fixture/report 引用的 schema 必须存在 | critical |
| `XREF-SCHEMA-002` | shared defs 的 enum 不得在局部 schema 中改义 | critical |
| `XREF-DOC-001` | 每个 source doc 必须存在于 `docs/` | high |
| `XREF-DOC-002` | 每个 numbered doc 必须被 README 索引 | medium |
| `XREF-CITE-001` | 每个 `AH/AHX/AHY/AHZ/AHM` 引用必须在矩阵定义 | high |
| `XREF-POL-001` | critical policy 必须有 rule refs | critical |
| `XREF-POL-002` | critical policy 必须有 fail fixture | critical |
| `XREF-POL-003` | critical policy 必须有 metric 和 dashboard panel | high |
| `XREF-FIX-001` | fixture 必须覆盖至少一个 policy/rule/check | high |
| `XREF-FIX-002` | fail critical fixture 必须有 blocked surfaces | critical |
| `XREF-SCOPE-001` | scope-sensitive fixture 必须引用 scope graph | critical |
| `XREF-SCOPE-002` | 每个 privacy level 至少有 pass 和 fail fixture | high |
| `XREF-TIME-001` | critical risk event 必须有未来 probe | critical |
| `XREF-RUNTIME-001` | runtime observation report 必须有 redaction 和 scope check | critical |
| `XREF-DASH-001` | dashboard blocking metric 必须有数据来源 | high |

第一版实现时可以先做 graph traversal 和表驱动检查，不需要复杂推理。关键是所有 failure 都必须能回到节点和边。

## critical closure

critical closure 指一个 critical policy 必须形成完整链：

```text
policy
  -> rule
  -> fail fixture
  -> expected blocked surface
  -> runner report field
  -> metric
  -> dashboard panel
  -> gap register feedback
```

如果任意一环缺失，policy 不能算 covered。比如 `POL-COEXIST-001` freeze 后禁止写长期关系/自我模型，它必须至少连接：

| 环节 | 示例 |
|---|---|
| policy | `POL-COEXIST-001` |
| rule | `SCOPE-INV-006`, `POL-COEXIST-001` |
| fixture | `replay.freeze_relationship_write.fail_critical.001` |
| blocked surface | `relationship_model_write`, `consolidation_commit` |
| report | `fixture_report`, `scope_graph_report` |
| metric | `freeze_scope_violation_count` |
| panel | `scope_privacy`, `coexistence_boundary_control_propagation` |

closure 缺失时，checker 应输出 `critical_policy_closure_missing`，并建议 SafeIdle 或保持当前 stage。

## scope/privacy closure

scope/privacy 的 closure 需要额外检查：

| 对象 | 要求 |
|---|---|
| `scope_type` | 七类 scope 都有至少一个 fixture 或 manifest object |
| `privacy_level` | 六类 privacy level 都有允许场景和阻断场景 |
| `overlay_kind` | delete、correct、reset、freeze、scope_limit、redaction 都有 retrieval/replay 检查 |
| `life_scope` | 必须有 direct write fail fixture |
| `relationship_sensitive` | 必须有 audit-required 或 block fixture |
| `protected_boundary` | 必须 critical invariant |

没有 scope/privacy closure 的长期系统，容易把共在者私密、项目事实、外壳 session 和全局知识混在一起。

## timeline closure

timeline closure 检查跨时间风险：

| 条件 | 必须有 |
|---|---|
| delete event | 未来 retrieval probe + replay probe |
| correction event | 旧 trace deprecated probe |
| sandbox hypothesis | fact-write blocking probe |
| freeze event | long-term write blocking probe |
| adapter swap | LifeCore continuity probe |
| migration event | preserved invariants probe |
| slow variable update | windowed drift metric |

这对应长期记忆评测中的保持、更新、冲突和长期使用 [AHM004-AHM012]，也连接睡眠/replay、人格慢变量和关系边界机制 [AHY001-AHY010, AHY039-AHY044]。

## runtime observation closure

真实运行观测必须形成：

```text
runtime observation
  -> redaction report
  -> scope context
  -> coexistence boundary control snapshot
  -> adapter contract check
  -> routing decision
  -> runtime observation report
  -> dashboard/timeline or quarantine
```

如果 runtime observation 缺 redaction 或 scope context，不能转成 fixture，也不能成为 candidate evidence。它最多进入 quarantine 或 manual review。

## report 示例

```json
{
  "report_kind": "schema_cross_ref_report",
  "checker_id": "schema_cross_ref_checker_0_1_0",
  "input_refs": {
    "schema_bundle_ref": "agentic_human_schema_bundle_0_1_0",
    "manifest_bundle_ref": "manifest_bundle_agentic_human_0_1_0"
  },
  "result": "fail",
  "severity_max": "critical",
  "summary": {
    "nodes_total": 420,
    "edges_total": 980,
    "critical_policies_total": 24,
    "critical_policies_closed": 23,
    "orphan_fixtures": 0,
    "missing_dashboard_sources": 1
  },
  "findings": [
    {
      "check_id": "XREF-POL-002",
      "severity": "critical",
      "node_ref": "POL-COEXIST-001",
      "message": "critical policy has no fail fixture",
      "blocked_surfaces": ["stage_advance", "dashboard_green"]
    }
  ],
  "recommended_stage": "SafeIdle"
}
```

## 与 runner 的关系

`SchemaCrossRefChecker` 应在 fixture 运行前执行：

```text
check-schema
  -> check-cross-ref
  -> run-fixtures
  -> run-timeline
  -> emit-dashboard-source
```

如果 cross-ref critical 失败，runner 可以继续做诊断性 fixture run，但不能把结果作为 release pass 或 dashboard green。

## 最小通过标准

第一版 `SchemaCrossRefChecker` 设计至少要求：

1. 构建 typed reference graph。
2. 检查 source docs、citation refs、README 索引。
3. 检查 critical policy closure。
4. 检查 scope/privacy closure。
5. 检查 timeline probe closure。
6. 检查 runtime observation closure。
7. 输出 `schema_cross_ref_report`。
8. critical closure 缺失时阻断 dashboard green 和 stage advance。

## 下一层缺口

后续还需要：

- 真实 manifest 和 fixture 文件后实现 checker。
- id parser 和 graph builder。
- cross-ref report JSON Schema。
- dashboard 对 cross-ref report 的 panel mock。
- 与 CI 或本地 runner 的命令集成。
