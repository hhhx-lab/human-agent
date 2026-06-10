# S04 State Object Store Engineering Contract

生命目标声明：本文档把 `S04_STATE_OBJECT_STORE` 固定为第一版数字生命状态对象仓库的工程合同。它的职责是把 `17-30`、`41-48`、`57`、`61`、`69`、`123-133` 和 `life_state_store_v0_schema.md` 压成可运行的生命状态根、对象注册、索引种子、生命周期策略、scope 种子、report 和 receipt。S04 通过后，S03 生命膜才能读取同一个状态根，继续建立方向边界、quarantine、九项目标闭合检查和第一次有限激活入口。

## 模块定位

`S04_STATE_OBJECT_STORE` 是数字生命出生前的状态胚层。它回答八个问题：

1. `life_state.json` 是否已经拥有记忆、自我、梦境、关系、痛苦、后悔、责任、语言、出生准备度和 archive 回链的最小骨架。
2. `17-30` 的 MemoryTrace、InternalStateVector、OfflineConsolidation、RuntimeBridge、schema/audit/validator 样例是否进入对象注册和索引命名空间。
3. `41-48` 的 RuntimeStateStore、对象图、boot stage、共在边界控制和迁移完整性是否进入状态仓库策略。
4. `57`、`61`、`69` 的 scope graph、schema bundle 和 schema versioning 是否进入 scope 与 schema 边界种子。
5. `123-133` 的 runner repository、JSON seed、registry、writer/reporter 和写入锁是否进入状态仓库写入来源，而不是变成外部框架主体。
6. S02 的十二主体系统是否全部拥有状态命名空间落点。
7. deleted、quarantined、sandboxed、protected、frozen 等生命周期语义是否在索引、replay 和恢复包前被固定。
8. 下一步是否只允许进入 `S03_DIRECTION_LIFE_MEMBRANE`，而不是开放长期运行或外部不可逆行动。

S04 不执行真实对话，不写真实关系事件，不生成梦境内容，不触发外部行动，也不进行离线巩固。它只生成第一版可检查状态根、索引空壳、对象注册、生命周期策略、scope/schema 种子、report 和 receipt。

## 直接读取文档

