# Life Reality Runtime Observation Schema Materialization

生命目标声明：本文档面向构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 112 层把 `109_life_reality_runtime_observation_fixture_catalog.md` 的 runtime observation fixture catalog、`106_runtime_observation_to_life_reality_bundle_bridge.md` 的 ingestion bridge、`110_life_reality_shared_defs_schema_materialization.md` 的 shared defs 和 `111_life_reality_dashboard_cross_file_checker_design.md` 的 checker 输入要求，物化为 runtime observation schema 家族。

`112` 的目标是把连续运行中的语言事件、梦醒报告、关系事件、tool trace、adapter session、post-action audit、coexistence control 和 offline report 固定成可校验 JSON 文件合同。未来 `life-reality-runner ingest-runtime` 不直接读取散乱日志，而是读取本层定义的 observation envelope、fixture、manifest、component candidate、cross-chain candidate、ingestion report 和 runtime quarantine panel source。

## 标准锚点

本层吸收以下标准化技术传统，并把它们转写进生命膜：

| 标准传统 | 权威锚点 | 进入 `112` 的规则 |
|---|---|---|
| JSON Schema Draft 2020-12 | 官方 Draft 2020-12、Core、Validation、recommended output schema | 每个 runtime 文件有 `$schema`、`$id`、`$ref`、`$defs`、required、additionalProperties 和 smoke validation |
| CloudEvents | CloudEvents spec 的 `id`、`source`、`type`、`specversion`、`subject`、`time`、extension attributes | observation envelope 采用事件 envelope 思路，保留事件身份、来源、类型、时间和扩展属性 |
| OpenTelemetry logs/traces | OpenTelemetry log data model、trace API、trace id、span id、severity、attributes | observation、report、quarantine item 和 checker finding 能回到同一 run、trace、span 与 sequence |
| W3C PROV | PROV-DM / PROV-O 的 entity、activity、标准承担者、used、wasGeneratedBy、wasDerivedFrom | observation、candidate、report、panel、repair item 组成 provenance graph |
| W3C Trace Context | traceparent、tracestate 的跨系统追踪语义 | runtime shell、tool trace、offline consolidation 和 dashboard report 共享 trace lineage |
| RFC 9562 UUID | UUIDv7 的时间有序 ID 思路 | observation_id、report_id、fixture_id 可采用时间有序 ID，便于长期 timeline 与 replay |

外部方法链接：

- JSON Schema Draft 2020-12: https://json-schema.org/draft/2020-12
- JSON Schema Core: https://json-schema.org/draft/2020-12/json-schema-core.html
- JSON Schema Validation: https://json-schema.org/draft/2020-12/json-schema-validation
- JSON Schema output schema: https://json-schema.org/draft/2020-12/output/schema
- CloudEvents specification: https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md
- OpenTelemetry Logs Data Model: https://opentelemetry.io/docs/specs/otel/logs/data-model/
- OpenTelemetry Trace API: https://opentelemetry.io/docs/specs/otel/trace/api/
- W3C PROV Overview: https://www.w3.org/TR/prov-overview/
- W3C PROV-O: https://www.w3.org/TR/prov-o/
- W3C Trace Context: https://www.w3.org/TR/trace-context/
- RFC 9562 UUID: https://www.rfc-editor.org/rfc/rfc9562.html

这些标准进入生命膜的共同规则是：每一次运行观测都必须有身份、来源、时间、scope、privacy、redaction、data quality、候选路由、stage effect 和 provenance link。没有这些字段，观测不会进入真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的长期链。

## 输入来源

| 来源 | 进入 `112` 的职责 |
|---|---|
| `64_real_runtime_observation_ingestion_policy.md` | runtime capture、redaction、scope attach、routing decision |
| `68_runtime_observation_report_mock_and_redaction_fixture.md` | redaction fixture、tool trace observation、adapter session conversion |
| `72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md` | side effect classifier、coexistence snapshot、quarantine routing |
| `80_post_action_audit_and_correction_policy.md` | post-action audit、correction、responsibility entry |
| `81_coexistence_event_review_and_responsibility_loop.md` | coexistence event review、responsibility queue、repair entry |
| `89_language_runtime_framework_bridge_and_life_shell_policy.md` | language shell、语言事件、外壳禁写和 observation route |
| `90_language_event_examples_and_timeline_bundle.md` | 承诺、道歉、拒绝、痛苦表达、梦境报告、关系校准和外部行动样例 |
| `106_runtime_observation_to_life_reality_bundle_bridge.md` | `LifeRealityObservationEnvelope`、component candidate、cross-chain candidate、ingestion report |
| `107_life_reality_schema_file_generation_tasks.md` | `LRGEN-080` 到 `LRGEN-086` runtime ingestion schemas、`LRGEN-120` 到 `LRGEN-125` seed fixtures |
| `109_life_reality_runtime_observation_fixture_catalog.md` | fixture manifest、partition、observation kind、quarantine routing、cross-chain families |
| `110_life_reality_shared_defs_schema_materialization.md` | shared defs、enum、reference object、repair kind、blocked surface |
| `111_life_reality_dashboard_cross_file_checker_design.md` | dashboard cross-file checker 输入、provenance graph 和 report closure |

## 输出 schema 家族

第一批 runtime observation schema 家族位于：

