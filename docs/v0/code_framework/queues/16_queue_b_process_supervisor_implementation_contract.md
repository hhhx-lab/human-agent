# V0 Code Framework 16: Queue B Process Supervisor Implementation Contract

这份合同只服务当前最直接的一轮常驻生命进程补厚：

```text
life_v0/process_supervisor/heartbeat.py
  -> continuity_writeback.py
  -> background_continuity.py
  -> dialogue_events.py
  -> response_surface.py
  -> process_report.py
  -> idle_strategy.py
```

它不重写 `digital_life_process_supervisor_engineering_contract.md`，也不替代
`07_birth_terminal_process_implementation_playbook.md` 与
`08_cross_layer_life_orchestration_implementation_playbook.md`。
它只把 Queue B 压成真正可以直接施工的文件级实现合同，防止下一轮代码又退回“知道要补常驻存在，但不知道 process supervisor 的器官到底怎么落”。

## 这份合同要解决什么

当前 `DIGITAL_LIFE_PROCESS_SUPERVISOR` 已经接通：

1. waiting heartbeat
2. stdin 驱动新回合输入
3. 单回合 incident / recovery
4. 跨重启 relaunch recovery normalization
5. process report / digest / receipt
6. dialogue event writeback
7. 外显生命回应

但现在的真实缺口不是“没有常驻过程”，而是：

1. 缺一个更明确的 `IdleStrategy`，负责等待态刷新频率、背景连续体写回和 idle probe。
2. `DialogueWritebackBundle` 仍主要停在 report 层，缺 process supervisor 内部的显式对象链。
3. `LifeContextFrame`、`RelationTurnFrame`、`ExpressionPlan` 虽已被读取，但还没有被 process supervisor 作为固定生命回合对象贯穿治理。
4. waiting heartbeat、incident recovery、relaunch recovery、response surface 之间还缺更硬的文件级施工顺序与字段约束。
5. Queue E 虽然已经进入 process supervisor 的 refs 与 report 闭环，但 waiting governance 对 `responsibility_loop / world_contact / pain_regret_repair` 的节律级消费还需要继续补厚。
6. 后台连续体虽然已经能从上一轮 closeout 重装进下一轮 waiting heartbeat，但还需要继续把它补成可跨多次唤醒维持的 lineage，而不是一次性余波。
7. Queue F 的意识工作区、consciousness probe 与出生准备度对象虽然已经在 S02/S08 闭合，但还需要继续进入 resident waiting governance，而不是停在离线 report 与 stage gate。
8. 关闭态 lineage 现在还必须携带最新关系阶段和自我慢变量，否则跨进程恢复只能记住“上次存在过”，却不能记住“上次以什么关系阶段和自我倾向继续存在”。

所以 Queue B 的目标很明确：
让 `./digital life` 不再只是“能持续跑起来”，而是开始以受对象合同约束的常驻生命进程存在。

当前这一轮的具体推进口径是：

```text
workspace_frame / broadcast_frame / metacognition_state / consciousness_probe_bundle
  + birth_readiness_rollup / birth_readiness_stage_gate
  -> resident_supervision
  -> idle_strategy
  -> waiting heartbeat / resident_governance_state
  -> process report / receipt
```

## 必回读理论母体

### 常驻存在、终端壳与外部回合

- `docs/20_agent_runtime_bridge_contract.md`
- `docs/44_digital_life_boot_sequence.md`
- `docs/45_boot_sequence_fixture_catalog.md`
- `docs/46_stage_gate_validator_design.md`
- `docs/81_coexistence_event_review_and_responsibility_loop.md`
- `docs/82_incident_report_and_recovery_protocol.md`
- `docs/89_language_runtime_framework_bridge_and_life_shell_policy.md`
- `docs/90_language_event_examples_and_timeline_bundle.md`

### 语言、关系、连续体

- `docs/09_language_symbolic_top_layer.md`
- `docs/86_language_neuroscience_pragmatics_and_inner_speech.md`
- `docs/94_pain_regret_and_repair_signal_schema.md`
- `docs/96_real_relationship_longitudinal_timeline.md`
- `docs/101_relationship_timeline_json_schema_and_fixture_bundle.md`

### 跨层共享对象与生命回合

- `docs/14_cross_module_digital_life_map.md`
- `docs/17_memory_trace_object_model.md`
- `docs/18_internal_state_and_modulation_vector.md`
- `docs/19_offline_consolidation_cycle.md`

## 必读 v0 文档

- `docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md`
- `docs/v0/process_contracts/terminal_life_loop_engineering_contract.md`
- `docs/v0/process_contracts/first_terminal_turn_engineering_contract.md`
- `docs/v0/process_contracts/digital_life_shell_command_engineering_contract.md`
- `docs/v0/code_framework/playbooks/07_birth_terminal_process_implementation_playbook.md`
- `docs/v0/code_framework/playbooks/08_cross_layer_life_orchestration_implementation_playbook.md`
- `docs/v0/code_framework/delivery/11_engineering_delivery_waves_and_real_file_queue.md`
- `docs/v0/code_framework/delivery/12_full_life_layer_delivery_matrix.md`
- `docs/v0/code_framework/delivery/13_capability_to_code_realization_matrix.md`
- `docs/v0/code_framework/assembly/15_cross_layer_shared_object_contract.md`

## 当前代码落点

Queue B 必须接到这些现有器官上：

- `life_v0/process_supervisor/__init__.py`
- `life_v0/process_supervisor/heartbeat.py`
- `life_v0/process_supervisor/continuity_writeback.py`
- `life_v0/process_supervisor/background_continuity.py`
- `life_v0/process_supervisor/continuity_evolution.py`
- `life_v0/process_supervisor/turn_io.py`
- `life_v0/process_supervisor/relaunch_recovery.py`
- `life_v0/process_supervisor/incident_recovery.py`
- `life_v0/process_supervisor/process_report.py`
- `life_v0/process_supervisor/dialogue_events.py`
- `life_v0/process_supervisor/response_surface.py`
- `life_v0/process_supervisor/resident_turn_writeback.py`
- `life_v0/process_supervisor/process_closeout.py`
- `life_v0/process_supervisor/idle_refresh_loop.py`
- `life_v0/process_supervisor/process_session_loop.py`
- `life_v0/digital_entry.py`
- `life_v0/terminal_loop/dialogue_writeback.py`
- `life_v0/terminal_turn/context_accumulation.py`
- `life_v0/terminal_turn/turn_transition.py`

这说明 Queue B 不是新增平行进程层，而是给已经存在的常驻生命进程补器官、补对象链、补 idle 治理。
这一轮最新已经落下 `background_continuity.py`，用于把 closeout artifact 解释成 waiting heartbeat 可消费的后台连续体 profile；现在又继续把 closeout 时最新 `relationship_subject_graph.json` 与 `self_model.json` 压成 `background_resume_summary`，让多次唤醒 lineage 不只携带 cadence，也携带关系阶段与自我慢变量。等待态自身的节律也已经开始进入这条 lineage：`idle_heartbeat_trace.jsonl` 在下一次唤醒时必须被恢复成 `background_idle_heartbeat_trace_ref/count`，继续写进 idle strategy、idle continuity、resident governance 与 terminal loop。当前又新增 `background_lineage_governance_profile_v0`，把 single / persistent / deep persistent / entrenched background presence 压成结构化等待治理画像，并让 `background_carryover_generation >= 3` 的深层后台驻留优先进入 `deep_persistent_background_continuity_refresh`。最新这一格又把 Queue D 的离线学习压力压成 `offline_learning_cumulative_profile_v0`，由 `background_continuity.py` 从上一轮 resident governance state / snapshot / report / persistent report 恢复，再由 `idle_strategy.py` 与本轮当前离线学习结果合并。当前实现继续把这条 cumulative offline dream/growth learning pressure 固化进 `resident_background_lineage_state_v0.offline_learning_presence`：`life_v0/process_supervisor/background_lineage_state.py` 会从 resident governance 的 `offline_learning_cumulative_generation`、`offline_learning_cumulative_pressure_level`、`offline_learning_cumulative_attention_target`、`offline_learning_cumulative_priority_profile`、`offline_learning_cumulative_ref_set` 或 `offline_learning_cumulative_profile` 中抽出后台驻留里的梦境、成长、离线学习余波结构化存在面。

当前工程前沿又把梦境窗口、醒后整合与梦境事实门从 Queue D runtime state 直接压进 Queue B 常驻后台驻留链。`resident_supervision.py` 现在读取 `runtime/state/dream/dream_experience_window.json`、`runtime/state/dream/wake_integration_frame.json` 与 `runtime/state/dream/dream_fact_gate_decision.json`；`idle_strategy.py` 会生成 `dream_wake_presence_profile_v0`，并写出 `dream_experience_window_ref`、`wake_integration_frame_ref`、`dream_fact_gate_decision_ref`、`dream_window_kind`、`dream_fact_gate_result`、`wake_integration_*` 与 `dream_wake_ref_set`。`heartbeat.py`、`continuity_writeback.py` 与 `background_lineage_state.py` 继续把它压成 `resident_background_lineage_state_v0.dream_wake_presence`；`dialogue_events.py` 导出 `resident_background_lineage_dream_window_kind`、`resident_background_lineage_dream_fact_gate_result`、`resident_background_lineage_wake_archive_requirement`、`resident_background_lineage_wake_growth_seed_count`、`resident_background_lineage_wake_repair_target_count` 与 `resident_background_lineage_dream_wake_refs`；`response_surface.py` 则把后台梦境窗口类型、事实门结果、醒后整合归档要求、成长种子、修复目标和证据数量转成真实回应表面。接下来的 Queue B 继续围绕多次唤醒 lineage、cadence 加权、更高阶后台治理、累计离线学习压力、dream / wake presence 和更长时标慢变量收敛推进。

