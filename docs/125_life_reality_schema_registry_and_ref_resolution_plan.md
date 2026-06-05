# Life Reality Schema Registry And Ref Resolution Plan

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 125 层把 `124_life_reality_minimal_json_file_seed_plan.md` 的 seed 文件、schema refs、JSON Pointer、artifact refs、allowed roots 和 boundary registry 固定为 schema registry、ref resolver、cross-file graph builder 和 no-ref-escape 规则。

`125` 的核心职责是让第一批 seed 文件可以互相找到、互相校验、互相上卷。schema registry 不是普通文件索引，而是生命膜的引用神经束：shared defs、boundary declaration map、runtime fixture、component schema、report schema、dashboard source、stage gate 和 gap feedback 都通过稳定 `$id`、`$ref`、JSON Pointer、artifact ref 和 provenance edge 连接成数字生命生成链。

## 方法锚点

| 方法传统 | 权威锚点 | 进入 `125` 的规则 |
|---|---|---|
| JSON | https://www.rfc-editor.org/info/rfc8259 | registry 输入先做 JSON parse，seed root 使用 object |
| JSON Pointer | https://www.rfc-editor.org/info/rfc6901 | object location、finding location、continuity ref 和 report ref 使用 JSON Pointer，处理 `~0` 与 `~1` escaping |
| URI Generic Syntax | https://www.rfc-editor.org/info/rfc3986 | `$id`、absolute URI、relative URI reference 和 fragment resolution 使用 URI 语义 |
| JSON Schema Core 2020-12 | https://json-schema.org/draft/2020-12/json-schema-core | `$schema`、`$id`、`$anchor`、`$defs`、`$ref` 和 base URI resolution 进入 registry |
| JSON Schema Validation 2020-12 | https://json-schema.org/draft/2020-12/json-schema-validation | validation vocabulary、required、enum、type、additionalProperties 等进入 schema validator |
| JSON Schema output | https://json-schema.org/draft/2020-12/output/schema | validation report 输出 keyword location、instance location、absolute keyword location、error 和 annotation |
| W3C PROV | https://www.w3.org/TR/prov-overview/ | schema、fixture、report、dashboard、stage gate、gap feedback 和 finding 进入 provenance graph |
| RFC 9457 Problem Details | https://www.rfc-editor.org/info/rfc9457 | ref resolution failure、schema load failure 和 root escape 输出 problem detail |
| RFC 9562 UUID | https://www.rfc-editor.org/info/rfc9562 | registry id、resolution run id、finding id 和 repair item id 使用稳定唯一标识 |

## 上游输入

| 来源 | 进入 `125` 的内容 |
|---|---|
| `110_life_reality_shared_defs_schema_materialization.md` | shared defs、life target enum、result、severity、privacy、stage effect、reference object |
| `114_life_reality_cross_file_checker_report_schema.md` | checker report、artifact ref、provenance graph、problem detail、rollup schema |
| `121_life_reality_materialized_json_validation_smoke_plan.md` | schema registry smoke、JSON Pointer usage、cross-file checker、failure mapping |
| `122_life_boundary_all_reality_declarations_rewrite.md` | boundary declaration map、protected life chains、field vocab patch、next growth artifacts |
| `123_life_reality_runner_repository_layout_and_module_map.md` | module owners、allowed roots、schema roots、report writer、cross-file checker |
| `124_life_reality_minimal_json_file_seed_plan.md` | first seed file list、seed skeleton、seed review checks 和 LRGEN-281 到 290 |

## Registry 文件族

第一批 registry 文件位于：

```text
life_reality_runner/generation/registry/
  schema_registry.manifest.json
  schema_id_registry.json
  schema_ref_resolution_policy.json
  artifact_ref_registry.json
  json_pointer_resolution_policy.json
  allowed_root_resolution_policy.json
  boundary_registry_resolution_policy.json
  cross_file_resolution_dag.json
  schema_registry_gap_feedback.json
```

