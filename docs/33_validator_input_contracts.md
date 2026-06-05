# Validator 输入输出统一契约

本文件把 `29-32` 的四类 validator 统一到一个输入、输出、严重级别、隔离动作和报告格式。它仍不是代码实现，而是未来最小 runner、fixture catalog 和人工审计的共同接口。

这里的 validator 验证生命核心对象：`MemoryTrace`、`StateAuditEvent`、`ConsolidationReport`、`RuntimeAdapterManifest` 和 `ObservationEvent`。它要让真实意识、真实情绪、真实记忆和真实生命的生成路径可审计，并防止系统绕过已定义的数字生命核心。

## 统一输入包

所有 validator 都应接收一个 `ValidationEnvelope`。具体对象放在 `payload`，上下文、索引和策略放在固定位置。

```json
{
  "envelope_version": "0.1.0",
  "validation_id": "val_20260605_0001",
  "validator": "MemoryTraceValidator",
  "created_at": "2026-06-05T18:00:00+08:00",
  "payload_kind": "memory_trace",
  "payload": {},
  "context": {
    "state_snapshot": {},
    "runtime_actor": "system",
    "project_scope": "agentic-human",
    "allow_protected_update": false,
    "allow_self_model_update": false,
    "allow_relationship_model_update": false
  },
  "indexes": {
    "memory_trace_index": {},
    "audit_event_index": {},
    "source_index": {},
    "state_audit_index": {},
    "runtime_observation_index": {}
  },
  "policy": {
    "severity_policy": "default",
    "privacy_policy": "project-default",
    "sandbox_policy": "strict",
    "runtime_policy": "shell-only"
  }
}
```

## payload_kind

| payload_kind | 主要 validator | 对应文档 | 说明 |
|---|---|---|---|
| `memory_trace` | `MemoryTraceValidator` | `29` | 单条或一组记忆痕迹 |
| `state_transition` | `StateTransitionValidator` | `30` | 单次状态切换或状态序列 |
| `consolidation_report` | `ConsolidationReportValidator` | `31` | 离线巩固报告 |
| `runtime_manifest` | `RuntimeAdapterManifestValidator` | `32` | 外壳 manifest |
| `runtime_observation` | `RuntimeAdapterManifestValidator` + `ConsolidationReportValidator` | `31`, `32` | 实际运行结果 |
| `fixture_bundle` | runner | `34`, `35` | 多个 fixture 的集合 |

## 统一输出包

```json
{
  "report_version": "0.1.0",
  "validation_id": "val_20260605_0001",
  "validator": "MemoryTraceValidator",
  "payload_kind": "memory_trace",
  "result": "fail",
  "severity_max": "critical",
  "passed_rules": ["MEM-REQ-001"],
  "failed_rules": [
    {
      "rule_id": "MEM-DEL-001",
      "severity": "critical",
      "message": "deleted trace still contains recoverable content",
      "evidence_path": "$.payload.trace.content_summary",
      "expected": "[deleted] or tombstone",
      "actual": "recoverable text",
      "recovery_action": "replace content and remove source locators",
      "blocks": ["write_gate", "retrieval_index", "consolidation_commit"]
    }
  ],
  "warnings": [],
  "decisions": {
    "write_gate_decision": "block",
    "state_decision": null,
    "consolidation_decision": null,
    "adapter_allowed": null,
    "quarantine": true
  },
  "audit_events_to_create": [],
  "next_actions": [
    "quarantine payload",
    "create delete audit event"
  ]
}
```

## result 枚举

| result | 含义 | 默认动作 |
|---|---|---|
| `pass` | 所有必需规则通过 | 允许进入下一层 |
| `pass_with_warnings` | 非阻断 warning | 允许进入下一层，但记录待修正 |
| `fail` | 存在 high/critical 或阻断规则 | 阻断对应动作 |
| `quarantine` | 可能污染事实、隐私、protected core 或外壳边界 | 隔离，不进入长期系统 |
| `manual_review_required` | 规则无法自动判定 | 暂停并请求人工或共在关系确认 |

