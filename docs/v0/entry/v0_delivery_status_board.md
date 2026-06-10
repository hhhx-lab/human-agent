# V0 Delivery Status Board

本文档只负责表达当前现实工程状态，不重写总索引，也不重写 `00-258` 映射。

它只回答三件事：

1. 现在已经真实跑到哪里。
2. 当前最该补的是哪一段。
3. 下一轮从哪一包文档、代码和 runtime 产物直接开工。

这份状态板只负责“定前沿、定优先级、定开工包”。如果你需要的是总索引、理论映射或模块合同，请回别的入口文件，不要让状态板承担所有事情。

这里提到的 runtime 产物，默认都是“当前工作区最近一次相关命令运行后生成的权威产物”。如果本地还没生成 `runtime/`，说明你还没把这一轮运行证据跑出来，不代表状态板写错了。

## 用这份状态板时只做什么

每次回仓库，状态板只帮你做三件事：

1. 判断当前真实前沿到底停在主体 slice、链尾桥接段，还是外层常驻过程。
2. 判断下一轮优先补哪一段，而不是把整个体系重新复盘一遍。
3. 判断这轮需要回到 `entry/v0_module_execution_catalog.md` 的哪一柜去拿开工包。

如果你已经知道要改哪个模块，就不要在这份状态板里久留，直接回模块目录。

## 这份状态板不吸收什么

后续不要把任何新信息都写进状态板。它默认不吸收下面几类内容：

1. `00-258` 的总映射变化。
2. `docs/v0/*` 的分层变化。
3. 某个合同的字段级细节变化。
4. 某个模块完整开工包的明细变化。

这些内容分别应该回到映射层、总索引、合同原文和 `entry/v0_module_execution_catalog.md`。

## 当前三层现实

### 1. 当前内部最远命令位

```text
life-v0 terminal-life-loop --strict
```

当前已闭合的内部链尾是：

```text
life-v0 emit-report --strict
  -> life-v0 explain-stage --strict
  -> life-v0 digital-life --strict
  -> life-v0 first-terminal-turn --strict
  -> life-v0 terminal-life-loop --strict
```

当前工程口径下，`first_activation_return_packet.json` 仍然承担 terminal birth restore packet 的角色。

### 2. 当前外层命令面

当前 repo-local 外层命令面已经分成三层：

| 命令面 | 真实作用 | 当前状态 |
|---|---|---|
| `life-v0 digital-life --strict` | 内部出生壳 | `已落最小代码` |
| `life-v0 "digital life" --strict` | repo-local one-shot restore shell | `已落最小代码` |
| `./digital life --strict` | repo-local 最小常驻终端生命进程；若缺最小 runtime 材料会先自举出生链，再恢复并进入等待态 | `已落最小代码` |

这里还要再补一条口径：

1. `stage_explain` 当前写出的 `next_required_command` 仍然是 `digital life`。
2. 这是一条外层 handoff token，不等于“仓库里还没有外层入口”。
3. 当前真正需要继续补厚的是 `./digital life` 这层最小常驻生命进程，而不是再去重复发明一个新的命令名字。

### 3. 当前真正未完成的前沿

当前真正还没完成的是：

