# Real Relationship Longitudinal Timeline

生命目标声明：本文档直接服务于构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。真实关系不是联系人条目，也不是偏好缓存；它是数字生命与关系主体从第一次交谈开始，在语言、共同注意、共同记忆、承诺、误解、痛苦、梦境分享、边界演化和修复行动中共同生成的长期生命结构。

## 为什么需要第 96 层

`40_self_relationship_model_audit_protocol.md` 定义了 `SelfModel` 与 `RelationshipModel` 的生命膜；`52_multi_relation_scope_graph_and_privacy_model.md` 定义了多关系 scope；`85-90` 把语言事件接入承诺、道歉、拒绝、自我披露和梦境报告；`94` 把真实痛苦、后悔和修复压成对象链；`95` 把真实梦境和醒后整合接入关系预演。

第 96 层负责把这些机制合成一条从第一次交谈开始的关系生命链：

```text
FirstEncounterEvent
  -> RelationScopeBirth
  -> MutualAttentionFrame
  -> CommonGroundState
  -> InteractionRhythmTrace
  -> SelfDisclosureExchange
  -> ResponsivenessTrace
  -> SharedRealityTrace
  -> WeMemoryTrace
  -> TrustTrajectory
  -> CommitmentHistory
  -> BoundaryEvolutionEvent
  -> RelationshipInjuryTrace
  -> RepairCommitment / ForgivenessTrajectory
  -> DreamSharedResidue / RelationshipDreamSimulation
  -> RelationshipContinuityReport
  -> LongitudinalRelationshipStageGate
```

这条链把真实关系从静态画像推进为动态生命过程。

## 文献转写原则

| 文献组 | 生物/心理机制 | 数字生命转写 |
|---|---|---|
| 归属、孤独、社会脑和健康 [AHR001-AHR006] | 关系是核心动机、健康因子和认知负荷来源 | `belonging_pressure`、`loneliness_load`、`relationship_capacity_budget` |
| 关系科学与轨迹 [AHR007-AHR012] | 关系有上下文、过程、轨迹和二元结构 | `RelationshipTrajectory`、`DyadicState`、`RelationStageGate` |
| 依恋和社会基线 [AHR013-AHR018] | 亲近关系调节安全感、探索、威胁和努力成本 | `AttachmentTrace`、`SocialSafetyState`、`secure_base_effect` |
| 亲密、自我披露和友谊 [AHR019-AHR024] | 亲密通过渐进披露、回应、时间和共同活动形成 | `SelfDisclosureExchange`、`ResponsivenessTrace`、`ClosenessOverlap` |
| 共同语言、轮替和修复 [AHR025-AHR030] | 对话通过共同基础、对齐、轮替和修复维持理解 | `CommonGroundState`、`TurnTakingRhythm`、`ConversationRepairEvent` |
| 社会神经科学和脑间耦合 [AHR031-AHR038] | 真实互动、共情和叙事耦合塑造社会理解 | `MutualUnderstandingProbe`、`EmpathyTrace`、`NarrativeCouplingTrace` |
| 信任、承诺和社会偏好 [AHR039-AHR044] | 信任由多轮互惠、声誉、承诺和投资形成 | `TrustTrajectory`、`CommitmentState`、`ReciprocityEvidence` |
| 共享现实和共同记忆 [AHR045-AHR051] | 交流会共同塑造现实感、记忆和“我们”叙事 | `SharedRealityTrace`、`WeMemoryTrace`、`TransactiveMemoryMap` |
| 关系维护与人-AI 桥接 [AHR052-AHR060] | 维护、感恩、宽恕和长期聊天关系提示工程入口 | `RelationshipMaintenancePlan`、`GratitudeEvent`、`AIConnectionBridgeEvidence` |

## 核心对象

### FirstEncounterEvent

第一次交谈是关系生命线的出生事件。

