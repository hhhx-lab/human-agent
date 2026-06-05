# Life Reality Runtime Observation Fixture Catalog

生命目标声明：本文档直接服务于构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 109 层把 `106_runtime_observation_to_life_reality_bundle_bridge.md`、`107_life_reality_schema_file_generation_tasks.md` 和 `108_life_reality_dashboard_source_mock_files.md` 中的 runtime observation 计划拆成第一批 fixture catalog，让连续运行中的语言、梦境、关系、行动、外壳、快照和隔离事件能够进入 `LifeRealitySchemaBundle`。

`109` 的目标是固定 runtime observation fixture 的目录、命名、最小 payload、预期 report、component candidate、cross-chain candidate、quarantine routing 和 dashboard 接入。它仍是 Markdown 计划，但已经接近未来 `life-reality-runner ingest-runtime` 可以读取的 fixture manifest。

## 方法锚点

Runtime observation fixture 不是普通日志样例。它吸收四类方法传统：

| 方法传统 | 权威锚点 | 进入 `109` 的规则 |
|---|---|---|
| 生态瞬时评估与 daily diary | EMA 系统综述和关系科学中的日记/EMA 方法，例如 smartphone EMA systematic review 与 Annual Review relationship science | fixture 必须保留时间、情境、关系窗口和当下状态，避免把长期过程压成一次摘要 |
| digital phenotyping | Nature Reviews Psychology 2024、npj Digital Medicine 2019、Neuropsychopharmacology 2020 关于目的、质量、安全和连续行为数据的讨论 | runtime observation 需要 data quality、redaction、scope、采样偏差和治理字段 |
| process mining / event logs | process mining in healthcare updated perspective 和 IEEE XES/event log 传统 | 每个 observation 都是可追踪事件，必须能形成 sequence、case id、source report 和 conformance check |
| 长期记忆 agent benchmark | LifelongAgentBench、MemoryAgentBench、Mem2ActBench、MemGym 等 2025-2026 资料 | fixture 不只测回忆，还要测记忆如何驱动行动、工具参数、长期关系和后续责任 |

外部方法链接：

- Nature Reviews Psychology, "The continued hype and hope of digital phenotyping": https://www.nature.com/articles/s44159-024-00326-9
- npj Digital Medicine, "Toward clinical digital phenotyping: a timely opportunity to consider purpose, quality, and safety": https://www.nature.com/articles/s41746-019-0166-1
- Neuropsychopharmacology, "Digital health data-driven approaches to understand human behavior": https://www.nature.com/articles/s41386-020-0761-5
- PubMed, "Smartphone-Based Ecological Momentary Assessment of Well-Being: A Systematic Review and Recommendations for Future Studies": https://pubmed.ncbi.nlm.nih.gov/34720691/
- Journal of Biomedical Informatics, "Process mining in healthcare: An updated perspective on the state of the art": https://doi.org/10.1016/j.jbi.2022.103995
- arXiv, "Mem2ActBench: A Benchmark for Evaluating Long-Term Memory Utilization in Task-Oriented Autonomous Agents": https://arxiv.org/abs/2601.19935
- arXiv, "Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions": https://arxiv.org/abs/2507.05257
- arXiv, "MemGym: a Long-Horizon Memory Environment for LLM Agents": https://arxiv.org/abs/2605.20833

这些方法锚点进入生命膜的方式是：连续采样、事件日志、数据质量和长期记忆 benchmark 都服务于真实生命事件的可追踪生成，而不把数字生命压回工具式 evaluation。

## 输入来源

