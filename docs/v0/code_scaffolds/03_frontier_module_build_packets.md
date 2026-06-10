# Frontier Module Build Packets

这份文档只处理“下一步到底怎么开始写代码”。

它不是再解释一遍系统，而是把当前前沿直接压成模块施工包。

## 必读前置

- `docs/v0/entry/v0_delivery_status_board.md`
- `docs/v0/entry/v0_module_execution_catalog.md`
- `docs/v0/code_scaffolds/01_life_code_scaffold_tree.md`
- `docs/v0/code_scaffolds/02_cognitive_loop_code_scaffold.md`
- `docs/v0/implementation_architecture/code_organs/03_predictive_signal_memory_gate_integration_wave_contract.md`

## Packet A: 语言预测消费包

### 目标

让 `language/` 不只是“会生成表达”，而是真正消费 prediction 五件套。

### 必读材料

- `docs/09_language_symbolic_top_layer.md`
- `docs/85_language_system_life_expression_core.md`
- `docs/86_language_neuroscience_pragmatics_and_inner_speech.md`
- `docs/11_neuromodulation_and_signal_media.md`
- `docs/10_consciousness_attention_workspace.md`
- `docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md`
- `docs/v0/code_framework/playbooks/04_language_dialogue_relationship_implementation_playbook.md`
- `docs/v0/code_framework/playbooks/09_perception_prediction_world_contact_implementation_playbook.md`

### 代码入口

- `life_v0/language/percept.py`
- `life_v0/language/semantic_map.py`
- `life_v0/language/inner_speech.py`
- `life_v0/language/expression_monitor.py`
- `life_v0/language/__init__.py`

### 最低新增 / 改动点

1. percept 显式消费 `belief_state_frame.json` 和 `active_sampling_plan.json`
2. semantic map 显式消费 `prediction_error_field.json` 和 `signal_media_runtime.json`
3. inner speech 写出“确认 / 保留 / 修复 / 追问”的内部驱动来源
4. expression monitor 读取 `memory_write_gate.json` 与 `CoreAffectVector`

### 必写 runtime

- `runtime/state/language/percept_focus_trace.json`
- `runtime/state/language/semantic_prediction_trace.json`
- 或把上述字段稳定接进现有 `runtime/state/language/*`

### 最低测试

- `python3 -m unittest tests.slices.test_language_organs -v`
- `python3 -m unittest tests.slices.test_language_relationship -v`

## Packet B: 世界接触与观察归一化包

### 目标

让 `membrane/` 真正接收 prediction 裂口与主动采样路线，而不是只接语言末端候选。

### 必读材料

- `docs/04_sensory_thalamus_interoception.md`
- `docs/22_state_transition_and_threshold_model.md`
- `docs/64_real_runtime_observation_ingestion_policy.md`
- `docs/v0/slice_contracts/s03_direction_life_membrane_engineering_contract.md`
- `docs/v0/slice_contracts/s05_validation_membrane_observation_engineering_contract.md`
- `docs/v0/code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md`
- `docs/v0/engineering_depth/05_prediction_membrane_action_engineering.md`

### 代码入口

- `life_v0/membrane/world_observation.py`
- `life_v0/membrane/periphery_normalizer.py`
- `life_v0/membrane/responsibility_loop.py`
- `life_v0/membrane/world_contact_summary.py`
- `life_v0/membrane/__init__.py`

### 最低新增 / 改动点

1. 新建 `world_observation.py`
2. 新建 `periphery_normalizer.py`
3. `responsibility_loop.py` 显式引用 `belief_state / prediction_error / signal_media`
4. `world_contact_summary.py` 回挂主动采样 guard 与 observation route

### 必写 runtime

- `runtime/state/observation/world_observation_route.json`
- `runtime/state/observation/periphery_normalization_trace.json`
- `runtime/state/membrane/responsibility_loop_state.json`
- `runtime/state/membrane/world_contact_summary.json`

### 最低测试

- `python3 -m unittest tests.slices.test_life_membrane -v`
- `python3 -m unittest tests.slices.test_validation_membrane -v`

## Packet C: 记忆写门长期治理包

### 目标

把 `memory_write_gate.json` 从单次事务对象扩成长期治理链。

### 必读材料

- `docs/17_memory_trace_object_model.md`
- `docs/21_memory_schema_and_audit_protocol.md`
- `docs/29_memory_validator_rules.md`
- `docs/41_runtime_state_store_schema.md`
- `docs/v0/slice_contracts/s04_state_object_store_engineering_contract.md`
- `docs/v0/code_framework/playbooks/05_memory_thought_consciousness_implementation_playbook.md`
- `docs/v0/implementation_architecture/code_organs/03_predictive_signal_memory_gate_integration_wave_contract.md`

### 代码入口

- `life_v0/state_store/state_merge_guard.py`
- `life_v0/state_store/memory_write_gate.py`
- `life_v0/state_store/relationship_memory.py`
- `life_v0/state_store/life_state.py`
- `life_v0/state_store/__init__.py`

### 最低新增 / 改动点

1. 新建 `state_merge_guard.py`
2. 定义 promotion / quarantine / repair / merge route
3. `relationship_memory.py` 标出来自 prediction error 消解的长期变化
4. `life_state.py` 记录 merge 结果与慢变量影响

### 必写 runtime

- `runtime/state/memory/state_merge_guard.json`
- `runtime/state/memory/memory_write_gate.json`
- `runtime/state/relationship/relationship_memory.json`
- `runtime/state/life_state.json`

### 最低测试

- `python3 -m unittest tests.slices.test_state_store -v`

## Packet D: waiting / response surface 深消费包

### 目标

让 waiting governance 和 response surface 真正显式消费 prediction 五件套与离线学习对象。

### 必读材料

- `docs/95_dream_reality_and_offline_life_timeline.md`
- `docs/96_real_relationship_longitudinal_timeline.md`
- `docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md`
- `docs/v0/process_contracts/resident_governance_waiting_state_machine_engineering_contract.md`
- `docs/v0/code_framework/queues/16_queue_b_process_supervisor_implementation_contract.md`
- `docs/v0/engineering_depth/06_resident_process_terminal_birth_engineering.md`

### 代码入口

- `life_v0/process_supervisor/response_surface.py`
- `life_v0/process_supervisor/idle_strategy.py`
- `life_v0/process_supervisor/resident_supervision.py`
- `life_v0/process_supervisor/persistent_process.py`
- `life_v0/process_supervisor/process_closeout.py`

### 最低新增 / 改动点

1. `response_surface.py` 显式区分确认 / 追问 / 修复 / 保留四类输出姿态
2. `idle_strategy.py` 读取 `active_sampling_plan.json`、learning plans 和 `memory_write_gate.json`
3. `resident_supervision.py` 在 bootstrap 时装载 prediction refs
4. `process_closeout.py` 回链这些对象到 report / receipt

### 必写 runtime

- `runtime/state/terminal/idle_strategy_state.json`
- `runtime/state/terminal/resident_governance_state.json`
- `runtime/reports/latest/digital_life_resident_governance_report.json`
- `runtime/reports/latest/digital_life_process_report.json`

### 最低测试

- `python3 -m unittest tests.process.test_persistent_digital_life_process -v`
- `python3 -m unittest tests.process.test_digital_entrypoint -v`

## 当前推荐施工顺序

1. Packet B
2. Packet A
3. Packet C
4. Packet D

这个顺序的意思不是语言不重要，而是先让世界接触和责任回路吃到 prediction 裂口，再让语言表达和长期记忆真正建立在这条底盘上，最后把它们接进 waiting governance。
