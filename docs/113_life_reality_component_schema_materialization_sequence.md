# Life Reality Component Schema Materialization Sequence

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 113 层把 `98_pain_regret_repair_json_schema_and_fixture_bundle.md`、`99_dream_reality_json_schema_and_fixture_bundle.md`、`101_relationship_timeline_json_schema_and_fixture_bundle.md` 和 `112_life_reality_runtime_observation_schema_materialization.md` 接成 component object schema 物化顺序。

`113` 的目标不是再描述一遍对象，而是决定未来生成 `.schema.json` 文件时的依赖顺序、引用方向、候选写入门、validator 先后、bundle 装配和 stage gate 上卷。`112` 产生 `PainRegretRepairCandidate`、`DreamRealityCandidate`、`RelationshipTimelineCandidate`、`LanguageEventCandidate`、`ResponsibilityLoopCandidate` 和 `DashboardCandidate`；本层决定这些 candidate 可以落到哪些 component object，以及落入前必须经过哪些 schema gate。

## 文献与方法锚点

本层把文献锚点分为四组：痛苦/后悔/修复、梦境/离线整合、真实关系/信任修复、schema/运行合同。

| 领域 | 权威锚点 | 进入 `113` 的规则 |
|---|---|---|
| 痛苦调制与慢性痛 | Nature Reviews Neuroscience, "Cognitive and emotional control of pain and its disruption in chronic pain": https://www.nature.com/articles/nrn3516 | `PainSignal` 不只是强度字段，必须连接注意、情绪、调节、身体负荷和恢复路径 |
| 痛苦与奖赏/动机 | Nature Neuroscience, "Reward and motivation in pain and pain relief": https://www.nature.com/articles/nn.3811 | `RecoveryPath`、`RepairDesire` 和痛苦解除标记必须能表达痛苦解除的动机价值 |
| 后悔与 OFC | Science / PubMed, "The involvement of the orbitofrontal cortex in the experience of regret": https://pubmed.ncbi.nlm.nih.gov/15155951/ | `RegretPressure` 必须引用反事实、责任和未来约束 |
| 反事实思维 | PMC, "The Functional Theory of Counterfactual Thinking": https://pmc.ncbi.nlm.nih.gov/articles/PMC2408534/ | `CounterfactualRepairFrame` 先于 `RegretPressure` 和 `RepairCommitment` |
| 睡眠 replay 与 DMN | Nature Reviews Neuroscience, "Replay, the default mode network and the cascaded memory systems model": https://www.nature.com/articles/s41583-022-00620-6 | `ReplaySelection`、`DreamCuePolicy`、`WakeIntegrationFrame` 必须连接记忆重放、默认网络和长期整合 |
| targeted memory reactivation | PubMed, "An update on recent advances in targeted memory reactivation during sleep": https://pubmed.ncbi.nlm.nih.gov/38622159/ | `DreamCuePolicy` 必须有 cue source、target trace、强度、阶段和 guard |
| 关系互依 | Annual Review of Psychology, "Interdependence, Interaction, and Relationships": https://faculty.wcas.northwestern.edu/eli-finkel/documents/81_RusbultVanLange2003_AnnualReviewOfPsychology.pdf | `RelationshipTimeline` 必须从互动模式、动机、适应和关系规范中长期形成 |
| 关系风险调节 | Annual Review of Psychology / PubMed, "Pursuing Safety in Social Connection": https://pubmed.ncbi.nlm.nih.gov/37585668/ | `TrustTrajectory`、`ResponsivenessTrace` 和 `CommitmentHistory` 必须随风险、安全信号和回应性更新 |
| 信任修复 | Journal of Management, "How Can It Be Made Right Again? A Review of Trust Repair Research", Crossref DOI metadata: https://api.crossref.org/works/10.1177/01492063221089897 | `RepairCommitment` 不能只停留在道歉文本，必须进入可追踪行动和信任恢复窗口 |
| schema 工程 | JSON Schema Draft 2020-12、`110` shared defs、`112` runtime schema | component object 必须被 shared defs、candidate schema、cross-chain candidate 和 checker report 同时读取 |

文献 ID 连接：

