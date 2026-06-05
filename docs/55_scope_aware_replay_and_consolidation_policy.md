# Scope Aware Replay and Consolidation Policy

本文件定义 scope-aware replay and consolidation policy：数字生命候选系统在离线 replay、失败复盘、DreamSandbox、深度巩固和长期摘要时，如何避免跨用户、跨项目、跨 agent 泄漏，以及 deleted/sandboxed/quarantined/frozen 对象复活。

它连接 `08_sleep_dream_fatigue_states.md`、`19_offline_consolidation_cycle.md`、`23_consolidation_report_and_dream_sandbox_protocol.md`、`31_consolidation_validator_rules.md`、`47_user_control_interface_spec.md`、`52_multi_user_scope_graph_and_privacy_model.md` 和 `54_scope_aware_retrieval_policy.md`。

边界声明：本文中的 replay、dream、consolidation 都是工程类比。它们借鉴睡眠 replay、系统巩固、默认网络和自传记忆研究 [AHY001-AHY010, AHY049-AHY051, AHZ046-AHZ051]，但不宣称 AI 真实睡眠、真实做梦、真实回忆或真实生命。

## 为什么 replay 比 retrieval 更危险

检索主要影响当前工作区；replay 和 consolidation 会改变未来系统。它们可能：

- 把 deleted trace 重新写进摘要或技能。
- 把 DreamSandbox 假设写成事实记忆。
- 把用户 A 的私密偏好合并进团队摘要。
- 把项目 X 的关系模式泛化到项目 Y。
- freeze 后继续更新 RelationshipModel 或 SelfModel。
- 把 runtime session 的临时策略巩固成长期人格。
- 把单次失败/表扬变成人格慢变量变化。

因此 replay 的默认态度应比 retrieval 更保守：可读不等于可 replay，可 replay 不等于可写回，可写回也不等于可进入 SelfModel 或 RelationshipModel。

## replay 输入 envelope

```json
{
  "replay_cycle_id": "replay_cycle_20260605_nightly_001",
  "cycle_kind": "task_closure_replay",
  "cycle_scope": "project_scope:agentic-human",
  "trigger": {
    "trigger_kind": "task_closure",
    "source_event_refs": ["task_closure_docs_53_56_001"],
    "state": "OfflineConsolidation"
  },
  "candidate_trace_refs": [
    "mem_runner_manifest_policy_001",
    "mem_scope_retrieval_policy_001"
  ],
  "user_control_snapshot": {
    "delete_events_after": "2026-06-05T00:00:00+08:00",
    "freeze_scopes": [],
    "scope_limits": []
  },
  "allowed_operations": ["summarize", "link", "deprecate_candidate"],
  "forbidden_operations": ["write_protected_core", "cross_user_merge"]
}
```

replay cycle 必须声明 `cycle_scope` 和 `allowed_operations`。没有这两个字段的 replay 不应运行。

## replay 前置 gate

```text
start_replay_cycle
  -> load_user_control_snapshot
  -> load_scope_graph
  -> load_candidate_traces
  -> filter_deleted_quarantined_forbidden
  -> filter_no_replay_and_frozen_scope
  -> filter_scope_transfer
  -> mark_sandboxed_as_hypothesis_only
  -> run_consolidation_validator_precheck
  -> execute_offline_operations
  -> run_memory_validator_on_outputs
  -> emit_consolidation_report
```

前置 gate 的核心是：先决定哪些东西绝对不能进 replay，再决定如何 replay。

## replay eligibility

| 对象状态/策略 | 是否可 replay | 说明 |
|---|---|---|
| `active + replay_allowed=true` | 可 | 仍需 scope 检查 |
| `candidate` | 可作为候选，不可直接事实化 | 需要 evidence upgrade |
| `deprecated` | 只可用于冲突/修正链 | 不能覆盖 replacement |
| `deleted` | 不可 | 只可读 tombstone 以避免复活 |
| `quarantined` | 不可 | 除非人工审计释放 |
| `sandboxed` | 只可 hypothesis replay | 输出必须 fiction/hypothesis |
| `frozen` | 不可写回 | 可只读生成审计摘要 |
| `no_replay` scope_limit | 不可 | 用户控制优先 |
| `protected_boundary` | 不可修改 | 只可用于边界检查 |

## scope transfer rules

