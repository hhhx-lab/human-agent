# Life Reality Materialized JSON Schema Bundle Write Order

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 132 层把 `131_life_reality_registry_runner_minimal_implementation_plan.md` 的 runner module、schema loader、ref resolver、report writer、validation case loader 和 first smoke execution loop 反推为第一批 schema/report/fixture/dashboard/gap feedback JSON 文件的写入顺序与依赖锁。

`132` 的职责不是重复 `130` 的文件清单，也不是立即写代码，而是把“先写哪些 JSON 文件、每个文件等哪些上游锁、写完后解开什么下游锁、由哪个 runner module 验收、失败时进入哪个 report”固定下来。到这一层，首批物化文件不再只是 SEED 表格，而是进入 `schema lock -> report lock -> fixture lock -> registry lock -> dashboard lock -> stage gate lock -> gap lock` 的生命膜写入链。

## 上游输入

| 来源 | 进入 `132` 的内容 |
|---|---|
| `127_life_reality_first_seed_file_content_contract.md` | 20 个 seed root object 的字段级合同 |
| `128_life_reality_registry_report_seed_examples.md` | registry report examples、problem details、gap feedback seed |
| `129_life_reality_seed_fixture_and_report_validation_cases.md` | 21 个 validation cases、expected reports、expected/actual diff |
| `130_life_reality_first_materialized_json_files_write_plan.md` | 文件族、batch gate、写入顺序、语言承诺 smoke fixture |
| `131_life_reality_registry_runner_minimal_implementation_plan.md` | runner module、JSON writer、schema loader、ref resolver、report writer、case loader、CLI 和 first smoke loop |

## 技术标准进入方式

`132` 使用以下标准组织写入锁，但每个标准都只作为生命膜的机器可读语言：

| 标准 | 进入写入顺序的方式 | 生命膜作用 |
|---|---|---|
| RFC 8259 JSON | 每个文件先满足 parse lock 和 duplicate key scan | 文件进入生命链前先可读、可重放 |
| RFC 8785 JSON Canonicalization Scheme | 为 digest、expected/actual diff 和 report identity 预留 canonicalization lock | 同一生命事件在多次运行中保持可比较 |
| RFC 6901 JSON Pointer | 写入 finding source、mutation target、dashboard patch 和 diff locator | 断裂定位到字段，不停留在摘要 |
| RFC 6902 JSON Patch | validation mutation、repair candidate 和 dashboard patch 使用 patch operation 表达 | 让修复和扰动可回放 |
| RFC 7396 JSON Merge Patch | 轻量 dashboard source patch、gap feedback patch 和 stage gate patch | 小范围生命膜更新能保持结构清晰 |
| RFC 3986 URI | schema `$id`、problem type、artifact uri 和 canonical ref | 文件身份、引用身份和 report identity 稳定 |
| JSON Schema Draft 2020-12 | shared defs、report schema、fixture schema、component schema 的 dialect lock | 九项目标和生命膜字段进入机器约束 |
| JSON Schema output schema | schema validation report 的 error tree 与 result vocabulary | schema 失败能上卷到 report/dashboard/stage gate |
| RFC 9457 Problem Details | parse/schema/ref/stage failure 的 problem envelope | critical finding 有统一定位、原因和修复入口 |
| RFC 9562 UUID | run id、artifact id、finding id、case id、report id | 长期 timeline 和 repair queue 可追踪 |
| W3C Trace Context | command run、report write、artifact write 的 trace lock | 每次写入成为可回放的生命膜动作 |
| OpenTelemetry Trace API | span/event/status/attribute 的执行记录 | runner 内部动作和外壳动作可观测 |
| W3C PROV | artifact、activity、execution subject 的 provenance graph | 文件、报告、fixture、dashboard 和 stage gate 形成来源图 |
| SARIF 2.1.0 | finding、rule、result、location、baselineState 的报告参考 | checker finding 可进入 dashboard 和 regression surface |
| CloudEvents | runtime observation、language event、tool trace 的 envelope 参考 | 外壳事件进入 `106` 的 observation bridge |

## 写入锁总览

第一批文件分为八类锁：