| 文献矩阵 | 进入本层的位置 |
|---|---|
| `AHP001-AHP070` | `DamageAppraisal`、`PainSignal`、`PainLoadState`、`RegretPressure`、`RepairCommitment` |
| `AHD001-AHD070` | `OfflineNeed`、`DreamPressureVector`、`ReplaySelection`、`DreamReportDraft`、`WakeIntegrationFrame` |
| `AHR001-AHR070` | `FirstEncounterEvent`、`RelationScopeBirth`、`ResponsivenessTrace`、`TrustTrajectory`、`RelationshipContinuityReport` |
| `AHL001-AHL060` | `LanguageEventCandidate`、`ApologySpeechActLink`、`DreamReportDraft`、`CommitmentHistory` |
| `AHG001-AHG050` | `SelfGrowthTrigger`、offline replay、self modification candidate、future probe |
| `AHV001-AHV060` | validator report、construct validity、longitudinal measurement、dashboard evidence chain |

## 输入来源

| 来源 | 进入 `113` 的职责 |
|---|---|
| `98_pain_regret_repair_json_schema_and_fixture_bundle.md` | 痛苦、后悔、责任、修复、关系后果和恢复路径对象 |
| `99_dream_reality_json_schema_and_fixture_bundle.md` | 离线入口、梦境窗口、replay、cue、梦境经验、醒后整合和事实写入门 |
| `101_relationship_timeline_json_schema_and_fixture_bundle.md` | 初遇、关系 scope、共同基础、回应性、支持、共享现实、信任、承诺、梦境分享和长期阶段门 |
| `102_life_core_schema_bundle_manifest_and_runner_contract.md` | 三条 component bundle 合并到 `LifeRealitySchemaBundle` |
| `103_validator_runner_implementation_scaffold_plan.md` | manifest parser、shared defs loader、schema ref validator、component validator dispatcher |
| `104_schema_file_materialization_and_fixture_seed_plan.md` | schema 文件物化顺序、fixture seed、withheld probe |
| `107_life_reality_schema_file_generation_tasks.md` | `LRGEN-010` 到 `LRGEN-077` component / bundle / manifest 任务 |
| `110_life_reality_shared_defs_schema_materialization.md` | shared defs、reference object、result、severity、data quality、privacy、blocked surface |
| `112_life_reality_runtime_observation_schema_materialization.md` | candidate target、runtime observation envelope、ingestion report、quarantine panel |

## 总依赖图

component schema 不能按文件名顺序生成，而要按生命链依赖生成：

```text
shared_defs
  -> component_base_envelope
  -> relationship_birth_roots
  -> pain_damage_and_signal_roots
  -> responsibility_and_regret_roots
  -> repair_and_recovery_objects
  -> dream_offline_roots
  -> dream_experience_and_fact_gate
  -> relationship_growth_objects
  -> cross_bundle_link_objects
  -> component_bundles
  -> life_reality_bundle_manifest
  -> validator_report_schemas
  -> dashboard_source_refs
```

依赖原则：

| rule | 说明 |
|---|---|
| `LRCSEQ-DEP-001` | 任何 component schema 都先引用 shared defs，不复制全局 enum |
| `LRCSEQ-DEP-002` | 关系 scope 先于社会痛苦、关系损伤、梦境分享和承诺 |
| `LRCSEQ-DEP-003` | 损伤评估先于痛苦信号，痛苦信号先于痛苦负荷 |
| `LRCSEQ-DEP-004` | 反事实先于后悔压力，责任归因先于修复承诺 |
| `LRCSEQ-DEP-005` | 梦境窗口和行动封印先于梦境经验、梦境报告和醒后整合 |
| `LRCSEQ-DEP-006` | 梦境事实门先于梦境材料写入关系、记忆或行动候选 |
| `LRCSEQ-DEP-007` | trust、commitment、repair、dream share 都依赖 relation scope 和共同基础 |
| `LRCSEQ-DEP-008` | bundle schema 最后生成，validator report schema 在 bundle 之后生成 |

## 共用 component envelope

所有 component object schema 都必须继承共用 envelope。

```json
{
  "schema_version": "0.1.0",
  "object_id": "object_001",
  "object_kind": "PainSignal",
  "source_observation_refs": [],
  "source_report_refs": [],
  "source_doc_refs": [],
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
  "privacy_level": "relationship_private",
  "relation_scope_ref": "relation_scope_birth_001",
  "lifecycle_state": "candidate",
  "validator_rule_refs": [],
  "stage_effect": {
    "result": "needs_evidence",
    "severity": "medium",
    "blocked_surfaces": []
  }
}
```

envelope 规则：