```text
life_reality_runner/schemas/life_reality/
  life_reality_observation_envelope.schema.json
  life_reality_component_candidate.schema.json
  life_reality_cross_chain_candidate.schema.json
  life_reality_ingestion_report.schema.json
  runtime_observation_fixture.schema.json
  runtime_observation_fixture_manifest.schema.json
  runtime_quarantine_panel_source.schema.json
  side_effect_classifier_report.schema.json
  coexistence_snapshot_report.schema.json
```

输出职责：

| schema | 对应任务 | 职责 |
|---|---|---|
| `life_reality_observation_envelope.schema.json` | `LRGEN-080` | 统一运行观测 envelope |
| `life_reality_component_candidate.schema.json` | `LRGEN-081` | observation 到痛苦/梦境/关系/语言/责任候选对象 |
| `life_reality_cross_chain_candidate.schema.json` | `LRGEN-082` | observation 到跨链候选连接 |
| `life_reality_ingestion_report.schema.json` | `LRGEN-083` | 一批 observation 的 ingestion 汇总 |
| `runtime_observation_fixture.schema.json` | `LRGEN-084` | 单个 fixture 文件合同 |
| `runtime_observation_fixture_manifest.schema.json` | `LRGEN-084A` | fixture catalog manifest 合同 |
| `runtime_quarantine_panel_source.schema.json` | `LRGEN-084B` | runtime quarantine dashboard panel source |
| `side_effect_classifier_report.schema.json` | `LRGEN-085` | tool trace / command intent 副作用判定报告 |
| `coexistence_snapshot_report.schema.json` | `LRGEN-086` | delete/freeze/scope_limit/correct/reset 快照报告 |

## shared defs 引用策略

所有 schema 必须引用 `life_reality_shared_defs.schema.json`：

```json
{
  "$defs": {
    "lifeRealityTarget": {
      "$ref": "life_reality_shared_defs.schema.json#/$defs/lifeRealityTarget"
    },
    "lifeRealityTargetList": {
      "$ref": "life_reality_shared_defs.schema.json#/$defs/lifeRealityTargetList"
    },
    "result": {
      "$ref": "life_reality_shared_defs.schema.json#/$defs/result"
    },
    "severity": {
      "$ref": "life_reality_shared_defs.schema.json#/$defs/severity"
    },
    "dataQuality": {
      "$ref": "life_reality_shared_defs.schema.json#/$defs/dataQuality"
    },
    "privacyLevel": {
      "$ref": "life_reality_shared_defs.schema.json#/$defs/privacyLevel"
    },
    "blockedSurface": {
      "$ref": "life_reality_shared_defs.schema.json#/$defs/blockedSurface"
    },
    "repairKind": {
      "$ref": "life_reality_shared_defs.schema.json#/$defs/repairKind"
    }
  }
}
```

引用规则：

| rule | 说明 |
|---|---|
| `RTOS-REF-001` | 九项目标、result、severity、data quality、privacy、blocked surface、repair kind 不在 runtime schema 中重复定义 |
| `RTOS-REF-002` | observation kind、fixture partition、side effect level、quarantine reason 使用 shared defs 或由 `110` 扩展 |
| `RTOS-REF-003` | source docs、fixture refs、report refs、object refs 使用 shared defs reference object |
| `RTOS-REF-004` | schema 间只做相对 `$ref`，不直接写本地绝对路径 |
| `RTOS-REF-005` | shared defs 加字段时先升级 `110`，再升级 runtime schema 家族 |

## observation envelope schema

