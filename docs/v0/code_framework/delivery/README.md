# Code Framework Delivery

这一柜只放交付矩阵和开发波次，负责把生命层、能力层和真实文件队列压成可执行顺序。

| 文件 | 作用 |
|---|---|
| `11_engineering_delivery_waves_and_real_file_queue.md` | 后续每轮先拆哪些真实文件，按什么波次推进 |
| `12_full_life_layer_delivery_matrix.md` | 全部生命层到代码、状态、测试和 gate 的总施工矩阵 |
| `13_capability_to_code_realization_matrix.md` | 每种生命能力是否真正落进代码、状态和证据 |
| `22_live0_acceptance_audit_contract.md` | 把 Stage 6 七项最终验收压成 `life-v0 audit-live0` 可执行收束 gate |

这一柜适合开工前判断优先级，也适合收尾时做覆盖审计。

如果已经知道优先级，但还需要进一步钉死“这棵代码树怎么分层、共享对象怎么流、阶段完成定义是什么”，继续转去 `docs/v0/code_architecture/`。

## 交付波次验收口径

每个 delivery wave 必须同时交付四类东西：

| 类别 | 必须包含 |
|---|---|
| 理论和机制 | 对应 `docs/00-258` 文档族、`docs/real—live0` 专题、trace matrix 行 |
| 代码对象 | `life_v0` 首写函数、消费函数、共享字段、写入权限 |
| runtime 证据 | `runtime/state`、`runtime/reports/latest`、`runtime/receipts` |
| 验收门 | slice/bridge/process/contract tests，或对应 `life-v0 ... --strict` gate |

delivery 的优先级不按“哪个功能像 agent 能力”排序，而按生命链断点排序：先补会阻断语言、记忆、情绪、梦境、责任、常驻或出生准备闭合的断点。

## 与 real-live0 的关系

`delivery/` 决定交付顺序，`docs/real—live0` 决定生命机制怎样才算落地。比如交付 Queue D 不能只实现 `body`、`dream`、`growth` 文件，还要符合 `03_body_affect_homeostasis.md` 的情绪 episode、`08_dream_sleep_offline_life.md` 的梦境事实门和 resident 离线时序、`13_growth_learning_self_modification.md` 的 self-read/shadow/archive 分级。