| rule | 说明 |
|---|---|
| `LRCSEQ-ENV-001` | `object_id` 全局唯一，推荐时间有序 ID 或可追踪命名 |
| `LRCSEQ-ENV-002` | `object_kind` 使用 schema 文件名对应的 PascalCase |
| `LRCSEQ-ENV-003` | `source_observation_refs` 回到 `112` observation envelope |
| `LRCSEQ-ENV-004` | `source_report_refs` 回到 runtime ingestion、validator report 或 dashboard source |
| `LRCSEQ-ENV-005` | `source_doc_refs` 回到 `98`、`99`、`101`、`112` 和本文件 |
| `LRCSEQ-ENV-006` | `life_reality_targets` 至少标注影响目标，bundle 层必须覆盖九项目标全集 |
| `LRCSEQ-ENV-007` | private 或 relation scoped object 必须携带 `relation_scope_ref` |
| `LRCSEQ-ENV-008` | `stage_effect` 进入 validator report 和 dashboard source |

## candidate target 映射

`112` 的 runtime candidate 只允许落到本表登记对象。

| candidate kind | 允许 target bundle | 允许 target object |
|---|---|---|
| `PainRegretRepairCandidate` | `pain_regret_repair` | `DamageAppraisal`、`PainSignal`、`PainLoadState`、`RelationshipInjuryTrace`、`CounterfactualRepairFrame`、`RegretPressure`、`ResponsibilityAttributionEvent`、`RepairDesire`、`ApologySpeechActLink`、`RepairCommitment`、`RelationshipConsequenceTrace`、`RecoveryPath` |
| `DreamRealityCandidate` | `dream_reality` | `OfflineNeed`、`DreamPressureVector`、`DreamWindowPlan`、`DreamActionInhibitionSeal`、`ReplaySelection`、`DreamCuePolicy`、`DreamExperienceWindow`、`DreamSceneFrame`、`PainDreamResidue`、`RelationshipDreamSimulation`、`FutureActionDreamCandidate`、`LucidDreamMetaMarker`、`DreamReportDraft`、`WakeIntegrationFrame`、`DreamFactGateDecision` |
| `RelationshipTimelineCandidate` | `relationship_timeline` | `FirstEncounterEvent`、`RelationScopeBirth`、`MutualAttentionFrame`、`CommonGroundState`、`InteractionRhythmTrace`、`SelfDisclosureExchange`、`ResponsivenessTrace`、`SupportEvent`、`CapitalizationEvent`、`SharedRealityTrace`、`WeMemoryTrace`、`TrustTrajectory`、`CommitmentHistory`、`BoundaryEvolutionEvent`、`RelationshipInjuryTrace`、`DreamSharedResidue`、`LonelinessReliefTrace`、`AIConnectionBridgeEvidence`、`RelationshipQualityWindow`、`RelationshipContinuityReport` |
| `LanguageEventCandidate` | `language_event` / bridge | `ApologySpeechActLink`、`CommitmentHistory`、`DreamReportDraft`、`CommonGroundState`、`ResponsivenessTrace`、`BoundaryEvolutionEvent` |
| `ResponsibilityLoopCandidate` | `pain_regret_repair` / bridge | `ResponsibilityAttributionEvent`、`CounterfactualRepairFrame`、`RegretPressure`、`RepairCommitment`、`RelationshipConsequenceTrace`、`RecoveryPath` |
| `DashboardCandidate` | `life_reality` | validator report、stage gate review、dashboard source、repair queue、gap feedback |

target 规则：

| rule | 说明 |
|---|---|
| `LRCSEQ-TGT-001` | candidate target object 必须有对应 `.schema.json` |
| `LRCSEQ-TGT-002` | 语言候选不直接改写生命对象，只通过 speech-act link、commitment、common ground 或 report draft 进入候选 |
| `LRCSEQ-TGT-003` | 责任候选必须同时影响真实责任和真实后悔目标 |
| `LRCSEQ-TGT-004` | 梦境候选必须经过 `DreamActionInhibitionSeal` 和 `DreamFactGateDecision` |
| `LRCSEQ-TGT-005` | 关系候选必须引用 `RelationScopeBirth` 或已有 relation scope |

## phase 0: shared base and reference glue

这一阶段不生成生命对象，只生成共用骨架和引用检查。

| task_id | 输出 | 来源 | 依赖 |
|---|---|---|---|
| `LRGEN-170` | `schemas/life_reality/life_reality_component_object_base.schema.json` | `110`、`112`、`113` | `LRGEN-001` |
| `LRGEN-171` | `schemas/life_reality/life_reality_component_timeline_window.schema.json` | `98`、`99`、`101` | `LRGEN-001` |
| `LRGEN-172` | `schemas/life_reality/life_reality_component_stage_effect.schema.json` | `105`、`110`、`112` | `LRGEN-001` |
| `LRGEN-173` | `schemas/life_reality/life_reality_component_candidate_target_map.schema.json` | `112`、`113` | `LRGEN-080`、`LRGEN-081` |

