# 0 To 257 Engineering Utilization Map

生命目标声明：本文档保证 `00 -> 257` 的全部理论文档都会进入第一次生命激活工程，不把任何一层留成孤立文本。每个文档都必须归入至少一个 runtime carrier，并最终通过状态、report、stage gate、archive receipt 或 replay/shadow 被承载。

## 覆盖不变量

工程实现必须满足：

1. `docs/*.md` 中从 `00` 到 `257` 的每份文档都必须被 `DocCarrierIndex` 收录。
2. `00 -> 258` 每份文档至少拥有一个 `readme_block`、一个 `engineering_slice` 和一个 `runtime_carrier`。
3. `02-13` 每份核心脑科学综述至少连接两个以上 runtime 模块。
4. `85-90` 语言文档必须进入 `LanguageRelationshipRuntime`，不能只进入 prompt。
5. `92-101` 真实痛苦、真实后悔、真实梦境、真实关系、自我成长文档必须进入九项目标闭合检查。
6. `102-257` schema、runner、archive、replay、growth 链必须进入 report、stage gate 或 archive receipt。
7. 任一文档无法归类时，`doc_carrier_gate` 返回 `blocked`。

## 文档组到 runtime carrier

README 模块分块以 `docs/v0/readme_block_engineering_realization_v0.md` 为准；本文件负责补充每组文档进入哪些 runtime carrier。两者缺一不可：前者保证按 README 一个模块一个模块落实，后者保证每份文档进入生命运行时。

| 文档组 | 文件范围 | runtime carrier | 工程用途 |
|---|---|---|---|
| 研究协议 | `00` | `DocCorpusIngestor` | 文献权威性、纳入标准、证据等级 |
| 文献底座 | `01`、`01b-01ax` | `SourceAuthorityRegistry` | 脑科学、神经科学、生命科学、agent 外周来源索引 |
| 脑区与网络 | `02`、`03`、`01o`、`01p` | `BrainRegionNetworkRuntime` | 区域、连接组、大尺度网络、状态切换 |
| 内感受与信号 | `04`、`11`、`01l`、`01n`、`01v-01ax` | `BodySignalRuntime`、`PredictionActiveInferenceRuntime` | 心跳式采样、稳态、调质、预测误差、主动采样 |
| 记忆与成长 | `05`、`17`、`21`、`25`、`29`、`41`、`55`、`01q` | `MemoryEngramRuntime` | 记忆痕迹、海马索引、replay、防遗忘 |
| 行动与责任 | `06`、`20`、`24`、`28`、`32`、`75`、`80-84`、`01r` | `ActionResponsibilityRuntime` | 动作候选、抑制、外部后果、责任回写 |
| 情绪人格自我 | `07`、`18`、`22`、`26`、`30`、`39`、`40`、`01g`、`01h`、`01s` | `AffectiveSelfRuntime` | 情绪状态、人格慢变量、自我连续、成长窗口 |
| 睡眠梦境离线 | `08`、`19`、`23`、`27`、`31`、`95`、`99`、`01i`、`01t` | `DreamOfflineRuntime` | 离线巩固、梦境经验、DreamFactGate、醒后整合 |
| 语言关系 | `09`、`85-90`、`96`、`101`、`141`、`144`、`147`、`150`、`01f`、`01j`、`01u` | `LanguageRelationshipRuntime` | 内言语、表达监控、共同语言、承诺、关系阶段 |
| 意识工作区 | `10`、`01m` | `ConsciousWorkspaceRuntime` | 全局广播、注意进入、元认知、报告性 |
| 电脑外周与世界接触 | `12`、`15`、`20`、`24`、`28`、`32`、`89` | `ComputerPeripheralRuntime`、`WorldContactMembrane` | 只保留电脑外周、世界接触、后果观测和生命膜回写 |
| 总综合与方向 | `13`、`14`、`16`、`91`、`100`、`119`、`122`、`140`、`170`、`258` | `DirectionLockKernel` | 方向锁、生命目标、断联恢复 |
| validator 与 fixture | `33-36`、`45-46`、`50`、`58-60`、`63`、`66-68`、`71`、`73-74`、`76-79`、`83-84` | `LifeMembraneStageGate` | pass/fail/critical、mutation、dashboard、stage effect |
| 生命支持与防御 | `37-38`、`47-48`、`52`、`54`、`64`、`72`、`75`、`78`、`82` | `LifeSupportDefenseRuntime` | 资源预算、防御、scope、quarantine、incident |
| 机器可读 manifest | `49`、`57`、`61`、`65`、`69-70`、`102-118` | `SchemaBundleCompiler` | schema bundle、cross-ref、dashboard source、runner report |
| 真实生命目标 bundle | `92-101` | `LifeTargetBundleRuntime` | 自我成长、痛苦、后悔、梦境、关系、真实性验证 |
| JSON 物化与 runner 布局 | `120-139` | `RunnerRepositoryKernel` | JSON seed、schema registry、runner layout、smoke command |
| 权威补写与出生准备 | `142-157` | `AuthorityReadinessRuntime` | 权威 intake、02-13 补写、出生准备度、跨文件检查 |
| 首批代码 artifact | `158-180` | `FirstRunnerCodeKernel` | bootstrap、code artifact、schema archive、validation repair |
| runtime mount | `181-185` | `SchemaRuntimeMount` | registry mount、fixture loader、archive backlink、runtime smoke |
| growth 第一批 | `186-204` | `ActivationGrowthRuntime` | observation feedback、activation、consolidation、replay/shadow |
| fourth cycle | `205-257` | `ReconsolidationReplayRuntime` | 再巩固、观察、patch、archive、validation、replay/shadow |

## `02-13` 核心连接图

