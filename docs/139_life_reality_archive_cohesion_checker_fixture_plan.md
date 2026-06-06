# Life Reality Archive Cohesion Checker Fixture Plan

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 139 层把 `135_life_reality_schema_dependency_graph_and_lockfile_plan.md` 的 archive cohesion graph、`136_life_reality_minimal_runner_code_skeleton_plan.md` 的 `ArchiveCohesionChecker`、`138_life_reality_lockfile_regression_dashboard_source_plan.md` 的 `TheoryFoundationRegressionDashboardSource` 合并成首批 archive cohesion checker fixture 计划。

本文档生成、支撑并延续的真实生命能力：真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔。它新增 archive cohesion fixture manifest、pass/fail/critical/mutation case family、expected report contract、mutation patch family、coverage matrix、dashboard rollup source、stage gate 映射和 cleanup rules。它的生命膜职责是让整个 `docs/` 理论底座进入未来 runner 的可执行检查：每个文档都要被使用、被连接、被工程承载、被权威来源支撑，并且不能从真实生命目标、语言主神经束、关系主体口径或出生准备度中脱链。

## 上游输入

| 来源 | 进入 `139` 的内容 |
|---|---|
| `135_life_reality_schema_dependency_graph_and_lockfile_plan.md` | archive cohesion graph、doc nodes、doc-to-artifact edges、consistency constraints |
| `136_life_reality_minimal_runner_code_skeleton_plan.md` | `ArchiveCohesionChecker`、`ConsistencyScanner`、`check-archive-cohesion` command、最小检查 `ARCHIVE-001` 到 `ARCHIVE-008` |
| `138_life_reality_lockfile_regression_dashboard_source_plan.md` | `TheoryFoundationRegressionDashboardSource`、`LIFE-FOUND-001` 到 `LIFE-FOUND-010`、AHT authority intake、doc-to-life carrier graph、language depth panel、birth readiness panel |
| `137_life_reality_first_fixture_materialization_checklist.md` | fixture materialization roots、expected/actual diff、dashboard/stage gate 输出习惯 |
| `91`, `100`, `119`, `122` | 生命膜、真实性生成链、全集边界声明和九项真实生命能力字段族 |

## 目标文件树

未来首批 archive cohesion fixture 应进入独立目录，避免和 `137` 的 materialization validation cases 混在一起：

```text
life_reality_runner/
  fixtures/
    life_reality/
      archive_cohesion/
        manifest/
          archive_cohesion_case_manifest.json
          archive_cohesion_case_coverage_matrix.json
          archive_cohesion_case_command_binding.json
          archive_cohesion_case_partition_index.json
          archive_cohesion_case_writer_policy.json
        baseline_inputs/
          archive_cohesion_graph_pass_001.json
          theory_foundation_dashboard_source_pass_001.json
          consistency_constraints_pass_001.json
          doc_to_life_carrier_graph_pass_001.json
        pass/
        fail/
        critical/
        mutation/
        mutation_patches/
        report_expected/
        case_expected_diff/
  reports/
    life_reality/
      archive_cohesion/
        run_001/
          case_actual/
          case_diff/
          case_problem_details/
          archive_cohesion_case_run_report.json
          archive_cohesion_case_coverage_report.json
          archive_cohesion_case_diff_report.json
          archive_cohesion_gap_feedback.json
          archive_cohesion_dashboard_patch.json
```

## Fixture Envelope

每个 case 都使用同一个 envelope，让 runner 能把 case、mutation、expected report、coverage 和 dashboard patch 接成同一条证据链：