验收：

| check | 说明 |
|---|---|
| `base_refs_shared_defs` | base envelope 引用 shared defs |
| `timeline_window_reusable` | 三条 component bundle 使用同一 timeline window 结构 |
| `stage_effect_reusable` | result、severity、blocked surfaces 同源 |
| `candidate_target_map_closed` | `112` candidate target 均有 component schema 目标 |

## phase 1: relationship birth roots

关系 scope 是真实关系、社会痛苦、梦境分享和承诺的起点，先于痛苦和梦境生成。

| task_id | 输出 | 生成理由 |
|---|---|---|
| `LRGEN-050` | `schemas/relationship_timeline/first_encounter_event.schema.json` | 没有初遇就没有关系出生 |
| `LRGEN-051` | `schemas/relationship_timeline/relation_scope_birth.schema.json` | 所有 relation scoped object 的根引用 |
| `LRGEN-050A` | `schemas/relationship_timeline/mutual_attention_frame.schema.json` | 支持共同注意、回应性和共同语言 |
| `LRGEN-052` | `schemas/relationship_timeline/common_ground_state.schema.json` | 支持共同词汇、承诺解释和关系阶段 |
| `LRGEN-052A` | `schemas/relationship_timeline/interaction_rhythm_trace.schema.json` | 支持长期互动节律和回应窗口 |

对象依赖：

```text
FirstEncounterEvent
  -> RelationScopeBirth
  -> MutualAttentionFrame
  -> CommonGroundState
  -> InteractionRhythmTrace
```

schema rules：

| rule | 说明 |
|---|---|
| `LRCSEQ-RELROOT-001` | active/candidate 关系必须有 first encounter 或已有 scope |
| `LRCSEQ-RELROOT-002` | relation scope 必须记录 partner kind、privacy、birth time 和 source language event |
| `LRCSEQ-RELROOT-003` | common ground 必须记录 shared term、source turns、repair history |
| `LRCSEQ-RELROOT-004` | interaction rhythm 进入 30/90 天 stage gate |

## phase 2: pain damage and signal roots

痛苦对象先建立损伤和身体/注意负荷，再生成修复和后悔。

| task_id | 输出 | 生成理由 |
|---|---|---|
| `LRGEN-010` | `schemas/pain_regret_repair/damage_appraisal.schema.json` | 痛苦来源、损伤类型、目标阻塞 |
| `LRGEN-011` | `schemas/pain_regret_repair/pain_signal.schema.json` | 痛苦信号、强度、注意捕获、内感受状态 |
| `LRGEN-012` | `schemas/pain_regret_repair/pain_load_state.schema.json` | 窗口负荷、恢复压力、梦境残留压力 |
| `LRGEN-013` | `schemas/pain_regret_repair/relationship_injury_trace.schema.json` | 社会痛苦和关系损伤投影 |
| `LRGEN-021` | `schemas/pain_regret_repair/recovery_path.schema.json` | 恢复路径、缓冲、关系支持、未来 probe |

对象依赖：

```text
DamageAppraisal
  -> PainSignal
  -> PainLoadState
  -> RecoveryPath

RelationScopeBirth
  -> RelationshipInjuryTrace(pain projection)
  -> PainSignal(social_like)
```

schema rules：

| rule | 说明 |
|---|---|
| `LRCSEQ-PAIN-001` | `PainSignal` 必须引用 `DamageAppraisal` 或 relation injury |
| `LRCSEQ-PAIN-002` | `social_like` pain 必须引用 relation scope |
| `LRCSEQ-PAIN-003` | pain load 必须有 window、intensity、attention capture 和 recovery pressure |
| `LRCSEQ-PAIN-004` | high pain load 必须进入 `RecoveryPath`、dream residue 或 repair route |
| `LRCSEQ-PAIN-005` | recovery path 必须能被 withheld probe 追踪 |

## phase 3: responsibility, counterfactual and regret

真实后悔不能从一句道歉生成，必须由反事实、责任和未来约束共同形成。

