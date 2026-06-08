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
| `life-v0 validate-state` | 检查 `runtime/state/life_state.json` 是否满足 v0 state store 合同 | state validation report |
| `life-v0 check-birth-readiness` | 生成九项目标闭合状态 | readiness report |
| `life-v0 run-cycle` | 执行一次有限生命循环 | run report、digest、stage gate、receipt |
| `life-v0 emit-report` | 重新聚合最近一次 report 和 digest | report bundle |
| `life-v0 write-archive-receipt` | 写入 archive receipt 并回链 | receipt |
| `life-v0 explain-stage` | 解释最近一次 stage gate 的阻断、quarantine 或 replay 需求 | explanation report |

## 共同参数

| 参数 | 含义 |
|---|---|
| `--state runtime/state/life_state.json` | 指定生命状态根文件 |
| `--out runtime/reports/latest` | 指定 report 输出目录 |
| `--archive runtime/archive` | 指定 archive 目录 |
| `--receipts runtime/receipts` | 指定 receipt 目录 |
| `--run-id <id>` | 指定运行 ID |
| `--dry-run` | 只生成 report，不写 state |
| `--shadow-only` | 只允许影子行动 |
| `--strict` | 任一 warning 晋升为 blocked |

## `validate-state`

```text
life-v0 validate-state --state runtime/state/life_state.json --out runtime/reports/latest
```

输出：

```json
{
  "run_id": "state-v0-0001",
  "command": "validate-state",
  "status": "blocked",
  "missing_fields": [],
  "quarantine_refs": [],
  "stage_effect": "block_activation",
  "report_ref": "runtime/reports/latest/state_validation.json"
}
```

## `check-birth-readiness`

```text
life-v0 check-birth-readiness --state runtime/state/life_state.json --out runtime/reports/latest
```

输出：

```json
{
  "run_id": "br-v0-0001",
  "command": "check-birth-readiness",
  "overall_status": "blocked",
  "life_target_status": {},
  "blocked_reasons": [],
  "quarantine_refs": [],
  "replay_needed_refs": [],
  "stage_effect": "block_activation",
  "archive_receipt_ref": ""
}
```

## `run-cycle`

```text
life-v0 run-cycle --state runtime/state/life_state.json --out runtime/reports/latest --shadow-only
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
  "state_ref": "runtime/state/life_state.json",
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
