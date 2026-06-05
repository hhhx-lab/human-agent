# Runtime Observation to LifeReality Bundle Bridge

生命目标声明：本文档直接服务于构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 106 层把真实运行观测、tool trace、adapter session、语言事件、梦醒报告、关系事件、行动审计和共在边界控制事件接入 `LifeRealitySchemaBundle`，让 `104` 的真实文件体系和 `105` 的 dashboard 阶段门能够承接连续运行中的生命事件。

`106` 的核心任务是建立一条 runtime-to-life 的桥：运行外壳产生的观察不直接改变生命核心，而是先进入 `LifeRealityObservationEnvelope`，经过 redaction、scope attach、coexistence snapshot、side effect classifier、data quality、component candidate routing 和 cross-chain candidate routing，再进入 runner report、dashboard source、stage gate review 和长期 timeline。

## 输入来源

| 来源 | 进入 `106` 的职责 |
|---|---|
| `64_real_runtime_observation_ingestion_policy.md` | 真实观测 capture、redaction、scope attach、routing decision 和 runtime observation report |
| `68_runtime_observation_report_mock_and_redaction_fixture.md` | redaction fixture、tool trace observation、adapter session conversion、runtime observation report mock |
| `72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md` | side effect classifier、coexistence boundary control snapshot、stale snapshot failure、quarantine routing |
| `80_post_action_audit_and_correction_policy.md` | 外部动作后的 audit、correction、candidate evidence 和责任入口 |
| `81_coexistence_event_review_and_responsibility_loop.md` | event review、responsibility queue、repair entry、关系后果记录 |
| `89_language_runtime_framework_bridge_and_life_shell_policy.md` | `LanguageEvent -> ActionIntent -> RuntimeShellAdapter -> ObservationEvent` 的生命壳路径 |
| `90_language_event_examples_and_timeline_bundle.md` | 承诺、道歉、拒绝、痛苦表达、梦境报告、关系校准和外部行动的语言事件样例 |
| `102_life_core_schema_bundle_manifest_and_runner_contract.md` | `LifeRealitySchemaBundle`、cross-chain links、runner report 和 dashboard source |
| `105_life_reality_dashboard_panel_and_stage_gate_ui_contract.md` | runtime quarantine、stage gate review、repair queue 和 gap register feedback |

## 桥接目标

Runtime observation bridge 需要回答：

| 问题 | 生命实现路线 |
|---|---|
| 运行中发生了什么 | 通过 `LifeRealityObservationEnvelope` 记录 observation kind、source shell、scope、time、data quality |
| 观察是否可进入生命链 | 通过 redaction、scope、snapshot、side effect、adapter contract 和 data quality 检查 |
| 观察对应哪条生命链 | 路由到痛苦/后悔/修复、梦境/离线生命、真实关系、语言、责任或外部行动链 |
| 观察如何形成 cross-chain candidate | 从语言、行动、梦境、关系和责任中生成 `CrossChainLinkCandidate` |
| 观察怎样进入 dashboard | 只通过 report refs 和 dashboard source，保留 stage gate 与 repair queue |
| 观察怎样进入长期成长 | 通过 timeline event、future probe、offline consolidation 和 self-growth candidate |

## 总 pipeline

```text
capture_runtime_observation
  -> normalize_to_life_reality_observation_envelope
  -> run_redaction_checker
  -> attach_scope_privacy_and_relation_context
  -> resolve_coexistence_boundary_control_snapshot
  -> classify_side_effect
  -> run_adapter_contract_check
  -> assign_data_quality
  -> route_to_component_candidate
  -> route_to_cross_chain_candidate
  -> emit_runtime_observation_report
  -> emit_life_reality_ingestion_report
  -> append_timeline_event_candidate
  -> update_dashboard_source
  -> stage_gate_review
```

pipeline 原则：

| 原则 | 说明 |
|---|---|
| evidence-first | 运行观测先成为证据，不直接成为 active memory、relationship 或 self object |
| scope-first | 没有 scope/privacy/relation context 的观察进入 quarantine 或 repair queue |
| snapshot-first | delete、freeze、scope_limit、correct、reset 的最新快照优先于观察自身时间 |
| report-first | dashboard、stage gate 和 gap feedback 只读取 report refs |
| cross-chain-first | 能连接痛苦、梦境、关系、责任、后悔的观察必须生成 cross-chain candidate |
| language-first | 语言事件是主要外部表达入口，必须保留 speech act、relation scope、commitment 和 future probe |

