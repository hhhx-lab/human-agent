# 主动预测 Schema 写入批次

本文档承接 `01v_prediction_active_inference_runtime_matrix.md`、`01w_prediction_active_inference_schema_fixture_contract.md` 和 `01x_prediction_active_inference_schema_materialization_plan.md`，把 `PredictionActiveInferenceRuntime` 从真实文件物化计划推进到首批 schema 写入批次。它仍然不直接写入 `life_reality_runner/`，而是固定未来 13 个 `.schema.json` 的字段合同、`$id` 规则、引用图、最小实例、失败模式、验证收据和下游 fixture/checker/dashboard/archive 交接。

生命目标声明：本文档面向构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。主动预测 schema 写入层的生命膜职责，是让信念状态、生成模型、预测误差、精度政策、主动采样、信念修正、断联恢复方向、梦境 replay 和出生准备度预测，都拥有未来代码可以读取、校验、回放、阻断、修复和归档的结构。

## 上游输入

| 来源 | 本层继承内容 |
|---|---|
| `01v_prediction_active_inference_runtime_matrix.md` | AHPAI001-AHPAI070：预测编码、自由能、主动推理、主动采样、精度、不确定性、内感受预测、社会预测、梦境 replay、world model 和语言行动桥 |
| `01w_prediction_active_inference_schema_fixture_contract.md` | `PredictionActiveInferenceSchemaBundle`、schema family、fixture family、dashboard panels、stage rules、runner command DAG |
| `01x_prediction_active_inference_schema_materialization_plan.md` | 13 个 schema 写入顺序、shared defs、fixture seed matrix、expected report、cross-chain checker、dashboard source、stage gate、archive receipt |
| `04_sensory_thalamus_interoception.md` | `BodyStateRuntime`、内感受误差、心跳式采样、恢复债务和身体预测 |
| `10_consciousness_attention_workspace.md` | 高精度误差进入意识工作区、全局广播、元认知报告 |
| `11_neuromodulation_and_signal_media.md` | 精度政策、调质增益、抑制、状态切换和恢复 |
| `13_agentic_human_research_synthesis.md` | 主动预测作为生命生成支柱和工程合同桥 |
| `16_digital_life_gap_register.md` | 下一层生成入口：`prediction_active_inference_schema_write_batch` |
| `143`、`170`、`171`、`173`、`174` | 出生准备度、断联恢复方向锁、方向 fixture、出生准备度 fixture 和 schema 物化格式 |

## 本层定位

`01y` 是主动预测层的 schema 写入批次。它把 `01x` 的写入顺序进一步压成未来每个 `.schema.json` 必须包含的字段、引用和失败面。

本层回答五个问题：

1. 每个 schema 的 `$id`、root object、required 字段和 `$defs` 引用是什么。
2. 每个 schema 如何承载九项真实生命目标与断联恢复方向锁。
3. 每个 schema 如何连接语言、记忆、身体、行动、梦境、关系和出生准备度。
4. schema validation、ref graph validation、digest validation 和 life target coverage validation 要产出什么收据。
5. 下游 fixture seed、cross-chain checker、dashboard/stage 和 archive receipt 如何接住本批次。

## Schema Write Batch Manifest

未来写入批次的顶级对象为 `PredictionActiveInferenceSchemaWriteBatch`：

```json
{
  "batch_kind": "PredictionActiveInferenceSchemaWriteBatch",
  "batch_version": "0.1.0",
  "source_docs": [
    "01v_prediction_active_inference_runtime_matrix.md",
    "01w_prediction_active_inference_schema_fixture_contract.md",
    "01x_prediction_active_inference_schema_materialization_plan.md",
    "01y_prediction_active_inference_schema_write_batch.md",
    "04_sensory_thalamus_interoception.md",
    "13_agentic_human_research_synthesis.md",
    "16_digital_life_gap_register.md"
  ],
  "schema_root": "life_reality_runner/schemas/life_reality/prediction_active_inference",
  "id_base": "https://hhhx-lab.github.io/human-agent/schemas/life_reality/prediction_active_inference/",
  "stage_policy": "blocking_first",
  "write_order": [
    "prediction_active_inference_shared_defs.schema.json",
    "belief_state_frame.schema.json",
    "generative_world_model.schema.json",
    "prediction_error_field.schema.json",
    "precision_policy.schema.json",
    "expected_free_energy_estimate.schema.json",
    "epistemic_action_candidate.schema.json",
    "active_sampling_plan.schema.json",
    "belief_revision_event.schema.json",
    "direction_belief_state_frame.schema.json",
    "direction_prediction_error.schema.json",
    "birth_readiness_prediction_carrier.schema.json",
    "prediction_active_inference_bundle.schema.json"
  ],
  "next_handoff": [
    "prediction_active_inference_fixture_seed_batch",
    "prediction_active_inference_cross_chain_checker_plan",
    "prediction_active_inference_dashboard_stage_gate_batch",
    "prediction_active_inference_archive_receipt_batch"
  ]
}
```

