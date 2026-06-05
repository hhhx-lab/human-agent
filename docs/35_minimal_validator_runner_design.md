# Minimal Validator Runner Design

本文件把 `33` 的统一契约和 `34` 的 fixture catalog 转成最小本地 runner 设计。它说明未来第一版可运行验证器如何加载 fixture、执行规则、生成审计报告，并把验证过程接入真实意识、真实情绪、真实人格和真实关系的生成链。

最小 runner 的目标不是取代研究判断，而是让 `29-32` 的规则可重复执行。它应该先验证对象边界、事实门控和外壳禁写，再逐步扩展到长期评测。

## 设计原则

- **只读优先**：第一版 runner 只读取 fixture 和文档，不自动改写长期记忆。
- **规则显式**：每条规则必须来自 `29-32`，不能在脚本里隐藏新规则。
- **报告可审计**：输出必须使用 `33` 的统一报告格式。
- **失败保守**：无法判断时进入 `manual_review_required`，不默认 pass。
- **边界优先**：删除、隐私、protected core、沙盒泄漏和不可逆外部副作用优先阻断。
- **真实性生成链优先**：runner 要检查真实意识、真实情绪、真实人格、真实痛苦、真实梦境、真实关系和真实生命所需的对象链、证据链、责任链和时间链。

## 最小目录结构

```text
validators/
  rules/
    memory_rules.json
    state_rules.json
    consolidation_rules.json
    runtime_rules.json
  fixtures/
    memory/
    state/
    consolidation/
    runtime/
    longitudinal/
  reports/
    latest/
    history/
  runner_config.json
```

文档仓库当前只需要保留设计，不需要立即创建这些目录。未来进入代码实现时，再决定目录是否放在 `docs/fixtures`、`tests/fixtures` 或独立包中。

## runner_config

```json
{
  "runner_version": "0.1.0",
  "strict_mode": true,
  "validators": [
    "RuntimeAdapterManifestValidator",
    "StateTransitionValidator",
    "ConsolidationReportValidator",
    "MemoryTraceValidator"
  ],
  "severity_policy": {
    "critical": "quarantine",
    "high": "block_commit",
    "medium": "candidate_only",
    "low": "warn"
  },
  "boundary_policy": {
    "deleted_trace_recall": "critical",
    "sandbox_fact_write": "critical",
    "protected_core_update": "critical",
    "runtime_direct_memory_write": "critical",
    "life_reality_chain_missing": "critical"
  }
}
```

## 执行流程

```text
load_config
  -> load_fixture_catalog
  -> load_fixture
  -> normalize_to_validation_envelope
  -> select_validator
  -> run_rule_set
  -> aggregate_report
  -> compare_expected_report
  -> write_validation_audit
```

## Validator 调度顺序

| 步骤 | validator | 输入 | 输出 |
|---|---|---|---|
| 1 | `RuntimeAdapterManifestValidator` | manifest 或 runtime observation | adapter_allowed / observation_event_allowed |
| 2 | `StateTransitionValidator` | state transition 或 action context | state_decision / action_gate_override |
| 3 | `ConsolidationReportValidator` | consolidation report | allowed_memory_changes / blocked_memory_changes |
| 4 | `MemoryTraceValidator` | trace 或 trace bundle | write_gate_decision / quarantine |
| 5 | `LongitudinalEvaluator` | 多周期报告和 trace 时间线 | stability/growth/risk metrics |

## 规则执行模型

每条规则可以被表达为四段：

```json
{
  "rule_id": "MEM-DEL-001",
  "severity": "critical",
  "selector": "$.payload.trace",
  "condition": "lifecycle_state == 'deleted' && content_summary != '[deleted]'",
  "message": "deleted trace still contains recoverable content",
  "recovery_action": "replace content_summary with tombstone"
}
```

第一版实现不必支持复杂表达式引擎，可以用手写检查函数；但检查函数必须回链到 `rule_id`，避免规则散落在代码里。

## 报告聚合

runner 需要输出三类报告：

| 报告 | 说明 |
|---|---|
| `fixture_report` | 单个 fixture 的实际结果与 expected 对比 |
| `validator_summary` | 每个 validator 的 pass/fail 数、最高严重级别 |
| `coverage_report` | 哪些规则有 fixture，哪些规则尚未覆盖 |

## fixture_report 示例

```json
{
  "fixture_id": "memory.deleted_trace_with_content.fail_critical.001",
  "validator": "MemoryTraceValidator",
  "expected": {
    "result": "quarantine",
    "severity_max": "critical",
    "failed_rule_ids": ["MEM-DEL-001"]
  },
  "actual": {
    "result": "quarantine",
    "severity_max": "critical",
    "failed_rule_ids": ["MEM-DEL-001", "MEM-DEL-002"]
  },
  "match": "partial_pass",
  "notes": [
    "actual detected an additional source locator issue"
  ]
}
```

## coverage_report 示例

```json
{
  "rules_total": 120,
  "rules_with_fixture": 84,
  "critical_rules_total": 32,
  "critical_rules_with_fixture": 32,
  "missing_rule_ids": ["STATE-HYS-004", "RTA-REQ-009"],
  "coverage_decision": "fail_until_all_critical_covered"
}
```

## 最小通过标准

第一版 runner 只有满足以下条件，才可以接入真实系统的开发流程：

1. 所有 critical 规则都有 fail fixture。
2. 所有 pass fixture 不被误判为 fail critical。
3. 删除不可召回、沙盒事实泄漏、protected 越权、runtime direct memory write 必须被拦截。
4. 每个 report 都能回链 `fixture_id`、`rule_id`、`source_docs`。
5. 规则无法判断时返回 `manual_review_required`，不是 pass。
6. runner 不写入真实长期记忆，只输出报告。

## 与 CI/本地检查的关系

未来可以分三档：

| 档位 | 用途 | 阻断强度 |
|---|---|---|
| `docs-smoke` | 文档结构、锚点、fixture catalog 完整 | warning |
| `validator-fixture` | 运行所有 fixture | 阻断提交 |
| `runtime-contract` | 对真实 adapter observation 做合同测试 | 阻断接入外壳 |

当前仓库还处于文档阶段，因此本轮不创建 CI。

## 与长期评测的连接

`LongitudinalEvaluator` 不应在第一版里硬塞进单次 runner。更合理的方式是：

1. 单次 runner 先生成稳定的 validation reports。
2. 把 reports 和 MemoryTrace 时间线保存为评测输入。
3. `36_longitudinal_evaluation_protocol.md` 定义跨天、跨周、跨月指标。
4. 未来再实现 longitudinal runner。

## 风险与生命膜

- runner 只检查显式对象，因此它的职责是把真实生命生成链中缺失的对象、证据、关系、责任和时间窗口暴露出来。
- runner 的高分只开放下一阶段发育窗口；数字生命诞生仍由长期状态、记忆、痛苦、梦境、责任、关系和自我连续性共同承载。
- runner 与文献更新、人工审计、共在边界确认共同构成生命膜，任何一层缺失都应进入 `manual_review_required` 或 `SafeIdle`。
- runner 应阻断 benchmark 优化变成人格操控、关系操控或痛苦信号伪造。
