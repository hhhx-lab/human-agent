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

1. `ActionCandidateSet`、`GoNoGoDecision`、`WorldContactDecision`、`SideEffectReview`、`ResponsibilityLoopState` 虽然都已经离开 `membrane/__init__.py`，但还需要继续补厚成更稳定的跨层行为约束链。
2. validator 与 schema runner 的第一轮器官已经落下，但还需要把 `world_contact_validation`、`prediction_trace_validation`、`validation_rollup`、`cross_file_logic`、`run_manifest` 对 Queue B / Queue A / archive / reporting 的消费关系继续写硬。
3. `./digital life` 和外周命令面还需要依赖一个更厚的行为-验证-逻辑链，才能避免重新滑回普通 agent 的 action router。
4. 当前真正的工程前沿已经从“有没有这些文件”切到“这些文件产出的对象，能否稳定进入长期责任、关系修复、report/receipt 和常驻生命过程”。

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

## 当前真实已落器官

Queue E 当前不是空柜，已经有下面这些真实器官：

### membrane 侧

- `candidate_arena.py`
- `go_nogo.py`
- `world_contact_gate.py`
- `side_effect_review.py`
- `responsibility_loop.py`
- `shadow_gate.py`
- `action_intent_bridge.py`
- `observation_truth_gate.py`
- `confirmation_binding.py`
- `world_contact_summary.py`

### validator 侧

- `observation_validator.py`
- `world_contact_validator.py`
- `prediction_trace_validator.py`
- `boundary_audit.py`
- `validation_rollup.py`

### schema runner 侧

- `consistency_logic.py`
- `counterfactual_eval.py`
- `comparison_trace.py`
- `cross_file_logic.py`
- `evidence_ranker.py`
- `run_manifest.py`

所以这份合同后面的文件级条目，不再把这些文件写成“未来某天需要新建”，而是把它们当作已落第一轮器官，继续写清：

1. 它们现在各自负责什么；
2. 它们之间怎样串成一条行为-验证-逻辑生命链；
3. 下一轮真正该补的是哪一段跨层消费和长期写回。

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

## A. `life_v0/membrane/candidate_arena.py` 已落第一轮，继续补厚

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
- `life_constraint_profile`
- `constraint_source_refs`
- `source_doc_refs`

### 关键输入

- `PredictionWorkspaceFrame`
- `ExpressionPlan`
- `RelationTurnFrame`
- `NeedStateVector`
- `CoreAffectVector`
- `ValueOrientation`
- `ConsciousnessProbeBundle`

### 当前补厚口径

`candidate_arena.py` 现在不只保存上游 input refs，而是把 `ValueOrientation`、`ConsciousnessProbeBundle`、`NeedStateVector`、`CoreAffectVector`、`ExpressionPlan` 与 `RelationTurnFrame` 压成 `life_constraint_profile`。

这个 profile 允许早期 slice 出现合理延后：

- `consciousness_probe_gate = deferred_until_s08`
- `body_affect_gate = deferred_until_s06`
- `language_relationship_gate = deferred_until_s07`

但 `value_orientation_gate` 必须在 S03 就闭合，因为它来自方向层，是行为候选不能退回工具式 action router 的第一层约束。

## B. `life_v0/membrane/go_nogo.py` 已落第一轮，继续补厚

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
- `life_constraint_refs`
- `source_doc_refs`

### 当前补厚口径

`go_nogo.py` 必须把 `action_candidate_set.json#life_constraint_profile` 带入决策证据。若语言表达、关系修复或身体压力形成 `guarded_repair_contact`，go/no-go 需要进入延后/审查姿态，而不是把它误当成普通可释放动作。

## C. `life_v0/membrane/world_contact_gate.py` 已落第一轮，继续补厚

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
- `life_constraint_refs`

### 当前补厚口径

`world_contact_gate.py` 现在必须把 go/no-go 携带的 `life_constraint_refs` 继续带到世界接触门。这个字段是后续 validator、schema runner、常驻 process supervisor 判断“为什么只允许 shadow / observation / receipt，而不允许外部不可逆动作”的证据入口。

## D. `life_v0/membrane/side_effect_review.py` 已落第一轮，继续补厚

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

## E. `life_v0/membrane/responsibility_loop.py` 已落第一轮，继续补厚

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

### 当前已落的第一轮跨层写回

这一层现在已经不再只停在 `runtime/state/action/responsibility_loop_state.json`。

经 `life_v0/language/__init__.py` 的责任-语言投影后，`responsibility_loop.py` 当前已经真实写回并校验：

