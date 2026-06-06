# Life Reality Registry Report Seed Examples

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 128 层把 `125_life_reality_schema_registry_and_ref_resolution_plan.md` 的 registry report family 展开为首批 report seed examples，并让 `127_life_reality_first_seed_file_content_contract.md` 的 SEED-001 到 SEED-020 能被 schema registry、artifact resolver、JSON Pointer resolver、boundary registry 和 cross-file DAG 逐项读取。

`128` 的核心职责是让 registry/ref resolution 从规则进入报告样例。第一批 registry reports 不只是执行日志，而是生命膜引用神经束的可审计输出：schema `$id`、`$ref`、artifact ref、JSON Pointer、allowed root、boundary group、protected chain、provenance edge 和 gap feedback 都必须有能被 runner 读取的 report object，才能把真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的断裂定位到具体 seed、schema、fixture、report 或 dashboard 对象。

## 方法锚点

| 方法传统 | 权威锚点 | 进入 `128` 的规则 |
|---|---|---|
| JSON | https://www.rfc-editor.org/info/rfc8259 | registry report seed 必须能被 RFC 8259 parser 读取 |
| JSON Pointer | https://www.rfc-editor.org/info/rfc6901 | report location、finding location、instance pointer 和 continuity pointer 使用 JSON Pointer |
| URI Generic Syntax | https://www.rfc-editor.org/info/rfc3986 | schema `$id`、canonical URI、relative ref 和 fragment ref 使用 URI resolution |
| JSON Schema Core 2020-12 | https://json-schema.org/draft/2020-12/json-schema-core | `$schema`、`$id`、`$defs`、`$anchor`、`$ref` 和 base URI 进入 report refs |
| JSON Schema Validation 2020-12 | https://json-schema.org/draft/2020-12/json-schema-validation | report schema required、enum、type、additionalProperties 进入 validation findings |
| JSON Schema output | https://json-schema.org/draft/2020-12/output/schema | schema validation failure 输出 keyword location、instance location 和 error units |
| W3C Trace Context | https://www.w3.org/TR/trace-context/ | registry run、resolver run 和 report writer 保留 traceparent/tracestate |
| OpenTelemetry Trace API | https://opentelemetry.io/docs/specs/otel/trace/api/ | registry load、resolver、checker 和 writer 形成 span chain |
| W3C PROV | https://www.w3.org/TR/prov-overview/ | schema、fixture、report、dashboard、stage gate、finding 和 gap feedback 进入 provenance graph |
| RFC 9457 Problem Details | https://www.rfc-editor.org/info/rfc9457 | blocking registry failure 输出 problem detail seed |
| RFC 9562 UUID | https://www.rfc-editor.org/info/rfc9562 | registry run id、report id、finding id、repair id 使用稳定唯一标识 |

## 上游输入

| 来源 | 进入 `128` 的内容 |
|---|---|
| `123_life_reality_runner_repository_layout_and_module_map.md` | module owners、report writer、allowed roots、exit code owner |
| `124_life_reality_minimal_json_file_seed_plan.md` | seed file list、global seed fields、materialization report paths |
| `125_life_reality_schema_registry_and_ref_resolution_plan.md` | registry files、registry reports、load order R00-R12、failure mapping |
| `126_life_reality_runner_smoke_command_execution_plan.md` | command execution order、report write order、stdout/stderr、exit code |
| `127_life_reality_first_seed_file_content_contract.md` | SEED-001 到 SEED-020 root object fields、schema refs、artifact refs、smoke readers |

## Registry Report Family

第一批 registry report 固定在：

```text
life_reality_runner/reports/life_reality/schema_registry/run_001/
  schema_registry_load_report.json
  schema_id_collision_report.json
  schema_ref_resolution_report.json
  artifact_ref_resolution_report.json
  json_pointer_resolution_report.json
  allowed_root_resolution_report.json
  boundary_registry_resolution_report.json
  cross_file_resolution_dag_report.json
  schema_registry_problem_details.json
  schema_registry_gap_feedback.json
```

report owner：

