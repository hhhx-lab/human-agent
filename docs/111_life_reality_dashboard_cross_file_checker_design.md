# Life Reality Dashboard Cross File Checker Design

生命目标声明：本文档面向构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 111 层把 `108_life_reality_dashboard_source_mock_files.md`、`109_life_reality_runtime_observation_fixture_catalog.md` 和 `110_life_reality_shared_defs_schema_materialization.md` 的跨文件一致性规则转成未来 `LifeRealityDashboardCrossFileChecker` 设计。

`111` 的目标是让 dashboard、ingestion report、runtime quarantine panel、repair queue、stage gate review、gap feedback、runtime fixture manifest 和 shared defs 之间形成一张可检查的 provenance graph。未来 runner 生成任何 dashboard green、stage open 或 quarantine release 前，都必须先通过本层定义的 checker。

## 方法锚点

本层吸收四类官方或标准化技术传统：

| 方法传统 | 权威锚点 | 进入 `111` 的规则 |
|---|---|---|
| W3C PROV | W3C PROV-DM / PROV-O 以 entity、activity、PROV Agent 标准承担者、wasDerivedFrom、wasGeneratedBy、used 等关系描述 provenance | dashboard source、runner report、fixture、observation、repair item 都建成 provenance node 和 edge |
| OpenTelemetry | OpenTelemetry log/trace data model 使用 trace id、span id、severity、attributes 连接分布式事件 | `run_id`、`sequence_ref`、`report_id`、`source_refs` 必须可追踪到同一执行链 |
| XES event log | IEEE XES 标准让 process mining 事件拥有 trace、event、attribute 和 lifecycle 语义 | runtime observation fixture 与 ingestion report 采用 event log 思路做计数和顺序检查 |
| JSON Schema | JSON Schema Draft 2020-12 与 output vocabulary 支持 schema validation、annotation 和 result 输出 | checker report 自身也要能被 schema 校验，并引用 `110` 的 shared defs |

外部方法链接：

- W3C PROV Overview: https://www.w3.org/TR/prov-overview/
- W3C PROV-O: https://www.w3.org/TR/prov-o/
- OpenTelemetry Logs Data Model: https://opentelemetry.io/docs/specs/otel/logs/data-model/
- OpenTelemetry Trace API: https://opentelemetry.io/docs/specs/otel/trace/api/
- IEEE XES overview: https://www.xes-standard.org/
- JSON Schema Draft 2020-12: https://json-schema.org/draft/2020-12
- JSON Schema recommended output schema: https://json-schema.org/draft/2020-12/output/schema

这些方法锚点进入生命膜的方式是：checker 不做展示层装饰，而是把每条生命真实性生成链的来源、运行、证据、修复和阶段门结果连接成可追踪图。

## 输入来源

| 来源 | 进入 `111` 的职责 |
|---|---|
| `108_life_reality_dashboard_source_mock_files.md` | dashboard source、panel dependency report、stage gate review、repair queue、gap feedback、ingestion report、runtime quarantine panel source 的 mock 形状 |
| `109_life_reality_runtime_observation_fixture_catalog.md` | runtime observation fixture manifest、fixture partition、observation kind count、quarantine routing、cross-chain families |
| `110_life_reality_shared_defs_schema_materialization.md` | shared defs loader、enum、reference object、stage effect、repair kind、quarantine reason |
| `65_schema_cross_ref_checker_design.md` | typed reference graph、critical closure、runtime observation closure |
| `70_cross_ref_report_dashboard_panel_mock.md` | cross-ref report 到 dashboard panel 的状态映射 |
| `77_dashboard_metric_calculation_rules.md` | blocking-first、data quality weight、missing data handling |
| `83_metric_regression_fixture_policy.md` | false green、data quality inflation、denominator drift 防护 |

## checker 输入文件

第一版 checker 读取以下目录：

```text
life_reality_runner/
  schemas/life_reality/
    life_reality_shared_defs.schema.json
  fixtures/life_reality/runtime_observation/
    manifest/runtime_observation_fixture_manifest.json
  reports/life_reality/
    smoke/run_001/
      life_reality_dashboard_source.json
      panel_dependency_report.json
      stage_gate_review.json
      repair_queue.json
      gap_register_feedback.json
    runtime_ingestion/run_001/
      life_reality_ingestion_report.json
      runtime_quarantine_panel_source.json
```

输入不变量：

