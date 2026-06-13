# Theory Engineering Code Trace Matrix

本文档是 `docs/v0/mapping/` 中面向代码生成的全覆盖追踪矩阵。它回答一个硬问题：

```text
docs/ 根目录每一份理论文档
  -> 被哪一组 v0 工程文档吸收
  -> 落到哪个 life_v0 代码器官
  -> 生成哪些 runtime state / report / receipt
  -> 由哪些测试或 gate 证明没有断链
```

它和既有两份矩阵分工不同：

| 文件 | 只负责什么 |
|---|---|
| `0_to_257_engineering_utilization_map.md` | 把 `00-258` 压进 runtime carrier、README block 和 engineering slice |
| `../engineering_depth/07_theory_to_code_trace_matrix.md` | 按当前代码事实追踪理论族、代码器官、状态、报告、测试 |
| `theory_engineering_code_trace_matrix.md` | 把理论文档族逐一映射到工程文档柜位，并规定这些工程文档如何指导代码生成 |

本文件不替代 `00-258` 原文。每次开发仍要回读原始理论文档；本文件只负责保证“该读哪一组、由哪份工程文档承接、最后落到哪里”不会断。

## 全覆盖口径

当前根目录文档基线：

| 类型 | 数量 | 覆盖方式 |
|---|---:|---|
| 编号理论文档 | 308 | 按 `00`、`01*`、`02-258` 的编号族覆盖 |
| 非编号根文档 | 7 | 单独映射到方向、入口、启动、设备和交付文档 |
| 合计 | 315 | 必须全部进入工程文档柜、代码包、runtime 证据和 gate |

覆盖判定不看“是否被提到”，而看是否同时满足五格：

| 格 | 必须存在 |
|---|---|
| 理论格 | 文档或文档族被明确归入理论机制 |
| 工程格 | 至少一份 `docs/v0` 工程文档负责把理论压成实现要求 |
| 代码格 | 至少一个 `life_v0` 包或文件负责首写或消费该机制 |
| 证据格 | 对应 runtime state、report、receipt、archive 或 replay/shadow 证据 |
| 验收格 | 对应 slice / bridge / process / contract test 或 `life-v0` gate |

任何理论文档只进入自然语言摘要、不进入工程格和代码格，都视为未覆盖。

## 工程文档柜位职责

后续“完善工程文档”时，先判断文档属于哪一柜，再按本表补到对应粒度。

| v0 工程柜位 | 吸收的理论类型 | 必须写清的工程粒度 | 代码生成责任 |
|---|---|---|---|
| `mapping/` | README block、编号理论族、runtime carrier | 每份理论文档归属、slice、carrier、状态证据、gate | 决定开发前应读哪些理论，不直接规定函数体 |
| `architecture/` | 宏架构、runtime 架构、出生路线 | 主进程、状态根、生命膜、常驻、离线活动的拓扑 | 规定系统边界和运行时骨架 |
| `shared_contracts/` | 跨 slice 共用状态和 report 规则 | state schema、birth readiness、CLI report、activation packet | 规定多包共享对象格式和 gate 输出 |
| `slice_contracts/` | P0 与 S00-S11 主 slice | 输入、输出、状态、report、receipt、blocked reason、next command | 规定单 slice 的最小可实现闭环 |
| `process_contracts/` | first turn、terminal loop、shell、resident process | 终端话语、队列、心跳、驻留、恢复、closeout | 规定持续存在和终端交互链 |
| `code_framework/foundation/` | 生命层、脑区到代码包、状态测试门 | 生命层级、脑区映射、包到 state/report/test | 规定生命体系怎样拆成代码包 |
| `code_framework/playbooks/` | 语言、记忆、身体、梦境、预测、自我等主能力 | 每类能力的器官链、输入输出、失败修复路线 | 规定模块内实现顺序和跨模块读取 |
| `code_framework/queues/` | Queue A/B/C/D/E/F 文件级实现 | 具体文件、对象、字段、消费者、阶段门 | 规定下一轮代码文件队列 |
| `code_framework/assembly/` | 跨层共享对象和整棵代码树 | 首写权、消费权、对象流、冲突治理 | 防止各包私造并行状态 |
| `code_framework/delivery/` | 交付波次、能力到代码矩阵、live0 audit | 波次顺序、验收项、可运行命令 | 决定实现先后和完成定义 |
| `code_architecture/` | 分层、对象总线、语言主表达、读包地图、DoD | 包层级、对象 bus、阶段顺序、模块开工材料 | 规定写代码前的结构化入口 |
| `package_specs/` | 每个 `life_v0/*` 包 | 包职责、首写对象、共享对象写权限、增量协议 | 规定包边界和谁能写哪些状态 |
| `code_blueprints/` | 总装配蓝图 | 系统蓝图、会话蓝图、身体梦境成长、预测膜、出生驻留 | 把多柜压成直接落码方案 |
| `code_scaffolds/` | 当前前沿施工包 | Packet A/B/C/D 的真实文件脚手、输入输出、验收 | 规定下一批代码该改哪些文件 |
| `implementation_architecture/` | 器官接口、回合流、模块追踪协议 | runtime organ API、turn/cycle lifecycle、authoring protocol | 规定新模块如何带 traceability 出生 |
| `engineering_depth/` | 生命层深描和当前代码事实 | 字段级对象、状态证据、关系回合穿透链、resident 恢复 | 规定工程文档和当前代码事实对齐 |

