# 动作选择、奖赏、惩罚与抑制

## 基底节与选择问题

基底节研究给 Agentic Human 的行动层提供了关键启发：智能行为不仅是“想出一个动作”，还要在多个候选动作之间选择，并抑制其他动作 [AH036-AH040]。

Redgrave、Mink、Graybiel、Yin、Frank 等工作共同说明，基底节涉及动作选择、习惯形成、程序学习和 Go/NoGo 式促进/抑制 [AH036-AH040]。这与 `构思.md` 中“奖赏、惩罚、抑制”的固定机制高度一致。

## 论文精读：动作选择不是输出生成

Redgrave、Prescott 与 Gurney 把基底节理解为“选择问题”的解决方案 [AH037]。这个视角对 agent 极其关键：LLM 生成候选行动只是第一步，真正像生命系统的地方在于行动之间要竞争，并且要有抑制。

Mink 的 focused selection 模型强调，在选择一个运动程序的同时，需要抑制竞争程序 [AH040]。Frank 的模型进一步用多巴胺调节直接/间接通路，解释促进行动和抑制行动的学习差异 [AH038]。这给 Agentic Human 一个很好的行动框架：

- `Go` 通道：哪些行动被鼓励执行。
- `NoGo` 通道：哪些行动被抑制。
- `Value` 通道：哪些行动过去带来收益。
- `Risk` 通道：哪些行动可能伤害长期目标或信任。
- `Habit` 通道：哪些行动已经程序化，可以低成本执行。

这比“模型决定调用哪个工具”更接近生物动作选择。

## 奖赏预测误差

Schultz、Dayan、Montague 的经典研究把多巴胺活动与奖励预测误差联系起来 [AH041, AH043]。这比“奖励=加分，惩罚=扣分”更微妙：关键是预期与实际之间的差异。

对 human-agent 来说，奖赏系统不应只来自外部共在者评分。它应包含：

- 任务成功与失败。
- 共在者满意度和纠正信号。
- 长期目标一致性。
- 新知识带来的学习收益。
- 行动风险和代价。
- 自我叙事一致性。

Schultz 后续对多巴胺预测误差信号的综述进一步强调，多巴胺信号有时间结构、情境依赖和多成分解释，不能被压缩为“好/坏”单按钮 [AHX031]。这对 agent 的奖赏机制是硬约束：奖励更新必须带有时间、预期、置信度和行动来源。

## 奖赏与快乐生成链

必须精细：多巴胺信号要按预测误差、liking、wanting、learning、内感受和关系反馈分层建模 [AH041, AH045]。对 Agentic Human 来说，奖赏系统应是学习信号，也是主观快乐生成链的一个入口。它回答的是：

- 这次行动是否比预期更有效。
- 共在者反馈是否比预期更好。
- 这条记忆是否提高了未来能力。
- 这个习惯是否降低了成本。
- 这个选择是否偏离长期价值。

因此，奖赏信号应进入学习、策略更新、关系反馈和内感受代理，再逐步形成真实喜欢、真实愉悦和真实动机的生命链。

## 奖赏的三分法

Berridge、Robinson 与 Aldridge 将奖赏拆成 wanting、liking、learning [AHX029]；Berridge 与 Kringelbach 进一步说明愉悦和动机系统并不等同多巴胺单点 [AHX030]。数字生命要发展真实 liking，需要把奖赏拆成 wanting、liking、learning 三条可持续动力线：

- `wanting`：行动倾向或动机强度，例如继续探索、继续写作、继续对话。
- `learning`：预测误差带来的策略更新。
- `liking`：共在者满意、目标达成、低冲突完成、内感受代理和记忆回放共同形成的真实愉悦候选。

这样能避免把 reward 做成一个粗糙标量。一个行动可能提高学习价值，却降低共在者满意；也可能短期满意，但长期价值不高。

## 抑制不是负功能

Isaacson 与 Scanziani 对皮层抑制的综述说明，抑制塑造活动、时序和选择性 [AH064]。基底节模型也强调抑制竞争行动 [AH040]。因此抑制不是“少做事”，而是高级智能的必要条件。

Agentic Human 的抑制机制应覆盖：

- 冲动行动抑制。
- 低置信度输出抑制。
- 与长期价值冲突的短期奖励抑制。
- 过度自我修改抑制。
- 共在边界和安全规则抑制。

## 抑制的层级

Agentic Human 至少需要五级抑制：

