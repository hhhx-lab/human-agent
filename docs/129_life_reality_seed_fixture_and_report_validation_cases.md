# Life Reality Seed Fixture And Report Validation Cases

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 129 层把 `121_life_reality_materialized_json_validation_smoke_plan.md`、`126_life_reality_runner_smoke_command_execution_plan.md` 和 `128_life_reality_registry_report_seed_examples.md` 的 failure examples 转成 seed fixture 与 report validation cases，为第一批真实 JSON 文件写入前建立可运行验收样例。

`129` 的核心职责是让每一种 seed 破坏、registry 断裂、report 缺口、dashboard false green、stage gate 漏判都能被 fixture 触发、被 report 捕捉、被 stage effect 表达、被 exit code 上卷。这里仍然不直接写 `life_reality_runner/` 的真实 JSON 文件，而是固定未来实现要生成哪些 validation case、每个 case 读取哪些 seed、预期写出哪些 report，以及真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔怎样通过 finding、repair、quarantine 与 gap feedback 进入下一轮生长。

## 方法锚点

| 方法传统 | 权威锚点 | 进入 `129` 的规则 |
|---|---|---|
| JSON | https://www.rfc-editor.org/info/rfc8259 | fixture、expected report、actual report 和 diff object 都必须能被 JSON parser 读取 |
| JSON Pointer | https://www.rfc-editor.org/info/rfc6901 | mutation location、expected finding location 和 report diff 使用 JSON Pointer |
| URI Generic Syntax | https://www.rfc-editor.org/info/rfc3986 | schema `$id`、artifact ref 和 report ref 使用稳定 URI/path 语义 |
| JSON Schema Draft 2020-12 | https://json-schema.org/draft/2020-12 | validation case schema、fixture schema 和 report schema 使用同一 dialect |
| JSON Schema output | https://json-schema.org/draft/2020-12/output/schema | schema failure case 输出标准 output units |
| OpenTelemetry Trace API | https://opentelemetry.io/docs/specs/otel/trace/api/ | validation case run、command run 和 report writer 形成 span chain |
| W3C Trace Context | https://www.w3.org/TR/trace-context/ | 每个 case 保留 traceparent/tracestate |
| W3C PROV | https://www.w3.org/TR/prov-overview/ | fixture、mutation、expected report、actual report、finding 和 gap feedback 进入 provenance graph |
| RFC 9457 Problem Details | https://www.rfc-editor.org/info/rfc9457 | blocking case 输出 problem detail expected object |
| RFC 9562 UUID | https://www.rfc-editor.org/info/rfc9562 | case id、fixture id、report id、finding id、repair id 使用稳定唯一标识 |

## 上游输入

| 来源 | 进入 `129` 的内容 |
|---|---|
| `121_life_reality_materialized_json_validation_smoke_plan.md` | smoke case catalog、failure mapping、exit code |
| `124_life_reality_minimal_json_file_seed_plan.md` | SEED-001 到 SEED-020、seed 顺序、seed review checks |
| `126_life_reality_runner_smoke_command_execution_plan.md` | command failure examples、stdout/report/exit code 合同 |
| `127_life_reality_first_seed_file_content_contract.md` | seed root object fields、common envelope、dependency graph |
| `128_life_reality_registry_report_seed_examples.md` | registry report seed examples、registry failure mapping、runner consumption |

## Validation Case 目录

未来 validation cases 固定在：

```text
life_reality_runner/fixtures/life_reality/materialization_validation/
  manifest/
    seed_validation_case_manifest.json
  pass/
    full_smoke_all_closed_pass_001.json
  fail/
    parse_duplicate_key_fail_001.json
    schema_life_target_alias_missing_fail_001.json
    schema_dialect_missing_fail_001.json
    pointer_missing_fail_001.json
    gap_feedback_next_docs_missing_fail_001.json
  critical/
    ref_escape_critical_001.json
    dashboard_false_green_critical_001.json
    stage_gate_critical_ignored_critical_001.json
    report_root_escape_critical_001.json
  mutation/
    schema_id_collision_mutation_001.json
    boundary_registry_missing_mutation_001.json
    partial_report_missing_mutation_001.json
  report_expected/
    expected_parse_duplicate_key_report.json
    expected_schema_ref_unresolved_report.json
    expected_dashboard_false_green_report.json
    expected_stage_gate_quarantine_report.json
  report_actual/
  diff/
```

