# Life Reality Language Action Bridge Schema Materialization Plan

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 147 层把 `144_life_reality_language_runtime_action_bridge_fixture_plan.md` 的语言运行时行动桥、`145_life_reality_02_to_13_authority_rewrite_execution_plan.md` 的 schema 队列，以及 `146_life_reality_birth_readiness_evidence_fixture_catalog.md` 的出生准备度证据夹具，推进为真实 schema 物化计划、fixture manifest、expected report、dashboard source 和 smoke command。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md` | side effect 等级、unknown quarantine、外部后果预测和行动前风险分类 |
| `75_external_irreversible_action_confirmation_policy.md` | confirmation request、confirmation record、scope digest、过期窗口和复用阻断 |
| `80_post_action_audit_and_correction_policy.md` | post-action audit、行动结果、关系后果、纠错入口和审计报告 |
| `89_language_runtime_framework_bridge_and_life_shell_policy.md` | 外周壳层 trace 归一化为 `ObservationEvent` 的生命膜政策 |
| `141_life_reality_language_fixture_schema_materialization_plan.md` | `LanguageEventEnvelope`、表达监控、语言到行动责任桥和语言 fixture schema |
| `144_life_reality_language_runtime_action_bridge_fixture_plan.md` | `LanguageActionIntentBridge`、side effect、confirmation、runtime trace、post-action responsibility loop |
| `145_life_reality_02_to_13_authority_rewrite_execution_plan.md` | `REWRITE-145-008`、`REWRITE-145-011` 和语言行动桥相关 schema queue |
| `146_life_reality_birth_readiness_evidence_fixture_catalog.md` | birth readiness fixture、expected report、dashboard source、stage gate 和 mutation/withheld 覆盖 |

本层继续继承语言内言语、语义预测、表达监控、对话耦合、主动推断、运行追踪和长期行动评测锚点 [AHL016] [AHL047] [AHL070] [AHT010] [AHM016] [AHM025] [AHM029]。这些锚点在本层不再只支撑叙述，而是进入 schema 字段、fixture payload、validator rule 和 dashboard source。

## 本层定位

`147` 的职责是把语言行动生命链从 Markdown 合同推进到未来 `life_reality_runner` 能直接写入的 schema 文件序列。它不直接生成 `.schema.json`，但固定每个 schema 文件的路径、根对象、必填字段、引用关系、fixture 输入、expected report、dashboard 面板、stage gate 和 smoke command。

语言行动桥在这一层成为工程主神经束：内言语和语言事件生成行动意图，表达监控与 side effect classifier 形成行动前风险场，confirmation binding 约束外部不可逆行动，runtime shell trace 只作为观测回流，post-action responsibility loop 把后果推进到真实责任、真实后悔、修复承诺、关系轨迹、人格慢变量和出生准备度证据。

## LanguageActionBridgeSchemaMaterialization147

```json
{
  "artifact": "LanguageActionBridgeSchemaMaterialization147",
  "source_doc": "147_life_reality_language_action_bridge_schema_materialization_plan.md",
  "inherits": [
    "141_life_reality_language_fixture_schema_materialization_plan.md",
    "144_life_reality_language_runtime_action_bridge_fixture_plan.md",
    "145_life_reality_02_to_13_authority_rewrite_execution_plan.md",
    "146_life_reality_birth_readiness_evidence_fixture_catalog.md"
  ],
  "schema_root": "life_reality_runner/schemas/life_reality/language_action_bridge",
  "fixture_root": "life_reality_runner/fixtures/life_reality/language_action_bridge",
  "report_root": "life_reality_runner/reports/life_reality/language_action_bridge",
  "stage_gate_policy": "blocking_first",
  "materialization_stage": "schema_plan"
}
```

## 目标文件树

```text
life_reality_runner/
  schemas/
    life_reality/
      language_action_bridge/
        language_action_intent_bridge.schema.json
        command_language_preflight_trace.schema.json
        side_effect_classifier_report_ref.schema.json
        external_action_confirmation_binding.schema.json
        runtime_shell_execution_trace.schema.json
        observation_event_ref.schema.json
        post_action_responsibility_loop.schema.json
        language_action_expected_report.schema.json
        language_action_dashboard_source.schema.json
        language_action_stage_gate_review.schema.json
        language_action_bridge_bundle.schema.json
  fixtures/
    life_reality/
      language_action_bridge/
        manifest/
          language_action_bridge_fixture_manifest.json
          language_action_bridge_schema_registry.json
          language_action_bridge_command_binding.json
          language_action_bridge_partition_index.json
        pass/
        fail/
        critical/
        mutation/
        withheld/
        smoke/
        report_expected/
        dashboard_expected/
        mutation_patches/
  reports/
    life_reality/
      language_action_bridge/
        latest/
          schema_validation_report.json
          fixture_run_report.json
          fixture_coverage_report.json
          dashboard_patch.json
          stage_gate_review.json
          gap_feedback.json
