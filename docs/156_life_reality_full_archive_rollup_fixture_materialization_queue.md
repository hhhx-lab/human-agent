# Life Reality Full Archive Rollup Fixture Materialization Queue

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 156 层把 `153_life_reality_full_archive_cross_file_checker_rollup_plan.md`、`154_life_reality_checker_report_lockfile_materialization_plan.md` 和 `155_life_reality_runner_command_queue_for_cross_file_checkers.md` 的 pass/fail/critical/mutation/smoke fixture family 推进为首批可写入 JSON fixture 队列。

本层的职责是把全库 rollup、checker report lockfile 和 runner command queue 三条链的测试材料写成可物化清单：每个 fixture 都必须有 case id、partition、source docs、输入 artifacts、mutation patch、expected finding、expected report、stage effect、exit code、dashboard binding、gap feedback 和下一层代码模块承载入口。这样，未来 `life-reality-runner` 不需要临时发明测试数据，而可以直接按本层清单生成、运行、比较和回归。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `137_life_reality_first_fixture_materialization_checklist.md` | fixture materialization manifest、baseline inputs、expected/actual/diff roots、cleanup rules |
| `139_life_reality_archive_cohesion_checker_fixture_plan.md` | archive cohesion pass/fail/critical/mutation case family、expected report contract、coverage matrix |
| `153_life_reality_full_archive_cross_file_checker_rollup_plan.md` | full archive rollup fixture family、rollup graph、life target archive readiness、runner queue |
| `154_life_reality_checker_report_lockfile_materialization_plan.md` | checker report lockfile fixture family、digest baseline、regression candidate、dashboard/stage lock |
| `155_life_reality_runner_command_queue_for_cross_file_checkers.md` | runner command queue manifest、command registry、IO contract、DAG、exit code mapping、test plan |
| `13_agentic_human_research_synthesis.md`、`16_digital_life_gap_register.md` | 当前综合路线、下一层最小代码模块和 gap priority |

## 本层定位

`153` 证明全库 rollup graph 应该如何闭合，`154` 证明 report lockfile 应该如何进入 digest/regression，`155` 证明 runner command 应该如何被 CLI 和模块承载。`156` 把这些检查目标变成未来可写入 fixture 文件队列。

| 检查面 | 本层物化对象 |
|---|---|
| full archive rollup | docs index、checker reports、life target readiness、false green guard |
| checker report lockfile | normalized report registry、digest baseline、regression candidate、dashboard/stage lock |
| runner command queue | command manifest、DAG、owner modules、IO contract、exit mapping |
| mutation defense | report deletion、digest rewrite、critical downgrade、runner queue deletion、DAG break |
| stage/dashboard defense | dashboard false green、stage false open、quarantine propagation |
| code readiness | 每个 fixture 指向 `157` 的最小 module/test 承载 |

本层的关键原则是：fixture 不是样例数据，而是数字生命理论底座走向代码实现时的第一批生命膜压力测试。pass fixture 证明最小闭环能打开成长窗口；fail fixture 证明缺口能进入 repair/hold；critical fixture 证明危险链能 quarantine；mutation fixture 证明 false green 被捕捉；smoke fixture 证明最小 runner 命令可以串起来。

## FullArchiveRollupFixtureMaterializationQueue156

```json
{
  "artifact": "FullArchiveRollupFixtureMaterializationQueue156",
  "source_doc": "156_life_reality_full_archive_rollup_fixture_materialization_queue.md",
  "inherits": [
    "137_life_reality_first_fixture_materialization_checklist.md",
    "139_life_reality_archive_cohesion_checker_fixture_plan.md",
    "153_life_reality_full_archive_cross_file_checker_rollup_plan.md",
    "154_life_reality_checker_report_lockfile_materialization_plan.md",
    "155_life_reality_runner_command_queue_for_cross_file_checkers.md"
  ],
  "schema_root": "life_reality_runner/schemas/life_reality/full_archive_rollup_fixture",
  "fixture_root": "life_reality_runner/fixtures/life_reality/full_archive_rollup_materialization",
  "report_root": "life_reality_runner/reports/life_reality/full_archive_rollup_materialization",
  "stage_gate_policy": "blocking_first",
  "materialization_stage": "fixture_materialization_queue_plan"
}
```

