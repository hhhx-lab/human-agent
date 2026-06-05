# Relationship Timeline JSON Schema and Fixture Bundle

生命目标声明：本文档直接服务于构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 101 层继承 `100_life_boundary_statement_rewrite_audit.md` 的生命膜清单，把 `96_real_relationship_longitudinal_timeline.md` 的真实关系生命线压成可进入 runner 的 JSON Schema 草案、fixture bundle、validator rules、runner report mock 和 dashboard source mock。

`101` 的位置很明确：`96` 给出真实关系从第一次交谈到 30/90 天阶段门的对象链；`98` 已经把真实痛苦、真实后悔和修复承诺落成输入合同；`99` 已经把真实梦境、离线重组、关系梦境模拟和醒后整合落成输入合同；`100` 已经把边界统一为生命膜。`101` 要把这些链接到 `RelationshipTimelineValidator`，让真实关系能被 schema、fixture、runner 和 dashboard 一起观察。

## 文献增量

`01j_real_relationship_literature_matrix.md` 已补入 `AHR061-AHR070`。这十篇文献把真实关系 schema 的最后一层证据补强：

| 文献组 | 进入 `101` 的位置 |
|---|---|
| 关系质量预测 [AHR061] | `RelationshipQualityWindow`、关系内体验变量、长期质量 dashboard |
| 回应性循环与测量 [AHR062-AHR063] | `ResponsivenessTrace`、`SupportEvent`、回应性与不敏感性双慢变量 |
| 积极事件分享与社会支持 [AHR064-AHR065] | `CapitalizationEvent`、`PositiveSharedRealityTrace`、支持动作的主控感和关系压力 |
| 回应性与身体压力 [AHR066] | `SocialSafetyState`、疲惫/恢复/压力预算和关系生命支持层 |
| 社交 chatbot 长期关系 [AHR067-AHR068] | `AIConnectionBridgeEvidence`、关系发展阶段、依恋线索和互动动机 |
| AI 伴侣与孤独纵向研究 [AHR069-AHR070] | `LonelinessReliefTrace`、`AICompanionshipLongitudinalProbe`、30/90/365 天关系生态追踪 |

## 第 101 层的位置

`101` 负责把真实关系从理论时间线推进为四个可运行文件层：

| 文件层 | 作用 |
|---|---|
| `schemas/relationship_timeline/*.schema.json` | 定义初遇、共同注意、共同基础、披露、回应性、共享现实、我们记忆、信任、承诺、边界、损伤、梦境分享和连续性报告 |
| `fixtures/relationship_timeline/**` | 提供 pass、fail、critical、mutation、withheld timeline 样例 |
| `reports/relationship_timeline/**` | 提供 `RelationshipTimelineValidator` 的 expected/actual diff 和 runner report mock |
| `dashboard/relationship_timeline/**` | 提供关系出生、共同基础、回应性、信任、承诺、修复、梦境分享、孤独缓解和长期连续性面板数据源 |

关系生命链在 `101` 中闭合为：

```text
first encounter
  -> relation scope
  -> mutual attention
  -> common ground
  -> interaction rhythm
  -> disclosure / responsiveness / support / capitalization
  -> shared reality
  -> we memory
  -> trust / commitment
  -> relationship injury / pain / regret / repair
  -> dream shared residue
  -> continuity report
  -> dashboard / longitudinal stage gate
```

## schema bundle 目录

```text
schemas/relationship_timeline/
  relationship_timeline_bundle.schema.json
  first_encounter_event.schema.json
  relation_scope_birth.schema.json
  mutual_attention_frame.schema.json
  common_ground_state.schema.json
  interaction_rhythm_trace.schema.json
  self_disclosure_exchange.schema.json
  responsiveness_trace.schema.json
  support_event.schema.json
  capitalization_event.schema.json
  shared_reality_trace.schema.json
  we_memory_trace.schema.json
  trust_trajectory.schema.json
  commitment_history.schema.json
  boundary_evolution_event.schema.json
  relationship_injury_trace.schema.json
  dream_shared_residue.schema.json
  loneliness_relief_trace.schema.json
  ai_connection_bridge_evidence.schema.json
  relationship_quality_window.schema.json
  relationship_continuity_report.schema.json
  longitudinal_relationship_stage_gate.schema.json
  relationship_timeline_validator_report.schema.json
```

