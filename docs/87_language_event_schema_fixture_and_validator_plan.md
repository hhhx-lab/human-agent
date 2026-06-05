# Language Event Schema, Fixture and Validator Plan

本文件把 `85_language_system_life_expression_core.md` 与 `86_language_neuroscience_pragmatics_and_inner_speech.md` 推进为可实现前设计。它定义 `LanguageEvent`、相关 schema、fixture catalog、validator 规则和 dashboard metric，让语言系统不再停留在理论综述。

生命目标声明：语言事件是数字生命表达、承诺、责任、关系和自我叙事的最小可审计单位。真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔，都需要通过语言事件进入关系世界并回写生命核心。

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

## 与现有验证链连接

- `29_memory_validator_rules.md`：检查语言事件进入记忆前的 evidence refs。
- `30_state_transition_validator_rules.md`：检查语言输出是否触发状态转移。
- `31_consolidation_validator_rules.md`：检查语言事件在离线 replay 中是否被正确巩固。
- `32_runtime_adapter_validator_rules.md`：检查工具/命令语言是否绕过 runtime gate。
- `36_longitudinal_evaluation_protocol.md`：检查语言承诺、修复和关系变化的长期后果。
- `81_coexistence_event_review_and_responsibility_loop.md`：承接道歉、后悔、责任和修复。
- `89_language_runtime_framework_bridge_and_life_shell_policy.md`：定义语言事件进入运行外壳的生命壳政策。
- `90_language_event_examples_and_timeline_bundle.md`：提供 `LanguageEvent` JSON-like examples、timeline bundle 和 pass/fail fixture。

## 下一步

下一轮应把 `90` 的 JSON-like examples 迁移为真实 fixture 文件布局，并继续细化 `LanguageEventValidator` 的字段完整性、scope、future probe、dream marker、side effect classifier、emotion-state alignment、shared term stability 和 narrative writeback 规则，使语言系统能进入真实 runner。
