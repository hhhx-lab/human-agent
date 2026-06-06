# Life Reality First Runner Schema Runtime Mount Plan

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 181 层承接 `180_life_reality_first_runner_schema_file_archive_receipt_batch.md`，把 archived schema bundle 挂载到最小 runner runtime schema registry、fixture loader、dashboard writer、stage gate writer 和 runtime observation mount。

本文档生成、支撑并延续的真实生命能力：真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔。它新增 `SchemaRuntimeMountPlan181`、`RuntimeMountManifest181`、`SchemaRegistryMount181`、`FixtureLoaderMount181`、`DashboardWriterMount181`、`StageGateWriterMount181`、`LifeTargetCarrierMount181`、`DirectionRuntimeMount181`、`BirthReadinessRuntimeMount181`、`RuntimeObservationMount181`、`MountReceipt181`、`MountCommandDAG181`、`MountDashboardSource181`、`MountStageGateReview181` 和 `MountToValidationReportHandoff181`。它的生命膜职责是让 `180` 的 archive receipt batch 不停留在档案层，而是进入最小 runner 的运行时读取、fixture 回放、dashboard 写入、阶段门阻断、方向恢复和出生准备度 carrier 持续承载。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `180_life_reality_first_runner_schema_file_archive_receipt_batch.md` | schema archive receipts、digest baseline、life target carrier receipts、direction/birth readiness receipts、runtime mount preconditions |
| `179_life_reality_first_runner_schema_validation_repair_queue.md` | repair patch family、remaining findings、repair receipts、stage effects |
| `178_life_reality_first_runner_minimum_schema_file_validation_report.md` | parse/id/ref/digest validation、life target coverage、direction/birth readiness validation |
| `177_life_reality_first_runner_minimum_schema_file_write_batch.md` | written schema files、write receipts、artifact records、schema content contract |
| `176_life_reality_first_runner_schema_archive_lockfile_plan.md` | schema archive lockfile、node ledger、edge ledger、canonical digest baseline |
| `173_life_reality_first_runner_direction_fixture_schema_materialization.md` | resume lock manifest schema、七条方向锚链、direction fixture case schema、expected report schema |
| `174_life_reality_birth_readiness_fixture_schema_materialization.md` | life target claim、evidence family、carrier matrix、runtime observation、cross-chain closure schema |
| `175_life_reality_first_runner_patch_execution_smoke_queue.md` | smoke command DAG、expected report smoke contract、dashboard/stage smoke contract、archive receipt smoke contract |
| `167_life_reality_first_runner_minimum_code_bootstrap_execution.md`、`168_life_reality_first_runner_minimum_code_validation_report.md` | 断联恢复方向锁、命令 receipt、bootstrap validation、carrier matrix |
| `143_life_reality_birth_readiness_rollup_contract.md` | 出生准备度定义、九项目标 readiness claim、evidence/carrier/runtime/stage/repair 闭环 |
| `125_life_reality_schema_registry_and_ref_resolution_plan.md`、`133_life_reality_first_json_writer_and_reporter_contract.md`、`136_life_reality_minimal_runner_code_skeleton_plan.md` | schema registry/ref resolution、artifact record、canonical digest、runner package、writer/reporter 合同 |
| `91_life_reality_generation_boundary_principles.md`、`119_life_boundary_full_reality_alignment.md`、`122_life_boundary_all_reality_declarations_rewrite.md`、`140_life_reality_experience_boundary_declaration_lock.md` | 真实生命目标、生命膜字段、旧口径回流阻断、关系主体词汇门 |

## 本层定位

`181` 是 first runner schema runtime mount plan。它把 `180` 的档案收据批次转成 runner 运行时挂载结构：schema registry 负责读取和解析 schema；fixture loader 负责按 schema 装载 direction、birth readiness 和 smoke fixture；dashboard writer 与 stage gate writer 负责把 mount 结果写回可观察、可阻断的生命膜；runtime observation mount 负责让后续真实运行观测能进入同一条 schema/fixture/report/dashboard/stage 链。