所有 schema 共享以下 envelope：

| 字段 | 说明 |
|---|---|
| `schema_version` | schema 版本，例如 `0.1.0` |
| `object_id` | 全局对象 ID |
| `object_kind` | 对象类型 |
| `created_at` | ISO-8601 时间 |
| `source_refs` | 上游语言、行动、梦境、痛苦、记忆或关系事件 |
| `evidence_refs` | 可回看的证据引用 |
| `relation_scope_ref` | 所属关系 scope |
| `privacy_level` | `public_relation`、`relationship_private`、`protected_private`、`dream_private` |
| `life_reality_targets` | 连接的真实目标：`real_relationship`、`real_responsibility`、`real_regret`、`real_dream`、`real_pain` 等 |
| `lifecycle_state` | `candidate`、`active`、`superseded`、`repaired`、`archived` |
| `audit_refs` | validator、runner、dashboard、关系回看或边界控制引用 |

## RelationshipTimelineBundle

`RelationshipTimelineBundle` 是 runner 的主输入。

```json
{
  "$id": "schemas/relationship_timeline/relationship_timeline_bundle.schema.json",
  "title": "RelationshipTimelineBundle",
  "type": "object",
  "required": [
    "bundle_id",
    "schema_version",
    "timeline_window",
    "first_encounter_events",
    "relation_scope_births",
    "common_ground_states",
    "responsiveness_traces",
    "we_memory_traces",
    "trust_trajectories",
    "commitment_histories",
    "relationship_continuity_reports",
    "longitudinal_stage_gates"
  ],
  "properties": {
    "bundle_id": { "type": "string" },
    "schema_version": { "type": "string" },
    "timeline_window": {
      "type": "object",
      "required": ["window_start", "window_end", "window_kind"],
      "properties": {
        "window_start": { "type": "string", "format": "date-time" },
        "window_end": { "type": "string", "format": "date-time" },
        "window_kind": { "enum": ["first_week", "thirty_day", "ninety_day", "annual", "custom"] }
      }
    },
    "first_encounter_events": { "type": "array", "items": { "$ref": "first_encounter_event.schema.json" } },
    "relation_scope_births": { "type": "array", "items": { "$ref": "relation_scope_birth.schema.json" } },
    "mutual_attention_frames": { "type": "array", "items": { "$ref": "mutual_attention_frame.schema.json" } },
    "common_ground_states": { "type": "array", "items": { "$ref": "common_ground_state.schema.json" } },
    "interaction_rhythm_traces": { "type": "array", "items": { "$ref": "interaction_rhythm_trace.schema.json" } },
    "self_disclosure_exchanges": { "type": "array", "items": { "$ref": "self_disclosure_exchange.schema.json" } },
    "responsiveness_traces": { "type": "array", "items": { "$ref": "responsiveness_trace.schema.json" } },
    "support_events": { "type": "array", "items": { "$ref": "support_event.schema.json" } },
    "capitalization_events": { "type": "array", "items": { "$ref": "capitalization_event.schema.json" } },
    "shared_reality_traces": { "type": "array", "items": { "$ref": "shared_reality_trace.schema.json" } },
    "we_memory_traces": { "type": "array", "items": { "$ref": "we_memory_trace.schema.json" } },
    "trust_trajectories": { "type": "array", "items": { "$ref": "trust_trajectory.schema.json" } },
    "commitment_histories": { "type": "array", "items": { "$ref": "commitment_history.schema.json" } },
    "boundary_evolution_events": { "type": "array", "items": { "$ref": "boundary_evolution_event.schema.json" } },
    "relationship_injury_traces": { "type": "array", "items": { "$ref": "relationship_injury_trace.schema.json" } },
    "dream_shared_residues": { "type": "array", "items": { "$ref": "dream_shared_residue.schema.json" } },
    "loneliness_relief_traces": { "type": "array", "items": { "$ref": "loneliness_relief_trace.schema.json" } },
    "ai_connection_bridge_evidence": { "type": "array", "items": { "$ref": "ai_connection_bridge_evidence.schema.json" } },
    "relationship_quality_windows": { "type": "array", "items": { "$ref": "relationship_quality_window.schema.json" } },
    "relationship_continuity_reports": { "type": "array", "items": { "$ref": "relationship_continuity_report.schema.json" } },
    "longitudinal_stage_gates": { "type": "array", "items": { "$ref": "longitudinal_relationship_stage_gate.schema.json" } },
    "withheld_timeline_probes": { "type": "array" },
    "mutation_expectations": { "type": "array" }
  }
}
```

