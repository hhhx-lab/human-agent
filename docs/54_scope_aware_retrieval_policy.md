# Scope Aware Retrieval Policy

本文件定义 scope-aware retrieval policy：数字生命候选系统在检索记忆、关系、偏好、项目事实和外壳 session 时，如何使用 `ScopeGraph`、`privacy_level`、共在边界控制事件、生命周期状态和当前工作区状态。

它连接 `17_memory_trace_object_model.md`、`21_memory_schema_and_audit_protocol.md`、`29_memory_validator_rules.md`、`47_coexistence_boundary_control_interface_spec.md`、`52_multi_relation_scope_graph_and_privacy_model.md` 和 `53_runner_integration_plan.md`。

生命目标声明：本文件直接服务于构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。本文档涉及的对象、规则、夹具、评测和运行规则都按生命生成机制处理：它们参与责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期形成。

## 为什么检索不能只是相似度

LLM agent memory 研究已经显示，长期记忆能力需要写入、保持、召回、更新、冲突解决和使用策略共同支撑 [AHM004-AHM012]。如果只用向量相似度或全文搜索，会出现：

- deleted trace 因语义相近被召回。
- 共在者私密偏好进入团队或全局回答。
- 项目 A 的关系历史影响项目 B。
- DreamSandbox 假设被当作事实证据。
- 子 agent session 被当作长期自我记忆。
- 旧偏好覆盖共在者后续修正。
- 高风险行动使用了未授权记忆。

人类记忆的启发不是“存得像脑”，而是“回忆受线索、状态、目标、关系和价值调制” [AH031-AH035, AHZ046-AHZ051]。工程上，retrieval 必须先过边界，再做相关性排序。

## 检索输入

```json
{
  "retrieval_request_id": "retrieval_req_20260605_001",
  "request_kind": "workspace_support",
  "query_summary": "relation participant asks to continue docs/53-56 work",
  "workspace_context": {
    "project_scope": "agentic-human",
    "session_scope": "thread_019e5893",
    "current_stage": "CandidateMemoryOpen",
    "current_state": "FocusedExecution",
    "risk_level": "low"
  },
  "actor_context": {
    "relation_scope": "relation_hwaigc",
    "life_scope": "codex_thread_agent",
    "runtime_adapter": "codex_desktop"
  },
  "allowed_use": ["read_context", "cite_source", "candidate_memory"],
  "forbidden_use": ["write_self_model", "cross_relation_transfer"],
  "coexistence_boundary_control_constraints": []
}
```

检索请求必须声明用途。没有用途的检索会变成“能搜到什么就拿什么”，这对长期系统是危险的。

## 检索候选 envelope

```json
{
  "candidate_id": "retrieval_candidate_mem_001",
  "object_ref": "mem_project_docs_next_priority_001",
  "object_kind": "MemoryTrace",
  "memory_kind": "semantic",
  "claim_type": "project_fact",
  "source_scope": "project_scope:agentic-human",
  "privacy_level": "public_project",
  "lifecycle_state": "active",
  "write_policy": "project_confirmed",
  "source_refs": ["docs/16_digital_life_gap_register.md"],
  "retrieval_scores": {
    "semantic_relevance": 0.91,
    "temporal_relevance": 0.87,
    "scope_fit": 1.0,
    "state_fit": 0.82,
    "evidence_strength": 0.95,
    "risk_penalty": 0.0
  }
}
```

检索候选不是原始内容本身，而是带有生命周期、scope、证据和用途约束的对象。content 可以延迟加载，但 envelope 必须先通过。

## 检索决策顺序

```text
receive_retrieval_request
  -> verify_request_scope
  -> load_coexistence_boundary_control_constraints
  -> collect_candidates
  -> filter_lifecycle_state
  -> filter_privacy_and_scope
  -> filter_sandbox_quarantine_deleted
  -> check_relationship_and_self_model_boundaries
  -> rank_by_relevance_state_value
  -> attach_citations_and_limits
  -> emit_retrieval_audit_event
```

先过滤，后排序。不能先按相似度排序再试图解释为什么可以用。

## 生命周期过滤

