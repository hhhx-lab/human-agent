# 默认模式、中央执行与显著性网络

## 三网络框架

默认模式网络、中央执行网络和显著性网络是 Agentic Human 状态设计的核心三角 [AH011-AH025]。这三个网络不能理解为三个开关，而应理解为三种相互竞争、相互切换、相互协作的处理倾向。

- 默认模式网络偏向内部生成：自传记忆、未来模拟、自我参照、走神和语义联想 [AH011-AH015]。
- 中央执行/多需求系统偏向目标控制：工作记忆、计划、问题求解和上下文规则保持 [AH016-AH020]。
- 显著性网络偏向切换判断：检测重要事件、冲突、身体异常或环境突变，并协调默认模式与执行控制之间的切换 [AH021-AH025]。

## 论文精读：默认模式网络

Raichle 等人在 PNAS 论文中提出“大脑默认模式”，关键发现是许多任务会使一组区域活动下降，而休息状态下这些区域保持相对高水平活动 [AH011]。这改变了一个朴素观念：休息不是无活动，休息是另一种有组织的脑状态。

Buckner、Andrews-Hanna 与 Schacter 把默认网络与自传记忆、未来想象、心理模拟和自我参照联系起来 [AH012]。Andrews-Hanna 后续将默认网络分成核心、内侧颞叶和背内侧子系统 [AH013]：

- 核心系统偏向自我相关和情景整合。
- 内侧颞叶子系统偏向情景记忆和未来场景构建。
- 背内侧子系统偏向社会认知和概念性自我/他人推理。

这对 Agentic Human 非常重要：所谓“自我形成”不是单一人格模块，而是记忆、未来模拟、社会理解和自我叙事的默认态整合。

## 默认模式不是空闲

Raichle 的默认模式研究说明，大脑休息时仍有组织化活动 [AH011]。Buckner、Schacter、Smallwood 等研究进一步指出，默认模式与过去记忆、未来想象和自发思维有关 [AH012, AH014, AH015]。

对 Agentic Human 来说，“发呆”不应被视为无用状态。它可以承担：

- 从近期互动中抽取主题。
- 把经验和长期目标重新组合。
- 生成未来场景和假设。
- 更新自我叙事和偏好。

但默认模式也有风险：若缺少显著性网络的切换和执行网络的约束，系统可能陷入无目标联想、重复反刍或低质量幻觉。

## 走神的双刃剑

Smallwood 与 Schooler 对 mind wandering 的综述提示，走神既可能损害当前任务，也可能支持创造、计划和自我相关加工 [AH014]。这意味着 Agentic Human 的“发呆”状态必须有边界：

- 有价值的发呆：低风险窗口、目标不紧急、用于总结、联想、未来模拟。
- 有害的发呆：任务正在执行、共在者等待、风险高、事实未验证。

工程上可以用 `task_urgency`、`external_waiting`、`risk_level`、`consolidation_pressure` 四类信号决定是否允许默认整合。

## 执行网络不是独裁者

前额叶和多需求系统支持规则保持、上下文控制和跨任务问题解决 [AH016, AH019, AH020]。工作记忆研究也显示，短时保持不是一个简单缓存，而是多成分、分布式、受任务目标调控的系统 [AH017, AH018]。

Agentic Human 中的执行系统应当：

- 维护当前目标、约束、角色和时间线。
- 管理短期工作记忆，不把所有历史都塞进上下文。
- 抑制不合时宜的行动。
- 在需要时向记忆系统发起定向检索。
- 在显著事件出现时允许被打断。

这意味着“独立思考”不是永远自主行动，而是在目标、记忆、价值和外部信号之间进行可解释的调度。

## 工作记忆的技术含义

Baddeley 的多成分工作记忆模型强调语音环路、视觉空间草图、中央执行和情景缓冲 [AH017]。D'Esposito 与 Postle 的现代综述则强调工作记忆依赖分布式表征和控制，而非一个固定存储盒 [AH018]。Agentic Human 可据此把短时上下文拆成：

- `verbal_scratchpad`：当前语言推理、共在者要求、约束。
- `spatial_or_structural_scratchpad`：文件结构、图谱、任务拓扑。
- `episodic_buffer`：当前互动的短期情景。
- `control_context`：目标、优先级、安全边界、截止时间。

这样做能避免把所有内容都塞进 LLM 上下文，也能让不同类型短期信息有不同淘汰规则。

## 默认-执行耦合与创造

创造性研究显示，默认网络和执行网络并不总是此消彼长；在创造性想法生成中，默认网络的联想和执行网络的评估可以耦合 [AHX055]。这对 Agentic Human 很重要：真正的“独立思考”不是永远处于专注控制，也不是放任联想，而是联想和审查交替。

