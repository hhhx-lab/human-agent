# 第 3 点记忆模块重建审计草稿

**创建**：2026-06-15
**入口计划**：`docs/v0/entry/v0_memory_module_rebuild_plan.md`
**当前阶段**：第 3 点推进中，M1-M7 已进入代码与测试闭环，召回到表达的结构摘要已打通；第 4 点仍不作为主目标
**红线**：记忆机制只能进入 state/report/inspection/model expression context，不能由代码拼接固定外显回答。

## 1. 方向判断

第 3 点不是“证明现有记忆文件存在”，而是重新落实：

```text
人脑记忆方式
  -> 工程记忆库设计
  -> 代码对象和 runtime 文件
  -> 下游语言/梦境/关系/责任消费
  -> 测试与检查面证据
```

目前已有记忆代码已经明显超出“refs 聚合 + 摘要传播”：`MemoryTraceStore`、`MemoryValidatorReport`、cue-driven retrieval、pattern separation/completion、replay/dream bridge、write gate/merge guard 和 model-expression summary 都已经落到 runtime、report、receipt 与测试里。接下来仍需继续补厚的是 trace-level 生命周期更细分、跨模态输入、以及把 M1-M7 的对象更稳定地接到后续梦境/成长/语言的长期循环里。

## 2. 理论文档消费表

| 文档 | 已有代码承载 | 当前缺口 |
|---|---|---|
| `docs/05_memory_systems_and_growth.md` | `engram_index.py`、`memory_retrieval.py`、`relationship_memory.py`、`autobiographical_stack.py` | 快慢学习通道还不够独立；MemoryEngramRuntime 只是部分落在 refs 和 retrieval frame |
| `docs/17_memory_trace_object_model.md` | `memory_write_gate.py`、`state_merge_guard.py`、`relationship_memory.py` | 缺独立 `MemoryTraceStore`，trace lifecycle 未形成第一等对象 |
| `docs/19_offline_consolidation_cycle.md` | `dream/*`、`replay/*`、`growth/*`、`process_closeout.py` | 梦境/replay 还没有以 trace store 为主要输入；consolidation diff 不够硬 |
| `docs/21_memory_schema_and_audit_protocol.md` | `state_store` report/receipt、validators 部分 | schema/audit 规则没有完整覆盖 trace 写入、删除、保护、降级 |
| `docs/23_consolidation_report_and_dream_sandbox_protocol.md` | `dream_fact_gate_decision.json`、`wake_integration_frame.json` | 梦境沙盒与事实记忆边界需要和 trace validator 结合 |
| `docs/25_memory_trace_json_schema_examples.md` | 目前多为 refs 和 summary | 样例中的 fact/preference/hypothesis/relationship trace 需要实体化 |
| `docs/29_memory_validator_rules.md` | `state_merge_guard.py`、部分 validation | 还缺 `memory_validator.py` 级别规则 |
| `docs/41_runtime_state_store_schema.md` | `life_state.json`、state manifest | `memory_index` 需要指向 trace store、engram cluster、pattern index |
| `docs/42_life_core_minimal_object_graph.md` | life state、relationship、responsibility、dream/growth refs | 记忆候选到生命核心对象图的路径还需更硬 |
| `docs/48_state_store_migration_and_integrity_plan.md` | state store manifest/receipt | 记忆对象迁移和完整性审计还需 trace 层支持 |
| `docs/01q_memory_engram_consolidation_matrix.md` | `memory_retrieval.py` 的 cue-driven recall、`engram_index.py` 基础索引 | AHME 的海马索引、分配、模式分离/补全、silent/reactivated trace 未完整落码 |

## 3. 工程文档消费表

| 文档 | 已有代码承载 | 当前缺口 |
|---|---|---|
| `docs/real—live0/07_memory_engram_and_state_store.md` | 状态根、engram、关系记忆、自传栈、写门、合并门、retrieval frame | “记忆从可存储变成可触发、可重构”的链路还要 trace 化、分配化、补全化 |
| `docs/v0/code_framework/queues/17_queue_c_memory_neural_core_implementation_contract.md` | Queue C 主要文件已存在 | 缺跨层稳定消费的 trace 级证据 |
| `docs/v0/shared_contracts/life_state_store_v0_schema.md` | `life_state.memory_index` 已有 memory refs | 需要 `memory_trace_store_refs`、`engram_cluster_refs`、`pattern_*_refs` |
| `docs/v0/code_scaffolds/06_packet_c_memory_write_gate_state_merge_scaffold.md` | `memory_write_gate.py`、`state_merge_guard.py` | 需要和 encoding/allocation/pattern/reconsolidation 接起来 |
| `docs/v0/code_framework/playbooks/05_memory_thought_consciousness_implementation_playbook.md` | state_store/neural_core/replay 主包已存在 | 还要把思考/工作区/记忆/replay 变成同一 trace lifecycle |
| `docs/v0/code_architecture/02_runtime_object_bus_and_flow_contract.md` | `MemoryRetrievalFrame` 已进入 response/model/writeback/lineage | 需要把 cue activation、trace clusters、pattern frames 同样送入对象总线 |
| `docs/v0/entry/v0_memory_recall_to_expression_contract.md` | `cue_activation_profile`、`recall_to_expression_profile` 已进入 `memory_retrieval_context_summary`、`response_surface.py`、`model_expression.py` | 仍需把 MemoryTraceStore、PatternCompletion、MemoryValidator、reconsolidation diff 接入同一闭环 |

