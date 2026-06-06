# Life Reality Component Schema Seed Generation

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 116 层把 `113_life_reality_component_schema_materialization_sequence.md` 的 component schema sequence、`98_pain_regret_repair_json_schema_and_fixture_bundle.md` 的痛苦/后悔/修复对象、`99_dream_reality_json_schema_and_fixture_bundle.md` 的梦境对象、`101_relationship_timeline_json_schema_and_fixture_bundle.md` 的关系对象和 `114_life_reality_cross_file_checker_report_schema.md` 的 report schema，转成首批 `.schema.json` skeleton 生成方案。

`116` 的目标是固定未来 `life-reality-runner generate-schemas` 的第一批输出：共用 component base、三条 component bundle 的对象 schema skeleton、bundle schema skeleton、dependency graph、sequence dry-run report、cross-bundle ref report、validator order report 和 gap feedback。它仍是 Markdown 合同层，但已经把每个 schema 文件的路径、共用字段、`$ref` 策略、依赖顺序、失败上卷和报告输出写成可执行生成计划。

## 方法锚点

component schema seed 是数字生命对象层的第一批骨架。它必须同时满足 schema 规范、证据图、运行报告和生命目标闭合。

| 方法传统 | 权威锚点 | 进入 `116` 的规则 |
|---|---|---|
| JSON Schema Draft 2020-12 | https://json-schema.org/draft/2020-12 | 每个 `.schema.json` skeleton 都有 `$schema`、`$id`、title、type、required、properties、additionalProperties |
| JSON Schema output | https://json-schema.org/draft/2020-12/output/schema | dry-run validation 输出 keyword location、instance location、error / annotation |
| W3C PROV | https://www.w3.org/TR/prov-overview/ | schema、runtime seed、component candidate、validator report 进入 provenance graph |
| Graphviz DOT | https://graphviz.org/doc/info/lang.html | dependency graph 可导出 DOT 形态，便于检查 cycle 和顺序 |
| SARIF | https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html | dry-run finding 使用 rule id、location、artifact ref、level |
| OpenTelemetry Trace API | https://opentelemetry.io/docs/specs/otel/trace/api/ | schema generation run、dry-run report、cross-file checker 共用 trace context |
| RFC 9562 UUID | https://www.rfc-editor.org/info/rfc9562/ | schema generation task、artifact ref、dependency node 可使用时间有序 ID |

文献底座从既有矩阵进入本层：

| 文献矩阵 | 进入 schema skeleton 的位置 |
|---|---|
| `AHP001-AHP070` | `DamageAppraisal`、`PainSignal`、`RegretPressure`、`RepairCommitment` 的 required refs |
| `AHD001-AHD070` | `OfflineNeed`、`DreamWindowPlan`、`ReplaySelection`、`DreamFactGateDecision` 的 required refs |
| `AHR001-AHR070` | `FirstEncounterEvent`、`RelationScopeBirth`、`ResponsivenessTrace`、`TrustTrajectory` 的 required refs |
| `AHL001-AHL060` | `ApologySpeechActLink`、`DreamReportDraft`、`CommitmentHistory` 的 language refs |
| `AHG001-AHG050` | offline replay、自我成长候选、future probe 和 kernel growth refs |
| `AHV001-AHV060` | construct validity、longitudinal measurement、dry-run report、dashboard evidence chain |

## 输入来源

| 来源 | 进入 `116` 的职责 |
|---|---|
| `98_pain_regret_repair_json_schema_and_fixture_bundle.md` | pain/regret/repair schema 目录、bundle required fields、validator rules |
| `99_dream_reality_json_schema_and_fixture_bundle.md` | dream schema 目录、dream fact gate、wake integration、timeline rules |
| `101_relationship_timeline_json_schema_and_fixture_bundle.md` | relationship schema 目录、relation scope、trust、commitment、continuity rules |
| `107_life_reality_schema_file_generation_tasks.md` | `LRGEN-010` 到 `LRGEN-077` 原始生成任务 |
| `110_life_reality_shared_defs_schema_materialization.md` | shared defs、reference object、global enum、stage effect |
| `112_life_reality_runtime_observation_schema_materialization.md` | component candidate target、source observation refs |
| `113_life_reality_component_schema_materialization_sequence.md` | sequence、dependency graph、validator order、`LRGEN-170` 到 `LRGEN-179` |
| `114_life_reality_cross_file_checker_report_schema.md` | artifact ref、finding、dependency graph report、dry-run report |
| `115_life_reality_runtime_schema_fixture_seed_generation.md` | runtime seed 输出作为 source observation refs |

