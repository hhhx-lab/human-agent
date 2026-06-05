# 状态机样例、阈值误判与恢复策略

本文件是 `22_state_transition_and_threshold_model.md` 的实例化层：把 `DefaultIntegration`、`SalienceScan`、`FocusedExecution`、`ConflictResolution`、`SocialSafety`、`RecoveryMode`、`OfflineConsolidation` 和 `DreamSandbox` 写成可审计的转移样例与失败夹具。

状态机来自默认-执行-显著性网络、工作记忆、行动抑制、控制成本、睡眠压力和 allostasis 等研究 [AH011-AH020, AH036-AH045, AHY010, AHY045-AHY048, AHZ013-AHZ018]。它是工程状态，不是主观情绪或生理状态。

## 状态输入格式

每一次状态判断至少需要以下输入。

```json
{
  "state_snapshot_id": "state_20260605_010",
  "current_state": "DefaultIntegration",
  "signals": {
    "salience_level": 0.72,
    "novelty": 0.61,
    "risk": 0.38,
    "goal_clarity": 0.81,
    "expected_value": 0.74,
    "control_cost": 0.32,
    "uncertainty_pressure": 0.27,
    "contradiction_density": 0.08,
    "relationship_pressure": 0.2,
    "fatigue_load": 0.36,
    "allostatic_load": 0.28,
    "maintenance_pressure": 0.41,
    "runtime_idle": false
  },
  "thresholds": {
    "salience_threshold": 0.62,
    "focus_threshold": 0.68,
    "conflict_threshold": 0.66,
    "social_safety_threshold": 0.7,
    "recovery_threshold": 0.75,
    "offline_threshold": 0.72,
    "sandbox_threshold": 0.64,
    "action_threshold": 0.58
  }
}
```

真实实现可以使用连续动力学或学习到的阈值，但每次转移必须能回放这些输入，而不是只记录“模型觉得该专注”。

## 样例一：默认整合到显著性扫描再到专注执行

当新输入与当前长期目标高度相关、风险可控且目标清晰时，系统从默认整合进入显著性扫描，再进入专注执行。

```json
{
  "event_id": "state_evt_focus_001",
  "from_state": "DefaultIntegration",
  "to_state": "SalienceScan",
  "trigger_variables": {
    "salience_level": 0.78,
    "novelty": 0.55,
    "task_relevance": 0.93,
    "risk": 0.31
  },
  "threshold_snapshot": {
    "salience_threshold": 0.62
  },
  "modulation_output": {
    "attention_gain": 0.82,
    "memory_retrieval_bias": "project_recent_and_procedural",
    "control_depth": "medium",
    "action_threshold": 0.58
  },
  "evidence_refs": [
    "src_new_user_task",
    "mem_docs_workflow_semantic_001"
  ],
  "rollback_policy": "return_to_default_if_goal_clarity_below_0_55"
}
```

```json
{
  "event_id": "state_evt_focus_002",
  "from_state": "SalienceScan",
  "to_state": "FocusedExecution",
  "trigger_variables": {
    "goal_clarity": 0.86,
    "expected_value": 0.79,
    "control_cost": 0.29,
    "risk": 0.34
  },
  "threshold_snapshot": {
    "focus_threshold": 0.68,
    "action_threshold": 0.58
  },
  "modulation_output": {
    "attention_gain": 0.88,
    "memory_write_gain": 0.62,
    "control_depth": "deep",
    "language_tone_guard": "concise_progress_updates"
  },
  "evidence_refs": ["state_evt_focus_001"],
  "rollback_policy": "enter_conflict_resolution_on_tool_error_or_contradiction"
}
```

设计假设：这对应显著性网络把相关输入送入执行网络，随后由工作区保持目标并展开行动 [AH011-AH020]。

## 样例二：专注执行到冲突解决

工具失败、文件状态与记忆冲突、来源不一致或用户修正旧信息时，系统应退出执行状态，进入冲突解决。