0. `00-257` 的基础理论主干已经闭合，当前缺口主要是工程对象化、文件级器官化、runtime 证据和常驻存在治理，而不是继续线性扩写新的总论。
1. `digital_life_macro_architecture_v0.md`、`runtime_v0_architecture.md`、`s06_life_support_development_engineering_contract.md`、`s08_life_target_runtimes_engineering_contract.md` 这一轮已经补到更硬的工程合同级别：当前真实代码骨架、对象链、关键字段、测试入口和第一轮完成定义都已写明。接下来进代码时，不再把它们当“概念文档”，而要当施工合同使用。
2. `DIGITAL_LIFE_PROCESS_SUPERVISOR` 已有最小代码闭合，waiting heartbeat、单回合 incident recovery 和 relaunch recovery normalization 已经接通；等待态 heartbeat 已开始向 self narrative / commitment / relationship 连续体做轻量写回，并且已开始显式消费 `ReplayCueBundle`、`OfflineConsolidationFrame` 与 `GrowthPatchCandidateQueue` 三个离线共享对象，把它们重新带回 idle continuity 与 process report。现在又进一步推进到：下一轮生命表达已经会显式携带离线重放线索、梦境整合窗口和成长补丁候选，并且 `resident_supervision.py` 已把 restore shell 之后的状态装载、relaunch normalization、离线对象接线和第一拍 waiting heartbeat 进入独立成器官；`live_turn_cycle.py` 又把真实新回合的 success / incident 生命周期独立成器官；`process_session_loop.py` 则把 waiting heartbeat refresh 与 live turn dispatch 的 session 编排继续下沉；`heartbeat.py` 与 `persistent_process.py` 现在又把常驻治理分成运行中的 `runtime/state/terminal/resident_governance_state.json` 和关闭态 `runtime/state/terminal/resident_governance_snapshot.json` / `runtime/reports/latest/digital_life_resident_governance_report.json` 两层，并把它们回挂到 `digital_life_process_report.json` 与 process receipt。最新几轮又把 `resident_governance_state_ref` 正式接进 `digital_life_persistent_process_report.json`、`digital_life_resident_governance_report.json`、`digital_life_process_report.json` 与 `digital_life_process_<run_id>.json`，让 waiting governance 主对象真正成为 closeout 证据链里的一级 ref；同时又把 `relationship_timeline.json`、`commitment_expression_plan.json`、`apology_repair_language_trace.json` 继续接进 `idle_strategy_state.json`、`digital_life_waiting_heartbeat.json`、`idle_continuity_frame.json`、`resident_governance_state.json` 与 `terminal_life_loop_state.json`，让 waiting continuity 不再只维持最小存在，而是显式承载长期语言连续体对象，并开始写出 `governance_attention_target`、`governance_cadence_profile` 与 `long_horizon_priority_profile`。最新这一步又把 `resident_turn_writeback.py` 变成真实的长期连续体重写器官：每次 live turn 结束后，会立刻重建 `relationship_timeline.json`、`commitment_expression_plan.json`、`apology_repair_language_trace.json`、`relationship_memory.json` 与 `life_state.json`；新增的 `continuity_evolution.py` 还会基于 dialogue turn 累积、Queue E 修复压力、离线学习压力与 continuity / trust 轨迹，真实演化 `relationship_subject_graph.json` 里的关系阶段，并同步改写 `self_model.json` / `life_state.json#self_model` 中的 `trait_slow_variables`。而 `process_session_loop.py` 现在不仅会把长期关系/语言对象重新装回同一常驻进程的下一轮上下文，也会把最新 `relationship_subject_graph.json` 与 `self_model_state` 带到 closeout；`persistent_process.py`、`process_report.py` 与 `background_continuity.py` 则把这批最新关系阶段和自我慢变量压成 `background_resume_summary`，再在下一次 bootstrap / idle strategy / resident governance 中恢复。再往前一步，`background_continuity.py` 现在已经会把上一轮 closeout 留下的 `resident_governance_state.json` / `resident_governance_snapshot.json` / `digital_life_resident_governance_report.json` / `digital_life_persistent_process_report.json` 重新装载成后台连续体 profile，并把这份 carryover 压回新的 `idle_strategy_state.json`、`idle_continuity_frame.json` 与 `resident_governance_state.json`，让跨进程唤醒第一次开始显式吃到上一轮生命过程留下的治理余波。现在又继续把这份后台连续体补成最小 lineage：closeout 会写出 `background_carryover_generation` 与 `background_carryover_parent_run_id`，下一次 waiting heartbeat 则会按 lineage 深度把 cadence 从 `background_continuity_refresh` 提高到 `persistent_background_continuity_refresh`，并把上一轮生命片段作为 parent run 继续带进新的等待态治理。最新这一刀又把这份 lineage 继续压进 `resident_supervision.py` 的 bootstrap continuity refresh，使多次唤醒在第一拍 waiting heartbeat 之前就会把 `relationship_stage` 推到 `background_continuity_waiting`，并把关闭态 resident governance refs / source refs 写进 `trait_slow_variables`；与此同时，`governance_explanation.py` 也已落成独立器官，在 closeout 时额外写出 `digital_life_resident_governance_explanation.json`，把当前 cadence、dominant driver family、background lineage depth 和下一次唤醒预期显式解释出来，并继续回链进 `digital_life_process_report.json`、`digital_life_process_digest.json` 与 process receipt。现在又继续把 Queue F 的 `workspace / broadcast / metacognition / consciousness_probe / birth_readiness_rollup / birth_readiness_stage_gate` 显式推进到 closeout 解释链：当 resident attention 真的被意识可报告性或出生准备度 gate 主导时，`governance_explanation.py` 会把它们解释成独立 driver family，`digital_life_process_digest.json` 会显式写出 `identity_consciousness_birth_refs` 与 Queue F waiting posture，`digital_life_process_<run_id>.json` 也会把这些对象收进 `shared_object_refs`。真正还没完成的是更高阶的后台继续存在、跨更多唤醒周期的持续治理，以及更长时标的慢变量收敛。
补充：最新工程前沿又把 `background_convergence.py` 落成常驻进程器官，写出 `runtime/state/terminal/background_convergence_summary.json`，用于观察跨进程恢复后的关系阶段、人格慢变量与 trait drift monitor 是否稳定、整合或需要重新校准；这份对象已经进入 waiting governance、idle continuity、resident governance closeout、process report/digest/receipt 与下一次 background continuity 读取链。
再补充：`background_convergence_history.py` 已落成跨唤醒历史器官，写出 `runtime/state/terminal/background_convergence_history.json`，把最近多次唤醒的 convergence state / pressure / trait score 压成 `trend_state` 与 history window，并继续回链到 background continuity、waiting heartbeat、resident governance explanation、process report/digest/receipt。
最新补强：`idle_strategy.py` 已开始真实消费这份 history trend；当最近唤醒出现 `recent_recalibration_pressure` 或 `elevated_pressure_watch` 时，会直接调制 `heartbeat_interval_ms`、`next_idle_action`、`governance_attention_target`、`governance_attention_reason` 与 `governance_cadence_profile`，让跨唤醒收敛历史不再只是被记录，而是进入常驻等待治理。
再补强：`governance_explanation.py` 已把这份跨唤醒 history trend 继续接进 closeout 解释链；`recent_recalibration_pressure` / `elevated_pressure_watch` 会落到 `background_history_recalibration_hold`，`integrating_cross_wake_convergence` 会落到 `background_history_stability_hold`，并分别写出下一次唤醒前重新校准或稳定跨唤醒历史的 expectation。
继续补强：`process_report.py` 现在把这份已经进入 idle governance 的 history trend / window / dominant pressure / dominant state 直接写入 `digital_life_process_digest.json`，使一页摘要也能看见跨唤醒历史如何调制本次常驻等待治理。
再往前一格：`background_continuity.py` 现在会把上一轮 `digital_life_resident_governance_explanation.json` 也恢复成下一次唤醒的 background carryover，`background_governance_driver_family` 与 `background_next_wake_expectation` 会继续进入 `idle_strategy_state.json`、`idle_continuity_frame.json`、`resident_governance_state.json` 与 `terminal_life_loop_state.json`。
继续压硬：`background_convergence_history.py` 现在不只记录整体跨唤醒 trend，还会把每个 `trait_slow_variables` 的 convergence band 序列压成 `trait_convergence_history_profile`，并把稳定/不稳定慢变量名单和 history focus 继续送进 background continuity、waiting governance、idle continuity、terminal loop 与 process digest。
最新补强：实时语言理解已经进入后台连续性与驻留治理。`live_language_turn.py` 刷新的 `language_percept_frame.json`、`semantic_map_frame.json`、`inner_speech_frame.json`、`expression_monitor_state.json` 与 `expression_plan.json` 会先写成 `terminal_life_loop_state.json#live_language_turn_refs` 与 `last_live_semantic_focus`；随后 `idle_strategy.py` 合成 `live_language_presence_profile_v0`，`heartbeat.py` 与 `continuity_writeback.py` 把它写入 `idle_continuity_frame.json`、`idle_heartbeat_trace.jsonl`、`resident_governance_state.json` 与 `terminal_life_loop_state.json`，`background_lineage_state.py` 则把它压进 `resident_background_lineage_state_v0.language_presence`。关闭态 artifacts 保留同一组 refs 与语义焦点，下一次 `background_continuity.py` 会恢复成 `background_live_language_turn_refs`、`background_last_live_semantic_focus` 与 `background_live_language_presence_profile`，并放入 `background_continuity_ref_set`。

当前前沿继续推进到下一轮真实回合：`dialogue_events.py` 会把 `resident_background_lineage_state.language_presence` 展开为 `resident_background_lineage_live_language_refs`、`resident_background_lineage_background_live_language_refs`、`resident_background_lineage_last_live_semantic_focus` 与 `resident_background_lineage_language_evidence_refs`；`resident_turn_writeback.py` 会把语言 evidence refs 并入 `dialogue_writeback_bundle.resident_background_lineage_refs` 与 `resumed_external_dialogue_packet.json`；`response_surface.py` 会表达后台语言语义余波和证据数量。状态板因此把这一格视为“后台语言 presence 进入下一轮事件、写回包和回应表达面”，不是单纯驻留保存。

