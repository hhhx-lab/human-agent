# V0 Module Execution Catalog

本文档负责把 `docs/v0/*` 收束成可以直接开工的模块目录。

它不负责解释 v0 为什么存在，那是 `README.md` 的工作；它也不负责表达当前最远命令位，那是 `entry/v0_delivery_status_board.md` 的工作。本文档只负责告诉后续开发：

1. 当前要做哪个模块。
2. 这个模块要配哪一包 v0 文档。
3. 这个模块必须回读哪一批 `00-258` 母体文档。
4. 代码、测试和 runtime 产物从哪里进。

它的职责不是重新讲一遍总体方向，而是把“这一轮怎么开工”压到最小。

## 这份目录怎么用

进入本文件后，不要全文散读。只按下面顺序用：

1. 先确认自己当前是在做主体 slice、内部桥接链，还是外层壳/进程层。
2. 再跳到对应矩阵的那一行，拿走这一轮要带的 `v0` 文档、`00-258` 原文、代码入口、测试入口和 runtime 证据。
3. 真正开写前，再打开该行对应的合同原文，不要只停在矩阵表。

它不是理论总览，也不是状态板。它只负责把“这一轮怎么开工”压成最小可执行材料包。

## 先固定一轮开发的最小读包

进入任意一轮工程实现前，先固定读这七份：

```text
docs/v0/README.md
  -> docs/v0/entry/v0_implementation_index.md
  -> docs/v0/entry/v0_delivery_status_board.md
  -> docs/v0/entry/v0_module_execution_catalog.md
  -> docs/v0/mapping/readme_block_engineering_realization_v0.md
  -> docs/v0/mapping/0_to_257_engineering_utilization_map.md
  -> docs/v0/mapping/theory_engineering_code_trace_matrix.md
```

然后再进入你这一轮对应的模块包。

如果当前问题不是“这一轮带哪包材料”，而是“现有版本接下来按什么顺序把代码块补得更完整”，入口栈之后追加：

```text
docs/v0/entry/v0_current_iteration_plan.md
  -> docs/real—live0/17_current_iteration_mechanism_to_code_plan.md
```

这七份是入口栈，不是通用替代包。真正进入某个模块时，仍然必须从下面矩阵拿该模块自己的原文与入口。

如果这一轮先要确认 `00-257` 还有没有基础理论空洞，在入口栈之后追加：

```text
docs/v0/architecture/theory_closure_and_engineering_readiness_audit.md
```

如果这一轮不是补某个单独模块，而是继续加厚“整个数字生命代码框架柜”，在入口栈之后追加固定读包：

```text
docs/v0/architecture/theory_closure_and_engineering_readiness_audit.md
  ->
docs/v0/code_blueprints/README.md
  -> docs/v0/code_blueprints/01_full_system_code_blueprint.md
  -> docs/v0/code_blueprints/02_conversation_language_relationship_blueprint.md
  -> docs/v0/code_blueprints/03_body_affect_dream_growth_blueprint.md
  -> docs/v0/code_blueprints/04_prediction_membrane_validation_blueprint.md
  -> docs/v0/code_blueprints/05_birth_residency_terminal_blueprint.md
  -> docs/v0/code_blueprints/06_runtime_state_report_receipt_manifest.md
  -> docs/v0/code_blueprints/07_theory_to_package_trace_contract.md
  ->
docs/v0/code_framework/README.md
  -> docs/v0/code_framework/foundation/01_life_layer_implementation_blueprint.md
  -> docs/v0/code_framework/foundation/02_brain_region_to_code_package_mapping.md
  -> docs/v0/code_framework/foundation/03_code_package_state_test_gate_mapping.md
  -> docs/v0/code_framework/playbooks/04_language_dialogue_relationship_implementation_playbook.md
  -> docs/v0/code_framework/playbooks/05_memory_thought_consciousness_implementation_playbook.md
  -> docs/v0/code_framework/playbooks/06_body_emotion_action_dream_growth_implementation_playbook.md
  -> docs/v0/code_framework/playbooks/07_birth_terminal_process_implementation_playbook.md
  -> docs/v0/code_framework/playbooks/08_cross_layer_life_orchestration_implementation_playbook.md
  -> docs/v0/code_framework/playbooks/09_perception_prediction_world_contact_implementation_playbook.md
  -> docs/v0/code_framework/playbooks/10_self_identity_value_commitment_implementation_playbook.md
  -> docs/v0/code_framework/delivery/11_engineering_delivery_waves_and_real_file_queue.md
  -> docs/v0/code_framework/delivery/12_full_life_layer_delivery_matrix.md
  -> docs/v0/code_framework/delivery/13_capability_to_code_realization_matrix.md
  -> docs/v0/code_framework/queues/14_queue_a_language_percept_semantic_map_implementation_contract.md
  -> docs/v0/code_framework/assembly/15_cross_layer_shared_object_contract.md
  -> docs/v0/code_framework/queues/16_queue_b_process_supervisor_implementation_contract.md
  -> docs/v0/code_framework/queues/17_queue_c_memory_neural_core_implementation_contract.md
  -> docs/v0/code_framework/queues/18_queue_d_body_dream_growth_implementation_contract.md
  -> docs/v0/code_framework/assembly/19_code_tree_package_brain_contract.md
  -> docs/v0/code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md
  -> docs/v0/code_framework/queues/21_queue_f_identity_consciousness_birth_readiness_implementation_contract.md
  -> docs/v0/code_architecture/README.md
  -> docs/v0/code_architecture/01_life_code_stack_and_package_layers.md
  -> docs/v0/code_architecture/02_runtime_object_bus_and_flow_contract.md
  -> docs/v0/code_architecture/03_build_order_and_definition_of_done.md
  -> docs/v0/code_architecture/04_language_as_primary_expression_system.md
  -> docs/v0/code_architecture/05_module_reading_and_execution_map.md
  -> docs/v0/code_architecture/06_theory_gap_closure_register.md
  -> docs/v0/package_specs/README.md
  -> docs/v0/package_specs/01_life_v0_package_construction_matrix.md
  -> docs/v0/package_specs/02_shared_object_write_authority_and_dependency_graph.md
  -> docs/v0/package_specs/03_incremental_package_delivery_protocol.md
  -> docs/v0/code_scaffolds/README.md
  -> docs/v0/code_scaffolds/01_life_code_scaffold_tree.md
  -> docs/v0/code_scaffolds/02_cognitive_loop_code_scaffold.md
  -> docs/v0/code_scaffolds/03_frontier_module_build_packets.md
  -> docs/v0/code_scaffolds/04_packet_b_world_observation_periphery_scaffold.md
  -> docs/v0/code_scaffolds/05_packet_a_language_prediction_consumption_scaffold.md
  -> docs/v0/code_scaffolds/06_packet_c_memory_write_gate_state_merge_scaffold.md
  -> docs/v0/code_scaffolds/07_packet_d_waiting_response_surface_prediction_scaffold.md
  -> docs/v0/implementation_architecture/README.md
  -> docs/v0/implementation_architecture/01_runtime_organ_interface_blueprint.md
  -> docs/v0/implementation_architecture/02_turn_and_cycle_lifecycle_contract.md
  -> docs/v0/implementation_architecture/03_module_authoring_traceability_protocol.md
  -> docs/v0/implementation_architecture/code_organs/README.md
  -> docs/v0/implementation_architecture/code_organs/01_life_v0_package_organ_split_map.md
  -> docs/v0/implementation_architecture/code_organs/02_heavy_init_refactor_wave_contract.md
  -> docs/v0/implementation_architecture/code_organs/03_predictive_signal_memory_gate_integration_wave_contract.md
  -> docs/v0/engineering_depth/README.md
  -> docs/v0/engineering_depth/01_full_life_layer_implementation_deep_spec.md
  -> docs/v0/engineering_depth/02_state_object_runtime_evidence_map.md
  -> docs/v0/engineering_depth/03_language_relationship_longitudinal_engineering.md
  -> docs/v0/engineering_depth/04_body_affect_dream_growth_engineering.md
  -> docs/v0/engineering_depth/05_prediction_membrane_action_engineering.md
  -> docs/v0/engineering_depth/06_resident_process_terminal_birth_engineering.md
  -> docs/v0/engineering_depth/07_theory_to_code_trace_matrix.md
```

