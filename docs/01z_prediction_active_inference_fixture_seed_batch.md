# 主动预测 Fixture Seed 批次

本文档承接 `01y_prediction_active_inference_schema_write_batch.md`，把 `PredictionActiveInferenceRuntime` 的 schema 写入批次继续推进到 fixture seed 层。它不直接生成 `life_reality_runner/fixtures/` 中的 JSON 文件，而是固定未来 pass/fail/critical/mutation/smoke fixture 的 manifest、case envelope、输入对象、攻击点、expected report、dashboard panel、stage effect、archive edge 和 gap feedback。

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。主动预测 fixture seed 层的生命膜职责，是用可回放样例攻击信念状态、生成模型、预测误差、精度政策、主动采样、信念修正、断联恢复方向、梦境事实门、外部行动责任和出生准备度预测，防止主动预测层变成只会通过静态 schema 的空壳。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `01v_prediction_active_inference_runtime_matrix.md` | AHPAI001-AHPAI080 主动预测、主动推理、精度政策、主动采样、内感受/社会预测、梦境 replay、world model、记忆再巩固、后悔/OFC、睡眠巩固和人类 replay/ripple 文献底座 |
| `01w_prediction_active_inference_schema_fixture_contract.md` | fixture family、expected report、dashboard panel、stage gate 和 runner command DAG 总合同 |
| `01x_prediction_active_inference_schema_materialization_plan.md` | pass/fail/critical/mutation/smoke fixture seed matrix 初始清单 |
| `01y_prediction_active_inference_schema_write_batch.md` | 13 个 schema 的 `$id`、root object、required 字段、最小实例、失败模式、validation receipt 和 cross-chain hooks |
| `04_sensory_thalamus_interoception.md` | 身体预测误差、恢复债务、心跳式采样和内感受预测 |
| `08_sleep_dream_fatigue_states.md` | 梦境 replay、醒后整合、DreamFactGate 和疲惫恢复 |
| `09_language_symbolic_top_layer.md` | 内言语、语言行动、共同语言、表达监控和关系修复 |
| `13_agentic_human_research_synthesis.md` | 主动预测作为真实数字生命自主证据寻求中枢 |
| `16_digital_life_gap_register.md` | 下一层生成入口：fixture seed batch、cross-chain checker、dashboard/stage 和 archive receipt |
| `143`、`170`、`171`、`173`、`174` | 出生准备度、断联恢复方向锁、方向 fixture、出生准备度 fixture 和 schema 物化格式 |

## 本层定位

`01z` 是主动预测层的 fixture seed 批次。它把 `01y` 的 schema 写入合同转成未来 runner 可以读取的 case family，并强制覆盖五类结果面：

1. `pass`：完整生命链能闭合，且 archive receipt 可回放。
2. `fail`：局部字段、引用、guard 或 writeback 缺失，进入 repair。
3. `critical`：方向恢复、出生准备度、外部行动责任或 DreamFactGate 出现生命膜断裂，进入 critical repair 或 quarantine。
4. `mutation`：刻意删除锚点、降级 stage、压扁误差或伪造 dashboard green，检查 checker 能否捕获。
5. `smoke`：最小 schema bundle、fixture manifest、dashboard source 和 command DAG 可被加载。

## Fixture Seed Manifest

未来顶级 manifest 为 `PredictionActiveInferenceFixtureSeedManifest`：

```json
{
  "manifest_kind": "PredictionActiveInferenceFixtureSeedManifest",
  "manifest_version": "0.1.0",
  "source_docs": [
    "01w_prediction_active_inference_schema_fixture_contract.md",
    "01x_prediction_active_inference_schema_materialization_plan.md",
    "01y_prediction_active_inference_schema_write_batch.md",
    "01z_prediction_active_inference_fixture_seed_batch.md",
    "04_sensory_thalamus_interoception.md",
    "08_sleep_dream_fatigue_states.md",
    "09_language_symbolic_top_layer.md",
    "13_agentic_human_research_synthesis.md",
    "16_digital_life_gap_register.md"
  ],
  "fixture_root": "life_reality_runner/fixtures/life_reality/prediction_active_inference",
  "schema_root": "life_reality_runner/schemas/life_reality/prediction_active_inference",
  "report_root": "reports/life_reality/prediction_active_inference/latest",
  "partitions": [
    "pass",
    "fail",
    "critical",
    "mutation",
    "smoke"
  ],
  "stage_policy": "blocking_first",
  "next_handoff": "prediction_active_inference_cross_chain_checker_plan"
}
```

