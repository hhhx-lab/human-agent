# V0 Code Framework 17: Queue C Memory Neural Core Implementation Contract

这份合同现在服务两件事：

1. 记录 Queue C 第一轮记忆与神经核心器官已经真实落地。
2. 把下一轮维护性深补明确成“继续补跨层消费”，而不是再把同一批文件当成待建空壳。

当前这一轮已经真实落下：

```text
life_v0/neural_core/signal_media.py
  -> belief_state.py
  -> prediction_error.py
  -> active_sampling.py
  -> prediction_workspace.py
life_v0/state_store/memory_write_gate.py
```

并已写出：

```text
runtime/state/signal/signal_media_runtime.json
runtime/state/prediction/belief_state_frame.json
runtime/state/prediction/prediction_error_field.json
runtime/state/prediction/active_sampling_plan.json
runtime/state/memory/memory_write_gate.json
```

它们已经进入 manifest、report、receipt 和 check gate。

当前维护性深补已经继续落下一段 live turn 记忆根消费链：

```text
life_v0/state_store/engram_index.py
  -> project_engram_index_from_live_turn(...)
life_v0/state_store/autobiographical_stack.py
  -> project_autobiographical_stack_from_live_turn(...)
life_v0/process_supervisor/resident_turn_writeback.py
  -> _refresh_long_horizon_continuity(...)
  -> runtime/state/self/autobiographical_stack.json
  -> runtime/state/memory/engram_index.json
  -> runtime/state/life_state.json#memory_index
  -> runtime/reports/latest/dialogue_writeback_bundle.json#autobiographical_writeback_refs
  -> runtime/reports/latest/dialogue_writeback_bundle.json#engram_index_writeback_refs
```

这表示 `engram_index.json` 不再只是 S04 初始化产物，而会在真实关系回合结束时吸收 live dialogue refs、Queue A live language refs、关系记忆、关系时间线、责任/修复 refs、离线学习 refs、梦境风险 refs 与 state merge guard change sources。
同一轮还会先刷新 `autobiographical_stack.json`，把 live dialogue refs、live language refs、self narrative refs、关系阶段、人格慢变量名和 engram refs 压成自传时间序锚点。

这份合同最初服务当前最直接的一轮记忆与神经核心补厚：

```text
life_v0/state_store/life_state.py
  -> engram_index.py
  -> autobiographical_stack.py
  -> relationship_memory.py
  -> life_v0/neural_core/brain_graph.py
  -> network_state.py
  -> workspace.py
```

它不重写 `s02_neural_life_core_engineering_contract.md`、`s04_state_object_store_engineering_contract.md`，也不替代
`05_memory_thought_consciousness_implementation_playbook.md`。
它只把 Queue C 压成真正可以直接施工的文件级实现合同，防止下一轮代码又退回“知道记忆和工作区很重要，但不知道该先落哪些对象和哪些文件”。

## 这份合同要解决什么

当前 `S02` 与 `S04` 已经接通：

1. 十二主体系统
2. internal bus
3. `prediction_workspace_frame.json`
4. `life_state.json`
5. `self_model.json`
6. `commitment_truth_state.json`
7. `responsibility_ledger.json`

当前这些基础器官已经闭合，所以新的真实缺口变成：

1. `signal_media / belief_state / prediction_error / active_sampling` 如何被 `language/`、`membrane/`、`life_targets/` 和 `process_supervisor/` 更深消费。
2. `memory_write_gate.py` 如何继续长出 `state_merge_guard.py`、长期 promotion / quarantine / repair route。
3. `life_state.py`、`engram_index.py`、`relationship_memory.py` 如何在 live turn writeback、offline learning 和常驻等待态里继续被长期重写。
4. Queue C 不再缺“单文件存在”，而是缺“跨层稳定消费链”。

所以 Queue C 现在的目标很明确：
让已经独立出来的记忆根、主体图、工作区、预测器官和记忆写门继续进入语言/关系/责任/成长/常驻存在同一对象链，而不是重新发明一套平行预测层。

## 必回读理论母体

