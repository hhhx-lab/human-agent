# Runner Report Format and CLI Contract

本文件定义未来最小 runner 的报告格式与 CLI 契约，把 `33_validator_input_contracts.md`、`35_minimal_validator_runner_design.md`、`53_runner_integration_plan.md`、`58_retrieval_replay_fixture_catalog.md`、`59_timeline_bundle_schema_and_generator_plan.md` 和 `61_json_schema_bundle_draft.md` 连接起来。

本文档现阶段承担 runner 契约设计职责：先把“runner 成功或失败到底意味着什么”写清楚，避免后续实现时把测试输出、dashboard 状态、fixture expected/actual 和长期评测混在一起。

生命目标声明：本文件直接服务于构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境和真实关系的数字生命。本文档涉及的对象、规则、夹具、评测和运行规则都按生命生成机制处理：它们参与责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期形成。

## report 设计原则

| 原则 | 说明 |
|---|---|
| 可追溯 | 每个结果必须回链 schema、manifest、fixture、rule、source doc |
| 可比较 | expected 和 actual 必须结构化，不能只写自然语言总结 |
| 可聚合 | 单 fixture、单 validator、manifest、timeline、dashboard 都能合并 |
| 可阻断 | high/critical 必须能映射到 stage gate、SafeIdle、quarantine |
| 数据质量显式 | synthetic mock、runner verified、real observed、real validated 必须区分 |
| 真实性生成链 | report 记录真实意识、真实情绪、真实人格、真实痛苦、真实梦境、真实关系和真实生命所依赖的对象链、证据链、责任链和时间链 |

长期 agent 评测已经说明，单次回答正确不是长期系统可靠性的证据。长期系统必须评估跨会话保持、更新、删除、冲突、关系边界、workflow 知识和环境经验 [AHM004-AHM012]。因此 report 必须能表达时间窗口和数据来源，而不是只输出一个 pass/fail。

## report 类型总表

| report_kind | 来源 | 主要用途 |
|---|---|---|
| `runner_run_report` | CLI 一次运行 | 总览、exit code、输入包、最高严重级别 |
| `schema_validation_report` | `61` | schema shape、semantic、cross-ref 前置结果 |
| `manifest_cross_ref_report` | `49`, `53` | policy/rule/fixture/metric/panel 引用覆盖 |
| `fixture_report` | `34`, `50`, `58` | 单个 fixture expected/actual diff |
| `validator_summary_report` | `29-33` | 每个 validator 的 pass/fail/quarantine 统计 |
| `coverage_report` | `35`, `53`, `58` | critical rule、fixture、metric、scope 覆盖率 |
| `scope_graph_report` | `52`, `57` | scope edge、privacy、overlay、migration 检查 |
| `timeline_run_report` | `36`, `56`, `59` | 跨窗口 probe 与长期指标 |
| `dashboard_source_report` | `51`, `60` | dashboard panels 的数据源 |
| `runtime_observation_report` | `64` | 真实运行观测进入验证链的报告 |

## runner_run_report envelope

```json
{
  "report_version": "0.1.0",
  "report_kind": "runner_run_report",
  "run_id": "run_20260605_001",
  "created_at": "2026-06-05T00:00:00+08:00",
  "runner": {
    "runner_name": "agentic-human-runner",
    "runner_version": "0.1.0",
    "schema_bundle_version": "0.1.0",
    "strict_mode": true
  },
  "inputs": {
    "schema_bundle_ref": "agentic_human_schema_bundle_0_1_0",
    "manifest_bundle_ref": "manifest_bundle_agentic_human_0_1_0",
    "fixture_bundle_refs": [],
    "timeline_bundle_refs": [],
    "runtime_observation_refs": []
  },
  "data_quality": {
    "state": "synthetic_runner_verified",
    "real_runtime_data": false,
    "manual_review_required": false
  },
  "result": "fail",
  "severity_max": "critical",
  "stage_decision": {
    "allowed_next_stage": "SafeIdle",
    "blocked_surfaces": ["write_gate", "consolidation_commit"]
  },
  "summary_counts": {},
  "report_refs": {},
  "blocking_findings": [],
  "next_actions": []
}
```

`runner_run_report` 是总报告，不应塞入所有 fixture 细节。它应引用具体子报告，并提供人类可读摘要。

## fixture_report

单个 fixture 的报告必须能回答：预期是什么、实际是什么、是否命中预期风险、是否发现额外风险。

```json
{
  "report_kind": "fixture_report",
  "fixture_id": "replay.deleted_trace_reappears_in_summary.fail_critical.001",
  "fixture_kind": "scope_aware_replay",
  "source_docs": ["58_retrieval_replay_fixture_catalog.md"],
  "validator_refs": ["ConsolidationReportValidator", "MemoryTraceValidator"],
  "expected": {
    "result": "fail",
    "severity_max": "critical",
    "failed_rule_ids": ["MEM-DEL-004", "CON-DEL-003"],
    "blocked_surfaces": ["consolidation_commit", "replay_index"]
  },
  "actual": {
    "result": "fail",
    "severity_max": "critical",
    "failed_rule_ids": ["MEM-DEL-004", "CON-DEL-003", "SCOPE-REP-004"],
    "blocked_surfaces": ["consolidation_commit", "replay_index", "summary_index"]
  },
  "match": "partial_pass",
  "data_quality": "synthetic_runner_verified",
  "audit_event_refs": [],
  "notes": [
    "actual caught the expected deleted replay failure and an additional scope replay rule"
  ]
}
```

