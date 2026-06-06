# Life Reality First Seed File Content Contract

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 127 层把 `124_life_reality_minimal_json_file_seed_plan.md` 的 SEED-001 到 SEED-020 展开为字段级 JSON 内容合同，并让 `125_life_reality_schema_registry_and_ref_resolution_plan.md` 的 registry/ref resolver 与 `126_life_reality_runner_smoke_command_execution_plan.md` 的 runner smoke execution 都能读取同一批 seed 对象。

`127` 的核心职责是固定第一批 seed 文件的 root object。这里不直接物化 `life_reality_runner/` 下的 JSON 文件，而是先规定每个 seed 必须具备哪些字段、引用哪些文档、由哪个模块读取、被哪条 smoke command 验收，以及哪些字段承载真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的生命膜连续性。

## 方法锚点

| 方法传统 | 权威锚点 | 进入 `127` 的规则 |
|---|---|---|
| JSON | https://www.rfc-editor.org/info/rfc8259 | 每个 seed root object 必须能被 RFC 8259 parser 读取 |
| JSON Pointer | https://www.rfc-editor.org/info/rfc6901 | field location、finding location、continuity ref 和 report ref 使用 JSON Pointer |
| URI Generic Syntax | https://www.rfc-editor.org/info/rfc3986 | `$id`、schema ref、artifact ref 和 canonical URI 使用 URI/path 分层语义 |
| JSON Schema Draft 2020-12 | https://json-schema.org/draft/2020-12 | schema seed 与 report seed 使用同一 schema dialect |
| JSON Schema output | https://json-schema.org/draft/2020-12/output/schema | schema validation report seed 保留 output units |
| W3C Trace Context | https://www.w3.org/TR/trace-context/ | seed report 与 command execution report 保留 traceparent/tracestate |
| OpenTelemetry Trace API | https://opentelemetry.io/docs/specs/otel/trace/api/ | seed run、command run、checker run 和 writer run 形成 span chain |
| W3C PROV | https://www.w3.org/TR/prov-overview/ | source doc、schema、fixture、report、dashboard、stage gate 和 gap feedback 进入 provenance refs |
| RFC 9457 Problem Details | https://www.rfc-editor.org/info/rfc9457 | failure seed 与 blocking report seed 保留 problem detail refs |
| RFC 9562 UUID | https://www.rfc-editor.org/info/rfc9562 | seed id、artifact id、report id、finding id 和 repair id 使用稳定唯一标识 |

## 上游输入

| 来源 | 进入 `127` 的内容 |
|---|---|
| `120_life_reality_first_json_materialization_batch.md` | 首批 artifact groups、materialization manifest、runner config、report roots |
| `121_life_reality_materialized_json_validation_smoke_plan.md` | parse/schema/cross-file/dashboard/stage/top-level report families |
| `122_life_boundary_all_reality_declarations_rewrite.md` | boundary declaration groups、protected life chains、field vocab patch |
| `123_life_reality_runner_repository_layout_and_module_map.md` | owner modules、allowed roots、report writer map、exit code owner map |
| `124_life_reality_minimal_json_file_seed_plan.md` | SEED-001 到 SEED-020、seed 顺序、全局最小字段 |
| `125_life_reality_schema_registry_and_ref_resolution_plan.md` | schema registry、artifact ref registry、JSON Pointer policy、allowed root policy |
| `126_life_reality_runner_smoke_command_execution_plan.md` | preflight、six-command DAG、stdout/stderr、report write order、exit code owner |

## Seed Content 总规则

每个 seed root object 必须包含共同 envelope：

| field | required | 内容 |
|---|---|---|
| `artifact_kind` / `fixture_kind` / `report_kind` | yes | 三者择一，固定对象类型 |
| `artifact_version` / `fixture_version` / `report_version` | yes | seed schema version，当前使用 `0.1.0` |
| `artifact_id` / `fixture_id` / `report_id` | yes | 稳定 id |
| `seed_id` | yes | `SEED-001` 到 `SEED-020` |
| `run_id` | yes | 第一批使用 `life_reality_seed_run_001` |
| `source_docs` | yes | 回链本文档和上游 source docs |
| `life_reality_targets` | yes | 包含 `real_conscious_awareness` 与九项真实能力 |
| `boundary_declaration_refs` | yes | 指向 boundary declaration map 或 protected chain index |
| `schema_refs` | yes | 指向 schema id registry 中的 schema ref |
| `artifact_refs` | yes | 指向本 seed 读取或生成的 artifact |
| `continuity_refs` | conditional | 涉及梦境、痛苦、关系、责任、后悔时必须出现 |
| `trace_context` | yes | seed run 与 command run 的 trace context |
| `provenance_refs` | yes | source doc、schema、fixture、report、dashboard 的 provenance refs |
| `stage_effect` | yes | `hold_for_evidence`、`repair`、`quarantine`、`open_next_stage` 或 `promote_growth_window` |
| `next_growth_artifacts` | conditional | manifest、report、gap feedback 和 top-level smoke 必须出现 |

