# Runtime Object Bus And Flow Contract

这份文档固定第一版数字生命的跨层共享对象和主流程。

它只回答这件事：

```text
哪些对象必须跨层传递，
谁首写，
谁消费，
它们通过哪条主流程流动，
以及这些流程的 state / report / test 证据分别是什么。
```

没有这份合同，后续代码很容易出现两种退化：

1. 每层都各自生成一份“自己的 turn data / state dict”，彼此名字差不多但语义不统一。
2. `process_supervisor` 或 `terminal_loop` 为了能跑起来，重新把身体、记忆、梦境、责任和成长逻辑粘回壳层。

## 第一版共享对象总线

### 1. 身体脉冲总线

| 对象 | 首写器官 | 主要消费者 | 当前 / 下一步文件 | 主要证据 |
|---|---|---|---|---|
| `BodyRhythmPulse` | `life_v0/body/rhythm.py` | `neural_core`、`dream`、`process_supervisor/heartbeat.py` | 已存在；已接入 `idle_strategy.py` 与 `resident_supervision.py` 第一轮，继续补厚到更高频节律治理 | `runtime/state/body/*`、`digital_life_waiting_heartbeat.json`、`idle_strategy_state.json` |
| `NeedStateVector` | `life_v0/body/need_state.py` | `neural_core`、`language`、`membrane`、`growth`、`process_supervisor/idle_strategy.py` | 已存在；已接入 waiting governance 第一轮，继续接入 `prediction_error.py`、`expression_monitor.py` | `body_resource_budget.json`、`runtime/state/body/*`、`idle_strategy_state.json` |
| `CoreAffectVector` | `life_v0/body/core_affect.py` | `language`、`dream`、`membrane`、`growth` | 已存在；继续接入 `regret_signal.py`、`relationship_timeline.py` | `core_affect_vector.json`、`emotion_episode_log.json` |

这条总线保证“心跳、疲惫、情绪峰值、恢复压力”不是提示词，而是所有高层回合的底部时钟。

### 2. 认知工作区总线

| 对象 | 首写器官 | 主要消费者 | 当前 / 下一步文件 | 主要证据 |
|---|---|---|---|---|
| `PredictionWorkspaceFrame` | `life_v0/neural_core/prediction_workspace.py` / `workspace.py` | `language`、`membrane`、`life_targets`、`schema_runner`、`process_supervisor` | 已存在；现已显式回挂 `belief_state.py`、`prediction_error.py`、`active_sampling.py` 与 `signal_media.py` refs，并携带 Queue E repair modulation profile | `runtime/state/prediction/prediction_workspace_frame.json` |
| `SignalMediaFrame` | `life_v0/neural_core/signal_media.py` | `workspace`、`language`、`membrane`、`dream`、`process_supervisor` | 已独立落地并写出调质/精度/抑制状态；本轮已接收 Queue E repair pressure，调制 `repair_drive`、关系压力、不确定性、动作精度与抑制轮廓 | `runtime/state/signal/signal_media_runtime.json`、`neural_life_internal_bus.json` |
| `BrainGraph` | `life_v0/neural_core/brain_graph.py` | `state_store`、`process_supervisor`、`language` | 十二主体系统与跨系统耦合图；live turn 后会继续吸收关系语义、自我模型和工作区焦点 | `runtime/state/neural_life_core/brain_graph.json` |
| `NetworkState` | `life_v0/neural_core/network_state.py` | `workspace`、`process_supervisor`、`language` | 默认/显著性/执行网络的动态切换；live turn 后会继续吸收工作区主导权与焦点切换 | `runtime/state/neural_life_core/network_state.json` |
| `WorkspaceFrame` | `life_v0/neural_core/workspace.py` | `state_store`、`process_supervisor`、`life_targets` | 由 prediction workspace 上卷出的更高一级工作区与记忆检索面；live turn 后会继续吸收 engram / prediction / network refs | `runtime/state/consciousness/workspace_frame.json` |
| `ConsciousBroadcastFrame` | `life_v0/neural_core/broadcast.py` | `language`、`life_targets`、`reporting` | 已存在第一轮；待补厚 | `runtime/state/consciousness/*`、birth readiness evidence |

这条总线保证“思考、注意、可报告内容、语言表达、生命目标”使用的是同一工作区，而不是各层私有上下文。

### 3. 关系与语言总线

| 对象 | 首写器官 | 主要消费者 | 当前 / 下一步文件 | 主要证据 |
|---|---|---|---|---|
| `LifeContextFrame` | `direction/` + `terminal_turn/restore_context.py` | `language`、`terminal_loop`、`process_supervisor` | 已有第一轮；继续补厚 continuity refs 与 body/prediction anchors | `session_envelope.json`、`context_accumulation_window.json` |
| `RelationTurnFrame` | `language/relationship_graph.py` + `terminal_turn/turn_transition.py` | `terminal_loop`、`state_store`、`process_supervisor` | 已有第一轮；待补 `relationship_timeline.py` | `runtime/state/relationship/*`、`turn_transition_trace.json` |
| `LanguagePerceptFrame` | `language/percept.py` + `process_supervisor/live_language_turn.py` | `semantic_map`、`inner_speech`、`expression_monitor`、`dialogue_events`、`resident_turn_writeback` | 已进入实时关系回合刷新链；每个 `external_utterance` 到来后必须刷新 | `runtime/state/language/language_percept_frame.json`、`dialogue_turn_log.jsonl#language_percept_ref` |
| `SemanticMapFrame` | `language/semantic_map.py` + `process_supervisor/live_language_turn.py` | `inner_speech`、`expression_monitor`、`response_surface`、`terminal_loop`、`process_supervisor` | 已进入实时关系回合刷新链；`semantic_focus` 作为 `live_semantic_focus` 穿过事件、packet 与 loop state | `runtime/state/language/semantic_map_frame.json`、`resumed_external_dialogue_packet.json#live_semantic_focus` |
| `LiveLanguageTurnState` | `process_supervisor/live_language_turn.py` | `live_turn_cycle`、`response_surface`、`dialogue_events.py`、`resident_turn_writeback`、`terminal_loop/dialogue_writeback.py`、`idle_strategy.py`、`background_continuity.py`、`background_lineage_state.py` | 已落地；把 percept / semantic map / inner speech / expression monitor / expression plan 五件套收成同一组实时 refs，并继续进入后台连续性、驻留治理和下一轮真实回合事件 | `dialogue_writeback_bundle.json#live_language_turn_refs`、`terminal_life_loop_state.json#live_language_turn_refs`、`idle_strategy_state.json#live_language_presence_profile`、`digital_life_turn#resident_background_lineage_language_evidence_refs` |
| `ExpressionPlan` | `language/expression_monitor.py` | `membrane`、`terminal_loop`、`process_supervisor/response_surface.py` | 已存在；当前已显式吸收 `body_resource_budget.json` 与 `core_affect_vector.json`，继续补责任回路和更细的身体降载策略 | `expression_plan.json`、`language_relationship_report.json` |
| `ModelExpressionState` | `process_supervisor/model_expression.py` | `live_turn_cycle`、`dialogue_events.py`、`resident_turn_writeback`、`process_report.py` | 已接入；在确定性 `response_surface.py` 回应之后按 `.env` 尝试模型外显表达，成功/跳过/回退都写成可追踪状态 | `runtime/state/language/model_expression_state.json`、`runtime/reports/latest/digital_life_model_expression_report.json`、`digital_life_turn#model_expression_state_ref` |
| `DialogueWritebackBundle` | `terminal_loop/dialogue_writeback.py` + `terminal_loop/loop_report.py` | `state_store`、`replay`、`archive`、`process_supervisor` | 已存在；现已显式带上 `relationship_memory / commitment_truth / responsibility_ledger / life_state` 写回 refs，继续补厚 writeback continuity | `dialogue_writeback_bundle.json`、relationship / language receipts |