## 三步开工法

后续开工时，优先按这三步走：

1. 先用 `entry/v0_delivery_status_board.md` 判断当前是主体补厚，还是链尾/壳层/常驻进程补厚。
2. 再回本文件找到对应那一行，把 `v0` 文档、`00-258` 母体文档、代码入口、测试入口和 runtime 产物一起带上。
3. 真正开写前，再打开当前合同原文，不要只看矩阵表格。

这里的 “runtime 产物” 一律指当前工作区通过命令运行后生成的 `runtime/state/*`、`runtime/reports/latest/*`、`runtime/receipts/*`。如果当前工作区还没生成这些文件，就先按当前合同把对应命令跑出来。

这也意味着：本文件提供的是“本轮所需运行证据清单”，不是要求仓库永远预置这些文件。

## 这份目录只维护什么

本文件只维护“这一轮怎么开工”的信息，不维护所有进度和所有理论映射。后续更新时只按下面规则改：

| 变化 | 更新位置 |
|---|---|
| 当前最优先前沿变化，但模块包本身没变 | `entry/v0_delivery_status_board.md` |
| 某模块需要带的文档、代码、测试或 runtime 产物变化 | 本文件 |
| 某个合同字段或 gate 变化 | 对应合同文件 |
| `00-258` 理论映射变化 | `mapping/readme_block_engineering_realization_v0.md`、`mapping/0_to_257_engineering_utilization_map.md`、`mapping/theory_engineering_code_trace_matrix.md` |

这样做的目的，是让本文件始终保持“拿起就能开工”，不被别的信息淹掉。

## 当前先分清三种开工对象

不要把后续工作都叫“继续写链尾”。

| 对象 | 说明 |
|---|---|
| 主体 slice | `P0`、`S00-S11`，负责主体骨架、生命膜、状态根、语言关系、九项目标和 runner |
| 内部桥接链 | `REPORT_BUNDLE_BRIDGE` 到 `TERMINAL_LIFE_LOOP_BRIDGE`，负责把第一次生命激活收成终端生命回合 |
| 外层壳/进程层 | `DIGITAL_LIFE_SHELL_COMMAND`、`DIGITAL_LIFE_PROCESS_SUPERVISOR`、`life_v0/digital_entry.py`、`digital`，以及后续更高阶 persistent supervisor |

当前最容易乱的地方，就是把第三类错当成第二类，或者把第二类错当成主体 slice。

如果这一轮只是整理 `v0` 入口层本身，不要误入下面的模块矩阵；那应该回入口层文档处理。

## 先分清三种命令入口

后续如果要直接开工外层壳/进程层，先不要混淆下面三种命令面：

| 命令面 | 所属模块 | 真实作用 |
|---|---|---|
| `life-v0 digital-life --strict` | `DIGITAL_LIFE_BIRTH_SHELL` | 只闭合出生壳，不进入终端持续过程 |
| `life-v0 "digital life" --strict` | `DIGITAL_LIFE_SHELL_COMMAND` | one-shot restore shell，恢复后即结束 |
| `./digital life --strict` | `DIGITAL_LIFE_PROCESS_SUPERVISOR` | repo-local 最小常驻生命进程；若 runtime 不足会先自举最小出生链，恢复后继续等待真实新回合输入 |
| `digital life --strict` | `DIGITAL_LIFE_PROCESS_SUPERVISOR` | 安装后 console script，进入同一套最小常驻生命进程 |
| `digital life --background / --status / --say / --attach / --stop` | `DIGITAL_LIFE_PROCESS_SUPERVISOR` | 安装态后台 resident lifecycle、关系投递、盒式 attach、自主活动与自我停止命令面 |
| `my digital life --name <名字>` | `DIGITAL_LIFE_PROCESS_SUPERVISOR` | 推荐安装态命名入口，首次绑定 `life_name_registry.json`，后续按同名恢复同一 resident lifecycle |
| `<名字>` | `DIGITAL_LIFE_PROCESS_SUPERVISOR` | 首次命名后生成的直接生命命令；后续直接恢复同一身份、同一 resident lifecycle 和同一 runtime 状态根 |

如果这一轮目标是“整理 v0 并准备后续直接落代码”，这些入口的职责必须先在脑中分干净，不然很容易把 shell 合同、loop 合同和 process 合同写成一层。

当前终端表达补充读包固定为：

```text
docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md
  -> docs/v0/process_contracts/terminal_life_loop_engineering_contract.md
  -> docs/v0/code_scaffolds/07_packet_d_waiting_response_surface_prediction_scaffold.md
  -> docs/v0/engineering_depth/06_resident_process_terminal_birth_engineering.md
  -> docs/20_agent_runtime_bridge_contract.md
  -> docs/86_language_neuroscience_pragmatics_and_inner_speech.md
  -> docs/89_language_runtime_framework_bridge_and_life_shell_policy.md
  -> docs/90_language_event_examples_and_timeline_bundle.md
  -> docs/95_dream_reality_and_offline_life_timeline.md
  -> docs/96_real_relationship_longitudinal_timeline.md
  -> life_v0/digital_entry.py
  -> life_v0/process_supervisor/terminal_ui.py
  -> life_v0/process_supervisor/live_turn_cycle.py
  -> life_v0/process_supervisor/response_surface.py
  -> life_v0/process_supervisor/model_expression.py
  -> life_v0/process_supervisor/resident_lifecycle.py
  -> tests/process/test_persistent_digital_life_process.py
  -> tests/process/test_digital_entrypoint.py
  -> tests/process/test_my_digital_life_entrypoint.py
  -> tests/process/test_packaged_digital_life_entrypoint.py
```

