# V0 Mapping Cabinet

`docs/v0/mapping/` 只处理两件事：

1. `docs/README.md` 的模块分块怎样压成 engineering slice。
2. `00-258` 的理论母体怎样进入 runtime carrier、state、report、receipt 和 archive。

这一柜不回答“现在最该先写哪个模块”，那是 `../entry/` 的工作；它只回答“理论到底怎样被工程承载”。

## 柜内文档

| 文件 | 作用 |
|---|---|
| `readme_block_engineering_realization_v0.md` | 把 README block 压成 engineering slice 与最小工程承载关系 |
| `0_to_257_engineering_utilization_map.md` | 把 `00-258` 文档压进 runtime carrier 与运行证据链 |
| `theory_engineering_code_trace_matrix.md` | 把根目录理论文档族逐一映射到 v0 工程文档、`life_v0` 代码包、runtime 证据和测试 gate，用于代码生成前的全覆盖校验 |

## 什么时候先开这柜

- 你要检查 `00-258` 是否真的被用起来了
- 你要确认当前 slice 背后的理论母体
- 你要补文档回链、runtime carrier 回链或断联恢复锚链
- 你要知道某组理论文档应读哪份工程文档、落哪个代码包、由哪个 gate 验收

如果当前已经确定要写哪个模块，回 `../entry/v0_module_execution_catalog.md` 拿本轮材料包。