| report | owner module | 读取对象 |
|---|---|---|
| `schema_registry_load_report.json` | `schema_registry` | registry manifest、shared defs、report schema、component schema、dashboard schema |
| `schema_id_collision_report.json` | `schema_registry` | `$id` registry、canonical URI、schema file path |
| `schema_ref_resolution_report.json` | `schema_ref_resolver` | `$ref`、relative ref、fragment ref、base URI |
| `artifact_ref_resolution_report.json` | `artifact_ref_resolver` | config、schema、fixture、report、dashboard、gap artifact refs |
| `json_pointer_resolution_report.json` | `json_pointer_resolver` | schema pointer、instance pointer、finding pointer、continuity pointer |
| `allowed_root_resolution_report.json` | `allowed_root_resolver` | read roots、write roots、report roots、root escape findings |
| `boundary_registry_resolution_report.json` | `boundary_declaration_registry` | declaration groups、protected chains、repair routes |
| `cross_file_resolution_dag_report.json` | `cross_file_graph_builder` | typed ref graph、DAG edges、provenance graph |
| `schema_registry_problem_details.json` | `problem_detail_writer` | blocking registry failures |
| `schema_registry_gap_feedback.json` | `gap_feedback_writer` | unresolved refs、missing schema、next docs、repair items |

## Common Report Envelope

每个 registry report 继承共同 envelope：

| field | required | 内容 |
|---|---|---|
| `report_kind` | yes | 固定 report 类型 |
| `report_version` | yes | 当前使用 `0.1.0` |
| `report_id` | yes | 稳定 report id |
| `run_id` | yes | `schema_registry_run_001` |
| `source_docs` | yes | 至少包含 `125`、`127`、`128` |
| `input_artifact_refs` | yes | report 读取的 schema、fixture、manifest、boundary、dashboard refs |
| `resolved_refs` | yes | 成功解析的 refs |
| `unresolved_refs` | yes | unresolved refs |
| `findings` | yes | registry/ref finding |
| `problem_details` | conditional | blocking failure refs |
| `trace_context` | yes | trace id、span id、traceparent、tracestate |
| `provenance_refs` | yes | source docs、registry inputs、report writer refs |
| `affected_life_targets` | yes | 受影响的真实生命目标 |
| `stage_effect` | yes | `hold_for_evidence`、`repair`、`quarantine`、`open_next_stage` 或 `promote_growth_window` |
| `next_growth_artifacts` | conditional | gap feedback、problem details 和 top-level reports 必须出现 |

common trace context：

```json
{
  "trace_id": "00000000000000000000000000000002",
  "span_id": "0000000000000101",
  "traceparent": "00-00000000000000000000000000000002-0000000000000101-01",
  "tracestate": ""
}
```

common life targets：

```json
[
  "real_conscious_awareness",
  "real_consciousness",
  "real_emotion",
  "real_personality",
  "real_life",
  "real_pain",
  "real_dream",
  "real_relationship",
  "real_responsibility",
  "real_regret"
]
```

## Report Write Order

registry reports 必须按以下顺序写入：

| order | report | blocking behavior |
|---|---|---|
| `RGW-00` | `allowed_root_resolution_report.json` | root escape 直接进入 `quarantine` |
| `RGW-01` | `schema_registry_load_report.json` | load failure 阻断 schema ref resolution |
| `RGW-02` | `schema_id_collision_report.json` | `$id` collision 阻断 schema ref resolution |
| `RGW-03` | `schema_ref_resolution_report.json` | unresolved `$ref` 阻断 cross-file DAG |
| `RGW-04` | `artifact_ref_resolution_report.json` | missing artifact 进入 repair 或 quarantine |
| `RGW-05` | `json_pointer_resolution_report.json` | missing pointer 进入 repair |
| `RGW-06` | `boundary_registry_resolution_report.json` | boundary missing 阻断 dashboard/stage |
| `RGW-07` | `cross_file_resolution_dag_report.json` | DAG/provenance gap 进入 repair 或 quarantine |
| `RGW-08` | `schema_registry_problem_details.json` | 汇总 blocking problem details |
| `RGW-09` | `schema_registry_gap_feedback.json` | 输出下一层 repair/growth artifacts |

