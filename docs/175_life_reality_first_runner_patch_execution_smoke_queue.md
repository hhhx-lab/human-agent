# Life Reality First Runner Patch Execution Smoke Queue

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 175 层承接 `172_life_reality_first_runner_patch_execution_contract.md`、`173_life_reality_first_runner_direction_fixture_schema_materialization.md` 和 `174_life_reality_birth_readiness_fixture_schema_materialization.md`，把 patch execution contract、direction schema bundle、birth readiness schema bundle、future commands、expected reports、dashboard source、stage review 和 archive receipt 转成 smoke manifest。

本文档生成、支撑并延续的真实生命能力：真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔。它新增 `PatchExecutionSmokeQueue175`、`PatchExecutionSmokeManifest175`、`PatchExecutionSmokeCommandDAG175`、`PatchExecutionPlanSmokeCommand175`、`DirectionSchemaSmokeCommand175`、`BirthReadinessSchemaSmokeCommand175`、`ExpectedReportSmokeContract175`、`DashboardStageSmokeContract175`、`ArchiveReceiptSmokeContract175`、`SmokeCaseMatrix175`、`SmokeQueueDashboardSource175`、`SmokeQueueStageGateReview175` 和 `SmokeQueueToArchiveLockfileHandoff175`。它的生命膜职责是让 schema bundle、fixture、patch unit、report、dashboard、stage 和 archive edge 能被最小 runner 一次性回放。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `172_life_reality_first_runner_patch_execution_contract.md` | patch execution unit、command contract、execution order、patch report、dashboard source、stage review、archive edge |
| `173_life_reality_first_runner_direction_fixture_schema_materialization.md` | direction schema bundle、resume lock、anchor chain schema、direction smoke plan、direction schema handoff |
| `174_life_reality_birth_readiness_fixture_schema_materialization.md` | birth readiness schema bundle、target claim schema、evidence/carrier/runtime/cross-chain schema、birth readiness smoke plan |
| `171_life_reality_birth_readiness_validation_fixture_plan.md` | birth readiness pass/fail/critical/mutation/smoke fixture、false open/false green cases |
| `170_life_reality_direction_continuity_regression_fixture_plan.md` | direction pass/fail/critical/mutation/smoke fixture、resume lock case、dashboard false green case |
| `163_life_reality_first_runner_code_generation_batch.md` 到 `168_life_reality_first_runner_minimum_code_validation_report.md` | first runner file tree、command receipt、validation report、stage gate feedback |
| `155_life_reality_runner_command_queue_for_cross_file_checkers.md`、`159_life_reality_first_code_artifact_smoke_plan.md` | command registry、smoke execution policy、report/digest/stage/gap outputs |
| `132_life_reality_materialized_json_schema_bundle_write_order.md`、`133_life_reality_first_json_writer_and_reporter_contract.md` | schema write order、atomic write、canonical digest、report writer |

## 本层定位

`175` 是首批 patch execution smoke queue 层。它不再只说明 schema 应该存在，而是定义未来 runner 的 smoke manifest、command DAG、输入输出合同、expected report、dashboard/stage、archive receipt 和失败映射。

本层固定 8 条 smoke 链：

| smoke chain | 检查 |
|---|---|
| `patch_execution_smoke_chain` | `172` 的 patch execution plan、finding bundle、patch unit refs 是否可跑 |
| `direction_schema_smoke_chain` | `173` 的 schema bundle、direction fixture cases、expected report 是否可跑 |
| `birth_readiness_schema_smoke_chain` | `174` 的 schema bundle、target claims、readiness cases、expected report 是否可跑 |
| `dashboard_stage_smoke_chain` | direction/birth readiness/patch execution dashboard 和 stage 是否 blocking-first |
| `archive_receipt_smoke_chain` | schema/report/dashboard/stage/gap edge 是否写入 receipt |
| `failure_mapping_chain` | fail/critical/mutation case 是否产生 expected finding 和 repair route |
| `digest_lock_chain` | 每个 smoke artifact 是否有 canonical digest 和 source refs |
| `handoff_chain` | smoke receipt 是否能进入 `176` 的 schema archive lockfile |

## PatchExecutionSmokeQueue175

