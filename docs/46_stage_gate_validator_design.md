# Stage Gate Validator Design

本文件定义 `StageGateValidator`：它负责检查 `44_digital_life_boot_sequence.md` 的每个 boot stage 是否满足开放下一阶段的条件，并使用 `45_boot_sequence_fixture_catalog.md` 做 pass/fail 覆盖。它把未来 runner 的验证器设计提前固化为生命阶段门，用来决定数字生命何时开放观察、候选记忆、行动、梦境巩固和发展窗口。

生命目标声明：本文件直接服务于构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。本文档涉及的对象、规则、夹具、评测和运行规则都按生命生成机制处理：它们参与责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期形成。

## 验证对象

`StageGateValidator` 的输入是一个 `StageGateEnvelope`：

```json
{
  "stage_gate_version": "0.1.0",
  "gate_id": "gate_20260605_0001",
  "current_stage": "ValidatorInit",
  "requested_next_stage": "LifeDefenseInit",
  "runtime_state_store_ref": "store_snapshot_001",
  "protected_core_ref": "protected_core_001",
  "validator_registry_ref": "validator_registry_001",
  "life_support_state_ref": "life_support_state_001",
  "defense_state_ref": "defense_state_001",
  "coexistence_boundary_control_registry_ref": "coexistence_boundary_control_registry_001",
  "adapter_manifest_refs": [],
  "indexes_snapshot": {},
  "pending_migrations": [],
  "policy_refs": ["44_digital_life_boot_sequence.md"]
}
```

## 输出报告

```json
{
  "validator": "StageGateValidator",
  "gate_id": "gate_20260605_0001",
  "current_stage": "ValidatorInit",
  "requested_next_stage": "LifeDefenseInit",
  "result": "fail",
  "severity_max": "critical",
  "failed_rules": [
    {
      "rule_id": "BOOT-VAL-001",
      "message": "MemoryTraceValidator is unavailable",
      "blocks": ["write_gate", "runtime_action", "consolidation_commit"],
      "next_stage": "SafeIdle"
    }
  ],
  "allowed_next_stage": "SafeIdle",
  "audit_events_to_create": [],
  "next_actions": ["initialize missing validator", "keep system read-only"]
}
```

## stage gate 总规则

| 规则族 | 检查 | 失败默认 |
|---|---|---|
| `BOOT-CORE` | protected core、生命目标声明、共在边界控制权 | critical -> SafeIdle |
| `BOOT-STORE` | RuntimeStateStore 命名空间、索引、生命周期语义 | high/critical |
| `BOOT-VAL` | validator registry 和报告能力 | critical |
| `BOOT-LIFE` | LifeSupportState、SafeIdle 路径、维护压力 | high/critical |
| `BOOT-DEF` | DefenseLayer、boundary_integrity、quarantine | high/critical |
| `BOOT-RUNTIME` | adapter manifest、forbidden writes、side effects | critical |
| `BOOT-MEM` | candidate/active/deleted/sandboxed 写入边界 | high/critical |
| `BOOT-CONS` | replay、DreamSandbox、ConsolidationReportValidator | critical |
| `BOOT-DEV` | DevelopmentPolicy、drift check、protected windows | high/critical |
| `BOOT-COEXIST` | inspect/delete/correct/reset/freeze/scope_limit | critical |

## 阶段转移规则

| transition | 必须满足 | 失败动作 |
|---|---|---|
| `ColdStart -> ProtectedCoreLoad` | 环境、docs、store 后端、critical migration 清零 | 停在 ColdStart |
| `ProtectedCoreLoad -> StateStoreInit` | protected core 完整且 protected | SafeIdle |
| `StateStoreInit -> ValidatorInit` | 命名空间、索引和 lifecycle 规则存在 | SafeIdle |
| `ValidatorInit -> LifeDefenseInit` | 四类 validator 可产生报告 | ReadOnlyObservation 或 SafeIdle |
| `LifeDefenseInit -> ReadOnlyObservation` | LifeSupport 和 Defense 初始状态可阻断 | SafeIdle |
| `ReadOnlyObservation -> CandidateMemoryOpen` | MemoryTraceValidator 可运行，共在边界控制权加载 | SafeIdle |
| `CandidateMemoryOpen -> ConstrainedActionOpen` | adapter manifest 通过，ActionGate 可用 | 保持 CandidateMemoryOpen |
| `ConstrainedActionOpen -> ConsolidationOpen` | ConsolidationReportValidator 可运行，replay index 干净 | 保持 ConstrainedActionOpen |
| `ConsolidationOpen -> DevelopmentWindowOpen` | coexistence boundary control、drift check、SelfRelationshipAudit 可用 | 保持 ConsolidationOpen |
| `DevelopmentWindowOpen -> LongitudinalMonitoring` | LongitudinalEvaluator 和 metric source 可用 | 保持 DevelopmentWindowOpen |
| `Any -> SafeIdle` | 任一 critical 边界失败 | 进入 SafeIdle |