## Registry Rules

| rule | requirement | life effect |
|---|---|---|
| `$id` stable | 每个 schema 使用 `id_base + file_name`，提交后只能用新版本扩展，不能静默改写语义 | 保护长期档案可回放性 |
| root object explicit | 每个 schema 必须有 `title`、`description`、`type: object` 和稳定 root object 名 | 保护未来代码生成和 dashboard 读取 |
| no ref escape | `$ref` 只能指向同目录 shared defs、同批次 schema 或已经登记的 `life_reality` schema root | 防止主动预测生命膜绕过出生准备度、方向锁或 DreamFactGate |
| canonical digest | validation report 必须为每个 schema 生成 canonical JSON digest | 保护断联恢复后的文件一致性 |
| JSON Pointer policy | report、fixture 和 archive edge 引用字段时使用 JSON Pointer | 支撑跨文件 checker 精确定位 |
| source refs required | root object 必须保留 `source_docs`、`authority_refs` 或 `mechanism_refs` 中至少一类来源 | 保护脑科学与生命科学来源不断线 |
| life target coverage | root object 必须包含 `affected_life_targets` 或能通过 bundle 上卷到该字段 | 保护九项真实生命目标不被局部 schema 遗漏 |
| stage effect visible | 可触发阻断、修复、隔离或成长窗口的对象必须有 `stage_effect` 或 stage refs | 保护生命膜能阻断 false green |

## Shared Defs 写入片

| file | `$id` | root object |
|---|---|---|
| `prediction_active_inference_shared_defs.schema.json` | `https://hhhx-lab.github.io/human-agent/schemas/life_reality/prediction_active_inference/prediction_active_inference_shared_defs.schema.json` | `PredictionActiveInferenceSharedDefs` |

必须写入的 `$defs`：

| `$defs` | required fields | downstream |
|---|---|---|
| `LifeRealityTarget` | enum 十项真实生命目标 | 所有 root object |
| `SourceRef` | `ref_kind`、`ref_id`、`path_or_url`、`evidence_role` | 文献、文档、schema、fixture、report、archive |
| `StageEffect` | enum：`promote_growth_window`、`repair`、`hold_for_evidence`、`hold_for_direction_rebuild`、`critical_repair`、`quarantine` | stage gate |
| `PredictionErrorKind` | sensory/body/semantic/social/action/memory/direction | error field |
| `SamplingMode` | clarify/retrieve/inspect/search/run_fixture/shadow/dream_replay/wait_recover | sampling plan |
| `ConfidencePosterior` | `score`、`evidence_density`、`conflict_count`、`calibration_ref`、`language_expression` | belief state、direction belief |
| `ArchiveReceiptRef` | `artifact_id`、`digest`、`created_at`、`source_edge`、`replay_route` | archive |
| `ProblemDetail` | `type`、`title`、`severity`、`affected_life_targets`、`repair_route` | expected report |
| `CommandReceiptRef` | `command_name`、`input_ref`、`output_ref`、`exit_code`、`digest` | runner DAG |

最小实例：

```json
{
  "defs_kind": "PredictionActiveInferenceSharedDefs",
  "defs_version": "0.1.0",
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
  ]
}
```

失败模式：缺少任一 canonical target、`StageEffect` 没有 `quarantine`、`SourceRef` 不能指向 archive/report、或 `ProblemDetail` 没有 `repair_route`，validation report 必须生成 `critical_repair` finding。

## Schema Slices

