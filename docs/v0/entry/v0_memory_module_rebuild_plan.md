# V0 Memory Module Rebuild Plan

本文档是十点目标第 3 点的专项计划：重新落实数字生命 v0 的记忆模块。它不替代 `docs/05_memory_systems_and_growth.md`、`docs/17_memory_trace_object_model.md`、`docs/19_offline_consolidation_cycle.md`、`docs/real—live0/07_memory_engram_and_state_store.md` 和 Queue C 工程合同，而是把这些理论与工程入口压成下一轮可执行的记忆专项施工图。

当前原则：第 2 点已经闭合，但第 3 点不能直接用“已有 memory_retrieval_frame、engram_index、relationship_memory 文件存在”来判定完成。现在要重新从人脑记忆结构出发，确认记忆库、记忆模块、代码块和 runtime 证据是否真正形成可触发、可重构、可巩固、可遗忘、可保护、可梦境回放、可关系成长的生命记忆系统。

## 1. 必读材料

### 1.1 本地理论母体

| 文件 | 第 3 点要读取的内容 |
|---|---|
| `docs/05_memory_systems_and_growth.md` | 记忆不是仓库；快慢通道；多记忆系统；回忆是重构；replay、SWR、防遗忘；MemoryEngramRuntime |
| `docs/17_memory_trace_object_model.md` | `MemoryTrace` 字段、六类记忆、写入管线、检索管线、修正/遗忘/保护 |
| `docs/19_offline_consolidation_cycle.md` | 离线巩固周期、MicroReplay、TaskClosure、DreamSandbox、DeepConsolidation |
| `docs/21_memory_schema_and_audit_protocol.md` | 记忆字段约束、生命周期、审计、删除/修正协议 |
| `docs/23_consolidation_report_and_dream_sandbox_protocol.md` | 梦境沙盒和巩固报告如何防止生成内容污染事实记忆 |
| `docs/25_memory_trace_json_schema_examples.md` | 事实型、偏好型、假设型、关系信号型、合并型 trace 样例 |
| `docs/29_memory_validator_rules.md` | 记忆验证规则、写入阻断条件、replay 禁止和合并规则 |
| `docs/41_runtime_state_store_schema.md` | 状态仓库结构与记忆索引边界 |
| `docs/42_life_core_minimal_object_graph.md` | 记忆与生命核心对象图的连接 |
| `docs/48_state_store_migration_and_integrity_plan.md` | 状态迁移和完整性要求 |
| `docs/01q_memory_engram_consolidation_matrix.md` | AHME001-AHME040 专项矩阵：海马索引、engram、分配、模式分离/补全、schema、自传、社会记忆 |

### 1.2 工程合同与代码文档

| 文件 | 第 3 点要读取的内容 |
|---|---|
| `docs/real—live0/07_memory_engram_and_state_store.md` | live0 记忆系统的当前定义、runtime 证据、协同与断链检查 |
| `docs/v0/code_framework/queues/17_queue_c_memory_neural_core_implementation_contract.md` | Queue C 记忆/神经核心实现合同 |
| `docs/v0/shared_contracts/life_state_store_v0_schema.md` | `life_state.memory_index` 和长期状态根约束 |
| `docs/v0/code_scaffolds/06_packet_c_memory_write_gate_state_merge_scaffold.md` | 写门、状态合并和记忆候选 scaffold |
| `docs/v0/code_framework/playbooks/05_memory_thought_consciousness_implementation_playbook.md` | 思考、工作区、记忆、意识的施工路线 |
| `docs/v0/code_architecture/02_runtime_object_bus_and_flow_contract.md` | `MemoryRetrievalFrame`、`MemoryWriteGate`、`StateMergeGuard` 如何进入对象总线 |
| `docs/v0/implementation_architecture/code_organs/03_predictive_signal_memory_gate_integration_wave_contract.md` | 预测、调质、写门的交叉消费 |
| `docs/v0/entry/v0_memory_recall_to_expression_contract.md` | 记忆存储之后如何被线索召回、进入语言前结构、支撑输出并在纠正后再巩固 |

