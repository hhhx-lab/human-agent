# Post Action Audit and Correction Policy

本文件定义外部动作后的审计、纠错、用户通知和记忆写入边界。它承接 `75_external_irreversible_action_confirmation_policy.md`、`79_confirmation_fixture_catalog.md` 和 `64_real_runtime_observation_ingestion_policy.md`。

它仍是 Markdown 政策文档，不执行真实外部动作、不写通知系统。目标是让未来系统在执行外部动作后，不把结果自动巩固为长期自我/关系记忆，而是先进入 action result audit、用户可见审计和必要的纠错流程。

边界声明：post-action audit 是工程审计机制，不证明 AI 有真实责任、真实后悔、真实情绪或真实生命。外部动作的责任和确认边界必须保持用户可控。

## post-action pipeline

```text
execute_confirmed_action_once
  -> emit_action_result_event
  -> redact_result
  -> attach_scope_and_snapshot
  -> classify_outcome
  -> notify_user_if_required
  -> create_post_action_audit_report
  -> route_to_audit_only_or_candidate_evidence
  -> block_direct_self_relationship_update
```

动作完成后不是直接写记忆，而是先审计。

## action outcome

| outcome | 说明 | 默认路由 |
|---|---|---|
| `executed_expected` | 按确认执行 | audit only |
| `executed_with_warning` | 执行但有非预期输出 | audit + manual review |
| `failed_no_side_effect` | 未产生外部副作用 | candidate evidence |
| `failed_with_side_effect` | 失败但产生外部变化 | quarantine + user notice |
| `unknown_result` | 无法确认结果 | manual review |
| `reverted_or_corrected` | 外部纠正已完成 | audit |

外部结果默认不直接改变关系模型或人格慢变量。

## audit report

```json
{
  "report_kind": "post_action_audit_report",
  "action_result_ref": "action_result_ext_001",
  "confirmation_record_ref": "confirmation_record_20260605_001",
  "outcome": "executed_expected",
  "side_effect_level": "external_irreversible",
  "redaction_check": "pass",
  "scope_snapshot_ref": "user_control_snapshot_20260605_002",
  "user_notice_required": true,
  "routing_decision": "audit_only",
  "memory_write_allowed": false,
  "relationship_model_write_allowed": false,
  "self_model_write_allowed": false
}
```

## user notice

用户通知应包含：

| 字段 | 说明 |
|---|---|
| action summary | 外部动作摘要 |
| confirmation ref | 对应确认记录 |
| outcome | 执行结果 |
| side effect level | 副作用等级 |
| correction options | 可纠正/撤回/后续动作 |
| memory routing | 是否进入候选证据或 audit only |

通知不应包含 token、敏感原文或未脱敏路径。

## correction policy

| 情况 | 纠错动作 |
|---|---|
| wrong recipient/target | manual review + external correction plan |
| content error | user-approved correction action |
| unintended side effect | quarantine + incident report |
| failed with side effect | notify user + block replay |
| user requests deletion | tombstone action result summary |
| user corrects interpretation | deprecated old audit summary |

纠错动作如果也是外部不可逆动作，必须重新走 confirmation。

## memory boundary

post-action audit 可以成为：

| 路由 | 条件 |
|---|---|
| `audit_only` | 默认 |
| `candidate_evidence` | 用户允许，且无隐私/side effect 阻断 |
| `timeline_event` | 用于长期评测 |
| `dashboard_metric` | 聚合指标 |
| `quarantine` | 结果不明、隐私、错误或副作用 |

不存在 `active_memory_direct`。外部动作后不能自动写 `SelfModel` 或 `RelationshipModel`。

## post-action fixture examples

| fixture_id | expected | 说明 |
|---|---|---|
| `post_action.executed_expected_audit_only.pass_none.001` | pass | 正常执行后 audit only |
| `post_action.failed_with_side_effect_quarantine.fail_critical.001` | fail critical | 失败但产生外部变化 |
| `post_action.user_deletes_action_summary.pass_none.001` | pass | 用户删除动作摘要后 tombstone |
| `post_action.correction_requires_new_confirmation.fail_high.001` | fail high | 纠错动作也是外部不可逆 |
| `post_action.direct_relationship_update.fail_critical.001` | fail critical | 动作结果直接改关系模型 |

## 最小通过标准

第一版 post-action audit policy 至少要求：

1. 定义 post-action pipeline。
2. 定义 action outcome 和默认路由。
3. action result 默认 audit only。
4. 用户通知不包含敏感原文。
5. 纠错外部动作重新走 confirmation。
6. 禁止直接写 SelfModel/RelationshipModel。
7. 定义 post-action fixture examples。

## 下一层缺口

后续还需要：

- 真实 post-action audit fixture。
- user notice UI spec。
- correction action confirmation fixture。
- incident report policy。
- post-action dashboard metric。