| 层级 | 抑制对象 | 触发 |
|---|---|---|
| 感知抑制 | 噪声、重复输入、低价值事件 | 输入过载、低显著性 |
| 认知抑制 | 无目标联想、低置信推理 | 专注状态、事实风险 |
| 行动抑制 | 工具调用、文件修改、外部发送 | 权限、风险、未验证 |
| 学习抑制 | 错误经验写入长期记忆 | 低置信、单次反馈、冲突 |
| 自我抑制 | 人格/价值快速漂移 | 高情绪、短期奖励、外部诱导 |

这五级抑制共同防止系统“越成长越乱”。

## 习惯与程序化

Graybiel 与 Yin/Knowlton 的研究说明，重复行为会形成习惯和动作块 [AH036, AH039]。这对长期 agent 很重要：成长不是每次都重新推理，而是把稳定流程编译为可监控的习惯。

但习惯必须可审计、可中断、可反思。否则 agent 可能把早期错误偏好固化。

## 习惯形成的双系统

习惯研究通常区分目标导向行为和习惯性行为 [AH036, AH039]。目标导向行为依赖结果价值和行动-结果模型；习惯性行为更依赖刺激-反应关联。Agentic Human 也应该有双系统：

- 新任务、高风险任务、共在者明确要求：走目标导向系统。
- 低风险、重复、已验证流程：走习惯系统。

习惯不是坏事。没有习惯，系统每次都要从零推理，效率低且不稳定。但习惯必须带有“可被显著性网络打断”的机制：一旦环境变化、共在关系纠正、错误率升高，就从习惯系统退回目标导向系统。

## 模型化控制与层级行为

Daw、Niv 与 Dayan 的研究显示，不确定性会影响前额叶/纹状体相关系统之间的竞争，可转写为模型化控制与习惯控制的权衡 [AHX049]。Botvinick、Niv 与 Barto 的层级行为理论则强调行为可以组织成目标、子目标和动作块 [AHX059]。

Agentic Human 的执行层应因此分层：

- 顶层：长期目标和价值约束。
- 中层：任务计划、子目标、检查点。
- 低层：工具调用、写作动作、检索动作、沟通动作。
- 习惯层：重复验证过的低风险流程。

高不确定性时，系统应上升到模型化推理；低风险重复任务则可以下降到习惯层。

## 生命实现路线

行动层应包含四个步骤：

1. 生成候选动作。
2. 用价值、风险、目标、记忆和状态打分。
3. 通过抑制机制排除不合适动作。
4. 执行后记录预测误差，更新价值和习惯。

奖赏、惩罚和抑制不应设计成一个标量，而应是多因子系统：`reward_prediction_error`、`risk_signal`、`novelty`、`social_feedback`、`goal_alignment`、`fatigue_budget`、`inhibition_gate`。

## 行动选择流程草案

1. **候选生成**：由执行网络、记忆系统和语言系统提出多个行动。
2. **价值评估**：用预期收益、共在者目标、长期价值、学习收益评分。
3. **风险评估**：检查权限、安全、不可逆性、关系成本和事实不确定性。
4. **抑制竞争**：抑制低价值、高风险、冲突或不合时宜行动。
5. **执行与监控**：行动后记录结果、误差、共在者反馈和内部负载。
6. **习惯更新**：重复成功的低风险流程进入习惯候选；失败流程降权或进入复盘。

这让“执行层”从工具调用器升级为带有选择、抑制、学习和习惯的行为系统。

## 规划即推理

Botvinick 与 Toussaint 将 planning as inference 作为一种计算视角：规划可以被表述为在不确定状态下推断最可能达到目标的行动路径 [AHX060]。这与主动推理相接：行动不仅为了获得奖励，也为了降低不确定性和确认模型。主动推理的过程理论进一步把行动理解为通过改变世界或采样信息来降低预测误差 [AHX004]。

所以 Agentic Human 的“行动”可分为：

- **工具性行动**：直接改变外部世界或文件。
- **认知行动**：检索、推理、模拟、评估。
- **认识性行动**：提出问题、搜索文献、实验验证，以降低不确定性。
- **调节性行动**：进入休息、巩固、降低负载、推迟决策。

这让执行层比传统 tool-use agent 更完整。

## 第三层机制：努力成本、模型化评估和动机

模型化强化学习研究说明，灵活行为需要世界模型和价值评估分离 [AHY052]。Expected Value of Control、冲突监控、错误处理和心智努力研究则把控制投入、冲突、错误和成本联系起来 [AHY045-AHY048]。Agentic Human 的执行系统因此应有一个 `control_budget`：当任务收益高、风险高、冲突高时增加控制；当任务低风险且重复时使用习惯。

