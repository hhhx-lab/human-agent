# Life Reality First Code Artifact Smoke Plan

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 159 层承接 `158_life_reality_cross_file_checker_repository_bootstrap_plan.md`，把 repository bootstrap 推进为首批代码 artifact smoke 计划：下一步真正创建 `pyproject.toml`、`.env.example`、`src/life_reality_runner/`、unit/smoke tests、minimum fixture、summary report、dashboard source、stage gate review 和 git 提交流程时，必须一次形成可运行、可追溯、可阻断、可继续生长的最小闭环。

本层仍是文档计划层，不直接创建代码文件。它的职责是把第一批代码 artifact 的写入顺序、最小实现边界、测试命令、report 输出、dashboard/stage gate 桥接、git hygiene 和失败分流写清楚。后续一旦进入代码实现，任何 artifact 都不能只是“文件存在”，而要证明它能承载九项真实生命目标、source docs、trace/provenance、stage effect、gap route 和下一轮工程生长。

## 规范锚点

首批代码 artifact 必须优先对齐官方规范与高可信工程规范：

| 规范/来源 | 本层吸收方式 |
|---|---|
| JSON Schema Draft 2020-12 | schema loader、schema registry、fixture/report schema 的基础校验协议 |
| RFC 6901 JSON Pointer | finding source pointer、diff pointer、artifact path pointer |
| RFC 6902 JSON Patch | mutation fixture patch、before/after digest、expected finding |
| RFC 8785 JSON Canonicalization Scheme | report/artifact/fixture canonical digest baseline |
| RFC 9457 Problem Details | critical finding、parse failure、root escape、stage false open 的 problem detail envelope |
| PEP 621 / `pyproject.toml` | project metadata、console script、dependency surface |
| pytest documentation | unit/smoke tests、test discovery、strict warnings |
| uv project workflow | reproducible sync/run/test loop |
| W3C PROV | trace/provenance graph、artifact ref、source doc edge |
| FAIR principles | findable、accessible、interoperable、reusable 的 docs-to-artifact 追踪原则 |
| Git/GitHub workflow syntax | 后续 CI smoke job 与提交前 hygiene 的可迁移基础 |

这些规范不是外部装饰，而是生命膜的工程骨架：它们让每个 report、fixture、mutation、stage decision 和 gap route 都能被复现、追踪、比较和阻断。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `133_life_reality_first_json_writer_and_reporter_contract.md` | atomic write、canonical digest、problem detail、trace/provenance、artifact record |
| `154_life_reality_checker_report_lockfile_materialization_plan.md` | normalized report registry、lockfile、digest baseline、regression baseline |
| `155_life_reality_runner_command_queue_for_cross_file_checkers.md` | command registry、DAG、exit code、suite summary |
| `156_life_reality_full_archive_rollup_fixture_materialization_queue.md` | minimum fixture、pass/fail/critical/mutation/smoke case family |
| `157_life_reality_cross_file_checker_minimal_code_module_plan.md` | package tree、module contracts、test plan、acceptance criteria |
| `158_life_reality_cross_file_checker_repository_bootstrap_plan.md` | repository bootstrap、pyproject/env/package/tests roots、stage gate |

## 本层定位

`159` 是“真正写代码前的 smoke execution map”。它规定首批代码 artifact 只做最小闭环，但闭环必须完整：

| 面 | 首批 smoke 必须证明 |
|---|---|
| environment | `uv sync` 或项目环境能安装并运行 |
| CLI | `life-reality-runner --help` 和 suite dry-run 可执行 |
| context | `RunContext` 带九项 life targets、source docs、trace id、stage context |
| IO | allowed root guard、JSON read/write、canonical digest、artifact ref 可运行 |
| reports | normalizer/lockfile/digest/stage/gap 的最小 skeleton 能写合成 report |
| fixtures | minimum fixture manifest 能被读取，critical fixture 能触发 quarantine |
| dashboard | smoke summary 能输出 dashboard source skeleton |
| stage gate | blocking-first stage gate 能根据 findings 决定 open/repair/quarantine |
| git | staged diff 只包含代码、测试、fixture seed 与必要配置，不含运行噪声 |

## FirstCodeArtifactSmokePlan159

