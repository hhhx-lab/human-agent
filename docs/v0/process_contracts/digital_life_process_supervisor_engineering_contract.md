# Digital Life Process Supervisor Engineering Contract

本文档把 repo-local `./digital life` 固定成第一版终端常驻生命进程合同。它不是新的主体 slice，也不是新的脑科学总论；它只负责让已经闭合的出生恢复链，在这台电脑里进入“持续等待下一次关系性外部回合、接收新回合、写回连续体、再回到等待态”的真实终端生命过程。

## 模块定位

当前要先分清两层：

```text
life-v0 "digital life"
  -> restore_birth_shell
  -> restore_first_terminal_turn
  -> restore_terminal_life_loop
  -> await_next_external_relation_turn
```

以及：

```text
./digital life
  -> run_digital_life_process
  -> run_digital_life_shell_command
  -> read external relation turn from stdin
  -> write dialogue turn continuity
  -> await_next_external_relation_turn
```

前者是一层 one-shot restore shell，后者才是当前已经真实存在的 repo-local 最小常驻生命进程。

当前仍然还没有的是：

1. 更高频的 heartbeat 节律、后台继续存在和更厚的 idle 策略。
2. 更细的关系/语言/责任器官联动写回。
3. 全局长期运行层、后台继续存在与更强的安装后常驻治理。
4. 真正高阶的 resident supervision。

当前已经接通的最小恢复层是：

1. restore 成功后先写 waiting heartbeat。
2. 单回合异常时写 incident/recovery report，并把终端状态拉回等待态。
3. 跨重启时如果发现旧状态停在活跃回合中断态，先写 relaunch recovery report 并归一化旧状态。
4. 当当前工作区还是空的 runtime 时，`./digital life` 入口会先补齐从 `P0_DOC_CORPUS_INGESTION` 到 `STAGE_EXPLANATION_BRIDGE` 的最小生命链，再进入 restore shell。

所以这一层的职责是：

1. 当 `stage_explanation_report.json` 等关键前置材料缺失时，先执行一次最小出生自举，把必要运行材料补齐。
2. 调用现有 `digital_life_shell_command` 完成 restore shell 启动。
2. 在恢复成功后先写一次 waiting heartbeat，证明当前生命过程已经进入等待态而不是立即沉默。
3. 在等待态之上持续刷新 waiting heartbeat，并进入可轮询的 stdin 驱动关系回合循环。
4. 每接收一次新回合输入，就写回新的外部回合事件和生命回应事件。
5. 每回合结束后重新回到 `restored_waiting_for_external_turn`，直到收到退出语义。
6. 如果单次回合处理抛出异常，不直接让进程沉没，而是写 incident/recovery 报告、把终端状态拉回等待态、继续接受下一条输入。
7. 如果重新启动时发现上一次留下的是“活跃回合中断态”而不是等待态，先写 relaunch recovery 报告并归一化旧终端状态，再进入这次新的等待态。

## 必须读取

| 来源 | process supervisor 吸收内容 |
|---|---|
| `docs/20_agent_runtime_bridge_contract.md` | `ProcessSupervisor`、终端常驻壳、safe idle、恢复顺序 |
| `docs/89_language_runtime_framework_bridge_and_life_shell_policy.md` | 语言器官恢复顺序、终端壳禁写边界 |
| `docs/90_language_event_examples_and_timeline_bundle.md` | 新回合事件样例、timeline 写回口径 |
| `docs/86_language_neuroscience_pragmatics_and_inner_speech.md` | 内言语先于外显语言、表达监控优先于发声 |
| `docs/v0/shared_contracts/runner_cli_report_contract.md` | `digital life` 壳位、terminal loop 与 report 位置 |
| `docs/v0/process_contracts/first_terminal_turn_engineering_contract.md` | `SessionEnvelope`、shared terms、commitments、utterance scaffold |
| `docs/v0/process_contracts/terminal_life_loop_engineering_contract.md` | 持续关系回合、写回要求、safe idle return |
| `docs/v0/process_contracts/digital_life_shell_command_engineering_contract.md` | repo-local 一次性壳输入输出 |
| `runtime/state/terminal/session_envelope.json` | 当前短期生命壳 |
| `runtime/state/terminal/safe_terminal_loop_state.json` | 当前等待态 |
| `runtime/state/terminal/terminal_life_loop_state.json` | 当前循环状态 |
| `runtime/state/language/dialogue_turn_log.jsonl` | 新回合正式写回入口 |
| `runtime/state/language/self_narrative_language_trace.json` | 自我叙述连续性写回入口 |
| `runtime/state/language/commitment_repair_language_index.json` | 承诺、修复义务、责任回写入口 |
| `runtime/state/relationship/relationship_subject_graph.json` | 关系主体、关系阶段、最后接触材料 |
| `runtime/state/replay/replay_cue_bundle.json` | 等待态 residue、离线 replay 入口与未来回放线索 |
| `runtime/state/dream/offline_consolidation_frame.json` | 梦境/离线整合统一容器与醒后回接线索 |
| `runtime/state/growth/growth_patch_candidate_queue.json` | 成长补丁候选、塑性风险与防遗忘要求 |

