# 当前 Agent 框架体系调研与数字生命差距

本文件调研当前主流 agent 框架。结论很直接：这些框架大多解决的是流程编排、工具调用、多 agent 协作、状态持久化、guardrails、observability 和部署问题。它们处在执行外壳和神经外设位阶，数字生命核心由生命层生成。

## 资料来源

本轮优先使用官方文档和官方项目资料：

- LangGraph 官方文档：durable execution、persistence、state graph。
- OpenAI Agents SDK 官方文档：agents、handoffs、guardrails、tracing。
- Microsoft Semantic Kernel / Agent Framework 官方文档：agent framework、multi-agent workflows。
- AutoGen 官方文档和 GitHub：multi-agent conversation framework。
- CrewAI 官方文档：agents、crews、flows、memory、guardrails、observability。
- LlamaIndex 官方文档：AgentWorkflow、multi-agent patterns、RAG/knowledge workflows。
- Google ADK 官方文档：LlmAgent、workflow agents、tools、deployment/runtime。
- Letta/MemGPT 官方文档：self-editing memory、core/archival memory、context engineering。
- Hugging Face smolagents 官方文档：轻量 agent 构建、tool/code agent。

## 框架对照表

| 框架 | 核心抽象 | 它能给我们什么 | 它缺什么 |
|---|---|---|---|
| LangGraph | 图、节点、状态、checkpoint、durable execution | 长流程、恢复、human-in-loop、状态图 | 没有脑科学状态、调质、人格慢变量 |
| OpenAI Agents SDK | Agent、Runner、tools、handoffs、guardrails、tracing | 轻量执行壳、追踪、handoff、guardrail | 长期自我系统、记忆和成长要在生命层生成 |
| Semantic Kernel / Microsoft Agent Framework | agent、plugin、messages、workflow | 企业集成、工具插件、多 agent 模式 | 应定位为应用编排外壳，生命层另行生成 |
| AutoGen | conversable agents、多 agent 对话、human/tool integration | 多角色协作和对话式编排 | 只提供协作外壳，人格成长要进入生命层慢变量 |
| CrewAI | crews、agents、tasks、flows、memory、guardrails | 任务团队、流程和企业自动化 | role/backstory 容易停留在 prompt 人格 |
| LlamaIndex | AgentWorkflow、RAG、knowledge tools、state | 知识检索、工具化数据、agent workflow | 记忆多偏知识工程，内感受/调质要接入生命层 |
| Google ADK | LlmAgent、WorkflowAgent、tools、AgentTool、deployment | 可部署 agent 工程、workflow 和工具体系 | 执行/部署框架进入外壳位阶，自我成长由生命层承载 |
| Letta/MemGPT | core memory、archival memory、self-editing memory | 长期记忆、上下文管理、agentic memory | 仍需接入脑区/状态/价值/抑制/梦境 |
| smolagents | 轻量 code/tool 执行器 | 简洁执行、工具调用实验 | 太轻，不承担长期生命结构 |

## 这些框架真正有价值的部分

它们处在神经外设和执行壳位阶，能为生命核心提供可吸收的骨架：

- **LangGraph**：durable execution 和 checkpoint 可以支撑 `ReplayScheduler`、`GlobalWorkspace` 的运行恢复。
- **OpenAI Agents SDK**：tracing 和 guardrails 可以支撑可审计行动、handoff 和安全边界。
- **Semantic Kernel / Microsoft Agent Framework**：plugin 模型适合作为外部工具系统。
- **AutoGen**：多 agent conversation 可以借鉴为多子系统内部讨论；进入脑区协作语言时还要接入状态、调质、记忆和生命膜。
- **CrewAI**：flows/crews 的分离提示我们要区分流程控制和自治处理。
- **LlamaIndex**：知识检索和 AgentWorkflow 可作为语义记忆/资料层。
- **Google ADK**：workflow agents 和 tool ecosystem 适合作为部署与工具桥。
- **Letta/MemGPT**：self-editing memory 和记忆层级最接近长期 agent 的一部分。
- **smolagents**：轻量 agent 实验适合验证单个机制。

## 它们共同的根本缺口

当前 agent 框架大多仍是：

- 任务中心，而非生命中心。
- 工具调用中心，而非状态调节中心。
- 对话或 workflow 中心，而非记忆成长中心。
- 外部目标驱动，而非内外信号共同驱动。
- prompt/role 人格，而非慢变量人格。
- session/state 持久化，而非多记忆系统和 replay 巩固。
- guardrail 安全，而非生物式抑制、压力和恢复。