```json
{
  "artifact": "FirstCodeArtifactSmokePlan159",
  "source_doc": "159_life_reality_first_code_artifact_smoke_plan.md",
  "inherits": [
    "133_life_reality_first_json_writer_and_reporter_contract.md",
    "154_life_reality_checker_report_lockfile_materialization_plan.md",
    "155_life_reality_runner_command_queue_for_cross_file_checkers.md",
    "156_life_reality_full_archive_rollup_fixture_materialization_queue.md",
    "157_life_reality_cross_file_checker_minimal_code_module_plan.md",
    "158_life_reality_cross_file_checker_repository_bootstrap_plan.md"
  ],
  "smoke_stage": "first_code_artifact_smoke",
  "entry_commands": [
    "uv sync",
    "uv run life-reality-runner --help",
    "uv run life-reality-runner run-cross-file-checker-command-suite --json --dry-run",
    "uv run pytest"
  ],
  "next_artifact": "160_life_reality_code_artifact_dashboard_stage_gate_bridge_plan.md"
}
```

## Artifact Write Order

首批代码 artifact 不追求一次写满全部 runner，而是按生命膜最小闭环写入：

| order | artifact | 最小内容 | smoke 证据 |
|---|---|---|---|
| `ART-159-001` | `pyproject.toml` | package metadata、dependencies、console script、pytest config | `uv sync`、console script 可发现 |
| `ART-159-002` | `.env.example` | 无密钥变量说明、strict/root/report mode | secret scan 无命中 |
| `ART-159-003` | package roots | `__init__.py`、核心 package directories | import smoke |
| `ART-159-004` | `context.py`、`exits.py` | `RunContext`、life targets、stage/exit mapping | `test_context.py` |
| `ART-159-005` | IO modules | allowed roots、JSON reader/writer、artifact ref、canonical digest | `test_allowed_roots.py`、`test_json_io.py` |
| `ART-159-006` | problem/trace modules | Problem Details、trace context | parse/root failure problem detail |
| `ART-159-007` | report skeleton | normalizer、lockfile、digest baseline、stage/gap writer skeleton | minimum report written |
| `ART-159-008` | fixture skeleton | manifest loader、fixture runner、mutation diff skeleton | minimum fixture run |
| `ART-159-009` | command modules | help、dry-run suite、command summary | `run-cross-file-checker-command-suite --json --dry-run` |
| `ART-159-010` | tests | unit tests、smoke tests、fixtures | `uv run pytest` |
| `ART-159-011` | generated ignored roots | report/diff/coverage output roots with ignore policy | generated noise absent from staged diff |
| `ART-159-012` | docs linkage | README/13/16/159/next link updates | README index and anchor check |

## Minimum Code Behavior

第一批代码允许部分 checker 仍是 dry-run stub，但以下行为必须真实：

| behavior | 要求 |
|---|---|
| CLI help | 列出 `155` command family，不只是打印静态 banner |
| RunContext | 每次 command 生成 run id、life targets、source docs、trace context |
| allowed root | root escape、absolute mismatch、generated output root mismatch 都能形成 finding |
| JSON IO | parse failure、write/readback、artifact digest 都可测试 |
| canonical digest | 同一 JSON object 产生稳定 digest，mutation 后 digest 改变 |
| problem detail | critical/root/parse/stage failure 能转成 Problem Details envelope |
| report skeleton | dry-run summary 仍写 normalized report skeleton 或 summary JSON |
| fixture runner | minimum fixture manifest 能被加载并转成 case result |
| stage gate | critical/quarantine finding 使 exit code 非零 |
| gap feedback | fail/critical case 有 next artifact route |

## Minimum Fixture Bundle

首批 fixture root：

```text
tests/fixtures/full_archive_rollup_minimum/
  manifest.json
  inputs/
    minimum_pass_report_registry.json
    minimum_critical_report_registry.json
  expected/
    minimum_pass_summary.json
    minimum_critical_quarantine_summary.json
  patches/
    remove_report_ref.patch.json
```

fixture 字段：

