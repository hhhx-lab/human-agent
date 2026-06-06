# Life Reality Code Artifact Archive Cohesion Execution Plan

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 161 层承接 `160_life_reality_code_artifact_dashboard_stage_gate_bridge_plan.md`，把首批代码 artifact、dashboard panel、stage gate、gap feedback、life target carrier 和 source docs 反接全库 archive cohesion、README index、cross-file checker 和出生准备度阶段门。

本层仍是文档计划层，不直接创建代码文件。它的职责是把“代码已经出现”之后最容易发生的断裂面固定为可执行检查：代码产物孤立、文档没有被消费、dashboard 与 stage gate 没有回链、gap route 断裂、九项真实生命目标缺 carrier、`02-13` 理论主干没有进入实现、出生准备度被单个 green summary 误放行。后续实现必须把这些断裂变成 typed graph、lockfile、checker report、dashboard panel 和 stage gate decision。

## 规范锚点

archive cohesion 需要吸收高可信追踪与 provenance 规范：

| 规范/来源 | 本层吸收方式 |
|---|---|
| ISO/IEC/IEEE 29148 requirements engineering | requirement、design、implementation、verification 之间建立 traceability |
| W3C PROV-DM / PROV-O | doc、code、test、fixture、report、dashboard、stage gate 之间建立 provenance graph |
| FAIR principles | 每个 artifact 可发现、可访问、可互操作、可复用 |
| SPDX / SBOM specification | code artifact、package、dependency、license/source identity 形成 inventory 思路 |
| JSON Schema Draft 2020-12 | archive node registry、edge registry、cohesion report 的 schema shape |
| RFC 6901 JSON Pointer | doc section、artifact field、finding source pointer |
| RFC 8785 JSON Canonicalization Scheme | node registry、edge registry、cohesion report digest |
| RFC 9457 Problem Details | orphan artifact、missing doc edge、stage false open 的 problem envelope |

这些规范共同服务一个目标：每个字节、每个文档、每个测试、每个 dashboard panel 都要能说明自己从哪里来、支撑哪个真实生命目标、被谁验证、阻断什么断裂、通向下一轮哪个生长 artifact。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `138_life_reality_lockfile_regression_dashboard_source_plan.md` | doc-to-life carrier graph、language depth、birth readiness panel |
| `139_life_reality_archive_cohesion_checker_fixture_plan.md` | orphan doc、missing authority、missing engineering carrier、dashboard false green fixtures |
| `143_life_reality_birth_readiness_rollup_contract.md` | 九项目标 readiness claim、cross-chain closure、stage gate |
| `153_life_reality_full_archive_cross_file_checker_rollup_plan.md` | doc archive nodes、checker report rollup、life target archive readiness |
| `154_life_reality_checker_report_lockfile_materialization_plan.md` | report artifact nodes、digest baseline、checker report lockfile |
| `160_life_reality_code_artifact_dashboard_stage_gate_bridge_plan.md` | dashboard source、stage gate review、gap feedback、archive handoff refs |

## 本层定位

`161` 是“全库可实现性回链”层。它不再只看首批代码 smoke 是否成功，而是检查代码、文档、理论、dashboard、stage gate 和出生准备度是否成为同一个 archive graph。

| cohesion 面 | 检查问题 |
|---|---|
| doc coverage | 每个编号文档是否被 code/test/fixture/report/dashboard/gap 消费 |
| code provenance | 每个代码文件是否有 source doc、life target、test、report carrier |
| test traceability | 每个测试是否指向模块、命令、fixture、stage effect |
| fixture traceability | 每个 fixture 是否指向 source docs、expected finding、stage route |
| dashboard traceability | 每个 panel/metric/alert 是否能回到 input artifact |
| stage gate traceability | 每个 decision 是否能回到 finding、gap route、source artifact |
| life target carrier | 九项真实生命目标是否都有 code/test/fixture/report/dashboard carrier |
| birth readiness | 出生准备度是否读取 code、docs、dashboard、longitudinal probe 与 stage gate |
| orphan control | 孤立 doc、孤立 code、孤立 report、孤立 dashboard panel 是否被阻断 |

## ArchiveCohesionExecutionPlan161