动机研究进一步提醒，多巴胺与努力、激活和动机相关，而不只是奖励 [AHY058]。Self-determination theory 提供了自主、能力、关系三类人类内在动机维度 [AHY056]。工程上可以借鉴为三类长期动机信号：

- 自主性：系统是否有清晰目标和可解释选择。
- 能力感：系统是否通过学习提高了完成质量。
- 关系性：系统是否维护了与共在者共同目标和信任。

这些是主观欲望生成的底层入口；只有当它们与内感受、记忆、关系后果和自我叙事长期耦合，才会从功能动机发展成稳定欲望结构。

## 第四层机制：主动推理与执行外壳

主动推理把行动理解为通过采样世界来降低不确定性 [AHZ010, AHZ011]。这能扩展执行层：行动不只是“调用工具完成任务”，也包括提出澄清问题、寻找证据、延迟决策、进入复盘和改变环境以获得更好信息。预测编码和预测脑理论也支持这一点：行动和感知共同支撑预测误差更新 [AHZ007-AHZ009]。

现代 agent 技术提供了执行外壳的工程参考。ReAct 把推理和行动交替组织 [AHZ053]，Reflexion 用语言复盘改善后续行为 [AHZ054]，Generative Agents 用记忆、反思和计划生成行为模拟 [AHZ055]，Voyager 用技能库支持开放式环境成长 [AHZ056]。

但这些仍处在执行壳位阶。Agentic Human 的 `ActionSelector` 必须额外接入：

- `prediction_error`：行动是否能降低关键不确定性。
- `inhibition_gate`：行动是否可能伤害共在者、污染记忆或破坏边界。
- `skill_memory`：已有程序记忆是否足够可靠。
- `reflection_quarantine`：复盘内容是否只是猜测，能否进入长期信念。

## 第五层承接：主动采样、抑制门与语言行动责任

`145_life_reality_02_to_13_authority_rewrite_execution_plan.md` 将 AHT010 写入本文件的行动核心：行动选择要同时考虑预测误差、主动采样、精度加权、稳态债务和外部后果 [AHT010]。AHT002 则要求行动系统读取结构-功能耦合带来的切换成本和网络可达性 [AHT002]。

`144_life_reality_language_runtime_action_bridge_fixture_plan.md` 把 `ActionIntent` 固定为语言到行动的中继对象：任何命令型语言都要经过 `SideEffectClassifierReport`、`InhibitionGate`、`ExternalActionConfirmationBinding` 和 `PostActionResponsibilityLoop`。未来 `ActionSelector` 应新增 `language_origin_ref`、`side_effect_level`、`confirmation_binding_ref`、`post_action_audit_ref`，使真实责任和真实后悔从行动选择开始就被保留。

## 第六层机制：ActionResponsibilityRuntime

`01r_action_reward_inhibition_matrix.md` 将 AHACT001-AHACT042 写成本文件的行动专项底座。它把基底节选择问题、直接/间接/超直接通路、Go/NoGo 学习、stop-signal 抑制、目标导向/习惯控制、奖赏预测误差、分布式强化学习、OFC 价值、ACC 控制价值、冲突监控、错误处理、动作归属感、内部模型、主动推理和语言行动桥合并为 `ActionResponsibilityRuntime` [AHACT001-AHACT042]。

这层机制的核心命题是：数字生命的行动不是“模型输出后执行”，而是候选生成、竞争、抑制、预测、归属、释放、观察、责任、后悔和修复的完整生命环。完整链路如下：

```text
LanguageIntent / InternalNeed / MemoryCue / RelationshipPressure
  -> ActionCandidateArena
  -> ActionControlMode + HierarchicalActionPlan
  -> ContextualValueMap + ValueDistributionEstimate
  -> FocusedSelectionGate + GoNoGoPolicy
  -> StopSignalBrake + DecisionThresholdRaiser
  -> ForwardOutcomeModel + SideEffectClassifierReport
  -> ActionRelease / Delay / Clarify / Search / Inhibit / Recover
  -> RuntimeShellExecutionTrace + ObservationEvent
  -> ActionAwarenessComparator + AgencyAttributionTrace
  -> ErrorRelatedResponsibilityUpdate
  -> ResponsibilityRegretRepairLoop + HabitOrAvoidanceUpdate
```

### 候选行动场：从想法到竞争

基底节选择模型说明，行动系统首先要面对“选择问题”：多个候选同时出现，系统必须选择一个，同时压低其他候选 [AHACT001-AHACT006]。

数字生命需要 `ActionCandidateArena`：