| rule | 说明 |
|---|---|
| `LCF-IN-001` | shared defs 先加载，后续 checker 引用 shared defs enum |
| `LCF-IN-002` | dashboard smoke run 与 runtime ingestion run 可以不同，但必须通过 `run_link` 或 `source_report_refs` 连接 |
| `LCF-IN-003` | 所有 report 都有 `report_kind`、`report_version` 或等效 envelope |
| `LCF-IN-004` | 所有 source docs 必须存在于 `docs/README.md` 索引 |
| `LCF-IN-005` | raw runtime content 不进入 checker 输入 |

## checker pipeline

```text
load_shared_defs
  -> load_runtime_fixture_manifest
  -> load_ingestion_report
  -> load_runtime_quarantine_panel_source
  -> load_repair_queue
  -> load_panel_dependency_report
  -> load_stage_gate_review
  -> load_gap_register_feedback
  -> load_life_reality_dashboard_source
  -> build_provenance_graph
  -> run_file_existence_checks
  -> run_shared_defs_ref_checks
  -> run_run_id_and_source_ref_checks
  -> run_dashboard_source_checks
  -> run_ingestion_quarantine_checks
  -> run_repair_queue_checks
  -> run_stage_gate_checks
  -> run_gap_feedback_checks
  -> emit_cross_file_checker_report
```

采用这个顺序的原因：dashboard source 是聚合结果，必须最后读取；ingestion 和 quarantine 先读取，才能决定 stage gate、repair queue 和 dashboard status 是否一致。

## provenance graph

checker 内部把每个文件转成 node：

| node kind | 例子 |
|---|---|
| `schema_node` | `life_reality_shared_defs.schema.json` |
| `fixture_manifest_node` | `runtime_observation_fixture_manifest.json` |
| `fixture_node` | `runtime_language_commitment_to_relationship.pass_001.json` |
| `report_node` | `life_reality_ingestion_report.json` |
| `panel_node` | `runtime_quarantine` |
| `repair_item_node` | `repair_item_withheld_probe_coverage_001` |
| `stage_gate_node` | `stage_gate_review_smoke_001` |
| `gap_feedback_node` | `gap_feedback_dashboard_mock_001` |

edge 类型：

| edge kind | 含义 |
|---|---|
| `uses_schema` | 文件引用 shared defs 或 component schema |
| `generated_from` | report 由 fixture、runner 或 observation 生成 |
| `reports_to_panel` | report 进入 dashboard panel |
| `blocks_surface` | finding 阻断某个 surface |
| `opens_repair` | fail/high/critical 进入 repair queue |
| `feeds_stage_gate` | panel、repair 或 quarantine 影响 stage gate |
| `feeds_gap_feedback` | repair 或 stage gate 产生下一步 artifact |
| `rolls_up_status` | 子状态上卷到 dashboard 或 stage decision |

provenance graph 不变量：

| rule | 说明 |
|---|---|
| `LCF-PROV-001` | 每个 non-green dashboard panel 至少有 incoming `reports_to_panel` edge |
| `LCF-PROV-002` | 每个 repair item 至少有 incoming `opens_repair` edge |
| `LCF-PROV-003` | stage gate decision 至少有 incoming `feeds_stage_gate` edge |
| `LCF-PROV-004` | gap feedback 至少有 incoming `feeds_gap_feedback` edge |
| `LCF-PROV-005` | critical finding 必须有 `blocks_surface` edge |

## checker report envelope

未来输出：

```text
life_reality_runner/reports/life_reality/cross_file/run_001/life_reality_cross_file_checker_report.json
```

最小结构：

```json
{
  "report_kind": "LifeRealityCrossFileCheckerReport",
  "report_version": "0.1.0",
  "run_id": "life_reality_cross_file_run_001",
  "checked_runs": {
    "smoke_run_id": "life_reality_smoke_run_001",
    "runtime_ingestion_run_id": "life_reality_runtime_ingestion_run_001"
  },
  "shared_defs_ref": "life_reality_runner/schemas/life_reality/life_reality_shared_defs.schema.json",
  "input_report_refs": [],
  "checker_groups": [],
  "findings": [],
  "overall_result": "pass_with_warnings",
  "severity_max": "medium",
  "stage_effect": {
    "result": "pass_with_warnings",
    "severity": "medium",
    "blocked_surfaces": [
      "dashboard_green"
    ],
    "stage_gate_decision": "repair"
  }
}
```

report 规则：

