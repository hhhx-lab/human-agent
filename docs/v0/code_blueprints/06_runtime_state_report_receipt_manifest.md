# Runtime State Report Receipt Manifest

这份蓝图把 v0 的 runtime 承载面统一成一张 manifest。

它回答的问题只有一个：

```text
后续新增任何数字生命器官时，
状态写到哪，
报告写到哪，
receipt 写到哪，
以及这些文件家族怎样组成第一次生命激活证据链。
```

## 三个承载面

| 承载面 | 路径 | 作用 |
|---|---|---|
| 状态 | `runtime/state/` | 当前生命结构、对象、工作区、节律、关系、责任、梦境、成长 |
| 报告 | `runtime/reports/latest/` | 当前运行的阶段性可读结果、bundle、digest、stage gate |
| receipt | `runtime/receipts/` | 本轮执行的可回放、可审计输入输出指纹 |

## 状态命名空间

| 命名空间 | 关键文件 |
|---|---|
| `direction/` | `direction_lock.json` |
| `authority/` | `authority_registry.json` |
| `neural_life_core/` | `neural_life_core.json` |
| `prediction/` | `prediction_workspace_frame.json` |
| 根状态 | `life_state.json`、`object_registry.json`、`lifecycle_policy.json` |
| `body/` | `need_state_vector.json`、`body_rhythm_pulse.json`、`core_affect_vector.json` |
| `defense/` | `defense_boundary_state.json` |
| `language/` | `inner_speech_frame.json`、`expression_plan.json`、`semantic_map_frame.json` |
| `relationship/` | `relationship_subject_graph.json` |
| `terminal/` | `life_context_frame.json`、`relation_turn_frame.json`、`safe_terminal_loop_state.json`、`terminal_life_loop_state.json`、`idle_continuity_frame.json` |
| `membrane/` | `life_membrane.json`、`dream_fact_boundary.json`、`responsibility_repair_boundary.json` |
| `action/` | `action_candidate_set.json`、`go_nogo_state.json`、`world_contact_gate_state.json`、`side_effect_review.json`、`responsibility_loop_state.json` |
| `validation/` | `observation_truth_review.json`、`boundary_audit_state.json`、`validation_stage_gate.json` |
| `observation/` | `runtime_observation_intake.json` |
| `schema_runner/` | `schema_registry.json`、`consistency_logic.json`、`counterfactual_trace.json`、`comparison_trace.json`、`evidence_ranking.json` |
| `life_targets/` | `life_target_claims.json`、`birth_readiness_stage_gate.json` |
| `dream/` | `dream_experience_window.json`、`offline_consolidation_frame.json`、`nightmare_loop_risk.json` |
| `replay/` | `shadow_cycle_trace.json`、`replay_cue_bundle.json` |
| `growth/` | `plasticity_window_state.json`、`growth_patch_candidate_queue.json`、`anti_forgetting_replay_plan.json` |
| `archive/` | `reconsolidation_archive_graph.json` |
| `activation/` | `limited_context_frame.json`、`life_membrane_opening_decision.json` |
| `contracts/` | `v0_contract_file_index.json`、`doc_to_code_coverage_matrix.json` |

## 报告家族

### 主体 slice 报告

1. `direction_lock_report.json`
2. `source_authority_report.json`
3. `neural_life_core_report.json`
4. `state_store_report.json`
5. `life_membrane_report.json`
6. `language_relationship_report.json`
7. `birth_readiness_report.json`
8. `validation_membrane_report.json`
9. `schema_runner_report.json`
10. `life_support_development_report.json`
11. `growth_reconsolidation_report.json`
12. `v0_contract_coverage_report.json`

### 链尾桥接报告

1. `first_activation_preflight_report.json`
2. `replay_shadow_report.json`
3. `growth_archive_report.json`
4. `report_bundle.json`
5. `stage_explanation_report.json`
6. `digital_life_birth_packet.json`
7. `first_terminal_turn_report.json`
8. `terminal_life_loop_report.json`
9. `digital_life_shell_report.json`
10. `digital_life_process_report.json`

### digest 家族

1. `digest.json`
2. `report_bundle_digest.json`
3. `digital_life_birth_digest.json`
4. `first_terminal_turn_digest.json`
5. `terminal_life_loop_digest.json`
6. `digital_life_process_digest.json`

## receipt 家族

| 家族 | 模式 |
|---|---|
| 文档/合同 | `doc_ingestion_*.json`、`v0_contract_coverage_*.json` |
| 主体 slice | `direction_lock_*.json`、`source_authority_*.json`、`neural_life_core_*.json`、`state_store_*.json`、`life_membrane_*.json`、`language_relationship_*.json`、`birth_readiness_*.json`、`validation_membrane_*.json`、`schema_runner_*.json`、`life_support_development_*.json` |
| reconsolidation 链 | `run_cycle_*.json`、`first_activation_preflight_*.json`、`emit_report_*.json`、`explain_stage_*.json`、`digital_life_birth_*.json`、`first_terminal_turn_*.json`、`terminal_life_loop_*.json` |
| 进程层 | `digital_life_shell_command_*.json`、`digital_life_process_*.json` |

## 最小规则

1. 新器官如果只写 state，不写 report，不算闭合。
2. 新器官如果只写 report，不写 state，不算主体器官。
3. 新命令如果不写 receipt，不允许进入长期存在链。
4. `runtime/reports/latest/` 是当前权威快照，不是 archive。
5. archive 由 `runtime/state/archive/*` 和对应 receipts 共同承接，不替代 latest report。

## 本页的用法

后续每新增一个文件，都至少补这四项：

1. 首写哪个 state 文件。
2. 影响哪个 latest report。
3. 产生哪个 receipt 家族。
4. 被哪个 stage gate 或 test 验证。

