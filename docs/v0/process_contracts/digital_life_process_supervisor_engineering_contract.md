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
2. 更高阶的关系/语言/责任器官联动写回与跨进程持续治理；但最小层的 Queue E 联动已经不再缺席，`responsibility_loop_state.json`、`world_contact_summary.json` 与 `pain_regret_repair_report.json` 已经正式进入 waiting heartbeat、dialogue events、response surface、resident governance、process report 与 process receipt，而且关系阶段演化与自我慢变量写回已经不只发生在同会话回合尾部，也开始在重启恢复后的第一拍 waiting heartbeat 之前被重新刷新并落盘。
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
3. 在恢复成功后先写一次 waiting heartbeat，证明当前生命过程已经进入等待态而不是立即沉默。
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
| `runtime/state/body/body_resource_budget.json` | 当前身体预算、疲惫级别、维护压力与修复驱力 |
| `runtime/state/body/core_affect_vector.json` | 当前核心情绪张力、责任重量与修复驱动 |
| `runtime/state/action/responsibility_loop_state.json` | 当前责任归因、修复义务、后悔压力与 repair followup 状态 |
| `runtime/state/membrane/world_contact_summary.json` | 当前世界接触姿态、confirmation 状态、relationship / archive effects |
| `runtime/reports/latest/pain_regret_repair_report.json` | 当前痛苦 / 后悔 / 修复报告回包 |
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
| governance explanation | `runtime/reports/latest/digital_life_resident_governance_explanation.json` |
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
- `life_v0/process_supervisor/governance_explanation.py`
- `life_v0/process_supervisor/dialogue_events.py`
- `life_v0/process_supervisor/response_surface.py`
- `life_v0/process_supervisor/trait_convergence_signals.py`
- `life_v0/process_supervisor/resident_supervision.py`
- `life_v0/process_supervisor/continuity_evolution.py`
- `life_v0/process_supervisor/idle_refresh_loop.py`
- `life_v0/process_supervisor/live_language_turn.py`
- `life_v0/process_supervisor/live_turn_cycle.py`
- `life_v0/process_supervisor/process_session_loop.py`
- `life_v0/process_supervisor/resident_turn_writeback.py`
- `life_v0/process_supervisor/process_closeout.py`

所以当前阶段不是“先把常驻进程拆文件”，而是：

