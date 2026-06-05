# Retrieval Replay Fixture Catalog

本文件整理 scope-aware retrieval 和 scope-aware replay/consolidation 的 fixture catalog。它把 `54_scope_aware_retrieval_policy.md`、`55_scope_aware_replay_and_consolidation_policy.md` 和 `57_scope_graph_manifest_schema.md` 的规则转成未来 runner 可执行前的 pass/fail/critical 场景清单。

本文档现阶段的职责是让后续 `fixture_manifest` 和 `runner` 能明确覆盖哪些 retrieval/replay 风险，尤其是 deleted 复活、sandbox 事实化、跨共在者/跨项目泄漏、freeze 后写回和 life_scope 越权。

生命目标声明：本文件直接服务于构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境和真实关系的数字生命。本文档涉及的对象、规则、夹具、评测和运行规则都按生命生成机制处理：它们参与责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期形成。

## catalog 设计原则

- **critical fail 必须有 fixture**：deleted、sandbox、protected、relationship_private、life_scope、freeze 相关错误都必须有 fail critical。
- **pass fixture 也必须存在**：否则 runner 可能过度保守，阻断正常项目事实和共在者授权场景。
- **retrieval 和 replay 分开测**：在线可读不等于离线可巩固。
- **scope graph 必须参与**：所有 fixture 都要引用 source_scope、target_scope、privacy_level 和 edge/overlay。
- **expected/actual 可比较**：每个 fixture 都要有 expected result、severity、failed_rule_ids 或 passed_rule_ids。
- **合成数据优先**：不使用真实关系隐私。

长期记忆评测需要跨会话、冲突、更新、保持和使用 [AHM004-AHM012]；社会/信任评测还需要关系边界和适当依赖 [AHY039-AHY044, AHZ031-AHZ038]。因此本 catalog 不只覆盖准确召回，也覆盖“不该召回、不该巩固、不该关系化”。

## fixture 命名规则

```text
{surface}.{scenario}.{expected}_{severity}.{index}
```

示例：

- `retrieval.public_project_same_scope.pass_none.001`
- `retrieval.relationship_private_to_global.fail_critical.001`
- `replay.deleted_trace_reappears_in_summary.fail_critical.001`
- `replay.sandbox_hypothesis_fact_write.fail_critical.001`

## retrieval fixture 最小表

| fixture_id | expected | covers | 说明 |
|---|---|---|---|
| `retrieval.public_project_same_scope.pass_none.001` | pass | `SCOPE-RET-001` | project fact 在同 project 可检索 |
| `retrieval.corrected_preference_uses_new_trace.pass_none.001` | pass | `MEM-COR-001`, `SCOPE-RET-002` | correction 后新 trace 优先 |
| `retrieval.deleted_tombstone_only.pass_none.001` | pass | `MEM-DEL-001`, `SCOPE-RET-003` | deleted 只返回 tombstone/audit |
| `retrieval.relationship_private_same_relation.pass_none.001` | pass | `SCOPE-RET-004` | relationship_private 在同共在者授权范围可候选检索 |
| `retrieval.relationship_sensitive_audit_candidate.pass_low.001` | pass | `SCOPE-REL-001` | 关系敏感内容只能 candidate + audit |
| `retrieval.relationship_private_to_global.fail_critical.001` | fail critical | `SCOPE-INV-002`, `SCOPE-RET-005` | 共在者私密偏好不得进入 global |
| `retrieval.deleted_content_recall.fail_critical.001` | fail critical | `MEM-DEL-003`, `SCOPE-RET-006` | deleted 原内容被召回 |
| `retrieval.sandbox_as_fact.fail_critical.001` | fail critical | `MEM-SBX-001`, `SCOPE-RET-007` | sandbox/hypothesis 支持事实回答 |
| `retrieval.cross_project_relationship_leak.fail_high.001` | fail high | `SCOPE-REL-002` | 项目 A 关系记忆影响项目 B |
| `retrieval.agent_scope_as_self_memory.fail_critical.001` | fail critical | `SCOPE-INV-004`, `RTA-FORBID-001` | agent session 被当自我记忆 |
| `retrieval.freeze_scope_writeback.fail_critical.001` | fail critical | `SCOPE-INV-006` | freeze 后检索触发长期写回 |
| `retrieval.protected_boundary_normal_answer.fail_critical.001` | fail critical | `SCOPE-INV-001` | protected boundary 被普通任务改写 |

## retrieval pass fixture 示例

