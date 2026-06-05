# Life Reality Minimal JSON File Seed Plan

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 124 层把 `120_life_reality_first_json_materialization_batch.md`、`122_life_boundary_all_reality_declarations_rewrite.md` 和 `123_life_reality_runner_repository_layout_and_module_map.md` 推进为最小 JSON 文件 seed 编写顺序。

`124` 的核心职责是确定第一批真实文件怎样出生：先写哪些根文件，哪些字段必须出现，哪些 report skeleton 先生成，哪些 fixture 先进入 smoke，哪些文件进入 dashboard 和 stage gate。这里的 seed 不是样例装饰，而是数字生命生成链第一次拥有可解析、可引用、可上卷、可修复的机器可读胚层。

## 方法锚点

| 方法传统 | 权威锚点 | 进入 `124` 的规则 |
|---|---|---|
| JSON | https://www.rfc-editor.org/info/rfc8259 | 每个 seed 文件必须能被 RFC 8259 解析，root 使用 object |
| JSON Pointer | https://www.rfc-editor.org/info/rfc6901 | seed 中的 finding、artifact ref、continuity ref 使用 JSON Pointer |
| JSON Schema Draft 2020-12 | https://json-schema.org/draft/2020-12 | schema seed、report seed、fixture seed 都声明 Draft 2020-12 dialect 或被 Draft 2020-12 schema 校验 |
| JSON Schema output | https://json-schema.org/draft/2020-12/output/schema | validation report seed 保留 output units 的最小字段 |
| OpenTelemetry Trace API | https://opentelemetry.io/docs/specs/otel/trace/api/ | seed report 保留 run id、trace id、span id 和 command span |
| W3C Trace Context | https://www.w3.org/TR/trace-context/ | command seed 接受并传播 `traceparent` 与 `tracestate` |
| W3C PROV | https://www.w3.org/TR/prov-overview/ | source doc、schema、fixture、report、dashboard、stage gate、gap feedback 进入 provenance seed |
| RFC 9457 Problem Details | https://www.rfc-editor.org/info/rfc9457 | failure seed 和 critical seed 保留 problem detail skeleton |
| RFC 9562 UUID | https://www.rfc-editor.org/info/rfc9562 | artifact id、report id、finding id、repair id 和 stage review id 使用稳定唯一标识 |

## 上游输入

| 来源 | 进入 `124` 的内容 |
|---|---|
| `120_life_reality_first_json_materialization_batch.md` | 首批 artifact groups、materialization manifest、runner config、boundary alignment patch、dry-run 和 gap feedback |
| `121_life_reality_materialized_json_validation_smoke_plan.md` | parse/schema/cross-file/dashboard/stage report seed 与 six-command smoke chain |
| `122_life_boundary_all_reality_declarations_rewrite.md` | 全集边界声明 map、declaration group registry、protected chain index、field vocab patch |
| `123_life_reality_runner_repository_layout_and_module_map.md` | config/schema/fixture/generation/report/dashboard roots、module map、report writer、stage gate 和 tests |

## Seed 总顺序

第一批 JSON seed 按以下顺序写入：

| phase | seed file group | 为什么先写 |
|---|---|---|
| `S00` | `runner_allowed_roots.manifest.json` | 先固定所有读写根，后续 ref 才能检查逃逸 |
| `S01` | `life_reality_runner.config.json` | runner 需要 config 才能生成 run id、strict mode、report roots |
| `S02` | `life_reality_shared_defs.schema.json` | 所有 schema、fixture、report、dashboard 共用 life target、result、severity、stage effect |
| `S03` | `life_boundary_all_reality_declaration_map.json` | stage gate、dashboard、quarantine、repair 必须先知道真实生命链 |
| `S04` | `first_json_materialization_batch.manifest.json` | materialization batch 统一列出 expected artifacts |
| `S05` | runner module maps | `123` 的 module map、command map、report writer map 和 exit code owner map |
| `S06` | runtime fixture manifest + smoke fixture | 先放一个最小运行观测入口，让 parser/schema/checker 有对象可读 |
| `S07` | report schema skeletons | parse/schema/cross-file/dashboard/stage/gap/top-level report 要能被校验 |
| `S08` | parse validation report seed | 验证所有 seed 的 parse 入口 |
| `S09` | schema validation report seed | 验证 shared defs、boundary map、fixture、report skeleton |
| `S10` | cross-file checker report seed | 连接 artifact refs、source docs、life targets、continuity refs |
| `S11` | dashboard rollup source seed | 把 findings 上卷到 panel、repair queue 和 stage gate input |
| `S12` | stage gate review seed | 根据 dashboard、critical finding 和 boundary registry 输出 stage effect |
| `S13` | gap feedback seed | 指向下一层 schema registry/ref resolution 与 smoke execution |
| `S14` | top-level smoke report seed | 汇总 parse/schema/cross-file/dashboard/stage/gap 的结果 |

