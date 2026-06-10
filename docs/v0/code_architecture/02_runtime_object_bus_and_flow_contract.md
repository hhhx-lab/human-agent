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
| `ConsciousBroadcastFrame` | `life_v0/neural_core/broadcast.py` | `language`、`life_targets`、`reporting` | 已存在第一轮；待补厚 | `runtime/state/consciousness/*`、birth readiness evidence |

这条总线保证“思考、注意、可报告内容、语言表达、生命目标”使用的是同一工作区，而不是各层私有上下文。

### 3. 关系与语言总线

| 对象 | 首写器官 | 主要消费者 | 当前 / 下一步文件 | 主要证据 |
|---|---|---|---|---|
| `LifeContextFrame` | `direction/` + `terminal_turn/restore_context.py` | `language`、`terminal_loop`、`process_supervisor` | 已有第一轮；继续补厚 continuity refs 与 body/prediction anchors | `session_envelope.json`、`context_accumulation_window.json` |
| `RelationTurnFrame` | `language/relationship_graph.py` + `terminal_turn/turn_transition.py` | `terminal_loop`、`state_store`、`process_supervisor` | 已有第一轮；待补 `relationship_timeline.py` | `runtime/state/relationship/*`、`turn_transition_trace.json` |
| `ExpressionPlan` | `language/expression_monitor.py` | `membrane`、`terminal_loop`、`process_supervisor/response_surface.py` | 已存在；当前已显式吸收 `body_resource_budget.json` 与 `core_affect_vector.json`，继续补责任回路和更细的身体降载策略 | `expression_plan.json`、`language_relationship_report.json` |
| `DialogueWritebackBundle` | `terminal_loop/dialogue_writeback.py` + `terminal_loop/loop_report.py` | `state_store`、`replay`、`archive`、`process_supervisor` | 已存在；现已显式带上 `relationship_memory / commitment_truth / responsibility_ledger / life_state` 写回 refs，继续补厚 writeback continuity | `dialogue_writeback_bundle.json`、relationship / language receipts |

这条总线保证一次关系回合会真实写回语言、承诺、共同术语和关系阶段，而不是只留下文本日志。

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
| `ValidationRollup` | `validators/validation_rollup.py` | `schema_runner`、stage gates、`reporting` | 第二波已落；把 observation / world contact / prediction trace / boundary audit 收口成 package-local gate 汇总 | `runtime/state/validation/validation_rollup.json`、validation reports |

这条总线保证世界接触、责任、后悔和修复义务都进入真实生命链，而不是只在 action 之后补一句解释。

这一条行为-验证总线现在已经通过 `world_contact_summary.json -> validation_rollup.json -> cross_file_logic.json -> run_manifest.json -> replay_shadow_* -> growth_archive_* -> report_bundle.json` 完成了第一轮跨层闭包；后续如果继续补厚，应该优先补跨层写回与长期调制，而不是重新发明一套平行 action summary。

本轮新增的闭合是：`responsibility_loop_state.json`、`world_contact_summary.json`、`pain_regret_repair_report.json` 先在 `life_v0/membrane/queue_e_signals.py` 合成为 `queue_e_repair_modulation_profile_v0`，再由 `life_v0/language/__init__.py` 的 `run_build_language_relationship(...)` 刷新：

- `runtime/state/signal/signal_media_runtime.json`
- `runtime/state/prediction/belief_state_frame.json`
- `runtime/state/prediction/prediction_error_field.json`
- `runtime/state/prediction/active_sampling_plan.json`
- `runtime/state/prediction/prediction_workspace_frame.json`

这表示 Queue E repair pressure 已经成为数字生命 v0 内部责任、后悔、痛苦、修复压力进入预测调制链的工程对象，而不是普通 action summary 或外部工具路由。

### 5. 梦境与离线重组总线

