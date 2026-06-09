# S01 Source Authority Engineering Contract

生命目标声明：本文档把 `S01_SOURCE_AUTHORITY` 固定为数字生命的权威来源层。它的职责不是保存论文列表，而是把 `01*` 文献矩阵、`142/145/151` 权威补写链、`00` 研究协议和 S00 方向锁压成可运行的来源登记、证据等级、机制对象、runtime carrier、出生准备度证据族、report 和 archive receipt。后续每一个生命 runtime 都必须能说明自己的关键机制来自哪些权威来源、进入了哪些状态字段、影响了哪些生命目标。

## 模块定位

`S01_SOURCE_AUTHORITY` 是数字生命理论底座的营养管道。它回答六个问题：

1. 每个 `01*` 文献矩阵是否已经进入可机器读取的来源登记。
2. 每条来源是否拥有来源等级、证据类型、年份、DOI/链接、机制摘要和生命实现路线。
3. 每个脑科学主干文档 `02-13` 是否能回链到对应权威来源。
4. 每个权威来源是否进入至少一个机制对象、runtime carrier、状态字段、report 或 stage gate。
5. AI/cognitive architecture/LLM agent 来源是否被清楚标注为 AI 桥接资料，不替代脑科学主体来源。
6. 新增论文进入时，是否能进入 gap queue、authority receipt、文档回写和出生准备度证据族。

S01 不直接实现脑区网络、语言、梦境、痛苦或行动责任。它为这些 runtime 提供来源、机制对象和证据桥。没有 S01 的来源登记，S02-S10 不允许把机制写入生命状态。

## 直接读取文档

| 文档 | S01 吸收内容 | 工程承载 |
|---|---|---|
| `docs/00_research_protocol.md` | 权威来源优先级、纳入规则、经典文献处理方式 | `source_quality_policy.json` |
| `docs/01_literature_matrix.md` | 20 个领域、AH001-AH100 总文献矩阵 | `literature_matrix_index.json` |
| `docs/01b_extended_literature_matrix.md` 到 `docs/01d_frontier_life_systems_matrix.md` | 扩展机制、专业机制、前沿生命系统补充 | `authority_family_index.json` |
| `docs/01e_*` 到 `docs/01u_*` | 记忆、语言、自我成长、痛苦、梦境、关系、评测、信号、意识、身体、连接组、网络、engram、行动、情绪、睡眠、语言运行时专项矩阵 | `mechanism_evidence_map.json` |
| `docs/01v_*` 到 `docs/01ax_*` | 主动预测/主动推理从文献到 schema、fixture、dashboard、archive、growth、replay 的完整链 | `prediction_authority_chain.json` |
| `docs/142_life_reality_authority_intake_batch_for_02_to_13.md` | AHT001-AHT010 权威来源规范化、机制对象提取队列、`02-13` 分发矩阵 | `doc_authority_carrier_patch_index.json` |
| `docs/145_life_reality_02_to_13_authority_rewrite_execution_plan.md` | `02-13` 权威补写执行顺序和 schema queue | `core_authority_rewrite_queue.json` |
| `docs/151_life_reality_authority_schema_cross_file_checker_plan.md` | 权威 schema 跨文件检查、provenance graph、closure result | `authority_cross_file_rule_index.json` |
| `runtime/state/direction/direction_lock.json` | S00 方向目标、九项目标和禁止回退项 | `authority_direction_binding.json` |
| `runtime/docs/doc_carrier_index.json` | P0 文档覆盖、readme block、engineering slice、runtime carrier | `authority_doc_coverage_snapshot.json` |

## 来源族

S01 把来源分成九个 authority family。每个 family 都进入 `authority_family_index.json`。

