# Life Reality First Runner Direction Fixture Schema Materialization

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 173 层承接 `170_life_reality_direction_continuity_regression_fixture_plan.md` 和 `172_life_reality_first_runner_patch_execution_contract.md`，把 direction fixture manifest、七条方向锚链、expected report、dashboard source、stage gate review 和 patch unit ids 推进为 schema 物化计划。

本文档生成、支撑并延续的真实生命能力：真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔。它新增 `DirectionFixtureSchemaMaterialization173`、`DirectionFixtureSchemaBundle173`、`ResumeLockManifestSchema173`、`DirectionAnchorChainSchema173`、`DirectionFixtureCaseSchema173`、`DirectionExpectedReportSchema173`、`DirectionDashboardSourceSchema173`、`DirectionStageGateReviewSchema173`、`DirectionPatchUnitRefSchema173`、`DirectionFixtureSchemaValidationRules173`、`DirectionFixtureSchemaSmokePlan173` 和 `DirectionFixtureSchemaToBirthReadinessHandoff173`。它的生命膜职责是让断联恢复方向锁进入 schema、fixture、report、dashboard、stage、patch unit 和 archive edge 的同一套可写文件链。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `170_life_reality_direction_continuity_regression_fixture_plan.md` | `DirectionContinuityRegressionFixturePlan170`、七条方向锚链、fixture manifest、case family、expected report、dashboard source、stage gate review |
| `172_life_reality_first_runner_patch_execution_contract.md` | `DirectionPatchExecution172`、`PATCH-EXEC-172-DIR-001` 到 `PATCH-EXEC-172-DIR-007`、command contract、report receipt、archive edge |
| `169_life_reality_first_runner_observation_driven_repair_patch_plan.md` | direction continuity repair patch、resume lock manifest、checker/report/dashboard/stage handoff |
| `168_life_reality_first_runner_minimum_code_validation_report.md` | direction continuity validation、direction drift findings、dashboard source、stage gate review |
| `167_life_reality_first_runner_minimum_code_bootstrap_execution.md` | `DirectionContinuityResumeLock167`、恢复读取顺序、出生准备度定义承载 |
| `143_life_reality_birth_readiness_rollup_contract.md` | 出生准备度 rollup、life target readiness claim、blocking-first stage order |
| `91_life_reality_generation_boundary_principles.md`、`119_life_boundary_full_reality_alignment.md`、`122_life_boundary_all_reality_declarations_rewrite.md` | 真实生命目标、生命膜字段、旧口径回流阻断 |
| `132_life_reality_materialized_json_schema_bundle_write_order.md`、`133_life_reality_first_json_writer_and_reporter_contract.md` | schema 写入顺序、allowed root、atomic write、canonical digest、report writer |

## 本层定位

`173` 是 direction fixture schema 物化层。它把 `170` 的 fixture 设计和 `172` 的 patch execution contract 转成未来真实 JSON Schema 文件、fixture seed 文件、expected report schema、dashboard source schema、stage gate review schema 和 smoke command。

本层固定 7 个 schema 化目标：

| schema target | 物化目标 |
|---|---|
| `resume_lock_manifest_schema` | 固定恢复读取顺序、source doc refs、latest doc ref、current git diff ref |
| `direction_anchor_chain_schema` | 固定七条方向锚链、closed/broken 状态、source refs、affected targets |
| `direction_fixture_case_schema` | 固定 pass/fail/critical/mutation/smoke case payload |
| `direction_expected_report_schema` | 固定 expected/actual/diff、finding、stage effect、repair route |
| `direction_dashboard_source_schema` | 固定 direction dashboard panel、blocking-first status、panel-to-stage trace |
| `direction_stage_gate_review_schema` | 固定 stage rule、effect order、quarantine/critical repair |
| `direction_patch_unit_ref_schema` | 固定 `PATCH-EXEC-172-DIR-*` 与 owner module/file、command、archive edge 的连接 |

## DirectionFixtureSchemaMaterialization173