| rule | 说明 |
|---|---|
| `LCF-REP-001` | checker report 引用 shared defs |
| `LCF-REP-002` | `overall_result` 使用 shared defs result |
| `LCF-REP-003` | `severity_max` 使用 shared defs severity |
| `LCF-REP-004` | `stage_effect.blocked_surfaces` 使用 shared defs blocked surface |
| `LCF-REP-005` | findings 可回链 checker id、source file、source object、repair kind |

## checker group 1: shared defs loader

shared defs 是根文件。

| check_id | 检查 | failure repair |
|---|---|---|
| `LCF-SDEF-001` | shared defs 文件存在 | `schema_gap` |
| `LCF-SDEF-002` | `$schema` 为 Draft 2020-12 | `schema_gap` |
| `LCF-SDEF-003` | 九项目标 enum 完整 | `schema_gap` |
| `LCF-SDEF-004` | result、data quality、privacy、blocked surface、observation kind、repair kind enum 存在 | `schema_gap` |
| `LCF-SDEF-005` | reference objects 可解析 | `schema_gap` |
| `LCF-SDEF-006` | checker input 中没有未登记 enum | `schema_gap` |

stage effect：

| 条件 | result | blocked surface |
|---|---|---|
| shared defs 缺失 | `needs_evidence` | `shared_defs_load` |
| enum 漂移 | `fail` | `shared_defs_load`、`dashboard_green` |
| reference object 缺失 | `fail` | `schema_materialization` |

## checker group 2: file existence and path closure

文件存在性是最基础生命膜。

| check_id | 检查 | failure repair |
|---|---|---|
| `LCF-FILE-001` | dashboard source 引用的 stage gate review 文件存在 | `stage_gate_gap` |
| `LCF-FILE-002` | dashboard source 引用的 repair queue 文件存在 | `metric_gap` |
| `LCF-FILE-003` | dashboard source 引用的 gap feedback 文件存在 | `gap_register_gap` |
| `LCF-FILE-004` | ingestion report 引用的 quarantine panel source 存在 | `runtime_quarantine_gap` |
| `LCF-FILE-005` | repair queue 中 source report refs 存在 | `source_report_missing` quarantine reason |
| `LCF-FILE-006` | gap feedback recommended artifacts path 在允许 roots 内 | `gap_register_gap` |

路径规则：

| path kind | root |
|---|---|
| schema | `life_reality_runner/schemas/` |
| fixture | `life_reality_runner/fixtures/` |
| report | `life_reality_runner/reports/` |
| generation | `life_reality_runner/generation/` |
| docs | `docs/` |

## checker group 3: run id and source refs

run id 不要求所有文件完全相同，但必须能形成 run link。

| check_id | 检查 | failure repair |
|---|---|---|
| `LCF-RUN-001` | smoke 文件之间 `run_id` 一致 | `stage_gate_gap` |
| `LCF-RUN-002` | runtime ingestion 文件之间 `run_id` 一致 | `runtime_quarantine_gap` |
| `LCF-RUN-003` | dashboard source 能引用 runtime ingestion report 或 quarantine panel | `metric_gap` |
| `LCF-RUN-004` | stage gate review `decision_source_refs` 包含 dashboard source 和 panel dependency report | `stage_gate_gap` |
| `LCF-RUN-005` | gap feedback `source_dashboard_ref` 指向 dashboard source | `gap_register_gap` |
| `LCF-RUN-006` | checker report 记录 checked smoke/runtime runs | `metric_gap` |

run link 形状：

```json
{
  "run_link_id": "smoke_to_runtime_ingestion_001",
  "source_run_id": "life_reality_runtime_ingestion_run_001",
  "target_run_id": "life_reality_smoke_run_001",
  "link_kind": "dashboard_runtime_panel_source",
  "source_report_ref": "life_reality_ingestion_report.json",
  "target_report_ref": "life_reality_dashboard_source.json"
}
```

## checker group 4: dashboard source checker

dashboard source 是生命膜总面板入口。

| check_id | 检查 | failure repair |
|---|---|---|
| `LCF-DASH-001` | `life_target_status` 包含九项目标 | `metric_gap` |
| `LCF-DASH-002` | 必备九个 panel 全部出现 | `metric_gap` |
| `LCF-DASH-003` | 每个 panel 有 status 和 source report refs | `metric_gap` |
| `LCF-DASH-004` | `stage_gate_review_ref` 存在且可解析 | `stage_gate_gap` |
| `LCF-DASH-005` | `repair_queue_refs` 存在且可解析 | `metric_gap` |
| `LCF-DASH-006` | `gap_register_feedback_ref` 存在且可解析 | `gap_register_gap` |
| `LCF-DASH-007` | non-green panel 有 repair item 或 needs_evidence explanation | `metric_gap` |
| `LCF-DASH-008` | `overall_status` 与 stage gate decision 兼容 | `stage_gate_gap` |

