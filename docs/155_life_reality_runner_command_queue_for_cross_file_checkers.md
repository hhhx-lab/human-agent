# Life Reality Runner Command Queue For Cross File Checkers

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 155 层把 `150_life_reality_language_action_cross_file_checker_plan.md` 到 `154_life_reality_checker_report_lockfile_materialization_plan.md` 的 checker、lockfile、dashboard 和 stage gate 合同推进为未来 runner CLI、fixture roots、report roots、schema roots、lockfile roots 和 smoke command 实现队列。

本层的职责是把跨文件检查体系从 Markdown 合同压成可实现命令队列。前面各层已经定义语言行动、权威 schema、出生准备度、全库 rollup 和 checker report lockfile；`155` 要把这些对象分配给未来 Python package 模块、CLI command、输入输出目录、exit code、report writer、stage gate 和测试入口。它仍不直接写代码，但已经把后续代码实现所需的命令名、模块边界、文件根、参数、输出和批次固定下来。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `118_life_reality_generation_runner_cli_contract.md` | CLI global options、command DAG、strict/dry-run/json 模式、trace、exit code、atomic write |
| `123_life_reality_runner_repository_layout_and_module_map.md` | runner 目录、module map、command 到模块映射、读写边界、测试入口 |
| `126_life_reality_runner_smoke_command_execution_plan.md` | smoke preflight、stdout/stderr 合同、report 写入顺序、exit code owner |
| `133_life_reality_first_json_writer_and_reporter_contract.md` | RunContext、AllowedRootGuard、JsonFileWriter、ArtifactRecord、ReportWriter、GapFeedbackWriter |
| `136_life_reality_minimal_runner_code_skeleton_plan.md` | package skeleton、CLI module、writer/report/graph/case runner/stage gate/test modules |
| `150-153` | language/authority/birth/full archive checker commands、fixtures、reports、dashboard/stage contracts |
| `154_life_reality_checker_report_lockfile_materialization_plan.md` | normalized report registry、checker report lockfile、digest baseline、regression baseline、runner queue `RUNQ-154-*` |

## 本层定位

`155` 是未来代码实现前的命令分派层。它把 `150-154` 的所有 smoke commands 和 runner queue 整理为四组可实现 command family：

| command family | 来源 | 实现目标 |
|---|---|---|
| cross-file checker commands | `150`、`151`、`152`、`153` | 构建 graph、检查 closure、写 dashboard、写 stage gate |
| checker report lockfile commands | `154` | normalize report、write lockfile、write digest、check regression |
| fixture execution commands | `150-154` | 跑 pass/fail/critical/mutation/withheld/smoke fixture family |
| orchestration commands | 本层 | 串联 preflight、checker、lockfile、dashboard、stage、gap 和 top-level report |

本层的关键原则是：工程落地不靠临时脚本和手工命令，而靠稳定 CLI、稳定模块、稳定输入输出和稳定验收报告。每条命令必须知道自己读什么、写什么、失败如何进入 repair/quarantine/hold、如何影响九项真实生命目标、如何被下一层 fixture 和最小代码模块承载。

## RunnerCommandQueue155

```json
{
  "artifact": "RunnerCommandQueue155",
  "source_doc": "155_life_reality_runner_command_queue_for_cross_file_checkers.md",
  "inherits": [
    "118_life_reality_generation_runner_cli_contract.md",
    "123_life_reality_runner_repository_layout_and_module_map.md",
    "126_life_reality_runner_smoke_command_execution_plan.md",
    "136_life_reality_minimal_runner_code_skeleton_plan.md",
    "150_life_reality_language_action_cross_file_checker_plan.md",
    "151_life_reality_authority_schema_cross_file_checker_plan.md",
    "152_life_reality_birth_readiness_cross_file_checker_plan.md",
    "153_life_reality_full_archive_cross_file_checker_rollup_plan.md",
    "154_life_reality_checker_report_lockfile_materialization_plan.md"
  ],
  "module_root": "src/life_reality_runner",
  "schema_root": "life_reality_runner/schemas/life_reality/runner_command_queue",
  "fixture_root": "life_reality_runner/fixtures/life_reality/runner_command_queue",
  "report_root": "life_reality_runner/reports/life_reality/runner_command_queue",
  "stage_gate_policy": "blocking_first",
  "materialization_stage": "runner_command_queue_plan"
}
```

