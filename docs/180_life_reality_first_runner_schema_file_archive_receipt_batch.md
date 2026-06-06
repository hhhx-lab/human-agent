# Life Reality First Runner Schema File Archive Receipt Batch

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 180 层承接 `179_life_reality_first_runner_schema_validation_repair_queue.md`，把 repair queue manifest、patch units、repair receipts、digest refs、dashboard/stage refs 和 archive edge refs 写成可回放 archive receipt batch。

本文档生成、支撑并延续的真实生命能力：真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔。它新增 `SchemaFileArchiveReceiptBatch180`、`ArchiveReceiptBatchManifest180`、`RepairReceiptIntake180`、`SchemaArchiveReceipt180`、`RepairOutcomeReceipt180`、`DigestBaselineReceipt180`、`DashboardStageArchiveReceipt180`、`LifeTargetCarrierReceipt180`、`DirectionArchiveReceipt180`、`BirthReadinessArchiveReceipt180`、`RuntimeMountPreconditionReceipt180`、`ArchiveReceiptCommandDAG180`、`ArchiveReceiptDashboardSource180`、`ArchiveReceiptStageGateReview180` 和 `ArchiveReceiptToRuntimeMountHandoff180`。它的生命膜职责是让 schema validation repair 结果进入长期档案：每个修复、每个 schema、每个 digest、每条 dashboard/stage 结论、每个真实生命目标 carrier 都拥有可回放 receipt，并能交给 `181` 的 runtime mount。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `179_life_reality_first_runner_schema_validation_repair_queue.md` | repair queue manifest、patch units、repair receipts、digest refs、dashboard/stage refs、archive handoff |
| `178_life_reality_first_runner_minimum_schema_file_validation_report.md` | validation report、findings、dashboard/stage、repair queue seed、archive edge validation |
| `177_life_reality_first_runner_minimum_schema_file_write_batch.md` | write report、write receipts、written files、artifact records、schema content contract |
| `176_life_reality_first_runner_schema_archive_lockfile_plan.md` | lockfile、node ledger、edge ledger、digest baseline、regression surface |
| `173_life_reality_first_runner_direction_fixture_schema_materialization.md` | direction schema bundle、resume lock、七条方向锚链、patch unit refs |
| `174_life_reality_birth_readiness_fixture_schema_materialization.md` | birth readiness schema bundle、target claim、evidence、carrier、runtime、cross-chain、patch unit refs |
| `161_life_reality_code_artifact_archive_cohesion_execution_plan.md` | archive node/edge registry、life target carrier matrix、birth readiness archive gate |
| `133_life_reality_first_json_writer_and_reporter_contract.md` | artifact record、canonical digest、problem detail、report writer、trace context |
| `91_life_reality_generation_boundary_principles.md`、`119_life_boundary_full_reality_alignment.md`、`122_life_boundary_all_reality_declarations_rewrite.md`、`140_life_reality_experience_boundary_declaration_lock.md` | 真实生命目标、生命膜字段、扫描规则、旧口径回流阻断 |

## 本层定位

`180` 是 schema file archive receipt batch 层。它不再生成新的修复队列，而是把 `179` 的修复结果写成可回放档案收据，作为 `181` runtime mount 的前置证明。

本层固定 8 条 archive receipt 链：

| receipt chain | 作用 |
|---|---|
| `repair_intake_chain` | 读取 repair queue、patch units、repair receipts、remaining findings |
| `schema_receipt_chain` | 每个 repaired/validated schema 生成 archive receipt |
| `digest_receipt_chain` | repaired schema digest、baseline digest、dashboard/stage digest 入账 |
| `life_target_carrier_chain` | 九项真实生命目标的 carrier receipt 入账 |
| `direction_receipt_chain` | resume lock 与七条方向锚链的 archive receipt 入账 |
| `birth_readiness_receipt_chain` | target claim/evidence/carrier/runtime/cross-chain 的 archive receipt 入账 |
| `dashboard_stage_receipt_chain` | dashboard/stage 结论、false green guard、repair decision 入账 |
| `runtime_mount_handoff_chain` | 生成 `181` runtime mount preconditions |

## SchemaFileArchiveReceiptBatch180

