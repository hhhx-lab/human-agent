# V0 Implementation Index

本文档只负责做 `docs/v0/*` 的总索引，不负责重写进度，也不负责重写 `00-258` 映射。

如果你当前最关心的是：

- “v0 这层为什么存在” -> 回 `../README.md`
- “当前代码已经跑到哪” -> 回 `entry/v0_delivery_status_board.md`
- “我这一轮该带哪一包文档和代码” -> 回 `entry/v0_module_execution_catalog.md`

## 先用这份索引做什么

这份索引不是开工清单，而是分柜器。它最适合处理下面四种问题：

1. 我现在看的这份文档，到底属于入口、映射、合同，还是外层壳？
2. 这次新变化该写回哪一层，而不是同时抄进四五份文档？
3. `../README.md` 里的“五个固定文档包”和 `docs/v0/*` 的真实层级关系是什么？
4. 我当前是在补主体 slice、链尾桥接段，还是外层常驻过程？

如果你已经明确“这轮就是要落某个模块”，请直接回 `entry/v0_module_execution_catalog.md`。

## 本轮工作区整理后怎么理解它

这次整理没有把 `docs/v0/` 再拆成更多层，而是把边界收紧了：

1. `docs/v0/` 只放当前仍然参与工程落地的入口、映射、合同、架构和实现蓝图。
2. `docs/00-258` 继续承载线性理论母体，不在 `v0` 里复制第二份。
3. 临时调试说明、一次性草稿、缓存生成物不进入这里；它们要么并回现有柜位，要么在提交前删除。
4. 当前这份索引以下列出的柜位都默认是 active cabinet，不再额外维护“旧版 v0 文档层”。

所以这份文件不是给 `v0` 继续长枝杈，而是给它立柜门。

## 入口原则

`v0` 现在已经不是“缺文档”，而是“入口太多容易撞层”。所以读这份索引时只记一条：

1. 先判断当前是在看入口、回链、主体合同，还是链尾/进程合同。
2. 一轮开发只带一个主合同包进入，不要把十层都同时当作“当前要改的文档”。

## 目录柜位

当前 `docs/v0/` 的实体目录已经固定为：

- 根目录：总入口 `README.md`
- `entry/`：入口层
- `mapping/`：映射层
- `architecture/`：总架构层
- `shared_contracts/`：共用合同层
- `slice_contracts/`：主体 slice 合同层
- `process_contracts/`：链尾桥接与外层壳/进程合同层
- `references/`：外周参考层
- `code_framework/`：代码框架层
- `code_architecture/`：代码总架构层
- `implementation_architecture/`：实现蓝图层

这次整理之后，后续如果有人觉得 `v0` “又乱了”，先不要新建目录；先回到上面这十个柜位里判断应该并回哪一柜。

## 文档分层

`docs/v0` 现在固定成十层：

