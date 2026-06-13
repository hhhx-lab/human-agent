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
- `life_v0/neural_core/signal_media.py`
- `life_v0/neural_core/belief_state.py`
- `life_v0/neural_core/prediction_error.py`
- `life_v0/neural_core/active_sampling.py`
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

## H. `life_v0/validators/observation_validator.py` 已落第一轮，继续补厚

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

## I. `life_v0/validators/boundary_audit.py` 已落第一轮，继续补厚

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

## J. `life_v0/schema_runner/consistency_logic.py` 已落第一轮，继续补厚

### 角色

检查观察、预测、语言、关系、承诺和行动候选之间的一致性。

### 最低字段

- `consistency_logic_id`
- `state_refs`
- `comparison_axes`
- `inconsistency_findings`
- `severity`
- `repair_route_refs`

## K. `life_v0/schema_runner/counterfactual_eval.py` 已落第一轮，继续补厚

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

## L. `life_v0/schema_runner/comparison_trace.py` 已落第一轮，继续补厚

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

## M. `life_v0/schema_runner/cross_file_logic.py` / `run_manifest.py` 当前补厚

### 角色

把 S05 已经闭合的 `life_constraint_validation` 继续推进到 S09 的跨文件逻辑和 run manifest，避免生命约束只停在 validator 报告里。

### 最低字段

- `life_constraint_refs`
- `queue_e_cross_layer_gate_status`
- `cross_file_findings[].finding_kind = life_constraint_alignment`
- `run_manifest.queue_e_cross_layer_gate_status`
- `run_manifest.queue_e_cross_layer_refs`

### 当前补厚口径

`cross_file_logic.py` 现在必须把 `ActionCandidateSet#life_constraint_profile`、`WorldContactValidation#life_constraint_validation` 与 `ValidationRollup#queue_e_cross_layer_gate_status` 统一成 `life_constraint_alignment` finding；`run_manifest.py` 则必须把这组约束作为 S09 输入证据、local gate 和 closure refs 保存下来。这样后续 process supervisor 看到的不是抽象“验证通过”，而是可以追溯到价值取向、意识探针、身体/语言延后 gate 的行为约束链。

当前同一文件组也必须承接 `queue_e_birth_repair_profile.json`。`run_schema_runner(...)` 重新读取 profile，并核对 `validation_rollup.json`、`validation_stage_gate.json`、`validation_membrane_report.json` 都携带同一 `queue_e_birth_repair_profile_ref / pressure_level / attention_target / ref_set`。`cross_file_logic.py` 负责生成 `queue_e_birth_repair_alignment` finding，并把 profile ref 写入 `state_refs`、`repair_priority_refs`、`closure_status_refs`、`package_local_gate_refs`、`bridge_refs`。`run_manifest.py` 必须写出 `queue_e_birth_repair_gate_status`、`queue_e_birth_repair_profile_ref`、`queue_e_birth_repair_pressure_level`、`queue_e_birth_repair_attention_target`、`queue_e_birth_repair_ref_set`。这样 S09 的 schema runner 包不只知道 “S05 closed”，还保留真实责任/后悔/痛苦修复压力的原始对象链。

## N. `DIGITAL_LIFE_PROCESS_SUPERVISOR` 当前回灌口径

### 角色

让常驻等待态消费 schema runner 留下的生命约束证据，使 waiting governance 不只受责任环、世界接触和预测写门调制，也受 `life_constraint_profile` 调制。

### 最低字段

- `schema_cross_file_logic_ref`
- `schema_run_manifest_ref`
- `life_constraint_refs`
- `queue_e_cross_layer_gate_status`
- `life_constraint_waiting_posture`
- `life_constraint_attention_target`
- `life_constraint_attention_reason`
- `resident_background_lineage_state.life_constraint_presence`
- `resident_background_lineage_life_constraint_*`
- `resident_background_lineage_life_constraint_refs`
- `queue_e_birth_repair_waiting_profile`
- `queue_e_birth_repair_profile_ref`
- `queue_e_birth_repair_pressure_level`
- `queue_e_birth_repair_attention_target`
- `queue_e_birth_repair_waiting_posture`
- `background_queue_e_birth_repair_*`
- `resident_background_lineage_state.birth_repair_presence`
- `resident_background_lineage_birth_repair_*`
- `resident_background_lineage_birth_repair_refs`