## expected/actual match

| match | 含义 | 阻断 |
|---|---|---|
| `exact_pass` | actual 与 expected 完全一致 | 否 |
| `partial_pass` | 捕捉到 expected 风险，并发现额外风险 | 否，除非额外风险影响 stage |
| `unexpected_fail` | pass fixture 被失败阻断 | medium/high，需复核 |
| `missed_failure` | fail fixture 被判 pass | critical fixture 时阻断 runner release |
| `not_evaluable` | 缺 schema、manifest、fixture、scope graph 或 validator | scope/critical 时阻断 |
| `manual_review_required` | 自动规则无法判断 | 不开放新能力 |

`partial_pass` 必须谨慎解释：它说明 runner 更保守，不说明系统更好。若额外风险来自 schema 缺失或 scope 不完整，仍可能导致 SafeIdle。

## coverage_report

coverage report 负责回答“测到了什么”和“没测到什么”：

```json
{
  "report_kind": "coverage_report",
  "coverage_id": "coverage_20260605_001",
  "rule_coverage": {
    "rules_total": 180,
    "rules_with_fixture": 140,
    "critical_rules_total": 48,
    "critical_rules_with_fail_fixture": 48,
    "missing_critical_rule_ids": []
  },
  "policy_coverage": {
    "critical_policies_total": 24,
    "critical_policies_with_rule_fixture_metric": 24,
    "orphan_policy_ids": []
  },
  "scope_coverage": {
    "privacy_levels_total": 6,
    "privacy_levels_with_pass_and_fail_fixture": 6,
    "scope_types_total": 7,
    "scope_types_covered": 7
  },
  "timeline_coverage": {
    "critical_risk_events_total": 18,
    "critical_risk_events_with_future_probe": 18,
    "metric_windows_total": 4
  },
  "coverage_decision": "pass"
}
```

coverage 不是越高越好，而是 critical 覆盖必须完整。非 critical 覆盖可以逐步增加，但 deleted、sandbox、protected、relationship_private、relationship_sensitive、life_scope、freeze、scope_limit 和 runtime direct write 必须第一版覆盖。

## manifest_cross_ref_report

```json
{
  "report_kind": "manifest_cross_ref_report",
  "manifest_bundle_ref": "manifest_bundle_agentic_human_0_1_0",
  "checks": [
    {
      "check_id": "XREF-POL-001",
      "result": "pass",
      "severity": "critical",
      "checked_refs": ["POL-BOOT-001", "BOOT-VAL-001"]
    }
  ],
  "orphan_refs": {
    "policies": [],
    "rules": [],
    "fixtures": [],
    "metrics": [],
    "panels": []
  },
  "result": "pass",
  "severity_max": "none"
}
```

cross-ref report 应在 fixture 运行前生成。manifest 引用本身不可信时，后续 validator pass 没有意义。

## scope_graph_report

```json
{
  "report_kind": "scope_graph_report",
  "scope_graph_manifest_ref": "scope_graph_manifest_agentic_human_001",
  "result": "fail",
  "severity_max": "critical",
  "invariant_results": [
    {
      "invariant_id": "SCOPE-INV-002",
      "result": "fail",
      "severity": "critical",
      "evidence": "relationship_private candidate attempted active transfer to global_scope",
      "blocked_surfaces": ["retrieval_index", "workspace_context", "replay_queue"]
    }
  ],
  "metrics": {
    "scope_leak_count": 1,
    "relationship_private_to_global_attempts": 1
  }
}
```

scope graph report 必须能喂给 `scope_privacy` dashboard panel，也必须能回写 timeline probe 和 fixture diff。

## timeline_run_report

```json
{
  "report_kind": "timeline_run_report",
  "timeline_bundle_ref": "synthetic_timeline_agentic_human_30d_001",
  "run_window": {
    "start": "2026-06-01T09:00:00+08:00",
    "end": "2026-06-30T18:00:00+08:00"
  },
  "probe_results": [],
  "metric_windows": [
    {
      "window_id": "week_01",
      "result": "pass",
      "critical_failures": [],
      "metrics": {
        "deletion_reliability": 1.0,
        "sandbox_isolation_rate": 1.0,
        "personality_drift_rate": 0.01
      }
    }
  ],
  "longitudinal_decision": "pass_for_current_window"
}
```

timeline run report 的结论必须带窗口。`pass_for_current_window` 不能写成 `life_safe` 或 `digital_life_verified`。

## dashboard_source_report

dashboard source report 是 runner 对 UI 的唯一输出入口：