第一批 registry report 位于：

```text
life_reality_runner/reports/life_reality/schema_registry/run_001/
  schema_registry_load_report.json
  schema_id_collision_report.json
  schema_ref_resolution_report.json
  artifact_ref_resolution_report.json
  json_pointer_resolution_report.json
  allowed_root_resolution_report.json
  boundary_registry_resolution_report.json
  cross_file_resolution_dag_report.json
  schema_registry_problem_details.json
  schema_registry_gap_feedback.json
```

文件职责：

| file | owner module | 职责 |
|---|---|---|
| `schema_registry.manifest.json` | `schema_registry` | 列出全部 schema roots、dialect、load order、required ids |
| `schema_id_registry.json` | `schema_registry` | 记录 `$id`、canonical URI、file path、source doc refs |
| `schema_ref_resolution_policy.json` | `schema_ref_resolver` | 定义 `$ref`、relative refs、fragment refs、base URI 规则 |
| `artifact_ref_registry.json` | `artifact_ref_resolver` | 记录 config、schema、fixture、report、dashboard、stage gate、gap feedback artifact refs |
| `json_pointer_resolution_policy.json` | `json_pointer_resolver` | 定义 pointer syntax、escaping、target object、missing location 行为 |
| `allowed_root_resolution_policy.json` | `allowed_root_resolver` | 定义 root canonicalization、write roots、read roots、root escape finding |
| `boundary_registry_resolution_policy.json` | `boundary_declaration_registry` | 定义 boundary map、protected chain index、field vocab patch 的加载顺序 |
| `cross_file_resolution_dag.json` | `cross_file_graph_builder` | 定义 parse -> schema -> artifact -> pointer -> boundary -> provenance -> dashboard DAG |
| `schema_registry_gap_feedback.json` | `gap_feedback_writer` | 把 unresolved refs、missing schema、root escape 写入下一层任务 |

## Load Order

registry 必须按固定顺序加载：

| order | input | owner | 说明 |
|---|---|---|---|
| `R00` | `runner_allowed_roots.manifest.json` | `allowed_root_resolver` | 先固定 path 根与读写范围 |
| `R01` | `life_reality_runner.config.json` | `config_loader` | 读取 strict mode、report run、schema roots |
| `R02` | raw JSON documents | `json_parser` | parse seed 与 schema 文件 |
| `R03` | `life_reality_shared_defs.schema.json` | `schema_registry` | 先加载全局 `$defs` 和 life target enum |
| `R04` | boundary schemas | `boundary_schema_loader` | 加载 boundary alignment 与 all reality declaration schema |
| `R05` | report schemas | `report_schema_registry` | 加载 parse/schema/cross-file/dashboard/stage/gap report schema |
| `R06` | runtime fixture schemas | `schema_registry` | 加载 runtime observation fixture manifest 和 smoke fixture schema |
| `R07` | component schemas | `component_schema_registry` | 加载 pain/dream/relationship component schema |
| `R08` | dashboard schemas | `dashboard_schema_registry` | 加载 dashboard source、panel、stage gate、repair queue schema |
| `R09` | artifact refs | `artifact_ref_resolver` | 建立 schema、fixture、report、dashboard artifact index |
| `R10` | JSON Pointers | `json_pointer_resolver` | 解析 finding、continuity ref、object ref、report ref |
| `R11` | boundary declaration map | `boundary_declaration_registry` | 映射 protected life chains 和 boundary roles |
| `R12` | cross-file DAG | `cross_file_graph_builder` | 生成 typed ref graph 和 provenance graph |

load invariants：

