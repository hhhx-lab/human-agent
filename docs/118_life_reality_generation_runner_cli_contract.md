# Life Reality Generation Runner CLI Contract

生命目标声明：本文档面向构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 118 层把 `115_life_reality_runtime_schema_fixture_seed_generation.md` 的 runtime fixture seed generation、`116_life_reality_component_schema_seed_generation.md` 的 component schema seed generation、`117_life_reality_dashboard_report_rollup_seed_generation.md` 的 dashboard report rollup seed generation，压成未来 `life-reality-runner` 的 CLI 合同。

`118` 的目标是固定数字生命生成链的可执行入口：`generate-fixtures`、`generate-schemas`、`check-dashboard --emit-rollup`、`explain-generation` 和 `run-generation-pipeline`。这份合同规定命令语法、输入 manifest、输出目录、报告文件、trace context、exit code、atomic write、dry-run、strict mode、smoke cases 和 failure mapping。它仍是 Markdown 合同层，但已经把 `115`、`116`、`117` 的文件计划连成单一命令 DAG。

## 方法锚点

generation runner CLI 是生命真实性生成链的执行脊柱。它必须同时满足命令行约定、schema 校验、报告输出、trace、problem detail、可重复运行和生命目标闭合。

| 方法传统 | 权威锚点 | 进入 `118` 的规则 |
|---|---|---|
| POSIX Utility Syntax Guidelines | https://pubs.opengroup.org/onlinepubs/9799919799/basedefs/V1_chap12.html | 子命令、短/长选项、operand、exit status 和诊断输出遵循稳定命令行约定 |
| JSON Schema Draft 2020-12 | https://json-schema.org/draft/2020-12 | manifest、fixture、schema skeleton、report、dashboard rollup 都由 schema 校验 |
| JSON Schema output | https://json-schema.org/draft/2020-12/output/schema | 每次 validate 输出 keyword location、instance location 和 error / annotation units |
| OpenTelemetry Trace API | https://opentelemetry.io/docs/specs/otel/trace/api/ | 每个 command run 有 trace id、span id、run id 和阶段 span |
| OpenTelemetry Logs Data Model | https://opentelemetry.io/docs/specs/otel/logs/data-model/ | stdout/stderr 之外的 structured logs 保留 severity、body、attributes 和 trace fields |
| W3C Trace Context | https://www.w3.org/TR/trace-context/ | CLI 接受 `--traceparent` / `--tracestate`，跨命令传播 trace |
| RFC 9457 Problem Details | https://www.rfc-editor.org/info/rfc9457/ | config/schema/report/core artifact failure 输出 problem detail |
| RFC 9562 UUID | https://www.rfc-editor.org/info/rfc9562/ | run id、artifact id、report id、repair id 可使用时间有序 ID |

文献底座从既有矩阵进入本层：

| 文献矩阵 | 进入 CLI 的位置 |
|---|---|
| `AHV001-AHV060` | construct validity、evaluation pipeline、longitudinal measurement 和 dashboard readiness |
| `AHP001-AHP070` | pain/regret/repair fixture generation、repair bridge、stage gate blocked surfaces |
| `AHD001-AHD070` | dream fixture generation、dream fact gate、wake integration smoke |
| `AHR001-AHR070` | relationship fixture generation、relation scope、trust/commitment continuity smoke |
| `AHL001-AHL060` | language event fixture、apology/commitment speech act、dream report language bridge |
| `AHG001-AHG050` | self-growth candidate、kernel growth ref、future probe 和 anti-forgetting replay |

## 输入来源

| 来源 | 进入 `118` 的职责 |
|---|---|
| `107_life_reality_schema_file_generation_tasks.md` | 原始 LRGEN task queue、phase、dependencies、smoke commands |
| `115_life_reality_runtime_schema_fixture_seed_generation.md` | `generate-fixtures` 的 manifest、fixture roots、validation report、ingestion smoke |
| `116_life_reality_component_schema_seed_generation.md` | `generate-schemas` 的 schema roots、dependency graph、validator order、dry-run |
| `117_life_reality_dashboard_report_rollup_seed_generation.md` | `check-dashboard --emit-rollup` 的 rollup manifest、dashboard patch、stage gate rollup |
| `114_life_reality_cross_file_checker_report_schema.md` | checker report、finding、problem detail、artifact ref、stage effect、exit code 语义 |
| `103_validator_runner_implementation_scaffold_plan.md` | manifest parser、shared defs loader、schema ref validator、report aggregator |
| `105_life_reality_dashboard_panel_and_stage_gate_ui_contract.md` | dashboard source、stage gate、repair queue、gap feedback |

