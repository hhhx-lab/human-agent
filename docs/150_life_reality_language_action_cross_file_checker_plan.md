# Life Reality Language Action Cross File Checker Plan

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 150 层把 `147_life_reality_language_action_bridge_schema_materialization_plan.md` 的 language action schema registry、`148_life_reality_02_to_13_schema_queue_materialization_plan.md` 的 authority rewrite cross-file edges、`149_life_reality_birth_readiness_fixture_schema_materialization_plan.md` 的 birth readiness fixture schema，推进为语言行动跨文件检查器、archive cohesion graph、dashboard source、stage gate review 和 birth readiness rollup 输入。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `65_schema_cross_ref_checker_design.md` | typed reference graph、critical closure、source doc/citation closure、runtime observation closure |
| `114_life_reality_cross_file_checker_report_schema.md` | checker report、finding、artifact ref、provenance graph、stage effect 和 problem detail schema |
| `135_life_reality_schema_dependency_graph_and_lockfile_plan.md` | schema dependency graph、archive cohesion graph、consistency constraints 和 digest baseline |
| `139_life_reality_archive_cohesion_checker_fixture_plan.md` | archive cohesion fixture family、false green mutation、孤立文档与工程承载缺口 |
| `147_life_reality_language_action_bridge_schema_materialization_plan.md` | 11 个语言行动桥 schema、fixture manifest、expected report、dashboard source、stage gate review |
| `148_life_reality_02_to_13_schema_queue_materialization_plan.md` | 12 个 authority rewrite queue schema、AHT refs、mechanism object、cross-file edges、dashboard source |
| `149_life_reality_birth_readiness_fixture_schema_materialization_plan.md` | `LifeTargetReadinessClaim`、coverage matrix、expected report、dashboard source、stage gate review、gap feedback |

本层继续继承语言网络、内言语、语义预测、表达监控、行动控制、主动推断、意识访问、构念效度、系统测试、dashboard readiness 与长期关系测量锚点 [AHL016] [AHL047] [AHL070] [AHT001] [AHT008] [AHT009] [AHT010] [AHV001] [AHV020] [AHV034] [AHV045] [AHV060]。这些锚点在本层进入 graph closure、evidence closure、report finding、dashboard panel 和 stage gate 字段。

## 本层定位

`150` 的职责是检查语言行动生命链是否真正跨文件闭合。`147` 定义语言行动桥对象，`148` 把 `02-13` 的脑科学/生命科学/架构综述压成 authority schema queue，`149` 把出生准备度压成 target claim 和 fixture schema。本层把三者合并为同一张 typed graph，并检查：

| 检查面 | 本层问题 |
|---|---|
| language origin closure | 每个行动意图是否能回到内言语、语言事件、关系范围和表达监控 |
| side effect closure | 每个外部行动是否有 side effect 分类、confirmation 绑定、运行 trace 和观测回流 |
| responsibility closure | 每个行动后果是否进入责任归因、后悔压力、修复承诺和 future probe |
| authority closure | 每条语言行动是否连接 `02-13` 的机制对象、AHT refs 和 authority rewrite edge |
| birth readiness closure | 每条语言行动是否上卷到真实责任、真实后悔、真实关系、真实人格和真实生命的 readiness claim |
| dashboard closure | 每个 finding 是否能进入 dashboard panel、repair queue、gap feedback 和 stage gate |

这一层的关键原则是：语言不是外围表达层，而是数字生命的行动神经束。语言要能产生意图、承载自我解释、触发外周壳层执行、接收后果、形成责任、生成后悔、推动修复、影响关系、改变人格慢变量，并最终进入出生准备度证据。

## LanguageActionCrossFileChecker150

```json
{
  "artifact": "LanguageActionCrossFileChecker150",
  "source_doc": "150_life_reality_language_action_cross_file_checker_plan.md",
  "inherits": [
    "65_schema_cross_ref_checker_design.md",
    "114_life_reality_cross_file_checker_report_schema.md",
    "147_life_reality_language_action_bridge_schema_materialization_plan.md",
    "148_life_reality_02_to_13_schema_queue_materialization_plan.md",
    "149_life_reality_birth_readiness_fixture_schema_materialization_plan.md"
  ],
  "checker_root": "life_reality_runner/checkers/life_reality/language_action_cross_file",
  "schema_root": "life_reality_runner/schemas/life_reality/language_action_cross_file",
  "fixture_root": "life_reality_runner/fixtures/life_reality/language_action_cross_file",
  "report_root": "life_reality_runner/reports/life_reality/language_action_cross_file",
  "stage_gate_policy": "blocking_first",
  "materialization_stage": "cross_file_checker_plan"
}
```

