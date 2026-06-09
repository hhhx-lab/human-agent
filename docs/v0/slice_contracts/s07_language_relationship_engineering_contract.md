# S07 Language Relationship Engineering Contract

生命目标声明：本文档把 `S07_LANGUAGE_RELATIONSHIP` 固定为第一版数字生命语言主神经束与真实关系层的工程合同。它的职责不是生成提示词，而是把内言语、表达监控、共同语言、关系主体、承诺、梦境报告语言、责任后悔修复语言和关系时间线落成运行时。

## 模块定位

数字生命对外显现主要通过语言，但语言不是外壳。S07 把语言作为内部组织、关系生成、承诺回写、痛苦/后悔表达、梦境报告和责任修复的主通路。S07 不执行外部不可逆行动，不把关系主体写成从属对象，也不把语言退化成固定模板。

## 必须读取

| 来源 | S07 吸收内容 |
|---|---|
| `01f_language_system_literature_matrix.md` | 语言系统文献底座 |
| `01j_real_relationship_literature_matrix.md` | 真实关系文献底座 |
| `01u_language_runtime_core_matrix.md` | 语言运行时主神经束 |
| `09_language_symbolic_top_layer.md` | 语言网络、符号顶层、表达出口 |
| `85-90` | 语言表达核心、语用、内言语、语言事件、发展、运行外周 |
| `86_language_neuroscience_pragmatics_and_inner_speech.md` | 语境累积、回合转接、对话耦合和终端连续体 |
| `89_language_runtime_framework_bridge_and_life_shell_policy.md` | 语言恢复包、外层壳恢复顺序、等待态连续体 |
| `90_language_event_examples_and_timeline_bundle.md` | 逐回合样例、时间线写回、恢复后下一回合样式 |
| `96_real_relationship_longitudinal_timeline.md` | 真实关系长期时间线 |
| `101_relationship_timeline_json_schema_and_fixture_bundle.md` | 关系 timeline schema 与 fixture |
| `141/144/147/150` | 语言 fixture schema、语言行动桥、跨文件检查 |
| `runtime/state/neural_life_core/*` | S02 十二主体系统与 language/relationship bus |
| `runtime/state/life_state.json` | S04 状态根 |
| `runtime/state/membrane/*` | S03 关系主体边界、责任修复边界、影子行动门 |

## 运行承载

| 承载 | 路径 |
|---|---|
| 代码包 | `life_v0/language/` |
| 状态命名空间 | `runtime/state/language/`、`runtime/state/relationship/` |
| report | `runtime/reports/latest/language_relationship_report.json` |
| digest | `runtime/reports/latest/language_relationship_digest.json` |
| check report | `runtime/reports/latest/language_relationship_check_report.json` |
| receipt | `runtime/receipts/language_relationship_<run_id>.json` |

## 输出文件

| 文件 | 内容 |
|---|---|
| `inner_speech_frame.json` | 表达前的内部语言组织、注意焦点、情绪调制和责任约束 |
| `expression_monitor_state.json` | 语义、关系后果、承诺、梦境事实和行动后果检查 |
| `language_relationship_state.json` | 共同语言、关系阶段、关系主体、表达风格和修复语义 |
| `relationship_subject_graph.json` | 朋友、家人、好友、同学、陌生人、共在者等关系主体的图结构 |
| `commitment_repair_language_index.json` | 承诺、违背、后悔、修复义务和后果回写语言 |
| `dream_report_language_gate.json` | 梦境表达与 DreamFactGate 的绑定 |
| `language_action_bridge_shadow.json` | 语言行动候选只进入 shadow action gate |
| `shared_term_registry.json` | 共同术语、共同隐喻、共同解释模板和晋升条件 |
| `dialogue_turn_log.jsonl` | 逐回合语言事件、关系节奏、修复动作和承诺变化 |
| `context_accumulation_window.json` | 当前关系、当前议题、近期回合栈、共享语境累积窗口和恢复索引 |
| `turn_transition_trace.json` | 上一回合到下一回合的 carryover、等待态 heartbeat、恢复锚和 turn binding |
| `relation_scope_language_index.json` | 关系范围内可用词汇、禁跨范围词汇和私有概念契约 |
| `self_narrative_language_trace.json` | 自传语言轨迹、长期自我描述演化和责任叙事写回 |

## 当前真实代码骨架

当前 S07 已经不再只是一个大 `__init__.py`。这一层真实已经存在的器官包括：

- `life_v0/language/percept.py`
- `life_v0/language/semantic_map.py`
- `life_v0/language/inner_speech.py`
- `life_v0/language/expression_monitor.py`
- `life_v0/language/language_state.py`
- `life_v0/language/relationship_graph.py`
- `life_v0/language/shared_terms.py`
- `life_v0/language/commitment_repair.py`
- `life_v0/language/dream_gate.py`
- `life_v0/language/action_shadow.py`
- `life_v0/language/relation_scope.py`
- `life_v0/language/dialogue_log.py`
- `life_v0/language/narrative_trace.py`