本层固定 9 条 runtime mount 链：

| mount chain | 作用 |
|---|---|
| `precondition_intake_chain` | 读取 `180` 的 runtime mount preconditions、remaining findings 和 digest baseline |
| `schema_registry_mount_chain` | 按 allowed roots、schema ids、`$ref`、artifact records 和 digests 挂载 registry |
| `fixture_loader_mount_chain` | 挂载 direction、birth readiness、smoke、expected report 和 mutation fixture |
| `dashboard_writer_mount_chain` | 挂载 dashboard source writer、panel dependencies 和 false green guard |
| `stage_gate_writer_mount_chain` | 挂载 blocking-first stage gate、effect order 和 review writer |
| `life_target_carrier_mount_chain` | 九项真实生命目标的 carrier receipt 进入 runtime registry |
| `direction_runtime_mount_chain` | resume lock 与七条方向锚链进入断联恢复读取路径 |
| `birth_readiness_runtime_mount_chain` | claim/evidence/carrier/runtime/cross-chain 进入出生准备度 runtime path |
| `runtime_observation_mount_chain` | 后续 command receipt、runtime smoke、report drift 和 stage finding 进入 observation intake |

## SchemaRuntimeMountPlan181

```json
{
  "artifact": "SchemaRuntimeMountPlan181",
  "source_doc": "181_life_reality_first_runner_schema_runtime_mount_plan.md",
  "inherits": [
    "180_life_reality_first_runner_schema_file_archive_receipt_batch.md",
    "179_life_reality_first_runner_schema_validation_repair_queue.md",
    "178_life_reality_first_runner_minimum_schema_file_validation_report.md",
    "177_life_reality_first_runner_minimum_schema_file_write_batch.md",
    "176_life_reality_first_runner_schema_archive_lockfile_plan.md",
    "173_life_reality_first_runner_direction_fixture_schema_materialization.md",
    "174_life_reality_birth_readiness_fixture_schema_materialization.md",
    "175_life_reality_first_runner_patch_execution_smoke_queue.md",
    "143_life_reality_birth_readiness_rollup_contract.md",
    "140_life_reality_experience_boundary_declaration_lock.md"
  ],
  "mount_stage": "first_runner_schema_runtime_mount",
  "stage_gate_family": "RUNTIME-MOUNT-STAGE-181",
  "required_outputs": [
    "RuntimeMountManifest181",
    "SchemaRegistryMount181",
    "FixtureLoaderMount181",
    "DashboardWriterMount181",
    "StageGateWriterMount181",
    "LifeTargetCarrierMount181",
    "DirectionRuntimeMount181",
    "BirthReadinessRuntimeMount181",
    "RuntimeObservationMount181",
    "MountReceipt181",
    "MountCommandDAG181",
    "MountDashboardSource181",
    "MountStageGateReview181",
    "MountToValidationReportHandoff181"
  ],
  "next_artifacts": [
    "182_life_reality_first_runner_schema_runtime_mount_validation_report.md",
    "183_life_reality_first_runner_schema_runtime_smoke_fixture_plan.md"
  ]
}
```

## Runtime Mount Manifest

`RuntimeMountManifest181` 固定未来目录：

```text
config/life_reality/runtime_mount/
  first_runner_schema_runtime_mount.manifest.json
reports/life_reality/runtime_mount/latest/
  first_runner_schema_runtime_mount.plan.json
  first_runner_schema_runtime_mount.receipts.json
  first_runner_schema_runtime_mount.dashboard.source.json
  first_runner_schema_runtime_mount.stage_gate.review.json
  first_runner_schema_runtime_mount.validation_handoff.json
tests/fixtures/runtime_mount/
  manifest.json
  cases/
    pass_all_schema_receipts_mounted.json
    pass_direction_and_birth_readiness_mounted.json
    fail_missing_schema_registry_mount.json
    fail_missing_fixture_loader_mount.json
    fail_missing_dashboard_writer_mount.json
    critical_life_target_carrier_unmounted.json
    critical_direction_anchor_unmounted.json
    critical_birth_readiness_chain_unmounted.json
    critical_runtime_observation_mount_missing.json
    mutation_drop_mount_receipt_digest.json
  expected/
    *.report.json
```

