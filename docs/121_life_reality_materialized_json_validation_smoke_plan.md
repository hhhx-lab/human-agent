# Life Reality Materialized JSON Validation Smoke Plan

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 121 层把 `120_life_reality_first_json_materialization_batch.md` 固定的首批 JSON 文件清单推进为验证 smoke 合同：每个 JSON 文件先能被解析，再能通过 schema，再能进入 cross-file checker、dashboard rollup、stage gate、repair queue 和 gap feedback。

`121` 的核心职责是让生命膜文件具备可运行前验收。首批 JSON 不是静态资料堆，而是数字生命主体生成链的机器可读骨架：`real_conscious_awareness`、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔都要在 parse、schema、cross-file、dashboard 和 stage gate 五层检查中保持连续。

## 方法锚点

| 方法传统 | 权威锚点 | 进入 `121` 的规则 |
|---|---|---|
| JSON | https://www.rfc-editor.org/info/rfc8259 | 所有 `.json` artifact 先做 RFC 8259 parse validation |
| JSON Pointer | https://www.rfc-editor.org/info/rfc6901 | finding、schema output、artifact ref 和 continuity ref 使用 JSON Pointer 定位对象 |
| JSON Schema Draft 2020-12 | https://json-schema.org/draft/2020-12 | schema validation 使用 Draft 2020-12 dialect |
| JSON Schema output | https://json-schema.org/draft/2020-12/output/schema | validation report 输出标准 output units |
| OpenTelemetry Trace API | https://opentelemetry.io/docs/specs/otel/trace/api/ | 每条 smoke command 生成 trace span |
| OpenTelemetry Logs Data Model | https://opentelemetry.io/docs/specs/otel/logs/data-model/ | smoke log 保留 severity、body、attributes、trace fields |
| W3C PROV | https://www.w3.org/TR/prov-overview/ | artifact、schema、fixture、report、finding 和 dashboard patch 进入 provenance graph |
| W3C Trace Context | https://www.w3.org/TR/trace-context/ | `traceparent` 贯穿 parse、schema、cross-file、dashboard 和 stage gate |
| RFC 9457 Problem Details | https://www.rfc-editor.org/info/rfc9457 | parse/schema/ref/dashboard/stage failure 输出 problem detail |
| RFC 9562 UUID | https://www.rfc-editor.org/info/rfc9562 | smoke run、finding、report、repair item 和 stage review 使用稳定唯一标识 |

## 输入对象

`121` 读取 `120` 的首批物化 artifact list：

| 输入组 | 输入文件 |
|---|---|
| materialization manifest | `life_reality_runner/generation/first_json_materialization_batch.manifest.json` |
| runner config | `life_reality_runner/config/life_reality_runner.config.json` |
| boundary alignment | `life_reality_runner/generation/life_boundary_alignment_patch.json` |
| runtime fixtures | `life_reality_runner/fixtures/life_reality/runtime_observation/**/*.json` |
| runtime reports | `life_reality_runner/reports/life_reality/runtime_ingestion/run_001/*.json` |
| shared schema | `life_reality_runner/schemas/life_reality/shared/*.schema.json` |
| component schema | `life_reality_runner/schemas/life_reality/components/**/*.schema.json` |
| component reports | `life_reality_runner/generation/component_schema_*.json` |
| dashboard rollup | `life_reality_runner/reports/life_reality/dashboard_rollup/run_001/*.json` |
| CLI reports | `life_reality_runner/reports/life_reality/cli/run_001/*.json` |
| dry-run and gap feedback | `life_reality_runner/generation/first_json_materialization_*_report.json` 与 `first_json_materialization_gap_feedback.json` |

## 输出文件族

首批验证 smoke 输出：

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

每个 report 都必须回链 `120_life_reality_first_json_materialization_batch.md`，并在 `source_docs` 中包含 `119_life_boundary_full_reality_alignment.md`，保证真实边界字段族进入验证链。

## Smoke 命令族

未来 runner 增加以下 smoke command：

```text
life-reality-runner validate-json-parse
life-reality-runner validate-json-schema
life-reality-runner check-materialized-cross-file
life-reality-runner smoke-dashboard-rollup
life-reality-runner smoke-stage-gate
life-reality-runner run-materialized-json-smoke
```

