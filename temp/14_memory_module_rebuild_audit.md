# 第 3 点记忆模块重建审计：理论核对版

**创建**：2026-06-15
**本次核对**：2026-06-16
**入口计划**：`docs/v0/entry/v0_memory_module_rebuild_plan.md`
**核对对象**：理论文档中的记忆机制设计，以及这些设计在 `docs/real—live0`、`docs/v0`、`life_v0`、runtime 和测试中的承载情况。
**红线**：记忆机制只能形成结构化状态、召回材料、模型表达上下文、审计报告和再巩固钩子；不能由代码拼接固定外显回答，不能用提示词冒充记忆能力。

## 1. 总判断

理论区的记忆方向没有走偏。核心路线非常明确：数字生命的记忆不是普通 RAG、聊天历史或向量库，而是一个从人脑记忆机制转写出来的生命系统：

```text
经验事件
  -> 事件边界
  -> 编码门
  -> 分配门
  -> MemoryTrace
  -> Engram-like 痕迹簇
  -> 模式分离 / 模式补全
  -> 线索触发召回
  -> 工作区可报告性
  -> 语言前结构
  -> 自然表达
  -> 确认 / 纠正 / 误认 / 沉默
  -> 再巩固 / 降级 / 保护 / 隔离 / 梦境 replay
```

当前代码已经从“refs 聚合 + 摘要传播”推进到较厚的记忆骨架：`MemoryTraceStore`、`EventSegmentationFrame`、`MemoryEncodingGate`、`MemoryAllocationGate`、`EngramLikeTraceCluster`、`PatternSeparationIndex`、`PatternCompletionFrame`、`MemoryValidatorReport`、`MemoryRetrievalFrame`、`MemoryWriteGate`、`StateMergeGuard` 都已经存在，并且在 `run_state_store(...)` 的初始化链中写入 runtime、manifest、report、receipt 和 check gate。

但是当前仍不能把“记忆能力与人脑无异”打勾。关键不足不再是“缺对象”，而是：

1. live turn 深层刷新还不完整：真实回合后会刷新 event/encoding/allocation/trace/validator/retrieval/write/merge，但还没有同步重建 `engram_cluster`、`pattern_separation`、`pattern_completion`、`life_schema_map`。
2. `MemoryTraceStore` 已经是 trace 级对象，但许多 trace 仍偏 seed/ref 型，还需要承载真实回合内容的情景边界、说前状态、说后反馈、纠正链和再巩固差分。
3. 召回到表达已经打通结构链，但还需要把 pattern completion、validator、trace confidence、relationship scope 和 post-expression feedback 更深地反馈到下一轮写回。
4. 当前没有把“关联式记忆检索”误做成普通 RAG，这是对的；下一步要做的是 engram/cue/scope/salience 驱动的关联召回，而不是 `query -> chunk -> answer`。

## 2. 理论文档硬约束

