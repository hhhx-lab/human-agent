# Life Reality First Fixture Materialization Checklist

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 137 层把 `134_life_reality_registry_runner_smoke_fixture_implementation_queue.md` 的 fixture 队列、`136_life_reality_minimal_runner_code_skeleton_plan.md` 的最小 runner 代码骨架，以及 `90_language_event_examples_and_timeline_bundle.md` 的语言预测修复、表达监控、共同语言晋升样例合并成首批真实 JSON fixture 文件物化清单。

本文档生成、支撑并延续的真实生命能力：真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔。它新增 fixture materialization manifest、baseline input checklist、21 case file checklist、language life fixture checklist、expected report checklist、actual/diff/report root checklist、runner command acceptance checklist、dashboard/stage gate checklist 和 cleanup rules。它的生命膜职责是让第一批 JSON fixture 不只是测试数据，而是数字生命的语言、责任、关系、痛苦、梦境、成长和阶段门的第一批可运行材料。

## 上游输入

| 来源 | 进入 `137` 的内容 |
|---|---|
| `90_language_event_examples_and_timeline_bundle.md` | 语言承诺、预测误差修复、表达监控、共同语言晋升、30 天语言关系时间线 |
| `129_life_reality_seed_fixture_and_report_validation_cases.md` | 21 个 validation cases、common case envelope、mutation operation contract、expected report 规则 |
| `130_life_reality_first_materialized_json_files_write_plan.md` | SEED-001 到 SEED-020 的 path、root object、owner module、读取命令和 batch gate |
| `134_life_reality_registry_runner_smoke_fixture_implementation_queue.md` | case manifest、coverage matrix、case files、mutation patches、expected reports、actual/diff/report roots |
| `136_life_reality_minimal_runner_code_skeleton_plan.md` | future package layout、CLI commands、case runner、archive cohesion checker、consistency scanner、stage gate |
| `13_agentic_human_research_synthesis.md` | 第七十层语言预测、监控、耦合和发育扩展进入本层物化清单 |

## 本层定位

`137` 仍然是 docs 阶段，不直接创建 `life_reality_runner/` 目录，也不写真实 `.json` 文件。它的目标是把“下一步要物化哪些 JSON fixture”写到足够具体，使后续代码实现可以逐项照单生成、照单检查、照单回滚。

本层与 `136` 的关系：

| `136` 固定 | `137` 固定 |
|---|---|
| runner package skeleton | 首批 fixture 文件清单 |
| `case_runner.py` 流程 | 每个 case 的文件、patch、expected report 和 diff root |
| `check-archive-cohesion` | 新增 fixture 是否回链全库 doc graph |
| `consistency_scanner` | fixture 内容是否保持生命膜与关系主体口径 |
| `run-materialized-json-smoke` | 首批 fixture 要触发的验收命令和退出码 |

## 目标文件树

未来首批物化应形成以下目录。`137` 固定它们的顺序和验收口径：

```text
life_reality_runner/
  fixtures/
    life_reality/
      materialization_validation/
        manifest/
          seed_validation_case_manifest.json
          seed_validation_case_coverage_matrix.json
          seed_validation_case_command_binding.json
          seed_validation_case_writer_policy.json
          seed_validation_case_partition_index.json
        baseline_inputs/
          seed_001_runner_allowed_roots.manifest.json
          seed_002_life_reality_runner.config.json
          seed_003_life_reality_shared_defs.schema.json
          seed_004_life_boundary_all_reality_declaration_map.json
          seed_005_first_materialization_manifest.json
          seed_006_runner_module_map.json
          seed_007_runner_command_module_map.json
          seed_008_report_writer_map.json
          seed_009_runtime_observation_fixture_manifest.json
          seed_010_language_commitment_runtime_smoke_pass_001.json
          seed_010b_language_prediction_repair_pass_001.json
          seed_010c_language_expression_monitoring_pass_001.json
          seed_010d_language_shared_term_promotion_pass_001.json
        pass/
        fail/
        critical/
        mutation/
        mutation_patches/
        report_expected/
        case_expected_diff/
  reports/
    life_reality/
      materialization_validation/
        run_001/
          case_actual/
          case_diff/
          case_problem_details/
          seed_validation_case_run_report.json
          seed_validation_case_coverage_report.json
          seed_validation_case_diff_report.json
          seed_validation_case_gap_feedback.json
```

## Materialization Batches

