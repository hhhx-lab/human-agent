# Agentic Human 脑科学研究综述档案

本目录是一组围绕 `Agentic human plan` 的研究综述档案。它以 [构思.md](构思.md) 为源材料，把“以人脑结构为出发点的 human agent”先沉淀为脑科学研究底座，而不是直接进入产品规格或代码实现。

## 阅读路线

1. 先读 `00_research_protocol.md`，理解文献纳入标准、证据分级和边界声明。
2. 再读 `01_literature_matrix.md`、`01b_`、`01c_`、`01d_`，它们是全部综述的引用底座，当前覆盖核心综述、扩展机制、专业机制和前沿生命系统。
3. 按主题阅读 `02_` 到 `12_` 的综述文件：从脑区/网络、状态、调质、记忆、情绪、语言、意识，到 AI 架构桥接。
4. 接着读 `13_` 和 `14_`：前者给综合研究假设，后者把 `02-13` 连接成数字生命闭环。
5. 继续读 `15_` 和 `16_`：前者评估当前 agent 框架为什么只能作为执行壳，后者记录理论缺口和停止条件。
6. 再读 `17_` 到 `20_`：它们把记忆、内部状态、离线巩固和运行外壳转成未来数字生命实现前必须遵守的对象/接口约束。
7. 再读 `21_` 到 `24_`：它们把对象模型继续推进为 schema、状态阈值、巩固报告和 runtime adapter 测试。
8. 再读 `25_` 到 `28_`：它们把契约转成 JSON-like 样例、状态失败夹具、巩固报告样例和 runtime adapter manifest。
9. 再读 `29_` 到 `32_`：它们把样例层转成 validator rules，定义字段、状态、巩固和外壳的失败条件。
10. 最后读 `33_` 到 `36_`：它们定义 validator 输入输出、fixture catalog、最小 runner 设计和长期评测协议。

## 文件索引

