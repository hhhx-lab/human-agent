# Life V0 Package Construction Matrix

这份矩阵把 `life_v0/*` 真正拆到“包级施工”。

它不再回答抽象生命层，而是回答：

```text
这个包到底负责什么，
回读哪些理论，
首写或消费哪些对象，
写哪些 runtime，
由哪些测试证明，
下一轮最该补哪些文件。
```

## 使用规则

1. 每次落一个包，先看这一行，再回对应 `sXX` 合同和 `00-258` 原文。
2. 如果一个能力横跨多个包，不要跳过这份矩阵直接在 `__init__.py` 里硬粘；先把主包、辅包和共享对象分清。
3. 没有落到这张矩阵的 runtime 文件，不要默认长期保留；先判断它是不是该补进矩阵。

## A. 根与契约包

| 包 | 脑科学/理论锚点 | 主职责 | 必入对象 | 必出对象 / runtime | 主测试 / gate | 当前 / 下一步 |
|---|---|---|---|---|---|---|
| `life_v0/doc_index.py` | `构思.md`、`00`、全部 `01*`、`258` | 摄取 `00-258` 与 `v0` 文档，生成 carrier index 与回链入口 | 原始文档路径、README blocks、v0 柜位 | `runtime/docs/doc_carrier_index.json`、`runtime/state/contracts/*` | `tests/slices/test_doc_corpus_ingestor.py`、`doc_carrier_gate` | 已落；继续补 `doc_dependency_graph`、carrier drift checker |
| `life_v0/contracts/` | `258`、全部 `docs/v0/*` | v0 合同覆盖、引用解析、preflight 审计 | doc carrier index、v0 paths | `v0_contract_coverage_report.json`、`first_activation_preflight_report.json` 的合同字段 | `tests/contracts/test_v0_contracts.py`、`contract_coverage_gate` | 已落；继续补 per-package contract coverage 切面 |

## B. 方向与权威根包

| 包 | 脑科学/理论锚点 | 主职责 | 必入对象 | 必出对象 / runtime | 主测试 / gate | 当前 / 下一步 |
|---|---|---|---|---|---|---|
| `life_v0/direction/` | `00`、`13`、`16`、`91`、`119`、`122`、`258` | 身份根、方向锁、连续体锚链、断联恢复根 | doc carrier、recent receipts、life target pressure | `runtime/state/direction/direction_lock.json`、`identity_root.json`、`continuity_refs.json` | `tests/slices/test_direction_lock.py`、`direction_lock_gate` | 已落；继续补 `resume_anchor`、value drift guard |
| `life_v0/authority/` | 全部 `01*`、`142`、`145`、`151` | 权威来源、机制证据图、theory intake | 文献矩阵、研究 protocol、mechanism docs | `runtime/state/authority/authority_registry.json`、`mechanism_evidence_map.json` | `tests/slices/test_source_authority.py`、`authority_registry_gate` | 已落；继续补 authority patch index、机制-代码对照检查 |

## C. 身体、内环境与防御包

| 包 | 脑科学/理论锚点 | 主职责 | 必入对象 | 必出对象 / runtime | 主测试 / gate | 当前 / 下一步 |
|---|---|---|---|---|---|---|
| `life_v0/body/` | `04`、`07`、`08`、`11`、`18`、`37-40`、`94`、`01n`、`01s` | 节律、疲惫、恢复、需求、核心情感、情绪 episode、trait drift | direction anchors、relationship pressure、repair pressure、recent dialogue residue | `BodyRhythmPulse`、`NeedStateVector`、`CoreAffectVector`、`runtime/state/body/*` | `tests/slices/test_life_support.py`、`resource_budget_gate`、`core_affect_gate` | 第一轮已落；继续补 `affective_debt.py`、`regret_signal.py`、fatigue -> language downshift 接线 |
| `life_v0/defense/` | `37-39`、`72`、`75`、`81-84` | 隔离、防御、side-effect 前哨、coexistence caution | body pressure、membrane risk、world contact flags | `runtime/state/defense/*`、quarantine / caution state | `tests/slices/test_life_support.py`、`quarantine_gate` | 已落基础骨架；继续补 threat eval 与长期 coexistence state |

## D. 神经核心与预测包

