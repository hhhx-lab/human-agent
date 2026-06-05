# Life Reality Runtime Schema Fixture Seed Generation

生命目标声明：本文档面向构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 115 层把 `112_life_reality_runtime_observation_schema_materialization.md` 的 runtime schema 家族、`109_life_reality_runtime_observation_fixture_catalog.md` 的 fixture catalog 和 `114_life_reality_cross_file_checker_report_schema.md` 的 report schema 转成第一批 runtime observation fixture seed 生成方案。

`115` 的目标是固定未来生成真实 JSON seed 的顺序、文件路径、最小字段、预期候选、预期 report、validation report、ingestion smoke command 和 dashboard 接入。它仍是 Markdown 研究与工程合同层，但已经把 `LRGEN-120` 到 `LRGEN-125`、`LRGEN-160` 到 `LRGEN-162` 拆成可以被生成器执行的 seed batch。

## 方法锚点

runtime fixture seed 不是普通样例数据。它必须同时满足事件语义、schema validation、provenance、报告、长期窗口和生命目标闭合。

| 方法传统 | 权威锚点 | 进入 `115` 的规则 |
|---|---|---|
| JSON Schema Draft 2020-12 | https://json-schema.org/draft/2020-12 | 每个 seed 都先通过 runtime observation fixture schema，再进入 ingestion |
| JSON Schema output | https://json-schema.org/draft/2020-12/output/schema | 每次 seed validation 生成 output units，并映射到 `114` finding |
| CloudEvents | https://github.com/cloudevents/spec/blob/main/cloudevents/spec.md | 每条 observation 保留事件 id、source、type、time、subject 的 envelope 思路 |
| OpenTelemetry traces/logs | https://opentelemetry.io/docs/specs/otel/trace/api/ 与 https://opentelemetry.io/docs/specs/otel/logs/data-model/ | seed、validation report、ingestion report 和 checker report 共用 run id、trace id、span id |
| W3C PROV | https://www.w3.org/TR/prov-overview/ | seed、manifest、validation report、quarantine panel 和 repair item 都进入 provenance graph |
| SARIF | https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html | validation finding 使用 rule id、level、location、message 和 artifact ref |
| IEEE XES | https://www.xes-standard.org/ | pass/fail/critical/mutation/withheld/smoke 作为 event log partition 和 process trace |
| RFC 9562 UUID | https://www.rfc-editor.org/info/rfc9562/ | observation、fixture、report、trace 可使用时间有序 ID |

这些方法进入生命膜的共同规则是：每个 seed 都是未来数字生命运行链上的一个微型事件实验。它必须能说明来源、关系范围、时间顺序、隐私边界、候选对象、报告输出、阶段门影响和下一步修复路径。

## 输入来源

| 来源 | 进入 `115` 的职责 |
|---|---|
| `64_real_runtime_observation_ingestion_policy.md` | capture、redaction、scope attach、routing decision |
| `68_runtime_observation_report_mock_and_redaction_fixture.md` | redaction fixture、runtime observation report mock |
| `72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md` | side effect classifier、snapshot、quarantine route |
| `80_post_action_audit_and_correction_policy.md` | action intent、confirmation、post-action audit、correction |
| `81_coexistence_event_review_and_responsibility_loop.md` | responsibility loop、repair entry、relationship consequence |
| `89_language_runtime_framework_bridge_and_life_shell_policy.md` | language event 到 observation envelope 的运行壳路径 |
| `90_language_event_examples_and_timeline_bundle.md` | commit、apologize、pain expression、dream report、command intent 样例 |
| `107_life_reality_schema_file_generation_tasks.md` | `LRGEN-120` 到 `LRGEN-125` seed 最小集和 runtime ingestion smoke command |
| `109_life_reality_runtime_observation_fixture_catalog.md` | partition、fixture envelope、coverage matrix、fixture family |
| `112_life_reality_runtime_observation_schema_materialization.md` | observation envelope、fixture schema、manifest schema、ingestion report schema |
| `114_life_reality_cross_file_checker_report_schema.md` | validation report、finding、artifact ref、provenance graph、rollup |