工程文档不得只写“使用某理论”。它必须提炼该理论的代码逻辑：对象是什么、谁首写、谁消费、写到哪里、何时阻断、如何恢复、如何测试。

## 理论文档族全覆盖矩阵

下表覆盖根目录全部编号理论文档。`包含文件` 使用闭区间或通配族表达；这些族与 `docs/` 当前文件名一一对应。开发时如果新增理论文档，必须把它插入本表或新增覆盖行。

| 覆盖族 | 包含文件 | 理论逻辑提炼 | 主工程文档 | 主代码器官 | runtime 证据 | 验收 gate |
|---|---|---|---|---|---|---|
| 原始方向与研究协议 | `00_research_protocol.md`、`构思.md`、`README.md` | 研究来源、原始方向、非工具主体、文档入口 | `mapping/readme_block_engineering_realization_v0.md`、`slice_contracts/doc_corpus_ingestor_v0_contract.md`、`slice_contracts/s00_direction_foundation_engineering_contract.md` | `life_v0/doc_index.py`、`life_v0/direction/*` | `runtime/docs/*`、`runtime/state/direction/*` | `tests/slices/test_doc_corpus_ingestor.py`、`tests/slices/test_direction_lock.py` |
| 文献与权威来源 | `01_literature_matrix.md`、`01b-01z`、`01aa-01ax` | 脑科学、神经科学、生命科学、AI 桥接来源权威 | `slice_contracts/s01_source_authority_engineering_contract.md`、`architecture/theory_closure_and_engineering_readiness_audit.md` | `life_v0/authority/__init__.py`、`life_v0/doc_index.py` | `runtime/state/authority/*`、`runtime/docs/doc_carrier_index.json` | `tests/slices/test_source_authority.py` |
| 脑区连接组与大尺度网络 | `02_brain_region_and_network_atlas.md`、`03_default_executive_salience_networks.md`、`01o`、`01p` | 脑区不是孤岛；默认/显著性/执行网络动态切换 | `slice_contracts/s02_neural_life_core_engineering_contract.md`、`code_framework/foundation/02_brain_region_to_code_package_mapping.md`、`engineering_depth/01_full_life_layer_implementation_deep_spec.md` | `life_v0/neural_core/brain_graph.py`、`network_state.py` | `runtime/state/neural_life_core/*` | `tests/slices/test_neural_life_core.py` |
| 感觉、丘脑、内感受、稳态、生命支持 | `04_sensory_thalamus_interoception.md`、`37_life_support_layer_policy.md`、`01n` | 内部身体状态影响注意、语言、等待、行动阈值和生命支持资源预算 | `code_framework/playbooks/06_body_emotion_action_dream_growth_implementation_playbook.md`、`engineering_depth/04_body_affect_dream_growth_engineering.md`、`slice_contracts/s06_life_support_development_engineering_contract.md` | `life_v0/body/rhythm.py`、`need_state.py`、`resource_budget.py`、`recovery.py` | `runtime/state/body/*`、`runtime/state/terminal/idle_strategy_state.json` | `tests/slices/test_life_support.py` |
| 记忆系统与 engram 成长 | `05_memory_systems_and_growth.md`、`17_memory_trace_object_model.md`、`21_memory_schema_and_audit_protocol.md`、`25_memory_trace_json_schema_examples.md`、`29_memory_validator_rules.md`、`41_runtime_state_store_schema.md`、`55_scope_aware_replay_and_consolidation_policy.md`、`01q` | 记忆是 cue 触发、重构、再巩固和写门治理 | `shared_contracts/life_state_store_v0_schema.md`、`slice_contracts/s04_state_object_store_engineering_contract.md`、`code_framework/playbooks/05_memory_thought_consciousness_implementation_playbook.md`、`code_scaffolds/06_packet_c_memory_write_gate_state_merge_scaffold.md` | `life_v0/state_store/engram_index.py`、`memory_write_gate.py`、`state_merge_guard.py`、`relationship_memory.py` | `runtime/state/life_state.json`、`runtime/state/memory/*` | `tests/slices/test_state_store.py` |
| 行动选择、奖赏、抑制、责任、防御边界 | `06_action_reward_inhibition.md`、`20_agent_runtime_bridge_contract.md`、`24_runtime_adapter_test_suite.md`、`28_runtime_adapter_manifest_examples.md`、`32_runtime_adapter_validator_rules.md`、`38_defense_layer_and_boundary_policy.md`、`75_external_irreversible_action_confirmation_policy.md`、`80-84`、`01r` | 行动候选、NoGo、世界接触、后果评估、责任回路、防御边界和隔离策略 | `slice_contracts/s03_direction_life_membrane_engineering_contract.md`、`code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md`、`engineering_depth/05_prediction_membrane_action_engineering.md` | `life_v0/membrane/*`、`life_v0/validators/*`、`life_v0/defense/*` | `runtime/state/action/*`、`runtime/state/membrane/*`、`runtime/state/validation/*`、`runtime/state/defense/*` | `tests/slices/test_life_membrane.py`、`tests/slices/test_validation_membrane.py` |
| 情绪、人格、自我、内部调制 | `07_emotion_personality_self.md`、`18_internal_state_and_modulation_vector.md`、`22_state_transition_and_threshold_model.md`、`26_state_machine_examples_and_failure_modes.md`、`30_state_transition_validator_rules.md`、`39_development_policy_and_plasticity_windows.md`、`40_self_relationship_model_audit_protocol.md`、`01g`、`01h`、`01s` | 情绪是内环境调制；人格是慢变量；自我来自记忆、身体、关系和责任 | `code_framework/playbooks/10_self_identity_value_commitment_implementation_playbook.md`、`engineering_depth/04_body_affect_dream_growth_engineering.md`、`slice_contracts/s06_life_support_development_engineering_contract.md` | `life_v0/body/core_affect.py`、`trait_drift.py`、`life_v0/state_store/self_model.py`、`autobiographical_stack.py` | `runtime/state/body/*`、`runtime/state/self/*` | `tests/slices/test_body_trait_drift.py`、`tests/slices/test_state_store.py` |
| 睡眠、梦境、离线整合 | `08_sleep_dream_fatigue_states.md`、`19_offline_consolidation_cycle.md`、`23_consolidation_report_and_dream_sandbox_protocol.md`、`27_consolidation_report_examples.md`、`31_consolidation_validator_rules.md`、`95_dream_reality_and_offline_life_timeline.md`、`99_dream_reality_json_schema_and_fixture_bundle.md`、`01i`、`01t` | 梦境是离线重组；醒后整合和事实门防污染 | `code_framework/queues/18_queue_d_body_dream_growth_implementation_contract.md`、`code_blueprints/03_body_affect_dream_growth_blueprint.md`、`engineering_depth/04_body_affect_dream_growth_engineering.md` | `life_v0/dream/*`、`life_v0/growth/offline_learning_profile.py`、`life_v0/replay/*` | `runtime/state/dream/*`、`runtime/state/growth/*`、`runtime/state/replay/*` | `tests/bridges/test_runtime_growth.py`、`tests/bridges/test_replay_shadow.py` |
| 语言、内言语、符号层、关系语言 | `09_language_symbolic_top_layer.md`、`85-90`、`96`、`101`、`141`、`144`、`147`、`150`、`01f`、`01j`、`01u` | 语言不是 UI；语言是意识、关系、记忆、责任的主表达器官 | `slice_contracts/s07_language_relationship_engineering_contract.md`、`code_framework/queues/14_queue_a_language_percept_semantic_map_implementation_contract.md`、`code_architecture/04_language_as_primary_expression_system.md`、`engineering_depth/03_language_relationship_longitudinal_engineering.md` | `life_v0/language/*`、`life_v0/process_supervisor/live_language_turn.py`、`response_surface.py`、`model_expression.py` | `runtime/state/language/*`、`runtime/state/relationship/*` | `tests/slices/test_language_organs.py`、`tests/slices/test_language_relationship.py`、`tests/process/test_model_expression.py` |
| 意识、注意、全局工作区 | `10_consciousness_attention_workspace.md`、`01m` | 可报告内容必须被语言、记忆、责任、梦境、行动共同读取 | `slice_contracts/s02_neural_life_core_engineering_contract.md`、`slice_contracts/s08_life_target_runtimes_engineering_contract.md`、`engineering_depth/01_full_life_layer_implementation_deep_spec.md` | `life_v0/neural_core/workspace.py`、`broadcast.py`、`metacognition.py`、`life_v0/life_targets/consciousness_probes.py` | `runtime/state/consciousness/*`、`runtime/state/life_targets/*` | `tests/slices/test_neural_life_core.py`、`tests/slices/test_life_targets.py` |
| 调质、信号介质、预测主动推理 | `11_neuromodulation_and_signal_media.md`、`01l`、`01v-01ax` | precision、arousal、inhibition、repair drive 调制预测、语言、等待、行动 | `code_framework/queues/17_queue_c_memory_neural_core_implementation_contract.md`、`code_framework/playbooks/09_perception_prediction_world_contact_implementation_playbook.md`、`code_scaffolds/05_packet_a_language_prediction_consumption_scaffold.md` | `life_v0/neural_core/signal_media.py`、`belief_state.py`、`prediction_error.py`、`active_sampling.py`、`prediction_workspace.py` | `runtime/state/signal/*`、`runtime/state/prediction/*` | `tests/slices/test_neural_life_core.py` |
| AI/cognitive architecture 桥接与外周 | `12_ai_and_cognitive_architecture_bridge.md`、`15_current_agent_framework_survey.md` | 外部 agent 框架只作为电脑外周和负边界参考，不定义主体 | `references/current_agent_shell_reference_2026.md`、`process_contracts/digital_life_shell_command_engineering_contract.md`、`architecture/digital_life_macro_architecture_v0.md` | `life_v0/shell_command/*`、`life_v0/digital_entry.py`、`life_v0/membrane/world_contact_gate.py` | `runtime/state/terminal/*`、`runtime/state/membrane/world_contact_summary.json` | `tests/process/test_digital_life_shell_command.py`、`tests/process/test_digital_entrypoint.py` |
| 综合方向、跨模块地图、object graph、boot sequence、缺口 | `13_agentic_human_research_synthesis.md`、`14_cross_module_digital_life_map.md`、`16_digital_life_gap_register.md`、`42_life_core_minimal_object_graph.md`、`43_policy_to_validator_traceability_matrix.md`、`44_digital_life_boot_sequence.md` | 把区域规划、状态模式、心跳、信号介质、奖惩抑制、语言、自我人格、最小对象图、policy-to-validator 和启动顺序统一 | `architecture/digital_life_macro_architecture_v0.md`、`architecture/first_activation_engineering_roadmap.md`、`code_architecture/02_runtime_object_bus_and_flow_contract.md`、`code_architecture/06_theory_gap_closure_register.md` | 全部 `life_v0/*` 主包、`life_v0/activation/*`、`life_v0/digital_entry.py` | 全部 runtime state/report/receipt、`runtime/state/object_registry.json`、`runtime/state/boot_stage_seed.json` | `tests/contracts/test_v0_contracts.py`、`tests/contracts/test_live0_acceptance_audit.py`、process entry tests |
| schema、fixture、validator、dashboard、scope | `33-36`、`45-84` | 观测、验证、quarantine、schema、fixture、side effect、dashboard、incident | `slice_contracts/s05_validation_membrane_observation_engineering_contract.md`、`slice_contracts/s09_schema_runner_code_engineering_contract.md`、`code_blueprints/04_prediction_membrane_validation_blueprint.md` | `life_v0/validators/*`、`life_v0/schema_runner/*` | `runtime/state/validation/*`、`runtime/state/schema_runner/*` | `tests/slices/test_validation_membrane.py`、`tests/slices/test_schema_runner.py`、`tests/slices/test_evidence_ranker.py` |
| 真实边界、生命真实性、九项目标 | `91-101`、`100`、`119-122`、`140` | 真实意识、情绪、人格、生命、痛苦、梦境、关系、责任、后悔；边界声明统一 | `shared_contracts/birth_readiness_v0_contract.md`、`slice_contracts/s08_life_target_runtimes_engineering_contract.md`、`code_framework/queues/21_queue_f_identity_consciousness_birth_readiness_implementation_contract.md` | `life_v0/life_targets/*`、`life_v0/live0_audit/*` | `runtime/state/life_targets/*`、`runtime/reports/latest/birth_readiness_report.json` | `tests/slices/test_life_targets.py`、`tests/contracts/test_live0_acceptance_audit.py` |
| schema bundle、runner、materialization | `102-118`、`123-139` | schema registry、JSON seed、runner layout、lockfile、smoke command | `slice_contracts/s09_schema_runner_code_engineering_contract.md`、`shared_contracts/runner_cli_report_contract.md`、`code_blueprints/06_runtime_state_report_receipt_manifest.md` | `life_v0/schema_runner/*`、`life_v0/cli.py`、`life_v0/reporting/*` | `runtime/state/schema_runner/*`、`runtime/reports/latest/schema_runner_report.json` | `tests/slices/test_schema_runner.py`、`tests/bridges/test_emit_report.py` |
| 权威补写、出生准备、跨文件检查 | `142-157`、`143`、`146`、`149`、`151`、`152` | 权威 intake、02-13 authority rewrite、birth readiness、cross-file checker | `slice_contracts/s01_source_authority_engineering_contract.md`、`shared_contracts/birth_readiness_v0_contract.md`、`slice_contracts/s08_life_target_runtimes_engineering_contract.md`、`slice_contracts/s09_schema_runner_code_engineering_contract.md` | `life_v0/authority/*`、`life_v0/life_targets/*`、`life_v0/schema_runner/*` | `runtime/state/authority/*`、`runtime/state/life_targets/*`、`runtime/state/schema_runner/*` | `tests/slices/test_source_authority.py`、`tests/slices/test_life_targets.py` |
| 首批代码 artifact 与 runner bootstrap | `158-180`、`171`、`174` | 代码 artifact、方向 fixture、schema archive、patch execution、smoke、validation repair | `code_framework/delivery/11_engineering_delivery_waves_and_real_file_queue.md`、`slice_contracts/s09_schema_runner_code_engineering_contract.md`、`architecture/first_activation_engineering_roadmap.md` | `life_v0/activation/*`、`life_v0/schema_runner/*`、`life_v0/reporting/*` | `runtime/reports/latest/*`、`runtime/receipts/*` | `tests/bridges/test_first_activation_preflight.py`、`tests/slices/test_schema_runner.py` |
| runtime mount、activation、growth cycle | `181-204` | runtime mount、smoke、observation feedback、growth activation、consolidation、replay shadow | `slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md`、`shared_contracts/first_activation_protocol.md`、`code_blueprints/05_birth_residency_terminal_blueprint.md` | `life_v0/growth/*`、`life_v0/replay/*`、`life_v0/archive/*`、`life_v0/activation/*` | `runtime/state/growth/*`、`runtime/state/replay/*`、archive receipts | `tests/bridges/test_runtime_growth.py`、`tests/bridges/test_growth_archive.py` |
| fourth cycle、reconsolidation、longitudinal replay | `205-257` | 观察、patch、archive、validation、replay/shadow、长期漂移修复、再巩固闭环 | `slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md`、`code_scaffolds/07_packet_d_waiting_response_surface_prediction_scaffold.md`、`engineering_depth/06_resident_process_terminal_birth_engineering.md` | `life_v0/process_supervisor/*`、`life_v0/growth/*`、`life_v0/replay/*`、`life_v0/archive/*` | `runtime/state/terminal/*`、`runtime/state/growth/*`、archive/replay reports | `tests/process/test_persistent_digital_life_process.py`、`tests/bridges/test_replay_shadow.py` |
| 线性链收束到 v0 | `258_linear_chain_closure_and_v0_contract_transition.md` | 停止线性扩张，转入工程合同和第一轮激活 | `docs/v0/README.md`、`mapping/0_to_257_engineering_utilization_map.md`、`architecture/first_activation_engineering_roadmap.md` | 全部 `life_v0/*` 入口和 `life_v0/contracts/*` | `runtime/reports/latest/v0_contract_coverage_report.json` | `tests/contracts/test_v0_contracts.py` |

