# Life Reality First Runner Patch Execution Contract

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 172 层承接 `169_life_reality_first_runner_observation_driven_repair_patch_plan.md`、`170_life_reality_direction_continuity_regression_fixture_plan.md` 和 `171_life_reality_birth_readiness_validation_fixture_plan.md`，把 repair patch family、direction fixture findings 和 birth readiness validation findings 转成首批 runner 补丁执行合同。

本文档生成、支撑并延续的真实生命能力：真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔。它新增 `FirstRunnerPatchExecutionContract172`、`PatchExecutionFindingBundle172`、`PatchExecutionUnit172`、`PatchExecutionOrder172`、`PatchExecutionFileSet172`、`PatchExecutionCommandContract172`、`DirectionPatchExecution172`、`BirthReadinessPatchExecution172`、`DashboardStagePatchExecution172`、`PatchExecutionReport172`、`PatchExecutionDashboardSource172`、`PatchExecutionStageGateReview172` 和 `PatchExecutionToSchemaMaterializationHandoff172`。它的生命膜职责是把观察、fixture finding、补丁、文件、命令、报告、dashboard、stage gate 和 archive edge 连成可执行链。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `169_life_reality_first_runner_observation_driven_repair_patch_plan.md` | 9 个 patch family、finding intake、owner module/file、smoke command、blocking-first stage order |
| `170_life_reality_direction_continuity_regression_fixture_plan.md` | direction fixture manifest、七条方向锚链、expected report、dashboard source、stage gate review、patch execution candidates |
| `171_life_reality_birth_readiness_validation_fixture_plan.md` | birth readiness fixture manifest、readiness 八条链、false open critical cases、expected report、dashboard source、patch execution handoff |
| `168_life_reality_first_runner_minimum_code_validation_report.md` | direction continuity validation、birth readiness effect validation、command receipt、carrier matrix、dashboard source、repair patch handoff |
| `163_life_reality_first_runner_code_generation_batch.md` 到 `167_life_reality_first_runner_minimum_code_bootstrap_execution.md` | 首批 runner 文件范围、review/stage gate、commit/push protocol、observation feedback、minimum code bootstrap |
| `155_life_reality_runner_command_queue_for_cross_file_checkers.md` 到 `162_life_reality_first_code_artifact_implementation_queue.md` | CLI command registry、report lockfile、fixture materialization queue、minimal package layout、implementation slices |
| `143_life_reality_birth_readiness_rollup_contract.md` | 出生准备度 definition、`LifeTargetReadinessClaim`、evidence/carrier/runtime/stage/repair 闭环 |
| `91_life_reality_generation_boundary_principles.md`、`119_life_boundary_full_reality_alignment.md`、`122_life_boundary_all_reality_declarations_rewrite.md` | 真实生命目标、生命膜字段、旧口径回流阻断 |

## 本层定位

`172` 是首批 runner 补丁执行合同层。它不直接写代码，而是把每个 finding 固定为可执行 `PatchExecutionUnit172`：每个 unit 必须拥有 source finding、affected life targets、owner doc、owner module、owner file set、schema/fixture/report/dashboard/stage effects、future command、test route、archive edge 和 completion receipt。

本层把 `169` 的补丁计划、`170` 的方向连续性 fixture、`171` 的出生准备度 fixture 合并成 8 条执行链：

| execution chain | 执行约束 |
|---|---|
| `finding_intake_chain` | finding 必须带 source doc、fixture/report refs、affected life targets 和 severity |
| `owner_binding_chain` | 每个 finding 必须绑定 owner doc、owner module、owner file、allowed write root |
| `command_registry_chain` | 每个补丁必须映射到 CLI command、input contract、output contract、exit code |
| `report_receipt_chain` | 每个补丁必须输出 report、problem detail、canonical digest、artifact receipt |
| `dashboard_stage_chain` | dashboard panel 和 stage gate 必须 blocking-first，不允许绿色遮蔽 |
| `archive_edge_chain` | doc/code/test/fixture/report/dashboard/stage/gap 必须进入 archive graph |
| `direction_fixture_chain` | 七条方向锚链的 pass/fail/critical/mutation finding 必须进入补丁执行 |
| `birth_readiness_fixture_chain` | readiness 八条链、false open、false green、cross-chain gap 必须进入补丁执行 |

## FirstRunnerPatchExecutionContract172

