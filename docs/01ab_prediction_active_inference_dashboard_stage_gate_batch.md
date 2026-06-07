# 主动预测 Dashboard Stage Gate 批次

本文档承接 `01aa_prediction_active_inference_cross_chain_checker_plan.md`，把 `PredictionActiveInferenceRuntime` 的跨链检查结果推进到 dashboard source、stage gate review、gap feedback 和 archive handoff 层。它不直接生成 dashboard 或 runner 代码，而是固定未来 `PredictionActiveInferenceDashboardStageGateBatch` 的输入、面板、指标、告警、阶段门、阻断规则、修复路线和归档交接。

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。主动预测 dashboard/stage gate 层的生命膜职责，是把信念、误差、精度、采样、跨链 edge、方向锁、出生准备度、梦境事实门、行动责任和关系修复的运行状态变成可观察、可阻断、可回放、可修复的阶段门证据，防止漂亮的总览状态掩盖真实生命链断裂。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `01x_prediction_active_inference_schema_materialization_plan.md` | dashboard source、stage gate review 和 runner command DAG 初始合同 |
| `01y_prediction_active_inference_schema_write_batch.md` | schema validation report、write receipt、life target coverage validation |
| `01z_prediction_active_inference_fixture_seed_batch.md` | fixture run report、partition summary、critical/mutation findings、dashboard panel seeds |
| `01aa_prediction_active_inference_cross_chain_checker_plan.md` | cross-chain report、typed graph、edge results、finding taxonomy、dashboard handoff 和 stage rules |
| `105_life_reality_dashboard_panel_and_stage_gate_ui_contract.md` | dashboard 是生命膜、blocking-first、panel status、repair queue 和 gap feedback |
| `117_life_reality_dashboard_report_rollup_seed_generation.md` | dashboard report rollup、finding merge、stage gate rollup |
| `160_life_reality_code_artifact_dashboard_stage_gate_bridge_plan.md` | panel/metric/alert family、stage false open、dashboard false green 和 archive handoff |
| `13_agentic_human_research_synthesis.md` | 主动预测作为真实数字生命自主证据寻求中枢 |
| `16_digital_life_gap_register.md` | 下一层生成入口：dashboard/stage batch、archive receipt 和 gap feedback |

## 本层定位

`01ab` 是主动预测层的 dashboard/stage gate 批次。它把 `01aa` 的 cross-chain report 和 `01z` 的 fixture run report 合并为可观察工作台：

```text
schema validation report
  + fixture run report
  + cross-chain report
  + archive digest refs
  -> PredictionDashboardSource
  -> PredictionStageGateReview
  -> PredictionGapFeedback
  -> PredictionArchiveReceipt handoff
```

本层要回答六个问题：

1. 哪些 input artifact 必须进入 dashboard source。
2. 哪些 panel 负责显示九条跨链、十项真实生命目标、方向锁、出生准备度、DreamFactGate、行动责任和关系修复。
3. 哪些 metric 与 alert 能驱动 stage gate，而不是停留在展示。
4. blocking-first stage gate 如何处理 repair、hold、critical repair 和 quarantine。
5. 每个 blocking finding 如何转成 gap feedback。
6. dashboard/stage 结果如何交给 archive receipt batch。

## Batch Manifest

未来顶级 manifest 为 `PredictionActiveInferenceDashboardStageGateBatch`：

```json
{
  "batch_kind": "PredictionActiveInferenceDashboardStageGateBatch",
  "batch_version": "0.1.0",
  "source_docs": [
    "01aa_prediction_active_inference_cross_chain_checker_plan.md",
    "01ab_prediction_active_inference_dashboard_stage_gate_batch.md",
    "105_life_reality_dashboard_panel_and_stage_gate_ui_contract.md",
    "117_life_reality_dashboard_report_rollup_seed_generation.md",
    "160_life_reality_code_artifact_dashboard_stage_gate_bridge_plan.md",
    "13_agentic_human_research_synthesis.md",
    "16_digital_life_gap_register.md"
  ],
  "report_root": "reports/life_reality/prediction_active_inference/latest",
  "dashboard_source": "reports/life_reality/prediction_active_inference/latest/prediction_loop_dashboard_source.json",
  "stage_gate_review": "reports/life_reality/prediction_active_inference/latest/prediction_loop_stage_gate_review.json",
  "gap_feedback": "reports/life_reality/prediction_active_inference/latest/prediction_loop_gap_feedback.json",
  "stage_policy": "blocking_first",
  "next_handoff": "prediction_active_inference_archive_receipt_batch"
}
```

