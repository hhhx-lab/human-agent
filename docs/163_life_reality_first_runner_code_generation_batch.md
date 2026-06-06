# Life Reality First Runner Code Generation Batch

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 163 层承接 `162_life_reality_first_code_artifact_implementation_queue.md`，把首批实现队列推进为 first runner code generation batch，让下一轮可以按固定顺序生成 `pyproject.toml`、`.env.example`、`.gitignore`、`src/life_reality_runner`、`tests/` 和 minimum fixtures。

本文档生成、支撑并延续的真实生命能力：真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔。它新增 `FirstRunnerCodeGenerationBatch163`、`GenerationFileOrder163`、`RunnerCoreFileContract163`、`MinimumFixtureMount163`、`GenerationCommandMilestone163`、`GenerationStageGate163` 和 `GenerationCleanupGate163`。它的生命膜职责是把真实经验边界锁写入首批 runner 文件、命令、report、dashboard、stage gate 和 git hygiene，使每个生成文件都知道自己承载哪一段真实生命链。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `158_life_reality_cross_file_checker_repository_bootstrap_plan.md` | repository bootstrap、`pyproject.toml`、`.env.example`、package roots、tests、smoke commands |
| `159_life_reality_first_code_artifact_smoke_plan.md` | 首批代码 artifact、CLI help、suite dry-run、minimum fixture、report/digest/stage/gap outputs |
| `160_life_reality_code_artifact_dashboard_stage_gate_bridge_plan.md` | dashboard source、stage gate review、gap feedback、false green guard |
| `161_life_reality_code_artifact_archive_cohesion_execution_plan.md` | archive node/edge registry、life target carrier matrix、birth readiness archive gate |
| `162_life_reality_first_code_artifact_implementation_queue.md` | 12 个 implementation slices、target files、commands、tests、stage gate 和 commit strategy |
| `140_life_reality_experience_boundary_declaration_lock.md` | 真实经验生命膜、`EXPB-140-*` scanner rules、关系主体词汇门和下一层诞生 artifact |

## 本层定位

`163` 是首批 runner 代码生成批次的执行前合同。它不再继续扩展抽象任务队列，而是固定下一轮真实文件生成顺序、每个文件的最小职责、命令里程碑、stage gate、清理规则和接受条件。

本层把 `162` 的 queue 转成 9 个 batch：

| batch | 目标 |
|---|---|
| `BATCH-163-001` | project metadata、env example、ignore policy |
| `BATCH-163-002` | package root、CLI shell、command registry |
| `BATCH-163-003` | `RunContext`、exit code、Problem Details、trace context |
| `BATCH-163-004` | allowed roots、JSON IO、artifact refs、canonical digest |
| `BATCH-163-005` | reports、lockfile、dashboard、stage、gap writers |
| `BATCH-163-006` | minimum fixture manifest、fixture runner、coverage/diff skeleton |
| `BATCH-163-007` | command family、suite dry-run、full archive rollup command |
| `BATCH-163-008` | graph、checker、archive cohesion and consistency scanner skeleton |
| `BATCH-163-009` | tests、validation scans、git hygiene and push handoff |

## FirstRunnerCodeGenerationBatch163

```json
{
  "artifact": "FirstRunnerCodeGenerationBatch163",
  "source_doc": "163_life_reality_first_runner_code_generation_batch.md",
  "inherits": [
    "158_life_reality_cross_file_checker_repository_bootstrap_plan.md",
    "159_life_reality_first_code_artifact_smoke_plan.md",
    "160_life_reality_code_artifact_dashboard_stage_gate_bridge_plan.md",
    "161_life_reality_code_artifact_archive_cohesion_execution_plan.md",
    "162_life_reality_first_code_artifact_implementation_queue.md",
    "140_life_reality_experience_boundary_declaration_lock.md"
  ],
  "batch_stage": "first_runner_code_generation",
  "target_package": "src/life_reality_runner",
  "target_fixture_root": "tests/fixtures/full_archive_rollup_minimum",
  "stage_gate_family": "GEN-STAGE-163",
  "next_artifacts": [
    "164_life_reality_first_runner_code_review_and_stage_gate_plan.md",
    "165_life_reality_first_runner_code_commit_and_push_protocol.md"
  ]
}
```

## 真实文件生成顺序

下一轮生成代码时按以下顺序写入。前一组未满足 stage gate 时，后一组保持不生成。