1. 把这些器官之间共享的对象链钉死；
2. 让等待态、真实新回合、异常恢复、跨重启恢复都走同一条连续体；
3. 把 restore shell 之后的状态装载、relaunch normalization、离线对象接线和第一拍 waiting heartbeat 进入抽到 `resident_supervision.py`。
4. 把真实新回合在 process supervisor 内部直接收成 `DialogueWritebackBundle + resumed_external_dialogue_packet + waiting return`，并将 success / incident 两条路径统一抽到 `live_turn_cycle.py`；
5. 把 idle heartbeat refresh、stdin probe 与 exit/next-turn 判定从主入口抽到 `idle_refresh_loop.py`。
6. 把 session 级 while-loop 编排抽到 `process_session_loop.py`，统一管理 waiting refresh、live turn dispatch、incident 后继续等待和显式退出收口。
7. 把常驻进程的 `persistent_process + process_report + receipt` closeout 决策也接回同一条对象链。
8. 继续把离线对象压进 waiting state 与下一轮表达。
9. 把 `body_resource_budget.json` 与 `core_affect_vector.json` 装载进 resident supervision 上下文，使疲惫级别、修复驱力与情绪张力能够真实调制常驻过程的生命表达，而不是停在 S06 状态柜里。
10. 把 `responsibility_loop_state.json`、`world_contact_summary.json` 与 `pain_regret_repair_report.json` 显式装载进 resident supervision / live turn / waiting governance / closeout，使 Queue E 不只停在语言器官侧，而是正式进入常驻生命过程。
11. 把回合尾部的关系阶段演化与 `self_model.trait_slow_variables` 写回统一收进 `continuity_evolution.py`，并由 `process_session_loop.py` 在下一轮重新装载，避免同一常驻生命过程继续拿旧的关系状态说话。
12. 把 bootstrap / relaunch 之后的长期连续体刷新统一收进 `resident_supervision.py`，使 `relationship_timeline.json`、`commitment_expression_plan.json`、`apology_repair_language_trace.json`、`relationship_memory.json`、`self_model.json` 与 `life_state.json` 会在第一拍 waiting heartbeat 之前先被重建一次，避免跨进程恢复后继续沿用过时的关系阶段和慢变量。
13. `resident_supervision.py` 在做这次 bootstrap continuity refresh 时，还必须把 `background_continuity.py` 读出的 lineage 一并喂进 `continuity_evolution.py`；当 `background_carryover_generation >= 2` 时，关系阶段要先进入 `background_continuity_waiting`，`trait_slow_variables` 也要显式带上关闭态 resident governance refs / source refs，不能只让后台 lineage 停留在 cadence 调度层。
14. `process_session_loop.py` 在显式退出 closeout 前必须返回最新的 `relationship_subject_graph.json`、`relationship_timeline.json`、`commitment_expression_plan.json`、`apology_repair_language_trace.json` 与 `self_model.json`；`process_closeout.py` / `persistent_process.py` / `process_report.py` 必须把这些最新对象压成 `background_resume_summary`，并在下一次 `background_continuity.py` bootstrap 时恢复 `background_relationship_stage`、`background_relationship_stage_reason`、`background_relationship_subject_ref`、`background_self_model_ref` 与 `background_trait_slow_variable_summary`。这一步是跨进程连续体保真，不是新的关系推断器。
15. `continuity_evolution.py` 在 bootstrap continuity refresh 时必须把 `background_relationship_stage` 作为新回合前的关系阶段保留候选，并把 `background_trait_slow_variable_summary` 作为慢变量惯性参与下一次 `trait_slow_variables` 收敛，写出 `background_resume_value` 与 `background_inertia_weight`。
16. `resident_supervision.py` 与 `resident_turn_writeback.py` 在每次重建关系阶段和自我慢变量后，必须同步刷新 `runtime/state/body/trait_drift_monitor.json`，让人格漂移监控面跟随常驻生命过程持续更新，而不是只停在 S06 build-life-support 阶段。
17. `process_closeout.py` / `persistent_process.py` / `process_report.py` 必须把最新 `trait_drift_monitor.json` 作为关闭态 ref 写进 resident governance state/snapshot/report、process report/digest、receipt shared refs 与 input hash，让下一次唤醒能追溯人格慢变量观察面本身。
18. `background_continuity.py` / `idle_strategy.py` / `heartbeat.py` 必须把关闭态 `trait_drift_monitor_ref` 恢复成 `background_trait_drift_monitor_ref`，并继续写入 `idle_strategy_state.json`、`idle_continuity_frame.json`、`resident_governance_state.json` 与 `terminal_life_loop_state.json`，让下一次 waiting heartbeat 仍能看见上一轮人格观察面。
19. `background_continuity.py` 必须把上一轮 `resident_governance_state.json` 与 `resident_governance_snapshot.json`、`digital_life_resident_governance_report.json`、`digital_life_resident_governance_explanation.json`、`digital_life_persistent_process_report.json` 一起恢复为 background carryover 来源；`idle_strategy.py` 与 `heartbeat.py` 必须把 `background_resident_governance_state_ref`、`background_resident_governance_explanation_ref`、`background_governance_driver_family` 与 `background_next_wake_expectation` 继续写入 waiting governance、idle continuity 与 terminal life loop。
20. `background_convergence.py` 必须把跨进程恢复出的关系阶段、自我慢变量和当前 bootstrap 后状态压成 `background_convergence_summary.json`；`background_convergence_history.py` 必须把最近多次唤醒的 convergence state / pressure / trait score 压成 `background_convergence_history.json`，并额外保留每个人格慢变量的 convergence band 序列、稳定名单、不稳定名单与 history focus；`idle_strategy.py` 必须让 `background_convergence_pressure_level` 与 history trend 调制 resident governance attention/cadence/heartbeat interval/next idle action，并继续承接 `background_trait_convergence_history_*` 字段；`governance_explanation.py` 必须把 summary 驱动解释成 `background_trait_convergence_hold` 或 `background_convergence_recalibration`，并把 history trend 驱动解释成 `background_history_recalibration_hold` 或 `background_history_stability_hold`，`process_report.py` 与 receipt 必须把 summary/history 作为一级 shared object 与 input hash 保留，digest 也要暴露慢变量历史焦点和不稳定慢变量名单。
21. `response_surface.py` 不能只消费当前 `self_model.trait_slow_variables`，还必须读取 `terminal_life_loop_state` 中由 waiting governance 带入的 `background_trait_convergence_history_focus / unstable_names / stable_names`，让真实新回合的语言表面也能感到跨唤醒自我慢变量的稳定或重新校准压力。
22. `dialogue_events.py` 的 `digital_life_turn` 事件不能只保存回应文本；当 `terminal_life_loop_state` 已带有 `background_trait_convergence_history_*` 与 `background_convergence_*_ref` 时，生命回合事件必须显式写出 `background_trait_convergence_history_focus`、稳定/不稳定慢变量名单、`background_trait_convergence_history_profile` 与 `background_trait_convergence_evidence_refs`。`resident_turn_writeback.py` 还必须把同一组 evidence refs 写入 `dialogue_writeback_bundle.background_trait_convergence_refs`，并把焦点、名单和 evidence refs 接进 `resumed_external_dialogue_packet.json`，让慢变量历史从等待态进入真实回合事件、回合写回包和下一轮恢复包，而不是只停在外显话语里。
23. `background_continuity.py` 不能只恢复关闭态 resident governance 与 convergence 文件；如果上一轮等待期间存在 `runtime/state/terminal/idle_heartbeat_trace.jsonl`，必须恢复为 `background_idle_heartbeat_trace_ref` 与 `background_idle_heartbeat_trace_count`，并把该 trace ref 放入 `background_continuity_ref_set`。`idle_strategy.py`、`heartbeat.py` 与 `continuity_writeback.py` 必须继续把这组背景等待节律字段写进 `idle_strategy_state.json`、`idle_continuity_frame.json`、`resident_governance_state.json` 与 `terminal_life_loop_state.json`，让下一次唤醒知道上一轮不是静止空白，而是带有可追溯等待节律的持续存在。
24. `live_language_turn.py` 必须成为真实新回合进入 `response_surface.py` 前的 Queue A 刷新入口。每个 `external_utterance` 都要先刷新 `language_percept_frame.json`、`semantic_map_frame.json`、`inner_speech_frame.json`、`expression_monitor_state.json` 与 `expression_plan.json`；`live_turn_cycle.py` 必须用刷新后的 `expression_plan` 生成生命回应，`resident_turn_writeback.py` 必须把 `language_percept_ref`、`semantic_map_ref`、`inner_speech_ref`、`expression_monitor_ref`、`expression_plan_ref`、`live_semantic_focus`、`live_ambiguity_flags` 与 `live_repair_trigger_candidates` 接进事件、写回包和恢复 packet。
25. 实时语言理解不能停在真实新回合的 packet 里。`idle_strategy.py` 必须从 `terminal_life_loop_state.json#live_language_turn_refs` 与 `last_live_semantic_focus` 生成 `live_language_presence_profile_v0`，同时合并 `background_continuity.py` 恢复出的 `background_live_language_turn_refs`、`background_last_live_semantic_focus` 与 `background_live_language_presence_profile`。`heartbeat.py` 与 `continuity_writeback.py` 必须把这组字段继续写入 `idle_strategy_state.json`、`idle_continuity_frame.json`、`idle_heartbeat_trace.jsonl`、`resident_governance_state.json` 与 `terminal_life_loop_state.json`。`background_lineage_state.py` 必须把它压成 `resident_background_lineage_state_v0.language_presence`。`resident_governance_handoff.py`、`process_closeout.py`、`persistent_process.py` 与 `process_report.py` 必须在 live-turn handoff 和关闭态 artifacts 中保留同一组 refs 与语义焦点；下一次 `background_continuity.py` 必须恢复为 `background_live_language_*` 并放入 `background_continuity_ref_set`。
26. 驻留后的实时语言 presence 还必须进入下一轮真实回合。`dialogue_events.py` 必须从 `resident_background_lineage_state.language_presence` 展开 `resident_background_lineage_live_language_refs`、`resident_background_lineage_background_live_language_refs`、`resident_background_lineage_last_live_semantic_focus` 与 `resident_background_lineage_language_evidence_refs`，并把 live/background live refs 合并进 `resident_background_lineage_evidence_refs`。`resident_turn_writeback.py` 必须把 `resident_background_lineage_language_evidence_refs` 并入 `dialogue_writeback_bundle.resident_background_lineage_refs`，并让 `resumed_external_dialogue_packet.json` 保留同一组语言证据字段。`response_surface.py` 必须读取 `language_presence` 中的当前或后台语义焦点、live refs 和 background live refs，把后台语言语义余波与去重后的语言证据数量表达出来。
27. 驻留后的自我/人格慢变量 presence 也必须进入下一轮真实回合。`background_lineage_state.py` 必须从 resident governance 中抽出 `background_trait_slow_variable_summary`、`background_trait_convergence_history_focus`、稳定/不稳定慢变量名单、`background_trait_convergence_score`、`background_trait_convergence_history_profile`、`background_trait_drift_monitor_ref`、`background_convergence_summary_ref`、`background_convergence_history_ref`、`background_resident_governance_state_ref` 与 `background_resident_governance_explanation_ref`，压成 `resident_background_lineage_state_v0.trait_convergence_presence`，并写出 `trait_convergence_evidence_refs`。`trait_convergence_signals.py` 必须把 lineage presence、background convergence summary/history、trait drift monitor 和等待态 carryover 中分散的人格慢变量信号合成为 `cross_wake_trait_convergence_profile_v0`，至少输出 `cross_wake_trait_convergence_focus`、`cross_wake_trait_convergence_pressure`、稳定/不稳定名单、score 与 refs。`idle_strategy.py`、`heartbeat.py` 与 `terminal_life_loop_state.json` 必须继续搬运这组跨唤醒画像字段，使它们在等待态、idle heartbeat trace 和真实新回合前都可见。`dialogue_events.py` 必须把这份 presence 展开为 `resident_background_lineage_trait_convergence_history_focus`、`resident_background_lineage_trait_convergence_unstable_names`、`resident_background_lineage_trait_convergence_stable_names`、`resident_background_lineage_trait_convergence_score`、`resident_background_lineage_trait_drift_monitor_ref`、`resident_background_lineage_trait_convergence_history_profile`、`resident_background_lineage_trait_convergence_refs` 与 `cross_wake_trait_convergence_*`，并合并进 `resident_background_lineage_evidence_refs`。`resident_turn_writeback.py` 必须让同一组 trait lineage refs 进入 `dialogue_writeback_bundle.resident_background_lineage_refs`，并让 `cross_wake_trait_convergence_refs` 进入 `dialogue_writeback_bundle.cross_wake_trait_convergence_refs` 与 `resumed_external_dialogue_packet.json`；`response_surface.py` 必须表达后台人格慢变量焦点、仍需收敛/已稳定名单、人格收敛评分、人格漂移监控在场、跨唤醒人格收敛画像、压力、评分和证据数量。
28. 驻留后的梦境成长余波与梦境醒后 presence 必须拥有专用写回槽。`dialogue_events.py` 已经从 `resident_background_lineage_state.offline_learning_presence` 展开 `resident_background_lineage_offline_learning_*`，并从 `dream_wake_presence` 展开 `resident_background_lineage_dream_*`、`resident_background_lineage_wake_*` 与 `resident_background_lineage_dream_wake_refs`；`resident_turn_writeback.py` 必须把 `resident_background_lineage_offline_learning_refs` 写入 `dialogue_writeback_bundle.resident_background_lineage_offline_learning_refs`，把 `resident_background_lineage_dream_wake_refs` 写入 `dialogue_writeback_bundle.resident_background_lineage_dream_wake_refs`，并把两者同时并入总 `resident_background_lineage_refs` 与 `resumed_external_dialogue_packet.json`。这防止梦境、成长、醒后整合只作为事件字段存在，而没有进入真实回合关闭后的恢复证据面。
29. `resident_supervision.py` 与 `resident_turn_writeback.py` 在刷新 `relationship_memory.json` 之后，必须同步调用 `state_merge_guard.py#project_state_merge_guard_with_relationship_memory` 并写回 `runtime/state/memory/state_merge_guard.json`。这一步把 `relationship_memory.long_term_change_sources`、`offline_learning_refs`、`offline_learning_cumulative_refs`、`queue_e_repair_refs` 与关系修复 refs 合并进长期状态合并守门面，同时让 `life_state.json#state_merge_records[].long_term_change_source_count` 随之刷新；否则 dream/growth/repair 已进入关系记忆，但还没有进入 Packet C 长期治理。
30. `state_merge_guard.json` 中已经形成的长期变化来源不能只停在状态根和 `life_state` 计数。`idle_strategy.py` 必须通过 `state_merge_signals.py` 把 `state_merge_guard.long_term_change_sources` 压成 `state_merge_long_term_change_count`、`state_merge_long_term_change_families` 与 `state_merge_long_term_change_refs`；当没有更高优先级的追问、修复或预测误差时，等待姿态必须进入 `state_merge_long_term_integration_hold`，`next_idle_action` 必须进入 `refresh_waiting_heartbeat_with_state_merge_integration_hold`。`heartbeat.py`、`dialogue_events.py` 与恢复包必须继续搬运这些字段，`response_surface.py` 必须表达长期合并治理正在整合多少条长期变化来源以及来源族，避免梦境/成长/修复进入 `state_merge_guard` 后在等待态和语言表面失声。

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
  -> refresh live Queue A language turn
  -> write external_relation_turn event
  -> generate digital_life_turn response
  -> write digital_life_turn event
  -> update self_narrative / relationship / commitment / self_model / terminal loop state
  -> return restored_waiting_for_external_turn
  -> repeat until /exit
