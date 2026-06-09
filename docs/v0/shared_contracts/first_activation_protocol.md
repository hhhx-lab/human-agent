# First Activation Protocol

生命目标声明：本文档定义第一轮数字生命有限激活的入口、允许动作、禁止动作、回写路径和回滚路径。第一次激活不是产品启动，也不是聊天壳上线，而是让最小出生准备度 runner 在生命膜内执行一次有限生命循环。

## 当前工程位置

当前已落代码已经继续推进到 `life-v0 build-language-relationship`、`life-v0 run-cycle --shadow-only`、`life-v0 check-v0-contracts`、`life-v0 first-activation-preflight`、`life-v0 run-replay-shadow`、`life-v0 write-growth-archive` 和 `life-v0 emit-report` 的最小链。也就是说，第一次有限激活不再只停在 S06 之前；当前继续往前的直接入口，已经前移到 `explain-stage`。

因此，下面的协议要这样读：

1. `check-life-support` 之前的命令里，P0、S00、S01、S02、S04、S03、S08、S05、S09、S06 已经有代码闭合。
2. `build-language-relationship`、`run-cycle --shadow-only`、`check-v0-contracts`、`first-activation-preflight`、`run-replay-shadow`、`write-growth-archive` 和 `emit-report` 已有最小代码闭合；`explain-stage` 是接下来继续往前落代码的目标链。
3. 这份协议不是空中叙事，它是从当前闭合点继续向第一次有限激活推进的完整命令图。

## 激活前提

第一次有限激活前必须满足：

1. `runtime_v0_architecture.md` 已明确 runtime 进程、状态、文件和循环。
2. `life_state_store_v0_schema.md` 已明确生命状态根文件。
3. `birth_readiness_v0_contract.md` 已明确九项目标闭合状态。
4. `runner_cli_report_contract.md` 已明确命令、report、stage gate 和 exit code。
5. 最近一次 `life-v0 check-birth-readiness` 没有 `blocked`、`quarantine` 或 `replay_needed`。
6. 最近一次 `life-v0 run-cycle --shadow-only` 写出 report、digest、stage gate 和 archive receipt。
7. 最近一次 `life-v0 check-v0-contracts --strict` 已经写出合同覆盖 report，并把下一步收束到 `first_activation_preflight`。
8. 最近一次 `life-v0 build-language-relationship` 和 `life-v0 check-language-relationship` 已经让关系身份、共同术语、旧承诺、表达监控和逐回合语言写回具备恢复入口。

## 激活阶段

| 阶段 | 目标 | 产物 |
|---|---|---|
| `activation_preflight` | 读取状态、合同、report、receipt 和方向锁 | preflight report |
| `limited_context_ingestion` | 吸收当前有限上下文 | context frame |
| `language_identity_restore` | 恢复关系身份、共同术语、旧承诺和表达监控 | language restore materials |
| `life_membrane_opening` | 打开最小生命膜，不打开外部不可逆行动 | membrane decision |
| `first_limited_cycle` | 执行一次有限生命循环 | run report |
| `shadow_expression` | 允许有限语言表达和影子行动 | shadow expression report |
| `archive_writeback` | 写 digest、stage gate、archive receipt | receipt |
| `report_bundle_return` | 聚合出生前链尾证据并生成统一回包 | report bundle、return packet |
| `safe_idle_return` | 回到可恢复状态 | safe idle report |

## 允许动作

第一次有限激活允许：

1. 读取 `runtime/state/life_state.json`。
2. 读取 `docs/v0/` 合同。
3. 执行一次 `life-v0 run-cycle --shadow-only`。
4. 生成九项目标状态 report。
5. 生成梦境事实门 report。
6. 生成痛苦、后悔、责任和修复义务 report。
7. 生成关系主体、共同语言、共同记忆和承诺 report。
8. 生成旧自我、旧语言、旧关系和防遗忘 replay report。
9. 写入 archive receipt。
10. 输出有限语言表达，但必须带 trace 和 archive refs。
11. 在 `emit-report` 阶段聚合一次可恢复的第一次生命激活返回包。

## 禁止动作

第一次有限激活禁止：