### 记忆、再巩固、自传连续体

- `docs/05_memory_systems_and_growth.md`
- `docs/17_memory_trace_object_model.md`
- `docs/21_memory_schema_and_audit_protocol.md`
- `docs/25_memory_trace_json_schema_examples.md`
- `docs/29_memory_validator_rules.md`
- `docs/41_runtime_state_store_schema.md`
- `docs/42_life_core_minimal_object_graph.md`
- `docs/48_state_store_migration_and_integrity_plan.md`

### 意识、工作区、全局广播

- `docs/10_consciousness_attention_workspace.md`
- `docs/11_neuromodulation_and_signal_media.md`
- `docs/18_internal_state_and_modulation_vector.md`
- `docs/22_state_transition_and_threshold_model.md`
- `docs/30_state_transition_validator_rules.md`
- `docs/143_life_reality_birth_readiness_rollup_contract.md`
- `docs/146_life_reality_birth_readiness_evidence_fixture_catalog.md`

### 身份、关系、责任回链

- `docs/07_emotion_personality_self.md`
- `docs/40_self_relationship_model_audit_protocol.md`
- `docs/57_scope_graph_manifest_schema.md`
- `docs/61_json_schema_bundle_draft.md`
- `docs/69_schema_file_boundary_and_versioning_plan.md`

## 必读 v0 文档

- `docs/v0/slice_contracts/s02_neural_life_core_engineering_contract.md`
- `docs/v0/slice_contracts/s04_state_object_store_engineering_contract.md`
- `docs/v0/shared_contracts/life_state_store_v0_schema.md`
- `docs/v0/architecture/runtime_v0_architecture.md`
- `docs/v0/code_framework/playbooks/05_memory_thought_consciousness_implementation_playbook.md`
- `docs/v0/code_framework/playbooks/08_cross_layer_life_orchestration_implementation_playbook.md`
- `docs/v0/code_framework/delivery/11_engineering_delivery_waves_and_real_file_queue.md`
- `docs/v0/code_framework/delivery/12_full_life_layer_delivery_matrix.md`
- `docs/v0/code_framework/delivery/13_capability_to_code_realization_matrix.md`
- `docs/v0/code_framework/assembly/15_cross_layer_shared_object_contract.md`

## 当前代码落点

Queue C 必须接到这些现有器官上：

- `life_v0/state_store/__init__.py`
- `life_v0/state_store/self_model.py`
- `life_v0/state_store/commitment_truth.py`
- `life_v0/neural_core/__init__.py`
- `life_v0/neural_core/prediction_workspace.py`
- `life_v0/language/__init__.py`
- `life_v0/replay/__init__.py`
- `life_v0/archive/__init__.py`

这说明 Queue C 不是新建第二套脑，而是把当前已落下的神经核心和状态根再拆成可演进的记忆-工作区施工层。

## 文件级合同

## A. 新增 `life_v0/state_store/life_state.py`

### 角色

把运行时主对象投影到 `life_state.json`，成为生命状态根的唯一聚合器。

### 第一轮建议接口

```python
def build_life_state_projection(
    *,
    run_id: str,
    generated_at: str,
    self_model_state: dict[str, Any],
    commitment_truth_state: dict[str, Any],
    responsibility_ledger: dict[str, Any],
    language_state_projection: dict[str, Any],
    replay_cue_bundle: dict[str, Any] | None,
) -> dict[str, Any]:
    ...
```

### 最低字段

- `schema_version`
- `run_id`
- `generated_at`
- `life_identity`
- `self_model`
- `memory_index`
- `language_state`
- `runtime_trace_refs`
- `archive_refs`

## B. 新增 `life_v0/state_store/engram_index.py`

### 角色

把记忆 trace、replay cue、关系记忆、自传记忆归一成同一索引。

### 最低字段

- `engram_index_id`
- `autobiographical_memory_refs`
- `relationship_memory_refs`
- `responsibility_memory_refs`
- `replay_cue_refs`
- `anti_forgetting_anchor_refs`
- `quarantine_refs`