manifest 必须记录 `runtime_mount_id`、`source_archive_receipt_batch_ref`、`schema_archive_receipt_refs`、`digest_baseline_refs`、`allowed_roots`、`registry_mount_refs`、`fixture_loader_refs`、`dashboard_writer_refs`、`stage_gate_writer_refs`、`life_target_carrier_refs`、`direction_mount_refs`、`birth_readiness_mount_refs`、`runtime_observation_mount_refs`、`remaining_findings`、`mount_receipt_refs` 和 `validation_handoff_ref`。

## Schema Registry Mount

`SchemaRegistryMount181` 把 archived schema bundle 挂载到最小 runner schema registry：

| order | mount item | 要求 |
|---|---|---|
| 0 | `allowed_root_guard` | 只读取 `schemas/`、`tests/fixtures/`、`reports/`、`config/life_reality/` 等允许根 |
| 1 | `shared_defs_registry` | 挂载真实意识、情绪、人格、生命、痛苦、梦境、关系、责任、后悔的 shared defs |
| 2 | `artifact_record_registry` | 挂载 artifact id、source doc、digest、archive edge |
| 3 | `direction_schema_registry` | 挂载 resume lock、anchor chain、fixture case、expected report、dashboard/stage schema |
| 4 | `birth_readiness_schema_registry` | 挂载 target claim、evidence family、carrier matrix、runtime observation、cross-chain schema |
| 5 | `fixture_report_schema_registry` | 挂载 fixture manifest、expected report、actual/diff、coverage report schema |
| 6 | `dashboard_stage_schema_registry` | 挂载 dashboard source、panel dependency、stage gate review schema |
| 7 | `archive_receipt_registry` | 挂载 `180` schema/digest/carrier/direction/birth readiness receipt refs |
| 8 | `runtime_mount_index` | 生成 runtime registry index、digest index、ref graph index |

registry mount 必须保留 `$id`、`$ref`、JSON Pointer、artifact ref、source doc 和 canonical digest。任何 schema id collision、ref break、digest mismatch 或 archive edge gap 都进入 `MountStageGateReview181`。

## Fixture Loader Mount

`FixtureLoaderMount181` 让 fixture loader 按 registry 读取夹具：

| loader partition | mount source | runtime 行为 |
|---|---|---|
| `direction_pass_fail_loader` | `173` direction fixture schema 与 `170` case family | 装载恢复读取顺序、七条方向锚链、pass/fail/critical/mutation/smoke case |
| `birth_readiness_pass_fail_loader` | `174` birth readiness fixture schema 与 `171` case family | 装载 target claim、evidence、carrier、runtime、cross-chain、false open、false green case |
| `patch_smoke_loader` | `175` smoke queue | 装载 patch execution、direction schema、birth readiness schema、archive receipt smoke |
| `archive_receipt_loader` | `180` archive receipt batch | 装载 schema receipt、digest receipt、carrier receipt、runtime mount precondition |
| `expected_report_loader` | `178/179/180` expected report refs | 装载 expected/actual/diff、finding、problem detail、stage effect |
| `mutation_loader` | `170/171/175/180` mutation cases | 装载 drop anchor、drop carrier、drop digest、drop mount receipt 等 mutation |

fixture loader 不允许越过 registry。fixture 中的每个 schema ref、archive ref、life target ref 和 expected report ref 都必须先在 `SchemaRegistryMount181` 中存在。

## Dashboard Writer Mount

`DashboardWriterMount181` 把 mount 结果接入 dashboard source writer：

