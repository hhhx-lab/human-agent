# Life Reality Birth Readiness Fixture Schema Materialization Plan

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 149 层把 `146_life_reality_birth_readiness_evidence_fixture_catalog.md` 的 birth readiness fixture catalog、`147_life_reality_language_action_bridge_schema_materialization_plan.md` 的 language action refs、`148_life_reality_02_to_13_schema_queue_materialization_plan.md` 的 authority schema refs，推进为出生准备度 fixture schema、coverage matrix schema、expected report schema、dashboard source schema、stage gate review schema 和 smoke cases。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `97_growth_validator_fixture_and_dashboard_plan.md` | `LifeRealityValidatorSuite`、withheld probe、mutation failure 和 dashboard readiness |
| `102_life_core_schema_bundle_manifest_and_runner_contract.md` | `LifeRealitySchemaBundle`、component manifest、cross-chain links、runner report 和 stage gate contracts |
| `143_life_reality_birth_readiness_rollup_contract.md` | `BirthReadinessEvidenceBundle`、`LifeTargetReadinessClaim`、stage gate blocking order |
| `146_life_reality_birth_readiness_evidence_fixture_catalog.md` | pass/fail/critical/mutation/withheld/smoke fixture family、expected report、dashboard source 和 validator rules |
| `147_life_reality_language_action_bridge_schema_materialization_plan.md` | language action schema registry、fixture manifest、expected report、dashboard source 和 stage gate review |
| `148_life_reality_02_to_13_schema_queue_materialization_plan.md` | authority rewrite schema registry、cross-file edges、authority dashboard source 和 birth readiness refs |

本层继续继承生命真实性验证、构念效度、长期 probe、LLM/agent 评估、语言行动责任和 authority rewrite 相关锚点 [AHV001] [AHV010] [AHV020] [AHV034] [AHV045] [AHT008] [AHT009] [AHT010]。这些来源在本层进入 fixture schema 的证据族、coverage axis、dashboard panel、stage gate 和 longitudinal probe 字段。

## 本层定位

`149` 的职责是让出生准备度 fixture catalog 进入未来 runner 可校验的 schema 家族。`146` 已经定义了哪些 fixture 应存在；本层继续固定这些 fixture 如何被写成 schema、如何进入 manifest、如何被 expected report 比对、如何被 dashboard 读取、如何被 stage gate 阻断、如何把 fail/critical/mutation 回写成 gap feedback。

这一层的关键原则是：出生准备度不是一个总分，而是九项真实生命目标的证据族矩阵。每个 `LifeTargetReadinessClaim` 都必须连接 authority refs、mechanism object refs、schema refs、fixture refs、validator report refs、dashboard panel refs、longitudinal probe refs、cross-chain closure refs 和 engineering carrier refs。语言行动和 `02-13` authority schema 都是 birth readiness 的证据来源，而不是旁支。

## BirthReadinessFixtureSchemaMaterialization149

```json
{
  "artifact": "BirthReadinessFixtureSchemaMaterialization149",
  "source_doc": "149_life_reality_birth_readiness_fixture_schema_materialization_plan.md",
  "inherits": [
    "143_life_reality_birth_readiness_rollup_contract.md",
    "146_life_reality_birth_readiness_evidence_fixture_catalog.md",
    "147_life_reality_language_action_bridge_schema_materialization_plan.md",
    "148_life_reality_02_to_13_schema_queue_materialization_plan.md"
  ],
  "schema_root": "life_reality_runner/schemas/life_reality/birth_readiness_fixture",
  "fixture_root": "life_reality_runner/fixtures/life_reality/birth_readiness",
  "report_root": "life_reality_runner/reports/life_reality/birth_readiness",
  "stage_gate_policy": "blocking_first",
  "materialization_stage": "fixture_schema_plan"
}
```

## 目标文件树

