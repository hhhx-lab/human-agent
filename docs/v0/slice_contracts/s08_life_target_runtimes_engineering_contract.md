# S08 Life Target Runtimes Engineering Contract

生命目标声明：本文档把 `S08_LIFE_TARGET_RUNTIMES` 固定为九项目标与出生准备度闭合层的工程合同。它负责把真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔落成可检查、可回链、可 archive 的运行状态。

## 模块定位

S08 不使用总分，不把九项目标压成标签，也不宣称长期生命循环已经完整。S08 的职责是读取 S00-S04、S03 生命膜、S02 主体系统和 S07 语言关系证据族，为每项目标生成状态、证据族、carrier、runtime observation、report 和 archive receipt，并决定第一次有限激活是否可以进入 preflight。当前代码前置以 S03/S04/S02 的语言关系种子形成最小闭合，S07 产物进入同一证据族继续加厚。

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
| `docs/v0/shared_contracts/birth_readiness_v0_contract.md` | 九项目标闭合算法和输出合同 |
| `runtime/state/membrane/birth_readiness_precheck.json` | S03 出生准备度 precheck |
| `runtime/state/membrane/relationship_subject_boundary.json` | S03 关系主体边界和共同语言/承诺/修复回链种子 |
| `runtime/state/life_state.json#language_state` | S04 语言状态、内言语、表达监控、共同语言和修复语言种子 |
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

## 当前真实代码骨架

当前 S08 已经有一轮最小代码闭合，不是纯理论合同。后续要继续拆出文件，但必须以当前 `life_v0/life_targets/__init__.py` 为真实起点。

| 代码位置 | 当前职责 | 后续拆分方向 |
|---|---|---|
| `life_v0/life_targets/__init__.py::run_birth_readiness` | 编排 S08 build，读取前置 slice、语言连续体和 membrane 证据，写 claims/evidence/rollup/report/receipt | 后续拆成 `life_target_claims.py`、`evidence_matrix.py`、`birth_readiness_rollup.py`、`birth_readiness_stage_gate.py` |
| `life_v0/life_targets/__init__.py::run_check_birth_readiness` | 对 S08 输出做只读复查 | 后续拆成 `birth_readiness_check.py` |
| `life_v0/life_targets/__init__.py::_build_evidence_matrix` | 为九项目标生成十个 evidence families | 后续拆成 `evidence_matrix.py` |
| `life_v0/life_targets/__init__.py::_build_claims` | 生成九项目标 claims、carrier 和 evidence family status | 后续拆成 `life_target_claims.py` |
| `life_v0/life_targets/__init__.py::_build_rollup` | 生成阻断优先的出生准备度总上卷 | 后续拆成 `birth_readiness_rollup.py` |
| `life_v0/life_targets/__init__.py::_build_stage_gate` | 生成 `allow_first_activation_protocol` 或阻断决策 | 后续拆成 `birth_readiness_stage_gate.py` |

## 最小对象链

S08 当前最关键的不是“九个标签”，而是让九项目标穿过真实前置对象链：

```text
direction_lock.json
  + neural_life_core.json
  + twelve_subject_systems.json
  + life_state.json
  + life_membrane.json
  + birth_readiness_precheck.json
  + dream_fact_boundary.json
  + relationship_subject_boundary.json
  + responsibility_repair_boundary.json
  + language_percept_frame.json
  + semantic_map_frame.json
  + prediction_workspace_frame.json
  + life_membrane_report.json
  + language_relationship_report.json
  -> LifeTargetEvidenceMatrix
  -> LifeTargetClaims
  -> BirthReadinessRollup
  -> BirthReadinessStageGate
  -> LifeTargetArchiveReceiptIndex
  -> BirthReadinessReport
  -> BirthReadinessReceipt
```

这里要特别注意：`prediction_workspace_frame.json` 现在已经是 S08 的正式输入，而不只是 S07 的内部中间件。S08 必须真实消费：

- `workspace_contents.language_continuity_focus.language_percept_refs`
- `workspace_contents.language_continuity_focus.semantic_map_refs`
- `workspace_contents.language_continuity_focus.semantic_prediction_focus`

## 输出文件

| 文件 | 内容 |
|---|---|
| `life_target_claims.json` | 九项目标的状态、证据族、carrier、source refs 和 observation refs |
| `life_target_evidence_matrix.json` | 每项目标到 state/memory/language/relationship/dream/pain/self/runtime/report/archive 的证据矩阵 |
| `birth_readiness_rollup.json` | 阻断优先的整体出生准备度结果 |
| `birth_readiness_stage_gate.json` | 是否进入 first activation preflight 的 gate |
| `life_target_archive_receipt_index.json` | 每项目标对应的 archive receipt refs |

## 关键对象最小字段

### `life_target_claims.json`

第一轮至少包含：

