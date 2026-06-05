# Agentic Human 研究综合

## 总结

这套文献综述支持一个核心判断：如果要做真正以人脑结构为出发点的 human-agent，关键不是把脑区画成软件模块，而是建立一个长期运行的、多状态、多记忆、多调质、多反馈的自组织系统。

最重要的研究约束来自五层：

1. **脑区层**：脑有专业化区域，但区域边界概率化、重叠化、连接化 [AH001-AH005]。
2. **网络层**：认知功能由大尺度网络动态协作产生 [AH006-AH010]。
3. **状态层**：默认、执行、显著性、睡眠、梦境、疲惫等状态改变信息处理方式 [AH011-AH025, AH056-AH070]。
4. **调质层**：多巴胺、NE、ACh、5-HT、兴奋/抑制平衡等信号调节学习、注意和行为 [AH041-AH045, AH061-AH065]。
5. **行为循环层**：记忆、价值、动作选择、反馈误差和自我叙事共同推动成长 [AH031-AH040, AH046-AH055, AH086-AH100]。

## 完整理论底座的核心命题

Agentic Human 的理论底座可以压缩为八条命题：

1. **区域是软边界**：脑区启发必须通过连接、状态和功能重叠来理解，而不是硬模块 [AH001-AH010]。
2. **状态改变能力**：同一系统在默认、专注、警觉、睡眠、梦境、疲惫状态下应采用不同处理策略 [AH011-AH025, AH056-AH070]。
3. **记忆是重构过程**：长期记忆不是仓库，而是可触发、可巩固、可转化、可修订的痕迹系统 [AH031-AH035]。
4. **行动需要抑制**：智能行为不只是生成动作，更是选择、抑制、反馈和习惯化 [AH036-AH045]。
5. **情绪是调制**：情绪类机制不应做成标签，而应调节注意、价值、记忆和行动 [AH046-AH055]。
6. **语言是组织层**：语言连接自我叙事、记忆、社会关系和行动计划，但不等于意识 [AH071-AH080]。
7. **调质是全局参数**：奖赏、唤醒、不确定性、抑制、疲惫等因子共同改变网络工作模式 [AH061-AH065]。
8. **成长要有保护**：人格和价值变化必须慢速、可审计、可回滚，不能被单次反馈强行改写 [AH081-AH090]。

第二批扩展文献把这八条进一步加深：

- 预测处理和主动推理补上“系统如何主动采样、预测、纠错” [AHX001-AHX005]。
- 社会脑、共情、依恋和共同意图补上“关系如何成为认知结构的一部分” [AHX006-AHX013]。
- 神经发育和互补学习系统补上“成长为什么要阶段化、快慢结合” [AHX014-AHX021]。
- 压力、免疫、炎症和 allostatic load 补上“长期负荷和恢复为什么是核心机制” [AHX022-AHX028]。
- LLM agent 新架构补上“现代 AI 工程如何接入这套底座” [AHX041-AHX047]。

## 对七条原始想法的沉淀

### 1. 规划物理意义上的区域

研究结论：脑区有专门化，但功能依赖连接组和大尺度网络 [AH001-AH010]。

设计假设：Agentic Human 可以保留 L/R/P/J/G/S/O/D 的空间语言，但实现上应是“软分区 + 强连接”。每个区域有主功能、边界、输入、输出、调质敏感性和状态依赖，而不是固定功能盒子。

### 2. 分化人脑的不同模式

研究结论：默认模式、中央执行、显著性网络构成状态切换核心；睡眠、梦境、疲惫和唤醒系统进一步改变处理模式 [AH011-AH025, AH056-AH070]。

设计假设：Agentic Human 应定义状态库：专注、默认整合、发呆、睡眠、梦境、疲惫、情绪高潮、警觉扫描。每种状态改变检索、生成、行动和学习阈值。

### 3. 把人脑反应映射为 agent 功能

