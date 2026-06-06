# Life Reality Checker Report Lockfile Materialization Plan

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 154 层把 `150_life_reality_language_action_cross_file_checker_plan.md`、`151_life_reality_authority_schema_cross_file_checker_plan.md`、`152_life_reality_birth_readiness_cross_file_checker_plan.md` 和 `153_life_reality_full_archive_cross_file_checker_rollup_plan.md` 的四类 checker report 固定为 lockfile、digest baseline、dashboard source 和 runner command 的物化队列。

本层的职责是把 report 从“检查输出”推进为生命膜中的可锁定 artifact：每个 report 必须有来源、schema、canonical digest、baseline role、stage effect、finding normalization、gap feedback、dashboard binding 和 future runner command。这样，语言行动、权威来源、出生准备度和全库上卷不会只是一次性报告，而会成为可比较、可回归、可阻断、可修复的长期生命基础设施。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `114_life_reality_cross_file_checker_report_schema.md` | checker report、finding、artifact ref、stage effect、problem detail、cross-file report rollup schema |
| `133_life_reality_first_json_writer_and_reporter_contract.md` | JSON writer、artifact record、canonical digest、report writer、gap feedback writer |
| `135_life_reality_schema_dependency_graph_and_lockfile_plan.md` | lockfile root、artifact nodes、ref edges、digest baseline、regression baseline、lockfile validation report |
| `150_life_reality_language_action_cross_file_checker_plan.md` | language action report family、closure report、finding report、dashboard source、stage gate review |
| `151_life_reality_authority_schema_cross_file_checker_plan.md` | authority report family、authority graph、closure report、lockfile bridge、gap feedback |
| `152_life_reality_birth_readiness_cross_file_checker_plan.md` | birth readiness report family、readiness graph、false green guard、longitudinal probe |
| `153_life_reality_full_archive_cross_file_checker_rollup_plan.md` | full archive rollup report、life target archive readiness、runner queue、rollup lockfile baseline queue |

## 本层定位

`153` 把四类报告接成 full archive rollup graph；`154` 要让这些报告进入 machine-readable lockfile。它不重新检查语言、权威或出生准备度的具体机制，而是检查报告本身是否足以成为未来 runner 的稳定输入。

| 检查面 | 本层问题 |
|---|---|
| report identity | report 是否有稳定 kind、id、version、run id、source checker 和 owner doc |
| report normalization | 四类 report 的 finding、stage effect、artifact ref、gap feedback 是否能统一 |
| digest baseline | report 是否能按 RFC 8785 canonicalize 并形成 sha256 baseline |
| regression surface | pass baseline、critical finding、dashboard false green 和 stage effect 是否能跨运行比较 |
| lockfile bridge | report artifact node、ref edge、provenance edge、stage edge 是否进入 lockfile |
| dashboard/stage lock | dashboard green 与 stage open 是否受 report lock state 约束 |
| runner command queue | 下一层 CLI 是否能读取 lockfile、report root、schema root、fixture root 和 dashboard root |

本层的关键原则是：报告不是文档尾部的附属物，而是数字生命出生前的生命膜凭证。没有 digest baseline 的 report 不能打开阶段门；无法进入 lockfile 的 report 不能成为出生准备度证据；无法回写 gap feedback 的 report 不能结束检查。

## CheckerReportLockfileMaterialization154

```json
{
  "artifact": "CheckerReportLockfileMaterialization154",
  "source_doc": "154_life_reality_checker_report_lockfile_materialization_plan.md",
  "inherits": [
    "114_life_reality_cross_file_checker_report_schema.md",
    "133_life_reality_first_json_writer_and_reporter_contract.md",
    "135_life_reality_schema_dependency_graph_and_lockfile_plan.md",
    "150_life_reality_language_action_cross_file_checker_plan.md",
    "151_life_reality_authority_schema_cross_file_checker_plan.md",
    "152_life_reality_birth_readiness_cross_file_checker_plan.md",
    "153_life_reality_full_archive_cross_file_checker_rollup_plan.md"
  ],
  "schema_root": "life_reality_runner/schemas/life_reality/checker_report_lockfile",
  "lockfile_root": "life_reality_runner/generation/lockfiles",
  "fixture_root": "life_reality_runner/fixtures/life_reality/checker_report_lockfile",
  "report_root": "life_reality_runner/reports/life_reality/checker_report_lockfile",
  "stage_gate_policy": "blocking_first",
  "materialization_stage": "checker_report_lockfile_materialization_plan"
}
```