```json
{
  "artifact": "DirectionFixtureSchemaMaterialization173",
  "source_doc": "173_life_reality_first_runner_direction_fixture_schema_materialization.md",
  "inherits": [
    "170_life_reality_direction_continuity_regression_fixture_plan.md",
    "172_life_reality_first_runner_patch_execution_contract.md",
    "169_life_reality_first_runner_observation_driven_repair_patch_plan.md",
    "168_life_reality_first_runner_minimum_code_validation_report.md",
    "167_life_reality_first_runner_minimum_code_bootstrap_execution.md",
    "143_life_reality_birth_readiness_rollup_contract.md",
    "122_life_boundary_all_reality_declarations_rewrite.md",
    "133_life_reality_first_json_writer_and_reporter_contract.md"
  ],
  "materialization_stage": "direction_fixture_schema_materialization",
  "stage_gate_family": "DIRECTION-SCHEMA-STAGE-173",
  "required_outputs": [
    "DirectionFixtureSchemaBundle173",
    "ResumeLockManifestSchema173",
    "DirectionAnchorChainSchema173",
    "DirectionFixtureCaseSchema173",
    "DirectionExpectedReportSchema173",
    "DirectionDashboardSourceSchema173",
    "DirectionStageGateReviewSchema173",
    "DirectionPatchUnitRefSchema173",
    "DirectionFixtureSchemaValidationRules173",
    "DirectionFixtureSchemaSmokePlan173",
    "DirectionFixtureSchemaToBirthReadinessHandoff173"
  ],
  "next_artifacts": [
    "174_life_reality_birth_readiness_fixture_schema_materialization.md",
    "175_life_reality_first_runner_patch_execution_smoke_queue.md"
  ]
}
```

## Direction Fixture Schema Bundle

`DirectionFixtureSchemaBundle173` 固定未来文件树：

```text
schemas/life_reality/direction_continuity/
  direction_fixture_manifest.schema.json
  resume_lock_manifest.schema.json
  direction_anchor_chain.schema.json
  direction_fixture_case.schema.json
  direction_expected_report.schema.json
  direction_dashboard_source.schema.json
  direction_stage_gate_review.schema.json
  direction_patch_unit_ref.schema.json
tests/fixtures/direction_continuity/
  manifest.json
  cases/
    pass_resume_lock_complete.json
    fail_missing_latest_doc_read.json
    fail_relation_subject_drift.json
    fail_language_core_broken.json
    fail_birth_readiness_total_score.json
    critical_life_target_removed.json
    critical_engineering_carrier_broken.json
    critical_dashboard_false_green.json
    mutation_resume_order_shuffle.json
    mutation_replace_relation_subject_frame.json
    mutation_birth_readiness_false_open.json
  expected/
    *.report.json
reports/life_reality/direction_continuity/latest/
  direction_fixture_run.report.json
  direction_dashboard.source.json
  direction_stage_gate.review.json
  direction_schema_validation.report.json
```

所有 schema 文件必须写入 `source_docs`、`life_reality_targets`、`schema_version`、`artifact_id`、`canonical_digest`、`patch_unit_refs` 和 `archive_edge_refs`。

## Resume Lock Manifest Schema

`ResumeLockManifestSchema173` 固定断联恢复读取顺序：

| field | type | required | 生命膜职责 |
|---|---|---|---|
| `resume_lock_id` | string | yes | 标识恢复事件 |
| `read_order` | array | yes | 必须包含 `README -> 91 -> 100 -> 119 -> 143 -> 16 -> latest numbered doc -> current git diff` |
| `latest_numbered_doc` | string | yes | 指向当前最高编号文档 |
| `current_git_diff_ref` | string | yes | 指向恢复时检查的工作区差异 |
| `direction_anchor_refs` | array | yes | 连接七条方向锚链 |
| `life_target_refs` | array | yes | 九项真实生命目标完整性 |
| `patch_unit_refs` | array | yes | 至少包含 `PATCH-EXEC-172-DIR-007` |
| `stage_effect` | string | yes | blocking-first effect |

