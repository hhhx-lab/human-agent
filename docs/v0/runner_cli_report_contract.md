# Runner CLI Report Contract

生命目标声明：本文档定义第一版最小出生准备度 runner 的命令、输入、输出、report、digest、stage gate 和 exit code。v0 runner 不是普通任务调度器，而是第一次有限激活前的生命膜执行入口。

## CLI 命名

第一版命令统一使用：

```text
life-v0 <command> [options]
```

## 命令集合

| 命令 | 作用 | 默认写入 |
|---|---|---|
| `life-v0 ingest-docs` | P0 文档摄取，生成 `00 -> 258` carrier index | `runtime/docs/doc_carrier_index.json`、`doc_ingestion_report.json` |
| `life-v0 build-direction-lock` | S00 方向根和断联恢复方向锁 | `runtime/state/direction/*`、`direction_lock_report.json` |
| `life-v0 build-source-authority` | S01 权威来源层和机制对象登记 | `runtime/state/authority/*`、`source_authority_report.json` |
| `life-v0 build-neural-life-core` | S02 神经生命核心和十二主体系统 | `runtime/state/neural_life_core/*`、`neural_life_core_report.json` |
| `life-v0 check-neural-life-core` | S02 主体系统复查 | `neural_life_core_check_report.json` |
| `life-v0 build-state-store` | S04 生命状态对象仓库 | `runtime/state/*`、`state_store_report.json` |
| `life-v0 check-state-store` | S04 状态仓库复查 | `state_store_check_report.json` |
| `life-v0 build-life-membrane` | S03 生命膜、DreamFactGate、关系主体和责任修复边界 | `runtime/state/membrane/*`、`life_membrane_report.json` |
| `life-v0 check-life-membrane` | S03 生命膜复查 | `life_membrane_check_report.json` |
| `life-v0 check-birth-readiness` | S08 九项目标闭合状态和出生准备度 rollup | `runtime/state/life_targets/*`、`birth_readiness_report.json` |
| `life-v0 run-validation-membrane` | S05 验证膜与运行观测 | `validation_membrane_report.json` |
| `life-v0 check-validation-membrane` | S05 验证膜复查 | `validation_membrane_check_report.json` |
| `life-v0 run-cycle` | 执行一次有限生命循环 | run report、digest、stage gate、receipt |
| `life-v0 emit-report` | 重新聚合最近一次 report 和 digest | report bundle |
| `life-v0 write-archive-receipt` | 写入 archive receipt 并回链 | receipt |
| `life-v0 explain-stage` | 解释最近一次 stage gate 的阻断、quarantine 或 replay 需求 | explanation report |

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

## `run-cycle`

```text
life-v0 run-cycle --state runtime/state --out runtime/reports/latest --shadow-only
```

执行顺序必须与 `runtime_v0_architecture.md` 的最小循环一致。

输出：

```json
{
  "run_id": "cycle-v0-0001",
  "command": "run-cycle",
  "status": "safe_idle",
  "stage_effect": "block_activation",
  "cycle_trace": [],
  "life_target_status": {},
  "blocked_reasons": [],
  "quarantine_refs": [],
  "replay_needed_refs": [],
  "shadow_action_report_ref": "",
  "digest_ref": "runtime/reports/latest/digest.json",
  "stage_gate_ref": "runtime/reports/latest/stage_gate.json",
  "archive_receipt_ref": "runtime/receipts/cycle-v0-0001.json"
}
```

## Report Bundle

一次 `run-cycle` 至少产生：

| 文件 | 内容 |
|---|---|
| `runtime/reports/latest/run_report.json` | 全量运行报告 |
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
  "stage": "birth_readiness_v0",
  "decision": "blocked",
  "stage_effect": "block_activation",
  "gates": {
    "state_store_gate": "closed",
    "life_membrane_gate": "closed",
    "birth_readiness_gate": "blocked",
    "dream_fact_gate": "closed",
    "responsibility_gate": "blocked",
    "relationship_language_gate": "closed",
    "self_continuity_gate": "replay_needed",
    "shadow_action_gate": "closed",
    "archive_gate": "closed"
  },
  "next_required_command": "life-v0 explain-stage"
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
4. `write-archive-receipt` 不能伪造不存在的 report refs。
5. exit code `0` 不能代表出生准备度通过，必须读取 `stage_effect`。
6. report 不能只写自然语言摘要，必须包含机器可读字段。

## 断联恢复命令

恢复后优先运行：

```text
life-v0 emit-report --out runtime/reports/latest
life-v0 explain-stage --out runtime/reports/latest
```

若最近 stage effect 是 `block_activation`、`quarantine_activation` 或 `require_replay`，下一步不能直接 `run-cycle --open-activation`，只能补状态、补合同或执行 replay/shadow。