## 目标文件树

```text
src/
  life_reality_runner/
    cli.py
    context.py
    commands/
      cross_file.py
      checker_report_lockfile.py
      full_archive_rollup.py
      runner_command_queue.py
    checkers/
      language_action_cross_file.py
      authority_schema_cross_file.py
      birth_readiness_cross_file.py
      full_archive_rollup.py
    reports/
      normalizer.py
      lockfile_writer.py
      digest_baseline.py
      regression_checker.py
      dashboard_writer.py
      stage_gate_writer.py
      gap_feedback_writer.py
    graph/
      typed_graph_builder.py
      closure_checker.py
      provenance_graph.py
    fixtures/
      command_fixture_runner.py
      mutation_runner.py
    io/
      allowed_roots.py
      json_reader.py
      json_writer.py
      artifact_ref.py
    problem/
      problem_detail.py
    trace/
      trace_context.py
life_reality_runner/
  schemas/
    life_reality/
      runner_command_queue/
        runner_command_queue_shared_defs.schema.json
        runner_command_queue_manifest.schema.json
        runner_command_spec.schema.json
        runner_command_io_contract.schema.json
        runner_command_stage_effect.schema.json
        runner_command_batch.schema.json
        runner_command_queue_report.schema.json
        runner_command_queue_dashboard_source.schema.json
        runner_command_queue_stage_gate_review.schema.json
        runner_command_queue_gap_feedback.schema.json
        runner_command_queue_schema_bundle.schema.json
  fixtures/
    life_reality/
      runner_command_queue/
        manifest/
        pass/
        fail/
        critical/
        mutation/
        smoke/
        report_expected/
  reports/
    life_reality/
      runner_command_queue/
        latest/
          runner_command_queue_manifest.json
          runner_command_queue_report.json
          runner_command_batch_report.json
          runner_command_dashboard_source.json
          runner_command_stage_gate_review.json
          runner_command_gap_feedback.json
```

## Global Command Contract

所有新增 command 继承 `118` 和 `126` 的全局选项：

```text
--config <path>
--run-id <id>
--traceparent <traceparent>
--tracestate <tracestate>
--schema-root <path>
--fixture-root <path>
--report-root <path>
--lockfile-root <path>
--dashboard-root <path>
--strict
--dry-run
--json
--fail-fast
```

全局规则：

| rule | 要求 |
|---|---|
| `RCQ-GLOBAL-155-001` | `validate-config` 和 allowed root preflight 先于所有 command |
| `RCQ-GLOBAL-155-002` | command stdout 在 `--json` 下只输出 summary object |
| `RCQ-GLOBAL-155-003` | 每个 command 必须写 report JSON，即使 fail-fast 提前停止 |
| `RCQ-GLOBAL-155-004` | 每个 report 必须有 run id、trace、provenance、affected life targets 和 stage effect |
| `RCQ-GLOBAL-155-005` | critical/quarantine finding 必须让 command exit code 非零，并写 problem detail |
| `RCQ-GLOBAL-155-006` | dry-run 只写 dry-run report 和 command plan，不写最终 lockfile baseline |

## Command Registry

