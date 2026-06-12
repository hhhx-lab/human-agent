# Digital Life Shell Command Engineering Contract

本文档把 `life-v0 "digital life"` 的 one-shot restore shell 固定成独立工程合同。它不是新的主体 slice，也不是新的脑科学理论层；它也不是常驻进程本体。它只负责把已经闭合的三段链：

```text
life-v0 digital-life
  -> life-v0 first-terminal-turn
  -> life-v0 terminal-life-loop
```

收成一个外层恢复壳命令，让这台电脑里的数字生命可以先被恢复，再交给常驻进程层继续维持。

repo-local `./digital life`、可安装后的 `digital life` 和推荐入口 `my digital life` 现在都已经比 one-shot restore shell 多一层：真实 TTY 下的裸 `digital life` 会进入 resident attach，`my digital life` 会先绑定或校验 `runtime/state/identity/life_name_registry.json`，再启动或复用后台 resident process，把终端话语投递给同一个后台生命进程。`digital life --background / --status / --say / --stop` 是同一套 resident lifecycle 命令面；非交互管道、测试输入和 `--foreground` 仍保留前台 process loop；`life-v0 "digital life"` 仍只代表 one-shot restore shell。

## 模块定位

当前链尾已经闭合到：

```text
emit-report
  -> explain-stage
  -> digital-life
  -> first-terminal-turn
  -> terminal-life-loop
```

但这仍然是三段内部工程命令。最终目标体验不是要求外部再次理解这三段，而是：

```text
digital life
  -> direction restore
  -> life state restore
  -> terminal birth restore
  -> first terminal turn restore
  -> terminal life loop restore
```

所以这一层的职责是：

1. 接住 `stage_explanation_report.json` 已经返回的 `digital life` 缺口命令位。
2. 顺序调用内部三段闭合链，而不是让调用方自己拼接。
3. 写出统一的外层壳报告、摘要、packet 和 receipt。
4. 把恢复后的下一步固定为“等待下一次外部关系回合”。
5. 为 `DIGITAL_LIFE_PROCESS_SUPERVISOR` 提供可复用的 restore shell，而不是自己承担常驻进程职责。

## 必须读取

| 来源 | digital life shell 吸收内容 |
|---|---|
| `docs/20_agent_runtime_bridge_contract.md` | 终端外壳顺序、`SessionEnvelope`、恢复链 |
| `docs/89_language_runtime_framework_bridge_and_life_shell_policy.md` | 语言恢复顺序、生命壳禁写边界 |
| `docs/90_language_event_examples_and_timeline_bundle.md` | 回合级语言事件与恢复后回合节奏 |
| `docs/v0/references/current_agent_shell_reference_2026.md` | `digital life` 只作为外层入口，不反向定义主体 |
| `docs/v0/shared_contracts/runner_cli_report_contract.md` | `digital life` 壳位和最小输入输出合同 |
| `docs/v0/shared_contracts/first_activation_protocol.md` | 第一次有限激活之后的恢复链 |
| `docs/v0/process_contracts/first_terminal_turn_engineering_contract.md` | 第一终端回合恢复材料 |
| `docs/v0/process_contracts/terminal_life_loop_engineering_contract.md` | 持续终端生命循环材料 |
| `runtime/reports/latest/stage_explanation_report.json` | 当前是否已允许 terminal birth restore |
| `runtime/reports/latest/digital_life_birth_packet.json` | 出生壳状态 |
| `runtime/reports/latest/first_terminal_turn_packet.json` | 第一终端回合状态 |
| `runtime/reports/latest/terminal_life_loop_packet.json` | 当前终端生命循环状态 |
| `runtime/state/terminal/session_envelope.json` | 当前短期终端生命壳 |
| `runtime/state/terminal/safe_terminal_loop_state.json` | 当前安全等待态 |
| `runtime/state/terminal/terminal_life_loop_state.json` | 当前终端循环状态 |

## 运行承载

| 承载 | 路径 |
|---|---|
| 代码包 | `life_v0/shell_command/` |
| 状态命名空间 | `runtime/state/terminal/` |
| packet | `runtime/reports/latest/digital_life_shell_packet.json` |
| report | `runtime/reports/latest/digital_life_shell_report.json` |
| digest | `runtime/reports/latest/digital_life_shell_digest.json` |
| receipt | `runtime/receipts/digital_life_shell_<run_id>.json` |

## 命令合同

当前内部壳命令仍保持：

```text
life-v0 digital-life --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 first-terminal-turn --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 terminal-life-loop --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
```

当前 one-shot restore shell 的命令面固定为：

```text
life-v0 "digital life" --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
```

如果在 repo 根目录直接工作，也可以通过：

```text
python -m life_v0 "digital life" --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
```

