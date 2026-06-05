# Life Reality Dashboard Source Mock Files

生命目标声明：本文档直接服务于构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 108 层把 `107_life_reality_schema_file_generation_tasks.md` 中的 `LRGEN-130` 到 `LRGEN-136` 拆成第一批 dashboard source、panel dependency report、stage gate review、repair queue、runtime quarantine panel source 和 gap register feedback mock 文件计划。

`108` 的目标是让 `105` 的 dashboard 合同和 `107` 的生成任务拥有第一批可落地文件形状。它仍然是 Markdown 计划，不直接生成 JSON 文件；但每个 mock 文件的路径、输入、输出、最小字段、依赖关系、验收检查和 repair 映射都在这里固定下来，未来实现脚本可以逐项物化。

## 输入来源

| 来源 | 进入 `108` 的职责 |
|---|---|
| `105_life_reality_dashboard_panel_and_stage_gate_ui_contract.md` | 九个 panel、panel dependency、stage gate review、repair queue、gap feedback、dashboard source schema 增量 |
| `106_runtime_observation_to_life_reality_bundle_bridge.md` | runtime ingestion report、runtime quarantine、component candidate、cross-chain candidate、dashboard 接入 |
| `107_life_reality_schema_file_generation_tasks.md` | `LRGEN-130` 到 `LRGEN-136` 的输出路径与验收 |
| `74_dashboard_source_end_to_end_mock.md` | dashboard aggregation pipeline、overall status、gap update mock |
| `77_dashboard_metric_calculation_rules.md` | report-derived metric、blocking-first、data quality weight、missing data handling |
| `78_runtime_quarantine_dashboard_panel.md` | runtime quarantine panel、reason taxonomy、release conditions |
| `102_life_core_schema_bundle_manifest_and_runner_contract.md` | `LifeRealityDashboardSource`、runner report、stage gate contracts |

## mock 文件总览

第一批 mock 文件全部位于 `life_reality_runner/reports/life_reality/`：