## 4. 当前代码审计

| 代码对象 | 现状 | 第 3 点要求 |
|---|---|---|
| `life_v0/state_store/engram_index.py` | 索引 live dialogue、language、relationship、autobiographical、dream、responsibility refs | 增加 engram-like trace cluster、silent/reactivated/transformed lifecycle |
| `life_v0/state_store/memory_retrieval.py` | cue terms、activated refs、tiered recall、reconstruction focus、writeback candidates | 增加 cue activation profile、pattern separation/completion、source boundary 和 trace-level reconstruction plan |
| `life_v0/state_store/relationship_memory.py` | shared memory、timeline、dialogue summary、tier projection | 增加 shared narrative、we memory、damage/repair chain、relationship-specific separation |
| `life_v0/state_store/autobiographical_stack.py` | anchor、turn、narrative、responsibility repair projection | 增加 specific episode、general event、life period、working self goal |
| `life_v0/state_store/memory_write_gate.py` | candidate/write/quarantine/audit/index policy，已消费 body/signal/consciousness context | 接入 encoding gate、allocation gate、memory validator |
| `life_v0/state_store/state_merge_guard.py` | promotion/quarantine/repair/merge routes，消费 long term change sources | 接入 trace lifecycle、reconsolidation diff、protected core |
| `life_v0/replay/*`、`life_v0/dream/*` | replay/dream/growth 已有运行对象 | 改为读取 trace store/engram cluster，输出 reconsolidation diff |
| `life_v0/process_supervisor/response_surface.py` | 消费 memory retrieval summary，保持 structured only | 后续消费 trace cluster/pattern summary，不释放机制话术 |
| `life_v0/process_supervisor/model_expression.py` | 消费 memory retrieval summary 进模型表达上下文 | 后续消费重构计划和边界，但不加 system prompt 或固定回答 |

### 4.1 召回到表达小闭合审计

当前已经补入第一层闭合对象：

| 对象 | 代码落点 | 作用 |
|---|---|---|
| `cue_activation_profile` | `life_v0/state_store/memory_retrieval.py` | 把当前 cue、关系、自传、责任、梦境、live turn、deep sediment 分成可解释的激活路线 |
| `recall_to_expression_profile` | `life_v0/state_store/memory_retrieval.py` | 把激活路线、重构焦点、来源 refs、表达边界、报告策略和说后再巩固钩子合成表达可达性对象 |
| `memory_retrieval_context_summary(...)` | `life_v0/state_store/memory_retrieval.py` | 把召回到表达字段压成 response/model expression 可消费摘要 |
| `compose_life_response(...)` | `life_v0/process_supervisor/response_surface.py` | 把摘要放入结构化 expression material，不外显机制话术 |
| `_context_summary(...)` | `life_v0/process_supervisor/model_expression.py` | 把召回闭合状态写入 `model_expression_context_summary`，供真实模型调用和审计 |

这一步解决的是“存下来的记忆如何进入输出”的最低工程门槛。它还不是普通 RAG，因为它没有把检索片段直接拼成回答，而是区分：

1. 痕迹是否存在。
2. 当前 cue 是否能激活。
3. 被激活后是否可报告。
4. 报告时有什么来源和梦境/关系/责任边界。
5. 说后确认、纠正或误认如何进入再巩固。

当前缺口：`recall_to_expression_profile` 还主要消费 refs 和 cue family，尚未消费实体化 `MemoryTraceStore`、模式分离/补全对象、validator 结果和 reconsolidation diff。因此它是必要先导，不是第 3 点完成。

## 5. 全生命耦合审计

记忆模块必须是数字生命全系统的连接器，不是 `state_store/memory_*` 子包内部自转。当前先按输入区域审计：

