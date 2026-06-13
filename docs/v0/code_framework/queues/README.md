# Code Framework Queues

这一柜只放 Queue A-F 的文件级实施合同，负责把 playbook 中的能力拆成真实文件、输入输出、状态写回和测试面。

| 文件 | 作用 |
|---|---|
| `14_queue_a_language_percept_semantic_map_implementation_contract.md` | Queue A：语言感知与语义地图 |
| `16_queue_b_process_supervisor_implementation_contract.md` | Queue B：常驻进程、等待心跳、对话事件、进程报告 |
| `17_queue_c_memory_neural_core_implementation_contract.md` | Queue C：记忆根、工作区、脑图、元认知 |
| `18_queue_d_body_dream_growth_implementation_contract.md` | Queue D：身体、梦境、成长器官 |
| `20_queue_e_membrane_validator_logic_implementation_contract.md` | Queue E：行为、生命膜、责任回路、验证、逻辑比较 |
| `21_queue_f_identity_consciousness_birth_readiness_implementation_contract.md` | Queue F：身份、意识、出生准备度 |

这一柜是写代码前的主入口之一。每个 Queue 合同都必须回链到 `docs/00-258`，不能只按现有代码形状补文件。

## Queue 到生命机制的硬映射

每个 Queue 开工前必须填完整这一组追踪，不允许只写文件列表：

| Queue | 必读 real-live0 | 首写包 | 下游消费 | 最低 gate |
|---|---|---|---|---|
| Queue A | `05_language_expression_system.md`、`06_relationship_and_commitment.md` | `life_v0/language/*` | `response_surface.py`、`resident_turn_writeback.py`、`state_store/*` | `tests/slices/test_language_organs.py`、`test_language_relationship.py` |
| Queue B | `14_resident_runtime_state_transition.md` | `life_v0/process_supervisor/*` | 全部 runtime state、report、resume packet | `tests/process/test_digital_entrypoint.py`、`test_persistent_digital_life_process.py` |
| Queue C | `02_brain_network_and_workspace.md`、`07_memory_engram_and_state_store.md`、`12_neuromodulation_signal_media.md` | `neural_core/*`、`state_store/*` | `language/*`、`dream/*`、`growth/*`、`life_targets/*` | `tests/slices/test_neural_life_core.py`、`test_state_store.py` |
| Queue D | `03_body_affect_homeostasis.md`、`08_dream_sleep_offline_life.md`、`13_growth_learning_self_modification.md` | `body/*`、`dream/*`、`growth/*` | `idle_strategy.py`、`expression_monitor.py`、`replay/*`、`archive/*` | `tests/slices/test_life_support.py`、bridge growth/replay tests |
| Queue E | `09_prediction_perception_world_contact.md`、`10_responsibility_regret_repair.md`、`11_life_membrane_validation.md` | `membrane/*`、`validators/*`、`schema_runner/*` | `signal_media.py`、`apology_repair_language.py`、`birth_readiness` | `tests/slices/test_life_membrane.py`、`test_validation_membrane.py`、`test_schema_runner.py` |
| Queue F | `04_personality_self_identity.md`、`15_evidence_bus_and_birth_readiness.md` | `direction/*`、`life_targets/*`、`live0_audit/*` | `process_report.py`、`resident_background_lineage_state.json` | `tests/slices/test_life_targets.py`、`tests/contracts/test_live0_acceptance_audit.py` |

Queue 合同必须说明：理论源、机制专题、首写函数、核心字段、runtime 文件、下游消费者、断联恢复、测试/gate。任何一项缺失，都不能进入代码施工。