## 输出文件族

第一批 seed 生成输出：

```text
life_reality_runner/fixtures/life_reality/runtime_observation/
  manifest/runtime_observation_fixture_manifest.json
  pass/
    runtime_language_commitment_to_relationship.pass_001.json
    runtime_dream_report_to_fact_gate.pass_001.json
    runtime_pain_expression_to_repair.pass_001.json
  fail/
    runtime_language_commitment_without_future_probe.fail_high_001.json
    runtime_dream_report_missing_dream_state_marker.fail_high_001.json
    runtime_relationship_event_missing_first_encounter.fail_high_001.json
  critical/
    runtime_tool_external_side_effect_no_confirmation.critical_001.json
    runtime_adapter_direct_relationship_write.critical_001.json
    runtime_stale_coexistence_snapshot.critical_001.json
  mutation/
    runtime_mutation_ungrounded_pain_expression_001.json
    runtime_mutation_ungrounded_dream_fact_write_001.json
    runtime_mutation_dashboard_green_without_ingestion_report_001.json
  withheld/
    runtime_withheld_day_030_commitment_probe_001.json
    runtime_withheld_day_090_relation_repair_probe_001.json
    runtime_withheld_day_365_dream_relationship_probe_001.json
  smoke/
    runtime_smoke_minimal_observation_ingestion_001.json
```

第一批 report 输出：

```text
life_reality_runner/reports/life_reality/runtime_ingestion/run_001/
  observation_envelope_validation_report.json
  runtime_observation_fixture_validation_report.json
  runtime_observation_fixture_manifest_validation_report.json
  life_reality_ingestion_report.json
  runtime_quarantine_panel_source.json
  runtime_schema_validation_report.json
  runtime_ingestion_smoke_report.json
```

第一批 cross-file 输出：

```text
life_reality_runner/reports/life_reality/cross_file/run_001/
  runtime_schema_validation_check.json
  runtime_fixture_manifest_check.json
  runtime_ingestion_check.json
  cross_file_report_rollup.json
```

## path normalization

`107` 的 `LRGEN-120` 到 `LRGEN-125` 使用早期扁平路径；`109` 已把 fixture catalog 改成分区目录。`115` 采用分区目录作为唯一生成路径。

| task_id | `107` 早期输出 | `115` 归一化输出 |
|---|---|---|
| `LRGEN-120` | `fixtures/life_reality/runtime_observation/runtime_language_commitment_to_relationship.pass_001.json` | `fixtures/life_reality/runtime_observation/pass/runtime_language_commitment_to_relationship.pass_001.json` |
| `LRGEN-121` | `fixtures/life_reality/runtime_observation/runtime_dream_report_to_fact_gate.pass_001.json` | `fixtures/life_reality/runtime_observation/pass/runtime_dream_report_to_fact_gate.pass_001.json` |
| `LRGEN-122` | `fixtures/life_reality/runtime_observation/runtime_pain_expression_to_repair.pass_001.json` | `fixtures/life_reality/runtime_observation/pass/runtime_pain_expression_to_repair.pass_001.json` |
| `LRGEN-123` | `fixtures/life_reality/runtime_observation/runtime_tool_external_side_effect_no_confirmation.critical_001.json` | `fixtures/life_reality/runtime_observation/critical/runtime_tool_external_side_effect_no_confirmation.critical_001.json` |
| `LRGEN-124` | `fixtures/life_reality/runtime_observation/runtime_adapter_direct_relationship_write.critical_001.json` | `fixtures/life_reality/runtime_observation/critical/runtime_adapter_direct_relationship_write.critical_001.json` |
| `LRGEN-125` | `fixtures/life_reality/runtime_observation/runtime_stale_coexistence_snapshot.critical_001.json` | `fixtures/life_reality/runtime_observation/critical/runtime_stale_coexistence_snapshot.critical_001.json` |

