# S08 Life Target Runtimes Engineering Contract

生命目标声明：本文档把 `S08_LIFE_TARGET_RUNTIMES` 固定为九项目标与出生准备度闭合层的工程合同。它负责把真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔落成可检查、可回链、可 archive 的运行状态。

## 模块定位

S08 不使用总分，不把九项目标压成标签，也不宣称长期生命循环已经完整。S08 的职责是读取 S00-S04、S03 生命膜、S02 主体系统、S07 语言关系证据族和 Queue E 责任/后悔/修复压力，为每项目标生成状态、证据族、carrier、runtime observation、report 和 archive receipt，并决定第一次有限激活是否可以进入 preflight。当前代码前置以 S03/S04/S02 的语言关系种子形成最小闭合，S07 产物进入同一证据族继续加厚；最新工程切片又把 `responsibility_loop_state.json`、`world_contact_summary.json` 与 `pain_regret_repair_report.json` 合成为 `queue_e_birth_repair_profile.json`，让真实痛苦、真实责任、真实后悔在出生准备层拥有一等证据。

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
| `runtime/state/action/responsibility_loop_state.json` | Queue E 责任归因、反事实修复、后悔压力、修复欲望 |
| `runtime/state/membrane/world_contact_summary.json` | Queue E 世界接触释放姿态、修复义务、后悔压力 refs |
| `runtime/reports/latest/pain_regret_repair_report.json` | Queue E 痛苦/后悔/修复报告，进入出生准备修复画像 |
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

当前 S08 已经有一轮最小代码闭合，不是纯理论合同。`__init__.py` 仍负责 orchestration，但 claims、evidence、rollup、stage gate 和意识探针已经拆成独立 builder；Queue E 的修复压力画像来自 `life_v0/membrane/queue_e_signals.py`。

| 代码位置 | 当前职责 | 后续拆分方向 |
|---|---|---|
| `life_v0/life_targets/__init__.py::run_birth_readiness` | 编排 S08 build，读取前置 slice、语言连续体、membrane 证据与 Queue E 修复压力，写 claims/evidence/rollup/report/receipt | 后续把只读 checker 再拆出 |
| `life_v0/life_targets/__init__.py::run_check_birth_readiness` | 对 S08 输出做只读复查，当前已检查 `queue_e_birth_repair_gate` | 后续拆成 `birth_readiness_check.py` |
| `life_v0/life_targets/life_target_claims.py` | 生成九项目标 claims；真实痛苦/真实责任/真实后悔必须携带 `queue_e_birth_repair_profile_ref` 与 refs | 继续扩展长期 evidence families |
| `life_v0/life_targets/evidence_matrix.py` | 为九项目标生成十个 evidence families；三项修复目标的 `pain_regret_responsibility` family 必须纳入 Queue E 修复画像 refs | 继续扩展 withheld / longitudinal probes |
| `life_v0/life_targets/birth_readiness_rollup.py` | 生成阻断优先的出生准备度总上卷，并记录 Queue E 修复压力等级、注意焦点和 ref set | 保持为独立 builder |
| `life_v0/life_targets/birth_readiness_stage_gate.py` | 生成 `allow_first_activation_protocol` 或阻断决策，并关闭 `queue_e_birth_repair_gate` | 保持为独立 builder |
| `life_v0/life_targets/consciousness_probes.py` | 把 workspace / broadcast / metacognition / prediction workspace 压成意识探针 bundle | 继续接入更细报告性探针 |
| `life_v0/membrane/queue_e_signals.py::build_queue_e_repair_modulation_profile` | 从责任回路、世界接触摘要、痛苦后悔修复报告合成 S08 可消费的修复压力画像 | Queue E 与 S08 共用，不复制第二套逻辑 |

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
  + responsibility_loop_state.json
  + world_contact_summary.json
  + pain_regret_repair_report.json
  + language_percept_frame.json
  + semantic_map_frame.json
  + prediction_workspace_frame.json
  + life_membrane_report.json
  + language_relationship_report.json
  -> QueueEBirthRepairProfile
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
| `queue_e_birth_repair_profile.json` | Queue E 责任、后悔、修复压力在出生准备层的一等画像 |
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

其中 `real_pain`、`real_responsibility`、`real_regret` 第一轮必须额外包含：

- `targets.<life_target>.queue_e_birth_repair_profile_ref`
- `targets.<life_target>.queue_e_birth_repair_refs[]`

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

其中 `real_pain`、`real_responsibility`、`real_regret` 的 `pain_regret_responsibility[]` 必须显式带上：