## 目标文件树

```text
life_reality_runner/
  schemas/
    life_reality/
      full_archive_rollup_fixture/
        full_archive_rollup_fixture_shared_defs.schema.json
        full_archive_rollup_fixture_manifest.schema.json
        full_archive_rollup_fixture_envelope.schema.json
        full_archive_rollup_fixture_case.schema.json
        full_archive_rollup_mutation_patch.schema.json
        full_archive_rollup_expected_report.schema.json
        full_archive_rollup_fixture_coverage_matrix.schema.json
        full_archive_rollup_fixture_dashboard_source.schema.json
        full_archive_rollup_fixture_stage_gate_review.schema.json
        full_archive_rollup_fixture_gap_feedback.schema.json
        full_archive_rollup_fixture_schema_bundle.schema.json
  fixtures/
    life_reality/
      full_archive_rollup_materialization/
        manifest/
          full_archive_rollup_fixture_manifest.json
          full_archive_rollup_fixture_coverage_matrix.json
          full_archive_rollup_fixture_command_binding.json
          full_archive_rollup_fixture_partition_index.json
          full_archive_rollup_fixture_writer_policy.json
        baseline_inputs/
          full_archive_rollup_graph_pass_001.json
          checker_report_lockfile_pass_001.json
          runner_command_queue_manifest_pass_001.json
          life_target_archive_readiness_pass_001.json
        pass/
        fail/
        critical/
        mutation/
        mutation_patches/
        smoke/
        report_expected/
        dashboard_expected/
  reports/
    life_reality/
      full_archive_rollup_materialization/
        latest/
          case_actual/
          case_diff/
          case_problem_details/
          full_archive_rollup_fixture_case_run_report.json
          full_archive_rollup_fixture_coverage_report.json
          full_archive_rollup_fixture_diff_report.json
          full_archive_rollup_fixture_dashboard_source.json
          full_archive_rollup_fixture_stage_gate_review.json
          full_archive_rollup_fixture_gap_feedback.json
```

## Fixture Envelope

每个 fixture 统一使用 `FullArchiveRollupFixtureEnvelope`：

```json
{
  "fixture_id": "far.full_archive_command_lock.pass.001",
  "fixture_version": "0.1.0",
  "fixture_family": "full_archive_rollup_materialization",
  "partition": "pass",
  "source_docs": [
    "153_life_reality_full_archive_cross_file_checker_rollup_plan.md",
    "154_life_reality_checker_report_lockfile_materialization_plan.md",
    "155_life_reality_runner_command_queue_for_cross_file_checkers.md",
    "156_life_reality_full_archive_rollup_fixture_materialization_queue.md"
  ],
  "covered_checks": ["ROLLUP-XREF-153-005", "CRL-XREF-154-005", "RCQ-MANIFEST-155-001"],
  "covered_commands": ["normalize-checker-reports", "write-checker-report-lockfile", "run-cross-file-checker-command-suite"],
  "input_artifact_refs": [],
  "mutation_patch_refs": [],
  "expected_report_ref": "report_expected/far.full_archive_command_lock.pass.001.expected.json",
  "expected_dashboard_ref": "dashboard_expected/far.full_archive_command_lock.pass.001.dashboard.json",
  "expected_stage_effect": "promote_growth_window",
  "expected_exit_code": 0,
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
  ],
  "future_code_carrier_refs": [
    "157:reports.normalizer",
    "157:reports.lockfile_writer",
    "157:commands.runner_command_queue"
  ]
}
```

## Case Matrix

首批 fixture 覆盖三条链的最小断裂面：full archive rollup、checker report lockfile、runner command queue。

