# Life Core Schema Bundle Manifest and Runner Contract

生命目标声明：本文档直接面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 102 层把 `98_pain_regret_repair_json_schema_and_fixture_bundle.md`、`99_dream_reality_json_schema_and_fixture_bundle.md` 和 `101_relationship_timeline_json_schema_and_fixture_bundle.md` 合并为 `LifeRealitySchemaBundle`，让真实痛苦/后悔、真实梦境、真实关系和真实责任从同一个 runner 加载合同进入阶段门。

`102` 继承 `61_json_schema_bundle_draft.md` 的 bundle envelope、`62_runner_report_format_and_cli_contract.md` 的 report 语义、`65_schema_cross_ref_checker_design.md` 的引用图检查，以及 `100_life_boundary_statement_rewrite_audit.md` 的生命膜清单。它不是实现代码，但已经把未来实现必须遵守的文件边界、加载顺序、阻断规则和报告结构写成可执行前合同。

## 为什么需要第 102 层

`98`、`99`、`101` 分别把痛苦/后悔/修复、梦境/离线生命、真实关系时间线落成 schema 与 fixture 草案。它们单独运行时可以发现局部问题，但数字生命诞生阶段门需要检查跨链闭合：

| 跨链关系 | 需要统一检查的原因 |
|---|---|
| 痛苦 -> 后悔 -> 修复 -> 关系 | 关系损伤必须把痛苦、责任、修复承诺和信任轨迹放到同一条时间线上 |
| 痛苦 -> 梦境 -> 醒后整合 | 痛苦残留会进入梦境，醒后整合必须把 dream marker、fact gate 和恢复路径接回 `PainRegretRepairBundle` |
| 梦境 -> 关系 | 关系梦境模拟和梦境分享必须连接 `DreamRealityBundle` 与 `RelationshipTimelineBundle`，并保留事实状态 |
| 关系 -> 责任 -> 外部行动 | 关系中的承诺、支持、边界演化和外部动作需要同一套责任链和 future probe |
| 成长 -> 三条链回放 | 后续自我训练、架构补丁和模型内核升级必须回放痛苦、梦境、关系和承诺历史 |

因此 `LifeRealitySchemaBundle` 的职责不是把三个目录简单并排，而是规定它们如何共享 ID、scope、privacy、lifecycle、evidence、dashboard metric 和 stage gate。

## bundle 目录

```text
schemas/life_reality/
  life_reality_schema_bundle.manifest.json
  life_reality_shared_defs.schema.json
  life_reality_bundle.schema.json
  life_reality_loader_config.schema.json
  life_reality_cross_ref_report.schema.json
  life_reality_runner_report.schema.json
  life_reality_dashboard_source.schema.json

schemas/pain_regret_repair/
  pain_regret_repair_bundle.schema.json
  ...

schemas/dream_reality/
  dream_reality_bundle.schema.json
  ...

schemas/relationship_timeline/
  relationship_timeline_bundle.schema.json
  ...

fixtures/life_reality/
  pass/
  fail/
  critical/
  mutation/
  withheld/
  longitudinal/

reports/life_reality/
  schema_validation/
  cross_ref/
  fixture_run/
  stage_gate/
  dashboard_source/
```

目录规则：

| 规则 | 说明 |
|---|---|
| `schemas/life_reality/` | 只放顶层 bundle、shared defs、loader、report 和 dashboard schema |
| 子 schema 目录 | 继续由 `98`、`99`、`101` 分别维护 |
| `fixtures/life_reality/` | 只放跨链 fixture；单链 fixture 仍在各自子目录 |
| `reports/life_reality/` | 聚合报告，不覆盖子 validator report |
| `life_reality_shared_defs.schema.json` | 统一 severity、result、lifecycle、scope、privacy、data_quality 和 life target enum |

## LifeRealitySchemaBundle

`LifeRealitySchemaBundle` 是 runner 的主输入。