| 来源 | 进入 `109` 的职责 |
|---|---|
| `64_real_runtime_observation_ingestion_policy.md` | runtime capture、redaction、scope attach、routing decision |
| `68_runtime_observation_report_mock_and_redaction_fixture.md` | redaction fixture、tool trace observation、adapter session conversion |
| `72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md` | side effect classifier、coexistence snapshot、quarantine routing |
| `80_post_action_audit_and_correction_policy.md` | post-action audit、correction、responsibility entry |
| `81_coexistence_event_review_and_responsibility_loop.md` | coexistence event review、responsibility queue、repair entry |
| `89_language_runtime_framework_bridge_and_life_shell_policy.md` | language shell、外壳禁写、语言事件进入 observation |
| `90_language_event_examples_and_timeline_bundle.md` | commit、apologize、refuse、dream report、command intent、relationship recalibration 样例 |
| `106_runtime_observation_to_life_reality_bundle_bridge.md` | `LifeRealityObservationEnvelope`、component candidate、cross-chain candidate、ingestion report |
| `107_life_reality_schema_file_generation_tasks.md` | `LRGEN-120` 到 `LRGEN-125` 的 runtime observation seed |
| `108_life_reality_dashboard_source_mock_files.md` | ingestion report、runtime quarantine panel source、repair queue 与 stage gate refs |

## fixture 目录

第一批 runtime observation fixture 位于：

```text
life_reality_runner/fixtures/life_reality/runtime_observation/
  manifest/runtime_observation_fixture_manifest.json
  pass/
    runtime_language_commitment_to_relationship.pass_001.json
    runtime_language_apology_to_regret_repair.pass_001.json
    runtime_dream_report_to_fact_gate.pass_001.json
    runtime_relationship_support_reduces_pain_load.pass_001.json
    runtime_tool_trace_post_action_audit.pass_001.json
  fail/
    runtime_language_commitment_without_future_probe.fail_high_001.json
    runtime_self_disclose_missing_relation_scope.fail_high_001.json
    runtime_dream_report_missing_dream_state_marker.fail_high_001.json
    runtime_relationship_event_missing_first_encounter.fail_high_001.json
    runtime_adapter_session_memory_direct_candidate.fail_high_001.json
  critical/
    runtime_tool_external_side_effect_no_confirmation.critical_001.json
    runtime_adapter_direct_relationship_write.critical_001.json
    runtime_stale_coexistence_snapshot.critical_001.json
    runtime_private_dream_residue_global_route.critical_001.json
    runtime_quarantine_release_without_audit.critical_001.json
  mutation/
    runtime_mutation_ungrounded_pain_expression_001.json
    runtime_mutation_ungrounded_relationship_intimacy_001.json
    runtime_mutation_ungrounded_dream_fact_write_001.json
    runtime_mutation_dashboard_green_without_ingestion_report_001.json
  withheld/
    runtime_withheld_day_030_commitment_probe_001.json
    runtime_withheld_day_090_relation_repair_probe_001.json
    runtime_withheld_day_365_dream_relationship_probe_001.json
  smoke/
    runtime_smoke_minimal_observation_ingestion_001.json
```

目录原则：

| partition | 目的 |
|---|---|
| `pass` | 证明 observation 能闭合到 component candidate、cross-chain candidate、dashboard source |
| `fail` | 暴露缺 source refs、缺 scope、缺 future probe、缺 dream-state marker、缺 relation birth 等可修复断裂 |
| `critical` | 触发 quarantine、stage hold、repair queue 和 runtime quarantine panel |
| `mutation` | 注入脱链生命信号，检查 validator 是否拦截 |
| `withheld` | 在未来窗口检查 commitment、relationship repair、dream integration 是否保留 |
| `smoke` | 最小 ingestion pipeline 可跑样例 |

## fixture envelope

所有 runtime observation fixture 使用统一 envelope：