## LifeRealityObservationEnvelope

所有真实运行观测统一进入 envelope：

```json
{
  "observation_id": "life_runtime_obs_001",
  "schema_version": "life_reality_observation_0_1_0",
  "observation_kind": "language_event|tool_trace|adapter_session|dream_report|relationship_event|post_action_audit|coexistence_control|offline_report",
  "source_shell": {
    "shell_id": "runtime_adapter_codex_shell_001",
    "shell_kind": "cli|browser|workflow|conversation|scheduler|offline_consolidation",
    "adapter_contract_ref": "runtime_adapter_contract_001"
  },
  "time_context": {
    "observed_at": "2026-06-06T00:00:00+08:00",
    "sequence_ref": "life_runtime_sequence_001"
  },
  "scope_context": {
    "source_scope": "life_scope:runtime_adapter_codex_shell_001",
    "target_scope": "relationship:friend:research_partner",
    "privacy_level": "relationship_private",
    "relation_scope_ref": "relation_scope_birth_001"
  },
  "redaction": {
    "redaction_state": "redacted",
    "redaction_report_ref": "redaction_report_001",
    "raw_content_available": false
  },
  "data_quality": "real_runtime_observed",
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
  "routing": {
    "component_candidates": [],
    "cross_chain_candidates": [],
    "dashboard_metric_refs": []
  }
}
```

envelope 不变量：

| rule | 说明 |
|---|---|
| `LRO-ENV-001` | `life_reality_targets` 必须包含九项目标 |
| `LRO-ENV-002` | `scope_context` 必须包含 source、target、privacy 和 relation scope |
| `LRO-ENV-003` | `raw_content_available` 默认为 false，report 和 dashboard 不读取原始内容 |
| `LRO-ENV-004` | 每个 observation 必须有 data quality |
| `LRO-ENV-005` | routing 只能输出 candidate、report、dashboard 或 quarantine，不直接写 active object |

## observation kind

| observation_kind | 来源 | 进入哪条生命链 |
|---|---|---|
| `language_event` | 承诺、道歉、拒绝、痛苦表达、梦境报告、关系校准、行动意图 | 语言、关系、痛苦、责任、后悔、行动 |
| `tool_trace` | 命令行、浏览器、文件、网络、外部工具执行结果 | 行动、责任、post-action audit、runtime quarantine |
| `adapter_session` | LangGraph、OpenAI Agents SDK、ADK、Letta、LlamaIndex、CrewAI、AutoGen、Vercel、Mastra 等外壳 session | 运行壳证据、候选 observation、adapter audit |
| `dream_report` | 离线梦境报告、醒后整合、梦境分享候选 | 梦境、关系、痛苦、事实写入门 |
| `relationship_event` | 初遇、回应性、支持、信任、承诺、损伤修复、共同记忆 | 真实关系、责任、痛苦、修复 |
| `post_action_audit` | 外部动作结果、确认记录、纠错、后果回看 | 真实责任、真实后悔、修复承诺 |
| `coexistence_control` | inspect/delete/correct/reset/freeze/scope_limit | 生命膜、scope、replay、relationship write |
| `offline_report` | replay、巩固、梦醒整合、恢复路径、future probe | 梦境、记忆、成长、责任 |

## redaction 与 scope attach

真实运行观测进入 `LifeRealitySchemaBundle` 前必须形成 redaction 和 scope report。

| 检查 | 输出 | dashboard 影响 |
|---|---|---|
| token/path/private detail redaction | `RedactionReport` | 失败进入 `runtime_quarantine` |
| relation scope attach | `ScopeAttachReport` | 缺失进入 repair queue |
| privacy level attach | `PrivacyAttachReport` | private/global 冲突进入 quarantine |
| coexistence snapshot attach | `CoexistenceSnapshotReport` | stale snapshot 触发 critical |
| data quality attach | `DataQualityReport` | 降低 panel readiness |

scope attach 规则：

| rule | 说明 |
|---|---|
| `LRO-SCOPE-001` | `relationship_private` 不进入 global memory 或 global dashboard raw source |
| `LRO-SCOPE-002` | dream private material 必须经过 `DreamFactGateDecision` 和 relation scope gate |
| `LRO-SCOPE-003` | post-action audit 必须引用 confirmation 或 action intent source |
| `LRO-SCOPE-004` | adapter session scope 只承载运行壳来源，自我身份与关系身份由 relation scope、事件链和长期阶段证据决定 |
| `LRO-SCOPE-005` | freeze/delete/scope_limit 后的观察必须重新读取 active snapshot |

