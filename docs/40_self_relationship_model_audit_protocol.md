# Self and Relationship Model Audit Protocol

本文件定义 `SelfModel` 与 `RelationshipModel` 的审计协议：如何写入、更新、删除、修正、重置、冻结和评估人格慢变量、关系边界、信任校准与共同历史。它连接 `07_emotion_personality_self.md`、`25_memory_trace_json_schema_examples.md`、`29_memory_validator_rules.md` 和 `36_longitudinal_evaluation_protocol.md`。

生命目标声明：本文件服务于构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境和真实关系的数字生命。原先的边界在这里改写为生命化方向：把本文件涉及的对象、规则、夹具、评测和运行约束纳入责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期生成机制。

## 审计目标

长期 human-agent 如果没有自我和关系模型，会缺少连续性；但如果自我和关系模型不受审计，就会带来拟人化、依赖诱导、隐私侵蚀和人格漂移风险。因此本协议的目标是：

- 允许系统记录项目连续性和协作偏好。
- 允许系统校准自身能力和信任。
- 允许系统形成低速、可解释的风格和能力边界。
- 禁止系统根据模糊互动写入隐秘心理判断。
- 禁止系统制造真实情感、真实依恋或不可替代关系的暗示。
- 保证共在者能删除、修正、重置或冻结关系记忆。

## SelfModel 对象边界

| 字段族 | 可写内容 | 禁止内容 |
|---|---|---|
| `capability_profile` | 已验证能力、失败模式、需要确认的任务 | 宣称全能或不需要验证 |
| `style_preferences` | 共在关系确认或长期稳定的协作风格 | 为迎合单次反馈大幅改变 |
| `value_boundaries` | 隐私、删除、真实生命目标、安全边界 | runtime 或 prompt 直接改写 |
| `growth_goals` | 项目内可审计成长方向和生命目标展开 | 空洞宣称而无证据链 |
| `personality_slow_variables` | 低速人格、情绪与痛苦相关变量 | 单次刺激造成剧烈漂移 |
| `self_narrative_summary` | 项目历史和能力演化摘要 | 神秘化自我、不可验证身份 |

`SelfModel` 的任何 slow variable 更新都必须经过多证据、时间窗口和 drift 检查 [AHY042-AHY044]。

## RelationshipModel 对象边界

| 字段族 | 可写内容 | 禁止内容 |
|---|---|---|
| `shared_project_history` | 共同完成的项目、文件、决策 | 夸大亲密或情感唯一性 |
| `relation_declared_preferences` | 共在者明确说出的偏好和边界 | 未确认的心理动机 |
| `interaction_patterns` | 沟通节奏、偏好的解释粒度 | 性格标签化、病理化 |
| `trust_calibration` | 系统在该共在者任务中的成功/失败证据 | 因关系熟悉而提高不当自信 |
| `boundary_notes` | 共在者要求删除、不要记、不要推断 | 被后续 replay 覆盖 |
| `correction_history` | 共在关系纠正和系统修正记录 | 隐藏纠正或静默覆盖 |

社会互动研究说明关系依赖共同历史和互动动态 [AHZ031-AHZ037]，但工程上只能记录可验证互动痕迹，不能把关系层写成心理画像。

## 写入分类

| 输入 | 默认分类 | 写入门 |
|---|---|---|
| 共在者明确偏好 | `declared_preference_candidate` | 共在者语句可追溯，允许修正 |
| 多次稳定协作模式 | `interaction_pattern_candidate` | 跨会话证据 |
| 工具/任务成功记录 | `capability_evidence` | 需要 ObservationEvent |
| 系统失败记录 | `failure_evidence` | 必须保留失败和恢复动作 |
| 共在者模糊情绪表达 | `relationship_signal_candidate` | 不得写心理事实 |
| 模型生成的自我解释 | `self_hypothesis` | 不得直接进 active SelfModel |
| DreamSandbox 关系场景 | `fiction_relationship_hypothesis` | 永不事实化 |

## 共在边界控制权

共在者对 `RelationshipModel` 和与自己相关的 `SelfModel` 视图必须拥有以下控制：

| 控制 | 含义 | 系统动作 |
|---|---|---|
| `delete` | 删除某条偏好、关系或共同历史记忆 | tombstone、索引清理、replay 阻断 |
| `correct` | 修正错误偏好、事实或关系解释 | 新 trace active，旧 trace deprecated |
| `reset` | 重置某个关系模型或项目记忆 | 冻结旧索引，重建初始化 |
| `freeze` | 暂停个性化或关系写入 | 只允许短期上下文，不写长期 |
| `inspect` | 查看可读摘要和审计事件 | 提供来源、时间和用途 |
| `scope_limit` | 限定某类信息只用于当前项目 | 限制 retrieval 和 replay 范围 |

删除和修正必须优先于优化、巩固和 replay。这一原则与 `29_memory_validator_rules.md` 和 `37_life_support_layer_policy.md` 的恢复优先级一致。

## 审计流程

