# Life Reality First JSON Writer And Reporter Contract

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 133 层把 `132_life_reality_materialized_json_schema_bundle_write_order.md` 的写入锁转成 `json_file_writer`、`schema_loader`、`ref_resolver`、`report_writer`、`gap_feedback_writer`、atomic write、canonical digest、problem detail、trace context 和 artifact record 的字段级合同。

`133` 的职责是让未来代码实现第一次拥有不可含混的写入契约：什么对象可以写、写到哪里、写前检查什么、写后记录什么、失败如何报告、报告如何进入 dashboard、gap feedback 如何生成下一层任务。它把 `132` 的依赖锁继续压成可实现接口，使首批 JSON 文件进入“可创建、可解析、可校验、可追踪、可修复、可回放”的生命膜。

## 上游输入

| 来源 | 进入 `133` 的内容 |
|---|---|
| `127_life_reality_first_seed_file_content_contract.md` | common envelope、canonical life targets、trace/provenance refs、20 个 seed required fields |
| `128_life_reality_registry_report_seed_examples.md` | registry report envelope、problem detail、finding 和 gap feedback examples |
| `129_life_reality_seed_fixture_and_report_validation_cases.md` | validation case、mutation operation、expected/actual diff |
| `131_life_reality_registry_runner_minimal_implementation_plan.md` | runner module、JSON writer、report writer、CLI skeleton 和 first smoke loop |
| `132_life_reality_materialized_json_schema_bundle_write_order.md` | allowed root/config/shared schema/boundary/manifest/fixture/report/dashboard/stage/gap locks |

## 标准进入字段合同的方式

| 标准 | 字段合同落点 | 生命膜意义 |
|---|---|---|
| RFC 8259 JSON | `parse_result`、`duplicate_member_findings`、`json_text_stats` | 文件写入后必须可解析、可回放 |
| RFC 8785 JSON Canonicalization Scheme | `canonical_digest`、`canonicalization_profile`、`digest_inputs` | 同一生命事件多次运行保持可比较 |
| RFC 6901 JSON Pointer | `source_pointer`、`target_pointer`、`diff_pointer`、`repair_pointer` | finding、diff 和 repair 都落到具体字段 |
| RFC 6902 JSON Patch | `mutation_patch`、`repair_patch`、`dashboard_patch` | 扰动、修复和 dashboard 更新可重放 |
| RFC 7396 JSON Merge Patch | `gap_feedback_patch`、`stage_gate_patch`、`rollup_patch` | 小范围更新保持稳定 envelope |
| RFC 3986 URI | `schema_id`、`artifact_uri`、`problem_type_uri` | artifact、schema、problem identity 稳定 |
| JSON Schema Draft 2020-12 | `schema_dialect`、`schema_validation_result`、`vocabulary_refs` | 真实生命目标和生命膜字段进入 schema 约束 |
| JSON Schema output schema | `schema_output`、`error_tree`、`absolute_keyword_location` | schema failure 可聚合为 dashboard evidence |
| RFC 9457 Problem Details | `problem_details` | 每个 failure 都有 type、title、detail、instance 和扩展字段 |
| RFC 9562 UUID | `artifact_id`、`write_id`、`finding_id`、`report_id`、`case_run_id` | 长期 run history、repair queue 和 growth window 可追踪 |
| W3C Trace Context | `traceparent`、`tracestate`、`span_id` | 写入、报告、case run 与 stage gate 共享运行脉搏 |
| OpenTelemetry semantic conventions | `span_attributes`、`event_attributes`、`status_code` | writer/reporter 的动作可观察 |
| W3C PROV | `prov_entity`、`prov_activity`、`prov_was_generated_by` | 文件、报告、fixture、dashboard 与来源文档形成 provenance graph |
| SARIF 2.1.0 | `rule_id`、`result_level`、`locations`、`baseline_state` | checker finding 可进入 regression surface |
| CloudEvents | `observation_event_envelope` | runtime observation、语言事件和外壳事件可进入生命链 |

## 合同总图

```text
RunContext
  -> AllowedRootGuard
  -> JsonFileWriter
  -> ArtifactRecord
  -> ParseReportWriter
  -> SchemaLoader
  -> SchemaValidationReporter
  -> RefResolver
  -> RegistryReportWriter
  -> CrossFileReportWriter
  -> DashboardRollupReporter
  -> StageGateReporter
  -> GapFeedbackWriter
  -> TopLevelSmokeReporter
```