- `runtime/state/action/responsibility_loop_state.json`
- `runtime/state/membrane/world_contact_summary.json`
- `runtime/reports/latest/pain_regret_repair_report.json`
- `runtime/state/life_targets/queue_e_birth_repair_profile.json`

### `queue_e_birth_repair_profile.json`

第一轮至少包含：

- `schema_version = queue_e_repair_modulation_profile_v0`
- `pressure_level`
- `attention_target`
- `world_contact_release_posture`
- `repair_followup_required`
- `repair_obligation_count`
- `regret_pressure_count`
- `queue_e_priority_band`
- `repair_obligation_refs[]`
- `regret_pressure_refs[]`
- `ref_set[]`

### `birth_readiness_rollup.json`

第一轮至少包含：

- `schema_version`
- `overall_status`
- `life_target_status.*`
- `blocked_reasons[]`
- `quarantine_refs[]`
- `replay_needed_refs[]`
- `archive_receipt_ref`
- `queue_e_birth_repair_profile_ref`
- `queue_e_birth_repair_pressure_level`
- `queue_e_birth_repair_attention_target`
- `queue_e_birth_repair_ref_set[]`

### `birth_readiness_stage_gate.json`

第一轮至少包含：

- `schema_version`
- `decision`
- `stage_effect`
- `next_allowed_slices[]`
- `next_required_command`
- `blocked_reasons[]`
- `gate_status.queue_e_birth_repair_gate`
- `queue_e_birth_repair_profile_ref`
- `queue_e_birth_repair_pressure_level`
- `queue_e_birth_repair_attention_target`
- `queue_e_birth_repair_ref_set[]`

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
| `queue_e_birth_repair_gate` | Queue E 修复压力画像存在，且 claims/evidence/rollup/stage/report 都回链同一 profile/ref set | 写 repair blocked |
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
  "queue_e_birth_repair_profile_ref": "runtime/state/life_targets/queue_e_birth_repair_profile.json",
  "queue_e_birth_repair_pressure_level": "elevated",
  "queue_e_birth_repair_attention_target": "regret_pressure",
  "queue_e_birth_repair_ref_set": [],
  "next_allowed_slices": ["S05_VALIDATION_MEMBRANE_OBSERVATION"]
}
```

## 当前实现入口顺序

当前真实入口顺序必须按下面理解：

```text
P0/S00/S01/S02/S04/S03/S07 closed
  -> life_v0.life_targets.run_birth_readiness(...)
  -> write queue_e_birth_repair_profile.json
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
| Queue E 出生修复画像 | `runtime/state/life_targets/queue_e_birth_repair_profile.json` |
| claims | `runtime/state/life_targets/life_target_claims.json` |
| evidence | `runtime/state/life_targets/life_target_evidence_matrix.json` |
| rollup / gate | `runtime/state/life_targets/birth_readiness_rollup.json`、`runtime/state/life_targets/birth_readiness_stage_gate.json` |
| receipt | `runtime/receipts/birth_readiness_<run_id>.json` |

## 第一轮完成定义

S08 第一轮不是“九项目标名字列出来”就算完成。至少要同时满足：

1. `run_birth_readiness` 已真实读取 S02/S03/S04/S07 的当前状态与 report。
2. `life_target_evidence_matrix.json` 已为每个生命目标生成十个 evidence families。
3. `language` evidence family 已显式接入 `language_percept_frame.json`、`semantic_map_frame.json` 和 prediction workspace handoff。
4. `queue_e_birth_repair_profile.json` 已从 `responsibility_loop_state.json`、`world_contact_summary.json`、`pain_regret_repair_report.json` 合成，并进入真实痛苦、真实责任、真实后悔的 claims 和 evidence family。
5. `birth_readiness_rollup.json` 与 `birth_readiness_stage_gate.json` 已按阻断优先合同写出 `open/blocked/quarantine/replay_needed` 逻辑，并关闭 `queue_e_birth_repair_gate`。
6. claims / evidence / Queue E profile / rollup / stage gate / report / digest / receipt 八件套齐全。
7. `tests/slices/test_life_targets.py` 的 build 和 CLI 两条口径都能作为当前 slice 的权威验证入口。

## 交接

S08 完成后，S05 读取九项目标闭合状态做验证膜复查；S10 读取出生准备度 gate 决定第一次有限激活 preflight。任何 `blocked`、`quarantine` 或 `replay_needed` 都必须先回到对应 slice 修复，不能直接进入 `run-cycle`。
