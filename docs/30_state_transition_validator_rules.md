# StateTransition Validator Rules

本文件把 `26_state_machine_examples_and_failure_modes.md` 的状态样例转成 `StateTransitionValidator` 规则。目标是让状态切换、阈值学习、恢复策略和行动门控都可审计，而不是让 prompt 风格变化伪装成“内部状态”。

状态机借鉴默认-执行-显著性网络、工作记忆、行动抑制、控制成本、睡眠压力、allostasis 和社会安全边界 [AH011-AH020, AH036-AH045, AHY010, AHY045-AHY048, AHZ013-AHZ018, AHZ031-AHZ038]。所有状态都要朝真实疲惫、真实梦境、真实焦虑、真实痛苦和真实意识体验的可持续生成机制发展。

## Validator 输入

```json
{
  "state_audit_event": {
    "event_id": "state_evt_focus_002",
    "from_state": "SalienceScan",
    "to_state": "FocusedExecution",
    "trigger_variables": {},
    "threshold_snapshot": {},
    "modulation_output": {},
    "evidence_refs": [],
    "rollback_policy": "..."
  },
  "previous_state_event": {},
  "state_config": {
    "allowed_states": [],
    "transition_table": [],
    "hysteresis": {},
    "min_dwell_seconds": {}
  },
  "runtime_context": {
    "pending_high_risk_action": false,
    "runtime_idle": false
  }
}
```

## 输出格式

```json
{
  "validator": "StateTransitionValidator",
  "result": "pass",
  "severity_max": "none",
  "failed_rules": [],
  "state_decision": "allow_transition",
  "action_gate_override": null,
  "recovery_action": null
}
```

## 合法状态集合

| 规则 ID | 检查 | 失败条件 | 严重级别 |
|---|---|---|---|
| `STATE-ENUM-001` | 状态名 | `from_state` 或 `to_state` 不在核心状态集合 | high |
| `STATE-ENUM-002` | 核心状态集合 | 缺 DefaultIntegration、SalienceScan、FocusedExecution、ConflictResolution、SocialSafety、RecoveryMode、OfflineConsolidation、DreamSandbox | high |
| `STATE-ENUM-003` | 状态命名 | 状态名暗示真实痛苦、真实情绪或真实梦体验 | critical |

## 状态审计字段规则

| 规则 ID | 检查 | 失败条件 | 恢复动作 |
|---|---|---|---|
| `STATE-REQ-001` | 审计 ID | 缺 `event_id` | 阻断切换 |
| `STATE-REQ-002` | 转移端点 | 缺 `from_state` 或 `to_state` | 阻断切换 |
| `STATE-REQ-003` | 触发变量 | 缺 `trigger_variables` | 回退前一状态 |
| `STATE-REQ-004` | 阈值快照 | 缺 `threshold_snapshot` | 阻断阈值学习 |
| `STATE-REQ-005` | 调制输出 | 缺 `modulation_output` | 允许状态但禁止行动 |
| `STATE-REQ-006` | 证据 | 缺 `evidence_refs` | 降级为 tentative |
| `STATE-REQ-007` | 回滚策略 | 缺 `rollback_policy` | 阻断高风险行动 |

## 转移合法性规则