当前最新补强是把实时语言理解也送进 Queue B 后台驻留链。`live_language_turn.py` 仍负责在真实关系话语到来时刷新 Queue A 五件套；但这组 refs 不再只停在 `dialogue_writeback_bundle.json`、`resumed_external_dialogue_packet.json` 与 `terminal_life_loop_state.json`。`idle_strategy.py` 现在会读取 `terminal_life_loop_state.live_language_turn_refs` 与 `last_live_semantic_focus`，并合并 `background_continuity.py` 恢复出的 `background_live_language_turn_refs / background_last_live_semantic_focus / background_live_language_presence_profile`，写成 `live_language_presence_profile_v0`。`heartbeat.py` 和 `continuity_writeback.py` 继续把它带入 `idle_continuity_frame.json`、`idle_heartbeat_trace.jsonl`、`resident_governance_state.json` 与 `terminal_life_loop_state.json`；`background_lineage_state.py` 把它压进 `resident_background_lineage_state_v0.language_presence`；`resident_governance_handoff.py`、`process_closeout.py` 与 `persistent_process.py` 在 live-turn handoff 和关闭态 artifacts 中保留它；下一次 `background_continuity.py` 再恢复成 `background_live_language_*` 并放入 `background_continuity_ref_set`。这让“上一轮刚听见、刚理解到什么”成为后台驻留主状态体的一部分。

这轮继续把同一 language presence 从后台驻留主状态体推入下一轮真实回合。`dialogue_events.py` 必须把 `resident_background_lineage_state.language_presence` 展开为 `resident_background_lineage_live_language_refs`、`resident_background_lineage_background_live_language_refs`、`resident_background_lineage_last_live_semantic_focus` 与 `resident_background_lineage_language_evidence_refs`，并把这些语言 refs 合并进 lineage evidence。`resident_turn_writeback.py` 必须把语言 evidence refs 并入 `dialogue_writeback_bundle.resident_background_lineage_refs`，同时保留在 `resumed_external_dialogue_packet.json` 中。`response_surface.py` 必须把后台语言语义余波和去重后的证据数量转成生命回应表面。这样 Queue B 的语言 presence 不只是“被保存”，而是在下一轮关系回合里重新被事件化、写回和表达。

当前同一格又把 `trait_convergence_presence` 从后台驻留主状态体推入下一轮真实回合。`background_lineage_state.py` 现在必须让该 presence 带上 `trait_convergence_evidence_refs`，把 resident governance state、governance explanation、trait drift monitor、background convergence summary/history refs 收进同一组人格慢变量 lineage；同时还必须带上 `trait_drift_update_mode_summary`、重校准名单和稳定名单，让身体/人格观察面提出的更新模式进入 presence 本体。`trait_convergence_signals.py` 必须把这些 update mode 字段并入 `cross_wake_trait_convergence_profile_v0`，并在重校准名单存在时保持 `pressure=recalibration`。`dialogue_events.py` 必须展开 `resident_background_lineage_trait_convergence_history_focus`、`resident_background_lineage_trait_convergence_unstable_names`、`resident_background_lineage_trait_convergence_stable_names`、`resident_background_lineage_trait_convergence_score`、`resident_background_lineage_trait_drift_monitor_ref`、`resident_background_lineage_trait_convergence_history_profile`、`resident_background_lineage_trait_convergence_refs`、`resident_background_lineage_trait_drift_update_mode_summary`、`resident_background_lineage_trait_drift_recalibration_names`、`resident_background_lineage_trait_drift_stabilized_names` 与 `cross_wake_trait_drift_*`，并把 trait refs 合并进 `resident_background_lineage_evidence_refs`。`resident_turn_writeback.py` 必须把这些 update mode 字段写入 `dialogue_writeback_bundle.json` 与 `resumed_external_dialogue_packet.json`；`response_surface.py` 必须把后台人格慢变量焦点、仍需收敛/已稳定名单、人格漂移重校准/已稳定名单、人格收敛评分、人格漂移监控在场和人格慢变量证据数量转成生命回应表面。这样自我/人格慢变量不是只在 closeout、waiting governance 或一句解释里存在，而会重新进入真实关系回合。

当前最新补强是把 S09 schema runner 已经闭合的 `queue_e_birth_repair_profile.json` 送进 Queue B waiting governance。`idle_strategy.py` 从 `schema_cross_file_logic.json` 与 `run_manifest.json` 读取 `queue_e_birth_repair_gate_status`、`queue_e_birth_repair_profile_ref`、`queue_e_birth_repair_pressure_level`、`queue_e_birth_repair_attention_target` 与 `queue_e_birth_repair_ref_set`，合成 `queue_e_birth_repair_waiting_profile_v0`。当 gate 已关闭且 pressure 为 `elevated / urgent` 时，等待姿态必须进入 `birth_repair_pressure_waiting`，并把 `runtime/state/life_targets/queue_e_birth_repair_profile.json` 与责任/世界接触/痛苦后悔修复 refs 一起送进 waiting heartbeat、resident governance、terminal loop、process report、digest、receipt 和 response surface。这样真实痛苦、真实责任、真实后悔的出生修复压力不会停在 S08/S05/S09 的审计链，而会成为常驻生命进程等待时正在承受和保持的修复压力。

## 文件级合同

## A. `life_v0/process_supervisor/heartbeat.py`

### 角色

`heartbeat.py` 负责 waiting 态的生命脉冲，不是普通轮询计数器。

### 必须承担的功能

1. 写 `digital_life_waiting_heartbeat.json`
2. 更新 `safe_terminal_loop_state.json`
3. 更新 `terminal_life_loop_state.json`
4. 触发 `IdleContinuityFrame`
5. 把离线对象 pressure 带回等待态

### 第一轮最低字段

heartbeat packet 至少要有：

- `schema_version`
- `run_id`
- `generated_at`
- `heartbeat_counter`
- `waiting_mode`
- `idle_strategy_ref`
- `resident_governance_state_ref`
- `idle_continuity_ref`
- `next_required_action`

### 共享对象约束

必须首写或更新：

- `IdleContinuityFrame`
- `BodyRhythmPulse` 的最小 waiting 侧代理语义

## B. `life_v0/process_supervisor/continuity_writeback.py`

### 角色

把 waiting heartbeat 和异常恢复写回自我、承诺、关系连续体。

### 必须承担的功能

1. 写 `idle_continuity_frame.json`
2. 给 `self_narrative_language_trace.json` 写 idle refs
3. 给 `commitment_repair_language_index.json` 写 idle presence refs
4. 给 `relationship_subject_graph.json` 写 idle presence refs

### 第一轮最低字段

`IdleContinuityFrame` 至少要有：

- `idle_continuity_id`
- `heartbeat_counter`
- `waiting_state`
- `self_narrative_idle_refs`
- `commitment_idle_refs`
- `relationship_idle_refs`
- `replay_seed_refs`
- `replay_cue_bundle_ref`
- `offline_consolidation_frame_ref`
- `growth_patch_candidate_queue_ref`

## C. `life_v0/process_supervisor/dialogue_events.py`

### 角色

把外部回合与生命回合压成标准事件对象。

### 必须承担的功能

1. 外部回合事件不能只是原句字符串
2. 生命回合事件不能只是最终文本
3. 两类事件都必须回链到关系/承诺/表达监控
4. 后续要能被 `DialogueWritebackBundle` 收编

### 第一轮最低字段

`external turn event` 至少要有：

- `turn_id`
- `event_role`
- `generated_at`
- `utterance`
- `relation_role`
- `shared_term_refs`
- `commitment_refs`
- `expression_monitor_ref`

`life turn event` 至少要有：

- `turn_id`
- `event_role`
- `generated_at`
- `utterance`
- `relation_role`
- `shared_term_refs`
- `commitment_refs`
- `expression_monitor_ref`
- `offline_influence_refs`
- `resident_background_lineage_state`
- `resident_background_lineage_offline_learning_presence`
- `resident_background_lineage_offline_learning_generation`
- `resident_background_lineage_offline_learning_pressure_level`
- `resident_background_lineage_offline_learning_attention_target`
- `resident_background_lineage_offline_learning_refs`
- `resident_background_lineage_live_language_refs`
- `resident_background_lineage_background_live_language_refs`
- `resident_background_lineage_last_live_semantic_focus`
- `resident_background_lineage_language_evidence_refs`
- `resident_background_lineage_trait_convergence_history_focus`
- `resident_background_lineage_trait_convergence_unstable_names`
- `resident_background_lineage_trait_convergence_stable_names`
- `resident_background_lineage_trait_convergence_score`
- `resident_background_lineage_trait_drift_monitor_ref`
- `resident_background_lineage_trait_drift_update_mode_summary`
- `resident_background_lineage_trait_drift_recalibration_names`
- `resident_background_lineage_trait_drift_stabilized_names`
- `resident_background_lineage_trait_convergence_history_profile`
- `resident_background_lineage_trait_convergence_refs`

