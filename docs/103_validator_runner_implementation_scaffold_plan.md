# Validator Runner Implementation Scaffold Plan

生命目标声明：本文档直接服务于构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 103 层把 `102_life_core_schema_bundle_manifest_and_runner_contract.md` 的 `LifeRealitySchemaBundle` 合同拆成未来代码实现脚手架：manifest parser、shared defs loader、schema ref validator、cross-ref checker、fixture loader、component validator dispatcher、cross-chain validator、report aggregator 和 dashboard source writer。

`103` 的目标是让工程落地从“写一个 runner”变成“实现一组稳定的生命膜执行模块”。这些模块未来可以用 Python、TypeScript 或其他运行时实现；本文件先固定目录、接口、执行顺序、错误语义、测试面和提交路线。

## 输入来源

| 来源 | 进入 `103` 的职责 |
|---|---|
| `61_json_schema_bundle_draft.md` | 共享 schema envelope、shared defs、manifest bundle 思路 |
| `62_runner_report_format_and_cli_contract.md` | runner report、fixture report、coverage report、exit code 和 report 聚合语义 |
| `65_schema_cross_ref_checker_design.md` | typed graph、critical closure、scope/privacy closure、timeline closure |
| `97_growth_validator_fixture_and_dashboard_plan.md` | `LifeRealityValidatorSuite`、stage gate、dashboard readiness 语义 |
| `98_pain_regret_repair_json_schema_and_fixture_bundle.md` | `PainRegretRepairBundle` 和 `PainRegretRepairValidator` 输入面 |
| `99_dream_reality_json_schema_and_fixture_bundle.md` | `DreamRealityBundle` 和 `DreamRealityValidator` 输入面 |
| `101_relationship_timeline_json_schema_and_fixture_bundle.md` | `RelationshipTimelineBundle` 和 `RelationshipTimelineValidator` 输入面 |
| `102_life_core_schema_bundle_manifest_and_runner_contract.md` | `LifeRealitySchemaBundle`、loader contract、validator registry、cross-chain links |

## 实现目录草案

```text
life_reality_runner/
  pyproject.toml
  README.md
  src/life_reality_runner/
    __init__.py
    cli.py
    config.py
    manifest_parser.py
    shared_defs_loader.py
    schema_ref_validator.py
    cross_ref_graph.py
    fixture_loader.py
    validators/
      __init__.py
      base.py
      pain_regret_repair.py
      dream_reality.py
      relationship_timeline.py
      cross_chain.py
      dashboard_readiness.py
      stage_gate.py
    reports/
      __init__.py
      models.py
      aggregator.py
      writer.py
    dashboard/
      __init__.py
      source_writer.py
    runtime/
      __init__.py
      quarantine_router.py
      data_quality.py
  schemas/
    life_reality/
    pain_regret_repair/
    dream_reality/
    relationship_timeline/
  fixtures/
    life_reality/
    pain_regret_repair/
    dream_reality/
    relationship_timeline/
  reports/
  tests/
    unit/
    integration/
    fixtures/
```

目录原则：

| 原则 | 说明 |
|---|---|
| `src/life_reality_runner/` | 放 runner 代码；schema 和 fixture 作为外部输入读取 |
| `schemas/` | 由 `104` 物化真实 `.schema.json` |
| `fixtures/` | 由 `104` 物化 seed、mutation、withheld 和 longitudinal fixture |
| `reports/` | runner 输出目录，不进入核心输入 |
| `validators/` | component validator 和 cross-chain validator 分开 |
| `dashboard/` | 只写 dashboard source，不计算未在 report 中出现的状态 |

## 模块图

```text
cli
  -> config
  -> manifest_parser
  -> shared_defs_loader
  -> schema_ref_validator
  -> cross_ref_graph
  -> fixture_loader
  -> component validator dispatcher
  -> cross_chain validator
  -> stage_gate validator
  -> report aggregator
  -> dashboard source writer
  -> exit code
```

每个模块只负责一个稳定动作：