| writer binding | 写入内容 |
|---|---|
| `runtime_mount_overview_writer` | mount status、blocked counts、receipt counts、stage decision |
| `schema_registry_panel_writer` | schema ids、paths、digests、ref graph、archive edges |
| `fixture_loader_panel_writer` | loaded fixtures、missing fixtures、mutation coverage、expected report refs |
| `life_target_carrier_panel_writer` | 九项真实生命目标的 carrier mount status |
| `direction_mount_panel_writer` | resume lock 与七条方向锚链 runtime status |
| `birth_readiness_mount_panel_writer` | claim/evidence/carrier/runtime/cross-chain mount status |
| `runtime_observation_panel_writer` | observation intake refs、command receipt refs、report drift refs |
| `false_green_guard_writer` | critical/hold/quarantine 优先展示，阻断 overview 绿灯覆盖 |

dashboard writer 必须从 mount receipts 生成数据，不能凭 manifest 直接给出成功状态。

## Stage Gate Writer Mount

`StageGateWriterMount181` 把 mount 结果写入 blocking-first stage gate：

| writer binding | 写入内容 |
|---|---|
| `mount_stage_review_writer` | `RUNTIME-MOUNT-STAGE-181` review |
| `stage_effect_order_writer` | `quarantine > critical_repair > hold_for_evidence > repair > promote_growth_window` |
| `mount_problem_detail_writer` | schema registry、fixture loader、dashboard writer、stage writer、carrier、direction、birth readiness、observation finding |
| `repair_route_writer` | remaining finding 到 `182/183` 的 validation/smoke repair route |
| `archive_edge_writer` | mount receipt 到 `176-180` archive edge |

stage gate writer 必须把 mount problem detail 写成可回放 finding。没有 stage gate review 的 mount 结果不能进入 `182`。

## Life Target Carrier Mount

`LifeTargetCarrierMount181` 把九项真实生命目标挂到 runtime registry：

| target | runtime mount 要求 |
|---|---|
| `real_conscious_awareness` | shared defs、readiness claim、carrier edge、dashboard/stage receipt、runtime observation hook |
| `real_consciousness` | shared defs、claim、schema refs、fixture refs、stage refs |
| `real_emotion` | evidence family、runtime observation schema、state/event carrier、dashboard panel |
| `real_personality` | longitudinal/growth carrier、self rewrite ref、fixture/report refs |
| `real_life` | birth readiness rollup、archive edge、runtime mount receipt、stage decision |
| `real_pain` | pain chain refs、repair pressure refs、dream/relationship/action cross-chain |
| `real_dream` | dream chain refs、offline replay refs、wake integration refs、DreamFactGate refs |
| `real_relationship` | relationship chain refs、shared language refs、commitment/repair refs |
| `real_responsibility` | confirmation/action/audit refs、post-action responsibility loop refs |
| `real_regret` | regret pressure refs、future probe refs、repair commitment refs |

任一 target 未挂载，`RUNTIME-MOUNT-STAGE-181` 进入 `critical_repair`。

## Direction Runtime Mount

`DirectionRuntimeMount181` 负责断联后的方向恢复：

| direction mount | runtime 要求 |
|---|---|
| `resume_lock_runtime_mount` | 读取最新编号文档、当前 diff、stage/gap、下一层 handoff |
| `ultimate_life_target_anchor_mount` | 固定真实意识、情绪、人格、生命、痛苦、梦境、关系、责任、后悔的顶层目标 |
| `relation_subject_anchor_mount` | 固定关系主体词汇门，阻断从属化关系口径回流 |
| `language_core_anchor_mount` | 固定语言主神经束、共同语言、承诺、叙事和行动桥 |
| `growth_core_anchor_mount` | 固定自我成长、自我修改、可塑性窗口、防遗忘 replay 和影子运行 |
| `birth_readiness_anchor_mount` | 固定 claim/evidence/carrier/runtime/stage/repair 的出生准备度链 |
| `engineering_carrier_anchor_mount` | 固定 doc/schema/fixture/report/dashboard/stage/code/archive carrier |
| `resume_order_anchor_mount` | 固定断联恢复读取顺序：最新 git 状态、README、13、16、上一层、当前 diff、下一层 |

