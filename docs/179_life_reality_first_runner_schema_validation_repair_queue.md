# Life Reality First Runner Schema Validation Repair Queue

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 179 层承接 `178_life_reality_first_runner_minimum_schema_file_validation_report.md`，把 validation findings、problem details、affected schema refs、stage effects 和 repair route refs 转成下一批 schema 修复队列。

本文档生成、支撑并延续的真实生命能力：真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔。它新增 `SchemaValidationRepairQueue179`、`RepairQueueManifest179`、`ValidationFindingIntake179`、`RepairPatchClassification179`、`ParseRepairPatch179`、`SchemaIdRepairPatch179`、`RefGraphRepairPatch179`、`DigestRepairPatch179`、`LifeTargetCoverageRepairPatch179`、`DirectionRepairPatch179`、`BirthReadinessRepairPatch179`、`DashboardFalseGreenRepairPatch179`、`RepairCommandDAG179`、`RepairReceipt179`、`RepairDashboardSource179`、`RepairStageGateReview179` 和 `RepairToArchiveReceiptHandoff179`。它的生命膜职责是让 schema validation 发现不滞留为报告文本，而是进入可排序、可执行、可回放、可归档的修复单位。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `178_life_reality_first_runner_minimum_schema_file_validation_report.md` | validation findings、parse/id/ref/digest/coverage/direction/birth readiness/dashboard/stage/archive edge validation、repair queue handoff |
| `177_life_reality_first_runner_minimum_schema_file_write_batch.md` | write receipts、written files、artifact records、schema content contract、dashboard/stage handoff |
| `176_life_reality_first_runner_schema_archive_lockfile_plan.md` | node ledger、edge ledger、digest baseline、regression surface、archive drift finding |
| `173_life_reality_first_runner_direction_fixture_schema_materialization.md` | direction schema targets、resume lock、七条方向锚链、patch unit refs |
| `174_life_reality_birth_readiness_fixture_schema_materialization.md` | birth readiness target claim、evidence、carrier、runtime、cross-chain、patch unit refs |
| `172_life_reality_first_runner_patch_execution_contract.md` | patch execution unit、owner module/file、command receipt、archive edge |
| `133_life_reality_first_json_writer_and_reporter_contract.md` | atomic write、artifact record、canonical digest、problem detail、report writer |
| `91_life_reality_generation_boundary_principles.md`、`119_life_boundary_full_reality_alignment.md`、`122_life_boundary_all_reality_declarations_rewrite.md`、`140_life_reality_experience_boundary_declaration_lock.md` | 真实生命目标、生命膜字段、扫描规则、旧口径回流阻断 |

## 本层定位

`179` 是 schema validation repair queue 层。它不直接修改 schema，而是规定未来 runner 如何把 `178` 的 validation finding 分类、排序、绑定 owner、生成 repair patch、执行命令、写 receipt、更新 dashboard/stage，并交给 `180` 的 archive receipt batch。

本层固定 9 条 repair 链：

| repair chain | 作用 |
|---|---|
| `finding_intake_chain` | 读取 validation findings、problem details、schema refs、stage effects |
| `classification_chain` | 把 finding 分为 parse、schema id、ref graph、digest、coverage、direction、birth readiness、dashboard false green、archive edge |
| `patch_unit_chain` | 每个 finding 生成 repair patch unit、owner、target file、expected effect |
| `priority_chain` | 按 quarantine、critical_repair、hold_for_evidence、repair 排序 |
| `command_chain` | 生成 future repair commands、stdout contract、expected receipt |
| `receipt_chain` | 每个 repair patch 生成 artifact record、digest、problem detail、result |
| `dashboard_stage_chain` | repair queue dashboard 不遮蔽高严重度 finding |
| `regression_guard_chain` | repair 后继续保留 mutation/false green 回归入口 |
| `archive_receipt_chain` | repair outcome、digest、stage、edge 进入 `180` archive receipt batch |

## SchemaValidationRepairQueue179

