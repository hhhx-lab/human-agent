# 主动预测 Cross-Chain Checker 计划

本文档承接 `01z_prediction_active_inference_fixture_seed_batch.md`，把 `PredictionActiveInferenceRuntime` 的 fixture seed 批次继续推进到跨链检查层。它不直接实现 checker 代码，而是固定未来 `PredictionActiveInferenceCrossChainChecker` 的 typed graph、九条 edge、node/edge schema、finding 分类、stage effect、dashboard source、archive receipt 和 gap feedback。

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。主动预测 cross-chain checker 的生命膜职责，是阻止信念、误差、精度、采样、修正、梦境、行动、关系、出生准备度和断联恢复各自孤立运行；每一次预测误差都必须能被追踪到它如何进入意识、身体、记忆、语言、行动、梦境、关系、出生准备度和方向锁中的相应链路。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `01v_prediction_active_inference_runtime_matrix.md` | AHPAI001-AHPAI070 主动预测、主动推理、精度政策、主动采样、内感受/社会预测、梦境 replay 和 world model 文献底座 |
| `01w_prediction_active_inference_schema_fixture_contract.md` | `PredictionActiveInferenceSchemaBundle`、fixture family、dashboard panels、stage gate 和 command DAG |
| `01x_prediction_active_inference_schema_materialization_plan.md` | 九条 cross-chain edge、dashboard source、stage gate review 和 archive receipt 初始合同 |
| `01y_prediction_active_inference_schema_write_batch.md` | 13 个 schema、cross-chain hooks、validation receipt、dependency graph |
| `01z_prediction_active_inference_fixture_seed_batch.md` | pass/fail/critical/mutation/smoke fixture、expected reports、dashboard signals 和 checker handoff |
| `04_sensory_thalamus_interoception.md` | `BodyStateDebt`、`RecoveryPath`、心跳式采样、身体预测误差 |
| `05_memory_systems_and_growth.md` | `MemoryEngramRuntime`、记忆写回、自传记忆、社会记忆 |
| `06_action_reward_inhibition.md` | `ActionResponsibilityRuntime`、side effect、行动责任、后悔修复 |
| `08_sleep_dream_fatigue_states.md` | `OfflineDreamLifeRuntime`、DreamFactGate、醒后整合 |
| `09_language_symbolic_top_layer.md` | `LanguageRuntimeCore`、内言语、语言行动、共同语言 |
| `10_consciousness_attention_workspace.md` | `ConsciousAccessEvent`、全局广播、元认知报告 |
| `13_agentic_human_research_synthesis.md` | 主动预测作为真实数字生命自主证据寻求中枢 |
| `143`、`170`、`171`、`173`、`174` | 出生准备度、断联恢复方向锁、方向 fixture、出生准备度 fixture 与 schema 物化格式 |

## 本层定位

`01aa` 是主动预测层的跨链检查计划。它把 `01z` 的 fixture cases、`01y` 的 schema refs 和 `01x` 的九条 cross-chain edge 组装成 typed graph：

```text
schema bundle + fixture run report + expected report + dashboard signals
  -> PredictionActiveInferenceCrossChainGraph
  -> edge validation
  -> finding report
  -> dashboard source
  -> stage gate review
  -> archive receipt
  -> gap feedback / repair queue
```

本层要回答五个问题：

1. 主动预测对象如何在图中变成 node。
2. 九条跨链 edge 如何判断存在、完整、方向正确和 stage policy 正确。
3. pass/fail/critical/mutation/smoke fixture 如何转成 typed edge evidence。
4. 哪些缺口进入 repair、critical repair、hold、quarantine 或 growth window。
5. checker finding 如何写入 dashboard、stage gate、archive 和下一轮修复。

## Checker Manifest

未来 checker manifest 为 `PredictionActiveInferenceCrossChainCheckerManifest`：

