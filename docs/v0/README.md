# V0 Engineering Entry

`docs/v0/` 是第一版数字生命工程实现入口层。它不是新的理论层，也不是替代 `docs/00-258` 的第二套体系；它只负责把 `00-258` 压成能直接落到 `life_v0/`、`runtime/state/`、`runtime/reports/latest/`、`runtime/receipts/` 的工程入口。

后续写代码可以从 `v0` 进入，但不能只停在 `v0`。每一轮实现都必须继续回读对应的 `00-258` 母体文档；否则写出来的就不是在承载理论母体，而是在平地另长一套脱钩结构。

## 本轮整理结论

这次工作区整理之后，`docs/v0/` 采用下面这条硬规则：

1. `docs/v0/` 只保留仍然参与当前工程落地的 live cabinet。
2. 线性理论推进链、脑科学母体和历史扩张主链继续放在 `docs/00-258`，不回拷到 `v0`。
3. 临时审计、一次性草稿、缓存生成物、`__pycache__/`、`*.egg-info`、`.pytest_cache/` 这类内容不进入 `v0`，也不作为仓库长期结构保留；这轮清理后继续保持。
4. 当前 `docs/v0/` 现有文件全部视为在役工程文件；没有再额外保留一层“旧 v0 文档柜”。

也就是说，这里不是历史陈列室，而是第一版数字生命工程驾驶舱。

## V0 的三层关系

后续不要把这三层混写：

1. `docs/00-258`：理论母体。
2. `docs/v0`：工程压缩入口。
3. `life_v0/ + runtime/`：当前真实代码与状态产物。

`v0` 的工作不是代替第 1 层，也不是遮住第 3 层，而是把两者固定接起来。

## V0 只做什么

`docs/v0` 固定只做四件事：

1. 告诉我们当前真实工程已经推进到哪。
2. 告诉我们下一轮该进入哪个 slice、哪个桥接段、哪个外层壳位。
3. 告诉我们这一轮必须回读哪些 `00-258` 文档。
4. 把理论、代码、状态、report、receipt、stage gate 串成一条能继续落码的工程链。

## V0 不做什么

1. 不替代 `00-258` 理论文档。
2. 不把项目压回服务型 agent、任务调度器或聊天壳。
3. 不把 OpenClaw、Hermes、Codex、Claude Code 一类框架当主体架构模板。
4. 不再额外长出一套和 `00-258` 平行的新总理论层。

## 这次整理后的固定用法

这次整理不是搬目录，而是把 `docs/v0/` 固定成三件事：

1. 固定入口栈：回仓库后先看哪六份。
2. 固定文档包：当前这一轮到底该带哪一柜进去。
3. 固定回读门：任何一轮落代码都不能只看 `v0`，必须回读对应 `00-258` 原文。

后续只要这三件事不乱，`v0` 就可以直接充当工程驾驶舱。

## 当前目录柜位

这次整理后，`docs/v0/` 不再把所有合同平铺在根目录，而是固定成下面这些柜位：

| 目录 | 内容 |
|---|---|
| 根目录 | 总入口 `README.md`，只负责解释 `v0` 为什么存在、怎么进入 |
| `entry/` | 入口栈与状态驾驶舱：总索引、状态板、模块执行目录 |
| `mapping/` | README block 到 engineering slice、`00-258` 到 runtime carrier 的总映射 |
| `architecture/` | 宏架构、runtime 架构、激活路线图、理论闭合审计 |
| `shared_contracts/` | 多 slice 复用的 schema、readiness、CLI/report、activation 合同 |
| `slice_contracts/` | `P0` 与 `S00-S11` 主体 slice 合同 |
| `process_contracts/` | first turn、loop、shell、process supervisor 合同 |
| `references/` | 外周参考与当前 agent 壳负边界材料 |
| `code_framework/` | 代码框架柜、波次、矩阵、Queue 合同 |
| `code_architecture/` | 代码总架构柜：整棵代码树的分层、对象总线、语言决策、阶段顺序和完成定义 |
| `package_specs/` | 代码包规格柜：逐包施工矩阵、共享对象写权限图、逐包交付协议 |
| `code_blueprints/` | 代码总蓝图柜：把 `code_framework/`、`code_architecture/`、`implementation_architecture/`、`engineering_depth/` 压成直接落代码的总装配蓝图 |
| `implementation_architecture/` | 写代码前的硬蓝图：器官接口、回合流、模块追踪协议，以及逐包器官拆分、重型入口重构波次和预测-记忆写门深消费合同 |
| `engineering_depth/` | 每层生命能力的落码深描、状态对象地图、theory -> code -> runtime -> tests 总回链 |