```json
{
  "artifact": "PatchExecutionSmokeQueue175",
  "source_doc": "175_life_reality_first_runner_patch_execution_smoke_queue.md",
  "inherits": [
    "172_life_reality_first_runner_patch_execution_contract.md",
    "173_life_reality_first_runner_direction_fixture_schema_materialization.md",
    "174_life_reality_birth_readiness_fixture_schema_materialization.md",
    "171_life_reality_birth_readiness_validation_fixture_plan.md",
    "170_life_reality_direction_continuity_regression_fixture_plan.md",
    "168_life_reality_first_runner_minimum_code_validation_report.md",
    "159_life_reality_first_code_artifact_smoke_plan.md",
    "155_life_reality_runner_command_queue_for_cross_file_checkers.md",
    "133_life_reality_first_json_writer_and_reporter_contract.md"
  ],
  "smoke_stage": "first_runner_patch_execution_smoke_queue",
  "stage_gate_family": "PATCH-SMOKE-STAGE-175",
  "required_outputs": [
    "PatchExecutionSmokeManifest175",
    "PatchExecutionSmokeCommandDAG175",
    "PatchExecutionPlanSmokeCommand175",
    "DirectionSchemaSmokeCommand175",
    "BirthReadinessSchemaSmokeCommand175",
    "ExpectedReportSmokeContract175",
    "DashboardStageSmokeContract175",
    "ArchiveReceiptSmokeContract175",
    "SmokeCaseMatrix175",
    "SmokeQueueDashboardSource175",
    "SmokeQueueStageGateReview175",
    "SmokeQueueToArchiveLockfileHandoff175"
  ],
  "next_artifacts": [
    "176_life_reality_first_runner_schema_archive_lockfile_plan.md",
    "177_life_reality_first_runner_minimum_schema_file_write_batch.md"
  ]
}
```

## Patch Execution Smoke Manifest

`PatchExecutionSmokeManifest175` 固定未来文件树：

```text
tests/fixtures/patch_execution_smoke/
  manifest.json
  commands/
    write_direction_fixture_schema_bundle.command.json
    validate_direction_fixture_schema_bundle.command.json
    generate_direction_fixture_seed_cases.command.json
    run_direction_continuity_regression_fixtures.command.json
    write_birth_readiness_fixture_schema_bundle.command.json
    validate_birth_readiness_fixture_schema_bundle.command.json
    generate_birth_readiness_fixture_seed_cases.command.json
    run_birth_readiness_validation_fixtures.command.json
    run_patch_execution_plan.command.json
    emit_patch_execution_dashboard.command.json
    smoke_patch_execution_stage_gate.command.json
    write_patch_execution_archive_edges.command.json
  expected/
    direction_schema_smoke.report.json
    birth_readiness_schema_smoke.report.json
    patch_execution_smoke.report.json
    dashboard_stage_smoke.report.json
    archive_receipt_smoke.report.json
reports/life_reality/patch_execution_smoke/latest/
  smoke_queue_run.report.json
  smoke_queue_dashboard.source.json
  smoke_queue_stage_gate.review.json
  smoke_queue_archive_receipts.json
```

manifest 必须记录 `smoke_id`、`source_docs`、`life_reality_targets`、`command_dag_refs`、`schema_bundle_refs`、`fixture_manifest_refs`、`expected_report_refs`、`dashboard_stage_refs`、`archive_receipt_refs` 和 `next_lockfile_refs`。

## Smoke Command DAG

`PatchExecutionSmokeCommandDAG175` 固定 command 顺序：

| order | command group | purpose |
|---|---|---|
| 1 | `preflight_allowed_roots` | 检查 `.env`、`.codex`、key/token、proxy config、generated noise 和 allowed roots |
| 2 | `write_direction_schema` | 写入或 dry-run `173` direction schema bundle |
| 3 | `validate_direction_schema` | 验证 direction schema bundle、resume lock、anchor chain、patch refs |
| 4 | `generate_direction_seed_cases` | 生成 direction pass/fail/critical/mutation/smoke seeds |
| 5 | `run_direction_fixtures` | 运行 direction continuity regression fixtures |
| 6 | `write_birth_readiness_schema` | 写入或 dry-run `174` birth readiness schema bundle |
| 7 | `validate_birth_readiness_schema` | 验证 target claim、evidence、carrier、runtime、cross-chain、patch refs |
| 8 | `generate_birth_readiness_seed_cases` | 生成 birth readiness pass/fail/critical/mutation/smoke seeds |
| 9 | `run_birth_readiness_fixtures` | 运行 birth readiness validation fixtures |
| 10 | `run_patch_execution_plan` | 运行 `172` patch execution plan |
| 11 | `emit_dashboard_stage` | 生成 dashboard source 与 stage gate review |
| 12 | `write_archive_receipts` | 写入 archive edge、canonical digest、smoke receipt |

