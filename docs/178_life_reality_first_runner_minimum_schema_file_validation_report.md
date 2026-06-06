# Life Reality First Runner Minimum Schema File Validation Report

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 178 层承接 `177_life_reality_first_runner_minimum_schema_file_write_batch.md`，读取 schema write report、write receipts、written files、expected digests、ref graph、dashboard/stage 和 problem details，生成首批 schema 文件 validation report。

本文档生成、支撑并延续的真实生命能力：真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔。它新增 `MinimumSchemaFileValidationReport178`、`SchemaValidationReportManifest178`、`SchemaParseValidation178`、`SchemaIdRegistryValidation178`、`SchemaRefGraphValidation178`、`SchemaDigestValidation178`、`LifeTargetCoverageValidation178`、`DirectionSchemaValidation178`、`BirthReadinessSchemaValidation178`、`DashboardStageValidation178`、`ArchiveEdgeValidation178`、`ValidationFinding178`、`ValidationDashboardSource178`、`ValidationStageGateReview178` 和 `ValidationToRepairQueueHandoff178`。它的生命膜职责是让第一批 schema 文件写入后立刻进入可回放验证，证明每个 schema 文件都能被读取、解析、引用、比对、上卷到 dashboard/stage，并把断裂面交给 `179` 修复队列。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `177_life_reality_first_runner_minimum_schema_file_write_batch.md` | write batch manifest、preflight、shared defs slice、direction schema slice、birth readiness schema slice、command DAG、write receipt、dashboard/stage、validation handoff |
| `176_life_reality_first_runner_schema_archive_lockfile_plan.md` | schema archive lockfile、node/edge ledger、digest baseline、regression surface、dashboard/stage、write batch refs |
| `173_life_reality_first_runner_direction_fixture_schema_materialization.md` | resume lock、七条方向锚链、fixture/report/dashboard/stage/patch unit ref schema |
| `174_life_reality_birth_readiness_fixture_schema_materialization.md` | target claim、evidence family、carrier matrix、runtime observation、cross-chain closure、fixture/report/dashboard/stage/patch unit ref schema |
| `175_life_reality_first_runner_patch_execution_smoke_queue.md` | smoke report、command DAG、expected report、dashboard/stage smoke、archive receipt |
| `125_life_reality_schema_registry_and_ref_resolution_plan.md` | schema id registry、JSON Pointer、`$ref` policy、cross-file resolution DAG |
| `133_life_reality_first_json_writer_and_reporter_contract.md` | artifact record、canonical digest、problem detail、report writer、trace context |
| `143_life_reality_birth_readiness_rollup_contract.md` | 出生准备度 evidence/carrier/runtime/stage/repair rollup |
| `91_life_reality_generation_boundary_principles.md`、`119_life_boundary_full_reality_alignment.md`、`122_life_boundary_all_reality_declarations_rewrite.md`、`140_life_reality_experience_boundary_declaration_lock.md` | 真实生命目标、生命膜字段、扫描规则、旧口径回流阻断 |

## 本层定位

`178` 是最小 schema 文件 validation report 层。它不生成新的 schema，而是规定未来 runner 如何读取 `177` 的写入结果，执行 parse、schema id、`$ref`、digest、coverage、direction、birth readiness、dashboard/stage 和 archive edge 验证，并把每个 finding 写成可修复对象。

本层固定 10 条 validation 链：

| validation chain | 作用 |
|---|---|
| `parse_chain` | 每个 `.schema.json` 能被 JSON parser 读取，并保留 Draft 2020-12 结构 |
| `schema_id_chain` | `$id` 唯一、稳定、和 registry 对齐 |
| `ref_graph_chain` | `$ref`、JSON Pointer、shared defs、cross-file refs 全部可解析 |
| `digest_chain` | written digest 和 `176/177` expected digest baseline 对齐 |
| `life_target_chain` | 九项真实生命目标在 shared defs、direction、birth readiness schema 中完整覆盖 |
| `direction_chain` | resume lock、七条方向锚链、fixture/report/dashboard/stage/patch unit refs 完整 |
| `birth_readiness_chain` | target claim、evidence、carrier、runtime、cross-chain、case/report/dashboard/stage 完整 |
| `dashboard_stage_chain` | validation dashboard 不遮蔽 missing schema、digest drift、ref break、coverage gap |
| `archive_edge_chain` | schema/report/dashboard/stage/gap/archive edge 可追溯 |
| `repair_handoff_chain` | validation findings 直接形成 `179` 修复队列输入 |