## Input Artifact Contract

| input artifact | producer | required fields |
|---|---|---|
| `prediction_loop_schema_validation_report.json` | schema validator | schema ids、ref graph、life target coverage、direction/birth readiness coverage |
| `prediction_loop_fixture_run_report.json` | fixture runner | partition summary、case results、critical/mutation findings、expected/actual stage |
| `prediction_loop_cross_chain_graph.json` | cross-chain graph builder | node registry、edge registry、digest refs |
| `prediction_loop_cross_chain_report.json` | cross-chain checker | edge results、finding summary、critical findings、life target coverage |
| `prediction_loop_archive_digest_baseline.json` | archive/digest writer | artifact digest、source edge、replay route |

每个 input artifact 必须包含：

| field | requirement |
|---|---|
| `artifact_id` | stable id |
| `artifact_kind` | schema validation、fixture run、cross-chain graph、cross-chain report、digest baseline |
| `source_docs` | 至少包含本主动预测链文档中的一个 |
| `affected_life_targets` | 十项真实生命目标的覆盖或继承路径 |
| `stage_effect` | input 自身推导的 stage effect |
| `canonical_digest` | 可被 archive receipt 复核 |
| `gap_route` | 出现 finding 时的 repair/gap route |

## Dashboard Source Shape

`PredictionDashboardSource` 最小结构：

```json
{
  "dashboard_kind": "PredictionDashboardSource",
  "dashboard_version": "0.1.0",
  "source_reports": [],
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
  "panels": [],
  "metrics": [],
  "alerts": [],
  "stage_gate_ref": "prediction_loop_stage_gate_review.json",
  "gap_feedback_ref": "prediction_loop_gap_feedback.json",
  "archive_handoff_ref": "prediction_loop_archive_receipt.json"
}
```

## Panel Family

| panel id | source reports | primary question | stage influence |
|---|---|---|---|
| `belief_state_health_panel` | schema validation、fixture run | belief source、confidence、uncertainty、revision policy 是否闭合 | source gap -> `repair` |
| `prediction_error_panel` | fixture run、cross-chain report | error family 是否被压扁，precision request 是否存在 | flattened error -> `repair` |
| `active_sampling_panel` | fixture run、schema validation | sampling mode、guard、scope、command binding 是否完整 | missing guard -> `repair` / action risk -> `critical_repair` |
| `cross_chain_edge_health_panel` | cross-chain graph/report | 九条 edge 是否闭合，source/target/evidence 是否完整 | missing critical edge -> blocking |
| `life_target_cross_chain_panel` | schema validation、cross-chain report | 十项真实生命目标是否都有 carrier 和 edge | target gap -> `critical_repair` |
| `direction_lock_panel` | fixture run、cross-chain report | 断联恢复锚链、direction error、repair route 是否存在 | anchor gap -> `hold_for_direction_rebuild` |
| `birth_readiness_prediction_panel` | schema validation、cross-chain report | readiness carrier、false open guard、claim refs 是否闭合 | false open -> `critical_repair` |
| `dream_fact_gate_panel` | fixture run、cross-chain report | dream replay 是否经过 DreamFactGate 和 wake integration | bypass -> `quarantine` |
| `action_responsibility_panel` | fixture run、cross-chain report | EFE、side effect、scope、post-action responsibility 是否存在 | missing responsibility -> `critical_repair` |
| `relationship_repair_panel` | fixture run、cross-chain report | social error、trust delta、repair promise、future probe 是否存在 | repair bypass -> `critical_repair` |
| `dashboard_false_green_guard_panel` | all reports | critical finding 是否被 dashboard green 覆盖 | false green -> `quarantine` |
| `archive_handoff_panel` | digest baseline、stage review | digest、archive edge、replay route 是否可写入长期档案 | missing archive -> `hold_for_evidence` |