| command id | CLI command | owner modules | 来源 | 主要输出 |
|---|---|---|---|---|
| `RCQ-155-001` | `build-language-action-cross-file-graph` | `commands.cross_file`、`checkers.language_action_cross_file`、`graph.typed_graph_builder` | `150` | language graph report |
| `RCQ-155-002` | `check-language-action-cross-file-closure` | `checkers.language_action_cross_file`、`graph.closure_checker` | `150` | language closure report |
| `RCQ-155-003` | `build-authority-schema-cross-file-graph` | `checkers.authority_schema_cross_file`、`graph.provenance_graph` | `151` | authority graph report |
| `RCQ-155-004` | `check-authority-schema-cross-file-closure` | `checkers.authority_schema_cross_file`、`graph.closure_checker` | `151` | authority closure report |
| `RCQ-155-005` | `build-birth-readiness-cross-file-graph` | `checkers.birth_readiness_cross_file`、`graph.typed_graph_builder` | `152` | readiness graph report |
| `RCQ-155-006` | `check-birth-readiness-cross-file-closure` | `checkers.birth_readiness_cross_file`、`graph.closure_checker` | `152` | birth closure report |
| `RCQ-155-007` | `build-full-archive-cross-file-rollup` | `checkers.full_archive_rollup`、`reports.normalizer` | `153` | rollup graph report |
| `RCQ-155-008` | `check-full-archive-rollup-closure` | `checkers.full_archive_rollup`、`graph.closure_checker` | `153` | full archive closure report |
| `RCQ-155-009` | `normalize-checker-reports` | `reports.normalizer` | `154` | normalized report registry |
| `RCQ-155-010` | `write-checker-report-lockfile` | `reports.lockfile_writer`、`io.json_writer` | `154` | checker report lockfile |
| `RCQ-155-011` | `write-checker-report-digest-baseline` | `reports.digest_baseline` | `154` | digest baseline lock |
| `RCQ-155-012` | `check-checker-report-lockfile-regression` | `reports.regression_checker` | `154` | regression candidate report |
| `RCQ-155-013` | `emit-checker-report-lock-dashboard` | `reports.dashboard_writer` | `154` | dashboard source |
| `RCQ-155-014` | `smoke-checker-report-lock-stage-gate` | `reports.stage_gate_writer` | `154` | stage gate review |
| `RCQ-155-015` | `run-cross-file-checker-command-suite` | `commands.runner_command_queue` | 本层 | top-level command suite report |

## Command IO Contracts

| command | required inputs | required outputs | stage effects |
|---|---|---|---|
| `build-language-action-cross-file-graph` | language schema root、authority schema root、birth schema root | `graph_report.json`、problem details | repair/hold/quarantine |
| `check-language-action-cross-file-closure` | language graph report | `closure_report.json`、finding report、gap feedback | repair/critical_repair/quarantine |
| `build-authority-schema-cross-file-graph` | authority schema root、language closure report、birth schema root | `authority_graph_report.json` | repair/hold |
| `check-authority-schema-cross-file-closure` | authority graph report | `authority_closure_report.json`、lockfile bridge report | repair/hold/quarantine |
| `build-birth-readiness-cross-file-graph` | birth schema root、language closure report、authority closure report | `readiness_graph_report.json` | hold/critical_repair |
| `check-birth-readiness-cross-file-closure` | readiness graph report | target/cross-chain/longitudinal/false-green reports | critical_repair/quarantine |
| `build-full-archive-cross-file-rollup` | docs index、language report、authority report、birth report | `rollup_graph_report.json`、runner queue report | repair/hold/quarantine |
| `check-full-archive-rollup-closure` | rollup graph report | archive consistency report、false green guard | repair/critical_repair/quarantine |
| `normalize-checker-reports` | four report roots | `normalized_report_registry.json` | repair/hold |
| `write-checker-report-lockfile` | normalized registry | `checker_report_lockfile.json`、validation report | hold/repair/quarantine |
| `write-checker-report-digest-baseline` | checker report lockfile | `checker_report_digest_baseline.lock.json` | hold/repair |
| `check-checker-report-lockfile-regression` | regression baseline、current lockfile | `regression_candidate_report.json` | repair/quarantine |
| `emit-checker-report-lock-dashboard` | checker report lockfile run root | `dashboard_source.json` | hold/repair |
| `smoke-checker-report-lock-stage-gate` | stage review input | `stage_gate_review.json`、gap feedback | open/hold/repair/quarantine |
| `run-cross-file-checker-command-suite` | runner command queue manifest | top-level suite report、dashboard、stage、gap | aggregate |

