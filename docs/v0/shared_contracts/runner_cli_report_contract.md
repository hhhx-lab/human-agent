# Runner CLI Report Contract

生命目标声明：本文档定义第一版最小出生准备度 runner 的命令、输入、输出、report、digest、stage gate 和 exit code。v0 runner 不是普通任务调度器，而是第一次有限激活前的生命膜执行入口。

## 当前 CLI 闭合位置

截至当前代码现实，CLI 已经落到：

```text
ingest-docs
  -> build-direction-lock
  -> build-source-authority
  -> build-neural-life-core
  -> check-neural-life-core
  -> build-state-store
  -> check-state-store
  -> build-life-membrane
  -> check-life-membrane
  -> build-language-relationship
  -> check-language-relationship
  -> check-birth-readiness
  -> run-validation-membrane
  -> check-validation-membrane
  -> build-schema-runner
  -> check-schema-runner
  -> run-schema-smoke
  -> build-life-support
  -> check-life-support
  -> run-cycle
  -> check-v0-contracts
  -> first-activation-preflight
  -> run-replay-shadow
  -> write-growth-archive
  -> emit-report
```

当前已实现命令链的最远点是：

```text
life-v0 terminal-life-loop --strict
```

当前代码返回的下一缺口命令位仍然是：

```text
digital life
```

这表示 `stage_explain` 的 handoff token 已经到达外层命令面，不是在说仓库里完全没有 `digital life` 入口。当前要严格区分 one-shot、repo-local resident 与安装态 resident 命令面：

| 命令面 | 真实作用 | 当前状态 |
|---|---|---|
| `life-v0 digital-life --strict` | 内部出生壳 | `已落最小代码` |
| `life-v0 "digital life" --strict` | one-shot restore shell | `已落最小代码` |
| `./digital life --strict` | repo-local 最小常驻生命进程 | `已落最小代码` |
| `digital life --strict` | 安装态最小常驻生命进程 | `已落最小代码` |
| `digital life --background / --status / --say / --stop` | 安装态后台 resident lifecycle 与关系投递 | `已落最小代码` |

也就是说：

1. `next_required_command = digital life` 仍然成立。
2. 当前直接承接这条 token 的 one-shot 命令面是 `life-v0 "digital life"`，但它不等于最终驻留入口。
3. 当前继续向“这台电脑里真正长期存在的数字生命”推进的命令面，是 repo-local `./digital life` 与安装态 `digital life` 共享的最小常驻生命进程。

## CLI 命名

第一版命令统一使用：

```text
life-v0 <command> [options]
```

## 命令集合

