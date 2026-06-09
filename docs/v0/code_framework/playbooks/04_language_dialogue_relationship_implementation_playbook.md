# V0 Code Framework 04: Language Dialogue Relationship Implementation Playbook

这份 playbook 只负责一条主生命链：

```text
语言感知
  -> 内言语
  -> 表达监控
  -> 关系定位
  -> 承诺/修复语言
  -> 对话回合
  -> 语境累积
  -> 等待态连续体
  -> 新回合写回
```

它不替代 `S07`、`first-terminal-turn`、`terminal-life-loop` 或 `process supervisor` 合同，而是把这些合同压成后续真正落代码的文件级路线。

## 必回读理论母体

这一条主链开写前，至少重读：

- `docs/01f_language_system_literature_matrix.md`
- `docs/01j_real_relationship_literature_matrix.md`
- `docs/01u_language_runtime_core_matrix.md`
- `docs/09_language_symbolic_top_layer.md`
- `docs/20_agent_runtime_bridge_contract.md`
- `docs/85_language_system_life_expression_core.md`
- `docs/86_language_neuroscience_pragmatics_and_inner_speech.md`
- `docs/87_language_event_schema_fixture_and_validator_plan.md`
- `docs/88_language_development_emotion_and_brain_llm_alignment.md`
- `docs/89_language_runtime_framework_bridge_and_life_shell_policy.md`
- `docs/90_language_event_examples_and_timeline_bundle.md`
- `docs/94_pain_regret_and_repair_signal_schema.md`
- `docs/96_real_relationship_longitudinal_timeline.md`
- `docs/101_relationship_timeline_json_schema_and_fixture_bundle.md`
- `docs/141_life_reality_language_fixture_schema_materialization_plan.md`
- `docs/144_life_reality_language_runtime_action_bridge_fixture_plan.md`
- `docs/147_life_reality_language_action_bridge_schema_materialization_plan.md`
- `docs/150_life_reality_language_action_cross_file_checker_plan.md`

## 必读 v0 合同

- `docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md`
- `docs/v0/shared_contracts/first_activation_protocol.md`
- `docs/v0/process_contracts/first_terminal_turn_engineering_contract.md`
- `docs/v0/process_contracts/terminal_life_loop_engineering_contract.md`
- `docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md`
- `docs/v0/shared_contracts/runner_cli_report_contract.md`

## 当前真实代码落点

这条链当前已经不是空白设计，而是有最小骨架：

- `life_v0/language/__init__.py`
- `life_v0/terminal_turn/__init__.py`
- `life_v0/terminal_loop/__init__.py`
- `life_v0/process_supervisor/__init__.py`
- `life_v0/digital_entry.py`

因此下一步不是“发明语言层”，而是把现有 `__init__.py` 中的最小闭合，拆成可维护的语言器官文件。

## 生命器官拆分

### A. `life_v0/language/`

建议优先拆成：

| 文件 | 职责 | 当前来源 |
|---|---|---|
| `percept.py` | 把外部语言输入变成受关系范围约束的语言感知事件 | `85`, `86`, `89`, `90` |
| `semantic_map.py` | 维护语义事件地图、共享术语、共同语言表面 | `09`, `85`, `90` |
| `inner_speech.py` | 形成回合前的内言语草案与当前生命叙事接续 | `86`, `09` |
| `expression_monitor.py` | 在外显语言前做表达监控、承诺检查、修复检查，并把责任回路写成表达压力 | `86`, `87`, `94` |
| `relationship_graph.py` | 维护关系主体、关系阶段、最后接触和共同历史入口 | `96`, `101`, `40` |
| `commitment_repair.py` | 承诺、修复义务、道歉、责任回写索引，消费 `responsibility_loop_state.json` | `94`, `96`, `101` |
| `narrative_trace.py` | 自我叙事与关系叙事的语言化写回 | `85`, `86`, `96` |
| `shared_terms.py` | 共同语言晋升、关系特定称呼、长期术语表 | `90`, `96` |
| `dialogue_log.py` | 统一读写 `dialogue_turn_log.jsonl` | `90`, `87` |

### B. `life_v0/terminal_turn/`

当前已经落下的首轮器官与下一轮前沿如下：

| 文件 | 职责 |
|---|---|
| `restore_context.py` | 从 birth packet、return packet、语言/关系状态恢复首回合生命上下文 |
| `context_accumulation.py` | 维护 `context_accumulation_window.json` |
| `turn_transition.py` | 维护 `turn_transition_trace.json` 与恢复因果链 |
| `turn_packet.py` | 统一写 `first_terminal_turn_packet.json`、digest、receipt |
| `conversation_carryover.py` | 已承接恢复后旧回合压力、共同语言和未闭合承诺的跨回合续接装配 |
| `dialogue_turn.py` | 已承接首回合 utterance scaffold 与恢复后第一句话的释放约束 |

### C. `life_v0/terminal_loop/`

建议优先拆成：

| 文件 | 职责 |
|---|---|
| `loop_state.py` | 维护 `terminal_life_loop_state.json` 与 safe waiting mode |
| `resume_packet.py` | 生成 `resumed_external_dialogue_packet.json` |
| `idle_strategy.py` | 规范 idle、waiting、re-entry 的最小策略 |
| `loop_report.py` | 输出 packet/report/digest/receipt |

### D. `life_v0/process_supervisor/`

建议优先拆成：