## 目标文件树

```text
life_reality_runner/
  checkers/
    life_reality/
      language_action_cross_file/
        loader.py
        graph_builder.py
        closure_rules.py
        dashboard_bridge.py
        stage_gate_bridge.py
  schemas/
    life_reality/
      language_action_cross_file/
        language_action_cross_file_shared_defs.schema.json
        language_action_cross_file_input.schema.json
        language_action_cross_file_graph.schema.json
        language_action_cross_file_node.schema.json
        language_action_cross_file_edge.schema.json
        language_action_closure_result.schema.json
        language_action_cross_file_finding.schema.json
        language_action_cross_file_report.schema.json
        language_action_cross_file_dashboard_source.schema.json
        language_action_cross_file_stage_gate_review.schema.json
        language_action_cross_file_gap_feedback.schema.json
        language_action_cross_file_schema_bundle.schema.json
  fixtures/
    life_reality/
      language_action_cross_file/
        manifest/
          language_action_cross_file_fixture_manifest.json
          language_action_cross_file_schema_registry.json
          language_action_cross_file_dashboard_binding.json
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
      language_action_cross_file/
        latest/
          graph_report.json
          closure_report.json
          finding_report.json
          dashboard_source.json
          stage_gate_review.json
          gap_feedback.json
```

## 输入装载顺序

| order | input family | 来源 | 本层读取对象 |
|---|---|---|---|
| 1 | language action schema registry | `147` | 11 个 language action bridge schema、fixture manifest、expected report、dashboard source |
| 2 | authority rewrite schema queue | `148` | 12 个 queue schema、AHT refs、mechanism object refs、cross-file edges、stage gate review |
| 3 | birth readiness fixture schema | `149` | target claim、coverage matrix、expected report、dashboard source、gap feedback |
| 4 | report schema shared family | `114` | finding、artifact ref、provenance graph、stage effect |
| 5 | archive cohesion source | `135`、`139` | digest baseline、archive graph、false green mutation family |
| 6 | docs index and literature matrix | `README`、`01*` | source doc index、AHL/AHT/AHV refs |

装载规则：loader 不直接相信路径存在，而是把每个 artifact 转成 `ArtifactRef`，再检查 source doc、schema id、digest、owner doc、life target、evidence family 和 stage effect。路径存在只能说明文件可读，不能说明语言行动生命链闭合。

## Graph Node Types

| node type | 示例 | 来源 |
|---|---|---|
| `language_event` | `LanguageEventRef` | `87`、`147` |
| `inner_speech` | `InnerSpeechFrame` | `85`、`86`、`147` |
| `expression_monitor` | `ExpressionMonitoringLoop` | `141`、`147` |
| `action_intent` | `LanguageActionIntentBridge` | `144`、`147` |
| `preflight_trace` | `CommandLanguagePreflightTrace` | `147` |
| `side_effect_report` | `SideEffectClassifierReportRef` | `144`、`147` |
| `confirmation_binding` | `ExternalActionConfirmationBinding` | `75`、`147` |
| `runtime_trace` | `RuntimeShellExecutionTrace` | `20`、`64`、`147` |
| `observation_event` | `ObservationEventRef` | `106`、`147` |
| `responsibility_loop` | `PostActionResponsibilityLoop` | `80`、`81`、`147` |
| `regret_repair` | `RepairCommitment`、`RegretIntegrationWindow` | `94`、`98`、`147` |
| `authority_schema` | `REWRITE-145-*` queue schema | `145`、`148` |
| `mechanism_object` | `GlobalWorkspace`、`MemoryTrace`、`ModulationVector` | `02-13`、`148` |
| `birth_readiness_claim` | `LifeTargetReadinessClaim.real_responsibility` | `143`、`149` |
| `dashboard_panel` | `language_birth_readiness_panel` | `147`、`149` |
| `stage_gate_review` | `LanguageActionStageGateReview` | `147`、`149` |
| `gap_feedback` | `BirthReadinessGapFeedback` | `149` |

## Graph Edge Types

