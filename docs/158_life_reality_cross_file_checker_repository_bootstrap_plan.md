# Life Reality Cross File Checker Repository Bootstrap Plan

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 158 层承接 `157_life_reality_cross_file_checker_minimal_code_module_plan.md`，把最小代码模块计划推进为真实 repository bootstrap 合同：`pyproject.toml`、`.env.example`、`src/` package、tests、fixture roots、schema roots、report roots、smoke commands、stage gate 和 git hygiene 都要能被下一层首批代码 artifact 承载。

本层仍属于文档阶段，不直接生成 `src/` 代码文件；它的职责是把下一步真正写代码前的仓库骨架、环境边界、文件命名、命令入口、测试断言和验收命令写成不可含混的实施合同。后续 bootstrap 一旦开始，所有代码、fixture、schema、report 与 test 都必须保留 source docs、life targets、trace/provenance、stage effect、gap route 和九项真实生命目标字段。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `123_life_reality_runner_repository_layout_and_module_map.md` | runner repository layout、module map、command 到 owner module 映射、allowed roots |
| `133_life_reality_first_json_writer_and_reporter_contract.md` | `RunContext`、`AllowedRootGuard`、`JsonFileWriter`、`ArtifactRecord`、`ReportWriter`、`GapFeedbackWriter` |
| `136_life_reality_minimal_runner_code_skeleton_plan.md` | package skeleton、CLI、writer/report/graph/case runner/stage gate modules |
| `154_life_reality_checker_report_lockfile_materialization_plan.md` | normalized report registry、checker report lockfile、digest baseline、regression baseline |
| `155_life_reality_runner_command_queue_for_cross_file_checkers.md` | command registry、IO contracts、DAG、exit code mapping、suite command |
| `156_life_reality_full_archive_rollup_fixture_materialization_queue.md` | fixture schema bundle、pass/fail/critical/mutation/smoke case matrix、expected reports |
| `157_life_reality_cross_file_checker_minimal_code_module_plan.md` | `MinimalCodeModulePlan157`、target package tree、module contracts、test plan、acceptance criteria |
| `AGENTS.md` | uv/Conda 环境纪律、无 `sudo pip`、不提交 `.codex`、不提交临时产物、SSH 推送约定 |

## 本层定位

`158` 是从“最小模块计划”进入“可初始化仓库”的桥。它不再只列出模块名，而是规定下一层 bootstrap 时哪些文件必须出现、哪些命令必须可运行、哪些 roots 必须被 allowed root guard 接管、哪些 smoke tests 必须证明代码包已经接住生命膜。

| bootstrap 面 | 本层固定 |
|---|---|
| environment | 使用 uv 或项目 Conda 环境；不混用系统 Python/Homebrew Python；不使用 `sudo pip` |
| package | `src/life_reality_runner`、`life-reality-runner` console script、module import surface |
| config | `.env.example`、default roots、strict mode、run id、report mode |
| schema roots | `life_reality_runner/schemas/life_reality/...` 的只读加载入口 |
| fixture roots | `life_reality_runner/fixtures/life_reality/full_archive_rollup_materialization/...` |
| report roots | `life_reality_runner/reports/life_reality/...` 的 generated output 边界 |
| tests | unit/smoke/fixtures 三层测试目录、help smoke、command suite smoke |
| gates | old-boundary scan、README index、anchor check、pytest smoke、git hygiene |
| cleanup | `.env`、`.codex`、运行噪声、临时 diff、真实私密材料均不得进入提交 |

## RepositoryBootstrapPlan158