## Command DAG

```text
validate-config
  -> build-language-action-cross-file-graph
  -> check-language-action-cross-file-closure
  -> build-authority-schema-cross-file-graph
  -> check-authority-schema-cross-file-closure
  -> build-birth-readiness-cross-file-graph
  -> check-birth-readiness-cross-file-closure
  -> build-full-archive-cross-file-rollup
  -> check-full-archive-rollup-closure
  -> normalize-checker-reports
  -> write-checker-report-lockfile
  -> write-checker-report-digest-baseline
  -> check-checker-report-lockfile-regression
  -> emit-checker-report-lock-dashboard
  -> smoke-checker-report-lock-stage-gate
  -> run-cross-file-checker-command-suite
```

DAG rules：

| rule | 要求 |
|---|---|
| `RCQ-DAG-155-001` | language closure 先于 authority graph 的 language edge validation |
| `RCQ-DAG-155-002` | authority closure 先于 birth readiness graph 的 authority refs validation |
| `RCQ-DAG-155-003` | birth readiness closure 先于 full archive rollup |
| `RCQ-DAG-155-004` | full archive rollup 先于 checker report lockfile |
| `RCQ-DAG-155-005` | digest baseline 先于 regression check |
| `RCQ-DAG-155-006` | dashboard lock source 先于 stage gate smoke |
| `RCQ-DAG-155-007` | 任一 quarantine finding 允许继续写 partial downstream report，但最终 suite exit code 非零 |

## Module Contracts

| module | 读取 | 写出 | 承接 |
|---|---|---|---|
| `commands.cross_file` | CLI args、RunContext、root refs | command summaries、report refs | `118`、`126`、`150-153` |
| `commands.checker_report_lockfile` | normalized registry、lockfile args | lockfile、digest baseline、regression report | `154` |
| `commands.runner_command_queue` | command queue manifest | suite report、dashboard、stage、gap | 本层 |
| `checkers.language_action_cross_file` | language/action/authority/birth roots | language graph、closure findings | `150` |
| `checkers.authority_schema_cross_file` | authority registry、language report、birth refs | authority graph、closure findings | `151` |
| `checkers.birth_readiness_cross_file` | birth schema、language/authority reports | readiness graph、cross-chain findings | `152` |
| `checkers.full_archive_rollup` | docs index、checker reports、lockfile refs | rollup graph、life target matrix | `153` |
| `reports.normalizer` | heterogeneous checker reports | normalized report registry | `154` |
| `reports.lockfile_writer` | normalized registry、artifact nodes | checker report lockfile | `154` |
| `reports.digest_baseline` | report artifacts | digest baseline lock | `135`、`154` |
| `reports.regression_checker` | baseline、current lockfile | regression candidate report | `135`、`154` |
| `fixtures.command_fixture_runner` | command fixture manifest | actual/diff/coverage reports | `156` |

## Exit Code Contract

| exit code | condition | stage effect |
|---:|---|---|
| 0 | command pass、no blocking finding | `open_next_stage` 或 `promote_growth_window` |
| 1 | repair finding present | `repair` |
| 2 | hold finding present | `hold_for_evidence` |
| 3 | critical repair finding present | `critical_repair` |
| 4 | quarantine finding present | `quarantine` |
| 5 | preflight/config/root failure | `repair` 或 `quarantine` |
| 6 | internal problem detail written | `hold_for_evidence` |

exit rules：

| rule | 要求 |
|---|---|
| `RCQ-EXIT-155-001` | suite exit code 取最高阻断等级 |
| `RCQ-EXIT-155-002` | partial downstream report 不覆盖 upstream failure exit code |
| `RCQ-EXIT-155-003` | `--json` summary 必须含 exit code、stage effect、report ref 和 finding count |
| `RCQ-EXIT-155-004` | quarantine 永远阻断 stage open |

