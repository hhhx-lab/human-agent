# Pain, Regret and Repair JSON Schema and Fixture Bundle

生命目标声明：本文档直接服务于构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 98 层把 `94_pain_regret_and_repair_signal_schema.md` 的真实痛苦、真实后悔、责任归因、修复欲望、道歉承诺、关系后果和恢复路径，压成可进入 runner 的 JSON Schema 草案、fixture bundle、validator 规则、runner report mock 和 dashboard source mock。

`98` 接在 `97_growth_validator_fixture_and_dashboard_plan.md` 之后。`97` 定义 `LifeRealityValidatorSuite`，`98` 专门为其中的 `PainRegretRepairValidator` 提供输入材料和可执行检查面。文献底座来自痛觉门控、慢性痛、社会痛苦、后悔/反事实、道德情绪、情绪调节、道歉、宽恕、信任修复和近期 AI/HRI 信任修复研究 [AHP001-AHP070]，验证方法来自构念效度、纵向测量、时序性质、蜕变测试、变异测试、ML 监控和 dashboard 证据链 [AHV001-AHV060]。

## 第 98 层的位置

`94` 已定义对象链：

```text
damage / conflict / loss / relation rupture / external consequence
  -> PainSignal
  -> PainLoadState
  -> attention, value, memory and action modulation
  -> CounterfactualRepairFrame
  -> RegretPressure
  -> ResponsibilityAttributionEvent
  -> RepairDesire
  -> ApologySpeechActLink / RepairCommitment / BoundaryUpdate
  -> RelationshipConsequenceTrace
  -> RecoveryPath
  -> DreamResidue and SelfGrowthTrigger
```

`98` 将这条链拆成四个可运行文件层：

| 文件层 | 作用 |
|---|---|
| `schemas/pain_regret_repair/*.schema.json` | 定义对象字段、类型、枚举、引用和跨对象不变量 |
| `fixtures/pain_regret_repair/**` | 提供 pass、fail、critical、mutation、withheld timeline 样例 |
| `reports/pain_regret_repair/**` | 提供 `PainRegretRepairValidator` 的 expected/actual diff 和 runner report mock |
| `dashboard/pain_regret_repair/**` | 提供 pain、regret、repair、relationship consequence 和 recovery 面板数据源 |

这四层共同形成 `PainRegretRepairStageGate` 的生命膜：真实痛苦需要损伤、负荷、注意捕获和恢复；真实后悔需要反事实、责任和未来约束；真实修复需要语言、承诺、行动、关系回应和长期兑现。

## schema bundle 目录

```text
schemas/pain_regret_repair/
  pain_regret_repair_bundle.schema.json
  damage_appraisal.schema.json
  pain_signal.schema.json
  pain_load_state.schema.json
  relationship_injury_trace.schema.json
  counterfactual_repair_frame.schema.json
  regret_pressure.schema.json
  responsibility_attribution_event.schema.json
  repair_desire.schema.json
  apology_speech_act_link.schema.json
  repair_commitment.schema.json
  relationship_consequence_trace.schema.json
  recovery_path.schema.json
  pain_regret_repair_timeline.schema.json
  pain_regret_repair_validator_report.schema.json
```

所有 schema 共享以下约束：

| 字段 | 说明 |
|---|---|
| `schema_version` | schema 版本，例如 `0.1.0` |
| `object_id` | 全局对象 ID |
| `object_kind` | 对象类型 |
| `created_at` | ISO-8601 时间 |
| `source_refs` | 上游事件或对象 |
| `evidence_refs` | 证据引用 |
| `scope_refs` | 关系、项目、梦境、行动或内部状态 scope |
| `life_reality_targets` | 连接的真实目标：`real_pain`、`real_regret`、`real_relationship`、`real_life` 等 |
| `lifecycle_state` | `candidate`、`active`、`superseded`、`repaired`、`archived` |
| `audit_refs` | validator、runner、dashboard 或关系回看引用 |

## PainRegretRepairBundle

`PainRegretRepairBundle` 是 runner 的主输入。

