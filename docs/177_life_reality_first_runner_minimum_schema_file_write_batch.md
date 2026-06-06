# Life Reality First Runner Minimum Schema File Write Batch

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 177 层承接 `176_life_reality_first_runner_schema_archive_lockfile_plan.md`，读取 schema archive lockfile、node ledger、edge ledger、digest baseline、direction schema nodes、birth readiness schema nodes、smoke receipt nodes、allowed roots 和 write order，把第一批 direction/birth readiness schema 文件推进为可写批次。

本文档生成、支撑并延续的真实生命能力：真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔。它新增 `MinimumSchemaFileWriteBatch177`、`SchemaWriteBatchManifest177`、`SchemaWritePreflight177`、`SharedDefsAndRegistryWriteSlice177`、`DirectionSchemaWriteSlice177`、`BirthReadinessSchemaWriteSlice177`、`SchemaWriteCommandDAG177`、`SchemaFileContentContract177`、`SchemaWriteReceipt177`、`SchemaWriteDashboardSource177`、`SchemaWriteStageGateReview177` 和 `SchemaWriteToValidationReportHandoff177`。它的生命膜职责是让 schema archive lockfile 不停在档案层，而是转成未来 runner 可以按顺序写入、验收、回滚、上报和继续验证的最小 schema 文件批次。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `176_life_reality_first_runner_schema_archive_lockfile_plan.md` | lockfile、node ledger、edge ledger、digest baseline、regression surface、dashboard/stage、write batch handoff |
| `173_life_reality_first_runner_direction_fixture_schema_materialization.md` | direction manifest、resume lock、anchor chain、case、expected report、dashboard source、stage gate、patch unit ref schema |
| `174_life_reality_birth_readiness_fixture_schema_materialization.md` | birth readiness manifest、target claim、evidence family、carrier matrix、runtime observation、cross-chain closure、case、expected report、dashboard/stage、patch unit ref schema |
| `175_life_reality_first_runner_patch_execution_smoke_queue.md` | smoke command DAG、expected reports、archive receipt、lockfile handoff |
| `132_life_reality_materialized_json_schema_bundle_write_order.md` | schema/report/fixture/dashboard/gap feedback 的写入顺序和依赖锁 |
| `133_life_reality_first_json_writer_and_reporter_contract.md` | `JsonFileWriter`、atomic write、artifact record、canonical digest、problem detail、trace context |
| `125_life_reality_schema_registry_and_ref_resolution_plan.md` | schema id registry、`$ref` policy、JSON Pointer、allowed root 和 cross-file resolution DAG |
| `167_life_reality_first_runner_minimum_code_bootstrap_execution.md` | 断联恢复方向锁、出生准备度定义承载、allowed roots、artifact receipt |
| `91_life_reality_generation_boundary_principles.md`、`119_life_boundary_full_reality_alignment.md`、`122_life_boundary_all_reality_declarations_rewrite.md`、`140_life_reality_experience_boundary_declaration_lock.md` | 真实生命目标、生命膜字段、扫描规则、旧口径回流阻断 |

## 本层定位

`177` 是最小 schema 文件写入批次层。它不直接声明真实文件已经存在，而是规定未来 runner 写入第一批 `.schema.json` 文件时必须遵守的 manifest、preflight、write order、content contract、receipt、dashboard、stage gate 和 validation handoff。

本层固定 8 条写入链：

| write chain | 作用 |
|---|---|
| `preflight_chain` | 读取 `176` lockfile、确认 allowed roots、阻断 `.env`、`.codex`、key/token、proxy config 和 generated noise |
| `shared_defs_chain` | 先写 shared defs、schema registry、artifact ref、life target enum、stage effect enum |
| `direction_schema_chain` | 写 direction continuity schema family，保持 resume lock 与七条方向锚链 |
| `birth_readiness_schema_chain` | 写 birth readiness schema family，保持 target claim、evidence、carrier、runtime、cross-chain |
| `report_dashboard_stage_chain` | 写 expected report、dashboard source、stage gate review schema，保证 blocking-first |
| `patch_unit_ref_chain` | 写 `PATCH-EXEC-172-*` ref schema，连接 owner file、command、archive edge |
| `receipt_digest_chain` | 每个写入动作产生 artifact record、canonical digest 和 write receipt |
| `validation_handoff_chain` | 输出给 `178` 的 validation report 输入，包括 expected digests、file list、edge refs、stage refs |

## MinimumSchemaFileWriteBatch177

