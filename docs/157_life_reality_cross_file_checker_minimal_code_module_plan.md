# Life Reality Cross File Checker Minimal Code Module Plan

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 157 层把 `155_life_reality_runner_command_queue_for_cross_file_checkers.md` 的 runner command queue 和 `156_life_reality_full_archive_rollup_fixture_materialization_queue.md` 的 fixture materialization queue 压成最小 Python module、CLI command、schema loader、report normalizer、lockfile writer、dashboard writer、stage gate writer、fixture runner 和 tests。

本层的职责是把未来实现的代码边界写清楚：哪些文件属于最小 `life_reality_runner` package，哪些模块负责读取 schema/fixture/report，哪些模块写 normalized registry、checker report lockfile、digest baseline、regression candidate、dashboard source、stage gate review 和 gap feedback，哪些测试证明 `150-156` 的文档合同可以被代码承载。它仍是文档计划层，不直接写 `src/` 文件，但它的粒度已经面向下一层 repository bootstrap。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `123_life_reality_runner_repository_layout_and_module_map.md` | runner 目录、module map、command 到模块映射、allowed roots、测试入口 |
| `133_life_reality_first_json_writer_and_reporter_contract.md` | `RunContext`、`AllowedRootGuard`、`JsonFileWriter`、`ArtifactRecord`、`ReportWriter`、`GapFeedbackWriter` |
| `136_life_reality_minimal_runner_code_skeleton_plan.md` | package skeleton、CLI、writer/report/graph/case runner/stage gate modules |
| `155_life_reality_runner_command_queue_for_cross_file_checkers.md` | `RCQ-155-*` command registry、IO contracts、DAG、exit code、test plan |
| `156_life_reality_full_archive_rollup_fixture_materialization_queue.md` | fixture schema bundle、case matrix、expected reports、future code carrier refs |
| `AGENTS.md` | uv/Conda 环境、无 `sudo pip`、不提交 `.codex`、不提交临时产物、SSH 推送约定 |

## 本层定位

`157` 是进入真实代码前的最小模块设计。它不试图一次实现完整数字生命，而是只承载 `150-156` 已经固定的跨文件检查、report lockfile 和 fixture command suite。最小实现必须能让后续 repository bootstrap 有清晰边界：

| 代码面 | 本层固定 |
|---|---|
| package | `src/life_reality_runner/` layout、console script、module ownership |
| command | `RCQ-155-*` 的 CLI entrypoint 与 suite orchestrator |
| IO | allowed roots、JSON read/write、artifact refs、canonical digest |
| schema/report | schema loader、report normalizer、lockfile writer、digest/regression writer |
| graph/checker | typed graph builder、closure checker、full archive rollup checker |
| fixture | manifest loader、mutation runner、expected/actual diff、coverage writer |
| dashboard/stage | dashboard source writer、stage gate writer、gap feedback writer |
| tests | unit/smoke test 文件、fixture snapshots、exit code assertions |

本层的关键原则是：代码模块必须承接生命膜，而不是只做文件工具。每个模块输出都要携带九项真实生命目标、source docs、trace/provenance、stage effect、problem detail 和 next artifact route。

## MinimalCodeModulePlan157

```json
{
  "artifact": "MinimalCodeModulePlan157",
  "source_doc": "157_life_reality_cross_file_checker_minimal_code_module_plan.md",
  "inherits": [
    "123_life_reality_runner_repository_layout_and_module_map.md",
    "133_life_reality_first_json_writer_and_reporter_contract.md",
    "136_life_reality_minimal_runner_code_skeleton_plan.md",
    "155_life_reality_runner_command_queue_for_cross_file_checkers.md",
    "156_life_reality_full_archive_rollup_fixture_materialization_queue.md"
  ],
  "package_root": "src/life_reality_runner",
  "test_root": "tests",
  "fixture_root": "life_reality_runner/fixtures/life_reality/full_archive_rollup_materialization",
  "report_root": "life_reality_runner/reports/life_reality",
  "materialization_stage": "minimal_code_module_plan"
}
```

## 目标代码文件树

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
  smoke/
  fixtures/