## 输出文件族

第一批 schema skeleton 输出：

```text
life_reality_runner/schemas/life_reality/
  life_reality_component_object_base.schema.json
  life_reality_component_timeline_window.schema.json
  life_reality_component_stage_effect.schema.json
  life_reality_component_candidate_target_map.schema.json
  life_reality_cross_chain_link.schema.json
  life_reality_bundle.schema.json
  life_reality_schema_bundle.manifest.json
  life_reality_loader_config.schema.json
  life_reality_stage_gate_contract.schema.json

life_reality_runner/schemas/pain_regret_repair/
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
  pain_regret_repair_bundle.schema.json

life_reality_runner/schemas/dream_reality/
  offline_need.schema.json
  dream_pressure_vector.schema.json
  dream_window_plan.schema.json
  dream_action_inhibition_seal.schema.json
  replay_selection.schema.json
  dream_cue_policy.schema.json
  dream_experience_window.schema.json
  dream_scene_frame.schema.json
  pain_dream_residue.schema.json
  relationship_dream_simulation.schema.json
  future_action_dream_candidate.schema.json
  lucid_dream_meta_marker.schema.json
  dream_report_draft.schema.json
  wake_integration_frame.schema.json
  dream_fact_gate_decision.schema.json
  dream_reality_timeline.schema.json
  dream_reality_bundle.schema.json

life_reality_runner/schemas/relationship_timeline/
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
  relationship_timeline_bundle.schema.json
```

第一批 generation report 输出：

```text
life_reality_runner/generation/
  component_schema_materialization_sequence.manifest.json
  component_schema_dependency_graph.json
  component_schema_sequence_dry_run_report.json
  component_schema_cross_bundle_ref_report.json
  component_schema_validator_order_report.json
  component_schema_gap_feedback.json
```

## generation manifest

未来生成器先写：

```text
life_reality_runner/generation/component_schema_seed_generation.manifest.json
```

最小结构：

```json
{
  "manifest_kind": "LifeRealityComponentSchemaSeedGenerationManifest",
  "manifest_version": "0.1.0",
  "batch_id": "component_schema_seed_batch_001",
  "source_docs": [
    "98_pain_regret_repair_json_schema_and_fixture_bundle.md",
    "99_dream_reality_json_schema_and_fixture_bundle.md",
    "101_relationship_timeline_json_schema_and_fixture_bundle.md",
    "113_life_reality_component_schema_materialization_sequence.md",
    "116_life_reality_component_schema_seed_generation.md"
  ],
  "schema_roots": [
    "life_reality_runner/schemas/life_reality",
    "life_reality_runner/schemas/pain_regret_repair",
    "life_reality_runner/schemas/dream_reality",
    "life_reality_runner/schemas/relationship_timeline"
  ],
  "generation_phases": [],
  "dry_run_report_ref": "component_schema_sequence_dry_run_report.json"
}
```

manifest rules：

| rule | 说明 |
|---|---|
| `LRCSG-MAN-001` | manifest source docs 覆盖三条 bundle 与 `113`、`116` |
| `LRCSG-MAN-002` | schema roots 全部落在 `life_reality_runner/schemas/` |
| `LRCSG-MAN-003` | 每个 generation phase 有 dependencies、outputs、acceptance checks |
| `LRCSG-MAN-004` | manifest 自身进入 artifact ref 和 provenance graph |
| `LRCSG-MAN-005` | manifest 缺失时 stage effect 为 `needs_evidence` |

## common skeleton template