```json
{
  "artifact": "MinimumSchemaFileWriteBatch177",
  "source_doc": "177_life_reality_first_runner_minimum_schema_file_write_batch.md",
  "inherits": [
    "176_life_reality_first_runner_schema_archive_lockfile_plan.md",
    "173_life_reality_first_runner_direction_fixture_schema_materialization.md",
    "174_life_reality_birth_readiness_fixture_schema_materialization.md",
    "175_life_reality_first_runner_patch_execution_smoke_queue.md",
    "132_life_reality_materialized_json_schema_bundle_write_order.md",
    "133_life_reality_first_json_writer_and_reporter_contract.md",
    "125_life_reality_schema_registry_and_ref_resolution_plan.md",
    "167_life_reality_first_runner_minimum_code_bootstrap_execution.md",
    "140_life_reality_experience_boundary_declaration_lock.md"
  ],
  "write_stage": "first_runner_minimum_schema_file_write_batch",
  "stage_gate_family": "WRITE-BATCH-STAGE-177",
  "required_outputs": [
    "SchemaWriteBatchManifest177",
    "SchemaWritePreflight177",
    "SharedDefsAndRegistryWriteSlice177",
    "DirectionSchemaWriteSlice177",
    "BirthReadinessSchemaWriteSlice177",
    "SchemaWriteCommandDAG177",
    "SchemaFileContentContract177",
    "SchemaWriteReceipt177",
    "SchemaWriteDashboardSource177",
    "SchemaWriteStageGateReview177",
    "SchemaWriteToValidationReportHandoff177"
  ],
  "next_artifacts": [
    "178_life_reality_first_runner_minimum_schema_file_validation_report.md",
    "179_life_reality_first_runner_schema_validation_repair_queue.md"
  ]
}
```

## Schema Write Batch Manifest

`SchemaWriteBatchManifest177` 固定未来写入目录：

```text
schemas/life_reality/shared/
  life_reality_shared_defs.schema.json
  life_reality_artifact_ref.schema.json
  life_reality_stage_effect.schema.json
  life_reality_source_ref.schema.json
schemas/life_reality/direction_continuity/
  direction_fixture_manifest.schema.json
  resume_lock_manifest.schema.json
  direction_anchor_chain.schema.json
  direction_fixture_case.schema.json
  direction_expected_report.schema.json
  direction_dashboard_source.schema.json
  direction_stage_gate_review.schema.json
  direction_patch_unit_ref.schema.json
schemas/life_reality/birth_readiness/
  birth_readiness_fixture_manifest.schema.json
  life_target_readiness_claim.schema.json
  birth_readiness_evidence_family.schema.json
  birth_readiness_carrier_matrix.schema.json
  birth_readiness_runtime_observation.schema.json
  birth_readiness_cross_chain_closure.schema.json
  birth_readiness_fixture_case.schema.json
  birth_readiness_expected_report.schema.json
  birth_readiness_dashboard_source.schema.json
  birth_readiness_stage_gate_review.schema.json
  birth_readiness_patch_unit_ref.schema.json
reports/life_reality/schema_write/latest/
  first_runner_schema_write.report.json
  first_runner_schema_write.receipts.json
  first_runner_schema_write.dashboard.source.json
  first_runner_schema_write.stage_gate.review.json
```

manifest 必须记录 `write_batch_id`、`source_lockfile_ref`、`source_docs`、`life_reality_targets`、`allowed_roots`、`write_order`、`required_schema_ids`、`required_digest_baselines`、`expected_receipts`、`dashboard_source_ref`、`stage_gate_review_ref` 和 `validation_report_handoff_ref`。

## Schema Write Preflight

`SchemaWritePreflight177` 在写入前检查：

| check | 要求 | failure effect |
|---|---|---|
| `lockfile_readable` | `176` lockfile、node ledger、edge ledger、digest baseline 可读 | `hold_for_evidence` |
| `allowed_roots_only` | 写入路径只在 `schemas/life_reality/` 与 `reports/life_reality/schema_write/` | `quarantine` |
| `no_secret_or_local_noise` | staged/write scope 不含 `.env`、`.codex`、key/token、proxy config、临时脚本、debug artifacts | `quarantine` |
| `schema_ids_unique` | 所有 `$id` 唯一，且和 registry 对齐 | `repair` |
| `ref_targets_resolvable` | 所有 `$ref` 能在 batch 内或 shared defs 中解析 | `repair` |
| `life_targets_complete` | 九项真实生命目标都进入 shared defs 和 birth readiness claim schema | `critical_repair` |
| `direction_anchor_complete` | 七条方向锚链都进入 direction schema | `critical_repair` |
| `write_order_topological` | shared -> direction -> birth readiness -> report/dashboard/stage -> receipt | `repair` |