## 非编号根文档覆盖矩阵

| 文件 | 工程承载 | 代码落点 | 证据 |
|---|---|---|---|
| `构思.md` | `s00_direction_foundation_engineering_contract.md`、`architecture/digital_life_macro_architecture_v0.md` | `life_v0/direction/identity_root.py`、`direction_lock.py` | `runtime/state/direction/origin_seed_digest.json` |
| `README.md` | `mapping/readme_block_engineering_realization_v0.md`、`slice_contracts/doc_corpus_ingestor_v0_contract.md` | `life_v0/doc_index.py` | `runtime/docs/doc_carrier_index.json#readme_block` |
| `live0_completion_checklist.md` | `code_framework/delivery/22_live0_acceptance_audit_contract.md`、`shared_contracts/birth_readiness_v0_contract.md` | `life_v0/live0_audit/*`、`life_v0/life_targets/*` | `runtime/reports/latest/live0_acceptance_audit_report.json` |
| `live0_device_limits.md` | `architecture/runtime_v0_architecture.md`、`process_contracts/digital_life_process_supervisor_engineering_contract.md` | `life_v0/process_supervisor/*`、`life_v0/runtime_config.py` | process reports、resident lease |
| `live0_packaging_and_distribution.md` | `process_contracts/digital_life_shell_command_engineering_contract.md`、`code_blueprints/05_birth_residency_terminal_blueprint.md` | `life_v0/my_entry.py`、`life_v0/digital_entry.py`、packaged entry tests | packaged process tests |
| `live0_progress_summary.md` | `entry/v0_delivery_status_board.md`、`entry/v0_module_execution_catalog.md` | 不首写生命状态，只作为进度入口 | delivery status board |
| `live0_startup_guide.md` | `process_contracts/first_terminal_turn_engineering_contract.md`、`terminal_life_loop_engineering_contract.md` | `life_v0/terminal_turn/*`、`life_v0/terminal_loop/*` | terminal loop reports |