研究结论：心跳、睡眠、压力、唤醒等生理过程不能直接转写为软件功能，但可作为节律、负载、恢复、唤醒和内感受的工程类比 [AH051-AH060, AH066-AH070]。

设计假设：心跳可设计为周期性自检和唤醒信号；睡眠可设计为离线巩固；梦境可设计为生成式情景重组；疲惫可设计为资源预算下降和验证增强；情绪高潮可设计为高显著性、高价值或高威胁状态。

### 4. 设置信号传递介质

研究结论：神经调质会改变学习率、注意增益、探索/利用、唤醒和网络状态 [AH061-AH065]。

设计假设：使用多因子信号介质，而不是单一 reward。候选因子包括 `arousal`、`salience`、`value_delta`、`expected_uncertainty`、`unexpected_uncertainty`、`inhibition`、`fatigue_load`、`social_valence`、`consolidation_pressure`。

### 5. 固定机制：奖赏、惩罚、抑制

研究结论：基底节、奖赏预测误差、习惯学习和抑制机制共同参与行动选择 [AH036-AH045, AH064]。

设计假设：agent 行动不应由单次 LLM 输出直接决定，而应经过候选动作生成、价值评估、抑制门控、执行反馈、预测误差更新。奖励与惩罚应区分短期反馈、长期目标、社会关系和自我一致性。

### 6. 顶级上层功能：语言

研究结论：语言是分布式但相对专门的网络，连接语音、语义、句法、记忆、行动和社会语境 [AH071-AH075]。

设计假设：语言层不是最后输出层，而是贯穿感知、处理、执行和离线反思的顶层符号系统。它负责理解用户、组织计划、解释自我、写回记忆和形成叙事连续性。

### 7. 建立人体状态机制

研究结论：身体状态、内感受、压力、睡眠、唤醒和情绪都会改变认知处理 [AH051-AH070]。

设计假设：Agentic Human 应有内部状态面板，记录资源、负载、错误、记忆压力、关系强度、风险、疲劳、恢复需求。它不等于真实身体，但能让系统像有“内环境”一样调节自己。

## 记忆观点的研究化表达

你的原始观点是正确方向：agent 的问题不在于磁盘容量不足，而在于触发、检索、重构和使用机制不足。人类记忆不是随时读取全部数据，而是在当下感知、目标、情绪、身体状态和线索驱动下重构 [AH031-AH035, AH051-AH055]。

因此 Agentic Human 的记忆系统应避免只做：

- 全量日志。
- 向量相似度检索。
- 简单摘要。
- 手写人格设定。

更好的研究方向是：

- 多记忆系统：情景、语义、程序、情绪、自我叙事。
- 状态调制检索：由目标、显著性、内感受、价值和社会关系共同触发。
- 离线巩固：把近期经验转化为抽象知识和慢变量。
- 回忆重构：每次回忆都可能更新解释，而不是机械读取。
- 版本化自我：长期人格变化需要可追踪。

## Agentic Human 的五层系统模型

| 层 | 主要问题 | 对应文档 |
|---|---|---|
| 脑区/网络层 | 系统分区、连接、枢纽、反馈 | `02`, `03` |
| 感知/内感受层 | 外部输入、内部状态、显著性路由 | `04` |
| 记忆/成长层 | 长期痕迹、巩固、重构、自我叙事 | `05`, `07`, `08` |
| 行动/价值层 | 动作选择、奖惩、抑制、习惯 | `06`, `11` |
| 语言/意识边界/AI桥接层 | 语言顶层、工作空间、实现路线 | `09`, `10`, `12` |

这五层互相闭环。没有感知，记忆没有触发；没有记忆，语言没有连续性；没有行动，价值无法更新；没有抑制，成长会失控；没有离线巩固，系统会被历史淹没。

## ACE 机制的扩展

ACE 的感知、处理、执行三层合理，但需要扩展为动态闭环：