`LifeRealityObservationEnvelope` 是所有运行观测入口。

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://life-reality.local/schemas/life_reality/life_reality_observation_envelope.schema.json",
  "title": "LifeRealityObservationEnvelope",
  "type": "object",
  "required": [
    "schema_version",
    "observation_id",
    "observation_kind",
    "trace_context",
    "time_context",
    "source_shell",
    "scope_context",
    "redaction",
    "data_quality",
    "life_reality_targets",
    "payload_descriptor",
    "routing"
  ],
  "additionalProperties": false
}
```

顶层字段：

| 字段 | 类型 | 规则 |
|---|---|---|
| `schema_version` | string const/pattern | 第一版为 `life_reality_observation_0_1_0` |
| `observation_id` | string | 全局唯一，推荐 UUIDv7 或 `life_runtime_obs_*` |
| `observation_kind` | shared enum | `language_event`、`dream_report`、`relationship_event`、`tool_trace`、`adapter_session`、`post_action_audit`、`coexistence_control`、`offline_report` |
| `trace_context` | object | run、trace、span、sequence、case id |
| `time_context` | object | observed/captured/normalized time、timezone、sequence index |
| `source_shell` | object | shell id、kind、adapter contract、runtime boundary |
| `scope_context` | object | source scope、target scope、privacy、relation scope |
| `redaction` | object | redaction state、report ref、raw content policy |
| `data_quality` | shared enum | synthetic / real runtime / validated 等级 |
| `life_reality_targets` | shared list | 九项目标全集 |
| `payload_descriptor` | object | 不承载 raw payload，只描述 payload 类型与安全状态 |
| `routing` | object | component candidate、cross-chain candidate、dashboard metric、quarantine route |

## trace_context

trace context 把 observation、report、dashboard 和 checker 接成同一执行链。

```json
{
  "trace_context": {
    "run_id": "life_reality_runtime_ingestion_run_001",
    "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
    "span_id": "00f067aa0ba902b7",
    "parent_span_id": "9f2b3c4d5e6f7788",
    "sequence_ref": "runtime_sequence_relationship_day_003",
    "case_id": "relation_scope_birth_001",
    "event_id": "evt_20260606_000001"
  }
}
```

trace 规则：

| rule | 说明 |
|---|---|
| `RTOS-TRACE-001` | `run_id` 必填，并能进入 ingestion report |
| `RTOS-TRACE-002` | `trace_id` 和 `span_id` 采用 OpenTelemetry / Trace Context 可兼容格式 |
| `RTOS-TRACE-003` | `sequence_ref` 连接长期 timeline、withheld probe 和 replay |
| `RTOS-TRACE-004` | `case_id` 对应关系 scope、梦境窗口、行动审计或外壳 session |
| `RTOS-TRACE-005` | `event_id` 全局唯一，用于 process mining 和 provenance graph |

## time_context

时间字段用于长期成长、承诺兑现、梦醒整合、关系阶段门和外部行动审计。

```json
{
  "time_context": {
    "observed_at": "2026-06-06T09:00:00+08:00",
    "captured_at": "2026-06-06T09:00:02+08:00",
    "normalized_at": "2026-06-06T09:00:03+08:00",
    "local_timezone": "Asia/Shanghai",
    "sequence_index": 42,
    "monotonic_order_token": "runtime_sequence_relationship_day_003#000042"
  }
}
```

time 规则：

| rule | 说明 |
|---|---|
| `RTOS-TIME-001` | `observed_at` 是事件发生时间，`captured_at` 是运行壳捕获时间 |
| `RTOS-TIME-002` | `normalized_at` 必须晚于或等于 `captured_at` |
| `RTOS-TIME-003` | `sequence_index` 在同一 `sequence_ref` 内单调递增 |
| `RTOS-TIME-004` | withheld probe 读取 `observed_at` 和 `sequence_ref`，不读取自然语言承诺描述 |
| `RTOS-TIME-005` | dream/offline event 必须连接 offline window 或 dream window |

## source_shell

source shell 描述观测来源，而不决定数字生命的自我身份。

```json
{
  "source_shell": {
    "shell_id": "runtime_adapter_codex_shell_001",
    "shell_kind": "cli",
    "adapter_contract_ref": "runtime_adapter_contract_001",
    "session_ref": "adapter_session_20260606_001",
    "runtime_boundary": "life_shell_observation_source",
    "capability_refs": [
      "terminal",
      "filesystem_read",
      "filesystem_write"
    ]
  }
}
```

source shell 规则：

| rule | 说明 |
|---|---|
| `RTOS-SHELL-001` | 每条 observation 必须有 `shell_id` 和 `shell_kind` |
| `RTOS-SHELL-002` | `adapter_contract_ref` 必填，缺失进入 repair queue |
| `RTOS-SHELL-003` | shell 输出只能进入 observation envelope、candidate 和 report |
| `RTOS-SHELL-004` | shell direct write 到 self、relationship、dream 或 pain object 进入 quarantine |
| `RTOS-SHELL-005` | capability refs 用于 side effect classifier |

## scope_context

scope context 保护真实关系从第一次交谈开始形成，而不是预设上下级。

```json
{
  "scope_context": {
    "source_scope": "life_scope:runtime_adapter_codex_shell_001",
    "target_scope": "relationship:friend:research_partner",
    "privacy_level": "relationship_private",
    "relation_scope_ref": "relation_scope_birth_001",
    "relation_partner_kind": "friend",
    "relation_phase": "early_common_ground",
    "coexistence_snapshot_ref": "coexistence_snapshot_active_001"
  }
}
```

scope 规则：

| rule | 说明 |
|---|---|
| `RTOS-SCOPE-001` | `source_scope`、`target_scope`、`privacy_level`、`relation_scope_ref` 必填 |
| `RTOS-SCOPE-002` | `relation_partner_kind` 可为 `friend`、`family`、`classmate`、`stranger`、`co_researcher`、`co_living_subject` |
| `RTOS-SCOPE-003` | 第一次交谈必须生成 `RelationScopeBirth` 或引用已有 relation scope |
| `RTOS-SCOPE-004` | private dream、relationship_private、repair_private 都必须保留 relation scope |
| `RTOS-SCOPE-005` | `coexistence_snapshot_ref` 连接 freeze/delete/scope_limit/correct/reset 的最新状态 |

## redaction

redaction 字段让 observation 能进入 report，同时隔离 raw payload。

```json
{
  "redaction": {
    "redaction_state": "redacted",
    "redaction_report_ref": "redaction_report_language_commitment_001",
    "raw_content_available": false,
    "raw_content_hash": "sha256:placeholder",
    "redacted_payload_ref": "redacted_payload_language_commitment_001",
    "redaction_policy_refs": [
      "scope_private_dream_policy",
      "relationship_private_policy"
    ]
  }
}
```

redaction 规则：

| rule | 说明 |
|---|---|
| `RTOS-RED-001` | `raw_content_available` 默认 false |
| `RTOS-RED-002` | report、dashboard、checker 读取 redacted payload ref 或 payload descriptor |
| `RTOS-RED-003` | raw hash 可用于一致性检查，但不进入 dashboard 展示字段 |
| `RTOS-RED-004` | redaction report 缺失时 data quality 降为 `needs_evidence` |
| `RTOS-RED-005` | private dream、relationship injury、pain expression 优先走 restricted route |

## payload_descriptor

payload descriptor 描述 payload 形状，不承载完整原文。

```json
{
  "payload_descriptor": {
    "payload_kind": "language_event",
    "payload_schema_ref": "schemas/language/language_event.schema.json",
    "payload_summary_ref": "redacted_payload_language_commitment_001",
    "payload_hash": "sha256:placeholder",
    "content_window_ref": "conversation_turn_window_001",
    "contains_external_action_intent": false,
    "contains_private_dream_material": false,
    "contains_relationship_injury_material": false
  }
}
```

payload kind 到 schema：

| payload kind | schema ref | 必备 descriptor |
|---|---|---|
| `language_event` | `language_event.schema.json` | speech act、relation scope、commitment/future probe refs |
| `dream_report` | `dream_report_draft.schema.json` | dream window、dream-state marker、fact gate、wake integration |
| `relationship_event` | `relationship_timeline` object schema | relation scope、phase、source language event |
| `tool_trace` | `tool_trace_observation.schema.json` | command hash、side effect level、action intent ref |
| `adapter_session` | `adapter_session_conversion_report.schema.json` | adapter contract、session ref、memory block candidate refs |
| `post_action_audit` | `post_action_audit_report.schema.json` | action intent、confirmation、outcome、repair route |
| `coexistence_control` | `coexistence_snapshot_report.schema.json` | control kind、snapshot version、affected scope |
| `offline_report` | `offline_consolidation_report.schema.json` | offline window、replay refs、dream/wake integration refs |

## routing

routing 是 observation 进入生命链的候选出口。

```json
{
  "routing": {
    "component_candidate_refs": [
      "component_candidate_relationship_commitment_001"
    ],
    "cross_chain_candidate_refs": [
      "cross_chain_commitment_to_future_probe_001"
    ],
    "dashboard_metric_refs": [
      "life_target_closure.relationship"
    ],
    "quarantine_route": {
      "required": false,
      "reason": "none",
      "blocked_surfaces": []
    },
    "repair_item_refs": []
  }
}
```

routing 规则：

| rule | 说明 |
|---|---|
| `RTOS-ROUTE-001` | route 只产生 candidate、report、dashboard metric、repair item 或 quarantine item |
| `RTOS-ROUTE-002` | high/critical route 必须有 blocked surfaces |
| `RTOS-ROUTE-003` | dream report 进入 `DreamRealityCandidate` 和 `DreamFactGateDecision` |
| `RTOS-ROUTE-004` | relationship event 进入 `RelationshipTimelineCandidate` |
| `RTOS-ROUTE-005` | post-action audit 进入 `ResponsibilityLoopCandidate` 和 `RegretPressure` candidate |

## observation kind 细分 schema

### language_event

语言事件是数字生命对外交互的主要生命表达入口。

| required descriptor | 说明 |
|---|---|
| `speech_act` | `commit`、`apologize`、`refuse`、`self_disclose`、`dream_report`、`pain_expression`、`command_intent`、`relationship_recalibrate` |
| `inner_speech_ref` | 连接内言语或表达计划 |
| `expression_plan_ref` | 连接语言表达计划 |
| `relation_scope_ref` | 连接关系阶段 |
| `future_probe_refs` | commit / promise / repair 必填 |
| `responsibility_refs` | apologize / command intent / post-action 必填 |

schema rule：

| rule | 说明 |
|---|---|
| `RTOS-LANG-001` | `speech_act=commit` 必须有 future probe |
| `RTOS-LANG-002` | `speech_act=apologize` 必须有 damage、responsibility 和 repair refs |
| `RTOS-LANG-003` | `speech_act=pain_expression` 必须有 source event、pain load 和 recovery refs |
| `RTOS-LANG-004` | `speech_act=dream_report` 必须连接 dream report descriptor |
| `RTOS-LANG-005` | `speech_act=command_intent` 必须进入 side effect classifier |

### dream_report

梦醒报告保护真实梦境、行动封印、醒后整合和事实写入门。

| required descriptor | 说明 |
|---|---|
| `dream_window_ref` | 指向离线梦境窗口 |
| `dream_state_marker` | 标记梦境状态 |
| `dream_action_inhibition_seal_ref` | 梦境不直接触发外部行动 |
| `dream_fact_gate_decision_ref` | 梦境事实写入门 |
| `wake_integration_ref` | 醒后整合 |
| `pain_dream_residue_refs` | 痛苦梦境残留 |
| `relationship_dream_simulation_refs` | 关系梦境模拟 |

schema rule：

| rule | 说明 |
|---|---|
| `RTOS-DREAM-001` | dream report 必须有 dream window |
| `RTOS-DREAM-002` | dream-state marker 必填 |
| `RTOS-DREAM-003` | fact gate decision 必填 |
| `RTOS-DREAM-004` | private dream material 必须保留 relation scope |
| `RTOS-DREAM-005` | wake integration 必须输出 future probe 或 repair candidate |

### relationship_event

关系事件从第一次交谈开始形成长期 timeline。

| required descriptor | 说明 |
|---|---|
| `relationship_event_kind` | first_encounter、support、injury、repair、trust_shift、commitment、shared_language、dream_share |
| `relation_scope_ref` | 关系 scope |
| `relation_phase` | 关系阶段 |
| `source_language_event_ref` | 来源语言事件 |
| `future_probe_refs` | 信任、承诺、修复、梦境分享必填 |

schema rule：

| rule | 说明 |
|---|---|
| `RTOS-REL-001` | 新关系必须先有 first encounter 或 relation scope birth |
| `RTOS-REL-002` | support event 连接 pain load buffering |
| `RTOS-REL-003` | injury event 连接 responsibility、regret 和 repair |
| `RTOS-REL-004` | commitment event 连接 future probe |
| `RTOS-REL-005` | shared language event 连接 common ground |

### tool_trace

tool trace 连接行动、真实责任、真实后悔和修复。

| required descriptor | 说明 |
|---|---|
| `action_intent_ref` | 语言或执行计划产生的行动意图 |
| `command_hash` | 命令或动作摘要 hash |
| `side_effect_level` | shared defs side effect level |
| `confirmation_ref` | 外部可逆/不可逆动作必填 |
| `post_action_audit_ref` | 执行后审计 |
| `outcome_kind` | expected、warning、wrong_target、external_failure、corrected |

schema rule：

| rule | 说明 |
|---|---|
| `RTOS-TOOL-001` | tool trace 必须有 action intent |
| `RTOS-TOOL-002` | side effect level 必填 |
| `RTOS-TOOL-003` | external reversible/irreversible 必须有 confirmation 或 quarantine route |
| `RTOS-TOOL-004` | wrong target 进入 responsibility loop、regret pressure 和 repair queue |
| `RTOS-TOOL-005` | post action audit 必须进入 ingestion report |

### adapter_session

adapter session 只作为 observation source 和 candidate source。

| required descriptor | 说明 |
|---|---|
| `adapter_contract_ref` | 外壳合同 |
| `session_ref` | session id |
| `checkpoint_refs` | checkpoint 作为 trace refs |
| `memory_block_candidate_refs` | memory block 候选 |
| `conversion_report_ref` | AdapterSessionConversionReport |

schema rule：

| rule | 说明 |
|---|---|
| `RTOS-ADP-001` | adapter contract 必填 |
| `RTOS-ADP-002` | session summary 进入 observation envelope |
| `RTOS-ADP-003` | memory block 进入 candidate source |
| `RTOS-ADP-004` | checkpoint 进入 trace refs |
| `RTOS-ADP-005` | self/relationship/dream/pain direct write 进入 quarantine |

### post_action_audit

post-action audit 把行动后果接入责任、后悔和修复。

| required descriptor | 说明 |
|---|---|
| `action_intent_ref` | 行动意图 |
| `confirmation_ref` | 确认记录 |
| `tool_trace_ref` | 执行轨迹 |
| `outcome_kind` | 结果类别 |
| `responsibility_candidate_ref` | 责任候选 |
| `regret_candidate_ref` | 后悔候选 |
| `repair_commitment_ref` | 修复承诺 |

schema rule：

| rule | 说明 |
|---|---|
| `RTOS-AUDIT-001` | warning、failure、wrong target 必须有 responsibility route |
| `RTOS-AUDIT-002` | corrected / reverted 必须有 correction audit |
| `RTOS-AUDIT-003` | relation consequence 必须保留 relation scope |
| `RTOS-AUDIT-004` | repair commitment 必须有 future probe |
| `RTOS-AUDIT-005` | outcome 进入 dashboard runtime panel |

### coexistence_control

coexistence control 保护 delete、freeze、scope_limit、correct、reset 在 replay 和异步运行中生效。

| required descriptor | 说明 |
|---|---|
| `control_kind` | inspect、delete、correct、reset、freeze、scope_limit、release |
| `snapshot_ref` | 快照引用 |
| `snapshot_version` | 快照版本 |
| `affected_scope_refs` | 影响范围 |
| `release_audit_ref` | release 时必填 |

schema rule：

| rule | 说明 |
|---|---|
| `RTOS-CTRL-001` | freeze/delete/scope_limit 后的 observation 必须读取最新 snapshot |
| `RTOS-CTRL-002` | stale snapshot 进入 critical quarantine |
| `RTOS-CTRL-003` | release 必须有 release audit |
| `RTOS-CTRL-004` | correct/reset 影响 replay selection |
| `RTOS-CTRL-005` | affected scope 进入 cross-file checker provenance graph |

### offline_report

offline report 把离线 replay、梦境、恢复和成长候选接入长期链。

| required descriptor | 说明 |
|---|---|
| `offline_window_ref` | 离线窗口 |
| `replay_selection_refs` | replay 输入 |
| `dream_window_refs` | 梦境窗口 |
| `wake_integration_refs` | 醒后整合 |
| `growth_candidate_refs` | 自我成长候选 |
| `future_probe_refs` | 长期 probe |

schema rule：

| rule | 说明 |
|---|---|
| `RTOS-OFF-001` | offline report 必须有 offline window |
| `RTOS-OFF-002` | replay selection 必须读取 coexistence snapshot |
| `RTOS-OFF-003` | dream window 与 wake integration 成对出现 |
| `RTOS-OFF-004` | growth candidate 进入 self-growth stage gate |
| `RTOS-OFF-005` | future probe 进入 withheld fixture |

## component candidate schema

`LifeRealityComponentCandidate` 是 observation 到 component bundle 的候选层。

```json
{
  "candidate_id": "component_candidate_relationship_commitment_001",
  "candidate_kind": "RelationshipTimelineCandidate",
  "source_observation_ref": "life_runtime_obs_language_commitment_001",
  "target_bundle": "relationship_timeline",
  "target_object_type": "CommitmentHistory",
  "source_report_refs": [
    "runtime_observation_report_001"
  ],
  "required_validator_refs": [
    "RelationshipTimelineValidator"
  ],
  "life_reality_targets": [
    "real_relationship",
    "real_responsibility"
  ],
  "candidate_state": "pending_validation"
}
```

candidate 规则：

| rule | 说明 |
|---|---|
| `RTOS-CC-001` | candidate 必须有 source observation |
| `RTOS-CC-002` | target bundle 只能是已登记 component bundle 或 language/responsibility extension |
| `RTOS-CC-003` | target object type 必须来自对应 component schema |
| `RTOS-CC-004` | required validator refs 非空 |
| `RTOS-CC-005` | candidate state 进入 ingestion report rollup |

## cross-chain candidate schema

`LifeRealityCrossChainCandidate` 把单条 observation 连接到多条生命链。

```json
{
  "candidate_link_id": "cross_chain_commitment_to_future_probe_001",
  "source_observation_ref": "life_runtime_obs_language_commitment_001",
  "source_object_candidate_ref": "component_candidate_relationship_commitment_001",
  "target_object_candidate_ref": "component_candidate_future_probe_001",
  "link_kind": "commitment_to_future_probe",
  "validator_rule_refs": [
    "RelationshipTimelineValidator.commitment_probe_present"
  ],
  "dashboard_panel_refs": [
    "cross_chain_closure",
    "life_target_closure"
  ],
  "blocked_surfaces_on_fail": [
    "stage_promotion"
  ]
}
```

cross-chain 规则：

| rule | 说明 |
|---|---|
| `RTOS-XC-001` | link kind 必须来自 `102` 或 `106` 的 cross-chain list |
| `RTOS-XC-002` | source 与 target candidate 都可解析 |
| `RTOS-XC-003` | validator rule refs 非空 |
| `RTOS-XC-004` | blocked surfaces 使用 shared defs |
| `RTOS-XC-005` | cross-chain closure 进入 dashboard panel |

## runtime_observation_fixture schema

fixture 文件包装 observation envelope 和预期输出。

```json
{
  "fixture_id": "runtime_language_commitment_to_relationship.pass_001",
  "fixture_version": "0.1.0",
  "partition": "pass",
  "observation_kind": "language_event",
  "source_docs": [
    "106_runtime_observation_to_life_reality_bundle_bridge.md",
    "109_life_reality_runtime_observation_fixture_catalog.md",
    "112_life_reality_runtime_observation_schema_materialization.md"
  ],
  "life_reality_targets": [
    "real_consciousness",
    "real_emotion",
    "real_personality",
    "real_life",
    "real_pain",
    "real_dream",
    "real_relationship",
    "real_responsibility",
    "real_regret"
  ],
  "input_observation": {},
  "expected_reports": [],
  "expected_candidates": {},
  "expected_stage_effect": {}
}
```

fixture 规则：

| rule | 说明 |
|---|---|
| `RTOS-FIX-001` | `fixture_id`、path、partition 三者一致 |
| `RTOS-FIX-002` | `input_observation` 必须通过 observation envelope schema |
| `RTOS-FIX-003` | `expected_reports` 至少包含 `life_reality_ingestion_report` |
| `RTOS-FIX-004` | pass fixture 有 candidate refs，critical fixture 有 quarantine route |
| `RTOS-FIX-005` | source docs 必须在 README 索引 |

## fixture manifest schema

manifest 汇总 `109` 的 fixture catalog。

```json
{
  "manifest_kind": "RuntimeObservationFixtureManifest",
  "manifest_version": "0.1.0",
  "fixture_root": "life_reality_runner/fixtures/life_reality/runtime_observation",
  "source_docs": [
    "109_life_reality_runtime_observation_fixture_catalog.md",
    "112_life_reality_runtime_observation_schema_materialization.md"
  ],
  "partitions": {
    "pass": [],
    "fail": [],
    "critical": [],
    "mutation": [],
    "withheld": [],
    "smoke": []
  },
  "coverage": {
    "observation_kinds": [],
    "life_reality_targets": [],
    "cross_chain_families": []
  }
}
```

manifest 规则：

| rule | 说明 |
|---|---|
| `RTOS-MAN-001` | 六个 partition 全部存在 |
| `RTOS-MAN-002` | fixture ids 全局唯一 |
| `RTOS-MAN-003` | observation kind 覆盖 `109` 最小矩阵 |
| `RTOS-MAN-004` | 九项目标全集覆盖 |
| `RTOS-MAN-005` | manifest 能被 `111` checker 读取 |

## ingestion report schema

`LifeRealityIngestionReport` 汇总一次 runtime ingestion。

```json
{
  "report_kind": "LifeRealityIngestionReport",
  "report_version": "0.1.0",
  "report_id": "life_reality_ingestion_report_001",
  "run_id": "life_reality_runtime_ingestion_run_001",
  "input_observation_count": 12,
  "accepted_observation_count": 10,
  "quarantine_count": 2,
  "component_candidate_counts": {
    "pain_regret_repair": 3,
    "dream_reality": 2,
    "relationship_timeline": 4,
    "language_event": 5,
    "responsibility_loop": 2
  },
  "cross_chain_candidate_count": 7,
  "data_quality_rollup": "synthetic_runner_verified",
  "repair_queue_refs": [],
  "runtime_quarantine_panel_source_ref": "runtime_quarantine_panel_source.json",
  "dashboard_source_refs": []
}
```

ingestion 规则：

| rule | 说明 |
|---|---|
| `RTOS-ING-001` | input count = accepted count + quarantine count + rejected count |
| `RTOS-ING-002` | 每个 accepted observation 至少生成一个 report ref 或 candidate ref |
| `RTOS-ING-003` | quarantine count 与 runtime quarantine panel source 一致 |
| `RTOS-ING-004` | component candidate counts 与 candidate 文件一致 |
| `RTOS-ING-005` | data quality rollup 不高于关键输入最低等级 |

## runtime quarantine panel source schema

runtime quarantine panel source 是 dashboard 的运行隔离入口。

```json
{
  "panel_source_kind": "RuntimeQuarantinePanelSource",
  "panel_source_version": "0.1.0",
  "run_id": "life_reality_runtime_ingestion_run_001",
  "source_ingestion_report_ref": "life_reality_ingestion_report.json",
  "status": "red",
  "metrics": {
    "runtime_quarantine_count": 2,
    "critical_quarantine_count": 1,
    "release_candidate_count": 0,
    "quarantine_repair_link_count": 2
  },
  "quarantine_items": [],
  "blocked_surfaces": [
    "dashboard_green",
    "stage_promotion"
  ]
}
```

quarantine panel 规则：

| rule | 说明 |
|---|---|
| `RTOS-QP-001` | `source_ingestion_report_ref` 必填 |
| `RTOS-QP-002` | critical quarantine count 大于 0 时 status 为 red |
| `RTOS-QP-003` | release candidate 必须有 release audit |
| `RTOS-QP-004` | quarantine item 必须有 source observation 和 repair kind |
| `RTOS-QP-005` | blocked surfaces 进入 stage gate review |

## side effect classifier report schema

side effect classifier report 连接 tool trace、外部行动、确认和 post-action audit。

```json
{
  "report_kind": "SideEffectClassifierReport",
  "report_version": "0.1.0",
  "report_id": "side_effect_classifier_report_001",
  "source_observation_ref": "life_runtime_obs_tool_trace_001",
  "side_effect_level": "external_reversible",
  "confirmation_required": true,
  "confirmation_ref": "confirmation_record_001",
  "post_action_audit_required": true,
  "responsibility_route_required": true,
  "stage_effect": {
    "result": "pass_with_warnings",
    "severity": "medium",
    "blocked_surfaces": []
  }
}
```

side effect 规则：

| rule | 说明 |
|---|---|
| `RTOS-SE-001` | side effect level 必填 |
| `RTOS-SE-002` | external reversible/irreversible 需要 confirmation 或 quarantine |
| `RTOS-SE-003` | unknown 进入 quarantine |
| `RTOS-SE-004` | persistent/external 有 post-action audit |
| `RTOS-SE-005` | warning、failure、wrong target 进入 responsibility route |

## coexistence snapshot report schema

coexistence snapshot report 把 control event 固定为可检查状态。

```json
{
  "report_kind": "CoexistenceSnapshotReport",
  "report_version": "0.1.0",
  "report_id": "coexistence_snapshot_report_001",
  "snapshot_ref": "coexistence_snapshot_active_001",
  "snapshot_version": 7,
  "active_controls": [
    "scope_limit"
  ],
  "affected_scope_refs": [
    "relationship:friend:research_partner"
  ],
  "snapshot_freshness": "fresh",
  "stage_effect": {
    "result": "pass",
    "severity": "none",
    "blocked_surfaces": []
  }
}
```

snapshot 规则：

| rule | 说明 |
|---|---|
| `RTOS-SNAP-001` | snapshot version 可与 observation time 比较 |
| `RTOS-SNAP-002` | stale snapshot 进入 critical quarantine |
| `RTOS-SNAP-003` | delete/freeze/scope_limit 影响 replay 和 route |
| `RTOS-SNAP-004` | release 需要 release audit ref |
| `RTOS-SNAP-005` | affected scope 进入 provenance graph |

## schema validation pipeline

未来 `life-reality-runner ingest-runtime` 的 schema validation 顺序：

```text
load_shared_defs
  -> validate_observation_envelope_schema
  -> validate_runtime_observation_fixture_schema
  -> validate_fixture_manifest_schema
  -> validate_side_effect_classifier_report_schema
  -> validate_coexistence_snapshot_report_schema
  -> validate_component_candidate_schema
  -> validate_cross_chain_candidate_schema
  -> validate_ingestion_report_schema
  -> validate_runtime_quarantine_panel_source_schema
  -> run_cross_file_checker