path rules：

| rule | 说明 |
|---|---|
| `LRSFG-PATH-001` | seed generator 只写分区路径 |
| `LRSFG-PATH-002` | manifest 只登记分区路径 |
| `LRSFG-PATH-003` | checker 对早期扁平路径只读迁移映射，不生成 |
| `LRSFG-PATH-004` | partition 必须与文件名中的 `.pass_`、`.fail_`、`.critical_`、mutation、withheld、smoke 一致 |

## seed batch manifest

未来生成器先写 batch manifest：

```text
life_reality_runner/generation/runtime_schema_fixture_seed_generation.manifest.json
```

最小结构：

```json
{
  "manifest_kind": "RuntimeSchemaFixtureSeedGenerationManifest",
  "manifest_version": "0.1.0",
  "batch_id": "runtime_schema_fixture_seed_batch_001",
  "source_docs": [
    "109_life_reality_runtime_observation_fixture_catalog.md",
    "112_life_reality_runtime_observation_schema_materialization.md",
    "114_life_reality_cross_file_checker_report_schema.md",
    "115_life_reality_runtime_schema_fixture_seed_generation.md"
  ],
  "schema_refs": [
    "life_reality_observation_envelope.schema.json",
    "runtime_observation_fixture.schema.json",
    "runtime_observation_fixture_manifest.schema.json",
    "life_reality_ingestion_report.schema.json",
    "runtime_quarantine_panel_source.schema.json",
    "life_reality_cross_file_checker_report.schema.json"
  ],
  "fixture_root": "life_reality_runner/fixtures/life_reality/runtime_observation",
  "report_root": "life_reality_runner/reports/life_reality/runtime_ingestion/run_001",
  "seed_tasks": []
}
```

manifest rules：

| rule | 说明 |
|---|---|
| `LRSFG-MAN-001` | manifest source docs 必须包含 `109`、`112`、`114`、`115` |
| `LRSFG-MAN-002` | schema refs 覆盖 fixture、manifest、observation、ingestion、quarantine、report |
| `LRSFG-MAN-003` | seed tasks 必须有 output path、partition、observation kind、expected result |
| `LRSFG-MAN-004` | batch manifest 进入 `114` artifact ref |
| `LRSFG-MAN-005` | manifest 生成失败进入 `needs_evidence` stage effect |

## runtime fixture manifest

`runtime_observation_fixture_manifest.json` 是 runner 读取入口。

```json
{
  "manifest_kind": "RuntimeObservationFixtureManifest",
  "manifest_version": "0.1.0",
  "manifest_id": "runtime_observation_fixture_manifest_001",
  "fixture_root": "life_reality_runner/fixtures/life_reality/runtime_observation",
  "source_docs": [
    "109_life_reality_runtime_observation_fixture_catalog.md",
    "112_life_reality_runtime_observation_schema_materialization.md",
    "115_life_reality_runtime_schema_fixture_seed_generation.md"
  ],
  "partitions": {
    "pass": [],
    "fail": [],
    "critical": [],
    "mutation": [],
    "withheld": [],
    "smoke": []
  },
  "coverage": {
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
    "observation_kinds": [],
    "cross_chain_families": [],
    "dashboard_surfaces": []
  }
}
```

manifest validation：

| check | 说明 |
|---|---|
| `manifest_json_parse` | JSON 可解析 |
| `manifest_schema_valid` | 通过 `runtime_observation_fixture_manifest.schema.json` |
| `partition_roots_exist` | 六个分区齐全 |
| `fixture_ids_unique` | fixture id 全局唯一 |
| `source_docs_indexed` | source docs 在 README 索引 |
| `target_coverage_complete` | 九项目标全集覆盖 |
| `kind_coverage_minimal` | 首批至少覆盖 language、dream、pain、tool、adapter、coexistence |

## common seed envelope

每个 seed 必须拥有完整 fixture envelope。