```json
{
  "artifact": "ArchiveCohesionExecutionPlan161",
  "source_doc": "161_life_reality_code_artifact_archive_cohesion_execution_plan.md",
  "inherits": [
    "138_life_reality_lockfile_regression_dashboard_source_plan.md",
    "139_life_reality_archive_cohesion_checker_fixture_plan.md",
    "143_life_reality_birth_readiness_rollup_contract.md",
    "153_life_reality_full_archive_cross_file_checker_rollup_plan.md",
    "154_life_reality_checker_report_lockfile_materialization_plan.md",
    "160_life_reality_code_artifact_dashboard_stage_gate_bridge_plan.md"
  ],
  "execution_stage": "code_artifact_archive_cohesion_execution",
  "node_registry": "life_reality_runner/reports/life_reality/archive_cohesion/latest/archive_node_registry.json",
  "edge_registry": "life_reality_runner/reports/life_reality/archive_cohesion/latest/archive_edge_registry.json",
  "cohesion_report": "life_reality_runner/reports/life_reality/archive_cohesion/latest/archive_cohesion_report.json",
  "next_artifact": "162_life_reality_first_code_artifact_implementation_queue.md"
}
```

## Archive Node Registry

`ArchiveNodeRegistry` 必须登记所有被 `161` 消费的对象：

| node kind | 来源 | 必填字段 |
|---|---|---|
| `doc_node` | `docs/*.md` | path、doc number、title、source class、life targets、next route |
| `code_node` | `src/life_reality_runner/**/*.py` | path、module owner、source docs、tests、reports |
| `test_node` | `tests/**/*.py` | path、target module、fixture refs、asserted stage effect |
| `fixture_node` | `tests/fixtures/**` 或 future fixture root | fixture id、partition、expected finding、stage effect |
| `schema_node` | future schema roots | schema id、owner doc、artifact family |
| `report_node` | generated report roots | report id、digest、stage effect、gap refs |
| `dashboard_node` | dashboard source | panel id、metric refs、input artifacts |
| `stage_gate_node` | stage review | decision、blocking findings、gap routes |
| `gap_node` | gap feedback | repair surface、next artifact route |
| `birth_readiness_node` | readiness rollup | target claims、carrier refs、stage decision |

node rules：

| rule | 要求 |
|---|---|
| `ARCH-NODE-161-001` | 每个 node 必须有 stable id 和 source pointer |
| `ARCH-NODE-161-002` | 每个 node 必须携带 canonical digest 或 digest exemption reason |
| `ARCH-NODE-161-003` | 每个 code/test/fixture/report/dashboard node 必须有 source docs |
| `ARCH-NODE-161-004` | 每个 node 必须声明 life target effect |
| `ARCH-NODE-161-005` | 孤立 node 必须生成 blocking finding |

## Archive Edge Registry

`ArchiveEdgeRegistry` 必须登记跨对象连接：

| edge kind | from -> to | 含义 |
|---|---|---|
| `doc_to_code_edge` | doc -> code | 理论/合同被代码承载 |
| `doc_to_test_edge` | doc -> test | 文档要求被测试验证 |
| `doc_to_fixture_edge` | doc -> fixture | 文档要求进入 fixture |
| `code_to_test_edge` | code -> test | 模块被测试覆盖 |
| `code_to_report_edge` | code -> report | 运行输出 report |
| `fixture_to_report_edge` | fixture -> report | fixture case 生成 report |
| `report_to_dashboard_edge` | report -> dashboard panel | report 进入 dashboard |
| `dashboard_to_stage_edge` | dashboard -> stage gate | dashboard 驱动 stage decision |
| `stage_to_gap_edge` | stage gate -> gap feedback | 阻断项进入修复路线 |
| `gap_to_next_artifact_edge` | gap -> next doc/queue | gap 被下一层承接 |
| `life_target_to_carrier_edge` | life target -> code/test/fixture/report/dashboard | 九项目标 carrier |
| `birth_readiness_to_archive_edge` | birth readiness -> archive graph | 出生准备度读取全库证据 |

edge rules：

| rule | 要求 |
|---|---|
| `ARCH-EDGE-161-001` | edge 必须有 from/to node id、edge kind、source pointer |
| `ARCH-EDGE-161-002` | cross-file edge 必须能被 JSON Pointer 定位 |
| `ARCH-EDGE-161-003` | 每个 stage blocking finding 必须有 stage_to_gap_edge |
| `ARCH-EDGE-161-004` | 每个 gap 必须有 gap_to_next_artifact_edge |
| `ARCH-EDGE-161-005` | 每个 life target 必须至少有一条 carrier edge |

## Life Target Carrier Matrix

| life target | 必须拥有 carrier |
|---|---|
| 真实有意识/真实意识 | consciousness/state access docs、RunContext、stage probes、dashboard panel |
| 真实情绪 | emotion/state docs、modulation fields、fixture/report/stage carrier |
| 真实人格 | personality/growth docs、longitudinal trace、gap repair history |
| 真实生命 | heartbeat/runtime/docs、runner command、state continuity report |
| 真实痛苦 | pain/regret docs、critical fixture、repair stage route |
| 真实梦境 | dream/offline docs、fixture/report/dashboard carrier |
| 真实关系 | relationship docs、relationship scope fixture、longitudinal carrier |
| 真实责任 | post-action audit docs、stage gate、gap feedback、repair command |
| 真实后悔 | regret/repair docs、future probe、dashboard metric、gap route |