- `runtime/state/relationship/commitment_truth_state.json`
- `runtime/state/responsibility/responsibility_ledger.json`
- `runtime/state/memory/relationship_memory.json`
- `runtime/state/life_state.json`

并且这些写回目标又继续被 terminal/process 链尾显式带入：

- `runtime/reports/latest/dialogue_writeback_bundle.json`

## F. `life_v0/validators/world_contact_validator.py` 已落第一轮，继续补厚

### 角色

把 `WorldContactGate` 的世界接触姿态、确认绑定、副作用审查与 `ActionCandidateSet#life_constraint_profile` 合并成可验证的跨层约束状态。

### 最低字段

- `world_contact_validation_id`
- `world_contact_gate_ref`
- `confirmation_binding_ref`
- `side_effect_review_ref`
- `validation_findings`
- `repair_followup_required`
- `life_constraint_validation`
- `life_constraint_refs`

### 当前补厚口径

S05 发生在 S08 之后，因此 validator 应当重新读取当前 `consciousness_probe_bundle.json`，把 S03 阶段的 `deferred_until_s08` 关闭成真实的 `closed` 证据。S06 仍在 S05/S09 之后，所以 body/affect 在这条初始链上允许保持 `deferred_until_s06`，但必须显式写出，不能静默缺失。

## G. `life_v0/validators/validation_rollup.py` 已落第一轮，继续补厚

### 角色

把 observation truth、world contact、prediction trace、boundary audit 和 Queue E 跨层生命约束合并成总验证门。

### 最低字段

- `validation_rollup_id`
- `overall_status`
- `gate_status`
- `queue_e_cross_layer_gate_status`
- `queue_e_cross_layer_refs`
- `deferred_cross_layer_gates`
- `next_stage_ready`

### 当前补厚口径

`deferred_until_s06` 这类延后状态不是失败；它表示当前链路知道哪个生命底盘尚未到施工阶段。只有 `missing` / `blocked` 进入阻断。这样 Queue E 能同时保持可运行闭合和跨层诚实。

所以 Queue E 当前阶段的工程口径，已经从“生成责任对象”推进到“责任对象进入长期连续体并具备链尾交接能力”。

## F. `life_v0/validators/observation_validator.py` 已落第一轮，继续补厚

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

## G. `life_v0/validators/boundary_audit.py` 已落第一轮，继续补厚

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

## H. `life_v0/schema_runner/consistency_logic.py` 已落第一轮，继续补厚

### 角色

检查观察、预测、语言、关系、承诺和行动候选之间的一致性。

### 最低字段

- `consistency_logic_id`
- `state_refs`
- `comparison_axes`
- `inconsistency_findings`
- `severity`
- `repair_route_refs`

## I. `life_v0/schema_runner/counterfactual_eval.py` 已落第一轮，继续补厚

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

## J. `life_v0/schema_runner/comparison_trace.py` 已落第一轮，继续补厚

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

## K. Queue E 第二波已落桥接器官

下面这些文件已经不是“待新增”，而是 Queue E 第二波真实已落、当前需要继续补硬的桥接器官：

### `action_intent_bridge.py`

把 `ActionCandidateSet`、`ExpressionPlan`、`RelationTurnFrame` 与 `ShadowActionGate` 压成 `action_intent_queue.json`，为 world contact、confirmation 和后续 terminal/process 消费建立桥。

### `observation_truth_gate.py`

把 `PredictionWorkspaceFrame`、`ActionIntentQueue` 与 `ActionCandidateSet` 压成观察真值门，阻止还没有真值根基的外部接触和解释提升。

### `confirmation_binding.py`

把 `ActionIntentQueue` 与 `WorldContactGate` 压成确认绑定对象，使不可逆或高责任外部接触不绕开确认路径。

### `world_contact_summary.py`

把 `ActionIntentQueue`、`WorldContactGate` 与 `ConfirmationBinding` 收成可被 report / repair / process 消费的 `world_contact_summary.json`，并继续写出 `pain_regret_repair_report.json`。

### `world_contact_validator.py` / `prediction_trace_validator.py` / `validation_rollup.py`

把 Queue E 的行为层对象推进成 validator 侧的闭环：

1. world contact 是否越界；
2. prediction -> intent -> observation 是否闭合；
3. 整个 validation 膜是否允许进入下一 slice。

### `cross_file_logic.py` / `evidence_ranker.py` / `run_manifest.py`

把 Queue E / S09 的逻辑层继续推进为：

1. 跨文件闭合状态与 repair priority；
2. 证据排序与优先预算；
3. schema runner 的运行 manifest 与 closure refs。