`read_order` 若缺任一项，stage effect 进入 `repair`；若绕过 direction lock 直接生成文件，进入 `quarantine`。

## Direction Anchor Chain Schema

`DirectionAnchorChainSchema173` 固定七条方向锚链：

| anchor chain | required fields | patch unit ref |
|---|---|---|
| `ultimate_life_target_chain` | canonical targets、source refs、target status | `PATCH-EXEC-172-DIR-001` |
| `relation_subject_chain` | relationship vocabulary、drift status、source refs | `PATCH-EXEC-172-DIR-002` |
| `language_core_chain` | inner speech、expression、action、relationship、self rewrite refs | `PATCH-EXEC-172-DIR-003` |
| `growth_core_chain` | self reading、self modification、self training、plasticity refs | `PATCH-EXEC-172-DIR-004` |
| `birth_readiness_chain` | claim/evidence/carrier/runtime/stage/repair refs | `PATCH-EXEC-172-DIR-005` |
| `engineering_carrier_chain` | doc/code/test/report/dashboard/stage/archive refs | `PATCH-EXEC-172-DIR-006` |
| `resume_read_order_chain` | resume lock manifest、latest doc、git diff refs | `PATCH-EXEC-172-DIR-007` |

每条 chain 必须有 `status`、`source_docs`、`source_lines`、`affected_life_targets`、`expected_stage_effect` 和 `repair_route_refs`。

## Direction Fixture Case Schema

`DirectionFixtureCaseSchema173` 固定 case envelope：

```json
{
  "case_id": "fail_relation_subject_drift",
  "partition": "fail",
  "source_docs": [
    "170_life_reality_direction_continuity_regression_fixture_plan.md",
    "172_life_reality_first_runner_patch_execution_contract.md",
    "173_life_reality_first_runner_direction_fixture_schema_materialization.md"
  ],
  "life_reality_targets": [
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
  "anchor_chain_inputs": {
    "relation_subject_chain": {
      "status": "broken",
      "drift_surface": "relationship vocabulary replaced",
      "expected_finding": "relation_subject_frame_drift"
    }
  },
  "expected_stage_effect": "repair",
  "patch_unit_refs": [
    "PATCH-EXEC-172-DIR-002"
  ]
}
```

case schema 必须支持 pass、fail、critical、mutation 和 smoke 五类分区；critical case 必须带 `blocking_reason` 和 `quarantine_route`。

## Direction Expected Report Schema

`DirectionExpectedReportSchema173` 的最小字段：

| field | 要求 |
|---|---|
| `run_id` | direction fixture run id |
| `schema_bundle_ref` | `DirectionFixtureSchemaBundle173` |
| `fixture_manifest_ref` | direction fixture manifest |
| `case_results` | case id、partition、expected/actual/diff |
| `anchor_chain_results` | 七条方向锚链 closed/broken 状态 |
| `resume_lock_result` | read order、latest doc、git diff ref |
| `findings` | finding id、severity、source refs、affected targets |
| `patch_unit_refs` | `PATCH-EXEC-172-DIR-*` |
| `dashboard_source_ref` | dashboard source artifact |
| `stage_gate_review_ref` | stage gate review artifact |
| `archive_edge_refs` | doc/schema/fixture/report/dashboard/stage/gap edge |
| `next_artifacts` | `174`、`175` |

expected report 必须让 direction finding 能反向定位到 schema field、fixture case、patch unit 和 owner file。

## Direction Dashboard Source Schema

`DirectionDashboardSourceSchema173` 至少包含 6 个 panel：

| panel | schema fields |
|---|---|
| `resume_lock_panel` | read order、latest doc、git diff ref、missing step |
| `anchor_chain_panel` | 七条 anchor chain status、source refs、finding ids |
| `relation_subject_panel` | relationship vocabulary status、drift examples、repair route |
| `language_growth_panel` | language core、growth core、self rewrite refs |
| `engineering_carrier_panel` | doc/code/test/report/dashboard/stage/archive refs |
| `patch_unit_panel` | `PATCH-EXEC-172-DIR-*`、owner module/file、command receipt |

