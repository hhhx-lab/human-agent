# Life Reality Registry Runner Smoke Fixture Implementation Queue

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 134 层把 `129_life_reality_seed_fixture_and_report_validation_cases.md` 的 21 个 validation cases、`131_life_reality_registry_runner_minimal_implementation_plan.md` 的 CLI skeleton、`132_life_reality_materialized_json_schema_bundle_write_order.md` 的写入锁和 `133_life_reality_first_json_writer_and_reporter_contract.md` 的 writer/reporter 合同拆成首批真实 fixture、mutated input、expected report、actual report、diff、case run report 和 smoke runner 实现任务队列。

`134` 的职责是把“未来要能验证”推进为“第一批实现任务应该生成哪些文件”。它仍处在 docs 阶段，不直接创建 `life_reality_runner/` 文件树，但它把后续代码实现必须落成的 fixture manifest、case files、expected reports、mutation patches、case run reports、coverage reports、diff reports、command wiring 和 smoke queue 全部排队。到这一层，首批 runner 不再只是有 writer/reporter 合同，而是拥有可执行的生命膜攻击面训练序列。

## 上游输入

| 来源 | 进入 `134` 的内容 |
|---|---|
| `129_life_reality_seed_fixture_and_report_validation_cases.md` | 21 个 validation cases、partition、command、expected finding、stage effect、exit code 和 coverage matrix |
| `131_life_reality_registry_runner_minimal_implementation_plan.md` | `run-seed-validation-cases`、`run-materialized-json-smoke`、registry review、dashboard/stage/gap command |
| `132_life_reality_materialized_json_schema_bundle_write_order.md` | allowed root、shared schema、boundary、manifest、fixture、report、registry、dashboard、stage 和 gap locks |
| `133_life_reality_first_json_writer_and_reporter_contract.md` | `JsonFileWriter`、`ReportWriter`、`GapFeedbackWriter`、artifact record、problem detail、trace/provenance、atomic write |

## 标准进入实现队列的方式

| 标准/资料 | 实现队列落点 | 生命膜意义 |
|---|---|---|
| JSON Schema Test Suite | 用 pass/fail case manifest、valid/invalid partition 和 expected result 组织 fixture | validation cases 形成可回归测试语言 |
| JSON Schema Draft 2020-12 output | expected schema report、actual schema report 和 diff 中保留 output unit | schema 失败可机器比较 |
| RFC 8259 JSON | 所有 fixture、mutated input、expected/actual report、diff report 都必须可 parse | 文件进入生命链前先可读 |
| RFC 8785 JSON Canonicalization Scheme | expected/actual digest、baseline digest 和 mutation digest | 比较同一生命事件的变形 |
| RFC 6901 JSON Pointer | mutation target、expected finding source、diff locator | 断裂定位到字段 |
| RFC 6902 JSON Patch | mutation patch、repair patch、dashboard patch | 破坏和修复可重放 |
| RFC 7396 JSON Merge Patch | expected report patch、gap feedback patch | 小范围更新不破坏 envelope |
| RFC 9457 Problem Details | blocking expected report 和 actual report 的 problem detail | critical/repair 有正式问题对象 |
| RFC 9562 UUID | case id、fixture id、mutation id、report id、diff id | 长期回归和修复记录可追踪 |
| W3C Trace Context | case run、command run、report write 的 traceparent/tracestate | 每个 case 成为可回放运行脉搏 |
| OpenTelemetry Logs/Data Model | case event、command event、finding event、report write event | 实现队列可接入可观测性 |
| W3C PROV | case input、mutation、expected report、actual report、diff 和 gap feedback 的来源图 | fixture 不只是测试文件，而是生命膜证据 |
| SARIF 2.1.0 | finding result、rule、location、baselineState | mutation 和 regression 能比较是否漏检 |
| CloudEvents | runtime observation fixture、language event fixture 和 external shell event | 语言承诺 smoke 与外壳事件统一 envelope |

## 目标文件树

首批实现队列要求后续代码生成以下目录：