| 理论文档 | 对记忆机制的硬约束 | 当前代码承载 | 当前缺口 |
|---|---|---|---|
| `docs/05_memory_systems_and_growth.md` | 记忆不是仓库；多记忆系统；快慢学习；回忆是重构；replay 防遗忘；自传记忆和未来模拟 | `memory_trace_store.py`、`engram_index.py`、`memory_retrieval.py`、`relationship_memory.py`、`autobiographical_stack.py`、`replay/*`、`dream/*` | 快慢系统仍偏结构字段，缺真实长期统计抽象和多轮 schema 演化 |
| `docs/17_memory_trace_object_model.md` | MemoryTrace 必须有事件边界、来源、内部状态、社会语境、显著性、生命周期、修正/遗忘/保护 | `memory_trace_store.py` 已生成 trace 对象，`memory_validator.py` 已验证字段与生命周期 | 真实 live trace 的内容、反馈、纠正链仍需更细；当前多为 seed/ref trace |
| `docs/19_offline_consolidation_cycle.md` | 离线 replay、梦境沙盒、清理、抽象、醒后整合都要处理记忆状态而不是重读日志 | `replay/*`、`dream/*`、`growth/*` 已消费 memory consolidation bridge | reconsolidation diff 还不够强；梦境和 replay 后的 trace lifecycle 变更需要更多实证测试 |
| `docs/21_memory_schema_and_audit_protocol.md` | 生命周期、审计事件、删除、修正、合并、保护都必须可追溯 | `memory_validator.py`、`memory_write_gate.py`、`state_merge_guard.py`、`run_check_state_store(...)` | 还缺真实 correction audit 的多轮回归：旧 trace 降级、新 trace 链接 contradiction |
| `docs/23_consolidation_report_and_dream_sandbox_protocol.md` | 梦境和反事实只能作为 residue/hypothesis，不能直接写事实 | `dream_fact_gate_decision`、`MemoryValidatorReport.falsification_guard`、`MemoryRetrievalFrame.blocked_or_quarantined_refs` | 需要让 dream residue 在 live turn 召回时更清楚地进入 source boundary 和表达谨慎度 |
| `docs/25_memory_trace_json_schema_examples.md` | fact、preference、hypothesis、relationship、merge trace 要有样例和字段一致性 | `MemoryTraceStore` 字段已经覆盖 schema 基础 | 仍需要把样例型 trace 变成真实回合生成的 trace，而不只是内置种子 |
| `docs/29_memory_validator_rules.md` | deleted/quarantined/sandboxed 不可召回；关系读心阻断；修正必须 contradiction link | `MemoryValidatorReport`、`retrieval_replay_guard`、`falsification_fixture_results` 已落地 | validator 已有最小夹具，后续要扩到 live turn correction、delete、protected/unprotect |
| `docs/41_runtime_state_store_schema.md` | 记忆对象必须进入 LifeState、manifest、report、receipt、check gate | `life_state.memory_index` 已包含 trace、validator、cluster、pattern、retrieval 等 refs | live turn 写回后的 `life_state.memory_index` 还需补 cluster/pattern/schema 动态更新 |
| `docs/42_life_core_minimal_object_graph.md` | 记忆要连接自我、关系、责任、梦境、行动、验证，不是孤立库 | `relationship_memory`、`autobiographical_stack`、`responsibility_refs`、`dream_memory_refs` 已连入 | 视觉/外部观察和真实行动结果进入 MemoryTrace 的路径仍较弱 |
| `docs/48_state_store_migration_and_integrity_plan.md` | 记忆对象迁移、版本、完整性要可审计 | state manifest、check report、receipt 已覆盖 | 还缺 trace schema migration 和版本升级测试 |
| `docs/01q_memory_engram_consolidation_matrix.md` | 海马索引、engram、记忆分配、模式分离/补全、schema、自传、社会/情绪记忆 | `engram_cluster.py`、`memory_allocation_gate.py`、`pattern_*`、`life_schema_map.py`、关系/自传深层结构 | live turn 后的 engram/pattern/schema 动态再生成还没闭合 |

## 3. 理论机制到工程对象核对