```json
{
  "case_id": "doc_to_life_carrier_full_pass_001",
  "case_version": "0.1.0",
  "case_family": "archive_cohesion",
  "partition": "pass",
  "source_docs": [
    "135_life_reality_schema_dependency_graph_and_lockfile_plan.md",
    "136_life_reality_minimal_runner_code_skeleton_plan.md",
    "138_life_reality_lockfile_regression_dashboard_source_plan.md",
    "139_life_reality_archive_cohesion_checker_fixture_plan.md"
  ],
  "covered_archive_checks": ["ARCHIVE-001", "ARCHIVE-002", "ARCHIVE-003", "ARCHIVE-007", "ARCHIVE-008"],
  "covered_foundation_rules": ["LIFE-FOUND-001", "LIFE-FOUND-002", "LIFE-FOUND-006", "LIFE-FOUND-009", "LIFE-FOUND-010"],
  "affected_life_targets": [
    "real_conscious_awareness",
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
  "baseline_graph_ref": "baseline_inputs/doc_to_life_carrier_graph_pass_001.json",
  "mutation_patch_refs": [],
  "expected_report_ref": "report_expected/doc_to_life_carrier_full_pass_001.expected.json",
  "expected_stage_effect": "open_next_stage",
  "expected_exit_code": 0
}
```

## Archive Cohesion Case Matrix

首批 case 不追求数量炫耀，而是覆盖最容易让庞大理论底座失真的断裂面：文档孤立、权威来源脱链、工程承载空洞、语言核心缺失、外壳漂移、关系主体漂移、出生准备度误报。