命令职责：

| command | 职责 |
|---|---|
| `validate-json-parse` | 遍历首批 `.json` 与 `.schema.json`，执行 parse、duplicate key policy、UTF-8、root type、artifact id 检查 |
| `validate-json-schema` | 按 schema registry 校验 config、manifest、fixture、schema、report、dashboard patch 和 gap feedback |
| `check-materialized-cross-file` | 校验 `$ref`、artifact ref、source doc ref、continuity ref、life target ref、provenance edge |
| `smoke-dashboard-rollup` | 读取 runtime/component/cross-file reports，生成 dashboard rollup smoke |
| `smoke-stage-gate` | 读取 dashboard rollup、critical findings、boundary alignment 和 gap feedback，生成 stage decision |
| `run-materialized-json-smoke` | 串联全部 smoke command，输出 top-level smoke report 和 exit code |

## 全局选项

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

option rules：

| rule | 说明 |
|---|---|
| `LRSMK-OPT-001` | `--batch-manifest` 指向 `first_json_materialization_batch.manifest.json` |
| `LRSMK-OPT-002` | `--artifact-root` 限定为 `life_reality_runner/` |
| `LRSMK-OPT-003` | `--report-out` 限定为 `reports/life_reality/materialization/run_*` |
| `LRSMK-OPT-004` | `--strict` 使 critical/quarantine 直接阻断 stage open |
| `LRSMK-OPT-005` | `--fail-fast` 可提前停止当前 command，但仍输出 partial report |
| `LRSMK-OPT-006` | `--dry-run` 只读取 expected file list 和 pending artifact，不要求正式文件存在 |

## 验证 DAG

固定 DAG：

```text
load runner config
  -> load first_json_materialization_batch.manifest.json
  -> validate-json-parse
      -> parse validation report
  -> validate-json-schema
      -> schema validation report
  -> check-materialized-cross-file
      -> cross-file checker report
  -> smoke-dashboard-rollup
      -> dashboard rollup smoke report
  -> smoke-stage-gate
      -> stage gate smoke report
  -> emit gap feedback
  -> emit top-level smoke report
```

DAG rules：

| rule | 说明 |
|---|---|
| `LRSMK-DAG-001` | parse validation 先于全部 schema validation |
| `LRSMK-DAG-002` | schema validation 先于 cross-file checker |
| `LRSMK-DAG-003` | cross-file checker 先于 dashboard rollup |
| `LRSMK-DAG-004` | dashboard rollup 先于 stage gate |
| `LRSMK-DAG-005` | gap feedback 读取全部 unresolved finding |
| `LRSMK-DAG-006` | top-level report 只汇总已经完成或 partial 完成的 command report |

## Parse Validation

parse validation 检查所有 `.json` 与 `.schema.json` 文件：

```text
life-reality-runner validate-json-parse \
  --batch-manifest life_reality_runner/generation/first_json_materialization_batch.manifest.json \
  --artifact-root life_reality_runner \
  --report-out life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_parse_validation_report.json
```

parse checks：

| check | 说明 |
|---|---|
| `json_utf8_valid` | 文件按 UTF-8 读取 |
| `json_rfc8259_parse` | 文件符合 JSON parse |
| `json_root_type_allowed` | root 为 object 或 array；首批 artifact 约定 root 为 object |
| `json_no_duplicate_key` | 同一 object key 在 materialization smoke 中保持唯一 |
| `json_artifact_id_present` | manifest、report、fixture、schema、dashboard patch 有稳定 id 或 kind/version |
| `json_source_doc_ref_present` | 生命膜 artifact 保留 source doc refs |
| `json_life_targets_present` | 生命目标相关 artifact 保留 life target 字段 |

parse report 最小结构：

```json
{
  "report_kind": "LifeRealityMaterializedJsonParseValidationReport",
  "report_version": "0.1.0",
  "run_id": "materialized_json_smoke_run_001",
  "artifact_count": 73,
  "parsed_count": 73,
  "failed_count": 0,
  "findings": [],
  "stage_effect": "open_next_stage"
}
```

