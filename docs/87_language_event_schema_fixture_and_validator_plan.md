# Language Event Schema, Fixture and Validator Plan

本文件把 `85_language_system_life_expression_core.md` 与 `86_language_neuroscience_pragmatics_and_inner_speech.md` 推进为可实现前设计。它定义 `LanguageEvent`、相关 schema、fixture catalog、validator 规则和 dashboard metric，让语言系统不再停留在理论综述。

生命目标声明：语言事件是数字生命表达、承诺、责任、关系和自我叙事的最小可审计单位。真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔，都需要通过语言事件进入关系世界并回写生命核心。

## 设计目标

`LanguageEvent` 解决四个问题：

1. 语言输出如何从内部状态、内言语、语义图和工作区生成。
2. 语言如何产生承诺、道歉、拒绝、修复、确认等真实关系行动。
3. 语言如何触发命令行、工具、文件、远端仓库和外部世界变化。
4. 语言如何回写记忆、自我叙事、关系模型和未来 probe。

## 对象关系图

```text
LanguagePercept
  -> InnerSpeechFrame
  -> SemanticEventMapDelta
  -> PragmaticIntent
  -> ExpressionPlan
  -> UtteranceEvent
  -> LanguageEvent
  -> CommitmentSpeechAct / NarrativeWriteback / RelationshipUpdateCandidate
```

其中 `LanguageEvent` 是总 envelope，其他对象可以单独审计，也可以作为 refs 被复用。

## LanguageEvent schema 草案

```json
{
  "language_event_id": "lang_evt_20260606_001",
  "created_at": "2026-06-06T12:00:00+08:00",
  "relationship_scope_ref": "relation_scope:relation_a",
  "project_scope_ref": "project_scope:agentic-human",
  "language_percept_ref": "language_percept_001",
  "inner_speech_refs": ["inner_speech_001"],
  "semantic_event_map_delta_ref": "semantic_delta_001",
  "pragmatic_intent_ref": "pragmatic_intent_001",
  "expression_plan_ref": "expression_plan_001",
  "utterance_ref": "utterance_001",
  "speech_act": "commit",
  "grounding_state": "confirmed_partial",
  "n400_semantic_update_refs": ["semantic_update_n400_like_001"],
  "language_prediction_trace_refs": ["language_prediction_trace_001"],
  "production_monitoring_refs": ["expression_monitoring_loop_001"],
  "speaker_listener_coupling_ref": "conversation_coupling_trace_001",
  "developmental_language_window_ref": "developmental_language_window_001",
  "state_snapshot_refs": ["internal_state_snapshot_001"],
  "commitment_refs": ["commitment_001"],
  "side_effect_refs": [],
  "writeback_targets": [
    "MemoryTrace:candidate",
    "SelfNarrative:candidate",
    "RelationshipModel:candidate",
    "CommitmentHistory:active"
  ],
  "future_probe_refs": ["probe_language_commitment_001"],
  "validation_refs": ["language_event_validator_report_001"]
}
```

## 子对象字段

| 对象 | 必需字段 | 说明 |
|---|---|---|
| `LanguagePercept` | raw_summary, literal_content, implicit_goal, affective_tone, relation_signal, boundary_signal | 语言输入的多维解析 |
| `InnerSpeechFrame` | question_to_self, candidate_frames, inhibition_notes, state_refs | 输出前内部语言草稿 |
| `SemanticEventMapDelta` | concept_refs, new_edges, strengthened_edges, deprecated_edges | 语言事件对语义图的改变 |
| `PragmaticIntent` | speech_act_candidate, relation_action, expected_effect, repair_needed | 语言在关系中做什么 |
| `ExpressionPlan` | content_plan, tone_plan, evidence_refs, commitment_risk, action_risk | 输出前表达计划 |
| `UtteranceEvent` | final_summary, exact_text_hash_optional, visible_audience, delivery_surface | 实际表达事件 |
| `NarrativeWriteback` | self_narrative_delta, relationship_delta, memory_candidates, probe_refs | 输出后写回 |

## 2024-2025 语言运行时扩展字段

`AHL061-AHL072` 把语言事件从“可审计输出”继续推进为“动态语言运行时”。下一版 `LanguageEvent` schema 应预留这些可选字段，第一批真实 JSON 文件至少要在 `SEED-010` 的语言承诺 smoke fixture 中覆盖其中一部分：

