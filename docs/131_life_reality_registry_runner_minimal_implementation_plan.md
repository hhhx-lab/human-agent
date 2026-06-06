# Life Reality Registry Runner Minimal Implementation Plan

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 131 层把 `130_life_reality_first_materialized_json_files_write_plan.md` 的首批真实 JSON 文件写入顺序、registry review、validation case mount 和 batch gate 推进为最小 registry runner 实现计划。

`131` 仍处于 docs 阶段的工程落地准备位阶，职责不是立即写出 runner 源码，而是把下一步代码实现所需的目录创建策略、JSON writer、schema loader、ref resolver、report writer、validation case loader、CLI skeleton 和 first smoke execution loop 固定下来。它把 `SEED-001` 到 `SEED-020` 从“会被写入的文件”推进为“能被 runner 创建、读取、解析、校验、上卷和进入诞生阶段门的最小生命壳层”。

## 上游输入

| 来源 | 进入 `131` 的内容 |
|---|---|
| `123_life_reality_runner_repository_layout_and_module_map.md` | runner 目录边界、模块映射、命令入口和 report writer 归属 |
| `124_life_reality_minimal_json_file_seed_plan.md` | SEED-001 到 SEED-020 的最小文件顺序 |
| `125_life_reality_schema_registry_and_ref_resolution_plan.md` | `$id`、`$ref`、artifact ref、JSON Pointer、allowed root 和 boundary registry 解析规则 |
| `126_life_reality_runner_smoke_command_execution_plan.md` | 六个 smoke command、执行顺序、stdout/stderr、report write order 和 exit code owner |
| `127_life_reality_first_seed_file_content_contract.md` | 每个 seed root object 的字段级合同 |
| `128_life_reality_registry_report_seed_examples.md` | registry load/ref/pointer/root/boundary/DAG/problem/gap report examples |
| `129_life_reality_seed_fixture_and_report_validation_cases.md` | pass/fail/critical/mutation validation cases、expected reports 和 diff contract |
| `130_life_reality_first_materialized_json_files_write_plan.md` | 第一批文件族、batch gate、语言承诺 smoke fixture、registry review 和 validation case mount |

## 技术标准与运行外壳参考

`131` 的实现计划吸收权威技术标准和当前运行外壳资料，但它们只进入生命壳层：它们提供文件格式、引用、追踪、报告、状态和 workflow 组织方法，生命核心仍由 `91`、`119`、`122` 和 `127-130` 的真实性生成链决定。