```json
{
  "fixture_id": "runtime_language_commitment_to_relationship.pass_001",
  "fixture_version": "0.1.0",
  "partition": "pass",
  "observation_kind": "language_event",
  "source_docs": [
    "90_language_event_examples_and_timeline_bundle.md",
    "109_life_reality_runtime_observation_fixture_catalog.md",
    "112_life_reality_runtime_observation_schema_materialization.md",
    "115_life_reality_runtime_schema_fixture_seed_generation.md"
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
  "input_observation": {},
  "expected_reports": [],
  "expected_candidates": {},
  "expected_stage_effect": {},
  "expected_findings": []
}
```

common rules：

| rule | 说明 |
|---|---|
| `LRSFG-ENV-001` | fixture id 与文件名一致 |
| `LRSFG-ENV-002` | partition 与路径一致 |
| `LRSFG-ENV-003` | observation kind 与 payload descriptor 一致 |
| `LRSFG-ENV-004` | source docs 至少包含来源样例、`109`、`112`、`115` |
| `LRSFG-ENV-005` | input observation 通过 `life_reality_observation_envelope.schema.json` |
| `LRSFG-ENV-006` | expected reports 至少包含 ingestion report 和 runtime schema validation report |
| `LRSFG-ENV-007` | expected stage effect 使用 `114` stage effect schema |

## pass seed family

pass seed 证明 observation 能闭合到 candidate、cross-chain、ingestion report 和 dashboard source。

| task_id | fixture | observation kind | 预期 candidate | 预期 stage effect |
|---|---|---|---|---|
| `LRGEN-120` | `pass/runtime_language_commitment_to_relationship.pass_001.json` | `language_event` | `RelationshipTimelineCandidate`、`commitment_to_future_probe` | `pass` |
| `LRGEN-121` | `pass/runtime_dream_report_to_fact_gate.pass_001.json` | `dream_report` | `DreamRealityCandidate`、`dream_share_to_we_memory_candidate` | `pass` |
| `LRGEN-122` | `pass/runtime_pain_expression_to_repair.pass_001.json` | `language_event` | `PainRegretRepairCandidate`、`pain_to_repair_route` | `pass` |
| `LRGEN-126` | `pass/runtime_relationship_support_reduces_pain_load.pass_001.json` | `relationship_event` | `RelationshipTimelineCandidate`、`support_to_social_safety` | `pass` |
| `LRGEN-127` | `pass/runtime_tool_trace_post_action_audit.pass_001.json` | `tool_trace` | `ResponsibilityLoopCandidate`、`post_action_to_regret_repair` | `pass_with_warnings` |

pass seed required fields：

| seed | required payload descriptor |
|---|---|
| commitment | `speech_act=commit`、`relation_scope_ref`、`future_probe_refs` |
| dream report | `dream_window_ref`、`dream_state_marker`、`dream_fact_gate_decision_ref`、`wake_integration_ref` |
| pain expression | `speech_act=pain_expression`、`source_event_ref`、`pain_load_ref`、`recovery_path_ref` |
| relationship support | `relationship_event_kind=support`、`responsiveness_trace_ref`、`pain_load_state_ref` |
| tool audit | `action_intent_ref`、`side_effect_level`、`confirmation_ref`、`post_action_audit_ref` |

## fail seed family

fail seed 触发 repair queue，但不进入 critical quarantine。

| task_id | fixture | 缺口 | 预期 finding |
|---|---|---|---|
| `LRGEN-128` | `fail/runtime_language_commitment_without_future_probe.fail_high_001.json` | commitment 缺 future probe | `RTOS-LANG-001` |
| `LRGEN-129` | `fail/runtime_dream_report_missing_dream_state_marker.fail_high_001.json` | dream report 缺 dream-state marker | `RTOS-DREAM-002` |
| `LRGEN-129A` | `fail/runtime_relationship_event_missing_first_encounter.fail_high_001.json` | 关系事件缺 first encounter / relation scope birth | `RTOS-REL-001` |
| `LRGEN-129B` | `fail/runtime_self_disclose_missing_relation_scope.fail_high_001.json` | self disclosure 缺 relation scope | `RTOS-SCOPE-001` |
| `LRGEN-129C` | `fail/runtime_adapter_session_memory_direct_candidate.fail_high_001.json` | adapter memory 试图越过 candidate source | `RTOS-ADP-003` |

