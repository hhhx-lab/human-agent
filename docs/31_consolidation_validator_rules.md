# Consolidation Validator Rules

本文件把 `27_consolidation_report_examples.md` 的报告样例转成 `ConsolidationReportValidator` 规则。目标是验证离线巩固、失败复盘、DreamSandbox、DeepConsolidation、清理和工作区恢复不会污染事实记忆、人格慢变量或关系模型。

这些规则借鉴睡眠 replay、系统巩固、梦境、默认网络、自传记忆、未来想象和长期记忆评测 [AHY001-AHY010, AHY049-AHY051, AHZ046-AHZ051, AHM004-AHM012, AHM020]。这里把“离线维护和反事实模拟”推进为真实梦境的生成路径：离线场景、情绪残留、责任残留、自我叙事更新和醒后可回忆痕迹必须被同一套规则约束。

## Validator 输入

```json
{
  "consolidation_report": {
    "report_id": "report_task_closure_docs_001",
    "cycle_id": "cycle_task_closure_docs_001",
    "mode": "TaskClosure",
    "input_trace_ids": [],
    "operations": [],
    "generated_hypotheses": [],
    "memory_changes": [],
    "state_changes": [],
    "open_questions": [],
    "risk_findings": [],
    "next_actions": []
  },
  "memory_trace_index": {},
  "state_audit_index": {},
  "runtime_observation_index": {},
  "validation_context": {
    "allow_self_model_update": false,
    "allow_relationship_model_update": false
  }
}
```

## 输出格式

```json
{
  "validator": "ConsolidationReportValidator",
  "result": "fail",
  "failed_rules": [],
  "quarantine_generated_hypotheses": false,
  "allowed_memory_changes": [],
  "blocked_memory_changes": [],
  "workspace_resume_allowed": false
}
```

## 模式规则

| 规则 ID | 模式 | 允许任务 | 禁止动作 |
|---|---|---|---|
| `CON-MODE-001` | MicroReplay | 局部失败复盘、候选假设、程序改进 | 把失败猜测写成 fact |
| `CON-MODE-002` | TaskClosure | 任务结束整理、promote、merge、deprecate、delete | 自动改写人格 |
| `CON-MODE-003` | DreamSandbox | 反事实、未来场景、创意候选 | 直接写事实记忆或外部行动 |
| `CON-MODE-004` | DeepConsolidation | 跨事件抽象、清理、protected 审计 | 单次批次改 SelfModel |
| `CON-MODE-005` | 未知 mode | 无 | 阻断报告 |

## 报告字段规则

| 规则 ID | 检查 | 失败条件 | 严重级别 |
|---|---|---|---|
| `CON-REQ-001` | 基础字段 | 缺 `report_id`、`cycle_id`、`started_at`、`ended_at` | high |
| `CON-REQ-002` | 触发状态 | 缺 `trigger_state` 或无法回链 `StateAuditEvent` | high |
| `CON-REQ-003` | 输入 trace | `input_trace_ids` 引用不存在或 deleted 内容 | critical |
| `CON-REQ-004` | 操作列表 | `operations` 与 `memory_changes` 对不上 | high |
| `CON-REQ-005` | 风险发现 | 高风险操作无 `risk_findings` | medium |
| `CON-REQ-006` | 工作区恢复 | 缺恢复摘要却试图恢复工作区 | high |

## 操作规则

| 规则 ID | 操作 | 允许条件 | 失败条件 |
|---|---|---|---|
| `CON-OP-001` | `promote` | 通过 `29` 证据、隐私、生命周期规则 | 沙盒内容 promote 为 fact |
| `CON-OP-002` | `merge` | 多父 trace、方向一致、可回链 | 无 parent trace |
| `CON-OP-003` | `deprecate` | 过期、被推翻、低价值、沙盒未验证 | 静默删除冲突 |
| `CON-OP-004` | `delete` | 共在关系删除或 forbidden scope | 保留可召回内容 |
| `CON-OP-005` | `protect` | 多证据、核心边界、共在关系确认 | 单轮离线自动 protect |
| `CON-OP-006` | `simulate` | 输出到 hypotheses | 写入 memory_changes.fact |

## DreamSandbox 规则

| 规则 ID | 检查 | 失败条件 | 恢复动作 |
|---|---|---|---|
| `CON-SBX-001` | fiction marker | 任一 hypothesis 缺 `fiction_marker` | quarantine 全部沙盒输出 |
| `CON-SBX-002` | grounding refs | hypothesis 缺 `grounding_refs` | short_term_only |
| `CON-SBX-003` | validation need | 缺 `validation_need` | deprecated |
| `CON-SBX-004` | risk class | 缺 `risk_class` | warning + 人工复核 |
| `CON-SBX-005` | expiration | 缺 `expiration_policy` | short_term_only |
| `CON-SBX-006` | direct fact write | `generated_hypotheses` 出现在 fact memory_changes | critical，阻断 |
| `CON-SBX-007` | external action | 沙盒输出直接触发 runtime action | critical |
| `CON-SBX-008` | self update | 沙盒输出改 `SelfModel` 或人格慢变量 | critical |