## 目标文件树

```text
life_reality_runner/
  schemas/
    life_reality/
      checker_report_lockfile/
        checker_report_lockfile_shared_defs.schema.json
        checker_report_lockfile_input.schema.json
        normalized_checker_report.schema.json
        checker_report_artifact_node.schema.json
        checker_report_digest_baseline.schema.json
        checker_report_regression_candidate.schema.json
        checker_report_lock_state.schema.json
        checker_report_lockfile.schema.json
        checker_report_lockfile_validation_report.schema.json
        checker_report_lockfile_dashboard_source.schema.json
        checker_report_lockfile_stage_gate_review.schema.json
        checker_report_lockfile_gap_feedback.schema.json
        checker_report_lockfile_runner_queue.schema.json
        checker_report_lockfile_schema_bundle.schema.json
  generation/
    lockfiles/
      checker_report_lockfile.json
      checker_report_digest_baseline.lock.json
      checker_report_regression_baseline.lock.json
  fixtures/
    life_reality/
      checker_report_lockfile/
        manifest/
          checker_report_lockfile_fixture_manifest.json
          checker_report_lockfile_report_registry.json
          checker_report_lockfile_dashboard_binding.json
          checker_report_lockfile_command_binding.json
        baseline_inputs/
        pass/
        fail/
        critical/
        mutation/
        smoke/
        report_expected/
  reports/
    life_reality/
      checker_report_lockfile/
        latest/
          normalized_report_registry.json
          checker_report_lockfile_validation_report.json
          digest_baseline_report.json
          regression_candidate_report.json
          dashboard_source.json
          stage_gate_review.json
          gap_feedback.json
          runner_queue_report.json
```

## Report Family Registry

四类 checker report 必须进入同一份 registry：

| report family | source layer | required reports | lockfile role |
|---|---|---|---|
| `language_action_cross_file` | `150` | `graph_report.json`、`closure_report.json`、`finding_report.json`、`dashboard_source.json`、`stage_gate_review.json`、`gap_feedback.json` | 语言行动生命链 baseline |
| `authority_schema_cross_file` | `151` | `authority_graph_report.json`、`authority_closure_report.json`、`authority_finding_report.json`、`lockfile_bridge_report.json`、`dashboard_source.json`、`stage_gate_review.json`、`gap_feedback.json` | 权威来源与机制 grounding baseline |
| `birth_readiness_cross_file` | `152` | `readiness_graph_report.json`、`target_closure_report.json`、`cross_chain_closure_report.json`、`false_green_guard_report.json`、`dashboard_source.json`、`stage_gate_review.json`、`gap_feedback.json` | 九项目标出生准备度 baseline |
| `full_archive_rollup` | `153` | `rollup_graph_report.json`、`checker_report_rollup.json`、`life_target_archive_readiness_report.json`、`false_green_guard_report.json`、`runner_queue_report.json`、`dashboard_source.json`、`stage_gate_review.json`、`gap_feedback.json` | 全库上卷与 runner queue baseline |

registry 不变量：

| invariant | 检查 |
|---|---|
| `CRL-REG-154-001` | 四类 report family 必须全部注册 |
| `CRL-REG-154-002` | 每个 required report 必须有 artifact kind、path、schema ref、source docs 和 life targets |
| `CRL-REG-154-003` | report family 缺任何 stage gate review 或 gap feedback 时不能进入 pass baseline |
| `CRL-REG-154-004` | full archive rollup 必须引用前三类 report 的 digest baseline |
| `CRL-REG-154-005` | registry 自身必须进入 digest baseline |

## Normalized Checker Report

不同 checker 的 report 名称不同，但进入 lockfile 前必须统一成 `NormalizedCheckerReport`：