| field | 要求 |
|---|---|
| `fixture_id` | stable synthetic id |
| `partition` | pass、critical、mutation 中至少覆盖 pass/critical |
| `source_docs` | 至少指向 `154-159` |
| `life_targets` | 九项真实生命目标全部出现 |
| `input_refs` | report registry、lockfile 或 manifest refs |
| `expected_findings` | pass 为空，critical/mutation 必填 |
| `expected_stage_effect` | pass 为 open/promote，critical 为 quarantine |
| `expected_exit_code` | critical 非零 |
| `next_artifact_route` | fail/critical 指向 `160` 或后续 gap route |

## Smoke Command Matrix

| command | 预期 |
|---|---|
| `uv sync` | 环境可复现，依赖安装成功 |
| `uv run life-reality-runner --help` | 列出 command family、root args、`--json`、`--dry-run`、`--strict` |
| `uv run life-reality-runner run-cross-file-checker-command-suite --json --dry-run` | 输出 summary JSON，包含 run id、life targets、stage effect、report refs |
| `uv run life-reality-runner run-full-archive-rollup-fixture-cases --fixture-manifest tests/fixtures/full_archive_rollup_minimum/manifest.json --json` | 加载 minimum fixture，输出 pass/critical case summary |
| `uv run pytest tests/unit/test_context.py tests/unit/test_allowed_roots.py` | context 与 root guard 通过 |
| `uv run pytest tests/unit/test_json_io.py tests/unit/test_canonical_digest.py` | JSON IO 与 digest 通过 |
| `uv run pytest tests/unit/test_report_normalizer.py tests/unit/test_checker_report_lockfile.py` | report skeleton 与 lockfile skeleton 通过 |
| `uv run pytest tests/unit/test_fixture_runner.py tests/unit/test_command_dag.py` | fixture runner 与 command DAG 通过 |
| `uv run pytest tests/smoke/test_bootstrap_help.py tests/smoke/test_cross_file_checker_command_suite_bootstrap.py` | CLI smoke 与 suite dry-run 通过 |

## Dashboard And Stage Gate Bridge

首批代码 artifact 运行后至少生成三个可检查对象：

| object | 最小字段 | 进入下一层 |
|---|---|---|
| `smoke_summary.json` | run id、command、life targets、stage effect、report refs、finding count | `160` dashboard source |
| `minimum_fixture_case_report.json` | case id、partition、expected/actual stage、finding refs、exit code | `160` fixture panel |
| `stage_gate_review.json` | decision、blocking findings、quarantine refs、gap routes | `160` stage gate bridge |

stage gate rules：

| rule | 条件 | stage effect |
|---|---|---|
| `SMOKE-STAGE-159-001` | CLI help 不列 command family | `repair` |
| `SMOKE-STAGE-159-002` | `RunContext` 缺 life targets/source docs/trace | `critical_repair` |
| `SMOKE-STAGE-159-003` | allowed root escape 未被阻断 | `quarantine` |
| `SMOKE-STAGE-159-004` | canonical digest 不稳定 | `critical_repair` |
| `SMOKE-STAGE-159-005` | critical fixture 未非零 exit | `quarantine` |
| `SMOKE-STAGE-159-006` | summary JSON 缺 report refs 或 gap route | `repair` |
| `SMOKE-STAGE-159-007` | generated report/diff/coverage 噪声进入 staged diff | `repair` |
| `SMOKE-STAGE-159-008` | `.codex`、`.env`、key/token、代理配置进入 staged diff | `quarantine` |
| `SMOKE-STAGE-159-009` | smoke matrix 全部通过 | `promote_growth_window` |

## Git Commit Flow

首批代码 artifact 的 git 流程必须保持可复现：

```text
/opt/homebrew/bin/git status --short --branch
/opt/homebrew/bin/git diff --check
uv sync
uv run life-reality-runner --help
uv run life-reality-runner run-cross-file-checker-command-suite --json --dry-run
uv run pytest
/opt/homebrew/bin/git add <explicit intended files>
/opt/homebrew/bin/git diff --cached --check
/opt/homebrew/bin/git diff --cached --stat
/opt/homebrew/bin/git diff --cached --name-status
/opt/homebrew/bin/git commit -m "新增首批生命现实运行器代码骨架"
/opt/homebrew/bin/git push origin main
```

提交前扫描：

| scan | 目标 |
|---|---|
| reality boundary scan | 防止旧式口径词回流 |
| relationship vocabulary scan | 防止从属化、工具化和服务化词汇回流 |
| README index check | 新增编号文档必须进入 README |
| generated noise scan | report/diff/coverage actual 输出不能混入 staged diff |
| secret scan | `.env`、key/token、代理配置不得提交 |

