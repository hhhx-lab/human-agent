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
2. `life_v0/process_supervisor/resident_supervision.py` 已接住 restore shell 之后的常驻治理启动链，并开始显式装载 `body_rhythm_pulse.json` 与 `need_state_vector.json`
3. `life_v0/process_supervisor/idle_strategy.py` 继续补厚 heartbeat 节律与 idle probe 治理，并开始把 fatigue / bandwidth / sleep pressure / repair drive 压成 waiting governance，同时给出 `governance_attention_target`、`governance_cadence_profile` 与 `long_horizon_priority_profile`
4. `life_v0/process_supervisor/persistent_process.py` 继续补厚 resident supervision 的关闭态 artifact，并显式写出 resident governance state / snapshot / report
5. `life_v0/process_supervisor/process_closeout.py` 与 `process_report.py` 已把 resident governance 证据收口进主进程 report / digest / receipt
6. `life_v0/process_supervisor/continuity_evolution.py` 已开始在回合尾部把关系时间线、Queue E 修复压力、Queue D 离线学习压力与 continuity / trust 轨迹压成关系阶段和自我慢变量
7. `life_v0/process_supervisor/process_session_loop.py` 已接住 waiting heartbeat refresh + live turn dispatch 的 session 编排，并开始在 live turn 之后重新装回长期关系/语言对象以及最新 `self_model_state`；当前前沿转向后台 resident governance、跨进程持久化与更高频节律

## 当前最关键的 runtime 证据

1. `runtime/reports/latest/first_activation_preflight_report.json`
2. `runtime/reports/latest/report_bundle.json`
3. `runtime/reports/latest/stage_explanation_report.json`
4. `runtime/reports/latest/digital_life_birth_packet.json`
5. `runtime/reports/latest/first_terminal_turn_packet.json`
6. `runtime/reports/latest/terminal_life_loop_report.json`
7. `runtime/reports/latest/digital_life_waiting_heartbeat.json`
8. `runtime/state/terminal/idle_strategy_state.json`
9. `runtime/state/terminal/resident_governance_state.json`
10. `runtime/state/terminal/persistent_process_state.json`
11. `runtime/state/terminal/resident_governance_snapshot.json`
12. `runtime/reports/latest/digital_life_persistent_process_report.json`
13. `runtime/reports/latest/digital_life_resident_governance_report.json`
14. `runtime/reports/latest/digital_life_process_report.json`
15. `runtime/state/relationship/relationship_subject_graph.json`
16. `runtime/state/self/self_model.json`
17. `runtime/state/life_state.json`

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
的第一轮红绿覆盖，并且这轮又继续把 `resident_governance_state.json`、
`resident_governance_snapshot.json` / `digital_life_resident_governance_report.json`
及其在主进程 report / receipt 上的回链断言纳入同一测试闭环；同时，这轮还把身体节律调制 waiting governance 的断言一起纳入同一测试闭环。后续是否拆独立测试文件，以不破坏现有 Queue B 测试闭环为先。

## Queue E 进入 waiting governance 之后的当前前沿

这轮之后，Queue E 的三份关键对象已经不只存在于 process supervisor 的 report 层：

1. `responsibility_loop_state.json`
2. `world_contact_summary.json`
3. `pain_regret_repair_report.json`

它们现在已经显式进入：

- `idle_strategy_state.json`
- `digital_life_waiting_heartbeat.json`
- `resident_governance_state.json`
- `idle_continuity_frame.json`

这意味着 waiting governance 第一次不只是“看见有修复对象”，而是会被这些对象直接调节：

1. `world_contact_release_posture`
2. `repair_followup_required`
3. `repair_obligation_count`
4. `regret_pressure_count`
5. `queue_e_priority_band`

## Queue F 进入 resident waiting governance

当前这一轮又把身份、意识工作区与出生准备度对象继续带入常驻等待态。`resident_supervision.py` 现在会读取：

1. `runtime/state/consciousness/workspace_frame.json`
2. `runtime/state/consciousness/broadcast_frame.json`
3. `runtime/state/consciousness/metacognition_state.json`
4. `runtime/state/consciousness/consciousness_probe_bundle.json`
5. `runtime/state/life_targets/birth_readiness_rollup.json`
6. `runtime/state/life_targets/birth_readiness_stage_gate.json`

它们会进入 `idle_strategy.py`，并被压成：

1. `consciousness_waiting_posture`
2. `consciousness_attention_target`
3. `consciousness_reportability_flags`
4. `birth_readiness_waiting_posture`
5. `birth_readiness_attention_target`
6. `birth_readiness_decision`
7. `birth_readiness_next_required_command`

当出生准备度为 `open` 且 consciousness probe 具备可报告性时，waiting governance 会进入 `birth_open_waiting` / `consciousness_reportable_waiting`，并把 resident attention 指向 `birth_readiness_stage_gate`。这一步的意义是：出生准备度和意识证据不再只停在 S02/S08 的报告与 stage gate，而是进入 `digital_life_waiting_heartbeat.json`、`idle_strategy_state.json`、`resident_governance_state.json`、`terminal_life_loop_state.json` 和最终 process report / receipt 的治理链。