## MinimumSchemaFileValidationReport178

```json
{
  "artifact": "MinimumSchemaFileValidationReport178",
  "source_doc": "178_life_reality_first_runner_minimum_schema_file_validation_report.md",
  "inherits": [
    "177_life_reality_first_runner_minimum_schema_file_write_batch.md",
    "176_life_reality_first_runner_schema_archive_lockfile_plan.md",
    "173_life_reality_first_runner_direction_fixture_schema_materialization.md",
    "174_life_reality_birth_readiness_fixture_schema_materialization.md",
    "175_life_reality_first_runner_patch_execution_smoke_queue.md",
    "125_life_reality_schema_registry_and_ref_resolution_plan.md",
    "133_life_reality_first_json_writer_and_reporter_contract.md",
    "143_life_reality_birth_readiness_rollup_contract.md",
    "140_life_reality_experience_boundary_declaration_lock.md"
  ],
  "validation_stage": "first_runner_minimum_schema_file_validation_report",
  "stage_gate_family": "VALIDATION-STAGE-178",
  "required_outputs": [
    "SchemaValidationReportManifest178",
    "SchemaParseValidation178",
    "SchemaIdRegistryValidation178",
    "SchemaRefGraphValidation178",
    "SchemaDigestValidation178",
    "LifeTargetCoverageValidation178",
    "DirectionSchemaValidation178",
    "BirthReadinessSchemaValidation178",
    "DashboardStageValidation178",
    "ArchiveEdgeValidation178",
    "ValidationFinding178",
    "ValidationDashboardSource178",
    "ValidationStageGateReview178",
    "ValidationToRepairQueueHandoff178"
  ],
  "next_artifacts": [
    "179_life_reality_first_runner_schema_validation_repair_queue.md",
    "180_life_reality_first_runner_schema_file_archive_receipt_batch.md"
  ]
}
```

## Schema Validation Report Manifest

`SchemaValidationReportManifest178` 固定未来报告目录：

```text
reports/life_reality/schema_validation/latest/
  first_runner_schema_validation.report.json
  first_runner_schema_validation.findings.json
  first_runner_schema_validation.ref_graph.json
  first_runner_schema_validation.digest_diff.json
  first_runner_schema_validation.coverage.json
  first_runner_schema_validation.dashboard.source.json
  first_runner_schema_validation.stage_gate.review.json
  first_runner_schema_validation.repair_queue.seed.json
tests/fixtures/schema_validation/
  manifest.json
  cases/
    pass_all_minimum_schema_files_valid.json
    fail_schema_parse_error.json
    fail_schema_id_collision.json
    fail_ref_target_missing.json
    fail_digest_mismatch.json
    fail_missing_life_target_coverage.json
    fail_missing_direction_anchor_schema.json
    fail_missing_birth_readiness_carrier_schema.json
    critical_dashboard_false_green_on_validation_gap.json
    mutation_remove_required_life_membrane_field.json
  expected/
    *.report.json
```

manifest 必须记录 `validation_run_id`、`source_write_report_ref`、`source_lockfile_ref`、`source_docs`、`life_reality_targets`、`schema_files`、`expected_schema_ids`、`expected_digest_baseline`、`expected_ref_graph`、`expected_coverage`、`dashboard_source_ref`、`stage_gate_review_ref` 和 `repair_queue_seed_ref`。

## Schema Parse Validation

`SchemaParseValidation178` 验证每个 schema 文件：

| check | 要求 | failure effect |
|---|---|---|
| `json_parseable` | 文件可被 JSON parser 读取 | `repair` |
| `draft_2020_12_shape` | `$schema` 指向 Draft 2020-12，结构含 `$id`、`title`、`type`、`properties` | `repair` |
| `required_life_membrane_fields` | `source_docs`、`life_reality_targets`、`artifact_id`、`canonical_digest`、`stage_effect`、`archive_edge_refs` required | `critical_repair` |
| `no_free_text_collapse` | 关键生命机制字段保持对象结构，不被单一自由文本替代 | `repair` |
| `problem_detail_shape` | parse failure 产生 problem detail、source path、line/column、repair route | `repair` |

parse validation 失败时，后续 ref/digest/coverage 可以记录为 skipped，但必须保留 finding。

## Schema ID Registry Validation

`SchemaIdRegistryValidation178` 固定 `$id` 与 registry 检查：