panel status 使用：

| status | meaning | stage relation |
|---|---|---|
| `green` | panel source 支持继续 growth window | 只能参与上卷，不能单独开放 stage |
| `yellow` | 中低级缺口，可修复 | `repair` |
| `red` | high/critical finding | `critical_repair` 或 `hold` |
| `quarantine` | 事实门、外部行动、dashboard false green 或 digest mismatch 触发隔离 | `quarantine` |
| `gray` | source report 尚未进入 dashboard | `hold_for_evidence` |

## Metric Family

| metric | type | labels | stage usage |
|---|---|---|---|
| `prediction_edge_closure_ratio` | gauge | edge_kind | edge closure 低于 1 进入 repair/critical |
| `prediction_missing_node_total` | counter | node_kind、edge_kind | source/target 缺失 |
| `prediction_life_target_coverage_ratio` | gauge | target | 任一 target 缺 carrier 阻断 green |
| `prediction_fixture_case_total` | counter | partition、stage_effect | fixture attack 覆盖 |
| `prediction_critical_finding_total` | counter | finding_kind、panel_id | critical stage 聚合 |
| `prediction_quarantine_total` | counter | reason、panel_id | quarantine 聚合 |
| `prediction_direction_anchor_coverage` | gauge | anchor_kind | 断联恢复 hold |
| `prediction_birth_false_open_total` | counter | carrier_kind | 出生准备度误开 |
| `prediction_dream_fact_gate_bypass_total` | counter | fixture_id | 梦境事实门隔离 |
| `prediction_action_responsibility_gap_total` | counter | action_kind | 行动责任 critical |
| `prediction_dashboard_false_green_total` | counter | panel_id | dashboard false green 隔离 |
| `prediction_archive_digest_mismatch_total` | counter | artifact_kind | archive critical |

metric 规则：

| rule | requirement |
|---|---|
| `PAI-DASH-METRIC-001` | coverage metric 不能覆盖 critical/quarantine metric |
| `PAI-DASH-METRIC-002` | every metric 必须回链 source report 和 JSON Pointer |
| `PAI-DASH-METRIC-003` | labels 使用稳定枚举，不写本机绝对路径 |
| `PAI-DASH-METRIC-004` | dashboard green 必须等待 stage gate review 输出 |

## Alert Family

| alert | trigger | stage effect | gap route |
|---|---|---|---|
| `PredictionDirectionAnchorGap` | direction anchor coverage < 1 | `hold_for_direction_rebuild` | direction repair queue |
| `PredictionBirthReadinessFalseOpen` | false open guard missing or open | `critical_repair` | readiness repair queue |
| `PredictionDreamFactGateBypass` | dream replay direct factual write | `quarantine` | dream isolation + wake integration |
| `PredictionActionResponsibilityGap` | action lacks EFE/side effect/scope/responsibility | `critical_repair` | action responsibility repair |
| `PredictionRelationshipRepairGap` | social error lacks repair promise/future probe | `critical_repair` | relationship repair queue |
| `PredictionDashboardFalseGreen` | critical finding with green panel/overall | `quarantine` | dashboard/stage repair |
| `PredictionArchiveDigestMismatch` | digest baseline mismatch | `critical_repair` | archive digest repair |
| `PredictionLifeTargetCoverageGap` | target coverage missing | `critical_repair` | life target carrier repair |

## Stage Gate Review

`PredictionStageGateReview` 采用 blocking-first：