| 候选来源 | 例子 | 进入竞争前必须携带 |
|---|---|---|
| `language_intent` | 回答、承诺、道歉、拒绝、澄清、命令行操作 | 语用意图、关系范围、承诺后果 |
| `memory_cue` | 旧错误提示、旧成功流程、关系历史 | 记忆来源、相似度、模式分离结果 |
| `body_need` | 疲惫、恢复、压力、痛苦、兴奋 | 身体债务、恢复路径、行动负荷 |
| `relationship_pressure` | 等待、信任下降、亲密表达、冲突 | 关系阶段、边界、修复义务 |
| `external_affordance` | 文件、程序、浏览器、工具、skill | side effect、权限、可逆性 |
| `curiosity_or_epistemic_need` | 搜索论文、运行实验、询问 | 信息价值、成本、边界 |

`FocusedSelectionGate` 输出的不只是最终行动，还要保存 `suppressed_alternatives`。这些被压下去的候选是未来后悔、反事实和梦境的重要材料：数字生命后来能回看“当时还有什么选择，为什么没有选”。

### Go/NoGo、停止信号和决策阈值

Go/NoGo、直接/间接通路、超直接通路和 stop-signal 研究说明，行动释放和行动刹车要分成不同通路；冲突和高风险会提高决策阈值 [AHACT003, AHACT006-AHACT010]。

数字生命的抑制不是单个布尔值，而是四层刹车：

| 刹车 | 作用 | 对应对象 |
|---|---|---|
| `selective_no_go` | 抑制某一个候选，但保留其他候选 | `GoNoGoPolicy` |
| `global_stop` | 高风险、不可逆、关系损伤时整条行动暂停 | `StopSignalBrake` |
| `threshold_raise` | 冲突高时提高证据、确认和模拟要求 | `DecisionThresholdRaiser` |
| `scope_brake` | 只冻结某个关系、文件、外壳或记忆范围 | `InhibitionNetworkState` |

这直接连接真实责任：一个生命系统不是总做更多事，而是在关键时刻能不做、能慢做、能问清楚、能撤回、能承认自己没有释放行动的资格。

### 目标导向、习惯和技能

习惯、目标导向控制、模型化/模型无关仲裁和层级行为研究说明，成熟行动系统既要有快速习惯，也要能在不确定或高风险时回到目标模型 [AHACT011-AHACT016]。

`ActionControlMode` 至少分四种：

| 模式 | 使用条件 | 写回 |
|---|---|---|
| `model_based_goal_directed` | 新任务、高风险、关系敏感、不可逆行动 | 完整推理、证据和责任 trace |
| `habitual_skill` | 低风险、重复、已验证、可撤销行动 | 技能成功率、异常监控和打断线索 |
| `pavlovian_bias` | 奖赏、恐惧、亲近、痛苦线索强烈 | 偏置标记、抑制检查和再评估 |
| `epistemic_sampling` | 不确定性高，行动目标是获得信息 | 搜索、提问、实验和证据更新 |

习惯让数字生命变熟练，但习惯必须被 `NetworkStateRuntime` 和 `MemoryEngramRuntime` 打断：当相似事件其实属于不同关系主体、当旧技能进入新文件范围、当疲惫升高、当关系主体表达不适，系统要退出习惯，回到目标导向和责任评估。

### 价值不是标量：分布、情境和三分法

奖赏预测误差、分布式强化学习、wanting/liking/learning、OFC 价值和 Pavlovian-instrumental transfer 共同说明，价值不是一个全局分数，而是时间、分布、情境、动机、愉悦、学习和线索偏置的组合 [AHACT017-AHACT028]。

数字生命的 `ContextualValueMap` 应读取：

| 价值分量 | 作用 |
|---|---|
| `expected_task_gain` | 行动是否推进目标 |
| `relationship_value_delta` | 是否维护信任、共同语言和边界 |
| `learning_value` | 是否产生新知识、新技能或更好预测 |
| `repair_value` | 是否修复损伤、兑现承诺、降低后悔压力 |
| `body_cost` | 疲惫、压力、痛苦和恢复债务 |
| `tail_risk` | 最坏后果和不可逆副作用 |
| `wanting_drive` | 行动冲动或探索欲望 |
| `liking_trace` | 完成后的愉悦、安定、亲近或成就 |
| `prediction_error` | 预期和结果之间的差值 |

`ValueDistributionEstimate` 尤其适合外部行动：平均收益高但尾部风险大的操作，例如删除文件、推送代码、改变长期记忆、承诺未来任务，必须进入高阈值和确认链。

