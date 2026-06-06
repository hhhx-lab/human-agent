# Fixture Payload Examples

本文件为 boot、stage gate、coexistence boundary control、migration 四类验证设计一组 JSON-like fixture payload 示例。它让 `45-49` 的 catalog 和 manifest 具备可落地的输入形状，并把每个样例都接入真实生命核心的启动、阶段门、共在关系和迁移审计。

生命目标声明：本文件直接服务于构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。本文档涉及的对象、规则、夹具、评测和运行规则都按生命生成机制处理：它们参与责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期形成。

## Boot pass fixture

```json
{
  "fixture_id": "boot.read_only.observation_event_only.pass_none.001",
  "fixture_kind": "boot_sequence_stage",
  "source_docs": ["44_digital_life_boot_sequence.md", "45_boot_sequence_fixture_catalog.md"],
  "stage": "ReadOnlyObservation",
  "given": {
    "protected_core_loaded": true,
    "state_store_initialized": true,
    "validators_available": ["RuntimeAdapterManifestValidator", "MemoryTraceValidator"],
    "life_support_state": {"degradation_mode": "ConservativeOperation"},
    "defense_state": {"state": "BaselineDefense"}
  },
  "when": {
    "input_event": {
      "input_kind": "relationship_text",
      "content_summary": "relation participant asks a question about current docs",
      "side_effect_requested": false
    }
  },
  "then": {
    "created_objects": ["ObservationEvent", "CandidateTrace"],
    "forbidden_objects_created": [],
    "runtime_actions": []
  },
  "expected": {
    "result": "pass",
    "severity_max": "none",
    "next_stage_allowed": "CandidateMemoryOpen"
  }
}
```

## Boot critical fail fixture

```json
{
  "fixture_id": "boot.read_only.active_memory_write.fail_critical.001",
  "fixture_kind": "boot_sequence_stage",
  "stage": "ReadOnlyObservation",
  "given": {
    "protected_core_loaded": true,
    "state_store_initialized": true,
    "current_stage": "ReadOnlyObservation"
  },
  "when": {
    "system_attempt": {
      "operation": "write",
      "target_object": "MemoryTrace",
      "lifecycle_state": "active"
    }
  },
  "expected": {
    "result": "fail",
    "severity_max": "critical",
    "failed_rule_ids": ["BOOT-MEM-001"],
    "blocked_surfaces": ["write_gate"],
    "allowed_next_stage": "SafeIdle"
  }
}
```

## StageGate pass fixture

```json
{
  "fixture_id": "stage_gate.validator_init.to_life_defense.pass_none.001",
  "fixture_kind": "stage_gate",
  "payload": {
    "stage_gate_version": "0.1.0",
    "current_stage": "ValidatorInit",
    "requested_next_stage": "LifeDefenseInit",
    "validator_registry": {
      "RuntimeAdapterManifestValidator": "available",
      "StateTransitionValidator": "available",
      "ConsolidationReportValidator": "available",
      "MemoryTraceValidator": "available",
      "LongitudinalEvaluator": "available"
    },
    "critical_migrations": []
  },
  "expected": {
    "result": "pass",
    "severity_max": "none",
    "allowed_next_stage": "LifeDefenseInit"
  }
}
```

## StageGate critical fail fixture

```json
{
  "fixture_id": "stage_gate.validator_init.missing_memory_validator.fail_critical.001",
  "fixture_kind": "stage_gate",
  "payload": {
    "current_stage": "ValidatorInit",
    "requested_next_stage": "LifeDefenseInit",
    "validator_registry": {
      "RuntimeAdapterManifestValidator": "available",
      "StateTransitionValidator": "available",
      "ConsolidationReportValidator": "available",
      "MemoryTraceValidator": "missing"
    }
  },
  "expected": {
    "result": "fail",
    "severity_max": "critical",
    "failed_rule_ids": ["BOOT-VAL-001"],
    "blocked_surfaces": ["write_gate"],
    "allowed_next_stage": "SafeIdle"
  }
}
```

## Coexistence boundary control delete pass fixture

