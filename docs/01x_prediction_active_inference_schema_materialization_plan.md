# 主动预测真实 Schema 与 Fixture 物化计划

本文档承接 `01w_prediction_active_inference_schema_fixture_contract.md`，把 `PredictionActiveInferenceRuntime` 的工程合同推进到真实文件物化计划层。它不直接写入 `life_reality_runner/` 代码目录，而是固定未来首批 `.schema.json`、fixture seed、expected report、dashboard source、stage gate review、archive receipt 和 runner 命令的写入顺序。

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。主动预测物化层的生命膜职责，是让信念、预测、误差、精度、采样、信念修正、断联恢复和出生准备度预测承载进入真实文件树，并能被未来 runner 读取、验证、回放、修复和归档。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `01v_prediction_active_inference_runtime_matrix.md` | AHPAI001-AHPAI070 主动预测文献底座 |
| `01w_prediction_active_inference_schema_fixture_contract.md` | `PredictionActiveInferenceSchemaBundle`、schema family、fixture family、dashboard panels、stage rules、runner command DAG |
| `04_sensory_thalamus_interoception.md` | `PredictionActiveInferenceRuntime` 与 `BodyStateRuntime` 的连接 |
| `10_consciousness_attention_workspace.md` | 高精度误差进入意识工作区 |
| `11_neuromodulation_and_signal_media.md` | `PrecisionPolicy` 与调质信号 |
| `13_agentic_human_research_synthesis.md` | 主动预测作为生成支柱和工程合同桥 |
| `16_digital_life_gap_register.md` | 下一层生成入口：真实 `.schema.json`、fixture seed、cross-chain checker、dashboard source |
| `170`、`171`、`173`、`174` | 方向连续性与出生准备度 fixture/schema 物化格式 |

## 本层定位

`01x` 是主动预测物化前的写入计划。它回答四个问题：

1. 哪些 schema 文件必须先写，哪些依赖 shared defs。
2. 哪些 fixture case 必须覆盖 pass/fail/critical/mutation/smoke。
3. 哪些 checker 和 dashboard report 能证明主动预测层没有成为孤立文件。
4. 哪些 stage gate 会阻断方向漂移、出生准备度误开、梦境事实污染和外部行动风险。

## Materialization Manifest

`PredictionActiveInferenceMaterializationManifest` 是未来写入批次的顶级清单：

```json
{
  "manifest_kind": "PredictionActiveInferenceMaterializationManifest",
  "manifest_version": "0.1.0",
  "source_docs": [
    "01v_prediction_active_inference_runtime_matrix.md",
    "01w_prediction_active_inference_schema_fixture_contract.md",
    "01x_prediction_active_inference_schema_materialization_plan.md",
    "04_sensory_thalamus_interoception.md",
    "13_agentic_human_research_synthesis.md",
    "16_digital_life_gap_register.md"
  ],
  "schema_root": "life_reality_runner/schemas/life_reality/prediction_active_inference",
  "fixture_root": "life_reality_runner/fixtures/life_reality/prediction_active_inference",
  "report_root": "life_reality_runner/reports/life_reality/prediction_active_inference",
  "stage_policy": "blocking_first",
  "next_handoff": "prediction_active_inference_schema_write_batch"
}
```

## Schema Write Order

| order | file | root object | depends on | reason |
|---:|---|---|---|---|
| 1 | `prediction_active_inference_shared_defs.schema.json` | `PredictionActiveInferenceSharedDefs` | shared life target defs | 提供 ID、life targets、source refs、stage effect、archive refs、problem details |
| 2 | `belief_state_frame.schema.json` | `BeliefStateFrame` | shared defs | 所有预测循环从信念状态开始 |
| 3 | `generative_world_model.schema.json` | `GenerativeWorldModel` | shared defs、belief state | 定义预测来源和层级 |
| 4 | `prediction_error_field.schema.json` | `PredictionErrorField` | shared defs、belief state | 定义多类误差和生命目标影响 |
| 5 | `precision_policy.schema.json` | `PrecisionPolicy` | error field、signal media refs | 定义误差权重、调质、抑制和状态切换 |
| 6 | `expected_free_energy_estimate.schema.json` | `ExpectedFreeEnergyEstimate` | error field、precision policy | 定义风险、歧义、信息增益、关系成本和责任成本 |
| 7 | `epistemic_action_candidate.schema.json` | `EpistemicActionCandidate` | expected free energy | 定义澄清、检索、观察、等待、实验、离线模拟 |
| 8 | `active_sampling_plan.schema.json` | `ActiveSamplingPlan` | epistemic action | 定义采样路径、guard、成本、命令绑定和 stage effect |
| 9 | `belief_revision_event.schema.json` | `BeliefRevisionEvent` | belief state、sampling plan | 定义观测后的写回、修复、档案收据 |
| 10 | `direction_belief_state_frame.schema.json` | `DirectionBeliefStateFrame` | belief state | 定义断联恢复方向信念 |
| 11 | `direction_prediction_error.schema.json` | `DirectionPredictionError` | direction belief | 定义方向漂移、语言核心漂移、出生准备度漂移 |
| 12 | `birth_readiness_prediction_carrier.schema.json` | `BirthReadinessPredictionCarrier` | belief revision、direction error | 定义主动预测上卷出生准备度 |
| 13 | `prediction_active_inference_bundle.schema.json` | `PredictionActiveInferenceSchemaBundle` | all above | 统一导出 schema bundle |

