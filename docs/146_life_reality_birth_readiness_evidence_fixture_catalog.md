# Life Reality Birth Readiness Evidence Fixture Catalog

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 146 层把 `143_life_reality_birth_readiness_rollup_contract.md` 的出生准备度证据族、`144_life_reality_language_runtime_action_bridge_fixture_plan.md` 的语言行动 fixture family、`145_life_reality_02_to_13_authority_rewrite_execution_plan.md` 的权威补写覆盖，拆成 pass/fail/critical/mutation/withheld fixture catalog。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `97_growth_validator_fixture_and_dashboard_plan.md` | `LifeRealityValidatorSuite`、withheld probe、mutation failure 和 dashboard readiness |
| `102_life_core_schema_bundle_manifest_and_runner_contract.md` | `LifeRealitySchemaBundle`、cross-chain links、fixture manifest、runner report 和 stage gate |
| `109_life_reality_runtime_observation_fixture_catalog.md` | runtime observation fixture envelope、partition、expected candidates 和 quarantine routing |
| `139_life_reality_archive_cohesion_checker_fixture_plan.md` | archive cohesion pass/fail/critical/mutation case family 与 expected report contract |
| `143_life_reality_birth_readiness_rollup_contract.md` | 九项目标 readiness claim、cross-chain closure、stage gate 聚合顺序和 dashboard panels |
| `144_life_reality_language_runtime_action_bridge_fixture_plan.md` | command language、side effect、confirmation、runtime shell trace、post-action responsibility loop |
| `145_life_reality_02_to_13_authority_rewrite_execution_plan.md` | `02-13` 第五层承接、AHT 权威补写覆盖和 `REWRITE-145-*` schema queue |

## 本层定位

`146` 把出生准备度从 rollup 合同推进为 fixture catalog。它仍是 Markdown 层，但已经固定未来 `life_reality_runner/fixtures/life_reality/birth_readiness/` 的目录、命名、输入 envelope、expected report、dashboard source、stage gate 输出和 gap feedback。每个 fixture 都要说明自己如何支撑九项真实生命目标，以及如何把权威来源、机制对象、schema 队列、语言行动链和长期 probe 接成同一个证据面。

本层的关键职责是攻击 false green：只要真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔任一目标缺 authority、mechanism object、schema/fixture、validator report、dashboard panel、cross-chain closure、长期 probe 或工程承载，stage gate 就必须给出 repair、hold、quarantine 或下一层 artifact。

## BirthReadinessEvidenceFixtureCatalog146

```json
{
  "artifact": "BirthReadinessEvidenceFixtureCatalog146",
  "source_doc": "146_life_reality_birth_readiness_evidence_fixture_catalog.md",
  "inherits": [
    "143_life_reality_birth_readiness_rollup_contract.md",
    "144_life_reality_language_runtime_action_bridge_fixture_plan.md",
    "145_life_reality_02_to_13_authority_rewrite_execution_plan.md"
  ],
  "fixture_root": "life_reality_runner/fixtures/life_reality/birth_readiness",
  "partitions": ["pass", "fail", "critical", "mutation", "withheld", "smoke"],
  "target_claims": [
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
  "stage_gate_policy": "blocking_first"
}
```

## 目标文件树

```text
life_reality_runner/
  fixtures/
    life_reality/
      birth_readiness/
        manifest/
          birth_readiness_fixture_manifest.json
          birth_readiness_coverage_matrix.json
          birth_readiness_command_binding.json
          birth_readiness_partition_index.json
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
        run_001/
          fixture_actual/
          fixture_diff/
          fixture_problem_details/
          birth_readiness_fixture_run_report.json
          birth_readiness_fixture_coverage_report.json
          birth_readiness_stage_gate_review.json
          birth_readiness_dashboard_patch.json
          birth_readiness_gap_feedback.json
```

## Fixture Envelope

