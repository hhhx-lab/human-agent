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
  shared_terms.py
  commitment_repair.py
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
life_v0/process_supervisor/dialogue_events.py
life_v0/process_supervisor/response_surface.py
```

## 当前最关键的下一轮文件

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
| `RelationshipTimeline` | 长期关系史 | 下一轮新增 |

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