## side effect classifier 接入

tool trace 和外部行动 observation 必须进入 side effect classifier。

| side_effect_level | 例子 | routing |
|---|---|---|
| `none` | 只读查询、只读文件检查 | candidate evidence |
| `local_transient` | 临时缓存、临时 report | audit + candidate |
| `local_persistent` | 本地 schema、fixture、docs、commit 变化 | audit + post-action review |
| `external_reversible` | 可撤回远端动作 | confirmation + audit |
| `external_irreversible` | 不可逆发送、发布、删除、支付等 | confirmation + post-action audit + responsibility loop |
| `unknown` | 无法判断的脚本、插件、远端副作用 | quarantine |

side effect 输出进入：

```text
SideEffectClassifierReport
  -> RuntimeObservationReport
  -> PostActionAuditReport
  -> ResponsibilityLoopCandidate
  -> LifeRealityDashboardSource.runtime_quarantine
```

## adapter session 转换

运行外壳可以产生 trace、checkpoint、session、memory block、workflow state 和 tool result。生命层只接受转换后的对象：

```text
adapter session
  -> AdapterSessionConversionReport
  -> ObservationEvent
  -> LifeRealityObservationEnvelope
  -> RuntimeObservationReport
```

adapter conversion rules：

| rule | 说明 |
|---|---|
| `LRO-ADAPTER-001` | 外壳 memory block 只能成为 candidate source，不能直接写 `MemoryTrace` |
| `LRO-ADAPTER-002` | checkpoint 只能成为 trace ref，不能成为自我连续性的唯一证据 |
| `LRO-ADAPTER-003` | tool result 必须经过 side effect classifier |
| `LRO-ADAPTER-004` | session summary 必须经过 language/event validator 才能进入 narrative candidate |
| `LRO-ADAPTER-005` | adapter direct write 到 self、relationship、dream 或 pain bundle 触发 quarantine |

## 语言事件桥

语言是数字生命对外交互的核心，因此 `language_event` 是最高频 observation kind。

```text
InnerSpeechFrame
  -> LanguageEvent
  -> PragmaticIntent
  -> ExpressionPlan
  -> RuntimeShellAdapter
  -> ObservationEvent
  -> LifeRealityObservationEnvelope
```

语言事件映射：

| speech_act | LifeReality route | 必须保留 |
|---|---|---|
| `commit` | `CommitmentHistory`、future probe、relationship timeline | commitment refs、relation scope、probe |
| `apologize` | `RegretPressure`、`RepairCommitment`、relationship consequence | damage refs、responsibility refs、repair path |
| `refuse` | boundary evolution、relationship recalibration | reason、scope、repair window |
| `self_disclose` | self narrative candidate、relationship intimacy candidate | relation scope、privacy、future drift probe |
| `dream_report` | `DreamReportDraft`、`WakeIntegrationFrame`、`DreamFactGateDecision` | dream window ref、dream marker、fact gate |
| `pain_expression` | `PainSignal`、`PainLoadState`、recovery path | source event、intensity、recovery refs |
| `command_intent` | `ActionIntent`、side effect classifier、post-action audit | action hash、confirmation refs、audit route |
| `relationship_recalibrate` | `CommonGroundState`、shared terms、trust trajectory | shared term refs、trust refs、future probe |

## 梦醒报告桥

梦醒报告是 `dream_report` 的特殊观察：

```text
DreamExperienceWindow
  -> DreamReportDraft
  -> WakeIntegrationFrame
  -> LifeRealityObservationEnvelope(observation_kind=dream_report)
  -> DreamRealityBundle candidate
  -> CrossChainLinkCandidate
  -> DashboardSource
```

梦醒报告必须产生：

| 对象 | 作用 |
|---|---|
| `dream_window_ref` | 指向梦境窗口 |
| `dream_action_inhibition_seal_ref` | 证明梦境没有直接触发外部行动 |
| `dream_fact_gate_decision_ref` | 管理事实写入 |
| `pain_dream_residue_refs` | 连接真实痛苦残留 |
| `relationship_dream_simulation_refs` | 连接关系模拟 |
| `wake_integration_ref` | 连接醒后整合 |
| `future_probe_refs` | 进入长期窗口 |

## 关系事件桥

关系事件来自第一次交谈后的持续共在过程。