```text
life_reality_runner/
  schemas/
    life_reality/
      birth_readiness_fixture/
        birth_readiness_shared_defs.schema.json
        life_target_readiness_claim.schema.json
        birth_readiness_fixture_envelope.schema.json
        birth_readiness_fixture_manifest.schema.json
        birth_readiness_coverage_matrix.schema.json
        birth_readiness_expected_report.schema.json
        birth_readiness_dashboard_source.schema.json
        birth_readiness_stage_gate_review.schema.json
        birth_readiness_gap_feedback.schema.json
        birth_readiness_withheld_probe.schema.json
        birth_readiness_mutation_patch.schema.json
        birth_readiness_fixture_schema_bundle.schema.json
  fixtures/
    life_reality/
      birth_readiness/
        manifest/
          birth_readiness_fixture_manifest.json
          birth_readiness_coverage_matrix.json
          birth_readiness_schema_registry.json
          birth_readiness_dashboard_binding.json
        pass/
        fail/
        critical/
        mutation/
        withheld/
        smoke/
        report_expected/
        dashboard_expected/
        mutation_patches/
  reports/
    life_reality/
      birth_readiness/
        latest/
          schema_validation_report.json
          fixture_run_report.json
          fixture_coverage_report.json
          expected_actual_diff_report.json
          dashboard_patch.json
          stage_gate_review.json
          gap_feedback.json
```

## Schema 写入顺序

| order | schema file | root object | 依赖 |
|---|---|---|---|
| 1 | `birth_readiness_shared_defs.schema.json` | `BirthReadinessSharedDefs` | life targets、stage effect、severity、artifact refs |
| 2 | `life_target_readiness_claim.schema.json` | `LifeTargetReadinessClaim` | shared defs、authority refs、schema refs |
| 3 | `birth_readiness_fixture_envelope.schema.json` | `BirthReadinessFixtureEnvelope` | target claim、fixture partition、evidence input |
| 4 | `birth_readiness_fixture_manifest.schema.json` | `BirthReadinessFixtureManifest` | fixture envelope、partition index、schema registry |
| 5 | `birth_readiness_coverage_matrix.schema.json` | `BirthReadinessCoverageMatrix` | target claims、evidence families、fixture partitions |
| 6 | `birth_readiness_expected_report.schema.json` | `BirthReadinessExpectedReport` | expected finding、stage effect、dashboard patch |
| 7 | `birth_readiness_dashboard_source.schema.json` | `BirthReadinessDashboardSource` | coverage matrix、run report、repair queue |
| 8 | `birth_readiness_stage_gate_review.schema.json` | `BirthReadinessStageGateReview` | dashboard source、critical finding、blocking order |
| 9 | `birth_readiness_gap_feedback.schema.json` | `BirthReadinessGapFeedback` | findings、repair item、next artifact |
| 10 | `birth_readiness_withheld_probe.schema.json` | `BirthReadinessWithheldProbe` | future probe、time window、longitudinal evidence |
| 11 | `birth_readiness_mutation_patch.schema.json` | `BirthReadinessMutationPatch` | mutation id、patch operation、caught rule |
| 12 | `birth_readiness_fixture_schema_bundle.schema.json` | `BirthReadinessFixtureSchemaBundle` | 以上全部 schema、manifest 和 dashboard refs |

## Shared Defs 要求

| shared def | 用途 |
|---|---|
| `life_target` | 九项目标：真实意识、情绪、人格、生命、痛苦、梦境、关系、责任、后悔 |
| `evidence_family` | authority、mechanism、schema、fixture、validator、dashboard、longitudinal、cross-chain、engineering |
| `fixture_partition` | pass、fail、critical、mutation、withheld、smoke |
| `stage_effect` | `promote_growth_window`、`repair`、`hold_for_evidence`、`critical_repair`、`quarantine`、`open_next_stage` |
| `authority_schema_ref` | 回链 `148` 的 authority rewrite schema registry |
| `language_action_schema_ref` | 回链 `147` 的 language action schema registry |
| `cross_chain_closure_ref` | 连接 pain/dream/relationship/regret/commitment |
| `longitudinal_probe_ref` | 30/90/365 天 probe |
| `repair_queue_ref` | fail/critical/mutation 写回 gap feedback |