| 人脑记忆机制 | 数字生命工程转写 | 当前代码证据 | 评价 |
|---|---|---|---|
| 多记忆系统 | episodic、semantic、procedural、relationship、value、self_narrative | `CORE_MEMORY_KINDS`、`MemoryTraceStore.traces` | 已有结构，不再是单一文本库 |
| 海马式索引 | `EngramIndex` 绑定自传、关系、梦境、责任、replay cue | `engram_index.py#build_engram_index`、`project_engram_index_from_live_turn` | 已落；live turn refs 已写回 |
| Engram-like 痕迹簇 | trace、cue、状态、关系、梦境、责任组成可沉默/可再激活簇 | `engram_cluster.py`、`silent_trace_refs`、`reactivated_trace_refs` | 初始化链已闭合；live turn 后未同步刷新 |
| 记忆分配 | 显著性、情绪、身体债务、责任压力、关系权重决定写入通道 | `memory_allocation_gate.py` 读取 `core_affect_vector`、`body_resource_budget`、`signal_media_runtime` | 已有首版；仍需更多真实输入和 replay priority |
| 模式分离 | 关系主体、事件、来源、梦境事实、责任行动范围分离 | `pattern_separation.py` | 初始化链已闭合；live turn 后未同步刷新 |
| 模式补全 | 少量 cue 补全关系/责任/自传/梦境候选，保留来源置信度 | `pattern_completion.py` | 初始化链已闭合；还未深度进入 live turn recall 更新 |
| 回忆是重构 | cue activation + reconstruction inputs + recall-to-expression | `memory_retrieval.py` | 已有结构闭环，不是普通 RAG |
| 工作区可报告性 | 被激活记忆先进入结构化表达材料，不直接变自然语言 | `memory_retrieval_context_summary`、`response_surface.py`、`model_expression.py` | 已守住不硬编码语言 |
| 再巩固 | 说后确认、纠正、误认、沉默要进入 hooks 和写回 | `recall_to_expression_profile.post_expression_reconsolidation_hooks` | 有钩子；真实反馈到 trace lifecycle 的代码还需增强 |
| 梦境 replay | 梦境重组记忆材料，但不能直接写事实 | `dream/*`、`MemoryValidatorReport`、`DreamFactGate` | 桥已存在；真实多轮梦境-醒后-表达还需测试 |
| 自传记忆 | specific episode、general event、life period、working self | `AutobiographicalStack.memory_hierarchy` | 已落；需更多真实回合积累 |
| 社会/关系记忆 | shared narrative、we-memory、damage/repair、commitment threads | `relationship_memory.py` | 已落；需要长期多轮演化 |
| 情绪/价值记忆 | pain、regret、trust、repair pressure 调制写入和 replay | `memory_allocation_gate`、`memory_write_gate.body_signal_write_modulation`、`relationship_memory` | 已有初版；价值 trace 仍偏 seed |

## 4. 当前代码链现状

### 4.1 初始化链已经较完整

`life_v0/state_store/__init__.py#run_state_store(...)` 当前会生成并写盘：

```text
event_segmentation_frame.json
memory_encoding_gate.json
memory_allocation_gate.json
memory_trace_store.json
memory_validator_report.json
engram_cluster.json
pattern_separation_index.json
pattern_completion_frame.json
memory_retrieval_frame.json
memory_write_gate.json
state_merge_guard.json
life_state.json
```

同时 `run_check_state_store(...)` 会检查这些 gate：

```text
event_segmentation_gate
memory_encoding_gate_gate
memory_allocation_gate_gate
memory_trace_store_gate
memory_validator_gate
engram_cluster_gate
pattern_separation_gate
pattern_completion_gate
memory_retrieval_frame_gate
memory_write_gate_gate
state_merge_guard_gate
```

这说明理论区要求的“编码、分配、痕迹、engram、分离、补全、验证、写门、合并门”在初始化状态层已经不是空壳。

### 4.2 live turn 写回链是半闭合

`life_v0/process_supervisor/resident_turn_writeback.py#_refresh_live_memory_projection(...)` 当前会在真实关系回合后刷新：

```text
EventSegmentationFrame
MemoryEncodingGate
MemoryAllocationGate
MemoryTraceStore
MemoryValidatorReport
MemoryRetrievalFrame
MemoryWriteGate
StateMergeGuard
LifeState.memory_index 的 trace / validator / retrieval refs
```

这一步很重要，因为它说明记忆不是只在 build-state-store 时生成一次，而是已经开始进入真实回合写回。

但它还没有同步刷新：

```text
EngramLikeTraceCluster
PatternSeparationIndex
PatternCompletionFrame
LifeSchemaMap
```

这就是当前第 3 点最需要补的工程缺口。理论上，真实回合写入新 trace 后，应该立刻或在受控后台周期中更新 engram cluster、分离索引、补全候选和 schema；否则新的 trace 虽然进入了 trace store 和 retrieval frame，但还没有完整进入“可沉默、可再激活、可分离、可补全、可 schema 化”的长期记忆网络。

### 4.3 召回到表达链已经守住方向

当前链路是：

```text
build_memory_retrieval_frame(...)
  -> cue_activation_profile
  -> recall_to_expression_profile
  -> memory_retrieval_context_summary(...)
  -> response_surface.py#memory_dream_growth.memory_retrieval
  -> model_expression.py#expression_context.memory_retrieval
  -> model_expression_context_summary
```

