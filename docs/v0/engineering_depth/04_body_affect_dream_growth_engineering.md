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

下一轮应新增：

1. `tests/slices/test_body_affect_runtime.py`
2. `tests/bridges/test_dream_runtime.py`
3. `tests/bridges/test_learning_promotion.py`