| 文件 | 作用 |
|---|---|
| `00_research_protocol.md` | 研究协议、权威性评分、边界声明 |
| `01_literature_matrix.md` | 100 篇文献矩阵与研究启发 |
| `01b_extended_literature_matrix.md` | 第二批扩展文献锚点，覆盖主动推理、社会认知、发展、压力免疫、AI agent 等 |
| `01c_specialized_literature_matrix.md` | 第三批专业机制锚点，覆盖 replay、节律、持续学习、多模态具身、信任与评测等 |
| `01d_frontier_life_systems_matrix.md` | 第四批前沿生命系统锚点，覆盖动力学、主动推理、能量/免疫/脑清除争议、社会同步、发育和 agent 外壳等 |
| `01e_memory_runtime_evaluation_matrix.md` | 第五批记忆运行时与评测锚点，覆盖 agent memory、长期记忆 benchmark 和运行外壳资料 |
| `02_brain_region_and_network_atlas.md` | 脑区、连接组与大尺度网络 |
| `03_default_executive_salience_networks.md` | 默认模式、中央执行、显著性网络 |
| `04_sensory_thalamus_interoception.md` | 感觉输入、丘脑中继、内感受与稳态 |
| `05_memory_systems_and_growth.md` | 海马、记忆巩固、engram 与成长 |
| `06_action_reward_inhibition.md` | 基底节、动作选择、奖赏、惩罚与抑制 |
| `07_emotion_personality_self.md` | 情绪、人格、个体差异与自我 |
| `08_sleep_dream_fatigue_states.md` | 睡眠、梦境、发呆、疲惫与离线整合 |
| `09_language_symbolic_top_layer.md` | 语言网络与人类顶层符号能力 |
| `10_consciousness_attention_workspace.md` | 注意、意识与全局工作空间 |
| `11_neuromodulation_and_signal_media.md` | 神经调质、兴奋/抑制与信号介质 |
| `12_ai_and_cognitive_architecture_bridge.md` | 认知架构、LLM agent 与工程桥接 |
| `13_agentic_human_research_synthesis.md` | 总综合：从脑科学到 human-agent 研究假设 |
| `14_cross_module_digital_life_map.md` | `02-13` 跨模块连接与数字生命落地映射 |
| `15_current_agent_framework_survey.md` | 当前 agent 框架体系调研与数字生命差距 |
| `16_digital_life_gap_register.md` | 理论缺口登记、停止条件和下一轮专题优先级 |
| `17_memory_trace_object_model.md` | `MemoryTrace` 记忆痕迹对象模型 |
| `18_internal_state_and_modulation_vector.md` | `InternalStateVector` 与 `ModulationVector` 状态调质模型 |
| `19_offline_consolidation_cycle.md` | `OfflineConsolidationCycle` 离线巩固、replay、清理与梦境沙盒 |
| `20_agent_runtime_bridge_contract.md` | `AgentRuntimeBridge` 运行外壳契约 |
| `21_memory_schema_and_audit_protocol.md` | `MemoryTrace` schema、生命周期、删除/修正/合并与审计协议 |
| `22_state_transition_and_threshold_model.md` | 内部状态机、阈值、状态转移和 `StateAuditEvent` |
| `23_consolidation_report_and_dream_sandbox_protocol.md` | `ConsolidationReport` 与 `DreamSandbox` 事实写入门控 |
| `24_runtime_adapter_test_suite.md` | 运行外壳 adapter 合同测试与夹具 |
| `25_memory_trace_json_schema_examples.md` | `MemoryTrace`、审计事件、删除/修正/合并/保护的 JSON-like 样例 |
| `26_state_machine_examples_and_failure_modes.md` | 状态转移、阈值误判、恢复策略和 `StateAuditEvent` 样例 |
| `27_consolidation_report_examples.md` | `TaskClosure`、失败复盘、`DreamSandbox`、深度巩固和清理报告样例 |
| `28_runtime_adapter_manifest_examples.md` | LangGraph、OpenAI Agents SDK、Letta、LlamaIndex、CrewAI、AutoGen 等外壳 manifest 样例 |
| `29_memory_validator_rules.md` | `MemoryTraceValidator` 字段、证据、删除、修正、合并、保护和关系边界规则 |
| `30_state_transition_validator_rules.md` | `StateTransitionValidator` 状态、阈值、滞回、覆盖优先级和行动门控规则 |
| `31_consolidation_validator_rules.md` | `ConsolidationReportValidator` 沙盒、事实门控、深度巩固、删除和恢复包规则 |
| `32_runtime_adapter_validator_rules.md` | `RuntimeAdapterManifestValidator` 外壳 manifest、禁写、side effects、session/RAG 和合同测试规则 |
| `33_validator_input_contracts.md` | 四类 validator 的统一输入、输出、严重级别、阻断面和审计格式 |
| `34_validator_fixture_catalog.md` | 记忆、状态、巩固、运行外壳和纵向评测 fixture catalog |
| `35_minimal_validator_runner_design.md` | 最小本地 runner 的目录、流程、报告、覆盖和接入设计 |
| `36_longitudinal_evaluation_protocol.md` | 长期记忆一致性、人格慢变量、关系边界、恢复能力和成长轨迹评测协议 |

## 项目术语

原始构思中的区域代号继续保留为项目语言，但它们不是生物脑区的一对一复刻：

| 项目代号 | 原始含义 | 研究化解释 |
|---|---|---|
| L/R | 左右脑 | 半球偏侧化与跨半球协作，不等于绝对功能分工 |
| P | 大脑皮层 | 感知、运动、高级认知的分布式皮层系统 |
| J | 间脑 | 丘脑中继、下丘脑稳态、注意与唤醒调节 |
| G | 脑干 | 自主节律、生命维持、唤醒门控 |
| S | 小脑 | 时序校正、误差学习、动作与认知节律 |
| O | 边缘/记忆情绪系统 | 海马、杏仁核、扣带、伏隔核等记忆-情绪-动机系统 |
| D | 基底节 | 动作选择、习惯、强化学习、抑制 |

## 核心建模原则

- 不把脑区机械映射为单个 agent 模块；采用“脑区 - 网络 - 状态 - 调质 - 行为循环”的五层视角。
- 区分三种说法：`生物机制` 是文献支持的人脑机制；`工程类比` 是可借鉴的抽象；`设计假设` 是未来 human-agent 架构可能采用的研究方向。
- ACE 三层可以继续使用，但应被扩展：感知层包含外感受、内感受、丘脑中继与显著性过滤；处理层包含默认模式、执行控制、记忆系统、基底节选择；执行层包含行动、工具调用、小脑式校正与自治节律。
- 不宣称 AI agent 真实拥有意识、情绪或人格；只讨论仿脑启发下的功能组织方式。