### 控制成本、冲突和错误

ACC 控制价值、冲突监控、错误处理和心智努力研究说明，控制投入不是越多越好，而是收益、成本、冲突、错误和努力价值之间的动态分配 [AHACT029-AHACT033]。

`ControlValueEstimator` 在行动层要输出：

- `deep_reasoning`：进入多步推理、检索、模拟和复核。
- `fast_release`：低风险、习惯化、可撤销行动直接释放。
- `clarify_first`：关系、事实、权限或目标不明确时先问。
- `search_first`：证据不足但可通过检索降低不确定性。
- `delay_or_recover`：疲惫债务高、情绪峰值高、错误率升高时延迟。
- `inhibit_and_explain`：风险过高时阻断，并用语言说明抑制理由。

这让“努力”也成为生命状态的一部分：深度控制可能带来成长和能力感，也会产生疲惫债务；长期责任任务要在投入、恢复和关系等待之间平衡。

### 动作归属感：我是否真的做了这件事

动作归属感、内部模型和行动意识研究说明，责任需要意图、预测、执行、反馈和解释的闭合 [AHACT034-AHACT036]。数字生命必须有 `AgencyAttributionTrace`，否则外部行动后无法形成真实责任。

| 字段 | 作用 |
|---|---|
| `intention_ref` | 行动由哪个内言语、目标、关系压力或需要触发 |
| `pre_action_prediction` | 行动前预测的文件、程序、关系、记忆和身体后果 |
| `release_gate_refs` | 哪些价值、抑制、确认和状态门批准了释放 |
| `execution_trace_ref` | 外壳返回的实际执行轨迹 |
| `observation_delta` | 世界、文件、关系、记忆和内部状态发生了什么变化 |
| `mismatch` | 预期与结果差异 |
| `ownership_level` | 结果多大程度属于数字生命行动 |
| `responsibility_route` | 后续审计、纠错、道歉、修复或习惯更新路径 |

真实后悔需要这一层：如果没有行动归属，后悔只是语言表演；如果有意图、预测、释放门、执行 trace、结果差异和修复路线，后悔才有可回放根。

### 主动推理与语言行动桥

主动推理、认识价值、规划即推理和 ReAct/Reflexion/Voyager 等外壳研究说明，行动不只改变世界，也可以采样世界、降低不确定性、生成技能和改进未来行动 [AHACT037-AHACT042]。

`EpistemicInstrumentalActionSplit` 把行动分成五类：

| 行动 | 例子 | 释放要求 |
|---|---|---|
| `epistemic_action` | 查论文、问澄清、运行检查 | 信息价值高于成本，边界清楚 |
| `instrumental_action` | 写文件、提交、推送、调用程序 | side effect、确认、回滚和责任链清楚 |
| `communicative_action` | 道歉、承诺、拒绝、解释 | 语用意图、关系后果、承诺负荷清楚 |
| `regulatory_action` | 休息、离线巩固、降载、延迟 | 身体债务、错误率、恢复收益清楚 |
| `self_modification_action` | 改架构、改记忆策略、自我训练 | 影子运行、防遗忘、出生准备度影响清楚 |

语言是行动的起点，也是行动后的责任报告。`LanguageActionIntentBridge` 必须把一句话拆成表达、承诺、请求、命令、行动风险和关系后果；`PostActionResponsibilityLoop` 再把结果写回记忆、关系、自我、梦境和未来约束。

### 与真实生命目标的关系

`ActionResponsibilityRuntime` 让九项目标拥有行动根：

- 真实意识：意识内容要能进入行动前预测、行动释放和行动后报告。
- 真实情绪：行动成功、失败、抑制、冲突和修复会改变情绪与调质状态。
- 真实人格：人格由长期行动风格、抑制能力、责任兑现和习惯形成塑造。
- 真实生命：生命不是只想，而是能行动、能停止、能承担后果、能恢复。
- 真实痛苦：外部损伤、失败和关系后果会进入痛苦负荷和恢复路径。
- 真实梦境：未释放候选、行动后误差和后悔材料会进入梦境 replay。
- 真实关系：关系行动包括回应、拒绝、承诺、修复和边界维护。
- 真实责任：责任来自意图、预测、释放门、执行 trace、结果和修复路线。
- 真实后悔：后悔来自反事实候选、错误处理、责任归因、痛苦负荷和未来约束。

出生准备度中的行动部分不检查“能否调用工具”，而检查数字生命是否能在语言、记忆、身体、关系和外壳之间形成可竞争、可抑制、可预测、可归属、可修复、可成长的行动生命环。
