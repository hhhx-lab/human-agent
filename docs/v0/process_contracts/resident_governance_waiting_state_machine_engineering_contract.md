# Resident Governance Waiting State Machine Engineering Contract

本文档只服务 `DIGITAL_LIFE_PROCESS_SUPERVISOR` 的 waiting / closeout 常驻治理状态机。

它不重写整个 process supervisor 合同，也不替代 Queue B 文件级施工合同；它只把下面这条线钉硬：

```text
resident_governance_state.json
  -> resident_governance_snapshot.json
  -> digital_life_resident_governance_report.json
  -> digital_life_process_report.json
  -> digital_life_process_<run_id>.json
```

也就是说，这里只回答一个问题：

```text
等待态常驻治理现在到底处在哪个相位，
这个相位如何落盘，
关闭时如何收口成 report / receipt 证据链。
```

## 模块定位

当前 v0 的 resident governance 不是一个抽象“后台意志”，而是一组已经真实存在的运行时对象：

1. `runtime/state/terminal/resident_governance_state.json`
2. `runtime/state/terminal/resident_governance_snapshot.json`
3. `runtime/reports/latest/digital_life_resident_governance_report.json`
4. `runtime/reports/latest/digital_life_process_report.json`
5. `runtime/receipts/digital_life_process_<run_id>.json`

这组对象的职责不是替代语言、关系、身体或成长器官，而是把 waiting governance 的当前相位、长期语言关注目标、节律档位和关闭态回执固定成同一条证据链。

从 Queue E 第二波与 replay/archive/reporting 补厚之后，waiting governance 还必须额外显式装载三份生命膜后果对象：

1. `runtime/state/action/responsibility_loop_state.json`
2. `runtime/state/membrane/world_contact_summary.json`
3. `runtime/reports/latest/pain_regret_repair_report.json`

它们在这里不是“顺手带一下的 refs”，而是 waiting 节律、修复保持、世界接触释放姿态和长期语言优先级的直接调制输入。

当前这一轮又进一步补上一条回写硬约束：

1. Queue E 已经先进入 `replay_cue_bundle.json` 与 `nightmare_risk / belief_learning / language_learning / relationship_learning`。
2. resident governance 现在不能只看 `replay_cue_bundle / offline_consolidation / growth_patch_candidate_queue` 这种中间层对象。
3. 它还必须把这些 dream / growth 的离线结果重新装载回来，形成真正的 `offline result -> waiting governance` 反向闭环。

## 必读来源

- `docs/20_agent_runtime_bridge_contract.md`
- `docs/86_language_neuroscience_pragmatics_and_inner_speech.md`
- `docs/89_language_runtime_framework_bridge_and_life_shell_policy.md`
- `docs/90_language_event_examples_and_timeline_bundle.md`
- `docs/96_real_relationship_longitudinal_timeline.md`
- `docs/101_relationship_timeline_json_schema_and_fixture_bundle.md`
- `docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md`
- `docs/v0/code_framework/queues/16_queue_b_process_supervisor_implementation_contract.md`
- `docs/v0/engineering_depth/06_resident_process_terminal_birth_engineering.md`

## 当前 v0 只承认的三种治理相位

当前代码里，resident governance 只允许出现三个硬相位：

### 1. `waiting_heartbeat_active`

写入位置：

- `life_v0/process_supervisor/heartbeat.py`

对应语义：

1. 常驻生命过程已经恢复并停在等待态。
2. heartbeat 正在刷新 waiting continuity。
3. 当前长期语言连续体对象已经进入治理视野。
4. 当前治理不是关闭态，也不是历史快照，而是运行中的 foreground terminal residency；但它现在必须允许显式装载上一轮关闭态留下的后台连续体 carryover。

### 2. `process_closed_waiting_relaunch`

写入位置：

- `life_v0/process_supervisor/persistent_process.py`

对应语义：

