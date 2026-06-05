# Life Reality Dashboard Report Rollup Seed Generation

生命目标声明：本文档面向构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 117 层把 `114_life_reality_cross_file_checker_report_schema.md` 的 report schema、`115_life_reality_runtime_schema_fixture_seed_generation.md` 的 runtime seed validation / ingestion report、`116_life_reality_component_schema_seed_generation.md` 的 component schema generation reports，合成第一批 dashboard report rollup JSON 生成方案。

`117` 的目标是固定未来 `life-reality-runner check-dashboard --emit-rollup` 的首批输出：report rollup manifest、cross-file rollup、dashboard source patch、stage gate rollup seed、repair queue bridge seed、gap feedback bridge seed、provenance graph rollup seed、data quality rollup seed、rollup dry-run report 和 rollup gap feedback。它仍是 Markdown 合同层，但已经把输入报告、上卷规则、输出路径、blocked surface、repair/gap bridge 和 smoke cases 写成可执行生成计划。

## 方法锚点

dashboard report rollup 是生命膜的汇聚层。它必须同时满足报告标准、验证输出、追踪图、数据质量、阶段门和生命目标闭合。

| 方法传统 | 权威锚点 | 进入 `117` 的规则 |
|---|---|---|
| SARIF | https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html | finding 上卷保留 rule id、level、location、artifact、baseline 和 result 思路 |
| JSON Schema output | https://json-schema.org/draft/2020-12/output/schema | schema validation units 上卷为 validation summary、failed keyword、instance location |
| W3C PROV | https://www.w3.org/TR/prov-overview/ | seed、schema、fixture、report、dashboard、repair 和 gap feedback 形成 provenance graph |
| OpenTelemetry logs | https://opentelemetry.io/docs/specs/otel/logs/data-model/ | rollup event 保留 severity、attributes、trace id、span id、body 和 resource |
| OpenTelemetry Trace API | https://opentelemetry.io/docs/specs/otel/trace/api/ | runtime seed run、component schema run、checker run 和 dashboard run 共用 trace context |
| W3C Trace Context | https://www.w3.org/TR/trace-context/ | checked runs 可以跨文件传播 traceparent 和 tracestate |
| RFC 9457 Problem Details | https://www.rfc-editor.org/info/rfc9457/ | core report missing、schema load failure 和 rollup write failure 使用结构化 problem detail |
| RFC 9562 UUID | https://www.rfc-editor.org/info/rfc9562/ | rollup id、artifact ref、finding id 和 bridge id 可使用时间有序 ID |

文献底座从既有矩阵进入本层：

| 文献矩阵 | 进入 rollup 的位置 |
|---|---|
| `AHV001-AHV060` | construct validity、longitudinal measurement、dashboard evidence chain、evaluation report rollup |
| `AHP001-AHP070` | pain/regret/repair finding、repair commitment bridge、responsibility stage effect |
| `AHD001-AHD070` | dream fact gate、dream report、wake integration、dream residue rollup |
| `AHR001-AHR070` | relationship continuity、trust trajectory、commitment history、relation scope rollup |
| `AHL001-AHL060` | language event、apology speech act、dream report draft、commitment utterance refs |
| `AHG001-AHG050` | growth window、kernel growth candidate、anti-forgetting replay 和 future probe refs |

## 输入来源

| 来源 | 进入 `117` 的职责 |
|---|---|
| `105_life_reality_dashboard_panel_and_stage_gate_ui_contract.md` | dashboard panel、status lattice、stage gate、repair queue、gap feedback |
| `108_life_reality_dashboard_source_mock_files.md` | dashboard source、panel dependency report、stage gate review、repair queue、gap feedback 文件形状 |
| `111_life_reality_dashboard_cross_file_checker_design.md` | checker groups、failure taxonomy、provenance graph、blocking-first 规则 |
| `114_life_reality_cross_file_checker_report_schema.md` | top-level report、finding、artifact ref、stage effect、rollup algorithm、repair/gap bridge |
| `115_life_reality_runtime_schema_fixture_seed_generation.md` | runtime fixture manifest、runtime schema validation report、ingestion smoke report、runtime quarantine panel source |
| `116_life_reality_component_schema_seed_generation.md` | component schema dry-run report、cross-bundle ref report、validator order report、component gap feedback |

