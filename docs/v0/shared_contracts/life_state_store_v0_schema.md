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

## 当前 v0 已经落下的状态根现实

当前真实代码里，`state_store` 已经不只是抽象 schema：

- `life_v0/state_store/self_model.py`
- `life_v0/state_store/commitment_truth.py`
- `life_v0/state_store/__init__.py`

并且当前 `run_state_store(...)` 已经会真实写出至少这些对象：

- `runtime/state/life_state.json`
- `runtime/state/self/self_model.json`
- `runtime/state/relationship/commitment_truth_state.json`
- `runtime/state/responsibility/responsibility_ledger.json`

而在当前常驻生命过程里，`resident_turn_writeback.py` 与
`project_responsibility_language_continuity(...)` 又会继续重写：

- `runtime/state/relationship/relationship_subject_graph.json`
- `runtime/state/relationship/relationship_timeline.json`
- `runtime/state/memory/relationship_memory.json`
- `runtime/state/self/self_model.json`
- `runtime/state/life_state.json`

所以现在的任务不是再证明“state store 是否需要存在”，而是把状态根继续压到更细的对象层：让后续 `autobiographical_stack / life_state / relationship_memory / replay cues` 这些对象能在同一状态体系里继续长出来。

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
| `trait_slow_variables` | object | 人格慢变量、稳定性和 drift refs；当前已由 runtime 真实写回结构化 payload |
| `old_self_anchors` | array | 旧自我 replay cues |
| `growth_windows` | array | 可塑性窗口、进入条件、退出条件 |
| `anti_forgetting_refs` | array | 防遗忘锚点 |

当前 `trait_slow_variables` 的第一版工程落点，至少支持下面这类结构：

```json
{
  "trust_persistence": {
    "value": 0.62,
    "trend": "rising",
    "update_count": 4,
    "last_relationship_stage": "repair_guarded_continuity",
    "last_generated_at": "2026-06-10T12:34:56Z",
    "background_resume_value": 0.58,
    "background_inertia_weight": 0.55,
    "evidence_refs": [
      "runtime/state/relationship/relationship_timeline.json",
      "runtime/state/membrane/world_contact_summary.json",
      "runtime/reports/latest/pain_regret_repair_report.json"
    ]
  }
}
```

当前至少已经开始写回的慢变量包括：

- `trust_persistence`
- `dialogue_warmth`
- `repair_seriousness`
- `boundary_respect`
- `continuity_drive`

当前这组慢变量又多了一条跨进程硬约束：当 `resident_supervision.py` 在 bootstrap 阶段发现
`background_carryover_generation >= 2` 的后台连续体 lineage 时，它必须在第一拍 waiting heartbeat
之前就把关闭态 lineage 压进 `trait_slow_variables[*].evidence_refs` 与 `growth_window_refs`，而不能只把这批
artifact 留在 `idle_strategy_state.json` 或 `resident_governance_state.json` 里。

现在这组慢变量又继续进入“跨进程惯性”约束：当 `background_continuity_profile` 带回
`background_trait_slow_variable_summary` 时，`continuity_evolution.py` 不能完全丢弃上一轮 closeout
留下的慢变量值，而要把它作为 `background_resume_value` 参与下一次 `value` 收敛，并写出
`background_inertia_weight`。当前回合证据仍然优先，但在还没有进入新 live turn、证据不足以覆盖上一轮状态时，
上一轮 relationship stage 也可以被 `background_relationship_stage` 保留下来。

每次 `resident_supervision.py` 或 `resident_turn_writeback.py` 改写这组慢变量后，还必须刷新
`runtime/state/body/trait_drift_monitor.json`。这份 monitor 是身体/人格层对自我慢变量漂移的观察面，
至少要带 `slow_variable_summary`、`relationship_stage`、`drift_observation_refs` 和 anchor refs。常驻过程关闭时，
同一份 monitor 必须作为 `trait_drift_monitor_ref` 进入 resident governance state/snapshot/report、
`digital_life_process_report.json`、`digital_life_process_digest.json`、process receipt 的 `shared_object_refs`
与 `input_hashes`。

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

