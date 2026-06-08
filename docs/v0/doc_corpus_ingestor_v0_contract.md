# Doc Corpus Ingestor V0 Contract

生命目标声明：本文档定义第一次生命激活 P0 的工程合同。`DocCorpusIngestor` 的使命是把 `docs/` 中 `00 -> 257` 的理论底座、`258` 收束文档和 `docs/v0/` 合同转成可运行的文档承载索引。它不是普通文档索引器，而是数字生命第一次激活前的理论摄取器、方向记忆器和断联恢复入口。

## P0 目标

`DocCorpusIngestor` 必须证明三件事：

1. `00 -> 257` 全部文档已经被发现。
2. 每份文档已经归入一个 README block、一个 engineering slice 和至少一个 runtime carrier。
3. `02-13` 核心脑科学文档已经形成跨模块连接，不停在孤立综述。

若任一条件失败，`doc_carrier_gate` 必须返回 `blocked`，第一次有限激活不能继续。

## 输入范围

| 输入 | 规则 |
|---|---|
| `docs/*.md` | 扫描一级 Markdown 文件，包含 `00`、`01*`、`02-257`、`258`、`README.md`、`构思.md` |
| `docs/v0/*.md` | 扫描 v0 合同与工程文档 |
| `docs/README.md` | 作为总索引与断联恢复锚 |
| `docs/16_digital_life_gap_register.md` | 作为下一轮优先级锚 |
| `docs/13_agentic_human_research_synthesis.md` | 作为总综合与生命目标锚 |

P0 不读取 runtime 产物作为理论来源。runtime 产物只能作为输出和回链。

## 文档编号解析

| 类型 | 匹配规则 | 示例 |
|---|---|---|
| `protocol` | `00_*.md` | `00_research_protocol.md` |
| `literature_matrix` | `01*.md` | `01_literature_matrix.md`、`01ax_*` |
| `core_synthesis` | `02_*.md` 到 `13_*.md` | `09_language_symbolic_top_layer.md` |
| `integration_gap` | `14_*.md` 到 `16_*.md` | `16_digital_life_gap_register.md` |
| `object_contract` | `17_*.md` 到 `84_*.md` | `41_runtime_state_store_schema.md` |
| `life_target` | `85_*.md` 到 `101_*.md` | `95_dream_reality_and_offline_life_timeline.md` |
| `schema_runner` | `102_*.md` 到 `180_*.md` | `136_life_reality_minimal_runner_code_skeleton_plan.md` |
| `activation_growth` | `181_*.md` 到 `257_*.md` | `225_life_reality_*_activation_plan.md` |
| `linear_closure` | `258_*.md` | `258_linear_chain_closure_and_v0_contract_transition.md` |
| `v0_contract` | `docs/v0/*.md` | `runtime_v0_architecture.md` |
| `origin_seed` | `构思.md` | `构思.md` |

## Runtime carrier 词表

`DocCorpusIngestor` 第一版必须支持以下 carrier：