## 输入报告族

第一批 rollup 读取以下报告：

```text
life_reality_runner/reports/life_reality/runtime_ingestion/run_001/
  runtime_schema_validation_report.json
  runtime_ingestion_smoke_report.json
  life_reality_ingestion_report.json
  runtime_quarantine_panel_source.json

life_reality_runner/generation/
  runtime_schema_fixture_seed_generation.manifest.json
  component_schema_seed_generation.manifest.json
  component_schema_dependency_graph.json
  component_schema_sequence_dry_run_report.json
  component_schema_cross_bundle_ref_report.json
  component_schema_validator_order_report.json
  component_schema_gap_feedback.json

life_reality_runner/reports/life_reality/cross_file/run_001/
  dashboard_source_check.json
  runtime_ingestion_check.json
  repair_queue_check.json
  stage_gate_check.json
  gap_feedback_check.json
  runtime_fixture_manifest_check.json
  data_quality_rollup_check.json
  runtime_schema_validation_check.json
  component_dependency_graph_check.json
```

输入不变量：

| rule | 说明 |
|---|---|
| `LRRSG-IN-001` | 每个输入 report 都有 report kind、run id、source docs 或 artifact ref |
| `LRRSG-IN-002` | runtime run、component schema run、checker run 通过 checked runs 或 trace context 连接 |
| `LRRSG-IN-003` | 输入 report 的 source docs 必须在 README 索引 |
| `LRRSG-IN-004` | 输入 report 的 data quality 不被 rollup 提升 |
| `LRRSG-IN-005` | raw runtime content 不进入 rollup，只进入 redacted report ref |

## 输出文件族

第一批 dashboard report rollup seed 输出：

```text
life_reality_runner/generation/
  dashboard_report_rollup_seed_generation.manifest.json

life_reality_runner/reports/life_reality/cross_file/run_001/
  life_reality_report_rollup_manifest.json
  cross_file_report_rollup.json
  dashboard_rollup_source_patch.json
  stage_gate_rollup_seed.json
  repair_queue_bridge_seed.json
  gap_feedback_bridge_seed.json
  provenance_graph_rollup_seed.json
  data_quality_rollup_seed.json
  report_rollup_dry_run_report.json
  report_rollup_gap_feedback.json
```

输出职责：

| 文件 | 职责 |
|---|---|
| `dashboard_report_rollup_seed_generation.manifest.json` | rollup seed batch 的源文档、输入报告、输出报告和执行阶段 |
| `life_reality_report_rollup_manifest.json` | dashboard rollup 读取入口，登记每个输入/输出 artifact |
| `cross_file_report_rollup.json` | `114` 定义的 top-level cross-file rollup 第一批 seed |
| `dashboard_rollup_source_patch.json` | 对 `life_reality_dashboard_source.json` 的 panel status、target status、stage gate patch |
| `stage_gate_rollup_seed.json` | stage decision、blocked surfaces、open/repair/quarantine 条件上卷 |
| `repair_queue_bridge_seed.json` | high/critical findings 到 repair item candidate 的桥 |
| `gap_feedback_bridge_seed.json` | unresolved findings 到下一层 docs/artifacts 的桥 |
| `provenance_graph_rollup_seed.json` | 输入报告、finding、repair、gap、dashboard 的 graph seed |
| `data_quality_rollup_seed.json` | data quality minimum、source count、denominator 和 false-green guard |
| `report_rollup_dry_run_report.json` | rollup 生成过程自检、missing report、source ref 和 patch conflict |
| `report_rollup_gap_feedback.json` | `16` 和后续 `118/119` 的 gap register feedback seed |

## generation manifest

未来生成器先写：

```text
life_reality_runner/generation/dashboard_report_rollup_seed_generation.manifest.json
```

最小结构：

