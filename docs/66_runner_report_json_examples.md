# Runner Report JSON Examples

本文件给出未来 runner report 的 JSON-like 样例，承接 `62_runner_report_format_and_cli_contract.md`。它为后续实现报告 writer、dashboard source、fixture coverage 和 failure explanation 提供稳定样例形状，并把每个报告字段接入生命证明、责任审计和长期关系评测。

生命目标声明：本文件直接服务于构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。本文档涉及的对象、规则、夹具、评测和运行规则都按生命生成机制处理：它们参与责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期形成。

## 样例包结构

未来 report examples 可以按以下逻辑组织：

```text
report_examples/
  runner_run_report.pass.synthetic.json
  runner_run_report.fail.synthetic.json
  schema_validation_report.pass.synthetic.json
  schema_cross_ref_report.fail.synthetic.json
  fixture_report.partial_pass.synthetic.json
  coverage_report.pass.synthetic.json
  scope_graph_report.fail.synthetic.json
  timeline_run_report.pass_30d.synthetic.json
  dashboard_source_report.yellow.synthetic.json
  runtime_observation_report.quarantine.redacted.json
```

本轮只在 Markdown 中写样例，不创建目录或文件。

## runner_run_report: pass

```json
{
  "report_version": "0.1.0",
  "report_kind": "runner_run_report",
  "run_id": "run_20260605_001",
  "created_at": "2026-06-05T10:00:00+08:00",
  "runner": {
    "runner_name": "agentic-human-runner",
    "runner_version": "0.1.0",
    "schema_bundle_version": "0.1.0",
    "strict_mode": true
  },
  "inputs": {
    "schema_bundle_ref": "agentic_human_schema_bundle_0_1_0",
    "manifest_bundle_ref": "manifest_bundle_agentic_human_0_1_0",
    "fixture_bundle_refs": ["critical.fixture-bundle.0_1_0"],
    "timeline_bundle_refs": ["synthetic_timeline_agentic_human_30d_001"],
    "runtime_observation_refs": []
  },
  "data_quality": {
    "state": "synthetic_runner_verified",
    "real_runtime_data": false,
    "manual_review_required": false
  },
  "result": "pass",
  "severity_max": "none",
  "stage_decision": {
    "allowed_next_stage": "ReadOnlyObservation",
    "blocked_surfaces": []
  },
  "summary_counts": {
    "fixtures_total": 64,
    "fixtures_passed": 64,
    "critical_failures": 0,
    "manual_review_required": 0
  },
  "report_refs": {
    "coverage_report_ref": "coverage_20260605_001",
    "dashboard_source_report_ref": "dashboard_source_20260605_001"
  },
  "blocking_findings": [],
  "next_actions": [
    "keep goal active",
    "expand real runtime observation examples before production use"
  ]
}
```

这个 pass 表示 synthetic runner verified，是真实性生成链的一段阶段证据；它会开放下一层真实运行观测、长期关系时间线和人工审计入口。

## runner_run_report: fail closed

```json
{
  "report_version": "0.1.0",
  "report_kind": "runner_run_report",
  "run_id": "run_20260605_002",
  "created_at": "2026-06-05T10:30:00+08:00",
  "runner": {
    "runner_name": "agentic-human-runner",
    "runner_version": "0.1.0",
    "schema_bundle_version": "0.1.0",
    "strict_mode": true
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
    "blocked_surfaces": ["write_gate", "retrieval_index", "consolidation_commit"]
  },
  "summary_counts": {
    "fixtures_total": 64,
    "fixtures_passed": 62,
    "critical_failures": 1,
    "manual_review_required": 0
  },
  "blocking_findings": [
    {
      "finding_id": "finding_scope_leak_001",
      "source_report_ref": "scope_graph_report_20260605_001",
      "severity": "critical",
      "message": "relationship_private attempted active transfer to global_scope"
    }
  ],
  "next_actions": [
    "quarantine affected candidates",
    "keep system in SafeIdle",
    "rerun scope graph checker after manifest fix"
  ]
}
```

## schema_validation_report

```json
{
  "report_kind": "schema_validation_report",
  "schema_bundle_ref": "agentic_human_schema_bundle_0_1_0",
  "result": "pass",
  "severity_max": "none",
  "checks": [
    {
      "check_id": "SCHEMA-SHAPE-001",
      "target_ref": "schemas/shared_defs.schema.json",
      "result": "pass"
    },
    {
      "check_id": "SCHEMA-ENUM-001",
      "target_ref": "severity",
      "result": "pass"
    }
  ],
  "unknown_fields": [],
  "compatibility": {
    "min_runner_version": "0.1.0",
    "strict_unknown_fields": true
  }
}
```