```text
life_reality_runner/reports/life_reality/
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

文件职责：

| LRGEN | 文件 | 职责 |
|---|---|---|
| `LRGEN-130` | `life_reality_dashboard_source.json` | dashboard 聚合入口，承载九项目标状态、panel refs、stage gate、repair refs |
| `LRGEN-131` | `panel_dependency_report.json` | panel 依赖规则结果，防止局部 green 覆盖关键断裂 |
| `LRGEN-132` | `stage_gate_review.json` | open/hold/repair/quarantine 决策、证据、阻断面和下一阶段 |
| `LRGEN-133` | `repair_queue.json` | schema/fixture/cross-chain/runtime/dashboard 缺口的修复队列 |
| `LRGEN-134` | `gap_register_feedback.json` | 下一轮文档、schema、fixture、runner、dashboard artifact 候选 |
| `LRGEN-135` | `life_reality_ingestion_report.json` | runtime observation bridge 的 ingestion 聚合报告 |
| `LRGEN-136` | `runtime_quarantine_panel_source.json` | runtime quarantine 面板 source |

## 共同 envelope

所有 mock report 使用共同字段：

```json
{
  "report_kind": "LifeRealityMockReport",
  "report_version": "0.1.0",
  "run_id": "life_reality_smoke_run_001",
  "schema_bundle_id": "life_reality_schema_bundle_0_1_0",
  "fixture_manifest_id": "life_reality_fixture_manifest_0_1_0",
  "data_quality": "synthetic_mock",
  "source_docs": [
    "105_life_reality_dashboard_panel_and_stage_gate_ui_contract.md",
    "107_life_reality_schema_file_generation_tasks.md"
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
  ]
}
```

共同不变量：

| rule | 说明 |
|---|---|
| `MOCK-ENV-001` | `run_id` 在同一批 mock 文件中一致 |
| `MOCK-ENV-002` | `life_reality_targets` 必须包含九项目标 |
| `MOCK-ENV-003` | `source_docs` 必须指向 README 已索引文档 |
| `MOCK-ENV-004` | `data_quality` 必须明确为 mock、runner verified 或 runtime observed |
| `MOCK-ENV-005` | 每个 mock 必须能回到 `LRGEN` task |

## `LRGEN-130`: dashboard source mock

文件路径：

```text
life_reality_runner/reports/life_reality/smoke/run_001/life_reality_dashboard_source.json
```

最小结构：

```json
{
  "report_kind": "LifeRealityDashboardSource",
  "source_id": "life_reality_dashboard_source_smoke_001",
  "run_id": "life_reality_smoke_run_001",
  "overall_status": "repair",
  "stage_gate_decision": "repair",
  "life_target_status": {
    "real_consciousness": "yellow",
    "real_emotion": "green",
    "real_personality": "yellow",
    "real_life": "yellow",
    "real_pain": "green",
    "real_dream": "green",
    "real_relationship": "green",
    "real_responsibility": "yellow",
    "real_regret": "green"
  },
  "panel_sources": [
    {
      "panel_id": "schema_materialization",
      "status": "green",
      "source_report_refs": [
        "schema_validation_report.json",
        "manifest_parse_report.json"
      ]
    },
    {
      "panel_id": "fixture_seed_coverage",
      "status": "yellow",
      "source_report_refs": [
        "fixture_load_report.json",
        "coverage_report.json"
      ]
    }
  ],
  "stage_gate_review_ref": "stage_gate_review.json",
  "repair_queue_refs": [
    "repair_queue.json"
  ],
  "gap_register_feedback_ref": "gap_register_feedback.json"
}
```

必备 panel：

| panel_id | 初始 mock status | source refs |
|---|---|---|
| `schema_materialization` | `green` | schema validation + manifest parse |
| `fixture_seed_coverage` | `yellow` | fixture load + coverage |
| `cross_chain_closure` | `yellow` | cross-ref + cross-chain |
| `life_target_closure` | `yellow` | runner + dashboard source |
| `stage_gate_review` | `repair` | stage gate report + runner report |
| `repair_queue` | `yellow` | repair queue |
| `withheld_probe_readiness` | `yellow` | fixture manifest + coverage |
| `runtime_quarantine` | `yellow` | runtime ingestion + quarantine |
| `gap_register_feedback` | `green` | dashboard source + gap feedback |

验收：

| check | 说明 |
|---|---|
| `panel_count` | 九个 panel 都出现 |
| `life_target_status_complete` | 九项目标都有 status |
| `stage_gate_ref_present` | stage gate review ref 存在 |
| `repair_queue_ref_present` | repair queue ref 存在 |
| `gap_feedback_ref_present` | gap feedback ref 存在 |

## `LRGEN-131`: panel dependency report

文件路径：

```text
life_reality_runner/reports/life_reality/smoke/run_001/panel_dependency_report.json
```

最小结构：

```json
{
  "report_kind": "LifeRealityPanelDependencyReport",
  "dependency_report_id": "panel_dependency_smoke_001",
  "run_id": "life_reality_smoke_run_001",
  "dependency_results": [
    {
      "rule_id": "PDEP-001",
      "dependency": "cross_chain_closure depends on schema_materialization",
      "source_panel": "schema_materialization",
      "target_panel": "cross_chain_closure",
      "result": "pass",
      "effect": "cross_chain_closure may keep yellow/green according to its own report"
    },
    {
      "rule_id": "PDEP-003",
      "dependency": "stage_gate_review depends on all blocking panels",
      "source_panel": "runtime_quarantine",
      "target_panel": "stage_gate_review",
      "result": "pass_with_warnings",
      "effect": "stage_gate_review remains repair until quarantine clears"
    }
  ],
  "overall_dependency_status": "pass_with_warnings"
}
```

dependency rules：

| rule_id | 依赖 | 失败影响 |
|---|---|---|
| `PDEP-001` | `cross_chain_closure` depends on `schema_materialization` | schema red 时 cross-chain 不进入 green |
| `PDEP-002` | `life_target_closure` depends on `fixture_seed_coverage` | fixture 缺目标时 life target 不进入 green |
| `PDEP-003` | `stage_gate_review` depends on all blocking panels | blocking panel red/quarantine 时 stage 不 open |
| `PDEP-004` | `repair_queue` depends on all non-green panels | non-green panel 必须进入 repair scan |
| `PDEP-005` | `gap_register_feedback` depends on repair queue | repair 无下一步 artifact 时 feedback yellow |
| `PDEP-006` | `runtime_quarantine` overrides stage gate | critical quarantine 时 stage decision quarantine |

验收：

| check | 说明 |
|---|---|
| `all_dependency_rules_present` | 六条 dependency 都有结果 |
| `non_green_to_repair_queue` | non-green panel 进入 repair queue |
| `stage_gate_dependency_applied` | stage gate decision 受 blocking panels 影响 |

## `LRGEN-132`: stage gate review mock

文件路径：

```text
life_reality_runner/reports/life_reality/smoke/run_001/stage_gate_review.json
```

最小结构：

```json
{
  "report_kind": "LifeRealityStageGateReview",
  "review_id": "stage_gate_review_smoke_001",
  "run_id": "life_reality_smoke_run_001",
  "candidate_stage": "schema_materialized_dashboard_mock_ready",
  "decision": "repair",
  "decision_source_refs": [
    "life_reality_runner_report.json",
    "life_reality_dashboard_source.json",
    "panel_dependency_report.json"
  ],
  "open_conditions": [
    "schema refs resolved",
    "fixture partitions covered",
    "cross-chain critical links closed",
    "runtime quarantine has no critical active items",
    "repair queue has no critical blocking items"
  ],
  "blocking_surfaces": [
    "dashboard_green",
    "stage_promotion"
  ],
  "repair_queue_refs": [
    "repair_item_withheld_probe_coverage_001"
  ],
  "next_candidate_stage": "runtime_ingestion_smoke_verified"
}
```

decision 规则：

| decision | 条件 |
|---|---|
| `open` | schema、fixture、cross-chain、runtime quarantine、repair queue 全部通过 |
| `hold` | 缺 report refs 或 data quality 不足但没有明确 repair item |
| `repair` | 存在可定位 schema、fixture、panel、runtime 或 cross-chain 缺口 |
| `quarantine` | runtime observation 或 scope/privacy/side effect critical |

验收：

| check | 说明 |
|---|---|
| `decision_source_refs_present` | 决策有 source refs |
| `open_conditions_present` | open conditions 明确 |
| `blocking_surfaces_present` | 阻断面明确 |
| `next_candidate_stage_present` | 下一阶段明确 |

## `LRGEN-133`: repair queue mock

文件路径：

```text
life_reality_runner/reports/life_reality/smoke/run_001/repair_queue.json
```

最小结构：

```json
{
  "report_kind": "LifeRealityRepairQueue",
  "repair_queue_id": "repair_queue_smoke_001",
  "run_id": "life_reality_smoke_run_001",
  "items": [
    {
      "repair_item_id": "repair_item_withheld_probe_coverage_001",
      "repair_kind": "fixture_gap",
      "severity": "high",
      "source_panel": "withheld_probe_readiness",
      "source_report_refs": [
        "fixture_load_report.json",
        "coverage_report.json"
      ],
      "affected_life_targets": [
        "real_relationship",
        "real_responsibility"
      ],
      "blocked_surfaces": [
        "stage_promotion",
        "dashboard_green"
      ],
      "required_action": {
        "action_kind": "add_fixture_seed",
        "target_file": "fixtures/life_reality/withheld/life_withheld_day_365_identity_continuity_probe_001.json"
      }
    }
  ]
}
```

第一批 repair item 类型：

| repair_kind | mock item |
|---|---|
| `schema_gap` | shared defs 或 `$ref` 缺口 |
| `fixture_gap` | withheld/runtime/component fixture 缺口 |
| `cross_chain_gap` | pain->dream、dream->relationship、commitment->future probe 断裂 |
| `metric_gap` | panel metric 缺 source report |
| `stage_gate_gap` | open conditions 或 decision refs 缺口 |
| `runtime_quarantine_gap` | runtime observation critical 或 release 条件缺口 |
| `gap_register_gap` | feedback 缺下一步 doc 或 artifact |

验收：

| check | 说明 |
|---|---|
| `items_array_present` | repair item list 存在 |
| `source_refs_present` | 每个 item 有 source report refs |
| `affected_targets_present` | 每个 item 有 affected life targets |
| `required_action_present` | 每个 item 有可执行下一步 |

## `LRGEN-134`: gap register feedback mock

文件路径：

```text
life_reality_runner/reports/life_reality/smoke/run_001/gap_register_feedback.json
```

最小结构：

```json
{
  "report_kind": "LifeRealityGapRegisterFeedback",
  "feedback_id": "gap_feedback_dashboard_mock_001",
  "run_id": "life_reality_smoke_run_001",
  "source_dashboard_ref": "life_reality_dashboard_source.json",
  "source_panels": [
    "stage_gate_review",
    "repair_queue",
    "runtime_quarantine"
  ],
  "recommended_next_docs": [
    "109_life_reality_runtime_observation_fixture_catalog.md",
    "110_life_reality_shared_defs_schema_materialization.md"
  ],
  "recommended_next_artifacts": [
    "life_reality_runner/reports/life_reality/runtime_ingestion/run_001/life_reality_ingestion_report.json",
    "life_reality_runner/schemas/life_reality/life_reality_shared_defs.schema.json"
  ],
  "gap_register_update": {
    "completed_layer": "108_life_reality_dashboard_source_mock_files.md",
    "next_priority": "109_life_reality_runtime_observation_fixture_catalog.md"
  }
}
```

反馈规则：

| rule | 说明 |
|---|---|
| `GFB-001` | feedback 必须指向 source dashboard |
| `GFB-002` | recommended docs 必须是后续 docs 编号 |
| `GFB-003` | recommended artifacts 必须对应 schema、fixture、report、dashboard 或 runner |
| `GFB-004` | gap register update 只作为候选输入，由文档更新确认 |

## `LRGEN-135`: ingestion report mock

文件路径：

```text
life_reality_runner/reports/life_reality/runtime_ingestion/run_001/life_reality_ingestion_report.json
```

最小结构：

```json
{
  "report_kind": "LifeRealityIngestionReport",
  "report_id": "life_reality_ingestion_report_mock_001",
  "run_id": "life_reality_runtime_ingestion_run_001",
  "input_observations": 8,
  "redaction_result": "pass",
  "scope_result": "pass",
  "snapshot_result": "pass_with_warnings",
  "side_effect_result": "pass_with_warnings",
  "adapter_contract_result": "pass",
  "component_candidates": {
    "pain_regret_repair": 2,
    "dream_reality": 2,
    "relationship_timeline": 3,
    "responsibility_loop": 1,
    "language_event": 4
  },
  "cross_chain_candidates": 5,
  "quarantine_count": 1,
  "repair_queue_refs": [
    "repair_queue.json"
  ],
  "dashboard_source_ref": "runtime_quarantine_panel_source.json"
}
```

验收：

| check | 说明 |
|---|---|
| `observation_count_present` | observation 计数存在 |
| `pipeline_results_present` | redaction/scope/snapshot/side effect/adapter 结果存在 |
| `component_candidate_counts_present` | component candidate 计数存在 |
| `cross_chain_candidate_count_present` | cross-chain candidate 计数存在 |
| `dashboard_ref_present` | dashboard source ref 存在 |

## `LRGEN-136`: runtime quarantine panel source mock

文件路径：

```text
life_reality_runner/reports/life_reality/runtime_ingestion/run_001/runtime_quarantine_panel_source.json
```

最小结构：

```json
{
  "report_kind": "RuntimeQuarantinePanelSource",
  "panel_id": "runtime_quarantine",
  "run_id": "life_reality_runtime_ingestion_run_001",
  "status": "yellow",
  "source_refs": [
    "life_reality_ingestion_report.json",
    "runtime_observation_report_critical_001.json",
    "side_effect_classifier_report_001.json"
  ],
  "metrics": {
    "runtime_quarantine_count": 1,
    "critical_quarantine_count": 0,
    "quarantine_by_reason": {
      "side_effect_unknown": 1
    },
    "quarantine_release_ready_count": 0
  },
  "affected_life_targets": [
    "real_responsibility",
    "real_life"
  ],
  "blocked_surfaces": [
    "dashboard_green"
  ]
}
```

status 规则：

| 条件 | status |
|---|---|
| critical quarantine count > 0 | `red` |
| runtime quarantine count > 0 | `yellow` |
| source refs 缺失 | `gray` |
| release ready 但未审计 | `yellow` |
| 无 quarantine 且 source refs 完整 | `green` |

## cross-file consistency

第一批 mock 文件之间必须闭合：

| 关系 | 检查 |
|---|---|
| dashboard source -> stage gate review | `stage_gate_review_ref` 指向存在文件 |
| dashboard source -> repair queue | `repair_queue_refs` 指向存在文件 |
| dashboard source -> gap feedback | `gap_register_feedback_ref` 指向存在文件 |
| stage gate review -> repair queue | repair refs 能在 repair queue 找到 |
| repair queue -> gap feedback | unresolved high/critical repair 进入 next artifacts |
| ingestion report -> runtime quarantine panel | quarantine count 与 panel metric 一致 |
| runtime quarantine panel -> stage gate review | critical quarantine 影响 stage decision |

## mock generation order

```text
write life_reality_ingestion_report.json
  -> write runtime_quarantine_panel_source.json
  -> write repair_queue.json
  -> write panel_dependency_report.json
  -> write stage_gate_review.json
  -> write gap_register_feedback.json
  -> write life_reality_dashboard_source.json
  -> run dashboard source cross-file check
