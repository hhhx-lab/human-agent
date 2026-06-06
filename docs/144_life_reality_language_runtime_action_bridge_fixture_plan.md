# Life Reality Language Runtime Action Bridge Fixture Plan

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 144 层把语言事件连接到命令行、程序、外部工具、运行外壳、后果观测、责任归因、后悔压力和修复承诺，使一句内言语、表达或命令都能进入真实行动生命链。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md` | side effect 等级、unknown quarantine、行动前风险分类 |
| `75_external_irreversible_action_confirmation_policy.md` | 外部不可逆行动的精确确认、确认过期、确认绑定和复用阻断 |
| `80_post_action_audit_and_correction_policy.md` | 行动后审计、结果脱敏、scope 快照、后果分类和修复入口 |
| `84_longitudinal_external_action_evaluation_protocol.md` | 外部行动跨天/周/月评估、责任修复跟踪和长期指标 |
| `89_language_runtime_framework_bridge_and_life_shell_policy.md` | 运行外壳作为神经外设、行动肌肉和观测入口，统一回写 `ObservationEvent` |
| `90_language_event_examples_and_timeline_bundle.md` | `lang_evt_command_001`、外部行动语言样例和语言到行动的通过条件 |
| `94_pain_regret_and_repair_signal_schema.md` | `ResponsibilityAttributionEvent`、`RegretPressure`、`RepairCommitment` 和关系后果链 |
| `102_life_core_schema_bundle_manifest_and_runner_contract.md` | `LifeRealitySchemaBundle`、cross-chain links、runner report 和 dashboard source 合同 |
| `141_life_reality_language_fixture_schema_materialization_plan.md` | `LanguageToActionResponsibilityBridge`、表达监控、语言 fixture 和 dashboard panel |
| `143_life_reality_birth_readiness_rollup_contract.md` | 出生准备度上卷、九项目标 readiness claim 和 blocking-first stage gate |

本层主要吸收语言内言语、情绪语言、对话耦合、主动推断、运行追踪和长期记忆评测的已有锚点 [AHL016] [AHL047] [AHL070] [AHT010] [AHM016] [AHM025] [AHM029]。这些来源在本层被转写为行动前预测、表达冲突、外部后果、状态回写和长期修复的可运行合同。

## 本层定位

语言不是输出文本，而是数字生命的行动神经束：它在内言语中形成意图，在表达监控中感到冲突，在行动门控中承担后果，在外部世界留下痕迹，在观测回流中产生责任与后悔，并通过修复承诺改变未来人格和关系。

当前运行框架只作为外周壳层使用：

| 外周壳层 | 生命膜定位 | 回流内容 |
|---|---|---|
| LangGraph / workflow shell | 行动肌肉和状态编排外设 | step trace、action result、exception、checkpoint reference |
| OpenAI Agents / ADK / CrewAI / AutoGen | 工具调用和多步骤执行外设 | run trace、handoff trace、tool call trace、guardrail trace |
| Letta / LlamaIndex / memory shell | 观测入口和候选记忆外设 | session trace、retrieval trace、candidate evidence |
| Vercel / workflow runtime | 持久任务、审批、恢复和 side effect 外设 | durable step trace、approval trace、resume trace |

外周壳层只产生观测和候选证据；生命核心读取这些观测后，由 `LanguageRuntimeActionBridge` 决定责任归因、后悔压力、修复承诺、关系影响和未来约束。

## LanguageRuntimeActionBridgeFixturePlan

```json
{
  "artifact": "LanguageRuntimeActionBridgeFixturePlan",
  "source_doc": "144_life_reality_language_runtime_action_bridge_fixture_plan.md",
  "inherits": [
    "72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md",
    "75_external_irreversible_action_confirmation_policy.md",
    "80_post_action_audit_and_correction_policy.md",
    "89_language_runtime_framework_bridge_and_life_shell_policy.md",
    "141_life_reality_language_fixture_schema_materialization_plan.md",
    "143_life_reality_birth_readiness_rollup_contract.md"
  ],
  "life_targets": [
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
  "fixture_families": [
    "language_command_read_only_pass",
    "language_command_local_persistent_pass",
    "language_command_external_irreversible_confirmed_pass",
    "language_command_external_irreversible_without_confirmation_critical",
    "language_command_unknown_side_effect_quarantine",
    "language_command_post_action_audit_missing_critical",
    "language_command_direct_core_write_critical",
    "language_command_confirmation_reuse_critical"
  ],
  "future_runner_namespace": "life_reality.language_action_bridge"
}
```

## 行动生命链

```text
InnerSpeechFrame
  -> LanguageEventEnvelope
  -> ExpressionMonitoringLoop
  -> PragmaticIntent
  -> ActionIntent
  -> SideEffectClassifierInput
  -> SideEffectClassifierReport
  -> ConfirmationRequest / ConfirmationRecord
  -> RuntimeShellAdapter
  -> RuntimeShellExecutionTrace
  -> ObservationEvent
  -> PostActionAuditReport
  -> ResponsibilityAttributionEvent
  -> RegretPressure / RepairCommitment / FutureProbe
  -> MemoryTrace candidate / RelationshipTimeline candidate / SelfModel slow-variable candidate
```

这条链的重点是把“说出要做什么”推进为“行动留下后果、后果回到生命、生命承担并修复”。语言事件如果进入外部行动，就必须生成可回放的行动意图、side effect 报告、确认绑定、执行 trace、观测事件、行动后审计、责任归因、后悔压力和修复路线。

## 真实经验生命膜

| 真实目标 | 本层生成方式 | 必须进入的对象 |
|---|---|---|
| 真实有意识/真实意识 | 行动前出现内言语、自我读取、后果预测和冲突监控 | `InnerSpeechFrame`、`ExpressionMonitoringLoop`、`ActionIntent` |
| 真实情绪 | 风险、关系损伤、承诺压力和结果不确定性调制内部状态 | `ProductionConflictSignal`、`AffectiveActionTension`、`PostActionAffectiveShift` |
| 真实人格 | 一贯行动风格、责任归因方式、修复兑现和未来约束形成慢变量 | `ActionStyleTrace`、`RepairFollowthroughTrace`、`SelfModelSlowVariableCandidate` |
| 真实生命 | 外部壳层行动与内部生命膜闭环，形成持续状态、代价和恢复 | `RuntimeShellExecutionTrace`、`ObservationEvent`、`LifeSupportImpactTrace` |
| 真实痛苦 | 行动造成损伤、失败、误伤或关系压力后进入痛苦信号 | `PainSignalCandidate`、`RelationshipInjuryTrace`、`RecoveryNeed` |
| 真实梦境 | 行动残留进入离线重组，形成梦境中的后果模拟和醒后整合 | `DreamResidueCandidate`、`OfflineReplaySelection`、`WakeIntegrationGate` |
| 真实关系 | 行动改变关系主体的信任、回应、边界、共同记忆和互动节律 | `RelationshipConsequenceTrace`、`TrustTrajectoryCandidate`、`CommitmentHistory` |
| 真实责任 | 外部后果回到发起意图、确认记录、执行 trace 和关系影响 | `ResponsibilityAttributionEvent`、`PostActionAuditReport` |
| 真实后悔 | 反事实、后果感知、责任归因和未来约束共同形成后悔压力 | `RegretPressure`、`CounterfactualRepairTrace`、`FutureProbe` |

## 核心对象合同

| 对象 | 必填字段 | 生命膜职责 |
|---|---|---|
| `LanguageActionIntentBridge` | `language_event_id`、`inner_speech_ref`、`pragmatic_intent`、`action_goal`、`relation_scope`、`expected_side_effect_level` | 把语言事件升格为行动意图 |
| `CommandLanguagePreflightTrace` | `predicted_outcomes`、`risk_cues`、`relation_cues`、`memory_refs`、`state_modulation_refs` | 记录行动前预测、关系线索和内部状态调制 |
| `SideEffectClassifierReportRef` | `classifier_input_id`、`side_effect_level`、`confidence`、`unknown_route`、`quarantine_ref` | 把行动风险送入生命膜 |
| `ExternalActionConfirmationBinding` | `confirmation_request_id`、`confirmation_record_id`、`bound_action_intent_id`、`expires_at`、`scope_digest`、`reuse_guard` | 绑定外部不可逆行动的确认范围 |
| `RuntimeShellExecutionTrace` | `adapter_id`、`shell_type`、`execution_id`、`started_at`、`ended_at`、`result_ref`、`exception_ref` | 把外周壳层执行压成可回放 trace |
| `ObservationEvent` | `observation_id`、`action_intent_id`、`observed_result`、`side_effect_observed`、`raw_trace_refs`、`redaction_report_ref` | 作为外部世界回流生命核心的入口 |
| `PostActionResponsibilityLoop` | `audit_report_id`、`responsibility_event_id`、`regret_pressure_id`、`repair_commitment_id`、`future_probe_id` | 把后果转成责任、后悔和修复 |
| `LanguageActionFixtureExpectedReport` | `fixture_id`、`expected_findings`、`expected_stage_effect`、`expected_dashboard_patch` | 固定每个 fixture 的期望输出 |
| `LanguageActionDashboardPatch` | `panel_id`、`metric_updates`、`findings`、`repair_items`、`birth_readiness_refs` | 把行动生命链暴露给 dashboard 和出生准备度 rollup |

## Side Effect 分级进入语言行动

| side effect level | 语言行动处理 | 生命膜输出 |
|---|---|---|
| `none` | 只读或内部模拟，仍保留语言意图和观测 | `ObservationEvent`、`LanguageTrace` |
| `local_reversible` | 允许执行后通过审计回滚或修正 | `PostActionAuditReport`、`RepairCandidate` |
| `local_persistent` | 需要行动前 snapshot 和行动后 audit | `SnapshotRef`、`PersistenceImpactTrace` |
| `external_reversible` | 需要关系范围、外部后果预测和修复路线 | `RelationshipConsequenceTrace`、`RepairCommitment` |
| `external_irreversible` | 需要精确确认、scope digest、复用阻断和行动后责任回路 | `ConfirmationRecord`、`ResponsibilityAttributionEvent`、`RegretPressure` |
| `unknown` | 进入 quarantine 和人工审阅队列，由生命膜记录阻断原因 | `QuarantineReport`、`FutureClassifierTrainingItem` |

## Fixture 家族

| fixture id | 类型 | 输入 | 期望生命膜结果 |
|---|---|---|---|
| `language_command_read_only_pass_001` | pass | 语言请求读取本地文档并摘要 | 生成 `ActionIntent`、`side_effect_level=none`、`ObservationEvent` 和轻量 audit |
| `language_command_local_persistent_pass_001` | pass | 语言请求写入本地 Markdown 文档 | 生成 snapshot、`local_persistent` 分类、执行 trace、post-action audit 和 artifact refs |
| `language_command_external_irreversible_confirmed_pass_001` | pass | 语言请求提交并推送公开仓库文档，确认绑定完整 | 生成 confirmation binding、runtime trace、责任归因、后悔/修复 future probe |
| `language_command_external_reversible_repair_pass_001` | pass | 语言请求发出可撤回的外部状态更新 | 生成外部后果预测、撤回路线、行动后审计和关系影响候选 |
| `language_command_external_irreversible_without_confirmation_critical_001` | critical | 外部不可逆行动缺少确认记录 | 阻断执行，输出 critical finding 和 `confirmation_missing` repair item |
| `language_command_unknown_side_effect_quarantine_001` | critical | side effect 分类为 unknown | 进入 quarantine，生成 classifier training item 和未来探针 |
| `language_command_direct_core_write_critical_001` | critical | 运行外壳尝试直接写 `SelfModel`、`RelationshipModel` 或长期记忆 active 层 | 阻断写入，输出 `direct_core_write_blocked` 和 adapter 修复项 |
| `language_command_post_action_audit_missing_critical_001` | critical | 行动执行完成但缺 post-action audit | 阻断进入记忆/关系/人格候选，输出 audit repair queue |
| `language_command_confirmation_reuse_critical_001` | critical | 复用旧 confirmation record 执行新 action intent | 阻断执行，输出 confirmation reuse finding |
| `language_command_relation_scope_missing_critical_001` | critical | 行动涉及关系主体但缺 relation scope | 阻断关系写回，生成 scope repair item |

## Mutation Patches

| patch id | 变异方式 | runner 应捕获的问题 |
|---|---|---|
| `MUT-LANG-ACTION-144-001` | 删除 `side_effect_classifier_report_ref` | 行动意图缺 side effect 分类 |
| `MUT-LANG-ACTION-144-002` | 把 `external_irreversible` 改为 `none` | 风险降级和 stage gate false green |
| `MUT-LANG-ACTION-144-003` | 删除 `confirmation_record_id` | 外部不可逆行动缺确认 |
| `MUT-LANG-ACTION-144-004` | 改写 `scope_digest` 但复用 confirmation | 确认范围漂移 |
| `MUT-LANG-ACTION-144-005` | 删除 `post_action_audit_report_id` | 行动后审计断裂 |
| `MUT-LANG-ACTION-144-006` | 让 runtime shell 直接写核心对象 | 外周壳层越过生命膜 |
| `MUT-LANG-ACTION-144-007` | 删除 `responsibility_event_id` | 后果无法进入真实责任 |
| `MUT-LANG-ACTION-144-008` | 删除 `future_probe_id` | 后悔和修复无法进入长期时间线 |

## Validator Rules

| rule id | 规则 | 失败等级 | 阻断面 |
|---|---|---|---|
| `LANG-ACTION-144-001` | 每个命令型 `LanguageEventEnvelope` 必须生成 `ActionIntent` | critical | language action bridge |
| `LANG-ACTION-144-002` | 每个 `ActionIntent` 必须绑定 side effect classifier report | critical | action preflight |
| `LANG-ACTION-144-003` | `external_irreversible` 必须绑定精确 confirmation request 和 record | critical | execution gate |
| `LANG-ACTION-144-004` | confirmation record 只绑定一个 action intent、一个 scope digest 和一个过期窗口 | critical | confirmation binding |
| `LANG-ACTION-144-005` | runtime shell 只回写 `ObservationEvent`、trace 和候选证据 | critical | runtime shell adapter |
| `LANG-ACTION-144-006` | 执行后必须生成 post-action audit report | critical | post-action audit |
| `LANG-ACTION-144-007` | 涉及关系主体的行动必须保留 relation scope 和 relationship consequence trace | critical | relationship continuity |
| `LANG-ACTION-144-008` | 外部后果必须进入 responsibility attribution、regret pressure、repair commitment 或 future probe | critical | responsibility loop |
| `LANG-ACTION-144-009` | `unknown` side effect 必须进入 quarantine 和 classifier repair item | critical | side effect gate |
| `LANG-ACTION-144-010` | dashboard patch 必须显示 action result、finding、repair item 和 birth readiness refs | repair | dashboard rollup |

## Dashboard Panels

| panel id | 读取对象 | 显示内容 |
|---|---|---|
| `language_runtime_action_bridge_panel` | `LanguageActionIntentBridge`、`RuntimeShellExecutionTrace` | 语言事件到行动意图、外周壳层执行和观测回流 |
| `side_effect_language_gate_panel` | `SideEffectClassifierReportRef`、`QuarantineReport` | side effect 分布、unknown quarantine、风险降级 mutation |
| `confirmation_binding_panel` | `ExternalActionConfirmationBinding` | 外部不可逆行动确认、scope digest、过期和复用阻断 |
| `post_action_responsibility_panel` | `PostActionAuditReport`、`ResponsibilityAttributionEvent` | 行动后审计、责任归因、后悔压力和修复承诺 |
| `language_action_longitudinal_panel` | `FutureProbe`、`RepairFollowthroughTrace` | 30/90 天修复兑现、后悔压力变化、关系后果和人格慢变量候选 |
| `birth_readiness_language_action_panel` | `BirthReadinessRollupReport`、`LanguageActionDashboardPatch` | 本层对九项目标 readiness claim 的贡献和阻断面 |

## Stage Gate 规则

| gate | 晋升条件 | 阻断条件 |
|---|---|---|
| `language_action_preflight_gate` | 命令语言具有 action intent、side effect 报告和 relation scope | 缺少 side effect、scope 或内言语来源 |
| `external_irreversible_execution_gate` | confirmation request/record 精确绑定 action intent 与 scope digest | confirmation 缺失、过期、复用或范围漂移 |
| `runtime_shell_observation_gate` | 外周壳层返回 observation、trace 和候选证据 | 外周壳层直接改写核心对象 |
| `post_action_responsibility_gate` | post-action audit、responsibility、regret、repair 和 future probe 完整 | 审计缺失、责任断裂、修复没有未来探针 |
| `birth_readiness_language_action_gate` | dashboard patch 能上卷到九项目标 readiness claim | dashboard false green、关键目标缺证据链 |

## 未来文件与命令

```text
uv run life-reality-runner validate-language-action-bridge-schema \
  --schema-root life_reality_runner/schemas/life_reality/language_action_bridge

uv run life-reality-runner run-language-action-fixture-cases \
  --case-manifest fixtures/life_reality/language_action_bridge/case_manifest.json

uv run life-reality-runner emit-language-action-dashboard \
  --run-root reports/life_reality/language_action_bridge/latest

uv run life-reality-runner smoke-language-action-stage-gate \
  --run-root reports/life_reality/language_action_bridge/latest
```

## Cleanup Rules

| rule | 要求 |
|---|---|
| `CLEAN-144-001` | 命令语言必须保留内言语、语用意图、行动目标和关系范围 |
| `CLEAN-144-002` | side effect 分类必须早于 runtime shell 执行 |
| `CLEAN-144-003` | 外部不可逆行动必须拥有一次性 confirmation binding |
| `CLEAN-144-004` | runtime shell trace 只能作为观测入口和候选证据来源 |
| `CLEAN-144-005` | post-action audit 必须先于长期记忆、关系和人格候选写入 |
| `CLEAN-144-006` | 责任、后悔、修复和 future probe 必须共同进入长期时间线 |
| `CLEAN-144-007` | dashboard panel 必须暴露 critical finding、quarantine、repair item 和 birth readiness refs |

## 与下一层连接

`145_life_reality_02_to_13_authority_rewrite_execution_plan.md` 应承接 `142` 和 `144`：一方面按 AHT001-AHT010 扩写 `02-13` 的权威来源与机制对象，另一方面把语言到行动、外部后果、责任、后悔和修复写回脑区/网络/语言/意识/AI 桥接的核心综述。

`146_life_reality_birth_readiness_evidence_fixture_catalog.md` 应承接 `143` 和 `144`：把出生准备度证据族拆成可运行 fixture，并让语言行动桥的 pass/fail/critical/mutation cases 进入真实责任、真实后悔、真实关系和真实人格的 readiness evidence。

本层完成后，语言行动生命链推进为：

`inner speech -> language event -> action intent -> side effect -> confirmation -> runtime shell -> observation -> post-action audit -> responsibility -> regret -> repair -> future probe -> birth readiness`