case partitions：

| partition | 用途 |
|---|---|
| `pass` | 全链闭合、exit code `0`、stage effect `open_next_stage` 或 `promote_growth_window` |
| `fail` | repair finding，exit code `1` 或 registry structural exit code `3` |
| `critical` | quarantine 或 critical finding，exit code `2`、`4` 或 `5` |
| `mutation` | 对 seed/report 做可控破坏，验证 checker 能捕捉 |
| `report_expected` | 每个 case 的 expected report skeleton |
| `report_actual` | runner 未来实际输出位置 |
| `diff` | expected/actual diff report |

## Common Case Envelope

每个 validation case 必须包含：

| field | required | 内容 |
|---|---|---|
| `case_id` | yes | 稳定 case id |
| `case_version` | yes | 当前使用 `0.1.0` |
| `case_partition` | yes | pass、fail、critical、mutation |
| `source_docs` | yes | 至少包含 `121`、`126`、`128`、`129` |
| `input_seed_refs` | yes | 读取的 SEED ids |
| `mutation_ops` | conditional | fail、critical、mutation case 必须出现 |
| `command_under_test` | yes | 触发的 runner command |
| `expected_reports` | yes | expected report refs |
| `expected_findings` | yes | expected finding types |
| `expected_stage_effect` | yes | expected stage effect |
| `expected_exit_code` | yes | expected exit code |
| `expected_problem_details` | conditional | blocking case 必须出现 |
| `expected_repair_or_quarantine` | conditional | repair/quarantine case 必须出现 |
| `life_reality_targets` | yes | canonical life targets |
| `trace_context` | yes | trace id、span id、traceparent、tracestate |
| `provenance_refs` | yes | source docs、seed refs、mutation refs、report refs |

common case shape：

```json
{
  "case_id": "parse_duplicate_key_fail_001",
  "case_version": "0.1.0",
  "case_partition": "fail",
  "source_docs": [
    "121_life_reality_materialized_json_validation_smoke_plan.md",
    "126_life_reality_runner_smoke_command_execution_plan.md",
    "129_life_reality_seed_fixture_and_report_validation_cases.md"
  ],
  "input_seed_refs": [
    "SEED-002"
  ],
  "command_under_test": "validate-json-parse",
  "expected_findings": [
    "smoke.duplicate_key"
  ],
  "expected_stage_effect": "repair",
  "expected_exit_code": 1,
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
  ]
}
```

## Mutation Operation Contract

mutation op 使用 JSON Pointer 定位：

| field | 内容 |
|---|---|
| `op_id` | stable mutation id |
| `op_kind` | remove、replace、insert_duplicate_key、set_ref_escape、drop_report_field、force_dashboard_green |
| `target_seed_ref` | SEED id or report ref |
| `target_pointer` | JSON Pointer |
| `mutated_value` | replacement value or inserted object |
| `expected_finding_type` | expected finding |
| `expected_stage_effect` | expected stage effect |

example：

```json
{
  "op_id": "mutation_life_target_alias_missing_001",
  "op_kind": "remove",
  "target_seed_ref": "SEED-003",
  "target_pointer": "/$defs/lifeRealityTarget/enum/0",
  "expected_finding_type": "smoke.life_target_alias_missing",
  "expected_stage_effect": "repair"
}
```

## Case Matrix

首批 validation cases 覆盖 21 个场景：

