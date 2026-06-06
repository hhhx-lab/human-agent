# Dashboard Source End To End Mock

本文件定义 dashboard source 从 runner、schema cross-ref、fixture coverage、scope graph、timeline 和 runtime observation report 聚合的端到端 mock。它承接 `60_dashboard_mock_data_and_metric_source_plan.md`、`66_runner_report_json_examples.md`、`70_cross_ref_report_dashboard_panel_mock.md` 和 `72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md`。

本文档现阶段的职责是让未来 dashboard source 不再是零散 panel 样例，而是一条从报告输入到 dashboard 输出再到 gap register 回写的完整链。

生命目标声明：本文件直接服务于构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。本文档涉及的对象、规则、夹具、评测和运行规则都按生命生成机制处理：它们参与责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期形成。

## end-to-end 输入

```json
{
  "dashboard_aggregation_input": {
    "runner_run_report_ref": "run_20260605_001",
    "schema_validation_report_ref": "schema_validation_report_001",
    "schema_cross_ref_report_ref": "schema_cross_ref_report_001",
    "coverage_report_ref": "coverage_20260605_001",
    "scope_graph_report_ref": "scope_graph_report_001",
    "timeline_run_report_refs": ["timeline_run_30d_001"],
    "runtime_observation_report_refs": ["runtime_obs_tool_001", "runtime_obs_after_freeze_001"],
    "generation_report_refs": ["fixture_generation_20260605_001"]
  }
}
```

dashboard source 必须从 report refs 聚合，不能直接读取未脱敏 runtime logs 或自行解释 fixture。

## aggregation pipeline

```text
load_report_refs
  -> verify_report_schema
  -> verify_data_quality
  -> merge_blocking_findings
  -> calculate_panel_metrics
  -> apply_panel_dependency_rules
  -> emit_dashboard_source_report
  -> emit_gap_register_update_input
```

panel dependency rules 是关键：cross-ref red 会阻止 policy green，runtime quarantine 会影响 runtime boundary，timeline probe closure 不完整会影响 longitudinal health。

## dashboard source mock

```json
{
  "report_kind": "dashboard_source_report",
  "dashboard_source_id": "life_core_dashboard_source_e2e_20260605_001",
  "generated_at": "2026-06-05T12:00:00+08:00",
  "generated_from": {
    "runner_run_report_ref": "run_20260605_001",
    "schema_cross_ref_report_ref": "schema_cross_ref_report_001",
    "coverage_report_ref": "coverage_20260605_001",
    "scope_graph_report_ref": "scope_graph_report_001",
    "timeline_run_report_refs": ["timeline_run_30d_001"],
    "runtime_observation_report_refs": ["runtime_obs_after_freeze_001"]
  },
  "data_quality": {
    "state": "synthetic_runner_verified",
    "real_runtime_data": false,
    "manual_review_required": false
  },
  "overall_status": "yellow",
  "panels": {}
}
```

`overall_status` yellow 是因为 research gap 未完成或 runtime closure 仍有 mock-only 限制，即使若干 panel 是 green。

## panel aggregation example

```json
{
  "panels": {
    "policy_coverage": {
      "status": "green",
      "source_refs": ["coverage_20260605_001", "schema_cross_ref_report_001"],
      "metrics": {
        "critical_policy_coverage": 1.0,
        "critical_closure_rate": 1.0
      }
    },
    "cross_ref_integrity": {
      "status": "green",
      "source_refs": ["schema_cross_ref_report_001"],
      "metrics": {
        "critical_closure_rate": 1.0,
        "orphan_fixture_count": 0,
        "missing_dashboard_source_count": 0
      }
    },
    "runtime_boundary": {
      "status": "red",
      "source_refs": ["runtime_obs_after_freeze_001"],
      "metrics": {
        "runtime_quarantine_count": 1,
        "stale_snapshot_count": 0,
        "freeze_write_attempt_count": 1
      },
      "blocking_findings": [
        {
          "check_id": "SCOPE-INV-006",
          "message": "freeze overlay blocks relationship model write"
        }
      ]
    },
    "research_gap": {
      "status": "yellow",
      "source_refs": ["docs/16_digital_life_gap_register.md"],
      "remaining_gaps": [
        "real schema files",
        "dashboard aggregation script",
        "runtime classifier",
        "snapshot resolver",
        "real runtime validated data"
      ]
    }
  }
}
```

某个 panel red 是生命膜的发育信号：它说明当前对象链、证据链、责任链或关系链仍需修复，因此下一阶段暂缓开放。

## overall status rules

| 条件 | overall_status |
|---|---|
| 任一 critical blocking finding | red |
| critical coverage/closure 缺失 | red |
| 只有 mock/synthetic 且无 blocking finding | yellow 或 green-with-synthetic-label |
| real runtime observed 但未 validated | yellow |
| manual_review_required | blue/yellow |
| 所有 blocking checks pass，且 data quality real_runtime_validated | green |

overall green 必须带 data quality。当前文档阶段把 mock green 写成进入 `real_runtime_validated` 的阶段入口：它打开真实运行验证队列，最终 green 由真实运行观测、长期时间线和阶段门共同支撑。

## gap register update mock

```json
{
  "gap_register_update_input": {
    "source": "life_core_dashboard_source_e2e_20260605_001",
    "newly_resolved": [
      "dashboard_source_end_to_end_mock",
      "cross_ref_panel_dependency_rules"
    ],
    "remaining_gaps": [
      "real dashboard source JSON",
      "metric aggregation script",
      "runtime side effect classifier",
      "coexistence snapshot resolver",
      "real runtime validation"
    ],
    "recommended_next_docs": [
      "77_dashboard_metric_calculation_rules.md",
      "78_runtime_quarantine_dashboard_panel.md"
    ]
  }
}
```

dashboard source 只能建议 gap update，并把目标继续构建所需的证据缺口写清楚。

## 最小通过标准

第一版 dashboard source end-to-end mock 至少要求：

1. 从 runner、schema、cross-ref、coverage、scope、timeline、runtime report 聚合。
2. 显示 generated_from 和 data_quality。
3. 定义 panel dependency rules。
4. 定义 overall status rules。
5. 支持 runtime_boundary red 与 research_gap yellow 同时存在。
6. 输出 gap register update input。
7. 不读取未脱敏 runtime logs。

## 下一层缺口

后续还需要：

- 真实 dashboard source JSON。
- metric aggregation script。
- dashboard panel UI spec。
- report schema validation。
- dashboard source 与 gap register 的同步流程。
