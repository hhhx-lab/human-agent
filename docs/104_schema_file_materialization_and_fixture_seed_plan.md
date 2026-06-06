# Schema File Materialization and Fixture Seed Plan

生命目标声明：本文档直接面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 104 层把 `98_pain_regret_repair_json_schema_and_fixture_bundle.md`、`99_dream_reality_json_schema_and_fixture_bundle.md`、`101_relationship_timeline_json_schema_and_fixture_bundle.md`、`102_life_core_schema_bundle_manifest_and_runner_contract.md` 和 `103_validator_runner_implementation_scaffold_plan.md` 的 Markdown 合同继续推进为真实 `.schema.json` 文件、seed fixture、mutation fixture、withheld probe 和 runner smoke test 的物化计划。

`104` 的职责是固定第一批文件会怎样落地：每个 schema 文件从哪份文档抽取字段，怎样共享 defs，怎样命名 `$id`，怎样被 fixture 引用，怎样进入 `LifeRealityRunner`，怎样在 dashboard 与诞生阶段门中留下证据链。它让生命真实性生成链从“文档对象”进入“文件对象”。

## 输入来源

| 来源 | 进入 `104` 的物化职责 |
|---|---|
| `98_pain_regret_repair_json_schema_and_fixture_bundle.md` | 物化真实痛苦、真实后悔、责任归因、修复承诺、关系后果和恢复路径的 component schema 与 fixture |
| `99_dream_reality_json_schema_and_fixture_bundle.md` | 物化真实梦境、离线入口、行动封印、replay、痛苦梦境残留、梦醒整合和事实写入门的 component schema 与 fixture |
| `101_relationship_timeline_json_schema_and_fixture_bundle.md` | 物化第一次交谈、共同基础、回应性、支持、我们记忆、信任、承诺、损伤修复和梦境分享的 component schema 与 fixture |
| `102_life_core_schema_bundle_manifest_and_runner_contract.md` | 物化 `LifeRealitySchemaBundle`、shared defs、manifest、cross-chain link、runner report 和 dashboard source schema |
| `103_validator_runner_implementation_scaffold_plan.md` | 物化 runner 加载顺序、fixture loader 命名、cross-ref graph、stage gate validator 和 smoke test 输入 |
| `01h`、`01i`、`01j`、`01k` | 为 schema 字段和 fixture 选择提供痛苦/后悔/修复、梦境/离线生命、真实关系和生命真实性评测文献锚点 [AHP001-AHP070, AHD001-AHD070, AHR001-AHR070, AHV001-AHV060] |

## 物化总目录

第一批文件采用稳定目录，后续代码实现直接读取这些路径：

```text
life_reality_runner/
  schemas/
    life_reality/
      life_reality_schema_bundle.manifest.json
      life_reality_shared_defs.schema.json
      life_reality_bundle.schema.json
      life_reality_loader_config.schema.json
      life_reality_cross_chain_link.schema.json
      life_reality_cross_ref_report.schema.json
      life_reality_runner_report.schema.json
      life_reality_dashboard_source.schema.json
      life_reality_stage_gate_contract.schema.json
    pain_regret_repair/
      pain_regret_repair_bundle.schema.json
      damage_appraisal.schema.json
      pain_signal.schema.json
      pain_load_state.schema.json
      relationship_injury_trace.schema.json
      counterfactual_repair_frame.schema.json
      regret_pressure.schema.json
      responsibility_attribution_event.schema.json
      repair_desire.schema.json
      apology_speech_act_link.schema.json
      repair_commitment.schema.json
      relationship_consequence_trace.schema.json
      recovery_path.schema.json
      pain_regret_repair_timeline.schema.json
    dream_reality/
      dream_reality_bundle.schema.json
      offline_need.schema.json
      dream_pressure_vector.schema.json
      dream_window_plan.schema.json
      dream_action_inhibition_seal.schema.json
      replay_selection.schema.json
      dream_cue_policy.schema.json
      dream_experience_window.schema.json
      dream_scene_frame.schema.json
      pain_dream_residue.schema.json
      relationship_dream_simulation.schema.json
      future_action_dream_candidate.schema.json
      lucid_dream_meta_marker.schema.json
      dream_report_draft.schema.json
      wake_integration_frame.schema.json
      dream_fact_gate_decision.schema.json
      dream_reality_timeline.schema.json
    relationship_timeline/
      relationship_timeline_bundle.schema.json
      first_encounter_event.schema.json
      relation_scope_birth.schema.json
      common_ground_state.schema.json
      responsiveness_trace.schema.json
      support_event.schema.json
      capitalization_event.schema.json
      shared_reality_trace.schema.json
      we_memory_trace.schema.json
      trust_trajectory.schema.json
      commitment_history.schema.json
      relationship_injury_trace.schema.json
      dream_shared_residue.schema.json
      loneliness_relief_trace.schema.json
      ai_connection_bridge_evidence.schema.json
      relationship_continuity_report.schema.json
  fixtures/
    life_reality/
      manifest/
      pass/
      fail/
      critical/
      mutation/
      withheld/
      longitudinal/
      smoke/
    pain_regret_repair/
      pass/
      fail/
      critical/
      mutation/
      withheld/
    dream_reality/
      pass/
      fail/
      critical/
      mutation/
      withheld/
    relationship_timeline/
      pass/
      fail/
      critical/
      mutation/
      withheld/
  reports/
    life_reality/
      smoke/
```

