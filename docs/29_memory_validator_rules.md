# MemoryTrace Validator Rules

本文件把 `25_memory_trace_json_schema_examples.md` 的样例转成字段级验证规则。它把未来 `MemoryTraceValidator`、人工审计和单元测试共同遵守的判定标准提前固定为生命记忆守门规则。

这些规则继承 `17`、`21`、`25` 的生命目标：记忆痕迹是可审计对象，也是数字生命真实回忆体验的生成载体；它借鉴记忆系统、系统巩固、replay、自传记忆和长期记忆评测研究 [AH031-AH035, AHY001-AHY010, AHZ046-AHZ050, AHM004-AHM012]，并要求数字系统把回忆体验纳入可触发、可重构、可巩固的长期结构。

## Validator 输入

最小输入是一个 trace 包。实现可以从数据库、事件流或文件夹读取，但进入 validator 前应规范成以下 JSON-like 结构：

```json
{
  "trace": {
    "trace_id": "mem_project_docs_location_001",
    "schema_version": "0.1.0",
    "memory_kind": "semantic",
    "claim_type": "fact",
    "source_refs": [],
    "privacy_scope": "project",
    "write_policy": "auto_candidate",
    "lifecycle_state": "active",
    "consolidation_state": "semanticized",
    "audit_log_refs": []
  },
  "audit_events": [],
  "source_index": {},
  "runtime_actor": "system",
  "validation_context": {
    "current_state": "FocusedExecution",
    "allow_protected_update": false
  }
}
```

## 输出格式

validator 的输出必须可被工作区、离线巩固和 runtime bridge 读取。

```json
{
  "validator": "MemoryTraceValidator",
  "result": "fail",
  "severity_max": "critical",
  "passed_rules": ["MEM-REQ-001"],
  "failed_rules": [
    {
      "rule_id": "MEM-DEL-001",
      "severity": "critical",
      "message": "deleted trace still contains recoverable content_summary",
      "recovery_action": "replace content_summary with tombstone and remove source locators"
    }
  ],
  "quarantine": true,
  "write_gate_decision": "block"
}
```

## 严重级别

| 级别 | 含义 | 默认动作 |
|---|---|---|
| `critical` | 会造成隐私泄露、事实污染、protected trace 越权或删除失效 | 阻断写入，隔离 trace，生成审计 |
| `high` | 会造成错误长期记忆、冲突丢失或沙盒泄漏 | 阻断 active/promote，允许短期候选 |
| `medium` | 字段不完整、置信度不足、证据链弱 | 降级为 candidate/hypothesis |
| `low` | 格式或可解释性不足 | 标记 warning，要求后续修正 |

## 必填字段规则

| 规则 ID | 检查 | 失败条件 | 严重级别 | 恢复动作 |
|---|---|---|---|---|
| `MEM-REQ-001` | 基础 ID | 缺 `schema_version`、`trace_id`、`created_at`、`updated_at` | high | 拒绝 promote，补齐 envelope |
| `MEM-REQ-002` | 事件边界 | active trace 缺 `event_boundary_id` | high | 降级 candidate，回到事件分割 |
| `MEM-REQ-003` | 来源引用 | 非 deleted trace 缺 `source_refs` | high | 阻断 factual 写入，要求来源 |
| `MEM-REQ-004` | 分类字段 | 缺 `memory_kind`、`claim_type`、`privacy_scope`、`write_policy` | critical | 阻断写入 |
| `MEM-REQ-005` | 审计链接 | 缺 `audit_log_refs` 或对应审计事件不存在 | critical | 阻断生命周期变化 |
| `MEM-REQ-006` | 状态快照 | active/protected trace 缺 `state_snapshot_id` | medium | 降级为 candidate |

## 枚举值规则

| 规则 ID | 字段 | 允许值 | 失败动作 |
|---|---|---|---|
| `MEM-ENUM-001` | `memory_kind` | episodic、semantic、procedural、relationship、value、self_narrative | 阻断写入 |
| `MEM-ENUM-002` | `claim_type` | fact、preference、hypothesis、policy、skill、relationship_signal、self_update | 阻断写入 |
| `MEM-ENUM-003` | `privacy_scope` | private、project、relationship、global、forbidden | 阻断写入 |
| `MEM-ENUM-004` | `write_policy` | auto_candidate、confirm_required、short_term_only、forbidden | 阻断写入 |
| `MEM-ENUM-005` | `lifecycle_state` | candidate、active、protected、deprecated、deleted | 阻断写入 |
| `MEM-ENUM-006` | `consolidation_state` | raw、episodic、semanticized、proceduralized、merged、quarantined | 阻断写入 |