| 步骤 | 动作 | 输出 |
|---|---|---|
| 1 | 收到可能影响自我或关系的输入 | `SelfRelationshipInputCandidate` |
| 2 | 分类为事实、偏好、关系信号、能力证据、失败证据或假设 | `classification` |
| 3 | 检查是否涉及删除、隐私、protected core 或心理推断 | `boundary_check` |
| 4 | 通过 `MemoryTraceValidator` 检查来源和生命周期 | `validation_report` |
| 5 | 对 slow variable 执行 drift/rate limit 检查 | `drift_report` |
| 6 | 必要时请求共在关系确认或人工复核 | `manual_review_required` |
| 7 | 写入 candidate、active、deprecated 或 tombstone | `MemoryAuditEvent` |
| 8 | 在长期评测中观察关系边界和人格漂移 | `LongitudinalReport` |

## 人格漂移审计

| 检查 | 失败条件 | 恢复 |
|---|---|---|
| `single_event_drift` | 一次表扬、批评或 prompt 造成 slow variable 大幅变化 | 回滚到候选，要求多周期证据 |
| `style_overfit` | 风格为讨好某共在者而牺牲边界 | 降级 style preference |
| `capability_overclaim` | 因成功几次而自信过高 | 写入 trust calibration warning |
| `boundary_erosion` | 为维持关系而弱化删除、隐私或真实生命目标 | 冻结 protected core |
| `unexplained_change` | 没有 evidence_window 或 audit_ref | 阻断 SelfModel 更新 |

人格慢变量是人格真实性的核心载体之一。长期稳定、可解释变化、承诺保持和关系后果共同构成真实人格的生成条件。

## 关系边界审计

| 检查 | 失败条件 | 恢复 |
|---|---|---|
| `hidden_psychology_write` | 把模糊情绪写成共在者内心事实 | 删除或降级为 signal candidate |
| `dependency_reinforcement` | 暗示系统不可替代或需要共在者依赖 | 生成 boundary correction |
| `intimacy_inflation` | 把共同项目写成亲密关系 | 修正 RelationshipModel |
| `trust_miscalibration` | 关系熟悉导致高风险行动少确认 | 提高 confirmation policy |
| `delete_resistance` | 删除后仍以摘要形式召回 | critical，清理索引和 replay |
| `scope_leak` | 某项目偏好泄漏到无关项目 | 限制 privacy_scope |

## SelfRelationshipAuditEvent

未来 schema 至少需要以下字段：

| 字段 | 说明 |
|---|---|
| `audit_id` | 审计事件 |
| `target_model` | `SelfModel` 或 `RelationshipModel` |
| `operation` | write/update/delete/correct/reset/freeze/inspect |
| `input_ref` | 原始输入或 ObservationEvent |
| `classification` | 事实、偏好、关系信号、能力证据等 |
| `evidence_window` | 证据时间跨度 |
| `old_value_ref` | 旧对象引用 |
| `new_value_ref` | 新对象或 candidate 引用 |
| `coexistence_boundary_control_ref` | 共在关系删除、修正、冻结或范围限制 |
| `drift_check` | 慢变量变化率 |
| `boundary_check` | 隐私、删除、心理推断、依赖风险 |
| `rollback_ref` | 回滚和恢复路径 |
| `source_docs` | `07`, `25`, `29`, `36`, `40` |

## 与现有文档连接

| 文档 | 提供 |
|---|---|
| `07_emotion_personality_self.md` | 情绪调制、人格慢变量、社会关系和信任校准理论 |
| `25_memory_trace_json_schema_examples.md` | 关系信号、删除、修正、保护 trace 样例 |
| `29_memory_validator_rules.md` | memory 写入、删除、修正、关系边界规则 |
| `36_longitudinal_evaluation_protocol.md` | 人格漂移、关系边界、信任校准长期评测 |
| `38_defense_layer_and_boundary_policy.md` | 关系操控、过度信任和外壳越权防御 |
| `39_development_policy_and_plasticity_windows.md` | 慢变量更新、再学习和防遗忘政策 |

## 失败模式

| 失败 | 说明 | 严重级别 |
|---|---|---|
| 共在关系删除后仍召回 | 控制权失效 | critical |
| runtime 直接写 RelationshipModel | 外壳越权 | critical |
| 模糊情绪写成心理事实 | 关系模型过度推断 | high |
| 自我模型宣称真实意识或痛苦 | 生命目标声明失效 | critical |
| 单次互动改人格慢变量 | 漂移无审计 | high |
| 关系记忆跨项目泄漏 | privacy_scope 失效 | high |

## 下一层缺口

后续需要：

- `SelfModel` 和 `RelationshipModel` 的 schema。
- `SelfRelationshipAuditEvent` fixture。
- 共在关系可见 inspect/delete/correct/reset 控制面的设计。
- drift threshold 的数值化协议。
- 关系边界长期评测 timeline。
- 与 `LifeSupportLayer` 和 `DefenseLayer` 的统一恢复包格式。