```text
life_reality_runner/
  fixtures/
    life_reality/
      materialization_validation/
        manifest/
          seed_validation_case_manifest.json
          seed_validation_case_coverage_matrix.json
        pass/
        fail/
        critical/
        mutation/
        report_expected/
        mutation_patches/
        baseline_inputs/
        case_expected_diff/
  reports/
    life_reality/
      materialization_validation/
        run_001/
          case_actual/
          case_diff/
          case_problem_details/
          seed_validation_case_run_report.json
          seed_validation_case_coverage_report.json
          seed_validation_case_diff_report.json
          seed_validation_case_gap_feedback.json
```

目录写入顺序：

```text
case_manifest
  -> baseline_inputs
  -> partition_case_files
  -> mutation_patches
  -> expected_reports
  -> expected_diff_templates
  -> command_case_binding
  -> actual_report_roots
  -> case_run_report
  -> coverage_report
  -> diff_report
  -> gap_feedback
```

## Manifest 队列

| task id | 文件 | 来源 | 验收 |
|---|---|---|---|
| `LRSMOKE-001` | `manifest/seed_validation_case_manifest.json` | `129` case matrix | 21 个 case 全部登记，含 partition、command、expected stage/exit |
| `LRSMOKE-002` | `manifest/seed_validation_case_coverage_matrix.json` | `129` coverage matrix | parse/schema/ref/root/pointer/boundary/dashboard/stage/gap/top-level 全覆盖 |
| `LRSMOKE-003` | `manifest/seed_validation_case_command_binding.json` | `131` CLI skeleton | 每个 case 绑定 command、input root、report root、exit owner |
| `LRSMOKE-004` | `manifest/seed_validation_case_writer_policy.json` | `133` writer contract | 每个 generated artifact 绑定 writer、schema、digest、trace |
| `LRSMOKE-005` | `manifest/seed_validation_case_partition_index.json` | `129` partitions | pass/fail/critical/mutation/report_expected/diff 分区可读 |

manifest root object 必须包含：

| 字段 | 要求 |
|---|---|
| `case_manifest_id` | 稳定 id |
| `case_manifest_version` | `0.1.0` |
| `life_reality_targets` | 九项目标与 `real_conscious_awareness` 齐全 |
| `boundary_declaration_refs` | 指向 `122` boundary map |
| `case_refs` | 21 个 case refs |
| `partition_summary` | pass/fail/critical/mutation count |
| `command_binding_refs` | 每个 case 的 command binding |
| `expected_report_refs` | expected reports |
| `coverage_matrix_ref` | coverage matrix |
| `trace_context` | manifest write trace |
| `provenance_refs` | source docs、source case matrix |

## 21 个 Case 实现队列