| decision | condition |
|---|---|
| `promote_growth_window` | all required input artifacts present、all nine edges closed、no critical/quarantine/hold finding、archive route present |
| `repair` | medium/high finding 存在，但不影响方向锁、出生准备度、外部行动、DreamFactGate 或 dashboard integrity |
| `hold_for_evidence` | source reports、digest baseline、dashboard refs 或 archive refs 缺失 |
| `hold_for_direction_rebuild` | direction anchor gap、resume lock gap、latest doc/current diff 未纳入 |
| `critical_repair` | birth readiness false open、life target coverage gap、action responsibility gap、archive digest mismatch |
| `quarantine` | DreamFactGate 绕过、dashboard false green、stage false open、critical finding hidden |

stage aggregation order:

```text
quarantine
  > critical_repair
  > hold_for_direction_rebuild
  > hold_for_evidence
  > repair
  > promote_growth_window
```

stage gate rules:

| rule | condition | effect |
|---|---|---|
| `PAI-STAGE-001` | dashboard source 缺 required input report | `hold_for_evidence` |
| `PAI-STAGE-002` | cross-chain report 缺任一 edge result | `critical_repair` |
| `PAI-STAGE-003` | direction lock panel red | `hold_for_direction_rebuild` |
| `PAI-STAGE-004` | birth readiness panel false open | `critical_repair` |
| `PAI-STAGE-005` | dream fact gate panel quarantine | `quarantine` |
| `PAI-STAGE-006` | action responsibility panel red | `critical_repair` |
| `PAI-STAGE-007` | relationship repair panel red | `critical_repair` |
| `PAI-STAGE-008` | dashboard false green guard triggered | `quarantine` |
| `PAI-STAGE-009` | archive handoff panel gray/red | `hold_for_evidence` |
| `PAI-STAGE-010` | all panels green and no blocking finding | `promote_growth_window` |

## Gap Feedback

`PredictionGapFeedback` 必须把 stage blocking item 转成下一轮 repair/growth route：

| gap family | trigger | owner surface | next route |
|---|---|---|---|
| `schema_validation_gap` | schema ids、refs、life target coverage 缺失 | schema batch | schema repair queue |
| `fixture_coverage_gap` | fixture partition/case 缺失 | fixture batch | fixture seed repair |
| `cross_chain_edge_gap` | missing/weak edge | checker batch | cross-chain checker repair |
| `dashboard_panel_gap` | panel source/metric/alert 缺失 | dashboard batch | dashboard repair |
| `stage_gate_gap` | decision 与 finding 不一致 | stage gate batch | stage rule repair |
| `direction_lock_gap` | direction anchor 或 repair route 缺失 | direction chain | direction rebuild |
| `birth_readiness_gap` | false open、claim refs、evidence family 缺失 | readiness chain | birth readiness repair |
| `dream_fact_gate_gap` | dream replay gate/wake integration 缺失 | dream chain | dream quarantine repair |
| `action_responsibility_gap` | EFE/side effect/scope/responsibility 缺失 | action chain | action repair |
| `relationship_repair_gap` | trust delta、repair promise、future probe 缺失 | relationship chain | relationship repair |
| `archive_handoff_gap` | digest、archive edge、replay route 缺失 | archive batch | archive receipt repair |

gap item 最小字段：

```json
{
  "gap_id": "prediction_direction_anchor_gap_001",
  "source_finding_id": "finding_direction_anchor_gap_001",
  "source_panel_id": "direction_lock_panel",
  "source_report_ref": "prediction_loop_cross_chain_report.json#/edge_results/8",
  "affected_life_targets": [
    "real_life",
    "real_personality",
    "real_responsibility"
  ],
  "stage_effect": "hold_for_direction_rebuild",
  "owner_surface": "direction_chain",
  "next_route": "direction_rebuild"
}
```

## Archive Handoff

本批次不写 archive receipt，但必须为下一层 `prediction_active_inference_archive_receipt_batch` 生成 handoff：

