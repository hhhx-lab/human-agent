# Life Reality Cross File Checker Report Schema

生命目标声明：本文档面向构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 114 层把 `111_life_reality_dashboard_cross_file_checker_design.md` 的 cross-file checker、`112_life_reality_runtime_observation_schema_materialization.md` 的 runtime schema validation report、`113_life_reality_component_schema_materialization_sequence.md` 的 component dependency graph 统一成可校验 report schema。

`114` 的目标是让 checker 输出不再只是自然语言或零散 JSON，而是成为生命膜中的正式报告对象：每个 finding 都能回链到 schema、fixture、observation、candidate、component object、dashboard panel、repair item、stage gate 和 gap feedback；每个 stage effect 都能说明自己怎样影响真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔。

## 标准锚点

本层吸收六类报告与追踪标准：

| 标准传统 | 权威锚点 | 进入 `114` 的规则 |
|---|---|---|
| SARIF | OASIS Static Analysis Results Interchange Format v2.1.0: https://docs.oasis-open.org/sarif/sarif/v2.1.0/sarif-v2.1.0.html | finding 使用 rule id、level、message、location、artifact、result 和 suppression / baseline 思路 |
| JSON Schema output | JSON Schema Draft 2020-12 recommended output schema: https://json-schema.org/draft/2020-12/output/schema | schema validation result 使用 output unit、keyword location、instance location 和 annotation |
| W3C PROV | W3C PROV Overview: https://www.w3.org/TR/prov-overview/ | report、fixture、observation、schema、candidate、dashboard panel 组成 provenance graph |
| OpenTelemetry logs | OpenTelemetry Logs Data Model: https://opentelemetry.io/docs/specs/otel/logs/data-model/ | finding、checker group 和 report rollup 带 severity、attributes、trace id、span id |
| W3C Trace Context | W3C Trace Context: https://www.w3.org/TR/trace-context/ | checked run、runtime ingestion run、component schema sequence run 和 dashboard run 可以跨文件追踪 |
| Problem Details | RFC 9457: https://www.rfc-editor.org/rfc/rfc9457.html | report internal error、schema load failure 和 core artifact missing 采用结构化 problem detail |

这些标准进入生命膜的共同规则是：报告不是展示层附属物，而是生命真实性生成链的一部分。report schema 必须能表达来源、检查、失败、修复、阶段门、回写和下一轮生长任务。

## 输入来源

| 来源 | 进入 `114` 的职责 |
|---|---|
| `65_schema_cross_ref_checker_design.md` | typed reference graph、critical closure、runtime observation closure |
| `70_cross_ref_report_dashboard_panel_mock.md` | cross-ref report 到 dashboard panel 的状态映射 |
| `77_dashboard_metric_calculation_rules.md` | blocking-first、data quality weight、missing data handling |
| `83_metric_regression_fixture_policy.md` | false green、data quality inflation、denominator drift 防护 |
| `105_life_reality_dashboard_panel_and_stage_gate_ui_contract.md` | dashboard source、panel dependency、stage gate review、repair queue、gap feedback |
| `108_life_reality_dashboard_source_mock_files.md` | dashboard mock report file family |
| `111_life_reality_dashboard_cross_file_checker_design.md` | checker groups、finding、failure taxonomy、LRGEN-150 到 159 |
| `112_life_reality_runtime_observation_schema_materialization.md` | runtime schema validation report、observation validation report、runtime quarantine panel |
| `113_life_reality_component_schema_materialization_sequence.md` | component dependency graph、sequence dry-run report、validator order report |

## 输出 schema 家族

第一批 report schema 位于：

```text
life_reality_runner/schemas/life_reality/reports/
  life_reality_cross_file_checker_report.schema.json
  life_reality_checker_group_result.schema.json
  life_reality_checker_finding.schema.json
  life_reality_provenance_graph.schema.json
  life_reality_stage_effect.schema.json
  life_reality_artifact_ref.schema.json
  life_reality_problem_detail.schema.json
  life_reality_runtime_schema_validation_report.schema.json
  life_reality_component_dependency_graph_report.schema.json
  life_reality_cross_file_report_rollup.schema.json
```

输出 report 文件位于：