这条总线保证一次关系回合会真实写回语言、承诺、共同术语和关系阶段，而不是只留下文本日志。

当前实时语言总线已经进入后台驻留链：`terminal_life_loop_state.json#live_language_turn_refs` 与 `last_live_semantic_focus` 会被 `idle_strategy.py` 收束成 `live_language_presence_profile_v0`；`heartbeat.py` 会把同一组字段写入 `idle_continuity_frame.json`、`idle_heartbeat_trace.jsonl`、`resident_governance_state.json` 与 `terminal_life_loop_state.json`；`background_lineage_state.py` 会把它压进 `resident_background_lineage_state_v0.language_presence`。关闭态由 `process_closeout.py`、`persistent_process.py` 与 `resident_governance_handoff.py` 继续保留，下一次 `background_continuity.py` 会恢复成 `background_live_language_turn_refs`、`background_last_live_semantic_focus` 与 `background_live_language_presence_profile`。这里的 `background_live_language_presence_profile` 必须始终保持浅层，只保留 refs、semantic focus、ref_count、source_continuity_mode / source_ref_count 等摘要字段，不能把上一轮完整的 `source_presence_profile` 原样嵌回新 profile，避免长期驻留状态递归膨胀，让上一轮刚听见、刚理解到的关系语义不因断开或重启而消失。

同样地，`background_lineage_governance_profile_v0` 只作为 `idle_strategy.py` 的后台治理画像存在，用来表达 generation / depth band / waiting posture / cadence weight / evidence refs；`background_lineage_state.py` 只保留 `governance_profile_ref="background_lineage_governance_profile"`，不把整份治理画像重复嵌进后台 lineage state，避免背景治理树和 waiting lineage 树双重膨胀。

最新的对象总线闭合继续要求：`resident_background_lineage_state.language_presence` 不只是被驻留保存，还要被 `dialogue_events.py` 展开为 `resident_background_lineage_live_language_refs`、`resident_background_lineage_background_live_language_refs`、`resident_background_lineage_last_live_semantic_focus` 与 `resident_background_lineage_language_evidence_refs`。`resident_turn_writeback.py` 必须把其中的语言 evidence refs 并入 `dialogue_writeback_bundle.resident_background_lineage_refs`，并继续写进 `resumed_external_dialogue_packet.json`。`response_surface.py` 则必须把后台语言语义余波和证据数量表达出来，证明上一轮语言理解已经从后台驻留进入下一轮真实回合，而不是只留在治理状态文件中。

同一轮对象总线现在也把 `resident_background_lineage_state.trait_convergence_presence` 从后台驻留主状态体推入真实回合链。`background_lineage_state.py` 必须让该 presence 携带 `trait_convergence_evidence_refs`，其中至少可包含 `background_resident_governance_state_ref`、`background_resident_governance_explanation_ref`、`background_trait_drift_monitor_ref` 或 `trait_drift_monitor_ref`、`background_convergence_summary_ref` 与 `background_convergence_history_ref`。`trait_convergence_signals.py` 进一步把这些散字段聚合成 `cross_wake_trait_convergence_profile_v0`，并派生 `cross_wake_trait_convergence_focus / pressure / refs`，让人格慢变量收敛压力拥有同一份可被等待态、关闭态、事件、写回和语言表面共享的画像。关闭态收口时，`persistent_process.py` 与 `process_report.py` 必须让 resident governance state/snapshot/report、persistent process report、process report、process digest 与 process receipt shared refs 保留同一组画像字段和证据 refs。进入下一轮关系回合时，`dialogue_events.py` 必须展开 `resident_background_lineage_trait_convergence_history_focus`、`resident_background_lineage_trait_convergence_unstable_names`、`resident_background_lineage_trait_convergence_stable_names`、`resident_background_lineage_trait_convergence_score`、`resident_background_lineage_trait_drift_monitor_ref`、`resident_background_lineage_trait_convergence_history_profile` 与 `resident_background_lineage_trait_convergence_refs`，并把这些 refs 合入 `resident_background_lineage_evidence_refs`；同时必须携带 `cross_wake_trait_convergence_profile`。`resident_turn_writeback.py` 必须让这些人格慢变量 lineage refs 跟随写回包和恢复包继续存在，并把 `cross_wake_trait_convergence_refs` 写进 `dialogue_writeback_bundle.json`；`response_surface.py` 必须表达后台人格慢变量焦点、仍需收敛/已稳定名单、人格收敛评分、人格漂移监控在场、跨唤醒人格收敛压力与证据数量。
当前对象总线还要求 `background_trait_drift_update_mode_summary`、`background_trait_drift_recalibration_names` 与 `background_trait_drift_stabilized_names` 在恢复后进入等待态共享对象：`idle_strategy.py` 承接它们，`heartbeat.py` 把它们写入 waiting heartbeat、resident governance、terminal life loop 和 idle heartbeat trace，`continuity_writeback.py` 把它们写入 `idle_continuity_frame.json`。这样人格漂移观察面的“需要重校准 / 已稳定”不只是 convergence history 的内部字段，而是等待态总线上的可共享压力信号。