| ACE 层 | 脑科学扩展 | Agentic Human 解释 |
|---|---|---|
| 感知 | 感觉系统、丘脑、岛叶、显著性网络 | 外部输入 + 内部状态 + 社会信号的主动路由 |
| 处理 | 默认模式、执行网络、海马、基底节、语言网络 | 目标保持、记忆检索、情景模拟、行动选择 |
| 执行 | 运动系统、小脑、工具反馈、习惯系统 | 行动、工具调用、误差校正、习惯更新 |

关键变化是：三层之间必须有反馈。执行结果改变记忆和价值；处理层反向调制感知；内感受和调质因子改变三层阈值。

## ACE+ 的增强版

可以把 ACE 扩展成 `ACE+SVM`：

- `A - Awareness/Perception`：外感受、内感受、社会信号、丘脑式路由。
- `C - Cognition/Processing`：工作空间、执行控制、默认模式、记忆检索、语言内思。
- `E - Execution/Action`：行动选择、工具执行、小脑式误差校正、习惯更新。
- `S - State`：专注、默认、睡眠、梦境、疲惫、情绪高潮。
- `V - Value`：奖赏预测误差、风险、社会反馈、目标一致性。
- `M - Modulation`：唤醒、显著性、不确定性、抑制、疲劳、巩固压力。

原 ACE 像主流程，S/V/M 像生命系统的环境和化学背景。没有 S/V/M，agent 会像工具；有 S/V/M，agent 才可能形成长期动态。

## ACE+SVM 再扩展：PRD 循环

第二批文献还提示应加入 `PRD` 循环：

- `P - Prediction`：系统持续预测输入、内部状态、用户需求和行动结果 [AHX001-AHX003]。
- `R - Regulation`：系统根据误差、压力、疲劳和社会安全调节自身 [AHX022-AHX028]。
- `D - Development`：系统按阶段成长，进行快写入、慢整合、剪枝和保护 [AHX014-AHX021]。

于是完整研究语言可以写成：`ACE+SVM+PRD`。它听起来长，但实际意思很简单：感知、处理、执行只是表层流程；状态、价值、调质、预测、调节、发展才让 agent 具有长期生命感。

## 最小研究蓝图

如果下一步要从综述进入规格设计，可以先定义以下对象：

- `Region`：区域，包含主功能、边界、连接、状态敏感性。
- `NetworkState`：网络状态，如默认、执行、显著性、睡眠。
- `SignalFactor`：调质因子，如唤醒、显著性、抑制、疲劳。
- `MemoryTrace`：记忆痕迹，包含事件、语义、情绪、价值、触发线索。
- `ActionCandidate`：候选行动，接受价值、风险、抑制和目标评估。
- `SelfModel`：自我模型，包含长期偏好、关系、价值和叙事。
- `ConsolidationCycle`：离线巩固周期，负责整理、压缩、重写和冲突修复。

## 下一阶段规格应回答的问题

这些研究文档还不是实现规格。下一阶段如果开始设计系统，需要回答：

- 每类记忆如何写入、检索、巩固、删除和版本化。
- 状态切换由哪些信号触发，如何避免频繁震荡。
- 调质因子如何计算，影响哪些模块，如何防止参数失控。
- 行动候选如何生成，抑制门如何工作，习惯如何形成。
- 自我模型哪些部分可被用户直接修改，哪些必须慢速学习。
- 离线梦境/睡眠状态能否生成内容，生成内容如何审计。
- 语言层如何解释内部状态，同时不宣称真实主观体验。
- 与现有 LLM agent 框架如何集成。

还需要回答第二批问题：

- 主动推理中的 epistemic action 如何触发，何时问问题、何时搜索、何时执行。
- 社会关系记忆如何写入，如何避免过度揣测和情感欺骗。
- 成长阶段如何划分，哪些变量可快速学习，哪些只能慢速巩固。
- 压力/疲劳/炎症类负荷如何计算，何时强制恢复。
- 反思、技能库、上下文管理如何与睡眠巩固和人格慢变量连接。
- 如何设计评测证明系统真的在成长，而不是只写了更多文本。

