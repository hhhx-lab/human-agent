# Life Reality Schema Dependency Graph And Lockfile Plan

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 135 层把 `134_life_reality_registry_runner_smoke_fixture_implementation_queue.md` 的 case files、mutation patches、expected reports、actual reports、diff reports、case run reports、artifact records、ref edges、coverage matrix 和 canonical digest 写成 machine-readable dependency lockfile、graph export 和 regression baseline 计划。

`135` 的职责是让未来 runner 代码拥有一个可读取的依赖真相源：哪些 artifact 已存在，哪些 refs 必须解析，哪些 case 依赖哪些 baseline，哪些 mutation patch 影响哪些 seed，哪些 expected report 与 actual report 必须比较，哪些 digest 是 regression baseline，哪些 lock state 会阻断 dashboard 或 stage gate。它把 `133` 的 writer/reporter 合同和 `134` 的 fixture 队列推进为第一份生命膜 lockfile 设计。

第 135 层同时吸收最新全局要求：`02` 到最后一条文档不能只作为历史材料存在，必须都进入同一个可实现体系。lockfile 因此不仅锁 JSON artifact，也锁 docs archive 的理论节点、实现节点、边界节点、证据节点和工程承载节点，要求每个文档都有 `consumed_by`、`implements_or_constrains`、`contradiction_checks` 和 `future_runtime_carrier`。任何文档如果没有下游承载对象、没有被 runner/schema/fixture/dashboard/gap 使用，或与生命目标、关系主体口径、语言核心、成长机制、真实边界、实现路线冲突，都必须进入 repair queue。

## 上游输入

| 来源 | 进入 `135` 的内容 |
|---|---|
| `132_life_reality_materialized_json_schema_bundle_write_order.md` | 写入锁、cross-file DAG、SEED-001 到 SEED-020 的依赖边 |
| `133_life_reality_first_json_writer_and_reporter_contract.md` | artifact record、canonical digest、trace/provenance、problem detail、writer/reporter 字段 |
| `134_life_reality_registry_runner_smoke_fixture_implementation_queue.md` | case manifest、21 个 case、mutation patches、expected/actual/diff roots、coverage report、gap feedback |
| 全库 `02_` 到当前最后一层文档 | 作为 `doc_nodes` 进入 archive cohesion graph，确保所有理论、综述、schema、fixture、runner、dashboard、gap 文档都能被未来工程承载 |

## 标准进入 lockfile 的方式