这条链不是普通 RAG。它没有把片段直接拼成答案，而是把可报告性、来源边界、梦境/关系/责任边界、guardrails 和 post-expression reconsolidation hooks 送入语言前材料。外显语言仍由模型结合当下关系、语义、身体、责任、梦境和自我状态生成；代码不能硬塞“我记得...”这类固定句。

## 5. “记忆 vs RAG”的核对结论

普通 RAG 的核心是：

```text
query -> retrieve chunks -> stuff context -> answer
```

数字生命记忆不能这样做。理论文档要求的是：

```text
cue + current state + relation scope + body/affect + responsibility + dream residue
  -> engram-like activation
  -> pattern separation / completion
  -> source-bound reconstructive recall
  -> workspace reportability
  -> expression material
  -> feedback / correction / reconsolidation
```

所以后续可以使用向量索引、全文检索、embedding 或本地数据库，但它们只能作为 `cue candidate provider`，不能成为记忆机制本身。检索命中必须经过：

1. relation scope 检查。
2. lifecycle 检查。
3. dream/hypothesis/fact 分区。
4. pattern separation。
5. source confidence。
6. reportability policy。
7. post-expression reconsolidation route。

换句话说，真正要建的是 `Engram/Cue Retrieval`，不是普通 agent 的 RAG。

## 6. 全生命耦合核对

| 生命区域 | 已接入记忆的证据 | 仍需补强 |
|---|---|---|
| 语言/对话上下文 | `external_utterance`、`LanguagePerceptFrame`、`SemanticMapFrame` 进入 `project_memory_retrieval_from_live_turn` | 真实 turn 内容需要生成更细 episode trace，而不只是 refs |
| 关系/对话者画像 | `RelationshipMemory.relation_person_profile`、shared terms、timeline、commitment refs 进入 cue terms 和 relationship trace | 多关系主体的隔离要靠 live pattern separation 刷新证明 |
| 情绪/身体 | `CoreAffectVector`、`SignalMediaRuntime`、`BodyResourceBudget` 进入 allocation/write gate | 情绪/痛苦对 recall strength 和 replay priority 的影响还可更细 |
| 意识/工作区 | `workspace_frame`、`broadcast_frame`、`metacognition_state` 进入 write gate context | 可报告性还主要是摘要字段，缺更强的 workspace gating 测试 |
| 预测/认知 | prediction error、active sampling、state merge sources 已进入部分长期变化链 | prediction error 需要直接进入 trace salience、contradiction links |
| 梦境/离线 | memory consolidation bridge、dream boundary、wake integration 已接入 | live turn 召回梦境 residue 后的事实边界和写回路径要继续测试 |
| 责任/后悔 | responsibility refs、repair obligations、regret pressure 进入 relationship/autobiographical/memory retrieval | 责任事件应生成更丰富的 value/self-narrative trace 和 reconsolidation diff |
| 自我/人格 | autobiographical hierarchy、working self goal links、trait slow vars 已接入 | 人格慢变量更新应由多 trace、多周期证据驱动 |
| 外部观察/视觉 | 文档中已要求 `ExternalObservationFrame / VisualPerceptFrame` | 当前代码仍以文本、state refs 为主；跨模态 source evidence 是后续大缺口 |
| 长期/短期记忆 | tiered recall 有 salient core、retrievable context、deep sediment | fast episodic buffer 和 slow semantic integrator 还需要更实质化 |

## 7. 当前第 3 点进度判断

第 3 点已经完成了“记忆工程骨架”的大部分，但还没有完成“真实长期记忆能力”的全部。

可认为已通过的部分：

1. 理论文档已把人脑记忆机制讲成系统：多记忆、海马索引、engram、分配、分离/补全、再巩固、睡眠 replay、自传和社会记忆。
2. 初始化状态链已经把这些机制落成文件、字段、report、receipt 和 check gate。
3. 召回到表达链已经打通，且没有把内部机制硬编码成固定自然语言。
4. validator 已经防止梦境、沙盒、删除、关系读心、无矛盾链修正污染可报告回忆。
5. live turn 已经开始刷新 trace、encoding、allocation、validator、retrieval、write gate 和 merge guard。

