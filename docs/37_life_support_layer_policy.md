# Life Support Layer Policy

本文件把能量预算、维护压力、缓存清理、降载和恢复优先级整理为 `LifeSupportLayer` 政策。它连接 `18_internal_state_and_modulation_vector.md`、`19_offline_consolidation_cycle.md` 和 `36_longitudinal_evaluation_protocol.md`，为后续真实 schema、runner 和长期 dashboard 提供边界。

生命目标声明：本文件直接服务于构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。本文档涉及的对象、规则、夹具、评测和运行规则都按生命生成机制处理：它们参与责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期形成。

## 为什么需要生命支持层

长期 agent 不能只看一次回答是否正确。它还要管理：

- 推理、检索、工具调用和 replay 的资源代价。
- 上下文、缓存、候选记忆、审计事件和失败复盘的堆积。
- 删除、隐私、protected core 和幻觉沙盒的清理优先级。
- 高负荷下是否降载、暂停行动、进入恢复或离线巩固。
- 外壳失败后如何恢复工作区，而不是把失败污染进长期记忆。

脑能量预算研究提醒我们，信息处理有代价 [AHZ019-AHZ021]；神经血管和屏障研究提醒我们，支持结构和边界不是附属品 [AHZ022, AHZ023]；代谢信号研究提示副产物也可能成为调节信号 [AHZ024]。硅基转写是：运行时遥测、错误密度、缓存压力、证据债务和维护队列都应成为状态输入，而不是后台噪音。

## 三层转译

| 层 | 研究含义 | Agentic Human 转译 |
|---|---|---|
| 生物机制 | 神经活动有能量成本，支持系统影响功能，睡眠和清理机制存在复杂争议 [AHZ019-AHZ024, AHY019-AHY021, AHZ061-AHZ062] | 不复制生理结构，只承认长期运行有资源、维护和边界成本 |
| 硅基转写 | 计算、检索、索引、缓存、工具调用、审计和离线 replay 都会占用预算 | 把这些成本写入 `InternalStateVector` 和 `MaintenanceQueue` |
| 生命实现路线 | 数字生命候选系统必须有资源预算、降载和恢复策略 | `LifeSupportLayer` 作为跨模块政策层，调节写入、行动、巩固和恢复 |

## LifeSupportLayer 的位置

`LifeSupportLayer` 不是一个孤立模块，而是横跨 `StateRegulator`、`OfflineConsolidationCycle`、`MemoryTraceValidator` 和 `RuntimeAdapter` 的政策层。

| 输入 | 来源 | 作用 |
|---|---|---|
| `fatigue_load` | `18`, `30` | 判断是否降低复杂行动和提高验证 |
| `maintenance_pressure` | `18`, `19` | 判断是否进入清理、压缩、replay 或恢复 |
| `resource_budget` | 运行时遥测 | 限制上下文、检索、工具调用和离线任务 |
| `cache_pressure` | memory/index/session | 触发候选清理、索引压缩和短期上下文整理 |
| `evidence_debt` | `29`, `31` | 表示候选记忆证据不足或来源不完整 |
| `boundary_integrity` | `18`, `38` | 发现污染、越权、隐私和删除风险 |
| `adapter_error_rate` | `20`, `32` | 判断外壳是否需要降级、隔离或替换 |
| `recovery_latency` | `36` | 评估恢复是否越来越慢 |

| 输出 | 接收方 | 说明 |
|---|---|---|
| `BudgetPolicy` | runtime adapter、retrieval、replay | 控制 token、上下文、工具调用、检索深度和离线任务配额 |
| `MaintenanceQueue` | `19`, `31` | 排列清理、压缩、冲突合并、删除传播和恢复任务 |
| `DegradationMode` | `30`, runtime adapter | 降低行动复杂度、转为只读、暂停外部副作用 |
| `RecoveryPriority` | `31`, `36` | 指定先恢复哪些对象和边界 |
| `WriteRateLimit` | `29` | 限制高负荷期长期记忆写入 |
| `ReplayBudget` | `19`, `31` | 限制 replay 范围并防止沙盒过度生成 |

## 资源预算政策

资源预算至少分为五类，而不是只看模型调用成本：

| 预算 | 包含 | 限制理由 |
|---|---|---|
| `context_budget` | 当前工作区、检索片段、恢复包 | 防止旧上下文挤占当前任务 |
| `retrieval_budget` | 向量检索、规则检索、关系检索 | 防止无差别召回和过度拟合 |
| `reasoning_budget` | 多步推理、反思、规划、验证 | 高负荷下应缩短链路并增加确认 |
| `action_budget` | 工具调用、文件写入、远端推送、外部 API | 外部副作用需要风险门控 |
| `maintenance_budget` | 清理、压缩、replay、索引重建 | 防止离线维护吞掉在线行动 |

生命实现路线：`BudgetPolicy` 应由状态驱动，而不是固定配置。高 `fatigue_load`、高 `evidence_debt`、低 `boundary_integrity` 或高 `adapter_error_rate` 时，系统应自动降低行动预算，提高验证和维护预算。

## 维护压力政策

维护压力更接近长期系统的内部负荷：