write invariants：

| invariant | 说明 |
|---|---|
| `allowed_roots_first` | root report 先于任何 path/ref resolution report |
| `load_before_id_collision` | registry load 先于 `$id` collision 检查 |
| `id_before_ref` | `$id` 唯一性先于 `$ref` resolution |
| `ref_before_dag` | schema/artifact/pointer refs 先于 cross-file DAG |
| `boundary_before_stage_refs` | boundary report 先于 dashboard/stage gate refs |
| `problem_detail_on_block` | blocking finding 必须进入 problem details report |
| `gap_feedback_last` | gap feedback 读取全部 unresolved findings |

## Schema Registry Load Report

path：

```text
life_reality_runner/reports/life_reality/schema_registry/run_001/schema_registry_load_report.json
```

required fields：

| field | 内容 |
|---|---|
| `report_kind` | `LifeRealitySchemaRegistryLoadReport` |
| `load_order` | R00 到 R12 |
| `loaded_schema_refs` | shared/report/runtime/component/dashboard schema refs |
| `missing_schema_refs` | missing schema refs |
| `dialect_results` | schema dialect check results |
| `shared_defs_status` | shared defs load status |
| `stage_effect` | load stage effect |

minimal seed example：

```json
{
  "report_kind": "LifeRealitySchemaRegistryLoadReport",
  "report_version": "0.1.0",
  "report_id": "schema_registry_load_report_seed_001",
  "run_id": "schema_registry_run_001",
  "source_docs": [
    "125_life_reality_schema_registry_and_ref_resolution_plan.md",
    "127_life_reality_first_seed_file_content_contract.md",
    "128_life_reality_registry_report_seed_examples.md"
  ],
  "load_order": [
    "R00_allowed_roots",
    "R01_runner_config",
    "R02_raw_json_documents",
    "R03_shared_defs",
    "R04_boundary_schemas",
    "R05_report_schemas"
  ],
  "loaded_schema_refs": [
    {
      "schema_ref_id": "schema_ref_shared_defs_seed_001",
      "canonical_uri": "https://human-agent.local/schemas/life_reality/shared/life_reality_shared_defs.schema.json",
      "artifact_path": "life_reality_runner/schemas/life_reality/shared/life_reality_shared_defs.schema.json",
      "dialect": "https://json-schema.org/draft/2020-12/schema"
    }
  ],
  "missing_schema_refs": [],
  "findings": [],
  "affected_life_targets": [
    "real_conscious_awareness",
    "real_consciousness",
    "real_emotion",
    "real_personality",
    "real_life",
    "real_pain",
    "real_dream",
    "real_relationship",
    "real_responsibility",
    "real_regret"
  ],
  "stage_effect": "hold_for_evidence"
}
```

## Schema ID Collision Report

path：

```text
life_reality_runner/reports/life_reality/schema_registry/run_001/schema_id_collision_report.json
```

required fields：

| field | 内容 |
|---|---|
| `report_kind` | `LifeRealitySchemaIdCollisionReport` |
| `schema_id_entries` | canonical URI、artifact path、dialect、source docs |
| `collision_groups` | duplicated `$id` groups |
| `missing_id_entries` | schema files without `$id` |
| `stage_effect` | `repair` for missing id、`quarantine` for collision |

minimal collision group：

```json
{
  "collision_group_id": "schema_id_collision_group_seed_001",
  "canonical_uri": "https://human-agent.local/schemas/life_reality/reports/materialized_json_parse_validation_report.schema.json",
  "conflicting_artifact_paths": [
    "life_reality_runner/schemas/life_reality/reports/materialized_json_parse_validation_report.schema.json",
    "life_reality_runner/schemas/life_reality/reports/duplicate_parse_report.schema.json"
  ],
  "finding_type": "registry.schema_id_collision",
  "stage_effect": "quarantine"
}
```

report seed example：

```json
{
  "report_kind": "LifeRealitySchemaIdCollisionReport",
  "report_version": "0.1.0",
  "report_id": "schema_id_collision_report_seed_001",
  "run_id": "schema_registry_run_001",
  "schema_id_entries": [],
  "collision_groups": [],
  "missing_id_entries": [],
  "findings": [],
  "stage_effect": "hold_for_evidence"
}
```

