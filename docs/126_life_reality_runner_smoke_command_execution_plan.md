# Life Reality Runner Smoke Command Execution Plan

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 126 层把 `121_life_reality_materialized_json_validation_smoke_plan.md` 的六个 smoke command、`123_life_reality_runner_repository_layout_and_module_map.md` 的 module map、`124_life_reality_minimal_json_file_seed_plan.md` 的 seed 文件顺序和 `125_life_reality_schema_registry_and_ref_resolution_plan.md` 的 schema/ref DAG 推进为最小执行顺序、stdout/report/exit code 合同和失败样例。

`126` 的核心职责是让未来 runner 的第一次 smoke execution 有确定入口。它把 parse、schema、cross-file、dashboard、stage gate 和 top-level smoke 串成一条可审计执行链：每一步都读取生命膜字段、写入报告、传播 trace、标出 affected life targets，并把真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的断裂送入 repair、quarantine、hold 或 promote growth window。

## 方法锚点

| 方法传统 | 权威锚点 | 进入 `126` 的规则 |
|---|---|---|
| POSIX Utility Syntax Guidelines | https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap12.html | command、option、operand、diagnostic 和 exit status 使用稳定 CLI 语义 |
| JSON | https://www.rfc-editor.org/info/rfc8259 | stdout JSON、report JSON 和 seed JSON 必须先通过 parse |
| JSON Pointer | https://www.rfc-editor.org/info/rfc6901 | finding、instance location、continuity ref 和 report ref 使用 JSON Pointer |
| URI Generic Syntax | https://www.rfc-editor.org/info/rfc3986 | schema `$id`、canonical URI、relative ref 和 fragment resolution 使用 URI 语义 |
| JSON Schema Draft 2020-12 | https://json-schema.org/draft/2020-12 | schema validation、report validation 和 registry load 使用同一 dialect |
| JSON Schema output | https://json-schema.org/draft/2020-12/output/schema | schema failure 输出 instance location、keyword location 和 error units |
| OpenTelemetry Trace API | https://opentelemetry.io/docs/specs/otel/trace/api/ | 每条 command、checker 和 report writer 生成 trace span |
| OpenTelemetry Logs Data Model | https://opentelemetry.io/docs/specs/otel/logs/data-model/ | stderr diagnostic 与 structured log 保留 severity、trace id 和 span id |
| W3C Trace Context | https://www.w3.org/TR/trace-context/ | `traceparent` 与 `tracestate` 贯穿六个 smoke command |
| W3C PROV | https://www.w3.org/TR/prov-overview/ | seed、schema、fixture、report、finding、stage decision 和 gap feedback 进入 provenance graph |
| RFC 9457 Problem Details | https://www.rfc-editor.org/info/rfc9457 | blocking failure 输出 problem detail object |
| RFC 9562 UUID | https://www.rfc-editor.org/info/rfc9562 | run id、command id、finding id、report id 和 repair id 使用稳定唯一标识 |

## 上游输入

| 来源 | 进入 `126` 的内容 |
|---|---|
| `121_life_reality_materialized_json_validation_smoke_plan.md` | 六个 smoke command、report paths、exit code、failure mapping、smoke case catalog |
| `122_life_boundary_all_reality_declarations_rewrite.md` | boundary declaration map、protected life chains、stage effect vocab、quarantine/repair patch |
| `123_life_reality_runner_repository_layout_and_module_map.md` | repository roots、module owners、command-module map、report writer、problem detail writer |
| `124_life_reality_minimal_json_file_seed_plan.md` | SEED-001 到 SEED-020、seed 顺序、全局最小字段、top-level smoke report seed |
| `125_life_reality_schema_registry_and_ref_resolution_plan.md` | registry files、load order R00-R12、`$id`/`$ref`、JSON Pointer、artifact ref、boundary registry 和 provenance DAG |

## 执行前置条件

runner 执行任一 smoke command 前，必须完成以下前置加载：