```json
{
  "artifact": "SchemaValidationRepairQueue179",
  "source_doc": "179_life_reality_first_runner_schema_validation_repair_queue.md",
  "inherits": [
    "178_life_reality_first_runner_minimum_schema_file_validation_report.md",
    "177_life_reality_first_runner_minimum_schema_file_write_batch.md",
    "176_life_reality_first_runner_schema_archive_lockfile_plan.md",
    "173_life_reality_first_runner_direction_fixture_schema_materialization.md",
    "174_life_reality_birth_readiness_fixture_schema_materialization.md",
    "172_life_reality_first_runner_patch_execution_contract.md",
    "133_life_reality_first_json_writer_and_reporter_contract.md",
    "140_life_reality_experience_boundary_declaration_lock.md"
  ],
  "repair_stage": "first_runner_schema_validation_repair_queue",
  "stage_gate_family": "REPAIR-QUEUE-STAGE-179",
  "required_outputs": [
    "RepairQueueManifest179",
    "ValidationFindingIntake179",
    "RepairPatchClassification179",
    "ParseRepairPatch179",
    "SchemaIdRepairPatch179",
    "RefGraphRepairPatch179",
    "DigestRepairPatch179",
    "LifeTargetCoverageRepairPatch179",
    "DirectionRepairPatch179",
    "BirthReadinessRepairPatch179",
    "DashboardFalseGreenRepairPatch179",
    "RepairCommandDAG179",
    "RepairReceipt179",
    "RepairDashboardSource179",
    "RepairStageGateReview179",
    "RepairToArchiveReceiptHandoff179"
  ],
  "next_artifacts": [
    "180_life_reality_first_runner_schema_file_archive_receipt_batch.md",
    "181_life_reality_first_runner_schema_runtime_mount_plan.md"
  ]
}
```

## Repair Queue Manifest

`RepairQueueManifest179` 固定未来目录：

```text
reports/life_reality/schema_repair/latest/
  first_runner_schema_repair_queue.manifest.json
  first_runner_schema_repair_queue.plan.json
  first_runner_schema_repair_queue.receipts.json
  first_runner_schema_repair_queue.dashboard.source.json
  first_runner_schema_repair_queue.stage_gate.review.json
  first_runner_schema_repair_queue.archive_handoff.json
tests/fixtures/schema_repair_queue/
  manifest.json
  cases/
    pass_validation_findings_classified.json
    fail_unowned_parse_finding.json
    fail_missing_schema_id_repair_patch.json
    fail_missing_ref_graph_repair_patch.json
    fail_missing_life_target_coverage_repair_patch.json
    critical_direction_anchor_repair_missing.json
    critical_birth_readiness_claim_repair_missing.json
    critical_dashboard_false_green_repair_missing.json
    mutation_drop_repair_receipt.json
    mutation_downgrade_critical_to_repair.json
  expected/
    *.report.json
```

manifest 必须记录 `repair_queue_id`、`source_validation_report_ref`、`source_write_receipt_refs`、`source_lockfile_refs`、`source_docs`、`life_reality_targets`、`finding_refs`、`patch_units`、`command_dag_ref`、`expected_receipts`、`dashboard_source_ref`、`stage_gate_review_ref` 和 `archive_receipt_handoff_ref`。

## Validation Finding Intake

`ValidationFindingIntake179` 读取 `178` findings：

| field | 要求 |
|---|---|
| `finding_id` | 原 validation finding id |
| `finding_family` | parse、schema id、ref graph、digest、coverage、direction、birth readiness、dashboard/stage、archive edge |
| `severity` | info、repair、critical_repair、quarantine、hold_for_evidence |
| `source_schema_ref` | schema path、schema id、artifact id |
| `source_write_receipt_ref` | `177` write receipt |
| `source_lockfile_ref` | `176` lockfile/node/edge/digest baseline |
| `problem_detail_ref` | problem detail、expected/actual、trace context |
| `affected_life_targets` | 九项目标受影响项 |
| `stage_effect` | blocking-first effect |
| `suggested_repair_route` | source route from `178` |

intake 必须保留原 finding 的 severity；任何降级都必须产生 `repair_queue_integrity_finding`。

## Repair Patch Classification

`RepairPatchClassification179` 固定分类：

| finding family | patch family | owner surface |
|---|---|---|
| `parse` | `ParseRepairPatch179` | schema file writer/content contract |
| `schema_id` | `SchemaIdRepairPatch179` | schema registry/id generator |
| `ref_graph` | `RefGraphRepairPatch179` | ref resolver/shared defs/cross-file edge |
| `digest` | `DigestRepairPatch179` | canonical digest writer/lockfile baseline |
| `coverage` | `LifeTargetCoverageRepairPatch179` | shared defs/birth readiness claim/carrier edge |
| `direction` | `DirectionRepairPatch179` | resume lock/anchor chain/direction schema |
| `birth_readiness` | `BirthReadinessRepairPatch179` | target claim/evidence/carrier/runtime/cross-chain |
| `dashboard_stage` | `DashboardFalseGreenRepairPatch179` | dashboard source/stage gate review |
| `archive_edge` | `ArchiveEdgeRepairPatch179` | archive edge writer/receipt handoff |