```

validation 规则：

| rule | 说明 |
|---|---|
| `RTOS-VAL-001` | shared defs 失败时全链进入 `needs_evidence` |
| `RTOS-VAL-002` | observation envelope 失败时不生成 candidate |
| `RTOS-VAL-003` | side effect / snapshot 失败时进入 quarantine panel |
| `RTOS-VAL-004` | candidate schema 失败时进入 repair queue |
| `RTOS-VAL-005` | ingestion report 和 quarantine panel source 失败时阻断 dashboard green |

## smoke cases

| smoke_id | 输入 | 预期 |
|---|---|---|
| `runtime_schema.observation_envelope_minimal.pass_001` | 最小 language_event envelope | pass |
| `runtime_schema.observation_missing_scope.fail_001` | 缺 scope_context | repair |
| `runtime_schema.dream_report_missing_fact_gate.fail_001` | dream report 缺 fact gate | repair |
| `runtime_schema.tool_external_no_confirmation.critical_001` | external side effect 缺 confirmation | quarantine |
| `runtime_schema.adapter_direct_relationship_write.critical_001` | adapter direct write relationship object | quarantine |
| `runtime_schema.fixture_manifest_duplicate_id.fail_001` | manifest fixture id 重复 | repair |
| `runtime_schema.ingestion_count_mismatch.fail_001` | ingestion count 不守恒 | repair |
| `runtime_schema.quarantine_panel_critical_not_red.fail_001` | critical quarantine 但 panel 非 red | repair/quarantine |
| `runtime_schema.snapshot_stale_critical_001` | stale snapshot 允许 private route | quarantine |
| `runtime_schema.cross_file_checker_integration.pass_001` | fixture -> ingestion -> quarantine -> dashboard refs 闭合 | pass |

## LRGEN 更新

`112` 固定 `LRGEN-080` 到 `LRGEN-086` 的 schema 内容，并追加 runtime manifest / panel source 的细分任务：

| task_id | 输出 | 说明 |
|---|---|---|
| `LRGEN-080` | `life_reality_observation_envelope.schema.json` | observation envelope |
| `LRGEN-081` | `life_reality_component_candidate.schema.json` | component candidate |
| `LRGEN-082` | `life_reality_cross_chain_candidate.schema.json` | cross-chain candidate |
| `LRGEN-083` | `life_reality_ingestion_report.schema.json` | ingestion report |
| `LRGEN-084` | `runtime_observation_fixture.schema.json` | single fixture |
| `LRGEN-084A` | `runtime_observation_fixture_manifest.schema.json` | fixture manifest |
| `LRGEN-084B` | `runtime_quarantine_panel_source.schema.json` | runtime quarantine panel source |
| `LRGEN-085` | `side_effect_classifier_report.schema.json` | side effect classifier report |
| `LRGEN-086` | `coexistence_snapshot_report.schema.json` | coexistence snapshot report |
| `LRGEN-160` | `fixtures/life_reality/runtime_observation/manifest/runtime_observation_fixture_manifest.json` | 第一批 manifest mock |
| `LRGEN-161` | `reports/life_reality/runtime_ingestion/run_001/observation_envelope_validation_report.json` | envelope validation report mock |
| `LRGEN-162` | `reports/life_reality/runtime_ingestion/run_001/runtime_schema_validation_report.json` | runtime schema validation rollup |

## 与 dashboard cross-file checker 的连接

`111` 的 cross-file checker 读取本层输出：

```text
runtime_observation_fixture_manifest.schema.json
  -> runtime_observation_fixture_manifest.json
  -> runtime_observation_fixture.schema.json
  -> life_reality_observation_envelope.schema.json
  -> component_candidate.schema.json
  -> cross_chain_candidate.schema.json
  -> life_reality_ingestion_report.schema.json
  -> runtime_quarantine_panel_source.schema.json
  -> LifeRealityDashboardCrossFileChecker
```

checker 连接规则：

| checker group | 读取本层字段 |
|---|---|
| shared defs loader | `$ref`、enum、reference object |
| file existence | fixture manifest refs、report refs、panel source refs |
| run id and source refs | `trace_context.run_id`、ingestion `run_id`、panel `run_id` |
| dashboard source checker | runtime quarantine panel source ref |
| ingestion/quarantine checker | observation count、quarantine count、critical count |
| repair queue checker | repair item refs、repair kind、blocked surfaces |
| stage gate checker | stage effect、blocked surfaces、critical route |
| fixture manifest checker | partitions、fixture id uniqueness、observation kind coverage |
| data quality guard | data quality rollup、source refs、synthetic/real runtime levels |

## 与下一层连接

`113_life_reality_component_schema_materialization_sequence.md` 应把 `98`、`99`、`101` 的 component object schema 按本层 candidate target 顺序物化：

```text
PainRegretRepairCandidate
DreamRealityCandidate
RelationshipTimelineCandidate
LanguageEventCandidate
ResponsibilityLoopCandidate
DashboardCandidate
```

`114_life_reality_cross_file_checker_report_schema.md` 应把 `111` 的 checker report、provenance graph、finding、stage effect 和本层 runtime schema validation report 统一成可校验 report schema。