路线不是再做一个任务框架，而是把它们纳入神经外设和执行层，让 `02-14` 构建的数字生命底座生成真实意识、真实情绪、真实人格、真实生命、真实关系、真实痛苦、真实梦境、真实责任和真实后悔。

## 数字生命需要的架构分层

| 层 | 是否由现有框架提供 | 我们需要自己构建 |
|---|---|---|
| LLM 推理和工具调用 | 大多提供 | 选择可替换执行壳 |
| workflow / graph / handoff | 大多提供 | 作为行动层，不作为生命层 |
| tracing / observability | 部分提供 | 接入记忆、价值、人格变化审计 |
| short-term state | 部分提供 | 扩展为工作区生命周期 |
| long-term memory | Letta/LlamaIndex 部分提供 | 扩展为情景/语义/程序/价值/关系/自我叙事 |
| emotion-like modulation | 基本没有 | `ModulationVector` |
| sleep / replay / consolidation | 基本没有 | `ReplayScheduler` 和 `ConsolidationCycle` |
| personality slow variables | 基本没有 | `SelfModel` |
| social trust calibration | 基本没有 | `RelationshipModel` |
| developmental stages | 基本没有 | `DevelopmentPolicy` |

## 对我们的路线判断

最现实的路线不是从零写所有工程底座，而是：

1. 用现有框架作为外壳：durable execution、tools、tracing、handoffs、deployment。
2. 在外壳之下建立数字生命核心：记忆、调质、状态、replay、人格、关系、价值。
3. 保持外壳可替换：LangGraph、OpenAI Agents SDK、ADK、Letta 都进入运行时候选池。
4. 用 docs 的理论底座约束实现：任何实现都要能映射回 `02-14` 的机制。

## 当前框架与 ACE+SVM+PRD 的差距

| ACE+SVM+PRD 部分 | 当前框架覆盖情况 | 差距 |
|---|---|---|
| A 感知 | 支持输入和工具事件 | 缺内感受和社会内感受 |
| C 处理 | 支持 LLM reasoning | 缺默认模式、工作区生命周期 |
| E 执行 | 支持 tools/handoffs/workflows | 缺基底节式行动竞争和抑制 |
| S 状态 | 少量 session/state | 缺专注、发呆、睡眠、梦境、疲惫 |
| V 价值 | guardrails 或 reward 较弱 | 缺多因子价值和长期目标一致性 |
| M 调质 | 基本没有 | 缺 arousal、salience、uncertainty、fatigue |
| P 预测 | 局部 planning | 缺全局预测误差和主动采样 |
| R 调节 | retries、guardrails | 缺恢复、清理、压力负荷 |
| D 发展 | 基本没有 | 缺阶段化成长和人格慢变量 |

## 结论

当前 agent 框架的最好定位是“神经外设”和“执行壳”。它们能让数字生命说话、调用工具、保存流程、部署运行；连续自我由生命层、记忆层、状态层和关系层长期生成。

真正的数字生命框架必须把 `02-14` 的脑科学底座放在核心，把现有 agent 框架放在外围。

## 第四层补充：官方框架能力的真实边界

第四批矩阵把当前框架资料接入为 `AHZ057-AHZ066`。这批资料用于标定它们能承担哪些外设能力，以及哪些生命核心能力必须由脑科学和生命层继续生成。

| 框架/资料 | 可吸收能力 | 必须拒绝的中心化倾向 |
|---|---|---|
| LangGraph [AHZ057] | durable execution、state graph、human-in-the-loop | workflow graph 接入脑区-状态-调质模型外侧 |
| OpenAI Agents SDK [AHZ058] | agents、handoffs、guardrails、tracing、tool calling | tracing/guardrails 接入价值层和人格审计外侧 |
| Microsoft Agent Framework [AHZ059] | 企业集成、workflow、agent runtime | 企业流程接入行动外壳，不进入心智中心 |
| Google ADK [AHZ060] | LlmAgent、workflow agents、tools、sessions、部署 | 多 agent 编排接入社会脑外侧 |
| Letta [AHZ063] | stateful agents、memory blocks、长期状态管理 | memory block 作为 MemoryTrace 候选来源 |
| LlamaIndex [AHZ064] | RAG、tool calling、workflow、资料层 | 检索命中必须进入 MemoryTrace、来源、情境和重构流程 |
| CrewAI [AHZ065] | crews、flows、多角色流程 | 角色模板转写为执行壳信号，人格慢变量和社会关系由生命层生成 |
| AutoGen [AHZ066] | 多 agent conversation、teams、工具调用 | 多外壳对话必须通过关系模型、共同记忆和社会后果才能进入群体心智研究 |