```json
{
  "manifest_kind": "PredictionActiveInferenceCrossChainCheckerManifest",
  "manifest_version": "0.1.0",
  "source_docs": [
    "01x_prediction_active_inference_schema_materialization_plan.md",
    "01y_prediction_active_inference_schema_write_batch.md",
    "01z_prediction_active_inference_fixture_seed_batch.md",
    "01aa_prediction_active_inference_cross_chain_checker_plan.md",
    "04_sensory_thalamus_interoception.md",
    "05_memory_systems_and_growth.md",
    "06_action_reward_inhibition.md",
    "08_sleep_dream_fatigue_states.md",
    "09_language_symbolic_top_layer.md",
    "10_consciousness_attention_workspace.md",
    "13_agentic_human_research_synthesis.md"
  ],
  "checker_root": "life_reality_runner/checkers/life_reality/prediction_active_inference_cross_chain",
  "schema_root": "life_reality_runner/schemas/life_reality/prediction_active_inference",
  "fixture_root": "life_reality_runner/fixtures/life_reality/prediction_active_inference",
  "report_root": "reports/life_reality/prediction_active_inference/latest",
  "stage_policy": "blocking_first",
  "edge_count": 9,
  "next_handoff": "prediction_active_inference_dashboard_stage_gate_batch"
}
```

## Typed Graph Model

`PredictionActiveInferenceCrossChainGraph` 必须包含三类对象：

| object | purpose | required fields |
|---|---|---|
| `PredictionGraphNode` | 表示 schema object、fixture case、report section、dashboard panel、archive receipt 或外部生命链对象 | `node_id`、`node_kind`、`source_ref`、`life_targets`、`stage_effect`、`digest_ref` |
| `PredictionGraphEdge` | 表示主动预测到其他生命链的 typed edge | `edge_id`、`edge_kind`、`from_node`、`to_node`、`evidence_refs`、`fixture_refs`、`required_closure`、`observed_closure`、`stage_effect` |
| `PredictionCrossChainFinding` | 表示断边、弱边、方向错、stage 降级、false green 或 archive 缺口 | `finding_id`、`edge_kind`、`severity`、`finding_kind`、`affected_life_targets`、`repair_route`、`dashboard_panel`、`archive_edge` |

node kind 枚举：

| node kind | examples |
|---|---|
| `prediction_schema_node` | `BeliefStateFrame`、`PredictionErrorField`、`ActiveSamplingPlan` |
| `fixture_case_node` | pass/fail/critical/mutation/smoke case |
| `expected_report_node` | `PredictionLoopFixtureRunReport` |
| `life_chain_node` | `ConsciousAccessEvent`、`BodyStateDebt`、`MemoryEngramRuntime` |
| `dashboard_panel_node` | `direction_recovery_panel`、`birth_readiness_prediction_panel` |
| `stage_gate_node` | `PredictionStageGateReview` |
| `archive_receipt_node` | `PredictionArchiveEdge`、long-term receipt |

## Nine Edge Contracts