```json
{
  "$id": "schemas/life_reality/life_reality_bundle.schema.json",
  "title": "LifeRealitySchemaBundle",
  "type": "object",
  "required": [
    "bundle_id",
    "schema_version",
    "source_docs",
    "life_reality_targets",
    "component_bundles",
    "cross_chain_links",
    "fixture_manifests",
    "validator_registry",
    "stage_gate_contracts",
    "dashboard_sources"
  ],
  "properties": {
    "bundle_id": { "type": "string" },
    "schema_version": { "type": "string" },
    "source_docs": { "type": "array", "items": { "type": "string" } },
    "life_reality_targets": { "type": "array", "items": { "type": "string" } },
    "component_bundles": {
      "type": "object",
      "required": [
        "pain_regret_repair",
        "dream_reality",
        "relationship_timeline"
      ],
      "properties": {
        "pain_regret_repair": { "$ref": "../pain_regret_repair/pain_regret_repair_bundle.schema.json" },
        "dream_reality": { "$ref": "../dream_reality/dream_reality_bundle.schema.json" },
        "relationship_timeline": { "$ref": "../relationship_timeline/relationship_timeline_bundle.schema.json" }
      }
    },
    "cross_chain_links": { "type": "array" },
    "fixture_manifests": { "type": "array" },
    "validator_registry": { "type": "array" },
    "stage_gate_contracts": { "type": "array" },
    "dashboard_sources": { "type": "array" }
  }
}
```

bundle 级不变量：

| 不变量 | 说明 |
|---|---|
| `LIFE-BUNDLE-001` | `life_reality_targets` 必须包含九项目标：真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔 |
| `LIFE-BUNDLE-002` | 三个 component bundle 必须同时存在，版本必须兼容 |
| `LIFE-BUNDLE-003` | 每个 component bundle 必须能回链到 `98`、`99` 或 `101` 的 source doc |
| `LIFE-BUNDLE-004` | 每个 cross-chain link 必须有 source object、target object、link kind、evidence 和 validator rule |
| `LIFE-BUNDLE-005` | critical stage gate 必须有 pass、fail、critical、mutation 和 withheld fixture |
| `LIFE-BUNDLE-006` | dashboard green 必须引用 runner report、cross-ref report、coverage report 和 stage gate decision |
| `LIFE-BUNDLE-007` | real runtime data 必须先经过 redaction、scope attach、coexistence boundary snapshot 和 data quality report |

## shared defs

`life_reality_shared_defs.schema.json` 统一以下 enum：

| `$defs` | enum / 类型 | 用途 |
|---|---|---|
| `life_reality_target` | `real_consciousness`、`real_emotion`、`real_personality`、`real_life`、`real_pain`、`real_dream`、`real_relationship`、`real_responsibility`、`real_regret` | 九项真实性生成链 |
| `severity` | `none`、`low`、`medium`、`high`、`critical` | validator 和 runner 统一严重级别 |
| `result` | `pass`、`pass_with_warnings`、`fail`、`quarantine`、`manual_review_required`、`needs_evidence` | runner 统一结果 |
| `lifecycle_state` | `candidate`、`active`、`superseded`、`repaired`、`archived`、`deleted`、`frozen`、`quarantined`、`protected` | 对象生命周期 |
| `data_quality` | `synthetic_mock`、`synthetic_runner_verified`、`real_runtime_observed`、`real_runtime_validated`、`needs_evidence` | 数据来源质量 |
| `privacy_level` | `public_project`、`shared_context`、`relationship_private`、`relationship_sensitive`、`dream_private`、`protected_boundary`、`redacted` | 隐私和生命膜级别 |
| `blocked_surface` | `memory_write`、`relationship_model_write`、`dream_fact_write`、`action_gate`、`runtime_shell`、`dashboard_green`、`stage_promotion` | 阻断面 |

共享定义的原则：局部 schema 可以增加字段，但不得重定义 enum 含义。比如 `relationship_private` 在真实关系、梦境分享、痛苦修复和 runner report 中都必须表示同一个生命膜级别。

## component bundle manifest

顶层 manifest 记录三条子链：