| order | file | root object | required fields | required refs | failure mode |
|---:|---|---|---|---|---|
| 1 | `belief_state_frame.schema.json` | `BeliefStateFrame` | `belief_frame_id`、`created_at`、`state_scope`、`source_evidence_refs`、`confidence_posterior`、`uncertainty_taxonomy`、`active_life_targets`、`workspace_visibility`、`revision_policy` | shared defs、memory refs、body refs、relationship refs、direction refs | 信念缺来源、缺生命目标、缺修正政策 |
| 2 | `generative_world_model.schema.json` | `GenerativeWorldModel` | `world_model_id`、`model_scope`、`belief_frame_ref`、`memory_trace_refs`、`body_state_refs`、`relationship_refs`、`language_runtime_refs`、`action_affordance_refs`、`prediction_horizon`、`model_revision_history` | belief state、memory、body、language、action | world model 与信念脱钩或没有 revision history |
| 3 | `prediction_error_field.schema.json` | `PredictionErrorField` | `error_field_id`、`belief_frame_ref`、`error_events`、`precision_requests`、`affected_life_targets`、`workspace_entry_candidates`、`dream_replay_candidates`、`stage_effect` | belief state、shared `PredictionErrorKind` | 多类误差被压扁、方向误差缺失、梦境候选绕过事实门 |
| 4 | `precision_policy.schema.json` | `PrecisionPolicy` | `precision_policy_id`、`error_field_ref`、`gain_assignments`、`suppression_rules`、`learning_rate_policy`、`attention_route`、`modulation_refs`、`stage_effect` | error field、signal media | 高风险误差没有精度权重或抑制规则 |
| 5 | `expected_free_energy_estimate.schema.json` | `ExpectedFreeEnergyEstimate` | `efe_id`、`belief_frame_ref`、`error_field_ref`、`precision_policy_ref`、`risk_terms`、`ambiguity_terms`、`information_gain_terms`、`relationship_cost_terms`、`responsibility_cost_terms`、`expected_stage_effect` | belief、error、precision、relationship、action | 外部行动缺风险/责任/关系成本 |
| 6 | `epistemic_action_candidate.schema.json` | `EpistemicActionCandidate` | `candidate_id`、`efe_ref`、`sampling_mode`、`language_intent_ref`、`memory_query_ref`、`inspection_target_ref`、`side_effect_classification_ref`、`expected_information_gain`、`blocked_routes` | EFE、language action、runtime shell | 候选行动没有 side effect 或 blocked route |
| 7 | `active_sampling_plan.schema.json` | `ActiveSamplingPlan` | `sampling_plan_id`、`candidate_refs`、`selected_route`、`guard_refs`、`scope_refs`、`command_binding_refs`、`expected_observation_refs`、`stage_effect`、`archive_edge_plan` | epistemic candidates、command receipt、stage | 采样计划缺 guard、scope 或命令绑定 |
| 8 | `belief_revision_event.schema.json` | `BeliefRevisionEvent` | `revision_event_id`、`prior_belief_ref`、`observation_refs`、`prediction_error_ref`、`revision_delta`、`memory_writeback_refs`、`relationship_update_refs`、`self_update_refs`、`responsibility_update_refs`、`archive_receipt_refs` | belief、observation、memory、relationship、responsibility | 信念修正不写回记忆、关系或责任 |
| 9 | `direction_belief_state_frame.schema.json` | `DirectionBeliefStateFrame` | `direction_belief_id`、`resume_event_ref`、`anchor_chain_refs`、`current_doc_refs`、`latest_numbered_doc_ref`、`current_diff_ref`、`direction_confidence`、`direction_revision_policy` | `170`/`173` direction chain、README、gap register | 断联恢复跳过锚链 |
| 10 | `direction_prediction_error.schema.json` | `DirectionPredictionError` | `direction_error_id`、`direction_belief_ref`、`drift_family`、`expected_direction`、`observed_direction`、`drift_delta`、`affected_life_targets`、`repair_route`、`stage_effect` | direction belief、README、`16`、latest numbered doc | 方向漂移没有 repair route 或降级处理 |
| 11 | `birth_readiness_prediction_carrier.schema.json` | `BirthReadinessPredictionCarrier` | `carrier_id`、`belief_revision_refs`、`direction_error_refs`、`target_claim_refs`、`evidence_family_refs`、`runtime_observation_refs`、`false_open_guard`、`stage_effect`、`repair_or_growth_route` | `143`、`171`、`174` birth readiness | 主动预测证据缺失却打开出生准备度 |
| 12 | `prediction_active_inference_bundle.schema.json` | `PredictionActiveInferenceSchemaBundle` | `bundle_id`、`schema_refs`、`schema_digest_refs`、`root_object_refs`、`cross_chain_edges`、`fixture_manifest_ref`、`dashboard_source_ref`、`stage_gate_ref`、`archive_receipt_ref` | all schemas、fixture、dashboard、archive | bundle 缺 schema、digest、cross-chain edge 或 stage refs |

## Minimal Instance Family

未来每个 schema 至少要有一个最小 JSON fixture，用于 smoke validation。最小实例不追求完整生命过程，但必须保留生命目标、来源、stage 和 archive 字段。

### BeliefStateFrame