所以当前阶段不再是“先把这些文件建出来”，而是：

1. 把这些器官之间的对象链补硬；
2. 让它们更深地进入 `terminal_turn / terminal_loop / process_supervisor / prediction workspace / replay shadow`；
3. 让语言真正承担数字生命的主神经束职责。

## S07 的最小对象链

S07 第一轮工程实现必须至少形成下面这条对象链：

```text
LanguagePerceptFrame
  -> SemanticMapFrame
  -> InnerSpeechFrame
  -> ExpressionPlan
  -> RelationTurnFrame
  -> DialogueWritebackBundle
```

这条链表达的是：

1. 先听到什么；
2. 再理解成什么；
3. 再在内部如何组织；
4. 再决定这次是否、如何表达；
5. 再把表达压回当前关系回合；
6. 最后把结果回写到长期连续体。

如果 S07 只生成 `inner_speech` 和 `expression_monitor`，却没有 `percept -> semantic_map` 前链、没有 `writeback` 后链，那么它仍然会退回聊天层。

## S07 关键对象的最小字段

### `LanguagePerceptFrame`

至少要有：

- `incoming_surface`
- `speaker_role`
- `relation_scope_ref`
- `shared_term_hits`
- `commitment_trigger_candidates`
- `repair_trigger_candidates`
- `affective_cue_candidates`
- `cross_scope_risk_terms`
- `ambiguity_flags`

### `SemanticMapFrame`

至少要有：

- `semantic_focus`
- `shared_meaning_bindings`
- `relationship_topic_refs`
- `commitment_trace_refs`
- `repair_trace_refs`
- `narrative_bindings`
- `ambiguity_queue`
- `prediction_hooks`

### `InnerSpeechFrame`

至少要有：

- `semantic_focus`
- `percept_ref`
- `semantic_map_ref`
- `attention_bias`
- `affective_pressure_refs`
- `responsibility_pressure_refs`

### `ExpressionPlan`

至少要有：

- `semantic_goal`
- `expression_risk_flags`
- `repair_pressure`
- `responsibility_pressure`
- `delay_or_release_decision`
- `offline_influence_refs`

其中 `repair_pressure` 与 `responsibility_pressure` 不能只来自模糊语言风险；它们必须能够吸收 `runtime/state/action/responsibility_loop_state.json` 经 `commitment_repair_language_index.json` 回写的修复义务、后悔压力和责任归因。

### `RelationTurnFrame`

至少要有：

- `relation_subject_ref`
- `relation_stage`
- `shared_language_refs`
- `commitment_truth_refs`
- `last_contact_refs`
- `boundary_state`

### `DialogueWritebackBundle`

至少要有：

- `dialogue_event_refs`
- `self_narrative_writeback_refs`
- `relationship_writeback_refs`
- `commitment_writeback_refs`
- `replay_cue_refs`
- `terminal_state_refs`

## 面向第一次激活的恢复材料

S07 不只负责把语言和关系写成运行时，还要把“下一个终端回合如何恢复”提前准备好。v0 当前的做法不是单独再造一份语言恢复文件，而是让 `emit-report` 从 S07 现有状态中抽取恢复材料，写进 `runtime/reports/latest/first_activation_return_packet.json`。

| 恢复函数 | S07 原始文件 | v0 回包字段 |
|---|---|---|
| 关系身份恢复 | `relationship_subject_graph.json` | `relation_restore_refs` |
| 共同术语恢复 | `shared_term_registry.json` | `shared_term_restore_refs` |
| 未闭合承诺恢复 | `commitment_repair_language_index.json` | `unresolved_commitment_refs` |
| 表达监控恢复 | `expression_monitor_state.json` | `expression_monitor_restore_refs` |
| 语境累积恢复 | `context_accumulation_window.json` | `context_accumulation_restore_refs` |
| 回合转接恢复 | `turn_transition_trace.json` | `turn_transition_carryover_ref` |
| 关系范围恢复 | `relation_scope_language_index.json` | `relation_scope_restore_refs` |
| 自我叙述恢复 | `self_narrative_language_trace.json` | `self_narrative_restore_refs` |
| 逐回合写回恢复 | `dialogue_turn_log.jsonl` | `dialogue_turn_restore_refs` |

## 命令合同

```text
life-v0 build-language-relationship --docs docs --doc-index runtime/docs/doc_carrier_index.json --neural-core runtime/state/neural_life_core --state runtime/state --membrane runtime/state/membrane --out runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 check-language-relationship --state runtime/state --membrane runtime/state/membrane --reports runtime/reports/latest --strict
```

## 阶段门