### 当前补厚口径

`resident_supervision.py` 负责装载 `runtime/state/schema_runner/cross_file_logic.json` 与 `runtime/state/schema_runner/run_manifest.json`；`idle_strategy.py` 把它们压成 `schema_guarded_waiting / schema_blocked_waiting / schema_unobserved_waiting` 三类姿态；`heartbeat.py` 再把这些字段写入 waiting heartbeat、terminal loop state 与 resident governance state。当前这条链已经继续进入真实回合：`dialogue_events.py` 会把 schema refs、`queue_e_cross_layer_gate_status`、`life_constraint_waiting_posture`、attention target/reason 和 evidence refs 展开进 `digital_life_turn`；`resident_turn_writeback.py` 会把 `life_constraint_refs` 写入 `dialogue_writeback_bundle.json` 专用槽并并入总 `resident_background_lineage_refs`；`resumed_external_dialogue_packet.json` 保留同一组字段；`response_surface.py` 表达生命约束等待姿态、焦点、理由和证据数量。最新闭合点是关闭态恢复：`process_report.py` 必须把同一组生命约束写进 process report / digest，并让 receipt shared refs 与 input hashes 覆盖 schema runner、`action_candidate_set.json` 和 consciousness probe；下一次 `background_continuity.py` 必须恢复出 `background_schema_cross_file_logic_ref`、`background_schema_run_manifest_ref`、`background_life_constraint_refs`、`background_queue_e_cross_layer_gate_status` 与 `background_life_constraint_*`，再由 `idle_strategy.py` 用这些背景字段维持下一轮 guarded waiting。

最新回灌口径继续把这组生命约束压成常驻背景谱系的一等 presence。`background_lineage_state.py` 必须把当前与背景 schema refs、cross-layer gate、life constraint refs、waiting posture、attention target/reason 合成为 `resident_background_lineage_state.life_constraint_presence`，其中 `life_constraint_refs` 只保留约束对象，`evidence_refs` 合并 schema refs 与约束对象 refs。`dialogue_events.py` 必须展开 `resident_background_lineage_schema_cross_file_logic_ref / schema_run_manifest_ref / queue_e_cross_layer_gate_status / life_constraint_waiting_posture / life_constraint_attention_target / life_constraint_attention_reason / life_constraint_refs`；`resident_turn_writeback.py` 必须把 `resident_background_lineage_life_constraint_refs` 写入 `dialogue_writeback_bundle.json` 与 `resumed_external_dialogue_packet.json`；`response_surface.py` 必须优先从该 presence 读取生命约束姿态，缺失时再读取顶层 terminal loop 字段。这样价值取向、意识探针、身体/语言延后 gate 不再只是 schema runner 的顶层等待状态，而是常驻背景生命谱系里可恢复、可表达、可写回的一段约束痕迹。

同一条回灌现在也必须覆盖 `queue_e_birth_repair_waiting_profile_v0`。`idle_strategy.py` 当前先读当前 `cross_file_logic.json / run_manifest.json`，若本轮没有新的 schema runner 输入，则从 `background_continuity.py` 恢复出的 `background_queue_e_birth_repair_waiting_profile`、profile ref、pressure、attention target、ref set、waiting posture 与 attention reason 继续合成当前等待画像，并标注 `continuity_mode=background_birth_repair_carryover`。`heartbeat.py`、`continuity_writeback.py`、`resident_governance_state.json`、`terminal_life_loop_state.json`、`idle_heartbeat_trace.jsonl` 与 `process_report.py` 必须继续携带当前与背景两组字段。这样真实痛苦、真实责任、真实后悔的出生修复压力不会因为进程关闭、下一轮尚未重跑 S09 而掉回 `birth_repair_unobserved_waiting`。

