# Prediction Membrane Action Engineering

本文档把感知、预测、候选行动、抑制、世界接触、责任后悔、逻辑比较和验证膜压成一条工程链。

## 这条链的标准流

```text
Observation / Language Percept / Body Signal
  -> PredictionWorkspaceFrame
  -> BeliefStateFrame
  -> PredictionErrorField
  -> ActiveSamplingPlan
  -> ActionCandidateArena
  -> GoNoGoPolicy
  -> ShadowActionGate
  -> WorldContactGate
  -> SideEffectReview
  -> ResponsibilityLoopState
  -> ObservationTruthFrame / BoundaryAuditTrace
  -> EvidenceRanking / CounterfactualEvaluation
  -> life_targets / repair / growth
```

## 当前最关键的下一轮文件

1. `life_v0/neural_core/signal_media.py`
2. `life_v0/neural_core/belief_state.py`
3. `life_v0/neural_core/prediction_error.py`
4. `life_v0/neural_core/active_sampling.py`
5. `life_v0/validators/cross_file_logic.py`
6. `life_v0/schema_runner/run_manifest.py`

## 当前最关键的 runtime 证据

1. `runtime/state/prediction/prediction_workspace_frame.json`
2. `runtime/state/membrane/life_membrane.json`
3. `runtime/state/action/action_candidate_arena.json`
4. `runtime/state/action/responsibility_loop_state.json`
5. `runtime/state/validation/observation_truth_frame.json`
6. `runtime/state/schema_runner/comparison_trace.json`

## 最低测试与新增测试

当前最低测试：

1. `tests/slices/test_neural_life_core.py`
2. `tests/slices/test_life_membrane.py`
3. `tests/slices/test_validation_membrane.py`
4. `tests/slices/test_schema_runner.py`

下一轮应新增：

1. `tests/slices/test_prediction_error_field.py`
2. `tests/slices/test_active_sampling_plan.py`
3. `tests/slices/test_cross_file_logic.py`
4. `tests/process/test_idle_strategy.py`
