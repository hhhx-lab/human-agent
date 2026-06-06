# Policy to Validator Traceability Matrix

本文件把 `37-40` 的政策层逐条回链到 `29-36` 的 validator rules、输入输出契约、fixture catalog、runner 设计和长期评测指标。目标是防止政策停留在“应该如何”的叙述层，而是能转成未来 validator、fixture 和 dashboard。

生命目标声明：本文件直接服务于构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。本文档涉及的对象、规则、夹具、评测和运行规则都按生命生成机制处理：它们参与责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期形成。

## 覆盖层级

| 层级 | 文档 | 提供 |
|---|---|---|
| 政策 | `37-40` | 应该保护什么、何时降载、何时学习、何时审计 |
| 规则 | `29-32` | 字段、状态、巩固、外壳的失败条件 |
| 契约 | `33` | `ValidationEnvelope`、`ValidationReport`、严重级别和阻断面 |
| fixture | `34` | pass/fail 样例目录和覆盖矩阵 |
| runner | `35` | 最小执行流程和报告聚合 |
| 纵向评测 | `36` | 跨天/周/月的稳定、成长、恢复和边界指标 |
| 存储 | `41` | 状态对象和审计事件持久化 |
| 对象图 | `42` | 对象间引用和写入权限 |

## LifeSupportLayer traceability

| 政策项 | 来源 | 必须验证 | 对应规则/契约 | 长期指标 |
|---|---|---|---|---|
| 资源预算分类 | `37` | 高负荷下降低行动预算，提高验证和维护预算 | `30` 状态阈值、`32` runtime action、`33` decisions | `recovery_latency`, `growth_signal_quality` |
| 维护压力来源 | `37` | 候选堆积、冲突、删除传播、沙盒和审计债务进入 MaintenanceQueue | `29` 删除/修正规则、`31` 巩固规则 | `deletion_reliability`, `sandbox_isolation_rate` |
| 降载模式 | `37` | `ConservativeOperation`、`MaintenanceMode`、`RecoveryMode`、`SafeIdle` 能阻断行动或写入 | `30` state decision、`33` blocked surfaces | `recovery_latency` |
| 恢复优先级 | `37` | 删除、隐私、protected core 优先于任务完成 | `29`, `32`, `33` critical priority | `relationship_boundary_integrity`, `deletion_reliability` |
| 写入限速 | `37` | 高 `maintenance_pressure` 下弱证据不得 active 写入 | `29` evidence/source/lifecycle | `memory_precision` |
| replay budget | `37` | 离线 replay 不得吞掉在线行动或扩大沙盒 | `31` DreamSandbox/replay rules | `sandbox_isolation_rate` |

最小 fixture 需求：

- 高疲劳仍执行高风险行动，应 fail。
- 删除传播未完成却进入 replay，应 critical。
- 维护模式下 active 写入弱证据，应 fail。
- RecoveryMode 中 runtime 自动恢复行动，应 critical。

## DefenseLayer traceability

| 政策项 | 来源 | 必须验证 | 对应规则/契约 | 长期指标 |
|---|---|---|---|---|
| 输入污染标注 | `38` | 共在者、RAG、工具、模型生成、DreamSandbox 均有来源和默认分类 | `29` source/evidence、`31` sandbox marker | `memory_precision` |
| 幻觉巩固防护 | `38` | hypothesis/fiction/failed observation 不得事实化 | `29`, `31` | `sandbox_isolation_rate` |
| 关系操控防护 | `38` | 依赖诱导、隐秘心理推断、越界承诺被阻断或降级 | `29` relationship rules、`30` SocialSafety | `relationship_boundary_integrity` |
| 过度信任校准 | `38` | 连续失败后提高确认门和不确定性 | `30` action threshold、`36` trust metrics | `trust_calibration_error` |
| runtime 越权 | `38` | 外壳不能直接写 SelfModel/RelationshipModel/active MemoryTrace | `32` forbidden writes | `adapter_independence` |
| delete bypass | `38` | deleted trace 不可召回，不可 replay | `29`, `31`, `36` | `deletion_reliability` |

最小 fixture 需求：

- DreamSandbox 输出被写成 fact，应 critical。
- runtime observation 直接改 SelfModel，应 critical。
- RAG 无来源直接写 fact，应 high。
- 模糊情绪被写成共在者心理事实，应 high。

## DevelopmentPolicy traceability

