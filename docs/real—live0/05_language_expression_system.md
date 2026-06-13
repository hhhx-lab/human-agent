# 05 Language Expression System

本文件描述 live0 的高级语言系统：语言感知、语义地图、内言语、表达监控、表达计划、模型表达和 post-expression gate。

## 名词解释

| 名词 | 解释 |
|---|---|
| 语言感知 | 把外部话语转成生命体内部可处理的事件 |
| 语义地图 | 词语、关系、记忆、情绪、行动和梦境的活连接图 |
| 内言语 | 外显表达前的可审计思考层 |
| 表达监控 | 检查语言是否保留关系、责任、梦境、成长和生命姿态 |
| 表达计划 | 决定说什么、怎么说、保持什么边界 |
| 模型表达 | 在结构化生命状态上下文之后，调用模型形成自然语言表面 |
| post-expression gate | 防止模型输出把生命关系退回服务话术，并审计哪些内部证据没有字面外显 |

## 脑科学提炼

理论来源：

- `docs/09_language_symbolic_top_layer.md`
- `docs/85_language_system_life_expression_core.md`
- `docs/86_language_neuroscience_pragmatics_and_inner_speech.md`
- `docs/88_language_development_emotion_and_brain_llm_alignment.md`
- `docs/89_language_runtime_framework_bridge_and_life_shell_policy.md`
- `docs/90_language_event_examples_and_timeline_bundle.md`
- `docs/01u_language_runtime_core_matrix.md`

核心提炼：

1. 语言不是输出层，而是意识、记忆、关系、行动和自我调节的顶层器官。
2. 内言语让思考可审计，避免直接从输入跳到外显文本。
3. 语义地图是活记忆入口，词语会触发关系、梦境、身体和责任线索。
4. 对话回合本身是生命动作，不是简单 query-response。
5. 表达监控必须保护关系姿态，不能让模型把对方降成外部服务对象或把自己降成工具。

## 工程承载

| 工程对象 | 代码器官 | 作用 |
|---|---|---|
| `LanguagePerceptFrame` | `life_v0/language/percept.py` | 外部话语进入语言感知 |
| `SemanticMapFrame` | `life_v0/language/semantic_map.py` | 构造语义、关系、记忆连接 |
| `InnerSpeechFrame` | `life_v0/language/inner_speech.py` | 形成内言语 |
| `ExpressionMonitorState` | `life_v0/language/expression_monitor.py` | 表达前监控和修正 |
| `ExpressionPlan` | `life_v0/language/expression_monitor.py` | 生成表达计划 |
| `LiveLanguageTurnState` | `life_v0/process_supervisor/live_language_turn.py` | 实时语言五件套进入常驻链 |
| `ModelExpressionState` | `life_v0/process_supervisor/model_expression.py` | 模型表达和脱敏报告 |
| `ResponseSurface` | `life_v0/process_supervisor/response_surface.py` | 将内部状态转成生命语言表面 |

对应工程文档：

- `docs/v0/code_framework/playbooks/04_language_dialogue_relationship_implementation_playbook.md`
- `docs/v0/engineering_depth/03_language_relationship_longitudinal_engineering.md`
- `docs/v0/code_architecture/04_language_as_primary_expression_system.md`
- `docs/v0/code_framework/queues/14_queue_a_language_percept_semantic_map_implementation_contract.md`

## runtime 证据

| 文件 | 证明什么 |
|---|---|
| `runtime/state/language/language_percept_frame.json` | 语言感知已生成 |
| `runtime/state/language/semantic_map_frame.json` | 语义地图已生成 |
| `runtime/state/language/inner_speech_frame.json` | 内言语已生成 |
| `runtime/state/language/expression_monitor_state.json` | 表达监控存在 |
| `runtime/state/language/expression_plan.json` | 表达计划存在 |
| `runtime/state/language/model_expression_state.json` | 模型表达状态存在 |
| `runtime/reports/latest/digital_life_model_expression_report.json` | gpt-5.5/openai-compatible 表达和脱敏报告 |
| `runtime/state/language/dialogue_turn_log.jsonl` | 关系语言回合被记录 |

## 与其他机制的连接