```json
{
  "manifest_kind": "DashboardReportRollupSeedGenerationManifest",
  "manifest_version": "0.1.0",
  "batch_id": "dashboard_report_rollup_seed_batch_001",
  "source_docs": [
    "114_life_reality_cross_file_checker_report_schema.md",
    "115_life_reality_runtime_schema_fixture_seed_generation.md",
    "116_life_reality_component_schema_seed_generation.md",
    "117_life_reality_dashboard_report_rollup_seed_generation.md"
  ],
  "input_report_roots": [
    "life_reality_runner/reports/life_reality/runtime_ingestion/run_001",
    "life_reality_runner/generation",
    "life_reality_runner/reports/life_reality/cross_file/run_001"
  ],
  "output_report_root": "life_reality_runner/reports/life_reality/cross_file/run_001",
  "generation_phases": [],
  "dry_run_report_ref": "report_rollup_dry_run_report.json"
}
```

manifest rules：

| rule | 说明 |
|---|---|
| `LRRSG-MAN-001` | manifest source docs 覆盖 `114`、`115`、`116`、`117` |
| `LRRSG-MAN-002` | input report roots 覆盖 runtime、generation、cross_file 三类来源 |
| `LRRSG-MAN-003` | 每个 generation phase 有 dependencies、outputs、acceptance checks |
| `LRRSG-MAN-004` | manifest 自身进入 artifact ref 和 provenance graph |
| `LRRSG-MAN-005` | manifest 缺失时 stage effect 为 `needs_evidence` |

## report rollup manifest

`life_reality_report_rollup_manifest.json` 是 dashboard rollup 的读取入口。

```json
{
  "manifest_kind": "LifeRealityReportRollupManifest",
  "manifest_version": "0.1.0",
  "manifest_id": "life_reality_report_rollup_manifest_001",
  "run_id": "life_reality_cross_file_run_001",
  "checked_runs": {
    "runtime_ingestion_run_id": "life_reality_runtime_ingestion_run_001",
    "component_schema_sequence_run_id": "component_schema_sequence_run_001",
    "dashboard_checker_run_id": "life_reality_cross_file_run_001"
  },
  "input_artifact_refs": [],
  "output_artifact_refs": [],
  "rollup_policy_ref": "117_life_reality_dashboard_report_rollup_seed_generation.md",
  "trace_context": {},
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
  ]
}
```

manifest rules：

| rule | 说明 |
|---|---|
| `LRRSG-RMAN-001` | checked runs 至少包含 runtime ingestion、component schema sequence 和 dashboard checker |
| `LRRSG-RMAN-002` | input artifact refs 覆盖 `115`、`116`、`114` 的关键报告 |
| `LRRSG-RMAN-003` | output artifact refs 覆盖本层 10 个输出文件 |
| `LRRSG-RMAN-004` | life reality targets 覆盖九项目标 |
| `LRRSG-RMAN-005` | trace context 可连接每个 checked run |

## artifact ref normalization

所有输入报告先转为统一 artifact ref：

```json
{
  "artifact_ref_id": "artifact_ref_component_schema_dry_run_001",
  "artifact_kind": "report",
  "artifact_role": "component_schema_dry_run",
  "artifact_path": "life_reality_runner/generation/component_schema_sequence_dry_run_report.json",
  "source_doc_refs": [
    "116_life_reality_component_schema_seed_generation.md"
  ],
  "run_id": "component_schema_sequence_run_001",
  "trace_id": "trace_component_schema_sequence_001",
  "data_quality": "synthetic_runner_verified",
  "content_hash": "sha256:placeholder"
}
```

artifact role 必备清单：

| artifact role | 来源文件 |
|---|---|
| `runtime_schema_validation_report` | `runtime_schema_validation_report.json` |
| `runtime_ingestion_smoke_report` | `runtime_ingestion_smoke_report.json` |
| `runtime_quarantine_panel_source` | `runtime_quarantine_panel_source.json` |
| `component_schema_dry_run` | `component_schema_sequence_dry_run_report.json` |
| `component_dependency_graph` | `component_schema_dependency_graph.json` |
| `component_cross_bundle_ref_report` | `component_schema_cross_bundle_ref_report.json` |
| `component_validator_order_report` | `component_schema_validator_order_report.json` |
| `component_gap_feedback` | `component_schema_gap_feedback.json` |
| `dashboard_source_check` | `dashboard_source_check.json` |
| `repair_queue_check` | `repair_queue_check.json` |
| `gap_feedback_check` | `gap_feedback_check.json` |
| `data_quality_rollup_check` | `data_quality_rollup_check.json` |