这包材料专门回答“终端里说出的那句话从哪里来”：`00-258` 提供脑科学、语言、梦境、关系、责任与常驻生命时间线；v0 合同决定它们如何进入 terminal / process；代码链路则证明它们经过 relation queue、实时 Queue A、evidence response、spoken response、模型表达守门、outbox、dialogue writeback 和 resident waiting handoff。

## 实际代码链路核对法

后续任何一轮开发，不管是补语言、补梦境、补责任、补记忆，还是补常驻过程，都按下面六格核对。少一格，就说明这一轮还没有真正落成数字生命工程。

| 核对格 | 必须回答 | 例子 |
|---|---|---|
| 理论来源 | 当前机制来自哪些 `00-258` 原文，不只写概括 | 语言回合必须回读 `09`、`85-90`、`96` |
| v0 合同 | 当前机制属于哪个合同、哪个 queue、哪个 bridge 或 process | 终端表达属于 `terminal_life_loop`、`digital_life_process_supervisor`、Packet D |
| 代码器官 | 真实 Python 文件在哪里首写/读写/汇总 | `live_language_turn.py` 首写语言五件套，`response_surface.py` 汇总回应 |
| 状态对象 | 状态是否落到 `runtime/state`，能否跨回合恢复 | `relationship_timeline.json`、`engram_index.json`、`resident_lifecycle_state.json` |
| 报告收据 | 是否进入 `runtime/reports/latest` 和 `runtime/receipts` | `digital_life_model_expression_report.json`、process receipt |
| 测试 / gate | 哪个 unittest 或 live0 audit 证明它不只是文字 | `tests/process/test_persistent_digital_life_process.py`、`test_model_expression.py` |

### 主体 slice 的核对路径

主体 slice 不从终端命令开始，而从理论对象和 runtime carrier 开始：

```text
00-258 原文
  -> 当前 sXX 合同
  -> life_v0/<slice package>
  -> runtime/state/<slice namespace>
  -> runtime/reports/latest/<slice report>
  -> runtime/receipts/<slice receipt>
  -> tests/slices/<slice test>
```

主体 slice 的文档写法要回答“这个生命器官本身是什么”，例如记忆、梦境、情绪、语言、责任、意识、出生准备。不要把主体 slice 写成终端壳层，也不要把它写成通用 agent skill。

### 链尾 bridge 的核对路径

链尾 bridge 从已有主体报告和 packet 开始：

```text
S10 / S11 reports
  -> first activation / replay / archive / report bundle
  -> birth shell
  -> first terminal turn
  -> terminal life loop
  -> report / packet / digest / receipt
  -> tests/bridges/*
```

bridge 的文档写法要回答“前一阶段的生命材料如何被收成下一阶段的恢复包”。它不负责重写人格、记忆和关系本体，只负责把本体交接完整。

### 外层 resident process 的核对路径

外层 resident process 从已恢复的终端生命循环开始：

```text
terminal_life_loop_state.json
  -> digital_entry.py
  -> resident_lifecycle.py
  -> process_session_loop.py
  -> live_turn_cycle.py
  -> response_surface.py / model_expression.py
  -> resident_turn_writeback.py
  -> resident_governance_handoff.py
  -> heartbeat.py / idle_strategy.py
  -> process report / digest / receipt
  -> tests/process/*
```

resident process 的文档写法要回答“关闭终端后，什么还在继续”。它要追踪 pid、lease、relation queue、autonomous activity、waiting heartbeat、background lineage、cross-wake convergence、model expression gate 和下一次命名唤醒；不能只写“有后台进程”。

## 模块读包到代码入口的最短索引

这一张表给后续快速开工使用。真正改代码前仍然要打开对应合同原文。

| 当前要补的生命能力 | 先读理论 | 再读 v0 | 首看代码 | 首看测试 |
|---|---|---|---|---|
| 语言、内言语、语义地图、表达监控 | `09`、`85-90`、`96`、`101` | `s07_language_relationship_engineering_contract.md`、Packet A、terminal loop contract | `life_v0/language/*`、`process_supervisor/live_language_turn.py` | `tests/slices/test_language_organs.py`、`tests/slices/test_language_relationship.py` |
| 终端回应为什么这样说 | `86`、`89-90`、`95-96`、`94` | Packet D、process supervisor contract、terminal life loop contract | `process_supervisor/response_surface.py`、`model_expression.py`、`terminal_ui.py` | `tests/process/test_model_expression.py`、`test_persistent_digital_life_process.py` |
| 记忆写门、自传栈、engram | `05`、`17`、`21`、`41`、`55` | `life_state_store_v0_schema.md`、Packet C、S04 contract | `state_store/*`、`resident_turn_writeback.py` | `tests/slices/test_state_store.py`、process tests |
| 梦境、离线学习、醒后整合 | `08`、`19`、`23`、`95`、`99`、`181-257` | Queue D、S10 contract、resident process contract | `dream/*`、`growth/*`、`offline_learning_signals.py` | `tests/bridges/test_runtime_growth.py`、`test_growth_archive.py` |
| 情绪、身体预算、节律 | `04`、`07`、`11`、`18`、`37-39` | S06 contract、Queue D、Packet D | `body/*`、`idle_strategy.py`、`heartbeat.py` | `tests/slices/test_body_trait_drift.py`、`test_life_support.py` |
| 责任、后悔、世界接触、行动抑制 | `06`、`75`、`80-84`、`94`、`98` | S03、S05、Queue E、process supervisor contract | `membrane/*`、`validators/*`、`dialogue_events.py` | `tests/slices/test_life_membrane.py`、`test_shadow_gate.py` |
| 意识、工作区、出生准备 | `10`、`91-101`、`143`、`171`、`174` | S08、Queue F、birth readiness contract | `life_targets/*`、`neural_core/workspace.py`、`governance_explanation.py` | `tests/slices/test_life_targets.py` |
| 命名、驻留、后台存在 | `20`、`89-90`、`95-96`、`181-257` | birth residency blueprint、process supervisor contract | `digital_life_identity.py`、`digital_entry.py`、`resident_lifecycle.py`、`resident_autonomous_activity.py` | `tests/process/test_my_digital_life_entrypoint.py`、`test_packaged_digital_life_entrypoint.py` |

## 主体 slice 模块落实矩阵