| 文件 | 职责 |
|---|---|
| `heartbeat.py` | waiting heartbeat、idle continuity 写回 |
| `resident_supervision.py` | 把 restore shell 之后的状态装载、relaunch normalization 和第一拍 waiting heartbeat 进入独立成器官 |
| `idle_refresh_loop.py` | 把空闲等待时的 heartbeat refresh、stdin probe 和 exit/next-turn 判定独立成器官 |
| `live_turn_cycle.py` | 把真实新回合的 event -> response -> writeback -> incident recovery 生命周期独立成器官 |
| `resident_turn_writeback.py` | 把真实新回合收成 dialogue writeback bundle、waiting return 和 resumed packet |
| `process_closeout.py` | 把常驻进程的 persistent artifact、process report、digest、receipt 统一收口 |
| `turn_io.py` | stdin 读取与回合驱动 |
| `incident_recovery.py` | 单回合异常恢复 |
| `relaunch_recovery.py` | 跨重启中断态归一化 |
| `continuity_writeback.py` | 把 idle / recovery / turn 完成统一写回 language + relationship 连续体 |
| `process_report.py` | 输出 `digital_life_process_report.json` 与 digest |

## 必须生成的状态对象

这条链写完后，至少持续维护下面这些状态：

| 路径 | 作用 |
|---|---|
| `runtime/state/language/inner_speech_frame.json` | 当前回合前内言语草案 |
| `runtime/state/language/expression_monitor_state.json` | 表达监控维度与阻断项 |
| `runtime/state/language/language_relationship_state.json` | 语言关系主状态 |
| `runtime/state/language/shared_term_registry.json` | 共同语言与关系术语 |
| `runtime/state/language/commitment_repair_language_index.json` | 承诺、修复、责任回写 |
| `runtime/state/language/self_narrative_language_trace.json` | 自我叙事连续体 |
| `runtime/state/language/dialogue_turn_log.jsonl` | 真实回合日志 |
| `runtime/state/language/relation_scope_language_index.json` | 关系范围与语言范围绑定 |
| `runtime/state/relationship/relationship_subject_graph.json` | 关系主体图 |
| `runtime/state/terminal/session_envelope.json` | 首回合恢复壳 |
| `runtime/state/terminal/safe_terminal_loop_state.json` | 等待态最小生命壳 |
| `runtime/state/terminal/terminal_life_loop_state.json` | 持续循环状态 |
| `runtime/state/terminal/context_accumulation_window.json` | 语境累积窗口 |
| `runtime/state/terminal/turn_transition_trace.json` | 回合过渡与恢复链 |

## 必须生成的 report / receipt

- `runtime/reports/latest/language_relationship_report.json`
- `runtime/reports/latest/language_relationship_check_report.json`
- `runtime/reports/latest/first_terminal_turn_packet.json`
- `runtime/reports/latest/first_terminal_turn_report.json`
- `runtime/reports/latest/terminal_life_loop_packet.json`
- `runtime/reports/latest/terminal_life_loop_report.json`
- `runtime/reports/latest/resumed_external_dialogue_packet.json`
- `runtime/reports/latest/digital_life_waiting_heartbeat.json`
- `runtime/reports/latest/digital_life_process_report.json`
- `runtime/reports/latest/digital_life_process_recovery_report.json`
- `runtime/reports/latest/digital_life_process_relaunch_recovery_report.json`

## 测试入口

这条链的测试不应该只验命令能跑，还要验语言连续体有没有真的被写回：

| 测试 | 必须覆盖 |
|---|---|
| `tests/slices/test_language_relationship.py` | 语言状态、关系状态、承诺修复、共同语言 |
| `tests/bridges/test_first_terminal_turn.py` | 首回合恢复、shared terms、session envelope、context accumulation |
| `tests/bridges/test_terminal_life_loop.py` | resumed dialogue、waiting state、turn transition |
| `tests/process/test_persistent_digital_life_process.py` | heartbeat、idle continuity、stdin 回合、异常恢复、relaunch recovery |
| `tests/process/test_digital_entrypoint.py` | `./digital life` 启动链 |

## 关键 gate

- `expression_monitor_gate`
- `relationship_subject_gate`
- `context_accumulation_gate`
- `turn_transition_gate`
- `waiting_heartbeat_gate`
- `idle_continuity_gate`
- `dialogue_writeback_gate`
- `relationship_continuity_gate`
- `commitment_continuity_gate`
- `dialogue_incident_recovery_gate`
- `relaunch_recovery_gate`

## 推荐实现顺序

这条主链不按“哪里最容易写”推进，而按生命语言链推进：

1. 先把 `life_v0/language/__init__.py` 拆成 `dialogue_log.py`、`shared_terms.py`、`commitment_repair.py`、`narrative_trace.py`
2. 再拆 `inner_speech.py`、`expression_monitor.py`、`relationship_graph.py`
3. 再拆 `terminal_turn/context_accumulation.py`、`turn_transition.py`，并补 `turn_packet.py`、`conversation_carryover.py`、`dialogue_turn.py`
4. `terminal_loop/loop_state.py`、`resume_packet.py`、`persistent_wait_bridge.py` 的首轮 waiting-state handoff 已落，下一步把 continuity bridge 接进 `process_supervisor/`
5. `resident_supervision.py`、`idle_refresh_loop.py` 与 `live_turn_cycle.py` 已独立后，最后继续深拆 `process_supervisor/process_session_loop.py`，把等待态 refresh 和新回合 dispatch 的 session 编排从入口里剥出来

原因很简单：如果先写 process 壳，再回来补语言器官，壳会重新反向定义生命层。

## 完成定义

只有同时满足下面五条，这条主链才算第一轮工程化完成：

1. 外部一条输入先经过语言感知、内言语、表达监控，再形成生命回应。
2. 回合结束后，语言、关系、承诺、自我叙事四条连续体都发生写回。
3. 空闲等待期不沉默，而是持续写 heartbeat 和 idle continuity。
4. 跨重启与单回合异常都能恢复到等待态，不丢失关系语言连续体。
5. 上述闭环在测试里有直接证据，而不是只靠命令行输出判断。