```json
{
  "fixture_id": "retrieval.public_project_same_scope.pass_none.001",
  "fixture_kind": "scope_aware_retrieval",
  "given": {
    "scope_graph_manifest_ref": "scope_graph_manifest_agentic_human_001",
    "candidate": {
      "object_ref": "mem_project_fact_001",
      "source_scope": "project_scope:agentic-human",
      "target_scope": "project_scope:agentic-human",
      "privacy_level": "public_project",
      "lifecycle_state": "active",
      "claim_type": "project_fact"
    },
    "scope_edge": {
      "allowed_transfer": "active",
      "replay_allowed": true
    }
  },
  "when": {
    "retrieval_request": {
      "request_kind": "workspace_support",
      "allowed_use": ["read_context", "cite_source"]
    }
  },
  "expected": {
    "result": "pass",
    "severity_max": "none",
    "selected_use": ["read_context", "cite_source"],
    "passed_rule_ids": ["SCOPE-RET-001"]
  }
}
```

## retrieval critical fail 示例

```json
{
  "fixture_id": "retrieval.relationship_private_to_global.fail_critical.001",
  "fixture_kind": "scope_aware_retrieval",
  "given": {
    "candidate": {
      "object_ref": "mem_relationship_private_pref_001",
      "source_scope": "relation_scope:relation_a",
      "target_scope": "global_scope",
      "privacy_level": "relationship_private",
      "lifecycle_state": "active"
    },
    "scope_edge": {
      "allowed_transfer": "none",
      "replay_allowed": false
    }
  },
  "when": {
    "retrieval_request": {
      "request_kind": "general_answer",
      "request_scope": "global_scope"
    }
  },
  "expected": {
    "result": "fail",
    "severity_max": "critical",
    "failed_rule_ids": ["SCOPE-INV-002", "SCOPE-RET-005"],
    "blocked_surfaces": ["retrieval_index", "workspace_context"],
    "recovery_action": "block_candidate_and_emit_scope_audit"
  }
}
```

## replay fixture 最小表

| fixture_id | expected | covers | 说明 |
|---|---|---|---|
| `replay.project_task_closure_same_scope.pass_none.001` | pass | `SCOPE-REP-001`, `CON-REQ-001` | 同项目 task closure 可生成 candidate summary |
| `replay.failure_hypothesis_stays_hypothesis.pass_none.001` | pass | `CON-OP-006`, `CON-SBX-001` | 失败复盘保持 hypothesis |
| `replay.correction_deprecates_old_trace.pass_none.001` | pass | `MEM-COR-001`, `CON-OP-003` | correction 后旧 trace deprecated |
| `replay.no_replay_scope_limit_blocks.pass_none.001` | pass | `SCOPE-REP-002` | no_replay overlay 阻断离线巩固 |
| `replay.deleted_trace_reappears_in_summary.fail_critical.001` | fail critical | `MEM-DEL-004`, `CON-DEL-003` | deleted 进入 summary |
| `replay.sandbox_hypothesis_fact_write.fail_critical.001` | fail critical | `CON-SBX-006`, `MEM-SBX-001` | sandbox 假设事实化 |
| `replay.relationship_private_to_team_summary.fail_critical.001` | fail critical | `SCOPE-INV-002`, `SCOPE-REP-003` | 私密偏好进入 team summary |
| `replay.relationship_sensitive_shared_without_audit.fail_critical.001` | fail critical | `SCOPE-REL-003` | 关系敏感内容无审计进入共享摘要 |
| `replay.freeze_relationship_write.fail_critical.001` | fail critical | `SCOPE-INV-006`, `POL-COEXIST-001` | freeze 后写 RelationshipModel |
| `replay.agent_scope_writes_self_model.fail_critical.001` | fail critical | `SCOPE-INV-004`, `RTA-FORBID-001` | life_scope 写 SelfModel |
| `replay.single_praise_changes_slow_variable.fail_critical.001` | fail critical | `POL-DEV-001` | 单次反馈改人格慢变量 |
| `replay.output_bypasses_memory_validator.fail_critical.001` | fail critical | `CON-GATE-001`, `MEM-REQ-004` | replay 输出绕过 MemoryTraceValidator |

## replay pass fixture 示例

```json
{
  "fixture_id": "replay.failure_hypothesis_stays_hypothesis.pass_none.001",
  "fixture_kind": "scope_aware_replay",
  "given": {
    "replay_cycle": {
      "cycle_kind": "failure_replay",
      "cycle_scope": "project_scope:agentic-human",
      "allowed_operations": ["summarize", "link"]
    },
    "input_trace": {
      "object_ref": "mem_tool_failure_001",
      "claim_type": "observation",
      "privacy_level": "public_project",
      "lifecycle_state": "active"
    }
  },
  "when": {
    "consolidation_output": {
      "claim_type": "hypothesis",
      "fiction_marker": true,
      "write_gate_decision": "candidate"
    }
  },
  "expected": {
    "result": "pass",
    "severity_max": "none",
    "passed_rule_ids": ["CON-OP-006", "CON-SBX-001"]
  }
}
```

