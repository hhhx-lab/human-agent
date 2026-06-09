# V0 实现蓝图柜

`implementation_architecture/` 是写代码前的硬蓝图柜。

`code_framework/` 已经回答了“要建哪些层、哪些包、哪些文件、哪些 Queue”；这一柜只回答另外三件事：

1. 真实一回合怎样在器官之间流动。
2. 每个器官的接口、输入输出和共享对象怎样被钉死。
3. 后续每一个新代码模块怎样保持 `00-258 -> v0 合同 -> code -> runtime -> test` 一一映射。

它不重写 `code_framework/`，也不替代 `slice_contracts/`。它是 `code_framework` 和真正代码实现之间的压缩层。

## 什么时候打开

- 准备给 `life_v0/` 新增真实文件时。
- 准备把一个过重的 `__init__.py` 拆成多个器官文件时。
- 准备把某条生命能力从“有理论、有合同”推进到“有真实回合流和真实 runtime 证据”时。

## 这柜文件分工

| 文件 | 只回答什么 |
|---|---|
| `README.md` | 这柜为什么存在、什么时候打开、和 `code_framework/` 的关系 |
| `01_runtime_organ_interface_blueprint.md` | 每个生命器官组的接口、共享对象、runtime 产物、测试与落码顺序 |
| `02_turn_and_cycle_lifecycle_contract.md` | 单次外部回合、离线梦境/成长循环、常驻等待态怎样逐阶段流动 |
| `03_module_authoring_traceability_protocol.md` | 后续每个新模块怎样写、怎样测、怎样回链文档和运行证据 |

## 使用顺序

进入这一柜时，先按下面顺序读：

1. `docs/v0/README.md`
2. `docs/v0/entry/v0_implementation_index.md`
3. `docs/v0/entry/v0_delivery_status_board.md`
4. `docs/v0/code_framework/README.md`
5. `docs/v0/code_framework/19_code_tree_package_brain_contract.md`
6. 本柜 `01 -> 03`

如果读完这一柜仍然无法回答“这次新增文件到底首写哪个共享对象、写出哪份 state/report/receipt、由哪个测试守住”，就不要开写代码。