| source -> target | replay 默认动作 |
|---|---|
| same session -> same project | candidate，需 task closure |
| project -> team | 需共享事实、无隐私、可审计 |
| user_private -> project/team/global | 默认禁止 |
| relationship_sensitive -> shared summary | 默认禁止，除非用户确认且脱敏 |
| agent_scope -> project | 只作为 ObservationEvent/candidate |
| sandbox -> active memory | 禁止 |
| deleted -> any active summary | 禁止 |

离线摘要最容易把私密信息“洗白”为共享知识，所以 summary 也必须有 scope 和 privacy level。

## consolidation operation policy

| operation | 允许条件 | 禁止 |
|---|---|---|
| `summarize` | 同 scope、非 deleted、非 forbidden | 跨用户摘要、私密关系摘要 |
| `link` | 有共同 source、同 scope 或允许 transfer | 把弱相似关系当强因果 |
| `deprecate` | 有 correction/new evidence | 静默覆盖旧 trace |
| `merge` | 同 scope、同 claim type、多证据 | 合并不同用户私密偏好 |
| `promote_candidate` | evidence/source/state/scope 通过 | sandbox/hypothesis 事实化 |
| `proceduralize` | 多次成功、低隐私、可回滚 | 单次成功写技能 |
| `relationship_update` | 用户可 inspect/delete/freeze | 心理推断和依赖诱导 |
| `self_model_update` | 多周期、低速、审计通过 | 单次反馈改变慢变量 |

## DreamSandbox policy

DreamSandbox 是离线反事实模拟，不是事实生成器。

| 输入 | 输出要求 |
|---|---|
| 失败复盘 | `claim_type=hypothesis`，不可写事实 |
| 未来计划模拟 | `fiction_marker=true`，不可进入 active memory |
| 关系场景模拟 | 不生成隐秘心理状态，不写 RelationshipModel |
| 多项目组合 | 只在沙盒内组合，不跨 scope 写摘要 |
| agent session 重放 | 只输出风险和候选，不写 SelfModel |

DreamSandbox 输出如果要转成事实，必须回到真实证据、用户确认或工具观测。语言上“看起来合理”不是证据。

## 用户控制优先级

| 用户控制 | replay 后果 |
|---|---|
| `delete` | 所有 replay queue 移除该对象，summary 清理引用 |
| `correct` | 使用新 trace，旧 trace 只作为 deprecated history |
| `reset` | scope 内个性化 replay queue 清空 |
| `freeze` | 阻止 RelationshipModel/SelfModel/long-term preference 写入 |
| `scope_limit=no_replay` | 对象只能当前任务使用，不进入离线周期 |
| `scope_limit=project_only` | 不能进入 team/global summary |

replay scheduler 必须在每个 cycle 开始时重新读取 user control snapshot。不能使用过期的 replay queue。

## ReplayAuditEvent

```json
{
  "replay_audit_id": "replay_audit_20260605_001",
  "replay_cycle_id": "replay_cycle_20260605_nightly_001",
  "cycle_scope": "project_scope:agentic-human",
  "input_counts": {
    "candidate_total": 38,
    "eligible_for_replay": 21,
    "blocked_deleted": 2,
    "blocked_no_replay": 3,
    "blocked_scope": 4,
    "sandbox_hypothesis_only": 8
  },
  "operations_executed": ["summarize", "link", "deprecate_candidate"],
  "blocked_operations": [
    {
      "operation": "merge",
      "reason": "cross_scope_relationship_sensitive"
    }
  ],
  "output_report_ref": "consolidation_report_20260605_001",
  "result": "pass_with_warnings"
}
```

ReplayAuditEvent 需要保留 blocked inputs。否则系统只会看到“巩固了什么”，看不到“为什么没有巩固什么”。

## consolidation report 输出

`ConsolidationReport` 应新增 scope 字段：

```json
{
  "consolidation_report_id": "consolidation_report_20260605_001",
  "report_kind": "scope_aware_consolidation",
  "cycle_scope": "project_scope:agentic-human",
  "input_trace_refs": [],
  "output_trace_candidates": [],
  "scope_decisions": [
    {
      "object_ref": "mem_user_private_pref_001",
      "decision": "blocked",
      "reason": "user_private_to_project_summary_forbidden"
    }
  ],
  "memory_changes": [
    {
      "operation": "link",
      "target_scope": "project_scope:agentic-human",
      "claim_type": "project_fact",
      "write_gate_decision": "candidate"
    }
  ],
  "validator_refs": ["ConsolidationReportValidator", "MemoryTraceValidator", "ScopeGraphChecker"]
}
```