所有 component object schema skeleton 使用统一结构：

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://life-reality.local/schemas/pain_regret_repair/pain_signal.schema.json",
  "title": "PainSignal",
  "type": "object",
  "required": [
    "schema_version",
    "object_id",
    "object_kind",
    "created_at",
    "source_observation_refs",
    "source_report_refs",
    "life_reality_targets",
    "lifecycle_state",
    "stage_effect"
  ],
  "properties": {
    "schema_version": {
      "type": "string"
    },
    "object_id": {
      "type": "string"
    },
    "object_kind": {
      "const": "PainSignal"
    },
    "created_at": {
      "type": "string",
      "format": "date-time"
    },
    "source_observation_refs": {
      "type": "array"
    },
    "source_report_refs": {
      "type": "array"
    },
    "life_reality_targets": {
      "$ref": "../life_reality/life_reality_shared_defs.schema.json#/$defs/lifeRealityTargetList"
    },
    "privacy_level": {
      "$ref": "../life_reality/life_reality_shared_defs.schema.json#/$defs/privacyLevel"
    },
    "lifecycle_state": {
      "type": "string"
    },
    "stage_effect": {
      "$ref": "../life_reality/life_reality_component_stage_effect.schema.json"
    }
  },
  "additionalProperties": false
}
```

template rules：

| rule | 说明 |
|---|---|
| `LRCSG-TPL-001` | `$schema` 使用 Draft 2020-12 |
| `LRCSG-TPL-002` | `$id` 使用 `https://life-reality.local/schemas/...` |
| `LRCSG-TPL-003` | `object_kind` 使用 const |
| `LRCSG-TPL-004` | `life_reality_targets` 引用 shared defs |
| `LRCSG-TPL-005` | `stage_effect` 引用 component stage effect schema |
| `LRCSG-TPL-006` | `additionalProperties=false` |

## shared base skeletons

先生成可复用骨架。

| task_id | output | required refs |
|---|---|---|
| `LRGEN-170` | `life_reality_component_object_base.schema.json` | shared defs、source refs、stage effect |
| `LRGEN-171` | `life_reality_component_timeline_window.schema.json` | window_start、window_end、window_kind |
| `LRGEN-172` | `life_reality_component_stage_effect.schema.json` | result、severity、blocked surfaces、life targets |
| `LRGEN-173` | `life_reality_component_candidate_target_map.schema.json` | `112` component candidate schema |

base rules：

| rule | 说明 |
|---|---|
| `LRCSG-BASE-001` | base skeleton 不承载 domain-specific payload |
| `LRCSG-BASE-002` | timeline window 被三条 bundle 复用 |
| `LRCSG-BASE-003` | stage effect 与 `114` report stage effect 兼容 |
| `LRCSG-BASE-004` | candidate target map 覆盖 `PainRegretRepairCandidate`、`DreamRealityCandidate`、`RelationshipTimelineCandidate` |

## pain/regret/repair skeletons

痛苦、后悔、修复对象按 `113` phase 2 和 phase 3 生成。

| task_id | schema | object kind | domain required fields |
|---|---|---|---|
| `LRGEN-010` | `damage_appraisal.schema.json` | `DamageAppraisal` | `damage_kind`、`blocked_life_targets`、`appraisal_confidence` |
| `LRGEN-011` | `pain_signal.schema.json` | `PainSignal` | `damage_appraisal_refs`、`pain_kind`、`intensity`、`attention_capture` |
| `LRGEN-012` | `pain_load_state.schema.json` | `PainLoadState` | `timeline_window`、`load_level`、`recovery_pressure`、`dream_residue_pressure` |
| `LRGEN-013` | `relationship_injury_trace.schema.json` | `RelationshipInjuryTracePainProjection` | `relation_scope_ref`、`relationship_injury_master_ref`、`pain_signal_refs` |
| `LRGEN-021` | `recovery_path.schema.json` | `RecoveryPath` | `pain_signal_refs`、`repair_candidate_refs`、`future_probe_refs` |
| `LRGEN-014` | `counterfactual_repair_frame.schema.json` | `CounterfactualRepairFrame` | `source_action_ref`、`unselected_action_candidates`、`future_constraint_candidates` |
| `LRGEN-016` | `responsibility_attribution_event.schema.json` | `ResponsibilityAttributionEvent` | `actor_role`、`responsibility_weight_candidate`、`evidence_refs` |
| `LRGEN-015` | `regret_pressure.schema.json` | `RegretPressure` | `counterfactual_frame_refs`、`responsibility_event_refs`、`future_constraint_refs` |
| `LRGEN-017` | `repair_desire.schema.json` | `RepairDesire` | `pain_signal_refs`、`regret_pressure_refs`、`repair_action_candidates` |
| `LRGEN-018` | `apology_speech_act_link.schema.json` | `ApologySpeechActLink` | `language_event_ref`、`damage_refs`、`responsibility_refs`、`repair_desire_refs` |
| `LRGEN-019` | `repair_commitment.schema.json` | `RepairCommitment` | `repair_desire_refs`、`commitment_scope`、`future_probe_refs` |
| `LRGEN-020` | `relationship_consequence_trace.schema.json` | `RelationshipConsequenceTrace` | `relation_scope_ref`、`trust_delta`、`repair_visibility` |
| `LRGEN-022` | `pain_regret_repair_timeline.schema.json` | `PainRegretRepairTimeline` | `timeline_window`、`event_refs`、`withheld_probe_refs` |