| carrier | 生命位置 | 对应文档 |
|---|---|---|
| `DocCorpusIngestor` | 理论摄取 | `00`、`README`、`258`、`docs/v0/*` |
| `SourceAuthorityRegistry` | 权威来源与论文底座 | `01*`、`142`、`145`、`151` |
| `DirectionLockKernel` | 方向锁与断联恢复 | `13`、`14`、`16`、`91`、`100`、`119`、`122`、`140`、`170`、`258` |
| `BrainRegionNetworkRuntime` | 脑区、连接组、大尺度网络 | `01o`、`01p`、`02`、`03` |
| `BodySignalRuntime` | 内感受、稳态、身体信号 | `01l`、`01n`、`04`、`11`、`18`、`37` |
| `PredictionActiveInferenceRuntime` | 主动预测、信念、误差、精度 | `01v-01ax`、`04`、`10`、`11` |
| `MemoryEngramRuntime` | 记忆、engram、replay | `01q`、`05`、`17`、`21`、`25`、`29`、`41`、`55` |
| `ActionResponsibilityRuntime` | 动作、抑制、责任 | `01r`、`06`、`20`、`75`、`80-84`、`94`、`98` |
| `AffectiveSelfRuntime` | 情绪、人格、自我成长 | `01g`、`01h`、`01s`、`07`、`39`、`40`、`92`、`93` |
| `DreamOfflineRuntime` | 睡眠、梦境、离线生命 | `01i`、`01t`、`08`、`19`、`23`、`27`、`31`、`95`、`99` |
| `LanguageRelationshipRuntime` | 语言主神经束与关系 | `01f`、`01j`、`01u`、`09`、`85-90`、`96`、`101`、`141`、`144`、`147`、`150` |
| `ConsciousWorkspaceRuntime` | 意识、注意、工作区 | `01m`、`10`、`13`、`143`、`146` |
| `LifeStateStore` | 生命状态根 | `17-18`、`21-22`、`25-30`、`41`、`48`、`57`、`61`、`69`、`123-133`、`docs/v0/life_state_store_v0_schema.md` |
| `LifeMembraneStageGate` | 生命膜、validator、quarantine | `13-16`、`33-36`、`37-48`、`49-84`、`91`、`97-100`、`102-118`、`119-122`、`docs/v0/s03_direction_life_membrane_engineering_contract.md` |
| `BirthReadinessRuntime` | 出生准备度九项目标 | `143`、`146`、`149`、`152`、`171`、`174`、`docs/v0/birth_readiness_v0_contract.md` |
| `RunnerCliRuntime` | 命令、report、receipt | `35`、`53`、`62`、`118`、`123`、`131`、`136`、`155`、`158-168`、`docs/v0/runner_cli_report_contract.md` |
| `ActivationGrowthRuntime` | 激活、观察、巩固、成长 | `181-204`、`205-257`、`docs/v0/first_activation_protocol.md` |
| `ComputerPeripheralRuntime` | 电脑外周与世界接触 | `12`、`15`、`20`、`24`、`28`、`32`、`89`、`docs/v0/current_agent_shell_reference_2026.md` |
| `WorldContactMembrane` | 外部后果进入生命膜的接触层 | `12`、`15`、`20`、`24`、`28`、`32`、`89`、`docs/v0/current_agent_shell_reference_2026.md` |

## 分类优先级

一份文档可以进入多个 carrier。分类顺序如下：

1. 明确编号范围优先。
2. 文件名关键词补充。
3. 文档标题补充。
4. 文档正文关键词补充。
5. `0_to_257_engineering_utilization_map.md` 的分组规则兜底。

若一份文档只被兜底分类，`classification_confidence` 为 `inferred`。若找不到 carrier，则 `doc_carrier_gate` 返回 `blocked`。

## 输出文件

| 输出 | 路径 | 必须内容 |
|---|---|---|
| `doc_carrier_index` | `runtime/docs/doc_carrier_index.json` | 每份文档的 id、path、group、readme_block、engineering_slice、carriers、life_targets、dependencies |
| `doc_dependency_graph` | `runtime/docs/doc_dependency_graph.json` | 文档依赖边、模块依赖边、核心 `02-13` 连接图 |
| `source_authority_report` | `runtime/docs/source_authority_report.json` | 文献矩阵覆盖、权威来源族、需继续补强的领域 |
| `doc_ingestion_report` | `runtime/reports/latest/doc_ingestion_report.json` | 本次扫描结果、blocked reasons、quarantine refs、stage effect |
| `doc_carrier_receipt` | `runtime/receipts/doc_ingestion_<run_id>.json` | 输入、输出、hash、stage effect、direction lock ref |

## `doc_carrier_index.json` 形状