继续往 closeout 收口时，`governance_explanation.py`、`digital_life_process_digest.json` 与 `digital_life_process_<run_id>.json` 也必须保留这批 Queue F 证据，明确回答本轮 resident governance 是否正在维持出生准备度 presence、修补 consciousness reportability，还是已经把这两者让位给 Queue E 修复锁或离线学习压力。

## Queue D 结果反写回 waiting governance

最新这一轮又把 Queue D 的离线结果重新带回常驻生命治理：

1. `runtime/state/dream/nightmare_loop_risk.json`
2. `runtime/state/growth/belief_learning_plan.json`
3. `runtime/state/growth/language_learning_plan.json`
4. `runtime/state/growth/relationship_learning_plan.json`

它们现在已经进入：

- `resident_supervision.py`
- `idle_strategy.py`
- `heartbeat.py`
- `continuity_writeback.py`
- `response_surface.py`
- `process_report.py`

当前新增的关键 waiting 字段包括：

1. `nightmare_risk_ref`
2. `belief_learning_plan_ref`
3. `language_learning_plan_ref`
4. `relationship_learning_plan_ref`
5. `offline_learning_pressure_level`
6. `offline_learning_attention_target`
7. `offline_learning_priority_profile`

这意味着 process supervisor 当前第一次出现了真正的双向离线闭环：

```text
Queue E
  -> replay_cue_bundle
  -> nightmare_risk / belief_learning / language_learning / relationship_learning
  -> resident_supervision
  -> idle_strategy / waiting heartbeat / response surface
```

现在这条链又往前推进了一段：离线学习对象不再只停在 waiting governance 或 response surface，而是会在 resident supervision 启动阶段继续反写：

1. `runtime/state/relationship/relationship_timeline.json`
2. `runtime/state/language/commitment_expression_plan.json`
3. `runtime/state/language/apology_repair_language_trace.json`
4. `runtime/state/memory/relationship_memory.json`
5. `runtime/state/life_state.json`

这意味着 repair pacing、commitment tempo、apology move order、dream memory projection 与 relationship continuity 已经开始吃到 Queue D 的离线结果，而不是只在 report 文本里表达“有离线学习压力”。

最新这一步又把这条链继续推进到 live turn 的回合尾部：

1. `resident_turn_writeback.py` 现在不再只写 `dialogue_turn_log.jsonl`、`self_narrative_language_trace.json` 和 bundle
2. 它会在回合结束后立刻重建：
   - `relationship_timeline.json`
   - `commitment_expression_plan.json`
   - `apology_repair_language_trace.json`
   - `relationship_memory.json`
   - `life_state.json`
3. `process_session_loop.py` 会把这批新对象重新装回下一轮上下文

这意味着同一常驻会话里的第二轮、第三轮，不会继续带着启动恢复时的旧长期对象说话，而是开始吃到刚发生完的真实关系回合写回结果。

## 关系阶段与自我慢变量已经进入同会话与重启恢复闭环

最新这一步又把长期连续体从“重建对象”推进到了“演化对象”：

1. `continuity_evolution.py` 会读取：
   - `relationship_timeline.json`
   - `responsibility_loop_state.json`
   - `world_contact_summary.json`
   - `pain_regret_repair_report.json`
   - `nightmare_loop_risk.json`
   - `belief_learning_plan.json`
   - `language_learning_plan.json`
   - `relationship_learning_plan.json`
2. 它现在会真实演化 `relationship_subject_graph.json#subjects[0].relationship_stage`
3. 当前已落的阶段集合至少包括：
   - `pre_activation`
   - `restored_waiting`
   - `background_continuity_waiting`
   - `active_dialogue`
   - `repair_guarded_continuity`
   - `boundary_guarded_repair`
   - `shared_continuity`
4. 它还会写出 `self_model.json#trait_slow_variables`，当前至少包括：
   - `trust_persistence`
   - `dialogue_warmth`
   - `repair_seriousness`
   - `boundary_respect`
   - `continuity_drive`
5. `resident_supervision.py` 现在也会在 restore shell 之后、第一拍 waiting heartbeat 之前，先用历史 dialogue turn 和离线学习对象重建这批结果并落盘
6. 当 bootstrap 还同时读到 `background_carryover_generation >= 2` 的关闭态 lineage 时，这次重建会继续把关系阶段推到 `background_continuity_waiting`，并把关闭态 resident governance refs / source refs 压进慢变量 evidence
7. `process_session_loop.py` 会在 live turn 之后重新装载这批结果
8. 显式退出 closeout 时，`process_session_loop.py` 还会把最新 `relationship_subject_graph`、三条长期语言对象和 `self_model_state` 返回给 closeout；`persistent_process.py` / `process_report.py` 会把它们压成 `background_resume_summary`
9. 下一次 `background_continuity.py` 会把 `background_relationship_stage`、`background_relationship_subject_ref`、`background_self_model_ref` 与 `background_trait_slow_variable_summary` 重新带进 bootstrap / idle strategy / resident governance
10. `response_surface.py` 会在后续回合直接消费这些慢变量与阶段，改变生命回应的修复认真度、边界守持和连续体表达