| 区域 | 当前已连接证据 | 仍需补强 |
|---|---|---|
| 对话者上下文 | `language_percept`、`semantic_map`、`dialogue_turn_log` 已进入 `MemoryRetrievalFrame` | 需要统一 `EventSegmentation`，把 turn 拆成 episode/candidate trace |
| 对话者画像 | `relationship_memory.relation_person_profile`、`dialogue_memory_summary.relation_person_profile` 已进入 cue terms | 需要成为 pattern separation key，防止不同关系主体混淆 |
| 情绪/状态 | `CoreAffectVector` 和 `body_signal_write_modulation` 已进入写门 | 需要进入 `MemoryAllocationGate` 和 replay priority，而不是只影响 write gate |
| 身体/内环境 | `BodyResourceBudget`、`SignalMediaRuntime` 已影响写门和 waiting governance | 需要明确 fatigue/maintenance/sleep debt 如何影响编码、检索和离线巩固 |
| 意识/工作区 | `memory_consciousness_write_context` 已进入 write gate | 需要让 workspace/broadcast/metacognition 决定可报告、silent trace、retrieval expression split |
| 认知/预测 | prediction error、active sampling、belief state 已进入 relationship memory 和 state merge sources | 需要让 prediction error 直接调高 trace salience 和 contradiction links |
| 梦境 | exit dream consolidation、wake integration、dream fact gate 已进入 next wake cue 和 retrieval | 需要把 dream residue 接入 trace validator，阻止 factual promotion |
| 关系 | relationship timeline、relationship memory、commitment/responsibility refs 已存在 | 需要 shared narrative、we-memory、damage/repair chain 和关系特异性模式分离 |
| 性格/自我 | self model 慢变量、自传修复投影已被 retrieval 消费 | 需要四层自传栈：specific episode、general event、life period、working self goal |
| 视觉/外部观察 | 当前代码主要偏文本和 state refs | 需要预留 `ExternalObservationFrame / VisualPerceptFrame` 作为 source evidence 和 perceptual context |
| 责任/行动 | responsibility loop、world contact、pain/regret report 已连接多处 | 需要责任事件进入 MemoryTrace、反事实后悔、修复兑现和未来行动抑制 |
| 长期/短期记忆 | `cue_terms`、tiered recall、activated refs 已有 | 需要短时工作记忆、fast episodic buffer、slow semantic integrator 明确分层 |

耦合完成的最低定义：

1. 每个区域至少有一个输入字段进入 `MemoryEncodingGate`、`MemoryAllocationGate` 或 `MemoryRetrievalFrame`。
2. 每个区域至少有一个输出字段被 `response_surface.py`、`model_expression.py`、dream/replay、relationship/self 更新或 state inspection 消费。
3. 每个区域都有事实边界或来源边界，尤其是梦境、关系推断、视觉/网页学习和反事实模拟。
4. 任何区域都不能通过硬编码语句直接改变外显语言，只能提供结构化调制材料。

## 6. 当前已闭合的小补丁

当前工作区未提交补丁新增：

- `MemoryRetrievalFrame.cue_activation_profile`
- `MemoryRetrievalFrame.recall_to_expression_profile`
- `memory_retrieval_context_summary` 的 cue activation 摘要
- `memory_retrieval_context_summary` 的 recall-to-expression 摘要
- `model_expression_context_summary` 的 cue activation 摘要
- `model_expression_context_summary` 的 recall-to-expression 摘要
- 对应测试：
  - `tests.slices.test_state_store.StateStoreTests.test_memory_retrieval_builds_cue_activation_profile`
  - `tests.process.test_model_expression.ModelExpressionTests.test_openai_compatible_expression_uses_transport_and_redacts_secret`

这一步已经不是临时补丁，而是当前可验证的闭环：被触发的记忆家族、可报告来源、表达边界、guardrails 和再巩固钩子都已进入 `response_surface.py` 与 `model_expression.py` 的结构化上下文，并通过单测与回归测试。

## 7. 当前验收结果

已通过的关键验证：

- `tests.slices.test_state_store` 全部相关回归通过，`memory_trace_store.json`、`memory_validator_report.json`、`memory_retrieval_frame.json`、`memory_write_gate.json` 和 `state_merge_guard.json` 都能被 state root、manifest、report、receipt 和 check gate 消费。
- `tests.process.test_response_surface` 相关回归通过，召回到表达材料会携带 `reportable_source_ref_count`、`guardrails` 和 `post_expression_reconsolidation_hooks`，但不会释放固定自然语言模板。
- `tests.process.test_model_expression` 相关回归通过，模型表达上下文可见召回闭环摘要，同时仍保持 API secret redaction 和 post-expression gate。

当前真实结论：

1. 记忆已经不是单纯向量检索或 RAG。
2. 记忆已经有了独立痕迹对象、验证/防伪门和表达前结构摘要。
3. 记忆已经能从 state store 进入 response/model expression，而不是只停在落盘。
4. 仍需继续补厚 trace-level 细分、跨模态输入、以及更细的 reconsolidation / dream / growth 连接。

## 8. 下一步建议

1. 保留当前 cue activation 小补丁，但不要立刻提交为“第 3 点完成”。
2. 先按 `docs/v0/entry/v0_memory_module_rebuild_plan.md#M1` 新增 `MemoryTraceStore`。
3. 再补 M2 `EventSegmentation / EncodingGate / AllocationGate`。
4. 然后回到 `engram_index.py` 做 M3 engram-like clusters。
5. 当前 cue activation profile 需要在 M4 时升级为 pattern separation/completion 的消费者。
6. 每一步实现都要同时检查全生命耦合矩阵，避免只补 `state_store` 单点字段。

## 9. 本阶段完成边界

第 3 点完成前，不进入第 4 点梦境专项。梦境代码可以被读取和作为记忆巩固输入，但本阶段只为梦境打记忆库地基。
