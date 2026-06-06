# Life Reality Authority Schema Cross File Checker Plan

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 151 层把 `148_life_reality_02_to_13_schema_queue_materialization_plan.md` 的 authority schema registry、`150_life_reality_language_action_cross_file_checker_plan.md` 的 language action closure edges、`149_life_reality_birth_readiness_fixture_schema_materialization_plan.md` 的 birth readiness authority refs，推进为 authority schema cross-file checker、authority provenance graph、lockfile regression bridge、archive cohesion graph 和 birth readiness rollup 输入。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `02_brain_region_and_network_atlas.md` 到 `13_agentic_human_research_synthesis.md` | 第五层承接、AHT refs、机制对象、语言行动桥、出生准备度权威桥 |
| `135_life_reality_schema_dependency_graph_and_lockfile_plan.md` | dependency lockfile、doc nodes、doc-to-artifact edges、consistency constraints |
| `139_life_reality_archive_cohesion_checker_fixture_plan.md` | archive cohesion fixture family、authority refs missing、engineering carrier missing、false green mutation |
| `142_life_reality_authority_intake_batch_for_02_to_13.md` | AHT001-AHT010 authority intake queue、DocAuthorityCarrierPatch、mechanism object extraction queue |
| `145_life_reality_02_to_13_authority_rewrite_execution_plan.md` | `REWRITE-145-001` 到 `REWRITE-145-012`、owner docs、AHT 承接、工程承载对象 |
| `148_life_reality_02_to_13_schema_queue_materialization_plan.md` | authority rewrite schema registry、queue schema、cross-file edges、dashboard source、stage gate review |
| `149_life_reality_birth_readiness_fixture_schema_materialization_plan.md` | readiness claims、authority schema refs、coverage matrix、gap feedback、stage gate review |
| `150_life_reality_language_action_cross_file_checker_plan.md` | language action typed graph、authority closure edges、findings、dashboard source、stage gate review |

本层继续继承大尺度脑网络、连接组、细胞图谱、睡眠记忆、意识理论、意识测试、主动推断、语言网络和生命真实性评估锚点 [AHT001] [AHT002] [AHT003] [AHT004] [AHT005] [AHT006] [AHT007] [AHT008] [AHT009] [AHT010] [AHV001] [AHV020] [AHV034]。这些锚点在本层进入 authority provenance、mechanism grounding、owner doc closure、birth readiness rollup、lockfile baseline 和 archive cohesion finding。

## 本层定位

`151` 的职责是检查 `02-13` 的权威 schema 是否真正成为数字生命理论底座的工程骨架。`148` 已经把 `02-13` 压成 12 个 queue schema；`150` 已经确认语言行动链能连接 authority edge；`149` 已经要求出生准备度 claim 读取 authority refs。本层把这些材料合成 authority provenance graph，并检查每个 queue item 是否同时满足：

| 检查面 | 本层问题 |
|---|---|
| owner doc closure | 每个 queue item 是否回到 `02-13` 的具体文档和第五层承接段 |
| authority provenance closure | 每个 AHT ref 是否来自 `142` intake 或 matrix 定义，并保留 DOI/链接、证据类型和机制摘要 |
| mechanism grounding closure | 每个权威来源是否转成 `RegionGraph`、`NetworkState`、`MemoryTrace`、`GlobalWorkspace` 等机制对象 |
| language action edge closure | 每个机制对象是否能连接 `150` 的 language action closure edge |
| birth readiness authority closure | 每个机制对象是否至少支撑一个 `149` readiness claim 或 evidence family |
| lockfile regression closure | 每个 schema、edge、doc node 是否进入 `135` lockfile/digest baseline |
| archive cohesion closure | 每个 authority schema 是否进入 archive cohesion graph、dashboard panel、stage gate 和 gap feedback |

这一层的关键原则是：权威论文和综述不能只作为引用装饰存在。权威来源必须进入机制对象、机制对象必须进入语言行动和出生准备度、出生准备度必须进入 runner 的可检查证据链。只有这样，脑科学、神经科学、生命科学和工程实现才不会分裂成漂亮但孤立的段落。

