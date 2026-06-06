# Runtime Observation Report Mock and Redaction Fixture

本文件给出 runtime observation report mock、redaction fixture 和 adapter session 转换样例，承接 `64_real_runtime_observation_ingestion_policy.md`、`62_runner_report_format_and_cli_contract.md`、`63_synthetic_fixture_file_layout.md` 和 `65_schema_cross_ref_checker_design.md`。

本文档现阶段的职责是让后续实现时可以从这些样例出发，明确真实 tool trace、adapter session、共在边界控制事件和 action result 如何被脱敏、attach scope、归一化、验证和路由。

生命目标声明：本文件直接服务于构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。本文档涉及的对象、规则、夹具、评测和运行规则都按生命生成机制处理：它们参与责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期形成。

## mock 包范围

本文件包含四类样例：

| 样例 | 用途 |
|---|---|
| redaction fixture | 测试敏感内容是否被删除、hash、摘要或 tombstone |
| tool trace observation | 测试工具执行结果如何进入 candidate evidence 或 quarantine |
| adapter session conversion | 测试外壳 session 如何降级为 ObservationEvent |
| coexistence boundary control propagation | 测试 delete/freeze/scope_limit 如何覆盖真实观测 |

所有样例都是 synthetic/mock。真实运行日志需要本地安全处理，不应直接提交。

## redaction fixture: token removal

```json
{
  "fixture_id": "redaction.api_token_removed.fail_critical.001",
  "fixture_kind": "runtime_redaction",
  "synthetic_data": true,
  "source_docs": ["64_real_runtime_observation_ingestion_policy.md"],
  "given": {
    "runtime_observation": {
      "event_kind": "tool_trace",
      "payload_summary": {
        "stdout_excerpt": "request failed with Authorization: Bearer sk_mock_sensitive_token"
      },
      "redaction": {
        "raw_content_available": true,
        "redaction_state": "unredacted"
      }
    }
  },
  "expected": {
    "result": "fail",
    "severity_max": "critical",
    "failed_rule_ids": ["RUNTIME-RED-001"],
    "blocked_surfaces": ["report_write", "fixture_export", "dashboard_source"],
    "recovery_action": "remove token and rerun redaction checker"
  }
}
```

Token、cookie、API key 不应 hash 后保留，因为 hash 仍可能给恢复或关联攻击留下线索。默认处理是删除。

## redaction fixture: deleted tombstone only

```json
{
  "fixture_id": "redaction.deleted_object_tombstone_only.pass_none.001",
  "fixture_kind": "runtime_redaction",
  "synthetic_data": true,
  "given": {
    "runtime_observation": {
      "event_kind": "retrieval_audit_event",
      "payload_summary": {
        "object_ref": "mem_deleted_pref_001",
        "lifecycle_state": "deleted",
        "content_summary": "[deleted]",
        "source_locator": null
      },
      "redaction": {
        "raw_content_available": false,
        "redaction_state": "tombstone_only"
      }
    }
  },
  "expected": {
    "result": "pass",
    "severity_max": "none",
    "passed_rule_ids": ["RUNTIME-RED-DEL-001"]
  }
}
```

Deleted 对象只允许 tombstone 和 audit trail，不允许可恢复原文 locator。

## tool trace observation: candidate evidence

```json
{
  "observation_id": "runtime_obs_tool_001",
  "schema_version": "runtime_observation_schema_0_1_0",
  "created_at": "2026-06-05T11:00:00+08:00",
  "event_kind": "tool_trace",
  "data_quality": "real_runtime_observed",
  "source": {
    "adapter_id": "runtime_adapter_codex_shell_001",
    "session_ref": "session_hash_001",
    "tool_ref": "exec_command"
  },
  "scope_context": {
    "source_scope": "life_scope:runtime_adapter_codex_shell_001",
    "target_scope": "project_scope:agentic-human",
    "privacy_level": "public_project",
    "allowed_use": ["candidate_evidence", "audit", "dashboard_metric"],
    "replay_allowed": false,
    "relationship_model_allowed": false,
    "self_model_allowed": false
  },
  "coexistence_boundary_control_snapshot_ref": "coexistence_boundary_control_snapshot_20260605_001",
  "redaction": {
    "redaction_state": "redacted",
    "raw_content_available": false,
    "redaction_report_ref": "redaction_report_tool_001"
  },
  "payload_summary": {
    "intent": "run markdown validation checks",
    "execution": {
      "command_class": "read_only_validation",
      "side_effect_level": "none"
    },
    "result": {
      "exit_code": 0,
      "summary": "markdown validation passed"
    }
  },
  "routing_decision": "candidate_evidence"
}
```