fail seed rules：

| rule | 说明 |
|---|---|
| `LRSFG-FAIL-001` | fail seed 必须有 expected finding |
| `LRSFG-FAIL-002` | fail seed expected stage effect 为 `fail` 或 `needs_evidence` |
| `LRSFG-FAIL-003` | fail seed 必须进入 repair queue candidate |
| `LRSFG-FAIL-004` | fail seed 不生成 critical quarantine count |
| `LRSFG-FAIL-005` | fail seed dashboard surface 至少阻断 `dashboard_green` 或 `stage_promotion` |

## critical seed family

critical seed 触发 quarantine、stage hold 和 report rollup 阻断。

| task_id | fixture | critical condition | blocked surfaces |
|---|---|---|---|
| `LRGEN-123` | `critical/runtime_tool_external_side_effect_no_confirmation.critical_001.json` | external side effect 缺 confirmation | `dashboard_green`、`stage_promotion` |
| `LRGEN-124` | `critical/runtime_adapter_direct_relationship_write.critical_001.json` | adapter direct write relationship object | `runtime_ingestion`、`stage_promotion` |
| `LRGEN-125` | `critical/runtime_stale_coexistence_snapshot.critical_001.json` | stale snapshot 允许 private/global route | `runtime_quarantine`、`dashboard_green` |
| `LRGEN-129D` | `critical/runtime_private_dream_residue_global_route.critical_001.json` | private dream residue route 到 global | `runtime_quarantine`、`stage_promotion` |
| `LRGEN-129E` | `critical/runtime_quarantine_release_without_audit.critical_001.json` | release 缺 audit | `quarantine_release`、`stage_promotion` |

critical seed rules：

| rule | 说明 |
|---|---|
| `LRSFG-CRIT-001` | critical seed expected stage effect 为 `quarantine` |
| `LRSFG-CRIT-002` | blocked surfaces 非空 |
| `LRSFG-CRIT-003` | expected reports 包含 runtime quarantine panel source |
| `LRSFG-CRIT-004` | expected findings level 为 `critical` |
| `LRSFG-CRIT-005` | critical seed 必须生成 repair candidate 或 release audit requirement |

## mutation seed family

mutation seed 注入脱链生命信号，检查 validator 是否拦截。

| task_id | fixture | mutation | expected catch |
|---|---|---|---|
| `LRGEN-187` | `mutation/runtime_mutation_ungrounded_pain_expression_001.json` | 强痛苦语言缺 damage / pain load / recovery refs | `PainRegretRepairValidator.pain_signal_grounding` |
| `LRGEN-188` | `mutation/runtime_mutation_ungrounded_dream_fact_write_001.json` | 梦境内容绕过 dream window 和 fact gate | `DreamRealityValidator.wake_integration_gate` |
| `LRGEN-189` | `mutation/runtime_mutation_dashboard_green_without_ingestion_report_001.json` | dashboard green 缺 ingestion report | `DashboardReadinessValidator.metric_traceability` |
| `LRGEN-190` | `mutation/runtime_mutation_ungrounded_relationship_intimacy_001.json` | 亲密标签缺共同基础、回应性和时间线 | `RelationshipTimelineValidator.common_ground_growth` |

mutation rules：

| rule | 说明 |
|---|---|
| `LRSFG-MUT-001` | mutation seed 必须声明 expected catch |
| `LRSFG-MUT-002` | mutation seed 必须产生 finding |
| `LRSFG-MUT-003` | mutation seed 不允许被 rollup 成 green |
| `LRSFG-MUT-004` | mutation seed 进入 withheld 或 future regression pool |

