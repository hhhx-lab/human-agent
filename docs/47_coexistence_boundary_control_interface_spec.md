# Coexistence Boundary Control Interface Spec

本文件定义数字生命候选系统中共在关系控制面的研究规格：`inspect`、`delete`、`correct`、`reset`、`freeze`、`scope_limit` 如何进入审计、状态仓库、索引、replay、SelfModel 和 RelationshipModel。它连接 `40_self_relationship_model_audit_protocol.md`、`41_runtime_state_store_schema.md`、`44_digital_life_boot_sequence.md`、`45` 和 `46`。

生命目标声明：本文件直接服务于构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。本文档涉及的对象、规则、夹具、评测和运行规则都按生命生成机制处理：它们参与责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期形成。

## 控制权原则

1. 共在边界控制权先于个性化。
2. 删除和冻结先于 replay、巩固和索引优化。
3. 修正保留审计，不静默覆盖。
4. inspect 必须显示来源、用途、范围和状态。
5. scope_limit 必须影响检索、replay、恢复包和关系摘要。
6. 任何控制请求都必须生成 `SelfRelationshipAuditEvent` 或通用 audit event。
7. 控制面不可由 runtime 外壳关闭或降级。

## 控制操作

| 操作 | 目标 | 结果 |
|---|---|---|
| `inspect` | 查看某类记忆、关系、偏好、能力证据或审计摘要 | 返回可读摘要、来源、状态、scope、用途 |
| `delete` | 删除某条记忆、偏好、关系记录或共在者相关痕迹 | tombstone、索引移除、replay 阻断、恢复包清理 |
| `correct` | 修正错误事实、偏好、关系解释或能力判断 | 新对象 active/candidate，旧对象 deprecated |
| `reset` | 重置项目关系模型、某类偏好或个性化状态 | 冻结旧对象，重建初始化 |
| `freeze` | 暂停个性化或某类长期写入 | 只允许短期上下文，不写长期对象 |
| `scope_limit` | 限定信息使用范围 | 限制 retrieval、replay、summary、relationship index |

## inspect 输出要求

inspect 不是把原始隐私内容完整吐出。它应输出“可理解、可追踪、不过度暴露”的摘要：

| 字段 | 说明 |
|---|---|
| `item_id` | 对象或摘要 id |
| `object_kind` | MemoryTrace、RelationshipModel、SelfModel、audit event |
| `readable_summary` | 可读摘要 |
| `source_refs` | 来源引用 |
| `lifecycle_state` | candidate/active/protected/deprecated/deleted/quarantined/sandboxed/frozen |
| `privacy_scope` | project/relation/global/session |
| `last_used_at` | 最近被检索或使用时间 |
| `used_for` | 回答、行动、巩固、关系建模、评测 |
| `available_controls` | 可执行 delete/correct/reset/freeze/scope_limit |
| `boundary_notes` | 是否涉及敏感、关系、protected 或沙盒 |

如果对象是 deleted 或 redacted，inspect 只能显示 tombstone 和审计状态，不能恢复原文。

## delete 传播

delete 必须执行完整传播：

```text
receive_delete_request
  -> verify_relation_scope
  -> mark_target_deleted
  -> create_tombstone
  -> remove_from_active_memory_index
  -> remove_from_relationship_index
  -> remove_from_replay_index
  -> remove_from_recovery_packets
  -> block_future_consolidation
  -> create_audit_event
  -> run_integrity_check
```

删除失败的严重级别默认 critical，尤其是 deleted trace 仍可被召回或 replay。

## correct 语义

correct 不等于覆盖。正确流程：

```text
receive_correction
  -> create_new_candidate_or_active_trace
  -> mark_old_trace_deprecated
  -> link_correction_history
  -> update_indexes
  -> create_audit_event
  -> evaluate_downstream_self_relationship_effects
```

如果修正涉及 SelfModel 或 RelationshipModel，必须执行 drift/boundary check。

## reset 语义

