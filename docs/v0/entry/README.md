# V0 Entry Cabinet

`docs/v0/entry/` 只放三类东西：

1. 总索引：`v0_implementation_index.md`
2. 当前前沿：`v0_delivery_status_board.md`
3. 本轮开工包：`v0_module_execution_catalog.md`

另外有一份“当前理论到 runtime 覆盖快照”：

4. `v0_theory_to_runtime_coverage_snapshot_2026-06-10.md`

进入 `docs/v0/` 后，如果你现在的目标是“先搞清楚从哪里开工”，就先读这一柜，不要先扎进 `slice_contracts/` 或 `code_framework/`。

## 建议顺序

1. `v0_implementation_index.md`
2. `v0_delivery_status_board.md`
3. `v0_module_execution_catalog.md`
4. `v0_theory_to_runtime_coverage_snapshot_2026-06-10.md`（当你需要快速判断“现在缺的是理论还是工程对象化”时）

这三份的分工固定如下：

| 文件 | 作用 |
|---|---|
| `v0_implementation_index.md` | 把整个 `docs/v0/*` 的层级与职责分开 |
| `v0_delivery_status_board.md` | 只回答“现在已经到哪、最该补哪” |
| `v0_module_execution_catalog.md` | 只回答“这一轮带哪包文档、代码、测试和 runtime 产物开工” |

如果当前问题不是“怎么进”，而是“这一批理论最后落到哪个 slice 和 runtime carrier”，转去 `../mapping/README.md`。