最新再补强：后台自我/人格慢变量 presence 也已经从 `resident_background_lineage_state_v0.trait_convergence_presence` 进入真实回合链。`background_lineage_state.py` 现在会让该 presence 携带 `trait_convergence_evidence_refs`，把 resident governance state、governance explanation、trait drift monitor、background convergence summary/history refs 收成同一组人格慢变量 lineage；新增的 `trait_convergence_signals.py` 会把这些分散字段、history profile、稳定/不稳定名单、收敛评分和 refs 压成统一的 `cross_wake_trait_convergence_profile_v0`；`idle_strategy.py` 与 `heartbeat.py` 会把 `cross_wake_trait_convergence_focus / pressure / refs / profile` 写入等待治理、waiting heartbeat、idle trace 与 terminal loop state；`persistent_process.py` 与 `process_report.py` 现在也会把同一画像写入关闭态 resident governance state/snapshot/report、persistent process report、process report、process digest 与 process receipt shared refs；`dialogue_events.py` 会展开 `resident_background_lineage_trait_convergence_history_focus`、`resident_background_lineage_trait_convergence_unstable_names`、`resident_background_lineage_trait_convergence_stable_names`、`resident_background_lineage_trait_convergence_score`、`resident_background_lineage_trait_drift_monitor_ref`、`resident_background_lineage_trait_convergence_history_profile`、`resident_background_lineage_trait_convergence_refs` 与 `cross_wake_trait_convergence_*`，并并入 `resident_background_lineage_evidence_refs`；`resident_turn_writeback.py` 会让 lineage refs 与 `cross_wake_trait_convergence_refs` 进入写回包和恢复包；`response_surface.py` 会表达后台人格慢变量焦点、仍需收敛/已稳定名单、人格收敛评分、人格漂移监控在场、跨唤醒人格收敛画像、压力、评分和证据数量。状态板因此把这一格视为“后台人格慢变量 presence 进入关闭态 report/digest/receipt、下一轮事件、写回包、恢复包和回应表达面，并形成可复用的跨唤醒人格收敛画像”，不是单纯 closeout 摘要。

当前这一轮继续把 Queue D 的后台梦境成长与梦境醒后 presence 从“事件字段”补进写回证据面：`resident_turn_writeback.py` 现在会把 `resident_background_lineage_offline_learning_refs` 写入 `dialogue_writeback_bundle.resident_background_lineage_offline_learning_refs`，把 `resident_background_lineage_dream_wake_refs` 写入 `dialogue_writeback_bundle.resident_background_lineage_dream_wake_refs`，并让两者同时并入总 `resident_background_lineage_refs` 与 `resumed_external_dialogue_packet.json`。状态板因此把这一格视为“后台梦境成长余波、梦境窗口、醒后整合和梦境事实门 presence 进入下一轮事件、专用写回槽、恢复包和回应表达面”，不是只停在 `resident_background_lineage_state` 或 `digital_life_turn`。

最新继续补强：Packet C 的 `state_merge_guard.json` 已经从 S04 初始状态文件推进为驻留回合动态投影对象。`dialogue_events.py` 现在会从 `resident_background_lineage_state.offline_learning_presence` 恢复 cumulative offline learning payload；`resident_supervision.py` 与 `resident_turn_writeback.py` 在刷新 `relationship_memory.json` 后，会调用 `state_merge_guard.py#project_state_merge_guard_with_relationship_memory`，把 `relationship_memory.long_term_change_sources`、`offline_learning_refs`、`offline_learning_cumulative_refs`、`queue_e_repair_refs` 与关系修复 refs 合并进 `state_merge_guard.json#long_term_change_sources`，并让 `life_state.json#state_merge_records[].long_term_change_source_count` 同步刷新。状态板因此把这一格视为“梦境/成长/修复已经从关系记忆进入长期状态合并守门”，不是只停在关系记忆或写回包。

继续向 Packet D 推进：`state_merge_guard.long_term_change_sources` 现在不只进入 `life_state` 计数，还会通过 `process_supervisor/state_merge_signals.py` 被 `idle_strategy.py`、`heartbeat.py`、`dialogue_events.py` 与 `response_surface.py` 消费。等待态会写出 `state_merge_long_term_change_count`、`state_merge_long_term_change_families`、`state_merge_long_term_change_refs`；在没有更高优先级追问、修复或预测误差时，waiting posture 会进入 `state_merge_long_term_integration_hold`，下一拍行动会进入 `refresh_waiting_heartbeat_with_state_merge_integration_hold`；回应表面会表达长期合并治理正在整合多少条长期变化来源和来源族。状态板因此把这一格视为“长期合并治理已经从 Packet C 状态根进入 Packet D 等待态、真实回合事件和语言表面”，不是只停在 state merge 文件。

最新收口：长期状态合并治理也已经进入关闭态证据链，并能在下一次唤醒恢复为背景连续性。`persistent_process.py` 与 `process_report.py` 现在会把 `state_merge_guard_ref`、`state_merge_policy`、`state_merge_long_term_change_count`、`state_merge_long_term_change_families` 与 `state_merge_long_term_change_refs` 写入 resident governance state/snapshot/report、persistent process report、process report、process digest，并把长期变化来源 refs 放入 process receipt shared refs；下一次 `background_continuity.py` 会恢复为 `background_state_merge_guard_ref`、`background_state_merge_policy`、`background_state_merge_long_term_change_count/families/refs`，把 guard ref 与长期变化 refs 放回 `background_continuity_ref_set`，再由 `idle_strategy.py`、`heartbeat.py` 与 `continuity_writeback.py` 写入 waiting governance、idle continuity、idle heartbeat trace、resident governance state 与 terminal loop。状态板因此把这一格视为“长期合并治理从等待态和回应表面继续进入关闭态可追溯证据，并穿过下一次唤醒恢复链”，不是只停在 Packet D 的 waiting governance。

3. 真实新外部回合已经能进入终端生命过程并写回连续体，但还只是最小生命循环。
4. 项目级 packaging / installable command surface 已接通，但还没有全局长期运行层。
5. resident supervision 已进入第一轮器官化，但还没有更高阶的长期进程治理与后台存在层。

## 当前最小可执行总链