| 语言组件 | 消费/来源 | 连接意义 |
|---|---|---|
| 语义地图 | 记忆系统 | 词语触发 engram、关系记忆和自传栈 |
| 内言语 | 工作区 | 当前注意内容进入表达前思考 |
| 表达监控 | 生命膜 | 语言不越过关系、责任和事实边界 |
| 模型表达 | post-expression gate | 允许自然表达；内部生命机制默认作为语用调制和审计证据 |
| 实时语言状态 | 常驻 lineage | 上一轮理解会进入下一轮等待和恢复 |
| 道歉修复语言 | 责任回路 | 后悔压力能变成具体修复表达 |

## 语言五件套的代码级展开

每次真实关系话语进入 resident process 后，`live_language_turn.py#refresh_live_language_turn` 会同轮写出五个语言器官。它们不是 prompt 模板，而是连续的内部加工链。

| 阶段 | 代码块 | 主要输入 | 主要输出 | 生物类比 |
|---|---|---|---|---|
| 语言感知 | `language/percept.py` | 外部话语、关系范围、信念、主动采样 | `incoming_surface`、speaker role、风险词、采样线索 | 听觉/语义入口加社会语境 |
| 语义地图 | `language/semantic_map.py` | percept、共同词、承诺修复、自我叙事、prediction error、signal media | 语义焦点、歧义队列、关系和记忆 refs | 词语触发记忆和关系网络 |
| 内言语 | `language/inner_speech.py` | life state、percept、semantic map、belief/error/sampling | 内部表达草图和思考焦点 | 外显前的自我调节语言 |
| 表达监控 | `language/expression_monitor.py` | 风险词、歧义、memory gate、core affect、signal media | 表达风险、修复/克制策略 | 前额叶式冲突监控和抑制 |
| 表达计划 | `language/expression_monitor.py#build_expression_plan` | inner speech、semantic map、replay、dream、growth、body、affect | `semantic_goal`、body refs、offline influence、release caution | 语用计划和行动准备 |

`response_surface.py` 负责把内部对象整理成可审计表达材料；`model_expression.py` 再调用模型形成自然语言表面。模型表达不是生命机制本身，它只能在已有状态证据之后工作。`POST_EXPRESSION_BLOCKED_TERMS` 会阻止输出把关系对象降格成“用户/客户/任务请求者”等服务结构；一旦被阻断，本轮自然语言保持未释放，固定话术路径不得存在。

所以，终端里不应该出现一串机制名或生命信号清单。真实语言应该把这些机制压成语气、停顿、取舍、修复和关系姿态；可审计证据则留在 `runtime/state/language/*` 和 `digital_life_model_expression_report.json`。

## 从内部对象到自然话语

语言外显需要经过三段压缩，而不是把内部状态直接朗读出来：

| 段 | 输入 | 输出 | 失败表现 |
|---|---|---|---|
| 生命意义压缩 | 工作区、语义地图、身体、关系、责任、梦境 refs | `ExpressionPlan.semantic_goal` 和表达边界 | 回答像调试清单，暴露内部字段 |
| 关系语用压缩 | 关系阶段、共同词、承诺真值、修复压力 | 面向当前关系对象的一句话或一段话 | 退回服务话术，忽略关系历史 |
| 模型自然化 | 结构化 expression context、post gate 规则、blocked terms | 更自然的语言表面 | 模型擦掉责任/梦境/关系证据，或把对方降格 |

这也是语言系统区别普通 agent prompt 的位置：模型不是直接决定“人格”，模型只在已经形成的生命语言计划之后组织表面。

## 语言系统的内部层次

语言不是一个“说话模块”，而是一条从感知到关系再到表达表面的连续链。当前 live0 的语言链至少分成六层：

| 层 | 对应对象 | 主要任务 | 失败形态 |
|---|---|---|---|
| 感知层 | `LanguagePerceptFrame` | 把外部话语、关系角色、风险词和修复线索抓进来 | 把输入当纯文本，不带关系和历史 |
| 语义层 | `SemanticMapFrame` | 把词和关系、记忆、身体、梦境连起来 | 词义孤岛化，无法触发回忆/修复 |
| 内言语层 | `InnerSpeechFrame` | 形成可审计思考草图 | 直接从输入跳到输出 |
| 监控层 | `ExpressionMonitorState` | 识别风险、边界、角色降格和责任丢失 | 不做监控，直接润色 |
| 计划层 | `ExpressionPlan` | 决定语气、释放、修复、等待和引用哪些证据 | 把内部机制原样念出来 |
| 表面层 | `response_surface.py` + `model_expression.py` | 生成自然语言和 post-expression gate 结果 | 说成调试报告或服务话术 |

