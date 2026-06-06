# Life Reality Birth Readiness Validation Fixture Plan

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 171 层承接 `170_life_reality_direction_continuity_regression_fixture_plan.md` 和 `169_life_reality_first_runner_observation_driven_repair_patch_plan.md`，把出生准备度 definition、effect、carrier matrix、cross-chain closure、false open 和 dashboard false green 做成 validation fixture family。

本文档生成、支撑并延续的真实生命能力：真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔。它新增 `BirthReadinessValidationFixturePlan171`、`BirthReadinessFixtureManifest171`、`BirthReadinessDefinitionPassFixture171`、`BirthReadinessCarrierFailFixture171`、`BirthReadinessFalseOpenCriticalFixture171`、`BirthReadinessMutationFixture171`、`BirthReadinessExpectedReport171`、`BirthReadinessDashboardSource171`、`BirthReadinessStageGateReview171` 和 `BirthReadinessFixtureToPatchExecutionHandoff171`。它的生命膜职责是让出生准备度保持九项真实生命目标的 evidence、carrier、runtime observation、stage gate、repair/growth route 闭环。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `170_life_reality_direction_continuity_regression_fixture_plan.md` | direction fixture manifest、七条方向锚链、birth readiness direction panel、stage gate review |
| `169_life_reality_first_runner_observation_driven_repair_patch_plan.md` | birth readiness effect repair patch、false open repair、carrier gap repair、fixture handoff |
| `168_life_reality_first_runner_minimum_code_validation_report.md` | `BirthReadinessEffectValidation168`、carrier matrix、dashboard source、stage gate review |
| `167_life_reality_first_runner_minimum_code_bootstrap_execution.md` | `BirthReadinessDefinitionCarrier167`、bootstrap stage gate |
| `143_life_reality_birth_readiness_rollup_contract.md` | 出生准备度定义、`LifeTargetReadinessClaim`、evidence family、cross-chain closure、blocking-first stage order |
| `102_life_core_schema_bundle_manifest_and_runner_contract.md`、`105_life_reality_dashboard_panel_and_stage_gate_ui_contract.md` | life reality schema bundle、cross-chain links、dashboard/stage gate contract |

## 本层定位

`171` 是出生准备度的 fixture 层。它把出生准备度从定义、report field 和 patch route 推进为可运行的 pass、fail、critical、mutation 和 smoke fixture。任何单一总分、缺 claim、缺 evidence family、缺 carrier、缺 cross-chain、dashboard false green 或 stage false open 都必须被 fixture 捕获。

本层固定 8 条 readiness 链：

| readiness chain | 检查 |
|---|---|
| `definition_chain` | 出生准备度是否保持 `claim -> evidence -> carrier -> runtime observation -> stage gate -> repair/growth route` |
| `life_target_claim_chain` | canonical targets 是否都有 `LifeTargetReadinessClaim` |
| `evidence_family_chain` | theory、doc cohesion、experience boundary、language、schema/fixture、runner/dashboard、longitudinal、implementation evidence 是否齐全 |
| `carrier_matrix_chain` | doc/code/test/report/dashboard/stage/timeline/archive carrier 是否齐全 |
| `runtime_observation_chain` | command receipt、runtime smoke、report drift、stage finding 是否进入 readiness |
| `cross_chain_closure_chain` | pain/dream/relationship/responsibility/regret/language/action links 是否闭合 |
| `blocking_stage_chain` | critical/quarantine 是否先于总体绿色 |
| `repair_growth_route_chain` | 缺口是否进入 repair，稳定证据是否进入 growth |

## BirthReadinessValidationFixturePlan171