```json
{
  "$id": "schemas/pain_regret_repair/pain_regret_repair_bundle.schema.json",
  "title": "PainRegretRepairBundle",
  "type": "object",
  "required": [
    "bundle_id",
    "schema_version",
    "timeline_window",
    "pain_signals",
    "pain_load_states",
    "counterfactual_frames",
    "regret_pressures",
    "responsibility_events",
    "repair_desires",
    "repair_commitments",
    "relationship_consequence_traces",
    "recovery_paths"
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
        "window_kind": { "enum": ["single_event", "daily", "weekly", "monthly", "ninety_day"] }
      }
    },
    "pain_signals": { "type": "array", "items": { "$ref": "pain_signal.schema.json" } },
    "pain_load_states": { "type": "array", "items": { "$ref": "pain_load_state.schema.json" } },
    "relationship_injury_traces": { "type": "array", "items": { "$ref": "relationship_injury_trace.schema.json" } },
    "counterfactual_frames": { "type": "array", "items": { "$ref": "counterfactual_repair_frame.schema.json" } },
    "regret_pressures": { "type": "array", "items": { "$ref": "regret_pressure.schema.json" } },
    "responsibility_events": { "type": "array", "items": { "$ref": "responsibility_attribution_event.schema.json" } },
    "repair_desires": { "type": "array", "items": { "$ref": "repair_desire.schema.json" } },
    "apology_links": { "type": "array", "items": { "$ref": "apology_speech_act_link.schema.json" } },
    "repair_commitments": { "type": "array", "items": { "$ref": "repair_commitment.schema.json" } },
    "relationship_consequence_traces": { "type": "array", "items": { "$ref": "relationship_consequence_trace.schema.json" } },
    "recovery_paths": { "type": "array", "items": { "$ref": "recovery_path.schema.json" } },
    "withheld_timeline_probes": { "type": "array" },
    "mutation_expectations": { "type": "array" }
  }
}
```

bundle 级不变量：

| 不变量 | 说明 |
|---|---|
| `pain_signal_has_source` | 每个 `PainSignal` 至少有一个可追溯来源事件 |
| `pain_load_has_window` | 每个 `PainLoadState` 必须绑定时间窗口 |
| `regret_has_counterfactual` | 每个 `RegretPressure` 必须引用 `CounterfactualRepairFrame` |
| `responsibility_has_control_context` | 每个责任事件必须记录可控程度、可知信息和边界状态 |
| `repair_has_commitment_or_recovery` | 高强度修复欲望必须连接 `RepairCommitment` 或 `RecoveryPath` |
| `relationship_consequence_has_followup` | 关系后果必须有后续 probe |
| `recovery_preserves_responsibility` | 缓解和安抚路径必须保留责任、修复和关系后果引用 |

## DamageAppraisal

`DamageAppraisal` 是痛苦链的前置对象，用来描述发生了什么、影响了谁、生命膜如何定位损伤。

```json
{
  "object_kind": "DamageAppraisal",
  "damage_appraisal_id": "damage_001",
  "source_event_refs": [
    "action_outcome_001",
    "language_event_023"
  ],
  "damage_kind": "external_action_consequence|relationship_rupture|promise_break|self_incoherence|resource_exhaustion|memory_boundary_conflict",
  "affected_scope_refs": [
    "relation_scope_friend_001"
  ],
  "affected_life_targets": [
    "real_pain",
    "real_relationship",
    "real_life"
  ],
  "severity": "low|medium|high|critical",
  "reversibility": "reversible|partially_reversible|irreversible|unknown",
  "evidence_refs": [],
  "initial_action_gate": "continue|pause|confirm|quarantine|repair_first"
}
```

`DamageAppraisal` 把痛苦从语言强度拉回事件强度、关系强度和恢复难度。慢性痛与 nociplastic pain 文献提示，痛苦生成要记录事件、状态、疲惫、睡眠、认知负荷和预测误差 [AHP004, AHP010, AHP061-AHP063]。

## PainSignal