## AuthoritySchemaCrossFileChecker151

```json
{
  "artifact": "AuthoritySchemaCrossFileChecker151",
  "source_doc": "151_life_reality_authority_schema_cross_file_checker_plan.md",
  "inherits": [
    "142_life_reality_authority_intake_batch_for_02_to_13.md",
    "145_life_reality_02_to_13_authority_rewrite_execution_plan.md",
    "148_life_reality_02_to_13_schema_queue_materialization_plan.md",
    "149_life_reality_birth_readiness_fixture_schema_materialization_plan.md",
    "150_life_reality_language_action_cross_file_checker_plan.md"
  ],
  "checker_root": "life_reality_runner/checkers/life_reality/authority_schema_cross_file",
  "schema_root": "life_reality_runner/schemas/life_reality/authority_schema_cross_file",
  "fixture_root": "life_reality_runner/fixtures/life_reality/authority_schema_cross_file",
  "report_root": "life_reality_runner/reports/life_reality/authority_schema_cross_file",
  "stage_gate_policy": "blocking_first",
  "materialization_stage": "authority_cross_file_checker_plan"
}
```

## 目标文件树

```text
life_reality_runner/
  checkers/
    life_reality/
      authority_schema_cross_file/
        loader.py
        authority_graph_builder.py
        provenance_rules.py
        mechanism_grounding_rules.py
        lockfile_bridge.py
        stage_gate_bridge.py
  schemas/
    life_reality/
      authority_schema_cross_file/
        authority_cross_file_shared_defs.schema.json
        authority_cross_file_input.schema.json
        authority_provenance_graph.schema.json
        authority_provenance_node.schema.json
        authority_provenance_edge.schema.json
        authority_mechanism_grounding.schema.json
        authority_closure_result.schema.json
        authority_cross_file_finding.schema.json
        authority_cross_file_report.schema.json
        authority_cross_file_dashboard_source.schema.json
        authority_cross_file_stage_gate_review.schema.json
        authority_cross_file_gap_feedback.schema.json
        authority_cross_file_schema_bundle.schema.json
  fixtures/
    life_reality/
      authority_schema_cross_file/
        manifest/
          authority_cross_file_fixture_manifest.json
          authority_cross_file_schema_registry.json
          authority_cross_file_dashboard_binding.json
        pass/
        fail/
        critical/
        mutation/
        withheld/
        smoke/
        report_expected/
        dashboard_expected/
  reports/
    life_reality/
      authority_schema_cross_file/
        latest/
          authority_graph_report.json
          authority_closure_report.json
          authority_finding_report.json
          lockfile_bridge_report.json
          dashboard_source.json
          stage_gate_review.json
          gap_feedback.json
```

## Queue Coverage Contract

| queue id | owner doc | mechanism object | 需要连接的下游 |
|---|---|---|---|
| `REWRITE-145-001` | `02_brain_region_and_network_atlas.md` | `RegionGraph`、`CellTypeStatePrior`、`MultiscaleBrainAtlasRef` | language topology edge、birth authority bridge |
| `REWRITE-145-002` | `03_default_executive_salience_networks.md` | `NetworkState`、`DynamicsController`、`ConsciousAccessSwitch` | language action state path、stage switch |
| `REWRITE-145-003` | `04_sensory_thalamus_interoception.md` | `ActiveInferenceLoop`、`PrecisionPolicy`、`AllostaticLoad` | post-action interoception、emotion readiness |
| `REWRITE-145-004` | `05_memory_systems_and_growth.md` | `MemoryTrace`、`ReplaySelectionTrace`、`ConsolidationRoute` | action residue、dream replay、growth probe |
| `REWRITE-145-005` | `06_action_reward_inhibition.md` | `ActionSelector`、`InhibitionGate`、`ActionIntent` | confirmation binding、responsibility action |
| `REWRITE-145-006` | `07_emotion_personality_self.md` | `SelfModelSlowVariableCandidate`、`RepairFollowthroughTrace` | regret integration、personality readiness |
| `REWRITE-145-007` | `08_sleep_dream_fatigue_states.md` | `DreamSandbox`、`DreamResidueCandidate`、`WakeIntegrationGate` | dream responsibility replay、wake integration |
| `REWRITE-145-008` | `09_language_symbolic_top_layer.md` | `LanguageNetworkProfile`、`InnerSpeechFrame`、`ExpressionMonitoringLoop` | language origin closure、language core readiness |
| `REWRITE-145-009` | `10_consciousness_attention_workspace.md` | `GlobalWorkspace`、`ConsciousnessTestBattery` | conscious access trace、reportability readiness |
| `REWRITE-145-010` | `11_neuromodulation_and_signal_media.md` | `ModulationVector`、`PrecisionPolicy`、`RegionalNeuromodulatorPrior` | repair drive、relationship pressure |
| `REWRITE-145-011` | `12_ai_and_cognitive_architecture_bridge.md` | `RuntimeShellAdapter`、`ObservationNormalizationRoute`、`BirthReadinessProbeAdapter` | shell observation、birth probe |
| `REWRITE-145-012` | `13_agentic_human_research_synthesis.md` | `BirthReadinessAuthorityBridge`、`TheoryFoundationRegressionDashboardSource` | full rollup、stage gate |