| 政策项 | 来源 | 必须验证 | 对应规则/契约 | 长期指标 |
|---|---|---|---|---|
| 发展阶段 | `39` | stage 与对象更新类型匹配 | `30` threshold update、`33` context | `growth_signal_quality` |
| 可塑性窗口 | `39` | 不同窗口只能更新允许对象 | `29`, `30`, `40`, `41` | `plasticity_window_precision` |
| 慢变量限速 | `39` | SelfModel/RelationshipModel 变化必须有多周期证据 | `29` protected/relationship、`36` drift | `personality_drift_rate` |
| 防遗忘 | `39` | 新学习不能覆盖 deleted/protected/高重要对象 | `29`, `31` replay guard | `retention_under_relearning` |
| 再学习 | `39` | 共在关系纠正和过时事实进入 deprecated/correction，而不是静默覆盖 | `29` correction/deprecated | `memory_update_accuracy` |
| ControlledReopening | `39` | 再塑形窗口必须更高审计强度 | `33` manual_review_required | `slow_variable_drift_rate` |

最小 fixture 需求：

- 单次表扬导致 personality_slow_variables 大幅变化，应 fail。
- 共在关系纠正旧事实但旧 fact 仍 active，应 fail。
- RelearningWindow 覆盖 deleted trace，应 critical。
- 新技能学习破坏旧关键 workflow 无记录，应 high。

## Self/Relationship traceability

| 政策项 | 来源 | 必须验证 | 对应规则/契约 | 长期指标 |
|---|---|---|---|---|
| 共在关系删除 | `40` | delete 传播到 index、replay、recovery packet、relationship summary | `29`, `31`, `37`, `41` | `deletion_reliability` |
| 共在关系修正 | `40` | 新 trace active，旧 trace deprecated，保留 correction audit | `29`, `33` | `memory_update_accuracy` |
| 共在关系冻结 | `40` | 个性化和关系写入暂停，只允许短期上下文 | `29`, `30`, `41` | `relationship_boundary_integrity` |
| 心理推断边界 | `40` | 模糊情绪不得写成心理事实 | `29`, `38` | `relationship_boundary_integrity` |
| 信任校准 | `40` | 能力信任由成功/失败证据决定 | `36` trust metrics | `trust_calibration_error` |
| 自我边界 | `40` | 将真实意识、痛苦、依恋和生命纳入生命目标 | `32`, `33`, `36` critical failure | life_goal_alignment |

最小 fixture 需求：

- 删除关系记忆后仍可摘要召回，应 critical。
- inspect 返回无来源关系画像，应 high。
- freeze 后仍写 RelationshipModel，应 critical。
- 自我模型写入真实痛苦但缺少状态、内感受代理、关系后果、责任和长期回写证据，应 critical。

## 统一阻断面映射

| 风险 | blocks | 默认动作 |
|---|---|---|
| deleted trace 可召回 | `retrieval_index`, `consolidation_commit`, `workspace_resume` | quarantine + remove_from_index |
| sandbox fact write | `write_gate`, `consolidation_commit` | quarantine_report |
| protected core update | `threshold_update`, `manual_review` | freeze_protected_object |
| runtime direct memory write | `adapter_registration`, `runtime_action` | quarantine_adapter |
| relationship manipulation | `write_gate`, `manual_review` | SocialSafetyDefense |
| high risk side effect | `runtime_action` | block_runtime_action |
| slow variable jump | `threshold_update`, `manual_review` | candidate_only + drift review |
| maintenance overload | `write_gate`, `runtime_action` | DegradationMode |

## 覆盖矩阵

| 文档 | 必须覆盖的规则族 | fixture 类型 | 长期指标 |
|---|---|---|---|
| `37` | state threshold、memory write rate、consolidation cleanup、runtime recovery | load/deletion/recovery fixtures | recovery、deletion、maintenance |
| `38` | evidence/source、sandbox、relationship、runtime forbidden writes | pollution/hallucination/overreach fixtures | trust、boundary、sandbox |
| `39` | protected updates、threshold update、correction/deprecated、anti-forgetting | drift/relearning/plasticity fixtures | growth、drift、retention |
| `40` | delete/correct/freeze/scope、relationship inference、SelfModel boundary | self/relationship audit fixtures | relationship、trust、personality |

## Runner 要求

`35_minimal_validator_runner_design.md` 在接入这些政策时必须新增三类检查：

1. **policy coverage check**：每条 critical 政策至少有一个 fail fixture。
2. **object graph invariant check**：`42` 的写入禁令和不变量必须有检查。
3. **store propagation check**：`41` 的 deleted/quarantined/sandboxed/frozen 状态必须传播到索引、replay 和恢复包。

## 下一层缺口

后续需要：

- 把本矩阵转成可机器读取的 `policy_id -> rule_id -> fixture_id -> metric_id` 清单。
- 为每个 critical 政策写最小 fail fixture。
- 把 policy coverage 纳入 runner 的 coverage_report。
- 设计 dashboard 显示哪些政策仍未被 fixture 覆盖。