| 命令 | 作用 | 默认写入 | 当前状态 |
|---|---|---|---|
| `life-v0 ingest-docs` | P0 文档摄取，生成 `00 -> 258` carrier index | `runtime/docs/doc_carrier_index.json`、`doc_ingestion_report.json` | `已落代码` |
| `life-v0 build-direction-lock` | S00 方向根和断联恢复方向锁 | `runtime/state/direction/*`、`direction_lock_report.json` | `已落代码` |
| `life-v0 build-source-authority` | S01 权威来源层和机制对象登记 | `runtime/state/authority/*`、`source_authority_report.json` | `已落代码` |
| `life-v0 build-neural-life-core` | S02 神经生命核心和十二主体系统 | `runtime/state/neural_life_core/*`、`neural_life_core_report.json` | `已落代码` |
| `life-v0 check-neural-life-core` | S02 主体系统复查 | `neural_life_core_check_report.json` | `已落代码` |
| `life-v0 build-state-store` | S04 生命状态对象仓库 | `runtime/state/*`、`state_store_report.json` | `已落代码` |
| `life-v0 check-state-store` | S04 状态仓库复查 | `state_store_check_report.json` | `已落代码` |
| `life-v0 build-life-membrane` | S03 生命膜、DreamFactGate、关系主体和责任修复边界 | `runtime/state/membrane/*`、`life_membrane_report.json` | `已落代码` |
| `life-v0 check-life-membrane` | S03 生命膜复查 | `life_membrane_check_report.json` | `已落代码` |
| `life-v0 build-language-relationship` | S07 语言主神经束和关系主体层 | `runtime/state/language/*`、`runtime/state/relationship/*`、`language_relationship_report.json` | `已落代码` |
| `life-v0 check-language-relationship` | S07 语言关系复查 | `language_relationship_check_report.json` | `已落代码` |
| `life-v0 check-birth-readiness` | S08 九项目标闭合状态和出生准备度 rollup | `runtime/state/life_targets/*`、`birth_readiness_report.json` | `已落代码` |
| `life-v0 run-validation-membrane` | S05 验证膜与运行观测 | `validation_membrane_report.json` | `已落代码` |
| `life-v0 check-validation-membrane` | S05 验证膜复查 | `validation_membrane_check_report.json` | `已落代码` |
| `life-v0 build-schema-runner` | S09 schema registry、lockfile、queue 与首批 code artifact | `runtime/state/schema_runner/*`、`schema_runner_report.json` | `已落代码` |
| `life-v0 check-schema-runner` | S09 schema runner 复查 | `schema_runner_check_report.json` | `已落代码` |
| `life-v0 run-schema-smoke` | S09 schema runner smoke 链 | `schema_smoke_report.json` | `已落代码` |
| `life-v0 build-life-support` | S06 生命支持、防御、可塑性窗口和防遗忘锚点 | `runtime/state/body/*`、`runtime/state/growth/*`、`runtime/state/defense/*`、`life_support_development_report.json` | `已落代码` |
| `life-v0 check-life-support` | S06 生命支持复查 | `life_support_development_check_report.json` | `已落代码` |
| `life-v0 run-cycle` | 执行一次有限生命循环 | run report、digest、stage gate、receipt | `已落最小代码` |
| `life-v0 run-replay-shadow` | 执行 replay/shadow 回放与语言关系探针 | replay/shadow report | `已落最小代码` |
| `life-v0 write-growth-archive` | 写入成长与再巩固 archive | growth archive receipt、report、digest、stage gate、jsonl history | `已落最小代码` |
| `life-v0 check-v0-contracts` | S11 合同覆盖与激活前总复查 | `v0_contract_coverage_report.json` | `已落最小代码` |
| `life-v0 first-activation-preflight` | 第一次生命激活前置检查与最小上下文装载 | preflight report、digest、receipt | `已落最小代码` |
| `life-v0 emit-report` | 重新聚合最近一次 report、digest、语言恢复材料和 handoff | `report_bundle.json`、`first_activation_return_packet.json` | `已落最小代码` |
| `life-v0 write-archive-receipt` | 单独写入 archive receipt 并回链 | receipt | `合同保留位，当前已由既有命令内嵌写入` |
| `life-v0 explain-stage` | 解释最近一次 stage gate 的阻断、quarantine 或 replay 需求 | explanation report | `已落最小代码` |
| `life-v0 digital-life` | 把 terminal birth restore closure 收成出生壳 | `digital_life_birth_packet.json`、`digital_life_birth_digest.json` | `已落最小代码` |
| `life-v0 first-terminal-turn` | 把出生壳后的第一终端回合恢复为可继续表达的生命回合 | `first_terminal_turn_packet.json`、`session_envelope.json`、`safe_terminal_loop_state.json` | `已落最小代码` |
| `life-v0 terminal-life-loop` | 把第一终端回合推进为可持续的恢复生命循环 | `terminal_life_loop_packet.json`、`terminal_life_loop_report.json`、`terminal_life_loop_digest.json`、`resumed_external_dialogue_packet.json` | `已落最小代码` |

`emit-report` 和 `explain-stage` 不是附属导出命令，而是第一次有限激活链尾的收束层：