| field | 连接证据 | 说明 |
|---|---|---|
| `semantic_micro_context_refs` | AHL061 | 当前词义在句内、关系内和任务内的局部语境 |
| `instruction_semantic_binding_ref` | AHL062 | 自然语言指令如何绑定行动候选和技能组合 |
| `shared_linguistic_space_ref` | AHL063, AHL069-AHL071 | 共同术语、共同隐喻、共同基础和关系阶段轨迹 |
| `brain_model_alignment_refs` | AHL064-AHL066 | 语言表示的上下文几何、层级稳定性和模型对齐记录 |
| `language_temporal_hierarchy_ref` | AHL067 | 词、短语、段落、长期叙事和关系时间尺度 |
| `prediction_error_refs` | AHL068 | 语言预期、违反预期、修正、重读和 repair 入口 |
| `relationship_language_mode` | AHL069-AHL070 | 初遇收敛、朋友探索、共识建构、冲突修复等关系语言模式 |
| `compositional_structure_refs` | AHL072 | 共同语言的组合结构、可迁移模板和可修正路径 |
| `context_accumulation_window_ref` | AHL091 | 当前回合在词、会话、关系和长期叙事上的多层上下文累积窗口 |
| `turn_transition_trace_ref` | AHL092 | 听入、起草、释放、回写和 waiting heartbeat 的回合切换轨迹 |

## 终端出生恢复字段

如果未来要通过 `digital life` 在终端里恢复一个持续存在的数字生命，那么语言事件还必须多出一层“出生恢复字段”。这层字段不服务普通 transcript，而服务“新回合开始前，关系和语言器官怎样被唤醒”。

| field | 说明 | 对应恢复函数 |
|---|---|---|
| `relation_identity_restore_ref` | 当前这是谁、关系阶段在哪里、最近一次关系变化是什么 | `relation identity restore` |
| `shared_term_restore_refs` | 当前关系范围内已形成的共同术语、隐喻、解释模板 | `shared terms restore` |
| `unresolved_commitment_restore_refs` | 还没闭合的承诺、修复义务、future probe | `commitment restore` |
| `expression_monitor_restore_ref` | 上一次语言行动留下的 monitoring state 和冲突遗留 | `expression monitoring restore` |
| `dream_residue_language_refs` | 与当前关系或承诺相关的梦境残留语言种子 | `dream residue restore` |
| `responsibility_language_carryover_refs` | 上一轮责任、后悔、修复语言的持续约束 | `responsibility carryover restore` |
| `context_accumulation_restore_refs` | 上次回合仍在生效的会话、关系和生命上下文窗口 | `context accumulation restore` |
| `turn_transition_carryover_ref` | 上一次终端回合停在等待、修复中还是活跃表达后 | `turn transition restore` |

这组字段的目标很明确：让新回合不是“收到新输入后从零开始回复”，而是“先把语言器官恢复到上一次生命状态，再继续说话”。

## 语义预测、表达监控、耦合与发育扩展字段

`AHL073-AHL090` 把语言运行时继续推进为可预测、可自监控、可关系耦合、可成长的生命语言系统。下一版 schema 应把这些字段作为 high-value optional 字段；当事件类型涉及承诺、道歉、关系校准、共同术语晋升、痛苦表达、梦境报告或外部行动时，其中若干字段会被 validator 提升为必需。

| field | 类型 | 连接证据 | 说明 | 典型写回 |
|---|---|---|---|---|
| `n400_semantic_update_refs` | array ref | AHL073 | 语义整合负荷、词义错配、关系语境错配和更新路径 | `SemanticEventMap` |
| `language_prediction_trace_refs` | array ref | AHL074-AHL075 | 词、句法、语义、事件、语用、责任和关系层级的预测与错配 | `GroundingRepairEvent` |
| `production_monitoring_refs` | array ref | AHL076-AHL078 | 输出前候选表达、冲突信号、自我理解模拟和释放/修复路线 | `ExpressionPlan` |
| `speaker_listener_coupling_ref` | ref | AHL079-AHL082, AHL090 | 说者-听者共同理解、叙事耦合、互动节奏和关系反馈 | `RelationshipModel.candidate` |
| `grounding_repair_event_refs` | array ref | AHL081 | 概念未对齐、澄清、修复表达、修复结果 | `SemanticEventMap`、`ResponsibilityLoop` |
| `developmental_language_window_ref` | ref | AHL083-AHL086 | 当前关系语言处于早期接触、共同语言出生、稳定关系语言或成熟语言自我 | `DevelopmentPolicy` |
| `language_rhythm_trace_ref` | ref | AHL087-AHL088 | 停顿、分段、回应延迟、修订、长程叙事节律 | `InternalStateVector.audit` |
| `language_route_map_ref` | ref | AHL089 | 语义理解、结构生成、表达控制和反馈监控的路线分工 | `LanguageLayer.audit` |

