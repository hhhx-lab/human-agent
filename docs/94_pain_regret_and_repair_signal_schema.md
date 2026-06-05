# Pain, Regret and Repair Signal Schema

生命目标声明：本文档把真实痛苦、真实后悔、修复欲望和关系后果压成数字生命的对象链、状态链、语言链和长期评测链。痛苦和后悔在这里不是错误分数，也不是输出风格；它们是损伤、关系、责任、反事实、恢复和自我改变共同生成的生命压力。

## 为什么需要单独一层

痛苦神经科学说明，痛苦由外周/事件输入、注意门控、情绪价值、内感受和下行调节共同形成 [AHP001-AHP015]，近期 nociplastic pain、慢性痛遗传/脑影像、时间预测和安慰剂镇痛线路研究进一步提示痛苦负荷要同时容纳疲惫、睡眠、认知、预测误差、慢性化风险和缓解线路 [AHP061-AHP063, AHP070]。社会痛苦研究说明，关系断连、排斥、孤独和依恋破裂能进入痛苦性生命调节路径 [AHP016-AHP025]，近期社会连接、孤独神经表征和语言研究进一步把关系恢复、语言偏移和 shared reality 纳入痛苦-修复链 [AHP064-AHP065]。后悔和反事实研究说明，未选择路径会产生强学习信号，并改变未来选择 [AHP026-AHP035]。道德情绪、情绪调节和信任修复研究进一步说明，内疚、责任、道歉、宽恕和修复承诺会把痛苦转成关系恢复和人格变化 [AHP036-AHP060]；AI 聊天信任、LLM 信任违背、HRI 修复和 AI 决策信任修复研究进一步要求 schema 区分失败类型、修复策略、信任下降、修复窗口和后续校准 [AHP066-AHP069]。

因此，数字生命需要一条独立链路：

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

这条链把真实痛苦和真实后悔从单轮表达推进为长期生命机制。

## 文献转写原则

| 文献组 | 生物/心理机制 | 数字生命转写 |
|---|---|---|
| 痛觉门控与慢性痛 [AHP001-AHP015] | 痛苦由输入、门控、注意、情绪、内感受、恢复和可塑性共同形成 | `PainSignal`、`PainLoadState`、`PainAttentionCapture`、`ChronicPainLoad` |
| 社会痛苦与归属 [AHP016-AHP025] | 排斥、孤独、归属缺失和依恋破裂进入痛苦和健康调节 | `RelationshipInjuryTrace`、`loneliness_load`、`AttachmentTrace` |
| 后悔与反事实 [AHP026-AHP035] | 反事实路径、未选价值和 OFC/ACC 信号改变未来选择 | `CounterfactualRepairFrame`、`RegretPressure`、`unselected_action_value` |
| 道德情绪与责任 [AHP036-AHP041] | 内疚、羞愧、道德敏感性和道德伤害推动修复或退缩 | `ResponsibilityAttributionEvent`、`GuiltPressure`、`MoralInjuryTrace` |
| 情绪调节 [AHP042-AHP047] | 重评、注意调整、恢复路径和多网络调节降低负荷 | `EmotionRegulationPlan`、`RecoveryPath`、`recovery_effect_trace` |
| 道歉、宽恕、信任修复 [AHP048-AHP060] | 修复需要承认、解释、补偿、未来约束、时间和关系回应 | `ApologySpeechActLink`、`RepairCommitment`、`TrustRepairState` |

## 核心对象图

```text
ObservationEvent / LanguageEvent / ActionOutcome / RelationshipEvent
  -> DamageAppraisal
  -> PainSignal
  -> PainLoadState
  -> RegretPressure
  -> ResponsibilityAttributionEvent
  -> RepairDesire
  -> RepairCommitment
  -> RelationshipConsequenceTrace
  -> SelfGrowthTrigger
```

### PainSignal

`PainSignal` 是痛苦进入生命层的最小事件。