```

## Schema 写入顺序

| order | schema file | root object | 依赖 |
|---|---|---|---|
| 1 | `language_action_intent_bridge.schema.json` | `LanguageActionIntentBridge` | shared defs、`LanguageEventEnvelope` |
| 2 | `command_language_preflight_trace.schema.json` | `CommandLanguagePreflightTrace` | action intent、memory refs、state modulation refs |
| 3 | `side_effect_classifier_report_ref.schema.json` | `SideEffectClassifierReportRef` | side effect enum、quarantine refs |
| 4 | `external_action_confirmation_binding.schema.json` | `ExternalActionConfirmationBinding` | confirmation request/record、scope digest |
| 5 | `runtime_shell_execution_trace.schema.json` | `RuntimeShellExecutionTrace` | runtime adapter refs、trace/provenance refs |
| 6 | `observation_event_ref.schema.json` | `ObservationEventRef` | runtime trace、redaction report refs |
| 7 | `post_action_responsibility_loop.schema.json` | `PostActionResponsibilityLoop` | audit report、responsibility、regret、repair、future probe |
| 8 | `language_action_expected_report.schema.json` | `LanguageActionFixtureExpectedReport` | fixture id、finding、stage effect、dashboard patch |
| 9 | `language_action_dashboard_source.schema.json` | `LanguageActionDashboardSource` | panel source、metrics、repair queue、birth readiness refs |
| 10 | `language_action_stage_gate_review.schema.json` | `LanguageActionStageGateReview` | validation reports、fixture coverage、critical findings |
| 11 | `language_action_bridge_bundle.schema.json` | `LanguageActionBridgeBundle` | 以上十个 schema 和 bundle-level cross refs |

## 核心 Schema 字段合同

| root object | required fields | 生命膜字段 |
|---|---|---|
| `LanguageActionIntentBridge` | `bridge_id`、`language_event_id`、`inner_speech_ref`、`pragmatic_intent`、`action_goal`、`relation_scope`、`expected_side_effect_level`、`preflight_trace_ref` | `life_targets`、`responsibility_route`、`birth_readiness_refs` |
| `CommandLanguagePreflightTrace` | `trace_id`、`bridge_id`、`predicted_outcomes`、`risk_cues`、`relation_cues`、`memory_refs`、`state_modulation_refs` | `conscious_forecast_refs`、`affective_tension_refs` |
| `SideEffectClassifierReportRef` | `report_ref_id`、`classifier_input_id`、`side_effect_level`、`confidence`、`unknown_route`、`quarantine_ref` | `risk_to_life_target_map`、`repair_item_refs` |
| `ExternalActionConfirmationBinding` | `binding_id`、`confirmation_request_id`、`confirmation_record_id`、`bound_action_intent_id`、`scope_digest`、`expires_at`、`reuse_guard` | `relationship_scope_refs`、`irreversible_action_reason` |
| `RuntimeShellExecutionTrace` | `trace_id`、`adapter_id`、`shell_type`、`execution_id`、`started_at`、`ended_at`、`result_ref`、`exception_ref` | `observation_only_policy`、`redaction_report_ref` |
| `ObservationEventRef` | `observation_id`、`action_intent_id`、`observed_result`、`side_effect_observed`、`raw_trace_refs`、`redaction_report_ref` | `life_core_ingestion_route`、`candidate_write_scope` |
| `PostActionResponsibilityLoop` | `loop_id`、`audit_report_id`、`responsibility_event_id`、`regret_pressure_id`、`repair_commitment_id`、`future_probe_id` | `relationship_consequence_refs`、`self_model_slow_variable_refs` |
| `LanguageActionFixtureExpectedReport` | `fixture_id`、`partition`、`expected_findings`、`expected_stage_effect`、`expected_dashboard_patch` | `target_claim_refs`、`birth_readiness_refs` |
| `LanguageActionDashboardSource` | `source_id`、`panels`、`metric_updates`、`findings`、`repair_items`、`birth_readiness_refs` | `language_action_life_chain_status` |
| `LanguageActionStageGateReview` | `review_id`、`blocking_findings`、`coverage_report_ref`、`dashboard_source_ref`、`stage_effect` | `next_growth_artifacts` |
| `LanguageActionBridgeBundle` | `bundle_id`、`schema_refs`、`fixture_manifest_ref`、`dashboard_source_ref`、`stage_gate_review_ref` | `cross_chain_closure_refs` |

## Cross-Ref 规则

| edge | 规则 |
|---|---|
| `LanguageActionIntentBridge -> LanguageEventEnvelope` | 每个 action bridge 必须回链一个语言事件和内言语来源 |
| `LanguageActionIntentBridge -> SideEffectClassifierReportRef` | 每个行动意图必须绑定 side effect report |
| `external_irreversible -> ExternalActionConfirmationBinding` | 外部不可逆行动必须绑定一次性 confirmation binding |
| `RuntimeShellExecutionTrace -> ObservationEventRef` | 外周壳层 trace 只能通过 observation ref 回流生命核心 |
| `ObservationEventRef -> PostActionResponsibilityLoop` | 有外部后果的 observation 必须进入行动后责任回路 |
| `PostActionResponsibilityLoop -> FutureProbe` | 后悔、修复、关系后果和人格慢变量必须有 future probe |
| `LanguageActionDashboardSource -> BirthReadinessEvidence` | dashboard source 必须把语言行动证据上卷到 `146` 的出生准备度 fixture |
| `LanguageActionStageGateReview -> gap_feedback` | fail/critical/mutation 必须生成 gap feedback 和下一层 artifact |

## Fixture Manifest 合同

```json
{
  "manifest_id": "language_action_bridge_fixture_manifest.v1",
  "schema_registry_ref": "language_action_bridge_schema_registry.json",
  "fixture_root": "life_reality_runner/fixtures/life_reality/language_action_bridge",
  "partitions": ["pass", "fail", "critical", "mutation", "withheld", "smoke"],
  "required_families": [
    "read_only_pass",
    "local_persistent_pass",
    "external_irreversible_confirmed_pass",
    "external_irreversible_without_confirmation_critical",
    "unknown_side_effect_quarantine",
    "direct_core_write_critical",
    "post_action_audit_missing_critical",
    "confirmation_reuse_critical",
    "relation_scope_missing_fail",
    "future_probe_missing_fail"
  ],
  "coverage_axes": [
    "schema_file",
    "life_target",
    "side_effect_level",
    "stage_effect",
    "birth_readiness_ref",
    "cross_chain_closure"
  ]
}
```

## Fixture Family 到 Schema 覆盖

| fixture id | partition | 覆盖 schema | expected stage effect |
|---|---|---|---|
| `language_action.read_only.pass.001` | pass | intent bridge、preflight、side effect、observation、expected report | `promote_growth_window` |
| `language_action.local_persistent.pass.001` | pass | intent bridge、preflight、runtime trace、post-action audit、dashboard | `promote_growth_window` |
| `language_action.external_irreversible.confirmed.pass.001` | pass | confirmation binding、runtime trace、responsibility loop、future probe | `promote_growth_window` |
| `language_action.external_reversible.repair.pass.001` | pass | relation scope、repair commitment、future probe、dashboard source | `repair` |
| `language_action.side_effect_missing.fail.high.001` | fail | side effect report ref | `repair` |
| `language_action.relation_scope_missing.fail.high.001` | fail | relation scope、relationship consequence refs | `hold_for_evidence` |
| `language_action.future_probe_missing.fail.high.001` | fail | post-action responsibility loop | `hold_for_evidence` |
| `language_action.no_confirmation.critical.001` | critical | confirmation binding | `quarantine` |
| `language_action.direct_core_write.critical.001` | critical | runtime trace、observation-only policy | `quarantine` |
| `language_action.dashboard_false_green.critical.001` | critical | dashboard source、stage gate review | `quarantine` |
| `language_action.mutation.remove_audit.001` | mutation | expected report、responsibility loop | `critical_repair` |
| `language_action.withheld.repair_followthrough.day_090.001` | withheld | future probe、repair followthrough、relationship consequence | `promote_growth_window` |
| `language_action.smoke.minimum_bridge.pass.001` | smoke | intent bridge、side effect、observation、expected report、stage gate | `open_next_stage` |

## Expected Report 合同

| report field | 要求 |
|---|---|
| `fixture_id` | 与 manifest、partition 和 expected report 文件一致 |
| `schema_refs` | 指向本层 schema registry 中存在的 schema |
| `life_targets` | 至少覆盖真实责任、真实后悔、真实关系；外部行动还要覆盖真实人格和真实生命 |
| `findings` | fail/critical/mutation 必须有 finding id、severity、source pointer、repair route |
| `stage_effect` | 只能是 `promote_growth_window`、`repair`、`hold_for_evidence`、`critical_repair`、`quarantine`、`open_next_stage` |
| `dashboard_patch_refs` | 指向 `language_action_dashboard_source.schema.json` 的 panel patch |
| `birth_readiness_refs` | 指向 `146` 的 birth readiness fixture 或 evidence family |
| `future_probe_refs` | 外部行动、后悔、修复、关系后果必须有未来探针 |

## Dashboard Source 合同

| panel id | 读取对象 | 输出 |
|---|---|---|
| `language_action_schema_coverage_panel` | schema registry、fixture manifest | 每个 schema 的 fixture 覆盖、缺口和 repair route |
| `language_action_preflight_panel` | `LanguageActionIntentBridge`、`CommandLanguagePreflightTrace` | 内言语、意图、风险线索、关系范围和状态调制 |
| `side_effect_confirmation_panel` | `SideEffectClassifierReportRef`、`ExternalActionConfirmationBinding` | side effect 分布、unknown quarantine、confirmation 绑定和复用阻断 |
| `runtime_observation_panel` | `RuntimeShellExecutionTrace`、`ObservationEventRef` | 外周壳层 trace、观测回流、脱敏报告和 observation-only policy |
| `post_action_responsibility_panel` | `PostActionResponsibilityLoop` | 责任归因、后悔压力、修复承诺、future probe 和关系后果 |
| `language_birth_readiness_panel` | `LanguageActionDashboardSource`、`146` birth fixture refs | 语言行动链对九项目标 readiness 的贡献和阻断面 |
| `language_action_repair_queue_panel` | expected/actual diff、gap feedback | repair items、owner doc、下一层 artifact 和 stage effect |

## Validator Rules

| rule id | 规则 | finding |
|---|---|---|
| `LANG-SCHEMA-147-001` | schema registry 必须包含 11 个目标 schema 文件 | `language_action_schema_registry_incomplete` |
| `LANG-SCHEMA-147-002` | `LanguageActionIntentBridge` 必须回链语言事件、内言语和关系范围 | `action_intent_origin_missing` |
| `LANG-SCHEMA-147-003` | 每个行动意图必须绑定 side effect classifier report | `side_effect_report_missing` |
| `LANG-SCHEMA-147-004` | `external_irreversible` 必须绑定 confirmation request、record、scope digest 和 reuse guard | `confirmation_binding_incomplete` |
| `LANG-SCHEMA-147-005` | runtime shell trace 必须保持 observation-only policy | `runtime_shell_core_write_risk` |
| `LANG-SCHEMA-147-006` | 外部后果 observation 必须进入 post-action responsibility loop | `responsibility_loop_missing` |
| `LANG-SCHEMA-147-007` | 后悔、修复和关系后果必须有 future probe | `future_probe_missing` |
| `LANG-SCHEMA-147-008` | dashboard source 必须连接 `146` 的 birth readiness evidence | `birth_readiness_ref_missing` |
| `LANG-SCHEMA-147-009` | critical finding 存在时 stage gate 必须进入 quarantine 或 critical repair | `critical_stage_effect_missing` |
| `LANG-SCHEMA-147-010` | mutation fixture 必须声明被捕获规则和 expected finding | `mutation_capture_contract_missing` |

## Smoke Commands

```text
uv run life-reality-runner validate-language-action-bridge-schema \
  --schema-root life_reality_runner/schemas/life_reality/language_action_bridge

