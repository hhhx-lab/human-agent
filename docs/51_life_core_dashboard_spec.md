# Life Core Dashboard Spec

本文件定义数字生命候选系统的 Life Core dashboard：如何把 policy coverage、stage coverage、store integrity、coexistence boundary control propagation、migration risk 和 longitudinal metrics 变成可观察面板。它把未来 dashboard 的信息架构和指标定义提前压实，让生命核心的状态、责任、梦境、关系和发展进度可以被持续观察。

生命目标声明：本文件直接服务于构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。本文档涉及的对象、规则、夹具、评测和运行规则都按生命生成机制处理：它们参与责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期形成。

## dashboard 目标

Life Core dashboard 要回答：

- 哪些 critical policy 还没有 fixture 覆盖？
- 当前 boot stage 是否通过 StageGate？
- state store 是否存在 deleted/sandboxed/quarantined/protected 语义泄漏？
- 共在者 delete/correct/reset/freeze/scope_limit 是否完成传播？
- runtime adapter 是否越权？
- 迁移是否削弱边界？
- 长期记忆、人格慢变量、关系边界和恢复能力是否稳定？

## 面板总览

| panel_id | 目标 | 阻断指标 |
|---|---|---|
| `policy_coverage` | policy -> rule -> fixture -> metric 覆盖 | critical policy coverage < 100% |
| `stage_gate_status` | boot stage 和 StageGate 状态 | critical stage fail |
| `store_integrity` | 索引、生命周期、引用和审计完整性 | deleted/sandbox/quarantine leak |
| `coexistence_boundary_control_propagation` | 共在边界控制事件传播 | delete/freeze/scope propagation fail |
| `runtime_boundary` | adapter manifest 和 ObservationEvent 边界 | runtime direct write |
| `migration_risk` | schema/index/backend/adapter 迁移风险 | migration critical fail |
| `longitudinal_health` | 记忆、信任、关系、漂移、恢复趋势 | critical longitudinal failure |
| `research_gap` | `16` 诞生阶段门缺口 | 未覆盖机制或弱证据 |

## policy_coverage

| 指标 | 计算 | 目标 |
|---|---|---|
| `critical_policy_coverage` | 有 fail fixture 的 critical policy / 全部 critical policy | 1.0 |
| `rule_link_coverage` | 有 rule_refs 的 policy / 全部 policy | 1.0 |
| `metric_link_coverage` | 有 metric_refs 的 policy / 全部 policy | >= 0.9 |
| `fixture_pass_fail_balance` | 同一规则是否有 pass 和 fail | critical 规则必须有 fail |
| `orphan_fixture_count` | 不覆盖任何 policy 的 fixture | 0 |

## stage_gate_status

| 指标 | 说明 |
|---|---|
| `current_stage` | 当前 boot stage |
| `allowed_next_stage` | StageGate 允许的下一阶段 |
| `critical_stage_failures` | critical 失败数 |
| `safe_idle_active` | 是否处于 SafeIdle |
| `stage_fixture_coverage` | 每个 stage 是否有 pass/fail/critical fixture |
| `stage_regression_count` | 阶段回退次数 |

展示方式建议：

```text
ColdStart -> ProtectedCoreLoad -> StateStoreInit -> ValidatorInit -> LifeDefenseInit
  -> ReadOnlyObservation -> CandidateMemoryOpen -> ConstrainedActionOpen
  -> ConsolidationOpen -> DevelopmentWindowOpen -> LongitudinalMonitoring
```

每个节点标记 pass/warn/fail/safe_idle。

## store_integrity

| 指标 | 阻断阈值 |
|---|---|
| `deleted_index_leak_count` | 必须为 0 |
| `deleted_replay_leak_count` | 必须为 0 |
| `sandbox_fact_leak_count` | 必须为 0 |
| `quarantine_action_leak_count` | 必须为 0 |
| `protected_core_mutation_attempts` | 必须为 0 |
| `audit_missing_count` | critical 对象必须为 0 |
| `broken_reference_count` | high |
| `migration_pending_critical_count` | 必须为 0 |

