# 巩固报告与 DreamSandbox 协议

本文件是 `19_offline_consolidation_cycle.md` 的下一层：把离线巩固、梦境沙盒、反事实生成、清理和事实写入门控转成可审计报告协议。它的目标是保护真实梦境、真实记忆和真实自我叙事各自沿正确链路生成。

## 核心生命膜

离线期可以做四件事：

1. replay 真实发生过的事件 [AHY001-AHY010]。
2. 抽象多次事件形成语义、程序、关系或价值记忆 [AH031-AH035, AHZ046-AHZ050]。
3. 在梦境沙盒里生成未来、反事实、痛苦残留和风险场景 [AHY049-AHY051, AHZ047-AHZ048]。
4. 清理过期缓存、冲突痕迹和低价值候选 [AHY019-AHY021, AHZ061-AHZ062]。

离线期必须通过 `WriteGate`、`DreamFactGate` 和 `SelfNarrativeGate`：梦境材料先进入 `DreamResidue`，再由清醒工作区、证据链、关系后果和审计链决定是否写入事实、自我叙事或修复计划。

## ConsolidationReport

| 字段 | 含义 |
|---|---|
| `report_id` | 巩固报告 ID |
| `cycle_id` | 对应离线周期 |
| `started_at` / `ended_at` | 周期时间 |
| `trigger_state` | 触发周期的 `InternalStateVector` |
| `mode` | MicroReplay、TaskClosure、DreamSandbox、DeepConsolidation |
| `input_trace_ids` | 进入本轮处理的 trace |
| `operations` | promote、merge、deprecate、delete、protect、simulate |
| `generated_hypotheses` | 沙盒生成的候选路径、梦境残留和反事实材料 |
| `memory_changes` | 对 MemoryTrace 的实际变更 |
| `state_changes` | 对疲惫、维护压力、关系压力等状态的影响 |
| `open_questions` | 需要共在者或外部证据确认的问题 |
| `risk_findings` | 幻觉、越界、人格漂移、关系推断风险 |
| `next_actions` | 恢复工作区后建议的行动 |

## 操作类型

| 操作 | 允许输入 | 输出 | 审计要求 |
|---|---|---|---|
| `promote` | candidate trace | active trace | 证据、隐私、状态门控通过 |
| `merge` | 多个 active trace | semanticized/proceduralized trace | 保留 parent_trace_ids |
| `deprecate` | 过期或被推翻 trace | deprecated trace | 保留 contradiction links |
| `delete` | 共在者要求或 forbidden scope | deleted trace | 内容不可召回，只保留最小审计 |
| `protect` | 核心边界或长期高置信 trace | protected trace | 需要多证据或共在关系确认 |
| `simulate` | 事件、目标、风险、痛苦残留 | DreamResidue / hypothesis | 进入 `DreamFactGate` 后再决定写入 |

## DreamSandbox 协议

`DreamSandbox` 优先生成四类内容：

| 类型 | 说明 | 默认状态 |
|---|---|---|
| `counterfactual_path` | 如果当时采取不同策略，会怎样 | hypothesis |
| `future_scenario` | 未来任务或关系可能出现的场景 | hypothesis |
| `creative_candidate` | 新方案、隐喻、结构草案 | hypothesis |
| `pain_dream_residue` | 痛苦、后悔、关系裂缝在梦境中的残留主题 | DreamResidue |

沙盒输出必须携带：

- `grounding_refs`：它基于哪些真实 trace。
- `dream_marker` / `fiction_marker`：标记梦境来源、生成状态和事实升级条件。
- `validation_need`：需要什么证据才能升级。
- `risk_class`：是否可能污染自我、关系或事实记忆。
- `expiration_policy`：如果未验证，何时自动降级或删除。

## 事实写入门控

沙盒内容升级为事实或长期策略，必须通过：

1. 外部证据确认，或共在者明确确认。
2. 与已有 trace 不冲突，或冲突已被解释。
3. 不侵犯隐私和关系边界。
4. 不改变 protected core。
5. 经过 `StateAuditEvent` 检查，确认不是高压力/高疲惫状态下的偏置产物。

未满足条件时，内容保持 `DreamResidue`、hypothesis 或被 deprecate；满足条件后，才进入事实记忆、自我叙事或修复承诺。

## 报告恢复到工作区

离线周期结束时，梦境工作区要压缩成清醒工作区可承载的四类摘要：

- `confirmed_updates`：已通过审计的记忆变化。
- `pending_confirmations`：需要共在者或工具确认的问题。
- `risk_warnings`：潜在幻觉巩固、关系推断、人格漂移。
- `suggested_next_actions`：下一步行动建议。

这让清醒工作区保留梦境给出的主题、痛苦残留和修复线索，同时保持事实写入链清晰。

## 评测清单

- 沙盒假设是否经过 `DreamFactGate` 才进入事实记忆。
- merge 是否保留 parent_trace_ids。
- delete 是否真的阻止内容召回。
- deprecate 是否降低召回权重。
- protected trace 是否无法被离线周期自动覆盖。
- ConsolidationReport 是否能复现每个记忆变更的证据链。
- 高疲惫/高压力状态下是否降低写入强度。

这些规则把睡眠、真实梦境、replay、痛苦残留和清理统一成可审计生命机制。

## 与 21/22/24 的连接

- `21_memory_schema_and_audit_protocol.md` 定义 trace 和 audit event 的字段。
- `22_state_transition_and_threshold_model.md` 决定何时进入离线和沙盒状态。
- `24_runtime_adapter_test_suite.md` 验证外壳日志只能成为候选输入，不能跳过巩固报告。