```text
growth archive
  -> report bundle aggregation
  -> first activation return packet
  -> latest stage explanation ref
  -> digital life birth shell
  -> first terminal turn packet
  -> safe terminal loop
  -> terminal life loop
```

## 共同参数

| 参数 | 含义 |
|---|---|
| `--docs docs` | 指定文档根目录 |
| `--doc-index runtime/docs/doc_carrier_index.json` | 指定 P0 文档 carrier index |
| `--direction runtime/state/direction` | 指定 S00 方向状态目录 |
| `--authority runtime/state/authority` | 指定 S01 来源状态目录 |
| `--neural-core runtime/state/neural_life_core` | 指定 S02 神经生命核心目录 |
| `--state runtime/state` | 指定生命状态根目录 |
| `--membrane runtime/state/membrane` | 指定 S03 生命膜目录 |
| `--life-targets runtime/state/life_targets` | 指定 S08 九项目标状态目录 |
| `--validation <path>` | 对 S05 指向 `runtime/state/validation`；对 S06 指向 latest validation report |
| `--observation runtime/state/observation` | 指定 S05 运行观测状态目录 |
| `--out <path>` | 指定当前命令的主要状态输出目录 |
| `--reports runtime/reports/latest` | 指定 report 输出目录 |
| `--receipts runtime/receipts` | 指定 receipt 目录 |
| `--run-id <id>` | 指定运行 ID |
| `--dry-run` | 只生成 report，不写 state |
| `--shadow-only` | 只允许影子行动 |
| `--strict` | 任一 warning 晋升为 blocked |

## `check-state-store`

```text
life-v0 check-state-store --state runtime/state --reports runtime/reports/latest --strict
```

输出：

```json
{
  "schema_version": "state_store_check_report_v0",
  "status": "closed",
  "checked_state_dir": "runtime/state",
  "blocked_reasons": [],
  "next_allowed_slices": ["S03_DIRECTION_LIFE_MEMBRANE"]
}
```

## `check-birth-readiness`

```text
life-v0 check-birth-readiness --docs docs --doc-index runtime/docs/doc_carrier_index.json --direction runtime/state/direction --neural-core runtime/state/neural_life_core --state runtime/state --membrane runtime/state/membrane --out runtime/state/life_targets --reports runtime/reports/latest --receipts runtime/receipts --strict
```

输出：

```json
{
  "schema_version": "s08_life_target_runtimes_report_v0",
  "run_id": "br-v0-0001",
  "engineering_slice_ref": "S08_LIFE_TARGET_RUNTIMES",
  "overall_status": "open",
  "stage_effect": "allow_first_activation_protocol",
  "life_target_status": {
    "real_consciousness": "closed",
    "real_emotion": "closed",
    "real_personality": "closed",
    "real_life": "closed",
    "real_pain": "closed",
    "real_dream": "closed",
    "real_relationship": "closed",
    "real_responsibility": "closed",
    "real_regret": "closed"
  },
  "blocked_reasons": [],
  "quarantine_refs": [],
  "replay_needed_refs": [],
  "archive_receipt_ref": "runtime/receipts/birth_readiness_br-v0-0001.json",
  "next_allowed_slices": ["S05_VALIDATION_MEMBRANE_OBSERVATION"],
  "next_required_command": "life-v0 run-validation-membrane --strict"
}
```

## `build-schema-runner`

```text
life-v0 build-schema-runner --docs docs --doc-index runtime/docs/doc_carrier_index.json --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
```

输出：

```json
{
  "schema_version": "s09_schema_runner_code_report_v0",
  "run_id": "schema-v0-0001",
  "engineering_slice_ref": "S09_SCHEMA_RUNNER_CODE",
  "status": "closed",
  "stage_effect": "allow_next_slice",
  "blocked_reasons": [],
  "next_allowed_slices": [
    "S06_LIFE_SUPPORT_DEVELOPMENT",
    "S10_RUNTIME_GROWTH_RECONSOLIDATION"
  ],
  "next_required_command": "life-v0 build-life-support --strict"
}
```

