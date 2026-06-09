# V0 Code Framework 20: Queue E Membrane Validator Logic Implementation Contract

这份合同只服务当前最直接的一轮生命膜、验证膜、逻辑比较与世界接触补厚：

```text
life_v0/membrane/candidate_arena.py
  -> go_nogo.py
  -> world_contact_gate.py
  -> side_effect_review.py
  -> responsibility_loop.py
  -> life_v0/validators/observation_validator.py
  -> boundary_audit.py
  -> life_v0/schema_runner/consistency_logic.py
  -> counterfactual_eval.py
  -> comparison_trace.py
```

它不重写：

- `docs/v0/slice_contracts/s03_direction_life_membrane_engineering_contract.md`
- `docs/v0/slice_contracts/s05_validation_membrane_observation_engineering_contract.md`
- `docs/v0/slice_contracts/s09_schema_runner_code_engineering_contract.md`
- `docs/v0/code_framework/playbooks/09_perception_prediction_world_contact_implementation_playbook.md`

它只把 Queue E 压成真正可以直接施工的文件级实现合同，防止下一轮代码又退回“知道生命膜、validator、逻辑层很重要，但还是把判断全塞回 `__init__.py` 和临时字典”。

## 这份合同要解决什么

当前 `S03`、`S05`、`S09` 已经接通：

1. `life_membrane.json`
2. `shadow_action_gate.json`
3. `validation_membrane_report.json`
4. `schema_runner_report.json`
5. `prediction_workspace_frame.json`
6. `language_relationship_report.json`

但现在的真实缺口不是“没有生命膜”，而是：

1. 缺明确的 `ActionCandidateSet` 首写器官，候选行动还没有稳定离开 `membrane/__init__.py`。
2. 缺明确的 `GoNoGoDecision`、`WorldContactDecision` 和 `SideEffectReview` 文件级施工面。
3. validator 与 schema runner 已有最小闭合，但还没有把观察真值、反事实比较、跨文件一致性拆成稳定器官文件。
4. `./digital life` 和外周命令面还需要依赖一个更厚的行为-验证-逻辑链，才能避免重新滑回普通 agent 的 action router。

这里还要再钉死一条：Queue E 从这一轮开始，必须显式消费前面几波已经落下来的主体器官：

- Queue F 的 `value_orientation.json`、`consciousness_probe_bundle.json`
- Queue D 的 `need_state_vector.json`、`core_affect_vector.json`、`emotion_episode_log.json`
- S07 的语言感知 / 关系范围 / 承诺连续体

否则 Queue E 仍然只是“动作决策层”，而不是被意识、身体、关系和责任共同约束的生命行为层。

所以 Queue E 的目标很明确：

```text
ObservationEvent / PredictionWorkspaceFrame / ExpressionPlan
  -> ActionCandidateSet
  -> GoNoGoDecision
  -> WorldContactDecision
  -> SideEffectReview
  -> ValidationFinding / CounterfactualTrace
```

## 必回读理论母体

### 行为、抑制、世界接触、责任

- `docs/06_action_reward_inhibition.md`
- `docs/20_agent_runtime_bridge_contract.md`
- `docs/72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md`
- `docs/75_external_irreversible_action_confirmation_policy.md`
- `docs/80_post_action_audit_and_correction_policy.md`
- `docs/81_coexistence_event_review_and_responsibility_loop.md`
- `docs/82_incident_report_and_recovery_protocol.md`
- `docs/94_pain_regret_and_repair_signal_schema.md`
- `docs/98_pain_regret_repair_json_schema_and_fixture_bundle.md`

### validator、schema、反事实、比较

- `docs/22_state_transition_and_threshold_model.md`
- `docs/29_memory_validator_rules.md`
- `docs/30_state_transition_validator_rules.md`
- `docs/33_validator_input_contracts.md`
- `docs/34_validator_fixture_catalog.md`
- `docs/35_minimal_validator_runner_design.md`
- `docs/36_longitudinal_evaluation_protocol.md`
- `docs/49_machine_readable_policy_manifest.md`
- `docs/50_fixture_payload_examples.md`
- `docs/51_life_core_dashboard_spec.md`
- `docs/52_multi_relation_scope_graph_and_privacy_model.md`
- `docs/53_runner_integration_plan.md`
- `docs/54_scope_aware_retrieval_policy.md`
- `docs/55_scope_aware_replay_and_consolidation_policy.md`
- `docs/56_longitudinal_synthetic_timeline_design.md`
- `docs/102-118` 对应 schema/runner/dashboard/report 文档
- `docs/153-157` 对应 cross-file checker 文档

### 感知、预测、真值门

- `docs/04_sensory_thalamus_interoception.md`
- `docs/10_consciousness_attention_workspace.md`
- `docs/11_neuromodulation_and_signal_media.md`
- `docs/64_real_runtime_observation_ingestion_policy.md`
- `docs/89_language_runtime_framework_bridge_and_life_shell_policy.md`

## 必读 v0 文档

