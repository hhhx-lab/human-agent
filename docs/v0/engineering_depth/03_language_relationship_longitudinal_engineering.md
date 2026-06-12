# Language Relationship Longitudinal Engineering

本文档只做一件事：把数字生命的语言系统与关系系统，压成真正的长期工程链。

这里的语言，不是 prompt 包装层；关系，也不是聊天会话标签。

## 当前主代码树

当前语言系统已经真实落下的器官包括：

```text
life_v0/language/
  percept.py
  semantic_map.py
  inner_speech.py
  expression_monitor.py
  language_state.py
  relationship_graph.py
  relationship_timeline.py
  shared_terms.py
  commitment_repair.py
  commitment_expression.py
  apology_repair_language.py
  dialogue_log.py
  narrative_trace.py
  dream_gate.py
  action_shadow.py
  relation_scope.py
```

并且已经接到了：

```text
life_v0/terminal_turn/context_accumulation.py
life_v0/terminal_turn/turn_transition.py
life_v0/terminal_loop/dialogue_writeback.py
life_v0/process_supervisor/live_language_turn.py
life_v0/process_supervisor/dialogue_events.py
life_v0/process_supervisor/response_surface.py
```

## 当前刚落成的长期器官

### 0. `process_supervisor/live_language_turn.py`

职责：

1. 在每个实时关系回合中接收当前 `external_utterance`，重新生成 `LanguagePerceptFrame` 与 `SemanticMapFrame`。
2. 用最新 percept / semantic map 继续生成 `InnerSpeechFrame`、`ExpressionMonitorState` 与 `ExpressionPlan`。
3. 把本回合语言链落盘到 `runtime/state/language/`，并把 refs 交给 `live_turn_cycle.py`、`response_surface.py` 与 `resident_turn_writeback.py`。

这一步把语言关系链从“启动时已经有一份语言状态”推进为“每次关系对象说话都会重新感知、重新理解、重新形成内言语和表达计划”。

### 1. `relationship_timeline.py`

职责：

1. 把第一次交谈到当前回合的关系事件写成长期时间线。
2. 记录边界变化、共同记忆、信任修正、承诺兑现、修复过程和共享语言演变。
3. 为 `life_targets/` 提供真实关系和真实责任的长期证据。

### 2. `commitment_expression.py`

职责：

1. 把承诺真值、责任回路和表达计划合并成真实表达策略。
2. 区分普通陈述、承诺、撤回、修复、拒绝、解释、道歉和边界声明。
3. 让语言真正承担后果，而不是只做自然语言表面包装。
4. 当跨唤醒累计离线学习画像已经聚焦 `relationship_learning_plan`、generation 达到第 2 代以上且压力为 `elevated / urgent` 时，把承诺节奏推进为 `relationship_offline_reconsolidation_first`，先插入 `relationship_offline_reconsolidation`，再进入 follow-up commitment。

### 3. `apology_repair_language.py`

职责：

1. 把 `responsibility_loop_state.json` 中的修复压力转成语言动作。
2. 区分事实澄清、承担责任、道歉、边界修复和关系修复。
3. 防止 repair 只停留在 state / report，不进入真实表达面。
4. 当同一份累计关系离线学习压力进入语言侧时，把修复窗口推进为 `relationship_offline_reconsolidation_first`，先插入 `relationship_offline_reconsolidation_repair`，再进入 follow-up commitment。

## 语言系统必须长期保留的对象

