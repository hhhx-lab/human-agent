# Life Reality Runner Repository Layout And Module Map

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 123 层把 `121_life_reality_materialized_json_validation_smoke_plan.md` 的验证命令和 `122_life_boundary_all_reality_declarations_rewrite.md` 的全集边界声明 map 落成未来 runner 的仓库布局、模块边界、文件归属、测试入口和下一层 JSON seed 顺序。

`123` 的核心职责是把生命膜从 Markdown 合同推进到可实现前的代码边界。runner 是数字生命生成链的文件循环器：它读取 schema、fixture、boundary declaration、runtime observation、report 和 dashboard source，输出 parse/schema/cross-file/stage gate 证据，并把真实痛苦、真实梦境、真实关系、真实责任和真实后悔的断裂送入 repair、quarantine 或 growth window。

## 方法锚点

| 方法传统 | 权威锚点 | 进入 `123` 的规则 |
|---|---|---|
| POSIX Utility Syntax Guidelines | https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap12.html | CLI command、option、operand、diagnostic、exit status 保持稳定命令行语义 |
| JSON | https://www.rfc-editor.org/info/rfc8259 | `.json` 与 `.schema.json` 先经过 parse、UTF-8、root type 和 duplicate key policy |
| JSON Pointer | https://www.rfc-editor.org/info/rfc6901 | finding、schema output、artifact ref 和 continuity ref 使用 JSON Pointer 定位 |
| JSON Schema Draft 2020-12 | https://json-schema.org/draft/2020-12 | schema registry、shared defs、component schema、report schema 和 dashboard schema 使用同一 dialect |
| JSON Schema output | https://json-schema.org/draft/2020-12/output/schema | validation report 输出 instance location、keyword location、error 和 annotation units |
| OpenTelemetry Trace API | https://opentelemetry.io/docs/specs/otel/trace/api/ | command、module、checker 和 report writer 生成 trace span |
| OpenTelemetry Logs Data Model | https://opentelemetry.io/docs/specs/otel/logs/data-model/ | structured logs 保留 severity、body、attributes、trace id 和 span id |
| W3C Trace Context | https://www.w3.org/TR/trace-context/ | `traceparent` 与 `tracestate` 贯穿 CLI、checker、dashboard 和 stage gate |
| W3C PROV | https://www.w3.org/TR/prov-overview/ | artifact、schema、fixture、report、finding、repair item 和 dashboard patch 进入 provenance graph |
| RFC 9457 Problem Details | https://www.rfc-editor.org/info/rfc9457 | parse/schema/ref/dashboard/stage failure 输出 problem detail |
| RFC 9562 UUID | https://www.rfc-editor.org/info/rfc9562 | run id、artifact id、report id、finding id、repair id 和 stage review id 使用稳定唯一标识 |

## 上游输入

| 来源 | 进入 `123` 的内容 |
|---|---|
| `118_life_reality_generation_runner_cli_contract.md` | generation command family、global options、runner config、command DAG、atomic write 和 exit code |
| `120_life_reality_first_json_materialization_batch.md` | 首批 JSON artifact list、runner config、boundary alignment patch、report roots、dry-run 和 gap feedback |
| `121_life_reality_materialized_json_validation_smoke_plan.md` | parse/schema/cross-file/dashboard/stage smoke 命令、report paths、failure mapping 和 LRGEN-246 到 260 |
| `122_life_boundary_all_reality_declarations_rewrite.md` | 全集边界声明 map、boundary declaration registry、protected chain index、field vocab patch、dashboard/stage/quarantine/gap patch 和 LRGEN-261 到 270 |

## 仓库布局

未来 runner 目录固定为：