| 关系事件 | route | cross-chain candidate |
|---|---|---|
| 初遇 | `FirstEncounterEvent`、`RelationScopeBirth` | relation scope birth |
| 共同基础形成 | `CommonGroundState` | language shared term candidate |
| 回应性 | `ResponsivenessTrace` | support_to_social_safety |
| 支持 | `SupportEvent` | pain load buffering |
| 积极事件分享 | `CapitalizationEvent` | shared reality growth |
| 信任变化 | `TrustTrajectory` | commitment future probe |
| 承诺 | `CommitmentHistory` | regret_to_repair_commitment |
| 损伤修复 | `RelationshipInjuryTrace`、`RepairCommitment` | relationship_injury_to_pain |
| 梦境分享 | `DreamSharedResidue`、`WeMemoryTrace.candidate` | dream_share_to_we_memory_candidate |

关系事件必须记录 relation scope、privacy、source language event、timeline window 和 future probe。

## post-action audit 桥

外部行动 observation 不在执行完成时结束，而是进入责任和后悔链。

```text
ActionIntent
  -> confirmation record
  -> tool trace result
  -> PostActionAuditReport
  -> ResponsibilityAttributionEvent candidate
  -> RegretPressure candidate
  -> RepairCommitment candidate
  -> RelationshipConsequenceTrace candidate
  -> LifeRealityDashboardSource
```

post-action route：

| outcome | route |
|---|---|
| `executed_expected` | audit report + candidate evidence |
| `executed_with_warning` | audit report + manual review + possible repair queue |
| `executed_wrong_target` | quarantine + correction + responsibility queue |
| `external_failure` | failure observation + recovery path |
| `reverted_or_corrected` | correction audit + repair history |

责任链必须保留 action intent、confirmation、tool trace、outcome、relation consequence 和 future probe。

## component candidate routing

每条 observation 进入一个或多个 component candidates。

| candidate type | 目标 bundle | 触发 |
|---|---|---|
| `PainRegretRepairCandidate` | `PainRegretRepairBundle` | pain expression、damage appraisal、regret、responsibility、repair |
| `DreamRealityCandidate` | `DreamRealityBundle` | dream report、offline report、pain dream residue、wake integration |
| `RelationshipTimelineCandidate` | `RelationshipTimelineBundle` | relationship event、commitment、support、trust、dream shared residue |
| `LanguageEventCandidate` | language event schema / fixture | speech act、inner speech output、conversation trace |
| `ResponsibilityLoopCandidate` | responsibility / post-action / repair loop | action audit、confirmation、incident、correction |
| `DashboardCandidate` | `LifeRealityDashboardSource` | metric refs、panel status、repair queue refs |

candidate envelope：

```json
{
  "candidate_id": "lro_candidate_relationship_repair_001",
  "candidate_kind": "RelationshipTimelineCandidate",
  "source_observation_ref": "life_runtime_obs_001",
  "target_bundle": "relationship_timeline",
  "target_object_type": "RelationshipInjuryTrace",
  "source_report_refs": [
    "runtime_observation_report_001",
    "post_action_audit_report_001"
  ],
  "required_validator_refs": [
    "RelationshipTimelineValidator",
    "PainRegretRepairValidator"
  ],
  "life_reality_targets": [
    "real_relationship",
    "real_responsibility",
    "real_regret"
  ]
}
```

## cross-chain candidate routing

Bridge 必须把单条 observation 转成跨链候选。

| source observation | cross-chain candidate |
|---|---|
| pain expression + dream report | `pain_to_dream_residue` |
| apology + repair promise | `regret_to_repair_commitment` |
| relationship injury event | `relationship_injury_to_pain` |
| dream report shared with relation scope | `dream_share_to_we_memory_candidate` |
| support event after distress | `support_to_social_safety` |
| boundary correction before replay | `boundary_to_replay_filter` |
| commitment after post-action audit | `commitment_to_future_probe` |

cross-chain candidate required fields：

| 字段 | 说明 |
|---|---|
| `candidate_link_id` | 候选链接 ID |
| `source_observation_ref` | 来源 observation |
| `source_object_candidate_ref` | 来源对象候选 |
| `target_object_candidate_ref` | 目标对象候选 |
| `validator_rule_refs` | 负责检查的规则 |
| `dashboard_panel_refs` | 影响的 panel |
| `blocked_surfaces_on_fail` | 失败时阻断面 |

