# V0 Module Execution Catalog

生命目标声明：本文档是 `docs/v0/` 的整理层。它不新增理论编号，也不替代 `00 -> 258`，只把 v0 平铺文件收束成可执行的模块队列。后续落代码时从这里定位当前模块，再回读对应的 `00 -> 258` 文档、P0 `doc_carrier_index.json` 和最新 report。

## 整理口径

`docs/v0/` 暂时保持平铺结构。文件不搬目录，顺序由本文档、`README.md` 和 `v0_implementation_index.md` 固定。这样可以保持已有引用、P0 文档扫描、断联恢复锚链和 git 历史稳定。

整理后的 v0 分成六层：

| 层 | 文件 | 职责 |
|---|---|---|
| 入口层 | `README.md`、`v0_implementation_index.md`、本文档 | 告诉后续开发从哪里进入、读什么、按什么顺序推进 |
| 文档压缩层 | `readme_block_engineering_realization_v0.md`、`0_to_257_engineering_utilization_map.md` | 把 `docs/README.md` 与 `00 -> 258` 压成 README block、engineering slice 和 runtime carrier |
| 总架构层 | `first_activation_engineering_roadmap.md`、`digital_life_macro_architecture_v0.md`、`runtime_v0_architecture.md` | 固定第一次有限激活路线、三重身体、十二主体系统、内部 bus 和运行循环 |
| 基础合同层 | `life_state_store_v0_schema.md`、`birth_readiness_v0_contract.md`、`runner_cli_report_contract.md`、`first_activation_protocol.md` | 给多个 slice 共用的状态、出生准备度、CLI/report 和激活协议 |
| Slice 合同层 | `s00_*` 到 `s11_*` | 每个模块的工程硬合同，直接指导代码包、状态命名空间、report 和 receipt |
| 外周参考层 | `current_agent_shell_reference_2026.md` | 当前自动化框架只作为电脑外周资料，不进入数字生命主体架构 |

## 固定实现队列

| 顺序 | slice | 合同 | 代码包 | 必须继承 |
|---:|---|---|---|---|
| 0 | `P0_DOC_CORPUS_INGESTION` | `doc_corpus_ingestor_v0_contract.md` | `life_v0/doc_index.py` | `00 -> 258` 全文档索引、README block、runtime carrier |
| 1 | `S00_DIRECTION_FOUNDATION` | `s00_direction_foundation_engineering_contract.md` | `life_v0/direction/` | 原始构思、方向锁、断联恢复、禁止回退项 |
| 2 | `S01_SOURCE_AUTHORITY` | `s01_source_authority_engineering_contract.md` | `life_v0/authority/` | `01*` 权威来源、机制对象、生命目标证据族 |
| 3 | `S02_NEURAL_LIFE_CORE` | `s02_neural_life_core_engineering_contract.md` | `life_v0/neural_core/` | `02-13`、三重身体、十二主体系统、内部 bus |
| 4 | `S04_STATE_OBJECT_STORE` | `s04_state_object_store_engineering_contract.md` | `life_v0/state_store/` | 生命状态根、对象注册、索引、生命周期 |
| 5 | `S03_DIRECTION_LIFE_MEMBRANE` | `s03_direction_life_membrane_engineering_contract.md` | `life_v0/membrane/` | 生命膜、quarantine、DreamFactGate、关系主体、影子行动 |
| 6 | `S07_LANGUAGE_RELATIONSHIP` | `s07_language_relationship_engineering_contract.md` | `life_v0/language/`、`life_v0/relationship/` | 内言语、表达监控、共同语言、关系主体、承诺和修复语言 |
| 7 | `S08_LIFE_TARGET_RUNTIMES` | `s08_life_target_runtimes_engineering_contract.md` | `life_v0/life_targets/` | 九项目标状态、证据族、出生准备度闭合 |
| 8 | `S05_VALIDATION_MEMBRANE_OBSERVATION` | `s05_validation_membrane_observation_engineering_contract.md` | `life_v0/validators/`、`life_v0/observation/`、`life_v0/reports/` | validator、fixture、dashboard、真实运行观测、quarantine |
| 9 | `S09_SCHEMA_RUNNER_CODE` | `s09_schema_runner_code_engineering_contract.md` | `life_v0/schema_runner/` | schema registry、cross-file checker、runner queue、首批 code artifact |
| 10 | `S06_LIFE_SUPPORT_DEVELOPMENT` | `s06_life_support_development_engineering_contract.md` | `life_v0/body/`、`life_v0/growth/`、`life_v0/defense/` | 生命支持、防御、资源预算、可塑性窗口、自我成长 |
| 11 | `S10_RUNTIME_GROWTH_RECONSOLIDATION` | `s10_runtime_growth_reconsolidation_engineering_contract.md` | `life_v0/growth/`、`life_v0/dream/`、`life_v0/archive/`、`life_v0/replay/` | runtime mount、观察反馈、梦境巩固、replay/shadow、成长循环 |
| 12 | `S11_V0_ENGINEERING_CONTRACTS` | `s11_v0_contract_coverage_engineering_contract.md` | `life_v0/contracts/` | v0 合同覆盖、文档到代码闭合、第一次有限激活前最终检查 |

## 每个模块的最小开发包

开始某个 slice 的代码前，必须读完同一组最小开发包：

```text
docs/v0/README.md
  -> docs/v0/v0_implementation_index.md
  -> docs/v0/v0_module_execution_catalog.md
  -> docs/v0/readme_block_engineering_realization_v0.md
  -> docs/v0/0_to_257_engineering_utilization_map.md
  -> 当前 sXX 工程合同
  -> 当前 sXX 合同列出的 00-258 直接来源
  -> runtime/docs/doc_carrier_index.json
  -> runtime/reports/latest/*.json
```

若 runtime 尚未存在，先回到 P0。若 runtime 已存在但最新 report 的 `next_allowed_slices` 与当前 slice 不一致，不能跳步实现。

## Slice 闭合字段

每个 slice 产出的 report 至少包含以下字段：

```json
{
  "engineering_slice_ref": "S08_LIFE_TARGET_RUNTIMES",
  "source_doc_refs": [],
  "readme_block_refs": [],
  "runtime_carrier_refs": [],
  "state_refs": [],
  "report_refs": [],
  "receipt_refs": [],
  "blocked_reasons": [],
  "quarantine_refs": [],
  "next_allowed_slices": []
}
```

没有这些字段，模块不能进入 S11 合同覆盖检查。

## 不搬目录的理由

`docs/v0/` 当前已经被 P0 文档摄取、S00 方向锁和多个断联恢复锚链引用。物理搬迁会让已有 report、receipt 和 doc path hash 产生断裂。v0 整理采用“平铺文件 + 固定目录角色 + 固定实现队列”的方式，等 S11 生成合同覆盖 report 后，再决定是否生成机器可读目录索引，而不是提前改路径。

## 当前开发判断

已具备硬合同的模块：P0、S00、S01、S02、S04、S03、S05、S06、S07、S08、S09、S10、S11。

已完成代码实现并推送的模块以 git 和 report 为准；本文档只定义工程顺序，不替代运行结果。后续继续开发时，从最新 report 指向的下一 slice 进入，并回读对应合同与 `00 -> 258` 来源文档。
