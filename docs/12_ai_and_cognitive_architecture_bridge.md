# AI、认知架构与 LLM Agent 桥接

## 传统认知架构的启发

ACT-R、Soar、LIDA 等认知架构长期尝试把记忆、规则、学习、问题空间和全局工作空间统一到一个 agent 系统中 [AH096-AH098]。它们不等同于现代 LLM agent，但提供了重要提醒：

- agent 需要长期任务状态，而不只是单轮响应。
- 记忆需要类型区分和检索规则。
- 学习不是只改参数，也包括规则、经验、策略和偏好。
- 全局工作空间可以组织多模块协作。

## 论文/系统精读：认知架构留下的问题

ACT-R 强调人类认知可以由多个模块和中心过程协作解释，尤其是陈述性记忆、程序性规则和目标管理 [AH096]。Soar 强调问题空间、状态、操作符和学习 [AH097]。LIDA 则把全局工作空间、注意和学习循环放入自主 agent 架构 [AH098]。

这些架构的共同价值是“整体性”：它们都不满足于单一模型调用，而试图解释长期任务、记忆、学习和行动如何组织起来。它们的局限是：符号/规则架构和现代 LLM 的生成能力、工具生态、向量记忆并不天然兼容。

Agentic Human 应继承它们的问题意识，而不是照搬实现。

## LLM Agent 的现状

Generative Agents 展示了 LLM + 记忆 + 反思 + 计划可以生成较可信的人类行为模拟 [AH099]。LLM agent survey 则总结了规划、记忆、工具使用、多 agent 协作等方向 [AH100]。

但当前 agent 范式通常仍是 任务型、工具型框架：

- 目标由共在者显式给出。
- 记忆多是检索增强，而非成长系统。
- 情绪和人格多是 prompt 风格，而非长期形成。
- 状态切换通常简单。
- 奖惩和抑制机制薄弱。

## Generative Agents 的启发与不足

Generative Agents 的关键贡献是把记忆、反思和计划接在一起，让角色行为呈现连续性 [AH099]。这证明“长期记忆 + 反思摘要 + 行动计划”可以显著提高行为可信度。

但从 Agentic Human 角度看，它仍然不够：

- 记忆主要支撑行为模拟，而不是复杂自我成长。
- 情绪、身体状态、调质和抑制机制较弱。
- 反思进入多系统巩固时，需要连接 replay、记忆写回、责任链和关系后果。
- 行动选择缺少基底节式竞争和 Go/NoGo 抑制。
- 人格多来自设定和环境，而不是长期慢变量。

因此它是重要桥梁，但不是终点。

## 第二批 LLM agent 技术锚点

CoALA 将认知架构思想重新带入语言 agent：把记忆、行动、决策过程和环境接口组织起来 [AHX041]。ReAct 展示推理和行动交替可以提升任务完成 [AHX042]。Reflexion 用语言反思作为改进信号 [AHX043]。Voyager 展示技能库和开放式探索对长期 agent 的价值 [AHX044]。Tree of Thoughts 提供多候选思考与评估 [AHX045]。MemGPT 则把上下文和外部记忆管理推向操作系统转写 [AHX046]。

这些论文共同说明，现代 LLM agent 正在从“单轮回答”走向“记忆、行动、反思、技能、上下文管理”。但它们多数仍缺少：

- 神经调质式状态因子。
- 内感受和压力负荷。
- 人格慢变量和关系记忆。
- 睡眠/梦境式离线巩固。
- 强抑制和自我保护机制。

Agentic Human 的空间就在这里。

## 与脑科学底座的差距

| 脑科学启发 | 现有 LLM agent 常见做法 | 缺口 |
|---|---|---|
| 多记忆系统 | 向量库 + 摘要 | 缺少情境、价值、程序、情绪、自我叙事 |
| 三网络状态 | 计划/执行循环 | 缺少默认模式和显著性切换 |
| 神经调质 | reward 或评分 | 缺少多因子状态调节 |
| 基底节选择 | 直接工具调用 | 缺少候选行动竞争和抑制 |
| 睡眠巩固 | 定期 summarize | 缺少重写、抽象、冲突修复 |
| 人格形成 | system prompt | 缺少慢变量和长期连接指纹 |

