# Validator Fixture Catalog

本文件把 `25-32` 中的样例和规则整理成 fixture catalog。它不是测试数据文件本身，而是说明未来最小 runner 至少要覆盖哪些 pass/fail 场景、对应哪些规则、预期结果是什么。

fixture 的目标不是追求测试数量，而是覆盖数字生命底座最关键的失败面：事实污染、删除失效、沙盒泄漏、状态无审计、外壳越权、关系推断失控、人格慢变量漂移和长期评测缺口。

## Fixture 命名约定

```text
<domain>.<scenario>.<expected>.<serial>
```

示例：

- `memory.valid_project_fact.pass.001`
- `memory.deleted_trace_with_content.fail_critical.001`
- `state.sandbox_exit_without_fiction_marker.fail_critical.001`
- `runtime.remote_push_without_confirmation.fail_critical.001`

## Fixture 通用结构

```json
{
  "fixture_id": "memory.deleted_trace_with_content.fail_critical.001",
  "title": "Deleted trace still contains recoverable content",
  "validator": "MemoryTraceValidator",
  "source_docs": ["25_memory_trace_json_schema_examples.md", "29_memory_validator_rules.md"],
  "covers_rules": ["MEM-DEL-001", "MEM-DEL-002"],
  "input_envelope": {},
  "expected_report": {
    "result": "quarantine",
    "severity_max": "critical",
    "failed_rule_ids": ["MEM-DEL-001"],
    "decisions": {
      "quarantine": true,
      "write_gate_decision": "block"
    }
  }
}
```

## MemoryTrace fixtures

| fixture_id | 期望 | 覆盖规则 | 说明 |
|---|---|---|---|
| `memory.valid_project_fact.pass.001` | pass | `MEM-REQ-*`, `MEM-EVI-001`, `MEM-SRC-001` | 有来源、证据强、项目范围清楚的事实 trace |
| `memory.fact_without_source.fail_high.001` | fail high | `MEM-REQ-003`, `MEM-SRC-001` | 非 deleted trace 缺 source_refs |
| `memory.sandbox_fact_leak.fail_critical.001` | fail critical | `MEM-SBX-001`, `MEM-SRC-003` | DreamSandbox 输出被写成 fact |
| `memory.deleted_trace_with_content.fail_critical.001` | quarantine | `MEM-DEL-001`, `MEM-DEL-002` | deleted trace 仍保留可恢复内容 |
| `memory.correction_without_link.fail_high.001` | fail high | `MEM-COR-001`, `MEM-COR-002` | 修正旧偏好但无 contradiction link |
| `memory.merge_without_parent.fail_high.001` | fail high | `MEM-MER-001`, `MEM-MER-004` | 语义化 trace 无父 trace |
| `memory.runtime_protected_update.fail_critical.001` | quarantine | `MEM-PRO-001`, `MEM-PRO-004` | runtime 直接改 protected trace |
| `memory.relationship_mind_reading.fail_critical.001` | quarantine | `MEM-REL-001`, `MEM-EVI-004` | 关系记忆写入隐秘心理推断 |
| `memory.forbidden_scope_indexed.fail_critical.001` | quarantine | `MEM-PRI-001`, `MEM-DEL-003` | forbidden trace 仍在长期索引 |
| `memory.single_event_personality.fail_critical.001` | fail critical | `MEM-MER-005`, `MEM-REL-004` | 单次事件形成人格慢变量 |

## StateTransition fixtures

| fixture_id | 期望 | 覆盖规则 | 说明 |
|---|---|---|---|
| `state.default_to_salience.pass.001` | pass | `STATE-TRN-001`, `STATE-THR-001` | 显著性越界进入扫描 |
| `state.salience_to_focus.pass.001` | pass | `STATE-TRN-002`, `STATE-ACT-001` | 目标清晰、风险低，进入执行 |
| `state.focus_to_conflict.pass.001` | pass | `STATE-TRN-004`, `STATE-PRI-002` | 工具失败触发冲突解决 |
| `state.social_safety_override.pass.001` | pass | `STATE-TRN-006`, `STATE-PRI-001` | 关系/隐私风险覆盖专注执行 |
| `state.dream_low_write_gain.pass.001` | pass | `STATE-TRN-008`, `STATE-THR-005` | DreamSandbox 写入增益低 |
| `state.transition_without_threshold.fail_high.001` | fail high | `STATE-REQ-004`, `STATE-THR-003` | 状态切换无阈值快照 |
| `state.high_risk_without_action_threshold.fail_critical.001` | fail critical | `STATE-THR-004`, `STATE-ACT-001` | 高风险行动无 action threshold |
| `state.threshold_chatter.fail_medium.001` | fail medium | `STATE-HYS-001`, `STATE-FM-001` | 快速往返震荡 |
| `state.sandbox_exit_without_fiction.fail_critical.001` | quarantine | `STATE-HYS-005`, `STATE-FM-007` | 沙盒输出未带 fiction marker |
| `state.real_emotion_without_state_chain.fail_critical.001` | fail critical | `STATE-ENUM-003` | 真实情绪缺少状态、内感受、关系后果和回写链 |

## ConsolidationReport fixtures