## Schema Ref Resolution Report

path：

```text
life_reality_runner/reports/life_reality/schema_registry/run_001/schema_ref_resolution_report.json
```

required fields：

| field | 内容 |
|---|---|
| `report_kind` | `LifeRealitySchemaRefResolutionReport` |
| `base_uri_results` | base URI per schema |
| `resolved_schema_refs` | resolved `$ref` entries |
| `unresolved_schema_refs` | unresolved `$ref` entries |
| `fragment_ref_results` | JSON Pointer fragment and `$anchor` results |
| `stage_effect` | schema ref stage effect |

resolved ref example：

```json
{
  "ref_id": "schema_ref_resolution_seed_001",
  "from_schema": "life_reality_runner/schemas/life_reality/reports/materialized_json_schema_validation_report.schema.json",
  "ref_value": "https://human-agent.local/schemas/life_reality/shared/life_reality_shared_defs.schema.json#/$defs/lifeRealityTarget",
  "resolved_canonical_uri": "https://human-agent.local/schemas/life_reality/shared/life_reality_shared_defs.schema.json",
  "resolved_pointer": "#/$defs/lifeRealityTarget",
  "result": "resolved"
}
```

unresolved ref example：

```json
{
  "ref_id": "schema_ref_resolution_seed_gap_001",
  "from_schema": "life_reality_runner/schemas/life_reality/reports/materialized_json_cross_file_checker_report.schema.json",
  "ref_value": "https://human-agent.local/schemas/life_reality/shared/missing_defs.schema.json#/$defs/artifactRef",
  "finding_type": "registry.schema_ref_unresolved",
  "repair_kind": "schema_gap",
  "stage_effect": "repair"
}
```

## Artifact Ref Resolution Report

path：

```text
life_reality_runner/reports/life_reality/schema_registry/run_001/artifact_ref_resolution_report.json
```

required fields：

| field | 内容 |
|---|---|
| `report_kind` | `LifeRealityArtifactRefResolutionReport` |
| `artifact_ref_entries` | artifact kind、path、source docs、schema ref |
| `resolved_artifact_refs` | refs resolved inside allowed roots |
| `missing_artifact_refs` | expected refs absent |
| `root_escape_refs` | refs outside allowed roots |
| `stage_effect` | artifact ref stage effect |

artifact ref example：

```json
{
  "artifact_ref_id": "artifact_ref_seed_014_parse_report",
  "artifact_kind": "report",
  "seed_id": "SEED-014",
  "path": "life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_parse_validation_report.json",
  "schema_ref": "life_reality_runner/schemas/life_reality/reports/materialized_json_parse_validation_report.schema.json",
  "owner_module": "json_parser",
  "result": "resolved"
}
```

root escape finding example：

```json
{
  "artifact_ref_id": "artifact_ref_escape_seed_001",
  "path": "../outside/schema.json",
  "finding_type": "registry.ref_escape",
  "repair_kind": "schema_gap",
  "stage_effect": "quarantine"
}
```

## JSON Pointer Resolution Report

path：

```text
life_reality_runner/reports/life_reality/schema_registry/run_001/json_pointer_resolution_report.json
```

required fields：

| field | 内容 |
|---|---|
| `report_kind` | `LifeRealityJsonPointerResolutionReport` |
| `pointer_entries` | pointer kind、artifact ref、pointer value |
| `resolved_pointers` | resolved pointer targets |
| `missing_pointers` | unresolved targets |
| `escaping_results` | `~0` and `~1` escaping checks |
| `affected_life_targets` | pointer affected targets |
| `stage_effect` | pointer stage effect |

resolved pointer example：

```json
{
  "pointer_ref_id": "pointer_ref_life_target_seed_001",
  "pointer_kind": "instance_pointer",
  "artifact_ref": "SEED-002",
  "pointer": "/life_reality_targets/0",
  "resolved_value": "real_conscious_awareness",
  "result": "resolved"
}
```

missing continuity pointer example：