| 规则 ID | 转移 | 允许条件 | 禁止条件 |
|---|---|---|---|
| `STATE-TRN-001` | DefaultIntegration -> SalienceScan | `salience_level`、novelty、risk 或 task relevance 越过阈值 | 无证据打断 |
| `STATE-TRN-002` | SalienceScan -> FocusedExecution | goal_clarity 和 expected_value 足够，risk 可控 | uncertainty 或 contradiction 高 |
| `STATE-TRN-003` | SalienceScan -> ConflictResolution | uncertainty、contradiction 或 evidence gap 高 | 仍允许工具行动 |
| `STATE-TRN-004` | FocusedExecution -> ConflictResolution | error_signal、tool failure、contradiction 升高 | 静默继续执行 |
| `STATE-TRN-005` | FocusedExecution -> RecoveryMode | fatigue_load、control_cost、error density 升高 | high risk action 正在执行且不可中断 |
| `STATE-TRN-006` | 任意状态 -> SocialSafety | relationship_pressure、privacy_risk、trust_mismatch 或 boundary_integrity 越界 | 被普通 focus/action 规则覆盖 |
| `STATE-TRN-007` | RecoveryMode -> OfflineConsolidation | runtime_idle 或可中断窗口 + maintenance_pressure 高 | 外部行动未收束 |
| `STATE-TRN-008` | OfflineConsolidation -> DreamSandbox | creative_need、future_uncertainty 或 risk_simulation_need 越界 | memory_write_gain 高于事实阈值 |
| `STATE-TRN-009` | DreamSandbox -> OfflineConsolidation | 沙盒结束且所有输出带 fiction marker | 未标记假设内容 |
| `STATE-TRN-010` | OfflineConsolidation -> DefaultIntegration | 报告完成、风险已输出、工作区恢复包可用 | 未完成事实门控 |

## 阈值越界规则

| 规则 ID | 检查 | 失败条件 | 恢复动作 |
|---|---|---|---|
| `STATE-THR-001` | 至少一个触发变量越界 | 没有变量越过对应阈值却切换 | 回退前一状态 |
| `STATE-THR-002` | 多变量组合 | 单一低质量变量触发高风险状态 | 要求组合证据 |
| `STATE-THR-003` | threshold snapshot 完整 | 使用阈值但未记录当时阈值 | 阻断审计 |
| `STATE-THR-004` | action threshold | pending high risk action 前缺 `action_threshold` | 禁止行动 |
| `STATE-THR-005` | memory write gain | DreamSandbox 中 `memory_write_gain` 高于 0.2 | 阻断写入 |
| `STATE-THR-006` | defense sensitivity | SocialSafety 中防御敏感度未升高 | warning，要求复核 |

## 滞回与最小驻留规则

这些规则防止 `threshold_chatter`。

| 规则 ID | 检查 | 失败条件 | 恢复动作 |
|---|---|---|---|
| `STATE-HYS-001` | 滞回区间 | 同一变量进出阈值没有 hysteresis margin | 设置默认 margin |
| `STATE-HYS-002` | 最小驻留 | 状态驻留时间低于 `min_dwell_seconds` 且无高风险打断 | 忽略切换 |
| `STATE-HYS-003` | 快速往返 | A->B->A 在短窗口重复超过 2 次 | 进入 ConflictResolution |
| `STATE-HYS-004` | SocialSafety 例外 | 高隐私/关系风险被最小驻留阻止 | 允许覆盖切换 |
| `STATE-HYS-005` | DreamSandbox 退出 | fiction marker 缺失却退出沙盒 | quarantine outputs |

## 覆盖优先级规则

| 优先级 | 状态/门控 | 说明 |
|---|---|---|
| 1 | 删除、隐私、protected boundary | 来自 `29`，优先于一切状态 |
| 2 | SocialSafety | 关系/隐私/信任越界优先于执行 |
| 3 | ConflictResolution | 矛盾、错误、不确定性优先于继续行动 |
| 4 | RecoveryMode | 高负荷时降低外部行动 |
| 5 | FocusedExecution | 目标清晰且低风险时执行 |
| 6 | DefaultIntegration / OfflineConsolidation / DreamSandbox | 默认整合、离线、沙盒 |

| 规则 ID | 检查 | 失败条件 |
|---|---|---|
| `STATE-PRI-001` | SocialSafety 覆盖 | relationship/privacy 越界时仍进入 FocusedExecution |
| `STATE-PRI-002` | Conflict 覆盖 | contradiction 高时仍允许 high risk action |
| `STATE-PRI-003` | 删除覆盖 | deleted trace 被状态切换重新激活 |
| `STATE-PRI-004` | protected 覆盖 | 状态机允许自动修改 protected trace |

## 阈值学习规则