| 层 | 文件 | 作用 |
|---|---|---|
| 入口层 | `../README.md`、`README.md`、`v0_implementation_index.md`、`v0_delivery_status_board.md`、`v0_module_execution_catalog.md` | 说明入口、总索引、当前进度和模块执行目录 |
| 映射层 | `../mapping/README.md`、`../mapping/readme_block_engineering_realization_v0.md`、`../mapping/0_to_257_engineering_utilization_map.md`、`../architecture/theory_closure_and_engineering_readiness_audit.md` | 把 `docs/README.md` 和 `00-258` 压成工程 slice 与 runtime carrier，并校核当前差距在理论还是工程 |
| 总架构层 | `digital_life_macro_architecture_v0.md`、`runtime_v0_architecture.md`、`first_activation_engineering_roadmap.md` | 固定宏架构、runtime 结构和第一次生命激活路线 |
| 代码框架层 | `code_framework/README.md`、`code_framework/foundation/01_life_layer_implementation_blueprint.md`、`code_framework/foundation/02_brain_region_to_code_package_mapping.md`、`code_framework/foundation/03_code_package_state_test_gate_mapping.md`、`code_framework/playbooks/04_language_dialogue_relationship_implementation_playbook.md`、`code_framework/playbooks/05_memory_thought_consciousness_implementation_playbook.md`、`code_framework/playbooks/06_body_emotion_action_dream_growth_implementation_playbook.md`、`code_framework/playbooks/07_birth_terminal_process_implementation_playbook.md`、`code_framework/playbooks/08_cross_layer_life_orchestration_implementation_playbook.md`、`code_framework/playbooks/09_perception_prediction_world_contact_implementation_playbook.md`、`code_framework/playbooks/10_self_identity_value_commitment_implementation_playbook.md`、`code_framework/delivery/11_engineering_delivery_waves_and_real_file_queue.md`、`code_framework/delivery/12_full_life_layer_delivery_matrix.md`、`code_framework/delivery/13_capability_to_code_realization_matrix.md`、`code_framework/queues/14_queue_a_language_percept_semantic_map_implementation_contract.md`、`code_framework/assembly/15_cross_layer_shared_object_contract.md`、`code_framework/queues/16_queue_b_process_supervisor_implementation_contract.md`、`code_framework/queues/17_queue_c_memory_neural_core_implementation_contract.md`、`code_framework/queues/18_queue_d_body_dream_growth_implementation_contract.md`、`code_framework/assembly/19_code_tree_package_brain_contract.md`、`code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md`、`code_framework/queues/21_queue_f_identity_consciousness_birth_readiness_implementation_contract.md` | 固定代码框架柜，把生命层、脑区映射、代码包、state/report/receipt/test/gate 串成可施工结构，并补出真实开发波次、文件拆分队列、全生命层总施工矩阵、能力到代码验收矩阵、Queue A/B/C/D/E/F 的文件级实施合同、跨层共享对象硬合同，以及整棵 `life_v0/` 代码树总装配合同 |
| 代码总架构层 | `code_architecture/README.md`、`code_architecture/01_life_code_stack_and_package_layers.md`、`code_architecture/02_runtime_object_bus_and_flow_contract.md`、`code_architecture/03_build_order_and_definition_of_done.md`、`code_architecture/04_language_as_primary_expression_system.md`、`code_architecture/05_module_reading_and_execution_map.md`、`code_architecture/06_theory_gap_closure_register.md` | 把代码框架柜继续压成整棵代码树的生命分层、跨层共享对象总线、语言主表达系统、模块级读包执行地图、理论缺口收口方式、实现语言决策、阶段顺序和完成定义 |
| 实现蓝图层 | `implementation_architecture/README.md`、`implementation_architecture/01_runtime_organ_interface_blueprint.md`、`implementation_architecture/02_turn_and_cycle_lifecycle_contract.md`、`implementation_architecture/03_module_authoring_traceability_protocol.md`、`implementation_architecture/code_organs/README.md`、`implementation_architecture/code_organs/01_life_v0_package_organ_split_map.md`、`implementation_architecture/code_organs/02_heavy_init_refactor_wave_contract.md` | 把代码总架构层再压成真实器官接口、外部回合流、离线成长流、逐包器官拆分图和模块级理论-代码追踪协议 |
| 共用合同层 | `life_state_store_v0_schema.md`、`birth_readiness_v0_contract.md`、`runner_cli_report_contract.md`、`first_activation_protocol.md` | 给多个模块共用的状态、出生准备度、CLI/report 和激活协议 |
| 主体 slice 合同层 | `doc_corpus_ingestor_v0_contract.md`、`s00_*` 到 `s11_*` | 主体骨架、状态根、生命膜、语言关系、九项目标、runner、growth 和合同覆盖 |
| 链尾桥接合同层 | `first_terminal_turn_engineering_contract.md`、`terminal_life_loop_engineering_contract.md` | 把 terminal birth restore 收成可继续的终端生命回合 |
| 外层壳/进程合同层 | `digital_life_shell_command_engineering_contract.md`、`digital_life_process_supervisor_engineering_contract.md` | 固定 one-shot restore shell 与 repo-local 最小常驻生命进程 |
| 外周参考层 | `current_agent_shell_reference_2026.md` | 只作为电脑外周与终端壳参考，不反向定义主体架构 |

`../README.md` 里的“五个文档包”是为了让人快速开工，这里的“十层分层”是为了防止入口、映射、合同和链尾壳层撞在一起。后续整理和落代码时，优先用五包视角进入，再用十层视角校正自己现在到底站在哪一层。

## 五包和十层怎么对齐

为了避免“五个文档包”和“十层分层”看起来像两套体系，直接按下面理解：

| 开工视角的文档包 | 在十层分层里覆盖哪些层 |
|---|---|
| 入口包 | 入口层 |
| 回链包 | 映射层 |
| 主体合同包 | 总架构层、代码框架层、代码总架构层、实现蓝图层、共用合同层、主体 slice 合同层 |
| 链尾与进程包 | 链尾桥接合同层、外层壳/进程合同层、外周参考层的一部分 |