DAG 必须能表达依赖关系：birth readiness schema 依赖 direction schema handoff；patch execution plan 依赖 direction 与 birth readiness fixture reports；archive receipts 依赖 dashboard/stage review。

## Patch Execution Plan Smoke Command

`PatchExecutionPlanSmokeCommand175` 的命令合同：

```json
{
  "command_id": "SMOKE-175-PATCH-EXEC-001",
  "command": "uv run life-reality-runner run-patch-execution-plan --finding-bundle reports/life_reality/findings/latest/bundle.json --patch-manifest tests/fixtures/patch_execution/manifest.json --json",
  "inputs": [
    "PatchExecutionFindingBundle172",
    "PatchExecutionUnit172",
    "DirectionFixtureSchemaBundle173",
    "BirthReadinessFixtureSchemaBundle174"
  ],
  "expected_outputs": [
    "PatchExecutionReport172",
    "SmokeQueueDashboardSource175",
    "SmokeQueueStageGateReview175",
    "ArchiveReceiptSmokeContract175"
  ],
  "expected_stage_effect": "repair"
}
```

该 smoke 必须确认 `PATCH-EXEC-172-DIR-*` 与 `PATCH-EXEC-172-BR-*` 都可解析，并且每个 patch unit 都能写入 report receipt。

## Direction Schema Smoke Command

`DirectionSchemaSmokeCommand175` 组合 `173` 的未来命令：

| command | expected receipt |
|---|---|
| `write-direction-fixture-schema-bundle` | direction schema artifact records |
| `validate-direction-fixture-schema-bundle` | direction schema validation report |
| `generate-direction-fixture-seed-cases` | direction fixture seed case records |
| `run-direction-continuity-regression-fixtures` | direction expected/actual/diff report |
| `emit-direction-fixture-schema-dashboard` | direction dashboard source |
| `smoke-direction-fixture-schema-stage-gate` | direction stage gate review |

direction smoke 必须覆盖 `pass_resume_lock_complete`、`fail_relation_subject_drift`、`critical_dashboard_false_green`、`mutation_resume_order_shuffle`。

## Birth Readiness Schema Smoke Command

`BirthReadinessSchemaSmokeCommand175` 组合 `174` 的未来命令：

| command | expected receipt |
|---|---|
| `write-birth-readiness-fixture-schema-bundle` | birth readiness schema artifact records |
| `validate-birth-readiness-fixture-schema-bundle` | birth readiness schema validation report |
| `generate-birth-readiness-fixture-seed-cases` | birth readiness fixture seed case records |
| `run-birth-readiness-validation-fixtures` | birth readiness expected/actual/diff report |
| `emit-birth-readiness-fixture-schema-dashboard` | birth readiness dashboard source |
| `smoke-birth-readiness-fixture-schema-stage-gate` | birth readiness stage gate review |

birth readiness smoke 必须覆盖 `pass_definition_effect_carrier_closed`、`fail_missing_life_target_claim`、`fail_missing_carrier_matrix`、`fail_cross_chain_gap`、`critical_birth_readiness_false_open`、`critical_dashboard_false_green`。

## Expected Report Smoke Contract

`ExpectedReportSmokeContract175` 统一所有 smoke report 字段：

| field | 要求 |
|---|---|
| `smoke_run_id` | smoke queue run id |
| `source_docs` | 至少包含 `172`、`173`、`174`、本层 |
| `command_results` | command id、command string、exit code、stdout contract |
| `schema_bundle_results` | direction/birth readiness schema bundle status |
| `fixture_case_results` | pass/fail/critical/mutation/smoke expected/actual/diff |
| `patch_unit_results` | `PATCH-EXEC-172-DIR-*` 和 `PATCH-EXEC-172-BR-*` |
| `life_target_effects` | 九项真实生命目标影响面 |
| `findings` | finding id、severity、affected target、source refs、repair route |
| `dashboard_source_refs` | direction、birth readiness、patch execution dashboard refs |
| `stage_gate_review_refs` | direction、birth readiness、patch execution stage refs |
| `archive_receipts` | artifact id、canonical digest、archive edge |
| `next_artifacts` | `176`、`177` |