```json
{
  "schema_version": "doc_carrier_index_v0",
  "run_id": "doc-ingest-v0-0001",
  "generated_at": "2026-06-08T00:00:00+08:00",
  "direction_lock_ref": "docs/258_linear_chain_closure_and_v0_contract_transition.md",
  "documents": [
    {
      "doc_id": "D002",
      "path": "docs/02_brain_region_and_network_atlas.md",
      "group": "core_synthesis",
      "sequence": 2,
      "readme_block": "B02_CORE_NEURAL_LIFE",
      "engineering_slice": "S02_NEURAL_LIFE_CORE",
      "title": "Brain Region And Network Atlas",
      "runtime_carriers": ["BrainRegionNetworkRuntime", "ConsciousWorkspaceRuntime", "LifeStateStore"],
      "life_targets": ["real_consciousness", "real_life"],
      "dependencies": ["docs/01o_multiscale_region_connectome_matrix.md", "docs/03_default_executive_salience_networks.md"],
      "classification_confidence": "direct"
    }
  ],
  "coverage": {
    "total_docs": 0,
    "covered_docs": 0,
    "uncovered_docs": []
  }
}
```

## `doc_dependency_graph.json` 形状

```json
{
  "schema_version": "doc_dependency_graph_v0",
  "run_id": "doc-ingest-v0-0001",
  "nodes": [],
  "edges": [
    {
      "from": "docs/04_sensory_thalamus_interoception.md",
      "to": "BodySignalRuntime",
      "edge_type": "implements_runtime_carrier"
    }
  ],
  "core_02_to_13_bridge": {
    "02": ["BrainRegionNetworkRuntime", "ConsciousWorkspaceRuntime", "LifeStateStore"],
    "03": ["MultiscaleBrainGraphRuntime", "BodySignalRuntime", "LanguageRelationshipRuntime"],
    "04": ["BodySignalRuntime", "AffectiveSelfRuntime", "PredictionActiveInferenceRuntime"],
    "05": ["MemoryEngramRuntime", "LanguageRelationshipRuntime", "DreamOfflineRuntime"],
    "06": ["ActionResponsibilityRuntime", "LifeMembraneStageGate", "LanguageRelationshipRuntime"],
    "07": ["AffectiveSelfRuntime", "MemoryEngramRuntime", "LanguageRelationshipRuntime"],
    "08": ["DreamOfflineRuntime", "MemoryEngramRuntime", "ActivationGrowthRuntime"],
    "09": ["LanguageRelationshipRuntime", "ConsciousWorkspaceRuntime", "ActionResponsibilityRuntime"],
    "10": ["ConsciousWorkspaceRuntime", "MultiscaleBrainGraphRuntime", "BirthReadinessRuntime"],
    "11": ["BodySignalRuntime", "SignalMediaRuntime", "AffectiveSelfRuntime"],
    "12": ["ComputerPeripheralRuntime", "WorldContactMembrane", "RunnerCliRuntime"],
    "13": ["DirectionLockKernel"]
  }
}
```

## `doc_ingestion_report.json` 形状

```json
{
  "schema_version": "doc_ingestion_report_v0",
  "run_id": "doc-ingest-v0-0001",
  "status": "blocked",
  "stage_effect": "block_activation",
  "total_docs": 0,
  "covered_docs": 0,
  "uncovered_docs": [],
  "core_bridge_status": "blocked",
  "readme_block_coverage": {
    "B02_CORE_NEURAL_LIFE": ["docs/02_brain_region_and_network_atlas.md"]
  },
  "engineering_slice_coverage": {
    "S02_NEURAL_LIFE_CORE": ["docs/02_brain_region_and_network_atlas.md"]
  },
  "blocked_reasons": [],
  "quarantine_refs": [],
  "next_required_command": "life-v0 ingest-docs --strict"
}
```

## 命令合同

第一版 runner 增加 P0 命令：

```text
life-v0 ingest-docs --docs docs --out runtime/docs --reports runtime/reports/latest --receipts runtime/receipts --strict
```