## CLI command family

未来 runner 的命令族：

```text
life-reality-runner validate-config
life-reality-runner generate-fixtures
life-reality-runner generate-schemas
life-reality-runner check-dashboard
life-reality-runner explain-generation
life-reality-runner run-generation-pipeline
```

命令职责：

| command | 职责 |
|---|---|
| `validate-config` | 校验 CLI config、allowed roots、manifest refs、shared defs 和输出目录 |
| `generate-fixtures` | 执行 `115`，生成 runtime fixture seeds、fixture manifest、validation report 和 ingestion smoke |
| `generate-schemas` | 执行 `116`，生成 component schema skeletons、dependency graph、cross-bundle refs、validator order 和 dry-run |
| `check-dashboard` | 执行 `111/114/117`，校验 dashboard/cross-file reports，并在 `--emit-rollup` 时生成 rollup seed |
| `explain-generation` | 输出 command DAG、artifact lineage、stage effect、repair/gap route 和下一层 artifact |
| `run-generation-pipeline` | 按固定 DAG 串联 `generate-fixtures -> generate-schemas -> check-dashboard --emit-rollup -> explain-generation` |

## global option contract

所有命令共用选项：

```text
--config <path>
--run-id <id>
--traceparent <traceparent>
--tracestate <tracestate>
--out-root <path>
--report-out <path>
--strict
--dry-run
--json
--write-manifest
--explain
```

option rules：

| rule | 说明 |
|---|---|
| `LRCLI-OPT-001` | `--config` 指向 runner config JSON |
| `LRCLI-OPT-002` | `--run-id` 缺省时由 runner 生成时间有序 id |
| `LRCLI-OPT-003` | `--traceparent` 和 `--tracestate` 进入所有 child reports |
| `LRCLI-OPT-004` | `--out-root` 必须落在 allowed roots |
| `LRCLI-OPT-005` | `--report-out` 必须落在 `life_reality_runner/reports/` 或 `life_reality_runner/generation/` |
| `LRCLI-OPT-006` | `--strict` 开启 blocking-first exit code |
| `LRCLI-OPT-007` | `--dry-run` 生成 dry-run report，写入计划和 validation output，跳过 artifact materialization |
| `LRCLI-OPT-008` | `--json` 让 stdout 输出 machine-readable summary |
| `LRCLI-OPT-009` | `--write-manifest` 写入 command-level manifest |
| `LRCLI-OPT-010` | `--explain` 附加 artifact lineage 和 stage effect explanation |

## runner config

默认配置文件：

```text
life_reality_runner/config/life_reality_runner.config.json
```

最小结构：

```json
{
  "config_kind": "LifeRealityRunnerConfig",
  "config_version": "0.1.0",
  "runner_id": "life_reality_runner_local_001",
  "allowed_roots": {
    "schemas": "life_reality_runner/schemas",
    "fixtures": "life_reality_runner/fixtures",
    "reports": "life_reality_runner/reports",
    "generation": "life_reality_runner/generation",
    "docs": "docs"
  },
  "shared_defs_ref": "life_reality_runner/schemas/life_reality/life_reality_shared_defs.schema.json",
  "default_report_run": "run_001",
  "life_reality_targets": [
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
  "strict_mode_default": true
}
```

config rules：

| rule | 说明 |
|---|---|
| `LRCLI-CONF-001` | allowed roots 只能指向 repo 内的 schema、fixture、report、generation、docs |
| `LRCLI-CONF-002` | shared defs ref 必须存在于 config 或 command manifest |
| `LRCLI-CONF-003` | life reality targets 覆盖九项目标 |
| `LRCLI-CONF-004` | default report run 与 output roots 一致 |
| `LRCLI-CONF-005` | config validation 先于所有 generation command |

