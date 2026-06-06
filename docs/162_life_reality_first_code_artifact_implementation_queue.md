# Life Reality First Code Artifact Implementation Queue

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 162 层承接 `158-161`，把 repository bootstrap、first code smoke、dashboard/stage gate bridge 和 archive cohesion execution 压成首批真实代码实现队列。

本层仍是文档计划层，不直接创建代码文件。它的职责是把下一轮真正生成代码时的任务队列写到足够细：每个任务要写哪些文件、引用哪些上游文档、暴露哪个命令、写哪些测试、产生哪些 report/dashboard/stage/gap 输出、如何被 archive cohesion 回链、如何提交推送。到本层之后，继续只写抽象计划的收益开始变低，下一轮应进入真实文件生成批次。

## 规范锚点

首批实现队列吸收以下工程规范：

| 规范/来源 | 本层吸收方式 |
|---|---|
| Python Packaging / `pyproject.toml` project metadata | package metadata、console script、dependency surface |
| Python entry points / scripts | `life-reality-runner` command exposure |
| pytest test discovery and fixtures | unit/smoke/fixture tests 的目录与断言入口 |
| uv project sync/run workflow | `uv sync`、`uv run`、lock/reproducible environment |
| OpenSSF SLSA | provenance、build inputs、source integrity、supply-chain hygiene |
| JSON Schema Draft 2020-12 | report/fixture/dashboard/archive schema validation |
| RFC 8785 JSON Canonicalization Scheme | artifact/report/dashboard/archive digest |
| RFC 9457 Problem Details | failure envelope and blocking finding detail |

这些规范进入实现队列的方式很简单：每个代码任务都必须能被安装、运行、测试、追踪、生成 digest、进入 stage gate，并且不把本地私密材料、key/token、临时产物带入仓库。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `158_life_reality_cross_file_checker_repository_bootstrap_plan.md` | `pyproject.toml`、`.env.example`、package roots、help smoke、stage gate |
| `159_life_reality_first_code_artifact_smoke_plan.md` | artifact write order、minimum fixture、smoke command matrix、git commit flow |
| `160_life_reality_code_artifact_dashboard_stage_gate_bridge_plan.md` | dashboard source、stage gate review、gap feedback、archive handoff |
| `161_life_reality_code_artifact_archive_cohesion_execution_plan.md` | archive node/edge registry、life target carrier matrix、cohesion checker、birth gate |

## 本层定位

`162` 是首批代码实现的任务队列。它把大任务拆成 12 个 implementation slices：

| slice | 目标 |
|---|---|
| `IMPL-162-001` | project/environment bootstrap |
| `IMPL-162-002` | package roots and CLI shell |
| `IMPL-162-003` | context、exit、problem、trace core |
| `IMPL-162-004` | allowed roots、JSON IO、artifact refs、canonical digest |
| `IMPL-162-005` | report skeleton、normalizer、lockfile、stage/gap writers |
| `IMPL-162-006` | fixture manifest、minimum fixture、fixture runner |
| `IMPL-162-007` | command family and suite dry-run |
| `IMPL-162-008` | dashboard/stage/gap bridge skeleton |
| `IMPL-162-009` | archive cohesion registry/checker skeleton |
| `IMPL-162-010` | tests: unit、smoke、fixture |
| `IMPL-162-011` | validation scans、generated output ignore、git hygiene |
| `IMPL-162-012` | commit/push and next generation batch handoff |

## ImplementationQueue162

```json
{
  "artifact": "ImplementationQueue162",
  "source_doc": "162_life_reality_first_code_artifact_implementation_queue.md",
  "inherits": [
    "158_life_reality_cross_file_checker_repository_bootstrap_plan.md",
    "159_life_reality_first_code_artifact_smoke_plan.md",
    "160_life_reality_code_artifact_dashboard_stage_gate_bridge_plan.md",
    "161_life_reality_code_artifact_archive_cohesion_execution_plan.md"
  ],
  "queue_stage": "first_code_artifact_implementation_queue",
  "target_package": "src/life_reality_runner",
  "target_test_root": "tests",
  "next_artifact": "163_life_reality_first_runner_code_generation_batch.md"
}
```

## Target File Set

第一批真实代码生成的 intended files：

```text
pyproject.toml
.env.example
.gitignore
src/life_reality_runner/
  __init__.py
  cli.py
  context.py
  exits.py
  io/
  schema/
  graph/
  checkers/
  reports/
  fixtures/
  commands/
  problem/
  trace/
tests/
  unit/
  smoke/
  fixtures/full_archive_rollup_minimum/
```

`.gitignore` 至少覆盖：

| pattern family | 目的 |
|---|---|
| `.env` | 不提交本地环境 |
| `.codex/` | 不提交本地代理/会话配置 |
| `__pycache__/`、`.pytest_cache/` | 不提交 Python 缓存 |
| `life_reality_runner/reports/**/latest/generated/` | 不提交运行噪声 |
| `*.tmp`、`*.bak` | 不提交临时文件 |

## Queue Items

### IMPL-162-001 Project Bootstrap