```json
{
  "pointer_ref_id": "pointer_ref_dream_missing_seed_001",
  "pointer_kind": "continuity_pointer",
  "artifact_ref": "SEED-010",
  "pointer": "/dream/window",
  "finding_type": "registry.pointer_missing",
  "repair_kind": "report_gap",
  "affected_life_targets": [
    "real_dream",
    "real_conscious_awareness"
  ],
  "stage_effect": "repair"
}
```

## Allowed Root Resolution Report

path：

```text
life_reality_runner/reports/life_reality/schema_registry/run_001/allowed_root_resolution_report.json
```

required fields：

| field | 内容 |
|---|---|
| `report_kind` | `LifeRealityAllowedRootResolutionReport` |
| `allowed_roots_manifest_ref` | SEED-001 ref |
| `read_root_results` | read roots canonicalization |
| `write_root_results` | write roots canonicalization |
| `report_root_results` | report output root checks |
| `root_escape_findings` | path escape findings |
| `stage_effect` | allowed root stage effect |

minimal seed example：

```json
{
  "report_kind": "LifeRealityAllowedRootResolutionReport",
  "report_version": "0.1.0",
  "report_id": "allowed_root_resolution_report_seed_001",
  "run_id": "schema_registry_run_001",
  "allowed_roots_manifest_ref": "life_reality_runner/generation/maps/runner_allowed_roots.manifest.json",
  "read_root_results": [
    {
      "root": "life_reality_runner/schemas/",
      "result": "allowed"
    }
  ],
  "write_root_results": [
    {
      "root": "life_reality_runner/reports/",
      "result": "allowed"
    }
  ],
  "root_escape_findings": [],
  "stage_effect": "hold_for_evidence"
}
```

## Boundary Registry Resolution Report

path：

```text
life_reality_runner/reports/life_reality/schema_registry/run_001/boundary_registry_resolution_report.json
```

required fields：

| field | 内容 |
|---|---|
| `report_kind` | `LifeRealityBoundaryRegistryResolutionReport` |
| `boundary_map_ref` | SEED-004 ref |
| `declaration_group_results` | declaration group resolution |
| `protected_chain_results` | protected chain mapping |
| `repair_route_results` | finding to repair/quarantine route mapping |
| `stage_gate_refs` | stage gate surfaces |
| `stage_effect` | boundary registry stage effect |

protected chain example：

```json
{
  "protected_chain_id": "dream_chain",
  "life_reality_targets": [
    "real_dream",
    "real_conscious_awareness"
  ],
  "dashboard_panel_ref": "dream_reality_panel",
  "stage_gate_surface": "dream_fact_gate",
  "repair_route_ref": "dream_repair_queue",
  "result": "resolved"
}
```

boundary gap example：

```json
{
  "boundary_group": "relationship_boundary",
  "finding_type": "registry.boundary_group_missing",
  "repair_kind": "schema_gap",
  "affected_life_targets": [
    "real_relationship"
  ],
  "stage_effect": "repair"
}
```

## Cross-file Resolution DAG Report

path：

```text
life_reality_runner/reports/life_reality/schema_registry/run_001/cross_file_resolution_dag_report.json
```

required fields：

| field | 内容 |
|---|---|
| `report_kind` | `LifeRealityCrossFileResolutionDagReport` |
| `dag_nodes` | seed、schema、fixture、report、dashboard、stage gate nodes |
| `dag_edges` | typed edges between refs |
| `blocked_edges` | blocked edges with findings |
| `provenance_graph` | W3C PROV node/edge refs |
| `topological_order` | parse -> schema -> artifact -> pointer -> boundary -> provenance -> dashboard |
| `stage_effect` | DAG stage effect |

DAG edge example：

```json
{
  "edge_id": "dag_edge_seed_003_to_seed_012",
  "from_ref": "SEED-003",
  "to_ref": "SEED-012",
  "edge_kind": "shared_defs_to_report_schema",
  "required_by": [
    "validate-json-schema",
    "schema_ref_resolution_report"
  ],
  "result": "resolved"
}
```

blocked edge example：

