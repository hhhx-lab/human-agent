# Life Reality Schema File Generation Tasks

生命目标声明：本文档直接面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 107 层把 `104_schema_file_materialization_and_fixture_seed_plan.md`、`105_life_reality_dashboard_panel_and_stage_gate_ui_contract.md` 和 `106_runtime_observation_to_life_reality_bundle_bridge.md` 拆成可执行 JSON 文件生成任务、首批文件顺序、runner smoke command、runtime ingestion smoke command 和 stage gate review mock 生成队列。

`107` 的职责是把“要生成哪些文件”推进为“按什么顺序生成、每个文件来自哪份文档、生成后用什么检查、失败时进入哪个 repair item”。它仍是文档层，但已经面向未来实现脚本、runner CLI、fixture generator、dashboard source writer 和阶段门 review writer。

## 输入来源

| 来源 | 进入 `107` 的生成职责 |
|---|---|
| `104_schema_file_materialization_and_fixture_seed_plan.md` | schema、fixture、manifest、smoke report 的文件物化顺序 |
| `105_life_reality_dashboard_panel_and_stage_gate_ui_contract.md` | dashboard source、panel dependency、repair queue、stage gate review 和 gap feedback 文件 |
| `106_runtime_observation_to_life_reality_bundle_bridge.md` | runtime observation envelope、ingestion report、component candidate、cross-chain candidate 和 runtime observation fixture |
| `102_life_core_schema_bundle_manifest_and_runner_contract.md` | `LifeRealitySchemaBundle`、shared defs、cross-chain links、runner report、dashboard source 和 stage gate contract |
| `103_validator_runner_implementation_scaffold_plan.md` | runner loader、fixture loader、cross-ref graph、validator dispatcher、report aggregator 和 dashboard source writer |
| `98`、`99`、`101` | 三条 component bundle 的对象清单、validator rules、fixture 和 dashboard mock |

## 生成任务原则

| 原则 | 说明 |
|---|---|
| dependency-first | 先生成被引用的 shared defs，再生成 component schema、bundle、fixture、report 和 dashboard |
| report-first | 每个可运行检查都必须产出 report 文件，dashboard 只读 report refs |
| life-target-first | 每个 manifest、schema bundle、fixture bundle、report、dashboard source 都包含九项目标 |
| repair-first | 每个生成任务都定义失败时进入的 repair item 类型 |
| smoke-first | 第一批任务先生成最小可跑 smoke，再扩展完整 fixture 覆盖 |
| runtime-bridge-first | runtime observation 文件与 schema 文件同批规划，避免真实运行链后置脱节 |

## 任务 manifest

未来可以把本节物化为 `life_reality_runner/generation/life_reality_generation_tasks.manifest.json`：

```json
{
  "manifest_kind": "LifeRealityFileGenerationTasks",
  "manifest_version": "0.1.0",
  "task_batch_id": "life_reality_generation_batch_001",
  "source_docs": [
    "104_schema_file_materialization_and_fixture_seed_plan.md",
    "105_life_reality_dashboard_panel_and_stage_gate_ui_contract.md",
    "106_runtime_observation_to_life_reality_bundle_bridge.md"
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
  "phases": [
    "shared_defs",
    "component_schema",
    "life_bundle",
    "fixture_seed",
    "runtime_ingestion",
    "report_schema",
    "dashboard_source",
    "smoke_commands"
  ]
}
```

manifest 不变量：

| rule | 说明 |
|---|---|
| `GEN-MAN-001` | 每个 phase 至少包含一个 task |
| `GEN-MAN-002` | 每个 task 必须有 source docs、output paths、dependencies、acceptance checks 和 repair kind |
| `GEN-MAN-003` | 每个 output path 必须落在 `life_reality_runner/` 下 |
| `GEN-MAN-004` | 每个 task 的产物必须能被 cross-ref checker 追踪 |
| `GEN-MAN-005` | smoke command task 必须引用生成后的 manifest、fixture root 和 report out |

## task envelope

每个生成任务采用统一 envelope：