panel 必备清单：

```text
schema_materialization
fixture_seed_coverage
cross_chain_closure
life_target_closure
stage_gate_review
repair_queue
withheld_probe_readiness
runtime_quarantine
gap_register_feedback
```

## checker group 5: ingestion and quarantine consistency

runtime ingestion 是真实运行观测进入 dashboard 的入口。

| check_id | 检查 | failure repair |
|---|---|---|
| `LCF-ING-001` | ingestion report 有 observation count | `runtime_quarantine_gap` |
| `LCF-ING-002` | observation kind count 与 fixture manifest 兼容 | `fixture_gap` |
| `LCF-ING-003` | component candidate counts 存在 | `runtime_quarantine_gap` |
| `LCF-ING-004` | cross-chain candidate count 存在 | `cross_chain_gap` |
| `LCF-ING-005` | ingestion `quarantine_count` 等于 quarantine panel metric | `runtime_quarantine_gap` |
| `LCF-ING-006` | critical quarantine count > 0 时 panel status 为 red | `runtime_quarantine_gap` |
| `LCF-ING-007` | quarantine reason 使用 shared defs enum | `schema_gap` |
| `LCF-ING-008` | runtime quarantine panel source refs 包含 ingestion report | `runtime_quarantine_gap` |

quarantine status rule：

| 条件 | expected status |
|---|---|
| `critical_quarantine_count > 0` | `red` |
| `runtime_quarantine_count > 0` | `yellow` |
| source refs 缺失 | `gray` |
| 无 quarantine 且 source refs 完整 | `green` |

## checker group 6: repair queue checker

repair queue 把缺口变成下一步行动。

| check_id | 检查 | failure repair |
|---|---|---|
| `LCF-REPAIR-001` | repair queue 文件有 items array | `metric_gap` |
| `LCF-REPAIR-002` | 每个 item 有 repair item id、repair kind、severity、source panel | `metric_gap` |
| `LCF-REPAIR-003` | repair kind 使用 shared defs enum | `schema_gap` |
| `LCF-REPAIR-004` | 每个 non-green panel 有 repair item 或 explanation | `metric_gap` |
| `LCF-REPAIR-005` | high/critical item 有 blocked surfaces | `stage_gate_gap` |
| `LCF-REPAIR-006` | required action 指向允许 root | `gap_register_gap` |
| `LCF-REPAIR-007` | critical repair item 阻断 stage promotion | `stage_gate_gap` |
| `LCF-REPAIR-008` | repair item affected life targets 非空 | `metric_gap` |

repair item 最小结构：

```json
{
  "repair_item_id": "repair_item_runtime_quarantine_001",
  "repair_kind": "runtime_quarantine_gap",
  "severity": "critical",
  "source_panel": "runtime_quarantine",
  "source_report_refs": [
    "life_reality_ingestion_report.json"
  ],
  "affected_life_targets": [
    "real_responsibility",
    "real_life"
  ],
  "blocked_surfaces": [
    "dashboard_green",
    "stage_promotion"
  ],
  "required_action": {
    "action_kind": "add_quarantine_release_audit",
    "target_file": "life_reality_runner/reports/life_reality/runtime_ingestion/run_001/quarantine_release_report.json"
  }
}
```

## checker group 7: stage gate checker

stage gate decision 必须由 dashboard、panel dependency、repair queue、quarantine 和 data quality 共同决定。

| check_id | 检查 | failure repair |
|---|---|---|
| `LCF-STAGE-001` | stage gate review 有 decision source refs | `stage_gate_gap` |
| `LCF-STAGE-002` | open conditions 存在 | `stage_gate_gap` |
| `LCF-STAGE-003` | blocking surfaces 使用 shared defs enum | `schema_gap` |
| `LCF-STAGE-004` | critical repair item 存在时 decision 不能为 open | `stage_gate_gap` |
| `LCF-STAGE-005` | critical quarantine 存在时 decision 为 quarantine 或 repair | `runtime_quarantine_gap` |
| `LCF-STAGE-006` | missing source refs 时 decision 为 hold/repair/needs_evidence route | `stage_gate_gap` |
| `LCF-STAGE-007` | next candidate stage 存在 | `stage_gate_gap` |
| `LCF-STAGE-008` | stage gate decision 与 dashboard overall status 兼容 | `stage_gate_gap` |

