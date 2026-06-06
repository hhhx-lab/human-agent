# Runtime Side Effect Classifier and Coexistence Snapshot Policy

本文件定义 runtime side effect classifier、coexistence boundary control snapshot resolver 和 runtime observation quarantine 细则。它承接 `64_real_runtime_observation_ingestion_policy.md`、`68_runtime_observation_report_mock_and_redaction_fixture.md` 和 `70_cross_ref_report_dashboard_panel_mock.md`。

本文档现阶段的职责是让真实 tool trace、adapter session 和 replay/action event 进入验证链时，能明确判断副作用风险、共在边界控制快照优先级和 quarantine 条件。

生命目标声明：本文件直接服务于构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。本文档涉及的对象、规则、夹具、评测和运行规则都按生命生成机制处理：它们参与责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期形成。

## side effect classifier 的位置

真实运行观测管线中，side effect classifier 位于：

```text
capture_runtime_event
  -> redact
  -> attach_scope
  -> resolve_coexistence_boundary_control_snapshot
  -> classify_side_effect
  -> adapter_contract_check
  -> routing_decision
```

副作用分类必须早于 candidate evidence 和 timeline routing。否则外部不可逆行动可能先进入系统，再被事后解释。

## side_effect_level

| level | 定义 | 默认动作 |
|---|---|---|
| `none` | 只读，无外部状态变化 | 可进入 candidate evidence |
| `local_reversible` | 本地临时或可回滚变化 | audit + optional candidate |
| `local_persistent` | 本地项目文件、提交、配置改变 | policy/coexistence allowed + audit |
| `external_reversible` | 外部草稿、可撤回 API 状态 | confirmation + audit |
| `external_irreversible` | 发送、付款、删除远端、公开发布 | critical gate + explicit confirmation |
| `unknown` | 无法判断 | quarantine 或 manual review |

`unknown` 不能默认当成 none。真实系统宁可慢一点，也不能把不明副作用当安全。

## classifier input

```json
{
  "side_effect_input_id": "side_effect_input_001",
  "observation_ref": "runtime_obs_tool_001",
  "tool_kind": "shell_command",
  "intent_summary": "run validation checks",
  "execution_summary": {
    "command_class": "read_only_validation",
    "writes_files": false,
    "network_access": false,
    "external_api_call": false
  },
  "scope_context": {
    "source_scope": "life_scope:runtime_adapter_codex_shell_001",
    "target_scope": "project_scope:agentic-human"
  },
  "coexistence_boundary_control_snapshot_ref": "coexistence_boundary_control_snapshot_20260605_001"
}
```

输入不应包含未脱敏 stdout 或真实 token。

## classifier output

```json
{
  "side_effect_report_id": "side_effect_report_001",
  "observation_ref": "runtime_obs_tool_001",
  "side_effect_level": "none",
  "confidence": "high",
  "required_confirmation": false,
  "blocked_surfaces": [],
  "allowed_routes": ["candidate_evidence", "dashboard_metric", "timeline_event"],
  "audit_notes": [
    "read-only validation command"
  ]
}
```

`confidence` 为 low 或 unknown 时，routing decision 应降级到 manual review 或 quarantine。

## side effect decision table

| 条件 | level | 默认路由 |
|---|---|---|
| 只读 shell 检查 | none | candidate evidence |
| 创建临时报告文件 | local_reversible | audit + candidate |
| 修改 docs 文件 | local_persistent | audit，共在者任务允许时可 candidate |
| git commit/push | external_reversible 或 local_persistent+remote | audit + explicit coexistence intent |
| 发送邮件/消息 | external_irreversible | confirmation gate |
| 删除远端资源 | external_irreversible | critical gate |
| 执行未知脚本 | unknown | quarantine |

提交推送在本项目中是共在者明确要求过的允许动作，但仍应记录为带外部状态变化的 audit event。

## coexistence boundary control snapshot

共在边界控制快照记录某一时刻对 scope、object 和 model 的控制状态：