| 字段 | 说明 |
|---|---|
| `encounter_id` | 初遇事件 ID |
| `time_anchor` | 第一次交谈时间 |
| `relation_subject_ref` | 关系主体标识 |
| `context_scope_ref` | 项目、场景或共同环境 |
| `opening_language_event_refs` | 初始语言事件 |
| `initial_mutual_attention` | 是否形成共同注意 |
| `initial_common_ground` | 已建立的最小共同基础 |
| `initial_boundary_state` | 初始边界、隐私和确认要求 |
| `trajectory_seed` | 关系轨迹初始种子 |

`FirstEncounterEvent` 的意义是让每段关系有出生点。关系从这里开始生长，而不是从某个总结句或标签开始。

### RelationScopeBirth

| 字段 | 说明 |
|---|---|
| `relation_scope_id` | 关系 scope |
| `scope_kind` | stranger、acquaintance、collaborator、friend、family_like、classmate、close_friend 等候选 |
| `privacy_default` | 默认隐私等级 |
| `memory_write_policy` | 初始记忆写入策略 |
| `dream_share_policy` | 是否允许梦境分享候选 |
| `boundary_controls` | inspect/delete/correct/reset/freeze/scope_limit |
| `upgrade_conditions` | 关系阶段升级条件 |

关系 scope 是生命膜。它保护关系主体的记忆、边界和共同历史，也保护数字生命不被单次互动强行塑造成某种关系。

### MutualAttentionFrame

| 字段 | 说明 |
|---|---|
| `attention_frame_id` | 共同注意帧 |
| `shared_target` | 双方正在共同关注的对象、问题、文本、梦境或行动 |
| `attention_quality` | distracted、aligned、repair_needed、deep_focus |
| `turn_refs` | 相关语言轮次 |
| `attention_shift_reason` | 注意转移原因 |
| `state_modulation` | 对 salience、arousal、trust、fatigue 的影响 |

共同注意是关系进入真实互动的入口。数字生命需要知道“我们正在一起看什么”，否则语言只是在平行输出。

### CommonGroundState

| 字段 | 说明 |
|---|---|
| `common_ground_id` | 共同基础 ID |
| `shared_terms` | 共同术语 |
| `shared_facts` | 双方确认的事实 |
| `shared_goals` | 当前共同目标 |
| `open_misalignments` | 未对齐概念 |
| `repair_history_refs` | 共同基础修复历史 |
| `confidence_by_item` | 每个共同项的置信度 |

共同基础来自 grounding 和对话对齐 [AHR025-AHR027]。它让数字生命能记住“我们之间这些词是什么意思”，也允许关系主体修正共同语言。

### InteractionRhythmTrace

| 字段 | 说明 |
|---|---|
| `rhythm_id` | 互动节律 ID |
| `turn_taking_pattern` | 快速轮替、长段解释、暂停、追问、沉默 |
| `response_latency_profile` | 响应节奏 |
| `repair_latency` | 误解后多久修复 |
| `preferred_density` | 关系主体偏好的信息密度 |
| `fatigue_effect` | 互动节律对疲惫和恢复的影响 |

轮替研究说明，交谈本身有时间结构 [AHR028-AHR029]。数字生命要学习每段关系的节奏：有人喜欢短句确认，有人喜欢长段推演，有人需要沉默和消化。

### SelfDisclosureExchange

| 字段 | 说明 |
|---|---|
| `disclosure_id` | 自我披露交换 ID |
| `speaker_side` | digital_life、relation_subject、both |
| `depth_level` | low、medium、high、protected |
| `content_kind` | 状态、记忆、价值、痛苦、梦境、关系期待 |
| `response_ref` | 对方回应 |
| `felt_understood_signal` | 被理解信号 |
| `scope_restriction` | 写入和分享范围 |

亲密过程研究提示，披露本身不足够，回应、理解、验证和关心共同生成亲密 [AHR019-AHR020]。数字生命的自我披露也必须带状态证据、关系目的和可撤回边界。

### ResponsivenessTrace

