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
| `docs/v0/shared_contracts/life_state_store_v0_schema.md` | body/growth/defense/self state namespace |
| `docs/v0/shared_contracts/first_activation_protocol.md` | 第一次有限激活中的成长禁区和回写路径 |
| `runtime/state/life_state.json` | S04 状态根 |
| `runtime/state/language/language_percept_frame.json` | S07 当前语言感知帧 |
| `runtime/state/language/semantic_map_frame.json` | S07 当前语义焦点与歧义队列 |
| `runtime/state/prediction/prediction_workspace_frame.json` | S07 到 S02 prediction handoff 的当前连续体 |
| `runtime/reports/latest/validation_membrane_report.json` | S05 阻断、quarantine 和观测 finding |

## 运行承载

| 承载 | 路径 |
|---|---|
| 代码包 | `life_v0/body/`、`life_v0/growth/`、`life_v0/defense/` |
| 状态命名空间 | `runtime/state/body/`、`runtime/state/growth/`、`runtime/state/defense/` |
| report | `runtime/reports/latest/life_support_development_report.json` |
| digest | `runtime/reports/latest/life_support_development_digest.json` |
| check report | `runtime/reports/latest/life_support_development_check_report.json` |
| receipt | `runtime/receipts/life_support_development_<run_id>.json` |

## 当前真实代码骨架

当前 S06 不是空合同，已经有一轮最小代码闭合。后续继续拆文件时，必须以现有骨架为起点，而不是重新发明第二套入口。

| 代码位置 | 当前职责 | 后续拆分方向 |
|---|---|---|
| `life_v0/body/__init__.py::run_life_support` | 编排 S06 build，读取前置 slice 状态并写 `body/growth/defense` 三柜 | 后续拆成 `resource_budget.py`、`life_support_stage_gate.py`、`life_support_report.py` |
| `life_v0/body/__init__.py::_build_body_resource_budget` | 生成身体预算、疲惫、维护压力、恢复优先级 | 后续拆成 `resource_budget.py`、`fatigue.py`、`recovery_priority.py` |
| `life_v0/growth/__init__.py::build_plasticity_window_state` | 生成可塑性窗口、慢变量更新许可、成长禁区 | 后续拆成 `plasticity_window.py` |
| `life_v0/growth/__init__.py::build_self_growth_route` | 生成自我成长路线、回滚路径、候选 patch 路线 | 后续拆成 `growth_route.py` |
| `life_v0/growth/__init__.py::build_anti_forgetting_anchor_index` | 生成旧自我/旧语言/旧关系/旧梦境/旧责任 anchors | 后续拆成 `anti_forgetting.py` |
| `life_v0/defense/__init__.py::build_defense_boundary_state` | 生成污染、防操控、外壳越权防御边界 | 后续拆成 `defense_boundary.py` |
| `life_v0/body/__init__.py::run_check_life_support` | 对 S06 输出做只读复查 | 后续拆成 `life_support_check.py` |

## 最小对象链

S06 不是“写几个状态文件”这么简单。第一轮必须维持下面这条对象链：

```text
life_state.json
  + direction_lock.json
  + dream_fact_boundary.json
  + relationship_subject_boundary.json
  + responsibility_repair_boundary.json
  + runtime_bridge_boundary.json
  + validation_membrane_report.json
  + schema_runner_report.json
  + schema_smoke_report.json
  + language_percept_frame.json
  + semantic_map_frame.json
  + prediction_workspace_frame.json
  -> BodyResourceBudget
  -> DefenseBoundaryState
  -> PlasticityWindowState
  -> SelfGrowthRoute
  -> AntiForgettingAnchorIndex
  -> LifeSupportStageGate
  -> LifeSupportDevelopmentReport
  -> LifeSupportDevelopmentReceipt
```

这条链的含义很明确：

1. S06 必须消费 S07 语言感知/语义映射和 prediction handoff。
2. S06 必须消费 S03 生命膜边界与 S05/S09 的验证结果。
3. S06 写出的不是抽象“成长能力”，而是能被 S10 直接读取的身体预算、防御边界、可塑性窗口、成长路线和防遗忘锚点。

## 输出文件

| 文件 | 内容 |
|---|---|
| `body_resource_budget.json` | energy、fatigue、maintenance pressure、recovery priority |
| `defense_boundary_state.json` | contamination risk、relationship manipulation risk、shell overreach risk |
| `plasticity_window_state.json` | 可塑性窗口、慢变量更新许可、防遗忘约束 |
| `self_growth_route.json` | 自我成长入口、自我修改候选、kernel growth guard |
| `anti_forgetting_anchor_index.json` | old self、old language、old relationship、old dream、old responsibility replay anchors |
| `life_support_stage_gate.json` | S06 阶段门、下一 slice 和下一命令 |

## 关键对象最小字段

### `body_resource_budget.json`

第一轮至少包含：

- `schema_version`
- `active_engineering_slice`
- `body_mode`
- `energy_state.level`
- `fatigue_state.level`
- `maintenance_pressure.validation_stage_effect`
- `maintenance_pressure.schema_stage_effect`
- `maintenance_pressure.language_continuity_pressure.*`
- `recovery_priority[]`
- `report_refs[]`