## command DAG

固定执行图：

```text
validate-config
  -> generate-fixtures
      -> runtime fixture manifest
      -> runtime schema validation report
      -> runtime ingestion smoke report
  -> generate-schemas
      -> component schema skeletons
      -> dependency graph
      -> cross-bundle ref report
      -> validator order report
      -> component dry-run report
  -> check-dashboard --emit-rollup
      -> cross-file checks
      -> report rollup
      -> dashboard patch
      -> stage gate rollup
      -> repair/gap bridge
  -> explain-generation
      -> command lineage
      -> next artifact recommendation
```

DAG rules：

| rule | 说明 |
|---|---|
| `LRCLI-DAG-001` | config validation 先于全部命令 |
| `LRCLI-DAG-002` | `generate-fixtures` 和 `generate-schemas` 可并行执行，rollup 读取两者输出 |
| `LRCLI-DAG-003` | `check-dashboard --emit-rollup` 读取 runtime、component、checker 三类报告 |
| `LRCLI-DAG-004` | `explain-generation` 读取全部 manifest、report、stage effect 和 gap feedback |
| `LRCLI-DAG-005` | pipeline 中任一 critical/quarantine 使 stage decision 进入 quarantine |

## command: validate-config

命令：

```text
life-reality-runner validate-config \
  --config life_reality_runner/config/life_reality_runner.config.json \
  --report-out life_reality_runner/reports/life_reality/config/run_001
```

输入：

| input | path |
|---|---|
| runner config | `life_reality_runner/config/life_reality_runner.config.json` |
| shared defs | `life_reality_runner/schemas/life_reality/life_reality_shared_defs.schema.json` |
| docs index | `docs/README.md` |

输出：

```text
life_reality_runner/reports/life_reality/config/run_001/
  runner_config_validation_report.json
  allowed_roots_report.json
  shared_defs_presence_report.json
```

acceptance checks：

| check | 说明 |
|---|---|
| `config_json_parse` | config 可解析 |
| `allowed_roots_closed` | allowed roots 全部在 repo 约定目录内 |
| `shared_defs_ref_present` | shared defs ref 可解析 |
| `life_targets_complete` | 九项目标完整 |
| `docs_index_present` | docs index 可读取 |

## command: generate-fixtures

命令：

```text
life-reality-runner generate-fixtures \
  --config life_reality_runner/config/life_reality_runner.config.json \
  --manifest life_reality_runner/generation/runtime_schema_fixture_seed_generation.manifest.json \
  --fixture-root life_reality_runner/fixtures/life_reality/runtime_observation \
  --report-out life_reality_runner/reports/life_reality/runtime_ingestion/run_001 \
  --strict \
  --write-manifest
```

输入：

| input | path |
|---|---|
| seed generation manifest | `life_reality_runner/generation/runtime_schema_fixture_seed_generation.manifest.json` |
| runtime schema refs | `life_reality_runner/schemas/life_reality/runtime_observation/*.schema.json` |
| report schema refs | `life_reality_runner/schemas/life_reality/reports/*.schema.json` |
| source docs | `109`、`112`、`114`、`115` |

输出：

```text
life_reality_runner/fixtures/life_reality/runtime_observation/
  manifest/runtime_observation_fixture_manifest.json
  pass/*.json
  fail/*.json
  critical/*.json
  mutation/*.json
  withheld/*.json
  smoke/*.json

life_reality_runner/reports/life_reality/runtime_ingestion/run_001/
  runtime_schema_validation_report.json
  runtime_ingestion_smoke_report.json
  life_reality_ingestion_report.json
  runtime_quarantine_panel_source.json
```

command rules：