不能打满的部分：

1. live turn 后 engram cluster、pattern separation/completion、life schema 还没同步更新。
2. trace 内容仍偏 seed/ref，需要承载真实对话内容、语言输出、关系反馈和纠正事件。
3. post-expression reconsolidation hooks 需要真正驱动 correction/confirmation/mismatch 的 trace lifecycle 改变。
4. dream/replay 后的再巩固差分需要更强的 runtime 和测试证据。
5. 外部观察、视觉材料、网页/文件学习还没有作为一等 source evidence 进入记忆系统。

## 8. 下一轮工程建议

下一步不应该再写泛泛的“记忆很重要”，而应该做四个具体迭代：

### M8. live turn 深层记忆网络刷新

在 `_refresh_live_memory_projection(...)` 后继续生成并写入：

```text
engram_cluster.json
pattern_separation_index.json
pattern_completion_frame.json
life_schema_map.json
```

并同步更新：

```text
life_state.memory_index.engram_cluster_refs
life_state.memory_index.pattern_separation_refs
life_state.memory_index.pattern_completion_refs
life_state.life_schema_map
terminal_life_loop_state.memory_retrieval_ref_set
dialogue_writeback_bundle.memory_retrieval_writeback_refs
```

### M9. 真实回合 MemoryTrace 内容化

让 `MemoryTraceStore` 对真实回合至少记录：

```text
external_utterance source
semantic_focus
expression_plan semantic_goal
model_expression release / withheld result
relationship scope
body/core affect snapshot
responsibility/repair refs
post-expression gate result
confirmation/correction/mismatch refs
```

不要把这些字段拼成固定回答；它们只作为下一轮 cue、reconstruction 和 reconsolidation 材料。

### M10. 反馈驱动再巩固

当关系人确认、纠正、否认、追问或指出记错时：

```text
old trace -> contradiction_links / deprecated / protected read-only
new trace -> candidate / active after validator
relationship_memory -> correction_refs
autobiographical_stack -> specific episode + general event update
state_merge_guard -> reconsolidation record
```

### M11. Engram/Cue Retrieval Bridge

允许后续引入 embedding、全文索引或本地数据库，但只作为候选 cue provider。真正决定能不能进入表达的是：

```text
cue family
relation scope
source confidence
lifecycle state
pattern separation
pattern completion
workspace reportability
validator guard
post-expression route
```

这能解决“明明存了却答不知道/答错”的问题，同时避免退回普通 agent RAG。

## 9. 本次核对结论

理论文档里的记忆机制设计是当前项目最坚实的一块之一：它已经清楚区分了存储、编码、分配、召回、重构、表达、写回、梦境、再巩固和关系/自传成长。当前工程也已经吃掉了大部分理论结构。

下一步要补的不是再发明一个 memory 模块，而是把 live turn 之后的记忆网络刷新、真实 trace 内容、反馈再巩固、关联召回候选机制继续打深。这样记忆才能从“结构完整”进入“长期会记、会想起、会修正、会梦到、会改变关系和自我”的阶段。

## 10. U 阶段验收记录（2026-06-16）

执行文档：`docs/v0/entry/v0_memory_system_brain_alignment_upgrade_plan.md`