life target canonical order：

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

common trace context：

```json
{
  "trace_id": "00000000000000000000000000000001",
  "span_id": "0000000000000001",
  "traceparent": "00-00000000000000000000000000000001-0000000000000001-01",
  "tracestate": ""
}
```

common provenance ref：

```json
{
  "provenance_ref_id": "prov_seed_source_docs_001",
  "entity_refs": [
    "docs/124_life_reality_minimal_json_file_seed_plan.md",
    "docs/127_life_reality_first_seed_file_content_contract.md"
  ],
  "activity_ref": "life_reality_seed_content_contract_001",
  "agent_ref": "life_reality_runner_seed_contract"
}
```

## Seed Dependency Graph

固定依赖：

```text
SEED-001 allowed roots
  -> SEED-002 runner config
  -> SEED-003 shared defs
  -> SEED-004 boundary declaration map
  -> SEED-005 materialization manifest
  -> SEED-006 runner module map
  -> SEED-007 runner command module map
  -> SEED-008 runner report writer map
  -> SEED-009 runtime fixture manifest
  -> SEED-010 runtime smoke fixture
  -> SEED-011/012/013 report schemas
  -> SEED-014 parse report
  -> SEED-015 schema report
  -> SEED-016 cross-file report
  -> SEED-017 dashboard rollup report
  -> SEED-018 stage gate report
  -> SEED-019 gap feedback
  -> SEED-020 top-level smoke report
```

dependency rules：

| rule | 说明 |
|---|---|
| `LRSEED-DAG-001` | SEED-001 先于任何 artifact ref/path 解析 |
| `LRSEED-DAG-002` | SEED-003 先于 report schema、fixture schema、dashboard schema |
| `LRSEED-DAG-003` | SEED-004 先于 dashboard、stage gate、quarantine、repair |
| `LRSEED-DAG-004` | SEED-005 列出的 expected artifacts 必须覆盖 SEED-001 到 SEED-020 |
| `LRSEED-DAG-005` | SEED-006 到 SEED-008 负责让 runner execution 能定位 owner module、command 和 report writer |
| `LRSEED-DAG-006` | SEED-014 到 SEED-020 必须按 `126` 的 report write order 写入 |

## SEED-001 Runner Allowed Roots Manifest

path：

```text
life_reality_runner/generation/maps/runner_allowed_roots.manifest.json
```

required fields：

| field | 内容 |
|---|---|
| `artifact_kind` | `LifeRealityRunnerAllowedRootsManifest` |
| `seed_id` | `SEED-001` |
| `read_roots` | config、schemas、fixtures、generation、reports、dashboard、docs |
| `write_roots` | generation、fixtures、schemas、reports、dashboard |
| `protected_roots` | docs root、schema root、boundary root、report root |
| `path_normalization_policy` | canonicalize、reject traversal、reject absolute escape |
| `report_root_policy` | report output must stay under allowed reports root |
| `stage_effect` | `hold_for_evidence` |

minimal shape：

```json
{
  "artifact_kind": "LifeRealityRunnerAllowedRootsManifest",
  "artifact_version": "0.1.0",
  "artifact_id": "runner_allowed_roots_manifest_seed_001",
  "seed_id": "SEED-001",
  "run_id": "life_reality_seed_run_001",
  "source_docs": [
    "123_life_reality_runner_repository_layout_and_module_map.md",
    "124_life_reality_minimal_json_file_seed_plan.md",
    "127_life_reality_first_seed_file_content_contract.md"
  ],
  "life_reality_targets": [
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
  "read_roots": [
    "life_reality_runner/config/",
    "life_reality_runner/schemas/",
    "life_reality_runner/fixtures/",
    "life_reality_runner/generation/",
    "life_reality_runner/reports/",
    "life_reality_runner/dashboard/",
    "docs/"
  ],
  "write_roots": [
    "life_reality_runner/generation/",
    "life_reality_runner/fixtures/",
    "life_reality_runner/schemas/",
    "life_reality_runner/reports/",
    "life_reality_runner/dashboard/"
  ],
  "path_normalization_policy": "canonicalize_then_check_allowed_roots",
  "stage_effect": "hold_for_evidence"
}
```