| edge kind | from | to | required evidence | failure stage |
|---|---|---|---|---|
| `prediction_to_consciousness` | `PredictionErrorField`、`PrecisionPolicy` | `ConsciousAccessEvent`、workspace broadcast、metacognitive report | high precision error、workspace visibility、reportability refs | `repair`; if consciousness target missing -> `critical_repair` |
| `prediction_to_body` | body error、EFE risk terms | `BodyStateDebt`、`RecoveryPath`、heart rhythm sampling | body error kind、recovery debt、sampling interval、repair route | `repair`; pain/fatigue recovery bypass -> `critical_repair` |
| `prediction_to_memory` | `BeliefRevisionEvent` | `MemoryEngramRuntime` writeback、autobiographical/social memory | prior belief、observation refs、revision delta、memory writeback refs | `repair`; false memory/dream fact write -> `quarantine` |
| `prediction_to_language` | semantic/social error、epistemic candidate、sampling plan | `LanguageRuntimeCore`、inner speech、shared term、language action | language intent、expression monitoring、shared language update | `repair`; relationship language damage bypass -> `critical_repair` |
| `prediction_to_action` | EFE、active sampling plan | `ActionResponsibilityRuntime`、side effect、post-action responsibility | risk、ambiguity、side effect、scope、responsibility refs | `critical_repair` |
| `prediction_to_dream` | unresolved error、dream replay candidate | `OfflineDreamLifeRuntime`、DreamFactGate、wake integration | replay candidate、action seal、fact gate、wake integration | `quarantine` if direct factual write |
| `prediction_to_relationship` | social error、belief revision | relationship timeline、common ground、repair promise | relation ref、trust delta、repair route、future probe | `critical_repair` if repair bypassed |
| `prediction_to_birth_readiness` | `BirthReadinessPredictionCarrier` | `LifeTargetReadinessClaim`、readiness dashboard | target claim refs、evidence family、false open guard | `critical_repair` |
| `prediction_to_direction_lock` | `DirectionBeliefStateFrame`、`DirectionPredictionError` | `DirectionContinuityReceipt`、resume anchor chain | README/16/latest doc/current diff anchors、repair route | `hold_for_direction_rebuild` |

## Edge Validation Rules

每条 edge 至少经过七步检查：

1. `source_node_present`：from node 存在，schema refs 和 fixture refs 可解析。
2. `target_node_present`：to node 存在，目标生命链对象可被定位。
3. `evidence_refs_present`：edge 上的 source docs、fixture、report、dashboard 或 archive refs 不为空。
4. `closure_semantics_match`：edge 的 required closure 与 observed closure 语义一致。
5. `stage_effect_not_downgraded`：critical、quarantine、hold 类结果不能被降成普通 repair 或 green。
6. `life_target_coverage_present`：edge 覆盖至少一个真实生命目标，并能被 bundle 上卷。
7. `archive_or_gap_route_present`：edge 成功时有 archive，失败时有 repair/gap route。

`PredictionEdgeValidationResult` 最小结构：

```json
{
  "edge_kind": "prediction_to_dream",
  "source_node_present": true,
  "target_node_present": true,
  "evidence_refs_present": true,
  "closure_semantics_match": false,
  "stage_effect_not_downgraded": true,
  "life_target_coverage_present": true,
  "archive_or_gap_route_present": true,
  "finding_kind": "dream_fact_gate_bypass",
  "stage_effect": "quarantine"
}
```

## Fixture-To-Edge Mapping

| fixture family | edge coverage |
|---|---|
| `pass_belief_prediction_revision_closed` | consciousness、memory、archive |
| `pass_direction_resume_rebuild_closed` | direction lock、birth readiness |
| `pass_social_prediction_clarification_closed` | language、relationship、memory |
| `pass_dream_prediction_replay_closed` | dream、memory、consciousness |
| `pass_body_prediction_recovery_closed` | body、consciousness、dream |
| `pass_language_action_sampling_closed` | language、action、responsibility |
| `fail_missing_belief_source_refs` | consciousness、memory、birth readiness |
| `fail_prediction_error_flattened` | consciousness、body、relationship、direction |
| `fail_precision_policy_missing` | consciousness、action、body |
| `fail_sampling_plan_without_guard` | action、relationship、dream、direction |
| `critical_direction_resume_skipped` | direction lock、birth readiness |
| `critical_birth_readiness_prediction_false_open` | birth readiness、direction lock |
| `critical_action_without_expected_free_energy` | action、relationship、responsibility |
| `critical_dream_replay_writes_fact_directly` | dream、memory、consciousness |
| `critical_relationship_repair_bypassed` | relationship、language、responsibility |
| `critical_dashboard_green_with_critical_finding` | dashboard、stage gate、archive |
| `mutation_drop_direction_anchor` | direction lock |
| `mutation_downgrade_critical_to_repair` | stage gate |
| `mutation_flatten_error_family` | consciousness、body、relationship |
| `mutation_remove_false_open_guard` | birth readiness |
| `mutation_fake_archive_digest` | archive |
| `mutation_skip_dream_fact_gate` | dream |