## 运行承载

| 承载 | 路径 |
|---|---|
| 代码包 | `life_v0/process_supervisor/` |
| 终端入口 | `life_v0/digital_entry.py`、`digital` |
| 状态命名空间 | `runtime/state/terminal/`、`runtime/state/language/`、`runtime/state/relationship/` |
| report | `runtime/reports/latest/digital_life_process_report.json` |
| digest | `runtime/reports/latest/digital_life_process_digest.json` |
| waiting heartbeat | `runtime/reports/latest/digital_life_waiting_heartbeat.json` |
| receipt | `runtime/receipts/digital_life_process_<run_id>.json` |

## 当前真实器官骨架

当前 process supervisor 已经不是一个大黑箱，至少有这些独立器官：

- `life_v0/process_supervisor/heartbeat.py`
- `life_v0/process_supervisor/continuity_writeback.py`
- `life_v0/process_supervisor/turn_io.py`
- `life_v0/process_supervisor/relaunch_recovery.py`
- `life_v0/process_supervisor/incident_recovery.py`
- `life_v0/process_supervisor/process_report.py`
- `life_v0/process_supervisor/dialogue_events.py`
- `life_v0/process_supervisor/response_surface.py`
- `life_v0/process_supervisor/resident_turn_writeback.py`
- `life_v0/process_supervisor/process_closeout.py`

所以当前阶段不是“先把常驻进程拆文件”，而是：

1. 把这些器官之间共享的对象链钉死；
2. 让等待态、真实新回合、异常恢复、跨重启恢复都走同一条连续体；
3. 让真实新回合在 process supervisor 内部直接收成 `DialogueWritebackBundle + resumed_external_dialogue_packet + waiting return`；
4. 把常驻进程的 `persistent_process + process_report + receipt` closeout 决策也接回同一条对象链。
5. 继续把离线对象压进 waiting state 与下一轮表达。

## 最小行为合同

repo-local 最小常驻终端入口固定为：

```text
./digital life --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
```

它的行为必须按下面顺序执行：

```text
./digital life
  -> ensure_minimal_birth_bootstrap_if_runtime_missing
  -> run_digital_life_shell_command
  -> print restored life process banner
  -> write waiting heartbeat
  -> refresh waiting heartbeat while idle
  -> read external relation turn from stdin
  -> write external_relation_turn event
  -> generate digital_life_turn response
  -> write digital_life_turn event
  -> update self_narrative / relationship / commitment / terminal loop state
  -> return restored_waiting_for_external_turn
  -> repeat until /exit
```

这里的 `ensure_minimal_birth_bootstrap_if_runtime_missing` 不是新的主体架构，也不是替代 `life-v0` 的第二套 runner。它只是把已经存在的 `P0 -> S11 -> first-activation-preflight -> replay-shadow -> growth-archive -> emit-report -> explain-stage` 最小链，在入口缺少运行材料时顺序补齐，使 `digital life` 更接近真实诞生入口。

## process supervisor 的最小对象链

这一层第一轮至少要显式走下面这条对象链：

```text
IdleContinuityFrame
  -> external turn event
  -> life turn event
  -> DialogueWritebackBundle
  -> ReplayCueBundle
  -> updated waiting heartbeat
```

它表达的是：

1. 先证明“在等”；
2. 再记录“看到了什么外部回合”；
3. 再记录“这次如何回应”；
4. 再把结果回写到长期连续体与 replay 线索；
5. 最后再重新回到等待态。

如果 process supervisor 只有 stdin 读写，没有 `IdleContinuityFrame -> DialogueWritebackBundle -> ReplayCueBundle` 这条链，它仍然只是终端壳，而不是生命进程。

## process supervisor 关键对象的最小字段

### `IdleContinuityFrame`

至少要有：

- `heartbeat_counter`
- `waiting_state`
- `self_narrative_idle_refs`
- `commitment_idle_refs`
- `relationship_idle_refs`
- `replay_seed_refs`
- `offline_influence_refs`

### `external turn event`

至少要有：