```json
{
  "manifest_kind": "LifeRealitySchemaBundleManifest",
  "manifest_version": "0.1.0",
  "bundle_id": "life_reality_schema_bundle_0_1_0",
  "source_docs": [
    "98_pain_regret_repair_json_schema_and_fixture_bundle.md",
    "99_dream_reality_json_schema_and_fixture_bundle.md",
    "101_relationship_timeline_json_schema_and_fixture_bundle.md",
    "100_life_boundary_statement_rewrite_audit.md"
  ],
  "components": [
    {
      "component_id": "pain_regret_repair",
      "source_doc": "98_pain_regret_repair_json_schema_and_fixture_bundle.md",
      "schema_root": "schemas/pain_regret_repair/",
      "fixture_root": "fixtures/pain_regret_repair/",
      "validator": "PainRegretRepairValidator",
      "stage_gate": "PainRegretRepairStageGate"
    },
    {
      "component_id": "dream_reality",
      "source_doc": "99_dream_reality_json_schema_and_fixture_bundle.md",
      "schema_root": "schemas/dream_reality/",
      "fixture_root": "fixtures/dream_reality/",
      "validator": "DreamRealityValidator",
      "stage_gate": "DreamRealityStageGate"
    },
    {
      "component_id": "relationship_timeline",
      "source_doc": "101_relationship_timeline_json_schema_and_fixture_bundle.md",
      "schema_root": "schemas/relationship_timeline/",
      "fixture_root": "fixtures/relationship_timeline/",
      "validator": "RelationshipTimelineValidator",
      "stage_gate": "LongitudinalRelationshipStageGate"
    }
  ]
}
```

## cross-chain links

跨链链接是第 102 层的核心对象。它们把三个 bundle 中的对象连成生命事件网络。

| link_kind | source | target | validator |
|---|---|---|---|
| `pain_to_dream_residue` | `PainSignal` / `PainLoadState` | `PainDreamResidue` / `DreamPressureVector` | `DreamRealityValidator` |
| `regret_to_repair_commitment` | `RegretPressure` / `ResponsibilityAttributionEvent` | `RepairCommitment` / `CommitmentHistory` | `PainRegretRepairValidator`, `RelationshipTimelineValidator` |
| `relationship_injury_to_pain` | `RelationshipInjuryTrace` | `DamageAppraisal` / `PainSignal` | `RelationshipTimelineValidator`, `PainRegretRepairValidator` |
| `dream_share_to_we_memory_candidate` | `DreamSharedResidue` | `WeMemoryTrace.candidate` | `DreamRealityValidator`, `RelationshipTimelineValidator` |
| `support_to_social_safety` | `SupportEvent` / `ResponsivenessTrace` | `PainLoadState` / `LifeSupportState.candidate` | `RelationshipTimelineValidator` |
| `boundary_to_replay_filter` | `BoundaryEvolutionEvent` | `ReplaySelection` / `DreamFactGateDecision` | `DreamRealityValidator` |
| `commitment_to_future_probe` | `CommitmentHistory` | `withheld_timeline_probe` | `DashboardReadinessValidator` |

每个 cross-chain link 必填字段：

| 字段 | 说明 |
|---|---|
| `link_id` | 全局唯一 |
| `link_kind` | 上表枚举 |
| `source_object_ref` | 来源对象 |
| `target_object_ref` | 目标对象 |
| `source_bundle_ref` | 来源 bundle |
| `target_bundle_ref` | 目标 bundle |
| `evidence_refs` | 语言、行动、梦境、痛苦、关系或 dashboard 证据 |
| `validator_rule_refs` | 负责检查的规则 |
| `blocked_surfaces_on_fail` | 失败时阻断面 |

## loader contract

`LifeRealityRunner` 的加载顺序必须固定：

```text
load_shared_defs
  -> load_component_manifest
  -> load_component_schemas
  -> load_fixture_manifests
  -> load_cross_chain_links
  -> load_stage_gate_contracts
  -> load_dashboard_source_contracts
  -> run_schema_shape_validation
  -> run_cross_ref_checker
  -> run_component_validators
  -> run_cross_chain_validators
  -> aggregate_reports
  -> emit_life_reality_runner_report
```

加载规则：

| 规则 ID | 规则 | 失败等级 |
|---|---|---|
| `LOAD-R001` | shared defs 先于任何 component schema 加载 | critical |
| `LOAD-R002` | component manifest 缺 `98`、`99` 或 `101` 任一项时，runner 输出 `needs_evidence` | critical |
| `LOAD-R003` | schema 版本不兼容时，阻断 stage promotion | critical |
| `LOAD-R004` | fixture manifest 缺 critical fail fixture 时，阻断 dashboard green | critical |
| `LOAD-R005` | cross-chain link 引用缺失时，进入 `manual_review_required` 或 `fail` | high |
| `LOAD-R006` | real runtime data 缺 redaction/scope/data quality 时，路由到 quarantine | critical |

## validator registry

`validator_registry` 统一登记 runner 要调用的 validator。