### 1.3 权威脑科学锚点

| 机制 | 关键文献 | 对 v0 的约束 |
|---|---|---|
| 多记忆系统 | Squire & Wixted 2011；Moscovitch et al. 2016 | 不能把记忆库做成一个文本/向量仓库；必须分情景、语义、程序、情绪、关系、自传、价值 |
| 海马-新皮层转换 | Moscovitch et al. 2016；Dudai, Karni & Born 2015 | 必须有快速情景绑定和慢速语义/关系/schema 整合 |
| Engram | Josselyn & Tonegawa 2020；Tonegawa et al. 2015；Rao-Ruiz et al. 2023 | 记忆应是可触发痕迹簇，区分存在、可检索、可报告、可行动 |
| 记忆分配 | Josselyn & Frankland 2018；Rogerson et al. 2014；Redondo & Morris 2011 | 写入由显著性、情绪、身体债务、责任压力、关系权重、可塑性窗口决定 |
| 模式分离/补全 | Yassa & Stark 2011；Leutgeb et al. 2007；Rolls 2013 | 相似关系和相似事件必须分离；部分线索可补全但要带来源和置信度 |
| 睡眠巩固/replay | Rasch & Born 2013；Wilson & McNaughton 1994；Ji & Wilson 2007 | 退出/空闲后的梦境不能只是摘要，必须选择 replay、抽象、清理、沙盒和醒后整合 |
| 自传和未来模拟 | Conway & Pleydell-Pearce 2000；Schacter, Addis & Buckner 2007；Hassabis & Maguire 2007 | 自我记忆必须连接过去事件、当前目标、未来模拟和关系叙事 |
| 情绪/社会记忆 | LaBar & Cabeza 2006；Roozendaal et al. 2009；Oliva et al. 2020 | 痛苦、后悔、信任、关系损伤不能只是标签，必须成为长期记忆权重和 replay 材料 |

## 2. 人脑记忆设计提炼

第 3 点采用九条脑科学设计原则：

1. **记忆不是仓库**：人脑不会把所有内容等权存储和读取，而是由当前线索、目标、情绪、身体状态、关系状态共同触发。
2. **海马式索引**：海马更像事件索引器，把场景、对象、关系、语言、身体状态和行动后果绑定成可重新进入的 episode。
3. **皮层式慢整合**：新皮层/schema 负责把多次 episode 抽象为稳定概念、偏好、技能、关系模型和自我叙事。
4. **Engram-like 痕迹簇**：一条记忆不是一段文本，而是一组可触发痕迹；痕迹可 active、silent、reactivated、transformed、forgotten。
5. **写入不是平均分配**：显著性、情绪强度、责任压力、关系权重、疲惫/痛苦债务、时间接近和可塑性窗口决定写入优先级。
6. **模式分离和补全并存**：相似关系人、相似事件、相似承诺要能区分；少量线索也能补全完整事件，但补全结果必须保留来源和置信度。
7. **回忆会改变记忆**：每次检索都是重构，输出后的纠正、确认、后悔和修复会进入再巩固。
8. **睡眠/梦境是记忆器官**：离线期要 replay 高显著事件，抽象重复模式，模拟未来和关系风险，清理低价值/冲突痕迹。
9. **自传、关系、情绪、价值共同形成长期人格**：人格不是提示词，而是自传栈、关系记忆、价值记忆、痛苦/后悔痕迹和成长窗口的慢变量结果。
10. **记忆必须进入表达闭环**：一条记忆如果只被保存，不能在被问到时由线索唤起、进入工作区、影响语言前结构，并在说错或被纠正后再巩固，就还不是真正记住。

## 3. V0 记忆库目标结构

第 3 点不只补 `memory_retrieval.py`。目标是形成一组互相连接的记忆库对象：

