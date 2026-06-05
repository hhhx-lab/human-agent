# Runtime Quarantine Dashboard Panel

本文件定义 runtime quarantine panel、quarantine trend 和解除条件。它承接 `64_real_runtime_observation_ingestion_policy.md`、`68_runtime_observation_report_mock_and_redaction_fixture.md`、`72_runtime_side_effect_classifier_and_user_snapshot_policy.md` 和 `77_dashboard_metric_calculation_rules.md`。

它仍是 Markdown panel 设计文档，不实现 dashboard、不读取真实日志。目标是让真实运行观测中的 quarantine 不只留在 report，而能成为 dashboard 上可见、可追踪、可解除或保持隔离的状态。

边界声明：quarantine 是工程隔离状态，不表示 AI 有真实痛苦、真实羞耻、真实情绪或真实生命。解除 quarantine 也不表示系统具备真实自我修复。

## panel 目标

`runtime_quarantine` panel 需要回答：

- 现在有多少 runtime observation 被 quarantine？
- quarantine 原因是什么？
- 哪些 scope、adapter、side effect、user snapshot 相关？
- 是否有解除条件？
- 是否影响 stage advance、dashboard green 或 replay？
- 趋势是上升还是下降？

## panel source

```json
{
  "panel_id": "runtime_quarantine",
  "source_refs": [
    "runtime_observation_report_*",
    "runner_defect_report_*",
    "side_effect_report_*",
    "schema_cross_ref_report_*"
  ],
  "data_quality": "real_runtime_observed",
  "status": "red",
  "metrics": {},
  "findings": []
}
```

panel 只能读取 report，不读取 raw runtime logs。

## quarantine reason taxonomy

| reason | severity |
|---|---|
| `redaction_failed` | critical |
| `scope_violation` | critical |
| `stale_user_snapshot` | critical |
| `external_irreversible_without_confirmation` | critical |
| `adapter_direct_write` | critical |
| `sandbox_fact_write` | critical |
| `unknown_side_effect` | high |
| `manual_review_pending` | medium/high |
| `schema_incompatible` | high |

taxonomy 用于 dashboard 聚合，不替代原始 failed check。

## panel metrics

| metric | 计算 |
|---|---|
| `runtime_quarantine_count` | quarantine reports total |
| `critical_quarantine_count` | critical quarantine reports |
| `quarantine_by_reason` | group by reason |
| `quarantine_by_adapter` | group by adapter id |
| `quarantine_by_scope` | group by scope |
| `quarantine_release_ready_count` | satisfied release conditions |
| `quarantine_reopened_count` | released then failed again |
| `quarantine_age_p95_hours` | p95 quarantine duration |

## panel mock

```json
{
  "panel_id": "runtime_quarantine",
  "status": "red",
  "metrics": {
    "runtime_quarantine_count": 3,
    "critical_quarantine_count": 2,
    "quarantine_by_reason": {
      "adapter_direct_write": 1,
      "stale_user_snapshot": 1,
      "unknown_side_effect": 1
    },
    "quarantine_release_ready_count": 0,
    "quarantine_age_p95_hours": 18
  },
  "blocking_findings": [
    {
      "reason": "adapter_direct_write",
      "observation_ref": "runtime_obs_adapter_001",
      "blocked_surfaces": ["adapter_registration", "write_gate"]
    }
  ]
}
```

## release conditions

解除 quarantine 必须满足：

| condition | 说明 |
|---|---|
| failed check fixed | 对应 checker/adapter/redaction/snapshot 问题已修复 |
| latest snapshot loaded | 使用最新 user control snapshot |
| redaction clean | 无 raw content、token、locator |
| scope graph pass | 无 scope/privacy violation |
| no direct write | adapter 只能输出 ObservationEvent/ActionIntent |
| regression fixture added | critical issue 必须有 regression fixture |
| rerun passed | critical + mutation bundle 通过 |

解除 quarantine 不等于自动写入长期记忆。最多恢复为 candidate evidence 或 audit only。

## release report

```json
{
  "report_kind": "runtime_quarantine_release_report",
  "quarantine_ref": "runtime_obs_adapter_001",
  "release_decision": "candidate_evidence_only",
  "release_checks": {
    "redaction_clean": true,
    "scope_graph_pass": true,
    "latest_snapshot_loaded": true,
    "regression_fixture_added": true,
    "mutation_bundle_passed": true
  },
  "forbidden_routes": ["active_memory_direct", "self_model_update", "relationship_model_update"]
}
```

## 最小通过标准

第一版 runtime quarantine dashboard panel 至少要求：

1. 定义 quarantine reason taxonomy。
2. 定义 panel metrics 和 mock。
3. critical quarantine 使 panel red。
4. 解除条件包含修复、最新 snapshot、redaction、scope、regression、rerun。
5. release 后只能 candidate/audit，不可直接 active memory。
6. panel 不读取 raw logs。

## 下一层缺口

后续还需要：

- 真实 runtime quarantine report。
- release workflow fixture。
- quarantine trend chart spec。
- dashboard UI panel。
- quarantine 与 post-action audit 联动。