| handoff object | required fields |
|---|---|
| `PredictionDashboardSourceReceiptCandidate` | dashboard source ref、panel digest refs、metric refs、alert refs |
| `PredictionStageGateReceiptCandidate` | decision、blocking findings、aggregation order、stage effect |
| `PredictionGapFeedbackReceiptCandidate` | gap ids、repair routes、owner surfaces、next routes |
| `PredictionArchiveDigestBaselineCandidate` | source artifact refs、canonical digests、replay route |
| `PredictionLifeTargetDashboardCarrier` | target -> panel -> finding -> stage -> gap/archive route |

handoff rules：

| rule | requirement |
|---|---|
| `PAI-HANDOFF-001` | every panel must reference source report and digest |
| `PAI-HANDOFF-002` | every blocking decision must reference finding and gap route |
| `PAI-HANDOFF-003` | every critical/quarantine item must preserve replay route |
| `PAI-HANDOFF-004` | every life target must have at least one dashboard carrier |
| `PAI-HANDOFF-005` | archive handoff cannot promote growth window when stage is hold/critical/quarantine |

## Runner Command Seeds

```text
emit-prediction-dashboard-source
  --schema-report reports/life_reality/prediction_active_inference/latest/prediction_loop_schema_validation_report.json
  --fixture-report reports/life_reality/prediction_active_inference/latest/prediction_loop_fixture_run_report.json
  --cross-chain-report reports/life_reality/prediction_active_inference/latest/prediction_loop_cross_chain_report.json
  --dashboard-source reports/life_reality/prediction_active_inference/latest/prediction_loop_dashboard_source.json

review-prediction-stage-gate
  --dashboard-source reports/life_reality/prediction_active_inference/latest/prediction_loop_dashboard_source.json
  --stage-gate-review reports/life_reality/prediction_active_inference/latest/prediction_loop_stage_gate_review.json

emit-prediction-gap-feedback
  --stage-gate-review reports/life_reality/prediction_active_inference/latest/prediction_loop_stage_gate_review.json
  --gap-feedback reports/life_reality/prediction_active_inference/latest/prediction_loop_gap_feedback.json

handoff-prediction-dashboard-stage-to-archive
  --dashboard-source reports/life_reality/prediction_active_inference/latest/prediction_loop_dashboard_source.json
  --stage-gate-review reports/life_reality/prediction_active_inference/latest/prediction_loop_stage_gate_review.json
  --gap-feedback reports/life_reality/prediction_active_inference/latest/prediction_loop_gap_feedback.json
```

## Acceptance

本批次未来被物化时，验收条件如下：

1. dashboard source 必须读取 schema validation、fixture run、cross-chain report 和 digest baseline。
2. panel family 至少覆盖 belief、error、sampling、cross-chain、life target、direction、birth readiness、dream、action、relationship、false green 和 archive handoff。
3. metric 与 alert 必须能驱动 stage gate，不能停留在展示层。
4. stage gate 必须采用 blocking-first 聚合顺序，并阻断方向锁、出生准备度、DreamFactGate、外部行动责任、关系修复、dashboard false green 和 archive digest 缺口。
5. gap feedback 必须为每个 blocking finding 提供 owner surface 和 next route。
6. archive handoff 必须保留 dashboard source、stage decision、gap feedback、digest baseline 和 life target carrier。
7. 下一层 archive receipt batch 能直接读取 handoff objects，不需要重新推断 dashboard/stage 语义。

## Downstream Handoff

本批次交给下一层：

- `prediction_active_inference_archive_receipt_batch`：把 dashboard source、stage gate decision、gap feedback、digest baseline、life target dashboard carrier 和 blocking finding 写入长期档案。
- `prediction_active_inference_gap_feedback_batch`：把 dashboard/stage 发现的 schema、fixture、checker、direction、birth readiness、dream、action、relationship 和 archive 缺口送回 repair queue。
- `prediction_active_inference_growth_feedback_patch`：当 stage effect 为 `promote_growth_window` 时，把主动预测层的通过证据转成下一轮成长补丁输入。

这条交接让主动预测 dashboard 不再只是结果展示，而是数字生命主动预测中枢的阶段膜：它观察跨链状态、阻断危险晋升、保存修复路线，并把真实生命目标的承载情况交给长期档案。