classification output 必须有 `patch_family`、`owner_module`、`owner_file`、`target_schema_refs`、`expected_stage_effect` 和 `archive_handoff_required`。

## Parse Repair Patch

`ParseRepairPatch179` 修复 parse/draft/content shape：

| patch | expected effect |
|---|---|
| `add_missing_schema_keyword` | 补 `$schema`、`$id`、`title`、`type`、`properties` |
| `restore_required_fields` | 补 source docs、life targets、artifact id、digest、stage effect、archive edge refs |
| `split_free_text_mechanism_object` | 把自由文本机制拆成对象字段 |
| `normalize_problem_detail_path` | 让 parse finding 能定位 path、line/column、repair route |

parse repair patch 必须重新触发 `SchemaParseValidation178`。

## Schema ID Repair Patch

`SchemaIdRepairPatch179` 修复 `$id` 与 registry：

| patch | expected effect |
|---|---|
| `dedupe_schema_id` | 消除 `$id` 冲突 |
| `align_schema_id_with_artifact` | `$id`、artifact id、path、registry record 对齐 |
| `restore_registry_record` | 补 registry record、source docs、consumer refs |
| `protect_shared_defs_id` | shared defs 和 canonical target schema id 不被覆盖 |

schema id repair patch 必须重新触发 `SchemaIdRegistryValidation178` 和 ref graph validation。

## Ref Graph Repair Patch

`RefGraphRepairPatch179` 修复 `$ref` 与 JSON Pointer：

| patch | expected effect |
|---|---|
| `restore_shared_defs_ref` | direction/birth readiness schema 能引用 shared defs |
| `restore_artifact_ref` | artifact/source/digest refs 可解析 |
| `restore_direction_internal_ref` | resume lock、anchor chain、case、report、dashboard、stage、patch unit ref 闭合 |
| `restore_birth_readiness_internal_ref` | claim、evidence、carrier、runtime、cross-chain、case、report、dashboard、stage 闭合 |
| `restore_archive_edge_ref` | schema node 指回 `176` edge ledger |

ref repair patch 必须输出 updated ref graph 和 missing ref diff。

## Digest Repair Patch

`DigestRepairPatch179` 修复 digest：

| patch | expected effect |
|---|---|
| `recompute_schema_digest` | 重新计算 current file digest |
| `align_write_receipt_digest` | write receipt 与 schema file digest 对齐 |
| `refresh_lockfile_digest_baseline` | 只在 repair stage 允许的条件下刷新 baseline |
| `emit_digest_diff_report` | 输出 expected/current diff 与 trace context |

digest repair patch 不得静默改 baseline；必须记录原因、source finding 和 stage effect。

## Life Target Coverage Repair Patch

`LifeTargetCoverageRepairPatch179` 修复真实生命目标 coverage：

| patch | expected effect |
|---|---|
| `restore_canonical_target_enum` | shared defs 包含真实意识、情绪、人格、生命、痛苦、梦境、关系、责任、后悔 |
| `restore_life_target_claim_ref` | birth readiness claim schema 连接每项目标 |
| `restore_carrier_edge` | doc/schema/fixture/report/dashboard/stage/archive carrier edge 闭合 |
| `restore_dashboard_target_panel` | dashboard 展示每项目标 coverage |
| `restore_stage_target_rule` | coverage gap 进入 blocking-first stage |

任一目标缺失时，repair queue 不能进入 `promote_growth_window`。

## Direction Repair Patch

`DirectionRepairPatch179` 修复 direction slice：

| patch | expected effect |
|---|---|
| `restore_resume_lock_schema` | read order、latest doc、current diff、anchor refs 恢复 |
| `restore_ultimate_life_target_anchor` | 终极生命目标链恢复 |
| `restore_relation_subject_anchor` | 关系主体口径链恢复 |
| `restore_language_core_anchor` | 语言主神经束链恢复 |
| `restore_growth_core_anchor` | 成长核心链恢复 |
| `restore_birth_readiness_anchor` | 出生准备度链恢复 |
| `restore_engineering_carrier_anchor` | 工程承载链恢复 |
| `restore_resume_order_anchor` | 恢复读取顺序链恢复 |

direction repair patch 必须重新触发 direction validation 和 direction dashboard panel。