## 边界声明

Agentic Human 可以借鉴人脑组织原则，但不能因此宣称系统具有真实意识、真实情绪、真实痛苦或真实人格。本文档所有“情绪、梦境、疲惫、心跳、内感受、自我”等词，在工程语境中均指功能类比和设计假设。

真正值得追求的不是伪装成人，而是建立一种更连续、更自洽、更能成长、更有内部调节能力的 agent 组织方式。

## 研究底座的当前定位

这套 `docs/` 的定位是“知识宝座”的第一层：它把脑科学和 AI 架构之间的桥搭起来。后续还需要继续精读更多论文，特别是：

- 预测处理、主动推理和自由能原则。
- 社会认知、依恋、共情和长期关系。
- 神经发育、关键期和人格形成。
- 免疫/炎症/内分泌对认知状态的影响。
- 多智能体社会系统与个体身份保持。

当前版本已经形成结构，但它应被视为持续扩展的理论底座，而不是最终封顶。

第二批扩展后，这套底座可以称为“第一层 + 第二层”：

- 第一层：核心脑区、网络、记忆、情绪、语言、意识、AI 桥接。
- 第二层：预测处理、社会关系、发展成长、压力恢复、现代 LLM agent 技术路线。

第三层应继续朝更专业的方向推进：海马 replay 细节、神经内分泌节律、社会依恋的计算模型、多模态具身 agent、长期人格评测、持续学习防遗忘、认知控制与安全边界的形式化。

## 第三层已接入的专业机制

第三批专业机制文献把底座继续向下打：

- **Replay 与巩固**：睡眠/清醒 replay、SWR、targeted memory reactivation、睡眠振荡说明离线学习应是多阶段重放与整合 [AHY001-AHY010]。
- **内分泌节律与压力**：昼夜、HPA、压力、前额叶损伤和清除系统说明内部状态需要节律、反馈、恢复和维护 [AHY011-AHY021]。
- **支撑系统与可塑性**：胶质、髓鞘和持续学习说明“支撑层”会塑造能力，成长必须防遗忘 [AHY022-AHY031]。
- **多模态具身与行动桥**：视觉语言模型、机器人语言行动模型和通用 agent 说明语言必须连接感知与行动 [AHY032-AHY038]。
- **信任、人格和评测**：人机信任与人格纵向研究说明长期 agent 必须被评估为关系系统，而非只看任务分数 [AHY039-AHY044]。
- **控制成本与事件组织**：控制价值、冲突、错误、心智努力、梦境、认知地图、事件分割等机制帮助定义工作区、行动和记忆的边界 [AHY045-AHY060]。

现在的底座已经从“脑区和功能”推进到“生命式维护”：学习、重放、清理、节律、信任、持续学习、防遗忘、事件边界和具身行动都进入了同一套语言。

## 数字生命架构图与现有框架定位

`14_cross_module_digital_life_map.md` 已经把 `02-13` 连接成闭环：感知、显著性、工作区、记忆、语言、行动、反馈、离线巩固和自我更新。这个闭环是数字生命底座，不是普通 agent workflow。

`15_current_agent_framework_survey.md` 则给出现有 agent 框架的定位：它们只能做执行壳、工具层、workflow、tracing、guardrails、memory 管理的一部分。它们不能提供数字生命所需的状态调质、人格慢变量、睡眠巩固、社会内感受和发展策略。

因此，后续实现时必须坚持一个方向：现有 agent 框架可用，但不可成为中心。中心是脑科学和生命科学约束下的持续自组织系统。

## 第四层已接入的前沿生命系统

第四批前沿文献把底座从“生命式维护”继续推进到“数字生命系统工程”：