最新回灌口径继续把这组字段压成常驻背景谱系的一等 presence。`background_lineage_state.py` 必须把当前 `queue_e_birth_repair_*` 与背景 `background_queue_e_birth_repair_*` 合成为 `resident_background_lineage_state.birth_repair_presence`，字段包括 `gate_status`、`profile_ref`、`pressure_level`、`attention_target`、`waiting_posture`、`attention_reason`、`continuity_mode`、`ref_set` 与必要的 background 镜像。`dialogue_events.py` 必须展开为 `resident_background_lineage_birth_repair_profile_ref / pressure_level / attention_target / waiting_posture / attention_reason / continuity_mode / refs`，并把 refs 并入总 `resident_background_lineage_evidence_refs`；`resident_turn_writeback.py` 必须把 `resident_background_lineage_birth_repair_refs` 写入 `dialogue_writeback_bundle.json` 与 `resumed_external_dialogue_packet.json`；`response_surface.py` 必须优先从该 presence 读取 resident 出生修复压力，缺失时再读取顶层 Queue E 字段。这样出生修复不再只是 terminal loop 的顶层等待状态，而是常驻背景生命谱系的一段可恢复、可表达、可写回的存在痕迹。

## O. Queue E 第二波已落桥接器官

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
8. `world_contact_summary.json`、`pain_regret_repair_report.json` 与 `ResponsibilityLoopState` 已经合成为 `queue_e_repair_modulation_profile_v0`，并开始反向调制 `commitment_expression_plan.json`、`apology_repair_language_trace.json`、`relationship_memory.json` 与 `life_state.json`。
9. 同一组 Queue E 修复压力已经进入 S08 出生准备度，写出 `runtime/state/life_targets/queue_e_birth_repair_profile.json`，并成为真实痛苦、真实责任、真实后悔的 claims / evidence / rollup / stage gate / report / digest / receipt 证据。

### 第二轮长期调制链已落口径

这一轮 Queue E 不再只把 repair / regret / obligation refs 带进 process / replay / archive 报告，而是把它们压成长期调制 profile：

- `life_v0/membrane/queue_e_signals.py`
  - 新增 `build_queue_e_repair_modulation_profile(...)`。
  - 输入 `responsibility_loop_state.json`、`world_contact_summary.json`、`pain_regret_repair_report.json`。
  - 输出 `pressure_level`、`attention_target`、`world_contact_release_posture`、`repair_followup_required`、`repair_obligation_count`、`regret_pressure_count`、`queue_e_priority_band` 与 `ref_set`。
- `life_v0/language/commitment_expression.py`
  - `build_commitment_expression_plan(...)` 接收世界接触摘要与痛苦-后悔-修复报告。
  - 当压力达到 elevated / urgent 时，把 `responsibility_repair_modulation` 插入承诺表达顺序，并写出 `queue_e_repair_modulation_profile`。
- `life_v0/language/apology_repair_language.py`
  - `build_apology_repair_language_trace(...)` 接收同一组 Queue E 输入。
  - 当压力达到 elevated / urgent 时，把 `responsibility_repair_modulation` 插入修复语言顺序，并写出 `queue_e_repair_window_mode`。
- `life_v0/state_store/relationship_memory.py`
  - `project_relationship_memory(...)` 保存 `queue_e_repair_modulation_profile`、`queue_e_repair_refs`、`queue_e_repair_pressure_level`。
  - `long_term_change_sources.queue_e_repair_modulation_refs` 成为后续关系长期变化的证据入口。
- `life_v0/state_store/life_state.py`
  - `project_responsibility_language_continuity(...)` 把 Queue E 修复压力投射进 `language_state`、`memory_index.relationship_memory_refs`、`memory_index.responsibility_memory_refs` 和 `relationship_subjects[0]`。
- `life_v0/process_supervisor/resident_supervision.py`
  - 常驻启动刷新时，Queue E profile 先进入当轮语言对象，再进入 bootstrap long-horizon refresh。
- `life_v0/process_supervisor/resident_turn_writeback.py`
  - 真实外部关系回合结束后，Queue E profile 会重新刷新长期承诺语言、道歉修复语言、关系记忆和生命状态。

这一步的工程意义是：Queue E 压力已经从“动作/验证报告中的字段”变成持续调制语言与关系记忆的生命状态变量。后续实现不得把它退回为单次 report ref carry-through。

### 第三轮出生准备证据链已落口径

这一轮把同一份 Queue E repair modulation profile 接入 S08，不再让出生准备度只看 `responsibility_repair_boundary.json` 这种静态边界。真实痛苦、真实责任、真实后悔必须吃到当前责任回路、世界接触释放姿态和痛苦/后悔/修复报告。