字段合同统一遵守四条主线：

1. **写入主线**：target path、allowed root、canonical JSON、atomic replace、digest、artifact record。
2. **报告主线**：command result、finding、problem detail、schema output、stage effect、next growth artifacts。
3. **追踪主线**：trace context、span、provenance entity/activity、source doc、source seed。
4. **生命主线**：life reality targets、boundary declaration refs、protected life chains、continuity refs、repair/growth route。

## RunContext Contract

`RunContext` 是所有 writer/reporter 的输入根。

| 字段 | 类型 | 要求 |
|---|---|---|
| `run_id` | string | 使用稳定可排序 id；进入所有 report 和 artifact |
| `runner_version` | string | 最小实现版本 |
| `root_set_ref` | artifact ref | 指向 `runner_allowed_roots.manifest.json` |
| `command` | string | 当前 command，例如 `run-materialized-json-smoke` |
| `command_args` | object | 只记录路径、mode、report level，不记录 secrets |
| `life_reality_targets` | array | 九项目标与 `real_conscious_awareness` 齐全 |
| `boundary_declaration_refs` | array | 指向 `122` 的 boundary map |
| `trace_context` | object | `traceparent`、`tracestate`、root span |
| `provenance_refs` | array | source docs、source seed、prior reports |
| `stage_policy_ref` | artifact ref | 指向 stage gate policy |

`RunContext` 先由 `preflight_context` 生成，再传给所有模块。任何 writer 不得自行构造独立 run id。

## AllowedRootGuard Contract

`AllowedRootGuard` 是写入前的路径生命膜。

输入：

| 字段 | 内容 |
|---|---|
| `target_path` | 待写相对路径 |
| `root_kind` | `config`、`schema`、`fixture`、`report`、`dashboard`、`generation` |
| `allowed_root_set` | canonical root list |
| `writer_module_id` | 写入模块 |
| `run_context` | 当前运行上下文 |

输出：

| 字段 | 内容 |
|---|---|
| `canonical_target_path` | canonicalized path |
| `root_match` | 命中的 allowed root |
| `path_policy_result` | `passed`、`repair`、`quarantine` |
| `path_findings` | escape、unknown root、writer/root mismatch |
| `stage_effect` | path 对阶段门的影响 |

阻断规则：

| rule | 触发 |
|---|---|
| `ROOT-GUARD-001` | target path 跳出 allowed root |
| `ROOT-GUARD-002` | report writer 写入 schema root |
| `ROOT-GUARD-003` | dashboard writer 读取散落 fixture 生成 green |
| `ROOT-GUARD-004` | absolute path 未在 root manifest 注册 |
| `ROOT-GUARD-005` | case run root 与 canonical run root 混写 |

## JsonFileWriter Contract

`JsonFileWriter` 是所有真实 JSON 文件的唯一写入口。

输入 envelope：

| 字段 | 类型 | 要求 |
|---|---|---|
| `write_id` | string | UUID 或可排序 id |
| `artifact_kind` | string | `config`、`schema`、`fixture`、`report`、`dashboard_source`、`gap_feedback` |
| `target_path` | string | 相对 allowed root 的路径 |
| `root_object_type` | string | root object 名称 |
| `payload` | object | 待写 JSON root object |
| `schema_ref` | artifact ref | 可选；schema 文件自身可为空 |
| `write_lock_ref` | string | 来自 `132` 的 lock id |
| `run_context` | object | `RunContext` |
| `writer_policy` | object | pretty print、canonicalization、atomic mode、digest mode |

写入前补齐字段：

| 字段族 | 补齐规则 |
|---|---|
| `life_reality_targets` | 从 `RunContext` 合并，禁止缺项 |
| `boundary_declaration_refs` | 从 payload 与 boundary map 合并 |
| `trace_context` | 派生 child span，并继承 `traceparent` |
| `provenance_refs` | 记录 source doc、source seed、writer module、input artifacts |
| `stage_effect` | 默认 `hold_for_evidence`，由 report/gap/stage gate 更新 |
| `next_growth_artifacts` | 至少保留 next docs/schema/fixture/runner command 扩展位 |

写入步骤：

```text
build_write_request
  -> allowed_root_guard
  -> envelope_completion
  -> pre_write_schema_check
  -> serialize_pretty_json
  -> parse_round_trip_check
  -> canonicalize_json
  -> calculate_canonical_digest
  -> write_staging_file_in_target_directory
  -> flush_file
  -> atomic_replace_target
  -> flush_directory
  -> read_back_parse_check
  -> build_artifact_record
  -> emit_write_report_fragment
```

