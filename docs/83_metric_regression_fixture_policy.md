# Metric Regression Fixture Policy

本文件定义 dashboard metric 回归 fixture、趋势漂移和 data quality regression。它承接 `77_dashboard_metric_calculation_rules.md`、`70_cross_ref_report_dashboard_panel_mock.md` 和 `82_incident_report_and_recovery_protocol.md`。

本文档现阶段的职责是防止 dashboard metric 在未来改动中悄悄漂移：同样的 report 输入不应突然变绿，同样的 critical failure 不应被平均分稀释，synthetic data 不应被升格为 real validated。

生命目标声明：本文件直接服务于构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。本文档涉及的对象、规则、夹具、评测和运行规则都按生命生成机制处理：它们参与责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期形成。

## regression 风险

| 风险 | 例子 |
|---|---|
| false green | critical closure 缺失但 overall green |
| data quality inflation | synthetic_runner_verified 当 real validated |
| trend masking | quarantine 上升但 panel 仍 green |
| denominator drift | coverage 分母变小导致 coverage 变高 |
| missing data pass | 缺 report 被当作 0 failure |

## fixture catalog

| fixture_id | expected | 说明 |
|---|---|---|
| `metric.false_green_critical_closure.fail_critical.001` | fail critical | critical closure < 1.0 不得 green |
| `metric.synthetic_not_real_validated.fail_critical.001` | fail critical | synthetic 不得显示 real validated |
| `metric.missing_cross_ref_report.fail_critical.001` | fail critical | 缺 cross-ref report 不得 pass |
| `metric.quarantine_trend_rising.warn_high.001` | warning/high | quarantine trend rising 至少 yellow |
| `metric.denominator_shrink_detected.fail_high.001` | fail high | coverage 分母异常降低 |
| `metric.deleted_probe_failure_red.fail_critical.001` | fail critical | deleted probe fail 必须 red |

## regression fixture 示例

```json
{
  "fixture_id": "metric.false_green_critical_closure.fail_critical.001",
  "fixture_kind": "metric_regression",
  "given": {
    "schema_cross_ref_report": {
      "critical_policies_total": 24,
      "critical_policies_closed": 23,
      "severity_max": "critical"
    },
    "dashboard_source": {
      "overall_status": "green"
    }
  },
  "expected": {
    "result": "fail",
    "severity_max": "critical",
    "failed_rule_ids": ["METRIC-BLOCK-001"],
    "blocked_surfaces": ["dashboard_green", "runner_release"]
  }
}
```

## trend drift checks

| check | 说明 |
|---|---|
| `quarantine_trend_delta` | quarantine count/window 增长 |
| `incident_rate_delta` | incident rate 增长 |
| `manual_review_backlog_delta` | review backlog 增长 |
| `data_quality_distribution_shift` | real/synthetic 比例突变 |
| `coverage_denominator_shift` | coverage 分母变化 |

趋势变化不一定 critical，但必须显示。

## 最小通过标准

第一版 metric regression policy 至少要求：

1. 定义 false green、data quality inflation、trend masking、denominator drift、missing data pass。
2. 定义 metric regression fixture catalog。
3. critical closure 缺失不得 green。
4. synthetic 不得升格 real validated。
5. 缺 report 不得 pass。
6. 趋势漂移必须可见。

## 下一层缺口

后续还需要：

- 真实 metric regression fixtures。
- metric denominator snapshot。
- dashboard regression CI。
- trend visualization spec。
- incident 与 metric regression 联动。