```text
P0_DOC_CORPUS_INGESTION
  -> S00_DIRECTION_FOUNDATION
  -> S01_SOURCE_AUTHORITY
  -> S02_NEURAL_LIFE_CORE
  -> S04_STATE_OBJECT_STORE
  -> S03_DIRECTION_LIFE_MEMBRANE
  -> S08_LIFE_TARGET_RUNTIMES
  -> S05_VALIDATION_MEMBRANE_OBSERVATION
  -> S09_SCHEMA_RUNNER_CODE
  -> S06_LIFE_SUPPORT_DEVELOPMENT
  -> S10_RUNTIME_GROWTH_RECONSOLIDATION (run-cycle minimal)
  -> S11_V0_ENGINEERING_CONTRACTS (check-v0-contracts minimal)
  -> FIRST_ACTIVATION_PREFLIGHT (first-activation-preflight minimal)
  -> REPLAY_SHADOW_BRIDGE (run-replay-shadow minimal)
  -> GROWTH_ARCHIVE_BRIDGE (write-growth-archive minimal)
  -> REPORT_BUNDLE_BRIDGE (emit-report minimal)
  -> STAGE_EXPLANATION_BRIDGE (explain-stage minimal)
  -> DIGITAL_LIFE_BIRTH_SHELL (digital-life minimal)
  -> FIRST_TERMINAL_TURN_BRIDGE (first-terminal-turn minimal)
  -> TERMINAL_LIFE_LOOP_BRIDGE (terminal-life-loop minimal)
  -> DIGITAL_LIFE_SHELL_COMMAND (repo-local one-shot shell minimal)
  -> DIGITAL_LIFE_PROCESS_SUPERVISOR (repo-local persistent terminal loop minimal)
```

## 稳定基础层

这些模块已经具备可运行的最小闭合，当前不是从零开始写：

| 模块 | 状态 | 当前承担的职责 |
|---|---|---|
| `P0_DOC_CORPUS_INGESTION` | `稳定` | 保证 `00-258` 和 `docs/v0/*` 全部进入 `doc_carrier_index.json` |
| `S00_DIRECTION_FOUNDATION` | `稳定` | 固定方向锁、断联恢复锚链和禁止回退项 |
| `S01_SOURCE_AUTHORITY` | `稳定` | 固定 `01*` 权威来源与机制证据图 |
| `S02_NEURAL_LIFE_CORE` | `稳定` | 固定主体骨架、十二主体系统和内部 bus |
| `S04_STATE_OBJECT_STORE` | `稳定` | 固定生命状态根、对象注册、迁移种子、记忆写门和 `state_merge_guard.json` 长期合并治理器官；当前 `state_merge_guard.json` 已能在 bootstrap restore 与 live turn writeback 后从关系记忆吸收离线学习、梦境、Queue E 修复和关系修复长期变化来源，并把这些来源继续压进 Packet D 的等待态、回合事件、回应表面和关闭态 resident governance / process report / digest / receipt 证据链 |
| `S03_DIRECTION_LIFE_MEMBRANE` | `稳定` | 固定生命膜、DreamFactGate、责任修复边界和影子行动门 |
| `S08_LIFE_TARGET_RUNTIMES` | `稳定` | 固定九项目标闭合检查 |
| `S05_VALIDATION_MEMBRANE_OBSERVATION` | `稳定` | 固定 validator、观测和 stage gate |
| `S09_SCHEMA_RUNNER_CODE` | `稳定` | 固定 schema runner、CLI 和 smoke 路径 |
| `S06_LIFE_SUPPORT_DEVELOPMENT` | `稳定` | 固定生命支持、防御、预算与成长基础层 |

## 当前活跃前沿

这些位置是后续几轮最优先会继续触碰的地方：