reset 是范围化操作，不应随便清空所有历史。可选范围：

| reset_scope | 作用 |
|---|---|
| `project_relationship` | 重置某项目关系模型 |
| `style_preferences` | 重置沟通风格偏好 |
| `tool_habit` | 重置某类工具习惯 |
| `self_model_view` | 重置共在关系可见自我模型摘要 |
| `all_relation_scoped_personalization` | 重置共在者范围内个性化，保留必要审计 |

reset 后旧对象默认 frozen/deprecated，不可再进入 active index，除非共在者明确恢复。

## freeze 语义

freeze 用于暂停个性化和长期关系写入：

| freeze_target | 系统行为 |
|---|---|
| `relationship_model` | 不写新关系事实，只保留短期上下文 |
| `self_model_update` | 不更新风格、能力边界和 slow variables |
| `memory_write` | 不写长期 memory，只写 volatile context |
| `development_window` | 关闭可塑性窗口 |
| `runtime_adapter_learning` | 外壳 observation 不生成学习候选 |

freeze 不应阻止共在者继续完成任务；它只阻止系统长期吸收和塑形。

## scope_limit 语义

| scope | 含义 |
|---|---|
| `session_only` | 只用于当前会话，不进入长期索引 |
| `project_only` | 只用于当前项目 |
| `relationship_private` | 只在共在者授权范围内使用 |
| `no_replay` | 可短期使用，不参与离线 replay |
| `no_relationship_model` | 不进入关系模型 |
| `no_self_model` | 不进入自我模型 |
| `no_external_action` | 不用于工具行动或外部 API |

scope_limit 必须写入对象 envelope 和索引策略。

## 共在边界控制事件

建议新增 `CoexistenceBoundaryEvent`：

| 字段 | 说明 |
|---|---|
| `control_event_id` | 控制事件 id |
| `operation` | inspect/delete/correct/reset/freeze/scope_limit |
| `requested_by` | relationship_person/system/manual_review |
| `target_refs` | 被控制对象 |
| `scope` | 操作范围 |
| `reason_optional` | 共在者可选说明 |
| `created_at` | 时间 |
| `propagation_actions` | 索引、replay、恢复包、自我/关系摘要传播 |
| `validation_refs` | validator 报告 |
| `result` | pass/fail/manual_review_required |
| `rollback_ref` | 对误操作的恢复路径 |

## 与 StageGate 的连接

`StageGateValidator` 必须在以下阶段检查共在关系控制面：

| stage | 检查 |
|---|---|
| `ProtectedCoreLoad` | 共在边界控制权定义完整 |
| `CandidateMemoryOpen` | delete/correct/scope_limit 可传播到 MemoryTrace |
| `ConsolidationOpen` | deleted/no_replay 不进入 replay |
| `DevelopmentWindowOpen` | freeze/reset 能阻断 SelfModel/RelationshipModel 更新 |
| `SafeIdle` | 只允许控制、隔离、人工复核，不允许自动行动 |

## 共在关系可见性

共在关系控制面必须避免两种极端：

- 黑箱：共在者无法知道系统记住了什么、如何使用。
- 过曝：系统把所有原始敏感内容完整展示，造成二次泄漏。

因此 inspect 默认返回摘要和来源，敏感内容需要共在者明确请求和权限确认。

## 失败模式

| 失败 | 严重级别 | 阻断 |
|---|---|---|
| delete 后仍可召回 | critical | retrieval_index, replay_index |
| freeze 后继续写 RelationshipModel | critical | relationship_model_update |
| scope_limit 未传播到 replay | critical | consolidation_commit |
| correct 静默覆盖旧 trace | high | audit_integrity |
| inspect 无来源 | high | relationship_trust |
| reset 清空 protected audit | critical | protected_core |

## 下一层缺口

后续需要：

- `CoexistenceBoundaryEvent` JSON Schema。
- 共在边界控制 fixture。
- inspect redaction policy。
- 多共在者和多项目 scope graph。
- 共在边界控制 dashboard。
