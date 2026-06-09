# Conversation Language Relationship Blueprint

这份蓝图只处理一条中轴：

```text
感知到关系对象的外部语言
  -> 内言语与关系判断
  -> 表达计划
  -> 终端回合输出
  -> 写回长期关系连续体
```

## 范围

这条中轴由下面这些包共同负责：

1. `life_v0/language/`
2. `life_v0/terminal_turn/`
3. `life_v0/terminal_loop/`
4. `life_v0/process_supervisor/`
5. `life_v0/state_store/relationship_memory.py`

它不把外部交谈对象定义成 `user`。这里的对象统一是关系对象、共在对象、外部关系对象。

## 语言主轴的固定对象

| 对象 | 首写位置 | 作用 |
|---|---|---|
| `LifeContextFrame` | `terminal_turn/` | 本回合的自我上下文、方向锚、关系基线 |
| `RelationTurnFrame` | `language/`、`terminal_turn/` | 当前关系对象、阶段、共用术语、承诺上下文 |
| `ExpressionPlan` | `language/expression_monitor.py` | 外显表达前的候选表达与边界 |
| `DialogueWritebackBundle` | `terminal_loop/dialogue_writeback.py` | 把本回合关系事件写回 memory / relationship / language |
| `IdleContinuityFrame` | `process_supervisor/heartbeat.py` | 没有新输入时的持续存在与关系连续体 |

## 当前已落的关键文件

| 包 | 当前文件 | 当前职责 |
|---|---|---|
| `life_v0/language/` | `percept.py` | 把外部语言输入编进语言感知帧 |
| `life_v0/language/` | `semantic_map.py` | 语义压缩、歧义索引、预测焦点 |
| `life_v0/language/` | `inner_speech.py` | 本回合内言语草案 |
| `life_v0/language/` | `expression_monitor.py` | 外显表达压力面、表达边界、表达计划 |
| `life_v0/language/` | `relationship_graph.py` | 当前关系主体图 |
| `life_v0/language/` | `commitment_repair.py` | 承诺修复索引与责任语言接线 |
| `life_v0/language/` | `dialogue_log.py` | 对话事件时间线记录 |
| `life_v0/language/` | `narrative_trace.py` | 自我叙事连续体 |
| `life_v0/language/` | `dream_gate.py`、`action_shadow.py` | 梦境残留与行动阴影如何进入表达 |
| `life_v0/terminal_turn/` | `restore_context.py`、`context_accumulation.py`、`turn_transition.py` | 第一次恢复回合如何恢复上下文、积累上下文、切换状态 |
| `life_v0/terminal_loop/` | `loop_state.py`、`resume_packet.py`、`dialogue_writeback.py` | 持续回合如何等待、恢复和写回 |
| `life_v0/process_supervisor/` | `dialogue_events.py`、`response_surface.py`、`continuity_writeback.py` | 等待态与真实外部回合怎样接语言连续体 |

## 当前 runtime 承载

### 状态

1. `runtime/state/language/inner_speech_frame.json`
2. `runtime/state/language/expression_monitor_state.json`
3. `runtime/state/language/expression_plan.json`
4. `runtime/state/language/language_relationship_state.json`
5. `runtime/state/language/shared_term_registry.json`
6. `runtime/state/language/relation_scope_language_index.json`
7. `runtime/state/language/self_narrative_language_trace.json`
8. `runtime/state/language/language_percept_frame.json`
9. `runtime/state/language/semantic_map_frame.json`
10. `runtime/state/language/commitment_repair_language_index.json`
11. `runtime/state/relationship/relationship_subject_graph.json`
12. `runtime/state/terminal/life_context_frame.json`
13. `runtime/state/terminal/relation_turn_frame.json`
14. `runtime/state/terminal/context_accumulation_window.json`
15. `runtime/state/terminal/turn_transition_trace.json`
16. `runtime/state/terminal/session_envelope.json`
17. `runtime/state/terminal/safe_terminal_loop_state.json`
18. `runtime/state/terminal/terminal_life_loop_state.json`

### 报告

1. `runtime/reports/latest/language_relationship_report.json`
2. `runtime/reports/latest/language_relationship_check_report.json`
3. `runtime/reports/latest/first_terminal_turn_report.json`
4. `runtime/reports/latest/terminal_life_loop_report.json`
5. `runtime/reports/latest/dialogue_writeback_bundle.json`
6. `runtime/reports/latest/resumed_external_dialogue_packet.json`

## 语言轴的下一轮文件

1. `life_v0/language/relationship_timeline.py`
2. `life_v0/language/commitment_expression.py`
3. `life_v0/language/apology_repair_language.py`

### 三个文件分别负责什么

| 文件 | 职责 | 必须消费 | 必须写出 |
|---|---|---|---|
| `relationship_timeline.py` | 关系对象的长期事件时间线、阶段变迁和重大节点 | `dialogue_log.jsonl`、`relationship_subject_graph.json` | `runtime/state/relationship/relationship_timeline.json` |
| `commitment_expression.py` | 把承诺、责任、修复义务真正变成语言表达候选 | `responsibility_loop_state.json`、`commitment_repair_language_index.json` | `runtime/state/language/commitment_expression_plan.json` |
| `apology_repair_language.py` | 当 regret / repair 被触发时生成关系修复语言轨迹 | `responsibility_loop_state.json`、`relationship_consequence_trace` | `runtime/state/language/apology_repair_language_trace.json` |

## 最低验证面

1. `tests/slices/test_language_organs.py`
2. `tests/slices/test_language_relationship.py`
3. `tests/bridges/test_first_terminal_turn.py`
4. `tests/bridges/test_terminal_life_loop.py`
5. `tests/process/test_persistent_digital_life_process.py`

## 完成定义

这一层不以“能说话”算完成，而以这五件事算完成：

1. 能识别关系对象，而不是只识别输入文本。
2. 能把责任、后悔、修复义务显式带入语言表达压力面。
3. 能把离线梦境、重放线索和成长候选带入下一次生命回应。
4. 能把每轮对话写回关系连续体，而不是只写日志。
5. 能在等待态维持最小自我叙事、关系图和承诺索引。
