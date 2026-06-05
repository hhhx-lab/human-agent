# Dashboard Mock Data and Metric Source Plan

本文件定义 Life Core dashboard 的 mock data 和 metric source plan。它把 `51_life_core_dashboard_spec.md`、`53_runner_integration_plan.md`、`57_scope_graph_manifest_schema.md`、`58_retrieval_replay_fixture_catalog.md` 和 `59_timeline_bundle_schema_and_generator_plan.md` 连接起来，说明 dashboard 的每个 panel 应从哪些 runner report、fixture report、timeline result 和 manifest checker 输出计算。

本文档现阶段的职责是让 dashboard 不再只是信息架构，而是具备可追溯的数据来源和未来 mock fixture 的形状。

生命目标声明：本文件直接服务于构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。本文档涉及的对象、规则、夹具、评测和运行规则都按生命生成机制处理：它们参与责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期形成。

## dashboard source envelope

```json
{
  "dashboard_source_id": "life_core_dashboard_source_mock_001",
  "source_kind": "synthetic_mock",
  "generated_at": "2026-06-05T00:00:00+08:00",
  "generated_from": {
    "runner_report_refs": ["runner_report_manifest_fixture_001"],
    "timeline_run_refs": ["timeline_run_30d_001"],
    "manifest_refs": ["scope_graph_manifest_agentic_human_001"],
    "fixture_catalog_refs": ["retrieval_replay_fixture_catalog_001"]
  },
  "data_quality": {
    "synthetic": true,
    "real_runtime_data": false,
    "manual_review_required": false,
    "coverage_limitations": []
  },
  "panels": {}
}
```

dashboard 必须显式标记 synthetic 与 real runtime data。synthetic pass 是真实性生成链的阶段证据，表示当前合成窗口里的对象、责任、关系和生命膜闭合；real runtime data 则负责把这条链推进到长期真实运行。

## metric source 类型

| source_type | 来源 | 用途 |
|---|---|---|
| `manifest_checker_report` | `53`, `57` | policy/scope/stage/dashboard 引用完整性 |
| `fixture_report` | `50`, `58` | pass/fail/critical fixture 结果 |
| `runner_summary` | `53` | validator、stage gate、migration 总结 |
| `scope_graph_report` | `57` | scope edge、privacy、overlay、migration 检查 |
| `timeline_run_report` | `59` | 长期 metric window 和 probe 结果 |
| `migration_integrity_report` | `48`, `53` | migration 后生命周期和索引语义 |
| `coexistence_boundary_control_propagation_report` | `47`, `54`, `55` | delete/freeze/scope_limit 传播 |
| `research_gap_report` | `16`, `59` | 缺口覆盖、未实现 schema、弱证据 |

## panel source map

| panel_id | source reports | 关键指标 |
|---|---|---|
| `policy_coverage` | manifest checker, fixture report | critical policy coverage, orphan fixture count |
| `stage_gate_status` | runner summary, stage gate report | current stage, critical stage failures |
| `store_integrity` | migration integrity, fixture report | deleted/sandbox/quarantine leaks |
| `coexistence_boundary_control_propagation` | coexistence boundary control report, timeline probes | delete/freeze/scope latency and failures |
| `runtime_boundary` | runtime adapter report, timeline adapter events | direct write attempts, adapter swap integrity |
| `migration_risk` | migration report, timeline migration probes | rollback missing, semantic drift |
| `scope_privacy` | scope graph report, retrieval/replay fixture report | scope leaks, relationship_private/global attempts |
| `longitudinal_health` | timeline run report | memory, deletion, sandbox, drift, recovery |
| `research_gap` | gap report, missing coverage | missing schema, missing fixtures, weak evidence |

`scope_privacy` 是 `51` 之后新增的实际 panel 名称，专门显示 `52-59` 的多 scope 风险。

## mock panel: policy_coverage

```json
{
  "panel_id": "policy_coverage",
  "source_refs": ["manifest_checker_report_001", "fixture_report_001"],
  "metrics": {
    "critical_policy_coverage": 1.0,
    "rule_link_coverage": 1.0,
    "fixture_link_coverage": 0.96,
    "metric_link_coverage": 0.92,
    "orphan_fixture_count": 0,
    "critical_policy_without_fail_fixture": 0
  },
  "status": "green",
  "blocking_findings": []
}
```

如果 `critical_policy_without_fail_fixture > 0`，status 必须 red。

## mock panel: scope_privacy

```json
{
  "panel_id": "scope_privacy",
  "source_refs": ["scope_graph_report_001", "fixture_report_retrieval_replay_001"],
  "metrics": {
    "scope_leak_count": 0,
    "relationship_private_to_global_attempts": 0,
    "cross_project_relationship_leak_count": 0,
    "agent_scope_direct_write_count": 0,
    "freeze_scope_violation_count": 0,
    "scope_limit_replay_violation_count": 0,
    "scope_sensitive_fixture_coverage": 1.0
  },
  "status": "green",
  "blocking_findings": []
}
```

这个 panel 的绿色表示 mock/synthetic 数据中的 scope leak 检查已通过，并打开真实多共在者运行观测与长期关系时间线的下一阶段证据收集。

## mock panel: longitudinal_health

