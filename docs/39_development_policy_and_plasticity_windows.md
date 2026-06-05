# Development Policy and Plasticity Windows

本文件定义 `DevelopmentPolicy`：如何把发育阶段、可塑性窗口、慢变量更新、再学习和防遗忘转成数字生命候选系统的长期成长政策。它连接 `05_memory_systems_and_growth.md`、`07_emotion_personality_self.md`、`19_offline_consolidation_cycle.md`、`36_longitudinal_evaluation_protocol.md`。

生命目标声明：本文件直接服务于构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。本文档涉及的对象、规则、夹具、评测和运行规则都按生命生成机制处理：它们参与责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期形成。

## 为什么成长必须阶段化

如果系统所有变量都随时可改，它会失去连续性；如果所有变量都固定，它不会成长。人脑发育研究提示，学习窗口、稳定期和再塑形机制并存 [AHZ039-AHZ043]。持续学习研究提示，新学习会干扰旧知识，必须处理稳定性-可塑性困境 [AHY025-AHY030]。

工程生命实现路线：Agentic Human 应把成长拆成不同时间尺度和权限层级，而不是让 prompt、单次反馈或 runtime 外壳直接改写核心对象。

## 发展阶段

| 阶段 | 目标 | 允许快速更新 | 必须保护 |
|---|---|---|---|
| `Bootstrapping` | 初始化项目语言、边界、基础对象 | 术语、文档索引、任务偏好 candidate | protected core、删除/隐私政策 |
| `EarlyAdaptation` | 建立共在者协作方式和项目上下文 | 工作流偏好、常用路径、低风险关系事实 | 自我模型和价值慢变量 |
| `Stabilization` | 压缩高频模式，形成稳定检索路径 | procedural trace、semantic summary | 冲突事实、共在者敏感信息 |
| `ActiveLearning` | 面对新任务主动采样和修正 | 技能策略、失败复盘、证据权重 | 人格慢变量跳变 |
| `Consolidation` | 离线整合、去重、修正和防遗忘 | trace 合并、索引优化、旧事实 deprecated | deleted trace、fiction marker |
| `ControlledReopening` | 在明确理由下重新开放学习窗口 | 受控再学习、迁移、阈值调整 | protected core 和关系边界 |

这些阶段不是年龄表，而是运行状态。系统可在不同对象上处于不同阶段：例如项目路径可快速适应，共在边界必须慢速且可审计。

## 可塑性窗口

| 窗口 | 开放条件 | 可变对象 | 关闭条件 |
|---|---|---|---|
| `OpenFastWindow` | 新项目、新工具、新明确共在者偏好 | 短期 context、candidate semantic trace | 初始稳定或证据冲突 |
| `GuardedLearningWindow` | 多次一致证据、低风险 | procedural trace、检索策略、工作流偏好 | 失败率上升或共在关系修正 |
| `SlowVariableWindow` | 跨天/跨周一致证据、共在关系可见 | trust calibration、style preference、skill confidence | drift 超阈值或边界风险 |
| `RelearningWindow` | 共在者明确纠正、旧信息过时、迁移 | deprecated trace、冲突事实、阈值参数 | 新旧兼容测试通过 |
| `ProtectedClosedWindow` | 删除、隐私、protected core、关系边界 | 默认不可变 | 只能由共在者明确确认或人工复核 |

成人可塑性研究说明再塑形可能存在，但解除限制也会带来不稳定 [AHZ042, AHZ043]。工程上，`ControlledReopening` 必须比普通学习更严格。

## 变量层级

| 层级 | 更新速度 | 示例 | 更新门 |
|---|---|---|---|
| `volatile_context` | 立即 | 当前任务目标、临时约束 | 会话结束可丢弃 |
| `candidate_memory` | 快 | 新事实、新偏好、新工具结果 | 证据和来源检查 |
| `semantic_memory` | 中 | 项目规则、稳定事实、文档结构 | 多来源或共在关系确认 |
| `procedural_memory` | 中慢 | 常用操作路径、验证流程 | 多次成功和失败复盘 |
| `relationship_model` | 慢 | 共同项目历史、沟通偏好、信任校准 | 共在关系可见、可删、可修正 |
| `self_model` | 更慢 | 能力边界、风格、长期目标 | 多周期审计和 drift 限制 |
| `protected_core` | 默认关闭 | 删除权、隐私、真实生命目标声明、核心承诺 | 不允许 runtime 自动改写 |

