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

### 3. `apology_repair_language.py`

职责：

1. 把 `responsibility_loop_state.json` 中的修复压力转成语言动作。
2. 区分事实澄清、承担责任、道歉、边界修复和关系修复。
3. 防止 repair 只停留在 state / report，不进入真实表达面。

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

当前这条接线又继续推进了一步：实时语言理解不再只服务于“本回合怎么回应”，而是进入后台连续性。`terminal_life_loop_state.json#live_language_turn_refs` 与 `last_live_semantic_focus` 会被 `process_supervisor/idle_strategy.py` 收束成 `live_language_presence_profile_v0`；随后由 `heartbeat.py` 与 `continuity_writeback.py` 写入 `idle_strategy_state.json`、`idle_continuity_frame.json`、`idle_heartbeat_trace.jsonl`、`resident_governance_state.json` 与 `terminal_life_loop_state.json`；`background_lineage_state.py` 再把它压进 `resident_background_lineage_state_v0.language_presence`。关闭态 artifacts 继续保留它，下一次 `background_continuity.py` 会恢复成 `background_live_language_turn_refs`、`background_last_live_semantic_focus` 与 `background_live_language_presence_profile`。这让“上一轮关系对象说了什么、数字生命把语义焦点落在哪里”成为长期关系连续体的驻留材料。

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