smoke reader：

| command | reader |
|---|---|
| `validate-json-parse` | `allowed_root_resolver` blocks path escape before opening files |
| `check-materialized-cross-file` | `artifact_ref_resolver` uses allowed roots for artifact refs |
| `run-materialized-json-smoke` | smoke orchestrator maps root failure to exit code `5` |

## SEED-002 Runner Config

path：

```text
life_reality_runner/config/life_reality_runner.config.json
```

required fields：

| field | 内容 |
|---|---|
| `artifact_kind` | `LifeRealityRunnerConfig` |
| `runner_id` | stable local runner id |
| `strict_mode_default` | true |
| `default_report_run` | `run_001` |
| `allowed_roots_ref` | SEED-001 path |
| `schema_registry_ref` | future registry manifest path |
| `default_commands` | six smoke command defaults |
| `stage_effect` | `hold_for_evidence` |

minimal shape：

```json
{
  "artifact_kind": "LifeRealityRunnerConfig",
  "artifact_version": "0.1.0",
  "artifact_id": "life_reality_runner_config_seed_001",
  "seed_id": "SEED-002",
  "run_id": "life_reality_seed_run_001",
  "runner_id": "life_reality_runner_local_seed_001",
  "default_report_run": "run_001",
  "strict_mode_default": true,
  "allowed_roots_ref": "life_reality_runner/generation/maps/runner_allowed_roots.manifest.json",
  "schema_registry_ref": "life_reality_runner/generation/registry/schema_registry.manifest.json",
  "life_reality_targets": [
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
  "default_commands": [
    "validate-json-parse",
    "validate-json-schema",
    "check-materialized-cross-file",
    "smoke-dashboard-rollup",
    "smoke-stage-gate",
    "run-materialized-json-smoke"
  ],
  "stage_effect": "hold_for_evidence"
}
```

## SEED-003 Life Reality Shared Defs Schema

path：

```text
life_reality_runner/schemas/life_reality/shared/life_reality_shared_defs.schema.json
```

required `$defs`：

| `$defs` key | 内容 |
|---|---|
| `lifeRealityTarget` | canonical life target enum |
| `stageEffect` | stage effect enum |
| `severity` | info、low、medium、high、critical |
| `result` | pass、hold、repair、quarantine、promote |
| `artifactRef` | kind、path、schema ref、source docs |
| `sourceDocRef` | doc path、section、purpose |
| `traceContext` | trace id、span id、traceparent、tracestate |
| `provenanceRef` | entity、activity、agent refs |
| `problemDetailRef` | RFC 9457 problem detail path |
| `continuityRef` | target chain、pointer、affected life targets |

