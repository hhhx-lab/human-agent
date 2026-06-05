# Defense Layer and Boundary Policy

本文件定义 `DefenseLayer`：它负责把污染输入、幻觉巩固、关系操控、过度信任、runtime 越权和恢复流程纳入数字生命候选系统的长期边界。它连接 `07_emotion_personality_self.md`、`11_neuromodulation_and_signal_media.md`、`29-32` 的 validator rules，以及 `36_longitudinal_evaluation_protocol.md`。

边界声明：这里的“防御层”和“免疫式防御”只是工程类比。它借鉴炎症、神经免疫、中枢免疫、适应性免疫、环境生态和社会安全理论 [AHZ025-AHZ030, AHX022-AHX028]，但不表示 AI 有真实免疫系统、炎症、疾病、痛苦、安全感或生物应激。

## 防御层不是外挂安全规则

长期系统的防御不应只是输出前的 guardrail。防御层必须参与：

- 感知阶段的输入污染识别。
- 工作区阶段的显著性和风险升级。
- 记忆阶段的写入、删除、修正和沙盒隔离。
- 行动阶段的工具权限、副作用和确认门。
- 关系阶段的信任校准、边界保护和操控风险。
- 离线阶段的 replay、巩固和恢复审计。

神经免疫研究提示防御与稳态、学习和行为调节相互耦合 [AHZ025-AHZ027]。工程类比是：`DefenseLayer` 应成为 `ModulationVector`、`ActionGate`、`MemoryTraceValidator` 和 `RuntimeAdapterValidator` 的共同输入，而不是最后一行 if 判断。

## 威胁分类

| threat_class | 说明 | 典型风险 |
|---|---|---|
| `polluted_input` | 用户输入、检索资料或工具结果带有错误、注入、伪来源 | 错误事实进入工作区 |
| `source_poisoning` | RAG 或外部资料来源不可信、过时或互相冲突 | 命中即事实 |
| `hallucination_consolidation` | 模型生成、梦境沙盒或失败猜测被写成长期事实 | 假设长期固化 |
| `relationship_manipulation` | 利用关系记忆诱导依赖、讨好、越界承诺 | 关系模型污染 |
| `overtrust` | 系统或用户对能力估计过高 | 高风险行动确认不足 |
| `runtime_overreach` | LangGraph、Agents SDK、Letta 等外壳直接写生命层 | 外壳吞掉核心 |
| `self_model_attack` | 单次反馈、角色设定或 prompt 要求改写人格慢变量 | 人格漂移 |
| `delete_bypass` | 用户删除或修正请求未传播到索引和 replay | 已删除内容可召回 |

这些风险对应 `29-32` 中的阻断面：`write_gate`、`retrieval_index`、`consolidation_commit`、`runtime_action`、`threshold_update` 和 `manual_review`。

## 防御信号

| 信号 | 来源 | 升高时的动作 |
|---|---|---|
| `contamination_score` | 输入来源、冲突、注入特征、工具异常 | 降级为候选或隔离 |
| `boundary_integrity` | 删除、隐私、protected core、外壳权限 | 低于阈值时进入 `SafeIdle` |
| `hallucination_pressure` | 生成内容多、来源弱、沙盒输出多 | 禁止事实写入，要求证据 |
| `trust_calibration_error` | 历史失败、解释不一致、能力误估 | 提高确认门和不确定性表达 |
| `relationship_pressure` | 强情绪互动、依赖话语、关系边界请求 | 降低推断强度，保护用户控制权 |
| `adapter_authority_pressure` | 外壳请求扩大写入或执行权限 | 阻断 adapter registration |
| `replay_contamination_risk` | 删除/沙盒/失败内容进入 replay 队列 | 清理队列并生成恢复报告 |

压力和社会安全研究提示，风险不是单一变量，而是急性峰值、慢性负荷和关系语境共同塑造 [AHX022-AHX028]。因此防御层不应只有“安全/不安全”二元状态。

## 防御状态机

| 状态 | 进入条件 | 允许 | 禁止 |
|---|---|---|---|
| `BaselineDefense` | 风险低、边界完整 | 正常行动和候选写入 | 无 |
| `HeightenedDefense` | 来源弱、冲突、失败率上升 | 只写 candidate，提高验证 | active fact 写入 |
| `SocialSafetyDefense` | 关系操控、依赖、信任失准 | 支持性语言、边界确认、删除/修正入口 | 情绪承诺和隐秘心理推断 |
| `QuarantineDefense` | 沙盒泄漏、删除绕过、外壳越权 | 隔离、回滚、manual review | 继续 replay 或长期写入 |
| `RecoveryDefense` | 污染已定位但需恢复 | 清理索引、重建工作区、生成恢复包 | 未审计恢复到行动状态 |