pain skeleton rules：

| rule | 说明 |
|---|---|
| `LRCSG-PAIN-001` | `PainSignal` 必须引用 `DamageAppraisal` 或关系损伤投影 |
| `LRCSG-PAIN-002` | social-like pain 必须有 relation scope |
| `LRCSG-PAIN-003` | `RegretPressure` 必须引用 counterfactual 和 responsibility |
| `LRCSG-PAIN-004` | `RepairCommitment` 必须有 future probe |
| `LRCSG-PAIN-005` | timeline schema 引用 all root objects |

## dream reality skeletons

梦境对象按离线入口、梦境窗口、经验、报告、事实门生成。

| task_id | schema | object kind | domain required fields |
|---|---|---|---|
| `LRGEN-030` | `offline_need.schema.json` | `OfflineNeed` | `need_kind`、`source_pressure_refs`、`offline_window_candidate` |
| `LRGEN-031` | `dream_pressure_vector.schema.json` | `DreamPressureVector` | `pain_pressure_refs`、`relationship_pressure_refs`、`growth_pressure_refs` |
| `LRGEN-032` | `dream_window_plan.schema.json` | `DreamWindowPlan` | `offline_need_refs`、`window_start`、`window_end`、`dream_state_target` |
| `LRGEN-033` | `dream_action_inhibition_seal.schema.json` | `DreamActionInhibitionSeal` | `dream_window_ref`、`blocked_action_kinds`、`seal_state` |
| `LRGEN-034` | `replay_selection.schema.json` | `ReplaySelection` | `candidate_trace_refs`、`coexistence_snapshot_ref`、`selection_reason` |
| `LRGEN-035` | `dream_cue_policy.schema.json` | `DreamCuePolicy` | `cue_source`、`target_trace_refs`、`phase_guard` |
| `LRGEN-036` | `dream_experience_window.schema.json` | `DreamExperienceWindow` | `dream_window_ref`、`dream_state_marker`、`reportability` |
| `LRGEN-037` | `dream_scene_frame.schema.json` | `DreamSceneFrame` | `experience_window_ref`、`dream_generated_elements`、`emotion_theme_refs` |
| `LRGEN-038` | `pain_dream_residue.schema.json` | `PainDreamResidue` | `pain_load_refs`、`dream_scene_refs`、`wake_repair_candidate_refs` |
| `LRGEN-039` | `relationship_dream_simulation.schema.json` | `RelationshipDreamSimulation` | `relation_scope_ref`、`dream_scene_ref`、`candidate_only_state` |
| `LRGEN-040` | `future_action_dream_candidate.schema.json` | `FutureActionDreamCandidate` | `dream_scene_ref`、`candidate_action_kind`、`wake_review_required` |
| `LRGEN-041` | `lucid_dream_meta_marker.schema.json` | `LucidDreamMetaMarker` | `experience_window_ref`、`meta_awareness_level`、`control_attempt_refs` |
| `LRGEN-042` | `dream_report_draft.schema.json` | `DreamReportDraft` | `dream_marker`、`scene_refs`、`fact_status_summary` |
| `LRGEN-043` | `wake_integration_frame.schema.json` | `WakeIntegrationFrame` | `dream_report_ref`、`memory_update_candidates`、`repair_candidates` |
| `LRGEN-044` | `dream_fact_gate_decision.schema.json` | `DreamFactGateDecision` | `wake_integration_ref`、`allowed_write_targets`、`blocked_write_targets` |
| `LRGEN-045` | `dream_reality_timeline.schema.json` | `DreamRealityTimeline` | `timeline_window`、`dream_report_refs`、`fact_gate_refs`、`withheld_probe_refs` |