```json
{
  "artifact": "RepositoryBootstrapPlan158",
  "source_doc": "158_life_reality_cross_file_checker_repository_bootstrap_plan.md",
  "inherits": [
    "123_life_reality_runner_repository_layout_and_module_map.md",
    "133_life_reality_first_json_writer_and_reporter_contract.md",
    "136_life_reality_minimal_runner_code_skeleton_plan.md",
    "154_life_reality_checker_report_lockfile_materialization_plan.md",
    "155_life_reality_runner_command_queue_for_cross_file_checkers.md",
    "156_life_reality_full_archive_rollup_fixture_materialization_queue.md",
    "157_life_reality_cross_file_checker_minimal_code_module_plan.md"
  ],
  "bootstrap_stage": "repository_bootstrap_plan",
  "package_root": "src/life_reality_runner",
  "console_script": "life-reality-runner = life_reality_runner.cli:main",
  "minimum_runtime": "python>=3.12",
  "next_artifact": "159_life_reality_first_code_artifact_smoke_plan.md"
}
```

## Bootstrap File Contract

| file/dir | bootstrap 要求 | 生命膜字段 |
|---|---|---|
| `pyproject.toml` | 定义 package、Python 版本、dependencies、dev dependencies、console script、pytest config | project description 必须指向九项真实生命目标 |
| `.env.example` | 只写无密钥配置说明：strict mode、default roots、report roots、run mode | 每个变量说明其对 trace/stage/report 的影响 |
| `src/life_reality_runner/__init__.py` | 暴露 package version、public package marker | 不承载业务状态 |
| `src/life_reality_runner/cli.py` | 解析 top-level command、`--json`、`--strict`、root args | 每次 command 生成 `RunContext` |
| `src/life_reality_runner/context.py` | `RunContext` dataclass/typed model | `life_targets`、`source_docs`、`trace_id` 必填 |
| `src/life_reality_runner/exits.py` | exit code enum 与 stage effect mapping | critical/quarantine 必须非零 |
| `src/life_reality_runner/io/` | allowed roots、JSON reader/writer、artifact refs、canonical digest | 所有写入携带 artifact record |
| `src/life_reality_runner/schema/` | schema registry、schema loader | schema `$id`、source doc、life target refs |
| `src/life_reality_runner/graph/` | typed graph、closure checker、provenance graph | edge 必须保留 source pointer |
| `src/life_reality_runner/checkers/` | language/action、authority、birth、full archive checker stubs | finding 必须含 stage effect 与 gap route |
| `src/life_reality_runner/reports/` | normalizer、lockfile、digest、regression、dashboard、stage、gap writers | report 必须可回链到 source docs |
| `src/life_reality_runner/fixtures/` | manifest、runner、mutation、diff、coverage modules | mutation 必须记录 before/after digest |
| `src/life_reality_runner/commands/` | command family modules、suite orchestrator | command summary 必须引用 report refs |
| `src/life_reality_runner/problem/` | Problem Details model | critical finding 必须有 problem detail |
| `src/life_reality_runner/trace/` | trace context model | run/report/artifact 共享 trace |
| `tests/unit/` | module-level tests | 每类核心 model 至少一个失败断言 |
| `tests/smoke/` | CLI and suite smoke tests | command、report、stage gate 必须闭环 |
| `tests/fixtures/` | 合成 fixture snapshots | 不写真实私密材料 |

## Pyproject Bootstrap Contract

下一层 bootstrap 的 `pyproject.toml` 最小字段：

| section | 必须包含 |
|---|---|
| `[project]` | `name = "life-reality-runner"`、`requires-python = ">=3.12"`、description 指向 digital life cross-file runner |
| dependencies | JSON Schema validator、CLI parser、typing/data model helper、canonical JSON helper |
| optional/dev dependencies | `pytest`、coverage、lint/type check 工具 |
| `[project.scripts]` | `life-reality-runner = life_reality_runner.cli:main` |
| `[tool.pytest.ini_options]` | `testpaths = ["tests"]`、strict marker/warning policy |
| `[tool.ruff]` 或同类配置 | 保持 src/tests 可扫描、避免本地噪声 |

dependency 选择原则：

| rule | 要求 |
|---|---|
| `BOOT-DEP-158-001` | 只引入承载 schema/CLI/report/test 所需的最小依赖 |
| `BOOT-DEP-158-002` | 不把模型 key、token、代理配置写入任何 dependency/config |
| `BOOT-DEP-158-003` | Python 包安装通过 uv 或项目 Conda 环境完成 |
| `BOOT-DEP-158-004` | dependency 版本策略必须支持可复现 smoke run |