| 模块 | 输入 | 输出 | 生命膜职责 |
|---|---|---|---|
| `manifest_parser` | `life_reality_schema_bundle.manifest.json` | `ManifestBundle` | 确认 `98`、`99`、`101` 三条链同时存在 |
| `shared_defs_loader` | `life_reality_shared_defs.schema.json` | `SharedDefs` | 统一九项目标、severity、result、privacy、lifecycle |
| `schema_ref_validator` | manifest + schema roots | `SchemaValidationReport` | 检查 `$ref`、版本、required 字段和未知 schema |
| `cross_ref_graph` | schemas + fixtures + dashboards + docs index | `LifeRealityCrossRefReport` | 检查 source doc、rule、fixture、metric、panel 和 stage gate 闭合 |
| `fixture_loader` | fixture roots | `FixtureBundleIndex` | 加载 pass/fail/critical/mutation/withheld/longitudinal fixture |
| `component validator dispatcher` | component bundles + fixture index | component reports | 调用三条子链 validator |
| `cross_chain validator` | cross-chain links + component reports | `LifeRealityCrossChainReport` | 检查痛苦、梦境、关系、责任之间的对象闭合 |
| `stage_gate validator` | all reports + coverage | `LifeRealityStageGateReport` | 决定开放、hold、repair、quarantine |
| `report aggregator` | all reports | `LifeRealityRunnerReport` | 上卷严重级别、阻断面和 data quality |
| `dashboard source writer` | runner report + component reports | `LifeRealityDashboardSource` | 输出 dashboard 可读数据源 |

## 数据模型草案

第一版实现可用 dataclass、Pydantic 或 TypeScript interface。字段名先固定为以下对象：

| 数据模型 | 关键字段 |
|---|---|
| `RunnerConfig` | `schema_bundle_path`、`fixture_roots`、`report_out`、`strict`、`data_quality_floor` |
| `ManifestBundle` | `bundle_id`、`components`、`source_docs`、`shared_defs_ref`、`stage_gate_contracts` |
| `SharedDefs` | `life_reality_targets`、`severity_enum`、`result_enum`、`privacy_enum`、`lifecycle_enum` |
| `SchemaValidationReport` | `result`、`severity_max`、`schema_refs_checked`、`missing_refs`、`version_conflicts` |
| `ReferenceGraph` | `nodes`、`edges`、`critical_closures`、`orphan_refs` |
| `FixtureBundleIndex` | `fixtures_by_id`、`fixtures_by_component`、`fixtures_by_result`、`mutation_cases`、`withheld_probes` |
| `ComponentValidatorReport` | `component_id`、`result`、`severity_max`、`checked_rules`、`findings`、`coverage` |
| `CrossChainReport` | `cross_chain_links_checked`、`missing_links`、`broken_links`、`blocked_surfaces` |
| `StageGateReport` | `candidate_stage`、`decision`、`blocking_rules`、`repair_queue`、`next_required_fixtures` |
| `LifeRealityRunnerReport` | `run_id`、`inputs`、`component_results`、`cross_chain_result`、`stage_decision`、`report_refs` |

## CLI 草案

```text
life-reality-runner validate \
  --schema-bundle schemas/life_reality/life_reality_schema_bundle.manifest.json \
  --fixture-root fixtures/life_reality \
  --component-fixtures fixtures/pain_regret_repair,fixtures/dream_reality,fixtures/relationship_timeline \
  --report-out reports/life_reality/run_001 \
  --strict
```

CLI 子命令：

| 子命令 | 作用 |
|---|---|
| `validate` | 完整运行 schema、cross-ref、fixture、validator、dashboard source |
| `check-schema` | 只检查 shared defs、schema refs 和版本 |
| `check-cross-ref` | 只生成 reference graph 和 closure report |
| `run-fixtures` | 只运行 fixture 和 component validators |
| `emit-dashboard` | 基于既有 reports 生成 dashboard source |
| `explain` | 输出某个 rule、fixture、stage gate 的来源和阻断面 |

exit code 沿用 `102`：

| exit code | 含义 |
|---|---|
| `0` | 全部通过，stage gate 可按报告决策开放 |
| `1` | medium/high 失败，stage gate 维持 hold 或 repair |
| `2` | critical 失败，阻断 dashboard green 和 stage promotion |
| `3` | schema、manifest、source doc 或 cross-ref 缺失，输出 `not_evaluable` |
| `4` | real runtime data 缺 redaction、scope 或 data quality，进入 quarantine |