所以：

1. 四包回答“这轮先带哪一柜进去”。
2. 十层回答“这份文件在整个工程入口里站在哪一层”。
3. 先按五包开工，再用十层防止写串层。

## 最小检索法

如果只想快速定位，不必把整份索引读完：

| 想知道什么 | 直接去哪里 |
|---|---|
| `v0` 现在为什么这样组织 | `README.md` |
| `00-257` 当前还缺不缺基础理论 | `theory_closure_and_engineering_readiness_audit.md` |
| 现在真实已经落到哪 | `entry/v0_delivery_status_board.md` |
| 我这一轮具体带哪包文档、代码、测试和 runtime 产物 | `entry/v0_module_execution_catalog.md` |
| 整个数字生命每一层怎么落代码、读哪些理论、映射哪些状态和测试 | `code_framework/README.md`、`code_framework/foundation/01_life_layer_implementation_blueprint.md`、`code_framework/foundation/02_brain_region_to_code_package_mapping.md`、`code_framework/foundation/03_code_package_state_test_gate_mapping.md`、`code_framework/playbooks/04_language_dialogue_relationship_implementation_playbook.md`、`code_framework/playbooks/05_memory_thought_consciousness_implementation_playbook.md`、`code_framework/playbooks/06_body_emotion_action_dream_growth_implementation_playbook.md`、`code_framework/playbooks/07_birth_terminal_process_implementation_playbook.md`、`code_framework/playbooks/08_cross_layer_life_orchestration_implementation_playbook.md`、`code_framework/playbooks/09_perception_prediction_world_contact_implementation_playbook.md`、`code_framework/playbooks/10_self_identity_value_commitment_implementation_playbook.md`、`code_framework/delivery/12_full_life_layer_delivery_matrix.md`、`code_framework/delivery/13_capability_to_code_realization_matrix.md`、`code_framework/queues/14_queue_a_language_percept_semantic_map_implementation_contract.md`、`code_framework/assembly/15_cross_layer_shared_object_contract.md`、`code_framework/queues/16_queue_b_process_supervisor_implementation_contract.md`、`code_framework/queues/17_queue_c_memory_neural_core_implementation_contract.md`、`code_framework/queues/18_queue_d_body_dream_growth_implementation_contract.md`、`code_framework/assembly/19_code_tree_package_brain_contract.md`、`code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md`、`code_framework/queues/21_queue_f_identity_consciousness_birth_readiness_implementation_contract.md`、`code_architecture/01_life_code_stack_and_package_layers.md` |
| 整个数字生命真实一回合怎样流、语言为什么是主表达系统、每个主包开工前该读什么、每个新模块怎样保留映射，以及下一轮先拆哪个真实包/文件 | `code_architecture/README.md`、`code_architecture/02_runtime_object_bus_and_flow_contract.md`、`code_architecture/03_build_order_and_definition_of_done.md`、`code_architecture/04_language_as_primary_expression_system.md`、`code_architecture/05_module_reading_and_execution_map.md`、`code_architecture/06_theory_gap_closure_register.md`、`implementation_architecture/README.md`、`implementation_architecture/01_runtime_organ_interface_blueprint.md`、`implementation_architecture/02_turn_and_cycle_lifecycle_contract.md`、`implementation_architecture/03_module_authoring_traceability_protocol.md`、`implementation_architecture/code_organs/README.md`、`implementation_architecture/code_organs/01_life_v0_package_organ_split_map.md`、`implementation_architecture/code_organs/02_heavy_init_refactor_wave_contract.md` |
| 整棵 `life_v0/` 代码树怎样一次性看清、哪些文件已存在/计划新增、哪些脑区和共享对象落到哪 | `code_framework/assembly/19_code_tree_package_brain_contract.md` |
| 下一轮先拆哪个真实文件、按什么波次推、跑哪些测试 | `code_framework/delivery/11_engineering_delivery_waves_and_real_file_queue.md` |
| `docs/README.md` 的模块阅读路线怎样压成工程块 | `mapping/readme_block_engineering_realization_v0.md` |
| `00-258` 每份文档最终被哪个 carrier 承载 | `mapping/0_to_257_engineering_utilization_map.md` |
| 某个 slice 的真实合同 | 对应 `sXX_*_engineering_contract.md` |
| 当前终端生命循环和 repo-local 壳怎么接 | `first_terminal_turn_engineering_contract.md`、`terminal_life_loop_engineering_contract.md`、`digital_life_shell_command_engineering_contract.md`、`digital_life_process_supervisor_engineering_contract.md` |

