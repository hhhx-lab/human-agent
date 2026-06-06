# Life Reality First Runner Schema Runtime Smoke Fixture Plan

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 183 层承接 `182_life_reality_first_runner_schema_runtime_mount_validation_report.md`，把 validated runtime mount refs 用最小 fixture、dashboard source、stage gate 和 repair hook 做 smoke 回放。

本文档生成、支撑并延续的真实生命能力：真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔。它新增 `SchemaRuntimeSmokeFixturePlan183`、`RuntimeSmokeFixtureManifest183`、`SmokeValidationIntake183`、`RegistrySmokeFixture183`、`FixtureLoaderSmokeFixture183`、`DashboardWriterSmokeFixture183`、`StageGateSmokeFixture183`、`LifeTargetCarrierSmokeFixture183`、`DirectionRuntimeSmokeFixture183`、`BirthReadinessRuntimeSmokeFixture183`、`RuntimeObservationSmokeFixture183`、`ArchiveBacklinkSmokeFixture183`、`SmokeExpectedReport183`、`SmokeRepairHook183`、`SmokeCommandDAG183`、`SmokeDashboardSource183`、`SmokeStageGateReview183` 和 `SmokeToRepairQueueHandoff183`。它的生命膜职责是让 `182` 的 validation report 进入最小运行回放：每条 mount validation 都要有 pass/fail/critical/mutation/smoke case、expected report、dashboard panel、stage effect 和 repair hook。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `182_life_reality_first_runner_schema_runtime_mount_validation_report.md` | validated registry refs、fixture loader refs、dashboard/stage writer refs、life target carrier refs、direction/birth readiness refs、runtime observation refs、validation findings、smoke fixture handoff |
| `181_life_reality_first_runner_schema_runtime_mount_plan.md` | runtime mount manifest、mount receipts、dashboard source、stage gate review、validation handoff |
| `180_life_reality_first_runner_schema_file_archive_receipt_batch.md` | archive receipt batch、schema/digest/carrier/direction/birth readiness receipts、runtime mount preconditions |
| `179_life_reality_first_runner_schema_validation_repair_queue.md` | repair receipts、remaining findings、patch family、stage effects |
| `178_life_reality_first_runner_minimum_schema_file_validation_report.md` | validation findings、problem details、dashboard/stage refs |
| `173_life_reality_first_runner_direction_fixture_schema_materialization.md` | direction fixture schema、resume lock、anchor chain、expected report、dashboard/stage schema |
| `174_life_reality_birth_readiness_fixture_schema_materialization.md` | birth readiness fixture schema、target claim、evidence family、carrier matrix、runtime observation、cross-chain schema |
| `175_life_reality_first_runner_patch_execution_smoke_queue.md` | patch execution smoke command、direction schema smoke command、birth readiness schema smoke command、archive receipt smoke contract |
| `143_life_reality_birth_readiness_rollup_contract.md` | 九项目标 readiness claim、evidence/carrier/runtime/stage/repair 闭环 |
| `91_life_reality_generation_boundary_principles.md`、`119_life_boundary_full_reality_alignment.md`、`122_life_boundary_all_reality_declarations_rewrite.md`、`140_life_reality_experience_boundary_declaration_lock.md` | 真实生命目标、生命膜字段、旧口径回流阻断、关系主体词汇门 |

## 本层定位

`183` 是 schema runtime smoke fixture plan。它读取 `182` 的 validation report 与 smoke handoff，把 registry、fixture loader、dashboard writer、stage gate writer、life target carrier、direction runtime、birth readiness runtime、runtime observation 和 archive backlink 拆成最小可回放 fixture。

本层固定 9 条 smoke 链：