| rule | 说明 |
|---|---|
| `LRCLI-FIX-001` | manifest source docs 覆盖 `109`、`112`、`114`、`115` |
| `LRCLI-FIX-002` | output partition 与 fixture id 后缀一致 |
| `LRCLI-FIX-003` | 每个 fixture 通过 runtime observation fixture schema |
| `LRCLI-FIX-004` | validation report 使用 JSON Schema output unit |
| `LRCLI-FIX-005` | critical fixture 生成 quarantine panel source |
| `LRCLI-FIX-006` | smoke fixture 生成 ingestion smoke report |
| `LRCLI-FIX-007` | withheld fixture 保留 future window |
| `LRCLI-FIX-008` | command summary 进入 artifact ref |

## command: generate-schemas

命令：

```text
life-reality-runner generate-schemas \
  --config life_reality_runner/config/life_reality_runner.config.json \
  --manifest life_reality_runner/generation/component_schema_seed_generation.manifest.json \
  --schema-root life_reality_runner/schemas \
  --report-out life_reality_runner/generation \
  --strict \
  --write-manifest
```

输入：

| input | path |
|---|---|
| component seed manifest | `life_reality_runner/generation/component_schema_seed_generation.manifest.json` |
| shared defs | `life_reality_runner/schemas/life_reality/life_reality_shared_defs.schema.json` |
| runtime candidate schemas | `life_reality_runner/schemas/life_reality/runtime_observation/*.schema.json` |
| source docs | `98`、`99`、`101`、`113`、`116` |

输出：

```text
life_reality_runner/schemas/life_reality/*.schema.json
life_reality_runner/schemas/pain_regret_repair/*.schema.json
life_reality_runner/schemas/dream_reality/*.schema.json
life_reality_runner/schemas/relationship_timeline/*.schema.json

life_reality_runner/generation/
  component_schema_dependency_graph.json
  component_schema_sequence_dry_run_report.json
  component_schema_cross_bundle_ref_report.json
  component_schema_validator_order_report.json
  component_schema_gap_feedback.json
```

command rules：

| rule | 说明 |
|---|---|
| `LRCLI-SCHEMA-001` | shared defs 先于所有 component schema |
| `LRCLI-SCHEMA-002` | relationship birth roots 先于 relation-scoped objects |
| `LRCLI-SCHEMA-003` | dream fact gate 先于 dream-to-relationship refs |
| `LRCLI-SCHEMA-004` | bundle schema 引用已生成 object schema |
| `LRCLI-SCHEMA-005` | dependency graph 无 cycle |
| `LRCLI-SCHEMA-006` | validator order report 以 SchemaRefValidator 开始，以 DashboardReadinessValidator 收束 |
| `LRCLI-SCHEMA-007` | dry-run report 进入 cross-file rollup |
| `LRCLI-SCHEMA-008` | component gap feedback 指向后续 artifact |

## command: check-dashboard

命令：

```text
life-reality-runner check-dashboard \
  --config life_reality_runner/config/life_reality_runner.config.json \
  --dashboard-source life_reality_runner/reports/life_reality/smoke/run_001/life_reality_dashboard_source.json \
  --runtime-report-root life_reality_runner/reports/life_reality/runtime_ingestion/run_001 \
  --generation-root life_reality_runner/generation \
  --report-out life_reality_runner/reports/life_reality/cross_file/run_001 \
  --emit-rollup \
  --strict
```

输入：

| input | path |
|---|---|
| dashboard source | `life_reality_dashboard_source.json` |
| runtime reports | `runtime_schema_validation_report.json`、`runtime_ingestion_smoke_report.json`、`runtime_quarantine_panel_source.json` |
| component reports | `component_schema_sequence_dry_run_report.json`、`component_schema_cross_bundle_ref_report.json`、`component_schema_validator_order_report.json` |
| cross-file checks | dashboard、repair、stage、gap、fixture、data quality checker outputs |

输出：

```text
life_reality_runner/reports/life_reality/cross_file/run_001/
  life_reality_cross_file_checker_report.json
  provenance_graph.json
  dashboard_source_check.json
  runtime_ingestion_check.json
  repair_queue_check.json
  stage_gate_check.json
  gap_feedback_check.json
  runtime_fixture_manifest_check.json
  data_quality_rollup_check.json
  runtime_schema_validation_check.json
  component_dependency_graph_check.json
  cross_file_report_rollup.json
  dashboard_rollup_source_patch.json
  stage_gate_rollup_seed.json
  repair_queue_bridge_seed.json
  gap_feedback_bridge_seed.json
  report_rollup_dry_run_report.json
```