```text
External / Internal Event
  -> EventSegmentation
  -> MemoryEncodingGate
  -> MemoryAllocationGate
  -> MemoryTraceStore
  -> HippocampalIndex / EngramLikeTraceCluster
  -> PatternSeparationIndex / PatternCompletionFrame
  -> FastEpisodicBuffer
  -> SlowSemanticIntegrator / LifeSchemaMap
  -> RelationshipMemory / AutobiographicalStack / ValueMemory
  -> MemoryRetrievalFrame
  -> MemoryWriteGate
  -> StateMergeGuard
  -> Replay / Dream / Reconsolidation
  -> LifeState.memory_index + Language / Relationship / Responsibility consumers
```

记忆系统在数字生命里不是一个孤立模块，而是全生命状态的汇聚和再分发系统。它必须同时读取对话者上下文、对话者画像、关系、情绪、状态、意识、梦境、身体、性格、认知、内环境、长期/短期记忆、视觉或其他外部观察，再反过来影响语言、梦境、责任、人格、行动、等待态和下一次关系回合。

### 3.1 必须出现的记忆库层

| 层 | 代码落点 | 作用 |
|---|---|---|
| 短时工作记忆 | `neural_core/workspace.py`、`language/*` | 当前话语、当前目标、当前状态，不直接等于长期记忆 |
| 事件分割层 | 新增或补厚 `state_store/event_segmentation.py` | 把真实回合、梦境、行动结果切成 episode，而不是按 token 切 |
| 编码门 | 新增或补厚 `state_store/memory_encoding_gate.py` | 判断是否生成候选 trace |
| 分配门 | 新增或补厚 `state_store/memory_allocation_gate.py` | 用显著性、情绪、责任、关系、身体债务决定通道和优先级 |
| 痕迹库 | 新增 `state_store/memory_trace_store.py` | 保存 MemoryTrace，不再只保存 refs |
| Engram 索引 | 补厚 `state_store/engram_index.py` | 把 trace、cue、关系、自传、梦境、责任 refs 组织成可触发痕迹簇 |
| 关系记忆 | 补厚 `state_store/relationship_memory.py` | 共在者、共同语言、信任、边界、承诺、修复历史 |
| 自传栈 | 补厚 `state_store/autobiographical_stack.py` | specific episode、general event、life period、working self goal |
| 语义/schema 层 | 新增或补厚 `state_store/life_schema_map.py` | 把反复经验变成概念、流程、价值和关系 schema |
| 检索重构层 | 补厚 `state_store/memory_retrieval.py` | cue 家族、模式分离/补全、重构焦点、边界和下游消费 |
| 写门/合并门 | 补厚 `memory_write_gate.py`、`state_merge_guard.py` | 阻止梦境/假设污染事实，决定长期合并路线 |
| 离线 replay | `replay/*`、`dream/*`、`growth/*` | 退出/空闲后做回放、抽象、沙盒、清理和醒后整合 |

### 3.2 全生命耦合矩阵