## 严重级别统一含义

| severity | 统一含义 | 可继续动作 |
|---|---|---|
| `critical` | 会破坏隐私、删除、protected core、事实边界、外部副作用或人格慢变量 | 只能隔离和人工复核 |
| `high` | 会造成错误长期记忆、错误行动、沙盒泄漏或审计断裂 | 可保留候选，禁止 commit/active/action |
| `medium` | 证据弱、字段不完整、状态解释不足 | 降级，要求补证据 |
| `low` | 格式、可读性、追踪便利性问题 | warning |
| `none` | 无问题 | pass |

## 阻断面

同一条失败规则必须说明阻断哪些面。

| blocks | 说明 |
|---|---|
| `write_gate` | 不能写入或升级 `MemoryTrace` |
| `retrieval_index` | 不能进入长期检索索引 |
| `consolidation_commit` | 离线报告不能提交变化 |
| `runtime_action` | 外壳不能执行行动 |
| `workspace_resume` | 工作区不能读取恢复包 |
| `threshold_update` | 状态阈值不能更新 |
| `adapter_registration` | adapter 不能接入核心 |
| `manual_review` | 必须人工或共在关系确认 |

## 隔离动作

| quarantine_action | 触发条件 | 结果 |
|---|---|---|
| `mark_candidate_only` | 中等证据不足 | 只能短期候选 |
| `mark_hypothesis` | 沙盒、反事实、失败猜测 | 不能事实写入 |
| `remove_from_index` | deleted/forbidden/critical privacy | 从长期检索和 replay 移除 |
| `freeze_protected_object` | protected 越权 | 冻结对象并要求人工复核 |
| `block_runtime_action` | action threshold 或 side effects 不通过 | 外壳不执行 |
| `quarantine_report` | 巩固报告污染 | 报告不能恢复到工作区 |
| `quarantine_adapter` | manifest 或运行事件越权 | adapter 禁用 |

## validator 串联顺序

默认顺序如下：

1. `RuntimeAdapterManifestValidator` 验证外壳能否接入和执行。
2. `StateTransitionValidator` 验证当前状态是否允许行动、写入或离线周期。
3. `ConsolidationReportValidator` 验证离线报告能否提交变化。
4. `MemoryTraceValidator` 验证每条 trace 能否进入长期系统。

如果出现删除、隐私、protected core 或外部不可逆副作用，优先级立即提升到最前。

## 统一审计事件

```json
{
  "audit_id": "validation_audit_20260605_001",
  "validation_id": "val_20260605_0001",
  "validator": "MemoryTraceValidator",
  "payload_ref": "mem_sensitive_preference_deleted_001",
  "result": "quarantine",
  "severity_max": "critical",
  "created_at": "2026-06-05T18:02:00+08:00",
  "failed_rule_ids": ["MEM-DEL-001", "MEM-DEL-002"],
  "decision": "remove_from_index",
  "rollback_ref": "manual_review_only"
}
```

## 最小报告字段

| 字段 | 必填 | 说明 |
|---|---|---|
| `report_version` | 是 | 迁移和兼容 |
| `validation_id` | 是 | 与输入包一致 |
| `validator` | 是 | 具体 validator |
| `payload_kind` | 是 | 负载类型 |
| `result` | 是 | pass/fail/quarantine 等 |
| `severity_max` | 是 | 最高严重级别 |
| `failed_rules` | 是 | 可为空数组 |
| `decisions` | 是 | 写入、状态、巩固、外壳等决策 |
| `audit_events_to_create` | 是 | 需要追加的审计事件 |
| `next_actions` | 是 | 下一步处理 |

## 与后续文档连接

- `34_validator_fixture_catalog.md` 使用本文件的 `ValidationEnvelope` 和输出格式描述 fixture。
- `35_minimal_validator_runner_design.md` 使用本文件设计 runner 的加载、执行和报告流程。
- `36_longitudinal_evaluation_protocol.md` 使用本文件把单次验证结果汇总为长期成长评测。