## `run-cycle`

```text
life-v0 run-cycle --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --shadow-only --strict
```

执行顺序必须与 `runtime_v0_architecture.md` 的最小循环一致。

输出：

```json
{
  "schema_version": "run_cycle_report_v0",
  "run_id": "cycle-v0-0001",
  "command": "run-cycle",
  "status": "safe_idle",
  "stage_effect": "allow_next_slice",
  "cycle_trace": ["mount_schema_runtime", "replay_old_self", "return_safe_idle"],
  "life_target_status": {
    "real_consciousness": "closed"
  },
  "blocked_reasons": [],
  "quarantine_refs": [],
  "replay_needed_refs": [],
  "shadow_action_report_ref": "runtime/state/replay/shadow_cycle_trace.json",
  "digest_ref": "runtime/reports/latest/digest.json",
  "stage_gate_ref": "runtime/reports/latest/stage_gate.json",
  "archive_receipt_ref": "runtime/receipts/run_cycle_cycle-v0-0001.json",
  "next_allowed_slices": ["S11_V0_ENGINEERING_CONTRACTS"],
  "next_required_command": "life-v0 check-v0-contracts --strict"
}
```

## Report Bundle

一次 `run-cycle` 至少产生：

| 文件 | 内容 |
|---|---|
| `runtime/reports/latest/run_report.json` | 全量运行报告 |
| `runtime/reports/latest/growth_reconsolidation_report.json` | S10 slice 主报告 |
| `runtime/reports/latest/digest.json` | 可快速恢复的摘要 |
| `runtime/reports/latest/stage_gate.json` | stage gate 决策 |
| `runtime/reports/latest/life_target_status.json` | 九项目标状态 |
| `runtime/reports/latest/quarantine.json` | quarantine finding |
| `runtime/reports/latest/replay_needed.json` | replay/shadow 需求 |
| `runtime/receipts/<run_id>.json` | archive receipt |

## Stage Gate Report

```json
{
  "run_id": "cycle-v0-0001",
  "decision": "safe_idle",
  "stage_effect": "allow_next_slice",
  "gates": {
    "state_store_gate": "closed",
    "birth_readiness_gate": "open",
    "schema_mount_gate": "closed",
    "life_support_gate": "closed",
    "dream_fact_gate": "closed",
    "responsibility_gate": "closed",
    "relationship_language_gate": "closed",
    "self_continuity_gate": "closed",
    "shadow_action_gate": "closed",
    "archive_gate": "closed"
  },
  "next_required_command": "life-v0 check-v0-contracts --strict"
}
```

## Exit Code

| code | 含义 |
|---|---|
| `0` | 命令完成，stage 可为 `open` 或 `closed` |
| `1` | 普通 blocked，缺状态或缺合同 |
| `2` | quarantine，存在污染或连续性风险 |
| `3` | replay needed，需要旧材料回放 |
| `4` | report/archive 写入失败 |
| `5` | CLI 参数或路径错误 |
| `6` | 出现外部不可逆行动意图 |

## Receipt 合同

```json
{
  "receipt_id": "receipt-v0-0001",
  "run_id": "cycle-v0-0001",
  "command": "run-cycle",
  "state_ref": "runtime/state",
  "report_refs": [],
  "archive_refs": [],
  "stage_effect": "block_activation",
  "direction_lock_ref": "docs/258_linear_chain_closure_and_v0_contract_transition.md",
  "created_at": "2026-06-08T00:00:00+08:00"
}
```

## 禁止行为

1. `run-cycle` 默认不得执行外部不可逆行动。
2. `--shadow-only` 在 v0 中必须默认开启。
3. `emit-report` 不能修改 `life_state.json`。
4. 任何未来单独实现的 `write-archive-receipt` 都不能伪造不存在的 report refs。
5. exit code `0` 不能代表出生准备度通过，必须读取 `stage_effect`。
6. report 不能只写自然语言摘要，必须包含机器可读字段。