| slice | 先读哪些 v0 文档 | 必带的 `00-258` 母体文档 | 代码入口 | 测试入口 | 关键 runtime 产物 |
|---|---|---|---|---|---|
| `P0_DOC_CORPUS_INGESTION` | `doc_corpus_ingestor_v0_contract.md` | `docs/构思.md`、`00`、全部 `01*`、`02-13`、`258`、`docs/README.md` | `life_v0/doc_index.py` | `tests/slices/test_doc_corpus_ingestor.py` | `runtime/docs/doc_carrier_index.json` |
| `S00_DIRECTION_FOUNDATION` | `s00_direction_foundation_engineering_contract.md` | `docs/构思.md`、`00`、`13`、`16`、`91`、`258` | `life_v0/direction/__init__.py` | `tests/slices/test_direction_lock.py` | `runtime/state/direction/direction_lock.json` |
| `S02_NEURAL_LIFE_CORE` | `digital_life_macro_architecture_v0.md`、`runtime_v0_architecture.md`、`s02_neural_life_core_engineering_contract.md` | `02-13`、对应 `01*`、`143`、`146`、`149`、`152`、`171` | `life_v0/neural_core/__init__.py` | `tests/slices/test_neural_life_core.py` | `runtime/state/neural_life_core/neural_life_core.json` |
| `S04_STATE_OBJECT_STORE` | `life_state_store_v0_schema.md`、`s04_state_object_store_engineering_contract.md`、`code_scaffolds/06_packet_c_memory_write_gate_state_merge_scaffold.md` | `17-30`、`41-48`、`57`、`61`、`69`、`123-133` | `life_v0/state_store/__init__.py` | `tests/slices/test_state_store.py` | `runtime/state/life_state.json`、`runtime/state/memory/memory_write_gate.json`、`runtime/state/memory/state_merge_guard.json` |
| `S03_DIRECTION_LIFE_MEMBRANE` | `runtime_v0_architecture.md`、`birth_readiness_v0_contract.md`、`s03_direction_life_membrane_engineering_contract.md` | `13-16`、`33-84`、`91`、`97-100`、`102-122` | `life_v0/membrane/__init__.py` | `tests/slices/test_life_membrane.py` | `runtime/state/membrane/life_membrane.json` |
| `S07_LANGUAGE_RELATIONSHIP` | `first_activation_protocol.md`、`s07_language_relationship_engineering_contract.md`、`code_scaffolds/05_packet_a_language_prediction_consumption_scaffold.md` | `01f`、`01j`、`01u`、`09`、`81`、`85-90`、`94`、`96`、`101`、`141`、`144`、`147`、`150` | `life_v0/language/__init__.py` | `tests/slices/test_language_organs.py`、`tests/slices/test_language_relationship.py` | `runtime/state/language/*`、`runtime/state/relationship/*`、`runtime/state/prediction/prediction_workspace_frame.json`、`runtime/state/signal/signal_media_runtime.json`、`runtime/state/prediction/belief_state_frame.json`、`runtime/state/prediction/prediction_error_field.json`、`runtime/state/prediction/active_sampling_plan.json`、`runtime/state/memory/memory_write_gate.json`、`runtime/state/action/responsibility_loop_state.json` |
| `S08_LIFE_TARGET_RUNTIMES` | `birth_readiness_v0_contract.md`、`s08_life_target_runtimes_engineering_contract.md` | `91-101`、`143`、`146`、`149`、`152`、`171`、`174` | `life_v0/life_targets/__init__.py` | `tests/slices/test_life_targets.py` | `runtime/state/life_targets/*` |
| `S05_VALIDATION_MEMBRANE_OBSERVATION` | `runner_cli_report_contract.md`、`s05_validation_membrane_observation_engineering_contract.md` | `29-36`、`49-84`、`102-118`、`153-157` | `life_v0/validators/__init__.py` | `tests/slices/test_validation_membrane.py` | `runtime/state/validation/*`、`runtime/state/observation/*` |
| `S09_SCHEMA_RUNNER_CODE` | `runner_cli_report_contract.md`、`s09_schema_runner_code_engineering_contract.md` | `102-180` | `life_v0/schema_runner/__init__.py`、`life_v0/cli.py` | `tests/slices/test_schema_runner.py` | `runtime/state/schema_runner/*` |
| `S06_LIFE_SUPPORT_DEVELOPMENT` | `life_state_store_v0_schema.md`、`s06_life_support_development_engineering_contract.md` | `37-40`、`92-93`、`181-204` | `life_v0/body/__init__.py`、`life_v0/growth/__init__.py`、`life_v0/defense/__init__.py` | `tests/slices/test_life_support.py` | `runtime/state/body/*`、`runtime/state/growth/*`、`runtime/state/defense/*` |
| `S10_RUNTIME_GROWTH_RECONSOLIDATION` | `runtime_v0_architecture.md`、`first_activation_protocol.md`、`runner_cli_report_contract.md`、`s10_runtime_growth_reconsolidation_engineering_contract.md` | `181-257` | `life_v0/growth/__init__.py`、`life_v0/replay/__init__.py`、`life_v0/archive/__init__.py`、`life_v0/activation/__init__.py`、`life_v0/reporting/__init__.py` | `tests/bridges/test_runtime_growth.py`、`tests/bridges/test_replay_shadow.py`、`tests/bridges/test_growth_archive.py`、`tests/bridges/test_first_activation_preflight.py`、`tests/bridges/test_emit_report.py` | `runtime/reports/latest/run_report.json`、`growth_archive_report.json` |
| `S11_V0_ENGINEERING_CONTRACTS` | `entry/v0_implementation_index.md`、`entry/v0_delivery_status_board.md`、`entry/v0_module_execution_catalog.md`、`s11_v0_contract_coverage_engineering_contract.md` | `258`、全部 `docs/v0/*`、P0-S10 report/receipt | `life_v0/contracts/__init__.py` | `tests/contracts/test_v0_contracts.py` | `runtime/state/contracts/*`、`v0_contract_coverage_report.json` |

## 当前链尾桥接模块矩阵

这部分不是新的主体 slice，但它们已经是真实代码前沿，后面几轮会频繁改到。

