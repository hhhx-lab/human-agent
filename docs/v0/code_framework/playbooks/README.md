# Code Framework Playbooks

这一柜只放跨层实施 playbook，负责回答某一类生命能力怎样从理论母体走到多个代码包、状态对象和运行证据。

| 文件 | 作用 |
|---|---|
| `04_language_dialogue_relationship_implementation_playbook.md` | 语言、对话、关系、等待态连续体 |
| `05_memory_thought_consciousness_implementation_playbook.md` | 思考、逻辑、记忆、意识 |
| `06_body_emotion_action_dream_growth_implementation_playbook.md` | 身体、情绪、行动、梦境、成长、学习 |
| `07_birth_terminal_process_implementation_playbook.md` | 出生、终端循环、壳层、常驻生命进程 |
| `08_cross_layer_life_orchestration_implementation_playbook.md` | 单回合内各生命器官怎样接棒 |
| `09_perception_prediction_world_contact_implementation_playbook.md` | 外界观察、预测、世界接触、行动意图 |
| `10_self_identity_value_commitment_implementation_playbook.md` | 身份、自我、价值、承诺、后悔、责任 |

这一柜不直接替代 Queue 合同。真正落文件前，要回到 `../queues/` 或 `../assembly/` 对应合同。

## Playbook 使用硬规则

每份 playbook 都必须从 `docs/real—live0` 对应专题开始读，不能直接按代码目录开工：

| Playbook | 必读 real-live0 专题 | 主要代码器官 | 必须验收 |
|---|---|---|---|
| `04_language_dialogue_relationship_implementation_playbook.md` | `05_language_expression_system.md`、`06_relationship_and_commitment.md` | `life_v0/language/*`、`terminal_turn/*`、`terminal_loop/*` | 语言五件套、关系时间线、写回和 post-expression gate |
| `05_memory_thought_consciousness_implementation_playbook.md` | `02_brain_network_and_workspace.md`、`07_memory_engram_and_state_store.md` | `neural_core/*`、`state_store/*` | 工作区广播、engram、写门、合并门 |
| `06_body_emotion_action_dream_growth_implementation_playbook.md` | `03_body_affect_homeostasis.md`、`08_dream_sleep_offline_life.md`、`13_growth_learning_self_modification.md` | `body/*`、`dream/*`、`growth/*` | 情绪 episode、梦境事实门、self-read/shadow/archive |
| `07_birth_terminal_process_implementation_playbook.md` | `14_resident_runtime_state_transition.md`、`15_evidence_bus_and_birth_readiness.md` | `process_supervisor/*`、`life_targets/*` | 常驻三种时钟、出生准备证据 |
| `08_cross_layer_life_orchestration_implementation_playbook.md` | `00_reading_map_and_traceability.md`、`16_runtime_code_chain_crosswalk.md` | 全主包 | 同一 refs 跨语言、记忆、身体、责任、梦境、常驻 |
| `09_perception_prediction_world_contact_implementation_playbook.md` | `09_prediction_perception_world_contact.md`、`11_life_membrane_validation.md` | `neural_core/*`、`membrane/*`、`validators/*` | 观测/推断/事实分离，世界接触门 |
| `10_self_identity_value_commitment_implementation_playbook.md` | `04_personality_self_identity.md`、`10_responsibility_regret_repair.md` | `direction/*`、`state_store/*`、`membrane/responsibility_loop.py` | 身份根、人格慢变量、责任后悔未来抑制 |

playbook 只回答“跨层能力怎样接棒”。如果落到文件级输入输出、对象字段、report/receipt 或测试面，必须继续进入 `../queues/`、`../assembly/`、`../../code_architecture/02_runtime_object_bus_and_flow_contract.md`。