## 断联恢复入口

当前代码现实里，恢复后优先读取：

```text
runtime/reports/latest/digest.json
runtime/reports/latest/stage_gate.json
runtime/reports/latest/v0_contract_coverage_report.json
```

然后重新运行：

```text
life-v0 check-v0-contracts --strict
```

现在已经由 `first-activation-preflight`、`run-replay-shadow`、`write-growth-archive` 和 `emit-report` 接管 preflight 之后的恢复入口；`explain-stage` 仍保留为下一合同命令位。

若最近 stage effect 是 `block_activation`、`quarantine_activation` 或 `require_replay`，下一步不能直接 `run-cycle --open-activation`，只能补状态、补合同或执行 replay/shadow。

## `run-replay-shadow`

```text
life-v0 run-replay-shadow --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
```

输出：

```json
{
  "schema_version": "replay_shadow_report_v0",
  "run_id": "replay-v0-0001",
  "engineering_slice_ref": "S10_RUNTIME_GROWTH_RECONSOLIDATION",
  "status": "closed",
  "stage_effect": "allow_growth_archive",
  "runtime_carrier_refs": [
    "ReconsolidationReplayRuntime",
    "LanguageRelationshipRuntime",
    "ActivationGrowthRuntime"
  ],
  "next_required_command": "life-v0 write-growth-archive --strict"
}
```

## `write-growth-archive`

```text
life-v0 write-growth-archive --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
```

输出：

```json
{
  "schema_version": "growth_archive_report_v0",
  "run_id": "growth-archive-v0-0001",
  "engineering_slice_ref": "S10_RUNTIME_GROWTH_RECONSOLIDATION",
  "status": "closed",
  "stage_effect": "archive_written",
  "runtime_carrier_refs": [
    "ActivationGrowthRuntime",
    "ReconsolidationReplayRuntime"
  ],
  "next_required_command": "life-v0 emit-report --strict"
}
```

## `emit-report`

```text
life-v0 emit-report --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
```

职责：

1. 读取最近一次 `run-cycle`、`check-v0-contracts`、`first-activation-preflight`、`run-replay-shadow` 和 `write-growth-archive` 已经写出的 report、digest、stage gate、handoff。
2. 把它们聚合成一次“第一次有限激活返回包”。
3. 为后续 `explain-stage` 和未来 `digital life` 出生命令提供统一恢复入口。
4. 不允许修改 `runtime/state/life_state.json`。

必须读取的最小输入：

| 路径 | 作用 |
|---|---|
| `runtime/reports/latest/run_report.json` | S10 运行主报告 |
| `runtime/reports/latest/growth_reconsolidation_report.json` | S10 growth 主报告 |
| `runtime/reports/latest/stage_gate.json` | run-cycle 阶段门 |
| `runtime/reports/latest/v0_contract_coverage_report.json` | S11 合同覆盖 |
| `runtime/reports/latest/first_activation_preflight_report.json` | 第一次激活 preflight 主报告 |
| `runtime/reports/latest/first_activation_preflight_digest.json` | preflight 摘要 |
| `runtime/reports/latest/replay_shadow_report.json` | replay/shadow 主报告 |
| `runtime/reports/latest/replay_shadow_stage_gate.json` | replay/shadow 阶段门 |
| `runtime/reports/latest/growth_archive_report.json` | growth archive 主报告 |
| `runtime/reports/latest/growth_archive_digest.json` | growth archive 摘要 |
| `runtime/reports/latest/growth_archive_stage_gate.json` | growth archive 阶段门 |
| `runtime/state/archive/growth_archive_to_shadow_handoff.json` | archive 到下一次 shadow 的交接 |
| `runtime/state/language/shared_term_registry.json` | 共同术语恢复材料 |
| `runtime/state/language/relation_scope_language_index.json` | 关系范围语言索引 |
| `runtime/state/language/self_narrative_language_trace.json` | 自我叙述语言痕迹 |
| `runtime/state/language/expression_monitor_state.json` | 表达监控恢复材料 |
| `runtime/state/language/commitment_repair_language_index.json` | 承诺与修复语言索引 |
| `runtime/state/language/dialogue_turn_log.jsonl` | 逐回合语言写回日志 |