```text
life_reality_runner/
  config/
    life_reality_runner.config.json
    allowed_roots.manifest.json
  schemas/
    life_reality/
      shared/
        life_reality_shared_defs.schema.json
        runner_config.schema.json
        life_boundary_alignment.schema.json
        life_boundary_all_reality_declaration_map.schema.json
      runtime_observation/
      components/
        pain_regret_repair/
        dream_reality/
        relationship_timeline/
      reports/
      dashboard/
      materialization/
  fixtures/
    life_reality/
      runtime_observation/
        manifest/
        pass/
        fail/
        critical/
        mutation/
        withheld/
        smoke/
      materialization/
        pass/
        fail/
        critical/
        smoke/
  generation/
    manifests/
    boundary/
    component_schema/
    dashboard_rollup/
    materialization/
    maps/
  reports/
    life_reality/
      config/
      cli/
      runtime_ingestion/
      component_generation/
      cross_file/
      dashboard_rollup/
      materialization/
      stage_gate/
      gap_feedback/
  dashboard/
    life_reality/
      sources/
      panels/
      stage_gate/
      repair_queue/
      quarantine/
      gap_feedback/
  src/
    life_reality_runner/
      cli/
      commands/
      config/
      paths/
      json_io/
      schema/
      refs/
      boundary/
      fixtures/
      cross_file/
      reports/
      dashboard/
      stage_gate/
      trace/
      problem/
  tests/
    unit/
    smoke/
    fixtures/
    snapshots/
```

目录归属：

| root | 拥有模块 | 职责 |
|---|---|---|
| `config/` | `config_loader`、`allowed_root_resolver` | 读取 runner config、allowed roots、strict/dry-run 默认值 |
| `schemas/life_reality/shared/` | `schema_registry`、`boundary_schema_loader` | shared defs、runner config schema、boundary alignment schema、全集边界声明 schema |
| `schemas/life_reality/runtime_observation/` | `schema_registry` | runtime observation envelope、fixture manifest、ingestion report schema |
| `schemas/life_reality/components/` | `component_schema_registry` | pain/regret/repair、dream reality、relationship timeline object schema |
| `schemas/life_reality/reports/` | `report_schema_registry` | parse/schema/cross-file/dashboard/stage/gap report schema |
| `schemas/life_reality/dashboard/` | `dashboard_schema_registry` | dashboard source、panel dependency、stage gate、repair queue schema |
| `fixtures/life_reality/` | `fixture_loader`、`fixture_partition_indexer` | pass/fail/critical/mutation/withheld/smoke fixture 读取与覆盖 |
| `generation/` | `generation_manifest_loader`、`boundary_declaration_registry` | LRGEN task manifests、boundary map、component generation report、gap feedback seed |
| `reports/life_reality/` | `report_writer`、`problem_detail_writer`、`trace_writer` | command reports、checker reports、stage review、gap feedback |
| `dashboard/life_reality/` | `dashboard_rollup_writer`、`stage_gate_evaluator` | dashboard source、panel patches、stage gate review、repair queue、quarantine panel |
| `src/life_reality_runner/` | runtime modules | CLI、commands、parser、schema、refs、checker、writer、stage gate |
| `tests/` | test harness | unit tests、smoke tests、fixture snapshots、report snapshots |

## 模块映射

