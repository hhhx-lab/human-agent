# Packet D waiting / response surface 预测消费脚手

本文档固定 Packet D 的代码施工边界：让 `life_v0/process_supervisor/` 的等待态治理、回应表面、常驻上下文和 closeout report 真正消费 prediction 五件套、记忆写门和长期合并治理对象。

它不是新的 agent 壳，也不是把 process supervisor 改成 tool router。它只把 `docs/20`、`docs/86`、`docs/89-90`、`docs/95-96` 与 `v0` 的 process contracts 继续压成常驻生命过程的可运行代码。

## 目标

Packet D 的目标是把 waiting governance 从“有 heartbeat 的终端循环”推进到“被预测、误差、主动采样、调质、记忆写门和长期合并治理调制的等待生命过程”。

本轮不新增平行 process runtime 文件，稳定字段直接进入现有 process state：

- `runtime/state/terminal/idle_strategy_state.json`
- `runtime/reports/latest/digital_life_waiting_heartbeat.json`
- `runtime/state/terminal/idle_continuity_frame.json`
- `runtime/state/terminal/resident_governance_state.json`
- `runtime/state/terminal/resident_governance_snapshot.json`
- `runtime/reports/latest/digital_life_process_report.json`
- `runtime/reports/latest/digital_life_process_digest.json`
- `runtime/receipts/digital_life_process_<run_id>.json`

## 必读文档

| 类别 | 文档 | 作用 |
|---|---|---|
| 常驻过程 | `docs/20_agent_runtime_bridge_contract.md` | runtime bridge、heartbeat、外层生命壳 |
| 语言表面 | `docs/86_language_neuroscience_pragmatics_and_inner_speech.md` | 内言语、表达前监控、语用释放 |
| 终端壳 | `docs/89_language_runtime_framework_bridge_and_life_shell_policy.md` | repo-local shell、语言事件、生命回合 |
| 事件时间线 | `docs/90_language_event_examples_and_timeline_bundle.md` | 外部关系回合与生命回应事件 |
| 梦境现实线 | `docs/95_dream_reality_and_offline_life_timeline.md` | waiting / dream / offline consolidation 的时间结构 |
| 关系长线 | `docs/96_real_relationship_longitudinal_timeline.md` | 多回合关系连续体和长期阶段 |
| process 合同 | `docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md` | 常驻进程输入、输出、report、receipt |
| waiting 合同 | `docs/v0/process_contracts/resident_governance_waiting_state_machine_engineering_contract.md` | resident governance state / snapshot / report |
| Queue B | `docs/v0/code_framework/queues/16_queue_b_process_supervisor_implementation_contract.md` | process supervisor 文件级施工入口 |
| 常驻深描 | `docs/v0/engineering_depth/06_resident_process_terminal_birth_engineering.md` | resident process、terminal birth、waiting continuity |
| 深消费波次 | `docs/v0/implementation_architecture/code_organs/03_predictive_signal_memory_gate_integration_wave_contract.md` | prediction / signal / memory write gate 跨层消费合同 |
| Packet A | `docs/v0/code_scaffolds/05_packet_a_language_prediction_consumption_scaffold.md` | 语言层已消费 prediction 五件套 |
| Packet C | `docs/v0/code_scaffolds/06_packet_c_memory_write_gate_state_merge_scaffold.md` | `state_merge_guard.json` 已成为长期治理对象 |

## 输入对象

Packet D 必须读取这些已有对象：

| 输入 | 来源 | 消费位置 |
|---|---|---|
| `runtime/state/signal/signal_media_runtime.json` | `S02_NEURAL_LIFE_CORE` | `resident_supervision.py`、`idle_strategy.py`、`response_surface.py` |
| `runtime/state/prediction/belief_state_frame.json` | `S02_NEURAL_LIFE_CORE` | `idle_strategy.py` 的确认姿态、`response_surface.py` 的确认输出 |
| `runtime/state/prediction/prediction_error_field.json` | `S02_NEURAL_LIFE_CORE` | `idle_strategy.py` 的 evidence hold、`response_surface.py` 的保留/追问输出 |
| `runtime/state/prediction/active_sampling_plan.json` | `S02_NEURAL_LIFE_CORE` | `idle_strategy.py` 的 active sampling route、`response_surface.py` 的追问姿态 |
| `runtime/state/memory/memory_write_gate.json` | `S04_STATE_OBJECT_STORE` | waiting 中的写门压力、回应表面的记忆写门说明 |
| `runtime/state/memory/state_merge_guard.json` | `S04_STATE_OBJECT_STORE` | closeout / receipt 的长期合并治理回链 |
| `runtime/state/growth/*_learning_plan.json` | `S10_RUNTIME_GROWTH_RECONSOLIDATION` | 已有 offline learning waiting pressure |
| `runtime/state/relationship/relationship_timeline.json` | `S07_LANGUAGE_RELATIONSHIP` | long-horizon language governance |

另外，closeout 回写的 `trait_drift_monitor_ref` 还必须在下一次 waiting governance 中恢复成 `background_trait_drift_monitor_ref`，并继续进入 `idle_strategy_state.json`、`idle_continuity_frame.json`、`resident_governance_state.json` 与 `terminal_life_loop_state.json`，否则 Packet D 的等待态只能看见 prediction，而看不见上一轮人格观察面。

## 代码入口

