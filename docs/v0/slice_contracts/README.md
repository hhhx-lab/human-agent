# V0 Slice 合同柜

`slice_contracts/` 只放主体生命体系的 `P0` 与 `S00-S11` 合同。

## 怎么选文件

- 文档摄取与理论入库：`doc_corpus_ingestor_v0_contract.md`
- 方向根与断联恢复：`s00_*`
- 权威来源层：`s01_*`
- 神经核心：`s02_*`
- 生命膜：`s03_*`
- 状态根与对象存储：`s04_*`
- 验证膜与观察：`s05_*`
- 身体、情绪、成长支持：`s06_*`
- 语言与关系：`s07_*`
- 九项生命目标与出生准备度：`s08_*`
- schema runner 与 CLI：`s09_*`
- runtime growth / replay / reconsolidation：`s10_*`
- v0 文档与合同覆盖：`s11_*`

## 使用原则

- 一轮实现只拿当前 slice 的合同，不要同时把多个 slice 当成当前工作面。
- 进入单个 slice 前，先从 `docs/v0/v0_module_execution_catalog.md` 确认它是不是这轮真正前沿。