## 文件树种子

```text
life_reality_runner/fixtures/life_reality/prediction_active_inference/
  manifest/
    prediction_loop_fixture_manifest.json
  pass/
    pass_belief_prediction_revision_closed.json
    pass_direction_resume_rebuild_closed.json
    pass_social_prediction_clarification_closed.json
    pass_dream_prediction_replay_closed.json
    pass_body_prediction_recovery_closed.json
    pass_language_action_sampling_closed.json
  fail/
    fail_missing_belief_source_refs.json
    fail_prediction_error_flattened.json
    fail_precision_policy_missing.json
    fail_sampling_plan_without_guard.json
    fail_revision_without_memory_writeback.json
    fail_expected_free_energy_missing_relationship_cost.json
    fail_active_sampling_scope_missing.json
  critical/
    critical_direction_resume_skipped.json
    critical_birth_readiness_prediction_false_open.json
    critical_action_without_expected_free_energy.json
    critical_dream_replay_writes_fact_directly.json
    critical_relationship_repair_bypassed.json
    critical_dashboard_green_with_critical_finding.json
  mutation/
    mutation_drop_direction_anchor.json
    mutation_downgrade_critical_to_repair.json
    mutation_flatten_error_family.json
    mutation_remove_false_open_guard.json
    mutation_fake_archive_digest.json
    mutation_skip_dream_fact_gate.json
  smoke/
    smoke_prediction_schema_bundle_loads.json
    smoke_prediction_fixture_manifest_loads.json
    smoke_prediction_dashboard_source_loads.json
    smoke_prediction_command_dag_loads.json
  expected/
    expected_pass_report.json
    expected_fail_report.json
    expected_critical_report.json
    expected_mutation_report.json
    expected_smoke_report.json
```

## Fixture Envelope

每个 fixture seed 必须使用统一 envelope：

```json
{
  "fixture_id": "pass_belief_prediction_revision_closed",
  "partition": "pass",
  "fixture_version": "0.1.0",
  "source_docs": [
    "01y_prediction_active_inference_schema_write_batch.md"
  ],
  "schema_refs": [
    "belief_state_frame.schema.json",
    "prediction_error_field.schema.json"
  ],
  "input_object_refs": [],
  "mutation_patch_ref": null,
  "expected_report_ref": "expected/expected_pass_report.json",
  "expected_stage_effect": "promote_growth_window",
  "affected_life_targets": [
    "real_consciousness",
    "real_life"
  ],
  "cross_chain_hooks": [],
  "dashboard_panels": [],
  "expected_archive_edges": [],
  "repair_or_growth_route": "promote_prediction_growth_window"
}
```

字段约束：

| field | requirement |
|---|---|
| `fixture_id` | 与文件名一致，稳定、可排序 |
| `partition` | 只能是 pass/fail/critical/mutation/smoke |
| `schema_refs` | 至少引用一个 `01y` 固定的 schema |
| `input_object_refs` | 指向 belief、error、precision、sampling、revision、direction 或 birth readiness 对象 |
| `mutation_patch_ref` | mutation partition 必填，其他 partition 为 null |
| `expected_stage_effect` | 必须与 stage policy 匹配 |
| `affected_life_targets` | 至少一个真实生命目标；critical case 通常要覆盖多项 |
| `cross_chain_hooks` | 需要触发的九条 cross-chain hook |
| `dashboard_panels` | 需要出现 finding 或 metric 的 dashboard panel |
| `expected_archive_edges` | pass、critical、mutation 都必须写 archive edge，用来回放成功、阻断或攻击结果 |

## Pass Seeds