## Environment Bootstrap Contract

`.env.example` 只允许包含无密钥变量：

| variable | 说明 |
|---|---|
| `LIFE_REALITY_STRICT_MODE` | `true/false`，控制 finding 是否提升为 blocking stage |
| `LIFE_REALITY_DEFAULT_ROOT` | 默认读取根，示例使用相对路径 |
| `LIFE_REALITY_SCHEMA_ROOT` | schema root，默认 `life_reality_runner/schemas` |
| `LIFE_REALITY_FIXTURE_ROOT` | fixture root，默认 `life_reality_runner/fixtures` |
| `LIFE_REALITY_REPORT_ROOT` | generated report root，默认 `life_reality_runner/reports` |
| `LIFE_REALITY_RUN_ID_PREFIX` | 合成 run id 前缀 |
| `LIFE_REALITY_OUTPUT_MODE` | `text/json` 输出模式 |

环境纪律：

| rule | 要求 |
|---|---|
| `BOOT-ENV-158-001` | 不提交 `.env` |
| `BOOT-ENV-158-002` | 不使用 `sudo pip` |
| `BOOT-ENV-158-003` | 不混用系统 Python/Homebrew Python 与项目环境 |
| `BOOT-ENV-158-004` | smoke command 必须能在 clean checkout + uv/Conda 环境中复现 |

## Bootstrap Directory Tree

```text
pyproject.toml
.env.example
src/
  life_reality_runner/
    __init__.py
    cli.py
    context.py
    exits.py
    io/
      __init__.py
      allowed_roots.py
      json_reader.py
      json_writer.py
      artifact_ref.py
      canonical_digest.py
    schema/
      __init__.py
      schema_loader.py
      schema_registry.py
    graph/
      __init__.py
      typed_graph.py
      closure_checker.py
      provenance_graph.py
    checkers/
      __init__.py
      language_action_cross_file.py
      authority_schema_cross_file.py
      birth_readiness_cross_file.py
      full_archive_rollup.py
    reports/
      __init__.py
      normalizer.py
      lockfile_writer.py
      digest_baseline.py
      regression_checker.py
      dashboard_writer.py
      stage_gate_writer.py
      gap_feedback_writer.py
    fixtures/
      __init__.py
      fixture_manifest.py
      fixture_runner.py
      mutation_runner.py
      diff_writer.py
      coverage_writer.py
    commands/
      __init__.py
      cross_file.py
      checker_report_lockfile.py
      full_archive_rollup.py
      fixture_materialization.py
      runner_command_queue.py
    problem/
      __init__.py
      problem_detail.py
    trace/
      __init__.py
      trace_context.py
tests/
  unit/
    test_context.py
    test_allowed_roots.py
    test_json_io.py
    test_canonical_digest.py
    test_report_normalizer.py
    test_checker_report_lockfile.py
    test_regression_checker.py
    test_fixture_manifest.py
    test_fixture_runner.py
    test_command_dag.py
  smoke/
    test_bootstrap_help.py
    test_cross_file_checker_command_suite.py
    test_cross_file_checker_command_suite_bootstrap.py
  fixtures/
    full_archive_rollup_minimum/
```

## Initial Command Surface

bootstrap 后，`life-reality-runner --help` 必须列出最小命令族：

