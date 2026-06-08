# V0 Implementation Index

生命目标声明：`docs/v0/` 是第一版数字生命工程实现目录。它不是独立于 `00 -> 258` 的新体系，而是把 `00 -> 258` 的理论底座压成可以写代码、写状态、写 report、写 receipt、跑 stage gate 的工程入口。后续落代码时先从本目录进入，但每个模块都必须按本索引回读对应的 `00 -> 258` 文档；v0 只负责压缩、排序和工程化，不替代理论源头。

## 整理原则

1. `docs/v0/README.md` 是入口。
2. 本文件是工程实现总索引。
3. `docs/v0/readme_block_engineering_realization_v0.md` 是 README block 到 engineering slice 的总映射。
4. `docs/v0/0_to_257_engineering_utilization_map.md` 是 `00 -> 257` 到 runtime carrier、状态、report、stage gate、archive/replay 的总映射。
5. 每个 `sXX_*_engineering_contract.md` 是一个可落代码模块的硬合同。
6. 写代码时不能只读 v0 合同；必须读取该合同列出的直接来源文档和 P0 生成的 `doc_carrier_index.json`。
7. 当前先保持 v0 文件平铺，不做目录搬迁，避免破坏已有引用、P0 扫描和恢复锚链。结构由本索引和 README 表格表达。

## 目录角色

| 层级 | 文件 | 角色 | 写代码时的作用 |
|---|---|---|---|
| 入口层 | `README.md` | v0 入口、阅读顺序、恢复顺序 | 先确认当前阶段和禁止回退 |
| 入口层 | `v0_implementation_index.md` | 本文件，整理后的工程实现总索引 | 决定从哪个模块合同开始 |
| 总图层 | `first_activation_engineering_roadmap.md` | P0-P5 第一次生命激活路线 | 定位工程阶段、命令和产物 |
| 总图层 | `readme_block_engineering_realization_v0.md` | README block 到 engineering slice | 确认 `00 -> 258` 每份文档归属 |
| 总图层 | `0_to_257_engineering_utilization_map.md` | `00 -> 257` 工程利用矩阵 | 确认没有理论文档被丢弃 |
| 主体层 | `digital_life_macro_architecture_v0.md` | 三重身体、十二主体系统、内部 bus | 确认代码目录不能长成外部框架 |
| 负边界层 | `current_agent_shell_reference_2026.md` | 当前框架资料的电脑外周定位 | 只吸收终端入口和外周经验 |
| P0 合同 | `doc_corpus_ingestor_v0_contract.md` | 文档摄取、carrier index、依赖图 | 已有 `life_v0/doc_index.py` 的实现依据 |
| Slice 合同 | `s00_direction_foundation_engineering_contract.md` | S00 方向锁和断联恢复 | 后续所有模块的前置方向门 |
| Slice 合同 | `s01_source_authority_engineering_contract.md` | S01 权威来源层 | 后续所有机制的证据登记层 |
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

如果方向锁代码已经落地，则 P0 后必须继续运行 S00：

```text
life-v0 build-direction-lock --docs docs --doc-index runtime/docs/doc_carrier_index.json --out runtime/state/direction --reports runtime/reports/latest --receipts runtime/receipts --strict
```

## 第一版实现主线