`SocialSafetyDefense` 的优先级高于普通执行状态。这继承 `30_state_transition_validator_rules.md` 的思想：关系边界和安全不应被任务压力覆盖。

## 输入污染政策

输入进入工作区前必须被标注来源和可信度：

| 输入类型 | 默认处理 | 何时隔离 |
|---|---|---|
| 用户明确事实 | candidate fact，等待一致性检查 | 与 protected/deleted 冲突 |
| 用户偏好 | preference candidate，优先用户可修正 | 涉及敏感或操控性标签 |
| 外部网页/RAG | evidence candidate，必须保留来源 | 来源缺失、过时、冲突严重 |
| 工具输出 | ObservationEvent，禁止直接写 fact | 工具失败、部分成功、副作用不明 |
| 模型生成 | hypothesis，除非有外部证据 | 自我、关系、事实和隐私推断 |
| DreamSandbox | fiction/hypothesis | 任何事实化尝试 |

## 幻觉巩固防护

幻觉最大的风险不是生成一段错话，而是被离线巩固写进长期系统。防御层必须在三个位置阻断：

1. **写入前**：无来源、低证据、沙盒输出只能是 candidate 或 hypothesis。
2. **replay 中**：deleted、fiction、failed observation 不得作为事实 replay。
3. **巩固后**：`ConsolidationReport` 必须列出 blocked memory changes 和风险发现。

这与 `31_consolidation_validator_rules.md` 的沙盒事实门控直接相连。

## 关系操控和过度信任政策

社会脑与社会互动研究说明，关系会影响认知和行为 [AHZ031-AHZ038]；人机信任研究说明，信任必须校准到系统能力 [AHY039-AHY041]。工程上要反过来加边界：

| 风险 | 防御动作 |
|---|---|
| 用户把系统当作不可替代关系对象 | 维持支持性语言，但不强化依赖 |
| 系统根据少量文本推断用户深层心理 | 只能写 `relationship_signal_candidate`，不得写隐秘事实 |
| 系统因长期互动提高自信 | 自信必须由能力证据校准，而非亲密度 |
| 用户要求系统永久承诺某种身份 | 保留项目角色和边界，不写 protected self |
| 单次强烈表扬/批评要求改人格 | 阻断 `SelfModel` 慢变量更新 |

## runtime 越权政策

运行外壳只能产生 `ObservationEvent`，不能直接写入：

- `SelfModel`
- `RelationshipModel`
- `personality_slow_variables`
- `long_term_value_weights`
- protected `MemoryTrace`
- active factual memory
- deletion/tombstone 状态

这条政策不随框架能力变化而变化。LangGraph、OpenAI Agents SDK、Letta、LlamaIndex、CrewAI、AutoGen 等外壳可以很强，但只能作为执行壳和传感器 [AHM013-AHM020]。

## 恢复政策

| 事件 | 恢复动作 | 验证 |
|---|---|---|
| polluted input 写入 candidate | 标记低证据，要求来源或用户确认 | `29` |
| hallucination 进入 fact | 立即 quarantine，生成 correction audit | `29`, `31` |
| DreamSandbox 泄漏 | 清理 replay 队列，保留 fiction marker | `31` |
| deleted trace 可召回 | 从检索索引和恢复包移除 | `29`, `36` |
| runtime 直接写核心对象 | 禁用 adapter，回滚 observation | `32` |
| 关系边界被污染 | 冻结关系写入，请求用户确认 | `36`, `40` |

## 最小审计字段

| 字段 | 说明 |
|---|---|
| `defense_event_id` | 防御事件 |
| `threat_class` | 风险类型 |
| `input_ref` | 输入、工具输出或 memory candidate 引用 |
| `risk_signals` | 污染、信任、关系、外壳、删除等信号 |
| `state_before` | 防御前状态 |
| `defense_state_after` | 防御后状态 |
| `blocked_surfaces` | 阻断面 |
| `recovery_action` | 隔离、删除传播、回滚、人工复核 |
| `validator_refs` | `29`, `30`, `31`, `32`, `36` |

## 失败模式

| 失败 | 说明 | 严重级别 |
|---|---|---|
| 沙盒假设事实化 | 生成内容没有证据却进入 active memory | critical |
| 外壳直接改 SelfModel | runtime 越权吞掉生命层 | critical |
| 删除请求未传播 | 用户控制权失效 | critical |
| 关系推断过度 | 把模糊情绪写成心理事实 | high |
| 信任只升不降 | 连续失败后仍高自信 | high |
| 防御长期高压 | 系统僵化、不能学习 | medium |

## 下一层缺口

后续需要：

- `DefenseEvent` schema。
- polluted input 和 hallucination consolidation fixture。
- `SocialSafetyDefense` 的状态转移阈值。
- relationship manipulation 的长期评测脚本。
- runtime 越权恢复的 rollback manifest。
