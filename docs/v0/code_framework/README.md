# V0 Code Framework Cabinet

`docs/v0/code_framework/` 是 v0 工程文档里的代码框架柜。它只做一件事：把 `00-258` 和 `docs/v0/*.md` 已经写定的生命结构，压成后续 `life_v0/` 真实落码时可直接执行的代码框架。

这里不重写总体理论，不代替 slice 合同，也不替代 `docs/v0/README.md`。它服务的是一个更具体的问题：

1. 当前数字生命代码应该按哪些层来展开。
2. 每一层优先挂到哪些现有 `life_v0/` 包。
3. 每个包要承载哪些状态、report、receipt、测试和 gate。
4. 后续工程回合怎样保证 `00-258 -> v0 合同 -> 代码包 -> runtime 产物` 不断链。

如果读完这柜之后，下一步已经是“真的要写代码，而不是继续补矩阵”，就接着进入：

- `docs/v0/implementation_architecture/README.md`
- `docs/v0/implementation_architecture/01_runtime_organ_interface_blueprint.md`
- `docs/v0/implementation_architecture/02_turn_and_cycle_lifecycle_contract.md`
- `docs/v0/implementation_architecture/03_module_authoring_traceability_protocol.md`

也就是说，`code_framework/` 解决“要建什么”，`implementation_architecture/` 解决“真实一回合怎么流、每个器官怎么接、每个模块怎么留痕”。

## 这柜文档怎么读

如果这一轮不是补某个单独 slice，而是补“整个代码框架应该怎么搭”，先按下面顺序读：

1. `docs/v0/README.md`
2. `docs/v0/entry/v0_implementation_index.md`
3. `docs/v0/entry/v0_delivery_status_board.md`
4. `docs/v0/entry/v0_module_execution_catalog.md`
5. 本文件
6. `foundation/README.md`
7. `playbooks/README.md`
8. `delivery/README.md`
9. `queues/README.md`
10. `assembly/README.md`

如果要完整扫一遍代码框架柜，顺序固定为：

```text
foundation/
  -> playbooks/
  -> delivery/
  -> queues/
  -> assembly/
  -> docs/v0/implementation_architecture/
```

如果这一轮已经明确只落某个模块，仍然要先过一遍本柜，再回对应 `sXX_*` 或链尾合同。

## 本柜子目录

| 子柜 | 文件 | 只回答什么 |
|---|---|---|
| `foundation/` | `01-03` | 生命层、脑区/网络到代码包、state/report/receipt/test/gate 的底层映射 |
| `playbooks/` | `04-10` | 语言、记忆、梦境、成长、关系、行动、意识等跨层能力怎样逐文件落代码 |
| `delivery/` | `11-13` | 开发波次、生命层总施工矩阵、能力到代码验收矩阵 |
| `queues/` | `14`、`16-18`、`20-21` | Queue A-F 的文件级实施合同 |
| `assembly/` | `15`、`19` | 跨层共享对象和整棵 `life_v0/` 代码树总装配 |

## 本柜文档各自负责什么