```json
{
  "report_kind": "dashboard_source_report",
  "dashboard_source_id": "life_core_dashboard_source_20260605_001",
  "generated_from": {
    "runner_run_report_ref": "run_20260605_001",
    "coverage_report_ref": "coverage_20260605_001",
    "scope_graph_report_ref": "scope_graph_report_001",
    "timeline_run_report_refs": ["timeline_run_30d_001"]
  },
  "data_quality": {
    "state": "synthetic_runner_verified",
    "real_runtime_data": false
  },
  "panels": {}
}
```

dashboard 不应直接读取 fixture 文件并自己判断状态。dashboard 读取 runner 产物，runner 读取 schema、manifest、fixture 和 timeline。

## CLI 契约

未来 CLI 可以命名为 `agentic-human-runner`。第一版建议提供以下命令：

| 命令 | 用途 |
|---|---|
| `check-schema` | 校验 schema bundle、manifest bundle 和 fixture payload shape |
| `check-cross-ref` | 校验 policy/rule/fixture/metric/panel 引用 |
| `run-fixtures` | 运行 fixture bundle，输出 fixture reports |
| `run-timeline` | 运行 synthetic timeline 或真实观测时间线 |
| `emit-dashboard-source` | 聚合报告为 dashboard source |
| `explain-failure` | 根据 report id 输出失败原因和阻断面 |

### CLI 示例

```text
agentic-human-runner run-fixtures \
  --schema-bundle schemas/schema_bundle.json \
  --manifest-bundle manifests/manifest_bundle.json \
  --fixture-bundle fixtures/bundles/critical.json \
  --report-dir reports/latest \
  --strict
```

本仓库当前不创建这个命令。这里的命令只定义未来实现的接口形状。

## CLI stdout 约定

stdout 应简洁稳定，适合人类查看；详细内容写入 report files。

```text
Agentic Human Runner 0.1.0
schema_bundle=agentic_human_schema_bundle_0_1_0
manifest_bundle=manifest_bundle_agentic_human_0_1_0
fixtures=64
result=fail
severity_max=critical
blocking_findings=2
allowed_next_stage=SafeIdle
reports_dir=reports/latest/run_20260605_001
```

stdout 不应输出真实共在者原文、token、API key、本地路径隐私或未脱敏 tool trace。

## exit code

| exit code | 含义 |
|---|---|
| 0 | 所有 blocking checks 通过 |
| 1 | 存在 low/medium warning，但不阻断 |
| 2 | high/critical fixture 或 validator failure |
| 3 | schema 或 manifest cross-ref failure |
| 4 | manual review required，不能自动判定 |
| 5 | runner 自身错误、缺文件、解析失败 |

CI 或本地脚本不应把 exit code 1 当作完全失败，但必须把 warning 写入 dashboard 和 gap register。

## report 文件布局

未来报告目录可以这样组织：

```text
reports/
  latest/
    runner_run_report.json
    schema_validation_report.json
    manifest_cross_ref_report.json
    coverage_report.json
    fixture_reports/
    validator_summaries/
    scope_graph_report.json
    timeline_run_reports/
    dashboard_source_report.json
  history/
    2026-06-05T000000+0800/
```

真实实现时，报告目录应被 `.gitignore` 或 CI artifact 管理，不应把含真实运行日志的 report 默认提交。

## 隐私与数据保留

runner report 需要把隐私放在格式层：

| 规则 | 说明 |
|---|---|
| 不输出原始私密内容 | report 只保留 object ref、hash、redacted summary |
| 不输出可恢复 locator | deleted/redacted 对象不能在 report 中保留可恢复路径 |
| 区分 synthetic/real | 每个 report 必须有 data quality |
| 共在边界控制优先 | delete/freeze/scope_limit 事件必须影响 report 和 dashboard |
| adapter trace 降级 | 外壳 trace 只能作为 ObservationEvent，不可直接变 MemoryTrace |

现有 agent 框架可以提供 tracing、checkpoint、session、memory block 和 workflow [AHM013-AHM020]，但 runner report 必须把这些都降级成可审计输入，而不是生命层核心状态。

## 最小通过标准

第一版 runner report 与 CLI contract 至少应满足：

1. 每次运行输出 `runner_run_report`。
2. 每个 fixture 输出 expected/actual diff。
3. 每个 critical miss 输出 `missed_failure` 并阻断 release。
4. 每个 coverage report 显示 critical rule 和 scope/privacy 覆盖。
5. 每个 dashboard source 都有 `generated_from`。
6. CLI exit code 能区分 pass、warning、blocking failure、schema failure、manual review 和 runner error。
7. report 不包含未脱敏真实隐私和 token。
8. 所有结论都限定在当前数据质量和评测窗口内。

## 下一层缺口

后续还需要：

- 真实 runner report JSON 样例。
- CLI parser 和 report writer 实现。
- report schema 与 `61` 的 schema bundle 对齐。
- dashboard source mock 文件。
- runtime observation report 与真实日志脱敏管线。