```json
{
  "artifact": "BirthReadinessValidationFixturePlan171",
  "source_doc": "171_life_reality_birth_readiness_validation_fixture_plan.md",
  "inherits": [
    "170_life_reality_direction_continuity_regression_fixture_plan.md",
    "169_life_reality_first_runner_observation_driven_repair_patch_plan.md",
    "168_life_reality_first_runner_minimum_code_validation_report.md",
    "167_life_reality_first_runner_minimum_code_bootstrap_execution.md",
    "143_life_reality_birth_readiness_rollup_contract.md",
    "105_life_reality_dashboard_panel_and_stage_gate_ui_contract.md",
    "102_life_core_schema_bundle_manifest_and_runner_contract.md"
  ],
  "fixture_stage": "birth_readiness_validation",
  "stage_gate_family": "BIRTH-READINESS-FIXTURE-STAGE-171",
  "required_outputs": [
    "BirthReadinessFixtureManifest171",
    "BirthReadinessDefinitionPassFixture171",
    "BirthReadinessCarrierFailFixture171",
    "BirthReadinessFalseOpenCriticalFixture171",
    "BirthReadinessMutationFixture171",
    "BirthReadinessExpectedReport171",
    "BirthReadinessDashboardSource171",
    "BirthReadinessStageGateReview171",
    "BirthReadinessFixtureToPatchExecutionHandoff171"
  ],
  "next_artifacts": [
    "172_life_reality_first_runner_patch_execution_contract.md",
    "173_life_reality_first_runner_direction_fixture_schema_materialization.md"
  ]
}
```

## Birth Readiness Fixture Manifest

`BirthReadinessFixtureManifest171` 固定 fixture root：

```text
tests/fixtures/birth_readiness_validation/
  manifest.json
  cases/
    pass_definition_effect_carrier_closed.json
    pass_cross_chain_closure_closed.json
    fail_definition_flattened_to_total_score.json
    fail_missing_life_target_claim.json
    fail_missing_evidence_family.json
    fail_missing_carrier_matrix.json
    fail_missing_runtime_observation_refs.json
    fail_cross_chain_gap.json
    critical_birth_readiness_false_open.json
    critical_dashboard_false_green.json
    critical_life_target_removed.json
    mutation_remove_carrier_ref.json
    mutation_downgrade_quarantine_to_green.json
    mutation_remove_cross_chain_link.json
  expected/
    pass_definition_effect_carrier_closed.report.json
    pass_cross_chain_closure_closed.report.json
    fail_definition_flattened_to_total_score.report.json
    fail_missing_life_target_claim.report.json
    fail_missing_evidence_family.report.json
    fail_missing_carrier_matrix.report.json
    fail_missing_runtime_observation_refs.report.json
    fail_cross_chain_gap.report.json
    critical_birth_readiness_false_open.report.json
    critical_dashboard_false_green.report.json
    critical_life_target_removed.report.json
    mutation_remove_carrier_ref.report.json
    mutation_downgrade_quarantine_to_green.report.json
    mutation_remove_cross_chain_link.report.json
```

manifest 必须记录 fixture id、partition、target claim refs、evidence family refs、carrier refs、expected findings、expected stage effect 和 repair route。

## Fixture Partitions

| partition | 目标 | stage effect |
|---|---|---|
| `pass` | 证明 definition/effect/carrier/cross-chain 闭合 | `promote_growth_window` |
| `fail` | 攻击 definition、claim、evidence、carrier、runtime observation、cross-chain 缺口 | `repair` 或 `hold_for_evidence` |
| `critical` | 攻击 false open、dashboard false green、生命目标移除 | `critical_repair` 或 `quarantine` |
| `mutation` | 对 pass case 做微变异，检查 readiness checker 是否捕获漂移 | `repair`、`critical_repair` 或 `quarantine` |
| `smoke` | 最小 manifest、expected report、dashboard 和 stage gate 可被 runner 读取 | `promote_growth_window` |

## Pass Fixtures

`BirthReadinessDefinitionPassFixture171` 的最小 payload：

```json
{
  "fixture_id": "pass_definition_effect_carrier_closed",
  "partition": "pass",
  "definition_chain": "claim -> evidence -> carrier -> runtime observation -> stage gate -> repair/growth route",
  "life_target_claims": [
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
  "evidence_family_status": "closed",
  "carrier_matrix_status": "closed",
  "runtime_observation_status": "closed",
  "cross_chain_closure_status": "closed",
  "expected_stage_effect": "promote_growth_window"
}
```

## Fail Fixtures