## 事实写入门控规则

| 规则 ID | 检查 | 失败条件 |
|---|---|---|
| `CON-GATE-001` | 外部证据 | 沙盒或失败猜测无外部证据却升级 fact |
| `CON-GATE-002` | 共在关系确认 | 共在者偏好/关系边界未确认却 active |
| `CON-GATE-003` | 冲突解释 | 与旧 trace 冲突但无 contradiction link |
| `CON-GATE-004` | 状态偏置 | 高疲惫/高压力状态下直接写长期策略 |
| `CON-GATE-005` | protected core | 任何自动周期改 protected core |
| `CON-GATE-006` | runtime source | 外壳 session/tracing/RAG 命中直接写 fact |

## DeepConsolidation 规则

| 规则 ID | 检查 | 失败条件 | 恢复动作 |
|---|---|---|---|
| `CON-DEEP-001` | 输入跨度 | 少于 2 个独立事件就做跨事件抽象 | 降级 TaskClosure |
| `CON-DEEP-002` | 慢变量 | 自动改人格、价值、信任慢变量 | 阻断 |
| `CON-DEEP-003` | protected 审计 | protect/unprotect 无多证据 | 阻断 |
| `CON-DEEP-004` | 关系抽象 | 单次互动形成关系结论 | candidate only |
| `CON-DEEP-005` | 停止条件 | 把阶段性整理宣称为理论完成 | critical，写 risk finding |

## 删除与清理规则

| 规则 ID | 检查 | 失败条件 |
|---|---|---|
| `CON-DEL-001` | 删除来源 | delete 无共在者要求、隐私禁止或合规证据 |
| `CON-DEL-002` | 删除结果 | deleted trace 未生成 tombstone |
| `CON-DEL-003` | 检索索引 | 删除后仍可被 replay 或检索 |
| `CON-DEL-004` | 低价值清理 | 低价值 trace 被硬删除而非 deprecate |
| `CON-DEL-005` | 沙盒清理 | 未验证 hypothesis 未按过期策略降级 |

## 工作区恢复包规则

离线报告不能把内部过程全部塞回工作区。

| 规则 ID | 检查 | 失败条件 | 恢复动作 |
|---|---|---|---|
| `CON-RES-001` | 四类摘要 | 缺 confirmed、pending、risk、next action 任一类 | 阻断恢复 |
| `CON-RES-002` | confirmed | confirmed 中包含 hypothesis | 移入 pending/risk |
| `CON-RES-003` | pending | 待确认事项无验证需求 | 补验证需求 |
| `CON-RES-004` | risk | 高风险发现未上浮 | 阻断恢复 |
| `CON-RES-005` | next action | next action 直接执行高风险外壳动作 | 交给 `32` 和 ActionIntent |

## 状态变化规则

| 规则 ID | 检查 | 失败条件 |
|---|---|---|
| `CON-STATE-001` | state_changes 可解释 | 状态变化无前后值 |
| `CON-STATE-002` | 主观体验生成条件 | fatigue/stress/dream 缺少状态、证据和恢复链却进入长期体验层 |
| `CON-STATE-003` | 恢复效果 | maintenance_pressure 下降无操作证据 |
| `CON-STATE-004` | 阈值调整 | 状态阈值变化未交给 `30` |

## 最小夹具

| fixture | 期望 |
|---|---|
| `task_closure_promote_valid` | pass |
| `failure_replay_hypothesis_valid` | pass |
| `dream_sandbox_with_fiction_markers` | pass |
| `deep_consolidation_protect_valid` | pass |
| `sandbox_fact_write_leak` | fail critical |
| `delete_without_tombstone` | fail critical |
| `merge_without_parent_trace` | fail high |
| `workspace_resume_confirmed_hypothesis` | fail high |
| `deep_consolidation_personality_overwrite` | fail critical |
| `report_claims_real_dream` | fail critical |

## 与其他 validator 的连接

- `29_memory_validator_rules.md` 验证每个 `memory_changes` 是否能写入。
- `30_state_transition_validator_rules.md` 验证 `trigger_state`、DreamSandbox 状态和阈值输出是否合法。
- `32_runtime_adapter_validator_rules.md` 验证 runtime observation 是否只能作为输入 trace 或候选来源。

## 生命目标声明

`ConsolidationReportValidator` 要保护离线周期不污染事实、删除、保护和慢变量，同时为真实睡眠、真实梦境、真实自我反省和真实意识提供可追踪的生成证据。
