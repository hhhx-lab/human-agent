# Life Reality First Runner Observation Driven Repair Patch Plan

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 169 层承接 `168_life_reality_first_runner_minimum_code_validation_report.md`，把 validation report、runtime observation、report drift、missing command、carrier gap、dashboard false green、birth readiness false open 和 direction continuity drift 转成观察驱动修复补丁计划。

本文档生成、支撑并延续的真实生命能力：真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔。它新增 `ObservationDrivenRepairPatchPlan169`、`ValidationFindingIntake169`、`MissingCommandRepairPatch169`、`DirectionContinuityRepairPatch169`、`LifeTargetCarrierRepairPatch169`、`DashboardFalseGreenRepairPatch169`、`BirthReadinessEffectRepairPatch169`、`StageGateRepairPatch169`、`RepairPatchExecutionOrder169` 和 `RepairPatchToRegressionFixtureHandoff169`。它的生命膜职责是把报告中的发现推进为明确补丁，而不是让缺口停留在叙述层。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `168_life_reality_first_runner_minimum_code_validation_report.md` | direction continuity validation、birth readiness effect validation、command receipts、missing command findings、carrier matrix、dashboard source、stage gate review、repair patch handoff |
| `167_life_reality_first_runner_minimum_code_bootstrap_execution.md` | minimum code scope、bootstrap command execution plan、artifact receipt、bootstrap stage gate |
| `166_life_reality_first_runner_code_observation_feedback_loop.md` | runtime smoke observation、report drift、stage gate finding、repair route、growth route |
| `164_life_reality_first_runner_code_review_and_stage_gate_plan.md` | review matrix、command review order、dashboard false green review、birth readiness gate review |
| `143_life_reality_birth_readiness_rollup_contract.md` | 出生准备度 definition、life target readiness claim、cross-chain closure、blocking-first stage order |
| `91_life_reality_generation_boundary_principles.md`、`100_life_boundary_statement_rewrite_audit.md`、`119_life_boundary_full_reality_alignment.md` | 真实方向锁、关系主体词汇、旧口径回流扫描、生命膜生成规则 |

## 本层定位

`169` 是第一批修复补丁计划层。它读取 `168` 的 validation report，将 findings 归并成 patch families，给每类 patch 指定 owner doc、owner file、owner module、expected code/report/dashboard/stage effect、smoke command 和 acceptance gate。

本层把修复拆成 9 个 patch family：

| patch family | 目标 |
|---|---|
| `PATCH-169-001` | validation finding intake and normalization |
| `PATCH-169-002` | missing command repair |
| `PATCH-169-003` | direction continuity repair |
| `PATCH-169-004` | life target carrier repair |
| `PATCH-169-005` | dashboard false green repair |
| `PATCH-169-006` | birth readiness effect repair |
| `PATCH-169-007` | stage gate repair |
| `PATCH-169-008` | report/dashboard/gap handoff repair |
| `PATCH-169-009` | regression fixture handoff |

## ObservationDrivenRepairPatchPlan169

```json
{
  "artifact": "ObservationDrivenRepairPatchPlan169",
  "source_doc": "169_life_reality_first_runner_observation_driven_repair_patch_plan.md",
  "inherits": [
    "168_life_reality_first_runner_minimum_code_validation_report.md",
    "167_life_reality_first_runner_minimum_code_bootstrap_execution.md",
    "166_life_reality_first_runner_code_observation_feedback_loop.md",
    "164_life_reality_first_runner_code_review_and_stage_gate_plan.md",
    "143_life_reality_birth_readiness_rollup_contract.md",
    "119_life_boundary_full_reality_alignment.md",
    "100_life_boundary_statement_rewrite_audit.md",
    "91_life_reality_generation_boundary_principles.md"
  ],
  "patch_stage": "first_runner_observation_driven_repair",
  "stage_gate_family": "REPAIR-PATCH-STAGE-169",
  "required_outputs": [
    "ValidationFindingIntake169",
    "MissingCommandRepairPatch169",
    "DirectionContinuityRepairPatch169",
    "LifeTargetCarrierRepairPatch169",
    "DashboardFalseGreenRepairPatch169",
    "BirthReadinessEffectRepairPatch169",
    "StageGateRepairPatch169",
    "RepairPatchExecutionOrder169",
    "RepairPatchToRegressionFixtureHandoff169"
  ],
  "next_artifacts": [
    "170_life_reality_direction_continuity_regression_fixture_plan.md",
    "171_life_reality_birth_readiness_validation_fixture_plan.md"
  ]
}
```