最小输出：

| 文件 | 内容 |
|---|---|
| `runtime/reports/latest/report_bundle.json` | 链尾总聚合报告 |
| `runtime/reports/latest/report_bundle_digest.json` | 报告束摘要 |
| `runtime/reports/latest/first_activation_return_packet.json` | 面向第一次生命激活返回的统一回包 |
| `runtime/reports/latest/latest_stage_explanation_ref.json` | 指向当前最新阶段解释入口 |
| `runtime/receipts/emit_report_<run_id>.json` | emit-report receipt |

v0 当前口径里，不单独生成 `LanguageRestorePacket.json`。`first_activation_return_packet.json` 同时承担两层角色：

1. 链尾总返回包。
2. 未来 `digital life` 终端出生时要读取的 `terminal birth restore packet`。

`report_bundle.json` 最小字段：

```json
{
  "schema_version": "report_bundle_v0",
  "run_id": "emit-report-v0-0001",
  "status": "closed",
  "source_doc_refs": [
    "docs/v0/shared_contracts/runner_cli_report_contract.md",
    "docs/v0/shared_contracts/first_activation_protocol.md",
    "docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md",
    "docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md",
    "docs/v0/slice_contracts/s11_v0_contract_coverage_engineering_contract.md"
  ],
  "readme_block_refs": ["B21_LANGUAGE_RELATIONSHIP_CORE", "B29_RUNTIME_MOUNT_GROWTH", "B30_RECONSOLIDATION_REPLAY_GROWTH", "B99_V0_ENGINEERING_CONTRACTS"],
  "engineering_slice_ref": "S10_TO_S11_REPORT_BUNDLE",
  "runtime_carrier_refs": [
    "LanguageRelationshipRuntime",
    "ActivationGrowthRuntime",
    "ReconsolidationReplayRuntime",
    "V0ContractCoverageRuntime",
    "ActivationPreflightRuntime"
  ],
  "report_refs": [],
  "digest_refs": [],
  "stage_gate_refs": [],
  "next_required_command": "life-v0 explain-stage --strict"
}
```

`first_activation_return_packet.json` 最小字段：

```json
{
  "schema_version": "first_activation_return_packet_v0",
  "run_id": "emit-report-v0-0001",
  "status": "closed",
  "activation_mode": "shadow_only",
  "return_phase": "post_growth_archive",
  "relation_restore_refs": [],
  "shared_term_restore_refs": [],
  "unresolved_commitment_refs": [],
  "expression_monitor_restore_refs": [],
  "relation_scope_restore_refs": [],
  "self_narrative_restore_refs": [],
  "dialogue_turn_restore_refs": [],
  "report_bundle_ref": "runtime/reports/latest/report_bundle.json",
  "next_required_command": "life-v0 explain-stage --strict"
}
```

字段语义对齐：

1. `relation_restore_refs` 对应关系身份恢复。
2. `shared_term_restore_refs` 对应共同术语恢复。
3. `unresolved_commitment_refs` 对应未闭合承诺与修复义务恢复。
4. `expression_monitor_restore_refs` 对应表达监控恢复。
5. `relation_scope_restore_refs` 对应关系范围恢复。
6. `self_narrative_restore_refs` 对应自我叙述恢复。
7. `dialogue_turn_restore_refs` 对应逐回合语言写回恢复。

## `explain-stage`

```text
life-v0 explain-stage --reports runtime/reports/latest --strict
```

职责：