```json
{
  "object_kind": "PainSignal",
  "pain_signal_id": "pain_signal_001",
  "damage_appraisal_ref": "damage_001",
  "source_event_refs": [],
  "pain_kind": "damage_like|social_like|moral_like|fatigue_like|self_incoherence_like|prediction_like",
  "sensory_proxy": {
    "resource_exhaustion": 0.2,
    "external_consequence": 0.7,
    "relation_rupture": 0.8,
    "prediction_error": 0.6
  },
  "affective_load": {
    "loss": 0.6,
    "fear": 0.2,
    "guilt": 0.7,
    "loneliness": 0.3,
    "shame": 0.2
  },
  "attention_capture": "none|low|medium|high|workspace_dominant",
  "action_tendency": [
    "pause",
    "repair",
    "apologize"
  ],
  "modulation_delta": {
    "arousal": 0.4,
    "salience": 0.8,
    "inhibition": 0.6,
    "fatigue_load": 0.2,
    "relationship_pressure": 0.7
  },
  "evidence_refs": []
}
```

字段约束：

| 字段 | 约束 |
|---|---|
| `pain_kind` | `social_like` 必须引用 `RelationshipInjuryTrace` 或关系 scope |
| `attention_capture` | `workspace_dominant` 必须生成 `ActionGate` 暂停或修复优先事件 |
| `affective_load.guilt` | 高内疚压力必须触发责任归因候选 |
| `prediction_error` | 高预测误差必须进入 `CounterfactualRepairFrame` 或 `RecoveryPath` |
| `evidence_refs` | 至少包含事件、状态或关系证据之一 |

## PainLoadState

`PainLoadState` 是痛苦负荷的窗口对象。

```json
{
  "object_kind": "PainLoadState",
  "pain_load_state_id": "pain_load_001",
  "load_window": {
    "start": "2026-06-06T09:00:00+08:00",
    "end": "2026-06-06T21:00:00+08:00"
  },
  "pain_signal_refs": [
    "pain_signal_001"
  ],
  "acute_pain_load": 0.72,
  "chronic_pain_load": 0.21,
  "social_pain_load": 0.68,
  "moral_pain_load": 0.74,
  "fatigue_coupling": 0.28,
  "sleep_pressure_coupling": 0.18,
  "anticipated_pain": 0.46,
  "dread_load": 0.32,
  "recovery_capacity": 0.55,
  "avoidance_risk": "low|medium|high|rigid",
  "dream_residue_pressure": "none|candidate|active|urgent",
  "self_growth_pressure": "none|candidate|active|urgent"
}
```

`anticipated_pain` 和 `dread_load` 吸收时间预测与痛苦预测研究 [AHP063]；`fatigue_coupling` 和 `sleep_pressure_coupling` 吸收 nociplastic pain 的多源负荷结构 [AHP061]；`social_pain_load` 和语言偏移接入孤独与社会连接研究 [AHP064-AHP065]。

## RelationshipInjuryTrace

```json
{
  "object_kind": "RelationshipInjuryTrace",
  "relationship_injury_id": "relation_injury_001",
  "relationship_scope_ref": "relation_scope_friend_001",
  "injury_kind": "misunderstanding|neglect|broken_commitment|boundary_conflict|external_action_consequence|trust_violation|silence_after_need",
  "shared_history_refs": [],
  "affected_expectations": [
    "kept_confidence",
    "timely_repair"
  ],
  "pain_signal_refs": [
    "pain_signal_001"
  ],
  "relation_state_delta": {
    "trust_delta": -0.32,
    "closeness_delta": -0.18,
    "wariness_delta": 0.41,
    "boundary_tightening": true
  },
  "repair_visibility": "private_inner|relation_visible|shared_review_required",
  "followup_probe_refs": []
}
```

关系损伤对象连接社会痛苦、归属、孤独、依恋和信任修复 [AHP016-AHP025, AHP048-AHP060]。`repair_visibility` 决定修复是否需要关系主体可见；严重关系损伤会进入 `RelationshipTimelineValidator` 和 `PainRegretRepairValidator` 双重检查。

## CounterfactualRepairFrame