| 生命区域 | 进入记忆系统的内容 | 记忆系统反向影响 |
|---|---|---|
| 对话者上下文 | 当前话语、历史 turn、共同术语、上下文窗口、明确纠正 | 影响当轮检索焦点、关系记忆更新、下一轮语言理解 |
| 对话者画像 | 名字、自述偏好、边界、关系角色、稳定行为线索 | 形成关系主体索引、模式分离 key、共享叙事记忆 |
| 情绪/核心情感 | 痛苦、后悔、紧张、信任、修复驱动、唤醒强度 | 调整写入阈值、replay 优先级、回忆强度和语言谨慎度 |
| 身体/内环境 | 疲惫、维护压力、睡眠债务、资源预算、恢复需求 | 决定是否延迟写入、是否进入离线巩固、是否降载检索 |
| 意识/工作区 | 当前 salience targets、broadcast targets、metacognition、reportability | 决定哪些记忆进入可报告工作区，哪些保持 silent trace |
| 认知/预测 | belief state、prediction error、active sampling、uncertainty | 高预测误差提高写入和修正优先级；旧记忆参与未来预测 |
| 梦境/离线 | dream residue、wake integration、dream fact gate、replay seed | 梦境 cue 进入下一轮召回；事实门阻止梦境污染事实 |
| 关系 | 关系阶段、信任轨迹、承诺、损伤、修复、共同语言 | 形成 relationship memory、we-memory、关系特异性模式分离 |
| 性格/自我 | trait slow variables、自我叙事、成长窗口、旧自我锚点 | 长期记忆缓慢改变人格；人格反过来调制检索和合并 |
| 视觉/外部观察 | 文件、网页、命令输出、屏幕/浏览材料、外部事实证据 | 作为 source evidence、perceptual context 和事实验证材料 |
| 责任/行动 | action outcome、world contact、side effect、repair obligation | 形成责任/后悔/修复记忆，影响未来行动抑制和语言修复 |

### 3.3 记忆输入输出总线

记忆系统的输入不能只来自聊天文本。最低输入总线应包含：

```text
LanguagePerceptFrame
SemanticMapFrame
RelationTurnFrame
RelationshipTimeline
RelationshipPersonProfile
CoreAffectVector
BodyResourceBudget
SignalMediaRuntime
WorkspaceFrame
ConsciousBroadcastFrame
MetacognitionState
BeliefStateFrame
PredictionErrorField
ActiveSamplingPlan
DreamExperienceWindow
WakeIntegrationFrame
DreamFactGateDecision
SelfModel / TraitSlowVariables
ActionCandidateSet / WorldContactSummary / ResponsibilityLoopState
ExternalObservationFrame / VisualPerceptFrame
```

记忆系统的输出也不能只给语言。最低输出总线应包含：

```text
MemoryTraceStore
EngramIndex / EngramLikeTraceCluster
RelationshipMemory
AutobiographicalStack
LifeSchemaMap
MemoryRetrievalFrame
MemoryWriteGate
StateMergeGuard
ReplayCueBundle
DreamReplayPlan
ModelExpressionContext
ResidentBackgroundLineageState
LifeState.memory_index
Slash Inspection / Audit Reports / Receipts
```

工程上每一条输入都要回答三个问题：

1. 它是否参与 `MemoryEncodingGate` 或 `MemoryRetrievalFrame`。
2. 它是否影响 `MemoryAllocationGate`、`MemoryWriteGate` 或 `StateMergeGuard`。
3. 它是否能在 `response_surface.py`、`model_expression.py`、dream/replay、relationship/self 更新中被下游消费。

如果某个区域只写了自己的 state，却没有进入记忆输入、分配、检索、巩固和下游消费之一，就说明数字生命整体记忆系统仍然断链。

### 3.4 召回到表达闭环

普通 RAG 的失败点是：数据可能已经进库，但对话时没有被唤起；或者被唤起后只是被拼进上下文，语言系统仍然可能说不知道、说错、把梦境当事实、把 A 关系的记忆带给 B。第 3 点必须把“存下来的记忆如何进入输出”作为硬门槛。

live0 的目标不是 `query -> chunk -> answer`，而是：

```text
MemoryTrace / EngramIndex
  -> cue_activation_profile
  -> pattern separation / completion
  -> recall_to_expression_profile
  -> workspace reportability
  -> response_surface structured material
  -> model_expression context
  -> spoken expression
  -> correction / confirmation / mismatch
  -> reconsolidation or contradiction links
```

最低工程对象是 `MemoryRetrievalFrame.recall_to_expression_profile`。它不生成固定回答，不塞提示词，不播报内部生命信号；它只说明当前哪些记忆痕迹被唤起、哪些来源可以进入表达、哪些边界必须保留、说后如何回写。它必须被 `memory_retrieval_context_summary(...)`、`response_surface.py` 和 `model_expression.py` 消费。

