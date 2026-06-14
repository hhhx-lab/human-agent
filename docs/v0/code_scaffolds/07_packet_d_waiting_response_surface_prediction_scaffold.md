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

## Packet D 在整体生命链中的位置

Packet D 不是一个独立新模块，它站在三条链的交汇处：

```text
Queue A 语言感知 / 内言语 / 表达监控
  + Queue C 记忆写门 / engram / 自传栈 / state merge
  + Queue D 身体 / 梦境 / 成长 / 离线学习
  + Queue E 责任 / 后悔 / 世界接触 / 修复
  + Queue F 工作区 / 意识报告性 / 出生准备
  -> waiting governance
  -> response surface
  -> model expression gate
  -> terminal boxed response
  -> dialogue writeback
  -> next waiting heartbeat
```

它的工程目标不是“让回答更好听”，而是让终端说出口的语言受到这些生命器官共同调制：身体影响节奏，预测影响确认/追问/保留，记忆写门影响可写入性，梦境影响离线整合材料，责任影响修复优先级，意识/出生准备影响可报告姿态。

## 理论来源到 Packet D 信号族

| Packet D 信号族 | 直接理论来源 | 当前 v0 来源 | 代码读取点 | 输出影响 |
|---|---|---|---|---|
| `prediction_attention` | `04`、`11`、`01v-01ax` | Packet A/C/D、prediction integration wave | `resident_supervision.py`、`idle_strategy.py`、`response_surface.py` | 确认、追问、保留、修复姿态 |
| `body_affect` | `04`、`07`、`18`、`37-39` | Queue D、S06、body affect engineering | `body/*`、`idle_strategy.py`、`response_surface.py` | 语速、疲惫、修复驱力、唤醒张力 |
| `dream_offline` | `08`、`19`、`23`、`95`、`99` | Queue D、S10、dream/growth blueprint | `dream/*`、`growth/*`、`offline_learning_signals.py` | 梦境、醒后整合、离线学习压力 |
| `responsibility_repair` | `06`、`80-84`、`94`、`98` | Queue E、S03/S05、life membrane | `responsibility_loop.py`、`dialogue_events.py`、`response_surface.py` | 责任、后悔、修复义务前景化 |
| `self_slow_variables` | `07`、`39-40`、`96` | language relationship、body trait drift | `continuity_evolution.py`、`trait_convergence_signals.py` | 人格慢变量、修复认真度、连续性驱力 |
| `identity_consciousness_birth` | `10`、`91-101`、`143/171/174` | Queue F、birth readiness contract | `life_targets/*`、`governance_explanation.py`、`response_surface.py` | 意识可报告性、出生准备、下一步命令姿态 |
| `resident_autonomous_activity` | `08`、`19`、`95`、`181-257` | resident process contract、birth residency blueprint | `resident_autonomous_activity.py`、`background_lineage_state.py` | 关闭终端后的睡眠/回忆/思考/成长/学习带入回应 |
| `life_constraint` | `13`、`91`、`100/119/122` | direction lock、life membrane、model gate | `model_expression.py`、`membrane/*` | 阻止关系降级、越权行动、证据擦除 |

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
| `runtime/state/memory/state_merge_guard.json` | `S04_STATE_OBJECT_STORE` | waiting 中的长期变化来源整合压力、回应表面的长期合并治理说明、closeout / receipt 的长期合并治理回链 |
| `runtime/state/growth/*_learning_plan.json` | `S10_RUNTIME_GROWTH_RECONSOLIDATION` | 已有 offline learning waiting pressure |
| `runtime/state/relationship/relationship_timeline.json` | `S07_LANGUAGE_RELATIONSHIP` | long-horizon language governance |