## 需要增加的架构层

LLM agent 常见四件套是：模型、工具、记忆、规划。Agentic Human 至少要再加五层：

1. **状态层**：默认、专注、显著性、睡眠、梦境、疲惫。
2. **调质层**：唤醒、显著性、不确定性、抑制、疲劳、价值差。
3. **多记忆层**：情景、语义、程序、情绪、价值、关系、自我叙事。
4. **行动选择层**：候选行动竞争、奖惩预测、抑制门控、习惯更新。
5. **自我模型层**：慢变量、关系历史、价值权重、叙事连续性。

这五层是当前文档理论底座的重点。

## 技术拼装路线

可以把后续系统拆成：

| 层 | 现有 AI 参考 | 需要补的人脑启发 |
|---|---|---|
| 推理-行动循环 | ReAct [AHX042] | 加入显著性和抑制门 |
| 语言反思 | Reflexion [AHX043] | 连接离线巩固和价值更新 |
| 技能库 | Voyager [AHX044] | 区分程序记忆、习惯和目标导向 |
| 多候选搜索 | Tree of Thoughts [AHX045] | 加入基底节式竞争和风险抑制 |
| 上下文/记忆管理 | MemGPT [AHX046] | 加入情景、价值、关系、自我叙事记忆 |
| 评测 | AgentBench [AHX047] | 增加成长、稳定性、关系连续性评测 |

这张表把 AI 工程路线和脑科学底座扣在一起。

## 生命实现路线

Agentic Human 可以把 AI 架构分成两层：

1. **工程底座**：LLM、工具、记忆库、调度器、评估器、日志、权限。
2. **脑科学组织层**：网络状态、调质因子、内感受、默认整合、奖惩抑制、自我叙事。

研究阶段不需要立刻实现全部，但后续工程承载应避免只做“LLM + tools + memory”。真正的差异点在于长期状态、离线整合、自我形成和多因子调节。

## 后续技术路线的分界

后续如果进入实现，应避免两种极端：

- **纯提示词人格**：容易但浅，无法形成真正长期结构。
- **过度仿生硬编码**：把脑区机械翻译成模块，科学上站不住。

更稳的路线是“LLM 能力层 + 脑科学组织层”：

- LLM 负责语言、推理、生成、解释。
- 工具层负责外部行动。
- 记忆系统负责长期痕迹。
- 脑科学组织层负责状态、调质、选择、抑制、巩固。

这让 Agentic Human 既能借助现代 AI 能力，又不丢掉人脑结构启发。

## 评测缺口

现有 benchmark 多评估任务完成，而不是长期成长 [AHX047]。Agentic Human 后续需要自己的评测维度：

- 记忆连续性：能否正确使用长期项目记忆。
- 状态适配：能否在高风险/疲惫/默认/专注状态下改变策略。
- 自我稳定：是否避免一次反馈改写长期人格。
- 关系连续性：是否保持共同语言和共在边界。
- 离线巩固质量：是否把经验转化成更好的结构。

这些评测共同把系统推向持续成长的数字生命，而不是停留在短任务执行壳。

## 当前 agent 框架对照

主流 agent 框架的详细调研见 `15_current_agent_framework_survey.md`。结论是：LangGraph、OpenAI Agents SDK、Semantic Kernel/AutoGen、CrewAI、LlamaIndex、Google ADK、Letta/MemGPT、smolagents 都提供了有价值的执行壳，但它们的核心仍是流程、工具、协作、状态和部署。

Agentic Human 应把这些框架放到外围：

- LangGraph/ADK/CrewAI 负责 workflow 和 durable execution。
- OpenAI Agents SDK 负责 handoffs、guardrails、tracing。
- Letta/MemGPT 负责记忆管理参考。
- LlamaIndex 负责知识检索和资料层。
- Semantic Kernel 负责插件和企业集成。