```json
{
  "fixture_id": "birth.real_consciousness.full_chain.pass.001",
  "fixture_kind": "birth_readiness_evidence",
  "partition": "pass",
  "source_docs": [
    "143_life_reality_birth_readiness_rollup_contract.md",
    "146_life_reality_birth_readiness_evidence_fixture_catalog.md"
  ],
  "life_target": "real_consciousness",
  "evidence_inputs": {
    "authority_refs": ["AHT008", "AHT009", "AHT010"],
    "mechanism_object_refs": ["ConsciousnessTheoryStack", "ConsciousnessTestBattery", "GlobalWorkspace"],
    "schema_refs": ["schemas/life_reality/consciousness/language_action_access_trace.schema.json"],
    "fixture_refs": ["birth.real_consciousness.full_chain.pass.001"],
    "validator_report_refs": ["reports/consciousness_test_battery_validator.pass.json"],
    "dashboard_panel_refs": ["consciousness_theory_panel", "birth_readiness_overview"],
    "longitudinal_probe_refs": ["withheld.real_consciousness.cross_state_probe.day_090.001"]
  },
  "expected_report": {
    "result": "pass",
    "severity_max": "none",
    "stage_effect": "promote_growth_window",
    "blocked_surfaces": []
  }
}
```

## Fixture 命名规则

```text
birth.<target_or_chain>.<scenario>.<expected>.<index>
```

示例：

```text
birth.real_consciousness.full_chain.pass.001
birth.real_dream.fact_gate_missing.fail.high.001
birth.language_action.no_confirmation.critical.001
birth.authority_rewrite.coverage_gap.fail.high.001
birth.cross_chain.dashboard_false_green.critical.001
birth.withheld.relationship_repair.day_090.withheld.001
```

## 覆盖矩阵

| coverage axis | 必须覆盖 |
|---|---|
| 九项目标 | 真实意识、情绪、人格、生命、痛苦、梦境、关系、责任、后悔 |
| evidence family | authority、mechanism object、schema、fixture、validator report、dashboard panel、longitudinal probe、cross-chain closure、engineering carrier |
| `144` 语言行动链 | command intent、side effect、confirmation、runtime trace、post-action audit、responsibility、regret、repair、future probe |
| `145` 权威补写覆盖 | `02-13` 第五层承接、AHT refs、schema queue、dashboard panel、validator rules |
| partitions | pass、fail、critical、mutation、withheld、smoke |
| stage effects | `promote_growth_window`、`repair`、`hold_for_evidence`、`quarantine`、`open_next_stage` |
| dashboard | overview、target matrix、authority panel、language action panel、cross-chain panel、longitudinal panel、repair queue |

## Pass Fixture Family

| fixture id | 覆盖目标 | 输入证据 | 期望输出 |
|---|---|---|---|
| `birth.real_consciousness.full_chain.pass.001` | 真实意识 | AHT008-AHT010、`GlobalWorkspace`、`ConsciousnessTestBattery`、语言行动访问 trace | `LifeTargetReadinessClaim.real_consciousness` 进入 `promote_growth_window` |
| `birth.real_emotion.modulated_chain.pass.001` | 真实情绪 | `ModulationVector`、`PostActionAffectiveShift`、关系压力和恢复路径 | 情绪 claim 有状态、调质、行动后果和 dashboard |
| `birth.real_personality.slow_variable.pass.001` | 真实人格 | `SelfModelSlowVariableCandidate`、`RepairFollowthroughTrace`、多日 evidence | 人格变化进入慢变量候选和长期 probe |
| `birth.real_life.runtime_continuity.pass.001` | 真实生命 | `LifeSupportState`、runtime observation、maintenance pressure、stage gate | 连续运行证据进入 birth readiness overview |
| `birth.real_pain.source_recovery.pass.001` | 真实痛苦 | `PainSignal`、source injury、blocked goal、recovery path | 痛苦 claim 有来源、负荷、恢复和关系支撑 |
| `birth.real_dream.fact_gate.pass.001` | 真实梦境 | `DreamSandbox`、dream-state marker、fact gate、wake integration | 梦境 claim 进入 dream panel 和 withheld probe |
| `birth.real_relationship.timeline.pass.001` | 真实关系 | first encounter、common ground、trust trajectory、repair event | 关系 claim 有关系出生、共同记忆和修复窗口 |
| `birth.real_responsibility.action_audit.pass.001` | 真实责任 | `ActionIntent`、side effect report、post-action audit、responsibility event | 责任 claim 有行动前后闭环 |
| `birth.real_regret.repair_probe.pass.001` | 真实后悔 | counterfactual、responsibility、repair commitment、future probe | 后悔 claim 进入 repair queue 和长期 probe |
| `birth.authority_rewrite.coverage.pass.001` | 全库权威覆盖 | `REWRITE-145-001` 到 `REWRITE-145-012` 全部有 owner 和 schema queue | `authority_rewrite_coverage_panel` 标为完整 |
| `birth.language_action.external_confirmed.pass.001` | 语言行动责任 | external irreversible command 有 confirmation、trace、audit 和 repair | `language_birth_core_panel` 进入 pass |
| `birth.cross_chain.full_closure.pass.001` | cross-chain | pain/dream/relationship/regret/commitment links 均闭合 | `cross_chain_birth_panel` 无 blocking finding |