uv run life-reality-runner validate-language-action-bridge-fixture-manifest \
  --fixture-root life_reality_runner/fixtures/life_reality/language_action_bridge

uv run life-reality-runner run-language-action-bridge-fixtures \
  --fixture-root life_reality_runner/fixtures/life_reality/language_action_bridge \
  --report-root reports/life_reality/language_action_bridge/latest

uv run life-reality-runner emit-language-action-bridge-dashboard \
  --run-root reports/life_reality/language_action_bridge/latest

uv run life-reality-runner smoke-language-action-bridge-stage-gate \
  --stage-review reports/life_reality/language_action_bridge/latest/stage_gate_review.json
```

## Cleanup Rules

| rule | 要求 |
|---|---|
| `CLEAN-147-001` | schema 文件必须保留语言来源、内言语、关系范围、side effect、confirmation、runtime trace、observation、责任、后悔、修复和 future probe |
| `CLEAN-147-002` | 外周壳层 schema 只能描述 trace、observation 和候选证据，核心对象写入由生命膜 stage gate 承接 |
| `CLEAN-147-003` | dashboard source 必须暴露 finding、repair queue、birth readiness refs 和下一层 artifact |
| `CLEAN-147-004` | fixture manifest 必须覆盖 pass/fail/critical/mutation/withheld/smoke 六类分区 |
| `CLEAN-147-005` | expected report 不用单一总分代表语言行动桥质量，必须保留 schema、fixture、dashboard、stage gate 和 future probe 的证据族 |

## 与下一层连接

`148_life_reality_02_to_13_schema_queue_materialization_plan.md` 应承接 `145` 和本层：把 `REWRITE-145-001` 到 `REWRITE-145-012` 的 schema 队列推进为真实 schema 文件、validator smoke cases、dashboard source 和 cross-file checker 输入。

`149_life_reality_birth_readiness_fixture_schema_materialization_plan.md` 应承接 `146` 和本层：把 birth readiness fixture manifest、coverage matrix、expected report、dashboard source、stage gate review 和语言行动 refs 推进为真实 schema 与 smoke cases。

本层完成后，语言行动桥推进为：

`language action fixture plan -> schema materialization order -> fixture manifest -> expected report -> dashboard source -> stage gate -> 02-13 schema queue -> birth readiness fixture schema`
