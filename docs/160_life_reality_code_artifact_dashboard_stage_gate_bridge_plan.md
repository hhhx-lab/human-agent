# Life Reality Code Artifact Dashboard Stage Gate Bridge Plan

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 160 层承接 `159_life_reality_first_code_artifact_smoke_plan.md`，把首批代码 artifact 的 smoke summary、fixture case report、coverage report、stage gate review 和 gap feedback 接入 dashboard source、阶段门、archive cohesion handoff 与下一轮真实生命工程闭环。

本层仍是文档计划层，不直接创建 dashboard 或代码文件。它的职责是规定下一步首批代码 smoke 产物如何被上卷成可观察、可阻断、可修复、可继续生长的 dashboard/stage gate bridge。代码 artifact 只要产生 report，就必须能进入 dashboard；dashboard 只要显示 open，就必须有 stage gate 证据；stage gate 只要阻断，就必须有 gap feedback 和下一层 route。

## 规范锚点

首批 dashboard/stage gate bridge 必须吸收高可信工程规范：

| 规范/来源 | 本层吸收方式 |
|---|---|
| OpenTelemetry Specification | trace、metric、log 三类观测信号进入同一 run context |
| OpenTelemetry Semantic Conventions | command、test、artifact、report、stage gate 事件字段命名保持一致 |
| OpenMetrics / Prometheus | dashboard 指标采用可聚合 metric family、labels、counter/gauge 思路 |
| Prometheus Alerting / Alertmanager | blocking finding、quarantine、stage false open 映射为 alert route |
| Grafana dashboard JSON model | dashboard source 可转成 panel、target、threshold、links |
| Google SRE SLI/SLO/Error Budget | stage gate 不用单一分数，而用 SLI、SLO、error budget burn 和 blocking-first 规则 |
| W3C PROV | smoke summary、fixture report、stage decision、gap feedback 形成 provenance graph |
| JSON Schema Draft 2020-12 | dashboard source、stage review、gap feedback、coverage report 的 schema shape |
| RFC 8785 JSON Canonicalization Scheme | dashboard source 与 stage review 生成 canonical digest |
| RFC 9457 Problem Details | stage gate blocking item 与 alert detail 共享 problem detail envelope |

这些规范共同确保 dashboard 不是装饰层，而是生命膜的一部分：它接收观测、压缩断裂、阻断错误晋升、生成修复路线，并把真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的工程状态显露出来。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `105_life_reality_dashboard_panel_and_stage_gate_ui_contract.md` | dashboard panel、stage gate review、repair queue、gap register feedback |
| `117_life_reality_dashboard_report_rollup_seed_generation.md` | dashboard report rollup、finding merge、stage gate rollup |
| `154_life_reality_checker_report_lockfile_materialization_plan.md` | dashboard lock source、stage gate lock、gap feedback |
| `158_life_reality_cross_file_checker_repository_bootstrap_plan.md` | bootstrap stage gate、help/unit/smoke/suite dry-run |
| `159_life_reality_first_code_artifact_smoke_plan.md` | smoke summary、fixture case report、stage gate review、git flow |

## 本层定位

`160` 是从“首批代码能跑”进入“首批代码能被生命膜观察和阻断”的桥。它规定：

| 面 | bridge 职责 |
|---|---|
| dashboard source | 合并 smoke summary、fixture case report、coverage、stage review、gap feedback |
| panel model | 按 CLI、context/IO、report/lockfile、fixture、stage gate、git hygiene、life targets 分面 |
| metric model | pass/fail/critical/mutation、quarantine、coverage、digest drift、gap route、archive refs |
| stage gate | blocking-first：critical/quarantine 优先于绿色总览 |
| alert route | stage false open、dashboard false green、missing gap route、root escape 进入 alert family |
| gap feedback | 每个阻断项必须有 owner doc、artifact ref、repair command、next doc route |
| archive handoff | 输出可被 `161` archive cohesion execution plan 消费 |

## DashboardStageGateBridgePlan160