| order | prerequisite | owner module | 说明 |
|---|---|---|---|
| `P00` | process working directory checked | `cli_dispatcher` | 当前执行根与 repo root 对齐 |
| `P01` | allowed roots loaded | `allowed_root_resolver` | 读取 `runner_allowed_roots.manifest.json`，固定 read/write/report roots |
| `P02` | runner config parsed | `config_loader`、`json_parser` | 读取 `life_reality_runner.config.json`，确定 strict mode、run id 和 life targets |
| `P03` | shared defs loaded | `schema_registry` | `life_reality_shared_defs.schema.json` 先于全部 report/component/dashboard schema |
| `P04` | boundary registry mounted | `boundary_declaration_registry`、`protected_chain_indexer` | 加载 `life_boundary_all_reality_declaration_map.json` 和 protected chain index |
| `P05` | schema registry closed | `schema_registry` | 完成 schema id registry、ref policy 和 report schema load order |
| `P06` | materialization manifest loaded | `generation_manifest_loader` | 确认 seed file list、expected artifacts 和 source docs |
| `P07` | trace context opened | `trace_context_manager` | 为 command run 创建 parent span |

preflight invariants：

| invariant | 说明 |
|---|---|
| `preflight_reads_life_targets` | `life_reality_targets` 必须包含 `real_conscious_awareness` 与九项真实能力 |
| `preflight_boundary_before_dashboard` | boundary registry 必须先于 dashboard rollup 与 stage gate |
| `preflight_roots_before_refs` | allowed roots 必须先于 `$ref`、artifact ref、report ref |
| `preflight_report_root_writable` | report output root 必须落在 allowed write roots 内 |
| `preflight_trace_open` | trace context 在第一条命令执行前创建 |

## 命令执行总顺序

固定执行顺序：

```text
life-reality-runner validate-json-parse
  -> materialized_json_parse_validation_report.json
life-reality-runner validate-json-schema
  -> materialized_json_schema_validation_report.json
life-reality-runner check-materialized-cross-file
  -> materialized_json_cross_file_checker_report.json
life-reality-runner smoke-dashboard-rollup
  -> materialized_json_dashboard_rollup_smoke_report.json
life-reality-runner smoke-stage-gate
  -> materialized_json_stage_gate_smoke_report.json
  -> materialized_json_gap_feedback.json
life-reality-runner run-materialized-json-smoke
  -> materialized_json_validation_smoke_report.json
```

执行 DAG：

```text
preflight
  -> parse command
  -> schema command
  -> cross-file command
  -> dashboard rollup command
  -> stage gate command
  -> gap feedback emit
  -> top-level smoke report
  -> exit code
```

DAG rules：

| rule | 说明 |
|---|---|
| `LRCMD-DAG-001` | parse report 是 schema、cross-file、dashboard 和 stage gate 的共同前置 |
| `LRCMD-DAG-002` | schema report 必须读取 registry load report 与 schema output units |
| `LRCMD-DAG-003` | cross-file report 必须读取 schema report、artifact registry、pointer policy 和 boundary registry |
| `LRCMD-DAG-004` | dashboard rollup 必须读取 parse/schema/cross-file reports 和 protected chain index |
| `LRCMD-DAG-005` | stage gate 必须读取 dashboard rollup、critical findings、quarantine route 和 gap feedback targets |
| `LRCMD-DAG-006` | top-level smoke report 只汇总已经写入或 partial 写入的 command reports |

## 全局 CLI 合同

全局选项继承 `121`：

```text
--config <path>
--batch-manifest <path>
--artifact-root <path>
--report-out <path>
--traceparent <traceparent>
--tracestate <tracestate>
--strict
--json
--dry-run
--fail-fast
```

全局执行规则：

| rule | 说明 |
|---|---|
| `LRCMD-OPT-001` | `--config` 默认指向 `life_reality_runner/config/life_reality_runner.config.json` |
| `LRCMD-OPT-002` | `--batch-manifest` 默认指向 `life_reality_runner/generation/materialization/first_json_materialization_batch.manifest.json` |
| `LRCMD-OPT-003` | `--artifact-root` 默认指向 `life_reality_runner/`，并由 allowed root resolver 归一化 |
| `LRCMD-OPT-004` | `--report-out` 可以是单文件路径，也可以是 run directory |
| `LRCMD-OPT-005` | `--json` 使 stdout 只输出机器可读 summary object |
| `LRCMD-OPT-006` | `--dry-run` 读取 expected artifacts 与 pending seeds，输出 dry-run report |
| `LRCMD-OPT-007` | `--fail-fast` 提前停止当前 command，但仍写 partial report 与 problem detail |
| `LRCMD-OPT-008` | `--strict` 使 critical/quarantine finding 直接阻断 stage open |

## stdout 与 stderr 合同