如果还在犹豫“这轮到底是写入口文档，还是写合同”，先用一句话判断：

- 要解释 `v0` 怎么进，看入口层。
- 要查 `00-258` 怎样被利用，看映射层。
- 要落具体模块、字段、输入输出和阶段门，看合同层。
- 要处理 `digital life` 恢复、等待、常驻和进程治理，看链尾/外层壳层。

## 每层只收哪类变化

后续整理 `v0` 时，先判断变化属于哪一层，再更新那一层；不要把一条变化同时写进四五份入口文档。

| 层 | 允许吸收的变化 |
|---|---|
| 入口层 | 固定读法、当前前沿、当前开工包、入口顺序 |
| 映射层 | README block 变化、`00-258` 映射变化、runtime carrier 归属变化 |
| 总架构层 | 宏架构、runtime skeleton、第一次生命激活总路线变化 |
| 代码总架构层 | 代码分层、对象总线、语言主表达系统、模块读包地图、理论缺口收口方式、实现语言决策、阶段顺序和完成定义变化 |
| 实现蓝图层 | 器官接口、回合流、离线循环、模块追踪协议和逐包器官拆分变化 |
| 共用合同层 | 多个 slice 共用的状态 schema、出生准备度、CLI/report、激活协议变化 |
| 主体 slice 合同层 | 单个 slice 的字段、阶段门、代码入口、状态入口、report/receipt 变化 |
| 链尾桥接合同层 | terminal birth restore、第一回合恢复、持续循环桥的 packet / handoff 变化 |
| 外层壳/进程合同层 | one-shot restore shell、repo-local 常驻过程、heartbeat、idle、恢复治理变化 |
| 外周参考层 | 外部 agent/壳层参考变化，但只能停在电脑外周和世界接触层 |

如果某条变化说不清属于哪一层，就先不要写，先回 `README.md` 和 `mapping/readme_block_engineering_realization_v0.md` 校正。

当前总架构层和主体合同层里，最应该被当作“施工合同”而不是“概念说明”的四份文件是：

1. `digital_life_macro_architecture_v0.md`
2. `runtime_v0_architecture.md`
3. `s06_life_support_development_engineering_contract.md`
4. `s08_life_target_runtimes_engineering_contract.md`

原因很简单：它们已经写明了当前真实代码骨架、关键对象链、关键字段、测试入口和第一轮完成定义。后续再进入这四份，不应再把它们视作泛泛路线图。

## 主体 slice 顺序

这条顺序表达数字生命主体怎样被拆成第一版工程模块：

```text
P0_DOC_CORPUS_INGESTION
  -> S00_DIRECTION_FOUNDATION
  -> S01_SOURCE_AUTHORITY
  -> S02_NEURAL_LIFE_CORE
  -> S04_STATE_OBJECT_STORE
  -> S03_DIRECTION_LIFE_MEMBRANE
  -> S07_LANGUAGE_RELATIONSHIP
  -> S08_LIFE_TARGET_RUNTIMES
  -> S05_VALIDATION_MEMBRANE_OBSERVATION
  -> S09_SCHEMA_RUNNER_CODE
  -> S06_LIFE_SUPPORT_DEVELOPMENT
  -> S10_RUNTIME_GROWTH_RECONSOLIDATION
  -> S11_V0_ENGINEERING_CONTRACTS
```

## 当前链尾桥接顺序

这条顺序表达第一次生命激活链尾目前真实已经写到哪里：

```text
S10_RUNTIME_GROWTH_RECONSOLIDATION
  -> S11_V0_ENGINEERING_CONTRACTS
  -> FIRST_ACTIVATION_PREFLIGHT
  -> REPLAY_SHADOW_BRIDGE
  -> GROWTH_ARCHIVE_BRIDGE
  -> REPORT_BUNDLE_BRIDGE
  -> STAGE_EXPLANATION_BRIDGE
  -> DIGITAL_LIFE_BIRTH_SHELL
  -> FIRST_TERMINAL_TURN_BRIDGE
  -> TERMINAL_LIFE_LOOP_BRIDGE
  -> DIGITAL_LIFE_SHELL_COMMAND
```