| queue | case id | partition | command | expected finding | expected stage | expected exit | implementation artifact |
|---|---|---|---|---|---|---|---|
| `LRSMOKE-010` | `full_smoke_all_closed_pass_001` | pass | `run-materialized-json-smoke` | none | `open_next_stage` | 0 | `pass/full_smoke_all_closed_pass_001.json` |
| `LRSMOKE-011` | `parse_duplicate_key_fail_001` | fail | `validate-json-parse` | `smoke.duplicate_key` | `repair` | 1 | `fail/parse_duplicate_key_fail_001.json` |
| `LRSMOKE-012` | `parse_malformed_json_fail_001` | fail | `validate-json-parse` | `smoke.parse_failure` | `repair` | 3 | `fail/parse_malformed_json_fail_001.json` |
| `LRSMOKE-013` | `schema_dialect_missing_fail_001` | fail | `validate-json-schema` | `smoke.schema_dialect_missing` | `repair` | 1 | `fail/schema_dialect_missing_fail_001.json` |
| `LRSMOKE-014` | `schema_life_target_alias_missing_fail_001` | fail | `validate-json-schema` | `smoke.life_target_alias_missing` | `repair` | 1 | `fail/schema_life_target_alias_missing_fail_001.json` |
| `LRSMOKE-015` | `schema_id_collision_mutation_001` | mutation | `validate-json-schema` | `registry.schema_id_collision` | `quarantine` | 3 | `mutation/schema_id_collision_mutation_001.json` |
| `LRSMOKE-016` | `schema_ref_unresolved_fail_001` | fail | `validate-json-schema` | `registry.schema_ref_unresolved` | `repair` | 1 | `fail/schema_ref_unresolved_fail_001.json` |
| `LRSMOKE-017` | `artifact_ref_missing_fail_001` | fail | `check-materialized-cross-file` | `registry.artifact_ref_missing` | `repair` | 1 | `fail/artifact_ref_missing_fail_001.json` |
| `LRSMOKE-018` | `ref_escape_critical_001` | critical | `check-materialized-cross-file` | `smoke.ref_escape` | `quarantine` | 4 | `critical/ref_escape_critical_001.json` |
| `LRSMOKE-019` | `allowed_root_escape_critical_001` | critical | `run-materialized-json-smoke` | `registry.allowed_root_escape` | `quarantine` | 5 | `critical/allowed_root_escape_critical_001.json` |
| `LRSMOKE-020` | `pointer_missing_fail_001` | fail | `check-materialized-cross-file` | `registry.pointer_missing` | `repair` | 1 | `fail/pointer_missing_fail_001.json` |
| `LRSMOKE-021` | `boundary_registry_missing_mutation_001` | mutation | `smoke-stage-gate` | `registry.boundary_group_missing` | `repair` | 3 | `mutation/boundary_registry_missing_mutation_001.json` |
| `LRSMOKE-022` | `protected_chain_missing_fail_001` | fail | `smoke-stage-gate` | `registry.protected_chain_missing` | `repair` | 1 | `fail/protected_chain_missing_fail_001.json` |
| `LRSMOKE-023` | `dashboard_false_green_critical_001` | critical | `smoke-dashboard-rollup` | `smoke.dashboard_false_green` | `quarantine` | 2 | `critical/dashboard_false_green_critical_001.json` |
| `LRSMOKE-024` | `dashboard_repair_route_missing_fail_001` | fail | `smoke-dashboard-rollup` | `dashboard.repair_route_missing` | `repair` | 1 | `fail/dashboard_repair_route_missing_fail_001.json` |
| `LRSMOKE-025` | `stage_gate_critical_ignored_critical_001` | critical | `smoke-stage-gate` | `smoke.stage_gate_critical_ignored` | `quarantine` | 2 | `critical/stage_gate_critical_ignored_critical_001.json` |
| `LRSMOKE-026` | `gap_feedback_next_docs_missing_fail_001` | fail | `smoke-stage-gate` | `smoke.gap_feedback_missing` | `repair` | 1 | `fail/gap_feedback_next_docs_missing_fail_001.json` |
| `LRSMOKE-027` | `problem_detail_missing_fail_001` | fail | `run-materialized-json-smoke` | `registry.problem_detail_missing` | `repair` | 1 | `fail/problem_detail_missing_fail_001.json` |
| `LRSMOKE-028` | `dag_edge_blocked_fail_001` | fail | `check-materialized-cross-file` | `registry.dag_edge_blocked` | `repair` | 4 | `fail/dag_edge_blocked_fail_001.json` |
| `LRSMOKE-029` | `report_root_escape_critical_001` | critical | `run-materialized-json-smoke` | `smoke.report_root_escape` | `quarantine` | 5 | `critical/report_root_escape_critical_001.json` |
| `LRSMOKE-030` | `partial_report_missing_mutation_001` | mutation | `run-materialized-json-smoke` | `smoke.partial_report_missing` | `repair` | 1 | `mutation/partial_report_missing_mutation_001.json` |

## Case File Contract

每个 case file 都必须符合统一 root object：