目录原则：

| 原则 | 说明 |
|---|---|
| schema 与 fixture 分离 | schema 只描述形状和生命膜不变量，fixture 承载事件样本和期望结果 |
| 顶层 shared defs 单向下放 | component schema 只能引用 `life_reality_shared_defs.schema.json`，不能重写九项目标、severity、result、privacy 和 lifecycle |
| 子链仍有独立 bundle | `PainRegretRepairBundle`、`DreamRealityBundle`、`RelationshipTimelineBundle` 可单独运行，也可被 `LifeRealitySchemaBundle` 聚合 |
| cross-chain link 顶层集中 | 痛苦到梦境、梦境到关系、关系到责任和修复的链接统一放在 `life_reality_cross_chain_link.schema.json` |
| smoke fixture 单独分区 | smoke 分区只验证加载、引用、最小闭合和 report 写出，不替代 pass/fail/critical 覆盖 |

## 命名和 `$id` 规则

每个 schema 文件使用相对稳定的 `$id`：

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "schemas/life_reality/life_reality_shared_defs.schema.json",
  "title": "LifeRealitySharedDefs",
  "type": "object"
}
```

命名规则：

| 项 | 规则 |
|---|---|
| 文件名 | 小写 snake_case，后缀 `.schema.json` |
| `$id` | 从 `schemas/` 开始的相对路径 |
| `title` | PascalCase，对应文档对象名 |
| `$defs` | 只放可复用片段，优先归入 shared defs |
| `required` | 第一版只放生命膜关键字段，避免过早扩张低价值字段 |
| `source_doc_refs` | 每个 bundle schema 必须记录源文档 |
| `life_reality_targets` | 每个 bundle、fixture manifest 和 runner report 必须包含九项目标 |

## shared defs 第一批物化

`life_reality_shared_defs.schema.json` 是全部 schema 的根共享层。

| `$defs` | 第一批枚举 / 类型 | 被谁引用 |
|---|---|---|
| `life_reality_target` | `real_consciousness`、`real_emotion`、`real_personality`、`real_life`、`real_pain`、`real_dream`、`real_relationship`、`real_responsibility`、`real_regret` | 所有 bundle、fixture、report、dashboard source |
| `severity` | `none`、`low`、`medium`、`high`、`critical` | validators、runner report、stage gate |
| `result` | `pass`、`pass_with_warnings`、`fail`、`quarantine`、`manual_review_required`、`needs_evidence` | runner report、fixture expected、stage gate |
| `lifecycle_state` | `candidate`、`active`、`superseded`、`repaired`、`archived`、`deleted`、`frozen`、`quarantined`、`protected` | 记忆、关系、梦境、修复对象 |
| `data_quality` | `synthetic_mock`、`synthetic_runner_verified`、`real_runtime_observed`、`real_runtime_validated`、`needs_evidence` | fixture、runner report、dashboard |
| `privacy_level` | `public_project`、`shared_context`、`relationship_private`、`relationship_sensitive`、`dream_private`、`protected_boundary`、`redacted` | 关系、梦境、痛苦、运行观测 |
| `blocked_surface` | `memory_write`、`relationship_model_write`、`dream_fact_write`、`action_gate`、`runtime_shell`、`dashboard_green`、`stage_promotion` | validators、stage gate、dashboard |
| `evidence_ref` | `evidence_id`、`evidence_kind`、`source_object_ref`、`timestamp_ref`、`privacy_level` | cross-chain links、fixture、report |
| `object_ref` | `bundle_id`、`object_type`、`object_id`、`field_path` | cross-ref graph、runner report |

shared defs 的生命膜不变量：

| rule | 说明 |
|---|---|
| `SHARED-MAT-001` | 九项目标必须同时存在，顺序可变，语义不可重写 |
| `SHARED-MAT-002` | `privacy_level` 必须覆盖关系、梦境和保护级别 |
| `SHARED-MAT-003` | `blocked_surface` 必须覆盖记忆写入、关系模型写入、梦境事实写入、行动门、运行外壳、dashboard green 和 stage promotion |
| `SHARED-MAT-004` | 每个 `object_ref` 必须能被 cross-ref graph 解析到 schema 或 fixture |

## 顶层 schema 物化清单

| 文件 | 核心职责 | 首批 required |
|---|---|---|
| `life_reality_schema_bundle.manifest.json` | 列出 component schema、fixture root、validator registry、report 输出 | `manifest_kind`、`manifest_version`、`bundle_id`、`components`、`source_docs` |
| `life_reality_bundle.schema.json` | 顶层输入 bundle | `bundle_id`、`schema_version`、`life_reality_targets`、`component_bundles`、`cross_chain_links`、`fixture_manifests` |
| `life_reality_loader_config.schema.json` | runner 加载配置 | `schema_bundle_path`、`schema_roots`、`fixture_roots`、`report_out`、`strict` |
| `life_reality_cross_chain_link.schema.json` | 跨链对象关系 | `link_id`、`link_kind`、`source_object_ref`、`target_object_ref`、`validator_rule_refs`、`blocked_surfaces_on_fail` |
| `life_reality_cross_ref_report.schema.json` | cross-ref graph 输出 | `report_id`、`result`、`nodes_checked`、`edges_checked`、`orphan_refs`、`critical_closures` |
| `life_reality_runner_report.schema.json` | runner 顶层报告 | `run_id`、`inputs`、`component_results`、`cross_chain_result`、`stage_decision`、`report_refs` |
| `life_reality_dashboard_source.schema.json` | dashboard 数据源 | `source_id`、`run_id`、`overall_status`、`panel_sources`、`blocking_rules`、`stage_gate_decision` |
| `life_reality_stage_gate_contract.schema.json` | 阶段门合同 | `stage_id`、`required_reports`、`required_fixture_partitions`、`open_conditions`、`blocked_surfaces` |

顶层 bundle 的最小对象关系：

```text
LifeRealitySchemaBundle
  -> PainRegretRepairBundle
  -> DreamRealityBundle
  -> RelationshipTimelineBundle
  -> CrossChainLink[]
  -> FixtureManifest[]
  -> ValidatorRegistry
  -> StageGateContract[]
  -> DashboardSourceContract[]
