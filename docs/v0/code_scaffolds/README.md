# V0 代码脚手柜

`docs/v0/code_scaffolds/` 是 v0 里的代码脚手柜。

它不是新的理论层，也不替代：

- `code_framework/` 的生命层与 Queue 合同
- `code_blueprints/` 的总装配蓝图
- `package_specs/` 的逐包施工规格
- `implementation_architecture/` 的器官接口与回合流

它只做最后一件事：

```text
把“已经足够厚的蓝图与合同”
继续压成
真正可以直接去写文件的代码脚手架。
```

## 这柜为什么现在必须存在

当前 `docs/v0/` 已经不缺工程材料。

现在真正缺的是：

1. 一个专门说明“代码树下一步具体怎么长”的柜位。
2. 一个专门固定“在线回合 / 离线回合 / 常驻过程”代码装配骨架的柜位。
3. 一个专门把当前前沿模块压成逐包施工包的柜位。

也就是说，当前问题已经不是“还不知道要做什么”，而是“怎么把知道的东西稳定地写成文件，而不散掉”。

## 这柜和其他柜的关系

| 柜位 | 原职责 | 这柜怎么使用它 |
|---|---|---|
| `code_blueprints/` | 给出整个系统总装配蓝图 | 抽取系统级主包、主对象、主流程 |
| `package_specs/` | 给出逐包施工矩阵 | 抽取每个包的最低文件骨架、runtime 和测试面 |
| `implementation_architecture/` | 给出器官接口、回合流和重型入口拆分位 | 抽取在线 / 离线 / waiting 的真实代码装配顺序 |
| `engineering_depth/` | 给出复杂生命层的深描 | 抽取当前前沿模块真正需要消费的对象链 |

所以这柜不是替代它们，而是把它们从“解释工程”继续压到“脚手施工”。

## 柜内文件

| 文件 | 只回答什么 |
|---|---|
| `README.md` | 这柜为什么存在、和其他柜是什么关系、怎么进入 |
| `01_life_code_scaffold_tree.md` | `life_v0/`、`runtime/`、`tests/` 的代码脚手树该怎样稳定生长 |
| `02_cognitive_loop_code_scaffold.md` | 在线回合、离线回合、常驻等待态在代码层如何真实装配 |
| `03_frontier_module_build_packets.md` | 当前前沿模块下一步到底读什么、改什么、写什么、跑什么 |
| `04_packet_b_world_observation_periphery_scaffold.md` | Packet B 这一轮怎样把世界观察与外周归一化真正落进 S03/S05 |

## 使用顺序

进入这柜前，先固定读：

1. `docs/v0/README.md`
2. `docs/v0/entry/v0_implementation_index.md`
3. `docs/v0/entry/v0_delivery_status_board.md`
4. `docs/v0/entry/v0_module_execution_catalog.md`
5. `docs/v0/code_blueprints/01_full_system_code_blueprint.md`
6. `docs/v0/package_specs/01_life_v0_package_construction_matrix.md`
7. `docs/v0/implementation_architecture/01_runtime_organ_interface_blueprint.md`
8. `docs/v0/implementation_architecture/02_turn_and_cycle_lifecycle_contract.md`

然后按下面顺序进入本柜：

1. `01_life_code_scaffold_tree.md`
2. `02_cognitive_loop_code_scaffold.md`
3. `03_frontier_module_build_packets.md`
4. `04_packet_b_world_observation_periphery_scaffold.md`

## 这柜的硬约束

1. 不允许把数字生命重新写回 tool router、skill shell 或 workflow gateway。
2. 不允许把外部对象写成 `user` 核心抽象，只允许关系对象、外部回合对象、共同语言对象这类关系位。
3. 不只写文件名，必须同时写明入口函数、runtime 产物、测试和 gate。
4. 每个脚手页都必须能回读 `00-257` 与已有 `v0` 合同，不允许断掉理论到代码的映射。