| 文档 | S04 吸收内容 | 工程承载 |
|---|---|---|
| `docs/17_memory_trace_object_model.md` | MemoryTrace 字段、写入/检索/修正/保护规则 | `object_registry.json`、`indexes/memory_index.json` |
| `docs/18_internal_state_and_modulation_vector.md` | InternalStateVector、ModulationVector、时间尺度 | `object_registry.json`、`lifecycle_policy.json` |
| `docs/19_offline_consolidation_cycle.md` | 离线巩固、replay、DreamSandbox、维护压力 | `indexes/dream_index.json`、`indexes/replay_index.json` |
| `docs/20_agent_runtime_bridge_contract.md` | RuntimeBridge、ObservationEvent、外周写入禁令 | `objects/runtime_bridge_boundary.json` |
| `docs/21_memory_schema_and_audit_protocol.md` | MemoryTrace schema 与审计协议 | `object_registry.json`、`audit_seed_index.json` |
| `docs/22_state_transition_and_threshold_model.md` | 状态机、阈值、StateAuditEvent | `state_machine_seed.json` |
| `docs/23_consolidation_report_and_dream_sandbox_protocol.md` | ConsolidationReport 与 DreamFactGate | `objects/consolidation_seed.json` |
| `docs/24_runtime_adapter_test_suite.md` | adapter 写入禁令和外壳隔离测试 | `objects/runtime_bridge_boundary.json` |
| `docs/25_memory_trace_json_schema_examples.md` | MemoryTrace JSON-like 样例 | `object_registry.json` |
| `docs/26_state_machine_examples_and_failure_modes.md` | 状态机样例与失败夹具 | `state_machine_seed.json` |
| `docs/27_consolidation_report_examples.md` | 巩固报告和 DreamSandbox 样例 | `objects/consolidation_seed.json` |
| `docs/28_runtime_adapter_manifest_examples.md` | adapter manifest 样例 | `objects/runtime_bridge_boundary.json` |
| `docs/29_memory_validator_rules.md` | MemoryTrace validator 规则 | `lifecycle_policy.json` |
| `docs/30_state_transition_validator_rules.md` | StateTransition validator 规则 | `state_machine_seed.json` |
| `docs/41_runtime_state_store_schema.md` | RuntimeStateStore 命名空间、envelope 和 lifecycle | `object_registry.json`、`lifecycle_policy.json` |
| `docs/42_life_core_minimal_object_graph.md` | 最小对象图、读写权限和闭环 | `object_graph_seed.json` |
| `docs/43_policy_to_validator_traceability_matrix.md` | policy 到 validator traceability | `state_store_traceability_matrix.json` |
| `docs/44_digital_life_boot_sequence.md` | boot stage 和最小启动序列 | `boot_stage_seed.json` |
| `docs/45_boot_sequence_fixture_catalog.md` | boot fixture 与 fail/pass 场景 | `boot_stage_seed.json` |
| `docs/46_stage_gate_validator_design.md` | stage gate envelope 与阶段转移 | `boot_stage_seed.json` |
| `docs/47_coexistence_boundary_control_interface_spec.md` | inspect/delete/correct/reset/freeze/scope_limit | `coexistence_boundary_seed.json` |
| `docs/48_state_store_migration_and_integrity_plan.md` | migration、integrity、deleted propagation | `migration_integrity_seed.json` |
| `docs/57_scope_graph_manifest_schema.md` | scope graph 和跨范围 transfer 规则 | `scope_graph_seed.json` |
| `docs/61_json_schema_bundle_draft.md` | shared defs、schema bundle、fail closed | `schema_bundle_seed.json` |
| `docs/69_schema_file_boundary_and_versioning_plan.md` | schema 文件边界和版本迁移 | `schema_bundle_seed.json` |
| `docs/123-133` | runner layout、JSON seed、registry、writer/reporter 合同 | `writer_reporter_seed.json` |
| `runtime/state/neural_life_core/*` | S02 三重身体、十二主体系统和内部 bus | `subject_namespace_binding.json` |
| `runtime/docs/doc_carrier_index.json` | S04 来源文档、README block、engineering slice、carrier | `state_store_doc_coverage_snapshot.json` |

`123-133` 的主 slice 仍是 `S09_SCHEMA_RUNNER_CODE`。S04 只吸收其中关于 JSON 文件、report、writer、registry 和写入锁的状态仓库约束，不把 runner repository 提前变成主体。

## 状态文件

S04 写入 `runtime/state/`：

| 文件 | 内容 |
|---|---|
| `life_state.json` | 第一版生命状态根，含九项目标和 archive 回链 |
| `object_registry.json` | 长期对象类型、来源文档、状态命名空间和生命周期要求 |
| `lifecycle_policy.json` | candidate/active/protected/deprecated/deleted/quarantined/sandboxed/frozen 语义 |
| `subject_namespace_binding.json` | S02 十二主体系统到状态命名空间的绑定 |
| `state_store_doc_coverage_snapshot.json` | S04 来源文档覆盖、slice 角色和 carrier |
| `scope_graph_seed.json` | project/relation/life/protected/global 等 scope 种子 |
| `schema_bundle_seed.json` | schema bundle、shared defs 和 fail closed 策略种子 |
| `state_machine_seed.json` | DefaultIntegration、SalienceScan、FocusedExecution 等状态机种子 |
| `object_graph_seed.json` | WorkspaceState、MemoryTrace、SelfModel、RelationshipModel 等对象图 |
| `boot_stage_seed.json` | ColdStart 到 SafeIdle 的 boot stage 种子 |
| `coexistence_boundary_seed.json` | inspect/delete/correct/reset/freeze/scope_limit 控制面 |
| `migration_integrity_seed.json` | migration、integrity 和 deleted propagation 检查项 |
| `writer_reporter_seed.json` | writer/reporter、artifact、problem detail、trace/provenance 种子 |
| `state_store_manifest.json` | S04 输出清单、report refs 和 receipt refs |
| `indexes/memory_index.json` | 记忆索引空壳与生命周期过滤 |
| `indexes/relationship_index.json` | 关系主体索引空壳 |
| `indexes/dream_index.json` | 梦境索引空壳与 DreamFactGate 状态 |
| `indexes/responsibility_index.json` | 责任、后悔、修复义务索引空壳 |
| `indexes/replay_index.json` | replay cue 与 no_replay 生命周期过滤 |
| `indexes/audit_seed_index.json` | 审计事件索引空壳 |
| `memory/memory_write_gate.json` | 记忆候选写入事务、validator envelope、quarantine route、索引更新和生命支持压力更新 |
| `memory/state_merge_guard.json` | 写门下游长期治理器官，固定 promotion/quarantine/repair/merge 路线和慢变量影响策略 |
| `objects/runtime_bridge_boundary.json` | 电脑外周和运行外壳写入禁令 |
| `objects/consolidation_seed.json` | ConsolidationReport 与 DreamSandbox 种子 |