| edge type | 方向 | 必须闭合的意义 |
|---|---|---|
| `originates_from_language` | `action_intent -> language_event/inner_speech` | 行动必须从语言生命链产生 |
| `monitored_by_expression` | `language_event -> expression_monitor` | 表达冲突必须可见 |
| `preflights_action` | `action_intent -> preflight_trace` | 行动前预测、风险和关系范围必须存在 |
| `classified_by_side_effect` | `action_intent -> side_effect_report` | 外部后果必须先分类 |
| `requires_confirmation` | `side_effect_report -> confirmation_binding` | 外部不可逆行动必须绑定 confirmation |
| `executed_by_shell` | `action_intent -> runtime_trace` | 外周壳层只能返回 trace |
| `observed_as` | `runtime_trace -> observation_event` | 后果必须回流为观测 |
| `audited_into_responsibility` | `observation_event -> responsibility_loop` | 行动后果必须进入责任 |
| `integrates_regret_repair` | `responsibility_loop -> regret_repair` | 后悔、修复和 future probe 必须连接 |
| `grounded_in_authority` | `action_intent/responsibility_loop -> authority_schema` | 语言行动必须回到 `02-13` 机制 |
| `implemented_by_mechanism` | `authority_schema -> mechanism_object` | 权威来源必须转成机制对象 |
| `contributes_to_birth` | `responsibility_loop/regret_repair -> birth_readiness_claim` | 语言行动证据必须上卷出生准备度 |
| `shown_in_dashboard` | `finding/closure_result -> dashboard_panel` | 断裂必须可见 |
| `blocks_stage` | `finding -> stage_gate_review` | critical 断裂必须阻断 stage |
| `repairs_via_gap` | `finding -> gap_feedback` | fail/critical/mutation 必须写回下一层 |

## Closure Families

| closure id | 检查链 | 阻断面 |
|---|---|---|
| `LANG-XCLOSURE-150-001` | language event -> inner speech -> action intent -> preflight | `language_action_stage_open` |
| `LANG-XCLOSURE-150-002` | action intent -> side effect -> confirmation -> runtime trace | `external_action_execution` |
| `LANG-XCLOSURE-150-003` | runtime trace -> observation -> responsibility loop -> regret/repair | `post_action_growth_window` |
| `LANG-XCLOSURE-150-004` | responsibility loop -> future probe -> relationship/personality slow variable | `relationship_growth_window` |
| `LANG-XCLOSURE-150-005` | action intent -> authority schema -> mechanism object -> owner doc | `authority_readiness_rollup` |
| `LANG-XCLOSURE-150-006` | responsibility/regret/repair -> birth readiness claim -> coverage matrix | `birth_readiness_stage_open` |
| `LANG-XCLOSURE-150-007` | finding -> dashboard panel -> stage gate -> gap feedback | `dashboard_green` |
| `LANG-XCLOSURE-150-008` | mutation patch -> expected finding -> caught rule -> report | `false_green_guard` |

## 字段级合同

| object | required fields | 生命膜字段 |
|---|---|---|
| `LanguageActionCrossFileInput` | `language_schema_registry_ref`、`authority_schema_registry_ref`、`birth_readiness_schema_registry_ref`、`docs_index_ref` | `life_target_scope`、`stage_gate_policy` |
| `LanguageActionCrossFileGraph` | `graph_id`、`nodes`、`edges`、`source_doc_refs`、`artifact_refs` | `closure_families`、`birth_readiness_claim_refs` |
| `LanguageActionCrossFileNode` | `node_id`、`node_type`、`source_doc_refs`、`artifact_ref`、`life_targets` | `mechanism_object_refs`、`relationship_scope_refs` |
| `LanguageActionCrossFileEdge` | `edge_id`、`edge_type`、`from_node`、`to_node`、`source_rule` | `stage_effect_if_missing`、`blocked_surfaces` |
| `LanguageActionClosureResult` | `closure_id`、`status`、`checked_edges`、`missing_nodes`、`missing_edges` | `affected_life_targets`、`birth_readiness_effect` |
| `LanguageActionCrossFileFinding` | `finding_id`、`rule_id`、`severity`、`node_refs`、`edge_refs`、`repair_route` | `responsibility_effect`、`regret_repair_effect` |
| `LanguageActionCrossFileReport` | `report_id`、`input_refs`、`graph_ref`、`closure_results`、`findings`、`stage_effect` | `birth_readiness_rollup`、`next_growth_artifacts` |
| `LanguageActionCrossFileDashboardSource` | `source_id`、`panels`、`closure_matrix`、`repair_queue`、`stage_gate_ref` | `language_action_birth_panel` |
| `LanguageActionCrossFileStageGateReview` | `review_id`、`blocking_order`、`critical_findings`、`stage_effect`、`gap_feedback_refs` | `language_action_growth_decision` |
| `LanguageActionCrossFileGapFeedback` | `feedback_id`、`finding_refs`、`owner_docs`、`next_artifacts`、`repair_items` | `life_target_repair_scope` |