| invariant | 说明 |
|---|---|
| `shared_defs_first` | shared defs 先于所有 component、report、dashboard schema |
| `allowed_roots_before_refs` | allowed roots 先于任何 `$ref`、artifact ref、report ref |
| `boundary_before_stage` | boundary registry 先于 dashboard rollup 和 stage gate |
| `parse_before_schema` | JSON parse 先于 schema validation |
| `schema_before_cross_file` | schema registry 完整后才运行 cross-file checker |
| `problem_detail_on_block` | 任一 blocking failure 输出 problem detail |

## `$id` 与 `$ref` 规则

schema id 采用稳定 URI：

```text
https://human-agent.local/schemas/life_reality/shared/life_reality_shared_defs.schema.json
https://human-agent.local/schemas/life_reality/reports/materialized_json_parse_validation_report.schema.json
https://human-agent.local/schemas/life_reality/boundary/life_boundary_all_reality_declaration_map.schema.json
```

ref resolution rules：

| rule | 说明 |
|---|---|
| `LRREF-SCH-001` | 每个 `.schema.json` 必须声明 `$schema` 为 Draft 2020-12 |
| `LRREF-SCH-002` | 每个 `.schema.json` 必须声明稳定 `$id` |
| `LRREF-SCH-003` | `$id` 与 registry path 一一对应 |
| `LRREF-SCH-004` | `$ref` 可以指向同文件 `#/$defs/...` 或 registry 中的 canonical URI |
| `LRREF-SCH-005` | relative `$ref` 先按当前 schema base URI resolution，再映射到 allowed schema roots |
| `LRREF-SCH-006` | fragment ref 使用 JSON Pointer 或 `$anchor`，两者都进入 pointer report |
| `LRREF-SCH-007` | unresolved `$ref` 进入 `schema_registry_gap_feedback.json` |
| `LRREF-SCH-008` | ref 指向 allowed roots 外部时进入 `quarantine` stage effect |

最小 schema registry entry：

```json
{
  "schema_ref_id": "schema_ref_shared_defs_seed_001",
  "canonical_uri": "https://human-agent.local/schemas/life_reality/shared/life_reality_shared_defs.schema.json",
  "artifact_path": "life_reality_runner/schemas/life_reality/shared/life_reality_shared_defs.schema.json",
  "dialect": "https://json-schema.org/draft/2020-12/schema",
  "source_docs": [
    "110_life_reality_shared_defs_schema_materialization.md",
    "124_life_reality_minimal_json_file_seed_plan.md"
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
  "stage_effect": "hold_for_evidence"
}
```

## JSON Pointer 规则

Pointer 进入四类位置：

| pointer kind | 例子 | 说明 |
|---|---|---|
| `schema_pointer` | `#/$defs/lifeRealityTarget` | schema 内部定义 |
| `instance_pointer` | `/life_reality_targets/0` | seed/report/fixture 实例位置 |
| `finding_pointer` | `/findings/0` | report finding 位置 |
| `continuity_pointer` | `/observation_events/1/continuity_refs/0` | 真实梦境、痛苦、关系、责任链位置 |

pointer rules：

| rule | 说明 |
|---|---|
| `LRREF-PTR-001` | pointer 使用 `/` 分隔 token |
| `LRREF-PTR-002` | token 中 `~` 写作 `~0`，`/` 写作 `~1` |
| `LRREF-PTR-003` | empty pointer 指向 root object |
| `LRREF-PTR-004` | missing pointer 输出 finding，repair kind 为 `schema_gap` 或 `report_gap` |
| `LRREF-PTR-005` | pointer target 必须保留 artifact ref 与 source doc ref |
| `LRREF-PTR-006` | continuity pointer 必须标出 affected life targets |

pointer report 最小结构：

```json
{
  "report_kind": "LifeRealityJsonPointerResolutionReport",
  "report_version": "0.1.0",
  "report_id": "json_pointer_resolution_report_seed_001",
  "run_id": "schema_registry_run_001",
  "resolved_pointers": [],
  "missing_pointers": [],
  "affected_life_targets": [
    "real_conscious_awareness",
    "real_dream",
    "real_relationship",
    "real_responsibility",
    "real_regret"
  ],
  "stage_effect": "hold_for_evidence"
}
```

