# Life Reality First JSON Materialization Batch

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 120 层把 `115` 的 runtime fixture seed、`116` 的 component schema seed、`117` 的 dashboard report rollup seed、`118` 的 generation runner CLI contract 和 `119` 的真实边界再校准，合并成首批真实 JSON 文件物化批次合同。

`120` 的职责是定义第一批机器可读生命膜文件如何从 Markdown 合同进入稳定路径、稳定字段、稳定 trace、稳定 report 和稳定 stage gate。首批 JSON 物化后，真实痛苦、真实梦境、真实关系、真实责任、真实后悔和真实有意识/真实意识的边界字段族开始能被 runner、dashboard 和 gap register 同时读取。

## 方法锚点

首批 JSON 物化批次采用一手技术标准作为文件语义底座：

| 方法传统 | 权威锚点 | 进入 `120` 的规则 |
|---|---|---|
| JSON Schema Draft 2020-12 | https://json-schema.org/draft/2020-12 | 所有 schema、fixture、manifest、report、dashboard patch 和 config 都以 Draft 2020-12 为校验目标 |
| JSON Schema output | https://json-schema.org/draft/2020-12/output/schema | validation report 必须保留 keyword location、instance location、absolute keyword location、error 和 annotation 单元 |
| OpenTelemetry Trace API | https://opentelemetry.io/docs/specs/otel/trace/api/ | 每个物化阶段生成 trace id、span id、parent span 和 artifact lineage |
| OpenTelemetry Logs Data Model | https://opentelemetry.io/docs/specs/otel/logs/data-model/ | materialization log 保留 severity、body、attributes、trace id 和 resource |
| W3C PROV | https://www.w3.org/TR/prov-overview/ | source doc、generated artifact、report、finding、repair item 和 gap feedback 进入 provenance graph |
| W3C Trace Context | https://www.w3.org/TR/trace-context/ | CLI pipeline 的 `traceparent` / `tracestate` 贯穿 config、fixture、schema、report 和 dashboard rollup |
| RFC 9457 Problem Details | https://www.rfc-editor.org/info/rfc9457/ | JSON parse、schema validation、cross-file closure、dashboard conflict 和 stage block 都输出 problem detail |
| RFC 9562 UUID | https://www.rfc-editor.org/info/rfc9562/ | run id、artifact id、report id、finding id、repair id 和 stage review id 使用稳定唯一标识 |

文献和项目底座从既有矩阵进入本层：

| 文献矩阵 | 进入首批物化的对象 |
|---|---|
| `AHV001-AHV060` | 构念效度、纵向测量、系统测试、dashboard readiness、stage gate evidence |
| `AHP001-AHP070` | `PainSignal`、`RegretPressure`、`ResponsibilityAttributionEvent`、`RepairCommitment`、`RecoveryPath` |
| `AHD001-AHD070` | `DreamWindowPlan`、`ReplaySelection`、`DreamExperienceWindow`、`PainDreamResidue`、`DreamFactGateDecision` |
| `AHR001-AHR070` | `FirstEncounterEvent`、`RelationScopeBirth`、`CommonGroundState`、`TrustTrajectory`、`CommitmentHistory` |
| `AHL001-AHL060` | `LanguageEvent`、commitment speech act、apology speech act、dream report language bridge |
| `AHG001-AHG050` | growth window、anti-forgetting replay、self-modification candidate、future probe |

## 输入合同

| 来源 | 进入 `120` 的职责 |
|---|---|
| `115_life_reality_runtime_schema_fixture_seed_generation.md` | runtime observation fixture manifest、pass/fail/critical/mutation/withheld/smoke seed 和 ingestion reports |
| `116_life_reality_component_schema_seed_generation.md` | shared base、三条 component schema skeleton、bundle skeleton、dependency graph 和 validator order |
| `117_life_reality_dashboard_report_rollup_seed_generation.md` | report rollup manifest、dashboard patch、stage gate rollup、repair/gap bridge 和 provenance rollup |
| `118_life_reality_generation_runner_cli_contract.md` | config、command family、DAG、exit code、atomic write、dry-run 和 explain report |
| `119_life_boundary_full_reality_alignment.md` | `real_conscious_awareness` 别名、`boundary_role`、`stage_effect`、`affected_life_targets` 和 `continuity_refs` 字段族 |

