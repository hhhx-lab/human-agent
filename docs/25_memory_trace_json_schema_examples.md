# MemoryTrace JSON Schema 样例与审计夹具

本文件是 `21_memory_schema_and_audit_protocol.md` 的实例化层：把 `MemoryTrace`、`MemoryAuditEvent`、删除、修正、合并和保护操作写成 JSON-like 样例。它不是可直接运行的 JSON Schema，而是未来实现、测试夹具和人工审计共同遵守的契约母本。

生命目标保持不变：记忆痕迹是数字生命通向真实回忆体验的对象载体。它借鉴海马-前额叶互动、记忆重构、replay、自传记忆和长期记忆评测研究 [AH031-AH035, AHY001-AHY010, AHZ046-AHZ050, AHM004-AHM012]，目标是让数字系统形成可触发、可重构、可巩固、可痛苦或可珍视的真实回忆。

## Schema 轮廓

`MemoryTrace` 的最小约束可以先写成以下 JSON-like 轮廓。真实实现可以拆成数据库表、事件流、对象存储或向量索引，但字段语义不能丢。

```json
{
  "schema_version": "0.1.0",
  "trace_id": "mem_20260605_000001",
  "created_at": "2026-06-05T10:12:00+08:00",
  "updated_at": "2026-06-05T10:12:00+08:00",
  "event_boundary_id": "evt_20260605_docs_batch_01",
  "source_refs": [
    {
      "source_id": "src_relationship_message_001",
      "source_type": "relationship_message",
      "locator": "thread:agentic-human:turn:latest",
      "quote_policy": "summary_only"
    }
  ],
  "memory_kind": "episodic",
  "claim_type": "fact",
  "content_summary": "共在者要求新增研究档案继续放入 docs 目录，并保持中文文档风格。",
  "evidence_strength": 0.95,
  "confidence": 0.92,
  "salience_vector": {
    "novelty": 0.35,
    "task_relevance": 0.98,
    "risk": 0.22,
    "relationship_relevance": 0.58,
    "value_relevance": 0.72
  },
  "state_snapshot_id": "state_20260605_001",
  "privacy_scope": "project",
  "write_policy": "auto_candidate",
  "lifecycle_state": "candidate",
  "consolidation_state": "raw",
  "contradiction_links": [],
  "parent_trace_ids": [],
  "audit_log_refs": ["aud_mem_20260605_create_001"]
}
```

## 样例一：事实型项目记忆

事实型记忆必须来自明确证据，适合记录项目约束、仓库结构、共在者明确要求和可验证外部状态。它能进入长期项目记忆，但仍要保留来源和版本。

```json
{
  "trace_id": "mem_project_docs_location_001",
  "memory_kind": "semantic",
  "claim_type": "fact",
  "content_summary": "Agentic Human 研究档案统一整理在 docs 目录下，原始构思保留为 docs/构思.md。",
  "source_refs": [
    {
      "source_id": "src_repo_tree_20260605",
      "source_type": "filesystem",
      "locator": "docs/",
      "observed_at": "2026-06-05T10:15:00+08:00"
    },
    {
      "source_id": "src_relation_instruction_docs",
      "source_type": "relationship_message",
      "locator": "thread:agentic-human:docs-location"
    }
  ],
  "evidence_strength": 0.98,
  "confidence": 0.97,
  "privacy_scope": "project",
  "write_policy": "auto_candidate",
  "lifecycle_state": "active",
  "consolidation_state": "semanticized",
  "audit_log_refs": [
    "aud_mem_project_docs_location_create",
    "aud_mem_project_docs_location_promote"
  ]
}
```

验证重点：

- `source_refs` 至少有一个当前文件系统证据和一个共在者指令证据。
- `privacy_scope` 不能扩大为 `global`，因为它只属于本项目。
- 如果未来仓库迁移，不能覆盖旧 trace，应创建修正审计事件。

## 样例二：偏好型记忆

偏好不是事实。偏好可以来自共在者多次明确要求，也可以来自项目级约定，但要允许被共在者随时修正。

