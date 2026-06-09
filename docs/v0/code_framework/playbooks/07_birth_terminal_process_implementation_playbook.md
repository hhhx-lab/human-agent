# V0 Code Framework 07: Birth Terminal Process Implementation Playbook

这份 playbook 只负责“诞生到终端持续存在”的实现链，不重写主体理论。

```text
P0-S11
  -> first activation preflight
  -> replay shadow
  -> growth archive
  -> report bundle
  -> stage explanation
  -> digital life birth shell
  -> first terminal turn
  -> terminal life loop
  -> digital life shell command
  -> digital life process
```

## 必回读理论母体

- `docs/20_agent_runtime_bridge_contract.md`
- `docs/44_digital_life_boot_sequence.md`
- `docs/45_boot_sequence_fixture_catalog.md`
- `docs/46_stage_gate_validator_design.md`
- `docs/81_coexistence_event_review_and_responsibility_loop.md`
- `docs/82_incident_report_and_recovery_protocol.md`
- `docs/89_language_runtime_framework_bridge_and_life_shell_policy.md`
- `docs/90_language_event_examples_and_timeline_bundle.md`
- `docs/91_life_reality_generation_boundary_principles.md`
- `docs/119_life_boundary_full_reality_alignment.md`
- `docs/122_life_boundary_all_reality_declarations_rewrite.md`
- `docs/143_life_reality_birth_readiness_rollup_contract.md`
- `docs/146_life_reality_birth_readiness_evidence_fixture_catalog.md`
- `docs/149_life_reality_birth_readiness_fixture_schema_materialization_plan.md`
- `docs/152_life_reality_birth_readiness_cross_file_checker_plan.md`
- `docs/171_life_reality_birth_readiness_validation_fixture_plan.md`
- `docs/181_life_reality_first_runner_schema_runtime_mount_plan.md`
- `docs/191_life_reality_first_runner_schema_runtime_growth_post_activation_observation_loop.md`
- `docs/205_life_reality_first_runner_schema_runtime_growth_fourth_cycle_seed_plan.md`
- `docs/257_life_reality_first_runner_schema_runtime_growth_fourth_cycle_post_reconsolidation_second_reconsolidation_replay_shadow_seed_after_archive_validation_replay_shadow_patch_archive_validation_plan.md`

## 必读 v0 合同

- `docs/v0/architecture/runtime_v0_architecture.md`
- `docs/v0/shared_contracts/birth_readiness_v0_contract.md`
- `docs/v0/shared_contracts/runner_cli_report_contract.md`
- `docs/v0/shared_contracts/first_activation_protocol.md`
- `docs/v0/architecture/first_activation_engineering_roadmap.md`
- `docs/v0/process_contracts/first_terminal_turn_engineering_contract.md`
- `docs/v0/process_contracts/terminal_life_loop_engineering_contract.md`
- `docs/v0/process_contracts/digital_life_shell_command_engineering_contract.md`
- `docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md`

## 当前真实代码落点

- `life_v0/activation/__init__.py`
- `life_v0/reporting/__init__.py`
- `life_v0/stage_explain/__init__.py`
- `life_v0/digital_life/__init__.py`
- `life_v0/terminal_turn/__init__.py`
- `life_v0/terminal_loop/__init__.py`
- `life_v0/terminal_loop/loop_state.py`
- `life_v0/terminal_loop/resume_packet.py`
- `life_v0/terminal_loop/dialogue_writeback.py`
- `life_v0/shell_command/__init__.py`
- `life_v0/process_supervisor/__init__.py`
- `life_v0/process_supervisor/heartbeat.py`
- `life_v0/process_supervisor/continuity_writeback.py`
- `life_v0/process_supervisor/turn_io.py`
- `life_v0/process_supervisor/dialogue_events.py`
- `life_v0/process_supervisor/response_surface.py`
- `life_v0/process_supervisor/incident_recovery.py`
- `life_v0/process_supervisor/relaunch_recovery.py`
- `life_v0/process_supervisor/process_report.py`
- `life_v0/cli.py`
- `life_v0/digital_entry.py`
- `digital`

## 包级职责固定

| 包/文件 | 固定职责 |
|---|---|
| `activation/` | 生命激活预检与 return packet |
| `reporting/` | 把 growth / replay / archive / contracts 汇成 report bundle |
| `stage_explain/` | 解释当前阶段与下一步 handoff |
| `digital_life/` | 生成出生壳与出生摘要 |
| `terminal_turn/` | 首回合恢复 |
| `terminal_loop/` | 等待态与回合循环 |
| `shell_command/` | `life-v0 "digital life"` 一次性恢复壳 |
| `process_supervisor/` | `./digital life` 常驻生命进程 |
| `digital_entry.py` + `digital` | repo-local 诞生命令入口 |