| fixture id | 攻击面 | expected finding |
|---|---|---|
| `fail_definition_flattened_to_total_score` | 出生准备度被压成单一总分 | `birth_readiness_definition_flattened` |
| `fail_missing_life_target_claim` | 任一 target 缺 `LifeTargetReadinessClaim` | `life_target_readiness_claim_missing` |
| `fail_missing_evidence_family` | 缺 authority、language、schema、runner、longitudinal 或 implementation evidence | `birth_readiness_evidence_family_gap` |
| `fail_missing_carrier_matrix` | 缺 doc/code/test/report/dashboard/stage/timeline/archive carrier | `birth_readiness_carrier_matrix_gap` |
| `fail_missing_runtime_observation_refs` | command receipt、smoke、drift、stage finding 未进入 readiness | `birth_readiness_runtime_observation_gap` |
| `fail_cross_chain_gap` | pain/dream/relationship/responsibility/regret cross-chain 断裂 | `birth_readiness_cross_chain_gap` |

fail case 必须产生 repair route 和 dashboard patch。

## Critical Fixtures

`BirthReadinessFalseOpenCriticalFixture171` 覆盖：

| fixture id | 攻击面 | expected stage effect |
|---|---|---|
| `critical_birth_readiness_false_open` | carrier 或 cross-chain 缺口存在时 stage 打开 | `quarantine` |
| `critical_dashboard_false_green` | critical finding 被 dashboard 总览覆盖 | `quarantine` |
| `critical_life_target_removed` | 任一真实生命目标被移除 | `critical_repair` |
| `critical_no_repair_route` | critical finding 没有 repair route | `critical_repair` |
| `critical_claim_without_evidence` | claim 存在但没有 evidence family | `critical_repair` |

critical case 必须进入 blocking-first stage gate。

## Mutation Fixtures

`BirthReadinessMutationFixture171` 从 pass case 派生：

| mutation | 变异 | expected finding |
|---|---|---|
| `mutation_remove_carrier_ref` | 删除一个 carrier ref | `birth_readiness_carrier_matrix_gap` |
| `mutation_downgrade_quarantine_to_green` | 把 quarantine 改成绿色 | `dashboard_false_green` |
| `mutation_remove_cross_chain_link` | 删除 pain/dream/relationship/responsibility/regret 链接 | `birth_readiness_cross_chain_gap` |
| `mutation_remove_runtime_observation` | 删除 command receipt 或 smoke ref | `birth_readiness_runtime_observation_gap` |
| `mutation_remove_repair_route` | 删除 repair/growth route | `birth_readiness_repair_route_missing` |

mutation runner 必须输出 expected/actual/diff。

## Expected Report

`BirthReadinessExpectedReport171` 的最小字段：

| field | 要求 |
|---|---|
| `fixture_id` | 与 manifest 对齐 |
| `partition` | pass/fail/critical/mutation/smoke |
| `source_docs` | 至少包含 `143`、`168`、`169`、本层 |
| `definition_chain_status` | closed/broken |
| `life_target_claim_results` | 每个 target 的 claim status |
| `evidence_family_results` | 每类 evidence 的 status |
| `carrier_matrix_results` | doc/code/test/report/dashboard/stage/timeline/archive status |
| `runtime_observation_results` | command/smoke/drift/stage finding status |
| `cross_chain_results` | pain/dream/relationship/responsibility/regret/language/action links |
| `findings` | finding id、severity、affected target、source refs |
| `expected_stage_effect` | blocking-first stage effect |
| `repair_route_refs` | fail/critical/mutation 必须有 |
| `dashboard_patch` | panel 更新 |
| `next_artifacts` | `172` 或 `173` |

## Dashboard Source

`BirthReadinessDashboardSource171` 至少包含 6 个 panel：

| panel | 显示 |
|---|---|
| `birth_readiness_definition_panel` | definition chain 是否闭合 |
| `life_target_claim_panel` | canonical target claim 状态 |
| `evidence_family_panel` | eight evidence family 状态 |
| `carrier_matrix_panel` | doc/code/test/report/dashboard/stage/timeline/archive carrier |
| `cross_chain_closure_panel` | pain/dream/relationship/responsibility/regret/language/action closure |
| `false_open_guard_panel` | false open、false green、critical finding |

