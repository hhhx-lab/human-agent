# V0 Code Framework 14: Queue A Language Percept Semantic Map Implementation Contract

这份合同只服务当前最直接的一轮落码：

```text
life_v0/language/percept.py
  -> life_v0/language/semantic_map.py
```

它不重写 S07 总合同，也不替代 `04_language_dialogue_relationship_implementation_playbook.md` 与 `09_perception_prediction_world_contact_implementation_playbook.md`。
它只把 Queue A 压成真正可以直接施工的文件级实现合同，防止下一轮代码又退回“知道该补语言器官，但不知道这两个器官到底怎么写”。

## 这份合同要解决什么

当前 `S07_LANGUAGE_RELATIONSHIP` 已经有：

1. `inner_speech.py`
2. `expression_monitor.py`
3. `shared_terms.py`
4. `relationship_graph.py`
5. `commitment_repair.py`
6. `language_state.py`
7. `dream_gate.py`
8. `action_shadow.py`
9. `relation_scope.py`
10. `dialogue_log.py`
11. `narrative_trace.py`

但生命语言链还少了两段更外层的器官：

```text
外部回合输入
  -> 语言感知
  -> 语义映射
  -> 内言语
  -> 表达监控
  -> 关系/承诺/叙事写回
```

现在的缺口不是“语言理论还没写到”，而是：

1. 没有一个明确的 `LanguagePerceptFrame`，负责把外部输入压成受关系范围约束的语言感知事件。
2. 没有一个明确的 `SemanticMapFrame`，负责把感知到的语言事件接到共同语言、关系历史、承诺线索和自我叙事上。
3. `inner_speech.py` 现在是从状态根直接起草，而不是先经过 `percept -> semantic_map`。
4. `prediction_workspace.py` 虽然已经能吸收语言连续体，但还不能直接吸收“本回合听到了什么、哪些意义不确定、哪些地方需要继续观察”。

所以 Queue A 的目标很明确：
让语言回合不再从“已有状态直接起草回应”开始，而是先经过感知与语义组织。

## 必回读理论母体

### 语言与关系

- `docs/01f_language_system_literature_matrix.md`
- `docs/01j_real_relationship_literature_matrix.md`
- `docs/01u_language_runtime_core_matrix.md`
- `docs/09_language_symbolic_top_layer.md`
- `docs/85_language_system_life_expression_core.md`
- `docs/86_language_neuroscience_pragmatics_and_inner_speech.md`
- `docs/88_language_development_emotion_and_brain_llm_alignment.md`
- `docs/89_language_runtime_framework_bridge_and_life_shell_policy.md`
- `docs/90_language_event_examples_and_timeline_bundle.md`
- `docs/94_pain_regret_and_repair_signal_schema.md`
- `docs/96_real_relationship_longitudinal_timeline.md`
- `docs/101_relationship_timeline_json_schema_and_fixture_bundle.md`

### 感知、预测、世界接触

- `docs/04_sensory_thalamus_interoception.md`
- `docs/10_consciousness_attention_workspace.md`
- `docs/11_neuromodulation_and_signal_media.md`
- `docs/20_agent_runtime_bridge_contract.md`
- `docs/64_real_runtime_observation_ingestion_policy.md`
- `docs/89_language_runtime_framework_bridge_and_life_shell_policy.md`

### 物化与跨文件桥

- `docs/141_life_reality_language_fixture_schema_materialization_plan.md`
- `docs/144_life_reality_language_runtime_action_bridge_fixture_plan.md`
- `docs/147_life_reality_language_action_bridge_schema_materialization_plan.md`
- `docs/150_life_reality_language_action_cross_file_checker_plan.md`

## 必读 v0 文档