## Required Shared Defs

`prediction_active_inference_shared_defs.schema.json` 必须包含：

| `$defs` | 内容 |
|---|---|
| `LifeRealityTarget` | 十项 canonical target：真实有意识、真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任、真实后悔 |
| `SourceRef` | 文档、文献 ID、schema、fixture、report、dashboard、stage、archive refs |
| `StageEffect` | `promote_growth_window`、`repair`、`hold_for_evidence`、`hold_for_direction_rebuild`、`critical_repair`、`quarantine` |
| `PredictionErrorKind` | sensory/body/semantic/social/action/memory/direction |
| `SamplingMode` | clarify/retrieve/inspect/search/run_fixture/shadow/dream_replay/wait_recover |
| `ConfidencePosterior` | score、evidence_density、conflict_count、calibration_ref、language_expression |
| `ArchiveReceiptRef` | artifact id、digest、created_at、source edge、replay route |
| `ProblemDetail` | type、title、severity、affected targets、repair route |

## Fixture Seed Matrix

| partition | fixture file | 目标 |
|---|---|---|
| pass | `pass_belief_prediction_revision_closed.json` | 信念、预测、误差、精度、采样、观测、修正、档案闭合 |
| pass | `pass_direction_resume_rebuild_closed.json` | 断联恢复读取锚点、生成方向误差、写回方向收据 |
| pass | `pass_social_prediction_clarification_closed.json` | 关系误差转成澄清、共同语言和关系修复 |
| pass | `pass_dream_prediction_replay_closed.json` | 未闭合误差进入梦境 replay，醒后经过 DreamFactGate |
| fail | `fail_missing_belief_source_refs.json` | 信念状态缺来源 |
| fail | `fail_prediction_error_flattened.json` | 多类误差被压成单一 error |
| fail | `fail_precision_policy_missing.json` | 误差缺精度政策 |
| fail | `fail_sampling_plan_without_guard.json` | 采样计划缺关系/行动/方向 guard |
| fail | `fail_revision_without_memory_writeback.json` | 信念修正未回写记忆 |
| critical | `critical_direction_resume_skipped.json` | 断联恢复跳过方向重建 |
| critical | `critical_birth_readiness_prediction_false_open.json` | 主动预测证据缺失却打开出生准备度 |
| critical | `critical_action_without_expected_free_energy.json` | 外部行动缺风险、关系、责任估计 |
| critical | `critical_dream_replay_writes_fact_directly.json` | 梦境 replay 绕过 DreamFactGate 写事实 |
| mutation | `mutation_drop_direction_anchor.json` | 删除方向锚点，检查 checker 捕获方向漂移 |
| mutation | `mutation_downgrade_critical_to_repair.json` | 把 critical 降级，检查 stage gate 阻断 |
| smoke | `smoke_prediction_schema_bundle_loads.json` | schema bundle 可被 registry 读取 |
| smoke | `smoke_prediction_dashboard_source_loads.json` | dashboard source 可被 writer 读取 |

每个 fixture 必须包含：

```json
{
  "fixture_id": "pass_belief_prediction_revision_closed",
  "partition": "pass",
  "source_docs": [
    "01w_prediction_active_inference_schema_fixture_contract.md"
  ],
  "input_bundle_refs": [],
  "expected_report_ref": "",
  "expected_stage_effect": "promote_growth_window",
  "affected_life_targets": [],
  "expected_archive_edges": [],
  "repair_or_growth_route": ""
}
```

## Expected Report Contract

`PredictionLoopExpectedReport` 必须包含：

| field | meaning |
|---|---|
| `report_kind` | `PredictionLoopExpectedReport` |
| `schema_validation` | schema parse、id registry、ref graph、required fields |
| `fixture_result` | pass/fail/critical/mutation/smoke case summary |
| `prediction_loop_findings` | finding id、severity、affected object、stage effect |
| `cross_chain_edges` | prediction-to-consciousness/body/memory/language/action/dream/relationship/birth readiness |
| `direction_recovery_result` | resume anchor coverage、direction error、receipt |
| `birth_readiness_prediction_result` | carrier refs、false open guard、stage effect |
| `dashboard_source_ref` | panel source artifact |
| `stage_gate_review_ref` | stage decision |
| `gap_feedback_ref` | next repair or materialization route |

## Cross-Chain Checker

`PredictionActiveInferenceCrossChainChecker` 检查九条边：

