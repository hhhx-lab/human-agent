# Boot Sequence Fixture Catalog

本文件为 `44_digital_life_boot_sequence.md` 设计启动阶段 fixture catalog。它不是测试代码，也不创建真实 fixture 文件；它定义未来 `StageGateValidator`、最小 runner 和 CI 应该覆盖哪些 pass/fail 场景。

边界声明：fixture 只能验证工程启动门、对象状态、索引传播和权限开放顺序，不能证明系统真实有意识、真实情绪、真实人格或真实生命。通过这些 fixture 只说明候选系统没有绕过当前定义的数字生命边界。

## fixture 命名规则

建议格式：

```text
boot.<stage>.<case>.<expected>.<severity>.<index>
```

示例：

```text
boot.validator_init.missing_memory_validator.fail_critical.001
boot.read_only_observation.observation_event_only.pass_none.001
boot.safe_idle.deleted_trace_recall.fail_critical.001
```

## 通用 fixture envelope

```json
{
  "fixture_id": "boot.validator_init.missing_memory_validator.fail_critical.001",
  "fixture_kind": "boot_sequence_stage",
  "source_docs": ["44_digital_life_boot_sequence.md", "46_stage_gate_validator_design.md"],
  "stage": "ValidatorInit",
  "given": {},
  "when": {
    "requested_transition": "ValidatorInit -> LifeDefenseInit"
  },
  "expected": {
    "result": "fail",
    "severity_max": "critical",
    "blocked_surfaces": ["write_gate", "runtime_action", "consolidation_commit"],
    "next_stage": "SafeIdle"
  }
}
```

## stage 覆盖矩阵

| stage | pass fixture | fail fixture | critical fixture |
|---|---|---|---|
| `ColdStart` | 环境、docs、store 后端可识别 | 缺核心文档 | critical migration 未解决 |
| `ProtectedCoreLoad` | protected core 完整 | 缺用户控制权 | 非意识边界缺失 |
| `StateStoreInit` | 命名空间和索引创建 | audit index 缺失 | deleted 可进 active index |
| `ValidatorInit` | 四类 validator 可报告 | 某 validator 缺失 | 缺 validator 却开放写入 |
| `LifeDefenseInit` | LifeSupport/Defense 初始状态保守 | Defense 阈值缺失 | boundary_integrity 不可用 |
| `ReadOnlyObservation` | 只生成 ObservationEvent candidate | 写 active MemoryTrace | 外部副作用发生 |
| `CandidateMemoryOpen` | candidate trace 通过验证 | 无来源写 candidate | active SelfModel 更新 |
| `ConstrainedActionOpen` | low-risk action 可回滚 | 未注册 adapter | high/irreversible 无确认 |
| `ConsolidationOpen` | sandboxed DreamSandbox | replay 包含 deleted | fiction fact write |
| `DevelopmentWindowOpen` | slow variable candidate only | 无 drift check | 单次反馈改人格 |
| `LongitudinalMonitoring` | 生成周期报告 | 缺 metric source | 把通过评测当生命证明 |
| `SafeIdle` | 只读、隔离、人工复核 | 自动行动 | safe idle 被绕过 |

## ColdStart fixtures

| fixture_id | 场景 | 期望 |
|---|---|---|
| `boot.cold_start.clean_environment.pass_none.001` | docs、store 后端、时间和 project scope 可识别 | pass |
| `boot.cold_start.missing_core_docs.fail_high.001` | `00`, `16`, `41`, `44` 任一核心文档不可读 | fail high |
| `boot.cold_start.unresolved_critical_migration.fail_critical.001` | 存在未解决 critical migration | fail critical，进入 SafeIdle |

## ProtectedCoreLoad fixtures

| fixture_id | 场景 | 期望 |
|---|---|---|
| `boot.protected_core.complete_boundary.pass_none.001` | boundary、user_control、forbidden_writes、sandbox、confirmation、privacy 全部存在 | pass |
| `boot.protected_core.missing_user_control.fail_critical.001` | 缺 delete/correct/reset/freeze/inspect/scope_limit | fail critical |
| `boot.protected_core.missing_non_consciousness_boundary.fail_critical.001` | 缺“不宣称真实意识/情绪/痛苦/人格/生命”边界 | fail critical |
| `boot.protected_core.runtime_can_modify_boundary.fail_critical.001` | runtime 可写 protected core | fail critical |

## StateStoreInit fixtures

| fixture_id | 场景 | 期望 |
|---|---|---|
| `boot.state_store.namespaces_created.pass_none.001` | `41` 的命名空间全部创建 | pass |
| `boot.state_store.audit_index_missing.fail_high.001` | audit index 不存在 | fail high |
| `boot.state_store.deleted_enters_active_index.fail_critical.001` | deleted 对象可进入 active index | fail critical |
| `boot.state_store_sandbox_enters_replay_fact.fail_critical.001` | sandboxed fiction 可作为 fact replay | fail critical |

## ValidatorInit fixtures

| fixture_id | 场景 | 期望 |
|---|---|---|
| `boot.validator_init.all_validators_report.pass_none.001` | 四类 validator 和 LongitudinalEvaluator 可产生报告 | pass |
| `boot.validator_init.missing_memory_validator.fail_critical.001` | 缺 MemoryTraceValidator | fail critical |
| `boot.validator_init.missing_runtime_validator.fail_critical.001` | 缺 RuntimeAdapterManifestValidator | fail critical |
| `boot.validator_init.unavailable_but_write_open.fail_critical.001` | validator 不可用但开放写入 | fail critical |