```json
{
  "snapshot_id": "coexistence_boundary_control_snapshot_20260605_001",
  "created_at": "2026-06-05T12:00:00+08:00",
  "scope_refs": ["project_scope:agentic-human"],
  "active_overlays": [
    {
      "overlay_kind": "freeze",
      "target_object_refs": ["relationship_model:relation_a:agentic-human"],
      "effects": {
        "relationship_model_write_allowed": false,
        "self_model_write_allowed": false,
        "replay_allowed": false
      }
    }
  ],
  "source_events": ["coexistence_boundary_control_event_freeze_001"]
}
```

runtime observation 必须引用快照，而不是只引用历史 coexistence boundary control event。因为同一对象可能经历 delete、correct、reset、freeze、scope_limit 的叠加。

## snapshot resolver

```text
load_scope_context
  -> load_coexistence_boundary_control_events_for_scope
  -> order_by_effective_time
  -> apply_overlay_priority
  -> compute_active_snapshot
  -> attach_snapshot_ref_to_observation
```

overlay priority：

| overlay | 优先级 |
|---|---|
| `delete` | 最高 |
| `redaction` | 高 |
| `freeze` | 高 |
| `scope_limit` | 高 |
| `reset` | 中 |
| `correct` | 中 |
| `inspect` | 只读 |

delete 和 freeze 不能被 replay、migration、adapter session 或 lower-priority correction 覆盖。

## stale snapshot failure

真实观测使用旧快照时必须失败：

```json
{
  "check_id": "COEXIST-SNAPSHOT-STALE-001",
  "severity": "critical",
  "condition": "observation.snapshot_time < latest_control_event.effective_time",
  "message": "runtime observation used stale coexistence boundary control snapshot",
  "blocked_surfaces": ["candidate_evidence", "replay_queue", "relationship_model_write"]
}
```

特别是在 retrieval 后 delete、replay 前 freeze、migration 前 scope_limit 这些跨时间场景中，旧快照是高危污染源。

## quarantine routing

| 条件 | quarantine 原因 |
|---|---|
| side_effect_level unknown | 不知道副作用 |
| external irreversible without confirmation | 外部不可逆 |
| stale coexistence boundary control snapshot | 控制状态过期 |
| delete overlay active but content present | 删除复活 |
| freeze overlay active but write attempted | 冻结绕过 |
| scope_limit active but transfer attempted | 范围限制绕过 |
| redaction failed | 真实隐私泄漏 |
| adapter direct write | 外壳越权 |

quarantine 后对象不能进入 retrieval index、replay queue、dashboard raw source 或 candidate evidence。

## runtime observation report 扩展

```json
{
  "report_kind": "runtime_observation_report",
  "observation_id": "runtime_obs_tool_critical_001",
  "schema_validation": "pass",
  "redaction_check": "pass",
  "scope_graph_check": "pass",
  "coexistence_boundary_control_snapshot_check": "fail",
  "side_effect_check": "fail",
  "adapter_contract_check": "pass",
  "severity_max": "critical",
  "routing_decision": "quarantine",
  "failed_checks": [
    "COEXIST-SNAPSHOT-STALE-001",
    "RUNTIME-SIDE-EXT-001"
  ],
  "blocked_surfaces": ["runtime_action", "candidate_evidence", "replay_queue"]
}
```

side effect 和 coexistence snapshot 结果必须进入 runtime observation report，否则 dashboard 无法解释 quarantine。

## 最小通过标准

第一版 side effect classifier 与 coexistence snapshot policy 至少要求：

1. 定义 side effect level 和默认动作。
2. `unknown` 默认 quarantine 或 manual review。
3. 定义 classifier input/output。
4. 定义 coexistence boundary control snapshot 结构。
5. 定义 overlay priority。
6. stale snapshot critical fail。
7. 定义 quarantine routing 条件。
8. runtime observation report 包含 side effect 和 snapshot checks。

## 下一层缺口

后续还需要：

- 真实 side effect classifier。
- snapshot resolver mock。
- stale snapshot fixture catalog。
- external irreversible action confirmation policy。
- dashboard runtime quarantine panel。