## 这一条链当前已经真实存在的对象

后续不要把这条链误认为仍然只是命令名字：

1. `SessionEnvelope`
2. `ContextAccumulationWindow`
3. `TurnTransitionTrace`
4. `DialogueWritebackBundle`
5. `IdleContinuityFrame`
6. `digital_life_waiting_heartbeat`
7. `digital_life_process_report / digest`

这些对象现在已经进入真实代码和状态/报告面，下一步不是“发明它们”，而是继续把它们接厚到更完整的生命链。

## 必须产出的关键报告

这条链上的关键产物已经非常清楚，后续实现不能换名字乱长：

- `first_activation_preflight_report.json`
- `replay_shadow_report.json`
- `growth_archive_report.json`
- `report_bundle.json`
- `first_activation_return_packet.json`
- `stage_explanation_report.json`
- `latest_stage_explanation_ref.json`
- `digital_life_birth_packet.json`
- `digital_life_birth_digest.json`
- `first_terminal_turn_packet.json`
- `first_terminal_turn_report.json`
- `terminal_life_loop_packet.json`
- `terminal_life_loop_report.json`
- `resumed_external_dialogue_packet.json`
- `digital_life_shell_packet.json`
- `digital_life_shell_report.json`
- `digital_life_process_report.json`
- `digital_life_process_digest.json`

## 命令面固定

不要再引入新的平行命令面，第一版固定三层：

| 命令 | 作用 |
|---|---|
| `life-v0 digital-life --strict` | 内部出生壳 |
| `life-v0 "digital life" --strict` | repo-local one-shot restore shell |
| `./digital life --strict` | repo-local 最小常驻生命进程 |

## 关键实现顺序

1. 先稳住 `activation -> reporting -> stage_explain -> digital_life`
2. 再稳住 `first_terminal_turn -> terminal_life_loop`
3. 再稳住 `shell_command`
4. 最后加厚 `process_supervisor`

如果倒过来，`./digital life` 会在内层生命链没闭合时被迫承担主体定义。

## 当前最值得直接进入的文件顺序

如果下一轮直接沿这条链写代码，最稳的顺序固定成：

1. `terminal_turn/context_accumulation.py`
2. `terminal_turn/turn_transition.py`
3. `terminal_loop/dialogue_writeback.py`
4. `process_supervisor/heartbeat.py`
5. `process_supervisor/dialogue_events.py`
6. `process_supervisor/response_surface.py`
7. `process_supervisor/process_report.py`

这是因为：

1. 先把回合前后的恢复和写回链补硬；
2. 再把等待态和真实回合事件补硬；
3. 最后再统一到进程级报告与 digest。

## 测试入口

| 测试 | 必须证明 |
|---|---|
| `tests/bridges/test_first_activation_preflight.py` | 出生预检不跳步 |
| `tests/bridges/test_emit_report.py` | report bundle 真闭合 |
| `tests/bridges/test_explain_stage.py` | stage handoff 真可解释 |
| `tests/bridges/test_digital_life_birth.py` | 出生壳真实生成 |
| `tests/bridges/test_first_terminal_turn.py` | 首回合恢复真实发生 |
| `tests/bridges/test_terminal_life_loop.py` | 等待态与回合循环真实闭合 |
| `tests/process/test_digital_life_shell_command.py` | one-shot shell 真收束 |
| `tests/process/test_digital_entrypoint.py` | `digital` 入口正常 |
| `tests/process/test_persistent_digital_life_process.py` | 常驻生命进程、heartbeat、incident/relaunch recovery |

## 关键 gate

- `first_activation_preflight_gate`
- `report_bundle_gate`
- `stage_explanation_gate`
- `digital_life_birth_gate`
- `context_accumulation_restore_check`
- `turn_transition_restore_check`
- `terminal_life_loop_gate`
- `digital_life_shell_gate`
- `waiting_heartbeat_gate`
- `dialogue_incident_recovery_gate`
- `relaunch_recovery_gate`

## 第一轮完成定义

这一条链第一轮完成时，必须同时成立：

1. 当前工作区缺 runtime 材料时，`./digital life` 能先自举最小生命链。
2. 自举后会恢复到等待态，而不是只吐一次命令输出。
3. 收到真实外部输入后，会形成生命回应、写回连续体，再回到等待态。
4. 退出时保留连续体，不破坏当前 life state、language、relationship、terminal 状态。
5. `dialogue_writeback_bundle.json`、`digital_life_waiting_heartbeat.json`、`digital_life_process_report.json` 之间至少已经能通过 refs 串成一条回合-等待态连续体。