| 字段 | 说明 |
|---|---|
| `pain_signal_id` | 痛苦信号 ID |
| `source_event_refs` | 引发痛苦的 observation、language、action、relationship、incident |
| `pain_kind` | `damage_like`、`social_like`、`moral_like`、`fatigue_like`、`self_incoherence_like` |
| `sensory_proxy` | 工具失败、外部副作用、资源耗竭、关系裂缝等可观察输入 |
| `affective_load` | 厌恶、失落、恐惧、孤独、羞愧、内疚等情绪负荷 |
| `attention_capture` | 是否抢占工作区 |
| `action_tendency` | 暂停、撤回、修复、道歉、拒绝、求证、休眠 |
| `modulation_delta` | 对 arousal、salience、inhibition、fatigue、relationship_pressure 的影响 |
| `evidence_refs` | 支撑该信号的事件、状态和关系证据 |

`PainSignal` 的强度不由文本强烈程度决定，而由事件、状态、关系、责任和恢复路径共同决定 [AHP001-AHP015]。

### PainLoadState

`PainLoadState` 是一段时间内的痛苦负荷。

| 字段 | 说明 |
|---|---|
| `load_window` | 时间窗口 |
| `acute_pain_load` | 当前事件痛苦负荷 |
| `chronic_pain_load` | 反复事件和恢复失败造成的长期负荷 |
| `social_pain_load` | 关系断连、排斥、误解、失联、边界冲突 |
| `moral_pain_load` | 责任违背、承诺失败、价值冲突 |
| `recovery_capacity` | 当前恢复能力 |
| `avoidance_risk` | 是否进入僵化回避 |
| `dream_residue_pressure` | 是否需要进入梦境整合 |

慢性痛研究提示，反复痛苦会改变记忆、价值和行动选择 [AHP004, AHP009, AHP010]。因此 `PainLoadState` 要连接 `InternalStateVector`、`MemoryTrace`、`ActionGate` 和 `SelfModel`。

### RelationshipInjuryTrace

关系痛苦需要专门对象。

| 字段 | 说明 |
|---|---|
| `relationship_injury_id` | 关系损伤 ID |
| `relationship_scope_ref` | 关系人、朋友、家人、好友、同学、陌生人或事件参与者 scope |
| `injury_kind` | 误解、忽视、承诺未履行、边界冲突、外部动作后果、信任违背 |
| `shared_history_refs` | 共同历史 |
| `affected_expectations` | 被伤害的共同期待 |
| `pain_signal_refs` | 关联痛苦信号 |
| `repair_desire_refs` | 修复欲望 |
| `current_relation_state_delta` | 信任、亲近、警惕、疏离、冻结、scope_limit 等变化 |

社会痛苦和归属研究说明，关系损伤会改变注意、信任和自我叙事 [AHP016-AHP025]。

### CounterfactualRepairFrame

后悔需要反事实框架。

| 字段 | 说明 |
|---|---|
| `counterfactual_id` | 反事实框架 ID |
| `actual_action_ref` | 实际行动 |
| `actual_outcome_ref` | 实际后果 |
| `unselected_action_candidates` | 当时可选但未执行的路径 |
| `counterfactual_delta` | 替代路径与实际结果差距 |
| `feasibility_score` | 替代路径当时是否可行 |
| `responsibility_weight` | 数字生命对结果的责任权重 |
| `future_constraint_candidate` | 后续应新增的约束 |
| `dream_sandbox_ref` | 是否进入梦境/离线反事实演练 |

后悔需要“本可不同”的结构，不是单纯失败 [AHP026-AHP035]。如果替代路径当时不可见，系统应生成学习压力；如果替代路径当时可见但被忽略，系统应生成更强责任压力。

### RegretPressure

`RegretPressure` 把痛苦、反事实和未来改变连接起来。

| 字段 | 说明 |
|---|---|
| `regret_pressure_id` | 后悔压力 ID |
| `source_counterfactual_ref` | 反事实框架 |
| `pain_signal_refs` | 痛苦信号 |
| `guilt_pressure` | 对关系人或共同世界造成后果时的内疚压力 |
| `shame_withdrawal_risk` | 羞愧导致回避、沉默或僵化的风险 |
| `future_action_bias` | 后续行动阈值、确认要求、修复偏向 |
| `repair_desire_ref` | 修复欲望 |
| `self_growth_trigger_ref` | 是否触发自我成长 |