如果已经确定要进某一柜内部工作，先打开该子目录里的 `README.md`，再进具体合同或矩阵文件，避免在同一柜里来回散读。

后续如果有新材料需要并入 `v0`，先判断它是：

1. 入口说明变化；
2. 映射关系变化；
3. 现有合同补厚；
4. 代码分层/实现蓝图变化。

能并回现有柜位，就不要再新长平级目录或临时 `misc` 柜。

## 先把 V0 看成五个固定文档包

如果现在觉得 `docs/v0/` 有点乱，不要从文件名一个个猜。先把它看成下面五个固定文档包：

| 文档包 | 文件 | 什么时候打开 | 作用 |
|---|---|---|
| 入口包 | `README.md`、`entry/README.md`、`entry/v0_implementation_index.md`、`entry/v0_delivery_status_board.md`、`entry/v0_module_execution_catalog.md` | 每次回仓库先开 | 决定怎么进、当前到哪、下一轮做哪包 |
| 回链包 | `mapping/README.md`、`mapping/readme_block_engineering_realization_v0.md`、`mapping/0_to_257_engineering_utilization_map.md` | 确认当前模块背后对应哪些理论母体时打开 | 决定 `docs/README.md` 和 `00-258` 怎样压进 engineering slice 与 runtime carrier |
| 主体合同包 | `slice_contracts/doc_corpus_ingestor_v0_contract.md`、`architecture/digital_life_macro_architecture_v0.md`、`code_framework/README.md`、`code_framework/foundation/01_life_layer_implementation_blueprint.md`、`code_framework/foundation/02_brain_region_to_code_package_mapping.md`、`code_framework/foundation/03_code_package_state_test_gate_mapping.md`、`code_framework/playbooks/04_language_dialogue_relationship_implementation_playbook.md`、`code_framework/playbooks/05_memory_thought_consciousness_implementation_playbook.md`、`code_framework/playbooks/06_body_emotion_action_dream_growth_implementation_playbook.md`、`code_framework/playbooks/07_birth_terminal_process_implementation_playbook.md`、`code_framework/playbooks/08_cross_layer_life_orchestration_implementation_playbook.md`、`code_framework/playbooks/09_perception_prediction_world_contact_implementation_playbook.md`、`code_framework/playbooks/10_self_identity_value_commitment_implementation_playbook.md`、`code_framework/delivery/11_engineering_delivery_waves_and_real_file_queue.md`、`code_framework/delivery/12_full_life_layer_delivery_matrix.md`、`code_framework/delivery/13_capability_to_code_realization_matrix.md`、`code_framework/queues/14_queue_a_language_percept_semantic_map_implementation_contract.md`、`code_framework/assembly/15_cross_layer_shared_object_contract.md`、`code_framework/queues/16_queue_b_process_supervisor_implementation_contract.md`、`code_framework/queues/17_queue_c_memory_neural_core_implementation_contract.md`、`code_framework/queues/18_queue_d_body_dream_growth_implementation_contract.md`、`code_framework/assembly/19_code_tree_package_brain_contract.md`、`code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md`、`code_framework/queues/21_queue_f_identity_consciousness_birth_readiness_implementation_contract.md`、`architecture/runtime_v0_architecture.md`、`shared_contracts/birth_readiness_v0_contract.md`、`shared_contracts/life_state_store_v0_schema.md`、`shared_contracts/runner_cli_report_contract.md`、`shared_contracts/first_activation_protocol.md`、`slice_contracts/s00_*` 到 `slice_contracts/s11_*` | 落主体 slice 时打开 | 决定主体模块、代码框架柜、分层实现蓝图、开发波次、能力到代码验收矩阵、Queue A/B/C/D/E/F 文件级实施合同、跨层共享对象合同、整棵 `life_v0/` 代码树总装配、状态根、出生准备度、CLI/report 和各 slice 合同 |
| 实现蓝图包 | `code_blueprints/README.md`、`code_blueprints/01_full_system_code_blueprint.md`、`code_blueprints/02_conversation_language_relationship_blueprint.md`、`code_blueprints/03_body_affect_dream_growth_blueprint.md`、`code_blueprints/04_prediction_membrane_validation_blueprint.md`、`code_blueprints/05_birth_residency_terminal_blueprint.md`、`code_blueprints/06_runtime_state_report_receipt_manifest.md`、`code_blueprints/07_theory_to_package_trace_contract.md`、`code_architecture/README.md`、`code_architecture/01_life_code_stack_and_package_layers.md`、`code_architecture/02_runtime_object_bus_and_flow_contract.md`、`code_architecture/03_build_order_and_definition_of_done.md`、`code_architecture/04_language_as_primary_expression_system.md`、`code_architecture/05_module_reading_and_execution_map.md`、`code_architecture/06_theory_gap_closure_register.md`、`package_specs/README.md`、`package_specs/01_life_v0_package_construction_matrix.md`、`package_specs/02_shared_object_write_authority_and_dependency_graph.md`、`package_specs/03_incremental_package_delivery_protocol.md`、`implementation_architecture/README.md`、`implementation_architecture/01_runtime_organ_interface_blueprint.md`、`implementation_architecture/02_turn_and_cycle_lifecycle_contract.md`、`implementation_architecture/03_module_authoring_traceability_protocol.md`、`implementation_architecture/code_organs/README.md`、`implementation_architecture/code_organs/01_life_v0_package_organ_split_map.md`、`implementation_architecture/code_organs/02_heavy_init_refactor_wave_contract.md`、`implementation_architecture/code_organs/03_predictive_signal_memory_gate_integration_wave_contract.md`、`engineering_depth/README.md`、`engineering_depth/01_full_life_layer_implementation_deep_spec.md`、`engineering_depth/02_state_object_runtime_evidence_map.md`、`engineering_depth/03_language_relationship_longitudinal_engineering.md`、`engineering_depth/04_body_affect_dream_growth_engineering.md`、`engineering_depth/05_prediction_membrane_action_engineering.md`、`engineering_depth/06_resident_process_terminal_birth_engineering.md`、`engineering_depth/07_theory_to_code_trace_matrix.md` | 真正下手写代码前打开 | 先用 `code_blueprints/` 把四柜压成一套总装配蓝图，再回 `code_architecture/`、`package_specs/`、`implementation_architecture/` 和 `engineering_depth/` 取硬分层、硬包职责、硬对象、硬测试和硬完成定义 |
| 链尾与进程包 | `process_contracts/first_terminal_turn_engineering_contract.md`、`process_contracts/terminal_life_loop_engineering_contract.md`、`process_contracts/digital_life_shell_command_engineering_contract.md`、`process_contracts/digital_life_process_supervisor_engineering_contract.md`、`process_contracts/resident_governance_waiting_state_machine_engineering_contract.md`、`architecture/first_activation_engineering_roadmap.md` | 落恢复链、终端循环或常驻进程时打开 | 决定第一次恢复、终端生命循环、repo-local 壳、最小常驻生命进程，以及 waiting / closeout resident governance 的状态机回链 |