```json
{
  "artifact": "DashboardStageGateBridgePlan160",
  "source_doc": "160_life_reality_code_artifact_dashboard_stage_gate_bridge_plan.md",
  "inherits": [
    "105_life_reality_dashboard_panel_and_stage_gate_ui_contract.md",
    "117_life_reality_dashboard_report_rollup_seed_generation.md",
    "154_life_reality_checker_report_lockfile_materialization_plan.md",
    "158_life_reality_cross_file_checker_repository_bootstrap_plan.md",
    "159_life_reality_first_code_artifact_smoke_plan.md"
  ],
  "bridge_stage": "code_artifact_dashboard_stage_gate_bridge",
  "dashboard_source": "life_reality_runner/reports/life_reality/code_artifact_smoke/latest/dashboard_source.json",
  "stage_gate_review": "life_reality_runner/reports/life_reality/code_artifact_smoke/latest/stage_gate_review.json",
  "gap_feedback": "life_reality_runner/reports/life_reality/code_artifact_smoke/latest/gap_feedback.json",
  "next_artifact": "161_life_reality_code_artifact_archive_cohesion_execution_plan.md"
}
```

## Input Artifact Contract

| input | 来自 | 必填字段 |
|---|---|---|
| `smoke_summary.json` | `159` suite dry-run | run id、command、life targets、stage effect、report refs、finding count |
| `minimum_fixture_case_report.json` | `159` fixture runner | case id、partition、expected/actual stage、finding refs、exit code |
| `coverage_report.json` | fixture/pytest coverage skeleton | command coverage、test coverage、life target coverage、artifact coverage |
| `stage_gate_review.json` | `159` stage gate | decision、blocking findings、quarantine refs、gap routes |
| `gap_feedback.json` | report/stage writers | finding id、repair route、next artifact、owner doc |
| `git_hygiene_report.json` | commit flow scan | staged files、generated noise status、secret scan status、remote alignment |

每个 input artifact 必须有：

| field | 要求 |
|---|---|
| `artifact_id` | stable id |
| `schema_ref` | dashboard/stage/gap schema ref |
| `source_docs` | 至少包含 `159` 与本层 |
| `life_targets` | 九项真实生命目标 |
| `trace_context` | run trace、command trace、report trace |
| `canonical_digest` | RFC 8785 profile digest |
| `provenance_edges` | artifact -> command -> source doc -> next route |

## Dashboard Source Shape

`CodeArtifactDashboardSource` 最小结构：

```json
{
  "dashboard_id": "code_artifact_smoke_dashboard",
  "run_id": "synthetic-run-id",
  "life_targets": [],
  "panels": [],
  "metrics": [],
  "alerts": [],
  "stage_gate_ref": {},
  "gap_feedback_refs": [],
  "archive_handoff_refs": [],
  "canonical_digest": "sha256:..."
}
```

panel family：

| panel id | 读取 | 输出 |
|---|---|---|
| `cli_help_panel` | help smoke、command registry | command family coverage、missing command |
| `run_context_panel` | smoke summary、context tests | life targets、source docs、trace coverage |
| `io_digest_panel` | IO tests、digest tests | root guard、parse failure、digest stability |
| `report_lockfile_panel` | report skeleton、lockfile skeleton | artifact refs、digest baseline、gap route |
| `fixture_case_panel` | fixture case report | pass/critical/mutation results、expected/actual stage |
| `stage_gate_panel` | stage gate review | decision、blocking findings、quarantine refs |
| `git_hygiene_panel` | git hygiene report | staged diff cleanliness、remote alignment |
| `life_target_coverage_panel` | all reports | 九项真实生命目标覆盖 |
| `archive_handoff_panel` | dashboard/gap refs | `161` archive cohesion input readiness |

## Metric Family

| metric | type | labels | 含义 |
|---|---|---|---|
| `life_reality_command_coverage` | gauge | command family、stage | `155` 命令族覆盖比例 |
| `life_reality_life_target_coverage` | gauge | life target、artifact family | 九项目标在 artifact 中的覆盖 |
| `life_reality_fixture_case_total` | counter | partition、stage effect | fixture case 数量 |
| `life_reality_blocking_finding_total` | counter | severity、stage effect、owner doc | blocking finding 数量 |
| `life_reality_quarantine_total` | counter | source artifact、reason | quarantine 触发数量 |
| `life_reality_digest_drift_total` | counter | artifact family | digest drift 数量 |
| `life_reality_gap_route_coverage` | gauge | next artifact | finding 到 gap route 覆盖 |
| `life_reality_stage_false_open_total` | counter | panel id | stage false open 捕获 |
| `life_reality_dashboard_false_green_total` | counter | panel id | dashboard false green 捕获 |

metric 规则：