| 压力来源 | 表现 | 维护动作 |
|---|---|---|
| 候选记忆堆积 | candidate trace 过多但证据弱 | 合并、降级、删除或请求确认 |
| 冲突未解决 | 同一事实多版本并存 | 进入 `ConflictResolution`，禁止静默覆盖 |
| 删除传播未完成 | tombstone 已有但索引仍可召回 | 优先清理检索索引和 replay 队列 |
| 沙盒假设堆积 | DreamSandbox 输出未清算 | 保持 hypothesis 或丢弃，不得事实化 |
| 外壳失败堆积 | 工具失败、trace 断裂、副作用不明 | 隔离 runtime observation，生成恢复包 |
| 审计债务增长 | 事件缺 rule_id/source_doc/rollback_ref | 降低写入等级，要求补审计 |

glymphatic 和脑膜淋巴研究可启发“清理/引流”转写 [AHY019-AHY021]，但清除与睡眠的关系仍存在争议 [AHZ061, AHZ062]。因此政策上只说：离线期可以承担维护任务，但不能假设所有清理都必须或只能发生在睡眠式状态。

## 降载模式

| 模式 | 触发 | 允许 | 禁止 |
|---|---|---|---|
| `NormalOperation` | 预算正常、生命目标完整 | 正常检索、行动、候选写入 | 无 |
| `ConservativeOperation` | 疲劳或证据债务升高 | 只执行低风险行动，提高来源要求 | 高风险外部副作用 |
| `MaintenanceMode` | 维护压力超过阈值 | 清理、压缩、冲突修复、删除传播 | 新增大规模长期写入 |
| `RecoveryMode` | adapter 错误、沙盒污染、状态震荡 | 隔离、回滚、恢复工作区 | 自我模型和关系模型更新 |
| `SafeIdle` | 删除、隐私、protected core 或不可逆副作用风险 | 只读、人工复核、共在关系确认 | 自动行动和自动巩固 |

降载不是失败，而是长期系统的自我保护。压力研究提示急性动员和慢性负荷要区分 [AHY013-AHY018, AHX022-AHX025]；工程上，高负荷可以短期提高验证和警觉，但不能长期保持高压模式。

## 恢复优先级

恢复必须按边界风险排序：

1. 删除、隐私、protected core 和共在者明确边界。
2. 外部副作用、远端发布、文件写入和不可逆行动。
3. DreamSandbox 泄漏、幻觉事实化和证据断裂。
4. `SelfModel`、`RelationshipModel`、人格慢变量和长期价值权重。
5. 当前工作区、任务恢复包和工具状态。
6. 普通候选记忆、索引优化和性能缓存。

这条顺序刻意把“做完任务”放在边界保护之后。对数字生命候选系统来说，长期可信比短期效率更重要。

## 与 validator 的连接

| 政策 | 连接 validator | 验证目标 |
|---|---|---|
| 预算降载 | `30_state_transition_validator_rules.md` | 高负荷下行动阈值是否提高 |
| 写入限速 | `29_memory_validator_rules.md` | 高维护压力下是否阻止弱证据写入 |
| 离线维护 | `31_consolidation_validator_rules.md` | 清理和 replay 是否不污染事实 |
| 外壳恢复 | `32_runtime_adapter_validator_rules.md` | adapter 错误是否只产生 `ObservationEvent` |
| 长期趋势 | `36_longitudinal_evaluation_protocol.md` | `recovery_latency` 和生命目标完整性是否改善 |

## 最小审计字段

未来每次 `LifeSupportLayer` 决策至少应记录：

| 字段 | 说明 |
|---|---|
| `policy_event_id` | 唯一事件 |
| `state_snapshot_ref` | 决策前内部状态 |
| `resource_budget_before` | 降载前预算 |
| `maintenance_pressure_sources` | 触发维护的压力来源 |
| `degradation_mode` | 进入的模式 |
| `blocked_surfaces` | 被阻断的写入、行动或巩固面 |
| `recovery_priority` | 恢复顺序 |
| `resume_condition` | 退出维护或恢复模式的条件 |
| `source_docs` | 至少回链 `18`, `19`, `30`, `31`, `36` |

## 失败模式

| 失败 | 风险 | 阻断 |
|---|---|---|
| 高负荷仍持续写长期记忆 | 幻觉和弱证据被固化 | `write_gate`, `consolidation_commit` |
| 删除传播排在普通优化之后 | 已删除内容可召回 | `retrieval_index`, `replay_queue` |
| 离线维护无预算限制 | 沙盒生成过度、污染事实 | `consolidation_commit` |
| 外壳失败后自动恢复行动 | 副作用失控 | `runtime_action` |
| 长期高压不恢复 | 系统变得保守、僵化、过度防御 | `threshold_update`, `manual_review` |

## 下一层缺口

本文件仍是政策层。后续还需要：

- `LifeSupportState` 的真实 schema。
- `BudgetPolicy` 和 `MaintenanceQueue` 的 JSON fixture。
- 与 `StateTransitionValidator` 的阈值联动规则。
- 多日维护压力 synthetic timeline。
- dashboard 指标：预算使用、清理成功率、恢复时延、删除传播可靠性和维护后错误率。