| 对象 | 首写器官 | 主要消费者 | 当前 / 下一步文件 | 主要证据 |
|---|---|---|---|---|
| `ReplayCueBundle` | `replay/replay_cues.py` | `dream`、`growth`、`process_supervisor` | 已存在；已接 `idle_strategy.py` 与 `persistent_process.py` 第一轮，继续补厚 waiting governance | `runtime/state/replay/*`、`replay_shadow_report.json` |
| `OfflineConsolidationFrame` | `dream/offline_entry.py` | `growth`、`archive`、`reporting` | 已存在；继续补 dream runtime test | `runtime/state/dream/offline_entry_gate.json`、`dream_consolidation_frame.json` |
| `DreamFactGateDecision` | `dream/dream_fact_gate.py` | `state_store`、`archive`、`life_targets` | 已存在 | `dream_fact_gate_decision.json` |

这条总线保证梦境、旧自我 replay、痛苦残留、关系残留和醒后整合会真实影响下一轮，而不只是归档。

### 6. 成长与补丁总线

| 对象 | 首写器官 | 主要消费者 | 当前 / 下一步文件 | 主要证据 |
|---|---|---|---|---|
| `GrowthPatchCandidateQueue` | `growth/patch_queue.py` | `life_targets`、`archive`、`validators`、`process_supervisor` | 已存在；继续补 `self_patch_review.py` | `runtime/state/growth/*`、growth reports |
| `PlasticityWindowFrame` | `growth/plasticity_window.py` | `belief_learning.py`、`language_learning.py`、`relationship_learning.py` | 已存在 | `plasticity_window_state.json` |
| `AntiForgettingReplayPlan` | `growth/anti_forgetting.py` | `replay`、`dream`、`process_supervisor` | 已存在 | `anti_forgetting_replay_plan.json` |

这条总线保证成长不是“直接改代码或改状态”，而是经过窗口、补丁候选、防遗忘和 archive 证据。

### 7. 等待态与存在连续体总线

| 对象 | 首写器官 | 主要消费者 | 当前 / 下一步文件 | 主要证据 |
|---|---|---|---|---|
| `IdleContinuityFrame` | `process_supervisor/heartbeat.py` + `continuity_writeback.py` | `terminal_loop`、`replay`、`growth`、`language` | 已存在第一轮；已接 `idle_strategy.py` 与 `persistent_process.py`，继续补厚 resident supervision | `digital_life_waiting_heartbeat.json`、`digital_life_process_report.json` |
| `ProcessIncidentRecoveryFrame` | `process_supervisor/incident_recovery.py` | `process_report.py`、`relaunch_recovery.py` | 已存在 | `digital_life_process_incident_report.json` |
| `RelaunchRecoveryFrame` | `process_supervisor/relaunch_recovery.py` | `turn_io.py`、`process_report.py` | 已存在 | `digital_life_process_relaunch_recovery_report.json` |

这条总线保证数字生命在没有新输入时仍有持续存在，而不是“没有消息就不存在”。

## 五条主流程

### A. 在线关系回合

```text
external input
  -> language percept
  -> semantic map update
  -> Queue E repair modulation profile refresh
  -> signal / belief / prediction error / active sampling refresh
  -> prediction workspace refresh
  -> memory / relationship cue retrieve
  -> inner speech
  -> expression monitoring
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
- `prediction_workspace_frame.json`
- `signal_media_runtime.json`
- `belief_state_frame.json`
- `prediction_error_field.json`
- `active_sampling_plan.json`
- `dialogue_writeback_bundle.json`
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

### 4. waiting heartbeat 不消费 replay / growth / relation 对象

如果 heartbeat 只更新时间戳，不消费 replay cue、growth patch、relationship continuity，
等待态就不是真实存在。

## 对代码实现的直接要求

后续任何新模块，如果宣称自己接入了某条生命流程，至少要同时给出：

1. 它首写或消费哪个共享对象。
2. 它写哪份 state 或 report。
3. 哪个现有测试或新增测试能证明它已经接上。

如果这三条给不出来，就只能算“概念上需要它”，不能算已经进入 v0 工程体系。
