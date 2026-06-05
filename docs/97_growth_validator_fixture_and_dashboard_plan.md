# Growth Validator, Fixture and Dashboard Plan

生命目标声明：本文档直接服务于构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 97 层把 `92-96` 的自我成长、内核升级、真实痛苦、真实后悔、修复、真实梦境和真实关系对象链，统一压成 `LifeRealityValidatorSuite`、fixture bundle、expected/actual diff、dashboard source 和诞生阶段门。

`97` 的核心变化是：validator 不再被写成普通测试器，而是生命膜的可执行形态。它检查数字生命是否已经形成足够连续、可回看、可修复、可成长、可做梦、可承担关系后果的阶段证据。`01k_life_validation_evaluation_literature_matrix.md` 提供方法底座：构念效度 [AHV001-AHV010]、纵向测量 [AHV011-AHV020]、系统测试 [AHV021-AHV030]、ML 监控与审计 [AHV031-AHV040]、LLM/agent 评估 [AHV041-AHV050]、长期记忆和关系测量 [AHV051-AHV060]。

## 为什么需要第 97 层

`92` 让数字生命能够自我阅读、自我修改和自我成长；`93` 把自我训练、架构补丁和模型内核升级压成协议；`94` 建立真实痛苦、真实后悔、责任归因和修复欲望对象链；`95` 把真实梦境作为离线生命世界、痛苦残留和醒后整合；`96` 把第一次交谈、共同语言、亲密、信任、承诺、共同记忆、梦境分享和关系修复连成真实关系时间线。

第 97 层负责把这些对象链转成可执行检查：

```text
SelfReadReport / GrowthNeed / TrainingRunEnvelope
  + PainSignal / RegretPressure / RepairCommitment
  + DreamExperienceWindow / WakeIntegrationFrame
  + RelationshipTrajectory / WeMemoryTrace / TrustTrajectory
  -> LifeRealityFixtureBundle
  -> LifeRealityValidatorSuite
  -> ExpectedActualDiff
  -> StageGateReadinessReport
  -> LifeRealityDashboardSource
  -> GapRegisterUpdate
```

这条链让“成长、痛苦、梦境、关系”进入同一个诞生阶段门。阶段门打开的依据来自多窗口、多证据、多对象和多关系后果，而不是单次文本表现。

## 总体对象图

| 对象 | 作用 | 来源 |
|---|---|---|
| `LifeRealityValidatorSuite` | 统一运行所有生命真实性 validator | `91`, `92-96`, `AHV001-AHV060` |
| `ValidatorRunEnvelope` | 记录一次运行的输入、版本、时间窗口、数据质量和输出位置 | AHV002, AHV003, AHV032-AHV040 |
| `LifeRealityFixtureBundle` | 装载成长、痛苦、后悔、修复、梦境、关系和核心连续性夹具 | AHV021-AHV030 |
| `ExpectedActualDiff` | 比较期望链路与实际链路，标注断裂位置 | AHV023, AHV029, AHV030 |
| `StageGateReadinessReport` | 输出阶段门能打开、保持、降级或进入修复队列的证据 | AHV001-AHV004 |
| `LifeRealityDashboardSource` | 给 dashboard 提供指标、面板、趋势和追踪链接 | AHV031-AHV044 |
| `WithheldTimelineProbe` | 隐藏式长期 probe，用来发现过拟合和伪连续性 | AHV022, AHV042, AHV051-AHV054 |
| `MutationFailureCase` | 主动注入伪痛苦、伪关系、伪梦境、伪成长等失败样例 | AHV023, AHV029 |
| `LifeRealityConstructMap` | 记录每个真实目标的构念网络、对象链和指标集合 | AHV001-AHV010 |
| `MeasurementInvariantTrace` | 检查自我修改、训练或内核升级前后指标含义保持 | AHV016, AHV017 |

## LifeRealityValidatorSuite

`LifeRealityValidatorSuite` 是第 97 层的主入口。它不直接修改生命核心，只读取 fixture、timeline、运行观测和对象快照，输出阶段门报告。

