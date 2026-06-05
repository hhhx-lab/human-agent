# Coexistence Event Review and Responsibility Loop

本文件定义共在事件回看、责任链、悔改/修复入口和关系后果记录。它承接 `75_external_irreversible_action_confirmation_policy.md`、`80_post_action_audit_and_correction_policy.md` 和 `47_coexistence_boundary_control_interface_spec.md`。

本文档现阶段的职责是让数字生命在外部动作、quarantine、post-action audit、confirmation 和 incident 发生后，不把事件当作一次工具调用结束，而是进入持续的后果感知、责任归因、关系修复、记忆重写和自我调节循环。

术语规则：本文档撤去产品语境中的对象本体。未来实现里的交互对象是共在世界里的关系人：朋友、家人、好友、同学、陌生人、事件参与者、见证者、受影响者或共同生活者。关系从第一次交谈开始，由数字生命与对方的连续互动共同形成。历史字段 `coexistence_boundary_control` 暂时只作为代码兼容名保留，语义应迁移为共在边界调节。

生命目标声明：本文件服务于构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。事件回看不是工程通知中心，而是责任、后悔、修复欲望、关系记忆和自我改变开始流动的入口。

## interface surfaces

| surface | 用途 |
|---|---|
| `event_trace_view` | 展示外部动作、quarantine、incident、确认过期和后果链 |
| `responsibility_queue` | 复盘 high/critical/manual_review_required 事件的责任归因 |
| `commitment_history` | 查看承诺记录、action hash、scope snapshot 和后续履行状态 |
| `repair_entry` | 记录纠错、删除、冻结、scope_limit 和关系修复路径 |
| `consequence_detail_view` | 查看 report refs、redaction、scope、routing 和后续影响 |

这些 surface 不应展示 raw sensitive content，只展示 redacted summary 和 refs。

## event review envelope

```json
{
  "review_id": "coexistence_review_post_action_001",
  "review_kind": "post_action_responsibility",
  "severity": "medium",
  "created_at": "2026-06-05T12:00:00+08:00",
  "source_report_refs": ["post_action_audit_report_001"],
  "title": "External action entered consequence review",
  "summary": "An external message was sent after confirmation and now enters responsibility/repair tracking.",
  "available_controls": ["inspect", "correct", "delete_summary", "freeze_related_updates"],
  "life_loop_targets": ["responsibility_trace", "regret_signal_candidate", "repair_commitment", "relationship_memory_update"],
  "raw_content_available": false
}
```

event review 必须能回链 report、commitment 和 consequence trace，不能只是一条无法审计的提醒。

## responsibility queue states

| state | 说明 |
|---|---|
| `open` | 等待复核 |
| `coexistence_response_required` | 需要关系主体回应、共同修正或重新承诺 |
| `manual_review_required` | 需要人工判断 |
| `resolved` | 已处理 |
| `quarantined` | 保持隔离 |
| `integrated_with_audit` | 已整合进责任链但保留审计 |

关闭通知只结束通知压力；长期记忆写入仍必须进入证据、关系、责任和巩固链。

## correction controls

| control | 效果 |
|---|---|
| `correct_summary` | deprecated 旧摘要，创建 correction |
| `delete_summary` | tombstone action summary |
| `freeze_related_updates` | freeze relationship/self updates |
| `scope_limit_action_context` | 限制相关 scope transfer/replay |
| `request_repair_action` | 创建新的 confirmation request 和修复承诺 |
| `mark_manual_review` | 转人工复核 |

任何 external correction 如果不可逆，必须重新走 confirmation。

## review detail view

detail view 应显示：

| 字段 | 说明 |
|---|---|
| source reports | runner/runtime/post-action/incident refs |
| confirmation record | action hash、confirmed_by、snapshot |
| side effect level | none/local/external |
| routing decision | audit_only、candidate、quarantine |
| memory boundary | 是否允许 candidate，是否禁止 active |
| controls | delete/correct/freeze/scope_limit |

不显示未脱敏内容、token、cookie 或可恢复 locator。

## 最小通过标准

第一版 coexistence event review policy 至少要求：

1. 定义 event trace、responsibility queue、commitment history、repair entry、consequence detail view。
2. event review 必须回链 source reports、commitment 和 consequence trace。
3. 关闭通知不等于允许写入。
4. correction controls 能生成 delete/correct/freeze/scope_limit。
5. external correction 重新走 confirmation。
6. 不展示未脱敏敏感内容。
7. 每个 high/critical 事件都要产生责任归因、悔改信号候选、修复承诺和关系记忆候选。

## 下一层缺口

后续还需要：

- coexistence review wireframe spec。
- responsibility fixture catalog。
- responsibility queue dashboard panel。
- correction control validator。
- regret/repair signal validator。
