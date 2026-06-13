# V0 Entry Cabinet

`docs/v0/entry/` 只放四类东西：

1. 总索引：`v0_implementation_index.md`
2. 当前前沿：`v0_delivery_status_board.md`
3. 本轮开工包：`v0_module_execution_catalog.md`
4. 当前版本迭代计划：`v0_current_iteration_plan.md`

另外有一份“当前理论到 runtime 覆盖快照”：

5. `v0_theory_to_runtime_coverage_snapshot_2026-06-10.md`

进入 `docs/v0/` 后，如果你现在的目标是“先搞清楚从哪里开工”，就先读这一柜，不要先扎进 `slice_contracts/` 或 `code_framework/`。

## 建议顺序

1. `v0_implementation_index.md`
2. `v0_delivery_status_board.md`
3. `v0_module_execution_catalog.md`
4. `v0_current_iteration_plan.md`
5. `v0_theory_to_runtime_coverage_snapshot_2026-06-10.md`（当你需要快速判断“现在缺的是理论还是工程对象化”时）

这四份的分工固定如下：

| 文件 | 作用 |
|---|---|
| `v0_implementation_index.md` | 把整个 `docs/v0/*` 的层级与职责分开 |
| `v0_delivery_status_board.md` | 只回答“现在已经到哪、最该补哪” |
| `v0_module_execution_catalog.md` | 只回答“这一轮带哪包文档、代码、测试和 runtime 产物开工” |
| `v0_current_iteration_plan.md` | 只回答“现有版本接下来按什么顺序把代码块补得更完整” |

如果当前问题不是“怎么进”，而是“这一批理论最后落到哪个 slice 和 runtime carrier”，转去 `../mapping/README.md`。

## 当前入口栈

进入 v0 后，实际开工入口不是单个 README，而是一组必须并读的入口栈。这里保留原有入口栈口径，不把当前版本计划直接塞进入口栈本体：

1. `v0_implementation_index.md`
2. `v0_delivery_status_board.md`
3. `v0_module_execution_catalog.md`
4. `../mapping/theory_engineering_code_trace_matrix.md`
5. `../../real—live0/00_reading_map_and_traceability.md`
6. `../../real—live0/16_runtime_code_chain_crosswalk.md`
7. `v0_theory_to_runtime_coverage_snapshot_2026-06-10.md`

这七份一起回答：理论是否全被利用、当前工程前沿在哪、哪个模块先开工、它读哪些机制专题、落到哪些代码包、产生哪些 runtime 证据、用哪些测试/gate 验收。

入口栈之后，如果当前目标是“按现有版本继续补厚代码块”，再追加这两份：

```text
v0_current_iteration_plan.md
  -> ../../real—live0/17_current_iteration_mechanism_to_code_plan.md
```

这两份不改变固定入口栈，只把入口栈导出的模块包排成当前版本的实际迭代路线。

如果只读 v0 入口而不读 `real—live0`，容易把工程变成普通 agent 壳；如果只读 `real—live0` 而不读 v0 入口，容易停在机制说明，无法进入代码队列。