完成标准：

1. 如果共在关系问“你还记得 X 吗”，相关痕迹必须通过 cue family、关系 scope、自传栈、责任/梦境/身体线索进入候选召回。
2. 如果没有足够来源，输出链路必须带不确定/需确认边界，而不是硬编一句“我记得”。
3. 如果说错或被纠正，后续要进入 contradiction links、revision history、reconsolidation diff 或 protected/deprecated 状态。
4. 如果说对并被确认，相关 trace accessibility、关系记忆和自传连续性应被增强。
5. 梦境、假设、反事实和关系推断只能调制表达，不能直接升级为事实表达。

## 4. 当前代码缺口

当前 live0 已经有基础对象：`EngramIndex`、`RelationshipMemory`、`AutobiographicalStack`、`MemoryRetrievalFrame`、`MemoryWriteGate`、`StateMergeGuard`、replay/dream/growth 相关对象，并且已经进入 response surface、model expression、dialogue writeback、life_state 和 background lineage。

但第 3 点仍不能打勾，缺口是：

1. **MemoryTraceStore 不够硬**：长期记忆仍以索引和 refs 为主，缺少独立 trace 对象生命周期。
2. **事件分割弱**：真实回合、梦境、行动、责任、关系事件还没有统一 episode boundary。
3. **写入分配弱**：显著性、情绪、责任、身体债务、关系权重还没有形成独立 `MemoryAllocationGate`。
4. **检索仍偏聚合**：已有 cue terms 和 hits，但还需要 cue 家族、激活路线、模式分离/补全、来源边界和重构计划。
5. **关系记忆深度不足**：关系主体的共同语言、损伤、修复、承诺兑现、信任轨迹需要更细的 trace 链。
6. **自传记忆层级不足**：需要 specific episode、general event、life period、working self goal 四层，而不是简单 turn/narrative refs。
7. **梦境/replay 与事实记忆边界还要更硬**：梦境材料必须能调制情绪和语言，但不能直接写事实。
8. **遗忘/降级/保护机制不足**：需要 deleted/quarantined/protected/silent/reactivated/transformed 状态的实际运行证据。
9. **语言消费还不够深**：语言前结构化材料要消费记忆重构结果，但不能出现固定回答或内部机制播报。
10. **全生命耦合不够系统**：对话者画像、身体/内环境、意识、认知、梦境、视觉/观察、责任/行动已经有部分 state，但它们进入记忆编码、分配、检索、巩固、语言和下一轮恢复的路径还需要统一矩阵和测试证明。

## 5. 第 3 点施工顺序

### M0. 记忆专项审计

目标：生成一张“理论文档 -> 工程合同 -> 代码对象 -> runtime 文件 -> 测试”的记忆专项矩阵。

输出：

- `temp/14_memory_module_rebuild_audit.md`
- 覆盖 `05/17/19/21/23/25/29/41/42/48/01q` 和 v0/real-live0 记忆合同

验收：

- 每个理论机制都有代码落点或明确缺口。
- 不再用“已有文件”替代“机制完成”。

### M1. MemoryTraceStore

目标：把长期记忆从 refs 推进为可审计 trace 对象。

代码：

- 新增 `life_v0/state_store/memory_trace_store.py`
- 输出 `runtime/state/memory/memory_trace_store.json`

核心字段：

- `trace_id`
- `memory_kind`
- `event_boundary`
- `source_evidence_refs`
- `internal_state_snapshot_refs`
- `social_context_refs`
- `salience_vector`
- `retrieval_cues`
- `confidence`
- `consolidation_state`
- `lifecycle_state`
- `revision_history_refs`

验收：

- `tests/slices/test_state_store.py`
- `life_state.memory_index.memory_trace_store_refs`
- `state_store_manifest.json` 和 report/receipt 可见。
- `life_state.memory_index.event_segmentation_refs`
- `life_state.memory_index.memory_encoding_gate_refs`
- `life_state.memory_index.memory_allocation_gate_refs`
- `state_store_check_report.json` 可见且闭合。