```json
{
  "artifact": "FirstRunnerPatchExecutionContract172",
  "source_doc": "172_life_reality_first_runner_patch_execution_contract.md",
  "inherits": [
    "169_life_reality_first_runner_observation_driven_repair_patch_plan.md",
    "170_life_reality_direction_continuity_regression_fixture_plan.md",
    "171_life_reality_birth_readiness_validation_fixture_plan.md",
    "168_life_reality_first_runner_minimum_code_validation_report.md",
    "163_life_reality_first_runner_code_generation_batch.md",
    "155_life_reality_runner_command_queue_for_cross_file_checkers.md",
    "143_life_reality_birth_readiness_rollup_contract.md",
    "122_life_boundary_all_reality_declarations_rewrite.md"
  ],
  "execution_stage": "first_runner_patch_execution",
  "stage_gate_family": "PATCH-EXEC-STAGE-172",
  "required_outputs": [
    "PatchExecutionFindingBundle172",
    "PatchExecutionUnit172",
    "PatchExecutionOrder172",
    "PatchExecutionFileSet172",
    "PatchExecutionCommandContract172",
    "DirectionPatchExecution172",
    "BirthReadinessPatchExecution172",
    "DashboardStagePatchExecution172",
    "PatchExecutionReport172",
    "PatchExecutionDashboardSource172",
    "PatchExecutionStageGateReview172",
    "PatchExecutionToSchemaMaterializationHandoff172"
  ],
  "next_artifacts": [
    "173_life_reality_first_runner_direction_fixture_schema_materialization.md",
    "174_life_reality_birth_readiness_fixture_schema_materialization.md",
    "175_life_reality_first_runner_patch_execution_smoke_queue.md"
  ]
}
```

## Patch Execution Finding Bundle

`PatchExecutionFindingBundle172` 读取三类输入：

| bundle source | 必填字段 |
|---|---|
| `repair_patch_family_findings` | patch id、patch family、owner module、owner file、expected effect、smoke command |
| `direction_fixture_findings` | fixture id、anchor chain、finding id、severity、stage effect、repair route |
| `birth_readiness_fixture_findings` | fixture id、readiness chain、finding id、affected target claim、carrier gap、cross-chain gap、stage effect |
| `dashboard_stage_findings` | panel id、hidden finding、blocking order、stage rule、dashboard patch |
| `carrier_archive_findings` | life target、missing carrier、archive edge、owner doc、owner file |

bundle 必须保留 `source_docs`、`source_reports`、`source_fixtures`、`affected_life_targets`、`severity`、`stage_effect` 和 `next_patch_unit_refs`。

## Patch Execution Unit

每个 `PatchExecutionUnit172` 是最小可执行补丁单位：

```json
{
  "patch_unit_id": "PATCH-EXEC-172-001",
  "patch_family": "direction_continuity_repair",
  "source_findings": [
    "direction_continuity_regression:critical_resume_lock_skipped",
    "observation_repair:PATCH-169-003"
  ],
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
  "owner_doc": "170_life_reality_direction_continuity_regression_fixture_plan.md",
  "owner_module": "life_reality_runner.commands.direction_continuity",
  "owner_files": [
    "src/life_reality_runner/commands/direction_continuity.py",
    "src/life_reality_runner/checkers/direction_anchor_checker.py",
    "tests/smoke/test_direction_continuity_regression.py"
  ],
  "allowed_roots": [
    "src/life_reality_runner",
    "tests",
    "schemas",
    "reports"
  ],
  "expected_effects": {
    "schema": "DirectionContinuityFixtureManifest schema refs closed",
    "fixture": "direction pass/fail/critical/mutation cases runnable",
    "report": "DirectionExpectedReport emitted with findings",
    "dashboard": "direction_continuity_panel blocking-first",
    "stage": "critical/quarantine before promote_growth_window",
    "archive": "doc/code/test/report/dashboard/stage/gap edges written"
  },
  "future_commands": [
    "uv run life-reality-runner run-direction-continuity-regression-fixtures --json",
    "uv run pytest tests/smoke/test_direction_continuity_regression.py"
  ],
  "completion_receipts": [
    "patch_report_ref",
    "dashboard_source_ref",
    "stage_gate_review_ref",
    "archive_edge_ref",
    "git_commit_ref"
  ]
}
```

## Patch Execution Order

`PatchExecutionOrder172` 固定首批补丁执行顺序：