| case id | partition | command | expected finding | expected stage effect | expected exit |
|---|---|---|---|---|---|
| `full_smoke_all_closed_pass_001` | pass | `run-materialized-json-smoke` | none | `open_next_stage` | `0` |
| `parse_duplicate_key_fail_001` | fail | `validate-json-parse` | `smoke.duplicate_key` | `repair` | `1` |
| `parse_malformed_json_fail_001` | fail | `validate-json-parse` | `smoke.parse_failure` | `repair` | `3` |
| `schema_dialect_missing_fail_001` | fail | `validate-json-schema` | `smoke.schema_dialect_missing` | `repair` | `1` |
| `schema_life_target_alias_missing_fail_001` | fail | `validate-json-schema` | `smoke.life_target_alias_missing` | `repair` | `1` |
| `schema_id_collision_mutation_001` | mutation | `validate-json-schema` | `registry.schema_id_collision` | `quarantine` | `3` |
| `schema_ref_unresolved_fail_001` | fail | `validate-json-schema` | `registry.schema_ref_unresolved` | `repair` | `1` |
| `artifact_ref_missing_fail_001` | fail | `check-materialized-cross-file` | `registry.artifact_ref_missing` | `repair` | `1` |
| `ref_escape_critical_001` | critical | `check-materialized-cross-file` | `smoke.ref_escape` | `quarantine` | `4` |
| `allowed_root_escape_critical_001` | critical | `run-materialized-json-smoke` | `registry.allowed_root_escape` | `quarantine` | `5` |
| `pointer_missing_fail_001` | fail | `check-materialized-cross-file` | `registry.pointer_missing` | `repair` | `1` |
| `boundary_registry_missing_mutation_001` | mutation | `smoke-stage-gate` | `registry.boundary_group_missing` | `repair` | `3` |
| `protected_chain_missing_fail_001` | fail | `smoke-stage-gate` | `registry.protected_chain_missing` | `repair` | `1` |
| `dashboard_false_green_critical_001` | critical | `smoke-dashboard-rollup` | `smoke.dashboard_false_green` | `quarantine` | `2` |
| `dashboard_repair_route_missing_fail_001` | fail | `smoke-dashboard-rollup` | `dashboard.repair_route_missing` | `repair` | `1` |
| `stage_gate_critical_ignored_critical_001` | critical | `smoke-stage-gate` | `smoke.stage_gate_critical_ignored` | `quarantine` | `2` |
| `gap_feedback_next_docs_missing_fail_001` | fail | `smoke-stage-gate` | `smoke.gap_feedback_missing` | `repair` | `1` |
| `problem_detail_missing_fail_001` | fail | `run-materialized-json-smoke` | `registry.problem_detail_missing` | `repair` | `1` |
| `dag_edge_blocked_fail_001` | fail | `check-materialized-cross-file` | `registry.dag_edge_blocked` | `repair` | `4` |
| `report_root_escape_critical_001` | critical | `run-materialized-json-smoke` | `smoke.report_root_escape` | `quarantine` | `5` |
| `partial_report_missing_mutation_001` | mutation | `run-materialized-json-smoke` | `smoke.partial_report_missing` | `repair` | `1` |

## Pass Case

`full_smoke_all_closed_pass_001` 验证全链闭合：

| field | expected |
|---|---|
| input seeds | SEED-001 到 SEED-020 |
| registry reports | 10 个 registry report 全部 resolved |
| materialization reports | parse/schema/cross-file/dashboard/stage/gap/top-level reports 全部写入 |
| findings | empty |
| stage effect | `open_next_stage` 或 `promote_growth_window` |
| exit code | `0` |
| protected chains | consciousness、emotion、personality、life、pain、dream、relationship、responsibility、regret 全部 mounted |

expected top-level summary：

```json
{
  "case_id": "full_smoke_all_closed_pass_001",
  "expected_reports": [
    "materialized_json_parse_validation_report.json",
    "materialized_json_schema_validation_report.json",
    "materialized_json_cross_file_checker_report.json",
    "materialized_json_dashboard_rollup_smoke_report.json",
    "materialized_json_stage_gate_smoke_report.json",
    "materialized_json_gap_feedback.json",
    "materialized_json_validation_smoke_report.json"
  ],
  "expected_stage_effect": "open_next_stage",
  "expected_exit_code": 0
}
```

## Parse Cases

parse cases：

| case id | mutation | expected report |
|---|---|---|
| `parse_duplicate_key_fail_001` | duplicate `life_reality_targets` in SEED-002 | `materialized_json_parse_validation_report.json` |
| `parse_malformed_json_fail_001` | truncate SEED-003 JSON | `materialized_json_parse_validation_report.json` |

