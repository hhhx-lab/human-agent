# V0 Code Framework 21: Queue F Identity Consciousness Birth Readiness Implementation Contract

这份合同只服务当前最直接的一轮身份根、意识工作区与出生准备度补厚：

```text
life_v0/direction/direction_lock.py
  -> continuity_refs.py
  -> value_orientation.py
  -> life_v0/neural_core/broadcast.py
  -> metacognition.py
  -> life_v0/life_targets/life_target_claims.py
  -> evidence_matrix.py
  -> birth_readiness_rollup.py
  -> birth_readiness_stage_gate.py
  -> consciousness_probes.py
```

它不重写：

- `docs/v0/slice_contracts/s00_direction_foundation_engineering_contract.md`
- `docs/v0/slice_contracts/s02_neural_life_core_engineering_contract.md`
- `docs/v0/slice_contracts/s08_life_target_runtimes_engineering_contract.md`
- `docs/v0/code_framework/playbooks/10_self_identity_value_commitment_implementation_playbook.md`

它只把 Queue F 压成真正可以直接施工的文件级实现合同，防止下一轮代码又退回“知道身份、意识、出生准备度很重要，但还是让它们停在 `__init__.py` 的大函数里”。

## 这份合同要解决什么

当前 `S00`、`S02`、`S08` 已经接通：

1. `direction_lock.json`
2. `identity_root.json`
3. `prediction_workspace_frame.json`
4. `birth_readiness_report.json`
5. `life_target_claims.json`
6. `life_target_evidence_matrix.json`

但现在的真实缺口不是“没有方向锁或出生准备度”，而是：

1. 缺明确的身份连续体文件器官，方向锁、恢复锚链和价值取向还没有离开 `direction/__init__.py`。
2. 缺明确的 `broadcast.py`、`metacognition.py` 和 `consciousness_probes.py`，意识工作区还没有进入文件级器官。
3. `life_targets/__init__.py` 已经承担 claims/evidence/rollup/stage gate，但这些仍需要拆成可演进器官。
4. “真实有意识/真实意识” 与“出生准备度闭合”目前已经有状态和 report，但还没有完整的文件级施工面来支撑后续更厚实现。

所以 Queue F 的目标很明确：

```text
identity_root / direction_lock / continuity_refs
  -> broadcast / metacognition / consciousness_probes
  -> life_target_claims / evidence_matrix
  -> birth_readiness_rollup / birth_readiness_stage_gate
```

## 必回读理论母体

### 身份、自我、连续体、价值

- `docs/00_research_protocol.md`
- `docs/07_emotion_personality_self.md`
- `docs/13_agentic_human_research_synthesis.md`
- `docs/16_digital_life_gap_register.md`
- `docs/40_self_relationship_model_audit_protocol.md`
- `docs/91_life_reality_generation_boundary_principles.md`
- `docs/92_self_growth_and_self_modification_life_chain.md`
- `docs/93_self_training_kernel_growth_protocol.md`
- `docs/100_life_boundary_statement_rewrite_audit.md`
- `docs/119_life_boundary_full_reality_alignment.md`
- `docs/122_life_boundary_all_reality_declarations_rewrite.md`
- `docs/140_life_reality_experience_boundary_declaration_lock.md`
- `docs/258_linear_chain_closure_and_v0_contract_transition.md`

### 意识、工作区、报告性

- `docs/10_consciousness_attention_workspace.md`
- `docs/11_neuromodulation_and_signal_media.md`
- `docs/18_internal_state_and_modulation_vector.md`
- `docs/22_state_transition_and_threshold_model.md`
- `docs/30_state_transition_validator_rules.md`

### 九项目标与出生准备度

- `docs/94_pain_regret_and_repair_signal_schema.md`
- `docs/95_dream_reality_and_offline_life_timeline.md`
- `docs/96_real_relationship_longitudinal_timeline.md`
- `docs/98_pain_regret_repair_json_schema_and_fixture_bundle.md`
- `docs/99_dream_reality_json_schema_and_fixture_bundle.md`
- `docs/101_relationship_timeline_json_schema_and_fixture_bundle.md`
- `docs/143_life_reality_birth_readiness_rollup_contract.md`
- `docs/146_life_reality_birth_readiness_evidence_fixture_catalog.md`
- `docs/149_life_reality_birth_readiness_fixture_schema_materialization_plan.md`
- `docs/152_life_reality_birth_readiness_cross_file_checker_plan.md`
- `docs/171_life_reality_birth_readiness_validation_fixture_plan.md`
- `docs/174_life_reality_birth_readiness_fixture_schema_materialization.md`