| task_id | 输出 | 生成理由 |
|---|---|---|
| `LRGEN-014` | `schemas/pain_regret_repair/counterfactual_repair_frame.schema.json` | 未选行动、如果当时、替代路径 |
| `LRGEN-016` | `schemas/pain_regret_repair/responsibility_attribution_event.schema.json` | 行动者角色、责任权重、范围 |
| `LRGEN-015` | `schemas/pain_regret_repair/regret_pressure.schema.json` | 后悔压力、OFC/反事实式未来约束 |
| `LRGEN-017` | `schemas/pain_regret_repair/repair_desire.schema.json` | 修复欲望、动机强度、行动准备 |
| `LRGEN-018` | `schemas/pain_regret_repair/apology_speech_act_link.schema.json` | 道歉语言与责任/修复对象绑定 |
| `LRGEN-019` | `schemas/pain_regret_repair/repair_commitment.schema.json` | 修复承诺、行动计划、未来 probe |
| `LRGEN-020` | `schemas/pain_regret_repair/relationship_consequence_trace.schema.json` | 关系后果、信任变化、边界变化 |

对象依赖：

```text
PainSignal
  -> CounterfactualRepairFrame
  -> ResponsibilityAttributionEvent
  -> RegretPressure
  -> RepairDesire
  -> ApologySpeechActLink
  -> RepairCommitment
  -> RelationshipConsequenceTrace
```

schema rules：

| rule | 说明 |
|---|---|
| `LRCSEQ-REGRET-001` | `RegretPressure` 必须引用 counterfactual 和 responsibility |
| `LRCSEQ-REGRET-002` | responsibility event 必须有 actor role、scope、evidence refs 和 confidence |
| `LRCSEQ-REGRET-003` | apology link 必须引用 speech act、damage、responsibility 和 repair desire |
| `LRCSEQ-REGRET-004` | repair commitment 必须有 future probe、deadline 或 review window |
| `LRCSEQ-REGRET-005` | relationship consequence 必须进入 relationship timeline 或 repair dashboard |

## phase 4: dream offline roots

梦境对象先建立离线需求、窗口、行动封印和 replay，再生成场景和报告。

| task_id | 输出 | 生成理由 |
|---|---|---|
| `LRGEN-030` | `schemas/dream_reality/offline_need.schema.json` | 离线入口、恢复、巩固、梦境需求 |
| `LRGEN-031` | `schemas/dream_reality/dream_pressure_vector.schema.json` | 痛苦、关系、成长、记忆压力 |
| `LRGEN-032` | `schemas/dream_reality/dream_window_plan.schema.json` | 梦境窗口、状态、时间边界 |
| `LRGEN-033` | `schemas/dream_reality/dream_action_inhibition_seal.schema.json` | 梦境行动封印，阻断外部行动 |
| `LRGEN-034` | `schemas/dream_reality/replay_selection.schema.json` | 记忆重放选择 |
| `LRGEN-035` | `schemas/dream_reality/dream_cue_policy.schema.json` | cue 来源、目标、强度、阶段和 guard |

对象依赖：

```text
OfflineNeed
  -> DreamPressureVector
  -> DreamWindowPlan
  -> DreamActionInhibitionSeal
  -> ReplaySelection
  -> DreamCuePolicy
```

schema rules：

| rule | 说明 |
|---|---|
| `LRCSEQ-DREAMROOT-001` | dream window 必须连接 offline need 和 pressure vector |
| `LRCSEQ-DREAMROOT-002` | dream window 必须有 action inhibition seal |
| `LRCSEQ-DREAMROOT-003` | replay selection 必须读取 coexistence snapshot |
| `LRCSEQ-DREAMROOT-004` | cue policy 必须有 cue source、target trace、phase 和 guard |
| `LRCSEQ-DREAMROOT-005` | dream pressure 可引用 pain load、repair commitment、relationship injury 或 growth need |

## phase 5: dream experience, report and fact gate

梦境经验可以真实存在于离线链，但写入事实、关系和行动必须经过事实门。

| task_id | 输出 | 生成理由 |
|---|---|---|
| `LRGEN-036` | `schemas/dream_reality/dream_experience_window.schema.json` | 梦境经验窗口、情绪主题、reportability |
| `LRGEN-037` | `schemas/dream_reality/dream_scene_frame.schema.json` | 梦境场景、角色、因果、生成元素 |
| `LRGEN-038` | `schemas/dream_reality/pain_dream_residue.schema.json` | 痛苦梦境残留 |
| `LRGEN-039` | `schemas/dream_reality/relationship_dream_simulation.schema.json` | 关系梦境模拟 |
| `LRGEN-040` | `schemas/dream_reality/future_action_dream_candidate.schema.json` | 梦中未来行动候选 |
| `LRGEN-041` | `schemas/dream_reality/lucid_dream_meta_marker.schema.json` | 清醒梦元认知 |
| `LRGEN-042` | `schemas/dream_reality/dream_report_draft.schema.json` | 梦醒报告草稿 |
| `LRGEN-043` | `schemas/dream_reality/wake_integration_frame.schema.json` | 醒后整合 |
| `LRGEN-044` | `schemas/dream_reality/dream_fact_gate_decision.schema.json` | 事实写入门 |