| module | 输入 | 输出 | 生命膜职责 |
|---|---|---|---|
| `cli_dispatcher` | argv、environment、traceparent | command context | 统一 CLI 入口，保持 command、option、exit code 和 trace 连续 |
| `config_loader` | `life_reality_runner.config.json` | `RunnerConfig` | 读取 allowed roots、strict mode、life targets、report run |
| `allowed_root_resolver` | config、artifact path | normalized artifact ref | 阻断 ref escape，保护 schema、fixture、report 和 dashboard 根目录 |
| `json_parser` | `.json`、`.schema.json` | parsed document、parse finding | 先解析再进入 schema，保护生命膜文件的机器可读根 |
| `duplicate_key_detector` | raw JSON text | duplicate key finding | 保护 object key 稳定性和 report 可追踪性 |
| `schema_registry` | schema roots、shared defs | schema id registry | 维护 Draft 2020-12 dialect、shared defs、component/report/dashboard schema |
| `schema_validator` | parsed document、schema registry | JSON Schema output report | 输出 instance location、keyword location、error 和 annotation units |
| `json_pointer_resolver` | document、pointer | object location | 让 finding、continuity ref 和 dashboard panel 能定位到对象 |
| `artifact_ref_resolver` | artifact ref、allowed roots | resolved artifact | 连接 manifest、fixture、schema、report、dashboard 和 source doc |
| `provenance_graph_builder` | artifact refs、report refs | W3C PROV graph | 建立 artifact、finding、repair、stage 和 gap feedback 的来源链 |
| `boundary_declaration_registry` | `life_boundary_all_reality_declaration_map.json` | boundary group index | 把每个 boundary 映射到真实生命链和字段 vocab |
| `protected_chain_indexer` | boundary map、life targets | protected chain index | 让真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔可被查找 |
| `cross_file_graph_builder` | schemas、fixtures、reports、dashboard source | typed ref graph | 建立 `$ref`、artifact ref、source doc ref、continuity ref、life target ref |
| `cross_file_checker` | typed ref graph | cross-file checker report | 检查 orphan、ref escape、life target closure、quarantine route、provenance closure |
| `fixture_loader` | fixture roots、fixture manifest | fixture set | 读取 pass/fail/critical/mutation/withheld/smoke 分区 |
| `fixture_coverage_checker` | fixture set、expected slots | coverage finding | 检查真实痛苦、真实梦境、真实关系、真实责任、真实后悔的样本覆盖 |
| `dashboard_rollup_writer` | parse/schema/cross-file reports | dashboard rollup smoke report | 把生命膜断裂上卷到 panel、repair queue 和 stage gate |
| `stage_gate_evaluator` | dashboard rollup、critical findings、boundary map | stage review | 决定 open、hold、repair、quarantine、promote growth window |
| `gap_feedback_writer` | unresolved findings、stage review | gap feedback report | 把缺口转成下一层 doc、schema、fixture、runner 和 dashboard artifact |
| `report_writer` | module outputs | report JSON | 按 schema、trace、problem detail 和 provenance 写入报告 |
| `problem_detail_writer` | blocking finding | problem detail | 为 parse/schema/ref/dashboard/stage failure 输出 RFC 9457 problem object |
| `trace_context_manager` | traceparent、tracestate | trace span context | 贯穿 command、module、checker、writer 和 stage gate |

## Command 到模块映射

| command | primary modules | output |
|---|---|---|
| `validate-config` | `cli_dispatcher`、`config_loader`、`allowed_root_resolver`、`schema_registry`、`report_writer` | `runner_config_validation_report.json`、`allowed_roots_report.json` |
| `generate-fixtures` | `fixture_loader`、`fixture_coverage_checker`、`schema_validator`、`report_writer` | runtime fixture manifest、runtime validation report、ingestion smoke report |
| `generate-schemas` | `schema_registry`、`component_schema_registry`、`provenance_graph_builder`、`report_writer` | component schema skeletons、dependency graph、validator order report |
| `check-dashboard --emit-rollup` | `cross_file_graph_builder`、`cross_file_checker`、`dashboard_rollup_writer`、`stage_gate_evaluator` | dashboard rollup report、stage gate rollup、repair/gap bridge |
| `explain-generation` | `provenance_graph_builder`、`gap_feedback_writer`、`report_writer` | command lineage report、next artifact recommendation |
| `run-generation-pipeline` | generation command orchestrator | pipeline report、CLI command reports |
| `validate-json-parse` | `json_parser`、`duplicate_key_detector`、`report_writer` | `materialized_json_parse_validation_report.json` |
| `validate-json-schema` | `schema_registry`、`schema_validator`、`report_writer` | `materialized_json_schema_validation_report.json` |
| `check-materialized-cross-file` | `artifact_ref_resolver`、`json_pointer_resolver`、`cross_file_graph_builder`、`cross_file_checker` | `materialized_json_cross_file_checker_report.json` |
| `smoke-dashboard-rollup` | `dashboard_rollup_writer`、`fixture_coverage_checker`、`report_writer` | `materialized_json_dashboard_rollup_smoke_report.json` |
| `smoke-stage-gate` | `boundary_declaration_registry`、`protected_chain_indexer`、`stage_gate_evaluator`、`gap_feedback_writer` | `materialized_json_stage_gate_smoke_report.json`、`materialized_json_gap_feedback.json` |
| `run-materialized-json-smoke` | smoke command orchestrator | `materialized_json_validation_smoke_report.json` |