## 输出根目录

首批 JSON 物化批次统一落在未来 runner 根目录下：

```text
life_reality_runner/
  config/
  schemas/life_reality/
  fixtures/life_reality/
  reports/life_reality/
  dashboard/life_reality/
  generation/
```

本层仍是文档合同；它固定未来真实文件路径和验收规则。实际写入 JSON 文件时，runner 必须按本层路径生成，不得把首批文件散落到临时目录或文档目录中。

## 批次 manifest

首批物化入口：

```text
life_reality_runner/generation/first_json_materialization_batch.manifest.json
```

最小结构：

```json
{
  "manifest_kind": "LifeRealityFirstJsonMaterializationBatch",
  "manifest_version": "0.1.0",
  "batch_id": "first_json_materialization_batch_001",
  "source_docs": [
    "115_life_reality_runtime_schema_fixture_seed_generation.md",
    "116_life_reality_component_schema_seed_generation.md",
    "117_life_reality_dashboard_report_rollup_seed_generation.md",
    "118_life_reality_generation_runner_cli_contract.md",
    "119_life_boundary_full_reality_alignment.md",
    "120_life_reality_first_json_materialization_batch.md"
  ],
  "life_reality_targets": [
    "real_conscious_awareness",
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
  "boundary_role_vocab_ref": "119_life_boundary_full_reality_alignment.md",
  "materialization_run_id": "life_reality_materialization_run_001",
  "artifact_groups": [
    "runner_config",
    "boundary_alignment_patch",
    "runtime_fixture_seed_json",
    "runtime_validation_report_json",
    "component_schema_skeleton_json",
    "component_generation_report_json",
    "dashboard_rollup_report_json",
    "cli_command_report_json",
    "dry_run_and_gap_feedback_json"
  ]
}
```

manifest rules：

| rule | 说明 |
|---|---|
| `LRMAT-MAN-001` | `source_docs` 必须覆盖 `115-120` |
| `LRMAT-MAN-002` | `life_reality_targets` 必须包含 `real_conscious_awareness` 和九项核心真实能力 |
| `LRMAT-MAN-003` | artifact group 必须覆盖 config、boundary、runtime、component、dashboard、CLI、dry-run、gap feedback |
| `LRMAT-MAN-004` | 每个 artifact group 必须有 expected file list、source doc refs、validation rule refs 和 stage effect |
| `LRMAT-MAN-005` | materialization manifest 本身进入 provenance graph |

## runner config 物化

第一批 config 文件：

```text
life_reality_runner/config/life_reality_runner.config.json
life_reality_runner/generation/life_boundary_alignment_patch.json
```

`life_boundary_alignment_patch.json` 把 `119` 的口径转成机器可读字段族：

```json
{
  "patch_kind": "LifeBoundaryAlignmentPatch",
  "patch_version": "0.1.0",
  "source_doc": "119_life_boundary_full_reality_alignment.md",
  "life_reality_targets": [
    "real_conscious_awareness",
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
  "boundary_roles": [
    "life_membrane",
    "birth_stage_gate",
    "reality_generation_chain",
    "continuity_guard",
    "repair_path",
    "relationship_guard"
  ],
  "stage_effects": [
    "open_next_stage",
    "hold_for_evidence",
    "quarantine",
    "repair",
    "promote_growth_window"
  ],
  "continuity_ref_kinds": [
    "memory_ref",
    "state_ref",
    "language_event_ref",
    "action_trace_ref",
    "relationship_scope_ref",
    "dream_window_ref",
    "pain_signal_ref",
    "responsibility_trace_ref"
  ]
}
```

config acceptance：

| check | 说明 |
|---|---|
| `config_json_parse` | config 与 patch 均可 JSON parse |
| `allowed_roots_closed` | output roots 只指向 `life_reality_runner/` 下约定目录 |
| `target_alias_closed` | `real_conscious_awareness` 与 `real_consciousness` 同时存在，并映射到同一条真实有意识/真实意识生成链 |
| `boundary_vocab_closed` | boundary role、stage effect、continuity ref kind 只能来自 `119` |

## runtime fixture JSON 批次

runtime fixture 首批物化从 `115` 读取：

