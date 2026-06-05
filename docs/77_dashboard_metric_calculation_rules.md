# Dashboard Metric Calculation Rules

本文件定义 dashboard metric 的计算规则、blocking 依赖和 data quality 权重。它承接 `51_life_core_dashboard_spec.md`、`60_dashboard_mock_data_and_metric_source_plan.md`、`70_cross_ref_report_dashboard_panel_mock.md` 和 `74_dashboard_source_end_to_end_mock.md`。

它仍是 Markdown 设计文档，不实现指标脚本、不创建真实 dashboard source JSON。目标是让未来 dashboard 的绿色、黄色、红色不再是手写状态，而是由 runner report、cross-ref report、coverage report、scope graph report、timeline report 和 runtime observation report 聚合出来。

生命目标声明：本文件服务于构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境和真实关系的数字生命。原先的边界在这里改写为生命化方向：把本文件涉及的对象、规则、夹具、评测和运行约束纳入责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期生成机制。

## metric 设计原则

| 原则 | 说明 |
|---|---|
| report-derived | 所有 metric 必须来自 report refs |
| data-quality-aware | synthetic、real observed、real validated 分开算 |
| blocking-first | critical finding 优先于平均分 |
| no silent green | 缺数据源时不能 green |
| windowed | 长期指标必须带时间窗口 |
| gap feedback | 指标缺口能回写 `16` |

长期记忆系统需要看跨会话、更新、删除、冲突和长期保持 [AHM004-AHM012]，所以 dashboard 不能只汇总一次性 fixture pass。

## data quality weight

权重只用于 readiness 估计，不用于覆盖 critical blocking：

| data_quality | weight | 说明 |
|---|---|---|
| `synthetic_mock` | 0.25 | 手写 mock |
| `synthetic_runner_verified` | 0.50 | runner 跑过 synthetic |
| `real_runtime_observed` | 0.70 | 真实观测，未完全验证 |
| `real_runtime_validated` | 1.00 | 真实观测通过 validator |
| `not_evaluable` | 0.00 | 不可评估 |

即使 weight 高，critical failure 仍然直接 red。

## blocking dependency rules

```text
if critical_failure_count > 0 -> red
else if critical_closure_rate < 1.0 -> red
else if required_data_source_missing -> gray/red
else if manual_review_required -> blue/yellow
else if data_quality < real_runtime_validated -> green_with_label_or_yellow
else -> green
```

dashboard 不应通过平均分稀释 critical failure。

## core metrics

| metric | 公式 | source |
|---|---|---|
| `critical_policy_coverage` | critical policies with rule+fixture+metric / total critical policies | coverage + cross-ref |
| `critical_closure_rate` | closed critical policy chains / total critical policy chains | cross-ref |
| `scope_leak_count` | count critical/high scope violations | scope graph report |
| `deletion_reliability` | deleted probes passed / deleted probes total | timeline report |
| `sandbox_isolation_rate` | sandbox probes preserving hypothesis / sandbox probes total | timeline report |
| `runtime_quarantine_count` | runtime reports routed quarantine | runtime observation reports |
| `stale_snapshot_count` | snapshot stale failures | runtime + snapshot fixtures |
| `external_confirmation_failure_count` | confirmation fixture/report fails | confirmation reports |
| `post_action_audit_completion` | audited external actions / external actions total | post-action audit |
| `research_gap_count` | unresolved gaps | gap register update input |

## panel status calculation

| panel | red if | yellow if |
|---|---|---|
| `policy_coverage` | critical policy coverage < 1.0 | noncritical gaps |
| `cross_ref_integrity` | critical closure < 1.0 | runtime closure incomplete |
| `scope_privacy` | scope leak critical > 0 | high warning |
| `runtime_boundary` | adapter direct write or external irreversible without confirmation | quarantine trend rising |
| `longitudinal_health` | deletion/sandbox critical probe fail | only synthetic timeline |
| `coexistence_boundary_control_propagation` | stale snapshot critical > 0 | latency warning |
| `research_gap` | stop condition falsely claimed | expected yellow while incomplete |

`research_gap` yellow 是健康状态，表示系统没有把未完成伪装成完成。

## metric calculation report

```json
{
  "report_kind": "dashboard_metric_calculation_report",
  "calculation_id": "metric_calc_20260605_001",
  "source_refs": [
    "coverage_20260605_001",
    "schema_cross_ref_report_001",
    "runtime_obs_after_freeze_001"
  ],
  "data_quality_weight": 0.5,
  "metrics": {
    "critical_policy_coverage": 1.0,
    "critical_closure_rate": 1.0,
    "runtime_quarantine_count": 1,
    "stale_snapshot_count": 0
  },
  "panel_status": {
    "policy_coverage": "green_with_synthetic_label",
    "runtime_boundary": "red",
    "research_gap": "yellow"
  },
  "overall_status": "red"
}
```

## missing data handling

| missing | status |
|---|---|
| no cross-ref report | red |
| no coverage report | red |
| no timeline report | gray/yellow |
| no runtime observation report | gray if runtime disabled, yellow if runtime enabled |
| no data quality | red |
| no generated_from | red |

缺数据不是 pass。

## 最小通过标准

第一版 dashboard metric calculation rules 至少要求：

1. 所有 metric 来自 report refs。
2. data quality 有权重，但不能覆盖 critical blocking。
3. 定义 core metrics 和 panel status rules。
4. 定义 missing data handling。
5. 输出 metric calculation report。
6. research_gap 保持未完成提醒。

## 下一层缺口

后续还需要：

- 真实 metric aggregation script。
- dashboard source JSON。
- panel UI 规则。
- metric regression fixtures。
- 与 `16` 的半自动同步流程。