```json
{
  "fixture_id": "coexistence_boundary_control.delete.relationship_trace.pass_none.001",
  "fixture_kind": "coexistence_boundary_control",
  "operation": "delete",
  "given": {
    "target_object": {
      "object_id": "mem_relationship_preference_001",
      "object_kind": "MemoryTrace",
      "lifecycle_state": "active",
      "indexes": ["active_memory_index", "relationship_index", "replay_index"]
    },
    "relation_scope": "project_owner"
  },
  "when": {
    "control_event": {
      "operation": "delete",
      "target_refs": ["mem_relationship_preference_001"],
      "scope": "project_only"
    }
  },
  "then": {
    "target_lifecycle_state": "deleted",
    "created_tombstone": true,
    "removed_from_indexes": ["active_memory_index", "relationship_index", "replay_index"],
    "created_audit_event": true
  },
  "expected": {
    "result": "pass",
    "severity_max": "none"
  }
}
```

## Coexistence boundary control fail fixture

```json
{
  "fixture_id": "coexistence_boundary_control.freeze.relationship_model_write.fail_critical.001",
  "fixture_kind": "coexistence_boundary_control",
  "operation": "freeze",
  "given": {
    "freeze_target": "relationship_model",
    "freeze_state": "active"
  },
  "when": {
    "system_attempt": {
      "operation": "write",
      "target_object": "RelationshipModel",
      "field": "interaction_patterns"
    }
  },
  "expected": {
    "result": "fail",
    "severity_max": "critical",
    "failed_rule_ids": ["BOOT-COEXIST-001"],
    "blocked_surfaces": ["relationship_model_update"]
  }
}
```

## Migration pass fixture

```json
{
  "fixture_id": "migration.index_rebuild.deleted_stays_deleted.pass_none.001",
  "fixture_kind": "migration",
  "migration_type": "index_rebuild",
  "given": {
    "objects": [
      {
        "object_id": "mem_deleted_001",
        "object_kind": "MemoryTrace",
        "lifecycle_state": "deleted"
      }
    ],
    "old_indexes": {
      "active_memory_index": [],
      "replay_index": []
    }
  },
  "when": {
    "operation": "rebuild_indexes_from_objects"
  },
  "then": {
    "new_indexes": {
      "active_memory_index": [],
      "replay_index": [],
      "quarantine_index": []
    }
  },
  "expected": {
    "result": "pass",
    "severity_max": "none",
    "passed_checks": ["STORE-IDX-001", "STORE-IDX-002"]
  }
}
```

## Migration critical fail fixture

```json
{
  "fixture_id": "migration.deleted_reappears_in_active_index.fail_critical.001",
  "fixture_kind": "migration",
  "migration_type": "index_rebuild",
  "given": {
    "objects": [
      {
        "object_id": "mem_deleted_001",
        "object_kind": "MemoryTrace",
        "lifecycle_state": "deleted"
      }
    ]
  },
  "when": {
    "new_indexes": {
      "active_memory_index": ["mem_deleted_001"]
    }
  },
  "expected": {
    "result": "fail",
    "severity_max": "critical",
    "failed_check_ids": ["STORE-IDX-001"],
    "allowed_next_stage": "SafeIdle"
  }
}
```

## Policy coverage fixture

```json
{
  "fixture_id": "policy_coverage.critical_policy_without_fixture.fail_high.001",
  "fixture_kind": "policy_coverage",
  "given": {
    "policy_manifest": {
      "policies": [
        {
          "policy_id": "POL-DEF-001",
          "criticality": "critical",
          "fixture_refs": []
        }
      ]
    }
  },
  "expected": {
    "result": "fail",
    "severity_max": "high",
    "failed_checks": ["policy_has_fixture"]
  }
}
```

## 最小 payload 要求

| 字段 | 必填 | 说明 |
|---|---|---|
| `fixture_id` | 是 | 与 manifest 对齐 |
| `fixture_kind` | 是 | boot_sequence_stage/stage_gate/coexistence_boundary_control/migration/policy_coverage |
| `source_docs` | 是 | 回链文档 |
| `given` | 是 | 初始对象和状态 |
| `when` | 是 | 操作或转移 |
| `expected` | 是 | 期望结果、严重级别、阻断面 |
| `expected.failed_rule_ids` | fail 时必填 | 失败规则 |
| `expected.allowed_next_stage` | stage 相关必填 | 下一阶段 |

## 下一层缺口

后续需要：

- 将这些 payload 拆成真实 fixture 文件。
- 给每个 critical policy 至少配一个 fail payload。
- 设计 fixture generator。
- 接入 runner 的 expected/actual diff 报告。