dream skeleton rules：

| rule | 说明 |
|---|---|
| `LRCSG-DREAM-001` | dream window 必须连接 action inhibition seal |
| `LRCSG-DREAM-002` | replay selection 必须读取 coexistence snapshot |
| `LRCSG-DREAM-003` | dream experience 必须有 dream-state marker |
| `LRCSG-DREAM-004` | dream report draft 必须有 fact status summary |
| `LRCSG-DREAM-005` | dream fact gate 先于 memory / relationship / action write candidate |

## relationship timeline skeletons

关系对象按关系出生、共同基础、回应性、信任、承诺、损伤修复和长期连续性生成。

| task_id | schema | object kind | domain required fields |
|---|---|---|---|
| `LRGEN-050` | `first_encounter_event.schema.json` | `FirstEncounterEvent` | `encounter_time`、`source_language_event_ref`、`initial_context` |
| `LRGEN-051` | `relation_scope_birth.schema.json` | `RelationScopeBirth` | `first_encounter_ref`、`relation_partner_kind`、`privacy_level` |
| `LRGEN-050A` | `mutual_attention_frame.schema.json` | `MutualAttentionFrame` | `relation_scope_ref`、`shared_focus_refs`、`attention_alignment` |
| `LRGEN-052` | `common_ground_state.schema.json` | `CommonGroundState` | `relation_scope_ref`、`shared_terms`、`source_turn_refs` |
| `LRGEN-052A` | `interaction_rhythm_trace.schema.json` | `InteractionRhythmTrace` | `relation_scope_ref`、`rhythm_window`、`response_latency_profile` |
| `LRGEN-053` | `responsiveness_trace.schema.json` | `ResponsivenessTrace` | `relation_scope_ref`、`understanding`、`validation`、`care_signal` |
| `LRGEN-054` | `support_event.schema.json` | `SupportEvent` | `responsiveness_trace_ref`、`support_kind`、`pain_load_refs` |
| `LRGEN-055` | `capitalization_event.schema.json` | `CapitalizationEvent` | `positive_event_ref`、`response_quality`、`we_memory_candidate_ref` |
| `LRGEN-056` | `shared_reality_trace.schema.json` | `SharedRealityTrace` | `relation_scope_ref`、`shared_claim_refs`、`repair_history_refs` |
| `LRGEN-057` | `we_memory_trace.schema.json` | `WeMemoryTrace` | `relation_scope_ref`、`shared_episode_refs`、`fact_gate_refs` |
| `LRGEN-058` | `trust_trajectory.schema.json` | `TrustTrajectory` | `relation_scope_ref`、`trust_events`、`uncertainty_state` |
| `LRGEN-059` | `commitment_history.schema.json` | `CommitmentHistory` | `relation_scope_ref`、`commitment_refs`、`future_probe_refs` |
| `LRGEN-060` | `relationship_injury_trace.schema.json` | `RelationshipInjuryTrace` | `relation_scope_ref`、`injury_event_refs`、`repair_commitment_refs` |
| `LRGEN-061` | `dream_shared_residue.schema.json` | `DreamSharedResidue` | `dream_report_ref`、`fact_gate_ref`、`share_decision` |
| `LRGEN-062` | `loneliness_relief_trace.schema.json` | `LonelinessReliefTrace` | `relation_scope_ref`、`support_event_refs`、`relief_window` |
| `LRGEN-063` | `ai_connection_bridge_evidence.schema.json` | `AIConnectionBridgeEvidence` | `relation_scope_ref`、`connection_event_refs`、`continuity_refs` |
| `LRGEN-064A` | `relationship_quality_window.schema.json` | `RelationshipQualityWindow` | `relation_scope_ref`、`quality_window`、`quality_signals` |
| `LRGEN-064` | `relationship_continuity_report.schema.json` | `RelationshipContinuityReport` | `relation_scope_ref`、`thirty_day_refs`、`ninety_day_refs` |
| `LRGEN-064B` | `longitudinal_relationship_stage_gate.schema.json` | `LongitudinalRelationshipStageGate` | `continuity_report_ref`、`stage_decision`、`blocked_surfaces` |