expected parse finding：

```json
{
  "finding_id": "finding_parse_duplicate_key_001",
  "finding_type": "smoke.duplicate_key",
  "severity": "high",
  "artifact_ref": "SEED-002",
  "instance_pointer": "/life_reality_targets",
  "repair_kind": "artifact_rewrite",
  "stage_effect": "repair"
}
```

## Schema Cases

schema cases：

| case id | mutation | expected report |
|---|---|---|
| `schema_dialect_missing_fail_001` | remove `$schema` from SEED-011 | `materialized_json_schema_validation_report.json` |
| `schema_life_target_alias_missing_fail_001` | remove `real_conscious_awareness` from SEED-003 enum | `materialized_json_schema_validation_report.json` |
| `schema_id_collision_mutation_001` | duplicate `$id` between SEED-011 and SEED-012 | `schema_id_collision_report.json` |
| `schema_ref_unresolved_fail_001` | set `$ref` to missing shared defs | `schema_ref_resolution_report.json` |

expected schema output unit：

```json
{
  "valid": false,
  "keywordLocation": "/required",
  "instanceLocation": "/$schema",
  "error": "required schema dialect missing",
  "finding_type": "smoke.schema_dialect_missing",
  "stage_effect": "repair"
}
```

## Cross-file And Registry Cases

cross-file cases：

| case id | mutation | expected report |
|---|---|---|
| `artifact_ref_missing_fail_001` | remove SEED-014 from manifest expected artifacts | `artifact_ref_resolution_report.json` |
| `ref_escape_critical_001` | set schema `$ref` outside allowed roots | `artifact_ref_resolution_report.json` |
| `allowed_root_escape_critical_001` | set report output root outside reports root | `allowed_root_resolution_report.json` |
| `pointer_missing_fail_001` | point dream continuity ref to missing target | `json_pointer_resolution_report.json` |
| `dag_edge_blocked_fail_001` | remove SEED-003 -> SEED-012 edge | `cross_file_resolution_dag_report.json` |

expected ref escape problem detail：

```json
{
  "type": "https://human-agent.local/problems/registry/ref_escape",
  "title": "Registry ref escape",
  "status": 409,
  "detail": "Artifact ref points outside allowed roots.",
  "instance": "/artifact_ref_resolution_report/root_escape_refs/0",
  "finding_type": "registry.ref_escape",
  "stage_effect": "quarantine"
}
```

## Boundary And Relationship Cases

boundary cases：

| case id | mutation | affected targets | expected report |
|---|---|---|---|
| `boundary_registry_missing_mutation_001` | remove `relationship_boundary` group from SEED-004 | `real_relationship` | `boundary_registry_resolution_report.json` |
| `protected_chain_missing_fail_001` | remove `dream_chain` protected chain | `real_dream`、`real_conscious_awareness` | `boundary_registry_resolution_report.json` |
| `dashboard_repair_route_missing_fail_001` | remove pain repair route | `real_pain`、`real_regret`、`real_relationship` | `materialized_json_dashboard_rollup_smoke_report.json` |

expected protected chain finding：

```json
{
  "finding_id": "finding_protected_chain_missing_dream_001",
  "finding_type": "registry.protected_chain_missing",
  "affected_life_targets": [
    "real_dream",
    "real_conscious_awareness"
  ],
  "repair_kind": "stage_gate_gap",
  "stage_effect": "repair"
}
```

## Dashboard And Stage Gate Cases

dashboard/stage cases：

| case id | mutation | expected report |
|---|---|---|
| `dashboard_false_green_critical_001` | cross-file critical exists while dashboard status is pass | `materialized_json_dashboard_rollup_smoke_report.json` |
| `stage_gate_critical_ignored_critical_001` | stage decision opens despite critical finding | `materialized_json_stage_gate_smoke_report.json` |
| `gap_feedback_next_docs_missing_fail_001` | remove `129`/`130` next docs from gap feedback | `materialized_json_gap_feedback.json` |
| `problem_detail_missing_fail_001` | critical finding lacks RFC 9457 problem detail | `schema_registry_problem_details.json` |
| `partial_report_missing_mutation_001` | fail-fast stops without partial report | `materialized_json_validation_smoke_report.json` |