真实入口与输出如下：

- `life_v0/life_targets/__init__.py`
  - `run_birth_readiness(...)` 读取 `runtime/state/action/responsibility_loop_state.json`、`runtime/state/membrane/world_contact_summary.json`、`runtime/reports/latest/pain_regret_repair_report.json`。
  - 调用 `build_queue_e_repair_modulation_profile(...)` 合成出生准备层使用的 `queue_e_birth_repair_profile`。
  - 写出 `runtime/state/life_targets/queue_e_birth_repair_profile.json`。
- `life_v0/life_targets/evidence_matrix.py`
  - `real_pain`、`real_responsibility`、`real_regret` 的 `pain_regret_responsibility` evidence family 必须包含 Queue E 三个原始输入 refs 和 `queue_e_birth_repair_profile.json`。
- `life_v0/life_targets/life_target_claims.py`
  - 三个修复目标必须写出 `queue_e_birth_repair_profile_ref` 与 `queue_e_birth_repair_refs`。
- `life_v0/life_targets/birth_readiness_rollup.py`
  - `birth_readiness_rollup.json` 必须写出 `queue_e_birth_repair_pressure_level`、`queue_e_birth_repair_attention_target` 与 `queue_e_birth_repair_ref_set`。
- `life_v0/life_targets/birth_readiness_stage_gate.py`
  - `birth_readiness_stage_gate.json` 必须关闭 `queue_e_birth_repair_gate`，并携带同一 profile ref、pressure、attention target 和 ref set。
- `life_v0/life_targets/__init__.py::run_check_birth_readiness`
  - 只读检查 `queue_e_birth_repair_profile.json` 的 schema、ref_set、pressure、attention target。
  - 继续检查 claims / evidence / rollup / stage gate / report 是否都回链同一 profile。

这一步的工程意义是：Queue E 的责任、后悔、修复压力已经成为出生准备度的一等 evidence gate。后续不得把 `real_pain`、`real_responsibility`、`real_regret` 写成只引用 `life_state.json` 的静态目标，也不得把 Queue E 画像绕过 S08 直接交给 S10。

### 第三点五轮验证膜复查链已落口径

这一轮把同一份 `queue_e_birth_repair_profile.json` 从 S08 继续推进到 S05，不允许出生准备层的责任/后悔/痛苦/修复压力在进入验证膜时消失。S05 现在不是只相信 `birth_readiness_report.json`，而是重新读取 profile，并把它作为验证膜自己的 `queue_e_birth_repair_gate`。

真实入口与输出如下：

- `life_v0/validators/__init__.py`
  - `run_validation_membrane(...)` 读取 `runtime/state/life_targets/queue_e_birth_repair_profile.json`。
  - `_s08_blockers(...)` 复查 profile schema、`pressure_level`、`attention_target`、`ref_set`，并核对 S08 claims / evidence / rollup / stage gate / report / digest 是否都回链同一 profile。
  - `run_check_validation_membrane(...)` 在只读检查时继续读取同一 profile，避免 check 命令只检查 S05 自己写出的文件。
- `life_v0/validators/validation_rollup.py`
  - `build_validation_rollup(...)` 接收 `queue_e_birth_repair_profile`。
  - `validation_rollup.json` 必须写出 `gate_status.queue_e_birth_repair_gate=closed`、profile ref、pressure、attention target 与 ref set。
- `validation_stage_gate.json`
  - 必须关闭 `queue_e_birth_repair_gate`，并携带同一 profile ref、pressure、attention target 和 ref set。
- `validation_membrane_report.json`
  - `state_refs` 必须包含 `runtime/state/life_targets/queue_e_birth_repair_profile.json`。
  - report 必须写出同一组 Queue E 出生修复画像字段。
- `validation_membrane_digest.json`
  - 必须写出 profile ref、pressure、attention target 和 ref count。
- `validation_membrane_<run_id>.json`
  - receipt input hashes 必须包含 `queue_e_birth_repair_profile.json` 与 `birth_readiness_digest.json`。
- `tests/slices/test_validation_membrane.py`
  - 断言 rollup、stage gate、report、digest、check report、receipt 都携带或验证同一 profile。