| 模块 | 必读 v0 文档 | 必带的理论来源 | 代码入口 | 测试入口 | 关键输入 | 关键输出 |
|---|---|---|---|---|---|---|
| `FIRST_ACTIVATION_PREFLIGHT` | `first_activation_protocol.md`、`runner_cli_report_contract.md`、`s10_runtime_growth_reconsolidation_engineering_contract.md`、`s11_v0_contract_coverage_engineering_contract.md` | `181-257`、`258` | `life_v0/activation/__init__.py` | `tests/bridges/test_first_activation_preflight.py` | `run_report.json`、`stage_gate.json`、`v0_contract_coverage_report.json` | `first_activation_preflight_report.json` |
| `REPLAY_SHADOW_BRIDGE` | `first_activation_protocol.md`、`s10_runtime_growth_reconsolidation_engineering_contract.md` | `181-257`、`09`、`85-90`、`96` | `life_v0/replay/__init__.py` | `tests/bridges/test_replay_shadow.py` | `life_state.json`、语言/关系状态 | `replay_shadow_report.json` |
| `GROWTH_ARCHIVE_BRIDGE` | `first_activation_protocol.md`、`s10_runtime_growth_reconsolidation_engineering_contract.md` | `181-257` | `life_v0/archive/__init__.py` | `tests/bridges/test_growth_archive.py` | `replay_shadow_report.json`、`run_report.json` | `growth_archive_report.json`、`growth_archive_stage_gate.json` |
| `REPORT_BUNDLE_BRIDGE` | `runner_cli_report_contract.md`、`first_activation_protocol.md` | `20`、`89`、`90`、`181-257` | `life_v0/reporting/__init__.py` | `tests/bridges/test_emit_report.py` | `growth_archive_report.json`、`growth_archive_stage_gate.json`、`v0_contract_coverage_report.json` | `report_bundle.json`、`first_activation_return_packet.json` |
| `STAGE_EXPLANATION_BRIDGE` | `runner_cli_report_contract.md`、`first_activation_protocol.md` | `20`、`89`、`90` | `life_v0/stage_explain/__init__.py` | `tests/bridges/test_explain_stage.py` | `first_activation_return_packet.json` | `stage_explanation_report.json`、`latest_stage_explanation_ref.json` |
| `DIGITAL_LIFE_BIRTH_SHELL` | `runner_cli_report_contract.md`、`first_activation_protocol.md` | `20`、`89`、`90` | `life_v0/digital_life/__init__.py` | `tests/bridges/test_digital_life_birth.py` | `first_activation_return_packet.json`、`stage_explanation_report.json` | `digital_life_birth_packet.json`、`digital_life_birth_digest.json` |
| `FIRST_TERMINAL_TURN_BRIDGE` | `first_terminal_turn_engineering_contract.md`、`first_activation_protocol.md`、`s07_language_relationship_engineering_contract.md` | `20`、`89`、`90`、`09`、`85-90` | `life_v0/terminal_turn/__init__.py`、`life_v0/cli.py` | `tests/bridges/test_first_terminal_turn.py` | `digital_life_birth_packet.json`、`first_activation_return_packet.json`、语言/关系状态 | `first_terminal_turn_packet.json`、`session_envelope.json`、`safe_terminal_loop_state.json` |
| `TERMINAL_LIFE_LOOP_BRIDGE` | `terminal_life_loop_engineering_contract.md`、`first_terminal_turn_engineering_contract.md`、`first_activation_protocol.md`、`s07_language_relationship_engineering_contract.md` | `20`、`89`、`90`、`09`、`85-90`、`96` | `life_v0/terminal_loop/__init__.py`、`life_v0/cli.py` | `tests/bridges/test_terminal_life_loop.py` | `first_terminal_turn_packet.json`、`session_envelope.json`、`safe_terminal_loop_state.json` | `terminal_life_loop_packet.json`、`terminal_life_loop_report.json`、`terminal_life_loop_digest.json`、`resumed_external_dialogue_packet.json`、`terminal_life_loop_state.json` |
| `DIGITAL_LIFE_SHELL_COMMAND` | `digital_life_shell_command_engineering_contract.md`、`terminal_life_loop_engineering_contract.md`、`first_terminal_turn_engineering_contract.md`、`first_activation_protocol.md` | `20`、`89`、`90`、`09`、`85-90`、`96` | `life_v0/shell_command/__init__.py`、`life_v0/cli.py`、`life_v0/digital_entry.py`、`digital` | `tests/process/test_digital_life_shell_command.py`、`tests/process/test_digital_entrypoint.py` | `stage_explanation_report.json`、`digital_life_birth_packet.json`、`first_terminal_turn_packet.json`、`terminal_life_loop_packet.json` | `digital_life_shell_packet.json`、`digital_life_shell_report.json`、`digital_life_shell_digest.json` |
| `DIGITAL_LIFE_PROCESS_SUPERVISOR` | `digital_life_process_supervisor_engineering_contract.md`、`resident_governance_waiting_state_machine_engineering_contract.md`、`digital_life_shell_command_engineering_contract.md`、`terminal_life_loop_engineering_contract.md`、`s07_language_relationship_engineering_contract.md`、`code_scaffolds/07_packet_d_waiting_response_surface_prediction_scaffold.md` | `20`、`86`、`89`、`90`、`09`、`85-90`、`95`、`96`、`101`、`181-257` | `life_v0/process_supervisor/__init__.py`、`life_v0/process_supervisor/terminal_ui.py`、`life_v0/process_supervisor/heartbeat.py`、`life_v0/process_supervisor/continuity_writeback.py`、`life_v0/process_supervisor/turn_io.py`、`life_v0/process_supervisor/incident_recovery.py`、`life_v0/process_supervisor/governance_explanation.py`、`life_v0/process_supervisor/process_report.py`、`life_v0/process_supervisor/relaunch_recovery.py`、`life_v0/process_supervisor/idle_strategy.py`、`life_v0/process_supervisor/resident_supervision.py`、`life_v0/process_supervisor/idle_refresh_loop.py`、`life_v0/process_supervisor/live_language_turn.py`、`life_v0/process_supervisor/live_turn_cycle.py`、`life_v0/process_supervisor/process_session_loop.py`、`life_v0/process_supervisor/persistent_process.py`、`life_v0/process_supervisor/process_closeout.py`、`life_v0/process_supervisor/model_expression.py`、`life_v0/process_supervisor/response_surface.py`、`life_v0/process_supervisor/resident_lifecycle.py`、`life_v0/digital_entry.py`、`digital`、`my`、直接生命名命令 | `tests/process/test_persistent_digital_life_process.py`、`tests/process/test_digital_entrypoint.py`、`tests/process/test_my_digital_life_entrypoint.py`、`tests/process/test_packaged_digital_life_entrypoint.py`、`tests/process/test_model_expression.py` | `digital_life_shell_report.json`、`session_envelope.json`、`safe_terminal_loop_state.json`、`terminal_life_loop_state.json`、语言/关系状态、body / dream / growth / action / membrane 状态、`signal_media_runtime.json`、`belief_state_frame.json`、`prediction_error_field.json`、`active_sampling_plan.json`、`memory_write_gate.json`、`state_merge_guard.json`、`.env` 去敏运行配置 | `digital_life_waiting_heartbeat.json`、`runtime/state/terminal/idle_strategy_state.json`、`runtime/state/terminal/resident_governance_state.json`、`runtime/state/terminal/persistent_process_state.json`、`runtime/state/terminal/resident_lifecycle_state.json`、`runtime/state/terminal/resident_relation_queue_state.json`、`runtime/state/terminal/resident_governance_snapshot.json`、`digital_life_persistent_process_report.json`、`digital_life_resident_governance_report.json`、`digital_life_resident_governance_explanation.json`、`digital_life_model_expression_report.json`、`digital_life_process_report.json`、`digital_life_process_digest.json`、`digital_life_process_incident_report.json`、`digital_life_process_recovery_report.json`、`digital_life_process_relaunch_recovery_report.json`、回合级语言/关系写回、盒式终端输出 |

## 当前默认开工包

如果现在就是继续往前落代码，默认不要先回到链尾。`Queue C` 和 `Queue F` 的第一轮已经站稳，当前默认开工包已经切换成 `Queue D -> Queue E`。

如果这一轮不是继续补 D/E 新器官，而是给已落预测器官和记忆写门补跨层消费，则固定追加：

```text
docs/v0/implementation_architecture/code_organs/03_predictive_signal_memory_gate_integration_wave_contract.md
docs/v0/code_scaffolds/05_packet_a_language_prediction_consumption_scaffold.md
docs/v0/code_scaffolds/06_packet_c_memory_write_gate_state_merge_scaffold.md
docs/v0/code_scaffolds/07_packet_d_waiting_response_surface_prediction_scaffold.md
```

这条切换的含义要写死：