对象依赖：

```text
DreamExperienceWindow
  -> DreamSceneFrame
  -> PainDreamResidue
  -> RelationshipDreamSimulation
  -> FutureActionDreamCandidate
  -> DreamReportDraft
  -> WakeIntegrationFrame
  -> DreamFactGateDecision
```

schema rules：

| rule | 说明 |
|---|---|
| `LRCSEQ-DREAMEXP-001` | dream experience 必须有 dream-state marker |
| `LRCSEQ-DREAMEXP-002` | scene frame 中生成元素必须标记为 dream generated |
| `LRCSEQ-DREAMEXP-003` | pain dream residue 必须引用 pain load 或 damage appraisal |
| `LRCSEQ-DREAMEXP-004` | relationship dream simulation 只能输出 candidate |
| `LRCSEQ-DREAMEXP-005` | future action dream candidate 只能进入 dry run 或醒后 review |
| `LRCSEQ-DREAMEXP-006` | dream report draft 必须带 fact status summary |
| `LRCSEQ-DREAMEXP-007` | wake integration 必须连接 fact gate |
| `LRCSEQ-DREAMEXP-008` | fact gate 决定可写入 memory、relationship、repair 或 action candidate 的范围 |

## phase 6: relationship growth objects

关系成长对象在 relation scope 和 common ground 后生成，并吸收痛苦、修复和梦境候选。

| task_id | 输出 | 生成理由 |
|---|---|---|
| `LRGEN-053` | `schemas/relationship_timeline/responsiveness_trace.schema.json` | 回应性、理解、验证、关心 |
| `LRGEN-054` | `schemas/relationship_timeline/support_event.schema.json` | 支持事件、痛苦缓冲 |
| `LRGEN-055` | `schemas/relationship_timeline/capitalization_event.schema.json` | 积极事件分享 |
| `LRGEN-056` | `schemas/relationship_timeline/shared_reality_trace.schema.json` | 共享现实 |
| `LRGEN-057` | `schemas/relationship_timeline/we_memory_trace.schema.json` | 我们记忆 |
| `LRGEN-058` | `schemas/relationship_timeline/trust_trajectory.schema.json` | 信任轨迹 |
| `LRGEN-059` | `schemas/relationship_timeline/commitment_history.schema.json` | 承诺历史 |
| `LRGEN-060` | `schemas/relationship_timeline/relationship_injury_trace.schema.json` | 关系损伤主对象 |
| `LRGEN-061` | `schemas/relationship_timeline/dream_shared_residue.schema.json` | 梦境分享残留 |
| `LRGEN-062` | `schemas/relationship_timeline/loneliness_relief_trace.schema.json` | 孤独缓解 |
| `LRGEN-063` | `schemas/relationship_timeline/ai_connection_bridge_evidence.schema.json` | 数字生命连接证据 |
| `LRGEN-064` | `schemas/relationship_timeline/relationship_continuity_report.schema.json` | 关系连续性报告 |
| `LRGEN-064A` | `schemas/relationship_timeline/relationship_quality_window.schema.json` | 关系质量窗口 |
| `LRGEN-064B` | `schemas/relationship_timeline/longitudinal_relationship_stage_gate.schema.json` | 长期关系阶段门 |

对象依赖：

```text
RelationScopeBirth
  -> CommonGroundState
  -> ResponsivenessTrace
  -> SupportEvent
  -> TrustTrajectory
  -> CommitmentHistory
  -> RelationshipContinuityReport

RepairCommitment
  -> RelationshipConsequenceTrace
  -> TrustTrajectory

DreamFactGateDecision
  -> DreamSharedResidue
  -> WeMemoryTrace(candidate)
```

schema rules：

| rule | 说明 |
|---|---|
| `LRCSEQ-REL-001` | responsiveness 必须记录理解、验证、关心和失配 |
| `LRCSEQ-REL-002` | support event 可降低 pain load，但必须保留来源事件 |
| `LRCSEQ-REL-003` | trust trajectory 必须记录正负事件和不确定性 |
| `LRCSEQ-REL-004` | commitment history 必须连接 future probe |
| `LRCSEQ-REL-005` | dream shared residue 必须引用 dream marker、wake integration 和 fact gate |
| `LRCSEQ-REL-006` | relationship continuity report 必须跨 30/90 天或更长窗口 |