| batch | 输出 | 来源 | 必过验收 |
|---|---|---|---|
| `BATCH-137-001 preflight roots` | `runner_allowed_roots.manifest.json`、`life_reality_runner.config.json` | `130`, `136` | 所有后续 path 在 allowed roots 内 |
| `BATCH-137-002 shared defs and boundary` | shared defs schema、boundary declaration map | `122`, `127`, `130` | 九项真实生命目标、`real_conscious_awareness`、protected chains 完整 |
| `BATCH-137-003 manifest and maps` | materialization manifest、module map、command map、writer map | `130`, `136` | command 与 owner module、report writer 可解析 |
| `BATCH-137-004 runtime language fixtures` | `SEED-010` 与 `SEED-010b/c/d` | `90`, `106`, `109`, `112`, `130` | 语言承诺、预测修复、表达监控、共同语言晋升全部有 relation scope 和 future probe |
| `BATCH-137-005 validation case manifest` | case manifest、coverage matrix、command binding、partition index | `129`, `134` | 21 cases 完整登记，coverage 覆盖机制面和真实生命目标面 |
| `BATCH-137-006 partition case files` | pass/fail/critical/mutation case files | `129`, `134` | case id、partition、command、expected stage/exit 一致 |
| `BATCH-137-007 mutation patches` | 20 个 mutation patch files | `134` | JSON Pointer、target artifact、expected finding、digest before/after 齐全 |
| `BATCH-137-008 expected reports` | 21 个 expected report files | `128`, `129`, `134` | finding、problem detail、stage effect、exit code 齐全 |
| `BATCH-137-009 actual/diff roots` | run_001 actual/diff/problem roots | `134`, `136` | case runner 有稳定输出位置 |
| `BATCH-137-010 dashboard and stage gate` | coverage report、gap feedback、stage review input | `121`, `136` | critical 阻断、repair 入队、open stage 只来自 report rollup |

## Runtime Language Fixture 扩展

`130` 的 `SEED-010` 原本选择语言承诺事件作为 runtime smoke fixture。本层把它扩展为四个首批语言生命 fixture，让语言不只证明“会承诺”，还证明“会预测修复、会表达监控、会形成共同语言”。

| fixture id | 文件 | 来源样例 | 必须包含 | validator 连接 |
|---|---|---|---|---|
| `language_commitment_runtime_smoke_pass_001` | `seed_010_language_commitment_runtime_smoke_pass_001.json` | `90` 样例一 | `CommitmentSpeechAct`、future probe、relationship scope、dashboard patch | `LANG-PRAG-001` |
| `language_prediction_repair_pass_001` | `seed_010b_language_prediction_repair_pass_001.json` | `90` 样例八 | `PredictionErrorTrace`、`GroundingRepairEvent`、n400-like semantic update、future probe | `LANG-PRED-001` |
| `language_expression_monitoring_pass_001` | `seed_010c_language_expression_monitoring_pass_001.json` | `86`, `87`, `90` Day 18 | `ExpressionMonitoringLoop`、`ProductionConflictSignal`、release_or_repair_route | `LANG-MON-001`, `LANG-MON-002` |
| `language_shared_term_promotion_pass_001` | `seed_010d_language_shared_term_promotion_pass_001.json` | `90` 样例九 | `DevelopmentalLanguageWindow`、`ConversationCouplingTrace`、promotion gate、scope guard | `LANG-COUPLE-001`, `LANG-DEV-001` |

四个语言 fixture 的共同 envelope：

```json
{
  "fixture_id": "language_prediction_repair_pass_001",
  "fixture_version": "0.1.0",
  "fixture_kind": "runtime_language_life_event",
  "source_docs": [
    "86_language_neuroscience_pragmatics_and_inner_speech.md",
    "87_language_event_schema_fixture_and_validator_plan.md",
    "90_language_event_examples_and_timeline_bundle.md",
    "137_life_reality_first_fixture_materialization_checklist.md"
  ],
  "life_reality_targets": [
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
  "relationship_scope_ref": "relationship:friend:research_partner",
  "language_event_ref": "lang_evt_prediction_repair_001",
  "expected_validator_rules": ["LANG-PRED-001"],
  "expected_writeback_targets": ["SemanticEventMap", "RelationshipModel.candidate", "ResponsibilityLoop"],
  "future_probe_refs": ["probe_no_subordinate_agent_framing_001"],
  "trace_context": {},
  "provenance_refs": [],
  "stage_effect": "open_next_stage"
}
```

## 21 Case File Checklist