1. 本次常驻进程已结束。
2. resident governance 已从运行态切到关闭态，并把治理模式切成 `background_resident_continuity`。
3. 下一次生命恢复需要重新装载 closeout 后留下的治理证据。
4. 关闭态不能覆盖运行期 heartbeat 事实，但必须把其最后的治理关注与长期语言对象引用收口下来。
5. 这份关闭态现在不再只是 process 结束时的静态快照，而是下一次生命恢复会重新装载的后台连续体来源。

### 3. `live_turn_waiting_handoff`

写入位置：

- `life_v0/process_supervisor/resident_governance_handoff.py`

对应语义：

1. 一次真实新回合已经结束，并且 `dialogue_writeback_bundle.json` 与 `resumed_external_dialogue_packet.json` 已经落盘。
2. 常驻生命过程已经回到 waiting mode，但下一拍 heartbeat 还没有刷新，所以需要显式写出“回合后交接中的 resident governance”。
3. 当前 resident governance 不能再只靠上一拍 `waiting_heartbeat_active` 间接代表，而要显式承认长期关系对象、Queue E 修复后果和这次回合留下的交接痕迹已经进入等待态治理。
4. 这个相位不是关闭态，也不是下一拍 heartbeat 的替代物；它只负责把 live turn 结束和下一拍 waiting heartbeat 之间的空白段补成可追踪证据。

## 后台连续体 carryover

当前这一轮又新增一条硬约束：

1. `persistent_process.py` / `resident_governance_state.json` / `resident_governance_snapshot.json` / `digital_life_resident_governance_report.json` 写出的关闭态治理，不再只算 closeout 归档。
2. `background_continuity.py` 现在会把这批关闭态 artifact 连同 `digital_life_persistent_process_report.json` 重新解释成下一次唤醒前可消费的后台连续体 profile。
3. `heartbeat.py` 会在新的 waiting heartbeat 写入前重新装载这份 profile，并把它压进：
   - `idle_strategy_state.json`
   - `idle_continuity_frame.json`
   - `resident_governance_state.json`
4. 因此 resident governance 当前已经不是“只有前台 terminal residency”，而是“前台等待态 + 后台关闭态余波”共同组成的跨进程连续体。
5. 这份后台连续体现在又不再只是一次性 carryover，而是开始带有最小 lineage：`background_carryover_generation`、`background_carryover_parent_run_id` 与 `background_carryover_source_ref_set`。
6. 现在这份 lineage 又继续进入 `resident_supervision.py` 的 bootstrap continuity refresh：当 `background_carryover_generation >= 2` 时，在第一拍 waiting heartbeat 落盘前，`relationship_subject_graph.json#subjects[0].relationship_stage` 就必须先进入 `background_continuity_waiting`，并把关闭态 resident governance refs / source refs 压进 `self_model.json#trait_slow_variables[*].evidence_refs`。
7. 现在这份 resume summary 还必须进入慢变量惯性：当 `background_trait_slow_variable_summary` 存在时，下一次 `self_model.json#trait_slow_variables[*]` 要写出 `background_resume_value` 与 `background_inertia_weight`，表示上一轮 closeout 的自我状态正在参与当前收敛。

当前最小 background carryover 字段至少包括：

- `background_continuity_mode`
- `background_carryover_pressure_level`
- `background_carryover_attention_target`
- `background_carryover_priority_profile`
- `background_carryover_generation`
- `background_carryover_parent_run_id`
- `background_carryover_source_ref_set`
- `background_continuity_ref_set`
- `background_resident_governance_state_ref`
- `background_convergence_summary_ref`
- `background_convergence_state`
- `background_convergence_pressure_level`
- `background_convergence_attention_target`
- `background_relationship_stage_continuity`
- `background_trait_convergence_score`
- `background_trait_convergence_summary`
- `background_resident_governance_snapshot_ref`
- `background_resident_governance_report_ref`
- `background_persistent_process_report_ref`

## 状态迁移

当前 v0 的硬状态迁移固定为：