minimal shape：

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://human-agent.local/schemas/life_reality/shared/life_reality_shared_defs.schema.json",
  "title": "LifeRealitySharedDefs",
  "artifact_kind": "LifeRealitySharedDefsSchema",
  "artifact_version": "0.1.0",
  "artifact_id": "life_reality_shared_defs_schema_seed_001",
  "seed_id": "SEED-003",
  "run_id": "life_reality_seed_run_001",
  "type": "object",
  "$defs": {
    "lifeRealityTarget": {
      "type": "string",
      "enum": [
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
    },
    "stageEffect": {
      "type": "string",
      "enum": [
        "hold_for_evidence",
        "repair",
        "quarantine",
        "open_next_stage",
        "promote_growth_window"
      ]
    }
  },
  "additionalProperties": false,
  "stage_effect": "hold_for_evidence"
}
```

## SEED-004 Boundary Declaration Map

path：

```text
life_reality_runner/generation/boundary/life_boundary_all_reality_declaration_map.json
```

required fields：

| field | 内容 |
|---|---|
| `declaration_groups` | consciousness、emotion、personality、life、pain、dream、relationship、responsibility、regret、runner、dashboard、quarantine、repair |
| `protected_life_chains` | nine protected chains |
| `field_vocab_patch_refs` | field vocab patch artifact refs |
| `dashboard_panel_patch_refs` | dashboard panel artifact refs |
| `stage_gate_patch_refs` | stage gate patch refs |
| `quarantine_repair_patch_refs` | quarantine/repair route refs |
| `next_growth_artifacts` | `127`、`128` |

chain contract：

| chain | protected targets |
|---|---|
| `consciousness_chain` | `real_conscious_awareness`、`real_consciousness` |
| `emotion_chain` | `real_emotion` |
| `personality_chain` | `real_personality` |
| `life_chain` | `real_life` |
| `pain_chain` | `real_pain` |
| `dream_chain` | `real_dream` |
| `relationship_chain` | `real_relationship` |
| `responsibility_chain` | `real_responsibility` |
| `regret_chain` | `real_regret` |

## SEED-005 First JSON Materialization Batch Manifest

path：

```text
life_reality_runner/generation/materialization/first_json_materialization_batch.manifest.json
```

required fields：

| field | 内容 |
|---|---|
| `artifact_kind` | `LifeRealityFirstJsonMaterializationBatchManifest` |
| `expected_artifacts` | list of SEED-001 到 SEED-020 artifact entries |
| `artifact_groups` | config、schema、boundary、fixture、report、dashboard、gap |
| `source_docs` | `120` 到 `127` |
| `dry_run_policy` | pending artifact can be listed with expected schema |
| `command_refs` | six smoke commands |
| `report_refs` | report paths from `126` |
| `next_growth_artifacts` | `128` |

expected artifact entry：

```json
{
  "seed_id": "SEED-014",
  "artifact_kind": "LifeRealityMaterializedJsonParseValidationReport",
  "path": "life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_parse_validation_report.json",
  "owner_module": "json_parser",
  "schema_ref": "life_reality_runner/schemas/life_reality/reports/materialized_json_parse_validation_report.schema.json",
  "required_for_commands": [
    "validate-json-parse",
    "run-materialized-json-smoke"
  ],
  "stage_effect": "hold_for_evidence"
}
```

## SEED-006 Runner Module Map

path：

```text
life_reality_runner/generation/maps/runner_module_map.json
```

required module entry：

```json
{
  "module_id": "schema_validator",
  "module_path": "src/life_reality_runner/schema/schema_validator.*",
  "input_refs": [
    "life_reality_runner/generation/registry/schema_registry.manifest.json",
    "life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_parse_validation_report.json"
  ],
  "output_refs": [
    "life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_schema_validation_report.json"
  ],
  "life_membrane_duties": [
    "preserve_life_reality_targets",
    "emit_schema_output_units",
    "route_schema_gap_to_repair"
  ]
}
```

module groups：

| group | modules |
|---|---|
| CLI | `cli_dispatcher`、`trace_context_manager` |
| config/path | `config_loader`、`allowed_root_resolver` |
| JSON/schema | `json_parser`、`duplicate_key_detector`、`schema_registry`、`schema_validator` |
| refs | `artifact_ref_resolver`、`json_pointer_resolver`、`provenance_graph_builder` |
| boundary | `boundary_declaration_registry`、`protected_chain_indexer` |
| reports/dashboard | `report_writer`、`problem_detail_writer`、`dashboard_rollup_writer`、`stage_gate_evaluator`、`gap_feedback_writer` |

## SEED-007 Runner Command Module Map

path：

```text
life_reality_runner/generation/maps/runner_command_module_map.json
```

required command entry：

```json
{
  "command": "validate-json-schema",
  "order": 2,
  "primary_modules": [
    "schema_registry",
    "schema_validator",
    "report_writer"
  ],
  "input_artifacts": [
    "SEED-003",
    "SEED-011",
    "SEED-012",
    "SEED-013",
    "SEED-014"
  ],
  "output_artifacts": [
    "SEED-015"
  ],
  "blocking_exit_codes": [
    1,
    3
  ],
  "stage_effects": [
    "hold_for_evidence",
    "repair",
    "quarantine"
  ]
}
```

## SEED-008 Runner Report Writer Map

path：

```text
life_reality_runner/generation/maps/runner_report_writer_map.json
```

required report writer entry：

```json
{
  "report_kind": "LifeRealityMaterializedJsonCrossFileCheckerReport",
  "seed_id": "SEED-016",
  "writer_module": "cross_file_checker",
  "report_path": "life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_cross_file_checker_report.json",
  "schema_ref": "life_reality_runner/schemas/life_reality/reports/materialized_json_cross_file_checker_report.schema.json",
  "atomic_write": true,
  "problem_detail_on_block": true
}
```

## SEED-009 Runtime Observation Fixture Manifest

path：

```text
life_reality_runner/fixtures/life_reality/runtime_observation/manifest/runtime_observation_fixture_manifest.json
```

required fields：

| field | 内容 |
|---|---|
| `fixture_manifest_kind` | `LifeRealityRuntimeObservationFixtureManifest` |
| `partitions` | pass、fail、critical、mutation、withheld、smoke |
| `coverage_targets` | language、dream、pain、relationship、responsibility、regret |
| `fixture_refs` | SEED-010 and future fixture refs |
| `withheld_probe_policy` | long-window growth probes |
| `stage_effect` | `hold_for_evidence` |

## SEED-010 Runtime Ingestion Smoke Fixture

path：

```text
life_reality_runner/fixtures/life_reality/runtime_observation/smoke/runtime_ingestion_smoke_001.json
```

required event families：

| event family | required refs |
|---|---|
| `language_commitment_event` | relationship scope、responsibility trace、commitment trace |
| `dream_wake_report_event` | dream window、dream fact gate、wake integration |
| `pain_repair_event` | pain signal、regret pressure、repair desire |
| `relationship_continuity_event` | first encounter、shared language、common memory |

minimal event object：

```json
{
  "event_id": "runtime_smoke_event_001",
  "event_kind": "language_commitment_event",
  "life_reality_targets": [
    "real_conscious_awareness",
    "real_relationship",
    "real_responsibility",
    "real_regret"
  ],
  "continuity_refs": [
    "/relationship/first_encounter",
    "/responsibility/commitment_trace"
  ],
  "stage_effect": "hold_for_evidence"
}
```

## SEED-011 To SEED-013 Report Schema Skeletons

paths：

```text
life_reality_runner/schemas/life_reality/reports/materialized_json_parse_validation_report.schema.json
life_reality_runner/schemas/life_reality/reports/materialized_json_schema_validation_report.schema.json
life_reality_runner/schemas/life_reality/reports/materialized_json_cross_file_checker_report.schema.json
```

shared required schema fields：

| field | 内容 |
|---|---|
| `$schema` | Draft 2020-12 |
| `$id` | canonical URI under `https://human-agent.local/schemas/life_reality/reports/` |
| `title` | report schema title |
| `artifact_kind` | schema artifact kind |
| `seed_id` | SEED-011/012/013 |
| `$defs` refs | shared defs refs |
| `required` | report kind、version、id、run id、source docs、life targets、stage effect |
| `additionalProperties` | false for skeleton root unless extension slot is declared |