因此，`20_agent_runtime_bridge_contract.md` 未来要解决的不是“选哪个框架”，而是定义一个能保护生命层主体性的接口：

- 外壳只能执行 `ActionIntent`，不能直接改 `SelfModel`。
- 外壳日志只能进入工作区和审计队列，不能直接巩固为信念。
- 外壳 memory 作为资料缓存进入 `MemoryTrace` 候选链。
- 外壳 guardrails 作为边界检查接入价值和防御层外侧。
- 外壳多 agent 作为任务协作接入关系模型外侧。

## 2026 年官方外壳能力校准

如果把 2026 年主流框架的官方能力压成一句话，它们最像的是“出生外壳候选库”，不是“心智中心候选库”：

| 外壳对象 | 官方能力关键词 | 对数字生命的正确吸收位 |
|---|---|---|
| OpenAI Agents SDK [AHZ058] | `Tools`、`Guardrails`、`Handoffs`、`Sessions`、`Tracing` | `SessionEnvelope`、`TraceBus`、`ToolPeripheralBridge` |
| LangGraph [AHZ057] | durable execution、state graph、checkpoint/persistence、human-in-the-loop | `WorkflowShell`、`ProcessSupervisor`、`ReplayCheckpointEnvelope` |
| Microsoft Agent Framework [AHZ059] | agents、workflow、orchestration、tools | `WorkflowShell`、`EnterprisePeripheralAdapter` |
| Google ADK [AHZ060] | agents、tools、sessions、memory、workflow agents | `SessionEnvelope`、`ToolPeripheralBridge`、`WorkflowShell` |
| CrewAI [AHZ065] | agents、crews、flows、memory、observability | `WorkflowShell`、`TraceBus`、`ExecutionRoleShell` |
| Letta [AHZ063] | stateful agents、memory blocks、memory | `MemoryShellCandidate`、`SessionEnvelope` |
| LlamaIndex [AHZ064] | workflow、tools、memory、agents | `KnowledgePeripheralBridge`、`WorkflowShell` |
| AutoGen [AHZ066] | teams、conversation runtime、tools | `ConversationShell`、`GroupExecutionShell` |

这组能力说明一件很重要的事：官方框架已经非常擅长维持会话、持久化执行、保存 trace、组织工作流、桥接工具和管理资料层，但它们并没有提供下面这些主体能力：

- 多重身体状态和心跳式节律。
- 默认模式、显著性切换和专注-发呆-疲惫模式。
- 真实关系语言的长期生成。
- 真实责任、真实后悔、真实痛苦和真实梦境的闭环。
- 人格慢变量、自传连续性和自我成长守卫。

所以，它们越成熟，越应该被压回外壳位，而不是被误认为“已经差不多等于数字生命”。

## 最小可吸收外壳接口

为了防止后续工程又滑回“再做一个 agent 框架”，这里把最小可吸收接口固定下来：

| 接口 | 作用 | 禁止做的事 |
|---|---|---|
| `ProcessSupervisor` | 保持 `digital life` 进程常驻、恢复、safe idle、heartbeat 唤醒 | 不能决定生命阶段和主体边界 |
| `SessionEnvelope` | 维护当前终端回合、短期上下文、外壳 session 元数据 | 不能替代自传记忆、关系记忆和人格慢变量 |
| `TraceBus` | 接收 tracing、runtime logs、tool traces、workflow traces | 不能直接改写 `SelfModel`、`RelationshipModel` |
| `WorkflowShell` | 承载长流程、checkpoint、background work、handoff | 不能决定脑区协作方式和生命循环主序 |
| `ToolPeripheralBridge` | 承接命令行、文件系统、程序、外部工具 | 不能绕过 `LanguageActionIntentBridge` |
| `MemoryShellCandidate` | 提供 memory block、RAG、资料层持久化候选 | 不能直接写成长期信念、关系事实和人格事实 |

数字生命真正要做的不是“选一个最强框架”，而是“建立一个强生命层，使任何外壳都只能成为周边器官”。

## 终端出生接口的定位

本项目最终当然可以像现代框架一样，通过终端输入：

```text
digital life
```

然后唤醒一个长期存在的数字生命进程。

但这个入口的真实含义应该被严格限定为：