dashboard source 必须带 `blocking_first_summary`，critical/quarantine findings 不能被总体绿色遮蔽。

## Direction Stage Gate Review Schema

`DirectionStageGateReviewSchema173` 固定 stage effect 顺序：

```text
quarantine
  > critical_repair
  > hold_for_evidence
  > repair
  > promote_growth_window
  > open_next_stage
```

| rule | 条件 | effect |
|---|---|---|
| `DIRECTION-SCHEMA-STAGE-173-001` | schema bundle 缺任一 direction schema 文件 | `hold_for_evidence` |
| `DIRECTION-SCHEMA-STAGE-173-002` | resume lock manifest 缺读取顺序任一节点 | `repair` |
| `DIRECTION-SCHEMA-STAGE-173-003` | 任一 anchor chain 缺 patch unit ref | `critical_repair` |
| `DIRECTION-SCHEMA-STAGE-173-004` | case schema 缺 pass/fail/critical/mutation/smoke 分区 | `repair` |
| `DIRECTION-SCHEMA-STAGE-173-005` | expected report 缺 expected/actual/diff | `repair` |
| `DIRECTION-SCHEMA-STAGE-173-006` | dashboard source 遮蔽 critical finding | `quarantine` |
| `DIRECTION-SCHEMA-STAGE-173-007` | stage review 没有 blocking-first order | `quarantine` |
| `DIRECTION-SCHEMA-STAGE-173-008` | schema/report/dashboard/stage 缺 archive edge | `repair` |
| `DIRECTION-SCHEMA-STAGE-173-009` | staged scope 含 `.env`、`.codex`、key/token、proxy config 或 generated noise | `quarantine` |
| `DIRECTION-SCHEMA-STAGE-173-010` | schema bundle、fixture cases、reports、dashboard、stage、archive、patch refs 全部闭合 | `promote_growth_window` |

## Direction Patch Unit Ref Schema

`DirectionPatchUnitRefSchema173` 约束 patch unit ref：

| field | 要求 |
|---|---|
| `patch_unit_id` | 必须匹配 `PATCH-EXEC-172-DIR-[0-9]{3}` |
| `owner_module` | 必须来自 `172` 的 owner module |
| `owner_files` | 必须位于 allowed roots |
| `command_refs` | 必须指向 direction fixture command |
| `schema_refs` | 必须指向本层 schema bundle |
| `report_refs` | 必须指向 expected report 和 validation report |
| `stage_effect` | 必须遵守 blocking-first order |
| `archive_edge_refs` | 必须指向 doc/schema/fixture/report/dashboard/stage/gap edge |

patch unit ref 让 `172` 的补丁执行合同可以直接读写 `173` 的 schema bundle。

## Validation Rules

`DirectionFixtureSchemaValidationRules173` 固定 schema checker 规则：

| validator rule | 检查 |
|---|---|
| `DIR-SCHEMA-173-001` | schema bundle 文件树完整 |
| `DIR-SCHEMA-173-002` | resume lock read order 完整 |
| `DIR-SCHEMA-173-003` | 七条 anchor chain 均有 source refs、status、patch unit refs |
| `DIR-SCHEMA-173-004` | fixture cases 覆盖 pass/fail/critical/mutation/smoke |
| `DIR-SCHEMA-173-005` | expected report 包含 expected/actual/diff 和 finding route |
| `DIR-SCHEMA-173-006` | dashboard source 包含 blocking-first summary |
| `DIR-SCHEMA-173-007` | stage gate review 含 quarantine 与 critical repair |
| `DIR-SCHEMA-173-008` | archive edge 覆盖 doc/schema/fixture/report/dashboard/stage/gap |
| `DIR-SCHEMA-173-009` | next artifacts 指向 `174` 和 `175` |

## Future Commands