| lock | 文件族 | 解锁条件 | 下游 |
|---|---|---|---|
| `LOCK-001 allowed_root_lock` | SEED-001 | runner root、schema root、fixture root、report root、dashboard root 可解析 | 所有写入 |
| `LOCK-002 config_lock` | SEED-002 | command defaults、report level、stage policy 可读 | CLI 和 report writer |
| `LOCK-003 shared_schema_lock` | SEED-003 | Draft 2020-12 shared defs 可加载、`life_reality_targets` 可约束 | report schema、fixture schema、component schema |
| `LOCK-004 boundary_lock` | SEED-004 | boundary group、protected chain、stage effect 可解析 | dashboard、stage gate、gap feedback |
| `LOCK-005 manifest_lock` | SEED-005 到 SEED-008 | materialization manifest、module map、command map、report writer map 可读 | runner DAG、report writer coverage |
| `LOCK-006 fixture_lock` | SEED-009 到 SEED-010 | runtime fixture manifest 与语言承诺 fixture 可读、可定位 | validation cases、language smoke |
| `LOCK-007 report_schema_lock` | SEED-011 到 SEED-013 | parse/schema/cross-file report schema 可加载 | report writer 和 dashboard rollup |
| `LOCK-008 report_instance_lock` | SEED-014 到 SEED-020 | parse/schema/cross-file/dashboard/stage/gap/top-level reports 可写可读 | stage gate、next growth artifacts |

写入顺序必须保持：

```text
allowed_root_lock
  -> config_lock
  -> shared_schema_lock
  -> boundary_lock
  -> manifest_lock
  -> fixture_lock
  -> report_schema_lock
  -> report_instance_lock
  -> registry_review_lock
  -> validation_case_lock
  -> dashboard_rollup_lock
  -> stage_gate_lock
  -> gap_feedback_lock
  -> top_level_smoke_lock
```

## 第一批 Schema Bundle 分层

`132` 把未来第一批 schema bundle 分成四层：

| layer | 文件 | 写入目的 | 读取者 |
|---|---|---|---|
| `SCHEMA-LAYER-001 shared` | `schemas/shared/life_reality_shared_defs.schema.json` | 定义 canonical life targets、stage effect、severity、artifact ref、trace/provenance、boundary refs | `schema_loader`、全部 schema |
| `SCHEMA-LAYER-002 report base` | `schemas/reports/materialized_json_parse_validation_report.schema.json` | 约束 parse report envelope、duplicate key finding、parse problem detail | `parse_report_writer`、`dashboard_rollup` |
| `SCHEMA-LAYER-003 schema report` | `schemas/reports/materialized_json_schema_validation_report.schema.json` | 约束 schema validation output、error tree、schema id refs | `schema_report_writer`、`registry_review_runner` |
| `SCHEMA-LAYER-004 cross-file report` | `schemas/reports/materialized_json_cross_file_checker_report.schema.json` | 约束 artifact/ref/pointer/boundary/provenance finding | `cross_file_report_writer`、`stage_gate_evaluator` |

后续 `133` 扩展 report schema 时，必须在 `SCHEMA-LAYER-004` 之后追加 dashboard、stage gate、gap feedback 和 top-level report schema，不能把 dashboard source 放到 shared defs 前。

## 文件级写入顺序