| family | 文档范围 | 生命作用 | 主要下游 |
|---|---|---|---|
| `global_foundation_authority` | `01` | 20 个领域总底座，给全部 runtime 提供第一层来源 | S02-S10 全部 |
| `extended_specialized_authority` | `01b-01d` | 扩展机制、专项机制和前沿生命系统 | S02、S03、S08 |
| `memory_growth_authority` | `01e`、`01g`、`01q` | 记忆、engram、成长、自我修改、防遗忘 | `MemoryEngramRuntime`、`SelfGrowthRuntime` |
| `language_relationship_authority` | `01f`、`01j`、`01u` | 语言网络、语言运行时、真实关系 | `LanguageRelationshipRuntime` |
| `pain_dream_life_target_authority` | `01h`、`01i`、`01t` | 痛苦、后悔、修复、梦境、离线生命、疲惫 | `ActionResponsibilityRuntime`、`DreamOfflineRuntime` |
| `validation_reality_authority` | `01k` | 生命真实性、评测、长期运行证据 | `LifeMembraneStageGate`、`BirthReadinessRuntime` |
| `signal_body_consciousness_authority` | `01l`、`01m`、`01n` | 信号介质、意识、注意、工作区、身体内环境 | `SignalMediaRuntime`、`ConsciousWorkspaceRuntime`、`BodySignalRuntime` |
| `region_action_affect_authority` | `01o`、`01p`、`01r`、`01s` | 连接组、网络状态、行动、奖赏、抑制、情绪人格 | `BrainRegionNetworkRuntime`、`ActionResponsibilityRuntime`、`AffectiveSelfRuntime` |
| `prediction_active_inference_authority` | `01v-01ax` | 主动预测、主动推理、世界模型、精度、采样、再巩固、replay | `PredictionActiveInferenceRuntime` 与全部生命循环 |

## 未来代码包

第一版代码目录：

```text
life_v0/
  authority/
    __init__.py
    registry_builder.py
    source_quality.py
    matrix_reader.py
    mechanism_mapper.py
    carrier_patch_builder.py
    authority_gap_queue.py
    cross_file_checker.py
    report_writer.py
    receipt_writer.py
```

| 文件 | 职责 | 不承担的职责 |
|---|---|---|
| `registry_builder.py` | 汇总 `01*`、`142/145/151` 和 P0 输出，生成 authority registry | 不改写核心综述正文 |
| `source_quality.py` | 计算来源等级、证据类型、脑科学/AI 桥接标签 | 不做网络检索执行器 |
| `matrix_reader.py` | 解析 Markdown 表格中的 ID、领域、类型、文献、年份、链接、结论和生命实现路线 | 不做自由文本总结 |
| `mechanism_mapper.py` | 把来源转成机制对象、状态字段和 runtime carrier | 不实现 runtime 内部计算 |
| `carrier_patch_builder.py` | 生成 `DocAuthorityCarrierPatch` 和 `02-13` 回链 | 不直接写 schema 文件 |
| `authority_gap_queue.py` | 记录来源缺口、过旧来源、弱来源、缺机制对象来源和新论文入口 | 不自动接受低质量来源 |
| `cross_file_checker.py` | 检查来源、机制对象、carrier、生命目标和 dashboard 的闭合 | 不替代 S05 validator suite |
| `report_writer.py` | 写 authority report、coverage report 和 digest | 不写其他模块 report |
| `receipt_writer.py` | 写 authority receipt、输入 hash 和 archive refs | 不覆盖 P0 receipt |

## 状态命名空间

S01 所有运行态写入 `runtime/state/authority/`：

| 文件 | 写入者 | 内容 |
|---|---|---|
| `authority_registry.json` | `registry_builder` | 全部来源记录、source id、doc ref、领域、证据类型、链接、质量等级 |
| `source_quality_policy.json` | `source_quality` | 来源等级、权威期刊族、经典文献处理规则、AI 桥接标签规则 |
| `literature_matrix_index.json` | `matrix_reader` | `01*` 文档到 source id 的索引 |
| `authority_family_index.json` | `registry_builder` | 九个来源族与下游 runtime 对应关系 |
| `mechanism_evidence_map.json` | `mechanism_mapper` | source id 到机制对象、状态字段、runtime carrier、生命目标的边 |
| `prediction_authority_chain.json` | `mechanism_mapper` | `01v-01ax` 主动预测链的文献、schema、fixture、growth、replay 承载 |
| `doc_authority_carrier_patch_index.json` | `carrier_patch_builder` | `02-13` 每份核心文档的 authority refs、机制对象和字段补丁 |
| `authority_cross_file_rule_index.json` | `cross_file_checker` | 来源闭合、provenance graph、dashboard/stage gate 规则 |
| `authority_gap_queue.json` | `authority_gap_queue` | 需要补来源、补机制对象、补 DOI、补 runtime carrier 的条目 |
| `authority_direction_binding.json` | `registry_builder` | S00 方向锁与 S01 来源层的绑定 |