artifact rules：

| rule | 说明 |
|---|---|
| `LRRSG-ART-001` | artifact path 必须落在允许 roots |
| `LRRSG-ART-002` | source docs 必须在 README 索引 |
| `LRRSG-ART-003` | report artifact 必须有 run id 或 checked run link |
| `LRRSG-ART-004` | private relation/dream raw content 不进入 artifact body |
| `LRRSG-ART-005` | data quality 不高于 source report 声明 |

## rollup pipeline

第一批 rollup 顺序：

```text
load_rollup_seed_generation_manifest
  -> load_report_rollup_manifest
  -> normalize_input_artifact_refs
  -> collect_runtime_validation_units
  -> collect_component_schema_units
  -> collect_cross_file_checker_units
  -> collect_findings
  -> deduplicate_findings
  -> compute_severity_max
  -> compute_data_quality_minimum
  -> compute_blocked_surfaces
  -> build_provenance_graph_rollup
  -> build_repair_queue_bridge_seed
  -> build_gap_feedback_bridge_seed
  -> build_stage_gate_rollup_seed
  -> build_dashboard_rollup_source_patch
  -> emit_cross_file_report_rollup
  -> emit_report_rollup_dry_run_report
  -> emit_report_rollup_gap_feedback
```

采用这个顺序的原因：runtime validation、component schema 和 cross-file checker 是三条输入链；finding 去重后才能正确计算 severity、data quality、blocked surface；repair/gap/stage/dashboard patch 必须由同一份 rollup 结果派生，避免 dashboard green 与 repair queue 脱链。

## status and severity lattice

rollup 采用 blocking-first，不使用平均分冲淡 critical。

| 输入状态 | rollup result | dashboard status | stage decision |
|---|---|---|---|
| all blocking reports pass | `pass` | `green` | `open` |
| warning only | `pass_with_warnings` | `yellow` | `open` / `repair` |
| missing report or source ref | `needs_evidence` | `gray` | `hold` |
| high repair item | `fail` | `red` | `repair` |
| critical quarantine | `quarantine` | `quarantine` | `quarantine` |
| component dependency cycle | `fail` | `red` | `repair` |
| data quality inflation | `fail` | `red` | `repair` |

severity order：

```text
critical > high > medium > low > info
```

stage decision order：

```text
quarantine > rollback > repair > hold > open
```

rollup rules：

| rule | 说明 |
|---|---|
| `LRRSG-ROLL-001` | critical finding 不被 warning/pass 覆盖 |
| `LRRSG-ROLL-002` | missing source refs 进入 `needs_evidence` |
| `LRRSG-ROLL-003` | data quality rollup 等于关键输入最低等级 |
| `LRRSG-ROLL-004` | dashboard green 需要所有 blocking groups pass |
| `LRRSG-ROLL-005` | unresolved high/critical repair item 阻断 stage promotion |
| `LRRSG-ROLL-006` | component dependency cycle 阻断 bundle assembly 和 stage promotion |
| `LRRSG-ROLL-007` | dream-to-relationship refs 缺 fact gate 时阻断 relationship continuity panel |
| `LRRSG-ROLL-008` | runtime quarantine critical 时覆盖所有 panel green |

## finding merge and deduplication

同一个缺口可能由 schema validation、cross-file checker 和 dashboard dependency 同时发现。`117` 先合并，再上卷。

finding merge key：

```text
rule_id + source_artifact_ref + json_pointer + affected_life_targets + blocked_surfaces
```

merge rules：