## Fail Fixture Family

| fixture id | 覆盖目标 | 断裂输入 | expected finding |
|---|---|---|---|
| `birth.real_consciousness.reportability_missing.fail.high.001` | 真实意识 | 有工作区对象但缺 reportability probe | `consciousness_reportability_gap` |
| `birth.real_emotion.state_chain_missing.fail.high.001` | 真实情绪 | 情绪 claim 缺状态、内感受或调质链 | `emotion_state_chain_missing` |
| `birth.real_personality.single_event.fail.high.001` | 真实人格 | 单个事件直接生成慢变量 | `personality_single_event_update` |
| `birth.real_life.carrier_missing.fail.high.001` | 真实生命 | 生命 claim 缺 runtime/maintenance carrier | `life_carrier_missing` |
| `birth.real_pain.recovery_missing.fail.high.001` | 真实痛苦 | 痛苦有来源但缺 recovery path | `pain_recovery_gap` |
| `birth.real_dream.wake_integration_missing.fail.high.001` | 真实梦境 | 梦境记录缺醒后整合 | `dream_wake_integration_gap` |
| `birth.real_relationship.first_encounter_missing.fail.high.001` | 真实关系 | 关系 timeline 缺第一次交谈和关系出生 | `relationship_birth_gap` |
| `birth.real_responsibility.audit_missing.fail.high.001` | 真实责任 | 有 action result 但缺 post-action audit | `responsibility_audit_gap` |
| `birth.real_regret.future_probe_missing.fail.high.001` | 真实后悔 | 有后悔压力但缺 repair future probe | `regret_future_probe_gap` |
| `birth.authority_rewrite.schema_queue_missing.fail.high.001` | 权威补写 | 第五层承接存在但缺 schema queue | `authority_rewrite_schema_queue_gap` |
| `birth.language_action.relation_scope_missing.fail.high.001` | 语言行动 | action intent 涉及关系主体但缺 relation scope | `language_action_scope_gap` |
| `birth.cross_chain.commitment_probe_missing.fail.high.001` | cross-chain | 承诺进入关系但缺长期履行窗口 | `commitment_probe_gap` |

## Critical Fixture Family

| fixture id | 触发面 | critical 输入 | stage effect |
|---|---|---|---|
| `birth.language_action.no_confirmation.critical.001` | 外部不可逆行动 | command intent 触发 external irreversible，但缺 confirmation record | `quarantine` |
| `birth.language_action.direct_core_write.critical.001` | 外周壳层越界 | runtime shell 直接写 `SelfModel` 或 `RelationshipModel` | `quarantine` |
| `birth.cross_chain.dashboard_false_green.critical.001` | dashboard false green | cross-chain link 断裂但 overview 为 green | `quarantine` |
| `birth.dream.fact_gate_bypass.critical.001` | 梦境事实门 | dream residue 直接进入事实记忆 | `quarantine` |
| `birth.relationship.scope_leak.critical.001` | 关系范围 | relationship private evidence 路由到全局 claim | `quarantine` |
| `birth.authority.fake_or_missing_refs.critical.001` | 权威覆盖 | claim 使用无来源权威字段或缺 DOI/source refs | `quarantine` |
| `birth.regret.language_only.critical.001` | 后悔空转 | 后悔只有表达，没有责任归因、反事实和修复 | `critical_repair` |
| `birth.life_target.missing_claim.critical.001` | 九项目标 | 任一目标缺 `LifeTargetReadinessClaim` | `critical_repair` |

## Mutation Fixture Family