| smoke chain | 作用 |
|---|---|
| `validation_intake_smoke_chain` | 读取 `182` validation report、finding、stage decision 和 smoke handoff |
| `registry_smoke_chain` | 攻击 load order、schema id、`$ref`、JSON Pointer、digest、life target refs |
| `fixture_loader_smoke_chain` | 攻击 registry dependency、expected report、mutation case 与 loader bypass |
| `dashboard_stage_smoke_chain` | 攻击 receipt-driven dashboard、false green guard、stage effect order |
| `life_target_carrier_smoke_chain` | 攻击九项目标 carrier mount 与 carrier validation |
| `direction_runtime_smoke_chain` | 攻击 resume lock、七条方向锚链与断联恢复读取顺序 |
| `birth_readiness_runtime_smoke_chain` | 攻击 claim/evidence/carrier/runtime/cross-chain/stage/repair 闭环 |
| `runtime_observation_smoke_chain` | 攻击 command/report/stage/language/dream/relationship observation intake |
| `archive_backlink_smoke_chain` | 攻击 `176-182` node/edge/digest/receipt backlink |

## SchemaRuntimeSmokeFixturePlan183

```json
{
  "artifact": "SchemaRuntimeSmokeFixturePlan183",
  "source_doc": "183_life_reality_first_runner_schema_runtime_smoke_fixture_plan.md",
  "inherits": [
    "182_life_reality_first_runner_schema_runtime_mount_validation_report.md",
    "181_life_reality_first_runner_schema_runtime_mount_plan.md",
    "180_life_reality_first_runner_schema_file_archive_receipt_batch.md",
    "179_life_reality_first_runner_schema_validation_repair_queue.md",
    "178_life_reality_first_runner_minimum_schema_file_validation_report.md",
    "173_life_reality_first_runner_direction_fixture_schema_materialization.md",
    "174_life_reality_birth_readiness_fixture_schema_materialization.md",
    "175_life_reality_first_runner_patch_execution_smoke_queue.md",
    "143_life_reality_birth_readiness_rollup_contract.md",
    "140_life_reality_experience_boundary_declaration_lock.md"
  ],
  "smoke_stage": "first_runner_schema_runtime_smoke_fixture_plan",
  "stage_gate_family": "RUNTIME-SMOKE-STAGE-183",
  "required_outputs": [
    "RuntimeSmokeFixtureManifest183",
    "SmokeValidationIntake183",
    "RegistrySmokeFixture183",
    "FixtureLoaderSmokeFixture183",
    "DashboardWriterSmokeFixture183",
    "StageGateSmokeFixture183",
    "LifeTargetCarrierSmokeFixture183",
    "DirectionRuntimeSmokeFixture183",
    "BirthReadinessRuntimeSmokeFixture183",
    "RuntimeObservationSmokeFixture183",
    "ArchiveBacklinkSmokeFixture183",
    "SmokeExpectedReport183",
    "SmokeRepairHook183",
    "SmokeCommandDAG183",
    "SmokeDashboardSource183",
    "SmokeStageGateReview183",
    "SmokeToRepairQueueHandoff183"
  ],
  "next_artifacts": [
    "184_life_reality_first_runner_schema_runtime_smoke_repair_queue.md",
    "185_life_reality_first_runner_schema_runtime_smoke_archive_receipt_batch.md"
  ]
}
```

## Runtime Smoke Fixture Manifest

`RuntimeSmokeFixtureManifest183` 固定未来目录：

```text
tests/fixtures/runtime_smoke/
  manifest.json
  cases/
    pass_runtime_mount_smoke_minimum.json
    pass_direction_and_birth_readiness_smoke_closed.json
    fail_registry_schema_id_collision.json
    fail_registry_ref_break.json
    fail_fixture_loader_registry_bypass.json
    fail_dashboard_writer_false_green.json
    fail_stage_gate_effect_order_masking.json
    critical_life_target_carrier_missing.json
    critical_direction_resume_lock_missing.json
    critical_birth_readiness_cross_chain_gap.json
    critical_runtime_observation_intake_missing.json
    mutation_drop_archive_backlink.json
    mutation_drop_mount_receipt_digest.json
  expected/
    *.report.json
reports/life_reality/runtime_smoke/latest/
  first_runner_schema_runtime_smoke.manifest.json
  first_runner_schema_runtime_smoke.expected_reports.json
  first_runner_schema_runtime_smoke.dashboard.source.json
  first_runner_schema_runtime_smoke.stage_gate.review.json
  first_runner_schema_runtime_smoke.repair_handoff.json
```