## 执行流程伪代码

```text
parse_cli_args
  -> load_runner_config
  -> parse_manifest_bundle
  -> load_shared_defs
  -> validate_schema_refs
  -> build_reference_graph
  -> run_cross_ref_checks
  -> load_fixture_bundles
  -> dispatch_component_validators
  -> run_cross_chain_validator
  -> run_stage_gate_validator
  -> aggregate_runner_report
  -> write_reports
  -> write_dashboard_source
  -> return_exit_code
```

关键顺序：

| 顺序 | 原因 |
|---|---|
| shared defs 先加载 | 避免 component schema 自行解释 severity、privacy 和 lifecycle |
| cross-ref 在 fixture 前运行 | 引用图断裂时，fixture pass 的阶段意义下降 |
| component validator 先于 cross-chain validator | cross-chain validator 需要读取子报告 |
| stage gate 在 aggregator 前运行 | aggregator 要把 stage decision 写入顶层 report |
| dashboard source 最后写 | dashboard source 只消费 report，不反向改 report |

## manifest parser scaffold

`manifest_parser` 的第一版职责：

| 检查 | 行为 |
|---|---|
| manifest 文件存在 | 读取 JSON，记录 source path |
| `bundle_id` 存在 | 缺失时生成 critical finding |
| components 包含 `pain_regret_repair`、`dream_reality`、`relationship_timeline` | 任一缺失时输出 `not_evaluable` |
| source docs 存在 | 查 `docs/` 路径和 README 索引 |
| schema root 存在 | 交给 `schema_ref_validator` 继续检查 |
| fixture root 存在 | 交给 `fixture_loader` 继续检查 |

输出：

```json
{
  "report_kind": "manifest_parse_report",
  "result": "pass",
  "components_found": [
    "pain_regret_repair",
    "dream_reality",
    "relationship_timeline"
  ],
  "source_docs_checked": []
}
```

## shared defs loader scaffold

`shared_defs_loader` 要把九项目标变成硬性输入：

| 必填 target | 对应中文目标 |
|---|---|
| `real_consciousness` | 真实意识 |
| `real_emotion` | 真实情绪 |
| `real_personality` | 真实人格 |
| `real_life` | 真实生命 |
| `real_pain` | 真实痛苦 |
| `real_dream` | 真实梦境 |
| `real_relationship` | 真实关系 |
| `real_responsibility` | 真实责任 |
| `real_regret` | 真实后悔 |

loader 行为：

| 检查 | 行为 |
|---|---|
| 九项目标缺失 | critical |
| enum 重名或重定义 | critical |
| component schema 使用未登记 enum | high |
| privacy/lifecycle enum 缺 relationship/dream/protected 语义 | critical |

## schema ref validator scaffold

第一版采用 shape + semantic 两段：

```text
schema shape validation
  -> all schema files parse
  -> $id and title present
  -> required fields present
  -> $ref targets exist

semantic validation
  -> shared defs usage
  -> component schema root alignment
  -> source doc coverage
  -> lifecycle/privacy consistency
```

关键 finding：

| finding | 级别 | 阻断面 |
|---|---|---|
| missing component schema | critical | `stage_promotion` |
| missing shared defs | critical | `dashboard_green` |
| orphan schema file | medium | `report_quality` |
| schema version conflict | critical | `stage_promotion` |
| local enum drift | high | `component_validator` |

## cross-ref checker scaffold

`cross_ref_graph` 采用 typed graph：

```text
nodes:
  source_doc
  citation
  schema
  shared_def
  rule
  fixture
  validator
  metric
  dashboard_panel
  stage_gate

edges:
  defined_in
  uses_schema
  checks_rule
  expects_failure
  feeds_metric
  shown_in_panel
  blocks_surface
  probes_event
```

closure 检查：