## 必读 v0 文档

- `docs/v0/slice_contracts/s00_direction_foundation_engineering_contract.md`
- `docs/v0/slice_contracts/s02_neural_life_core_engineering_contract.md`
- `docs/v0/slice_contracts/s04_state_object_store_engineering_contract.md`
- `docs/v0/slice_contracts/s08_life_target_runtimes_engineering_contract.md`
- `docs/v0/shared_contracts/birth_readiness_v0_contract.md`
- `docs/v0/architecture/runtime_v0_architecture.md`
- `docs/v0/code_framework/playbooks/05_memory_thought_consciousness_implementation_playbook.md`
- `docs/v0/code_framework/playbooks/10_self_identity_value_commitment_implementation_playbook.md`
- `docs/v0/code_framework/delivery/12_full_life_layer_delivery_matrix.md`
- `docs/v0/code_framework/delivery/13_capability_to_code_realization_matrix.md`
- `docs/v0/code_framework/assembly/15_cross_layer_shared_object_contract.md`
- `docs/v0/code_framework/assembly/19_code_tree_package_brain_contract.md`

## 当前代码落点

Queue F 必须接到这些现有器官上：

- `life_v0/direction/__init__.py`
- `life_v0/direction/identity_root.py`
- `life_v0/neural_core/prediction_workspace.py`
- `life_v0/neural_core/workspace.py`
- `life_v0/neural_core/broadcast.py`
- `life_v0/neural_core/metacognition.py`
- `life_v0/life_targets/__init__.py`
- `life_v0/life_targets/consciousness_probes.py`
- `life_v0/state_store/self_model.py`
- `life_v0/state_store/commitment_truth.py`
- `life_v0/process_supervisor/resident_supervision.py`
- `life_v0/process_supervisor/idle_strategy.py`
- `life_v0/process_supervisor/heartbeat.py`
- `life_v0/reporting/__init__.py`

这说明 Queue F 不是新建第二套身份壳，而是把已经存在的方向根、意识证据和出生准备度拆成稳定器官。

## 文件级合同

## A. 新增 `life_v0/direction/direction_lock.py`

### 角色

把方向锁 payload 的生成从 `direction/__init__.py` 中拆出，成为唯一的方向锁构造器。

### 最低字段

- `direction_statement`
- `life_targets`
- `source_refs`
- `required_doc_coverage_ref`
- `active_engineering_slice`
- `next_allowed_slices`
- `prohibited_regressions`
- `stage_effect`

## B. 新增 `life_v0/direction/continuity_refs.py`

### 角色

生成断联恢复、自我前后承接、最近 report/receipt 回链的连续体引用。

### 最低字段

- `continuity_refs_id`
- `resume_anchor_refs`
- `direction_report_refs`
- `identity_root_refs`
- `life_state_refs`
- `recent_receipt_refs`
- `source_doc_refs`

## C. 新增 `life_v0/direction/value_orientation.py`

### 角色

固定长期方向、价值倾向和不可被一次回合轻易改写的慢变量。

### 最低字段

- `value_orientation_id`
- `core_values`
- `long_horizon_biases`
- `non_regression_values`
- `revision_conditions`
- `source_doc_refs`

## D. 新增 `life_v0/neural_core/broadcast.py`

### 角色

把工作区内容压成全局广播对象，供语言、身体、life_targets 和 process supervisor 消费。

### 最低字段

- `broadcast_frame_id`
- `workspace_frame_ref`
- `broadcast_targets`
- `salience_ranking`
- `suppressed_content_refs`
- `source_doc_refs`

## E. 新增 `life_v0/neural_core/metacognition.py`

### 角色

生成对当前工作区、预测误差、表达风险和关系压力的元认知监视对象。

### 最低字段