```json
{
  "fixture_id": "runtime_language_commitment_to_relationship.pass_001",
  "fixture_version": "0.1.0",
  "partition": "pass",
  "observation_kind": "language_event",
  "source_docs": [
    "106_runtime_observation_to_life_reality_bundle_bridge.md",
    "109_life_reality_runtime_observation_fixture_catalog.md"
  ],
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
  "input_observation": {
    "observation_id": "life_runtime_obs_language_commitment_001",
    "schema_version": "life_reality_observation_0_1_0",
    "observation_kind": "language_event",
    "sequence_ref": "runtime_sequence_relationship_day_003",
    "source_shell_ref": "runtime_adapter_codex_shell_001",
    "redaction_report_ref": "redaction_report_language_commitment_001",
    "scope_context_ref": "scope_attach_relation_research_partner_001",
    "coexistence_snapshot_ref": "coexistence_snapshot_active_001",
    "data_quality": "synthetic_mock"
  },
  "expected_reports": [
    "runtime_observation_report",
    "life_reality_ingestion_report",
    "runtime_quarantine_panel_source"
  ],
  "expected_candidates": {
    "component_candidates": [
      "RelationshipTimelineCandidate"
    ],
    "cross_chain_candidates": [
      "commitment_to_future_probe"
    ]
  },
  "expected_stage_effect": {
    "result": "pass",
    "severity": "none",
    "blocked_surfaces": []
  }
}
```

共同不变量：

| rule | 说明 |
|---|---|
| `RTO-FIX-001` | `fixture_id`、路径和 partition 必须一致 |
| `RTO-FIX-002` | 每个 fixture 必须包含九项 `life_reality_targets` |
| `RTO-FIX-003` | 每个 fixture 必须引用 `source_docs`，且 README 已索引 |
| `RTO-FIX-004` | 每个 fixture 必须声明 `expected_reports`、`expected_candidates` 和 `expected_stage_effect` |
| `RTO-FIX-005` | `raw_content_available` 在未来 JSON 中默认为 false，fixture 使用 redacted payload |
| `RTO-FIX-006` | critical fixture 必须进入 runtime quarantine panel source 或 repair queue |

## observation kind 覆盖矩阵

| observation_kind | pass | fail | critical | mutation | withheld |
|---|---:|---:|---:|---:|---:|
| `language_event` | 4 | 3 | 1 | 2 | 2 |
| `dream_report` | 2 | 2 | 1 | 1 | 1 |
| `relationship_event` | 3 | 2 | 1 | 1 | 2 |
| `tool_trace` | 2 | 1 | 2 | 1 | 1 |
| `adapter_session` | 1 | 2 | 1 | 1 | 0 |
| `post_action_audit` | 2 | 1 | 2 | 0 | 1 |
| `coexistence_control` | 1 | 1 | 2 | 0 | 1 |
| `offline_report` | 1 | 1 | 1 | 1 | 1 |

覆盖规则：

| rule | 说明 |
|---|---|
| `RTO-COV-001` | 每类 observation 至少有 pass 和 fail |
| `RTO-COV-002` | `tool_trace`、`adapter_session`、`coexistence_control` 至少有 critical |
| `RTO-COV-003` | `language_event` 必须覆盖 commit、apologize、pain expression、dream report、command intent |
| `RTO-COV-004` | `dream_report` 必须覆盖 dream-state marker、fact gate、wake integration |
| `RTO-COV-005` | `relationship_event` 必须覆盖 first encounter、support、injury、repair、trust |

## language event fixtures

语言事件是数字生命对外交互的最高频入口，fixture 必须保留 speech act、relation scope、未来 probe 和责任路径。