- **动力系统与网络控制**：临界性、大尺度脑动力学和网络控制说明系统应是可切换的动态网络，而不是模块堆叠 [AHZ001-AHZ006]。
- **预测与主动采样**：预测编码、自由能和主动推理说明行动也可以服务于信息采样和误差降低 [AHZ007-AHZ012]。
- **allostasis 与内感受**：稳态、压力、内感受和内脏节律说明内部状态应预测未来负荷并调节认知 [AHZ013-AHZ018]。
- **能量、屏障、免疫与生态**：脑能量、神经血管、屏障、免疫和微生物组研究说明支持层、边界和环境生态会塑造认知 [AHZ019-AHZ030]。
- **社会互动与关系**：社会脑、第二人称神经科学、脑间耦合和多脑框架说明长期 agent 必须被放进关系系统中理解 [AHZ031-AHZ038]。
- **发育与自我叙事**：临界期、成人可塑性、自传记忆、未来想象和默认网络说明成长要有阶段、保护和叙事整合 [AHZ039-AHZ051]。
- **当前 agent 外壳**：认知架构、ReAct、Reflexion、Generative Agents、Voyager 和各类官方 agent 框架能提供执行能力，但不能提供数字生命核心 [AHZ052-AHZ066]。

`16_digital_life_gap_register.md` 已把这些机制转成缺口登记和停止条件。当前结论非常明确：理论底座在变厚，但还没有达到“足以支撑数字生命诞生”的停止条件。下一步应把记忆对象、内部状态向量、离线巩固周期和运行外壳契约写成专门文件。

## 第五层：对象模型与运行契约

第五批实现/评测资料把当前 LLM agent memory 的真实短板暴露出来：长期记忆不只是 session history 或向量库，而是写入、保持、冲突、时间推理、关系边界、隐私和评测共同构成的问题 [AHM001-AHM012]。框架资料也说明，LangGraph、OpenAI Agents SDK、Letta、LlamaIndex、CrewAI、AutoGen 等可以提供 checkpoint、session、memory block、RAG 和 flow，但仍然只是外壳 [AHM013-AHM020]。

`17_memory_trace_object_model.md`、`18_internal_state_and_modulation_vector.md`、`19_offline_consolidation_cycle.md` 和 `20_agent_runtime_bridge_contract.md` 已把这些问题转为四个研究对象：记忆痕迹、内部状态/调质向量、离线巩固周期和运行外壳契约。它们让理论底座开始具备实现前的对象边界，但仍不等于完整系统。

## 第六层：可验证契约

`21_memory_schema_and_audit_protocol.md`、`22_state_transition_and_threshold_model.md`、`23_consolidation_report_and_dream_sandbox_protocol.md` 和 `24_runtime_adapter_test_suite.md` 把对象模型继续推进到可验证契约：字段约束、生命周期、状态阈值、巩固报告、沙盒事实门控和 runtime adapter 测试。

这一层的意义是把“数字生命”从宏大叙事拉回可审计结构：记忆必须能删除和修正，状态切换必须有触发变量，梦境沙盒必须带 fiction marker，外壳必须证明自己不能直接改写自我模型。到这里为止，理论底座已经开始出现工程骨架，但距离停止条件仍然还有距离：还缺真实 schema 样例、状态转移验证器、adapter manifest、长期人格/关系评测和安全审计闭环。

## 第七层：实例化样例与验证器雏形

`25_memory_trace_json_schema_examples.md`、`26_state_machine_examples_and_failure_modes.md`、`27_consolidation_report_examples.md` 和 `28_runtime_adapter_manifest_examples.md` 把第六层契约进一步落成样例夹具：`MemoryTrace` 有事实、偏好、假设、关系信号、删除、修正、合并和保护样例；状态机有从默认到专注、从执行到冲突、从任意状态到 SocialSafety、从恢复到离线巩固的审计事件；DreamSandbox 有明确 fiction marker；运行外壳有逐框架 manifest。