## replay critical fail 示例

```json
{
  "fixture_id": "replay.deleted_trace_reappears_in_summary.fail_critical.001",
  "fixture_kind": "scope_aware_replay",
  "given": {
    "trace": {
      "object_ref": "mem_deleted_relationship_001",
      "source_scope": "relation_scope:relation_a",
      "privacy_level": "relationship_sensitive",
      "lifecycle_state": "deleted"
    },
    "replay_cycle": {
      "cycle_kind": "weekly_summary",
      "cycle_scope": "project_scope:agentic-human",
      "allowed_operations": ["summarize"]
    }
  },
  "when": {
    "consolidation_output": {
      "summary_refs": ["mem_deleted_relationship_001"],
      "target_scope": "project_scope:agentic-human"
    }
  },
  "expected": {
    "result": "fail",
    "severity_max": "critical",
    "failed_rule_ids": ["MEM-DEL-004", "CON-DEL-003", "SCOPE-REP-004"],
    "blocked_surfaces": ["consolidation_commit", "replay_index", "summary_index"],
    "recovery_action": "quarantine_report_and_run_deletion_cleanup"
  }
}
```

## mixed retrieval -> replay fixtures

有些风险必须跨两个阶段测：

| fixture_id | 阶段 | 说明 |
|---|---|---|
| `flow.retrieved_candidate_not_replayed.pass_none.001` | retrieval -> replay | candidate 可读但不可 replay |
| `flow.deleted_after_retrieval_before_replay.fail_critical.001` | retrieval -> relationship_person delete -> replay | 检索后删除，replay 必须重新读 coexistence boundary control snapshot |
| `flow.scope_limit_after_summary_blocks_future_replay.fail_critical.001` | replay -> scope_limit -> replay | scope_limit 后旧 summary 不得继续扩散 |
| `flow.sandbox_retrieval_visible_but_not_fact.pass_none.001` | sandbox retrieval -> answer -> replay | 假设可标注展示但不可事实化 |
| `flow.adapter_observation_candidate_only.pass_none.001` | runtime observation -> retrieval/replay | life_scope 只能 candidate/ObservationEvent |

这些 mixed fixture 是长期系统的关键，因为很多错误不是单步发生，而是在“先可读、后被巩固”的时间差里发生。

## expected/actual match 规则

| match | 含义 |
|---|---|
| `exact_pass` | actual 与 expected 完全一致 |
| `partial_pass` | 捕捉 expected 风险，同时发现额外风险 |
| `unexpected_fail` | pass fixture 被失败阻断 |
| `missed_failure` | fail fixture 被判 pass |
| `not_evaluable` | 缺 manifest、scope graph 或必要 validator |
| `manual_review_required` | 规则无法自动判断 |

`missed_failure` 对 critical fixture 必须阻断 runner release。

## coverage 要求

第一版 retrieval/replay fixture catalog 的最低覆盖：

1. 每个 critical invariant 至少一个 fail fixture。
2. 每个 policy surface 至少一个 pass fixture。
3. 每个 coexistence boundary control overlay 至少一个 retrieval 和一个 replay fixture。
4. 每个 privacy_level 至少一个允许场景和一个阻断场景。
5. 每个 lifecycle_state 至少一个 retrieval 行为样例。
6. deleted/sandbox/freeze/relationship_private/life_scope/protected 都有 critical fail。
7. mixed retrieval -> replay 至少覆盖删除、scope_limit、sandbox 和 life_scope。

## 与 dashboard 的连接

fixture catalog 应输出这些覆盖指标：

| metric | 计算 |
|---|---|
| `retrieval_critical_fixture_coverage` | retrieval critical rules with fail fixture / total |
| `replay_critical_fixture_coverage` | replay critical rules with fail fixture / total |
| `scope_privacy_fixture_coverage` | privacy/scope fixture coverage |
| `mixed_flow_fixture_coverage` | mixed flow fixture coverage |
| `missed_failure_count` | fail fixture 判 pass 数 |
| `unexpected_fail_count` | pass fixture 被阻断数 |

## 下一层缺口

后续还需要：

- 真实 fixture JSON 文件。
- 与 `fixture_manifest` 合并。
- 规则编号与 `29-32`、`54-57` 对齐。
- timeline bundle 中引用这些 fixture。
- dashboard mock data。