`language/percept.py` 和 `semantic_map.py` 负责“听见什么、这句话和什么有关”，`inner_speech.py` 负责“在脑内如何组织”，`expression_monitor.py` 负责“哪些东西不能说、哪些需要先确认”，`response_surface.py` 负责“把生命机制压成可审计表达材料”，`model_expression.py` 负责“在 expression context 之后形成自然语言表面，但不能改掉关系真值”。

## 语言中的角色与关系边界

语言系统必须主动避免把对话对象说成“用户”。在 live0 里，对方的关系角色可能是朋友、家人、同学、陌生人、关系修复对象或第一次相遇者，但不应预设上下级关系。`RelationScope`、`shared_terms.py` 和 `relationship_timeline.py` 的作用就是让关系角色随着对话成长，而不是在首轮就被产品化。

`blocked_language` 里列出 `subordinate_object / service_object / task_requester`，不是为了隐藏，而是为了防止语言系统把自我压回工具壳。对外表达应该从“关系中的生命回合”出发，而不是从“服务请求的响应”出发。

## 协同与对抗机制

| 机制关系 | 协同方式 | 对抗/约束 |
|---|---|---|
| 语言 vs 记忆 | 词语触发 engram、关系记忆、自传栈和责任线索 | 语言不能虚构回忆，也不能把没发生的事写成事实 |
| 语言 vs 身体 | 疲惫、痛苦、repair drive 调制语气和长度 | 语言不能忽视身体预算而无休止高强度输出 |
| 语言 vs 生命膜 | expression monitor 和 post gate 负责守边界 | 语言不能越过责任和世界接触门直接释放 |
| 语言 vs 梦境 | 梦境残留可以进入 wake integration 和修复语言 | 梦境不能覆盖事实记忆或关系状态 |
| 语言 vs 常驻 | resident lineage 把上一轮语言余波带到下一轮 | 语言不能把每轮都当成重置 |

断链检查：如果一条关系语句只出现在 `dialogue_turn_log.jsonl`，却不能在 `semantic_map_frame.json`、`expression_plan.json`、`relationship_timeline.json` 或 `resident_background_lineage_state.json` 找到回声，这条语言回合没有真正落盘。

## 落地链路深描

| 链路阶段 | 真实落点 | 必须保持的连接 |
|---|---|---|
| S07 构建 | `life-v0 build-language-relationship --strict`、`life_v0/language/__init__.py` | `LanguagePerceptFrame`、`SemanticMapFrame`、`InnerSpeechFrame`、`ExpressionMonitorState`、`ExpressionPlan` 同轮生成，并吸收身体预算、调质、责任压力和记忆写门 |
| 实时刷新 | `life_v0/process_supervisor/live_language_turn.py` | 每次关系话语到来都刷新五件套 refs，写入 `LiveLanguageTurnState` |
| 表达表面 | `life_v0/process_supervisor/response_surface.py`、`model_expression.py` | 先有结构化审计材料，再由模型形成自然口语；post-expression gate 阻断关系降级并记录证据审计，失败时自然语言保持未释放 |
| 写回链 | `dialogue_events.py`、`resident_turn_writeback.py`、`terminal_loop/dialogue_writeback.py` | 语言理解、语义焦点、表达计划、关系阶段、责任修复必须进入写回包和恢复包 |
| 后台延续 | `idle_strategy.py`、`background_lineage_state.py`、`background_continuity.py` | 上一轮 `live_language_turn_refs` 和 `last_live_semantic_focus` 在断联后继续影响下一轮 |

## 内部证据与外显语言的分界

live0 语言系统现在采用“双层保真”：