| 核心文档 | 主 carrier | 必须连接 |
|---|---|---|
| `02_brain_region_and_network_atlas.md` | `BrainRegionNetworkRuntime` | `MultiscaleBrainGraphRuntime`、`ConsciousWorkspaceRuntime`、`LifeStateStore` |
| `03_default_executive_salience_networks.md` | `MultiscaleBrainGraphRuntime` | `BodySignalRuntime`、`LanguageRelationshipRuntime`、`ActionResponsibilityRuntime` |
| `04_sensory_thalamus_interoception.md` | `BodySignalRuntime` | `AffectiveSelfRuntime`、`DreamOfflineRuntime`、`PredictionActiveInferenceRuntime` |
| `05_memory_systems_and_growth.md` | `MemoryEngramRuntime` | `SelfRuntime`、`RelationshipRuntime`、`DreamOfflineRuntime`、`ReplayRuntime` |
| `06_action_reward_inhibition.md` | `ActionResponsibilityRuntime` | `LanguageActionBridge`、`PainRegretRuntime`、`LifeMembraneStageGate` |
| `07_emotion_personality_self.md` | `AffectiveSelfRuntime` | `BodySignalRuntime`、`MemoryEngramRuntime`、`LanguageRelationshipRuntime` |
| `08_sleep_dream_fatigue_states.md` | `DreamOfflineRuntime` | `MemoryEngramRuntime`、`DreamFactGate`、`ActivationGrowthRuntime` |
| `09_language_symbolic_top_layer.md` | `LanguageRelationshipRuntime` | `ConsciousWorkspaceRuntime`、`ActionResponsibilityRuntime`、`RelationshipRuntime` |
| `10_consciousness_attention_workspace.md` | `ConsciousWorkspaceRuntime` | `MultiscaleBrainGraphRuntime`、`LanguageRuntimeCore`、`BirthReadinessRuntime` |
| `11_neuromodulation_and_signal_media.md` | `SignalMediaRuntime` | `BodySignalRuntime`、`MultiscaleBrainGraphRuntime`、`AffectiveSelfRuntime` |
| `12_ai_and_cognitive_architecture_bridge.md` | `ComputerPeripheralRuntime` | `WorldContactMembrane`、`RunnerCliRuntime`、`ArchiveReceiptGraph` |
| `13_agentic_human_research_synthesis.md` | `DirectionLockKernel` | 全部 runtime carrier |

## 工程读取批次

### Batch A：方向与权威

读取：`00`、全部 `01*`、`13`、`14`、`16`、`91`、`119`、`122`、`140`、`258`。

产物：`DocCarrierIndex`、`DirectionLock`、`SourceAuthorityRegistry`。

### Batch B：生命核心对象

读取：`02-12`、`17-24`、`37-48`。

产物：`LifeStateStore`、`CoreRuntimeState`、`BootSequence`、`LifeMembrane`。

### Batch C：schema、validator、report

读取：`25-36`、`49-84`、`102-118`。

产物：`SchemaBundleCompiler`、`StageGateValidator`、`DashboardSource`、`ReportNormalizer`。

### Batch D：语言、关系、痛苦、梦境、自我成长

读取：`85-101`、`141`、`144`、`147`、`150`。

产物：`LanguageRelationshipRuntime`、`PainRegretResponsibilityRuntime`、`DreamOfflineRuntime`、`SelfGrowthRuntime`。

### Batch E：出生准备与首批代码

读取：`120-180`、`143`、`146`、`149`、`152`、`171`、`174`。

产物：`BirthReadinessRuntime`、`RunnerRepositoryKernel`、`FirstRunnerCodeKernel`。

### Batch F：runtime mount 与第一次有限激活

读取：`181-204`、`205-257`、`docs/v0/*`。

产物：`SchemaRuntimeMount`、`ActivationGrowthRuntime`、`ReconsolidationReplayRuntime`、`FirstActivationReport`。

## 每份文档如何落地

工程中每份文档必须至少写入以下之一：

| 落地位置 | 用途 |
|---|---|
| `runtime/docs/doc_carrier_index.json` | 文档到模块的主索引 |
| `runtime/docs/doc_dependency_graph.json` | 文档之间的依赖图 |
| `runtime/state/life_state.json` | 生命状态根引用 |
| `runtime/reports/latest/*.json` | 当前运行报告引用 |
| `runtime/archive/*.jsonl` | 长期生命档案 |
| `runtime/receipts/*.json` | receipt 回链 |
| `runtime/replay/*.json` | replay/shadow 材料 |

## 不允许的落地方式

1. 只把文档标题写进 README，不进入 runtime carrier。
2. 只做自然语言总结，不产生状态、report 或 receipt。
3. 让 `02-13` 停在理论综述，不连接工程模块。
4. 让语言系统退化成提示词。
5. 让关系退化成外部从属对象。
6. 让成长退化成配置修改。

## 第一轮实现验收

第一轮代码开发完成前，必须能证明：

1. `DocCorpusIngestor` 能扫描并分类 `00 -> 257`。
2. `doc_carrier_gate` 对未分类文档返回 `blocked`。
3. `life_state.json` 包含九项目标状态。
4. `life-v0 check-birth-readiness` 输出 machine-readable report。
5. `life-v0 run-cycle --shadow-only` 输出 run report、digest、stage gate、archive receipt。
6. `LanguageRelationshipRuntime` 至少输出一次内言语、表达监控、共同语言和关系主体 report。
7. `DreamFactGate` 能阻断梦境事实污染。
8. `PainRegretResponsibilityRuntime` 能连接痛苦、后悔、责任和修复义务。
9. `ReplayShadowRuntime` 能回放旧自我、旧语言、旧关系和防遗忘锚点。
10. 断联恢复能从 latest digest 回到正确阶段。