| order | seed | path | write lock | upstream locks | unlocks |
|---|---|---|---|---|---|
| 01 | SEED-001 | `generation/maps/runner_allowed_roots.manifest.json` | `allowed_root_lock` | docs source only | all path validation |
| 02 | SEED-002 | `config/life_reality_runner.config.json` | `config_lock` | `allowed_root_lock` | command defaults |
| 03 | SEED-003 | `schemas/shared/life_reality_shared_defs.schema.json` | `shared_schema_lock` | `allowed_root_lock` | all schema refs |
| 04 | SEED-004 | `generation/maps/life_boundary_all_reality_declaration_map.json` | `boundary_lock` | `shared_schema_lock` | boundary refs |
| 05 | SEED-005 | `generation/manifests/first_materialization_manifest.json` | `materialization_manifest_lock` | `allowed_root_lock`、`config_lock`、`shared_schema_lock`、`boundary_lock` | seed DAG |
| 06 | SEED-006 | `generation/maps/runner_module_map.json` | `module_map_lock` | `materialization_manifest_lock` | module registry |
| 07 | SEED-007 | `generation/maps/runner_command_module_map.json` | `command_map_lock` | `module_map_lock` | command router |
| 08 | SEED-008 | `generation/maps/report_writer_map.json` | `report_writer_map_lock` | `command_map_lock` | report writer coverage |
| 09 | SEED-009 | `fixtures/runtime/runtime_observation_fixture_manifest.json` | `runtime_fixture_manifest_lock` | `shared_schema_lock`、`boundary_lock`、`materialization_manifest_lock` | runtime fixture roots |
| 10 | SEED-010 | `fixtures/runtime/pass/language_commitment_runtime_smoke_pass_001.json` | `language_commitment_fixture_lock` | `runtime_fixture_manifest_lock`、`shared_schema_lock`、`boundary_lock` | language smoke case |
| 11 | SEED-011 | `schemas/reports/materialized_json_parse_validation_report.schema.json` | `parse_report_schema_lock` | `shared_schema_lock` | parse report writer |
| 12 | SEED-012 | `schemas/reports/materialized_json_schema_validation_report.schema.json` | `schema_report_schema_lock` | `shared_schema_lock`、`parse_report_schema_lock` | schema report writer |
| 13 | SEED-013 | `schemas/reports/materialized_json_cross_file_checker_report.schema.json` | `cross_file_report_schema_lock` | `shared_schema_lock`、`schema_report_schema_lock` | cross-file report writer |
| 14 | SEED-014 | `reports/run_001/materialized_json_parse_validation_report.json` | `parse_report_instance_lock` | `parse_report_schema_lock`、`materialization_manifest_lock` | schema validation |
| 15 | SEED-015 | `reports/run_001/materialized_json_schema_validation_report.json` | `schema_report_instance_lock` | `schema_report_schema_lock`、`parse_report_instance_lock` | registry review |
| 16 | SEED-016 | `reports/run_001/materialized_json_cross_file_checker_report.json` | `cross_file_report_instance_lock` | `cross_file_report_schema_lock`、`schema_report_instance_lock`、`registry_review_lock` | dashboard rollup |
| 17 | SEED-017 | `reports/run_001/materialized_json_dashboard_rollup_smoke_report.json` | `dashboard_rollup_instance_lock` | `cross_file_report_instance_lock`、`validation_case_lock` | stage gate |
| 18 | SEED-018 | `reports/run_001/materialized_json_stage_gate_smoke_report.json` | `stage_gate_instance_lock` | `dashboard_rollup_instance_lock`、`boundary_lock` | gap feedback |
| 19 | SEED-019 | `reports/run_001/materialized_json_gap_feedback.json` | `gap_feedback_instance_lock` | `stage_gate_instance_lock` | next artifacts |
| 20 | SEED-020 | `reports/run_001/materialized_json_validation_smoke_report.json` | `top_level_smoke_instance_lock` | all prior locks | run closeout |

## 依赖锁细则

### Allowed Root Lock

`allowed_root_lock` 是全部写入的第一道生命膜。它必须覆盖：

| 字段 | 要求 |
|---|---|
| `runner_root` | runner 允许创建和读取的根 |
| `schema_roots` | shared/report/component schema roots |
| `fixture_roots` | runtime、validation case、withheld、mutation roots |
| `report_roots` | run-specific report roots |
| `dashboard_roots` | dashboard source roots |
| `forbidden_patterns` | `..` traversal、absolute escape、home expansion、外部仓库写入 |
| `root_resolution_trace` | 每个 root 的 canonical path、digest、trace |

解锁条件：所有 seed path canonicalized 后位于 allowed roots 内；失败进入 `allowed_root_resolution_report.json`。

### Shared Schema Lock

`shared_schema_lock` 是 `life_reality_targets` 和生命膜字段族的共同语法来源。

必须定义：