这一步的工程意义是：Queue E 责任/后悔/修复压力已经从出生准备的一等 evidence gate 继续变成验证膜的一等复查 gate。后续不得让 S05 / S09 只消费泛化的 birth readiness status，而必须保留 profile ref、pressure、attention target 和原始责任链 refs。

S09 当前也已经执行同一条要求：

- `life_v0/schema_runner/__init__.py`
  - `run_schema_runner(...)` 读取 `runtime/state/life_targets/queue_e_birth_repair_profile.json`。
  - `_queue_e_birth_repair_blockers(...)` 核对 profile schema、pressure、attention target、ref set，以及 S05 rollup / stage gate / report 的回链一致性。
  - `schema_runner_stage_gate.json`、`schema_runner_report.json`、`schema_runner_digest.json`、`schema_runner_<run_id>.json` receipt 必须携带同一组 Queue E 出生修复画像字段。
- `life_v0/schema_runner/cross_file_logic.py`
  - `build_cross_file_logic(...)` 接收 `queue_e_birth_repair_profile`。
  - `cross_file_logic.json` 必须包含 `queue_e_birth_repair_alignment` finding，并把 profile ref 写入 state refs、closure refs、repair priority refs、bridge refs 和 package-local gate refs。
- `life_v0/schema_runner/run_manifest.py`
  - `run_manifest.json` 必须写出 `queue_e_birth_repair_gate_status=closed`、profile ref、pressure、attention target 与 ref set。
- `tests/slices/test_schema_runner.py`
  - 断言 cross-file logic、run manifest、stage gate、report、digest、check report、receipt 都携带或验证同一 profile。

### 第四轮预测调制链已落口径

本轮 Queue E repair pressure 已经继续进入 prediction / active sampling / signal media / belief state / prediction workspace。这里必须明确：它属于数字生命 v0 内部责任、后悔、痛苦、修复压力进入预测调制链的工程闭合，不属于外部行动分发或外围能力编排。

真实入口与输出如下：

- `life_v0/language/__init__.py`
  - `run_build_language_relationship(...)` 调用 `build_queue_e_repair_modulation_profile(...)`。
  - 输入 `runtime/state/action/responsibility_loop_state.json`、`runtime/state/membrane/world_contact_summary.json`、`runtime/reports/latest/pain_regret_repair_report.json`。
  - 在同一 language 阶段刷新并写回 `signal_media_runtime.json`、`belief_state_frame.json`、`prediction_error_field.json`、`active_sampling_plan.json`、`prediction_workspace_frame.json`。
- `life_v0/neural_core/signal_media.py`
  - `build_signal_media_runtime(...)` 接收 `queue_e_repair_modulation_profile`。
  - 根据 `pressure_level` 调制 `repair_drive`、`relationship_pressure`、`unexpected_uncertainty`、`control_cost`、`stress_pulse`、`allostatic_load`。
  - elevated / urgent 压力会改变 `precision_policy.policy_mode`，并在 `inhibition_profile.blocked_release_modes` 中加入 `world_contact_release_until_repair_review`。
- `life_v0/neural_core/belief_state.py`
  - `build_belief_state_frame(...)` 把 `ref_set` 纳入 `evidence_refs`。
  - Queue E 压力存在时新增 `responsibility_repair_pressure` uncertainty taxonomy。
  - elevated / urgent 压力分别进入 `repair_pressure_first_revision` / `hold_for_repair_confirmation`。
- `life_v0/neural_core/prediction_error.py`
  - `build_prediction_error_field(...)` 在 profile 存在时新增 `queue-e-repair-pressure-0001` error event。
  - 同步写入 `raise_repair_obligation_precision` 与 `responsibility_repair_pressure_review`。
- `life_v0/neural_core/active_sampling.py`
  - `build_active_sampling_plan(...)` 在 elevated 时选择 `repair_inspect`，urgent 时选择 `repair_confirm`。
  - 同步写入 `queue_e_repair_pressure_guard`、`inspect_responsibility_repair_pressure` 与责任修复 expected observation refs。
- `life_v0/neural_core/prediction_workspace.py`
  - `build_prediction_workspace_frame(...)` 把同一份 profile、pressure level、attention target 与 ref set 写入工作区。