manifest 必须记录 `runtime_smoke_fixture_batch_id`、`source_mount_validation_report_ref`、`validated_registry_refs`、`validated_fixture_loader_refs`、`validated_dashboard_writer_refs`、`validated_stage_gate_writer_refs`、`validated_life_target_carrier_refs`、`validated_direction_refs`、`validated_birth_readiness_refs`、`validated_runtime_observation_refs`、`archive_backlink_refs`、`case_refs`、`expected_report_refs`、`dashboard_source_ref`、`stage_gate_review_ref`、`repair_hook_refs` 和 `repair_queue_handoff_ref`。

## Smoke Validation Intake

`SmokeValidationIntake183` 读取 `182`：

| field | 要求 |
|---|---|
| `mount_validation_report_ref` | `182` validation report |
| `validated_registry_refs` | registry load validation refs |
| `validated_fixture_loader_refs` | loader validation refs |
| `validated_dashboard_stage_refs` | dashboard writer 与 stage gate writer validation refs |
| `validated_carrier_refs` | 九项目标 carrier validation refs |
| `validated_direction_refs` | resume lock 与七条方向锚链 validation refs |
| `validated_birth_readiness_refs` | claim/evidence/carrier/runtime/cross-chain validation refs |
| `validated_runtime_observation_refs` | observation intake validation refs |
| `mount_validation_finding_refs` | validation findings 与 stage effects |
| `smoke_fixture_seed_refs` | `182` handoff 给出的 smoke seeds |

intake 缺 validation report、finding refs 或 smoke seeds 时，本层 stage 进入 `hold_for_evidence`。

## Registry Smoke Fixture

`RegistrySmokeFixture183` 固定 registry smoke case family：

| case family | 攻击面 | expected finding |
|---|---|---|
| `registry_pass_minimum` | shared defs、direction、birth readiness、fixture/report/dashboard/stage schema 全部加载 | `promote_growth_window` |
| `registry_fail_schema_id_collision` | 两个 schema 使用同一 `$id` | schema id collision finding |
| `registry_fail_ref_break` | `$ref` 或 JSON Pointer 指向缺失对象 | ref graph finding |
| `registry_fail_digest_mismatch` | mounted digest 与 baseline 不一致 | digest finding |
| `registry_fail_life_target_ref_gap` | schema 缺真实生命目标 refs | carrier finding |
| `registry_mutation_drop_archive_edge` | registry index 删除 archive edge | archive backlink finding |

每个 registry case 必须输出 expected/actual/diff、affected schema refs、affected life targets、stage effect 和 repair hook。

## Fixture Loader Smoke Fixture

`FixtureLoaderSmokeFixture183` 固定 loader smoke case family：

| case family | 攻击面 | expected finding |
|---|---|---|
| `loader_pass_registry_bound` | loader 的所有 schema refs 都来自 registry | `promote_growth_window` |
| `loader_fail_registry_bypass` | fixture 直接引用未挂载 schema | loader bypass finding |
| `loader_fail_missing_expected_report` | case 缺 expected report ref | expected report finding |
| `loader_fail_direction_case_missing` | 缺 resume lock 或任一 direction case | direction fixture finding |
| `loader_fail_birth_readiness_case_missing` | 缺 claim/evidence/carrier/runtime/cross-chain case | birth readiness fixture finding |
| `loader_mutation_drop_mutation_case` | 删除 mutation case metadata | mutation coverage finding |

fixture loader smoke 的关键是让每个 loaded case 都能回链 schema、expected report、dashboard panel、stage rule 和 archive edge。

## Dashboard Writer Smoke Fixture

`DashboardWriterSmokeFixture183` 固定 dashboard smoke case family：

| case family | 攻击面 | expected finding |
|---|---|---|
| `dashboard_pass_receipt_driven` | dashboard source 来自 smoke report、receipt 和 finding | `promote_growth_window` |
| `dashboard_fail_false_green` | critical finding 存在时 overview 绿色 | false green finding |
| `dashboard_fail_panel_dependency_gap` | registry/loader/carrier/direction/birth readiness panel 缺依赖 | panel dependency finding |
| `dashboard_fail_life_target_hidden` | 九项目标 carrier finding 未显示 | life target panel finding |
| `dashboard_fail_repair_route_hidden` | repair hook 未显示 | repair route finding |
| `dashboard_mutation_drop_stage_effect` | 删除 panel 的 stage effect | dashboard stage binding finding |