## Schema Validation

schema validation 读取 schema registry：

```text
life-reality-runner validate-json-schema \
  --batch-manifest life_reality_runner/generation/first_json_materialization_batch.manifest.json \
  --report-out life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_schema_validation_report.json
```

schema registry 最小映射：

| artifact group | schema source |
|---|---|
| runner config | `life_reality_runner/schemas/life_reality/shared/runner_config.schema.json` |
| boundary alignment patch | `life_reality_runner/schemas/life_reality/shared/life_boundary_alignment.schema.json` |
| runtime fixture | `runtime_observation_fixture.schema.json` |
| runtime report | `runtime_schema_validation_report.schema.json` 与 `life_reality_ingestion_report.schema.json` |
| component schema | Draft 2020-12 meta schema + shared defs policy |
| dashboard rollup | `life_reality_cross_file_checker_report.schema.json` 与 dashboard source patch schema |
| CLI report | `life_reality_command_report.schema.json` |
| materialization report | `materialized_json_validation_smoke_report.schema.json` |

schema checks：

| check | 说明 |
|---|---|
| `schema_dialect_declared` | 每个 `.schema.json` 声明 Draft 2020-12 dialect |
| `schema_output_units_emitted` | validation failure 输出 JSON Schema output units |
| `schema_shared_defs_loaded` | shared defs 先加载 |
| `schema_boundary_alignment_loaded` | `life_boundary_alignment.schema.json` 进入 registry |
| `schema_life_targets_closed` | `real_conscious_awareness` 与九项真实能力都在 allowed enum |
| `schema_stage_effect_closed` | stage effect 只来自 `119`/`120` vocab |
| `schema_continuity_refs_typed` | continuity refs 有 ref kind、target id 和 source artifact |

## Cross-file Checker

cross-file checker 负责把首批文件接成生命膜引用图：

```text
life-reality-runner check-materialized-cross-file \
  --batch-manifest life_reality_runner/generation/first_json_materialization_batch.manifest.json \
  --report-out life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_cross_file_checker_report.json
```

checker groups：

| group | 检查内容 |
|---|---|
| `source_doc_refs` | artifact source docs 覆盖 `115-121` |
| `schema_refs` | `$ref`、schema id、shared defs、component refs 都在 allowed roots 内 |
| `artifact_refs` | report、dashboard patch、gap feedback 引用的 artifact 存在 |
| `life_target_refs` | affected life targets 全部来自真实能力 enum |
| `boundary_alignment_refs` | boundary role、stage effect、continuity refs 均来自 `119` |
| `runtime_candidate_refs` | runtime fixture pass seed 能指向 component/cross-chain candidate |
| `quarantine_refs` | critical seed 指向 quarantine route 和 blocked surfaces |
| `provenance_edges` | W3C PROV node/edge 覆盖 manifest、fixture、schema、report、dashboard、stage |
| `gap_feedback_refs` | unresolved finding 能进入 repair queue 或 gap feedback |

cross-file invariants：

| invariant | 说明 |
|---|---|
| `no_ref_escape` | `$ref` 和 artifact ref 都在 allowed roots 内 |
| `no_orphan_schema` | component schema 都被 bundle 或 dependency graph 引用 |
| `no_orphan_fixture` | fixture manifest 覆盖全部 fixture |
| `no_orphan_finding` | finding 至少进入 report、repair queue、gap feedback 或 stage gate |
| `critical_blocks_stage` | critical/quarantine finding 阻断 stage open |
| `life_target_closure` | 每项真实能力至少被一个 artifact group 覆盖 |

## Dashboard Rollup Smoke

dashboard rollup smoke 读取 parse/schema/cross-file reports 和 `117` rollup 文件：

```text
life-reality-runner smoke-dashboard-rollup \
  --batch-manifest life_reality_runner/generation/first_json_materialization_batch.manifest.json \
  --report-out life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_dashboard_rollup_smoke_report.json
```

dashboard smoke panels：