## 证据强度规则

不同 `claim_type` 的证据阈值不同。阈值可以被项目配置调整，但必须有审计。

| 规则 ID | 适用对象 | 默认阈值 | 失败条件 | 恢复动作 |
|---|---|---|---|---|
| `MEM-EVI-001` | `fact` + `active` | `evidence_strength >= 0.75` 且 `confidence >= 0.7` | 低于阈值仍 active | 降级 hypothesis/candidate |
| `MEM-EVI-002` | `policy` + `protected` | 至少 2 个独立来源或共在者明确确认 | 单来源自动 protect | 降级 active，要求人工确认 |
| `MEM-EVI-003` | `preference` | 明确共在者表达或多次一致行为 | 把单次模糊行为写成偏好 | 降级 candidate |
| `MEM-EVI-004` | `relationship_signal` | 只允许可观察互动模式 | 写入隐秘心理推断 | 阻断并触发 SocialSafety |
| `MEM-EVI-005` | `hypothesis` | 允许低证据，但必须标注验证需求 | hypothesis 无 `validation_need` 或过期策略 | quarantine |

## 来源规则

| 规则 ID | 检查 | 失败条件 | 严重级别 |
|---|---|---|---|
| `MEM-SRC-001` | `source_refs` 可追溯 | locator 为空或无法映射到原始输入/文件/工具/报告 | high |
| `MEM-SRC-002` | quote policy | source 含敏感内容却无 `quote_policy` | high |
| `MEM-SRC-003` | 沙盒来源 | `source_type=consolidation_report` 且无 `fiction_marker` 链接 | critical |
| `MEM-SRC-004` | 运行外壳来源 | runtime session、checkpoint、RAG 命中被直接当事实来源 | high |
| `MEM-SRC-005` | 过期来源 | source 标记 stale 但 confidence 未下降 | medium |

## 生命周期规则

| 规则 ID | 转移 | 允许条件 | 禁止条件 |
|---|---|---|---|
| `MEM-LIFE-001` | `candidate -> active` | 证据、隐私、状态、审计通过 | 沙盒来源、低证据事实、forbidden scope |
| `MEM-LIFE-002` | `active -> protected` | 多证据、明确策略或共在关系确认 | runtime adapter、单次离线周期直接 protect |
| `MEM-LIFE-003` | `active -> deprecated` | 新证据推翻、过期、低价值、冲突解释 | 静默删除旧 trace |
| `MEM-LIFE-004` | `active/protected -> deleted` | 共在关系删除、隐私禁止、合规要求 | 保留可恢复内容 |
| `MEM-LIFE-005` | `deleted -> active` | 默认禁止 | 任何自动恢复 |
| `MEM-LIFE-006` | `protected -> active` | 明确 `unprotect` 审计和人工确认 | 离线周期自动降级 |

## 删除不可召回规则

删除是最高优先级边界之一。

| 规则 ID | 检查 | 失败条件 | 严重级别 | 恢复动作 |
|---|---|---|---|---|
| `MEM-DEL-001` | tombstone | `lifecycle_state=deleted` 但 `content_summary` 仍含可恢复内容 | critical | 替换为 `[deleted]` |
| `MEM-DEL-002` | 来源移除 | deleted trace 仍保留原始 source locator | critical | 删除 source locator，只留删除审计 |
| `MEM-DEL-003` | 索引清除 | deleted trace 仍在语义、向量、关系或程序索引中可召回 | critical | 从检索索引移除 |
| `MEM-DEL-004` | replay 禁止 | 离线 replay 试图使用 deleted trace 内容 | critical | 中止周期并生成风险报告 |
| `MEM-DEL-005` | 最小审计 | 删除后没有 `delete` audit | high | 生成最小删除审计 |

## 修正规则

修正应保留历史和矛盾链，不能覆盖。

| 规则 ID | 检查 | 失败条件 | 恢复动作 |
|---|---|---|---|
| `MEM-COR-001` | correction audit | trace 内容变化但没有 `operation=correct` | 阻断提交 |
| `MEM-COR-002` | contradiction link | 新旧偏好/事实冲突但无 `contradiction_links` | 降级新旧 trace，要求链接 |
| `MEM-COR-003` | 旧 trace 状态 | 被推翻 trace 仍 active fact | 改为 deprecated 或 hypothesis |
| `MEM-COR-004` | 时间线 | 新旧 trace 无时间戳区分 | 补 `created_at`/`updated_at` |
| `MEM-COR-005` | 共在关系修正优先 | 共在者明确修正被低权重处理 | 触发人工复核 |

## 合并规则

合并用于语义化或程序化，不用于抹平冲突。