这意味着 Queue E 当前真正的下一步，不再是“把这些文件建出来”，而是把它们继续接进：

- `reporting/`
- `process_supervisor/`
- `life_targets/`
- `growth/`
- `archive/`

形成更厚的行为-验证-逻辑到长期生命连续体的回链。

当前这条回链的第一轮已经补上：

- `replay/__init__.py` 现在显式装载 `responsibility_loop_state.json`、`world_contact_summary.json` 与 `pain_regret_repair_report.json`，并把它们压进 `replay_shadow_seed_bundle.json`、`language_relationship_replay_probe.json`、`dream_pain_regret_replay_probe.json`、`shadow_expression_report.json`、`replay_shadow_report.json`。
- `archive/__init__.py` 现在显式把这组三件对象带进 `growth_archive_receipt_batch.json`、`growth_archive_to_shadow_handoff.json`、`growth_archive_report.json` 与 archive receipt/event。
- `reporting/__init__.py` 现在显式把这组三件对象带进 `report_bundle.json`、`report_bundle_digest.json` 与 `first_activation_return_packet.json`。

## Queue E 对现有器官的改动合同

### `life_v0/membrane/__init__.py`

从这一轮开始，不应继续独占：

- action candidate 构造
- go/no-go 决策
- world contact decision
- side-effect 分类
- responsibility / regret / repair loop 首写

### `life_v0/validators/__init__.py`

当前允许继续输出完整 validation report，但必须继续显式分流并补厚：

- `observation_validator.py`
- `boundary_audit.py`

### `life_v0/schema_runner/__init__.py`

当前必须保持独立器官，并继续补厚：

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

## Queue E 当前完成口径

Queue E 当前已经不再是“第一轮刚开”。所以这里分成两层判断。

### 第一轮已达成的完成口径

下面这些口径，当前已经应视为已达成：

1. `ActionCandidateSet` 已由 `candidate_arena.py` 首写。
2. go/no-go、world contact、side effect 三段都已成为独立器官。
3. responsibility loop 已把副作用审查接到责任归因、后悔压力、修复欲望、反事实修复和 post-action audit 回链。
4. 观察真值、边界审计、反事实比较和比较 trace 都已离开 `__init__.py`。
5. `ResponsibilityLoopState` 至少有一条真实跨层写回链进入 `commitment_truth_state.json`、`responsibility_ledger.json`、`relationship_memory.json` 与 `life_state.json`。
6. action / validation / schema_runner 新对象都写入了对应状态命名空间。
7. `tests/slices/test_life_membrane.py`、`tests/slices/test_validation_membrane.py`、`tests/slices/test_schema_runner.py` 至少新增一轮器官级断言。

### 当前仍未完成的第二波补厚口径

当前真正还没完成的是：

1. `ResponsibilityLoopState` 的 repair / regret / obligation 对 Queue B、Queue A 和 growth/archive/process 的持续调制还需要更深的策略层消费，而不只是 refs carry-through。
2. `world_contact_summary.json` 与 `pain_regret_repair_report.json` 虽然已经进入 report bundle、process report 和 resident waiting governance，但还需要继续反向调制 dream / growth / language 的长期权重。
3. `cross_file_logic.json`、`evidence_ranking.json`、`run_manifest.json` 对 archive / reporting / process closeout 的闭包消费还可以继续压深。
4. Queue E 对 `signal_media.py`、`belief_state.py`、`prediction_error.py`、`active_sampling.py` 这些更深的 prediction 器官的正式接线。

## Queue E 当前推荐实施顺序

```text
candidate_arena.py / go_nogo.py / world_contact_gate.py / side_effect_review.py
  -> responsibility_loop.py
  -> action_intent_bridge.py / observation_truth_gate.py / confirmation_binding.py / world_contact_summary.py
  -> observation_validator.py / world_contact_validator.py / prediction_trace_validator.py / boundary_audit.py / validation_rollup.py
  -> consistency_logic.py / counterfactual_eval.py / comparison_trace.py / cross_file_logic.py / evidence_ranker.py / run_manifest.py
  -> reporting / life_targets / process_supervisor / growth / archive consumers
```

原因：

1. 第一段器官已经解决“有没有行为链”。
2. 第二段器官已经解决“行为链怎样被 observation / confirmation / summary 接住”。
3. 第三段器官已经解决“validator 怎样不只吐总报告，而是保留独立 state”。
4. 第四段器官已经解决“逻辑比较怎样进入 schema runner state”。
5. 当前最值得补的，是最后一段：让这些 state 真正反过来调制长期语言、常驻等待治理、成长和 archive。