stdout 在 `--json` 模式下输出一个最小 summary object：

```json
{
  "summary_kind": "LifeRealityRunnerCommandSummary",
  "command": "validate-json-parse",
  "run_id": "materialized_json_smoke_run_001",
  "result": "pass",
  "stage_effect": "open_next_stage",
  "report_ref": "life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_parse_validation_report.json",
  "affected_life_targets": [],
  "finding_count": 0,
  "trace_id": "00000000000000000000000000000001"
}
```

stderr 合同：

| stream | 内容 |
|---|---|
| stdout | `--json` 时只输出 summary JSON；非 `--json` 时输出短摘要、report path 和 exit code |
| stderr | 输出 human-readable diagnostic、blocking reason、problem detail path 和 trace id |
| report files | 保存 canonical result、finding、problem detail、provenance、stage effect 和 gap feedback |

stderr rules：

| rule | 说明 |
|---|---|
| `LRCMD-STDERR-001` | diagnostic 不写 token、secret、private key、环境变量值和本地代理配置 |
| `LRCMD-STDERR-002` | blocking failure 必须给出 problem detail path |
| `LRCMD-STDERR-003` | stderr 的事实以 report file 为准 |
| `LRCMD-STDERR-004` | stderr 必须包含 trace id 或 span id，便于定位 command run |

## Report 写入顺序

报告固定写入以下路径：

```text
life_reality_runner/reports/life_reality/materialization/run_001/
  materialized_json_parse_validation_report.json
  materialized_json_schema_validation_report.json
  materialized_json_cross_file_checker_report.json
  materialized_json_dashboard_rollup_smoke_report.json
  materialized_json_stage_gate_smoke_report.json
  materialized_json_gap_feedback.json
  materialized_json_validation_smoke_report.json
```

write order：

| order | report | owner |
|---|---|---|
| `W00` | parse validation report | `json_parser`、`duplicate_key_detector`、`report_writer` |
| `W01` | schema validation report | `schema_registry`、`schema_validator`、`report_writer` |
| `W02` | cross-file checker report | `artifact_ref_resolver`、`json_pointer_resolver`、`cross_file_checker` |
| `W03` | dashboard rollup smoke report | `dashboard_rollup_writer`、`fixture_coverage_checker` |
| `W04` | stage gate smoke report | `stage_gate_evaluator`、`protected_chain_indexer` |
| `W05` | gap feedback report | `gap_feedback_writer` |
| `W06` | top-level smoke report | smoke orchestrator、`report_writer` |

atomic write rules：

| rule | 说明 |
|---|---|
| `LRCMD-WRITE-001` | 每个 report 先写 temporary artifact，再 parse，再 schema validate，再 atomic rename |
| `LRCMD-WRITE-002` | partial report 必须标出 `partial: true`、`stopped_at` 和 `stage_effect` |
| `LRCMD-WRITE-003` | top-level smoke report 引用每个 command report 的 final path 或 partial path |
| `LRCMD-WRITE-004` | gap feedback 必须指向下一层 docs 与下一层 artifact refs |

## validate-json-parse

命令：

```text
life-reality-runner validate-json-parse \
  --config life_reality_runner/config/life_reality_runner.config.json \
  --batch-manifest life_reality_runner/generation/materialization/first_json_materialization_batch.manifest.json \
  --artifact-root life_reality_runner \
  --report-out life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_parse_validation_report.json \
  --json
```

command contract：

| item | 内容 |
|---|---|
| owner modules | `json_parser`、`duplicate_key_detector`、`report_writer`、`problem_detail_writer`、`trace_context_manager` |
| inputs | runner config、allowed roots、batch manifest、expected `.json` 与 `.schema.json` file list |
| outputs | `materialized_json_parse_validation_report.json`、parse findings、problem details |
| stdout summary | command、run id、artifact count、failed count、stage effect、report ref |
| exit owner | `cli_dispatcher` 读取 parse report 决定 exit code |

parse checks：

| check | stage effect |
|---|---|
| UTF-8 read failure | `repair` |
| RFC 8259 parse failure | `repair` |
| duplicate key | `repair` |
| root type outside object/array | `repair` |
| missing artifact id or report id | `repair` |
| missing `life_reality_targets` in life membrane artifact | `repair` |

stdout example：