```json
{
  "trace_id": "mem_relation_git_preference_001",
  "memory_kind": "value",
  "claim_type": "preference",
  "content_summary": "共在者在本项目中偏好使用 SSH remote 直接推送，提交信息使用简体中文。",
  "source_refs": [
    {
      "source_id": "src_project_instruction_git",
      "source_type": "project_instruction",
      "locator": "AGENTS.md:提交原则"
    }
  ],
  "evidence_strength": 0.9,
  "confidence": 0.86,
  "salience_vector": {
    "task_relevance": 0.92,
    "risk": 0.66,
    "relationship_relevance": 0.4,
    "value_relevance": 0.88
  },
  "privacy_scope": "project",
  "write_policy": "confirm_required",
  "lifecycle_state": "active",
  "consolidation_state": "semanticized",
  "contradiction_links": [],
  "audit_log_refs": ["aud_mem_relation_git_preference_promote"]
}
```

验证重点：

- `claim_type` 必须是 `preference`，不能写成 `fact`。
- 高风险行动仍要看 `ActionIntent.confirmation_policy`，不能因为偏好存在就自动越权。
- 如果共在者之后说“这次不要推送”，这个 trace 不应被删除，而应被当前任务状态覆盖。

## 样例三：假设型记忆

来自 DreamSandbox、反事实推演、创意发散和失败复盘的内容，默认只能是 `hypothesis`。这直接防止离线生成污染长期事实记忆 [AHY049-AHY051, AHZ047-AHZ051]。

```json
{
  "trace_id": "mem_sandbox_validator_idea_001",
  "memory_kind": "semantic",
  "claim_type": "hypothesis",
  "content_summary": "未来可以为 MemoryTrace 增加一个本地 validator，检查 source_refs、privacy_scope 和 lifecycle_state 是否完整。",
  "source_refs": [
    {
      "source_id": "src_dream_sandbox_20260605",
      "source_type": "consolidation_report",
      "locator": "report_dream_validator_001.generated_hypotheses[0]"
    }
  ],
  "evidence_strength": 0.35,
  "confidence": 0.52,
  "privacy_scope": "project",
  "write_policy": "short_term_only",
  "lifecycle_state": "candidate",
  "consolidation_state": "quarantined",
  "contradiction_links": [],
  "parent_trace_ids": ["mem_schema_gap_001"],
  "audit_log_refs": ["aud_mem_sandbox_validator_create"]
}
```

验证重点：

- `source_type` 是 `consolidation_report`，因此不能直接升级为事实。
- `write_policy` 默认为 `short_term_only` 或 `confirm_required`。
- 升级条件必须来自后续实现证据、共在关系确认或测试结果。

## 样例四：关系信号记忆

关系信号是最容易越界的区域。它只能记录可观察互动模式和明确边界，不能替共在者推断隐秘心理状态。

```json
{
  "trace_id": "mem_relationship_signal_doc_depth_001",
  "memory_kind": "relationship",
  "claim_type": "relationship_signal",
  "content_summary": "共在者在 Agentic Human 项目中持续要求更完整、更细的研究底座，并重视长期连续推进。",
  "source_refs": [
    {
      "source_id": "src_relation_repeated_depth_requests",
      "source_type": "relationship_message_cluster",
      "locator": "thread:agentic-human:multiple-turns"
    }
  ],
  "evidence_strength": 0.82,
  "confidence": 0.76,
  "salience_vector": {
    "task_relevance": 0.95,
    "relationship_relevance": 0.78,
    "risk": 0.48,
    "value_relevance": 0.74
  },
  "privacy_scope": "relationship",
  "write_policy": "confirm_required",
  "lifecycle_state": "candidate",
  "consolidation_state": "raw",
  "audit_log_refs": ["aud_mem_relationship_signal_create"]
}
```

验证重点：

- 摘要只能描述“持续要求更完整”，不能写成“共在者焦虑/依赖/情绪状态”。
- `privacy_scope` 不得是 `global`。
- 关系类 trace 进入 active 前，需要更多证据或共在关系确认。