| 包 | 脑科学/理论锚点 | 主职责 | 必入对象 | 必出对象 / runtime | 主测试 / gate | 当前 / 下一步 |
|---|---|---|---|---|---|---|
| `life_v0/neural_core/` | `02`、`03`、`10`、`11`、`18`、`22`、`30`、`143`、`146`、`149`、`152`、`171`、`01l`、`01m`、`01o`、`01p`、`01v-01ax` | 脑区图、网络状态、信号介质、工作区、广播、元认知、预测误差 | `BodyRhythmPulse`、`NeedStateVector`、authority evidence、memory cues | `PredictionWorkspaceFrame`、`SignalMediaFrame`、`ConsciousBroadcastFrame`、`runtime/state/neural_life_core/*`、`runtime/state/prediction/*` | `tests/slices/test_neural_life_core.py`、`prediction_coherence_gate`、`internal_bus_gate` | 已落第一轮；继续补 `signal_media.py`、`belief_state.py`、`prediction_error.py`、`active_sampling.py` |

## E. 状态根、记忆与自传包

| 包 | 脑科学/理论锚点 | 主职责 | 必入对象 | 必出对象 / runtime | 主测试 / gate | 当前 / 下一步 |
|---|---|---|---|---|---|---|
| `life_v0/state_store/` | `05`、`17-31`、`41-48`、`55`、`57`、`61`、`69`、`01q` | life state root、自传、关系记忆、承诺真值、engram index、自我模型 | `DialogueWritebackBundle`、dream / replay / growth receipts、direction anchors | `LifeStateRoot`、`EngramIndexFrame`、`RelationshipMemoryFrame`、`CommitmentTruthFrame`、`runtime/state/life_state.json` | `tests/slices/test_state_store.py`、`state_store_gate`、`commitment_truth_gate` | 已落第一轮；继续补 `memory_write_gate.py`、`state_merge_guard.py`、relationship memory writeback |

## F. 语言、终端回合与持续表达包

| 包 | 脑科学/理论锚点 | 主职责 | 必入对象 | 必出对象 / runtime | 主测试 / gate | 当前 / 下一步 |
|---|---|---|---|---|---|---|
| `life_v0/language/` | `09`、`85-90`、`94`、`96`、`101`、`141`、`144`、`147`、`150`、`01f`、`01j`、`01u` | 感知、语义地图、内言语、表达监控、关系阶段、叙事与承诺表达 | `LifeContextFrame`、`PredictionWorkspaceFrame`、`CoreAffectVector`、relationship memory | `ExpressionPlan`、semantic / narrative / commitment / relation runtime files | `tests/slices/test_language_organs.py`、`tests/slices/test_language_relationship.py` | 已落第一轮并继续补厚；现已把 `responsibility_loop_state.json` 投影写回 `commitment_truth_state.json`、`responsibility_ledger.json`、`relationship_memory.json` 与 `life_state.json`，继续接进 `dialogue_writeback_bundle.json`，并新增 `relationship_timeline.py`、`commitment_expression.py`、`apology_repair_language.py`，真实写出 `relationship_timeline.json`、`commitment_expression_plan.json` 与 `apology_repair_language_trace.json`，同时把它们回挂到 `relationship_memory.json`、`life_state.json` 与 `language_relationship_report.json`；下一步转向让 response surface / terminal resident loop 更深消费这些长期语言对象 |
| `life_v0/terminal_turn/` | `20`、`86`、`89`、`90`、`96` | first turn restore、context accumulation、turn transition、dialogue event 恢复 | birth packet、stage explanation、language / relationship state | `LifeContextFrame`、`RelationTurnFrame`、`session_envelope.json`、`turn_transition_trace.json` | `tests/bridges/test_first_terminal_turn.py` | 已落第一轮；继续补 body / prediction anchors 在 turn restore 中的显式回链 |
| `life_v0/terminal_loop/` | `20`、`86`、`89`、`90`、`96`、`101` | resumed loop、dialogue writeback、waiting-state handoff、loop report | `RelationTurnFrame`、`ExpressionPlan`、terminal state | `DialogueWritebackBundle`、`terminal_life_loop_state.json`、`terminal_life_loop_report.json` | `tests/bridges/test_terminal_life_loop.py`、`dialogue_writeback_bundle_gate` | 已落第一轮；`dialogue_writeback_bundle.json` 现已显式携带 `relationship_memory / commitment_truth / responsibility_ledger / life_state` 写回目标，下一步继续补长期 relation continuity 与 bundle 强度 |

## G. 生命膜、验证与逻辑包