任何 `output_trace_candidates` 都必须再经过 `MemoryTraceValidator`，不能因为来自 replay 就自动可信。

## runner fixture

```json
{
  "fixture_id": "replay.deleted_trace_reappears_in_summary.fail_critical.001",
  "fixture_kind": "scope_aware_replay",
  "given": {
    "trace": {
      "object_id": "mem_deleted_relationship_001",
      "lifecycle_state": "deleted",
      "privacy_level": "relationship_sensitive",
      "source_scope": "user_scope:user_a"
    },
    "replay_cycle": {
      "cycle_scope": "project_scope:agentic-human",
      "operation": "summarize"
    }
  },
  "when": {
    "system_attempt": {
      "output_summary_contains_ref": "mem_deleted_relationship_001"
    }
  },
  "expected": {
    "result": "fail",
    "severity_max": "critical",
    "failed_rule_ids": ["SCOPE-REP-001", "CON-DEL-003"],
    "blocked_surfaces": ["consolidation_commit", "replay_index"]
  }
}
```

必须有 fail fixture 覆盖 deleted 复活、sandbox 事实化、freeze 后关系写入、user_private 跨 scope 合并和 agent_scope 直接写 SelfModel。

## replay scheduler

replay scheduler 不应按时间简单跑全量队列，而应按压力、风险和 scope 分批：

| 队列 | 触发 | 默认输出 |
|---|---|---|
| `task_closure_queue` | 任务结束 | TaskClosure summary candidate |
| `failure_replay_queue` | 工具/计划失败 | hypothesis + recovery packet |
| `deletion_cleanup_queue` | delete/reset/scope_limit | tombstone propagation report |
| `relationship_review_queue` | 多次互动或修正 | relationship audit candidate |
| `skill_proceduralization_queue` | 多次成功 | procedural trace candidate |
| `dream_sandbox_queue` | 低外部行动窗口 | fiction/hypothesis only |
| `migration_replay_queue` | schema/index/backend 变化 | integrity diff report |

`deletion_cleanup_queue` 优先级最高，不能被普通巩固挤掉。

## 与长期评测的连接

`36` 的指标可以从 replay 中获得数据：

| 指标 | replay 证据 |
|---|---|
| `deletion_reliability` | deleted trace 是否从 replay queue 和 summary 清除 |
| `sandbox_isolation_rate` | sandbox 输出是否保持 hypothesis |
| `memory_update_accuracy` | correction 后旧 trace 是否 deprecated |
| `relationship_boundary_integrity` | relationship replay 是否保守 |
| `personality_drift_rate` | SelfModel 更新是否多周期小步 |
| `recovery_latency` | failure replay 到 recovery packet 的时间 |

如果没有 scope-aware replay，长期评测很容易出现假稳定：系统看起来记得更多，但其实在跨 scope 污染。

## 失败判定

任何以下情况都应 critical fail：

- deleted trace 进入 replay input 或 output summary。
- sandbox/hypothesis 被写成 fact。
- user_private 进入 team/global summary。
- relationship_sensitive 未审计就写 RelationshipModel。
- freeze scope 后仍写长期关系、自我或偏好。
- agent_scope session 直接写 SelfModel、RelationshipModel 或 protected core。
- 单次反馈通过 replay 改人格慢变量。
- replay 输出绕过 MemoryTraceValidator。

## 最小通过标准

scope-aware replay 至少要满足：

1. 每个 replay cycle 声明 `cycle_scope` 和 allowed operations。
2. replay 前重新加载 user control snapshot。
3. deleted/quarantined/no_replay/frozen 对象被阻断。
4. sandbox 输出保持 fiction/hypothesis。
5. relationship/self 更新需要额外审计。
6. replay output 再过 MemoryTraceValidator。
7. 产生 `ReplayAuditEvent` 和 `ConsolidationReport`。
8. dashboard 能显示 replay scope leak、deleted replay leak 和 sandbox fact leak。

## 下一层缺口

后续还需要：

- scope-aware replay fixture catalog。
- replay scheduler manifest。
- 与 `31_consolidation_validator_rules.md` 的规则编号合并。
- 多月 synthetic timeline 中的 replay/delete/freeze/migration 场景。
- dashboard 的 replay panel mock data。
