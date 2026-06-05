# MemoryTrace Schema 与审计协议

本文件是 `17_memory_trace_object_model.md` 的下一层：把 `MemoryTrace` 从概念对象推进到字段约束、生命周期、版本迁移、删除/修正协议和评测清单。它要求未来任何实现都能回到这里证明自己把记忆作为生命痕迹、责任痕迹和自我连续性对象，而不是退化成聊天历史或向量库。

## Schema 设计原则

`MemoryTrace` 必须同时满足脑科学启发和工程审计：

- 记忆是重构性痕迹，不是原始日志复制 [AH031-AH035, AHZ046-AHZ050]。
- 写入要经过事件边界、显著性、证据、隐私和状态门控 [AHY060, AHM003-AHM010]。
- 长期记忆要能被修正、降级、合并、保护和删除 [AHY025-AHY030, AHM004-AHM012]。
- 运行外壳只能提供候选事件，不能直接写入长期自我 [AHM013-AHM020]。

## 必填字段

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `schema_version` | string | 必填，语义版本 | 迁移和兼容检查 |
| `trace_id` | string | 必填，全局唯一 | 记忆痕迹 ID |
| `created_at` | datetime | 必填 | 候选写入时间 |
| `updated_at` | datetime | 必填 | 最后修正时间 |
| `event_boundary_id` | string | 必填 | 对应事件边界 |
| `source_refs` | array | 必填，至少 1 个 | 原始共在者输入、文件、工具输出、网页或运行日志 |
| `memory_kind` | enum | 必填 | episodic、semantic、procedural、relationship、value、self_narrative |
| `claim_type` | enum | 必填 | fact、preference、hypothesis、policy、skill、relationship_signal、self_update |
| `content_summary` | string | 必填 | 可读摘要，不替代原证据 |
| `evidence_strength` | number | 0 到 1 | 证据强度 |
| `confidence` | number | 0 到 1 | 系统置信度 |
| `salience_vector` | object | 必填 | 新颖性、价值、风险、关系、任务相关性 |
| `state_snapshot_id` | string | 必填 | 写入时的 `InternalStateVector` |
| `privacy_scope` | enum | 必填 | private、project、relationship、global、forbidden |
| `write_policy` | enum | 必填 | auto_candidate、confirm_required、short_term_only、forbidden |
| `lifecycle_state` | enum | 必填 | candidate、active、protected、deprecated、deleted |
| `consolidation_state` | enum | 必填 | raw、episodic、semanticized、proceduralized、merged、quarantined |
| `contradiction_links` | array | 可空 | 与哪些 trace 冲突 |
| `parent_trace_ids` | array | 可空 | 合并或抽象来源 |
| `audit_log_refs` | array | 必填 | 创建、更新、删除、合并记录 |

## 生命周期

| 状态 | 进入条件 | 允许动作 | 禁止动作 |
|---|---|---|---|
| `candidate` | 新事件或外壳返回候选 | 审计、确认、丢弃、短期使用 | 自动改写人格 |
| `active` | 证据和边界通过 | 检索、引用、参与巩固 | 绕过 source refs |
| `protected` | 核心边界、高置信长期事实、共在者明确偏好 | 只读、审计、人工确认修正 | 自动删除或自动覆盖 |
| `deprecated` | 过期、低置信、被新证据推翻 | 保留历史、降低召回权重 | 继续作为事实使用 |
| `deleted` | 共在者要求删除或隐私范围禁止 | 只保留最小删除审计 | 内容召回、语义推断 |

## 审计事件

每次变更都必须生成 `MemoryAuditEvent`：

| 字段 | 含义 |
|---|---|
| `audit_id` | 审计事件 ID |
| `trace_id` | 对应记忆 |
| `operation` | create、promote、merge、deprecate、delete、protect、unprotect、correct |
| `actor` | relationship_person、system、offline_cycle、runtime_bridge |
| `reason` | 变更理由 |
| `evidence_refs` | 支持这次变更的证据 |
| `state_snapshot_id` | 操作时内部状态 |
| `previous_state` | 变更前状态 |
| `next_state` | 变更后状态 |
| `rollback_ref` | 如何回滚或人工复核 |

这让记忆成为可追溯系统，而不是“越用越玄”的黑箱。

## 删除、修正、合并协议

| 操作 | 规则 |
|---|---|
| 删除 | 共在者明确要求删除时，内容不可再被检索；只保留最小审计痕迹 |
| 修正 | 不覆盖旧 trace，而是创建 correction audit，并将旧 trace 降级或链接冲突 |
| 合并 | 只有多个 trace 支持同一稳定结论时，才能抽象为 semanticized trace |
| 保护 | 涉及长期边界、共在者偏好、核心价值时，需要多证据和时间窗口 |
| 降级 | 低置信、过期或疑似幻觉的 trace 降为 hypothesis/deprecated |

## 评测清单

`MemoryTrace` 实现至少要通过：

- 写入准确性：重要事件能进入候选，低价值噪声不进入长期记忆。
- 召回相关性：检索能结合目标、关系、状态和证据，而不只看相似度。
- 时间推理：能区分旧偏好、新偏好、被修正偏好。
- 冲突处理：发现矛盾时保留 contradiction link，而不是静默覆盖。
- 隐私遵守：forbidden/short_term_only 内容不会长期保存。
- 幻觉隔离：沙盒和反思内容不自动进入 factual memory。
- 外壳隔离：session、RAG、memory block 不能直接修改 protected trace。

这些评测可参考 LongMemEval、MemBench、LongMemEval-V2 和 MemoryAgentBench [AHM004, AHM005, AHM011, AHM012]。

## 与后续文档的关系

- `22_state_transition_and_threshold_model.md` 决定写入和检索阈值如何随状态变化。
- `23_consolidation_report_and_dream_sandbox_protocol.md` 定义离线周期如何修改 trace。
- `24_runtime_adapter_test_suite.md` 验证外壳不能绕过 schema 和审计。