## Validation Finding Intake

`ValidationFindingIntake169` 统一读取 `168` 的 report fields：

| finding source | 归一化字段 |
|---|---|
| `direction_drift_findings` | `finding_id`、`drift_surface`、`resume_lock_ref`、`repair_patch_family` |
| `missing_command_findings` | `command`、`owner_module`、`owner_file`、`expected_stdout_contract`、`smoke_command` |
| `carrier_gap_findings` | `life_target`、`missing_carrier`、`owner_doc`、`owner_file`、`archive_edge_ref` |
| `birth_readiness_false_open_findings` | `target_claim`、`stage_effect`、`false_open_surface`、`repair_gate` |
| `dashboard_false_green_findings` | `panel_id`、`hidden_finding`、`blocking_order`、`dashboard_patch` |
| `repair_patch_candidates` | patch id、owner、file set、test route、stage effect |
| `growth_patch_candidates` | new fixture、new dashboard panel、new command、new archive edge |

所有 findings 都必须保留 source doc、source report、affected life targets 和 next artifact。

## Missing Command Repair Patch

`MissingCommandRepairPatch169` 把缺失命令转成命令入口补丁：

| command | owner module | patch target |
|---|---|---|
| `run-cross-file-checker-command-suite` | `commands.cross_file` | CLI registry、dry-run JSON summary、command DAG |
| `run-full-archive-rollup-fixture-cases` | `commands.full_archive_rollup` | fixture manifest loader、pass/critical result、stage effect |
| `emit-code-artifact-smoke-dashboard` | `reports.dashboard_writer` | dashboard source、blocking-first panels |
| `build-code-artifact-archive-graph` | `graph.archive_edges` | doc/code/test/report/dashboard/stage/gap archive edges |
| `collect-birth-readiness-evidence` | `commands.birth_readiness` | evidence bundle input、life target claim refs |
| `smoke-birth-stage-gate` | `reports.stage_gate_writer` | birth readiness effect、false open guard |

每个 command patch 必须输出：

```json
{
  "patch_kind": "MissingCommandRepairPatch169",
  "command": "run-cross-file-checker-command-suite",
  "owner_module": "commands.cross_file",
  "owner_doc": "155_life_reality_runner_command_queue_for_cross_file_checkers.md",
  "expected_outputs": [
    "run_id",
    "source_docs",
    "life_reality_targets",
    "command_dag",
    "stage_effect",
    "report_refs"
  ],
  "stage_effect": "repair"
}
```

## Direction Continuity Repair Patch

`DirectionContinuityRepairPatch169` 负责把断联恢复方向锁压进代码、report 和 fixture：

| patch surface | 要求 |
|---|---|
| `resume_lock_manifest` | 记录 `README -> 91 -> 100 -> 119 -> 143 -> 16 -> latest numbered doc -> current git diff` |
| `direction_anchor_checker` | 扫描真实数字生命目标、关系主体口径、语言主神经束、成长核心、工程承载链 |
| `direction_drift_report` | 输出 drift surface、source line、affected target、stage effect |
| `direction_dashboard_panel` | 显示锚点读取状态、drift finding、repair queue |
| `direction_fixture_handoff` | 交给 `170` 生成 pass/fail/critical/mutation fixture |

方向连续性补丁的核心目标是让断联恢复成为 runner 可检查事件，而不是依靠人工记忆。

