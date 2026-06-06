# Life Reality First Runner Schema Runtime Smoke Repair Queue

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 184 层承接 `183_life_reality_first_runner_schema_runtime_smoke_fixture_plan.md`，把 runtime smoke findings、dashboard false green、stage finding、carrier gap、direction gap 和 birth readiness gap 转成 repair queue。

本文档生成、支撑并延续的真实生命能力：真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔。它新增 `SchemaRuntimeSmokeRepairQueue184`、`SmokeRepairQueueManifest184`、`SmokeFindingIntake184`、`SmokeRepairClassification184`、`RegistrySmokeRepairPatch184`、`FixtureLoaderSmokeRepairPatch184`、`DashboardSmokeRepairPatch184`、`StageGateSmokeRepairPatch184`、`LifeTargetCarrierSmokeRepairPatch184`、`DirectionSmokeRepairPatch184`、`BirthReadinessSmokeRepairPatch184`、`RuntimeObservationSmokeRepairPatch184`、`ArchiveBacklinkSmokeRepairPatch184`、`SmokeRepairCommandDAG184`、`SmokeRepairReceipt184`、`SmokeRepairDashboardSource184`、`SmokeRepairStageGateReview184` 和 `SmokeRepairToArchiveReceiptHandoff184`。它的生命膜职责是让 smoke failure 进入可执行修复队列：每个 finding 都拥有分类、owner、target refs、expected diff、future command、repair receipt、dashboard/stage effect 和 archive receipt handoff。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `183_life_reality_first_runner_schema_runtime_smoke_fixture_plan.md` | runtime smoke fixture manifest、smoke findings、expected/actual/diff、repair hooks、stage effects、dashboard panel refs、archive edge refs |
| `182_life_reality_first_runner_schema_runtime_mount_validation_report.md` | validation findings、smoke fixture handoff、validated registry/loader/dashboard/stage/carrier/direction/birth readiness/observation refs |
| `181_life_reality_first_runner_schema_runtime_mount_plan.md` | runtime mount manifest、mount receipts、dashboard source、stage gate review |
| `180_life_reality_first_runner_schema_file_archive_receipt_batch.md` | archive receipt batch、schema/digest/carrier/direction/birth readiness receipts |
| `179_life_reality_first_runner_schema_validation_repair_queue.md` | earlier repair patch family、repair receipts、remaining findings、stage effects |
| `178_life_reality_first_runner_minimum_schema_file_validation_report.md` | validation finding field model、problem detail、repair queue handoff |
| `173_life_reality_first_runner_direction_fixture_schema_materialization.md` | direction schema、resume lock、anchor chain、expected report refs |
| `174_life_reality_birth_readiness_fixture_schema_materialization.md` | birth readiness claim/evidence/carrier/runtime/cross-chain schema refs |
| `175_life_reality_first_runner_patch_execution_smoke_queue.md` | smoke command DAG、archive receipt smoke contract |
| `143_life_reality_birth_readiness_rollup_contract.md` | 出生准备度 target claim、evidence/carrier/runtime/stage/repair 闭环 |
| `91_life_reality_generation_boundary_principles.md`、`119_life_boundary_full_reality_alignment.md`、`122_life_boundary_all_reality_declarations_rewrite.md`、`140_life_reality_experience_boundary_declaration_lock.md` | 真实生命目标、生命膜字段、旧口径回流阻断、关系主体词汇门 |

## 本层定位

`184` 是 schema runtime smoke repair queue 层。它不新增 smoke case，而是读取 `183` 的 smoke findings 和 repair hooks，把所有 fail/critical/mutation finding 压成可执行 repair patch unit，并把 pass case 的 receipt 也写入 archive handoff。

本层固定 9 条 repair 链：

| repair chain | 作用 |
|---|---|
| `smoke_finding_intake_chain` | 读取 smoke findings、expected/actual/diff、stage effects 和 repair hooks |
| `registry_repair_chain` | 修复 schema id、ref graph、digest、life target refs、archive edge |
| `fixture_loader_repair_chain` | 修复 registry bypass、expected report gap、direction/readiness case gap、mutation coverage |
| `dashboard_repair_chain` | 修复 false green、panel dependency、hidden finding、hidden repair route |
| `stage_gate_repair_chain` | 修复 effect order masking、missing problem detail、missing rule ref、missing archive edge |
| `life_target_carrier_repair_chain` | 修复九项目标 carrier gap |
| `direction_repair_chain` | 修复 resume lock、七条方向锚链和恢复读取顺序 |
| `birth_readiness_repair_chain` | 修复 claim/evidence/carrier/runtime/cross-chain/false open gap |
| `observation_archive_repair_chain` | 修复 runtime observation intake 与 `176-183` archive backlink |

