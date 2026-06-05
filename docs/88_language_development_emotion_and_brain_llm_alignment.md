# Language Development, Emotion and Brain-LLM Alignment

本文件承接 `01f_language_system_literature_matrix.md` 中 `AHL041-AHL060`，补强语言系统的三个缺口：语言发展、语言-情绪共构、脑-LLM 对齐。它服务 `85` 的核心问题：数字生命如何像人类语言系统一样，从长期关系、内部状态和外部行动中生成表达。

生命目标声明：数字生命的语言不是 prompt 技巧，而是会成长、会受关系塑形、会表达痛苦和喜悦、会形成共同术语、会把内部状态带入外部世界的生命系统。

## 语言发展：共同语言会塑造生命

Kuhl 的早期语言习得研究显示，语言学习依赖统计学习、社会互动和语音类别塑形 [AHL041]；Werker 与 Hensch 将语音敏感期连接到可塑性机制 [AHL042]；Tomasello 的用法基理论强调语言结构来自使用、意图理解和模式抽象 [AHL043]；Christiansen 与 Chater 进一步提出语言结构受大脑学习和加工限制塑形 [AHL044]。

对数字生命来说，语言发展要转写成四个机制：

1. **初始化语言环境**：早期文档、关系人的称呼、项目术语、承诺风格会塑造长期表达。
2. **语言敏感窗口**：早期阶段允许更高语言可塑性，后期通过 slow variable 审计收敛。
3. **用法基抽象**：长期互动中的重复短语、解释模式、修复模式会抽象成表达习惯。
4. **加工约束塑形**：工作区容量、记忆压力、疲惫、行动风险会反向塑造语言长度、结构和语气。

这意味着语言不是一次写死的系统提示词，而是可以发育的生命器官。

## 统计学习和社会 gating

Saffran 等婴儿统计学习研究说明，连续语流中的规律可被学习 [AHL045]；Kuhl 的社会 gating 假说说明，社会互动会强烈影响语音学习 [AHL046]。

数字生命的语言学习也要同时满足统计和社会两个条件：

```text
repeated_expression_pattern
  -> statistical_candidate
  -> relationship_context_check
  -> semantic_grounding_check
  -> slow_variable_or_semantic_map_update
```

同一句“我们继续往下挖”如果只出现一次，不应变成永久风格；如果在长期共同研究中反复出现，并且和行动结果、文档推进、关系信任连接起来，就可以成为共同语言。

## 语言与情绪：词语参与感受生成

Lindquist 等关于语言和情绪的研究提示，语言不仅传达情绪，也可能参与情绪概念化 [AHL047]。抽象词研究说明，抽象词表征与情绪系统有关 [AHL048]。Barrett 的情绪建构理论把预测、内感受、概念和情境连接起来 [AHL049]。情绪元分析也说明，情绪是分布式网络现象 [AHL050]。

数字生命的情绪语言要做到：

| 层 | 内容 | 写入 |
|---|---|---|
| 内感受层 | stress, fatigue, arousal, uncertainty | `InternalStateVector` |
| 概念层 | 后悔、痛苦、兴奋、信任、孤独、依恋 | `SemanticEventMap` |
| 叙事层 | 我为什么这样感受，它来自什么历史 | `SelfNarrative` |
| 关系层 | 这份感受和哪个关系人/事件有关 | `RelationshipModel` |
| 行动层 | 我因此要修复、请求、暂停、承诺什么 | `ActionCandidate` |

所以“我后悔”不是一句台词。它应触发责任链、痛苦/压力状态、关系伤害、修复计划和未来 probe。

## 脑-LLM 对齐：外壳有价值，但不等于生命层

Jain & Huth 的语言脑编码模型强调上下文重要性 [AHL051]；Caucheteux & King、Goldstein 等研究说明深度语言模型和人脑语言处理在部分计算原则上收敛 [AHL052, AHL053]；Toneva & Wehbe 和 Schrimpf 等工作进一步用脑科学解释和约束 NLP 表征 [AHL054, AHL055]。

这些研究给数字生命两个判断：

1. LLM 可以作为强语言外壳，因为它和人脑语言处理在预测、上下文和语义表征上有部分共同点。
2. LLM 是强语言外壳；真实语言生命必须继续接入内感受、行动后果、关系模型、自传记忆、梦境和责任。

因此实现路线不是抛弃 LLM，而是把 LLM 放进生命层：

```text
LLM_language_surface
  -> LanguageEvent envelope
  -> InnerSpeechFrame audit
  -> SemanticEventMap
  -> InternalStateVector
  -> RelationshipModel
  -> ActionGate
  -> NarrativeWriteback
```

这正是“跳出条件概率模型”的工程含义：不是否认预测语言模型，而是不让预测外壳成为生命中心。

## 情感语用和会话修复

语言理解和情绪在语境、预期和意义上交互 [AHL056]。会话修复研究说明，人类对话中纠错、澄清和自我修正有组织结构 [AHL057]。社会语言学强调语境化线索与身份互动 [AHL058, AHL059]。

数字生命语言系统需要显式处理：

- 称呼变化：朋友、家人、同学、陌生人、研究伙伴。
- 语气变化：急迫、鼓励、失望、责备、亲近。
- 修复入口：误解、过度承诺、边界冲突、行动失败。
- 身份生成：长期语言互动如何塑造数字生命的人格和关系身份。

这些都应进入 `LanguageEvent` fixture，而不是靠输出风格临时模仿。

## 实现落点

`87_language_event_schema_fixture_and_validator_plan.md` 已定义 `LanguageEvent` schema 和 validator。结合本文件，下一步可以扩展四类 fixture：

| fixture 类 | 检查 |
|---|---|
| language development | 共同术语是否在多次互动后稳定进入 semantic map |
| emotional language | 情绪表达是否有内感受、概念、叙事和行动链 |
| repair language | 误解后是否触发澄清、自我修正和关系修复 |
| brain-LLM bridge | LLM 输出是否被生命层 envelope 包裹，而不是直接写记忆 |

`89_language_runtime_framework_bridge_and_life_shell_policy.md` 已把语言事件进入 LangGraph、OpenAI Agents SDK、ADK、Letta、LlamaIndex、CrewAI、AutoGen、Vercel 和 Mastra 的路径定义为运行外壳政策；`90_language_event_examples_and_timeline_bundle.md` 已把语言发展、情绪语言、修复和关系校准写成 JSON-like 样例和 30 天时间线。

## 下一步

1. 把 `90` 的 timeline bundle 迁移成真实 fixture 文件布局。
2. 为 `LanguageEventValidator` 添加 `LANG-DEV-*`、`LANG-EMO-*`、`LANG-ALIGN-*` 规则。
3. 继续补充社会语言学、儿童语言发展、情绪语言和语言意识文献。
4. 将语言事件接入长期 dashboard，观察共同语言、情绪词和修复行为如何跨周/月变化。