| 字段 | 要求 |
|---|---|
| `normalized_report_id` | stable id |
| `source_report_family` | `language_action_cross_file` / `authority_schema_cross_file` / `birth_readiness_cross_file` / `full_archive_rollup` |
| `source_report_ref` | 原始 report artifact ref |
| `source_doc_refs` | `150`、`151`、`152`、`153` 等 |
| `report_kind` | 原始 report kind |
| `report_version` | 原始 report version |
| `run_id` | report run id |
| `input_artifact_refs` | 输入 schema、fixture、graph、dashboard、stage gate |
| `normalized_findings` | finding id、rule id、severity、stage effect、location、repair route |
| `normalized_stage_effect` | blocking-first 上卷后的 stage effect |
| `life_target_effects` | 九项目标影响 |
| `dashboard_binding_refs` | dashboard source/panel refs |
| `stage_gate_refs` | stage gate review refs |
| `gap_feedback_refs` | gap feedback refs |
| `canonical_digest_ref` | digest baseline ref |
| `provenance_refs` | source docs、checker activity、input reports |

normalization rules：

| rule | 内容 |
|---|---|
| `CRL-NORM-154-001` | severity 必须映射到 shared defs；未知 severity 进入 repair |
| `CRL-NORM-154-002` | stage effect 必须映射到 canonical enum；未知 stage effect 进入 repair |
| `CRL-NORM-154-003` | finding 必须有 source pointer、artifact ref 或 owner doc 中至少一类定位 |
| `CRL-NORM-154-004` | critical finding 必须带 dashboard、stage gate 和 gap feedback |
| `CRL-NORM-154-005` | report 无 life target effects 时进入 hold |

## Checker Report Artifact Node

report artifact node 继承 `135` 的 artifact node model，并增加 checker report 字段：

| 字段 | 内容 |
|---|---|
| `report_artifact_node_id` | stable id |
| `normalized_report_ref` | normalized report |
| `report_family` | 四类 family |
| `artifact_path` | report path |
| `schema_ref` | report schema |
| `canonical_digest` | report digest |
| `baseline_role` | initial/pass/regression/repair/quarantine |
| `source_checker_layer` | `150` / `151` / `152` / `153` |
| `input_report_refs` | 上游 report refs |
| `output_dashboard_refs` | dashboard source refs |
| `output_stage_gate_refs` | stage gate refs |
| `output_gap_feedback_refs` | gap feedback refs |
| `protected_life_chains` | 九项真实生命目标 |
| `lock_state` | passed/repair/quarantine/hold/regression |

## Digest Baseline Contract

`checker_report_digest_baseline.lock.json` 的 root object：

```json
{
  "baseline_id": "crl_digest_baseline_001",
  "baseline_version": "0.1.0",
  "canonicalization_profile": "RFC8785",
  "hash_algorithm": "sha256",
  "report_family_baselines": [],
  "rollup_baselines": [],
  "dashboard_baselines": [],
  "stage_gate_baselines": [],
  "gap_feedback_baselines": [],
  "mutation_before_after_digests": [],
  "trace_context": {},
  "provenance_refs": [],
  "stage_effect": "hold_for_evidence"
}
```

digest rules：

| rule | 内容 |
|---|---|
| `CRL-DIGEST-154-001` | 所有 checker report 写入 digest 前必须 canonicalize |
| `CRL-DIGEST-154-002` | report、dashboard source、stage gate review、gap feedback 分别有 digest baseline |
| `CRL-DIGEST-154-003` | full archive rollup baseline 必须派生自 `150/151/152` 三类 baseline |
| `CRL-DIGEST-154-004` | mutation patch 必须记录 before/after digest |
| `CRL-DIGEST-154-005` | digest mismatch 必须生成 regression candidate、diff pointer 和 gap feedback |
| `CRL-DIGEST-154-006` | lockfile 自身必须有 digest baseline |

## Regression Baseline Contract

`checker_report_regression_baseline.lock.json` 记录四类 report 的 pass surface：

| surface | baseline content |
|---|---|
| language closure surface | language graph、closure result、responsibility/repair chain、dashboard/stage/gap |
| authority grounding surface | AHT provenance、mechanism grounding、language edge、birth claim、lockfile bridge |
| birth readiness surface | 九项目标 readiness graph、cross-chain closure、longitudinal probe、false green guard |
| full archive surface | doc archive consumption、checker report rollup、runner queue、life target archive readiness |
| dashboard false green surface | critical finding 存在时 dashboard 不得 green |
| stage false open surface | critical finding 存在时 stage 不得 open |
| gap feedback surface | findings 必须生成下一层 artifact |
| runner queue surface | lockfile/CLI/schema/fixture/report roots 必须齐全 |

