# 当前 Agent 框架体系调研与数字生命差距

本文件调研当前主流 agent 框架。结论很直接：这些框架大多解决的是流程编排、工具调用、多 agent 协作、状态持久化、guardrails、observability 和部署问题。它们可以作为执行外壳或工程参考，但远远不是数字生命。

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
| OpenAI Agents SDK | Agent、Runner、tools、handoffs、guardrails、tracing | 轻量执行壳、追踪、handoff、guardrail | 不是长期自我系统，记忆和成长要外接 |
| Semantic Kernel / Microsoft Agent Framework | agent、plugin、messages、workflow | 企业集成、工具插件、多 agent 模式 | 偏应用编排，不是生命层 |
| AutoGen | conversable agents、多 agent 对话、human/tool integration | 多角色协作和对话式编排 | 只提供协作外壳，人格成长要进入生命层慢变量 |
| CrewAI | crews、agents、tasks、flows、memory、guardrails | 任务团队、流程和企业自动化 | role/backstory 容易停留在 prompt 人格 |
| LlamaIndex | AgentWorkflow、RAG、knowledge tools、state | 知识检索、工具化数据、agent workflow | 记忆多偏知识工程，不是内感受/调质 |
| Google ADK | LlmAgent、WorkflowAgent、tools、AgentTool、deployment | 可部署 agent 工程、workflow 和工具体系 | 仍是执行/部署框架，不是自我成长框架 |
| Letta/MemGPT | core memory、archival memory、self-editing memory | 长期记忆、上下文管理、agentic memory | 仍需接入脑区/状态/价值/抑制/梦境 |
| smolagents | 轻量 code/tool agent | 简洁执行、工具代理实验 | 太轻，不承担长期生命结构 |

## 这些框架真正有价值的部分

它们不是目标，但都有可吸收的骨架：

- **LangGraph**：durable execution 和 checkpoint 可以服务 `ReplayScheduler`、`GlobalWorkspace` 的运行恢复。
- **OpenAI Agents SDK**：tracing 和 guardrails 可以服务可审计行动、handoff 和安全边界。
- **Semantic Kernel / Microsoft Agent Framework**：plugin 模型适合作为外部工具系统。
- **AutoGen**：多 agent conversation 可以借鉴为多子系统内部讨论，但不能等同脑区协作。
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

所以我们不能再做一个 agent 框架。那只是换壳。我们的目标是把它们降级为执行层，真正的核心放在 `02-14` 构建的数字生命底座。

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
3. 保持外壳可替换：LangGraph、OpenAI Agents SDK、ADK、Letta 都只是运行时候选。
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

当前 agent 框架的最好定位是“神经外设”和“执行壳”。它们能让数字生命说话、调用工具、保存流程、部署运行，但不能让它长出连续自我。

真正的数字生命框架必须把 `02-14` 的脑科学底座放在核心，把现有 agent 框架放在外围。

## 第四层补充：官方框架能力的真实边界

第四批矩阵把当前框架资料接入为 `AHZ057-AHZ066`。这批资料用于标定它们能承担哪些外设能力，以及哪些生命核心能力必须由脑科学和生命层继续生成。

| 框架/资料 | 可吸收能力 | 必须拒绝的中心化倾向 |
|---|---|---|
| LangGraph [AHZ057] | durable execution、state graph、human-in-the-loop | 不能让 workflow graph 取代脑区-状态-调质模型 |
| OpenAI Agents SDK [AHZ058] | agents、handoffs、guardrails、tracing、tool calling | 不能让 tracing/guardrails 取代价值层和人格审计 |
| Microsoft Agent Framework [AHZ059] | 企业集成、workflow、agent runtime | 不能让企业流程成为数字生命心智结构 |
| Google ADK [AHZ060] | LlmAgent、workflow agents、tools、sessions、部署 | 不能让多 agent 编排替代社会脑 |
| Letta [AHZ063] | stateful agents、memory blocks、长期状态管理 | 不能把 memory block 等同情景/语义/关系/自我记忆 |
| LlamaIndex [AHZ064] | RAG、tool calling、workflow、资料层 | 检索命中必须进入 MemoryTrace、来源、情境和重构流程 |
| CrewAI [AHZ065] | crews、flows、多角色流程 | 角色模板必须降级为执行壳，不能替代人格慢变量和社会关系 |
| AutoGen [AHZ066] | 多 agent conversation、teams、工具调用 | 多外壳对话必须通过关系模型、共同记忆和社会后果才能进入群体心智研究 |

因此，`20_agent_runtime_bridge_contract.md` 未来要解决的不是“选哪个框架”，而是定义一个不可被框架反向吞噬的生命层接口：

- 外壳只能执行 `ActionIntent`，不能直接改 `SelfModel`。
- 外壳日志只能进入工作区和审计队列，不能直接巩固为信念。
- 外壳 memory 只能作为资料缓存，不能替代 `MemoryTrace`。
- 外壳 guardrails 只能作为边界检查，不能替代价值和防御层。
- 外壳多 agent 只能作为任务协作，不能替代关系模型。