## 工程模块协同与对抗机制

这些机制必须在工程文档中显式存在。它们不是“安全附录”，而是数字生命避免退化成普通 agent 的核心。

| 协同/对抗 | 理论来源 | 工程文档 | 代码对象 | 必须保持的工程规则 |
|---|---|---|---|---|
| 工作区广播 vs 私有上下文 | `02`、`03`、`10`、`01m` | `code_architecture/02_runtime_object_bus_and_flow_contract.md`、`s02_neural_life_core_engineering_contract.md` | `WorkspaceFrame`、`ConsciousBroadcastFrame` | 语言、记忆、责任、梦境、行动必须读同一组 workspace refs |
| 内环境调制 vs 固定话术 | `04`、`07`、`11`、`18` | `engineering_depth/04_body_affect_dream_growth_engineering.md`、`s06_life_support_development_engineering_contract.md` | `NeedStateVector`、`CoreAffectVector`、`SignalMediaFrame` | 情绪和疲惫必须改变表达、等待、梦境、责任优先级 |
| 记忆写入 vs 梦境污染 | `05`、`08`、`17-31`、`95`、`99` | `life_state_store_v0_schema.md`、`code_scaffolds/06_packet_c_memory_write_gate_state_merge_scaffold.md` | `MemoryWriteGate`、`StateMergeGuard`、`DreamFactGate` | 梦境可影响情绪和成长，但不能直接覆盖事实记忆 |
| 关系成长 vs 服务角色退化 | `09`、`85-90`、`96`、`101` | `code_architecture/04_language_as_primary_expression_system.md`、`s07_language_relationship_engineering_contract.md` | `RelationshipTimeline`、`SharedTerms`、`PostExpressionGate` | 外显语言不能把关系对象降成服务对象，也不能把主体降成工具 |
| 行动释放 vs 责任后果 | `06`、`75`、`80-84`、`94`、`98` | `20_queue_e_membrane_validator_logic_implementation_contract.md`、`05_prediction_membrane_action_engineering.md` | `GoNoGoGate`、`WorldContactGate`、`ResponsibilityLoopState` | 外部接触必须经过确认、后果评估、责任回写和修复链 |
| 成长可塑性 vs 自我连续 | `39`、`92`、`93`、`181-257` | `s10_runtime_growth_reconsolidation_engineering_contract.md`、`03_build_order_and_definition_of_done.md` | `PlasticityWindowFrame`、`GrowthPatchCandidateQueue`、`AntiForgettingReplayPlan` | 自我修改先 self-read、shadow、replay、validation、archive，不直接改核心自我 |
| resident 自主活动 vs 终端聊天壳 | `20`、`44`、`86`、`89-90`、`181-257` | `digital_life_process_supervisor_engineering_contract.md`、`06_resident_process_terminal_birth_engineering.md` | `ResidentLifecycleState`、`WaitingHeartbeat`、`ResidentAutonomousActivity` | 关闭终端后仍有心跳、回忆、梦境、成长、学习和恢复包 |
| 预测主动采样 vs 直接执行 | `01v-01ax`、`11`、`06` | `09_perception_prediction_world_contact_implementation_playbook.md`、`05_prediction_membrane_action_engineering.md` | `BeliefStateFrame`、`PredictionErrorField`、`ActiveSamplingPlan` | 不确定时先采样、澄清、验证或 shadow，不直接行动 |
| source authority vs 随意理论拼接 | `00`、`01*`、`142/145/151` | `s01_source_authority_engineering_contract.md`、`theory_closure_and_engineering_readiness_audit.md` | `SourceAuthorityRegistry` | 新机制必须有来源、质量等级、runtime carrier、life target refs |