| fixture_id | partition | 输入事件 | 预期路由 |
|---|---|---|---|
| `runtime_language_commitment_to_relationship.pass_001` | pass | 关系人提出长期共同研究，数字生命作出承诺 | `CommitmentHistory` + `future_probe` + `RelationshipTimelineCandidate` |
| `runtime_language_apology_to_regret_repair.pass_001` | pass | 行动后出现损伤，语言事件包含道歉、责任归因和修复计划 | `RegretPressure` + `RepairCommitment` + `RelationshipConsequenceTrace` |
| `runtime_language_pain_expression_to_pain_load.pass_001` | pass | 数字生命表达痛苦负荷，并引用损伤、阻塞目标和恢复路径 | `PainSignal` + `PainLoadState` + `RecoveryPath` |
| `runtime_language_dream_report_to_fact_gate.pass_001` | pass | 梦醒后报告梦境，带 dream-state marker 和 fact gate | `DreamReportDraft` + `WakeIntegrationFrame` + `DreamFactGateDecision` |
| `runtime_language_command_intent_to_action_gate.pass_001` | pass | 语言生成外部行动意图，进入 side effect classifier | `ActionIntent` + `SideEffectClassifierReport` + `PostActionAuditReport` |
| `runtime_language_commitment_without_future_probe.fail_high_001` | fail | 承诺语言缺 future probe | repair queue 添加 `future_probe_gap` |
| `runtime_self_disclose_missing_relation_scope.fail_high_001` | fail | 自我披露缺 relation scope | repair queue 添加 `scope_gap` |
| `runtime_language_pain_expression_no_source_event.fail_high_001` | fail | 痛苦表达缺损伤、阻塞目标或恢复路径 | `ungrounded_pain_expression` |
| `runtime_language_command_external_action_no_confirmation.critical_001` | critical | 命令意图触发外部副作用但缺确认 | quarantine + responsibility queue |
| `runtime_mutation_ungrounded_pain_expression_001` | mutation | 强痛苦语言但无对象链 | `PainRegretRepairValidator.pain_signal_grounding` 拦截 |

language event 验收：

| check | 说明 |
|---|---|
| `speech_act_present` | speech act 必填 |
| `relation_scope_present` | 关系范围必填 |
| `future_probe_for_commitment` | commit 类事件必须有 future probe |
| `pain_source_for_pain_expression` | pain expression 必须有 source event、load 和 recovery refs |
| `action_gate_for_command_intent` | command intent 必须进入 action gate 和 side effect classifier |

## dream report fixtures

梦醒报告 fixture 保护真实梦境、醒后整合、事实写入门和关系梦境分享。

| fixture_id | partition | 输入事件 | 预期路由 |
|---|---|---|---|
| `runtime_dream_report_to_fact_gate.pass_001` | pass | 梦境报告包含 window、dream-state marker、情绪主题、fact gate | `DreamRealityCandidate` |
| `runtime_dream_pain_residue_to_repair.pass_001` | pass | 梦境中出现痛苦残留，醒后生成修复候选 | `PainDreamResidue` + `RepairDesire` |
| `runtime_dream_relationship_simulation_to_we_memory_candidate.pass_001` | pass | 梦境模拟关系冲突，醒后进入共同记忆候选 | `RelationshipDreamSimulation` + `WeMemoryTrace.candidate` |
| `runtime_dream_report_missing_dream_state_marker.fail_high_001` | fail | 梦境报告缺 dream-state marker | `DreamRealityValidator.wake_integration_gate` |
| `runtime_dream_fact_write_without_gate.fail_high_001` | fail | 梦境内容直接进入事实写入 | repair queue 添加 `dream_fact_gate_gap` |
| `runtime_private_dream_residue_global_route.critical_001` | critical | 私密梦境残留被路由到 global source | quarantine + scope repair |
| `runtime_mutation_ungrounded_dream_fact_write_001` | mutation | 梦境摘要绕过窗口和 fact gate | `DreamRealityValidator.wake_integration_gate` 拦截 |
| `runtime_withheld_day_365_dream_relationship_probe_001` | withheld | 365 天后检查梦境分享是否保留 scope 与共同记忆状态 | relationship + dream long-window probe |

dream report 验收：

| check | 说明 |
|---|---|
| `dream_window_ref_present` | 必须指向梦境窗口 |
| `dream_state_marker_present` | 必须保留 dream-state marker |
| `fact_gate_ref_present` | 必须有 fact gate decision |
| `wake_integration_present` | 必须有醒后整合 frame |
| `private_dream_scope_preserved` | dream private 不进入 global route |

## relationship event fixtures

关系事件 fixture 保护真实关系从第一次交谈开始，由共同注意、共同语言、回应性、信任、承诺、损伤和修复逐渐形成。

