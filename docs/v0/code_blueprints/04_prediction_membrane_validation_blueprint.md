# Prediction Membrane Validation Blueprint

这份蓝图处理另一条主体中轴：

```text
预测工作区
  -> 候选表达/候选行动
  -> 抑制与世界接触门
  -> 观察真值与反事实比较
  -> 责任与修复回写
```

## 主包边界

| 层 | 主包 | 作用 |
|---|---|---|
| 预测 | `life_v0/neural_core/` | 工作区、广播、网络切换、元认知、预测焦点 |
| 生命膜 | `life_v0/membrane/` | 候选、go/no-go、世界接触、side effect、责任回路、shadow gate |
| 验证 | `life_v0/validators/` | 观察 intake、truth review、boundary audit、quarantine |
| schema runner | `life_v0/schema_runner/` | consistency、counterfactual、comparison、evidence ranking |

## 当前固定对象

| 对象 | 首写位置 | 下游 |
|---|---|---|
| `PredictionWorkspaceFrame` | `neural_core/prediction_workspace.py` | `language/`、`membrane/`、`life_targets/` |
| `ActionCandidateSet` | `membrane/candidate_arena.py` | `go_nogo.py`、`validators/`、`schema_runner/` |
| `ResponsibilityLoopState` | `membrane/responsibility_loop.py` | `language/commitment_repair.py`、`schema_runner/` |
| `ObservationTruthReview` | `validators/__init__.py` | `schema_runner/consistency_logic.py` |
| `BoundaryAuditState` | `validators/boundary_audit.py` | `schema_runner/consistency_logic.py` |
| `CounterfactualTrace` | `schema_runner/counterfactual_eval.py` | `comparison_trace.py` |
| `ComparisonTrace` | `schema_runner/comparison_trace.py` | `evidence_ranker.py` |
| `EvidenceRanking` | `schema_runner/evidence_ranker.py` | report bundle / stage gate / future process policy |

## 当前已落文件

### neural core

1. `life_v0/neural_core/brain_graph.py`
2. `life_v0/neural_core/network_state.py`
3. `life_v0/neural_core/prediction_workspace.py`
4. `life_v0/neural_core/workspace.py`
5. `life_v0/neural_core/broadcast.py`
6. `life_v0/neural_core/metacognition.py`

### membrane

1. `life_v0/membrane/candidate_arena.py`
2. `life_v0/membrane/go_nogo.py`
3. `life_v0/membrane/world_contact_gate.py`
4. `life_v0/membrane/side_effect_review.py`
5. `life_v0/membrane/responsibility_loop.py`
6. `life_v0/membrane/shadow_gate.py`

### validators

1. `life_v0/validators/observation_validator.py`
2. `life_v0/validators/boundary_audit.py`
3. `life_v0/validators/__init__.py`

### schema runner

1. `life_v0/schema_runner/consistency_logic.py`
2. `life_v0/schema_runner/counterfactual_eval.py`
3. `life_v0/schema_runner/comparison_trace.py`
4. `life_v0/schema_runner/evidence_ranker.py`
5. `life_v0/schema_runner/__init__.py`

## 当前 runtime 承载

### 预测与行动

1. `runtime/state/prediction/prediction_workspace_frame.json`
2. `runtime/state/action/action_candidate_set.json`
3. `runtime/state/action/go_nogo_state.json`
4. `runtime/state/action/world_contact_gate_state.json`
5. `runtime/state/action/side_effect_review.json`
6. `runtime/state/action/responsibility_loop_state.json`

### 生命膜

1. `runtime/state/membrane/life_membrane.json`
2. `runtime/state/membrane/membrane_gate_decision.json`
3. `runtime/state/membrane/dream_fact_boundary.json`
4. `runtime/state/membrane/responsibility_repair_boundary.json`
5. `runtime/state/membrane/shadow_action_gate.json`
6. `runtime/state/membrane/birth_readiness_precheck.json`

### 验证与 schema runner

1. `runtime/state/validation/runtime_observation_intake.json`
2. `runtime/state/validation/validator_rule_index.json`
3. `runtime/state/validation/quarantine_packet_index.json`
4. `runtime/state/validation/dashboard_metric_source.json`
5. `runtime/state/validation/cross_file_finding_index.json`
6. `runtime/state/validation/observation_truth_review.json`
7. `runtime/state/validation/boundary_audit_state.json`
8. `runtime/state/validation/validation_stage_gate.json`
9. `runtime/state/schema_runner/schema_registry.json`
10. `runtime/state/schema_runner/schema_dependency_lockfile.json`
11. `runtime/state/schema_runner/runner_command_queue.json`
12. `runtime/state/schema_runner/cross_file_checker_manifest.json`
13. `runtime/state/schema_runner/first_code_artifact_manifest.json`
14. `runtime/state/schema_runner/consistency_logic.json`
15. `runtime/state/schema_runner/counterfactual_trace.json`
16. `runtime/state/schema_runner/comparison_trace.json`
17. `runtime/state/schema_runner/evidence_ranking.json`
18. `runtime/state/schema_runner/schema_runner_stage_gate.json`

## 下一轮关键文件

### 必须新增

1. `life_v0/schema_runner/cross_file_logic.py`
2. `life_v0/schema_runner/run_manifest.py`

### 必须补厚

1. `life_v0/membrane/responsibility_loop.py`

## 文件级职责

| 文件 | 主要职责 | 必须写出 |
|---|---|---|
| `cross_file_logic.py` | 把 validation / membrane / language / growth 的跨文件发现收束成统一逻辑索引 | `runtime/state/schema_runner/cross_file_logic.json` |
| `run_manifest.py` | 把 schema runner 本轮依赖、命令序列、输入哈希和输出物收束成运行 manifest | `runtime/state/schema_runner/run_manifest.json` |
| `responsibility_loop.py` | 把 side effect、关系后果、痛苦/后悔压力、修复义务和成长触发连成稳定闭环 | `runtime/state/action/responsibility_loop_state.json` 的更厚版本 |

## 最低验证面

1. `tests/slices/test_life_membrane.py`
2. `tests/slices/test_shadow_gate.py`
3. `tests/slices/test_validation_membrane.py`
4. `tests/slices/test_schema_runner.py`
5. `tests/slices/test_evidence_ranker.py`

## 完成定义

这条中轴完成，不是“有验证文件”就算完成，而要满足：

1. 预测工作区真实影响语言与行动候选。
2. world contact 和 side effect 真实进入责任回路。
3. 责任回路真实反推 regret / repair / growth。
4. schema runner 真实能比较实际路径与反事实路径。
5. 证据排序真实决定下一轮修复和观察优先级。