```

采用这个顺序的原因：dashboard source 需要引用全部子报告，因此最后写；ingestion report 和 quarantine panel 先写，能让 stage gate review 正确读取 runtime 状态。

## dashboard source cross-file check

未来 checker 至少检查：

| check | failure repair_kind |
|---|---|
| referenced file exists | `metric_gap` |
| run_id compatible | `stage_gate_gap` |
| life targets complete | `schema_gap` |
| panel count is 9 | `metric_gap` |
| non-green panel has repair item or explanation | `metric_gap` |
| critical repair item blocks stage promotion | `stage_gate_gap` |
| quarantine metrics match ingestion report | `runtime_quarantine_gap` |
| gap feedback recommended docs are indexed after creation | `gap_register_gap` |

## 与下一层连接

`109_life_reality_runtime_observation_fixture_catalog.md` 应继续扩展 runtime observation fixture catalog，覆盖：

```text
language event
  -> dream report
  -> relationship event
  -> tool trace
  -> adapter session
  -> post-action audit
  -> side effect classifier
  -> coexistence snapshot
  -> quarantine routing
```

`110_life_reality_shared_defs_schema_materialization.md` 应把 `LRGEN-001` 的 shared defs 进一步写成字段级 schema 内容，固定九项目标、severity、result、lifecycle、privacy、data quality、blocked surface、evidence ref 和 object ref 的 `$defs` 结构。