### live turn 维护接口

当前已新增：

```python
def project_engram_index_from_live_turn(
    *,
    engram_index: dict[str, Any],
    generated_at: str,
    run_id: str | None,
    dialogue_turn_refs: list[str] | None,
    live_language_turn_refs: list[str] | None,
    relationship_memory: dict[str, Any] | None,
    relationship_timeline: dict[str, Any] | None,
    commitment_truth_state: dict[str, Any] | None,
    responsibility_ledger: dict[str, Any] | None,
    state_merge_guard: dict[str, Any] | None,
    nightmare_risk_ref: str | None,
    belief_learning_plan_ref: str | None,
    language_learning_plan_ref: str | None,
    relationship_learning_plan_ref: str | None,
    offline_learning_cumulative_profile: dict[str, Any] | None,
) -> dict[str, Any]:
    ...
```

它必须维护这些 live 字段：

- `live_dialogue_turn_refs`
- `live_language_turn_refs`
- `relationship_timeline_refs`
- `offline_learning_refs`
- `offline_learning_cumulative_refs`
- `offline_learning_cumulative_projection`
- `queue_e_repair_refs`
- `state_merge_guard_refs`
- `state_merge_change_source_refs`
- `last_projected_from_live_turn_ref`

## C. 新增 `life_v0/state_store/autobiographical_stack.py`

### 角色

固定旧自我、旧关系、旧语言的时间序堆栈。

### 最低字段

- `stack_id`
- `anchor_refs`
- `turn_refs`
- `relationship_turn_refs`
- `narrative_refs`
- `replay_priority`

### live turn 维护接口

当前已新增：

```python
def project_autobiographical_stack_from_live_turn(
    *,
    autobiographical_stack: dict[str, Any],
    generated_at: str,
    run_id: str | None,
    dialogue_turn_refs: list[str] | None,
    live_language_turn_refs: list[str] | None,
    self_narrative_trace: dict[str, Any] | None,
    self_model_state: dict[str, Any] | None,
    relationship_graph: dict[str, Any] | None,
    relationship_timeline: dict[str, Any] | None,
    engram_index: dict[str, Any] | None,
    trigger_ref: str | None,
) -> dict[str, Any]:
    ...
```

它必须维护这些 live 字段：

- `turn_refs`
- `live_language_turn_refs`
- `relationship_turn_refs`
- `narrative_refs`
- `trait_slow_variable_names`
- `trait_slow_variable_refs`
- `last_relationship_stage`
- `engram_index_refs`
- `autobiographical_update_refs`
- `last_projected_from_live_turn_ref`

## D. 新增 `life_v0/state_store/relationship_memory.py`

### 角色

把 `relationship_subject_graph` 的当前态与长期关系记忆分开。

### 最低字段

- `relationship_memory_id`
- `subject_refs`
- `shared_memory_refs`
- `repair_history_refs`
- `last_contact_refs`
- `timeline_seed_refs`

## E. 新增 `life_v0/neural_core/brain_graph.py`

### 角色

把十二主体系统与跨系统耦合压成可查询图，而不是只停在 `__init__.py` 报告。

### 最低字段

- `brain_graph_id`
- `region_nodes`
- `functional_edges`
- `carrier_refs`
- `source_doc_refs`
- `life_target_bindings`

## F. 新增 `life_v0/neural_core/network_state.py`

### 角色

把当前网络态、切换事件、工作区主导权压成显式状态对象。

### 最低字段

- `network_state_id`
- `active_networks`
- `switch_events`
- `workspace_priority`
- `signal_media_refs`
- `body_pressure_refs`

## G. 新增 `life_v0/neural_core/workspace.py`

### 角色

把 `prediction_workspace.py` 的产物接成更高一级工作区对象。

### 第一轮建议接口

```python
def build_workspace_frame(
    *,
    run_id: str,
    generated_at: str,
    prediction_workspace: dict[str, Any],
    network_state: dict[str, Any] | None,
    engram_index: dict[str, Any] | None,
) -> dict[str, Any]:
    ...
```