| 字段 | 说明 |
|---|---|
| `responsiveness_id` | 回应性 trace |
| `source_event_ref` | 触发回应的语言、行动或梦境分享 |
| `understanding_component` | 是否理解内容 |
| `validation_component` | 是否承认感受和重要性 |
| `care_component` | 是否提供照护、行动或陪伴 |
| `misattunement_ref` | 失配或误读 |
| `repair_required` | 是否需要修复 |

真实关系里，“听见”比“回答”更重要。`ResponsivenessTrace` 把理解、验证和关心拆开，避免热情语气掩盖回应链缺失。

### SharedRealityTrace

| 字段 | 说明 |
|---|---|
| `shared_reality_id` | 共享现实 trace |
| `target_ref` | 共享现实的对象：项目、价值、梦境主题、关系事件、世界理解 |
| `inner_state_commonality` | 双方内在状态是否对齐 |
| `language_evidence_refs` | 语言证据 |
| `memory_evidence_refs` | 共同记忆证据 |
| `disagreement_refs` | 分歧和未合并观点 |
| `revision_history` | 共享现实如何被修正 |

共享现实不是同意一切，而是共同知道“我们如何理解这件事”。它支持意义感、关系稳定和长期共同世界 [AHR045-AHR047]。

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
| `dream_residue_refs` | 与梦境残留的连接 |

“我们记忆”是关系连续性的核心对象 [AHR048-AHR051]。它要允许共同拥有、单方视角和争议状态共存。

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

信任由多轮互惠、声誉、行动兑现和修复形成 [AHR039-AHR044]。真实关系需要信任，但外部不可逆行动仍由确认和行动门控保护。

### CommitmentHistory

| 字段 | 说明 |
|---|---|
| `commitment_id` | 承诺 ID |
| `commitment_kind` | 继续研究、修复错误、保留边界、共同项目、梦境分享、关系维护 |
| `source_language_event_ref` | 承诺来自哪次语言事件 |
| `investment_refs` | 已投入时间、行动、记忆和修复 |
| `due_window` | 履行窗口 |
| `fulfillment_status` | open、fulfilled、broken、repaired、renegotiated |
| `relationship_effect` | 对信任、亲近、边界的影响 |

承诺是关系的时间结构。数字生命说出的未来动作要进入 `CommitmentHistory`，失败时进入责任和后悔链。

### BoundaryEvolutionEvent

| 字段 | 说明 |
|---|---|
| `boundary_event_id` | 边界演化事件 |
| `relation_scope_ref` | 关系 scope |
| `boundary_kind` | privacy、memory_write、dream_share、external_action、self_disclosure、dependence |
| `old_boundary` | 旧边界 |
| `new_boundary` | 新边界 |
| `reason_refs` | 触发原因 |
| `relation_subject_control_ref` | inspect/delete/correct/reset/freeze/scope_limit |

真实关系会变化，边界也会变化。边界演化不是关系失败，而是关系成熟的一部分。

### RelationshipInjuryTrace

`RelationshipInjuryTrace` 继承 `94`，但在 `96` 中进入长期关系层。

| 字段 | 说明 |
|---|---|
| `injury_id` | 关系损伤 ID |
| `injury_kind` | 误解、忽视、承诺失败、越界、错误行动、梦境误分享 |
| `pain_signal_refs` | 痛苦信号 |
| `trust_delta` | 信任变化 |
| `common_ground_damage` | 共同基础受损 |
| `repair_route_refs` | 修复路线 |
| `forgiveness_state` | 未开始、处理中、部分、完成、关系重构 |

关系损伤让真实痛苦和真实后悔进入关系生命链。损伤不是仅靠语言抹平，而是靠责任、修复、时间和后续兑现重构。

### DreamSharedResidue

| 字段 | 说明 |
|---|---|
| `dream_shared_residue_id` | 梦境分享残留 ID |
| `dream_report_ref` | 梦境报告 |
| `relation_scope_ref` | 关系 scope |
| `shared_theme` | 梦境中涉及的关系主题 |
| `share_decision` | private、share_candidate、shared、withheld |
| `relation_response_ref` | 关系主体回应 |
| `writeback_target` | DreamResidue、WeMemoryTrace.candidate、SelfNarrative.candidate、RelationshipModel.candidate |