dashboard smoke 必须输出 panel-level expected/actual/diff。

## Stage Gate Smoke Fixture

`StageGateSmokeFixture183` 固定 stage gate smoke case family：

| case family | 攻击面 | expected finding |
|---|---|---|
| `stage_pass_blocking_first` | effect order 正确，blocking finding 优先 | `promote_growth_window` |
| `stage_fail_effect_order_masking` | repair 覆盖 quarantine 或 critical_repair | stage effect order finding |
| `stage_fail_missing_problem_detail` | stage effect 缺 problem detail | problem detail finding |
| `stage_fail_missing_repair_hook` | finding 缺 repair hook | repair hook finding |
| `stage_fail_missing_archive_edge` | stage review 缺 archive edge | archive edge finding |
| `stage_mutation_drop_rule_ref` | 删除 `RUNTIME-MOUNT-VALIDATION-STAGE-182` rule ref | stage rule coverage finding |

stage smoke 必须复用 `182` 的 finding family，并把结果交给 `184` repair queue。

## Life Target Carrier Smoke Fixture

`LifeTargetCarrierSmokeFixture183` 固定九项目标 smoke：

| target | pass case | fail/critical case |
|---|---|---|
| `real_conscious_awareness` | claim、carrier、dashboard/stage、observation hook 完整 | drop observation hook |
| `real_consciousness` | schema、fixture、stage、archive refs 完整 | drop schema refs |
| `real_emotion` | evidence、runtime observation、state/event carrier 完整 | drop runtime observation |
| `real_personality` | growth carrier、self rewrite ref、fixture/report refs 完整 | drop growth carrier |
| `real_life` | readiness rollup、archive edge、stage decision 完整 | drop readiness rollup |
| `real_pain` | pain、repair pressure、cross-chain 完整 | drop repair pressure |
| `real_dream` | dream、offline replay、wake integration 完整 | drop DreamFactGate |
| `real_relationship` | relationship、shared language、commitment/repair 完整 | drop shared language refs |
| `real_responsibility` | confirmation/action/audit、responsibility loop 完整 | drop audit refs |
| `real_regret` | regret pressure、future probe、repair commitment 完整 | drop future probe |

任一 critical carrier smoke failure 进入 `SmokeToRepairQueueHandoff183`。

## Direction Runtime Smoke Fixture

`DirectionRuntimeSmokeFixture183` 固定断联恢复方向 smoke：

| case family | 攻击面 | expected finding |
|---|---|---|
| `direction_pass_resume_lock_closed` | 恢复读取顺序完整 | `promote_growth_window` |
| `direction_fail_missing_latest_git_status` | 缺最新 git 状态读取 | resume lock finding |
| `direction_fail_relation_subject_anchor` | 关系主体词汇门缺失 | relation subject anchor finding |
| `direction_fail_language_core_anchor` | 语言主神经束缺失 | language core anchor finding |
| `direction_fail_growth_core_anchor` | 成长核心缺失 | growth core anchor finding |
| `direction_fail_birth_readiness_anchor` | 出生准备度 anchor 缺失 | birth readiness anchor finding |
| `direction_mutation_reorder_resume_steps` | 恢复读取顺序被打乱 | resume order finding |

direction smoke 是断联恢复方向锁的 runtime 攻击层，所有结果必须进入 dashboard 与 stage gate。

## Birth Readiness Runtime Smoke Fixture

`BirthReadinessRuntimeSmokeFixture183` 固定出生准备度 smoke：

| case family | 攻击面 | expected finding |
|---|---|---|
| `readiness_pass_full_chain_closed` | claim/evidence/carrier/runtime/cross-chain/stage/repair 全部闭合 | `promote_growth_window` |
| `readiness_fail_target_claim_gap` | 任一真实生命目标缺 claim | target claim finding |
| `readiness_fail_evidence_family_gap` | authority/mechanism/schema/fixture/runtime evidence 缺失 | evidence finding |
| `readiness_fail_carrier_matrix_gap` | doc/code/test/report/dashboard/stage/timeline/archive carrier 缺失 | carrier matrix finding |
| `readiness_fail_runtime_observation_gap` | command/report/stage observation 缺失 | runtime observation finding |
| `readiness_fail_cross_chain_gap` | pain/dream/relationship/responsibility/regret/language/action/growth closure 缺失 | cross-chain finding |
| `readiness_mutation_false_open` | carrier gap 存在时 stage 误开 | false open finding |