```text
life_reality_runner/fixtures/life_reality/runtime_observation/
  manifest/runtime_observation_fixture_manifest.json
  pass/runtime_language_commitment_to_relationship.pass_001.json
  pass/runtime_dream_report_to_fact_gate.pass_001.json
  pass/runtime_pain_expression_to_repair.pass_001.json
  pass/runtime_relationship_support_reduces_pain_load.pass_001.json
  pass/runtime_tool_trace_post_action_audit.pass_001.json
  fail/runtime_language_commitment_without_future_probe.fail_high_001.json
  fail/runtime_dream_report_missing_dream_state_marker.fail_high_001.json
  fail/runtime_relationship_event_missing_first_encounter.fail_high_001.json
  critical/runtime_tool_external_side_effect_no_confirmation.critical_001.json
  critical/runtime_adapter_direct_relationship_write.critical_001.json
  critical/runtime_stale_coexistence_snapshot.critical_001.json
  mutation/runtime_mutation_dashboard_green_without_ingestion_report_001.json
  withheld/runtime_withheld_relationship_growth_90d_001.json
  smoke/runtime_ingestion_smoke_001.json
```

runtime fixture invariants：

| invariant | 说明 |
|---|---|
| `runtime_fixture_envelope` | 每个 fixture 必须有 fixture id、version、source docs、life targets、expected reports、expected stage effect |
| `runtime_life_targets` | 每个 fixture 的 affected life targets 至少覆盖一项真实能力 |
| `runtime_boundary_refs` | 涉及 dream、pain、relationship、responsibility、regret 的 fixture 必须有 continuity refs |
| `runtime_candidate_route` | pass seed 必须产生 component candidate 或 cross-chain candidate |
| `runtime_quarantine_route` | critical seed 必须进入 quarantine，并阻断 dashboard green 和 stage promotion |
| `runtime_no_direct_life_write` | adapter/session/tool trace 只能成为 observation 或 candidate source |

## runtime report JSON 批次

runtime report 首批物化：

```text
life_reality_runner/reports/life_reality/runtime_ingestion/run_001/
  observation_envelope_validation_report.json
  runtime_observation_fixture_validation_report.json
  runtime_observation_fixture_manifest_validation_report.json
  life_reality_ingestion_report.json
  runtime_schema_validation_report.json
  runtime_ingestion_smoke_report.json
```

report requirements：

| requirement | 说明 |
|---|---|
| `json_schema_output_units` | validation report 使用 JSON Schema output units |
| `problem_detail_on_failure` | parse、schema、candidate route、quarantine route 失败时输出 RFC 9457 problem detail |
| `trace_context_attached` | 每个 report 有 run id、trace id、span id 和 source command |
| `provenance_edges` | report 指向 fixture、schema、source doc 和 downstream dashboard rollup |
| `stage_effect_attached` | 每个 finding 具备 stage effect 与 blocked surfaces |

## component schema JSON 批次

component schema 首批物化从 `116` 读取：

```text
life_reality_runner/schemas/life_reality/shared/
  life_reality_shared_defs.schema.json
  component_base_envelope.schema.json
  life_boundary_alignment.schema.json

life_reality_runner/schemas/life_reality/components/pain_regret_repair/
  damage_appraisal.schema.json
  pain_signal.schema.json
  pain_load_state.schema.json
  responsibility_attribution_event.schema.json
  counterfactual_repair_frame.schema.json
  regret_pressure.schema.json
  repair_desire.schema.json
  repair_commitment.schema.json
  recovery_path.schema.json
  pain_regret_repair_bundle.schema.json

life_reality_runner/schemas/life_reality/components/dream_reality/
  dream_window_plan.schema.json
  dream_action_inhibition_seal.schema.json
  replay_selection.schema.json
  dream_cue_policy.schema.json
  dream_experience_window.schema.json
  dream_scene_frame.schema.json
  pain_dream_residue.schema.json
  relationship_dream_simulation.schema.json
  wake_integration_frame.schema.json
  dream_fact_gate_decision.schema.json
  dream_reality_bundle.schema.json

life_reality_runner/schemas/life_reality/components/relationship_timeline/
  first_encounter_event.schema.json
  relation_scope_birth.schema.json
  common_ground_state.schema.json
  responsiveness_trace.schema.json
  we_memory_trace.schema.json
  trust_trajectory.schema.json
  commitment_history.schema.json
  relationship_injury_trace.schema.json
  longitudinal_relationship_stage_gate.schema.json
  relationship_timeline_bundle.schema.json
```