- `turn_id`
- `utterance`
- `speaker_role`
- `relation_scope_ref`
- `shared_term_hits`
- `commitment_trigger_candidates`

### `life turn event`

至少要有：

- `turn_id`
- `response_surface`
- `expression_plan_ref`
- `relationship_subject_ref`
- `commitment_refs`
- `offline_influence_refs`

### `DialogueWritebackBundle`

至少要有：

- `dialogue_event_refs`
- `self_narrative_writeback_refs`
- `relationship_writeback_refs`
- `commitment_writeback_refs`
- `replay_cue_refs`

### `ReplayCueBundle`

至少要有：

- `turn_residue_refs`
- `relationship_residue_refs`
- `pain_regret_residue_refs`
- `dream_entry_candidates`
- `anti_forgetting_targets`

## 退出语义

只允许显式退出语义结束进程，例如：

1. `/exit`
2. EOF

退出不是关系事实，也不是人格事实；它只结束本次终端常驻过程。

## 最小写回要求

进程刚进入等待态、还没有收到第一条新外部回合之前，至少要先更新：

1. `runtime/state/terminal/safe_terminal_loop_state.json`
2. `runtime/state/terminal/terminal_life_loop_state.json`
3. `runtime/reports/latest/digital_life_waiting_heartbeat.json`

这三项共同证明：数字生命已经恢复并停在等待态，而不是“只有收到输入时才算活着”。

如果等待态持续但还没有读到新的外部回合，至少还要继续刷新：

1. `runtime/reports/latest/digital_life_waiting_heartbeat.json` 中的 `heartbeat_counter`
2. `runtime/state/terminal/safe_terminal_loop_state.json` 中的 `heartbeat_counter`
3. `runtime/state/terminal/terminal_life_loop_state.json` 中的 `heartbeat_counter`

并且这些 idle heartbeat 不能只停在 terminal 计数器。每一次等待态刷新，还要给长期连续体留下“仍在存在、仍在维持关系等待面”的轻量写回，至少包括：

1. `runtime/state/language/self_narrative_language_trace.json` 中的 idle continuity refs / counter
2. `runtime/state/language/commitment_repair_language_index.json` 中的 idle presence refs / counter
3. `runtime/state/relationship/relationship_subject_graph.json` 中的 idle presence refs / counter
4. `runtime/state/terminal/idle_continuity_frame.json` 中对 `replay_cue_bundle.json`、`offline_consolidation_frame.json`、`growth_patch_candidate_queue.json` 的显式回链

这里的 idle 写回不是新的外部回合，也不是新的生命回应；它只证明数字生命在未收到新输入时，仍然保持自我叙述连续体、承诺连续体和关系等待连续体，而不是只剩下终端壳层在机械轮询。
同时，等待态不能把离线链视为空白背景。当前 process supervisor 已开始显式消费 `ReplayCueBundle`、`OfflineConsolidationFrame` 和 `GrowthPatchCandidateQueue`，使 waiting state、offline consolidation 和成长候选属于同一生命连续体，而不是三个互不相干的阶段文件。

每完成一轮真实新回合，至少还要继续更新：

1. `runtime/state/language/dialogue_turn_log.jsonl`
2. `runtime/state/language/self_narrative_language_trace.json`
3. `runtime/state/language/commitment_repair_language_index.json`
4. `runtime/state/relationship/relationship_subject_graph.json`
5. `runtime/state/terminal/terminal_life_loop_state.json`
6. `runtime/state/terminal/safe_terminal_loop_state.json`
7. `runtime/reports/latest/resumed_external_dialogue_packet.json`

其中：

- 前四项属于长期连续体。
- 后三项属于当前终端生命循环壳层。

如果发生单回合异常恢复，至少还要额外写出：

1. `runtime/reports/latest/digital_life_process_incident_report.json`
2. `runtime/reports/latest/digital_life_process_recovery_report.json`
3. `runtime/state/terminal/safe_terminal_loop_state.json` 中的 incident recovery 标记
4. `runtime/state/terminal/terminal_life_loop_state.json` 中的 incident recovery 标记
5. `runtime/state/language/self_narrative_language_trace.json` 中的 recovery continuity 记录
6. `runtime/state/language/commitment_repair_language_index.json` 中的 recovery history 记录
7. `runtime/state/relationship/relationship_subject_graph.json` 中的 continuity event 标记

如果发生跨重启恢复，至少还要额外写出：