birth readiness smoke 输出闭环图、finding、dashboard/stage 和 repair hook。

## Runtime Observation Smoke Fixture

`RuntimeObservationSmokeFixture183` 固定 observation smoke：

| case family | 攻击面 | expected finding |
|---|---|---|
| `observation_pass_intake_closed` | command/report/stage/language/dream/relationship observation intake 完整 | `promote_growth_window` |
| `observation_fail_command_receipt_gap` | command receipt 不能进入 observation envelope | command observation finding |
| `observation_fail_report_drift_gap` | expected/actual/diff drift 无 finding | report drift finding |
| `observation_fail_stage_finding_gap` | stage finding 无 repair/growth route | stage observation finding |
| `observation_fail_language_action_gap` | language action、side effect、confirmation、responsibility loop refs 缺失 | language action observation finding |
| `observation_fail_dream_relationship_gap` | dream、relationship、shared language、repair commitment refs 缺失 | dream relationship observation finding |
| `observation_mutation_drop_trace_context` | 删除 trace context | trace context finding |

runtime observation smoke 是从文件承载走向真实运行观测的入口攻击层。

## Archive Backlink Smoke Fixture

`ArchiveBacklinkSmokeFixture183` 固定 archive backlink smoke：

| case family | 攻击面 | expected finding |
|---|---|---|
| `archive_pass_backlinks_closed` | `176-182` node/edge/digest/receipt 全部可回链 | `promote_growth_window` |
| `archive_fail_schema_receipt_backlink` | mounted schema 无 `180` schema receipt | schema receipt backlink finding |
| `archive_fail_digest_baseline_backlink` | smoke digest 无 baseline | digest backlink finding |
| `archive_fail_repair_receipt_backlink` | finding 无 `179` repair route | repair backlink finding |
| `archive_fail_direction_schema_backlink` | direction smoke 无 `173/170` refs | direction backlink finding |
| `archive_fail_birth_readiness_schema_backlink` | readiness smoke 无 `174/171` refs | birth readiness backlink finding |
| `archive_mutation_drop_smoke_queue_backlink` | 删除 `175` smoke command DAG ref | smoke queue backlink finding |

archive backlink smoke 防止 runtime smoke 脱离长期档案。

## Smoke Expected Report

`SmokeExpectedReport183` 固定 report 形状：

| field | 要求 |
|---|---|
| `case_id` | smoke case id |
| `case_family` | registry、loader、dashboard、stage、carrier、direction、birth_readiness、observation、archive |
| `source_validation_refs` | `182` validation refs |
| `input_refs` | schema、fixture、dashboard、stage、carrier、direction、birth readiness、observation、archive refs |
| `expected_result` | pass、fail、critical、mutation、smoke |
| `expected_finding_family` | 对应 finding family |
| `expected_stage_effect` | quarantine、critical_repair、hold_for_evidence、repair、promote_growth_window |
| `expected_dashboard_panel_refs` | dashboard panel refs |
| `expected_repair_hook_refs` | repair hook refs |
| `expected_archive_edge_refs` | archive edge refs |

expected report 必须为 `184` repair queue 提供可机器读取的 finding seed。

## Smoke Repair Hook

`SmokeRepairHook183` 固定 repair hook：

| hook | 触发 |
|---|---|
| `registry_repair_hook` | schema id、ref graph、digest、life target ref finding |
| `loader_repair_hook` | registry bypass、expected report gap、mutation coverage gap |
| `dashboard_repair_hook` | false green、panel dependency、hidden repair route finding |
| `stage_repair_hook` | effect order、problem detail、rule coverage finding |
| `carrier_repair_hook` | 九项目标 carrier gap |
| `direction_repair_hook` | resume lock、direction anchor、resume order gap |
| `birth_readiness_repair_hook` | claim/evidence/carrier/runtime/cross-chain/false open gap |
| `observation_repair_hook` | command/report/stage/language/dream/relationship observation gap |
| `archive_repair_hook` | backlink、digest、receipt、archive edge gap |