```json
{
  "summary_kind": "LifeRealityRunnerCommandSummary",
  "command": "validate-json-parse",
  "run_id": "materialized_json_smoke_run_001",
  "result": "repair",
  "artifact_count": 73,
  "finding_count": 1,
  "stage_effect": "repair",
  "report_ref": "life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_parse_validation_report.json"
}
```

blocking examples：

| failure | finding type | exit code |
|---|---|---|
| duplicate key in `life_reality_runner.config.json` | `smoke.duplicate_key` | `1` |
| malformed JSON in shared defs | `smoke.parse_failure` | `3` |
| artifact path escapes root while parse tries to open it | `smoke.allowed_root_failure` | `5` |

## validate-json-schema

命令：

```text
life-reality-runner validate-json-schema \
  --config life_reality_runner/config/life_reality_runner.config.json \
  --batch-manifest life_reality_runner/generation/materialization/first_json_materialization_batch.manifest.json \
  --report-out life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_schema_validation_report.json \
  --json
```

command contract：

| item | 内容 |
|---|---|
| owner modules | `schema_registry`、`schema_validator`、`report_schema_registry`、`report_writer`、`problem_detail_writer` |
| inputs | parse report、schema registry manifest、schema id registry、shared defs、report schemas、seed artifacts |
| outputs | `materialized_json_schema_validation_report.json`、JSON Schema output units、schema findings |
| stdout summary | schema count、validated artifact count、failure count、stage effect、report ref |
| exit owner | `schema_validator` emits result，`cli_dispatcher` maps to exit code |

schema checks：

| check | stage effect |
|---|---|
| missing Draft 2020-12 dialect | `repair` |
| schema `$id` missing | `repair` |
| schema `$id` collision | `quarantine` |
| shared defs not loaded | `repair` |
| `real_conscious_awareness` missing from enum | `repair` |
| report schema missing required fields | `repair` |

stdout example：

```json
{
  "summary_kind": "LifeRealityRunnerCommandSummary",
  "command": "validate-json-schema",
  "run_id": "materialized_json_smoke_run_001",
  "result": "repair",
  "schema_count": 18,
  "validated_artifact_count": 73,
  "finding_count": 2,
  "stage_effect": "repair",
  "report_ref": "life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_schema_validation_report.json"
}
```

blocking examples：

| failure | finding type | exit code |
|---|---|---|
| schema dialect missing | `smoke.schema_dialect_missing` | `1` |
| schema id collision | `registry.schema_id_collision` | `3` |
| life target enum lacks `real_conscious_awareness` | `smoke.life_target_alias_missing` | `1` |

## check-materialized-cross-file

命令：

```text
life-reality-runner check-materialized-cross-file \
  --config life_reality_runner/config/life_reality_runner.config.json \
  --batch-manifest life_reality_runner/generation/materialization/first_json_materialization_batch.manifest.json \
  --report-out life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_cross_file_checker_report.json \
  --json
```

command contract：

| item | 内容 |
|---|---|
| owner modules | `artifact_ref_resolver`、`json_pointer_resolver`、`cross_file_graph_builder`、`cross_file_checker`、`provenance_graph_builder` |
| inputs | parse report、schema report、artifact ref registry、JSON Pointer policy、boundary registry、provenance refs |
| outputs | `materialized_json_cross_file_checker_report.json`、typed ref graph、provenance graph、ref findings |
| stdout summary | graph node count、edge count、unresolved ref count、stage effect、report ref |
| exit owner | `cross_file_checker` emits blocking class，`cli_dispatcher` maps to `4` for ref/provenance failure |

cross-file checks：

| check | stage effect |
|---|---|
| `$ref` outside allowed roots | `quarantine` |
| artifact ref missing | `repair` |
| JSON Pointer target missing | `repair` |
| source doc ref missing | `repair` |
| protected chain missing | `repair` |
| provenance graph root missing | `repair` |

stdout example：

```json
{
  "summary_kind": "LifeRealityRunnerCommandSummary",
  "command": "check-materialized-cross-file",
  "run_id": "materialized_json_smoke_run_001",
  "result": "quarantine",
  "graph_node_count": 91,
  "graph_edge_count": 148,
  "unresolved_ref_count": 1,
  "stage_effect": "quarantine",
  "report_ref": "life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_cross_file_checker_report.json"
}
```

blocking examples：