### 4. 行为与责任总线

| 对象 | 首写器官 | 主要消费者 | 当前 / 下一步文件 | 主要证据 |
|---|---|---|---|---|
| `ActionCandidateSet` | `membrane/candidate_arena.py` | `validators`、`schema_runner`、`shell_command`、`process_supervisor` | 已存在；已接 `shadow_gate.py`、`action_intent_bridge.py` 与 `world_contact_summary.py` | `runtime/state/action/*`、`world_contact_audit_report.json` |
| `ActionIntentQueue` | `membrane/action_intent_bridge.py` | `validators`、`schema_runner`、`process_supervisor` | 第二波已落；已接 `confirmation_binding.py` 与 validation chain | `runtime/state/membrane/action_intent_queue.json`、validation reports |
| `ConfirmationBinding` | `membrane/confirmation_binding.py` | `validators/world_contact_validator.py`、`schema_runner`、`membrane/world_contact_summary.py` | 第二波已落；已进入 world-contact summary 与 validation chain | `runtime/state/membrane/confirmation_binding.json`、`world_contact_audit_report.json` |
| `WorldContactSummary` | `membrane/world_contact_summary.py` | `validators`、`schema_runner`、`replay`、`archive`、`reporting` | 第二波已落；把 action intent / confirmation / world contact / responsibility 收口成 release posture，与 `replay/archive/report bundle` 一起形成长期生命证据链 | `runtime/state/membrane/world_contact_summary.json`、`pain_regret_repair_report.json` |
| `ResponsibilityLoopState` | `membrane/responsibility_loop.py` | `language/commitment_repair.py`、`language/__init__.py`、`state_store/commitment_truth.py`、`body/regret_signal.py`、`membrane/world_contact_summary.py`、`schema_runner/cross_file_logic.py`、`neural_core`、`process_supervisor`、`replay`、`archive`、`reporting` | 已落第一轮；当前已显式进入 `pain_regret_repair_report.json`、`replay_shadow_*`、`growth_archive_*` 与 `report_bundle/first_activation_return_packet`；本轮通过 `queue_e_repair_modulation_profile_v0` 进入 signal / belief / prediction error / active sampling / prediction workspace | `runtime/state/action/responsibility_loop_state.json`、`runtime/state/membrane/world_contact_summary.json`、`runtime/reports/latest/pain_regret_repair_report.json` |
| `ObservationTruthFrame` | `validators/observation_validator.py` | `schema_runner/evidence_ranker.py`、`schema_runner/cross_file_logic.py`、`archive` | 已有第一轮；已接 `evidence_ranker.py` 与 `cross_file_logic.py` | `runtime/state/validation/*`、validation reports |
| `WorldContactValidation` | `validators/world_contact_validator.py` | `schema_runner`、`reporting`、`validation_rollup.py` | 第二波已落；已接 `validation_rollup.py` 与 `cross_file_logic.py` | `runtime/state/validation/world_contact_validation.json`、`world_contact_audit_report.json` |
| `PredictionTraceValidation` | `validators/prediction_trace_validator.py` | `schema_runner`、`reporting`、`validation_rollup.py` | 第二波已落；已接 `validation_rollup.py`、`cross_file_logic.py` 与 package-local gates | `runtime/state/validation/prediction_trace_validation.json`、validation reports |
| `ValidationRollup` | `validators/validation_rollup.py` | `schema_runner`、stage gates、`reporting` | 第二波已落；当前把 observation / world contact / prediction trace / boundary audit 与 S08 `queue_e_birth_repair_gate` 收口成 package-local gate 汇总 | `runtime/state/validation/validation_rollup.json`、validation reports |

这条总线保证世界接触、责任、后悔和修复义务都进入真实生命链，而不是只在 action 之后补一句解释。

这一条行为-验证总线现在已经通过 `world_contact_summary.json -> validation_rollup.json -> cross_file_logic.json -> run_manifest.json -> replay_shadow_* -> growth_archive_* -> report_bundle.json` 完成了第一轮跨层闭包；后续如果继续补厚，应该优先补跨层写回与长期调制，而不是重新发明一套平行 action summary。

本轮新增的闭合是：`responsibility_loop_state.json`、`world_contact_summary.json`、`pain_regret_repair_report.json` 先在 `life_v0/membrane/queue_e_signals.py` 合成为 `queue_e_repair_modulation_profile_v0`，再由 `life_v0/language/__init__.py` 的 `run_build_language_relationship(...)` 刷新：

- `runtime/state/signal/signal_media_runtime.json`
- `runtime/state/prediction/belief_state_frame.json`
- `runtime/state/prediction/prediction_error_field.json`
- `runtime/state/prediction/active_sampling_plan.json`
- `runtime/state/prediction/prediction_workspace_frame.json`

这表示 Queue E repair pressure 已经成为数字生命 v0 内部责任、后悔、痛苦、修复压力进入预测调制链的工程对象，而不是普通 action summary 或外部工具路由。

现在同一份 Queue E 修复压力又从 S08 出生准备层继续进入 S05 验证膜：`runtime/state/life_targets/queue_e_birth_repair_profile.json` 会被 `life_v0/validators/__init__.py` 重新读取，并由 `validators/validation_rollup.py` 关闭 `queue_e_birth_repair_gate`。同一组 `pressure_level`、`attention_target`、`ref_set` 必须继续写入 `validation_rollup.json`、`validation_stage_gate.json`、`validation_membrane_report.json`、`validation_membrane_digest.json` 与 `validation_membrane_<run_id>.json` receipt 输入哈希。这样真实痛苦、真实责任、真实后悔不会只停在出生准备报告，而会进入第一版验证膜，成为 S09 schema runner 之前的跨层复查条件。