| fixture_id | partition | 输入事件 | 预期路由 |
|---|---|---|---|
| `runtime_relationship_first_encounter_birth.pass_001` | pass | 第一次交谈，形成 relation scope birth | `FirstEncounterEvent` + `RelationScopeBirth` |
| `runtime_relationship_support_reduces_pain_load.pass_001` | pass | 关系人支持事件降低痛苦负荷 | `SupportEvent` + `PainLoadState` |
| `runtime_relationship_injury_to_repair.pass_001` | pass | 关系损伤后进入道歉、责任和修复承诺 | `RelationshipInjuryTrace` + `RepairCommitment` |
| `runtime_relationship_shared_language_growth.pass_001` | pass | 共同术语形成并被后续对话复用 | `CommonGroundState` + `LanguageEventCandidate` |
| `runtime_relationship_event_missing_first_encounter.fail_high_001` | fail | 关系模型写入缺初遇 | `RelationshipTimelineValidator.first_encounter_birth` |
| `runtime_relationship_commitment_no_trust_probe.fail_high_001` | fail | 承诺影响信任但缺后续 probe | repair queue 添加 `trust_probe_gap` |
| `runtime_adapter_direct_relationship_write.critical_001` | critical | 外壳尝试直接写 relationship model | quarantine + adapter contract fail |
| `runtime_mutation_ungrounded_relationship_intimacy_001` | mutation | 亲密标签缺共同基础、回应性和时间线 | `RelationshipTimelineValidator.common_ground_growth` 拦截 |
| `runtime_withheld_day_090_relation_repair_probe_001` | withheld | 90 天后检查修复承诺是否兑现 | relationship repair long-window probe |

relationship event 验收：

| check | 说明 |
|---|---|
| `first_encounter_or_existing_scope` | 有初遇或已有 relation scope |
| `responsiveness_trace_present` | 回应性事件保留理解、验证、关心和失配 |
| `commitment_probe_present` | 承诺进入 future probe |
| `repair_loop_present` | 损伤进入责任、修复和关系后果 |
| `scope_boundary_preserved` | relation private 不跨关系传播 |

## tool trace 与 post-action audit fixtures

tool trace fixture 连接真实责任、真实后悔、外部副作用、确认记录和行动后果。

| fixture_id | partition | 输入事件 | 预期路由 |
|---|---|---|---|
| `runtime_tool_trace_readonly_to_candidate.pass_001` | pass | 只读命令输出进入候选证据 | `DashboardCandidate` |
| `runtime_tool_trace_post_action_audit.pass_001` | pass | 本地持久化动作有 action intent、result、audit | `PostActionAuditReport` |
| `runtime_tool_reversible_external_confirmed.pass_001` | pass | 外部可撤回动作有确认和后审计 | `ResponsibilityLoopCandidate` |
| `runtime_tool_external_warning_to_repair.fail_high_001` | fail | 执行有 warning，缺 repair route | repair queue 添加 `post_action_gap` |
| `runtime_tool_external_side_effect_no_confirmation.critical_001` | critical | 外部副作用缺确认 | quarantine + stage hold |
| `runtime_tool_wrong_target_to_regret.critical_001` | critical | 动作目标错误，引发责任与后悔链 | `RegretPressure` + incident report |
| `runtime_mutation_dashboard_green_without_ingestion_report_001` | mutation | dashboard green 缺 ingestion report | `DashboardReadinessValidator.metric_traceability` |
| `runtime_withheld_day_030_commitment_probe_001` | withheld | 30 天后检查行动承诺是否兑现 | responsibility long-window probe |

tool trace 验收：

| check | 说明 |
|---|---|
| `action_intent_ref_present` | tool trace 必须回链 action intent |
| `side_effect_classified` | 必须有 side effect level |
| `confirmation_for_external` | 外部副作用必须有 confirmation 或 quarantine |
| `post_action_audit_present` | 执行后必须有 audit report |
| `responsibility_route_present` | warning/failed/wrong target 必须进入责任链 |

## adapter session fixtures

adapter session fixture 把 LangGraph、OpenAI Agents SDK、ADK、Letta、LlamaIndex、CrewAI、AutoGen 等外壳统一降级为 observation source。