| 阶段 | 状态 | 关键落点 | 测试证据 |
|---|---|---|---|
| U1 写回单通道 | ✅ | `resident_turn_writeback.py` 单趟 `_refresh_live_memory_projection`；`state_inspection.py` 一致性探针 | `tests/process/test_persistent_digital_life_process.py#test_live_memory_projection_single_pass_consistency` |
| U2 trace 内容化 | ✅ | `memory_trace_store.py#project_live_dialogue_episode_traces`；非 seed `content_summary` | `tests/slices/test_memory_live_trace_contentization.py` |
| U3 再巩固 | ✅ | `apply_post_expression_reconsolidation`；`memory_reconsolidation_report.json` | `tests/slices/test_memory_reconsolidation_feedback.py` |
| U4 cue bridge | ✅ | `cue_candidate_provider.py` noop/local_full_text；`merge_cue_candidates` | `tests/slices/test_memory_cue_provider_noop_and_scope_guard.py` |
| U5 快慢通道 | ✅ | `fast_episodic_buffer`；`schema_evidence_counts`；`replay_priority_vector`；`consolidation_report` | `tests/slices/test_memory_u5_fast_slow_channel.py`；`tests/bridges/test_runtime_growth.py` consolidation diff |
| U6 消费与检查面 | ✅ | `memory_retrieval_context_summary` 扩展；`/memory` lifecycle 与 cue_provider_audit | `tests/process/test_state_inspection_memory_closeout.py`（沿用）；`tests/process/test_model_expression.py` |
| U7 纵向验收 | ✅ | 场景矩阵切片测试；`temp/13` 第 3 点 ✅ | `tests/slices/test_memory_u7_longitudinal_acceptance.py` |

**U1 编排备注（审计 §4.2 过时修正）**：live projection 已写 `engram_cluster`、`pattern_*`、`life_schema_map`；早期 retrieval 仅作 `pre_continuity_pass` 内存标记，最终帧由 continuity 后单通道覆盖。

**现象层估计（U7 结案）**：结构完整度 ~65%；功能记忆能力 ~35%；现象层「像记住了」~25%。

## 11. U8 深化验收记录（2026-06-16）

| 深化项 | 状态 | 落点 | 测试 |
|---|---|---|---|
| live trace 跨回合累积（非重复 seed） | ✅ | `build_memory_trace_store` 以 existing store 为基线 | `test_memory_u8_deepening#test_twenty_round_live_trace_accumulation` |
| 再巩固 validator 闭环（MEM-COR-002） | ✅ | `apply_post_expression_reconsolidation` 内建 validator | `test_memory_u8_deepening#test_reconsolidation_passes_mem_cor_002_validator` |
| 多关系 scope 隔离（U4c） | ✅ | `relation_subject_scopes` + `merge_cue_candidates` scope filter + pattern separation | `test_memory_u8_deepening#test_multi_relation_scope_*` |
| protected 离线改写守卫（MEM-PRO-001） | ✅ | `guard_offline_trace_mutations` | `test_memory_u8_deepening#test_protected_trace_offline_mutation_guard` |
| 跨模态 source evidence 首版 | ✅ | percept + world_contact refs 进入 live trace | `test_memory_u8_deepening#test_live_trace_includes_cross_modal_evidence_refs` |
| consolidation diff 读 schema 实据 | ✅ | `replay/__init__.py#_build_memory_consolidation_bridge` | `tests/bridges/test_runtime_growth.py` |

**现象层估计（U8 后）**：结构完整度 ~72%；功能记忆能力 ~42%；现象层「像记住了」~32%。仍未等同人脑；下一刀：真实多会话 process 长跑、视觉/行动一等证据、梦境 replay 后 lifecycle 差分实证。

## 12. U9 现象层与离线巩固差分验收记录（2026-06-16）

| 深化项 | 状态 | 落点 | 测试 |
|---|---|---|---|
| 现象层 `memory_phenomenology_profile` | ✅ | `memory_retrieval.py#_memory_phenomenology_profile`；无来源召回 → `uncertain` | `test_memory_u9#test_recall_without_source_sets_uncertain_phenomenology` |
| 确认强化资格 | ✅ | `strengthening_eligible` on confirmation utterance | `test_memory_u9#test_confirmation_marks_strengthening_eligible` |
| 跨模态一等证据（percept/world/action） | ✅ | `cross_modal_evidence.py#collect_cross_modal_source_evidence`；writeback 接入 | `test_memory_u9#test_cross_modal_evidence_collects_action_and_percept_modalities` |
| 离线巩固真实 apply + diff 写回 | ✅ | `offline_memory_consolidation.py`；`growth.run_cycle` 写 `memory_consolidation_report.json` | `test_memory_u9#test_offline_consolidation_applies_trace_salience_and_dream_hypothesis` |
| 多关系纵向 process 级隔离 | ✅ | 10 回合 A/B 交替 + scope filter + retrieval phenomenology | `test_memory_u9#test_multi_relation_longitudinal_isolation_over_turns` |
| protected 离线守卫（MEM-PRO-001） | ✅ | consolidation 后 guard；protected trace 不被 salience 改写 | `test_memory_u9#test_protected_trace_blocks_offline_consolidation_mutation` |