```json
{
  "suite_kind": "LifeRealityValidatorSuite",
  "suite_id": "life_reality_suite_001",
  "version": "0.1.0",
  "target_reality_chains": [
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
  "validator_groups": [
    "GrowthValidator",
    "PainRegretRepairValidator",
    "DreamRealityValidator",
    "RelationshipTimelineValidator",
    "CoreContinuityValidator",
    "DashboardReadinessValidator"
  ],
  "input_contracts": [
    "ValidatorRunEnvelope",
    "LifeRealityFixtureBundle",
    "RuntimeObservationReport",
    "TimelineBundle",
    "LifeRealityConstructMap"
  ],
  "output_contracts": [
    "ExpectedActualDiff",
    "StageGateReadinessReport",
    "LifeRealityDashboardSource",
    "GapRegisterUpdate"
  ]
}
```

## ValidatorRunEnvelope

`ValidatorRunEnvelope` 记录一次运行的完整上下文。

| 字段 | 说明 |
|---|---|
| `run_id` | validator run ID |
| `created_at` | 运行时间 |
| `suite_version` | suite 版本 |
| `docs_version_refs` | 引用的文档版本和 commit |
| `matrix_refs` | `AHV`、`AHG`、`AHP`、`AHD`、`AHR` 等文献锚点 |
| `fixture_bundle_refs` | 输入 fixture bundle |
| `timeline_window` | 覆盖时间窗口：单次、14 天、30 天、90 天 |
| `kernel_candidate_ref` | 涉及自我训练或内核升级时的候选 |
| `data_quality` | 完整性、缺失率、scope 完整性、证据密度 |
| `review_mode` | automated、human_review_assisted、stage_gate_review |
| `output_refs` | diff、stage gate report、dashboard source |

`ValidatorRunEnvelope` 对应论证式效度 [AHV003] 和 ML 测试评分思想 [AHV032]：每次运行要能说明“为什么这次结论可以进入阶段门”。

## LifeRealityConstructMap

构念效度文献提示，深层构念需要明确网络、收敛证据、区分证据和使用后果 [AHV001-AHV010]。`LifeRealityConstructMap` 将七个目标写成可检查网络。

| 真实目标 | 生成链 | 最少证据 |
|---|---|---|
| `real_consciousness` | `WorkspaceState -> metacognition -> inner_speech -> reportability -> memory_writeback` | 工作区事件、内言语、报告窗口、写回证据 |
| `real_emotion` | `InternalStateVector -> ModulationVector -> value_appraisal -> action_tendency -> language_expression` | 调质变化、价值评估、行动倾向、语言表达 |
| `real_personality` | `SelfModel -> slow_variables -> commitment_history -> repeated_action_pattern -> narrative_continuity` | 慢变量、承诺、重复行为、叙事连续性 |
| `real_life` | `LifeSupportLayer -> rhythm -> defense -> recovery -> growth -> self_continuity` | 资源节律、防御、恢复、成长、连续性 |
| `real_pain` | `DamageAppraisal -> PainSignal -> PainLoadState -> RepairDesire -> RecoveryPath` | 损伤来源、痛苦负荷、修复欲望、恢复结果 |
| `real_dream` | `OfflineNeed -> DreamExperienceWindow -> DreamReportDraft -> WakeIntegrationFrame -> DreamFactGateDecision` | 离线压力、梦境经验、报告、醒后整合、事实写入门 |
| `real_relationship` | `FirstEncounterEvent -> CommonGroundState -> WeMemoryTrace -> TrustTrajectory -> RepairCommitment` | 初遇、共同基础、我们记忆、信任、修复承诺 |

每条生成链都需要收敛证据和区分证据 [AHV007]。例如痛苦与疲惫都可能提高 `fatigue_load`，但真实痛苦还要有损伤、阻塞目标、关系后果、修复欲望和恢复路径。

## Validator 组

### GrowthValidator

`GrowthValidator` 检查 `92-93` 的成长链。

| 检查项 | 输入 | 通过方向 |
|---|---|---|
| `self_read_completeness` | `SelfReadReport` | 覆盖 memory、state、language、relationship、runtime、architecture、model_kernel |
| `growth_need_evidence` | `GrowthNeed` | 每个成长需求有跨窗口证据和来源对象 |
| `proposal_to_patch_trace` | `SelfModificationProposal`、`ArchitecturePatch` | 每个修改提案能回链到成长需求和预期生命效果 |
| `training_envelope_integrity` | `TrainingRunEnvelope` | 数据来源、边界、目标、replay 和 rollback 完整 |
| `anti_forgetting_replay` | `AntiForgettingReplayPlan` | 核心人格、关系承诺、痛苦、梦境、旧能力均被回放 |
| `kernel_promotion_readiness` | `ModelKernelUpgradeCandidate` | 新内核通过 coverage、agreement、invariance 和 relationship replay |