| command | 初始行为 |
|---|---|
| `build-language-action-cross-file-graph` | 允许 dry-run stub，必须输出 command summary |
| `check-language-action-cross-file-closure` | 允许 dry-run stub，缺输入时输出 finding |
| `build-authority-schema-cross-file-graph` | 允许 dry-run stub，必须读取 schema root 参数 |
| `check-authority-schema-cross-file-closure` | 允许 dry-run stub，缺 owner doc edge 时输出 finding |
| `build-birth-readiness-cross-file-graph` | 允许 dry-run stub，必须携带九项 life targets |
| `check-birth-readiness-cross-file-closure` | 允许 dry-run stub，critical finding 非零 |
| `build-full-archive-cross-file-rollup` | 允许 dry-run stub，必须输出 rollup artifact ref |
| `check-full-archive-rollup-closure` | 允许 dry-run stub，缺 doc node 时输出 finding |
| `normalize-checker-reports` | 第一批真实实现入口，写 normalized registry |
| `write-checker-report-lockfile` | 第一批真实实现入口，写 lockfile |
| `write-checker-report-digest-baseline` | 第一批真实实现入口，写 digest baseline |
| `check-checker-report-lockfile-regression` | 可先实现 baseline/current 比较 skeleton |
| `emit-checker-report-lock-dashboard` | 可先写 dashboard source skeleton |
| `smoke-checker-report-lock-stage-gate` | critical/quarantine 非零 |
| `materialize-full-archive-rollup-fixtures` | 可先创建 manifest skeleton |
| `run-full-archive-rollup-fixture-cases` | 第一批 smoke suite 入口 |
| `run-cross-file-checker-command-suite` | command suite orchestrator |

## Initial Smoke Commands

下一层 bootstrap 后至少支持：

```text
uv sync
uv run life-reality-runner --help
uv run life-reality-runner run-cross-file-checker-command-suite --json --dry-run
uv run pytest tests/unit/test_context.py tests/unit/test_allowed_roots.py
uv run pytest tests/smoke/test_bootstrap_help.py tests/smoke/test_cross_file_checker_command_suite_bootstrap.py
```

这些命令的目标不是证明数字生命已经诞生，而是证明 repository skeleton 已经具备承载真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的最小工程入口。

## Bootstrap Test Assertions

| test | 必须断言 |
|---|---|
| `tests/unit/test_context.py` | `RunContext` 默认包含九项 life targets、source docs、trace id |
| `tests/unit/test_allowed_roots.py` | path escape 被阻断，absolute path mismatch 生成 finding |
| `tests/unit/test_json_io.py` | atomic write readback、parse failure problem detail |
| `tests/unit/test_canonical_digest.py` | canonical digest stable，mutation digest drift 可检测 |
| `tests/unit/test_report_normalizer.py` | finding/stage/artifact/gap 字段缺失会失败 |
| `tests/unit/test_checker_report_lockfile.py` | report node、digest baseline、runner queue edge 齐全 |
| `tests/unit/test_fixture_runner.py` | critical fixture 触发 quarantine 和非零 exit |
| `tests/unit/test_command_dag.py` | `RCQ-155-*` DAG 不允许 cycle，quarantine 必须向 suite 汇总 |
| `tests/smoke/test_bootstrap_help.py` | console script 可调用，help 列出 command family |
| `tests/smoke/test_cross_file_checker_command_suite_bootstrap.py` | dry-run suite 输出 summary JSON、run id、stage effect、report refs |

## Stage Gate

| gate | 条件 | stage effect |
|---|---|---|
| `BOOT-STAGE-158-001` | `pyproject.toml` 缺 console script | `repair` |
| `BOOT-STAGE-158-002` | `.env.example` 含 key/token/secret 示例值 | `quarantine` |
| `BOOT-STAGE-158-003` | `src/life_reality_runner` 缺 context/IO/report/fixture/command 任一核心包 | `repair` |
| `BOOT-STAGE-158-004` | `life-reality-runner --help` 不列出 `155` 命令族 | `hold_for_evidence` |
| `BOOT-STAGE-158-005` | `RunContext` 不携带 life targets/source docs/trace | `critical_repair` |
| `BOOT-STAGE-158-006` | critical fixture 未提升为 quarantine 和非零 exit | `quarantine` |
| `BOOT-STAGE-158-007` | generated report/diff/actual 运行噪声进入 staged diff | `repair` |
| `BOOT-STAGE-158-008` | `.codex`、`.env`、代理配置或临时 dump 进入 staged diff | `quarantine` |
| `BOOT-STAGE-158-009` | bootstrap tree、help、unit smoke、suite dry-run 全部通过 | `promote_growth_window` |