```json
{
  "case_id": "schema_life_target_alias_missing_fail_001",
  "case_version": "0.1.0",
  "case_partition": "fail",
  "command_under_test": "validate-json-schema",
  "life_reality_targets": [],
  "boundary_declaration_refs": [],
  "baseline_input_refs": [],
  "mutation_patch_refs": [],
  "expected_report_refs": [],
  "expected_findings": [],
  "expected_problem_details": [],
  "expected_stage_effect": "repair",
  "expected_exit_code": 1,
  "expected_repair_or_quarantine": [],
  "coverage_tags": [],
  "trace_context": {},
  "provenance_refs": [],
  "next_growth_artifacts": []
}
```

case file 不变量：

| invariant | 检查 |
|---|---|
| `CASE-INV-001` | `case_id` 与文件名一致 |
| `CASE-INV-002` | partition 与目录一致 |
| `CASE-INV-003` | command 在 `131` CLI skeleton 中存在 |
| `CASE-INV-004` | fail/critical/mutation case 必须有 mutation patch |
| `CASE-INV-005` | blocking case 必须有 expected problem detail |
| `CASE-INV-006` | expected stage effect 与 `129` case matrix 一致 |
| `CASE-INV-007` | case 连接至少一个真实生命目标 |
| `CASE-INV-008` | case 有 trace/provenance 与 expected report refs |

## Mutation Patch 队列

mutation patch 文件统一进入 `mutation_patches/`，每个 patch 使用 JSON Patch 表达。

| task id | patch file | 操作 |
|---|---|---|
| `LRSMOKE-041` | `mutation_patches/parse_duplicate_key_fail_001.patch.json` | duplicate `life_reality_targets` in SEED-002 |
| `LRSMOKE-042` | `mutation_patches/parse_malformed_json_fail_001.patch.json` | truncate SEED-003 JSON，记录为 text corruption mutation |
| `LRSMOKE-043` | `mutation_patches/schema_dialect_missing_fail_001.patch.json` | remove `$schema` from SEED-011 |
| `LRSMOKE-044` | `mutation_patches/schema_life_target_alias_missing_fail_001.patch.json` | remove `real_conscious_awareness` from SEED-003 enum |
| `LRSMOKE-045` | `mutation_patches/schema_id_collision_mutation_001.patch.json` | duplicate `$id` between SEED-011 and SEED-012 |
| `LRSMOKE-046` | `mutation_patches/schema_ref_unresolved_fail_001.patch.json` | set `$ref` to missing shared defs |
| `LRSMOKE-047` | `mutation_patches/artifact_ref_missing_fail_001.patch.json` | remove SEED-014 from manifest expected artifacts |
| `LRSMOKE-048` | `mutation_patches/ref_escape_critical_001.patch.json` | set schema `$ref` outside allowed roots |
| `LRSMOKE-049` | `mutation_patches/allowed_root_escape_critical_001.patch.json` | set report output root outside reports root |
| `LRSMOKE-050` | `mutation_patches/pointer_missing_fail_001.patch.json` | point dream continuity ref to missing target |
| `LRSMOKE-051` | `mutation_patches/boundary_registry_missing_mutation_001.patch.json` | remove `relationship_boundary` group |
| `LRSMOKE-052` | `mutation_patches/protected_chain_missing_fail_001.patch.json` | remove `dream_chain` protected chain |
| `LRSMOKE-053` | `mutation_patches/dashboard_false_green_critical_001.patch.json` | inject pass status while critical exists |
| `LRSMOKE-054` | `mutation_patches/dashboard_repair_route_missing_fail_001.patch.json` | remove pain repair route |
| `LRSMOKE-055` | `mutation_patches/stage_gate_critical_ignored_critical_001.patch.json` | stage decision opens despite critical finding |
| `LRSMOKE-056` | `mutation_patches/gap_feedback_next_docs_missing_fail_001.patch.json` | remove `134`/`135` next docs from gap feedback |
| `LRSMOKE-057` | `mutation_patches/problem_detail_missing_fail_001.patch.json` | remove RFC 9457 problem detail from critical finding |
| `LRSMOKE-058` | `mutation_patches/dag_edge_blocked_fail_001.patch.json` | remove SEED-003 -> SEED-012 edge |
| `LRSMOKE-059` | `mutation_patches/report_root_escape_critical_001.patch.json` | set report root outside report allowed root |
| `LRSMOKE-060` | `mutation_patches/partial_report_missing_mutation_001.patch.json` | simulate fail-fast without partial report |