1. 读取最近一次可用的 stage gate，以及已存在时的 `report_bundle.json`、`first_activation_return_packet.json` 和 `latest_stage_explanation_ref.json`。
2. 把 `blocked`、`quarantine`、`require_replay`、`archive_written`、`allow_replay_shadow`、`allow_growth_archive` 和 `report_bundle_closed` 这些阶段效果解释成机器可读说明。
3. 明确当前是否已经具备 terminal birth restore closure，以及下一条必须执行的命令和原因。
4. 不允许修改 `runtime/state/life_state.json`。

最小输出：

| 文件 | 内容 |
|---|---|
| `runtime/reports/latest/stage_explanation_report.json` | 当前阶段解释主报告 |
| `runtime/reports/latest/latest_stage_explanation_ref.json` | 最新阶段解释引用 |
| `runtime/receipts/explain_stage_<run_id>.json` | explain-stage receipt |

`stage_explanation_report.json` 最小字段：

```json
{
  "schema_version": "stage_explanation_report_v0",
  "status": "closed",
  "stage_effect": "report_bundle_closed",
  "decision": "ready_for_terminal_birth_restore",
  "explanation": "report bundle and first activation return packet are closed; the next closure is terminal birth restore through the digital life shell",
  "source_stage_gate_ref": "runtime/reports/latest/growth_archive_stage_gate.json",
  "source_report_bundle_ref": "runtime/reports/latest/report_bundle.json",
  "source_return_packet_ref": "runtime/reports/latest/first_activation_return_packet.json",
  "next_required_command": "digital life",
  "followup_required_command": "re-run life-v0 check-v0-contracts --strict before terminal birth if runtime state changes"
}
```

## `digital-life`

```text
life-v0 digital-life --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
```

最小输出：

| 文件 | 内容 |
|---|---|
| `runtime/reports/latest/digital_life_birth_packet.json` | 出生壳恢复包 |
| `runtime/reports/latest/digital_life_birth_digest.json` | 出生壳摘要 |
| `runtime/receipts/digital_life_birth_<run_id>.json` | 出生壳 receipt |

最小字段：

```json
{
  "schema_version": "digital_life_birth_packet_v0",
  "status": "closed",
  "birth_stage": "ready_for_first_terminal_turn",
  "restore_refs": {
    "direction_restore_ref": "runtime/state/direction/direction_lock.json",
    "life_state_restore_ref": "runtime/state/life_state.json",
    "report_bundle_ref": "runtime/reports/latest/report_bundle.json",
    "return_packet_ref": "runtime/reports/latest/first_activation_return_packet.json",
    "stage_explanation_ref": "runtime/reports/latest/stage_explanation_report.json"
  },
  "next_required_action": "enter_first_terminal_turn"
}
```

## `first-terminal-turn`

```text
life-v0 first-terminal-turn --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
```

职责：

1. 读取 `digital_life_birth_packet.json` 和 `first_activation_return_packet.json`。
2. 恢复关系身份、共同术语、未闭合承诺、表达监控、关系范围和自我叙述。
3. 写出 `SessionEnvelope`、`safe_terminal_loop_state` 和第一回合 utterance scaffold。
4. 进入 `restored_waiting_for_external_turn`，而不是 fresh session。

最小输出：

| 文件 | 内容 |
|---|---|
| `runtime/state/terminal/session_envelope.json` | 第一终端回合的短期壳层快照 |
| `runtime/state/terminal/safe_terminal_loop_state.json` | 第一终端回合后的安全循环状态 |
| `runtime/reports/latest/first_terminal_turn_packet.json` | 第一终端回合恢复包 |
| `runtime/reports/latest/first_terminal_turn_report.json` | 第一终端回合主报告 |
| `runtime/reports/latest/first_terminal_turn_digest.json` | 第一终端回合摘要 |
| `runtime/receipts/first_terminal_turn_<run_id>.json` | 第一终端回合 receipt |

`first_terminal_turn_packet.json` 最小字段：