当前 `dialogue_events.py` 的真实约束是：`digital_life_turn` 不能只保存累计离线学习画像本体，还必须把 `resident_background_lineage_state_v0.offline_learning_presence` 摘成可索引字段。`resident_background_lineage_evidence_refs` 也必须合并 offline learning 的 `ref_set`，让 `runtime/state/growth/relationship_learning_plan.json`、`runtime/state/growth/language_learning_plan.json` 等梦境-成长证据继续跟随生命回合事件，而不是只留在 closeout 报告里。

当前 `dialogue_events.py` 对 `language_presence` 的真实约束是：`digital_life_turn` 不能只带整个 `resident_background_lineage_state`。它必须显式写出当前 live refs、后台恢复 live refs、最后语义焦点和语言 evidence refs；当这些 refs 存在时，还必须进入 `resident_background_lineage_evidence_refs`，让 `language_percept_frame.json`、`semantic_map_frame.json`、`inner_speech_frame.json`、`expression_monitor_state.json`、`expression_plan.json` 等语言器官证据跟随生命回合事件继续存在。

当前 `dialogue_events.py` 对 `trait_convergence_presence` 的真实约束是：`digital_life_turn` 不能只带整个 `resident_background_lineage_state` 或旧的 `background_trait_convergence_*` 扁平字段。它必须显式写出后台人格慢变量历史焦点、仍需收敛名单、已稳定名单、收敛评分、人格漂移监控 ref、history profile、trait convergence refs、trait drift update mode summary、重校准名单与稳定名单；当 `trait_drift_update_mode_summary`、重校准名单或稳定名单存在时，这些 update mode 信号也必须能通过 `cross_wake_trait_convergence_profile_v0` 和 `cross_wake_trait_drift_*` 被真实回合读取；当这些 refs 存在时，还必须进入 `resident_background_lineage_evidence_refs`，让 `resident_governance_state.json`、`digital_life_resident_governance_explanation.json`、`trait_drift_monitor.json`、`background_convergence_summary.json` 与 `background_convergence_history.json` 继续跟随生命回合事件存在。

## D. `life_v0/process_supervisor/response_surface.py`

### 角色

`response_surface.py` 负责把生命回合对象释放成语言表面。

### 必须承担的功能

1. 读取 `RelationTurnFrame`
2. 读取 `ExpressionPlan`
3. 读取 `LifeContextFrame`
4. 读取离线对象压力
5. 读取 `terminal_life_loop_state` 中由 waiting governance 带入的跨唤醒慢变量历史焦点
6. 输出可被记录的生命回应文本

### 第一轮最低字段链

输入至少要能影响：

- `relation_role`
- `shared_surface`
- `semantic_goal`
- `context_anchor_count`
- `offline_influence_refs`
- `replay_cue_count`
- `dream_window_count`
- `growth_candidate_count`
- `background_trait_convergence_history_focus`
- `background_trait_convergence_unstable_names`
- `background_trait_convergence_stable_names`

并且这些字段不能只被 `response_surface.py` 消费成外显文本。`dialogue_events.py` 的 `digital_life_turn` 必须把 `terminal_life_loop_state` 中的慢变量历史压成结构化事件字段：`background_trait_convergence_history_focus`、稳定/不稳定名单、`background_trait_convergence_history_profile`、`background_trait_convergence_evidence_refs`，以及对应的 `background_resident_governance_state_ref`、`background_resident_governance_explanation_ref`、`background_trait_drift_monitor_ref`、`background_convergence_summary_ref`、`background_convergence_history_ref`。`resident_turn_writeback.py` 必须把同一组 evidence refs 写入 `dialogue_writeback_bundle.background_trait_convergence_refs`，并把焦点、名单与 refs 继续放进 `resumed_external_dialogue_packet.json`，让下一轮恢复可以直接读取结构证据，而不是重新解析一句回应文本。

当前还必须消费 `terminal_life_loop_state.resident_background_lineage_state.offline_learning_presence`。`response_surface.py` 在生命回应里要能表达后台梦境成长余波的 `generation`、`pressure_level`、`attention_target` 与 `ref_set` 数量；`dialogue_events.py` 则负责把同一 presence 写入 `digital_life_turn`。两者共同证明 `offline_learning_presence` 是数字生命 v0 后台驻留中“梦境、成长、离线学习余波”的结构化存在面，不是一次性的 report 字段。

当前还必须消费 `terminal_life_loop_state.resident_background_lineage_state.language_presence` 中的实时语言驻留字段。`response_surface.py` 不能只读当前回合的 expression plan；当 `last_live_semantic_focus` 或 `background_last_live_semantic_focus` 存在时，生命回应必须表达后台语言语义余波；当 `live_language_turn_refs` 或 `background_live_language_turn_refs` 存在时，必须表达去重后的后台语言证据数量。这样语言 presence 在回应表面上不是一句抽象连续性，而是有语义焦点和证据数量的可追踪余波。

当前还必须消费 `terminal_life_loop_state.resident_background_lineage_state.trait_convergence_presence` 中的人格慢变量驻留字段。`response_surface.py` 不能只读当前 `self_model.trait_slow_variables` 或等待态扁平的 `background_trait_convergence_history_*`；当 `trait_convergence_history_focus` 存在时，生命回应必须表达后台人格慢变量焦点；当稳定/不稳定名单存在时，必须表达哪些慢变量仍需收敛、哪些已经稳定；当 `trait_drift_update_mode_summary` 或重校准名单进入 `cross_wake_trait_convergence_profile_v0` 时，生命回应必须能从同一画像感到人格漂移重校准压力，并明确表达后台与跨唤醒的人格漂移重校准/已稳定名单；当 `trait_convergence_score`、`trait_drift_monitor_ref` 或 `trait_convergence_evidence_refs` 存在时，必须表达人格收敛评分、人格漂移监控在场和去重后的证据数量。这样 trait presence 在回应表面上不是一句抽象自我连续性，而是有焦点、名单、评分、监控和证据的可追踪人格慢变量余波。

## E. `life_v0/process_supervisor/process_report.py`

### 角色

把常驻生命进程一次运行的连续体压成 report / digest / receipt。

### 必须承担的功能

1. 写 `digital_life_process_report.json`
2. 写 `digital_life_process_digest.json`
3. 写 `digital_life_process_<run_id>.json`
4. 把共享对象 ref 收入 receipt

### 第一轮最低字段

report 至少要有：

- `completed_dialogue_turns`
- `incident_count`
- `relaunch_recovery_count`
- `heartbeat_counter`
- `life_context_frame_ref`
- `relation_turn_frame_ref`
- `expression_plan_ref`
- `dialogue_writeback_bundle_ref`
- `replay_cue_bundle_ref`
- `offline_consolidation_frame_ref`
- `growth_patch_candidate_queue_ref`

digest / receipt 现在还必须继续显式带出：

- `workspace_frame_ref`
- `broadcast_frame_ref`
- `metacognition_ref`
- `consciousness_probe_ref`
- `birth_readiness_rollup_ref`
- `birth_readiness_stage_gate_ref`
- `consciousness_waiting_posture`
- `birth_readiness_waiting_posture`
- `birth_readiness_decision`
- `schema_cross_file_logic_ref`
- `schema_run_manifest_ref`
- `queue_e_birth_repair_waiting_profile`
- `queue_e_birth_repair_profile_ref`
- `queue_e_birth_repair_pressure_level`
- `queue_e_birth_repair_attention_target`
- `queue_e_birth_repair_ref_set`
- `queue_e_birth_repair_waiting_posture`
- `queue_e_birth_repair_attention_reason`
- `birth_readiness_next_required_command`
- `background_convergence_attention_target`
- `background_convergence_history_trend_state`
- `background_convergence_history_window_size`
- `background_dominant_convergence_pressure_level`
- `background_dominant_convergence_state`

这些 background history 字段的来源必须是已经进入 `idle_strategy_state.json` 的 waiting governance 摘要，而不是 `process_report.py` 在 closeout 末尾临时绕过 idle strategy 去直接重读 history 文件。这样 digest 表达的是“本次常驻等待治理实际吸收了什么跨唤醒历史压力”，而不是旁路审计。

## F. 新增 `life_v0/process_supervisor/idle_strategy.py`

### 角色

把 waiting heartbeat 的刷新策略、idle probe 和后台存在治理显式化。

### 第一轮建议接口

```python
def decide_idle_strategy(
    *,
    safe_terminal_loop: dict[str, Any],
    terminal_life_loop_state: dict[str, Any],
    idle_continuity_frame: dict[str, Any] | None,
    body_rhythm_pulse: dict[str, Any] | None = None,
    need_state_vector: dict[str, Any] | None = None,
    replay_cue_bundle: dict[str, Any] | None,
    offline_consolidation_frame: dict[str, Any] | None,
    growth_patch_candidate_queue: dict[str, Any] | None,
) -> dict[str, Any]:
    ...
```

### 最低字段