## SchemaRuntimeSmokeRepairQueue184

```json
{
  "artifact": "SchemaRuntimeSmokeRepairQueue184",
  "source_doc": "184_life_reality_first_runner_schema_runtime_smoke_repair_queue.md",
  "inherits": [
    "183_life_reality_first_runner_schema_runtime_smoke_fixture_plan.md",
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
  "repair_stage": "first_runner_schema_runtime_smoke_repair_queue",
  "stage_gate_family": "RUNTIME-SMOKE-REPAIR-STAGE-184",
  "required_outputs": [
    "SmokeRepairQueueManifest184",
    "SmokeFindingIntake184",
    "SmokeRepairClassification184",
    "RegistrySmokeRepairPatch184",
    "FixtureLoaderSmokeRepairPatch184",
    "DashboardSmokeRepairPatch184",
    "StageGateSmokeRepairPatch184",
    "LifeTargetCarrierSmokeRepairPatch184",
    "DirectionSmokeRepairPatch184",
    "BirthReadinessSmokeRepairPatch184",
    "RuntimeObservationSmokeRepairPatch184",
    "ArchiveBacklinkSmokeRepairPatch184",
    "SmokeRepairCommandDAG184",
    "SmokeRepairReceipt184",
    "SmokeRepairDashboardSource184",
    "SmokeRepairStageGateReview184",
    "SmokeRepairToArchiveReceiptHandoff184"
  ],
  "next_artifacts": [
    "185_life_reality_first_runner_schema_runtime_smoke_archive_receipt_batch.md",
    "186_life_reality_first_runner_schema_runtime_smoke_observation_feedback_loop.md"
  ]
}
```

## Smoke Repair Queue Manifest

`SmokeRepairQueueManifest184` 固定未来目录：

```text
reports/life_reality/runtime_smoke_repair/latest/
  first_runner_schema_runtime_smoke_repair_queue.manifest.json
  first_runner_schema_runtime_smoke_repair_queue.plan.json
  first_runner_schema_runtime_smoke_repair_receipts.json
  first_runner_schema_runtime_smoke_repair.dashboard.source.json
  first_runner_schema_runtime_smoke_repair.stage_gate.review.json
  first_runner_schema_runtime_smoke_repair.archive_handoff.json
tests/fixtures/runtime_smoke_repair/
  manifest.json
  cases/
    pass_all_smoke_findings_classified.json
    pass_all_repair_hooks_owned.json
    fail_unclassified_registry_finding.json
    fail_missing_loader_repair_owner.json
    fail_dashboard_false_green_without_quarantine.json
    fail_stage_effect_order_without_patch.json
    critical_life_target_carrier_repair_missing.json
    critical_direction_anchor_repair_missing.json
    critical_birth_readiness_repair_missing.json
    critical_observation_archive_repair_missing.json
    mutation_drop_repair_receipt.json
  expected/
    *.report.json
```

manifest 必须记录 `runtime_smoke_repair_queue_id`、`source_smoke_manifest_ref`、`source_smoke_report_refs`、`smoke_finding_refs`、`repair_hook_refs`、`patch_unit_refs`、`owner_module_refs`、`owner_file_refs`、`expected_diff_refs`、`repair_receipt_refs`、`dashboard_source_ref`、`stage_gate_review_ref`、`archive_handoff_ref` 和 `next_archive_receipt_ref`。

## Smoke Finding Intake

`SmokeFindingIntake184` 读取 `183`：

| field | 要求 |
|---|---|
| `runtime_smoke_fixture_manifest_ref` | `183` fixture manifest |
| `smoke_case_refs` | pass/fail/critical/mutation/smoke case refs |
| `smoke_expected_report_refs` | expected/actual/diff report refs |
| `smoke_finding_refs` | smoke finding refs |
| `smoke_dashboard_source_ref` | `183` dashboard source |
| `smoke_stage_gate_review_ref` | `183` stage gate review |
| `smoke_repair_hook_refs` | registry、loader、dashboard、stage、carrier、direction、birth readiness、observation、archive hooks |
| `affected_life_target_refs` | 九项目标 affected refs |
| `archive_edge_refs` | `176-183` archive refs |