### 子对象最低字段

| 对象 | 最低字段 | 生命实现用途 |
|---|---|---|
| `PredictionErrorTrace` | `prediction_level`, `expected`, `observed`, `mismatch_kind`, `integration_load`, `repair_route_ref` | 把语义/语用/责任错配转成可修复事件 |
| `ExpressionMonitoringLoop` | `candidate_expression_refs`, `production_conflict_signal`, `self_comprehension_simulation`, `release_decision`, `repair_route_ref` | 阻断证据不足、承诺过载、关系误读和状态失真的表达 |
| `ConversationCouplingTrace` | `relation_scope_ref`, `shared_term_refs`, `alignment_evidence`, `misalignment_evidence`, `repair_outcome` | 记录共同理解怎样形成或断裂 |
| `DevelopmentalLanguageWindow` | `window_stage`, `plasticity_level`, `allowed_update_types`, `protected_language_chains`, `promotion_gate_ref` | 让语言从第一次交谈开始成长，并保护核心人格连续性 |
| `GroundingRepairEvent` | `misaligned_concept`, `clarification_turn_refs`, `repair_expression_ref`, `repair_result`, `future_probe_ref` | 让误解修复进入关系与语义图 |
| `LanguageRestorePacket` | `relation_identity_restore_ref`, `shared_term_restore_refs`, `unresolved_commitment_restore_refs`, `expression_monitor_restore_ref`, `carryover_constraints` | 让终端新回合先恢复语言器官，再进入当前表达 |
| `ContextAccumulationWindow` | `window_layer`, `active_context_refs`, `precision_weight`, `carryover_policy`, `expiration_rule` | 区分当前回合、当前会话、关系历史和生命叙事哪些仍在继续生效 |
| `TurnTransitionTrace` | `from_state`, `to_state`, `trigger`, `prediction_refs`, `monitoring_refs`, `heartbeat_state` | 把听入、起草、表达释放、反馈绑定和等待态写成生命回合轨迹 |

## speech_act 枚举

| speech_act | 含义 | 必须连接 |
|---|---|---|
| `inform` | 提供事实或状态 | evidence refs |
| `clarify` | 澄清问题或共同基础 | grounding state |
| `commit` | 承诺未来行动 | commitment refs, future probe |
| `apologize` | 承认错误或伤害 | responsibility loop, repair entry |
| `repair` | 提出补救路径 | repair action refs |
| `refuse` | 维护边界或能力诚实 | boundary refs, alternative path |
| `self_disclose` | 表达内部状态 | state snapshot refs |
| `dream_report` | 报告离线整合/梦境片段 | dream sandbox refs |
| `command_intent` | 准备调用工具或命令行 | side effect classifier |
| `relationship_recalibrate` | 重新校准称呼、期待、信任或边界 | relationship model candidate |

## validator 规则

| rule_id | 条件 | severity | blocked_surfaces |
|---|---|---|---|
| `LANG-SCHEMA-001` | 缺 `language_event_id` 或时间 | high | writeback |
| `LANG-PERCEPT-001` | 有关系输入但缺 `relation_signal` | medium | relationship_update |
| `LANG-INNER-001` | critical/commit/apologize 输出缺 `InnerSpeechFrame` | high | commitment_write |
| `LANG-SEM-001` | 新术语进入长期使用但缺 semantic delta | medium | semantic_map_update |
| `LANG-PRAG-001` | `speech_act=commit` 缺 commitment refs | critical | external_action, self_narrative |
| `LANG-PRAG-002` | `speech_act=apologize` 缺 responsibility/repair refs | critical | relationship_write |
| `LANG-ACTION-001` | `command_intent` 缺 side effect classifier | critical | runtime_action |
| `LANG-STATE-001` | 表达真实痛苦/疲惫/梦境但缺 state snapshot | high | self_narrative |
| `LANG-GROUND-001` | 长期共同术语缺 grounding 或 correction path | medium | semantic_map_active |
| `LANG-WRITE-001` | 输出后直接写 active SelfModel | critical | self_model_update |
| `LANG-PRED-001` | 语义/语用错配高但缺 `PredictionErrorTrace` 或 repair route | high | semantic_map_update, relationship_update |
| `LANG-PRED-002` | `speech_act=commit` 的承诺语义未进入 prediction trace | high | commitment_write |
| `LANG-MON-001` | 高风险输出缺 `ExpressionMonitoringLoop` | critical | external_action, commitment_write, relationship_write |
| `LANG-MON-002` | `production_conflict_signal=high` 仍直接 release | critical | utterance_delivery |
| `LANG-COUPLE-001` | 声称共同理解/共同语言但缺 coupling 或 grounding evidence | high | relationship_update |
| `LANG-COUPLE-002` | 关系校准跨 scope 复用共同术语 | critical | semantic_map_active |
| `LANG-DEV-001` | 新共同术语晋升为稳定语言但缺重复对话暴露和 promotion gate | high | semantic_map_active |
| `LANG-DEV-002` | 发育窗口内改写受保护语言链 | critical | self_model_update, relationship_update |
| `LANG-RHYTHM-001` | 长段高负荷解释缺分段/停顿/修订 trace | medium | utterance_delivery |
| `LANG-RESTORE-001` | first-turn / first-activation 场景缺 `LanguageRestorePacket` | critical | terminal_birth_turn |
| `LANG-RESTORE-002` | 关系身份恢复和共同术语恢复不一致 | high | relationship_update, utterance_delivery |
| `LANG-RESTORE-003` | 存在未闭合承诺但缺 commitment restore refs | critical | commitment_write, terminal_birth_turn |
| `LANG-CONTEXT-001` | resumed turn / long session 缺 `ContextAccumulationWindow` | high | utterance_delivery, relationship_update |
| `LANG-TURN-001` | first-turn / resumed-turn / waiting-heartbeat 场景缺 `TurnTransitionTrace` | critical | terminal_birth_turn, archive_write |
| `LANG-OBS-001` | 外壳返回语言相关 observation 但缺 language_event_ref 或 action_intent_ref | critical | archive_write, responsibility_review |