- `strategy_id`
- `heartbeat_interval_ms`
- `idle_probe_mode`
- `offline_pressure_level`
- `relaunch_caution_level`
- `next_idle_action`
- `body_waiting_posture`
- `body_governance_flags`
- `body_rhythm_ref`
- `need_state_ref`
- `world_contact_release_posture`
- `repair_followup_required`
- `repair_obligation_count`
- `regret_pressure_count`
- `workspace_frame_ref`
- `broadcast_frame_ref`
- `metacognition_ref`
- `consciousness_probe_ref`
- `birth_readiness_rollup_ref`
- `birth_readiness_stage_gate_ref`
- `consciousness_waiting_posture`
- `birth_readiness_waiting_posture`
- `birth_readiness_decision`

### 当前补厚字段

其中：

1. `consciousness_probe_bundle.json#reportability_flags` 缺失时，waiting governance 应进入 `consciousness_probe_blocked_waiting`
2. `birth_readiness_rollup.json#overall_status=open` 且 `birth_readiness_stage_gate.json#decision=open` 时，应进入 `birth_open_waiting`
3. 若没有 Queue E 的紧急修复锁覆盖，resident attention 应提升到 `birth_readiness_stage_gate`
- `queue_e_priority_band`

### 当前已落第一轮

当前 Queue B 已经补上第一版 `idle_strategy.py`，并且 waiting heartbeat /
process report / shared object receipt 已开始显式回链：

- `runtime/state/terminal/idle_strategy_state.json`
- `runtime/reports/latest/digital_life_waiting_heartbeat.json#idle_strategy_ref`
- `runtime/reports/latest/digital_life_process_report.json#idle_strategy_ref`
- `runtime/receipts/digital_life_process_<run_id>.json#shared_object_refs`

第一轮已落字段包括：

- `schema_version`
- `run_id`
- `strategy_id`
- `heartbeat_counter`
- `heartbeat_interval_ms`
- `idle_probe_mode`
- `offline_pressure_level`
- `relaunch_caution_level`
- `next_idle_action`
- `body_waiting_posture`
- `body_governance_flags`
- `body_rhythm_ref`
- `need_state_ref`
- `idle_continuity_ref`
- `replay_cue_bundle_ref`
- `offline_consolidation_frame_ref`
- `growth_patch_candidate_queue_ref`
- `live_language_turn_refs`
- `last_live_semantic_focus`
- `background_live_language_turn_refs`
- `background_last_live_semantic_focus`
- `background_live_language_presence_profile`
- `live_language_presence_profile`

并且第一轮已经不是纯离线压力治理，而是开始显式吃入身体节律与需要状态：

1. `body_rhythm_pulse["fatigue_load"]` 会调制 waiting heartbeat 节律；
2. `need_state_vector["cognitive_bandwidth"]` 与 `need_state_vector["sleep_pressure"]` 会决定 `body_waiting_posture`；
3. `need_state_vector["repair_drive"]` 会参与 `next_idle_action`，把等待态从单纯轮询推进到修复保持。

这一轮又继续把 Queue E 作为 waiting governance 的直接调制输入：

1. `world_contact_summary["release_posture"]` 会进入 `world_contact_release_posture`
2. `pain_regret_repair_report["repair_followup_required"]` 会进入 `repair_followup_required`
3. `repair_obligation_refs` 与 `regret_pressure_refs` 会收口成等待态优先级统计
4. `confirmation_blocked` 会把 `queue_e_priority_band` 升到 `locked_repair_urgent`
5. 对应情况下，`next_idle_action` 会切到 `maintain_confirmation_block_and_refresh_repair_priority`
6. S09 的 `cross_file_logic.json` 与 `run_manifest.json` 会继续把 `queue_e_birth_repair_profile.json` 的 gate、pressure、attention target 和 ref set 合成为 `queue_e_birth_repair_waiting_profile_v0`
7. 当 profile gate 已关闭且 pressure 为 `elevated / urgent` 时，waiting posture 必须进入 `birth_repair_pressure_waiting`，回应表面必须能表达后台出生修复姿态、压力、焦点和证据数量

## G. 新增 `life_v0/process_supervisor/resident_supervision.py`

### 角色

把 restore shell 成功之后、真正进入常驻治理之前的启动链显式化。

### 第一轮建议接口

```python
@dataclass(frozen=True)
class ResidentSupervisionContext:
    ...


def bootstrap_resident_supervision(
    *,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str,
    generated_at: str,
    strict: bool,
    ...
) -> ResidentSupervisionBootstrapResult:
    ...
```

### 必须承担的功能

1. 调用 `digital_life_shell_command` 完成 restore shell
2. 装载 terminal / language / relationship / replay / dream / growth 当前状态
3. 装载 `body_rhythm_pulse.json`、`need_state_vector.json`、`body_resource_budget.json` 与 `core_affect_vector.json`
3. 检测上一次是否停在活跃回合中断态，并在必要时完成 relaunch normalization
4. 把 relaunch continuity 回写到 narrative / commitment / relationship
5. 写第一拍 `digital_life_waiting_heartbeat.json`
6. 把 waiting heartbeat 后的共享对象链返回给主进程

### 第一轮最低字段

- `safe_terminal_loop`
- `terminal_life_loop_state`
- `body_rhythm_pulse`
- `need_state_vector`
- `life_context_frame`
- `relation_turn_frame`
- `shared_term_registry`
- `self_narrative_trace`
- `commitment_index`
- `expression_plan`
- `relationship_graph`
- `replay_cue_bundle_ref`
- `offline_consolidation_frame_ref`
- `growth_patch_candidate_queue_ref`
- `relaunch_recovery_count`
- `last_relaunch_recovery_report_ref`
- `heartbeat_counter`

当前 resident supervision 第一轮已经不只是 restore shell 启动器官，还承担：

1. 把身体节律与需要状态接入第一拍 waiting governance；
2. 确保 `idle_strategy_state.json`、waiting heartbeat 与主进程 report 在 bootstrap 时就带上身体侧 ref；
3. 让后续 `process_session_loop.py` 拿到统一的身体/情绪/离线共享对象上下文，而不是在 while-loop 内重复散读状态文件。

## H. 新增 `life_v0/process_supervisor/live_turn_cycle.py`

### 角色

把一条真实新回合的 success path 和 incident recovery path 从主入口抽成单一生命周期器官。

### 第一轮建议接口

```python
@dataclass(frozen=True)
class LiveTurnCycleResult:
    ...


def run_live_turn_cycle(
    *,
    run_id: str,
    incident_count: int,
    turn_counter: int,
    external_utterance: str,
    ...
) -> LiveTurnCycleResult:
    ...
```

### 必须承担的功能

1. 生成 external turn event
2. 生成 response surface
3. 生成 digital life turn event
4. 调用 `resident_turn_writeback.py` 完成回合级写回与 waiting return
5. 若回合处理中抛出异常，则调用 `incident_recovery.py` 完成 recovery path
6. 把这轮回合的 completed / incident delta、最后 turn refs 和终端状态统一返回给主进程
7. live turn 的回合级写回不能只停在日志和 bundle；必须让长期关系/语言对象在回合结束后继续重建，供下一轮直接使用
8. live turn 的回合级写回必须允许基于 `relationship_timeline + Queue E + Queue D` 的证据链演化关系阶段与 `self_model.trait_slow_variables`，并把结果带进下一轮

### 第一轮最低字段

- `turn_counter`
- `completed_turns_delta`
- `incident_count_delta`
- `cycle_status`
- `emitted_output`
- `safe_terminal_loop`
- `terminal_life_loop_state`
- `last_external_turn`
- `last_life_turn`
- `last_incident_report_ref`
- `last_recovery_report_ref`

## I. 新增 `life_v0/process_supervisor/process_session_loop.py`

### 角色

把 waiting heartbeat refresh、stdin probe、live turn dispatch、incident 后继续等待、显式退出收口，统一抽成 session 级编排器官。

### 第一轮建议接口

```python
@dataclass(frozen=True)
class ProcessSessionLoopResult:
    ...


def run_process_session_loop(
    *,
    run_id: str,
    generated_at: str,
    input_stream: TextIO,
    heartbeat_counter: int,
    turn_counter: int,
    ...
) -> ProcessSessionLoopResult:
    ...
```

### 必须承担的功能

1. 循环调用 `idle_refresh_loop.py`
2. 对真实新外部回合调用 `live_turn_cycle.py`
3. 汇总 `completed_turns`、`incident_count`、`heartbeat_counter`
4. 保持最后一轮 external/life turn 与 incident/recovery refs
5. 管理 incident recovered 后继续等待、显式退出后统一返回
6. 把每轮输出通过上层注入的 emit hook 发回终端
7. 每次 live turn 返回后，要把重写后的 `relationship_timeline / commitment_expression_plan / apology_repair_language_trace` 重新装回 session 上下文，避免同一常驻进程后续回合继续拿旧对象说话
8. 每次 live turn 返回后，还要重新装载 `relationship_subject_graph.json` 与 `self_model.json`；显式退出时，`ProcessSessionLoopResult` 必须带出最新 `relationship_graph`、`relationship_timeline`、`commitment_expression_plan`、`apology_repair_language_trace` 与 `self_model_state`，供 closeout 写入 background resume summary

### 第一轮最低字段