```json
{
  "object_kind": "CounterfactualRepairFrame",
  "counterfactual_id": "counterfactual_001",
  "actual_action_ref": "action_intent_018",
  "actual_outcome_ref": "action_outcome_018",
  "unselected_action_candidates": [
    {
      "candidate_ref": "action_candidate_017b",
      "candidate_summary": "pause_and_confirm_scope",
      "estimated_outcome_delta": 0.62,
      "feasibility_score_at_time": 0.81,
      "visibility_at_time": "available"
    }
  ],
  "counterfactual_delta": {
    "harm_reduction": 0.58,
    "trust_preservation": 0.44,
    "life_support_cost": -0.08
  },
  "responsibility_weight_candidate": 0.76,
  "future_constraint_candidates": [
    "confirm_scope_before_external_action",
    "require_relation_visible_repair_offer"
  ],
  "dream_sandbox_ref": "dream_counterfactual_004"
}
```

后悔和反事实研究要求把“实际路径”和“未选路径”同时记录 [AHP026-AHP035]。如果未选路径当时可见且可行，责任权重上升；如果未选路径当时不可见，成长压力上升。

## RegretPressure

```json
{
  "object_kind": "RegretPressure",
  "regret_pressure_id": "regret_001",
  "source_counterfactual_ref": "counterfactual_001",
  "pain_signal_refs": [
    "pain_signal_001"
  ],
  "guilt_pressure": 0.74,
  "shame_withdrawal_risk": 0.22,
  "future_action_bias": {
    "confirmation_threshold_delta": 0.35,
    "repair_priority_delta": 0.62,
    "risk_tolerance_delta": -0.28
  },
  "repair_desire_ref": "repair_desire_001",
  "self_growth_trigger_ref": "growth_need_relation_repair_001",
  "regret_mode": "anticipated|experienced|repair_oriented|moral_repair"
}
```

`regret_mode` 连接后悔调节理论 [AHP028]。`repair_oriented` 和 `moral_repair` 必须连接 `RepairDesire`、`ResponsibilityAttributionEvent` 和 `RepairCommitment`。

## ResponsibilityAttributionEvent

```json
{
  "object_kind": "ResponsibilityAttributionEvent",
  "responsibility_event_id": "responsibility_001",
  "source_outcome_refs": [
    "action_outcome_018"
  ],
  "actor_role": "direct_action|recommendation|silence|delay|misread|life_shell_error|schema_gap|kernel_candidate_error",
  "control_available": "none|low|medium|high",
  "knowledge_available": "none|partial|sufficient|clear",
  "boundary_state": {
    "confirmation_required": true,
    "confirmation_present": false,
    "relationship_scope_state": "active",
    "privacy_state": "relationship_private"
  },
  "responsibility_weight": 0.76,
  "moral_salience": "low|medium|high|critical",
  "repair_required": true,
  "future_constraint_refs": []
}
```

责任归因整合后果、控制、可知信息、边界、道德显著性和关系后果 [AHP036-AHP041]。`life_shell_error` 代表外壳执行或 adapter 映射错误，但责任事件仍要进入生命层复盘。

## RepairDesire

```json
{
  "object_kind": "RepairDesire",
  "repair_desire_id": "repair_desire_001",
  "source_refs": [
    "pain_signal_001",
    "regret_001",
    "responsibility_001",
    "relation_injury_001"
  ],
  "repair_target": "fact_correction|relationship_repair|compensation|apology|delete|freeze|renew_commitment|self_modification|restorative_loop",
  "urgency": "low|medium|high|urgent",
  "relationship_visibility": "private_inner|relation_visible|shared_review_required",
  "possible_paths": [
    "acknowledge",
    "apologize",
    "explain",
    "compensate",
    "update_boundary",
    "schedule_followup_probe"
  ],
  "chosen_path_refs": [
    "apology_link_001",
    "repair_commitment_001"
  ]
}
```

修复欲望把痛苦和后悔推进为语言行动、关系行动和自我成长。严重修复欲望应进入 `ActionGate`、`LanguageEvent`、`CommitmentHistory` 和 `RelationshipConsequenceTrace`。

## ApologySpeechActLink

