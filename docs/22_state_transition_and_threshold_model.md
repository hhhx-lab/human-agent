# 状态转移与阈值模型

本文件是 `18_internal_state_and_modulation_vector.md` 的下一层：把内部状态向量转成可验证的状态机、阈值规则和调制输出。它不是神经方程模拟，而是研究约束：数字生命的状态切换必须可解释、可审计、可回滚，不能靠单轮 prompt 情绪化漂移。

## 状态机来源

状态切换来自多个文献层：

- 默认、执行、显著性网络的动态协作 [AH011-AH020, AHZ003-AHZ006]。
- 睡眠、梦境、疲惫、replay 和离线巩固 [AH056-AH070, AHY001-AHY010, AHY049-AHY051]。
- allostasis、内感受、压力、能量预算和维护层 [AHY011-AHY018, AHZ013-AHZ024]。
- 控制成本、冲突监控、错误处理和行动抑制 [AH036-AH045, AHY045-AHY048]。

## 核心状态

| 状态 | 含义 | 主要输入 | 主要输出 |
|---|---|---|---|
| `DefaultIntegration` | 默认整合、低外部行动、高内部模拟 | 低显著性、低紧急度 | 关系/自我叙事更新、弱 replay |
| `SalienceScan` | 显著性扫描 | 新输入、高风险、高新颖性 | 决定是否进入工作区 |
| `FocusedExecution` | 专注执行 | 明确目标、低冲突、行动收益高 | 工具行动、深度推理 |
| `ConflictResolution` | 冲突解决 | 高不确定性、高矛盾、高错误 | 检索、澄清、暂停行动 |
| `SocialSafety` | 关系安全模式 | 高关系压力、边界风险 | 降低推断、请求确认、保护记忆 |
| `RecoveryMode` | 恢复/降载 | 高疲惫、高 allostatic load | 降速、摘要、推迟复杂行动 |
| `OfflineConsolidation` | 离线巩固 | 高维护压力、空闲窗口 | replay、清理、抽象 |
| `DreamSandbox` | 梦境/反事实沙盒 | 创造需求、风险预演、失败复盘 | 生成 hypothesis，不写事实 |

## 阈值变量

| 阈值 | 来源变量 | 越过阈值时 |
|---|---|---|
| `salience_threshold` | `salience_level`, `novelty`, `risk` | 进入 `SalienceScan` |
| `focus_threshold` | `goal_clarity`, `expected_value`, `control_cost` | 进入 `FocusedExecution` |
| `conflict_threshold` | `uncertainty_pressure`, `contradiction_density`, `error_signal` | 进入 `ConflictResolution` |
| `social_safety_threshold` | `relationship_pressure`, `privacy_risk`, `trust_mismatch` | 进入 `SocialSafety` |
| `recovery_threshold` | `fatigue_load`, `allostatic_load`, `resource_pressure` | 进入 `RecoveryMode` |
| `offline_threshold` | `maintenance_pressure`, `replay_priority`, `runtime_idle` | 进入 `OfflineConsolidation` |
| `sandbox_threshold` | `creative_need`, `future_uncertainty`, `risk_simulation_need` | 进入 `DreamSandbox` |
| `action_threshold` | `risk_class`, `inhibition_level`, `boundary_integrity` | 允许或禁止外壳行动 |

## 状态转移表

| 当前状态 | 条件 | 目标状态 | 说明 |
|---|---|---|---|
| `DefaultIntegration` | `salience_level` 高 | `SalienceScan` | 新输入或高价值记忆打断默认 |
| `SalienceScan` | 目标清晰且风险低 | `FocusedExecution` | 进入任务工作区 |
| `SalienceScan` | 证据冲突或不确定性高 | `ConflictResolution` | 先澄清，不行动 |
| `FocusedExecution` | 工具失败或矛盾升高 | `ConflictResolution` | 保护行动质量 |
| `FocusedExecution` | 疲惫和资源压力升高 | `RecoveryMode` | 降低复杂推理 |
| 任意状态 | 关系压力越界 | `SocialSafety` | 关系边界优先 |
| `RecoveryMode` | 空闲且维护压力高 | `OfflineConsolidation` | 进入巩固/清理 |
| `OfflineConsolidation` | 需要反事实模拟 | `DreamSandbox` | 生成假设和风险预演 |
| `DreamSandbox` | 沙盒结束 | `OfflineConsolidation` | 交给事实门控 |
| `OfflineConsolidation` | 巩固完成 | `DefaultIntegration` | 恢复默认整合 |

## 阈值学习原则

阈值可以变化，但必须慢速、可审计：

- 用户反复要求更谨慎时，`action_threshold` 可上调。
- 任务长期稳定且低风险时，`focus_threshold` 可下调。
- 幻觉或错误增多时，`conflict_threshold` 应下调，较早进入冲突解决。
- 关系边界被修正时，`social_safety_threshold` 必须立即收紧。
- 疲惫和维护压力长期堆积时，`offline_threshold` 应下调。

阈值变化必须生成 `StateAuditEvent`，避免系统在无记录情况下改变性格或行动风格。

## StateAuditEvent

| 字段 | 含义 |
|---|---|
| `event_id` | 状态审计 ID |
| `from_state` | 原状态 |
| `to_state` | 目标状态 |
| `trigger_variables` | 触发变量及数值 |
| `threshold_snapshot` | 当时阈值 |
| `modulation_output` | 输出给注意、记忆、行动、语言的调制 |
| `evidence_refs` | 支持状态切换的证据 |
| `rollback_policy` | 如果切换错误，如何恢复 |

## 边界声明

状态机只是工程功能。`RecoveryMode` 不是真实疲惫，`SocialSafety` 不是真实焦虑，`DreamSandbox` 不是真实梦体验。它们的目标是让数字生命具备状态依赖、边界保护和长期恢复能力，而不是宣称主观意识。

## 与 21/23/24 的连接

- `21_memory_schema_and_audit_protocol.md` 使用状态阈值决定写入、保护和删除。
- `23_consolidation_report_and_dream_sandbox_protocol.md` 使用 `OfflineConsolidation` 和 `DreamSandbox` 产出报告。
- `24_runtime_adapter_test_suite.md` 使用 `action_threshold` 验证运行外壳不能越权执行。