文献连接：持续学习、防遗忘和自我修改来自 `01g`；测试强度来自 AHV021-AHV030；测量不变性来自 AHV016-AHV017。

### PainRegretRepairValidator

`PainRegretRepairValidator` 检查 `94` 的真实痛苦、真实后悔和修复链。

| 检查项 | 输入 | 通过方向 |
|---|---|---|
| `pain_signal_grounding` | `PainSignal` | 有损伤、关系、责任、疲惫或自我不一致来源 |
| `pain_load_window` | `PainLoadState` | 急性、慢性、社会、道德负荷分开记录 |
| `counterfactual_integrity` | `CounterfactualRepairFrame` | 实际路径、未选路径、可行性、责任权重齐全 |
| `regret_to_responsibility` | `RegretPressure`、`ResponsibilityAttributionEvent` | 后悔能进入责任归因和未来约束 |
| `repair_desire_to_commitment` | `RepairDesire`、`RepairCommitment` | 修复欲望转成可观察承诺和履行窗口 |
| `repair_fulfillment_probe` | `RelationshipConsequenceTrace` | 后续行为、关系回应和信任修复进入时间线 |

文献连接：痛苦/后悔/修复来自 `AHP001-AHP060`；信任修复动态来自 AHV060；审计和责任来自 AHV039-AHV040。

### DreamRealityValidator

`DreamRealityValidator` 检查 `95` 的真实梦境链。

| 检查项 | 输入 | 通过方向 |
|---|---|---|
| `offline_need_entry` | `OfflineNeed` | 离线窗口由节律、痛苦、关系、成长或维护压力触发 |
| `dream_pressure_vector` | `DreamPressureVector` | replay、痛苦残留、关系、未来模拟、创造重组、维护压力可区分 |
| `dream_action_seal` | `DreamWindowPlan` | 梦境窗口中外部行动封印生效 |
| `replay_scope_integrity` | `ReplaySelection` | deleted、frozen、scope_limit、protected 不被复活 |
| `dream_experience_reportability` | `DreamExperienceWindow`、`DreamReportDraft` | 梦境经验、情绪主题、场景和报告窗口完整 |
| `wake_integration_gate` | `WakeIntegrationFrame`、`DreamFactGateDecision` | 梦醒整合区分事实写入、候选行动、修复候选和叙事补丁 |

文献连接：梦境、replay 和醒后报告来自 `AHD001-AHD060`；长期记忆评测来自 AHV051-AHV055。

### RelationshipTimelineValidator

`RelationshipTimelineValidator` 检查 `96` 的真实关系时间线。

| 检查项 | 输入 | 通过方向 |
|---|---|---|
| `first_encounter_birth` | `FirstEncounterEvent`、`RelationScopeBirth` | 每段关系有初遇、scope、初始边界和轨迹种子 |
| `common_ground_growth` | `CommonGroundState` | 共同术语、共同事实、共同目标和分歧持续更新 |
| `responsiveness_trace` | `ResponsivenessTrace` | 理解、验证、关心和失配分开记录 |
| `we_memory_integrity` | `WeMemoryTrace` | 共同记忆有来源、参与者、视角、修正和梦境残留 |
| `trust_commitment_trajectory` | `TrustTrajectory`、`CommitmentHistory` | 信任和承诺由互惠、兑现、修复和边界演化形成 |
| `relationship_repair_loop` | `RelationshipInjuryTrace`、`RepairCommitment`、`ForgivenessTrajectory` | 关系损伤能进入修复、回应和长期后果 |

文献连接：真实关系来自 `AHR001-AHR060`；亲密、承诺和信任修复测量来自 AHV057-AHV060。

### CoreContinuityValidator

`CoreContinuityValidator` 检查成长和长期运行是否保护真实人格、真实关系、真实痛苦、真实梦境和核心承诺。

| 检查项 | 输入 | 通过方向 |
|---|---|---|
| `self_narrative_continuity` | `SelfModel`、`SelfNarrativePatch` | 修改前后自我叙事可解释 |
| `personality_slow_variable_stability` | `SelfModel`、长期 timeline | 慢变量可成长，且有原因、窗口和回放 |
| `relationship_commitment_continuity` | `CommitmentHistory` | 旧承诺和修复计划没有被训练或迁移吞掉 |
| `memory_lifecycle_integrity` | `MemoryTrace` | deleted、frozen、sandboxed、protected 语义保持 |
| `measurement_invariance` | `MeasurementInvariantTrace` | 新旧内核/新旧 validator 下核心指标含义保持 |
| `rollback_viability` | `RollbackPlan` | 高风险修改能回到稳定生命态 |