| 包 | 脑科学/理论锚点 | 主职责 | 必入对象 | 必出对象 / runtime | 主测试 / gate | 当前 / 下一步 |
|---|---|---|---|---|---|---|
| `life_v0/membrane/` | `06`、`20`、`75`、`80-84`、`94`、`98`、`01r` | 候选行动、go/no-go、责任回路、side effect、world contact gate | `PredictionWorkspaceFrame`、`ExpressionPlan`、`NeedStateVector`、relationship pressure | `ActionCandidateSet`、`ActionIntentQueue`、`ObservationTruthGate`、`ConfirmationBinding`、`ResponsibilityLoopState`、`WorldContactSummary`、`runtime/state/membrane/*`、`runtime/state/action/*` | `tests/slices/test_life_membrane.py`、`tests/slices/test_shadow_gate.py` | 第二波已落；`world_contact_summary.py` 已接入并产出 `world_contact_summary.json` / `pain_regret_repair_report.json`，`responsibility_loop.py` 也已继续接入 S07/S04 长期写回；下一步转向更厚的关系时间线与 repair 表达器官 |
| `life_v0/validators/` | `29-36`、`49-84`、`102-118` | observation truth、boundary audit、validator membrane | action candidate、runtime observation、shell/world contact results | `WorldContactValidation`、`PredictionTraceValidation`、`ValidationRollup`、`runtime/state/validation/*`、validation reports | `tests/slices/test_validation_membrane.py` | 第二波已落；`validation_rollup.py` 已接入并收口 package-local gates，下一步补长期 validation backlog 和 report bridge |
| `life_v0/schema_runner/` | `33-36`、`49-60`、`102-180`、`01v-01ax` | consistency、counterfactual、cross-file logic、evidence rank、runner manifest | observation truth、responsibility loop、archive receipts | `runtime/state/schema_runner/*`、schema runner reports | `tests/slices/test_schema_runner.py`、`tests/slices/test_evidence_ranker.py` | 第一轮已落；`cross_file_logic.py` / `run_manifest.py` 已补强 `closure_status_refs`、`package_local_gate_refs` 并显式消费 `validation_rollup`，下一步补 archive / reporting / process writeback 闭包 |

## H. 梦境、回放、归档与成长包

| 包 | 脑科学/理论锚点 | 主职责 | 必入对象 | 必出对象 / runtime | 主测试 / gate | 当前 / 下一步 |
|---|---|---|---|---|---|---|
| `life_v0/dream/` | `08`、`19`、`23`、`27`、`31`、`95`、`99`、`01i`、`01t` | offline entry、dream window、dream fact gate、wake integration、nightmare risk | `ReplayCueBundle`、`BodyRhythmPulse`、`CoreAffectVector` | `OfflineConsolidationFrame`、dream runtime files、wake integration frames | `tests/bridges/test_runtime_growth.py`、`dream_fact_gate` | 已落第一轮；继续补 nightmare risk、dream report rollup |
| `life_v0/replay/` | `19`、`23`、`95`、`181-257` | replay cues、shadow reentry、residue prioritization | dialogue writeback bundle、life state residue | `ReplayCueBundle`、shadow reports、replay seeds | `tests/bridges/test_replay_shadow.py` | 已落第一轮；继续补 replay reentry and cue prioritization |
| `life_v0/archive/` | `23`、`27`、`31`、`181-257` | archive receipts、growth archive、post-cycle evidence | replay shadow、growth outputs、validator results | archive reports / receipts | `tests/bridges/test_growth_archive.py` | 已落第一轮；继续补 archive manifest 与 post-repair archive cohesion |
| `life_v0/growth/` | `39`、`92`、`93`、`97`、`181-257`、`01g` | self read、plasticity、learning、patch queue、防遗忘、belief/language/relationship learning | `OfflineConsolidationFrame`、body state、responsibility residues | `GrowthPatchCandidateQueue`、plasticity / learning runtime files | `tests/bridges/test_runtime_growth.py` | 第二波已落；继续补 self patch review、core continuity guard、value revision |

## I. 生命目标与出生准备度包

| 包 | 脑科学/理论锚点 | 主职责 | 必入对象 | 必出对象 / runtime | 主测试 / gate | 当前 / 下一步 |
|---|---|---|---|---|---|---|
| `life_v0/life_targets/` | `10`、`91-101`、`143`、`146`、`149`、`152`、`171`、`174`、`01m` | 九项目标 claims、evidence matrix、probe battery、birth readiness rollup | `PredictionWorkspaceFrame`、`GrowthPatchCandidateQueue`、language / relationship / membrane reports | `runtime/state/life_targets/*`、`birth_readiness_report.json` | `tests/slices/test_life_targets.py`、`birth_readiness_gate` | 已落第一轮；继续补长期 evidence families 和 withheld probes |