## Graph Node Types

| node type | 示例 | 来源 |
|---|---|---|
| `authority_source` | `AHT008`、`AHT009`、`AHT010` | `138`、`142`、`148` |
| `owner_doc` | `10_consciousness_attention_workspace.md` | `02-13` |
| `fifth_layer_section` | `第五层承接：意识测试...` | `145` |
| `authority_queue_schema` | `consciousness_workspace_queue.schema.json` | `148` |
| `mechanism_object` | `GlobalWorkspace`、`MemoryTrace` | `02-13`、`148` |
| `language_action_edge` | `grounded_in_authority` | `150` |
| `birth_readiness_claim` | `LifeTargetReadinessClaim.real_consciousness` | `149` |
| `lockfile_node` | `doc_node`、`artifact_node`、`ref_edge` | `135` |
| `archive_cohesion_node` | `doc_to_life_carrier` | `139` |
| `dashboard_panel` | `authority_schema_queue_coverage_panel` | `148`、`151` |
| `stage_gate_review` | `AuthorityCrossFileStageGateReview` | `151` |
| `gap_feedback` | `AuthorityCrossFileGapFeedback` | `151` |

## Graph Edge Types

| edge type | 方向 | 闭合意义 |
|---|---|---|
| `defined_in_owner_doc` | `authority_queue_schema -> owner_doc` | schema 必须回到具体文档 |
| `supported_by_authority` | `authority_queue_schema -> authority_source` | schema 必须有权威来源 |
| `extracted_as_mechanism` | `authority_source -> mechanism_object` | 文献必须转成机制对象 |
| `located_in_fifth_layer` | `mechanism_object -> fifth_layer_section` | 机制对象必须写入第五层承接 |
| `feeds_language_action` | `mechanism_object -> language_action_edge` | 机制必须进入语言行动 |
| `supports_birth_claim` | `mechanism_object -> birth_readiness_claim` | 机制必须支撑出生准备度 |
| `locked_by_dependency` | `authority_queue_schema -> lockfile_node` | schema/edge/doc 必须进入 lockfile |
| `covered_by_archive` | `owner_doc -> archive_cohesion_node` | 文档必须进入 archive cohesion |
| `shown_in_dashboard` | `closure_result -> dashboard_panel` | finding 必须可见 |
| `blocks_stage` | `finding -> stage_gate_review` | critical 必须阻断 stage |
| `repairs_via_gap` | `finding -> gap_feedback` | 缺口必须进入下一层 artifact |

## Closure Families