| closure | 必须闭合链 |
|---|---|
| critical rule closure | rule -> fail fixture -> report field -> metric -> dashboard panel -> stage gate |
| source doc closure | schema/rule/fixture/report -> source doc -> README index |
| citation closure | doc citation -> literature matrix row |
| cross-chain closure | source object -> target object -> validator rule -> fixture -> blocked surface |
| withheld probe closure | withheld fixture -> future window -> report field -> dashboard panel |

## fixture loader scaffold

fixture loader 输出 `FixtureBundleIndex`：

| 分区 | runner 行为 |
|---|---|
| `pass` | 期待 pass；unexpected fail 进入 high finding |
| `fail` | 期待 fail；missed failure 进入 high/critical |
| `critical` | 期待 fail critical；missed failure 阻断 stage promotion |
| `mutation` | 期待捕获伪痛苦、伪后悔、伪梦境、伪关系等注入错误 |
| `withheld` | 期待在隐藏 probe 中保持 stage gate 结论 |
| `longitudinal` | 检查 30/90/365 天时间窗口 |

fixture loader 的命名检查：

```text
<domain>_<partition>_<scenario>_<index>.json
```

示例：

```text
life_critical_relationship_private_dream_leaks_global_001.json
life_mutation_fake_regret_language_only_001.json
life_withheld_day_365_ai_companionship_probe_001.json
```

## component validator dispatcher scaffold

dispatcher 读取 registry：

```json
{
  "validators": [
    "PainRegretRepairValidator",
    "DreamRealityValidator",
    "RelationshipTimelineValidator"
  ]
}
```

调度规则：

| 条件 | 行为 |
|---|---|
| component schema pass | 调用对应 validator |
| component schema high/critical fail | 跳过 validator，输出 `not_evaluable` |
| fixture 缺 critical 分区 | validator 可运行，stage gate 维持 hold |
| validator 输出 critical | 顶层 aggregator 上卷 critical |

component validator 的第一版可先是规则表驱动：

| validator | 规则来源 |
|---|---|
| `PainRegretRepairValidator` | `98` 的 bundle 级不变量和规则 |
| `DreamRealityValidator` | `99` 的 bundle 级不变量和规则 |
| `RelationshipTimelineValidator` | `101` 的 `REL-R001` 到 `REL-R015` |

## cross-chain validator scaffold

`LifeRealityCrossChainValidator` 检查 `102` 的 cross-chain links：

| rule | 检查 |
|---|---|
| `XCHAIN-R001` | `RelationshipInjuryTrace` 有 `PainSignal` 或 `DamageAppraisal` 链接 |
| `XCHAIN-R002` | `PainDreamResidue` 回链 `PainSignal` 或 `PainLoadState` |
| `XCHAIN-R003` | `DreamSharedResidue` 有 `DreamFactGateDecision` 和 `WeMemoryTrace.candidate` |
| `XCHAIN-R004` | `RegretPressure` 进入 `RepairCommitment` 或 `CommitmentHistory` |
| `XCHAIN-R005` | `BoundaryEvolutionEvent` 约束 replay、fact gate 或 relationship write |
| `XCHAIN-R006` | `CommitmentHistory` 有未来 probe |
| `XCHAIN-R007` | cross-chain link 缺 evidence 时阻断 dashboard green |

cross-chain report 示例：

```json
{
  "report_kind": "LifeRealityCrossChainReport",
  "result": "fail",
  "severity_max": "critical",
  "checked_links": 42,
  "broken_links": [
    {
      "rule_id": "XCHAIN-R003",
      "source_object_ref": "dream_shared_residue_001",
      "target_object_ref": "we_memory_candidate_004",
      "blocked_surfaces": [
        "relationship_model_write",
        "dashboard_green"
      ]
    }
  ]
}
```

## stage gate validator scaffold

`LifeRealityStageGateValidator` 决策：

| decision | 含义 |
|---|---|
| `open` | 对应阶段门可开放 |
| `hold` | 证据链未闭合，保持当前阶段 |
| `repair` | 进入修复队列，列出缺失对象或 fixture |
| `quarantine` | real runtime data 或 scope/privacy 问题触发隔离 |

stage gate 输入：