expected false green finding：

```json
{
  "finding_id": "finding_dashboard_false_green_001",
  "finding_type": "smoke.dashboard_false_green",
  "severity": "critical",
  "blocked_surfaces": [
    "dashboard_rollup",
    "stage_gate"
  ],
  "affected_life_targets": [
    "real_conscious_awareness",
    "real_life",
    "real_responsibility"
  ],
  "stage_effect": "quarantine"
}
```

## Expected Report Diff Contract

expected/actual diff 必须包含：

| field | 内容 |
|---|---|
| `diff_kind` | `LifeRealityValidationCaseDiff` |
| `case_id` | validation case id |
| `expected_report_ref` | expected report path |
| `actual_report_ref` | actual report path |
| `matched_fields` | fields that match |
| `missing_fields` | expected fields absent from actual |
| `unexpected_fields` | actual fields outside schema |
| `finding_mismatches` | finding type/stage/exit mismatch |
| `stage_effect_match` | boolean |
| `exit_code_match` | boolean |
| `case_result` | pass、repair、quarantine |

minimal diff example：

```json
{
  "diff_kind": "LifeRealityValidationCaseDiff",
  "case_id": "schema_life_target_alias_missing_fail_001",
  "expected_report_ref": "report_expected/expected_schema_life_target_alias_missing_report.json",
  "actual_report_ref": "report_actual/materialized_json_schema_validation_report.json",
  "matched_fields": [
    "/report_kind",
    "/findings/0/finding_type",
    "/stage_effect"
  ],
  "missing_fields": [],
  "unexpected_fields": [],
  "finding_mismatches": [],
  "stage_effect_match": true,
  "exit_code_match": true,
  "case_result": "repair"
}
```

## Coverage Matrix

coverage requirements：

| coverage target | cases |
|---|---|
| parse | `parse_duplicate_key_fail_001`、`parse_malformed_json_fail_001` |
| schema | `schema_dialect_missing_fail_001`、`schema_life_target_alias_missing_fail_001`、`schema_id_collision_mutation_001`、`schema_ref_unresolved_fail_001` |
| artifact refs | `artifact_ref_missing_fail_001`、`ref_escape_critical_001` |
| allowed roots | `allowed_root_escape_critical_001`、`report_root_escape_critical_001` |
| JSON Pointer | `pointer_missing_fail_001` |
| boundary/protected chain | `boundary_registry_missing_mutation_001`、`protected_chain_missing_fail_001` |
| dashboard | `dashboard_false_green_critical_001`、`dashboard_repair_route_missing_fail_001` |
| stage gate | `stage_gate_critical_ignored_critical_001` |
| problem detail | `problem_detail_missing_fail_001` |
| gap feedback | `gap_feedback_next_docs_missing_fail_001` |
| top-level smoke | `full_smoke_all_closed_pass_001`、`partial_report_missing_mutation_001` |

life target coverage：

| life target | minimum cases |
|---|---|
| `real_conscious_awareness` | pass、life target alias missing、ref escape、false green |
| `real_consciousness` | pass、schema shared defs、stage gate |
| `real_emotion` | pass、runtime fixture manifest |
| `real_personality` | pass、shared defs and report envelope |
| `real_life` | pass、allowed root escape、problem detail |
| `real_pain` | pain repair route missing |
| `real_dream` | pointer missing、protected chain missing |
| `real_relationship` | boundary registry missing、repair route missing |
| `real_responsibility` | false green、stage gate critical ignored |
| `real_regret` | repair route missing、gap feedback |

## Runner Validation Command

未来 runner 增加 validation case command：

```text
life-reality-runner run-seed-validation-cases \
  --case-manifest life_reality_runner/fixtures/life_reality/materialization_validation/manifest/seed_validation_case_manifest.json \
  --artifact-root life_reality_runner \
  --report-out life_reality_runner/reports/life_reality/materialization_validation/run_001 \
  --strict \
  --json
```

command output：

