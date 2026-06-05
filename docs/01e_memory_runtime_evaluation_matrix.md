# 第五批记忆运行时与评测资料矩阵

本文件使用 `AHM` 编号，作为第五批实现/评测锚点。它不是脑科学核心文献，而是把当前 LLM agent 的记忆、运行时、长程评测和框架资料纳入可追溯边界。`AHM` 的作用是提醒我们：现有 agent memory 研究可以作为工程参考，但必须被 `02-20` 的生命层约束。

| ID | 领域 | 类型 | 资料 | 年份 | 链接/DOI | 核心结论 | Agentic Human 启发 | 风险/争议 |
|---|---|---|---|---:|---|---|---|---|
| AHM001 | agent memory | 经典工程论文 | Packer et al., "MemGPT: Towards LLMs as Operating Systems" | 2023 | https://arxiv.org/abs/2310.08560 | 通过虚拟上下文和显式记忆管理扩展 LLM 长期交互能力。 | `MemoryTrace` 需要写入/召回/分页式管理。 | 操作系统类比不等于生物记忆。 |
| AHM002 | stateful agents | 官方框架资料 | Letta, "Letta Documentation" | 2025 | https://docs.letta.com/ | Letta 提供 stateful agent、memory block 和工具运行时。 | 可作为长期状态外壳，不应直接成为自我模型。 | 框架 memory 不是自传记忆。 |
| AHM003 | agent memory | 研讨会论文 | Zhong et al., "MemoryBank: Enhancing Large Language Models with Long-Term Memory" | 2023 | https://arxiv.org/abs/2305.10250 | 长期记忆库可改善个性化和连续对话。 | 长期记忆要有用户/事件/偏好维度。 | 个性化容易带来隐私和过度记忆风险。 |
| AHM004 | 记忆评测 | 基准论文 | Wu et al., "LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory" | 2025 | https://openreview.net/forum?id=3gk1Zh1gpw | 长期互动记忆需要跨会话、时间和关系线索评测。 | 评测不能只看短上下文问答。 | benchmark 覆盖仍有限。 |
| AHM005 | 记忆评测 | 基准论文 | Liu et al., "MemBench: Towards More Comprehensive Evaluation on the Memory of LLM-based Agents" | 2025 | https://aclanthology.org/2025.findings-acl.1173/ | 从记忆写入、保持、召回和使用等方面评估 agent memory。 | `MemoryTrace` 需要独立评测写入、保持、检索和应用。 | 基准不等于真实长期关系。 |
| AHM006 | agent memory survey | 综述 | Singh et al., "Memory for Autonomous LLM Agents: A Survey" | 2026 | https://arxiv.org/abs/2603.07670 | 综述自主 LLM agent 的 memory 表征、操作和评测。 | 记忆层应区分 storage、retrieval、update、forgetting。 | 新综述需持续跟进版本。 |
| AHM007 | agent memory survey | 综述 | Kotecha et al., "A Survey on the Memory Mechanism of Large Language Model based Agents" | 2026 | https://openreview.net/forum?id=xu4AElQuWs | 归纳 LLM agent memory 机制和挑战。 | 工程记忆需连接任务、长期身份和安全。 | OpenReview 版本可能变化。 |
| AHM008 | 认知启发记忆 | 工程论文 | Gao et al., "Towards Cognitive AI Memory for LLM Agents" | 2025 | https://arxiv.org/abs/2505.13044 | 提出更接近认知过程的 AI memory 框架。 | 可作为 `MemoryTrace` 分层的工程参照。 | 认知启发仍需脑科学约束。 |
| AHM009 | 长程记忆评测 | 工程论文 | Pham et al., "MemInsight: Autonomous Memory Augmentation for LLM Agents" | 2025 | https://arxiv.org/abs/2506.13925 | 探索 agent 自主记忆增强和洞察生成。 | 记忆增强必须经过事实与价值审计。 | 自主写入可能放大幻觉。 |
| AHM010 | 记忆管理影响 | 工程论文 | Jang et al., "How Memory Management Impacts LLM Agents" | 2025 | https://arxiv.org/abs/2505.16067 | 记忆管理策略会显著影响 agent 表现。 | memory policy 是核心能力，不是存储细节。 | 结果依赖任务设计。 |
| AHM011 | 长程记忆评测 | 基准论文 | Wu et al., "LongMemEval-V2: Towards Deeper Understanding and Improved Evaluation of Long-term Memory in LLMs" | 2026 | https://arxiv.org/abs/2605.12493 | 进一步细化长期记忆能力评估。 | 需要评估时间、矛盾、关系和上下文漂移。 | 未来版本可能更新。 |
| AHM012 | agent memory benchmark | 基准资料 | Hu, Wang & McAuley, "Evaluating Memory in LLM Agents via Incremental Multi-Turn Interactions" | 2026 | https://arxiv.org/abs/2507.05257 | MemoryAgentBench 从准确检索、测试时学习、长程理解和冲突解决评估 agent memory。 | 可作为后续 `MemoryTrace` 测试参考。 | 仍需结合真实项目和关系记忆评测。 |
| AHM013 | LangGraph memory | 官方框架资料 | LangChain, "Memory" | 2025 | https://docs.langchain.com/oss/python/langgraph/memory | LangGraph 把 memory 分为 thread-scoped 和 long-term memory。 | 可作为工作区/长期记忆外壳。 | 框架 memory 粒度仍偏工程状态。 |
| AHM014 | LangGraph persistence | 官方框架资料 | LangChain, "Persistence" | 2025 | https://docs.langchain.com/oss/python/langgraph/persistence | checkpoint 和 persistence 支持 durable execution。 | checkpoint 是行动外壳的审计基础。 | checkpoint 不等于生物巩固。 |
| AHM015 | OpenAI Agents sessions | 官方框架资料 | OpenAI, "Sessions" | 2025 | https://openai.github.io/openai-agents-python/sessions/ | Sessions 提供跨轮会话历史管理。 | 可作为短期工作区外壳。 | session history 不是长期记忆。 |
| AHM016 | OpenAI Agents tracing | 官方框架资料 | OpenAI, "Tracing" | 2025 | https://openai.github.io/openai-agents-python/tracing/ | tracing 记录 agent、工具调用和运行事件。 | 运行日志必须进入审计队列。 | tracing 不能自动判断价值和人格漂移。 |
| AHM017 | LlamaIndex memory | 官方框架资料 | LlamaIndex, "Agents" | 2025 | https://docs.llamaindex.ai/en/stable/use_cases/agents/ | LlamaIndex agent 连接 RAG、tools 和 workflow。 | 适合作为资料层与检索外壳。 | RAG 命中不等于记忆重构。 |
| AHM018 | AutoGen runtime | 官方框架资料 | Microsoft, "AutoGen Documentation" | 2025 | https://microsoft.github.io/autogen/ | AutoGen 支持多 agent teams、tools 和 conversation runtime。 | 可作为多角色执行外壳。 | 多 agent 对话不等于社会脑。 |
| AHM019 | CrewAI flows | 官方框架资料 | CrewAI, "Flows" | 2025 | https://docs.crewai.com/concepts/flows | Flows 提供事件驱动和流程编排。 | 可作为行动编排外壳。 | flow 不能取代生命层状态机。 |
| AHM020 | memory governance | 工程论文 | Wang et al., "ReMem: Retrieval-Augmented Memory for LLM Agents" | 2025 | https://arxiv.org/abs/2502.09357 | 探索检索增强记忆对 agent 的影响。 | 记忆检索要结合事件、价值和关系上下文。 | 检索增强仍可能带入错误或过时痕迹。 |