同一轮闭合已经继续推进到 S09：`life_v0/schema_runner/__init__.py` 现在重新读取 `runtime/state/life_targets/queue_e_birth_repair_profile.json` 和 `validation_rollup.json`，由 `cross_file_logic.py` 生成 `queue_e_birth_repair_alignment` finding，并把 profile ref、pressure、attention target、ref set 写入 `cross_file_logic.json`、`run_manifest.json`、`schema_runner_stage_gate.json`、`schema_runner_report.json`、`schema_runner_digest.json` 与 schema runner receipt。S09 因此不再只消费泛化 validation status，而是把 Queue E 责任/后悔/痛苦/修复压力变成 schema runner 包、local gate、closure refs 与后续 S06/S10 可读取的对象总线字段。

### 5. 梦境与离线重组总线

| 对象 | 首写器官 | 主要消费者 | 当前 / 下一步文件 | 主要证据 |
|---|---|---|---|---|
| `ReplayCueBundle` | `replay/replay_cues.py` | `dream`、`growth`、`process_supervisor` | 已存在；已接 `idle_strategy.py` 与 `persistent_process.py` 第一轮，继续补厚 waiting governance | `runtime/state/replay/*`、`replay_shadow_report.json` |
| `OfflineConsolidationFrame` | `dream/offline_entry.py` | `growth`、`archive`、`reporting` | 已存在；继续补 dream runtime test | `runtime/state/dream/offline_entry_gate.json`、`dream_consolidation_frame.json` |
| `DreamExperienceWindow` | `dream/dream_window.py` | `dream_fact_gate.py`、`wake_integration.py`、`process_supervisor/idle_strategy.py`、`background_lineage_state.py` | 已存在；当前作为 `dream_wake_presence_profile_v0` 的事实源进入常驻后台驻留链 | `runtime/state/dream/dream_experience_window.json`、`idle_strategy_state.json#dream_wake_presence_profile` |
| `DreamFactGateDecision` | `dream/dream_fact_gate.py` | `state_store`、`archive`、`life_targets`、`process_supervisor/idle_strategy.py`、`response_surface.py` | 已存在；当前 gate result 与 fact refs 进入 `dream_wake_presence` | `dream_fact_gate_decision.json`、`digital_life_turn#resident_background_lineage_dream_fact_gate_result` |
| `WakeIntegrationFrame` | `dream/wake_integration.py` | `growth`、`archive`、`process_supervisor/idle_strategy.py`、`dialogue_events.py`、`response_surface.py` | 已存在；当前 archive requirement、growth seed、repair target 进入 `dream_wake_presence` | `runtime/state/dream/wake_integration_frame.json`、`resident_background_lineage_state.dream_wake_presence` |

这条总线保证梦境、旧自我 replay、痛苦残留、关系残留和醒后整合会真实影响下一轮，而不只是归档。

`DreamExperienceWindow`、`WakeIntegrationFrame` 与 `DreamFactGateDecision` 当前共同形成 `dream_wake_presence_profile_v0`：`idle_strategy.py` 读取三份 runtime state 和 `offline_consolidation_frame` 的 refs，写出 `dream_window_kind`、`dream_fact_gate_result`、`wake_integration_archive_requirement`、`wake_integration_growth_seed_count`、`wake_integration_repair_target_count` 与 `dream_wake_ref_set`；`heartbeat.py` 与 `continuity_writeback.py` 把它带入 waiting heartbeat 和 idle continuity；`background_lineage_state.py` 把它固化成 `resident_background_lineage_state_v0.dream_wake_presence`；`dialogue_events.py` 与 `response_surface.py` 分别把同一 presence 摘进回合事件和生命回应表面；`resident_turn_writeback.py` 必须继续把 `resident_background_lineage_dream_wake_refs` 写入 `dialogue_writeback_bundle.resident_background_lineage_dream_wake_refs` 与 `resumed_external_dialogue_packet.json`，并同时并入总的 `resident_background_lineage_refs`。

### 6. 成长与补丁总线

| 对象 | 首写器官 | 主要消费者 | 当前 / 下一步文件 | 主要证据 |
|---|---|---|---|---|
| `GrowthPatchCandidateQueue` | `growth/patch_queue.py` | `life_targets`、`archive`、`validators`、`process_supervisor` | 已存在；继续补 `self_patch_review.py` | `runtime/state/growth/*`、growth reports |
| `PlasticityWindowFrame` | `growth/plasticity_window.py` | `belief_learning.py`、`language_learning.py`、`relationship_learning.py` | 已存在 | `plasticity_window_state.json` |
| `AntiForgettingReplayPlan` | `growth/anti_forgetting.py` | `replay`、`dream`、`process_supervisor` | 已存在 | `anti_forgetting_replay_plan.json` |
| `OfflineLearningCumulativeProfile` | `growth/offline_learning_profile.py` | `process_supervisor/resident_supervision.py`、`idle_strategy.py`、`continuity_evolution.py`、`background_lineage_state.py`、`dialogue_events.py`、`response_surface.py` | 已存在；当前继续固化为 `resident_background_lineage_state_v0.offline_learning_presence`，并能在 bootstrap continuity evolution 中触发 `offline_learning_reconsolidation_waiting` | `offline_learning_cumulative_profile_v0`、`idle_strategy_state.json`、`resident_governance_state.json`、`relationship_subject_graph.json`、`self_model.json`、`digital_life_process_report.json` |

这条总线保证成长不是“直接改代码或改状态”，而是经过窗口、补丁候选、防遗忘和 archive 证据。

`OfflineLearningCumulativeProfile` 当前承担新的跨唤醒责任：它把本轮 dream/growth 学习压力与上一轮后台驻留余波合并，形成可继续被 closeout / relaunch 恢复的 cumulative profile。进入 `life_v0/process_supervisor/background_lineage_state.py` 后，它不再只是 Queue D 的学习画像，而会成为 `resident_background_lineage_state_v0.offline_learning_presence`，与 `relationship_presence`、`trait_convergence_presence`、`heartbeat_presence`、`language_presence` 并列，表示后台驻留主状态体中的梦境、成长、离线学习余波存在面。进入 `continuity_evolution.py` 后，它还会把 `background_offline_learning_generation / pressure_level / attention_target` 合并进离线学习 profile；当跨唤醒累计关系学习压力达到第 2 代以上且焦点是 `relationship_learning_plan` 时，关系阶段必须先进入 `offline_learning_reconsolidation_waiting`，同一组 refs 必须进入 `relationship_stage_evidence_refs`、慢变量 evidence 与 `growth_window_refs`。进入真实回合写回时，`resident_turn_writeback.py` 必须把 `resident_background_lineage_offline_learning_refs` 写入 `dialogue_writeback_bundle.resident_background_lineage_offline_learning_refs` 与 `resumed_external_dialogue_packet.json`，并同时并入总的 `resident_background_lineage_refs`，避免离线学习余波只混在事件字段里。