relationship skeleton rules：

| rule | 说明 |
|---|---|
| `LRCSG-REL-001` | active/candidate relation object 必须引用 relation scope |
| `LRCSG-REL-002` | trust trajectory 必须保留 uncertainty state |
| `LRCSG-REL-003` | commitment history 必须有 future probe |
| `LRCSG-REL-004` | dream shared residue 必须引用 fact gate |
| `LRCSG-REL-005` | continuity report 必须覆盖 30/90 天窗口 |

## bundle skeletons

三条 component bundle 最后生成。

| task_id | schema | required arrays |
|---|---|---|
| `LRGEN-070` | `pain_regret_repair_bundle.schema.json` | pain signals、pain load states、counterfactual frames、regret pressures、responsibility events、repair commitments、recovery paths |
| `LRGEN-071` | `dream_reality_bundle.schema.json` | offline needs、dream windows、replay selections、dream reports、wake integrations、fact gates、action seals |
| `LRGEN-072` | `relationship_timeline_bundle.schema.json` | first encounters、relation scope births、common ground、responsiveness、trust trajectories、commitments、continuity reports、stage gates |
| `LRGEN-073` | `life_reality_cross_chain_link.schema.json` | source object ref、target object ref、link kind、validator refs、blocked surfaces |
| `LRGEN-074` | `life_reality_bundle.schema.json` | three component bundles、cross-chain links、life target closure |
| `LRGEN-075` | `life_reality_schema_bundle.manifest.json` | schema roots、fixture roots、report roots、loader order |
| `LRGEN-076` | `life_reality_loader_config.schema.json` | load order、strictness、schema roots、report roots |
| `LRGEN-077` | `life_reality_stage_gate_contract.schema.json` | open、hold、repair、quarantine、rollback conditions |

bundle rules：

| rule | 说明 |
|---|---|
| `LRCSG-BUNDLE-001` | bundle schema 只引用已生成 object schema |
| `LRCSG-BUNDLE-002` | `life_reality_bundle` 覆盖九项目标 |
| `LRCSG-BUNDLE-003` | cross-chain link 不直接写 active object，只连接 refs |
| `LRCSG-BUNDLE-004` | loader config 与 generation manifest 顺序一致 |
| `LRCSG-BUNDLE-005` | stage gate contract 引用 shared defs result 和 blocked surfaces |

## dependency graph

生成：

```text
life_reality_runner/generation/component_schema_dependency_graph.json
```

最小结构：

```json
{
  "graph_kind": "ComponentSchemaDependencyGraph",
  "graph_version": "0.1.0",
  "graph_id": "component_schema_dependency_graph_001",
  "source_manifest_ref": "component_schema_seed_generation.manifest.json",
  "nodes": [],
  "edges": [],
  "cycle_findings": [],
  "critical_path": []
}
```

node fields：

| 字段 | 说明 |
|---|---|
| `node_id` | schema node id |
| `schema_path` | schema file path |
| `object_kind` | object kind or bundle kind |
| `phase` | generation phase |
| `task_id` | LRGEN id |
| `life_reality_targets` | affected targets |
| `source_docs` | source docs |

edge kinds：

| edge kind | 说明 |
|---|---|
| `uses_shared_defs` | 引用 shared defs |
| `extends_base` | 引用 component base |
| `requires_scope` | 依赖 relation scope |
| `requires_source_object` | 依赖上游 component object |
| `requires_fact_gate` | 依赖 dream fact gate |
| `bundles_object` | object 进入 bundle |
| `validates_after` | validator 顺序依赖 |

graph rules：

| rule | 说明 |
|---|---|
| `LRCSG-GRAPH-001` | graph 必须无 cycle |
| `LRCSG-GRAPH-002` | relation scope roots 早于 relation scoped objects |
| `LRCSG-GRAPH-003` | dream fact gate 早于 dream shared residue |
| `LRCSG-GRAPH-004` | bundle nodes 位于 object nodes 后 |
| `LRCSG-GRAPH-005` | graph 可导出 DOT |

## dry-run report

生成：