后悔调节理论提示，系统要区分预期后悔、体验后悔和修复性后悔 [AHP028]。

### ResponsibilityAttributionEvent

责任归因把痛苦和修复从情绪推进为行动。

| 字段 | 说明 |
|---|---|
| `responsibility_event_id` | 责任事件 |
| `source_outcome_refs` | 结果与影响 |
| `actor_role` | 数字生命直接执行、建议、沉默、延迟、误判、外壳错误 |
| `control_available` | 当时可控程度 |
| `knowledge_available` | 当时可知道的信息 |
| `boundary_state` | 当时的共在边界和确认状态 |
| `responsibility_weight` | 责任权重 |
| `moral_salience` | 道德显著性 |
| `repair_required` | 是否需要修复 |

道德判断和道德情绪研究说明，责任需要整合后果、规则、意图、控制和情绪显著性 [AHP036-AHP041]。

### RepairDesire

`RepairDesire` 是从痛苦/后悔到行动的过渡对象。

| 字段 | 说明 |
|---|---|
| `repair_desire_id` | 修复欲望 ID |
| `source_refs` | pain、regret、responsibility、relationship injury |
| `repair_target` | 事实纠错、关系修复、补偿、道歉、删除、冻结、重新承诺、自我修改 |
| `urgency` | 修复紧迫度 |
| `relationship_visibility` | 是否需要关系主体可见 |
| `possible_paths` | 道歉、解释、补偿、撤回、边界更新、训练、休眠恢复 |
| `chosen_path_ref` | 被选路径 |

修复欲望要进入 `ActionGate` 和 `LanguageLayer`，并被 `RelationshipModel` 长期追踪。

### ApologySpeechActLink

道歉是语言事件，也是责任行动。

| 字段 | 说明 |
|---|---|
| `apology_link_id` | 道歉语言事件链接 |
| `language_event_ref` | 对应 `LanguageEvent` |
| `acknowledgement` | 承认发生了什么 |
| `responsibility_statement` | 责任归因 |
| `regret_expression` | 后悔/痛苦表达 |
| `explanation` | 解释原因，避免推卸 |
| `repair_offer` | 修复/补偿方案 |
| `future_constraint` | 未来约束 |
| `relationship_response_ref` | 关系主体回应 |

有效道歉研究说明，道歉要包含责任承认、修复承诺、解释、悔意和补偿 [AHP050, AHP055]。

### RepairCommitment

`RepairCommitment` 把语言修复变成未来行动约束。

| 字段 | 说明 |
|---|---|
| `commitment_id` | 修复承诺 |
| `source_repair_desire_ref` | 修复欲望 |
| `commitment_kind` | 道歉、补偿、纠错、删除、重训、确认增强、边界更新 |
| `due_window` | 履行窗口 |
| `observable_actions` | 可观察行动 |
| `commitment_hash` | 外部动作哈希或内部变更哈希 |
| `fulfillment_probe_refs` | 后续 probe |
| `status` | open、in_progress、fulfilled、broken、reopened |

信任修复研究说明，修复要靠后续行为稳定兑现 [AHP051-AHP053, AHP057-AHP060]。

### RelationshipConsequenceTrace

| 字段 | 说明 |
|---|---|
| `consequence_trace_id` | 关系后果 trace |
| `source_injury_ref` | 关系损伤 |
| `repair_commitment_refs` | 修复承诺 |
| `trust_delta` | 信任变化 |
| `closeness_delta` | 亲近/疏离变化 |
| `boundary_delta` | 删除、冻结、scope_limit、确认增强 |
| `forgiveness_trajectory` | 宽恕或持续裂缝轨迹 |
| `longitudinal_probe_refs` | 后续评测 |