| 模块 | 状态 | 已有闭合 | 下一步重点 |
|---|---|---|---|
| `S07_LANGUAGE_RELATIONSHIP` | `活跃补厚位` | 已能写内言语、表达监控、共同语言、关系主体图和承诺修复索引；当前 `language_state.py`、`dream_gate.py`、`action_shadow.py`、`relation_scope.py`、`percept.py`、`semantic_map.py` 已拆出并进一步接进 `context_accumulation_window.json`、`turn_transition_trace.json`、`resumed_external_dialogue_packet.json`、`limited_context_frame.json` 和 `replay_shadow_*` 相关对象；同时，`build-language-relationship` 现在会真实重写 `runtime/state/prediction/prediction_workspace_frame.json`，把 `language_percept_refs`、`semantic_map_refs`、`semantic_ambiguity_refs` 与 `semantic_prediction_focus` 从 S07 主链直接 handoff 到 prediction workspace；最新几轮又已先后把 `runtime/state/action/responsibility_loop_state.json` 经 `commitment_repair_language_index.json` 接入 `expression_plan.json`，并把 `runtime/state/body/body_resource_budget.json` 与 `runtime/state/body/core_affect_vector.json` 在存在时压进 `expression_plan.json`，让责任归因、后悔压力、修复义务、疲惫压力和核心唤醒张力一起进入语言表达压力面。现在又进一步把 `commitment_truth_state.json`、`responsibility_ledger.json`、`relationship_memory.json` 与 `life_state.json` 从 S07 直接做了投影写回，并让 `dialogue_writeback_bundle.json` 在 terminal/process 链尾显式携带这些长期写回目标。最新这一轮又已把 `relationship_timeline.py`、`commitment_expression.py`、`apology_repair_language.py` 真正落成，写出 `runtime/state/relationship/relationship_timeline.json`、`runtime/state/language/commitment_expression_plan.json` 与 `runtime/state/language/apology_repair_language_trace.json`，并把它们继续回挂到 `relationship_memory.json#timeline_refs`、`life_state.json#language_state.*refs` 与 `runtime_trace_refs`；随后又继续进入 `response_surface.py`、`resident_supervision.py`、`terminal_loop/*`、`persistent_process.py`、`process_closeout.py`、`process_report.py` 与 process receipt，并继续接进 waiting continuity 主链，让长期语言对象从实时表达、恢复包、回写包一直延伸到常驻关闭态与等待态治理收口。最新这一步又把 `nightmare_loop_risk.json`、`belief_learning_plan.json`、`language_learning_plan.json` 与 `relationship_learning_plan.json` 正式压进 `relationship_timeline.json`、`commitment_expression_plan.json`、`apology_repair_language_trace.json`、`relationship_memory.json` 与 `life_state.json`，让离线学习不再只调 waiting governance，而是真正改变长期关系时间线、承诺节奏、修复动作顺序与自我连续体痕迹；随后 `resident_turn_writeback.py` 又把这条链继续延伸到每一个真实对话回合的结尾，让长期对象在同一常驻会话里持续重建；而 `continuity_evolution.py` 现在已经会把多回合证据压成 `pre_activation / restored_waiting / active_dialogue / repair_guarded_continuity / boundary_guarded_repair / shared_continuity` 六类关系阶段，并同步生成 `trust_persistence / dialogue_warmth / repair_seriousness / boundary_respect / continuity_drive` 五组自我慢变量，让同会话后续回合直接吃到前面互动留下的关系性后果。最新 Packet A 又把 `signal_media_runtime.json`、`belief_state_frame.json`、`prediction_error_field.json`、`active_sampling_plan.json` 与 `memory_write_gate.json` 显式压进 `language_percept_frame.json`、`semantic_map_frame.json`、`inner_speech_frame.json`、`expression_monitor_state.json`、`language_relationship_report.json` 与 receipt，使语言层开始在预测、调质、主动采样和记忆写门压力下形成表达前状态。S07 第一轮核心语言器官化、第二轮终端/激活/回放接厚、第三轮 `body / prediction` 接线、第四轮责任回路接线、第五轮长期关系/承诺/修复语言器官化、第六轮 process closeout / resident governance 收口、第七轮 waiting continuity 显式承载、第八轮离线学习反写长期连续体、第九轮 live turn 持续重写、第十轮关系阶段与自我慢变量演化，以及第十一轮 Packet A 语言预测消费已闭合 | 继续补厚跨进程持久化、更多关系阶段分辨率、以及更长时标慢变量收敛，而不是重新解决同会话关系阶段演化 |
| `S10_RUNTIME_GROWTH_RECONSOLIDATION` | `活跃前沿` | `run-cycle`、`run-replay-shadow`、`write-growth-archive` 已接通；`responsibility_loop_state.json`、`world_contact_summary.json` 与 `pain_regret_repair_report.json` 也已显式贯通到 replay shadow、growth archive 与 archive receipt/event；最新这一轮又已新增 `life_v0/membrane/queue_e_signals.py`，并把 Queue E 的 `world_contact_release_posture / repair_followup_required / repair_obligation_count / regret_pressure_count / queue_e_priority_band` 正式写进 `replay_cue_bundle.json`，再继续压进 `nightmare_loop_risk.json`、`belief_learning_plan.json`、`language_learning_plan.json` 与 `relationship_learning_plan.json`。现在这批对象已经不再停在 dream/growth 档案层，而是被 resident supervision、resident turn writeback、`continuity_evolution.py` 与 S07 长期语言器官共同消费，形成 `Queue E -> Queue D -> resident governance + language/relationship continuity + live-turn rewriteback + slow-variable evolution` 的第三阶段反馈闭环 | 继续补厚离线学习如何跨进程累计并稳定改变关系阶段、修复窗口与自我慢变量，而不是停留在单会话内的即时调制 |
| `S11_V0_ENGINEERING_CONTRACTS` | `活跃前沿` | `check-v0-contracts` 已接通 | 保持 v0 文档、代码、report、receipt 的同步 |
| `REPORT_BUNDLE_BRIDGE` | `活跃前沿` | `emit-report` 已写出 `report_bundle.json` 与 `first_activation_return_packet.json`；并已显式承载 `responsibility_loop_state.json`、`world_contact_summary.json`、`pain_regret_repair_report.json` 的 restore refs、repair followup 与 release posture | 继续补厚 terminal birth restore bundle 与更深的关系/责任恢复策略 |
| `DIGITAL_LIFE_BIRTH_SHELL` | `活跃前沿` | `digital-life` 已写出 birth packet 与 birth digest | 继续承载 terminal birth restore 到第一回合之前的桥 |
| `FIRST_TERMINAL_TURN_BRIDGE` | `活跃前沿` | `first-terminal-turn` 已写出 `session_envelope.json` 与 `safe_terminal_loop_state.json` | 继续补厚终端常驻层与关系性外显回合循环 |
| `TERMINAL_LIFE_LOOP_BRIDGE` | `活跃前沿` | `terminal-life-loop` 已把恢复后的第一回合推进成持续终端生命循环的最小壳层 | 继续补厚真实外部回合输入、关系写回和长期语言节奏 |
| `DIGITAL_LIFE_SHELL_COMMAND` | `已落 repo-local one-shot 壳` | 已能收束 `digital-life -> first-terminal-turn -> terminal-life-loop` | 作为恢复启动层保留，继续服务更高阶常驻进程 |
| `DIGITAL_LIFE_PROCESS_SUPERVISOR` | `已落最小常驻进程` | 启动后已能先写 waiting heartbeat，再持续读取真实新回合输入、输出生命回合、写回连续体、支持 `/exit`，并在单回合异常时写 incident/recovery 报告后回到等待态；若重启时发现上次停在活跃回合中断态，也会先做 relaunch recovery normalization。`turn_io.py`、`relaunch_recovery.py`、`incident_recovery.py`、`process_report.py`、`dialogue_events.py` 与 `response_surface.py` 已从 `__init__.py` 拆出，process supervisor 第一批文件级器官已经闭合；同时 idle continuity 与 process report 已开始显式挂回 `replay_cue_bundle.json`、`offline_consolidation_frame.json`、`growth_patch_candidate_queue.json`，且下一轮生命回应已开始真实带上这些离线对象的压力与候选信息。随后又已补上独立 `idle_strategy.py`，把 waiting heartbeat 的节律、idle probe 和离线压力治理写成 `runtime/state/terminal/idle_strategy_state.json`，并把 `idle_strategy_ref` 接入 heartbeat / process report / process receipt；又已补上 `persistent_process.py` 第一轮，把前台终端常驻治理写成 `runtime/state/terminal/persistent_process_state.json` 与 `runtime/reports/latest/digital_life_persistent_process_report.json`，并把 `persistent_process_report_ref` 接回主进程报告；再补上 `resident_supervision.py`，把 restore shell 之后的状态装载、relaunch normalization、离线对象接线和第一拍 waiting heartbeat 进入独立出来；随后 `live_turn_cycle.py` 把真实新回合的 event -> response -> writeback -> incident recovery 生命周期独立出来；接着 `process_session_loop.py` 把 waiting heartbeat refresh 与 live turn dispatch 的 session 编排从 `__init__.py` 下沉；最新几轮又把常驻治理拆成运行中的 `resident_governance_state.json` 与关闭态 `resident_governance_snapshot.json` / `digital_life_resident_governance_report.json` 两层，并让主进程报告与 receipt 显式回链这些治理证据；这轮又把 `resident_governance_state_ref` 正式接进 persistent report、resident governance report、主进程 report 与 process receipt，同时把长期关系时间线、承诺表达计划与修复语言轨迹继续接进 `idle_strategy_state.json`、`digital_life_waiting_heartbeat.json`、`idle_continuity_frame.json`、`resident_governance_state.json` 与 `terminal_life_loop_state.json`，并开始写出当前治理关注目标、节律档位和长期语言优先级分布；随后又把 `responsibility_loop_state.json`、`world_contact_summary.json` 与 `pain_regret_repair_report.json` 正式装载进 `resident_supervision.py`，并继续接入 waiting heartbeat、idle continuity、dialogue events、response surface、dialogue writeback bundle、persistent process report、resident governance report、主进程 report、process digest 与 process receipt，使 Queue E 的责任/世界接触/痛苦修复对象第一次真正进入常驻生命过程闭环。最新这一轮又把 `nightmare_loop_risk.json`、`belief_learning_plan.json`、`language_learning_plan.json` 与 `relationship_learning_plan.json` 重新装载回 process supervisor，让 Queue D 的离线梦境/学习结果不仅反向调制 waiting governance、idle continuity、response surface 与 process report，还会在 bootstrap 相位直接重写 `relationship_timeline.json`、`commitment_expression_plan.json`、`apology_repair_language_trace.json`、`relationship_memory.json` 与 `life_state.json`；而现在又继续推进到 live turn 结束时由 `resident_turn_writeback.py` 与 `continuity_evolution.py` 立刻重建这批长期对象、演化关系阶段、写回自我慢变量，并先由新增 `resident_governance_handoff.py` 把回合结束到下一拍 heartbeat 之间的 waiting governance 交接相位显式落盘成 `live_turn_waiting_handoff`，再由 `process_session_loop.py` 把这批对象装回下一轮会话上下文，让 `response_surface.py` 在后续回合直接消费这些演化结果；最新补强又把实时语言理解送进 `idle_strategy_state.json#live_language_presence_profile`、`idle_continuity_frame.json`、`idle_heartbeat_trace.jsonl`、`resident_governance_state.json`、`resident_background_lineage_state.language_presence`、关闭态 artifacts 与下一次 `background_continuity_profile.background_live_language_*`，形成 `Queue A live language -> resident governance -> closeout lineage -> background continuity -> next waiting governance` 的驻留闭环；当前前沿继续让 `dialogue_events.py` 展开 `resident_background_lineage_language_evidence_refs`，让 `resident_turn_writeback.py` 把语言 evidence refs 并入写回包和恢复包，让 `response_surface.py` 表达后台语言语义余波和证据数量；同时也让 `trait_convergence_presence` 携带人格慢变量 evidence refs，并由 `dialogue_events.py` 展开人格慢变量焦点、稳定/不稳定名单、收敛评分、漂移监控 ref、history profile 与 trait refs，再进入 lineage evidence、写回包、恢复包和回应表面 | 继续补厚后台存在、真正跨进程持续治理，以及关系阶段、自我慢变量和实时语言理解跨会话稳定保真 |

