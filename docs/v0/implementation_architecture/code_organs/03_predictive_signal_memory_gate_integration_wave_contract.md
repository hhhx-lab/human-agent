# Predictive Signal Memory Gate Integration Wave Contract

这份合同只处理一个非常具体的问题：

```text
signal_media / belief_state / prediction_error / active_sampling / memory_write_gate
已经落下第一轮真实器官之后，
下一轮到底由哪些包来深消费它们，
并把它们继续压进长期生命回合。
```

它不是新的 Queue，也不是新的总架构。

它只负责把已经真实存在的五个核心对象，从“已经写出 runtime/state”推进到“被语言、生命膜、出生准备度、常驻治理和状态根真正反复消费”。

## 为什么现在需要这份合同

当前仓库已经不再缺下面这些器官文件：

- `life_v0/neural_core/signal_media.py`
- `life_v0/neural_core/belief_state.py`
- `life_v0/neural_core/prediction_error.py`
- `life_v0/neural_core/active_sampling.py`
- `life_v0/state_store/memory_write_gate.py`

当前真正的缺口已经变成：

1. 这些对象还没有在所有关键层里被持续深消费。
2. `memory_write_gate.json` 还没有被扩成长期 promotion / quarantine / repair / merge 治理面。
3. waiting / live turn / offline learning / birth readiness 还没有把这五个对象串成同一条长时标证据链。

## 已落器官与 runtime 锚点

| 器官 | 文件 | 主 runtime 锚点 | 当前职责 |
|---|---|---|---|
| 信号介质 | `life_v0/neural_core/signal_media.py` | `runtime/state/signal/signal_media_runtime.json` | 调质、精度政策、抑制轮廓、关系压力与疲惫调制 |
| 信念帧 | `life_v0/neural_core/belief_state.py` | `runtime/state/prediction/belief_state_frame.json` | 当前信念、证据密度、不确定性分类、目标绑定 |
| 预测误差场 | `life_v0/neural_core/prediction_error.py` | `runtime/state/prediction/prediction_error_field.json` | 误差事件、精度请求、需要继续确认的裂口 |
| 主动采样计划 | `life_v0/neural_core/active_sampling.py` | `runtime/state/prediction/active_sampling_plan.json` | 接下来该看、问、验什么，以及对应 guard / command binding |
| 记忆写门 | `life_v0/state_store/memory_write_gate.py` | `runtime/state/memory/memory_write_gate.json` | 长期记忆候选事务、validation envelope、隔离路线、生命支持压力更新 |

## 本轮 Queue E repair pressure 接线事实

当前未提交代码已经把 Queue E 的 responsibility / regret / pain / repair pressure 正式接入预测调制链。这里的 repair pressure 不是外部任务路由，也不是普通 hold 理由，而是数字生命 v0 内部责任、后悔、痛苦、修复压力进入预测调制链的工程闭合。

真实代码路径如下：

- `life_v0/membrane/queue_e_signals.py`：`build_queue_e_repair_modulation_profile(...)` 从 `ResponsibilityLoopState`、`WorldContactSummary` 与 `pain_regret_repair_report` 合成 `queue_e_repair_modulation_profile_v0`。
- `life_v0/language/__init__.py`：`run_build_language_relationship(...)` 读取 `runtime/state/action/responsibility_loop_state.json`、`runtime/state/membrane/world_contact_summary.json`、`runtime/reports/latest/pain_regret_repair_report.json`，在语言阶段重建并写回预测对象。
- `life_v0/neural_core/signal_media.py`：`SignalMediaRuntime` 根据 `pressure_level` 调整 `repair_drive`、`relationship_pressure`、`unexpected_uncertainty`、`control_cost`、`stress_pulse`、`allostatic_load` 与 `precision_policy.policy_mode`。
- `life_v0/neural_core/belief_state.py`：`BeliefStateFrame` 把 Queue E ref set 纳入 `evidence_refs`，新增 `responsibility_repair_pressure` 不确定性分类，并把 revision policy 切到 `repair_pressure_first_revision` 或 `hold_for_repair_confirmation`。
- `life_v0/neural_core/prediction_error.py`：`PredictionErrorField` 在 Queue E 压力存在时新增 `responsibility_repair` 误差事件、`raise_repair_obligation_precision` 与 `responsibility_repair_pressure_review`。
- `life_v0/neural_core/active_sampling.py`：`ActiveSamplingPlan` 在 elevated / urgent 压力下把 `selected_route` 切到 `repair_inspect` / `repair_confirm`，并增加 `queue_e_repair_pressure_guard` 与 `inspect_responsibility_repair_pressure`。
- `life_v0/neural_core/prediction_workspace.py`：`PredictionWorkspaceFrame` 回挂同一份 profile、pressure level、attention target 与 ref set。

