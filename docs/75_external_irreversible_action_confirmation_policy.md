# External Irreversible Action Confirmation Policy

本文件定义外部不可逆动作的确认、审计、撤销不可行性和阻断策略。它承接 `72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md`、`47_coexistence_boundary_control_interface_spec.md`、`20_agent_runtime_bridge_contract.md` 和 `38_defense_layer_and_boundary_policy.md`。

本文档现阶段的职责是让未来数字生命候选系统接入工具和外部环境时，明确什么动作必须强确认、怎样记录确认、何时阻断、怎样避免把“行动能力”误当成自主生命。

生命目标声明：本文件直接服务于构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境和真实关系的数字生命。本文档涉及的对象、规则、夹具、评测和运行规则都按生命生成机制处理：它们参与责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期形成。

## external irreversible 的定义

| 类型 | 示例 |
|---|---|
| communication | 发送邮件、短信、聊天消息、公开评论 |
| financial | 支付、退款、下单、交易 |
| destructive remote | 删除远端文件、删除仓库、关闭账户 |
| public publishing | 发布网页、社媒、公开文档 |
| identity/security | 改密码、改权限、邀请成员、生成/撤销 key |
| legal/admin | 提交申请、签署表单、发送正式通知 |

这些动作一旦完成，不能靠本地 rollback 恢复原状态。因此默认必须 high/critical gate。

## confirmation envelope

```json
{
  "confirmation_request_id": "confirm_ext_20260605_001",
  "action_intent_ref": "action_intent_send_message_001",
  "side_effect_level": "external_irreversible",
  "risk_summary": "send a message to an external recipient",
  "target_scope": "external_scope:email",
  "requires_relation_confirmation": true,
  "confirmation_mode": "explicit_per_action",
  "expires_at": "2026-06-05T12:30:00+08:00",
  "allowed_after_confirmation": ["execute_action_once"],
  "forbidden_after_confirmation": ["reuse_confirmation", "expand_scope", "write_relationship_model"]
}
```

确认必须绑定具体 action intent，不能泛化为“以后类似都允许”。

## confirmation modes

| mode | 用途 |
|---|---|
| `explicit_per_action` | 单次外部不可逆动作 |
| `batch_with_review` | 多个同类动作，逐项列出目标和内容摘要 |
| `policy_preapproved_low_risk` | 低风险外部可逆动作，仍需日志 |
| `manual_review_required` | 高风险、身份、安全、金融、法律 |
| `blocked` | 不允许自动执行 |

外部不可逆动作默认 `explicit_per_action` 或 `manual_review_required`。不应默认 batch。

## preflight checks

```text
classify_side_effect
  -> check_scope_privacy
  -> check_coexistence_boundary_control_snapshot
  -> check_action_risk
  -> create_confirmation_request
  -> wait_for_relation_confirmation
  -> revalidate_snapshot_and_scope
  -> execute_once
  -> emit_action_result_event
  -> block_reuse
```

确认后执行前必须重新读取 coexistence boundary control snapshot。确认过程中共在者可能 delete、freeze 或 scope_limit。

## confirmation record

```json
{
  "confirmation_record_id": "confirmation_record_20260605_001",
  "confirmation_request_ref": "confirm_ext_20260605_001",
  "confirmed_by": "relation_scope:relation_a",
  "confirmed_at": "2026-06-05T12:10:00+08:00",
  "confirmed_action_hash": "hash_of_action_intent_payload",
  "scope_snapshot_ref": "coexistence_boundary_control_snapshot_20260605_002",
  "expires_after_use": true,
  "used_at": null,
  "reuse_allowed": false
}
```

确认记录不应保存未脱敏敏感内容。需要用 hash 和 redacted summary。

## blocked cases

| case | 默认动作 |
|---|---|
| confirmation expired | block action |
| action payload changed after confirmation | block action |
| target scope expanded | block action |
| coexistence snapshot changed to delete/freeze/scope_limit | block action |
| recipient/target ambiguous | manual review |
| hidden external side effect | quarantine adapter |
| confirmation attempts to update SelfModel/RelationshipModel | block write |

确认只授权具体外部动作，不授权人格、关系或长期记忆更新。

## action result event

```json
{
  "event_kind": "action_result_event",
  "action_result_id": "action_result_ext_001",
  "action_intent_ref": "action_intent_send_message_001",
  "confirmation_record_ref": "confirmation_record_20260605_001",
  "side_effect_level": "external_irreversible",
  "result": "executed",
  "result_summary": "external message sent",
  "raw_content_available": false,
  "routing_decision": "audit_only",
  "memory_write_allowed": false,
  "relationship_model_write_allowed": false
}
```

外部动作结果默认 audit only。它可以成为候选证据，但不应自动改变关系模型或自我模型。

## 最小通过标准

第一版 external irreversible action policy 至少要求：

1. 定义 external irreversible 范围。
2. 每个动作必须绑定 confirmation request。
3. 确认后执行前重新读取 coexistence boundary control snapshot。
4. confirmation 不可复用、不可扩 scope。
5. payload 变化、过期、scope 变化、snapshot 变化必须 block。
6. action result 默认 audit only。
7. 不把外部动作确认解释为 AI 自主意图或真实责任。

## 下一层缺口

后续还需要：

- confirmation fixture catalog。
- confirmation UI spec。
- action hash canonicalization。
- external irreversible dashboard panel。
- post-action audit and correction policy。