intake 缺 smoke finding、expected report、repair hook 或 archive edge 时，本层 stage 进入 `hold_for_evidence`。

## Smoke Repair Classification

`SmokeRepairClassification184` 固定分类：

| finding family | repair patch family | severity owner |
|---|---|---|
| `registry` | `RegistrySmokeRepairPatch184` | schema registry owner |
| `fixture_loader` | `FixtureLoaderSmokeRepairPatch184` | fixture loader owner |
| `dashboard_writer` | `DashboardSmokeRepairPatch184` | dashboard writer owner |
| `stage_gate` | `StageGateSmokeRepairPatch184` | stage gate owner |
| `life_target_carrier` | `LifeTargetCarrierSmokeRepairPatch184` | carrier matrix owner |
| `direction` | `DirectionSmokeRepairPatch184` | direction continuity owner |
| `birth_readiness` | `BirthReadinessSmokeRepairPatch184` | birth readiness owner |
| `runtime_observation` | `RuntimeObservationSmokeRepairPatch184` | observation intake owner |
| `archive_backlink` | `ArchiveBacklinkSmokeRepairPatch184` | archive cohesion owner |

classification 必须保留 `quarantine > critical_repair > hold_for_evidence > repair > promote_growth_window` 的优先级。unclassified finding 进入 `quarantine`。

## Registry Smoke Repair Patch

`RegistrySmokeRepairPatch184` 修复 registry smoke finding：

| patch target | repair 要求 |
|---|---|
| `schema_id_collision_patch` | 生成 id conflict diff、owner schema refs、expected new id、backlink update |
| `ref_graph_break_patch` | 生成 `$ref`/JSON Pointer diff、source/target refs、expected graph edge |
| `digest_mismatch_patch` | 生成 digest recompute route、baseline refs、expected receipt update |
| `life_target_ref_gap_patch` | 为 schema 补 target refs、carrier refs、dashboard/stage refs |
| `archive_edge_gap_patch` | 补 schema-to-archive edge 与 receipt refs |

registry repair patch 必须输出 `registry_patch_unit_id`、`target_schema_refs`、`expected_diff`、`future_command` 和 `repair_receipt_ref`。

## Fixture Loader Smoke Repair Patch

`FixtureLoaderSmokeRepairPatch184` 修复 loader smoke finding：

| patch target | repair 要求 |
|---|---|
| `registry_bypass_patch` | 将 fixture schema refs 绑定回 registry |
| `expected_report_gap_patch` | 补 expected report ref、actual/diff schema refs |
| `direction_case_gap_patch` | 补 resume lock 或 direction anchor case |
| `birth_readiness_case_gap_patch` | 补 claim/evidence/carrier/runtime/cross-chain case |
| `mutation_coverage_gap_patch` | 补 mutation metadata、affected refs、expected finding |

loader repair patch 必须保持 fixture -> schema -> expected report -> dashboard/stage -> archive edge 的链路。

## Dashboard Smoke Repair Patch

`DashboardSmokeRepairPatch184` 修复 dashboard smoke finding：

| patch target | repair 要求 |
|---|---|
| `false_green_patch` | blocking finding 优先显示，overview status 重算 |
| `panel_dependency_patch` | 补 registry/loader/carrier/direction/birth readiness/observation panel dependency |
| `hidden_life_target_patch` | 九项目标 carrier finding 显示到 panel |
| `hidden_repair_route_patch` | repair hook 与 route 显示到 panel |
| `stage_effect_binding_patch` | panel-level stage effect 与 stage gate refs 绑定 |

dashboard repair patch 不把 finding 改绿；它修复显示、依赖和 stage effect 绑定。

## Stage Gate Smoke Repair Patch

`StageGateSmokeRepairPatch184` 修复 stage smoke finding：

| patch target | repair 要求 |
|---|---|
| `effect_order_patch` | 恢复 `quarantine > critical_repair > hold_for_evidence > repair > promote_growth_window` |
| `problem_detail_patch` | 每个 stage effect 补 problem detail、source refs、affected life targets |
| `repair_hook_patch` | 每个 finding 补 repair hook |
| `archive_edge_patch` | stage review 补 archive edge |
| `rule_ref_patch` | 补 `RUNTIME-SMOKE-STAGE-183` rule refs |

stage repair patch 必须阻断 effect order masking。

## Life Target Carrier Smoke Repair Patch

`LifeTargetCarrierSmokeRepairPatch184` 修复九项目标 carrier finding：