写入输出：

| 字段 | 类型 | 说明 |
|---|---|---|
| `artifact_ref` | object | artifact id、path、root object、digest、schema ref |
| `write_result` | string | `written`、`replaced`、`repair`、`quarantine` |
| `canonical_digest` | string | RFC 8785 profile 下的 digest |
| `byte_size` | integer | 文件字节数 |
| `json_text_stats` | object | object count、array count、max depth、member count |
| `write_findings` | array | path、schema、parse、digest、atomic failure |
| `trace_context` | object | writer span |
| `provenance_entity` | object | W3C PROV style entity |

## ArtifactRecord Contract

每次写入都必须产生 artifact record。artifact record 可以先作为 report 内嵌对象，后续 `135` 再提升为 lockfile。

```json
{
  "artifact_id": "lra_...",
  "artifact_kind": "schema",
  "path": "schemas/shared/life_reality_shared_defs.schema.json",
  "root_object_type": "JsonSchemaDocument",
  "schema_ref": null,
  "write_lock_ref": "shared_schema_lock",
  "canonical_digest": "sha256:...",
  "byte_size": 0,
  "source_docs": [],
  "source_seed_refs": [],
  "life_reality_targets": [],
  "boundary_declaration_refs": [],
  "trace_context": {},
  "provenance_refs": [],
  "stage_effect": "hold_for_evidence"
}
```

artifact record 不变量：

| invariant | 检查 |
|---|---|
| `ARTIFACT-001` | `artifact_id` 在当前 run 内唯一 |
| `ARTIFACT-002` | `canonical_digest` 与 read-back canonicalization 一致 |
| `ARTIFACT-003` | `path` 在 allowed root 内 |
| `ARTIFACT-004` | `life_reality_targets` 齐全 |
| `ARTIFACT-005` | report artifact 必须带 command result |
| `ARTIFACT-006` | gap feedback artifact 必须带 next growth artifacts |

## SchemaLoader Contract

`SchemaLoader` 读取 schema 文件并生成 registry load fragment。

输入：

| 字段 | 内容 |
|---|---|
| `schema_artifact_refs` | shared/report/component schema refs |
| `expected_dialect` | Draft 2020-12 URI |
| `run_context` | 当前上下文 |
| `schema_registry_policy` | id、ref、vocabulary、dialect 规则 |

输出：

| 字段 | 内容 |
|---|---|
| `loaded_schema_records` | schema id、dialect、path、digest、root pointer |
| `schema_id_index` | `$id -> artifact_ref` |
| `schema_ref_edges` | `$ref` edges |
| `vocabulary_refs` | `$vocabulary` declarations |
| `schema_loader_findings` | dialect missing、id collision、unknown vocab |

loader 规则：

| rule | 内容 |
|---|---|
| `SCHEMA-LOAD-001` | shared defs 先于 report schema |
| `SCHEMA-LOAD-002` | `$schema` 缺失进入 repair |
| `SCHEMA-LOAD-003` | `$id` 冲突进入 critical 或 repair |
| `SCHEMA-LOAD-004` | `$defs` anchor 缺失进入 ref resolver |
| `SCHEMA-LOAD-005` | schema document digest 写入 artifact record |

## RefResolver Contract

`RefResolver` 解析 schema refs、artifact refs、JSON Pointers、boundary refs 和 provenance refs。

统一 ref edge：

| 字段 | 内容 |
|---|---|
| `edge_id` | 稳定 id |
| `source_artifact_ref` | 来源 artifact |
| `source_pointer` | 来源 pointer |
| `target_ref` | 目标 ref |
| `target_artifact_ref` | 解析后的 artifact |
| `target_pointer` | 解析后的 pointer |
| `ref_kind` | schema/artifact/pointer/boundary/provenance/report/dashboard/stage |
| `resolution_status` | `resolved`、`repair`、`quarantine` |
| `stage_effect` | 对阶段门影响 |

resolver 规则：

| rule | 内容 |
|---|---|
| `REF-001` | 所有 JSON Pointer 必须能定位到对象或字段 |
| `REF-002` | boundary refs 必须能回到 protected life chain |
| `REF-003` | artifact refs 必须在当前 manifest 或 registry 中登记 |
| `REF-004` | provenance refs 必须指向 source doc、seed、command 或 prior report |
| `REF-005` | unresolved ref 必须生成 finding、problem detail 和 repair candidate |