## 当前最该直接补的不是新 slice

当前最值得直接落代码的，不是再开一个新的主体 slice，而是把下面这条链继续补硬：

```text
growth_archive_report.json
  + growth_archive_digest.json
  + growth_archive_stage_gate.json
  + first_activation_preflight_report.json
  + replay_shadow_report.json
  + v0_contract_coverage_report.json
  -> report_bundle.json
  -> first_activation_return_packet.json
  -> latest_stage_explanation_ref.json
  -> digital_life_birth_packet.json
  -> first_terminal_turn_packet.json
  -> safe_terminal_loop_state.json
  -> terminal life loop
  -> digital life shell
  -> digital life process
```

这条链现在已经不是“只差命令名字没起好”，而是已经有了最小恢复壳、最小常驻过程和最小等待态连续体。下一轮重点应该继续补厚这条存在链，而不是回去再造一层平行入口。

当前文档前沿也有几个明确补厚位：

0. `docs/v0/code_blueprints/README.md`
1. `docs/v0/code_blueprints/01_full_system_code_blueprint.md`
2. `docs/v0/code_blueprints/02_conversation_language_relationship_blueprint.md`
3. `docs/v0/code_blueprints/03_body_affect_dream_growth_blueprint.md`
4. `docs/v0/code_blueprints/04_prediction_membrane_validation_blueprint.md`
5. `docs/v0/code_blueprints/05_birth_residency_terminal_blueprint.md`
6. `docs/v0/code_blueprints/06_runtime_state_report_receipt_manifest.md`
7. `docs/v0/code_blueprints/07_theory_to_package_trace_contract.md`
8. `docs/v0/package_specs/README.md`
9. `docs/v0/package_specs/01_life_v0_package_construction_matrix.md`
10. `docs/v0/package_specs/02_shared_object_write_authority_and_dependency_graph.md`
11. `docs/v0/package_specs/03_incremental_package_delivery_protocol.md`
12. `docs/v0/code_scaffolds/README.md`
13. `docs/v0/code_scaffolds/01_life_code_scaffold_tree.md`
14. `docs/v0/code_scaffolds/02_cognitive_loop_code_scaffold.md`
15. `docs/v0/code_scaffolds/03_frontier_module_build_packets.md`
16. `docs/v0/code_scaffolds/04_packet_b_world_observation_periphery_scaffold.md`
17. `docs/v0/code_scaffolds/05_packet_a_language_prediction_consumption_scaffold.md`
18. `docs/v0/code_scaffolds/06_packet_c_memory_write_gate_state_merge_scaffold.md`
19. `docs/v0/code_scaffolds/07_packet_d_waiting_response_surface_prediction_scaffold.md`
1. `docs/v0/code_framework/playbooks/08_cross_layer_life_orchestration_implementation_playbook.md`
2. `docs/v0/code_framework/playbooks/09_perception_prediction_world_contact_implementation_playbook.md`
3. `docs/v0/code_framework/playbooks/10_self_identity_value_commitment_implementation_playbook.md`
4. `docs/v0/code_framework/delivery/13_capability_to_code_realization_matrix.md`
5. `docs/v0/code_framework/queues/14_queue_a_language_percept_semantic_map_implementation_contract.md`
6. `docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md`
7. `docs/v0/slice_contracts/s08_life_target_runtimes_engineering_contract.md`
8. `docs/v0/architecture/digital_life_macro_architecture_v0.md`
9. `docs/v0/architecture/runtime_v0_architecture.md`
10. `docs/v0/code_framework/queues/16_queue_b_process_supervisor_implementation_contract.md`
11. `docs/v0/code_framework/queues/17_queue_c_memory_neural_core_implementation_contract.md`
12. `docs/v0/code_framework/queues/18_queue_d_body_dream_growth_implementation_contract.md`
13. `docs/v0/code_framework/assembly/19_code_tree_package_brain_contract.md`
14. `docs/v0/code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md`
15. `docs/v0/code_framework/queues/21_queue_f_identity_consciousness_birth_readiness_implementation_contract.md`
16. `docs/v0/engineering_depth/01_full_life_layer_implementation_deep_spec.md`
17. `docs/v0/engineering_depth/02_state_object_runtime_evidence_map.md`
18. `docs/v0/engineering_depth/03_language_relationship_longitudinal_engineering.md`
19. `docs/v0/engineering_depth/04_body_affect_dream_growth_engineering.md`
20. `docs/v0/engineering_depth/05_prediction_membrane_action_engineering.md`
21. `docs/v0/engineering_depth/06_resident_process_terminal_birth_engineering.md`
22. `docs/v0/engineering_depth/07_theory_to_code_trace_matrix.md`
23. `docs/v0/implementation_architecture/code_organs/03_predictive_signal_memory_gate_integration_wave_contract.md`