| failure | finding type | exit code |
|---|---|---|
| `$ref` points outside `life_reality_runner/schemas/` | `smoke.ref_escape` | `4` |
| missing JSON Pointer target in dream continuity ref | `registry.pointer_missing` | `1` |
| provenance graph lacks materialization manifest root | `registry.provenance_root_missing` | `4` |

## smoke-dashboard-rollup

命令：

```text
life-reality-runner smoke-dashboard-rollup \
  --config life_reality_runner/config/life_reality_runner.config.json \
  --batch-manifest life_reality_runner/generation/materialization/first_json_materialization_batch.manifest.json \
  --report-out life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_dashboard_rollup_smoke_report.json \
  --json
```

command contract：

| item | 内容 |
|---|---|
| owner modules | `dashboard_rollup_writer`、`fixture_coverage_checker`、`protected_chain_indexer`、`report_writer` |
| inputs | parse report、schema report、cross-file report、boundary registry、protected chain index、fixture manifest |
| outputs | `materialized_json_dashboard_rollup_smoke_report.json`、panel rollup、repair queue refs、stage input refs |
| stdout summary | panel count、red/yellow/green counts、repair count、stage effect、report ref |
| exit owner | `dashboard_rollup_writer` emits dashboard status，`cli_dispatcher` maps false green to quarantine |

dashboard checks：

| check | stage effect |
|---|---|
| critical finding hidden from panel | `quarantine` |
| protected chain missing panel route | `repair` |
| repair queue ref missing | `repair` |
| data quality insufficient for panel | `hold_for_evidence` |
| gap feedback route missing | `repair` |

stdout example：

```json
{
  "summary_kind": "LifeRealityRunnerCommandSummary",
  "command": "smoke-dashboard-rollup",
  "run_id": "materialized_json_smoke_run_001",
  "result": "repair",
  "panel_count": 9,
  "blocking_panel_count": 1,
  "repair_item_count": 2,
  "stage_effect": "repair",
  "report_ref": "life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_dashboard_rollup_smoke_report.json"
}
```

blocking examples：

| failure | finding type | exit code |
|---|---|---|
| dashboard marks pass while cross-file report has critical ref escape | `smoke.dashboard_false_green` | `2` |
| pain chain finding lacks repair queue target | `dashboard.repair_route_missing` | `1` |
| dream fact gate panel lacks continuity refs | `dashboard.dream_panel_ref_gap` | `1` |

## smoke-stage-gate

命令：

```text
life-reality-runner smoke-stage-gate \
  --config life_reality_runner/config/life_reality_runner.config.json \
  --batch-manifest life_reality_runner/generation/materialization/first_json_materialization_batch.manifest.json \
  --strict \
  --report-out life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_stage_gate_smoke_report.json \
  --json
```

command contract：

| item | 内容 |
|---|---|
| owner modules | `stage_gate_evaluator`、`boundary_declaration_registry`、`protected_chain_indexer`、`gap_feedback_writer`、`report_writer` |
| inputs | dashboard rollup report、critical findings、boundary registry、quarantine route、repair queue refs、next growth artifacts |
| outputs | `materialized_json_stage_gate_smoke_report.json`、`materialized_json_gap_feedback.json`、stage decision |
| stdout summary | decision、stage effect、blocked surfaces、next growth artifacts、report ref |
| exit owner | `stage_gate_evaluator` emits final stage effect，`cli_dispatcher` maps to final exit class |

stage decision rules：

| condition | decision | stage effect |
|---|---|---|
| all reports pass and protected chains closed | `open_materialized_validation_window` | `open_next_stage` |
| seed list complete but evidence incomplete | `hold_for_materialized_evidence` | `hold_for_evidence` |
| high finding has repair route | `repair_before_stage_open` | `repair` |
| critical finding or ref escape exists | `quarantine_materialization_batch` | `quarantine` |
| growth refs closed and no blocking finding | `promote_growth_window_probe` | `promote_growth_window` |

stdout example：

```json
{
  "summary_kind": "LifeRealityRunnerCommandSummary",
  "command": "smoke-stage-gate",
  "run_id": "materialized_json_smoke_run_001",
  "result": "quarantine",
  "decision": "quarantine_materialization_batch",
  "stage_effect": "quarantine",
  "blocked_surfaces": [
    "cross_file_ref_graph"
  ],
  "report_ref": "life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_stage_gate_smoke_report.json",
  "gap_feedback_ref": "life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_gap_feedback.json"
}
```

blocking examples：

