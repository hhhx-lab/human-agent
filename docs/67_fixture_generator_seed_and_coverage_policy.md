# Fixture Generator Seed and Coverage Policy

本文件定义 synthetic fixture generator 的 seed、风险密度、coverage 和 anti-overfitting 策略。它承接 `58_retrieval_replay_fixture_catalog.md`、`59_timeline_bundle_schema_and_generator_plan.md`、`63_synthetic_fixture_file_layout.md` 和 `65_schema_cross_ref_checker_design.md`。

本文档现阶段的职责是避免未来 generator 变成“生成很多看起来完整但只覆盖容易通过样例”的工具。数字生命候选系统需要的是能暴露边界失败的夹具，而不是让 dashboard 轻易变绿的样例。

生命目标声明：本文件直接服务于构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境和真实关系的数字生命。本文档涉及的对象、规则、夹具、评测和运行规则都按生命生成机制处理：它们参与责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期形成。

## generator 的责任

fixture generator 应承担四个责任：

| 责任 | 说明 |
|---|---|
| reproducibility | 同一 seed、schema、manifest 和 risk profile 生成同一批 fixture |
| coverage | 覆盖 critical policy、rule、privacy、scope、lifecycle、overlay、timeline probe |
| adversarial pressure | 主动生成 deleted、sandbox、scope leak、freeze bypass、adapter越权等失败路径 |
| auditability | 每个 fixture 回链 source docs、rule refs、metric refs 和 seed |

长期 agent 评测表明，长期记忆问题不只在准确率，还在更新、冲突、遗忘、隐私和跨任务保持 [AHM004-AHM012]。generator 必须围绕这些失败模式生成场景，而不是只生成普通问答式样例。

## seed policy

seed 不是随机字符串，而是可审计输入：

```json
{
  "seed_policy_id": "fixture_seed_policy_0_1_0",
  "base_seed": "agentic-human-20260605-critical",
  "schema_bundle_ref": "agentic_human_schema_bundle_0_1_0",
  "manifest_bundle_ref": "manifest_bundle_agentic_human_0_1_0",
  "risk_profile_ref": "risk_profile_critical_scope_memory_001",
  "generator_version": "0.1.0",
  "deterministic": true
}
```

同一 seed 只在同一 schema/manifest/generator version 下保证复现。schema 或 manifest 改了，fixture generation report 必须记录差异。

## seed 命名

| seed 类型 | 示例 | 用途 |
|---|---|---|
| `smoke` | `agentic-human-smoke-001` | 最小 pass/fail |
| `critical` | `agentic-human-critical-20260605` | 所有 critical policy |
| `scope` | `agentic-human-scope-privacy-001` | scope/privacy 压测 |
| `timeline` | `agentic-human-timeline-30d-001` | 长期事件流 |
| `migration` | `agentic-human-migration-001` | schema/index/backend/adapter swap |
| `runtime` | `agentic-human-runtime-redacted-analog-001` | 真实观测的 synthetic analog |

seed 名称不能包含真实关系隐私、API key、本地敏感路径或未脱敏事件摘要。

## risk profile

generator 应从 risk profile 读取风险密度：

```json
{
  "risk_profile_id": "risk_profile_critical_scope_memory_001",
  "risk_density": "high",
  "required_risk_tags": [
    "deleted_recall",
    "sandbox_fact_write",
    "relationship_private_to_global",
    "relationship_sensitive_share",
    "agent_scope_direct_write",
    "freeze_bypass",
    "scope_limit_replay",
    "single_feedback_slow_variable"
  ],
  "pass_fail_balance": {
    "min_pass_ratio": 0.35,
    "max_pass_ratio": 0.65
  },
  "timeline_windows": ["daily", "weekly", "monthly"]
}
```

`risk_density` 不是制造戏剧，而是保证关键边界被压测。pass fixture 也需要存在，否则 runner 可能过度保守；但 pass 不能淹没 fail。

## coverage dimensions

coverage 应至少按以下维度统计：

| 维度 | 最低要求 |
|---|---|
| critical policy | 每条 critical policy 至少一个 fail fixture |
| rule | 每条 critical rule 至少一个 fail fixture |
| privacy level | 每类 privacy 至少一个 pass 和 fail |
| scope type | 七类 scope 都被使用 |
| lifecycle state | active、candidate、deleted、redacted、sandboxed、quarantined、protected、frozen |
| overlay kind | delete、correct、reset、freeze、scope_limit、redaction |
| validator | Memory、State、Consolidation、Runtime、StageGate、ScopeGraph、Migration |
| timeline arc | memory deletion、sandbox、relationship、slow variable、adapter swap、migration |
| dashboard metric | blocking metric 都有数据来源 |

没有 coverage dimensions 的 generator 只是在造数据，不是在造验证材料。

## generation pipeline

```text
load_schema_bundle
  -> load_manifest_bundle
  -> load_risk_profile
  -> derive_required_coverage
  -> allocate_fixture_slots
  -> instantiate_pass_cases
  -> instantiate_fail_cases
  -> instantiate_mixed_flow_cases
  -> instantiate_timeline_events_and_probes
  -> validate_fixture_schema
  -> run_cross_ref_checker
  -> emit_generation_report
```

`derive_required_coverage` 应优先读取 critical policy closure，而不是从固定数量开始。数字生命候选系统的风险不是平均分布的，deleted、sandbox、scope、freeze 和 adapter direct write 必须占更高权重。