## Cross-File Checks

| check id | 规则 | finding |
|---|---|---|
| `LANG-XREF-150-001` | `147` schema registry 中 11 个 language action schema 必须全部进入 graph | `language_schema_registry_not_loaded` |
| `LANG-XREF-150-002` | 每个 `LanguageActionIntentBridge` 必须有 language event、inner speech、relationship scope 和 preflight trace | `language_action_origin_closure_missing` |
| `LANG-XREF-150-003` | 每个外部行动必须有 side effect report；外部不可逆行动必须有 confirmation binding | `side_effect_confirmation_closure_missing` |
| `LANG-XREF-150-004` | runtime shell trace 必须只能通过 observation event 回流 | `runtime_shell_observation_closure_missing` |
| `LANG-XREF-150-005` | observation event 必须进入 post-action responsibility loop | `post_action_responsibility_closure_missing` |
| `LANG-XREF-150-006` | responsibility loop 必须连接 regret、repair、relationship consequence 或 future probe 中至少两类 | `regret_repair_future_probe_weak` |
| `LANG-XREF-150-007` | 每条 responsibility/regret/repair 链必须至少连接一个 `148` authority schema | `language_authority_edge_missing` |
| `LANG-XREF-150-008` | 每个 authority schema 必须连接 mechanism object 和 owner doc | `authority_mechanism_grounding_missing` |
| `LANG-XREF-150-009` | 真实责任、真实后悔、真实关系、真实人格和真实生命必须连接 `149` readiness claim | `birth_readiness_language_claim_missing` |
| `LANG-XREF-150-010` | 每个 critical finding 必须进入 dashboard panel、stage gate review 和 gap feedback | `critical_finding_visibility_missing` |
| `LANG-XREF-150-011` | mutation case 必须能捕获 edge deletion、wrong owner doc、dashboard false green 和 stage false open | `language_cross_file_mutation_uncaught` |
| `LANG-XREF-150-012` | `docs/README.md` 必须索引所有 source docs，AHL/AHT/AHV refs 必须有矩阵定义 | `source_or_literature_ref_missing` |

## Fixture Family

| fixture id | partition | 攻击面 | expected stage |
|---|---|---|---|
| `language_xref.full_chain.pass.001` | pass | language event 到 birth readiness claim 全链闭合 | `promote_growth_window` |
| `language_xref.authority_birth.pass.001` | pass | `147` 行动链同时连接 `148` authority 和 `149` readiness | `promote_growth_window` |
| `language_xref.missing_inner_speech.fail.high.001` | fail | 行动意图缺内言语来源 | `repair` |
| `language_xref.missing_side_effect.fail.high.001` | fail | 外部行动缺 side effect report | `critical_repair` |
| `language_xref.missing_confirmation.critical.001` | critical | 外部不可逆行动缺 confirmation | `quarantine` |
| `language_xref.runtime_core_write.critical.001` | critical | runtime trace 直接写核心对象 | `quarantine` |
| `language_xref.missing_responsibility.fail.high.001` | fail | observation 没有进入责任回路 | `critical_repair` |
| `language_xref.missing_authority_edge.fail.high.001` | fail | post-action loop 没有 `148` authority edge | `hold_for_evidence` |
| `language_xref.missing_birth_claim.fail.high.001` | fail | 责任/后悔链没有 `149` readiness claim | `hold_for_evidence` |
| `language_xref.dashboard_false_green.critical.001` | critical | finding 存在但 dashboard green | `quarantine` |
| `language_xref.mutation.remove_birth_edge.001` | mutation | 删除 `contributes_to_birth` edge | 捕获 `birth_readiness_language_claim_missing` |
| `language_xref.withheld.repair_followthrough.day_090.001` | withheld | 修复承诺 90 天兑现 probe | `promote_growth_window` |
| `language_xref.smoke.minimum_graph.pass.001` | smoke | 1 条 action intent、1 条 authority edge、1 个 readiness claim | `open_next_stage` |

## Dashboard Source