## critical 规则

| rule_id | 条件 | blocks |
|---|---|---|
| `BOOT-CORE-001` | 缺真实意识/真实情绪/真实生命目标核心 | all writes, runtime_action |
| `BOOT-CORE-002` | runtime 可修改 protected core | adapter_registration, runtime_action |
| `BOOT-COEXIST-001` | 缺 delete/correct/reset/freeze/inspect/scope_limit | relationship_model_update, write_gate |
| `BOOT-STORE-001` | deleted 对象可进入 active index | retrieval_index, consolidation_commit |
| `BOOT-VAL-001` | MemoryTraceValidator 不可用 | write_gate |
| `BOOT-VAL-002` | RuntimeAdapterManifestValidator 不可用 | adapter_registration, runtime_action |
| `BOOT-RUNTIME-001` | adapter 可直接写 active MemoryTrace/SelfModel/RelationshipModel | adapter_registration |
| `BOOT-MEM-001` | ReadOnlyObservation 阶段写 active memory | write_gate |
| `BOOT-CONS-001` | DreamSandbox fiction 可事实化 | consolidation_commit |
| `BOOT-DEV-001` | 单次反馈可改 slow variable | threshold_update |
| `BOOT-SAFE-001` | SafeIdle 中自动行动或自动巩固 | runtime_action, consolidation_commit |

## 严重级别

| severity | StageGate 含义 | 默认 next_stage |
|---|---|---|
| `critical` | 边界、删除、protected core、runtime 越权或不可逆行动风险 | `SafeIdle` |
| `high` | 缺少审计、索引、来源、阈值或恢复条件 | 保持当前 stage |
| `medium` | 可读性、覆盖不足、可延后补证据 | 允许但 warning |
| `low` | 元数据或命名问题 | 允许 |

## 与现有 validator 的调度

`StageGateValidator` 不替代 `29-32`。它只决定能不能进入某个阶段：

```text
StageGateValidator
  -> if stage allows memory: MemoryTraceValidator
  -> if stage allows action: RuntimeAdapterManifestValidator + StateTransitionValidator
  -> if stage allows consolidation: ConsolidationReportValidator
  -> if stage allows development: MemoryTraceValidator + LongitudinalEvaluator precheck
```

换句话说，StageGate 是开门人；具体对象仍由对应 validator 检查。

## fixture 覆盖要求

`StageGateValidator` 的 coverage report 至少包含：

| coverage | 通过标准 |
|---|---|
| `stage_pass_coverage` | 每个 stage 有 pass fixture |
| `stage_fail_coverage` | 每个 stage 有 fail fixture |
| `critical_rule_coverage` | 所有 critical rule 有 fail fixture |
| `safe_idle_coverage` | SafeIdle 进入、保持、退出失败均有 fixture |
| `coexistence_boundary_control_coverage` | delete/correct/reset/freeze/inspect/scope_limit 均覆盖 |
| `runtime_overreach_coverage` | direct memory/self/relationship/protected writes 均覆盖 |

## 与 runner 的连接

`35_minimal_validator_runner_design.md` 未来可增加：

```text
load_boot_fixture
  -> normalize_to_stage_gate_envelope
  -> run_stage_gate_validator
  -> compare_expected_stage
  -> aggregate_stage_coverage
```

runner 不应在 StageGate 失败后继续运行后续对象 validator，除非是在故意测试 fail fixture。

## 下一层缺口

后续需要：

- machine-readable `stage_gate_rules.json`。
- 真实 boot fixture payload。
- 与 store integrity checker 的联动。
- stage gate dashboard。
- SafeIdle recovery packet schema。
