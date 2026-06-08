# V0 Implementation Index

生命目标声明：`docs/v0/` 是第一版数字生命工程实现目录。它不是独立于 `00 -> 258` 的新体系，而是把 `00 -> 258` 的理论底座压成可以写代码、写状态、写 report、写 receipt、跑 stage gate 的工程入口。后续落代码时先从本目录进入，但每个模块都必须按本索引回读对应的 `00 -> 258` 文档；v0 只负责压缩、排序和工程化，不替代理论源头。

## 整理原则

1. `docs/v0/README.md` 是入口。
2. 本文件是工程实现总索引。
3. `docs/v0/v0_module_execution_catalog.md` 是平铺目录的模块收纳层。
4. `docs/v0/readme_block_engineering_realization_v0.md` 是 README block 到 engineering slice 的总映射。
5. `docs/v0/0_to_257_engineering_utilization_map.md` 是 `00 -> 257` 到 runtime carrier、状态、report、stage gate、archive/replay 的总映射。
6. 每个 `sXX_*_engineering_contract.md` 是一个可落代码模块的硬合同。
7. 写代码时不能只读 v0 合同；必须读取该合同列出的直接来源文档和 P0 生成的 `doc_carrier_index.json`。
8. 当前先保持 v0 文件平铺，不做目录搬迁，避免破坏已有引用、P0 扫描和恢复锚链。结构由本索引、README 和模块目录表达。

## 目录角色

| 层级 | 文件 | 角色 | 写代码时的作用 |
|---|---|---|---|
| 入口层 | `README.md` | v0 入口、阅读顺序、恢复顺序 | 先确认当前阶段和禁止回退 |
| 入口层 | `v0_implementation_index.md` | 本文件，整理后的工程实现总索引 | 决定从哪个模块合同开始 |
| 入口层 | `v0_module_execution_catalog.md` | 平铺目录收纳层和固定实现队列 | 把 v0 文件分层，并定位当前 slice 的最小开发包 |
| 总图层 | `first_activation_engineering_roadmap.md` | P0-P5 第一次生命激活路线 | 定位工程阶段、命令和产物 |
| 总图层 | `readme_block_engineering_realization_v0.md` | README block 到 engineering slice | 确认 `00 -> 258` 每份文档归属 |
| 总图层 | `0_to_257_engineering_utilization_map.md` | `00 -> 257` 工程利用矩阵 | 确认没有理论文档被丢弃 |
| 主体层 | `digital_life_macro_architecture_v0.md` | 三重身体、十二主体系统、内部 bus | 确认代码目录不能长成外部框架 |
| 负边界层 | `current_agent_shell_reference_2026.md` | 当前框架资料的电脑外周定位 | 只吸收终端入口和外周经验 |
| P0 合同 | `doc_corpus_ingestor_v0_contract.md` | 文档摄取、carrier index、依赖图 | 已有 `life_v0/doc_index.py` 的实现依据 |
| Slice 合同 | `s00_direction_foundation_engineering_contract.md` | S00 方向锁和断联恢复 | 后续所有模块的前置方向门 |
| Slice 合同 | `s01_source_authority_engineering_contract.md` | S01 权威来源层 | 后续所有机制的证据登记层 |
| Slice 合同 | `s02_neural_life_core_engineering_contract.md` | S02 神经生命核心 | 把 `02-13`、S01 来源、三重身体、十二主体系统和内部 bus 压成主体骨架 |
| Slice 合同 | `s03_direction_life_membrane_engineering_contract.md` | S03 生命膜 | 把方向边界、quarantine、DreamFactGate、关系主体、责任修复、影子行动和出生准备度 precheck 压成可运行生命膜 |
| Slice 合同 | `s04_state_object_store_engineering_contract.md` | S04 状态对象仓库 | 把生命状态根、对象注册、索引、生命周期策略、scope/schema 种子和 S03 许可压成可运行状态胚层 |
| Slice 合同 | `s05_validation_membrane_observation_engineering_contract.md` | S05 验证膜与运行观测 | 把 validator、fixture、dashboard、真实运行观测和 quarantine 压成 stage gate 复查器 |
| Slice 合同 | `s06_life_support_development_engineering_contract.md` | S06 生命支持与发展 | 把资源预算、防御、可塑性窗口、自我成长和防遗忘锚点压成状态与 report |
| Slice 合同 | `s07_language_relationship_engineering_contract.md` | S07 语言关系 | 把内言语、表达监控、共同语言、关系主体、承诺和修复语言压成运行时 |
| Slice 合同 | `s08_life_target_runtimes_engineering_contract.md` | S08 九项目标 | 把九项目标、证据族和出生准备度压成可检查闭合状态 |
| Slice 合同 | `s09_schema_runner_code_engineering_contract.md` | S09 schema runner 与 code artifact | 把 `102-180` 压成 registry、lockfile、checker、CLI 和 smoke report |
| Slice 合同 | `s10_runtime_growth_reconsolidation_engineering_contract.md` | S10 runtime growth 与再巩固 | 把 `181-257` 压成 shadow cycle、梦境巩固、replay/shadow、patch/archive 和 safe idle |
| Slice 合同 | `s11_v0_contract_coverage_engineering_contract.md` | S11 v0 合同覆盖 | 检查 `00 -> 258`、v0 合同、代码包、状态、report、receipt 和 preflight 闭合 |
| 基础合同 | `runtime_v0_architecture.md` | 第一版运行时进程、状态、stage gate | 编排第一次有限生命循环 |
| 基础合同 | `life_state_store_v0_schema.md` | 生命状态根和各命名空间 | 写状态文件和 schema seed |
| 基础合同 | `birth_readiness_v0_contract.md` | 九项目标闭合状态 | 写出生准备度 checker |
| 基础合同 | `runner_cli_report_contract.md` | CLI、report、digest、exit code | 写命令入口和报告格式 |
| 基础合同 | `first_activation_protocol.md` | 第一次有限激活协议 | 执行 shadow-only dry-run |