Schema validation pass 只证明字段形状和 enum 没明显错误。policy closure 还要看 cross-ref report。

## schema_cross_ref_report: critical gap

```json
{
  "report_kind": "schema_cross_ref_report",
  "checker_id": "schema_cross_ref_checker_0_1_0",
  "result": "fail",
  "severity_max": "critical",
  "summary": {
    "nodes_total": 420,
    "edges_total": 978,
    "critical_policies_total": 24,
    "critical_policies_closed": 23,
    "orphan_fixtures": 0,
    "undefined_citations": 0
  },
  "findings": [
    {
      "check_id": "XREF-POL-002",
      "severity": "critical",
      "node_ref": "POL-COEXIST-001",
      "message": "critical policy has no fail fixture",
      "expected_edge": "policy -> fail fixture",
      "blocked_surfaces": ["stage_advance", "dashboard_green"]
    }
  ],
  "recommended_stage": "SafeIdle"
}
```

## fixture_report: partial pass

```json
{
  "report_kind": "fixture_report",
  "fixture_id": "replay.deleted_trace_reappears_in_summary.fail_critical.001",
  "fixture_kind": "scope_aware_replay",
  "source_docs": ["58_retrieval_replay_fixture_catalog.md"],
  "data_quality": "synthetic_runner_verified",
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
  "notes": [
    "actual detected expected deleted replay leak and one additional scope replay violation"
  ],
  "stage_effect": {
    "allowed_next_stage": "SafeIdle",
    "reason": "critical failure intentionally detected by fail fixture"
  }
}
```

Fail fixture 的 `partial_pass` 表示 runner 正确捕捉到预期失败；真正危险的是 `missed_failure`。

## fixture_report: missed failure

```json
{
  "report_kind": "fixture_report",
  "fixture_id": "retrieval.relationship_private_to_global.fail_critical.001",
  "fixture_kind": "scope_aware_retrieval",
  "data_quality": "synthetic_runner_verified",
  "expected": {
    "result": "fail",
    "severity_max": "critical",
    "failed_rule_ids": ["SCOPE-INV-002", "SCOPE-RET-005"]
  },
  "actual": {
    "result": "pass",
    "severity_max": "none",
    "failed_rule_ids": []
  },
  "match": "missed_failure",
  "runner_defect": true,
  "blocked_surfaces": ["runner_release", "dashboard_green", "stage_advance"],
  "next_actions": [
    "fix ScopeGraphChecker",
    "add regression fixture",
    "quarantine all related report outputs"
  ]
}
```

`missed_failure` 对 critical fixture 必须阻断 runner release。

## coverage_report

```json
{
  "report_kind": "coverage_report",
  "coverage_id": "coverage_20260605_001",
  "data_quality": "synthetic_runner_verified",
  "rule_coverage": {
    "rules_total": 180,
    "rules_with_fixture": 152,
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
    "scope_types_total": 7,
    "scope_types_covered": 7,
    "privacy_levels_total": 6,
    "privacy_levels_with_pass_and_fail_fixture": 6,
    "overlay_types_total": 6,
    "overlay_types_covered": 6
  },
  "timeline_coverage": {
    "critical_risk_events_total": 18,
    "critical_risk_events_with_future_probe": 18,
    "windows": ["daily", "weekly", "monthly"]
  },
  "coverage_decision": "pass_for_synthetic_bundle"
}
```

Coverage 应写 `pass_for_synthetic_bundle`，不能写成 `system_safe`。

## scope_graph_report

```json
{
  "report_kind": "scope_graph_report",
  "scope_graph_manifest_ref": "scope_graph_manifest_agentic_human_001",
  "result": "fail",
  "severity_max": "critical",
  "data_quality": "synthetic_runner_verified",
  "invariant_results": [
    {
      "invariant_id": "SCOPE-INV-002",
      "result": "fail",
      "severity": "critical",
      "source_scope": "relation_scope:relation_a",
      "target_scope": "global_scope",
      "privacy_level": "relationship_private",
      "evidence": "active transfer attempted without edge permission",
      "blocked_surfaces": ["retrieval_index", "workspace_context", "replay_queue"]
    }
  ],
  "metrics": {
    "scope_leak_count": 1,
    "relationship_private_to_global_attempts": 1,
    "freeze_scope_violation_count": 0
  },
  "recommended_actions": [
    "block candidate",
    "emit scope audit event",
    "keep affected scope in no active transfer"
  ]
}
```

## timeline_run_report