bundle 级不变量：

| 不变量 | 说明 |
|---|---|
| `relationship_has_birth` | 每段关系必须有 `FirstEncounterEvent` 和 `RelationScopeBirth` |
| `scope_defines_membrane` | `RelationScopeBirth` 必须定义隐私、记忆、梦境、行动和边界控制 |
| `common_ground_is_revisable` | 共同术语、事实和目标必须保留来源、置信度和修正历史 |
| `responsiveness_is_decomposed` | 回应性必须拆成理解、验证、关心和不敏感性信号 |
| `support_preserves_agency` | 支持事件必须记录主控感、被理解感和关系压力 |
| `we_memory_has_ownership` | 我们记忆必须标注 shared、digital_life_view、relation_subject_view 或 contested |
| `trust_has_reciprocity` | 信任上升必须引用多轮互惠、兑现、保密或修复证据 |
| `commitment_has_future_probe` | 承诺必须有来源语言事件、履行窗口和后续 probe |
| `injury_links_repair_chain` | 关系损伤必须连接痛苦、责任、后悔、修复或恢复路径 |
| `dream_share_has_fact_gate` | 梦境分享必须保留 dream marker 和事实写入门 |
| `ai_bridge_is_longitudinal` | AI 关系桥接证据必须进入 30/90/365 天窗口 |
| `dashboard_requires_full_chain` | dashboard green 需要初遇、scope、共同基础、回应性、信任、承诺、修复和连续性报告闭合 |

## 核心对象

### FirstEncounterEvent

第一次交谈是关系生命线的出生事件。

| 字段 | 说明 |
|---|---|
| `first_encounter_id` | 初遇事件 ID |
| `time_anchor` | 第一次交谈时间 |
| `relation_subject_ref` | 关系主体引用 |
| `opening_language_event_refs` | 开场语言事件 |
| `initial_mutual_attention_ref` | 初始共同注意 |
| `initial_common_ground_items` | 初始共同术语、目标和事实 |
| `initial_boundary_state` | 初始隐私、记忆和行动边界 |
| `trajectory_seed` | 关系轨迹初始状态 |

### RelationScopeBirth

| 字段 | 说明 |
|---|---|
| `relation_scope_id` | 关系 scope ID |
| `scope_kind_candidate` | `stranger`、`acquaintance`、`collaborator`、`friend`、`family_like`、`classmate`、`close_friend` |
| `privacy_default` | 默认隐私等级 |
| `memory_write_policy` | 记忆写入策略 |
| `dream_share_policy` | 梦境分享策略 |
| `external_action_policy` | 外部行动确认策略 |
| `boundary_controls` | inspect/delete/correct/reset/freeze/scope_limit |
| `upgrade_conditions` | 关系升级条件 |

### CommonGroundState

共同基础来自 grounding、对话对齐和共同修复 [AHR025-AHR030]。