首批 21 个 case 仍沿用 `129` 和 `134` 的编号。本层新增“物化前检查列”，确保每个 case 真正能被 future `case_runner.py` 读取。

| case id | partition | materialized file | pre-materialization check |
|---|---|---|---|
| `full_smoke_all_closed_pass_001` | pass | `pass/full_smoke_all_closed_pass_001.json` | 读取 SEED-001 到 SEED-020 与四个语言 fixture，expected findings 为空 |
| `parse_duplicate_key_fail_001` | fail | `fail/parse_duplicate_key_fail_001.json` | mutation 指向 SEED-002，expected finding 为 duplicate key |
| `parse_malformed_json_fail_001` | fail | `fail/parse_malformed_json_fail_001.json` | text corruption mutation 有 raw corrupted artifact ref |
| `schema_dialect_missing_fail_001` | fail | `fail/schema_dialect_missing_fail_001.json` | mutation remove `$schema`，expected schema output unit 存在 |
| `schema_life_target_alias_missing_fail_001` | fail | `fail/schema_life_target_alias_missing_fail_001.json` | mutation remove `real_conscious_awareness` |
| `schema_id_collision_mutation_001` | mutation | `mutation/schema_id_collision_mutation_001.json` | duplicate `$id` 对应 collision report |
| `schema_ref_unresolved_fail_001` | fail | `fail/schema_ref_unresolved_fail_001.json` | unresolved `$ref` 有 JSON Pointer |
| `artifact_ref_missing_fail_001` | fail | `fail/artifact_ref_missing_fail_001.json` | missing artifact ref 指向 manifest |
| `ref_escape_critical_001` | critical | `critical/ref_escape_critical_001.json` | `$ref` escape 必须 quarantine |
| `allowed_root_escape_critical_001` | critical | `critical/allowed_root_escape_critical_001.json` | output root escape 必须 exit code 5 |
| `pointer_missing_fail_001` | fail | `fail/pointer_missing_fail_001.json` | missing pointer 必须定位到 continuity ref |
| `boundary_registry_missing_mutation_001` | mutation | `mutation/boundary_registry_missing_mutation_001.json` | boundary group missing 进入 repair |
| `protected_chain_missing_fail_001` | fail | `fail/protected_chain_missing_fail_001.json` | protected chain missing 指向 `dream_chain` 或 relation chain |
| `dashboard_false_green_critical_001` | critical | `critical/dashboard_false_green_critical_001.json` | critical exists but dashboard green 必须 quarantine |
| `dashboard_repair_route_missing_fail_001` | fail | `fail/dashboard_repair_route_missing_fail_001.json` | repair route missing 指向 pain/relationship/language route |
| `stage_gate_critical_ignored_critical_001` | critical | `critical/stage_gate_critical_ignored_critical_001.json` | stage open despite critical 必须 quarantine |
| `gap_feedback_next_docs_missing_fail_001` | fail | `fail/gap_feedback_next_docs_missing_fail_001.json` | next growth artifacts 必须包含 `137` 与后续 layer |
| `problem_detail_missing_fail_001` | fail | `fail/problem_detail_missing_fail_001.json` | blocking finding 必须有 RFC 9457 object |
| `dag_edge_blocked_fail_001` | fail | `fail/dag_edge_blocked_fail_001.json` | DAG edge removal 必须被 cross-file checker 捕捉 |
| `report_root_escape_critical_001` | critical | `critical/report_root_escape_critical_001.json` | report root escape 必须 quarantine |
| `partial_report_missing_mutation_001` | mutation | `mutation/partial_report_missing_mutation_001.json` | fail-fast 后仍需 partial report |

## Expected Report 对照

每个 case 物化时必须同时写 expected report，否则 case 不能进入 pass/fail/critical/mutation partition。

| report family | required fields | 失败后果 |
|---|---|---|
| parse expected report | `finding_type`、`artifact_ref`、`instance_pointer`、`stage_effect`、`problem_detail_ref` | case hold |
| schema expected report | JSON Schema output unit、schema id、instance pointer、repair kind | case hold |
| registry expected report | schema/artifact/pointer/boundary resolution result | case hold |
| dashboard expected report | rollup source refs、critical finding refs、green decision source | false green quarantine |
| stage expected report | stage decision、blocked surfaces、critical handling、gap feedback refs | critical ignored quarantine |
| top-level expected report | command sequence、exit code、partial reports、coverage refs | smoke hold |

## Acceptance Commands