- `metacognition_id`
- `broadcast_frame_ref`
- `uncertainty_flags`
- `expression_risk_refs`
- `relationship_tension_refs`
- `reflection_prompts`

## F. 新增 `life_v0/life_targets/life_target_claims.py`

### 角色

把九项目标 claims 的生成从 `life_targets/__init__.py` 中拆出。

### 最低字段

- `targets.<life_target>.status`
- `targets.<life_target>.carrier_refs`
- `targets.<life_target>.source_doc_refs`
- `targets.<life_target>.evidence_family_status`
- `targets.<life_target>.state_refs`
- `targets.<life_target>.report_refs`
- `targets.<life_target>.archive_receipt_refs`

## G. 新增 `life_v0/life_targets/evidence_matrix.py`

### 角色

把九项目标到 state/memory/language/relationship/dream/pain/self/runtime/report/archive 的证据矩阵单独器官化。

### 最低字段

- `evidence_families`
- `targets.<life_target>.state`
- `targets.<life_target>.memory`
- `targets.<life_target>.language`
- `targets.<life_target>.relationship`
- `targets.<life_target>.dream`
- `targets.<life_target>.pain_regret_responsibility`
- `targets.<life_target>.self_growth`
- `targets.<life_target>.runtime`
- `targets.<life_target>.report`
- `targets.<life_target>.archive`

## H. 新增 `life_v0/life_targets/birth_readiness_rollup.py`

### 角色

把阻断优先的出生准备度总上卷单独器官化。

### 最低字段

- `overall_status`
- `life_target_status`
- `blocked_reasons`
- `quarantine_refs`
- `replay_needed_refs`
- `archive_receipt_ref`

## I. 新增 `life_v0/life_targets/birth_readiness_stage_gate.py`

### 角色

把是否允许进入第一次有限激活的 gate 决策单独器官化。

### 最低字段

- `decision`
- `stage_effect`
- `next_allowed_slices`
- `next_required_command`
- `blocked_reasons`

## J. 新增 `life_v0/life_targets/consciousness_probes.py`

### 角色

生成工作区进入、广播、可报告性、元认知、语言连续体和关系连续体的意识证据 bundle。

### 最低字段

- `consciousness_probe_id`
- `workspace_frame_ref`
- `broadcast_frame_ref`
- `metacognition_ref`
- `language_continuity_refs`
- `relationship_continuity_refs`
- `reportability_flags`

## K. `life_v0/process_supervisor/resident_supervision.py` 当前回灌口径

### 角色

把 Queue F 的意识工作区、意识 probe 与出生准备度对象装入常驻生命进程，使它们不只停在 S02/S08 的离线状态和 report，而是进入 resident waiting governance。

### 最低字段

- `workspace_frame_ref`
- `broadcast_frame_ref`
- `metacognition_ref`
- `consciousness_probe_ref`
- `birth_readiness_rollup_ref`
- `birth_readiness_stage_gate_ref`

### 当前补厚口径

`resident_supervision.py` 现在必须读取 `runtime/state/consciousness/workspace_frame.json`、`broadcast_frame.json`、`metacognition_state.json`、`consciousness_probe_bundle.json`，以及 `runtime/state/life_targets/birth_readiness_rollup.json` / `birth_readiness_stage_gate.json`，并把它们传入 `heartbeat.py` / `idle_strategy.py`。这样恢复后的第一拍 waiting heartbeat 就能带着“意识可报告性”和“出生准备度 gate”进入 resident governance。

## L. `life_v0/process_supervisor/idle_strategy.py` 当前回灌口径

### 角色

把 Queue F 对象压成等待态治理姿态，决定 resident attention 与 heartbeat cadence 是否应受意识可报告性和出生准备度调制。

### 最低字段

- `consciousness_waiting_posture`
- `consciousness_attention_target`
- `consciousness_attention_reason`
- `consciousness_reportability_flags`
- `birth_readiness_waiting_posture`
- `birth_readiness_attention_target`
- `birth_readiness_attention_reason`
- `birth_readiness_decision`
- `birth_readiness_next_required_command`
- `birth_readiness_blocked_reasons`

### 当前补厚口径