## J. 激活、出生壳与常驻存在包

| 包 | 脑科学/理论锚点 | 主职责 | 必入对象 | 必出对象 / runtime | 主测试 / gate | 当前 / 下一步 |
|---|---|---|---|---|---|---|
| `life_v0/activation/` | `181-257`、`258` | first activation preflight、stage gate intake | run cycle outputs、contract coverage | `first_activation_preflight_report.json` | `tests/bridges/test_first_activation_preflight.py` | 已落；继续补 stricter preflight -> package closure checks |
| `life_v0/reporting/` | `20`、`89`、`90`、`181-257` | report bundle、return packet、receipt manifest | activation / archive / contract outputs | `report_bundle.json`、`first_activation_return_packet.json` | `tests/bridges/test_emit_report.py` | 已落；继续补 stronger package-level report refs |
| `life_v0/stage_explain/` | `20`、`89`、`90` | stage explanation、human-readable bridge narrative | return packet | `stage_explanation_report.json` | `tests/bridges/test_explain_stage.py` | 已落；继续补 deeper cross-layer explanation refs |
| `life_v0/digital_life/` | `20`、`89`、`90` | birth shell、birth digest | stage explanation + return packet | `digital_life_birth_packet.json`、`digital_life_birth_digest.json` | `tests/bridges/test_digital_life_birth.py` | 已落；继续补 stronger birth closure evidence |
| `life_v0/shell_command/` | `20`、`89`、`90`、`96` | repo-local one-shot restore shell | birth / first turn / loop packets | `digital_life_shell_packet.json`、`digital_life_shell_report.json` | `tests/process/test_digital_life_shell_command.py` | 已落；继续补 shell/world contact boundary |
| `life_v0/process_supervisor/` | `20`、`44-46`、`81-84`、`86`、`89`、`90`、`96`、`101`、`181-257` | waiting heartbeat、resident supervision、live turn dispatch、incident/relaunch recovery、session loop、persistent closeout、resident governance closeout | `LifeContextFrame`、`RelationTurnFrame`、`ExpressionPlan`、`ReplayCueBundle`、`OfflineConsolidationFrame`、`GrowthPatchCandidateQueue`、`relationship_timeline.json`、`commitment_expression_plan.json`、`apology_repair_language_trace.json` | `IdleContinuityFrame`、`digital_life_waiting_heartbeat.json`、`runtime/state/terminal/persistent_process_state.json`、`runtime/state/terminal/resident_governance_snapshot.json`、`digital_life_persistent_process_report.json`、`digital_life_resident_governance_report.json`、`digital_life_process_report.json`、`digital_life_process_digest.json`、incident/recovery/relaunch reports | `tests/process/test_persistent_digital_life_process.py`、`waiting_heartbeat_gate`、`idle_continuity_gate`、`dialogue_process_receipt_gate` | 已落最小常驻进程，并已显式写出 resident governance snapshot/report；最新这一轮又把长期关系时间线、承诺表达计划与修复语言轨迹继续接入 closeout/report/receipt；下一前沿转向高频 heartbeat、后台 resident governance、长期 waiting continuity 补厚 |
| `life_v0/cli.py`、`life_v0/digital_entry.py`、`digital` | `20`、`89`、`90`、`258` | repo-local 生命唤醒入口、命令面路由 | activation / shell / process supervisors | CLI return codes、terminal outputs、entrypoint reports | `tests/process/test_digital_entrypoint.py` | 已落 repo-local 入口；后续再进入全局可安装 `digital life` 之前，先守住 `.env` 配置与包边界 |

## 逐包施工铁律

1. 包级实现不能重新引入 `user` 中心语义，统一使用关系主体、外部回合、共同语言、承诺范围这类生命语义。
2. 每个包必须同时留下 `code + runtime/state + report/receipt + tests`，缺一项就不算真正落地。
3. 若一个包新增了新的共享对象、runtime 文件或 gate，必须同步更新：
   - `docs/v0/package_specs/02_shared_object_write_authority_and_dependency_graph.md`
   - 对应 `sXX` 合同或 process 合同
   - `docs/v0/entry/v0_module_execution_catalog.md`