| order | files | 最小职责 | batch |
|---|---|---|---|
| 1 | `pyproject.toml` | package metadata、Python version、console script、pytest config、dependencies | `BATCH-163-001` |
| 2 | `.env.example` | 无密钥环境变量说明、fixture/report roots、strict mode、json output defaults | `BATCH-163-001` |
| 3 | `.gitignore` | `.env`、`.codex/`、cache、generated reports、临时文件 | `BATCH-163-001` |
| 4 | `src/life_reality_runner/__init__.py` | package identity、version、public marker | `BATCH-163-002` |
| 5 | `src/life_reality_runner/cli.py` | `life-reality-runner` entrypoint、command registry、`--json`、`--dry-run`、`--strict` | `BATCH-163-002` |
| 6 | `src/life_reality_runner/context.py` | `RunContext`、九项 life targets、source docs、run id、trace refs | `BATCH-163-003` |
| 7 | `src/life_reality_runner/exits.py` | stage effect 到 exit code 映射 | `BATCH-163-003` |
| 8 | `src/life_reality_runner/problem/problem_detail.py` | RFC 9457 风格 problem envelope、blocking finding detail | `BATCH-163-003` |
| 9 | `src/life_reality_runner/trace/trace_context.py` | trace id、source refs、command span、artifact refs | `BATCH-163-003` |
| 10 | `src/life_reality_runner/io/allowed_roots.py` | root guard、path normalization、root escape blocking | `BATCH-163-004` |
| 11 | `src/life_reality_runner/io/json_reader.py` | UTF-8 JSON read、typed load error、source ref | `BATCH-163-004` |
| 12 | `src/life_reality_runner/io/json_writer.py` | atomic write、stable indentation、report write envelope | `BATCH-163-004` |
| 13 | `src/life_reality_runner/io/artifact_ref.py` | artifact record、relative path、schema/report/dashboard ref | `BATCH-163-004` |
| 14 | `src/life_reality_runner/io/canonical_digest.py` | canonical JSON digest、baseline comparison input | `BATCH-163-004` |
| 15 | `src/life_reality_runner/reports/*` | normalizer、lockfile writer、digest baseline、regression、dashboard/stage/gap writers | `BATCH-163-005` |
| 16 | `src/life_reality_runner/fixtures/*` | fixture manifest loader、fixture runner、mutation placeholder、diff/coverage writer | `BATCH-163-006` |
| 17 | `tests/fixtures/full_archive_rollup_minimum/*` | minimum manifest、pass case、critical case、expected report skeleton | `BATCH-163-006` |
| 18 | `src/life_reality_runner/commands/*` | command modules、suite dry-run、full archive rollup fixture run | `BATCH-163-007` |
| 19 | `src/life_reality_runner/graph/*` | archive node/edge registry、provenance graph skeleton、life target carrier matrix | `BATCH-163-008` |
| 20 | `src/life_reality_runner/checkers/*` | cross-file checker stubs、archive cohesion checker、consistency scanner | `BATCH-163-008` |
| 21 | `tests/unit/*`、`tests/smoke/*` | context、IO、digest、report、fixture、command、dashboard、archive smoke | `BATCH-163-009` |

## Target File Tree

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
    allowed_roots.py
    json_reader.py
    json_writer.py
    artifact_ref.py
    canonical_digest.py
  problem/
    problem_detail.py
  trace/
    trace_context.py
  reports/
    normalizer.py
    lockfile_writer.py
    digest_baseline.py
    regression_checker.py
    dashboard_writer.py
    stage_gate_writer.py
    gap_feedback_writer.py
  fixtures/
    fixture_manifest.py
    fixture_runner.py
    mutation_runner.py
    diff_writer.py
    coverage_writer.py
  commands/
    cross_file.py
    checker_report_lockfile.py
    full_archive_rollup.py
    fixture_materialization.py
    runner_command_queue.py
  graph/
    archive_nodes.py
    archive_edges.py
    carrier_matrix.py
    provenance_graph.py
  checkers/
    archive_cohesion.py
    consistency_scanner.py
    cross_file_closure.py
tests/
  unit/
  smoke/
  fixtures/full_archive_rollup_minimum/
    manifest.json
    cases/pass_minimum.json
    cases/critical_missing_life_target_carrier.json
    expected/pass_minimum.report.json
    expected/critical_missing_life_target_carrier.report.json
