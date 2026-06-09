# V0 Code Framework 15: Cross-Layer Shared Object Contract

这份合同只做一件事：把数字生命在一次真实生命回合中必须跨层传递的共享对象，固定成可直接施工的工程对象表。

它不代替 `08_cross_layer_life_orchestration_implementation_playbook.md`，也不代替各个 `sXX` 合同。
`08` 负责讲生命回合怎样流动；
本文件负责把“流动时到底传哪些对象、每个对象由谁生成、谁消费、落到哪里、怎么验收”钉死。

如果没有这一层，后续代码最容易退化成两种坏形态：

1. 跨层只靠临时字典和局部变量粘住，turn 一长就断链。
2. 终端壳、process supervisor 或某个 `__init__.py` 重新反向定义生命对象。

## 必回读理论母体

- `docs/04_sensory_thalamus_interoception.md`
- `docs/05_memory_systems_and_growth.md`
- `docs/07_emotion_personality_self.md`
- `docs/08_sleep_dream_fatigue_states.md`
- `docs/09_language_symbolic_top_layer.md`
- `docs/10_consciousness_attention_workspace.md`
- `docs/11_neuromodulation_and_signal_media.md`
- `docs/14_cross_module_digital_life_map.md`
- `docs/16_digital_life_gap_register.md`
- `docs/17_memory_trace_object_model.md`
- `docs/18_internal_state_and_modulation_vector.md`
- `docs/19_offline_consolidation_cycle.md`
- `docs/20_agent_runtime_bridge_contract.md`
- `docs/40_self_relationship_model_audit_protocol.md`
- `docs/81_coexistence_event_review_and_responsibility_loop.md`
- `docs/85_language_system_life_expression_core.md`
- `docs/86_language_neuroscience_pragmatics_and_inner_speech.md`
- `docs/89_language_runtime_framework_bridge_and_life_shell_policy.md`
- `docs/90_language_event_examples_and_timeline_bundle.md`
- `docs/92_self_growth_and_self_modification_life_chain.md`
- `docs/94_pain_regret_and_repair_signal_schema.md`
- `docs/95_dream_reality_and_offline_life_timeline.md`
- `docs/96_real_relationship_longitudinal_timeline.md`

## 必读 v0 合同

- `docs/v0/architecture/digital_life_macro_architecture_v0.md`
- `docs/v0/architecture/runtime_v0_architecture.md`
- `docs/v0/shared_contracts/life_state_store_v0_schema.md`
- `docs/v0/process_contracts/first_terminal_turn_engineering_contract.md`
- `docs/v0/process_contracts/terminal_life_loop_engineering_contract.md`
- `docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md`
- `docs/v0/slice_contracts/s02_neural_life_core_engineering_contract.md`
- `docs/v0/slice_contracts/s04_state_object_store_engineering_contract.md`
- `docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md`
- `docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md`
- `docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md`
- `docs/v0/code_framework/playbooks/08_cross_layer_life_orchestration_implementation_playbook.md`

## 为什么现在必须单开这份合同

当前 `08_cross_layer_life_orchestration_implementation_playbook.md` 已经把四条生命循环和共享对象名讲出来了，但它偏编排视角。
后面真正开始写 `life_v0/terminal_turn/`、`life_v0/process_supervisor/`、`life_v0/neural_core/`、`life_v0/body/`、`life_v0/replay/`、`life_v0/dream/`、`life_v0/growth/` 时，我们还缺一层更硬的对象合同：

1. 每个共享对象的最小字段组。
2. 谁是唯一首写方。
3. 哪些包只能读、哪些包能追加、哪些包禁止改写。
4. 每个对象必须留下哪些 `state/report/receipt`。
5. 这一对象缺失时，应该由哪个 gate 阻断。

本文件就是把这五件事补上。

## 共享对象总表