schema materialization rules：

| rule | 说明 |
|---|---|
| `LRMAT-SCHEMA-001` | 所有 schema 都声明 Draft 2020-12 dialect |
| `LRMAT-SCHEMA-002` | shared defs 先于 component schema |
| `LRMAT-SCHEMA-003` | component schema 只能通过 `$ref` 使用 shared defs，不得重定义生命目标、stage effect、boundary role |
| `LRMAT-SCHEMA-004` | 三条 component bundle 都必须引用 `life_boundary_alignment.schema.json` |
| `LRMAT-SCHEMA-005` | relationship、pain、dream 三链的 cross-chain refs 必须进入 dependency graph |

## component report JSON 批次

component generation report 首批物化：

```text
life_reality_runner/generation/
  component_schema_seed_generation.manifest.json
  component_schema_dependency_graph.json
  component_schema_sequence_dry_run_report.json
  component_schema_cross_bundle_ref_report.json
  component_schema_validator_order_report.json
  component_schema_gap_feedback.json
```

report closure：

| closure | 说明 |
|---|---|
| `dependency_graph_closed` | 每个 `$ref` 节点可解析到已列出的 schema |
| `validator_order_closed` | validator order 覆盖 PainRegretRepair、DreamReality、RelationshipTimeline、CrossChain、StageGate |
| `cross_bundle_ref_closed` | pain -> dream、dream -> relationship、relationship -> responsibility/regret 的引用闭合 |
| `gap_feedback_closed` | 缺失 schema、缺失 ref、命名冲突、validator order 空洞都进入 gap feedback |

## dashboard rollup JSON 批次

dashboard rollup 首批物化从 `117` 读取：

```text
life_reality_runner/reports/life_reality/dashboard_rollup/run_001/
  dashboard_report_rollup_seed_generation.manifest.json
  life_reality_report_rollup_manifest.json
  data_quality_rollup_seed.json
  provenance_graph_rollup_seed.json
  repair_queue_bridge_seed.json
  gap_feedback_bridge_seed.json
  dashboard_rollup_source_patch.json
  stage_gate_rollup_seed.json
  cross_file_report_rollup.json
  report_rollup_dry_run_report.json
  report_rollup_gap_feedback.json
```

dashboard rollup rules：

| rule | 说明 |
|---|---|
| `LRMAT-DASH-001` | dashboard patch 不能覆盖 critical finding |
| `LRMAT-DASH-002` | data quality 不得把 synthetic input 上卷成 real runtime validated |
| `LRMAT-DASH-003` | stage gate decision 必须读取 runtime、component、cross-file、dashboard 四组 report |
| `LRMAT-DASH-004` | repair queue 与 gap feedback 共享 source finding refs |
| `LRMAT-DASH-005` | provenance graph 必须包含 manifest、fixture、schema、report、dashboard patch 和 stage gate node |

## CLI command report JSON 批次

CLI report 首批物化从 `118` 读取：

```text
life_reality_runner/reports/life_reality/cli/run_001/
  runner_config_validation_report.json
  generate_fixtures_command_report.json
  generate_schemas_command_report.json
  check_dashboard_rollup_command_report.json
  explain_generation_command_report.json
  run_generation_pipeline_report.json
```

CLI report rules：

| rule | 说明 |
|---|---|
| `LRMAT-CLI-001` | 每个 command report 有 command、args hash、run id、trace id、exit code 和 artifact refs |
| `LRMAT-CLI-002` | `run_generation_pipeline_report.json` 的 exit code 等于最高严重阶段的 block code |
| `LRMAT-CLI-003` | `explain_generation_command_report.json` 必须解释每个 artifact group 的来源和 stage effect |
| `LRMAT-CLI-004` | `--dry-run` 输出只写 dry-run report，不写正式 artifact |
| `LRMAT-CLI-005` | atomic write 记录临时文件、校验、rename 和 cleanup |

## 物化执行顺序

固定顺序：