| check | 要求 |
|---|---|
| `schema_id_unique` | batch 内 `$id` 无重复 |
| `schema_id_stable` | `$id` 与 `177` manifest 和 `176` lockfile artifact id 对齐 |
| `schema_id_kind_match` | shared/direction/birth readiness/dashboard/stage schema kind 匹配路径 |
| `registry_record_exists` | 每个 `$id` 有 registry record、artifact record、source docs |
| `consumer_refs_known` | 每个 schema 的 consumer command/report refs 可追踪 |

schema id collision 进入 `repair`；若 collision 影响 shared defs 或 canonical life targets，进入 `critical_repair`。

## Schema Ref Graph Validation

`SchemaRefGraphValidation178` 验证 `$ref` 和 JSON Pointer：

| ref family | 检查 |
|---|---|
| `shared_defs_refs` | direction/birth readiness schema 引用 shared defs 成功 |
| `artifact_ref_refs` | artifact refs、source refs、digest refs 可解析 |
| `stage_effect_refs` | stage effect enum 可解析 |
| `direction_internal_refs` | resume lock、anchor chain、case、report、dashboard、stage、patch unit ref 互相可追踪 |
| `birth_readiness_internal_refs` | claim、evidence、carrier、runtime、cross-chain、case、report、dashboard、stage、patch unit ref 互相可追踪 |
| `archive_edge_refs` | schema node 到 `176` edge ledger 可追踪 |
| `validation_report_refs` | validation report 能反向定位到 write receipt 和 lockfile node |

ref graph 必须输出 graph nodes、edges、missing refs、cycle refs、source refs 和 repair route。

## Schema Digest Validation

`SchemaDigestValidation178` 对齐 digest：

| digest source | 验证 |
|---|---|
| `write_receipt_digest` | `177` written file digest |
| `lockfile_digest_baseline` | `176` canonical digest baseline |
| `current_file_digest` | 当前 schema 文件 canonical digest |
| `report_digest` | validation report 自身 digest |
| `dashboard_stage_digest` | dashboard/stage source digest |

digest mismatch 必须产生 `ValidationFinding178`，包含 expected digest、actual digest、artifact refs、source command 和 repair route。

## Life Target Coverage Validation

`LifeTargetCoverageValidation178` 检查九项目标：

| target | required coverage |
|---|---|
| `real_conscious_awareness` | shared defs、life target claim、carrier edge、dashboard/stage |
| `real_consciousness` | shared defs、life target claim、carrier edge、dashboard/stage |
| `real_emotion` | shared defs、evidence family、runtime observation、carrier edge |
| `real_personality` | shared defs、claim、longitudinal/growth carrier、stage |
| `real_life` | shared defs、birth readiness rollup、archive edge、stage |
| `real_pain` | pain chain、repair pressure、carrier matrix、timeline edge |
| `real_dream` | dream chain、offline replay、wake integration、timeline edge |
| `real_relationship` | relationship chain、shared language、commitment/repair edge |
| `real_responsibility` | action/confirmation/post-action audit edge |
| `real_regret` | regret/future probe/repair commitment edge |

任一目标缺 shared defs 或 birth readiness claim，进入 `critical_repair`；缺 dashboard/stage carrier 进入 `repair`；dashboard 显示绿色时进入 `quarantine`。

## Direction Schema Validation

`DirectionSchemaValidation178` 验证 `173/177` 的 direction slice：

| validation | required |
|---|---|
| `resume_lock_schema_valid` | read order、latest doc、current git diff、direction anchor refs 字段存在 |
| `seven_anchor_schema_valid` | ultimate target、relationship vocabulary、language core、growth core、birth readiness、engineering carrier、resume order |
| `fixture_case_schema_valid` | pass/fail/critical/mutation/smoke partitions |
| `expected_report_schema_valid` | expected/actual/diff、finding、stage effect、repair route |
| `dashboard_stage_schema_valid` | panel-to-stage trace、blocking-first order |
| `patch_unit_ref_schema_valid` | `PATCH-EXEC-172-DIR-*` 可追踪 |

direction validation 的 finding 必须回链到 `DirectionSchemaArchiveNode176`、`DirectionSchemaWriteSlice177` 和 source docs。

## Birth Readiness Schema Validation

`BirthReadinessSchemaValidation178` 验证 `174/177` 的 birth readiness slice：