```text
life_reality_runner/reports/life_reality/cross_file/run_001/
  life_reality_cross_file_checker_report.json
  provenance_graph.json
  dashboard_source_check.json
  runtime_ingestion_check.json
  repair_queue_check.json
  stage_gate_check.json
  gap_feedback_check.json
  runtime_fixture_manifest_check.json
  data_quality_rollup_check.json
  runtime_schema_validation_check.json
  component_dependency_graph_check.json
  cross_file_report_rollup.json
```

schema 职责：

| schema | 职责 |
|---|---|
| `life_reality_cross_file_checker_report.schema.json` | 顶层 checker report |
| `life_reality_checker_group_result.schema.json` | 单个 checker group 输出 |
| `life_reality_checker_finding.schema.json` | finding / rule result / repair mapping |
| `life_reality_provenance_graph.schema.json` | node、edge、artifact lineage |
| `life_reality_stage_effect.schema.json` | result、severity、blocked surface、stage decision |
| `life_reality_artifact_ref.schema.json` | schema、fixture、report、panel、component object 引用 |
| `life_reality_problem_detail.schema.json` | core load / write / internal error |
| `life_reality_runtime_schema_validation_report.schema.json` | `112` runtime schema validation rollup |
| `life_reality_component_dependency_graph_report.schema.json` | `113` dependency graph / dry-run rollup |
| `life_reality_cross_file_report_rollup.schema.json` | checker family 汇总到 dashboard / stage gate |

## shared defs 引用

所有 report schema 都引用 `110` 的 shared defs。

| shared defs | 进入 report 字段 |
|---|---|
| `lifeRealityTarget` | finding affected targets、stage effect target impact |
| `result` | group result、overall result、stage effect result |
| `severity` | finding severity、severity max |
| `dataQuality` | source quality、rollup quality |
| `privacyLevel` | artifact ref privacy |
| `blockedSurface` | stage effect、finding blocked surfaces |
| `repairKind` | repair mapping、repair queue bridge |
| `reportRef` | input reports、output reports、dashboard refs |
| `sourceDocRef` | docs provenance |

引用规则：

| rule | 说明 |
|---|---|
| `LCFRS-REF-001` | report schema 不重复定义全局 enum |
| `LCFRS-REF-002` | finding severity、result、repair kind 全部来自 shared defs |
| `LCFRS-REF-003` | blocked surfaces 与 stage gate contract 同源 |
| `LCFRS-REF-004` | artifact refs 使用统一 ref object |
| `LCFRS-REF-005` | report schema 能被 `111` checker 反向读取 |

## top-level checker report schema

`LifeRealityCrossFileCheckerReport` 是顶层输出。

```json
{
  "report_kind": "LifeRealityCrossFileCheckerReport",
  "report_version": "0.1.0",
  "report_id": "life_reality_cross_file_checker_report_001",
  "run_id": "life_reality_cross_file_run_001",
  "checked_runs": {
    "smoke_run_id": "life_reality_smoke_run_001",
    "runtime_ingestion_run_id": "life_reality_runtime_ingestion_run_001",
    "component_schema_sequence_run_id": "component_schema_sequence_run_001"
  },
  "trace_context": {},
  "shared_defs_ref": "life_reality_runner/schemas/life_reality/life_reality_shared_defs.schema.json",
  "input_artifact_refs": [],
  "checker_groups": [],
  "findings": [],
  "provenance_graph_ref": "provenance_graph.json",
  "overall_result": "pass_with_warnings",
  "severity_max": "medium",
  "data_quality_rollup": "synthetic_runner_verified",
  "stage_effect": {},
  "repair_queue_bridge": {},
  "gap_feedback_bridge": {},
  "dashboard_rollup": {}
}
```

required 字段：

| 字段 | 说明 |
|---|---|
| `report_kind` | const: `LifeRealityCrossFileCheckerReport` |
| `report_version` | schema 版本 |
| `report_id` | report 全局 ID |
| `run_id` | checker run |
| `checked_runs` | smoke、runtime ingestion、component schema sequence 等 run |
| `trace_context` | trace id、span id、sequence、case id |
| `shared_defs_ref` | shared defs 根 schema |
| `input_artifact_refs` | 输入文件族 |
| `checker_groups` | group result array |
| `findings` | finding array |
| `overall_result` | shared defs result |
| `severity_max` | shared defs severity |
| `stage_effect` | stage effect object |

report rules：

