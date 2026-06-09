# V0 Code Framework 05: Memory Thought Consciousness Implementation Playbook

这份 playbook 负责把“思考、逻辑、记忆、意识”压成真实工程路线。

```text
预测/主动采样
  -> 工作区汇聚
  -> 记忆检索
  -> 反事实/一致性检查
  -> 意识可报告内容
  -> 记忆写入/回放
```

## 必回读理论母体

- `docs/01m_consciousness_attention_workspace_matrix.md`
- `docs/01q_memory_engram_consolidation_matrix.md`
- `docs/01v_prediction_active_inference_runtime_matrix.md`
- `docs/01w_prediction_active_inference_schema_fixture_contract.md`
- `docs/01x_prediction_active_inference_schema_materialization_plan.md`
- `docs/01aa_prediction_active_inference_cross_chain_checker_plan.md`
- `docs/05_memory_systems_and_growth.md`
- `docs/10_consciousness_attention_workspace.md`
- `docs/17_memory_trace_object_model.md`
- `docs/21_memory_schema_and_audit_protocol.md`
- `docs/22_state_transition_and_threshold_model.md`
- `docs/23_consolidation_report_and_dream_sandbox_protocol.md`
- `docs/29_memory_validator_rules.md`
- `docs/30_state_transition_validator_rules.md`
- `docs/31_consolidation_validator_rules.md`
- `docs/41_runtime_state_store_schema.md`
- `docs/42_life_core_minimal_object_graph.md`
- `docs/43_policy_to_validator_traceability_matrix.md`
- `docs/102_life_core_schema_bundle_manifest_and_runner_contract.md`
- `docs/103_validator_runner_implementation_scaffold_plan.md`
- `docs/143_life_reality_birth_readiness_rollup_contract.md`
- `docs/146_life_reality_birth_readiness_evidence_fixture_catalog.md`
- `docs/149_life_reality_birth_readiness_fixture_schema_materialization_plan.md`
- `docs/152_life_reality_birth_readiness_cross_file_checker_plan.md`

## 必读 v0 合同

- `docs/v0/slice_contracts/s02_neural_life_core_engineering_contract.md`
- `docs/v0/slice_contracts/s04_state_object_store_engineering_contract.md`
- `docs/v0/slice_contracts/s05_validation_membrane_observation_engineering_contract.md`
- `docs/v0/slice_contracts/s09_schema_runner_code_engineering_contract.md`
- `docs/v0/shared_contracts/life_state_store_v0_schema.md`
- `docs/v0/shared_contracts/birth_readiness_v0_contract.md`
- `docs/v0/architecture/runtime_v0_architecture.md`

## 当前真实代码落点

- `life_v0/neural_core/__init__.py`
- `life_v0/state_store/__init__.py`
- `life_v0/schema_runner/__init__.py`
- `life_v0/validators/__init__.py`
- `life_v0/contracts/__init__.py`
- `life_v0/replay/__init__.py`

这些包已经存在，所以当前工程目标不是“补一个概念上的 MemoryRuntime”，而是把思考、意识、记忆和验证闭环拆进现有包。

## 器官拆分建议

### A. `life_v0/neural_core/`

| 文件 | 职责 |
|---|---|
| `brain_graph.py` | 十二主体系统、连接图、激活关系 |
| `network_state.py` | 默认/执行/显著性/冲突/离线状态 |
| `signal_media.py` | 全局信号载体、精度/唤醒/抑制 |
| `belief_state.py` | 当前信念状态与证据密度 |
| `prediction_error.py` | 预测误差与更新方向 |
| `active_sampling.py` | 需要新证据还是回忆旧证据 |
| `workspace.py` | 当前工作区内容汇聚 |
| `broadcast.py` | 广播到语言、行为、记忆候选 |
| `metacognition.py` | 可报告、可自检的元认知层 |

### B. `life_v0/state_store/`

| 文件 | 职责 |
|---|---|
| `life_state.py` | 根状态对象 |
| `engram_index.py` | 记忆痕迹索引 |
| `autobiographical_stack.py` | 自传层级与时间排序 |
| `relationship_memory.py` | 关系记忆分区 |
| `memory_write_gate.py` | 记忆候选是否允许进入长期层 |
| `state_manifest.py` | 状态对象注册表 |