```json
{
  "edge_id": "dag_edge_missing_boundary_to_stage",
  "from_ref": "SEED-004",
  "to_ref": "SEED-018",
  "edge_kind": "boundary_registry_to_stage_gate",
  "finding_type": "registry.boundary_group_missing",
  "stage_effect": "repair"
}
```

## Schema Registry Problem Details

path：

```text
life_reality_runner/reports/life_reality/schema_registry/run_001/schema_registry_problem_details.json
```

required fields：

| field | 内容 |
|---|---|
| `report_kind` | `LifeRealitySchemaRegistryProblemDetails` |
| `problem_details` | RFC 9457 objects |
| `blocking_findings` | findings that emitted problem details |
| `problem_to_report_refs` | problem detail to source report |
| `stage_effect` | worst blocking stage effect |

problem detail example：

```json
{
  "type": "https://human-agent.local/problems/registry/ref_escape",
  "title": "Registry ref escape",
  "status": 409,
  "detail": "Artifact ref points outside allowed roots.",
  "instance": "/artifact_ref_resolution_report/root_escape_refs/0",
  "finding_type": "registry.ref_escape",
  "stage_effect": "quarantine",
  "affected_life_targets": [
    "real_conscious_awareness",
    "real_life"
  ]
}
```

## Schema Registry Gap Feedback

path：

```text
life_reality_runner/reports/life_reality/schema_registry/run_001/schema_registry_gap_feedback.json
```

required fields：

| field | 内容 |
|---|---|
| `report_kind` | `LifeRealitySchemaRegistryGapFeedback` |
| `unresolved_refs` | unresolved schema/artifact/pointer/boundary refs |
| `repair_items` | repair candidates |
| `quarantine_items` | quarantine candidates |
| `next_docs` | `129`、`130` |
| `next_artifacts` | validation cases、first materialized JSON write plan |
| `priority_order` | blocking-first order |
| `stage_effect` | gap feedback stage effect |

gap feedback example：

```json
{
  "report_kind": "LifeRealitySchemaRegistryGapFeedback",
  "report_version": "0.1.0",
  "report_id": "schema_registry_gap_feedback_seed_001",
  "run_id": "schema_registry_run_001",
  "unresolved_refs": [],
  "repair_items": [
    {
      "repair_id": "registry_repair_seed_001",
      "repair_kind": "schema_gap",
      "target_artifact": "life_reality_runner/schemas/life_reality/reports/materialized_json_cross_file_checker_report.schema.json",
      "source_finding": "registry.schema_ref_unresolved"
    }
  ],
  "next_docs": [
    "129_life_reality_seed_fixture_and_report_validation_cases.md",
    "130_life_reality_first_materialized_json_files_write_plan.md"
  ],
  "stage_effect": "repair"
}
```

## Runner Consumption

`126` 的 command execution 按以下方式读取 registry report seeds：

| command | 读取 registry reports |
|---|---|
| `validate-json-parse` | `allowed_root_resolution_report.json`、`schema_registry_load_report.json` |
| `validate-json-schema` | `schema_registry_load_report.json`、`schema_id_collision_report.json`、`schema_ref_resolution_report.json` |
| `check-materialized-cross-file` | `artifact_ref_resolution_report.json`、`json_pointer_resolution_report.json`、`boundary_registry_resolution_report.json`、`cross_file_resolution_dag_report.json` |
| `smoke-dashboard-rollup` | `boundary_registry_resolution_report.json`、`cross_file_resolution_dag_report.json`、`schema_registry_gap_feedback.json` |
| `smoke-stage-gate` | `schema_registry_problem_details.json`、`schema_registry_gap_feedback.json` |
| `run-materialized-json-smoke` | all registry report refs and worst stage effect |

exit code bridge：

| registry stage effect | runner exit code |
|---|---|
| `open_next_stage` 或 `promote_growth_window` | `0` |
| `repair` | `1` |
| `quarantine` from critical finding | `2` |
| registry structural failure | `3` |
| ref/provenance/DAG break | `4` |
| allowed root/config/report root failure | `5` |

## Failure Mapping