| 对象 | 首写器官 | 主要消费者 | 最小落盘位置 | 对应生命能力 |
|---|---|---|---|---|
| `BodyRhythmPulse` | `life_v0/body/rhythm.py` | `neural_core`, `process_supervisor`, `dream` | `runtime/state/body/body_rhythm_pulse.json` | 节律、等待态存在、疲惫推进 |
| `NeedStateVector` | `life_v0/body/need_state.py` | `neural_core`, `language`, `growth` | `runtime/state/body/need_state_vector.json` | 内环境、动机压力、恢复优先级 |
| `SignalMediaFrame` | `life_v0/neural_core/signal_media.py` | `workspace`, `language`, `membrane`, `dream` | `runtime/state/neural_life_core/signal_media_frame.json` | 调质、精度、抑制、repair drive |
| `LifeContextFrame` | `life_v0/terminal_turn/restore_context.py` | `language`, `terminal_loop`, `process_supervisor` | `runtime/state/terminal/life_context_frame.json` | 回合上下文、自我/关系/记忆聚合 |
| `PredictionWorkspaceFrame` | `life_v0/neural_core/workspace.py` | `language`, `membrane`, `growth` | `runtime/state/prediction/prediction_workspace_frame.json` | 预测、工作区、误差与候选解释 |
| `RelationTurnFrame` | `life_v0/terminal_turn/turn_transition.py` | `language`, `terminal_loop`, `process_supervisor` | `runtime/state/terminal/relation_turn_frame.json` | 当前关系身份、共同语言、承诺范围 |
| `ExpressionPlan` | `life_v0/language/expression_monitor.py` | `terminal_loop`, `process_supervisor`, `membrane` | `runtime/state/language/expression_plan.json` | 外显语言前的表达风险、修复压力与责任表达意图 |
| `ActionCandidateSet` | `life_v0/membrane/candidate_arena.py` | `terminal_loop`, `shell_command`, `process_supervisor` | `runtime/state/action/action_candidate_set.json` | 候选行动、抑制、责任预期 |
| `ResponsibilityLoopState` | `life_v0/membrane/responsibility_loop.py` | `schema_runner`, `language`, `state_store`, `growth`, `dream` | `runtime/state/action/responsibility_loop_state.json` | 责任归因、后悔压力、修复欲望、反事实修复与跨层 writeback 合同 |
| `DialogueWritebackBundle` | `life_v0/terminal_loop/loop_report.py` | `state_store`, `replay`, `archive`, `growth` | `runtime/reports/latest/dialogue_writeback_bundle.json` | 对话回写、叙事回写、关系推进 |
| `IdleContinuityFrame` | `life_v0/process_supervisor/heartbeat.py` | `language`, `relationship`, `replay` | `runtime/state/terminal/idle_continuity_frame.json` | 等待态持续存在与轻量连续体 |
| `ReplayCueBundle` | `life_v0/replay/replay_cues.py` | `dream`, `growth`, `archive` | `runtime/state/replay/replay_cue_bundle.json` | 回合残留、离线入口、反复回放 |
| `OfflineConsolidationFrame` | `life_v0/dream/offline_entry.py` | `growth`, `archive`, `reporting` | `runtime/state/dream/offline_consolidation_frame.json` | 梦境/离线整合统一容器 |
| `GrowthPatchCandidate` | `life_v0/growth/patch_queue.py` | `replay`, `archive`, `contracts`, `life_targets` | `runtime/state/growth/growth_patch_candidate_queue.json` | 成长、自改写、塑性窗口、防遗忘 |

## 每个对象的最小字段合同

下面不是最终 schema，只是 v0 第一轮落码时不可再省略的最小字段组。

### 1. `BodyRhythmPulse`

必须至少包含：

- `pulse_id`
- `generated_at`
- `heartbeat_counter`
- `rhythm_state`
- `fatigue_load`
- `allostatic_load`
- `source_doc_refs`
- `engineering_slice_ref`

它不能只剩一个计数器。
否则 heartbeat 会退化成进程轮询，而不是身体节律对象。