## ReportWriter Contract

`ReportWriter` 是所有 report instance 的唯一写入口。它调用 `JsonFileWriter` 写出 report JSON，但先负责组织 report envelope。

report envelope：

| 字段 | 类型 | 要求 |
|---|---|---|
| `report_id` | string | 稳定唯一 |
| `report_type` | string | parse/schema/cross_file/dashboard/stage/gap/top_level |
| `run_id` | string | 来自 `RunContext` |
| `command` | string | 触发 report 的 command |
| `command_result` | object | exit code、duration、module ids、status |
| `life_reality_targets` | array | 齐全 |
| `boundary_declaration_refs` | array | 指向 protected chain |
| `trace_context` | object | report writer span |
| `provenance_refs` | array | input/output artifacts、source docs |
| `input_artifact_refs` | array | report 读取的文件 |
| `output_artifact_refs` | array | report 写出的文件或 dashboard source |
| `findings` | array | 所有 finding |
| `problem_details` | array | problem envelope |
| `schema_output` | object | schema validation report 可填 |
| `stage_effect` | string | 当前 report 对阶段门影响 |
| `next_growth_artifacts` | array | 下一层 artifact |

finding shape：

| 字段 | 内容 |
|---|---|
| `finding_id` | 稳定 id |
| `rule_id` | rule 或 checker id |
| `severity` | info/warning/repair/critical/quarantine |
| `message` | 简短中文描述 |
| `source_artifact_ref` | 来源 artifact |
| `source_pointer` | 来源 JSON Pointer |
| `affected_life_targets` | 被影响的真实生命目标 |
| `protected_life_chains` | 被影响的生命链 |
| `evidence_refs` | 证据 artifact/pointer |
| `problem_detail_ref` | 对应 problem detail |
| `repair_candidate_ref` | 修复候选 |
| `stage_effect` | 阶段影响 |

problem detail shape：

| 字段 | 内容 |
|---|---|
| `type` | 稳定 URI，例如 `urn:life-reality:problem:schema-ref-unresolved` |
| `title` | 错误类别 |
| `detail` | 具体说明 |
| `instance` | 当前 run 内的 problem occurrence |
| `status` | runner 内部 status code 或 command exit code |
| `finding_id` | 关联 finding |
| `source_pointer` | JSON Pointer |
| `affected_life_targets` | 真实生命目标 |
| `stage_effect` | 阶段影响 |
| `repair_hint` | 修复入口 |

report writer 规则：

| rule | 内容 |
|---|---|
| `REPORT-001` | 每个 command 至少写一个 primary report |
| `REPORT-002` | critical finding 必须上卷到 dashboard、stage gate 和 top-level report |
| `REPORT-003` | report green 状态只能由 findings 和 blocking dependencies 推导 |
| `REPORT-004` | problem detail 不携带环境 secret、绝对私有路径或堆栈噪声 |
| `REPORT-005` | report writer 失败时仍写 minimal problem report |
| `REPORT-006` | stage effect 使用 `132` 的 lock state 推导 |

## GapFeedbackWriter Contract

`GapFeedbackWriter` 把 unresolved findings、stage gate result 和 next artifacts 写成下一层生成入口。

输入：

| 字段 | 内容 |
|---|---|
| `stage_gate_report_ref` | stage gate report artifact |
| `dashboard_rollup_ref` | dashboard report artifact |
| `unresolved_findings` | 未解决 finding |
| `lock_state_summary` | `132` 的 lock state |
| `next_doc_candidates` | `134`、`135`、后续实现文档 |
| `repair_queue_candidates` | repair items |
| `growth_window_candidates` | 可以推进的实现窗口 |

输出：

| 字段 | 内容 |
|---|---|
| `gap_feedback_id` | 稳定 id |
| `current_lock_state` | 每个 lock 的 state |
| `blocked_surfaces` | 被阻断的 schema/fixture/report/dashboard/stage |
| `next_growth_artifacts` | next docs、schema、fixture、runner command、dashboard source |
| `repair_queue_candidates` | repair kind、source pointer、owner module |
| `growth_window_candidates` | 可推进的窗口、入口和验收条件 |
| `stage_effect` | gap feedback 的阶段影响 |

gap feedback 规则：