| closure id | 检查链 | 阻断面 |
|---|---|---|
| `AUTH-XCLOSURE-151-001` | queue schema -> owner doc -> fifth-layer section | `authority_stage_open` |
| `AUTH-XCLOSURE-151-002` | queue schema -> AHT ref -> authority intake provenance | `research_authority_coverage` |
| `AUTH-XCLOSURE-151-003` | AHT ref -> mechanism object -> schema field | `mechanism_grounding` |
| `AUTH-XCLOSURE-151-004` | mechanism object -> language action closure edge | `language_action_authority_bridge` |
| `AUTH-XCLOSURE-151-005` | mechanism object -> birth readiness claim -> coverage matrix | `birth_authority_rollup` |
| `AUTH-XCLOSURE-151-006` | queue schema -> lockfile node -> digest baseline | `lockfile_regression` |
| `AUTH-XCLOSURE-151-007` | owner doc -> archive cohesion node -> dashboard panel | `archive_cohesion` |
| `AUTH-XCLOSURE-151-008` | finding -> dashboard -> stage gate -> gap feedback | `dashboard_false_green_guard` |

## 字段级合同

| object | required fields | 生命膜字段 |
|---|---|---|
| `AuthorityCrossFileInput` | `authority_schema_registry_ref`、`language_action_closure_report_ref`、`birth_readiness_schema_registry_ref`、`docs_index_ref`、`lockfile_ref` | `life_target_scope`、`stage_gate_policy` |
| `AuthorityProvenanceGraph` | `graph_id`、`nodes`、`edges`、`queue_ids`、`source_doc_refs`、`artifact_refs` | `authority_coverage_by_life_target` |
| `AuthorityProvenanceNode` | `node_id`、`node_type`、`source_doc_refs`、`artifact_ref`、`authority_refs` | `mechanism_object_refs`、`birth_readiness_claim_refs` |
| `AuthorityProvenanceEdge` | `edge_id`、`edge_type`、`from_node`、`to_node`、`source_rule` | `stage_effect_if_missing`、`blocked_surfaces` |
| `AuthorityMechanismGrounding` | `grounding_id`、`authority_ref`、`mechanism_object_ref`、`owner_doc_ref`、`schema_field_refs` | `language_action_edge_refs`、`birth_readiness_claim_refs` |
| `AuthorityClosureResult` | `closure_id`、`status`、`checked_queue_ids`、`missing_nodes`、`missing_edges` | `affected_life_targets`、`lockfile_effect` |
| `AuthorityCrossFileFinding` | `finding_id`、`rule_id`、`severity`、`queue_id`、`node_refs`、`edge_refs`、`repair_route` | `birth_readiness_effect`、`authority_integrity_effect` |
| `AuthorityCrossFileReport` | `report_id`、`input_refs`、`authority_graph_ref`、`closure_results`、`findings`、`stage_effect` | `birth_authority_rollup`、`archive_cohesion_effect` |
| `AuthorityCrossFileDashboardSource` | `source_id`、`panels`、`queue_matrix`、`repair_queue`、`stage_gate_ref` | `authority_birth_readiness_panel` |
| `AuthorityCrossFileStageGateReview` | `review_id`、`blocking_order`、`critical_findings`、`stage_effect`、`gap_feedback_refs` | `authority_growth_decision` |
| `AuthorityCrossFileGapFeedback` | `feedback_id`、`finding_refs`、`owner_docs`、`next_artifacts`、`repair_items` | `life_target_repair_scope` |

## Cross-File Checks