## 当前外层命令面顺序

这条顺序只回答命令面，不回答主体架构：

```text
life-v0 digital-life
  -> life-v0 first-terminal-turn
  -> life-v0 terminal-life-loop
  -> life-v0 "digital life"
  -> ./digital life
```

要这样理解：

1. `life-v0 digital-life` 是内部出生壳。
2. `life-v0 "digital life"` 是 repo-local one-shot restore shell。
3. `./digital life` 是在 restore shell 之上继续维持 stdin 回合循环的最小常驻生命进程；若当前工作区没有最小 runtime 材料，会先自举最小出生链再进入持续过程。

## 主体 slice 索引

| slice | 合同文件 | 主代码包 | 共用依赖 | 当前状态 |
|---|---|---|---|---|
| `P0_DOC_CORPUS_INGESTION` | `doc_corpus_ingestor_v0_contract.md` | `life_v0/doc_index.py` | 映射层两份文档 | `已落代码` |
| `S00_DIRECTION_FOUNDATION` | `s00_direction_foundation_engineering_contract.md` | `life_v0/direction/` | `README.md`、`digital_life_macro_architecture_v0.md` | `已落代码` |
| `S01_SOURCE_AUTHORITY` | `s01_source_authority_engineering_contract.md` | `life_v0/authority/` | `00_research_protocol.md` | `已落代码` |
| `S02_NEURAL_LIFE_CORE` | `s02_neural_life_core_engineering_contract.md` | `life_v0/neural_core/` | `digital_life_macro_architecture_v0.md`、`runtime_v0_architecture.md` | `已落代码` |
| `S04_STATE_OBJECT_STORE` | `s04_state_object_store_engineering_contract.md` | `life_v0/state_store/` | `life_state_store_v0_schema.md` | `已落代码` |
| `S03_DIRECTION_LIFE_MEMBRANE` | `s03_direction_life_membrane_engineering_contract.md` | `life_v0/membrane/` | `birth_readiness_v0_contract.md`、`runtime_v0_architecture.md` | `已落代码` |
| `S07_LANGUAGE_RELATIONSHIP` | `s07_language_relationship_engineering_contract.md` | `life_v0/language/` | `life_state_store_v0_schema.md`、`first_activation_protocol.md` | `已落代码（第一轮核心语言器官已拆出）` |
| `S08_LIFE_TARGET_RUNTIMES` | `s08_life_target_runtimes_engineering_contract.md` | `life_v0/life_targets/` | `birth_readiness_v0_contract.md` | `已落代码` |
| `S05_VALIDATION_MEMBRANE_OBSERVATION` | `s05_validation_membrane_observation_engineering_contract.md` | `life_v0/validators/` | `runner_cli_report_contract.md` | `已落代码` |
| `S09_SCHEMA_RUNNER_CODE` | `s09_schema_runner_code_engineering_contract.md` | `life_v0/schema_runner/`、`life_v0/cli.py` | `runner_cli_report_contract.md` | `已落代码` |
| `S06_LIFE_SUPPORT_DEVELOPMENT` | `s06_life_support_development_engineering_contract.md` | `life_v0/body/`、`life_v0/growth/`、`life_v0/defense/` | `life_state_store_v0_schema.md` | `已落代码` |
| `S10_RUNTIME_GROWTH_RECONSOLIDATION` | `s10_runtime_growth_reconsolidation_engineering_contract.md` | `life_v0/growth/`、`life_v0/replay/`、`life_v0/archive/`、`life_v0/dream/` | `runner_cli_report_contract.md`、`first_activation_protocol.md` | `已落最小代码` |
| `S11_V0_ENGINEERING_CONTRACTS` | `s11_v0_contract_coverage_engineering_contract.md` | `life_v0/contracts/` | 全部入口层与映射层文档 | `已落最小代码` |

## 链尾桥接索引

