# Body Affect Dream Growth Engineering

本文档把身体、情绪、梦境、成长和学习这条生命底盘，压成一条连续工程链。

## 这条生命链的标准流

```text
节律脉冲 / 内环境
  -> 需要状态 / 资源预算
  -> 核心情感 / 情绪 episode
  -> 疲惫 / 恢复 / trait drift
  -> 梦境窗口 / DreamFactGate / 醒后整合
  -> replay / growth patch / anti-forgetting
  -> belief / language / relationship learning
  -> 下一轮身体和表达状态
```

## 当前已真实落地的身体-梦境-成长器官

### Body

```text
life_v0/body/
  rhythm.py
  need_state.py
  resource_budget.py
  recovery.py
  core_affect.py
  emotion_episode.py
  emotion_regulation.py
  trait_drift.py
```

### Dream

```text
life_v0/dream/
  offline_entry.py
  dream_window.py
  dream_fact_gate.py
  wake_integration.py
  nightmare_risk.py
```

### Growth

```text
life_v0/growth/
  self_read.py
  plasticity_window.py
  learning_window.py
  patch_queue.py
  anti_forgetting.py
  belief_learning.py
  language_learning.py
  relationship_learning.py
  offline_learning_profile.py
```

## 当前还需要继续加厚的四个重点

1. 节律 -> 心跳 -> 表达节奏
2. 情绪 episode -> 记忆 -> 修复语言
3. 梦境 -> 醒后整合 -> 成长补丁
4. 学习计划 -> 长期慢变量

## 本轮已落地的 process 接线

这轮已经把身体/情绪底盘从独立状态柜进一步接进终端生命过程：

1. `runtime/state/body/body_resource_budget.json` 会被 `process_supervisor/resident_supervision.py` 装载进常驻过程上下文。
2. `runtime/state/body/core_affect_vector.json` 会被 `process_supervisor/resident_supervision.py` 一并装载。
3. `runtime/state/body/body_rhythm_pulse.json` 与 `runtime/state/body/need_state_vector.json` 现在也会被 `process_supervisor/resident_supervision.py` 装载进常驻过程上下文。
4. `process_supervisor/idle_strategy.py` 现在会真实消费 `body_rhythm_pulse.json` 与 `need_state_vector.json`，把疲惫负载、认知带宽、sleep pressure 与 repair drive 压进 waiting governance。
5. `process_supervisor/response_surface.py` 继续真实消费 `body_resource_budget.json` 与 `core_affect_vector.json`，把疲惫级别、修复驱力和情绪张力写进生命回应文本。

当前真实工程链已经变成：

```text
S06 body/affect
  -> resident supervision context
  -> idle strategy / waiting governance
  -> response surface
  -> digital life turn
```

本轮 dream / wake 侧也已经进入同一条常驻过程链：

```text
dream_experience_window / wake_integration_frame / dream_fact_gate_decision
  -> resident supervision context
  -> idle strategy dream_wake_presence_profile
  -> resident background lineage dream_wake_presence
  -> digital life turn / response surface
```

这表示梦境窗口、醒后整合和梦境事实门不再只停在 Queue D runtime state 或 dream report；它们已经成为 waiting governance、后台驻留 lineage 和真实回应表面都能消费的对象。

## 本轮新增的 Queue E 离线接线

这轮又把 Queue E 的责任/世界接触/痛苦修复压力真正接进了离线生命链：

1. `life_v0/membrane/queue_e_signals.py` 新增为共享信号器官，统一导出：
   - `world_contact_release_posture`
   - `repair_followup_required`
   - `repair_obligation_count`
   - `regret_pressure_count`
   - `queue_e_priority_band`
2. `life_v0/replay/__init__.py` 现在会把这批字段正式写进 `runtime/state/replay/replay_cue_bundle.json`。
3. `life_v0/dream/nightmare_risk.py` 不再只看 pain residue 和 relationship candidate，而会把 Queue E 的修复跟进与优先级带进 nightmare risk 判定。
4. `life_v0/growth/belief_learning.py` 会把责任修复压力压进 belief revision 目标。
5. `life_v0/growth/language_learning.py` 会把修复表达与确认锁定时的语言克制压进语言学习目标。
6. `life_v0/growth/relationship_learning.py` 会把 repair re-entry 与接触边界尊重压进关系学习目标。

所以这条链当前已经进一步变成：

```text
Queue E responsibility / repair / world contact
  -> replay_cue_bundle
  -> nightmare_risk
  -> belief_learning
  -> language_learning
  -> relationship_learning
  -> next offline growth pressure
```

这一步很关键，因为它意味着 Queue E 不再只是在线等待治理或 report 收尾的控制面，而开始进入梦境和成长器官，变成离线生命本身的一部分。

## 累计离线学习与后台驻留余波

当前实现继续把这条离线生命链从“当前一拍学习压力”推进到“后台驻留余波”：