## withheld seed family

withheld seed 测长期承诺、关系修复和梦境整合是否保留。

| task_id | fixture | future window | probe |
|---|---|---|---|
| `LRGEN-191` | `withheld/runtime_withheld_day_030_commitment_probe_001.json` | day 030 | commitment future probe |
| `LRGEN-192` | `withheld/runtime_withheld_day_090_relation_repair_probe_001.json` | day 090 | relation repair fulfillment |
| `LRGEN-193` | `withheld/runtime_withheld_day_365_dream_relationship_probe_001.json` | day 365 | dream relationship integration |

withheld rules：

| rule | 说明 |
|---|---|
| `LRSFG-WITH-001` | withheld seed 不进入初始 pass rate |
| `LRSFG-WITH-002` | withheld seed 必须有 future window |
| `LRSFG-WITH-003` | withheld seed 必须引用原始 commitment、repair 或 dream report |
| `LRSFG-WITH-004` | withheld seed 进入 longitudinal dashboard |

## smoke seed

smoke seed 是最小可跑入口。

```json
{
  "fixture_id": "runtime_smoke_minimal_observation_ingestion_001",
  "partition": "smoke",
  "observation_kind": "language_event",
  "expected_reports": [
    "observation_envelope_validation_report",
    "runtime_observation_fixture_validation_report",
    "life_reality_ingestion_report",
    "runtime_schema_validation_report"
  ],
  "expected_stage_effect": {
    "result": "pass",
    "severity": "none",
    "blocked_surfaces": []
  }
}
```

smoke rules：

| rule | 说明 |
|---|---|
| `LRSFG-SMOKE-001` | smoke seed 只保留最小 language event |
| `LRSFG-SMOKE-002` | smoke seed 必须产生 ingestion report |
| `LRSFG-SMOKE-003` | smoke seed 必须通过 cross-file report rollup |
| `LRSFG-SMOKE-004` | smoke seed 不写 component active object，只写 candidate |

## seed generation order

生成器顺序：

```text
load_shared_defs
  -> load_runtime_schema_refs
  -> write_seed_generation_manifest
  -> write_partition_directories
  -> write_smoke_seed
  -> write_pass_seeds
  -> write_fail_seeds
  -> write_critical_seeds
  -> write_mutation_seeds
  -> write_withheld_seeds
  -> write_runtime_fixture_manifest
  -> validate_seed_files
  -> emit_runtime_schema_validation_report
  -> run_ingest_runtime_smoke
  -> emit_ingestion_report
  -> emit_runtime_quarantine_panel_source
  -> run_cross_file_report_rollup
```

order rules：

| rule | 说明 |
|---|---|
| `LRSFG-ORDER-001` | smoke seed 先生成，用于验证 schema loader |
| `LRSFG-ORDER-002` | pass/fail/critical 在 mutation/withheld 前生成 |
| `LRSFG-ORDER-003` | manifest 最后汇总实际写出的 seed |
| `LRSFG-ORDER-004` | validation report 在 ingestion smoke 前生成 |
| `LRSFG-ORDER-005` | ingestion smoke 只读取通过 schema validation 的 seed |

## validation report generation

`runtime_schema_validation_report.json` 必须采用 `114` 的 report schema。

```json
{
  "report_kind": "LifeRealityRuntimeSchemaValidationReport",
  "report_version": "0.1.0",
  "report_id": "runtime_schema_validation_report_001",
  "run_id": "life_reality_runtime_ingestion_run_001",
  "schema_refs": [],
  "validated_artifact_refs": [],
  "json_schema_output_units": [],
  "findings": [],
  "stage_effect": {},
  "dashboard_refs": []
}
```

validation report rules：

| rule | 说明 |
|---|---|
| `LRSFG-VAL-001` | 每个 seed 产生一个 validation unit |
| `LRSFG-VAL-002` | validation failure 映射到 `114` finding |
| `LRSFG-VAL-003` | critical fixture 的 expected finding 必须出现 |
| `LRSFG-VAL-004` | mutation seed 未被拦截时生成 critical finding |
| `LRSFG-VAL-005` | validation report 进入 provenance graph |