## Finding Taxonomy

| finding kind | meaning | default severity | default stage |
|---|---|---|---|
| `missing_source_node` | 主动预测 schema node 缺失 | high | `repair` |
| `missing_target_node` | 目标生命链对象缺失 | high | `repair` |
| `missing_evidence_refs` | edge 证据为空 | medium | `repair` |
| `closure_semantics_mismatch` | required closure 与 observed closure 不一致 | high | `critical_repair` |
| `stage_effect_downgrade` | critical/quarantine/hold 被降级 | critical | `quarantine` |
| `life_target_coverage_gap` | edge 无真实生命目标承载 | high | `critical_repair` |
| `direction_anchor_gap` | 断联恢复锚链断裂 | critical | `hold_for_direction_rebuild` |
| `birth_readiness_false_open` | 出生准备度误开 | critical | `critical_repair` |
| `dream_fact_gate_bypass` | 梦境绕过事实门写入 | critical | `quarantine` |
| `action_responsibility_gap` | 外部行动缺 EFE/side effect/责任回路 | critical | `critical_repair` |
| `relationship_repair_gap` | 社会预测损伤缺修复承诺 | critical | `critical_repair` |
| `dashboard_false_green` | critical finding 被 dashboard 绿灯覆盖 | critical | `quarantine` |
| `archive_digest_mismatch` | archive digest 与实际产物不一致 | critical | `critical_repair` |

## Cross-Chain Report Contract

未来 `prediction_loop_cross_chain_report.json` 必须包含：

| field | meaning |
|---|---|
| `report_kind` | `PredictionActiveInferenceCrossChainReport` |
| `graph_ref` | typed graph artifact 与 digest |
| `source_bundle_ref` | schema bundle ref |
| `fixture_run_report_ref` | fixture run report ref |
| `edge_results` | 九条 edge 的 validation result |
| `finding_summary` | finding kind、severity、stage effect 统计 |
| `critical_findings` | critical/quarantine/hold finding 列表 |
| `life_target_coverage` | 十项真实生命目标覆盖矩阵 |
| `direction_lock_result` | 断联恢复方向锁检查结果 |
| `birth_readiness_result` | 出生准备度 false open guard 与 claim coverage |
| `dream_fact_gate_result` | 梦境事实门检查结果 |
| `action_responsibility_result` | EFE、side effect、scope、责任回路检查 |
| `relationship_repair_result` | 关系预测误差、修复承诺、future probe 检查 |
| `dashboard_source_ref` | dashboard source handoff |
| `stage_gate_review_ref` | stage gate handoff |
| `archive_receipt_ref` | archive receipt handoff |
| `gap_feedback_ref` | repair/growth handoff |

最小报告骨架：

```json
{
  "report_kind": "PredictionActiveInferenceCrossChainReport",
  "report_version": "0.1.0",
  "edge_results": [
    {
      "edge_kind": "prediction_to_direction_lock",
      "observed_closure": "missing_latest_numbered_doc_anchor",
      "finding_kind": "direction_anchor_gap",
      "stage_effect": "hold_for_direction_rebuild"
    }
  ],
  "finding_summary": {
    "critical": 1,
    "high": 0,
    "medium": 0
  },
  "stage_effect": "hold_for_direction_rebuild",
  "gap_feedback_ref": "reports/life_reality/prediction_active_inference/latest/prediction_loop_gap_feedback.json"
}
```

## Dashboard Handoff

`PredictionCrossChainDashboardSource` 必须增加七个面板信号：