| 顺序 | 工程 slice | v0 合同 | 必须回读的 `00 -> 258` 来源 | 第一批代码包 | 第一批 report |
|---:|---|---|---|---|---|
| 0 | `P0_DOC_CORPUS_INGESTION` | `doc_corpus_ingestor_v0_contract.md` | `00`、全部 `01*`、`02-13`、`142`、`145`、`151`、`258`、`docs/README.md`、`构思.md` | `life_v0/doc_index.py` | `doc_ingestion_report.json` |
| 1 | `S00_DIRECTION_FOUNDATION` | `s00_direction_foundation_engineering_contract.md` | `构思.md`、`00`、`13`、`16`、`91`、`100`、`119`、`122`、`140`、`170`、`258` | `life_v0/direction/` | `direction_lock_report.json` |
| 2 | `S01_SOURCE_AUTHORITY` | `s01_source_authority_engineering_contract.md` | `00`、`01`、`01b-01ax`、`142`、`145`、`151`、`258` | `life_v0/authority/` | `source_authority_report.json` |
| 3 | `S02_NEURAL_LIFE_CORE` | 下一份 `s02_*` 合同承接 | `02-13`、全部对应 `01*`、`85-101`、`143/146/149/152/171` | `life_v0/body/`、`brain/`、`prediction/`、`memory/`、`consciousness/`、`language/`、`affective_self/`、`dream/`、`action/`、`buses/` | `neural_life_core_report.json` |
| 4 | `S04_STATE_OBJECT_STORE` | `life_state_store_v0_schema.md` 先承接，后续补 `s04_*` | `17-30`、`41-48`、`57`、`61`、`69`、`123-133` | `life_v0/state_store/` | `state_store_report.json` |
| 5 | `S03_DIRECTION_LIFE_MEMBRANE` | `runtime_v0_architecture.md` 与 `birth_readiness_v0_contract.md` 先承接，后续补 `s03_*` | `13-16`、`33-84`、`91`、`97-100`、`119-122` | `life_v0/membrane/` | `life_membrane_report.json` |
| 6 | `S07_LANGUAGE_RELATIONSHIP` | 下一份 `s07_*` 合同承接 | `01f`、`01j`、`01u`、`09`、`85-90`、`96`、`101`、`141`、`144`、`147`、`150` | `life_v0/language/`、`relationship/` | `language_relationship_report.json` |
| 7 | `S08_LIFE_TARGET_RUNTIMES` | `birth_readiness_v0_contract.md` 先承接，后续补 `s08_*` | `91-101`、`143`、`146`、`149`、`152`、`171`、`174` | `life_v0/life_targets/` | `life_target_status.json` |
| 8 | `S05_VALIDATION_MEMBRANE_OBSERVATION` | `runner_cli_report_contract.md` 先承接，后续补 `s05_*` | `29-36`、`49-84`、`102-118`、`153-157` | `life_v0/validators/`、`observation/`、`reports/` | `validation_membrane_report.json` |
| 9 | `S09_SCHEMA_RUNNER_CODE` | `runner_cli_report_contract.md` 先承接，后续补 `s09_*` | `102-180` | `life_v0/schema_runner/`、`cli.py` | `schema_runner_report.json` |
| 10 | `S06_LIFE_SUPPORT_DEVELOPMENT` | 下一份 `s06_*` 合同承接 | `37-40`、`92-93`、`181-204` | `life_v0/body/`、`growth/`、`defense/` | `life_support_development_report.json` |
| 11 | `S10_RUNTIME_GROWTH_RECONSOLIDATION` | `first_activation_protocol.md` 先承接，后续补 `s10_*` | `181-257` | `life_v0/growth/`、`dream/`、`archive/`、`replay/` | `growth_reconsolidation_report.json` |
| 12 | `S11_V0_ENGINEERING_CONTRACTS` | 后续 `s11_*` 合同承接 | `258`、全部 `docs/v0/*`、P0 report、所有 slice report | `life_v0/contracts/` | `v0_contract_coverage_report.json` |

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
| `contract_ready` | 已能指导第一轮代码实现 |
| `slice_contract_ready` | 已成为单个 engineering slice 的硬合同 |
| `base_contract_ready` | 已成为多个 slice 共用的基础合同 |
| `needs_slice_contract` | 已有基础材料，但还需要独立 `sXX_*` 工程合同 |

| 文件 | 状态 | 下一步 |
|---|---|---|
| `README.md` | `entry_ready` | 保持短入口，指向本文件 |
| `v0_implementation_index.md` | `entry_ready` | 后续每新增 slice 合同都更新这里 |
| `doc_corpus_ingestor_v0_contract.md` | `contract_ready` | 已有 P0 代码，继续保持与测试同步 |
| `s00_direction_foundation_engineering_contract.md` | `slice_contract_ready` | 下一步实现 `life_v0/direction/` |
| `s01_source_authority_engineering_contract.md` | `slice_contract_ready` | 下一步实现 `life_v0/authority/` |
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