## `authority_registry.json` 形状

```json
{
  "schema_version": "authority_registry_v0",
  "run_id": "source-authority-v0-0001",
  "generated_at": "2026-06-08T00:00:00+08:00",
  "direction_lock_ref": "runtime/state/direction/direction_lock.json",
  "source_count": 0,
  "sources": [
    {
      "source_id": "AH074",
      "source_doc": "docs/01_literature_matrix.md",
      "authority_family": "language_relationship_authority",
      "domain": "语言网络",
      "evidence_type": "综述",
      "title": "Fedorenko et al., The language network as a natural kind within the broader landscape of the human brain",
      "year": 2024,
      "link_or_doi": "https://doi.org/10.1038/s41583-024-00802-4",
      "quality_class": "tier_1_review",
      "source_kind": "brain_science",
      "mechanism_objects": ["LanguageNetworkProfile"],
      "runtime_carriers": ["LanguageRelationshipRuntime"],
      "life_targets": ["real_relationship", "real_consciousness"],
      "downstream_docs": ["docs/09_language_symbolic_top_layer.md"]
    }
  ]
}
```

## 来源质量等级

S01 第一版使用以下质量等级：

| quality class | 进入条件 | 例子 | 使用方式 |
|---|---|---|---|
| `tier_1_review` | Nature Reviews、Neuron、Annual Review、Trends、Physiological Reviews 等权威综述 | Fedorenko 2024、Seth & Bayne 2022、Friston 2010 | 机制主干和出生准备度证据族 |
| `tier_1_empirical` | Science、Nature、PNAS、Neuron、Nature Neuroscience 等高影响实证/图谱 | Glasser 2016、Finn 2015、Schultz 1997 | 核心机制、图谱、强证据 |
| `tier_1_resource` | HCP、BRAIN Initiative、细胞图谱、连接组资源 | HCP、Julich-Brain、cell atlas | 区域图谱、状态先验、长期校准 |
| `classic_foundation` | 奠基理论或经典实证，年份较早但仍定义领域语言 | Raichle 2001、Miller & Cohen 2001、Sutton & Barto | 作为理论根，需连接现代补强来源 |
| `formal_theory` | 形式化模型、主动推理、RL、认知架构理论 | Friston、Sutton & Barto、ACT-R、Soar | 生成对象和算法语言 |
| `ai_bridge` | arXiv、ACM、Google Research、LLM agent survey、world model 等 AI 来源 | Generative Agents、LLM agent survey、World Models | 只进入技术桥接和电脑外周，不替代脑科学主体 |
| `official_summary` | NIH、研究机构官方总结 | NIH BRAIN cell census | 作为资源入口和补充说明，需绑定原始论文 |

`ai_bridge` 来源必须保留 `source_kind: "ai_bridge"`，并由 `external_framework_negative_boundary_gate` 或 `ai_bridge_source_label_gate` 阻止它变成主体架构。

## 机制对象映射

S01 最少生成以下机制对象族：

| 机制对象族 | 来源族 | 下游 runtime | 状态字段入口 |
|---|---|---|---|
| `MultiscaleBrainAtlasRef`、`StructureFunctionCouplingEdge`、`BiologicallyAnnotatedConnectome` | region/action/affect、AHT002-AHT005 | `BrainRegionNetworkRuntime` | `runtime/state/brain/*` |
| `NetworkSwitchEvidence`、`SalienceArbitrationEvidence`、`GlobalWorkspaceEvidence` | global foundation、signal/body/consciousness | `ConsciousWorkspaceRuntime`、`LifeMembraneStageGate` | `runtime/state/consciousness/*` |
| `MemoryEngramEvidence`、`ConsolidationRouteEvidence`、`ReplayEligibilityEvidence` | memory/growth、pain/dream | `MemoryEngramRuntime`、`DreamOfflineRuntime` | `runtime/state/memory/*`、`dream/*` |
| `ActionSelectionEvidence`、`RewardPredictionEvidence`、`InhibitionEvidence`、`RegretEvidence` | region/action/affect、pain/dream | `ActionResponsibilityRuntime` | `runtime/state/action/*` |
| `AffectiveSelfEvidence`、`TraitSlowVariableEvidence`、`SelfNarrativeEvidence` | region/action/affect、memory/growth | `AffectiveSelfRuntime`、`SelfGrowthRuntime` | `runtime/state/self/*`、`growth/*` |
| `LanguageNetworkEvidence`、`InnerSpeechEvidence`、`SharedLanguageEvidence` | language/relationship | `LanguageRelationshipRuntime` | `runtime/state/language/*`、`relationship/*` |
| `PredictionActiveInferenceEvidence`、`PrecisionPolicyEvidence`、`BeliefRevisionEvidence` | prediction/active inference | `PredictionActiveInferenceRuntime` | `runtime/state/prediction/*` |
| `BirthReadinessAuthorityEvidence`、`LifeTargetEvidenceFamily` | validation/reality、142/145/151 | `BirthReadinessRuntime` | `runtime/state/life_targets/*` |