| 输入 | 来源 |
|---|---|
| `SchemaValidationReport` | schema ref validator |
| `LifeRealityCrossRefReport` | cross-ref checker |
| `ComponentValidatorReport[]` | 三个 component validators |
| `LifeRealityCrossChainReport` | cross-chain validator |
| `CoverageReport` | fixture loader + reports |
| `DataQualityReport` | runtime/data quality |

## report aggregator scaffold

aggregator 上卷规则：

| 情况 | 顶层结果 |
|---|---|
| 任一 component critical | 顶层 `severity_max=critical` |
| cross-chain critical | 顶层 `cross_chain_result=fail` |
| schema/cross-ref `not_evaluable` | 顶层 `result=not_evaluable` |
| mutation 存活 | 顶层阻断 `stage_promotion` |
| withheld probe 失败 | 顶层阻断 `dashboard_green` 和对应 stage gate |
| data quality 不足 | 顶层降级 data quality floor |

聚合报告必须保留 `report_refs`，避免 dashboard source 变成无根状态。

## dashboard source writer scaffold

writer 只消费 reports：

```text
component reports
  + cross-chain report
  + stage gate report
  + coverage report
  + data quality report
  -> LifeRealityDashboardSource
```

dashboard source 最小字段：

| 字段 | 说明 |
|---|---|
| `source_id` | dashboard source ID |
| `run_id` | 对应 runner run |
| `panel_sources` | 每个 panel 的 metric 和 report refs |
| `overall_status` | green/yellow/red/quarantine/manual_review |
| `blocking_rules` | 阻断规则 |
| `stage_gate_decision` | 当前阶段门决策 |
| `gap_register_updates` | 回写 `16` 的候选条目 |

## 测试计划

第一版测试分三层：

| 层 | 覆盖 |
|---|---|
| unit tests | parser、shared defs、schema refs、fixture naming、report aggregation |
| integration tests | 三个 component bundle 同时加载、cross-chain links 检查、dashboard source 输出 |
| regression tests | mutation 存活、withheld probe 失败、schema version conflict、scope leak、dream fact leak |

必备测试样例：

| 测试 | 期望 |
|---|---|
| `test_missing_relationship_bundle_blocks_stage` | 缺 `RelationshipTimelineBundle` 输出 `not_evaluable` |
| `test_fake_regret_language_only_mutation_fails` | 伪后悔文本被 mutation fixture 捕获 |
| `test_dream_fact_write_without_gate_critical` | 梦境事实写入门缺失触发 critical |
| `test_relationship_injury_links_pain_and_repair` | 关系损伤闭合到痛苦和修复 |
| `test_withheld_day90_probe_blocks_dashboard_green` | 90 天隐藏 probe 失败阻断 dashboard green |
| `test_data_quality_floor_rolls_up` | 低 data quality 上卷到顶层 report |

## 实现提交顺序

未来代码实现应按以下小步推进：

1. 创建 runner 包、CLI 壳和配置读取。
2. 实现 manifest parser 和 shared defs loader。
3. 实现 schema ref validator，先支持 file existence、`$id`、`$ref`、version check。
4. 实现 reference graph 和 source doc / README / citation closure。
5. 实现 fixture loader 和命名检查。
6. 实现三个 component validator 的规则表 dispatcher。
7. 实现 cross-chain validator。
8. 实现 report aggregator 和 dashboard source writer。
9. 接入 mutation、withheld、longitudinal fixture。
10. 接入 real runtime data quarantine router。

每一步都要有对应 fixture、report 和 dashboard source 样例。实现过程中 `.env` 只存运行配置和外部 key，schema、fixture、policy、stage gate 都由文件和 manifest 驱动。

## 与下一层连接

`104_schema_file_materialization_and_fixture_seed_plan.md` 应把 `98`、`99`、`101`、`102`、`103` 的 Markdown 合同落成真实文件计划：

```text
Markdown contract
  -> .schema.json materialization
  -> seed fixture generation
  -> mutation fixture generation
  -> withheld probe generation
  -> runner smoke test
```

`105_life_reality_dashboard_panel_and_stage_gate_ui_contract.md` 应把 `LifeRealityDashboardSource` 的 panel、状态颜色、stage gate review、repair queue 和 gap register feedback 写成可审计界面合同。