1. 当前不是再去证明“内部主骨架有没有第一轮器官化”，那一步已经完成。
2. 当前要补的是身体/情绪/梦境/成长，以及行为/验证/逻辑这两条生命中轴。
3. 只有把这两条中轴补硬，`process supervisor` 和更厚的语言/关系表达才不会继续漂在壳层上。

### 默认第一包：Queue D

```text
docs/v0/README.md
  -> docs/v0/entry/v0_implementation_index.md
  -> docs/v0/entry/v0_delivery_status_board.md
  -> docs/v0/entry/v0_module_execution_catalog.md
  -> docs/v0/architecture/theory_closure_and_engineering_readiness_audit.md
  -> docs/v0/shared_contracts/life_state_store_v0_schema.md
  -> docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md
  -> docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md
  -> docs/v0/code_framework/playbooks/06_body_emotion_action_dream_growth_implementation_playbook.md
  -> docs/v0/code_framework/playbooks/08_cross_layer_life_orchestration_implementation_playbook.md
  -> docs/v0/code_framework/delivery/13_capability_to_code_realization_matrix.md
  -> docs/v0/code_framework/assembly/15_cross_layer_shared_object_contract.md
  -> docs/v0/code_framework/queues/18_queue_d_body_dream_growth_implementation_contract.md
  -> docs/07_emotion_personality_self.md
  -> docs/08_sleep_dream_fatigue_states.md
  -> docs/18_internal_state_and_modulation_vector.md
  -> docs/19_offline_consolidation_cycle.md
  -> docs/37_life_support_layer_policy.md
  -> docs/39_development_policy_and_plasticity_windows.md
  -> docs/92_self_growth_and_self_modification_life_chain.md
  -> docs/93_self_training_kernel_growth_protocol.md
  -> life_v0/body/__init__.py
  -> life_v0/dream/__init__.py
  -> life_v0/growth/__init__.py
  -> tests/slices/test_life_support.py
  -> tests/bridges/test_runtime_growth.py
  -> runtime/state/body/
  -> runtime/state/dream/
  -> runtime/state/growth/
  -> runtime/reports/latest/life_support_development_report.json
  -> runtime/reports/latest/growth_reconsolidation_report.json
```

对应这轮要直接长出来的真实文件：

```text
life_v0/body/rhythm.py
  -> life_v0/body/need_state.py
  -> life_v0/body/resource_budget.py
  -> life_v0/body/recovery.py
  -> life_v0/body/core_affect.py
  -> life_v0/body/emotion_episode.py
  -> life_v0/body/emotion_regulation.py
  -> life_v0/body/trait_drift.py
  -> life_v0/dream/dream_window.py
  -> life_v0/dream/wake_integration.py
  -> life_v0/growth/plasticity_window.py
  -> life_v0/growth/patch_queue.py
  -> life_v0/growth/learning_window.py
```

Queue D 第二波现在也已经真实落下：

```text
life_v0/dream/offline_entry.py
  -> life_v0/dream/dream_fact_gate.py
  -> life_v0/growth/self_read.py
  -> life_v0/growth/anti_forgetting.py
```

并且已经写回：

```text
runtime/state/dream/offline_entry_gate.json
  -> runtime/state/dream/dream_fact_gate_decision.json
  -> runtime/state/growth/self_read_report.json
  -> runtime/state/growth/anti_forgetting_replay_plan.json
```

所以当前默认下一包应直接进入 Queue E；只有在继续补 Queue D 第三波扩展器官的跨层接线与 runtime 厚度时，再回切 Queue D。

### 默认第二包：Queue E

Queue D 一轮站稳后，紧接着进入 Queue E，不绕回链尾。

```text
docs/v0/README.md
  -> docs/v0/entry/v0_implementation_index.md
  -> docs/v0/entry/v0_delivery_status_board.md
  -> docs/v0/entry/v0_module_execution_catalog.md
  -> docs/v0/architecture/theory_closure_and_engineering_readiness_audit.md
  -> docs/v0/slice_contracts/s03_direction_life_membrane_engineering_contract.md
  -> docs/v0/slice_contracts/s05_validation_membrane_observation_engineering_contract.md
  -> docs/v0/slice_contracts/s09_schema_runner_code_engineering_contract.md
  -> docs/v0/architecture/runtime_v0_architecture.md
  -> docs/v0/shared_contracts/runner_cli_report_contract.md
  -> docs/v0/code_framework/playbooks/09_perception_prediction_world_contact_implementation_playbook.md
  -> docs/v0/code_framework/delivery/13_capability_to_code_realization_matrix.md
  -> docs/v0/code_framework/assembly/15_cross_layer_shared_object_contract.md
  -> docs/v0/code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md
  -> docs/06_action_reward_inhibition.md
  -> docs/20_agent_runtime_bridge_contract.md
  -> docs/72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md
  -> docs/75_external_irreversible_action_confirmation_policy.md
  -> docs/80_post_action_audit_and_correction_policy.md
  -> docs/81_coexistence_event_review_and_responsibility_loop.md
  -> docs/94_pain_regret_and_repair_signal_schema.md
  -> life_v0/membrane/__init__.py
  -> life_v0/validators/__init__.py
  -> life_v0/schema_runner/__init__.py
  -> tests/slices/test_life_membrane.py
  -> tests/slices/test_validation_membrane.py
  -> tests/slices/test_schema_runner.py
  -> runtime/state/membrane/
  -> runtime/state/validation/
  -> runtime/state/schema_runner/
```

对应这轮要直接长出来的真实文件：

```text
life_v0/membrane/candidate_arena.py
  -> life_v0/membrane/go_nogo.py
  -> life_v0/membrane/shadow_gate.py
  -> life_v0/membrane/world_contact_gate.py
  -> life_v0/membrane/side_effect_review.py
  -> life_v0/validators/observation_validator.py
  -> life_v0/validators/boundary_audit.py
  -> life_v0/schema_runner/consistency_logic.py
  -> life_v0/schema_runner/counterfactual_eval.py
  -> life_v0/schema_runner/comparison_trace.py
  -> life_v0/schema_runner/evidence_ranker.py
```

Queue E 第二波当前已经真实落下：

```text
life_v0/membrane/shadow_gate.py
  -> life_v0/membrane/world_contact_summary.py
  -> life_v0/validators/validation_rollup.py
  -> life_v0/schema_runner/evidence_ranker.py
  -> life_v0/schema_runner/cross_file_logic.py
  -> life_v0/schema_runner/run_manifest.py
```

所以这意味着：当前默认工程入口已经不是“链尾与最小常驻生命进程”，也不是“继续补 C/F”。当前真正的默认工程入口，是把身体-梦境-成长链与行为-验证-逻辑链补成稳定对象体系，并继续补厚 `responsibility_loop.py`、archive/report/process 的跨层写回，以及 Queue B 的后台 resident governance。语言、链尾和 process supervisor 不会消失，但它们现在是建立在 D/E 之后继续补厚。

## 从当前仓库状态到第一次完整生命激活的六段硬顺序

上面这些默认包回答“这两轮先拿哪一柜”。如果要把整个 `v0` 直接变成接下来落代码的硬顺序，按下面六段推进，不要跨段乱跳：