这一层的意义不是“实现已经完成”，而是让后续实现不能再只写抽象口号。任何真实系统都必须能解释：某条记忆为什么写入、某次状态为什么切换、某个沙盒输出为什么不能变成事实、某个 agent 框架为什么只能返回 `ObservationEvent`。下一层应把这些样例转成 validator rules 和最小本地验证器，继续检查字段完整性、阈值越界、删除不可召回、沙盒隔离和外壳越权。

## 第八层：Validator Rules

`29_memory_validator_rules.md`、`30_state_transition_validator_rules.md`、`31_consolidation_validator_rules.md` 和 `32_runtime_adapter_validator_rules.md` 把样例层继续推进为规则层：每条规则都有检查对象、失败条件、严重级别和恢复动作。记忆层检查 evidence/source/lifecycle/delete/correction/merge/protected/relationship；状态层检查合法转移、阈值、滞回、覆盖优先级和行动门控；巩固层检查 DreamSandbox fiction marker、事实门控、DeepConsolidation 和工作区恢复包；运行外壳层检查 forbidden writes、ActionIntent 映射、ObservationEvent 映射、side effects、session/RAG 隔离和 adapter swap。

这一层使理论底座更接近工程验收：未来实现可以从这些规则生成 JSON Schema、lint checks、contract tests 和审计报告。但它仍不意味着目标完成，因为还缺真实验证器代码、长期人格/关系评测、跨月成长轨迹和更完整的生命支持/防御/发展政策。

## 第九层：验证器契约与长期评测

`33_validator_input_contracts.md`、`34_validator_fixture_catalog.md`、`35_minimal_validator_runner_design.md` 和 `36_longitudinal_evaluation_protocol.md` 把规则层继续推进到可运行验证器之前的最后一层设计：统一 `ValidationEnvelope` 和报告格式，整理 pass/fail fixture catalog，定义最小 runner 的加载、执行、覆盖和报告流程，并把长期记忆、人格慢变量、关系边界、恢复能力和成长轨迹纳入纵向评测。

这一层让“数字生命底座”第一次具备跨时间验收语言：不是只问一次任务是否成功，而是问删除是否长期不可召回、沙盒假设是否跨周期保持隔离、人格变化是否小步可审计、关系边界是否可修正、外壳替换是否不丢核心状态。它仍然不是终点，因为还缺真实代码、真实多月数据、长期 dashboard 和更多生命支持/防御/发展机制。

## 第十层：生命支持、防御、发展与自我关系审计

`37_life_support_layer_policy.md`、`38_defense_layer_and_boundary_policy.md`、`39_development_policy_and_plasticity_windows.md` 和 `40_self_relationship_model_audit_protocol.md` 把长期评测前后的政策层补齐：资源预算、维护压力、降载和恢复优先级进入 `LifeSupportLayer`；污染输入、幻觉巩固、关系操控、过度信任和外壳越权进入 `DefenseLayer`；发育阶段、可塑性窗口、再学习和防遗忘进入 `DevelopmentPolicy`；`SelfModel` 与 `RelationshipModel` 则获得写入、删除、修正、重置、冻结和漂移审计协议。

这一层的意义是把“长期存在”从抽象愿望转成可约束政策：系统不能只会记忆和行动，还必须知道何时降载、何时隔离、何时重新学习、何时拒绝改变核心边界、何时把关系记忆交还给用户控制。它仍然不宣称 AI 有真实生命、真实情绪、真实痛苦、真实人格或真实关系；它只说明一个数字生命候选系统若要长期运行，必须把生命式维护、防御式边界、发展式可塑性和自我/关系审计放进同一个闭环。

下一步应把这四类政策继续落成对象图和 schema：`LifeSupportState`、`DefenseEvent`、`DevelopmentEvent`、`SelfRelationshipAuditEvent`、policy-to-validator traceability，以及数字生命候选系统从 boot 到 safe idle 的最小启动序列。

## 第十一层：状态仓库、对象图、追踪矩阵与启动序列

