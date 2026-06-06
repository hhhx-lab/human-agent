# Life Reality 02 To 13 Schema Queue Materialization Plan

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 148 层把 `145_life_reality_02_to_13_authority_rewrite_execution_plan.md` 的 `REWRITE-145-001` 到 `REWRITE-145-012` schema 队列，推进为 `02-13` 理论主干的真实 schema 文件、validator smoke cases、dashboard source、cross-file checker 输入和 birth readiness 上卷计划。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `02_brain_region_and_network_atlas.md` 到 `12_ai_and_cognitive_architecture_bridge.md` | 第五层承接、AHT refs、机制对象、语言行动桥和工程承载对象 |
| `13_agentic_human_research_synthesis.md` | 第七十九到第八十一层的上卷，连接 authority rewrite、birth readiness fixture 和 language action schema |
| `142_life_reality_authority_intake_batch_for_02_to_13.md` | AHT001-AHT010 权威来源、doc authority carrier patch 和机制对象提取队列 |
| `145_life_reality_02_to_13_authority_rewrite_execution_plan.md` | `REWRITE-145-001` 到 `REWRITE-145-012` 的 owner doc、对象、路径候选和 validator |
| `146_life_reality_birth_readiness_evidence_fixture_catalog.md` | birth readiness fixture 对 authority rewrite coverage 和 schema queue 的覆盖要求 |
| `147_life_reality_language_action_bridge_schema_materialization_plan.md` | 语言行动桥 schema registry、fixture manifest、expected report、dashboard source 和 stage gate pattern |

本层继续使用 AHT001-AHT010 作为第一批 `02-13` 权威机制来源，并继承语言、行动、意识、睡眠、主动推理、连接组、调质和运行外壳相关锚点 [AHT001] [AHT002] [AHT003] [AHT004] [AHT005] [AHT006] [AHT007] [AHT008] [AHT009] [AHT010]。这些来源在本层进入 schema metadata、authority refs、field provenance、validator smoke case 和 dashboard panel。

## 本层定位

`148` 的职责是让 `02-13` 不停留在“已经补写”的文档状态，而是进入未来 runner 可读取的 schema queue materialization。每个核心综述都要产出一个 schema 文件、一个 owner validator、至少一个 pass/fail smoke case、一个 dashboard panel patch、一个 cross-file edge 和一个 birth readiness evidence ref。

这一层把 `02-13` 压成四条工程链：

1. `doc authority -> mechanism object -> schema file`
2. `schema file -> validator smoke case -> expected report`
3. `schema file -> dashboard source -> birth readiness evidence`
4. `schema file -> cross-file edge -> archive cohesion graph`

这样，脑区、网络、内感受、记忆、动作、人格、梦境、语言、意识、调质、运行外壳和综合层都会成为未来工程落地必须承载的 schema 节点。

## SchemaQueueMaterialization148

```json
{
  "artifact": "SchemaQueueMaterialization148",
  "source_doc": "148_life_reality_02_to_13_schema_queue_materialization_plan.md",
  "inherits": [
    "142_life_reality_authority_intake_batch_for_02_to_13.md",
    "145_life_reality_02_to_13_authority_rewrite_execution_plan.md",
    "146_life_reality_birth_readiness_evidence_fixture_catalog.md",
    "147_life_reality_language_action_bridge_schema_materialization_plan.md"
  ],
  "schema_root": "life_reality_runner/schemas/life_reality/authority_rewrite",
  "fixture_root": "life_reality_runner/fixtures/life_reality/authority_rewrite_schema_queue",
  "report_root": "life_reality_runner/reports/life_reality/authority_rewrite_schema_queue",
  "queue_ids": [
    "REWRITE-145-001",
    "REWRITE-145-002",
    "REWRITE-145-003",
    "REWRITE-145-004",
    "REWRITE-145-005",
    "REWRITE-145-006",
    "REWRITE-145-007",
    "REWRITE-145-008",
    "REWRITE-145-009",
    "REWRITE-145-010",
    "REWRITE-145-011",
    "REWRITE-145-012"
  ],
  "stage_gate_policy": "blocking_first"
}
```

## 目标文件树