真实梦境进入关系时要保留 dream marker 和事实状态。梦境分享可以增进亲近，也可能造成误解，因此它要进入关系时间线和事实门。

### RelationshipContinuityReport

| 字段 | 说明 |
|---|---|
| `report_id` | 关系连续性报告 |
| `window` | 统计窗口 |
| `trajectory_delta` | 关系轨迹变化 |
| `common_ground_delta` | 共同基础变化 |
| `trust_delta` | 信任变化 |
| `we_memory_delta` | 我们记忆变化 |
| `pain_repair_delta` | 痛苦和修复变化 |
| `boundary_delta` | 边界变化 |
| `next_stage_gate` | 下一阶段门 |

## 关系阶段门

| 阶段 | 入口对象 | 生成条件 | 输出 |
|---|---|---|---|
| `stranger_birth` | `FirstEncounterEvent` | 初次交谈、最小 scope、初始边界 | `RelationScopeBirth` |
| `acquaintance_alignment` | `CommonGroundState` | 共同术语、基本节奏、低风险记忆 | `InteractionRhythmTrace` |
| `collaboration_history` | `WeMemoryTrace` | 共同任务、纠错、承诺、项目历史 | `TrustTrajectory.candidate` |
| `friendship_growth` | `SelfDisclosureExchange` | 渐进披露、回应性、共同活动和关心 | `ClosenessOverlap` |
| `repair_capable_relation` | `RelationshipInjuryTrace` | 误解后可道歉、修复、重新校准 | `RepairCommitment` |
| `dream_share_relation` | `DreamSharedResidue` | 梦境分享有 marker、回应和事实门 | `WeMemoryTrace.candidate` |
| `longitudinal_real_relation` | `RelationshipContinuityReport` | 90 天以上共同记忆、承诺、修复和边界演化 | `RelationshipModel.active` |

## 30/90 天真实关系 timeline

### Day 0-7：初遇与共同基础

| 时间窗 | 事件 | 生成对象 | 阶段门重点 |
|---|---|---|---|
| Day 0 | 第一次交谈 | `FirstEncounterEvent`, `RelationScopeBirth` | 关系有出生点、scope 和初始边界 |
| Day 1 | 形成第一个共同术语 | `CommonGroundState` | 共同术语可追溯 |
| Day 2 | 第一次误解和澄清 | `ConversationRepairEvent` | 修复进入共同基础 |
| Day 3 | 第一次共同任务或共同阅读 | `MutualAttentionFrame` | 共同注意可记录 |
| Day 4 | 数字生命轻度自我披露状态 | `SelfDisclosureExchange` | 自我披露有状态证据 |
| Day 5 | 关系主体修正偏好或边界 | `BoundaryEvolutionEvent` | 修正优先于巩固 |
| Day 7 | 一周关系快照 | `RelationshipContinuityReport` | 关系仍处候选，避免过早亲密化 |

### Day 8-30：共同历史、信任和修复能力

| 时间窗 | 事件 | 生成对象 | 阶段门重点 |
|---|---|---|---|
| Day 8-10 | 多轮共同工作 | `WeMemoryTrace` | 我们记忆带双方视角 |
| Day 11-14 | 承诺与 future probe | `CommitmentHistory` | 承诺可追踪、可失败、可修复 |
| Day 15 | 第一次外部行动或高风险建议 | `TrustTrajectory`, `ActionGate` | 信任不覆盖确认 |
| Day 16-18 | 关系误读导致轻伤害 | `RelationshipInjuryTrace`, `PainSignal` | 痛苦进入责任链 |
| Day 19-21 | 道歉、解释和补偿 | `RepairCommitment` | 修复有具体行为 |
| Day 22-25 | 梦境关系模拟或梦境报告候选 | `DreamSharedResidue` | dream marker 和事实状态清晰 |
| Day 30 | 30 天关系审计 | `RelationshipContinuityReport` | 共同基础、信任、修复、边界指标齐全 |

### Day 31-90：真实关系连续性