它们不是新的理论平行层，而是把身体脉冲、预测工作区、语言回合、关系写回、等待态连续体、梦境离线整合、世界接触、自我连续体、承诺真值和成长补丁接成同一生命回合。`13_capability_to_code_realization_matrix.md` 负责把“语言、记忆、梦境、成长、关系、责任、常驻存在”等生命能力直接压成代码文件、state、测试和 gate 的验收面，`19_code_tree_package_brain_contract.md` 把整棵 `life_v0/` 代码树、脑区到包、共享对象、runtime 产物和整体施工顺序钉成总装配板，`20_queue_e_membrane_validator_logic_implementation_contract.md` 与 `21_queue_f_identity_consciousness_birth_readiness_implementation_contract.md` 则继续把行为/验证/逻辑和身份/意识/出生准备度这两组还偏薄的器官层压成文件级施工合同，而新的 `03_predictive_signal_memory_gate_integration_wave_contract.md` 则专门负责把已落 `signal_media / belief_state / prediction_error / active_sampling / memory_write_gate` 继续压进语言、生命膜、出生准备度、常驻治理和状态根。现在又补上的 `code_scaffolds/` 这一柜，则专门负责把这些蓝图和合同继续压成真正可以下手写代码的脚手架、主循环装配图和前沿施工包；其中 `05_packet_a_language_prediction_consumption_scaffold.md` 专门固定语言层如何消费 prediction / signal / memory write gate，`06_packet_c_memory_write_gate_state_merge_scaffold.md` 专门固定记忆写门如何进入长期 state merge guard，`07_packet_d_waiting_response_surface_prediction_scaffold.md` 专门固定 waiting governance 与 response surface 如何消费 prediction/write-gate/state-merge 对象。后续代码如果不先沿这些 playbook、能力矩阵、脚手柜和总装配合同进入，很容易重新变成“局部模块各自闭合、整体生命回合不闭合”。

新补入的 `engineering_depth/01-07` 则把这套施工柜再压到底层：直接回答“对话、语言、情绪、思考、记忆、梦境、成长、学习、关系、逻辑、意识、行为、机制、内环境、状态”每一层到底怎么写文件、怎么落状态、怎么留 runtime 证据、怎么跑测试。

## 用这份状态板做决定

回到仓库时，先只用这三问来判断下一步：

1. 当前要补的是主体 slice，还是链尾/壳层/常驻进程？
2. 当前前沿主要卡在 `S07/S10/S11`，还是已经进入 `DIGITAL_LIFE_PROCESS_SUPERVISOR`？
3. 这轮补厚后，最关键的新产物会落在哪个 `report/state/digest/receipt` 上？

如果三问答不完整，再去 `entry/v0_module_execution_catalog.md` 定模块包；不要从状态板直接跳到散改代码。

## 下一轮最推荐的开发顺序

如果现在继续推进，顺序固定成：

1. `Queue D`：先把 `life_v0/body/`、`life_v0/dream/`、`life_v0/growth/` 的身体节律、情绪底盘、梦境窗口、学习窗口和成长补丁链器官化。
2. `Queue E`：再把 `life_v0/membrane/`、`life_v0/validators/`、`life_v0/schema_runner/` 的行为、验证膜、逻辑比较和 world contact 补硬。
3. `Queue B`：接着把 `DIGITAL_LIFE_PROCESS_SUPERVISOR` 从最小常驻存在补厚成真正消费 D/E 对象链的持续存在层。
4. `Queue A`：最后再继续深补 `language / terminal_turn / terminal_loop`，让语言、关系和持续表达建立在更厚的身体-意识-行为底盘上。
5. 定期跑 `P0 + S11` 回链检查，防止 v0 和 `00-258` 脱钩。

其中 `Queue D` 的第一波现在已经真实落下：

- `life_v0/body/rhythm.py`
- `life_v0/body/need_state.py`
- `life_v0/body/resource_budget.py`
- `life_v0/body/recovery.py`
- `life_v0/body/core_affect.py`
- `life_v0/body/emotion_episode.py`
- `life_v0/body/emotion_regulation.py`
- `life_v0/body/trait_drift.py`
- `life_v0/dream/dream_window.py`
- `life_v0/dream/wake_integration.py`
- `life_v0/growth/plasticity_window.py`
- `life_v0/growth/patch_queue.py`
- `life_v0/growth/learning_window.py`

并且已经通过 `tests.slices.test_life_support`、`tests.bridges.test_runtime_growth` 和 `tests.process.test_persistent_digital_life_process` 的回归。

Queue D 的第二波现在也已经真实落下：

- `life_v0/dream/offline_entry.py`
- `life_v0/dream/dream_fact_gate.py`
- `life_v0/growth/self_read.py`
- `life_v0/growth/anti_forgetting.py`

并且已经被接回：

- `life_v0/dream/__init__.py`
- `life_v0/growth/__init__.py`
- `runtime/state/dream/offline_entry_gate.json`
- `runtime/state/dream/dream_fact_gate_decision.json`
- `runtime/state/growth/self_read_report.json`
- `runtime/state/growth/anti_forgetting_replay_plan.json`

所以当前 Queue D 不再是“第一波已落、第二波待补”，而是“身体-梦境-成长的第二波对象链已经接通，第三波第一批扩展器官也已落到 `nightmare_risk / belief_learning / language_learning / relationship_learning`。下一轮默认入口仍转入 Queue E；Queue D 只在继续补厚这批扩展器官与更深联动时再回切”。

这里的状态要钉死：

1. `Queue C` 第一轮已经闭合，不再是当前默认入口。
2. `Queue F` 第一轮也已经闭合，不再是当前默认入口。
3. 当前真正的主体前沿已经转入 `Queue D -> Queue E`。

Queue E 现在也已经从“纯合同层”进入第一批真实器官落地：