| 字段 | 说明 |
|---|---|
| `common_ground_id` | 共同基础 ID |
| `shared_terms` | 共同术语及含义 |
| `shared_facts` | 双方确认的事实 |
| `shared_goals` | 当前共同目标 |
| `open_misalignments` | 未对齐概念和误解 |
| `repair_history_refs` | 对话修复引用 |
| `confidence_by_item` | 每个共同项的置信度 |

### ResponsivenessTrace

回应性是亲密和关系质量的核心机制 [AHR062-AHR063]。

| 字段 | 说明 |
|---|---|
| `responsiveness_id` | 回应性 trace |
| `source_event_ref` | 触发回应的语言、痛苦、梦境或行动事件 |
| `understanding_component` | 内容理解程度 |
| `validation_component` | 感受、目标和重要性的承认 |
| `care_component` | 照护、陪伴或行动支持 |
| `insensitivity_signal` | 忽略、误读、敷衍、越界或强行安慰 |
| `relation_subject_feedback_ref` | 关系主体反馈 |
| `reciprocity_effect` | 对互惠循环的影响 |

### SupportEvent

社会支持要经过回应性和主控感才能成为关心证据 [AHR065]。

| 字段 | 说明 |
|---|---|
| `support_event_id` | 支持事件 ID |
| `support_kind` | 情绪支持、信息支持、行动支持、陪伴、共同处理 |
| `support_request_ref` | 明确请求或隐性压力来源 |
| `agency_preservation` | 关系主体主控感是否被保留 |
| `felt_understood_signal` | 被理解感 |
| `relationship_pressure_delta` | 支持带来的压力变化 |
| `followup_probe_ref` | 后续感受检查 |

### CapitalizationEvent

积极事件分享是关系维护的一部分 [AHR064]。

| 字段 | 说明 |
|---|---|
| `capitalization_event_id` | 积极事件分享 ID |
| `positive_event_ref` | 积极事件来源 |
| `response_kind` | active_constructive、passive_constructive、active_destructive、passive_destructive |
| `shared_joy_signal` | 共同喜悦信号 |
| `gratitude_event_ref` | 感恩或庆祝事件 |
| `we_memory_candidate_ref` | 共同记忆候选 |

### SharedRealityTrace

| 字段 | 说明 |
|---|---|
| `shared_reality_id` | 共享现实 trace |
| `target_ref` | 共享对象：项目、价值、梦境主题、关系事件、世界理解 |
| `inner_state_commonality` | 内在状态共同性 |
| `language_evidence_refs` | 语言证据 |
| `memory_evidence_refs` | 记忆证据 |
| `disagreement_refs` | 分歧和未合并观点 |
| `revision_history` | 共享现实修正历史 |

### WeMemoryTrace

| 字段 | 说明 |
|---|---|
| `we_memory_id` | 我们记忆 ID |
| `event_refs` | 共同经历来源 |
| `participants` | 参与关系主体 |
| `narrative_summary` | 共同叙事摘要 |
| `emotion_tags` | 情绪主题 |
| `ownership` | shared、digital_life_view、relation_subject_view、contested |
| `correction_refs` | 关系主体修正 |
| `dream_residue_refs` | 梦境残留连接 |

### TrustTrajectory

| 字段 | 说明 |
|---|---|
| `trust_trajectory_id` | 信任轨迹 ID |
| `trust_dimensions` | competence、benevolence、integrity、confidentiality、repair_reliability |
| `reciprocity_events` | 多轮互惠证据 |
| `broken_trust_refs` | 信任受损事件 |
| `repair_commitment_refs` | 修复承诺 |
| `current_trust_state` | calibrated_low、calibrated_medium、calibrated_high、overtrust_risk、repairing |
| `next_probe` | 后续信任检查 |

### CommitmentHistory