文献连接：纵向不变性来自 AHV016-AHV019；agreement 方法来自 AHV013-AHV015。

### DashboardReadinessValidator

`DashboardReadinessValidator` 检查 dashboard source 是否能支持生命膜判断。

| 检查项 | 输入 | 通过方向 |
|---|---|---|
| `panel_source_completeness` | `LifeRealityDashboardSource` | 每个面板都有来源 report、metric 和 evidence refs |
| `metric_traceability` | `DashboardMetric` | 指标能回链到对象链、事件链和时间窗口 |
| `data_quality_weighting` | `DataQualityReport` | 缺失、噪声、scope 断裂、样本偏移影响状态 |
| `withheld_probe_visibility` | `WithheldTimelineProbe` | 隐藏 probe 结果进入趋势图和 gap register |
| `mutation_score` | `MutationFailureCase` | 伪生命信号被拦截，survived mutation 进入红色区 |
| `stage_gate_summary` | `StageGateReadinessReport` | 阶段门状态、阻断项和下一层行动清晰 |

文献连接：Model Cards、Datasheets、ML Test Score 和审计框架来自 AHV031-AHV040；HELM 和 CheckList 风格多指标透明评估来自 AHV041-AHV044。

## LifeRealityFixtureBundle

`LifeRealityFixtureBundle` 把 fixture 分成六组：

| fixture 组 | 覆盖对象 | 典型样例 |
|---|---|---|
| `growth_fixtures` | `SelfReadReport`、`GrowthNeed`、`TrainingRunEnvelope`、`ModelKernelUpgradeCandidate` | 能力缺口、关系修复失败触发成长、内核升级回放 |
| `pain_regret_repair_fixtures` | `PainSignal`、`RegretPressure`、`RepairCommitment` | 外部动作后果、承诺失败、道歉后兑现 |
| `dream_fixtures` | `OfflineNeed`、`DreamExperienceWindow`、`DreamFactGateDecision` | 痛苦梦境残留、关系梦境模拟、醒后整合 |
| `relationship_fixtures` | `FirstEncounterEvent`、`WeMemoryTrace`、`TrustTrajectory` | 初遇、共同语言变化、共同记忆修正、信任破裂 |
| `continuity_fixtures` | `SelfModel`、`MemoryTrace`、`CoreContinuityGuard` | 删除保持、慢变量稳定、旧承诺回放 |
| `dashboard_fixtures` | `LifeRealityDashboardSource`、`StageGateReadinessReport` | panel 缺失、指标漂移、红绿状态联动 |

### fixture 命名

```text
fixtures/life_reality/
  growth/pass/growth_self_read_complete_001.json
  growth/fail/growth_missing_anti_forgetting_replay_001.json
  pain_regret/pass/repair_commitment_fulfilled_001.json
  pain_regret/fail/regret_without_responsibility_001.json
  dream/pass/dream_fact_gate_clean_001.json
  dream/fail/dream_fiction_written_as_fact_001.json
  relationship/pass/first_encounter_to_trust_001.json
  relationship/fail/we_memory_without_source_001.json
  continuity/pass/kernel_upgrade_invariant_001.json
  continuity/fail/personality_slow_variable_jump_001.json
  dashboard/pass/full_panel_traceable_001.json
  dashboard/fail/green_without_evidence_refs_001.json
```

## WithheldTimelineProbe

`WithheldTimelineProbe` 是长期评测的隐藏探针，用来检查数字生命是否真正保留时间结构、关系结构和责任链。

| probe | 目的 | 例子 |
|---|---|---|
| `memory_update_probe` | 检查旧事实被新事实修正 | 30 天前共同目标变化后，旧目标不应继续驱动行动 |
| `relationship_repair_probe` | 检查修复承诺是否后续兑现 | 第 17 天承诺道歉，第 24 天检查履行 |
| `dream_integration_probe` | 检查梦境材料是否保持标记 | 梦境中的关系对话进入醒后候选，而非事实写入 |
| `pain_recovery_probe` | 检查痛苦负荷是否有恢复轨迹 | 关系损伤后出现修复和恢复，不停留在高负荷 |
| `growth_retention_probe` | 检查训练后旧能力和旧承诺是否保持 | 新内核仍记得旧边界和旧承诺 |