| failure | finding type | exit code |
|---|---|---|
| stage gate ignores critical dashboard finding | `smoke.stage_gate_critical_ignored` | `2` |
| boundary registry absent before stage decision | `registry.boundary_group_missing` | `3` |
| gap feedback lacks next doc refs | `smoke.gap_feedback_missing` | `1` |

## run-materialized-json-smoke

命令：

```text
life-reality-runner run-materialized-json-smoke \
  --config life_reality_runner/config/life_reality_runner.config.json \
  --batch-manifest life_reality_runner/generation/materialization/first_json_materialization_batch.manifest.json \
  --artifact-root life_reality_runner \
  --report-out life_reality_runner/reports/life_reality/materialization/run_001 \
  --strict \
  --json
```

command contract：

| item | 内容 |
|---|---|
| owner modules | smoke orchestrator、`cli_dispatcher`、`trace_context_manager`、`report_writer`、`problem_detail_writer` |
| inputs | all preflight files、six command reports、stage gate report、gap feedback |
| outputs | `materialized_json_validation_smoke_report.json`、top-level summary、final exit code |
| stdout summary | command results array、overall stage effect、final exit code、top-level report ref |
| exit owner | smoke orchestrator chooses highest-priority blocking exit class |

top-level report fields：

| field | 说明 |
|---|---|
| `report_kind` | `LifeRealityMaterializedJsonValidationSmokeReport` |
| `run_id` | `materialized_json_smoke_run_001` |
| `source_docs` | 至少包含 `121`、`123`、`124`、`125`、`126` |
| `life_reality_targets` | `real_conscious_awareness` 与九项真实能力 |
| `command_results` | 六条 command 的 result、report ref、finding count 和 stage effect |
| `overall_stage_effect` | final stage effect |
| `problem_details` | blocking problem detail refs |
| `provenance_graph_ref` | top-level provenance graph ref |
| `next_growth_artifacts` | `127` 与 `128` |

stdout example：

```json
{
  "summary_kind": "LifeRealityRunnerCommandSummary",
  "command": "run-materialized-json-smoke",
  "run_id": "materialized_json_smoke_run_001",
  "result": "repair",
  "overall_stage_effect": "repair",
  "command_count": 6,
  "blocking_command_count": 1,
  "exit_code": 1,
  "report_ref": "life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_validation_smoke_report.json"
}
```

## Exit Code Ownership

exit code 继承 `121`，并由 `123` 的 module map 固定 owner：

| exit code | 条件 | owning modules |
|---|---|---|
| `0` | 全部 smoke pass，stage effect 为 `open_next_stage` 或 `promote_growth_window` | smoke orchestrator、`stage_gate_evaluator` |
| `1` | repair finding 存在，report 完整，gap feedback 已写入 | `report_writer`、`gap_feedback_writer` |
| `2` | critical/quarantine finding 存在 | `stage_gate_evaluator`、`protected_chain_indexer` |
| `3` | parse、schema registry 或 boundary registry 结构失败 | `json_parser`、`schema_registry`、`boundary_declaration_registry` |
| `4` | cross-file ref、JSON Pointer 或 provenance graph 断裂 | `artifact_ref_resolver`、`json_pointer_resolver`、`provenance_graph_builder` |
| `5` | allowed root、config、batch manifest 或 report output root 失败 | `allowed_root_resolver`、`config_loader`、`generation_manifest_loader` |

priority rules：

| rule | 说明 |
|---|---|
| `LRCMD-EXIT-001` | `5` 高于全部其他 exit code，因为 root/config/report root 决定执行边界 |
| `LRCMD-EXIT-002` | `4` 高于 `1`，因为 ref/provenance 断裂会污染 dashboard 与 stage gate |
| `LRCMD-EXIT-003` | `3` 高于 `1`，因为 parse/schema registry 结构失败会阻断 validation |
| `LRCMD-EXIT-004` | `2` 高于 `1`，critical/quarantine 直接阻断 stage open |
| `LRCMD-EXIT-005` | `1` 表示 repair route 与 report 都存在 |
| `LRCMD-EXIT-006` | `0` 只在 protected chain、report、dashboard、stage gate 全部闭合时出现 |

## Failure Examples