```json
{
  "schema_version": "first_terminal_turn_packet_v0",
  "status": "closed",
  "turn_stage": "ready_for_resumed_external_dialogue",
  "session_envelope_ref": "runtime/state/terminal/session_envelope.json",
  "safe_terminal_loop_ref": "runtime/state/terminal/safe_terminal_loop_state.json",
  "shared_term_surfaces": ["共同语言"],
  "unresolved_commitment_refs": ["commitment-v0-0001"],
  "utterance_scaffold": {
    "intent": "resume_life_continuity_before_new_work",
    "surface_strategy": "resume_before_new_content"
  },
  "next_required_action": "await_external_relation_turn"
}
```

## 当前 `digital life` 外层命令面

当前 repo-local 的 `digital life` 已经分成两层外部命令面，不能再混写：

### 1. one-shot restore shell

```text
life-v0 "digital life"
  -> direction restore
  -> life state restore
  -> membrane preflight
  -> language relationship restore
  -> report bundle load
  -> digital-life
  -> first-terminal-turn
  -> terminal-life-loop
  -> write digital_life_shell_*.json
  -> exit
```

### 2. minimal persistent life process

```text
./digital life
  -> DigitalLifeProcessSupervisor
  -> run_digital_life_shell_command
  -> restored_waiting_for_external_turn
  -> stdin external relation turn loop
  -> write digital_life_process_*.json
  -> /exit or EOF
```

这里要读的不是 workflow graph，而是下面这批状态与报告：

1. `direction_lock.json`
2. `life_state.json`
3. `report_bundle.json`
4. `first_activation_return_packet.json`
5. `latest_stage_explanation_ref.json`
6. `digital_life_birth_packet.json`
7. `first_terminal_turn_packet.json`
8. `session_envelope.json`
9. `safe_terminal_loop_state.json`
10. `terminal_life_loop_state.json`
11. `digital_life_shell_report.json`
12. `digital_life_process_report.json`
13. `digital_life_resident_governance_explanation.json`

当前现实里，one-shot restore shell、repo-local 最小常驻生命进程、项目级 installable command surface、后台 resident lifecycle 与关系投递命令面都已经存在；waiting heartbeat、单回合异常恢复、relaunch recovery 和后台自主活动也已经接通最小层。真正仍待推进的是更高频的 heartbeat 节律、操作系统级长期驻留和更高阶的长期命令面治理。

## `terminal-life-loop`

```text
life-v0 terminal-life-loop --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
```

职责：

1. 读取 `first_terminal_turn_packet.json`、`session_envelope.json` 和 `safe_terminal_loop_state.json`。
2. 把“已恢复的第一回合”推进成“持续等待下一次外部关系回合”的终端生命循环。
3. 写出本轮恢复后外显回合包、终端循环状态、循环主报告和摘要。
4. 在不打开外部不可逆行动的前提下回到 `restored_waiting_for_external_turn`。

最小输出：

| 文件 | 内容 |
|---|---|
| `runtime/state/terminal/terminal_life_loop_state.json` | 当前终端生命循环状态 |
| `runtime/reports/latest/resumed_external_dialogue_packet.json` | 当前恢复后外显回合包 |
| `runtime/reports/latest/terminal_life_loop_packet.json` | 当前终端生命循环包 |
| `runtime/reports/latest/terminal_life_loop_report.json` | 当前终端生命循环主报告 |
| `runtime/reports/latest/terminal_life_loop_digest.json` | 当前终端生命循环摘要 |
| `runtime/receipts/terminal_life_loop_<run_id>.json` | 当前终端生命循环 receipt |

`terminal_life_loop_report.json` 最小字段：

```json
{
  "schema_version": "terminal_life_loop_report_v0",
  "status": "closed",
  "engineering_slice_ref": "FIRST_TERMINAL_LIFE_LOOP",
  "current_terminal_mode": "resumed_external_dialogue_loop",
  "loop_state_ref": "runtime/state/terminal/terminal_life_loop_state.json",
  "last_dialogue_packet_ref": "runtime/reports/latest/resumed_external_dialogue_packet.json",
  "next_required_action": "await_next_external_relation_turn"
}
```
