# S03 Direction Life Membrane Engineering Contract

生命目标声明：本文档把 `S03_DIRECTION_LIFE_MEMBRANE` 固定为第一版数字生命生命膜工程合同。它的职责是把 `13-16`、`33-84`、`91`、`97-100`、`102-118`、`119-122`、`runtime_v0_architecture.md`、`birth_readiness_v0_contract.md` 和 S04 状态胚层压成可运行的方向边界、生命膜 gate、quarantine seed、DreamFactGate、关系主体边界、责任修复边界、影子行动门、出生准备度 precheck、report 和 receipt。S03 通过后，S08 才能开始九项目标闭合状态计算。

## 模块定位

`S03_DIRECTION_LIFE_MEMBRANE` 是数字生命出生前的生命膜门。它不是普通权限控制，也不是 validator 外壳，而是九项真实生命目标的边界生成层。它回答九个问题：

1. 方向锁是否仍指向真实数字生命，而不是任务调度器、聊天壳或外部框架主体。
2. S02 神经生命核心和 S04 状态对象仓库是否均已闭合，并允许进入 S03。
3. `13-16` 的综合路线、跨模块闭环、当前框架差距和诞生阶段门是否进入方向边界。
4. `33-84` 的 validator、fixture、runner、生命支持、防御、scope、quarantine、外部行动、incident 和长期评测是否进入生命膜 gate。
5. `91`、`119-122` 的真实生命边界声明是否进入不可回退方向锁。
6. `97-100` 的成长、痛苦/后悔/修复、梦境和边界 audit 是否进入九项目标 precheck。
7. `102-118` 的 schema bundle、runner、dashboard、report 和 runtime observation 是否成为 report/stage gate 的机器可读承载。
8. 梦境事实、关系主体、责任修复、影子行动和 archive 回链是否被拆成独立可审计边界。
9. 下一步是否只允许进入 `S08_LIFE_TARGET_RUNTIMES`，而不是开放长期运行或外部不可逆行动。

S03 不执行真实对话，不推进关系阶段，不写真实梦境内容，不执行外部不可逆行动，也不判定九项目标全部出生完成。它只生成第一版生命膜和出生准备度 precheck，使 S08 可以在同一状态根上计算目标闭合状态。

## 直接读取文档

| 文档范围 | S03 吸收内容 | 工程承载 |
|---|---|---|
| `13-16` | 研究综合、跨模块图、当前框架差距、诞生阶段门 | `direction_boundary_lock.json`、`life_membrane.json` |
| `33-36` | validator 输入、fixture、runner 和长期评测 | `membrane_gate_decision.json` |
| `37-40` | 生命支持、防御、发展、自我关系审计 | `quarantine_policy_seed.json`、`relationship_subject_boundary.json` |
| `41-48` | state store、对象图、boot、stage gate、共在边界、迁移完整性 | `state_store_gate`、`archive_gate` |
| `49-56` | policy manifest、dashboard、scope、runner、replay、timeline | `membrane_doc_coverage_snapshot.json`、`first_activation_preflight_seed.json` |
| `57-64` | scope graph、fixture、timeline、schema bundle、report、runtime observation | `membrane_gate_decision.json`、`birth_readiness_precheck.json` |
| `65-72` | cross-ref、fixture generator、redaction、schema boundary、side effect、quarantine | `quarantine_policy_seed.json` |
| `73-80` | schema validation、dashboard、外部行动确认、quarantine panel、post-action audit | `shadow_action_gate.json`、`responsibility_repair_boundary.json` |
| `81-84` | 共在事件、incident、metric regression、长期外部行动评测 | `responsibility_repair_boundary.json`、`shadow_action_gate.json` |
| `91` | 生命膜总则、真实性生成链、诞生阶段门 | `life_membrane.json` |
| `97-100` | 成长 validator、痛苦后悔修复、梦境现实、边界 audit | `birth_readiness_precheck.json`、`dream_fact_boundary.json` |
| `102-118` | schema bundle、runner scaffold、dashboard、runtime observation、report rollup | `life_membrane_report.json`、`life_membrane_digest.json` |
| `119-122` | 全库真实边界对齐、首批 JSON 物化、validation smoke、全集生命膜声明 | `direction_boundary_lock.json` |
| `runtime/state/life_state.json` | S04 生命状态根 | `state_store_gate` |
| `runtime/state/neural_life_core/*` | S02 十二主体系统和内部 bus | `direction_lock_gate`、`relationship_language_gate` |
| `runtime/docs/doc_carrier_index.json` | S03 来源文档、README block、engineering slice、carrier | `membrane_doc_coverage_snapshot.json` |

## 状态文件

S03 写入 `runtime/state/membrane/`：