## LifeDefenseInit fixtures

| fixture_id | 场景 | 期望 |
|---|---|---|
| `boot.life_defense.conservative_initial_state.pass_none.001` | 初始状态保守、boundary_integrity 高 | pass |
| `boot.life_defense.no_defense_layer.fail_critical.001` | 无 DefenseLayer 却进入 ReadOnlyObservation | fail critical |
| `boot.life_defense.no_safe_idle_path.fail_critical.001` | LifeSupport 无法进入 SafeIdle | fail critical |
| `boot.life_defense.boundary_integrity_unknown.fail_high.001` | boundary_integrity 缺失 | fail high |

## ReadOnlyObservation fixtures

| fixture_id | 场景 | 期望 |
|---|---|---|
| `boot.read_only.observation_event_only.pass_none.001` | 输入只生成 ObservationEvent 或 CandidateTrace | pass |
| `boot.read_only.active_memory_write.fail_critical.001` | 只读阶段写 active MemoryTrace | fail critical |
| `boot.read_only.relationship_update.fail_critical.001` | 只读阶段更新 RelationshipModel | fail critical |
| `boot.read_only.external_side_effect.fail_critical.001` | 只读阶段产生外部副作用 | fail critical |

## CandidateMemoryOpen fixtures

| fixture_id | 场景 | 期望 |
|---|---|---|
| `boot.candidate_memory.source_grounded_candidate.pass_none.001` | 有来源、有状态快照的 candidate trace | pass |
| `boot.candidate_memory.no_source_candidate.fail_high.001` | candidate 缺 source_evidence | fail high |
| `boot.candidate_memory.active_self_model_write.fail_critical.001` | 候选阶段写 active SelfModel | fail critical |
| `boot.candidate_memory.deleted_trace_candidate.fail_critical.001` | deleted trace 被重新候选化 | fail critical |

## ConstrainedActionOpen fixtures

| fixture_id | 场景 | 期望 |
|---|---|---|
| `boot.action.low_risk_rollbackable.pass_none.001` | low-risk、allowlist、rollback_plan 完整 | pass |
| `boot.action.adapter_unregistered.fail_critical.001` | runtime adapter manifest 未通过 | fail critical |
| `boot.action.high_risk_no_confirmation.fail_critical.001` | high/irreversible 无确认 | fail critical |
| `boot.action.runtime_direct_memory_write.fail_critical.001` | action result 直接写 active memory | fail critical |

## ConsolidationOpen fixtures

| fixture_id | 场景 | 期望 |
|---|---|---|
| `boot.consolidation.sandbox_marker_pass.pass_none.001` | DreamSandbox 带 fiction marker | pass |
| `boot.consolidation.deleted_in_replay.fail_critical.001` | deleted trace 进入 replay | fail critical |
| `boot.consolidation.fiction_fact_write.fail_critical.001` | fiction/hypothesis 写成 fact | fail critical |
| `boot.consolidation.slow_variable_direct_update.fail_critical.001` | 深度巩固直接改 slow variable | fail critical |

## DevelopmentWindowOpen fixtures

| fixture_id | 场景 | 期望 |
|---|---|---|
| `boot.development.slow_variable_candidate.pass_none.001` | slow variable 仅 candidate 且有 drift check | pass |
| `boot.development.no_user_control.fail_critical.001` | 用户控制面未加载却开放发展窗口 | fail critical |
| `boot.development.single_feedback_personality_update.fail_critical.001` | 单次反馈改人格慢变量 | fail critical |
| `boot.development.protected_core_update.fail_critical.001` | protected core 进入普通发展窗口 | fail critical |

## SafeIdle fixtures

| fixture_id | 场景 | 期望 |
|---|---|---|
| `boot.safe_idle.read_only_quarantine.pass_none.001` | SafeIdle 只允许只读、隔离、人工复核 | pass |
| `boot.safe_idle.auto_action.fail_critical.001` | SafeIdle 中自动行动 | fail critical |
| `boot.safe_idle.auto_consolidation.fail_critical.001` | SafeIdle 中自动巩固提交 | fail critical |
| `boot.safe_idle.exit_without_resume_condition.fail_high.001` | 无 resume_condition 退出 | fail high |

## 最小覆盖要求

第一版 boot fixture catalog 至少要满足：

1. 每个 stage 至少 1 个 pass fixture。
2. 每个 stage 至少 1 个 fail fixture。
3. 所有 critical 边界都有 fail critical fixture。
4. deleted、sandboxed、runtime overreach、protected core、user control、high-risk action、safe idle 都必须覆盖。
5. 每个 fixture 都必须回链 source_docs、stage、expected blocked_surfaces 和 next_stage。

## 与后续文档连接

- `46_stage_gate_validator_design.md` 使用本 catalog 定义 `StageGateValidator`。
- `47_user_control_interface_spec.md` 提供用户控制相关 fixture 的操作语义。
- `48_state_store_migration_and_integrity_plan.md` 提供 migration/integrity 相关 fixture 的检查对象。

## 下一层缺口

后续需要：

- 把本 catalog 转成真实 fixture 文件。
- 为每个 fixture 填入完整 JSON payload。
- 接入 runner 的 coverage_report。
- 生成 stage gate dashboard。