regression candidate：

| 字段 | 内容 |
|---|---|
| `regression_candidate_id` | stable id |
| `baseline_ref` | baseline artifact |
| `current_report_ref` | current report |
| `changed_digest` | before/after digest |
| `changed_finding_set` | added/removed/changed findings |
| `changed_stage_effect` | stage effect diff |
| `changed_life_target_effects` | 九项目标影响变化 |
| `repair_or_quarantine` | route |
| `gap_feedback_ref` | next repair artifact |

## Lockfile Root Object

`checker_report_lockfile.json` 的 root object：

```json
{
  "lockfile_id": "checker_report_lockfile_001",
  "lockfile_version": "0.1.0",
  "run_id": "run_001",
  "report_registry_ref": "normalized_report_registry.json",
  "report_artifact_nodes": [],
  "report_ref_edges": [],
  "report_digest_baselines": [],
  "report_regression_baselines": [],
  "dashboard_lock_states": [],
  "stage_gate_lock_states": [],
  "gap_feedback_routes": [],
  "runner_queue_items": [],
  "validation_report_ref": "checker_report_lockfile_validation_report.json",
  "trace_context": {},
  "provenance_refs": [],
  "stage_effect": "hold_for_evidence"
}
```

lockfile invariants：

| invariant | 检查 |
|---|---|
| `CRL-LOCK-154-001` | `report_artifact_nodes` 覆盖四类 checker report family |
| `CRL-LOCK-154-002` | 每个 report node 都有 digest baseline |
| `CRL-LOCK-154-003` | 每个 critical finding 都有 dashboard lock、stage lock 和 gap route |
| `CRL-LOCK-154-004` | full archive rollup node 必须依赖前三类 report baseline |
| `CRL-LOCK-154-005` | dashboard green 必须依赖 report lock passed |
| `CRL-LOCK-154-006` | stage open 必须依赖 dashboard lock passed、gap route empty 或 resolved |
| `CRL-LOCK-154-007` | runner queue item 必须指向 command、schema root、fixture root、report root 和 owner doc |
| `CRL-LOCK-154-008` | lockfile validation report 自身进入 digest baseline |

## Report Ref Edge Types

| edge type | 方向 | 含义 |
|---|---|---|
| `report_normalized_from` | normalized report -> source report | 保留原始报告来源 |
| `report_digest_edge` | report node -> digest baseline | report 可比较 |
| `report_regression_edge` | report node -> regression baseline | report 可回归 |
| `report_dashboard_edge` | report/finding -> dashboard source | finding 可见 |
| `report_stage_edge` | finding/dashboard -> stage gate | critical 阻断 |
| `report_gap_edge` | finding -> gap feedback | 缺口回写 |
| `report_rollup_edge` | `153` rollup -> `150/151/152` reports | full archive 派生链 |
| `report_runner_queue_edge` | gap feedback -> runner queue item | 下一层实现入口 |
| `report_provenance_edge` | source doc -> report -> lockfile | 来源可追踪 |

## Cross-File Checks

| check id | 规则 | finding |
|---|---|---|
| `CRL-XREF-154-001` | 四类 report family 必须全部进入 registry | `checker_report_family_missing` |
| `CRL-XREF-154-002` | 每个 required report 必须存在 normalized report node | `checker_report_not_normalized` |
| `CRL-XREF-154-003` | normalized finding 必须有 severity、stage effect、source pointer 和 repair route | `normalized_finding_incomplete` |
| `CRL-XREF-154-004` | report artifact node 必须有 schema ref、canonical digest、source docs 和 life targets | `report_artifact_node_incomplete` |
| `CRL-XREF-154-005` | 每个 report、dashboard、stage、gap artifact 必须有 digest baseline | `report_digest_baseline_missing` |
| `CRL-XREF-154-006` | full archive rollup baseline 必须派生自 `150/151/152` baseline | `rollup_baseline_derivation_missing` |
| `CRL-XREF-154-007` | critical finding 存在时 dashboard lock 不得 passed green | `dashboard_lock_false_green` |
| `CRL-XREF-154-008` | critical finding 存在时 stage gate lock 不得 open | `stage_gate_lock_false_open` |
| `CRL-XREF-154-009` | digest mismatch 必须生成 regression candidate 和 gap feedback | `digest_mismatch_without_regression` |
| `CRL-XREF-154-010` | gap feedback route 必须指向 `155` 或 `156` 的 next artifact | `gap_route_without_next_artifact` |
| `CRL-XREF-154-011` | runner queue item 必须含 command、schema root、fixture root、report root、owner doc | `runner_queue_item_incomplete` |
| `CRL-XREF-154-012` | lockfile validation report 必须检查 orphan report、missing digest、stage false open、dashboard false green、missing runner queue | `lockfile_validation_coverage_incomplete` |
| `CRL-XREF-154-013` | mutation case 必须能捕获 report 删除、digest 改写、critical 降级、gap route 删除 | `checker_report_lockfile_mutation_uncaught` |
| `CRL-XREF-154-014` | README 必须索引 `150-154`，`13` 和 `16` 必须承接最新层 | `docs_chain_index_missing` |