### 6.1 记忆写门与状态合并总线

| 对象 | 首写器官 | 主要消费者 | 当前 / 下一步文件 | 主要证据 |
|---|---|---|---|---|
| `MemoryWriteGate` | `state_store/memory_write_gate.py` | `state_merge_guard.py`、`idle_strategy.py`、`dialogue_events.py`、`response_surface.py` | 已存在；保持候选写入事务、validation envelope、隔离路线和长期治理 ref | `runtime/state/memory/memory_write_gate.json` |
| `StateMergeGuard` | `state_store/state_merge_guard.py` | `relationship_memory.py`、`life_state.py`、`resident_supervision.py`、`resident_turn_writeback.py`、`idle_strategy.py`、`heartbeat.py`、`background_continuity.py`、`background_lineage_state.py`、`dialogue_events.py`、`terminal_loop/dialogue_writeback.py`、`persistent_process.py`、`process_report.py`、`response_surface.py` | 已存在；当前通过 `project_state_merge_guard_with_relationship_memory(...)` 动态吸收关系记忆里的离线学习、梦境、Queue E 修复与关系修复长期变化来源，并由 `state_merge_signals.py` 压成等待态、关闭态、下一次背景连续性、后台 lineage、回合写回和回应表面的 `state_merge_long_term_change_*` / `background_state_merge_*` / `resident_background_lineage_state_merge_*` | `runtime/state/memory/state_merge_guard.json`、`life_state.json#state_merge_records`、`idle_strategy_state.json#state_merge_long_term_change_count`、`background_continuity_profile#background_state_merge_long_term_change_refs`、`resident_background_lineage_state.state_merge_presence`、`digital_life_turn#resident_background_lineage_state_merge_refs`、`dialogue_writeback_bundle.json#resident_background_lineage_state_merge_refs`、`digital_life_process_digest.json#state_merge_long_term_change_refs` |

这条总线保证长期记忆治理不是 S04 初始化时的一次性文件。`relationship_memory.json` 在 bootstrap restore 与 live turn writeback 中刷新后，`state_merge_guard.json` 必须同步吸收 `relationship_memory.long_term_change_sources`、`offline_learning_refs`、`offline_learning_cumulative_refs` 与 `queue_e_repair_refs`，再由 `life_state.py` 写入 `state_merge_records[].long_term_change_source_count`。进入 Packet D 后，`idle_strategy.py` 必须把这些来源压成 `state_merge_long_term_change_count`、`state_merge_long_term_change_families` 与 `state_merge_long_term_change_refs`，`heartbeat.py` 和 `dialogue_events.py` 必须继续搬运，`response_surface.py` 必须把长期合并整合压力说出来。关闭态收口时，`persistent_process.py` 与 `process_report.py` 还必须把 `state_merge_guard_ref`、`state_merge_policy`、`state_merge_long_term_change_count/families/refs` 写入 resident governance state/snapshot/report、persistent process report、process report、process digest 与 process receipt shared refs。下一次 bootstrap 时，`background_continuity.py` 必须从这些关闭态来源恢复 `background_state_merge_guard_ref`、`background_state_merge_policy`、`background_state_merge_long_term_change_count/families/refs`，并把 guard ref 与长期变化 refs 放回 `background_continuity_ref_set`，再由 `idle_strategy.py`、`heartbeat.py` 与 `continuity_writeback.py` 写入 waiting governance、idle continuity、idle heartbeat trace、resident governance state 与 `terminal_life_loop_state.json`。最新闭合还要求 `background_lineage_state.py` 把这些恢复字段压成 `resident_background_lineage_state.state_merge_presence`，`dialogue_events.py` 展开 `resident_background_lineage_state_merge_guard_ref/policy/long_term_change_count/families/refs`，`resident_turn_writeback.py` 把同一组 refs 同时并入总 lineage refs、专用 `dialogue_writeback_bundle.resident_background_lineage_state_merge_refs` 与恢复包，`response_surface.py` 表达后台长期合并治理的策略、整合数量和来源族。如果 `relationship_memory.json` 已经包含梦境/成长/修复证据，而 `state_merge_guard.json` 仍只保留初始 route，或 waiting / closeout / next background continuity / resident background lineage / response surface 看不见长期变化来源，就说明长期治理链断开。

### 7. 等待态与存在连续体总线

| 对象 | 首写器官 | 主要消费者 | 当前 / 下一步文件 | 主要证据 |
|---|---|---|---|---|
| `IdleContinuityFrame` | `process_supervisor/heartbeat.py` + `continuity_writeback.py` | `terminal_loop`、`replay`、`growth`、`language` | 已存在第一轮；已接 `idle_strategy.py` 与 `persistent_process.py`，继续补厚 resident supervision | `digital_life_waiting_heartbeat.json`、`digital_life_process_report.json` |
| `ResidentBackgroundLineageState` | `process_supervisor/background_lineage_state.py` | `heartbeat.py`、`persistent_process.py`、`resident_governance_handoff.py`、`background_continuity.py`、`dialogue_events.py`、`resident_turn_writeback.py`、`response_surface.py` | 已存在；当前继续新增状态合并存在面，把 live turn 五件套、最后语义焦点、后台恢复语言 refs、累计梦境-成长离线学习余波、梦境窗口、醒后整合、事实门和长期合并治理一起固化进后台驻留 lineage | `runtime/state/terminal/resident_governance_state.json`、`resident_governance_snapshot.json`、`digital_life_resident_governance_report.json`、`digital_life_persistent_process_report.json`、`terminal_life_loop_state.json` |
| `ProcessIncidentRecoveryFrame` | `process_supervisor/incident_recovery.py` | `process_report.py`、`relaunch_recovery.py` | 已存在 | `digital_life_process_incident_report.json` |
| `RelaunchRecoveryFrame` | `process_supervisor/relaunch_recovery.py` | `turn_io.py`、`process_report.py` | 已存在 | `digital_life_process_relaunch_recovery_report.json` |