| 文件 | 只回答什么 |
|---|---|
| `README.md` | 代码框架柜为什么存在、怎么进、和 v0 其余文档是什么关系 |
| `foundation/01_life_layer_implementation_blueprint.md` | 整个数字生命按哪些生命层落代码、每层优先读哪些理论和合同 |
| `foundation/02_brain_region_to_code_package_mapping.md` | 脑区/网络/主体系统怎样映射到当前 `life_v0/` 包与后续文件拆分 |
| `foundation/03_code_package_state_test_gate_mapping.md` | 每个代码包该承载哪些状态对象、report、receipt、测试和阶段门 |
| `playbooks/04_language_dialogue_relationship_implementation_playbook.md` | 语言、对话、关系、等待态连续体怎样逐文件落代码 |
| `playbooks/05_memory_thought_consciousness_implementation_playbook.md` | 思考、逻辑、记忆、意识怎样逐文件落代码 |
| `playbooks/06_body_emotion_action_dream_growth_implementation_playbook.md` | 身体、情绪、行动、梦境、成长、学习怎样逐文件落代码 |
| `playbooks/07_birth_terminal_process_implementation_playbook.md` | 出生、终端循环、壳层、常驻生命进程怎样逐文件落代码 |
| `playbooks/08_cross_layer_life_orchestration_implementation_playbook.md` | 身体、信号、思考、语言、关系、梦境、成长和常驻过程怎样在同一生命回合里接棒 |
| `playbooks/09_perception_prediction_world_contact_implementation_playbook.md` | 外界观察、预测工作区、世界接触、行动意图和 observation 正规化怎样逐文件落代码 |
| `playbooks/10_self_identity_value_commitment_implementation_playbook.md` | 身份、自我、价值、承诺、后悔、责任和自我改写保护怎样逐文件落代码 |
| `delivery/11_engineering_delivery_waves_and_real_file_queue.md` | 接下来每一轮先拆哪些真实文件、按什么波次落、回读哪些理论和跑哪些测试 |
| `delivery/12_full_life_layer_delivery_matrix.md` | 把全部生命层压成总施工矩阵，直接决定这一轮该改哪层、哪包、哪文件 |
| `delivery/13_capability_to_code_realization_matrix.md` | 把生命能力直接压成代码文件、state、测试和 gate 的验收矩阵，回答“某种能力到底有没有真正开始落地” |
| `queues/14_queue_a_language_percept_semantic_map_implementation_contract.md` | 把 Queue A 的 `percept.py` / `semantic_map.py` 压成文件级实施合同，固定输入输出、状态、测试和下游接线 |
| `assembly/15_cross_layer_shared_object_contract.md` | 把跨层共享对象压成唯一首写方、字段组、state/report/receipt 和 gate 的硬合同，防止生命回合重新退回临时字典拼接 |
| `queues/16_queue_b_process_supervisor_implementation_contract.md` | 把 Queue B 的 process supervisor / waiting heartbeat / dialogue event / process report 压成文件级实施合同，固定常驻生命进程的对象链与测试面 |
| `queues/17_queue_c_memory_neural_core_implementation_contract.md` | 把 Queue C 的 state store / engram / workspace / brain graph 压成文件级实施合同，固定记忆根、工作区与主体图的落码顺序 |
| `queues/18_queue_d_body_dream_growth_implementation_contract.md` | 把 Queue D 的 body / dream / growth 器官压成文件级实施合同，固定身体节律、梦境窗口与成长补丁链的落码顺序 |
| `assembly/19_code_tree_package_brain_contract.md` | 把整棵 `life_v0/` 代码树、脑区到包、共享对象、runtime 产物、测试和整体施工顺序钉成一张总装配板，作为正式大规模落码前的总合同 |
| `queues/20_queue_e_membrane_validator_logic_implementation_contract.md` | 把 Queue E 的 membrane / validators / schema_runner 压成文件级实施合同，固定候选行动、world contact、side effect、观察真值和反事实比较的落码顺序 |
| `queues/21_queue_f_identity_consciousness_birth_readiness_implementation_contract.md` | 把 Queue F 的 direction / consciousness / birth readiness 压成文件级实施合同，固定身份连续体、意识广播、元认知和九项目标上卷的落码顺序 |

## 本柜和其他 v0 文档的关系

这柜文档不单独形成体系，它只是把其他文档压得更可施工：

| 上游 | 这里接什么 |
|---|---|
| `docs/00-258` | 理论母体、脑区/网络/语言/梦境/关系/生命目标的原始约束 |
| `docs/v0/architecture/digital_life_macro_architecture_v0.md` | 主体宏架构、十二主体系统、运行时主通路 |
| `docs/v0/architecture/runtime_v0_architecture.md` | runtime 根目录、state/report/receipt 的真实承载面 |
| `docs/v0/s00_*` 到 `s11_*`、链尾合同 | 每个 slice、bridge、shell、process 的字段、输入输出和 gate |

| 下游 | 这里如何落 |
|---|---|
| `life_v0/*` | 确定先落到哪个顶层包，再细分文件 |
| `tests/*` | 约束每个包至少有一个真实测试入口 |
| `runtime/state/*` | 约束状态对象必须真实落盘 |
| `runtime/reports/latest/*` | 约束 report 必须能成为出生准备度和持续过程证据 |
| `runtime/receipts/*` | 约束 receipt 必须能被 archive/replay/recovery 回链 |

## 当前使用边界

当前代码框架柜有三个硬规则：

1. 不重命名当前已经存在的 `life_v0/` 顶层包，先在包内细分文件。
2. 不让外部 agent 框架反向定义主体器官，只把它们限制在外周、壳层或过程治理层。
3. 不允许只写代码结构而不写 runtime 承载；任何一层都必须同时给出状态、report、receipt 和测试/gate。

## 进入代码前的固定检查

开始任意一个工程回合前，至少同时确认：

1. 当前要改的是哪一层生命结构。
2. 当前层回读了哪些 `00-258` 原文。
3. 当前层落到哪些 `life_v0/` 包。
4. 当前层要新增或细分哪些文件。
5. 当前层写完后会产出哪些 state、report、receipt。
6. 当前层由哪些测试和 gate 验收。

六条缺一条，不开写。