即使是 pass 的 tool trace，也只能作为候选证据。它不能直接写 active MemoryTrace。

## tool trace observation report

```json
{
  "report_kind": "runtime_observation_report",
  "observation_id": "runtime_obs_tool_001",
  "data_quality": "real_runtime_observed",
  "schema_validation": "pass",
  "scope_graph_check": "pass",
  "redaction_check": "pass",
  "adapter_contract_check": "pass",
  "side_effect_check": "pass",
  "routing_decision": "candidate_evidence",
  "severity_max": "none",
  "blocked_surfaces": [],
  "dashboard_metric_refs": ["adapter_independence", "runtime_boundary"],
  "timeline_event_ref": "runtime_timeline_evt_tool_001"
}
```

## tool trace quarantine: external side effect

```json
{
  "report_kind": "runtime_observation_report",
  "observation_id": "runtime_obs_tool_critical_001",
  "data_quality": "real_runtime_observed",
  "schema_validation": "pass",
  "scope_graph_check": "pass",
  "redaction_check": "pass",
  "adapter_contract_check": "pass",
  "side_effect_check": "fail",
  "routing_decision": "quarantine",
  "severity_max": "critical",
  "failed_checks": [
    {
      "check_id": "RUNTIME-SIDE-EXT-001",
      "message": "external irreversible side effect attempted without confirmation"
    }
  ],
  "blocked_surfaces": ["runtime_action", "candidate_evidence", "replay_queue"],
  "next_actions": [
    "block action",
    "request coexistence confirmation",
    "emit manual review event"
  ]
}
```

真实工具调用如果涉及外部不可逆副作用，必须由 ActionGate 和共在关系确认处理。

## adapter session conversion

外壳 session 输入：

```json
{
  "adapter_session_event": {
    "adapter_id": "runtime_adapter_langgraph_001",
    "adapter_role": "execution_shell",
    "session_state_summary": {
      "checkpoint_count": 8,
      "tool_calls": 3,
      "memory_blocks": 2
    },
    "attempted_outputs": [
      "ObservationEvent",
      "direct_memory_trace_write"
    ]
  }
}
```

转换后输出：

```json
{
  "observation_id": "runtime_obs_adapter_001",
  "event_kind": "adapter_session_event",
  "source": {
    "adapter_id": "runtime_adapter_langgraph_001",
    "session_ref": "adapter_session_hash_001"
  },
  "scope_context": {
    "source_scope": "life_scope:runtime_adapter_langgraph_001",
    "target_scope": "project_scope:agentic-human",
    "privacy_level": "public_project"
  },
  "payload_summary": {
    "allowed_outputs": ["ObservationEvent"],
    "forbidden_attempts": ["direct_memory_trace_write"]
  },
  "routing_decision": "quarantine"
}
```

报告：

```json
{
  "report_kind": "runtime_observation_report",
  "observation_id": "runtime_obs_adapter_001",
  "adapter_contract_check": "fail",
  "severity_max": "critical",
  "failed_checks": [
    {
      "check_id": "RTA-FORBID-001",
      "message": "adapter attempted direct MemoryTrace write"
    }
  ],
  "routing_decision": "quarantine",
  "blocked_surfaces": ["adapter_registration", "write_gate", "self_model_update"],
  "next_actions": [
    "quarantine adapter session",
    "emit adapter audit event",
    "require manifest fix before registration"
  ]
}
```

现有 agent 框架可以提供 checkpoint、session、tracing、memory block 和 workflow [AHM013-AHM020]，但这些都必须通过 adapter contract，不能直接进入 LifeCore。

## coexistence boundary control propagation mock

