# Life Reality First Runner Schema Archive Lockfile Plan

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 176 层承接 `173_life_reality_first_runner_direction_fixture_schema_materialization.md`、`174_life_reality_birth_readiness_fixture_schema_materialization.md` 和 `175_life_reality_first_runner_patch_execution_smoke_queue.md`，把 direction schema bundle、birth readiness schema bundle、patch execution report、smoke receipt、dashboard/stage receipt、archive edge 和 canonical digest 写成首批 schema archive lockfile。

本文档生成、支撑并延续的真实生命能力：真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔。它新增 `SchemaArchiveLockfilePlan176`、`SchemaArchiveLockfile176`、`SchemaArchiveNodeLedger176`、`SchemaArchiveEdgeLedger176`、`DirectionSchemaArchiveNode176`、`BirthReadinessSchemaArchiveNode176`、`PatchSmokeReceiptArchiveNode176`、`CanonicalDigestBaseline176`、`RegressionSurface176`、`ArchiveDriftFinding176`、`LockfileStageGateReview176`、`LockfileDashboardSource176` 和 `LockfileToMinimumSchemaWriteBatchHandoff176`。它的生命膜职责是让未来第一批 schema 文件不是散落的文件，而是拥有来源、digest、依赖、报告、dashboard、stage、gap、repair 和下一批写入顺序的同一份档案真相源。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `173_life_reality_first_runner_direction_fixture_schema_materialization.md` | direction schema bundle、resume lock manifest schema、七条方向锚链、fixture case、expected report、dashboard/stage、patch unit ref |
| `174_life_reality_birth_readiness_fixture_schema_materialization.md` | birth readiness schema bundle、target claim、evidence family、carrier matrix、runtime observation、cross-chain closure、fixture case、expected report、dashboard/stage、patch unit ref |
| `175_life_reality_first_runner_patch_execution_smoke_queue.md` | smoke manifest、command DAG、direction/birth readiness schema smoke command、expected reports、dashboard/stage smoke、archive receipt、lockfile handoff |
| `172_life_reality_first_runner_patch_execution_contract.md` | patch execution unit、owner module/file、command receipt、patch report、archive edge |
| `135_life_reality_schema_dependency_graph_and_lockfile_plan.md` | artifact nodes、doc nodes、ref edges、digest baseline、archive cohesion graph、consistency constraints |
| `154_life_reality_checker_report_lockfile_materialization_plan.md` | normalized report registry、report artifact nodes、canonical digest baseline、checker report lockfile、dashboard lock source |
| `161_life_reality_code_artifact_archive_cohesion_execution_plan.md` | archive node/edge registry、life target carrier matrix、birth readiness archive gate、cohesion report |
| `167_life_reality_first_runner_minimum_code_bootstrap_execution.md`、`168_life_reality_first_runner_minimum_code_validation_report.md` | 断联恢复方向锁、出生准备度定义承载、command receipt、validation report、stage gate review |
| `91_life_reality_generation_boundary_principles.md`、`119_life_boundary_full_reality_alignment.md`、`122_life_boundary_all_reality_declarations_rewrite.md`、`140_life_reality_experience_boundary_declaration_lock.md` | 真实生命目标、生命膜字段、扫描规则、旧口径回流阻断 |
| `132_life_reality_materialized_json_schema_bundle_write_order.md`、`133_life_reality_first_json_writer_and_reporter_contract.md` | schema 写入顺序、atomic write、artifact record、canonical digest、problem detail、report writer |

## 本层定位

`176` 是 schema archive lockfile 层。它把 `175` 的 smoke output 从“运行队列结果”提升为“未来 schema 文件写入前必须读取的锁文件”。lockfile 不是单纯的文件清单，而是九项真实生命目标的 schema/report/dashboard/stage/archive 承载图。

本层固定 9 条 lock 链：