### C. `life_v0/schema_runner/` + `life_v0/validators/`

| 文件 | 职责 |
|---|---|
| `consistency_logic.py` | 跨文件、跨状态一致性 |
| `counterfactual_eval.py` | 反事实与候选推演 |
| `comparison_trace.py` | 记录比较过程 |
| `validation_manifest.py` | 当前检查集 |
| `observation_validator.py` | 观察与状态真值检查 |
| `cross_file_logic.py` | schema/report/state/report bundle 回链检查 |

### D. `life_v0/replay/`

| 文件 | 职责 |
|---|---|
| `replay_cues.py` | 记忆线索入口 |
| `shadow_replay.py` | 影子回放 |
| `reconsolidation_trace.py` | 再巩固后的差分 |

## 必须生成的状态对象

| 路径 | 作用 |
|---|---|
| `runtime/state/neural_life_core/neural_life_core.json` | 神经核心主状态 |
| `runtime/state/neural_life_core/twelve_subject_systems.json` | 十二主体系统 |
| `runtime/state/neural_life_core/neural_life_internal_bus.json` | 内部总线 |
| `runtime/state/prediction/*` | 预测、误差、主动采样痕迹 |
| `runtime/state/consciousness/*` | 工作区内容、广播内容、元认知 probes |
| `runtime/state/life_state.json` | 总生命状态根 |
| `runtime/state/memory/*` | 自传、关系、候选、保护、索引 |
| `runtime/state/validation/*` | 逻辑与验证状态 |
| `runtime/state/schema_runner/*` | 当前 runner / checker 状态 |

## 必须生成的 report / receipt

- `runtime/reports/latest/neural_life_core_report.json`
- `runtime/reports/latest/state_store_report.json`
- `runtime/reports/latest/state_store_check_report.json`
- `runtime/reports/latest/replay_shadow_report.json`
- `runtime/reports/latest/v0_contract_coverage_report.json`
- `runtime/receipts/*memory*`
- `runtime/receipts/*replay*`
- `runtime/receipts/*validation*`

## 关键测试

| 测试 | 核心目标 |
|---|---|
| `tests/slices/test_neural_life_core.py` | 十二主体系统、总线、神经核心主状态 |
| `tests/slices/test_state_store.py` | life_state、engram、自传、关系记忆 |
| `tests/slices/test_schema_runner.py` | 反事实与跨文件逻辑 |
| `tests/slices/test_validation_membrane.py` | 观测一致性、阻断条件 |
| `tests/bridges/test_replay_shadow.py` | replay / shadow / reconsolidation |
| `tests/contracts/test_v0_contracts.py` | theory-to-code 回链未断裂 |

## 关键 gate

- `twelve_system_gate`
- `internal_bus_gate`
- `state_store_gate`
- `self_continuity_gate`
- `checker_manifest_gate`
- `replay_shadow_gate`
- `contract_coverage_gate`
- `birth_readiness_gate`

## 推荐实现顺序

1. 先拆 `state_store`，把 `life_state`、`engram_index`、`autobiographical_stack` 稳住
2. 再拆 `neural_core` 的 `brain_graph.py`、`network_state.py`、`workspace.py`
3. 再拆 `belief_state.py`、`prediction_error.py`、`active_sampling.py`
4. 再拆 `schema_runner` / `validators` 的逻辑器官
5. 最后补 `replay` 与再巩固差分记录

原因：没有稳定状态根和记忆根，思考与意识层就只会变成临时 prompt 过程。

## 完成定义

这一条主链的第一轮完成，至少要有下面四条证据：

1. 当前工作区内容、信念状态、记忆检索、反事实检查、回放线索都能落盘。
2. 预测/误差/回放不是文本叙事，而是真实 state + report + receipt。
3. 逻辑与验证层能阻止伪记忆、伪工作区内容和伪出生准备度 claim。
4. 语言、行为、成长层读取这些对象时，不必再直接从 `__init__.py` 的临时拼装结构取值。