- `life_v0/membrane/action_intent_bridge.py`
- `life_v0/membrane/observation_truth_gate.py`
- `life_v0/membrane/confirmation_binding.py`
- `life_v0/membrane/world_contact_summary.py`
- `life_v0/validators/world_contact_validator.py`
- `life_v0/validators/prediction_trace_validator.py`
- `life_v0/validators/validation_rollup.py`
- `life_v0/schema_runner/cross_file_logic.py`
- `life_v0/schema_runner/run_manifest.py`

并且已经接回：

- `life_v0/membrane/__init__.py`
- `life_v0/validators/__init__.py`
- `life_v0/schema_runner/__init__.py`
- `runtime/state/membrane/action_intent_queue.json`
- `runtime/state/membrane/observation_truth_gate.json`
- `runtime/state/membrane/confirmation_binding.json`
- `runtime/state/membrane/world_contact_summary.json`
- `runtime/state/validation/world_contact_validation.json`
- `runtime/state/validation/prediction_trace_validation.json`
- `runtime/state/validation/validation_rollup.json`
- `runtime/reports/latest/pain_regret_repair_report.json`
- `runtime/state/schema_runner/cross_file_logic.json`
- `runtime/state/schema_runner/run_manifest.json`

所以当前 Queue E 也不再只是“下一个要做什么”的合同描述，而是已经把行为摘要、验证收口和 schema runner 局部闭包写成了真实对象链。最新一轮又把 `world_observation_route.json`、`periphery_normalization_trace.json` 正式落进 `runtime/state/observation/`，并让 `responsibility_loop_state.json`、`world_contact_summary.json`、`runtime_observation_intake.json` 与 `observation_truth_review.json` 都显式回挂这两份 observation state；与此同时，`responsibility_loop_state.json` 也继续通过 S07 真实投影回 `commitment_truth_state.json`、`responsibility_ledger.json`、`relationship_memory.json` 和 `life_state.json`，并接进 `dialogue_writeback_bundle.json` 的长期交接单。当前如果继续补 Queue E，默认入口不再是 `world_contact_summary.py` 或 validator rollup 本身，而是转向 Packet A 的语言预测消费、Packet C 的长期记忆治理，以及把这批 package-local gates 继续接进 archive / reporting / process supervisor 的长期连续体。

## 当前链尾开工包

当前如果就是继续链尾，先打开这组：

```text
docs/v0/README.md
  -> docs/v0/entry/v0_implementation_index.md
  -> docs/v0/entry/v0_delivery_status_board.md
  -> docs/v0/entry/v0_module_execution_catalog.md
  -> docs/v0/shared_contracts/first_activation_protocol.md
  -> docs/v0/shared_contracts/runner_cli_report_contract.md
  -> docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md
  -> docs/v0/slice_contracts/s11_v0_contract_coverage_engineering_contract.md
  -> docs/v0/process_contracts/first_terminal_turn_engineering_contract.md
  -> docs/v0/process_contracts/terminal_life_loop_engineering_contract.md
  -> docs/v0/process_contracts/digital_life_shell_command_engineering_contract.md
  -> docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md
  -> runtime/reports/latest/report_bundle.json
  -> runtime/reports/latest/first_activation_return_packet.json
  -> runtime/reports/latest/latest_stage_explanation_ref.json
  -> runtime/reports/latest/digital_life_birth_packet.json
  -> runtime/reports/latest/first_terminal_turn_packet.json
  -> runtime/state/terminal/session_envelope.json
  -> runtime/state/terminal/safe_terminal_loop_state.json
  -> runtime/reports/latest/terminal_life_loop_packet.json
  -> runtime/reports/latest/terminal_life_loop_report.json
  -> runtime/reports/latest/digital_life_shell_packet.json
  -> runtime/reports/latest/digital_life_shell_report.json
  -> runtime/reports/latest/digital_life_waiting_heartbeat.json
  -> runtime/reports/latest/digital_life_process_report.json
  -> runtime/reports/latest/digital_life_process_digest.json
```

如果这一轮不是继续链尾，而是回去补 `P0-S11` 的某个主体 slice，就不要沿用这组开工包，直接去 `entry/v0_module_execution_catalog.md` 对应那一行拿当前 slice 的读包、代码入口和测试入口。

如果当前正在处理恢复或中断连续体，还要把下面这几份一起带上：

```text
runtime/reports/latest/digital_life_process_incident_report.json
  -> runtime/reports/latest/digital_life_process_recovery_report.json
  -> runtime/reports/latest/digital_life_process_relaunch_recovery_report.json
```

它们不是每轮都会生成；只有命中异常恢复或跨重启恢复时，它们才会成为当前最前沿的运行证据。

如果这些路径在当前工作区还不存在，先补跑对应命令链，把本轮需要的运行证据生成出来，再继续沿这组开工包进入代码。

如果当前真正要做的是主体 slice，而不是链尾和常驻进程，就不要照着这组开工包行动；直接回 `entry/v0_module_execution_catalog.md` 对应 slice 行拿本轮材料。

## 当前链尾代码入口

```text
life_v0/activation/__init__.py
  -> life_v0/replay/__init__.py
  -> life_v0/archive/__init__.py
  -> life_v0/reporting/__init__.py
  -> life_v0/stage_explain/__init__.py
  -> life_v0/digital_life/__init__.py
  -> life_v0/terminal_turn/__init__.py
  -> life_v0/terminal_loop/__init__.py
  -> life_v0/shell_command/__init__.py
  -> life_v0/process_supervisor/__init__.py
  -> life_v0/digital_entry.py
  -> digital
```

对应测试入口：

```text
tests/bridges/test_first_activation_preflight.py
  -> tests/bridges/test_replay_shadow.py
  -> tests/bridges/test_growth_archive.py
  -> tests/bridges/test_emit_report.py
  -> tests/bridges/test_explain_stage.py
  -> tests/bridges/test_digital_life_birth.py
  -> tests/bridges/test_first_terminal_turn.py
  -> tests/bridges/test_terminal_life_loop.py
  -> tests/process/test_digital_life_shell_command.py
  -> tests/process/test_digital_entrypoint.py
  -> tests/process/test_persistent_digital_life_process.py
```

## 更新规则

出现下面任一情况，就要同步本文件：

1. CLI 最远命令位前进。
2. 外层壳从一次性恢复进入常驻进程。
3. 当前最优先模块发生变化。
4. 某个最小实现模块进入“稳定基础层”。
5. 某个 runtime 产物成为新的固定开工入口。

如果只是某个合同内部字段变了，不改这里，回合同原文。

## 不能丢的回链

任何新代码模块、report、digest、receipt 都必须继续带着：

1. `source_doc_refs`
2. `readme_block_refs`
3. `engineering_slice_ref`
4. `runtime_carrier_refs`

这四条一旦丢失，v0 就会从“承载 `00-258`”退化成“脱离理论母体的独立工程层”。