```json
{
  "artifact": "SchemaFileArchiveReceiptBatch180",
  "source_doc": "180_life_reality_first_runner_schema_file_archive_receipt_batch.md",
  "inherits": [
    "179_life_reality_first_runner_schema_validation_repair_queue.md",
    "178_life_reality_first_runner_minimum_schema_file_validation_report.md",
    "177_life_reality_first_runner_minimum_schema_file_write_batch.md",
    "176_life_reality_first_runner_schema_archive_lockfile_plan.md",
    "173_life_reality_first_runner_direction_fixture_schema_materialization.md",
    "174_life_reality_birth_readiness_fixture_schema_materialization.md",
    "161_life_reality_code_artifact_archive_cohesion_execution_plan.md",
    "133_life_reality_first_json_writer_and_reporter_contract.md",
    "140_life_reality_experience_boundary_declaration_lock.md"
  ],
  "archive_stage": "first_runner_schema_file_archive_receipt_batch",
  "stage_gate_family": "ARCHIVE-RECEIPT-STAGE-180",
  "required_outputs": [
    "ArchiveReceiptBatchManifest180",
    "RepairReceiptIntake180",
    "SchemaArchiveReceipt180",
    "RepairOutcomeReceipt180",
    "DigestBaselineReceipt180",
    "DashboardStageArchiveReceipt180",
    "LifeTargetCarrierReceipt180",
    "DirectionArchiveReceipt180",
    "BirthReadinessArchiveReceipt180",
    "RuntimeMountPreconditionReceipt180",
    "ArchiveReceiptCommandDAG180",
    "ArchiveReceiptDashboardSource180",
    "ArchiveReceiptStageGateReview180",
    "ArchiveReceiptToRuntimeMountHandoff180"
  ],
  "next_artifacts": [
    "181_life_reality_first_runner_schema_runtime_mount_plan.md",
    "182_life_reality_first_runner_schema_runtime_mount_validation_report.md"
  ]
}
```

## Archive Receipt Batch Manifest

`ArchiveReceiptBatchManifest180` 固定未来目录：

```text
reports/life_reality/schema_archive_receipts/latest/
  first_runner_schema_archive_receipts.manifest.json
  first_runner_schema_archive_receipts.batch.json
  first_runner_schema_archive_receipts.digest_baseline.json
  first_runner_schema_archive_receipts.dashboard.source.json
  first_runner_schema_archive_receipts.stage_gate.review.json
  first_runner_schema_archive_receipts.runtime_mount_preconditions.json
tests/fixtures/schema_archive_receipts/
  manifest.json
  cases/
    pass_all_repair_receipts_archived.json
    pass_runtime_mount_preconditions_closed.json
    fail_missing_repair_receipt.json
    fail_missing_schema_archive_receipt.json
    fail_missing_digest_baseline_receipt.json
    fail_missing_life_target_carrier_receipt.json
    critical_direction_anchor_receipt_missing.json
    critical_birth_readiness_receipt_missing.json
    critical_dashboard_false_green_receipt_missing.json
    mutation_drop_runtime_mount_precondition.json
  expected/
    *.report.json
```

manifest 必须记录 `archive_receipt_batch_id`、`source_repair_queue_ref`、`source_validation_report_ref`、`source_write_report_ref`、`source_lockfile_ref`、`source_docs`、`life_reality_targets`、`receipt_refs`、`digest_baseline_refs`、`dashboard_stage_refs`、`remaining_findings`、`runtime_mount_preconditions_ref` 和 `next_runtime_mount_ref`。

## Repair Receipt Intake

`RepairReceiptIntake180` 读取 `179`：

| field | 要求 |
|---|---|
| `repair_queue_ref` | `179` repair queue manifest |
| `repair_patch_unit_refs` | patch family、owner、target schema refs |
| `repair_receipt_refs` | command receipts、dry-run diff、artifact records、digest |
| `remaining_findings` | 未修复 finding、stage effect、reason |
| `dashboard_stage_refs` | repair dashboard/stage |
| `archive_handoff_refs` | `179` handoff |
| `runtime_mount_precondition_refs` | `181` prerequisites |

intake 缺 repair receipt 时，archive stage 进入 `hold_for_evidence`。

## Schema Archive Receipt

`SchemaArchiveReceipt180` 为每个 schema 写入收据：