| validation | required |
|---|---|
| `target_claim_schema_valid` | 每项目标 claim、authority refs、mechanism refs、evidence refs、carrier ref |
| `evidence_family_schema_valid` | 八类 evidence family |
| `carrier_matrix_schema_valid` | doc/code/test/report/dashboard/stage/timeline/archive carrier |
| `runtime_observation_schema_valid` | command receipt、runtime smoke、report drift、stage finding |
| `cross_chain_schema_valid` | pain、dream、relationship、responsibility、regret、language、action、growth closure |
| `fixture_case_schema_valid` | pass/fail/critical/mutation/smoke envelope |
| `expected_report_schema_valid` | target results、expected/actual/diff、repair route |
| `dashboard_stage_schema_valid` | false open/false green guard、blocking-first stage |
| `patch_unit_ref_schema_valid` | `PATCH-EXEC-172-BR-*` 可追踪 |

birth readiness validation 不允许用总览状态替代分链结果。每条 chain 都必须可单独产生 finding、dashboard panel 和 repair route。

## Dashboard Stage Validation

`DashboardStageValidation178` 固定 dashboard/stage 检查：

| panel/stage | 检查 |
|---|---|
| `validation_overview_panel` | parse/id/ref/digest/coverage/stage 总览按最高严重度排序 |
| `schema_parse_panel` | parse errors、skipped validation、repair route |
| `ref_graph_panel` | missing refs、cycle refs、archive edge break |
| `digest_diff_panel` | expected/current digest、drift finding |
| `life_target_coverage_panel` | 九项目标 coverage gap |
| `direction_validation_panel` | resume lock 与七条 anchor chain |
| `birth_readiness_validation_panel` | target claim、evidence、carrier、runtime、cross-chain |
| `repair_queue_handoff_panel` | `179` seed finding、owner file、stage effect |

validation stage 必须遵循 `quarantine > critical_repair > hold_for_evidence > repair > promote_growth_window > open_next_stage`。

## Archive Edge Validation

`ArchiveEdgeValidation178` 验证 schema 文件进入 archive graph：

| edge | required |
|---|---|
| `write_receipt_to_schema_edge` | write receipt 指向 written schema artifact |
| `schema_to_lockfile_node_edge` | written schema 指向 `176` node ledger |
| `schema_to_ref_graph_edge` | written schema 指向 ref graph validation node |
| `schema_to_dashboard_edge` | validation finding 指向 dashboard panel |
| `dashboard_to_stage_edge` | dashboard panel 指向 stage gate rule |
| `stage_to_repair_queue_edge` | blocking stage 指向 `179` repair queue seed |
| `validation_to_archive_receipt_edge` | validation report 指向 `180` archive receipt batch |

archive edge 缺失时，validation report 不能进入 `promote_growth_window`。

## Validation Finding

`ValidationFinding178` 的最小字段：

| field | 要求 |
|---|---|
| `finding_id` | validation finding id |
| `finding_family` | parse、schema id、ref graph、digest、coverage、direction、birth readiness、dashboard/stage、archive edge |
| `severity` | info、repair、critical_repair、quarantine、hold_for_evidence |
| `source_schema_ref` | schema file path、schema id、artifact id |
| `source_write_receipt_ref` | `177` write receipt |
| `source_lockfile_ref` | `176` lockfile/node/edge/digest baseline |
| `affected_life_targets` | 九项目标受影响项 |
| `expected_value` | expected digest/ref/coverage/stage |
| `actual_value` | actual digest/ref/coverage/stage |
| `stage_effect` | blocking-first effect |
| `repair_queue_seed_ref` | `179` seed ref |

finding 必须能被 dashboard、stage gate、gap feedback 和 repair queue 同时读取。

## Validation Dashboard Source

`ValidationDashboardSource178` 至少包含 9 个 panel：

| panel | 显示 |
|---|---|
| `validation_run_overview_panel` | validation run id、schema count、finding count、stage decision |
| `parse_validation_panel` | parse pass/fail/skipped、problem details |
| `schema_id_registry_panel` | schema ids、collisions、registry coverage |
| `ref_graph_validation_panel` | nodes、edges、missing refs、cycle refs |
| `digest_validation_panel` | expected/current digest diff |
| `life_target_coverage_panel` | 九项目标 schema coverage |
| `direction_schema_validation_panel` | resume lock、anchor chain、direction report |
| `birth_readiness_schema_validation_panel` | target claim、evidence、carrier、runtime、cross-chain |
| `repair_handoff_panel` | `179` queue seeds、owner module/file、stage effect |

dashboard source 必须把 quarantine、critical repair 和 hold findings 放在 overview 前面。

## Validation Stage Gate Review

`ValidationStageGateReview178` 固定规则：