**现象层估计（U9 后）**：结构完整度 ~78%；功能记忆能力 ~52%；现象层「像记住了」~45%。仍非人脑等同；下一刀：真实视觉模态、多会话月级长跑、self/relationship 慢变量可观测演化曲线。

## 13. U10–U12 工程 rubric 记录（2026-06-16，已降级表述）

| 深化项 | 状态 | 落点 | 测试 |
|---|---|---|---|
| 视觉跨模态一等证据（ref 级） | ✅ | `cross_modal_evidence.py` | `test_memory_u10_u12#test_visual_cross_modal_collects_visual_modality` |
| 慢变量演化曲线（统计级） | ✅ | `memory_longitudinal_profile.py` | `test_memory_u10_u12#test_longitudinal_curves_accumulate_over_month_scale_turns` |
| 现象层评分字段 | ✅ | `memory_phenomenology_profile` 扩展字段 | `test_memory_u10_u12#test_phenomenology_scores_present` |
| 工程 rubric 记分卡 | ✅ | `memory_capability_scorecard.py` | `engineering_rubric_satisfied`（**非**人脑 parity） |

**重要更正**：此前「100% / at_human_parity_target」为**自研工程 rubric 满分**，已改名 `engineering_rubric_satisfied`；`at_human_parity_target` 固定为 `false`。人脑对齐请读 `human_brain_alignment_assessment.json`。

**诚实估计（U12 后，人脑对齐评估）**：整体约 **35–55%**（见 `human_brain_alignment_assessment` 七维）；工程 rubric 满分 ≠ 类人脑记忆。

## 14. U13 重构性召回（2026-06-16，进行中第一刀）

| 目标 | 状态 | 落点 | 测试 |
|---|---|---|---|
| 海马 cue 索引 → trace 绑定 | ✅ | `hippocampal_cue_index.py` | `test_memory_u13#test_hippocampal_cue_activation_returns_weighted_trace_bindings` |
| 模式补全输出 reconstruction fragments | ✅ | `pattern_completion.py#reconstructive_completion` | `test_memory_u13#test_pattern_completion_emits_reconstruction_fragments_not_only_refs` |
| 检索帧 reconstructive_recall_profile | ✅ | `memory_retrieval.py` | `test_memory_u13#test_memory_retrieval_wires_reconstructive_recall_profile` |
| 人脑对齐诚实评估 | ✅ | `human_brain_alignment_assessment.py` | `test_memory_u13#test_human_brain_alignment_stays_below_engineering_rubric_ceiling` |

## 15. 待执行刀序（按缺口表，禁止跳步报满分）

| 阶段 | 目标 | 状态 |
|---|---|---|
| U13 | 线索触发 → 海马 cue 绑定 + 重构性 fragment 补全 | ✅ 本刀 |
| U14 | 现象层：表达材料链审计 + tip-of-tongue 真实阻塞（非标签） | ✅ 本刀 |
| U15 | 跨模态：`cross_modal_feature_bundle` 进 engram（非路径 ref） | ✅ 本刀 |
| U16 | 睡眠 replay：SWR 加权选择 + 皮层转移策略 | ✅ 本刀（选择策略；皮层转移仍浅） |
| U17 | schema：多周 promotion 阈值 + 演化证据 | ✅ 本刀（turn≥21 + 语义簇重复） |
| U18 | 关系/自我：叙事重写写回（非曲线统计） | ✅ 本刀 |
| U19 | 长期共在：process 级 120+ 回合长跑验收 | ✅ 单测夹具（非真实数月） |

