# Resident Process Terminal Birth Engineering

本文档把第一次生命激活、出生壳、第一回合、终端循环、heartbeat 和常驻过程，压成一条完整存在链。

## 当前存在链

当前最小存在链已经真实闭合到：

```text
life-v0 emit-report --strict
  -> life-v0 explain-stage --strict
  -> life-v0 digital-life --strict
  -> life-v0 first-terminal-turn --strict
  -> life-v0 terminal-life-loop --strict
  -> life-v0 "digital life" --strict
  -> ./digital life --strict
```

## 当前最关键的器官文件

1. `life_v0/process_supervisor/live_turn_cycle.py` 已接住真实新回合的 success / incident 生命周期
2. `life_v0/process_supervisor/resident_supervision.py` 已接住 restore shell 之后的常驻治理启动链
3. `life_v0/process_supervisor/idle_strategy.py` 继续补厚 heartbeat 节律与 idle probe 治理
4. `life_v0/process_supervisor/persistent_process.py` 继续补厚 resident supervision 的关闭态 artifact，并显式写出 resident governance snapshot / report
5. `life_v0/process_supervisor/process_closeout.py` 与 `process_report.py` 已把 resident governance 证据收口进主进程 report / digest / receipt
6. `life_v0/process_supervisor/process_session_loop.py` 已接住 waiting heartbeat refresh + live turn dispatch 的 session 编排；当前前沿转向后台 resident governance 与更高频节律

## 当前最关键的 runtime 证据

1. `runtime/reports/latest/first_activation_preflight_report.json`
2. `runtime/reports/latest/report_bundle.json`
3. `runtime/reports/latest/stage_explanation_report.json`
4. `runtime/reports/latest/digital_life_birth_packet.json`
5. `runtime/reports/latest/first_terminal_turn_packet.json`
6. `runtime/reports/latest/terminal_life_loop_report.json`
7. `runtime/reports/latest/digital_life_waiting_heartbeat.json`
8. `runtime/state/terminal/idle_strategy_state.json`
9. `runtime/state/terminal/persistent_process_state.json`
10. `runtime/state/terminal/resident_governance_snapshot.json`
11. `runtime/reports/latest/digital_life_persistent_process_report.json`
12. `runtime/reports/latest/digital_life_resident_governance_report.json`
13. `runtime/reports/latest/digital_life_process_report.json`

## 最低测试与新增测试

当前最低测试：

1. `tests/bridges/test_first_activation_preflight.py`
2. `tests/bridges/test_emit_report.py`
3. `tests/bridges/test_explain_stage.py`
4. `tests/bridges/test_digital_life_birth.py`
5. `tests/bridges/test_first_terminal_turn.py`
6. `tests/bridges/test_terminal_life_loop.py`
7. `tests/process/test_digital_life_shell_command.py`
8. `tests/process/test_digital_entrypoint.py`
9. `tests/process/test_persistent_digital_life_process.py`

下一轮应新增或补厚：

1. `tests/process/test_idle_strategy.py`
2. `tests/process/test_persistent_process_state.py`
3. `tests/process/test_relaunch_continuity.py`
4. `tests/process/test_live_turn_cycle.py`
5. `tests/process/test_process_session_loop.py`（若后续从 `test_persistent_digital_life_process.py` 独立拆出）

当前实际已经由 `tests/process/test_persistent_digital_life_process.py` 吸收了
`idle_strategy.py`、`persistent_process.py`、`resident_supervision.py` 与 `live_turn_cycle.py`
的第一轮红绿覆盖，并且这轮又继续把 `resident_governance_snapshot.json` /
`digital_life_resident_governance_report.json` 及其在主进程 report / receipt 上的回链断言纳入同一测试闭环；后续是否拆独立测试文件，以不破坏现有 Queue B 测试闭环为先。