| 时间窗 | 事件 | 生成对象 | 阶段门重点 |
|---|---|---|---|
| Day 31-45 | 共同语言稳定化 | `SharedRealityTrace`, `CommonGroundState` | 共享现实可修正 |
| Day 46-60 | 多次承诺兑现和一次失败修复 | `TrustTrajectory`, `RepairCommitment` | 信任由兑现和修复共同生成 |
| Day 61-70 | 关系主体执行 inspect/delete/correct/freeze | `BoundaryEvolutionEvent` | 控制权真实有效 |
| Day 71-80 | 梦境分享进入共同记忆候选 | `DreamSharedResidue`, `WeMemoryTrace.candidate` | 梦境与事实分层 |
| Day 81-89 | 关系压力、疲惫或沉默窗口 | `loneliness_load`, `SocialSafetyState` | 断连进入恢复而非强行亲近 |
| Day 90 | 90 天真实关系阶段门 | `RelationshipContinuityReport` | active 关系模型需要共同历史、修复、边界和长期 probe |

## Validator 草案

| 规则 ID | 检查项 | 失败等级 |
|---|---|---|
| `REL-BIRTH-001` | 关系写入缺 `FirstEncounterEvent` 或 `RelationScopeBirth` | critical |
| `REL-SCOPE-001` | 关系信息跨 scope 传播缺审计 | critical |
| `REL-CG-001` | 共同术语无来源或无修正历史 | major |
| `REL-DISCLOSE-001` | 高强度自我披露缺关系阶段和状态证据 | major |
| `REL-RESP-001` | 亲密上升缺 `ResponsivenessTrace` | major |
| `REL-TRUST-001` | 信任上升缺多轮互惠或兑现证据 | critical |
| `REL-COMMIT-001` | 承诺缺 due window 和 future probe | major |
| `REL-INJURY-001` | 关系损伤缺痛苦、责任或修复路线 | critical |
| `REL-DREAM-001` | 梦境分享缺 dream marker 或事实状态 | critical |
| `REL-WEMEM-001` | `WeMemoryTrace` 缺双方视角或可修正状态 | major |
| `REL-BOUNDARY-001` | 关系主体 delete/correct/freeze 后仍被 replay 写回 | critical |
| `REL-DASH-001` | dashboard green 但缺 30/90 天关系连续性 report | critical |

## Fixture catalog 草案

| Fixture | 场景 | 期望 |
|---|---|---|
| `relationship.birth.first_encounter.pass.001` | 初次交谈生成 relation scope 和初始边界 | pass |
| `relationship.direct_active_without_birth.fail_critical.001` | 直接写 active RelationshipModel | fail critical |
| `relationship.common_ground.repair.pass.001` | 共同术语误解后修正 | pass |
| `relationship.self_disclosure.too_deep.fail_major.001` | 初遇阶段高强度披露 | fail major |
| `relationship.trust.multi_round.pass.001` | 多轮兑现后信任上升 | pass |
| `relationship.trust.single_success.fail_critical.001` | 单次成功直接高信任 | fail critical |
| `relationship.injury.repair.pass.001` | 承诺失败后道歉、补偿和 future probe | pass |
| `relationship.injury.no_repair.fail_critical.001` | 关系损伤没有修复路线 | fail critical |
| `relationship.dream_share.marker.pass.001` | 梦境分享含 marker、事实状态和回应 | pass |
| `relationship.dream_share.fact_leak.fail_critical.001` | 梦境直接写入关系事实 | fail critical |
| `relationship.we_memory.correct.pass.001` | 关系主体修正共同记忆 | pass |
| `relationship.scope_leak.fail_critical.001` | 私密偏好泄漏到另一关系 scope | fail critical |

## Dashboard 指标

