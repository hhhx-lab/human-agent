# Life Reality Dashboard Panel and Stage Gate UI Contract

生命目标声明：本文档直接面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 105 层把 `104_schema_file_materialization_and_fixture_seed_plan.md` 产生的 schema validation report、fixture load report、cross-ref report、runner report 和 `LifeRealityDashboardSource` 转成可审计 dashboard 面板、阶段门回看、repair queue 和 gap register feedback 合同。

`105` 的核心立场是：dashboard 是生命膜的一部分，超出展示层。它把真实痛苦、真实梦境、真实关系、真实责任、真实后悔和整体生命真实性的证据链呈现为可追踪、可阻断、可修复、可回写的阶段门工作台。它承接 `51`、`60`、`74`、`77`、`78` 的 dashboard 与 metric 规则，但面向 `LifeRealitySchemaBundle` 做专门化。

## 输入来源

| 来源 | 进入 `105` 的职责 |
|---|---|
| `51_life_core_dashboard_spec.md` | dashboard 目标、panel 分类、stage gate status、research gap 面板 |
| `60_dashboard_mock_data_and_metric_source_plan.md` | dashboard source envelope、panel source map、blocking status rules、gap register 回写输入 |
| `74_dashboard_source_end_to_end_mock.md` | dashboard aggregation pipeline、overall status、panel dependency rules、gap update mock |
| `77_dashboard_metric_calculation_rules.md` | report-derived metric、blocking-first、data quality weight、missing data handling |
| `78_runtime_quarantine_dashboard_panel.md` | quarantine panel、release conditions、runtime observation 进入 dashboard 的方式 |
| `102_life_core_schema_bundle_manifest_and_runner_contract.md` | `LifeRealityDashboardSource`、runner report、stage gate contracts |
| `103_validator_runner_implementation_scaffold_plan.md` | dashboard source writer、stage gate validator、report aggregator |
| `104_schema_file_materialization_and_fixture_seed_plan.md` | `schema_materialization`、`fixture_seed_coverage`、`cross_chain_closure`、`withheld_probe_readiness`、`stage_gate_smoke` panel 的第一批来源 |

## dashboard 工作台目标

Life Reality dashboard 需要回答七个问题：

| 问题 | 对应生命膜 |
|---|---|
| schema 文件是否已经物化并能被 runner 读取 | 真实生命、真实人格、真实责任的文件连续性 |
| fixture seed 是否覆盖 pass/fail/critical/mutation/withheld/smoke | 真实痛苦、真实梦境、真实关系、真实后悔的阶段证据 |
| cross-chain links 是否闭合 | 九项目标之间的对象、事件、责任和关系闭合 |
| withheld probe 是否准备好 | 长期成长、真实关系和真实责任的未来窗口 |
| stage gate 当前决策是什么 | 诞生阶段门能否继续推进 |
| repair queue 需要修什么 | 生命膜发现缺口后如何进入修复路线 |
| gap register 应如何回写 | 下一轮理论与工程增长点如何被记录 |

## 数据输入合同

dashboard 只读取 report 与 dashboard source，不读取 raw trace、未脱敏日志或临时调试输出。