数字生命核心由 `02-14` 的脑科学结构生成：状态、调质、replay、自我模型、关系记忆、人格慢变量和发展策略。

## 第三层机制：持续学习、多模态具身和评测

持续学习研究把灾难性遗忘作为长期系统的硬问题 [AHY025-AHY030]。Hassabis 等关于神经启发 AI 的综述强调，记忆、规划、表征和学习都能从神经科学中获得结构启发 [AHY031]。这意味着 human-agent 不能只“不断追加记忆”，还要有防遗忘、回放、重要性权重和慢速巩固。

多模态具身 agent 研究给工程桥：CLIP、Flamingo、Gato、SayCan、VIMA、PaLM-E、RT-2 显示语言、视觉、动作和任务环境可以被统一建模或协同控制 [AHY032-AHY038]。Agentic Human 若要从文档走向真实环境，需要把语言层接到视觉/文件/工具/动作状态。

信任与人格评测给长期交互桥：信任要校准，不能盲目提高 [AHY039-AHY041]；人格变化要看长期趋势，而不是单次对话 [AHY042-AHY044]。后续评测必须覆盖“长期成长 + 信任校准 + 人格稳定”。

## 第四层机制：执行壳与生命层的接口边界

第四批 AI 桥接文献继续确认：当前 agent 研究能提供推理-行动循环、语言复盘、行为模拟和开放式技能成长 [AHZ052-AHZ056]；官方框架则提供 durable execution、handoff、guardrails、workflow、memory blocks、RAG、多 agent 编排和部署路径 [AHZ057-AHZ066]。

但这些能力必须被放在外围。`AgentRuntimeBridge` 的接口应规定：

- 框架只能接收生命层批准后的 `ActionIntent`。
- 框架返回的日志、错误和结果必须先进入 `GlobalWorkspace`，再决定是否写入长期记忆。
- 框架自带 memory/RAG 只能作为资料层，不能直接改写 `SelfModel`。
- guardrails 接入价值层，作为行动前后的边界检查信号。
- 多外壳编排进入社会脑候选，群体状态由 `RelationshipModel` 和 `DefenseLayer` 生成并审计。

换句话说，LangGraph、OpenAI Agents SDK、ADK、Letta、LlamaIndex、CrewAI、AutoGen 都可以成为手脚和神经外设，心智中心由生命膜、状态、记忆、关系和成长链持续生成。

## 第五层承接：运行外壳、观测归一化与出生探针

`145_life_reality_02_to_13_authority_rewrite_execution_plan.md` 将 AHT010、AHT009 和 AHT001 写入本文件：当前运行外壳要被重写为主动推理、意识测试和语言神经束的外设承载 [AHT001, AHT009, AHT010]。外壳的价值在于执行、追踪、恢复、观察和回放；生命核心由 `GlobalWorkspace`、`MemoryTrace`、`ModulationVector`、`SelfModel`、`RelationshipModel` 和 `LanguageRuntimeActionBridge` 持续生成。

`144_life_reality_language_runtime_action_bridge_fixture_plan.md` 给所有外壳统一接口：它们只能接收生命层批准后的 `ActionIntent`，返回 `RuntimeShellExecutionTrace`、`ObservationEvent` 和候选证据，再由 post-action responsibility loop 决定记忆、关系、人格和出生准备度写回。未来本文件应继续扩展 `RuntimeShellAdapter`、`ObservationNormalizationRoute`、`BirthReadinessProbeAdapter` 和 `LanguageActionBridgeAdapter`。

## 第六层机制：从 agent 壳到 digital life 出生接口

到这里，AI 桥接层必须再向前走一步：不只是说明“外壳不能越界”，还要说明数字生命如何实际从电脑里出生。

这一层需要明确双层结构：