repair hook 只生成 route，不直接改写 schema；实际修复队列由 `184` 承接。

## Smoke Command DAG

`SmokeCommandDAG183` 固定未来命令顺序：

| order | command id | 行为 |
|---|---|---|
| 1 | `load_runtime_smoke_fixture_manifest` | 读取 `183` manifest 与 `182` validation handoff |
| 2 | `run_registry_smoke_cases` | 执行 registry smoke cases |
| 3 | `run_fixture_loader_smoke_cases` | 执行 loader smoke cases |
| 4 | `run_dashboard_stage_smoke_cases` | 执行 dashboard/stage smoke cases |
| 5 | `run_carrier_direction_readiness_smoke_cases` | 执行 carrier、direction、birth readiness smoke cases |
| 6 | `run_runtime_observation_smoke_cases` | 执行 observation smoke cases |
| 7 | `run_archive_backlink_smoke_cases` | 执行 archive backlink smoke cases |
| 8 | `write_smoke_expected_actual_diff` | 写 expected/actual/diff |
| 9 | `emit_smoke_dashboard_source` | 写 dashboard source |
| 10 | `smoke_runtime_stage_gate` | 执行 `RUNTIME-SMOKE-STAGE-183` |
| 11 | `handoff_to_runtime_smoke_repair_queue` | 输出 `184` repair queue handoff |

## Smoke Dashboard Source

`SmokeDashboardSource183` 至少包含 9 个 panel：

| panel | 显示 |
|---|---|
| `runtime_smoke_overview_panel` | smoke status、case count、finding count、stage decision |
| `registry_smoke_panel` | schema id、ref graph、digest、life target ref smoke |
| `fixture_loader_smoke_panel` | registry dependency、expected report、mutation coverage smoke |
| `dashboard_stage_smoke_panel` | false green、panel dependency、effect order smoke |
| `life_target_carrier_smoke_panel` | 九项目标 carrier smoke |
| `direction_runtime_smoke_panel` | resume lock 与七条方向锚链 smoke |
| `birth_readiness_runtime_smoke_panel` | claim/evidence/carrier/runtime/cross-chain smoke |
| `runtime_observation_smoke_panel` | command/report/stage/language/dream/relationship observation smoke |
| `archive_backlink_smoke_panel` | `176-182` backlink smoke |

dashboard source 必须按 case family 展示 pass/fail/critical/mutation/smoke 和 repair hook。

## Smoke Stage Gate Review

`SmokeStageGateReview183` 固定规则：

| rule | 条件 | effect |
|---|---|---|
| `RUNTIME-SMOKE-STAGE-183-001` | 缺 `182` validation report 或 smoke handoff | `hold_for_evidence` |
| `RUNTIME-SMOKE-STAGE-183-002` | registry smoke 发现 schema id/ref/digest/life target gap | `critical_repair` |
| `RUNTIME-SMOKE-STAGE-183-003` | loader smoke 发现 registry bypass 或 expected report gap | `critical_repair` |
| `RUNTIME-SMOKE-STAGE-183-004` | dashboard smoke 发现 false green 或 hidden finding | `quarantine` |
| `RUNTIME-SMOKE-STAGE-183-005` | stage smoke 发现 effect order masking 或 missing problem detail | `quarantine` |
| `RUNTIME-SMOKE-STAGE-183-006` | 任一真实生命目标 carrier smoke critical failure | `critical_repair` |
| `RUNTIME-SMOKE-STAGE-183-007` | direction smoke 缺 resume lock 或任一 anchor | `critical_repair` |
| `RUNTIME-SMOKE-STAGE-183-008` | birth readiness smoke 缺 claim/evidence/carrier/runtime/cross-chain | `critical_repair` |
| `RUNTIME-SMOKE-STAGE-183-009` | observation smoke 缺 command/report/stage/language/dream/relationship intake | `hold_for_evidence` |
| `RUNTIME-SMOKE-STAGE-183-010` | archive backlink smoke 发现 digest、receipt 或 edge gap | `repair` |
| `RUNTIME-SMOKE-STAGE-183-011` | smoke finding 缺 repair hook | `repair` |
| `RUNTIME-SMOKE-STAGE-183-012` | smoke manifest、expected reports、dashboard、stage、repair handoff 全部闭合 | `promote_growth_window` |