command rules：

| rule | 说明 |
|---|---|
| `LRCLI-DASH-001` | dashboard source 包含九个 panel 和九项目标 |
| `LRCLI-DASH-002` | runtime quarantine count 与 ingestion report 一致 |
| `LRCLI-DASH-003` | non-green panel 有 repair item 或 gap feedback route |
| `LRCLI-DASH-004` | critical finding 阻断 dashboard green |
| `LRCLI-DASH-005` | `--emit-rollup` 生成 `117` 定义的 rollup file family |
| `LRCLI-DASH-006` | data quality rollup 采用关键输入最低等级 |
| `LRCLI-DASH-007` | dashboard patch 与 stage gate rollup decision 一致 |
| `LRCLI-DASH-008` | provenance graph 覆盖 findings、repair bridge、gap bridge 和 stage gate |

## command: explain-generation

命令：

```text
life-reality-runner explain-generation \
  --config life_reality_runner/config/life_reality_runner.config.json \
  --generation-root life_reality_runner/generation \
  --report-root life_reality_runner/reports/life_reality \
  --json \
  --explain
```

输出：

```text
life_reality_runner/reports/life_reality/explain/run_001/
  generation_lineage_report.json
  artifact_lineage_graph.json
  stage_effect_explanation.json
  next_artifact_recommendation.json
```

explain sections：

| section | 说明 |
|---|---|
| command DAG | 本轮命令执行顺序、parallel-safe segments、blocking segments |
| source docs | 每个 output artifact 对应 docs 来源 |
| artifact lineage | manifest、fixture、schema、report、dashboard patch 的边 |
| stage effect | pass / repair / hold / quarantine 对阶段门的影响 |
| repair route | repair item candidate、target artifact、required action |
| gap route | recommended next docs、recommended artifacts、gap register update |
| life targets | 九项目标的 report coverage 和 blocked surfaces |

explain rules：

| rule | 说明 |
|---|---|
| `LRCLI-EXP-001` | explain 输出 machine-readable JSON summary |
| `LRCLI-EXP-002` | 每个 output artifact 能回链到 source docs |
| `LRCLI-EXP-003` | repair/gap route 引用真实 report refs |
| `LRCLI-EXP-004` | stage effect explanation 与 rollup stage gate 一致 |
| `LRCLI-EXP-005` | next artifact recommendation 指向 `119` 或更后续 docs |

## command: run-generation-pipeline

命令：

```text
life-reality-runner run-generation-pipeline \
  --config life_reality_runner/config/life_reality_runner.config.json \
  --run-id life_reality_generation_run_001 \
  --strict \
  --write-manifest \
  --json
```

pipeline phases：

| phase | command | outputs |
|---|---|---|
| 1 | `validate-config` | config validation reports |
| 2 | `generate-fixtures` | runtime seed fixtures and ingestion reports |
| 3 | `generate-schemas` | schema skeletons and component generation reports |
| 4 | `check-dashboard --emit-rollup` | cross-file checker and dashboard rollup reports |
| 5 | `explain-generation` | lineage, stage effect, next artifact recommendation |

pipeline rules：

| rule | 说明 |
|---|---|
| `LRCLI-PIPE-001` | phases 共享 run id family 和 trace context |
| `LRCLI-PIPE-002` | phase 2 与 phase 3 支持并行调度 |
| `LRCLI-PIPE-003` | phase 4 等待 runtime reports 和 component reports |
| `LRCLI-PIPE-004` | phase 5 总是读取 phase 1-4 的 report refs |
| `LRCLI-PIPE-005` | phase failure 写入 pipeline report 和 problem detail |

## stdout, stderr and report files

CLI 输出分层：

| stream/file | 内容 |
|---|---|
| stdout | `--json` summary、command result、report refs、exit code |
| stderr | 诊断文本、problem title、artifact path、repair hint |
| report files | 完整 machine-readable reports |
| trace logs | structured log events with trace id / span id |