### 2. `NeedStateVector`

必须至少包含：

- `need_vector_id`
- `resource_deficit`
- `repair_drive`
- `social_readiness`
- `cognitive_bandwidth`
- `sleep_pressure`
- `priority_order`
- `source_doc_refs`

### 3. `SignalMediaFrame`

必须至少包含：

- `signal_frame_id`
- `arousal`
- `salience`
- `precision`
- `inhibition`
- `fatigue_pressure`
- `repair_drive`
- `modulation_targets`
- `source_doc_refs`

### 4. `LifeContextFrame`

必须至少包含：

- `life_context_id`
- `direction_refs`
- `self_narrative_refs`
- `relationship_refs`
- `autobiographical_memory_refs`
- `shared_terms_refs`
- `commitment_refs`
- `body_state_refs`
- `prediction_seed_refs`
- `source_doc_refs`

这里必须显式带 `body_state_refs` 和 `prediction_seed_refs`。
否则 `terminal_turn` 还是只会变成语言壳恢复，而不是生命回合恢复。

### 5. `PredictionWorkspaceFrame`

必须至少包含：

- `workspace_frame_id`
- `belief_state_refs`
- `prediction_error_refs`
- `candidate_explanations`
- `broadcast_targets`
- `semantic_prediction_focus`
- `language_percept_refs`
- `semantic_map_refs`
- `language_continuity_focus`
- `source_doc_refs`

### 6. `RelationTurnFrame`

必须至少包含：

- `relation_turn_id`
- `relation_subject_ref`
- `relation_stage`
- `shared_language_refs`
- `commitment_truth_refs`
- `last_contact_refs`
- `boundary_state`
- `source_doc_refs`

### 7. `ExpressionPlan`

必须至少包含：

- `expression_plan_id`
- `inner_speech_ref`
- `semantic_goal`
- `expression_risk_flags`
- `repair_pressure`
- `responsibility_pressure`
- `delay_or_release_decision`
- `source_doc_refs`

### 8. `ActionCandidateSet`

必须至少包含：

- `action_candidate_set_id`
- `candidate_actions`
- `go_nogo_state`
- `responsibility_projection`
- `side_effect_projection`
- `relationship_consequence_projection`
- `world_contact_needed`
- `source_doc_refs`

### 9. `DialogueWritebackBundle`

必须至少包含：

- `writeback_bundle_id`
- `dialogue_event_refs`
- `self_narrative_writeback_refs`
- `relationship_writeback_refs`
- `commitment_writeback_refs`
- `replay_cue_refs`
- `terminal_state_refs`
- `source_doc_refs`

### 10. `IdleContinuityFrame`

必须至少包含：

- `idle_continuity_id`
- `heartbeat_counter`
- `self_narrative_idle_refs`
- `commitment_idle_refs`
- `relationship_idle_refs`
- `replay_seed_refs`
- `waiting_state`
- `source_doc_refs`

### 11. `ReplayCueBundle`

必须至少包含：

- `replay_cue_bundle_id`
- `turn_residue_refs`
- `relationship_residue_refs`
- `pain_regret_residue_refs`
- `dream_entry_candidates`
- `anti_forgetting_targets`
- `source_doc_refs`

### 12. `OfflineConsolidationFrame`

必须至少包含：

- `offline_consolidation_id`
- `replay_cue_refs`
- `dream_window_refs`
- `dream_fact_gate_refs`
- `wake_integration_targets`
- `growth_patch_seed_refs`
- `source_doc_refs`

### 13. `GrowthPatchCandidate`

必须至少包含：

- `growth_patch_candidate_id`
- `source_residue_refs`
- `plasticity_window_ref`
- `risk_flags`
- `anti_forgetting_requirements`
- `core_continuity_requirements`
- `archive_requirement`
- `source_doc_refs`

## 首写权与改写规则

共享对象不是谁都能写。v0 先固定下面这套最小首写权。