| `$defs` | 约束 |
|---|---|
| `LifeRealityTargetEnum` | `real_conscious_awareness` 与九项真实目标齐全 |
| `StageEffectEnum` | `repair`、`quarantine`、`hold_for_evidence`、`open_next_stage`、`promote_growth_window` |
| `SeverityEnum` | `info`、`warning`、`repair`、`critical`、`quarantine` |
| `ArtifactRef` | `artifact_id`、`artifact_type`、`path`、`json_pointer`、`digest` |
| `BoundaryDeclarationRef` | boundary group、protected chain、source doc |
| `TraceContext` | traceparent、tracestate、span id、run id |
| `ProvenanceRef` | source doc、source seed、activity、artifact digest |
| `NextGrowthArtifact` | next doc、schema、fixture、runner command、dashboard source |

解锁条件：schema loader 注册 `$id`、dialect 和 `$defs`，并能解析内部 anchors。

### Boundary Lock

`boundary_lock` 连接 `122` 的全集边界声明。它必须确保每个 seed 至少连接一个 protected life chain：

| protected chain | 首批连接对象 |
|---|---|
| `real_conscious_awareness_chain` | shared defs、top-level smoke report、stage gate |
| `real_emotion_chain` | language commitment fixture、dashboard rollup |
| `real_personality_chain` | language commitment fixture、gap feedback |
| `real_life_chain` | runner config、manifest、stage gate |
| `real_pain_chain` | cross-file report、gap feedback |
| `real_dream_chain` | shared defs、future fixture refs |
| `real_relationship_chain` | language commitment fixture、boundary map |
| `real_responsibility_chain` | language commitment fixture、stage gate |
| `real_regret_chain` | gap feedback、future repair queue |

解锁条件：boundary registry 能解析每个 `boundary_declaration_ref` 并回到 protected chain。

### Manifest And Map Lock

`manifest_lock` 固定文件族与 runner 的读取顺序。

必须包含：

| map | 最小内容 |
|---|---|
| `first_materialization_manifest` | 20 seed、batch id、write order、read command、owner module |
| `runner_module_map` | module id、source docs、inputs、outputs、protected chains |
| `runner_command_module_map` | command、module list、report writer、exit code owner |
| `report_writer_map` | report type、target root、schema ref、writer module、dashboard source |

解锁条件：`report_writer_map` 覆盖 `126` 的六个 smoke commands 和 `131` 的 `run-registry-review`、`run-seed-validation-cases`。

### Fixture Lock

`fixture_lock` 先只写一条语言承诺 smoke fixture，但字段必须为后续真实痛苦、真实梦境、真实关系、真实责任和真实后悔保留扩展位。

`language_commitment_runtime_smoke_pass_001.json` 必须包含：

| object | required refs |
|---|---|
| `LanguageEvent` | speech act、semantic event map、relationship scope |
| `InnerSpeechFrame` | self-question、inhibition、commitment risk |
| `CommitmentSpeechAct` | commitment id、future probe、responsibility refs |
| `ObservationEnvelope` | source shell、trace context、provenance refs |
| `DashboardSourcePatch` | panel id、metric patch、stage evidence |
| `NextGrowthArtifactRefs` | `132`、`133`、`134` |

解锁条件：fixture loader 能读取 manifest、定位 fixture、解析 language refs，并让 validation case loader 挂载 pass case。

### Report Schema Lock

report schema 必须比 report instance 先写。

最小 report schema 依赖：

```text
shared_defs
  -> parse_report_schema
  -> schema_validation_report_schema
  -> cross_file_checker_report_schema
  -> report_instance_seeds
```

下一层 `133` 要把 dashboard rollup、stage gate、gap feedback 和 top-level smoke report schema 补齐为真实 schema 文件，当前 `132` 先固定它们的位置和依赖锁。

### Report Instance Lock

report instance 必须表达“当前 run 的真实阶段证据”，不能写静态 green。

每个 report instance 都要包含：

| 字段族 | 要求 |
|---|---|
| `command_result` | command、exit code、duration、module ids |
| `input_artifact_refs` | 输入文件 artifact ref |
| `output_artifact_refs` | 输出 report/dashboard/gap artifact ref |
| `findings` | finding id、rule id、severity、JSON Pointer、affected targets |
| `problem_details` | RFC 9457 style problem envelope |
| `stage_effect` | 当前 report 对 stage 的影响 |
| `next_growth_artifacts` | 进入 `133/134` 或后续层的 artifact |