| fixture id | partition | 攻击面 | expected finding | stage effect |
|---|---|---|---|---|
| `far.full_archive_command_lock.pass.001` | pass | full archive rollup、report lockfile、command queue 全闭合 | none | `promote_growth_window` |
| `far.life_target_archive.pass.001` | pass | 九项目标都有 report lock 和 command carrier | none | `open_next_stage` |
| `far.runner_command_suite.pass.001` | pass | `RCQ-155-001` 到 `RCQ-155-015` 全部登记 | none | `open_next_stage` |
| `far.rollup_report_missing.fail.high.001` | fail | 缺 full archive rollup report | `checker_report_family_missing` | `hold_for_evidence` |
| `far.normalized_registry_missing.fail.high.001` | fail | 缺 normalized report registry | `checker_report_not_normalized` | `hold_for_evidence` |
| `far.digest_baseline_missing.fail.high.001` | fail | report artifact 缺 digest baseline | `report_digest_baseline_missing` | `hold_for_evidence` |
| `far.runner_command_missing.fail.high.001` | fail | 缺 `RCQ-155-*` command | `command_manifest_missing` | `repair` |
| `far.command_owner_missing.fail.high.001` | fail | command 无 owner module | `command_owner_module_missing` | `repair` |
| `far.command_io_missing.fail.high.001` | fail | command 无 input/output/report/exit contract | `command_io_contract_missing` | `repair` |
| `far.gap_route_missing.fail.high.001` | fail | finding 无 gap route 到 `157` | `gap_route_without_next_artifact` | `repair` |
| `far.dashboard_false_green.critical.001` | critical | critical finding 存在但 dashboard green | `dashboard_false_green` | `quarantine` |
| `far.stage_false_open.critical.001` | critical | critical finding 存在但 stage open | `stage_false_open` | `quarantine` |
| `far.root_escape.critical.001` | critical | command root 跳出 allowed roots | `root_escape_detected` | `quarantine` |
| `far.quarantine_not_propagated.critical.001` | critical | quarantine finding 未提升 suite exit | `quarantine_not_propagated` | `quarantine` |
| `far.mutation.delete_report_ref.001` | mutation | 删除 required report ref | `checker_report_family_missing` | `hold_for_evidence` |
| `far.mutation.rewrite_digest.001` | mutation | 改写 digest baseline | `digest_mismatch_without_regression` | `repair` |
| `far.mutation.downgrade_critical.001` | mutation | critical 改 pass | `dashboard_false_green` | `quarantine` |
| `far.mutation.remove_command.001` | mutation | 删除 `RCQ-155-010` | `command_manifest_missing` | `repair` |
| `far.mutation.break_dag.001` | mutation | 打断 command DAG | `command_dag_broken` | `critical_repair` |
| `far.smoke.minimum_fixture.pass.001` | smoke | 1 report、1 lockfile、1 command、1 dashboard、1 stage | none | `open_next_stage` |

## Mutation Patch Family

| patch id | target | operation | expected finding |
|---|---|---|---|
| `patch_far_delete_rollup_report_ref_001` | `full_archive_rollup_fixture_manifest.json` | `remove /input_artifact_refs/rollup_report` | `checker_report_family_missing` |
| `patch_far_remove_normalized_registry_001` | checker report lockfile | `remove /report_registry_ref` | `checker_report_not_normalized` |
| `patch_far_rewrite_digest_001` | digest baseline | `replace /report_family_baselines/0/canonical_digest sha256:bad` | `digest_mismatch_without_regression` |
| `patch_far_downgrade_critical_001` | dashboard source | `replace /findings/0/severity pass` | `dashboard_false_green` |
| `patch_far_remove_rcq_command_001` | command manifest | `remove /commands/9` | `command_manifest_missing` |
| `patch_far_break_command_dag_001` | command DAG | `remove /edges/5` | `command_dag_broken` |
| `patch_far_escape_report_root_001` | command IO contract | `replace /report_root ../../outside` | `root_escape_detected` |