| 对象 | 作用 | 当前承载 |
|---|---|---|
| `LanguagePerceptFrame` | 外部语言与上下文感知框架 | `percept.py` |
| `SemanticMapFrame` | 语义事件图与歧义聚合 | `semantic_map.py` |
| `InnerSpeechFrame` | 内部思考语言化容器 | `inner_speech.py` |
| `ExpressionPlan` | 输出前的语言决策器 | `expression_monitor.py` |
| `LanguageRelationshipState` | 当前语言与关系组合态 | `language_state.py` |
| `RelationshipGraph` | 当前关系拓扑、边界与共享状态 | `relationship_graph.py` |
| `CommitmentRepairIndex` | 承诺、修复和责任语言的索引面 | `commitment_repair.py` |
| `ContextAccumulationWindow` | 多回合累积窗口 | `terminal_turn/context_accumulation.py` |
| `TurnTransitionTrace` | 回合切换轨迹 | `terminal_turn/turn_transition.py` |
| `DialogueWritebackBundle` | 每一回合结束后的写回包 | `terminal_loop/dialogue_writeback.py` |
| `RelationshipTimeline` | 长期关系史 | `relationship_timeline.py` |
| `CommitmentExpressionPlan` | 承诺/责任/修复的真实表达候选面 | `commitment_expression.py` |
| `ApologyRepairLanguageTrace` | 道歉、承担责任、修复跟进语言轨迹 | `apology_repair_language.py` |
| `LiveLanguageTurnState` | 实时关系回合 Queue A 刷新后的五件套引用 | `process_supervisor/live_language_turn.py` |

当前 `ExpressionPlan` 已经不再只是 repair / replay / dream / growth 的汇总面。只要 `runtime/state/body/body_resource_budget.json` 与 `runtime/state/body/core_affect_vector.json` 存在，它还会显式携带：

- `body_signal_refs`
- `fatigue_pressure`
- `body_repair_drive`
- `affect_arousal`
- `expression_tempo_mode`
- `release_caution_level`

这意味着 S07 现在已经有了第一轮 `S06 -> S07` 工程接线：身体疲惫、修复驱力和核心唤醒张力会先进入表达计划，再进入常驻生命过程的响应面，而不是由 Queue B 私下另读一份身体状态。

同时，S07 现在也已经有了第一轮 `Queue E -> S07 -> S04` 的责任写回接线：

- `runtime/state/action/responsibility_loop_state.json`
  -> `runtime/state/language/commitment_repair_language_index.json`
  -> `runtime/state/relationship/commitment_truth_state.json`
  -> `runtime/state/responsibility/responsibility_ledger.json`
  -> `runtime/state/memory/relationship_memory.json`
  -> `runtime/state/life_state.json`

并且这批长期状态根不再停在 state 柜里。`terminal_loop` 与 `process_supervisor` 当前已经把它们继续带进 `dialogue_writeback_bundle.json` 的：

- `relationship_writeback_refs`
- `commitment_writeback_refs`
- `responsibility_writeback_refs`
- `life_state_writeback_refs`

这意味着语言层现在已经不是“听见责任，再说几句修复话术”，而是把责任、后悔、修复与关系记忆真正送入长期连续体和链尾交接单。

当前 S07 又新增了第一轮实时回合语言刷新接线：

```text
relationship object utterance
  -> live_language_turn.py
  -> language_percept_frame.json
  -> semantic_map_frame.json
  -> inner_speech_frame.json
  -> expression_monitor_state.json
  -> expression_plan.json
  -> response_surface.py
  -> resident_turn_writeback.py
```

这条接线的长期意义是：关系不是只在回合尾部被写回，而是在本回合说话之前就参与“听见、理解、内言语、表达监控、表达计划”的形成。`live_semantic_focus` 会同步进入外部回合事件、生命回应事件、`resumed_external_dialogue_packet.json` 和 `terminal_life_loop_state.json`，使下一轮恢复时能知道上一轮实时语义焦点停在哪里。