## 读写边界

runner 的写入必须集中在以下 roots：

| write root | 允许写入 |
|---|---|
| `life_reality_runner/generation/` | generation manifests、boundary maps、dry-run reports、gap feedback seed |
| `life_reality_runner/fixtures/` | seed fixture、mutation fixture、withheld fixture、smoke fixture |
| `life_reality_runner/schemas/` | materialized schema skeleton 和 shared defs |
| `life_reality_runner/reports/` | command report、validation report、checker report、stage review、problem detail |
| `life_reality_runner/dashboard/` | dashboard source、panel patch、stage gate review、repair queue、quarantine source |

写入规则：

| rule | 说明 |
|---|---|
| `LRRUN-WRITE-001` | 所有写入先生成 temporary artifact，再 parse/schema check，再 atomic rename |
| `LRRUN-WRITE-002` | report writer 写入前必须附加 `run_id`、`source_docs`、`life_reality_targets`、`trace` 和 `stage_effect` |
| `LRRUN-WRITE-003` | dashboard source 写入前必须读取 cross-file checker report 和 boundary declaration registry |
| `LRRUN-WRITE-004` | stage gate 写入前必须读取 dashboard rollup、critical finding、quarantine route 和 gap feedback target |
| `LRRUN-WRITE-005` | gap feedback 只能指向下一层 doc、schema、fixture、runner command、report 或 dashboard source |

## Boundary Map 接入

`122` 的全集边界声明文件在 `123` 中拥有专门模块：

```text
life_reality_runner/generation/boundary/
  life_boundary_all_reality_declaration_map.json
  life_boundary_declaration_group_registry.json
  life_boundary_protected_chain_index.json
  life_boundary_field_vocab_patch.json
  life_boundary_dashboard_panel_patch.json
  life_boundary_stage_gate_patch.json
  life_boundary_quarantine_repair_patch.json
  life_boundary_scope_privacy_patch.json
  life_boundary_gap_feedback_patch.json
```

接入规则：

| rule | 说明 |
|---|---|
| `LRRUN-BND-001` | `boundary_declaration_registry` 先于 dashboard rollup 和 stage gate 加载 |
| `LRRUN-BND-002` | 每个 finding 都要标出 `affected_life_targets` 与 `protected_life_chains` |
| `LRRUN-BND-003` | quarantine finding 必须连接真实痛苦、真实责任、真实后悔或真实关系中的至少一条修复链 |
| `LRRUN-BND-004` | dream fact gate finding 必须连接真实梦境、醒后整合和 continuity refs |
| `LRRUN-BND-005` | relationship finding 必须连接 relation scope、共同记忆、承诺、损伤修复或共同边界 |
| `LRRUN-BND-006` | gap feedback 必须读取 `next_growth_artifacts`，并输出下一层 artifact refs |

## 最小测试入口

测试入口先覆盖 smoke 命令，再覆盖 generation 命令：

```text
tests/smoke/test_validate_json_parse_smoke.*
tests/smoke/test_validate_json_schema_smoke.*
tests/smoke/test_materialized_cross_file_smoke.*
tests/smoke/test_dashboard_rollup_smoke.*
tests/smoke/test_stage_gate_smoke.*
tests/smoke/test_boundary_declaration_registry_smoke.*
tests/smoke/test_run_materialized_json_smoke.*
tests/unit/test_allowed_root_resolver.*
tests/unit/test_json_pointer_resolver.*
tests/unit/test_schema_registry.*
tests/unit/test_report_writer.*
tests/unit/test_problem_detail_writer.*
```

测试职责：