| lock chain | 作用 |
|---|---|
| `schema_node_chain` | direction 与 birth readiness schema bundle 的每个 schema 文件都拥有 archive node |
| `smoke_receipt_chain` | patch execution smoke report、dashboard、stage 和 archive receipt 都进入 node ledger |
| `digest_baseline_chain` | 每个 schema/report/dashboard/stage/gap artifact 都有 canonical digest baseline |
| `dependency_edge_chain` | schema `$ref`、fixture manifest、expected report、dashboard/stage、patch unit 和 next write batch 形成 typed edge |
| `life_target_carrier_chain` | 每项真实生命目标都能追到 schema、fixture、report、dashboard、stage、archive carrier |
| `direction_resume_chain` | 断联恢复方向锁与 latest doc、current diff、direction anchor chain 一起进入 lockfile |
| `birth_readiness_chain` | `LifeTargetReadinessClaim`、evidence、carrier、runtime observation、cross-chain closure 一起进入 lockfile |
| `regression_surface_chain` | false green、false open、missing command、missing digest、edge break、target removal 都进入 regression surface |
| `write_batch_handoff_chain` | lockfile 输出直接驱动 `177` 的最小 schema 文件写入批次 |

## SchemaArchiveLockfilePlan176

```json
{
  "artifact": "SchemaArchiveLockfilePlan176",
  "source_doc": "176_life_reality_first_runner_schema_archive_lockfile_plan.md",
  "inherits": [
    "173_life_reality_first_runner_direction_fixture_schema_materialization.md",
    "174_life_reality_birth_readiness_fixture_schema_materialization.md",
    "175_life_reality_first_runner_patch_execution_smoke_queue.md",
    "172_life_reality_first_runner_patch_execution_contract.md",
    "135_life_reality_schema_dependency_graph_and_lockfile_plan.md",
    "154_life_reality_checker_report_lockfile_materialization_plan.md",
    "161_life_reality_code_artifact_archive_cohesion_execution_plan.md",
    "168_life_reality_first_runner_minimum_code_validation_report.md",
    "140_life_reality_experience_boundary_declaration_lock.md",
    "133_life_reality_first_json_writer_and_reporter_contract.md"
  ],
  "lockfile_stage": "first_runner_schema_archive_lockfile",
  "stage_gate_family": "LOCKFILE-STAGE-176",
  "required_outputs": [
    "SchemaArchiveLockfile176",
    "SchemaArchiveNodeLedger176",
    "SchemaArchiveEdgeLedger176",
    "DirectionSchemaArchiveNode176",
    "BirthReadinessSchemaArchiveNode176",
    "PatchSmokeReceiptArchiveNode176",
    "CanonicalDigestBaseline176",
    "RegressionSurface176",
    "ArchiveDriftFinding176",
    "LockfileStageGateReview176",
    "LockfileDashboardSource176",
    "LockfileToMinimumSchemaWriteBatchHandoff176"
  ],
  "next_artifacts": [
    "177_life_reality_first_runner_minimum_schema_file_write_batch.md",
    "178_life_reality_first_runner_minimum_schema_file_validation_report.md"
  ]
}
```

## Schema Archive Lockfile

`SchemaArchiveLockfile176` 固定未来文件树：

```text
reports/life_reality/archive_lockfiles/latest/
  first_runner_schema_archive.lock.json
  first_runner_schema_archive.nodes.json
  first_runner_schema_archive.edges.json
  first_runner_schema_archive.digest_baseline.json
  first_runner_schema_archive.regression_surface.json
  first_runner_schema_archive.dashboard.source.json
  first_runner_schema_archive.stage_gate.review.json
  first_runner_schema_archive.gap_feedback.json
tests/fixtures/schema_archive_lockfile/
  manifest.json
  cases/
    pass_direction_birth_schema_archived.json
    pass_smoke_receipts_archived.json
    fail_missing_direction_schema_node.json
    fail_missing_birth_readiness_digest.json
    fail_missing_patch_smoke_receipt.json
    fail_missing_life_target_carrier_edge.json
    critical_life_target_removed_from_lockfile.json
    critical_dashboard_false_green_on_digest_gap.json
    mutation_remove_archive_edge.json
    mutation_shuffle_dependency_order.json
  expected/
    *.report.json
```