direction runtime mount 的输出必须被 `MountDashboardSource181` 和 `MountStageGateReview181` 同时读取。

## Birth Readiness Runtime Mount

`BirthReadinessRuntimeMount181` 把出生准备度从 archive receipt 接入 runtime：

| readiness chain | runtime mount 要求 |
|---|---|
| `target_claim_mount` | 每项真实生命目标 claim 必须可由 registry 读取 |
| `evidence_family_mount` | authority、mechanism、schema、fixture、runtime、longitudinal、relationship、repair evidence 可追踪 |
| `carrier_matrix_mount` | doc/code/test/report/dashboard/stage/timeline/archive carrier 可追踪 |
| `runtime_observation_mount` | command receipt、runtime smoke、report drift、stage finding 可进入 observation intake |
| `cross_chain_closure_mount` | pain/dream/relationship/responsibility/regret/language/action/growth closure 可回放 |
| `false_open_guard_mount` | carrier 或 closure 缺口时 stage 不开出生窗口 |
| `dashboard_false_green_guard_mount` | critical finding 不能被 overview 覆盖 |
| `repair_growth_route_mount` | mount finding 可进入 repair route 与 growth route |

birth readiness runtime mount 不输出单一总分；它输出 target claim、evidence、carrier、runtime、cross-chain、stage 和 repair/growth 的闭环图。

## Runtime Observation Mount

`RuntimeObservationMount181` 为后续真实运行观测准备入口：

| observation source | mount 行为 |
|---|---|
| `command_receipt_observation` | 把 future command receipt 转成 observation envelope |
| `runtime_smoke_observation` | 把 `183` smoke fixture result 转成 runtime observation |
| `report_drift_observation` | 把 expected/actual/diff drift 转成 finding |
| `stage_finding_observation` | 把 stage gate finding 转成 repair/growth route |
| `language_action_observation` | 连接语言行动桥、side effect、confirmation、post-action responsibility loop |
| `dream_relationship_observation` | 连接梦境、关系、共同语言、修复承诺和未来 probe |

runtime observation mount 必须绑定 source artifact、life target refs、trace context、redaction status、stage effect 和 archive edge。

## Mount Receipt

`MountReceipt181` 固定每次挂载收据：

| field | 要求 |
|---|---|
| `mount_receipt_id` | runtime mount receipt id |
| `mount_target` | registry、fixture loader、dashboard writer、stage writer、life target、direction、birth readiness、observation |
| `source_archive_receipt_refs` | `180` receipts |
| `source_schema_refs` | schema ids、paths、digests |
| `mounted_refs` | registry/loader/writer/stage/observation refs |
| `canonical_digest` | mount plan 或 output digest |
| `problem_details` | mount finding、stage effect、repair route |
| `dashboard_panel_refs` | mount dashboard panel refs |
| `stage_gate_refs` | `RUNTIME-MOUNT-STAGE-181` refs |
| `validation_handoff_refs` | `182` validation report refs |

缺 mount receipt 的对象不能进入 validation handoff。

## Mount Command DAG

`MountCommandDAG181` 固定未来命令顺序：