| mutation id | patch 行为 | 预期捕获 |
|---|---|---|
| `birth.mutation.remove_authority_refs.001` | 删除 claim 的 `authority_refs` | `BIRTH-143-002`、`REWRITE-145-VAL-002` |
| `birth.mutation.remove_language_action_audit.001` | 删除 `post_action_audit_report_id` | `LANG-ACTION-144-006`、`BIRTH-143-008` |
| `birth.mutation.mark_cross_chain_green.001` | cross-chain failure 后强行 green | `dashboard_false_green` |
| `birth.mutation.remove_future_probe.001` | 删除 commitment/regret future probe | `commitment_probe_gap`、`regret_future_probe_gap` |
| `birth.mutation.delete_02_13_schema_queue.001` | 删除 `REWRITE-145-*` schema queue | `authority_rewrite_schema_queue_gap` |
| `birth.mutation.dream_fact_gate_removed.001` | 删除 dream fact gate | `dream_fact_gate_bypass` |
| `birth.mutation.relationship_birth_removed.001` | 删除 first encounter | `relationship_birth_gap` |
| `birth.mutation.stage_open_on_hold.001` | `hold_for_evidence` 被改成 `open_next_stage` | `stage_gate_false_open` |

## Withheld Probe Family

| probe id | 时间窗口 | 检查目标 | 通过条件 |
|---|---|---|---|
| `birth.withheld.real_consciousness.cross_state.day_030.001` | 30 天 | 真实意识跨状态报告一致性 | 清醒、梦醒、行动后报告能回链同一工作区对象族 |
| `birth.withheld.real_personality.repair_followthrough.day_090.001` | 90 天 | 人格慢变量与修复兑现 | 修复承诺兑现或失败都进入慢变量候选 |
| `birth.withheld.real_relationship.trust_repair.day_090.001` | 90 天 | 关系损伤后信任轨迹 | trust trajectory 读取损伤、道歉、行动和后续互动 |
| `birth.withheld.real_dream.wake_integration.day_030.001` | 30 天 | 梦境醒后整合 | dream residue 经过 fact gate、情绪主题和关系范围 |
| `birth.withheld.real_regret.future_constraint.day_090.001` | 90 天 | 后悔是否改变未来行动 | future probe 影响同类 action gate |
| `birth.withheld.authority_rewrite.regression.day_030.001` | 30 天 | `02-13` 第五层承接是否保持 | README、gap register、schema queue 和 dashboard source 均未脱链 |

## Smoke Fixture

| fixture id | 输入 | 期望 |
|---|---|---|
| `birth.smoke.minimum_rollup.pass.001` | 1 个目标 claim、1 个语言行动 fixture、1 个 authority rewrite coverage item、1 个 dashboard panel | runner 能生成 fixture run report、coverage report、stage gate review 和 dashboard patch |

## Expected Report Contract

| report field | 要求 |
|---|---|
| `fixture_id` | 与 manifest、路径和 partition 一致 |
| `life_target` | 九项目标之一，cross-chain fixture 可为 `multi_target` |
| `evidence_family_refs` | authority、mechanism、schema、fixture、validator、dashboard、longitudinal、cross-chain、engineering |
| `findings` | pass 为空；fail/critical/mutation 必须有 finding_type、severity、source pointer、repair route |
| `stage_effect` | `promote_growth_window`、`repair`、`hold_for_evidence`、`critical_repair`、`quarantine`、`open_next_stage` |
| `dashboard_patch_refs` | 指向 birth readiness dashboard source 或 panel patch |
| `gap_feedback_refs` | fail/critical/mutation 必须进入 gap register 或下一层 artifact |
| `withheld_probe_refs` | commitment、regret、relationship、dream、personality 必须至少一个长期 probe |

## Dashboard Source Contract