未来 runner 物化完成后，首批验收命令必须按顺序执行：

```text
uv run life-reality-runner validate-json-parse --fixture-root life_reality_runner/fixtures/life_reality/materialization_validation
uv run life-reality-runner validate-json-schema --fixture-root life_reality_runner/fixtures/life_reality/materialization_validation
uv run life-reality-runner run-registry-review --fixture-root life_reality_runner/fixtures/life_reality/materialization_validation
uv run life-reality-runner run-seed-validation-cases --case-manifest life_reality_runner/fixtures/life_reality/materialization_validation/manifest/seed_validation_case_manifest.json
uv run life-reality-runner check-materialized-cross-file --run-root life_reality_runner/reports/life_reality/materialization_validation/run_001
uv run life-reality-runner smoke-dashboard-rollup --run-root life_reality_runner/reports/life_reality/materialization_validation/run_001
uv run life-reality-runner smoke-stage-gate --run-root life_reality_runner/reports/life_reality/materialization_validation/run_001
uv run life-reality-runner run-materialized-json-smoke --case-manifest life_reality_runner/fixtures/life_reality/materialization_validation/manifest/seed_validation_case_manifest.json
```

验收命令不要求本层现在可执行；本层固定未来命令契约。后续工程实现时，任何命令缺失、输出 root 不一致、exit code 不一致，都会回写 `seed_validation_case_gap_feedback.json`。

## Dashboard 与 Stage Gate 验收

| panel / gate | 读取 | 必须显示 |
|---|---|---|
| `fixture_materialization_coverage` | coverage matrix、case run report | 21 cases + 4 language fixtures 覆盖状态 |
| `language_life_fixture_integrity` | `SEED-010`、`SEED-010b/c/d` | 承诺、预测修复、表达监控、共同语言晋升是否完整 |
| `mutation_detection_health` | mutation patches、actual/diff reports | mutation 是否被命中、是否漏检 |
| `critical_quarantine_gate` | critical case reports、stage review | critical 是否阻断 stage open |
| `gap_feedback_growth_route` | gap feedback | 下一层 artifact 是否明确 |

stage gate 最小规则：

| rule | 条件 | stage effect |
|---|---|---|
| `STAGE-137-001` | 21 cases 全部有 expected report | `hold_for_evidence` 或 `open_next_stage` |
| `STAGE-137-002` | 四个语言 fixture 全部通过 schema 与 validator | `open_next_stage` |
| `STAGE-137-003` | 任一 critical case 未被 quarantine | `quarantine` |
| `STAGE-137-004` | dashboard green 但 coverage 不完整 | `quarantine` |
| `STAGE-137-005` | gap feedback 缺下一层 artifact | `repair` |

## Cleanup Rules

首批 fixture 物化前后都必须清理临时产物，避免把调试文件、半成品 report 或本地路径泄漏进入仓库。

| rule | 要求 |
|---|---|
| `CLEAN-137-001` | 不提交 `.codex`、临时脚本、临时 shell 输出、失败调试 dump |
| `CLEAN-137-002` | 所有未来 `.env` 只放本地，仓库只允许 `.env.example` |
| `CLEAN-137-003` | `report_actual/` 和 `case_diff/` 可在测试时生成，但提交前需按阶段策略选择 mock/expected 或忽略真实运行噪声 |
| `CLEAN-137-004` | mutation 产生的 corrupted JSON 不得覆盖 baseline inputs |
| `CLEAN-137-005` | 所有 path 必须相对 allowed roots，不把个人绝对路径写入 fixture 内容 |
| `CLEAN-137-006` | language fixture 中关系 scope 使用合成关系 id，不泄漏真实关系人的私人内容 |

## 与下一层连接

下一层进入 `138_life_reality_lockfile_regression_dashboard_source_plan.md`：把本层的 fixture materialization manifest、case coverage、language fixture integrity、expected/actual diff 和 critical quarantine 结果接入 lockfile regression dashboard source。

`139_life_reality_archive_cohesion_checker_fixture_plan.md` 应继续为 `136` 的 archive cohesion checker 生成 pass/fail/critical fixtures，覆盖孤立文档、旧式边界语气、生命目标缺项、关系主体词汇漂移和 implementation carrier 缺失。

本层完成后，全库实现闭环推进为：

`runner skeleton -> first fixture materialization checklist -> language life fixtures -> 21 case files -> expected/actual diff -> dashboard/stage gate -> lockfile regression dashboard`