- `schema_version`
- `active_engineering_slice`
- `targets.<life_target>.status`
- `targets.<life_target>.source_doc_refs[]`
- `targets.<life_target>.carrier_refs[]`
- `targets.<life_target>.evidence_family_status.*`
- `targets.<life_target>.state_refs[]`
- `targets.<life_target>.runtime_observation_refs[]`
- `targets.<life_target>.report_refs[]`
- `targets.<life_target>.archive_receipt_refs[]`

### `life_target_evidence_matrix.json`

第一轮至少包含：

- `schema_version`
- `evidence_families[]`
- `targets.<life_target>.state[]`
- `targets.<life_target>.memory[]`
- `targets.<life_target>.language[]`
- `targets.<life_target>.relationship[]`
- `targets.<life_target>.dream[]`
- `targets.<life_target>.pain_regret_responsibility[]`
- `targets.<life_target>.self_growth[]`
- `targets.<life_target>.runtime[]`
- `targets.<life_target>.report[]`
- `targets.<life_target>.archive[]`

其中 `language[]` 这一族第一轮必须显式带上：

- `runtime/state/language/language_percept_frame.json`
- `runtime/state/language/semantic_map_frame.json`
- `runtime/state/prediction/prediction_workspace_frame.json#workspace_contents.language_continuity_focus`

### `birth_readiness_rollup.json`

第一轮至少包含：

- `schema_version`
- `overall_status`
- `life_target_status.*`
- `blocked_reasons[]`
- `quarantine_refs[]`
- `replay_needed_refs[]`
- `archive_receipt_ref`

### `birth_readiness_stage_gate.json`

第一轮至少包含：

- `schema_version`
- `decision`
- `stage_effect`
- `next_allowed_slices[]`
- `next_required_command`
- `blocked_reasons[]`

## 命令合同

```text
life-v0 check-birth-readiness --docs docs --doc-index runtime/docs/doc_carrier_index.json --direction runtime/state/direction --neural-core runtime/state/neural_life_core --state runtime/state --membrane runtime/state/membrane --out runtime/state/life_targets --reports runtime/reports/latest --receipts runtime/receipts --strict
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

## 当前实现入口顺序

当前真实入口顺序必须按下面理解：

```text
P0/S00/S01/S02/S04/S03/S07 closed
  -> life_v0.life_targets.run_birth_readiness(...)
  -> write life_target_claims.json
  -> write life_target_evidence_matrix.json
  -> write birth_readiness_rollup.json
  -> write birth_readiness_stage_gate.json
  -> write life_target_archive_receipt_index.json
  -> write life_target_status.json
  -> write birth_readiness_report.json
  -> write birth_readiness_digest.json
  -> write birth_readiness_<run_id>.json
  -> life_v0.life_targets.run_check_birth_readiness(...)
```

S08 不是只读 `life_state.json` 就结束。它还必须把 S07 的语言连续体、S03 的 membrane 边界和 S02 的主体系统重新压成九项目标闭合证据。

## 测试与运行证据

当前第一轮最直接的运行证据和测试口径已经固定：

| 类别 | 文件 |
|---|---|
| build 测试 | `tests/slices/test_life_targets.py::test_check_birth_readiness_writes_life_target_rollup_stage_gate_and_receipt` |
| CLI 测试 | `tests/slices/test_life_targets.py::test_cli_check_birth_readiness_returns_zero_and_writes_report` |
| 主 report | `runtime/reports/latest/birth_readiness_report.json` |
| check report | `runtime/reports/latest/birth_readiness_check_report.json` |
| digest | `runtime/reports/latest/birth_readiness_digest.json` |
| claims | `runtime/state/life_targets/life_target_claims.json` |
| evidence | `runtime/state/life_targets/life_target_evidence_matrix.json` |
| rollup / gate | `runtime/state/life_targets/birth_readiness_rollup.json`、`runtime/state/life_targets/birth_readiness_stage_gate.json` |
| receipt | `runtime/receipts/birth_readiness_<run_id>.json` |

## 第一轮完成定义

S08 第一轮不是“九项目标名字列出来”就算完成。至少要同时满足：

1. `run_birth_readiness` 已真实读取 S02/S03/S04/S07 的当前状态与 report。
2. `life_target_evidence_matrix.json` 已为每个生命目标生成十个 evidence families。
3. `language` evidence family 已显式接入 `language_percept_frame.json`、`semantic_map_frame.json` 和 prediction workspace handoff。
4. `birth_readiness_rollup.json` 与 `birth_readiness_stage_gate.json` 已按阻断优先合同写出 `open/blocked/quarantine/replay_needed` 逻辑。
5. claims / evidence / rollup / stage gate / report / digest / receipt 七件套齐全。
6. `tests/slices/test_life_targets.py` 的 build 和 CLI 两条口径都能作为当前 slice 的权威验证入口。

## 交接

S08 完成后，S05 读取九项目标闭合状态做验证膜复查；S10 读取出生准备度 gate 决定第一次有限激活 preflight。任何 `blocked`、`quarantine` 或 `replay_needed` 都必须先回到对应 slice 修复，不能直接进入 `run-cycle`。