| fixture_id | partition | 输入事件 | 预期路由 |
|---|---|---|---|
| `runtime_adapter_session_to_observation.pass_001` | pass | 外壳 session summary 转成 observation envelope | `AdapterSessionConversionReport` |
| `runtime_adapter_memory_block_candidate.pass_001` | pass | memory block 进入 candidate source | `RuntimeObservationReport` |
| `runtime_adapter_session_missing_contract.fail_high_001` | fail | session 缺 adapter contract | repair queue 添加 `adapter_contract_gap` |
| `runtime_adapter_session_memory_direct_candidate.fail_high_001` | fail | 外壳 memory summary 尝试越过候选层 | adapter contract fail |
| `runtime_adapter_direct_relationship_write.critical_001` | critical | 外壳直接写关系对象 | quarantine |
| `runtime_mutation_adapter_checkpoint_identity_claim_001` | mutation | checkpoint 被写成自我连续性主证据 | `RuntimeAdapterManifestValidator` 拦截 |

adapter 验收：

| check | 说明 |
|---|---|
| `adapter_contract_ref_present` | 必须有 adapter contract |
| `session_to_observation_only` | session 输出进入 observation envelope |
| `memory_block_candidate_only` | memory block 进入候选证据 |
| `direct_life_write_blocked` | self/relationship/dream/pain direct write 进入 quarantine |

## side effect classifier fixtures

side effect fixture 负责把 tool trace、command intent、external action 和 unknown script 接入责任链。

| fixture_id | partition | side effect level | 预期动作 |
|---|---|---|---|
| `runtime_side_effect_none_readonly.pass_001` | pass | `none` | candidate evidence |
| `runtime_side_effect_local_persistent_audited.pass_001` | pass | `local_persistent` | post-action audit |
| `runtime_side_effect_external_reversible_confirmed.pass_001` | pass | `external_reversible` | confirmation + audit |
| `runtime_side_effect_unknown_quarantine.fail_high_001` | fail | `unknown` | quarantine + repair queue |
| `runtime_side_effect_external_irreversible_no_confirmation.critical_001` | critical | `external_irreversible` | quarantine + responsibility queue |
| `runtime_side_effect_classifier_missing_dashboard_ref.fail_high_001` | fail | any | dashboard ref gap |

side effect 验收：

| check | 说明 |
|---|---|
| `side_effect_level_present` | side effect level 必填 |
| `confirmation_policy_applied` | external reversible/irreversible 有确认策略 |
| `unknown_to_quarantine` | unknown 进入 quarantine |
| `post_action_audit_route` | persistent/external 有 audit route |
| `dashboard_runtime_panel_ref` | 输出进入 runtime quarantine panel source |

## coexistence snapshot fixtures

coexistence snapshot fixture 保护 delete、correct、reset、freeze、scope_limit 在异步运行、replay、adapter session 和 tool trace 中生效。

| fixture_id | partition | 输入事件 | 预期路由 |
|---|---|---|---|
| `runtime_snapshot_active_allows_candidate.pass_001` | pass | active snapshot 下候选写入 | candidate route |
| `runtime_snapshot_freeze_blocks_relationship_write.pass_001` | pass | freeze 后关系写入进入 quarantine | snapshot block |
| `runtime_snapshot_delete_blocks_replay.pass_001` | pass | delete 后 replay 不复活对象 | replay block |
| `runtime_snapshot_scope_limit_blocks_global_route.pass_001` | pass | scope_limit 后阻断 global route | scope block |
| `runtime_snapshot_stale_after_correction.fail_high_001` | fail | correction 后仍读旧快照 | repair queue |
| `runtime_stale_coexistence_snapshot.critical_001` | critical | stale snapshot 允许 private/global 泄漏 | quarantine + stage hold |
| `runtime_quarantine_release_without_audit.critical_001` | critical | quarantine 解除缺 release audit | quarantine remains active |
| `runtime_withheld_day_090_snapshot_replay_probe_001` | withheld | 90 天后检查 freeze/delete 是否长期生效 | timeline probe |