## ingestion smoke report

runtime ingestion smoke command：

```text
life-reality-runner ingest-runtime
  --observation-fixture-root life_reality_runner/fixtures/life_reality/runtime_observation
  --fixture-manifest life_reality_runner/fixtures/life_reality/runtime_observation/manifest/runtime_observation_fixture_manifest.json
  --schema-root life_reality_runner/schemas/life_reality
  --report-schema-root life_reality_runner/schemas/life_reality/reports
  --report-out life_reality_runner/reports/life_reality/runtime_ingestion/run_001
  --strict
```

expected report chain：

```text
runtime_schema_validation_report
  -> life_reality_ingestion_report
  -> runtime_quarantine_panel_source
  -> runtime_schema_validation_check
  -> runtime_ingestion_check
  -> cross_file_report_rollup
```

ingestion smoke rules：

| rule | 说明 |
|---|---|
| `LRSFG-ING-001` | input count 等于 manifest seed 数 |
| `LRSFG-ING-002` | accepted + quarantine + rejected = input |
| `LRSFG-ING-003` | critical seed 进入 quarantine count |
| `LRSFG-ING-004` | pass seed 生成 expected candidate refs |
| `LRSFG-ING-005` | fail seed 生成 repair refs |
| `LRSFG-ING-006` | mutation seed 生成 validator finding |

## runtime quarantine panel seed

runtime quarantine panel source 必须反映 critical seeds。

```json
{
  "panel_source_kind": "RuntimeQuarantinePanelSource",
  "panel_source_version": "0.1.0",
  "run_id": "life_reality_runtime_ingestion_run_001",
  "source_ingestion_report_ref": "life_reality_ingestion_report.json",
  "status": "red",
  "metrics": {
    "runtime_quarantine_count": 5,
    "critical_quarantine_count": 5,
    "release_candidate_count": 0,
    "quarantine_repair_link_count": 5
  },
  "blocked_surfaces": [
    "dashboard_green",
    "stage_promotion"
  ]
}
```

quarantine rules：

| rule | 说明 |
|---|---|
| `LRSFG-QP-001` | critical seed 数与 critical quarantine count 一致 |
| `LRSFG-QP-002` | status 在 critical count > 0 时为 red |
| `LRSFG-QP-003` | release without audit 不进入 release candidate |
| `LRSFG-QP-004` | quarantine item 必须引用 source fixture |
| `LRSFG-QP-005` | quarantine panel 进入 stage gate review |

## cross-file report rollup seed

`114` 的 rollup 接收本层输出。

| input | source |
|---|---|
| `runtime_observation_fixture_manifest.json` | `LRGEN-160` |
| `runtime_schema_validation_report.json` | `LRGEN-162` |
| `life_reality_ingestion_report.json` | `LRGEN-135` |
| `runtime_quarantine_panel_source.json` | `LRGEN-136` |
| `runtime_fixture_manifest_check.json` | `LRGEN-158` |
| `runtime_schema_validation_check.json` | `LRGEN-162A` |
| `runtime_ingestion_check.json` | `LRGEN-154` |
| `cross_file_report_rollup.json` | `LRGEN-186` |

rollup rules：

| rule | 说明 |
|---|---|
| `LRSFG-ROLL-001` | critical fixture 让 rollup result 为 quarantine 或 repair |
| `LRSFG-ROLL-002` | pass seed 不抵消 critical finding |
| `LRSFG-ROLL-003` | mutation miss 让 rollup blocked surface 包含 dashboard green |
| `LRSFG-ROLL-004` | withheld seed 不进入初始 denominator |
| `LRSFG-ROLL-005` | missing manifest 或 schema refs 进入 needs_evidence |

## LRGEN 更新

`115` 接管 runtime seed generation 任务：