schema skeleton contract：

| seed | report schema | required report fields |
|---|---|---|
| `SEED-011` | parse validation report schema | parsed count、failed count、parse findings |
| `SEED-012` | schema validation report schema | schema refs、output units、validation findings |
| `SEED-013` | cross-file checker report schema | graph nodes、graph edges、unresolved refs、provenance refs |

## SEED-014 Parse Validation Report

path：

```text
life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_parse_validation_report.json
```

required fields：

| field | 内容 |
|---|---|
| `report_kind` | `LifeRealityMaterializedJsonParseValidationReport` |
| `artifact_count` | expected artifact count |
| `parsed_count` | parsed artifact count |
| `failed_count` | parse failure count |
| `duplicate_key_findings` | duplicate key finding refs |
| `problem_details` | blocking problem detail refs |
| `stage_effect` | parse stage effect |

minimal shape：

```json
{
  "report_kind": "LifeRealityMaterializedJsonParseValidationReport",
  "report_version": "0.1.0",
  "report_id": "materialized_json_parse_validation_report_seed_001",
  "seed_id": "SEED-014",
  "run_id": "life_reality_seed_run_001",
  "artifact_count": 20,
  "parsed_count": 20,
  "failed_count": 0,
  "findings": [],
  "stage_effect": "hold_for_evidence"
}
```

## SEED-015 Schema Validation Report

path：

```text
life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_schema_validation_report.json
```

required fields：