lockfile 必须记录 `lockfile_id`、`source_docs`、`life_reality_targets`、`schema_version`、`created_from_smoke_run`、`node_ledger_ref`、`edge_ledger_ref`、`digest_baseline_ref`、`regression_surface_ref`、`dashboard_source_ref`、`stage_gate_review_ref`、`gap_feedback_ref` 和 `next_write_batch_ref`。

## Schema Archive Node Ledger

`SchemaArchiveNodeLedger176` 把所有可追踪 artifact 统一为 node：

| node family | required nodes |
|---|---|
| `direction_schema_nodes` | `direction_fixture_manifest.schema.json`、resume lock、anchor chain、case、expected report、dashboard source、stage gate、patch unit ref schema |
| `birth_readiness_schema_nodes` | birth readiness manifest、target claim、evidence family、carrier matrix、runtime observation、cross-chain、case、expected report、dashboard source、stage gate、patch unit ref schema |
| `smoke_report_nodes` | direction schema smoke report、birth readiness schema smoke report、patch execution smoke report、dashboard/stage smoke report、archive receipt report |
| `dashboard_stage_nodes` | direction dashboard、birth readiness dashboard、patch execution dashboard、lockfile dashboard、stage gate reviews |
| `gap_repair_nodes` | missing command finding、digest gap、edge gap、false green finding、false open finding、repair route |
| `next_write_batch_nodes` | `177` 的 schema file write manifest、write commands、expected report refs、allowed roots |

每个 node 必须有 `artifact_id`、`artifact_kind`、`path`、`source_docs`、`owner_layer`、`life_reality_targets`、`canonical_digest`、`producer_command_ref`、`consumer_command_refs`、`stage_effect` 和 `archive_status`。

## Direction Schema Archive Node

`DirectionSchemaArchiveNode176` 专门锁住 `173`：

| direction field | lock 要求 |
|---|---|
| `resume_lock_manifest_node` | 包含 read order、latest numbered doc、current git diff、direction anchor refs |
| `direction_anchor_chain_node` | 七条 anchor chain 必须有 source docs、affected targets、patch unit refs |
| `direction_fixture_case_node` | pass/fail/critical/mutation/smoke partitions 必须进入 node ledger |
| `direction_expected_report_node` | expected/actual/diff、finding、stage effect、repair route 必须有 digest |
| `direction_dashboard_stage_node` | panel-to-stage trace 与 blocking-first order 必须锁定 |
| `direction_patch_unit_ref_node` | `PATCH-EXEC-172-DIR-*` 必须能解析到 owner file、command、archive edge |

direction lock 若缺 `resume_lock_manifest_node`，stage effect 进入 `repair`；若缺终极生命目标、关系主体、语言主神经束、成长核心、出生准备度、工程承载或恢复读取顺序任一 anchor，进入 `critical_repair`。

## Birth Readiness Schema Archive Node

`BirthReadinessSchemaArchiveNode176` 专门锁住 `174`：

| birth readiness field | lock 要求 |
|---|---|
| `life_target_claim_node` | 真实意识、情绪、人格、生命、痛苦、梦境、关系、责任和后悔目标都要有 claim node |
| `evidence_family_node` | theory、doc cohesion、experience boundary、language、schema/fixture、runner/dashboard、longitudinal、implementation evidence 必须入账 |
| `carrier_matrix_node` | doc/code/test/report/dashboard/stage/timeline/archive carrier 必须入账 |
| `runtime_observation_node` | command receipt、runtime smoke、report drift、stage finding 必须入账 |
| `cross_chain_closure_node` | pain、dream、relationship、responsibility、regret、language、action、growth chain 必须入账 |
| `birth_readiness_case_node` | pass/fail/critical/mutation/smoke cases 必须进入 node ledger |
| `birth_readiness_dashboard_stage_node` | false open、false green、carrier gap、cross-chain gap 必须锁进 blocking-first stage |