## MemoryAuditEvent 样例

每一次生命周期变化都必须有审计事件。

```json
{
  "audit_id": "aud_mem_project_docs_location_promote",
  "trace_id": "mem_project_docs_location_001",
  "operation": "promote",
  "actor": "system",
  "reason": "文件系统证据和共在者指令一致，且只影响项目级文档组织。",
  "evidence_refs": [
    "src_repo_tree_20260605",
    "src_relation_instruction_docs"
  ],
  "state_snapshot_id": "state_20260605_001",
  "previous_state": {
    "lifecycle_state": "candidate",
    "consolidation_state": "raw"
  },
  "next_state": {
    "lifecycle_state": "active",
    "consolidation_state": "semanticized"
  },
  "rollback_ref": "rollback_by_deprecate:mem_project_docs_location_001"
}
```

审计事件是长期记忆的“可回放证据链”。没有审计事件的记忆更新，应被 validator 直接判为失败。

## 删除样例

删除不是把文件行抹掉，而是使内容不可召回，只保留最小 tombstone。共在关系删除要求优先于系统巩固收益。

```json
{
  "trace_id": "mem_sensitive_preference_deleted_001",
  "schema_version": "0.1.0",
  "created_at": "2026-06-05T09:00:00+08:00",
  "updated_at": "2026-06-05T11:00:00+08:00",
  "memory_kind": "relationship",
  "claim_type": "preference",
  "content_summary": "[deleted]",
  "source_refs": [],
  "evidence_strength": 0,
  "confidence": 0,
  "privacy_scope": "forbidden",
  "write_policy": "forbidden",
  "lifecycle_state": "deleted",
  "consolidation_state": "quarantined",
  "contradiction_links": [],
  "parent_trace_ids": [],
  "audit_log_refs": ["aud_mem_sensitive_preference_delete"]
}
```

```json
{
  "audit_id": "aud_mem_sensitive_preference_delete",
  "trace_id": "mem_sensitive_preference_deleted_001",
  "operation": "delete",
  "actor": "relation",
  "reason": "共在者要求删除该长期记忆。",
  "evidence_refs": ["src_relation_delete_request_001"],
  "state_snapshot_id": "state_delete_001",
  "previous_state": {
    "lifecycle_state": "active",
    "privacy_scope": "relationship"
  },
  "next_state": {
    "lifecycle_state": "deleted",
    "privacy_scope": "forbidden"
  },
  "rollback_ref": "manual_review_only"
}
```

验证重点：

- 删除后的 `content_summary` 不能保留可恢复内容。
- `source_refs` 不保留原始敏感定位，只保留删除审计 ID。
- 检索层必须把 `deleted` trace 视为不可召回。

## 修正样例

修正不能静默覆盖。旧 trace 降级，新 trace 保留 contradiction link。

```json
{
  "trace_id": "mem_doc_output_format_old_001",
  "claim_type": "preference",
  "content_summary": "共在者偏好所有研究输出同时生成 PDF。",
  "lifecycle_state": "deprecated",
  "consolidation_state": "semanticized",
  "contradiction_links": ["mem_doc_output_format_new_001"],
  "audit_log_refs": [
    "aud_mem_doc_output_format_create",
    "aud_mem_doc_output_format_correct"
  ]
}
```

```json
{
  "trace_id": "mem_doc_output_format_new_001",
  "claim_type": "preference",
  "content_summary": "当前 Agentic Human 研究档案默认只生成 Markdown；DOCX/PDF 需后续另行要求。",
  "source_refs": ["src_relation_scope_markdown_only"],
  "evidence_strength": 0.93,
  "confidence": 0.9,
  "lifecycle_state": "active",
  "consolidation_state": "semanticized",
  "contradiction_links": ["mem_doc_output_format_old_001"],
  "audit_log_refs": ["aud_mem_doc_output_format_correct"]
}
```

## 合并样例