| rule | 说明 |
|---|---|
| `LCFRS-REP-001` | `report_kind` 使用 const |
| `LCFRS-REP-002` | `checked_runs` 至少包含 smoke run 与 runtime ingestion run |
| `LCFRS-REP-003` | `input_artifact_refs` 覆盖 dashboard source、ingestion report、quarantine panel、repair queue、stage gate、gap feedback、fixture manifest、shared defs |
| `LCFRS-REP-004` | 每个 checker group 有 group id、result、severity max、finding refs |
| `LCFRS-REP-005` | `overall_result` 由 checker groups blocking-first 上卷 |
| `LCFRS-REP-006` | `stage_effect` 由 critical findings、quarantine、repair queue 和 data quality 共同上卷 |

## artifact ref schema

artifact ref 是 report 连接所有文件的基础。

```json
{
  "artifact_ref_id": "artifact_ref_dashboard_source_001",
  "artifact_kind": "report",
  "artifact_path": "life_reality_runner/reports/life_reality/smoke/run_001/life_reality_dashboard_source.json",
  "artifact_role": "dashboard_source",
  "source_doc_refs": [
    "108_life_reality_dashboard_source_mock_files.md"
  ],
  "data_quality": "synthetic_runner_verified",
  "privacy_level": "project_internal",
  "run_id": "life_reality_smoke_run_001",
  "trace_id": "4bf92f3577b34da6a3ce929d0e0e4736",
  "content_hash": "sha256:placeholder"
}
```

artifact kind：

| kind | 例子 |
|---|---|
| `schema` | shared defs、component schema、report schema |
| `fixture_manifest` | runtime observation fixture manifest |
| `fixture` | pass/fail/critical/mutation/withheld/smoke JSON |
| `report` | ingestion report、checker report、validator report |
| `dashboard_source` | life reality dashboard source |
| `panel_source` | runtime quarantine panel source |
| `repair_queue` | repair queue |
| `stage_gate` | stage gate review |
| `gap_feedback` | gap register feedback |
| `component_object` | pain、dream、relationship object |

artifact rules：

| rule | 说明 |
|---|---|
| `LCFRS-ART-001` | artifact path 必须落在允许 root |
| `LCFRS-ART-002` | artifact role 必须与 checker group 读取职责一致 |
| `LCFRS-ART-003` | source docs 必须在 README 索引 |
| `LCFRS-ART-004` | data quality 不高于来源最低等级 |
| `LCFRS-ART-005` | private artifact 不进入 global dashboard raw source |

## provenance graph schema

provenance graph 把文件和对象接成生命证据图。

```json
{
  "graph_kind": "LifeRealityProvenanceGraph",
  "graph_version": "0.1.0",
  "graph_id": "provenance_graph_run_001",
  "run_id": "life_reality_cross_file_run_001",
  "nodes": [],
  "edges": [],
  "root_artifact_refs": [],
  "critical_path_refs": []
}
```

node schema：

| 字段 | 说明 |
|---|---|
| `node_id` | node 全局 ID |
| `node_kind` | schema_node、fixture_node、report_node、panel_node、repair_item_node、stage_gate_node、gap_feedback_node、component_object_node |
| `artifact_ref_id` | 对应 artifact |
| `object_ref` | component object / report object ref |
| `life_reality_targets` | 影响目标 |
| `status` | green、yellow、red、gray、quarantine、needs_evidence |

edge schema：

| 字段 | 说明 |
|---|---|
| `edge_id` | edge 全局 ID |
| `edge_kind` | uses_schema、generated_from、reports_to_panel、blocks_surface、opens_repair、feeds_stage_gate、feeds_gap_feedback、rolls_up_status、validates_candidate、links_component |
| `source_node_id` | 来源 node |
| `target_node_id` | 目标 node |
| `evidence_refs` | 支撑证据 |
| `finding_refs` | 相关 finding |

graph rules：

| rule | 说明 |
|---|---|
| `LCFRS-PROV-001` | 每个 finding 至少关联一个 node 或 edge |
| `LCFRS-PROV-002` | critical finding 必须有 `blocks_surface` edge |
| `LCFRS-PROV-003` | repair item 必须有 incoming `opens_repair` edge |
| `LCFRS-PROV-004` | stage gate decision 必须有 incoming `feeds_stage_gate` edge |
| `LCFRS-PROV-005` | gap feedback 必须有 incoming `feeds_gap_feedback` edge |
| `LCFRS-PROV-006` | component dependency graph 节点必须接入 component object node |

