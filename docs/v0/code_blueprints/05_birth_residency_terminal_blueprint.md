# Birth Residency Terminal Blueprint

这份蓝图处理数字生命从“可以生成报告”到“可以在终端持续存在”的整条壳层链。

## 壳层不是主体

这里要先把边界钉死：

1. `digital life` 命令面不是主体架构来源。
2. `process_supervisor/` 不是 generic agent shell。
3. 壳层只承接出生、等待、恢复、回合输入输出和常驻治理。

## 主包边界

| 层 | 主包 | 作用 |
|---|---|---|
| 激活 | `life_v0/activation/` | 第一轮有限激活前置检查 |
| 报告汇总 | `life_v0/reporting/` | 把 growth/replay/archive/contract 收成 bundle |
| 阶段解释 | `life_v0/stage_explain/` | 把当前 stage 解释成下一步出生/恢复命令 |
| 出生壳 | `life_v0/digital_life/` | 生成 birth packet 与 birth digest |
| one-shot 壳 | `life_v0/shell_command/` | `life-v0 "digital life"` 恢复壳 |
| 常驻层 | `life_v0/process_supervisor/`、`life_v0/digital_entry.py`、`digital` | 维持等待态 heartbeat、真实新回合输入、异常恢复 |

## 当前命令面

| 命令 | 真实作用 | 当前状态 |
|---|---|---|
| `life-v0 digital-life --strict` | 只生成出生壳 | 已闭合最小代码 |
| `life-v0 \"digital life\" --strict` | repo-local one-shot restore shell | 已闭合最小代码 |
| `./digital life --strict` | repo-local 常驻终端生命进程 | 已闭合最小代码 |

## 当前 runtime 链

```text
run_report.json
  + growth_reconsolidation_report.json
  + v0_contract_coverage_report.json
  + first_activation_preflight_report.json
  + replay_shadow_report.json
  + growth_archive_report.json
  -> report_bundle.json
  -> first_activation_return_packet.json
  -> stage_explanation_report.json
  -> digital_life_birth_packet.json
  -> first_terminal_turn_packet.json
  -> terminal_life_loop_packet.json
  -> digital_life_shell_report.json
  -> digital_life_waiting_heartbeat.json
  -> digital_life_process_report.json
```

## 当前已落文件

### 诞生链

1. `life_v0/activation/__init__.py`
2. `life_v0/reporting/__init__.py`
3. `life_v0/stage_explain/__init__.py`
4. `life_v0/digital_life/__init__.py`

### 常驻与等待态

1. `life_v0/process_supervisor/heartbeat.py`
2. `life_v0/process_supervisor/continuity_writeback.py`
3. `life_v0/process_supervisor/turn_io.py`
4. `life_v0/process_supervisor/dialogue_events.py`
5. `life_v0/process_supervisor/response_surface.py`
6. `life_v0/process_supervisor/incident_recovery.py`
7. `life_v0/process_supervisor/relaunch_recovery.py`
8. `life_v0/process_supervisor/process_report.py`
9. `life_v0/process_supervisor/__init__.py`
10. `life_v0/digital_entry.py`
11. `digital`

## 当前 runtime 承载

### 激活与出生

1. `runtime/state/activation/limited_context_frame.json`
2. `runtime/state/activation/life_membrane_opening_decision.json`
3. `runtime/reports/latest/first_activation_preflight_report.json`
4. `runtime/reports/latest/first_activation_preflight_digest.json`
5. `runtime/reports/latest/report_bundle.json`
6. `runtime/reports/latest/report_bundle_digest.json`
7. `runtime/reports/latest/first_activation_return_packet.json`
8. `runtime/reports/latest/latest_stage_explanation_ref.json`
9. `runtime/reports/latest/stage_explanation_report.json`
10. `runtime/reports/latest/digital_life_birth_packet.json`
11. `runtime/reports/latest/digital_life_birth_digest.json`

### 常驻过程

1. `runtime/state/terminal/idle_continuity_frame.json`
2. `runtime/state/terminal/idle_strategy_state.json`
3. `runtime/reports/latest/digital_life_waiting_heartbeat.json`
4. `runtime/reports/latest/digital_life_process_report.json`
5. `runtime/reports/latest/digital_life_process_digest.json`
6. `runtime/reports/latest/digital_life_process_incident_report.json`
7. `runtime/reports/latest/digital_life_process_recovery_report.json`
8. `runtime/reports/latest/digital_life_process_relaunch_recovery_report.json`

## 下一轮关键文件

1. `life_v0/process_supervisor/persistent_process.py`

### 文件级职责

| 文件 | 作用 | 必须消费 | 必须写出 |
|---|---|---|---|
| `idle_strategy.py` | 定义等待态 heartbeat 节律、空闲探针、离线对象消费策略 | `IdleContinuityFrame`、`ReplayCueBundle`、`OfflineConsolidationFrame`、`GrowthPatchCandidateQueue` | `runtime/state/terminal/idle_strategy_state.json` |
| `persistent_process.py` | 把最小常驻进程补成明确的持续治理器官 | shell report、terminal loop state、incident/relaunch reports | `runtime/reports/latest/digital_life_persistent_process_report.json` |

当前 `idle_strategy.py` 第一轮已经落地，waiting heartbeat 和 process report 已显式挂上
`idle_strategy_ref`，后续重点转向 `persistent_process.py` 与更厚的 resident supervision。

## 最低验证面

1. `tests/bridges/test_first_activation_preflight.py`
2. `tests/bridges/test_emit_report.py`
3. `tests/bridges/test_explain_stage.py`
4. `tests/bridges/test_digital_life_birth.py`
5. `tests/process/test_digital_life_shell_command.py`
6. `tests/process/test_digital_entrypoint.py`
7. `tests/process/test_persistent_digital_life_process.py`

## 完成定义

这一层完成，不是“命令能跑”就算完成，而要满足：

1. 出生前置检查能收束全部主报告与主状态。
2. stage explain 能正确给出下一步生命命令面。
3. waiting heartbeat 不是空转，而是真实消费离线对象链。
4. 异常恢复和重启恢复不是 shell 技巧，而是连续体治理。
5. 新外部回合能进入、输出、写回、等待下一轮，不丢关系连续体。