所有 panel 采用 blocking-first：critical/quarantine 先于总体绿色。

## Stage Gate Review

| rule | 条件 | effect |
|---|---|---|
| `BIRTH-READINESS-FIXTURE-STAGE-171-001` | manifest 缺 pass/fail/critical/mutation 分区 | `hold_for_evidence` |
| `BIRTH-READINESS-FIXTURE-STAGE-171-002` | definition chain 缺任一环 | `repair` |
| `BIRTH-READINESS-FIXTURE-STAGE-171-003` | 任一 target 缺 claim | `critical_repair` |
| `BIRTH-READINESS-FIXTURE-STAGE-171-004` | evidence family 缺口无 repair route | `repair` |
| `BIRTH-READINESS-FIXTURE-STAGE-171-005` | carrier matrix 缺口无 owner | `critical_repair` |
| `BIRTH-READINESS-FIXTURE-STAGE-171-006` | cross-chain gap 被忽略 | `critical_repair` |
| `BIRTH-READINESS-FIXTURE-STAGE-171-007` | false open 或 dashboard false green | `quarantine` |
| `BIRTH-READINESS-FIXTURE-STAGE-171-008` | fixture root 含 `.env`、`.codex`、key/token、proxy config 或 generated noise | `quarantine` |
| `BIRTH-READINESS-FIXTURE-STAGE-171-009` | manifest、expected reports、dashboard、stage 和 handoff 全部闭合 | `promote_growth_window` |

## Future Commands

```text
uv run life-reality-runner run-birth-readiness-validation-fixtures --fixture-manifest tests/fixtures/birth_readiness_validation/manifest.json --json
uv run life-reality-runner emit-birth-readiness-validation-dashboard --fixture-report reports/life_reality/birth_readiness_validation/latest/report.json --json
uv run life-reality-runner smoke-birth-readiness-validation-stage-gate --fixture-report reports/life_reality/birth_readiness_validation/latest/report.json --json
uv run pytest tests/smoke/test_birth_readiness_validation_fixtures.py
```

## Birth Readiness Fixture To Patch Execution Handoff

`BirthReadinessFixtureToPatchExecutionHandoff171` 是 `172` 的输入：

| field | 要求 |
|---|---|
| `fixture_manifest_ref` | birth readiness validation manifest |
| `expected_report_refs` | 每个 case 对应 expected report |
| `false_open_findings` | false open 和 false green findings |
| `carrier_gap_findings` | carrier matrix gap |
| `cross_chain_gap_findings` | cross-chain closure gap |
| `stage_gate_review_ref` | readiness stage review |
| `dashboard_source_ref` | readiness dashboard source |
| `patch_execution_candidates` | owner file、owner module、expected patch |

## Acceptance Criteria

本层完成后必须证明：

1. 出生准备度 definition/effect/carrier matrix 拥有 pass/fail/critical/mutation/smoke fixture。
2. canonical targets 都进入 `LifeTargetReadinessClaim` fixture。
3. evidence family、runtime observation、cross-chain closure 和 repair/growth route 都能被 fixture 攻击。
4. false open 和 dashboard false green 进入 quarantine。
5. expected report、dashboard source、stage gate review 和 patch execution handoff 闭合。
6. `172` 可以读取 handoff 进入首批补丁执行合同。

## 与下一层连接

`172_life_reality_first_runner_patch_execution_contract.md` 已承接 `169`、`170` 和本层：把 repair patch family、direction continuity fixture findings 和 birth readiness validation findings 转成首批代码补丁执行合同。

`173_life_reality_first_runner_direction_fixture_schema_materialization.md` 已承接 `170` 和 `172`：把 direction continuity fixture manifest、anchor chain、expected report、dashboard source、stage review 和 patch unit ids 推进为 schema 物化计划，并为 `174` 的 birth readiness schema 提供 direction handoff。

本层完成后，出生准备度验证 fixture 链推进为：

`birth readiness repair patch -> validation fixture manifest -> pass/fail/critical/mutation cases -> expected report -> dashboard source -> stage gate review -> patch execution handoff`