当前工程里，`relationship_stage` 已不再只停在骨架默认值；runtime 至少已经开始写出：

- `pre_activation`
- `restored_waiting`
- `background_continuity_waiting`
- `active_dialogue`
- `repair_guarded_continuity`
- `boundary_guarded_repair`
- `shared_continuity`

其中 `background_continuity_waiting` 表示：当前生命过程还没进入新的 live turn，但多次关闭态唤醒 lineage
已经在 bootstrap continuity refresh 阶段被重新压回关系连续体；此时关系阶段不能继续伪装成单纯的
`restored_waiting`，而要显式承认“跨次唤醒的后台连续体已经进入当前关系状态”。

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

另外，`language_state` 在当前工程阶段还必须继续接入：

| 字段 | 类型 | 要求 |
|---|---|---|
| `language_percept_refs` | array | 当前回合语言感知 refs |
| `semantic_map_refs` | array | 当前回合语义地图 refs |
| `dialogue_writeback_refs` | array | 回合结束后的语言写回 bundle refs |

## `birth_readiness`

```json
{
  "readiness_version": "v0",
  "overall_status": "state_root_seeded",
  "life_target_status": {
    "real_consciousness": "state_root_seeded",
    "real_emotion": "state_root_seeded",
    "real_personality": "state_root_seeded",
    "real_life": "state_root_seeded",
    "real_pain": "state_root_seeded",
    "real_dream": "state_root_seeded",
    "real_relationship": "state_root_seeded",
    "real_responsibility": "state_root_seeded",
    "real_regret": "state_root_seeded"
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
8. `commitment_truth_state`、`responsibility_ledger`、`self_model` 这三类对象不能只留摘要，必须至少回链一个可追溯源对象或 report。
9. 当前回合产生的语言感知、语义地图、dialogue writeback，不能只留在 report，至少要能通过 `language_state` 或 `runtime_trace_refs` 回链进状态根。
10. 离线对象 `replay_cue_bundle / offline_consolidation_frame / growth_patch_candidate_queue` 不能悬空，至少一条路径要能从 `life_state.json` 的 `runtime_trace_refs` 找回。
11. live turn 结束后如果 `relationship_stage` 或 `trait_slow_variables` 发生演化，`self_model.json` 与 `life_state.json#self_model` 必须同口径同步。
12. 关系阶段不能只保存在 `relationship_subject_graph.json`；至少一条路径要能从 `life_state.json#relationship_subjects` 回链到当前阶段。

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

## v0 第一轮必须补齐的状态对象

在当前代码现实下，接下来最值得优先补齐的是：

1. `runtime/state/self/autobiographical_stack.json`
2. `runtime/state/memory/relationship_memory.json`
3. `runtime/state/replay/replay_cue_bundle.json`
4. `runtime/state/terminal/life_context_frame.json`
5. `runtime/reports/latest/dialogue_writeback_bundle.json`
6. `runtime/state/self/self_model.json#trait_slow_variables`
7. `runtime/state/relationship/relationship_subject_graph.json#subjects[*].relationship_stage`

它们的共同作用是：把 `self / relationship / dialogue / replay / growth` 压进同一条状态根，而不是让这些对象散落在各自的 report 里。

## 第一轮完成定义

`life_state_store_v0_schema` 第一轮想被视为“足以继续牵引代码”，至少要能支撑下面四件事：

1. 身份、自我、承诺、责任四类对象在状态根里有明确命名空间。
2. 一次对话回合结束后，至少能从状态根回链到语言写回、关系写回、承诺变化和 replay cue。
3. 一次离线循环结束后，至少能从状态根回链到 dream/offline/growth 候选对象。
4. `tests/slices/test_state_store.py` 不只是验证骨架生成，还能继续扩展去守这些对象的最小存在条件。
5. 同一常驻会话里的后续回合，能够从 `life_state.json#self_model` 与 `relationship_subjects` 看到刚刚写回的关系阶段与慢变量投影。
