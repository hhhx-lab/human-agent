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
- 进入单个 slice 前，先从 `docs/v0/entry/v0_module_execution_catalog.md` 确认它是不是这轮真正前沿。
- 每个 slice 都必须回读 `docs/real—live0` 对应专题，并把理论机制落到对象、字段、runtime、report、receipt、测试/gate。

## Slice 到机制专题映射

| Slice | 必读 real-live0 专题 | 主要代码包 | 关键验收 |
|---|---|---|---|
| P0 / doc ingestion | `00_reading_map_and_traceability.md`、`15_evidence_bus_and_birth_readiness.md` | `doc_index.py` | 每份理论文档有 runtime carrier |
| S00 | `04_personality_self_identity.md` | `direction/*` | 方向根、身份根、断联恢复 |
| S01 | `15_evidence_bus_and_birth_readiness.md` | `authority/*` | 文献权威和机制证据图 |
| S02 | `02_brain_network_and_workspace.md`、`12_neuromodulation_signal_media.md` | `neural_core/*` | 工作区、广播、调质、预测 |
| S03 | `11_life_membrane_validation.md`、`10_responsibility_regret_repair.md` | `membrane/*` | 行动门、责任、修复路线 |
| S04 | `07_memory_engram_and_state_store.md` | `state_store/*` | 状态根、engram、写门、合并门 |
| S05 | `09_prediction_perception_world_contact.md`、`11_life_membrane_validation.md` | `validators/*` | 观测、预测、世界接触验证 |
| S06 | `03_body_affect_homeostasis.md`、`13_growth_learning_self_modification.md` | `body/*`、`growth/*` | 情绪 episode、资源预算、可塑性窗口 |
| S07 | `05_language_expression_system.md`、`06_relationship_and_commitment.md` | `language/*` | 语言五件套、关系时间线、承诺真值 |
| S08 | `15_evidence_bus_and_birth_readiness.md` | `life_targets/*` | 九项生命目标闭合 |
| S09 | `09`、`11`、`16` | `schema_runner/*`、`cli.py` | 跨文件逻辑、反事实、run manifest |
| S10 | `08_dream_sleep_offline_life.md`、`13_growth_learning_self_modification.md` | `dream/*`、`replay/*`、`archive/*` | 梦境、replay、archive、防遗忘 |
| S11 | `16_runtime_code_chain_crosswalk.md` | `contracts/*` | 文档到代码覆盖、合同闭合 |