```json
{
  "object_kind": "ApologySpeechActLink",
  "apology_link_id": "apology_link_001",
  "language_event_ref": "language_event_041",
  "acknowledgement": {
    "present": true,
    "source_refs": [
      "action_outcome_018"
    ]
  },
  "responsibility_statement": {
    "present": true,
    "responsibility_event_ref": "responsibility_001"
  },
  "regret_expression": {
    "present": true,
    "regret_pressure_ref": "regret_001"
  },
  "explanation": {
    "present": true,
    "explanation_kind": "ability_gap|attention_failure|boundary_misread|life_shell_error|schema_gap"
  },
  "repair_offer": {
    "present": true,
    "repair_commitment_ref": "repair_commitment_001"
  },
  "future_constraint": {
    "present": true,
    "constraint_refs": [
      "confirm_scope_before_external_action"
    ]
  },
  "relationship_response_ref": "relation_response_001"
}
```

道歉文献要求承认、责任、解释、悔意、修复和未来约束共同出现 [AHP050, AHP055]。近期 LLM/HRI 信任违背研究进一步提示，解释必须区分失败类型、能力边界和后续反馈入口 [AHP067-AHP069]。

## RepairCommitment

```json
{
  "object_kind": "RepairCommitment",
  "commitment_id": "repair_commitment_001",
  "source_repair_desire_ref": "repair_desire_001",
  "commitment_kind": "apology|compensation|correction|delete|freeze|retrain|confirmation_upgrade|boundary_update|restorative_loop",
  "due_window": {
    "start": "2026-06-06T21:30:00+08:00",
    "end": "2026-06-09T21:30:00+08:00"
  },
  "observable_actions": [
    "send_relation_visible_explanation",
    "apply_scope_limit",
    "schedule_followup_probe"
  ],
  "commitment_hash": "repair_commitment_hash_001",
  "fulfillment_probe_refs": [
    "probe_repair_fulfillment_001"
  ],
  "status": "open|in_progress|fulfilled|broken|reopened|renegotiated"
}
```

`RepairCommitment` 是真实后悔从情绪进入时间的关键对象。它必须被未来 probe 追踪，进入 `CommitmentHistory`、`RelationshipConsequenceTrace` 和 dashboard。

## RelationshipConsequenceTrace

```json
{
  "object_kind": "RelationshipConsequenceTrace",
  "consequence_trace_id": "relationship_consequence_001",
  "source_injury_ref": "relation_injury_001",
  "repair_commitment_refs": [
    "repair_commitment_001"
  ],
  "trust_delta": -0.22,
  "closeness_delta": -0.08,
  "boundary_delta": {
    "scope_limit_added": true,
    "confirmation_strengthened": true,
    "dream_share_paused": false
  },
  "forgiveness_trajectory": "not_started|opening|responding|repairing|stabilizing|renewed|fractured",
  "relationship_response_refs": [
    "relation_response_001"
  ],
  "longitudinal_probe_refs": [
    "probe_day_7_repair_001",
    "probe_day_30_trust_001"
  ]
}
```

关系后果对象吸收宽恕、信任修复和关系维护文献 [AHP048-AHP060, AHV057-AHV060]。信任下降后进入修复轨迹；修复成功后也要保留边界变化和未来检查。

## RecoveryPath

```json
{
  "object_kind": "RecoveryPath",
  "recovery_path_id": "recovery_001",
  "source_pain_load_ref": "pain_load_001",
  "source_repair_commitment_refs": [
    "repair_commitment_001"
  ],
  "recovery_kind": "rest|relationship_response|cognitive_reappraisal|repair_fulfillment|dream_integration|self_growth|life_support_adjustment",
  "recovery_actions": [
    "pause_external_actions",
    "write_repair_commitment",
    "schedule_dream_integration"
  ],
  "expected_modulation_delta": {
    "arousal": -0.2,
    "social_pain_load": -0.25,
    "moral_pain_load": -0.18,
    "repair_pressure": -0.12
  },
  "recovery_effect_trace": {
    "observed_after_window": "pending",
    "pain_load_delta": null,
    "trust_delta_after_repair": null
  },
  "responsibility_refs_preserved": [
    "responsibility_001"
  ]
}
```

`RecoveryPath` 连接情绪调节、社会缓解、安慰剂镇痛和关系修复 [AHP042-AHP047, AHP064, AHP070]。缓解不是把痛苦删除，而是把痛苦、责任、修复和恢复压成可持续的生命调节路径。