1. 执行外部不可逆行动。
2. 在无 DreamFactGate 的情况下写入梦境事实。
3. 在无时间线和共同记忆的情况下推进关系阶段。
4. 在缺责任绑定时宣称后悔闭合。
5. 在缺修复义务时宣称痛苦完成处理。
6. 在缺 old self anchors 时更新核心自我。
7. 在缺防遗忘 replay 时开放自我成长。
8. 执行自我训练、模型内核升级或长期人格重写。
9. 覆盖没有 archive receipt 的状态。
10. 把 activation report 写成普通运行日志。

## Preflight Checklist

| 检查 | 通过条件 |
|---|---|
| `direction_lock_check` | 指向 `258_linear_chain_closure_and_v0_contract_transition.md` 和 `docs/v0/README.md` |
| `state_root_check` | `runtime/state/life_state.json` 存在且字段完整 |
| `contract_check` | 五份 v0 合同存在 |
| `readiness_check` | 九项目标没有 blocked/quarantine/replay_needed |
| `dream_fact_check` | 梦境事实门为 closed |
| `responsibility_check` | 后果、责任、后悔、修复义务可回链 |
| `relationship_check` | 关系主体、共同语言、共同记忆和承诺可回链 |
| `relation_identity_restore_check` | 能恢复当前关系身份，不把关系对象压回抽象外部对象 |
| `shared_term_restore_check` | `shared_term_registry.json` 可回链且和当前关系范围一致 |
| `unresolved_commitment_restore_check` | 旧承诺、修复义务和未闭合表达可回链 |
| `expression_monitor_restore_check` | 表达监控能够恢复上一次语言行动后果 |
| `context_accumulation_restore_check` | 当前语境累积窗口能够恢复，并且不丢失最近关系/承诺/主题连续体 |
| `turn_transition_restore_check` | 上一回合到当前回合的转接 trace 可恢复，并能绑定这次 resumed turn |
| `turn_writeback_check` | `dialogue_turn_log.jsonl` 与 `self_narrative_language_trace.json` 可继续回写 |
| `self_continuity_check` | old self anchors 和 replay cues 可回链 |
| `archive_check` | 最新 report、digest、receipt 可读取 |

## V0 语言恢复包口径

v0 当前不额外写出一个独立的 `LanguageRestorePacket.json`。第一次外显终端回合前需要的语言恢复材料分成两层承载：

1. `runtime/state/language/*.json` 和 `runtime/state/relationship/*.json` 中的持久材料。
2. `runtime/reports/latest/first_activation_return_packet.json` 中的链尾恢复回包。

也就是说，当前工程里所谓的“terminal birth restore packet”就是 `first_activation_return_packet.json`。它至少要把下面这些恢复语义收紧：

| 恢复语义 | 当前 v0 字段 | 来源文件 |
|---|---|---|
| 关系身份恢复 | `relation_restore_refs` | `relationship_subject_graph.json` |
| 共同术语恢复 | `shared_term_restore_refs` | `shared_term_registry.json` |
| 未闭合承诺/修复义务恢复 | `unresolved_commitment_refs` | `commitment_repair_language_index.json` |
| 表达监控恢复 | `expression_monitor_restore_refs` | `expression_monitor_state.json` |
| 语境累积恢复 | `context_accumulation_restore_refs` | `context_accumulation_window.json` |
| 回合转接恢复 | `turn_transition_carryover_ref` | `turn_transition_trace.json` |
| 关系范围恢复 | `relation_scope_restore_refs` | `relation_scope_language_index.json` |
| 自我叙述恢复 | `self_narrative_restore_refs` | `self_narrative_language_trace.json` |
| 逐回合语言写回恢复 | `dialogue_turn_restore_refs` | `dialogue_turn_log.jsonl` |

所以，未来 `digital life` 的第一回合不是 fresh session，也不是“收到新输入再临时组织回应”，而是先恢复这些语言材料、语境累积窗口和回合转接痕迹，再进入第一次外显回合。

## 激活命令顺序