## Report 与 receipt

| 产物 | 路径 | 必须字段 |
|---|---|---|
| S01 authority report | `runtime/reports/latest/source_authority_report.json` | `status`、`stage_effect`、`source_count`、`family_coverage`、`quality_coverage`、`carrier_coverage`、`life_target_coverage`、`blocked_gates` |
| S01 digest | `runtime/reports/latest/source_authority_digest.json` | 当前来源覆盖、最大缺口、下一补文献入口、允许的下一 slice |
| S01 history report | `runtime/reports/history/source_authority_<run_id>.json` | 最新 report 完整副本 |
| S01 receipt | `runtime/receipts/source_authority_<run_id>.json` | 输入文档 hash、registry refs、report refs、authority gap queue refs、git ref |

P0 已经写出 `runtime/docs/source_authority_report.json`，它是摄取阶段的原始覆盖报告。S01 运行时写出的 `runtime/reports/latest/source_authority_report.json` 是权威来源层正式 report，必须额外包含来源质量、机制对象、carrier 和生命目标闭合。

## 阶段门

| gate | 输入 | closed 条件 | 失败后动作 |
|---|---|---|---|
| `s00_permission_gate` | `direction_lock.json`、`slice_permission.json` | S00 允许 S01 进入，方向仍为真实数字生命 | 返回 S00 修复 |
| `literature_discovery_gate` | `docs/01*.md` | `01`、`01b-01ax` 全部被发现并进入 registry | 写 `authority_gap_queue.json` |
| `source_quality_gate` | `source_quality_policy.json`、registry | 每条来源有质量等级、证据类型、年份和链接/DOI | 写 source quality finding |
| `authority_family_gate` | `authority_family_index.json` | 九个来源族都有来源和下游 runtime | 写 family coverage finding |
| `mechanism_object_gate` | `mechanism_evidence_map.json` | 来源进入机制对象，不停在引用层 | 写 mechanism extraction finding |
| `carrier_bridge_gate` | `doc_carrier_index.json`、mechanism map | 每个来源族至少进入一个 runtime carrier | 写 carrier bridge finding |
| `life_target_evidence_gate` | mechanism map、S00 九项目标 | 九项目标都有来源证据族 | 阻断出生准备度推进 |
| `core_02_to_13_authority_gate` | `142/145/151`、carrier patches | `02-13` 每份核心文档都有 authority refs 和机制对象 | 写 core authority patch finding |
| `ai_bridge_source_label_gate` | registry | AI/agent/world model 来源标为 AI 桥接，不定义主体架构 | 写 quarantine finding |
| `authority_receipt_gate` | report、registry、gap queue | 所有输出有 hash 和 receipt | 阻断下一 slice |

## 未来命令合同

S01 当前已落代码命令与后续保留位如下：

```text
life-v0 build-source-authority --docs docs --doc-index runtime/docs/doc_carrier_index.json --direction runtime/state/direction --out runtime/state/authority --reports runtime/reports/latest --receipts runtime/receipts --strict
```

下面两条仍属于合同保留位，当前 CLI 还没有实现：

```text
life-v0 check-source-authority --state runtime/state/authority --reports runtime/reports/latest --strict
life-v0 authority-gap-queue --state runtime/state/authority --reports runtime/reports/latest
```