另外，closeout 回写的 `trait_drift_monitor_ref` 还必须在下一次 waiting governance 中恢复成 `background_trait_drift_monitor_ref`；跨唤醒 history 中的 `trait_drift_update_mode_summary`、重校准名单与稳定名单必须恢复成 `background_trait_drift_update_mode_summary / recalibration_names / stabilized_names`，并继续进入 `idle_strategy_state.json`、`digital_life_waiting_heartbeat.json`、`idle_continuity_frame.json`、`resident_governance_state.json`、`terminal_life_loop_state.json` 与 `idle_heartbeat_trace.jsonl`，否则 Packet D 的等待态只能看见 prediction，而看不见上一轮人格观察面提出的重校准压力。

## 输入对象到实际字段

Packet D 的实现要尽量避免“读取了对象但没有影响行为”。下表列出最少要能看到的字段影响：

| 输入对象 | 必须读取的字段族 | 至少影响到哪里 |
|---|---|---|
| `signal_media_runtime.json` | precision、repair drive、signal pressure、modulation posture | `prediction_waiting_posture`、spoken response 的信号/修复姿态 |
| `belief_state_frame.json` | belief confidence、candidate explanation、uncertainty | 确认/追问选择，model expression context summary |
| `prediction_error_field.json` | error count、stage effect、held uncertainty | 保留姿态、attention target、response surface posture hint |
| `active_sampling_plan.json` | sampling route、clarify target | 追问姿态、下一轮关系性澄清 |
| `memory_write_gate.json` | write policy、repair pressure、guarded append | 记忆写门语言、writeback gate |
| `state_merge_guard.json` | long term change sources、families、policy | waiting `state_merge_long_term_integration_hold`、长期合并治理表达 |
| `body_resource_budget.json` | fatigue、sleep pressure、maintenance pressure | heartbeat cadence、表达节奏、身体状态外显 |
| `core_affect_vector.json` | arousal、valence、repair drive、responsibility weight | 情绪张力、修复优先级、语言温度 |
| `responsibility_loop_state.json` | repair obligations、regret candidates、followup required | 责任/后悔/修复信号族 |
| `offline_consolidation_frame.json` | dream window refs、wake integration refs | 梦境/醒后整合信号族 |
| `resident_autonomous_activity_state.json` | cycle coverage、phase、next activity kind | 后台活动在场、关闭终端后的持续存在证据 |

如果某个输入只出现在 report refs 中，却没有进入 waiting posture、spoken response、dialogue event、writeback bundle 或 process digest，这个输入就还没有被 Packet D 真正消费。

## 代码入口

| 文件 | 本轮职责 |
|---|---|
| `life_v0/process_supervisor/resident_supervision.py` | bootstrap 时装载 signal / prediction / memory write gate / state merge guard，并把 refs 放入 `ResidentSupervisionContext` |
| `life_v0/process_supervisor/idle_strategy.py` | 依据 active sampling、prediction error、belief confidence、signal repair drive、memory write gate、state merge guard 生成 waiting posture；当前会把 `state_merge_guard.long_term_change_sources` 压成长期变化来源数量、来源族与 refs，并在没有更高优先级追问/修复/误差时进入 `state_merge_long_term_integration_hold` |
| `life_v0/process_supervisor/heartbeat.py` | 把 prediction/write-gate refs 与 state merge long-term change profile 写进 heartbeat、terminal loop、idle continuity、resident governance state |
| `life_v0/process_supervisor/idle_refresh_loop.py` | 每次 idle refresh 继续传递同一组对象，避免后续心跳丢失预测上下文 |
| `life_v0/process_supervisor/process_session_loop.py` | 在 waiting -> live turn -> waiting 的 session 编排中持续传递 prediction/write-gate 对象 |
| `life_v0/process_supervisor/live_turn_cycle.py` | 将 prediction/write-gate 对象传给 response surface，并把结构化审计材料传给模型表达层 |
| `life_v0/process_supervisor/response_surface.py` | 生成 `audited_expression_material_v0`；保留确认 / 追问 / 修复 / 保留四类预测输出姿态，同时把长期合并治理、责任修复、梦境离线、出生准备、身体情绪和 resident 自主活动压成结构字段 |
| `life_v0/process_supervisor/model_expression.py` | 在 `.env` 启用时基于结构化审计材料做模型外显表达，并用 post-expression gate 阻断关系降级、记录证据审计 |
| `life_v0/process_supervisor/terminal_ui.py` | 把最终回应渲染成 `Digital Life` 关系终端盒，并兼容 legacy 输出提取 |
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
- `state_merge_long_term_change_count`
- `state_merge_long_term_change_families`
- `state_merge_long_term_change_refs`