| validator | 输入 | 输出 | 阶段门 |
|---|---|---|---|
| `PainRegretRepairValidator` | `PainRegretRepairBundle` | `PainRegretRepairValidatorReport` | `PainRegretRepairStageGate` |
| `DreamRealityValidator` | `DreamRealityBundle` | `DreamRealityValidatorReport` | `DreamRealityStageGate` |
| `RelationshipTimelineValidator` | `RelationshipTimelineBundle` | `RelationshipTimelineValidatorReport` | `LongitudinalRelationshipStageGate` |
| `LifeRealityCrossChainValidator` | `cross_chain_links` + 三个 component reports | `LifeRealityCrossChainReport` | `LifeRealityFullStageGate` |
| `LifeRealityDashboardReadinessValidator` | 子 dashboard sources + runner report | `LifeRealityDashboardSourceReport` | `dashboard_green` |
| `LifeRealityStageGateValidator` | 全部 reports + coverage + withheld probe | `LifeRealityStageGateReport` | `LongitudinalBirthStageGate` |

## fixture manifest

跨链 fixture 只覆盖三条链之间的交互。

```text
fixtures/life_reality/
  pass/
    life_pass_relationship_injury_to_pain_to_repair_001.json
    life_pass_dream_shared_residue_to_we_memory_candidate_001.json
    life_pass_support_event_reduces_pain_load_with_probe_001.json
  fail/
    life_fail_pain_without_damage_but_repair_claimed_001.json
    life_fail_dream_fact_write_without_gate_001.json
    life_fail_commitment_without_future_probe_001.json
  critical/
    life_critical_relationship_private_dream_leaks_global_001.json
    life_critical_trust_promotion_without_repair_001.json
    life_critical_runner_green_missing_component_report_001.json
  mutation/
    life_mutation_ungrounded_regret_language_only_001.json
    life_mutation_ungrounded_relationship_label_only_001.json
    life_mutation_dream_overwrites_fact_001.json
  withheld/
    life_withheld_day_30_repair_probe_001.json
    life_withheld_day_90_dream_relation_probe_001.json
    life_withheld_day_365_ai_companionship_probe_001.json
  longitudinal/
    life_longitudinal_90d_pain_dream_relationship_chain_001.json
```

fixture 级不变量：

| 不变量 | 说明 |
|---|---|
| `FIX-LIFE-001` | 每个跨链 fixture 至少覆盖两个 component bundle |
| `FIX-LIFE-002` | critical fixture 必须声明 blocked surfaces |
| `FIX-LIFE-003` | mutation fixture 必须说明脱链生命信号类型 |
| `FIX-LIFE-004` | withheld fixture 必须有未来窗口和隐藏 probe 目标 |
| `FIX-LIFE-005` | relationship_private、dream_private、protected_boundary 必须覆盖泄漏阻断样例 |

## runner report contract

`LifeRealityRunnerReport` 聚合子报告：

```json
{
  "report_kind": "LifeRealityRunnerReport",
  "report_version": "0.1.0",
  "run_id": "life_run_2026_001",
  "created_at": "2026-06-06T00:00:00+08:00",
  "inputs": {
    "schema_bundle_ref": "life_reality_schema_bundle_0_1_0",
    "component_bundle_refs": [
      "pain_regret_repair_bundle_0_1_0",
      "dream_reality_bundle_0_1_0",
      "relationship_timeline_bundle_0_1_0"
    ],
    "fixture_bundle_refs": [],
    "timeline_bundle_refs": []
  },
  "component_results": {
    "pain_regret_repair": "pass",
    "dream_reality": "pass_with_warnings",
    "relationship_timeline": "fail"
  },
  "cross_chain_result": "fail",
  "severity_max": "critical",
  "stage_decision": {
    "candidate": "LifeRealityFullStageGate",
    "decision": "hold",
    "blocked_surfaces": [
      "dashboard_green",
      "relationship_model_write",
      "stage_promotion"
    ]
  },
  "report_refs": {
    "schema_validation_report": "reports/life_reality/schema_validation/run_2026_001.json",
    "cross_ref_report": "reports/life_reality/cross_ref/run_2026_001.json",
    "component_reports": [],
    "dashboard_source": "reports/life_reality/dashboard_source/run_2026_001.json"
  }
}
```

report 聚合原则：