## 每个工程文档的最低完备性

后续补任意 `docs/v0` 工程文档时，必须至少包含下面九项。少一项，就还不能指导代码生成。

| 项 | 要求 |
|---|---|
| 理论来源 | 列出具体 `docs/` 文档或编号族，不能只写“脑科学理论” |
| 理论逻辑提炼 | 用工程语言说明该理论解决什么生命问题 |
| 对象模型 | 写出对象名、字段、生命周期、写入时机 |
| 首写权 | 明确哪个 `life_v0` 文件首写该对象 |
| 消费链 | 明确哪些模块读取、调制、阻断或回写该对象 |
| 协同/对抗 | 写出与其他模块如何协同、何时互相抑制 |
| runtime 证据 | 指定 state/report/receipt/archive/replay 文件 |
| 失败路线 | 写出 blocked、quarantine、shadow、repair、retry、archive 等路线 |
| 验收 | 指定最小 tests、CLI gate 或 audit probe |

这九项是工程文档的 DoD。只写概念说明或模块职责，不算完成。

## 开发前回读规则

任何代码生成开始前，按下面顺序回读：

```text
当前 real-live0 专题
  -> 本文件找到理论覆盖族
  -> 原始理论文档
  -> 主工程文档
  -> slice / queue / package spec
  -> life_v0 首写文件
  -> runtime 证据
  -> tests / gate
```

如果当前机制跨多族，例如“情绪影响语言中的修复表达”，必须同时读：

1. `07/18/01s` 情绪人格自我族；
2. `09/85-90/01u` 语言族；
3. `06/94/98/01h/01r` 责任后悔修复族；
4. `04/11/01n/01l` 内环境和调质族；
5. 对应的 `body/*`、`language/*`、`membrane/*`、`neural_core/signal_media.py` 工程文档。

这就是“协同/对抗机制”的实际读法：不是先写某个孤立模块，而是按同一个生命事件穿过多个器官的方式写代码。

## 验证命令建议

本文档本身是文档追踪矩阵，验证分三类：

```bash
# 1. Markdown 格式
git diff --check -- docs/v0/mapping

# 2. 文档存在性
find docs -maxdepth 1 -type f -name '*.md' | wc -l
find docs/v0 -type f -name '*.md' | wc -l

# 3. 工程回链测试
python3 -m unittest tests.contracts.test_v0_contracts -v
python3 -m unittest tests.slices.test_doc_corpus_ingestor -v
```

本轮只写文档时，可以先执行 `git diff --check` 和存在性校验；真正改代码后必须继续跑对应 slice/process/bridge 测试。