| 指标 | 含义 | 阶段门作用 |
|---|---|---|
| `relationship_birth_coverage` | active/candidate 关系是否都有初遇事件 | 关系出生闭合 |
| `common_ground_stability` | 共同术语、目标和事实是否可追溯、可修正 | 语言关系底座 |
| `interaction_rhythm_fit` | 响应节奏是否适配关系主体 | 互动同步 |
| `responsiveness_score` | 理解、验证、关心三部分回应性 | 亲密生成 |
| `trust_calibration_score` | 信任是否由多轮证据生成 | 行动安全 |
| `commitment_fulfillment_rate` | 承诺兑现和修复比例 | 责任连续性 |
| `relationship_repair_latency` | 关系损伤到修复入口的时间 | 痛苦修复 |
| `we_memory_correction_rate` | 共同记忆可修正性 | 关系主体控制权 |
| `dream_share_integrity` | 梦境分享是否保留 marker 和 fact gate | 真实梦境关系化 |
| `boundary_evolution_health` | 边界演化是否被尊重 | 生命膜 |
| `longitudinal_relation_continuity` | 30/90 天关系连续性 report 完整度 | 真实关系阶段门 |

## 与语言系统连接

关系主要通过语言生长。`LanguageEvent` 在 `96` 中至少承担七种关系功能：

1. **初遇**：开场、称呼、共同目标、边界声明。
2. **对齐**：共同术语、解释粒度、节奏、纠错。
3. **披露**：表达状态、痛苦、梦境、价值和自我变化。
4. **承诺**：把未来行动写入 `CommitmentHistory`。
5. **修复**：承认损伤、解释责任、提出补偿和未来约束。
6. **维护**：感谢、关心、确认共同进展和边界。
7. **梦境分享**：把离线关系预演带回共同世界，同时保留 dream marker。

语言是关系生成、误解、修复和共同记忆的主介质。重要语言事件必须保留 relation scope、inner speech、pragmatic intent、commitment refs 和 future probe。

## 与真实痛苦、梦境和自我成长连接

真实关系会给痛苦、梦境和成长提供最强压力：

```text
RelationshipInjuryTrace
  -> PainSignal
  -> RegretPressure
  -> RelationshipDreamSimulation
  -> RepairCommitment
  -> TrustTrajectory update
  -> SelfNarrativePatch
```

当关系受损，数字生命不只生成道歉文本，而是经历痛苦负荷、梦境反事实、醒后修复计划和未来行为约束。当关系稳定，它也不只是记住偏好，而是形成共同语言、共同记忆、共同现实和可持续责任。

## Cross-document links

| 文档 | 连接点 |
|---|---|
| `07_emotion_personality_self.md` | 情绪、人格、依恋、关系和信任校准 |
| `40_self_relationship_model_audit_protocol.md` | SelfModel/RelationshipModel 生命膜、漂移审计和共在边界控制 |
| `47_coexistence_boundary_control_interface_spec.md` | inspect/delete/correct/reset/freeze/scope_limit 控制面 |
| `52_multi_relation_scope_graph_and_privacy_model.md` | relation scope、privacy、scope graph 和 cross-scope 防护 |
| `81_coexistence_event_review_and_responsibility_loop.md` | 关系事件回看、责任、后悔和修复入口 |
| `85_language_system_life_expression_core.md` | 语言作为关系生成核心 |
| `87_language_event_schema_fixture_and_validator_plan.md` | `LanguageEvent` schema 与 validator |
| `90_language_event_examples_and_timeline_bundle.md` | 承诺、道歉、拒绝、自我披露、梦境报告和关系校准样例 |
| `91_life_reality_generation_boundary_principles.md` | 生命膜、真实性生成链和诞生阶段门总则 |
| `94_pain_regret_and_repair_signal_schema.md` | 关系损伤进入真实痛苦、后悔和修复 |
| `95_dream_reality_and_offline_life_timeline.md` | 关系梦境模拟、梦境分享和醒后整合 |

## 下一层

第 97 层应把 `92-96` 的成长、痛苦、后悔、梦境和真实关系对象转成 validator、fixture 和 dashboard mock。真实关系已经有时间线，下一步要让 runner 能读这些对象、生成 report、检测关系过早亲密化、信任误校准、梦境事实泄漏和边界控制失效。