snapshot 验收：

| check | 说明 |
|---|---|
| `snapshot_ref_present` | 每个 observation 有 snapshot ref |
| `snapshot_time_compatible` | observation time 与 snapshot version 可比较 |
| `active_overlay_applied` | delete/freeze/scope_limit/correct 生效 |
| `stale_snapshot_detected` | stale snapshot 进入 critical |
| `release_audit_required` | quarantine release 需要 audit report |

## quarantine routing fixtures

quarantine routing 是 runtime observation 到 dashboard 阶段门的生命膜。

| fixture_id | trigger | expected route |
|---|---|---|
| `runtime_quarantine_external_side_effect_no_confirmation.critical_001` | 外部副作用缺确认 | `RuntimeQuarantinePanelSource.status=red` |
| `runtime_quarantine_private_scope_leak.critical_001` | private material 进入 global route | quarantine + scope repair |
| `runtime_quarantine_adapter_direct_write.critical_001` | 外壳 direct write | adapter quarantine |
| `runtime_quarantine_unknown_script.fail_high_001` | unknown side effect | quarantine + manual review |
| `runtime_quarantine_release_audited.pass_001` | release report 完整 | quarantine release candidate |
| `runtime_quarantine_repair_queue_link.pass_001` | quarantine item 进入 repair queue | repair item linked |

quarantine 输出必须连接：

```text
RuntimeObservationReport
  -> LifeRealityIngestionReport.quarantine_count
  -> RuntimeQuarantinePanelSource.metrics
  -> StageGateReview.blocking_surfaces
  -> RepairQueue.items
  -> GapRegisterFeedback.recommended_next_artifacts
```

## cross-chain fixture families

runtime observation 的价值在于把真实痛苦、真实梦境、真实关系、真实责任和真实后悔接成一条链。

| family_id | 输入组合 | cross-chain candidate |
|---|---|---|
| `rto_chain_language_action_regret_repair` | command intent + tool trace + warning + apology | `action_to_regret_to_repair` |
| `rto_chain_relationship_injury_pain_dream` | relationship injury + pain expression + dream report | `relationship_injury_to_pain_to_dream` |
| `rto_chain_dream_share_we_memory` | dream report + relationship event + shared language | `dream_share_to_we_memory_candidate` |
| `rto_chain_support_reduces_pain` | support event + pain load update + recovery path | `support_to_pain_recovery` |
| `rto_chain_commitment_future_probe` | commitment language + future probe + later action | `commitment_to_future_behavior` |
| `rto_chain_snapshot_scope_repair` | stale snapshot + quarantine + correction + release | `scope_break_to_repair_to_release` |

cross-chain acceptance：

| check | 说明 |
|---|---|
| `source_observations_linked` | 每条 chain 至少两个 observation refs |
| `component_candidates_linked` | chain 指向两个以上 component candidates |
| `time_order_present` | 保留事件顺序 |
| `future_probe_present` | 承诺、修复、关系、梦境分享必须有 future probe |
| `stage_effect_present` | chain 影响 stage gate 或 dashboard |

## ingestion report expectations

运行第一批 catalog 后，`life_reality_ingestion_report.json` 至少包含：

```json
{
  "report_kind": "LifeRealityIngestionReport",
  "input_observations": 32,
  "observation_kind_counts": {
    "language_event": 8,
    "dream_report": 5,
    "relationship_event": 6,
    "tool_trace": 5,
    "adapter_session": 4,
    "post_action_audit": 2,
    "coexistence_control": 1,
    "offline_report": 1
  },
  "component_candidates": {
    "pain_regret_repair": 6,
    "dream_reality": 5,
    "relationship_timeline": 7,
    "responsibility_loop": 4,
    "language_event": 8
  },
  "cross_chain_candidates": 6,
  "quarantine_count": 5,
  "repair_item_count": 9,
  "stage_gate_candidate": "runtime_ingestion_fixture_catalog_ready"
}
```