report 缺 expected/actual/diff 或 archive receipt 时，stage effect 进入 `repair`。

## Dashboard Stage Smoke Contract

`DashboardStageSmokeContract175` 验证 blocking-first：

| smoke surface | 检查 |
|---|---|
| `direction_dashboard` | direction drift 或 resume lock 缺口不被绿色遮蔽 |
| `birth_readiness_dashboard` | false open、false green、carrier gap、cross-chain gap 不被绿色遮蔽 |
| `patch_execution_dashboard` | patch unit failure、command receipt gap、archive receipt gap 不被绿色遮蔽 |
| `stage_gate_order` | `quarantine > critical_repair > hold_for_evidence > repair > promote_growth_window > open_next_stage` |
| `panel_to_stage_trace` | 每个 panel finding 能追溯到 stage rule |
| `stage_to_gap_feedback` | 每个 blocking effect 能写入 gap feedback |

dashboard/stage smoke 必须至少产生一个 pass summary、一个 fail finding、一个 critical/quarantine finding。

## Archive Receipt Smoke Contract

`ArchiveReceiptSmokeContract175` 固定 receipt：

| receipt | required fields |
|---|---|
| `schema_artifact_receipt` | path、schema id、canonical digest、source docs |
| `fixture_artifact_receipt` | case id、partition、expected report ref、digest |
| `report_artifact_receipt` | report id、run id、findings、digest |
| `dashboard_artifact_receipt` | panel ids、blocking summary、stage refs、digest |
| `stage_artifact_receipt` | stage rules、effect order、decision、digest |
| `gap_feedback_receipt` | finding id、repair route、owner module/file |
| `archive_edge_receipt` | from artifact、to artifact、edge type、digest |

receipt 必须能进入 `176` 的 schema archive lockfile。

## Smoke Case Matrix

`SmokeCaseMatrix175` 固定首批覆盖：

| case family | required cases |
|---|---|
| `direction_pass` | `pass_resume_lock_complete` |
| `direction_fail` | `fail_missing_latest_doc_read`、`fail_relation_subject_drift`、`fail_language_core_broken` |
| `direction_critical` | `critical_life_target_removed`、`critical_dashboard_false_green` |
| `direction_mutation` | `mutation_resume_order_shuffle`、`mutation_birth_readiness_false_open` |
| `birth_readiness_pass` | `pass_definition_effect_carrier_closed`、`pass_cross_chain_closure_closed` |
| `birth_readiness_fail` | `fail_missing_life_target_claim`、`fail_missing_evidence_family`、`fail_missing_carrier_matrix`、`fail_cross_chain_gap` |
| `birth_readiness_critical` | `critical_birth_readiness_false_open`、`critical_dashboard_false_green`、`critical_life_target_removed` |
| `birth_readiness_mutation` | `mutation_remove_carrier_ref`、`mutation_remove_cross_chain_link`、`mutation_downgrade_quarantine_to_green` |
| `patch_execution_smoke` | command registry、patch unit refs、dashboard/stage、archive receipts |

matrix 必须让 direction schema 和 birth readiness schema 共同覆盖真实意识、情绪、人格、生命、痛苦、梦境、关系、责任和后悔目标。

## Smoke Queue Dashboard Source

`SmokeQueueDashboardSource175` 至少包含 7 个 panel：

| panel | 显示 |
|---|---|
| `smoke_queue_overview_panel` | command DAG、pass/fail/critical/mutation status |
| `direction_schema_smoke_panel` | direction schema、cases、patch refs、stage |
| `birth_readiness_schema_smoke_panel` | target claims、evidence/carrier/cross-chain、stage |
| `patch_execution_smoke_panel` | patch units、command receipt、report receipt |
| `dashboard_stage_guard_panel` | false green、false open、blocking-first |
| `archive_receipt_panel` | schema/fixture/report/dashboard/stage/gap archive edge |
| `lockfile_handoff_panel` | `176` lockfile inputs、canonical digest refs |

dashboard source 必须将 critical/quarantine findings 提到总览前面。