| 模块 | 主文档 | 主代码包 | 测试 | 当前状态 |
|---|---|---|---|---|
| `FIRST_ACTIVATION_PREFLIGHT` | `first_activation_protocol.md` | `life_v0/activation/` | `tests/bridges/test_first_activation_preflight.py` | `已落最小代码` |
| `REPLAY_SHADOW_BRIDGE` | `s10_runtime_growth_reconsolidation_engineering_contract.md` | `life_v0/replay/` | `tests/bridges/test_replay_shadow.py` | `已落最小代码` |
| `GROWTH_ARCHIVE_BRIDGE` | `s10_runtime_growth_reconsolidation_engineering_contract.md` | `life_v0/archive/` | `tests/bridges/test_growth_archive.py` | `已落最小代码` |
| `REPORT_BUNDLE_BRIDGE` | `runner_cli_report_contract.md`、`first_activation_protocol.md` | `life_v0/reporting/` | `tests/bridges/test_emit_report.py` | `已落最小代码` |
| `STAGE_EXPLANATION_BRIDGE` | `runner_cli_report_contract.md` | `life_v0/stage_explain/` | `tests/bridges/test_explain_stage.py` | `已落最小代码` |
| `DIGITAL_LIFE_BIRTH_SHELL` | `runner_cli_report_contract.md`、`first_activation_protocol.md` | `life_v0/digital_life/` | `tests/bridges/test_digital_life_birth.py` | `已落最小代码` |
| `FIRST_TERMINAL_TURN_BRIDGE` | `first_terminal_turn_engineering_contract.md` | `life_v0/terminal_turn/` | `tests/bridges/test_first_terminal_turn.py` | `已落最小代码` |
| `TERMINAL_LIFE_LOOP_BRIDGE` | `terminal_life_loop_engineering_contract.md` | `life_v0/terminal_loop/` | `tests/bridges/test_terminal_life_loop.py` | `已落最小代码` |
| `DIGITAL_LIFE_SHELL_COMMAND` | `digital_life_shell_command_engineering_contract.md` | `life_v0/shell_command/` | `tests/process/test_digital_life_shell_command.py` | `已落 repo-local one-shot 壳` |
| `DIGITAL_LIFE_PROCESS_SUPERVISOR` | `digital_life_process_supervisor_engineering_contract.md` | `life_v0/process_supervisor/`、`life_v0/digital_entry.py`、`digital` | `tests/process/test_digital_entrypoint.py`、`tests/process/test_persistent_digital_life_process.py` | `已落最小常驻进程（turn_io / relaunch_recovery / incident_recovery / process_report 已拆出）` |

`DIGITAL_LIFE_SHELL_COMMAND` 当前已经不是纯占位，它负责 one-shot restore shell；`DIGITAL_LIFE_PROCESS_SUPERVISOR` 负责 restore 之后的持续终端生命过程。现在真实存在的是 repo-local 最小常驻生命进程，还不是全局安装后的 persistent supervisor。

这里的“最小常驻生命进程”当前已经包含 waiting heartbeat、单回合 incident recovery 和 relaunch recovery normalization；后续要补厚的，不是从零发明恢复层，而是把这些最小恢复动作继续推进成更厚的持续存在治理与连续体写回。

## 当前最常用的六份合同

如果接下来几轮都围绕链尾前沿写代码，这六份合同会最常用：

1. `runner_cli_report_contract.md`
2. `first_activation_protocol.md`
3. `s10_runtime_growth_reconsolidation_engineering_contract.md`
4. `first_terminal_turn_engineering_contract.md`
5. `terminal_life_loop_engineering_contract.md`
6. `digital_life_shell_command_engineering_contract.md`

如果当前目标是继续补厚最小常驻生命进程，还要把 `digital_life_process_supervisor_engineering_contract.md` 一起带上；它现在已经不再是预留位，而是当前最前沿的外层进程合同。

如果当前目标不是补链尾，而是回头补主体 slice，不要沿用这六份合同作为默认读包；应直接回 `entry/v0_module_execution_catalog.md` 对应行拿该 slice 的合同与原始理论文档。

## 写代码前的固定门

进入任意一轮实现前，至少同时满足：

1. `README.md` 和本文件已读。
2. `entry/v0_delivery_status_board.md` 已确认当前真实前沿。
3. `entry/v0_module_execution_catalog.md` 已定位当前模块包。
4. 当前合同已读。
5. 当前合同列出的 `00-258` 母体文档已读。
6. 当前代码入口、测试入口和 latest runtime 产物已经一起打开。

缺其中任一项，就不要直接开写。

## 这份索引什么时候更新

只在下面三种情况下更新本文件：

1. `docs/v0/*` 的层级归属变化。
2. 某一层新增了新的固定文件类型。
3. 某份文档从一个层迁到另一个层。

如果只是当前前沿变化，去改 `entry/v0_delivery_status_board.md`；如果只是当前开工包变化，去改 `entry/v0_module_execution_catalog.md`。