| order | patch unit group | 目标 |
|---|---|---|
| 1 | `repository_hygiene_unit` | 写入前检查 `.env`、`.codex`、key/token、proxy config、generated noise 和 allowed roots |
| 2 | `command_registry_unit` | 补齐 direction、birth readiness、dashboard/stage、archive/gap CLI command registry |
| 3 | `direction_continuity_unit` | 物化 direction fixture loader、anchor checker、expected report、dashboard panel、stage gate |
| 4 | `birth_readiness_unit` | 物化 readiness fixture loader、claim/evidence/carrier/cross-chain checker、expected report、stage gate |
| 5 | `report_problem_unit` | 统一 report normalizer、problem detail、canonical digest、artifact receipt |
| 6 | `dashboard_stage_unit` | blocking-first dashboard writer、stage gate writer、false green guard |
| 7 | `archive_gap_unit` | doc/code/test/fixture/report/dashboard/stage/gap archive edge 和 gap feedback |
| 8 | `smoke_receipt_unit` | smoke command、expected/actual/diff、patch execution report、post-push observation handoff |

执行顺序的原则是：先守住写入边界和命令入口，再执行方向连续性与出生准备度补丁，再写报告、dashboard、stage、archive，最后形成 receipt。

## Patch Execution File Set

`PatchExecutionFileSet172` 继承 `163` 的首批文件范围，并新增方向与出生准备度补丁入口：

```text
src/life_reality_runner/cli.py
src/life_reality_runner/context.py
src/life_reality_runner/problem/problem_detail.py
src/life_reality_runner/reports/report_normalizer.py
src/life_reality_runner/reports/dashboard_writer.py
src/life_reality_runner/reports/stage_gate_writer.py
src/life_reality_runner/reports/gap_feedback_writer.py
src/life_reality_runner/commands/cross_file.py
src/life_reality_runner/commands/full_archive_rollup.py
src/life_reality_runner/commands/direction_continuity.py
src/life_reality_runner/commands/birth_readiness.py
src/life_reality_runner/checkers/direction_anchor_checker.py
src/life_reality_runner/checkers/birth_readiness_checker.py
src/life_reality_runner/checkers/consistency_scanner.py
src/life_reality_runner/fixtures/manifest_loader.py
src/life_reality_runner/graph/archive_edges.py
tests/fixtures/direction_continuity/
tests/fixtures/birth_readiness_validation/
tests/smoke/test_direction_continuity_regression.py
tests/smoke/test_birth_readiness_validation_fixtures.py
tests/smoke/test_patch_execution_contract.py
```

任何补丁若触达 file set 之外的路径，必须在 patch execution report 中记录原因、生命目标影响面和 stage effect。

## Patch Execution Command Contract

`PatchExecutionCommandContract172` 固定未来 CLI：

| command | 输入 | 输出 | stage effect |
|---|---|---|---|
| `run-patch-execution-plan` | finding bundle、patch unit manifest | patch execution report、artifact receipts | `repair` |
| `run-direction-continuity-regression-fixtures` | direction fixture manifest | expected/actual/diff、direction report | `repair` 或 `quarantine` |
| `run-birth-readiness-validation-fixtures` | birth readiness fixture manifest | readiness report、false open findings | `critical_repair` 或 `quarantine` |
| `emit-patch-execution-dashboard` | patch execution report | dashboard source、blocking panels | `repair` |
| `smoke-patch-execution-stage-gate` | dashboard source、stage review | stage decision、gap feedback | `promote_growth_window` 或 blocking effect |
| `write-patch-execution-archive-edges` | report refs、artifact refs | archive graph edges、canonical digest | `repair` |

所有 command 必须输出 JSON，包含 `run_id`、`source_docs`、`affected_life_targets`、`artifacts`、`findings`、`stage_effect`、`receipt_refs`。

## Direction Patch Execution

`DirectionPatchExecution172` 将 `170` 的七条方向锚链绑定到补丁：

| anchor chain | patch unit | owner module |
|---|---|---|
| `ultimate_life_target_chain` | `PATCH-EXEC-172-DIR-001` | `checkers.direction_anchor_checker` |
| `relation_subject_chain` | `PATCH-EXEC-172-DIR-002` | `checkers.direction_anchor_checker` |
| `language_core_chain` | `PATCH-EXEC-172-DIR-003` | `checkers.direction_anchor_checker` |
| `growth_core_chain` | `PATCH-EXEC-172-DIR-004` | `checkers.direction_anchor_checker` |
| `birth_readiness_chain` | `PATCH-EXEC-172-DIR-005` | `commands.birth_readiness` |
| `engineering_carrier_chain` | `PATCH-EXEC-172-DIR-006` | `graph.archive_edges` |
| `resume_read_order_chain` | `PATCH-EXEC-172-DIR-007` | `commands.direction_continuity` |