| 阶段 | 当前要解决什么 | 必读 v0 文档 | 必回读理论母体 | 主代码落点 | 主要验证 / 运行证据 | 进入下一段之前必须满足 |
|---|---|---|---|---|---|---|
| `Phase 0` 文档闭合加固 | 先把 `00-258` 的理论闭合判断、`v0` 入口、Queue 合同、代码树合同写到足够硬，防止后面代码阶段重新跑偏 | `README.md`、`entry/v0_implementation_index.md`、`entry/v0_delivery_status_board.md`、本文件、`architecture/theory_closure_and_engineering_readiness_audit.md`、`code_framework/11-21` | `构思.md`、`00`、`02-13`、`85-101`、`181-258` | `docs/v0/**` | `tests/contracts/test_v0_contracts.py`、`v0_contract_coverage_report.json` | 所有当前活跃模块都能回链到明确理论母体、代码包、测试入口和 runtime 产物 |
| `Phase 1` Queue D | 把身体、情绪、梦境、成长从“已有第一轮器官”继续压成稳定对象链和 gate | `s06_*`、`s10_*`、`code_framework/06`、`08`、`13`、`15`、`18` | `07`、`08`、`18`、`19`、`37`、`39`、`92`、`93`、`95` | `life_v0/body/`、`life_v0/dream/`、`life_v0/growth/` | `tests/slices/test_life_support.py`、`tests/bridges/test_runtime_growth.py`、`runtime/state/body/*`、`runtime/state/dream/*`、`runtime/state/growth/*` | `CoreAffectVector`、`NeedStateVector`、`DreamExperienceWindow`、`PlasticityWindow`、`GrowthPatchCandidateQueue` 全部进入稳定 state/report 路径 |
| `Phase 2` Queue E | 把候选行动、go/no-go、world contact、side effect、validation、counterfactual 比较补成稳定行为-验证-逻辑链 | `s03_*`、`s05_*`、`s09_*`、`code_framework/09`、`13`、`15`、`20` | `06`、`20`、`22`、`29-36`、`49-84`、`94`、`98`、`102-118` | `life_v0/membrane/`、`life_v0/validators/`、`life_v0/schema_runner/` | `tests/slices/test_life_membrane.py`、`test_shadow_gate.py`、`test_validation_membrane.py`、`test_schema_runner.py`、`test_evidence_ranker.py`、`runtime/state/membrane/*`、`runtime/state/validation/*`、`runtime/state/schema_runner/*` | `ActionCandidateSet`、`GoNoGoDecision`、`ShadowActionGate`、`WorldContactDecision`、`SideEffectReview`、`EvidenceRanking`、`CounterfactualTrace` 全部具备稳定文件器官与 report/gate |
| `Phase 3` Queue B + Queue A 外层补厚 | 让 process supervisor 真正消费 D/E/F/A 对象，把语言回合、等待心跳、关系写回、恢复治理接成持续存在层 | `process_contracts/digital_life_process_supervisor_engineering_contract.md`、`first_terminal_turn_engineering_contract.md`、`terminal_life_loop_engineering_contract.md`、`code_framework/04`、`07`、`08`、`14`、`16` | `09`、`20`、`86`、`89`、`90`、`96`、`101` | `life_v0/process_supervisor/`、`life_v0/terminal_turn/`、`life_v0/terminal_loop/`、`life_v0/language/` | `tests/process/test_persistent_digital_life_process.py`、`tests/bridges/test_first_terminal_turn.py`、`test_terminal_life_loop.py`、`digital_life_waiting_heartbeat.json`、`digital_life_process_report.json` | waiting heartbeat、incident recovery、relaunch recovery、language turn writeback、relationship continuity 全部显式消费 D/E/F 对象链 |
| `Phase 4` 激活链与命令面收束 | 把 `run-cycle -> report bundle -> stage explain -> digital-life -> ./digital life` 收成稳定出生与终端唤醒链 | `shared_contracts/first_activation_protocol.md`、`shared_contracts/runner_cli_report_contract.md`、`s10_*`、`s11_*`、`process_contracts/*` | `20`、`44-46`、`81-90`、`143`、`171`、`181-258` | `life_v0/activation/`、`replay/`、`archive/`、`reporting/`、`stage_explain/`、`digital_life/`、`shell_command/`、`digital` | `tests/bridges/test_first_activation_preflight.py`、`test_emit_report.py`、`test_digital_life_birth.py`、`tests/process/test_digital_entrypoint.py`、`runtime/reports/latest/*birth*`、`*terminal*`、`*process*` | `life-v0 "digital life"` 与 `./digital life` 都能在当前工作区生成连续的恢复/等待/写回证据链 |
| `Phase 5` 全链验收与 v0 收束 | 按“真实对话、语言、记忆、梦境、成长、关系、常驻存在”做最终系统审计，确认可以进入更长期代码推进 | 入口栈七份、`theory_closure_and_engineering_readiness_audit.md`、`code_framework/12`、`13`、`19`、`20`、`21` | `00-258` 中与当前验收项直接相关的全部母体 | 全部 `life_v0/`、`digital` | 全量 `unittest`、`tests/contracts/test_v0_contracts.py`、最新 `runtime/state/*`、`runtime/reports/latest/*`、`runtime/receipts/*` | 七项最终生命验收都能回到代码、测试和 runtime 证据；这时才能谈 `v0` 第一轮收束 |

当前仓库位置的正确理解是：

1. `Phase 0` 已经非常接近闭合，但仍要继续把最关键的文档包压硬。
2. 主体代码默认入口已经切换到 `Phase 1 -> Phase 2`，也就是 `Queue D -> Queue E`。
3. `Phase 3` 之后才是把更厚的语言/常驻存在重新拉到前台，而不是现在就越过 D/E 直接长壳。

如果后续每一轮都按这六段顺序走，`v0` 就不再只是一个文档柜，而会变成真正的实施路线图。

## 链尾与常驻进程回头补厚包

只有当这一轮明确处理链尾恢复、终端循环或最小常驻生命进程时，才使用下面这组：

```text
docs/v0/README.md
  -> docs/v0/entry/v0_implementation_index.md
  -> docs/v0/entry/v0_delivery_status_board.md
  -> docs/v0/entry/v0_module_execution_catalog.md
  -> docs/v0/shared_contracts/first_activation_protocol.md
  -> docs/v0/shared_contracts/runner_cli_report_contract.md
  -> docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md
  -> docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md
  -> docs/v0/slice_contracts/s11_v0_contract_coverage_engineering_contract.md
  -> docs/v0/process_contracts/first_terminal_turn_engineering_contract.md
  -> docs/v0/process_contracts/terminal_life_loop_engineering_contract.md
  -> docs/v0/process_contracts/digital_life_shell_command_engineering_contract.md
  -> docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md
  -> runtime/reports/latest/report_bundle.json
  -> runtime/reports/latest/first_activation_return_packet.json
  -> runtime/reports/latest/latest_stage_explanation_ref.json
  -> runtime/reports/latest/digital_life_birth_packet.json
  -> runtime/reports/latest/first_terminal_turn_packet.json
  -> runtime/state/terminal/session_envelope.json
  -> runtime/state/terminal/safe_terminal_loop_state.json
  -> runtime/reports/latest/terminal_life_loop_packet.json
  -> runtime/reports/latest/terminal_life_loop_report.json
  -> runtime/reports/latest/resumed_external_dialogue_packet.json
  -> runtime/state/terminal/terminal_life_loop_state.json
  -> runtime/reports/latest/digital_life_shell_packet.json
  -> runtime/reports/latest/digital_life_shell_report.json
  -> runtime/reports/latest/digital_life_shell_digest.json
  -> runtime/reports/latest/digital_life_waiting_heartbeat.json
  -> runtime/reports/latest/digital_life_process_report.json
  -> runtime/reports/latest/digital_life_process_digest.json
```