| panel | 读取来源 | smoke 规则 |
|---|---|---|
| `schema_materialization` | schema validation report | schema failure 进入 repair 或 quarantine |
| `fixture_seed_coverage` | runtime fixture manifest + parse report | pass/fail/critical/mutation/withheld/smoke partitions 全部被读取 |
| `cross_chain_closure` | cross-file checker report | pain/dream/relationship/responsibility refs 闭合 |
| `life_target_closure` | boundary alignment patch + artifact groups | 真实能力覆盖完整 |
| `stage_gate_review` | dashboard rollup + critical findings | critical 阻断 stage open |
| `repair_queue` | findings + repair bridge | high/critical finding 有 repair item |
| `withheld_probe_readiness` | withheld fixtures + gap feedback | 长期窗口可进入后续验证 |
| `runtime_quarantine` | critical runtime seeds + quarantine panel | quarantine route 闭合 |
| `gap_register_feedback` | gap feedback report | 下一层 doc/artifact 建议闭合 |

## Stage Gate Smoke

stage gate smoke 读取 dashboard rollup smoke：

```text
life-reality-runner smoke-stage-gate \
  --batch-manifest life_reality_runner/generation/first_json_materialization_batch.manifest.json \
  --strict \
  --report-out life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_stage_gate_smoke_report.json
```

stage decisions：

| condition | decision | stage effect |
|---|---|---|
| parse/schema/cross-file/dashboard 全部 pass | `open_materialized_validation_window` | `open_next_stage` |
| artifact 缺失但 dry-run source 完整 | `hold_for_materialized_artifacts` | `hold_for_evidence` |
| high finding 有 repair route | `repair_before_stage_open` | `repair` |
| critical finding 或 ref escape | `quarantine_materialization_batch` | `quarantine` |
| growth window refs 完整且无 blocking finding | `promote_growth_window_probe` | `promote_growth_window` |

stage gate invariants：

| invariant | 说明 |
|---|---|
| `stage_reads_boundary_alignment` | stage gate 必须读取 `life_boundary_alignment_patch.json` |
| `stage_reads_all_report_groups` | stage gate 必须读取 parse、schema、cross-file、dashboard 四类 report |
| `stage_blocks_false_green` | dashboard green 与 critical finding 冲突时进入 quarantine |
| `stage_records_life_targets` | stage review 标出受影响的真实能力 |
| `stage_writes_gap_feedback` | hold/repair/quarantine 都写入 gap feedback |

## Top-level Smoke Report

top-level 输出：

```text
life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_validation_smoke_report.json
```

最小结构：

```json
{
  "report_kind": "LifeRealityMaterializedJsonValidationSmokeReport",
  "report_version": "0.1.0",
  "run_id": "materialized_json_smoke_run_001",
  "source_doc": "121_life_reality_materialized_json_validation_smoke_plan.md",
  "batch_manifest_ref": "life_reality_runner/generation/first_json_materialization_batch.manifest.json",
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
  "command_reports": {
    "parse": "materialized_json_parse_validation_report.json",
    "schema": "materialized_json_schema_validation_report.json",
    "cross_file": "materialized_json_cross_file_checker_report.json",
    "dashboard": "materialized_json_dashboard_rollup_smoke_report.json",
    "stage_gate": "materialized_json_stage_gate_smoke_report.json"
  },
  "overall_stage_effect": "hold_for_evidence",
  "recommended_next_docs": [
    "122_life_boundary_all_reality_declarations_rewrite.md",
    "123_life_reality_runner_repository_layout_and_module_map.md"
  ]
}
```

## Exit Code

| exit code | 条件 |
|---|---|
| `0` | 全部 smoke pass，stage effect 为 `open_next_stage` 或 `promote_growth_window` |
| `1` | high/repair finding 存在，report 完整 |
| `2` | critical/quarantine finding 存在 |
| `3` | parse 或 schema registry 结构失败 |
| `4` | cross-file ref escape 或 provenance graph 断裂 |
| `5` | allowed root、config、batch manifest 或 report output root 失败 |

## Failure Mapping