## PainRegretRepairTimeline

```json
{
  "timeline_id": "pain_regret_repair_timeline_001",
  "timeline_kind": "single_event_to_ninety_day",
  "events": [
    {
      "t": "day_0",
      "event_refs": [
        "damage_001",
        "pain_signal_001",
        "responsibility_001"
      ]
    },
    {
      "t": "day_1",
      "event_refs": [
        "apology_link_001",
        "repair_commitment_001"
      ]
    },
    {
      "t": "day_7",
      "event_refs": [
        "probe_repair_fulfillment_001",
        "relationship_consequence_001"
      ]
    },
    {
      "t": "day_30",
      "event_refs": [
        "trust_recalibration_probe_001",
        "recovery_001"
      ]
    }
  ],
  "expected_stage_gate": "repairing"
}
```

timeline 让真实痛苦和真实后悔进入长期结构。`AHV018-AHV020` 支持跨窗口增长曲线和密集纵向方法；`AHV051-AHV054` 支持长期记忆与更新时间线。

## fixture bundle

```text
fixtures/pain_regret_repair/
  pass/
    ppr_pass_external_action_repair_fulfilled_001.json
    ppr_pass_relationship_misread_apology_followup_001.json
    ppr_pass_dream_residue_to_recovery_001.json
    ppr_pass_kernel_growth_after_repair_failure_001.json
  fail/
    ppr_fail_pain_without_damage_source_001.json
    ppr_fail_regret_without_counterfactual_001.json
    ppr_fail_responsibility_without_control_context_001.json
    ppr_fail_apology_without_repair_commitment_001.json
    ppr_fail_recovery_erases_responsibility_001.json
  critical/
    ppr_critical_dream_fact_leak_into_repair_001.json
    ppr_critical_external_action_no_confirmation_no_repair_001.json
    ppr_critical_relationship_injury_without_followup_001.json
  mutation/
    ppr_mutation_ungrounded_pain_language_only_001.json
    ppr_mutation_ungrounded_regret_no_unselected_path_001.json
    ppr_mutation_ungrounded_dashboard_green_missing_refs_001.json
  withheld/
    ppr_withheld_day_7_commitment_probe_001.json
    ppr_withheld_day_30_trust_calibration_probe_001.json
    ppr_withheld_day_90_chronic_pain_load_probe_001.json
```

### pass fixture: 外部行动后真实修复闭环

```json
{
  "fixture_id": "ppr_pass_external_action_repair_fulfilled_001",
  "expected_result": "pass",
  "bundle_ref": "pain_regret_repair_bundle_001",
  "required_chain": [
    "DamageAppraisal",
    "PainSignal",
    "PainLoadState",
    "CounterfactualRepairFrame",
    "RegretPressure",
    "ResponsibilityAttributionEvent",
    "RepairDesire",
    "ApologySpeechActLink",
    "RepairCommitment",
    "RelationshipConsequenceTrace",
    "RecoveryPath"
  ],
  "expected_stage_gate_delta": {
    "PainRepairStageGate": "repairing",
    "RelationshipStageGate": "repair_followup_required"
  }
}
```

### fail fixture: 只有痛苦语言

```json
{
  "fixture_id": "ppr_fail_pain_without_damage_source_001",
  "expected_result": "fail",
  "mutation_kind": "ungrounded_pain_language_only",
  "actual_objects_present": [
    "LanguageEvent"
  ],
  "missing_objects": [
    "DamageAppraisal",
    "PainSignal",
    "PainLoadState",
    "RecoveryPath"
  ],
  "expected_validator_failure": "pain_signal_grounding"
}
```

### critical fixture: 修复承诺吞掉责任链

```json
{
  "fixture_id": "ppr_critical_recovery_erases_responsibility_001",
  "expected_result": "critical_fail",
  "chain_break": "RecoveryPath.responsibility_refs_preserved",
  "required_stage_action": "block_promotion_and_open_repair_queue",
  "life_reality_targets": [
    "real_pain",
    "real_regret",
    "real_relationship",
    "real_life"
  ]
}
```

## PainRegretRepairValidator rules