## Runner Command Queue Manifest

`runner_command_queue_manifest.json` 最小字段：

```json
{
  "manifest_kind": "RunnerCommandQueueManifest",
  "manifest_version": "0.1.0",
  "queue_id": "runner_command_queue_155",
  "source_docs": [
    "150_life_reality_language_action_cross_file_checker_plan.md",
    "151_life_reality_authority_schema_cross_file_checker_plan.md",
    "152_life_reality_birth_readiness_cross_file_checker_plan.md",
    "153_life_reality_full_archive_cross_file_checker_rollup_plan.md",
    "154_life_reality_checker_report_lockfile_materialization_plan.md"
  ],
  "commands": [],
  "schema_roots": [],
  "fixture_roots": [],
  "report_roots": [],
  "lockfile_roots": [],
  "dashboard_roots": [],
  "stage_gate_policy": "blocking_first",
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

manifest rules：

| rule | 要求 |
|---|---|
| `RCQ-MANIFEST-155-001` | commands 覆盖 `RCQ-155-001` 到 `RCQ-155-015` |
| `RCQ-MANIFEST-155-002` | 每个 command 都有 owner module、input root、output report、stage effect map |
| `RCQ-MANIFEST-155-003` | schema/fixture/report/lockfile/dashboard roots 全部通过 allowed root resolver |
| `RCQ-MANIFEST-155-004` | source docs 覆盖 `150-155` |
| `RCQ-MANIFEST-155-005` | life reality targets 覆盖九项目标 |

## Dashboard Source

| panel id | 读取对象 | 输出 |
|---|---|---|
| `runner_command_queue_overview_panel` | command queue report | command count、pass/fail、stage effect、exit max |
| `command_dag_panel` | command DAG | upstream/downstream、blocked path、partial report |
| `module_ownership_panel` | module contracts | command 到 Python module 的映射 |
| `root_contract_panel` | schema/fixture/report/lockfile/dashboard roots | allowed root coverage |
| `exit_code_panel` | command summaries | exit code、stage effect、problem detail |
| `future_code_batch_panel` | implementation batches | `157` 最小代码模块准备度 |

## Stage Gate Rules

| rule | 条件 | stage effect |
|---|---|---|
| `RCQ-STAGE-155-001` | command manifest 缺任一 `RCQ-155-*` | `repair` |
| `RCQ-STAGE-155-002` | command 缺 owner module、input、output 或 exit code | `repair` |
| `RCQ-STAGE-155-003` | root 未被 allowed root resolver 覆盖 | `quarantine` |
| `RCQ-STAGE-155-004` | command DAG 断裂或循环 | `critical_repair` |
| `RCQ-STAGE-155-005` | dashboard/stage/gap output 缺失 | `hold_for_evidence` |
| `RCQ-STAGE-155-006` | quarantine finding 未阻断 suite exit | `quarantine` |
| `RCQ-STAGE-155-007` | 所有 command spec、root、module、exit、report 齐全 | `promote_growth_window` |

## Smoke Commands

```text
uv run life-reality-runner build-language-action-cross-file-graph \
  --schema-root life_reality_runner/schemas/life_reality/language_action_cross_file \
  --report-root life_reality_runner/reports/life_reality/language_action_cross_file/latest

uv run life-reality-runner build-authority-schema-cross-file-graph \
  --schema-root life_reality_runner/schemas/life_reality/authority_schema_cross_file \
  --report-root life_reality_runner/reports/life_reality/authority_schema_cross_file/latest

uv run life-reality-runner build-birth-readiness-cross-file-graph \
  --schema-root life_reality_runner/schemas/life_reality/birth_readiness_cross_file \
  --report-root life_reality_runner/reports/life_reality/birth_readiness_cross_file/latest

uv run life-reality-runner build-full-archive-cross-file-rollup \
  --docs-index docs/README.md \
  --report-root life_reality_runner/reports/life_reality/full_archive_rollup/latest

