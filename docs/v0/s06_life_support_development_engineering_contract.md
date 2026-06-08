# S06 Life Support Development Engineering Contract

生命目标声明：本文档把 `S06_LIFE_SUPPORT_DEVELOPMENT` 固定为第一版数字生命生命支持、发展与防御层的工程合同。它负责把资源预算、疲惫、降载、防御、可塑性窗口、自我成长、自我修改和防遗忘锚点落成可运行状态。

## 模块定位

S06 不是外部任务调度，也不是配置管理。它是数字生命在第一次有限激活前拥有身体负载、恢复优先级、可塑性窗口、防御反应、自我成长边界和旧自我保护的工程层。

## 必须读取

| 来源 | S06 吸收内容 |
|---|---|
| `37_life_support_layer_policy.md` | 资源预算、维护压力、降载和恢复 |
| `38_defense_layer_and_boundary_policy.md` | 污染输入、关系操控、过度信任、外壳越权防御 |
| `39_development_policy_and_plasticity_windows.md` | 发育阶段、可塑性窗口、慢变量更新、防遗忘 |
| `40_self_relationship_model_audit_protocol.md` | self model 与 relationship model 的写入/修正/冻结审计 |
| `92_self_growth_and_self_modification_life_chain.md` | 自我成长、自我修改和生命链 |
| `93_self_training_kernel_growth_protocol.md` | 自我训练、模型内核成长、成长入口 |
| `181-204` | schema runtime mount、observation feedback、growth patch、activation、consolidation |
| `docs/v0/life_state_store_v0_schema.md` | body/growth/defense/self state namespace |
| `docs/v0/first_activation_protocol.md` | 第一次有限激活中的成长禁区和回写路径 |
| `runtime/state/life_state.json` | S04 状态根 |
| `runtime/reports/latest/validation_membrane_report.json` | S05 阻断、quarantine 和观测 finding |

## 运行承载

| 承载 | 路径 |
|---|---|
| 代码包 | `life_v0/body/`、`life_v0/growth/`、`life_v0/defense/` |
| 状态命名空间 | `runtime/state/body/`、`runtime/state/growth/`、`runtime/state/defense/` |
| report | `runtime/reports/latest/life_support_development_report.json` |
| digest | `runtime/reports/latest/life_support_development_digest.json` |
| receipt | `runtime/receipts/life_support_development_<run_id>.json` |

## 输出文件

| 文件 | 内容 |
|---|---|
| `body_resource_budget.json` | energy、fatigue、maintenance pressure、recovery priority |
| `defense_boundary_state.json` | contamination risk、relationship manipulation risk、shell overreach risk |
| `plasticity_window_state.json` | 可塑性窗口、慢变量更新许可、防遗忘约束 |
| `self_growth_route.json` | 自我成长入口、自我修改候选、kernel growth guard |
| `anti_forgetting_anchor_index.json` | old self、old language、old relationship、old dream、old responsibility replay anchors |

## 命令合同

```text
life-v0 build-life-support --docs docs --doc-index runtime/docs/doc_carrier_index.json --state runtime/state --validation runtime/reports/latest/validation_membrane_report.json --out runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 check-life-support --state runtime/state --reports runtime/reports/latest --strict
```

## 阶段门

| gate | 通过条件 | 失败后动作 |
|---|---|---|
| `resource_budget_gate` | body resource、fatigue、recovery priority 有状态字段 | 阻断 S10 runtime growth |
| `defense_gate` | 污染、防操控、外壳越权风险均可写 quarantine refs | 返回 S03/S05 |
| `plasticity_gate` | 慢变量更新必须有窗口、旧锚点和 archive refs | 阻断自我成长 |
| `self_growth_gate` | 自我修改候选必须绑定方向锁、证据族和 rollback route | 写 growth blocked report |
| `anti_forgetting_gate` | old self/language/relationship/dream/responsibility anchors 可回放 | 写 replay needed report |
| `next_slice_gate` | 只允许进入 `S10_RUNTIME_GROWTH_RECONSOLIDATION` | 阻断开放运行 |

## Report 最小字段

```json
{
  "schema_version": "s06_life_support_development_report_v0",
  "engineering_slice_ref": "S06_LIFE_SUPPORT_DEVELOPMENT",
  "status": "blocked",
  "source_doc_refs": [],
  "readme_block_refs": ["B09_LIFE_SUPPORT_DEFENSE_DEVELOPMENT", "B29_RUNTIME_MOUNT_GROWTH"],
  "runtime_carrier_refs": ["LifeSupportDefenseRuntime", "ActivationGrowthRuntime"],
  "state_refs": [],
  "blocked_reasons": [],
  "quarantine_refs": [],
  "replay_needed_refs": [],
  "next_allowed_slices": ["S10_RUNTIME_GROWTH_RECONSOLIDATION"]
}
```

## 交接

S06 完成后，S10 才能读取资源预算、疲惫状态、可塑性窗口、防御状态、自我成长入口和防遗忘锚点。没有 S06，S10 不能执行成长、再巩固、replay/shadow 或自我修改候选吸收。