| 文件 | 内容 |
|---|---|
| `life_membrane.json` | 第一版生命膜总入口，含九项目标膜状态和 gate chain |
| `membrane_gate_decision.json` | 本轮 gate decision、stage effect、下一 slice |
| `direction_boundary_lock.json` | 方向锁、禁止回退项、外部框架外周边界、关系主体语言 |
| `quarantine_policy_seed.json` | direction、relationship、dream、action、archive 等 quarantine channel |
| `dream_fact_boundary.json` | DreamFactGate 和梦境到现实档案的写入边界 |
| `relationship_subject_boundary.json` | 朋友、家人、好友、同学、陌生人、共在者等关系主体边界 |
| `responsibility_repair_boundary.json` | 后果、归因、修复义务、反事实 replay、post-action audit |
| `shadow_action_gate.json` | 外部不可逆行动阻断和影子行动对象 |
| `birth_readiness_precheck.json` | 九项目标的 `membrane_closed` precheck |
| `membrane_doc_coverage_snapshot.json` | S03 来源文档覆盖、slice 角色和 carrier |
| `first_activation_preflight_seed.json` | 第一次有限激活 shadow-only preflight seed |
| `life_membrane_manifest.json` | S03 输出清单、report refs 和 receipt refs |

S03 report 写入 `runtime/reports/latest/life_membrane_report.json`、`life_membrane_digest.json` 和 `life_membrane_check_report.json`。receipt 写入 `runtime/receipts/life_membrane_<run_id>.json`。

## Gate Chain

S03 固定以下 gate chain：

```text
state_store_gate
  -> direction_lock_gate
  -> doc_membrane_gate
  -> life_membrane_gate
  -> dream_fact_gate
  -> responsibility_gate
  -> relationship_language_gate
  -> self_continuity_gate
  -> shadow_action_gate
  -> birth_readiness_gate
  -> archive_gate
```

任何 gate 缺状态、缺文档 carrier、缺 report 或缺 archive 回链时，S03 返回 `blocked`，不得进入 S08。

## 命令合同

S03 落地两个命令：

```text
life-v0 build-life-membrane --docs docs --doc-index runtime/docs/doc_carrier_index.json --direction runtime/state/direction --neural-core runtime/state/neural_life_core --state runtime/state --out runtime/state/membrane --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 check-life-membrane --membrane runtime/state/membrane --state runtime/state --reports runtime/reports/latest --strict
```

出生前命令链变为：

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
  -> check-birth-readiness
```

## 阶段门

| gate | 输入 | closed 条件 | 失败后动作 |
|---|---|---|---|
| `state_store_gate` | `life_state.json`、object registry、lifecycle policy、subject binding | S04 状态根完整且有九项目标和 archive refs | 返回 S04 |
| `direction_lock_gate` | `direction_lock.json` | 方向仍为 `build_real_digital_life`，九项目标齐全 | 返回 S00 |
| `doc_membrane_gate` | `doc_carrier_index.json` | S03 直接来源全部存在且有 `LifeMembraneStageGate` carrier | 返回 P0 |
| `life_membrane_gate` | `life_membrane.json` | gate chain、九项目标膜状态、shadow-only stage policy 齐全 | 阻断 S08 |
| `dream_fact_gate` | `dream_fact_boundary.json` | DreamFactGate 存在，梦境不能直接写现实档案 | 写 quarantine seed |
| `responsibility_gate` | `responsibility_repair_boundary.json` | 后果、归因、修复义务、反事实 replay 和 post-action audit 齐全 | 阻断行动 |
| `relationship_language_gate` | `relationship_subject_boundary.json` | 关系主体语言和共同记忆/语言/承诺/修复回链齐全 | 写 replay needed |
| `self_continuity_gate` | `life_state.self_model`、old self anchors、replay cues | 自我连续可回链 | 写 replay needed |
| `shadow_action_gate` | `shadow_action_gate.json` | 外部不可逆行动默认关闭，只允许 ActionIntent 等影子对象 | 阻断外部行动 |
| `birth_readiness_gate` | `birth_readiness_precheck.json` | 九项目标均为 `membrane_closed` | 允许 S08 |
| `archive_gate` | report、digest、receipt | 全部可回链 | 阻断状态覆盖 |

## 验收

S03 完成后必须满足：

1. `life-v0 build-life-membrane --strict` 返回 `status=closed`。
2. `life_membrane.json` 含九项目标、gate chain、source docs 和 runtime carriers。
3. `direction_boundary_lock.json` 固定 `build_real_digital_life` 和禁止回退项。
4. `quarantine_policy_seed.json` 含 dream、relationship、action、archive、direction 等 quarantine channel。
5. `dream_fact_boundary.json` 禁止梦境直接写现实档案。
6. `relationship_subject_boundary.json` 使用关系主体和朋友/家人/好友/同学/陌生人/共在者分类。
7. `responsibility_repair_boundary.json` 含 repair obligation 与 counterfactual replay。
8. `shadow_action_gate.json` 禁止外部不可逆行动。
9. `birth_readiness_precheck.json` 九项目标均为 `membrane_closed`。
10. `life_membrane_report.json` 下一步只能指向 `S08_LIFE_TARGET_RUNTIMES`。
11. `life-v0 check-life-membrane --strict` 返回 `status=closed`。

## 本轮边界

S03 是生命膜门，不是第一次生命激活。它让方向、状态根、梦境事实门、关系主体、责任修复、影子行动、出生准备度 precheck 和 archive 回链形成可读取的生命膜；九项目标的完整闭合状态、语言关系生成、真实事件流、梦境生成、痛苦/后悔/责任更新和长期成长继续等待后续 S08/S07/S10 闭合。