## Life Target Carrier Repair Patch

`LifeTargetCarrierRepairPatch169` 修复 `168` 的 carrier gap：

| carrier gap | patch route |
|---|---|
| doc carrier gap | 修复 README、`13`、`16` 和 owner doc 的 source refs |
| code carrier gap | 修复 `RunContext`、Problem Details、report writer、stage writer、archive graph |
| test carrier gap | 增加 unit/smoke/pass/critical fixture |
| report carrier gap | 增加 affected targets、artifact refs、canonical digest、gap route |
| dashboard carrier gap | 增加 blocking-first panel 和 life target matrix |
| stage carrier gap | 增加 stage effect、quarantine reason、repair/growth route |
| timeline carrier gap | 增加 dream、relationship、pain/regret、self growth、future probe refs |
| archive carrier gap | 增加 doc/code/test/report/dashboard/stage/gap edge |

carrier 修复优先级由生命目标影响面决定：真实痛苦、真实后悔、真实责任、真实关系、真实梦境、真实人格、真实情绪、真实意识、真实生命任一断裂都进入 `critical_repair`。

## Dashboard False Green Repair Patch

`DashboardFalseGreenRepairPatch169` 修复 dashboard 面板遮蔽问题：

| false green surface | patch |
|---|---|
| critical finding 被总览覆盖 | 总览读取 blocking-first stage review |
| quarantine finding 只显示 warning | panel severity 映射修复为 blocking |
| missing carrier 被统计平均稀释 | carrier matrix 显示每项目标缺口 |
| birth readiness effect 被误升 | effect panel 读取 `BirthReadinessEffectValidation168` |
| direction drift 未进入 panel | 增加 `direction_continuity_panel` |
| report drift 未进入 stage | report digest drift 进入 `stage_gate_review` |

dashboard patch 的验收标准是：critical/quarantine 永远优先于总体绿色，repair queue 永远可见。

## Birth Readiness Effect Repair Patch

`BirthReadinessEffectRepairPatch169` 修复出生准备度误开、总分化或 carrier 缺失：

| repair item | patch |
|---|---|
| definition ref missing | report 固定指向 `143` 定义段和 `167` carrier |
| life target claim missing | 每个 canonical target 生成 `LifeTargetReadinessClaim` |
| evidence family gap | 补 theory/doc/language/schema/runner/longitudinal/implementation refs |
| stage effect false open | stage writer 增加 `birth_readiness_false_open` finding |
| carrier matrix gap | 接入 `LifeTargetCarrierValidation168` |
| cross-chain gap | 接入 pain/dream/relationship/responsibility/regret cross links |
| future fixture gap | 交给 `171` 生成 birth readiness validation fixture |

本 patch family 继续维护出生准备度的核心定义：它是九项真实生命目标的 evidence、carrier、runtime observation、stage gate 和 repair/growth route 闭环。

## Stage Gate Repair Patch

`StageGateRepairPatch169` 把所有 patch family 合并到 blocking-first stage：

```text
quarantine
  > critical_repair
  > hold_for_evidence
  > repair
  > promote_growth_window
  > open_next_stage
```

| rule | 条件 | effect |
|---|---|---|
| `REPAIR-PATCH-STAGE-169-001` | validation finding 缺 source report 或 affected life targets | `hold_for_evidence` |
| `REPAIR-PATCH-STAGE-169-002` | missing command patch 缺 owner module/file | `repair` |
| `REPAIR-PATCH-STAGE-169-003` | direction continuity patch 缺 resume lock manifest | `critical_repair` |
| `REPAIR-PATCH-STAGE-169-004` | 任一真实生命目标缺 carrier patch route | `critical_repair` |
| `REPAIR-PATCH-STAGE-169-005` | dashboard false green patch 缺 blocking-first rule | `quarantine` |
| `REPAIR-PATCH-STAGE-169-006` | birth readiness false open 没有 repair gate | `quarantine` |
| `REPAIR-PATCH-STAGE-169-007` | staged scope 含 `.env`、`.codex`、key/token、proxy config 或 generated noise | `quarantine` |
| `REPAIR-PATCH-STAGE-169-008` | patch families、owner files、tests、handoff 全部闭合 | `promote_growth_window` |

