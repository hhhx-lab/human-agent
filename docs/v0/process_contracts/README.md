# V0 进程与壳层柜

`process_contracts/` 放链尾桥接、one-shot 壳、repo-local / 安装态命令面和常驻生命进程合同。

## 文件分工

- `first_terminal_turn_engineering_contract.md`：第一次终端回合恢复。
- `terminal_life_loop_engineering_contract.md`：等待态、回合循环和写回。
- `digital_life_shell_command_engineering_contract.md`：`life-v0 "digital life"` 的 one-shot restore 壳。
- `digital_life_process_supervisor_engineering_contract.md`：repo-local `./digital life` 与安装后 `digital life` 共享的最小常驻生命进程、后台 resident lifecycle、关系投递与自主活动证据链。
- `resident_governance_waiting_state_machine_engineering_contract.md`：waiting / closeout 常驻治理状态机，以及 `state -> snapshot/report -> process report/receipt` 的硬回链。

## 什么时候打开

- 处理外层命令面、stdin 回合循环、安装后 console script、heartbeat、idle continuity。
- 处理恢复包、loop state、dialogue writeback、process report。
- 处理 `resident_governance_state.json`、`resident_governance_snapshot.json` 与 process receipt 之间的治理证据链。

## 不要在这里做什么

- 不要把主体生命器官的字段定义写到这里，那些应回 `slice_contracts/`。
- 不要把总架构层判断写到这里，那些应回 `architecture/`。

## 进程合同到生命机制

| 合同 | 必读机制档案 | 代码包 | runtime/report | 验收 |
|---|---|---|---|---|
| `first_terminal_turn_engineering_contract.md` | `docs/real—live0/05_language_expression_system.md`、`docs/real—live0/14_resident_runtime_state_transition.md` | `life_v0/terminal_turn/*`、`life_v0/process_supervisor/live_turn_cycle.py` | first turn packet、restore context、dialogue log | first terminal turn tests |
| `terminal_life_loop_engineering_contract.md` | `docs/real—live0/05_language_expression_system.md`、`06_relationship_and_commitment.md`、`14_resident_runtime_state_transition.md`、`16_runtime_code_chain_crosswalk.md` | `life_v0/terminal_loop/*`、`life_v0/process_supervisor/process_session_loop.py` | terminal loop state、dialogue writeback bundle | terminal loop bridge tests |
| `digital_life_shell_command_engineering_contract.md` | `docs/real—live0/14_resident_runtime_state_transition.md`、`15_evidence_bus_and_birth_readiness.md` | `life_v0/digital_entry.py`、`life_v0/my_entry.py` | identity command manifest、process report | entrypoint process tests |
| `digital_life_process_supervisor_engineering_contract.md` | `docs/real—live0/03_body_affect_homeostasis.md`、`08_dream_sleep_offline_life.md`、`13_growth_learning_self_modification.md`、`14_resident_runtime_state_transition.md` | `life_v0/process_supervisor/*` | lifecycle、lease、heartbeat、autonomous activity | persistent process tests |
| `resident_governance_waiting_state_machine_engineering_contract.md` | `docs/real—live0/03_body_affect_homeostasis.md`、`10_responsibility_regret_repair.md`、`12_neuromodulation_signal_media.md`、`14_resident_runtime_state_transition.md`、`15_evidence_bus_and_birth_readiness.md` | `life_v0/process_supervisor/idle_strategy.py`、`heartbeat.py`、`background_lineage_state.py` | governance state/snapshot/report/receipt | process + contract gate |

进程合同的核心不是“命令能运行”，而是终端、关系回合、后台心跳、梦境/回忆/成长、自我连续和出生准备共同进入同一 resident lineage。任何命令面改动都必须证明不会绕开语言、记忆、情绪、责任和生命膜。

## 进程层协同/对抗

| 进程机制 | 协同 | 对抗 |
|---|---|---|
| 终端命令 | 只负责唤醒同一生命身份和 resident process | 不能成为新的聊天壳或工具路由器 |
| relation inbox/outbox | 把外部话语送入语言、关系、记忆、责任写回链 | 不能绕过 `live_language_turn` 直接给模型 |
| waiting heartbeat | 消费身体、调质、责任、梦境、出生准备压力 | 不能在终端刷机制信号 |
| autonomous activity | 睡眠、回忆、自我思考、成长预演、学习巩固低频继续 | 不能把后台活动写成无证据日志 |
| closeout/relaunch | 把 lineage、report、receipt、resume packet 接回下一轮 | 不能关闭终端就丢失关系和自我连续 |