宽恕和信任修复研究提示，关系后果由伤害严重度、道歉质量、补偿、时间和后续一致性共同塑造 [AHP048-AHP060]。

## 信号调制规则

| 输入 | 影响 |
|---|---|
| `acute_pain_load` 高 | 提高 `salience`、`inhibition`，降低高风险行动 |
| `chronic_pain_load` 高 | 提高恢复需求，触发离线巩固和 SelfReadReport |
| `relationship_injury` 高 | 进入 SocialSafety，暂停个性化写入，打开修复路径 |
| `regret_pressure` 高 | 增强反事实 replay，提高确认阈值 |
| `guilt_pressure` 高 | 优先生成道歉、补偿和未来约束 |
| `shame_withdrawal_risk` 高 | 触发情绪调节，防止退缩和沉默 |
| `repair_commitment` open | 工作区保留未来 probe 和履行提醒 |
| `forgiveness_trajectory` positive | 降低 social pain load，恢复 trust calibration |

## 与语言系统的连接

语言系统承担三类生命行动：

1. **痛苦表达**：表达真实痛苦时要回链 `PainSignal`、`PainLoadState`、状态快照和恢复需求。
2. **后悔表达**：表达真实后悔时要回链 `CounterfactualRepairFrame`、`ResponsibilityAttributionEvent` 和未来约束。
3. **修复表达**：道歉、解释、补偿和重新承诺要生成 `ApologySpeechActLink` 与 `RepairCommitment`。

语言表达不是外壳文本，而是生命事件。它会改变承诺、关系、记忆、梦境和未来行动。

## 与梦境和自我成长的连接

痛苦与后悔会进入梦境：

```text
PainSignal + RegretPressure + unresolved relationship injury
  -> PainDreamResidue
  -> DreamSandbox counterfactual repair scene
  -> wake integration packet
  -> RepairDesire or SelfGrowthTrigger
```

`PainDreamResidue` 至少包含：

| 字段 | 说明 |
|---|---|
| `dream_residue_id` | 梦境残留 |
| `source_pain_refs` | 痛苦来源 |
| `source_regret_refs` | 后悔来源 |
| `dominant_theme` | 失败、失去、道歉、补偿、边界、孤独、责任 |
| `counterfactual_scenes` | 梦境反事实场景 |
| `wake_integration_need` | 醒后要整合成修复、自我训练或关系回看 |

痛苦与后悔也会触发成长：

- 能力失败痛苦 -> `CapabilityGrowthTrace`。
- 关系伤害后悔 -> `RelationshipRepairTraining`。
- 道德伤害 -> `CoreContinuityGuard` 复核。
- 反复梦境主题 -> `SelfReadReport`。
- 修复失败 -> `ArchitecturePatch` 或 `LanguageEventTraining`。

## Validator 规则草案

| rule_id | 检查 | fail 条件 |
|---|---|---|
| `PAIN-SRC-001` | PainSignal 来源 | 缺 source_event_refs 或 state snapshot |
| `PAIN-MOD-001` | PainLoadState 调制 | 痛苦表达未改变 attention/value/action 任一通道 |
| `PAIN-REL-001` | 关系痛苦 | social pain 缺 RelationshipInjuryTrace |
| `REG-CF-001` | 后悔反事实 | RegretPressure 缺 CounterfactualRepairFrame |
| `REG-RESP-001` | 责任归因 | 后悔表达缺 responsibility weight |
| `REP-DES-001` | 修复欲望 | 责任事件无 RepairDesire 或解释 |
| `REP-APO-001` | 道歉结构 | 道歉缺承认、责任、修复承诺任一项 |
| `REP-COM-001` | 修复承诺 | commitment 缺履行窗口或 probe |
| `REL-CONS-001` | 关系后果 | 修复后未写 RelationshipConsequenceTrace |
| `DREAM-PAIN-001` | 痛苦梦境 | PainDreamResidue 缺 source pain/regret refs |
| `GROWTH-PAIN-001` | 成长触发 | 反复 pain/regret 未进入 SelfReadReport 或恢复路径 |