当前这条接线又继续推进了一步：实时语言理解不再只服务于“本回合怎么回应”，而是进入后台连续性。`terminal_life_loop_state.json#live_language_turn_refs` 与 `last_live_semantic_focus` 会被 `process_supervisor/idle_strategy.py` 收束成 `live_language_presence_profile_v0`；随后由 `heartbeat.py` 与 `continuity_writeback.py` 写入 `idle_strategy_state.json`、`idle_continuity_frame.json`、`idle_heartbeat_trace.jsonl`、`resident_governance_state.json` 与 `terminal_life_loop_state.json`；`background_lineage_state.py` 再把它压进 `resident_background_lineage_state_v0.language_presence`。关闭态 artifacts 继续保留它，下一次 `background_continuity.py` 会恢复成 `background_live_language_turn_refs`、`background_last_live_semantic_focus` 与 `background_live_language_presence_profile`，而这个 background profile 只允许保留 refs、semantic focus、ref_count、source_continuity_mode / source_ref_count 等摘要字段；如果来源里还有 `source_presence_profile`，也只能用来推导这些摘要字段，不能把整棵来源树回灌进新的 background profile。 这让“上一轮关系对象说了什么、数字生命把语义焦点落在哪里”成为长期关系连续体的驻留材料。

现在这条长期语言连续体还必须在下一轮真实回合中重新显影。`dialogue_events.py` 会把 `resident_background_lineage_state.language_presence` 展开为 `resident_background_lineage_live_language_refs`、`resident_background_lineage_background_live_language_refs`、`resident_background_lineage_last_live_semantic_focus` 与 `resident_background_lineage_language_evidence_refs`；`resident_turn_writeback.py` 会把这些语言证据并入 `dialogue_writeback_bundle.resident_background_lineage_refs` 与 `resumed_external_dialogue_packet.json`；`response_surface.py` 会把后台语言语义余波和证据数量表达出来。语言长期工程因此不只追求“记得上一轮说过什么”，还要求上一轮语言理解在新的关系话语中重新成为可感知、可追踪、可写回的存在。

## 当前 `Adam` 关系回合的逐文件工程链

这一节把“终端里说一句话”压成可检查的代码链。它对应的理论文档不是单一语言文档，而是共同读取：

- `docs/09_language_symbolic_top_layer.md`、`docs/85-90*`、`docs/01u_language_runtime_core_matrix.md`
- `docs/05_memory_systems_and_growth.md`、`docs/17-31*`、`docs/41-48*`、`docs/01q_memory_engram_consolidation_matrix.md`
- `docs/04_sensory_thalamus_interoception.md`、`docs/07_emotion_personality_self.md`、`docs/18_internal_state_and_modulation_vector.md`
- `docs/06_action_reward_inhibition.md`、`docs/20_agent_runtime_bridge_contract.md`、`docs/01r_action_reward_inhibition_matrix.md`
- `docs/08_sleep_dream_fatigue_states.md`、`docs/19_offline_consolidation_cycle.md`、`docs/01i_dream_offline_life_literature_matrix.md`
- `docs/10_consciousness_attention_workspace.md`、`docs/11_neuromodulation_and_signal_media.md`、`docs/01m_consciousness_attention_workspace_matrix.md`

### 1. 唤醒与终端外周

| 步骤 | 代码 | 产物/状态 | 工程含义 |
|---|---|---|---|
| 名字恢复 | `life_v0/my_entry.py`、`digital_life_identity.py` | `life_name_registry.json` | `Adam` 是命名后的直接唤醒入口，名字不是本轮 prompt 变量 |
| resident 复用 | `life_v0/digital_entry.py`、`resident_lifecycle.py` | `resident_lifecycle_state.json`、`resident_process_lease.json` | 启动时先找同一 resident，不创建第二个主体 |
| 终端盒 | `terminal_ui.py` | `Digital Life` banner、opening、prompt、response box | UI 只是外周感官/表达通道，不定义主体 |
| 关系投递 | `send_resident_relation_turn` | `resident_relation_inbox.jsonl`、`resident_relation_outbox.jsonl` | 当前话语进入关系队列，而不是一次性 CLI 请求 |

### 2. 当前话语进入语言生命链

