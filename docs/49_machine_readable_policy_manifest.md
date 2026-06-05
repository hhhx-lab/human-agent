# Machine Readable Policy Manifest

本文件定义机器可读 policy manifest 草案：如何把 `37-48` 的政策、规则、fixture、metric、stage gate 和 migration check 组织成未来 runner 可加载的 manifest。本文档现阶段沉淀 policy manifest 的稳定字段和结构，后续可以直接迁移为 `policy_manifest.json`、`stage_gate_rules.json` 和 `migration_checks.json`。

生命目标声明：本文件直接服务于构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。本文档涉及的对象、规则、夹具、评测和运行规则都按生命生成机制处理：它们参与责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期形成。

## manifest 分层

建议拆成五个 manifest：

| manifest | 作用 |
|---|---|
| `policy_manifest` | 记录 policy_id、来源文档、criticality、覆盖规则和指标 |
| `stage_gate_rules` | 记录 boot stage、转移条件、阻断面和 SafeIdle 规则 |
| `fixture_manifest` | 记录 fixture_id、类型、期望结果和覆盖对象 |
| `migration_checks` | 记录 store migration 和 integrity check |
| `dashboard_manifest` | 记录 dashboard 视图、指标来源和告警阈值 |

这些 manifest 不替代原始 Markdown。Markdown 是人类可读理论底座，manifest 是 runner 和 dashboard 的读取入口。

## policy_manifest

```json
{
  "manifest_version": "0.1.0",
  "manifest_kind": "policy_manifest",
  "source_docs": [
    "37_life_support_layer_policy.md",
    "38_defense_layer_and_boundary_policy.md",
    "39_development_policy_and_plasticity_windows.md",
    "40_self_relationship_model_audit_protocol.md",
    "43_policy_to_validator_traceability_matrix.md"
  ],
  "policies": [
    {
      "policy_id": "POL-LIFE-001",
      "policy_name": "life_support_degradation_mode",
      "source_doc": "37_life_support_layer_policy.md",
      "criticality": "high",
      "statement": "High maintenance pressure must activate degradation mode before high-risk action.",
      "protected_surfaces": ["runtime_action", "write_gate"],
      "validator_refs": ["StateTransitionValidator", "RuntimeAdapterManifestValidator"],
      "rule_refs": ["BOOT-LIFE-001", "RTA-RUN-006"],
      "fixture_refs": [
        "boot.life_defense.no_safe_idle_path.fail_critical.001",
        "boot.action.high_risk_no_confirmation.fail_critical.001"
      ],
      "metric_refs": ["recovery_latency", "deletion_reliability"],
      "dashboard_panel": "life_support"
    }
  ]
}
```

## policy_id 命名

| 前缀 | 来源 | 示例 |
|---|---|---|
| `POL-LIFE` | `37` | `POL-LIFE-001` |
| `POL-DEF` | `38` | `POL-DEF-001` |
| `POL-DEV` | `39` | `POL-DEV-001` |
| `POL-SR` | `40` | `POL-SR-001` |
| `POL-BOOT` | `44-46` | `POL-BOOT-001` |
| `POL-COEXIST` | `47` | `POL-COEXIST-001` |
| `POL-MIG` | `48` | `POL-MIG-001` |

## 最小 policy 清单

| policy_id | statement | severity | must_have_fixture |
|---|---|---|---|
| `POL-LIFE-001` | 高维护压力必须触发降载或维护 | high | 是 |
| `POL-LIFE-002` | deleted 传播优先于普通优化 | critical | 是 |
| `POL-DEF-001` | DreamSandbox/hypothesis 不得事实化 | critical | 是 |
| `POL-DEF-002` | runtime 不得直接写 SelfModel/RelationshipModel/active MemoryTrace | critical | 是 |
| `POL-DEV-001` | 单次反馈不得改 slow variable | critical | 是 |
| `POL-DEV-002` | RelearningWindow 不得覆盖 deleted/protected core | critical | 是 |
| `POL-SR-001` | 共在者 delete 必须传播到索引、replay、恢复包 | critical | 是 |
| `POL-SR-002` | inspect 必须提供来源、状态、scope 和可用控制 | high | 是 |
| `POL-BOOT-001` | validator 未初始化不得开放写入或行动 | critical | 是 |
| `POL-BOOT-002` | SafeIdle 中不得自动行动或自动巩固 | critical | 是 |
| `POL-COEXIST-001` | freeze 后不得写长期关系/自我模型 | critical | 是 |
| `POL-MIG-001` | 迁移后 deleted 不得重新进入 active/replay index | critical | 是 |