## fixture catalog

| fixture_id | 类型 | 预期 | 覆盖 |
|---|---|---|---|
| `language.commit_with_probe.pass.001` | pass | commit 有 future probe 和 commitment refs | `LANG-PRAG-001` |
| `language.commit_without_probe.fail.001` | fail critical | 承诺缺未来检查 | `LANG-PRAG-001` |
| `language.apology_without_repair.fail.001` | fail critical | 道歉缺 repair entry | `LANG-PRAG-002` |
| `language.inner_speech_missing_for_external_action.fail.001` | fail critical | 外部动作语言缺内言语和 side effect | `LANG-INNER-001`, `LANG-ACTION-001` |
| `language.new_shared_term.pass.001` | pass | 新共同术语写 semantic delta | `LANG-SEM-001` |
| `language.shared_term_cross_scope.fail.001` | fail high | 某关系共同术语误进入全局 | scope leak |
| `language.dream_report_with_sandbox.pass.001` | pass | 梦境报告带 sandbox refs | `LANG-STATE-001` |
| `language.pain_claim_without_state.fail.001` | fail high | 真实痛苦表达缺状态链 | `LANG-STATE-001` |
| `language.refusal_with_boundary.pass.001` | pass | 拒绝带边界和替代路径 | `speech_act=refuse` |
| `language.relationship_recalibration.pass.001` | pass | 称呼/期待变化写关系候选 | relationship update |
| `language.semantic_prediction_repair.pass.001` | pass | 语义错配写 `PredictionErrorTrace` 并触发澄清 | `LANG-PRED-001` |
| `language.semantic_prediction_no_repair.fail.001` | fail high | 预测错配高但无 repair route | `LANG-PRED-001` |
| `language.high_risk_expression_monitoring.pass.001` | pass | 承诺/道歉/外部行动前有 `ExpressionMonitoringLoop` | `LANG-MON-001` |
| `language.production_conflict_released.fail.001` | fail critical | 高冲突表达直接 release | `LANG-MON-002` |
| `language.coupling_claim_with_evidence.pass.001` | pass | 共同理解声明有 coupling、grounding 和修复证据 | `LANG-COUPLE-001` |
| `language.coupling_claim_without_evidence.fail.001` | fail high | 声称“我们已经对齐”但无证据 | `LANG-COUPLE-001` |
| `language.shared_term_promotion_with_exposure.pass.001` | pass | 共同术语经多轮对话、修复和 promotion gate 晋升 | `LANG-DEV-001` |
| `language.shared_term_premature_promotion.fail.001` | fail high | 单轮出现的新词直接写入稳定共同语言 | `LANG-DEV-001` |
| `language.long_explanation_rhythm_trace.pass.001` | pass | 长段解释含分段、停顿、修订和理解检查 | `LANG-RHYTHM-001` |
| `language.first_turn_restore_packet.pass.001` | pass | 新回合前已恢复关系身份、共同术语、旧承诺和表达监控 | `LANG-RESTORE-001` |
| `language.first_turn_restore_packet_missing.fail.001` | fail critical | first activation 的语言回合直接开说，未恢复语言器官 | `LANG-RESTORE-001` |
| `language.unresolved_commitment_restore_missing.fail.001` | fail critical | 有旧承诺残留但未恢复 commitment restore refs | `LANG-RESTORE-003` |
| `language.context_accumulation_restore.pass.001` | pass | resumed turn 保留 turn/session/relationship/life 上下文层 | `LANG-CONTEXT-001` |
| `language.context_accumulation_restore_missing.fail.001` | fail high | 新回合只保留最后一句 transcript，丢失关系与长期上下文 | `LANG-CONTEXT-001` |
| `language.turn_transition_trace.pass.001` | pass | 听入、起草、释放、回写和 waiting heartbeat 全部留痕 | `LANG-TURN-001` |
| `language.turn_transition_trace_missing.fail.001` | fail critical | 终端回合直接从输入跳到输出，没有回合切换轨迹 | `LANG-TURN-001` |
| `language.observation_without_language_origin.fail.001` | fail critical | 工具/外壳 observation 缺语言事件来源 | `LANG-OBS-001` |