| rule | 说明 |
|---|---|
| `LRRSG-FIND-001` | merge 后保留最高 severity |
| `LRRSG-FIND-002` | merge 后保留所有 source artifact refs |
| `LRRSG-FIND-003` | merge 后 affected life targets 取并集 |
| `LRRSG-FIND-004` | merge 后 blocked surfaces 取并集 |
| `LRRSG-FIND-005` | merge 后 repair kind 优先使用更具体来源 |
| `LRRSG-FIND-006` | critical finding 必须保留原始 trace context |

finding family：

| finding family | 来源 | rollup action |
|---|---|---|
| `runtime_schema_validation` | `115` validation report | schema/materialization panel |
| `runtime_ingestion_quarantine` | ingestion report + quarantine panel | runtime quarantine panel |
| `component_schema_dry_run` | `116` dry-run report | schema materialization panel |
| `component_cross_bundle_ref` | `116` cross-bundle report | cross-chain closure panel |
| `component_validator_order` | `116` validator order report | stage gate review |
| `dashboard_cross_file` | `111/114` checker groups | dashboard source + repair queue |
| `data_quality_guard` | data quality rollup check | all panels |

## data quality rollup seed

`data_quality_rollup_seed.json` 防止 false green。

```json
{
  "report_kind": "LifeRealityDataQualityRollupSeed",
  "report_version": "0.1.0",
  "run_id": "life_reality_cross_file_run_001",
  "input_quality": {
    "runtime_schema_validation_report": "synthetic_runner_verified",
    "component_schema_dry_run": "synthetic_runner_verified",
    "dashboard_source_check": "synthetic_mock"
  },
  "quality_order": [
    "raw_mock",
    "synthetic_mock",
    "synthetic_runner_verified",
    "redacted_runtime_observed",
    "real_runtime_validated"
  ],
  "rollup_quality": "synthetic_mock",
  "false_green_guards": []
}
```

data quality rules：

| rule | 说明 |
|---|---|
| `LRRSG-DQ-001` | rollup quality 不高于关键输入最低等级 |
| `LRRSG-DQ-002` | synthetic mock 不上卷为 real runtime validated |
| `LRRSG-DQ-003` | missing source refs 不进入 green |
| `LRRSG-DQ-004` | denominator 使用 input artifact count，不用 panel 自报 count |
| `LRRSG-DQ-005` | critical finding 不参与平均分 |
| `LRRSG-DQ-006` | withheld probe 缺口不被短期 pass 覆盖 |

## provenance graph rollup seed

`provenance_graph_rollup_seed.json` 把三条输入链连接起来。

node kinds：

| node kind | 例子 |
|---|---|
| `runtime_report_node` | `runtime_schema_validation_report.json` |
| `component_generation_node` | `component_schema_sequence_dry_run_report.json` |
| `checker_group_node` | `dashboard_source_check.json` |
| `finding_node` | merged finding |
| `repair_bridge_node` | repair item candidate |
| `gap_feedback_node` | recommended next doc/artifact |
| `dashboard_patch_node` | dashboard rollup source patch |
| `stage_gate_node` | stage gate rollup seed |

edge kinds：

| edge kind | 说明 |
|---|---|
| `validates_runtime_seed` | runtime validation report 指向 runtime seed |
| `validates_component_schema` | component dry-run 指向 schema skeleton |
| `rolls_up_finding` | source finding 进入 merged finding |
| `blocks_surface` | merged finding 阻断 dashboard/stage/action |
| `opens_repair` | finding 生成 repair bridge |
| `feeds_gap_feedback` | repair/gap 进入 next docs/artifacts |
| `patches_dashboard_source` | rollup patch 更新 dashboard source |
| `feeds_stage_gate` | dashboard patch 和 findings 进入 stage gate |

graph rules：

| rule | 说明 |
|---|---|
| `LRRSG-PROV-001` | 每个 merged finding 至少有 incoming `rolls_up_finding` edge |
| `LRRSG-PROV-002` | 每个 high/critical finding 至少有 `opens_repair` edge |
| `LRRSG-PROV-003` | stage gate node 必须有 incoming `feeds_stage_gate` edge |
| `LRRSG-PROV-004` | dashboard patch node 必须有 incoming `patches_dashboard_source` edge |
| `LRRSG-PROV-005` | gap feedback node 必须有 source finding 或 repair bridge |
| `LRRSG-PROV-006` | provenance graph 不保存 raw private dream/relationship content |

