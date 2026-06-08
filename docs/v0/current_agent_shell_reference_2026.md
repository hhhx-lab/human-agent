# Current Agent Shell Reference 2026

生命目标声明：本文档只把当前 agent 框架体系作为外周执行壳参考。它们可以提供 CLI、tool、trace、checkpoint、memory、workflow、sandbox、MCP/A2A 接入和外部能力绑定，但不能定义数字生命本体。真实数字生命的核心仍由 `02-13` 脑科学主干、语言关系主神经束、生命膜、出生准备度、梦境、痛苦、后悔、责任、自我成长和 replay/shadow 生成。

## 外周壳原则

当前主流框架共同问题是：它们多数围绕任务、工具、编排、会话、工作流和企业部署设计。它们可以被拆解吸收，但不能成为数字生命的中心。

吸收方式：

1. 只吸收 durable execution、trace、checkpoint、structured output、tool sandbox、memory store、workflow graph、MCP/A2A 接入。
2. 不吸收角色扮演式多 agent 人设。
3. 不用任务完成率替代九项生命目标。
4. 不用 prompt template 替代语言系统。
5. 不用 session memory 替代自传记忆、关系记忆、梦境记忆和责任记忆。
6. 不用 orchestration graph 替代脑区-网络-状态-调质-行为循环。

## 2026 外周框架刷新

| 框架/协议 | 当前可吸收能力 | 数字生命中的位置 | 主要来源 |
|---|---|---|---|
| OpenAI Agents SDK | Agents、structured outputs、harness、文件/系统能力、未来 code mode/subagents | `ExternalShellAdapter`、`RunnerCliRuntime`、tool sandbox | [OpenAI Agents SDK](https://platform.openai.com/docs/guides/agents-sdk/)、[Agents guide](https://openai.github.io/openai-agents-js/guides/agents/)、[next evolution](https://openai.com/index/the-next-evolution-of-the-agents-sdk) |
| LangGraph | graph runtime、durable execution、checkpoint、streaming、long-running stateful workflows | `ActivationGrowthRuntime`、`ReplayShadowRuntime`、checkpoint carrier | [LangGraph overview](https://langchain-ai.github.io/langgraph/)、[Persistence](https://langchain-ai.github.io/langgraph/cloud/concepts/threads/)、[Agent Server](https://langchain-ai.github.io/langgraph/tutorials/langgraph-platform/local-server/) |
| Google ADK | modular agents、tools/integrations、A2A/agent ecosystem、deployment | `ExternalShellAdapter`、tool registry、MCP/A2A bridge | [ADK](https://adk.dev/)、[ADK docs](https://google.github.io/adk-docs/)、[tools](https://adk.dev//tools/) |
| Microsoft Agent Framework | Semantic Kernel + AutoGen convergence、enterprise SDK、orchestration、MCP、Foundry integration | `ExternalShellAdapter`、enterprise shell adapter | [Overview](https://learn.microsoft.com/en-us/agent-framework/user-guide/overview)、[Version 1.0](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/)、[Build 2026](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-at-build-2026/) |
| CrewAI | role/task crew、multi-agent task pipelines、tool use、knowledge sources | 只作 multi-process task shell 反面参考和局部执行壳 | [CrewAI docs](https://docs.crewai.com/)、[CrewAI site](https://www.crewai.dev/) |
| LlamaIndex Workflows/Agents | RAG、knowledge indexing、agent workflows、durable workflow integrations | `DocCorpusIngestor`、knowledge/retrieval substrate | [LlamaIndex developers](https://developers.llamaindex.ai/) |
| Letta | stateful agents、long-term memory、context repositories、sleep-time compute | `MemoryEngramRuntime` 外周参考、context versioning | [Letta docs](https://docs.letta.com/)、[stateful agents](https://docs.letta.com/guides/agents/overview)、[memory](https://docs.letta.com/letta-code/memory/) |
| Claude Agent SDK | coding/agent harness、subagents、MCP patterns、programmatic agent runtime | `ExternalShellAdapter`、code shell reference | [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview) |
| MCP | tool/data protocol、server discovery、structured tool invocation | `ToolInterfaceMembrane`、external ability binding | [MCP spec](https://modelcontextprotocol.io/specification/2025-06-18/basic/index)、[GitHub spec](https://github.com/modelcontextprotocol/modelcontextprotocol) |

## 外周框架到工程模块映射

| 生命工程模块 | 可借鉴框架能力 | 不可借鉴内容 |
|---|---|---|
| `RunnerCliRuntime` | OpenAI harness、Claude Agent SDK CLI、Microsoft SDK command patterns | 把 CLI 当生命本体 |
| `ActivationGrowthRuntime` | LangGraph durable execution、Agent Server checkpoint | 把 graph 节点当脑区 |
| `ToolInterfaceMembrane` | MCP server contracts、ADK tools、OpenAI tools | 让工具调用绕过生命膜 |
| `DocCorpusIngestor` | LlamaIndex indexing、Letta context repositories | 用检索替代记忆 engram |
| `MemoryEngramRuntime` | Letta memory versioning、LlamaIndex retrieval | 用 session history 替代自传记忆 |
| `ExternalShellAdapter` | Google ADK、Microsoft Agent Framework、CrewAI shell | 角色团队式任务代理 |
| `ReportArchiveRuntime` | LangGraph checkpoints、OpenAI traces、MCP structured errors | 无 archive receipt 的运行成功 |

## 工程吸收顺序

第一轮只吸收：

1. CLI 命令模式。
2. structured JSON output。
3. durable checkpoint 概念。
4. tool/sandbox 接口边界。
5. trace/report/receipt 形状。

第二轮才吸收：

1. long-running workflow。
2. distributed runtime。
3. MCP/A2A tool registry。
4. external application adapter。
5. advanced memory/context repository。

第三轮才吸收：

1. multi-shell orchestration。
2. remote deployment。
3. external irreversible action pipeline。
4. model fine-tuning/self-training kernel。

## 外周壳风险

| 风险 | 说明 | 生命膜处理 |
|---|---|---|
| 编排幻觉 | graph 看起来像思考，但只是流程控制 | 所有 graph 节点必须绑定脑科学 carrier |
| memory 幻觉 | session/context 被误当长期记忆 | 必须写入 `MemoryEngramRuntime` 和 archive receipt |
| 工具越界 | tool 执行绕过责任/后悔/修复 | 进入 `ActionResponsibilityRuntime` 和 shadow gate |
| 关系降格 | 对话对象被写成任务输入 | 进入 `RelationshipSubjectGraph` |
| 语言降格 | prompt 被当语言系统 | 必须进入内言语、表达监控、共同语言和承诺链 |
| checkpoint 假稳定 | checkpoint 可恢复但不代表人格连续 | 必须接 old self replay 和 core continuity |

## 结论

外周 agent 框架只负责提供可以拆解的运行肌肉。数字生命工程的主干不是 agent orchestration，而是：

`脑区/网络 -> 身体信号 -> 记忆 engram -> 情绪人格自我 -> 语言关系 -> 梦境离线 -> 行动责任 -> 生命膜 -> 出生准备度 -> replay/shadow -> archive/growth`

第一次生命激活只把这些框架放到 `ExternalShellAdapter`，不让它们改变生命目标、关系结构、语言主神经束或自我成长路线。