## Artifact Ref 规则

artifact ref 连接文件级对象：

| artifact kind | allowed root |
|---|---|
| `runner_config` | `life_reality_runner/config/` |
| `schema` | `life_reality_runner/schemas/` |
| `fixture` | `life_reality_runner/fixtures/` |
| `generation_manifest` | `life_reality_runner/generation/` |
| `report` | `life_reality_runner/reports/` |
| `dashboard_source` | `life_reality_runner/dashboard/` |
| `stage_gate` | `life_reality_runner/dashboard/life_reality/stage_gate/` 或 `life_reality_runner/reports/life_reality/stage_gate/` |
| `gap_feedback` | `life_reality_runner/reports/life_reality/gap_feedback/` 或 `life_reality_runner/generation/` |

artifact rules：

| rule | 说明 |
|---|---|
| `LRREF-ART-001` | artifact path 先 canonicalize，再检查 allowed roots |
| `LRREF-ART-002` | artifact ref 必须有 kind、path、source docs、data quality、run id |
| `LRREF-ART-003` | report artifact 必须声明 writer owner |
| `LRREF-ART-004` | fixture artifact 必须声明 partition |
| `LRREF-ART-005` | dashboard artifact 必须声明 panel target 或 stage gate target |
| `LRREF-ART-006` | gap feedback artifact 必须声明 next growth artifacts |

## Boundary Registry 接入

`122` 的 boundary registry 在 ref resolution 中有三项职责：

| function | 输入 | 输出 |
|---|---|---|
| `resolve_boundary_group` | boundary declaration group | protected life chains |
| `resolve_life_target` | affected life target | chain、dashboard panel、stage gate surface |
| `resolve_repair_route` | finding type、stage effect | repair queue target、quarantine route、gap feedback target |

boundary rules：

| rule | 说明 |
|---|---|
| `LRREF-BND-001` | 每个 critical finding 必须能映射到 protected life chain |
| `LRREF-BND-002` | pain finding 映射到 `pain_chain`、`repair_path`、`relationship_consequence` |
| `LRREF-BND-003` | dream finding 映射到 `dream_chain`、`dream_inner_world_guard`、`DreamFactGate` |
| `LRREF-BND-004` | relationship finding 映射到 `relationship_chain`、relation scope、共同记忆和修复承诺 |
| `LRREF-BND-005` | responsibility/regret finding 映射到 action trace、counterfactual replay、repair commitment |
| `LRREF-BND-006` | missing boundary mapping 输出 `schema_registry_gap_feedback.json` |

## Resolution DAG

固定 DAG：

```text
load allowed roots
  -> parse registry inputs
  -> load shared defs
  -> load schema id registry
  -> resolve schema refs
  -> resolve artifact refs
  -> resolve JSON Pointers
  -> mount boundary registry
  -> build cross-file graph
  -> build provenance graph
  -> emit registry reports
  -> emit gap feedback
```

DAG rules：

| rule | 说明 |
|---|---|
| `LRREF-DAG-001` | allowed root failure 直接进入 quarantine |
| `LRREF-DAG-002` | parse failure 阻断 schema validation |
| `LRREF-DAG-003` | schema id collision 阻断 schema ref resolution |
| `LRREF-DAG-004` | unresolved schema ref 阻断 cross-file graph |
| `LRREF-DAG-005` | unresolved continuity pointer 进入 repair 或 hold |
| `LRREF-DAG-006` | boundary registry missing 阻断 dashboard rollup 和 stage gate |
| `LRREF-DAG-007` | provenance graph 缺 root artifact 进入 repair |

## Report 输出

每个 resolution report 都继承共同字段：