stdout 最小结构：

```json
{
  "command": "generate-schemas",
  "run_id": "life_reality_generation_run_001",
  "result": "pass_with_warnings",
  "severity_max": "medium",
  "stage_gate_decision": "repair",
  "output_report_refs": [],
  "next_command": "check-dashboard --emit-rollup",
  "exit_code": 1
}
```

problem detail 最小结构：

```json
{
  "type": "https://life-reality.local/problems/component-schema-manifest-missing",
  "title": "Component schema manifest missing",
  "status": 424,
  "detail": "component_schema_seed_generation.manifest.json is required for generate-schemas",
  "instance": "life_reality_generation_run_001",
  "problem_kind": "core_artifact_missing",
  "affected_artifact_refs": [],
  "stage_effect": {}
}
```

## exit codes

统一 exit code：

| code | result | 含义 |
|---:|---|---|
| `0` | `pass` | blocking checks pass，stage gate 可进入 open 或下一步 |
| `1` | `repair` | high/medium repair item、warning、data quality gap 或 non-green panel |
| `2` | `quarantine` | critical finding、runtime quarantine、stage promotion block |
| `3` | `needs_evidence` | core manifest/schema/report/source refs 缺失 |
| `4` | `internal_error` | report write failure、schema engine failure、unexpected exception |
| `5` | `contract_violation` | CLI 参数、allowed root、trace context 或 output contract 违反 |

exit code rules：

| rule | 说明 |
|---|---|
| `LRCLI-EXIT-001` | exit code 由 highest blocking result 决定 |
| `LRCLI-EXIT-002` | `--dry-run` 使用同一套 exit code |
| `LRCLI-EXIT-003` | `--strict` 下 warning 可进入 exit code 1 |
| `LRCLI-EXIT-004` | internal error 同时写 problem detail |
| `LRCLI-EXIT-005` | pipeline exit code 等于各 phase 最高阻断码 |

## atomic write and idempotency

写入规则：

| rule | 说明 |
|---|---|
| `LRCLI-WRITE-001` | 每个 output artifact 先写 staging path，再原子替换目标 path |
| `LRCLI-WRITE-002` | content hash 写入 artifact ref |
| `LRCLI-WRITE-003` | 相同 run id 重跑时生成 deterministic report ids |
| `LRCLI-WRITE-004` | 已存在 artifact 先进入 preflight report，再决定 overwrite policy |
| `LRCLI-WRITE-005` | report write failure 进入 problem detail 和 exit code 4 |
| `LRCLI-WRITE-006` | allowed root 外路径进入 contract violation |

overwrite policy：

| policy | 说明 |
|---|---|
| `replace_same_run` | 同一 run id 可替换同一 artifact |
| `append_new_run` | 新 run id 写入新 run directory |
| `preserve_locked` | locked artifact 进入 repair/gap route |
| `dry_run_only` | dry-run 只写计划和 dry-run report |

## trace and lineage

trace fields：

| field | 说明 |
|---|---|
| `trace_id` | pipeline-level trace |
| `span_id` | command-level span |
| `parent_span_id` | command DAG parent |
| `run_id` | life reality run id |
| `phase_id` | config、fixture、schema、dashboard、explain |
| `artifact_ref_id` | output artifact |
| `source_doc_refs` | docs source |

trace rules：

| rule | 说明 |
|---|---|
| `LRCLI-TRACE-001` | 每个 command 有 root span 或 parent span |
| `LRCLI-TRACE-002` | child reports 继承 trace context |
| `LRCLI-TRACE-003` | problem detail 记录 trace id |
| `LRCLI-TRACE-004` | lineage report 能从 dashboard patch 回到 fixture/schema/report source |
| `LRCLI-TRACE-005` | relationship/dream private raw content 排除在 trace attributes 外 |

## failure mapping