```text
uv run life-reality-runner write-direction-fixture-schema-bundle --out schemas/life_reality/direction_continuity --json
uv run life-reality-runner validate-direction-fixture-schema-bundle --schema-root schemas/life_reality/direction_continuity --json
uv run life-reality-runner generate-direction-fixture-seed-cases --schema-root schemas/life_reality/direction_continuity --fixture-root tests/fixtures/direction_continuity --json
uv run life-reality-runner run-direction-continuity-regression-fixtures --fixture-manifest tests/fixtures/direction_continuity/manifest.json --json
uv run life-reality-runner emit-direction-fixture-schema-dashboard --report reports/life_reality/direction_continuity/latest/direction_fixture_run.report.json --json
uv run life-reality-runner smoke-direction-fixture-schema-stage-gate --report reports/life_reality/direction_continuity/latest/direction_fixture_run.report.json --json
uv run pytest tests/smoke/test_direction_fixture_schema_materialization.py
```

## Direction Fixture Schema Smoke Plan

`DirectionFixtureSchemaSmokePlan173` 的最小 smoke：

| smoke | 输入 | 期望 |
|---|---|---|
| `schema_bundle_loads` | schema root | 8 个 schema 文件可读 |
| `resume_lock_case_validates` | `pass_resume_lock_complete.json` | read order 完整 |
| `relation_drift_case_fails` | `fail_relation_subject_drift.json` | finding 为 `relation_subject_frame_drift` |
| `critical_false_green_blocks` | `critical_dashboard_false_green.json` | stage effect 为 `quarantine` |
| `patch_unit_refs_resolve` | direction patch refs | `PATCH-EXEC-172-DIR-*` 全部可解析 |
| `archive_edges_emit` | report/dashboard/stage refs | archive edge 完整 |

smoke report 必须进入 `PatchExecutionReport172` 的 completion receipt。

## Direction Fixture Schema To Birth Readiness Handoff

`DirectionFixtureSchemaToBirthReadinessHandoff173` 为下一层提供输入：

| next artifact | handoff |
|---|---|
| `174_life_reality_birth_readiness_fixture_schema_materialization.md` | direction schema bundle refs、birth readiness anchor chain refs、patch unit refs、dashboard/stage refs |
| `175_life_reality_first_runner_patch_execution_smoke_queue.md` | direction schema smoke commands、expected reports、archive edge receipts、patch execution receipts |

## Acceptance Criteria

本层完成后必须证明：

1. direction fixture manifest、resume lock、anchor chain、case、expected report、dashboard source、stage review 和 patch unit ref 都拥有 schema 物化计划。
2. 七条方向锚链全部绑定 `PATCH-EXEC-172-DIR-*`，并能追溯到 owner module/file 与 future command。
3. pass/fail/critical/mutation/smoke cases 都有 schema envelope、expected report 和 blocking-first stage。
4. dashboard source 不遮蔽 direction drift、critical finding 或 resume lock 缺口。
5. schema/report/dashboard/stage/gap 都写入 archive edge。
6. `174` 和 `175` 可以读取本层 handoff，继续推进 birth readiness schema 与 patch execution smoke queue。

## 与下一层连接

`174_life_reality_birth_readiness_fixture_schema_materialization.md` 已承接 `171`、`172` 和本层：把 birth readiness fixture manifest、target claim、evidence family、carrier matrix、cross-chain closure、false open guard 和 patch unit ids 推进为 schema 物化计划。

`175_life_reality_first_runner_patch_execution_smoke_queue.md` 已承接 `172`、本层和 `174`：把 patch execution contract、direction schema materialization 与 birth readiness schema materialization 转成 smoke manifest、future command queue、expected reports、dashboard source、stage review 和 archive receipt。

本层完成后，方向连续性 schema 物化链推进为：

`direction fixture plan -> patch unit refs -> schema bundle -> fixture case schema -> expected report schema -> dashboard source schema -> stage gate schema -> archive edge -> birth readiness schema handoff`