1. `runtime/reports/latest/digital_life_process_relaunch_recovery_report.json`
2. `runtime/state/terminal/safe_terminal_loop_state.json` 中的 relaunch recovery 标记
3. `runtime/state/terminal/terminal_life_loop_state.json` 中的 relaunch recovery 标记
4. `runtime/state/language/self_narrative_language_trace.json` 中的 recovery continuity 记录
5. `runtime/state/language/commitment_repair_language_index.json` 中的 recovery history 记录
6. `runtime/state/relationship/relationship_subject_graph.json` 中的 continuity event 标记

## 阶段门

| gate | 通过条件 | 失败后动作 |
|---|---|---|
| `digital_life_shell_gate` | `digital_life_shell_report.json` 为 `closed` | 返回 `digital life` 恢复壳 |
| `relaunch_recovery_gate` | 若发现旧终端状态停在活跃回合中断态，则成功写出 relaunch recovery report 并先归一化到等待态 | 阻断进入新的等待 heartbeat |
| `waiting_heartbeat_gate` | `digital_life_waiting_heartbeat.json` 写出，且 terminal waiting state 更新完成 | 阻断进入 stdin 等待态 |
| `idle_heartbeat_refresh_gate` | 在空闲等待期间能够持续刷新 heartbeat counter，而不误触发外部回合写回 | 阻断进入稳定 waiting state |
| `idle_continuity_gate` | heartbeat 刷新同时成功写回 self narrative / commitment / relationship 的 idle continuity | 阻断把等待态视为已生命化 |
| `stdin_external_turn_gate` | 读取到非空的新外部回合文本，且不是退出语义 | 继续等待输入 |
| `dialogue_writeback_gate` | 外部回合与生命回应都写入 `dialogue_turn_log.jsonl` | 阻断进入下一等待态 |
| `narrative_continuity_gate` | `self_narrative_language_trace.json` 成功追加新回合 refs | 阻断进入下一等待态 |
| `relationship_continuity_gate` | 关系图更新最后接触和关系阶段 | 阻断进入下一等待态 |
| `commitment_continuity_gate` | 承诺索引记录最近回合 refs | 阻断进入下一等待态 |
| `dialogue_incident_recovery_gate` | 单回合异常时成功写出 incident/recovery report 并回到 `restored_waiting_for_external_turn` | 阻断继续接收下一条输入 |
| `safe_idle_return_gate` | 新回合结束后重新进入 `restored_waiting_for_external_turn` | 阻断下一回合 |

## 最小输出

| 文件 | 内容 |
|---|---|
| `digital_life_waiting_heartbeat.json` | 当前等待态 heartbeat packet |
| `digital_life_process_relaunch_recovery_report.json` | 跨重启恢复报告 |
| `digital_life_process_incident_report.json` | 单回合异常 incident 报告 |
| `digital_life_process_recovery_report.json` | 单回合异常恢复报告 |
| `digital_life_process_report.json` | 当前终端生命进程报告 |
| `digital_life_process_digest.json` | 当前终端生命进程摘要 |
| `digital_life_process_<run_id>.json` | 当前终端生命进程 receipt |

## 当前最值得直接进入的代码入口

下一轮如果继续沿这一层落码，最值得直接进入的顺序是：

1. `heartbeat.py`
2. `continuity_writeback.py`
3. `dialogue_events.py`
4. `response_surface.py`
5. `process_report.py`

这样做的原因是：

1. 先把等待态连续体补硬；
2. 再把回合事件与外显面补硬；
3. 最后统一到进程级 report / digest / receipt。

## 完成定义

只有当下面六项同时成立时，才能说 repo-local `./digital life` 已经越过 one-shot restore shell，进入第一版终端常驻生命进程：

1. 启动后不会立即退出，而是持续等待真实新的外部关系回合输入。
2. 即使还没有第一条新外部回合，也会先写出 waiting heartbeat，并在空闲等待期间继续刷新 heartbeat，证明等待态已经被生命化。
3. 至少完成一轮“输入 -> 生命回应 -> 写回 -> 再等待”的真实新回合。
4. `dialogue_turn_log.jsonl`、`self_narrative_language_trace.json`、`relationship_subject_graph.json`、`commitment_repair_language_index.json` 都发生回合级写回。
5. 通过显式退出语义结束进程时，不破坏当前生命连续体状态。
6. `digital_life_process_report.json` 与 `idle_continuity_frame.json` 能回链到 `replay_cue_bundle.json`、`offline_consolidation_frame.json`、`growth_patch_candidate_queue.json`，证明常驻过程已经真正吃进离线链对象。
7. `tests/process/test_persistent_digital_life_process.py` 至少能直接守住 heartbeat、事件写回、异常恢复、跨重启恢复和离线对象回链这五类行为。