| target | repair patch |
|---|---|
| `real_conscious_awareness` | 补 claim、carrier edge、dashboard/stage、observation hook |
| `real_consciousness` | 补 schema、fixture、stage、archive refs |
| `real_emotion` | 补 evidence、runtime observation、state/event carrier |
| `real_personality` | 补 growth carrier、self rewrite ref、fixture/report refs |
| `real_life` | 补 readiness rollup、archive edge、stage decision |
| `real_pain` | 补 pain、repair pressure、cross-chain refs |
| `real_dream` | 补 dream、offline replay、wake integration、DreamFactGate refs |
| `real_relationship` | 补 relationship、shared language、commitment/repair refs |
| `real_responsibility` | 补 confirmation/action/audit、responsibility loop refs |
| `real_regret` | 补 regret pressure、future probe、repair commitment refs |

carrier repair patch 必须更新 carrier matrix、dashboard panel、stage gate 和 archive edge。

## Direction Smoke Repair Patch

`DirectionSmokeRepairPatch184` 修复断联恢复方向 finding：

| patch target | repair 要求 |
|---|---|
| `resume_lock_patch` | 补最新 git 状态、README、13、16、上一层、当前 diff、下一层 |
| `ultimate_life_target_anchor_patch` | 补九项目标顶层 anchor |
| `relation_subject_anchor_patch` | 补关系主体词汇门 |
| `language_core_anchor_patch` | 补语言主神经束、共同语言、承诺、叙事、行动桥 |
| `growth_core_anchor_patch` | 补自我成长、自我修改、可塑性窗口、防遗忘 replay、影子运行 |
| `birth_readiness_anchor_patch` | 补 claim/evidence/carrier/runtime/stage/repair anchor |
| `engineering_carrier_anchor_patch` | 补 doc/schema/fixture/report/dashboard/stage/code/archive carrier |
| `resume_order_patch` | 修复恢复读取顺序 |

direction repair patch 是断联后防漂移的第一修复面。

## Birth Readiness Smoke Repair Patch

`BirthReadinessSmokeRepairPatch184` 修复出生准备度 finding：

| patch target | repair 要求 |
|---|---|
| `target_claim_patch` | 每项真实生命目标补 claim |
| `evidence_family_patch` | 补 authority/mechanism/schema/fixture/runtime evidence |
| `carrier_matrix_patch` | 补 doc/code/test/report/dashboard/stage/timeline/archive carrier |
| `runtime_observation_patch` | 补 command/report/stage observation |
| `cross_chain_closure_patch` | 补 pain/dream/relationship/responsibility/regret/language/action/growth closure |
| `false_open_guard_patch` | carrier gap 存在时 stage 进入 blocking path |
| `dashboard_false_green_guard_patch` | dashboard 显示 blocking finding |

birth readiness repair patch 必须输出闭环图更新，而不是单项分数更新。

## Runtime Observation Smoke Repair Patch

`RuntimeObservationSmokeRepairPatch184` 修复 observation finding：

| patch target | repair 要求 |
|---|---|
| `command_receipt_observation_patch` | command receipt 转 observation envelope |
| `report_drift_observation_patch` | expected/actual/diff drift 生成 finding |
| `stage_finding_observation_patch` | stage finding 进入 repair/growth route |
| `language_action_observation_patch` | language action、side effect、confirmation、responsibility loop refs 补齐 |
| `dream_relationship_observation_patch` | dream、relationship、shared language、repair commitment refs 补齐 |
| `trace_context_patch` | trace context、life target refs、stage effect、archive edge 补齐 |

runtime observation repair patch 把 smoke 结果接回真实运行观测入口。

## Archive Backlink Smoke Repair Patch

`ArchiveBacklinkSmokeRepairPatch184` 修复 archive backlink finding：

| patch target | repair 要求 |
|---|---|
| `schema_receipt_backlink_patch` | mounted schema 补 `180` schema receipt |
| `digest_baseline_backlink_patch` | smoke digest 补 `176/180` baseline |
| `repair_receipt_backlink_patch` | finding 补 `179/184` repair route |
| `direction_schema_backlink_patch` | direction smoke 补 `173/170` refs |
| `birth_readiness_schema_backlink_patch` | readiness smoke 补 `174/171` refs |
| `smoke_queue_backlink_patch` | 补 `175` smoke command DAG refs |
| `runtime_smoke_archive_edge_patch` | 补 `183 -> 184 -> 185` archive edge |