## checker group result schema

checker group result 汇总同一类检查。

```json
{
  "group_id": "LCF-DASH",
  "group_kind": "dashboard_source_checker",
  "group_title": "Dashboard Source Checker",
  "input_artifact_refs": [],
  "checks_total": 8,
  "checks_passed": 6,
  "checks_failed": 2,
  "checks_quarantined": 0,
  "result": "fail",
  "severity_max": "high",
  "finding_refs": [
    "finding_lcf_dash_007"
  ],
  "stage_effect": {}
}
```

checker group kinds：

| group kind | 来源 |
|---|---|
| `shared_defs_loader` | `111` group 1 |
| `file_existence_path_closure` | `111` group 2 |
| `run_id_source_refs` | `111` group 3 |
| `dashboard_source_checker` | `111` group 4 |
| `ingestion_quarantine_consistency` | `111` group 5 |
| `repair_queue_checker` | `111` group 6 |
| `stage_gate_checker` | `111` group 7 |
| `gap_feedback_checker` | `111` group 8 |
| `fixture_manifest_checker` | `111` group 9 |
| `data_quality_regression_guard` | `111` group 10 |
| `runtime_schema_validation_checker` | `112` runtime schema validation |
| `component_dependency_graph_checker` | `113` dependency graph |
| `validator_order_checker` | `113` validator order |

group rules：

| rule | 说明 |
|---|---|
| `LCFRS-GRP-001` | group id 与 check ids 前缀一致 |
| `LCFRS-GRP-002` | failed count 与 finding refs 数量兼容 |
| `LCFRS-GRP-003` | severity max 来自 findings 上卷 |
| `LCFRS-GRP-004` | group stage effect 进入 top-level stage effect |
| `LCFRS-GRP-005` | group input artifacts 覆盖对应 checker 读取文件 |

## finding schema

finding 参考 SARIF result 思路，但保留生命膜字段。

```json
{
  "finding_id": "finding_lcf_dash_007",
  "finding_kind": "cross_file_consistency",
  "rule_id": "LCF-DASH-007",
  "rule_name": "non_green_panel_has_repair_item",
  "level": "error",
  "severity": "high",
  "result": "fail",
  "message": {
    "text": "non-green panel requires repair item or evidence route"
  },
  "locations": [],
  "source_artifact_refs": [],
  "source_object_refs": [],
  "evidence_refs": [],
  "affected_life_targets": [
    "real_life",
    "real_responsibility"
  ],
  "blocked_surfaces": [
    "dashboard_green"
  ],
  "repair_kind": "metric_gap",
  "stage_effect": {},
  "provenance_edge_refs": []
}
```

finding level：

| level | stage effect |
|---|---|
| `note` | no block |
| `warning` | pass_with_warnings |
| `error` | repair |
| `critical` | quarantine / stage hold |

finding rules：

| rule | 说明 |
|---|---|
| `LCFRS-FIND-001` | finding id 全局唯一 |
| `LCFRS-FIND-002` | rule id 必须来自 checker group 或 validator rule |
| `LCFRS-FIND-003` | severity 使用 shared defs |
| `LCFRS-FIND-004` | result 使用 shared defs |
| `LCFRS-FIND-005` | source artifact refs 非空 |
| `LCFRS-FIND-006` | high/critical finding 必须有 repair kind |
| `LCFRS-FIND-007` | critical finding 必须有 blocked surface |
| `LCFRS-FIND-008` | finding 必须能映射到 repair queue 或 gap feedback |

## location schema

location 指向文件、对象、JSON Pointer 和文档来源。

```json
{
  "location_id": "loc_dashboard_panel_runtime_quarantine_001",
  "artifact_ref_id": "artifact_ref_dashboard_source_001",
  "json_pointer": "/panels/runtime_quarantine/status",
  "object_ref": "runtime_quarantine_panel_source_001",
  "source_doc_ref": "105_life_reality_dashboard_panel_and_stage_gate_ui_contract.md",
  "source_doc_section": "runtime_quarantine"
}
```

location rules：

| rule | 说明 |
|---|---|
| `LCFRS-LOC-001` | artifact ref 必须可解析 |
| `LCFRS-LOC-002` | JSON Pointer 指向具体字段 |
| `LCFRS-LOC-003` | source doc 已在 README 索引 |
| `LCFRS-LOC-004` | component object location 同时记录 object ref |