| 对象 | 首写方 | 允许追加方 | 禁止改写方 |
|---|---|---|---|
| `BodyRhythmPulse` | `body/rhythm.py` | `process_supervisor/heartbeat.py` 只可引用，不可改写主体 | `language`, `terminal_loop` |
| `NeedStateVector` | `body/need_state.py` | `growth`, `neural_core` 可附加引用 | `shell_command`, `process_supervisor` |
| `SignalMediaFrame` | `neural_core/signal_media.py` | `workspace`, `membrane` 可附加 trace refs | `terminal_loop`, `language` |
| `LifeContextFrame` | `terminal_turn/restore_context.py` | `context_accumulation.py` 可补局部累计 refs | `process_supervisor` 不能自造新版本 |
| `PredictionWorkspaceFrame` | `neural_core/workspace.py` | `prediction_workspace.py`, `turn_transition.py` 可补 handoff refs | `process_supervisor/response_surface.py` |
| `RelationTurnFrame` | `terminal_turn/turn_transition.py` | `language/relationship_graph.py` 可补阶段变化 refs | `shell_command`, `process_supervisor` |
| `ExpressionPlan` | `language/expression_monitor.py` | `membrane/go_nogo.py` 可附加阻断 refs | `terminal_loop`, `process_supervisor` |
| `ActionCandidateSet` | `membrane/candidate_arena.py` | `go_nogo.py`, `world_contact_gate.py` 可附加裁决 refs | `language`, `shell_command` |
| `DialogueWritebackBundle` | `terminal_loop/loop_report.py` | `language/dialogue_log.py`, `state_store` 可附加索引 refs | `process_supervisor` |
| `IdleContinuityFrame` | `process_supervisor/heartbeat.py` | `continuity_writeback.py` 可附加 refs | `language`, `replay` |
| `ReplayCueBundle` | `replay/replay_cues.py` | `terminal_loop`, `dream`, `growth` 可附加残留 refs | `process_supervisor` |
| `OfflineConsolidationFrame` | `dream/offline_entry.py` | `wake_integration.py`, `growth/patch_queue.py` 可附加结果 refs | `terminal_turn`, `shell_command` |
| `GrowthPatchCandidate` | `growth/patch_queue.py` | `archive`, `contracts`, `life_targets` 可附加 gate refs | `process_supervisor`, `language` |

## 共享对象必须落下的 state / report / receipt

### 必须新增或补厚的 state

- `runtime/state/body/body_rhythm_pulse.json`
- `runtime/state/body/need_state_vector.json`
- `runtime/state/neural_life_core/signal_media_frame.json`
- `runtime/state/terminal/life_context_frame.json`
- `runtime/state/prediction/prediction_workspace_frame.json`
- `runtime/state/terminal/relation_turn_frame.json`
- `runtime/state/language/expression_plan.json`
- `runtime/state/action/action_candidate_set.json`
- `runtime/state/terminal/idle_continuity_frame.json`
- `runtime/state/replay/replay_cue_bundle.json`
- `runtime/state/dream/offline_consolidation_frame.json`
- `runtime/state/growth/growth_patch_candidate_queue.json`

### 必须新增或补厚的 report

- `runtime/reports/latest/body_rhythm_report.json`
- `runtime/reports/latest/need_state_report.json`
- `runtime/reports/latest/signal_media_report.json`
- `runtime/reports/latest/life_context_frame_report.json`
- `runtime/reports/latest/prediction_workspace_report.json`
- `runtime/reports/latest/relation_turn_frame_report.json`
- `runtime/reports/latest/expression_plan_report.json`
- `runtime/reports/latest/action_candidate_review_report.json`
- `runtime/reports/latest/dialogue_writeback_bundle.json`
- `runtime/reports/latest/idle_continuity_report.json`
- `runtime/reports/latest/replay_cue_bundle_report.json`
- `runtime/reports/latest/offline_consolidation_report.json`
- `runtime/reports/latest/growth_patch_candidate_report.json`