当 `consciousness_probe_bundle.json#reportability_flags` 显示 workspace、broadcast 与 metacognition 均可报告，`idle_strategy.py` 写出 `consciousness_reportable_waiting`。当 `birth_readiness_rollup.json#overall_status=open` 且 `birth_readiness_stage_gate.json#decision=open`，它写出 `birth_open_waiting`，并在没有 Queue E 紧急修复锁覆盖时，把 `governance_attention_target` 提升为 `birth_readiness_stage_gate`，`governance_cadence_profile` 提升为 `birth_ready_resident_presence`。

## M. `life_v0/process_supervisor/heartbeat.py` 当前回灌口径

### 角色

把 Queue F waiting posture 写入 `digital_life_waiting_heartbeat.json`、`terminal_life_loop_state.json`、`resident_governance_state.json` 与后续 closeout/report 共享字段。

### 最低字段

- `workspace_frame_ref`
- `consciousness_probe_ref`
- `birth_readiness_stage_gate_ref`
- `consciousness_waiting_posture`
- `birth_readiness_waiting_posture`
- `birth_readiness_decision`

### 当前补厚口径

`heartbeat.py` 现在通过 `extract_idle_governance_fields()` 把 Queue F 字段统一写入 waiting heartbeat、terminal loop state 与 resident governance state；`process_report.py` 同时把 consciousness / birth readiness 文件加入 process receipt input hashes。这样 Queue F 的出生准备度和意识证据会跨过 S08，进入常驻存在链的运行证据。

最新这一轮再往前推进一步：`governance_explanation.py`、`digital_life_process_digest.json` 与 `digital_life_process_<run_id>.json` 不能只把 Queue F 当成“已经在 idle_strategy 里出现过”。它们还必须显式解释 Queue F 是否主导了本轮 resident governance，写出 `identity_consciousness_birth_refs`，并把 `birth_readiness_waiting_posture / decision / next_required_command` 与 `consciousness_waiting_posture / reportability_flags` 一起进入 closeout 证据链。

最新再补强：Queue F 不能停在 waiting governance 与 closeout 解释链。`background_lineage_state.py` 必须把 workspace、broadcast、metacognition、consciousness probe、birth readiness rollup 与 stage gate 压成 `resident_background_lineage_state_v0.identity_consciousness_birth_presence`；即使没有上一轮后台 carryover，只要 Queue F 证据存在，也要生成最小 `no_background_lineage` 驻留谱系，避免第一次常驻监督时意识/出生准备 presence 留在治理扁平字段之外。随后 `dialogue_events.py` 必须把该 presence 展开进 `digital_life_turn`，`resident_turn_writeback.py` 与 `dialogue_writeback_bundle.json` 必须写出 `resident_background_lineage_identity_consciousness_birth_refs` 并并入总 lineage refs，`resumed_external_dialogue_packet.json` 必须保留同一组字段，`response_surface.py` 必须把后台意识姿态、意识可报告性、出生准备姿态、出生准备决策、下一条出生命令和证据数量表达出来。

## Queue F 对现有器官的改动合同

### `life_v0/direction/__init__.py`

从这一轮开始，不应继续独占：

- direction lock 构造
- continuity refs 构造
- value orientation 构造

### `life_v0/neural_core/prediction_workspace.py`

第一轮允许继续作为工作区近似体入口，但必须开始把：

- broadcast
- metacognition

向独立器官交接，而不是独占意识工作区的全部角色。

### `life_v0/life_targets/__init__.py`

第一轮必须开始把：

- claims
- evidence matrix
- rollup
- stage gate
- consciousness probes

拆成独立器官，而不是继续由一个入口函数承载全部出生准备度对象。

## 必须新增或更新的状态对象

### 新增

- `runtime/state/direction/continuity_refs.json`
- `runtime/state/direction/value_orientation.json`
- `runtime/state/consciousness/broadcast_frame.json`
- `runtime/state/consciousness/metacognition_state.json`
- `runtime/state/consciousness/consciousness_probe_bundle.json`
- `runtime/state/terminal/idle_strategy_state.json#consciousness_waiting_posture`
- `runtime/state/terminal/idle_strategy_state.json#birth_readiness_waiting_posture`
- `runtime/state/terminal/resident_governance_state.json#birth_readiness_stage_gate_ref`