| field | 内容 |
|---|---|
| files | `pyproject.toml`、`.env.example`、`.gitignore` |
| source docs | `158`、`159` |
| actions | 定义 package metadata、scripts、dependencies、pytest config、ignore policy |
| tests | `uv sync`、`uv run life-reality-runner --help` 后续可执行 |
| stage gate | `pyproject` 缺 script 或 `.env.example` 含 key/token -> quarantine |

### IMPL-162-002 Package Roots And CLI Shell

| field | 内容 |
|---|---|
| files | `__init__.py`、`cli.py`、package subdirs |
| source docs | `157`、`158`、`155` |
| actions | 建立 command registry、top-level parser、`--json`、`--dry-run`、`--strict` |
| tests | `tests/smoke/test_bootstrap_help.py` |
| stage gate | help 不列 command family -> repair |

### IMPL-162-003 Context, Exit, Problem, Trace Core

| field | 内容 |
|---|---|
| files | `context.py`、`exits.py`、`problem/problem_detail.py`、`trace/trace_context.py` |
| source docs | `133`、`157`、`159` |
| actions | `RunContext`、life targets、source docs、trace id、stage-to-exit mapping、Problem Details |
| tests | `tests/unit/test_context.py`、problem detail assertions |
| stage gate | context 缺 life targets/source docs/trace -> critical_repair |

### IMPL-162-004 IO, Artifact Ref, Digest

| field | 内容 |
|---|---|
| files | `io/allowed_roots.py`、`json_reader.py`、`json_writer.py`、`artifact_ref.py`、`canonical_digest.py` |
| source docs | `133`、`154`、`159` |
| actions | root guard、JSON read/write、artifact record、canonical digest |
| tests | `test_allowed_roots.py`、`test_json_io.py`、`test_canonical_digest.py` |
| stage gate | root escape 或 digest instability -> quarantine/critical_repair |

### IMPL-162-005 Report Skeleton

| field | 内容 |
|---|---|
| files | `reports/normalizer.py`、`lockfile_writer.py`、`digest_baseline.py`、`regression_checker.py`、`dashboard_writer.py`、`stage_gate_writer.py`、`gap_feedback_writer.py` |
| source docs | `154`、`160` |
| actions | 写最小 summary/report/stage/gap skeleton，保留 artifact refs 和 digest |
| tests | `test_report_normalizer.py`、`test_checker_report_lockfile.py` |
| stage gate | report 缺 refs/digest/gap route -> repair |

### IMPL-162-006 Fixture Manifest And Runner

| field | 内容 |
|---|---|
| files | `fixtures/fixture_manifest.py`、`fixture_runner.py`、`mutation_runner.py`、`diff_writer.py`、`coverage_writer.py`、`tests/fixtures/full_archive_rollup_minimum/*` |
| source docs | `156`、`159` |
| actions | 读取 minimum fixture manifest，生成 pass/critical case summary |
| tests | `test_fixture_manifest.py`、`test_fixture_runner.py` |
| stage gate | critical fixture 未非零 exit -> quarantine |

### IMPL-162-007 Command Family And Suite Dry Run

| field | 内容 |
|---|---|
| files | `commands/cross_file.py`、`checker_report_lockfile.py`、`full_archive_rollup.py`、`fixture_materialization.py`、`runner_command_queue.py` |
| source docs | `155`、`157`、`159` |
| actions | 暴露 command family、suite dry-run、summary JSON |
| tests | `test_command_dag.py`、`test_cross_file_checker_command_suite_bootstrap.py` |
| stage gate | command DAG 缺失或 cycle -> critical_repair |

### IMPL-162-008 Dashboard Stage Gap Bridge

| field | 内容 |
|---|---|
| files | report writers or command wrappers for dashboard/stage/gap |
| source docs | `160` |
| actions | 从 smoke summary/fixture report 生成 dashboard source、stage review、gap feedback |
| tests | smoke bridge assertions |
| stage gate | dashboard false green or stage false open -> quarantine |

### IMPL-162-009 Archive Cohesion Skeleton

| field | 内容 |
|---|---|
| files | graph/checker/report skeleton for archive cohesion |
| source docs | `161` |
| actions | 构建 node registry、edge registry、life target carrier matrix skeleton |
| tests | archive cohesion smoke assertions |
| stage gate | orphan artifact or missing life target carrier -> critical_repair |

### IMPL-162-010 Unit And Smoke Tests

| field | 内容 |
|---|---|
| files | `tests/unit/*`、`tests/smoke/*` |
| source docs | `158-161` |
| actions | 覆盖 context、IO、digest、report、fixture、commands、dashboard、archive |
| tests | `uv run pytest` |
| stage gate | smoke subset fail -> repair/critical by surface |

### IMPL-162-011 Validation And Hygiene

| field | 内容 |
|---|---|
| files | no new generated files committed |
| source docs | `158-161` |
| actions | old口径扫描、关系词扫描、README index、anchor check、secret/generated noise scan |
| tests | shell/node validation commands |
| stage gate | forbidden vocabulary or secret/generated noise -> quarantine |