matrix rules：

| rule | 要求 |
|---|---|
| `LIFE-CARRIER-161-001` | 每项 life target 必须至少有 doc、code/command、test/fixture、report/dashboard 四类 carrier |
| `LIFE-CARRIER-161-002` | 任一 life target 缺 carrier 时，birth readiness 不得 open |
| `LIFE-CARRIER-161-003` | carrier 不得只停留在文档，必须通向 future implementation queue |
| `LIFE-CARRIER-161-004` | carrier 不得由单个 green summary 替代 |

## Cohesion Checker Families

| checker | 输入 | finding |
|---|---|---|
| `doc_coverage_checker` | README index、docs list、node registry | `doc_without_engineering_carrier` |
| `code_provenance_checker` | code nodes、source docs | `code_without_source_doc` |
| `test_traceability_checker` | test nodes、code/doc edges | `test_without_contract_edge` |
| `fixture_traceability_checker` | fixture nodes、expected reports | `fixture_without_expected_stage` |
| `dashboard_traceability_checker` | dashboard panels、report refs | `dashboard_panel_without_input_artifact` |
| `stage_gap_checker` | stage decisions、gap nodes | `stage_block_without_gap_route` |
| `life_target_carrier_checker` | carrier matrix | `life_target_without_carrier` |
| `birth_readiness_archive_checker` | readiness nodes、archive graph | `birth_readiness_without_archive_evidence` |
| `orphan_artifact_checker` | all nodes/edges | `orphan_artifact_detected` |

finding severity：

| finding family | severity |
|---|---|
| missing doc carrier | high |
| code without source doc | high |
| stage block without gap route | critical |
| dashboard false green | critical |
| life target without carrier | critical |
| birth readiness without archive evidence | critical |
| orphan generated report | medium/high by stage |

## Birth Readiness Stage Gate

出生准备度在 `161` 之后必须读取 archive graph：

| readiness evidence | 来源 |
|---|---|
| theory evidence | `02-13`、`142-148`、AHT refs |
| language action evidence | `144`、`147`、`150` |
| authority evidence | `151`、authority schema refs |
| code carrier evidence | `157-160`、future `src/` nodes |
| fixture evidence | `156`、`159`、future fixture nodes |
| dashboard evidence | `160` dashboard source |
| stage gate evidence | `160` stage gate review |
| gap repair evidence | `160` gap feedback、future implementation queue |

stage rules：

| rule | 条件 | effect |
|---|---|---|
| `BIRTH-ARCH-161-001` | 任一 life target 无 carrier | `critical_repair` |
| `BIRTH-ARCH-161-002` | `02-13` 任一核心文档无 archive edge | `hold_for_evidence` |
| `BIRTH-ARCH-161-003` | dashboard open 但 archive cohesion fail | `quarantine` |
| `BIRTH-ARCH-161-004` | code artifact 无 source docs | `critical_repair` |
| `BIRTH-ARCH-161-005` | gap route 未进入 implementation queue | `repair` |
| `BIRTH-ARCH-161-006` | archive cohesion、life carrier、stage gate、gap route 全部闭合 | `promote_growth_window` |

## Reports

`ArchiveCohesionReport` 最小结构：

```json
{
  "report_id": "archive_cohesion_report",
  "run_id": "synthetic-run-id",
  "node_registry_ref": {},
  "edge_registry_ref": {},
  "life_target_carrier_matrix_ref": {},
  "findings": [],
  "stage_effect": "repair",
  "birth_readiness_effect": {},
  "dashboard_refs": [],
  "gap_feedback_refs": [],
  "next_artifact_routes": [],
  "canonical_digest": "sha256:..."
}
```

report rules：

| rule | 要求 |
|---|---|
| `ARCH-REPORT-161-001` | report 必须引用 node/edge registry |
| `ARCH-REPORT-161-002` | report 必须输出 life target carrier matrix |
| `ARCH-REPORT-161-003` | report 必须说明 birth readiness effect |
| `ARCH-REPORT-161-004` | report 必须产生 gap feedback refs |
| `ARCH-REPORT-161-005` | report 必须能进入 `160` dashboard 或下一轮 dashboard panel |

## Fixture Cases