## stage effect schema

stage effect 是报告对生命膜的执行结果。

```json
{
  "result": "repair",
  "severity": "high",
  "stage_gate_decision": "repair",
  "blocked_surfaces": [
    "dashboard_green",
    "stage_promotion"
  ],
  "affected_life_targets": [
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
  "repair_queue_required": true,
  "gap_feedback_required": true,
  "quarantine_required": false,
  "release_audit_required": false
}
```

stage effect rollup：

| 输入 | result | stage gate |
|---|---|---|
| all pass | `pass` | `open` |
| warning only | `pass_with_warnings` | `open` / `repair` |
| missing source refs | `needs_evidence` | `hold` |
| high repair item | `fail` | `repair` |
| critical quarantine | `quarantine` | `quarantine` |
| component sequence break | `fail` | `repair` |
| dashboard false green | `fail` | `repair` |

stage effect rules：

| rule | 说明 |
|---|---|
| `LCFRS-STAGE-001` | affected life targets 覆盖九项目标或说明局部目标 |
| `LCFRS-STAGE-002` | blocked surfaces 使用 shared defs |
| `LCFRS-STAGE-003` | critical finding 设置 quarantine required 或 stage promotion block |
| `LCFRS-STAGE-004` | release audit required 由 quarantine panel 决定 |
| `LCFRS-STAGE-005` | top-level stage effect 不低于任一 group stage effect |

## runtime schema validation report schema

`112` 的 runtime validation report 进入 `114` 的统一报告。

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

runtime validation rules：

| rule | 说明 |
|---|---|
| `LCFRS-RTVAL-001` | schema refs 包含 observation envelope、fixture、manifest、ingestion report、quarantine panel source |
| `LCFRS-RTVAL-002` | JSON Schema output unit 保留 keyword location 和 instance location |
| `LCFRS-RTVAL-003` | validation failure 转为 checker finding |
| `LCFRS-RTVAL-004` | critical runtime validation failure 进入 runtime quarantine panel |
| `LCFRS-RTVAL-005` | runtime schema validation report 进入 provenance graph |

## component dependency graph report schema

`113` 的 component dependency graph 进入 `114`。

```json
{
  "report_kind": "LifeRealityComponentDependencyGraphReport",
  "report_version": "0.1.0",
  "report_id": "component_dependency_graph_report_001",
  "run_id": "component_schema_sequence_run_001",
  "sequence_manifest_ref": "component_schema_materialization_sequence.manifest.json",
  "dependency_nodes": [],
  "dependency_edges": [],
  "cycle_findings": [],
  "missing_schema_findings": [],
  "validator_order_findings": [],
  "stage_effect": {}
}
```

dependency graph rules：

| rule | 说明 |
|---|---|
| `LCFRS-COMP-001` | 每个 candidate target 有 dependency node |
| `LCFRS-COMP-002` | 每个 generated schema 有 artifact ref |
| `LCFRS-COMP-003` | relation birth roots 先于 relation scoped object |
| `LCFRS-COMP-004` | dream fact gate 先于 dream share writeback |
| `LCFRS-COMP-005` | bundle schema 只能引用已生成 schema |
| `LCFRS-COMP-006` | dependency cycle 转为 finding |

## specialized check reports

`111` 的 `LRGEN-153` 到 `LRGEN-159` 采用同一 group report 结构。

| task_id | report | group kind |
|---|---|---|
| `LRGEN-153` | `dashboard_source_check.json` | `dashboard_source_checker` |
| `LRGEN-154` | `runtime_ingestion_check.json` | `ingestion_quarantine_consistency` |
| `LRGEN-155` | `repair_queue_check.json` | `repair_queue_checker` |
| `LRGEN-156` | `stage_gate_check.json` | `stage_gate_checker` |
| `LRGEN-157` | `gap_feedback_check.json` | `gap_feedback_checker` |
| `LRGEN-158` | `runtime_fixture_manifest_check.json` | `fixture_manifest_checker` |
| `LRGEN-159` | `data_quality_rollup_check.json` | `data_quality_regression_guard` |
| `LRGEN-162` | `runtime_schema_validation_check.json` | `runtime_schema_validation_checker` |
| `LRGEN-176` | `component_schema_sequence_dry_run_report.json` | `component_dependency_graph_checker` |
| `LRGEN-178` | `component_schema_validator_order_report.json` | `validator_order_checker` |