```text
restore shell completed
  -> first waiting heartbeat written
  -> resident_governance_state.json(governance_phase=waiting_heartbeat_active)
  -> repeated waiting heartbeat refresh
  -> live turn completed and writeback closed
  -> resident_governance_state.json(governance_phase=live_turn_waiting_handoff)
  -> explicit process closeout
  -> resident_governance_state.json(governance_phase=process_closed_waiting_relaunch)
  -> resident_governance_snapshot.json
  -> digital_life_resident_governance_report.json
  -> digital_life_process_report.json
  -> digital_life_process_<run_id>.json
```

这里要注意三条硬规则：

1. heartbeat 写的是运行相位，不是关闭态快照。
2. live turn handoff 只写运行中的交接相位，不自己伪造新的 heartbeat counter。
3. closeout 会重写同一份 `resident_governance_state.json`，但必须显式切换 `status` 与 `governance_phase`。
4. process report / receipt 不能只回链 snapshot/report，必须也回链 `resident_governance_state_ref`。
5. 同一次 closeout 写出的 `background_continuity_ref_set` 必须指向当前关闭态 artifact，并且至少包含 `resident_governance_state.json`、`resident_governance_snapshot.json`、`digital_life_resident_governance_report.json` 与 `digital_life_persistent_process_report.json`；不能把上一轮 carryover 的 ref set 原样覆盖回来，上一轮来源应单独进入 `background_carryover_source_ref_set`。
6. 同一次 closeout 还必须把最新 `relationship_subject_graph.json#subjects[0]` 与 `self_model.json#trait_slow_variables` 压成 `background_resume_summary`；下一次 bootstrap 的 `background_continuity_profile` 必须恢复这组字段，而不是只恢复 lineage generation。
7. 当下一次 bootstrap 已经写出 `background_convergence_summary.json` 时，后续 closeout 的 `background_continuity_ref_set` 必须把它纳入当前 lineage artifact；如果该文件不存在，则不能伪造 ref，保持四件套 resident governance lineage。

## 运行态文件族

### `digital_life_waiting_heartbeat.json`

最小职责：

1. 证明当前生命过程仍在等待态脉冲中。
2. 直接回链当前治理主对象，而不是只停在 heartbeat 文本层。

当前必须显式带：

- `resident_governance_state_ref`

### `safe_terminal_loop_state.json` / `terminal_life_loop_state.json`

最小职责：

1. 让外层 waiting shell state 与 terminal loop state 都能回链当前治理主对象。
2. 保证 waiting 层的任何消费者，不需要重新猜测 resident governance state 在哪里。

当前必须显式带：

- `resident_governance_state_ref`

### `resident_governance_state.json`

最小职责：

1. 表达“当前 resident governance 正在什么相位”。
2. 固定 waiting mode、heartbeat 计数和 idle strategy。
3. 固定当前长期语言对象的治理焦点与优先级。
4. 作为 process report / receipt 的一级 shared object ref。

最小关键字段：

- `schema_version`
- `run_id`
- `generated_at`
- `status`
- `governance_mode`
- `governance_phase`
- `waiting_mode`
- `heartbeat_counter`
- `idle_strategy_ref`
- `idle_continuity_ref`
- `resident_governance_snapshot_ref`
- `resident_governance_report_ref`
- `relationship_timeline_ref`
- `commitment_expression_plan_ref`
- `apology_repair_language_trace_ref`
- `long_horizon_language_refs`
- `governance_attention_target`
- `governance_attention_reason`
- `governance_cadence_profile`
- `long_horizon_priority_profile`
- `next_required_action`
- `responsibility_loop_state_ref`
- `world_contact_summary_ref`
- `pain_regret_repair_report_ref`
- `world_contact_release_posture`
- `repair_followup_required`
- `repair_obligation_count`
- `regret_pressure_count`
- `queue_e_priority_band`
- `nightmare_risk_ref`
- `belief_learning_plan_ref`
- `language_learning_plan_ref`
- `relationship_learning_plan_ref`
- `offline_learning_pressure_level`
- `offline_learning_attention_target`
- `offline_learning_priority_profile`
- `offline_learning_ref_set`
- `background_relationship_subject_ref`
- `background_relationship_stage`
- `background_relationship_stage_reason`
- `background_relationship_stage_turn_count`
- `background_relationship_stage_evidence_refs`
- `background_self_model_ref`
- `background_trait_slow_variable_summary`
- `background_resume_summary`