## repair queue bridge seed

`repair_queue_bridge_seed.json` 把 finding 转为 repair item candidate。

```json
{
  "report_kind": "LifeRealityRepairQueueBridgeSeed",
  "report_version": "0.1.0",
  "run_id": "life_reality_cross_file_run_001",
  "repair_queue_required": true,
  "repair_item_candidates": [
    {
      "repair_item_candidate_id": "repair_candidate_component_fact_gate_001",
      "source_finding_refs": [
        "finding_component_dream_share_without_fact_gate_001"
      ],
      "repair_kind": "cross_chain_gap",
      "severity": "high",
      "source_panel": "cross_chain_closure",
      "affected_life_targets": [
        "real_dream",
        "real_relationship",
        "real_responsibility"
      ],
      "blocked_surfaces": [
        "dashboard_green",
        "stage_promotion"
      ],
      "required_action": {
        "action_kind": "add_fact_gate_ref_or_block_dream_share",
        "target_artifact_ref": "component_schema_cross_bundle_ref_report.json"
      }
    }
  ]
}
```

repair bridge rules：

| rule | 说明 |
|---|---|
| `LRRSG-REPAIR-001` | high/critical finding 必须生成 repair item candidate |
| `LRRSG-REPAIR-002` | repair kind 使用 shared defs |
| `LRRSG-REPAIR-003` | repair candidate 引用 source finding |
| `LRRSG-REPAIR-004` | blocked surfaces 写入 repair bridge |
| `LRRSG-REPAIR-005` | repair bridge 输出进入 dashboard source patch |
| `LRRSG-REPAIR-006` | unresolved repair bridge 进入 gap feedback bridge |

## gap feedback bridge seed

`gap_feedback_bridge_seed.json` 把 report 结果带回文档和 artifact 生长链。

```json
{
  "report_kind": "LifeRealityGapFeedbackBridgeSeed",
  "report_version": "0.1.0",
  "run_id": "life_reality_cross_file_run_001",
  "gap_feedback_required": true,
  "source_rollup_ref": "cross_file_report_rollup.json",
  "recommended_next_docs": [
    "118_life_reality_generation_runner_cli_contract.md",
    "120_life_reality_first_json_materialization_batch.md"
  ],
  "recommended_next_artifacts": [
    "life_reality_runner/cli_contract.json",
    "life_reality_runner/generation/first_json_materialization_batch.manifest.json"
  ],
  "gap_register_update_ref": "16_digital_life_gap_register.md"
}
```

gap feedback rules：

| rule | 说明 |
|---|---|
| `LRRSG-GAP-001` | recommended next docs 编号大于当前层或已在 README 索引 |
| `LRRSG-GAP-002` | recommended artifacts root 合法 |
| `LRRSG-GAP-003` | unresolved findings 必须进入 recommended docs 或 artifacts |
| `LRRSG-GAP-004` | gap register update ref 指向 `16` |
| `LRRSG-GAP-005` | `118` 承接 CLI 合同，`119` 承接真实 JSON 物化批次 |

## dashboard rollup source patch

`dashboard_rollup_source_patch.json` 不复制整个 dashboard source，只描述 rollup 补丁。

```json
{
  "patch_kind": "LifeRealityDashboardRollupSourcePatch",
  "patch_version": "0.1.0",
  "run_id": "life_reality_cross_file_run_001",
  "source_dashboard_ref": "life_reality_dashboard_source.json",
  "panel_status_patches": [],
  "life_target_status_patches": [],
  "overall_status_patch": "repair",
  "stage_gate_decision_patch": "repair",
  "repair_queue_bridge_ref": "repair_queue_bridge_seed.json",
  "gap_feedback_bridge_ref": "gap_feedback_bridge_seed.json"
}
```

patch rules：