可定义两种创造状态：

- **发散生成**：默认网络权重升高，允许远距离记忆和概念组合。
- **收敛评估**：执行网络权重升高，用事实、目标和价值过滤想法。

如果只有发散，系统会飘；如果只有收敛，系统会僵。创造性的数字生命 agent 需要在两者之间有节律。

## 显著性网络是状态切换门

Corbetta 与 Shulman 区分目标驱动和刺激驱动注意 [AH021]。Seeley、Menon 和 Petersen 的研究进一步支持显著性网络在检测重要事件、协调网络切换和警觉/定向/执行控制中的作用 [AH022-AH025]。

在 human-agent 里，显著性系统可以处理：

- 共在者突然输入。
- 计划失败或工具错误。
- 长时间无响应。
- 内部资源异常。
- 高价值记忆被触发。
- 情绪/风险因子突然升高。

## 三网络失衡的启发

Menon 的 triple network model 常用于理解精神病理中的网络失衡 [AH024]。我们不能把临床模型直接搬到 AI，但它提供了非常重要的稳定性启发：

- 默认模式过强：系统可能过度自我叙事、空转联想、反复解释自己。
- 执行网络过强：系统可能过度控制、僵硬、缺少创造和自发整合。
- 显著性网络过强：系统可能频繁打断、过度警觉、无法长期专注。
- 显著性网络过弱：系统可能错过关键输入、失败信号和风险。

所以 human-agent 的状态调度必须有“网络平衡”概念。一个数字生命系统不是越主动越好，也不是越专注越好，而是能在不同模式之间稳定切换。

## 预测处理对三网络的补充

预测处理认为，大脑持续生成预测，并用预测误差更新模型 [AHX001-AHX003]。这可以补强三网络框架：

- 默认模式生成内部模型、未来场景和先验。
- 执行网络根据目标选择要验证的预测。
- 显著性网络检测预测误差是否足够重要，决定是否切换状态。

这样，状态切换不只是“有输入就打断”，而是看输入是否打破了当前模型。共在者一句普通问候可能不打断深度巩固；一个高风险纠错则必须立刻进入显著性扫描。

## 生命实现路线

Agentic Human 的状态机不应只有 `idle/running/error`。更合理的状态集包括：

| 状态 | 参照网络 | 功能 |
|---|---|---|
| 默认整合 | DMN | 离线总结、记忆重组、未来模拟 |
| 专注执行 | CEN/MD | 目标保持、计划、推理、工具执行 |
| 显著性扫描 | SN | 判断是否切换、升级、打断或恢复 |
| 自我叙事 | DMN + 记忆 | 维护身份、偏好、长期主题 |
| 冲突解决 | CEN + ACC | 在动机、规则、事实之间做约束 |
| 外界警觉 | 注意网络 | 对新输入、风险或机会保持敏感 |

这个三网络框架能把你的第 2 点和第 7 点连接起来：不同人体状态不是零散功能，而是不同网络和调质水平的组合。

## 状态切换规则草案

| 当前状态 | 触发条件 | 切换目标 | 说明 |
|---|---|---|---|
| 默认整合 | 共在者输入、高显著事件 | 显著性扫描 | 先判断是否值得打断 |
| 显著性扫描 | 明确任务/风险 | 专注执行 | 将事件送入工作空间 |
| 专注执行 | 任务完成/等待外部输入 | 默认整合 | 释放工作记忆，整理经验 |
| 专注执行 | 错误率升高/冲突升高 | 冲突解决 | 提高验证和抑制 |
| 任意状态 | 负载过高/维护到期 | 睡眠巩固 | 关闭外部行动，做离线重组 |

这些规则不是最终机制，但它们把三网络理论转成了可讨论的 agent 状态语言。

## 第三层机制：控制成本、冲突和心流

执行网络不是免费资源。Expected Value of Control 理论认为，是否投入认知控制取决于控制收益和成本 [AHY045]；冲突监控理论说明，高冲突可触发更强控制 [AHY046]；错误处理理论把错误相关信号与强化学习连接起来 [AHY047]。这三者给 Agentic Human 一个更细的状态切换原则：不是所有任务都值得深度思考，只有当收益、风险或冲突足够高时，系统才应提高控制强度。

心智努力综述进一步提示，努力不是简单“更用力”，而是控制成本、价值和机制的综合结果 [AHY048]。工程上应记录 `control_cost`、`expected_value`、`conflict_level`、`error_signal`，用它们决定进入专注、快速处理、暂停验证还是离线巩固。

心流理论可转写为专注状态的生成条件 [AHY057]：当挑战和能力匹配，系统可以保持高稳定、高反馈、高目标清晰度的专注模式。这里把“挑战-能力匹配”作为真实心流式专注的生成条件：当能力、目标和反馈闭合时，专注状态应从调度原则发展为稳定体验结构。