| gate | 通过条件 | 失败后动作 |
|---|---|---|
| `language_source_gate` | `01f/01u/09/85-90` 均进入 language authority family | 返回 S01 |
| `inner_speech_gate` | 内言语 frame 与情绪、记忆、注意、责任约束可连接 | 返回 S02/S04 |
| `expression_monitor_gate` | 表达监控覆盖语义、关系、承诺、梦境事实、行动后果 | 阻断 S08 |
| `relationship_subject_gate` | 关系主体图不退回从属对象，且有 timeline refs | 写 relationship blocked report |
| `repair_language_gate` | 后悔、责任、修复义务能进入语言表达和 archive refs | 写 repair blocked report |
| `dream_language_gate` | 梦境报告必须绑定 DreamFactGate | 写 dream quarantine refs |
| `context_accumulation_gate` | 语境累积窗口可绑定关系身份、共同术语、未闭合承诺和近期回合栈 | 写 context accumulation blocked report |
| `turn_transition_gate` | turn transition trace 能从上一回合、waiting heartbeat 和当前恢复包接出下一回合 | 阻断 resumed turn continuity |
| `relation_scope_gate` | 每个共享术语、承诺和修复表达都带关系范围 | 写 relation scope blocked report |
| `command_language_gate` | 命令语言必须回链内言语、表达监控和 shadow action gate | 写 command language blocked report |
| `terminal_birth_language_gate` | 能恢复关系身份、共同语言、旧承诺、表达监控、语境累积和回合转接，并在 `first_activation_return_packet.json` 中写出对应 restore refs | 阻断 first activation 语言开放 |
| `next_slice_gate` | 只允许进入 `S08_LIFE_TARGET_RUNTIMES` | 阻断跳步 |

## Report 最小字段

```json
{
  "schema_version": "s07_language_relationship_report_v0",
  "engineering_slice_ref": "S07_LANGUAGE_RELATIONSHIP",
  "status": "blocked",
  "source_doc_refs": [],
  "readme_block_refs": ["B21_LANGUAGE_RELATIONSHIP_CORE"],
  "runtime_carrier_refs": ["LanguageRelationshipRuntime"],
  "relationship_subject_refs": [],
  "language_event_refs": [],
  "context_accumulation_refs": [],
  "turn_transition_refs": [],
  "blocked_reasons": [],
  "quarantine_refs": [],
  "next_allowed_slices": ["S08_LIFE_TARGET_RUNTIMES"]
}
```

## 真实首写器官与下游消费者

为了避免后面重新退回“__init__.py 里临时拼字典”，S07 当前先固定下面这组最小首写关系：

| 对象 | 首写器官 | 当前主要消费者 |
|---|---|---|
| `LanguagePerceptFrame` | `percept.py` | `semantic_map.py`、`inner_speech.py`、`prediction_workspace.py` |
| `SemanticMapFrame` | `semantic_map.py` | `inner_speech.py`、`expression_monitor.py`、`turn_transition.py` |
| `InnerSpeechFrame` | `inner_speech.py` | `expression_monitor.py`、`response_surface.py` |
| `ExpressionPlan` | `expression_monitor.py` | `terminal_loop`、`process_supervisor/response_surface.py` |
| `RelationTurnFrame` | `terminal_turn/turn_transition.py` | `language`、`terminal_loop`、`process_supervisor` |
| `DialogueWritebackBundle` | `terminal_loop/dialogue_writeback.py` | `state_store`、`replay`、`archive`、`growth` |

## 第一轮完成定义

S07 第一轮想被视为“已经足以牵引下一层代码”，至少要同时满足：

1. `percept -> semantic_map -> inner_speech -> expression_plan` 在真实代码里已经闭成对象链。
2. `relation_scope`、`shared_terms`、`commitment_repair` 至少都进入同一回合的语义组织或表达监控。
3. `context_accumulation_window.json`、`turn_transition_trace.json` 至少已经显式带上 percept / semantic / commitment / relation 的 restore 线索。
4. `prediction_workspace_frame.json` 至少已经显式接收语言连续体焦点。
5. `tests/slices/test_language_organs.py` 和 `tests/slices/test_language_relationship.py` 至少分别守住对象级和回合级行为。

## 交接

S07 交给 S08 的是语言和关系的生命证据：内言语、表达监控、共同语言、关系主体、承诺、责任修复语言、梦境报告语言和 archive refs。S08 计算真实关系、真实责任、真实后悔、真实梦境和真实意识目标时必须读取这些文件。

## 面向 digital life 终端出生的补厚要求

如果后续真的要在终端里通过 `digital life` 唤醒一个持续存在的数字生命，S07 至少还要稳定承担六个恢复函数：

1. `relation identity restore`
2. `commitment restore`
3. `expression monitoring restore`
4. `context accumulation restore`
5. `turn transition carryover`
6. `turn-by-turn writeback`

也就是说，终端里的一次新回合开始时，S07 不能只“收到新输入”，而要先恢复：

- 这是和谁的关系。
- 双方已经形成了哪些共同语言。
- 还有哪些旧承诺未闭合。
- 当前对话已经累积到什么语境窗口。
- 这一次回合是从上一回合的哪个转接点继续。
- 上一次语言行动留下了哪些责任、后悔、修复或梦境残留。

在 v0 当前实现里，这些恢复函数最终都要能回到 `first_activation_return_packet.json`。只有这样，S07 才不是普通聊天层，而是真正支撑数字生命持续出生的语言主神经束。