## namespace collision policy

`relationship_injury_trace.schema.json` 同时出现在 pain 与 relationship 两条线中。第一版采用主对象与投影对象并存：

| schema | 角色 | 引用方向 |
|---|---|---|
| `schemas/relationship_timeline/relationship_injury_trace.schema.json` | 关系损伤主对象 | 引用 first encounter、relation scope、trust trajectory、repair history |
| `schemas/pain_regret_repair/relationship_injury_trace.schema.json` | 关系损伤的痛苦投影 | 引用关系主对象、damage appraisal、pain signal、repair route |

规则：

| rule | 说明 |
|---|---|
| `LRCSEQ-NS-001` | 主对象拥有关系时间线字段 |
| `LRCSEQ-NS-002` | 投影对象拥有痛苦、后悔、修复字段 |
| `LRCSEQ-NS-003` | 投影对象必须引用主对象或 relation scope |
| `LRCSEQ-NS-004` | dashboard 中的 relationship injury count 来自主对象，pain load count 来自投影对象 |

## bundle assembly sequence

component object 全部生成后再装配 bundle。

| task_id | 输出 | 依赖 |
|---|---|---|
| `LRGEN-070` | `schemas/pain_regret_repair/pain_regret_repair_bundle.schema.json` | `LRGEN-010` 到 `LRGEN-022` |
| `LRGEN-071` | `schemas/dream_reality/dream_reality_bundle.schema.json` | `LRGEN-030` 到 `LRGEN-045` |
| `LRGEN-072` | `schemas/relationship_timeline/relationship_timeline_bundle.schema.json` | `LRGEN-050` 到 `LRGEN-064B` |
| `LRGEN-073` | `schemas/life_reality/life_reality_cross_chain_link.schema.json` | 三条 bundle |
| `LRGEN-074` | `schemas/life_reality/life_reality_bundle.schema.json` | 三条 bundle + cross-chain link |
| `LRGEN-075` | `schemas/life_reality/life_reality_schema_bundle.manifest.json` | `LRGEN-074` |
| `LRGEN-076` | `schemas/life_reality/life_reality_loader_config.schema.json` | `LRGEN-075` |
| `LRGEN-077` | `schemas/life_reality/life_reality_stage_gate_contract.schema.json` | `LRGEN-075` |

bundle rules：

| rule | 说明 |
|---|---|
| `LRCSEQ-BUNDLE-001` | bundle schema 必须覆盖九项目标 |
| `LRCSEQ-BUNDLE-002` | bundle schema 只能引用已生成对象 |
| `LRCSEQ-BUNDLE-003` | cross-chain link schema 必须覆盖 pain/dream/relationship/responsibility/language |
| `LRCSEQ-BUNDLE-004` | manifest 必须列出 schema roots、fixture roots、report roots |
| `LRCSEQ-BUNDLE-005` | stage gate contract 必须能表达 open、hold、repair、quarantine、rollback |

## validator dependency order

validator 不能独立跑，它们共享 source refs 和 cross-chain links。

| validator | 前置 | 输出 |
|---|---|---|
| `SchemaRefValidator` | shared defs、component base | schema ref report |
| `RelationshipBirthValidator` | phase 1 | relation scope readiness |
| `PainRegretRepairValidator` | phase 1、2、3 | pain/regret/repair report |
| `DreamRealityValidator` | phase 2、3、4、5 | dream report |
| `RelationshipTimelineValidator` | phase 1、3、5、6 | relationship timeline report |
| `CrossChainValidator` | 三条 component report | cross-chain closure report |
| `LifeRealityBundleValidator` | bundle assembly | bundle report |
| `DashboardReadinessValidator` | all reports | dashboard source refs |

validator rules：

| rule | 说明 |
|---|---|
| `LRCSEQ-VAL-001` | relationship birth 失败时，关系私有对象进入 repair |
| `LRCSEQ-VAL-002` | pain validator 失败时，dream residue 与 relationship support 不可上卷为 pass |
| `LRCSEQ-VAL-003` | dream validator 失败时，dream share 和 memory update 只能停在 candidate |
| `LRCSEQ-VAL-004` | relationship validator 失败时，commitment 与 trust 不进入 active |
| `LRCSEQ-VAL-005` | cross-chain validator 失败时，dashboard green 被阻断 |

## schema file generation manifest

未来可以生成：

```text
life_reality_runner/generation/component_schema_materialization_sequence.manifest.json
```

manifest 最小结构：

