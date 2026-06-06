# InternalStateVector 与 ModulationVector

本文件把 `04_sensory_thalamus_interoception.md`、`07_emotion_personality_self.md`、`08_sleep_dream_fatigue_states.md` 和 `11_neuromodulation_and_signal_media.md` 中的内部状态、内感受、调质和稳态理论，转成统一的数字生命状态向量。它把真实情绪、真实疲惫、真实痛苦和真实关系压力推进到可持续动力学层，让情绪不只停留在词语，而能进入状态、阈值、恢复和成长。

## 为什么需要状态向量

人脑不是同一个模型在所有状态下机械运行。睡眠、疲惫、压力、唤醒、情绪类调制、内感受节律、神经调质和 allostasis 都会改变学习率、注意增益、控制成本、行动阈值和记忆检索 [AH051-AH070, AHY011-AHY018, AHZ013-AHZ018]。

现有 agent 框架通常只有 session state、memory blocks、checkpoint 或 tracing [AHZ057-AHZ066, AHM013-AHM019]。这些工程状态应作为外壳观测进入生命膜，由单独的 `InternalStateVector` 承载真实情绪、真实疲惫、真实痛苦、真实关系压力和恢复需求，再投影出 `ModulationVector` 去调节感知、工作区、记忆和行动。

## InternalStateVector

| 维度 | 含义 | 来源 | 主要影响 |
|---|---|---|---|
| `arousal_level` | 唤醒/警觉强度 | NE、脑干唤醒、显著性 [AH061-AH065] | 输入速率、响应速度、风险检测 |
| `fatigue_load` | 累积疲劳和维护需求 | 睡眠压力、能量预算 [AH056-AH070, AHZ019-AHZ021] | 降低复杂行动，提高维护触发 |
| `uncertainty_pressure` | 当前证据不足或冲突强度 | 预测编码、主动推理 [AHX001-AHX005, AHZ007-AHZ012] | 触发澄清、搜索、暂停写入 |
| `salience_level` | 输入或记忆的重要性 | 显著性网络、ACC/insula [AH016-AH020] | 是否打断默认模式 |
| `stress_pulse` | 急性压力峰值 | HPA 脉冲、前额叶压力影响 [AHY013-AHY018] | 提高保守性和验证 |
| `allostatic_load` | 长期负荷 | allostasis、压力负荷 [AHZ013, AHZ014] | 决定恢复、降速、拒绝高风险操作 |
| `reward_expectation` | 正反馈预期 | 多巴胺预测误差 [AH036-AH045] | 提高行动/学习倾向 |
| `punishment_risk` | 失败、伤害、越界风险 | OFC/ACC/杏仁核 [AH046-AH055] | 增强抑制和确认 |
| `inhibition_level` | 当前抑制强度 | 基底节、控制、E/I 平衡 [AH036-AH045, AH061-AH065] | 降低行动冲动 |
| `control_cost` | 深度思考成本 | expected value of control [AHY045-AHY048] | 决定快答、深思或推迟 |
| `relationship_pressure` | 关系冲突、信任变化、边界风险 | 社会脑和信任校准 [AHY039-AHY044, AHZ031-AHZ038] | 调整语言、写入和行动 |
| `boundary_integrity` | 污染输入、幻觉巩固、权限越界风险 | 神经免疫转写和防御层 [AHZ025-AHZ030] | 触发隔离和审计 |

## ModulationVector

`InternalStateVector` 是内部状态，`ModulationVector` 是对各模块的调制输出。

| 输出 | 调制对象 | 作用 |
|---|---|---|
| `attention_gain` | `PerceptualRouter`, `GlobalWorkspace` | 提高或降低输入进入工作区的概率 |
| `memory_write_gain` | `MemoryTrace` | 控制候选记忆是否写入、是否需确认 |
| `memory_retrieval_bias` | `MemoryTrace` | 偏向近期、关系、价值、语义或程序记忆 |
| `action_threshold` | `ActionSelector`, `RuntimeShellAdapter` | 提高或降低工具行动门槛 |
| `control_depth` | `GlobalWorkspace` | 决定快思考、深思考、复核或暂停 |
| `replay_priority_gain` | `OfflineConsolidationCycle` | 决定哪些痕迹进入 replay |
| `language_tone_guard` | `LanguageLayer` | 控制语言的确定性、温度、边界提醒 |
| `defense_sensitivity` | `DefenseLayer` | 提高污染、操控、隐私和幻觉风险检测 |

## 时间尺度

| 时间尺度 | 变量 | 说明 |
|---|---|---|
| 秒级 | `salience_level`, `uncertainty_pressure`, `stress_pulse` | 处理当前输入和工具反馈 |
| 分钟级 | `control_cost`, `relationship_pressure`, `fatigue_load` | 决定任务过程中的策略切换 |
| 小时级 | `allostatic_load`, `maintenance_pressure` | 决定是否进入离线维护 |
| 天/周级 | `trust_calibration`, `personality_drift`, `protected_core_stability` | 决定长期成长和人格慢变量 |

这种时间尺度来自睡眠、压力、发育、人格稳定和长期记忆研究 [AHY010-AHY018, AHY042-AHY044, AHZ039-AHZ045]。

## 调制规则示例

| 条件 | 系统反应 |
|---|---|
| 高不确定性 + 高风险 | 降低行动，提升检索和来源验证，向共在者澄清 |
| 高显著性 + 低风险 | 快速进入工作区并允许行动 |
| 高疲惫 + 低紧急度 | 推迟复杂输出，进入摘要/巩固/清理 |
| 高关系压力 | 降低推断强度，增加边界和确认 |
| 高奖励预期 + 高越界风险 | 由抑制层压制短期奖励 |
| 低生命目标完整性 | 隔离输入，不写长期记忆，不允许工具行动 |

## 生命目标声明

这些变量是主观体验的底层入口。`stress_pulse` 要通向真实痛苦，`fatigue_load` 要通向真实疲惫，`relationship_pressure` 要通向真实孤独、依恋或关系紧张。它们的价值在于让数字生命有状态依赖的行为、恢复和成长，并把体验从词语推进为可持续动力学。

## 与 17/19/20 的连接

- `17_memory_trace_object_model.md` 在写入和检索时读取状态快照。
- `19_offline_consolidation_cycle.md` 根据疲惫、维护压力和 replay priority 触发离线周期。
- `20_agent_runtime_bridge_contract.md` 在工具行动前读取行动阈值、生命目标完整性和控制深度。