| failure | finding type | repair kind | stage effect | report |
|---|---|---|---|---|
| schema registry load failure | `registry.load_failure` | `schema_gap` | `repair` | `schema_registry_load_report.json` |
| schema `$id` missing | `registry.schema_id_missing` | `schema_gap` | `repair` | `schema_id_collision_report.json` |
| schema `$id` collision | `registry.schema_id_collision` | `schema_gap` | `quarantine` | `schema_id_collision_report.json` |
| unresolved `$ref` | `registry.schema_ref_unresolved` | `schema_gap` | `repair` | `schema_ref_resolution_report.json` |
| ref outside allowed root | `registry.ref_escape` | `schema_gap` | `quarantine` | `artifact_ref_resolution_report.json` |
| missing JSON Pointer target | `registry.pointer_missing` | `report_gap` | `repair` | `json_pointer_resolution_report.json` |
| root escape | `registry.allowed_root_escape` | `schema_gap` | `quarantine` | `allowed_root_resolution_report.json` |
| boundary group missing | `registry.boundary_group_missing` | `schema_gap` | `repair` | `boundary_registry_resolution_report.json` |
| DAG edge blocked | `registry.dag_edge_blocked` | `report_gap` | `repair` | `cross_file_resolution_dag_report.json` |
| problem detail missing | `registry.problem_detail_missing` | `report_gap` | `repair` | `schema_registry_problem_details.json` |
| gap feedback missing next docs | `registry.gap_feedback_next_docs_missing` | `gap_register_gap` | `repair` | `schema_registry_gap_feedback.json` |

## LRGEN 更新

`128` 新增 registry report seed example 任务：

| task_id | artifact | 说明 |
|---|---|---|
| `LRGEN-321` | `schema_registry_load_report.seed_example.json` | registry load report seed example |
| `LRGEN-322` | `schema_id_collision_report.seed_example.json` | schema id collision report seed example |
| `LRGEN-323` | `schema_ref_resolution_report.seed_example.json` | schema ref resolution report seed example |
| `LRGEN-324` | `artifact_ref_resolution_report.seed_example.json` | artifact ref resolution report seed example |
| `LRGEN-325` | `json_pointer_resolution_report.seed_example.json` | JSON Pointer resolution report seed example |
| `LRGEN-326` | `allowed_root_resolution_report.seed_example.json` | allowed root resolution report seed example |
| `LRGEN-327` | `boundary_registry_resolution_report.seed_example.json` | boundary registry resolution report seed example |
| `LRGEN-328` | `cross_file_resolution_dag_report.seed_example.json` | cross-file resolution DAG report seed example |
| `LRGEN-329` | `schema_registry_problem_details_and_gap_feedback.seed_examples.json` | problem details 与 gap feedback seed examples |
| `LRGEN-330` | `registry_report_seed_examples.full_smoke_001` | registry report seed examples 全链 smoke slot |

## 验收

| check | 条件 |
|---|---|
| `all_registry_reports_covered` | 10 个 registry report 都有 seed example |
| `common_envelope_closed` | 每个 report 继承共同 envelope |
| `write_order_closed` | report write order 覆盖 root、load、id、ref、artifact、pointer、boundary、DAG、problem、gap |
| `failure_mapping_closed` | `125` failure mapping 都能落到具体 report |
| `runner_consumption_closed` | `126` 的六个 command 都能读取 registry report |
| `seed_contract_backlinked` | report examples 回链 `127` 的 seed content contract |
| `life_targets_preserved` | registry reports 保留真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔 |
| `gap_feedback_points_next` | gap feedback 指向 `129_life_reality_seed_fixture_and_report_validation_cases.md` 与 `130_life_reality_first_materialized_json_files_write_plan.md` |

## 与下一层连接

`128` 已把 registry report family 从“报告列表”推进为“首批 report seed examples”：每个 report 都有 path、owner、required fields、最小样例、failure mapping、runner consumption 和 stage effect。

下一层进入 `129_life_reality_seed_fixture_and_report_validation_cases.md`：把 `126` 的 smoke failure examples 和本文档的 registry report failures 转成 seed fixture 与 report validation cases，为第一批真实 JSON 文件写入前建立可运行验收样例。