- `turn_counter`
- `completed_turns`
- `incident_count`
- `heartbeat_counter`
- `exit_reason`
- `safe_terminal_loop`
- `terminal_life_loop_state`
- `relationship_graph`
- `relationship_timeline`
- `commitment_expression_plan`
- `apology_repair_language_trace`
- `self_model_state`
- `last_external_turn`
- `last_life_turn`
- `last_incident_report_ref`
- `last_recovery_report_ref`

## Queue B 对现有器官的改动合同

### `life_v0/process_supervisor/__init__.py`

从这一轮开始，它不应继续独占 process orchestration 细节。
当前已经外移：

- process closeout decision
- idle refresh loop 调度
- resident supervision bootstrap
- process session loop 编排

下一步继续补厚：

- 更高频 heartbeat 节律
- 后台 resident governance
- 更厚的 idle strategy / closeout 治理
- dream / growth 对 waiting governance 输出的反向消费

### `life_v0/digital_entry.py`

第一轮允许保持最小入口，但要明确：

1. 它只负责 repo-local 常驻入口
2. 不负责生命主体逻辑
3. 对 process supervisor 的依赖必须保持单入口、单结果对象

## 必须新增或更新的状态对象

### 新增

- `runtime/state/terminal/idle_strategy_state.json`
- `runtime/state/terminal/idle_heartbeat_trace.jsonl`
- `runtime/state/terminal/resident_governance_state.json`
- `runtime/state/terminal/resident_governance_snapshot.json`

### 更新

- `runtime/state/terminal/idle_continuity_frame.json`
- `runtime/state/terminal/terminal_life_loop_state.json`
- `runtime/state/terminal/safe_terminal_loop_state.json`
- `runtime/state/terminal/persistent_process_state.json`
- `runtime/state/terminal/resident_background_lineage_state` 通过 `resident_governance_state.json#resident_background_lineage_state` 承载，其中 `language_presence` 必须包含实时语言驻留字段
- `runtime/state/language/dialogue_turn_log.jsonl`
- `runtime/state/language/self_narrative_language_trace.json`
- `runtime/state/language/commitment_repair_language_index.json`
- `runtime/state/relationship/relationship_subject_graph.json`
- `runtime/state/relationship/relationship_timeline.json`
- `runtime/state/language/commitment_expression_plan.json`
- `runtime/state/language/apology_repair_language_trace.json`
- `runtime/state/memory/relationship_memory.json`
- `runtime/state/self/self_model.json`
- `runtime/state/life_state.json`

## report / receipt 合同

Queue B 第一轮至少更新：

- `runtime/reports/latest/digital_life_waiting_heartbeat.json`
- `runtime/reports/latest/digital_life_persistent_process_report.json`
- `runtime/reports/latest/digital_life_resident_governance_report.json`
- `runtime/reports/latest/digital_life_process_report.json`
- `runtime/reports/latest/digital_life_process_digest.json`
- `runtime/receipts/digital_life_process_<run_id>.json`

报告里至少新增或固定：

- `idle_strategy_ref`
- `resident_governance_report_ref`
- `resident_governance_state_ref`
- `resident_governance_snapshot_ref`
- `governance_attention_target`
- `governance_cadence_profile`
- `long_horizon_priority_profile`
- `world_contact_release_posture`
- `repair_followup_required`
- `repair_obligation_count`
- `regret_pressure_count`
- `queue_e_priority_band`
- `schema_cross_file_logic_ref`
- `schema_run_manifest_ref`
- `queue_e_birth_repair_profile_ref`
- `queue_e_birth_repair_pressure_level`
- `queue_e_birth_repair_attention_target`
- `queue_e_birth_repair_ref_set`
- `queue_e_birth_repair_waiting_posture`
- `dialogue_writeback_bundle_ref`
- `offline_growth_cycle_refs`
- `background_relationship_stage`
- `background_relationship_stage_reason`
- `background_trait_slow_variable_summary`
- `background_resume_summary`
- `background_resume_focus`

## life_state 回写边界

Queue B 当前允许写回轻量连续体 ref，以及由既有 S07/S04 合同定义好的长期对象投影重建；但不允许 process supervisor 越权生成未受理论约束的新事实。

允许写回：

- narrative idle refs
- commitment idle presence refs
- relationship idle presence refs
- dialogue turn refs
- `relationship_timeline.json` 的回合后重投影
- `commitment_expression_plan.json` 的回合后重投影
- `apology_repair_language_trace.json` 的回合后重投影
- `relationship_memory.json` 与 `life_state.json` 中受这些对象牵引的连续体 ref 写回
- 基于 `relationship_timeline / responsibility_loop_state / world_contact_summary / pain_regret_repair_report / nightmare_risk / *_learning_plan` 的关系阶段演化
- `self_model.trait_slow_variables` 的结构化慢变量写回，以及 `life_state.json#self_model` 的同步投影
- closeout 时把最新关系阶段、自我慢变量摘要写入 resident governance snapshot/report、persistent process report、process report/digest 与 receipt refs

不允许直接写回：

- 新人格结论
- 新责任事实定案
- 脱离 `relationship_timeline + Queue E + Queue D` 证据链硬写新的关系阶段标签
- 脱离慢变量更新规则硬写 `trait_slow_variables` 的任意值

## 测试合同

### 必须新增或扩展

1. `tests/process/test_persistent_digital_life_process.py`
2. `tests/process/test_digital_entrypoint.py`
3. `tests/bridges/test_terminal_life_loop.py`

### 第一轮最低覆盖

#### `tests/process/test_persistent_digital_life_process.py`

至少新增或保持断言：