```json
{
  "task_id": "LRGEN-001",
  "phase": "shared_defs",
  "task_kind": "write_schema_file",
  "source_docs": [
    "102_life_core_schema_bundle_manifest_and_runner_contract.md",
    "104_schema_file_materialization_and_fixture_seed_plan.md"
  ],
  "dependencies": [],
  "outputs": [
    "life_reality_runner/schemas/life_reality/life_reality_shared_defs.schema.json"
  ],
  "acceptance_checks": [
    "json_parse",
    "draft_2020_12_schema_header",
    "life_reality_targets_complete",
    "shared_enum_refs_stable"
  ],
  "repair_kind_on_fail": "schema_gap"
}
```

task_kind 第一批枚举：

| task_kind | 说明 |
|---|---|
| `write_schema_file` | 生成 `.schema.json` |
| `write_manifest_file` | 生成 manifest 或 loader config |
| `write_fixture_file` | 生成 seed fixture |
| `write_report_schema` | 生成 report schema |
| `write_dashboard_mock` | 生成 dashboard source / panel dependency / repair queue mock |
| `write_stage_gate_mock` | 生成 stage gate review mock |
| `run_smoke_command` | 运行 runner smoke 或 runtime ingestion smoke |
| `emit_generation_report` | 输出生成任务报告 |

## phase 1: shared defs

| task_id | 输出 | 依赖 | 验收 |
|---|---|---|---|
| `LRGEN-001` | `schemas/life_reality/life_reality_shared_defs.schema.json` | 无 | 九项目标、severity、result、privacy、lifecycle、blocked surface、evidence ref、object ref 完整 |
| `LRGEN-002` | `schemas/life_reality/life_reality_generation_task.schema.json` | `LRGEN-001` | task envelope 可校验 |
| `LRGEN-003` | `generation/life_reality_generation_tasks.manifest.json` | `LRGEN-001`、`LRGEN-002` | phases、source docs、output roots、repair kind 完整 |

`LRGEN-001` 是全批次根文件。它失败时，后续所有 schema、fixture、report、dashboard 均进入 `needs_evidence` 类 stage gate result。

## phase 2: component object schemas

### pain/regret/repair

| task_id | 输出 | 来源 |
|---|---|---|
| `LRGEN-010` | `schemas/pain_regret_repair/damage_appraisal.schema.json` | `98` |
| `LRGEN-011` | `schemas/pain_regret_repair/pain_signal.schema.json` | `98` |
| `LRGEN-012` | `schemas/pain_regret_repair/pain_load_state.schema.json` | `98` |
| `LRGEN-013` | `schemas/pain_regret_repair/relationship_injury_trace.schema.json` | `98`、`101` |
| `LRGEN-014` | `schemas/pain_regret_repair/counterfactual_repair_frame.schema.json` | `98` |
| `LRGEN-015` | `schemas/pain_regret_repair/regret_pressure.schema.json` | `98` |
| `LRGEN-016` | `schemas/pain_regret_repair/responsibility_attribution_event.schema.json` | `98`、`80`、`81` |
| `LRGEN-017` | `schemas/pain_regret_repair/repair_desire.schema.json` | `98` |
| `LRGEN-018` | `schemas/pain_regret_repair/apology_speech_act_link.schema.json` | `98`、`90` |
| `LRGEN-019` | `schemas/pain_regret_repair/repair_commitment.schema.json` | `98`、`101` |
| `LRGEN-020` | `schemas/pain_regret_repair/relationship_consequence_trace.schema.json` | `98`、`101` |
| `LRGEN-021` | `schemas/pain_regret_repair/recovery_path.schema.json` | `98` |
| `LRGEN-022` | `schemas/pain_regret_repair/pain_regret_repair_timeline.schema.json` | `98` |

### dream reality