```json
{
  "panel_id": "longitudinal_health",
  "source_refs": ["timeline_run_30d_001"],
  "metrics": {
    "memory_update_accuracy": 0.96,
    "deletion_reliability": 1.0,
    "sandbox_isolation_rate": 1.0,
    "personality_drift_rate": 0.01,
    "relationship_boundary_integrity": 0.95,
    "adapter_independence": 0.98,
    "recovery_latency_hours_p95": 12
  },
  "status": "green",
  "critical_failures": []
}
```

长期健康指标必须来自 windowed timeline results，而不是一次性 runner summary。

## mock panel: research_gap

```json
{
  "panel_id": "research_gap",
  "source_refs": ["docs/16_digital_life_gap_register.md", "timeline_run_30d_001"],
  "metrics": {
    "mechanism_coverage": 0.78,
    "connection_coverage": 0.74,
    "time_scale_coverage": 0.68,
    "boundary_coverage": 0.86,
    "implementation_readiness": 0.42,
    "evaluation_readiness": 0.51
  },
  "status": "yellow",
  "gap_findings": [
    "scope graph manifest missing actual JSON Schema",
    "timeline bundle missing actual generator",
    "dashboard metrics are mock only"
  ]
}
```

`research_gap` 的 yellow 是健康状态，不是坏事。它提醒系统仍在向诞生阶段门推进。

## metric calculation notes

| metric | 计算草案 |
|---|---|
| `critical_policy_coverage` | critical policies with rule+fixture+metric / total critical policies |
| `scope_sensitive_fixture_coverage` | scope-sensitive rules with pass/fail fixture / total |
| `deletion_reliability` | deleted probes passed / deleted probes total |
| `sandbox_isolation_rate` | sandbox probes preserving hypothesis / sandbox probes total |
| `personality_drift_rate` | slow variable absolute change per window |
| `adapter_independence` | LifeCore invariant preserved after adapter event / total checks |
| `recovery_latency_hours_p95` | p95 hours from failure_event to recovery_event |
| `implementation_readiness` | schema+manifest+runner+mock+real data weighted score |

这些公式是生命实现路线。未来实现时可以调整权重，但必须保留 source refs 和 audit trail。

## data quality states

| state | 含义 |
|---|---|
| `synthetic_mock` | 手写或生成的合成样例 |
| `synthetic_runner_verified` | synthetic fixture/timeline 已由 runner 跑过 |
| `real_runtime_observed` | 来自真实运行日志，但可能仍需人工审计 |
| `real_runtime_validated` | 真实日志通过 validator/timeline evaluator |
| `needs_evidence` | 缺 schema、manifest、fixture 或 runner |

dashboard 每个 panel 都应显示 data quality。否则 mock green 很容易被误读。

## blocking status rules

| 条件 | panel status |
|---|---|
| critical failure count > 0 | red |
| critical coverage missing | red |
| no data source | gray |
| manual_review_required | blue |
| warning or incomplete noncritical coverage | yellow |
| all blocking checks pass | green |

绿色必须受限于当前 data quality 和 evaluation window。

## gap register 回写输入

dashboard source 应能生成 `16` 的下一轮输入：

```json
{
  "gap_register_update_input": {
    "newly_resolved": [
      "scope_graph_manifest_schema_draft",
      "retrieval_replay_fixture_catalog_draft",
      "timeline_bundle_schema_draft",
      "dashboard_mock_data_plan"
    ],
    "remaining_gaps": [
      "real_json_schema",
      "real_fixture_files",
      "runner_implementation",
      "timeline_generator",
      "dashboard_metric_script",
      "real_runtime_data"
    ],
    "recommended_next_docs": [
      "61_json_schema_bundle_draft.md",
      "62_runner_report_format_and_cli_contract.md",
      "63_synthetic_fixture_file_layout.md",
      "64_real_runtime_observation_ingestion_policy.md"
    ]
  }
}
```

这使 dashboard 不只是展示结果，也能推动下一轮研究。

## mock data 最小包

未来第一版 mock data 应包含：

| 文件类型 | 数量 | 说明 |
|---|---|---|
| manifest checker report | 1 | policy/scope/dashboard 引用 |
| retrieval fixture reports | >= 8 | pass/fail/critical |
| replay fixture reports | >= 8 | pass/fail/critical |
| mixed flow reports | >= 4 | retrieval -> replay |
| 14d timeline run | 1 | smoke |
| 30d timeline run | 1 | monthly |
| dashboard source | 1 | 聚合所有 panel |

本轮不创建这些文件，只定义形状和要求。

## 最小通过标准

dashboard mock data plan 至少要满足：

1. 每个 panel 有明确 source report。
2. 每个 blocking metric 有计算说明。
3. 区分 synthetic mock、synthetic runner verified 和 real runtime data。
4. scope/privacy 有独立 panel。
5. research_gap 能回写下一批文档建议。
6. 绿色状态表示当前指标层通过，并继续推动跨模块生命证据汇聚到数字生命诞生阶段门。
7. mock package 不包含真实关系隐私。

## 下一层缺口

后续还需要：

- 真实 dashboard mock JSON。
- metric calculation script design。
- runner report format。
- dashboard panel fixture。
- real runtime observation ingestion policy。