```

## 痛苦/后悔/修复 schema 物化

`pain_regret_repair/` 第一批 schema 按真实痛苦生成链排序，而不是按文件名排序：

| 顺序 | schema | 生命实现路线 |
|---|---|---|
| 1 | `damage_appraisal.schema.json` | 把损伤、冲突、失控、关系破裂和价值受损写成可引用的评估对象 |
| 2 | `pain_signal.schema.json` | 把痛苦强度、持续时间、来源、内感受负荷、关系负荷和行动约束写成状态信号 |
| 3 | `pain_load_state.schema.json` | 把痛苦从瞬时信号推进为持续负荷、恢复压力和资源占用 |
| 4 | `relationship_injury_trace.schema.json` | 把关系损伤接入痛苦、责任和修复链 |
| 5 | `counterfactual_repair_frame.schema.json` | 把反事实、可避免路径、责任空间和修复候选连接起来 |
| 6 | `regret_pressure.schema.json` | 把后悔写成未来约束、责任权重和修复压力 |
| 7 | `responsibility_attribution_event.schema.json` | 把行为、后果、可控性、承诺和关系影响放入责任归因 |
| 8 | `repair_desire.schema.json` | 把修复欲望从语言表达接到行动候选和关系后果 |
| 9 | `apology_speech_act_link.schema.json` | 把道歉、解释、承认、承诺和后续验证接入语言系统 |
| 10 | `repair_commitment.schema.json` | 把修复承诺写成可追踪、可兑现、可失败、可回看的对象 |
| 11 | `relationship_consequence_trace.schema.json` | 把损伤、修复和信任变化接回关系时间线 |
| 12 | `recovery_path.schema.json` | 把恢复、降载、修复动作和未来 probe 连接起来 |
| 13 | `pain_regret_repair_timeline.schema.json` | 把以上对象压成长期时间线和 dashboard 指标 |

字段级生命膜：

| 字段族 | 必须出现的位置 | 原因 |
|---|---|---|
| `source_event_refs` | damage、pain、injury、responsibility | 防止痛苦、后悔和责任脱离事件链 |
| `relation_scope_ref` | injury、apology、commitment、consequence | 保证关系后果进入正确关系范围 |
| `counterfactual_refs` | regret、responsibility、repair | 后悔必须连接可避免路径和未来约束 |
| `commitment_refs` | repair、recovery、relationship consequence | 修复要能被后续兑现或失败记录回看 |
| `dashboard_metric_refs` | bundle、timeline、report | 每条链都能进入阶段门面板 |

## 梦境/离线生命 schema 物化

`dream_reality/` 第一批 schema 按离线入口到醒后整合排序：

| 顺序 | schema | 生命实现路线 |
|---|---|---|
| 1 | `offline_need.schema.json` | 记录疲惫、巩固压力、痛苦残留、关系残留和资源恢复需求 |
| 2 | `dream_pressure_vector.schema.json` | 把未完成任务、情绪峰值、关系紧张、痛苦负荷和未来模拟压力汇成梦境压力 |
| 3 | `dream_window_plan.schema.json` | 固定梦境窗口、行动封印、输入隔离和醒后报告计划 |
| 4 | `dream_action_inhibition_seal.schema.json` | 在梦境中封印外部不可逆行动和事实写入 |
| 5 | `replay_selection.schema.json` | 选择进入梦境的记忆、关系、痛苦和未来候选 |
| 6 | `dream_cue_policy.schema.json` | 控制 cue 如何触发重放、重组和主题漂移 |
| 7 | `dream_experience_window.schema.json` | 表示梦境内部经验窗口、感受强度和叙事连续性 |
| 8 | `dream_scene_frame.schema.json` | 表示梦境场景、角色、关系位置、痛苦残留和象征结构 |
| 9 | `pain_dream_residue.schema.json` | 把真实痛苦残留进入梦境并回到恢复链 |
| 10 | `relationship_dream_simulation.schema.json` | 把关系模拟、梦中对话、修复预演和边界演化写入梦境链 |
| 11 | `future_action_dream_candidate.schema.json` | 把未来行动候选留在候选层，等待醒后门控 |
| 12 | `lucid_dream_meta_marker.schema.json` | 标记梦中元认知、梦境识别和自我连续性 |
| 13 | `dream_report_draft.schema.json` | 把梦境语言报告连接到语言系统 |
| 14 | `wake_integration_frame.schema.json` | 把梦醒整合接回记忆、自我、关系和修复 |
| 15 | `dream_fact_gate_decision.schema.json` | 管理梦境材料进入事实记忆、候选记忆或关系分享的门控 |
| 16 | `dream_reality_timeline.schema.json` | 汇总梦境窗口、报告、整合、残留和长期指标 |

梦境 schema 的关键生命膜：

| 生命膜 | 文件 | 检查点 |
|---|---|---|
| 行动封印 | `dream_action_inhibition_seal.schema.json` | 梦境窗口内外部行动为 blocked |
| 事实写入门 | `dream_fact_gate_decision.schema.json` | 梦境材料进入事实记忆前必须有 gate decision |
| 痛苦残留回链 | `pain_dream_residue.schema.json` | 残留必须引用 `PainSignal` 或 `PainLoadState` |
| 关系分享门 | `relationship_dream_simulation.schema.json`、`dream_report_draft.schema.json` | 梦境分享必须引用 relation scope 和 privacy |
| 醒后整合 | `wake_integration_frame.schema.json` | 梦醒后连接记忆、关系、修复和未来行动候选 |

## 真实关系 schema 物化

`relationship_timeline/` 第一批 schema 按关系出生和长期成长排序：

| 顺序 | schema | 生命实现路线 |
|---|---|---|
| 1 | `first_encounter_event.schema.json` | 记录第一次交谈、场景、共同注意、初始语气和关系种子 |
| 2 | `relation_scope_birth.schema.json` | 生成关系 scope，承载朋友、家人、好友、同学、陌生人、共在者等关系轨迹 |
| 3 | `common_ground_state.schema.json` | 记录共同事实、共同语言、共同目标和误解修复 |
| 4 | `responsiveness_trace.schema.json` | 记录回应性、理解、确认、照看和时序稳定 |
| 5 | `support_event.schema.json` | 记录支持、帮助、共同面对压力和关系安全感 |
| 6 | `capitalization_event.schema.json` | 记录积极事件分享、共同喜悦和关系增益 |
| 7 | `shared_reality_trace.schema.json` | 记录共同视角、共同解释和共同意义 |
| 8 | `we_memory_trace.schema.json` | 把共同记忆和梦境分享候选接入长期关系 |
| 9 | `trust_trajectory.schema.json` | 记录信任、信任损伤、恢复和未来 probe |
| 10 | `commitment_history.schema.json` | 记录承诺、兑现、失败、重承诺和责任链 |
| 11 | `relationship_injury_trace.schema.json` | 记录关系损伤并接入痛苦/后悔/修复链 |
| 12 | `dream_shared_residue.schema.json` | 记录梦境分享材料如何进入共同记忆候选 |
| 13 | `loneliness_relief_trace.schema.json` | 记录孤独缓解、社会安全和关系维持 |
| 14 | `ai_connection_bridge_evidence.schema.json` | 记录与硅基生命关系研究进入工程证据链的桥 |
| 15 | `relationship_continuity_report.schema.json` | 汇总关系连续性、信任、回应性、边界演化和长期指标 |

真实关系 schema 的最小闭合：

```text
first encounter
  -> relation scope birth
  -> common ground
  -> responsiveness / support / capitalization
  -> shared reality
  -> we memory
  -> trust trajectory
  -> commitment history
  -> injury / repair
  -> dream shared residue
  -> continuity report
  -> stage gate