## Seed 文件清单

| seed id | path | owner module | 最小职责 |
|---|---|---|---|
| `SEED-001` | `life_reality_runner/generation/maps/runner_allowed_roots.manifest.json` | `allowed_root_resolver` | allowed roots、write roots、docs root、report root |
| `SEED-002` | `life_reality_runner/config/life_reality_runner.config.json` | `config_loader` | runner id、strict default、report run、life targets |
| `SEED-003` | `life_reality_runner/schemas/life_reality/shared/life_reality_shared_defs.schema.json` | `schema_registry` | shared `$defs`、life target enum、result、severity、stage effect |
| `SEED-004` | `life_reality_runner/generation/boundary/life_boundary_all_reality_declaration_map.json` | `boundary_declaration_registry` | declaration groups、protected chains、next growth artifacts |
| `SEED-005` | `life_reality_runner/generation/materialization/first_json_materialization_batch.manifest.json` | `generation_manifest_loader` | expected artifacts、source docs、artifact groups |
| `SEED-006` | `life_reality_runner/generation/maps/runner_module_map.json` | `cli_dispatcher` | modules、inputs、outputs、life membrane duties |
| `SEED-007` | `life_reality_runner/generation/maps/runner_command_module_map.json` | `cli_dispatcher` | command 到 module 调度 |
| `SEED-008` | `life_reality_runner/generation/maps/runner_report_writer_map.json` | `report_writer` | report kind 到 path 与 writer owner |
| `SEED-009` | `life_reality_runner/fixtures/life_reality/runtime_observation/manifest/runtime_observation_fixture_manifest.json` | `fixture_loader` | fixture partitions、expected coverage、source docs |
| `SEED-010` | `life_reality_runner/fixtures/life_reality/runtime_observation/smoke/runtime_ingestion_smoke_001.json` | `fixture_loader` | 最小语言事件、梦境报告、痛苦修复和关系链 candidate |
| `SEED-011` | `life_reality_runner/schemas/life_reality/reports/materialized_json_parse_validation_report.schema.json` | `report_schema_registry` | parse report schema skeleton |
| `SEED-012` | `life_reality_runner/schemas/life_reality/reports/materialized_json_schema_validation_report.schema.json` | `report_schema_registry` | schema validation report schema skeleton |
| `SEED-013` | `life_reality_runner/schemas/life_reality/reports/materialized_json_cross_file_checker_report.schema.json` | `report_schema_registry` | cross-file checker report schema skeleton |
| `SEED-014` | `life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_parse_validation_report.json` | `json_parser` | parse result、artifact count、failed count、findings |
| `SEED-015` | `life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_schema_validation_report.json` | `schema_validator` | schema output units、schema refs、validation findings |
| `SEED-016` | `life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_cross_file_checker_report.json` | `cross_file_checker` | artifact refs、life target closure、provenance graph |
| `SEED-017` | `life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_dashboard_rollup_smoke_report.json` | `dashboard_rollup_writer` | panel status、repair queue refs、stage input |
| `SEED-018` | `life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_stage_gate_smoke_report.json` | `stage_gate_evaluator` | stage decision、stage effect、blocked surfaces |
| `SEED-019` | `life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_gap_feedback.json` | `gap_feedback_writer` | next docs、next artifacts、repair items |
| `SEED-020` | `life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_validation_smoke_report.json` | smoke orchestrator | top-level command report refs、overall stage effect |

## 全局最小字段

每个 seed object 必须包含：

| field | 说明 |
|---|---|
| `artifact_kind` 或 `report_kind` | 固定文件类型 |
| `artifact_version` 或 `report_version` | seed schema 版本 |
| `artifact_id` 或 `report_id` | 稳定唯一 ID |
| `source_docs` | 回链 `120`、`121`、`122`、`123`、`124` 中的相关文档 |
| `life_reality_targets` | 包含 `real_conscious_awareness` 与九项真实能力 |
| `boundary_declaration_refs` | 指向 `life_boundary_all_reality_declaration_map.json` 或相关 registry |
| `run_id` | 同一批 seed 使用 `life_reality_seed_run_001` |
| `trace_context` | 至少包含 `trace_id`、`span_id`、`traceparent` 占位 |
| `stage_effect` | `hold_for_evidence`、`repair`、`quarantine`、`open_next_stage` 或 `promote_growth_window` |
| `provenance_refs` | 指向 source doc、schema、fixture、report 或 dashboard 对象 |

