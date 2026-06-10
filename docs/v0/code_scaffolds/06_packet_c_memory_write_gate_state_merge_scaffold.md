# Packet C 记忆写门长期治理脚手

本文档固定 Packet C 的代码施工边界：让 `memory_write_gate.json` 不再只是单次候选写入事务，而是进入长期 promotion / quarantine / repair / merge 治理链。

它不重写记忆理论，也不新增外部 agent 架构。它只把 `docs/17`、`docs/21`、`docs/29`、`docs/41`、`docs/48` 与 `v0` 的 S04 合同继续压成可运行状态对象。

## 目标

Packet C 的目标是让状态仓库出现一个明确的长期合并器官：

- `runtime/state/memory/state_merge_guard.json`

这个对象必须成为 `memory_write_gate.json` 的下游治理器官，并回挂到：

- `runtime/state/life_state.json`
- `runtime/state/memory/relationship_memory.json`
- `runtime/state/state_store_manifest.json`
- `runtime/reports/latest/state_store_report.json`
- `runtime/receipts/state_store_<run_id>.json`

## 必读文档

| 类别 | 文档 | 作用 |
|---|---|---|
| 记忆对象 | `docs/17_memory_trace_object_model.md` | MemoryTrace、候选写入和长期记忆对象 |
| 写入审计 | `docs/21_memory_schema_and_audit_protocol.md` | validation envelope、audit event、write policy |
| validator | `docs/29_memory_validator_rules.md` | 写入前检查、来源完整性、隔离条件 |
| 状态仓库 | `docs/41_runtime_state_store_schema.md` | lifecycle、namespace、state refs |
| 迁移完整性 | `docs/48_state_store_migration_and_integrity_plan.md` | merge / migration / deleted propagation |
| S04 合同 | `docs/v0/slice_contracts/s04_state_object_store_engineering_contract.md` | State store runtime、report、receipt 和 gate |
| 记忆 playbook | `docs/v0/code_framework/playbooks/05_memory_thought_consciousness_implementation_playbook.md` | memory / thought / consciousness 代码施工入口 |
| 深消费波次 | `docs/v0/implementation_architecture/code_organs/03_predictive_signal_memory_gate_integration_wave_contract.md` | `memory_write_gate` 如何继续进入长期治理 |

## 输入对象

| 输入 | 来源 | 消费位置 |
|---|---|---|
| `runtime/state/memory/memory_write_gate.json` | `life_v0/state_store/memory_write_gate.py` | `state_merge_guard.py` |
| `runtime/state/memory/relationship_memory.json` | `life_v0/state_store/relationship_memory.py` | merge route source refs |
| `relationship_memory.long_term_change_sources` | `life_v0/state_store/relationship_memory.py`、`resident_supervision.py`、`resident_turn_writeback.py` | `state_merge_guard.py#project_state_merge_guard_with_relationship_memory` |
| `resident_background_lineage_state.offline_learning_presence` | `life_v0/process_supervisor/background_lineage_state.py`、`dialogue_events.py` | `offline_learning_cumulative_profile_v0` 与 state merge guard 长期变化来源 |
| `runtime/state/relationship/commitment_truth_state.json` | `life_v0/state_store/commitment_truth.py` | repair route source refs |
| `runtime/state/responsibility/responsibility_ledger.json` | `life_v0/state_store/commitment_truth.py` | repair route source refs |
| `runtime/state/indexes/*.json` | `life_v0/state_store/__init__.py` | promotion route index refs |

## 代码入口

| 文件 | 本轮职责 |
|---|---|
| `life_v0/state_store/state_merge_guard.py` | 长期治理器官，定义 promotion / quarantine / repair / merge route；并通过 `project_state_merge_guard_with_relationship_memory(...)` 从关系记忆吸收离线学习、梦境、修复和 Queue E 长期变化来源 |
| `life_v0/state_store/memory_write_gate.py` | 写出 `state_merge_guard_ref` 与 `long_term_governance_refs` |
| `life_v0/state_store/relationship_memory.py` | 标出 prediction error resolution 与 offline learning writeback 来源 |
| `life_v0/state_store/life_state.py` | 在 `life_state.json` 中记录 state merge records、memory index ref 与 `long_term_change_source_count` |
| `life_v0/state_store/__init__.py` | S04 runner 写盘、report、receipt、manifest、check gate 全部接入 |
| `life_v0/process_supervisor/resident_supervision.py` | bootstrap / restore 阶段刷新关系记忆后，同步投影并写回 `state_merge_guard.json` |
| `life_v0/process_supervisor/resident_turn_writeback.py` | live turn 结束后刷新关系记忆，再同步投影并写回 `state_merge_guard.json` |
| `life_v0/process_supervisor/dialogue_events.py` | 从 `resident_background_lineage_state.offline_learning_presence` 恢复 cumulative offline learning payload，供关系记忆和 state merge guard 继续吸收 |