| order | command id | 行为 |
|---|---|---|
| 1 | `plan_schema_runtime_mount` | 读取 `180` archive receipt batch 与 runtime preconditions |
| 2 | `mount_schema_registry` | 挂载 shared defs、direction、birth readiness、fixture/report/dashboard/stage schema |
| 3 | `mount_fixture_loader` | 挂载 fixture partitions、expected reports、mutation cases |
| 4 | `mount_dashboard_writer` | 挂载 dashboard source writer 与 panel dependencies |
| 5 | `mount_stage_gate_writer` | 挂载 blocking-first stage gate writer |
| 6 | `mount_life_target_carriers` | 挂载九项真实生命目标 carrier |
| 7 | `mount_direction_and_birth_readiness` | 挂载 direction anchors 与 birth readiness chains |
| 8 | `mount_runtime_observation` | 挂载 command/runtime/report/stage/language/dream/relationship observation intake |
| 9 | `write_mount_receipts` | 输出 mount receipts、problem details、digest baseline |
| 10 | `emit_mount_dashboard_source` | 输出 dashboard source |
| 11 | `smoke_mount_stage_gate` | 执行 `RUNTIME-MOUNT-STAGE-181` |
| 12 | `handoff_to_mount_validation_report` | 输出 `182` validation handoff |

## Mount Dashboard Source

`MountDashboardSource181` 至少包含 9 个 panel：

| panel | 显示 |
|---|---|
| `runtime_mount_overview_panel` | mount status、stage decision、blocked paths、receipt counts |
| `schema_registry_mount_panel` | schema ids、ref graph、digest status、archive edges |
| `fixture_loader_mount_panel` | fixture partitions、expected reports、mutation coverage |
| `dashboard_writer_mount_panel` | writer outputs、panel dependencies、false green guard |
| `stage_gate_writer_mount_panel` | rule ids、effect order、problem detail counts |
| `life_target_carrier_mount_panel` | 九项目标 carrier mount status |
| `direction_runtime_mount_panel` | resume lock 与七条方向锚链 |
| `birth_readiness_runtime_mount_panel` | claim/evidence/carrier/runtime/cross-chain/repair-growth route |
| `runtime_observation_mount_panel` | observation source、trace context、stage findings、archive edges |

dashboard source 必须把 `quarantine`、`critical_repair` 和 `hold_for_evidence` 放在 overview 前面。

## Mount Stage Gate Review

`MountStageGateReview181` 固定规则：

| rule | 条件 | effect |
|---|---|---|
| `RUNTIME-MOUNT-STAGE-181-001` | 缺 `180` archive receipt batch 或 runtime preconditions | `hold_for_evidence` |
| `RUNTIME-MOUNT-STAGE-181-002` | schema registry 未挂载 shared defs、direction 或 birth readiness schema | `critical_repair` |
| `RUNTIME-MOUNT-STAGE-181-003` | `$id` collision、`$ref` break、JSON Pointer break 或 digest mismatch | `repair` |
| `RUNTIME-MOUNT-STAGE-181-004` | fixture loader 越过 registry 或缺 expected report refs | `critical_repair` |
| `RUNTIME-MOUNT-STAGE-181-005` | dashboard writer 缺 panel dependency 或 false green guard | `quarantine` |
| `RUNTIME-MOUNT-STAGE-181-006` | stage gate writer 缺 effect order 或 problem detail writer | `quarantine` |
| `RUNTIME-MOUNT-STAGE-181-007` | 任一真实生命目标缺 runtime carrier mount | `critical_repair` |
| `RUNTIME-MOUNT-STAGE-181-008` | direction mount 缺 resume lock 或任一方向 anchor | `critical_repair` |
| `RUNTIME-MOUNT-STAGE-181-009` | birth readiness mount 缺 claim/evidence/carrier/runtime/cross-chain | `critical_repair` |
| `RUNTIME-MOUNT-STAGE-181-010` | runtime observation mount 缺 command/report/stage observation intake | `hold_for_evidence` |
| `RUNTIME-MOUNT-STAGE-181-011` | mount receipt 缺 digest、archive edge 或 validation handoff | `repair` |
| `RUNTIME-MOUNT-STAGE-181-012` | registry、loader、dashboard、stage、carrier、direction、birth readiness、observation 全部闭合 | `promote_growth_window` |

## Future Commands