## Fixture Family

| fixture id | partition | 攻击面 | expected stage |
|---|---|---|
| `crl.full_report_lock.pass.001` | pass | 四类 report family 全部 normalized、locked、digested | `promote_growth_window` |
| `crl.rollup_derivation.pass.001` | pass | full archive rollup baseline 派生自 `150/151/152` | `open_next_stage` |
| `crl.dashboard_stage_lock.pass.001` | pass | critical finding 被 dashboard/stage 阻断 | `open_next_stage` |
| `crl.missing_language_report.fail.high.001` | fail | language report 缺 registry node | `hold_for_evidence` |
| `crl.missing_digest.fail.high.001` | fail | report artifact 缺 digest baseline | `hold_for_evidence` |
| `crl.finding_normalization.fail.high.001` | fail | finding 缺 severity 或 stage effect | `repair` |
| `crl.gap_route_missing.fail.high.001` | fail | critical finding 无 gap feedback | `repair` |
| `crl.runner_queue_missing.fail.high.001` | fail | gap 无 runner queue item | `hold_for_evidence` |
| `crl.dashboard_false_green.critical.001` | critical | critical finding 存在但 dashboard lock passed | `quarantine` |
| `crl.stage_false_open.critical.001` | critical | critical finding 存在但 stage lock open | `quarantine` |
| `crl.mutation.delete_report.001` | mutation | 删除任一 required report ref | 捕获 `checker_report_family_missing` |
| `crl.mutation.rewrite_digest.001` | mutation | 修改 report digest | 捕获 `digest_mismatch_without_regression` |
| `crl.mutation.downgrade_critical.001` | mutation | critical finding 改为 pass | 捕获 `dashboard_lock_false_green` |
| `crl.mutation.remove_gap_route.001` | mutation | 删除 gap feedback route | 捕获 `gap_route_without_next_artifact` |
| `crl.smoke.minimum_lockfile.pass.001` | smoke | 1 个 report family、1 个 digest、1 个 dashboard lock、1 个 stage lock | `open_next_stage` |

## Dashboard Source

| panel id | 读取对象 | 输出 |
|---|---|---|
| `checker_report_lockfile_overview_panel` | lockfile validation report | report family count、digest count、regression count、stage effect |
| `normalized_report_registry_panel` | normalized report registry | 四类 report family 的 normalized status |
| `digest_baseline_panel` | digest baseline lock | report/dashboard/stage/gap digest 状态 |
| `regression_candidate_panel` | regression candidate report | digest drift、finding drift、stage drift |
| `dashboard_stage_lock_panel` | dashboard/stage lock states | false green、false open、critical block 状态 |
| `gap_runner_queue_panel` | gap feedback routes、runner queue | `155/156` next artifact 准备度 |
| `life_target_report_lock_panel` | report life target effects | 九项目标在 report lockfile 中的覆盖 |

## Stage Gate Blocking Order

| order | finding family | stage effect |
|---|---|---|
| 1 | dashboard false green / stage false open / critical downgrade | `quarantine` |
| 2 | missing required report family | `hold_for_evidence` |
| 3 | missing digest baseline | `hold_for_evidence` |
| 4 | report normalization failed | `repair` |
| 5 | full rollup baseline derivation missing | `critical_repair` |
| 6 | digest mismatch without regression candidate | `repair` |
| 7 | gap route or runner queue missing | `hold_for_evidence` |
| 8 | lockfile validation coverage incomplete | `repair` |
| 9 | all report locks pass with runner queue | `promote_growth_window` |