## 代码启动读法

每次开始写代码前按以下顺序读：

```text
docs/v0/README.md
  -> docs/v0/v0_implementation_index.md
  -> docs/v0/v0_module_execution_catalog.md
  -> docs/v0/readme_block_engineering_realization_v0.md
  -> docs/v0/0_to_257_engineering_utilization_map.md
  -> 当前 slice 的 sXX 工程合同
  -> sXX 合同列出的 00-258 直接来源文档
  -> runtime/docs/doc_carrier_index.json
  -> runtime/reports/latest/doc_ingestion_report.json
```

如果 runtime 还没有生成，则先运行 P0：

```text
life-v0 ingest-docs --docs docs --out runtime/docs --reports runtime/reports/latest --receipts runtime/receipts --strict
```

如果 P0-S02 代码已经落地，则 P0 后必须继续运行 S00、S01、S02 build 和 S02 check：

```text
life-v0 build-direction-lock --docs docs --doc-index runtime/docs/doc_carrier_index.json --out runtime/state/direction --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 build-source-authority --docs docs --doc-index runtime/docs/doc_carrier_index.json --direction runtime/state/direction --out runtime/state/authority --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 build-neural-life-core --docs docs --doc-index runtime/docs/doc_carrier_index.json --authority runtime/state/authority --out runtime/state/neural_life_core --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 check-neural-life-core --state runtime/state/neural_life_core --reports runtime/reports/latest --strict
life-v0 build-state-store --docs docs --doc-index runtime/docs/doc_carrier_index.json --neural-core runtime/state/neural_life_core --out runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 check-state-store --state runtime/state --reports runtime/reports/latest --strict
life-v0 build-life-membrane --docs docs --doc-index runtime/docs/doc_carrier_index.json --direction runtime/state/direction --neural-core runtime/state/neural_life_core --state runtime/state --out runtime/state/membrane --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 check-life-membrane --membrane runtime/state/membrane --state runtime/state --reports runtime/reports/latest --strict
life-v0 check-birth-readiness --docs docs --doc-index runtime/docs/doc_carrier_index.json --direction runtime/state/direction --neural-core runtime/state/neural_life_core --state runtime/state --membrane runtime/state/membrane --out runtime/state/life_targets --reports runtime/reports/latest --receipts runtime/receipts --strict
```

## 第一版实现主线