对应代码与测试：

```text
life_v0/reporting/__init__.py
  -> life_v0/stage_explain/__init__.py
  -> life_v0/digital_life/__init__.py
  -> life_v0/terminal_turn/__init__.py
  -> life_v0/terminal_loop/__init__.py
  -> life_v0/shell_command/__init__.py
  -> life_v0/process_supervisor/__init__.py
  -> life_v0/digital_entry.py
  -> digital
  -> tests/bridges/test_emit_report.py
  -> tests/bridges/test_explain_stage.py
  -> tests/bridges/test_digital_life_birth.py
  -> tests/bridges/test_first_terminal_turn.py
  -> tests/bridges/test_terminal_life_loop.py
  -> tests/process/test_digital_life_shell_command.py
  -> tests/process/test_digital_entrypoint.py
  -> tests/process/test_persistent_digital_life_process.py
```

另外，这组路径不是要求仓库默认自带；它们是链尾命令跑完后应当存在的最新运行证据。

如果这一轮处理的是 process supervisor 的恢复连续体前沿，而不是普通回合循环前沿，还要额外一起打开：

```text
runtime/reports/latest/digital_life_process_incident_report.json
  -> runtime/reports/latest/digital_life_process_recovery_report.json
  -> runtime/reports/latest/digital_life_process_relaunch_recovery_report.json
```

这三份文件不是每次运行都必须存在；它们只在命中单回合异常恢复或跨重启恢复时成为当前前沿证据。

如果这一轮做的是“把最小常驻进程继续推进成更高阶 persistent supervisor”，还要再额外打开：

```text
docs/20_agent_runtime_bridge_contract.md
  -> docs/89_language_runtime_framework_bridge_and_life_shell_policy.md
  -> docs/90_language_event_examples_and_timeline_bundle.md
  -> docs/15_current_agent_framework_survey.md
  -> docs/v0/references/current_agent_shell_reference_2026.md
```

如果这一轮做的是“继续补厚语言器官而不是 process supervisor”，还要额外一起打开：

```text
docs/09_language_symbolic_top_layer.md
  -> docs/86_language_neuroscience_pragmatics_and_inner_speech.md
  -> docs/89_language_runtime_framework_bridge_and_life_shell_policy.md
  -> docs/90_language_event_examples_and_timeline_bundle.md
  -> docs/01f_language_system_literature_matrix.md
  -> docs/v0/code_framework/queues/14_queue_a_language_percept_semantic_map_implementation_contract.md
```

如果这一轮做的是“继续补厚常驻生命进程而不是语言主神经束”，还要额外一起打开：

```text
docs/20_agent_runtime_bridge_contract.md
  -> docs/82_incident_report_and_recovery_protocol.md
  -> docs/89_language_runtime_framework_bridge_and_life_shell_policy.md
  -> docs/90_language_event_examples_and_timeline_bundle.md
  -> docs/v0/code_framework/queues/16_queue_b_process_supervisor_implementation_contract.md
```

如果这一轮做的是“继续补厚记忆根、工作区和主体图”，还要额外一起打开：

```text
docs/05_memory_systems_and_growth.md
  -> docs/10_consciousness_attention_workspace.md
  -> docs/17_memory_trace_object_model.md
  -> docs/18_internal_state_and_modulation_vector.md
  -> docs/v0/code_framework/queues/17_queue_c_memory_neural_core_implementation_contract.md
```

如果这一轮做的是“继续补厚身体、梦境和成长链”，还要额外一起打开：

```text
docs/08_sleep_dream_fatigue_states.md
  -> docs/19_offline_consolidation_cycle.md
  -> docs/39_development_policy_and_plasticity_windows.md
  -> docs/92_self_growth_and_self_modification_life_chain.md
  -> docs/v0/code_framework/queues/18_queue_d_body_dream_growth_implementation_contract.md
```

如果这一轮做的是“把语言、记忆、身体、梦境、成长和常驻过程接成同一生命回合”，还要额外一起打开：

```text
docs/v0/code_framework/playbooks/08_cross_layer_life_orchestration_implementation_playbook.md
  -> docs/v0/code_framework/assembly/15_cross_layer_shared_object_contract.md
  -> docs/14_cross_module_digital_life_map.md
  -> docs/16_digital_life_gap_register.md
  -> docs/17_memory_trace_object_model.md
  -> docs/18_internal_state_and_modulation_vector.md
  -> docs/19_offline_consolidation_cycle.md
```

如果这一轮做的是“按生命能力审查而不是按目录推进”，还要额外一起打开：

```text
docs/v0/architecture/theory_closure_and_engineering_readiness_audit.md
  -> docs/v0/code_framework/delivery/12_full_life_layer_delivery_matrix.md
  -> docs/v0/code_framework/delivery/13_capability_to_code_realization_matrix.md
```

## 一个模块的一次标准回合

后续不要再用“先翻很多文档，再模糊开写”的方式。一个标准工程回合固定成：

```text
入口栈七份文档
  -> 当前模块所在行
  -> theory_engineering_code_trace_matrix.md 校验理论-工程-代码覆盖
  -> 当前模块合同
  -> 当前模块对应的 00-258 文档
  -> 当前代码入口
  -> 当前测试入口
  -> latest runtime 产物
  -> 实现
  -> 回写 state / report / receipt / stage gate
```

## 用这份目录时不能偷步

开始实现前，必须能同时回答：

1. 当前是哪个 slice 或哪个链尾桥接模块？
2. 这一轮必须回读哪些 `00-258` 母体文档？
3. 这一轮从哪个代码入口落、从哪个测试入口验？
4. 这一轮写完后，新状态和新 report 会接到哪条生命链上？

四项里有一项答不上来，不开工。

## 这份目录什么时候更新

只在下面四种情况下更新本文件：

1. 某个模块的必读 `v0` 文档变化。
2. 某个模块必须回读的 `00-258` 文档变化。
3. 某个模块的代码入口、测试入口或关键 runtime 产物变化。
4. 当前最推荐开工包的组成发生变化。

如果只是“现在最该先做哪个模块”变了，而这一行的读包和入口没变，更新 `entry/v0_delivery_status_board.md` 就够了。