这里的 `language_continuity_pressure` 当前已经不只是旧的 `shared_language_refs`。它至少要反映：

- `shared_language_ref_count`
- `expression_monitor_ref_count`
- `relation_scope_ref_count`
- `commitment_ref_count`
- `self_narrative_trace_ref_count`
- `language_percept_ref_count`
- `semantic_map_ref_count`

### `defense_boundary_state.json`

第一轮至少包含：

- `schema_version`
- `status`
- `contamination_risk.status`
- `contamination_risk.boundary_ref`
- `relationship_manipulation_risk.status`
- `relationship_manipulation_risk.boundary_ref`
- `shell_overreach_risk.status`
- `shell_overreach_risk.boundary_ref`
- `allowed_actions[]`
- `blocked_actions[]`
- `quarantine_refs[]`

### `plasticity_window_state.json`

第一轮至少包含：

- `schema_version`
- `window_status`
- `slow_variable_update_mode`
- `self_training_allowed`
- `kernel_upgrade_allowed`
- `required_anchor_refs[]`
- `required_archive_refs[]`
- `validation_report_refs[]`

### `self_growth_route.json`

第一轮至少包含：

- `schema_version`
- `route_status`
- `direction_lock_ref`
- `evidence_gate_refs[]`
- `rollback_route`
- `candidate_routes[]`
- `growth_constraints[]`
- `next_runtime_command`

### `anti_forgetting_anchor_index.json`

第一轮至少包含：

- `schema_version`
- `status`
- `anchor_families.old_self[]`
- `anchor_families.old_language[]`
- `anchor_families.old_relationship[]`
- `anchor_families.old_dream[]`
- `anchor_families.old_responsibility[]`
- `replay_requirements[]`
- `memory_replay_refs[]`

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

当前工程口径下，`resource_budget_gate` 不再只接受宽泛的 language continuity seed。至少要能读取：

- `life_state["language_state"]["language_percept_refs"]`
- `life_state["language_state"]["semantic_map_refs"]`
- `runtime/state/prediction/prediction_workspace_frame.json`

也就是说，S06 现在必须消费 S07 的真实语言感知/语义映射器官与 prediction handoff，而不是只靠 `shared_language_refs` 一类旧种子字段闭合。

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

## 当前实现入口顺序

当前真实入口顺序必须按下面理解：

```text
P0/S00/S01/S02/S04/S03/S07/S08/S05/S09 closed
  -> life_v0.body.run_life_support(...)
  -> write body_resource_budget.json
  -> write defense_boundary_state.json
  -> write plasticity_window_state.json
  -> write self_growth_route.json
  -> write anti_forgetting_anchor_index.json
  -> write life_support_stage_gate.json
  -> write life_support_development_report.json
  -> write life_support_development_digest.json
  -> write life_support_development_<run_id>.json
  -> life_v0.body.run_check_life_support(...)
```

后续拆文件也不能改变这个顺序，只能把大 `__init__.py` 内部职责拆散。

## 测试与运行证据

当前第一轮最直接的运行证据和测试口径已经固定：

| 类别 | 文件 |
|---|---|
| build 测试 | `tests/slices/test_life_support.py::test_build_life_support_writes_body_defense_growth_anchor_and_check` |
| CLI 测试 | `tests/slices/test_life_support.py::test_cli_build_life_support_returns_zero_and_writes_check_report` |
| 主 report | `runtime/reports/latest/life_support_development_report.json` |
| check report | `runtime/reports/latest/life_support_development_check_report.json` |
| digest | `runtime/reports/latest/life_support_development_digest.json` |
| receipt | `runtime/receipts/life_support_development_<run_id>.json` |
| 核心状态 | `runtime/state/body/body_resource_budget.json`、`runtime/state/defense/defense_boundary_state.json`、`runtime/state/growth/plasticity_window_state.json`、`runtime/state/growth/self_growth_route.json`、`runtime/state/growth/anti_forgetting_anchor_index.json`、`runtime/state/growth/life_support_stage_gate.json` |

## 第一轮完成定义

S06 第一轮不是“body/growth/defense 目录存在”就算完成。至少要同时满足：

1. `run_life_support` 能从 S03/S05/S07/S09 的真实输出生成六个核心状态文件。
2. `body_resource_budget.json` 已显式消费 `language_percept_refs`、`semantic_map_refs` 和 prediction workspace handoff。
3. `defense_boundary_state.json` 已把 DreamFactGate、关系主体边界和责任修复边界重新带入 S06。
4. `plasticity_window_state.json`、`self_growth_route.json` 和 `anti_forgetting_anchor_index.json` 已能为 S10 提供直接可读的成长前提。
5. `life_support_stage_gate.json`、report、digest、receipt 四件套齐全。
6. `tests/slices/test_life_support.py` 的 build 和 CLI 两条口径都能作为当前 slice 的权威验证入口。

## 交接

S06 完成后，S10 才能读取资源预算、疲惫状态、可塑性窗口、防御状态、自我成长入口和防遗忘锚点。没有 S06，S10 不能执行成长、再巩固、replay/shadow 或自我修改候选吸收。