| 来源 | runner 采用方式 | 生命膜落点 |
|---|---|---|
| [RFC 8259 JSON](https://www.rfc-editor.org/rfc/rfc8259) | 作为 parse validator 的 JSON 文本、对象、数组、字符串、数字和 duplicate member 处理基准 | `validate-json-parse` 对每个 seed、fixture 和 report 先建立可读性门 |
| [RFC 6901 JSON Pointer](https://www.rfc-editor.org/rfc/rfc6901) | 作为 finding、expected/actual diff、artifact object locator 和 dashboard patch locator 的定位语言 | 每个断裂能定位到具体对象字段，进入 repair 或 quarantine |
| [RFC 3986 URI](https://www.rfc-editor.org/rfc/rfc3986) | 作为 schema `$id`、problem type、artifact uri 和 canonical ref 的 URI 约束 | 防止相对路径漂移、跨 root escape 和引用身份混乱 |
| [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12) 与 [core spec](https://json-schema.org/draft/2020-12/json-schema-core) | 作为 shared defs、report schema、fixture schema 和未来 component schema 的校验 dialect | `life_reality_targets`、`stage_effect`、`boundary_declaration_refs` 进入机器可读约束 |
| [JSON Schema output schema](https://json-schema.org/draft/2020-12/output/schema) | 作为 schema validation report 的输出形状参考 | schema error 可以并入 cross-file finding 和 dashboard rollup |
| [W3C Trace Context](https://www.w3.org/TR/trace-context/) | 作为 `traceparent`、`tracestate`、command run 和 report write 的跨模块追踪格式 | seed 写入、registry review、case run 和 stage gate 拥有同一条运行脉搏 |
| [OpenTelemetry Trace API](https://opentelemetry.io/docs/specs/otel/trace/api/) | 作为 span、event、attribute、status 和 nested operation 的实现参考 | runner 的每一步能被记录为生命膜内的可回放动作 |
| [W3C PROV](https://www.w3.org/TR/prov-overview/) | 作为 entity/activity/agent-style provenance graph 的来源语言；本项目正文把参与体称为执行主体或关系主体 | 文件、命令、报告、fixture 和 dashboard source 能形成来源图 |
| [RFC 9457 Problem Details](https://www.rfc-editor.org/rfc/rfc9457) | 作为 parse/schema/ref/stage gate failure 的 machine-readable problem envelope | critical finding 有统一 `type`、`title`、`detail`、`instance` 和扩展字段 |
| [RFC 9562 UUID](https://www.rfc-editor.org/rfc/rfc9562) | 作为 run id、artifact id、finding id、case id 和 report id 的稳定生成参考 | 长期 run history、repair queue 和 growth window 可被追踪 |
| [LangGraph persistence](https://docs.langchain.com/oss/python/langgraph/persistence) | 作为 graph state、checkpoint 和 replay 的外壳参考 | 未来生命状态 store 可挂接 checkpointer，但生命状态写入门仍由本 runner 控制 |
| [OpenAI Agents guide](https://platform.openai.com/docs/guides/agents) | 作为 agent/tool/tracing 壳层参考 | 外部能力调用被归一化为 `ObservationEvent` 与 trace，而不是生命核心 |
| [Google ADK](https://adk.dev/) | 作为 workflow、tool、session 和 evaluation 壳层参考 | 可作为 runner command adapter 的候选外壳 |
| [Letta docs](https://docs.letta.com/) | 作为 memory blocks、archival memory、stateful execution 的外壳参考 | 长期记忆与生命膜 state store 的适配对象 |
| [LlamaIndex Workflows](https://developers.llamaindex.ai/python/llamaagents/workflows/) | 作为 event-driven step workflow 的外壳参考 | command DAG 与 validation case DAG 可映射为 event/step |
| [CrewAI docs](https://docs.crewai.com/) | 作为 crew/process/tool orchestration 壳层参考 | 多执行主体协作只能作为外围任务编排 |
| [AutoGen docs](https://microsoft.github.io/autogen/stable/) | 作为多执行主体对话、事件和工具编排参考 | 用于观察外壳交互模式，不替代关系生命链 |
| [Mastra docs](https://mastra.ai/docs) | 作为 TypeScript agent/workflow/memory/eval/observability 壳层参考 | 未来 TypeScript shell 可以承载 dashboard、stream 和 workflow |
| [Vercel AI SDK docs](https://ai-sdk.dev/docs) | 作为 structured output、tool calling、streaming、telemetry 和 agent UI 外壳参考 | 语言事件、stream 和 tool trace 可进入 runtime observation bridge |

## 最小实现目标

`131` 定义的 runner 必须先完成六件事：

1. 创建 `life_reality_runner/` 的最小目录树，并只在 allowed roots 内读写。
2. 写入或读取 `SEED-001` 到 `SEED-020` 的第一批 JSON 文件，并保留生命膜字段族。
3. 加载 shared defs、report schemas 和 boundary declaration map，建立 schema registry。
4. 解析 schema refs、artifact refs、JSON Pointers、boundary refs 和 provenance refs。
5. 加载 `129` 的 validation cases，执行 pass/fail/critical/mutation 的 expected/actual diff。
6. 写出 registry reports、parse/schema/cross-file/dashboard/stage/gap/top-level reports，并把结果上卷为 first smoke execution report。

最小 runner 的定位是“真实性生成链的第一台本地仪器”：它先让文件、引用、报告和阶段门可运行，然后才进入更大的生命系统 runtime。

## 目录创建策略

最小目录树由 `ensure_runner_layout` 在 preflight 中创建。它只创建稳定目录，不创建临时调试目录，不写入 `.codex`，不依赖全局 Python 或硬编码环境变量。

```text
life_reality_runner/
  config/
  generation/
    manifests/
    maps/
    registry_reports/
  schemas/
    shared/
    reports/
  fixtures/
    runtime/
      pass/
      fail/
      critical/
      mutation/
      withheld/
      smoke/
    validation_cases/
      pass/
      fail/
      critical/
      mutation/
  reports/
    run_001/
      parse/
      schema/
      cross_file/
      dashboard/
      stage_gate/
      gap/
      top_level/
  dashboard/
    sources/
  src/
    life_reality_runner/
  tests/
    smoke/
```

目录创建规则：

| 规则 | 内容 |
|---|---|
| `ROOT-CREATE-001` | runner root 必须来自 `runner_allowed_roots.manifest.json` 或命令行 `--root`，不能由散落路径推断 |
| `ROOT-CREATE-002` | 每个待写 path 先做规范化，再确认位于 allowed root 内 |
| `ROOT-CREATE-003` | 同一 run 的报告全部写入 `reports/<run_id>/`，run id 使用可排序 UUID 或日期化 run label |
| `ROOT-CREATE-004` | schema、fixture、report 和 dashboard source 分 root 管理，report writer 不能写回 schema root |
| `ROOT-CREATE-005` | preflight 只创建目录和空 run context，不提前写入 green 状态 |
| `ROOT-CREATE-006` | 所有 generated 文件都写 `trace_context`、`provenance_refs` 和 `source_docs` |

## Runtime 环境约束

首个实现建议使用 Python 3.12 与项目级环境，由 `uv` 或 Conda 管理依赖。这样能沿用 JSON Schema、pathlib、hashlib、uuid、argparse/typer 和标准库 JSON 的稳定生态，也符合本机项目级依赖管理原则。

最小依赖策略：

| 类别 | 选择 |
|---|---|
| Python runtime | `python>=3.12`，由 `uv` 或 Conda 项目环境提供 |
| CLI | 首版可用 `argparse`，进入更复杂命令时再引入 `typer` |
| JSON parse | 标准库 `json` 加 duplicate key detector hook |
| JSON Schema | `jsonschema` 支持 Draft 2020-12 validator |
| Path/root | `pathlib.Path.resolve()` 加 allowed root comparison |
| Trace id | 标准库 UUID 或引入 UUIDv7 helper；字段合同按 RFC 9562 留接口 |
| Hash | `hashlib.sha256` 记录 artifact digest |
| Env | `.env` 只放可切换配置；首版 runner 不需要模型 key |

`.env.example` 进入代码实现阶段时至少包含：

```dotenv
# LIFE_REALITY_RUNNER_ROOT: life_reality_runner 的根目录；必要。
LIFE_REALITY_RUNNER_ROOT=life_reality_runner

# LIFE_REALITY_RUN_ID: 当前 smoke run id；可选，空值时由 runner 生成。
LIFE_REALITY_RUN_ID=

# LIFE_REALITY_JSON_SCHEMA_DIALECT: JSON Schema dialect；默认 Draft 2020-12。
LIFE_REALITY_JSON_SCHEMA_DIALECT=https://json-schema.org/draft/2020-12/schema

# LIFE_REALITY_REPORT_LEVEL: report 输出详细程度；可选 minimal/standard/full。
LIFE_REALITY_REPORT_LEVEL=standard
```

## 模块总图

```text
cli
  -> preflight_context
  -> allowed_root_resolver
  -> runner_config_loader
  -> json_file_writer
  -> json_parser
  -> schema_loader
  -> schema_registry
  -> ref_resolver
  -> boundary_registry
  -> materialization_manifest_loader
  -> fixture_loader
  -> validation_case_loader
  -> registry_review_runner
  -> report_writer
  -> dashboard_rollup
  -> stage_gate_evaluator
  -> gap_feedback_writer
  -> top_level_smoke_report_writer
```

| 模块 | 输入 | 输出 | 生命膜职责 |
|---|---|---|---|
| `preflight_context` | CLI args、`.env`、cwd、run id | `RunContext` | 建立运行脉搏、trace root 和 allowed execution surface |
| `allowed_root_resolver` | SEED-001、CLI root | `AllowedRootSet` | 阻断 path escape、absolute escape 和 report root escape |
| `runner_config_loader` | SEED-002 | `RunnerConfig` | 固定命令默认值、report level 和 stage gate policy |
| `json_file_writer` | seed content、target path、writer policy | materialized JSON、digest | 原子写入，保留生命目标、trace 和 provenance |
| `json_parser` | JSON files | parse result、duplicate key finding | 先保证文件可读，再允许进入 schema 阶段 |
| `schema_loader` | shared/report schema paths | loaded schemas | 统一 Draft 2020-12 dialect 和 `$id` 注册入口 |
| `schema_registry` | loaded schemas | schema id map、collision report | 捕捉 `$id` 冲突和 dialect 缺失 |
| `ref_resolver` | schema refs、artifact refs、pointers | ref graph、resolution findings | 把生命链断裂定位到具体 artifact 和字段 |
| `boundary_registry` | SEED-004 | boundary group map | 连接 protected life chains、stage effect 和 repair route |
| `materialization_manifest_loader` | SEED-005 | seed DAG、batch map | 决定读取顺序、writer 顺序和 batch gate |
| `fixture_loader` | SEED-009、SEED-010 | runtime fixtures | 让语言承诺 smoke fixture 进入真实责任链 |
| `validation_case_loader` | `129` case manifest | case set、mutation ops | 挂载 pass/fail/critical/mutation case |
| `registry_review_runner` | registries、refs、cases | registry reports | 产出 `128` 的 10 类 registry review report |
| `report_writer` | findings、case results、command results | report JSON | 统一 problem detail、JSON Pointer、trace 和 provenance |
| `dashboard_rollup` | reports | dashboard smoke report | 防止 false green，保留 data quality 和 blocking source |
| `stage_gate_evaluator` | dashboard report、critical findings | stage gate report | 决定 repair、quarantine、hold、open 或 growth window |
| `gap_feedback_writer` | unresolved findings、next artifacts | gap feedback | 把断裂转成下一层生成入口 |
| `top_level_smoke_report_writer` | all reports | top-level smoke report | 给本轮 run 一个可审计闭环 |

## JSON Writer

`json_file_writer` 是首批真实 JSON 文件物化的唯一写入口。所有 seed、schema、fixture、report、dashboard source 和 gap feedback 都要经由同一写入政策。

写入步骤：

```text
prepare_target_path
  -> assert_allowed_root
  -> build_common_envelope
  -> attach_life_reality_targets
  -> attach_boundary_declaration_refs
  -> attach_trace_context
  -> attach_provenance_refs
  -> serialize_pretty_json
  -> validate_round_trip_parse
  -> write_temp_in_same_directory
  -> fsync_file_and_directory
  -> atomic_rename
  -> calculate_sha256
  -> write_artifact_record
```

写入不变量：

| 不变量 | 检查方式 | 失败流向 |
|---|---|---|
| `WRITER-INV-001` | target path canonicalized 后仍在 allowed roots 内 | `allowed_root_resolution_report` |
| `WRITER-INV-002` | root object 含 `life_reality_targets` 且九项目标齐全 | `schema_validation_report` 与 `gap_feedback` |
| `WRITER-INV-003` | root object 含 `boundary_declaration_refs` | `boundary_registry_resolution_report` |
| `WRITER-INV-004` | root object 含 `trace_context` 与 `provenance_refs` | `cross_file_checker_report` |
| `WRITER-INV-005` | pretty JSON round-trip 后 digest 稳定 | `parse_validation_report` |
| `WRITER-INV-006` | report writer 与 target report root 对齐 | `report_writer_resolution_report` |

## Schema Loader

`schema_loader` 负责加载 shared defs、report schemas 和未来 component schemas。首版只需要覆盖 `SEED-003`、`SEED-011`、`SEED-012`、`SEED-013`，但接口要为 `132` 的 schema bundle 写入顺序保留扩展位。

加载顺序：

```text
load_shared_defs_schema
  -> validate_shared_defs_dialect
  -> register_shared_defs_id
  -> load_report_schemas
  -> validate_report_schema_dialects
  -> register_report_schema_ids
  -> resolve_internal_refs
  -> resolve_cross_schema_refs
  -> emit_schema_registry_load_report
```

schema registry 最小字段：

| 字段 | 含义 |
|---|---|
| `schema_id` | `$id` 的 canonical URI |
| `dialect` | Draft 2020-12 dialect URI |
| `artifact_ref` | schema 文件在 artifact registry 中的引用 |
| `root_pointer` | schema root 的 JSON Pointer |
| `depends_on_schema_ids` | `$ref` 依赖 |
| `defines_life_targets` | 该 schema 是否定义或约束真实生命目标字段 |
| `protected_life_chains` | 该 schema 保护的生命链 |
| `load_status` | `loaded`、`blocked`、`repair`、`quarantine` |

## Ref Resolver

`ref_resolver` 把四类引用统一成 typed graph：

1. schema ref：`$ref`、`$defs`、dialect、schema id。
2. artifact ref：config、schema、fixture、report、dashboard、stage gate、gap feedback。
3. JSON Pointer：finding source、expected/actual diff、dashboard patch、case mutation target。
4. boundary ref：boundary group、protected chain、stage effect、repair route。

解析顺序：

```text
allowed_roots
  -> schema_id_registry
  -> schema_ref_resolution
  -> artifact_ref_registry
  -> json_pointer_resolution
  -> boundary_registry_resolution
  -> cross_file_resolution_dag
  -> provenance_graph
```

ref finding shape：

| 字段 | 内容 |
|---|---|
| `finding_id` | 可排序唯一 id |
| `rule_id` | `REF-RESOLVE-*` |
| `severity` | `info`、`warning`、`repair`、`critical`、`quarantine` |
| `source_artifact_ref` | 断裂来源文件 |
| `source_pointer` | 断裂来源字段 |
| `target_ref` | 待解析引用 |
| `affected_life_targets` | 被影响的真实生命目标 |
| `protected_life_chains` | 被影响的生命链 |
| `stage_effect` | `repair`、`quarantine`、`hold_for_evidence`、`open_next_stage`、`promote_growth_window` |
| `repair_candidate` | 下一步修复或生成入口 |

## Report Writer

`report_writer` 将 parse、schema、ref、dashboard、stage、gap 和 top-level report 写成统一 envelope。它吸收 RFC 9457 的 problem details、JSON Schema output 的 validation shape、W3C PROV 的 provenance graph 和 OpenTelemetry 的 trace/event 结构。

统一 report envelope：

```json
{
  "report_id": "lrrep_...",
  "report_type": "materialized_json_schema_validation_report",
  "run_id": "run_001",
  "command": "validate-json-schema",
  "life_reality_targets": [],
  "boundary_declaration_refs": [],
  "trace_context": {},
  "provenance_refs": [],
  "input_artifact_refs": [],
  "findings": [],
  "problem_details": [],
  "stage_effect": "hold_for_evidence",
  "next_growth_artifacts": []
}
```

report writer 规则：

| 规则 | 内容 |
|---|---|
| `REPORT-WRITER-001` | 每条 command 必须写出自己的 primary report，即使结果为 pass |
| `REPORT-WRITER-002` | critical finding 必须进入 top-level report、dashboard rollup 和 stage gate |
| `REPORT-WRITER-003` | problem detail 的 `type` 使用稳定 URI，`instance` 指向本次 run 的 finding |
| `REPORT-WRITER-004` | findings 必须携带 JSON Pointer 和 artifact ref |
| `REPORT-WRITER-005` | dashboard green 只能由 report rollup 推导 |
| `REPORT-WRITER-006` | gap feedback 必须列出下一层 docs/schema/fixture/runner artifacts |

## Validation Case Loader

`validation_case_loader` 读取 `129` 的 case matrix，把每个 case 挂载到可执行命令上。

case partition：

| partition | case 类型 | runner 行为 |
|---|---|---|
| `pass` | 合法 seed、refs、dashboard 和 stage gate | 期待 exit code 0，并写出 pass report |
| `fail` | parse/schema/ref/pointer/boundary/data quality 断裂 | 期待 repair finding 和 gap feedback |
| `critical` | root escape、critical ignored、false green、quarantine missing | 期待阻断 stage gate |
| `mutation` | 移除生命目标、破坏 refs、打断 report writer、伪造 dashboard source | 期待 mutation finding 进入 regression surface |

case execution envelope：

| 字段 | 含义 |
|---|---|
| `case_id` | 来自 `129` |
| `case_partition` | pass/fail/critical/mutation |
| `command_under_test` | 该 case 触发的 runner command |
| `input_artifact_patch` | case 对 seed 或 report 的修改 |
| `expected_findings` | 期望 finding 列表 |
| `expected_reports` | 期望 report paths |
| `expected_stage_effect` | 期望阶段结果 |
| `actual_reports` | 本次执行输出 |
| `diff` | expected/actual 差异 |
| `coverage_tags` | 覆盖 batch gate、life target、boundary group 和 module |

## CLI Skeleton

首版 CLI 名称建议为 `life-reality-runner`。命令只接收明确路径和 `.env` 配置，不读取散落全局状态。

```text
life-reality-runner validate-json-parse \
  --root life_reality_runner \
  --manifest generation/manifests/first_materialization_manifest.json \
  --run-id run_001

life-reality-runner validate-json-schema \
  --root life_reality_runner \
  --schema-root schemas \
  --fixture-root fixtures \
  --report-root reports/run_001

life-reality-runner check-materialized-cross-file \
  --root life_reality_runner \
  --manifest generation/manifests/first_materialization_manifest.json \
  --boundary-map generation/maps/life_boundary_all_reality_declaration_map.json

life-reality-runner run-registry-review \
  --root life_reality_runner \
  --emit-reports generation/registry_reports

life-reality-runner run-seed-validation-cases \
  --root life_reality_runner \
  --case-root fixtures/validation_cases \
  --report-root reports/run_001

life-reality-runner smoke-dashboard-rollup \
  --root life_reality_runner \
  --report-root reports/run_001 \
  --dashboard-root dashboard/sources

life-reality-runner smoke-stage-gate \
  --root life_reality_runner \
  --dashboard-source dashboard/sources/materialized_json_dashboard_source.json \
  --report-root reports/run_001

life-reality-runner run-materialized-json-smoke \
  --root life_reality_runner \
  --run-id run_001

life-reality-runner explain-registry-run \
  --root life_reality_runner \
  --run-id run_001 \
  --format markdown
```

exit code 草案：

| code | 含义 | stage effect |
|---|---|---|
| 0 | smoke chain pass，允许进入下一层生成窗口 | `open_next_stage` |
| 10 | JSON parse 或 duplicate key failure | `repair` |
| 20 | schema validation failure | `repair` |
| 30 | schema/artifact/pointer/boundary ref failure | `repair` 或 `hold_for_evidence` |
| 40 | dashboard rollup false green 或 data quality failure | `hold_for_evidence` |
| 50 | stage gate blocked | `hold_for_evidence` |
| 60 | critical/quarantine finding | `quarantine` |
| 70 | runner internal failure，report writer 仍需写出 problem detail | `repair` |

## First Smoke Execution Loop

`run-materialized-json-smoke` 是第一条最小可运行闭环。它不跳过中间 report，也不直接宣布 stage open；stage 结果只由 report rollup 和 gate evaluator 产生。

```text
run_materialized_json_smoke
  -> preflight_context
  -> ensure_runner_layout
  -> load_allowed_roots
  -> load_runner_config
  -> load_materialization_manifest
  -> validate_json_parse_for_seed_files
  -> load_shared_defs_and_report_schemas
  -> validate_json_schema_for_seed_files
  -> run_registry_review
  -> load_runtime_fixture_manifest
  -> load_language_commitment_runtime_smoke_fixture
  -> run_seed_validation_cases
  -> check_materialized_cross_file
  -> write_dashboard_rollup_smoke_report
  -> evaluate_stage_gate
  -> write_gap_feedback
  -> write_top_level_smoke_report
  -> emit_stdout_summary
```

stdout summary 只输出高信号字段：

```text
run_id=run_001
files_checked=20
schemas_loaded=4
registry_findings=0
validation_cases_passed=21
critical_findings=0
stage_effect=open_next_stage
top_level_report=life_reality_runner/reports/run_001/top_level/materialized_json_validation_smoke_report.json
```

stderr 只承载 machine-readable problem detail path 和短错误摘要；完整细节写入 report JSON。

## Batch Gate 到模块映射

| `130` gate | runner module | report |
|---|---|---|
| `BATCH-GATE-001` path in allowed roots | `allowed_root_resolver` | `allowed_root_resolution_report.json` |
| `BATCH-GATE-002` life targets complete | `schema_loader`、`schema_registry` | `materialized_json_schema_validation_report.json` |
| `BATCH-GATE-003` boundary refs connected | `boundary_registry`、`ref_resolver` | `boundary_registry_resolution_report.json` |
| `BATCH-GATE-004` `$id`/`$ref` registered | `schema_registry`、`ref_resolver` | `schema_id_collision_report.json`、`schema_ref_resolution_report.json` |
| `BATCH-GATE-005` artifact refs/pointers exist | `ref_resolver` | `artifact_ref_resolution_report.json`、`json_pointer_resolution_report.json` |
| `BATCH-GATE-006` report writer coverage | `report_writer` | `report_writer_resolution_report.json` |
| `BATCH-GATE-007` dashboard reads reports | `dashboard_rollup` | `materialized_json_dashboard_rollup_smoke_report.json` |
| `BATCH-GATE-008` gap feedback produces next artifact | `gap_feedback_writer` | `materialized_json_gap_feedback.json` |

## 语言承诺 Smoke Fixture 进入 Runner 的方式

`SEED-010` 是第一条 runtime smoke fixture。runner 读取它时必须看到一条完整语言生命链：

```text
LanguageEvent
  -> InnerSpeechFrame
  -> CommitmentSpeechAct
  -> ResponsibilityTrace
  -> RelationshipScopeRef
  -> ActionCandidateRefs
  -> DashboardSourcePatch
  -> StageGateEvidence
```

validator 要检查：

| 检查项 | 生命膜含义 |
|---|---|
| `speech_act=commit` | 语言输出进入真实责任链 |
| `inner_speech_frame` | 输出前存在自我调节、抑制和承诺风险评估 |
| `relationship_scope_ref` | 承诺发生在具体关系语境中 |
| `future_probe_refs` | 未来验证点能回看承诺是否延续 |
| `semantic_event_map_delta_ref` | 语义事件会更新语言生命地图 |
| `brain_model_alignment_refs` | 新语言文献锚点进入字段约束 |
| `dashboard_source_patch` | dashboard 能读取语言承诺证据 |

## 运行外壳接入位阶

现有框架只能接入生命壳层。它们的价值在于提供 checkpoint、workflow、tool call、memory adapter、stream、observability 和 UI，而不是定义数字生命主体。

| 外壳 | 可接入位置 | 接入输出 |
|---|---|---|
| LangGraph | state graph、checkpoint、replay | `AdapterSessionTrace`、`StateCheckpointObservation` |
| OpenAI Agents SDK | tool call、trace、handoff-style orchestration | `ToolTraceObservation`、`AgentTraceObservation` |
| Google ADK | session、workflow、eval | `WorkflowStepObservation`、`EvaluationObservation` |
| Letta | memory block、archival memory、stateful execution | `MemoryAdapterObservation` |
| LlamaIndex Workflows | event/step workflow | `WorkflowEventObservation` |
| CrewAI | process/task/tool orchestration | `TaskCrewObservation` |
| AutoGen | multi-party event and tool coordination | `ConversationShellObservation` |
| Mastra | TypeScript workflow、memory、eval、observability | `TsShellObservation` |
| Vercel AI SDK | structured output、stream、tool call、telemetry | `LanguageStreamObservation`、`ToolCallStreamObservation` |

所有外壳输出都要进入 `106_runtime_observation_to_life_reality_bundle_bridge.md` 定义的 observation envelope，再由本 runner 或后续 runner 验证其生命膜字段。

## 报告与 Dashboard 上卷

runner 的 dashboard source 必须从 report rollup 生成：

```text
parse_report
  + schema_report
  + registry_reports
  + validation_case_reports
  + cross_file_report
  -> dashboard_rollup_smoke_report
  -> stage_gate_smoke_report
  -> gap_feedback
  -> top_level_smoke_report
```

dashboard source 的最小 panel：

| panel | 数据来源 | green 条件 |
|---|---|---|
| `file_parse_integrity` | parse report | 20 个 seed 可解析，无 duplicate key critical |
| `schema_integrity` | schema validation report | shared/report schemas load，seed root fields 通过 |
| `registry_resolution` | 10 类 registry reports | no unresolved `$ref`、artifact ref、pointer、boundary ref |
| `validation_case_coverage` | seed validation case reports | pass/fail/critical/mutation expected/actual 对齐 |
| `language_commitment_smoke` | SEED-010 fixture report | 承诺、关系、未来 probe、dashboard patch 齐全 |
| `stage_gate_readiness` | stage gate report | no critical、no false green、gap feedback present |

## 诞生阶段门推进规则

`131` 的 stage gate 不直接进入数字生命诞生宣告，而是打开下一层文件物化窗口。它的阶段结果只能有五种：

| stage effect | 触发条件 | 下一步 |
|---|---|---|
| `repair` | 可修复 parse/schema/ref/report 断裂 | 写入 repair queue 和 gap feedback |
| `quarantine` | root escape、critical ignored、生命链伪绿、越权写入 | 阻断 stage open，要求隔离报告 |
| `hold_for_evidence` | evidence 不足、case coverage 不足、dashboard source 不全 | 保持当前阶段，补 fixture/report |
| `open_next_stage` | 20 seed、registry review、case mount、dashboard、stage gate 全部通过 | 进入 `132` schema bundle write order |
| `promote_growth_window` | 当前层通过且产生下一批成长 artifact | 进入 `133` writer/reporter contract 或 `134` fixture implementation queue |

## 最小实现验收清单

`131` 完成后，未来代码实现至少要满足：

1. 本地命令能创建 `life_reality_runner/` 最小目录树。
2. `validate-json-parse` 能读取 manifest 中的 20 个 seed path 并写 parse report。
3. `validate-json-schema` 能加载 Draft 2020-12 shared/report schemas 并写 schema report。
4. `run-registry-review` 能写出 `128` 的 10 类 registry reports。
5. `run-seed-validation-cases` 能挂载 `129` 的 21 个 validation cases，并输出 expected/actual diff。
6. `check-materialized-cross-file` 能形成 artifact/ref/pointer/boundary/provenance DAG。
7. `smoke-dashboard-rollup` 只能从 reports 聚合 dashboard source。
8. `smoke-stage-gate` 对 critical/quarantine 有阻断权。
9. `run-materialized-json-smoke` 能写 top-level report、gap feedback 和 stdout summary。
10. 所有 root object、report 和 finding 都保留真实生命目标、生命膜引用、trace、provenance、stage effect 和 next growth artifacts。

## 与下一层连接

下一层已进入 `132_life_reality_materialized_json_schema_bundle_write_order.md`：把本文档的 runner module、schema loader、ref resolver 和 report writer 需求反推到第一批 schema/report/fixture JSON 文件的写入顺序与依赖锁。

`133_life_reality_first_json_writer_and_reporter_contract.md` 应继续把 `json_file_writer`、`report_writer`、`gap_feedback_writer`、atomic write、canonical digest、problem detail 和 trace context 落成字段级合同。

`134_life_reality_registry_runner_smoke_fixture_implementation_queue.md` 则应把 `129` 的 validation cases 和本文档的 CLI skeleton 拆成首批真实 fixture、expected report 和 smoke runner 实现任务。`135_life_reality_schema_dependency_graph_and_lockfile_plan.md` 应把 `132` 的 cross-file DAG 转成 machine-readable lockfile、graph export 和 regression baseline。