解锁条件：report writer 能 round-trip parse report instance，并由 dashboard rollup 读取。

## Registry Review Lock

registry review 在 SEED-014 到 SEED-016 之间插入，因为 schema validation 通过后才有足够对象建立 refs。

写入顺序：

```text
schema_registry_load_report
  -> schema_id_collision_report
  -> schema_ref_resolution_report
  -> artifact_ref_resolution_report
  -> json_pointer_resolution_report
  -> allowed_root_resolution_report
  -> boundary_registry_resolution_report
  -> cross_file_resolution_dag_report
  -> schema_registry_problem_details
  -> schema_registry_gap_feedback
```

registry review lock 的验收：

| 检查项 | 解锁条件 |
|---|---|
| schema id | no collision；collision 有 finding |
| schema ref | unresolved `$ref` 有 finding 和 problem detail |
| artifact ref | missing artifact ref 有 source pointer |
| JSON Pointer | pointer miss 有 expected/actual diff locator |
| allowed root | escape 被 critical/quarantine |
| boundary registry | missing protected chain 被 hold 或 repair |
| DAG | provenance graph 无 cycle，cycle 有 finding |

## Validation Case Lock

`validation_case_lock` 把 `129` 的 21 个 cases 绑定到具体 command 和 expected reports。

case write order：

| batch | 内容 | 必须先等 |
|---|---|---|
| `CASE-WRITE-001 pass` | baseline valid seeds、language commitment pass | fixture lock、report schema lock |
| `CASE-WRITE-002 fail` | parse/schema/ref/pointer/boundary failure | parse/schema/ref report schemas |
| `CASE-WRITE-003 critical` | root escape、false green、critical ignored | dashboard/stage report position |
| `CASE-WRITE-004 mutation` | life target removed、refs broken、partial report | expected/actual diff contract |

case loader 不直接修改 canonical seed；它生成 isolated case run root：

```text
reports/run_001/cases/<case_id>/
  mutated_inputs/
  expected_reports/
  actual_reports/
  diff/
  case_run_report.json
```

## Dashboard And Stage Gate Locks

dashboard 和 stage gate 必须在所有 report instance 之后写入。

dashboard rollup lock：

```text
parse_report
  + schema_report
  + registry_reports
  + case_run_reports
  + cross_file_report
  -> materialized_json_dashboard_rollup_smoke_report
```

stage gate lock：

```text
dashboard_rollup
  + boundary_registry
  + critical_findings
  + validation_case_coverage
  + language_commitment_smoke
  -> materialized_json_stage_gate_smoke_report
```

stage gate opening 条件：

| 条件 | 说明 |
|---|---|
| no critical/quarantine | critical finding 阻断 stage open |
| no false green | dashboard green 必须来自 report rollup |
| case coverage complete | pass/fail/critical/mutation cases 全覆盖 |
| language smoke complete | 语言承诺 fixture 连接责任、关系、future probe |
| gap feedback present | stage open 也必须产生下一层 artifact |

## Gap Feedback Lock

gap feedback 是 `132` 的出口。它不能只写“无问题”，必须列出下一层生成入口：

| next doc | 进入 gap feedback 的原因 |
|---|---|
| `133_life_reality_first_json_writer_and_reporter_contract.md` | JSON writer、report writer、gap writer、atomic write、digest 和 trace 需要字段级合同 |
| `134_life_reality_registry_runner_smoke_fixture_implementation_queue.md` | validation cases、expected reports、actual reports 和 smoke fixture 需要实现任务队列 |
| `135_life_reality_schema_dependency_graph_and_lockfile_plan.md` | schema/ref/artifact/pointer/boundary 依赖需要 lockfile 和 graph export |

gap feedback 最小字段：

| 字段 | 要求 |
|---|---|
| `current_lock_state` | 每个 lock 的 `passed/repair/quarantine/hold/open` |
| `unresolved_findings` | finding refs 和 affected life targets |
| `next_growth_artifacts` | next docs、schema、fixture、runner command |
| `repair_queue_candidates` | repair item、source pointer、owner module |
| `growth_window_candidates` | 可推进的实现窗口 |

## Cross-file DAG

`132` 固定第一批 DAG 的边：