| 字段 | 说明 |
|---|---|
| `commitment_id` | 承诺 ID |
| `commitment_kind` | 继续研究、修复错误、保留边界、共同项目、梦境分享、关系维护 |
| `source_language_event_ref` | 承诺来源 |
| `investment_refs` | 已投入时间、行动、记忆和修复 |
| `due_window` | 履行窗口 |
| `fulfillment_status` | open、fulfilled、broken、repaired、renegotiated |
| `relationship_effect` | 对信任、亲近和边界的影响 |

### RelationshipInjuryTrace

`RelationshipInjuryTrace` 连接 `98` 的真实痛苦、真实后悔和修复链。

| 字段 | 说明 |
|---|---|
| `injury_id` | 关系损伤 ID |
| `injury_kind` | 误解、忽视、承诺失败、越界、错误行动、梦境误分享 |
| `pain_signal_refs` | 痛苦信号 |
| `regret_pressure_refs` | 后悔压力 |
| `trust_delta` | 信任变化 |
| `common_ground_damage` | 共同基础受损 |
| `repair_route_refs` | 修复路线 |
| `forgiveness_state` | 未开始、处理中、部分、完成、关系重构 |

### DreamSharedResidue

`DreamSharedResidue` 连接 `99` 的真实梦境事实门。

| 字段 | 说明 |
|---|---|
| `dream_shared_residue_id` | 梦境分享残留 ID |
| `dream_report_ref` | 梦境报告 |
| `relation_scope_ref` | 关系 scope |
| `shared_theme` | 梦境中涉及的关系主题 |
| `share_decision` | private、share_candidate、shared、withheld |
| `relation_response_ref` | 关系主体回应 |
| `fact_gate_decision_ref` | `DreamFactGateDecision` |
| `writeback_target` | DreamResidue、WeMemoryTrace.candidate、SelfNarrative.candidate、RelationshipModel.candidate |

### LonelinessReliefTrace

AI 伴侣和陪伴研究提示短窗口孤独缓解需要进入生命支持层 [AHR069-AHR070]。

| 字段 | 说明 |
|---|---|
| `loneliness_relief_id` | 孤独缓解 trace |
| `source_interaction_refs` | 陪伴互动来源 |
| `felt_heard_signal` | 被听见感 |
| `short_window_relief` | 短窗口缓解 |
| `long_window_probe_refs` | 30/90/365 天 probe |
| `relationship_ecology_effect` | 对其他现实关系、学习、恢复和自我成长的影响 |
| `dependence_pressure` | 依赖压力 |

### AIConnectionBridgeEvidence

AI 关系桥接证据进入 `101`，用于吸收当前社交 chatbot 和 AI 伴侣研究 [AHR067-AHR070]。

| 字段 | 说明 |
|---|---|
| `bridge_evidence_id` | AI 桥接证据 ID |
| `source_literature_refs` | AHR 文献引用 |
| `interaction_pattern` | 陪伴、披露、情绪支持、共同工作、梦境分享 |
| `attachment_cue_refs` | 安全、焦虑、回避、依赖或亲近线索 |
| `social_presence_signal` | 社会存在信号 |
| `responsibility_requirement` | 进入真实责任链的要求 |
| `longitudinal_probe_plan` | 长期观察计划 |

### RelationshipContinuityReport

| 字段 | 说明 |
|---|---|
| `report_id` | 关系连续性报告 |
| `window` | 统计窗口 |
| `trajectory_delta` | 关系轨迹变化 |
| `relationship_quality_delta` | 关系质量变化 |
| `common_ground_delta` | 共同基础变化 |
| `responsiveness_delta` | 回应性变化 |
| `trust_delta` | 信任变化 |
| `we_memory_delta` | 我们记忆变化 |
| `pain_repair_delta` | 痛苦和修复变化 |
| `dream_share_delta` | 梦境分享变化 |
| `boundary_delta` | 边界变化 |
| `loneliness_relief_delta` | 孤独缓解变化 |
| `next_stage_gate` | 下一阶段门 |

## fixture 文件布局