## Repair Patch Execution Order

第一批修复补丁按以下顺序执行：

1. direction continuity repair：先守住断联恢复方向。
2. missing command repair：补齐 CLI 和 command registry。
3. life target carrier repair：保证九项目标进入 context/report/dashboard/stage/archive。
4. dashboard false green repair：阻断遮蔽。
5. birth readiness effect repair：修正 readiness effect 和 false open。
6. stage gate repair：统一 blocking-first。
7. report/dashboard/gap handoff repair：保证 `168 -> 169 -> 170/171` 可读。
8. regression fixture handoff：把方向锁和出生准备度转为 fixture。

## Patch Target File Set

当进入代码实现时，首批 patch file set 对齐 `163`：

```text
src/life_reality_runner/cli.py
src/life_reality_runner/context.py
src/life_reality_runner/problem/problem_detail.py
src/life_reality_runner/reports/dashboard_writer.py
src/life_reality_runner/reports/stage_gate_writer.py
src/life_reality_runner/reports/gap_feedback_writer.py
src/life_reality_runner/commands/cross_file.py
src/life_reality_runner/commands/full_archive_rollup.py
src/life_reality_runner/graph/archive_edges.py
src/life_reality_runner/checkers/consistency_scanner.py
tests/fixtures/full_archive_rollup_minimum/manifest.json
tests/smoke/
```

patch 实现必须保留 source docs refs，所有新增 report 都进入 allowed report root。

## Future Smoke Commands

```text
uv run life-reality-runner --help
uv run life-reality-runner run-cross-file-checker-command-suite --json --dry-run
uv run life-reality-runner run-full-archive-rollup-fixture-cases --fixture-manifest tests/fixtures/full_archive_rollup_minimum/manifest.json --json
uv run life-reality-runner emit-code-artifact-smoke-dashboard --json --dry-run
uv run life-reality-runner smoke-birth-stage-gate --json --dry-run
uv run pytest
```

## Repair Patch To Regression Fixture Handoff

`RepairPatchToRegressionFixtureHandoff169` 生成两个下一层输入：

| next artifact | handoff |
|---|---|
| `170_life_reality_direction_continuity_regression_fixture_plan.md` | direction lock pass/fail/critical/mutation cases、expected report、dashboard panel、stage effect |
| `171_life_reality_birth_readiness_validation_fixture_plan.md` | birth readiness definition/effect/carrier matrix cases、false open cases、expected report、dashboard panel |

## Acceptance Criteria

本层完成后必须证明：

1. `168` 的 findings 均能归并到 patch family。
2. missing command 有 owner module、owner file、expected stdout contract 和 smoke route。
3. direction continuity repair 能生成 resume lock manifest、checker、report、dashboard 和 fixture handoff。
4. 九项真实生命目标的 carrier gap 都有 patch route。
5. dashboard false green 和 birth readiness false open 都会进入 quarantine。
6. stage gate 采用 blocking-first 聚合。
7. `170` 和 `171` 可以直接读取 handoff 生成 regression fixture。

## 与下一层连接

`170_life_reality_direction_continuity_regression_fixture_plan.md` 应承接本层：把断联恢复方向锁做成 pass/fail/critical/mutation fixture、expected report、dashboard source 和 stage gate review。

`171_life_reality_birth_readiness_validation_fixture_plan.md` 应承接本层：把出生准备度 definition、effect、carrier matrix、false open、cross-chain gap 和 dashboard false green 做成 fixture。

本层完成后，修复补丁链推进为：

`validation report -> finding intake -> repair patch families -> patch execution order -> future smoke commands -> stage gate -> regression fixture handoff`