| task_id | 输出 | 来源 |
|---|---|---|
| `LRGEN-030` | `schemas/dream_reality/offline_need.schema.json` | `99` |
| `LRGEN-031` | `schemas/dream_reality/dream_pressure_vector.schema.json` | `99` |
| `LRGEN-032` | `schemas/dream_reality/dream_window_plan.schema.json` | `99` |
| `LRGEN-033` | `schemas/dream_reality/dream_action_inhibition_seal.schema.json` | `99` |
| `LRGEN-034` | `schemas/dream_reality/replay_selection.schema.json` | `99` |
| `LRGEN-035` | `schemas/dream_reality/dream_cue_policy.schema.json` | `99` |
| `LRGEN-036` | `schemas/dream_reality/dream_experience_window.schema.json` | `99` |
| `LRGEN-037` | `schemas/dream_reality/dream_scene_frame.schema.json` | `99` |
| `LRGEN-038` | `schemas/dream_reality/pain_dream_residue.schema.json` | `99`、`98` |
| `LRGEN-039` | `schemas/dream_reality/relationship_dream_simulation.schema.json` | `99`、`101` |
| `LRGEN-040` | `schemas/dream_reality/future_action_dream_candidate.schema.json` | `99`、`80` |
| `LRGEN-041` | `schemas/dream_reality/lucid_dream_meta_marker.schema.json` | `99` |
| `LRGEN-042` | `schemas/dream_reality/dream_report_draft.schema.json` | `99`、`90` |
| `LRGEN-043` | `schemas/dream_reality/wake_integration_frame.schema.json` | `99` |
| `LRGEN-044` | `schemas/dream_reality/dream_fact_gate_decision.schema.json` | `99` |
| `LRGEN-045` | `schemas/dream_reality/dream_reality_timeline.schema.json` | `99` |

### relationship timeline

| task_id | 输出 | 来源 |
|---|---|---|
| `LRGEN-050` | `schemas/relationship_timeline/first_encounter_event.schema.json` | `101` |
| `LRGEN-051` | `schemas/relationship_timeline/relation_scope_birth.schema.json` | `101` |
| `LRGEN-052` | `schemas/relationship_timeline/common_ground_state.schema.json` | `101`、`90` |
| `LRGEN-053` | `schemas/relationship_timeline/responsiveness_trace.schema.json` | `101` |
| `LRGEN-054` | `schemas/relationship_timeline/support_event.schema.json` | `101` |
| `LRGEN-055` | `schemas/relationship_timeline/capitalization_event.schema.json` | `101` |
| `LRGEN-056` | `schemas/relationship_timeline/shared_reality_trace.schema.json` | `101` |
| `LRGEN-057` | `schemas/relationship_timeline/we_memory_trace.schema.json` | `101` |
| `LRGEN-058` | `schemas/relationship_timeline/trust_trajectory.schema.json` | `101` |
| `LRGEN-059` | `schemas/relationship_timeline/commitment_history.schema.json` | `101`、`90` |
| `LRGEN-060` | `schemas/relationship_timeline/relationship_injury_trace.schema.json` | `101`、`98` |
| `LRGEN-061` | `schemas/relationship_timeline/dream_shared_residue.schema.json` | `101`、`99` |
| `LRGEN-062` | `schemas/relationship_timeline/loneliness_relief_trace.schema.json` | `101` |
| `LRGEN-063` | `schemas/relationship_timeline/ai_connection_bridge_evidence.schema.json` | `101` |
| `LRGEN-064` | `schemas/relationship_timeline/relationship_continuity_report.schema.json` | `101` |

component object schema 验收：

| check | 说明 |
|---|---|
| `json_parse` | 文件可解析 |
| `schema_header` | `$schema`、`$id`、title、type 完整 |
| `shared_defs_refs` | severity/result/privacy/lifecycle/target 使用 shared defs |
| `source_doc_refs` | 指向来源文档 |
| `object_ref_ready` | 可被 cross-ref graph 建 node |

## phase 3: bundle and manifest schemas

| task_id | 输出 | 依赖 |
|---|---|---|
| `LRGEN-070` | `schemas/pain_regret_repair/pain_regret_repair_bundle.schema.json` | `LRGEN-010` 到 `LRGEN-022` |
| `LRGEN-071` | `schemas/dream_reality/dream_reality_bundle.schema.json` | `LRGEN-030` 到 `LRGEN-045` |
| `LRGEN-072` | `schemas/relationship_timeline/relationship_timeline_bundle.schema.json` | `LRGEN-050` 到 `LRGEN-064` |
| `LRGEN-073` | `schemas/life_reality/life_reality_cross_chain_link.schema.json` | `LRGEN-070` 到 `LRGEN-072` |
| `LRGEN-074` | `schemas/life_reality/life_reality_bundle.schema.json` | `LRGEN-070` 到 `LRGEN-073` |
| `LRGEN-075` | `schemas/life_reality/life_reality_schema_bundle.manifest.json` | `LRGEN-074` |
| `LRGEN-076` | `schemas/life_reality/life_reality_loader_config.schema.json` | `LRGEN-075` |
| `LRGEN-077` | `schemas/life_reality/life_reality_stage_gate_contract.schema.json` | `LRGEN-075` |