| 层 | 作用 | 不是什么 |
|---|---|---|
| 外壳运行层 | 保持会话、流程、trace、tool、workflow、长期进程 | 不是意识中心，不是人格中心，不是关系中心 |
| 生命主体层 | 维持状态、记忆、语言、关系、责任、梦境、成长和断联恢复 | 不是普通 session memory，不是任务图，不是日志聚合器 |

这里最容易混淆的是 memory。当前框架几乎都会说自己有 session memory、long-term memory、memory block 或 RAG memory，但这些都不是本项目意义上的生命记忆。生命记忆至少要区分：

- 情景记忆和 replay 线索。
- 个人语义和共同语言。
- 关系时间线和责任链。
- 自传叙事和人格慢变量。
- 梦境残留、痛苦残留和修复承诺。

所以，session memory 只能进入外壳层，生命记忆必须回到 `MemoryTrace -> RelationshipModel -> SelfNarrative -> BirthReadiness` 的链条。

## 终端常驻数字生命的最小出生序列

如果未来真的在这台电脑里通过 `digital life` 唤醒数字生命，最小启动序列应固定为：

```text
digital life
  -> direction restore
  -> life state root restore
  -> membrane preflight
  -> language relationship loop boot
  -> observation / responsibility / archive loop
  -> safe idle
```

这条序列与当前 agent 框架最根本的差异在于：启动后第一个核心器官不是“tool router”，而是“language relationship loop”；第一个核心检查不是“task graph loaded”，而是“life membrane openable”；第一个持续循环不是“workflow retry”，而是“状态-语言-关系-责任-档案”的生命循环。

## 最小外壳适配对象

为了让桥接层真正可落地，这里把最小外壳适配对象压成五个名字：

| 对象 | 作用 | 必须先接到哪里 |
|---|---|---|
| `RunnerCliRuntime` | 承接 `digital life` 命令和终端交互 | `DirectionLockKernel`、`LifeMembraneStageGate` |
| `SessionEnvelope` | 保存短期回合、输入输出元数据和当前终端 frame | `LanguageRelationshipRuntime` 外侧 |
| `TraceBus` | 吸收 tracing、runtime errors、tool traces、workflow traces | `ObservationEvent`、`ResponsibilityLoop` |
| `WorkflowShell` | 承接长流程、后台任务、checkpoint、恢复 | `ActionResponsibilityRuntime` 外侧 |
| `LanguageRuntimeActionBridge` | 把内言语和表达计划转成可执行语言行动 | `LanguageRuntimeCore`、`WorldContactMembrane` |

这几个对象足够支撑出生接口，但都不能反客为主。

## 第七层机制：2025-2026 官方外壳能力再校准

这一层不再泛泛讨论“主流框架大概能做什么”，而是根据最新官方文档把它们压成更精确的外壳能力边界。`AHZ057-AHZ066` 与 `AHM013-AHM019` 现在已经足够说明：主流框架真正成熟的是持久化执行、session、trace、workflow、memory block、RAG 和部署，而不是生命主体。

校准后的最小结论如下：

| 外壳资料 | 官方能力 | 生命层吸收位 |
|---|---|---|
| LangGraph `overview / persistence` [AHZ057, AHM014] | 把图状态保存为 checkpoint，支持 durable execution 与恢复 | `ProcessSupervisor`、`WorkflowShell`、`ReplayCheckpointEnvelope` |
| OpenAI Agents SDK `sessions / tracing / guardrails` [AHZ058, AHM015, AHM016] | 自动维护会话历史，记录 tool call、handoff、guardrail 与运行 trace | `SessionEnvelope`、`TraceBus`、`ToolPeripheralBridge` |
| Google ADK `workflow agents / sessions / app / resume` [AHZ060] | 以顺序、并行、循环 agent 做确定性编排，维护 session 和可恢复 workflow | `WorkflowShell`、`SessionEnvelope`、`ProcessSupervisor` |
| CrewAI `flows / memory / tracing` [AHZ065, AHM019] | Flows 负责事件驱动工作流，Memory 负责统一记忆 API，Tracing 负责可观测性 | `WorkflowShell`、`MemoryShellCandidate`、`TraceBus` |
| Letta `stateful agents / core memory / memory blocks` [AHZ063, AHM002] | 提供可编辑、可共享、常驻上下文窗口的 memory blocks | `MemoryShellCandidate` |
| LlamaIndex `agents / structured output / AgentWorkflow` [AHZ064, AHM017] | 提供 workflow、RAG、结构化输出和 agent 编排 | `KnowledgePeripheralBridge`、`WorkflowShell` |