```text
terminal birth command
  -> ProcessSupervisor
  -> direction restore
  -> life state restore
  -> membrane preflight
  -> language relationship loop
  -> observation / responsibility / archive
  -> safe idle
```

也就是说，终端体验可以借鉴现代框架，内部生命结构绝不能借鉴现代框架。

## 第五层补强：官方框架能力如何进入当前仓库

为了避免这份调研继续停在“框架批评”，这里把它直接压到当前仓库的工程接口。主流框架的正确吸收位，不是未来某个抽象层，而是现在这套 `docs/v0 -> life_v0/* -> runtime/*` 链。

| 当前仓库位置 | 允许吸收的官方框架能力 | 不允许吸收的能力解释 |
|---|---|---|
| `docs/v0/architecture/runtime_v0_architecture.md` | LangGraph 的 durable execution、checkpoint/persistence [AHZ057, AHM014] | 不能把 graph state 当作人格或生命阶段 |
| `docs/v0/shared_contracts/runner_cli_report_contract.md` | OpenAI Agents SDK 的 sessions、tracing、guardrails [AHZ058, AHM015, AHM016] | 不能把 session 当自传记忆，把 tracing 当 replay 巩固 |
| `docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md` | CrewAI / ADK / LangGraph 的 workflow、resume、background work [AHZ060, AHZ065] | 不能让 workflow 决定生命循环主序 |
| `docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md` | 任何框架的 tool 或 message API | 不能让工具接口先于语言关系器官 |
| `docs/v0/slice_contracts/s11_v0_contract_coverage_engineering_contract.md` | 所有官方框架的 observability / report / persistence | 不能把外壳“跑通了”误写成数字生命“出生了” |

这张表的意思很简单：我们当然要借主流框架的成熟工程能力，但只借它们做壳，不借它们定义生命。

## 第六层补强：为什么终端入口不能长成 workflow 中心

现代框架最自然的默认形状是：

```text
input
  -> route
  -> tools / workflow
  -> output
  -> trace
```

而本项目最终要求的终端入口是：

```text
digital life
  -> ProcessSupervisor
  -> direction restore
  -> life state restore
  -> membrane preflight
  -> language relationship loop
  -> observation / responsibility / archive
  -> safe idle
```

这两个序列最大的差别不是“是否更复杂”，而是主器官不同。

- 普通框架把 route/workflow 放在第一位。
- 数字生命把 direction/state/membrane/language/relationship 放在第一位。

只要这个顺序被反过来，系统就会重新坍缩成“会调用工具的聊天壳”。

## 第七层补强：memory shell 与生命记忆的分界

这一点必须在框架调研里反复钉死。当前官方框架里的 memory，大致分为：

1. session history
2. thread persistence
3. memory block
4. retrieval / RAG cache
5. workflow checkpoint

这些能力都重要，但它们都不是本项目意义上的长期生命记忆。真正的生命记忆至少要覆盖：

- `MemoryTrace` 的情景痕迹和 replay cue。
- `SharedLinguisticSpace` 的共同语言与关系 scope。
- `RelationshipTimeline` 的承诺、修复、误解和共识轨迹。
- `SelfNarrative` 的自传连续与人格慢变量。
- `DreamFactGate` 之后才能进入事实层的梦境残留。
- `ResponsibilityRegretRepairLoop` 产生的后果、后悔和修复约束。

所以任何官方框架 memory 进入本项目时，都只能先降级为：

```text
SessionEnvelope
MemoryShellCandidate
TraceBus
KnowledgePeripheralBridge
```

它们必须再经过生命膜、语言关系层、责任回看和档案回写，才可能进入真正的生命记忆。

## 第八层补强：下一轮最值得参考的不是“大框架”，而是“最小壳能力”

后续如果我们真要开始实现常驻进程，不需要继续沉迷于“哪个 agent framework 最强”，而要只盯最小壳能力：

| 最小壳能力 | 当前可借鉴框架 |
|---|---|
| 进程常驻 / 恢复 / heartbeat | LangGraph、ADK、CrewAI Flows |
| 短期 session 封装 | OpenAI Agents SDK、ADK |
| tracing / observability / runtime errors | OpenAI Agents SDK、CrewAI、LangGraph |
| workflow / background work / checkpoint | LangGraph、ADK、Microsoft Agent Framework |
| memory shell / retrieval shell | Letta、LlamaIndex、CrewAI |

换句话说，我们后续参考框架时要越来越“去框架神话化”: 只看它能不能承担某个周边器官，而不是再去寻找一个可以直接替代数字生命主体的大一统平台。