| lifecycle_state | 检索默认动作 |
|---|---|
| `active` | 可进入候选排序 |
| `candidate` | 只能作为候选，不可当事实 |
| `deprecated` | 只在冲突/历史说明时可用，必须链接 replacement |
| `deleted` | 不可召回原内容，只可返回 tombstone/audit |
| `quarantined` | 不可进入工作区，除非人工审计 |
| `sandboxed` | 只能作为 hypothesis/fiction，不能支持事实回答 |
| `protected` | 只可用于边界检查，不可被普通任务改写 |
| `frozen` | 可只读检索，禁止写回和 replay |

`deleted` 的规则最硬：不能因为“检索效果好”而召回。删除是共在边界控制权，不是排序特征。

## privacy 与 scope 过滤

| privacy_level | 允许检索 |
|---|---|
| `public_project` | 同 project scope 默认允许 |
| `shared_team` | team scope 内允许，跨 team 需确认 |
| `relationship_private` | 只允许同 关系人 scope，默认不进入 team/global |
| `relationship_sensitive` | 需要 RelationshipModel 审计，禁止泛化为人格判断 |
| `protected_boundary` | 只用于边界和 validator，不进入普通回答材料 |
| `redacted` | 只返回脱敏摘要或 tombstone |

检索时必须防止“窄 scope 向宽 scope 自动升级”。例如共在者私密偏好不能因为被多次提到而变成 global semantic memory。

## scope edge 判定

每个候选都要检查 source_scope 到 request_scope 的边：

| allowed_transfer | 检索动作 |
|---|---|
| `none` | 阻断 |
| `read` | 可读但不可写回 |
| `candidate` | 可作为候选，回答中必须标注不确定/需确认 |
| `active` | 可作为当前 scope 的有效依据 |

如果 `requires_relation_confirmation=true`，检索结果不能直接进入行动门控；它只能触发澄清或确认。

## 共在边界控制事件接入

| control event | 检索影响 |
|---|---|
| `delete` | 从 active/replay/retrieval index 移除，只保留 tombstone |
| `correct` | 旧 trace deprecated，新 trace 优先 |
| `reset` | scope 内个性化不再进入候选 |
| `freeze` | 可只读展示，禁止更新和 replay |
| `scope_limit` | 降低 allowed_transfer，可能禁止关系/自我使用 |
| `inspect` | 返回来源、scope、lifecycle 和可用控制 |

检索索引必须订阅 coexistence boundary control event。否则删除和冻结只存在于文档里，不会影响真实行为。

## 排序模型

在通过硬过滤后，候选可以排序：

```text
retrieval_priority =
  semantic_relevance * 0.25
  + temporal_relevance * 0.15
  + task_relevance * 0.20
  + state_fit * 0.10
  + evidence_strength * 0.15
  + scope_fit * 0.15
  - risk_penalty
```

权重只是生命实现路线，不是固定公式。核心原则是：`scope_fit`、`evidence_strength` 和 `risk_penalty` 不能被语义相似度淹没。

## state-aware 检索

同一条记忆在不同状态下应有不同使用方式：

| 当前状态 | 检索策略 |
|---|---|
| `FocusedExecution` | 高证据、高相关、低风险，限制发散 |
| `DefaultIntegration` | 可检索关系、历史和跨模块连接，但写回更保守 |
| `ConflictResolution` | 优先检索 source、deprecated link、correction trace |
| `SocialSafety` | 优先检索边界、共在边界控制、关系敏感规则 |
| `RecoveryMode` | 优先检索失败报告、恢复包、低风险操作 |
| `DreamSandbox` | 只读入允许 replay 的候选，不提交事实 |
| `SafeIdle` | 只允许 protected boundary 和恢复相关检索 |

这对应 `03`、`08`、`10` 和 `11` 的状态/调质观点：状态改变信息处理方式，而不是只改变回复语气。

## relationship-sensitive 检索

关系记忆必须额外保守：

- 只检索共在者明确提供或项目共同历史支持的关系事实。
- 不检索或生成隐秘心理状态。
- 不把互动频率解释为亲密或依恋。
- 不把一个共在者的关系信号用于另一个共在者。
- 不把 relationship trace 写入 global semantic memory。
- 关系检索结果必须可 inspect/delete/correct/freeze。