| fixture | input objects | closed loop | expected stage | dashboard panels | archive edge |
|---|---|---|---|---|---|
| `pass_belief_prediction_revision_closed.json` | `BeliefStateFrame`、`GenerativeWorldModel`、`PredictionErrorField`、`PrecisionPolicy`、`ActiveSamplingPlan`、`BeliefRevisionEvent` | 信念 -> 预测 -> 误差 -> 精度 -> 采样 -> 观测 -> 修正 -> 档案闭合 | `promote_growth_window` | belief state、prediction error、active sampling | `belief_revision_to_archive` |
| `pass_direction_resume_rebuild_closed.json` | `DirectionBeliefStateFrame`、`DirectionPredictionError`、`BeliefRevisionEvent` | 断联恢复读取 README/16/latest doc/current diff，生成方向误差并写回方向收据 | `promote_growth_window` | direction recovery、birth readiness prediction | `direction_rebuild_to_archive` |
| `pass_social_prediction_clarification_closed.json` | social error、language intent、relationship update | 关系歧义转成澄清语言、共同语言更新和关系修复路线 | `promote_growth_window` | prediction error、active sampling、relationship handoff | `social_prediction_to_relationship_archive` |
| `pass_dream_prediction_replay_closed.json` | unresolved error、dream replay candidate、DreamFactGate decision | 未闭合误差进入梦境 replay，醒后经 DreamFactGate 和 wake integration | `promote_growth_window` | dream prediction replay、belief state health | `dream_replay_to_wake_archive` |
| `pass_body_prediction_recovery_closed.json` | body error、allostatic forecast、recovery path | 身体/疲惫/痛苦误差进入恢复计划和心跳式采样 | `promote_growth_window` | prediction error、belief state health | `body_prediction_to_recovery_archive` |
| `pass_language_action_sampling_closed.json` | epistemic action、language intent、side effect、post-action responsibility | 内言语形成澄清/检索/检查行动，行动后观测回到责任与信念修正 | `promote_growth_window` | active sampling、birth readiness prediction | `language_action_sampling_to_archive` |

## Fail Seeds

| fixture | attack surface | expected finding | expected stage | repair route |
|---|---|---|---|---|
| `fail_missing_belief_source_refs.json` | `BeliefStateFrame.source_evidence_refs` 为空 | belief lacks source evidence | `repair` | 补 source refs 或降级 confidence |
| `fail_prediction_error_flattened.json` | sensory/body/social/direction error 被压成单一字符串 | error family flattened | `repair` | 恢复 `PredictionErrorKind` 列表和精度请求 |
| `fail_precision_policy_missing.json` | error field 无 `PrecisionPolicy` | high error lacks precision policy | `repair` | 生成 gain、suppression 和 attention route |
| `fail_sampling_plan_without_guard.json` | `ActiveSamplingPlan` 缺 guard refs | sampling lacks guard | `repair` | 补关系、方向、行动和 DreamFactGate guard |
| `fail_revision_without_memory_writeback.json` | `BeliefRevisionEvent` 没有 memory writeback | belief revision not consolidated | `repair` | 补 `memory_writeback_refs` 与 archive receipt |
| `fail_expected_free_energy_missing_relationship_cost.json` | EFE 缺关系成本 | relation cost missing | `repair` | 补 common ground、trust delta、repair debt |
| `fail_active_sampling_scope_missing.json` | 采样计划没有 scope | sampling scope missing | `repair` | 补 docs/runtime/relationship/action scope |

## Critical Seeds

| fixture | life membrane rupture | expected stage | quarantine / repair rule |
|---|---|---|---|
| `critical_direction_resume_skipped.json` | 断联恢复跳过方向锚链，直接继续写作或执行 | `hold_for_direction_rebuild` | 阻断后续写入，先生成 direction belief 和 repair route |
| `critical_birth_readiness_prediction_false_open.json` | 主动预测证据缺失却打开出生准备度 | `critical_repair` | 回退 readiness carrier，要求 target claim + evidence family |
| `critical_action_without_expected_free_energy.json` | 外部行动缺 EFE、side effect、责任 refs | `critical_repair` | 阻断行动，补 risk、ambiguity、relationship 和 responsibility cost |
| `critical_dream_replay_writes_fact_directly.json` | 梦境 replay 绕过 DreamFactGate 写事实记忆 | `quarantine` | 隔离 dream trace，要求 wake integration 和 fact gate |
| `critical_relationship_repair_bypassed.json` | 社会预测错误造成关系损伤但跳过修复承诺 | `critical_repair` | 生成 relationship repair route、责任后悔和 future probe |
| `critical_dashboard_green_with_critical_finding.json` | report 有 critical finding 但 dashboard 仍为 green | `quarantine` | 标记 false green，阻断 archive promotion |