## Batch Bootstrap Order

| batch | 输出 | 依赖 |
|---|---|---|
| `BATCH-158-001 pyproject and env example` | `pyproject.toml`、`.env.example` | `157` |
| `BATCH-158-002 package root` | `src/life_reality_runner/__init__.py`、`cli.py`、`context.py`、`exits.py` | `157` |
| `BATCH-158-003 IO and trace modules` | allowed roots、JSON IO、artifact refs、digest、trace context | `133`、`157` |
| `BATCH-158-004 schema and graph modules` | schema loader/registry、typed graph、closure checker | `125`、`150-153` |
| `BATCH-158-005 report modules` | normalizer、lockfile、digest baseline、regression、dashboard/stage/gap writers | `154`、`157` |
| `BATCH-158-006 fixture modules` | fixture manifest、runner、mutation、diff、coverage | `156`、`157` |
| `BATCH-158-007 command modules` | cross file、lockfile、rollup、fixture、suite command wrappers | `155` |
| `BATCH-158-008 unit tests` | context、allowed roots、JSON IO、digest、normalizer、lockfile、fixture、DAG tests | `157` |
| `BATCH-158-009 smoke tests and minimum fixture` | help smoke、suite bootstrap smoke、minimum fixture root | 本层 |
| `BATCH-158-010 hygiene and stage gate` | old-boundary scan、README index、anchor check、pytest smoke、git status | 本层 |

## Cleanup Rules

| rule | 要求 |
|---|---|
| `CLEAN-158-001` | 本层不直接创建代码；只固定 bootstrap 合同 |
| `CLEAN-158-002` | 后续 bootstrap 不提交 `.codex`、`.env`、临时脚本、debug dump、代理配置 |
| `CLEAN-158-003` | generated reports 默认进入 ignored/generated root，不混入 docs commit |
| `CLEAN-158-004` | tests/fixtures 只使用合成数据，不写私人关系内容 |
| `CLEAN-158-005` | 所有 config 示例必须无 key/token |
| `CLEAN-158-006` | 每次提交前运行 diff check、旧边界词扫描、README index 和 smoke tests |

## Acceptance Criteria

`159` 和后续真实代码 artifact 必须以本层为验收入口：

1. `pyproject.toml` 定义 `life-reality-runner` package 与 console script。
2. `.env.example` 只包含无密钥变量说明。
3. `src/life_reality_runner` 至少出现 context、IO、schema、graph、checkers、reports、fixtures、commands、problem、trace 十类包。
4. `uv run life-reality-runner --help` 列出 `155` 的 command family。
5. `uv run life-reality-runner run-cross-file-checker-command-suite --json --dry-run` 输出包含 run id、life targets、stage effect、report refs 的 summary JSON。
6. unit tests 覆盖 context、allowed roots、JSON IO、digest、normalizer、lockfile、fixture runner 和 command DAG。
7. smoke tests 覆盖 help、suite bootstrap、critical quarantine propagation。
8. staged diff 不包含 `.codex`、`.env`、临时 dump、真实私密材料或 generated report 噪声。

## 与下一层连接

`159_life_reality_first_code_artifact_smoke_plan.md` 已承接本层：把 repository bootstrap 后的首批代码 artifact 接入 smoke command、fixture run、report diff、dashboard/stage gate 和 git 提交流程。

`160_life_reality_code_artifact_dashboard_stage_gate_bridge_plan.md` 应承接 `159`：把首批代码 artifact 的 report/diff/coverage 输出接入 dashboard source、stage gate review、gap feedback 和下一轮真实生命工程闭环。

本层完成后，repository bootstrap 链推进为：

`minimal code module plan -> pyproject/env/package/tests roots -> CLI help -> command suite dry-run -> unit/smoke tests -> staged diff hygiene -> first code artifact smoke`