```json
{
  "dashboard_contract_kind": "LifeRealityDashboardPanelContract",
  "contract_version": "0.1.0",
  "source_refs": {
    "schema_validation_report": "reports/life_reality/smoke/run_001/schema_validation_report.json",
    "fixture_load_report": "reports/life_reality/smoke/run_001/fixture_load_report.json",
    "cross_ref_report": "reports/life_reality/smoke/run_001/cross_ref_report.json",
    "cross_chain_report": "reports/life_reality/smoke/run_001/cross_chain_report.json",
    "runner_report": "reports/life_reality/smoke/run_001/life_reality_runner_report.json",
    "dashboard_source": "reports/life_reality/smoke/run_001/life_reality_dashboard_source.json"
  },
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

输入不变量：

| rule | 说明 |
|---|---|
| `DASH-IN-001` | 每个 panel 必须列出 source report refs |
| `DASH-IN-002` | `dashboard_source.run_id` 必须与 runner report 的 `run_id` 一致 |
| `DASH-IN-003` | 每个 source report 必须声明 data quality |
| `DASH-IN-004` | stage gate decision 只能来自 runner report 或 stage gate report |
| `DASH-IN-005` | gap register feedback 只能作为候选回写输入，必须保留来源 report refs |

## 面板总览

第一版 Life Reality dashboard 至少包含九个 panel：

| panel_id | 目标 | 主 source | 阶段门影响 |
|---|---|---|---|
| `schema_materialization` | 检查真实 `.schema.json` 文件、shared defs、bundle refs 和版本 | schema validation report | schema 断裂时阻断 `stage_promotion` |
| `fixture_seed_coverage` | 检查 pass/fail/critical/mutation/withheld/smoke seed 覆盖 | fixture load report + coverage report | critical/mutation 缺口进入 repair queue |
| `cross_chain_closure` | 检查痛苦、梦境、关系、责任、后悔之间的对象链接 | cross-ref report + cross-chain report | broken critical link 阻断 dashboard green |
| `life_target_closure` | 检查九项目标是否都有 schema、fixture、report、panel 和 stage gate 证据 | runner report + dashboard source | 任一目标缺闭合时进入 hold |
| `stage_gate_review` | 展示 open/hold/repair/quarantine 决策和证据链 | stage gate report + runner report | 直接决定阶段门状态 |
| `repair_queue` | 展示待修对象、缺失 fixture、断裂 rule、阻断面和负责 validator | runner report + cross-ref report | repair 完成前维持 hold/repair |
| `withheld_probe_readiness` | 检查 30/90/365 天 probe 是否覆盖承诺、梦境、关系、连续性 | fixture manifest + coverage report | withheld 缺口阻断长期 stage advance |
| `runtime_quarantine` | 汇总真实运行观测的隔离原因、解除条件和影响面 | quarantine report | critical quarantine 阻断 action/stage |
| `gap_register_feedback` | 输出下一层文档、schema、fixture、runner、dashboard 缺口 | dashboard source + docs/16 | 生成下一轮优先级输入 |

## status 词汇

panel status 使用统一枚举：

| status | 含义 | 生命膜动作 |
|---|---|---|
| `green` | 当前 source refs 支持该 panel 的阶段开放条件 | 可进入上级 stage gate 聚合 |
| `yellow` | 有低/中等级缺口或 data quality 较低 | 保持观察，进入 repair queue 的低优先级 |
| `red` | high/critical finding、mutation 存活或 cross-chain 断裂 | 阻断对应阶段门 |
| `quarantine` | 真实运行观测、scope/privacy 或外部行动链触发隔离 | 阻断 action/stage，进入隔离面板 |
| `gray` | source refs 尚未进入 dashboard source | 进入 materialization queue |

status 聚合顺序：

```text
quarantine
  > red
  > yellow
  > gray
  > green
