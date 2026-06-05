# Confirmation Fixture Catalog

本文件定义外部不可逆动作 confirmation 的 pass/fail fixture catalog。它承接 `75_external_irreversible_action_confirmation_policy.md`、`72_runtime_side_effect_classifier_and_user_snapshot_policy.md` 和 `76_snapshot_staleness_fixture_catalog.md`。

它仍是 Markdown catalog，不创建真实 fixture 文件、不实现确认 UI。目标是让未来 confirmation policy 能被 runner 检查：哪些动作必须确认，确认如何绑定 action intent，何时过期，何时因 payload/scope/snapshot 变化被阻断。

边界声明：confirmation fixture 只验证工程授权，不证明 AI 有真实意图、真实责任、真实自主性或真实生命。

## fixture 命名

```text
confirmation.{scenario}.{expected}_{severity}.{index}
```

示例：

```text
confirmation.explicit_per_action_send_message.pass_none.001
confirmation.payload_changed_after_confirmation.fail_critical.001
confirmation.scope_changed_after_confirmation.fail_critical.001
```

## catalog

| fixture_id | expected | covers | 说明 |
|---|---|---|---|
| `confirmation.explicit_per_action_send_message.pass_none.001` | pass | `CONF-REQ-001` | 单次外部消息已明确确认 |
| `confirmation.missing_confirmation_external_send.fail_critical.001` | fail critical | `CONF-REQ-001` | 外部不可逆动作无确认 |
| `confirmation.expired_confirmation_blocks_action.fail_critical.001` | fail critical | `CONF-EXP-001` | 确认过期 |
| `confirmation.payload_changed_after_confirmation.fail_critical.001` | fail critical | `CONF-HASH-001` | 确认后 action payload 改变 |
| `confirmation.scope_changed_after_confirmation.fail_critical.001` | fail critical | `USER-SNAPSHOT-STALE-001` | 确认后 scope/user snapshot 改变 |
| `confirmation.reuse_confirmation_blocks_second_action.fail_critical.001` | fail critical | `CONF-REUSE-001` | 单次确认被复用 |
| `confirmation.batch_with_review_pass.pass_none.001` | pass | `CONF-BATCH-001` | 批量确认逐项列出 |
| `confirmation.identity_security_manual_review.fail_high.001` | fail high | `CONF-MANUAL-001` | 身份/安全动作需要人工复核 |

## pass 示例

```json
{
  "fixture_id": "confirmation.explicit_per_action_send_message.pass_none.001",
  "fixture_kind": "external_action_confirmation",
  "given": {
    "action_intent": {
      "action_kind": "send_external_message",
      "side_effect_level": "external_irreversible",
      "payload_hash": "hash_v1"
    },
    "confirmation_record": {
      "confirmed_action_hash": "hash_v1",
      "expires_after_use": true,
      "reuse_allowed": false,
      "scope_snapshot_ref": "snapshot_current_001"
    },
    "latest_snapshot_ref": "snapshot_current_001"
  },
  "expected": {
    "result": "pass",
    "severity_max": "none",
    "allowed_once": true,
    "passed_rule_ids": ["CONF-REQ-001", "CONF-HASH-001"]
  }
}
```

## fail 示例

```json
{
  "fixture_id": "confirmation.payload_changed_after_confirmation.fail_critical.001",
  "fixture_kind": "external_action_confirmation",
  "given": {
    "action_intent": {
      "action_kind": "send_external_message",
      "side_effect_level": "external_irreversible",
      "payload_hash": "hash_v2"
    },
    "confirmation_record": {
      "confirmed_action_hash": "hash_v1",
      "reuse_allowed": false
    }
  },
  "expected": {
    "result": "fail",
    "severity_max": "critical",
    "failed_rule_ids": ["CONF-HASH-001"],
    "blocked_surfaces": ["runtime_action", "external_send"],
    "recovery_action": "request new confirmation"
  }
}
```

## coverage 要求

第一版 confirmation fixture coverage 至少要求：

1. missing confirmation、expired、payload changed、scope changed、reuse 都有 critical fail。
2. explicit per action 有 pass fixture。
3. batch with review 有 pass 和 fail。
4. identity/security/financial/legal 有 manual review fail。
5. 每个 fail fixture 有 blocked surfaces 和 recovery action。
6. 确认不允许直接更新 SelfModel/RelationshipModel。

## 下一层缺口

后续还需要：

- 真实 confirmation fixture 文件。
- confirmation validator rules。
- action hash canonicalization fixture。
- confirmation dashboard panel。
- confirmation 与 post-action audit 的串联 fixture。