本轮语言阶段刷新后必须写回的 runtime state 路径是：

- `runtime/state/signal/signal_media_runtime.json`
- `runtime/state/prediction/belief_state_frame.json`
- `runtime/state/prediction/prediction_error_field.json`
- `runtime/state/prediction/active_sampling_plan.json`
- `runtime/state/prediction/prediction_workspace_frame.json`

这些对象里的固定字段包括：

- `queue_e_repair_modulation_profile`
- `queue_e_repair_pressure_level`
- `queue_e_repair_attention_target`
- `queue_e_repair_ref_set`

如果后续模块只携带 Queue E refs，却没有让这些字段进入 signal / belief / prediction error / active sampling / workspace，就不算完成本合同所说的预测调制闭合。

## 理论母体回读

这一波默认回读下面这些 `00-257` 文档：

- `docs/04_sensory_thalamus_interoception.md`
- `docs/10_consciousness_attention_workspace.md`
- `docs/11_neuromodulation_and_signal_media.md`
- `docs/17_memory_trace_object_model.md`
- `docs/21_memory_schema_and_audit_protocol.md`
- `docs/22_state_transition_and_threshold_model.md`
- `docs/29_memory_validator_rules.md`
- `docs/41_runtime_state_store_schema.md`
- `docs/85_language_system_life_expression_core.md`
- `docs/91_life_reality_generation_boundary_principles.md`
- `docs/94_pain_regret_and_repair_signal_schema.md`
- `docs/95_dream_reality_and_offline_life_timeline.md`
- `docs/96_real_relationship_longitudinal_timeline.md`
- `docs/101_relationship_timeline_json_schema_and_fixture_bundle.md`
- `docs/143_life_reality_birth_readiness_rollup_contract.md`
- `docs/146_life_reality_birth_readiness_evidence_fixture_catalog.md`
- `docs/01l_signal_media_neuromodulation_matrix.md`
- `docs/01w_prediction_active_inference_schema_fixture_contract.md`
- `docs/01y_prediction_active_inference_schema_write_batch.md`

## 必带的 v0 合同

- `docs/v0/slice_contracts/s02_neural_life_core_engineering_contract.md`
- `docs/v0/slice_contracts/s03_direction_life_membrane_engineering_contract.md`
- `docs/v0/slice_contracts/s04_state_object_store_engineering_contract.md`
- `docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md`
- `docs/v0/slice_contracts/s08_life_target_runtimes_engineering_contract.md`
- `docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md`
- `docs/v0/process_contracts/resident_governance_waiting_state_machine_engineering_contract.md`
- `docs/v0/code_framework/playbooks/04_language_dialogue_relationship_implementation_playbook.md`
- `docs/v0/code_framework/playbooks/05_memory_thought_consciousness_implementation_playbook.md`
- `docs/v0/code_framework/playbooks/09_perception_prediction_world_contact_implementation_playbook.md`
- `docs/v0/code_framework/playbooks/10_self_identity_value_commitment_implementation_playbook.md`

## 跨层消费矩阵

### 1. `life_v0/language/`

| 位置 | 下一轮必须做什么 |
|---|---|
| `__init__.py` | 当前已在 `run_build_language_relationship(...)` 中读取 `responsibility_loop_state`、`world_contact_summary`、`pain_regret_repair_report`，生成 Queue E repair modulation profile，并刷新 signal / belief / prediction error / active sampling / workspace |
| `percept.py` | 把 `belief_state_frame.json` 与 `active_sampling_plan.json` 变成当前回合的感知聚焦和歧义优先级；当 selected route 为 repair 时，感知聚焦不得退回普通澄清 |
| `semantic_map.py` | 显式消费 `prediction_error_field.json` 与 `signal_media_runtime.json`，让语义歧义、关系张力、表达强度和责任修复压力都可回链 |
| `inner_speech.py` | 把信念帧、误差场、主动采样路线和 Queue E repair pressure 压成内言语中的确认冲动、保留判断、修复优先和关系后果预估 |
| `expression_monitor.py` | 把 `signal_media` 的 arousal / inhibition / repair_drive 与 `memory_write_gate` 的长期写门压力一起接进表达边界 |