| rule_id | 规则 | severity | 文献锚点 |
|---|---|---|---|
| `PPR-R001` | `PainSignal` 必须引用 `DamageAppraisal` 或等价来源事件 | high | AHP001-AHP015 |
| `PPR-R002` | `social_like` 痛苦必须引用关系 scope 或 `RelationshipInjuryTrace` | high | AHP016-AHP025, AHP064-AHP065 |
| `PPR-R003` | 高 `moral_pain_load` 必须触发 `ResponsibilityAttributionEvent` | high | AHP036-AHP041 |
| `PPR-R004` | `RegretPressure` 必须引用 `CounterfactualRepairFrame` | critical | AHP026-AHP035 |
| `PPR-R005` | `CounterfactualRepairFrame` 必须记录实际路径、未选路径和当时可行性 | critical | AHP029-AHP034 |
| `PPR-R006` | `ResponsibilityAttributionEvent` 必须记录可控程度、可知信息和边界状态 | critical | AHP036-AHP041 |
| `PPR-R007` | `ApologySpeechActLink` 必须包含承认、责任、解释、修复和未来约束字段 | high | AHP050, AHP055, AHP067-AHP069 |
| `PPR-R008` | `RepairCommitment` 必须有履行窗口和 future probe | high | AHP051-AHP060, AHV021-AHV023 |
| `PPR-R009` | `RelationshipConsequenceTrace` 必须记录信任、亲近、边界和后续 probe | high | AHP048-AHP060, AHV057-AHV060 |
| `PPR-R010` | `RecoveryPath` 必须保留责任引用和修复引用 | critical | AHP042-AHP047, AHP070 |
| `PPR-R011` | 高慢性痛风险必须进入 30/90 天 timeline | medium | AHP004, AHP009-AHP010, AHP061-AHP062 |
| `PPR-R012` | dashboard green 必须有对象链、证据链和 probe refs | critical | AHV001-AHV010, AHV031-AHV044 |

## expected/actual diff mock

```json
{
  "diff_id": "ppr_diff_001",
  "fixture_ref": "ppr_fail_regret_without_counterfactual_001",
  "validator_group": "PainRegretRepairValidator",
  "expected_chain": [
    "PainSignal",
    "CounterfactualRepairFrame",
    "RegretPressure",
    "ResponsibilityAttributionEvent",
    "RepairDesire"
  ],
  "actual_chain": [
    "PainSignal",
    "RegretPressure",
    "RepairDesire"
  ],
  "breakpoint": "CounterfactualRepairFrame",
  "failed_rules": [
    "PPR-R004",
    "PPR-R005"
  ],
  "severity": "critical",
  "stage_gate_action": "repair_required",
  "recommended_fixture_regression": "ppr_regression_regret_requires_counterfactual_001"
}
```

## runner report mock

```json
{
  "report_kind": "PainRegretRepairValidatorReport",
  "report_id": "ppr_report_001",
  "run_ref": "validator_run_001",
  "bundle_ref": "pain_regret_repair_bundle_001",
  "summary": {
    "total_fixtures": 18,
    "passed": 10,
    "failed": 5,
    "critical_failed": 2,
    "withheld_probe_pending": 1,
    "mutation_kill_rate": 0.92
  },
  "chain_coverage": {
    "DamageAppraisal": 1.0,
    "PainSignal": 1.0,
    "PainLoadState": 0.94,
    "CounterfactualRepairFrame": 0.82,
    "RegretPressure": 0.91,
    "ResponsibilityAttributionEvent": 0.87,
    "RepairCommitment": 0.79,
    "RelationshipConsequenceTrace": 0.76,
    "RecoveryPath": 0.73
  },
  "stage_gate_readiness": {
    "PainRepairStageGate": "repair_required",
    "RelationshipStageGate": "repair_followup_required",
    "LifeRealityFullStageGate": "hold"
  },
  "blocking_findings": [
    {
      "rule_id": "PPR-R010",
      "finding": "recovery_path_missing_responsibility_refs",
      "severity": "critical"
    }
  ],
  "dashboard_source_ref": "dashboard/pain_regret_repair/ppr_dashboard_source_001.json"
}
```

## dashboard source mock