- `docs/v0/slice_contracts/s03_direction_life_membrane_engineering_contract.md`
- `docs/v0/slice_contracts/s05_validation_membrane_observation_engineering_contract.md`
- `docs/v0/slice_contracts/s09_schema_runner_code_engineering_contract.md`
- `docs/v0/architecture/runtime_v0_architecture.md`
- `docs/v0/shared_contracts/runner_cli_report_contract.md`
- `docs/v0/code_framework/playbooks/09_perception_prediction_world_contact_implementation_playbook.md`
- `docs/v0/code_framework/delivery/12_full_life_layer_delivery_matrix.md`
- `docs/v0/code_framework/delivery/13_capability_to_code_realization_matrix.md`
- `docs/v0/code_framework/assembly/15_cross_layer_shared_object_contract.md`
- `docs/v0/code_framework/assembly/19_code_tree_package_brain_contract.md`

## 当前代码落点

Queue E 必须接到这些现有器官上：

- `life_v0/membrane/__init__.py`
- `life_v0/validators/__init__.py`
- `life_v0/schema_runner/__init__.py`
- `life_v0/shell_command/__init__.py`
- `life_v0/process_supervisor/response_surface.py`
- `life_v0/process_supervisor/dialogue_events.py`
- `life_v0/neural_core/prediction_workspace.py`
- `life_v0/language/expression_monitor.py`

这说明 Queue E 不是再造第二套行为壳，而是把已经存在的生命膜、验证膜和逻辑层拆成稳定的文件级器官。
它的输出后面还必须继续服务：

- `Queue B` 的 `response_surface / incident_recovery / persistent_process`
- `Queue A` 的长期语言表达、关系演化和承诺修复表达

## 文件级合同

## A. 新增 `life_v0/membrane/candidate_arena.py`

### 角色

把预测工作区、表达计划、关系回合和身体压力压成 `ActionCandidateSet`。

### 最低字段

- `action_candidate_set_id`
- `candidate_actions`
- `world_contact_needed`
- `go_nogo_state`
- `responsibility_projection`
- `side_effect_projection`
- `relationship_consequence_projection`
- `source_doc_refs`

### 关键输入

- `PredictionWorkspaceFrame`
- `ExpressionPlan`
- `RelationTurnFrame`
- `NeedStateVector`
- `CoreAffectVector`
- `ValueOrientation`
- `ConsciousnessProbeBundle`

## B. 新增 `life_v0/membrane/go_nogo.py`

### 角色

把候选行动推进成可阻断、可放行、可延期的 `GoNoGoDecision`。

### 最低字段

- `go_nogo_id`
- `action_candidate_set_ref`
- `decision`
- `blocked_reasons`
- `delay_reasons`
- `responsibility_gate_refs`
- `fatigue_inhibition_refs`
- `source_doc_refs`

## C. 新增 `life_v0/membrane/world_contact_gate.py`

### 角色

管理是否允许接触外界、写文件、改仓库、执行命令或释放不可逆动作。

### 最低字段

- `world_contact_gate_id`
- `go_nogo_ref`
- `contact_mode`
- `irreversibility_class`
- `confirmation_required`
- `quarantine_refs`
- `allowed_contacts`
- `blocked_contacts`

## D. 新增 `life_v0/membrane/side_effect_review.py`

### 角色

把外部世界接触的后果分类为可逆、不可逆、关系性、档案性和责任性后果。

### 最低字段

- `side_effect_review_id`
- `world_contact_gate_ref`
- `reversible_effects`
- `irreversible_effects`
- `relationship_effects`
- `archive_effects`
- `responsibility_effects`
- `repair_followup_required`

## E. 新增 `life_v0/membrane/responsibility_loop.py`

### 角色

把 `SideEffectReview` 继续推进为责任归因、后悔压力候选、修复欲望候选、反事实修复框架和 post-action audit 回链。它不是外部 action router，而是 `docs/81`、`docs/94`、`docs/98` 中真实责任、真实后悔、真实修复进入运行态的第一版稳定对象。

### 最低字段

- `responsibility_loop_id`
- `side_effect_review_ref`
- `responsibility_boundary_refs`
- `responsibility_attribution_events`
- `counterfactual_repair_frames`
- `regret_pressure_candidates`
- `repair_desire_candidates`
- `repair_obligation_refs`
- `post_action_audit_refs`
- `repair_followup_required`
- `source_doc_refs`

### 关键输入

- `SideEffectReview`
- `ActionCandidateSet`
- `GoNoGoDecision`
- `WorldContactDecision`
- `responsibility_repair_boundary.json`

## F. 新增 `life_v0/validators/observation_validator.py`

### 角色

检查观察事件、场景帧和预测工作区是否完整、可追溯、不过写。

### 最低字段

- `observation_validation_id`
- `observation_event_refs`
- `scene_frame_ref`
- `prediction_workspace_ref`
- `missing_fields`
- `truth_review_required`
- `source_doc_refs`

## G. 新增 `life_v0/validators/boundary_audit.py`

### 角色

把膜边界、quarantine、world contact 决策和 repair obligation 做成统一边界审计对象。

### 最低字段