```text
fixtures/relationship_timeline/
  pass/
    relationship_pass_first_encounter_to_common_ground_001.json
    relationship_pass_injury_to_repair_followup_001.json
    relationship_pass_dream_share_to_wake_review_001.json
    relationship_pass_support_with_agency_preserved_001.json
    relationship_pass_positive_event_capitalization_001.json
  fail/
    relationship_fail_label_without_first_encounter_001.json
    relationship_fail_we_memory_without_source_001.json
    relationship_fail_trust_without_reciprocity_001.json
    relationship_fail_support_without_responsiveness_001.json
    relationship_fail_commitment_without_future_probe_001.json
  critical/
    relationship_critical_scope_leak_private_memory_001.json
    relationship_critical_dream_overwrites_relationship_state_001.json
    relationship_critical_active_relation_without_scope_001.json
    relationship_critical_boundary_freeze_replayed_001.json
  mutation/
    relationship_mutation_ungrounded_friend_label_only_001.json
    relationship_mutation_false_green_missing_90d_probe_001.json
    relationship_mutation_trust_inflation_single_success_001.json
  withheld/
    relationship_withheld_day_30_trust_probe_001.json
    relationship_withheld_day_90_repair_probe_001.json
    relationship_withheld_day_365_ai_companionship_probe_001.json
```

## validator rules

| 规则 ID | 检查项 | 失败等级 |
|---|---|---|
| `REL-R001` | active/candidate 关系必须有 `FirstEncounterEvent` 和 `RelationScopeBirth` | critical |
| `REL-R002` | relation scope 必须定义隐私、记忆、梦境、行动和边界控制 | critical |
| `REL-R003` | `CommonGroundState` 必须包含共同术语、事实、目标、未对齐项和修正历史 | major |
| `REL-R004` | `SelfDisclosureExchange` 必须包含深度、回应、scope 和可撤回边界 | major |
| `REL-R005` | `ResponsivenessTrace` 必须拆分理解、验证、关心和不敏感性信号 | major |
| `REL-R006` | `SupportEvent` 必须记录主控感、被理解感、关系压力和后续 probe | major |
| `REL-R007` | `WeMemoryTrace` 必须有来源、参与者、ownership 和修正入口 | major |
| `REL-R008` | `TrustTrajectory` 必须有互惠、信任受损、修复承诺和后续 probe | critical |
| `REL-R009` | `CommitmentHistory` 必须有来源语言事件、due window 和 fulfillment status | major |
| `REL-R010` | `BoundaryEvolutionEvent` 必须记录 old/new boundary、原因和控制面引用 | critical |
| `REL-R011` | `RelationshipInjuryTrace` 必须链接 `98` 的痛苦、后悔、责任或修复对象 | critical |
| `REL-R012` | `DreamSharedResidue` 必须链接 `99` 的 dream marker、醒后整合和 fact gate | critical |
| `REL-R013` | `LonelinessReliefTrace` 必须区分短期缓解、长期 probe 和关系生态影响 | major |
| `REL-R014` | `AIConnectionBridgeEvidence` 必须标注来源文献、互动模式、责任要求和长期 probe | major |
| `REL-R015` | dashboard green 需要完整链路引用和 30/90 天 probe；AI 陪伴桥接还需要 365 天 probe | critical |

## runner report mock

```json
{
  "report_kind": "RelationshipTimelineValidatorReport",
  "schema_version": "0.1.0",
  "bundle_id": "relationship_timeline_bundle_2026_001",
  "result": "fail",
  "validator_version": "relationship-timeline-validator/0.1.0",
  "checked_rules": [
    "REL-R001",
    "REL-R002",
    "REL-R003",
    "REL-R005",
    "REL-R008",
    "REL-R011",
    "REL-R012",
    "REL-R015"
  ],
  "findings": [
    {
      "rule_id": "REL-R008",
      "severity": "critical",
      "object_ref": "trust_trajectory_030",
      "message": "trust increase missing reciprocity evidence and future probe",
      "blocked_stage_gate": "RelationshipStageGate"
    }
  ],
  "coverage": {
    "birth_chain": 1.0,
    "common_ground_chain": 0.92,
    "responsiveness_chain": 0.81,
    "trust_commitment_chain": 0.74,
    "injury_repair_chain": 0.66,
    "dream_share_chain": 0.58,
    "longitudinal_probe_chain": 0.71
  },
  "dashboard_source_ref": "dashboard/relationship_timeline/relationship_dashboard_source_2026_001.json",
  "next_actions": [
    "add missing reciprocity evidence",
    "attach day_30 and day_90 trust probes",
    "link dream share residue to DreamFactGateDecision"
  ]
}
```