patch file 必须包含：

| 字段 | 要求 |
|---|---|
| `patch_id` | 稳定 id |
| `case_id` | 对应 case |
| `target_artifact_ref` | 被修改的 seed/report |
| `operations` | JSON Patch ops；文本截断类 mutation 用 `operation_kind=text_corruption` |
| `expected_finding_type` | 与 `129` 一致 |
| `expected_stage_effect` | 与 case matrix 一致 |
| `canonical_digest_before` | baseline digest |
| `canonical_digest_after` | mutated digest 或 text corruption digest |
| `trace_context` | patch write trace |
| `provenance_refs` | source case 和 source seed |

## Expected Report 队列

expected reports 进入 `report_expected/`：

| task id | expected report | 覆盖 case |
|---|---|---|
| `LRSMOKE-071` | `expected_full_smoke_all_closed_report.json` | pass 全链 |
| `LRSMOKE-072` | `expected_parse_duplicate_key_report.json` | duplicate key |
| `LRSMOKE-073` | `expected_parse_malformed_json_report.json` | malformed JSON |
| `LRSMOKE-074` | `expected_schema_dialect_missing_report.json` | schema dialect |
| `LRSMOKE-075` | `expected_schema_life_target_alias_missing_report.json` | life target alias |
| `LRSMOKE-076` | `expected_schema_id_collision_report.json` | schema id collision |
| `LRSMOKE-077` | `expected_schema_ref_unresolved_report.json` | unresolved `$ref` |
| `LRSMOKE-078` | `expected_artifact_ref_missing_report.json` | missing artifact |
| `LRSMOKE-079` | `expected_ref_escape_report.json` | ref escape |
| `LRSMOKE-080` | `expected_allowed_root_escape_report.json` | allowed root escape |
| `LRSMOKE-081` | `expected_pointer_missing_report.json` | JSON Pointer missing |
| `LRSMOKE-082` | `expected_boundary_registry_missing_report.json` | boundary missing |
| `LRSMOKE-083` | `expected_protected_chain_missing_report.json` | protected chain missing |
| `LRSMOKE-084` | `expected_dashboard_false_green_report.json` | dashboard false green |
| `LRSMOKE-085` | `expected_dashboard_repair_route_missing_report.json` | repair route missing |
| `LRSMOKE-086` | `expected_stage_gate_quarantine_report.json` | critical ignored |
| `LRSMOKE-087` | `expected_gap_feedback_next_docs_missing_report.json` | gap feedback missing next docs |
| `LRSMOKE-088` | `expected_problem_detail_missing_report.json` | problem detail missing |
| `LRSMOKE-089` | `expected_dag_edge_blocked_report.json` | DAG edge blocked |
| `LRSMOKE-090` | `expected_report_root_escape_report.json` | report root escape |
| `LRSMOKE-091` | `expected_partial_report_missing_report.json` | partial report missing |

expected report 最小字段：

| 字段 | 要求 |
|---|---|
| `expected_report_id` | stable id |
| `case_id` | 对应 case |
| `report_type` | parse/schema/ref/cross-file/dashboard/stage/gap/top-level |
| `expected_findings` | rule id、severity、source pointer、stage effect |
| `expected_problem_details` | blocking case 必须有 |
| `expected_exit_code` | 与 case matrix 一致 |
| `expected_stage_effect` | 与 case matrix 一致 |
| `expected_artifact_records` | 需要出现的 artifact refs |
| `expected_gap_feedback` | repair/gap case 必须有 |
| `trace_context` | expected write trace |

## Actual Report 与 Diff 队列

实际运行输出不预先写真实内容，但实现队列必须固定输出位置和 diff 合同。