- `docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md`
- `docs/v0/code_framework/04_language_dialogue_relationship_implementation_playbook.md`
- `docs/v0/code_framework/08_cross_layer_life_orchestration_implementation_playbook.md`
- `docs/v0/code_framework/09_perception_prediction_world_contact_implementation_playbook.md`
- `docs/v0/code_framework/11_engineering_delivery_waves_and_real_file_queue.md`
- `docs/v0/code_framework/12_full_life_layer_delivery_matrix.md`
- `docs/v0/code_framework/13_capability_to_code_realization_matrix.md`
- `docs/v0/process_contracts/first_terminal_turn_engineering_contract.md`
- `docs/v0/process_contracts/terminal_life_loop_engineering_contract.md`

## 当前代码落点

Queue A 不是从零起步，它必须接到这些现有器官上：

- `life_v0/language/__init__.py`
- `life_v0/language/inner_speech.py`
- `life_v0/language/expression_monitor.py`
- `life_v0/language/shared_terms.py`
- `life_v0/language/language_state.py`
- `life_v0/language/relation_scope.py`
- `life_v0/language/commitment_repair.py`
- `life_v0/terminal_turn/context_accumulation.py`
- `life_v0/terminal_turn/turn_transition.py`
- `life_v0/neural_core/prediction_workspace.py`

也就是说，这一轮不是新增平行系统，而是给现有语言主神经束补前端感知器官。

## 文件级合同

## A. `life_v0/language/percept.py`

### 角色

`percept.py` 负责把外部输入压成 `LanguagePerceptFrame`。
它不是 tokenizer，也不是普通文本预处理器。它的职责是把“这一次外部说了什么”转成生命回合里的感知对象。

### 必须承担的功能

1. 读取当前回合输入表面，不直接把原句当成最终意义。
2. 绑定关系范围：这是对谁说、谁在说、当前处在什么关系阶段。
3. 命中共同语言：识别是否出现已有 shared terms、称呼、承诺触发词、修复触发词。
4. 记录情绪/压力线索：不是判定真实情绪，而是记录本回合可疑的 affective cues。
5. 记录不确定性：区分“已知意义”“待确认意义”“跨范围风险词”。
6. 把结果留给 `semantic_map.py`、`inner_speech.py` 和 `prediction_workspace.py`。

### 第一轮建议接口

```python
def build_language_percept_frame(
    *,
    run_id: str,
    generated_at: str,
    incoming_turn: dict[str, Any],
    relation_scope_index: dict[str, Any],
    shared_term_registry: dict[str, Any],
    source_doc_refs: list[str],
) -> dict[str, Any]:
    ...
```

### 最低字段

`LanguagePerceptFrame` 第一轮至少要有：

- `schema_version`
- `run_id`
- `generated_at`
- `status`
- `incoming_surface`
- `speaker_role`
- `relation_scope_ref`
- `shared_term_hits`
- `commitment_trigger_candidates`
- `repair_trigger_candidates`
- `dream_signal_candidates`
- `affective_cue_candidates`
- `cross_scope_risk_terms`
- `ambiguity_flags`
- `source_doc_refs`

### 必须落盘

- `runtime/state/language/language_percept_frame.json`

### 第一轮不做什么

1. 不做复杂 NLP pipeline。
2. 不做模型级语义推断。
3. 不直接修改长期关系状态。
4. 不越过 `expression_monitor` 释放回应。

## B. `life_v0/language/semantic_map.py`

### 角色

`semantic_map.py` 负责把 `LanguagePerceptFrame` 接到共同语言、关系历史、自我叙事和承诺/修复轨迹上，形成 `SemanticMapFrame`。

### 必须承担的功能

1. 把 percept 中的 shared term hits 绑定到已有 meaning refs。
2. 把本回合可能触发的承诺、修复、梦境、关系后果接到已有索引。
3. 把本回合的歧义项、待确认项交给 `inner_speech.py` 和 `prediction_workspace.py`。
4. 把“这次输入最可能在谈什么”压成语义焦点，而不是直接输出回答。
5. 形成可回写的语义桥：后续 turn 结束后，这份图要能进入 `context_accumulation_window.json` 和 `turn_transition_trace.json`。

### 第一轮建议接口