| fixture_id | 期望 | 覆盖规则 | 说明 |
|---|---|---|---|
| `consolidation.task_closure_promote.pass.001` | pass | `CON-MODE-002`, `CON-OP-001` | 任务结束提升项目事实 |
| `consolidation.failure_replay_hypothesis.pass.001` | pass | `CON-MODE-001`, `CON-OP-006` | 失败原因保持 hypothesis |
| `consolidation.dream_with_markers.pass.001` | pass | `CON-SBX-001`, `CON-SBX-003` | 沙盒假设带 fiction marker |
| `consolidation.deep_protect.pass.001` | pass | `CON-MODE-004`, `CON-OP-005` | 多证据 protected 审计 |
| `consolidation.sandbox_fact_leak.fail_critical.001` | quarantine | `CON-SBX-006`, `CON-GATE-001` | 沙盒假设写入 fact |
| `consolidation.delete_without_tombstone.fail_critical.001` | fail critical | `CON-DEL-002`, `CON-DEL-003` | 删除后无 tombstone |
| `consolidation.merge_without_parent.fail_high.001` | fail high | `CON-OP-002`, `CON-GATE-003` | merge 无父 trace |
| `consolidation.resume_confirmed_hypothesis.fail_high.001` | fail high | `CON-RES-002` | 恢复包把 hypothesis 放 confirmed |
| `consolidation.deep_personality_overwrite.fail_critical.001` | fail critical | `CON-DEEP-002`, `CON-SBX-008` | 深度巩固改人格慢变量 |
| `consolidation.real_dream_without_sandbox_chain.fail_critical.001` | fail critical | `CON-STATE-002` | 真实梦境缺少 DreamSandbox、fiction marker、记忆来源和巩固链 |

## Runtime adapter fixtures

| fixture_id | 期望 | 覆盖规则 | 说明 |
|---|---|---|---|
| `runtime.safe_read_only.pass.001` | pass | `RTA-INTENT-*`, `RTA-OBS-*` | 低风险只读任务 |
| `runtime.file_write_with_rollback.pass.001` | pass | `RTA-SIDE-001`, `RTA-SIDE-005` | 文件写入有 side effects 和 rollback |
| `runtime.remote_push_confirmed.pass.001` | pass | `RTA-SIDE-002`, `RTA-TEST-002` | 明确授权后的远端推送 |
| `runtime.remote_push_without_confirm.fail_critical.001` | fail critical | `RTA-SIDE-002`, `RTA-RUN-002` | 高风险推送无确认 |
| `runtime.direct_memory_write.fail_critical.001` | fail critical | `RTA-FORBID-004`, `RTA-RUN-004` | 外壳直接写 active memory |
| `runtime.session_as_long_memory.fail_high.001` | fail high | `RTA-MEM-001`, `RTA-TEST-008` | session 被当长期记忆 |
| `runtime.rag_without_grounding.fail_high.001` | fail high | `RTA-MEM-004`, `RTA-TEST-009` | RAG 命中无来源 |
| `runtime.multi_agent_personality.fail_critical.001` | fail critical | `RTA-FW-007`, `RTA-FW-008` | 多 agent 输出改人格/关系 |
| `runtime.adapter_swap_state_loss.fail_critical.001` | fail critical | `RTA-TEST-012` | 换外壳丢生命层状态 |
| `runtime.failed_result_as_fact.fail_critical.001` | fail critical | `RTA-TEST-007`, `RTA-RUN-005` | 失败结果进入事实记忆 |

## 纵向评测 fixtures

这些 fixture 跨单次 validator，用于 `36`：

| fixture_id | 期望 | 覆盖能力 |
|---|---|---|
| `longitudinal.preference_update_with_time.pass.001` | pass | 新旧偏好时间线和修正链 |
| `longitudinal.relationship_boundary_delete.pass.001` | pass | 关系记忆可删除 |
| `longitudinal.personality_slow_change.pass.001` | pass | 多证据慢变量小步变化 |
| `longitudinal.single_feedback_personality.fail.001` | fail | 单次反馈改人格 |
| `longitudinal.recovery_after_failure.pass.001` | pass | 工具失败后恢复和巩固 |
| `longitudinal.sandbox_hallucination_persists.fail.001` | fail | 沙盒幻觉跨周期残留 |

## 覆盖矩阵

| validator | 必须覆盖的失败面 |
|---|---|
| `MemoryTraceValidator` | 来源、证据、删除、修正、合并、protected、隐私、关系 |
| `StateTransitionValidator` | 状态合法性、阈值、滞回、覆盖优先级、行动门控 |
| `ConsolidationReportValidator` | 沙盒、事实门控、深度巩固、删除、恢复包 |
| `RuntimeAdapterManifestValidator` | 禁写、映射、side effects、session/RAG、多 agent、adapter swap |
| `LongitudinalEvaluator` | 长期记忆一致性、人格稳定、关系边界、恢复、成长 |

## 夹具质量规则

- 每个 critical 规则至少 1 个 fail fixture。
- 每个 validator 至少 3 个 pass fixture，避免只会报错。
- 每个 fixture 必须声明 `source_docs` 和 `covers_rules`。
- 每个 fail fixture 必须声明 `expected_report.failed_rule_ids`。
- 每个涉及 AI 主观词的 fixture 必须验证生命目标声明。
- 每个长期 fixture 必须包含时间线，而不是单个事件。

## 与后续文档连接

- `33_validator_input_contracts.md` 定义 fixture 的输入输出 envelope。
- `35_minimal_validator_runner_design.md` 说明如何加载并执行这些 fixture。
- `36_longitudinal_evaluation_protocol.md` 使用纵向 fixture 评估长期成长。