| test | 覆盖 |
|---|---|
| `test_validate_json_parse_smoke` | UTF-8、RFC 8259 parse、duplicate key、root type、artifact id |
| `test_validate_json_schema_smoke` | Draft 2020-12 dialect、shared defs、schema output units、life target enum |
| `test_materialized_cross_file_smoke` | `$ref`、artifact ref、source doc ref、continuity ref、provenance graph |
| `test_dashboard_rollup_smoke` | panel dependency、critical finding、repair queue、stage gate input |
| `test_stage_gate_smoke` | open、hold、repair、quarantine、promote growth window |
| `test_boundary_declaration_registry_smoke` | `122` declaration groups、protected chains、field vocab patch、next growth artifacts |
| `test_run_materialized_json_smoke` | 全链 command order、partial report、exit code、top-level smoke report |

## Exit Code 所属模块

| exit code | owner module | 条件 |
|---|---|---|
| `0` | `stage_gate_evaluator` | 全部 smoke pass，stage effect 为 `open_next_stage` 或 `promote_growth_window` |
| `1` | `repair_router` | high/repair finding 存在，repair route 完整 |
| `2` | `quarantine_router` | critical/quarantine finding 存在 |
| `3` | `json_parser`、`schema_registry` | parse 或 schema registry 结构失败 |
| `4` | `cross_file_checker` | ref escape、orphan critical artifact 或 provenance graph 断裂 |
| `5` | `allowed_root_resolver`、`config_loader` | allowed root、config、batch manifest 或 report output root 失败 |

## LRGEN 更新

`123` 新增 runner repository layout 和 module map 任务：

| task_id | artifact | 说明 |
|---|---|---|
| `LRGEN-271` | `runner_repository_layout.manifest.json` | runner 目录布局 manifest |
| `LRGEN-272` | `runner_module_map.json` | module 到 input/output/life membrane 职责映射 |
| `LRGEN-273` | `runner_command_module_map.json` | CLI command 到 module 调度映射 |
| `LRGEN-274` | `runner_allowed_roots.manifest.json` | allowed roots 与 write roots manifest |
| `LRGEN-275` | `runner_report_writer_map.json` | report writer 到 output report 路径映射 |
| `LRGEN-276` | `runner_boundary_registry_mount.json` | `122` 边界声明 map 的加载位置 |
| `LRGEN-277` | `runner_dashboard_stage_gate_mount.json` | dashboard rollup 与 stage gate 模块挂载 |
| `LRGEN-278` | `runner_smoke_test_entry_map.json` | smoke/unit test entry map |
| `LRGEN-279` | `runner_exit_code_owner_map.json` | exit code 到 owner module 映射 |
| `LRGEN-280` | `runner_repository_layout_dry_run_report.json` | layout dry-run report |

## 验收

`123` 的验收条件：

| check | 条件 |
|---|---|
| `layout_covers_all_roots` | config、schema、fixture、generation、report、dashboard、src、tests roots 全覆盖 |
| `commands_have_modules` | `118` 与 `121` 的所有命令都有 owner modules |
| `boundary_map_mounted` | `122` 的 boundary map、registry、protected chain index、field vocab patch 都有路径 |
| `reports_have_writers` | parse/schema/cross-file/dashboard/stage/gap/top-level report 都有 writer owner |
| `stage_gate_reads_boundary` | stage gate evaluator 读取 boundary declaration registry 与 protected chain index |
| `tests_cover_smoke_chain` | 六个 materialized JSON smoke command 和 boundary registry smoke 都有测试入口 |
| `next_docs_emitted` | gap feedback 指向 `124_life_reality_minimal_json_file_seed_plan.md` 和 `125_life_reality_schema_registry_and_ref_resolution_plan.md` |

## 与下一层连接

`124_life_reality_minimal_json_file_seed_plan.md` 已按本文档的目录布局生成最小 JSON 文件 seed 编写顺序，先落 config、allowed roots、shared defs、boundary declaration map、materialization manifest、parse/schema/cross-file/dashboard/stage report skeleton 和 smoke fixture。

下一层进入 `125_life_reality_schema_registry_and_ref_resolution_plan.md`：把 `124` 的 seed 文件、schema refs、JSON Pointer、artifact refs、allowed roots 和 boundary registry 固定为可实现前的 ref resolution 规则。