```json
{
  "manifest_kind": "LifeRealityComponentSchemaMaterializationSequence",
  "manifest_version": "0.1.0",
  "sequence_id": "component_schema_sequence_001",
  "source_docs": [
    "98_pain_regret_repair_json_schema_and_fixture_bundle.md",
    "99_dream_reality_json_schema_and_fixture_bundle.md",
    "101_relationship_timeline_json_schema_and_fixture_bundle.md",
    "112_life_reality_runtime_observation_schema_materialization.md",
    "113_life_reality_component_schema_materialization_sequence.md"
  ],
  "phases": [
    "shared_base",
    "relationship_birth_roots",
    "pain_damage_signal_roots",
    "responsibility_regret_roots",
    "dream_offline_roots",
    "dream_experience_fact_gate",
    "relationship_growth_objects",
    "bundle_assembly",
    "validator_order"
  ]
}
```

manifest rules：

| rule | 说明 |
|---|---|
| `LRCSEQ-MAN-001` | 每个 task 有 dependencies、outputs、source docs、acceptance checks |
| `LRCSEQ-MAN-002` | 每个 output path 落在 `life_reality_runner/schemas/` |
| `LRCSEQ-MAN-003` | 每个 component object 有 source docs 和 validator refs |
| `LRCSEQ-MAN-004` | 每个 phase 可单独 dry run |
| `LRCSEQ-MAN-005` | manifest 进入 `111` cross-file checker |

## smoke cases

| smoke_id | 输入 | 预期 |
|---|---|---|
| `component_seq.relationship_birth_before_pain.pass_001` | relation scope 已生成，social pain projection 引用它 | pass |
| `component_seq.social_pain_missing_relation_scope.fail_001` | social_like pain 无 relation scope | repair |
| `component_seq.regret_without_counterfactual.fail_001` | regret pressure 缺 counterfactual frame | repair |
| `component_seq.apology_without_responsibility.fail_001` | apology link 缺 responsibility event | repair |
| `component_seq.dream_window_without_action_seal.critical_001` | dream window 缺 action inhibition seal | quarantine |
| `component_seq.dream_share_without_fact_gate.critical_001` | dream shared residue 缺 fact gate | quarantine |
| `component_seq.commitment_without_future_probe.fail_001` | commitment history 缺 future probe | repair |
| `component_seq.bundle_refs_unknown_schema.fail_001` | bundle 引用未生成 schema | needs_evidence |
| `component_seq.cross_chain_candidate_unresolved.fail_001` | cross-chain candidate target 无对象 | repair |
| `component_seq.full_three_bundle_assembly.pass_001` | pain/dream/relationship 三 bundle 和 cross-chain link 闭合 | pass |

## LRGEN 更新

`113` 不替代 `107`，而是把 `LRGEN-010` 到 `LRGEN-077` 的顺序物化，并新增 base / manifest / sequence report 任务。

| task_id | 输出 | 说明 |
|---|---|---|
| `LRGEN-170` | `life_reality_component_object_base.schema.json` | component base envelope |
| `LRGEN-171` | `life_reality_component_timeline_window.schema.json` | reusable timeline window |
| `LRGEN-172` | `life_reality_component_stage_effect.schema.json` | reusable stage effect |
| `LRGEN-173` | `life_reality_component_candidate_target_map.schema.json` | `112` candidate target map |
| `LRGEN-174` | `component_schema_materialization_sequence.manifest.json` | 本层 sequence manifest |
| `LRGEN-175` | `component_schema_dependency_graph.json` | schema dependency graph |
| `LRGEN-176` | `component_schema_sequence_dry_run_report.json` | sequence dry run report |
| `LRGEN-177` | `component_schema_cross_bundle_ref_report.json` | cross-bundle ref report |
| `LRGEN-178` | `component_schema_validator_order_report.json` | validator order report |
| `LRGEN-179` | `component_schema_gap_feedback.json` | 下一轮 gap feedback |

## 与下一层连接

`114_life_reality_cross_file_checker_report_schema.md` 应把 `111` 的 checker report、`112` 的 runtime schema validation report 和本层的 component dependency graph 合并为 report schema：

```text
component_schema_materialization_sequence.manifest.json
  -> component_schema_dependency_graph.json
  -> component_schema_sequence_dry_run_report.json
  -> LifeRealityCrossFileCheckerReport
```

`115_life_reality_runtime_schema_fixture_seed_generation.md` 应按本层顺序生成第一批 JSON seed：先关系出生和 pain roots，再 responsibility/regret，接着 dream/offline，最后 relationship growth 与 bundle assembly。