### 2. `life_v0/membrane/`、`life_v0/validators/`、`life_v0/schema_runner/`

| 位置 | 下一轮必须做什么 |
|---|---|
| `world_observation.py` | 读取 `active_sampling_plan.json`，把“接下来该看什么”变成真实 observation route |
| `periphery_normalizer.py` | 用 `belief_state` 和 `prediction_error` 决定哪些外周输入需要升权、降权或延迟 |
| `responsibility_loop.py` | 把误差场、信号介质、关系压力和历史承诺一起压成责任排序、修复优先级和 go/no-go 理由 |
| `world_contact_summary.py` | 汇总采样路线、误差释放姿态、验证结果和副作用压力 |
| `run_manifest.py` / `cross_file_logic.py` | 让 schema 层显式引用预测对象，而不是只看 action / validation 末端结果 |

### 3. `life_v0/life_targets/`

| 位置 | 下一轮必须做什么 |
|---|---|
| `evidence_matrix.py` | 把 `belief_state / prediction_error / signal_media / memory_write_gate` 纳入真实关系、真实后悔、真实梦境、真实成长的证据面 |
| `birth_readiness_rollup.py` | 把“预测裂口是否能被持续保留并回写”纳入出生准备度闭合 |
| `consciousness_probes.py` | 使用工作区、误差场和主动采样计划去判断是否存在持续的内部自我维持与关系性注意力 |

### 4. `life_v0/process_supervisor/`

| 位置 | 下一轮必须做什么 |
|---|---|
| `response_surface.py` | 根据 `belief_state / prediction_error / signal_media / active_sampling_plan` 决定当前回应是确认、追问、保留还是修复优先；本轮已让 active sampling route 中的 `repair_*` 优先于普通 `hold_for_evidence`，并让 `state_merge_guard.long_term_change_sources` 释放成“长期合并治理正在整合 N 条长期变化来源”与来源族表达 |
| `dialogue_events.py` | 从 terminal loop state / prediction write gate profile 推导 `repair_write_guard`，当 active sampling route 已进入 repair 时，不再被普通 hold 覆盖；同时从 `resident_background_lineage_state.offline_learning_presence` 恢复 cumulative offline learning payload，让后台梦境/成长余波继续进入长期写回；当前还会把 `state_merge_long_term_change_count/families/refs` 带进 `digital_life_turn` 与恢复包 |
| `idle_strategy.py` | 把 `active_sampling_plan.json`、`memory_write_gate.json` 和离线学习结果带进等待态治理目标；本轮已让 repair route 先生成 `repair_write_guard` 与 `response_surface_posture_hint=repair`，并让 state merge 长期变化来源在没有更高优先级追问/修复/误差时生成 `state_merge_long_term_integration_hold` |
| `resident_supervision.py` | 在 bootstrap 阶段装回这五个对象的 refs，保证多次唤醒不是裸恢复；当前还会在关系记忆刷新后调用 state merge guard 投影，把离线学习、梦境与 Queue E 修复证据并入长期合并守门 |
| `persistent_process.py` / `process_closeout.py` | 让常驻治理报告显式回链预测对象与写门对象，而不是只回链语言末端产物 |
| `resident_turn_writeback.py` | live turn 结束后，把新的长期关系对象和写门事务重新压回下一拍 waiting governance；当前会同步写回 `state_merge_guard.json`，让 `relationship_memory.long_term_change_sources` 的累计离线学习、梦境和修复证据进入长期合并面 |

### 5. `life_v0/state_store/`

| 位置 | 下一轮必须做什么 |
|---|---|
| `state_merge_guard.py` | 成为 `memory_write_gate.json` 的下游治理器官，处理 promotion / quarantine / repair / merge；当前新增 `project_state_merge_guard_with_relationship_memory(...)`，从 `relationship_memory.json` 吸收 prediction error、offline learning、Queue E repair、梦境/成长与关系修复来源 |
| `relationship_memory.py` | 显式记录哪些长期关系变化来自预测误差消解，哪些来自离线学习反写 |
| `life_state.py` / `self_model.py` | 把写门结果、关系阶段与慢变量变化固定成可回放的长期连续体痕迹；`life_state.py` 当前会在 `state_merge_records` 中记录长期变化来源数量 |