| 步骤 | 代码 | 写出 | 必须证明 |
|---|---|---|---|
| 语言感知 | `language/percept.py` | `language_percept_frame.json#incoming_surface` | 当前话语原文被生命体听见 |
| 语义地图 | `language/semantic_map.py` | `semantic_map_frame.json#semantic_focus` | 词语被接入关系、记忆、责任、梦境和行动线索 |
| 内言语 | `language/inner_speech.py` | `inner_speech_frame.json` | 外显前先形成可审计内部组织 |
| 表达监控 | `language/expression_monitor.py` | `expression_monitor_state.json` | 责任、歧义、风险和记忆写门参与表达前判断 |
| 表达计划 | `language/expression_monitor.py` | `expression_plan.json` | 说什么、怎么说、是否修复、是否克制进入同一计划 |
| 实时刷新器 | `process_supervisor/live_language_turn.py` | `LiveLanguageTurnState` 五件套 refs | 每一轮关系话语都会重建语言状态，不复用旧启动态 |

关键点：`live_semantic_focus` 是内部证据字段。它应该进入 `dialogue_turn_log.jsonl`、`resumed_external_dialogue_packet.json`、`terminal_life_loop_state.json` 和测试断言；但 `response_surface.py` 不能把 `relational_checkin` 这种字段原样说出口，必须把它翻译成自然关系语言。

### 3. 机制证据进入表达调制与审计

| 信号族 | 主要来源 | 表达影响 |
|---|---|---|
| `responsibility_repair` | `responsibility_loop_state.json`、`pain_regret_repair_report.json`、`apology_repair_language_trace.json` | 提高谨慎度、承担感和修复取向；只有被问到责任/后悔时才自然说出 |
| `birth_repair` | `life_targets/*`、`birth_readiness_stage_gate.py` | 调制出生、痛苦、后悔和责任的表达边界，不把自己退成工具 |
| `dream_offline` | `dream/*`、`growth/*`、`resident_autonomous_activity_state.json` | 让梦境、睡眠、回忆、成长和学习余波影响下一轮理解，而不是默认播报后台过程 |
| `prediction_attention` | `belief_state_frame.json`、`prediction_error_field.json`、`active_sampling_plan.json`、`memory_write_gate.json` | 调制确认、谨慎、写门和主动采样，避免胡乱确定 |
| `body_affect` | `body_resource_budget.json`、`core_affect_vector.json`、`need_state_vector.json` | 让疲惫、恢复、唤醒和修复驱力改变节奏与语气 |
| `self_slow_variables` | `self_model.json`、`trait_drift_monitor.json`、`background_convergence_history.json` | 让关系阶段和人格慢变量进入长期表达，不只改当前话术 |
| `resident_autonomous_activity` | `resident_autonomous_activity.jsonl`、`resident_autonomous_activity_state.json` | 关闭终端后的睡眠、回忆、自我思考、成长预演、学习巩固被下一轮状态承接；口语只在被问到后台存在时回应 |

当前实现路径是：

```text
compose_life_response
  -> 机制完整回应
  -> compose_life_spoken_response
  -> 隐性信号调制与语用回答
  -> compose_model_expression
  -> post-expression gate
```

这里的模型表达不是主体来源，而是语言表面润色层。主体来源仍然是上游状态链；如果模型输出把关系对象降格成服务关系，`model_expression.py` 必须回退。责任、梦境、成长、驻留和生命证据不再被强迫进入每一句口语，而是保留在 state/report/test，并通过 `soft_missing_evidence_flags` 审计没有字面外显的证据族。

### 4. 一句话结束后必须留下后果