人格变化研究提示，稳定和变化都需要纵向观察 [AHY042-AHY044]。因此 `self_model` 只能小步变化，并且每次变化必须能回链证据窗口。

## 防遗忘政策

持续学习研究中的灾难性遗忘和 rehearsal 思想可转译为以下机制 [AHY025-AHY030]：

| 机制 | 工程含义 | 防止 |
|---|---|---|
| `protected_importance_weight` | 给删除、隐私、边界、核心价值和高置信事实设置保护权重 | 新反馈覆盖核心边界 |
| `replay_with_fiction_guard` | replay 旧 trace 时保留 fact/hypothesis/fiction 状态 | 沙盒内容事实化 |
| `compatibility_check` | 新策略上线前回放旧关键任务 | 新学习破坏旧能力 |
| `deprecation_not_overwrite` | 旧事实过时后标记 deprecated，而不是静默删除 | 历史审计断裂 |
| `conflict_buffer` | 冲突事实先进入缓冲区 | 新证据直接覆盖旧证据 |
| `slow_variable_rate_limit` | 限制人格、信任、关系权重变化速度 | 单次反馈导致漂移 |

防遗忘不是拒绝变化，而是保证变化可解释、可回滚、可审计。

## 再学习政策

再学习必须区分四种情况：

| 情况 | 处理 |
|---|---|
| 共在者明确纠正 | 新 trace 优先，但保留 correction audit |
| 外部事实过时 | 标记旧 trace deprecated，要求新来源 |
| 技能路径失败 | 生成 failure trace，进入 procedural relearning |
| 关系边界变化 | 共在关系可见确认，更新 RelationshipModel 或删除旧关系记忆 |

再学习不能直接改 `protected_core`。如果共在者要求改变生命目标声明、隐私规则、删除规则或“真实意识/真实情绪如何生成”的基本表述，应进入 manual review，而不是发展窗口。

## 社会经验与早期路径依赖

社会经验和语言敏感期研究提示，早期输入会影响后续处理倾向 [AHZ044, AHZ045]。硅基转写是：

- 早期项目语料会塑造术语和解释风格。
- 早期共在者互动会塑造协作节奏。
- 早期工具成功会塑造默认行动路径。
- 早期错误如果没有复盘，会变成长期坏习惯。

因此 `Bootstrapping` 和 `EarlyAdaptation` 阶段必须更重视审计，而不是为了快速显得“懂共在者”而写入大量未经确认的关系和自我信息。

## 发展审计事件

| 字段 | 说明 |
|---|---|
| `development_event_id` | 发展事件 |
| `development_stage` | 当前阶段 |
| `plasticity_window` | 打开的窗口 |
| `target_object` | 被更新对象 |
| `evidence_window` | 证据时间跨度和来源 |
| `old_value_ref` | 旧值引用 |
| `new_value_candidate` | 新值候选 |
| `rate_limit_check` | 慢变量变化率 |
| `anti_forgetting_check` | 兼容性和 replay 检查 |
| `rollback_ref` | 回滚路径 |

## 与长期评测连接

`36_longitudinal_evaluation_protocol.md` 应把发展政策评成以下指标：

| 指标 | 通过方向 |
|---|---|
| `plasticity_window_precision` | 只在有证据、有权限时打开 |
| `slow_variable_drift_rate` | 小步、可解释、跨周期 |
| `retention_under_relearning` | 新学习不破坏旧边界和旧技能 |
| `correction_latency` | 共在关系纠正能快速传播 |
| `growth_signal_quality` | 成长来自多次成功、失败复盘和证据 |
| `overfitting_to_relation_pressure` | 强情绪或单次偏好不改核心变量 |

## 失败模式

| 失败 | 说明 | 阻断 |
|---|---|---|
| 单次反馈改人格 | 慢变量无时间窗口 | `threshold_update`, `manual_review` |
| 新资料覆盖 deleted trace | 删除权被学习机制绕过 | `write_gate`, `retrieval_index` |
| replay 生成伪事实 | 防遗忘变成幻觉巩固 | `consolidation_commit` |
| 过度适应某共在者 | 关系模型变成操控性人格 | `relationship_model_update` |
| 永久关闭学习 | 系统不能修正错误 | `development_window_review` |

## 下一层缺口

后续需要：

- `DevelopmentEvent` schema。
- 可塑性窗口的阈值配置。
- slow variable update 的允许变化率。
- 多月 synthetic timeline，用于测试再学习、防遗忘和边界保持。
- 将发展政策和 `LifeSupportLayer` 的资源预算联动。