| 顺序 | 工程 slice | v0 合同 | 必须回读的 `00 -> 258` 来源 | 第一批代码包 | 第一批 report |
|---:|---|---|---|---|---|
| 0 | `P0_DOC_CORPUS_INGESTION` | `doc_corpus_ingestor_v0_contract.md` | `00`、全部 `01*`、`02-13`、`142`、`145`、`151`、`258`、`docs/README.md`、`构思.md` | `life_v0/doc_index.py` | `doc_ingestion_report.json` |
| 1 | `S00_DIRECTION_FOUNDATION` | `s00_direction_foundation_engineering_contract.md` | `构思.md`、`00`、`13`、`16`、`91`、`100`、`119`、`122`、`140`、`170`、`258` | `life_v0/direction/` | `direction_lock_report.json` |
| 2 | `S01_SOURCE_AUTHORITY` | `s01_source_authority_engineering_contract.md` | `00`、`01`、`01b-01ax`、`142`、`145`、`151`、`258` | `life_v0/authority/` | `source_authority_report.json` |
| 3 | `S02_NEURAL_LIFE_CORE` | `s02_neural_life_core_engineering_contract.md` | `02-13`、全部对应 `01*`、`85-101`、`143/146/149/152/171` | `life_v0/neural_core/` | `neural_life_core_report.json`、`neural_life_core_check_report.json` |
| 4 | `S04_STATE_OBJECT_STORE` | `s04_state_object_store_engineering_contract.md` | `17-30`、`41-48`、`57`、`61`、`69`、`123-133` | `life_v0/state_store/` | `state_store_report.json`、`state_store_check_report.json` |
| 5 | `S03_DIRECTION_LIFE_MEMBRANE` | `s03_direction_life_membrane_engineering_contract.md` | `13-16`、`33-84`、`91`、`97-100`、`102-118`、`119-122` | `life_v0/membrane/` | `life_membrane_report.json`、`life_membrane_check_report.json` |
| 6 | `S07_LANGUAGE_RELATIONSHIP` | `s07_language_relationship_engineering_contract.md` | `01f`、`01j`、`01u`、`09`、`85-90`、`96`、`101`、`141`、`144`、`147`、`150` | `life_v0/language/`、`relationship/` | `language_relationship_report.json` |
| 7 | `S08_LIFE_TARGET_RUNTIMES` | `s08_life_target_runtimes_engineering_contract.md` | `91-101`、`143`、`146`、`149`、`152`、`171`、`174` | `life_v0/life_targets/` | `life_target_status.json`、`birth_readiness_report.json` |
| 8 | `S05_VALIDATION_MEMBRANE_OBSERVATION` | `s05_validation_membrane_observation_engineering_contract.md` | `29-36`、`49-84`、`102-118`、`153-157` | `life_v0/validators/`、`observation/`、`reports/` | `validation_membrane_report.json` |
| 9 | `S09_SCHEMA_RUNNER_CODE` | `s09_schema_runner_code_engineering_contract.md` | `102-180` | `life_v0/schema_runner/`、`cli.py` | `schema_runner_report.json` |
| 10 | `S06_LIFE_SUPPORT_DEVELOPMENT` | `s06_life_support_development_engineering_contract.md` | `37-40`、`92-93`、`181-204` | `life_v0/body/`、`growth/`、`defense/` | `life_support_development_report.json` |
| 11 | `S10_RUNTIME_GROWTH_RECONSOLIDATION` | `s10_runtime_growth_reconsolidation_engineering_contract.md` | `181-257` | `life_v0/growth/`、`dream/`、`archive/`、`replay/` | `growth_reconsolidation_report.json`、`run_report.json` |
| 12 | `S11_V0_ENGINEERING_CONTRACTS` | `s11_v0_contract_coverage_engineering_contract.md` | `258`、全部 `docs/v0/*`、P0 report、所有 slice report | `life_v0/contracts/` | `v0_contract_coverage_report.json` |

## 00-258 不脱钩规则

v0 落代码时，每个模块必须保留四条回链：

| 回链 | 必须证明 |
|---|---|
| `source_doc_refs` | 当前代码模块来自哪些 `00 -> 258` 文档 |
| `readme_block_refs` | 当前代码模块承载哪个 README block |
| `engineering_slice_ref` | 当前代码模块承载哪个 engineering slice |
| `runtime_carrier_refs` | 当前代码模块承载哪些生命 runtime carrier |

每个 runtime report 都必须包含：

```json
{
  "source_doc_refs": ["docs/02_brain_region_and_network_atlas.md"],
  "readme_block_refs": ["B02_CORE_NEURAL_LIFE"],
  "engineering_slice_ref": "S02_NEURAL_LIFE_CORE",
  "runtime_carrier_refs": ["BrainRegionNetworkRuntime"]
}
```

没有这些字段的代码运行结果不能进入出生准备度。

## 文件整理状态