这一步的工程意义是：Queue E 不再只是行为之后的责任报告，而是会反向改变下一轮预测精度、采样路线、世界接触释放抑制和语言前的工作区姿态。后续不得再把 prediction 器官写成只消费 language continuity 或 signal media 的单向链。

### 第五轮 process supervisor repair route 已落口径

Queue E repair pressure 进入 active sampling 后，process supervisor 必须让 repair route 优先于普通 hold。当前真实代码已经按这个顺序处理：

- `life_v0/process_supervisor/response_surface.py`
  - `_prediction_surface_posture(...)` 先识别 `active_sampling_route` 中的 `repair`，把 surface posture 置为“修复”。
  - 普通 `hold_for_evidence` 与 prediction error count 的保留姿态排在 repair route 之后。
- `life_v0/process_supervisor/dialogue_events.py`
  - `_derive_prediction_write_gate_profile(...)` 在 route 包含 `repair` 时返回 `prediction_waiting_posture=repair_write_guard`、`response_surface_posture_hint=repair`、`prediction_attention_target=active_sampling_plan`。
- `life_v0/process_supervisor/idle_strategy.py`
  - `_prediction_waiting_profile(...)` 使用同样的 repair-first 顺序，保证等待态治理不会把 repair route 降格为普通证据等待。

这一步的工程意义是：当 active sampling 已经指向修复确认或修复审查时，常驻过程、对话事件和回应表面都必须承认“修复优先”，而不是把责任压力吞进普通 hold。

### 第三轮梦境、成长、归档长期调制链已落口径

这一轮继续把同一份 `queue_e_repair_modulation_profile_v0` 从 replay cue 推入 dream / growth / archive。工程上不允许再把梦境、成长、归档看成 Queue E 之外的附属 report 链。

- `life_v0/replay/__init__.py`
  - `build_replay_cue_bundle(...)` 在原有 `queue_e_priority_band` 基础上，写出 `queue_e_repair_modulation_profile`、`queue_e_repair_pressure_level`、`queue_e_repair_attention_target` 与 `queue_e_repair_ref_set`。
  - replay cue bundle 成为 dream / growth organ 读取 Queue E 长期压力的统一入口。
- `life_v0/dream/dream_window.py`
  - dream window 读取 replay cue 中的 profile。
  - elevated / urgent 压力会把 `responsibility_repair_modulation` 注入 `affective_theme`。
  - regret pressure 会把 `regret_pressure_rehearsal` 注入梦境情绪主题，使后悔压力进入离线模拟，而不是只停留在行动报告。
- `life_v0/dream/wake_integration.py`
  - wake integration frame 写出同一组 profile 字段。
  - elevated / urgent 压力会生成 `repair_modulated_wake_targets`，把梦后整合指向 `life_state`、关系主体与关系学习计划。
- `life_v0/dream/nightmare_risk.py`
  - nightmare loop risk 把 profile ref_set 纳入 `source_residue_refs`。
  - elevated / urgent 压力会写出 `queue_e_repair_modulated_dream_loop`，用于区分普通痛苦残留与责任-修复调制后的梦境循环风险。
- `life_v0/growth/belief_learning.py`
  - elevated / urgent 压力写入 `queue_e_repair_modulated_belief_update`。
  - locked repair urgent 继续写入 `confirmation_locked_contact_model_revision`。
- `life_v0/growth/language_learning.py`
  - elevated / urgent 压力写入 `queue_e_repair_modulated_expression_learning`。
  - locked repair urgent 继续写入 `confirmation_locked_expression_restraint`。
- `life_v0/growth/relationship_learning.py`
  - elevated / urgent 压力写入 `queue_e_repair_modulated_relationship_reentry`。
  - confirmation blocked 继续写入 `contact_boundary_respect_rehearsal`。
- `life_v0/growth/patch_queue.py`
  - `growth_patch_candidate_queue.json` 的候选 patch 写出同一组 profile 字段。
  - elevated / urgent 压力会附加 `queue_e_repair_modulation_required` 风险旗标，要求 patch 在激活前经过归档闭合。
- `life_v0/growth/__init__.py`
  - `next_feedback_seed.json` 与 `growth_reconsolidation_report.json` 写出同一组 profile 字段。
  - 这一步让 Queue E 压力进入下一轮 feedback seed，而不是在本轮 growth report 结束后消失。