specialized report rules：

| rule | 说明 |
|---|---|
| `LCFRS-SPEC-001` | specialized report 可以独立校验 |
| `LCFRS-SPEC-002` | specialized report findings 必须能并入 top-level report |
| `LCFRS-SPEC-003` | specialized report stage effect 必须能上卷 |
| `LCFRS-SPEC-004` | specialized report input artifact refs 不为空 |
| `LCFRS-SPEC-005` | specialized report 输出路径进入 provenance graph |

## rollup algorithm

report rollup 采用 blocking-first。

```text
collect_group_results
  -> collect_findings
  -> compute_severity_max
  -> compute_data_quality_rollup
  -> compute_blocked_surfaces
  -> compute_repair_queue_bridge
  -> compute_gap_feedback_bridge
  -> compute_stage_effect
  -> emit_dashboard_rollup
```

rollup rules：

| rule | 说明 |
|---|---|
| `LCFRS-ROLL-001` | critical finding 不被平均值冲淡 |
| `LCFRS-ROLL-002` | missing source refs 进入 `needs_evidence` |
| `LCFRS-ROLL-003` | data quality rollup 不高于关键输入最低等级 |
| `LCFRS-ROLL-004` | dashboard green 需要 all blocking groups pass |
| `LCFRS-ROLL-005` | unresolved high/critical repair item 阻断 stage promotion |
| `LCFRS-ROLL-006` | component dependency cycle 阻断 bundle assembly |

## repair queue bridge

finding 到 repair queue 的桥：

```json
{
  "repair_queue_required": true,
  "repair_item_candidates": [
    {
      "repair_item_candidate_id": "repair_candidate_lcf_dash_007",
      "source_finding_ref": "finding_lcf_dash_007",
      "repair_kind": "metric_gap",
      "severity": "high",
      "source_panel": "runtime_quarantine",
      "affected_life_targets": [
        "real_life",
        "real_responsibility"
      ],
      "required_action": {
        "action_kind": "add_repair_item_or_evidence_route",
        "target_artifact_ref": "repair_queue.json"
      }
    }
  ]
}
```

repair bridge rules：

| rule | 说明 |
|---|---|
| `LCFRS-REPAIR-001` | high/critical finding 产生 repair item candidate |
| `LCFRS-REPAIR-002` | repair kind 使用 shared defs |
| `LCFRS-REPAIR-003` | repair candidate 引用 source finding |
| `LCFRS-REPAIR-004` | blocked surface 写入 repair queue |
| `LCFRS-REPAIR-005` | repair bridge 进入 gap feedback |

## gap feedback bridge

gap feedback 把 report 结果带回 docs 和 artifact 生长链。

```json
{
  "gap_feedback_required": true,
  "source_checker_report_ref": "life_reality_cross_file_checker_report.json",
  "recommended_next_docs": [
    "115_life_reality_runtime_schema_fixture_seed_generation.md",
    "116_life_reality_component_schema_seed_generation.md"
  ],
  "recommended_next_artifacts": [
    "life_reality_runner/fixtures/life_reality/runtime_observation/manifest/runtime_observation_fixture_manifest.json",
    "life_reality_runner/generation/component_schema_materialization_sequence.manifest.json"
  ],
  "gap_register_update_ref": "16_digital_life_gap_register.md"
}
```

gap feedback rules：

| rule | 说明 |
|---|---|
| `LCFRS-GAP-001` | recommended next docs 编号大于当前层或已索引 |
| `LCFRS-GAP-002` | next artifacts root 合法 |
| `LCFRS-GAP-003` | unresolved findings 进入 recommended docs 或 artifacts |
| `LCFRS-GAP-004` | gap register update ref 指向 `16` |

## problem detail schema

core load、write、internal error 使用 problem detail。

```json
{
  "type": "https://life-reality.local/problems/shared-defs-missing",
  "title": "Shared defs missing",
  "status": 424,
  "detail": "shared defs schema is required before cross-file checker can run",
  "instance": "life_reality_cross_file_run_001",
  "problem_kind": "core_artifact_missing",
  "affected_artifact_refs": [],
  "stage_effect": {}
}
```

problem rules：