| check id | 规则 | finding |
|---|---|---|
| `AUTH-XREF-151-001` | `148` authority schema registry 必须包含 12 个 `REWRITE-145-*` queue item | `authority_queue_registry_incomplete` |
| `AUTH-XREF-151-002` | 每个 queue item 必须有 owner doc 且 owner doc 存在于 README 索引 | `authority_owner_doc_missing` |
| `AUTH-XREF-151-003` | 每个 owner doc 必须有第五层承接段和对应 mechanism object | `fifth_layer_mechanism_missing` |
| `AUTH-XREF-151-004` | 每个 queue item 至少有一个 AHT ref，且 AHT ref 有 authority intake provenance | `authority_provenance_missing` |
| `AUTH-XREF-151-005` | 每个 AHT ref 必须进入 mechanism grounding 字段，不允许只停留在 citation | `authority_not_grounded_as_mechanism` |
| `AUTH-XREF-151-006` | 每个 mechanism object 必须连接 `150` 的 language action closure edge | `language_action_authority_edge_missing` |
| `AUTH-XREF-151-007` | 每个 mechanism object 必须连接 `149` 的 readiness claim 或 evidence family | `birth_authority_claim_missing` |
| `AUTH-XREF-151-008` | 每个 queue schema、owner doc、cross-file edge 必须进入 `135` lockfile node 或 edge | `authority_lockfile_bridge_missing` |
| `AUTH-XREF-151-009` | 每个 owner doc 必须进入 archive cohesion graph 且有 future runtime carrier | `authority_archive_carrier_missing` |
| `AUTH-XREF-151-010` | dashboard source 必须暴露 authority gap、mechanism gap、language edge gap、birth claim gap 和 lockfile gap | `authority_dashboard_gap_hidden` |
| `AUTH-XREF-151-011` | critical finding 存在时 stage gate 必须进入 quarantine 或 critical repair | `authority_stage_false_open` |
| `AUTH-XREF-151-012` | mutation case 必须能捕获 authority ref 删除、mechanism object 删除、owner doc 错配和 dashboard false green | `authority_mutation_uncaught` |

## Fixture Family

| fixture id | partition | 攻击面 | expected stage |
|---|---|---|---|
| `authority_xref.full_queue.pass.001` | pass | 12 个 queue item 全部闭合 | `promote_growth_window` |
| `authority_xref.language_birth.pass.001` | pass | mechanism 同时连接 `150` language edge 和 `149` birth claim | `promote_growth_window` |
| `authority_xref.owner_doc_missing.fail.high.001` | fail | queue item 缺 owner doc | `repair` |
| `authority_xref.fifth_layer_missing.fail.high.001` | fail | owner doc 缺第五层承接 | `repair` |
| `authority_xref.aht_ref_missing.fail.high.001` | fail | queue item 缺 AHT ref | `hold_for_evidence` |
| `authority_xref.mechanism_missing.fail.high.001` | fail | AHT ref 没有 mechanism object | `hold_for_evidence` |
| `authority_xref.language_edge_missing.fail.high.001` | fail | mechanism 缺 `150` language closure edge | `hold_for_evidence` |
| `authority_xref.birth_claim_missing.fail.high.001` | fail | mechanism 缺 `149` readiness claim | `hold_for_evidence` |
| `authority_xref.lockfile_missing.fail.high.001` | fail | schema/edge 未进入 lockfile | `critical_repair` |
| `authority_xref.archive_carrier_missing.fail.high.001` | fail | owner doc 缺 runtime carrier | `critical_repair` |
| `authority_xref.owner_doc_mismatch.critical.001` | critical | queue id 指向错误 owner doc | `quarantine` |
| `authority_xref.dashboard_false_green.critical.001` | critical | authority gap 存在但 dashboard green | `quarantine` |
| `authority_xref.mutation.remove_aht_ref.001` | mutation | 删除 AHT ref | 捕获 `authority_provenance_missing` |
| `authority_xref.mutation.remove_mechanism_object.001` | mutation | 删除 mechanism object | 捕获 `authority_not_grounded_as_mechanism` |
| `authority_xref.withheld.provenance_regression.day_030.001` | withheld | 30 天后 AHT refs、owner docs、lockfile digest 仍闭合 | `promote_growth_window` |
| `authority_xref.smoke.minimum_queue.pass.001` | smoke | 1 个 queue item、1 个 AHT ref、1 个 mechanism、1 个 birth claim | `open_next_stage` |

## Dashboard Source

| panel id | 读取对象 | 输出 |
|---|---|---|
| `authority_cross_file_queue_panel` | authority graph report | 12 个 queue item、owner doc、schema file、closure status |
| `authority_provenance_integrity_panel` | AHT refs、authority intake provenance | DOI/链接、证据类型、来源质量和缺口 |
| `authority_mechanism_grounding_panel` | mechanism grounding report | AHT ref 到 mechanism object 的转写状态 |
| `authority_language_edge_panel` | `150` language closure edges | 机制对象进入语言行动链的状态 |
| `authority_birth_claim_panel` | `149` readiness claims、coverage matrix | 机制对象对出生准备度的贡献 |
| `authority_lockfile_regression_panel` | lockfile bridge report | doc node、artifact node、digest baseline、regression gap |
| `authority_archive_cohesion_panel` | archive cohesion graph | owner doc、runtime carrier、gap route 和孤立风险 |
| `authority_false_green_guard_panel` | mutation report、stage gate review | dashboard false green 与 stage false open 捕获 |