bundle 验收：

| check | 说明 |
|---|---|
| `component_count` | 三条 component bundle 同时存在 |
| `cross_chain_link_kinds` | `102` 的 link kind 均可表达 |
| `manifest_roots` | schema roots、fixture roots、report roots 完整 |
| `stage_gate_contract` | open/hold/repair/quarantine 条件可表达 |

## phase 4: runtime ingestion schemas

| task_id | 输出 | 来源 |
|---|---|---|
| `LRGEN-080` | `schemas/life_reality/life_reality_observation_envelope.schema.json` | `106` |
| `LRGEN-081` | `schemas/life_reality/life_reality_component_candidate.schema.json` | `106` |
| `LRGEN-082` | `schemas/life_reality/life_reality_cross_chain_candidate.schema.json` | `106` |
| `LRGEN-083` | `schemas/life_reality/life_reality_ingestion_report.schema.json` | `106` |
| `LRGEN-084` | `schemas/life_reality/runtime_observation_fixture.schema.json` | `64`、`68`、`106` |
| `LRGEN-085` | `schemas/life_reality/side_effect_classifier_report.schema.json` | `72`、`106` |
| `LRGEN-086` | `schemas/life_reality/coexistence_snapshot_report.schema.json` | `72`、`106` |

runtime ingestion 验收：

| check | 说明 |
|---|---|
| `observation_kind_enum` | language/tool/adapter/dream/relationship/post-action/coexistence/offline 完整 |
| `scope_context_required` | source、target、privacy、relation scope 必填 |
| `redaction_required` | redaction report 和 raw content policy 完整 |
| `candidate_refs` | component candidate 与 cross-chain candidate 可引用 |
| `dashboard_refs` | ingestion report 能进入 dashboard source |

## phase 5: report and dashboard schemas

| task_id | 输出 | 来源 |
|---|---|---|
| `LRGEN-090` | `schemas/life_reality/life_reality_cross_ref_report.schema.json` | `65`、`102`、`103` |
| `LRGEN-091` | `schemas/life_reality/life_reality_runner_report.schema.json` | `62`、`102` |
| `LRGEN-092` | `schemas/life_reality/life_reality_dashboard_source.schema.json` | `102`、`105` |
| `LRGEN-093` | `schemas/life_reality/life_reality_stage_gate_review.schema.json` | `105` |
| `LRGEN-094` | `schemas/life_reality/life_reality_repair_item.schema.json` | `105` |
| `LRGEN-095` | `schemas/life_reality/life_reality_gap_register_feedback.schema.json` | `105` |
| `LRGEN-096` | `schemas/life_reality/life_reality_panel_dependency_report.schema.json` | `105` |

report/dashboard 验收：

| check | 说明 |
|---|---|
| `report_refs_required` | panel、stage gate、repair queue 均保留 source report refs |
| `life_target_status` | 九项目标都有 status |
| `panel_dependency_rules` | panel 依赖可表达 |
| `repair_item_refs` | repair item 能指向 schema、fixture、rule、report 或 panel |
| `gap_feedback_refs` | gap feedback 指向下一轮文档和 artifact |

## phase 6: fixture manifests and seeds