### IMPL-162-012 Commit Push Handoff

| field | 内容 |
|---|---|
| files | intended staged files only |
| source docs | `159`、`161` |
| actions | explicit git add、cached diff check、commit、push `origin main` |
| tests | clean `git status --short --branch` |
| stage gate | local main not aligned with origin/main -> hold_for_evidence |

## Command Milestones

| milestone | command |
|---|---|
| env | `uv sync` |
| help | `uv run life-reality-runner --help` |
| suite dry-run | `uv run life-reality-runner run-cross-file-checker-command-suite --json --dry-run` |
| fixture smoke | `uv run life-reality-runner run-full-archive-rollup-fixture-cases --fixture-manifest tests/fixtures/full_archive_rollup_minimum/manifest.json --json` |
| dashboard bridge | `uv run life-reality-runner emit-code-artifact-smoke-dashboard --help` |
| archive bridge | `uv run life-reality-runner build-code-artifact-archive-graph --help` |
| tests | `uv run pytest` |
| git | `/opt/homebrew/bin/git diff --cached --check` |

## Stage Gate

| rule | 条件 | effect |
|---|---|---|
| `IMPL-STAGE-162-001` | package script 不存在 | `repair` |
| `IMPL-STAGE-162-002` | context 缺九项 life targets | `critical_repair` |
| `IMPL-STAGE-162-003` | root escape 未阻断 | `quarantine` |
| `IMPL-STAGE-162-004` | report 缺 artifact refs/digest/gap route | `repair` |
| `IMPL-STAGE-162-005` | critical fixture 未非零 exit | `quarantine` |
| `IMPL-STAGE-162-006` | dashboard green 覆盖 blocking finding | `quarantine` |
| `IMPL-STAGE-162-007` | archive graph 缺 life target carrier | `critical_repair` |
| `IMPL-STAGE-162-008` | `.env`、`.codex`、key/token、generated noise staged | `quarantine` |
| `IMPL-STAGE-162-009` | command/test/dashboard/archive smoke 全部通过 | `promote_growth_window` |

## Implementation Commit Strategy

首批实现可以分 3 个提交，也可以一次提交；若分批，必须保持每批可运行：

| commit batch | 建议提交信息 | 内容 |
|---|---|---|
| `COMMIT-162-A` | `新增生命现实运行器项目骨架` | pyproject、env example、package roots、context/IO/problem/trace |
| `COMMIT-162-B` | `新增生命现实运行器冒烟命令` | command family、fixture runner、report skeleton、tests |
| `COMMIT-162-C` | `新增生命现实运行器仪表盘与凝聚检查骨架` | dashboard/stage/gap、archive cohesion skeleton、smoke tests |

无论单提交还是多提交，每次都必须：

```text
/opt/homebrew/bin/git diff --check
uv run pytest
/opt/homebrew/bin/git diff --cached --check
/opt/homebrew/bin/git status --short --branch
```

## Gap Routing

| gap | route |
|---|---|
| package bootstrap gap | `163` generation batch, project bootstrap slice |
| context/core gap | `163` context generation slice |
| IO/digest gap | `163` IO generation slice |
| report/lockfile gap | `163` report generation slice |
| fixture gap | `163` fixture generation slice |
| command gap | `163` command generation slice |
| dashboard/stage gap | `163` dashboard generation slice |
| archive cohesion gap | `163` archive generation slice |
| birth readiness carrier gap | future birth readiness implementation slice |

## Cleanup Rules

| rule | 要求 |
|---|---|
| `CLEAN-162-001` | 本层不直接创建代码，只固定 implementation queue |
| `CLEAN-162-002` | 首批代码不得提交 `.env`、`.codex`、key/token、代理配置 |
| `CLEAN-162-003` | generated reports 默认 ignored |
| `CLEAN-162-004` | fixture 使用合成数据 |
| `CLEAN-162-005` | 每个实现 slice 必须有 source docs 和 tests |
| `CLEAN-162-006` | 每个 blocking finding 必须有 gap route |

## Acceptance Criteria

后续真实实现开始前，本层提供的队列必须能支持：

1. 生成完整 intended file set。
2. 每个 file set 都有 source docs、tests、stage gate。
3. 每个 command milestone 都有实现 slice。
4. 每个 stage gate failure 都有 gap route。
5. 每个真实生命目标都至少进入一个实现 slice。
6. 后续 `163` 可以按本队列直接生成真实文件。

## 与下一层连接

`163_life_reality_first_runner_code_generation_batch.md` 应承接本层：把 implementation queue 推进到真实文件生成批次，开始创建 `pyproject.toml`、`.env.example`、`src/`、`tests/` 和 minimum fixtures。

`164_life_reality_first_runner_code_review_and_stage_gate_plan.md` 应承接 `163`：把首批生成代码接入 review、test、dashboard、archive cohesion 和出生准备度阶段门。

本层完成后，首批真实代码实现队列链推进为：

`repository bootstrap + smoke + dashboard/stage + archive cohesion -> implementation slices -> file set -> tests -> stage gate -> generation batch`