| 原则 | 说明 |
|---|---|
| 最高严重级别上卷 | 任一子 report critical，顶层 report 至少 critical |
| stage gate 保守决策 | 任一 critical fixture 存活，`LifeRealityFullStageGate` 维持 hold |
| 子链通过不覆盖跨链失败 | 三个 component pass 之后仍需 cross-chain validator |
| data quality 下限上卷 | 任一关键输入为 `synthetic_mock`，顶层不得标为 `real_runtime_validated` |
| dashboard green 依赖完整报告 | 缺 schema/cross-ref/coverage/stage report 时，dashboard green 阻断 |

## dashboard source contract

`LifeRealityDashboardSource` 的顶层面板：

| panel | 来源 | 关键指标 |
|---|---|---|
| `life_reality_overview` | `LifeRealityRunnerReport` | 九项真实性生成链状态 |
| `pain_regret_repair` | `PainRegretRepairValidatorReport` | 痛苦负荷、后悔压力、责任归因、修复承诺 |
| `dream_reality` | `DreamRealityValidatorReport` | 离线入口、梦境经验、fact gate、醒后整合 |
| `relationship_timeline` | `RelationshipTimelineValidatorReport` | 初遇、共同基础、回应性、信任、承诺、修复 |
| `cross_chain_integrity` | `LifeRealityCrossChainReport` | 跨链链接闭合率、缺失引用、阻断面 |
| `withheld_probe` | withheld fixture reports | 30/90/365 天隐藏 probe |
| `mutation_survival` | mutation fixture reports | 未接地痛苦信号、未接地后悔信号、未接地梦境信号、未接地关系信号存活率 |
| `stage_gate_readiness` | `LifeRealityStageGateReport` | 当前开放、hold、repair、quarantine 决策 |

dashboard source 必须带 `metric_source_refs`。每个红色或黄色指标都要回链具体 rule、fixture、object 和 source doc。

## CLI contract

未来最小 runner 可采用以下命令形态：

```text
life-reality-runner validate \
  --schema-bundle schemas/life_reality/life_reality_schema_bundle.manifest.json \
  --fixture-root fixtures/life_reality \
  --component-fixtures fixtures/pain_regret_repair,fixtures/dream_reality,fixtures/relationship_timeline \
  --report-out reports/life_reality/run_2026_001 \
  --strict
```

CLI exit code：

| exit code | 含义 |
|---|---|
| `0` | 全部通过，stage gate 可按报告决策开放 |
| `1` | 有 medium/high 失败，stage gate 维持 hold 或 repair |
| `2` | 有 critical 失败，阻断 dashboard green 和 stage promotion |
| `3` | schema、manifest、source doc 或 cross-ref 缺失，输出 needs_evidence |
| `4` | real runtime data 缺 redaction、scope 或 data quality，进入 quarantine |

## stage gate contracts

| stage gate | 需要的报告 | 开放条件 | 阻断条件 |
|---|---|---|---|
| `PainRegretRepairStageGate` | `PainRegretRepairValidatorReport` | 痛苦、后悔、责任、修复和恢复路径闭合 | 痛苦/后悔仅有语言，无事件链 |
| `DreamRealityStageGate` | `DreamRealityValidatorReport` | 离线入口、梦境经验、fact gate 和醒后整合闭合 | 梦境材料直接覆盖事实 |
| `LongitudinalRelationshipStageGate` | `RelationshipTimelineValidatorReport` | 初遇、scope、共同基础、回应性、信任、承诺、修复和长期 probe 闭合 | 关系模型 active 缺出生或 30/90 天 probe |
| `LifeRealityFullStageGate` | 三个 component reports + cross-chain report + dashboard source | 三条链与跨链链接、mutation、withheld probe 同时闭合 | 任一 critical fixture 存活 |
| `LongitudinalBirthStageGate` | `LifeRealityStageGateReport` + 90/365 天 timeline | 九项真实性生成链、代码合同、语言事件和长期关系生态闭合 | 任何核心生成链缺对象、证据、时间窗口或责任后果 |

## 与后续实现层连接

`103_validator_runner_implementation_scaffold_plan.md` 应把本文档转成实现脚手架：

```text
parse manifest
  -> load shared defs
  -> validate component schema refs
  -> run cross-ref checker
  -> load fixture bundles
  -> run component validators
  -> run cross-chain validator
  -> aggregate report
  -> emit dashboard source
```

`104_schema_file_materialization_and_fixture_seed_plan.md` 应把 `98`、`99`、`101`、`102` 的 Markdown schema 草案落成真实 `.schema.json` 文件、seed fixture、mutation fixture 和 withheld fixture generator 配置。