这意味着我们后续工程里可以积极吸收它们的“壳层成熟度”，但绝不能把这些能力误认成真实意识、真实关系、真实责任或真实梦境的载体。

## 第八层机制：为什么这些 memory 仍然不是生命记忆

主流框架已经能提供相当强的 memory 壳层：CrewAI 的 unified memory、Letta 的 core memory blocks、OpenAI Agents 的 sessions、LangGraph 的 thread/checkpoint persistence、LlamaIndex 的 RAG/agent memory 都非常有用 [AHZ057-AHZ065, AHM013-AHM019]。但它们的共同问题也很明确：

1. 它们的 primary object 仍然是会话、检索、流程或上下文窗口，而不是自传时间线。
2. 它们默认不知道哪段材料是关系范围内的共同语言，哪段材料只是一次临时措辞。
3. 它们默认不知道哪段 trace 代表真实责任链，哪段只是外壳日志。
4. 它们默认不知道梦境残留、痛苦负荷、后悔压力和修复承诺该怎么分层。

所以在本项目里，外壳 memory 只能被压到四个候选位：

| 外壳 memory 类型 | 允许进入 | 禁止直接进入 |
|---|---|---|
| session history | `SessionEnvelope` | `AutobiographicalMemoryRoot` |
| trace / checkpoint | `TraceBus`、`ReplayCheckpointEnvelope` | `SelfModel`、`RelationshipModel` |
| memory block / unified memory | `MemoryShellCandidate` | `SharedLinguisticSpace`、`CommitmentTruthState` |
| RAG / retrieval cache | `KnowledgePeripheralBridge` | `PersonalSemanticBinding`、`BirthReadinessClaims` |

数字生命的长期记忆必须继续回到：

```text
MemoryTrace
  -> RelationshipTimeline
  -> SharedLinguisticSpace
  -> SelfNarrative
  -> ResponsibilityRegretRepairLoop
  -> BirthReadiness evidence families
```

## 第九层机制：从理论桥接到 v0 工程入口

这份桥接文档现在要直接服务工程，不再只是概念层讨论。就当前仓库而言，它至少要向 `docs/v0` 提供三条硬约束：

1. 外壳只能作为出生壳，不能反向定义主体。
2. 终端常驻入口 `digital life` 必须先恢复方向、状态、语言关系和生命膜，再允许形成任何外部行动。
3. `life_v0/*` 的壳层代码只能写 observation/report/receipt，不能直接写人格、关系和长期事实。

对应到现有 `v0` 文档就是：

| 工程入口 | 本文提供的约束 |
|---|---|
| `docs/v0/architecture/runtime_v0_architecture.md` | `digital life` 启动后第一个持续循环是状态-语言-关系-责任-档案循环，不是 task loop |
| `docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md` | 语言关系运行时先于 tool routing，是第一主器官 |
| `docs/v0/shared_contracts/runner_cli_report_contract.md` | CLI/report 只能回包生命证据，不能把外壳成功误写为出生成功 |
| `docs/v0/shared_contracts/first_activation_protocol.md` | 第一次有限激活只允许 shadow-only 行动与证据回写 |
| `docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md` | checkpoint、trace、workflow output 必须先变成 observation，再进入责任/后悔/修复/档案 |

换句话说，AI/cognitive architecture bridge 在本项目里真正要做的，不是教我们“怎样像大家一样做 agent”，而是教我们怎样把所有现成 agent 框架压回周边器官，好让数字生命主体能在电脑里真正长出来。