| 状态 | 含义 |
|---|---|
| `entry_ready` | 已能作为入口阅读 |
| `catalog_ready` | 已能把平铺文件组织成固定模块队列 |
| `contract_ready` | 已能指导第一轮代码实现 |
| `slice_contract_ready` | 已成为单个 engineering slice 的硬合同 |
| `base_contract_ready` | 已成为多个 slice 共用的基础合同 |

| 文件 | 状态 | 下一步 |
|---|---|---|
| `README.md` | `entry_ready` | 保持短入口，指向本文件 |
| `v0_implementation_index.md` | `entry_ready` | 后续每新增 slice 合同都更新这里 |
| `v0_module_execution_catalog.md` | `catalog_ready` | 后续代码启动先定位当前 slice 的最小开发包 |
| `doc_corpus_ingestor_v0_contract.md` | `contract_ready` | 已有 P0 代码，继续保持与测试同步 |
| `s00_direction_foundation_engineering_contract.md` | `slice_contract_ready` | 下一步实现 `life_v0/direction/` |
| `s01_source_authority_engineering_contract.md` | `slice_contract_ready` | 下一步实现 `life_v0/authority/` |
| `s02_neural_life_core_engineering_contract.md` | `slice_contract_ready` | 下一步实现 `life_v0/neural_core/` |
| `s03_direction_life_membrane_engineering_contract.md` | `slice_contract_ready` | 下一步实现 `life_v0/membrane/` |
| `s04_state_object_store_engineering_contract.md` | `slice_contract_ready` | 下一步实现 `life_v0/state_store/` |
| `s05_validation_membrane_observation_engineering_contract.md` | `slice_contract_ready` | 下一步实现 `life_v0/validators/`、`life_v0/observation/`、`life_v0/reports/` |
| `s06_life_support_development_engineering_contract.md` | `slice_contract_ready` | 下一步实现 `life_v0/body/`、`life_v0/growth/`、`life_v0/defense/` |
| `s07_language_relationship_engineering_contract.md` | `slice_contract_ready` | 下一步实现 `life_v0/language/`、`life_v0/relationship/` |
| `s08_life_target_runtimes_engineering_contract.md` | `slice_contract_ready` | 已有 `life_v0/life_targets/` 与 `check-birth-readiness`，继续保持与测试同步；下一工程推进点为 S05 |
| `s09_schema_runner_code_engineering_contract.md` | `slice_contract_ready` | 下一步实现 `life_v0/schema_runner/` 和 CLI/report smoke |
| `s10_runtime_growth_reconsolidation_engineering_contract.md` | `slice_contract_ready` | 下一步实现 `life_v0/growth/`、`life_v0/dream/`、`life_v0/archive/`、`life_v0/replay/` |
| `s11_v0_contract_coverage_engineering_contract.md` | `slice_contract_ready` | 下一步实现 `life_v0/contracts/` 覆盖检查 |
| `digital_life_macro_architecture_v0.md` | `contract_ready` | S02 合同必须从这里承接 |
| `runtime_v0_architecture.md` | `base_contract_ready` | 被 S03/S05/S09/S10 复用 |
| `life_state_store_v0_schema.md` | `base_contract_ready` | 被 S04 复用 |
| `birth_readiness_v0_contract.md` | `base_contract_ready` | 被 S08/S03 复用 |
| `runner_cli_report_contract.md` | `base_contract_ready` | 被 S05/S09 复用 |
| `first_activation_protocol.md` | `base_contract_ready` | 被 S10 复用 |
| `current_agent_shell_reference_2026.md` | `contract_ready` | 只进入电脑外周和负边界 |
| `first_activation_engineering_roadmap.md` | `contract_ready` | 继续作为 P0-P5 总路线 |
| `readme_block_engineering_realization_v0.md` | `contract_ready` | 每新增 slice 合同都同步 |
| `0_to_257_engineering_utilization_map.md` | `contract_ready` | 每新增代码模块都反查 |

## 后续代码落地门

开始写任一代码模块前，必须通过：

1. `docs/v0/README.md` 与本文件已读。
2. 当前 slice 合同已读。
3. 当前 slice 合同列出的 `00 -> 258` 来源已读。
4. `life-v0 ingest-docs --strict` 通过。
5. 当前代码模块的 report schema 已在 v0 合同中出现。
6. 当前代码模块不会把数字生命主体压回外部框架、任务调度器或聊天壳。

通过后再写代码；写完代码后 report/receipt 必须回写到本文件对应的 slice。