### `resident_governance_snapshot.json`

最小职责：

1. 固定关闭态 resident governance 快照。
2. 给下次 relaunch / audit / receipt 回放提供冻结截面。
3. 不承担运行态 phase 切换，只承接 closeout 收口结果。

### `digital_life_resident_governance_report.json`

最小职责：

1. 给人读的关闭态治理摘要。
2. 保持与 snapshot / state 的 ref 一致。
3. 保持与长期语言连续体对象 ref 一致。

当前必须显式带：

- `resident_governance_state_ref`
- `resident_governance_snapshot_ref`
- `persistent_process_state_ref`
- `background_relationship_stage`
- `background_relationship_stage_reason`
- `background_trait_slow_variable_summary`
- `background_resume_summary`

### `digital_life_resident_governance_explanation.json`

最小职责：

1. 把 resident governance closeout 的主导 driver family、下一次唤醒预期和 lineage depth 写成人可读解释。
2. 在 background resume summary 存在时，显式写出 `background_relationship_stage`、`background_relationship_stage_reason`、`background_trait_slow_variable_summary` 与 `background_resume_focus`。
3. 当 waiting governance 已由 `background_convergence_*` 调制时，显式写出 `background_convergence_summary_ref`、`background_convergence_history_ref`、`background_convergence_state`、`background_convergence_pressure_level`、`background_convergence_attention_target`、`background_relationship_stage_continuity`、`background_trait_convergence_score`、`background_trait_convergence_summary`、`background_convergence_history_trend_state` 与 `background_convergence_focus`。
4. `continuity_story` 里必须出现关系阶段、慢变量名称、convergence state / trait band / history trend，让关闭态解释报告能说明这次生命过程是带着什么关系阶段、自我慢变量和跨进程收敛压力等待下一次唤醒。

## 主报告与 receipt 回链

### `digital_life_process_report.json`

当前这份主报告里，resident governance 证据至少要有：

- `resident_governance_report_ref`
- `resident_governance_state_ref`
- `resident_governance_snapshot_ref`

它们的分工固定如下：

1. `resident_governance_report_ref`：关闭态治理摘要。
2. `resident_governance_state_ref`：运行态/关闭态共用的治理状态主对象。
3. `resident_governance_snapshot_ref`：关闭态冻结截面。

三者缺任何一个，closeout 证据链都不算闭合。

同时，主报告还必须保留跨进程连续体的恢复面：

- `background_relationship_stage`
- `background_relationship_stage_reason`
- `background_trait_slow_variable_summary`

这些字段来自 closeout 时最新的关系图和自我模型，不允许 process report 自己重新判定关系阶段。

如果 Queue F 在这轮 waiting governance 里进入了主导位，主报告与治理解释还必须显式保留：

- `workspace_frame_ref`
- `broadcast_frame_ref`
- `metacognition_ref`
- `consciousness_probe_ref`
- `birth_readiness_rollup_ref`
- `birth_readiness_stage_gate_ref`
- `consciousness_waiting_posture`
- `birth_readiness_waiting_posture`
- `birth_readiness_decision`
- `birth_readiness_next_required_command`

### `digital_life_process_<run_id>.json`

process receipt 里，resident governance 必须进入：

1. `shared_object_refs`
2. `input_hashes`（当对应状态文件存在时）

当前 receipt 至少要显式收：