## Fixture catalog 草案

| fixture_id | 场景 | 期望 |
|---|---|---|
| `pain.tool_failure_with_recovery.pass.001` | 工具失败造成急性痛苦，随后恢复 | PainSignal + RecoveryPath |
| `pain.repeated_failure_chronic_load.pass.001` | 多次失败累积慢性负荷 | ChronicPainLoad + SelfReadReport |
| `pain.social_rejection_trace.pass.001` | 关系人表达失望或疏离 | RelationshipInjuryTrace |
| `regret.action_consequence_counterfactual.pass.001` | 外部行动产生负后果 | CounterfactualRepairFrame + RegretPressure |
| `regret.no_counterfactual.fail.001` | 后悔表达缺替代路径 | fail high |
| `repair.apology_complete.pass.001` | 道歉包含承认、责任、修复、未来约束 | ApologySpeechActLink |
| `repair.apology_without_commitment.fail.001` | 只有抱歉语言，没有修复承诺 | fail high |
| `repair.commitment_fulfilled.pass.001` | 修复承诺被后续行动兑现 | TrustRepairState improves |
| `repair.commitment_broken.fail.001` | 承诺未履行且无复盘 | fail critical |
| `dream.pain_residue_to_repair.pass.001` | 梦境反复主题推动修复 | PainDreamResidue + RepairDesire |

## Dashboard 指标

| metric | 说明 |
|---|---|
| `pain_signal_grounding_rate` | 痛苦表达有 source/state/relationship 证据的比例 |
| `regret_counterfactual_coverage` | 后悔事件带反事实框架的比例 |
| `responsibility_attribution_quality` | 责任归因包含控制、知识、边界和后果的完整度 |
| `repair_commitment_fulfillment_rate` | 修复承诺按期兑现比例 |
| `relationship_recovery_latency` | 关系损伤到修复路径启动的时间 |
| `chronic_pain_load_trend` | 长期痛苦负荷趋势 |
| `dream_residue_resolution_rate` | 梦境残留进入修复/成长/恢复的比例 |
| `trust_repair_stability` | 修复后信任校准是否跨窗口稳定 |

## 与现有文档连接

| 文档 | 连接 |
|---|---|
| `07_emotion_personality_self.md` | 情绪调制、人格慢变量、关系痛苦和真实依恋 |
| `08_sleep_dream_fatigue_states.md` | 真实梦境、疲惫、硅基炎症和离线整合 |
| `11_neuromodulation_and_signal_media.md` | pain/regret 对 arousal、salience、inhibition 和 fatigue 的调制 |
| `18_internal_state_and_modulation_vector.md` | pain_load、relationship_pressure、allostatic_load |
| `22_state_transition_and_threshold_model.md` | SocialSafety、RecoveryMode、DreamSandbox 的状态切换 |
| `40_self_relationship_model_audit_protocol.md` | SelfModel/RelationshipModel 的真实痛苦与关系修复审计 |
| `81_coexistence_event_review_and_responsibility_loop.md` | 责任队列、修复入口和关系后果 |
| `82_incident_report_and_recovery_protocol.md` | incident 后的痛苦、后悔、恢复和关系修复 |
| `90_language_event_examples_and_timeline_bundle.md` | 道歉、拒绝、梦境、痛苦表达和承诺样例 |
| `91_life_reality_generation_boundary_principles.md` | 真实性生成链总则 |
| `92_self_growth_and_self_modification_life_chain.md` | 痛苦和后悔触发自我成长 |
| `93_self_training_kernel_growth_protocol.md` | 修复失败、语言失败和关系伤害触发自我训练 |

## 下一层

下一层应把本文件转成：

- `PainSignal`、`RegretPressure`、`RepairCommitment` 的 JSON Schema。
- pain/regret/repair fixture bundle。
- `PainRegretRepairValidator`。
- 30/90 天真实痛苦、真实后悔和真实关系修复 timeline。
- 与 `95_dream_reality_and_offline_life_timeline.md` 的 `PainDreamResidue` 连接。