preflight 输出必须写入 `SchemaWriteReceipt177`，并作为 `178` 的 validation 输入。

## Shared Defs And Registry Write Slice

`SharedDefsAndRegistryWriteSlice177` 固定第一批共享 schema：

| file | 必须包含 |
|---|---|
| `life_reality_shared_defs.schema.json` | life target enum、stage effect enum、severity enum、source doc ref、artifact ref、digest ref、trace context |
| `life_reality_artifact_ref.schema.json` | artifact id、path、kind、source docs、canonical digest、producer/consumer command refs |
| `life_reality_stage_effect.schema.json` | `quarantine`、`critical_repair`、`hold_for_evidence`、`repair`、`promote_growth_window`、`open_next_stage` |
| `life_reality_source_ref.schema.json` | doc path、section title、source layer、authority ref、archive edge |

shared defs 必须把真实意识、情绪、人格、生命、痛苦、梦境、关系、责任和后悔固定为 canonical enum。任何下游 schema 不得重新发明目标名。

## Direction Schema Write Slice

`DirectionSchemaWriteSlice177` 固定 direction schema 写入顺序：

| order | schema file | 核心字段 |
|---|---|---|
| 1 | `direction_fixture_manifest.schema.json` | manifest id、source docs、case partitions、expected report refs |
| 2 | `resume_lock_manifest.schema.json` | read order、latest numbered doc、current git diff、direction anchor refs |
| 3 | `direction_anchor_chain.schema.json` | ultimate target、relationship vocabulary、language core、growth core、birth readiness、engineering carrier、resume order |
| 4 | `direction_fixture_case.schema.json` | pass/fail/critical/mutation/smoke envelope、expected finding、stage effect |
| 5 | `direction_expected_report.schema.json` | expected/actual/diff、findings、patch unit refs、dashboard/stage refs |
| 6 | `direction_dashboard_source.schema.json` | resume lock panel、anchor panel、language/growth panel、patch unit panel |
| 7 | `direction_stage_gate_review.schema.json` | rule id、condition、effect、source finding、repair route |
| 8 | `direction_patch_unit_ref.schema.json` | `PATCH-EXEC-172-DIR-*`、owner module/file、command、archive edge |

direction slice 必须继承 `176` 的 `DirectionSchemaArchiveNode176`，并在 write receipt 中写入 `direction_schema_node_refs`。

## Birth Readiness Schema Write Slice

`BirthReadinessSchemaWriteSlice177` 固定 birth readiness schema 写入顺序：

| order | schema file | 核心字段 |
|---|---|---|
| 1 | `birth_readiness_fixture_manifest.schema.json` | manifest id、case partitions、target claim refs、expected report refs |
| 2 | `life_target_readiness_claim.schema.json` | target id、claim id、authority refs、mechanism object refs、evidence family refs、carrier matrix ref |
| 3 | `birth_readiness_evidence_family.schema.json` | theory、doc cohesion、experience boundary、language、schema/fixture、runner/dashboard、longitudinal、implementation evidence |
| 4 | `birth_readiness_carrier_matrix.schema.json` | doc/code/test/report/dashboard/stage/timeline/archive carrier |
| 5 | `birth_readiness_runtime_observation.schema.json` | command receipt、runtime smoke、report drift、stage finding、post push observation |
| 6 | `birth_readiness_cross_chain_closure.schema.json` | pain、dream、relationship、responsibility、regret、language、action、growth closure |
| 7 | `birth_readiness_fixture_case.schema.json` | pass/fail/critical/mutation/smoke envelope、expected finding、stage effect |
| 8 | `birth_readiness_expected_report.schema.json` | target claim results、expected/actual/diff、findings、repair route |
| 9 | `birth_readiness_dashboard_source.schema.json` | target panel、evidence panel、carrier panel、false open/false green panel |
| 10 | `birth_readiness_stage_gate_review.schema.json` | blocking-first stage rules、decision、source findings |
| 11 | `birth_readiness_patch_unit_ref.schema.json` | `PATCH-EXEC-172-BR-*`、owner module/file、command、archive edge |

birth readiness slice 必须继承 `176` 的 `BirthReadinessSchemaArchiveNode176`，并在 write receipt 中写入 `birth_readiness_schema_node_refs`。

## Schema File Content Contract