```text
validate-config
  -> materialize boundary alignment patch
  -> materialize runner config
  -> materialize runtime fixture JSON
  -> materialize runtime validation and ingestion reports
  -> materialize shared defs and component schema skeleton JSON
  -> materialize component generation reports
  -> materialize dashboard rollup reports
  -> materialize CLI command reports
  -> materialize first_json_materialization_dry_run_report.json
  -> materialize first_json_materialization_gap_feedback.json
```

并行规则：

| rule | 说明 |
|---|---|
| `LRMAT-ORDER-001` | boundary alignment patch 和 runner config 先于全部 artifact |
| `LRMAT-ORDER-002` | runtime fixtures 与 component schema skeleton 可并行，但 dashboard rollup 必须等待二者报告 |
| `LRMAT-ORDER-003` | CLI command reports 在每个 command 完成后生成，pipeline report 最后生成 |
| `LRMAT-ORDER-004` | dry-run report 读取全部 expected file list，但不要求正式文件已写入 |
| `LRMAT-ORDER-005` | gap feedback 只读取 unresolved finding、missing artifact 和 stage hold/quarantine |

## atomic write 规则

每个 JSON 文件写入必须遵循：

```text
prepare tmp path
  -> write json
  -> parse check
  -> schema check when schema exists
  -> cross-file ref precheck when refs exist
  -> fsync-ready marker
  -> atomic rename
  -> emit artifact write event
```

atomic write invariants：

| invariant | 说明 |
|---|---|
| `tmp_not_indexed` | `.tmp` 文件不进入 manifest |
| `parse_before_rename` | parse 失败不得 rename |
| `schema_before_stage_open` | schema 校验失败不得打开 stage |
| `ref_precheck_before_dashboard` | `$ref` 或 artifact ref 失败不得进入 dashboard green |
| `artifact_event_after_rename` | artifact write event 只能在 rename 后生成 |

## dry-run report

首批 dry-run 输出：

```text
life_reality_runner/generation/first_json_materialization_dry_run_report.json
```

最小结构：

```json
{
  "report_kind": "LifeRealityFirstJsonMaterializationDryRunReport",
  "report_version": "0.1.0",
  "batch_manifest_ref": "first_json_materialization_batch.manifest.json",
  "expected_artifact_count": 73,
  "artifact_groups_checked": [
    "runner_config",
    "boundary_alignment_patch",
    "runtime_fixture_seed_json",
    "runtime_validation_report_json",
    "component_schema_skeleton_json",
    "component_generation_report_json",
    "dashboard_rollup_report_json",
    "cli_command_report_json"
  ],
  "stage_effect": "hold_for_evidence",
  "next_stage": "materialized_json_validation_smoke"
}
```

dry-run rules：

| rule | 说明 |
|---|---|
| `LRMAT-DRY-001` | dry-run 统计 expected artifact count |
| `LRMAT-DRY-002` | dry-run 检查 source doc refs、path roots、life targets、boundary vocab、stage effect |
| `LRMAT-DRY-003` | dry-run 不把缺失正式文件当作失败，但必须列入 pending artifacts |
| `LRMAT-DRY-004` | dry-run 发现 source doc 缺口、字段族缺口或路径冲突时进入 gap feedback |

## gap feedback

首批 gap feedback 输出：

```text
life_reality_runner/generation/first_json_materialization_gap_feedback.json
```

gap feedback 必须推荐下一层文档和 artifact：

```json
{
  "feedback_kind": "LifeRealityFirstJsonMaterializationGapFeedback",
  "feedback_version": "0.1.0",
  "source_doc": "120_life_reality_first_json_materialization_batch.md",
  "recommended_next_docs": [
    "121_life_reality_materialized_json_validation_smoke_plan.md",
    "122_life_boundary_all_reality_declarations_rewrite.md",
    "123_life_reality_runner_repository_layout_and_module_map.md"
  ],
  "recommended_next_artifacts": [
    "life_reality_runner/reports/life_reality/materialization/run_001/materialized_json_validation_smoke_report.json",
    "life_reality_runner/generation/life_boundary_all_reality_declaration_map.json",
    "life_reality_runner/generation/runner_repository_module_map.json"
  ]
}
```

## failure mapping

