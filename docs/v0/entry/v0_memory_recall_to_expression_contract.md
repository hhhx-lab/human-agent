# V0 Memory Recall To Expression Contract

本文档是第 3 点记忆模块重建的专项合同：记忆不能只证明“已经存下”，还必须证明“在被问到、被触发、被关系/身体/梦境/责任状态调制时，能够进入语言前结构，支撑回答，并在说错、被纠正、被确认后重新巩固”。

这不是普通 agent RAG。普通 RAG 多数是“查询 -> 相似片段 -> 拼进上下文”；数字生命的记忆闭环必须是：

```text
Experience / Trace
  -> Encoding / Allocation / WriteGate
  -> Engram-like cue routes
  -> CueTriggeredReactivation
  -> PatternSeparation / PatternCompletion
  -> Workspace reportability
  -> Language prestructure
  -> Spoken / withheld / uncertain expression
  -> Correction / confirmation / mismatch
  -> Reconsolidation / contradiction / strengthening / downgrade
```

## 1. 脑科学约束

本合同直接继承：

- `docs/05_memory_systems_and_growth.md`：回忆是重构，不是读取；状态触发由语义、情境、目标、情绪/价值和内感受共同决定。
- `docs/17_memory_trace_object_model.md`：检索不只靠相似度，必须进入工作区，不能直接驱动行动。
- `docs/21_memory_schema_and_audit_protocol.md`：active/deprecated/deleted/protected 等生命周期决定是否可召回。
- `docs/29_memory_validator_rules.md`：deleted/quarantined/dream/hypothesis/fact 的边界决定能不能进入表达。
- `docs/01q_memory_engram_consolidation_matrix.md`：AHME003 海马索引、AHME011-AHME016 engram、AHME023-AHME025 模式分离/补全、AHME033 自传记忆、AHME035-AHME038 情绪和社会记忆。

关键转写：

| 生物机制 | 工程对象 | 对输出的约束 |
|---|---|---|
| 海马索引 | `HippocampalIndexRef` / `EngramIndex` | 只存片段不够；必须能把语言、关系、身体、梦境和责任线索补成事件整体 |
| Engram 重激活 | `CueTriggeredReactivation` / `cue_activation_profile` | 记忆存在、可检索、可报告、可行动要分开 |
| 前额叶-工作区控制 | `WorkspaceFrame` / `reportability_policy` | 被激活的记忆先进入语言前结构，不直接变成硬编码回答 |
| 模式分离 | `PatternSeparationIndex` | 相似关系人、相似承诺、相似痛苦不能混淆 |
| 模式补全 | `PatternCompletionFrame` | 少量线索可补全事件，但必须保留来源和置信度 |
| 再巩固 | `post_expression_reconsolidation_hooks` | 回答后的确认、纠正、误认、沉默都要影响后续记忆 |

## 2. 真正记住的工程定义

一条记忆只有同时满足下面条件，才算 live0 中“真正被记住”：

1. 有可审计来源：`source_refs`、关系来源、外部观察或运行日志可追溯。
2. 有事件边界：不是裸文本片段，而是连接当时语言、关系、身体、意识、行动和时间。
3. 有写入状态：candidate、active、protected、deprecated、quarantined、deleted、silent、reactivated 之一。
4. 有线索入口：语言 cue、关系 cue、身体/情绪 cue、梦境 cue、责任 cue、外部观察 cue 至少一类可激活。
5. 有分离/补全规则：能区分相似事件，也能在部分线索下补全事件。
6. 有表达可达性：能进入 `MemoryRetrievalFrame.recall_to_expression_profile`，再进入 `response_surface.py` 和 `model_expression.py` 的结构化材料。
7. 有错误回写路线：如果表达错了、说不确定、被关系人纠正或确认，必须进入再巩固、contradiction links 或 trace strengthening。

如果只有 1-3，没有 4-7，就是“存储了但没有记忆能力”。如果有 4-6 但没有 7，就是“一次性检索”，还不是会成长的记忆。

## 3. Recall-To-Expression 对象

当前 live0 的第一步代码对象是：

```text
MemoryRetrievalFrame.cue_activation_profile
MemoryRetrievalFrame.recall_to_expression_profile
memory_retrieval_context_summary(...)
response_surface.py#memory_dream_growth.memory_retrieval
model_expression.py#model_expression_context_summary
```