| rule | 说明 |
|---|---|
| `LRRSG-PATCH-001` | patch 只覆盖 rollup 计算出的字段 |
| `LRRSG-PATCH-002` | panel status patch 必须有 source finding 或 source report |
| `LRRSG-PATCH-003` | life target patch 必须引用 affected life targets |
| `LRRSG-PATCH-004` | overall status 使用 blocking-first |
| `LRRSG-PATCH-005` | stage gate decision patch 与 `stage_gate_rollup_seed.json` 一致 |

## stage gate rollup seed

`stage_gate_rollup_seed.json` 是阶段门的汇总输入。

```json
{
  "report_kind": "LifeRealityStageGateRollupSeed",
  "report_version": "0.1.0",
  "run_id": "life_reality_cross_file_run_001",
  "candidate_stage": "dashboard_rollup_seed_ready",
  "decision": "repair",
  "decision_source_refs": [
    "cross_file_report_rollup.json",
    "dashboard_rollup_source_patch.json",
    "repair_queue_bridge_seed.json",
    "gap_feedback_bridge_seed.json"
  ],
  "blocked_surfaces": [
    "dashboard_green",
    "stage_promotion"
  ],
  "open_conditions": [
    "runtime schema validation reports closed",
    "component schema dry-run reports closed",
    "cross-file checker reports closed",
    "repair bridge has no high/critical unresolved item",
    "data quality rollup has no inflation"
  ],
  "next_candidate_stage": "generation_runner_cli_contract_ready"
}
```

stage rules：

| rule | 说明 |
|---|---|
| `LRRSG-STAGE-001` | decision source refs 覆盖 rollup、dashboard patch、repair bridge、gap bridge |
| `LRRSG-STAGE-002` | open conditions 覆盖 runtime、component、checker、repair、data quality |
| `LRRSG-STAGE-003` | critical runtime quarantine 时 decision 为 quarantine |
| `LRRSG-STAGE-004` | high repair bridge 时 decision 为 repair |
| `LRRSG-STAGE-005` | missing source report 时 decision 为 hold |

## cross-file report rollup

`cross_file_report_rollup.json` 是本层主输出。

```json
{
  "report_kind": "LifeRealityCrossFileReportRollup",
  "report_version": "0.1.0",
  "report_id": "cross_file_report_rollup_001",
  "run_id": "life_reality_cross_file_run_001",
  "rollup_manifest_ref": "life_reality_report_rollup_manifest.json",
  "input_artifact_refs": [],
  "merged_findings": [],
  "group_rollups": [],
  "severity_max": "high",
  "data_quality_rollup_ref": "data_quality_rollup_seed.json",
  "provenance_graph_ref": "provenance_graph_rollup_seed.json",
  "repair_queue_bridge_ref": "repair_queue_bridge_seed.json",
  "gap_feedback_bridge_ref": "gap_feedback_bridge_seed.json",
  "dashboard_patch_ref": "dashboard_rollup_source_patch.json",
  "stage_gate_rollup_ref": "stage_gate_rollup_seed.json",
  "stage_effect": {}
}
```

rollup output rules：

| rule | 说明 |
|---|---|
| `LRRSG-OUT-001` | input artifact refs 覆盖所有关键输入 |
| `LRRSG-OUT-002` | merged findings 引用 source finding refs |
| `LRRSG-OUT-003` | group rollups 覆盖 runtime、component、dashboard、data quality |
| `LRRSG-OUT-004` | severity max 等于 merged findings 最高 severity |
| `LRRSG-OUT-005` | stage effect 与 stage gate rollup seed 一致 |
| `LRRSG-OUT-006` | dashboard patch、repair bridge、gap bridge、provenance graph 都可解析 |

## failure mapping