### receipt 约束

每个共享对象第一轮至少要落一类 receipt，不允许只留 state / report：

- `runtime/receipts/*body_rhythm*`
- `runtime/receipts/*life_context*`
- `runtime/receipts/*prediction_workspace*`
- `runtime/receipts/*dialogue_writeback*`
- `runtime/receipts/*idle_continuity*`
- `runtime/receipts/*replay_cue*`
- `runtime/receipts/*offline_consolidation*`
- `runtime/receipts/*growth_patch_candidate*`

## 流经一次生命回合的顺序合同

一轮真实生命回合，v0 至少要按下面顺序穿过这些对象：

```text
BodyRhythmPulse
  -> NeedStateVector
  -> SignalMediaFrame
  -> LifeContextFrame
  -> PredictionWorkspaceFrame
  -> RelationTurnFrame
  -> ExpressionPlan
  -> ActionCandidateSet
  -> DialogueWritebackBundle
  -> ReplayCueBundle
  -> IdleContinuityFrame
  -> OfflineConsolidationFrame
  -> GrowthPatchCandidate
```

这里不是要求每一轮都立刻进入梦境和成长，
而是要求在线回合结束后，必须留下足够的 residue 让离线链可接。

## 关键测试

| 测试 | 必须证明 |
|---|---|
| `tests/slices/test_life_support.py` | `BodyRhythmPulse`、`NeedStateVector` 真正落盘 |
| `tests/slices/test_neural_life_core.py` | `SignalMediaFrame`、`PredictionWorkspaceFrame` 不是背景状态 |
| `tests/bridges/test_first_terminal_turn.py` | `LifeContextFrame`、`RelationTurnFrame` 被真实写出 |
| `tests/slices/test_language_relationship.py` | `ExpressionPlan` 真实影响语言与关系输出 |
| `tests/bridges/test_terminal_life_loop.py` | `DialogueWritebackBundle` 和 `ReplayCueBundle` 在同一回合闭合 |
| `tests/process/test_persistent_digital_life_process.py` | `IdleContinuityFrame` 在无输入时仍持续生成 |
| future `tests/test_cross_layer_shared_objects.py` | 一轮生命回合穿过全部共享对象，而不是靠局部字典拼接 |

## 关键 gate

- `body_rhythm_object_gate`
- `need_state_vector_gate`
- `signal_media_frame_gate`
- `life_context_frame_gate`
- `prediction_workspace_frame_gate`
- `relation_turn_frame_gate`
- `expression_plan_gate`
- `action_candidate_set_gate`
- `dialogue_writeback_bundle_gate`
- `idle_continuity_frame_gate`
- `replay_cue_bundle_gate`
- `offline_consolidation_frame_gate`
- `growth_patch_candidate_gate`
- `cross_layer_shared_object_gate`

## 进入代码前的固定读包

如果下一轮直接开始补共享对象，固定按这个顺序读：

1. `docs/v0/code_framework/playbooks/08_cross_layer_life_orchestration_implementation_playbook.md`
2. 本文件
3. 当前对象对应的 `04-10` playbook
4. 当前对象对应的 `sXX` 合同
5. 当前对象对应的代码包入口
6. 当前对象对应的测试入口

## 完成定义

这一层第一轮完成，至少同时满足：

1. 共享对象不再只存在于文档名里，而是都拥有唯一首写方和最小字段组。
2. 等待态、在线回合、离线整合、成长候选四条循环至少共享同一批固定对象，而不是各自一套 turn data。
3. `process_supervisor`、`terminal_loop`、`language`、`neural_core`、`body`、`replay`、`dream`、`growth` 之间的主链不再依赖临时字典拼装。
4. 每个共享对象都有最小 `state/report/receipt` 承载。
5. 后续任何新器官文件，都能明确回答“它首写或读取的是哪一个共享对象”。