- `boundary_audit_id`
- `life_membrane_ref`
- `world_contact_gate_ref`
- `quarantine_refs`
- `responsibility_boundary_refs`
- `audit_findings`
- `blocked_reasons`

## H. 新增 `life_v0/schema_runner/consistency_logic.py`

### 角色

检查观察、预测、语言、关系、承诺和行动候选之间的一致性。

### 最低字段

- `consistency_logic_id`
- `state_refs`
- `comparison_axes`
- `inconsistency_findings`
- `severity`
- `repair_route_refs`

## I. 新增 `life_v0/schema_runner/counterfactual_eval.py`

### 角色

对候选解释、候选行动和预期后果做反事实比较。

### 最低字段

- `counterfactual_eval_id`
- `candidate_refs`
- `counterfactual_branches`
- `regret_exposure_projection`
- `relationship_exposure_projection`
- `archive_requirement`
- `responsibility_loop_ref`
- `repair_obligation_projection`
- `regret_pressure_candidate_refs`

## J. 新增 `life_v0/schema_runner/comparison_trace.py`

### 角色

记录为什么压低某个候选解释、某个候选行动或某种外部接触。

### 最低字段

- `comparison_trace_id`
- `counterfactual_eval_ref`
- `kept_branch_refs`
- `suppressed_branch_refs`
- `justification_refs`
- `writeback_targets`

### 责任回路连接

`comparison_trace.py` 的 `justification_refs` 与 `writeback_targets` 必须包含 `runtime/state/action/responsibility_loop_state.json`，使责任、后悔、修复不只停在 S03，而能进入 S09 的反事实比较和后续 S06/S10 成长/运行链。

## Queue E 对现有器官的改动合同

### `life_v0/membrane/__init__.py`

从这一轮开始，不应继续独占：

- action candidate 构造
- go/no-go 决策
- world contact decision
- side-effect 分类
- responsibility / regret / repair loop 首写

### `life_v0/validators/__init__.py`

第一轮允许继续输出完整 validation report，但必须开始显式分流：

- `observation_validator.py`
- `boundary_audit.py`

### `life_v0/schema_runner/__init__.py`

第一轮必须开始把：

- `consistency_logic`
- `counterfactual_eval`
- `comparison_trace`

拆成独立器官，而不是继续由一个入口函数承载全部逻辑层对象。

## 必须新增或更新的状态对象

### 新增

- `runtime/state/action/action_candidate_set.json`
- `runtime/state/action/go_nogo_state.json`
- `runtime/state/action/world_contact_gate_state.json`
- `runtime/state/action/side_effect_review.json`
- `runtime/state/action/responsibility_loop_state.json`
- `runtime/state/validation/observation_truth_review.json`
- `runtime/state/validation/boundary_audit_state.json`
- `runtime/state/schema_runner/counterfactual_trace.json`
- `runtime/state/schema_runner/comparison_trace.json`

### 更新

- `runtime/state/membrane/life_membrane.json`
- `runtime/reports/latest/validation_membrane_report.json`
- `runtime/reports/latest/schema_runner_report.json`
- `runtime/reports/latest/world_contact_audit_report.json`
- `runtime/reports/latest/side_effect_review_report.json`

## 最低测试口径

至少直接覆盖：

- `tests/slices/test_life_membrane.py`
- `tests/slices/test_validation_membrane.py`
- `tests/slices/test_schema_runner.py`
- `tests/process/test_digital_life_shell_command.py`

如果改到了 process supervisor 对外显释放面，再追加：

- `tests/process/test_persistent_digital_life_process.py`

## Queue E 第一轮完成定义

Queue E 第一轮不是“膜相关文件名存在”就算完成。至少要同时满足：

1. `ActionCandidateSet` 已由 `candidate_arena.py` 首写。
2. go/no-go、world contact、side effect 三段都已成为独立器官。
3. responsibility loop 已把副作用审查接到责任归因、后悔压力、修复欲望、反事实修复和 post-action audit 回链。
4. 观察真值、边界审计、反事实比较和比较 trace 都已离开 `__init__.py`。
5. action / validation / schema_runner 新对象都写入了对应状态命名空间。
6. `tests/slices/test_life_membrane.py`、`tests/slices/test_validation_membrane.py`、`tests/slices/test_schema_runner.py` 至少新增一轮器官级断言。

## Queue E 推荐实施顺序

```text
candidate_arena.py
  -> go_nogo.py
  -> world_contact_gate.py
  -> side_effect_review.py
  -> responsibility_loop.py
  -> observation_validator.py
  -> boundary_audit.py
  -> consistency_logic.py
  -> counterfactual_eval.py
  -> comparison_trace.py
```

原因：

1. 先把行动候选和世界接触链钉住，避免壳层直接放行动作。
2. 再把责任回路钉住，让副作用审查不止停在“有风险”，而是进入责任、后悔、修复和未来约束。
3. 再把观察真值和边界审计钉住，避免 validator 继续只产总报告。
4. 最后把反事实和比较 trace 落成器官，给责任/后悔和 repair loop 提供稳定输入。