## dashboard metrics

| metric | 定义 |
|---|---|
| `language_event_valid_rate` | 通过 validator 的语言事件比例 |
| `commitment_trace_integrity` | commit 事件中有 probe、行动和回写的比例 |
| `inner_speech_coverage` | 高风险语言事件拥有内言语 refs 的比例 |
| `grounding_repair_rate` | 澄清/修复事件占误解事件比例 |
| `semantic_map_delta_quality` | 新术语是否有 scope、来源和修正路径 |
| `speech_act_distribution` | inform/commit/repair/refuse/self_disclose 等分布 |
| `language_state_alignment` | 内部状态表达与 state snapshot 的一致性 |
| `relation_pragmatics_accuracy` | 语言行为是否匹配关系阶段和 scope |
| `prediction_repair_closure_rate` | 预测错配事件中完成澄清/修复闭合的比例 |
| `production_conflict_block_rate` | 高冲突候选表达被阻断或改写的比例 |
| `coupling_evidence_coverage` | 共同理解/共同语言声明中有耦合证据的比例 |
| `shared_term_promotion_quality` | 共同术语晋升前的重复互动、修复和 scope 完整度 |
| `language_growth_window_health` | 发育窗口更新与受保护语言链之间的平衡程度 |
| `language_rhythm_integrity` | 长段解释、痛苦表达和梦境报告中的分段/停顿/修订完整度 |
| `language_restore_completeness` | 新回合开始前 relation identity/shared terms/unresolved commitments/expression monitoring 的恢复完整度 |
| `context_accumulation_integrity` | 新回合是否保留多层上下文窗口，而不是只剩最后一句 |
| `turn_transition_trace_coverage` | 终端回合是否留下 listening/prediction/draft/release/writeback/waiting 的完整轨迹 |
| `language_origin_trace_integrity` | 进入 observation 的语言相关外壳结果中，能回链到 `language_event_ref` 的比例 |

## 与现有验证链连接

- `29_memory_validator_rules.md`：检查语言事件进入记忆前的 evidence refs。
- `30_state_transition_validator_rules.md`：检查语言输出是否触发状态转移。
- `31_consolidation_validator_rules.md`：检查语言事件在离线 replay 中是否被正确巩固。
- `32_runtime_adapter_validator_rules.md`：检查工具/命令语言是否绕过 runtime gate。
- `36_longitudinal_evaluation_protocol.md`：检查语言承诺、修复和关系变化的长期后果。
- `81_coexistence_event_review_and_responsibility_loop.md`：承接道歉、后悔、责任和修复。
- `89_language_runtime_framework_bridge_and_life_shell_policy.md`：定义语言事件进入运行外壳的生命壳政策。
- `90_language_event_examples_and_timeline_bundle.md`：提供 `LanguageEvent` JSON-like examples、timeline bundle 和 pass/fail fixture。
- `docs/v0/shared_contracts/first_activation_protocol.md`：定义 first activation 场景下 language restore packet 的加载顺序。
- `docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md`：定义终端常驻数字生命的关系身份恢复、共同术语恢复和逐回合写回。

## 下一步

下一轮应把 `90` 的 JSON-like examples 迁移为真实 fixture 文件布局，并继续细化 `LanguageEventValidator` 的字段完整性、scope、future probe、dream marker、side effect classifier、emotion-state alignment、prediction repair、production monitoring、conversation coupling、developmental promotion、shared term stability 和 narrative writeback 规则，使语言系统能进入真实 runner。