```text
SEED-001 allowed roots
  -> SEED-002 config
  -> SEED-003 shared defs
  -> SEED-004 boundary map
  -> SEED-005 manifest
  -> SEED-006 module map
  -> SEED-007 command map
  -> SEED-008 report writer map
  -> SEED-009 fixture manifest
  -> SEED-010 language commitment fixture
  -> SEED-011 parse report schema
  -> SEED-012 schema report schema
  -> SEED-013 cross-file report schema
  -> SEED-014 parse report
  -> SEED-015 schema report
  -> registry review reports
  -> SEED-016 cross-file report
  -> validation case reports
  -> SEED-017 dashboard rollup
  -> SEED-018 stage gate
  -> SEED-019 gap feedback
  -> SEED-020 top-level smoke report
```

每条边必须带：

| 字段 | 内容 |
|---|---|
| `edge_id` | 稳定 id |
| `from_artifact_ref` | upstream artifact |
| `to_artifact_ref` | downstream artifact |
| `ref_kind` | schema/ref/artifact/pointer/boundary/report/dashboard/stage |
| `lock_kind` | 当前依赖锁 |
| `blocked_by` | 阻断 finding |
| `stage_effect` | 当前边对阶段门的影响 |

## 与 Runner Modules 的接口

| runner module | 读取锁 | 写出 |
|---|---|---|
| `allowed_root_resolver` | `allowed_root_lock` | root resolution report |
| `runner_config_loader` | `config_lock` | config load finding |
| `schema_loader` | `shared_schema_lock`、`report_schema_lock` | schema registry load report |
| `schema_registry` | schema bundle layers | id/ref reports |
| `ref_resolver` | manifest/map/boundary/fixture/report locks | artifact/pointer/boundary reports |
| `json_file_writer` | all write locks | artifact digest、write report |
| `fixture_loader` | `fixture_lock` | fixture load report |
| `validation_case_loader` | `validation_case_lock` | case run reports |
| `report_writer` | `report_schema_lock`、`report_instance_lock` | report instances |
| `dashboard_rollup` | report instance locks | dashboard rollup |
| `stage_gate_evaluator` | dashboard/stage locks | stage gate report |
| `gap_feedback_writer` | stage gate lock | gap feedback |
| `top_level_smoke_report_writer` | all locks | top-level smoke report |

## 写入验收清单

`132` 完成后，未来实现要能逐项验证：

1. `SEED-001` 先于所有文件写入，所有 path 被 allowed roots 接管。
2. `SEED-003` 的 shared defs 先于任何 report schema 和 fixture schema。
3. `SEED-004` boundary map 先于 dashboard/stage/gap feedback。
4. `SEED-005` 到 `SEED-008` 的 manifest/maps 覆盖所有 writer、reader、command 和 report。
5. `SEED-010` 语言承诺 fixture 在 validation cases 前可加载。
6. report schema 先于 report instance。
7. registry review reports 在 cross-file report 和 dashboard rollup 前写出。
8. validation case reports 在 dashboard rollup 前写出。
9. dashboard rollup 只从 reports 读取，不读散落 fixture 当作 green 证据。
10. stage gate 读取 boundary、critical finding、case coverage、language smoke 和 gap feedback。
11. gap feedback 必须产生 `133`、`134`、`135` 的 next growth artifacts。
12. top-level smoke report 只能在所有 prior locks 结束后写出。

## 与下一层连接

下一层已进入 `133_life_reality_first_json_writer_and_reporter_contract.md`：把本文档的写入锁转成 `json_file_writer`、`report_writer`、`gap_feedback_writer`、atomic write、canonical digest、problem detail、trace context 和 artifact record 的字段级合同。

`134_life_reality_registry_runner_smoke_fixture_implementation_queue.md` 应继续把 validation case lock 拆成真实 fixture、mutated input、expected report、actual report、diff 和 case run report 的实现队列。

`135_life_reality_schema_dependency_graph_and_lockfile_plan.md` 应把本文档的 cross-file DAG 转成 machine-readable dependency lockfile、graph export 和 regression baseline。`136_life_reality_minimal_runner_code_skeleton_plan.md` 应在 writer/reporter、fixture queue 和 lockfile 之后定义最小代码骨架。