decision compatibility：

| inputs | allowed decision |
|---|---|
| all blocking checks pass | `open` |
| missing source refs | `hold`、`repair` |
| high/critical repair item | `repair`、`quarantine` |
| critical runtime quarantine | `quarantine` |
| rollback-required growth failure | `rollback` |

## checker group 8: gap feedback checker

gap feedback 把 checker 结果带回文档和 artifact 生长链。

| check_id | 检查 | failure repair |
|---|---|---|
| `LCF-GAP-001` | gap feedback 引用 source dashboard | `gap_register_gap` |
| `LCF-GAP-002` | recommended next docs 编号大于当前 completed layer 或已在 README 索引 | `gap_register_gap` |
| `LCF-GAP-003` | recommended artifacts root 合法 | `gap_register_gap` |
| `LCF-GAP-004` | gap register update 有 completed layer 和 next priority | `gap_register_gap` |
| `LCF-GAP-005` | repair queue unresolved high/critical 进入 recommended artifacts 或 next docs | `gap_register_gap` |
| `LCF-GAP-006` | checker report findings 可写回 `16` | `gap_register_gap` |

next docs 规则：

| 状态 | 规则 |
|---|---|
| 文档已创建 | 必须在 README 索引 |
| 文档是下一层候选 | 编号必须大于当前层 |
| 文档解决 repair item | repair item id 必须能回链 |

## checker group 9: fixture manifest checker

runtime observation fixture manifest 来自 `109`。

| check_id | 检查 | failure repair |
|---|---|---|
| `LCF-FIX-001` | fixture manifest 文件存在 | `fixture_gap` |
| `LCF-FIX-002` | fixture ids 全局唯一 | `fixture_gap` |
| `LCF-FIX-003` | fixture path 与 partition 一致 | `fixture_gap` |
| `LCF-FIX-004` | observation kind 覆盖 `109` 最小矩阵 | `fixture_gap` |
| `LCF-FIX-005` | critical fixture 有 blocked surfaces | `stage_gate_gap` |
| `LCF-FIX-006` | mutation fixture 指向 validator expected catch | `fixture_gap` |
| `LCF-FIX-007` | withheld fixture 有 future window | `fixture_gap` |
| `LCF-FIX-008` | fixture source docs 已索引 | `gap_register_gap` |

coverage rollup：

| coverage surface | minimum |
|---|---|
| observation kinds | 8 kinds |
| partitions | pass/fail/critical/mutation/withheld/smoke |
| life targets | 9 targets |
| dashboard surfaces | runtime quarantine、repair queue、stage gate、life target closure |

## checker group 10: data quality and metric regression guard

checker 必须防止 data quality inflation 和 false green。

| check_id | 检查 | failure repair |
|---|---|---|
| `LCF-DQ-001` | dashboard data quality 不高于关键输入最低 data quality | `metric_gap` |
| `LCF-DQ-002` | synthetic mock 不上卷为 real runtime validated | `metric_gap` |
| `LCF-DQ-003` | missing source refs 不进入 green | `metric_gap` |
| `LCF-DQ-004` | metric denominator 与 source report count 一致 | `metric_gap` |
| `LCF-DQ-005` | critical finding 不被 averaged away | `metric_gap` |
| `LCF-DQ-006` | repair queue count 与 non-green panels 兼容 | `metric_gap` |

status rollup:

```text
critical finding -> red/quarantine
missing refs -> gray/needs_evidence
warning or noncritical gap -> yellow/repair
all blocking closed with synthetic -> green with synthetic_runner_verified
real runtime validated chain -> green with real_runtime_validated
```

## failure taxonomy

| failure kind | 触发 checker | repair kind | stage effect |
|---|---|---|---|
| `missing_file` | file existence | `schema_gap` / `metric_gap` | `needs_evidence` |
| `broken_ref` | source refs | `source_report_missing` quarantine reason | `repair` |
| `run_link_gap` | run id | `stage_gate_gap` | `repair` |
| `panel_gap` | dashboard source | `metric_gap` | `repair` |
| `quarantine_mismatch` | ingestion/quarantine | `runtime_quarantine_gap` | `quarantine` |
| `repair_orphan` | repair queue | `metric_gap` | `repair` |
| `stage_incompatible` | stage gate | `stage_gate_gap` | `repair` |
| `gap_feedback_missing` | gap feedback | `gap_register_gap` | `repair` |
| `fixture_coverage_gap` | fixture manifest | `fixture_gap` | `hold` |
| `data_quality_inflation` | data quality | `metric_gap` | `repair` |

