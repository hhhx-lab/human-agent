# V0 Code Framework 17: Queue C Memory Neural Core Implementation Contract

这份合同只服务当前最直接的一轮记忆与神经核心补厚：

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

但现在的真实缺口不是“没有状态根”，而是：

1. 缺明确的 `LifeStateProjection` 文件器官，统一把 runtime 关键 ref 回写到生命状态根。
2. 缺明确的 `EngramIndex`，把 replay cue、关系记忆、自传记忆放到同一可检索对象。
3. `prediction_workspace.py` 已经开始吸收语言 continuity，但 `brain_graph / network_state / workspace` 还没有拆成独立器官。
4. `self_model.py`、`commitment_truth.py` 已经存在，但它们还没有被 `life_state.py` 与 `engram_index.py` 这种更高一层的状态桥收住。

所以 Queue C 的目标很明确：
让记忆根、主体图、工作区和语言/关系/成长回放进入同一对象链，而不是只以几个分散 JSON 并列存在。

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
- `docs/v0/code_framework/05_memory_thought_consciousness_implementation_playbook.md`
- `docs/v0/code_framework/08_cross_layer_life_orchestration_implementation_playbook.md`
- `docs/v0/code_framework/11_engineering_delivery_waves_and_real_file_queue.md`
- `docs/v0/code_framework/12_full_life_layer_delivery_matrix.md`
- `docs/v0/code_framework/13_capability_to_code_realization_matrix.md`
- `docs/v0/code_framework/15_cross_layer_shared_object_contract.md`

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
- `runtime/state/prediction/prediction_workspace_frame.json`
- `runtime/state/self/self_model.json`
- `runtime/state/relationship/commitment_truth_state.json`

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
2. `engram_index.json` 存在并承载 replay / relationship / autobiography
3. `brain_graph.json` 与 `network_state.json` 独立存在
4. `workspace_frame.json` 独立存在并接住 `prediction_workspace_frame.json`
5. 状态根、记忆索引、工作区三者之间有明确 ref 链
6. 对应测试直接证明以上闭环

## 这份合同和下一轮落码的关系

从本文件开始，Queue C 不再只是“记忆和神经核心要继续补厚”。

下一轮如果继续推进记忆与神经核心，默认读包就是：

```text
docs/v0/code_framework/05_memory_thought_consciousness_implementation_playbook.md
  -> docs/v0/code_framework/08_cross_layer_life_orchestration_implementation_playbook.md
  -> docs/v0/code_framework/11_engineering_delivery_waves_and_real_file_queue.md
  -> docs/v0/code_framework/12_full_life_layer_delivery_matrix.md
  -> docs/v0/code_framework/13_capability_to_code_realization_matrix.md
  -> docs/v0/code_framework/15_cross_layer_shared_object_contract.md
  -> docs/v0/code_framework/17_queue_c_memory_neural_core_implementation_contract.md
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