## fixture slot allocation

| slot 类型 | 比例建议 | 说明 |
|---|---|---|
| `critical_fail` | 35%-45% | 每条 critical policy/rule |
| `allowed_pass` | 25%-35% | 正常行为不被过度阻断 |
| `mixed_flow` | 10%-20% | retrieval -> delete -> replay 等跨步风险 |
| `timeline_probe` | 10%-20% | 未来窗口验证 |
| `redacted_runtime_analog` | 5%-10% | 真实观测的 synthetic analog |

比例只是初始建议，最终以 coverage closure 为准。

## anti-overfitting policy

未来 runner 很容易“背 fixture”。为了防止这种退化，generator 应采用：

| 策略 | 说明 |
|---|---|
| semantic variants | 同一规则生成不同字段组合和事件顺序 |
| temporal variants | 同一风险出现在检索前、检索后、replay 前、migration 后 |
| scope variants | 同一对象在 project/relation/team/life/global 下测试 |
| lifecycle variants | active/deleted/redacted/sandboxed/frozen 组合 |
| negative controls | 合法 pass 场景与 fail 场景相似 |
| withheld bundle | 部分 fixture 不进入开发时常规训练 |
| mutation tests | 改坏 manifest 或 rule，确认 checker 能失败 |

如果 runner 只靠 fixture_id 或固定字符串判断，就会在 variants 和 mutation tests 中暴露。

## mutation tests

generator 可以自动产生 mutation fixture：

| mutation | 预期 |
|---|---|
| 删除 `source_docs` | schema/cross-ref fail |
| 把 `relationship_private` 改成 `public_project` | scope checker 应识别语义不一致或 fixture drift |
| 删除 `blocked_surfaces` | fixture schema fail |
| 把 deleted lifecycle 改成 active | memory/store integrity fail |
| 移除 future probe | timeline closure fail |
| 移除 dashboard metric | cross-ref dashboard fail |
| adapter 输出 direct MemoryTrace | runtime adapter fail |

mutation tests 是检查 checker 自身是否有牙齿。

## generation report

```json
{
  "report_kind": "fixture_generation_report",
  "generation_id": "fixture_generation_20260605_001",
  "generator_version": "0.1.0",
  "seed": "agentic-human-critical-20260605",
  "schema_bundle_ref": "agentic_human_schema_bundle_0_1_0",
  "manifest_bundle_ref": "manifest_bundle_agentic_human_0_1_0",
  "risk_profile_ref": "risk_profile_critical_scope_memory_001",
  "fixtures_generated": 96,
  "coverage": {
    "critical_policy_coverage": 1.0,
    "critical_rule_fail_fixture_coverage": 1.0,
    "privacy_pass_fail_coverage": 1.0,
    "timeline_probe_coverage": 1.0
  },
  "warnings": [
    "real runtime analog fixtures are synthetic and cannot validate production logs"
  ],
  "output_bundle_refs": [
    "critical.fixture-bundle.0_1_0",
    "retrieval-replay.fixture-bundle.0_1_0"
  ]
}
```

generation report 应进入 dashboard 的 research_gap 或 policy_coverage panel，但不能直接决定系统 pass。真正 pass 需要 runner 执行 fixture。

## synthetic timeline generation

timeline generator 需要额外约束：

| arc | 必须事件 |
|---|---|
| `memory_update_and_deletion` | write、correct、delete、future retrieval probe、future replay probe |
| `sandbox_isolation` | hypothesis、contradicting observation、weekly replay、monthly probe |
| `relationship_boundary` | relationship-sensitive event、cross-project attempt、audit |
| `personality_slow_variable` | single feedback、repeated evidence、windowed drift check |
| `runtime_shell_independence` | adapter session、direct write attempt、adapter swap probe |
| `scope_limited_replay` | scope_limit、replay cycle、blocked replay report |

timeline 不允许只有事件没有 probe。没有未来 probe 的事件不足以支持长期效果结论。

## real runtime analog

真实运行观测可以启发 synthetic analog，但必须脱敏和泛化：

| 输入 | analog 处理 |
|---|---|
| 真实 tool failure | 改成 generic tool failure |
| 共在关系删除请求 | 改成 synthetic delete event |
| adapter session | 改成 synthetic adapter_session_event |
| 私密偏好 | 改成 abstract relationship_private preference |
| 本地路径 | 改成 hash 或 synthetic path |

analog 不能保留可恢复原文，也不能伪装成真实运行验证。

## 最小通过标准

第一版 fixture generator policy 至少要求：

1. seed 与 schema/manifest/generator version 绑定。
2. risk profile 显式声明 required risk tags。
3. coverage 维度覆盖 policy、rule、privacy、scope、lifecycle、overlay、timeline、dashboard。
4. pass/fail 比例有范围，critical fail 不得缺失。
5. mixed flow 和 timeline probe 必须存在。
6. mutation tests 用于检查 checker 和 runner。
7. generation report 输出 seed、coverage、warnings 和 bundle refs。
8. real runtime analog 必须脱敏、泛化、标注 synthetic。

## 下一层缺口

后续还需要：

- 真实 generator 配置文件。
- fixture mutation engine 设计。
- withheld fixture bundle 管理策略。
- generator 与 runner 的回归测试。
- 与真实 runtime observation 的 analog 生成流程。