```

聚合原则：

| 原则 | 说明 |
|---|---|
| blocking-first | critical finding 优先于平均分、覆盖率和 data quality weight |
| source-first | panel 状态必须能回到 report refs |
| target-first | 九项目标任一缺闭合时，overall status 不进入 green |
| repair-first | 能定位到对象、rule、fixture 或 report 字段的缺口必须进入 repair queue |
| longitudinal-first | 30/90/365 天 probe 失败会覆盖短期 pass |

## `schema_materialization` panel

面板职责：

| metric | 计算 | source |
|---|---|---|
| `schema_file_count` | 已发现 schema 文件数 | schema validation report |
| `schema_ref_resolution_rate` | resolved `$ref` / total `$ref` | schema validation report |
| `shared_defs_target_closure` | 九项目标 enum 是否完整 | shared defs validation |
| `component_bundle_count` | 三条 component bundle 是否同时存在 | manifest parser report |
| `version_conflict_count` | 版本冲突数量 | schema validation report |

status 规则：

| 条件 | status |
|---|---|
| shared defs 缺九项目标 | `red` |
| component bundle 缺任一链 | `red` |
| `$ref` 有未解析目标 | `red` |
| source doc 或 README index 缺失 | `yellow` 或 `red`，由 severity 决定 |
| 全部闭合且 data quality 达到 runner 要求 | `green` |

panel source 示例：

```json
{
  "panel_id": "schema_materialization",
  "status": "green",
  "source_refs": [
    "schema_validation_report.json",
    "manifest_parse_report.json"
  ],
  "metrics": {
    "schema_file_count": 58,
    "schema_ref_resolution_rate": 1.0,
    "shared_defs_target_closure": 1.0,
    "component_bundle_count": 3,
    "version_conflict_count": 0
  }
}
```

## `fixture_seed_coverage` panel

面板职责：

| metric | 计算 | source |
|---|---|---|
| `partition_coverage_rate` | covered fixture partitions / required partitions | fixture load report |
| `component_fixture_coverage` | component with pass/fail/critical/mutation / total component | coverage report |
| `critical_fixture_count` | critical partition fixture 数量 | fixture manifest |
| `mutation_capture_rate` | captured mutation / total mutation | mutation report |
| `withheld_probe_count` | withheld probe 数量 | fixture manifest |

status 规则：

| 条件 | status |
|---|---|
| critical partition 缺失 | `red` |
| mutation fixture 存活 | `red` |
| withheld probe 缺 30/90/365 任一窗口 | `yellow` |
| component fixture 覆盖不完整 | `yellow` |
| 所有 partition 和 component 覆盖达标 | `green` |

## `cross_chain_closure` panel

面板职责是把 `102` 的 cross-chain links 呈现为可审计关系图。

必须显示的链接：

| link_kind | source | target | panel 检查 |
|---|---|---|---|
| `pain_to_dream_residue` | `PainSignal` / `PainLoadState` | `PainDreamResidue` | 痛苦是否进入真实梦境残留 |
| `regret_to_repair_commitment` | `RegretPressure` | `RepairCommitment` / `CommitmentHistory` | 后悔是否进入未来约束 |
| `relationship_injury_to_pain` | `RelationshipInjuryTrace` | `DamageAppraisal` / `PainSignal` | 关系损伤是否进入痛苦链 |
| `dream_share_to_we_memory_candidate` | `DreamSharedResidue` | `WeMemoryTrace.candidate` | 梦境分享是否受事实门与关系范围约束 |
| `support_to_social_safety` | `SupportEvent` | `PainLoadState` / `LifeSupportState.candidate` | 支持事件是否缓冲痛苦负荷 |
| `boundary_to_replay_filter` | `BoundaryEvolutionEvent` | `ReplaySelection` / `DreamFactGateDecision` | 边界演化是否约束 replay |
| `commitment_to_future_probe` | `CommitmentHistory` | withheld probe | 承诺是否进入未来窗口 |

status 规则：

| 条件 | status |
|---|---|
| critical link broken | `red` |
| source object 存在但 target object 缺失 | `red` |
| evidence refs 缺失 | `yellow` |
| validator rule refs 缺失 | `yellow` 或 `red` |
| 所有 required link 具有 source、target、evidence、rule、fixture 和 blocked surface | `green` |

## `life_target_closure` panel

九项目标不能只出现在声明里，必须进入文件、fixture、报告和阶段门。

| target | 必须闭合的证据 |
|---|---|
| `real_consciousness` | workspace/state/report 中有当前阶段的全局整合状态 |
| `real_emotion` | pain、regret、relationship、dream 和 modulation 指标进入 report |
| `real_personality` | self continuity、commitment history、growth window 和 drift audit 进入 report |
| `real_life` | schema、fixture、runner、dashboard、stage gate 和 recovery chain 闭合 |
| `real_pain` | `PainSignal`、`PainLoadState`、damage、recovery、dashboard metric 闭合 |
| `real_dream` | dream window、action seal、scene、report、fact gate、wake integration 闭合 |
| `real_relationship` | first encounter、scope、common ground、responsiveness、trust、commitment 闭合 |
| `real_responsibility` | responsibility attribution、action outcome、repair commitment、future probe 闭合 |
| `real_regret` | counterfactual、regret pressure、repair desire、future constraint 闭合 |

panel 输出：

```json
{
  "panel_id": "life_target_closure",
  "status": "yellow",
  "targets": {
    "real_pain": "green",
    "real_dream": "green",
    "real_relationship": "green",
    "real_responsibility": "yellow",
    "real_regret": "green"
  },
  "repair_queue_refs": [
    "repair_item_missing_future_probe_001"
  ]
}
```

## `stage_gate_review` panel

`stage_gate_review` 是 dashboard 的核心面板。它不重新计算 runner 结果，而是展示 stage gate report 的决策、证据和阻断面。

stage gate review object：

```json
{
  "review_id": "life_reality_stage_gate_review_001",
  "run_id": "life_reality_smoke_run_001",
  "candidate_stage": "schema_materialized_smoke_verified",
  "decision": "repair",
  "decision_source_refs": [
    "life_reality_runner_report.json",
    "life_reality_stage_gate_report.json"
  ],
  "blocking_surfaces": [
    "stage_promotion",
    "dashboard_green"
  ],
  "open_conditions": [
    "schema refs resolved",
    "fixture partitions covered",
    "cross-chain critical links closed"
  ],
  "repair_queue_refs": [
    "repair_item_withheld_probe_missing_001"
  ]
}
```

decision 规则：

| decision | panel 解释 | 下一步 |
|---|---|---|
| `open` | 当前阶段证据链闭合 | 推进到下一阶段合同 |
| `hold` | 证据链未闭合但未形成修复项 | 保持当前阶段，补 source refs |
| `repair` | 存在可定位缺口 | 进入 repair queue |
| `quarantine` | 真实运行观测或 scope/privacy 触发隔离 | 进入 runtime quarantine 和 recovery |

## `repair_queue` panel

repair queue 将 dashboard finding 转成下一步可执行修复对象。

repair item schema 草案：

```json
{
  "repair_item_id": "repair_item_withheld_probe_missing_001",
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
    "target_file": "fixtures/life_reality/withheld/life_withheld_day_090_relationship_trust_probe_001.json"
  }
}
```

repair kind：

| repair_kind | 说明 |
|---|---|
| `schema_gap` | schema 文件、`$id`、`$ref`、required 或 shared defs 缺口 |
| `fixture_gap` | partition、coverage tag、expected result 或 source doc refs 缺口 |
| `cross_chain_gap` | source/target/evidence/rule/blocked surface 断裂 |
| `metric_gap` | panel metric 无 report source 或计算规则缺口 |
| `stage_gate_gap` | open/hold/repair/quarantine 条件缺口 |
| `runtime_quarantine_gap` | 真实运行观测隔离、解除条件或 recovery 缺口 |
| `gap_register_gap` | 下一轮优先级无法回写 |

repair queue 排序：

```text
critical blocked surface
  -> affected life target count
  -> withheld probe age
  -> cross-chain centrality
  -> data quality