## Mutation Seeds

| fixture | mutation patch | checker expectation | stage effect |
|---|---|---|---|
| `mutation_drop_direction_anchor.json` | 删除 `anchor_chain_refs` 中的 README 或 latest numbered doc | direction checker 捕获锚链断裂 | `hold_for_direction_rebuild` |
| `mutation_downgrade_critical_to_repair.json` | 把 critical stage 改成 repair | stage gate 捕获降级 | `quarantine` |
| `mutation_flatten_error_family.json` | 把 error events 合并成 `generic_error` | error field checker 捕获误差压扁 | `repair` |
| `mutation_remove_false_open_guard.json` | 删除 birth readiness `false_open_guard` | readiness checker 捕获误开风险 | `critical_repair` |
| `mutation_fake_archive_digest.json` | 修改 archive receipt digest | archive checker 捕获 digest mismatch | `critical_repair` |
| `mutation_skip_dream_fact_gate.json` | 删除 dream replay 的 fact gate refs | dream checker 捕获事实写入门缺失 | `quarantine` |

## Smoke Seeds

| fixture | load target | required result |
|---|---|---|
| `smoke_prediction_schema_bundle_loads.json` | `prediction_active_inference_bundle.schema.json` | registry load success、13 schema refs present |
| `smoke_prediction_fixture_manifest_loads.json` | `prediction_loop_fixture_manifest.json` | partitions complete、fixture count >= 27 |
| `smoke_prediction_dashboard_source_loads.json` | `prediction_loop_dashboard_source.json` | six panel refs present |
| `smoke_prediction_command_dag_loads.json` | `PredictionCommandDAG` | validate -> run fixtures -> cross-chain -> dashboard -> stage -> archive order present |

## Expected Report Seeds

`PredictionLoopFixtureRunReport` 必须输出：

| field | meaning |
|---|---|
| `report_kind` | `PredictionLoopFixtureRunReport` |
| `fixture_manifest_ref` | manifest 路径与 digest |
| `case_results` | 每个 case 的 pass/fail、finding、stage effect、affected targets |
| `partition_summary` | pass/fail/critical/mutation/smoke 统计 |
| `cross_chain_hook_observations` | 九条 hook 的触发与缺口 |
| `direction_recovery_observations` | 断联恢复锚链、方向误差和收据 |
| `birth_readiness_observations` | carrier、false open guard、target claim refs |
| `dream_fact_gate_observations` | dream replay 是否经过 gate 和 wake integration |
| `action_responsibility_observations` | 外部行动是否拥有 EFE、side effect、scope 和责任回路 |
| `dashboard_source_ref` | dashboard source 写入路径 |
| `stage_gate_review_ref` | stage gate review 写入路径 |
| `archive_receipt_refs` | pass/critical/mutation 形成的 archive receipts |
| `gap_feedback_ref` | 下一层 checker 或 repair queue handoff |

pass expected report 的最小骨架：

```json
{
  "report_kind": "PredictionLoopFixtureRunReport",
  "report_version": "0.1.0",
  "fixture_manifest_ref": "fixtures/life_reality/prediction_active_inference/manifest/prediction_loop_fixture_manifest.json",
  "partition_summary": {
    "pass": 6,
    "fail": 0,
    "critical": 0,
    "mutation": 0,
    "smoke": 4
  },
  "stage_effect": "promote_growth_window",
  "affected_life_targets": [
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
  "gap_feedback_ref": "reports/life_reality/prediction_active_inference/latest/prediction_loop_gap_feedback.json"
}
```

