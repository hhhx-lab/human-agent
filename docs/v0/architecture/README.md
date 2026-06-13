# V0 架构柜

`architecture/` 只放跨多个 slice 的总架构文件，不放单个模块合同。

## 先看什么

1. `digital_life_macro_architecture_v0.md`：整套数字生命 v0 的宏观分层。
2. `runtime_v0_architecture.md`：运行时状态、report、receipt、gate 的骨架。
3. `first_activation_engineering_roadmap.md`：第一次生命激活从文档到运行证据的路线。
4. `theory_closure_and_engineering_readiness_audit.md`：判断当前缺的是理论闭合，还是工程物化。

## 什么时候打开

- 需要改动跨层结构、runtime 总线、state/report/receipt 骨架时。
- 需要确认当前前沿还能不能继续落代码时。
- 需要把 `docs/00-258` 的理论闭合重新压回工程入口时。

## 工程覆盖口径

这一柜不是概念总览。任何跨层架构结论都必须同时回链：

| 层 | 必须读到 | 工程含义 |
|---|---|---|
| 理论母体 | `docs/00-258` 与 `docs/v0/mapping/theory_engineering_code_trace_matrix.md` | 确认理论族没有被漏用 |
| 机制档案 | `docs/real—live0/00_reading_map_and_traceability.md`、`16_runtime_code_chain_crosswalk.md` | 把脑科学机制压成对象、字段、消费链 |
| 代码落点 | `life_v0/neural_core`、`state_store`、`body`、`language`、`dream`、`growth`、`membrane`、`process_supervisor` 等主包 | 确认架构不是空图，而是代码器官协作 |
| runtime 证据 | `runtime/state`、`runtime/reports/latest`、`runtime/receipts` | 架构必须能生成状态、报告和回执 |
| 验收门 | `tests/slices`、`tests/bridges`、`tests/process`、`tests/contracts` | 架构变化必须有 gate 发现断链 |

如果一条架构规则说不出首写对象、共享字段、下游消费和断链测试，就不要写进这里；先回到 `code_architecture/02_runtime_object_bus_and_flow_contract.md` 或具体 slice 合同补硬。

## 不要在这里做什么

- 不要把单个 slice 的字段变化写到这里。
- 不要把 Queue 级别的文件拆分计划写到这里，那些属于 `code_framework/`。
- 不要把整棵代码树的分层、对象总线、阶段顺序和完成定义写到这里，那些属于 `code_architecture/`。
- 不要把 shell 或常驻进程细节写到这里，那些属于 `process_contracts/`。