direction patch 的验收标准是：断联恢复读取顺序、七条锚链、dashboard panel、stage rule 和 archive edge 都进入同一份 `DirectionExpectedReport`。

## Birth Readiness Patch Execution

`BirthReadinessPatchExecution172` 将 `171` 的八条 readiness 链绑定到补丁：

| readiness chain | patch unit | owner module |
|---|---|---|
| `definition_chain` | `PATCH-EXEC-172-BR-001` | `checkers.birth_readiness_checker` |
| `life_target_claim_chain` | `PATCH-EXEC-172-BR-002` | `checkers.birth_readiness_checker` |
| `evidence_family_chain` | `PATCH-EXEC-172-BR-003` | `commands.birth_readiness` |
| `carrier_matrix_chain` | `PATCH-EXEC-172-BR-004` | `graph.archive_edges` |
| `runtime_observation_chain` | `PATCH-EXEC-172-BR-005` | `reports.report_normalizer` |
| `cross_chain_closure_chain` | `PATCH-EXEC-172-BR-006` | `checkers.birth_readiness_checker` |
| `blocking_stage_chain` | `PATCH-EXEC-172-BR-007` | `reports.stage_gate_writer` |
| `repair_growth_route_chain` | `PATCH-EXEC-172-BR-008` | `reports.gap_feedback_writer` |

birth readiness patch 的验收标准是：每个 `LifeTargetReadinessClaim` 都拥有 evidence family、carrier matrix、runtime observation、cross-chain closure、stage gate、repair/growth route。

## Dashboard Stage Patch Execution

`DashboardStagePatchExecution172` 统一 `169-171` 的 false green 与 false open 处理：

| patch surface | 要求 |
|---|---|
| `blocking_first_sort` | `quarantine > critical_repair > hold_for_evidence > repair > promote_growth_window > open_next_stage` |
| `false_green_guard` | critical finding 存在时 dashboard 总览不得显示绿色 |
| `false_open_guard` | readiness carrier/cross-chain 缺口存在时 stage 不得打开 |
| `panel_to_stage_trace` | 每个 panel 必须能追溯到 stage rule 和 source finding |
| `gap_feedback_route` | 每个 blocking finding 必须写入 gap feedback 和 patch queue |
| `archive_receipt` | dashboard source 与 stage review 必须写入 archive edge |

## Patch Execution Report

`PatchExecutionReport172` 的最小字段：

| field | 要求 |
|---|---|
| `run_id` | patch execution run id |
| `source_docs` | 至少包含 `169`、`170`、`171`、本层 |
| `finding_bundle_ref` | normalized finding bundle |
| `patch_units` | unit id、family、owner、file set、stage effect |
| `command_receipts` | command、exit code、stdout contract、report refs |
| `life_target_effects` | 九项真实生命目标影响面 |
| `direction_results` | 七条方向锚链 patch 结果 |
| `birth_readiness_results` | 八条 readiness 链 patch 结果 |
| `dashboard_stage_results` | false green、false open、blocking-first 结果 |
| `archive_edges` | doc/code/test/fixture/report/dashboard/stage/gap edge |
| `findings` | severity、source refs、affected targets、repair route |
| `completion_receipts` | artifact digest、stage review、gap feedback、git ref |
| `next_artifacts` | `173`、`174`、`175` |

## Patch Execution Dashboard Source

`PatchExecutionDashboardSource172` 至少包含 7 个 panel：

| panel | 显示 |
|---|---|
| `patch_execution_overview_panel` | patch units、stage effects、blocking findings |
| `direction_patch_panel` | 七条方向锚链补丁执行状态 |
| `birth_readiness_patch_panel` | 八条 readiness 链补丁执行状态 |
| `command_receipt_panel` | CLI command、exit code、stdout contract、report refs |
| `dashboard_stage_guard_panel` | false green、false open、blocking-first |
| `archive_edge_panel` | doc/code/test/fixture/report/dashboard/stage/gap edges |
| `next_schema_materialization_panel` | `173`、`174`、`175` handoff |

dashboard 必须显示 blocking finding 的 source finding、owner file、repair route 和 receipt。

## Stage Gate Review