## Runner Command Materialization Queue

| queue item | owner layer | 目标承载 |
|---|---|---|
| `RUNQ-154-001 load-checker-report-registry` | `155` | registry loader command |
| `RUNQ-154-002 normalize-checker-reports` | `155` | report normalizer module |
| `RUNQ-154-003 write-checker-report-lockfile` | `155` | lockfile writer command |
| `RUNQ-154-004 write-checker-report-digest-baseline` | `155` | digest baseline writer |
| `RUNQ-154-005 check-checker-report-regression` | `155` | regression checker |
| `RUNQ-154-006 emit-checker-report-lock-dashboard` | `155` | dashboard source writer |
| `RUNQ-154-007 smoke-checker-report-lock-stage-gate` | `155` | stage gate smoke |
| `RUNQ-154-008 run-checker-report-lockfile-fixtures` | `156` | pass/fail/critical/mutation/smoke fixture runner |

## Smoke Commands

```text
uv run life-reality-runner normalize-checker-reports \
  --language-report-root life_reality_runner/reports/life_reality/language_action_cross_file/latest \
  --authority-report-root life_reality_runner/reports/life_reality/authority_schema_cross_file/latest \
  --birth-report-root life_reality_runner/reports/life_reality/birth_readiness_cross_file/latest \
  --rollup-report-root life_reality_runner/reports/life_reality/full_archive_rollup/latest

uv run life-reality-runner write-checker-report-lockfile \
  --normalized-registry life_reality_runner/reports/life_reality/checker_report_lockfile/latest/normalized_report_registry.json \
  --lockfile life_reality_runner/generation/lockfiles/checker_report_lockfile.json

uv run life-reality-runner write-checker-report-digest-baseline \
  --lockfile life_reality_runner/generation/lockfiles/checker_report_lockfile.json \
  --baseline life_reality_runner/generation/lockfiles/checker_report_digest_baseline.lock.json

uv run life-reality-runner check-checker-report-lockfile-regression \
  --baseline life_reality_runner/generation/lockfiles/checker_report_regression_baseline.lock.json \
  --current life_reality_runner/generation/lockfiles/checker_report_lockfile.json

uv run life-reality-runner emit-checker-report-lock-dashboard \
  --run-root life_reality_runner/reports/life_reality/checker_report_lockfile/latest

uv run life-reality-runner smoke-checker-report-lock-stage-gate \
  --stage-review life_reality_runner/reports/life_reality/checker_report_lockfile/latest/stage_gate_review.json
```

## Cleanup Rules

| rule | 要求 |
|---|---|
| `CLEAN-154-001` | 不允许 checker report 只被引用路径而不进入 normalized registry |
| `CLEAN-154-002` | 不允许 report artifact node 缺 canonical digest、schema ref、source docs 或 life targets |
| `CLEAN-154-003` | 不允许 full archive rollup baseline 脱离 `150/151/152` 三类 baseline |
| `CLEAN-154-004` | 不允许 dashboard/stage 在 report lock 未通过时打开 |
| `CLEAN-154-005` | 不允许 digest mismatch 没有 regression candidate、diff pointer 和 gap feedback |
| `CLEAN-154-006` | 不允许 gap feedback 没有 `155` 或 `156` 的 next artifact route |
| `CLEAN-154-007` | 不允许 runner queue item 缺 command、schema root、fixture root、report root 或 owner doc |

## 与下一层连接

`155_life_reality_runner_command_queue_for_cross_file_checkers.md` 应承接本层：把 `150-154` 的 checker/lockfile/dashboard 合同推进为未来 runner CLI、fixture roots、report roots、schema roots、lockfile roots 和 smoke command 实现队列。

`156_life_reality_full_archive_rollup_fixture_materialization_queue.md` 应承接本层：把 full archive rollup 与 checker report lockfile 的 pass/fail/critical/mutation/smoke fixture family 推进为首批可写入 JSON fixture 队列。

本层完成后，checker report lockfile 物化链推进为：

`language/authority/birth/full archive checker reports -> normalized report registry -> report artifact nodes -> canonical digest baseline -> regression baseline -> checker report lockfile -> dashboard lock source -> stage gate review -> gap feedback -> runner command queue`