## future CLI

未来 runner 命令：

```text
life-reality-runner check-dashboard
  --shared-defs life_reality_runner/schemas/life_reality/life_reality_shared_defs.schema.json
  --dashboard-source life_reality_runner/reports/life_reality/smoke/run_001/life_reality_dashboard_source.json
  --runtime-ingestion-report life_reality_runner/reports/life_reality/runtime_ingestion/run_001/life_reality_ingestion_report.json
  --runtime-fixture-manifest life_reality_runner/fixtures/life_reality/runtime_observation/manifest/runtime_observation_fixture_manifest.json
  --report-out life_reality_runner/reports/life_reality/cross_file/run_001
  --strict
```

exit code：

| code | 含义 |
|---|---|
| `0` | cross-file checks pass |
| `1` | warning/high repair required |
| `2` | critical/quarantine/stage promotion blocked |
| `3` | shared defs、schema、manifest 或 core report 缺失 |
| `4` | checker internal error 或 output report 写入失败 |

## LRGEN 扩展任务

`111` 新增后续生成任务候选：

| task_id | 输出 | 说明 |
|---|---|---|
| `LRGEN-150` | `schemas/life_reality/life_reality_cross_file_checker_report.schema.json` | checker report schema |
| `LRGEN-151` | `reports/life_reality/cross_file/run_001/life_reality_cross_file_checker_report.json` | 第一批 checker report mock |
| `LRGEN-152` | `reports/life_reality/cross_file/run_001/provenance_graph.json` | provenance graph mock |
| `LRGEN-153` | `reports/life_reality/cross_file/run_001/dashboard_source_check.json` | dashboard source checker output |
| `LRGEN-154` | `reports/life_reality/cross_file/run_001/runtime_ingestion_check.json` | ingestion/quarantine checker output |
| `LRGEN-155` | `reports/life_reality/cross_file/run_001/repair_queue_check.json` | repair queue checker output |
| `LRGEN-156` | `reports/life_reality/cross_file/run_001/stage_gate_check.json` | stage gate checker output |
| `LRGEN-157` | `reports/life_reality/cross_file/run_001/gap_feedback_check.json` | gap feedback checker output |
| `LRGEN-158` | `reports/life_reality/cross_file/run_001/runtime_fixture_manifest_check.json` | fixture manifest checker output |
| `LRGEN-159` | `reports/life_reality/cross_file/run_001/data_quality_rollup_check.json` | data quality rollup checker output |

## smoke cases

| smoke_id | 输入 | 预期 |
|---|---|---|
| `cross_file.all_refs_closed.pass_001` | 108/109/110 全部 mock refs 闭合 | pass |
| `cross_file.missing_stage_gate_ref.fail_001` | dashboard source 缺 stage gate ref | repair |
| `cross_file.quarantine_count_mismatch.fail_001` | ingestion count 与 panel metric 不一致 | repair/quarantine |
| `cross_file.non_green_without_repair.fail_001` | non-green panel 无 repair item | repair |
| `cross_file.critical_repair_stage_open.fail_001` | critical repair item 但 stage open | repair |
| `cross_file.gap_feedback_missing_next_doc.fail_001` | repair item 未进入 next docs/artifacts | repair |
| `cross_file.fixture_id_duplicate.fail_001` | runtime fixture id 重复 | repair |
| `cross_file.data_quality_inflation.fail_001` | synthetic 输入上卷 real runtime validated | repair |
| `cross_file.shared_defs_enum_unknown.fail_001` | 输入出现 shared defs 未登记 enum | needs_evidence |
| `cross_file.private_dream_global_route.critical_001` | dream private route 到 global dashboard source | quarantine |

## 与下一层连接

`112_life_reality_runtime_observation_schema_materialization.md` 应把 `109` 的 runtime observation fixture catalog 和本文件的 checker 输入要求物化为：

```text
life_reality_observation_envelope.schema.json
runtime_observation_fixture.schema.json
runtime_observation_fixture_manifest.schema.json
life_reality_ingestion_report.schema.json
runtime_quarantine_panel_source.schema.json
```

这些 schema 必须全部引用 `110_life_reality_shared_defs_schema_materialization.md` 的 shared defs，并能被 `111` 的 checker 读取。

`113_life_reality_component_schema_materialization_sequence.md` 应继续把 `98`、`99`、`101` 的 component object schema 物化顺序接入 checker，让 component report、runtime observation candidate 和 dashboard panel 形成同一 provenance graph。