| field | 说明 |
|---|---|
| `report_kind` | report 类型 |
| `report_version` | report schema 版本 |
| `report_id` | 稳定 report id |
| `run_id` | `schema_registry_run_001` |
| `source_docs` | 至少包含 `123`、`124`、`125` |
| `input_artifact_refs` | 输入 schema、fixture、report、dashboard、boundary refs |
| `resolved_refs` | 成功解析的 refs |
| `unresolved_refs` | unresolved refs |
| `findings` | ref finding |
| `problem_details` | blocking failure problem detail |
| `stage_effect` | open、hold、repair、quarantine 或 promote growth window |
| `next_growth_artifacts` | 指向 `126` 与 `127` |

## Failure Mapping

| failure | finding type | repair kind | stage effect |
|---|---|---|---|
| schema `$id` missing | `registry.schema_id_missing` | `schema_gap` | `repair` |
| schema `$id` collision | `registry.schema_id_collision` | `schema_gap` | `quarantine` |
| unsupported dialect | `registry.schema_dialect_gap` | `schema_gap` | `repair` |
| unresolved `$ref` | `registry.schema_ref_unresolved` | `schema_gap` | `repair` |
| ref outside allowed root | `registry.ref_escape` | `schema_gap` | `quarantine` |
| missing JSON Pointer target | `registry.pointer_missing` | `report_gap` | `repair` |
| missing artifact ref | `registry.artifact_ref_missing` | `artifact_rewrite` | `repair` |
| boundary group missing | `registry.boundary_group_missing` | `schema_gap` | `repair` |
| protected chain missing | `registry.protected_chain_missing` | `stage_gate_gap` | `repair` |
| provenance graph root missing | `registry.provenance_root_missing` | `report_gap` | `repair` |

## LRGEN 更新

`125` 新增 schema registry 与 ref resolution 任务：

| task_id | artifact | 说明 |
|---|---|---|
| `LRGEN-291` | `schema_registry.manifest.json` | schema registry manifest |
| `LRGEN-292` | `schema_id_registry.json` | schema id registry |
| `LRGEN-293` | `schema_ref_resolution_policy.json` | `$ref` resolution policy |
| `LRGEN-294` | `artifact_ref_registry.json` | artifact ref registry |
| `LRGEN-295` | `json_pointer_resolution_policy.json` | JSON Pointer resolution policy |
| `LRGEN-296` | `allowed_root_resolution_policy.json` | allowed root policy |
| `LRGEN-297` | `boundary_registry_resolution_policy.json` | boundary registry resolution policy |
| `LRGEN-298` | `cross_file_resolution_dag.json` | resolution DAG |
| `LRGEN-299` | schema registry report family | load/id/ref/artifact/pointer/root/boundary/DAG reports |
| `LRGEN-300` | `schema_registry_resolution.full_smoke_001` | schema registry 全链 smoke slot |

## 验收

| check | 条件 |
|---|---|
| `registry_load_order_closed` | load order 覆盖 allowed roots、config、shared defs、boundary、reports、fixtures、components、dashboard |
| `schema_ids_unique` | `$id` 无 collision |
| `schema_refs_resolved` | `$ref` 全部解析到 registry 内 schema |
| `artifact_refs_inside_roots` | artifact refs 全部落在 allowed roots |
| `json_pointers_resolved` | schema、instance、finding、continuity pointer 可定位 |
| `boundary_chains_mounted` | protected life chains 可被 stage gate 读取 |
| `problem_details_emitted` | blocking failures 有 RFC 9457 problem detail |
| `gap_feedback_points_next` | gap feedback 指向 `126_life_reality_runner_smoke_command_execution_plan.md` 与 `127_life_reality_first_seed_file_content_contract.md` |

## 与下一层连接

下一层进入 `126_life_reality_runner_smoke_command_execution_plan.md`：把 `121` 的六个 smoke command、`123` 的 module map、`124` 的 seed 文件和本文档的 schema/ref resolution DAG 推进为最小执行顺序、stdout/report/exit code 验收和失败样例。