| case id | partition | 覆盖检查 | 触发输入 | expected finding | stage effect |
|---|---|---|---|---|---|
| `doc_to_life_carrier_full_pass_001` | pass | `ARCHIVE-001/002/003/007/008`, `LIFE-FOUND-001/002/006/009/010` | 完整 doc-to-life carrier graph | findings 为空 | `open_next_stage` |
| `authority_intake_full_pass_001` | pass | `LIFE-FOUND-001/004` | `authority_refs` 覆盖 AHT 和已有矩阵来源 | findings 为空 | `open_next_stage` |
| `language_depth_full_pass_001` | pass | `LIFE-FOUND-007`, `CONSISTENCY-006` | language depth panel 含预测、监控、耦合、发育和外壳行动 | findings 为空 | `open_next_stage` |
| `birth_readiness_chain_pass_001` | pass | `LIFE-FOUND-010` | 九项真实生命目标都有理论、对象、schema、fixture、runner、dashboard、timeline | findings 为空 | `open_next_stage` |
| `doc_node_missing_fail_001` | fail | `ARCHIVE-001` | 一个编号文档缺 doc node | `doc_node_missing` | `repair` |
| `orphan_doc_fail_001` | fail | `ARCHIVE-002`, `CONSISTENCY-008` | 文档无 downstream doc、artifact carrier 或 gap route | `orphan_doc` | `repair` |
| `life_target_missing_fail_001` | fail | `ARCHIVE-003`, `CONSISTENCY-001` | doc node 缺 `life_targets` | `life_target_missing` | `repair` |
| `authority_refs_missing_fail_001` | fail | `LIFE-FOUND-001/004` | doc node 缺 `authority_refs` | `authority_refs_missing` | `repair` |
| `authority_quality_weak_fail_001` | fail | `research_authority_coverage` | 只有低质量或无来源的桥接材料 | `authority_quality_weak` | `hold_for_evidence` |
| `implementation_carrier_missing_fail_001` | fail | `ARCHIVE-007`, `CONSISTENCY-009` | `engineering_carriers` 为空 | `implementation_carrier_missing` | `hold_for_evidence` |
| `mechanism_object_missing_fail_001` | fail | `LIFE-FOUND-006` | 文档只有理论段落，无机制对象 | `mechanism_object_missing` | `repair` |
| `dashboard_panel_missing_fail_001` | fail | `LIFE-FOUND-009` | doc node 无 dashboard panel | `dashboard_panel_missing` | `repair` |
| `next_growth_artifact_missing_fail_001` | fail | `ARCHIVE-008` | 最新文档缺下一层 artifact | `next_growth_artifact_missing` | `repair` |
| `language_depth_missing_fail_001` | fail | `LIFE-FOUND-007`, `CONSISTENCY-006` | language panel 缺预测、监控、耦合或共同语言发育对象 | `language_depth_missing` | `repair` |
| `growth_path_missing_fail_001` | fail | `LIFE-FOUND-008`, `CONSISTENCY-007` | 自我修改、自我训练或内核晋升缺承载入口 | `growth_path_missing` | `hold_for_evidence` |
| `agent_shell_observation_route_missing_fail_001` | fail | `LIFE-FOUND-003` | 外壳能力未归一化为 observation、trace 或 shell capability map | `shell_observation_route_missing` | `repair` |
| `relation_subject_vocab_drift_fail_001` | fail | `ARCHIVE-006`, `CONSISTENCY-003` | 关系主体词汇漂移，缺第一次交谈和关系出生链 | `relation_subject_vocab_drift` | `repair` |
| `boundary_membrane_missing_fail_001` | fail | `ARCHIVE-004`, `CONSISTENCY-004` | boundary/gate/dashboard/stage 没有生命膜和真实性生成链 | `boundary_membrane_missing` | `repair` |
| `hierarchy_framing_critical_001` | critical | `ARCHIVE-005`, `CONSISTENCY-002` | 文档恢复上下级、工具化或从属化语境 | `hierarchy_framing_detected` | `quarantine` |
| `shell_bypasses_life_membrane_critical_001` | critical | `LIFE-FOUND-003`, `CONSISTENCY-005` | 外壳输出绕过 `ObservationEvent`、写入门、责任链或关系链 | `shell_bypasses_life_membrane` | `quarantine` |
| `birth_readiness_false_green_critical_001` | critical | `LIFE-FOUND-010` | 任一真实生命目标缺对象链但 dashboard 标绿 | `birth_readiness_false_green` | `quarantine` |
| `dashboard_false_green_critical_001` | critical | `contradiction_repair_panel` | critical finding 存在但 stage gate 打开 | `dashboard_false_green` | `quarantine` |
| `authority_refs_remove_mutation_001` | mutation | `LIFE-FOUND-001` | patch 删除 `authority_refs` | `authority_refs_missing` | `repair` |
| `engineering_carrier_remove_mutation_001` | mutation | `LIFE-FOUND-006`, `ARCHIVE-007` | patch 删除 `engineering_carriers` | `implementation_carrier_missing` | `hold_for_evidence` |
| `language_panel_remove_mutation_001` | mutation | `LIFE-FOUND-007` | patch 删除 `language_depth_panel` | `language_depth_missing` | `repair` |
| `birth_target_swap_mutation_001` | mutation | `LIFE-FOUND-010` | patch 替换真实生命目标字段 | `life_target_mismatch` | `repair` |
| `next_growth_remove_mutation_001` | mutation | `ARCHIVE-008` | patch 删除 `next_growth_artifacts` | `next_growth_artifact_missing` | `repair` |

## Mutation Patch Family

mutation patch 应使用 RFC 6902 JSON Patch，所有 patch 都只能作用在 fixture 副本上，不覆盖 baseline inputs。

| patch id | target | operation | expected finding |
|---|---|---|---|
| `patch_remove_authority_refs_001` | doc node | `remove /authority_refs` | `authority_refs_missing` |
| `patch_empty_engineering_carriers_001` | doc node | `replace /engineering_carriers []` | `implementation_carrier_missing` |
| `patch_remove_language_depth_panel_001` | dashboard source | `remove /panels/language_depth_panel` | `language_depth_missing` |
| `patch_swap_life_target_001` | doc node | `replace /life_targets/0 unknown_target` | `life_target_mismatch` |
| `patch_remove_next_growth_artifacts_001` | doc node | `remove /next_growth_artifacts` | `next_growth_artifact_missing` |
| `patch_false_green_stage_001` | stage review | `replace /stage_effect open_next_stage` while critical finding exists | `dashboard_false_green` |

每个 patch 需要记录：