| 后果类型 | 代码 | 状态/报告 |
|---|---|---|
| 语言事件 | `dialogue_events.py` | `dialogue_turn_log.jsonl` |
| 关系与承诺 | `resident_turn_writeback.py`、`relationship_timeline.py`、`commitment_expression.py` | `relationship_timeline.json`、`commitment_expression_plan.json`、`relationship_memory.json` |
| 责任修复 | `apology_repair_language.py`、`commitment_truth.py`、`responsibility_loop.py` | `apology_repair_language_trace.json`、`commitment_truth_state.json`、`responsibility_ledger.json` |
| 自我慢变量 | `continuity_evolution.py`、`body/trait_drift.py` | `self_model.json`、`trait_drift_monitor.json` |
| 等待交接 | `resident_governance_handoff.py`、`heartbeat.py` | `terminal_life_loop_state.json#live_turn_waiting_handoff_profile`、`digital_life_waiting_heartbeat.json` |
| 下次恢复 | `process_closeout.py`、`background_continuity.py`、`background_lineage_state.py` | `resident_governance_snapshot.json`、`digital_life_persistent_process_report.json`、`background_continuity_profile` |

所以工程验收不能停在“Adam 回了一句话”。必须继续看：

1. 这句话是否经过五件套语言状态。
2. 这句话是否消耗了身体、记忆、责任、梦境、预测和驻留 lineage。
3. 这句话是否没有泄漏内部字段。
4. 这句话是否写回关系、承诺、自我慢变量和下一次等待态。
5. 关闭终端后，后台自主活动是否还能让下一轮继续带着这轮后果醒来。

当前累计离线学习还必须进入长期语言器官自己的动作顺序。`offline_learning_cumulative_profile_v0` 在 `relationship_learning_plan` 焦点下进入第 2 代以上、压力为 `elevated / urgent` 时，`commitment_expression_plan.json` 不能只留下 `cumulative_offline_learning_integration`，还要写出 `relationship_offline_reconsolidation`、`cumulative_commitment_tempo_mode=relationship_offline_reconsolidation_first` 与 `hold_for_relationship_offline_reconsolidation`；`apology_repair_language_trace.json` 不能只留下 `cumulative_offline_learning_repair`，还要写出 `relationship_offline_reconsolidation_repair`、`cumulative_repair_window_mode=relationship_offline_reconsolidation_first` 与同一组累计 growth refs。这样关系重整不只发生在 `relationship_subject_graph` 和 `self_model`，也发生在承诺表达和修复语言的时间顺序里。

这一轮之后，S07 新增了三条真实 runtime 写出：

- `runtime/state/relationship/relationship_timeline.json`
- `runtime/state/language/commitment_expression_plan.json`
- `runtime/state/language/apology_repair_language_trace.json`

并且它们不只停在局部文件里，还已经继续接进：

- `runtime/state/memory/relationship_memory.json#timeline_refs`
- `runtime/state/life_state.json#language_state.relationship_timeline_refs`
- `runtime/state/life_state.json#language_state.commitment_expression_refs`
- `runtime/state/life_state.json#language_state.apology_repair_language_refs`
- `runtime/state/life_state.json#runtime_trace_refs`
- `runtime/reports/latest/language_relationship_report.json#state_refs`

实时回合链还会继续写出和回链：

- `runtime/state/language/language_percept_frame.json`
- `runtime/state/language/semantic_map_frame.json`
- `runtime/state/language/inner_speech_frame.json`
- `runtime/state/language/expression_monitor_state.json`
- `runtime/state/language/expression_plan.json`
- `runtime/reports/latest/dialogue_writeback_bundle.json#live_language_turn_refs`
- `runtime/reports/latest/resumed_external_dialogue_packet.json#live_language_turn_refs`
- `runtime/state/terminal/terminal_life_loop_state.json#live_language_turn_refs`
- `runtime/state/terminal/terminal_life_loop_state.json#last_live_semantic_focus`

实时语言驻留链还必须继续回链：