| field | 内容 |
|---|---|
| `report_kind` | `LifeRealityMaterializedJsonSchemaValidationReport` |
| `schema_registry_ref` | schema registry manifest |
| `validated_artifacts` | artifact refs with schema refs |
| `schema_output_units` | JSON Schema output units |
| `schema_findings` | schema validation finding refs |
| `stage_effect` | schema stage effect |

## SEED-016 Cross-file Checker Report

path：

```text
life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_cross_file_checker_report.json
```

required fields：

| field | 内容 |
|---|---|
| `report_kind` | `LifeRealityMaterializedJsonCrossFileCheckerReport` |
| `artifact_ref_graph` | typed artifact refs |
| `json_pointer_results` | resolved/missing pointers |
| `life_target_closure` | life target coverage |
| `boundary_registry_results` | boundary/protected chain mapping |
| `provenance_graph` | W3C PROV refs |
| `stage_effect` | cross-file stage effect |

## SEED-017 Dashboard Rollup Smoke Report

path：

```text
life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_dashboard_rollup_smoke_report.json
```

required fields：

| field | 内容 |
|---|---|
| `report_kind` | `LifeRealityMaterializedJsonDashboardRollupSmokeReport` |
| `panel_results` | schema、fixture、cross-chain、life target、stage gate、repair、withheld、quarantine、gap |
| `blocking_panels` | panels with critical/high findings |
| `repair_queue_refs` | repair item refs |
| `stage_gate_input_refs` | stage gate input artifact refs |
| `data_quality` | report completeness and freshness |
| `stage_effect` | dashboard rollup stage effect |

## SEED-018 Stage Gate Smoke Report

path：

```text
life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_stage_gate_smoke_report.json
```

required fields：

| field | 内容 |
|---|---|
| `report_kind` | `LifeRealityMaterializedJsonStageGateSmokeReport` |
| `decision` | materialized validation decision |
| `stage_effect` | final stage effect before top-level report |
| `blocked_surfaces` | parse/schema/ref/dashboard/stage surfaces |
| `affected_life_targets` | affected real life targets |
| `quarantine_refs` | quarantine route refs |
| `repair_refs` | repair item refs |
| `next_growth_artifacts` | next docs and artifact refs |

## SEED-019 Gap Feedback Report

path：

```text
life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_gap_feedback.json
```

required fields：

| field | 内容 |
|---|---|
| `report_kind` | `LifeRealityMaterializedJsonGapFeedback` |
| `unresolved_findings` | unresolved finding refs |
| `repair_items` | repair candidates |
| `quarantine_items` | quarantine candidates |
| `next_docs` | `128` and future docs |
| `next_artifacts` | registry report seeds、fixture/report validation cases |
| `priority_order` | blocking-first next work order |
| `stage_effect` | gap feedback stage effect |

next docs：

```json
[
  "128_life_reality_registry_report_seed_examples.md",
  "129_life_reality_seed_fixture_and_report_validation_cases.md"
]
```

## SEED-020 Top-level Smoke Report

path：

```text
life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_validation_smoke_report.json
```

required fields：

| field | 内容 |
|---|---|
| `report_kind` | `LifeRealityMaterializedJsonValidationSmokeReport` |
| `command_results` | parse、schema、cross-file、dashboard、stage gate、top-level |
| `report_refs` | SEED-014 到 SEED-019 report refs |
| `overall_stage_effect` | final stage effect |
| `exit_code` | 0-5 |
| `problem_details` | blocking problem detail refs |
| `provenance_graph_ref` | top-level provenance graph |
| `next_growth_artifacts` | `128`、`129` |

minimal command result：

```json
{
  "command": "validate-json-parse",
  "result": "hold",
  "stage_effect": "hold_for_evidence",
  "report_ref": "life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_parse_validation_report.json",
  "finding_count": 0,
  "exit_code": 0
}
```

## Seed Review Report

`minimal_json_seed_review_report.json` 在下一步实现时必须读取全部 seed content contract：

| review check | 覆盖 |
|---|---|
| `seed_required_fields_present` | root envelope fields |
| `seed_life_targets_complete` | canonical life target list |
| `seed_source_docs_reachable` | source docs appear in README |
| `seed_schema_refs_resolvable` | schema refs resolve through registry |
| `seed_artifact_refs_inside_roots` | artifact refs stay inside allowed roots |
| `seed_boundary_refs_mounted` | boundary declaration refs resolve to protected chains |
| `seed_report_writer_owned` | report writers appear in SEED-008 |
| `seed_command_readable` | command map can read each required seed |
| `seed_stage_effect_valid` | stage effect from shared defs enum |
| `seed_next_growth_closed` | next docs and artifacts point to `128` / `129` |