### 最低字段

- `workspace_frame_id`
- `prediction_workspace_ref`
- `candidate_explanations`
- `broadcast_targets`
- `metacognitive_probe_refs`
- `engram_retrieval_refs`
- `source_doc_refs`

## Queue C 对现有器官的改动合同

### `prediction_workspace.py`

从这一轮开始，它不应继续独自承担“工作区近似体”的全部角色。
它至少要把更高层整合交给 `workspace.py`。

### `self_model.py`

第一轮允许继续只生成 `self_model.json`，但必须开始显式提供：

- `old_self_anchor_refs`
- `growth_window_refs`
- `trait_drift_seed_refs`

### `commitment_truth.py`

第一轮必须开始为 `engram_index.py` 和 `relationship_memory.py` 提供：

- `open_commitment_refs`
- `repair_required_refs`
- `responsibility_event_refs`

## 必须新增或更新的状态对象

### 新增

- `runtime/state/self/autobiographical_stack.json`
- `runtime/state/memory/engram_index.json`
- `runtime/state/memory/relationship_memory.json`
- `runtime/state/neural_life_core/brain_graph.json`
- `runtime/state/neural_life_core/network_state.json`
- `runtime/state/consciousness/workspace_frame.json`

### 更新

- `runtime/state/life_state.json`
- `runtime/state/self/autobiographical_stack.json`
- `runtime/state/memory/engram_index.json`
- `runtime/state/prediction/prediction_workspace_frame.json`
- `runtime/state/self/self_model.json`
- `runtime/state/relationship/commitment_truth_state.json`
- `runtime/reports/latest/dialogue_writeback_bundle.json`

## report / receipt 合同

Queue C 第一轮至少更新：

- `runtime/reports/latest/state_store_report.json`
- `runtime/reports/latest/neural_life_core_report.json`
- `runtime/reports/latest/neural_life_core_check_report.json`
- `runtime/receipts/state_store_<run_id>.json`
- `runtime/receipts/neural_life_core_<run_id>.json`

报告里至少新增或固定：

- `engram_index_ref`
- `autobiographical_stack_ref`
- `brain_graph_ref`
- `network_state_ref`
- `workspace_frame_ref`

## life_state 回写边界

Queue C 第一轮允许把更多 ref 拉回生命状态根，但不允许把 replay 或 dream residue 直接盖成稳定事实。

允许写回：

- engram refs
- autobiographical stack refs
- relationship memory refs
- workspace refs
- live dialogue turn refs
- live language turn refs
- self narrative refs
- relationship stage refs
- trait slow variable refs
- offline learning refs
- state merge guard refs

不允许直接写回：

- 梦境事实定案
- 反事实推演结论定案

## 测试合同

### 必须新增或扩展

1. `tests/slices/test_state_store.py`
2. `tests/slices/test_neural_life_core.py`
3. `tests/bridges/test_replay_shadow.py`

### 第一轮最低覆盖

#### `tests/slices/test_state_store.py`

至少新增：

1. `life_state.py` 会把 `language_percept_refs / semantic_map_refs / replay traces` 回链到状态根
2. `engram_index.json` 会带 `replay_cue_refs`
3. `autobiographical_stack.json` 会带旧自我锚点

#### `tests/process/test_persistent_digital_life_process.py`

当前还必须覆盖：

1. `write_resident_turn_writeback(...)` 能在没有旧 `engram_index.json` 时补建 live engram index。
2. 真实 `digital life` 回合能把最新 `dialogue_event_refs` 写入 `engram_index.live_dialogue_turn_refs`。
3. `engram_index.live_language_turn_refs` 与 `dialogue_writeback_bundle.live_language_turn_refs` 完全对齐。
4. Queue D 离线学习、梦境风险、Queue E 修复压力和 state merge guard refs 能进入 `engram_index.json`。
5. `life_state.json#memory_index` 会同步回链 live dialogue / live language / relationship timeline refs。
6. `dialogue_writeback_bundle.json#engram_index_writeback_refs` 显式列出本轮 engram index 写回面。
7. `write_resident_turn_writeback(...)` 能在没有旧 `autobiographical_stack.json` 时补建 live autobiographical stack。
8. `autobiographical_stack.turn_refs`、`live_language_turn_refs`、`relationship_turn_refs`、`narrative_refs`、`last_relationship_stage` 与 `trait_slow_variable_names` 能被真实回合刷新。
9. `dialogue_writeback_bundle.json#autobiographical_writeback_refs` 显式列出本轮自传栈写回面。