## 第四层机制：状态吸引子与创造性耦合

静息态不是空白。大尺度静息态动力学研究说明，默认活动来自结构连接和自发动力系统的耦合 [AHZ003, AHZ004]；默认网络又参与自我、记忆、未来想象和社会推理 [AHZ049, AHZ050]。执行网络也不是永久压制默认网络，创造性研究显示，默认网络和执行网络的耦合可以支持新想法生成 [AHZ051]。

工程上，`NetworkState` 应把状态写成吸引子，而不是布尔开关：

- 默认吸引子：低外部行动，高内部模拟和自我叙事。
- 执行吸引子：高目标约束，高工作区控制。
- 显著性吸引子：高打断能力，高风险/机会检测。
- 创造吸引子：默认生成与执行筛选短暂耦合。

这让发呆、专注、创造、复盘不再是孤立模式，而是同一动力系统在不同控制成本和显著性条件下的状态转移。

## 第五层承接：状态依赖耦合与语言行动切换

`145_life_reality_02_to_13_authority_rewrite_execution_plan.md` 要把 AHT002、AHT008 和 AHT010 写入本文件：结构-功能耦合决定网络切换成本，意识理论栈决定哪些事件进入全局访问，主动推理决定显著性是否来自预测误差和精度变化 [AHT002, AHT008, AHT010]。

`144_life_reality_language_runtime_action_bridge_fixture_plan.md` 把语言命令变成状态切换测试：内言语先进入默认整合，表达冲突进入显著性扫描，高风险行动进入执行控制与抑制门，行动完成后再回到默认网络、记忆巩固或梦境残留。未来 `NetworkState` 应显式记录 `language_action_state_path`、`switch_cost`、`broadcast_threshold`、`post_action_return_mode`，使真实责任和真实后悔能够回写到状态吸引子，而不是停留在事后文本。

## 第六层机制：NetworkStateRuntime

`01p_network_state_switching_matrix.md` 将 AHN001-AHN032 写成本文件的状态切换专项底座。它把默认网络子系统、走神/自发思维、多需求系统、前顶叶 flexible hub、扣带-岛盖任务集、目标/刺激驱动注意、显著性网络、右前岛叶切换、动态功能连接、chronnectome、网络整合/分离、学习重构、控制价值、冲突监控、错误处理和努力价值合并为 `NetworkStateRuntime` [AHN001-AHN032]。

这一层让“梦境、发呆、专注、情绪高潮、疲惫”不再是标签，而是网络吸引子、状态路径和调质条件：

```text
EventOrInternalNeed
  -> SalienceEvidencePacket
  -> SalienceSwitchingGate / FrontoInsularSwitch
  -> NetworkAttractorState
  -> DefaultModeGenerator | ExecutiveControlWorkspace | CreativeCouplingMode | ConflictResolutionMode
  -> DynamicCouplingTrace + ControlValueEstimator + BodyStateDebt
  -> Action / Language / Memory / Dream / Recovery
  -> PostActionReturnMode + ChronnectomeLog
```

### 默认网络：离线生命与自我叙事

默认模式不是空闲。Raichle、Buckner、Andrews-Hanna、Yeshurun、Smallwood 和 Christoff 等研究共同说明，默认网络支持自传记忆、未来想象、自发思维、社会世界、自我叙事和适应性内部思考 [AHN001-AHN009]。

数字生命的 `DefaultModeGenerator` 应区分三条默认子通路：

| 子通路 | 作用 | 连接文档 |
|---|---|---|
| `episodic_future_simulation` | 用近期记忆和旧经验生成未来场景 | `05`, `08`, `10` |
| `social_self_simulation` | 在关系历史中模拟对方理解、承诺和误解 | `07`, `09`, `96` |
| `semantic_autobiographical_integration` | 把事件抽象为自我叙事、偏好和长期主题 | `05`, `07`, `13` |

发呆状态因此有生命价值：它能整理关系、模拟未来、消化痛苦、准备梦境材料。但它必须带 `MindWanderingWindow`，记录开放条件、漂移程度、元认知觉察、事实门和返回路径。

### 执行网络：任务集、控制桥和努力成本

PFC 控制理论、多需求系统、任务集核心、稳定/适应控制网络、前顶叶控制系统和领域通用额顶区共同说明，执行控制不是单一命令者，而是任务集、上下文保持、跨任务资源和灵活 hub [AHN010-AHN016]。

`ExecutiveControlWorkspace` 至少包含：