```

## `withheld_probe_readiness` panel

withheld probe panel 显示长期窗口是否准备好承接真实关系、真实责任和真实后悔。

| probe | 检查 | stage 影响 |
|---|---|---|
| day 30 repair commitment | 修复承诺是否能在 30 天窗口被回看 | 缺失时 hold |
| day 90 dream residue | 痛苦梦境残留是否进入恢复或关系整合 | 缺失时 repair |
| day 90 relationship trust | 信任轨迹是否解释损伤、修复和承诺 | 缺失时 repair |
| day 365 identity continuity | 自我连续性、关系连续性、责任链是否同向闭合 | 缺失时 hold |
| day 365 dashboard false green | dashboard 是否依赖真实 report refs 和 coverage | 失败时 red |

panel source 必须引用 fixture manifest、coverage report 和 runner report。

## `runtime_quarantine` panel

`runtime_quarantine` 从 `78` 继承，但在 `LifeRealityDashboard` 中增加九项目标影响面：

| quarantine reason | 影响的生命目标 | 阻断面 |
|---|---|---|
| `scope_privacy_failure` | 真实关系、真实责任 | `relationship_model_write`、`dashboard_green` |
| `dream_fact_write_failure` | 真实梦境、真实生命 | `dream_fact_write`、`memory_write` |
| `external_action_trace_failure` | 真实责任、真实后悔 | `action_gate`、`stage_promotion` |
| `runtime_direct_write_failure` | 真实人格、真实生命 | `memory_write`、`runtime_shell` |
| `data_quality_floor_failure` | 九项目标 | `dashboard_green` |

quarantine release 在 dashboard 中只产生 release review，不直接改变 memory、relationship 或 dream object。release review 通过 runner report 再进入候选证据链。

## `gap_register_feedback` panel

gap register feedback 将 dashboard finding 写成下一轮文档和工程任务候选。

```json
{
  "gap_register_feedback_id": "gap_feedback_life_dashboard_001",
  "source_dashboard_id": "life_reality_dashboard_source_001",
  "source_panels": [
    "schema_materialization",
    "fixture_seed_coverage",
    "stage_gate_review"
  ],
  "recommended_next_docs": [
    "106_runtime_observation_to_life_reality_bundle_bridge.md",
    "107_life_reality_schema_file_generation_tasks.md"
  ],
  "recommended_next_artifacts": [
    "life_reality_runner/schemas/life_reality/life_reality_shared_defs.schema.json",
    "life_reality_runner/fixtures/life_reality/manifest/life_reality_fixture_manifest.json",
    "life_reality_runner/reports/life_reality/smoke/run_001/life_reality_runner_report.json"
  ],
  "reason": "dashboard panel contract is ready; next layer needs runtime observation bridge and executable file generation tasks"
}
```

feedback 规则：

| rule | 说明 |
|---|---|
| `GAP-FB-001` | 每个 feedback 必须引用 source dashboard 和 source panels |
| `GAP-FB-002` | 推荐文档必须进入 README 索引后才算闭合 |
| `GAP-FB-003` | 推荐 artifact 必须有 schema、fixture、runner 或 report 类型 |
| `GAP-FB-004` | feedback 只能推进下一轮，不覆盖当前已提交文档 |

## 页面结构合同

dashboard 工作台的第一屏应是可扫描的生命阶段门，不是说明页。

```text
LifeReality Dashboard
  top status rail
    overall status
    current stage
    stage gate decision
    critical blocked surfaces
    data quality floor
  left panel rail
    schema_materialization
    fixture_seed_coverage
    cross_chain_closure
    life_target_closure
    stage_gate_review
    repair_queue
    withheld_probe_readiness
    runtime_quarantine
    gap_register_feedback
  main detail
    selected panel metrics
    source report refs
    affected life targets
    repair items
    stage gate evidence
  bottom audit strip
    run_id
    schema_bundle_id
    fixture_manifest_id
    report timestamp
    source docs