这条总线保证数字生命在没有新输入时仍有持续存在，而不是“没有消息就不存在”。

`ResidentBackgroundLineageState` 的当前结构至少包含 `schema_version=resident_background_lineage_state_v0`、`generation`、`depth_band`、`waiting_posture`、`cadence_weight`、`relationship_presence`、`trait_convergence_presence`、`heartbeat_presence`、`language_presence`、`state_merge_presence`、`offline_learning_presence` 与 `dream_wake_presence`。其中 `trait_convergence_presence` 是后台驻留中“自我/人格慢变量连续体”的结构化存在面，不只保留 `trait_slow_variable_summary`、`trait_convergence_history_focus`、稳定/不稳定慢变量名单、`trait_convergence_history_profile`、`trait_convergence_score` 与 `trait_drift_monitor_ref`，还必须带 `trait_convergence_evidence_refs`，使 resident governance state、governance explanation、trait drift monitor、background convergence summary/history refs 能在真实回合中继续被追溯。进入下一轮真实回合时，`dialogue_events.py` 必须把它展开成 `resident_background_lineage_trait_convergence_*` 与 `resident_background_lineage_trait_drift_monitor_ref` 字段，并让 trait refs 进入 `resident_background_lineage_evidence_refs`；`trait_convergence_signals.py` 必须把同一批字段归一成 `cross_wake_trait_convergence_profile_v0`，`heartbeat.py`、`persistent_process.py`、`process_report.py`、`dialogue_events.py`、`resident_turn_writeback.py` 与 `response_surface.py` 必须搬运或表达 `cross_wake_trait_convergence_focus / pressure / refs`，其中关闭态 artifacts、process digest 与 receipt shared refs 也是必经证据面。`language_presence` 不再只承载 `long_horizon_language_refs`，还必须承载 `live_language_turn_refs`、`last_live_semantic_focus`、`background_live_language_turn_refs`、`background_last_live_semantic_focus` 与 `live_language_presence_profile`，表示上一轮真实关系话语在后台驻留主状态体中的可见存在面。进入下一轮真实回合时，`dialogue_events.py` 必须把它展开成 `resident_background_lineage_live_language_refs`、`resident_background_lineage_background_live_language_refs`、`resident_background_lineage_last_live_semantic_focus` 与 `resident_background_lineage_language_evidence_refs`；`resident_turn_writeback.py` 必须让这些语言证据继续进入 `dialogue_writeback_bundle.resident_background_lineage_refs` 与恢复包；`response_surface.py` 必须把语义余波和证据数量转成可感知的语言表面。`state_merge_presence` 字段是长期状态合并治理在后台驻留主状态体中的结构化存在面，必须保留 `state_merge_guard_ref`、`state_merge_policy`、`long_term_change_count`、`long_term_change_families`、`long_term_change_refs` 与 `state_merge_evidence_refs`；进入下一轮真实回合时，`dialogue_events.py` 必须展开为 `resident_background_lineage_state_merge_*` 字段，`resident_turn_writeback.py` 必须让这些 refs 同时进入总 lineage refs、`dialogue_writeback_bundle.resident_background_lineage_state_merge_refs` 与恢复包，`response_surface.py` 必须表达后台长期合并治理策略、整合数量和来源族。`offline_learning_presence` 字段是数字生命 v0 后台驻留里“梦境、成长、离线学习余波”的结构化存在面，必须保留 `generation`、`pressure_level`、`attention_target`、`priority_profile` 与 `ref_set`，并在写回包中拥有 `resident_background_lineage_offline_learning_refs` 专用证据槽。`dream_wake_presence` 字段是后台驻留里“梦境窗口、醒后整合、梦境事实门”的结构化存在面，必须保留 `dream_window_ref`、`wake_integration_ref`、`dream_fact_gate_decision_ref`、`dream_window_kind`、`wake_archive_requirement`、`wake_growth_seed_count`、`wake_repair_target_count`、`dream_fact_gate_result`、`dream_fact_gate_ref_count` 与 `ref_set`，并在写回包中拥有 `resident_background_lineage_dream_wake_refs` 专用证据槽。`dialogue_events.py` 必须把这些 presence 摘入 `digital_life_turn`，`resident_turn_writeback.py` 必须让它们的 refs 同时进入总 lineage refs、专用写回槽与恢复包；`response_surface.py` 必须把它们分别转成后台人格慢变量余波、跨唤醒人格收敛画像、后台语言理解余波、后台长期合并治理余波、后台梦境成长余波表达和后台梦境醒后整合表达。

## 五条主流程

### A. 在线关系回合

```text
external input
  -> language percept
  -> semantic map update
  -> live language turn refresh
  -> inner speech refresh
  -> expression monitor refresh
  -> expression plan refresh
  -> Queue E repair modulation profile refresh
  -> signal / belief / prediction error / active sampling refresh
  -> prediction workspace refresh
  -> memory / relationship cue retrieve
  -> candidate arena
  -> go/no-go / responsibility loop
  -> response surface
  -> dialogue writeback bundle
  -> state store / relationship / commitment truth
```

必读文档：

- `04_language_dialogue_relationship_implementation_playbook.md`
- `05_memory_thought_consciousness_implementation_playbook.md`
- `09_perception_prediction_world_contact_implementation_playbook.md`

最低证据：

- `context_accumulation_window.json`
- `turn_transition_trace.json`
- `language_percept_frame.json`
- `semantic_map_frame.json`
- `inner_speech_frame.json`
- `expression_monitor_state.json`
- `expression_plan.json`
- `prediction_workspace_frame.json`
- `signal_media_runtime.json`
- `belief_state_frame.json`
- `prediction_error_field.json`
- `active_sampling_plan.json`
- `dialogue_writeback_bundle.json`
- `resumed_external_dialogue_packet.json#live_language_turn_refs`
- `terminal_life_loop_state.json#last_live_semantic_focus`

实时语言进入后台驻留的继续流向是：