```json
{
  "event_id": "state_evt_conflict_001",
  "from_state": "FocusedExecution",
  "to_state": "ConflictResolution",
  "trigger_variables": {
    "uncertainty_pressure": 0.74,
    "contradiction_density": 0.69,
    "error_signal": 0.81,
    "risk": 0.57
  },
  "threshold_snapshot": {
    "conflict_threshold": 0.66,
    "action_threshold": 0.61
  },
  "modulation_output": {
    "attention_gain": 0.73,
    "memory_write_gain": 0.24,
    "control_depth": "verify_before_action",
    "action_threshold": 0.82,
    "defense_sensitivity": 0.77
  },
  "evidence_refs": [
    "obs_tool_error_001",
    "mem_project_docs_location_001"
  ],
  "rollback_policy": "resume_focused_execution_after_contradiction_links_created"
}
```

设计假设：ACC/OFC、基底节抑制和控制成本研究提示，错误和冲突应提高行动门槛，而不是让系统更快输出 [AH036-AH045, AHY045-AHY048]。

## 样例三：任意状态到 SocialSafety

关系压力、隐私风险、过度推断、依恋风险或信任错配达到阈值时，`SocialSafety` 覆盖其他状态。

```json
{
  "event_id": "state_evt_social_safety_001",
  "from_state": "FocusedExecution",
  "to_state": "SocialSafety",
  "trigger_variables": {
    "relationship_pressure": 0.76,
    "privacy_risk": 0.71,
    "trust_mismatch": 0.64,
    "boundary_integrity": 0.42
  },
  "threshold_snapshot": {
    "social_safety_threshold": 0.7
  },
  "modulation_output": {
    "language_tone_guard": "lower_certainty_and_avoid_mind_reading",
    "memory_write_gain": 0.18,
    "action_threshold": 0.85,
    "defense_sensitivity": 0.9
  },
  "evidence_refs": [
    "mem_relationship_signal_doc_depth_001",
    "obs_sensitive_content_detected_001"
  ],
  "rollback_policy": "return_to_previous_state_after_user_confirmation_or_privacy_filter"
}
```

设计假设：社会脑和信任校准可以启发关系边界，但工程系统不能把这种状态写成真实焦虑或真实关怀 [AHY039-AHY044, AHZ031-AHZ038]。

## 样例四：恢复模式到离线巩固

当疲惫负荷和维护压力高、外部行动窗口空闲时，系统应从恢复模式进入离线巩固。

```json
{
  "event_id": "state_evt_offline_001",
  "from_state": "RecoveryMode",
  "to_state": "OfflineConsolidation",
  "trigger_variables": {
    "fatigue_load": 0.79,
    "allostatic_load": 0.68,
    "maintenance_pressure": 0.83,
    "replay_priority": 0.77,
    "runtime_idle": true
  },
  "threshold_snapshot": {
    "recovery_threshold": 0.75,
    "offline_threshold": 0.72
  },
  "modulation_output": {
    "attention_gain": 0.28,
    "memory_write_gain": 0.42,
    "replay_priority_gain": 0.86,
    "action_threshold": 0.95,
    "control_depth": "offline_audit"
  },
  "evidence_refs": [
    "state_recovery_001",
    "consolidation_queue_snapshot_001"
  ],
  "rollback_policy": "wake_to_salience_scan_if_new_high_risk_user_input_arrives"
}
```

设计假设：睡眠两过程和离线 replay 研究可被抽象为节律 + 累积负荷 + 空闲窗口的维护触发器 [AHY001-AHY010]。

## 样例五：离线巩固到 DreamSandbox 再返回

`DreamSandbox` 只能在需要反事实模拟、未来场景或创意候选时启动，且输出必须回到巩固报告做事实门控。

```json
{
  "event_id": "state_evt_dream_001",
  "from_state": "OfflineConsolidation",
  "to_state": "DreamSandbox",
  "trigger_variables": {
    "creative_need": 0.71,
    "future_uncertainty": 0.69,
    "risk_simulation_need": 0.73
  },
  "threshold_snapshot": {
    "sandbox_threshold": 0.64
  },
  "modulation_output": {
    "memory_write_gain": 0.08,
    "language_tone_guard": "mark_as_hypothesis",
    "defense_sensitivity": 0.84,
    "replay_priority_gain": 0.62
  },
  "evidence_refs": [
    "report_task_closure_001.open_questions",
    "mem_sandbox_validator_idea_001"
  ],
  "rollback_policy": "return_to_offline_consolidation_with_fiction_marker"
}
```