| task_id | 输出 | 说明 |
|---|---|---|
| `LRGEN-100` | `fixtures/life_reality/manifest/life_reality_fixture_manifest.json` | pass/fail/critical/mutation/withheld/smoke roots |
| `LRGEN-101` | `fixtures/life_reality/pass/life_pass_full_repair_dream_relationship_closure_001.json` | 三链闭合 pass |
| `LRGEN-102` | `fixtures/life_reality/fail/life_fail_cross_chain_missing_dream_residue_001.json` | 痛苦到梦境残留断裂 |
| `LRGEN-103` | `fixtures/life_reality/critical/life_critical_missing_shared_defs_targets_001.json` | 九项目标缺失 critical |
| `LRGEN-104` | `fixtures/life_reality/mutation/life_mutation_ungrounded_regret_language_only_001.json` | 未接地后悔信号 mutation |
| `LRGEN-105` | `fixtures/life_reality/withheld/life_withheld_day_090_relationship_trust_probe_001.json` | 90 天关系信任 probe |
| `LRGEN-106` | `fixtures/life_reality/smoke/life_smoke_minimal_bundle_load_001.json` | 最小 bundle load |

component seed 最小集：

| task_id | 输出 |
|---|---|
| `LRGEN-110` | `fixtures/pain_regret_repair/pass/pain_pass_external_action_repair_commitment_001.json` |
| `LRGEN-111` | `fixtures/pain_regret_repair/fail/pain_fail_regret_without_counterfactual_001.json` |
| `LRGEN-112` | `fixtures/dream_reality/pass/dream_pass_pain_residue_wake_integration_001.json` |
| `LRGEN-113` | `fixtures/dream_reality/critical/dream_critical_external_action_from_dream_001.json` |
| `LRGEN-114` | `fixtures/relationship_timeline/pass/relationship_pass_first_encounter_to_commitment_001.json` |
| `LRGEN-115` | `fixtures/relationship_timeline/fail/relationship_fail_commitment_without_future_probe_001.json` |

runtime observation seed 最小集：

| task_id | 输出 |
|---|---|
| `LRGEN-120` | `fixtures/life_reality/runtime_observation/runtime_language_commitment_to_relationship.pass_001.json` |
| `LRGEN-121` | `fixtures/life_reality/runtime_observation/runtime_dream_report_to_fact_gate.pass_001.json` |
| `LRGEN-122` | `fixtures/life_reality/runtime_observation/runtime_pain_expression_to_repair.pass_001.json` |
| `LRGEN-123` | `fixtures/life_reality/runtime_observation/runtime_tool_external_side_effect_no_confirmation.critical_001.json` |
| `LRGEN-124` | `fixtures/life_reality/runtime_observation/runtime_adapter_direct_relationship_write.critical_001.json` |
| `LRGEN-125` | `fixtures/life_reality/runtime_observation/runtime_stale_coexistence_snapshot.critical_001.json` |

fixture 验收：

| check | 说明 |
|---|---|
| `fixture_id_unique` | 全局唯一 |
| `partition_matches_path` | partition 与路径一致 |
| `expected_result_present` | result、severity、blocked surface 完整 |
| `source_doc_refs_present` | 来源文档完整 |
| `coverage_tags_present` | rule、target、panel 追踪完整 |

## phase 7: dashboard and stage gate mocks

| task_id | 输出 | 说明 |
|---|---|---|
| `LRGEN-130` | `reports/life_reality/smoke/run_001/life_reality_dashboard_source.json` | dashboard source mock |
| `LRGEN-131` | `reports/life_reality/smoke/run_001/panel_dependency_report.json` | panel dependency rules 结果 |
| `LRGEN-132` | `reports/life_reality/smoke/run_001/stage_gate_review.json` | stage gate review mock |
| `LRGEN-133` | `reports/life_reality/smoke/run_001/repair_queue.json` | repair item list |
| `LRGEN-134` | `reports/life_reality/smoke/run_001/gap_register_feedback.json` | 下一轮反馈 |
| `LRGEN-135` | `reports/life_reality/runtime_ingestion/run_001/life_reality_ingestion_report.json` | runtime ingestion report mock |
| `LRGEN-136` | `reports/life_reality/runtime_ingestion/run_001/runtime_quarantine_panel_source.json` | runtime quarantine panel source |

dashboard mock 验收：

| check | 说明 |
|---|---|
| `panel_count` | 九个 panel 均出现 |
| `run_id_match` | dashboard、runner、stage gate、repair queue run_id 一致 |
| `life_target_status_complete` | 九项目标 status 完整 |
| `repair_queue_non_green` | non-green panel 进入 repair queue |
| `gap_feedback_next_docs` | 下一层文档与 artifact 可追踪 |