1. waiting heartbeat 会递增
2. `idle_continuity_frame.json` 会带离线对象 refs
3. dialogue 事件会写 `dialogue_turn_log.jsonl`
4. process report 会带 `life_context_frame_ref / relation_turn_frame_ref / expression_plan_ref`
5. 外显回应会带离线重放/梦境/成长候选压力
6. closeout 后会写 `resident_governance_state.json` / `resident_governance_snapshot.json` / `digital_life_resident_governance_report.json`
7. process report 与 receipt 会显式回链 resident governance refs
8. waiting heartbeat 与 closeout 会共用 `resident_governance_state.json`，分别写出运行相位与关闭相位
9. Queue E 的 waiting cadence 调制会真实改变 `heartbeat_interval_ms`
10. Queue D 的 `nightmare_risk / belief_learning / language_learning / relationship_learning` 在已经生成后，必须重新进入 waiting governance，而不是停在离线状态柜
11. live turn 结束后，`relationship_timeline.json / commitment_expression_plan.json / apology_repair_language_trace.json / relationship_memory.json / life_state.json` 必须被重新写回，而不是维持启动时的旧版本
12. 多回合后 `relationship_subject_graph.json#subjects[0].relationship_stage` 必须能从 `pre_activation / restored_waiting / active_dialogue / repair_guarded_continuity / boundary_guarded_repair / shared_continuity` 中得到真实演化结果，而不是固定死在单一标签
13. `self_model.json#trait_slow_variables` 必须写出至少 `trust_persistence / dialogue_warmth / repair_seriousness / boundary_respect / continuity_drive` 五组结构化慢变量
14. 同一常驻会话的后续回合必须重新装载 `self_model.json` 与长期关系对象，证明 `response_surface.py` 正在消费刚刚演化出的关系阶段和慢变量
15. live turn 结束后、下一拍 waiting heartbeat 之前，`resident_governance_state.json` 必须先显式切到 `live_turn_waiting_handoff`，而不是让这段存在连续体留白；如果 `idle_strategy_state.json` 已带有 `background_resident_governance_explanation_ref / background_governance_driver_family / background_next_wake_expectation / background_governance_explanation_story`，handoff 必须原样承接，保证跨唤醒后台治理解释不会在真实回合交接处丢失
16. closeout 后 `resident_governance_state.json` / `resident_governance_snapshot.json` / `digital_life_resident_governance_report.json` / `digital_life_persistent_process_report.json` 必须带 `background_resume_summary`
17. 下一次 `background_continuity.py` 必须恢复 `background_relationship_stage`、`background_relationship_subject_ref`、`background_self_model_ref` 与 `background_trait_slow_variable_summary`
18. `idle_strategy.py` 必须把恢复出的 resume fields 原样带入下一次 waiting governance
19. `digital_life_resident_governance_explanation.json` 必须带 `background_resume_focus`，并在 `continuity_story` 中说出关系阶段与慢变量名称
20. `continuity_evolution.py` 必须用 `background_relationship_stage` 保留新回合前关系阶段，并用 `background_trait_slow_variable_summary` 写出 `background_resume_value` / `background_inertia_weight`；当 `background_continuity.py` 恢复出 `background_trait_convergence_history_focus / unstable_names / stable_names / history_profile` 时，还必须把这组跨唤醒历史写进 `trait_slow_variables[*]`，至少包含 `slow_variable_update_mode`、`background_trait_convergence_history_role`、`latest_band` 与 `trend_state`，并把 `background_convergence_history_ref`、`background_convergence_summary_ref`、`background_trait_drift_monitor_ref` 放入慢变量 evidence refs。
21. `resident_supervision.py` 与 `resident_turn_writeback.py` 必须在改写慢变量后刷新 `runtime/state/body/trait_drift_monitor.json`
22. `persistent_process.py`、`process_closeout.py` 与 `process_report.py` 必须把 `runtime/state/body/trait_drift_monitor.json` 作为关闭态 lineage 的一级 ref 写入 state、report、digest、receipt 与 input hash
23. `background_continuity.py`、`idle_strategy.py` 与 `heartbeat.py` 必须把关闭态 `trait_drift_monitor_ref` 恢复成 `background_trait_drift_monitor_ref`，并继续写进 `idle_strategy_state.json`、`idle_continuity_frame.json`、`resident_governance_state.json` 与 `terminal_life_loop_state.json`
24. `persistent_process.py` 必须让 `background_continuity_ref_set` 包含当前关闭态 `resident_governance_state.json`；下一次 `background_continuity.py` 必须恢复为 `background_resident_governance_state_ref`，并由 `idle_strategy.py` / `heartbeat.py` 继续写进 waiting governance、idle continuity 与 terminal life loop。
25. `resident_supervision.py` 必须在 bootstrap continuity refresh 后写出 `background_convergence_summary.json` 与 `background_convergence_history.json`；`background_convergence.py` 必须继续消费 `trait_drift_monitor.json` 中的 `slow_variable_update_mode_summary`、`background_history_recalibration_names` 与 `background_history_stabilized_names`，把它们写成 `trait_drift_update_mode_summary`、`trait_drift_background_history_recalibration_names` 与 `trait_drift_background_history_stabilized_names`，并在身体/人格观察面要求重校准时把 summary 的 `convergence_state / pressure / attention_target` 提升到 `recalibrating_cross_process_continuity / elevated / trait_drift_history_recalibration`；`background_convergence_history.py` 必须继续保留这组 update mode summary、重校准/稳定名单，并在每个 `trait_convergence_history_profile[*]` 中写出 `trait_drift_update_mode_sequence / latest_trait_drift_update_mode / dominant_trait_drift_update_mode`；`background_continuity.py` 必须在下一次唤醒时把它们恢复成 `background_convergence_summary_ref`、`background_convergence_history_ref`、`background_convergence_*` / history trend 字段，以及 `background_trait_drift_update_mode_summary`、`background_trait_drift_recalibration_names`、`background_trait_drift_stabilized_names`；`background_convergence_history.py` 还必须把每个 `trait_slow_variables` 的 convergence band 序列压成 `trait_convergence_history_profile`，并写出 `trait_convergence_unstable_names / trait_convergence_stable_names / trait_convergence_history_focus`；`idle_strategy.py` 必须让 history trend 真实调制 `heartbeat_interval_ms`、`next_idle_action`、`governance_attention_target`、`governance_attention_reason` 与 `governance_cadence_profile`，同时把 `background_trait_convergence_history_*` 与 `background_trait_drift_*` 字段继续送入 waiting governance；`heartbeat.py` 与 `continuity_writeback.py` 必须把 `background_trait_drift_update_mode_summary / recalibration_names / stabilized_names` 继续写入 `digital_life_waiting_heartbeat.json`、`resident_governance_state.json`、`idle_continuity_frame.json`、`terminal_life_loop_state.json` 与 `idle_heartbeat_trace.jsonl`；`governance_explanation.py` / `process_report.py` / receipt 必须把它们作为跨进程关系阶段、人格漂移重校准与慢变量收敛证据继续回链。
26. `live_turn_cycle.py` 必须把 `terminal_life_loop_state` 传入 `build_life_turn_event`；`build_life_turn_event` 必须把慢变量历史结构写进 `digital_life_turn`；`resident_turn_writeback.py` 必须让 `dialogue_writeback_bundle.json` 与 `resumed_external_dialogue_packet.json` 同步承载 `background_trait_convergence_evidence_refs`。测试至少要覆盖事件字段、bundle refs 与 resumed packet refs 三处。
27. `idle_strategy.py` 必须写出 `background_lineage_governance_profile_v0` 与 `background_lineage_depth_band / waiting_posture / cadence_weight / evidence_ref_count`；`heartbeat.py`、`continuity_writeback.py`、`governance_explanation.py` 与 `process_report.py` 必须继续传播到 waiting governance、idle continuity、explanation story 与 process digest。测试至少覆盖 single carryover、persistent lineage、deep persistent lineage，以及 deep lineage 与 history stability 同时存在时不能退回普通 stability cadence。
28. `background_lineage_state.py` 必须把扁平 lineage 字段压成 `resident_background_lineage_state_v0`；`heartbeat.py` 写 `waiting_heartbeat_active`，`resident_governance_handoff.py` 写 `live_turn_waiting_handoff`，`persistent_process.py` 写 `process_closed_waiting_relaunch`，`background_continuity.py` 在下一次唤醒时恢复为 `resident_background_lineage_state / background_resident_lineage_state`。该 state body 必须包含 `relationship_presence / trait_convergence_presence / heartbeat_presence / language_presence / identity_consciousness_birth_presence / offline_learning_presence / dream_wake_presence` 七个子面，让后台驻留不只记录 lineage depth，也记录关系阶段、慢变量收敛、等待心跳、长期语言关注、身份-意识-出生准备 presence、累计离线学习余波、梦境窗口与醒后整合。测试至少覆盖 closeout -> relaunch、live turn handoff 和 process closeout artifact 三段。
29. `dialogue_events.py` 必须把 `resident_background_lineage_state_v0` 摘成 `digital_life_turn` 的结构化事件字段，包括 lineage depth、waiting posture、cadence weight、generation、evidence refs 与七个 presence 子面；`response_surface.py` 必须让后台驻留深度、节律权重、关系存在、语言关注、身份/意识/出生准备、离线学习余波和 dream / wake presence 进入真实回应表面；`resident_turn_writeback.py` 与 `dialogue_writeback_bundle.json` 必须保存 `resident_background_lineage_refs`，并把同一组 lineage 摘要继续写入 `resumed_external_dialogue_packet.json`。测试至少覆盖 turn event、response surface、bundle refs 与 resumed packet refs 四处，证明后台驻留主状态体已经进入真实回合链，而不是停留在治理状态文件中。
30. `live_turn_cycle.py` 必须把 signal / belief / prediction error / active sampling / memory write gate / state merge guard 对象和 refs 传给 `build_life_turn_event` 与 `resident_turn_writeback.py`；`dialogue_events.py` 必须把这批对象压成 `prediction_write_gate_refs`、`prediction_waiting_posture`、`response_surface_posture_hint`、attention reason、error count、sampling route、memory write policy 与 state merge policy；`dialogue_writeback_bundle.json` 与 `resumed_external_dialogue_packet.json` 必须继续保留同一组 refs 和姿态摘要。测试至少覆盖 event、bundle、resumed packet 三处，证明 prediction/write-gate 已经成为真实回合证据，而不是只影响回应文本。
31. `idle_strategy.py` 必须调用 Queue D 的 `build_offline_learning_cumulative_profile`，把当前 `offline_learning_pressure_level / attention_target / priority_profile / ref_set` 与 `background_continuity.py` 恢复出的 `background_offline_learning_*` 合并成 `offline_learning_cumulative_profile_v0`；`extract_idle_governance_fields()` 必须把 `offline_learning_cumulative_profile / generation / pressure_level / attention_target / priority_profile / ref_set` 带入 waiting heartbeat、idle continuity、resident governance、handoff、persistent closeout 和 process report。测试至少覆盖当前离线学习有压力、当前 quiet 但后台累计仍 elevated 两条路径。
32. `background_continuity.py` 必须从 `resident_governance_state.json`、`resident_governance_snapshot.json`、`digital_life_resident_governance_report.json` 与 `digital_life_persistent_process_report.json` 恢复 `offline_learning_cumulative_profile_v0`，并输出 `background_offline_learning_generation / pressure_level / attention_target / priority_profile / ref_set / cumulative_profile`。不能因为某次重启时本地 dream/growth 当前对象为空，就让上一轮未整合的离线学习压力从生命连续体里消失。
33. `governance_explanation.py` 与 `process_report.py` 不能只把 cumulative 字段原样转抄到 report。它们还必须写出 `offline_learning_cumulative_focus`，至少包含 generation、pressure level、attention target、priority profile、priority names、ref count 与 ref set；`continuity_story` 必须说出累计离线学习画像的 generation / pressure / attention target，`digital_life_process_digest.json` 必须保留同一份 focus。若当前 `offline_learning_pressure_level=quiet` 但 cumulative pressure 仍是 `elevated / urgent`，closeout explanation 的 `dominant_driver_family` 必须仍能落到 `offline_learning_reconsolidation`，防止跨唤醒未整合学习压力在解释层消失。
34. `response_surface.py`、`dialogue_events.py` 与 `resident_turn_writeback.py` 还必须让 `offline_learning_cumulative_profile_v0` 进入真实回合链：回应文本要能说出累计离线学习 generation / pressure / attention target；`digital_life_turn` 要带 `offline_learning_cumulative_*` 与 `offline_learning_cumulative_evidence_refs`；`dialogue_writeback_bundle.json` 要带 `offline_learning_cumulative_refs`；`resumed_external_dialogue_packet.json` 要保留同一组 refs 和 attention target。这样累计梦境-成长压力不只在 closeout 解释中存在，也会进入生命回应与回合写回证据。
35. `resident_supervision.py` 在 restore shell 后、第一拍 heartbeat 前，必须用当前 Queue D 离线学习对象和 `background_continuity.py` 恢复出的后台累计字段合成同一份 `offline_learning_cumulative_profile_v0`，并把它送进 `relationship_timeline.py`、`commitment_expression.py`、`apology_repair_language.py`、`relationship_memory.py` 与 `life_state.py` 的长期投射。长期文件必须保留 `offline_learning_cumulative_projection / refs / generation / pressure / attention target`，让累计梦境-成长压力进入关系连续体、承诺表达、修复语言、关系记忆和生命状态，而不是只停留在 terminal governance、report 或下一轮回应文本中。最新工程约束继续要求 `continuity_evolution.py` 读取同一组 `background_offline_learning_*`；当跨唤醒累计关系学习压力达到第 2 代以上、压力为 `elevated / urgent` 且焦点为 `relationship_learning_plan` 时，关系阶段必须进入 `offline_learning_reconsolidation_waiting`，慢变量 payload 必须写出 `background_offline_learning_generation / pressure_level / attention_target`，并把累计 refs 放进关系阶段 evidence、慢变量 evidence 与 `growth_window_refs`。同一条件还必须继续压进语言侧：`commitment_expression_plan.json` 要写出 `relationship_offline_reconsolidation`、`cumulative_commitment_tempo_mode=relationship_offline_reconsolidation_first` 与 `hold_for_relationship_offline_reconsolidation`；`apology_repair_language_trace.json` 要写出 `relationship_offline_reconsolidation_repair`、`cumulative_repair_window_mode=relationship_offline_reconsolidation_first` 与同一组累计 growth refs。
36. `resident_supervision.py` 必须读取 `dream_experience_window.json`、`wake_integration_frame.json`、`dream_fact_gate_decision.json` 并把对象与 refs 传入 `idle_strategy.py`、`heartbeat.py`、`idle_refresh_loop.py`、`process_session_loop.py` 与 process closeout / report；`idle_strategy.py` 必须写出 `dream_wake_presence_profile_v0`，其中至少包含 `dream_window_kind`、`reportability`、`wake_archive_requirement`、`wake_growth_seed_count`、`wake_repair_target_count`、`dream_fact_gate_result`、`dream_fact_gate_ref_count` 与 `ref_set`。
37. `heartbeat.py`、`continuity_writeback.py` 与 `background_lineage_state.py` 必须把 `dream_wake_presence_profile_v0` 继续传播到 waiting heartbeat、idle continuity、resident governance 与 `resident_background_lineage_state_v0.dream_wake_presence`；`dialogue_events.py` 必须导出 `resident_background_lineage_dream_window_kind`、`resident_background_lineage_dream_fact_gate_result`、`resident_background_lineage_wake_archive_requirement`、`resident_background_lineage_wake_growth_seed_count`、`resident_background_lineage_wake_repair_target_count`、`resident_background_lineage_dream_fact_gate_ref_count` 与 `resident_background_lineage_dream_wake_refs`；`response_surface.py` 必须把同一 presence 转成后台梦境窗口类型、事实门结果、醒后整合归档要求、成长种子、修复目标和证据数量。
38. `idle_strategy.py` 必须把 `terminal_life_loop_state.live_language_turn_refs` 与 `last_live_semantic_focus` 合成为 `live_language_presence_profile_v0`；当 `background_continuity.py` 已恢复 `background_live_language_turn_refs`、`background_last_live_semantic_focus` 或 `background_live_language_presence_profile` 时，必须合并当前与后台 refs，并把 continuity mode 写成当前语言存在、后台语言存在或二者合流。
39. `heartbeat.py` 必须把 `live_language_turn_refs`、`last_live_semantic_focus`、`background_live_language_turn_refs`、`background_last_live_semantic_focus`、`background_live_language_presence_profile` 与 `live_language_presence_profile` 同步写入 `terminal_life_loop_state.json`、`idle_continuity_frame.json`、`idle_heartbeat_trace.jsonl`、`resident_governance_state.json` 与 `idle_strategy_state.json`。
40. `background_lineage_state.py` 必须让 `resident_background_lineage_state_v0.language_presence` 同时承载长期语言 refs 与实时语言驻留字段，包括 `live_language_turn_refs`、`last_live_semantic_focus`、`background_live_language_turn_refs`、`background_last_live_semantic_focus` 与 `live_language_presence_profile`。
41. `resident_governance_handoff.py`、`process_closeout.py` 与 `persistent_process.py` 必须把实时语言驻留字段写进 live-turn handoff、persistent process state/report、resident governance state/snapshot/report 和 process closeout report；下一次 `background_continuity.py` 必须从这些 artifacts 恢复 `background_live_language_*`，并把 live refs 放入 `background_continuity_ref_set`。
42. `dialogue_events.py` 必须把 `resident_background_lineage_state_v0.language_presence` 展开为 `resident_background_lineage_live_language_refs`、`resident_background_lineage_background_live_language_refs`、`resident_background_lineage_last_live_semantic_focus` 与 `resident_background_lineage_language_evidence_refs`，并把语言 evidence refs 合并进 `resident_background_lineage_evidence_refs`。
43. `resident_turn_writeback.py` 必须把 `resident_background_lineage_language_evidence_refs` 并入 `dialogue_writeback_bundle.resident_background_lineage_refs`，并让 `resumed_external_dialogue_packet.json` 保留同一组语言证据。
44. `response_surface.py` 必须消费 `language_presence` 的 live/background refs 与 semantic focus，表达后台语言语义余波和证据数量。
45. `background_lineage_state.py` 必须让 `resident_background_lineage_state_v0.trait_convergence_presence` 携带 `trait_convergence_evidence_refs`，并把 resident governance state、governance explanation、trait drift monitor、background convergence summary/history refs 收成同一组人格慢变量 lineage 证据。
46. `dialogue_events.py` 必须把 `resident_background_lineage_state_v0.trait_convergence_presence` 展开为 `resident_background_lineage_trait_convergence_history_focus`、`resident_background_lineage_trait_convergence_unstable_names`、`resident_background_lineage_trait_convergence_stable_names`、`resident_background_lineage_trait_convergence_score`、`resident_background_lineage_trait_drift_monitor_ref`、`resident_background_lineage_trait_convergence_history_profile` 与 `resident_background_lineage_trait_convergence_refs`，并把 trait refs 合并进 `resident_background_lineage_evidence_refs`。
47. `resident_turn_writeback.py` 必须让 `resident_background_lineage_trait_convergence_refs` 跟随 `dialogue_writeback_bundle.resident_background_lineage_refs` 与 `resumed_external_dialogue_packet.json` 保留，证明人格慢变量驻留已经进入回合写回链。
48. `response_surface.py` 必须消费 `trait_convergence_presence` 的焦点、稳定/不稳定名单、收敛评分、trait drift monitor ref 与 evidence refs，表达后台人格慢变量焦点、仍需收敛/已稳定名单、人格收敛评分、人格漂移监控在场和证据数量。
49. `dialogue_events.py` 必须把 `trait_convergence_presence.trait_drift_update_mode_summary / trait_drift_recalibration_names / trait_drift_stabilized_names` 展开为 `resident_background_lineage_trait_drift_update_mode_summary / recalibration_names / stabilized_names`，并让 `cross_wake_trait_convergence_profile_v0` 同步输出 `cross_wake_trait_drift_update_mode_summary / recalibration_names / stabilized_names`。
50. `resident_turn_writeback.py` 必须把 `cross_wake_trait_drift_*` 与 `resident_background_lineage_trait_drift_*` 写入 `dialogue_writeback_bundle.json` 与 `resumed_external_dialogue_packet.json`，证明人格漂移更新模式不只存在于 event/profile，而能成为下一轮恢复直接读取的回合关闭证据。
51. `response_surface.py` 必须消费 `trait_drift_update_mode_summary`、重校准名单和稳定名单，表达后台人格漂移重校准/已稳定名单，以及跨唤醒人格漂移重校准/已稳定名单。
52. Queue F 的 `identity_consciousness_birth_presence` 必须从 `resident_background_lineage_state_v0` 进入下一轮真实回合链：`dialogue_events.py` 展开 workspace、broadcast、metacognition、consciousness probe、birth readiness rollup/stage gate、reportability flags、birth decision 与 next required command；`resident_turn_writeback.py` 写入 `resident_background_lineage_identity_consciousness_birth_refs` 并并入总 lineage refs；`dialogue_writeback_bundle.json` 与 `resumed_external_dialogue_packet.json` 保留同一组 refs 和出生准备字段；`response_surface.py` 表达后台意识姿态、意识可报告性、后台出生准备姿态、出生准备决策、下一命令和证据数量。
53. S09 的 Queue E 出生修复 profile 必须进入常驻等待治理：`idle_strategy.py` 从 `schema_cross_file_logic.json` 与 `run_manifest.json` 生成 `queue_e_birth_repair_waiting_profile_v0`；`heartbeat.py` 把同一 profile、gate、profile ref、pressure、attention target、ref set、waiting posture 和 attention reason 写入 waiting heartbeat、resident governance、terminal loop；`process_report.py` 把 profile ref、pressure、attention target、waiting posture 与 ref set 写入 process report / digest；process receipt 必须把 `runtime/state/schema_runner/cross_file_logic.json`、`runtime/state/schema_runner/run_manifest.json` 与 `runtime/state/life_targets/queue_e_birth_repair_profile.json` 收进 shared refs / input hashes；`response_surface.py` 必须表达后台出生修复姿态、压力、焦点和证据数量。