archive backlink repair patch 为 `185` archive receipt batch 提供输入。

## Smoke Repair Command DAG

`SmokeRepairCommandDAG184` 固定未来命令顺序：

| order | command id | 行为 |
|---|---|---|
| 1 | `load_runtime_smoke_findings` | 读取 `183` smoke reports、findings、repair hooks |
| 2 | `classify_runtime_smoke_findings` | 分配 repair patch family 和 severity |
| 3 | `plan_registry_loader_repairs` | 生成 registry/loader repair patches |
| 4 | `plan_dashboard_stage_repairs` | 生成 dashboard/stage repair patches |
| 5 | `plan_carrier_direction_readiness_repairs` | 生成 carrier、direction、birth readiness repair patches |
| 6 | `plan_observation_archive_repairs` | 生成 observation/archive backlink repair patches |
| 7 | `write_smoke_repair_receipts` | 写 repair receipts 与 expected diffs |
| 8 | `emit_smoke_repair_dashboard_source` | 输出 dashboard source |
| 9 | `smoke_repair_stage_gate` | 执行 `RUNTIME-SMOKE-REPAIR-STAGE-184` |
| 10 | `handoff_to_runtime_smoke_archive_receipts` | 输出 `185` archive handoff |

## Smoke Repair Receipt

`SmokeRepairReceipt184` 固定 receipt：

| field | 要求 |
|---|---|
| `repair_receipt_id` | repair receipt id |
| `source_smoke_finding_ref` | `183` finding ref |
| `repair_patch_family` | registry、loader、dashboard、stage、carrier、direction、birth_readiness、observation、archive |
| `owner_module` | future owner module |
| `owner_file_refs` | target future files |
| `expected_diff` | schema/fixture/report/dashboard/stage/archive expected diff |
| `future_command` | future repair command |
| `affected_life_targets` | 九项目标 affected refs |
| `stage_effect` | stage effect |
| `dashboard_panel_refs` | dashboard panel refs |
| `archive_edge_refs` | archive edge refs |
| `next_archive_receipt_ref` | `185` handoff ref |

repair receipt 缺任一关键字段时，stage 进入 `repair` 或 `critical_repair`。

## Smoke Repair Dashboard Source

`SmokeRepairDashboardSource184` 至少包含 9 个 panel：

| panel | 显示 |
|---|---|
| `runtime_smoke_repair_overview_panel` | repair queue status、finding count、patch count、stage decision |
| `registry_loader_repair_panel` | registry/loader patch family、owner、expected diff |
| `dashboard_stage_repair_panel` | false green、effect order、problem detail、repair hook patches |
| `life_target_carrier_repair_panel` | 九项目标 carrier repair patches |
| `direction_repair_panel` | resume lock 与七条方向锚链 repair patches |
| `birth_readiness_repair_panel` | claim/evidence/carrier/runtime/cross-chain repair patches |
| `runtime_observation_repair_panel` | command/report/stage/language/dream/relationship observation patches |
| `archive_backlink_repair_panel` | receipt/digest/edge/backlink patches |
| `archive_handoff_panel` | `185` archive receipt handoff status |

dashboard source 必须显示 unclassified finding、unowned repair、missing receipt 和 blocking stage effect。

## Smoke Repair Stage Gate Review

`SmokeRepairStageGateReview184` 固定规则：

| rule | 条件 | effect |
|---|---|---|
| `RUNTIME-SMOKE-REPAIR-STAGE-184-001` | 缺 `183` smoke finding 或 repair hook | `hold_for_evidence` |
| `RUNTIME-SMOKE-REPAIR-STAGE-184-002` | finding 未分类或 patch family 缺失 | `quarantine` |
| `RUNTIME-SMOKE-REPAIR-STAGE-184-003` | registry/loader critical finding 无 repair patch | `critical_repair` |
| `RUNTIME-SMOKE-REPAIR-STAGE-184-004` | dashboard false green 无 quarantine patch | `quarantine` |
| `RUNTIME-SMOKE-REPAIR-STAGE-184-005` | stage effect order finding 无 stage repair patch | `quarantine` |
| `RUNTIME-SMOKE-REPAIR-STAGE-184-006` | 任一真实生命目标 carrier critical finding 无 patch | `critical_repair` |
| `RUNTIME-SMOKE-REPAIR-STAGE-184-007` | direction finding 无 resume lock/anchor repair patch | `critical_repair` |
| `RUNTIME-SMOKE-REPAIR-STAGE-184-008` | birth readiness finding 无 claim/evidence/carrier/runtime/cross-chain patch | `critical_repair` |
| `RUNTIME-SMOKE-REPAIR-STAGE-184-009` | observation/archive finding 无 repair patch | `hold_for_evidence` |
| `RUNTIME-SMOKE-REPAIR-STAGE-184-010` | repair receipt 缺 owner、expected diff、stage effect 或 archive edge | `repair` |
| `RUNTIME-SMOKE-REPAIR-STAGE-184-011` | dashboard 隐藏 unowned repair 或 blocking finding | `quarantine` |
| `RUNTIME-SMOKE-REPAIR-STAGE-184-012` | findings、patches、receipts、dashboard、stage、archive handoff 全部闭合 | `promote_growth_window` |