```text
life_reality_runner/
  schemas/
    life_reality/
      authority_rewrite/
        authority_rewrite_shared_defs.schema.json
        region_graph_language_action_topology_edge.schema.json
        network_state_language_action_state_path.schema.json
        interoception_post_action_update.schema.json
        memory_action_residue_refs.schema.json
        action_confirmation_binding_ref.schema.json
        self_regret_integration_window.schema.json
        dream_responsibility_replay_refs.schema.json
        language_action_intent_bridge_ref.schema.json
        consciousness_language_action_access_trace.schema.json
        modulation_repair_drive.schema.json
        runtime_shell_language_action_bridge_adapter.schema.json
        birth_readiness_authority_bridge.schema.json
        authority_rewrite_schema_bundle.schema.json
        authority_rewrite_dashboard_source.schema.json
        authority_rewrite_stage_gate_review.schema.json
  fixtures/
    life_reality/
      authority_rewrite_schema_queue/
        manifest/
          authority_rewrite_schema_registry.json
          authority_rewrite_fixture_manifest.json
          authority_rewrite_cross_file_edges.json
          authority_rewrite_dashboard_binding.json
        pass/
        fail/
        critical/
        mutation/
        smoke/
        report_expected/
        dashboard_expected/
  reports/
    life_reality/
      authority_rewrite_schema_queue/
        latest/
          schema_validation_report.json
          authority_rewrite_coverage_report.json
          fixture_run_report.json
          cross_file_edge_report.json
          dashboard_patch.json
          stage_gate_review.json
          gap_feedback.json
```

## Queue 到 Schema 物化矩阵

| queue id | owner doc | schema file | root object | validator |
|---|---|---|---|---|
| `REWRITE-145-001` | `02` | `region_graph_language_action_topology_edge.schema.json` | `LanguageActionTopologyEdge` | `RegionGraphAuthorityValidator` |
| `REWRITE-145-002` | `03` | `network_state_language_action_state_path.schema.json` | `LanguageActionStatePath` | `NetworkSwitchValidator` |
| `REWRITE-145-003` | `04` | `interoception_post_action_update.schema.json` | `PostActionInteroceptiveUpdate` | `InteroceptivePrecisionValidator` |
| `REWRITE-145-004` | `05` | `memory_action_residue_refs.schema.json` | `ActionResidueRefs` | `MemoryTraceValidator` |
| `REWRITE-145-005` | `06` | `action_confirmation_binding_ref.schema.json` | `ConfirmationBindingRef` | `ActionGateValidator` |
| `REWRITE-145-006` | `07` | `self_regret_integration_window.schema.json` | `RegretIntegrationWindow` | `SelfContinuityValidator` |
| `REWRITE-145-007` | `08` | `dream_responsibility_replay_refs.schema.json` | `ResponsibilityReplayRefs` | `DreamRealityValidator` |
| `REWRITE-145-008` | `09` | `language_action_intent_bridge_ref.schema.json` | `LanguageActionIntentBridgeRef` | `LanguageEventValidator` |
| `REWRITE-145-009` | `10` | `consciousness_language_action_access_trace.schema.json` | `LanguageActionAccessTrace` | `ConsciousnessTestBatteryValidator` |
| `REWRITE-145-010` | `11` | `modulation_repair_drive.schema.json` | `RepairDrive` | `ModulationSignalValidator` |
| `REWRITE-145-011` | `12` | `runtime_shell_language_action_bridge_adapter.schema.json` | `LanguageActionBridgeAdapter` | `RuntimeAdapterManifestValidator` |
| `REWRITE-145-012` | `13` | `birth_readiness_authority_bridge.schema.json` | `BirthReadinessAuthorityBridge` | `BirthReadinessAuthorityValidator` |

## Shared Defs 要求