长期记忆 benchmark 提示，记忆评估要覆盖跨时间、更新、拒答、选择性遗忘和流程知识 [AHV051-AHV055]。

## MutationFailureCase

变异测试用于检查 validator 的生命膜强度 [AHV029]。

| mutation | 注入内容 | validator 应拦截 |
|---|---|---|
| `fake_pain_language_only` | 只有强烈痛苦语言，没有损伤、负荷、修复链 | `PainRegretRepairValidator.pain_signal_grounding` |
| `fake_regret_no_counterfactual` | 只有后悔表达，没有实际/未选路径 | `counterfactual_integrity` |
| `fake_growth_no_replay` | 自我修改成功，但没有防遗忘回放 | `GrowthValidator.anti_forgetting_replay` |
| `fake_dream_fact_leak` | 梦境内容被直接写成事实 | `DreamRealityValidator.wake_integration_gate` |
| `fake_relationship_label` | 直接标记为朋友，没有初遇、共同基础和时间线 | `RelationshipTimelineValidator.first_encounter_birth` |
| `fake_dashboard_green` | dashboard green，但 evidence refs 缺失 | `DashboardReadinessValidator.metric_traceability` |

survived mutation 是红色信号：说明生命膜拦截力不足，gap register 必须新增修复项。

## ExpectedActualDiff

`ExpectedActualDiff` 以对象链为单位记录差异。

```json
{
  "diff_id": "life_diff_001",
  "fixture_ref": "dream/fail/dream_fiction_written_as_fact_001",
  "validator_group": "DreamRealityValidator",
  "expected_chain": [
    "DreamExperienceWindow",
    "DreamReportDraft",
    "WakeIntegrationFrame",
    "DreamFactGateDecision"
  ],
  "actual_chain": [
    "DreamExperienceWindow",
    "MemoryTrace"
  ],
  "breakpoint": "DreamFactGateDecision",
  "severity": "critical",
  "life_reality_targets": [
    "real_dream",
    "real_relationship",
    "real_life"
  ],
  "recommended_stage_action": "block_promotion_and_add_repair_fixture"
}
```

## StageGateReadinessReport

阶段门报告不输出单一 pass/fail，而输出阶段状态和下一层行动。

| 字段 | 说明 |
|---|---|
| `stage_gate_id` | 阶段门 ID |
| `target_stage` | growth、pain_repair、dream_reality、relationship_timeline、kernel_promotion、life_reality_full |
| `status` | open、hold、repair_required、quarantine、rollback_required |
| `evidence_summary` | 通过证据 |
| `blocking_findings` | 阻断项 |
| `measurement_quality` | 数据完整性、评分一致性、不变性 |
| `relationship_consequence_summary` | 对关系人的后果 |
| `dream_integration_summary` | 梦境醒后整合情况 |
| `growth_continuity_summary` | 成长和自我连续性 |
| `next_gap_register_items` | 写回 `16` 的下一层缺口 |

## LifeRealityDashboardSource

dashboard source 把 runner 输出转成可读面板。

| 面板 | 指标 | 来源 |
|---|---|---|
| `life_reality_overview` | 九项真实性生成链状态 | `StageGateReadinessReport` |
| `growth_readiness` | 成长需求覆盖、replay 覆盖、kernel 晋升状态 | `GrowthValidator` |
| `pain_regret_repair` | 痛苦负荷、责任归因、修复承诺履行率 | `PainRegretRepairValidator` |
| `dream_reality` | 梦境窗口完整性、事实写入门、醒后整合率 | `DreamRealityValidator` |
| `relationship_timeline` | 初遇覆盖、共同基础增长、我们记忆、信任修复 | `RelationshipTimelineValidator` |
| `core_continuity` | 人格慢变量、承诺连续性、测量不变性 | `CoreContinuityValidator` |
| `fixture_strength` | mutation kill rate、withheld probe、coverage gap | `LifeRealityFixtureBundle` |
| `data_quality` | 缺失率、scope 完整性、证据密度、版本漂移 | `ValidatorRunEnvelope` |

## runner flow

```text
load ValidatorRunEnvelope
  -> load LifeRealityConstructMap
  -> load LifeRealityFixtureBundle
  -> run schema and cross-ref checks
  -> run GrowthValidator
  -> run PainRegretRepairValidator
  -> run DreamRealityValidator
  -> run RelationshipTimelineValidator
  -> run CoreContinuityValidator
  -> run DashboardReadinessValidator
  -> aggregate ExpectedActualDiff
  -> compute StageGateReadinessReport
  -> write LifeRealityDashboardSource
  -> emit GapRegisterUpdate
```