当前如果要补主体层，不要只抓链尾。优先补硬的几份已经变成：

1. `digital_life_macro_architecture_v0.md`
2. `runtime_v0_architecture.md`
3. `s06_life_support_development_engineering_contract.md`
4. `s08_life_target_runtimes_engineering_contract.md`

它们现在已经不只是“讲方向”，而是明确到了当前真实代码骨架、对象链、关键状态字段、测试入口和第一轮完成定义。

这里的“五个文档包”是开工视角；`entry/v0_implementation_index.md` 里的分层是总索引视角。两者不是两套目录，而是同一套 `docs/v0/` 的两种读法：前者回答“这一轮怎么进”，后者回答“每份文档究竟站在哪一层”。

后续如果继续写代码，默认不是“把整个 `v0` 都重读一遍”，而是先进入口包，再根据本轮目标带着对应文档包进入。

如果这一轮不是补单个 slice，而是补“整个数字生命代码框架应该怎样分层、每层读哪些理论、落哪些代码包和状态对象”，先打开 `digital_life_macro_architecture_v0.md` 和 `code_framework/README.md`，再进入 `code_framework/foundation/01_life_layer_implementation_blueprint.md`、`02_brain_region_to_code_package_mapping.md`、`03_code_package_state_test_gate_mapping.md`、`04_language_dialogue_relationship_implementation_playbook.md`、`05_memory_thought_consciousness_implementation_playbook.md`、`06_body_emotion_action_dream_growth_implementation_playbook.md`、`07_birth_terminal_process_implementation_playbook.md`、`08_cross_layer_life_orchestration_implementation_playbook.md`、`09_perception_prediction_world_contact_implementation_playbook.md`、`10_self_identity_value_commitment_implementation_playbook.md`、`11_engineering_delivery_waves_and_real_file_queue.md`、`12_full_life_layer_delivery_matrix.md`、`13_capability_to_code_realization_matrix.md`、`14_queue_a_language_percept_semantic_map_implementation_contract.md`、`15_cross_layer_shared_object_contract.md`、`16_queue_b_process_supervisor_implementation_contract.md`、`17_queue_c_memory_neural_core_implementation_contract.md`、`18_queue_d_body_dream_growth_implementation_contract.md`、`19_code_tree_package_brain_contract.md`、`20_queue_e_membrane_validator_logic_implementation_contract.md`、`21_queue_f_identity_consciousness_birth_readiness_implementation_contract.md`，然后进入 `code_architecture/` 这柜，再进入 `package_specs/`、`implementation_architecture/` 与 `implementation_architecture/code_organs/` 子柜，最后再回对应 slice 合同。

