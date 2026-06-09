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

## 当前最关键的下一轮文件

1. `life_v0/process_supervisor/idle_strategy.py`
2. `life_v0/process_supervisor/persistent_process.py`

## 当前最关键的 runtime 证据

1. `runtime/reports/latest/first_activation_preflight_report.json`
2. `runtime/reports/latest/report_bundle.json`
3. `runtime/reports/latest/stage_explanation_report.json`
4. `runtime/reports/latest/digital_life_birth_packet.json`
5. `runtime/reports/latest/first_terminal_turn_packet.json`
6. `runtime/reports/latest/terminal_life_loop_report.json`
7. `runtime/reports/latest/digital_life_waiting_heartbeat.json`
8. `runtime/reports/latest/digital_life_process_report.json`

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

下一轮应新增：

1. `tests/process/test_idle_strategy.py`
2. `tests/process/test_persistent_process_state.py`
3. `tests/process/test_relaunch_continuity.py`