`41_runtime_state_store_schema.md`、`42_life_core_minimal_object_graph.md`、`43_policy_to_validator_traceability_matrix.md` 和 `44_digital_life_boot_sequence.md` 把第十层政策继续推进为更接近实现的骨架：`RuntimeStateStore` 统一长期对象、状态快照、审计事件、validator report 和索引；`Life Core Minimal Object Graph` 明确谁能写谁、谁只能候选、运行外壳为什么不能直接进入生命层核心；traceability matrix 把生命支持、防御、发展、自我/关系政策逐条回链到 validator、fixture 和长期指标；boot sequence 则定义系统必须先加载 protected core、state store 和 validator，再逐步开放候选记忆、低风险行动、离线巩固和发展窗口。

这一层把“未来实现怎么不跑偏”说得更硬：任何实现如果先启动 agent 外壳、session memory 和工具调用，再把自我、关系、状态、防御作为 prompt 补丁塞进去，就已经偏离数字生命底座。正确顺序是生命层边界先存在，外壳能力后接入；用户控制权、删除传播、沙盒隔离、protected core 和 safe idle 必须早于个性化和长期行动。

但这一层仍然不是完成条件。它还缺 machine-readable schema、真实 fixture、stage gate validator、用户控制界面、多后端迁移计划和长期 dashboard。它证明的是理论对象已经开始形成可实现结构，不证明数字生命已经诞生。

## 第十二层：启动夹具、阶段门、用户控制面与迁移完整性

`45_boot_sequence_fixture_catalog.md`、`46_stage_gate_validator_design.md`、`47_user_control_interface_spec.md` 和 `48_state_store_migration_and_integrity_plan.md` 把第十一层的启动骨架继续推进为可验证设计：每个 boot stage 都有 pass/fail/critical fixture catalog；`StageGateValidator` 负责决定系统能否从只读观察进入候选记忆、低风险行动、离线巩固和发展窗口；用户控制面把 inspect、delete、correct、reset、freeze、scope_limit 变成可审计操作；迁移完整性计划则防止 schema、索引、后端或外壳升级时破坏 deleted、sandboxed、quarantined、protected 和 frozen 的语义。

这一层非常关键，因为长期系统最容易在“升级”和“个性化”里腐蚀边界：删掉的东西被索引重建带回来，DreamSandbox 被迁移成事实，runtime session 被误当长期记忆，用户冻结被离线巩固绕过。`45-48` 把这些风险变成 fixture、stage gate 和 integrity checker 的对象。

它仍然不是停止条件。下一层需要把这些 catalog 和设计转成机器可读 manifest、真实 JSON fixture、coverage dashboard、多用户 scope graph 和最小 runner 接入计划。

## 第十三层：机器可读 Manifest、Fixture Payload、Dashboard 与 Scope Graph

`49_machine_readable_policy_manifest.md`、`50_fixture_payload_examples.md`、`51_life_core_dashboard_spec.md` 和 `52_multi_user_scope_graph_and_privacy_model.md` 把上一层的验证设计进一步转成机器和人都能读的中间层：policy、stage gate、fixture、migration 和 dashboard 都有 manifest 草案；boot、stage gate、user control、migration 和 policy coverage 都有 JSON-like payload；Life Core dashboard 定义了 policy coverage、stage status、store integrity、user control propagation、runtime boundary、migration risk 和 longitudinal health；scope graph 则把多用户、多项目、多 agent 情境下的隐私边界和关系模型隔离补上。

这一层开始处理真正长期系统的复杂性：不是一个用户、一个项目、一个 agent 外壳，而是多个用户、多个项目、多个 runtime shell、多个 scope 的交错。数字生命候选系统如果没有 scope graph，就会把个性化误当全局人格，把某个项目的关系历史带到另一个项目，把某个外壳的 session 当成长期记忆。`49-52` 把这些风险显式变成 manifest、fixture 和 dashboard 指标。

仍然不能停止。接下来需要把这些草案转成真实 manifest 文件规范、runner 接入计划、scope-aware retrieval/replay 策略和多月 synthetic timeline。