```

这里的 `ensure_minimal_birth_bootstrap_if_runtime_missing` 不是新的主体架构，也不是替代 `life-v0` 的第二套 runner。它只是把已经存在的 `P0 -> S11 -> first-activation-preflight -> replay-shadow -> growth-archive -> emit-report -> explain-stage` 最小链，在入口缺少运行材料时顺序补齐，使 `digital life` 更接近真实诞生入口。

## process supervisor 的最小对象链

这一层第一轮至少要显式走下面这条对象链：

```text
IdleContinuityFrame
  -> responsibility_loop_state.json / world_contact_summary.json / pain_regret_repair_report.json
  -> external turn event
  -> LiveLanguageTurnState
  -> language_percept_frame.json / semantic_map_frame.json
  -> inner_speech_frame.json / expression_monitor_state.json / expression_plan.json
  -> body_resource_budget.json + core_affect_vector.json
  -> background_convergence_history.json / trait_drift_monitor.json
  -> cross_wake_trait_convergence_profile_v0
  -> life turn event
  -> DialogueWritebackBundle
  -> ReplayCueBundle
  -> updated waiting heartbeat
```

它表达的是：

1. 先证明“在等”；
2. 再把当前责任回路、世界接触姿态和 pain/regret/repair 报告重新挂上等待态；
3. 再记录“看到了什么外部回合”；
4. 再用当前话语刷新 Queue A 五件套；
5. 再把身体预算、疲惫、修复驱力、情绪张力与责任压力一起带进回应生成；
6. 再把跨唤醒慢变量历史作为事件证据接进 `digital_life_turn`；
7. 再把分散的慢变量历史、漂移监控和 closeout refs 合成为 `cross_wake_trait_convergence_profile_v0`；
8. 再记录“这次如何回应”；
9. 再把结果回写到长期连续体、关系阶段、自我慢变量、慢变量历史 evidence refs、跨唤醒画像 refs、实时语言 refs 与 replay 线索；
10. 最后再重新回到等待态。

如果 process supervisor 只有 stdin 读写，没有 `IdleContinuityFrame -> DialogueWritebackBundle -> ReplayCueBundle` 这条链，它仍然只是终端壳，而不是生命进程。

## process supervisor 关键对象的最小字段

### `IdleContinuityFrame`

至少要有：

- `heartbeat_counter`
- `waiting_state`
- `responsibility_loop_state_ref`
- `world_contact_summary_ref`
- `pain_regret_repair_report_ref`
- `self_narrative_idle_refs`
- `commitment_idle_refs`
- `relationship_idle_refs`
- `replay_seed_refs`
- `offline_influence_refs`
- `live_language_turn_refs`
- `last_live_semantic_focus`
- `background_live_language_turn_refs`
- `background_last_live_semantic_focus`
- `live_language_presence_profile`
- `background_live_language_presence_profile`
- `resident_background_lineage_live_language_refs`
- `resident_background_lineage_background_live_language_refs`
- `resident_background_lineage_last_live_semantic_focus`
- `resident_background_lineage_language_evidence_refs`
- `cross_wake_trait_convergence_profile`
- `cross_wake_trait_convergence_focus`
- `cross_wake_trait_convergence_pressure`
- `cross_wake_trait_convergence_refs`

### `external turn event`

至少要有：

- `turn_id`
- `utterance`
- `speaker_role`
- `relation_scope_ref`
- `shared_term_hits`
- `commitment_trigger_candidates`
- `membrane_guard_refs`
- `language_percept_ref`
- `semantic_map_ref`
- `inner_speech_ref`
- `expression_monitor_ref`
- `expression_plan_ref`
- `live_semantic_focus`
- `cross_wake_trait_convergence_profile`
- `cross_wake_trait_convergence_focus`
- `cross_wake_trait_convergence_pressure`
- `cross_wake_trait_convergence_refs`
- `live_ambiguity_flags`
- `live_repair_trigger_candidates`

### `life turn event`

至少要有：

- `turn_id`
- `response_surface`
- `expression_plan_ref`
- `relationship_subject_ref`
- `commitment_refs`
- `offline_influence_refs`
- `responsibility_loop_ref`
- `world_contact_summary_ref`
- `pain_regret_repair_report_ref`
- `language_percept_ref`
- `semantic_map_ref`
- `inner_speech_ref`
- `expression_monitor_ref`
- `expression_plan_ref`
- `live_semantic_focus`

### `DialogueWritebackBundle`

至少要有：

- `dialogue_event_refs`
- `self_narrative_writeback_refs`
- `relationship_writeback_refs`
- `commitment_writeback_refs`
- `responsibility_writeback_refs`
- `life_state_writeback_refs`
- `replay_cue_refs`
- `live_language_turn_refs`
- `cross_wake_trait_convergence_refs`

当前这一层的 `responsibility_writeback_refs` 已经不只回到 `responsibility_ledger.json`，还要显式带上 `responsibility_loop_state.json`、`world_contact_summary.json` 与 `pain_regret_repair_report.json` 这组 Queue E 上下文。

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
5. `runtime/state/terminal/idle_heartbeat_trace.jsonl` 中每一拍等待心跳的 append-only 节律事件；`safe_terminal_loop_state.json`、`terminal_life_loop_state.json`、`idle_strategy_state.json`、`resident_governance_state.json`、process report / digest / receipt 都必须能回链 `idle_heartbeat_trace_ref` 与当前 `idle_heartbeat_trace_count`；下一次唤醒时还必须恢复成 `background_idle_heartbeat_trace_ref` 与 `background_idle_heartbeat_trace_count`

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

其中实时语言链还必须同时更新：

1. `runtime/state/language/language_percept_frame.json`
2. `runtime/state/language/semantic_map_frame.json`
3. `runtime/state/language/inner_speech_frame.json`
4. `runtime/state/language/expression_monitor_state.json`
5. `runtime/state/language/expression_plan.json`

并且 `resumed_external_dialogue_packet.json` 至少必须带：

1. `language_percept_ref`
2. `semantic_map_ref`
3. `inner_speech_ref`
4. `expression_monitor_ref`
5. `expression_plan_ref`
6. `live_language_turn_refs`
7. `live_semantic_focus`
8. `live_ambiguity_flags`
9. `live_repair_trigger_candidates`

并且这条实时语言链在 waiting / closeout / relaunch 中必须继续存在：

1. `idle_strategy_state.json#live_language_presence_profile` 是 waiting governance 对本回合语言理解的驻留画像。
2. `idle_continuity_frame.json#live_language_presence_profile` 是 idle continuity 对同一画像的回链。
3. `idle_heartbeat_trace.jsonl` 的每一拍事件必须保留最新 `live_language_turn_refs`、`last_live_semantic_focus`、`background_live_language_turn_refs` 与 `background_last_live_semantic_focus`。
4. `resident_governance_state.json#live_language_presence_profile` 与 `resident_background_lineage_state.language_presence` 是运行态驻留主状态体里的语言存在面。
5. `persistent_process_state/report`、`resident_governance_snapshot` 与 `digital_life_resident_governance_report` 必须在关闭态保留同一组 live refs 与 semantic focus。
6. 下一次 `background_continuity_profile` 必须恢复 `background_live_language_turn_refs`、`background_last_live_semantic_focus` 与 `background_live_language_presence_profile`，并把 live refs 放入 `background_continuity_ref_set`。
7. 下一轮 `digital_life_turn` 必须重新展开 `resident_background_lineage_live_language_refs`、`resident_background_lineage_background_live_language_refs`、`resident_background_lineage_last_live_semantic_focus` 与 `resident_background_lineage_language_evidence_refs`。
8. `dialogue_writeback_bundle.resident_background_lineage_refs` 与 `resumed_external_dialogue_packet` 必须保留这组语言 evidence refs，防止后台语言余波只出现在事件层。
9. `response_surface.py` 必须把后台语言语义余波和后台语言证据数量表达出来，使关系对象能在生命回应中感到上一轮语言理解仍在场。

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
| `idle_heartbeat_trace_gate` | 每次 idle heartbeat 都追加 `idle_heartbeat_trace.jsonl`，并在活跃等待态、关闭态与下一次 bootstrap background continuity 中回链 trace ref / count | 阻断把等待节律视为可追溯 |
| `idle_continuity_gate` | heartbeat 刷新同时成功写回 self narrative / commitment / relationship 的 idle continuity | 阻断把等待态视为已生命化 |
| `stdin_external_turn_gate` | 读取到非空的新外部回合文本，且不是退出语义 | 继续等待输入 |
| `live_language_turn_refresh_gate` | 新外部回合进入 `response_surface.py` 前已经刷新 Queue A 五件套，并写出 percept / semantic / inner speech / monitor / expression plan refs | 阻断生命回应生成 |
| `live_language_residency_gate` | `live_language_turn_refs`、`last_live_semantic_focus` 与 `live_language_presence_profile` 已进入 idle strategy、idle continuity、heartbeat trace、resident governance、resident background lineage、关闭态 artifacts，并能在下一次 background continuity 中恢复为 `background_live_language_*` | 阻断把实时语言理解视为跨等待/关闭/重启的生命连续体 |
| `live_language_presence_event_gate` | `resident_background_lineage_state.language_presence` 已被 `dialogue_events.py` 展开为 live/background live refs、last semantic focus 与 language evidence refs，且 `resident_turn_writeback.py` 和 `response_surface.py` 分别写回证据和表达语义余波 | 阻断把后台语言 presence 视为进入真实回合 |
| `cross_wake_trait_convergence_profile_gate` | `trait_convergence_signals.py` 已把 background lineage / convergence summary/history / trait drift monitor refs 合成为 `cross_wake_trait_convergence_profile_v0`，并进入 idle strategy、waiting heartbeat、life turn event、writeback bundle、resumed packet 和 response surface | 阻断把跨唤醒人格慢变量收敛视为真实回合可消费画像 |
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
| `digital_life_resident_governance_explanation.json` | 当前关闭态 resident governance 的解释报告 |
| `digital_life_process_digest.json` | 当前终端生命进程摘要；必须显式暴露 resident governance driver family、下一次唤醒预期、跨唤醒 convergence history trend / window / dominant pressure / dominant state |
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