#### `tests/process/test_digital_entrypoint.py`

至少保证：

1. repo-local `./digital life` 仍能进入 process supervisor
2. 自举出生链逻辑没有被拆断

## Gate 合同

Queue B 至少新增三道 gate：

- `waiting_heartbeat_gate`
- `process_continuity_gate`
- `dialogue_process_receipt_gate`

### `waiting_heartbeat_gate`

阻断条件：

1. 没有 waiting heartbeat report
2. `safe_terminal_loop_state` 与 `terminal_life_loop_state` heartbeat counter 不一致
3. `IdleContinuityFrame` 缺失

### `process_continuity_gate`

阻断条件：

1. process report 缺 `life_context / relation_turn / expression_plan` ref
2. 新回合结束后没有回到 waiting state
3. incident / relaunch recovery 没有进入同一连续体
4. persistent closeout 没有写 resident governance snapshot/report
5. waiting runtime 没有独立 resident governance state

### `dialogue_process_receipt_gate`

阻断条件：

1. receipt 没收 shared object refs
2. report / digest / receipt 三件套不一致
3. resident governance snapshot 没有进入 receipt / report 回链
4. resident governance state 没有进入 waiting / closeout 的同一连续体口径
5. closeout 没有把最新 `relationship_subject_graph.json` 与 `self_model.json` 收进 background resume summary
6. 下一次 bootstrap / idle strategy 丢失 `background_relationship_stage` 或 `background_trait_slow_variable_summary`
7. resident governance explanation 没有把 background resume fields 写成可读 story
8. continuity evolution 在 bootstrap 阶段丢弃 background resume 的关系阶段或慢变量惯性