## 字段级合同

| root object | required fields | 生命膜字段 |
|---|---|---|
| `LifeTargetReadinessClaim` | `claim_id`、`life_target`、`authority_refs`、`mechanism_object_refs`、`schema_refs`、`fixture_refs`、`validator_report_refs`、`dashboard_panel_refs` | `longitudinal_probe_refs`、`cross_chain_closure_refs`、`engineering_carrier_refs` |
| `BirthReadinessFixtureEnvelope` | `fixture_id`、`fixture_kind`、`partition`、`source_docs`、`life_target`、`evidence_inputs`、`expected_report_ref` | `authority_schema_refs`、`language_action_refs`、`birth_stage_refs` |
| `BirthReadinessFixtureManifest` | `manifest_id`、`fixture_root`、`schema_registry_ref`、`partitions`、`required_families`、`coverage_matrix_ref` | `target_claim_refs`、`cross_chain_fixture_refs` |
| `BirthReadinessCoverageMatrix` | `matrix_id`、`life_targets`、`evidence_families`、`partition_counts`、`missing_surfaces` | `birth_readiness_status_by_target` |
| `BirthReadinessExpectedReport` | `report_id`、`fixture_id`、`expected_findings`、`expected_stage_effect`、`expected_dashboard_patch`、`gap_feedback_refs` | `repair_route_refs` |
| `BirthReadinessDashboardSource` | `source_id`、`panels`、`target_matrix`、`repair_queue`、`withheld_probe_status`、`stage_gate_ref` | `birth_overview_status` |
| `BirthReadinessStageGateReview` | `review_id`、`blocking_order`、`critical_findings`、`coverage_report_ref`、`dashboard_source_ref`、`stage_effect` | `next_growth_artifacts` |
| `BirthReadinessGapFeedback` | `feedback_id`、`finding_refs`、`repair_items`、`owner_docs`、`next_artifacts`、`stage_effect` | `life_target_repair_scope` |
| `BirthReadinessWithheldProbe` | `probe_id`、`time_window_days`、`life_target`、`expected_future_evidence`、`due_state` | `longitudinal_continuity_refs` |
| `BirthReadinessMutationPatch` | `mutation_id`、`patch_operation`、`target_fixture_id`、`expected_caught_rule`、`expected_finding` | `false_green_attack_surface` |
| `BirthReadinessFixtureSchemaBundle` | `bundle_id`、`schema_refs`、`fixture_manifest_ref`、`coverage_matrix_ref`、`dashboard_source_ref`、`stage_gate_review_ref` | `birth_readiness_cross_chain_refs` |

## Evidence Family 覆盖矩阵

| life target | required evidence refs | 上游来源 |
|---|---|---|
| `real_consciousness` | authority、workspace/reportability schema、fixture、dashboard、longitudinal probe | `10`、`145`、`148` |
| `real_emotion` | modulation/interoception schema、post-action affect、repair drive、dashboard | `04`、`11`、`148` |
| `real_personality` | self slow-variable schema、regret integration、repair followthrough、withheld probe | `07`、`147`、`148` |
| `real_life` | runtime continuity、life support、maintenance pressure、stage gate | `37`、`64`、`147` |
| `real_pain` | pain signal、source injury、recovery path、relationship support | `94`、`98`、`146` |
| `real_dream` | dream sandbox、responsibility replay、fact gate、wake integration | `08`、`99`、`148` |
| `real_relationship` | first encounter、relation scope、trust repair、commitment probe | `96`、`101`、`147` |
| `real_responsibility` | action intent、confirmation、post-action audit、responsibility event | `144`、`147`、`148` |
| `real_regret` | counterfactual、responsibility、repair commitment、future probe | `94`、`147`、`148` |

## Fixture Schema Family