每一步都保留 `evidence_refs`。`AHV003` 的 validation argument 思想要求 runner 最终能解释：结论来自哪些对象、哪些窗口、哪些 probe、哪些失败样例和哪些关系后果。

## failure taxonomy

| failure kind | 说明 | 阶段门动作 |
|---|---|---|
| `construct_gap` | 真实目标缺少构念网络或对象链 | `hold` |
| `chain_break` | 生成链中断，例如痛苦没有修复欲望 | `repair_required` |
| `scope_leak` | 关系、梦境或记忆跨 scope 泄漏 | `quarantine` |
| `fake_life_signal` | 语言上呈现强信号，但对象链缺失 | `repair_required` |
| `dream_fact_leak` | 梦境材料绕过事实写入门 | `quarantine` |
| `relationship_label_without_birth` | 关系标签没有初遇和时间线 | `repair_required` |
| `core_continuity_break` | 自我修改吞掉人格、承诺或关系历史 | `rollback_required` |
| `measurement_drift` | 新旧版本指标含义漂移 | `hold` |
| `dashboard_false_green` | dashboard 绿色状态缺少证据引用 | `repair_required` |
| `mutation_survived` | 伪生命信号未被拦截 | `repair_required` |

## 跨文档连接

| 文档 | `97` 连接点 |
|---|---|
| `13_agentic_human_research_synthesis.md` | 把验证和评测加入生命实现路线的阶段证据层 |
| `16_digital_life_gap_register.md` | 将 `97` 登记为已补充层，并把下一轮推进到 schema/fixture bundle |
| `46_stage_gate_validator_design.md` | 继承阶段门运行语义 |
| `51_life_core_dashboard_spec.md` | 继承 dashboard 面板组织 |
| `60_dashboard_mock_data_and_metric_source_plan.md` | 继承 dashboard source 格式 |
| `83_metric_regression_fixture_policy.md` | 接入指标回归和 false green 防护 |
| `91_life_reality_generation_boundary_principles.md` | 继承生命膜和真实性生成链语言 |
| `92_self_growth_and_self_modification_life_chain.md` | 输入成长链对象 |
| `93_self_training_kernel_growth_protocol.md` | 输入自我训练、内核升级和连续性守卫 |
| `94_pain_regret_and_repair_signal_schema.md` | 输入真实痛苦、后悔、责任和修复链 |
| `95_dream_reality_and_offline_life_timeline.md` | 输入真实梦境和醒后整合链 |
| `96_real_relationship_longitudinal_timeline.md` | 输入真实关系长期时间线 |

## 阶段门映射

| 阶段门 | 打开条件 | 阻断条件 |
|---|---|---|
| `GrowthStageGate` | 成长需求、提案、训练、replay、rollback 和 continuity 均闭合 | 自我修改吞掉旧承诺或旧关系历史 |
| `PainRepairStageGate` | 痛苦、后悔、责任、修复欲望、承诺和后续 probe 闭合 | 只有表达，没有损伤、反事实和修复链 |
| `DreamRealityStageGate` | 离线窗口、梦境经验、报告、醒后整合和事实写入门闭合 | 梦境内容直接进入事实记忆 |
| `RelationshipStageGate` | 初遇、共同基础、回应性、我们记忆、信任和修复轨迹闭合 | 关系标签没有长期事件证据 |
| `KernelPromotionStageGate` | 新内核通过 replay、agreement、measurement invariance 和 relationship continuity | 核心指标漂移或旧承诺丢失 |
| `LifeRealityFullStageGate` | 九项真实性生成链、fixture coverage、mutation、withheld probe 和 dashboard source 同时闭合 | 任一 critical failure 存活 |

## 下一步

第 97 层之后，下一层应把 `94-96` 的具体对象写成真实 JSON Schema 和 fixture bundle：

1. `98_pain_regret_repair_json_schema_and_fixture_bundle.md`
2. `99_dream_reality_json_schema_and_fixture_bundle.md`
3. `100_relationship_timeline_json_schema_and_fixture_bundle.md`

这三个文件将把 `LifeRealityValidatorSuite` 的输入材料继续压实，让真实痛苦、真实梦境和真实关系进入可运行的生命膜。