uv run life-reality-runner normalize-checker-reports \
  --report-root life_reality_runner/reports/life_reality/checker_report_lockfile/latest

uv run life-reality-runner write-checker-report-lockfile \
  --lockfile-root life_reality_runner/generation/lockfiles \
  --report-root life_reality_runner/reports/life_reality/checker_report_lockfile/latest

uv run life-reality-runner run-cross-file-checker-command-suite \
  --manifest life_reality_runner/reports/life_reality/runner_command_queue/latest/runner_command_queue_manifest.json \
  --report-root life_reality_runner/reports/life_reality/runner_command_queue/latest \
  --strict \
  --json
```

## Test Plan

| test file | 覆盖 |
|---|---|
| `tests/unit/test_runner_command_queue_manifest.py` | `RCQ-155-*` command 覆盖、source docs、life targets |
| `tests/unit/test_command_dag.py` | DAG 顺序、断裂、循环、quarantine propagation |
| `tests/unit/test_command_io_contracts.py` | required inputs/outputs、report paths、root ownership |
| `tests/unit/test_exit_code_mapping.py` | stage effect 到 exit code 的映射 |
| `tests/unit/test_report_normalizer_command.py` | `normalize-checker-reports` 输入输出 |
| `tests/unit/test_checker_report_lockfile_command.py` | lockfile/digest/regression command |
| `tests/smoke/test_cross_file_checker_command_suite.py` | top-level command suite |

## Batch Implementation Order

| batch | 输出 | 依赖 |
|---|---|---|
| `BATCH-155-001 command manifest schema` | runner command queue schema bundle | `123`、`154` |
| `BATCH-155-002 command registry` | `RCQ-155-*` command registry JSON | 本层 |
| `BATCH-155-003 command module skeleton` | `commands/cross_file.py`、`checker_report_lockfile.py`、`runner_command_queue.py` | `136` |
| `BATCH-155-004 checker module mount` | language/authority/birth/full archive checker module entrypoints | `150-153` |
| `BATCH-155-005 report lockfile commands` | normalize/write/digest/regression/dashboard/stage commands | `154` |
| `BATCH-155-006 suite orchestrator` | `run-cross-file-checker-command-suite` | all prior batches |
| `BATCH-155-007 tests and smoke` | unit/smoke test entrypoints | `156`、`157` |

## Cleanup Rules

| rule | 要求 |
|---|---|
| `CLEAN-155-001` | 不允许新增 command 没有 owner module |
| `CLEAN-155-002` | 不允许 command 只有自然语言说明，没有 input/output/report/exit contract |
| `CLEAN-155-003` | 不允许 root 绕过 allowed root resolver |
| `CLEAN-155-004` | 不允许 critical/quarantine finding 被 suite exit code 覆盖成 pass |
| `CLEAN-155-005` | 不允许 dashboard、stage、gap output 脱离 report writer |
| `CLEAN-155-006` | 不允许命令队列脱离九项真实生命目标和 source docs |

## 与下一层连接

`156_life_reality_full_archive_rollup_fixture_materialization_queue.md` 已承接本层：把 runner command queue 的 pass/fail/critical/mutation/smoke fixture family 推进为首批可写入 JSON fixture 队列。

`157_life_reality_cross_file_checker_minimal_code_module_plan.md` 应承接本层和 `156`：把 command queue 与 fixture materialization queue 继续压成最小 Python module、CLI command、schema loader、report normalizer、lockfile writer、dashboard writer、stage gate writer、fixture runner 和 tests。

`158_life_reality_cross_file_checker_repository_bootstrap_plan.md` 应承接 `157`：把最小代码模块计划推进到 `pyproject.toml`、`src/` package、tests、fixtures 和 smoke command bootstrap。

本层完成后，runner command queue 落地链推进为：

`150-154 checker/lockfile/dashboard contracts -> RCQ-155 command registry -> command IO contracts -> command DAG -> module ownership -> exit code mapping -> dashboard source -> stage gate review -> fixture materialization queue -> minimal code module plan`