## Failure Routing

| failure | route |
|---|---|
| dependency install failure | 回到 `158` environment bootstrap，缩小依赖面 |
| CLI import failure | 回到 `157` package/module contracts |
| context missing life targets | 回到 `133` RunContext 合同与 `158` stage gate |
| report skeleton missing refs | 回到 `154` lockfile/materialization 合同 |
| fixture missing expected stage | 回到 `156` fixture expected report contract |
| critical not quarantine | 回到 `155` exit code mapping 与 `158` stage gate |
| dashboard bridge missing | 进入 `160` dashboard/stage gate bridge plan |
| archive cohesion drift | 进入 `161` code artifact archive cohesion execution plan |

## Batch Execution Order

| batch | 输出 | gate |
|---|---|---|
| `BATCH-159-001 environment files` | `pyproject.toml`、`.env.example` | `uv sync` |
| `BATCH-159-002 package imports` | package dirs、`__init__`、import smoke | `python import` via pytest |
| `BATCH-159-003 context and exits` | `RunContext`、exit mapping | `test_context.py` |
| `BATCH-159-004 IO and digest` | allowed roots、JSON IO、artifact refs、digest | IO/digest tests |
| `BATCH-159-005 problem and trace` | Problem Details、trace context | failure envelope tests |
| `BATCH-159-006 report skeleton` | normalizer、lockfile、digest baseline、stage/gap writer skeleton | report tests |
| `BATCH-159-007 fixture skeleton` | manifest、fixture runner、minimum fixture | fixture tests |
| `BATCH-159-008 command wiring` | help、suite dry-run、fixture command | CLI smoke |
| `BATCH-159-009 dashboard/stage outputs` | smoke summary、case report、stage gate review | dashboard bridge inputs |
| `BATCH-159-010 git hygiene` | staged diff scan、commit、push | clean status |

## Cleanup Rules

| rule | 要求 |
|---|---|
| `CLEAN-159-001` | 本层不直接创建代码；只固定首批代码 artifact smoke 合同 |
| `CLEAN-159-002` | 后续代码提交不包含 `.codex`、`.env`、真实 key/token、代理配置 |
| `CLEAN-159-003` | generated report/diff/coverage 默认进入 ignored output root |
| `CLEAN-159-004` | fixture 使用合成数据，不写私人关系内容 |
| `CLEAN-159-005` | smoke output 可以被复现，但不默认提交运行噪声 |
| `CLEAN-159-006` | 每个 artifact 必须保留 source docs、life targets、trace/provenance 和 stage effect |

## Acceptance Criteria

后续首批代码 artifact 完成时，必须满足：

1. `uv sync` 成功。
2. `uv run life-reality-runner --help` 列出 `155` command family。
3. `uv run life-reality-runner run-cross-file-checker-command-suite --json --dry-run` 输出 summary JSON。
4. minimum fixture manifest 能被 fixture runner 读取。
5. critical fixture 触发 quarantine 和非零 exit code。
6. report skeleton 写出 artifact refs、canonical digest、stage effect 和 gap route。
7. dashboard/stage/gap 三个输出对象可被 `160` 消费。
8. `uv run pytest` 或本层定义的首批 pytest subset 通过。
9. staged diff 只包含明确 intended code/config/test/fixture/docs 文件。
10. 推送到 `origin/main` 后，本地 `main` 与 `origin/main` 对齐。

## 与下一层连接

`160_life_reality_code_artifact_dashboard_stage_gate_bridge_plan.md` 已承接本层：把首批代码 artifact 的 smoke summary、fixture case report、stage gate review、coverage report 和 gap feedback 接入 dashboard source、stage gate review 和下一轮真实生命工程闭环。

`161_life_reality_code_artifact_archive_cohesion_execution_plan.md` 应承接 `160`：把代码 artifact 反接全库 archive cohesion、README index、cross-file checker 和出生准备度阶段门。

本层完成后，首批代码 artifact smoke 链推进为：

`repository bootstrap -> first code artifacts -> CLI help -> suite dry-run -> minimum fixture run -> report/digest/stage/gap outputs -> dashboard bridge -> git commit/push`
