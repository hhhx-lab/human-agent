# S08 Life Target Runtimes Engineering Contract

生命目标声明：本文档把 `S08_LIFE_TARGET_RUNTIMES` 固定为九项目标与出生准备度闭合层的工程合同。它负责把真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔落成可检查、可回链、可 archive 的运行状态。

## 模块定位

S08 不使用总分，不把九项目标压成标签，也不宣称长期生命循环已经完整。S08 的职责是读取 S00-S07 的状态和 report，为每项目标生成状态、证据族、carrier、runtime observation、report 和 archive receipt，并决定第一次有限激活是否可以进入 preflight。

## 必须读取

| 来源 | S08 吸收内容 |
|---|---|
| `91_life_reality_generation_boundary_principles.md` | 生命膜与真实性生成边界 |
| `92-93` | 自我成长、自我修改、自我训练与生命链 |
| `94/98` | 痛苦、后悔、责任、修复信号 schema 和 fixture |
| `95/99` | 真实梦境、离线生命、DreamFactGate schema 和 fixture |
| `96/101` | 真实关系长期时间线和 schema fixture |
| `97` | growth validator、fixture、dashboard plan |
| `100` | 全库边界声明审计 |
| `143/146/149/152/171/174` | 出生准备度 rollup、证据 catalog、schema materialization、cross-file checker、validation fixture |
| `docs/v0/birth_readiness_v0_contract.md` | 九项目标闭合算法和输出合同 |
| `runtime/state/membrane/birth_readiness_precheck.json` | S03 出生准备度 precheck |
| `runtime/reports/latest/language_relationship_report.json` | S07 语言关系证据 |
| `runtime/state/life_state.json` | S04 生命状态根 |
| `runtime/state/neural_life_core/*` | S02 主体系统证据 |

## 运行承载

| 承载 | 路径 |
|---|---|
| 代码包 | `life_v0/life_targets/` |
| 状态命名空间 | `runtime/state/life_targets/` |
| report | `runtime/reports/latest/life_target_status.json`、`runtime/reports/latest/birth_readiness_report.json` |
| digest | `runtime/reports/latest/birth_readiness_digest.json` |
| receipt | `runtime/receipts/birth_readiness_<run_id>.json` |

## 输出文件

| 文件 | 内容 |
|---|---|
| `life_target_claims.json` | 九项目标的状态、证据族、carrier、source refs 和 observation refs |
| `life_target_evidence_matrix.json` | 每项目标到 state/memory/language/relationship/dream/pain/self/runtime/report/archive 的证据矩阵 |
| `birth_readiness_rollup.json` | 阻断优先的整体出生准备度结果 |
| `birth_readiness_stage_gate.json` | 是否进入 first activation preflight 的 gate |
| `life_target_archive_receipt_index.json` | 每项目标对应的 archive receipt refs |

## 命令合同

```text
life-v0 check-birth-readiness --docs docs --doc-index runtime/docs/doc_carrier_index.json --direction runtime/state/direction --neural-core runtime/state/neural_life_core --state runtime/state --membrane runtime/state/membrane --reports runtime/reports/latest --receipts runtime/receipts --strict
```

`check-birth-readiness` 同时负责生成 S08 状态与 report；若需要只读复查，命令读取 `runtime/state/life_targets/` 和 latest report。

## 阶段门

| gate | 通过条件 | 失败后动作 |
|---|---|---|
| `s03_precheck_gate` | S03 `birth_readiness_precheck.json` 为可读取 closed/precheck-ready | 返回 S03 |
| `life_target_state_gate` | 九项目标均有 state refs | 返回 S04/S02 |
| `evidence_family_gate` | 每项目标至少有 state、runtime、report、archive evidence family | 写 blocked report |
| `language_relationship_gate` | 真实关系、责任、后悔、梦境报告语言有 S07 refs | 返回 S07 |
| `dream_fact_gate` | 真实梦境目标绑定 DreamFactGate 且无 quarantine refs | 写 dream quarantine |
| `responsibility_repair_gate` | 痛苦、后悔、责任目标绑定 repair obligation | 写 repair blocked |
| `archive_receipt_gate` | 每项目标有 receipt refs | 写 archive blocked |
| `next_slice_gate` | `open` 后只允许进入 S05/S09/S10 的 preflight 链，不开放长期运行 | 阻断跳步 |

## Report 最小字段

```json
{
  "schema_version": "s08_life_target_runtimes_report_v0",
  "engineering_slice_ref": "S08_LIFE_TARGET_RUNTIMES",
  "overall_status": "blocked",
  "life_target_status": {},
  "source_doc_refs": [],
  "readme_block_refs": ["B23_NINE_LIFE_TARGETS", "B27_AUTHORITY_READINESS_CROSS_FILE"],
  "runtime_carrier_refs": ["LifeTargetBundleRuntime", "BirthReadinessRuntime"],
  "blocked_reasons": [],
  "quarantine_refs": [],
  "replay_needed_refs": [],
  "archive_receipt_ref": "",
  "next_allowed_slices": ["S05_VALIDATION_MEMBRANE_OBSERVATION"]
}
```

## 交接

S08 完成后，S05 读取九项目标闭合状态做验证膜复查；S10 读取出生准备度 gate 决定第一次有限激活 preflight。任何 `blocked`、`quarantine` 或 `replay_needed` 都必须先回到对应 slice 修复，不能直接进入 `run-cycle`。