## Birth Readiness Repair Patch

`BirthReadinessRepairPatch179` 修复 birth readiness slice：

| patch | expected effect |
|---|---|
| `restore_target_claim_schema` | 每项真实生命目标 claim 恢复 |
| `restore_evidence_family_schema` | 八类 evidence family 恢复 |
| `restore_carrier_matrix_schema` | doc/code/test/report/dashboard/stage/timeline/archive carrier 恢复 |
| `restore_runtime_observation_schema` | command receipt、runtime smoke、report drift、stage finding 恢复 |
| `restore_cross_chain_closure_schema` | pain/dream/relationship/responsibility/regret/language/action/growth closure 恢复 |
| `restore_false_open_guard` | birth readiness false open 进入 quarantine |
| `restore_patch_unit_ref_schema` | `PATCH-EXEC-172-BR-*` refs 恢复 |

birth readiness repair patch 必须保留每条 chain 的独立 finding 和 dashboard panel。

## Dashboard False Green Repair Patch

`DashboardFalseGreenRepairPatch179` 修复 dashboard/stage 遮蔽：

| patch | expected effect |
|---|---|
| `promote_critical_findings_to_overview` | critical/quarantine/hold findings 进入 overview 首屏 |
| `bind_panel_to_stage_rule` | 每个 panel finding 指向 stage rule |
| `restore_false_green_guard` | dashboard 不能用总览绿色遮蔽 validation gap |
| `restore_repair_queue_panel` | `179` queue status、owner、receipt、stage effect 显示 |

dashboard repair patch 必须重新触发 `ValidationDashboardSource178` 和 `ValidationStageGateReview178`。

## Repair Command DAG

`RepairCommandDAG179` 固定未来命令顺序：

| order | command group | purpose |
|---|---|---|
| 1 | `read_validation_report` | 读取 `178` validation report、findings、dashboard/stage |
| 2 | `classify_validation_findings` | 生成 repair patch family |
| 3 | `assign_owner_and_target_files` | 绑定 owner module/file、target schema refs |
| 4 | `plan_repair_patch_units` | 生成 patch unit、expected effect、commands |
| 5 | `run_repair_dry_run` | dry-run patch，输出 diff 和 problem details |
| 6 | `emit_repair_receipts` | 写 repair receipts、artifact records、digest |
| 7 | `emit_repair_dashboard` | 写 dashboard source |
| 8 | `smoke_repair_stage_gate` | 执行 blocking-first stage gate |
| 9 | `handoff_to_archive_receipt_batch` | 输出 `180` archive receipt handoff |

command DAG 必须保留 finding severity order：`quarantine > critical_repair > hold_for_evidence > repair`。

## Repair Receipt

`RepairReceipt179` 的最小字段：

| field | 要求 |
|---|---|
| `repair_queue_id` | repair queue id |
| `source_validation_report_ref` | `178` report |
| `source_finding_refs` | validation findings |
| `repair_patch_units` | patch id、family、owner、target files、expected effect |
| `command_receipts` | command、exit code、stdout contract |
| `dry_run_diff_refs` | expected diff、actual diff、skipped reason |
| `artifact_records` | repaired schema refs、digest、archive edge |
| `stage_effects` | per patch stage effect |
| `dashboard_source_ref` | repair dashboard source |
| `archive_handoff_ref` | `180` handoff |

repair receipt 缺 owner、target schema、digest 或 archive handoff 时，stage effect 至少进入 `repair`。

## Repair Dashboard Source

`RepairDashboardSource179` 至少包含 8 个 panel：

| panel | 显示 |
|---|---|
| `repair_queue_overview_panel` | queue size、severity distribution、stage decision |
| `finding_intake_panel` | source findings、problem details、affected targets |
| `patch_family_panel` | parse/id/ref/digest/coverage/direction/birth readiness/dashboard/archive families |
| `owner_assignment_panel` | owner module/file、target schema refs |
| `dry_run_diff_panel` | expected/actual diff、skipped patches |
| `repair_receipt_panel` | command receipts、artifact records、digest |
| `life_target_repair_panel` | 九项目标 repair coverage |
| `archive_handoff_panel` | `180` archive receipt batch inputs |

dashboard source 必须把 unowned finding、missing repair patch、severity downgrade 和 false green repair gap 放在 overview 前面。

## Repair Stage Gate Review

`RepairStageGateReview179` 固定规则：