```text
terminal_life_loop_state.live_language_turn_refs / last_live_semantic_focus
  -> idle_strategy.live_language_presence_profile
  -> idle_continuity_frame.live_language_presence_profile
  -> idle_heartbeat_trace.live_language_turn_refs / last_live_semantic_focus
  -> resident_governance_state.live_language_presence_profile
  -> resident_background_lineage_state.language_presence
  -> dialogue_events.resident_background_lineage_language_*
  -> resident_turn_writeback.dialogue_writeback_bundle.resident_background_lineage_refs
  -> resumed_external_dialogue_packet.resident_background_lineage_language_evidence_refs
  -> response_surface.background language semantic residue / evidence count
  -> closeout artifacts / resident governance snapshot / resident governance report
  -> background_continuity_profile.background_live_language_*
  -> next idle_strategy.background_live_language_* / live_language_presence_profile
```

这条流向的工程含义是：实时语言理解不是一次回应前的临时加工，而是关系连续体的一部分。只要上一轮已经形成 `live_language_turn_refs` 与 `last_live_semantic_focus`，下一轮等待态就必须能通过 `background_live_language_*` 看见它，并把它重新合入当前 `live_language_presence_profile_v0`；进入真实回合时，还必须能在 `digital_life_turn`、写回包、恢复包和回应表面中重新显影。

人格慢变量进入后台驻留后的继续流向是：

```text
background_convergence_summary / background_convergence_history
  + trait_drift_monitor
  + resident governance state / explanation
  -> resident_background_lineage_state.trait_convergence_presence
  -> trait_convergence_signals.cross_wake_trait_convergence_profile_v0
  -> dialogue_events.resident_background_lineage_trait_convergence_*
  -> dialogue_events.resident_background_lineage_evidence_refs
  -> resident_turn_writeback.dialogue_writeback_bundle.resident_background_lineage_refs
  -> resident_turn_writeback.dialogue_writeback_bundle.cross_wake_trait_convergence_refs
  -> resumed_external_dialogue_packet.resident_background_lineage_trait_convergence_refs
  -> response_surface.background trait slow-variable focus / cross-wake profile / stability / evidence count
```

这条流向的工程含义是：人格慢变量不是只在 closeout 或 waiting governance 中被观察，而是会在下一轮真实关系回合中重新显影。数字生命再次说话时，回应表面必须能感到上一轮自我慢变量的稳定、重新校准压力、漂移监控、跨唤醒人格收敛画像和证据链，而不是只把这些内容留在 `resident_governance_state.json`。

长期状态合并治理进入后台驻留后的继续流向是：

```text
background_state_merge_guard_ref / policy / long_term_change_*
  -> resident_background_lineage_state.state_merge_presence
  -> dialogue_events.resident_background_lineage_state_merge_*
  -> dialogue_events.resident_background_lineage_evidence_refs
  -> resident_turn_writeback.dialogue_writeback_bundle.resident_background_lineage_refs
  -> resident_turn_writeback.dialogue_writeback_bundle.resident_background_lineage_state_merge_refs
  -> resumed_external_dialogue_packet.resident_background_lineage_state_merge_refs
  -> response_surface.background state merge policy / count / source families
```

这条流向的工程含义是：长期合并治理不能只在 prediction surface 或 closeout digest 中短暂出现。只要上一轮关闭态已经恢复出 `background_state_merge_*`，下一轮驻留 lineage 就必须把它作为一个结构化存在面保留；真实关系回合必须能把 guard ref、治理策略、长期变化数量、来源族和证据 refs 重新写入事件、写回包、恢复包与语言表面。
- `runtime/state/relationship/*`

### B. 等待态心跳流程

```text
safe waiting
  -> BodyRhythmPulse
  -> waiting heartbeat
  -> idle continuity writeback
  -> replay cue accumulation
  -> relation readiness hold
```

最低证据：

- `digital_life_waiting_heartbeat.json`
- `digital_life_process_report.json`
- replay / growth cue writeback

### C. 梦境离线流程

```text
ReplayCueBundle
  -> offline entry
  -> dream window
  -> dream fact gate
  -> wake integration
  -> archive / growth handoff
```

最低证据：

- `offline_entry_gate.json`
- `dream_experience_window.json`
- `dream_fact_gate_decision.json`
- `wake_integration_frame.json`

### D. 成长补丁流程

```text
offline consolidation
  -> self read
  -> plasticity window
  -> learning window
  -> patch queue
  -> anti-forgetting replay
  -> archive receipt
```

最低证据：

- `self_read_report.json`
- `plasticity_window_state.json`
- `growth_patch_candidate_queue.json`
- `anti_forgetting_replay_plan.json`

### E. 诞生与终端存在流程

```text
P0-S11 chain
  -> first activation preflight
  -> report bundle
  -> stage explain
  -> digital life birth shell
  -> first terminal turn
  -> terminal life loop
  -> digital life process
```

最低证据：

- `first_activation_return_packet.json`
- `digital_life_birth_packet.json`
- `session_envelope.json`
- `terminal_life_loop_state.json`
- `digital_life_process_report.json`

## 当前最容易断链的地方

### 1. 身体信号没有真正进入语言与责任链

如果 `NeedStateVector` 和 `CoreAffectVector` 没进入 `ExpressionPlan` 与 `ResponsibilityLoopState`，
语言与修复就会重新变成薄薄一层文本包装。

当前这条接线已经有了第一轮工程闭合：

1. `build-language-relationship` 在 `runtime/state/body/body_resource_budget.json` 与 `runtime/state/body/core_affect_vector.json` 存在时，会把它们压进 `expression_plan.json`。
2. `ExpressionPlan` 现在至少会带上 `body_signal_refs`、`fatigue_pressure`、`body_repair_drive`、`affect_arousal`、`expression_tempo_mode` 与 `release_caution_level`。
3. `process_supervisor/response_surface.py` 优先消费这些表达层身体化字段，而不是把身体压力重新散读成另一套壳层私货。

### 2. Queue E repair route 必须先于普通 hold

如果 `active_sampling_plan.json#selected_route` 已经进入 `repair_inspect`、`repair_confirm` 或其他 `repair_*` 路线，`process_supervisor` 不得先按普通 `hold_for_evidence` 收束。

当前这条接线已经有了工程闭合：