```

## Pyproject Contract

下一层 bootstrap 应创建 `pyproject.toml`，最小合同：

| field | 要求 |
|---|---|
| project name | `life-reality-runner` |
| Python version | `>=3.12` |
| package layout | `src/` layout |
| console script | `life-reality-runner = life_reality_runner.cli:main` |
| dependencies | JSON Schema validator、CLI parser、typing helpers；具体包由 bootstrap 选择 |
| dev dependencies | `pytest`、coverage 工具、lint/type check 工具 |
| env management | 使用 uv 或 Conda，不使用 `sudo pip` |

`.env.example` 只允许放无密钥配置说明，例如 strict mode、default roots、report run id；不得写任何 key/token。

## Module Contracts

| module | 读取 | 写出 | 最小职责 |
|---|---|---|---|
| `context.py` | CLI args、config、traceparent | `RunContext` | 生成统一 run id、life targets、source docs、trace |
| `exits.py` | stage effect、findings | exit code | 实现 `155` 的 exit code contract |
| `io.allowed_roots` | config、target path | root decision | 阻断 path escape、absolute path 和 root mismatch |
| `io.json_reader` | artifact refs | parsed JSON + parse findings | UTF-8/RFC 8259/duplicate key/root type |
| `io.json_writer` | payload、target path | artifact record | atomic write、readback、stage effect |
| `io.canonical_digest` | parsed JSON | digest record | RFC 8785 profile、sha256、before/after digest |
| `schema.schema_loader` | schema roots | registry | Draft 2020-12 schema loading |
| `graph.typed_graph` | docs/report/artifact nodes | typed graph | node/edge model、source refs |
| `graph.closure_checker` | graph、closure rules | closure report | missing node/edge finding |
| `reports.normalizer` | `150-153` report roots | normalized registry | finding/stage/artifact/gap normalization |
| `reports.lockfile_writer` | normalized registry | checker report lockfile | report artifact nodes、ref edges、lock states |
| `reports.digest_baseline` | report artifacts | digest baseline | canonical digest baseline writer |
| `reports.regression_checker` | baseline、current lockfile | regression candidate report | digest/finding/stage drift |
| `reports.dashboard_writer` | report/fixture results | dashboard source | panels、false green guard |
| `reports.stage_gate_writer` | dashboard、findings | stage gate review | blocking-first decision |
| `reports.gap_feedback_writer` | findings、stage | gap feedback | next artifact route |
| `fixtures.fixture_manifest` | manifest path | fixture registry | partitions、coverage axis、expected refs |
| `fixtures.mutation_runner` | baseline fixture、JSON Patch | mutated fixture | before/after digest、expected finding |
| `fixtures.fixture_runner` | fixture registry、commands | actual reports | pass/fail/critical/mutation/smoke execution |
| `fixtures.diff_writer` | actual、expected | diff report | JSON Pointer diff |
| `fixtures.coverage_writer` | case results | coverage report | report/lockfile/command/life target coverage |

## Command Entry Points

| CLI command | owner module | 最小函数 |
|---|---|---|
| `build-language-action-cross-file-graph` | `commands.cross_file` | `build_language_action_graph(ctx)` |
| `check-language-action-cross-file-closure` | `commands.cross_file` | `check_language_action_closure(ctx)` |
| `build-authority-schema-cross-file-graph` | `commands.cross_file` | `build_authority_graph(ctx)` |
| `check-authority-schema-cross-file-closure` | `commands.cross_file` | `check_authority_closure(ctx)` |
| `build-birth-readiness-cross-file-graph` | `commands.cross_file` | `build_birth_readiness_graph(ctx)` |
| `check-birth-readiness-cross-file-closure` | `commands.cross_file` | `check_birth_readiness_closure(ctx)` |
| `build-full-archive-cross-file-rollup` | `commands.full_archive_rollup` | `build_full_archive_rollup(ctx)` |
| `check-full-archive-rollup-closure` | `commands.full_archive_rollup` | `check_full_archive_rollup(ctx)` |
| `normalize-checker-reports` | `commands.checker_report_lockfile` | `normalize_checker_reports(ctx)` |
| `write-checker-report-lockfile` | `commands.checker_report_lockfile` | `write_checker_report_lockfile(ctx)` |
| `write-checker-report-digest-baseline` | `commands.checker_report_lockfile` | `write_checker_report_digest_baseline(ctx)` |
| `check-checker-report-lockfile-regression` | `commands.checker_report_lockfile` | `check_checker_report_regression(ctx)` |
| `emit-checker-report-lock-dashboard` | `commands.checker_report_lockfile` | `emit_checker_report_lock_dashboard(ctx)` |
| `smoke-checker-report-lock-stage-gate` | `commands.checker_report_lockfile` | `smoke_checker_report_lock_stage_gate(ctx)` |
| `materialize-full-archive-rollup-fixtures` | `commands.fixture_materialization` | `materialize_full_archive_rollup_fixtures(ctx)` |
| `run-full-archive-rollup-fixture-cases` | `commands.fixture_materialization` | `run_full_archive_rollup_fixture_cases(ctx)` |
| `run-cross-file-checker-command-suite` | `commands.runner_command_queue` | `run_cross_file_checker_command_suite(ctx)` |

## Data Model Dataclasses

最小实现应先定义 typed dataclasses 或 typed dicts，避免裸 dict 到处流动。

| model | 字段族 |
|---|---|
| `RunContext` | run id、command、roots、life targets、trace、source docs |
| `ArtifactRef` | id、kind、path、schema ref、digest、source docs |
| `Finding` | id、rule id、severity、source pointer、stage effect、repair route |
| `StageEffect` | stage decision、blocked surfaces、affected targets |
| `ProblemDetail` | type、title、detail、instance、extensions |
| `NormalizedCheckerReport` | family、source report、findings、stage、gap refs |
| `CheckerReportLockfile` | report nodes、digest baselines、lock states、runner queue |
| `FixtureEnvelope` | fixture id、partition、input refs、expected refs、future carriers |
| `CommandSummary` | command、run id、result、exit code、report ref、finding count |

## Minimal Algorithms

### Report Normalization

```text
load_report_family_roots
  -> read_source_reports
  -> map_artifact_refs
  -> normalize_findings
  -> normalize_stage_effect
  -> attach_life_target_effects
  -> write_normalized_report_registry