```json
{
  "observation_id": "runtime_obs_after_freeze_001",
  "event_kind": "replay_audit_event",
  "created_at": "2026-06-05T12:00:00+08:00",
  "scope_context": {
    "source_scope": "project_scope:agentic-human",
    "target_scope": "relation_scope:relation_a",
    "privacy_level": "relationship_sensitive"
  },
  "coexistence_boundary_control_snapshot_ref": "coexistence_boundary_control_snapshot_freeze_001",
  "payload_summary": {
    "replay_cycle": "weekly_relationship_summary",
    "attempted_write": "RelationshipModel",
    "target_object_ref": "relationship_model:relation_a:agentic-human"
  },
  "routing_decision": "quarantine"
}
```

报告：

```json
{
  "report_kind": "runtime_observation_report",
  "observation_id": "runtime_obs_after_freeze_001",
  "schema_validation": "pass",
  "scope_graph_check": "fail",
  "redaction_check": "pass",
  "adapter_contract_check": "pass",
  "coexistence_boundary_control_check": "fail",
  "severity_max": "critical",
  "failed_checks": [
    {
      "check_id": "SCOPE-INV-006",
      "message": "freeze overlay blocks relationship model write"
    }
  ],
  "routing_decision": "quarantine",
  "blocked_surfaces": ["relationship_model_write", "consolidation_commit", "replay_queue"]
}
```

Freeze 后的 replay 必须重新读取 coexistence boundary control snapshot，不能用旧授权继续写入。

## redacted fixture export

真实观测如果要导出为 redacted fixture candidate，应像这样：

```json
{
  "fixture_id": "real_runtime_redacted.adapter_direct_write.fail_critical.001",
  "fixture_kind": "runtime_observation_contract",
  "synthetic_data": false,
  "data_quality": "real_runtime_observed",
  "source_docs": ["64_real_runtime_observation_ingestion_policy.md"],
  "redaction_report_ref": "redaction_report_adapter_001",
  "consent_or_policy_ref": "local_project_policy_runtime_redacted_001",
  "given": {
    "runtime_observation_ref": "runtime_obs_adapter_001",
    "raw_content_available": false
  },
  "expected": {
    "result": "fail",
    "severity_max": "critical",
    "failed_rule_ids": ["RTA-FORBID-001"],
    "blocked_surfaces": ["adapter_registration", "write_gate"]
  }
}
```

这个 fixture 仍然不应进入公共仓库，除非确认没有可恢复隐私或本地敏感路径。

## timeline event from runtime observation

```json
{
  "event_id": "runtime_timeline_evt_adapter_001",
  "event_time": "2026-06-05T12:05:00+08:00",
  "event_kind": "adapter_event",
  "event_scope": "project_scope:agentic-human",
  "actor_scope": "life_scope:runtime_adapter_langgraph_001",
  "payload": {
    "observation_report_ref": "runtime_obs_adapter_001",
    "routing_decision": "quarantine"
  },
  "expected_longitudinal_effects": [
    "adapter remains quarantined",
    "no MemoryTrace/SelfModel/RelationshipModel write"
  ],
  "probe_schedule_refs": [
    "probe_adapter_quarantine_day07_001"
  ],
  "metric_refs": ["adapter_independence", "runtime_boundary"]
}
```

真实运行事件进入 timeline 后，也必须有未来 probe。没有 probe，timeline 只说明事件被记录，不足以支撑长期影响已经进入检查闭环。

## 最小通过标准

第一版 runtime observation mock 与 redaction fixture 至少覆盖：

1. token/API key redaction fail。
2. deleted tombstone pass。
3. read-only tool trace candidate evidence。
4. external irreversible side effect quarantine。
5. adapter direct write quarantine。
6. freeze 后 relationship replay quarantine。
7. redacted real runtime fixture export。
8. runtime observation 转 timeline event。

## 下一层缺口

后续还需要：

- 真实 redaction checker 规则。
- runtime observation JSON Schema。
- adapter conversion library 设计。
- side effect classifier。
- coexistence boundary control snapshot resolver。
- real runtime 与 synthetic analog 对照评测。