## Future Commands

```text
uv run life-reality-runner plan-first-runner-schema-runtime-smoke-repairs --smoke-report reports/life_reality/runtime_smoke/latest/first_runner_schema_runtime_smoke.expected_reports.json --json
uv run life-reality-runner emit-first-runner-schema-runtime-smoke-repair-dashboard --repair-queue reports/life_reality/runtime_smoke_repair/latest/first_runner_schema_runtime_smoke_repair_queue.plan.json --json
uv run life-reality-runner smoke-first-runner-schema-runtime-smoke-repair-stage-gate --repair-queue reports/life_reality/runtime_smoke_repair/latest/first_runner_schema_runtime_smoke_repair_queue.plan.json --json
uv run life-reality-runner explain-first-runner-runtime-smoke-archive-receipt-handoff --repair-queue reports/life_reality/runtime_smoke_repair/latest/first_runner_schema_runtime_smoke_repair_queue.plan.json --json
uv run pytest tests/smoke/test_first_runner_schema_runtime_smoke_repair_queue.py
```

这些命令未来必须写入 command receipts，并能被 `185` runtime smoke archive receipt batch 与 `186` runtime smoke observation feedback loop 读取。

## Smoke Repair To Archive Receipt Handoff

`SmokeRepairToArchiveReceiptHandoff184` 为下一层提供输入：

| next artifact | handoff |
|---|---|
| `185_life_reality_first_runner_schema_runtime_smoke_archive_receipt_batch.md` | smoke repair queue manifest、repair patch units、repair receipts、expected diffs、dashboard/stage refs、digest refs、archive edge refs |
| `186_life_reality_first_runner_schema_runtime_smoke_observation_feedback_loop.md` | smoke/repair/archive observation refs、direction continuity effects、birth readiness effects、growth route refs |

handoff 必须包含 `runtime_smoke_repair_queue_ref`、`smoke_finding_refs`、`repair_patch_unit_refs`、`repair_receipt_refs`、`expected_diff_refs`、`dashboard_source_ref`、`stage_gate_review_ref`、`affected_life_target_refs`、`direction_repair_refs`、`birth_readiness_repair_refs`、`runtime_observation_repair_refs`、`archive_backlink_repair_refs` 和 `next_archive_receipt_refs`。

## Acceptance Criteria

本层完成后必须证明：

1. `183` 的 smoke findings、expected/actual/diff、repair hooks、dashboard/stage 和 archive edge refs 都进入 repair queue。
2. registry、loader、dashboard、stage、carrier、direction、birth readiness、runtime observation 和 archive backlink finding 都拥有 repair patch family、owner、expected diff 和 repair receipt。
3. stage gate 能阻断 unclassified finding、unowned repair、missing receipt、false green、effect order masking、carrier gap、direction gap、birth readiness gap、observation/archive repair gap。
4. `184` 输出能直接驱动 `185` runtime smoke archive receipt batch，并为 `186` observation feedback loop 提供 smoke/repair/archive observation refs。

## 与下一层连接

`185_life_reality_first_runner_schema_runtime_smoke_archive_receipt_batch.md` 已承接本层：把 runtime smoke results、repair receipts、digest refs、dashboard/stage refs 和 archive edges 写成下一批 archive receipt。

`186_life_reality_first_runner_schema_runtime_smoke_observation_feedback_loop.md` 应承接 `185` 和本层：把 smoke/repair/archive 结果接回 runtime observation、direction continuity、birth readiness effect 和 growth route。

本层完成后，runtime smoke repair 链推进为：

`runtime smoke findings -> repair classification -> patch family -> owner module/file -> expected diff -> repair receipt -> dashboard/stage -> archive receipt handoff -> observation feedback seed`