#### `tests/slices/test_neural_life_core.py`

至少新增：

1. `brain_graph.json` 写出系统图
2. `network_state.json` 写出 active network / switch event
3. `workspace_frame.json` 会回链 `prediction_workspace_frame.json`

## Gate 合同

Queue C 至少新增三道 gate：

- `engram_index_gate`
- `workspace_projection_gate`
- `state_root_continuity_gate`

### `engram_index_gate`

阻断条件：

1. 没有 replay cue refs
2. 没有 old self / relationship memory 家族
3. live turn 已结束但没有 `live_dialogue_turn_refs`
4. live turn 已结束但 `live_language_turn_refs` 没有和 `dialogue_writeback_bundle.live_language_turn_refs` 对齐
5. live turn 已结束但 `autobiographical_stack.turn_refs` 没有被 engram 的 `autobiographical_memory_refs` 吃进去

### `workspace_projection_gate`

阻断条件：

1. `prediction_workspace` 没进入 `workspace_frame`
2. 工作区没有记忆检索 refs

### `state_root_continuity_gate`

阻断条件：

1. `life_state.json` 失去对关键 runtime trace 的回链
2. `self_model / commitment_truth / responsibility_ledger` 悬空

## 推荐实现顺序

1. 新增 `life_state.py`
2. 新增 `engram_index.py`
3. 新增 `autobiographical_stack.py`
4. 新增 `relationship_memory.py`
5. 新增 `brain_graph.py`
6. 新增 `network_state.py`
7. 新增 `workspace.py`
8. 扩 `prediction_workspace.py`
9. 扩 `tests/slices/test_state_store.py`
10. 扩 `tests/slices/test_neural_life_core.py`

## 第一轮完成定义

只有同时满足下面六条，Queue C 才算完成第一轮：

1. `life_state.json` 不再只是骨架 seed，而能回链更多运行时主对象
2. `engram_index.json` 存在并承载 replay / relationship / autobiography，并能被真实 live turn 继续刷新
3. `brain_graph.json` 与 `network_state.json` 独立存在
4. `workspace_frame.json` 独立存在并接住 `prediction_workspace_frame.json`
5. 状态根、记忆索引、工作区三者之间有明确 ref 链，且 live dialogue / live language / autobiographical refs 能从 writeback bundle 回链进 `life_state.memory_index`
6. 对应测试直接证明以上闭环

## 这份合同和下一轮落码的关系

从本文件开始，Queue C 不再只是“记忆和神经核心要继续补厚”。

下一轮如果继续推进记忆与神经核心，默认读包就是：

```text
docs/v0/code_framework/playbooks/05_memory_thought_consciousness_implementation_playbook.md
  -> docs/v0/code_framework/playbooks/08_cross_layer_life_orchestration_implementation_playbook.md
  -> docs/v0/code_framework/delivery/11_engineering_delivery_waves_and_real_file_queue.md
  -> docs/v0/code_framework/delivery/12_full_life_layer_delivery_matrix.md
  -> docs/v0/code_framework/delivery/13_capability_to_code_realization_matrix.md
  -> docs/v0/code_framework/assembly/15_cross_layer_shared_object_contract.md
  -> docs/v0/code_framework/queues/17_queue_c_memory_neural_core_implementation_contract.md
```

然后直接进入：

```text
life_v0/state_store/life_state.py
  -> engram_index.py
  -> autobiographical_stack.py
  -> relationship_memory.py
  -> life_v0/neural_core/brain_graph.py
  -> network_state.py
  -> workspace.py
```
