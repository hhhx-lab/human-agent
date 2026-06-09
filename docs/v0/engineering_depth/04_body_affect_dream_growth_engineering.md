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

下一轮应新增：

1. `tests/slices/test_body_affect_runtime.py`
2. `tests/bridges/test_dream_runtime.py`
3. `tests/bridges/test_learning_promotion.py`