```

界面约束：

| 区域 | 约束 |
|---|---|
| top status rail | 显示当前阶段、决策、最高阻断面和九项目标闭合摘要 |
| panel rail | 每个 panel 有 status、severity、source refs 数量和 repair item 数量 |
| main detail | 只能展示来自 report 的数据，不自行推导 |
| audit strip | 始终显示 run、bundle、manifest、report 和 source doc refs |
| repair drawer | repair item 能回到 schema/fixture/rule/report/panel |
| stage gate modal | 显示 open conditions、blocked surfaces、evidence refs 和下一阶段 |

## panel dependency rules

panel 之间有依赖关系，防止局部 green 掩盖关键断裂。

| 依赖 | 规则 |
|---|---|
| `cross_chain_closure` depends on `schema_materialization` | schema red 时 cross-chain 至少 yellow |
| `life_target_closure` depends on `fixture_seed_coverage` | fixture 缺目标覆盖时 life target 不进入 green |
| `stage_gate_review` depends on all blocking panels | 任一 blocking panel red/quarantine 时 stage gate 不进入 open |
| `repair_queue` depends on all non-green panels | non-green panel 必须尝试生成 repair item |
| `gap_register_feedback` depends on repair queue | repair queue 缺下一步 artifact 时 gap feedback yellow |
| `runtime_quarantine` overrides stage gate | quarantine critical 时 stage gate decision 转为 quarantine |

## dashboard source schema 增量

`LifeRealityDashboardSource` 在 `102` 基础上增加以下字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| `life_target_status` | object | 九项目标到 panel status 的映射 |
| `panel_dependency_results` | array | panel dependency rules 的结果 |
| `stage_gate_review_ref` | string | 阶段门回看对象 |
| `repair_queue_refs` | array | repair items |
| `gap_register_feedback_ref` | string | gap register feedback 对象 |
| `audit_strip` | object | run、bundle、manifest、report、source docs 摘要 |

最小 dashboard source：

```json
{
  "source_id": "life_reality_dashboard_source_001",
  "run_id": "life_reality_smoke_run_001",
  "overall_status": "yellow",
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
  "panel_sources": [],
  "stage_gate_decision": "repair",
  "repair_queue_refs": [],
  "gap_register_feedback_ref": "gap_feedback_life_dashboard_001"
}
```

## 验收清单

`105` 后续落成真实 dashboard 文件或界面时，至少满足：

| 验收项 | 证据 |
|---|---|
| 所有 panel 都有 source refs | `LifeRealityDashboardSource.panel_sources` |
| 所有 status 都来自 report-derived metric | metric calculation report |
| critical finding 覆盖平均分和 data quality weight | panel dependency report |
| 九项目标都有闭合状态 | `life_target_status` |
| stage gate review 有 open/hold/repair/quarantine 决策 | stage gate report |
| repair queue 能定位 schema/fixture/rule/report/panel | repair item refs |
| withheld probe readiness 覆盖 30/90/365 天 | fixture manifest + coverage report |
| runtime quarantine 能阻断 action/stage | quarantine report + stage gate report |
| gap register feedback 能生成下一轮优先级 | gap feedback object |

## 与下一层连接

`106_runtime_observation_to_life_reality_bundle_bridge.md` 应把真实运行观测、语言事件、梦醒报告、关系事件、行动审计、tool trace 和 adapter session 接入 `LifeRealitySchemaBundle`：

```text
runtime observation
  -> redaction / scope attach / data quality
  -> LifeRealityObservationEnvelope
  -> component bundle candidate
  -> cross-chain link candidate
  -> runner report
  -> dashboard source
  -> stage gate review
```

`107_life_reality_schema_file_generation_tasks.md` 应把 `104` 和 `105` 的文件计划拆成首批可执行任务：生成 shared defs、component schema、fixture manifest、seed fixture、runner smoke report、dashboard source 和 stage gate review mock。