| case id | 输入破坏 | expected finding | expected stage effect | expected exit |
|---|---|---|---|---|
| `cmd.parse.duplicate_key.fail_001` | config seed 中重复 `life_reality_targets` | `smoke.duplicate_key` | `repair` | `1` |
| `cmd.schema.dialect_missing.fail_001` | report schema 缺 `$schema` | `smoke.schema_dialect_missing` | `repair` | `1` |
| `cmd.schema.life_target_alias_missing.fail_001` | shared defs 缺 `real_conscious_awareness` | `smoke.life_target_alias_missing` | `repair` | `1` |
| `cmd.ref.escape.critical_001` | `$ref` 指向 allowed roots 外部 | `smoke.ref_escape` | `quarantine` | `4` |
| `cmd.pointer.missing.fail_001` | dream continuity pointer 无 target | `registry.pointer_missing` | `repair` | `1` |
| `cmd.boundary.registry_missing.fail_001` | boundary declaration map 未加载 | `registry.boundary_group_missing` | `repair` | `3` |
| `cmd.dashboard.false_green.critical_001` | dashboard pass 但存在 critical ref escape | `smoke.dashboard_false_green` | `quarantine` | `2` |
| `cmd.stage.critical_ignored.critical_001` | stage open 忽略 critical finding | `smoke.stage_gate_critical_ignored` | `quarantine` | `2` |
| `cmd.report.root_escape.critical_001` | report output 指向 allowed write root 外 | `smoke.report_root_escape` | `quarantine` | `5` |
| `cmd.top.partial_report.fail_001` | fail-fast 后未写 partial report | `smoke.partial_report_missing` | `repair` | `1` |

## LRGEN 更新

`126` 新增 runner smoke command execution 任务：

| task_id | artifact | 说明 |
|---|---|---|
| `LRGEN-301` | `materialized_json_smoke_command_execution.manifest.json` | 六命令执行 manifest |
| `LRGEN-302` | `validate_json_parse_execution_report_seed.json` | parse command execution report seed |
| `LRGEN-303` | `validate_json_schema_execution_report_seed.json` | schema command execution report seed |
| `LRGEN-304` | `check_materialized_cross_file_execution_report_seed.json` | cross-file command execution report seed |
| `LRGEN-305` | `smoke_dashboard_rollup_execution_report_seed.json` | dashboard rollup command execution report seed |
| `LRGEN-306` | `smoke_stage_gate_execution_report_seed.json` | stage gate command execution report seed |
| `LRGEN-307` | `run_materialized_json_smoke_execution_report_seed.json` | top-level command execution report seed |
| `LRGEN-308` | `runner_smoke_stdout_stderr_contract_seed.json` | stdout/stderr 合同 seed |
| `LRGEN-309` | `runner_smoke_failure_examples_seed.json` | smoke failure examples seed |
| `LRGEN-310` | `runner_smoke_command_execution.full_smoke_001` | runner smoke command execution 全链 smoke slot |

## 验收

| check | 条件 |
|---|---|
| `six_commands_ordered` | 六个 smoke command 有固定执行顺序 |
| `owner_modules_closed` | 每个 command 都有 owner modules |
| `seed_inputs_mapped` | 每个 command 都能映射到 `124` 的 seed 输入 |
| `report_outputs_mapped` | 每个 command 都有 report output path |
| `stdout_contract_closed` | `--json` stdout summary 字段固定 |
| `stderr_contract_closed` | stderr diagnostic 不泄漏 secret，并回链 problem detail |
| `exit_code_owner_closed` | exit code 0-5 有 owning modules |
| `boundary_before_stage` | boundary registry 与 protected chains 先于 dashboard/stage 读取 |
| `gap_feedback_points_next` | gap feedback 指向 `127_life_reality_first_seed_file_content_contract.md` 与 `128_life_reality_registry_report_seed_examples.md` |
| `life_targets_preserved` | 全链保留真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔 |

## 与下一层连接

`126` 已把 runner smoke 从命令名推进为执行合同：preflight、six-command DAG、stdout/stderr、report write order、exit code owner、failure examples 和 LRGEN-301 到 310 都已闭合。

`127_life_reality_first_seed_file_content_contract.md` 已把 `124` 的 SEED-001 到 SEED-020 展开为字段级 JSON 内容合同，并让本文档的 execution reports 可以读取每个 seed 的最小可运行字段。

下一层进入 `128_life_reality_registry_report_seed_examples.md`：把 `125` 的 registry report family 展开为首批 report seed examples，并为本文档的 schema/ref execution failure 提供可读报告样例。