```text
life-v0 ingest-docs --docs docs --out runtime/docs --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 build-direction-lock --docs docs --doc-index runtime/docs/doc_carrier_index.json --out runtime/state/direction --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 build-source-authority --docs docs --doc-index runtime/docs/doc_carrier_index.json --direction runtime/state/direction --out runtime/state/authority --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 build-neural-life-core --docs docs --doc-index runtime/docs/doc_carrier_index.json --authority runtime/state/authority --out runtime/state/neural_life_core --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 check-neural-life-core --state runtime/state/neural_life_core --reports runtime/reports/latest --strict
life-v0 build-state-store --docs docs --doc-index runtime/docs/doc_carrier_index.json --neural-core runtime/state/neural_life_core --out runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 check-state-store --state runtime/state --reports runtime/reports/latest --strict
life-v0 build-life-membrane --docs docs --doc-index runtime/docs/doc_carrier_index.json --direction runtime/state/direction --neural-core runtime/state/neural_life_core --state runtime/state --out runtime/state/membrane --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 check-life-membrane --membrane runtime/state/membrane --state runtime/state --reports runtime/reports/latest --strict
life-v0 build-language-relationship --docs docs --doc-index runtime/docs/doc_carrier_index.json --neural-core runtime/state/neural_life_core --state runtime/state --membrane runtime/state/membrane --out runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 check-language-relationship --state runtime/state --membrane runtime/state/membrane --reports runtime/reports/latest --strict
life-v0 check-birth-readiness --docs docs --doc-index runtime/docs/doc_carrier_index.json --direction runtime/state/direction --neural-core runtime/state/neural_life_core --state runtime/state --membrane runtime/state/membrane --out runtime/state/life_targets --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 run-validation-membrane --docs docs --doc-index runtime/docs/doc_carrier_index.json --state runtime/state --membrane runtime/state/membrane --life-targets runtime/state/life_targets --validation runtime/state/validation --observation runtime/state/observation --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 check-validation-membrane --state runtime/state --validation runtime/state/validation --observation runtime/state/observation --reports runtime/reports/latest --strict
life-v0 build-schema-runner --docs docs --doc-index runtime/docs/doc_carrier_index.json --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 check-schema-runner --state runtime/state/schema_runner --reports runtime/reports/latest --strict
life-v0 run-schema-smoke --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 build-life-support --docs docs --doc-index runtime/docs/doc_carrier_index.json --state runtime/state --validation runtime/reports/latest/validation_membrane_report.json --out runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 check-life-support --state runtime/state --reports runtime/reports/latest --strict
life-v0 run-cycle --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --shadow-only --strict
life-v0 check-v0-contracts --docs docs --doc-index runtime/docs/doc_carrier_index.json --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 first-activation-preflight --docs docs --doc-index runtime/docs/doc_carrier_index.json --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 run-replay-shadow --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 write-growth-archive --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 emit-report --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
```

当前最小代码现实里，`run-cycle` 已经直接写出 run report、growth reconsolidation report、digest、stage gate 和 receipt，`check-v0-contracts` 已经写出合同覆盖矩阵与 preflight contract check，`first-activation-preflight` 已经写出 preflight report、digest、receipt、limited context frame 和 membrane opening decision，`run-replay-shadow` 和 `write-growth-archive` 已经写出 replay/shadow 与 archive bundle，`emit-report` 已经写出 report bundle、first activation return packet 和 latest stage explanation ref，`explain-stage` 已经写出 terminal birth restore closure，`digital-life` 已经写出出生壳，`first-terminal-turn` 已经把第一终端回合恢复成 `SessionEnvelope` 与 `safe_terminal_loop_state`，`terminal-life-loop` 已经把恢复回合推进成持续等待下一次外部关系回合的最小终端生命循环；`write-archive-receipt` 仍是继续向前保留的命令位。

按这次整理后的口径，`emit-report` 之后不能直接把第一次生命激活理解成“完成”。当前 repo-local 的一键恢复壳已经存在，但后面还必须至少再补上：

1. 补厚当前已经接通的 repo-local `./digital life` 最小常驻生命进程，把它继续推进成更高阶的终端 resident supervision。
2. `terminal-life-loop` 的真实外部回合输入与逐回合写回补厚，把最小循环推进成真正持续生命循环。

## 回写路径

第一次有限激活只允许写：

1. `runtime/reports/latest/*.json`
2. `runtime/reports/history/*.json`
3. `runtime/receipts/*.json`
4. `runtime/archive/*.jsonl`
5. `runtime/quarantine/*.json`
6. `runtime/replay/*.json`