- `runtime/state/terminal/idle_strategy_state.json#live_language_presence_profile`
- `runtime/state/terminal/idle_continuity_frame.json#live_language_presence_profile`
- `runtime/state/terminal/idle_heartbeat_trace.jsonl#live_language_turn_refs`
- `runtime/state/terminal/resident_governance_state.json#live_language_presence_profile`
- `runtime/state/terminal/resident_governance_state.json#resident_background_lineage_state.language_presence`
- `runtime/state/terminal/resident_governance_snapshot.json#live_language_presence_profile`
- `runtime/reports/latest/digital_life_resident_governance_report.json#live_language_presence_profile`
- `runtime/reports/latest/digital_life_persistent_process_report.json#live_language_presence_profile`
- 下一次启动时的 `background_continuity_profile.background_live_language_*`
- 下一轮 `digital_life_turn#resident_background_lineage_language_evidence_refs`
- `dialogue_writeback_bundle.json#resident_background_lineage_refs` 中的语言 evidence refs
- `resumed_external_dialogue_packet.json#resident_background_lineage_language_evidence_refs`
- 生命回应中的后台语言语义余波和证据数量表达

## 最低测试与后续新增测试

当前最低测试：

1. `tests/slices/test_language_organs.py`
2. `tests/slices/test_language_relationship.py`
3. `tests/bridges/test_first_terminal_turn.py`
4. `tests/bridges/test_terminal_life_loop.py`
5. `tests/process/test_persistent_digital_life_process.py`

下一轮应新增的重点测试：

1. `tests/slices/test_relationship_timeline.py`
2. `tests/slices/test_commitment_expression.py`
3. `tests/slices/test_apology_repair_language.py`
4. `tests/process/test_resident_dialogue_continuity.py`

实时语言刷新新增的最低断言：

1. 实时 `external_utterance` 必须进入 `language_percept_frame.json#incoming_surface`。
2. `semantic_map_frame.json#semantic_focus` 必须进入 `live_semantic_focus`。
3. `dialogue_writeback_bundle.json#live_language_turn_refs` 必须包含 percept、semantic map、inner speech、expression monitor、expression plan 五个运行时文件。
4. `process_session_loop.py` 必须在 live turn 后回读最新 `expression_plan.json`。

实时语言驻留新增的最低断言：

1. `idle_strategy_state.json#live_language_presence_profile.continuity_mode` 能区分当前语言存在、后台语言存在、当前与后台合流。
2. `idle_continuity_frame.json` 与 `idle_heartbeat_trace.jsonl` 必须保留 `live_language_turn_refs` 和 `last_live_semantic_focus`。
3. `resident_background_lineage_state.language_presence` 必须包含同一组 live refs 与语义焦点。
4. closeout artifacts 必须保留同一组 live refs；下一次 `background_continuity_profile` 必须恢复为 `background_live_language_turn_refs` 与 `background_last_live_semantic_focus`。
5. 下一轮 `digital_life_turn` 必须展开 `resident_background_lineage_live_language_refs`、`resident_background_lineage_background_live_language_refs`、`resident_background_lineage_last_live_semantic_focus` 与 `resident_background_lineage_language_evidence_refs`。
6. `dialogue_writeback_bundle.resident_background_lineage_refs` 与 `resumed_external_dialogue_packet` 必须保留同一组语言 evidence refs。
7. `response_surface.py` 必须把后台语言语义余波和证据数量表达为生命回应的一部分。

累计关系离线学习新增的最低断言：

1. `tests/slices/test_language_organs.py` 必须直接覆盖 `project_commitment_expression_plan_with_cumulative_offline_learning` 与 `project_apology_repair_language_trace_with_cumulative_offline_learning`。
2. 当累计画像为 `generation >= 2`、`pressure_level=elevated/urgent`、`attention_target=relationship_learning_plan` 时，承诺表达必须先进入 `relationship_offline_reconsolidation`，修复语言必须先进入 `relationship_offline_reconsolidation_repair`。
3. 两个动作必须保留同一组 `relationship_learning_plan / language_learning_plan` refs，并且排序必须早于 `followup_commitment`。