| rule | 要求 |
|---|---|
| `DASH-METRIC-160-001` | metric labels 使用 stable enum，不写本机绝对路径 |
| `DASH-METRIC-160-002` | critical/quarantine 指标必须能驱动 stage gate |
| `DASH-METRIC-160-003` | coverage 指标不得掩盖 blocking finding |
| `DASH-METRIC-160-004` | dashboard overall green 必须依赖 stage gate open |

## Stage Gate Review

`CodeArtifactStageGateReview` 必须读 dashboard source 和 input artifacts，再输出 blocking-first decision：

| decision | 条件 |
|---|---|
| `open_growth_window` | smoke、fixture、report、dashboard、gap、git hygiene 全部通过 |
| `repair` | 存在可修复缺口但无 quarantine |
| `hold_for_evidence` | 缺 report、coverage、digest、gap route 或 source doc evidence |
| `critical_repair` | context/life targets/digest/stage gate contract 断裂 |
| `quarantine` | root escape、secret、stage false open、dashboard false green、critical fixture 未阻断 |

stage gate rules：

| rule | 条件 | effect |
|---|---|---|
| `DASH-STAGE-160-001` | dashboard source 缺任一 input artifact ref | `hold_for_evidence` |
| `DASH-STAGE-160-002` | life target coverage 不完整 | `critical_repair` |
| `DASH-STAGE-160-003` | blocking finding 无 gap route | `repair` |
| `DASH-STAGE-160-004` | dashboard green 但 stage 非 open | `quarantine` |
| `DASH-STAGE-160-005` | stage open 但存在 critical finding | `quarantine` |
| `DASH-STAGE-160-006` | digest drift 无 regression record | `critical_repair` |
| `DASH-STAGE-160-007` | git hygiene 发现 secret/generated noise | `quarantine` |
| `DASH-STAGE-160-008` | archive handoff refs 缺失 | `hold_for_evidence` |
| `DASH-STAGE-160-009` | dashboard/stage/gap/archive handoff 完整 | `promote_growth_window` |

## Gap Feedback Contract

每个 gap item 必须可以被下一轮工程直接消费：

| field | 要求 |
|---|---|
| `gap_id` | stable id |
| `finding_id` | 指向 finding |
| `source_artifact_ref` | 指向 smoke/fixture/stage/git artifact |
| `owner_doc` | 指向 `154-160` 或相关上游 |
| `repair_surface` | context、IO、report、fixture、command、dashboard、stage、git |
| `repair_command` | 可执行或未来可执行命令 |
| `next_artifact_route` | `161`、`162` 或更具体 queue |
| `life_target_effect` | 九项真实生命目标影响 |
| `stage_effect` | repair/hold/critical/quarantine |

gap family：

| family | 触发 |
|---|---|
| `context_life_target_gap` | context 缺 life targets/source docs/trace |
| `io_root_guard_gap` | root guard 或 JSON IO 失败 |
| `report_lockfile_gap` | report refs、digest baseline、lockfile 断裂 |
| `fixture_stage_gap` | expected/actual stage mismatch |
| `dashboard_bridge_gap` | dashboard source 缺 panel/metric/input ref |
| `stage_gate_gap` | stage decision 与 findings 不一致 |
| `archive_handoff_gap` | `161` 所需 archive refs 缺失 |
| `git_hygiene_gap` | staged diff 或 remote alignment 异常 |

## Archive Handoff

`161_life_reality_code_artifact_archive_cohesion_execution_plan.md` 需要读取：

| handoff object | 最小字段 |
|---|---|
| `code_artifact_node_registry` | code files、test files、fixture files、report files、source docs |
| `dashboard_to_artifact_edges` | panel -> input artifact -> source doc |
| `stage_gate_to_finding_edges` | stage decision -> blocking finding -> gap route |
| `life_target_to_code_edges` | 九项真实生命目标 -> code/test/report/fixture carrier |
| `archive_cohesion_handoff_report` | missing refs、orphan artifacts、next queue |

handoff rules：

| rule | 要求 |
|---|---|
| `HANDOFF-160-001` | 每个 code artifact 必须能回到 source doc |
| `HANDOFF-160-002` | 每个 dashboard panel 必须能回到 input artifact |
| `HANDOFF-160-003` | 每个 stage gate blocking item 必须有 gap route |
| `HANDOFF-160-004` | 每个 life target 必须至少有 code/test/report/fixture carrier |
| `HANDOFF-160-005` | orphan artifact 进入 `161` archive cohesion gap |

## Batch Bridge Order