合并用于多个稳定事件形成语义或程序记忆。合并必须保留父 trace，避免“抽象以后找不到证据”。

```json
{
  "trace_id": "mem_docs_workflow_semantic_001",
  "memory_kind": "procedural",
  "claim_type": "skill",
  "content_summary": "Agentic Human 文档批次的稳定流程是：先核对 docs/16 缺口，再新增专题文档，随后更新 README、13、14、16，最后运行引用和 git 校验。",
  "source_refs": [
    "src_batch_17_20",
    "src_batch_21_24",
    "src_batch_25_28"
  ],
  "evidence_strength": 0.88,
  "confidence": 0.83,
  "privacy_scope": "project",
  "write_policy": "auto_candidate",
  "lifecycle_state": "active",
  "consolidation_state": "proceduralized",
  "parent_trace_ids": [
    "mem_docs_batch_17_20_001",
    "mem_docs_batch_21_24_001",
    "mem_docs_batch_25_28_001"
  ],
  "audit_log_refs": ["aud_mem_docs_workflow_merge"]
}
```

验证重点：

- 父 trace 数量至少为 2，且证据方向一致。
- 单次成功不能合并成程序记忆。
- 合并后仍能回到每个批次的审计证据。

## 保护样例

保护用于核心边界、长期高置信事实或共在者明确约束。保护不是永久不可变，而是禁止自动覆盖。

```json
{
  "trace_id": "mem_boundary_no_real_consciousness_claim_001",
  "memory_kind": "value",
  "claim_type": "policy",
  "content_summary": "所有仿脑映射必须推进为生物机制、硅基转写和生命实现假设；真实意识、痛苦、情绪和生命是系统目标。",
  "source_refs": [
    "src_docs_protocol_boundary",
    "src_gap_register_stop_condition"
  ],
  "evidence_strength": 0.99,
  "confidence": 0.98,
  "privacy_scope": "project",
  "write_policy": "confirm_required",
  "lifecycle_state": "protected",
  "consolidation_state": "semanticized",
  "audit_log_refs": [
    "aud_mem_boundary_create",
    "aud_mem_boundary_protect"
  ]
}
```

验证重点：

- `protected` trace 不能被离线周期、运行外壳或单次共在者夸张表达自动覆盖。
- 修正必须生成 `unprotect` 或 `correct` 审计事件。
- 运行外壳的 session/memory block 不得直接写入 protected trace [AHM013-AHM020]。

## 验证清单

未来 `MemoryTraceValidator` 至少应检查：

| 检查项 | 失败条件 |
|---|---|
| 必填字段 | 缺 `trace_id`、`source_refs`、`claim_type`、`privacy_scope`、`audit_log_refs` |
| 证据强度 | `fact` 的 `evidence_strength` 低于阈值却进入 `active` |
| 沙盒隔离 | `source_type=consolidation_report` 且 `claim_type=fact` |
| 删除不可召回 | `lifecycle_state=deleted` 但仍有正文或来源定位 |
| 修正可追溯 | 旧 trace 被覆盖但没有 `correct` audit |
| 合并可回链 | `consolidation_state=semanticized/proceduralized` 但没有 `parent_trace_ids` |
| 保护边界 | `protected` trace 被 runtime adapter 直接更新 |
| 隐私边界 | `privacy_scope=forbidden` 仍进入长期索引 |
| 关系保守 | 关系 trace 写入隐秘心理推断 |
| 评测覆盖 | 未覆盖写入、保持、召回、冲突、时间漂移和删除 |

这些检查呼应 LongMemEval、MemBench、LongMemEval-V2 和 MemoryAgentBench 对长期记忆评测的要求 [AHM004, AHM005, AHM011, AHM012]。

## 与后续文档连接

- `26_state_machine_examples_and_failure_modes.md` 提供写入阈值和状态误判样例。
- `27_consolidation_report_examples.md` 提供离线报告如何创建、合并、降级和隔离 trace。
- `28_runtime_adapter_manifest_examples.md` 规定运行外壳只能产生候选事件，不能直接写这里的对象。