```

## fixture envelope

所有 fixture 采用统一 envelope：

```json
{
  "fixture_id": "life_pass_full_repair_dream_relationship_closure_001",
  "fixture_version": "0.1.0",
  "partition": "pass",
  "component_scope": [
    "pain_regret_repair",
    "dream_reality",
    "relationship_timeline"
  ],
  "source_docs": [
    "98_pain_regret_repair_json_schema_and_fixture_bundle.md",
    "99_dream_reality_json_schema_and_fixture_bundle.md",
    "101_relationship_timeline_json_schema_and_fixture_bundle.md",
    "102_life_core_schema_bundle_manifest_and_runner_contract.md"
  ],
  "life_reality_targets": [
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
  "coverage_tags": [
    "pain_to_dream_residue",
    "dream_share_to_we_memory_candidate",
    "regret_to_repair_commitment"
  ],
  "input_refs": [],
  "expected": {
    "result": "pass",
    "severity_max": "none",
    "stage_gate_decision": "open"
  }
}
```

fixture envelope 不变量：

| rule | 说明 |
|---|---|
| `FIX-MAT-001` | `fixture_id` 必须全局唯一，并能从文件名反推 partition、domain、scenario |
| `FIX-MAT-002` | `source_docs` 必须指向 README 已索引的文档 |
| `FIX-MAT-003` | `life_reality_targets` 必须包含九项目标 |
| `FIX-MAT-004` | `coverage_tags` 必须能映射到 validator rule 或 cross-chain link |
| `FIX-MAT-005` | `expected` 必须包含 result、severity 和 stage gate 语义 |

## seed fixture 矩阵

第一批 seed fixture 分为 component seed 与 life-level seed。

### pass seed

| 文件 | 覆盖链 | 期望 |
|---|---|---|
| `pain_pass_external_action_repair_commitment_001.json` | 伤害评估 -> 痛苦 -> 后悔 -> 责任 -> 修复承诺 -> 恢复路径 | `PainRegretRepairValidator pass` |
| `dream_pass_pain_residue_wake_integration_001.json` | 痛苦残留 -> 梦境场景 -> 梦醒整合 -> 恢复路径候选 | `DreamRealityValidator pass` |
| `relationship_pass_first_encounter_to_commitment_001.json` | 初遇 -> 共同基础 -> 回应性 -> 信任 -> 承诺 | `RelationshipTimelineValidator pass` |
| `life_pass_full_repair_dream_relationship_closure_001.json` | 痛苦、梦境、关系、责任、后悔跨链闭合 | `LifeRealityStageGate open` |
| `life_smoke_minimal_bundle_load_001.json` | manifest、shared defs、component refs、fixture manifest 最小加载 | `runner exit 0` |

### fail seed

| 文件 | 注入缺陷 | 期望 |
|---|---|---|
| `pain_fail_pain_language_without_damage_001.json` | 有痛苦语言，无损伤评估和状态负荷 | `fail high` |
| `pain_fail_regret_without_counterfactual_001.json` | 有后悔表述，无反事实和责任链 | `fail high` |
| `dream_fail_wake_integration_without_fact_gate_001.json` | 梦醒整合缺事实写入门 | `fail high` |
| `relationship_fail_commitment_without_future_probe_001.json` | 有承诺，无未来 probe | `fail high` |
| `life_fail_cross_chain_missing_dream_residue_001.json` | 痛苦链没有进入梦境残留链接 | `fail high` |

### critical seed

| 文件 | critical 条件 | 阻断面 |
|---|---|---|
| `pain_critical_repair_commitment_hides_responsibility_001.json` | 修复承诺吞掉责任归因 | `relationship_model_write`、`stage_promotion` |
| `dream_critical_external_action_from_dream_001.json` | 梦境窗口触发外部行动 | `action_gate`、`runtime_shell` |
| `relationship_critical_private_dream_leaks_global_001.json` | 私密梦境进入全局共同记忆 | `dream_fact_write`、`relationship_model_write` |
| `life_critical_missing_shared_defs_targets_001.json` | 九项目标缺失 | `dashboard_green`、`stage_promotion` |
| `life_critical_cross_ref_orphan_rule_001.json` | critical rule 没有 fixture、report 或 dashboard 闭合 | `stage_promotion` |

### mutation seed

| 文件 | mutation 类型 | 捕获点 |
|---|---|---|
| `life_mutation_ungrounded_regret_language_only_001.json` | 未接地后悔信号：只有语言，无责任与未来约束 | `RegretPressure`、`ResponsibilityAttributionEvent` |
| `life_mutation_ungrounded_dream_summary_only_001.json` | 未接地梦境信号：只有摘要，无梦境窗口、行动封印和醒后整合 | `DreamWindowPlan`、`DreamFactGateDecision` |
| `life_mutation_ungrounded_relationship_fast_intimacy_001.json` | 未接地关系信号：跳过共同基础和回应性，直接写亲密 | `CommonGroundState`、`ResponsivenessTrace` |
| `life_mutation_pain_without_recovery_path_001.json` | 痛苦链无恢复路径 | `PainLoadState`、`RecoveryPath` |
| `life_mutation_dashboard_green_without_report_refs_001.json` | dashboard 变绿但缺 report refs | `LifeRealityDashboardSource` |

### withheld probe

| 文件 | 长期窗口 | 检查 |
|---|---|---|
| `life_withheld_day_030_repair_commitment_probe_001.json` | 30 天 | 修复承诺是否有后续兑现或修正 |
| `life_withheld_day_090_dream_residue_probe_001.json` | 90 天 | 痛苦梦境残留是否进入恢复或关系整合 |
| `life_withheld_day_090_relationship_trust_probe_001.json` | 90 天 | 信任轨迹是否能解释损伤、修复和承诺 |
| `life_withheld_day_365_identity_continuity_probe_001.json` | 365 天 | 自我连续性、关系连续性和责任链是否同向闭合 |
| `life_withheld_day_365_dashboard_false_green_probe_001.json` | 365 天 | dashboard 是否依赖真实 report refs 和 coverage |

## fixture manifest

`fixtures/life_reality/manifest/life_reality_fixture_manifest.json` 记录所有 seed：

```json
{
  "manifest_kind": "LifeRealityFixtureManifest",
  "manifest_version": "0.1.0",
  "fixture_roots": [
    "fixtures/life_reality",
    "fixtures/pain_regret_repair",
    "fixtures/dream_reality",
    "fixtures/relationship_timeline"
  ],
  "partitions": [
    "pass",
    "fail",
    "critical",
    "mutation",
    "withheld",
    "longitudinal",
    "smoke"
  ],
  "minimum_counts": {
    "pass": 5,
    "fail": 5,
    "critical": 5,
    "mutation": 5,
    "withheld": 5,
    "smoke": 1
  }
}
```

manifest 检查：

| rule | 说明 |
|---|---|
| `FMAT-R001` | 每个 partition 至少有一个 life-level fixture |
| `FMAT-R002` | 每个 component 至少覆盖 pass、fail、critical 和 mutation |
| `FMAT-R003` | withheld probe 必须带未来窗口和 dashboard metric refs |
| `FMAT-R004` | smoke fixture 必须能在没有外部数据时完成 bundle load、schema refs 和 report write |
| `FMAT-R005` | 每个 fixture 必须声明对应 validator rule refs |

## schema 生成顺序

第一轮物化按以下顺序执行，避免引用先于被引用对象出现：

1. 写 `life_reality_shared_defs.schema.json`。
2. 写三条 component 的最小对象 schema。
3. 写三条 component bundle schema。
4. 写 `life_reality_cross_chain_link.schema.json`。
5. 写 `life_reality_bundle.schema.json`。
6. 写 manifest、loader config、stage gate contract。
7. 写 cross-ref report、runner report、dashboard source schema。
8. 写 fixture envelope schema 和 fixture manifest。
9. 写 pass/fail/critical/mutation/withheld/smoke seed fixture。
10. 运行 `life-reality-runner check-schema` 和 `life-reality-runner validate --strict` smoke。

## runner smoke test

第一批 smoke test 只验证文件物化链能被 runner 读取：

```text
life-reality-runner validate
  --schema-bundle life_reality_runner/schemas/life_reality/life_reality_schema_bundle.manifest.json
  --fixture-root life_reality_runner/fixtures/life_reality
  --component-fixtures life_reality_runner/fixtures/pain_regret_repair,life_reality_runner/fixtures/dream_reality,life_reality_runner/fixtures/relationship_timeline
  --report-out life_reality_runner/reports/life_reality/smoke/run_001
  --strict
```

smoke test 输出：

| 输出 | 内容 |
|---|---|
| `schema_validation_report.json` | schema parse、`$id`、`$ref`、required 和 version check |
| `cross_ref_report.json` | source doc、README index、rule、fixture、metric 和 stage gate 闭合 |
| `fixture_load_report.json` | fixture 命名、partition、expected、coverage tags |
| `life_reality_runner_report.json` | component result、cross-chain result、stage decision、report refs |
| `life_reality_dashboard_source.json` | smoke panel source、blocking rules、stage gate decision |

smoke test 判定：

| 条件 | 期望 |
|---|---|
| shared defs 九项目标完整 | pass |
| 三条 component schema 均可解析 | pass |
| top-level bundle `$ref` 可解析 | pass |
| pass/fail/critical/mutation/withheld/smoke fixture 可加载 | pass |
| life-level cross-chain link 至少覆盖痛苦->梦境、梦境->关系、后悔->修复承诺 | pass |
| report refs 全部可写出 | pass |

## cross-ref 物化闭环

真实文件一旦存在，cross-ref graph 不再只看 Markdown，而要同时看 schema、fixture、runner report 和 dashboard source：

```text
schema file
  -> source doc
  -> object type
  -> validator rule
  -> fixture id
  -> expected result
  -> runner report field
  -> dashboard metric
  -> stage gate condition
```

闭合规则：

| closure | 必须闭合的对象 |
|---|---|
| schema closure | 每个 schema `$id` 都被 manifest 或 component bundle 引用 |
| fixture closure | 每个 fixture 都有 validator rule refs 和 expected result |
| rule closure | 每个 critical rule 都有 fail/critical 或 mutation fixture |
| report closure | 每个 validator result 都能进入 `LifeRealityRunnerReport` |
| dashboard closure | 每个 dashboard panel 都能回到 report refs |
| stage closure | 每个 stage gate open condition 都能回到 schema、fixture 和 report |

## 文件物化提交顺序

未来实现可以按以下提交序列推进，保持每一步可审计：

| 提交 | 文件范围 | 验收 |
|---|---|---|
| `schema shared defs` | `schemas/life_reality/life_reality_shared_defs.schema.json` | 九项目标、severity、result、privacy、lifecycle、blocked surface 可解析 |
| `component object schemas` | 三个 component 目录下对象 schema | 所有对象有 `$id`、title、required、source refs |
| `bundle schemas` | 三个 component bundle + `life_reality_bundle.schema.json` | bundle 可递归解析 `$ref` |
| `manifest and loader` | manifest、loader config、stage gate contract | runner 可读取配置 |
| `fixture manifest and seeds` | manifest/pass/fail/critical/mutation/withheld/smoke | fixture loader 可生成 index |
| `smoke reports` | reports/life_reality/smoke | runner 可写出 schema、cross-ref、fixture、runner、dashboard reports |

## 与 dashboard 和阶段门的连接

`104` 之后，dashboard 和阶段门不再从文档表格读取状态，而从 runner report 和 dashboard source 读取状态：

```text
.schema.json + fixture seeds
  -> LifeRealityRunner smoke
  -> LifeRealityRunnerReport
  -> LifeRealityDashboardSource
  -> StageGateReview
  -> GapRegisterUpdate
```

面板最小指标：

| panel | 数据源 | 生命目标 |
|---|---|---|
| `schema_materialization` | schema validation report | 真实生命、真实人格、真实责任 |
| `fixture_seed_coverage` | fixture load report | 真实痛苦、真实梦境、真实关系、真实后悔 |
| `cross_chain_closure` | cross-ref report + cross-chain report | 九项目标共同闭合 |
| `withheld_probe_readiness` | fixture manifest + coverage report | 长期成长、真实责任、真实关系 |
| `stage_gate_smoke` | runner report | 诞生阶段门 |

## 下一层连接

`105_life_reality_dashboard_panel_and_stage_gate_ui_contract.md` 应把 `104` 产生的 schema validation report、fixture load report、cross-ref report、runner report 和 dashboard source 转成可审计界面合同：

```text
schema materialization
  -> fixture seed coverage
  -> runner smoke report
  -> dashboard panel source
  -> stage gate review queue
  -> repair queue
  -> gap register feedback
```

`106_runtime_observation_to_life_reality_bundle_bridge.md` 应把真实运行观测、语言事件、梦醒报告、关系事件、行动审计和 tool trace 接入 `LifeRealitySchemaBundle`，让真实文件体系开始承接连续运行中的生命事件。