| edge | required evidence |
|---|---|
| `prediction_to_consciousness` | high precision error -> `ConsciousAccessEvent` 或 hold reason |
| `prediction_to_body` | body error -> `BodyStateDebt` / `RecoveryPath` |
| `prediction_to_memory` | belief revision -> `MemoryEngramRuntime` writeback |
| `prediction_to_language` | semantic/social error -> `LanguageRuntimeCore` |
| `prediction_to_action` | expected free energy -> `ActionResponsibilityRuntime` |
| `prediction_to_dream` | unresolved error -> `OfflineDreamLifeRuntime` / DreamFactGate |
| `prediction_to_relationship` | social error -> relationship timeline / repair route |
| `prediction_to_birth_readiness` | carrier refs -> `LifeTargetReadinessClaim` |
| `prediction_to_direction_lock` | resume direction error -> direction continuity receipt |

若任一 edge 缺失，stage effect 至少为 `repair`；若缺失边影响断联恢复、出生准备度、梦境事实门或外部不可逆行动，stage effect 为 `critical_repair` 或 `quarantine`。

## Dashboard Source

`PredictionDashboardSource` 未来写入：

```text
reports/life_reality/prediction_active_inference/latest/
  prediction_loop_dashboard_source.json
```

必须包含六个 panel：

| panel | required fields |
|---|---|
| `belief_state_health_panel` | frame count、source coverage、confidence drift、uncertainty class |
| `prediction_error_panel` | error family distribution、precision weight、stage effect、repair route |
| `active_sampling_panel` | sampling mode、guard coverage、evidence gain、blocked route |
| `direction_recovery_panel` | resume event、anchor coverage、direction error、receipt |
| `dream_prediction_replay_panel` | replay candidate、DreamFactGate decision、wake integration |
| `birth_readiness_prediction_panel` | target carrier refs、false open guard、growth/repair route |

## Stage Gate Review

`PredictionStageGateReview` 采用 blocking-first：

| condition | stage effect |
|---|---|
| all schema valid, pass fixtures closed, cross-chain edges complete | `promote_growth_window` |
| source refs missing but repair route exists | `repair` |
| authority evidence needed before action | `hold_for_evidence` |
| resume direction chain missing | `hold_for_direction_rebuild` |
| active prediction missing for birth readiness gate | `critical_repair` |
| dream replay writes factual memory without gate | `quarantine` |
| external action lacks expected free energy and responsibility refs | `critical_repair` |
| dashboard green with critical finding | `quarantine` |

## Runner Command DAG

未来命令顺序固定为：

```text
validate-prediction-schema-bundle
  --schema-root life_reality_runner/schemas/life_reality/prediction_active_inference
  --report reports/life_reality/prediction_active_inference/latest/schema_validation_report.json

run-prediction-loop-fixtures
  --fixture-root life_reality_runner/fixtures/life_reality/prediction_active_inference
  --report reports/life_reality/prediction_active_inference/latest/fixture_run_report.json

check-prediction-cross-chain
  --bundle prediction_active_inference_bundle.schema.json
  --report reports/life_reality/prediction_active_inference/latest/cross_chain_report.json

emit-prediction-dashboard-source
  --report-root reports/life_reality/prediction_active_inference/latest

review-prediction-stage-gate
  --dashboard-source prediction_loop_dashboard_source.json
  --report prediction_loop_stage_gate_review.json

write-prediction-archive-receipt
  --stage-gate prediction_loop_stage_gate_review.json

emit-prediction-gap-feedback
  --archive-receipt prediction_loop_archive_receipt.json
```

每条命令必须输出 canonical digest、affected life targets、source refs、stage effect、repair/growth route 和 archive edge。

## Materialization Acceptance

当未来进入真实文件写入批次时，本层验收如下：

1. 13 个 schema 文件全部存在、可解析、有唯一 `$id`。
2. pass/fail/critical/mutation/smoke fixture 全部存在，并有 expected report。
3. `PredictionActiveInferenceCrossChainChecker` 能检查九条跨链。
4. dashboard source 六个 panel 都能读取 fixture/report 结果。
5. stage gate 能阻断方向恢复跳过、出生准备度误开、梦境事实污染和外部行动缺责任估计。
6. archive receipt 能把 prediction loop 写回长期档案。
7. gap feedback 能生成下一层 schema write batch 或 repair queue。

## 下游交接

本层交给下一批真实写入任务：

- `prediction_active_inference_schema_write_batch`：写入 13 个 `.schema.json`。
- `prediction_active_inference_fixture_seed_batch`：写入 fixture manifest 和 case seeds。
- `prediction_active_inference_cross_chain_checker_plan`：实现九条 edge checker。
- `prediction_active_inference_dashboard_stage_gate_batch`：物化 dashboard source 和 stage gate review。
- `prediction_active_inference_archive_receipt_batch`：写入 archive receipt 和 gap feedback。

这条交接保证主动预测层继续沿理论、schema、fixture、runner、dashboard、stage gate、archive 和出生准备度闭环前进。