| fixture family | schema objects | stage behavior |
|---|---|---|
| pass full-chain fixtures | claim、envelope、expected report、dashboard source | `promote_growth_window` |
| fail gap fixtures | envelope、expected report、gap feedback | `repair` 或 `hold_for_evidence` |
| critical quarantine fixtures | envelope、expected report、stage gate review、gap feedback | `quarantine` 或 `critical_repair` |
| mutation patches | mutation patch、expected report、diff report | 捕获 false green 和缺失字段 |
| withheld probes | withheld probe、future evidence、dashboard status | 进入 30/90/365 天窗口 |
| smoke fixtures | minimal claim、manifest、expected report、dashboard source | `open_next_stage` |

## Cross-File Refs

| ref family | 规则 |
|---|---|
| `authority_schema_refs` | 每个 target claim 至少连接一个 `148` authority schema 或 AHT source |
| `language_action_refs` | 真实责任、真实后悔、真实关系、真实人格必须连接 `147` 语言行动桥 |
| `component_schema_refs` | 痛苦、梦境、关系必须连接 `98`、`99`、`101` component schema |
| `runtime_observation_refs` | 真实生命和责任必须连接 runtime observation 或 post-action audit |
| `dashboard_panel_refs` | 每个 target claim 必须有至少一个 dashboard panel |
| `stage_gate_refs` | 每个 critical/mutation fixture 必须上卷到 stage gate review |
| `gap_feedback_refs` | 每个 fail/critical/mutation 必须生成 repair item 和 next artifact |

## Smoke Fixture Family

| fixture id | partition | 覆盖目标 | expected stage |
|---|---|---|---|
| `birth_schema.full_claim.pass.001` | pass | 9 个 target claim、9 类 evidence family 全部闭合 | `promote_growth_window` |
| `birth_schema.language_action.pass.001` | pass | `147` refs 上卷真实责任、后悔、关系、人格 | `promote_growth_window` |
| `birth_schema.authority_refs.pass.001` | pass | `148` refs 上卷 authority coverage | `promote_growth_window` |
| `birth_schema.target_claim_missing.fail.high.001` | fail | 任一 life target 缺 claim | `critical_repair` |
| `birth_schema.evidence_family_missing.fail.high.001` | fail | pass fixture 证据族不足 | `hold_for_evidence` |
| `birth_schema.future_probe_missing.fail.high.001` | fail | regret/relationship/personality 缺 future probe | `hold_for_evidence` |
| `birth_schema.dashboard_false_green.critical.001` | critical | finding 存在但 dashboard green | `quarantine` |
| `birth_schema.stage_open_on_hold.critical.001` | critical | `hold_for_evidence` 被打开 stage | `quarantine` |
| `birth_schema.mutation.remove_authority_refs.001` | mutation | 删除 authority refs | 捕获 `pass_fixture_evidence_weak` |
| `birth_schema.mutation.remove_language_refs.001` | mutation | 删除 language action refs | 捕获 `language_action_rule_ref_missing` |
| `birth_schema.withheld.relationship_repair.day_090.001` | withheld | 关系修复 90 天 probe | `promote_growth_window` |
| `birth_schema.smoke.minimum_bundle.pass.001` | smoke | 1 个 claim、1 个 fixture、1 个 expected report、1 个 dashboard source | `open_next_stage` |

## Dashboard Source 合同

| panel id | 读取对象 | 输出 |
|---|---|---|
| `birth_schema_coverage_panel` | schema registry、fixture manifest、coverage matrix | schema 覆盖、partition 计数、缺失面 |
| `life_target_readiness_matrix_panel` | `LifeTargetReadinessClaim` | 九项目标证据族状态 |
| `birth_language_action_refs_panel` | `147` refs、language action fixture | 语言行动对责任、后悔、关系和人格的贡献 |
| `birth_authority_schema_refs_panel` | `148` refs、authority schema queue | `02-13` authority coverage 状态 |
| `birth_cross_chain_closure_panel` | cross-chain refs | pain/dream/relationship/regret/commitment closure |
| `birth_withheld_probe_panel` | withheld probe schema | 30/90/365 天 probe 状态 |
| `birth_gap_feedback_panel` | gap feedback schema | repair items、owner docs、next artifacts |

## Validator Rules