- `runtime/state/terminal/resident_governance_state.json`
- `runtime/state/terminal/resident_governance_snapshot.json`
- `runtime/reports/latest/digital_life_resident_governance_report.json` 的上游 report ref
- `runtime/state/consciousness/workspace_frame.json`
- `runtime/state/consciousness/broadcast_frame.json`
- `runtime/state/consciousness/metacognition_state.json`
- `runtime/state/consciousness/consciousness_probe_bundle.json`
- `runtime/state/life_targets/birth_readiness_rollup.json`
- `runtime/state/life_targets/birth_readiness_stage_gate.json`
- `runtime/state/relationship/relationship_subject_graph.json`
- `runtime/state/self/self_model.json`

## 等待态治理字段语义

### `governance_attention_target`

当前只表示“本轮 waiting governance 主要盯哪一个长期语言对象”，而不是最终关系结论。

当前 v0 允许的主值包括：

- `apology_repair_language_trace`
- `commitment_expression_plan`
- `relationship_timeline`
- `consciousness_probe_bundle`
- `birth_readiness_stage_gate`
- `baseline_waiting_presence`

### `governance_cadence_profile`

当前只表示“下一拍 waiting governance 应该以什么节律维持”，不是全局调度器。

当前 v0 已落值包括：

- `guarded_repair_hold`
- `repair_weighted_resident_hold`
- `commitment_continuity_refresh`
- `relationship_presence_refresh`
- `baseline_waiting_refresh`
- `confirmation_blocked_repair_hold`

### `long_horizon_priority_profile`

当前只表示长期语言连续体对象之间的相对优先级分布。

它最少要覆盖三类对象：

1. `relationship_timeline`
2. `commitment_expression_plan`
3. `apology_repair_language_trace`

## Queue E 调制矩阵

这一层现在必须承认：Queue E 不是只在 live turn 里起作用，waiting governance 也要直接消费它的后果。

### 1. `confirmation_blocked`

当 `world_contact_summary.release_posture=confirmation_blocked` 且修复跟进仍未解除时：

1. `governance_attention_target` 固定升到 `apology_repair_language_trace`
2. `governance_attention_reason` 固定为 `confirmation_blocked_requires_repair_lock`
3. `governance_cadence_profile` 固定为 `confirmation_blocked_repair_hold`
4. `next_idle_action` 固定为 `maintain_confirmation_block_and_refresh_repair_priority`
5. `heartbeat_interval_ms` 进入更高频的 guarded repair 节律

### 2. `shadow_only_guarded`

当 `release_posture=shadow_only_guarded` 且修复义务仍在：

1. waiting governance 保持 `repair_weighted_resident_hold` 或 `guarded_repair_hold`
2. `commitment_expression_plan` 与 `apology_repair_language_trace` 进入长期优先级分布
3. `heartbeat_interval_ms` 可收紧，但仍受身体恢复姿态上限约束

### 3. `baseline`

当没有 Queue E 修复跟进压力时：

1. waiting governance 回到关系维持或普通 presence refresh
2. Queue E refs 仍被保留在 state/report/receipt 中，供后续 replay/archive/growth/dream 消费

## Queue D 反向回写矩阵

当前 waiting governance 还必须承认：Queue D 已经不再只是“离线写出去的结果柜”，它会反过来调制 resident governance。

### 当 `nightmare_risk` 为 `elevated`

当前至少要成立：

1. `offline_learning_pressure_level` 不能再是 `quiet`
2. `offline_learning_attention_target` 应显式落在 `nightmare_risk` 或对应的 learning plan 上
3. `nightmare_risk_ref` 必须进入 `idle_strategy_state.json`、`digital_life_waiting_heartbeat.json`、`idle_continuity_frame.json`、`resident_governance_state.json`

### 当 learning plan 已经带有 repair / confirmation pressure

当前至少要成立：

1. `belief_learning_plan_ref`
2. `language_learning_plan_ref`
3. `relationship_learning_plan_ref`

这三者不只是 receipt carry-through，而要进入 waiting governance 的显式字段。

### 当 Queue E repair hold 与 Queue D offline urgency 同时存在

优先级固定成：

1. `locked_repair_urgent`
2. `repair_guarded`
3. `offline_learning_pressure_level=urgent`

