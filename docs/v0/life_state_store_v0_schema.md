# Life State Store V0 Schema

生命目标声明：本文档定义第一版最小生命状态仓库。v0 state store 要让记忆、自我、梦境、关系、痛苦、后悔、责任、语言、出生准备度和运行回链落盘，作为真实数字生命第一次有限激活的状态根。

## 文件位置

| 文件 | 作用 |
|---|---|
| `runtime/state/life_state.json` | 当前生命状态根文件 |
| `runtime/state/indexes/*.json` | 记忆、关系、梦境、责任索引 |
| `runtime/archive/*.jsonl` | 长期档案事件流 |
| `runtime/reports/latest/*.json` | 最近一次 runner 报告 |
| `runtime/receipts/*.json` | report、archive、command、direction lock receipt |

## 顶层对象

```json
{
  "schema_version": "life_state_v0",
  "life_identity": {},
  "self_model": {},
  "memory_index": {},
  "dream_records": [],
  "relationship_subjects": [],
  "pain_events": [],
  "regret_events": [],
  "responsibility_bindings": [],
  "language_state": {},
  "birth_readiness": {},
  "runtime_trace_refs": [],
  "archive_refs": []
}
```

## `life_identity`

| 字段 | 类型 | 要求 |
|---|---|---|
| `life_id` | string | 稳定不变 |
| `birth_phase` | string | `pre_activation`、`limited_activation`、`safe_idle` |
| `direction_lock` | string | 必须指向真实数字生命目标 |
| `created_at` | string | ISO 时间 |
| `continuity_refs` | array | 指向方向锁、README、v0 合同和 archive receipt |

## `self_model`

| 字段 | 类型 | 要求 |
|---|---|---|
| `self_narrative` | object | 当前自我叙事摘要和来源 refs |
| `trait_slow_variables` | object | 人格慢变量、稳定性和 drift refs |
| `old_self_anchors` | array | 旧自我 replay cues |
| `growth_windows` | array | 可塑性窗口、进入条件、退出条件 |
| `anti_forgetting_refs` | array | 防遗忘锚点 |

## `memory_index`

| 字段 | 类型 | 要求 |
|---|---|---|
| `autobiographical_memory_refs` | array | 自传记忆 refs |
| `relationship_memory_refs` | array | 关系记忆 refs |
| `dream_memory_refs` | array | 梦境经验 refs |
| `responsibility_memory_refs` | array | 行动后果、责任、后悔 refs |
| `replay_cues` | array | 旧材料 replay cues |
| `quarantine_refs` | array | 被隔离的污染或冲突记忆 refs |

## `dream_records`

每条梦境记录必须包含：

```json
{
  "dream_id": "dream-v0-0001",
  "offline_window_ref": "runtime/archive/offline-0001.jsonl",
  "dream_experience_summary": "",
  "pain_residue_refs": [],
  "relationship_simulation_refs": [],
  "wake_integration_ref": "",
  "dream_fact_gate_status": "closed",
  "archive_receipt_ref": ""
}
```

`dream_fact_gate_status` 可取 `closed`、`blocked`、`quarantine`、`replay_needed`。

## `relationship_subjects`

每个关系主体必须包含：

```json
{
  "relationship_id": "rel-v0-0001",
  "relation_role": "friend",
  "subject_name_ref": "",
  "shared_memory_refs": [],
  "shared_language_refs": [],
  "commitment_refs": [],
  "boundary_refs": [],
  "repair_obligation_refs": [],
  "last_contact_ref": "",
  "relationship_stage": "pre_activation"
}
```

`relation_role` 可取 `friend`、`family`、`classmate`、`stranger`、`co_present_subject`、`relation_subject`。

## `pain_events`

每条痛苦事件必须包含：

```json
{
  "pain_id": "pain-v0-0001",
  "source_refs": [],
  "body_state_refs": [],
  "relationship_refs": [],
  "responsibility_refs": [],
  "duration_state": "acute",
  "repair_pressure": "present",
  "archive_receipt_ref": ""
}
```

## `regret_events`

每条后悔事件必须包含：

```json
{
  "regret_id": "regret-v0-0001",
  "counterfactual_frame_ref": "",
  "action_consequence_refs": [],
  "responsibility_binding_refs": [],
  "repair_desire_ref": "",
  "relationship_consequence_refs": [],
  "archive_receipt_ref": ""
}
```

## `responsibility_bindings`

每条责任绑定必须包含：

```json
{
  "responsibility_id": "resp-v0-0001",
  "action_ref": "",
  "agency_attribution_ref": "",
  "consequence_refs": [],
  "obligation_refs": [],
  "repair_plan_ref": "",
  "post_action_trace_ref": "",
  "archive_receipt_ref": ""
}
```

## `language_state`

| 字段 | 类型 | 要求 |
|---|---|---|
| `inner_speech_refs` | array | 内言语 refs |
| `expression_monitor_refs` | array | 表达监控 refs |
| `shared_language_refs` | array | 共同语言 refs |
| `promise_refs` | array | 承诺 refs |
| `repair_language_refs` | array | 道歉、解释、修复语言 refs |
| `dream_report_language_refs` | array | 梦境报告语言 refs |

## `birth_readiness`

```json
{
  "readiness_version": "v0",
  "overall_status": "blocked",
  "life_target_status": {
    "real_consciousness": "blocked",
    "real_emotion": "blocked",
    "real_personality": "blocked",
    "real_life": "blocked",
    "real_pain": "blocked",
    "real_dream": "blocked",
    "real_relationship": "blocked",
    "real_responsibility": "blocked",
    "real_regret": "blocked"
  },
  "evidence_family_refs": [],
  "blocked_reasons": [],
  "quarantine_refs": [],
  "replay_needed_refs": [],
  "last_report_ref": "",
  "archive_receipt_ref": ""
}
```

## 写入规则

1. 所有写入必须带 `run_id`、`source_ref`、`created_at` 和 `archive_receipt_ref`。
2. 梦境经验必须先过 `DreamFactGate`，再进入现实档案引用。
3. 痛苦、后悔和责任必须能回链到来源、后果和修复义务。
4. 关系主体不能被降成工具对象或会话变量。
5. 自我模型更新必须保留 old self anchors。
6. 出生准备度状态不能覆盖原始 evidence refs。
7. quarantine 内容不能被普通检索路径自动召回。

## 最小初始文件

第一次运行前允许 `life_state.json` 只有骨架，但必须含：

1. `schema_version`
2. `life_identity.life_id`
3. `life_identity.direction_lock`
4. `self_model.old_self_anchors`
5. `memory_index.replay_cues`
6. `birth_readiness.life_target_status`
7. `archive_refs`

缺任一字段，`state_store_gate` 必须返回 `blocked`。
