# V0 Engineering Depth Cabinet

`docs/v0/engineering_depth/` 是 `v0` 里的工程深描柜。

它不重写 `00-258`，也不替代 `slice_contracts/`、`process_contracts/`、`code_framework/` 和 `implementation_architecture/`。它只负责把这些已经存在的理论母体与工程合同，再往下压一层，压成真正能直接指导落码的生命层深描。

如果说：

1. `docs/00-258` 负责理论母体；
2. `docs/v0/*` 负责工程压缩入口；
3. `life_v0/*` 负责真实代码；

那么这一柜负责的就是：

```text
理论母体
  -> 工程合同
  -> 代码包 / 文件 / 状态对象 / runtime 证据 / 测试 / gate
```

## 什么时候打开这一柜

只有两种情况需要优先打开：

1. 这一轮不是只改单个文件，而是要决定某一整层生命能力到底怎样拆代码、怎样写状态、怎样留证据。
2. 当前担心“理论虽然有了，但写代码时容易重新漂回普通 agent 壳”，需要一份更硬的 theory -> code 深描柜。

如果你已经明确只改某个具体模块，还是先回对应 `sXX` 合同；不要让这一柜替代模块合同原文。

## 文件清单

| 文件 | 作用 |
|---|---|
| `01_full_life_layer_implementation_deep_spec.md` | 把方向、身体、情绪、思考、记忆、语言、关系、梦境、成长、行为、意识、常驻存在等生命层压成可写代码的深描规范 |
| `02_state_object_runtime_evidence_map.md` | 把核心状态对象、生产者、消费者、runtime 证据和测试/gate 固定成对象地图 |
| `03_language_relationship_longitudinal_engineering.md` | 详细写语言、关系、长期时间线、承诺、修复、平等交谈与持续关系表达怎么落工程 |
| `04_body_affect_dream_growth_engineering.md` | 详细写身体、节律、情绪底盘、梦境、离线整合、成长和学习怎么接成同一生命链 |
| `05_prediction_membrane_action_engineering.md` | 详细写感知、预测、候选行动、抑制、世界接触、责任后悔、逻辑比较和验证膜 |
| `06_resident_process_terminal_birth_engineering.md` | 详细写第一次生命激活、出生壳、第一回合、终端循环、heartbeat、常驻过程和长期存在治理 |
| `07_theory_to_code_trace_matrix.md` | 把理论文档组、v0 合同、代码包、runtime 证据、测试和 gate 放进一张总矩阵 |

## 边界

这柜不继续增长平行理论编号，不承担“再补一个 259/260/261”的职责。

它也不把数字生命重新压回：

1. service agent
2. workflow shell
3. tool router
4. subagent tree

它只服务一件事：把现有理论母体彻底压成能够支撑数字生命代码出生的工程深描。