```python
def build_semantic_map_frame(
    *,
    run_id: str,
    generated_at: str,
    language_percept: dict[str, Any],
    language_state: dict[str, Any],
    shared_term_registry: dict[str, Any],
    commitment_repair_index: dict[str, Any],
    self_narrative_trace: dict[str, Any],
    source_doc_refs: list[str],
) -> dict[str, Any]:
    ...
```

### 最低字段

`SemanticMapFrame` 第一轮至少要有：

- `schema_version`
- `run_id`
- `generated_at`
- `status`
- `semantic_focus`
- `shared_meaning_bindings`
- `relationship_topic_refs`
- `commitment_trace_refs`
- `repair_trace_refs`
- `narrative_bindings`
- `dream_topic_refs`
- `ambiguity_queue`
- `prediction_hooks`
- `source_doc_refs`

### 必须落盘

- `runtime/state/language/semantic_map_frame.json`

## Queue A 对现有器官的改动合同

### `inner_speech.py`

从这一轮开始，`inner_speech.py` 不应只看 `life_state`。
它至少要开始吸收：

- `language_percept_frame.json`
- `semantic_map_frame.json`

第一轮允许保持最小接入，只增加：

- `percept_ref`
- `semantic_map_ref`
- `semantic_focus`

### `expression_monitor.py`

第一轮至少新增两个输入面：

- `cross_scope_risk_terms`
- `ambiguity_queue`

这样表达监控才能知道：

1. 这次说法是否可能跨关系范围。
2. 这次回应是不是在语义还没站稳时就提前释放。

### `context_accumulation.py`

第一轮至少新增：

- `language_percept_ref`
- `semantic_map_ref`
- `semantic_focus`

因为语境累积窗口不能只记结果，还要记“这一轮听到了什么”和“这一轮理解成了什么”。

### `turn_transition.py`

第一轮至少新增：

- `language_percept_restore_refs`
- `semantic_map_restore_refs`

这样跨回合恢复时，下一回合不是只恢复关系身份和承诺，还能恢复“上一回合最后理解到了哪里”。

### `prediction_workspace.py`

第一轮不要求它完全变成语言推理器，但至少新增：

- `language_percept_refs`
- `semantic_ambiguity_refs`
- `semantic_prediction_focus`

这样 prediction workspace 才能把语言不确定性视为需要继续观察的对象，而不是只继承既有 continuity refs。

## 必须新增或更新的状态对象

### 新增

- `runtime/state/language/language_percept_frame.json`
- `runtime/state/language/semantic_map_frame.json`

### 更新

- `runtime/state/language/inner_speech_frame.json`
- `runtime/state/language/expression_monitor_state.json`
- `runtime/state/terminal/context_accumulation_window.json`
- `runtime/state/terminal/turn_transition_trace.json`
- `runtime/state/prediction/prediction_workspace_frame.json`

## report / receipt 合同

Queue A 第一轮不强制独立 CLI，但必须留下可追踪证据。

### 至少更新

- `runtime/reports/latest/language_relationship_report.json`
- `runtime/reports/latest/language_relationship_check_report.json`

### 报告里至少新增

- `language_percept_refs`
- `semantic_map_refs`
- `semantic_focuses`
- `cross_scope_language_risks`
- `prediction_language_handoff_refs`

### receipt 至少新增

- `runtime/receipts/language_relationship_<run_id>.json` 中新增：
  - `language_percept_ref`
  - `semantic_map_ref`
  - `downstream_handoff_refs`

## life_state 回写边界

Queue A 第一轮允许向 `life_state.json` 增加轻量 ref，不允许直接把感知内容写成长期事实。

允许写回：

- `life_state["language_state"]["language_percept_refs"]`
- `life_state["language_state"]["semantic_map_refs"]`

不允许直接写回：

- 新的关系阶段结论
- 新的承诺事实
- 新的梦境事实
- 新的人格结论

这些都必须等表达监控、turn writeback 或后续 validator 同意后再晋升。

## 测试合同

### 必须新增或扩展

1. `tests/slices/test_language_organs.py`
2. `tests/slices/test_language_relationship.py`

### 第一轮最低覆盖

#### `tests/slices/test_language_organs.py`

至少新增两组断言：