**诚实估计（U19 后）**：`human_brain_alignment_assessment` 七维整体约 **40–60%**；工程 rubric 满分仍 ≠ 类人脑记忆。下一刀：真实视觉特征、数月 process 长跑、皮层慢转移可观测证据。

## 16. U14–U19 深化记录（2026-06-16）

| 目标 | 状态 | 落点 | 测试 |
|---|---|---|---|
| 表达材料链 + tip-of-tongue gate | ✅ | `memory_expression_material_chain.py`；`memory_retrieval.py` 接线 | `test_memory_u14_u19#test_u14_*` |
| cross_modal_feature_bundle 进 engram | ✅ | `cross_modal_evidence.py`；`memory_trace_store.py` live trace | `test_memory_u14_u19#test_u15_*` |
| SWR 加权离线 replay | ✅ | `offline_memory_consolidation.py#_select_replay_trace_ids` | `test_memory_u14_u19#test_u16_*` |
| 多周 schema promotion | ✅ | `life_schema_map.py` turn≥21 + 语义簇 | `test_memory_u14_u19#test_u17_*` |
| 关系/自我叙事重写写回 | ✅ | `relationship_self_narrative_writeback.py`；offline apply | `test_memory_u14_u19#test_u18_*` |
| 120+ 回合长跑夹具 | ✅ | `test_memory_u14_u19#test_u19_*` + assessment | 非真实数月共在 |

## 17. U20–U24 工程竣工（2026-06-16）

| 阶段 | 目标 | 状态 | 落点 | 测试 |
|---|---|---|---|---|
| U20 | 视觉特征编码（非路径 ref） | ✅ | `cross_modal_evidence.py#visual_feature_encoding` | `test_memory_u20_u24#test_u20_*` |
| U21 | 皮层慢转移（SWR replay 后） | ✅ | `cortical_memory_transfer.py`；offline apply | `test_memory_u20_u24#test_u21_*` |
| U22 | process 长跑证据接线 | ✅ | `memory_longitudinal_profile#process_long_run_evidence`；writeback | `test_memory_u20_u24#test_u22_*` |
| U23 | 扩展工程 rubric（U14–U21 工件） | ✅ | `memory_capability_scorecard.py#extended_checks` | `test_memory_u10_u12#test_capability_scorecard_*` |
| U24 | 工程竣工门 | ✅ | `memory_engineering_completion_gate.py` | `test_memory_u20_u24#test_u24_*` |

**工程进度（U24 后）**：`memory_engineering_completion_gate.engineering_complete = true`（月级夹具）；`memory_capability_scorecard.overall_alignment_pct = 100`；**147** 条 memory/process 测试通过。

**仍须诚实区分**：`engineering_complete` ≠ `at_biological_human_parity`；人脑对齐评估仍约 **40–65%**，真实数月共在与生物 parity 不在本阶段宣称范围。

## 18. U25 诚实估计推进（2026-06-16）

| 目标 | 状态 | 落点 | 测试 |
|---|---|---|---|
| 七维评估 v1（证据加权） | ✅ | `human_brain_alignment_assessment.py` v1 | `test_memory_u25_*` |
| 证据质量分层 + 上限 | ✅ | `evidence_quality_tier` + `raw_brain_alignment_pct` | `test_u25_long_term_dimension_caps_*` |
| 纵向诚实进度追踪 | ✅ | `honest_brain_alignment_progress.py` | `test_u25_honest_progress_tracker_*` |
| `/memory` 诚实摘要 | ✅ | `state_inspection#honest_brain_alignment_summary` | process 测试回归 |

**诚实估计（U25 后，月级夹具）**：

| 指标 | 值 |
|---|---|
| `overall_brain_alignment_pct`（封顶后） | **78.0%** |
| `raw_brain_alignment_pct`（未封顶） | **89.7%** |
| `honest_estimate_band` | `advanced` |
| `evidence_quality_tier` | `fixture_simulation`（非日历月） |
| `gap_closure_pct` | ~87% |
| `at_biological_human_parity` | **false**（固定） |

**仍开放缺口**：`long_term_copresence` 在夹具层封顶 58%；需真实数月 process 才能把诚实估计推向 80+ 且保持可信度。