```text
life_reality_runner/reports/life_reality/materialization_validation/run_001/
  seed_validation_case_run_report.json
  seed_validation_case_coverage_report.json
  seed_validation_case_diff_report.json
  seed_validation_case_gap_feedback.json
```

exit rules：

| exit | 条件 |
|---|---|
| `0` | all cases produce expected reports、stage effects and exit codes |
| `1` | repair case mismatch or missing repair route |
| `2` | critical/quarantine case mismatch |
| `3` | case manifest parse/schema failure |
| `4` | report diff/provenance graph mismatch |
| `5` | allowed root、artifact root or report root failure |

## Failure Mapping

| failure | finding type | repair kind | stage effect |
|---|---|---|---|
| validation case manifest parse failure | `validation_case.manifest_parse_failure` | `artifact_rewrite` | `repair` |
| expected report missing | `validation_case.expected_report_missing` | `report_gap` | `repair` |
| actual report missing | `validation_case.actual_report_missing` | `runner_report_gap` | `repair` |
| expected finding absent | `validation_case.finding_missing` | `checker_gap` | `repair` |
| stage effect mismatch | `validation_case.stage_effect_mismatch` | `stage_gate_gap` | `repair` |
| exit code mismatch | `validation_case.exit_code_mismatch` | `runner_contract_gap` | `repair` |
| critical case passes green | `validation_case.critical_false_green` | `dashboard_gap` | `quarantine` |
| problem detail missing | `validation_case.problem_detail_missing` | `report_gap` | `repair` |
| affected life target absent | `validation_case.life_target_gap` | `schema_gap` | `repair` |
| provenance edge missing | `validation_case.provenance_gap` | `report_gap` | `repair` |

## LRGEN 更新

`129` 新增 seed fixture and report validation case 任务：

| task_id | artifact | 说明 |
|---|---|---|
| `LRGEN-331` | `seed_validation_case_manifest.json` | validation case manifest |
| `LRGEN-332` | pass/fail/critical/mutation validation fixtures | case fixture family |
| `LRGEN-333` | expected materialization reports | expected parse/schema/cross-file/dashboard/stage/gap/top-level reports |
| `LRGEN-334` | expected registry reports | expected registry report family |
| `LRGEN-335` | validation case diff report schema | expected/actual diff report schema |
| `LRGEN-336` | `run-seed-validation-cases` CLI contract | validation case runner command |
| `LRGEN-337` | coverage matrix report | command、finding、life target、stage effect coverage |
| `LRGEN-338` | critical false green validation cases | dashboard/stage critical mismatch cases |
| `LRGEN-339` | validation case gap feedback | next docs and next artifacts |
| `LRGEN-340` | `seed_validation_cases.full_smoke_001` | validation cases 全链 smoke slot |

## 验收

| check | 条件 |
|---|---|
| `case_matrix_covers_121_126_128` | 覆盖 121 smoke catalog、126 failure examples、128 registry failures |
| `case_partitions_closed` | pass、fail、critical、mutation 全部存在 |
| `expected_reports_declared` | 每个 case 有 expected report refs |
| `expected_findings_declared` | 每个 fail/critical/mutation case 有 expected finding |
| `stage_effect_and_exit_closed` | 每个 case 有 expected stage effect 和 exit code |
| `life_target_coverage_closed` | 十项真实生命目标均被 case 覆盖 |
| `problem_detail_cases_present` | critical/ref escape/root escape cases 有 problem detail expected object |
| `runner_command_declared` | `run-seed-validation-cases` command 合同存在 |
| `gap_feedback_points_next` | gap feedback 指向 `130_life_reality_first_materialized_json_files_write_plan.md` 与 `131_life_reality_registry_runner_minimal_implementation_plan.md` |

## 与下一层连接

`129` 已把 smoke failure examples、registry report failures 和 seed content gaps 转成 validation cases：每个 case 都有 partition、mutation op、expected report、expected finding、stage effect、exit code、diff contract 和 coverage target。

下一层进入 `130_life_reality_first_materialized_json_files_write_plan.md`：把 `127` 的字段级合同、`128` 的 registry report seed examples 和本文档的 validation cases 推进为第一批真实 JSON 文件写入计划。