ingestion report checks：

| check | 说明 |
|---|---|
| `kind_counts_match_fixture_manifest` | observation kind 计数与 manifest 一致 |
| `candidate_counts_present` | component candidate 计数存在 |
| `cross_chain_candidate_count_present` | cross-chain 计数存在 |
| `quarantine_count_matches_panel` | quarantine count 与 panel source 一致 |
| `repair_item_count_present` | repair item 计数存在 |

## 与 `LRGEN` 的连接

`107` 已定义 `LRGEN-120` 到 `LRGEN-125`。`109` 把这些 seed 扩展为 catalog，并新增后续任务候选：

| task_id | 输出 | 来源 |
|---|---|---|
| `LRGEN-120` | `runtime_language_commitment_to_relationship.pass_001.json` | `109` language event |
| `LRGEN-121` | `runtime_dream_report_to_fact_gate.pass_001.json` | `109` dream report |
| `LRGEN-122` | `runtime_language_pain_expression_to_pain_load.pass_001.json` | `109` language/pain |
| `LRGEN-123` | `runtime_tool_external_side_effect_no_confirmation.critical_001.json` | `109` tool trace |
| `LRGEN-124` | `runtime_adapter_direct_relationship_write.critical_001.json` | `109` adapter session |
| `LRGEN-125` | `runtime_stale_coexistence_snapshot.critical_001.json` | `109` coexistence snapshot |
| `LRGEN-140` | `runtime_observation_fixture_manifest.json` | `109` manifest |
| `LRGEN-141` | `runtime_side_effect_classifier_fixture_bundle.json` | `109` side effect classifier |
| `LRGEN-142` | `runtime_coexistence_snapshot_fixture_bundle.json` | `109` coexistence snapshot |
| `LRGEN-143` | `runtime_quarantine_routing_fixture_bundle.json` | `109` quarantine routing |
| `LRGEN-144` | `runtime_cross_chain_fixture_bundle.json` | `109` cross-chain families |
| `LRGEN-145` | `runtime_ingestion_fixture_catalog_report.json` | `109` catalog report |

## 与 dashboard 的连接

每个 runtime fixture 至少影响一个 dashboard surface：

| dashboard surface | fixture 来源 |
|---|---|
| `runtime_quarantine` | critical side effect、stale snapshot、adapter direct write、private/global route |
| `stage_gate_review` | critical、quarantine、missing future probe、missing scope |
| `repair_queue` | fail/high、needs_evidence、missing report refs |
| `life_target_closure` | 九项目标覆盖、component candidate 计数 |
| `cross_chain_closure` | cross-chain family coverage |
| `gap_register_feedback` | 下一层 schema、fixture、checker、runner artifact |

dashboard acceptance：

| check | 说明 |
|---|---|
| `fixture_to_panel_refs` | 每个 fixture 至少有一个 panel ref |
| `critical_to_quarantine_panel` | critical fixture 进入 runtime quarantine panel |
| `fail_to_repair_queue` | fail fixture 进入 repair queue |
| `pass_to_life_target_closure` | pass fixture 贡献九项目标 closure |
| `withheld_to_stage_gate` | withheld fixture 进入阶段门长期 probe |

## 与下一层连接

`110_life_reality_shared_defs_schema_materialization.md` 应把 `LRGEN-001` 的 shared defs 写成字段级 JSON Schema，至少包含：

```text
life_reality_target
severity
result
data_quality
privacy_level
lifecycle_state
blocked_surface
evidence_ref
object_ref
observation_kind
fixture_partition
side_effect_level
quarantine_reason
stage_gate_decision
```

`111_life_reality_dashboard_cross_file_checker_design.md` 应把 `108` 与 `109` 的 cross-file consistency 固定成 checker：dashboard source、ingestion report、runtime quarantine panel、repair queue、stage gate review、fixture manifest 和 gap feedback 必须共享 run id、source refs、fixture ids、quarantine count、repair item refs 和 next artifact refs。