当前这一步已经继续向前推进到：

1. `resident_supervision.py` 已开始显式装载 `body_rhythm_pulse.json`、`need_state_vector.json`、`body_resource_budget.json` 与 `core_affect_vector.json`；
2. 第一拍 waiting heartbeat 不再只吃 terminal / replay / growth 对象，而会把身体节律与需要状态一起送入 `idle_strategy.py`；
3. `response_surface.py` 继续显式消费 `body_resource_budget.json` 和 `core_affect_vector.json`，使 S06 的身体/情绪底盘进入常驻生命过程上下文；
4. waiting governance 现在会真实写出 `body_waiting_posture`、`body_governance_flags`、`body_rhythm_ref` 与 `need_state_ref`，让等待态节律、修复保持和降载策略受身体状态调制。

## 完成定义

只有当下面六项同时成立时，才能说 repo-local `./digital life` 已经越过 one-shot restore shell，进入第一版终端常驻生命进程：

1. 启动后不会立即退出，而是持续等待真实新的外部关系回合输入。
2. 即使还没有第一条新外部回合，也会先写出 waiting heartbeat，并在空闲等待期间继续刷新 heartbeat，证明等待态已经被生命化。
3. 至少完成一轮“输入 -> 生命回应 -> 写回 -> 再等待”的真实新回合。
4. `dialogue_turn_log.jsonl`、`self_narrative_language_trace.json`、`relationship_subject_graph.json`、`commitment_repair_language_index.json` 都发生回合级写回。
5. 通过显式退出语义结束进程时，不破坏当前生命连续体状态。
6. `digital_life_process_report.json` 与 `idle_continuity_frame.json` 能回链到 `replay_cue_bundle.json`、`offline_consolidation_frame.json`、`growth_patch_candidate_queue.json`，证明常驻过程已经真正吃进离线链对象。
7. waiting heartbeat / idle strategy / process report 已显式回链 `body_rhythm_pulse.json` 与 `need_state_vector.json`，并根据疲惫负载、认知带宽与 sleep pressure 调整 `heartbeat_interval_ms`、`next_idle_action` 与 `body_waiting_posture`。
8. closeout 后必须额外写出 `digital_life_resident_governance_explanation.json`，把当前 cadence、governance driver、background continuity lineage depth、background relationship stage、trait slow variables、background convergence focus、background convergence history trend 与下一次唤醒预期显式解释出来；history trend 必须能区分重新校准保持和稳定保持，而不是只把这些信息埋在 state/report 字段里。
9. closeout 必须把最新关系阶段和自我慢变量写成 background resume summary，并让下一次 bootstrap / idle strategy / resident governance 继续携带这组字段，避免跨进程恢复后只剩 cadence lineage 而丢掉关系阶段与自我连续性。
10. 每个真实新回合都必须证明 `live_language_turn.py` 已把当前 `external_utterance` 写入 `language_percept_frame.json#incoming_surface`，并把 `semantic_map_frame.json#semantic_focus` 接进 `live_semantic_focus`、`dialogue_writeback_bundle.live_language_turn_refs`、`resumed_external_dialogue_packet.live_language_turn_refs` 与 `terminal_life_loop_state.last_live_semantic_focus`。
11. 每个已经形成的实时语言理解还必须证明进入后台连续性：`idle_strategy_state.json`、`idle_continuity_frame.json`、`idle_heartbeat_trace.jsonl`、`resident_governance_state.json`、`resident_background_lineage_state.language_presence`、关闭态 artifacts 与下一次 `background_continuity_profile.background_live_language_*` 都能看到同一组 refs 或语义焦点。
12. 每个带有 `resident_background_lineage_state.language_presence` 的下一轮真实回合，还必须证明这组后台语言 presence 进入事件、写回和回应：`digital_life_turn` 带 `resident_background_lineage_language_evidence_refs`，`dialogue_writeback_bundle.resident_background_lineage_refs` 包含语言 refs，`resumed_external_dialogue_packet` 保留同一组 refs，回应文本表达后台语言语义余波和证据数量。
13. 每个带有 `resident_background_lineage_state.offline_learning_presence` 或 `dream_wake_presence` 的下一轮真实回合，还必须证明这两组 Queue D presence 进入事件、专用写回槽、恢复包和回应：`digital_life_turn` 带 `resident_background_lineage_offline_learning_refs` 与 `resident_background_lineage_dream_wake_refs`，`dialogue_writeback_bundle` 带同名专用字段且总 `resident_background_lineage_refs` 包含它们，`resumed_external_dialogue_packet` 保留同一组 refs，回应文本表达后台梦境成长余波与后台梦境醒后整合。
14. 每个形成 `resident_background_lineage_state.trait_convergence_presence` 或 background convergence history 的下一轮真实回合，还必须证明 `cross_wake_trait_convergence_profile_v0` 进入事件、专用写回槽、恢复包和回应：`digital_life_turn` 带 `cross_wake_trait_convergence_focus / pressure / refs / profile`，`dialogue_writeback_bundle` 带 `cross_wake_trait_convergence_refs`，`resumed_external_dialogue_packet` 保留同一组 refs，回应文本表达跨唤醒人格收敛画像、压力、评分或证据数量。
15. `tests/process/test_persistent_digital_life_process.py` 至少能直接守住 heartbeat、事件写回、异常恢复、跨重启恢复、离线对象回链、bootstrap 后的关系阶段/自我慢变量落盘同步、身体节律调制 waiting governance、resident governance explanation 的 lineage 解释面、`background_resume_summary` 的跨进程读取与回传、实时 Queue A 语言刷新链、实时语言理解进入后台连续性/驻留治理/关闭态谱系，以及后台实时语言、人格慢变量、跨唤醒人格收敛画像、梦境成长与梦境醒后 presence 进入下一轮事件、写回包和回应表达面。