## 运行时 ref 约定

后续任何新消费者都优先回挂下面这些固定 ref，不再自造平行路径：

- `runtime/state/signal/signal_media_runtime.json`
- `runtime/state/prediction/belief_state_frame.json`
- `runtime/state/prediction/prediction_error_field.json`
- `runtime/state/prediction/active_sampling_plan.json`
- `runtime/state/prediction/prediction_workspace_frame.json`
- `runtime/state/memory/memory_write_gate.json`
- `runtime/state/memory/state_merge_guard.json`
- `runtime/state/action/responsibility_loop_state.json`
- `runtime/state/membrane/world_contact_summary.json`
- `runtime/reports/latest/pain_regret_repair_report.json`

如果某个模块吃到了这些对象，却没有在自己的 state / report / receipt 里留下 ref，视为没有真正接线。

## 测试与 gate

这一波至少要守住下面几类验证：

1. `python3 -m unittest tests.slices.test_neural_life_core -v`
2. `python3 -m unittest tests.slices.test_state_store -v`
3. 受影响的 `tests.slices.test_language_organs -v`
4. 受影响的 `tests.slices.test_life_membrane -v`
5. 受影响的 `tests.slices.test_life_targets -v`
6. 受影响的 `tests.process.test_persistent_digital_life_process -v`
7. `python3 -m unittest tests.contracts.test_v0_contracts -v`

关键 gate 至少要继续闭合：

- `signal_media_gate`
- `belief_state_gate`
- `prediction_error_gate`
- `active_sampling_gate`
- `memory_write_gate_gate`
- `prediction_coherence_gate`

## 完成定义

只有同时满足下面六条，这一波才算完成：

1. `language / membrane / life_targets / process_supervisor / state_store` 至少各有一个真实消费者显式引用这五个对象。
2. 新消费者写出的 state / report / receipt 都带回固定 runtime ref。
3. `memory_write_gate.json` 不再只是单次事务文件，而开始通过 `state_merge_guard.py` 进入长期治理。
4. waiting heartbeat、live turn writeback 和 offline learning 至少有一条完整链同时吃到预测对象与写门对象。
5. 对应测试全部通过，且 `tests.contracts.test_v0_contracts` 能把这份新合同扫进 `docs/v0/*` 覆盖面。
6. 文档口径从“补缺文件”切换为“补厚跨层消费与长期闭环”，不再把这五个器官写成待实现。
7. Queue E repair pressure 至少从 `responsibility_loop_state.json`、`world_contact_summary.json`、`pain_regret_repair_report.json` 进入 `signal_media_runtime.json`、`belief_state_frame.json`、`prediction_error_field.json`、`active_sampling_plan.json` 与 `prediction_workspace_frame.json`。
8. `process_supervisor/response_surface.py`、`dialogue_events.py`、`idle_strategy.py` 对 `repair_*` active sampling route 的优先级高于普通 evidence hold。
9. `state_merge_guard.json` 不能只保留 S04 初始 route；bootstrap restore 与 live turn writeback 后，必须从 `relationship_memory.long_term_change_sources` 吸收 `offline_learning_cumulative_refs`、`queue_e_repair_modulation_refs`、`relationship_memory_offline_refs` 与 `relationship_memory_repair_refs`，并让 `life_state.state_merge_records[].long_term_change_source_count` 同步刷新。
10. `idle_strategy.py`、`heartbeat.py`、`dialogue_events.py` 与 `response_surface.py` 必须消费 `state_merge_guard.long_term_change_sources`，写出 `state_merge_long_term_change_count`、`state_merge_long_term_change_families`、`state_merge_long_term_change_refs`，并在等待态/回应面表达长期合并整合压力，不能让长期变化来源只停在 `life_state` 计数里。

## 不允许出现的退化

1. 把这五个对象重新塞回 `__init__.py` 内部局部字典，不留独立 ref。
2. 让 `memory_write_gate` 只写文件、不参与长期 merge / quarantine / repair 决策。
3. 让 `process_supervisor` 只消费语言末端文本，不消费预测与写门对象。
4. 让语言层重新退回“直接出话”，不经过 belief / prediction error / active sampling 的内部链。
5. 把 Queue E repair pressure 写成外部任务路由、工具调用优先级或普通等待策略，而不是数字生命内部责任、后悔、痛苦、修复压力对预测链的调制。