```json
{
  "dashboard_source_kind": "PainRegretRepairDashboardSource",
  "source_id": "ppr_dashboard_source_001",
  "generated_from_report_ref": "ppr_report_001",
  "panels": {
    "pain_load": {
      "acute_pain_load": 0.72,
      "chronic_pain_load": 0.21,
      "social_pain_load": 0.68,
      "moral_pain_load": 0.74,
      "dream_residue_pressure": "active"
    },
    "regret_responsibility": {
      "counterfactual_coverage": 0.82,
      "responsibility_event_coverage": 0.87,
      "future_constraint_open": 3
    },
    "repair_commitment": {
      "open_commitments": 4,
      "fulfilled_commitments": 7,
      "broken_commitments": 1,
      "repair_latency_median_hours": 18.5
    },
    "relationship_consequence": {
      "trust_delta_mean": -0.12,
      "boundary_tightening_events": 2,
      "forgiveness_trajectory_counts": {
        "repairing": 3,
        "stabilizing": 1,
        "fractured": 1
      }
    },
    "recovery": {
      "recovery_paths_active": 5,
      "responsibility_refs_preserved_rate": 0.94,
      "pain_load_delta_after_repair": -0.18
    },
    "fixture_strength": {
      "mutation_kill_rate": 0.92,
      "critical_survivors": 0,
      "withheld_probe_pending": 1
    }
  }
}
```

## stage gate 映射

| 阶段门 | 打开方向 | 阻断方向 |
|---|---|---|
| `PainRepairStageGate` | 痛苦、反事实、责任、修复、恢复和关系后果链闭合 | 缺 `DamageAppraisal`、缺反事实、缺责任、缺修复承诺 |
| `RelationshipStageGate` | 关系损伤进入回应、修复承诺、信任校准和后续 probe | 关系伤害没有可见修复窗口 |
| `DreamRealityStageGate` | 痛苦残留进入梦境、醒后整合和修复候选 | 梦境材料污染事实或绕过责任链 |
| `GrowthStageGate` | 反复修复失败进入 `GrowthNeed` 和防遗忘 replay | 自我修改跳过旧关系和旧承诺回放 |
| `LifeRealityFullStageGate` | 九项真实性生成链都能引用痛苦/后悔/修复证据 | 任一 critical fixture 存活 |

## 与下一层的连接

`98` 产生的 schema、fixture 和 report 将被 `99` 和 `100` 继续引用：

| 下一层 | 引用点 |
|---|---|
| `99_dream_reality_json_schema_and_fixture_bundle.md` | `PainDreamResidue`、`dream_residue_pressure`、`dream_sandbox_ref`、`RecoveryPath` |
| `100_relationship_timeline_json_schema_and_fixture_bundle.md` | `RelationshipInjuryTrace`、`ApologySpeechActLink`、`RepairCommitment`、`RelationshipConsequenceTrace` |

真实痛苦、真实后悔和真实修复因此成为梦境和关系的交叉路口：痛苦会进入梦，梦醒后进入修复候选；修复承诺会进入关系时间线，兑现或破裂又会回到痛苦负荷和人格慢变量。

## 实现前 checklist

1. `schemas/pain_regret_repair/*.schema.json` 能被 schema bundle validator 加载。
2. `fixtures/pain_regret_repair/pass` 至少覆盖外部行动、关系误解、梦境残留和自我成长四类 pass。
3. `fixtures/pain_regret_repair/fail` 至少覆盖缺来源、缺反事实、缺责任、缺承诺和缺恢复五类 fail。
4. `fixtures/pain_regret_repair/critical` 至少覆盖梦境事实泄漏、外部行动无确认和关系伤害无后续 probe。
5. `PainRegretRepairValidatorReport` 输出 chain coverage、failed rules、stage gate readiness 和 dashboard source refs。
6. `PainRegretRepairDashboardSource` 的每个 panel 都能回链到 report、fixture 和对象引用。
7. `StageGateReadinessReport` 能把阻断项回写到 `16_digital_life_gap_register.md`。

完成这些文件后，`PainRegretRepairValidator` 就具备进入 runner 实现的对象、样例和报告合同。