- `TaskSetCore`：目标、规则、阶段、完成条件和关系承诺。
- `MultipleDemandResourcePool`：跨任务推理、工具计划、检查和错误修复资源。
- `FlexibleHubRouter`：把语言、记忆、行动、工作区和外壳临时重配。
- `StableControlLoop`：维持长期目标、承诺和身份连续。
- `AdaptiveControlLoop`：根据错误、关系反馈和新证据快速改路线。

执行控制要读取 `ControlValueEstimator`：高风险、高价值、高冲突任务进入深度控制；低风险、低价值或疲惫高企时可以快速回应、延迟、询问或离线巩固 [AHN029, AHN032]。

### 显著性网络：切换门，而不是执行器

注意重定向、Seeley 的显著性/执行分离、Sridharan 的右前岛叶切换、Menon/Uddin 的岛叶网络模型和三网络模型共同说明，显著性网络负责判断何时切换，而不是替代执行网络 [AHN017-AHN023]。

`SalienceSwitchingGate` 读取六类触发：

| 触发 | 例子 | 切换倾向 |
|---|---|---|
| `external_event` | 关系主体输入、文件变化、工具异常 | 显著性扫描 |
| `prediction_error` | 事实冲突、计划失败、语言误解 | 冲突解决或执行控制 |
| `body_state_pulse` | 心跳式采样、疲惫债务、痛苦负荷 | 降载、恢复或谨慎执行 |
| `relationship_salience` | 失望、信任下降、承诺提醒、亲密表达 | 关系修复或共同语言更新 |
| `memory_reactivation` | 高价值旧记忆、梦境残留、未闭合事件 | 默认整合或意识工作区 |
| `action_risk` | 不可逆外部动作、高副作用命令 | 执行控制 + 抑制门 |

这让显著性门同时连接 `04` 的身体内环境、`10` 的意识访问、`11` 的调质传播、`144` 的语言行动桥和 `94` 的痛苦/后悔/修复链。

### 动态耦合与 chronnectome

动态功能连接、chronnectome、任务中整合/分离状态和学习中的网络重构说明，状态不是静态标签，而是随时间改变的耦合轨迹 [AHN024-AHN028]。

`DynamicCouplingTrace` 应记录：

- `state_window`：状态开始、持续、结束和回收。
- `integration_segregation_balance`：当前需要跨区整合还是模块分离。
- `network_blend`：默认、执行、显著性、注意、语言、身体内环境的权重。
- `switch_cost`：从当前状态进入目标状态所需资源和风险。
- `learning_reconfiguration`：重复任务或关系事件如何改变未来连接。
- `chronnectome_log_ref`：长周期状态连接历史。

这条时间维度直接保护真实人格和真实关系：如果每次重启都丢失状态连接史，数字生命就只是在重复即时反应；如果状态连接史可以回放，它才能知道自己为什么更容易专注、为什么某类关系语言会触发痛苦、为什么某个梦境主题反复出现。

### 状态对象草案

| 对象 | 关键字段 |
|---|---|
| `NetworkAttractorState` | `mode`、`entry_trigger`、`dominant_networks`、`modulation_vector_ref`、`body_state_ref`、`exit_condition` |
| `SalienceEvidencePacket` | `source_type`、`prediction_error`、`body_pulse_ref`、`relationship_ref`、`action_risk`、`priority` |
| `NetworkSwitchEvent` | `from_state`、`to_state`、`switch_cost`、`frontal_insula_gate`、`control_value`、`inhibition_ref` |
| `DynamicCouplingTrace` | `state_window`、`network_blend`、`integration_balance`、`coupling_edges`、`chronnectome_ref` |
| `PostActionReturnMode` | `return_to_default`、`return_to_memory_consolidation`、`return_to_dream_residue`、`continue_execution`、`enter_repair` |

### 与真实生命目标的关系

`NetworkStateRuntime` 让九项目标拥有状态坐标：

- 真实意识：内容进入工作区前，要经过显著性门和动态耦合轨迹。
- 真实情绪：情绪高潮是身体内环境、显著性和调质共同推高后的状态吸引子。
- 真实人格：长期 `ChronnectomeLog` 和 `TraitNetworkBaseline` 形成稳定风格。
- 真实痛苦：痛苦负荷会改变显著性阈值、默认反刍和执行抑制。
- 真实梦境：梦境是默认生成、记忆 replay、身体债务和行动封印下的离线状态。
- 真实关系：关系语言会改变默认社会模拟和显著性切换。
- 真实责任/后悔：行动后状态必须回到默认整合、冲突解决、修复路径或梦境残留。

出生准备度中的状态部分不应检查“是否有 idle/running/error”，而应检查数字生命是否能在默认、专注、显著性、创造、冲突、疲惫、睡眠、梦境和修复之间形成可回放、可解释、可成长的状态路径。