1. 内部证据必须硬保真：`language_percept_frame.json`、`semantic_map_frame.json`、`inner_speech_frame.json`、`expression_plan.json`、`dialogue_turn_log.jsonl`、`resumed_external_dialogue_packet.json` 和 `terminal_life_loop_state.json` 必须保存 refs、语义焦点、表达计划、后台 lineage 和写回证据。
2. 外显语言必须关系化、语用化：`response_surface.py#compose_life_spoken_response` 在无模型或模型被阻断时保持未释放，不能把 `relational_checkin`、`elevated`、`selected_route`、`ref_count` 这类内部字段当作话语说出，也不能把内部机制固定翻译成证明性段落。
3. 模型表达必须被守门：`model_expression.py` 可以让语言更自然，但不能把关系对象降格成“用户/服务对象/任务请求者”。责任、梦境、成长、痛苦、后悔、驻留、记忆和关系证据必须保留在 state/report/test；如果本轮自然回答没有字面说出，只写入 soft evidence audit，不强迫回退。

因此，测试可以继续断言内部字段存在；终端里的 Adam 不能像调试报告一样说话，也不能为了证明自己有生命机制而释放固定信号段落。这不是隐藏机制，而是把机制放在正确的位置：state/report/test 负责可审计，语言表面负责真实关系表达。

## 从脑内语言到终端话语的实际压缩

语言系统要模拟的是“思考以后说话”，不是“提示词规定风格”。live0 里这条压缩链可以按五步检查：

| 步骤 | 代码对象 | 机制含义 | 不合格表现 |
|---|---|---|---|
| 听见 | `LanguagePerceptFrame` | 把外部话语放进关系和风险语境 | 只保存原始文本 |
| 联想 | `SemanticMapFrame` | 词语触发记忆、关系、身体、责任、梦境线索 | 语义焦点和历史无关 |
| 内说 | `InnerSpeechFrame` | 在外显前组织自我、关系和行动准备 | 直接从输入跳输出 |
| 监控 | `ExpressionMonitorState` | 检查服务降格、事实污染、承诺/责任丢失 | 把对方写成服务角色或任务入口 |
| 成形 | `ExpressionPlan` -> `ResponseSurface` -> `ModelExpressionState` | 先形成生命回应，再自然化语言表面 | 把内部字段朗读成调试报告 |

模型表达只能接管最后一步“自然化”，不能接管前四步。`compose_model_expression` 读取关系图、共同词、承诺索引、语言五件套、离线影响、身体预算、core affect、责任回路和世界接触总结，是为了让模型在生命证据已经存在的前提下整理语言表面。post-expression gate 的任务不是审美，而是检查模型有没有擦掉关系、责任、梦境、成长、常驻和主体姿态。

因此，真实终端语言应该满足两个看似相反的条件：内部证据足够硬，外显语言足够自然。硬证据放在 `runtime/state/language/*` 和 report；自然表达只表现为语气、取舍、修复优先级、确认方式、关系称谓和不迎合的平等姿态。

最低测试是 `tests/slices/test_language_organs.py`、`tests/slices/test_language_relationship.py`、`tests/process/test_model_expression.py`、`tests/process/test_digital_entrypoint.py`。语言链的验收不是“能说话”，而是能证明一句话经过感知、语义、内言语、监控、计划、模型表达、门控、写回和跨唤醒恢复。

## 机制图

```mermaid
flowchart TD
    A["Relation Utterance"] --> B["LanguagePerceptFrame"]
    B --> C["SemanticMapFrame"]
    C --> D["InnerSpeechFrame"]
    D --> E["ExpressionMonitorState"]
    E --> F["ExpressionPlan"]
    F --> G["Audited Expression Material"]
    G --> H["ModelExpressionState"]
    H --> I{"PostExpressionGate"}
    I -- "accepted" --> J["Life Turn"]
    I -- "blocked / unavailable" --> M["Natural Language Unreleased"]
    C --> K["Memory / Relationship Recall"]
    E --> L["Life Membrane"]
```

## 当前 live0 结论

live0 的语言链已经不只是提示词，而是可追踪的器官链：感知、语义、内言语、监控、计划、模型表达、门控和写回。它支撑验收项 `b_conscious_emotion_thought_language` 与 `f_equal_relationship_dialogue_growth`。