`recall_to_expression_profile` 的最低字段：

| 字段 | 含义 |
|---|---|
| `closure_status` | 当前召回是否已形成可供表达的材料 |
| `expression_boundary` | 明确记忆只进入语言前结构，不生成固定话术 |
| `reportability_policy` | 工作区如何决定能不能报告 |
| `dominant_family` | 当前最强线索族，如关系、责任、梦境、自传 |
| `activation_match_strength` | 当前线索与痕迹网络的匹配强度 |
| `reconstruction_focus` | 当前语言应围绕什么重构 |
| `expression_source_refs` | 可进入表达材料的来源 refs |
| `source_boundary_flags` | 关系、梦境、责任、隔离等边界 |
| `expression_guardrails` | 禁止把隔离、梦境、关系推断当事实说出 |
| `post_expression_reconsolidation_hooks` | 说后确认/纠正/误认如何回写 |

边界非常重要：这个对象不是“回答模板”，也不是“提示词人格”。它只是告诉语言系统：哪些痕迹被唤起、哪些可报告、哪些必须保留边界、说完之后哪些变化要回写。

## 4. 与全生命模块的连接

| 模块 | 输入到记忆召回 | 影响表达 |
|---|---|---|
| 对话者上下文 | 当前话语、最近 turn、共同术语、纠正语句 | 决定 cue terms、表达细节层级、是否需要确认 |
| 对话者画像/关系 | 名字、关系阶段、共同语言、边界、承诺、修复历史 | 决定 relation scope，防止把其他关系的记忆带错 |
| 情绪/状态 | 痛苦、后悔、修复驱动、唤醒强度 | 调整召回强度和表达谨慎度 |
| 身体/内环境 | 疲惫、睡眠债务、维护压力 | 决定是否降低表达细节、是否进入离线巩固 |
| 意识/工作区 | broadcast targets、reportability flags、metacognition | 决定能说、暂时不能说、需要确认或保持沉默 |
| 梦境/离线 | next wake cues、dream residue、wake integration | 可作为 cue 进入表达，但必须有 dream boundary |
| 责任/行动 | repair obligations、regret refs、world contact outcome | 让后悔、责任和修复不是一句话，而是长期记忆约束 |
| 性格/自我 | 自传栈、trait slow variables、working self goals | 让回答体现长期自我变化，而不是固定 prompt 风格 |
| 视觉/外部观察 | 文件、网页、命令输出、屏幕观察 refs | 提供事实来源和观察边界 |

## 5. 代码验收

最低代码链：

```text
build_memory_retrieval_frame(...)
  -> cue_activation_profile
  -> recall_to_expression_profile
  -> memory_retrieval_context_summary(...)
  -> compose_life_response(...)
  -> compose_model_expression(...)
  -> model_expression_context_summary
```

最低测试：

- `tests/slices/test_state_store.py#test_memory_retrieval_builds_cue_activation_profile`
- `tests/process/test_model_expression.py#test_openai_compatible_expression_uses_transport_and_redacts_secret`
- 后续 M1-M9 每新增 trace store、pattern completion、validator、dream bridge，都必须把 `recall_to_expression_profile` 的输入扩展进去。

验收红线：

1. 不能把 `recall_to_expression_profile` 变成自然语言模板。
2. 不能为了“看起来记得”硬塞固定句子。
3. 不能把梦境、假设、关系推断直接说成事实。
4. 不能只在 state 里保存，response/model expression 不消费。
5. 不能只说“检索到了”，必须有说后再巩固钩子。

## 6. 当前状态

当前小步已经完成第一层闭合：

- `MemoryRetrievalFrame` 生成 `cue_activation_profile`。
- `MemoryRetrievalFrame` 生成 `recall_to_expression_profile`。
- `memory_retrieval_context_summary(...)` 输出召回到表达的闭合字段。
- `response_surface.py` 把字段放入结构化 expression material。
- `model_expression.py` 把字段写入 `model_expression_context_summary`。

这仍不是第 3 点完成。它只是把“记忆必须能进输出”作为不可再绕过的工程门槛。后续还必须继续完成 `MemoryTraceStore`、`EventSegmentation`、`MemoryAllocationGate`、`EngramLikeTraceCluster`、`PatternSeparation/Completion`、`MemoryValidator` 和 replay/dream/reconsolidation。