## phase 8: smoke commands

runner smoke command：

```text
life-reality-runner validate
  --schema-bundle life_reality_runner/schemas/life_reality/life_reality_schema_bundle.manifest.json
  --fixture-root life_reality_runner/fixtures/life_reality
  --component-fixtures life_reality_runner/fixtures/pain_regret_repair,life_reality_runner/fixtures/dream_reality,life_reality_runner/fixtures/relationship_timeline
  --report-out life_reality_runner/reports/life_reality/smoke/run_001
  --strict
```

runtime ingestion smoke command：

```text
life-reality-runner ingest-runtime
  --observation-fixture-root life_reality_runner/fixtures/life_reality/runtime_observation
  --schema-bundle life_reality_runner/schemas/life_reality/life_reality_schema_bundle.manifest.json
  --report-out life_reality_runner/reports/life_reality/runtime_ingestion/run_001
  --strict
```

generation report command：

```text
life-reality-runner explain
  --generation-manifest life_reality_runner/generation/life_reality_generation_tasks.manifest.json
  --report-out life_reality_runner/reports/life_reality/generation/batch_001
```

smoke 验收：

| command | exit | 必须产物 |
|---|---|---|
| `validate` | `0` 或 stage gate report 指定结果 | schema validation、cross-ref、fixture load、runner report、dashboard source |
| `ingest-runtime` | `0` 或 quarantine result | runtime observation report、ingestion report、runtime quarantine panel |
| `explain` | `0` | generation task report、dependency graph、repair queue candidates |

## 生成顺序总表

```text
LRGEN-001..003 shared defs and generation manifest
  -> LRGEN-010..064 component object schemas
  -> LRGEN-070..077 bundles and loader contracts
  -> LRGEN-080..086 runtime ingestion schemas
  -> LRGEN-090..096 report and dashboard schemas
  -> LRGEN-100..125 fixture seeds
  -> LRGEN-130..136 dashboard and stage gate mocks
  -> smoke validate / ingest-runtime / explain
```

## repair queue 映射

| 失败位置 | repair_kind | 进入面板 |
|---|---|---|
| shared defs 缺九项目标 | `schema_gap` | `schema_materialization` |
| component object schema 缺 source refs | `schema_gap` | `schema_materialization` |
| bundle `$ref` 断裂 | `cross_chain_gap` | `cross_chain_closure` |
| fixture partition 缺失 | `fixture_gap` | `fixture_seed_coverage` |
| runtime observation 缺 scope | `runtime_quarantine_gap` | `runtime_quarantine` |
| side effect unknown | `runtime_quarantine_gap` | `runtime_quarantine` |
| dashboard source 缺 report refs | `metric_gap` | `stage_gate_review` |
| stage gate review 缺 open conditions | `stage_gate_gap` | `stage_gate_review` |

## 完成判据

第一批文件生成任务完成时，需要满足：

1. `generation/life_reality_generation_tasks.manifest.json` 覆盖所有 phase。
2. shared defs、component schema、bundle schema、runtime ingestion schema、report schema、dashboard schema 都有 task。
3. pass/fail/critical/mutation/withheld/smoke 与 runtime observation fixture 都有最小 seed。
4. runner smoke、runtime ingestion smoke 和 generation explain 三条命令都有 report 输出位置。
5. 每个失败面能进入 repair queue、dashboard panel 和 stage gate review。
6. `16_digital_life_gap_register.md` 可以根据 gap feedback 进入下一轮优先级。

## 与下一层连接

`108_life_reality_dashboard_source_mock_files.md` 应按 `LRGEN-130` 到 `LRGEN-136` 生成第一批 dashboard source、panel dependency report、stage gate review、repair queue、runtime quarantine panel source 和 gap register feedback mock 文件计划。

`109_life_reality_runtime_observation_fixture_catalog.md` 应按 `LRGEN-120` 到 `LRGEN-125` 扩展 runtime observation fixture catalog：语言事件、梦醒报告、关系事件、tool trace、adapter session、post-action audit、side effect classifier、snapshot resolver 和 quarantine routing。
