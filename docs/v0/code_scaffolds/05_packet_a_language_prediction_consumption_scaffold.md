# Packet A 语言预测消费脚手

本文档只固定 Packet A 的代码施工边界：让 `life_v0/language/` 真正消费已经落下的 prediction / signal / memory write gate 对象，并把消费痕迹写回现有语言 runtime。

它不是新的语言理论层，也不是新的 agent 壳层。它只把 `docs/09`、`docs/85-86`、`docs/10-11`、`docs/17`、`docs/21` 与 `v0` 现有合同继续压成可运行代码。

## 目标

Packet A 的目标是把语言系统从“独立生成语言状态”推进到“在预测、调质、记忆写门压力下形成语言状态”。

本轮不新建平行 runtime 文件，稳定字段直接进入现有四个语言 state：

- `runtime/state/language/language_percept_frame.json`
- `runtime/state/language/semantic_map_frame.json`
- `runtime/state/language/inner_speech_frame.json`
- `runtime/state/language/expression_monitor_state.json`

## 必读文档

| 类别 | 文档 | 作用 |
|---|---|---|
| 语言母体 | `docs/09_language_symbolic_top_layer.md` | 语言作为顶层表达系统 |
| 表达核心 | `docs/85_language_system_life_expression_core.md` | 语言、关系、生命表达的主轴 |
| 内言语与语用 | `docs/86_language_neuroscience_pragmatics_and_inner_speech.md` | inner speech、语用推断、表达前监控 |
| 意识工作区 | `docs/10_consciousness_attention_workspace.md` | 语言内容进入可报告工作区 |
| 调质信号 | `docs/11_neuromodulation_and_signal_media.md` | precision、repair drive、relationship pressure |
| 记忆对象 | `docs/17_memory_trace_object_model.md` | 语言事件与记忆候选对象 |
| 写入审计 | `docs/21_memory_schema_and_audit_protocol.md` | 写门、隔离、promotion / quarantine 路线 |
| S07 合同 | `docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md` | S07 输入、输出、gate 与 runtime 职责 |
| 语言 playbook | `docs/v0/code_framework/playbooks/04_language_dialogue_relationship_implementation_playbook.md` | language / relationship 代码施工入口 |
| 感知预测 playbook | `docs/v0/code_framework/playbooks/09_perception_prediction_world_contact_implementation_playbook.md` | prediction / observation / active sampling 消费方式 |
| 深消费波次 | `docs/v0/implementation_architecture/code_organs/03_predictive_signal_memory_gate_integration_wave_contract.md` | `signal_media / belief_state / prediction_error / active_sampling / memory_write_gate` 跨层消费合同 |

## 输入对象

Packet A 必须读取这些已有对象：

| 输入 | 来源 | 消费位置 |
|---|---|---|
| `runtime/state/signal/signal_media_runtime.json` | `S02_NEURAL_LIFE_CORE` | semantic map、inner speech、expression monitor、prediction workspace |
| `runtime/state/prediction/belief_state_frame.json` | `S02_NEURAL_LIFE_CORE` | language percept、inner speech、prediction workspace |
| `runtime/state/prediction/prediction_error_field.json` | `S02_NEURAL_LIFE_CORE` | semantic map、inner speech、prediction workspace |
| `runtime/state/prediction/active_sampling_plan.json` | `S02_NEURAL_LIFE_CORE` | language percept、inner speech、prediction workspace |
| `runtime/state/memory/memory_write_gate.json` | `S04_STATE_OBJECT_STORE` | expression monitor |
| `runtime/state/body/core_affect_vector.json` | `S06_LIFE_SUPPORT_DEVELOPMENT` | expression monitor；不存在时保留字段，存在后写入 ref |

## 代码入口

| 文件 | 本轮职责 |
|---|---|
| `life_v0/language/percept.py` | 将 belief scope、active sampling route 与 percept focus trace 写进 language percept |
| `life_v0/language/semantic_map.py` | 将 prediction error 与 signal media 写进 semantic prediction trace |
| `life_v0/language/inner_speech.py` | 依据 percept / semantic / error / signal 形成 confirm、hold、repair、ask 四类内部驱动 |
| `life_v0/language/expression_monitor.py` | 将 memory write gate、core affect、signal media 压进表达监控 |
| `life_v0/language/__init__.py` | 在 S07 runner 中统一读取输入、传入器官、写 report / receipt / check gate |
| `life_v0/neural_core/prediction_workspace.py` | 保留 S07 回写后的 prediction refs 与 signal refs |

## 字段落点

### `language_percept_frame.json`

必须新增或保持：

- `belief_state_ref`
- `active_sampling_plan_ref`
- `prediction_focus`
- `percept_focus_trace`

### `semantic_map_frame.json`

必须新增或保持：

- `prediction_error_ref`
- `signal_media_ref`
- `semantic_prediction_trace`
- `prediction_hooks.prediction_error_refs`
- `prediction_hooks.signal_media_refs`

### `inner_speech_frame.json`

必须新增或保持：

- `belief_state_ref`
- `prediction_error_ref`
- `active_sampling_plan_ref`
- `signal_media_ref`
- `internal_drive_sources.confirm`
- `internal_drive_sources.hold`
- `internal_drive_sources.repair`
- `internal_drive_sources.ask`
- `drive_resolution_order`

### `expression_monitor_state.json`

必须新增或保持：

- `memory_write_gate_ref`
- `core_affect_vector_ref`
- `signal_media_ref`
- `write_gate_pressure`
- `affect_expression_modulation`

## Report / Receipt

`language_relationship_report.json` 必须写出：

- `prediction_language_consumption_refs`
- `state_refs` 中包含 prediction / signal / memory write gate 输入
- 原有 `prediction_language_handoff_refs` 继续保留

`language_relationship_<run_id>.json` receipt 必须对下列输入做 hash：

- `signal_media_runtime.json`
- `belief_state_frame.json`
- `prediction_error_field.json`
- `active_sampling_plan.json`
- `memory_write_gate.json`

## 验收

最低验证命令：

```text
python3 -m unittest tests.slices.test_language_organs -v
python3 -m unittest tests.slices.test_language_relationship -v
python3 -m unittest tests.contracts.test_v0_contracts -v
```

通过标准：

1. 器官级测试能直接断言四个语言器官的新字段。
2. S07 端到端测试能断言 report、receipt、prediction workspace 都保留预测消费 refs。
3. V0 合同覆盖测试能收录本脚手文件，且本文件所有 `docs/...` 引用可解析。
4. 不出现 `user` 核心抽象，不引入 skill router / gateway / subagent 架构。

## 下一步衔接

Packet A 闭合后，默认进入：

1. Packet C：`memory_write_gate.json` 到长期治理链。
2. Packet D：waiting / response surface 深消费 prediction 五件套。

这两个后续包都必须继续读取本文件，因为语言层已经开始把 prediction / signal / write gate 压进表达前状态。