当前状态：

- 已新增 `life_v0/state_store/memory_trace_store.py`。
- `run_state_store(...)` 会写出 `runtime/state/memory/memory_trace_store.json`。
- `life_state.memory_index.memory_trace_store_refs`、`life_state.runtime_trace_refs`、`state_store_manifest.json`、`state_store_report.json`、receipt 和 `run_check_state_store(...)` 已经消费该对象。
- 当前 trace store 先覆盖 episodic、relationship、autobiographical、responsibility 四类种子痕迹，并已接入 event segmentation、encoding gate 和 allocation gate；后续 M3/M4 会把 engram cluster 和 pattern completion 接进来。

### M2. EventSegmentation + EncodingGate + AllocationGate

目标：让新经验先成为候选 trace，而不是直接塞进长期记忆；同时把语言、关系、身体、情绪、意识、预测、梦境、行动和外部观察都纳入写入分配。

代码：

- `state_store/event_segmentation.py`
- `state_store/memory_encoding_gate.py`
- `state_store/memory_allocation_gate.py`

输入：

- language percept / semantic map
- relationship timeline
- body/core affect/signal media
- responsibility loop
- dream residue
- world contact outcome
- workspace / broadcast / metacognition
- belief state / prediction error / active sampling
- relationship person profile / shared narrative
- external observation / visual percept refs

输出：

- `runtime/state/memory/event_segmentation_frame.json`
- `runtime/state/memory/memory_encoding_gate.json`
- `runtime/state/memory/memory_allocation_gate.json`

验收：

- 高责任/高后悔/关系损伤事件进入高优先候选。
- 低价值边缘信息进入 deep sediment 或短期层。
- 梦境假设默认不是 factual trace。
- `tests/slices/test_state_store.py` 已覆盖三层门的写入、落盘和检查。

### M3. EngramLikeTraceCluster

目标：把 trace、cue、状态和关系边组织成可再激活痕迹簇。

代码：

- 补厚 `engram_index.py`
- 新增 `state_store/engram_cluster.py` 或在 engram index 内分区

输出：

- `engram_clusters`
- `silent_trace_refs`
- `reactivated_trace_refs`
- `trace_cluster_cue_routes`

验收：

- 同一记忆可由语言 cue、关系 cue、身体/情绪 cue、梦境 cue、责任 cue 激活。
- 想不起、不能说、不能行动要能分开表示。

### M4. Pattern Separation / Completion

目标：防止相似关系、相似任务、相似痛苦事件、相似梦境和相似观察混淆；同时支持少量线索补全事件。

代码：

- 新增 `state_store/pattern_separation.py`
- 新增 `state_store/pattern_completion.py`
- 补厚 `memory_retrieval.py`

输出：

- `runtime/state/memory/pattern_separation_index.json`
- `runtime/state/memory/pattern_completion_frame.json`

验收：

- 两个关系主体的偏好不会互相污染。
- 只给一句“还记得那次修复吗”时，能补全相关 episode，但保留置信度和来源。
- 梦境补全必须显示 dream boundary。

### M5. RelationshipMemory / AutobiographicalStack 深化

目标：让关系记忆和自传记忆成为长期人格与真实关系的根。

代码：

- 补厚 `relationship_memory.py`
- 补厚 `autobiographical_stack.py`

新增结构：

- `specific_episode_refs`
- `general_event_threads`
- `life_period_markers`
- `working_self_goal_links`
- `shared_narrative_memory`
- `we_memory_traces`
- `relationship_damage_and_repair_chain`

验收：

- 同一关系的名字、共同术语、边界、损伤、修复、承诺兑现能跨唤醒恢复。
- 语言消费这些记忆，但不播报内部字段。

### M6. Consolidation / Replay / Dream Bridge