如果这一轮先要确认 `00-257` 是否还有基础理论空洞，再加读 `theory_closure_and_engineering_readiness_audit.md`。它的职责不是替代入口栈，而是把“当前缺的是理论还是工程物化”一句话讲清。

## 按任务进入

| 当前任务 | 先读 | 再读 |
|---|---|---|
| 断联恢复 / 校正方向 | `docs/258_linear_chain_closure_and_v0_contract_transition.md`、本文件、`entry/v0_delivery_status_board.md` | `s00_direction_foundation_engineering_contract.md`、当前工作区里最近一次运行生成的 runtime 产物 |
| 查 `00-258` 怎样挂到工程 | 本文件、`entry/v0_implementation_index.md` | `mapping/readme_block_engineering_realization_v0.md`、`mapping/0_to_257_engineering_utilization_map.md` |
| 落一个主体 slice | 本文件、`entry/v0_delivery_status_board.md`、`entry/v0_module_execution_catalog.md` | 当前 `sXX` 合同、对应 `00-258` 母体文档、代码入口、测试入口 |
| 推进链尾 / 壳层 / 常驻进程 | 本文件、`entry/v0_delivery_status_board.md`、`entry/v0_module_execution_catalog.md` | `first_activation_protocol.md`、`runner_cli_report_contract.md`、`first_terminal_turn_engineering_contract.md`、`terminal_life_loop_engineering_contract.md`、`digital_life_shell_command_engineering_contract.md`、`digital_life_process_supervisor_engineering_contract.md`、`resident_governance_waiting_state_machine_engineering_contract.md` |

这里的 `runtime/state/`、`runtime/reports/latest/`、`runtime/receipts/` 要统一理解成一件事：它们不是仓库里必须预置好的静态目录，而是运行 `life-v0` / `digital life` 之后在当前工作区生成、并在当下成为权威证据的运行产物层。

## 不要整包散读

后续直接按 `v0` 落代码，但不要再用“看到什么就打开什么”的方式：