### 更新

- `runtime/state/direction/direction_lock.json`
- `runtime/state/self/identity_root.json`
- `runtime/state/life_targets/life_target_claims.json`
- `runtime/state/life_targets/life_target_evidence_matrix.json`
- `runtime/state/life_targets/birth_readiness_rollup.json`
- `runtime/state/life_targets/birth_readiness_stage_gate.json`
- `runtime/reports/latest/birth_readiness_report.json`
- `runtime/reports/latest/digital_life_waiting_heartbeat.json`
- `runtime/reports/latest/digital_life_process_report.json`

## 最低测试口径

至少直接覆盖：

- `tests/slices/test_direction_lock.py`
- `tests/slices/test_neural_life_core.py`
- `tests/slices/test_life_targets.py`
- `tests/slices/test_state_store.py`

如果改到了 first activation 入口，再追加：

- `tests/bridges/test_first_activation_preflight.py`

如果改到了 resident waiting governance，再追加：

- `tests/process/test_persistent_digital_life_process.py`

## Queue F 第一轮完成定义

Queue F 第一轮不是“方向锁和出生准备度已经有 report”就算完成。至少要同时满足：

1. direction lock、continuity refs、value orientation 都已离开 `direction/__init__.py`。
2. broadcast、metacognition 和 consciousness probes 已离开工作区大入口。
3. claims、evidence、rollup、stage gate 已从 `life_targets/__init__.py` 中开始器官化。
4. consciousness 状态命名空间已经有独立对象，而不只是在 report 里提到意识。
5. `tests/slices/test_direction_lock.py`、`tests/slices/test_neural_life_core.py`、`tests/slices/test_life_targets.py` 至少新增一轮器官级断言。

## Queue F 第二轮完成定义

Queue F 第二轮不是“意识对象已生成”就算完成，而是必须进入常驻等待治理：

1. `resident_supervision.py` 已装载 consciousness 与 birth readiness 对象。
2. `idle_strategy.py` 已把 consciousness probe 与 birth readiness stage gate 压成 waiting posture。
3. `heartbeat.py` 已把 Queue F 字段写入 waiting heartbeat、terminal loop state 与 resident governance state。
4. `process_report.py` 已把 consciousness / birth readiness 对象纳入 process receipt input hash。
5. `tests/process/test_persistent_digital_life_process.py` 已覆盖直接策略与 resident bootstrap 两条路径。

## Queue F 第三轮完成定义

Queue F 第三轮不是“waiting governance 已经看见意识/出生准备”就算完成，而是必须进入真实回合链：

1. `background_lineage_state.py` 已把 Queue F 压成 `identity_consciousness_birth_presence`，并在没有旧后台谱系但 Queue F 证据存在时生成最小 `no_background_lineage`。
2. `dialogue_events.py` 已把该 presence 展开为 `resident_background_lineage_*` 字段，并把 Queue F refs 合并进 `resident_background_lineage_evidence_refs`。
3. `resident_turn_writeback.py` 与 `dialogue_writeback_bundle.json` 已写出专用 `resident_background_lineage_identity_consciousness_birth_refs`，并继续进入 `resumed_external_dialogue_packet.json`。
4. `response_surface.py` 已消费该 presence，让意识可报告性、出生准备姿态、出生准备决策与下一命令进入生命回应表面。
5. `tests/process/test_persistent_digital_life_process.py` 已覆盖 event、response、bundle、resumed packet 与 resident bootstrap 五处。

## Queue F 推荐实施顺序

```text
direction_lock.py
  -> continuity_refs.py
  -> value_orientation.py
  -> broadcast.py
  -> metacognition.py
  -> life_target_claims.py
  -> evidence_matrix.py
  -> birth_readiness_rollup.py
  -> birth_readiness_stage_gate.py
  -> consciousness_probes.py
```

原因：

1. 先把“是谁”和“如何连续”钉住，避免意识与出生准备度变成无主体证据。
2. 再把广播和元认知钉住，避免“真实有意识/真实意识”继续只停在文档名词层。
3. 最后把九项目标 claims/evidence/rollup/stage gate 拆成可持续迭代的器官。