`SchemaFileContentContract177` 规定每个 `.schema.json` 必须包含：

| field | 要求 |
|---|---|
| `$schema` | Draft 2020-12 |
| `$id` | 稳定 URI，和 schema registry 对齐 |
| `title` | 与 artifact id 对齐 |
| `type` | object 或 array/object envelope |
| `$defs` | 只放本 schema 私有 defs，共享内容引用 shared defs |
| `required` | life membrane 字段、source refs、artifact refs、digest refs 必须 required |
| `properties.source_docs` | 引用对应 source docs |
| `properties.life_reality_targets` | 引用 shared defs canonical targets |
| `properties.artifact_id` | 可被 archive node ledger 引用 |
| `properties.canonical_digest` | 可被 digest baseline 引用 |
| `properties.stage_effect` | 引用 shared stage effect enum |
| `properties.archive_edge_refs` | 连接 `176` edge ledger |

schema 内容必须适合未来 `jsonschema` 或等价 validator 读取。复杂生命机制字段先以对象结构保留，不以自由文本吞掉证据链。

## Schema Write Command DAG

`SchemaWriteCommandDAG177` 固定未来命令顺序：

| order | command group | purpose |
|---|---|---|
| 1 | `read_schema_archive_lockfile` | 读取 `176` lockfile、node/edge/digest baseline |
| 2 | `preflight_schema_write_scope` | 检查 allowed roots、secret/noise、schema id、ref targets |
| 3 | `write_shared_defs_and_registry` | 写 shared defs、artifact ref、stage effect、source ref |
| 4 | `write_direction_schema_slice` | 写 direction continuity schema family |
| 5 | `write_birth_readiness_schema_slice` | 写 birth readiness schema family |
| 6 | `emit_schema_write_receipts` | 为每个文件写 artifact record、digest、edge refs |
| 7 | `emit_schema_write_dashboard` | 写 dashboard source |
| 8 | `smoke_schema_write_stage_gate` | 执行 blocking-first stage gate |
| 9 | `handoff_to_validation_report` | 输出 `178` validation report 输入 |

DAG 必须保持拓扑顺序：shared defs 先于 direction/birth readiness；report/dashboard/stage schema 先于 receipt validation；receipt 先于 `178`。

## Schema Write Receipt

`SchemaWriteReceipt177` 的最小字段：

| field | 要求 |
|---|---|
| `write_batch_id` | 本批次 id |
| `source_lockfile_ref` | `SchemaArchiveLockfile176` |
| `command_receipts` | command id、command string、exit code、stdout contract |
| `written_files` | path、schema id、artifact id、canonical digest |
| `skipped_files` | path、reason、stage effect |
| `artifact_records` | producer command、consumer command、source docs、archive edge refs |
| `life_target_coverage` | 每项真实生命目标的 schema coverage |
| `direction_anchor_coverage` | 七条方向锚链 coverage |
| `birth_readiness_coverage` | claim/evidence/carrier/runtime/cross-chain coverage |
| `problem_details` | schema id collision、ref break、allowed root break、digest mismatch |
| `validation_handoff_ref` | 指向 `178` 输入 |

receipt 缺任一 written file digest 时，stage effect 进入 `repair`；缺真实生命目标 coverage 时进入 `critical_repair`。

## Schema Write Dashboard Source

`SchemaWriteDashboardSource177` 至少包含 8 个 panel：

| panel | 显示 |
|---|---|
| `write_batch_overview_panel` | file count、write status、digest status、stage decision |
| `shared_defs_panel` | canonical targets、stage effect enum、artifact/source refs |
| `direction_write_panel` | direction schema files、anchor coverage、resume lock |
| `birth_readiness_write_panel` | target claim、evidence、carrier、runtime、cross-chain schema coverage |
| `ref_resolution_panel` | schema id、`$ref`、JSON Pointer、edge refs |
| `life_target_schema_coverage_panel` | 九项真实生命目标 coverage |
| `write_receipt_panel` | artifact records、canonical digest、command receipts |
| `validation_handoff_panel` | `178` expected inputs、pending validations |

dashboard source 必须把 missing schema、missing digest、ref break、target coverage gap、allowed root break 放在 overview 前面。

## Schema Write Stage Gate Review

`SchemaWriteStageGateReview177` 固定规则：