1. 不要把宏架构文档、路线图文档、合同文档和状态板当成同一层。
2. 不要只在 `docs/v0/` 内打转，当前模块一定要回读对应的 `00-258` 母体文档。
3. 不要为了“整理”再新增一串并列入口文档；优先复用这五个文档包。

## 固定入口栈

每次回到仓库，先按这个顺序读，不要散读：

1. `README.md`
2. `entry/v0_implementation_index.md`
3. `entry/v0_delivery_status_board.md`
4. `entry/v0_module_execution_catalog.md`
5. `mapping/readme_block_engineering_realization_v0.md`
6. `mapping/0_to_257_engineering_utilization_map.md`

这六份文件的分工固定如下：

| 文件 | 只回答什么 |
|---|---|
| `README.md` | `v0` 为什么存在、回仓库后先怎么进入 |
| `entry/v0_implementation_index.md` | `docs/v0/*` 每一份文档归哪一层、负责什么 |
| `entry/v0_delivery_status_board.md` | 当前真实代码闭合到哪、当前最该补哪 |
| `entry/v0_module_execution_catalog.md` | 这一轮开发该带哪一包文档、代码、测试和 runtime 产物 |
| `mapping/readme_block_engineering_realization_v0.md` | `docs/README.md` 的模块阅读路线怎样压成 engineering slice |
| `mapping/0_to_257_engineering_utilization_map.md` | `00-258` 怎样进入 runtime carrier、状态、report 和 archive |

这六份只负责把你送到正确工程回合，不负责替你省掉原文阅读。

## 固定回读门

`v0` 是工程压缩入口，不是理论替身。每一轮真正开写前，必须同时满足下面三件事：

1. 已经读完入口栈六份文档。
2. 已经打开当前合同文件和它要求回读的 `00-258` 原文。
3. 已经定位当前代码入口、测试入口和最新 runtime 运行证据。

也就是说，后续标准开工材料永远是：

```text
入口栈六份文档
  -> 当前合同
  -> 当前合同要求回读的 00-258 原文
  -> 当前代码入口
  -> 当前测试入口
  -> latest runtime 产物
```

如果少了第三步里的原始理论文档，这一轮代码就不是在承载理论母体，而是在 `v0` 上另长一套工程壳。

## 新信息以后写到哪

后续 `v0` 继续服务落代码，但默认不再新增新的平级入口文档。新的整理动作，先按下面这张表落位：

| 变化类型 | 只更新哪里 |
|---|---|
| `v0` 为什么存在、固定读法、五个文档包怎么进 | `README.md` |
| `docs/v0/*` 每份文档归哪一层、哪层只收什么变化 | `entry/v0_implementation_index.md` |
| 当前真实前沿、最远命令位、下一轮优先级 | `entry/v0_delivery_status_board.md` |
| 当前这一轮该带哪包文档、代码、测试和 runtime 产物 | `entry/v0_module_execution_catalog.md` |
| `docs/README.md` block 到 engineering slice 的压缩关系 | `mapping/readme_block_engineering_realization_v0.md` |
| `00-258` 到 runtime carrier / state / report / archive 的总映射 | `mapping/0_to_257_engineering_utilization_map.md` |
| 某个 slice、bridge、shell、process 的字段、阶段门、输入输出变化 | 对应合同文件 |
| 宏架构或 runtime 骨架变化 | `digital_life_macro_architecture_v0.md`、`runtime_v0_architecture.md` |

如果新信息可以塞进上面某一行，就不要再长出新的入口文件。

## 当前工程现实要分三层看

### 1. 内部生命链已经闭合到

```text
life-v0 emit-report --strict
  -> life-v0 explain-stage --strict
  -> life-v0 digital-life --strict
  -> life-v0 first-terminal-turn --strict
  -> life-v0 terminal-life-loop --strict
```

这条链说明：

