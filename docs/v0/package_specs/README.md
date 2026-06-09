# Package Specs

`docs/v0/package_specs/` 是第一版数字生命的逐包施工柜。

它不替代：

- `code_framework/` 的总体波次与 Queue 合同
- `code_architecture/` 的分层与对象总线
- `implementation_architecture/` 的器官接口和重型入口拆分图

它只负责把这些总图压到真正能写 `life_v0/*` 代码的包级规格：

1. 每个包要回读哪些 `00-258` 理论文档。
2. 每个包必须首写或消费哪些共享对象。
3. 每个包必须写出哪些 `runtime/state/*`、`runtime/reports/latest/*`、`runtime/receipts/*`。
4. 每个包最小该有哪些文件、测试和 gate。
5. 每轮新增代码时，怎样保留 theory -> package -> runtime -> test 的回链。

## 什么时候先开这柜

下面三种场景，先开 `package_specs/`：

1. 当前不是改单个 bug，而是要继续铺整棵 `life_v0/` 包树。
2. 已经知道要改哪一层，但还没决定具体落到哪个包、哪个文件、哪个共享对象。
3. 断联恢复后，需要快速判断“这个功能应该归 body / neural_core / language / membrane / dream / growth / process_supervisor 的哪一包”。

## 这柜和其他柜的关系

| 柜位 | 只回答什么 |
|---|---|
| `code_framework/` | 生命层、开发波次、Queue、能力矩阵 |
| `code_architecture/` | 整棵代码树分层、对象总线、语言主表达系统 |
| `package_specs/` | 具体到每个 `life_v0/*` 包该怎么写、读什么、写什么、怎么验收 |
| `implementation_architecture/` | 器官接口、回合流、逐包重构波次 |
| `engineering_depth/` | 复杂生命层的深描、runtime 证据与 tests 回链 |

## 当前文件

1. `01_life_v0_package_construction_matrix.md`
   - 按包列出脑科学锚点、主对象、runtime、测试、下一步文件。
2. `02_shared_object_write_authority_and_dependency_graph.md`
   - 固定共享对象的唯一首写权、可追加边界、只读消费者和依赖图。
3. `03_incremental_package_delivery_protocol.md`
   - 固定每一包从读理论、定对象、落文件、写 runtime 到补测试的施工协议。

## 使用顺序

如果这一轮要继续补整个代码框架，推荐顺序固定为：

```text
docs/v0/README.md
  -> docs/v0/entry/v0_implementation_index.md
  -> docs/v0/entry/v0_delivery_status_board.md
  -> docs/v0/entry/v0_module_execution_catalog.md
  -> docs/v0/architecture/theory_closure_and_engineering_readiness_audit.md
  -> docs/v0/code_architecture/01_life_code_stack_and_package_layers.md
  -> docs/v0/code_architecture/02_runtime_object_bus_and_flow_contract.md
  -> docs/v0/package_specs/README.md
  -> docs/v0/package_specs/01_life_v0_package_construction_matrix.md
  -> docs/v0/package_specs/02_shared_object_write_authority_and_dependency_graph.md
  -> docs/v0/package_specs/03_incremental_package_delivery_protocol.md
```

然后再回当前正在实现的 `sXX` 合同、Queue 合同和具体代码入口。
