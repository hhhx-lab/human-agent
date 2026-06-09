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

## 不要在这里做什么

- 不要把单个 slice 的字段变化写到这里。
- 不要把 Queue 级别的文件拆分计划写到这里，那些属于 `code_framework/`。
- 不要把整棵代码树的分层、对象总线、阶段顺序和完成定义写到这里，那些属于 `code_architecture/`。
- 不要把 shell 或常驻进程细节写到这里，那些属于 `process_contracts/`。