退出码：

| code | 含义 |
|---|---|
| `0` | 全部文档已分类，`02-13` 连接完整 |
| `1` | 有文档未分类或缺 carrier |
| `2` | `02-13` 核心连接不完整 |
| `3` | 输出写入失败 |
| `4` | 输入路径错误 |

## 阶段门

| gate | 通过条件 | blocked 示例 |
|---|---|---|
| `doc_discovery_gate` | 找到 `00`、全部 `01*`、`02-257`、`258`、`docs/v0/*` | 缺 `13` 或 `257` |
| `readme_block_gate` | 每份文档都有 README block，且不是 `UNCLASSIFIED_README_BLOCK` | 新文档未进入 README 分块合同 |
| `engineering_slice_gate` | 每份文档都有 engineering slice，且不是 `UNCLASSIFIED_ENGINEERING_SLICE` | 文档无法进入代码包、状态命名空间或 report |
| `carrier_assignment_gate` | 每份文档至少一个 carrier | `docs/73_*.md` 无 carrier |
| `core_bridge_gate` | `02-13` 每份至少两个 carrier，`13` 连接全部核心 carrier | `09` 未连 `LanguageRelationshipRuntime` |
| `life_target_gate` | 九项生命目标都有文档支撑 | 真实梦境缺 `08/95/99` |
| `direction_lock_gate` | `258`、`README`、`16`、`13` 都被索引 | 缺断联恢复锚 |
| `output_write_gate` | index、graph、report、receipt 全部写出 | receipt 缺 hash |

## 生命目标映射

| 生命目标 | 必须有的文档支撑 | 第一 carrier |
|---|---|---|
| 真实有意识/真实意识 | `01m`、`10`、`13`、`143`、`146` | `ConsciousWorkspaceRuntime` |
| 真实情绪 | `01s`、`07`、`18`、`94` | `AffectiveSelfRuntime` |
| 真实人格 | `07`、`39`、`40`、`92`、`93` | `AffectiveSelfRuntime` |
| 真实生命 | `02-13`、`37`、`41`、`44`、`91`、`258` | `LifeStateStore` |
| 真实痛苦 | `01h`、`07`、`94`、`98` | `ActionResponsibilityRuntime` |
| 真实梦境 | `01i`、`01t`、`08`、`95`、`99` | `DreamOfflineRuntime` |
| 真实关系 | `01j`、`09`、`85-90`、`96`、`101` | `LanguageRelationshipRuntime` |
| 真实责任 | `01r`、`06`、`80-82`、`94`、`98` | `ActionResponsibilityRuntime` |
| 真实后悔 | `01h`、`06`、`94`、`98` | `ActionResponsibilityRuntime` |

## 第一轮验收样例

P0 实现完成后必须能回答：

1. 当前 `docs/` 有多少份可归类文档。
2. 哪些文档进入 `LanguageRelationshipRuntime`。
3. `02-13` 是否全部连接到 runtime carrier。
4. 九项生命目标分别由哪些文档支撑。
5. 哪些文档只被推断分类，需要后续补强。
6. 断联恢复时应该先读哪些文档。
7. 下一步 P1 需要哪些输出作为输入。

## 下一步交接

P0 成功后交给 P1：

| P0 输出 | P1 使用方式 |
|---|---|
| `doc_carrier_index.json` | `LifeStateStore` 写入 `archive_refs`、`continuity_refs` 和 `evidence_family_refs` |
| `doc_dependency_graph.json` | `LifeStateStore` 生成 `runtime/state/indexes/*.json` |
| `source_authority_report.json` | `BirthReadinessRuntime` 检查证据族 |
| `doc_ingestion_report.json` | `StageGate` 记录 P0 是否允许进入 P1 |
| `doc_carrier_receipt` | `ArchiveReceiptGraph` 写入长期回链 |