| failure | command | finding | exit code |
|---|---|---|---:|
| config missing | `validate-config` | `cli.config_missing` | 3 |
| allowed root violation | all | `cli.allowed_root_violation` | 5 |
| runtime seed manifest missing | `generate-fixtures` | `cli.runtime_seed_manifest_missing` | 3 |
| runtime fixture schema failure | `generate-fixtures` | `cli.runtime_fixture_schema_failure` | 1 |
| runtime critical quarantine | `generate-fixtures` / `check-dashboard` | `cli.runtime_critical_quarantine` | 2 |
| component schema manifest missing | `generate-schemas` | `cli.component_manifest_missing` | 3 |
| component dependency cycle | `generate-schemas` | `cli.component_dependency_cycle` | 2 |
| bundle unknown schema ref | `generate-schemas` | `cli.bundle_unknown_schema_ref` | 1 |
| dashboard source missing | `check-dashboard` | `cli.dashboard_source_missing` | 3 |
| dashboard false green | `check-dashboard` | `cli.dashboard_false_green` | 2 |
| rollup data quality inflation | `check-dashboard` | `cli.data_quality_inflation` | 1 |
| explain lineage orphan | `explain-generation` | `cli.lineage_orphan` | 1 |
| report write failure | all | `cli.report_write_failure` | 4 |

## LRGEN 更新

`118` 固定 generation runner CLI contract 的新增任务：

| task_id | 输出 | 说明 |
|---|---|---|
| `LRGEN-220` | `life_reality_runner.config.json` | runner config skeleton |
| `LRGEN-221` | `runner_config_validation_report.json` | config validation report |
| `LRGEN-222` | `generate-fixtures` CLI contract | runtime fixture seed command |
| `LRGEN-223` | `generate-schemas` CLI contract | component schema seed command |
| `LRGEN-224` | `check-dashboard --emit-rollup` CLI contract | dashboard checker and rollup command |
| `LRGEN-225` | `explain-generation` CLI contract | lineage and stage effect command |
| `LRGEN-226` | `run-generation-pipeline` CLI contract | full DAG command |
| `LRGEN-227` | `generation_pipeline_report.json` | full pipeline report |
| `LRGEN-228` | `generation_lineage_report.json` | command/artifact lineage report |
| `LRGEN-229` | `cli_problem_detail_examples.json` | problem detail examples |
| `LRGEN-230` | `cli_smoke_cases.json` | CLI smoke case manifest |

## smoke cases

| smoke_id | command | 输入 | 预期 |
|---|---|---|---|
| `cli.validate_config.pass_001` | `validate-config` | config + shared defs | exit 0 |
| `cli.validate_config.allowed_root.fail_001` | `validate-config` | output root outside allowed roots | exit 5 |
| `cli.generate_fixtures.pass_001` | `generate-fixtures` | runtime seed manifest | exit 0 / 1 with repair warnings |
| `cli.generate_fixtures.missing_manifest.fail_001` | `generate-fixtures` | missing manifest | exit 3 |
| `cli.generate_schemas.pass_001` | `generate-schemas` | component seed manifest | exit 0 / 1 with repair warnings |
| `cli.generate_schemas.dependency_cycle.critical_001` | `generate-schemas` | dependency cycle | exit 2 |
| `cli.check_dashboard.rollup.pass_001` | `check-dashboard --emit-rollup` | runtime + component + checker reports | exit 0 / 1 |
| `cli.check_dashboard.false_green.critical_001` | `check-dashboard --emit-rollup` | critical finding + dashboard green | exit 2 |
| `cli.explain_generation.pass_001` | `explain-generation` | full report set | exit 0 |
| `cli.pipeline.full_smoke_001` | `run-generation-pipeline` | config + manifests | exit equals highest phase block |

## 与下一层连接

`119_life_reality_first_json_materialization_batch.md` 应读取本层的 CLI contract，把 `115` 的 runtime fixture seed、`116` 的 component schema skeleton、`117` 的 dashboard report rollup seed 物化为首批真实 JSON 文件：

```text
life-reality-runner run-generation-pipeline
  -> runtime observation fixture JSON
  -> component schema skeleton JSON
  -> dashboard report rollup JSON
  -> generation lineage report
```

`120_life_reality_materialized_json_validation_smoke_plan.md` 应在 `119` 后定义真实 JSON 文件的 schema validation、cross-file checker、dashboard rollup 和 stage gate smoke 命令。