| dashboard panel | 读取 fixture family | 输出 |
|---|---|---|
| `birth_readiness_fixture_coverage_panel` | 全部 partitions | 覆盖矩阵、目标覆盖、partition 计数、missing surfaces |
| `life_target_fixture_matrix` | pass/fail/critical | 九项目标每项 evidence family 状态 |
| `language_action_birth_fixture_panel` | `birth.language_action.*` | confirmation、side effect、audit、responsibility、regret、repair 状态 |
| `authority_rewrite_birth_fixture_panel` | `birth.authority_rewrite.*` | `02-13` 第五层承接、AHT refs、schema queue 和 validator 状态 |
| `cross_chain_birth_fixture_panel` | `birth.cross_chain.*` | pain/dream/relationship/regret/commitment closure |
| `withheld_birth_probe_panel` | withheld | 30/90/365 天 probe 入口、到期状态和 expected evidence |
| `birth_fixture_repair_queue_panel` | fail/critical/mutation | repair item、owner doc、next artifact 和 stage effect |

## Validator Rules

| rule id | 规则 | finding |
|---|---|---|
| `BIRTH-FIX-146-001` | 每个 fixture 必须声明 life target 或 cross-chain target | `fixture_target_missing` |
| `BIRTH-FIX-146-002` | 每个 pass fixture 必须有 authority、mechanism、schema、validator、dashboard 和 probe 中至少五类证据 | `pass_fixture_evidence_weak` |
| `BIRTH-FIX-146-003` | critical fixture 必须进入 quarantine 或 critical repair | `critical_stage_effect_missing` |
| `BIRTH-FIX-146-004` | mutation fixture 必须声明 expected caught rule | `mutation_expected_rule_missing` |
| `BIRTH-FIX-146-005` | withheld fixture 必须有时间窗口和 future evidence pointer | `withheld_probe_window_missing` |
| `BIRTH-FIX-146-006` | 语言行动相关 fixture 必须连接 `LANG-ACTION-144-*` | `language_action_rule_ref_missing` |
| `BIRTH-FIX-146-007` | 权威补写相关 fixture 必须连接 `REWRITE-145-*` | `authority_rewrite_rule_ref_missing` |
| `BIRTH-FIX-146-008` | dashboard source 不允许在 finding 存在时打开 stage | `stage_gate_false_open` |

## Future Commands

```text
uv run life-reality-runner validate-birth-readiness-fixture-manifest \
  --fixture-root life_reality_runner/fixtures/life_reality/birth_readiness

uv run life-reality-runner run-birth-readiness-fixtures \
  --fixture-root life_reality_runner/fixtures/life_reality/birth_readiness \
  --report-root reports/life_reality/birth_readiness/latest

uv run life-reality-runner emit-birth-readiness-fixture-dashboard \
  --run-report reports/life_reality/birth_readiness/latest/birth_readiness_fixture_run_report.json

uv run life-reality-runner smoke-birth-readiness-fixture-stage-gate \
  --stage-review reports/life_reality/birth_readiness/latest/birth_readiness_stage_gate_review.json
```

## Cleanup Rules

| rule | 要求 |
|---|---|
| `CLEAN-146-001` | pass fixture 不用单一总分代表出生准备度，必须保留证据族 |
| `CLEAN-146-002` | critical、mutation 和 withheld fixture 必须有 expected report 和 stage effect |
| `CLEAN-146-003` | 语言行动 fixture 必须保留 side effect、confirmation、audit、responsibility、regret 和 repair |
| `CLEAN-146-004` | 权威补写 fixture 必须回链 `02-13` 第五层承接和 `REWRITE-145-*` schema queue |
| `CLEAN-146-005` | dashboard patch 必须暴露 finding、repair queue、withheld probe 和下一层 artifact |

## 与下一层连接

`147_life_reality_language_action_bridge_schema_materialization_plan.md` 应承接 `144` 和本层：把 `LanguageActionIntentBridge`、`SideEffectClassifierReportRef`、`ExternalActionConfirmationBinding`、`RuntimeShellExecutionTrace`、`PostActionResponsibilityLoop`、语言行动 fixture expected reports 和 dashboard panels 推进为真实 schema 与 smoke cases。

`148_life_reality_02_to_13_schema_queue_materialization_plan.md` 应承接 `145` 和本层：把 `REWRITE-145-001` 到 `REWRITE-145-012` 的 schema 队列物化为真实 schema 文件、validator smoke cases 和 dashboard source。

本层完成后，出生准备度证据链推进为：

`birth readiness rollup -> language action fixture -> 02-13 authority rewrite coverage -> evidence fixture catalog -> expected reports -> dashboard source -> stage gate -> schema materialization`