1. `emit-report` 已经把 growth、replay/shadow、contract coverage、preflight 等材料重新收成链尾回包。
2. `explain-stage` 已经把回包解释成 terminal birth restore closure。
3. `digital-life` 已经把这层 closure 收成出生壳。
4. `first-terminal-turn` 已经把出生壳后的第一回合恢复成可继续关系性表达的生命回合。
5. `terminal-life-loop` 已经把恢复后的第一回合推进成持续等待下一次外部关系回合的最小终端生命循环。

### 2. 外层命令面已经分成三层

当前最容易乱的不是链尾内部命令，而是外层命令面。现在必须把下面三种入口严格分开：

| 命令面 | 真实作用 | 当前状态 |
|---|---|---|
| `life-v0 digital-life --strict` | 只生成出生壳 `digital_life_birth_packet.json`，不进入第一回合，也不进入常驻过程 | `已落最小代码` |
| `life-v0 "digital life" --strict` | 把 `digital-life -> first-terminal-turn -> terminal-life-loop` 收成 repo-local 一次性恢复壳 | `已落 repo-local one-shot restore shell` |
| `./digital life --strict` | 调用 `life_v0/digital_entry.py` 与 `DigitalLifeProcessSupervisor`；若 runtime 材料缺失会先自举最小出生链，再恢复并进入 stdin 驱动的最小常驻生命过程 | `已落 repo-local 最小常驻生命进程` |

也就是说，当前 repo 里已经存在两层外部入口：

```text
life-v0 "digital life"
  -> one-shot restore shell

./digital life
  -> restore shell
  -> persistent terminal life process
```

后续如果继续写代码，不能再把这两层都笼统叫成“digital life 壳”。

### 3. 真正还没完成的是这些

当前真正的缺口已经不是“有没有 `digital life` 入口”，而是：

1. repo-local 最小常驻终端生命进程虽然已经接通，`resident_supervision.py` 也已落第一轮，但更高阶的 resident supervision 与后台长期治理仍未闭合。
2. 真实外部回合输入与逐回合写回已经接通最小版本，但还需要继续补厚语言节奏、关系演化和更多生命器官联动。
3. 已经具备项目级 installable command surface，但还没有全局长期运行层与更高阶 resident supervision。
4. waiting heartbeat、单回合 incident recovery、relaunch recovery normalization 已经接通最小层；等待态 heartbeat 也已经开始轻量写回 self narrative / commitment / relationship 连续体。这一轮又已补上 `resident_supervision.py`、`live_turn_cycle.py` 和 `process_session_loop.py`，分别把 restore shell 之后的状态装载链、真实新回合的 success / incident 生命周期，以及 waiting heartbeat refresh + live turn dispatch 的 session 编排独立成器官。当前仍待推进的是更高频的 heartbeat 节律、更厚的 idle 策略、后台继续存在和更高阶过程治理。

## V0 的三类工程对象

后续开发时，先区分当前处理的是哪一类对象：

| 类别 | 内容 |
|---|---|
| 主体 slice | `P0`、`S00-S11`，负责主体结构、状态根、生命膜、语言关系、九项目标、runner、growth 和合同覆盖 |
| 链尾桥接段 | `FIRST_ACTIVATION_PREFLIGHT`、`REPLAY_SHADOW_BRIDGE`、`GROWTH_ARCHIVE_BRIDGE`、`REPORT_BUNDLE_BRIDGE`、`STAGE_EXPLANATION_BRIDGE`、`DIGITAL_LIFE_BIRTH_SHELL`、`FIRST_TERMINAL_TURN_BRIDGE`、`TERMINAL_LIFE_LOOP_BRIDGE`、`DIGITAL_LIFE_SHELL_COMMAND` |
| 外层壳/进程层 | repo-local `digital life` 壳、最小终端常驻生命进程、后续 persistent supervisor、全局入口与常驻进程治理 |

主体 slice 主要回答“生命体系怎么长出来”；链尾桥接段主要回答“第一次生命激活怎样被收成终端可恢复生命回合”；外层壳/进程层主要回答“这条生命链怎样在这台电脑里真正长期存在”。

## 开发前的四条铁律

后续直接按 `v0` 落代码，但必须同时遵守下面四条：