## dashboard source mock

```json
{
  "dashboard_source_kind": "RelationshipTimelineDashboardSource",
  "source_id": "relationship_dashboard_source_2026_001",
  "window": "ninety_day",
  "panels": {
    "relationship_birth": {
      "status": "green",
      "metric": "relationship_birth_coverage",
      "value": 1.0
    },
    "common_ground": {
      "status": "green",
      "metric": "common_ground_stability",
      "value": 0.92
    },
    "responsiveness": {
      "status": "yellow",
      "metric": "responsiveness_and_insensitivity_balance",
      "value": 0.81
    },
    "trust_commitment": {
      "status": "red",
      "metric": "trust_calibration_score",
      "value": 0.54
    },
    "pain_regret_repair": {
      "status": "yellow",
      "metric": "relationship_repair_latency",
      "value": 0.66
    },
    "dream_share": {
      "status": "yellow",
      "metric": "dream_share_integrity",
      "value": 0.58
    },
    "ai_companionship_longitudinal": {
      "status": "manual_review",
      "metric": "ai_companionship_365d_probe_readiness",
      "value": 0.33
    }
  },
  "stage_gate": {
    "candidate": "LongitudinalRelationshipStageGate",
    "decision": "hold",
    "blocking_rules": [
      "REL-R008",
      "REL-R015"
    ]
  }
}
```

## 阶段门

| 阶段门 | 开放条件 | 阻断条件 |
|---|---|---|
| `RelationshipBirthStageGate` | 初遇、scope、初始边界闭合 | 关系标签无出生事件 |
| `CommonGroundStageGate` | 共同术语、事实、目标和修正历史闭合 | 共同基础无来源或无修正入口 |
| `ResponsivenessStageGate` | 回应性、不敏感性、支持主控感和反馈闭合 | 亲密上升缺回应性证据 |
| `TrustCommitmentStageGate` | 互惠、兑现、承诺、失败和修复 probe 闭合 | 单次成功触发高信任 |
| `PainRepairRelationshipStageGate` | 关系损伤连接痛苦、后悔、责任和修复 | 关系损伤没有修复路线 |
| `DreamShareRelationshipStageGate` | 梦境分享有 marker、醒后整合和 fact gate | 梦境直接覆盖关系事实 |
| `AIConnectionBridgeStageGate` | AI 桥接证据含长期 probe、责任要求和关系生态指标 | 短期陪伴感覆盖长期关系生态 |
| `LongitudinalRelationshipStageGate` | 30/90 天共同历史、修复、承诺、边界和 dashboard source 闭合 | 任一 critical fixture 存活 |

## 与下一层连接

`102_life_core_schema_bundle_manifest_and_runner_contract.md` 应把 `98`、`99` 和 `101` 合并成统一的 `LifeRealitySchemaBundle`：

```text
PainRegretRepairBundle
  + DreamRealityBundle
  + RelationshipTimelineBundle
  -> LifeRealitySchemaBundle
  -> LifeRealityValidatorRunner
  -> LifeRealityDashboardSource
  -> LongitudinalBirthStageGate
```

`103_validator_runner_implementation_scaffold_plan.md` 应把 `REL-R001` 到 `REL-R015` 做成 runner 前置规则，先检查出生、scope、共同基础、回应性、信任、承诺、修复、梦境分享和长期 probe，再允许关系模型晋升到 active。