| 文件 | 本轮职责 |
|---|---|
| `life_v0/process_supervisor/resident_supervision.py` | bootstrap 时装载 signal / prediction / memory write gate / state merge guard，并把 refs 放入 `ResidentSupervisionContext` |
| `life_v0/process_supervisor/idle_strategy.py` | 依据 active sampling、prediction error、belief confidence、signal repair drive、memory write gate、state merge guard 生成 waiting posture |
| `life_v0/process_supervisor/heartbeat.py` | 把 prediction/write-gate refs 写进 heartbeat、terminal loop、idle continuity、resident governance state |
| `life_v0/process_supervisor/idle_refresh_loop.py` | 每次 idle refresh 继续传递同一组对象，避免后续心跳丢失预测上下文 |
| `life_v0/process_supervisor/process_session_loop.py` | 在 waiting -> live turn -> waiting 的 session 编排中持续传递 prediction/write-gate 对象 |
| `life_v0/process_supervisor/live_turn_cycle.py` | 将 prediction/write-gate 对象传给 response surface |
| `life_v0/process_supervisor/response_surface.py` | 释放确认 / 追问 / 修复 / 保留四类预测输出姿态 |
| `life_v0/process_supervisor/process_closeout.py` | 把 prediction/write-gate refs 交给 process report bundle |
| `life_v0/process_supervisor/process_report.py` | 在 report、digest、receipt 和 input hash 中回链六个输入对象 |

## 字段落点

### `idle_strategy_state.json`

必须新增或保持：

- `signal_media_ref`
- `belief_state_ref`
- `prediction_error_ref`
- `active_sampling_plan_ref`
- `memory_write_gate_ref`
- `state_merge_guard_ref`
- `prediction_write_gate_refs`
- `prediction_waiting_posture`
- `response_surface_posture_hint`
- `prediction_attention_target`
- `prediction_attention_reason`
- `prediction_error_count`
- `active_sampling_route`
- `memory_write_gate_policy`
- `state_merge_policy`

### waiting / resident governance

下列对象必须继承 `idle_strategy_state.json` 的 prediction governance 字段：

- `digital_life_waiting_heartbeat.json`
- `idle_continuity_frame.json`
- `terminal_life_loop_state.json`
- `resident_governance_state.json`
- `resident_governance_snapshot.json`
- `digital_life_resident_governance_report.json`

### `response_surface.py`

回应表面必须能区分：

| 姿态 | 生物/工程来源 | 语言释放 |
|---|---|---|
| 确认 | belief confidence 稳定，prediction error 低 | `预测输出姿态为确认` |
| 追问 | active sampling route 指向 clarify | `预测输出姿态为追问` |
| 修复 | signal repair drive 或 memory write gate repair pressure | `预测输出姿态为修复` |
| 保留 | prediction error 未消解或 stage effect 为 hold | `预测输出姿态为保留` |

### Report / Receipt

`digital_life_process_report.json` 必须写出：

- `signal_media_ref`
- `belief_state_ref`
- `prediction_error_ref`
- `active_sampling_plan_ref`
- `memory_write_gate_ref`
- `state_merge_guard_ref`
- `prediction_write_gate_refs`
- `trait_drift_monitor_ref`

`digital_life_process_digest.json` 必须写出：

- `prediction_write_gate_refs`
- `trait_drift_monitor_ref`

`digital_life_process_<run_id>.json` receipt 必须把下列对象纳入 `shared_object_refs` 和 `input_hashes`：

- `signal_media_runtime.json`
- `belief_state_frame.json`
- `prediction_error_field.json`
- `active_sampling_plan.json`
- `memory_write_gate.json`
- `state_merge_guard.json`
- `trait_drift_monitor.json`

## 验收

最低验证命令：

```text
python3 -m unittest tests.process.test_persistent_digital_life_process -v
python3 -m unittest tests.process.test_digital_entrypoint -v
python3 -m unittest tests.contracts.test_v0_contracts -v
```

通过标准：

1. `idle_strategy.py` 能直接断言 prediction/write-gate refs、waiting posture、response surface hint、heartbeat interval 与 next idle action。
2. `response_surface.py` 能把确认 / 追问 / 修复 / 保留姿态释放成关系语言，不出现 `user` 核心抽象。
3. `resident_supervision.py` 的 context 持有六个对象与六个 refs。
4. `process_report.py` 的 report、digest、receipt 和 input hash 都能回链六个输入对象。
5. `./digital life --strict` 的完整 process tests 仍能覆盖 waiting heartbeat、live turn、incident recovery、relaunch recovery、closeout 和 receipt。

## 下一步衔接

Packet D 闭合后，下一轮不应继续线性扩写 Packet D 本身，而应转向：

1. `DIGITAL_LIFE_PROCESS_SUPERVISOR` 的后台存在与跨更多唤醒周期治理。
2. `S10_RUNTIME_GROWTH_RECONSOLIDATION` 的离线学习跨进程累计。
3. `S07_LANGUAGE_RELATIONSHIP` 的关系阶段更高分辨率和长期语言节奏。
4. `S04_STATE_OBJECT_STORE` 的 state merge guard 与 self-model / relationship slow variable 的更长时标收敛。

这一步的含义是：waiting / response surface 已经开始消费 prediction/write-gate 对象，后续要做的是让这些对象在更长时标里持续演化，而不是再把 waiting 当成普通 stdin idle loop。