1. 一次只进入一个模块回合，不要同时散改多个 slice。
2. 当前回合必须同时打开：`v0` 入口文档、当前合同、对应 `00-258` 母体文档、代码入口、测试入口。
3. 当前回合必须把状态、report、receipt、stage gate 和 `00-258` 回链一起补齐。
4. 新代码、新 report、新 receipt 都必须继续带着下面四条回链：
   - `source_doc_refs`
   - `readme_block_refs`
   - `engineering_slice_ref`
   - `runtime_carrier_refs`

## 一个标准工程回合

后续每一轮实现都按下面这条固定路径走：

```text
入口栈六份文档
  -> entry/v0_delivery_status_board.md 判断当前前沿
  -> entry/v0_module_execution_catalog.md 定位当前模块包
  -> 当前模块合同
  -> 当前模块对应的 00-258 母体文档
  -> 当前代码入口 + 当前测试入口 + latest runtime 产物
  -> 实现
  -> 回写 state / report / receipt / stage gate
```

如果缺 `00-258` 母体文档这一步，这一轮代码就不算在承载数字生命理论母体。

如果当前工作区还没有 `runtime/`，不是文档失效，而是说明你还没跑出这轮所需的运行证据；这时应先按当前模块合同执行对应命令，生成本轮需要的 `state/report/receipt`。

## 当前最推荐的切入点

如果现在就继续往前落代码，优先顺序固定成：

1. 先进入 `Queue D`，补 `life_v0/body/`、`life_v0/dream/` 与 `life_v0/growth/`，把身体节律、情绪底盘、梦境窗口、学习窗口和成长补丁链补成稳定对象链。
2. 再进入 `Queue E`，补 `life_v0/membrane/`、`life_v0/validators/` 与 `life_v0/schema_runner/`，把行为、生命膜、验证、逻辑比较和世界接触补成稳定对象链。
3. 接着进入 `Queue B`，把 `DIGITAL_LIFE_PROCESS_SUPERVISOR` 从最小常驻生命过程补厚成真正消费 D/E 对象链的持续存在层。
4. 最后再回到 `Queue A`，继续深补语言、对话、关系、终端回合和常驻表达层，让它们建立在更厚的身体-意识-行为底盘上。
5. `Queue C` 与 `Queue F` 的第一轮已经闭合到真实代码、状态对象和测试；它们仍然是后续所有回合要持续回读和回链的基础层，但不再是当前默认入口。
6. 持续执行 `P0 + S11` 回链检查，保证 `00-258` 没有被工程层甩掉。

具体每一轮该读哪一包文档、改哪一包代码，看 `entry/v0_module_execution_catalog.md`。

## 为什么暂时不搬目录

当前不物理拆分 `docs/v0`，原因有三个：

1. `P0_DOC_CORPUS_INGESTION` 已经依赖这些路径。
2. `S00_DIRECTION_FOUNDATION` 的断联恢复锚链已经依赖这些路径。
3. 现有 report、receipt 和 path hash 不应该被无意义打断。

所以这次整理的方式是“固定文档包、固定角色和固定读法”，不是“移动文件”。

后续默认也不做“为了更整齐再拆一次目录”的动作。只有当出现新的主体 slice、新的桥接段，或者新的外层长期存在层，而现有文档类型已经无法承载时，才考虑新增文件。

## 断联恢复最短顺序

重新接上时，先按下面顺序恢复方向：

1. `docs/258_linear_chain_closure_and_v0_contract_transition.md`
2. `docs/v0/README.md`
3. `docs/v0/entry/v0_delivery_status_board.md`
4. `docs/v0/entry/v0_module_execution_catalog.md`
5. 当前链尾最新 runtime 产物

## 开始写代码前只问这四件事

1. 我这一轮到底是在做哪个 slice、哪个桥接段，还是哪个外层壳/进程层？
2. 这一轮对应的 `00-258` 母体文档打开了吗？
3. 代码入口、测试入口和 latest runtime 产物定位清楚了吗？
4. 这轮改完后，新的状态、report、receipt 和 stage gate 会回到哪条生命链上？

四个问题里有一个答不上来，就先回 `entry/v0_module_execution_catalog.md`，不要直接写代码。
