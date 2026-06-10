# V0 代码器官装配柜

`implementation_architecture/code_organs/` 只做一件事：把 `life_v0/` 已经存在的顶层包，继续压成“逐包可拆、逐文件可落、逐测试可守”的代码器官装配图。

前面的 `code_framework/` 已经回答了：

1. 数字生命按哪些生命层施工。
2. 哪些脑区/网络先映射到哪些顶层包。
3. 哪些 Queue 先做、哪些共享对象先钉死。

这一柜只补最后一步：

1. 当前每个顶层包里已经有哪些真实器官文件。
2. 还剩哪些重型 `__init__.py` 没拆干净。
3. 下一轮到底该先从哪个包、哪个文件、哪条测试链下手。
4. 每次拆分之后要写回哪些 `runtime/state/*`、`runtime/reports/latest/*`、`runtime/receipts/*`。

## 什么时候打开

- 准备继续拆 `life_v0/*/__init__.py`。
- 准备把某个 Queue 从“文档已定”推进到“逐文件实现”。
- 准备确认某个顶层包后续还应该长哪些器官文件，而不是继续把逻辑堆在入口文件里。

## 柜内文件

| 文件 | 作用 |
|---|---|
| `README.md` | 说明这一柜为什么存在、什么时候打开 |
| `01_life_v0_package_organ_split_map.md` | 整棵 `life_v0/` 的逐包器官拆分总图，固定每个包的理论回链、现状、目标文件、runtime 产物和测试面 |
| `02_heavy_init_refactor_wave_contract.md` | 把当前仍然过重的 `__init__.py` 按 Queue 波次压成拆分合同，固定每一波先拆谁、怎么拆、跑哪些测试 |
| `03_predictive_signal_memory_gate_integration_wave_contract.md` | 固定已落 `signal_media / belief_state / prediction_error / active_sampling / memory_write_gate` 的跨层深消费波次 |

## 使用顺序

进入这一柜时，固定顺序是：

1. `docs/v0/README.md`
2. `docs/v0/entry/v0_delivery_status_board.md`
3. `docs/v0/entry/v0_module_execution_catalog.md`
4. `docs/v0/code_framework/assembly/19_code_tree_package_brain_contract.md`
5. `docs/v0/implementation_architecture/01_runtime_organ_interface_blueprint.md`
6. 本柜 `01 -> 03`

如果读完这里仍然回答不出“这个包下一轮先拆哪个真实文件、要写哪份 state/report/receipt、跑哪组测试”，就不要开写代码。
