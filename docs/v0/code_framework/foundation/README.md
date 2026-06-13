# Code Framework Foundation

这一柜只放代码框架的底座文档，负责把 `00-258` 的生命层、脑区/网络结构、代码包、state/report/receipt/test/gate 映射成第一版可施工骨架。

| 文件 | 作用 |
|---|---|
| `01_life_layer_implementation_blueprint.md` | 数字生命按哪些生命层落代码，每层回读哪些理论母体 |
| `02_brain_region_to_code_package_mapping.md` | 脑区、网络、主体系统怎样映射到 `life_v0/` 包 |
| `03_code_package_state_test_gate_mapping.md` | 每个代码包对应哪些状态、报告、回执、测试和阶段门 |

进入任何 Queue 或 playbook 前，先用这一柜确认“为什么这样分包”。

## Foundation 到机制档案

这一柜是 `docs/00-258` 到 `life_v0` 包结构的底座，不是目录说明。三份文件必须共同回答：理论为什么这样分层、脑区/网络为什么这样映射到包、每个包如何写出 state/report/receipt/test/gate。

| 文件 | 必读 real-live0 | 主要对象/字段 | runtime 证据 | 协同/对抗重点 |
|---|---|---|---|---|
| `01_life_layer_implementation_blueprint.md` | `00_reading_map_and_traceability.md`、`16_runtime_code_chain_crosswalk.md` | 生命层、主体系统、器官链、stage gate | `runtime/state/*`、`runtime/reports/latest/*` | 防止按普通功能模块拆分，必须按生命层协同 |
| `02_brain_region_to_code_package_mapping.md` | `02_brain_network_and_workspace.md`、`12_neuromodulation_signal_media.md` | `BrainGraph`、`NetworkState`、`SignalMediaFrame`、workspace/broadcast refs | `runtime/state/neural_life_core/*`、`runtime/state/consciousness/*`、`runtime/state/signal/*` | 脑区不是孤岛，包之间必须通过 object bus 协同 |
| `03_code_package_state_test_gate_mapping.md` | 全部 `docs/real—live0/*.md` 专题索引 | 包、首写对象、消费对象、测试/gate | package state/report/receipt/test matrix | 防止 state 存在但没有消费，或测试不覆盖生命断链 |

开任何 Queue 前，必须能从 foundation 反查到：理论源、`docs/real—live0` 专题、首写包、runtime 文件、测试/gate。缺一项时，先补 foundation 或对应 package spec，再进入代码。