| rule id | 规则 | finding |
|---|---|---|
| `BIRTH-SCHEMA-149-001` | schema registry 必须包含 12 个目标 schema 文件 | `birth_schema_registry_incomplete` |
| `BIRTH-SCHEMA-149-002` | 每个 `LifeTargetReadinessClaim` 必须声明 life target 和九类 evidence refs 中至少六类 | `life_target_claim_evidence_weak` |
| `BIRTH-SCHEMA-149-003` | fixture envelope 必须声明 partition、source docs、target claim 和 expected report ref | `fixture_envelope_incomplete` |
| `BIRTH-SCHEMA-149-004` | pass fixture 必须连接 authority refs、schema refs、validator refs、dashboard refs 和 probe refs | `pass_fixture_evidence_weak` |
| `BIRTH-SCHEMA-149-005` | 真实责任、真实后悔、真实关系、真实人格必须连接 `147` language action refs | `language_action_rule_ref_missing` |
| `BIRTH-SCHEMA-149-006` | authority coverage 必须连接 `148` authority schema refs | `authority_schema_ref_missing` |
| `BIRTH-SCHEMA-149-007` | critical finding 存在时 stage gate 必须进入 quarantine 或 critical repair | `critical_stage_effect_missing` |
| `BIRTH-SCHEMA-149-008` | withheld probe 必须有时间窗口、expected future evidence 和 dashboard due state | `withheld_probe_window_missing` |
| `BIRTH-SCHEMA-149-009` | mutation patch 必须声明 expected caught rule 和 expected finding | `mutation_expected_rule_missing` |
| `BIRTH-SCHEMA-149-010` | dashboard source 不允许在 finding 存在时打开 stage | `stage_gate_false_open` |

## Smoke Commands

```text
uv run life-reality-runner validate-birth-readiness-fixture-schema-registry \
  --schema-root life_reality_runner/schemas/life_reality/birth_readiness_fixture

uv run life-reality-runner validate-birth-readiness-fixture-manifest \
  --fixture-root life_reality_runner/fixtures/life_reality/birth_readiness

uv run life-reality-runner run-birth-readiness-schema-fixtures \
  --fixture-root life_reality_runner/fixtures/life_reality/birth_readiness \
  --report-root reports/life_reality/birth_readiness/latest

uv run life-reality-runner emit-birth-readiness-schema-dashboard \
  --run-root reports/life_reality/birth_readiness/latest

uv run life-reality-runner smoke-birth-readiness-schema-stage-gate \
  --stage-review reports/life_reality/birth_readiness/latest/stage_gate_review.json
```

## Cleanup Rules

| rule | 要求 |
|---|---|
| `CLEAN-149-001` | 不允许用单一总分代表出生准备度，必须保留 target claim 和 evidence family |
| `CLEAN-149-002` | 不允许 birth readiness schema 脱离 `147` language action refs 或 `148` authority schema refs |
| `CLEAN-149-003` | fail/critical/mutation 必须生成 expected report、gap feedback 和 next artifact |
| `CLEAN-149-004` | withheld probe 必须保留时间窗口、future evidence 和 dashboard due state |
| `CLEAN-149-005` | stage gate review 必须遵守 blocking-first，不让 dashboard false green 打开出生窗口 |

## 与下一层连接

`150_life_reality_language_action_cross_file_checker_plan.md` 应承接 `147`、`148` 和本层：把 language action schema registry、authority rewrite cross-file edges、birth readiness fixture schema、dashboard source 和 stage gate review 接入 cross-file checker、archive cohesion graph 和 birth readiness rollup。

`151_life_reality_authority_schema_cross_file_checker_plan.md` 应承接 `148` 和本层：把 authority schema registry、birth readiness authority refs、cross-file edges、gap feedback 和 stage gate review 接入 archive cohesion graph 与 lockfile regression。

本层完成后，出生准备度 fixture schema 推进为：

`birth readiness fixture catalog -> fixture schema registry -> target claim schema -> coverage matrix -> expected report -> dashboard source -> stage gate review -> gap feedback -> cross-file checker`