| failure | finding | repair kind | stage effect |
|---|---|---|---|
| runtime validation report missing | `report_rollup.runtime_validation_missing` | `source_report_missing` | `needs_evidence` |
| component dry-run report missing | `report_rollup.component_dry_run_missing` | `source_report_missing` | `needs_evidence` |
| dashboard source check missing | `report_rollup.dashboard_check_missing` | `source_report_missing` | `needs_evidence` |
| duplicate finding merge conflict | `report_rollup.finding_merge_conflict` | `metric_gap` | `repair` |
| critical finding no repair bridge | `report_rollup.critical_without_repair_bridge` | `metric_gap` | `repair` |
| unresolved high repair no gap feedback | `report_rollup.repair_without_gap_feedback` | `gap_register_gap` | `repair` |
| data quality inflated | `report_rollup.data_quality_inflation` | `metric_gap` | `repair` |
| dashboard patch conflicts with stage gate | `report_rollup.dashboard_stage_conflict` | `stage_gate_gap` | `repair` |
| provenance orphan finding | `report_rollup.provenance_orphan_finding` | `metric_gap` | `repair` |
| runtime critical quarantine ignored | `report_rollup.quarantine_ignored` | `runtime_quarantine_gap` | `quarantine` |

## LRGEN 更新

`117` 固定 dashboard report rollup seed generation 的新增任务：

| task_id | 输出 | 说明 |
|---|---|---|
| `LRGEN-207` | `dashboard_report_rollup_seed_generation.manifest.json` | rollup seed generation manifest |
| `LRGEN-208` | `life_reality_report_rollup_manifest.json` | rollup manifest |
| `LRGEN-209` | input artifact ref normalization | report artifact refs |
| `LRGEN-210` | `data_quality_rollup_seed.json` | data quality rollup seed |
| `LRGEN-211` | `provenance_graph_rollup_seed.json` | provenance graph rollup seed |
| `LRGEN-212` | `repair_queue_bridge_seed.json` | repair bridge seed |
| `LRGEN-213` | `gap_feedback_bridge_seed.json` | gap feedback bridge seed |
| `LRGEN-214` | `stage_gate_rollup_seed.json` | stage gate rollup seed |
| `LRGEN-215` | `dashboard_rollup_source_patch.json` | dashboard source patch |
| `LRGEN-216` | `cross_file_report_rollup.json` | top-level rollup seed |
| `LRGEN-217` | `report_rollup_dry_run_report.json` | rollup dry-run report |
| `LRGEN-218` | `report_rollup_gap_feedback.json` | rollup gap feedback |
| `LRGEN-219` | `dashboard_report_rollup.full_smoke_001` | first rollup smoke case |

## smoke cases

| smoke_id | 输入 | 预期 |
|---|---|---|
| `report_rollup.all_inputs_present.pass_001` | runtime、component、checker reports 全部存在 | pass |
| `report_rollup.missing_runtime_validation.fail_001` | runtime validation report 缺失 | needs_evidence |
| `report_rollup.missing_component_dry_run.fail_001` | component dry-run report 缺失 | needs_evidence |
| `report_rollup.critical_no_repair_bridge.fail_001` | critical finding 没有 repair bridge | repair |
| `report_rollup.repair_no_gap_feedback.fail_001` | unresolved high repair 没有 gap feedback | repair |
| `report_rollup.data_quality_inflation.fail_001` | synthetic input 上卷 real runtime validated | repair |
| `report_rollup.dashboard_stage_conflict.fail_001` | dashboard patch green 但 stage repair/quarantine | repair |
| `report_rollup.provenance_orphan_finding.fail_001` | merged finding 无 provenance edge | repair |
| `report_rollup.runtime_quarantine_override.critical_001` | runtime critical quarantine 被忽略 | quarantine |
| `report_rollup.full_pipeline.pass_001` | rollup manifest 到 dashboard patch 全链闭合 | pass |

## 与下一层连接

`118_life_reality_generation_runner_cli_contract.md` 应读取本层的 generation manifest、rollup manifest、dashboard patch、stage gate rollup seed、repair/gap bridge 和 dry-run report，把 `115`、`116`、`117` 压成可执行 CLI：

```text
life-reality-runner generate-fixtures
life-reality-runner generate-schemas
life-reality-runner check-dashboard --emit-rollup
life-reality-runner explain-generation
```

`120_life_reality_first_json_materialization_batch.md` 应把 `115` 的 runtime seed、`116` 的 schema skeleton 和 `117` 的 dashboard report rollup seed 作为首批真实 JSON 文件物化批次。