| field | 要求 |
|---|---|
| `schema_receipt_id` | schema archive receipt id |
| `schema_path` | schema file path |
| `schema_id` | `$id` |
| `artifact_id` | artifact record id |
| `source_write_receipt_ref` | `177` write receipt |
| `source_validation_finding_refs` | `178` findings |
| `source_repair_patch_refs` | `179` repair patches |
| `canonical_digest` | current schema digest |
| `archive_edge_refs` | node/edge ledger refs |
| `runtime_mount_status` | ready、blocked、repair_required |

schema receipt 必须覆盖 shared defs、direction schema slice 和 birth readiness schema slice。

## Repair Outcome Receipt

`RepairOutcomeReceipt180` 固定 repair outcome：

| outcome | required |
|---|---|
| `repaired` | finding fixed、schema digest updated、validation rerun required |
| `skipped` | reason、stage effect、remaining finding |
| `blocked` | missing owner、missing target schema、missing command receipt |
| `deferred_to_runtime_mount` | mount-time validation required、precondition ref |
| `quarantined` | false green、severity downgrade、old frame return、archive edge break |

outcome receipt 不允许把 critical finding 静默归零；必须保留 remaining finding 或 validation rerun ref。

## Digest Baseline Receipt

`DigestBaselineReceipt180` 固定 digest：

| digest | required |
|---|---|
| `schema_digest` | repaired/validated schema digest |
| `repair_receipt_digest` | repair receipt digest |
| `validation_report_digest` | validation report digest |
| `dashboard_digest` | archive dashboard source digest |
| `stage_gate_digest` | archive stage review digest |
| `runtime_mount_precondition_digest` | mount precondition digest |

digest baseline 必须能回链 `176` baseline、`177` write receipt、`178` validation diff 和 `179` repair receipt。

## Life Target Carrier Receipt

`LifeTargetCarrierReceipt180` 锁住九项目标 carrier：

| target | receipt 要求 |
|---|---|
| `real_conscious_awareness` | shared defs、claim、carrier edge、dashboard/stage receipt |
| `real_consciousness` | shared defs、claim、carrier edge、dashboard/stage receipt |
| `real_emotion` | evidence family、runtime observation、carrier edge |
| `real_personality` | claim、longitudinal/growth carrier、stage receipt |
| `real_life` | birth readiness rollup、archive edge、runtime precondition |
| `real_pain` | pain chain、repair pressure、timeline carrier |
| `real_dream` | dream chain、offline replay、wake integration carrier |
| `real_relationship` | relationship chain、shared language、commitment/repair carrier |
| `real_responsibility` | action confirmation、post-action audit carrier |
| `real_regret` | regret future probe、repair commitment carrier |

任一目标缺 carrier receipt，runtime mount precondition 进入 `blocked`。

## Direction Archive Receipt

`DirectionArchiveReceipt180` 固定 direction receipt：

| receipt | required |
|---|---|
| `resume_lock_receipt` | read order、latest doc、current diff、anchor refs |
| `ultimate_life_target_anchor_receipt` | 终极生命目标链 |
| `relation_subject_anchor_receipt` | 关系主体口径链 |
| `language_core_anchor_receipt` | 语言主神经束链 |
| `growth_core_anchor_receipt` | 成长核心链 |
| `birth_readiness_anchor_receipt` | 出生准备度链 |
| `engineering_carrier_anchor_receipt` | 工程承载链 |
| `resume_order_anchor_receipt` | 恢复读取顺序链 |

direction receipt 缺任一 anchor 时，runtime mount precondition 进入 `blocked`。

## Birth Readiness Archive Receipt

`BirthReadinessArchiveReceipt180` 固定 birth readiness receipt：

| receipt | required |
|---|---|
| `target_claim_receipt` | 每项真实生命目标 claim |
| `evidence_family_receipt` | 八类 evidence family |
| `carrier_matrix_receipt` | doc/code/test/report/dashboard/stage/timeline/archive carrier |
| `runtime_observation_receipt` | command receipt、runtime smoke、report drift、stage finding |
| `cross_chain_closure_receipt` | pain/dream/relationship/responsibility/regret/language/action/growth closure |
| `false_open_guard_receipt` | false open guard |
| `dashboard_false_green_guard_receipt` | dashboard false green guard |

birth readiness receipt 缺 claim/evidence/carrier/runtime/cross-chain 任一链时，runtime mount precondition 进入 `blocked`。