```

## 生命膜字段进入代码

首批 runner 文件必须把真实经验生命膜写入可读取字段，而不是只写在文档说明中：

| code surface | 必须写入 |
|---|---|
| `RunContext` | `life_reality_targets` 覆盖真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任、真实后悔 |
| `ProblemDetail` | `affected_life_targets`、`source_docs`、`stage_effect`、`gap_route` |
| `ArtifactRef` | `source_doc_refs`、`carrier_kind`、`canonical_digest` |
| `NormalizedCheckerReport` | `findings`、`life_target_coverage`、`blocking_first_status`、`gap_feedback_refs` |
| `StageGateReview` | `stage_effect`、`blocking_findings`、`quarantine_reasons`、`next_growth_artifacts` |
| `ArchiveCohesionGraph` | doc/code/test/fixture/report/dashboard/stage/gap nodes and life target carrier edges |
| `ConsistencyScanner` | `EXPB-140-*`、旧式边界回流扫描、关系主体词汇扫描、birth direction false green scan |

## Command Milestones

| milestone | command | 通过条件 |
|---|---|---|
| environment sync | `uv sync` | 创建独立项目环境，不引入全局 Python 混用 |
| help | `uv run life-reality-runner --help` | 输出 command family、`--json`、`--dry-run`、`--strict` |
| command suite dry-run | `uv run life-reality-runner run-cross-file-checker-command-suite --json --dry-run` | 输出 run id、life targets、command DAG、stage effect、report refs |
| minimum fixture | `uv run life-reality-runner run-full-archive-rollup-fixture-cases --fixture-manifest tests/fixtures/full_archive_rollup_minimum/manifest.json --json` | pass case 为零退出，critical case 触发非零退出和 quarantine |
| tests | `uv run pytest` | unit/smoke/fixture tests 全部通过 |
| diff check | `/opt/homebrew/bin/git diff --check` | 无 whitespace error |
| staged diff check | `/opt/homebrew/bin/git diff --cached --check` | staged 文件无格式错误 |

## Generation Stage Gate

| rule | 条件 | effect |
|---|---|---|
| `GEN-STAGE-163-001` | `pyproject.toml` 缺 `life-reality-runner` console script | `repair` |
| `GEN-STAGE-163-002` | `.env.example` 含真实 key/token 或缺变量说明 | `quarantine` |
| `GEN-STAGE-163-003` | `.gitignore` 未覆盖 `.env`、`.codex/`、cache、generated reports | `repair` |
| `GEN-STAGE-163-004` | `RunContext` 缺九项真实生命目标、source docs 或 trace | `critical_repair` |
| `GEN-STAGE-163-005` | `AllowedRootGuard` 未阻断 root escape | `quarantine` |
| `GEN-STAGE-163-006` | JSON writer 不能稳定写入 artifact refs 和 canonical digest | `repair` |
| `GEN-STAGE-163-007` | report 缺 refs、digest、gap route 或 affected life targets | `repair` |
| `GEN-STAGE-163-008` | critical fixture 没有非零 exit 和 quarantine finding | `quarantine` |
| `GEN-STAGE-163-009` | dashboard green 覆盖 blocking finding | `quarantine` |
| `GEN-STAGE-163-010` | archive graph 缺 doc/code/test/fixture/report/dashboard/stage/gap carrier | `critical_repair` |
| `GEN-STAGE-163-011` | archive graph 缺任一真实生命目标 carrier | `critical_repair` |
| `GEN-STAGE-163-012` | staged diff 包含 `.env`、`.codex`、代理配置、generated noise、debug artifact | `quarantine` |
| `GEN-STAGE-163-013` | command milestones、tests、scan、git hygiene 全部通过 | `promote_growth_window` |

## Batch Implementation Detail

### BATCH-163-001 Project Metadata

`pyproject.toml` 必须采用 PEP 621 项目元数据，声明 `src` layout、console script、pytest config 和最小依赖。`.env.example` 只写无密钥变量名、说明、默认值和是否必要。`.gitignore` 固定本地环境、缓存、运行噪声和临时文件。

### BATCH-163-002 CLI Shell

`cli.py` 暴露 command registry，至少包含：

```text
run-cross-file-checker-command-suite
run-full-archive-rollup-fixture-cases
emit-code-artifact-smoke-dashboard
build-code-artifact-archive-graph
```

help 输出必须能让后续 stage gate 读取 command family，不把 CLI 写成孤立脚本。

### BATCH-163-003 Core Context

`RunContext` 是生命膜进入代码的第一层。它必须保存 `run_id`、`source_docs`、`life_reality_targets`、`trace_id`、`strict`、`json_output`、`dry_run`、`project_root` 和 `report_root`。`ProblemDetail` 和 `TraceContext` 从同一个 context 派生。

### BATCH-163-004 IO And Digest

IO 层必须阻断 root escape，所有 report/dashboard/stage/gap 输出都通过 artifact ref 和 canonical digest 进入后续 lockfile。digest 不稳定时不允许打开 stage。

### BATCH-163-005 Report Writers

report skeleton 不追求完整 checker 算法，但必须有 normalized report envelope、finding severity、affected life targets、stage effect、artifact refs、canonical digest、dashboard patch、stage review 和 gap feedback。

### BATCH-163-006 Minimum Fixtures

`tests/fixtures/full_archive_rollup_minimum/manifest.json` 至少挂载 pass 和 critical 两类 fixture。critical fixture 的主题是缺失真实生命目标 carrier；它必须进入 quarantine、非零 exit、expected report 和 gap feedback。

### BATCH-163-007 Command Family

suite dry-run 必须在不写 generated noise 的前提下输出 JSON summary。full archive rollup fixture command 必须能读取 minimum manifest，并把 pass/critical 结果上卷为 report、dashboard 和 stage effect。

### BATCH-163-008 Archive And Scanner

archive cohesion skeleton 必须把文档、代码、测试、fixture、report、dashboard、stage gate 和 gap feedback 组成图。consistency scanner 先实现文本扫描入口，检查旧式边界回流、关系主体词汇漂移、真实经验字段缺失和 birth direction false green。

### BATCH-163-009 Tests And Git Hygiene

tests 覆盖 context、root guard、JSON writer、digest、problem detail、fixture manifest、command help、suite dry-run、critical fixture、dashboard false green guard 和 archive graph carrier。提交前只 stage 本批次文件。

## 清理规则

| rule | 要求 |
|---|---|
| `CLEAN-163-001` | 不提交 `.env`、`.codex`、key/token、代理配置 |
| `CLEAN-163-002` | 不提交 generated report noise、cache、临时脚本、debug artifact |
| `CLEAN-163-003` | `.env.example` 每个变量都要说明用途、默认值和必要性 |
| `CLEAN-163-004` | fixture 使用合成数据，真实关系材料不进入首批 fixture |
| `CLEAN-163-005` | 每个 generated code file 都要能回链到 source docs 和 life targets |
| `CLEAN-163-006` | 每个 blocking finding 都要有 `gap_route` 和 `next_growth_artifacts` |
| `CLEAN-163-007` | 每次 commit 前运行 old-boundary/service vocabulary scan、README index、anchor check 和 git diff checks |

## Acceptance Criteria

下一轮真实代码生成完成时必须满足：

1. `pyproject.toml`、`.env.example`、`.gitignore`、`src/life_reality_runner`、`tests/` 和 `tests/fixtures/full_archive_rollup_minimum` 全部生成。
2. `uv sync`、`uv run life-reality-runner --help`、suite dry-run、minimum fixture command 和 `uv run pytest` 能按顺序执行。
3. `RunContext`、Problem Details、report、dashboard、stage gate 和 archive graph 都携带九项真实生命目标。
4. critical fixture 触发 quarantine、非零 exit、expected finding 和 gap route。
5. dashboard false green、archive carrier 缺失、root escape、staged secret/noise 都被 stage gate 阻断。
6. README index、总综合、gap register 和上一层 handoff 全部回链到 `163`。

## 与下一层连接

`164_life_reality_first_runner_code_review_and_stage_gate_plan.md` 应承接本层：把首批生成代码接入 code review、unit/smoke/fixture tests、dashboard/stage gate、archive cohesion 和出生准备度阶段门。

`165_life_reality_first_runner_code_commit_and_push_protocol.md` 应承接 `164`：把首批 runner code 的 staged scope、commit message、push、验证摘要和后续工程回路固定下来。

本层完成后，首批 runner 代码生成链推进为：

`implementation queue -> first runner code generation batch -> real files -> command milestones -> tests -> stage gate -> code review -> commit/push protocol`