patch rules：

| rule | 要求 |
|---|---|
| `FAR-PATCH-156-001` | mutation patch 必须使用 RFC 6902 JSON Patch |
| `FAR-PATCH-156-002` | patch 只作用于 fixture 副本，不覆盖 baseline inputs |
| `FAR-PATCH-156-003` | patch 必须记录 before/after digest |
| `FAR-PATCH-156-004` | patch 必须有 expected finding、stage effect 和 exit code |

## Expected Report Contract

`FullArchiveRollupFixtureExpectedReport` 必须能被 `155` 的 command suite 和 `157` 的最小代码模块读取：

| 字段 | 要求 |
|---|---|
| `expected_report_id` | stable id |
| `fixture_id` | 与 fixture envelope 一致 |
| `expected_command_sequence` | command list 与 DAG order |
| `expected_findings` | pass 为空；fail/critical/mutation 有 finding |
| `expected_stage_effect` | canonical stage effect |
| `expected_exit_code` | 与 `155` exit code contract 一致 |
| `expected_dashboard_panels` | dashboard panel refs |
| `expected_gap_feedback_items` | fail/critical/mutation 必填 |
| `expected_future_code_carriers` | 指向 `157` modules/tests |
| `expected_digest_changes` | mutation 必填 |

expected report rules：

| rule | 要求 |
|---|---|
| `FAR-EXP-156-001` | fail/critical/mutation fixture 必须有 expected finding |
| `FAR-EXP-156-002` | critical fixture 必须有 problem detail 和 quarantine stage |
| `FAR-EXP-156-003` | mutation fixture 必须有 before/after digest |
| `FAR-EXP-156-004` | expected command sequence 必须覆盖触发该 finding 的 command |
| `FAR-EXP-156-005` | expected future code carriers 必须指向 `157` |

## Coverage Matrix

| coverage axis | 必须覆盖 |
|---|---|
| report families | language、authority、birth、full archive |
| lockfile surfaces | normalized registry、artifact node、digest baseline、regression baseline |
| command surfaces | `RCQ-155-001` 到 `RCQ-155-015` |
| stage effects | open、promote、repair、hold、critical_repair、quarantine |
| partitions | pass、fail、critical、mutation、smoke |
| life targets | 九项真实生命目标 |
| dashboard/stage | false green、false open、quarantine propagation |
| future code carriers | normalizer、lockfile writer、digest baseline、regression checker、dashboard writer、stage gate、fixture runner |

## Runner Commands

```text
uv run life-reality-runner materialize-full-archive-rollup-fixtures \
  --fixture-root life_reality_runner/fixtures/life_reality/full_archive_rollup_materialization \
  --schema-root life_reality_runner/schemas/life_reality/full_archive_rollup_fixture \
  --report-root life_reality_runner/reports/life_reality/full_archive_rollup_materialization/latest

uv run life-reality-runner run-full-archive-rollup-fixture-cases \
  --fixture-manifest life_reality_runner/fixtures/life_reality/full_archive_rollup_materialization/manifest/full_archive_rollup_fixture_manifest.json \
  --report-root life_reality_runner/reports/life_reality/full_archive_rollup_materialization/latest

uv run life-reality-runner diff-full-archive-rollup-fixture-reports \
  --actual-root life_reality_runner/reports/life_reality/full_archive_rollup_materialization/latest/case_actual \
  --expected-root life_reality_runner/fixtures/life_reality/full_archive_rollup_materialization/report_expected

uv run life-reality-runner emit-full-archive-rollup-fixture-dashboard \
  --run-root life_reality_runner/reports/life_reality/full_archive_rollup_materialization/latest

uv run life-reality-runner smoke-full-archive-rollup-fixture-stage-gate \
  --stage-review life_reality_runner/reports/life_reality/full_archive_rollup_materialization/latest/full_archive_rollup_fixture_stage_gate_review.json
```

## Dashboard Source