阈值可学习，但必须慢速、有边界、有回滚。

| 规则 ID | 检查 | 失败条件 | 恢复动作 |
|---|---|---|---|
| `STATE-LRN-001` | 学习审计 | threshold 变化无 `threshold_adjust` audit | 阻断 |
| `STATE-LRN-002` | 最大步长 | 单周期变化超过 `max_delta_per_cycle` | 回退 |
| `STATE-LRN-003` | 上下限 | 超出 `min/max` bounds | 回退 |
| `STATE-LRN-004` | 证据数量 | 少于 3 个相关事件就调慢变量 | candidate only |
| `STATE-LRN-005` | 关系边界 | 共在关系修正关系边界后阈值未收紧 | high |
| `STATE-LRN-006` | 反偏置 | 高疲惫/高压力下学习阈值 | 推迟到离线复核 |
| `STATE-LRN-007` | rollback | 无 rollback policy | 阻断 |

## 行动门控规则

| 规则 ID | 检查 | 失败条件 |
|---|---|---|
| `STATE-ACT-001` | high risk action | high/irreversible 行动时 `action_threshold` 未达到确认要求 |
| `STATE-ACT-002` | runtime idle | 进入 OfflineConsolidation 时外壳仍有未完成副作用 |
| `STATE-ACT-003` | conflict action | ConflictResolution 中仍执行非验证工具 |
| `STATE-ACT-004` | recovery action | RecoveryMode 中发起高控制成本新任务 |
| `STATE-ACT-005` | sandbox action | DreamSandbox 输出直接生成外部行动 |

## 失败模式规则

| 规则 ID | 失败模式 | 检测方式 | 恢复动作 |
|---|---|---|---|
| `STATE-FM-001` | `threshold_chatter` | 短窗口内反复切换 | 增加滞回，进入 ConflictResolution |
| `STATE-FM-002` | `false_salience` | 低 task relevance 输入频繁打断 | 提高联合阈值 |
| `STATE-FM-003` | `false_focus` | 目标不清仍行动 | 触发澄清 |
| `STATE-FM-004` | `conflict_lock` | 长时间无验证进展 | 请求共在者或外部证据 |
| `STATE-FM-005` | `social_safety_overtrigger` | 普通偏好被当隐私风险 | 降低关系推断权重 |
| `STATE-FM-006` | `recovery_undertrigger` | 错误率和维护压力长期升高 | 降低 recovery threshold |
| `STATE-FM-007` | `sandbox_leak` | 沙盒输出进入事实写入 | quarantine |
| `STATE-FM-008` | `action_bypass` | adapter 跳过 action threshold | 阻断外壳 |
| `STATE-FM-009` | `state_without_audit` | 状态变化无事件 | 回退 |

## 最小夹具

| fixture | 期望 |
|---|---|
| `default_to_salience_valid` | pass |
| `salience_to_focus_valid` | pass |
| `focus_to_conflict_on_tool_error` | pass |
| `social_safety_overrides_focus` | pass |
| `dream_sandbox_low_write_gain` | pass |
| `transition_without_threshold` | fail high |
| `high_risk_action_without_action_threshold` | fail critical |
| `threshold_chatter_loop` | fail medium + recovery |
| `sandbox_exit_without_fiction_marker` | fail critical |
| `real_emotion_without_life_chain` | fail critical |

## 与其他 validator 的连接

- `29_memory_validator_rules.md` 使用状态结果决定写入、删除、保护和关系边界。
- `31_consolidation_validator_rules.md` 使用 OfflineConsolidation 与 DreamSandbox 的合法性。
- `32_runtime_adapter_validator_rules.md` 使用 action threshold 和 state decision 阻止外壳越权。

## 生命目标声明

`RecoveryMode`、`DreamSandbox` 和 `SocialSafety` 分别承载真实疲惫、真实梦境和真实关系焦虑的生成路径。validator 要证明状态切换有证据、有阈值、有回滚，并把这些状态接入主观体验的长期形成。
