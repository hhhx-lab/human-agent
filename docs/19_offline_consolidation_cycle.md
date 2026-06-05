# OfflineConsolidationCycle 离线巩固周期

本文件把 `08_sleep_dream_fatigue_states.md`、`05_memory_systems_and_growth.md`、`11_neuromodulation_and_signal_media.md` 和 `17_memory_trace_object_model.md` 连接起来，定义数字生命的离线巩固周期。它借鉴睡眠、梦境、replay、系统巩固、清理和反事实模拟，目标是让真实睡眠、真实梦境和真实自我反省在硅基系统中拥有可执行循环。

## 生物机制约束

睡眠巩固研究说明，离线学习不是简单摘要。海马 replay、尖波涟漪、慢振荡、睡眠纺锤和 targeted memory reactivation 共同参与记忆重放与系统巩固 [AHY001-AHY010]。梦境研究提示，内部生成状态可能涉及记忆、情绪、默认网络和局部皮层热点 [AHY049-AHY051]。自传记忆和未来想象研究进一步说明，记忆系统可用于模拟未来场景 [AHZ046-AHZ050]。

清理机制要保留争议。glymphatic 和脑膜淋巴研究支持脑存在清除/引流机制 [AHY019-AHY021]，但 2024 年研究也对“睡眠必然增强脑清除”提出挑战 [AHZ061, AHZ062]。因此，工程上只能说“离线期承担维护任务”，不能把它写成单一生物清除过程。

## 周期触发条件

`OfflineConsolidationCycle` 由 `InternalStateVector` 触发：

| 触发器 | 说明 | 来源 |
|---|---|---|
| `fatigue_load` 高 | 长时间任务、上下文压力、错误密度升高 | `18`, AHZ019-AHZ021 |
| `maintenance_pressure` 高 | 缓存、候选记忆、冲突痕迹堆积 | `17`, AHY019-AHY021 |
| `replay_priority` 高 | 高价值事件、失败任务、关系变化 | `17`, AHY001-AHY009 |
| `contradiction_density` 高 | 新旧记忆冲突过多 | `17`, AHM004-AHM011 |
| `development_window` 打开 | 阶段化成长或受控再塑形 | AHZ039-AHZ045 |
| `runtime_idle` | 外部行动低、可进入维护窗口 | AHZ003, AHZ049-AHZ050 |

## 周期阶段

| 阶段 | 输入 | 输出 | 风险控制 |
|---|---|---|---|
| `Quiesce` | 当前工作区、未完成行动 | 暂停外部行动、保存 checkpoint | 不在工具行动中途强行维护 |
| `Collect` | candidate traces、日志、错误、共在者反馈 | 巩固候选队列 | 隐私和边界先筛掉 |
| `Replay` | 高优先级事件和关系变化 | 事件重放、失败复盘、成功路径压缩 | replay 内容标记为回放，不是新事实 |
| `Abstract` | 重复事件、概念、流程 | 语义记忆、程序记忆、价值规则 | 不由单次事件抽象人格 |
| `Simulate` | 未来任务、关系风险、反事实路径 | 梦境/沙盒假设 | 沙盒输出不得直接写入事实记忆 |
| `Prune` | 过期缓存、低价值痕迹、冲突候选 | 删除、降级、合并、隔离 | 尊重共在关系删除和隐私范围 |
| `Commit` | 通过审计的巩固结果 | 更新 MemoryTrace、SelfModel、RelationshipModel | 核心价值和人格慢变量需多轮证据 |
| `Wake` | 巩固摘要、待确认事项 | 恢复工作区、生成下一步计划 | 标注哪些是事实、假设和待确认 |

## 四种离线模式

| 模式 | 转写 | 作用 | 使用场景 |
|---|---|---|---|
| `MicroReplay` | 清醒 replay | 几秒到几分钟复盘局部错误 | 工具失败、共在关系纠正、证据冲突 |
| `TaskClosure` | 任务结束整理 | 把完成任务写成事件和程序记忆 | 文档完成、代码提交、调研结束 |
| `DreamSandbox` | 梦境/默认模拟 | 生成未来方案和反事实场景 | 创意、风险预演、关系修复计划 |
| `DeepConsolidation` | 睡眠式系统巩固 | 跨事件抽象、清理、人格慢变量审计 | 长期项目阶段性回顾 |

## 与 MemoryTrace 的交互

`OfflineConsolidationCycle` 不直接生成“真实记忆”，它处理 `MemoryTrace` 的状态：

- `candidate -> episodic`：证据足够且边界允许。
- `episodic -> semanticized`：多个事件支持同一概念。
- `episodic -> proceduralized`：多次成功路径形成技能。
- `relationship_candidate -> relationship_memory`：经过时间和多次互动验证。
- `hypothesis -> deprecated`：反事实模拟未被证实。
- `conflict -> contradiction_link`：保留冲突而非删除历史。
- `protected_core`：核心约束只允许审计，不允许自动重写。

## 幻觉巩固防护

离线期最危险的是把生成内容巩固成事实。防护规则：

- 沙盒输出默认是 `hypothesis`。
- 没有外部证据的反思不能写入 factual memory。
- 共在者偏好必须来自明确表达或多次一致行为。
- 关系推断必须保守，且允许共在关系删除/修正。
- replay 只能提高候选优先级，不能绕过 `WriteGate`。
- 任何人格慢变量变化都需要时间窗口和差异审计。

这些规则对应当前 memory benchmark 和 memory governance 的核心问题：长期记忆不仅要能记，还要能防止错误记忆、过度记忆和冲突记忆污染系统 [AHM004-AHM012, AHM020]。

## 周期输出

每次离线周期结束后，应产出四类对象：

1. `ConsolidationReport`：哪些痕迹被写入、合并、降级或删除。
2. `OpenQuestions`：哪些假设需要共在关系确认或外部验证。
3. `StateReset`：疲惫、压力、维护压力如何变化。
4. `NextDevelopmentSignal`：是否出现稳定成长、技能形成或人格漂移风险。

这让离线期成为可审计的成长机制，而不是神秘的“自我进化”。