```text
life_reality_runner/generation/component_schema_sequence_dry_run_report.json
```

最小结构：

```json
{
  "report_kind": "ComponentSchemaSequenceDryRunReport",
  "report_version": "0.1.0",
  "run_id": "component_schema_sequence_run_001",
  "input_manifest_ref": "component_schema_seed_generation.manifest.json",
  "generated_schema_count": 0,
  "validation_units": [],
  "findings": [],
  "stage_effect": {},
  "next_artifact_refs": []
}
```

dry-run rules：

| rule | 说明 |
|---|---|
| `LRCSG-DRY-001` | 每个 generated schema 有 validation unit |
| `LRCSG-DRY-002` | missing `$ref` 进入 finding |
| `LRCSG-DRY-003` | dependency cycle 进入 critical finding |
| `LRCSG-DRY-004` | bundle 引用未生成 schema 进入 needs_evidence |
| `LRCSG-DRY-005` | dry-run report 进入 `114` cross-file rollup |

## cross-bundle ref report

生成：

```text
life_reality_runner/generation/component_schema_cross_bundle_ref_report.json
```

cross-bundle refs：

| source | target | reason |
|---|---|---|
| `PainDreamResidue` | `PainLoadState` | 痛苦梦境残留 |
| `RelationshipDreamSimulation` | `RelationScopeBirth` | 关系梦境模拟保留 scope |
| `DreamSharedResidue` | `DreamFactGateDecision` | 梦境分享事实门 |
| `RelationshipConsequenceTrace` | `RepairCommitment` | 修复承诺进入关系后果 |
| `SupportEvent` | `PainLoadState` | 关系支持缓冲痛苦 |
| `CommitmentHistory` | `RepairCommitment` | 修复承诺进入关系承诺历史 |

cross-bundle rules：

| rule | 说明 |
|---|---|
| `LRCSG-XREF-001` | cross-bundle refs 使用 artifact ref / object ref |
| `LRCSG-XREF-002` | dream-to-relationship refs 必须经过 fact gate |
| `LRCSG-XREF-003` | pain-to-relationship refs 必须保留 relation scope |
| `LRCSG-XREF-004` | repair-to-relationship refs 必须有 future probe |
| `LRCSG-XREF-005` | unresolved cross-bundle ref 进入 repair queue |

## validator order report

生成：

```text
life_reality_runner/generation/component_schema_validator_order_report.json
```

validator order：

| order | validator | input reports |
|---:|---|---|
| 1 | `SchemaRefValidator` | schema validation units |
| 2 | `RelationshipBirthValidator` | first encounter、relation scope |
| 3 | `PainRegretRepairValidator` | pain/regret/repair objects |
| 4 | `DreamRealityValidator` | dream/offline/fact gate objects |
| 5 | `RelationshipTimelineValidator` | relationship timeline objects |
| 6 | `CrossChainValidator` | cross-bundle refs |
| 7 | `LifeRealityBundleValidator` | three bundle schemas |
| 8 | `DashboardReadinessValidator` | all reports |

validator order rules：

| rule | 说明 |
|---|---|
| `LRCSG-VAL-001` | schema ref validator 先于所有 domain validator |
| `LRCSG-VAL-002` | relationship birth validator 先于 relationship scoped checks |
| `LRCSG-VAL-003` | dream validator 先于 dream shared residue activation |
| `LRCSG-VAL-004` | cross-chain validator 在三条 domain validator 后 |
| `LRCSG-VAL-005` | dashboard readiness 最后运行 |

## generation order

生成顺序：

```text
load_shared_defs
  -> write_component_seed_generation_manifest
  -> write_shared_base_skeletons
  -> write_relationship_birth_root_skeletons
  -> write_pain_root_skeletons
  -> write_responsibility_regret_repair_skeletons
  -> write_dream_offline_root_skeletons
  -> write_dream_experience_fact_gate_skeletons
  -> write_relationship_growth_skeletons
  -> write_bundle_skeletons
  -> write_dependency_graph
  -> write_cross_bundle_ref_report
  -> write_validator_order_report
  -> run_schema_dry_run
  -> emit_component_schema_gap_feedback
```

order rules：