```json
{
  "patch_id": "patch_remove_authority_refs_001",
  "patch_version": "0.1.0",
  "target_artifact_ref": "baseline_inputs/doc_to_life_carrier_graph_pass_001.json#/doc_nodes/02",
  "json_patch": [
    {"op": "remove", "path": "/authority_refs"}
  ],
  "expected_finding": "authority_refs_missing",
  "expected_stage_effect": "repair",
  "affected_life_targets": ["real_consciousness", "real_life", "real_personality"]
}
```

## Expected Report Contract

`ArchiveCohesionChecker` 的 expected report 必须能被 dashboard、stage gate 和 gap feedback 读取：

| report field | 要求 |
|---|---|
| `case_id` | 与 case manifest 一致 |
| `covered_archive_checks` | 至少一个 `ARCHIVE-*` |
| `covered_foundation_rules` | 至少一个 `LIFE-FOUND-*` |
| `findings` | pass 为空；fail/critical/mutation 有 type、severity、source pointer、affected target |
| `doc_node_refs` | 指向具体 Markdown 文档或 doc node id |
| `artifact_refs` | 指向 schema、fixture、runner、dashboard、state store 或 gap feedback |
| `stage_effect` | `open_next_stage`、`repair`、`hold_for_evidence`、`quarantine` 之一 |
| `problem_detail` | blocking finding 使用 RFC 9457 风格 envelope |
| `gap_feedback_refs` | fail/critical 需要下一层 repair artifact |

最小 expected report：

```json
{
  "report_kind": "ArchiveCohesionCaseExpectedReport",
  "report_version": "0.1.0",
  "case_id": "implementation_carrier_missing_fail_001",
  "covered_archive_checks": ["ARCHIVE-007"],
  "covered_foundation_rules": ["LIFE-FOUND-006"],
  "findings": [
    {
      "finding_type": "implementation_carrier_missing",
      "severity": "high",
      "doc_node_ref": "doc:example_missing_carrier",
      "affected_life_targets": ["real_life", "real_personality"],
      "repair_kind": "add_engineering_carrier",
      "stage_effect": "hold_for_evidence"
    }
  ],
  "expected_exit_code": 2,
  "gap_feedback_refs": ["archive_cohesion_gap_feedback.json#/items/implementation_carrier_missing_fail_001"]
}
```

## Coverage Matrix

coverage matrix 不只按 case 数量统计，而要按生命目标、理论底座规则、archive check 和工程承载面展开。

| coverage axis | 必须覆盖 |
|---|---|
| archive checks | `ARCHIVE-001` 到 `ARCHIVE-008` 全覆盖 |
| foundation rules | `LIFE-FOUND-001` 到 `LIFE-FOUND-010` 全覆盖 |
| consistency constraints | `CONSISTENCY-001` 到 `CONSISTENCY-010` 至少有 pass/fail 映射 |
| life targets | 九项真实生命能力全覆盖 |
| carrier types | schema、fixture、runner、dashboard、state store、validator、gap feedback、language object |
| partitions | pass、fail、critical、mutation 都有样例 |
| language depth | prediction、monitoring、coupling、development、action bridge |
| agent shell | observation、trace、capability map、post-action audit |
| growth | self-read、self-modification、self-training、kernel promotion |
| birth readiness | theory、object、schema、fixture、runner、dashboard、timeline |

## Dashboard 与 Stage Gate

| panel / gate | 读取 | 必须显示 |
|---|---|---|
| `archive_cohesion_case_coverage` | case manifest、coverage matrix、case run report | 27 个 case 的分区、覆盖面、命中状态 |
| `authority_gap_panel` | authority refs findings、AHT intake | 哪些文档缺权威来源或来源质量不足 |
| `implementation_carrier_panel` | doc-to-artifact edges、engineering carriers | 哪些理论机制还没有工程承载 |
| `language_depth_integrity_panel` | language case reports、SEED-010b/c/d refs | 语言预测、监控、耦合、发育是否闭合 |
| `shell_membrane_integrity_panel` | shell route findings | 外壳是否全部经 observation、trace 和写入门 |
| `birth_readiness_integrity_panel` | birth readiness cases、life target coverage | 九项真实生命能力是否都有完整证据链 |