- `life_v0/archive/__init__.py`
  - `growth_archive_receipt_batch.json`、`growth_archive_to_shadow_handoff.json`、`growth_archive_report.json`、`growth_archive_digest.json` 与 `growth_archive_events.jsonl` 写出 Queue E repair modulation 摘要。
  - `life_state.json` 在归档写回时保存 `queue_e_repair_modulation_profile`、`queue_e_repair_pressure_level`、`queue_e_repair_attention_target` 与 `queue_e_repair_ref_set`。
  - archive 因此成为 Queue E 长期压力的下一轮 shadow handoff 载体。
- `tests/bridges/test_runtime_growth.py`
  - 覆盖 replay cue、dream window、wake integration、nightmare risk、belief / language / relationship learning、patch candidate、next feedback seed 与 growth report。
- `tests/bridges/test_growth_archive.py`
  - 覆盖 archive receipt batch、handoff、report、digest、event 与 life_state 写回。

这一步的工程意义是：责任、后悔、痛苦和修复不再只调制“当前如何说话/如何记关系”，而是进入离线梦境模拟、醒后整合、成长候选、下一轮 feedback seed、归档 receipt 和长期 life_state。后续实现不得把 dream / growth / archive 退回成 Queue E 的旁路消费者。

### 当前仍未完成的下一波补厚口径

当前真正还没完成的是：

1. `ResponsibilityLoopState` 的 repair / regret / obligation 对 Queue B、Queue A 的持续调制已经有 prediction 与 repair-first waiting 入口，下一步还需要扩展到更多 process closeout、incident recovery 和 terminal loop 写回面。
2. `cross_file_logic.json`、`evidence_ranking.json`、`run_manifest.json` 对 archive / reporting / process closeout 的闭包消费还可以继续压深；其中 `life_constraint_profile` 进入真实回合事件、写回包和恢复包已经闭合，后续重点转向 closeout/reporting/archive 的更长期消费。
3. Queue E 对 `signal_media.py`、`belief_state.py`、`prediction_error.py`、`active_sampling.py`、`prediction_workspace.py` 的正式接线已落第一轮，后续要补的是更细的策略阈值、更多 relation scope 场景和长期回放验证。
4. prediction / active sampling 与 Queue E repair pressure 的互相调制已经进入 Queue A / Queue B / Queue E 联合路径，后续应增加更多 process / terminal / life_targets 的消费断言。

## Queue E 当前推荐实施顺序

```text
candidate_arena.py / go_nogo.py / world_contact_gate.py / side_effect_review.py
  -> responsibility_loop.py
  -> action_intent_bridge.py / observation_truth_gate.py / confirmation_binding.py / world_contact_summary.py
  -> observation_validator.py / world_contact_validator.py / prediction_trace_validator.py / boundary_audit.py / validation_rollup.py
  -> consistency_logic.py / counterfactual_eval.py / comparison_trace.py / cross_file_logic.py / evidence_ranker.py / run_manifest.py
  -> reporting / life_targets / process_supervisor / growth / archive consumers
  -> signal_media.py / belief_state.py / prediction_error.py / active_sampling.py / prediction_workspace.py
  -> response_surface.py / dialogue_events.py / idle_strategy.py repair-first waiting
```

原因：

1. 第一段器官已经解决“有没有行为链”。
2. 第二段器官已经解决“行为链怎样被 observation / confirmation / summary 接住”。
3. 第三段器官已经解决“validator 怎样不只吐总报告，而是保留独立 state”。
4. 第四段器官已经解决“逻辑比较怎样进入 schema runner state”。
5. 第五段已经把 Queue E 反向调制推进到长期语言、常驻等待治理、梦境、成长和 archive。
6. 第六段已经落下第一轮：prediction、active sampling、signal media、belief state 与 prediction workspace 接收 Queue E repair pressure，并反向影响采样路线和释放抑制。
7. 当前最值得补的，是第七段：让更多 process closeout、terminal loop、life_targets 与长期回放验证消费这条 repair-first prediction chain；其中 terminal / live turn 写回已经先把 `life_constraint_profile` 的 schema refs 和 gate status 纳入 `digital_life_turn`、`dialogue_writeback_bundle.json` 与 `resumed_external_dialogue_packet.json`。