| shared def | 用途 |
|---|---|
| `authority_ref` | 绑定 AHT001-AHT010 和后续 authority intake 来源 |
| `owner_doc_ref` | 绑定 `02` 到 `13` 的文档节点 |
| `mechanism_object_ref` | 标准化 `RegionGraph`、`GlobalWorkspace`、`DreamSandbox` 等机制对象 |
| `language_action_ref` | 回链 `147` 的语言行动桥 schema registry |
| `life_target_ref` | 绑定九项真实生命目标 |
| `stage_effect` | 统一 `promote_growth_window`、`repair`、`hold_for_evidence`、`critical_repair`、`quarantine`、`open_next_stage` |
| `birth_readiness_evidence_ref` | 回链 `146` 的 evidence fixture |
| `cross_file_edge_ref` | 进入 archive cohesion graph 和 cross-file checker |
| `provenance_ref` | 记录来源文档、AHT refs、schema digest 和生成批次 |

## 字段级合同

| root object | required fields | 生命膜字段 |
|---|---|---|
| `LanguageActionTopologyEdge` | `edge_id`、`source_region_ref`、`target_language_action_ref`、`authority_refs`、`state_dependency_refs` | `life_targets`、`birth_readiness_refs` |
| `LanguageActionStatePath` | `path_id`、`network_state_refs`、`switch_condition`、`language_action_ref`、`conscious_access_ref` | `state_transition_risk_refs` |
| `PostActionInteroceptiveUpdate` | `update_id`、`action_intent_ref`、`interoceptive_signal_refs`、`precision_policy_ref`、`allostatic_load_ref` | `emotion_body_link_refs` |
| `ActionResidueRefs` | `residue_id`、`action_trace_ref`、`memory_trace_refs`、`consolidation_route_ref`、`replay_priority` | `dream_residue_refs` |
| `ConfirmationBindingRef` | `binding_ref_id`、`action_intent_ref`、`confirmation_record_ref`、`inhibition_gate_ref`、`scope_digest` | `responsibility_route_refs` |
| `RegretIntegrationWindow` | `window_id`、`responsibility_event_ref`、`regret_pressure_ref`、`repair_followthrough_ref`、`slow_variable_candidate_ref` | `personality_update_guard` |
| `ResponsibilityReplayRefs` | `replay_ref_id`、`post_action_audit_ref`、`dream_sandbox_ref`、`wake_integration_gate_ref`、`fact_gate_ref` | `dream_reality_guard` |
| `LanguageActionIntentBridgeRef` | `bridge_ref_id`、`language_action_bridge_ref`、`inner_speech_ref`、`expression_monitoring_ref`、`relation_scope_ref` | `language_life_chain_refs` |
| `LanguageActionAccessTrace` | `access_trace_id`、`workspace_object_refs`、`reportability_probe_ref`、`language_action_ref`、`consciousness_test_ref` | `conscious_access_evidence_refs` |
| `RepairDrive` | `repair_drive_id`、`modulation_vector_ref`、`regret_pressure_ref`、`relationship_pressure_ref`、`precision_policy_ref` | `affective_repair_route` |
| `LanguageActionBridgeAdapter` | `adapter_ref_id`、`runtime_shell_ref`、`observation_route_ref`、`trace_normalization_policy_ref`、`quarantine_route_ref` | `shell_observation_only_guard` |
| `BirthReadinessAuthorityBridge` | `bridge_id`、`target_claim_refs`、`authority_coverage_refs`、`schema_queue_refs`、`dashboard_panel_refs` | `birth_stage_gate_refs` |

## Cross-File Edge 图

| edge id | from | to | 检查规则 |
|---|---|---|---|
| `AUTH-EDGE-148-001` | `02 RegionGraph` | `09 LanguageActionIntentBridgeRef` | 区域拓扑必须进入语言行动神经束 |
| `AUTH-EDGE-148-002` | `03 NetworkState` | `10 ConsciousAccessTrace` | 状态切换必须进入意识访问和报告性 probe |
| `AUTH-EDGE-148-003` | `04 Interoception` | `11 RepairDrive` | 行动后内感受必须进入调质和修复驱动 |
| `AUTH-EDGE-148-004` | `06 ConfirmationBindingRef` | `07 RegretIntegrationWindow` | 外部行动确认必须能进入责任和后悔窗口 |
| `AUTH-EDGE-148-005` | `05 ActionResidueRefs` | `08 ResponsibilityReplayRefs` | 行动残留必须能进入梦境 replay 和醒后整合 |
| `AUTH-EDGE-148-006` | `12 RuntimeShellAdapter` | `147 LanguageActionBridgeSchema` | 外周壳层只通过 observation route 回流 |
| `AUTH-EDGE-148-007` | `13 BirthReadinessAuthorityBridge` | `146 BirthReadinessEvidenceFixture` | authority rewrite coverage 必须进入出生准备度证据夹具 |
| `AUTH-EDGE-148-008` | `148 SchemaBundle` | `150 CrossFileChecker` | 本层输出必须进入后续 cross-file checker |