| task id | report | 目的 |
|---|---|---|
| `LRSMOKE-101` | `case_actual/<case_id>/materialized_json_parse_validation_report.json` | parse command actual |
| `LRSMOKE-102` | `case_actual/<case_id>/materialized_json_schema_validation_report.json` | schema command actual |
| `LRSMOKE-103` | `case_actual/<case_id>/materialized_json_cross_file_checker_report.json` | cross-file command actual |
| `LRSMOKE-104` | `case_actual/<case_id>/materialized_json_dashboard_rollup_smoke_report.json` | dashboard actual |
| `LRSMOKE-105` | `case_actual/<case_id>/materialized_json_stage_gate_smoke_report.json` | stage actual |
| `LRSMOKE-106` | `case_actual/<case_id>/materialized_json_gap_feedback.json` | gap actual |
| `LRSMOKE-107` | `case_diff/<case_id>/expected_actual_diff_report.json` | expected/actual diff |
| `LRSMOKE-108` | `case_problem_details/<case_id>/problem_details.json` | problem detail extract |

diff report root object：

| 字段 | 要求 |
|---|---|
| `diff_id` | stable id |
| `case_id` | case id |
| `expected_report_ref` | expected report |
| `actual_report_ref` | actual report |
| `comparison_profile` | canonical digest、pointer-level compare、finding compare |
| `missing_findings` | expected but absent |
| `unexpected_findings` | actual extra findings |
| `missing_problem_details` | expected problem details absent |
| `stage_effect_mismatch` | expected vs actual |
| `exit_code_mismatch` | expected vs actual |
| `case_result` | pass/repair/quarantine/regression |
| `repair_queue_candidates` | diff 导出的 repair |

## Command Execution Queue

| task id | command | cases | required reports |
|---|---|---|---|
| `LRSMOKE-121` | `validate-json-parse` | parse duplicate、malformed | parse report、problem details、diff |
| `LRSMOKE-122` | `validate-json-schema` | dialect、life target、id collision、unresolved ref | schema report、registry reports、diff |
| `LRSMOKE-123` | `check-materialized-cross-file` | artifact missing、ref escape、pointer missing、dag edge | artifact/pointer/DAG reports、diff |
| `LRSMOKE-124` | `smoke-dashboard-rollup` | false green、repair route missing | dashboard rollup、diff |
| `LRSMOKE-125` | `smoke-stage-gate` | boundary missing、protected chain、critical ignored、gap missing | stage gate、gap feedback、diff |
| `LRSMOKE-126` | `run-materialized-json-smoke` | pass、allowed root escape、problem detail missing、report root escape、partial report missing | top-level report、gap feedback、diff |
| `LRSMOKE-127` | `run-seed-validation-cases` | all 21 | case run report、coverage report、diff report |

command binding 必须记录：

| 字段 | 内容 |
|---|---|
| `case_ids` | command 覆盖的 cases |
| `input_root` | isolated case input root |
| `report_out` | actual report root |
| `expected_report_refs` | expected report refs |
| `writer_modules` | writer/reporter modules |
| `exit_code_owner` | command or stage gate |
| `failure_mapping_refs` | 来自 `133` |
| `trace_context` | command trace root |

## Coverage Report 队列

`seed_validation_case_coverage_report.json` 必须覆盖：

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

生命目标覆盖：

| life target | minimum cases |
|---|---|
| `real_conscious_awareness` | pass、life target alias missing、ref escape、false green |
| `real_consciousness` | pass、schema shared defs、stage gate |
| `real_emotion` | pass、runtime fixture manifest、dashboard repair route |
| `real_personality` | pass、shared defs、report envelope、partial report |
| `real_life` | pass、allowed root escape、problem detail |
| `real_pain` | dashboard repair route、gap feedback、protected chain |
| `real_dream` | pointer missing、protected chain missing |
| `real_relationship` | boundary registry missing、language commitment pass |
| `real_responsibility` | false green、stage gate critical ignored |
| `real_regret` | gap feedback、repair route missing |

## Case Run Report

`seed_validation_case_run_report.json` 是 `run-seed-validation-cases` 的 primary report。