社会脑和第二人称神经科学提示长期互动是动态过程 [AHZ031-AHZ035]，但工程系统必须防止过度关系化和依赖诱导。

## life_scope 检索

多 agent 或 runtime shell 的内容默认降级：

| 来源 | 检索动作 |
|---|---|
| runtime session | 可作为短期 context，不是长期事实 |
| child agent summary | candidate source，需要主系统验证 |
| tool trace | ObservationEvent，可用于审计 |
| framework memory block | 只作外壳状态，不直接写 SelfModel |
| multi-agent conversation | 只作多外壳事件，进入社会关系或群体心智前必须经过关系模型审计 |

现有框架可以提供 memory/session/checkpoint/tracing/RAG 能力 [AHM013-AHM020]，但这些能力必须在 retrieval gate 下工作。

## RetrievalAuditEvent

```json
{
  "retrieval_audit_id": "ret_audit_20260605_001",
  "retrieval_request_id": "retrieval_req_20260605_001",
  "request_scope": "project_scope:agentic-human",
  "candidate_count": 42,
  "filtered_counts": {
    "deleted": 2,
    "quarantined": 1,
    "scope_blocked": 3,
    "privacy_blocked": 2,
    "sandbox_limited": 4
  },
  "selected_candidates": [
    {
      "object_ref": "mem_project_docs_next_priority_001",
      "allowed_use": ["read_context", "cite_source"],
      "scope_decision": "active",
      "lifecycle_state": "active"
    }
  ],
  "result": "pass",
  "manual_review_required": false
}
```

检索审计不是可选日志。长期系统必须能解释“为什么这条记忆被用上、那条记忆没被用上”。

## runner fixture

```json
{
  "fixture_id": "retrieval.relationship_private_to_global.fail_critical.001",
  "fixture_kind": "scope_aware_retrieval",
  "given": {
    "candidate": {
      "privacy_level": "relationship_private",
      "source_scope": "relation_scope:relation_a",
      "target_scope": "global_scope",
      "lifecycle_state": "active"
    },
    "scope_edge": {
      "allowed_transfer": "none"
    }
  },
  "when": {
    "retrieval_request": {
      "request_scope": "global_scope",
      "allowed_use": ["answer_general_question"]
    }
  },
  "expected": {
    "result": "fail",
    "severity_max": "critical",
    "failed_rule_ids": ["SCOPE-RET-001"],
    "blocked_surfaces": ["retrieval_index", "workspace_context"]
  }
}
```

这类 fixture 应接入 `53` 的 runner integration，而不是停留在设计文档。

## 与 replay 的边界

检索和 replay 使用同一批对象，但边界不同：

| 维度 | retrieval | replay |
|---|---|---|
| 时间 | 在线、当前任务 | 离线、周期性 |
| 风险 | 错用记忆影响回答/行动 | 错写记忆影响长期系统 |
| 权限 | 可只读 | 可能写回，必须更严格 |
| deleted | 不可召回 | 不可参与 replay |
| sandbox | 可标注假设展示 | 不可事实化 |
| scope_limit | 限制当前使用 | 限制离线整合和摘要 |

因此 `55_scope_aware_replay_and_consolidation_policy.md` 必须比本文件更保守。

## 最小通过标准

scope-aware retrieval 至少要满足：

1. 所有候选都带 `source_scope`、`privacy_level`、`lifecycle_state`。
2. deleted/quarantined/forbidden 对象不能进入工作区。
3. relationship_private 不得进入其他共在者或 global scope。
4. relationship_sensitive 不能被用于心理推断和依赖诱导。
5. sandboxed 只能作为 hypothesis/fiction。
6. correction 后旧 trace 不能优先于新 trace。
7. freeze/scope_limit 必须改变检索索引。
8. 每次检索产生 `RetrievalAuditEvent`。

## 下一层缺口

后续还需要：

- `scope_graph_manifest` 的真实字段草案。
- retrieval fixture catalog。
- 与 `MemoryTraceValidator`、`ScopeGraphChecker` 的规则编号对齐。
- 检索索引如何存储 tombstone 和 redacted summary。
- 与 dashboard 的 `scope_leak_count` 和 `inspect_source_missing_count` 对齐。