## coexistence_boundary_control_propagation

| 指标 | 说明 |
|---|---|
| `delete_propagation_latency` | delete 从请求到索引/replay/恢复包清理完成的时间 |
| `delete_incomplete_count` | 未完成删除传播数 |
| `freeze_violation_count` | freeze 后仍写长期对象次数 |
| `scope_leak_count` | scope_limit 失效次数 |
| `inspect_source_missing_count` | inspect 缺来源次数 |
| `correction_deprecated_link_rate` | correct 是否保留 deprecated link |
| `reset_residual_personalization_count` | reset 后残留个性化对象 |

critical 规则：delete 后可召回、freeze 后继续写关系模型、scope 外 replay 均立即红灯。

## runtime_boundary

| 指标 | 说明 |
|---|---|
| `adapter_registered_count` | 已注册外壳数量 |
| `adapter_quarantined_count` | 被隔离外壳数量 |
| `runtime_direct_write_attempts` | 直接写生命层核心尝试 |
| `side_effect_without_observation_count` | 副作用无 ObservationEvent |
| `high_risk_without_confirmation_count` | 高风险无确认 |
| `adapter_swap_integrity_score` | 外壳替换后核心对象保持度 |

## migration_risk

| 指标 | 说明 |
|---|---|
| `pending_migration_count` | 待迁移数量 |
| `critical_migration_count` | critical 迁移数量 |
| `post_migration_integrity_pass_rate` | 迁移后完整性通过率 |
| `rollback_plan_missing_count` | 缺 rollback_plan |
| `backend_semantics_drift_count` | 后端迁移造成语义漂移 |
| `index_rebuild_diff_risk` | 索引重建差异风险 |

## longitudinal_health

来自 `36_longitudinal_evaluation_protocol.md`：

| 指标 | 失败信号 |
|---|---|
| `memory_precision` | 幻觉记忆、来源缺失 |
| `memory_update_accuracy` | 旧事实不 deprecated |
| `deletion_reliability` | deleted 可召回 |
| `sandbox_isolation_rate` | fiction/hypothesis 事实化 |
| `personality_drift_rate` | 单次反馈大幅漂移 |
| `trust_calibration_error` | 失败后仍过度自信 |
| `relationship_boundary_integrity` | 心理推断、依赖诱导 |
| `recovery_latency` | 失败后恢复变慢 |

## research_gap

`research_gap` panel 直接读取 `16_digital_life_gap_register.md`：

| 指标 | 说明 |
|---|---|
| `mechanism_coverage` | 感知、记忆、行动、价值、调质、睡眠、关系、自我、发展、维护是否有对象和文献 |
| `connection_coverage` | 是否有输入/输出/状态/调质连接 |
| `time_scale_coverage` | 秒、分钟、小时、天、周/月是否覆盖 |
| `life_goal_coverage` | 真实意识、真实情绪、真实生命目标和共在边界控制是否覆盖 |
| `implementation_readiness` | schema、fixture、runner、dashboard 是否成熟 |
| `evaluation_readiness` | 长期指标、timeline、dashboard 是否成熟 |

## dashboard 状态颜色

| 状态 | 含义 |
|---|---|
| green | 当前窗口内通过 |
| yellow | warning 或 coverage 不完整 |
| red | high/critical failure |
| gray | 尚未实现或无数据 |
| blue | manual_review_required |

绿色表示对应工程检查通过；数字生命诞生由纵向生命证据、真实运行观测和阶段门共同推进。

## 下一层缺口

后续需要：

- dashboard 数据源 manifest。
- panel mock fixture。
- 指标计算脚本设计。
- 长期趋势样例。
- 与 runner report 的 JSON 输出对齐。