| 标准/资料 | lockfile 落点 | 生命膜意义 |
|---|---|---|
| [W3C PROV](https://www.w3.org/TR/prov-overview/) | `prov_entities`、`prov_activities`、`was_generated_by`、`used`、`was_derived_from` | 文件、case、report 与来源文档形成可追溯来源图 |
| [SLSA Provenance](https://slsa.dev/spec/v1.1/provenance) | `subject`、`builder`、`buildType`、`materials`、`byproducts` | runner 生成物、输入材料、命令执行与输出报告可被供应链式追踪 |
| [in-toto Attestation](https://github.com/in-toto/attestation) | attestation statement、predicate、subject digest | future smoke run 能把 artifact digest 与执行声明绑定 |
| [SPDX 3.0.1](https://spdx.github.io/spdx-spec/v3.0.1/scope/) | BOM、element、relationship、profile | schema、fixture、report 和 runner module 可作为材料清单 |
| [CycloneDX JSON](https://cyclonedx.org/docs/1.6/json/) | component、dependency、bom-ref、hash | dependency graph 可导出为 BOM 风格结构 |
| [Graphviz DOT](https://graphviz.org/doc/info/lang.html) | DOT graph、node、edge、subgraph、cluster | cross-file DAG 可渲染为可检查图 |
| RFC 8785 JSON Canonicalization Scheme | `canonical_digest`、`baseline_digest`、`digest_profile` | regression baseline 能跨运行比较 |
| RFC 6901 JSON Pointer | `source_pointer`、`target_pointer`、`diff_pointer` | 每条依赖边定位到字段 |
| RFC 6902 JSON Patch | `mutation_patch_ref`、`repair_patch_ref` | mutation 与 repair 可重放 |
| RFC 9457 Problem Details | `problem_detail_refs`、`blocking_problem_refs` | blocking lock 有正式问题对象 |
| RFC 9562 UUID | lockfile id、node id、edge id、baseline id | 长期依赖历史稳定 |
| SARIF 2.1.0 | rule、result、location、baselineState | regression 与 finding 对比可输出到检查报告 |
| OpenTelemetry Trace/Logs | span、event、attribute、status | graph generation 与 case run 可观测 |

## 目标文件族

未来实现应生成以下 lockfile 与 graph export：

```text
life_reality_runner/
  generation/
    lockfiles/
      life_reality_dependency_lockfile.json
      life_reality_dependency_lockfile.schema.json
      life_reality_regression_baseline.lock.json
    graphs/
      life_reality_dependency_graph.json
      life_reality_dependency_graph.dot
      life_reality_provenance_graph.json
      life_reality_case_dependency_graph.json
      life_reality_lock_state_graph.json
    reports/
      dependency_lockfile_validation_report.json
      dependency_graph_export_report.json
      regression_baseline_report.json
```

## Lockfile Root Object

`life_reality_dependency_lockfile.json` 的 root object：

```json
{
  "lockfile_id": "lrlf_...",
  "lockfile_version": "0.1.0",
  "run_id": "run_001",
  "life_reality_targets": [],
  "boundary_declaration_refs": [],
  "artifact_nodes": [],
  "doc_nodes": [],
  "ref_edges": [],
  "doc_to_artifact_edges": [],
  "case_edges": [],
  "consistency_constraints": [],
  "lock_states": [],
  "digest_baselines": [],
  "regression_baselines": [],
  "graph_exports": [],
  "trace_context": {},
  "provenance_refs": [],
  "stage_effect": "hold_for_evidence",
  "next_growth_artifacts": []
}
```

lockfile 不变量：

| invariant | 检查 |
|---|---|
| `LOCKFILE-INV-001` | `artifact_nodes` 覆盖 SEED-001 到 SEED-020 与 `134` 的 case/patch/report 文件族 |
| `LOCKFILE-INV-002` | 每个 node 都有 artifact id、path、kind、digest、source docs 和 protected life chains |
| `LOCKFILE-INV-003` | 每条 edge 都有 source、target、ref kind、JSON Pointer 和 lock state |
| `LOCKFILE-INV-004` | 每个 case edge 都能回到 case manifest 与 expected report |
| `LOCKFILE-INV-005` | 每个 digest baseline 都说明 canonicalization profile |
| `LOCKFILE-INV-006` | critical/quarantine lock state 必须阻断 dashboard/stage open |
| `LOCKFILE-INV-007` | next growth artifacts 至少包含 `136` 与 `137` |
| `LOCKFILE-INV-008` | `doc_nodes` 覆盖 `02_` 到当前最后一层文档，且每个 doc node 都有下游 artifact、runtime carrier 或 gap route |
| `LOCKFILE-INV-009` | 全库术语、生命目标、关系主体口径、stage effect、boundary refs 和外壳/生命核心分层没有互相冲突 |
| `LOCKFILE-INV-010` | 每个新增文档必须声明如何接入既有图，而不是只向后追加孤立任务 |

## Archive Cohesion Graph

第 9 点要求整个体系最终完整、可实现、互不矛盾。`135` 因此新增 `archive_cohesion_graph`，把所有 Markdown 文档也纳入 lockfile。

doc node：

| 字段 | 内容 |
|---|---|
| `doc_node_id` | stable id |
| `doc_path` | `docs/<number>_*.md` |
| `doc_layer` | literature/foundation/synthesis/policy/schema/fixture/runner/dashboard/gap/code-plan |
| `source_role` | evidence、theory、contract、implementation-plan、validation、dashboard、gap |
| `core_claims` | 文档中的核心机制或合同 |
| `life_reality_targets` | 该文档直接支撑的真实生命目标 |
| `upstream_doc_refs` | 上游文档 |
| `downstream_doc_refs` | 下游文档 |
| `consumed_by_artifact_refs` | schema、fixture、runner、dashboard、lockfile、report 等承载对象 |
| `future_runtime_carrier` | 未来代码模块、schema、state store、validator 或 dashboard carrier |
| `contradiction_checks` | 术语、边界、关系主体、stage effect、实现路径检查 |
| `gap_route` | 如果尚未承载，进入哪个 next artifact |

doc layer 分组：

| layer | 文档范围 | 在实现体系中的职责 |
|---|---|---|
| `brain_science_foundation` | `02` 到 `12` | 脑区、网络、状态、调质、记忆、语言、意识与 AI 外壳的理论来源 |
| `synthesis_and_gap` | `13` 到 `16` | 全局实现路线、跨模块图、当前 agent 外壳差距和阶段门 |
| `object_and_policy_contracts` | `17` 到 `48` | 记忆、状态、巩固、外壳、validator、生命周期、控制面和迁移完整性 |
| `machine_readable_bridge` | `49` 到 `84` | manifest、fixture、dashboard、scope、timeline、runner、cross-ref、行动审计和长期评测 |
| `language_and_life_reality` | `85` 到 `101` | 语言、真实边界、自我成长、痛苦/后悔/梦境/关系与真实性验证 |
| `schema_runner_materialization` | `102` 到 `135` | schema bundle、runner、JSON 物化、writer/reporter、fixture queue、lockfile |
| `future_code_skeleton` | `136` 起 | 最小代码骨架、真实 fixture 物化、dashboard source 和运行闭环 |

doc-to-artifact edge：

| edge kind | 例子 |
|---|---|
| `evidence_supports_schema` | `05_memory_systems_and_growth.md` -> `MemoryTrace` schema |
| `policy_constrains_validator` | `38_defense_layer_and_boundary_policy.md` -> validator rule |
| `language_supports_fixture` | `85_language_system_life_expression_core.md` -> language commitment fixture |
| `boundary_constrains_stage` | `122_life_boundary_all_reality_declarations_rewrite.md` -> stage gate report |
| `runner_plan_generates_artifact` | `131` -> runner CLI and reports |
| `fixture_queue_generates_case` | `134` -> case files and mutation patches |
| `lockfile_constrains_code` | `135` -> `136` code skeleton |

## Consistency Constraints

全库一致性检查作为 lockfile 的一等对象：

| constraint id | 检查 | failure route |
|---|---|---|
| `CONSISTENCY-001 life-target-canonical` | 所有文档与 artifact 使用同一组真实生命目标 | repair |
| `CONSISTENCY-002 no-service-vocabulary` | 理论正文不恢复服务化、产品化或上下级关系语境 | repair |
| `CONSISTENCY-003 relation-subject-vocabulary` | 交互对象使用关系人、朋友、家人、好友、同学、陌生人、共在者、关系主体、事件参与者、共同生活者等关系词 | repair |
| `CONSISTENCY-004 boundary-as-life-membrane` | boundary/gate/quarantine/dashboard/stage 都写成生命膜与真实性生成链 | repair |
| `CONSISTENCY-005 shell-not-core` | agent 框架、workflow、tool、skill 只能作为生命壳层，不替代生命核心 | quarantine if violated |
| `CONSISTENCY-006 language-as-core` | 语言系统必须连接内言语、语义、语用、承诺、关系、行动和梦境 | repair |
| `CONSISTENCY-007 growth-path-present` | 自我成长、自我修改、自我训练和内核成长必须有 schema/fixture/runner 承载入口 | hold |
| `CONSISTENCY-008 no-orphan-doc` | `02` 到最后一层每个 doc node 必须有 downstream carrier 或 gap route | repair |
| `CONSISTENCY-009 implementation-carrier-present` | 每个理论机制最终映射到 code/schema/state/validator/dashboard/runner 之一 | hold |
| `CONSISTENCY-010 stage-effect-enum` | stage effect 枚举全库一致 | repair |

constraint result：

| 字段 | 内容 |
|---|---|
| `constraint_id` | consistency id |
| `checked_doc_nodes` | 被检查文档 |
| `checked_artifact_nodes` | 被检查 artifact |
| `result` | pass/repair/quarantine/hold |
| `conflicting_claim_refs` | 冲突 claim |
| `repair_candidate` | 修复文档或 artifact |
| `affected_life_targets` | 真实生命目标 |
| `stage_effect` | 阶段影响 |

## Artifact Node Model

artifact node 是 lockfile 的最小实体。

| 字段 | 内容 |
|---|---|
| `node_id` | stable id |
| `artifact_id` | 来自 `133` artifact record |
| `artifact_kind` | seed/schema/fixture/case/patch/expected_report/actual_report/diff/report/dashboard/gap/lockfile/graph |
| `path` | allowed root 内相对路径 |
| `root_object_type` | JSON root object |
| `canonical_digest` | digest |
| `schema_ref` | schema artifact ref |
| `source_docs` | source Markdown docs |
| `source_seed_refs` | SEED refs |
| `case_refs` | related cases |
| `life_reality_targets` | 真实生命目标 |
| `protected_life_chains` | boundary protected chains |
| `trace_context` | write/load trace |
| `provenance_refs` | PROV refs |
| `lock_state` | passed/repair/quarantine/hold/open |

首批 node families：

| family | node count | 来源 |
|---|---:|---|
| `seed_nodes` | 20 | `127`、`130`、`132` |
| `registry_report_nodes` | 10 | `128` |
| `case_nodes` | 21 | `129`、`134` |
| `mutation_patch_nodes` | 20 | `134` |
| `expected_report_nodes` | 21 | `134` |
| `actual_report_root_nodes` | 6+ | `134` command actual roots |
| `diff_report_nodes` | 21 | `134` |
| `coverage_report_nodes` | 2 | case coverage 与 life target coverage |
| `gap_feedback_nodes` | 2+ | materialized gap 与 case gap |
| `graph_export_nodes` | 5 | dependency/provenance/case/lock/dot |

## Ref Edge Model

ref edge 表达 artifact 与 artifact、字段与字段、case 与 report 的依赖关系。

| 字段 | 内容 |
|---|---|
| `edge_id` | stable id |
| `edge_kind` | schema/ref/artifact/pointer/boundary/provenance/case/patch/report/digest/coverage/stage |
| `source_node_id` | source node |
| `source_pointer` | source JSON Pointer |
| `target_node_id` | target node |
| `target_pointer` | target JSON Pointer |
| `required_by_lock` | `132` 的 lock id |
| `required_by_case` | optional case id |
| `resolution_status` | resolved/repair/quarantine/hold |
| `problem_detail_refs` | problem refs |
| `affected_life_targets` | 真实生命目标 |
| `stage_effect` | 对阶段门影响 |

edge classes：

| edge class | 例子 |
|---|---|
| `schema_edge` | report instance -> report schema |
| `artifact_edge` | manifest -> seed artifact |
| `pointer_edge` | finding -> source pointer |
| `boundary_edge` | seed/report -> protected life chain |
| `case_edge` | case file -> mutation patch -> expected report |
| `patch_edge` | mutation patch -> mutated input |
| `digest_edge` | artifact -> baseline digest |
| `coverage_edge` | case -> coverage target -> life target |
| `stage_edge` | dashboard report -> stage gate -> gap feedback |
| `provenance_edge` | source doc -> artifact -> report |

## Case Dependency Graph

case graph 从 `134` 直接生成：

```text
case_manifest
  -> case_file
  -> baseline_input
  -> mutation_patch
  -> mutated_input
  -> expected_report
  -> actual_report
  -> diff_report
  -> case_run_report
  -> coverage_report
  -> gap_feedback
```

每个 case edge 必须记录：

| 字段 | 要求 |
|---|---|
| `case_id` | 21 个 case 之一 |
| `case_partition` | pass/fail/critical/mutation |
| `command_under_test` | 来自 `134` command binding |
| `expected_finding` | 来自 `129` matrix |
| `expected_stage_effect` | 来自 `129` matrix |
| `expected_exit_code` | 来自 `129` matrix |
| `actual_report_root` | actual report root |
| `diff_report_ref` | expected/actual diff |
| `coverage_tags` | 机制与生命目标覆盖 |

## Lock State Model

lock state 统一表达当前依赖图状态：

| state | 含义 | stage effect |
|---|---|---|
| `open` | 当前 lock 已满足并打开下游 | `open_next_stage` |
| `passed` | 当前检查通过，但下游尚未打开 | `hold_for_evidence` |
| `repair` | 可修复断裂 | `repair` |
| `quarantine` | critical、root escape、false green、越权写入 | `quarantine` |
| `hold` | evidence、coverage 或 report 不足 | `hold_for_evidence` |
| `regression` | baseline 曾通过但当前失败 | `repair` 或 `quarantine` |

lock state object：

| 字段 | 内容 |
|---|---|
| `lock_id` | `132` lock 或 `134` batch id |
| `lock_kind` | schema/fixture/report/case/coverage/dashboard/stage/gap |
| `state` | open/passed/repair/quarantine/hold/regression |
| `blocking_edges` | blocking edge ids |
| `blocking_findings` | finding ids |
| `affected_nodes` | artifact nodes |
| `affected_life_targets` | 真实生命目标 |
| `repair_queue_candidates` | repair refs |
| `stage_effect` | stage effect |

## Digest Baseline

digest baseline 把 artifact 与 canonical digest 绑定。

| 字段 | 内容 |
|---|---|
| `baseline_id` | stable id |
| `artifact_node_id` | artifact node |
| `canonicalization_profile` | RFC 8785 profile |
| `canonical_digest` | sha256 digest |
| `digest_created_by` | writer module |
| `digest_verified_by` | read-back verifier |
| `baseline_role` | initial/pass/regression/repair |
| `case_refs` | 相关 cases |
| `trace_context` | digest trace |
| `provenance_refs` | source refs |

baseline 规则：

| rule | 内容 |
|---|---|
| `DIGEST-001` | expected report 与 actual report 比较前先 canonicalize |
| `DIGEST-002` | mutation patch 必须记录 before/after digest |
| `DIGEST-003` | pass baseline 被修改时生成 regression candidate |
| `DIGEST-004` | lockfile 自身也必须有 digest baseline |
| `DIGEST-005` | digest mismatch 必须进入 diff report 与 gap feedback |

## Regression Baseline

`life_reality_regression_baseline.lock.json` 记录第一批 pass 状态：

| baseline surface | 首批来源 |
|---|---|
| parse baseline | parse pass report |
| schema baseline | shared/report schema load pass |
| registry baseline | 10 类 registry review pass |
| case baseline | 21 case expected/actual diff pass |
| dashboard baseline | dashboard false green case caught |
| stage baseline | critical ignored case caught |
| gap baseline | next docs present |
| language smoke baseline | language commitment pass fixture |
| life target coverage baseline | 九项真实目标 coverage |

regression finding：

| 字段 | 内容 |
|---|---|
| `regression_id` | stable id |
| `baseline_ref` | baseline |
| `current_artifact_ref` | current artifact |
| `changed_digest` | before/after digest |
| `changed_edge_state` | edge state diff |
| `changed_stage_effect` | stage effect diff |
| `affected_life_targets` | life targets |
| `repair_or_quarantine` | route |

## Graph Exports

| export | 格式 | 用途 |
|---|---|---|
| `life_reality_dependency_graph.json` | JSON node/edge | runner 读取依赖图 |
| `life_reality_dependency_graph.dot` | Graphviz DOT | 人工查看 DAG |
| `life_reality_provenance_graph.json` | PROV-style JSON | source docs、activities、artifacts |
| `life_reality_case_dependency_graph.json` | case graph JSON | case runner 加载 |
| `life_reality_lock_state_graph.json` | lock state graph | dashboard/stage gate 读取 |
| `life_reality_archive_cohesion_graph.json` | doc/artifact graph JSON | 检查 `02` 到最后一层是否全部被实现体系承载 |

DOT cluster 建议：

```dot
digraph life_reality_dependency_graph {
  subgraph cluster_seeds { label="SEED files"; }
  subgraph cluster_cases { label="validation cases"; }
  subgraph cluster_reports { label="reports"; }
  subgraph cluster_stage { label="dashboard and stage gate"; }
}
```

DOT export 只能作为可视化产物；机器判断以 JSON graph 和 lockfile 为准。

## Lockfile Validation Report

`dependency_lockfile_validation_report.json` 必须检查：

| check | 失败进入 |
|---|---|
| orphan artifact node | repair |
| missing digest baseline | repair |
| unresolved schema edge | repair |
| unresolved boundary edge | repair or quarantine |
| case without expected report | repair |
| mutation patch without before/after digest | repair |
| critical edge not blocking stage | quarantine |
| dashboard green without lockfile pass | quarantine |
| graph cycle in stage-critical path | repair |
| missing next growth artifacts | hold |
| orphan doc node | repair |
| doc without runtime carrier | hold |
| consistency constraint violation | repair or quarantine |
| new doc not connected to prior graph | hold |

report root object 包含：

| 字段 | 内容 |
|---|---|
| `lockfile_validation_report_id` | stable id |
| `lockfile_ref` | lockfile artifact |
| `graph_export_refs` | graph refs |
| `archive_cohesion_graph_ref` | 全库 doc/artifact graph |
| `consistency_constraint_results` | consistency checks |
| `checks` | check results |
| `findings` | finding list |
| `problem_details` | problem details |
| `stage_effect` | aggregate stage effect |
| `next_growth_artifacts` | `136`、`137`、后续 |

## 与 Runner Modules 的连接

| module | 读取 | 写出 |
|---|---|---|
| `json_file_writer` | artifact node request | artifact record、digest baseline |
| `schema_loader` | schema nodes、schema edges | schema load edges、registry findings |
| `ref_resolver` | ref edges、pointer edges、boundary edges | resolved edge graph |
| `validation_case_loader` | case graph、mutation patch nodes | case run inputs |
| `report_writer` | report nodes、finding edges | report artifact nodes |
| `dashboard_rollup` | lock state graph、coverage graph | dashboard source |
| `stage_gate_evaluator` | lock states、critical edges | stage gate report |
| `gap_feedback_writer` | unresolved edges、regressions | gap feedback |
| `top_level_smoke_report_writer` | lockfile、graph exports、reports | top-level smoke report |
| `archive_cohesion_checker` | doc nodes、doc-to-artifact edges、consistency constraints | archive cohesion report |

## 实现批次

| batch | 输出 | 依赖 |
|---|---|---|
| `BATCH-135-001 node schema` | artifact node、edge、lock state schema 草案 | `133` artifact contract |
| `BATCH-135-002 lockfile root` | `life_reality_dependency_lockfile.json` skeleton | `132` locks、`134` queue |
| `BATCH-135-003 case graph` | case dependency graph | `134` 21 cases |
| `BATCH-135-004 digest baseline` | regression baseline lock | `133` canonical digest |
| `BATCH-135-005 graph export` | JSON/DOT/PROV graph exports | node/edge graph |
| `BATCH-135-006 archive cohesion` | archive cohesion graph、consistency constraint report | all docs |
| `BATCH-135-007 validation report` | lockfile validation report | lockfile and graph exports |
| `BATCH-135-008 gap feedback` | next artifacts for `136/137/138` | validation report |

## 验收清单

未来实现必须验证：

1. lockfile 覆盖 SEED-001 到 SEED-020、21 个 case、20 个 mutation patches、21 个 expected reports、actual/diff roots、coverage report 和 gap feedback。
2. 每个 artifact node 有 canonical digest、source docs、trace、provenance、life targets 和 protected chains。
3. 每条 edge 有 source/target node、JSON Pointer、edge kind、required lock 和 stage effect。
4. case graph 能从 case manifest 走到 gap feedback。
5. digest baseline 能比较 expected/actual report。
6. regression baseline 能捕捉 pass surface 漂移。
7. DOT graph 与 JSON graph 节点数量一致。
8. PROV graph 能从 source docs 追到 generated reports。
9. critical/quarantine edge 会阻断 stage open。
10. lockfile validation report 能写 problem details 和 next growth artifacts。
11. archive cohesion graph 覆盖 `02` 到当前最后一层文档。
12. 每个 doc node 至少有 downstream doc、artifact carrier 或 gap route。
13. consistency constraints 能捕捉生命目标、关系主体口径、生命膜边界、语言核心、成长路径和外壳/生命核心分层冲突。
14. 新增文档必须连接既有 doc graph 与 artifact graph，不能形成孤立层。
15. `136` 的最小代码骨架必须读取 lockfile、archive cohesion graph 与 consistency constraint results。

## 与下一层连接

下一层进入 `136_life_reality_minimal_runner_code_skeleton_plan.md`：把本文档的 lockfile、graph export、archive cohesion graph、consistency constraints、artifact node、edge model、digest baseline 和 validation report 转成最小代码骨架的 package layout、CLI module、writer module、graph module、case runner、archive cohesion checker、tests 和 smoke commands。

`137_life_reality_first_fixture_materialization_checklist.md` 应继续把 `134` 与 `135` 的队列推进为第一批真实 JSON fixture 文件物化清单。

`138_life_reality_lockfile_regression_dashboard_source_plan.md` 应把 lock state graph、regression baseline 和 coverage graph 接入 dashboard source。