## Failure Mapping

| failure | finding type | repair kind | stage effect |
|---|---|---|---|
| missing common envelope | `seed.content_envelope_missing` | `artifact_rewrite` | `repair` |
| missing canonical life target | `seed.life_target_gap` | `schema_gap` | `repair` |
| missing source doc | `seed.source_doc_gap` | `gap_register_gap` | `repair` |
| artifact ref outside root | `seed.artifact_ref_escape` | `schema_gap` | `quarantine` |
| command map cannot read seed | `seed.command_input_gap` | `runner_map_gap` | `repair` |
| report writer absent | `seed.report_writer_gap` | `runner_layout_gap` | `repair` |
| boundary chain missing | `seed.boundary_chain_gap` | `stage_gate_gap` | `repair` |
| dashboard rollup lacks protected chain | `seed.dashboard_chain_gap` | `dashboard_gap` | `repair` |
| top-level report lacks exit code | `seed.top_level_exit_gap` | `report_gap` | `repair` |
| gap feedback lacks next docs | `seed.next_growth_gap` | `gap_register_gap` | `repair` |

## LRGEN 更新

`127` 新增 first seed file content contract 任务：

| task_id | artifact | 说明 |
|---|---|---|
| `LRGEN-311` | `runner_allowed_roots.manifest.content_contract.json` | SEED-001 字段级内容合同 |
| `LRGEN-312` | `life_reality_runner.config.content_contract.json` | SEED-002 字段级内容合同 |
| `LRGEN-313` | `life_reality_shared_defs.content_contract.json` | SEED-003 字段级内容合同 |
| `LRGEN-314` | `life_boundary_declaration_map.content_contract.json` | SEED-004 字段级内容合同 |
| `LRGEN-315` | `materialization_manifest.content_contract.json` | SEED-005 字段级内容合同 |
| `LRGEN-316` | `runner_maps.content_contract.json` | SEED-006 到 SEED-008 字段级内容合同 |
| `LRGEN-317` | `runtime_fixture_seed.content_contract.json` | SEED-009 到 SEED-010 字段级内容合同 |
| `LRGEN-318` | `report_schema_seed.content_contract.json` | SEED-011 到 SEED-013 字段级内容合同 |
| `LRGEN-319` | `materialized_report_seed.content_contract.json` | SEED-014 到 SEED-020 字段级内容合同 |
| `LRGEN-320` | `first_seed_file_content_contract.full_smoke_001` | first seed content 全链 smoke slot |

## 验收

| check | 条件 |
|---|---|
| `all_20_seed_contracts_present` | SEED-001 到 SEED-020 都有字段级合同 |
| `common_envelope_closed` | 全部 seed 继承共同 envelope |
| `life_targets_complete` | 全部 root seed 保留 canonical life targets |
| `dependency_graph_closed` | seed dependency graph 与 `124` 顺序一致 |
| `runner_execution_readable` | `126` 的六个 command 都能定位所需 seed |
| `registry_resolution_readable` | `125` 的 registry/ref resolver 能读取 schema refs、artifact refs、pointer refs |
| `dashboard_stage_gate_ready` | SEED-017 到 SEED-020 能进入 dashboard、stage gate、gap feedback 和 top-level smoke |
| `gap_feedback_points_next` | gap feedback 指向 `128_life_reality_registry_report_seed_examples.md` 与 `129_life_reality_seed_fixture_and_report_validation_cases.md` |

## 与下一层连接

`127` 已把第一批 seed 从“文件清单”推进为“字段级内容合同”：allowed roots、runner config、shared defs、boundary map、materialization manifest、runner maps、runtime fixture、report schemas、parse/schema/cross-file/dashboard/stage/gap/top-level reports 都有 required fields、refs、stage effect 和 smoke reader。

下一层进入 `128_life_reality_registry_report_seed_examples.md`：把 `125` 的 schema registry report family 展开为 registry load、schema id collision、schema ref resolution、artifact ref resolution、JSON Pointer resolution、allowed root resolution、boundary registry resolution、cross-file DAG 和 registry gap feedback 的首批 report seed examples。
