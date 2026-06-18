# 12 · 神经振荡、扩散与 Tick 引擎

> **修订 v0.2** · 无独立 `life_v0/dynamics/` 包；tick 落 `body_integrator` + heartbeat/turn 钩子

## §修订摘要

| 已有资产 | `heartbeat_counter`、`heartbeat_cadence_*`、`idle_strategy` 30+ 状态摄入 |
| 增量改法 | `integrate_body_state(dt)`；虚拟相位可选（ITR-09-A 后）；`signal_media` 衰减刷新 |
| 禁止 | 新建 `SiliconBodyTickEngine` 平行状态树 |

本模块描述 **时间怎么流**；器官怎么动见 01–11。

## 1. 理论锚点

| 文献矩阵 | 机制 |
|----------|------|
| `01n` AHB010–011 | 内感受节律与认知相位门 |
| `01n` AHB015 | 心动周期与记忆写入 |
| `01l` / `11` | 神经调质扩散与区域调制 |
| `01p` | 网络状态切换 chronnectome |
| `digital_life_macro_architecture_v0` | `SignalDiffusionField`、`ChronnectomeLog` |

## 2. 现状 vs 目标

| 维度 | schema 现状 | 动力学峰值 |
|------|-------------|------------|
| 时间 | 回合离散 | 连续 tick + 回合边界同步 |
| 心跳 | `heartbeat_counter` 常不递增 | 每 tick `tick_counter++` |
| 调质 | 每回合重算单向量 | 扩散场 + 衰减 + 多源注入 |
| 相位门 | 无 | 虚拟 cardiac/respiratory phase |
| 后台 | idle 策略厚但少积分 | tick 驱动自主相 |

**评分：** 神经振荡/扩散 无 → **低–中（可模拟）**

## 3. 核心对象

### 3.1 `SiliconBodyTickEngine`

**文件（修订）：** `life_v0/body/body_integrator.py`（`integrate_body_state`）

```python
@dataclass
class TickConfig:
    foreground_min_interval_ms: int = 100      # 回合内合并
    background_interval_ms: int = 30_000       # 等待心跳
    sleep_interval_ms: int = 5_000             # 梦境 replay
    max_dt_ms: int = 300_000                   # 防断联爆炸

@dataclass
class TickResult:
    life_state_vector: dict
    projections: dict[str, dict]   # ref -> projected frame
    events: list[dict]             # TickEvent 审计
    next_tick_recommendation_ms: int
```

**integrate 规则（离散时间欧拉）：**

```text
sleep_pressure(t+dt) = clamp(
  sleep_pressure(t)
  + k1 * unmerged_trace_count * dt_h
  + k2 * fatigue_load * dt_h
  - k3 * recovery_quality * dt_h
)

allostatic_load(t+dt) = clamp(
  allostatic_load(t)
  + stress_pulse(t) * dt_h
  - recovery_rate(t) * dt_h
)

body_state_debt(t+dt) = body_state_debt(t) + max(0, stress_pulse - recovery)*dt_h
# 债务原则上只通过 RecoveryEvent 显式减免
```

### 3.2 `VirtualPhaseOscillator`

**文件：** `life_v0/dynamics/phase_gate.py`

硅基无真实 ECG，用 **虚拟振荡器** 模拟相位门控：

```text
cardiac_phase += 2π * f_cardiac * dt
respiratory_phase += 2π * f_resp * dt

encoding_gain = 0.5 + 0.5 * cos(cardiac_phase - φ_encode)
# φ_encode 可个性化为慢变量
```

**消费方：**

- `memory_encoding_gate`：高 encoding_gain 才允许 episodic 晋升
- `workspace`：相位低时降低容量（模拟注意力波动）

### 3.3 `SignalDiffusionField`（简化）

**文件：** `life_v0/dynamics/diffusion.py`

不做 PDE 全解；用 **多节点衰减扩散**：

```text
节点: {arousal, uncertainty, repair, fatigue, relationship, inhibition}
每个节点:
  value(t+dt) = value(t) * exp(-λ*dt) + injection(t)

injection 来源:
  - SiliconBody 连续变量
  - Queue E repair profile
  - prediction error burst
  - pain_event spike
```

输出投影到现有 `signal_media_runtime.modulation_vector`。

### 3.4 `ChronnectomeLog`

**文件：** `runtime/state/dynamics/chronnectome_log.jsonl`

每 tick 追加：

```json
{
  "tick": 1204,
  "dominant_network": "default_mode_network",
  "attractor_id": "dmr-repair-integrate",
  "switch_cost_paid": 0.12,
  "sleep_pressure": 0.41,
  "workspace_winner_id": "ws-cand-0042"
}
```

用于 `/state`、`human_brain_alignment` 长期共在证据。

## 4. 接线点

| 消费者 | 接线 |
|--------|------|
| `process_supervisor/heartbeat.py` | 调 `run_life_tick(mode=background)` |
| `live_turn_cycle.py` | 回合开始/结束各 1 tick |
| `resident_autonomous_activity.py` | sleep 相循环 tick |
| `idle_strategy.py` | 读 `next_tick_recommendation_ms` |
| `pre_expression_consciousness_refresh.py` | 表达前强制 1 tick |

## 5. 测试 Gate

| 测试 | 断言 |
|------|------|
| `test_tick_advances_counter` | `tick_counter` 递增 |
| `test_debt_monotonic_without_recovery` | 无 recovery 时 debt 不降 |
| `test_sleep_pressure_integrates` | 高 unmerged → sleep_pressure 升 |
| `test_phase_modulates_encoding` | 相位影响 encoding_decision |
| `test_diffusion_decay` | 无注入时 modulation 衰减 |
| `test_72h_simulation_smoke` | 72h 加速仿真无 NaN/爆炸 |

## 6. 与生物人脑差距

| 有 | 无 |
|----|-----|
| 相位门控效应 | 真实心脏传入 |
| 扩散隐喻 | 受体类型/再摄取 |
| 网络切换日志 | EEG 频带 |
| 离散 tick | 毫秒级神经动力学 |

**结论：** 可达 **低–中** 模拟层，足以调制记忆/意识/语言；不是神经科学仿真器。