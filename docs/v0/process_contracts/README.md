# V0 进程与壳层柜

`process_contracts/` 放链尾桥接、repo-local shell 和常驻生命进程合同。

## 文件分工

- `first_terminal_turn_engineering_contract.md`：第一次终端回合恢复。
- `terminal_life_loop_engineering_contract.md`：等待态、回合循环和写回。
- `digital_life_shell_command_engineering_contract.md`：`life-v0 "digital life"` 的 one-shot restore 壳。
- `digital_life_process_supervisor_engineering_contract.md`：`./digital life` 的 repo-local 最小常驻生命进程。

## 什么时候打开

- 处理外层命令面、stdin 回合循环、heartbeat、idle continuity。
- 处理恢复包、loop state、dialogue writeback、process report。

## 不要在这里做什么

- 不要把主体生命器官的字段定义写到这里，那些应回 `slice_contracts/`。
- 不要把总架构层判断写到这里，那些应回 `architecture/`。