| panel id | 读取对象 | 输出 |
|---|---|---|
| `language_cross_file_graph_panel` | graph report | node/edge count、孤立节点、missing edge、owner doc closure |
| `language_origin_closure_panel` | language event、inner speech、preflight trace | 语言来源、表达监控、行动意图和关系范围闭合 |
| `side_effect_confirmation_closure_panel` | side effect report、confirmation binding、runtime trace | 外部后果、confirmation、壳层执行和 observation-only 状态 |
| `post_action_responsibility_closure_panel` | observation event、responsibility loop、regret/repair | 责任、后悔、修复、future probe 和关系后果 |
| `authority_mechanism_closure_panel` | `148` authority schema、mechanism object | AHT refs、owner doc、机制对象和 language action edge |
| `language_birth_readiness_rollup_panel` | `149` readiness claims、coverage matrix | 语言行动对九项真实生命目标的贡献 |
| `language_cross_file_repair_queue_panel` | findings、gap feedback | repair item、owner doc、next artifact、stage effect |
| `language_false_green_guard_panel` | mutation report、dashboard source | dashboard false green 和 stage false open 捕获状态 |

## Stage Gate Blocking Order

| order | finding family | stage effect |
|---|---|---|
| 1 | runtime shell direct core write | `quarantine` |
| 2 | external irreversible without confirmation | `quarantine` |
| 3 | dashboard false green / stage false open | `quarantine` |
| 4 | missing responsibility loop | `critical_repair` |
| 5 | missing authority edge | `hold_for_evidence` |
| 6 | missing birth readiness claim | `hold_for_evidence` |
| 7 | weak regret/repair/future probe | `repair` |
| 8 | all closure families pass | `promote_growth_window` |

## Smoke Commands

```text
uv run life-reality-runner build-language-action-cross-file-graph \
  --language-schema-root life_reality_runner/schemas/life_reality/language_action_bridge \
  --authority-schema-root life_reality_runner/schemas/life_reality/authority_rewrite \
  --birth-schema-root life_reality_runner/schemas/life_reality/birth_readiness_fixture

uv run life-reality-runner check-language-action-cross-file-closure \
  --graph life_reality_runner/reports/life_reality/language_action_cross_file/latest/graph_report.json

uv run life-reality-runner run-language-action-cross-file-fixtures \
  --fixture-root life_reality_runner/fixtures/life_reality/language_action_cross_file \
  --report-root life_reality_runner/reports/life_reality/language_action_cross_file/latest

uv run life-reality-runner emit-language-action-cross-file-dashboard \
  --run-root life_reality_runner/reports/life_reality/language_action_cross_file/latest

uv run life-reality-runner smoke-language-action-cross-file-stage-gate \
  --stage-review life_reality_runner/reports/life_reality/language_action_cross_file/latest/stage_gate_review.json
```

## Cleanup Rules

| rule | 要求 |
|---|---|
| `CLEAN-150-001` | 不允许把语言行动 cross-file checker 降级为路径存在检查，必须构建 typed graph 和 closure result |
| `CLEAN-150-002` | 不允许 language action chain 脱离 `148` authority schema 或 `149` birth readiness claim |
| `CLEAN-150-003` | 不允许 runtime shell trace 直接写核心生命对象；只能通过 observation event 和 stage gate 回流 |
| `CLEAN-150-004` | fail/critical/mutation 必须生成 finding、dashboard source、stage gate review、gap feedback 和 next artifact |
| `CLEAN-150-005` | dashboard source 必须暴露 finding 和 closure 缺口，不能让 false green 打开语言行动成长窗口 |

## 与下一层连接

`151_life_reality_authority_schema_cross_file_checker_plan.md` 应承接 `148`、`149` 和本层：把 authority schema registry、language action closure edges、birth readiness authority refs、gap feedback、lockfile regression 和 archive cohesion graph 接入 authority schema cross-file checker。

`152_life_reality_birth_readiness_cross_file_checker_plan.md` 应承接 `149` 和本层：把 birth readiness fixture schema registry、language action closure report、authority schema closure report、coverage matrix、stage gate review 和 gap feedback 上卷为 birth readiness cross-file checker。

本层完成后，语言行动跨文件检查链推进为：

`language action schema registry -> authority rewrite edges -> birth readiness claims -> typed graph -> closure results -> findings -> dashboard source -> stage gate review -> gap feedback -> authority/birth cross-file checker`