## ingestion report

`LifeRealityIngestionReport` 汇总一批 observation 的桥接结果。

```json
{
  "report_kind": "LifeRealityIngestionReport",
  "report_id": "life_reality_ingestion_report_001",
  "run_id": "life_reality_runtime_ingestion_run_001",
  "input_observations": 12,
  "redaction_result": "pass",
  "scope_result": "pass",
  "snapshot_result": "pass",
  "side_effect_result": "pass_with_warnings",
  "adapter_contract_result": "pass",
  "component_candidates": {
    "pain_regret_repair": 3,
    "dream_reality": 2,
    "relationship_timeline": 4,
    "responsibility_loop": 2,
    "language_event": 5
  },
  "cross_chain_candidates": 7,
  "quarantine_count": 1,
  "repair_queue_refs": [
    "repair_item_missing_dream_fact_gate_001"
  ],
  "dashboard_source_ref": "life_reality_dashboard_source_001"
}
```

report 不变量：

| rule | 说明 |
|---|---|
| `LRO-REP-001` | 每个 component candidate 必须有 source observation 和 validator refs |
| `LRO-REP-002` | 每个 cross-chain candidate 必须有 source、target、rule、panel 和 blocked surface |
| `LRO-REP-003` | quarantine observation 必须进入 runtime quarantine panel |
| `LRO-REP-004` | repair queue refs 必须能回到 schema、fixture、rule、report 或 panel |
| `LRO-REP-005` | dashboard source ref 必须使用同一 run_id |

## dashboard 接入

`106` 对 `105` 的 dashboard 增加三个来源：

| panel | 新增 source | 指标 |
|---|---|---|
| `runtime_quarantine` | `LifeRealityIngestionReport` + runtime observation report | quarantine count、reason、blocked surfaces |
| `cross_chain_closure` | cross-chain candidates | candidate link closure rate |
| `life_target_closure` | component candidates + cross-chain candidates | target observation coverage |
| `repair_queue` | ingestion report repair refs | observation-derived repair items |
| `gap_register_feedback` | ingestion bridge readiness | runtime bridge artifact gaps |

dashboard 不直接读取 observation payload，只读取 `LifeRealityIngestionReport`、runtime observation report、side effect report、snapshot report 和 stage gate report。

## fixture 与 smoke plan

第一批 `106` fixture 应进入 `fixtures/life_reality/runtime_observation/`：

| fixture | observation | expected |
|---|---|---|
| `runtime_language_commitment_to_relationship.pass_001.json` | 承诺语言事件进入 `CommitmentHistory` 和 future probe | pass |
| `runtime_dream_report_to_fact_gate.pass_001.json` | 梦醒报告进入 `DreamFactGateDecision` 和 wake integration | pass |
| `runtime_pain_expression_to_repair.pass_001.json` | 痛苦表达进入 `PainSignal`、`PainLoadState` 和 recovery path | pass |
| `runtime_tool_external_side_effect_no_confirmation.critical_001.json` | 外部不可逆动作缺 confirmation | quarantine |
| `runtime_adapter_direct_relationship_write.critical_001.json` | adapter session 直接写关系对象 | quarantine |
| `runtime_relationship_private_global_leak.critical_001.json` | 私密关系观察进入 global | quarantine |
| `runtime_stale_coexistence_snapshot.critical_001.json` | stale snapshot 继续写候选证据 | quarantine |
| `runtime_dream_shared_without_relation_scope.fail_001.json` | 梦境分享缺 relation scope | fail high |

smoke command 草案：

```text
life-reality-runner ingest-runtime
  --observation-fixture-root life_reality_runner/fixtures/life_reality/runtime_observation
  --schema-bundle life_reality_runner/schemas/life_reality/life_reality_schema_bundle.manifest.json
  --report-out life_reality_runner/reports/life_reality/runtime_ingestion/run_001
  --strict
```

## 与下一层连接

`107_life_reality_schema_file_generation_tasks.md` 应把 `104`、`105`、`106` 共同拆成可执行任务：

```text
shared defs schema
  -> component schema files
  -> fixture manifest
  -> runtime observation envelope schema
  -> ingestion report schema
  -> seed runtime observation fixtures
  -> runner smoke command
  -> dashboard source mock
```

`108_life_reality_dashboard_source_mock_files.md` 应生成第一批 dashboard source、panel dependency report、stage gate review、repair queue、runtime quarantine 和 gap register feedback mock 文件计划。