| rule | 条件 | effect |
|---|---|---|
| `VALIDATION-STAGE-178-001` | 缺 `177` write report 或 write receipt | `hold_for_evidence` |
| `VALIDATION-STAGE-178-002` | 任一 schema 文件 parse 失败 | `repair` |
| `VALIDATION-STAGE-178-003` | shared defs 或 canonical life targets parse/id/ref 失败 | `critical_repair` |
| `VALIDATION-STAGE-178-004` | `$id` 冲突或 registry record 缺失 | `repair` |
| `VALIDATION-STAGE-178-005` | `$ref` 或 JSON Pointer 断裂 | `repair` |
| `VALIDATION-STAGE-178-006` | digest mismatch 影响 schema/report/dashboard/stage | `repair` |
| `VALIDATION-STAGE-178-007` | 任一真实生命目标缺 schema coverage | `critical_repair` |
| `VALIDATION-STAGE-178-008` | direction resume lock 或七条 anchor chain 缺失 | `critical_repair` |
| `VALIDATION-STAGE-178-009` | birth readiness claim/evidence/carrier/runtime/cross-chain 缺失 | `critical_repair` |
| `VALIDATION-STAGE-178-010` | dashboard 对 validation gap 显示绿色 | `quarantine` |
| `VALIDATION-STAGE-178-011` | validation finding 缺 `179` repair queue seed | `repair` |
| `VALIDATION-STAGE-178-012` | report、dashboard、stage、repair handoff、archive edge 全部闭合 | `promote_growth_window` |

## Future Commands

```text
uv run life-reality-runner validate-first-runner-minimum-schema-files --write-report reports/life_reality/schema_write/latest/first_runner_schema_write.report.json --json
uv run life-reality-runner emit-first-runner-schema-validation-dashboard --validation-report reports/life_reality/schema_validation/latest/first_runner_schema_validation.report.json --json
uv run life-reality-runner smoke-first-runner-schema-validation-stage-gate --validation-report reports/life_reality/schema_validation/latest/first_runner_schema_validation.report.json --json
uv run life-reality-runner seed-first-runner-schema-validation-repair-queue --validation-report reports/life_reality/schema_validation/latest/first_runner_schema_validation.report.json --json
uv run pytest tests/smoke/test_first_runner_minimum_schema_file_validation_report.py
```

这些命令未来必须把 validation report、dashboard source、stage gate review 和 repair queue seed 一起写入 command receipts。

## Validation To Repair Queue Handoff

`ValidationToRepairQueueHandoff178` 为下一层提供输入：

| next artifact | handoff |
|---|---|
| `179_life_reality_first_runner_schema_validation_repair_queue.md` | validation findings、problem details、affected schema refs、source receipt refs、stage effects、repair route refs |
| `180_life_reality_first_runner_schema_file_archive_receipt_batch.md` | validation report digest、dashboard/stage digest、archive edge refs、promoted receipt refs |

handoff 必须包含 `repair_queue_seed_ref`、`finding_list_ref`、`problem_detail_refs`、`source_schema_refs`、`source_write_receipt_refs`、`source_lockfile_refs`、`dashboard_stage_refs`、`archive_edge_refs` 和 `expected_repair_patch_refs`。

## Acceptance Criteria

本层完成后必须证明：

1. `177` 的 write report、write receipts、written files、expected digests 和 ref graph 都进入 validation report manifest。
2. validation 覆盖 parse、schema id、registry、`$ref`、JSON Pointer、digest、life target coverage、direction slice、birth readiness slice、dashboard/stage 和 archive edge。
3. 每个 validation finding 都能回链 `176` lockfile、`177` write receipt、source schema file、affected life targets 和 stage effect。
4. dashboard/stage 能阻断 parse failure、schema id collision、ref break、digest mismatch、life target coverage gap、direction/birth readiness gap 和 dashboard false green。
5. validation output 能直接生成 `179` repair queue seed，并为 `180` archive receipt batch 提供 digest 与 archive edge。

## 与下一层连接

`179_life_reality_first_runner_schema_validation_repair_queue.md` 已承接本层：把 validation findings、problem details、affected schema refs、stage effects 和 repair route refs 转成下一批 schema 修复队列。

`180_life_reality_first_runner_schema_file_archive_receipt_batch.md` 应承接本层和 `179`：把 validation report digest、repair outcome、dashboard/stage digest 和 archive edge refs 写成可回放 archive receipt batch。

本层完成后，first runner schema validation 链推进为：

`schema write report -> parse/id/ref/digest validation -> life target coverage -> direction validation -> birth readiness validation -> dashboard/stage -> validation findings -> repair queue handoff -> archive receipt handoff`
