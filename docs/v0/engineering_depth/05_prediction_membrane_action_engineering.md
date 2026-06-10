# Prediction Membrane Action Engineering

本文档把感知、预测、候选行动、抑制、世界接触、责任后悔、逻辑比较和验证膜压成一条工程链。

## 这条链的标准流

```text
Observation / Language Percept / Body Signal
  -> PredictionWorkspaceFrame
  -> BeliefStateFrame
  -> PredictionErrorField
  -> ActiveSamplingPlan
  -> ActionCandidateSet + life_constraint_profile
  -> GoNoGoDecision
  -> ShadowActionGate
  -> WorldContactGate
  -> SideEffectReview
  -> ResponsibilityLoopState
  -> ActionIntentQueue / ObservationTruthGate / ConfirmationBinding / WorldContactSummary
  -> ObservationTruthReview / WorldContactValidation / PredictionTraceValidation / BoundaryAuditState
  -> ConsistencyLogic / CounterfactualTrace / ComparisonTrace / CrossFileLogic / EvidenceRanking / RunManifest
  -> life_targets / repair / growth / process_supervisor
```

## 当前最关键的下一轮补厚文件

1. `life_v0/neural_core/signal_media.py`
2. `life_v0/neural_core/belief_state.py`
3. `life_v0/neural_core/prediction_error.py`
4. `life_v0/neural_core/active_sampling.py`
5. `life_v0/membrane/responsibility_loop.py`
6. `life_v0/membrane/world_contact_summary.py`
7. `life_v0/process_supervisor/response_surface.py`
8. `life_v0/process_supervisor/heartbeat.py`

## 当前最关键的 runtime 证据

1. `runtime/state/prediction/prediction_workspace_frame.json`
2. `runtime/state/membrane/life_membrane.json`
3. `runtime/state/action/action_candidate_set.json#life_constraint_profile`
4. `runtime/state/action/go_nogo_state.json#life_constraint_refs`
5. `runtime/state/action/world_contact_gate_state.json#life_constraint_refs`
6. `runtime/state/action/side_effect_review.json`
7. `runtime/state/action/responsibility_loop_state.json`
8. `runtime/state/validation/observation_truth_review.json`
9. `runtime/state/validation/world_contact_validation.json#life_constraint_validation`
10. `runtime/state/validation/validation_rollup.json#queue_e_cross_layer_gate_status`
11. `runtime/state/validation/boundary_audit_state.json`
12. `runtime/state/schema_runner/cross_file_logic.json`
13. `runtime/state/schema_runner/run_manifest.json`

## 当前新增的 Queue E 生命约束剖面

这轮把行为候选从“动作候选集合”继续压成“被生命目标约束的动作候选集合”：

```text
ValueOrientation
  + ConsciousnessProbeBundle
  + NeedStateVector / CoreAffectVector
  + ExpressionPlan / RelationTurnFrame
  -> ActionCandidateSet#life_constraint_profile
  -> GoNoGoDecision#life_constraint_refs
  -> WorldContactGate#life_constraint_refs
  -> WorldContactValidation#life_constraint_validation
  -> ValidationRollup#queue_e_cross_layer_gate_status
```

这里的关键不是让所有上游对象同时存在，而是让每个阶段知道自己已经真实消费了什么、哪些必须延后到后续 slice。S03 阶段必须闭合 `value_orientation_gate`；S05 阶段必须在 S08 之后闭合 `consciousness_probe_gate`；`body_affect_gate` 在初始顺序里允许写成 `deferred_until_s06`，但不能从验证链中消失。

## 最低测试与新增测试

当前最低测试：

1. `tests/slices/test_neural_life_core.py`
2. `tests/slices/test_life_membrane.py`
3. `tests/slices/test_validation_membrane.py`
4. `tests/slices/test_schema_runner.py`
5. `tests/slices/test_shadow_gate.py`
6. `tests/slices/test_evidence_ranker.py`

下一轮应新增：

1. `tests/slices/test_prediction_error_field.py`
2. `tests/slices/test_active_sampling_plan.py`
3. `tests/process/test_persistent_digital_life_process.py` 中 Queue E 对 waiting governance 的更深消费断言