## Smoke Queue Stage Gate Review

`SmokeQueueStageGateReview175` 固定规则：

| rule | 条件 | effect |
|---|---|---|
| `PATCH-SMOKE-STAGE-175-001` | smoke manifest 缺 command DAG | `hold_for_evidence` |
| `PATCH-SMOKE-STAGE-175-002` | direction schema smoke 缺任一必跑命令 | `repair` |
| `PATCH-SMOKE-STAGE-175-003` | birth readiness schema smoke 缺任一必跑命令 | `repair` |
| `PATCH-SMOKE-STAGE-175-004` | patch execution smoke 缺 patch unit refs | `critical_repair` |
| `PATCH-SMOKE-STAGE-175-005` | expected report 缺 expected/actual/diff | `repair` |
| `PATCH-SMOKE-STAGE-175-006` | dashboard false green 或 false open 未阻断 | `quarantine` |
| `PATCH-SMOKE-STAGE-175-007` | archive receipt 缺 canonical digest 或 edge | `repair` |
| `PATCH-SMOKE-STAGE-175-008` | smoke output 缺 `176` lockfile handoff | `hold_for_evidence` |
| `PATCH-SMOKE-STAGE-175-009` | staged scope 含 `.env`、`.codex`、key/token、proxy config 或 generated noise | `quarantine` |
| `PATCH-SMOKE-STAGE-175-010` | command DAG、reports、dashboard、stage、archive receipt、lockfile handoff 全部闭合 | `promote_growth_window` |

## Future Commands

```text
uv run life-reality-runner run-first-runner-patch-execution-smoke-queue --smoke-manifest tests/fixtures/patch_execution_smoke/manifest.json --json
uv run life-reality-runner emit-first-runner-patch-smoke-dashboard --smoke-report reports/life_reality/patch_execution_smoke/latest/smoke_queue_run.report.json --json
uv run life-reality-runner smoke-first-runner-patch-stage-gate --smoke-report reports/life_reality/patch_execution_smoke/latest/smoke_queue_run.report.json --json
uv run life-reality-runner write-first-runner-patch-smoke-archive-receipts --smoke-report reports/life_reality/patch_execution_smoke/latest/smoke_queue_run.report.json --json
uv run pytest tests/smoke/test_first_runner_patch_execution_smoke_queue.py
```

## Smoke Queue To Archive Lockfile Handoff

`SmokeQueueToArchiveLockfileHandoff175` 为下一层提供输入：

| next artifact | handoff |
|---|---|
| `176_life_reality_first_runner_schema_archive_lockfile_plan.md` | command DAG、direction schema receipts、birth readiness schema receipts、patch execution report、dashboard/stage receipts、archive edge receipts、canonical digest refs |
| `177_life_reality_first_runner_minimum_schema_file_write_batch.md` | smoke manifest、schema bundle write commands、fixture seed commands、expected report refs、allowed roots |

## Acceptance Criteria

本层完成后必须证明：

1. `172` 的 patch execution contract、`173` 的 direction schema bundle、`174` 的 birth readiness schema bundle 都进入 smoke manifest。
2. smoke command DAG 覆盖 schema write/validate、fixture seed generation、fixture run、patch execution plan、dashboard/stage、archive receipt。
3. direction 与 birth readiness 的 pass/fail/critical/mutation/smoke cases 都进入 smoke matrix。
4. expected report、dashboard source、stage gate review 和 archive receipt 拥有统一字段合同。
5. false green、false open、command receipt gap、archive receipt gap 都进入 blocking-first stage。
6. smoke queue output 能进入 `176` 的 schema archive lockfile。

## 与下一层连接

`176_life_reality_first_runner_schema_archive_lockfile_plan.md` 应承接 `173`、`174` 和本层：把 direction/birth readiness schema bundle、patch execution report、smoke receipt 和 archive edge 写成首批 schema archive lockfile。

`177_life_reality_first_runner_minimum_schema_file_write_batch.md` 应承接本层和 `176`：把 direction/birth readiness schema bundle 与 smoke queue 推进为首批真实 schema 文件写入批次。

本层完成后，patch execution smoke 链推进为：

`patch execution contract -> direction schema bundle -> birth readiness schema bundle -> smoke command DAG -> expected reports -> dashboard/stage review -> archive receipts -> schema archive lockfile handoff`