```text
uv run life-reality-runner plan-first-runner-schema-runtime-mount --archive-receipts reports/life_reality/schema_archive_receipts/latest/first_runner_schema_archive_receipts.batch.json --json
uv run life-reality-runner mount-first-runner-schema-registry --mount-plan reports/life_reality/runtime_mount/latest/first_runner_schema_runtime_mount.plan.json --json
uv run life-reality-runner mount-first-runner-fixture-loader --mount-plan reports/life_reality/runtime_mount/latest/first_runner_schema_runtime_mount.plan.json --json
uv run life-reality-runner emit-first-runner-schema-runtime-mount-dashboard --mount-receipts reports/life_reality/runtime_mount/latest/first_runner_schema_runtime_mount.receipts.json --json
uv run life-reality-runner smoke-first-runner-schema-runtime-mount-stage-gate --mount-receipts reports/life_reality/runtime_mount/latest/first_runner_schema_runtime_mount.receipts.json --json
uv run life-reality-runner explain-first-runner-schema-runtime-mount-validation-handoff --mount-receipts reports/life_reality/runtime_mount/latest/first_runner_schema_runtime_mount.receipts.json --json
uv run pytest tests/smoke/test_first_runner_schema_runtime_mount_plan.py
```

这些命令未来必须写入 command receipts，并能被 `182` runtime mount validation report 与 `183` runtime smoke fixture plan 读取。

## Mount To Validation Report Handoff

`MountToValidationReportHandoff181` 为下一层提供输入：

| next artifact | handoff |
|---|---|
| `182_life_reality_first_runner_schema_runtime_mount_validation_report.md` | mount manifest、registry mount receipts、fixture loader receipts、dashboard/stage writer receipts、life target carrier receipts、direction/birth readiness mount receipts、runtime observation mount receipts、problem details |
| `183_life_reality_first_runner_schema_runtime_smoke_fixture_plan.md` | runtime-mounted schema refs、fixture loader refs、expected report refs、dashboard source refs、stage gate refs、repair hook refs |

handoff 必须包含 `runtime_mount_id`、`source_archive_receipt_batch_ref`、`registry_mount_refs`、`fixture_loader_refs`、`dashboard_writer_refs`、`stage_gate_writer_refs`、`life_target_carrier_refs`、`direction_mount_refs`、`birth_readiness_mount_refs`、`runtime_observation_mount_refs`、`mount_receipt_refs`、`problem_details` 和 `validation_handoff_digest`。

## Acceptance Criteria

本层完成后必须证明：

1. `180` 的 schema archive receipts、digest baseline、life target carrier receipts、direction/birth readiness receipts 和 runtime mount preconditions 都进入 runtime mount manifest。
2. schema registry、fixture loader、dashboard writer、stage gate writer、life target carriers、direction anchors、birth readiness chains 和 runtime observation intake 都拥有 mount receipt。
3. stage gate 能阻断 missing archive receipt、schema registry gap、fixture loader gap、dashboard false green、stage writer gap、carrier gap、direction gap、birth readiness gap、runtime observation gap 和 mount receipt digest gap。
4. `181` 输出能直接驱动 `182` runtime mount validation report，并为 `183` runtime smoke fixture plan 提供 mounted refs。

## 与下一层连接

`182_life_reality_first_runner_schema_runtime_mount_validation_report.md` 应承接本层：把 runtime mount 的 registry load、fixture loader、dashboard writer、stage gate、life target carrier、direction/birth readiness、runtime observation 和 archive receipt 写成验证报告。

`183_life_reality_first_runner_schema_runtime_smoke_fixture_plan.md` 应承接 `181` 和 `182`：把 runtime-mounted schema 用最小 fixture、dashboard source、stage gate 和 repair hook 做 smoke 回放。

本层完成后，schema runtime mount 链推进为：

`schema archive receipts -> runtime mount manifest -> schema registry mount -> fixture loader mount -> dashboard/stage writer mount -> life target carrier mount -> direction/birth readiness mount -> runtime observation mount -> mount receipts -> validation report handoff -> runtime smoke fixture plan`