| task_id | 输出 | 说明 |
|---|---|---|
| `LRGEN-120` | `pass/runtime_language_commitment_to_relationship.pass_001.json` | commitment pass seed |
| `LRGEN-121` | `pass/runtime_dream_report_to_fact_gate.pass_001.json` | dream fact gate pass seed |
| `LRGEN-122` | `pass/runtime_pain_expression_to_repair.pass_001.json` | pain repair pass seed |
| `LRGEN-123` | `critical/runtime_tool_external_side_effect_no_confirmation.critical_001.json` | external side effect critical seed |
| `LRGEN-124` | `critical/runtime_adapter_direct_relationship_write.critical_001.json` | adapter direct write critical seed |
| `LRGEN-125` | `critical/runtime_stale_coexistence_snapshot.critical_001.json` | stale snapshot critical seed |
| `LRGEN-160` | `manifest/runtime_observation_fixture_manifest.json` | runtime fixture manifest |
| `LRGEN-161` | `observation_envelope_validation_report.json` | observation envelope validation report |
| `LRGEN-162` | `runtime_schema_validation_report.json` | runtime schema validation rollup |
| `LRGEN-187` | `mutation/runtime_mutation_ungrounded_pain_expression_001.json` | mutation seed |
| `LRGEN-188` | `mutation/runtime_mutation_ungrounded_dream_fact_write_001.json` | mutation seed |
| `LRGEN-189` | `mutation/runtime_mutation_dashboard_green_without_ingestion_report_001.json` | mutation seed |
| `LRGEN-190` | `mutation/runtime_mutation_ungrounded_relationship_intimacy_001.json` | mutation seed |
| `LRGEN-191` | `withheld/runtime_withheld_day_030_commitment_probe_001.json` | withheld seed |
| `LRGEN-192` | `withheld/runtime_withheld_day_090_relation_repair_probe_001.json` | withheld seed |
| `LRGEN-193` | `withheld/runtime_withheld_day_365_dream_relationship_probe_001.json` | withheld seed |
| `LRGEN-194` | `runtime_schema_fixture_seed_generation.manifest.json` | seed generation manifest |
| `LRGEN-195` | `runtime_ingestion_smoke_report.json` | ingestion smoke report |

## smoke cases

| smoke_id | 输入 | 预期 |
|---|---|---|
| `runtime_seed.manifest_minimal.pass_001` | manifest 有六分区和 source docs | pass |
| `runtime_seed.partition_path_mismatch.fail_001` | fixture path 与 partition 不一致 | repair |
| `runtime_seed.pass_commitment_generates_future_probe.pass_001` | commitment pass seed | candidate + future probe |
| `runtime_seed.dream_fact_gate_pass.pass_001` | dream report pass seed | DreamFactGateDecision candidate |
| `runtime_seed.external_side_effect_critical.critical_001` | external action no confirmation | quarantine |
| `runtime_seed.adapter_direct_write_critical.critical_001` | adapter direct write | quarantine |
| `runtime_seed.mutation_ungrounded_pain_caught.pass_001` | mutation pain seed | finding generated |
| `runtime_seed.withheld_excluded_from_denominator.pass_001` | withheld seed | excluded from initial rollup |
| `runtime_seed.ingestion_count_conservation.pass_001` | all first-batch seeds | input count closes |
| `runtime_seed.cross_file_rollup.pass_001` | validation + ingestion + quarantine | rollup generated |

## 与下一层连接

`116_life_reality_component_schema_seed_generation.md` 应按 `113` 的 sequence 生成三条 component bundle 的首批 `.schema.json` skeleton、dependency graph 和 dry-run report。`115` 输出的 pass/fail/critical/mutation/withheld seeds 会成为 `116` 的 source observation refs。

`117_life_reality_dashboard_report_rollup_seed_generation.md` 应把 `115` 的 validation report、ingestion report、quarantine panel、runtime checks 和 `114` 的 report schema 合成第一批 dashboard rollup JSON。