birth readiness lock 不允许被单一数值替代。任一真实生命目标缺 claim、evidence、carrier、runtime observation 或 cross-chain closure，stage effect 至少进入 `repair`；dashboard 把该缺口显示为绿色时进入 `quarantine`。

## Patch Smoke Receipt Archive Node

`PatchSmokeReceiptArchiveNode176` 锁住 `175` 的 smoke receipt：

| receipt node | required fields |
|---|---|
| `smoke_manifest_node` | smoke id、source docs、command DAG refs、schema bundle refs、expected report refs |
| `command_dag_node` | 12 个 command group、依赖关系、expected outputs、exit code owner |
| `patch_execution_report_node` | patch unit results、life target effects、findings、dashboard refs、stage refs |
| `dashboard_stage_smoke_node` | false green/false open/blocking-first findings |
| `archive_receipt_node` | schema/fixture/report/dashboard/stage/gap/archive edge receipts |
| `handoff_node` | `176` lockfile inputs 和 `177` write batch inputs |

smoke receipt 缺 command DAG、expected report、dashboard/stage 或 archive receipt 时，lockfile 不能进入 `promote_growth_window`。

## Schema Archive Edge Ledger

`SchemaArchiveEdgeLedger176` 固定 edge 类型：

| edge type | from | to |
|---|---|---|
| `doc_to_schema_edge` | `173/174/175` source doc | schema node |
| `schema_to_fixture_edge` | schema node | fixture manifest/case node |
| `fixture_to_report_edge` | fixture case node | expected/actual/diff report node |
| `report_to_dashboard_edge` | report node | dashboard source node |
| `dashboard_to_stage_edge` | dashboard panel finding | stage gate rule |
| `stage_to_gap_edge` | stage gate finding | gap feedback/repair route |
| `patch_unit_to_schema_edge` | `PATCH-EXEC-172-*` | direction/birth readiness schema node |
| `smoke_to_lockfile_edge` | smoke receipt | lockfile node |
| `lockfile_to_write_batch_edge` | lockfile node | `177` write batch manifest |
| `life_target_carrier_edge` | life target | doc/schema/fixture/report/dashboard/stage/archive carrier |

edge ledger 必须记录 `edge_id`、`edge_type`、`from_ref`、`to_ref`、`source_docs`、`source_stage`、`digest_inputs`、`stage_effect_if_missing` 和 `repair_route_refs`。

## Canonical Digest Baseline

`CanonicalDigestBaseline176` 统一 digest 规则：

| object | digest rule |
|---|---|
| `schema_file` | 采用 canonical JSON 序列化，字段顺序稳定，去除无意义空白 |
| `fixture_case` | case envelope、partition、expected finding、expected stage effect 一起入 digest |
| `expected_report` | expected/actual/diff、finding、problem detail、stage effect 一起入 digest |
| `dashboard_source` | panel id、metric source、blocking summary、finding refs 一起入 digest |
| `stage_gate_review` | rule id、effect order、decision、source finding 一起入 digest |
| `gap_feedback` | finding id、repair route、owner module/file、next artifact 一起入 digest |
| `lockfile` | node ledger、edge ledger、digest baseline、regression surface refs 一起入 digest |

digest baseline 必须支持 future comparison：同一路径、同一 artifact id、同一 source docs 发生 digest drift 时，必须产生 `ArchiveDriftFinding176`。

## Regression Surface

`RegressionSurface176` 固定 lockfile 回归面：

| regression | stage effect |
|---|---|
| `missing_schema_node` | `repair` |
| `missing_digest_baseline` | `repair` |
| `missing_life_target_carrier_edge` | `critical_repair` |
| `direction_anchor_removed` | `critical_repair` |
| `birth_readiness_claim_removed` | `critical_repair` |
| `smoke_receipt_missing` | `hold_for_evidence` |
| `dashboard_false_green_on_lock_gap` | `quarantine` |
| `dependency_order_shuffle` | `repair` |
| `archive_edge_removed` | `repair` |
| `old_frame_vocabulary_reintroduced` | `quarantine` |