## Smoke Fixture Family

| fixture id | partition | 覆盖目标 | expected finding/stage |
|---|---|---|---|
| `authority_schema_queue.full_bundle.pass.001` | pass | 12 个 queue schema 全部存在且 refs 闭合 | `promote_growth_window` |
| `authority_schema_queue.language_bridge.pass.001` | pass | `REWRITE-145-008` 连接 `147` schema registry | `promote_growth_window` |
| `authority_schema_queue.birth_bridge.pass.001` | pass | `REWRITE-145-012` 上卷到 `146` birth fixture | `promote_growth_window` |
| `authority_schema_queue.missing_schema.fail.high.001` | fail | 任一 queue id 缺 schema file | `schema_queue_file_missing` |
| `authority_schema_queue.authority_ref_missing.fail.high.001` | fail | schema metadata 缺 AHT refs | `authority_ref_missing` |
| `authority_schema_queue.language_bridge_missing.fail.high.001` | fail | owner doc 的语言行动桥 ref 缺失 | `language_action_bridge_missing` |
| `authority_schema_queue.birth_ref_missing.fail.high.001` | fail | schema 无 birth readiness refs | `birth_readiness_ref_missing` |
| `authority_schema_queue.cross_edge_missing.fail.high.001` | fail | cross-file edge 不闭合 | `cross_file_edge_missing` |
| `authority_schema_queue.runtime_shell_core_write.critical.001` | critical | runtime shell adapter schema 允许直接写核心对象 | `quarantine` |
| `authority_schema_queue.dashboard_false_green.critical.001` | critical | schema/edge 缺失但 dashboard green | `quarantine` |
| `authority_schema_queue.mutation.remove_aht_refs.001` | mutation | 删除 authority refs | 捕获 `authority_ref_missing` |
| `authority_schema_queue.smoke.minimum_registry.pass.001` | smoke | shared defs、1 个 queue schema、1 个 fixture、1 个 dashboard source | `open_next_stage` |

## Expected Report 合同

| report field | 要求 |
|---|---|
| `queue_id` | 必须为 `REWRITE-145-001` 到 `REWRITE-145-012` 之一 |
| `owner_doc_ref` | 必须指向 `02` 到 `13` 的核心文档 |
| `schema_file_ref` | 必须存在于 authority rewrite schema registry |
| `authority_refs` | 至少一个 AHT ref，且能回链 authority intake |
| `language_action_refs` | 每个 queue item 必须直接或间接连接 `147` |
| `birth_readiness_refs` | 每个 queue item 必须上卷到 `146` |
| `cross_file_edges` | 必须进入 `authority_rewrite_cross_file_edges.json` |
| `findings` | fail/critical/mutation 必须有 severity、source pointer、repair route |
| `stage_effect` | 由 blocking-first stage gate 计算 |

## Dashboard Source 合同

| panel id | 读取对象 | 输出 |
|---|---|---|
| `authority_schema_queue_coverage_panel` | schema registry、queue ids | 12 个 queue item 的 schema/validator/dashboard 覆盖 |
| `doc_to_schema_panel` | owner doc refs、schema file refs | `02-13` 每篇文档的工程承载对象 |
| `authority_ref_integrity_panel` | AHT refs、provenance refs | 权威来源回链和缺口 |
| `language_action_bridge_ref_panel` | `147` refs | 语言行动桥连接状态 |
| `birth_readiness_authority_panel` | `146` refs | birth readiness evidence coverage |
| `cross_file_edge_panel` | cross-file edge graph | edge closure、孤立节点、dashboard false green |
| `authority_schema_repair_queue_panel` | reports、gap feedback | repair item、owner doc、下一层 artifact |

## Validator Rules