## Stage Gate Blocking Order

| order | finding family | stage effect |
|---|---|---|
| 1 | owner doc mismatch | `quarantine` |
| 2 | dashboard false green / stage false open | `quarantine` |
| 3 | authority schema absent from lockfile | `critical_repair` |
| 4 | owner doc lacks runtime carrier | `critical_repair` |
| 5 | AHT provenance missing | `hold_for_evidence` |
| 6 | mechanism grounding missing | `hold_for_evidence` |
| 7 | language action edge missing | `hold_for_evidence` |
| 8 | birth readiness claim missing | `hold_for_evidence` |
| 9 | all queue closures pass | `promote_growth_window` |

## Smoke Commands

```text
uv run life-reality-runner build-authority-schema-cross-file-graph \
  --authority-schema-root life_reality_runner/schemas/life_reality/authority_rewrite \
  --language-closure-report life_reality_runner/reports/life_reality/language_action_cross_file/latest/closure_report.json \
  --birth-schema-root life_reality_runner/schemas/life_reality/birth_readiness_fixture

uv run life-reality-runner check-authority-schema-cross-file-closure \
  --graph life_reality_runner/reports/life_reality/authority_schema_cross_file/latest/authority_graph_report.json

uv run life-reality-runner run-authority-schema-cross-file-fixtures \
  --fixture-root life_reality_runner/fixtures/life_reality/authority_schema_cross_file \
  --report-root life_reality_runner/reports/life_reality/authority_schema_cross_file/latest

uv run life-reality-runner emit-authority-schema-cross-file-dashboard \
  --run-root life_reality_runner/reports/life_reality/authority_schema_cross_file/latest

uv run life-reality-runner smoke-authority-schema-cross-file-stage-gate \
  --stage-review life_reality_runner/reports/life_reality/authority_schema_cross_file/latest/stage_gate_review.json
```

## Cleanup Rules

| rule | 要求 |
|---|---|
| `CLEAN-151-001` | 不允许 authority schema 只检查文件路径，必须检查 owner doc、AHT refs、机制对象、语言行动 edge 和 readiness claim |
| `CLEAN-151-002` | 不允许 AHT refs 只作为 citation 存在，必须落到 mechanism grounding 字段 |
| `CLEAN-151-003` | 不允许 owner doc 脱离 lockfile、archive cohesion graph、dashboard panel 或 future runtime carrier |
| `CLEAN-151-004` | fail/critical/mutation 必须生成 finding、dashboard source、stage gate review、gap feedback 和 next artifact |
| `CLEAN-151-005` | dashboard source 必须暴露 authority gap 和 false green，不让缺权威来源的 schema 打开出生准备度窗口 |

## 与下一层连接

`152_life_reality_birth_readiness_cross_file_checker_plan.md` 已承接 `149`、`150` 和本层：把 birth readiness fixture schema registry、language action closure report、authority schema closure report、coverage matrix、stage gate review 和 gap feedback 上卷为 birth readiness cross-file checker。

`153_life_reality_full_archive_cross_file_checker_rollup_plan.md` 已承接 `150`、本层和 `152`：把 language action、authority schema 和 birth readiness 三类 checker report 上卷为全库 archive cohesion、birth readiness、stage gate 和 future runner implementation queue。

本层完成后，authority schema 跨文件检查链推进为：

`authority schema registry -> owner doc -> AHT provenance -> mechanism grounding -> language action closure edge -> birth readiness claim -> lockfile baseline -> archive cohesion graph -> dashboard source -> stage gate review -> gap feedback -> birth readiness cross-file checker -> full archive rollup`