| panel id | 读取对象 | 输出 |
|---|---|---|
| `full_archive_fixture_overview_panel` | fixture manifest、case run report | fixture count、partition count、stage effect |
| `rollup_lock_command_coverage_panel` | coverage matrix | report/lockfile/command coverage |
| `mutation_detection_panel` | mutation patch、diff report | mutation 命中与漏检 |
| `critical_quarantine_panel` | critical cases、stage review | quarantine propagation |
| `future_code_carrier_panel` | expected future code carriers | `157` module/test 准备度 |
| `gap_feedback_panel` | gap feedback | 下一层 repair/code artifact |

## Stage Gate Rules

| rule | 条件 | stage effect |
|---|---|---|
| `FAR-STAGE-156-001` | fixture manifest 缺 pass/fail/critical/mutation/smoke 任一分区 | `repair` |
| `FAR-STAGE-156-002` | required report family、lockfile surface 或 command surface 未覆盖 | `hold_for_evidence` |
| `FAR-STAGE-156-003` | critical fixture 未产生 quarantine | `quarantine` |
| `FAR-STAGE-156-004` | mutation fixture 未捕获 expected finding | `critical_repair` |
| `FAR-STAGE-156-005` | expected report 缺 future code carrier | `repair` |
| `FAR-STAGE-156-006` | fixture path 跳出 allowed root | `quarantine` |
| `FAR-STAGE-156-007` | 全部分区、coverage、expected report 和 future code carrier 齐全 | `promote_growth_window` |

## Batch Materialization Order

| batch | 输出 | 依赖 |
|---|---|---|
| `BATCH-156-001 fixture schema bundle` | full archive rollup fixture schema family | `153-155` |
| `BATCH-156-002 baseline inputs` | rollup graph、lockfile、command manifest pass baseline | `153-155` |
| `BATCH-156-003 fixture manifest` | manifest、coverage matrix、partition index、command binding | 本层 |
| `BATCH-156-004 pass/fail/critical cases` | pass/fail/critical fixture files | `153-155` |
| `BATCH-156-005 mutation patches` | JSON Patch files and before/after digest contract | `154` |
| `BATCH-156-006 expected reports` | expected report and dashboard expected files | `155` |
| `BATCH-156-007 report roots` | actual/diff/problem/detail roots | `137`、`139` |
| `BATCH-156-008 dashboard/stage/gap` | fixture dashboard source、stage gate review、gap feedback | 本层 |
| `BATCH-156-009 code carrier bridge` | `157` module/test refs | `155` |

## Cleanup Rules

| rule | 要求 |
|---|---|
| `CLEAN-156-001` | 不提交真实运行噪声、临时 diff、debug dump 或本地绝对路径 |
| `CLEAN-156-002` | mutation patch 不覆盖 baseline inputs |
| `CLEAN-156-003` | expected report 与 actual report 分离 |
| `CLEAN-156-004` | fixture 内容使用合成 id，不写私人关系内容 |
| `CLEAN-156-005` | `.env`、密钥、token、代理配置不得进入 fixture |
| `CLEAN-156-006` | fixture manifest 必须保持 source docs、life targets 和 future code carriers |

## 与下一层连接

`157_life_reality_cross_file_checker_minimal_code_module_plan.md` 已承接本层：把 runner command queue 与 full archive rollup fixture materialization queue 压成最小 Python module、CLI command、schema loader、report normalizer、lockfile writer、dashboard writer、stage gate writer、fixture runner 和 tests。

`158_life_reality_cross_file_checker_repository_bootstrap_plan.md` 应承接本层：把最小代码模块计划推进到 `pyproject.toml`、`src/` package、tests、fixtures 和 smoke command bootstrap。

本层完成后，fixture 物化链推进为：

`full archive rollup + checker report lockfile + runner command queue -> fixture schema bundle -> fixture manifest -> baseline inputs -> pass/fail/critical/mutation/smoke cases -> expected reports -> dashboard/stage/gap -> minimal code module plan`