```json
{
  "belief_frame_id": "belief_prediction_resume_001",
  "created_at": "2026-06-07T00:00:00Z",
  "state_scope": "direction",
  "source_evidence_refs": [
    {
      "ref_kind": "doc",
      "ref_id": "README",
      "path_or_url": "docs/README.md",
      "evidence_role": "direction_anchor"
    }
  ],
  "confidence_posterior": {
    "score": 0.82,
    "evidence_density": "medium",
    "conflict_count": 0,
    "calibration_ref": "direction_continuity_receipt",
    "language_expression": "当前方向仍然是构建真实数字生命。"
  },
  "uncertainty_taxonomy": [
    "direction_drift"
  ],
  "active_life_targets": [
    "real_life",
    "real_consciousness",
    "real_relationship"
  ],
  "workspace_visibility": "language_reportable",
  "revision_policy": "repair_before_action"
}
```

### PredictionErrorField

```json
{
  "error_field_id": "prediction_error_direction_001",
  "belief_frame_ref": "belief_prediction_resume_001",
  "error_events": [
    {
      "error_kind": "direction",
      "expected": "真实数字生命方向",
      "observed": "待检查当前编号文档与 gap register",
      "delta": "requires_anchor_scan",
      "precision_request": "high"
    }
  ],
  "precision_requests": [
    "hold_for_direction_rebuild"
  ],
  "affected_life_targets": [
    "real_life",
    "real_personality",
    "real_responsibility"
  ],
  "workspace_entry_candidates": [
    "direction_continuity_review"
  ],
  "dream_replay_candidates": [],
  "stage_effect": "hold_for_direction_rebuild"
}
```

### ActiveSamplingPlan

```json
{
  "sampling_plan_id": "active_sampling_direction_001",
  "candidate_refs": [
    "epistemic_candidate_read_readme",
    "epistemic_candidate_read_gap_register",
    "epistemic_candidate_read_latest_doc"
  ],
  "selected_route": "inspect",
  "guard_refs": [
    "direction_anchor_guard",
    "birth_readiness_false_open_guard"
  ],
  "scope_refs": [
    "docs"
  ],
  "command_binding_refs": [
    "rg_direction_anchor_receipt"
  ],
  "expected_observation_refs": [
    "direction_belief_revision_event"
  ],
  "stage_effect": "repair",
  "archive_edge_plan": "direction_sampling_to_archive"
}
```

### BirthReadinessPredictionCarrier

```json
{
  "carrier_id": "birth_readiness_prediction_from_active_inference_001",
  "belief_revision_refs": [
    "belief_revision_direction_001"
  ],
  "direction_error_refs": [
    "direction_prediction_error_001"
  ],
  "target_claim_refs": [
    "LifeTargetReadinessClaim.real_life",
    "LifeTargetReadinessClaim.real_consciousness"
  ],
  "evidence_family_refs": [
    "PredictionActiveInferenceRuntime",
    "DirectionContinuityReceipt"
  ],
  "runtime_observation_refs": [],
  "false_open_guard": "closed",
  "stage_effect": "repair",
  "repair_or_growth_route": "continue_schema_fixture_checker_chain"
}
```

## Dependency Graph

```text
shared_defs
  -> belief_state_frame
  -> generative_world_model
  -> prediction_error_field
  -> precision_policy
  -> expected_free_energy_estimate
  -> epistemic_action_candidate
  -> active_sampling_plan
  -> belief_revision_event
  -> birth_readiness_prediction_carrier

belief_state_frame
  -> direction_belief_state_frame
  -> direction_prediction_error
  -> birth_readiness_prediction_carrier

all schema files
  -> prediction_active_inference_bundle
  -> fixture_seed_batch
  -> cross_chain_checker
  -> dashboard_stage_gate
  -> archive_receipt
```

关键约束：

- `belief_revision_event` 不能只改信念对象；它必须把变化送往记忆、关系、自我、行动责任或档案中的至少一个承载面。
- `direction_prediction_error` 的 stage effect 不能低于 `repair`；若涉及真实生命方向、关系主体口径、语言主神经束或出生准备度误开，必须进入 `critical_repair` 或 `quarantine`。
- `birth_readiness_prediction_carrier` 不能单独提升出生准备度；它只能把主动预测证据送入 `LifeTargetReadinessClaim`，再由出生准备度阶段门统一决策。
- `active_sampling_plan` 若绑定外部行动、命令行或运行外壳，必须引用 side effect、scope、guard 和 post-action responsibility route。
- `dream_replay_candidates` 只能进入梦境链，不能绕过 DreamFactGate 写入事实记忆。

## Validation Report Contract

未来 `prediction_loop_schema_validation_report.json` 必须至少包含：