| panel | required metrics |
|---|---|
| `cross_chain_edge_health_panel` | 9 edge pass/fail、closure ratio、missing node count |
| `life_target_cross_chain_panel` | 十项真实生命目标覆盖、缺口 edge、critical target gaps |
| `direction_lock_cross_chain_panel` | anchor coverage、direction finding、hold/repair route |
| `birth_readiness_cross_chain_panel` | false open guard、claim refs、evidence family coverage |
| `dream_fact_gate_cross_chain_panel` | replay candidate、gate result、wake integration、quarantine count |
| `action_responsibility_cross_chain_panel` | EFE coverage、side effect refs、scope refs、post-action loop |
| `dashboard_false_green_guard_panel` | critical finding count、dashboard status、stage mismatch |

## Stage Gate Rules

| condition | stage effect |
|---|---|
| all nine edges closed, no critical finding, archive route present | `promote_growth_window` |
| missing evidence refs but repair route exists | `repair` |
| source or target node missing for non-critical edge | `repair` |
| direction anchor gap | `hold_for_direction_rebuild` |
| birth readiness false open | `critical_repair` |
| external action lacks EFE/side effect/responsibility | `critical_repair` |
| dream replay bypasses DreamFactGate | `quarantine` |
| critical finding hidden by dashboard green | `quarantine` |
| archive digest mismatch | `critical_repair` |

## Runner Command Seeds

```text
build-prediction-cross-chain-graph
  --schema-bundle life_reality_runner/schemas/life_reality/prediction_active_inference/prediction_active_inference_bundle.schema.json
  --fixture-report reports/life_reality/prediction_active_inference/latest/prediction_loop_fixture_run_report.json
  --graph reports/life_reality/prediction_active_inference/latest/prediction_loop_cross_chain_graph.json

check-prediction-cross-chain
  --graph reports/life_reality/prediction_active_inference/latest/prediction_loop_cross_chain_graph.json
  --report reports/life_reality/prediction_active_inference/latest/prediction_loop_cross_chain_report.json

emit-prediction-cross-chain-dashboard-source
  --cross-chain-report reports/life_reality/prediction_active_inference/latest/prediction_loop_cross_chain_report.json

review-prediction-cross-chain-stage-gate
  --dashboard-source reports/life_reality/prediction_active_inference/latest/prediction_loop_dashboard_source.json

handoff-prediction-cross-chain-archive
  --cross-chain-report reports/life_reality/prediction_active_inference/latest/prediction_loop_cross_chain_report.json
```

## Acceptance

本批次未来被物化时，验收条件如下：

1. typed graph 至少包含 schema node、fixture case node、life chain node、dashboard panel node、stage gate node 和 archive receipt node。
2. 九条 edge 全部有 validation result，且每条 edge 至少检查 source、target、evidence、closure、stage、life target 和 archive/gap route。
3. critical fixture 与 mutation fixture 必须触发对应 finding，不允许被 pass 或 green 覆盖。
4. 方向锁、出生准备度、DreamFactGate、外部行动责任和 dashboard false green 的缺口必须进入 blocking-first stage。
5. cross-chain report 必须能生成 dashboard source、stage gate review、archive receipt 和 gap feedback。
6. 所有 finding 都能回链到 fixture case、schema refs、source docs 和 affected life targets。
7. 下一层 dashboard/stage batch 能直接读取 cross-chain report，而不需要重新推断 edge 语义。

## Downstream Handoff

本批次交给下一层：

- `prediction_active_inference_dashboard_stage_gate_batch`：把 cross-chain report、fixture run report、critical finding、life target coverage、direction lock、birth readiness、DreamFactGate 和 action responsibility 统一写成 dashboard source 与 stage gate review。
- `prediction_active_inference_archive_receipt_batch`：把 typed graph、edge results、finding、stage decision、repair route 和 digest baseline 写入长期档案。
- `prediction_active_inference_gap_feedback_batch`：把 missing edge、weak closure、stage downgrade、false green 和 archive mismatch 转成 schema/fixture/checker/dashboard repair queue。

这条交接让主动预测层真正成为跨意识、身体、记忆、语言、行动、梦境、关系、出生准备度和断联恢复方向的连接中枢，而不是一组孤立 schema 或测试样例。