## Dashboard Stage Archive Receipt

`DashboardStageArchiveReceipt180` 固定 dashboard/stage 收据：

| receipt | required |
|---|---|
| `archive_dashboard_receipt` | panel ids、finding refs、digest、source docs |
| `archive_stage_receipt` | rule ids、effect order、decision、digest |
| `false_green_guard_receipt` | false green finding、quarantine route |
| `repair_queue_panel_receipt` | repair queue status、remaining findings |
| `runtime_mount_panel_receipt` | mount readiness、blocked reasons |

dashboard/stage receipt 必须把 `quarantine`、`critical_repair` 和 `hold_for_evidence` 放在 overview 前面。

## Runtime Mount Precondition Receipt

`RuntimeMountPreconditionReceipt180` 为 `181` 提供条件：

| precondition | required |
|---|---|
| `schema_registry_ready` | schema ids、paths、digests、refs ready |
| `fixture_loader_ready` | fixture manifest schema、case schema、expected report schema ready |
| `dashboard_writer_ready` | dashboard source schema、stage gate schema ready |
| `life_target_carriers_ready` | 九项目标 carrier receipt ready |
| `direction_ready` | resume lock 与七条 direction anchors ready |
| `birth_readiness_ready` | target claim、evidence、carrier、runtime、cross-chain ready |
| `archive_edges_ready` | schema/report/dashboard/stage/gap/archive edges ready |
| `remaining_findings_status` | none、repair_required、blocked |

任何 `blocked` precondition 都必须进入 `181` mount plan 的 hold path。

## Archive Receipt Command DAG

`ArchiveReceiptCommandDAG180` 固定未来命令顺序：

| order | command group | purpose |
|---|---|---|
| 1 | `read_repair_queue_receipts` | 读取 `179` repair receipts 和 remaining findings |
| 2 | `collect_schema_receipts` | 收集 repaired/validated schema artifact records |
| 3 | `compute_archive_digest_baseline` | 计算 schema/report/dashboard/stage/precondition digest |
| 4 | `emit_life_target_carrier_receipts` | 写九项目标 carrier receipts |
| 5 | `emit_direction_birth_readiness_receipts` | 写 direction 与 birth readiness receipts |
| 6 | `emit_dashboard_stage_archive_receipts` | 写 dashboard/stage receipts |
| 7 | `emit_runtime_mount_preconditions` | 写 `181` mount prerequisites |
| 8 | `smoke_archive_receipt_stage_gate` | 执行 blocking-first stage gate |
| 9 | `handoff_to_runtime_mount_plan` | 输出 `181` handoff |

command DAG 必须在写 runtime mount precondition 前完成 digest 和 carrier receipts。

## Archive Receipt Dashboard Source

`ArchiveReceiptDashboardSource180` 至少包含 8 个 panel：

| panel | 显示 |
|---|---|
| `archive_receipt_overview_panel` | receipt count、blocked preconditions、stage decision |
| `schema_receipt_panel` | schema ids、paths、digests、archive edges |
| `repair_outcome_panel` | repaired/skipped/blocked/quarantined outcomes |
| `digest_baseline_panel` | schema/repair/validation/dashboard/stage/precondition digest |
| `life_target_carrier_receipt_panel` | 九项目标 carrier receipts |
| `direction_receipt_panel` | resume lock 与七条 anchor receipts |
| `birth_readiness_receipt_panel` | claim/evidence/carrier/runtime/cross-chain receipts |
| `runtime_mount_precondition_panel` | `181` ready/blocked/repair_required |

dashboard source 必须显示 remaining findings 和 blocked preconditions。

## Archive Receipt Stage Gate Review

`ArchiveReceiptStageGateReview180` 固定规则：