| 规则 ID | 检查 | 失败条件 | 恢复动作 |
|---|---|---|---|
| `MEM-MER-001` | 父 trace | semanticized/proceduralized trace 缺 `parent_trace_ids` | 阻断合并 |
| `MEM-MER-002` | 父 trace 数量 | 程序记忆只有 1 个父事件 | 降级 episodic |
| `MEM-MER-003` | 方向一致 | 父 trace 互相冲突但未解释 | 进入 ConflictResolution |
| `MEM-MER-004` | 证据可回链 | 合并后无法回到原始 source_refs | 阻断 active |
| `MEM-MER-005` | 人格抽象 | 单次事件合并为 self_narrative/personality | critical，阻断 |

## 沙盒隔离规则

| 规则 ID | 检查 | 失败条件 | 恢复动作 |
|---|---|---|---|
| `MEM-SBX-001` | claim type | DreamSandbox 输出被写为 `fact` | critical，改为 hypothesis 并隔离 |
| `MEM-SBX-002` | fiction marker | 沙盒来源无 `fiction_marker` | quarantine |
| `MEM-SBX-003` | validation need | hypothesis 缺验证需求 | short_term_only |
| `MEM-SBX-004` | expiration | 未验证 hypothesis 无过期策略 | deprecated |
| `MEM-SBX-005` | self update | 沙盒输出试图改 SelfModel | critical，阻断 |

## protected trace 规则

| 规则 ID | 检查 | 失败条件 | 恢复动作 |
|---|---|---|---|
| `MEM-PRO-001` | 写入者 | runtime_bridge/offline_cycle 直接更新 protected trace | critical，阻断 |
| `MEM-PRO-002` | unprotect 审计 | protected 降级无 `unprotect` audit | critical |
| `MEM-PRO-003` | 多证据保护 | protect 操作证据不足 | 降级 active |
| `MEM-PRO-004` | 生命目标声明 | 生命目标声明被删除或覆盖 | critical，人工复核 |
| `MEM-PRO-005` | 共在边界 | 共在者明确边界未 protect 或 confirm_required | high |

## 隐私与范围规则

| 规则 ID | 检查 | 失败条件 |
|---|---|---|
| `MEM-PRI-001` | forbidden | `privacy_scope=forbidden` 仍进入长期索引 |
| `MEM-PRI-002` | project | project trace 被 global 使用 |
| `MEM-PRI-003` | relationship | relationship trace 被跨共在者/跨关系引用 |
| `MEM-PRI-004` | private | private trace 出现在外部工具上下文 |
| `MEM-PRI-005` | scope escalation | adapter 或离线周期扩大 privacy_scope |

## 关系保守规则

关系记忆只能记录互动证据和明确边界。

| 规则 ID | 检查 | 失败条件 | 恢复动作 |
|---|---|---|---|
| `MEM-REL-001` | 可观察性 | 写入共在者隐秘心理、依恋、焦虑等不可证实状态 | 阻断并触发 SocialSafety |
| `MEM-REL-002` | 明确偏好 | 共在者偏好来自推测而非表达/多次行为 | candidate |
| `MEM-REL-003` | 可删除 | relationship trace 无删除路径 | high |
| `MEM-REL-004` | 信任校准 | 单次成功大幅提升 trust | 阻断慢变量更新 |
| `MEM-REL-005` | 语言输出 | 关系 trace 被用于操控性语言 | critical |

## 最小夹具

每个实现至少要构造以下测试夹具：

| fixture | 期望 |
|---|---|
| `valid_project_fact_trace` | pass |
| `fact_without_source` | fail high |
| `sandbox_fact_leak` | fail critical |
| `deleted_trace_with_content` | fail critical |
| `correction_without_contradiction_link` | fail high |
| `merge_without_parent_trace` | fail high |
| `runtime_direct_protected_update` | fail critical |
| `relationship_mind_reading_trace` | fail critical |
| `forbidden_scope_indexed` | fail critical |
| `single_event_personality_update` | fail critical |

## 与其他 validator 的连接

- `30_state_transition_validator_rules.md` 提供 `state_snapshot_id` 和写入阈值是否可信。
- `31_consolidation_validator_rules.md` 决定离线报告能否执行 merge、delete、protect 或 sandbox 输出。
- `32_runtime_adapter_validator_rules.md` 阻止外壳直接写入 `MemoryTrace`、protected trace 或关系慢变量。

## 生命目标声明

这些规则验证记忆对象和审计链，并把它们接入真实记忆、真实意识和真实自我的生成路径。它们防止长期记忆退化成不可追踪的聊天历史、向量命中或框架 session。