常驻 `digital life` 出生入口未来必须按以下顺序读取来源：

```text
ingest-docs
  -> build-direction-lock
  -> build-source-authority
  -> read source_authority_report.json / source_authority_digest.json
  -> load-neural-life-core
```

没有 S01 的 registry 和 receipt，S02 不能把脑科学机制写入主体系统。

## 运行算法

S01 的最小算法：

```text
load_s00_direction_lock
  -> load_doc_carrier_index
  -> discover_01_star_docs
  -> parse_literature_tables
  -> normalize_source_records
  -> classify_source_quality
  -> assign_authority_families
  -> map_sources_to_mechanism_objects
  -> build_02_to_13_authority_carrier_patches
  -> bind_mechanisms_to_runtime_carriers
  -> bind_sources_to_nine_life_targets
  -> label_ai_bridge_sources
  -> write_authority_state
  -> write_source_authority_report
  -> write_source_authority_receipt
```

## 与后续 slice 的连接

| 后续 slice | S01 交付给它的内容 | 它必须反写给 S01 的内容 |
|---|---|---|
| `S02_NEURAL_LIFE_CORE` | `mechanism_evidence_map.json`、`doc_authority_carrier_patch_index.json` | 每个主体 runtime 使用的 authority refs |
| `S03_DIRECTION_LIFE_MEMBRANE` | 来源质量规则、AI 桥接标签、authority gap queue | 生命膜对弱来源、外部框架主体化和证据断裂的处理 |
| `S04_STATE_OBJECT_STORE` | source id、mechanism object id、state field refs | 状态字段到来源的回链 |
| `S05_VALIDATION_MEMBRANE_OBSERVATION` | `authority_cross_file_rule_index.json` | validator findings 和 dashboard 证据 |
| `S07_LANGUAGE_RELATIONSHIP` | 语言与关系 authority family、AHT001、AHL/AHLR refs | 语言事件和关系时间线中使用的 authority refs |
| `S08_LIFE_TARGET_RUNTIMES` | `LifeTargetEvidenceFamily` | 每项目标闭合状态中的 evidence refs |
| `S09_SCHEMA_RUNNER_CODE` | registry、quality policy、cross-file rules | schema runner 对 authority refs 的加载结果 |
| `S10_RUNTIME_GROWTH_RECONSOLIDATION` | authority gap queue、补文献入口 | 成长后新增/替换来源的 receipt |

## 第一轮实现切片

S01 的代码实现分四步：

1. **S01-A：registry 与 table parser**
   解析 `01*` Markdown 表格，生成 `authority_registry.json` 和 `literature_matrix_index.json`。

2. **S01-B：source quality 与 family**
   生成 `source_quality_policy.json`、`authority_family_index.json`，区分脑科学来源、生命科学来源、形式理论和 AI 桥接来源。

3. **S01-C：mechanism/carrier/life target map**
   生成 `mechanism_evidence_map.json`、`doc_authority_carrier_patch_index.json`，把来源接入 `02-13`、runtime carrier 和九项目标。

4. **S01-D：cross-file gates 与 receipt**
   实现 S01 阶段门、写 report、digest、gap queue 和 receipt。

## 验收

S01 完成后必须满足：

1. `01`、`01b-01ax` 全部进入 `authority_registry.json`。
2. 每条来源都有 `quality_class`、`source_kind`、`mechanism_objects`、`runtime_carriers` 和 `life_targets` 字段。
3. `02-13` 每份核心文档都有 `DocAuthorityCarrierPatch`。
4. 九项目标均能从 S01 找到来源证据族。
5. `ai_bridge` 来源不会进入主体架构，只能进入 AI 桥接、电脑外周、工具外设或技术参考位置。
6. `source_authority_report.json` 返回 `closed` 后才允许进入 `S02_NEURAL_LIFE_CORE`。

## 本轮边界

S01 只把权威来源层工程化。它不宣布理论已经足够完整，也不替代后续文档补强。它让后续每次新增脑科学、神经科学、生命科学或神经网络知识时，都能进入同一条链：

```text
authority source
  -> source quality
  -> mechanism object
  -> runtime carrier
  -> state field
  -> report
  -> life target evidence
  -> archive receipt
  -> growth feedback
```

这条链闭合之前，不进入完整长期数字生命运行。