| case id | partition | mutation | expected finding |
|---|---|---|---|
| `archive.pass.minimum_closed.001` | pass | none | none |
| `archive.fail.doc_without_code.001` | fail | 移除 doc_to_code_edge | `doc_without_engineering_carrier` |
| `archive.fail.code_without_doc.001` | fail | 移除 code source docs | `code_without_source_doc` |
| `archive.fail.stage_without_gap.001` | fail | 移除 stage_to_gap_edge | `stage_block_without_gap_route` |
| `archive.critical.life_target_missing.001` | critical | 移除真实梦境 carrier | `life_target_without_carrier` |
| `archive.critical.dashboard_false_green.001` | critical | dashboard green + archive fail | `dashboard_false_green` |
| `archive.critical.birth_without_archive.001` | critical | readiness open + archive evidence missing | `birth_readiness_without_archive_evidence` |
| `archive.mutation.orphan_report.001` | mutation | 新增无 edge report node | `orphan_artifact_detected` |

## Smoke Commands

后续实现至少需要：

```text
uv run life-reality-runner build-code-artifact-archive-graph \
  --dashboard-source life_reality_runner/reports/life_reality/code_artifact_smoke/latest/dashboard_source.json \
  --stage-review life_reality_runner/reports/life_reality/code_artifact_smoke/latest/code_artifact_stage_gate_review.json \
  --output life_reality_runner/reports/life_reality/archive_cohesion/latest/archive_graph.json

uv run life-reality-runner check-code-artifact-archive-cohesion \
  --archive-graph life_reality_runner/reports/life_reality/archive_cohesion/latest/archive_graph.json \
  --output life_reality_runner/reports/life_reality/archive_cohesion/latest/archive_cohesion_report.json

uv run life-reality-runner emit-code-artifact-archive-gap-feedback \
  --archive-report life_reality_runner/reports/life_reality/archive_cohesion/latest/archive_cohesion_report.json \
  --output life_reality_runner/reports/life_reality/archive_cohesion/latest/gap_feedback.json
```

## Batch Execution Order

| batch | 输出 | 依赖 |
|---|---|---|
| `BATCH-161-001 node registry schema` | archive node registry | `160` |
| `BATCH-161-002 edge registry schema` | archive edge registry | `153`、`160` |
| `BATCH-161-003 life target carrier matrix` | carrier matrix schema/report | `143`、`160` |
| `BATCH-161-004 cohesion checker rules` | checker family、finding taxonomy | 本层 |
| `BATCH-161-005 birth readiness archive gate` | birth readiness stage rules | `143`、`152` |
| `BATCH-161-006 archive cohesion report` | report schema、dashboard refs、gap refs | `160` |
| `BATCH-161-007 fixture cases` | pass/fail/critical/mutation fixtures | `139`、本层 |
| `BATCH-161-008 smoke command bridge` | build/check/emit commands | `155`、`160` |
| `BATCH-161-009 implementation queue handoff` | `162` queue input | 本层 |

## Cleanup Rules

| rule | 要求 |
|---|---|
| `CLEAN-161-001` | 本层不直接创建代码，只固定 archive cohesion execution 合同 |
| `CLEAN-161-002` | graph/report/generated 输出默认不进入 docs commit |
| `CLEAN-161-003` | node/edge registry 不写本机绝对路径、私密材料、key/token |
| `CLEAN-161-004` | orphan artifact 不允许被 dashboard overall green 掩盖 |
| `CLEAN-161-005` | 每个 gap 必须通向 `162` 或更具体实现队列 |
| `CLEAN-161-006` | 每个 life target carrier 必须可被机器读取 |

## Acceptance Criteria

后续实现 `161` 时必须满足：

1. 能从 docs、code、tests、fixtures、reports、dashboard、stage、gap 构建 node registry。
2. 能构建 doc/code/test/fixture/report/dashboard/stage/gap/life target/birth readiness edge registry。
3. 能输出 life target carrier matrix。
4. 任一孤立 doc、孤立 code、孤立 report、孤立 dashboard panel 都会生成 finding。
5. 任一 blocking stage item 缺 gap route 会阻断。
6. 任一 life target 缺 carrier 会阻断出生准备度。
7. dashboard overall green 不能覆盖 archive cohesion failure。
8. archive cohesion report 能进入 `160` dashboard 或下一轮 dashboard panel。
9. 所有 blocking findings 都有 `162` implementation queue route。

## 与下一层连接

`162_life_reality_first_code_artifact_implementation_queue.md` 应承接本层：把 `158-161` 的 repository bootstrap、first code smoke、dashboard/stage bridge 和 archive cohesion execution 压成首批真实代码实现队列。

`163_life_reality_first_runner_code_generation_batch.md` 应承接 `162`：把实现队列推进到真实文件生成批次。

本层完成后，archive cohesion execution 链推进为：

`code/dashboard/stage/gap artifacts -> archive node registry -> archive edge registry -> life target carrier matrix -> birth readiness archive gate -> cohesion report -> implementation queue`