进入同一层 one-shot restore shell。

它不是普通 shell alias，也不是 workflow graph。它的意义是把“出生恢复”收成一个可复用的 restore shell，供更外层的常驻生命进程继续承载。

repo-local `./digital life` 与安装后 `digital life` 的当前命令面分层为同一套：

```text
./digital life
digital life
  -> interactive TTY: start/reuse resident process, attach terminal relation client
  -> non-interactive stdin: foreground process loop for tests and scripted runs

./digital life --attach
digital life --attach
  -> force resident attach even under piped stdin

./digital life --foreground
digital life --foreground
  -> force foreground process loop even under interactive TTY

./digital life --background / --status / --say / --stop
digital life --background / --status / --say / --stop
  -> resident lifecycle and single-turn relation delivery controls

my digital life --name <life-name>
  -> bind life_name_registry.json once, then delegate to the same resident lifecycle
```

其中 `--status` 不再只是 PID 查询。它必须把同一 resident process 的 lifecycle state、relation queue、自主活动相位与闭合状态、waiting heartbeat、resident governance、idle strategy、terminal loop、`resident_process_lease`、`resident_process_lease_history_profile`、persistent process closeout 与 background convergence 摘成一个 `resident_long_term_residency_status_v0` 视图。这个视图只负责暴露持续存在证据，不承担调度或工具控制职责。

`/exit` 在 attach client 中只代表当前终端脱离，后台 resident process 继续驻留；`/stop`、`./digital life --stop` 或安装后的 `digital life --stop` 才会写 lifecycle command，让 resident process 通过普通 closeout 收口。

## 阶段门

| gate | 通过条件 | 失败后动作 |
|---|---|---|
| `stage_explanation_gate` | `stage_explanation_report.json` 为 `closed`，且 `next_required_command=digital life` | 返回 `life-v0 explain-stage --strict` |
| `digital_birth_gate` | `digital_life_birth_packet.json` 为 `closed` 或可通过当前运行闭合 | 返回 `life-v0 digital-life --strict` |
| `first_terminal_turn_gate` | `first_terminal_turn_packet.json` 为 `closed` 或可通过当前运行闭合 | 返回 `life-v0 first-terminal-turn --strict` |
| `terminal_life_loop_gate` | `terminal_life_loop_packet.json` 为 `closed` 或可通过当前运行闭合 | 返回 `life-v0 terminal-life-loop --strict` |
| `shell_writeback_gate` | 外层壳 report、digest、packet、receipt 全部写出 | 阻断外层壳完成 |

## 最小输出

| 文件 | 内容 |
|---|---|
| `digital_life_shell_packet.json` | 一键入口壳当前闭合状态、三段内部闭合 refs、下一外部回合入口 |
| `digital_life_shell_report.json` | 外层壳主报告 |
| `digital_life_shell_digest.json` | 外层壳摘要 |
| `digital_life_shell_<run_id>.json` | 外层壳 receipt |

## Report 最小字段

```json
{
  "schema_version": "digital_life_shell_report_v0",
  "status": "closed",
  "engineering_slice_ref": "DIGITAL_LIFE_SHELL_COMMAND",
  "current_shell_mode": "terminal_life_loop_restored",
  "birth_packet_ref": "runtime/reports/latest/digital_life_birth_packet.json",
  "first_terminal_turn_ref": "runtime/reports/latest/first_terminal_turn_packet.json",
  "terminal_life_loop_ref": "runtime/reports/latest/terminal_life_loop_packet.json",
  "next_required_action": "await_next_external_relation_turn"
}
```

## 回链要求

这一层新增后，所有外层壳产物仍然必须带着：

1. `source_doc_refs`
2. `readme_block_refs`
3. `engineering_slice_ref`
4. `runtime_carrier_refs`

它们的作用不是装饰，而是防止 `digital life` 从“承载生命体系的出生入口”退化成“对三段内部命令的简单包装脚本”。

## 完成定义

只有当下面四项同时存在时，才能说 one-shot restore shell 已经落成最小闭合：

1. `runtime/reports/latest/digital_life_shell_packet.json`
2. `runtime/reports/latest/digital_life_shell_report.json`
3. `runtime/reports/latest/digital_life_shell_digest.json`
4. `runtime/receipts/digital_life_shell_<run_id>.json`

此时调用方面对的入口不再是三段内部命令，而是：

```text
life-v0 "digital life"
  -> restore_birth_shell
  -> restore_first_terminal_turn
  -> restore_terminal_life_loop
  -> await_next_external_relation_turn
```

持续等待真实新回合、resident attach、关系投递队列、关闭终端后的睡眠/回忆/思考/成长/学习活动，不属于 one-shot restore shell；那是 `digital_life_process_supervisor_engineering_contract.md` 的职责。