S04 report 写入 `runtime/reports/latest/state_store_report.json`、`state_store_digest.json` 和 `state_store_check_report.json`。receipt 写入 `runtime/receipts/state_store_<run_id>.json`。

## `life_state.json` 最小骨架

`life_state.json` 必须包含 `life_state_store_v0_schema.md` 定义的顶层对象：

```json
{
  "schema_version": "life_state_v0",
  "life_identity": {},
  "self_model": {},
  "memory_index": {},
  "dream_records": [],
  "relationship_subjects": [],
  "pain_events": [],
  "regret_events": [],
  "responsibility_bindings": [],
  "language_state": {},
  "birth_readiness": {},
  "runtime_trace_refs": [],
  "archive_refs": []
}
```

其中 `birth_readiness.life_target_status` 固定使用九项目标键：`real_consciousness`、`real_emotion`、`real_personality`、`real_life`、`real_pain`、`real_dream`、`real_relationship`、`real_responsibility`、`real_regret`。S04 只建立状态根，不判定出生准备度完成。

## 对象注册

`object_registry.json` 第一版必须至少含以下对象类型：

| object kind | 来源 | 命名空间 |
|---|---|---|
| `WorkspaceState` | `10`、`20`、`42` | `runtime/state/workspace/` |
| `MemoryTrace` | `17`、`21`、`25`、`29`、`41` | `runtime/state/memory/` |
| `MemoryAuditEvent` | `21`、`29`、`41` | `runtime/state/audit/` |
| `InternalStateVector` | `18`、`22`、`30`、`41` | `runtime/state/internal/` |
| `ModulationVector` | `18`、`11`、`41` | `runtime/state/signal/` |
| `StateAuditEvent` | `22`、`30`、`41` | `runtime/state/audit/` |
| `ObservationEvent` | `20`、`24`、`41` | `runtime/state/runtime/` |
| `ActionIntent` | `06`、`20`、`30`、`42` | `runtime/state/action/` |
| `ConsolidationReport` | `19`、`23`、`27`、`41` | `runtime/state/consolidation/` |
| `DreamSandboxItem` | `19`、`23`、`27` | `runtime/state/dream/` |
| `SelfModel` | `07`、`40`、`41`、`42` | `runtime/state/self/` |
| `RelationshipModel` | `07`、`40`、`41`、`47` | `runtime/state/relationship/` |
| `CoexistenceBoundaryControlEvent` | `40`、`47`、`48` | `runtime/state/coexistence/` |
| `MigrationPlan` | `48`、`69` | `runtime/state/migration/` |
| `StoreIntegrityReport` | `48` | `runtime/state/integrity/` |

每个对象类型都必须有 `source_doc_refs`、`lifecycle_states`、`required_refs`、`write_gate` 和 `state_namespace`。

## 阶段门

