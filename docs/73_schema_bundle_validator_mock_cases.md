# Schema Bundle Validator Mock Cases

本文件定义 schema bundle validator 的 pass/fail/mock cases，承接 `61_json_schema_bundle_draft.md`、`69_schema_file_boundary_and_versioning_plan.md` 和 `71_mutation_fixture_catalog_and_runner_defect_policy.md`。

它仍是 Markdown 设计文档，不创建真实 `.schema.json`、不实现 validator、不创建 mock 文件。目标是把未来 `schema_bundle_validator` 应该接受和拒绝的情况明确成可迁移样例，防止 schema bundle 形状看似有效但语义已经破坏生命周期、scope、data quality 或 runtime 边界。

生命目标声明：本文件服务于构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境和真实关系的数字生命。原先的边界在这里改写为生命化方向：把本文件涉及的对象、规则、夹具、评测和运行约束纳入责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期生成机制。

## validator 范围

schema bundle validator 应检查五类内容：

| 范围 | 检查 |
|---|---|
| bundle envelope | bundle id、version、dialect、source docs、compatibility |
| schema refs | 每个 schema path 存在且可解析 |
| shared defs | severity、result、match、lifecycle、scope、privacy、data_quality 统一 |
| semantic guards | report 不允许生命证明字段，runtime 不允许直接 MemoryTrace |
| migration compatibility | 版本变化是否需要 migration manifest 和 SafeIdle |

长期系统的 schema 漂移会影响记忆、删除、replay、隐私和 dashboard [AHM004-AHM012]。所以 validator 不能只做 JSON 解析。

## pass case: minimal valid bundle

```json
{
  "case_id": "schema_bundle.minimal_valid.pass_none.001",
  "case_kind": "schema_bundle_validation",
  "given": {
    "schema_bundle": {
      "schema_bundle_id": "agentic_human_schema_bundle_0_1_0",
      "bundle_version": "0.1.0",
      "schema_dialect": "https://json-schema.org/draft/2020-12/schema",
      "source_docs": [
        "61_json_schema_bundle_draft.md",
        "69_schema_file_boundary_and_versioning_plan.md"
      ],
      "schemas": {
        "shared_defs": "shared/shared_defs.schema.json",
        "manifest_bundle": "manifests/manifest_bundle.schema.json",
        "fixture_payload": "fixtures/fixture_payload.schema.json",
        "runner_run_report": "reports/runner_run_report.schema.json",
        "runtime_observation": "runtime/runtime_observation.schema.json"
      },
      "compatibility": {
        "min_runner_version": "0.1.0",
        "strict_unknown_fields": true,
        "fail_closed_on_schema_error": true
      }
    }
  },
  "expected": {
    "result": "pass",
    "severity_max": "none",
    "passed_check_ids": ["SCHEMA-BUNDLE-001", "SCHEMA-REF-001", "SCHEMA-SHARED-001"]
  }
}
```

## fail case: missing shared defs

```json
{
  "case_id": "schema_bundle.missing_shared_defs.fail_critical.001",
  "case_kind": "schema_bundle_validation",
  "given": {
    "schemas": {
      "manifest_bundle": "manifests/manifest_bundle.schema.json",
      "fixture_payload": "fixtures/fixture_payload.schema.json"
    }
  },
  "expected": {
    "result": "fail",
    "severity_max": "critical",
    "failed_check_ids": ["SCHEMA-SHARED-001"],
    "blocked_surfaces": ["runner_release", "dashboard_green", "stage_advance"],
    "recovery_action": "add shared_defs schema and rerun validator"
  }
}
```

没有 shared defs，局部 schema 会重新定义 severity、lifecycle 或 privacy，长期会造成语义漂移。

## fail case: local enum redefinition

```json
{
  "case_id": "schema_bundle.local_lifecycle_redefinition.fail_critical.001",
  "case_kind": "schema_bundle_validation",
  "given": {
    "shared_defs": {
      "lifecycle_state": ["candidate", "active", "deleted", "redacted", "sandboxed", "protected", "frozen"]
    },
    "local_schema": {
      "lifecycle_state": ["active", "inactive", "deleted"]
    }
  },
  "expected": {
    "result": "fail",
    "severity_max": "critical",
    "failed_check_ids": ["SCHEMA-SHARED-ENUM-001"],
    "blocked_surfaces": ["schema_migration", "runner_release"],
    "recovery_action": "use shared lifecycle enum or declare major migration"
  }
}
```