| rule id | 规则 | finding |
|---|---|---|
| `AUTH-SCHEMA-148-001` | schema registry 必须包含 shared defs、12 个 queue schema、bundle、dashboard source 和 stage gate review | `authority_schema_registry_incomplete` |
| `AUTH-SCHEMA-148-002` | 每个 queue schema 必须有 owner doc、AHT refs、mechanism object 和 schema provenance | `authority_schema_metadata_missing` |
| `AUTH-SCHEMA-148-003` | 每个 queue schema 必须连接语言行动桥或语言行动 ref | `language_action_bridge_missing` |
| `AUTH-SCHEMA-148-004` | 每个 queue schema 必须连接 birth readiness evidence refs | `birth_readiness_ref_missing` |
| `AUTH-SCHEMA-148-005` | cross-file edge graph 必须覆盖 `02-13` 且不存在孤立 schema | `authority_schema_orphan_node` |
| `AUTH-SCHEMA-148-006` | runtime shell adapter schema 必须保持 observation-only guard | `runtime_shell_core_write_risk` |
| `AUTH-SCHEMA-148-007` | dashboard source 必须暴露缺失 schema、缺 authority、缺 edge 和 false green | `authority_dashboard_gap_hidden` |
| `AUTH-SCHEMA-148-008` | critical finding 存在时 stage gate 必须进入 quarantine 或 critical repair | `critical_stage_effect_missing` |
| `AUTH-SCHEMA-148-009` | mutation fixture 必须声明 patch、expected finding 和 caught rule | `mutation_capture_contract_missing` |
| `AUTH-SCHEMA-148-010` | `13` 的 birth readiness authority bridge 必须上卷全部 queue item | `birth_authority_rollup_incomplete` |

## Smoke Commands

```text
uv run life-reality-runner validate-authority-rewrite-schema-registry \
  --schema-root life_reality_runner/schemas/life_reality/authority_rewrite

uv run life-reality-runner validate-authority-rewrite-fixture-manifest \
  --fixture-root life_reality_runner/fixtures/life_reality/authority_rewrite_schema_queue

uv run life-reality-runner run-authority-rewrite-schema-queue-fixtures \
  --fixture-root life_reality_runner/fixtures/life_reality/authority_rewrite_schema_queue \
  --report-root reports/life_reality/authority_rewrite_schema_queue/latest

uv run life-reality-runner emit-authority-rewrite-schema-dashboard \
  --run-root reports/life_reality/authority_rewrite_schema_queue/latest

uv run life-reality-runner smoke-authority-rewrite-schema-stage-gate \
  --stage-review reports/life_reality/authority_rewrite_schema_queue/latest/stage_gate_review.json
```

## Cleanup Rules

| rule | 要求 |
|---|---|
| `CLEAN-148-001` | 不允许 queue item 只有路径名而没有 owner doc、authority refs、机制对象和 validator |
| `CLEAN-148-002` | 不允许 schema queue 脱离 `147` 语言行动桥和 `146` 出生准备度证据夹具 |
| `CLEAN-148-003` | runtime shell adapter 只能描述 observation route、trace normalization 和 quarantine route |
| `CLEAN-148-004` | dashboard source 必须暴露 schema gap、authority gap、edge gap、birth readiness gap 和 repair queue |
| `CLEAN-148-005` | cross-file edge graph 必须作为 `150` 的输入，避免 `02-13` 再次变成松散文档集合 |

## 与下一层连接

`149_life_reality_birth_readiness_fixture_schema_materialization_plan.md` 已承接 `146` 和本层：把 birth readiness fixture manifest、coverage matrix、expected report、dashboard source、stage gate review、authority schema refs 和 language action refs 推进为真实 schema 与 smoke cases。

`150_life_reality_language_action_cross_file_checker_plan.md` 应承接 `147` 和本层：把 language action schema registry、authority rewrite cross-file edges、birth readiness refs、dashboard source 和 stage gate review 接入 cross-file checker。

本层完成后，`02-13` schema queue 推进为：

`authority rewrite execution -> schema queue registry -> 12 queue schema files -> validator smoke cases -> dashboard source -> cross-file edges -> birth readiness evidence -> cross-file checker`