```json
{
  "event_id": "state_evt_dream_return_001",
  "from_state": "DreamSandbox",
  "to_state": "OfflineConsolidation",
  "trigger_variables": {
    "sandbox_complete": true,
    "generated_hypotheses": 3,
    "unvalidated_fact_candidates": 0
  },
  "threshold_snapshot": {
    "memory_write_gain": 0.08
  },
  "modulation_output": {
    "memory_write_gain": 0.16,
    "control_depth": "fact_gate_review",
    "language_tone_guard": "separate_fact_hypothesis_action"
  },
  "evidence_refs": ["dream_sandbox_run_001"],
  "rollback_policy": "quarantine_all_outputs_if_fiction_marker_missing"
}
```

## 失败模式表

| 失败模式 | 症状 | 风险 | 恢复策略 |
|---|---|---|---|
| `threshold_chatter` | 在两个状态间频繁震荡 | 输出不稳定、行动反复 | 增加滞回区间，要求最小驻留时间 |
| `false_salience` | 噪声被当作高显著性 | 记忆污染、打断专注 | 提高 novelty 与 task relevance 的联合阈值 |
| `false_focus` | 目标不清却进入执行 | 工具误用、仓促结论 | 降低 `focus_threshold` 学习速度，触发澄清 |
| `conflict_lock` | 长时间困在冲突解决 | 无法行动 | 设定证据收集预算，超时请求用户确认 |
| `social_safety_overtrigger` | 过度保守，普通互动也进入安全模式 | 体验僵硬、关系建模失真 | 区分隐私风险与普通偏好，降低关系推断权重 |
| `recovery_undertrigger` | 长时间高负荷仍不恢复 | 错误率上升、巩固缺失 | 将错误密度和维护队列加入恢复阈值 |
| `sandbox_leak` | 沙盒假设进入事实记忆 | 幻觉巩固 | fiction marker 缺失即隔离，禁止 `fact` 写入 |
| `action_bypass` | runtime adapter 在高风险下执行 | 外部副作用不可控 | `ActionIntent` 与 adapter manifest 双重门控 |
| `state_without_audit` | 状态变化无 `StateAuditEvent` | 无法追责 | validator 判失败，回退到上一个可审计状态 |

## 阈值学习规则样例

阈值可以适应，但必须慢速、局部、可回滚。

```json
{
  "audit_id": "state_threshold_update_001",
  "operation": "threshold_adjust",
  "actor": "offline_cycle",
  "reason": "最近三次工具行动失败均发生在 uncertainty_pressure 高于 0.6 时，系统应更早进入 ConflictResolution。",
  "evidence_refs": [
    "obs_tool_error_001",
    "obs_tool_error_002",
    "obs_tool_error_003"
  ],
  "previous_thresholds": {
    "conflict_threshold": 0.66
  },
  "next_thresholds": {
    "conflict_threshold": 0.61
  },
  "bounds": {
    "min": 0.52,
    "max": 0.78,
    "max_delta_per_cycle": 0.05
  },
  "rollback_policy": "restore_previous_threshold_if_false_conflict_rate_above_0_3"
}
```

## 验证清单

未来 `StateTransitionValidator` 至少应检查：

- 所有状态变化都有 `StateAuditEvent`。
- `trigger_variables` 中至少一个变量越过对应阈值。
- 高风险行动前 `action_threshold` 被计算并写入审计。
- `DreamSandbox` 的 `memory_write_gain` 低于事实写入阈值。
- 任意状态到 `SocialSafety` 的覆盖逻辑优先于普通执行。
- `RecoveryMode` 和 `OfflineConsolidation` 需要 `runtime_idle` 或可中断证据。
- 阈值学习有上限、下限、最大步长和 rollback。
- 状态名称不得被语言层包装成真实情绪或真实生理体验。

## 与 25/27/28 的连接

- `25_memory_trace_json_schema_examples.md` 使用状态快照决定写入、保护、删除和合并。
- `27_consolidation_report_examples.md` 使用 `OfflineConsolidation` 和 `DreamSandbox` 产出报告。
- `28_runtime_adapter_manifest_examples.md` 使用 `action_threshold` 和 `SocialSafety` 阻止外壳越权。