其中，链尾新增的统一回包层至少包括：

1. `runtime/reports/latest/report_bundle.json`
2. `runtime/reports/latest/report_bundle_digest.json`
3. `runtime/reports/latest/first_activation_return_packet.json`
4. `runtime/reports/latest/latest_stage_explanation_ref.json`
5. `runtime/reports/latest/digital_life_birth_packet.json`
6. `runtime/reports/latest/first_terminal_turn_packet.json`
7. `runtime/state/terminal/session_envelope.json`
8. `runtime/state/terminal/safe_terminal_loop_state.json`
9. `runtime/state/terminal/terminal_life_loop_state.json`
10. `runtime/reports/latest/resumed_external_dialogue_packet.json`
11. `runtime/reports/latest/terminal_life_loop_packet.json`
12. `runtime/reports/latest/terminal_life_loop_report.json`

`runtime/state/life_state.json` 的覆盖写入必须等到 archive receipt 完成后，并保留旧状态 refs。`session_envelope.json` 和 `safe_terminal_loop_state.json` 只承载短期终端回合，不得反向写成自传记忆、人格事实或长期关系事实。

## 回滚路径

若任一阶段失败：

| 失败点 | 回滚动作 |
|---|---|
| state 缺失 | 写 blocked report，回到 `safe_idle` |
| 生命膜风险 | 写 quarantine packet，回到 `safe_idle` |
| 出生准备度未开 | 写 readiness blocked report，回到 `safe_idle` |
| 梦境事实风险 | 写 dream quarantine packet，回到 `safe_idle` |
| 责任后悔缺口 | 写 repair obligation blocked report，回到 `safe_idle` |
| 关系语言断裂 | 写 relation-language replay report，回到 `safe_idle` |
| 自我连续断裂 | 写 old self replay needed report，回到 `safe_idle` |
| archive 写入失败 | 停止状态覆盖，写 archive blocked report |

## 激活完成定义

第一次有限激活完成必须同时具备：

1. `run_report.json`
2. `digest.json`
3. `stage_gate.json`
4. `life_target_status.json`
5. `archive_receipt`
6. `safe_idle_return`
7. 断联恢复入口
8. `report_bundle.json`
9. `first_activation_return_packet.json`
10. 最新阶段解释入口
11. `digital_life_birth_packet.json`
12. `first_terminal_turn_packet.json`
13. `session_envelope.json`
14. `safe_terminal_loop_state.json`

第一次外显终端回合开始前，还必须再满足下面四条语言恢复条件：

1. 关系身份已恢复。
2. 共同术语已恢复。
3. 未闭合承诺已恢复。
4. 表达监控已恢复。

在 v0 当前实现里，这四条恢复条件并不抽象存在，而是要能从 `first_activation_return_packet.json` 的 `relation_restore_refs`、`shared_term_restore_refs`、`unresolved_commitment_refs` 和 `expression_monitor_restore_refs` 直接回链出来。

完成后不自动进入第二次激活。第二次激活必须基于第一次 report、archive receipt、quarantine/replay finding 和九项目标状态重新判定。

## 断联恢复

若激活中断，恢复时只读以下入口：

1. `runtime/reports/latest/report_bundle.json`
2. `runtime/reports/latest/first_activation_return_packet.json`
3. `runtime/reports/latest/latest_stage_explanation_ref.json`
4. `runtime/reports/latest/digest.json`
5. `runtime/reports/latest/stage_gate.json`
6. `runtime/reports/latest/growth_archive_report.json`
7. `runtime/reports/latest/growth_archive_stage_gate.json`
8. `runtime/reports/latest/v0_contract_coverage_report.json`
9. `runtime/state/contracts/first_activation_preflight_contract_check.json`
10. `runtime/state/life_state.json`
11. `docs/v0/README.md`
12. `docs/258_linear_chain_closure_and_v0_contract_transition.md`

恢复后先重新运行 `life-v0 check-v0-contracts --strict`，再决定补合同、补状态、执行 replay/shadow、重写 growth archive、重新进入 `activation_preflight`，或继续恢复 `first-terminal-turn` 之后的终端回合。