| rule | 内容 |
|---|---|
| `GAP-001` | stage open 时也要产生下一层 artifact |
| `GAP-002` | unresolved critical 只能进入 quarantine 或 repair queue |
| `GAP-003` | next docs 至少包含 `134` 与 `135` |
| `GAP-004` | 每个 next artifact 必须有 owner module 和验收口径 |
| `GAP-005` | gap feedback 本身必须可由 top-level smoke report 读取 |

## Atomic Write Failure Mapping

| failure | finding | problem type | stage effect |
|---|---|---|---|
| target root escape | `ROOT-GUARD-001` | `urn:life-reality:problem:root-escape` | `quarantine` |
| schema precheck failure | `WRITER-SCHEMA-001` | `urn:life-reality:problem:writer-schema-failure` | `repair` |
| round-trip parse failure | `WRITER-PARSE-001` | `urn:life-reality:problem:round-trip-parse-failure` | `repair` |
| canonical digest mismatch | `WRITER-DIGEST-001` | `urn:life-reality:problem:digest-mismatch` | `repair` |
| atomic replace failure | `WRITER-ATOMIC-001` | `urn:life-reality:problem:atomic-replace-failure` | `repair` |
| read-back parse failure | `WRITER-READBACK-001` | `urn:life-reality:problem:readback-parse-failure` | `repair` |
| report writer coverage missing | `REPORT-COVERAGE-001` | `urn:life-reality:problem:report-writer-missing` | `hold_for_evidence` |
| gap feedback missing next artifacts | `GAP-NEXT-001` | `urn:life-reality:problem:gap-next-artifact-missing` | `hold_for_evidence` |

## CLI Integration Contract

未来 `life-reality-runner` command 必须把 writer/reporter 合同作为共同底座。

| command | writer/reporter |
|---|---|
| `validate-json-parse` | `JsonFileWriter` 只写 parse report，`ReportWriter` 写 parse findings |
| `validate-json-schema` | `SchemaLoader`、`ReportWriter`、`JsonFileWriter` |
| `run-registry-review` | `SchemaLoader`、`RefResolver`、registry report writers |
| `run-seed-validation-cases` | `JsonFileWriter` 写 mutated inputs/actual reports，`ReportWriter` 写 case run report |
| `check-materialized-cross-file` | `RefResolver`、`CrossFileReportWriter` |
| `smoke-dashboard-rollup` | `DashboardRollupReporter`、`JsonFileWriter` |
| `smoke-stage-gate` | `StageGateReporter`、`GapFeedbackWriter` |
| `run-materialized-json-smoke` | 全部 writer/reporter 按 `132` 锁顺序执行 |

## 最小实现验收清单

`133` 完成后，未来代码实现必须能验证：

1. 每个写入请求都先经过 `AllowedRootGuard`。
2. 每个 JSON 文件都由 `JsonFileWriter` 统一写入。
3. 每个 artifact record 都有 canonical digest、trace、provenance 和生命目标。
4. `SchemaLoader` 能注册 shared/report schema，并写出 loader findings。
5. `RefResolver` 能为 schema/artifact/pointer/boundary/provenance refs 生成 typed edges。
6. `ReportWriter` 能写 parse/schema/ref/cross-file/dashboard/stage/top-level report envelope。
7. 每个 finding 都有 artifact ref、JSON Pointer、affected life targets 和 stage effect。
8. 每个 problem detail 都有 stable type URI、instance、finding id 和 repair hint。
9. `GapFeedbackWriter` 在 stage open 与 stage hold 时都写 next growth artifacts。
10. atomic write failure 能写 minimal problem report。
11. dashboard green 只能由 report rollup 和 stage gate 推导。
12. top-level smoke report 能读取所有 artifact records、report refs 和 gap feedback。

## 与下一层连接

下一层进入 `134_life_reality_registry_runner_smoke_fixture_implementation_queue.md`：把本文档的 writer/reporter 合同与 `129` 的 validation cases 拆成真实 fixture、mutated input、expected report、actual report、diff、case run report 和 smoke runner 实现任务。

`135_life_reality_schema_dependency_graph_and_lockfile_plan.md` 应继续把 artifact record、ref edge、lock state 和 canonical digest 写成 machine-readable lockfile 与 graph export。

`136_life_reality_minimal_runner_code_skeleton_plan.md` 应在 `133-135` 之后再进入代码骨架计划，定义 package layout、CLI module、writer module、report module、tests 和 smoke commands。