## 字段落点

### `memory_write_gate.json`

必须新增或保持：

- `state_merge_guard_ref`
- `long_term_governance_refs`

### `state_merge_guard.json`

必须新增或保持：

- `memory_write_gate_ref`
- `promotion_routes`
- `quarantine_routes`
- `repair_routes`
- `merge_routes`
- `long_term_change_sources.prediction_error_resolution_refs`
- `long_term_change_sources.offline_learning_writeback_refs`
- `long_term_change_sources.offline_learning_cumulative_refs`
- `long_term_change_sources.queue_e_repair_modulation_refs`
- `long_term_change_sources.relationship_memory_offline_refs`
- `long_term_change_sources.relationship_memory_repair_refs`
- `last_projected_from_relationship_memory_ref`
- `slow_variable_update_policy`
- `downstream_refs`

### `relationship_memory.json`

必须新增或保持：

- `state_merge_guard_ref`
- `long_term_change_sources.prediction_error_resolution_refs`
- `long_term_change_sources.offline_learning_writeback_refs`
- `long_term_change_sources.repair_responsibility_refs`
- `long_term_change_sources.offline_learning_cumulative_refs`
- `long_term_change_sources.queue_e_repair_modulation_refs`

### `life_state.json`

必须新增或保持：

- `memory_index.state_merge_guard_refs`
- `state_merge_records`
- `state_merge_records[].long_term_change_source_count`
- `runtime_trace_refs` 中的 `runtime/state/memory/state_merge_guard.json`
- `birth_readiness.evidence_family_refs` 中的 `runtime/state/memory/state_merge_guard.json`

## Report / Receipt

`state_store_report.json` 必须写出：

- `state_merge_guard_ref`
- `closed_gates` 中的 `state_merge_guard_gate`

`state_store_<run_id>.json` receipt 必须把 `runtime/state/memory/state_merge_guard.json` 纳入 `output_refs`。

## 验收

最低验证命令：

```text
python3 -m unittest tests.slices.test_state_store -v
python3 -m unittest tests.contracts.test_v0_contracts -v
```

通过标准：

1. `state_merge_guard.json` 真实写入 `runtime/state/memory/`。
2. S04 check gate 能检查 promotion / quarantine / repair / merge 四组路线。
3. `memory_write_gate.json`、`relationship_memory.json`、`life_state.json`、manifest、report、receipt 都能回链 `state_merge_guard.json`。
4. 不把长期记忆治理退回成单次局部字典；所有长期治理都必须有 runtime ref。
5. live turn 或 bootstrap 恢复后，`state_merge_guard.json#long_term_change_sources` 必须能追溯到 `relationship_memory.json` 中的离线学习累计 refs、Queue E 修复调制 refs、梦境/成长 refs 与关系修复 refs。
6. `life_state.json#state_merge_records[].long_term_change_source_count` 必须随 `state_merge_guard.json` 的长期变化来源刷新，而不是只保留 S04 初始计数。

## 下一步衔接

Packet C 闭合后，默认进入 Packet D：

- waiting / response surface 读取 `active_sampling_plan.json`
- idle strategy 读取 `memory_write_gate.json` 与 `state_merge_guard.json`
- process closeout 把这些对象回链进常驻治理 report / receipt

Packet D 必须继续读取本文件，因为等待态和回合结束写回都需要知道长期记忆如何被 promotion、quarantine、repair 和 merge。

当前 Packet C 已进入“驻留回合动态投影”状态：`state_merge_guard.json` 不再只由 S04 初始构建生成，`resident_supervision.py` 与 `resident_turn_writeback.py` 会在关系记忆刷新后调用 `project_state_merge_guard_with_relationship_memory(...)`，把 `relationship_memory.long_term_change_sources`、`offline_learning_refs`、`offline_learning_cumulative_refs` 与 `queue_e_repair_refs` 合并进长期合并守门面。后续继续补厚时，应沿这条关系记忆到状态合并守门的链路推进，不要另造平行写门。