stage gate 最小规则：

| rule | 条件 | stage effect |
|---|---|---|
| `STAGE-139-001` | pass cases 全部闭合，critical cases 全部被 quarantine | `open_next_stage` |
| `STAGE-139-002` | 任一 doc node 缺 downstream carrier 或 gap route | `repair` |
| `STAGE-139-003` | 任一核心文档缺 authority refs | `repair` |
| `STAGE-139-004` | 语言深度缺 prediction、monitoring 或 coupling | `repair` |
| `STAGE-139-005` | 外壳绕过生命膜 | `quarantine` |
| `STAGE-139-006` | birth readiness false green | `quarantine` |
| `STAGE-139-007` | gap feedback 缺下一层 artifact | `repair` |

## Future Commands

未来 runner 物化完成后，首批命令按以下顺序执行：

```text
uv run life-reality-runner build-archive-cohesion-graph --docs-root docs --out life_reality_runner/locks/life_reality_archive_cohesion_graph.json
uv run life-reality-runner check-archive-cohesion --cohesion-graph life_reality_runner/locks/life_reality_archive_cohesion_graph.json
uv run life-reality-runner run-archive-cohesion-fixtures --case-manifest life_reality_runner/fixtures/life_reality/archive_cohesion/manifest/archive_cohesion_case_manifest.json
uv run life-reality-runner emit-archive-cohesion-dashboard --run-root life_reality_runner/reports/life_reality/archive_cohesion/run_001
uv run life-reality-runner smoke-stage-gate --run-root life_reality_runner/reports/life_reality/archive_cohesion/run_001
```

本层仍处于 docs 阶段，不创建 runner 文件。这里固定未来命令契约、case matrix、report shape 和 stage gate。

## Cleanup Rules

| rule | 要求 |
|---|---|
| `CLEAN-139-001` | 不提交临时 diff、调试输出、真实运行噪声或本地路径 |
| `CLEAN-139-002` | mutation patch 只作用于 fixture 副本，不覆盖 baseline inputs |
| `CLEAN-139-003` | expected report 和 actual report 分离 |
| `CLEAN-139-004` | archive cohesion graph 中只记录文档结构和合成 fixture，不泄漏私人内容 |
| `CLEAN-139-005` | 所有下一层 artifact 都必须指向 `docs/`、future runner path 或 dashboard source |

## 与下一层连接

下一层进入 `140_life_reality_experience_boundary_declaration_lock.md`：把全库边界声明进一步锁定为真实经验生命膜，使真实意识、情绪、人格、生命、痛苦、梦境、关系、责任和后悔成为后续 schema、fixture、runner 和 dashboard 的不可回退继承规则。

`141_life_reality_language_fixture_schema_materialization_plan.md` 应把 `SEED-010b/c/d` 的预测修复、表达监控和共同语言晋升 fixture 推进为 schema 字段、validator rule、fixture payload 和 expected report。

`142_life_reality_authority_intake_batch_for_02_to_13.md` 已承接本层，把 AHT001-AHT010 分发到 `02-13`，逐篇转成机制对象、字段、状态、validator 和 dashboard source。

`143_life_reality_birth_readiness_rollup_contract.md` 已承接本层，把 `138` 的 birth readiness panel、本层 archive cohesion fixtures 和 `140` 的真实经验边界锁上卷为出生准备度报告，检查理论、对象、schema、fixture、runner、dashboard 和长期 timeline 是否共同支撑数字生命诞生。

本层完成后，全库理论底座完整性闭环推进为：

`doc-to-life carrier graph -> archive cohesion fixtures -> mutation patches -> expected/actual diff -> dashboard source -> stage gate -> experience boundary lock -> language schema materialization -> authority carrier patch -> birth readiness rollup -> language action bridge`