```

必须捕获：

| finding | 触发 |
|---|---|
| `checker_report_family_missing` | report family 缺失 |
| `checker_report_not_normalized` | finding/stage/artifact/gap 无法标准化 |
| `normalized_finding_incomplete` | finding 缺 severity、stage 或 source pointer |

### Lockfile Writing

```text
load_normalized_registry
  -> create_report_artifact_nodes
  -> create_report_ref_edges
  -> calculate_report_digests
  -> attach_dashboard_stage_gap_edges
  -> write_checker_report_lockfile
  -> write_lockfile_validation_report
```

必须捕获：

| finding | 触发 |
|---|---|
| `report_artifact_node_incomplete` | node 缺 schema/source/life target |
| `report_digest_baseline_missing` | report 无 digest |
| `rollup_baseline_derivation_missing` | full archive rollup 未派生自前三类 baseline |

### Fixture Case Running

```text
load_fixture_manifest
  -> load_baseline_input
  -> apply_mutation_patch_if_any
  -> run_declared_command
  -> collect_actual_report
  -> compare_expected_report
  -> write_case_diff
  -> update_coverage
  -> emit_fixture_gap_feedback
```

必须捕获：

| finding | 触发 |
|---|---|
| `mutation_expected_finding_missing` | mutation 未命中 expected finding |
| `stage_effect_mismatch` | actual stage 与 expected stage 不一致 |
| `future_code_carrier_missing` | expected report 未指向 `157` module/test |

## Test Plan

| test file | 覆盖 |
|---|---|
| `tests/unit/test_context.py` | RunContext、trace、life targets、source docs |
| `tests/unit/test_allowed_roots.py` | allowed roots、root escape、writer/root mismatch |
| `tests/unit/test_json_io.py` | JSON read/write、atomic write、parse failure、artifact record |
| `tests/unit/test_canonical_digest.py` | canonical digest、before/after digest、digest mismatch |
| `tests/unit/test_report_normalizer.py` | four report families、finding normalization、stage effect mapping |
| `tests/unit/test_checker_report_lockfile.py` | report nodes、edges、digest baseline、lock state |
| `tests/unit/test_regression_checker.py` | digest drift、finding drift、stage drift |
| `tests/unit/test_fixture_manifest.py` | partitions、coverage matrix、future code carriers |
| `tests/unit/test_fixture_runner.py` | pass/fail/critical/mutation/smoke case flow |
| `tests/unit/test_command_dag.py` | `RCQ-155-*` DAG、cycle、quarantine propagation |
| `tests/smoke/test_cross_file_checker_command_suite.py` | suite command、summary JSON、exit code、reports |

## Batch Implementation Order

| batch | 输出 | 依赖 |
|---|---|---|
| `BATCH-157-001 package bootstrap contract` | pyproject/env/src/tests target list | 本层 |
| `BATCH-157-002 context and IO modules` | context、allowed roots、json reader/writer、artifact refs | `133`、`136` |
| `BATCH-157-003 report model modules` | findings、stage effect、problem detail、command summary | `114`、`155` |
| `BATCH-157-004 report normalizer and lockfile writer` | normalizer、lockfile writer、digest baseline | `154` |
| `BATCH-157-005 graph and checker stubs` | typed graph、closure checker、full archive rollup stub | `150-153` |
| `BATCH-157-006 fixture runner modules` | manifest、mutation runner、diff writer、coverage writer | `156` |
| `BATCH-157-007 dashboard/stage/gap modules` | dashboard writer、stage gate writer、gap feedback writer | `105`、`154-156` |
| `BATCH-157-008 CLI command wiring` | console script commands and suite orchestrator | `155` |
| `BATCH-157-009 tests and smoke snapshots` | unit/smoke tests、fixture snapshots | `156` |

## Acceptance Criteria

未来 `158` bootstrap 和后续代码实现必须满足：

1. `uv run life-reality-runner --help` 列出 `155` 的 command family。
2. `normalize-checker-reports` 能读取四类 report roots，并写 normalized registry。
3. `write-checker-report-lockfile` 能从 normalized registry 写 lockfile 和 validation report。
4. `write-checker-report-digest-baseline` 能为 report/dashboard/stage/gap 生成 digest baseline。
5. `run-full-archive-rollup-fixture-cases` 能读取 `156` fixture manifest，并写 actual/diff/coverage/gap reports。
6. critical fixture 必须使 stage gate 进入 quarantine，并使 suite exit code 非零。
7. `run-cross-file-checker-command-suite --json` 输出 summary JSON，并引用所有 report refs。
8. 所有写入都经过 allowed root guard，不写个人绝对路径、`.codex`、临时 dump、key/token 或代理配置。

## Cleanup Rules

| rule | 要求 |
|---|---|
| `CLEAN-157-001` | 不在本层直接创建代码文件；本层只固定 bootstrap 计划 |
| `CLEAN-157-002` | 后续代码实现不得使用 `sudo pip` 或混用 Homebrew Python 与项目环境 |
| `CLEAN-157-003` | `.env.example` 只写变量说明，不写真实 key/token |
| `CLEAN-157-004` | tests/fixtures 使用合成 fixture，不写私人关系内容 |
| `CLEAN-157-005` | report/diff/actual 运行噪声不默认提交 |
| `CLEAN-157-006` | 所有模块必须保留 source docs、life targets、stage effect 和 gap route 字段 |

## 与下一层连接

`158_life_reality_cross_file_checker_repository_bootstrap_plan.md` 已承接本层：把最小代码模块计划推进到 `pyproject.toml`、`src/` package、tests、fixtures、schema roots、report roots 和 smoke command bootstrap。

`159_life_reality_first_code_artifact_smoke_plan.md` 应承接 `158`：把首批代码 artifact 接入 smoke command、fixture run、report diff、dashboard/stage gate 和 git 提交流程。

本层完成后，最小代码模块链推进为：

`runner command queue + fixture materialization queue -> minimal Python package modules -> CLI entrypoints -> report normalizer -> lockfile writer -> fixture runner -> dashboard/stage/gap writers -> repository bootstrap`