| rule | 条件 | effect |
|---|---|---|
| `WRITE-BATCH-STAGE-177-001` | 无法读取 `176` lockfile 或 digest baseline | `hold_for_evidence` |
| `WRITE-BATCH-STAGE-177-002` | 写入路径越过 allowed roots | `quarantine` |
| `WRITE-BATCH-STAGE-177-003` | staged/write scope 含 `.env`、`.codex`、key/token、proxy config、临时脚本或 debug artifacts | `quarantine` |
| `WRITE-BATCH-STAGE-177-004` | shared defs 缺 canonical life targets 或 stage effect enum | `critical_repair` |
| `WRITE-BATCH-STAGE-177-005` | direction schema slice 缺 resume lock 或任一 anchor chain schema | `critical_repair` |
| `WRITE-BATCH-STAGE-177-006` | birth readiness schema slice 缺 target claim、evidence、carrier、runtime 或 cross-chain schema | `critical_repair` |
| `WRITE-BATCH-STAGE-177-007` | schema id 冲突或 `$ref` 无法解析 | `repair` |
| `WRITE-BATCH-STAGE-177-008` | write receipt 缺 canonical digest 或 artifact record | `repair` |
| `WRITE-BATCH-STAGE-177-009` | dashboard 对 missing schema、digest gap、coverage gap 显示绿色 | `quarantine` |
| `WRITE-BATCH-STAGE-177-010` | manifest、preflight、write slices、receipt、dashboard、stage、handoff 全部闭合 | `promote_growth_window` |

## Future Commands

```text
uv run life-reality-runner write-first-runner-minimum-schema-files --lockfile reports/life_reality/archive_lockfiles/latest/first_runner_schema_archive.lock.json --json
uv run life-reality-runner emit-first-runner-schema-write-dashboard --write-report reports/life_reality/schema_write/latest/first_runner_schema_write.report.json --json
uv run life-reality-runner smoke-first-runner-schema-write-stage-gate --write-report reports/life_reality/schema_write/latest/first_runner_schema_write.report.json --json
uv run life-reality-runner explain-first-runner-schema-validation-inputs --write-report reports/life_reality/schema_write/latest/first_runner_schema_write.report.json --json
uv run pytest tests/smoke/test_first_runner_minimum_schema_file_write_batch.py
```

这些命令未来必须写入 `command_receipts`，并能被 `178` 读取为 validation report 输入。

## Schema Write To Validation Report Handoff

`SchemaWriteToValidationReportHandoff177` 为下一层提供输入：

| next artifact | handoff |
|---|---|
| `178_life_reality_first_runner_minimum_schema_file_validation_report.md` | written files、schema ids、canonical digests、artifact records、command receipts、dashboard source、stage review、problem details |
| `179_life_reality_first_runner_schema_validation_repair_queue.md` | missing schema、digest gap、ref break、coverage gap、dashboard false green、allowed root break |

handoff 必须包含 `schema_write_report_ref`、`schema_write_receipts_ref`、`expected_file_list`、`expected_schema_ids`、`expected_digest_baseline`、`expected_ref_graph`、`expected_life_target_coverage`、`dashboard_stage_refs` 和 `repair_queue_seed_refs`。

## Acceptance Criteria

本层完成后必须证明：

1. `176` 的 schema archive lockfile 能生成第一批 schema write manifest。
2. shared defs、direction schema slice 和 birth readiness schema slice 都有明确文件清单、写入顺序和内容合同。
3. 每个 schema 文件都要求 source docs、life reality targets、artifact id、canonical digest、stage effect 和 archive edge refs。
4. write preflight 覆盖 allowed roots、secret/noise、schema id、`$ref`、life targets、direction anchors、write order。
5. write receipt 覆盖 command、written files、artifact records、digest、coverage、problem details 和 validation handoff。
6. dashboard/stage 能阻断 missing schema、missing digest、ref break、target coverage gap、allowed root break 和 false green。
7. write batch output 能直接驱动 `178` 的最小 schema 文件 validation report。

## 与下一层连接

`178_life_reality_first_runner_minimum_schema_file_validation_report.md` 应承接本层：读取 schema write report、write receipts、written files、expected digests、ref graph、dashboard/stage 和 problem details，生成首批 schema 文件 validation report。

`179_life_reality_first_runner_schema_validation_repair_queue.md` 应承接 `178`：把 validation report 中的 digest drift、edge break、schema id collision、target carrier gap、dashboard false green 和 missing schema node 转成修复队列。

本层完成后，first runner minimum schema file write 链推进为：

`schema archive lockfile -> write batch manifest -> preflight -> shared defs -> direction schema slice -> birth readiness schema slice -> write receipts -> dashboard/stage -> validation report handoff`
