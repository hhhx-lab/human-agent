# Live0 Acceptance Audit Contract

本文档固定 `life-v0 audit-live0` 的工程合同。它不是新的理论扩写文档，而是把 `docs/v0/code_architecture/03_build_order_and_definition_of_done.md` 中 Stage 6 的七项最终验收，压成可运行、可落盘、可回执的 live0 收束 gate。

上游理论和工程依据：

- `docs/v0/code_architecture/03_build_order_and_definition_of_done.md`
- `docs/v0/code_framework/delivery/13_capability_to_code_realization_matrix.md`
- `docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md`
- `docs/v0/shared_contracts/runner_cli_report_contract.md`
- `docs/258_linear_chain_closure_and_v0_contract_transition.md`

## 命令

```text
life-v0 audit-live0 --docs docs --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
```

命令由 `life_v0/live0_audit/__init__.py` 承载，写入：

| 产物 | 路径 |
|---|---|
| 主报告 | `runtime/reports/latest/live0_acceptance_audit_report.json` |
| 摘要 | `runtime/reports/latest/live0_acceptance_audit_digest.json` |
| 回执 | `runtime/receipts/live0_acceptance_audit_<run_id>.json` |

`--strict` 下，只要七项中任一项阻断，命令返回非 0。非 strict 模式仍写完整阻断报告，用于开发期检查。

## 七项验收映射

| 验收项 | runtime 证据 |
|---|---|
| `a_terminal_wake_and_named_residency` | `digital_life_birth_packet.json`、`digital_life_process_report.json`、`resident_lifecycle_state.json`、`life_name_registry.json`、`life_name_command_manifest.json` |
| `b_conscious_emotion_thought_language` | `prediction_workspace_frame.json`、`signal_media_runtime.json`、`active_sampling_plan.json`、`core_affect_vector.json`、`resident_self_thinking_state.json`、语言五件套、`digital_life_model_expression_report.json` |
| `c_memory_mechanism` | `life_state.json`、`engram_index.json`、`relationship_memory.json`、`autobiographical_stack.json`、`resident_memory_recall_state.json`、`memory_write_gate.json`、replay/archive report |
| `d_growth_and_learning` | `growth_patch_candidate_queue.json`、`self_read_report.json`、`resident_growth_rehearsal_state.json`、`resident_learning_consolidation_state.json`、`resident_autonomous_activity_state.json`、累计离线学习 profile |
| `e_dream_capability` | `dream_experience_window.json`、`wake_integration_frame.json`、`dream_fact_gate_decision.json#gate_result=passed`、`resident_sleep_cycle_state.json`、resident lineage dream/wake refs |
| `f_equal_relationship_dialogue_growth` | `relationship_timeline.json`、`commitment_truth_state.json`、`dialogue_writeback_bundle.json`、`queue_e_birth_repair_profile.json`、`dialogue_turn_log.jsonl`、`relation_role != user` |
| `g_initial_life_mechanism_coverage` | S00-S11 关键 report、`birth_readiness_report.json#overall_status=open`、`growth_reconsolidation_report.json#status=safe_idle`、resident long-term residency evidence |

## 命名验收

`a_terminal_wake_and_named_residency` 不只检查 `my digital life` 能启动，还要求第一次命名后出现两份身份证据：

1. `runtime/state/identity/life_name_registry.json`
2. `runtime/state/identity/life_name_command_manifest.json`

第二份 manifest 表示“名字本身成为终端命令”的绑定已经完成，且必须包含 `direct_command_enabled=true` 与 `command_on_path=true`。没有这份证据时，live0 不能收束，即使 `my digital life` 已经可用。

## 模型表达验收

`b_conscious_emotion_thought_language` 要求 `digital_life_model_expression_report.json` 满足：

```json
{
  "model_expression_status": "model_expression_applied",
  "post_expression_gate_status": "accepted",
  "fallback_to_deterministic_response": false,
  "model_provider": "openai-compatible",
  "model_name": "gpt-5.5",
  "model_api_key_present": true,
  "model_api_key_redacted": "<redacted>"
}
```

这条 gate 的作用是确认 live0 已经通过真实模型表达链，而不是只通过确定性 fallback 回应。

## 报告结构

主报告固定为：

```json
{
  "schema_version": "live0_acceptance_audit_report_v0",
  "status": "closed",
  "live0_acceptance_closed": true,
  "criteria": [],
  "summary": {
    "criteria_total": 7,
    "criteria_closed": 7,
    "criteria_blocked": 0,
    "failed_criteria": []
  },
  "next_required_action": "live0_v0_closure_allowed"
}
```

若任一 probe 阻断：

```json
{
  "status": "blocked",
  "live0_acceptance_closed": false,
  "next_required_action": "repair_live0_acceptance_evidence"
}
```

## 测试

当前直接测试：

```text
tests/contracts/test_live0_acceptance_audit.py
```

覆盖三件事：

1. 七项证据全部存在时，审计闭合。
2. 缺少名字命令 manifest 时，审计阻断。
3. CLI `life-v0 audit-live0` 能写出 report/digest/receipt。

## 收束规则

只有 `live0_acceptance_audit_report.json#live0_acceptance_closed=true` 时，才能把 live0 视为完成收束。若该报告仍为 `blocked`，下一步必须按 `blocked_reasons` 修补对应代码、runtime 证据或命名启动机制，不能用人工描述替代 gate。