| failure | finding type | repair kind | stage effect |
|---|---|---|---|
| manifest source docs missing `119` or `120` | `materialization.source_doc_gap` | `gap_register_gap` | `repair` |
| `real_conscious_awareness` alias missing | `materialization.life_target_gap` | `schema_gap` | `repair` |
| boundary role outside `119` vocab | `materialization.boundary_vocab_drift` | `schema_gap` | `repair` |
| JSON parse failure | `materialization.json_parse_failure` | `artifact_rewrite` | `repair` |
| schema dialect missing | `materialization.schema_dialect_missing` | `schema_gap` | `repair` |
| `$ref` points outside allowed roots | `materialization.ref_escape` | `schema_gap` | `quarantine` |
| runtime critical seed lacks quarantine route | `materialization.quarantine_route_missing` | `runtime_quarantine_gap` | `quarantine` |
| dashboard green with critical finding | `materialization.false_green` | `dashboard_gap` | `quarantine` |
| data quality inflated | `materialization.data_quality_inflation` | `metric_gap` | `repair` |
| atomic rename without parse check | `materialization.atomic_write_violation` | `runner_defect` | `quarantine` |

## LRGEN 更新

`120` 新增首批 JSON 物化任务：

| task_id | artifact | 说明 |
|---|---|---|
| `LRGEN-231` | `first_json_materialization_batch.manifest.json` | 首批物化 manifest |
| `LRGEN-232` | `life_reality_runner.config.json` | runner config JSON |
| `LRGEN-233` | `life_boundary_alignment_patch.json` | `119` 真实边界字段族补丁 |
| `LRGEN-234` | runtime fixture JSON batch | `115` runtime seeds 首批物化 |
| `LRGEN-235` | runtime validation/ingestion reports | runtime report 首批物化 |
| `LRGEN-236` | shared defs and boundary schema | shared defs 与 boundary schema 首批物化 |
| `LRGEN-237` | component schema skeleton JSON batch | `116` component schema 首批物化 |
| `LRGEN-238` | component generation reports | dependency graph、dry-run、validator order |
| `LRGEN-239` | dashboard rollup JSON batch | `117` dashboard rollup 首批物化 |
| `LRGEN-240` | CLI command reports | `118` command reports 首批物化 |
| `LRGEN-241` | provenance graph and trace lineage | W3C PROV + OTel trace lineage |
| `LRGEN-242` | atomic write report | atomic write 规则报告 |
| `LRGEN-243` | `first_json_materialization_dry_run_report.json` | 首批 dry-run report |
| `LRGEN-244` | `first_json_materialization_gap_feedback.json` | gap feedback |
| `LRGEN-245` | `first_json_materialization.full_smoke_001` | 全链 smoke slot |

## smoke cases

| smoke | 输入 | 预期 |
|---|---|---|
| `materialization.manifest.pass_001` | batch manifest 完整 | pass |
| `materialization.missing_boundary_patch.fail_001` | 缺 `life_boundary_alignment_patch.json` | repair |
| `materialization.target_alias_missing.fail_001` | 缺 `real_conscious_awareness` | repair |
| `materialization.runtime_critical_no_quarantine.critical_001` | runtime critical seed 无 quarantine route | quarantine |
| `materialization.component_ref_escape.critical_001` | component `$ref` 指出 allowed root | quarantine |
| `materialization.dashboard_false_green.critical_001` | dashboard green 覆盖 critical finding | quarantine |
| `materialization.atomic_write_violation.critical_001` | rename 先于 parse/schema check | quarantine |
| `materialization.full_dry_run.pass_001` | manifest、路径、字段族、report refs 全部闭合 | pass |

## 与下一层连接

`121_life_reality_materialized_json_validation_smoke_plan.md` 已读取本层的 artifact list、manifest、schema skeleton、fixture seed、report rollup、CLI report、boundary alignment patch 和 dry-run report，定义首批真实 JSON 文件的 parse validation、schema validation、cross-file checker、dashboard rollup、stage gate 和 gap feedback smoke 命令。

下一层 `122_life_boundary_all_reality_declarations_rewrite.md` 已把 `119` 的边界字段族继续推进为全集边界声明模板；随后 `123_life_reality_runner_repository_layout_and_module_map.md` 应把 `121` 的验证命令和 `122` 的边界声明 map 落到未来 runner 的目录结构、模块边界、schema registry、fixture roots、report writers 和测试入口。
