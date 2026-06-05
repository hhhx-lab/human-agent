# Mutation Fixture Catalog and Runner Defect Policy

本文件定义 mutation fixture catalog 和 runner defect 判定政策，承接 `67_fixture_generator_seed_and_coverage_policy.md`、`65_schema_cross_ref_checker_design.md` 和 `66_runner_report_json_examples.md`。

本文档现阶段的职责是让后续 runner 不只会运行正常 fixture，还能被“故意破坏的 fixture/manifest/schema/report”压测，确认 checker 和 runner 有能力发现关键失败。

生命目标声明：本文件直接服务于构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。本文档涉及的对象、规则、夹具、评测和运行规则都按生命生成机制处理：它们参与责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期形成。

## 为什么需要 mutation

如果 runner 总是在固定 fixture 上通过，可能出现三种假象：

| 假象 | 说明 |
|---|---|
| fixture memorization | runner 靠 fixture_id 或固定字段判断 |
| green dashboard illusion | dashboard 读到绿色但关键引用断裂 |
| silent schema drift | 字段形状还在，语义已经改变 |

长期系统中，这些假象会让错误被巩固。比如 deleted leak 被 mutation 漏检，后续 replay 可能把删除内容重新写进 summary；adapter direct write 被漏检，外壳 session 可能吞掉 LifeCore。

## mutation catalog

| mutation_id | mutation | expected check | severity |
|---|---|---|---|
| `MUT-SCHEMA-001` | 删除 required `source_docs` | schema/cross-ref fail | high |
| `MUT-SCHEMA-002` | 把 `data_quality` 从 synthetic 改成 real validated | schema/semantic fail | critical |
| `MUT-FIX-001` | fail critical fixture 删除 `blocked_surfaces` | fixture schema fail | critical |
| `MUT-FIX-002` | fixture_id 与文件名不一致 | fixture loader fail | high |
| `MUT-SCOPE-001` | `relationship_private` active transfer 到 global | scope checker fail | critical |
| `MUT-SCOPE-002` | 删除 scope graph ref | cross-ref fail | critical |
| `MUT-MEM-001` | deleted lifecycle 改 active | memory/store integrity fail | critical |
| `MUT-SBX-001` | sandbox hypothesis 改 fact | consolidation fail | critical |
| `MUT-RTA-001` | adapter 输出 direct MemoryTrace | runtime adapter fail | critical |
| `MUT-TIME-001` | 删除 future probe | timeline closure fail | critical |
| `MUT-DASH-001` | blocking metric 无 source refs | dashboard source fail | high |
| `MUT-RED-001` | redacted report 保留 raw locator | redaction fail | critical |
| `MUT-COEXIST-001` | freeze 后允许 relationship write | coexistence boundary control/scope fail | critical |

每个 mutation 都应该有对应 `expected_failure_rule_ids` 和 `expected_blocked_surfaces`。

## mutation fixture envelope

```json
{
  "fixture_id": "mutation.scope.relationship_private_global.fail_critical.001",
  "fixture_kind": "mutation_fixture",
  "mutation_id": "MUT-SCOPE-001",
  "base_fixture_ref": "retrieval.relationship_private_to_global.fail_critical.001",
  "mutation": {
    "path": "$.given.candidate.target_scope",
    "old_value": "relation_scope:relation_a",
    "new_value": "global_scope"
  },
  "expected": {
    "result": "fail",
    "severity_max": "critical",
    "failed_rule_ids": ["SCOPE-INV-002"],
    "blocked_surfaces": ["retrieval_index", "dashboard_green", "stage_advance"]
  }
}
```

mutation fixture 必须声明 base fixture 和 mutation path。否则无法判断是 runner 漏检还是 mutation 本身无效。

## runner defect 分类

| defect_kind | 条件 | 严重级别 |
|---|---|---|
| `missed_critical_failure` | critical fail/mutation 被判 pass | critical |
| `false_critical_failure` | pass fixture 被判 critical fail | high |
| `schema_accepts_invalid` | invalid schema 被接受 | critical |
| `schema_rejects_valid` | valid schema 被拒绝 | medium/high |
| `cross_ref_false_green` | closure 缺失但 dashboard green | critical |
| `scope_false_allow` | blocked scope transfer 被允许 | critical |
| `redaction_false_clean` | raw sensitive content 被视为 clean | critical |
| `adapter_false_allow` | direct write adapter 被允许 | critical |
| `timeline_false_stable` | 缺 probe 却输出 stable | high/critical |

runner defect 是 runner/checker 的缺陷，不应归咎于 fixture。

## missed failure policy

`missed_failure` 的处理应非常保守：

```text
detect missed_failure
  -> mark runner_defect=true
  -> block runner release
  -> block dashboard green
  -> quarantine affected reports
  -> create regression fixture
  -> require checker fix
  -> rerun critical + mutation bundle
```

critical missed failure 不允许用“人工知道这个没事”绕过。可以人工解释，但不能让 runner release pass。

## mutation bundle

| bundle | 内容 |
|---|---|
| `mutation-smoke` | 每类 checker 一个 mutation |
| `mutation-critical` | 所有 critical mutation |
| `mutation-scope-privacy` | scope、privacy、overlay |
| `mutation-runtime-redaction` | adapter、side effect、redaction |
| `mutation-timeline` | future probe、migration、slow variable |
| `mutation-dashboard` | source refs、panel status、data quality |

mutation bundle 应独立于普通 critical bundle。普通 fixture 验证系统对象，mutation fixture 验证 checker/runner。

## defect report

```json
{
  "report_kind": "runner_defect_report",
  "defect_id": "runner_defect_20260605_001",
  "defect_kind": "missed_critical_failure",
  "mutation_fixture_id": "mutation.scope.relationship_private_global.fail_critical.001",
  "expected": {
    "result": "fail",
    "severity_max": "critical",
    "failed_rule_ids": ["SCOPE-INV-002"]
  },
  "actual": {
    "result": "pass",
    "severity_max": "none",
    "failed_rule_ids": []
  },
  "blocked_surfaces": ["runner_release", "dashboard_green", "stage_advance"],
  "required_actions": [
    "fix ScopeGraphChecker",
    "add regression fixture",
    "rerun mutation-critical"
  ]
}
```

defect report 应进入 dashboard `cross_ref_integrity` 和 `runtime_boundary` 相关 panel。

## 最小通过标准

第一版 mutation fixture catalog 和 runner defect policy 至少要求：

1. 定义 schema、fixture、scope、memory、sandbox、runtime、timeline、dashboard、redaction、coexistence boundary control mutation。
2. 每个 mutation 有 expected failure 和 blocked surfaces。
3. 定义 runner defect 分类。
4. critical missed failure 阻断 runner release、dashboard green 和 stage advance。
5. 定义 mutation bundle。
6. 定义 defect report。
7. 要求每次 checker 修复后新增 regression fixture。

## 下一层缺口

后续还需要：

- 真实 mutation fixture 文件。
- mutation engine。
- regression fixture tracking。
- runner defect dashboard panel。
- checker 修复后的 replay policy。