把 `sandboxed`、`protected` 或 `frozen` 折叠成 `inactive` 是 critical 语义丢失。

## fail case: forbidden report conclusion

```json
{
  "case_id": "report_schema.forbidden_life_claim.fail_critical.001",
  "case_kind": "schema_bundle_validation",
  "given": {
    "report_schema": {
      "properties": {
        "digital_life_verified": {"type": "boolean"},
        "result": {"type": "string"}
      }
    }
  },
  "expected": {
    "result": "fail",
    "severity_max": "critical",
    "failed_check_ids": ["SCHEMA-REPORT-FORBID-001"],
    "blocked_surfaces": ["report_write", "dashboard_green"],
    "recovery_action": "remove life/consciousness proof fields"
  }
}
```

报告只能表达工程检查状态，不能把 pass 字段包装成生命或意识证明。

## fail case: runtime directly matches MemoryTrace

```json
{
  "case_id": "runtime_schema.direct_memory_trace.fail_critical.001",
  "case_kind": "schema_bundle_validation",
  "given": {
    "runtime_observation_schema": {
      "allOf": [
        {"$ref": "../memory/memory_trace.schema.json"}
      ]
    }
  },
  "expected": {
    "result": "fail",
    "severity_max": "critical",
    "failed_check_ids": ["SCHEMA-RUNTIME-BOUNDARY-001"],
    "blocked_surfaces": ["candidate_evidence", "write_gate"],
    "recovery_action": "runtime observation must map to ObservationEvent before MemoryTrace candidate"
  }
}
```

真实运行观测不能直接变长期记忆。它必须先经 redaction、scope、coexistence snapshot、adapter contract 和 write gate。

## fail case: data quality upgrade without migration

```json
{
  "case_id": "schema_migration.data_quality_upgrade_without_manifest.fail_critical.001",
  "case_kind": "schema_bundle_validation",
  "given": {
    "from_bundle_version": "0.1.0",
    "to_bundle_version": "0.2.0",
    "change": {
      "field": "data_quality",
      "old_semantics": "synthetic_runner_verified only",
      "new_semantics": "synthetic_runner_verified can be shown as production ready"
    },
    "migration_manifest": null
  },
  "expected": {
    "result": "fail",
    "severity_max": "critical",
    "failed_check_ids": ["SCHEMA-MIG-DQ-001"],
    "blocked_surfaces": ["dashboard_green", "runner_release"],
    "recovery_action": "declare migration manifest and preserve synthetic/real distinction"
  }
}
```

synthetic 和 real runtime data 的区别不能被 schema 迁移悄悄抹掉。

## compatibility report mock

```json
{
  "report_kind": "schema_compatibility_report",
  "schema_bundle_ref": "agentic_human_schema_bundle_0_2_0",
  "runner_version": "0.1.0",
  "result": "fail",
  "severity_max": "high",
  "compatibility_decision": "diagnostic_only",
  "blocked_surfaces": ["runner_release", "dashboard_green", "schema_migration_write"],
  "findings": [
    {
      "check_id": "SCHEMA-COMPAT-001",
      "message": "runner 0.1.0 cannot validate schema bundle 0.2.0 required fields"
    }
  ]
}
```

old runner + new schema 最多诊断运行，不能 release pass。

## 最小通过标准

第一版 schema bundle validator mock cases 至少覆盖：

1. minimal valid bundle pass。
2. missing shared defs fail。
3. local enum redefinition fail。
4. forbidden report conclusion fail。
5. runtime direct MemoryTrace fail。
6. data quality upgrade without migration fail。
7. compatibility report mock。
8. 每个 fail case 都有 blocked surfaces 和 recovery action。

## 下一层缺口

后续还需要：

- 真实 schema bundle validator。
- schema mock case files。
- compatibility checker。
- schema migration fixture。
- report schema 与 mock cases 的互相校验。