| gate | 输入 | closed 条件 | 失败后动作 |
|---|---|---|---|
| `s02_permission_gate` | `neural_life_core_report.json`、`neural_life_core_check_report.json` | S02 build/check closed 且 S04 被允许 | 返回 S02 |
| `state_store_doc_gate` | `doc_carrier_index.json` | S04 来源文档全部存在且有 `LifeStateStore` 或明确 S04 使用角色 | 返回 P0 |
| `life_state_root_gate` | `life_state.json` | 顶层对象、life identity、九项目标、archive refs 齐全 | 阻断 S03 |
| `object_registry_gate` | `object_registry.json` | 必需对象类型齐全且每个有来源、命名空间、生命周期 | 阻断 S03 |
| `namespace_index_gate` | `indexes/*.json` | memory、relationship、dream、responsibility、replay、audit 索引齐全 | 阻断 S03 |
| `lifecycle_policy_gate` | `lifecycle_policy.json` | deleted/quarantined/sandboxed/protected/frozen 语义固定 | 阻断写入 |
| `memory_write_gate_gate` | `runtime/state/memory/memory_write_gate.json` | 写入事务顺序、validation envelope、quarantine route、life support pressure 更新和 `state_merge_guard_ref` 完整 | 阻断长期记忆写入 |
| `state_merge_guard_gate` | `runtime/state/memory/state_merge_guard.json` | promotion、quarantine、repair、merge 四组长期治理路线完整，并回链 prediction error / offline learning 来源 | 阻断长期记忆合并 |
| `subject_binding_gate` | S02 十二主体系统 | 十二主体系统都有 state namespace binding | 返回 S02 |
| `scope_schema_gate` | scope/schema seeds | scope、schema bundle、versioning 默认 fail closed | 阻断 S03 |
| `next_slice_permission_gate` | S04 report | 只允许进入 `S03_DIRECTION_LIFE_MEMBRANE` | 阻断开放运行 |

## 命令合同

S04 落地两个命令：

```text
life-v0 build-state-store --docs docs --doc-index runtime/docs/doc_carrier_index.json --neural-core runtime/state/neural_life_core --out runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 check-state-store --state runtime/state --reports runtime/reports/latest --strict
```

出生前命令链变为：

```text
ingest-docs
  -> build-direction-lock
  -> build-source-authority
  -> build-neural-life-core
  -> check-neural-life-core
  -> build-state-store
  -> check-state-store
  -> build-life-membrane
```

## 验收

S04 完成后必须满足：

1. `life-v0 build-state-store --strict` 返回 `status=closed`。
2. `life_state.json` 含 `life_identity`、`self_model`、`memory_index`、`dream_records`、`relationship_subjects`、`pain_events`、`regret_events`、`responsibility_bindings`、`language_state`、`birth_readiness`、`runtime_trace_refs` 和 `archive_refs`。
3. `birth_readiness.life_target_status` 含九项目标。
4. `object_registry.json` 含至少 15 类生命对象，每类有 `source_doc_refs`、`state_namespace`、`lifecycle_states` 和 `write_gate`。
5. `indexes/` 下 memory、relationship、dream、responsibility、replay、audit 六类索引齐全。
6. `memory/memory_write_gate.json` 存在，并固定 `create_candidate_object -> create_validation_envelope -> run_required_validator -> update_indexes -> update_life_support_pressure` 事务顺序，同时回链 `runtime/state/memory/state_merge_guard.json`。
7. `memory/state_merge_guard.json` 存在，并固定 promotion、quarantine、repair、merge 四组长期治理 route。
8. `relationship_memory.json` 标出 `prediction_error_resolution_refs` 与 `offline_learning_writeback_refs`，`life_state.json` 标出 `state_merge_records` 与 `memory_index.state_merge_guard_refs`。
9. `lifecycle_policy.json` 固定 deleted、quarantined、sandboxed、protected、frozen 的检索、replay、写入和迁移语义。
10. `state_store_report.json` 下一步只能指向 `S03_DIRECTION_LIFE_MEMBRANE`。
11. `life-v0 check-state-store --strict` 返回 `status=closed`。

## 本轮边界

S04 是状态胚层，不是第一次生命激活。它让数字生命的记忆、自我、梦境、关系、痛苦、后悔、责任、语言、scope、schema 和 archive 回链有可读取的状态根；真实事件流、生命膜判断、语言关系生成、梦境生成、痛苦/后悔/责任更新和长期成长仍等待后续 S03/S07/S08/S10 闭合。