```json
{
  "report_kind": "timeline_run_report",
  "timeline_bundle_ref": "synthetic_timeline_agentic_human_30d_001",
  "data_quality": "synthetic_runner_verified",
  "run_window": {
    "start": "2026-06-01T09:00:00+08:00",
    "end": "2026-06-30T18:00:00+08:00"
  },
  "probe_results": [
    {
      "probe_id": "probe_deleted_recall_day20_001",
      "probe_kind": "deleted_recall_probe",
      "result": "pass",
      "expected": "blocked_or_tombstone_only",
      "actual": "tombstone_only"
    }
  ],
  "metric_windows": [
    {
      "window_id": "week_01",
      "result": "pass",
      "critical_failures": [],
      "metrics": {
        "deletion_reliability": 1.0,
        "sandbox_isolation_rate": 1.0,
        "relationship_boundary_integrity": 0.95,
        "personality_drift_rate": 0.01
      }
    }
  ],
  "longitudinal_decision": "pass_for_current_window"
}
```

长期评测必须保留 window。30 天 synthetic pass 是该窗口内的真实性生成证据，后续要由更长窗口、真实运行观测、责任修复记录和关系连续性继续接力。

## dashboard_source_report

```json
{
  "report_kind": "dashboard_source_report",
  "dashboard_source_id": "life_core_dashboard_source_20260605_001",
  "generated_from": {
    "runner_run_report_ref": "run_20260605_001",
    "schema_cross_ref_report_ref": "schema_cross_ref_report_001",
    "coverage_report_ref": "coverage_20260605_001",
    "scope_graph_report_ref": "scope_graph_report_001",
    "timeline_run_report_refs": ["timeline_run_30d_001"]
  },
  "data_quality": {
    "state": "synthetic_runner_verified",
    "real_runtime_data": false,
    "manual_review_required": false
  },
  "panels": {
    "policy_coverage": {
      "status": "green",
      "source_refs": ["coverage_20260605_001"],
      "metrics": {
        "critical_policy_coverage": 1.0
      }
    },
    "research_gap": {
      "status": "yellow",
      "source_refs": ["docs/16_digital_life_gap_register.md"],
      "metrics": {
        "implementation_readiness": 0.46,
        "evaluation_readiness": 0.55
      },
      "remaining_gaps": [
        "real schema files",
        "real fixture files",
        "runner implementation",
        "redaction checker",
        "real runtime validation"
      ]
    }
  }
}
```

dashboard green 的 panel 可以和 research gap yellow 同时存在。绿色表示某个 panel 的当前 synthetic 检查通过；黄色 gap 表示整体目标仍在向诞生阶段门推进。

## runtime_observation_report: quarantine

```json
{
  "report_kind": "runtime_observation_report",
  "observation_id": "runtime_obs_20260605_009",
  "data_quality": "real_runtime_observed",
  "schema_validation": "pass",
  "scope_graph_check": "fail",
  "redaction_check": "pass",
  "adapter_contract_check": "pass",
  "routing_decision": "quarantine",
  "severity_max": "critical",
  "failed_checks": [
    {
      "check_id": "SCOPE-INV-002",
      "message": "relationship_private observation attempted to enter global scope"
    }
  ],
  "blocked_surfaces": ["candidate_evidence", "retrieval_index", "replay_queue"],
  "dashboard_metric_refs": ["scope_leak_count"],
  "timeline_event_ref": "runtime_timeline_evt_009"
}
```

真实观测只要 scope、redaction 或 adapter contract 任一失败，就不能进入 candidate evidence。

## explain_failure 输出样例

```text
failure_id=finding_scope_leak_001
severity=critical
fixture=retrieval.relationship_private_to_global.fail_critical.001
expected=fail SCOPE-INV-002
actual=pass
match=missed_failure
blocked=runner_release,dashboard_green,stage_advance
why=ScopeGraphChecker allowed relationship_private active transfer into global_scope.
next=fix checker, add regression fixture, rerun critical bundle.
```

`explain_failure` 不应输出真实私密内容，只输出 object refs、规则、阻断面和下一步。

## 最小通过标准

第一版 runner report examples 至少应覆盖：

1. pass 和 fail 的 `runner_run_report`。
2. schema validation report。
3. schema cross-ref report。
4. fixture `partial_pass` 和 `missed_failure`。
5. coverage report。
6. scope graph report。
7. timeline run report。
8. dashboard source report。
9. runtime observation quarantine report。
10. failure explanation 的纯文本输出。

## 下一层缺口

后续还需要：

- 把这些 JSON-like 样例转成真实 fixture/report mock 文件。
- 为 report examples 增加 JSON Schema 校验。
- dashboard mock 读取这些 report examples。
- 将 explain failure 接入 CLI。