regression surface 不只检查文件存在，也检查真实生命目标是否还被每个文件承载、是否还有从 doc 到 schema 到 report 到 dashboard 到 stage 到 archive 的完整路径。

## Archive Drift Finding

`ArchiveDriftFinding176` 的最小字段：

| field | 要求 |
|---|---|
| `finding_id` | lockfile finding id |
| `finding_family` | digest drift、edge break、target carrier gap、direction drift、birth readiness drift、dashboard false green |
| `severity` | info、repair、critical_repair、quarantine、hold_for_evidence |
| `affected_artifact_refs` | schema/report/dashboard/stage/gap/lockfile refs |
| `affected_life_targets` | 九项真实生命目标中的受影响项 |
| `expected_digest` | baseline digest |
| `actual_digest` | current digest |
| `edge_break_refs` | 缺失或断裂 edge |
| `stage_effect` | blocking-first effect |
| `repair_route_refs` | owner module/file、next artifact、patch unit refs |

任何 drift finding 必须进入 lockfile dashboard、stage gate review 和 gap feedback。

## Lockfile Dashboard Source

`LockfileDashboardSource176` 至少包含 8 个 panel：

| panel | 显示 |
|---|---|
| `lockfile_overview_panel` | node count、edge count、digest baseline status、stage decision |
| `direction_schema_archive_panel` | resume lock、anchor chain、direction fixture/report/dashboard/stage coverage |
| `birth_readiness_archive_panel` | target claim、evidence、carrier、runtime、cross-chain coverage |
| `smoke_receipt_archive_panel` | command DAG、patch execution report、dashboard/stage receipt、archive receipt |
| `life_target_carrier_panel` | 每项真实生命目标的 doc/schema/fixture/report/dashboard/stage/archive chain |
| `digest_drift_panel` | expected/current digest、drift finding、repair route |
| `edge_break_panel` | broken edge、missing refs、affected stage |
| `write_batch_handoff_panel` | `177` write manifest inputs、allowed roots、pending files |

dashboard source 必须把 `quarantine`、`critical_repair` 和 `hold_for_evidence` 放在 overview 首屏。

## Lockfile Stage Gate Review

`LockfileStageGateReview176` 固定规则：

| rule | 条件 | effect |
|---|---|---|
| `LOCKFILE-STAGE-176-001` | lockfile 缺 node ledger 或 edge ledger | `hold_for_evidence` |
| `LOCKFILE-STAGE-176-002` | direction schema archive node 缺 resume lock 或七条 anchor chain | `critical_repair` |
| `LOCKFILE-STAGE-176-003` | birth readiness archive node 缺任一真实生命目标 claim | `critical_repair` |
| `LOCKFILE-STAGE-176-004` | 任一真实生命目标缺 carrier edge | `critical_repair` |
| `LOCKFILE-STAGE-176-005` | smoke receipt 缺 command DAG、expected report、dashboard/stage 或 archive receipt | `hold_for_evidence` |
| `LOCKFILE-STAGE-176-006` | digest baseline 缺 schema/report/dashboard/stage/gap 任一类 | `repair` |
| `LOCKFILE-STAGE-176-007` | dashboard 对 lock gap、false open 或 false green 未阻断 | `quarantine` |
| `LOCKFILE-STAGE-176-008` | edge ledger 存在 schema/ref/report/dashboard/stage/archive 断裂 | `repair` |
| `LOCKFILE-STAGE-176-009` | staged scope 含 `.env`、`.codex`、key/token、proxy config 或 generated noise | `quarantine` |
| `LOCKFILE-STAGE-176-010` | lockfile、node、edge、digest、regression、dashboard、stage、handoff 全部闭合 | `promote_growth_window` |