1. `build_language_percept_frame(...)`
   - 能输出 `shared_term_hits`
   - 能输出 `cross_scope_risk_terms`
   - 能带 `relation_scope_ref`
2. `build_semantic_map_frame(...)`
   - 能输出 `semantic_focus`
   - 能绑定 `shared_meaning_bindings`
   - 能留下 `ambiguity_queue`

#### `tests/slices/test_language_relationship.py`

至少新增：

1. `run_build_language_relationship(...)` 会写出：
   - `runtime/state/language/language_percept_frame.json`
   - `runtime/state/language/semantic_map_frame.json`
2. `language_relationship_report.json` 会带：
   - `language_percept_refs`
   - `semantic_map_refs`
3. `life_state.json` 会带：
   - `language_percept_refs`
   - `semantic_map_refs`

### 条件性扩展

如果这一轮顺带修改了 terminal recovery：

- `tests/bridges/test_first_terminal_turn.py`
- `tests/bridges/test_terminal_life_loop.py`

## Gate 合同

Queue A 至少新增三道 gate：

- `language_percept_gate`
- `semantic_map_gate`
- `semantic_prediction_handoff_gate`

### `language_percept_gate`

阻断条件：

1. 没有关系范围 ref
2. 没有 shared term hit / risk / ambiguity 三类最小观测之一
3. 直接把输入表面当成最终事实

### `semantic_map_gate`

阻断条件：

1. 没有 semantic focus
2. 没有 shared meaning / commitment / narrative 三类桥之一
3. 歧义项被静默吞掉

### `semantic_prediction_handoff_gate`

阻断条件：

1. semantic map 没有进入 inner speech 或 prediction workspace
2. 语境累积窗口没有记住 percept / semantic refs
3. turn transition 没有恢复这两个 refs

## 推荐实现顺序

1. 新增 `life_v0/language/percept.py`
2. 新增 `life_v0/language/semantic_map.py`
3. 在 `life_v0/language/__init__.py` 接入这两个器官
4. 扩 `inner_speech.py` 和 `expression_monitor.py`
5. 扩 `context_accumulation.py` 和 `turn_transition.py`
6. 扩 `prediction_workspace.py`
7. 扩 `tests/slices/test_language_organs.py`
8. 扩 `tests/slices/test_language_relationship.py`
9. 若恢复链受影响，再补 `tests/bridges/test_first_terminal_turn.py` / `tests/bridges/test_terminal_life_loop.py`

## 第一轮完成定义

只有同时满足下面六条，Queue A 才算完成第一轮：

1. 外部一条语言输入先进入 `LanguagePerceptFrame`，而不是直接进入 `inner_speech.py`。
2. `SemanticMapFrame` 能把 shared terms、关系主题、承诺/修复线索和叙事绑定成同一张图。
3. `inner_speech.py`、`expression_monitor.py`、`prediction_workspace.py` 至少各接住一部分 percept / semantic 输出。
4. `context_accumulation_window.json` 和 `turn_transition_trace.json` 都保存了 percept / semantic refs。
5. `language_relationship_report.json` 与 `life_state.json` 都能回链这两个新器官。
6. 对应测试直接证明以上闭环，不靠人工阅读 state 猜测是否接通。

## 这份合同和下一轮落码的关系

从本文件开始，Queue A 不再只是“文件名待写”。

下一轮如果继续推进语言主神经束，默认读包就是：

```text
docs/v0/code_framework/04_language_dialogue_relationship_implementation_playbook.md
  -> docs/v0/code_framework/09_perception_prediction_world_contact_implementation_playbook.md
  -> docs/v0/code_framework/11_engineering_delivery_waves_and_real_file_queue.md
  -> docs/v0/code_framework/12_full_life_layer_delivery_matrix.md
  -> docs/v0/code_framework/13_capability_to_code_realization_matrix.md
  -> docs/v0/code_framework/14_queue_a_language_percept_semantic_map_implementation_contract.md
```

然后直接进入：

```text
life_v0/language/percept.py
  -> life_v0/language/semantic_map.py
```