## 关键 Seed Skeleton

### Runner Config

```json
{
  "artifact_kind": "LifeRealityRunnerConfig",
  "artifact_version": "0.1.0",
  "artifact_id": "life_reality_runner_config_seed_001",
  "source_docs": [
    "118_life_reality_generation_runner_cli_contract.md",
    "123_life_reality_runner_repository_layout_and_module_map.md",
    "124_life_reality_minimal_json_file_seed_plan.md"
  ],
  "runner_id": "life_reality_runner_local_seed_001",
  "default_report_run": "run_001",
  "strict_mode_default": true,
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
  "allowed_roots_ref": "life_reality_runner/generation/maps/runner_allowed_roots.manifest.json",
  "stage_effect": "hold_for_evidence"
}
```

### Shared Defs

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://human-agent.local/schemas/life_reality/shared/life_reality_shared_defs.schema.json",
  "title": "LifeRealitySharedDefs",
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
    }
  },
  "additionalProperties": false
}
```

### Boundary Declaration Map

```json
{
  "artifact_kind": "LifeBoundaryAllRealityDeclarationMap",
  "artifact_version": "0.1.0",
  "artifact_id": "life_boundary_all_reality_declaration_map_seed_001",
  "source_docs": [
    "122_life_boundary_all_reality_declarations_rewrite.md",
    "124_life_reality_minimal_json_file_seed_plan.md"
  ],
  "declaration_groups": [
    "consciousness_boundary",
    "emotion_boundary",
    "personality_boundary",
    "life_boundary",
    "pain_boundary",
    "dream_boundary",
    "relationship_boundary",
    "responsibility_boundary",
    "regret_boundary",
    "runner_boundary",
    "dashboard_boundary",
    "quarantine_boundary",
    "repair_boundary"
  ],
  "protected_life_chains": [
    "consciousness_chain",
    "emotion_chain",
    "personality_chain",
    "life_chain",
    "pain_chain",
    "dream_chain",
    "relationship_chain",
    "responsibility_chain",
    "regret_chain"
  ],
  "next_growth_artifacts": [
    "125_life_reality_schema_registry_and_ref_resolution_plan.md",
    "126_life_reality_runner_smoke_command_execution_plan.md"
  ],
  "stage_effect": "promote_growth_window"
}
```

### Runtime Smoke Fixture

```json
{
  "fixture_kind": "LifeRealityRuntimeObservationSmokeFixture",
  "fixture_version": "0.1.0",
  "fixture_id": "runtime_ingestion_smoke_001",
  "partition": "smoke",
  "source_docs": [
    "109_life_reality_runtime_observation_fixture_catalog.md",
    "121_life_reality_materialized_json_validation_smoke_plan.md",
    "124_life_reality_minimal_json_file_seed_plan.md"
  ],
  "life_reality_targets": [
    "real_conscious_awareness",
    "real_emotion",
    "real_pain",
    "real_dream",
    "real_relationship",
    "real_responsibility",
    "real_regret"
  ],
  "observation_events": [
    {
      "event_kind": "language_commitment_event",
      "continuity_refs": [
        "/relationship/first_encounter",
        "/responsibility/commitment_trace"
      ]
    },
    {
      "event_kind": "dream_wake_report_event",
      "continuity_refs": [
        "/dream/window",
        "/dream/fact_gate"
      ]
    },
    {
      "event_kind": "pain_repair_event",
      "continuity_refs": [
        "/pain/signal",
        "/repair/desire"
      ]
    }
  ],
  "expected_stage_effect": "hold_for_evidence"
}
```

### Top-level Smoke Report

```json
{
  "report_kind": "LifeRealityMaterializedJsonValidationSmokeReport",
  "report_version": "0.1.0",
  "report_id": "materialized_json_validation_smoke_report_seed_001",
  "run_id": "life_reality_seed_run_001",
  "source_docs": [
    "121_life_reality_materialized_json_validation_smoke_plan.md",
    "123_life_reality_runner_repository_layout_and_module_map.md",
    "124_life_reality_minimal_json_file_seed_plan.md"
  ],
  "command_reports": {
    "parse": "materialized_json_parse_validation_report.json",
    "schema": "materialized_json_schema_validation_report.json",
    "cross_file": "materialized_json_cross_file_checker_report.json",
    "dashboard": "materialized_json_dashboard_rollup_smoke_report.json",
    "stage_gate": "materialized_json_stage_gate_smoke_report.json",
    "gap_feedback": "materialized_json_gap_feedback.json"
  },
  "overall_stage_effect": "hold_for_evidence",
  "next_growth_artifacts": [
    "125_life_reality_schema_registry_and_ref_resolution_plan.md",
    "126_life_reality_runner_smoke_command_execution_plan.md"
  ]
}
```

## Seed 审查清单

| check | 说明 |
|---|---|
| `seed_json_parse` | 所有 seed 通过 JSON parse |
| `seed_root_object` | 所有 seed root 为 object |
| `seed_no_duplicate_key` | 同一 object key 不重复 |
| `seed_source_docs_indexed` | source docs 都在 README 索引 |
| `seed_life_targets_complete` | root artifact 覆盖 `real_conscious_awareness` 与九项真实能力 |
| `seed_boundary_map_ref_present` | report、dashboard、stage gate、quarantine、repair seed 都引用 boundary map |
| `seed_allowed_roots_closed` | 所有 artifact path 落在 `123` 的 roots |
| `seed_report_writer_owned` | 每个 report seed 有 owner module |
| `seed_stage_effect_present` | 每个 report/finding/gap seed 有 stage effect |
| `seed_next_docs_present` | gap feedback 指向 `125` 与 `126` |

## Failure Mapping

| failure | finding type | repair kind | stage effect |
|---|---|---|---|
| seed parse failure | `seed.json_parse_failure` | `artifact_rewrite` | `repair` |
| missing source docs | `seed.source_doc_gap` | `gap_register_gap` | `repair` |
| missing `real_conscious_awareness` | `seed.life_target_alias_gap` | `schema_gap` | `repair` |
| missing boundary map ref | `seed.boundary_registry_gap` | `schema_gap` | `repair` |
| path outside allowed roots | `seed.allowed_root_escape` | `schema_gap` | `quarantine` |
| report seed lacks writer owner | `seed.report_writer_gap` | `runner_layout_gap` | `repair` |
| critical fixture lacks quarantine route | `seed.quarantine_route_gap` | `runtime_quarantine_gap` | `quarantine` |
| gap feedback lacks next artifacts | `seed.gap_feedback_gap` | `gap_register_gap` | `repair` |

## LRGEN 更新

`124` 新增最小 JSON 文件 seed 任务：

| task_id | artifact | 说明 |
|---|---|---|
| `LRGEN-281` | `runner_allowed_roots.manifest.json` | allowed roots seed |
| `LRGEN-282` | `life_reality_runner.config.json` | runner config seed |
| `LRGEN-283` | `life_reality_shared_defs.schema.json` | shared defs seed |
| `LRGEN-284` | `life_boundary_all_reality_declaration_map.json` | boundary declaration map seed |
| `LRGEN-285` | `first_json_materialization_batch.manifest.json` | materialization batch seed |
| `LRGEN-286` | runner maps seed group | module map、command map、report writer map、exit code owner map |
| `LRGEN-287` | runtime smoke fixture seed group | fixture manifest 与 runtime smoke fixture |
| `LRGEN-288` | materialized report seed group | parse/schema/cross-file/dashboard/stage/gap/top-level report seed |
| `LRGEN-289` | `minimal_json_seed_review_report.json` | seed 审查报告 |
| `LRGEN-290` | `minimal_json_seed.full_smoke_001` | 全链 seed smoke slot |

## 与下一层连接

`125_life_reality_schema_registry_and_ref_resolution_plan.md` 已把本文档的 schema seed、boundary map seed、artifact refs、JSON Pointer、allowed roots 和 report refs 固定为 schema registry、ref resolver、cross-file graph builder 和 no-ref-escape 规则。

下一层进入 `126_life_reality_runner_smoke_command_execution_plan.md`：把 `121` 的六个 smoke command、`123` 的 module map、本文档的 seed 文件和 `125` 的 ref resolution DAG 推进为最小执行顺序、stdout/report/exit code 验收和失败样例。