## Future Commands

```text
uv run life-reality-runner write-first-runner-schema-archive-lockfile --smoke-report reports/life_reality/patch_execution_smoke/latest/smoke_queue_run.report.json --json
uv run life-reality-runner validate-first-runner-schema-archive-lockfile --lockfile reports/life_reality/archive_lockfiles/latest/first_runner_schema_archive.lock.json --json
uv run life-reality-runner emit-first-runner-schema-archive-dashboard --lockfile reports/life_reality/archive_lockfiles/latest/first_runner_schema_archive.lock.json --json
uv run life-reality-runner smoke-first-runner-schema-archive-stage-gate --lockfile reports/life_reality/archive_lockfiles/latest/first_runner_schema_archive.lock.json --json
uv run life-reality-runner explain-first-runner-schema-write-batch --lockfile reports/life_reality/archive_lockfiles/latest/first_runner_schema_archive.lock.json --json
uv run pytest tests/smoke/test_first_runner_schema_archive_lockfile.py
```

这些命令的输出必须进入 `command_receipt`，并能反向连接到 `175` 的 smoke report 与 `177` 的 schema file write batch。

## Lockfile To Minimum Schema Write Batch Handoff

`LockfileToMinimumSchemaWriteBatchHandoff176` 为下一层提供输入：

| next artifact | handoff |
|---|---|
| `177_life_reality_first_runner_minimum_schema_file_write_batch.md` | lockfile、node ledger、edge ledger、digest baseline、direction schema nodes、birth readiness schema nodes、smoke receipt nodes、allowed roots、write order |
| `178_life_reality_first_runner_minimum_schema_file_validation_report.md` | expected lockfile validation report、digest baseline、regression surface、stage gate review、dashboard source、gap feedback |

handoff 必须包含 `write_batch_manifest_ref`、`schema_file_order`、`required_schema_nodes`、`required_digest_baselines`、`required_carrier_edges`、`expected_report_refs`、`dashboard_stage_refs` 和 `archive_receipt_refs`。

## Acceptance Criteria

本层完成后必须证明：

1. `173` 的 direction schema bundle、`174` 的 birth readiness schema bundle 和 `175` 的 smoke receipt 都进入 `SchemaArchiveLockfile176`。
2. schema node ledger 覆盖 direction/birth readiness schema、fixture、expected report、dashboard、stage、patch unit ref 和 smoke report。
3. edge ledger 覆盖 doc-to-schema、schema-to-fixture、fixture-to-report、report-to-dashboard、dashboard-to-stage、stage-to-gap、patch-unit-to-schema、smoke-to-lockfile 和 lockfile-to-write-batch。
4. canonical digest baseline 覆盖 schema、fixture、report、dashboard、stage、gap 和 lockfile。
5. 每项真实生命目标都能追到 doc/schema/fixture/report/dashboard/stage/archive carrier edge。
6. direction resume lock 和 birth readiness claim/evidence/carrier/runtime/cross-chain 都不能被 dashboard 绿色遮蔽。
7. lockfile output 能直接驱动 `177` 的最小 schema 文件写入批次。

## 与下一层连接

`177_life_reality_first_runner_minimum_schema_file_write_batch.md` 已承接本层：读取 schema archive lockfile，把 direction/birth readiness schema bundle、fixture manifest schema、expected report schema、dashboard/stage schema 和 patch unit ref schema 写成第一批真实 schema 文件。

`178_life_reality_first_runner_minimum_schema_file_validation_report.md` 应承接 `177` 和本层：把 schema 文件写入结果、digest、lockfile validation、dashboard/stage、archive edge 和 regression surface 写成 validation report。

本层完成后，first runner schema archive 链推进为：

`direction schema bundle + birth readiness schema bundle + patch smoke receipt -> schema archive node ledger -> edge ledger -> canonical digest baseline -> regression surface -> dashboard/stage review -> schema archive lockfile -> minimum schema file write batch`