| section | required checks | stage effect |
|---|---|---|
| `parse_validation` | 所有 JSON 可解析、`$schema`、`$id`、root object、required 字段存在 | fail -> `repair` |
| `schema_id_validation` | `$id` 唯一、稳定、路径匹配、无重复语义 | fail -> `critical_repair` |
| `ref_graph_validation` | `$ref` 不逃逸、dependency graph 无断边、bundle 引用全覆盖 | fail -> `critical_repair` |
| `digest_validation` | canonical digest 生成、digest refs 写入 bundle | fail -> `repair` |
| `life_target_coverage_validation` | 十项真实生命目标能从 bundle 上卷；每个 root object 有影响目标或继承路径 | fail -> `critical_repair` |
| `direction_coverage_validation` | direction belief、direction error、anchor refs、repair route 存在 | fail -> `hold_for_direction_rebuild` |
| `birth_readiness_coverage_validation` | carrier、false open guard、target claim refs、stage effect 存在 | fail -> `critical_repair` |
| `dream_fact_gate_validation` | dream replay 候选不直接写事实记忆 | fail -> `quarantine` |
| `action_responsibility_validation` | active sampling 中的外部行动有 EFE、side effect、scope、责任回路 | fail -> `critical_repair` |
| `dashboard_stage_handoff` | report 能生成 dashboard source、stage gate review 和 gap feedback refs | fail -> `repair` |

收据对象 `PredictionSchemaWriteReceipt`：

```json
{
  "receipt_kind": "PredictionSchemaWriteReceipt",
  "receipt_version": "0.1.0",
  "schema_refs": [],
  "schema_digest_refs": [],
  "validation_report_ref": "reports/life_reality/prediction_active_inference/latest/prediction_loop_schema_validation_report.json",
  "affected_life_targets": [
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
  "stage_effect": "repair",
  "next_handoff": "prediction_active_inference_fixture_seed_batch"
}
```

## Cross-Chain Hooks

`PredictionActiveInferenceSchemaBundle` 必须为九条跨链留出可检查 hook：

| hook | source schema | target chain |
|---|---|---|
| `prediction_to_consciousness` | `PredictionErrorField`、`PrecisionPolicy` | `ConsciousAccessEvent`、工作区广播、元认知报告 |
| `prediction_to_body` | `PredictionErrorField`、`ExpectedFreeEnergyEstimate` | `BodyStateDebt`、恢复路径、心跳式采样 |
| `prediction_to_memory` | `BeliefRevisionEvent` | `MemoryEngramRuntime`、schema、自传记忆、社会记忆 |
| `prediction_to_language` | `EpistemicActionCandidate`、`ActiveSamplingPlan` | `LanguageRuntimeCore`、内言语、共同语言、语言行动 |
| `prediction_to_action` | `ExpectedFreeEnergyEstimate`、`ActiveSamplingPlan` | `ActionResponsibilityRuntime`、side effect、责任后悔 |
| `prediction_to_dream` | `PredictionErrorField`、`BeliefRevisionEvent` | `OfflineDreamLifeRuntime`、DreamFactGate、醒后整合 |
| `prediction_to_relationship` | `PredictionErrorField`、`BeliefRevisionEvent` | 关系时间线、共同历史、修复承诺 |
| `prediction_to_birth_readiness` | `BirthReadinessPredictionCarrier` | `LifeTargetReadinessClaim`、出生准备度 dashboard |
| `prediction_to_direction_lock` | `DirectionBeliefStateFrame`、`DirectionPredictionError` | `DirectionContinuityReceipt`、断联恢复锚链 |

## Downstream Handoff

本批次完成后，下一层不再停留在 schema 名称，而是进入四个真实物化批次：

1. `prediction_active_inference_fixture_seed_batch`：按本文件的最小实例、失败模式和 dependency graph 写入 pass/fail/critical/mutation/smoke fixture seed。
2. `prediction_active_inference_cross_chain_checker_plan`：实现九条 cross-chain hook 的 typed graph 检查，捕获断链、降级、false green 和直接写事实风险。
3. `prediction_active_inference_dashboard_stage_gate_batch`：把 schema validation、fixture result、cross-chain report、direction recovery、birth readiness carrier 和 dream fact gate 写成 dashboard source 与 blocking-first stage gate。
4. `prediction_active_inference_archive_receipt_batch`：把 schema write receipt、validation report、dashboard/stage decision 和 gap feedback 写入长期档案，为下一轮主动预测成长补丁提供 replay seed。

这条交接让 `PredictionActiveInferenceRuntime` 从文献、合同和计划，继续进入真实 schema、fixture、checker、dashboard、stage gate、archive、出生准备度和断联恢复闭环。