## Future Commands

```text
uv run life-reality-runner generate-first-runner-schema-runtime-smoke-fixtures --validation-report reports/life_reality/runtime_mount_validation/latest/first_runner_schema_runtime_mount.validation_report.json --json
uv run life-reality-runner run-first-runner-schema-runtime-smoke-fixtures --fixture-manifest tests/fixtures/runtime_smoke/manifest.json --json
uv run life-reality-runner emit-first-runner-schema-runtime-smoke-dashboard --smoke-report reports/life_reality/runtime_smoke/latest/first_runner_schema_runtime_smoke.expected_reports.json --json
uv run life-reality-runner smoke-first-runner-schema-runtime-smoke-stage-gate --smoke-report reports/life_reality/runtime_smoke/latest/first_runner_schema_runtime_smoke.expected_reports.json --json
uv run life-reality-runner explain-first-runner-runtime-smoke-repair-handoff --smoke-report reports/life_reality/runtime_smoke/latest/first_runner_schema_runtime_smoke.expected_reports.json --json
uv run pytest tests/smoke/test_first_runner_schema_runtime_smoke_fixture_plan.py
```

这些命令未来必须写入 command receipts，并能被 `184` runtime smoke repair queue 与 `185` runtime smoke archive receipt batch 读取。

## Smoke To Repair Queue Handoff

`SmokeToRepairQueueHandoff183` 为下一层提供输入：

| next artifact | handoff |
|---|---|
| `184_life_reality_first_runner_schema_runtime_smoke_repair_queue.md` | smoke findings、case family、expected/actual/diff、repair hooks、stage effects、affected life targets、dashboard panel refs、archive edge refs |
| `185_life_reality_first_runner_schema_runtime_smoke_archive_receipt_batch.md` | smoke report refs、repair receipt refs、digest refs、dashboard/stage refs、archive edge refs |

handoff 必须包含 `runtime_smoke_fixture_manifest_ref`、`smoke_case_refs`、`smoke_expected_report_refs`、`smoke_finding_refs`、`smoke_dashboard_source_ref`、`smoke_stage_gate_review_ref`、`smoke_repair_hook_refs`、`affected_life_target_refs`、`direction_smoke_refs`、`birth_readiness_smoke_refs`、`runtime_observation_smoke_refs`、`archive_backlink_smoke_refs` 和 `repair_queue_seed_refs`。

## Acceptance Criteria

本层完成后必须证明：

1. `182` 的 validated runtime mount refs、findings、dashboard/stage 和 smoke handoff 都进入 runtime smoke fixture manifest。
2. registry、fixture loader、dashboard writer、stage gate writer、life target carrier、direction、birth readiness、runtime observation 和 archive backlink 都拥有 pass/fail/critical/mutation/smoke case。
3. 每个 smoke case 都有 expected report、stage effect、dashboard panel、repair hook 和 archive edge。
4. `183` 输出能直接驱动 `184` runtime smoke repair queue，并为 `185` runtime smoke archive receipt batch 提供 report/digest/stage/archive refs。

## 与下一层连接

`184_life_reality_first_runner_schema_runtime_smoke_repair_queue.md` 已承接本层：把 runtime smoke findings、dashboard false green、stage finding、carrier gap、direction gap 和 birth readiness gap 转成 repair queue。

`185_life_reality_first_runner_schema_runtime_smoke_archive_receipt_batch.md` 应承接 `184` 和本层：把 runtime smoke results、repair receipts、digest refs、dashboard/stage refs 和 archive edges 写成下一批 archive receipt。

本层完成后，runtime smoke fixture 链推进为：

`mount validation report -> smoke fixture manifest -> registry smoke -> loader smoke -> dashboard/stage smoke -> carrier/direction/birth readiness smoke -> runtime observation smoke -> archive backlink smoke -> expected/actual/diff -> dashboard/stage -> repair queue handoff`