### waiting / resident governance

下列对象必须继承 `idle_strategy_state.json` 的 prediction governance 字段：

- `digital_life_waiting_heartbeat.json`
- `idle_continuity_frame.json`
- `terminal_life_loop_state.json`
- `resident_governance_state.json`
- `resident_governance_snapshot.json`
- `digital_life_resident_governance_report.json`

### `response_surface.py`

回应表面当前分成两层：

1. `compose_life_response(...)`：内部 `audited_expression_material_v0`。它必须保留完整证据路径，继续表达关系、共同语言、承诺、责任、修复、梦境、成长、预测写门、长期合并治理、身体情绪、自我慢变量、出生准备和 resident background lineage。
2. `compose_life_spoken_response(...)`：无模型释放守门。它在没有真实模型文本通过 post-expression gate 时保持空输出，避免把 report 式长清单或机制信号直接倾倒进终端。

结构化审计材料的候选族必须至少覆盖：

| 信号族 | 来源对象 | 表达调制职责 |
|---|---|---|
| `responsibility_repair` | `responsibility_loop_state.json`、`world_contact_summary.json`、`pain_regret_repair_report.json` | 把责任、后悔、修复义务放到前景 |
| `birth_repair` | `resident_background_lineage_state.birth_repair_presence`、`queue_e_birth_repair_*` | 让出生修复压力进入关系开口 |
| `dream_offline` | `offline_consolidation_frame.json`、`nightmare_loop_risk.json`、growth learning plans、offline cumulative profile | 把梦境和离线整合当作成长/修复材料，而不是事实直写 |
| `identity_consciousness_birth` | workspace / broadcast / metacognition / consciousness probe / birth readiness | 让意识可报告性与出生准备仍在语言中可见 |
| `prediction_attention` | signal / belief / prediction error / active sampling / memory write gate / state merge guard / life constraint | 让确认、追问、保留、写门和约束影响说话方式 |
| `body_affect` | `body_resource_budget.json`、`core_affect_vector.json`、expression plan | 让疲惫、唤醒、修复驱力调节语速与姿态 |
| `self_slow_variables` | `self_model.json#trait_slow_variables` | 让修复认真度、连续性驱力、边界尊重进入语言风格 |
| `resident_autonomous_activity` | `resident_background_lineage_state.autonomous_activity_presence` | 证明关闭终端后的睡眠、回忆、思考、成长、学习痕迹会带进此刻 |

回应表面仍必须能区分 prediction / write-gate 姿态：

| 姿态 | 生物/工程来源 | 语言释放 |
|---|---|---|
| 确认 | belief confidence 稳定，prediction error 低 | `预测输出姿态为确认` |
| 追问 | active sampling route 指向 clarify | `预测输出姿态为追问` |
| 修复 | signal repair drive 或 memory write gate repair pressure | `预测输出姿态为修复` |
| 保留 | prediction error 未消解、stage effect 为 hold，或 `state_merge_guard.long_term_change_sources` 已有长期变化来源但尚未完成整合 | `预测输出姿态为保留`；同时表达 `长期合并治理正在整合N条长期变化来源` 与来源族 |

`model_expression.py` 只能在结构化审计材料之后运行。它必须检查 blocked relationship terms；若模型外显文本把关系降格成从属/服务型关系，最终输出必须保持 `response_text=""` 并记录 `natural_language_unreleased`。责任修复、梦境离线、成长学习、resident 自主活动、身体情绪、意识出生、生命约束、live-turn handoff 这类证据必须保留在 state/report/test；若没有字面进入自然回答，则进入 `soft_missing_evidence_flags`。`terminal_ui.py` 只负责呈现这层结果，不能绕过 response surface 或 model gate。