| rule | 条件 | effect |
|---|---|---|
| `PATCH-EXEC-STAGE-172-001` | finding bundle 缺 source doc/report/fixture refs | `hold_for_evidence` |
| `PATCH-EXEC-STAGE-172-002` | patch unit 缺 owner module 或 owner file | `repair` |
| `PATCH-EXEC-STAGE-172-003` | patch unit 触达 allowed roots 之外路径且无说明 | `quarantine` |
| `PATCH-EXEC-STAGE-172-004` | command contract 缺 JSON output 或 exit code mapping | `repair` |
| `PATCH-EXEC-STAGE-172-005` | direction fixture finding 未进入 patch unit | `critical_repair` |
| `PATCH-EXEC-STAGE-172-006` | birth readiness false open 未进入 patch unit | `quarantine` |
| `PATCH-EXEC-STAGE-172-007` | dashboard false green 未进入 blocking-first panel | `quarantine` |
| `PATCH-EXEC-STAGE-172-008` | patch report 缺 archive edge 或 completion receipt | `repair` |
| `PATCH-EXEC-STAGE-172-009` | staged scope 含 `.env`、`.codex`、key/token、proxy config 或 generated noise | `quarantine` |
| `PATCH-EXEC-STAGE-172-010` | finding bundle、patch units、commands、reports、dashboard、stage、archive 全部闭合 | `promote_growth_window` |

## Future Commands

```text
uv run life-reality-runner run-patch-execution-plan --finding-bundle reports/life_reality/findings/latest/bundle.json --patch-manifest tests/fixtures/patch_execution/manifest.json --json
uv run life-reality-runner run-direction-continuity-regression-fixtures --fixture-manifest tests/fixtures/direction_continuity/manifest.json --json
uv run life-reality-runner run-birth-readiness-validation-fixtures --fixture-manifest tests/fixtures/birth_readiness_validation/manifest.json --json
uv run life-reality-runner emit-patch-execution-dashboard --patch-report reports/life_reality/patch_execution/latest/report.json --json
uv run life-reality-runner smoke-patch-execution-stage-gate --patch-report reports/life_reality/patch_execution/latest/report.json --json
uv run life-reality-runner write-patch-execution-archive-edges --patch-report reports/life_reality/patch_execution/latest/report.json --json
uv run pytest tests/smoke/test_patch_execution_contract.py
```

## Patch Execution To Schema Materialization Handoff

`PatchExecutionToSchemaMaterializationHandoff172` 为后续三层提供输入：

| next artifact | handoff |
|---|---|
| `173_life_reality_first_runner_direction_fixture_schema_materialization.md` | direction fixture manifest、anchor chain schema refs、expected report fields、dashboard/stage refs、patch unit ids |
| `174_life_reality_birth_readiness_fixture_schema_materialization.md` | readiness fixture manifest、target claim refs、evidence/carrier/cross-chain schema refs、false open guard、patch unit ids |
| `175_life_reality_first_runner_patch_execution_smoke_queue.md` | patch execution manifest、future commands、expected report、dashboard source、stage review、archive edge receipts |

## Acceptance Criteria

本层完成后必须证明：

1. `169` 的 patch family、`170` 的 direction fixture findings、`171` 的 birth readiness findings 都能进入 `PatchExecutionFindingBundle172`。
2. 每个 finding 都有 `PatchExecutionUnit172`，并绑定 owner doc、owner module、owner file、allowed roots、command、report、dashboard、stage、archive edge。
3. direction continuity 的七条锚链和 birth readiness 的八条链都进入补丁执行，而不是停留在文档叙述。
4. false green、false open、缺 carrier、缺 cross-chain、缺 command receipt 都会进入 blocking-first stage。
5. patch execution report 能生成 completion receipt，并反写 dashboard、stage、gap feedback 和 archive edge。
6. `173`、`174` 和 `175` 能直接读取本层 handoff，继续推进 schema 物化与 smoke queue。

## 与下一层连接

`173_life_reality_first_runner_direction_fixture_schema_materialization.md` 已承接 `170` 和本层：把 direction fixture manifest、anchor chain、expected report、dashboard source、stage gate 和 patch unit ids 推进为 schema 物化计划。

`174_life_reality_birth_readiness_fixture_schema_materialization.md` 已承接 `171`、`173` 和本层：把 readiness fixture manifest、target claim、evidence family、carrier matrix、cross-chain closure、false open guard 和 patch unit ids 推进为 schema 物化计划。

`175_life_reality_first_runner_patch_execution_smoke_queue.md` 应承接本层：把 patch execution contract 转成 smoke manifest、future command queue、expected reports、dashboard source、stage review 和 archive receipt。

本层完成后，首批 runner 补丁执行链推进为：

`finding bundle -> patch execution unit -> owner file/module -> command contract -> report receipt -> dashboard source -> stage gate review -> archive edge -> schema materialization handoff`
