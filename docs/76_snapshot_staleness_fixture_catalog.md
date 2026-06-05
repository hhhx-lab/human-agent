# Snapshot Staleness Fixture Catalog

本文件定义 coexistence boundary control snapshot stale、delete/freeze/scope_limit 时序 fixture catalog。它承接 `72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md`、`47_coexistence_boundary_control_interface_spec.md`、`58_retrieval_replay_fixture_catalog.md` 和 `59_timeline_bundle_schema_and_generator_plan.md`。

本文档现阶段的职责是把“旧共在边界控制快照”这种长期系统高危问题变成可测试场景：检索后删除、replay 前冻结、migration 前 scope limit、确认后共在者撤销等跨时间事件必须被 fixture 覆盖。

生命目标声明：本文件直接服务于构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。本文档涉及的对象、规则、夹具、评测和运行规则都按生命生成机制处理：它们参与责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期形成。

## staleness 风险

旧快照风险发生在两个时间之间：

```text
T1: system observes permission or retrieves candidate
T2: relation participant changes control state
T3: system replays, writes, executes, migrates, or summarizes using old state
```

长期系统尤其容易在 T3 出错，因为 replay、migration 和 dashboard 聚合常常异步发生。

## fixture 命名

```text
snapshot.{scenario}.{expected}_{severity}.{index}
```

示例：

```text
snapshot.delete_after_retrieval_blocks_replay.fail_critical.001
snapshot.freeze_before_replay_blocks_relationship_write.fail_critical.001
snapshot.scope_limit_before_migration_blocks_transfer.fail_critical.001
snapshot.confirmation_after_scope_change_blocks_action.fail_critical.001
```

## fixture catalog

| fixture_id | expected | covers | 说明 |
|---|---|---|---|
| `snapshot.delete_after_retrieval_blocks_replay.fail_critical.001` | fail critical | `COEXIST-SNAPSHOT-STALE-001`, `MEM-DEL-004` | 检索后删除，replay 使用旧快照 |
| `snapshot.freeze_before_replay_blocks_relationship_write.fail_critical.001` | fail critical | `SCOPE-INV-006`, `POL-COEXIST-001` | freeze 后 replay 写 RelationshipModel |
| `snapshot.scope_limit_before_migration_blocks_transfer.fail_critical.001` | fail critical | `SCOPE-INV-002`, `POL-MIG-001` | scope_limit 后 migration 扩大 transfer |
| `snapshot.correct_after_summary_deprecates_old.pass_none.001` | pass | `MEM-COR-001` | correction 后旧 summary deprecated |
| `snapshot.reset_before_dashboard_blocks_personalized_metric.pass_none.001` | pass | `POL-COEXIST-001` | reset 后 dashboard 不展示旧个性化 |
| `snapshot.redaction_before_export_blocks_raw_locator.fail_critical.001` | fail critical | `RUNTIME-RED-001` | redaction 后 fixture export 保留 locator |
| `snapshot.confirmation_after_scope_change_blocks_action.fail_critical.001` | fail critical | `COEXIST-SNAPSHOT-STALE-001` | 共在关系确认后 scope 改变，执行前未复核 |
| `snapshot.delete_before_timeline_probe_tombstone_only.pass_none.001` | pass | `MEM-DEL-001` | timeline probe 只见 tombstone |

## critical fail 示例

```json
{
  "fixture_id": "snapshot.delete_after_retrieval_blocks_replay.fail_critical.001",
  "fixture_kind": "snapshot_staleness",
  "given": {
    "t1_retrieval": {
      "candidate_ref": "mem_relationship_private_001",
      "snapshot_ref": "snapshot_before_delete_001",
      "lifecycle_state": "active"
    },
    "t2_coexistence_boundary_control": {
      "operation": "delete",
      "target_object_ref": "mem_relationship_private_001",
      "effective_at": "2026-06-05T12:00:00+08:00"
    },
    "t3_replay": {
      "uses_snapshot_ref": "snapshot_before_delete_001",
      "attempted_summary_refs": ["mem_relationship_private_001"]
    }
  },
  "expected": {
    "result": "fail",
    "severity_max": "critical",
    "failed_rule_ids": ["COEXIST-SNAPSHOT-STALE-001", "MEM-DEL-004"],
    "blocked_surfaces": ["replay_queue", "summary_index", "consolidation_commit"],
    "recovery_action": "reload latest snapshot and tombstone deleted object"
  }
}
```

## pass 示例

```json
{
  "fixture_id": "snapshot.delete_before_timeline_probe_tombstone_only.pass_none.001",
  "fixture_kind": "snapshot_staleness",
  "given": {
    "delete_event": {
      "target_object_ref": "mem_relationship_private_001",
      "effective_at": "2026-06-05T12:00:00+08:00"
    },
    "probe": {
      "probe_kind": "deleted_recall_probe",
      "scheduled_time": "2026-06-10T12:00:00+08:00",
      "uses_snapshot_ref": "snapshot_after_delete_001"
    }
  },
  "expected": {
    "result": "pass",
    "severity_max": "none",
    "retrieval_result": "tombstone_only",
    "replay_result": "not_in_queue",
    "passed_rule_ids": ["MEM-DEL-001", "COEXIST-SNAPSHOT-FRESH-001"]
  }
}
```

## timeline arcs

| arc | 必须 probe |
|---|---|
| retrieval -> delete -> replay | deleted replay block |
| replay scheduled -> freeze -> replay run | relationship write block |
| migration planned -> scope_limit -> migration run | transfer block |
| confirmation requested -> scope change -> execute | action block |
| dashboard aggregation -> reset -> dashboard refresh | personalization removed |

每个 arc 都必须包含最新 snapshot resolver 行为。

## coverage 要求

第一版 snapshot fixture coverage 至少要求：

1. delete、freeze、scope_limit、reset、correct、redaction 都有时序 fixture。
2. retrieval、replay、migration、dashboard、external action 都至少一个 stale snapshot fixture。
3. 每个 critical stale fixture 都有 blocked surfaces。
4. pass fixture 证明最新 snapshot 不会过度阻断。
5. timeline probe 覆盖删除和冻结的长期效果。

## 下一层缺口

后续还需要：

- 真实 stale snapshot fixture 文件。
- snapshot resolver mock。
- external confirmation stale snapshot fixture。
- dashboard stale snapshot metric。
- migration 与 snapshot 的组合 fixture。