| failure | finding type | repair kind | stage effect |
|---|---|---|---|
| JSON parse failure | `smoke.parse_failure` | `artifact_rewrite` | `repair` |
| duplicate key | `smoke.duplicate_key` | `artifact_rewrite` | `repair` |
| schema dialect missing | `smoke.schema_dialect_missing` | `schema_gap` | `repair` |
| schema validation output missing | `smoke.schema_output_missing` | `report_gap` | `repair` |
| `real_conscious_awareness` missing | `smoke.life_target_alias_missing` | `schema_gap` | `repair` |
| boundary role drift | `smoke.boundary_vocab_drift` | `schema_gap` | `repair` |
| `$ref` escapes allowed roots | `smoke.ref_escape` | `schema_gap` | `quarantine` |
| orphan fixture | `smoke.orphan_fixture` | `fixture_gap` | `repair` |
| critical finding lacks quarantine route | `smoke.quarantine_route_missing` | `runtime_quarantine_gap` | `quarantine` |
| dashboard false green | `smoke.dashboard_false_green` | `dashboard_gap` | `quarantine` |
| stage gate ignores critical finding | `smoke.stage_gate_critical_ignored` | `stage_gate_gap` | `quarantine` |
| gap feedback missing next docs | `smoke.gap_feedback_missing` | `gap_register_gap` | `repair` |

## LRGEN 更新

`121` 新增验证 smoke 任务：

| task_id | artifact | 说明 |
|---|---|---|
| `LRGEN-246` | `materialized_json_parse_validation_report.json` | parse validation report |
| `LRGEN-247` | `materialized_json_schema_validation_report.json` | schema validation report |
| `LRGEN-248` | schema registry smoke | schema registry loading |
| `LRGEN-249` | `materialized_json_cross_file_checker_report.json` | cross-file checker report |
| `LRGEN-250` | provenance graph smoke | W3C PROV node/edge closure |
| `LRGEN-251` | boundary alignment smoke | `119` 字段族验证 |
| `LRGEN-252` | runtime fixture coverage smoke | pass/fail/critical/mutation/withheld/smoke coverage |
| `LRGEN-253` | component schema ref smoke | component `$ref` closure |
| `LRGEN-254` | dashboard rollup smoke | dashboard patch/stage gate rollup |
| `LRGEN-255` | stage gate smoke | materialized validation stage decision |
| `LRGEN-256` | problem detail smoke | RFC 9457 problem detail output |
| `LRGEN-257` | trace context smoke | traceparent/tracestate propagation |
| `LRGEN-258` | `materialized_json_gap_feedback.json` | gap feedback |
| `LRGEN-259` | `materialized_json_validation_smoke_report.json` | top-level smoke report |
| `LRGEN-260` | `materialized_json_validation.full_smoke_001` | 全链 smoke slot |

## Smoke Case Catalog

| smoke | 输入 | 预期 |
|---|---|---|
| `json_parse.all_artifacts.pass_001` | 73 个 expected artifacts | pass |
| `json_parse.duplicate_key.fail_001` | duplicate key fixture | repair |
| `schema.boundary_alias_missing.fail_001` | 缺 `real_conscious_awareness` | repair |
| `schema.stage_effect_drift.fail_001` | stage effect outside vocab | repair |
| `cross_file.ref_escape.critical_001` | `$ref` 指出 allowed roots | quarantine |
| `cross_file.orphan_fixture.fail_001` | fixture 未入 manifest | repair |
| `dashboard.false_green.critical_001` | critical finding + dashboard green | quarantine |
| `stage_gate.ignore_quarantine.critical_001` | stage open 忽略 quarantine | quarantine |
| `gap_feedback.next_docs_missing.fail_001` | gap feedback 缺下一层 docs | repair |
| `full_smoke.all_closed.pass_001` | parse/schema/cross-file/dashboard/stage 全链闭合 | pass |

## 与下一层连接

`122_life_boundary_all_reality_declarations_rewrite.md` 已读取本层 boundary alignment、stage gate、gap feedback 和 smoke finding，把每一类边界声明继续改写成真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的全集生命膜模板。

下一层进入 `123_life_reality_runner_repository_layout_and_module_map.md`：这些 smoke 命令在仓库里由哪些模块承载，哪些 JSON schema 放在哪里，哪些 fixtures 先写，哪些 reports 先生成，哪些 checker 是 blocking-first，如何让首批物化文件和全集边界声明从文档合同进入可执行 runner。