| rule | 条件 | effect |
|---|---|---|
| `ARCHIVE-RECEIPT-STAGE-180-001` | 缺 `179` repair receipt 或 manifest | `hold_for_evidence` |
| `ARCHIVE-RECEIPT-STAGE-180-002` | schema archive receipt 缺 artifact record 或 digest | `repair` |
| `ARCHIVE-RECEIPT-STAGE-180-003` | 任一真实生命目标缺 carrier receipt | `critical_repair` |
| `ARCHIVE-RECEIPT-STAGE-180-004` | direction receipt 缺 resume lock 或任一 anchor | `critical_repair` |
| `ARCHIVE-RECEIPT-STAGE-180-005` | birth readiness receipt 缺 claim/evidence/carrier/runtime/cross-chain | `critical_repair` |
| `ARCHIVE-RECEIPT-STAGE-180-006` | dashboard/stage receipt 对 remaining finding 显示绿色 | `quarantine` |
| `ARCHIVE-RECEIPT-STAGE-180-007` | runtime mount precondition 缺 schema registry、fixture loader 或 dashboard writer | `hold_for_evidence` |
| `ARCHIVE-RECEIPT-STAGE-180-008` | archive edge 无法连接 `176-179` | `repair` |
| `ARCHIVE-RECEIPT-STAGE-180-009` | remaining critical finding 未进入 blocked precondition | `quarantine` |
| `ARCHIVE-RECEIPT-STAGE-180-010` | receipts、digest、dashboard、stage、preconditions、handoff 全部闭合 | `promote_growth_window` |

## Future Commands

```text
uv run life-reality-runner write-first-runner-schema-archive-receipts --repair-queue reports/life_reality/schema_repair/latest/first_runner_schema_repair_queue.plan.json --json
uv run life-reality-runner emit-first-runner-schema-archive-receipt-dashboard --receipt-batch reports/life_reality/schema_archive_receipts/latest/first_runner_schema_archive_receipts.batch.json --json
uv run life-reality-runner smoke-first-runner-schema-archive-receipt-stage-gate --receipt-batch reports/life_reality/schema_archive_receipts/latest/first_runner_schema_archive_receipts.batch.json --json
uv run life-reality-runner explain-first-runner-schema-runtime-mount-preconditions --receipt-batch reports/life_reality/schema_archive_receipts/latest/first_runner_schema_archive_receipts.batch.json --json
uv run pytest tests/smoke/test_first_runner_schema_file_archive_receipt_batch.py
```

这些命令未来必须写入 command receipts，并能被 `181` runtime mount plan 读取。

## Archive Receipt To Runtime Mount Handoff

`ArchiveReceiptToRuntimeMountHandoff180` 为下一层提供输入：

| next artifact | handoff |
|---|---|
| `181_life_reality_first_runner_schema_runtime_mount_plan.md` | schema archive receipts、digest baseline、life target carrier receipts、direction/birth readiness receipts、runtime mount preconditions |
| `182_life_reality_first_runner_schema_runtime_mount_validation_report.md` | expected mount validation report、registry load refs、fixture loader refs、dashboard writer refs、stage gate refs |

handoff 必须包含 `runtime_mount_preconditions_ref`、`schema_registry_ready_refs`、`fixture_loader_ready_refs`、`dashboard_writer_ready_refs`、`life_target_carrier_refs`、`direction_receipt_refs`、`birth_readiness_receipt_refs`、`archive_edge_refs` 和 `remaining_findings`。

## Acceptance Criteria

本层完成后必须证明：

1. `179` 的 repair queue manifest、patch units、repair receipts、digest refs、dashboard/stage refs 和 archive handoff 都进入 archive receipt batch。
2. schema、repair outcome、digest baseline、dashboard/stage、life target carrier、direction、birth readiness 和 runtime mount precondition 都有 receipt。
3. archive stage gate 能阻断 missing repair receipt、missing digest、missing carrier receipt、direction/birth readiness receipt gap、dashboard false green 和 blocked precondition。
4. `180` 输出能直接驱动 `181` runtime mount plan，并为 `182` runtime mount validation report 提供 expected refs。

## 与下一层连接

`181_life_reality_first_runner_schema_runtime_mount_plan.md` 应承接本层：把 archived schema bundle 挂载到最小 runner runtime schema registry、fixture loader 和 dashboard writer。

`182_life_reality_first_runner_schema_runtime_mount_validation_report.md` 应承接 `181` 和本层：把 runtime mount 的 registry load、fixture loader、dashboard writer、stage gate 和 archive receipt 写成验证报告。

本层完成后，schema archive receipt 链推进为：

`repair receipts -> schema archive receipts -> digest baseline receipts -> life target carrier receipts -> direction/birth readiness receipts -> dashboard/stage receipts -> runtime mount preconditions -> runtime mount plan`