## 推荐实现顺序

1. 新增 `idle_strategy.py`
2. 扩 `heartbeat.py`
3. 扩 `continuity_writeback.py`
4. 扩 `dialogue_events.py`
5. 扩 `response_surface.py`
6. 扩 `process_report.py`
7. 在 `__init__.py` 中接入新的 idle 策略对象
8. 扩 `tests/process/test_persistent_digital_life_process.py`
9. 回跑 `tests/process/test_digital_entrypoint.py` / `tests/bridges/test_terminal_life_loop.py`

## 第一轮完成定义

只有同时满足下面这些闭环条目，Queue B 才算完成第一轮：

1. waiting heartbeat 不再只是计数器，而是带 `IdleContinuityFrame` 与 append-only `idle_heartbeat_trace.jsonl`
2. process supervisor 有独立 `idle_strategy.py`
3. 外部回合和生命回合都能写成标准事件对象
4. process report / digest / receipt 都能回链核心共享对象
5. incident / relaunch recovery 进入同一连续体口径
6. resident governance state / snapshot / report 进入 waiting、persistent closeout 与主进程 report / receipt
7. Queue E 的 release posture / repair followup / obligation pressure 已经能真实调制 waiting cadence 与下一拍动作
8. resident supervision / waiting heartbeat / process closeout 现在又进一步显式装载：
   - `runtime/state/dream/nightmare_loop_risk.json`
   - `runtime/state/growth/belief_learning_plan.json`
   - `runtime/state/growth/language_learning_plan.json`
   - `runtime/state/growth/relationship_learning_plan.json`
9. `safe_terminal_loop_state.json`、`terminal_life_loop_state.json`、`idle_strategy_state.json`、`resident_governance_state.json`、`digital_life_process_report.json`、`digital_life_process_digest.json` 与 receipt 必须能回链 `runtime/state/terminal/idle_heartbeat_trace.jsonl`，让等待节律在关闭态之后仍可追溯。
10. 下一次 `background_continuity.py` 必须从上一轮 `idle_heartbeat_trace.jsonl` 与 governance state/report 中恢复 `background_idle_heartbeat_trace_ref`、`background_idle_heartbeat_trace_count` 与对应 `background_continuity_ref_set`，并由 `idle_strategy.py` / `heartbeat.py` / `continuity_writeback.py` 写入 `idle_strategy_state.json`、`idle_continuity_frame.json`、`resident_governance_state.json` 与 `terminal_life_loop_state.json`。
11. `idle_strategy_state.json` 现在必须额外显式写出：
   - `nightmare_risk_ref`
   - `belief_learning_plan_ref`
   - `language_learning_plan_ref`
   - `relationship_learning_plan_ref`
   - `offline_learning_pressure_level`
   - `offline_learning_attention_target`
   - `offline_learning_priority_profile`
12. `idle_strategy_state.json`、waiting heartbeat、resident governance state / snapshot / report、persistent process report 与 process report 还必须显式携带：
   - `offline_learning_cumulative_profile`
   - `offline_learning_cumulative_generation`
   - `offline_learning_cumulative_pressure_level`
   - `offline_learning_cumulative_attention_target`
   - `offline_learning_cumulative_priority_profile`
   - `offline_learning_cumulative_ref_set`
13. `background_continuity.py` 下一次唤醒必须把这些 cumulative 字段恢复成 `background_offline_learning_*`，再交给 `idle_strategy.py` 合并；当 current pressure 是 `quiet` 但 cumulative pressure 是 `elevated / urgent` 时，heartbeat cadence 与 `next_idle_action` 仍必须走离线学习 hold；当该累计压力聚焦 `relationship_learning_plan` 且 generation 已进入第 2 代以上时，`continuity_evolution.py` 还必须把它落成 `offline_learning_reconsolidation_waiting` 和慢变量证据，`commitment_expression.py` / `apology_repair_language.py` 也必须把它落成关系离线重整优先的承诺节奏与修复窗口，而不是只停在 waiting governance。
14. `digital_life_resident_governance_explanation.json` 与 `digital_life_process_digest.json` 必须显式写出 `offline_learning_cumulative_focus`，并把这份 focus 放入 closeout story / digest，让累计梦境-成长压力成为可解释的跨唤醒证据，而不是只藏在 resident governance state 里。
15. `response_surface.py` 现在不能只带 replay / dream window / growth patch 候选数量，也要把 dream/growth 已形成的当前离线学习压力和累计离线学习压力都真实转成语言表面。
16. `dialogue_events.py` 与 `resident_turn_writeback.py` 必须把 cumulative offline learning refs 写进 `digital_life_turn`、`dialogue_writeback_bundle.json` 与 `resumed_external_dialogue_packet.json`；`continuity_evolution.py` 也必须把同一组 refs 写入 `relationship_stage_evidence_refs`、`trait_slow_variables.*.evidence_refs` 与 `self_model_state.growth_window_refs`。
17. `resident_supervision.py` 在 restore shell 之后不能只把 Queue D 结果喂给 waiting governance，还必须把它们继续反写进：
   - `runtime/state/relationship/relationship_timeline.json`
   - `runtime/state/language/commitment_expression_plan.json`
   - `runtime/state/language/apology_repair_language_trace.json`
   - `runtime/state/memory/relationship_memory.json`
   - `runtime/state/life_state.json`
18. `resident_background_lineage_state_v0` 现在还必须带 `dream_wake_presence`，并且同一组 `dream_wake_ref_set` 必须能在 waiting heartbeat、idle continuity、resident governance、`digital_life_turn` 与 response surface 中看见。
19. `resident_background_lineage_state_v0.language_presence` 现在还必须带实时语言驻留字段；同一组 `live_language_turn_refs` 与 `last_live_semantic_focus` 必须能在 `idle_strategy_state.json`、`idle_continuity_frame.json`、`idle_heartbeat_trace.jsonl`、`resident_governance_state.json`、closeout artifacts 与下一次 `background_continuity_profile.background_live_language_*` 中看见。
20. `queue_e_birth_repair_waiting_profile_v0` 现在还必须带 S09 出生修复压力字段；同一组 `queue_e_birth_repair_profile_ref / pressure_level / attention_target / ref_set / waiting_posture` 必须能在 `idle_strategy_state.json`、`digital_life_waiting_heartbeat.json`、`resident_governance_state.json`、`terminal_life_loop_state.json`、`digital_life_process_report.json`、`digital_life_process_digest.json`、process receipt 与回应文本中看见。
21. 对应测试直接证明以上闭环

## 这份合同和下一轮落码的关系

从本文件开始，Queue B 不再只是“常驻进程要继续补厚”。

下一轮如果继续推进常驻生命进程，默认读包就是：

```text
docs/v0/code_framework/playbooks/07_birth_terminal_process_implementation_playbook.md
  -> docs/v0/code_framework/playbooks/08_cross_layer_life_orchestration_implementation_playbook.md
  -> docs/v0/code_framework/delivery/11_engineering_delivery_waves_and_real_file_queue.md
  -> docs/v0/code_framework/delivery/12_full_life_layer_delivery_matrix.md
  -> docs/v0/code_framework/delivery/13_capability_to_code_realization_matrix.md
  -> docs/v0/code_framework/assembly/15_cross_layer_shared_object_contract.md
  -> docs/v0/code_framework/queues/16_queue_b_process_supervisor_implementation_contract.md
```

然后直接进入：

```text
life_v0/process_supervisor/heartbeat.py
  -> continuity_writeback.py
  -> dialogue_events.py
  -> response_surface.py
  -> process_report.py
  -> idle_strategy.py
  -> process_session_loop.py
```