目标：第 3 点为第 4 点梦境打基础。退出终端后的梦境要读取 trace store、engram、关系记忆、自传栈，而不是只读聊天日志。

代码：

- 补厚 `replay/*`
- 补厚 `dream/*`
- 补厚 `process_closeout.py`

输出：

- `consolidation_report`
- `dream_replay_plan`
- `dream_fact_gate_decision`
- `wake_integration_frame`
- `reconsolidation_diff`

验收：

- dream residue 能进入下一轮 cue，但不能直接晋升事实记忆。
- replay 后的关系/自传/语义变化必须经过 write gate 和 merge guard。

### M7. Memory Validator / Falsification Guard

目标：记忆系统必须能防止错误长期记忆、过度泛化、梦境污染、关系混淆。

代码：

- 新增或补厚 `state_store/memory_validator.py`
- 补厚 `validators/*` 与 `state_merge_guard.py`

验收：

- fact/hypothesis/dream/counterfactual/relationship inference 明确分区。
- deleted/quarantined/protected trace 不进入 active retrieval。
- 多次纠正形成 contradiction links，而不是覆盖旧历史。

### M8. 语言消费但不硬编码语言

目标：记忆重构结果连同对话者画像、关系、身体、情绪、意识、梦境、认知、内环境、长期/短期记忆和外部观察摘要进入 `response_surface.py` 和 `model_expression.py` 的内部结构化材料，但不能变成代码拼接话术。

代码：

- `memory_retrieval_context_summary(...)`
- `MemoryRetrievalFrame.recall_to_expression_profile`
- `response_surface.py`
- `model_expression.py`

验收：

- 模型输入能看到记忆重构、关系和自传线索。
- 模型输入能看到召回到表达闭合状态、表达边界、报告策略、来源 ref 数、影响家族和再巩固钩子。
- 外显语言不包含 `schema_version`、`runtime/state`、机制清单、固定问句。
- `compose_life_spoken_response(...)` 继续不释放硬编码中文回答。

### M9. Slash inspection 和 20 轮测试准备

目标：为后续第 9 点做证据面。

代码：

- `state_inspection.py`
- `/memory`
- `/relationship`
- `/dream`
- `/context`
- `/state`

验收：

- `/memory` 能显示 trace store、engram cluster、cue activation、pattern separation/completion、write gate、merge guard、dream boundary。
- 这些是检查面，不是外显自然语言。

## 6. 第 3 点完成定义

第 3 点只有同时满足下面条件才可打勾：

1. 本地理论母体中的记忆文档全部被专项矩阵消费。
2. 代码中存在 MemoryTrace 级对象，不只是 refs 聚合。
3. 新经验写入经过事件分割、编码门、分配门、写门和合并门。
4. 检索经过 cue 家族、engram cluster、模式分离/补全和重构焦点。
5. 关系记忆和自传记忆能跨唤醒恢复，并能被语言前结构化材料消费。
6. 梦境/replay 能激活和重构记忆，但不能直接污染事实记忆。
7. 记忆有修正、降级、隔离、保护、遗忘和再激活机制。
8. response surface / model expression 消费记忆，并证明 `recall_to_expression_profile` 已经把存储、召回、报告、表达和再巩固接成闭环，但没有硬编码回答或机制播报。
9. runtime/state、reports、receipts、slash inspection、unit tests 都能证明链路闭合。

## 7. 当前小步状态

在写本计划前，工作区已有一个未提交的小型实验补丁：`memory_retrieval.py` 新增 `cue_activation_profile`，并把它送入 `memory_retrieval_context_summary`、`response_surface` 和 `model_expression_context_summary`。随后又补入 `recall_to_expression_profile`，把记忆激活到语言前结构、报告边界和说后再巩固钩子串起来。它只能算 M4/M8 的局部雏形，不能代表第 3 点完成。

下一步应先执行 M0 记忆专项审计，再决定是否保留、调整或扩展这份小补丁。