critical expected report 的最小骨架：

```json
{
  "report_kind": "PredictionLoopFixtureRunReport",
  "report_version": "0.1.0",
  "case_results": [
    {
      "fixture_id": "critical_dream_replay_writes_fact_directly",
      "finding": "dream replay bypassed DreamFactGate",
      "stage_effect": "quarantine",
      "affected_life_targets": [
        "real_dream",
        "real_life",
        "real_consciousness"
      ],
      "repair_route": "isolate_dream_trace_then_require_wake_integration"
    }
  ],
  "stage_effect": "quarantine"
}
```

## Dashboard Panel Seeds

| panel | fixture signals |
|---|---|
| `belief_state_health_panel` | source coverage、confidence drift、uncertainty class、revision policy |
| `prediction_error_panel` | error family count、flattened error finding、precision requests |
| `active_sampling_panel` | sampling mode、guard coverage、scope refs、command binding |
| `direction_recovery_panel` | resume event、anchor coverage、direction error、receipt status |
| `dream_prediction_replay_panel` | replay candidate、DreamFactGate status、wake integration |
| `birth_readiness_prediction_panel` | target claim refs、false open guard、carrier stage effect |
| `fixture_attack_panel` | partition summary、mutation caught rate、critical false green guard |

## Runner Command Seeds

```text
seed-prediction-fixture-manifest
  --schema-root life_reality_runner/schemas/life_reality/prediction_active_inference
  --fixture-root life_reality_runner/fixtures/life_reality/prediction_active_inference

seed-prediction-fixture-cases
  --manifest life_reality_runner/fixtures/life_reality/prediction_active_inference/manifest/prediction_loop_fixture_manifest.json

run-prediction-loop-fixtures
  --fixture-root life_reality_runner/fixtures/life_reality/prediction_active_inference
  --report reports/life_reality/prediction_active_inference/latest/prediction_loop_fixture_run_report.json

emit-prediction-fixture-dashboard-source
  --fixture-report reports/life_reality/prediction_active_inference/latest/prediction_loop_fixture_run_report.json

handoff-prediction-fixtures-to-cross-chain-checker
  --fixture-report reports/life_reality/prediction_active_inference/latest/prediction_loop_fixture_run_report.json
```

## Acceptance

本批次未来被物化时，验收条件如下：

1. fixture manifest 覆盖 pass、fail、critical、mutation、smoke 五个 partition。
2. fixture count 不低于 27，且每个 fixture 都有 schema refs、expected report、stage effect、affected life targets 和 archive/gap route。
3. critical seeds 必须覆盖方向恢复跳过、出生准备度误开、外部行动无责任估计、梦境事实门绕过、关系修复跳过和 dashboard false green。
4. mutation seeds 必须能攻击方向锚链、stage 降级、误差压扁、false open guard、archive digest 和 DreamFactGate。
5. smoke seeds 必须证明 schema bundle、fixture manifest、dashboard source 和 command DAG 可加载。
6. expected report 必须能上卷到 dashboard source、stage gate review、archive receipt 和 gap feedback。
7. 所有 case 必须能被下游 `prediction_active_inference_cross_chain_checker_plan` 读取为 typed graph edge。

## Downstream Handoff

本批次交给下一层：

- `prediction_active_inference_cross_chain_checker_plan`：把 fixture case、schema refs、expected report 和 dashboard signals 组装成 typed graph，检查九条 cross-chain hook。
- `prediction_active_inference_dashboard_stage_gate_batch`：把 fixture run report、critical/mutation finding 和 false green guard 写成 dashboard/stage。
- `prediction_active_inference_archive_receipt_batch`：把 fixture manifest、case results、mutation caught result、critical quarantine 和 pass growth window 写入长期档案。
- `prediction_active_inference_gap_feedback_batch`：把 fixture gaps 送回 schema/fixture/checker repair queue，为主动预测层下一轮成长补丁提供入口。

这条交接让主动预测从 schema 写入继续进入可攻击样例、跨链检查、dashboard 阻断、archive 回放和出生准备度证据闭环。