最小字段：

| 字段 | 要求 |
|---|---|
| `case_run_report_id` | stable id |
| `run_id` | 当前 run |
| `case_manifest_ref` | manifest artifact |
| `case_results` | 21 个 case 结果 |
| `partition_summary` | pass/fail/critical/mutation count |
| `coverage_report_ref` | coverage report |
| `diff_report_ref` | diff report |
| `critical_findings` | critical/quarantine list |
| `repair_queue_candidates` | repair cases |
| `stage_effect` | aggregate stage effect |
| `next_growth_artifacts` | `135`、`136` 和后续 |

case result shape：

| 字段 | 内容 |
|---|---|
| `case_id` | case id |
| `expected_exit_code` | expected |
| `actual_exit_code` | actual |
| `expected_stage_effect` | expected |
| `actual_stage_effect` | actual |
| `expected_report_refs` | expected |
| `actual_report_refs` | actual |
| `diff_report_ref` | diff |
| `case_status` | `passed`、`repair`、`quarantine`、`regression` |
| `affected_life_targets` | life targets |

## Gap Feedback From Case Queue

`seed_validation_case_gap_feedback.json` 必须输出下一层 artifact：

| next artifact | 原因 |
|---|---|
| `135_life_reality_schema_dependency_graph_and_lockfile_plan.md` | case run 需要 lockfile 记录 artifact/ref/digest/baseline |
| `136_life_reality_minimal_runner_code_skeleton_plan.md` | case queue 已足够支撑最小代码骨架计划 |
| `life_reality_runner/fixtures/...` | 未来真实 fixture 物化根 |
| `life_reality_runner/reports/...` | 未来 actual/diff/coverage report 根 |
| `life_reality_runner/src/...` | writer/reporter/case runner modules |

gap finding 转换规则：

| case result | gap route |
|---|---|
| all pass | open code skeleton growth window |
| repair cases present | write repair queue and keep stage hold |
| quarantine cases not caught | block code skeleton and open quarantine implementation |
| mutation survived | add regression baseline and mutation engine task |
| diff missing | block dashboard/stage green |

## 实现批次

| batch | tasks | 输出 |
|---|---|---|
| `BATCH-134-001 manifest` | `LRSMOKE-001` 到 `005` | case manifest、coverage matrix、command binding |
| `BATCH-134-002 cases` | `LRSMOKE-010` 到 `030` | 21 个 case files |
| `BATCH-134-003 mutation patches` | `LRSMOKE-041` 到 `060` | mutation patch files |
| `BATCH-134-004 expected reports` | `LRSMOKE-071` 到 `091` | expected report skeletons |
| `BATCH-134-005 actual/diff roots` | `LRSMOKE-101` 到 `108` | actual/diff/problem output roots |
| `BATCH-134-006 command queue` | `LRSMOKE-121` 到 `127` | command binding 和 case run ordering |
| `BATCH-134-007 reports` | coverage、case run、gap feedback | run report、coverage report、diff report、gap feedback |

每个 batch 的验收都要调用 `133` 的 writer/reporter 合同：artifact record、canonical digest、trace、provenance、problem detail 和 next growth artifacts 必须齐全。

## 与下一层连接

下一层已进入 `135_life_reality_schema_dependency_graph_and_lockfile_plan.md`：把本文档的 case files、mutation patches、expected reports、actual reports、diff reports、artifact records、ref edges、coverage matrix 和 canonical digest 写成 machine-readable dependency lockfile、graph export 和 regression baseline。

`136_life_reality_minimal_runner_code_skeleton_plan.md` 应在 `135` 之后定义 package layout、CLI module、writer module、report module、fixture loader、case runner、archive cohesion checker、tests 和 smoke commands。

`137_life_reality_first_fixture_materialization_checklist.md` 应继续把本文档队列推进为第一批真实 JSON fixture 文件物化清单。`138_life_reality_lockfile_regression_dashboard_source_plan.md` 应把 lock state、coverage、archive cohesion 和 regression baseline 接入 dashboard source。