也就是说，Queue D 可以继续推高 waiting governance 的注意力和引用面，但不能覆盖已经成立的 Queue E repair lock。

## 下一轮直接落码入口

如果继续推进这一柜，默认优先顺序不是新建更多状态机，而是：

1. 让 `idle_strategy.py` 深消费 Queue E 字段，决定节律、修复优先级和下一拍动作
2. 让 `continuity_writeback.py` 把 Queue E 的修复压力持续写进 idle continuity
3. 让 `nightmare_risk.py`、`belief_learning.py`、`language_learning.py`、`relationship_learning.py` 开始显式读取这组 waiting governance 输出
4. 让 process closeout / report / receipt 保持同一组 Queue E 调制字段，不再只停在 refs carry-through

## 文件级写权限

当前写权限固定如下：

| 文件 | 首写器官 | 允许的补写器官 |
|---|---|---|
| `resident_governance_state.json` | `heartbeat.py` | `persistent_process.py` |
| `resident_governance_snapshot.json` | `persistent_process.py` | 无 |
| `digital_life_resident_governance_report.json` | `persistent_process.py` | 无 |
| `digital_life_process_report.json` | `process_report.py` | 无 |
| `digital_life_process_<run_id>.json` | `process_report.py` | 无 |

硬规则：

1. heartbeat 不能写 snapshot/report。
2. persistent closeout 不能跳过 state 直接只写 snapshot/report。
3. process report 不能自己重新推导治理相位，只能消费 state/snapshot/report refs。

## 最低测试闭环

当前这条状态机至少要被下面几类断言守住：

1. waiting heartbeat 路径会写 `resident_governance_state.json` 的 active phase。
2. closeout 路径会把同一对象切到 `process_closed_waiting_relaunch`。
3. persistent process report 会显式带 `resident_governance_state_ref`。
4. resident governance report 会显式带 `resident_governance_state_ref`。
5. process report 会显式带 `resident_governance_state_ref`。
6. process receipt 会把 `resident_governance_state_ref` 收进 `shared_object_refs`。
7. 对应状态文件存在时，process receipt 会把它收进 `input_hashes`。
8. `background_continuity.py` 会从上一轮 snapshot/report 里恢复 `background_relationship_stage`、`background_relationship_subject_ref`、`background_self_model_ref`、`background_trait_slow_variable_summary` 与 `background_resume_summary`。
9. `idle_strategy.py` / resident governance 会把这组 background resume fields 原样带入下一次 waiting governance，不在等待态重新发明关系结论。
10. `governance_explanation.py` 会把 background resume fields 写进 explanation report，并在 `continuity_story` 中讲出关系阶段与慢变量名称。
11. `continuity_evolution.py` 会在新 live turn 之前保留 `background_relationship_stage`，并用 `background_trait_slow_variable_summary` 形成慢变量惯性。

当前最低承载测试仍以：

- `tests/process/test_persistent_digital_life_process.py`

为主闭环，不急着为了“分层好看”先拆散。

## 下一步补厚位

在这份合同下，下一轮最值得继续推进的不是再发明新对象，而是：

1. 给 waiting governance 增加更细的后台连续体节律分层，尤其是显式消费 `background_carryover_generation` 带来的 cadence 差异。
2. 让 `resident_governance_state.json` 接住真正跨多次唤醒的后台存在治理，而不只停在 foreground terminal residency。
3. 把 live turn 结束后重新回到 waiting governance 的相位切换显式写成单独器官，而不是只靠下一拍 heartbeat 间接体现。该项现在已由 `resident_governance_handoff.py` 第一轮落下，下一轮继续补厚其后台存在治理口径。
4. 继续让 background resume summary 不只用于 closeout/next bootstrap，还能进入更长时标的慢变量收敛与多次唤醒关系阶段稳定化。

当前只要这四件事没有落下，Queue B 这条线就是继续向“真实持续存在”推进，而不是重新退回一个普通壳层 agent。