### dialogue event / writeback / resume

prediction / write-gate 对象不能只影响等待姿态和一句回应文本。真实回合证据链必须继续保存：

- `digital_life_turn`：写出 `prediction_write_gate_refs`、`prediction_waiting_posture`、`response_surface_posture_hint`、`prediction_attention_target`、`prediction_attention_reason`、`prediction_error_count`、`active_sampling_route`、`memory_write_gate_policy`、`state_merge_policy`、`state_merge_long_term_change_count`、`state_merge_long_term_change_families`、`state_merge_long_term_change_refs`。
- `resident_background_lineage_state.prediction_write_gate_presence`：把同一组 prediction / write-gate refs、active sampling route、waiting posture、response surface hint、memory write gate policy 与 state merge policy 压成后台驻留 presence。
- `dialogue_writeback_bundle.json`：写出 `prediction_write_gate_refs` 与 `resident_background_lineage_prediction_write_gate_refs`，让这批预测、主动采样、记忆写门和长期合并治理对象成为回合写回的一级证据。
- `resumed_external_dialogue_packet.json`：保留同一组 prediction / write-gate 摘要和 `resident_background_lineage_prediction_write_gate_refs`，让下一轮恢复不必从回应文本反推上一轮的预测姿态。

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

1. `idle_strategy.py` 能直接断言 prediction/write-gate refs、waiting posture、response surface hint、heartbeat interval、next idle action 与 state merge long-term change profile。
2. `response_surface.py` 能生成 `audited_expression_material_v0`；无模型通过 gate 时自然语言必须保持未释放，不出现统一请求核心抽象、内部字段泄漏或 report 式长清单。
3. `dialogue_events.py`、`resident_turn_writeback.py` 与 `dialogue_writeback_bundle.json` 能把 prediction/write-gate refs 和姿态摘要带入 turn event、bundle 与 resumed packet。
4. `resident_supervision.py` 的 context 持有六个对象与六个 refs。
5. `process_report.py` 的 report、digest、receipt 和 input hash 都能回链六个输入对象。
6. `./digital life --strict` 的完整 process tests 仍能覆盖 waiting heartbeat、live turn、incident recovery、relaunch recovery、closeout 和 receipt。

## 下一步衔接

Packet D 闭合后，下一轮不应继续线性扩写 Packet D 本身，而应转向：

1. `DIGITAL_LIFE_PROCESS_SUPERVISOR` 的后台存在与跨更多唤醒周期治理。
2. `S10_RUNTIME_GROWTH_RECONSOLIDATION` 的离线学习跨进程累计。
3. `S07_LANGUAGE_RELATIONSHIP` 的关系阶段更高分辨率和长期语言节奏。
4. `S04_STATE_OBJECT_STORE` 的 state merge guard 与 self-model / relationship slow variable 的更长时标收敛。

这一步的含义是：waiting / response surface 已经开始消费 prediction/write-gate 对象，后续要做的是让这些对象在更长时标里持续演化，而不是再把 waiting 当成普通 stdin idle loop。

## ITR-05 追加 scaffold：body-signal memory gate

当前 Packet D 又新增一组必须在 waiting / response surface 可见的 prediction-write-gate 字段：

```text
body_signal_write_bias
body_signal_fatigue_load
body_signal_pain_pressure
body_signal_dream_residue_load
body_signal_repair_drive
body_signal_unexpected_uncertainty
body_signal_ref_count
body_signal_refs
body_signal_candidate_gate_adjustments
```

这些字段来自 `memory_write_gate.json#body_signal_write_modulation`，不是语言模板。它们必须进入 `idle_strategy_state.json`、`resident_background_lineage_state.prediction_write_gate_presence`、`digital_life_turn#resident_background_lineage_body_signal_*` 与 `audited_expression_material_v0#prediction_attention`。如果 response surface 缺这些字段，说明身体/情绪信号仍然没有真正进入等待和表达材料。