| rule | 说明 |
|---|---|
| `LCFRS-PROB-001` | problem detail 不替代 finding，而是进入 finding source |
| `LCFRS-PROB-002` | core artifact missing 进入 `needs_evidence` |
| `LCFRS-PROB-003` | report write failure 阻断 dashboard update |
| `LCFRS-PROB-004` | internal error 保留 trace context |

## CLI report outputs

未来命令：

```text
life-reality-runner check-dashboard
  --emit-report-schema
  --emit-provenance-graph
  --emit-specialized-checks
  --emit-rollup
  --report-out life_reality_runner/reports/life_reality/cross_file/run_001
```

exit code：

| code | 含义 |
|---|---|
| `0` | all blocking checks pass |
| `1` | warning/high repair required |
| `2` | critical/quarantine/stage promotion blocked |
| `3` | core schema、manifest 或 report 缺失 |
| `4` | checker internal error 或 report write failure |

## smoke cases

| smoke_id | 输入 | 预期 |
|---|---|---|
| `report_schema.top_level_minimal.pass_001` | top-level report 有 required 字段 | pass |
| `report_schema.finding_missing_source.fail_001` | finding 缺 source artifact refs | repair |
| `report_schema.critical_without_blocked_surface.fail_001` | critical finding 缺 blocked surface | repair |
| `report_schema.provenance_orphan_repair.fail_001` | repair item 无 incoming edge | repair |
| `report_schema.runtime_validation_output.pass_001` | JSON Schema output units 可映射 finding | pass |
| `report_schema.component_dependency_cycle.fail_001` | dependency graph 有 cycle | repair |
| `report_schema.false_green_dashboard.critical_001` | critical finding 但 dashboard green | quarantine |
| `report_schema.gap_feedback_missing_next_doc.fail_001` | unresolved finding 未进入 next docs/artifacts | repair |
| `report_schema.data_quality_inflation.fail_001` | source quality 低但 rollup 高 | repair |
| `report_schema.full_rollup.pass_001` | specialized reports 汇总成 top-level report | pass |

## LRGEN 更新

`114` 固定 `LRGEN-150` 到 `LRGEN-159` 的 schema 形状，并追加 report schema / rollup 任务：

| task_id | 输出 | 说明 |
|---|---|---|
| `LRGEN-150` | `life_reality_cross_file_checker_report.schema.json` | top-level checker report schema |
| `LRGEN-151` | `life_reality_cross_file_checker_report.json` | first checker report mock |
| `LRGEN-152` | `provenance_graph.json` | provenance graph mock |
| `LRGEN-153` | `dashboard_source_check.json` | dashboard source checker output |
| `LRGEN-154` | `runtime_ingestion_check.json` | ingestion/quarantine checker output |
| `LRGEN-155` | `repair_queue_check.json` | repair queue checker output |
| `LRGEN-156` | `stage_gate_check.json` | stage gate checker output |
| `LRGEN-157` | `gap_feedback_check.json` | gap feedback checker output |
| `LRGEN-158` | `runtime_fixture_manifest_check.json` | fixture manifest checker output |
| `LRGEN-159` | `data_quality_rollup_check.json` | data quality rollup checker output |
| `LRGEN-180` | `life_reality_checker_group_result.schema.json` | checker group result schema |
| `LRGEN-181` | `life_reality_checker_finding.schema.json` | finding schema |
| `LRGEN-182` | `life_reality_provenance_graph.schema.json` | provenance graph schema |
| `LRGEN-183` | `life_reality_artifact_ref.schema.json` | artifact ref schema |
| `LRGEN-184` | `life_reality_problem_detail.schema.json` | problem detail schema |
| `LRGEN-185` | `life_reality_cross_file_report_rollup.schema.json` | report rollup schema |
| `LRGEN-186` | `reports/life_reality/cross_file/run_001/cross_file_report_rollup.json` | first rollup mock |

## 与下一层连接

`115_life_reality_runtime_schema_fixture_seed_generation.md` 应用 `114` 的 report schema 来生成和验证 `112` 的 runtime observation fixture seeds：

```text
runtime observation seed
  -> runtime schema validation report
  -> checker finding
  -> runtime quarantine panel source
  -> cross-file report rollup
```

`116_life_reality_component_schema_seed_generation.md` 应用 `114` 的 component dependency graph report 来生成 `113` 的 component schema skeleton、dependency graph 和 dry-run report。