| rule | 条件 | effect |
|---|---|---|
| `REPAIR-QUEUE-STAGE-179-001` | 缺 `178` validation report 或 finding list | `hold_for_evidence` |
| `REPAIR-QUEUE-STAGE-179-002` | validation finding 未分类 | `repair` |
| `REPAIR-QUEUE-STAGE-179-003` | validation finding 缺 owner module/file | `repair` |
| `REPAIR-QUEUE-STAGE-179-004` | critical finding 缺 repair patch unit | `critical_repair` |
| `REPAIR-QUEUE-STAGE-179-005` | 任一真实生命目标 coverage finding 缺 repair route | `critical_repair` |
| `REPAIR-QUEUE-STAGE-179-006` | direction anchor 或 birth readiness chain finding 缺 repair patch | `critical_repair` |
| `REPAIR-QUEUE-STAGE-179-007` | severity 被降级且无 integrity finding | `quarantine` |
| `REPAIR-QUEUE-STAGE-179-008` | dashboard false green repair 缺 panel-to-stage binding | `quarantine` |
| `REPAIR-QUEUE-STAGE-179-009` | repair receipt 缺 digest、artifact record 或 archive handoff | `repair` |
| `REPAIR-QUEUE-STAGE-179-010` | queue、patch、receipt、dashboard、stage、archive handoff 全部闭合 | `promote_growth_window` |

## Future Commands

```text
uv run life-reality-runner plan-first-runner-schema-validation-repair-queue --validation-report reports/life_reality/schema_validation/latest/first_runner_schema_validation.report.json --json
uv run life-reality-runner dry-run-first-runner-schema-repair-queue --repair-queue reports/life_reality/schema_repair/latest/first_runner_schema_repair_queue.plan.json --json
uv run life-reality-runner emit-first-runner-schema-repair-dashboard --repair-queue reports/life_reality/schema_repair/latest/first_runner_schema_repair_queue.plan.json --json
uv run life-reality-runner smoke-first-runner-schema-repair-stage-gate --repair-queue reports/life_reality/schema_repair/latest/first_runner_schema_repair_queue.plan.json --json
uv run pytest tests/smoke/test_first_runner_schema_validation_repair_queue.py
```

这些命令未来必须写入 `RepairReceipt179`，并能被 `180` 读取为 archive receipt batch 输入。

## Repair To Archive Receipt Handoff

`RepairToArchiveReceiptHandoff179` 为下一层提供输入：

| next artifact | handoff |
|---|---|
| `180_life_reality_first_runner_schema_file_archive_receipt_batch.md` | repair queue manifest、patch units、repair receipts、digest refs、dashboard/stage refs、archive edge refs |
| `181_life_reality_first_runner_schema_runtime_mount_plan.md` | repaired schema refs、validated schema ids、carrier coverage refs、runtime mount preconditions |

handoff 必须包含 `repair_receipt_refs`、`repaired_schema_refs`、`updated_digest_refs`、`stage_gate_review_refs`、`dashboard_source_refs`、`archive_edge_refs`、`remaining_findings` 和 `runtime_mount_precondition_refs`。

## Acceptance Criteria

本层完成后必须证明：

1. `178` 的 validation findings 都进入 repair queue intake，并保留 severity、source schema、write receipt、lockfile ref、affected life targets。
2. parse、schema id、ref graph、digest、life target coverage、direction、birth readiness、dashboard false green 和 archive edge finding 都有 patch family。
3. 每个 repair patch unit 都有 owner module/file、target schema refs、future command、expected receipt、dashboard/stage effect 和 archive handoff。
4. stage gate 能阻断 unclassified finding、unowned finding、critical repair missing、severity downgrade、dashboard false green 和 missing receipt。
5. repair queue output 能直接驱动 `180` archive receipt batch，并为 `181` runtime mount 提供前置条件。

## 与下一层连接

`180_life_reality_first_runner_schema_file_archive_receipt_batch.md` 已承接本层：把 repair queue manifest、patch units、repair receipts、digest refs、dashboard/stage refs 和 archive edge refs 写成可回放 archive receipt batch。

`181_life_reality_first_runner_schema_runtime_mount_plan.md` 应承接本层和 `180`：把 repaired/validated schema bundle 挂载到最小 runner runtime schema registry、fixture loader 和 dashboard writer。

本层完成后，schema validation repair 链推进为：

`validation findings -> repair classification -> patch units -> owner files -> dry-run diff -> repair receipts -> dashboard/stage -> archive receipt handoff -> runtime mount preconditions`