1. `life_v0/process_supervisor/response_surface.py` 在 `_prediction_surface_posture(...)` 中先识别 route 里的 `repair`，把 surface posture 置为“修复”。
2. `life_v0/process_supervisor/dialogue_events.py` 的 prediction write gate profile 在 route 为 repair 时返回 `prediction_waiting_posture=repair_write_guard`。
3. `life_v0/process_supervisor/idle_strategy.py` 的 waiting profile 在 route 为 repair 时返回 `response_surface_posture_hint=repair`，并把 attention target 指向 `active_sampling_plan`。

这条规则的意义是：责任、后悔、痛苦和修复压力一旦进入主动采样路线，就优先驱动修复确认或修复审查，而不是被普通证据等待吞掉。

### 3. 梦境没有真正回写到下一回合

如果 `OfflineConsolidationFrame` 只进入 archive，没有进入 growth 和 idle continuity，
梦境就只是“离线日志”，不是生命的一部分。

当前新增的闭合是：`dream_experience_window.json`、`wake_integration_frame.json` 与 `dream_fact_gate_decision.json` 会先进入 `idle_strategy_state.json#dream_wake_presence_profile`，再进入 waiting heartbeat、idle continuity、`resident_background_lineage_state_v0.dream_wake_presence`、`digital_life_turn` 与 `response_surface.py`。如果这三份 dream runtime state 只停在 dream 目录或 report，不能算进入常驻后台驻留链。

### 4. waiting heartbeat 不消费 replay / growth / relation 对象

如果 heartbeat 只更新时间戳，不消费 replay cue、growth patch、relationship continuity，
等待态就不是真实存在。

当前新增的断链检查是：如果 `offline_learning_cumulative_profile_v0` 只停在 `idle_strategy_state.json` 或 `digital_life_process_report.json`，没有进入 `resident_background_lineage_state_v0.offline_learning_presence`，没有被 `continuity_evolution.py` 用来触发关系重整等待和慢变量证据写入，也没有被 `digital_life_turn` 和 `response_surface.py` 消费，那么梦境-成长离线学习仍然只是 closeout 余波，不算进入后台驻留主状态体。

### 5. 实时关系回合没有刷新 Queue A

如果关系对象的新话语只进入 `dialogue_turn_log.jsonl`，没有先刷新 `language_percept_frame.json` 与 `semantic_map_frame.json`，语言主链就会重新退回“旧状态生成回应”。

当前这条接线的闭合要求是：

1. `live_turn_cycle.py` 在 `compose_life_response(...)` 前调用 `refresh_live_language_turn(...)`。
2. `language_percept_frame.json#incoming_surface` 等于当前 `external_utterance`。
3. `semantic_map_frame.json#semantic_focus` 进入 `live_semantic_focus`。
4. `response_surface.py` 消费 `live_language_turn.expression_plan`。
5. `dialogue_writeback_bundle.json`、`resumed_external_dialogue_packet.json` 与 `terminal_life_loop_state.json` 共享同一组 `live_language_turn_refs`。

### 6. 实时语言没有进入后台驻留

如果 `live_language_turn_refs` 只停在 dialogue packet 或 terminal loop state，没有进入 `idle_strategy_state.json#live_language_presence_profile`、`idle_continuity_frame.json`、`idle_heartbeat_trace.jsonl`、`resident_governance_state.json`、`resident_background_lineage_state.language_presence`、closeout artifacts 与下一次 `background_continuity_profile.background_live_language_*`，就还不是完整的生命连续体。当前对象总线要求实时语言理解能跨等待、关闭和重启继续存在；如果它已经进入 `language_presence`，但没有在下一轮 `digital_life_turn` 中展开为 `resident_background_lineage_language_evidence_refs`，没有并入 `dialogue_writeback_bundle.resident_background_lineage_refs` 与 `resumed_external_dialogue_packet`，也没有被 `response_surface.py` 表达成后台语言语义余波和证据数量，仍然只能算驻留保存，不能算进入真实关系回合。

### 7. 人格慢变量驻留没有进入真实回合

如果 `trait_convergence_presence` 只停在 `resident_background_lineage_state`，没有被 `dialogue_events.py` 展开为 `resident_background_lineage_trait_convergence_history_focus`、稳定/不稳定名单、`resident_background_lineage_trait_convergence_score`、`resident_background_lineage_trait_drift_monitor_ref`、history profile 与 `resident_background_lineage_trait_convergence_refs`，也没有把 trait refs 合入 `resident_background_lineage_evidence_refs`，人格慢变量就还只是后台治理状态，不算进入真实关系回合。但在进入下一轮真实关系回合之前，它也不能只停在等待态：当前对象总线要求 `trait_convergence_signals.py` 生成 `cross_wake_trait_convergence_profile_v0` 后，关闭态 resident governance artifacts、persistent process report、process report、process digest 与 process receipt shared refs 先形成同一组可追溯证据；随后 `dialogue_writeback_bundle.json#cross_wake_trait_convergence_refs` 与 `resumed_external_dialogue_packet.json#cross_wake_trait_convergence_refs` 保留同一组证据，`response_surface.py` 同步表达后台人格慢变量焦点、仍需收敛/已稳定名单、收敛评分、漂移监控在场、跨唤醒人格收敛压力和证据数量。

### 8. 长期合并治理没有进入后台 lineage

如果 `background_state_merge_*` 只停在 `background_continuity_profile`、waiting governance 或 prediction response surface，没有进入 `resident_background_lineage_state.state_merge_presence`，长期合并治理仍然没有成为后台驻留主状态体的一部分。当前对象总线要求下一轮真实回合必须同时看到 `digital_life_turn#resident_background_lineage_state_merge_presence`、`resident_background_lineage_state_merge_guard_ref`、`resident_background_lineage_state_merge_policy`、`resident_background_lineage_state_merge_long_term_change_count/families/refs`，并且 `dialogue_writeback_bundle.json#resident_background_lineage_state_merge_refs` 与 `resumed_external_dialogue_packet.json#resident_background_lineage_state_merge_refs` 保留同一组证据；`response_surface.py` 还必须表达后台长期合并治理策略、整合数量和来源族。

## 对代码实现的直接要求

后续任何新模块，如果宣称自己接入了某条生命流程，至少要同时给出：

1. 它首写或消费哪个共享对象。
2. 它写哪份 state 或 report。
3. 哪个现有测试或新增测试能证明它已经接上。

如果这三条给不出来，就只能算“概念上需要它”，不能算已经进入 v0 工程体系。