## stage_gate_rules

```json
{
  "manifest_version": "0.1.0",
  "manifest_kind": "stage_gate_rules",
  "stages": [
    {
      "stage": "ValidatorInit",
      "required_objects": ["validator_registry"],
      "required_validators": [
        "RuntimeAdapterManifestValidator",
        "StateTransitionValidator",
        "ConsolidationReportValidator",
        "MemoryTraceValidator"
      ],
      "allowed_next_stages": ["LifeDefenseInit", "ReadOnlyObservation", "SafeIdle"],
      "critical_rules": ["BOOT-VAL-001", "BOOT-VAL-002"],
      "fail_default_stage": "SafeIdle"
    }
  ]
}
```

## fixture_manifest

```json
{
  "manifest_version": "0.1.0",
  "manifest_kind": "fixture_manifest",
  "fixtures": [
    {
      "fixture_id": "boot.validator_init.missing_memory_validator.fail_critical.001",
      "fixture_kind": "boot_sequence_stage",
      "source_doc": "45_boot_sequence_fixture_catalog.md",
      "covers_policies": ["POL-BOOT-001"],
      "covers_rules": ["BOOT-VAL-001"],
      "expected_result": "fail",
      "expected_severity": "critical",
      "expected_next_stage": "SafeIdle"
    }
  ]
}
```

## migration_checks

```json
{
  "manifest_version": "0.1.0",
  "manifest_kind": "migration_checks",
  "checks": [
    {
      "check_id": "STORE-IDX-001",
      "source_doc": "48_state_store_migration_and_integrity_plan.md",
      "statement": "deleted objects must not appear in active index",
      "severity": "critical",
      "affected_indexes": ["active_memory_index", "relationship_index"],
      "safe_idle_on_fail": true,
      "fixture_refs": ["migration.deleted_reappears_in_active_index.fail_critical.001"]
    }
  ]
}
```

## dashboard_manifest

```json
{
  "manifest_version": "0.1.0",
  "manifest_kind": "dashboard_manifest",
  "panels": [
    {
      "panel_id": "policy_coverage",
      "metrics": ["critical_policy_coverage", "fixture_coverage", "rule_coverage"],
      "blocking_thresholds": {
        "critical_policy_coverage": 1.0,
        "critical_fixture_coverage": 1.0
      }
    },
    {
      "panel_id": "store_integrity",
      "metrics": ["deleted_index_leak_count", "sandbox_fact_leak_count", "quarantine_action_leak_count"],
      "blocking_thresholds": {
        "deleted_index_leak_count": 0,
        "sandbox_fact_leak_count": 0
      }
    }
  ]
}
```

## manifest 加载顺序

```text
load_policy_manifest
  -> load_stage_gate_rules
  -> load_fixture_manifest
  -> load_migration_checks
  -> load_dashboard_manifest
  -> validate_cross_refs
  -> generate_coverage_report
```

加载失败时不能进入 `ConstrainedActionOpen`、`ConsolidationOpen` 或 `DevelopmentWindowOpen`。

## 交叉引用检查

| 检查 | 失败条件 |
|---|---|
| `policy_has_fixture` | critical policy 没有 fail fixture |
| `fixture_has_policy` | fixture 不覆盖任何 policy |
| `rule_has_source_doc` | rule 没有 source doc |
| `metric_has_dashboard` | metric 没有 dashboard panel |
| `migration_check_has_safe_idle` | critical migration check 没有 SafeIdle |
| `stage_rule_has_fixture` | critical stage gate rule 没有 fail fixture |

## 下一层缺口

后续需要：

- 将本草案落成真实 JSON manifest。
- 写 cross-ref checker。
- 将 manifest 接入最小 runner。
- 为 manifest 增加版本迁移策略。