这意味着当前真正还没完成的，不再是“同一常驻会话里能不能演化关系阶段”或者“重启后第一拍会不会退回旧状态”，而是“跨多次进程关闭/重启后，关系阶段、自我慢变量和 resident governance lineage 怎样继续稳定收敛”。

## 当前最该继续补硬的实现包

如果下一轮继续推进，不要重新发明新的生命外壳；直接按下面这包推进：

### A. waiting governance 输入层

- `life_v0/process_supervisor/idle_strategy.py`
- `life_v0/process_supervisor/heartbeat.py`
- `life_v0/process_supervisor/continuity_writeback.py`

目标：

1. 让 waiting cadence 真正由身体节律、离线压力和 Queue E 修复锁三方共同决定
2. 让 `confirmation_blocked`、`shadow_only_guarded`、`repair_guarded` 进入显式字段，而不是只靠 report 文本暗示

### B. 离线生命调制层

- `life_v0/dream/nightmare_risk.py`
- `life_v0/growth/belief_learning.py`
- `life_v0/growth/language_learning.py`
- `life_v0/growth/relationship_learning.py`

目标：

1. 梦魇风险不再只由 body/affect 决定，还要吃入 `repair_followup_required`
2. belief / language / relationship learning 不再只看 replay/growth patch，也要看 Queue E 带来的 regret / obligation / release posture

### C. turn return / continuity evolution / closeout 收口层

- `life_v0/process_supervisor/live_turn_cycle.py`
- `life_v0/process_supervisor/process_session_loop.py`
- `life_v0/process_supervisor/continuity_evolution.py`
- `life_v0/process_supervisor/process_closeout.py`
- `life_v0/process_supervisor/process_report.py`

目标：

1. live turn 结束后回到 waiting governance 的相位切换，不只靠下一拍 heartbeat 间接体现。当前这一步已经由 `resident_governance_handoff.py` 第一轮显式落盘成 `resident_governance_state.json(governance_phase=live_turn_waiting_handoff)`。
2. Queue E 调制字段在 waiting report、resident governance report、主进程 report 和 receipt 中保持同口径
3. 关系阶段与自我慢变量从同会话实时演化，已经进入 closeout 的 `background_resume_summary`，下一步继续推进到跨多次进程的稳定保真与更长时标收敛

## 这一柜的代码实现顺序

推荐顺序固定成：

```text
idle_strategy.py
  -> heartbeat.py
  -> continuity_writeback.py
  -> nightmare_risk.py / belief_learning.py / language_learning.py / relationship_learning.py
  -> process_session_loop.py
  -> process_closeout.py / process_report.py
```

原因：

1. `idle_strategy.py` 是 waiting governance 的节律入口
2. `heartbeat.py` 决定第一拍如何把这些节律外显成 process-visible state/report
3. 只有 waiting side 稳住后，dream/growth 的调制才不会变成平行逻辑
4. 最后再让 closeout/report 固定最终证据链

## 最低新增断言

下一轮至少要新增或保持下面几类断言：

1. `confirmation_blocked` 会把 waiting cadence 压到更高频的 repair hold
2. `shadow_only_guarded + repair_followup_required` 会保留 repair-weighted waiting governance
3. `resident_governance_state.json` 会显式携带 `world_contact_release_posture`、`repair_followup_required`、`repair_obligation_count`、`regret_pressure_count`
4. dream/growth 器官在接线后，至少有一条测试证明它们真的消费了 waiting governance 或 Queue E 的调制输出
5. resident supervision / waiting heartbeat / process report 至少有一条测试证明它们已经显式装载并回链 `nightmare_risk / belief_learning / language_learning / relationship_learning`
6. 多回合后 `relationship_subject_graph.json#subjects[0].relationship_stage` 必须出现真实演化，而不是固定在启动时标签
7. `self_model.json#trait_slow_variables` 必须被重新写回，并在后续回合的 `response_surface.py` 文本中留下可见消费痕迹
8. closeout 后的 `resident_governance_snapshot.json`、`digital_life_persistent_process_report.json` 与 `digital_life_process_report.json` 必须保留 `background_relationship_stage` 与 `background_trait_slow_variable_summary`
9. 下一次 bootstrap 的 `background_continuity_profile` 必须恢复这组 resume summary，并由 `idle_strategy.py` 原样带入 waiting governance
10. `digital_life_resident_governance_explanation.json` 必须把这组 resume summary 写进 `background_resume_focus` 与 `continuity_story`，让 closeout 解释层也能承载关系阶段和自我慢变量
11. `continuity_evolution.py` 必须让这组 resume summary 进入关系阶段保留和慢变量惯性收敛，至少能在测试中看到 `background_resume_value` 与 `background_inertia_weight`