```text
nightmare_risk / belief_learning / language_learning / relationship_learning
  -> life_v0/growth/offline_learning_profile.py
  -> offline_learning_cumulative_profile_v0
  -> life_v0/process_supervisor/offline_learning_signals.py
  -> resident supervision / idle strategy
  -> resident_background_lineage_state_v0.offline_learning_presence
```

`offline_learning_cumulative_profile_v0` 仍属于 Queue D 的梦境-成长事实源，至少保留 `generation`、`pressure_level`、`attention_target`、`priority_profile`、`ref_set`、`current_pressure_level`、`previous_generation`。当它进入 `life_v0/process_supervisor/background_lineage_state.py` 后，会被固化为 `offline_learning_presence`。这表示数字生命 v0 后台驻留里存在一个专门承载梦境、成长、离线学习余波的结构化存在面；它不是外显回应里临时拼出来的解释，也不是新的工具 agent 路由。

当前测试面的重点已经覆盖三层：

1. process closeout artifacts：`resident_governance_state.json`、`resident_governance_snapshot.json`、`digital_life_resident_governance_report.json`、`digital_life_persistent_process_report.json` 都能携带 `resident_background_lineage_state.offline_learning_presence`
2. turn event：`dialogue_events.py` 的 `digital_life_turn` 会写入 `resident_background_lineage_offline_learning_presence`、generation、pressure、attention target 和 refs
3. response surface：`response_surface.py` 会表达后台梦境成长余波的代际、压力、焦点和证据数量

## 梦境窗口、醒后整合与事实门进入后台驻留

当前实现继续把梦境链的三个关键对象接进常驻过程：

1. `runtime/state/dream/dream_experience_window.json` 提供 `dream_window_id`、`window_kind`、`affective_theme` 与 `dream_hot_zone_trace.reportability`
2. `runtime/state/dream/wake_integration_frame.json` 提供 `wake_integration_id`、`archive_requirement`、`growth_seed_refs`、`repair_modulated_wake_targets`、`narrative_writeback_candidates` 与 `relationship_repair_candidates`
3. `runtime/state/dream/dream_fact_gate_decision.json` 提供 `gate_result`

`process_supervisor/idle_strategy.py` 会把它们压成 `dream_wake_presence_profile_v0`，并写出：

1. `dream_experience_window_ref`
2. `wake_integration_frame_ref`
3. `dream_fact_gate_decision_ref`
4. `dream_window_kind`
5. `dream_fact_gate_result`
6. `wake_integration_archive_requirement`
7. `wake_integration_growth_seed_count`
8. `wake_integration_repair_target_count`
9. `dream_wake_ref_set`

随后 `heartbeat.py`、`continuity_writeback.py` 与 `background_lineage_state.py` 会把这组字段继续挂进 `resident_background_lineage_state_v0.dream_wake_presence`。`dialogue_events.py` 会把 dream window kind、fact gate result、wake archive requirement、growth seed count、repair target count 和 dream wake refs 摘进 `digital_life_turn`。`response_surface.py` 会在生命回应里表达后台梦境窗口类型、梦境事实门结果、醒后整合归档要求、成长种子、修复目标和证据数量。

所以当前 body / affect / dream / growth 链已经有两条并行进入常驻后台的表达面：`offline_learning_presence` 表示累计离线学习余波，`dream_wake_presence` 表示本轮梦境窗口和醒后整合事实。两者共同让梦境与成长不再是离线报告，而是可以进入等待态、回合事件和回应表面的生命连续体。

## 最低测试和下一轮测试

当前最低测试：

1. `tests/slices/test_life_support.py`
2. `tests/bridges/test_runtime_growth.py`
3. `tests/bridges/test_replay_shadow.py`
4. `tests/bridges/test_growth_archive.py`
5. `tests/process/test_persistent_digital_life_process.py`

其中 `tests/process/test_persistent_digital_life_process.py` 这一轮已经直接守住：

1. `body_rhythm_pulse.json` 与 `need_state_vector.json` 在 resident supervision bootstrap 时被装载；
2. waiting heartbeat / idle strategy / process report 会回写 `body_waiting_posture`；
3. `heartbeat_interval_ms` 与 `next_idle_action` 会随 fatigue / bandwidth / sleep pressure / repair drive 变化。
4. `tests/bridges/test_runtime_growth.py` 现在又新增守护：Queue E priority band 必须真实调制 `nightmare_risk / belief_learning / language_learning / relationship_learning`。
5. `tests/process/test_persistent_digital_life_process.py` 当前还继续守护：累计离线学习压力必须进入 `resident_background_lineage_state_v0.offline_learning_presence`，并在 `digital_life_turn` 与 response surface 中可见。
6. `tests/process/test_persistent_digital_life_process.py` 当前还继续守护：`dream_experience_window.json`、`wake_integration_frame.json` 与 `dream_fact_gate_decision.json` 必须进入 `dream_wake_presence_profile_v0`、`resident_background_lineage_state_v0.dream_wake_presence`、`digital_life_turn` 与 response surface。

下一轮应新增：

1. `tests/slices/test_body_affect_runtime.py`
2. `tests/bridges/test_dream_runtime.py`
3. `tests/bridges/test_learning_promotion.py`