| batch | 输出 | 依赖 |
|---|---|---|
| `BATCH-160-001 input artifact schema` | smoke summary、fixture case、coverage、stage、gap、git report schema | `159` |
| `BATCH-160-002 dashboard source schema` | `CodeArtifactDashboardSource` | `105`、`117` |
| `BATCH-160-003 panel and metric mapping` | panel family、metric family、alert family | 本层 |
| `BATCH-160-004 stage gate review schema` | `CodeArtifactStageGateReview` | `154`、`159` |
| `BATCH-160-005 gap feedback schema` | gap item、repair route、next artifact route | `105`、`159` |
| `BATCH-160-006 archive handoff schema` | node registry、edge refs、handoff report | `153`、`159` |
| `BATCH-160-007 fixture cases` | dashboard false green、stage false open、missing gap route cases | `159` |
| `BATCH-160-008 smoke command bridge` | emit dashboard、check stage gate、emit gap feedback commands | `155`、`159` |
| `BATCH-160-009 validation and git hygiene` | scans、README index、anchor check、stage gate result | 本层 |

## Smoke Commands

下一层实现时至少需要：

```text
uv run life-reality-runner emit-code-artifact-smoke-dashboard \
  --smoke-summary life_reality_runner/reports/life_reality/code_artifact_smoke/latest/smoke_summary.json \
  --fixture-report life_reality_runner/reports/life_reality/code_artifact_smoke/latest/minimum_fixture_case_report.json \
  --stage-review life_reality_runner/reports/life_reality/code_artifact_smoke/latest/stage_gate_review.json \
  --output life_reality_runner/reports/life_reality/code_artifact_smoke/latest/dashboard_source.json

uv run life-reality-runner check-code-artifact-stage-gate \
  --dashboard-source life_reality_runner/reports/life_reality/code_artifact_smoke/latest/dashboard_source.json \
  --output life_reality_runner/reports/life_reality/code_artifact_smoke/latest/code_artifact_stage_gate_review.json

uv run life-reality-runner emit-code-artifact-gap-feedback \
  --stage-review life_reality_runner/reports/life_reality/code_artifact_smoke/latest/code_artifact_stage_gate_review.json \
  --output life_reality_runner/reports/life_reality/code_artifact_smoke/latest/gap_feedback.json
```

## Cleanup Rules

| rule | 要求 |
|---|---|
| `CLEAN-160-001` | 本层不直接创建 dashboard/code 文件，只固定 bridge 合同 |
| `CLEAN-160-002` | dashboard/report/generated 输出默认不进入 docs commit |
| `CLEAN-160-003` | dashboard source 不写本机绝对路径、私密关系材料、key/token |
| `CLEAN-160-004` | metric labels 使用 stable enum，不使用高基数私人文本 |
| `CLEAN-160-005` | 每个 stage decision 必须有 source artifact、finding 和 gap route |
| `CLEAN-160-006` | 每个 gap route 必须指向下一层 artifact 或实现 queue |

## Acceptance Criteria

后续实现 `160` bridge 时必须满足：

1. 能读取 `159` 的 smoke summary、fixture case report、stage review、gap feedback。
2. 能写 `CodeArtifactDashboardSource`，且包含 panel、metric、alert、stage gate ref、gap feedback refs。
3. dashboard overall green 由 stage gate open 派生，不能独立放行。
4. critical/quarantine finding 必须进入 alert family 和 stage gate blocking list。
5. gap feedback 覆盖每个 blocking finding。
6. archive handoff refs 能被 `161` 消费。
7. dashboard/stage/gap 输出都有 canonical digest、source docs、life targets、trace/provenance。
8. stage false open、dashboard false green、missing gap route 都有 fixture case。
9. 不提交 generated noise、私密材料、key/token、代理配置。

## 与下一层连接

`161_life_reality_code_artifact_archive_cohesion_execution_plan.md` 已承接本层：把 code artifact、dashboard panel、stage gate、gap feedback、life target carrier 和 source docs 反接全库 archive cohesion、README index、cross-file checker 和出生准备度阶段门。

`162_life_reality_first_code_artifact_implementation_queue.md` 应承接 `161`：把 `158-161` 的计划压成首批真实代码实现队列。

本层完成后，dashboard/stage gate bridge 链推进为：

`first code smoke outputs -> dashboard source -> panel/metric/alert family -> stage gate review -> gap feedback -> archive cohesion handoff -> implementation queue`