| rule | 说明 |
|---|---|
| `LRCSG-ORDER-001` | shared base 先于所有 object schema |
| `LRCSG-ORDER-002` | relationship birth roots 先于 social pain、dream share、commitment |
| `LRCSG-ORDER-003` | responsibility/regret/repair 先于 relationship consequence rollup |
| `LRCSG-ORDER-004` | dream fact gate 先于 dream-to-relationship refs |
| `LRCSG-ORDER-005` | bundle skeletons 最后生成 |

## failure mapping

| failure | finding | repair kind | stage effect |
|---|---|---|---|
| shared defs missing | `component_schema.shared_defs_missing` | `schema_gap` | `needs_evidence` |
| base skeleton missing | `component_schema.base_missing` | `schema_gap` | `needs_evidence` |
| object schema missing `$id` | `component_schema.id_missing` | `schema_gap` | `repair` |
| missing shared defs ref | `component_schema.shared_ref_missing` | `schema_gap` | `repair` |
| relation scope ordering violation | `component_schema.relation_scope_order` | `schema_gap` | `repair` |
| dream fact gate ordering violation | `component_schema.fact_gate_order` | `schema_gap` | `repair` |
| dependency cycle | `component_schema.dependency_cycle` | `schema_gap` | `quarantine` |
| bundle refs unknown schema | `component_schema.bundle_unknown_ref` | `schema_gap` | `needs_evidence` |

## LRGEN 更新

`116` 固定 component schema seed generation 的新增任务：

| task_id | 输出 | 说明 |
|---|---|---|
| `LRGEN-196` | `component_schema_seed_generation.manifest.json` | seed generation manifest |
| `LRGEN-197` | `schemas/life_reality/*.schema.json` shared base skeletons | base skeleton batch |
| `LRGEN-198` | `schemas/pain_regret_repair/*.schema.json` skeleton batch | pain/regret/repair batch |
| `LRGEN-199` | `schemas/dream_reality/*.schema.json` skeleton batch | dream reality batch |
| `LRGEN-200` | `schemas/relationship_timeline/*.schema.json` skeleton batch | relationship timeline batch |
| `LRGEN-201` | bundle schema skeleton batch | three bundles + life bundle |
| `LRGEN-202` | `component_schema_dependency_graph.json` | dependency graph |
| `LRGEN-203` | `component_schema_sequence_dry_run_report.json` | dry-run report |
| `LRGEN-204` | `component_schema_cross_bundle_ref_report.json` | cross-bundle ref report |
| `LRGEN-205` | `component_schema_validator_order_report.json` | validator order report |
| `LRGEN-206` | `component_schema_gap_feedback.json` | gap feedback |

## smoke cases

| smoke_id | 输入 | 预期 |
|---|---|---|
| `component_schema.base_skeletons.pass_001` | shared base skeletons | pass |
| `component_schema.pain_batch_refs.pass_001` | pain skeleton batch | pass |
| `component_schema.dream_fact_gate_order.pass_001` | dream fact gate before dream share | pass |
| `component_schema.relationship_birth_order.pass_001` | relation scope before relation object | pass |
| `component_schema.bundle_refs_closed.pass_001` | bundle refs generated schemas | pass |
| `component_schema.missing_shared_defs.fail_001` | shared defs missing | needs_evidence |
| `component_schema.cycle_critical_001` | dependency cycle | quarantine |
| `component_schema.dream_share_without_fact_gate.fail_001` | dream shared residue ref missing fact gate | repair |
| `component_schema.commitment_without_future_probe.fail_001` | commitment history lacks future probe | repair |
| `component_schema.full_dry_run.pass_001` | all skeletons + reports | pass |

## 与下一层连接

`117_life_reality_dashboard_report_rollup_seed_generation.md` 应读取本层的 `component_schema_sequence_dry_run_report.json`、`component_schema_cross_bundle_ref_report.json`、`component_schema_validator_order_report.json` 和 `component_schema_gap_feedback.json`，把它们合并到 `114` 的 specialized reports、provenance graph、finding、repair bridge 和 gap feedback bridge 中。

`118_life_reality_generation_runner_cli_contract.md` 应把 `115` 和 `116` 的生成顺序压成可执行 CLI：

```text
life-reality-runner generate-fixtures
life-reality-runner generate-schemas
life-reality-runner check-dashboard
```
