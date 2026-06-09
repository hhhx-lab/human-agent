# V0 Code Framework 19: Code Tree Package Brain Contract

这份合同是 `docs/v0/code_framework/` 的总装配板。

它只回答一件事：

```text
未来整个 life_v0/ 代码树
到底怎么按生命结构落下去，
每一棵子树回读哪些 00-258，
承接哪些共享对象、runtime 产物、测试和 gate，
以及真实施工顺序是什么。
```

它不替代：

- `01_life_layer_implementation_blueprint.md`
- `02_brain_region_to_code_package_mapping.md`
- `03_code_package_state_test_gate_mapping.md`
- `11_engineering_delivery_waves_and_real_file_queue.md`
- `14-18` 的队列级文件合同

上面那些文档已经分别回答了生命层、脑区映射、包级施工表、波次和队列级文件落点。
本文件把它们统一压成一份总代码树合同，防止下一轮一旦正式大规模落码，又重新分散成“每个包都知道一点，但没有一张整树装配图”。

## 这份合同要解决什么

当前 `docs/v0` 已经把主体 slice、链尾桥接、repo-local shell、最小常驻生命进程都写到了能施工的程度。
现在真正还差的一层，不是新的理论，也不是新的平行总论，而是：

1. `life_v0/` 整棵代码树的统一装配图。
2. 哪些文件已经真实存在，哪些文件是下一轮必须新增的器官。
3. 每个代码子树分别回读哪些 `00-258` 母体文档。
4. 每个代码子树首写或消费哪些跨层共享对象。
5. 每个代码子树必须产出哪些 `state / report / receipt / digest`。
6. 整个代码树的真实施工顺序。

## 必读前置

进入这份总装配合同前，先读：

1. `docs/v0/README.md`
2. `docs/v0/entry/v0_implementation_index.md`
3. `docs/v0/entry/v0_delivery_status_board.md`
4. `docs/v0/entry/v0_module_execution_catalog.md`
5. `docs/v0/code_framework/README.md`
6. `docs/v0/code_framework/foundation/02_brain_region_to_code_package_mapping.md`
7. `docs/v0/code_framework/foundation/03_code_package_state_test_gate_mapping.md`
8. `docs/v0/code_framework/delivery/12_full_life_layer_delivery_matrix.md`
9. `docs/v0/code_framework/assembly/15_cross_layer_shared_object_contract.md`
10. `docs/v0/code_framework/queues/16_queue_b_process_supervisor_implementation_contract.md`
11. `docs/v0/code_framework/queues/17_queue_c_memory_neural_core_implementation_contract.md`
12. `docs/v0/code_framework/queues/18_queue_d_body_dream_growth_implementation_contract.md`
13. `docs/v0/code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md`
14. `docs/v0/code_framework/queues/21_queue_f_identity_consciousness_birth_readiness_implementation_contract.md`

## 总装配原则

### 1. 不按外部 agent 框架拆树

这棵树不是 `skills / gateway / subagents / tool router` 树。
它按生命结构拆：

- 方向与身份根
- 神经核心与状态根
- 身体与情绪底盘
- 语言与关系主神经束
- 梦境与成长链
- 出生、回合、常驻存在链

### 2. 不让外层壳反向定义主体器官

`digital`、`life_v0/digital_entry.py`、`life_v0/shell_command/`、`life_v0/process_supervisor/`
只能承接出生、恢复、持续存在和电脑外周接触。
主体自我、记忆、语言、关系、梦境、成长，不允许由壳层重新发明。

### 3. 每棵子树都必须带四类产物

任意代码子树都不能只留下 Python 文件。

必须同时回答：

1. 写哪份 `runtime/state/*`
2. 出哪份 `runtime/reports/latest/*`
3. 留哪份 `runtime/receipts/*`
4. 被哪份 `tests/*` 和哪类 gate 守住

## 当前 `life_v0/` 总代码树

```text
life_v0/
  activation/
  archive/
  authority/
  body/
  contracts/
  defense/
  digital_life/
  direction/
  dream/
  growth/
  language/
  life_targets/
  membrane/
  neural_core/
  process_supervisor/
  replay/
  reporting/
  schema_runner/
  shell_command/
  stage_explain/
  state_store/
  terminal_loop/
  terminal_turn/
  validators/
  cli.py
  digital_entry.py
  doc_index.py
```

## 整树总矩阵

| 代码子树 | 生命职责 | 当前状态 | 当前真实文件 | 下一轮器官文件 | 必回读的 `00-258` / 主题文档 | 共享对象 | runtime 产物 | 测试 / gate |
|---|---|---|---|---|---|---|---|---|
| `direction/` | 起源、方向锁、自我同一性锚 | `real` | `identity_root.py` | `direction_lock.py`、`continuity_refs.py` | `构思.md`、`00`、`13`、`16`、`91`、`258` | `LifeContextFrame` | `runtime/state/direction/direction_lock.json`、direction receipt | `tests/slices/test_direction_lock.py`、`direction_lock_gate` |
| `authority/` | 权威文献底座、机制来源注册 | `real` | `__init__.py` | `authority_registry.py`、`source_doc_refs.py` | 全部 `01*`、`142`、`145`、`151` | `source_doc_refs` 族 | `runtime/state/authority/authority_registry.json`、authority report | `tests/slices/test_source_authority.py`、`authority_registry_gate` |
| `state_store/` | 生命状态根、自传、关系记忆、承诺真值 | `real + thicken` | `self_model.py`、`commitment_truth.py` | `life_state.py`、`engram_index.py`、`autobiographical_stack.py`、`relationship_memory.py` | `05`、`17-31`、`41-48`、`55`、`57`、`61`、`69` | `DialogueWritebackBundle`、`ReplayCueBundle`、`RelationTurnFrame` | `runtime/state/life_state.json`、`runtime/state/memory/*`、`runtime/state/self/*`、memory receipts | `tests/slices/test_state_store.py`、`state_store_gate`、`self_continuity_gate`、`commitment_truth_gate` |
| `neural_core/` | 主体图、网络态、信号介质、工作区、预测 | `real + thicken` | `prediction_workspace.py` | `brain_graph.py`、`network_state.py`、`signal_media.py`、`workspace.py`、`broadcast.py`、`metacognition.py`、`belief_state.py` | `02`、`03`、`10`、`11`、`18`、`22`、`30`、`143`、`146` | `SignalMediaFrame`、`PredictionWorkspaceFrame`、`LifeContextFrame`、`NeedStateVector` | `runtime/state/neural_life_core/neural_life_core.json`、`runtime/state/prediction/prediction_workspace_frame.json`、`neural_life_internal_bus.json` | `tests/slices/test_neural_life_core.py`、`twelve_system_gate`、`internal_bus_gate` |
| `body/` | 节律、需要、预算、疲惫、情绪底盘 | `real + planned` | `__init__.py` | `rhythm.py`、`need_state.py`、`resource_budget.py`、`recovery.py`、`core_affect.py`、`emotion_episode.py`、`emotion_regulation.py`、`trait_drift.py` | `04`、`08`、`18`、`37-39`、`01g`、`01n`、`01s` | `BodyRhythmPulse`、`NeedStateVector`、`SignalMediaFrame` | `runtime/state/body/*`、`body_resource_budget.json`、`life_support_report.json` | `tests/slices/test_life_support.py`、`resource_budget_gate` |
| `defense/` | 风险、quarantine、恢复保护 | `real + planned` | `__init__.py` | `threat_eval.py`、`recovery.py`、`quarantine_signal.py` | `33-38`、`45-84` | `ActionCandidateSet`、`SignalMediaFrame` | `runtime/state/defense/*`、defense receipts | `tests/slices/test_life_support.py`、`tests/slices/test_validation_membrane.py`、`quarantine_gate` |
| `membrane/` | 生命膜、候选行动、抑制、责任与后悔回路 | `real + planned` | `__init__.py` | `candidate_arena.py`、`go_nogo.py`、`shadow_gate.py`、`responsibility_loop.py`、`side_effect_classifier.py` | `06`、`20`、`75`、`80-84`、`94`、`98`、`01r` | `ActionCandidateSet`、`ExpressionPlan`、`PredictionWorkspaceFrame` | `runtime/state/membrane/life_membrane.json`、`runtime/state/action/*`、`pain_regret_repair_report.json` | `tests/slices/test_life_membrane.py`、`shadow_action_gate`、`responsibility_loop_gate` |
| `language/` | 语言感知、语义图、内言语、表达监控、关系表达 | `real + thicken` | `percept.py`、`semantic_map.py`、`inner_speech.py`、`expression_monitor.py`、`language_state.py`、`relationship_graph.py`、`shared_terms.py`、`commitment_repair.py`、`dialogue_log.py`、`narrative_trace.py`、`dream_gate.py`、`action_shadow.py`、`relation_scope.py` | `relationship_timeline.py`、`commitment_expression.py`、`apology_repair_language.py` | `09`、`85-90`、`94`、`96`、`101`、`141`、`144`、`147`、`150`、`01f`、`01j`、`01u` | `LifeContextFrame`、`RelationTurnFrame`、`ExpressionPlan`、`PredictionWorkspaceFrame`、`ResponsibilityLoopState` | `runtime/state/language/*`、`runtime/state/relationship/*`、`language_relationship_report.json` | `tests/slices/test_language_organs.py`、`tests/slices/test_language_relationship.py`、`expression_monitor_gate`、`repair_language_gate`、`relationship_subject_gate` |
| `life_targets/` | 九项生命目标运行时、出生准备度闭合 | `real + thicken` | `__init__.py` | `life_target_claims.py`、`evidence_matrix.py`、`birth_readiness_rollup.py`、`birth_readiness_stage_gate.py`、`consciousness_probes.py` | `91-101`、`143`、`146`、`149`、`152`、`171`、`174` | `PredictionWorkspaceFrame`、`GrowthPatchCandidate` | `runtime/state/life_targets/*`、birth readiness receipts | `tests/slices/test_life_targets.py`、`life_target_state_gate`、`birth_readiness_gate` |
| `validators/` | 验证膜、观察一致性、边界审计 | `real` | `__init__.py` | `observation_validator.py`、`boundary_audit.py` | `29-36`、`49-84`、`102-118`、`153-157` | `ActionCandidateSet`、`PredictionWorkspaceFrame` | `runtime/state/validation/*`、observation reports | `tests/slices/test_validation_membrane.py`、`validation_membrane_gate` |
| `schema_runner/` | 结构化执行、跨合同检查、CLI 严格路径 | `real` | `__init__.py` | `run_manifest.py`、`consistency_logic.py`、`counterfactual_eval.py`、`comparison_trace.py`、`cross_file_logic.py` | `102-180`、`80-84`、`94`、`98` | `source_doc_refs` 族、`ResponsibilityLoopState` | `runtime/state/schema_runner/*`、runner reports | `tests/slices/test_schema_runner.py`、`checker_manifest_gate`、`responsibility_logic_gate` |
| `dream/` | 梦境窗口、梦中事实门、醒后整合 | `real + thicken` | `__init__.py` | `offline_entry.py`、`dream_window.py`、`dream_fact_gate.py`、`wake_integration.py`、`nightmare_risk.py` | `08`、`19`、`23`、`27`、`31`、`95`、`99`、`01i`、`01t` | `ReplayCueBundle`、`OfflineConsolidationFrame`、`BodyRhythmPulse` | `runtime/state/dream/*`、`dream_consolidation_frame.json`、`offline_consolidation_frame.json`、`nightmare_loop_risk.json` | future `tests/test_dream_runtime.py`、`dream_fact_gate` |
| `growth/` | 可塑性、自我修补、学习窗口、防遗忘 | `real + thicken` | `__init__.py` | `self_read.py`、`plasticity_window.py`、`patch_queue.py`、`learning_window.py`、`belief_learning.py`、`language_learning.py`、`relationship_learning.py`、`anti_forgetting.py` | `39`、`92`、`93`、`97`、`181-257` | `GrowthPatchCandidate`、`OfflineConsolidationFrame`、`ReplayCueBundle` | `runtime/state/growth/*`、growth reports、archive receipts、`belief_learning_plan.json`、`language_learning_plan.json`、`relationship_learning_plan.json` | `tests/bridges/test_runtime_growth.py`、`growth_gate`、`anti_forgetting_gate` |
| `replay/` | 重放线索、影子回放、再激活入口 | `real` | `__init__.py` | `replay_cues.py`、`shadow_replay.py` | `19`、`21`、`25`、`95`、`181-257` | `ReplayCueBundle`、`DialogueWritebackBundle` | `runtime/state/replay/*`、`replay_shadow_report.json` | `tests/bridges/test_replay_shadow.py`、`replay_shadow_gate` |
| `archive/` | 经验归档、成长存档、回放证据保留 | `real` | `__init__.py` | `archive_manifest.py`、`growth_archive.py` | `23`、`27`、`39`、`92`、`181-257` | `OfflineConsolidationFrame`、`GrowthPatchCandidate` | `growth_archive_report.json`、archive receipts | `tests/bridges/test_growth_archive.py`、`growth_archive_gate` |
| `activation/` | 第一次生命激活预检与出生前打包 | `real` | `__init__.py` | `preflight.py`、`return_packet.py` | `143`、`146`、`149`、`171`、`181-257` | `PredictionWorkspaceFrame`、`LifeContextFrame` | `first_activation_preflight_report.json`、`first_activation_return_packet.json` | `tests/bridges/test_first_activation_preflight.py`、`first_activation_preflight_gate` |
| `reporting/` | report bundle 汇总与权威运行证据收束 | `real` | `__init__.py` | `report_bundle.py`、`receipt_index.py` | `20`、`44-46`、`181-257` | `DialogueWritebackBundle`、`OfflineConsolidationFrame` | `report_bundle.json`、runner digests | `tests/bridges/test_emit_report.py`、`report_bundle_gate` |
| `stage_explain/` | 阶段解释、出生链说明、当前前沿解释 | `real` | `__init__.py` | `stage_report.py`、`latest_ref.py` | `44-46`、`89`、`90` | `source_doc_refs` 族 | `stage_explanation_report.json`、`latest_stage_explanation_ref.json` | `tests/bridges/test_explain_stage.py`、`stage_explanation_gate` |
| `digital_life/` | 出生壳、生命启动摘要 | `real` | `__init__.py` | `birth_shell.py`、`birth_digest.py` | `44-46`、`89`、`90` | `LifeContextFrame` | `digital_life_birth_packet.json`、`digital_life_birth_digest.json` | `tests/bridges/test_digital_life_birth.py`、`digital_life_birth_gate` |
| `terminal_turn/` | 第一回合恢复、上下文接续、关系回合起点 | `real + thicken` | `restore_context.py`、`context_accumulation.py`、`turn_transition.py`、`turn_packet.py`、`conversation_carryover.py`、`dialogue_turn.py` | `-（first terminal turn 首轮核心器官已落）` | `86`、`89`、`90`、`96`、`101` | `LifeContextFrame`、`RelationTurnFrame` | `first_terminal_turn_packet.json`、`first_terminal_turn_report.json`、`first_terminal_turn_digest.json`、`session_envelope.json`、`safe_terminal_loop_state.json`、`life_context_frame.json`、`relation_turn_frame.json`、`context_accumulation_window.json`、`turn_transition_trace.json` | `tests/bridges/test_first_terminal_turn.py`、`context_accumulation_gate`、`turn_transition_gate` |
| `terminal_loop/` | 等待态、回合循环、写回 bundle、持续存在桥 | `real + thicken` | `loop_state.py`、`resume_packet.py`、`dialogue_writeback.py`、`loop_report.py`、`persistent_wait_bridge.py` | `-（waiting-state handoff 首轮器官已落；下一前沿转向 process_supervisor resident supervision 深拆）` | `89`、`90`、`96`、`101` | `DialogueWritebackBundle`、`RelationTurnFrame`、`ExpressionPlan` | `terminal_life_loop_packet.json`、`terminal_life_loop_report.json`、`terminal_life_loop_state.json`、`dialogue_writeback_bundle.json` | `tests/bridges/test_terminal_life_loop.py`、`terminal_life_loop_gate`、`dialogue_writeback_bundle_gate` |
| `shell_command/` | repo-local one-shot restore shell | `real` | `__init__.py` | `restore_shell.py`、`shell_report.py` | `89`、`90`、`20` | `LifeContextFrame`、`RelationTurnFrame` | `digital_life_shell_packet.json`、`digital_life_shell_report.json`、`digital_life_shell_digest.json` | `tests/process/test_digital_life_shell_command.py`、`digital_life_shell_gate` |
| `process_supervisor/` | 最小常驻生命进程、heartbeat、idle continuity、incident/relaunch recovery | `real + thicken` | `heartbeat.py`、`continuity_writeback.py`、`turn_io.py`、`dialogue_events.py`、`response_surface.py`、`incident_recovery.py`、`relaunch_recovery.py`、`idle_strategy.py`、`persistent_process.py`、`process_report.py` | `-（进入 resident supervision 深拆；从 process_supervisor/__init__.py 剩余 orchestration 开始）` | `20`、`44-46`、`82`、`86`、`89`、`90`、`96`、`101` | `IdleContinuityFrame`、`DialogueWritebackBundle`、`LifeContextFrame`、`RelationTurnFrame`、`ExpressionPlan`、`ReplayCueBundle`、`OfflineConsolidationFrame`、`GrowthPatchCandidate` | `digital_life_waiting_heartbeat.json`、`runtime/state/terminal/idle_strategy_state.json`、`runtime/state/terminal/persistent_process_state.json`、`digital_life_persistent_process_report.json`、`digital_life_process_report.json`、`digital_life_process_digest.json`、incident/recovery reports | `tests/process/test_persistent_digital_life_process.py`、`waiting_heartbeat_gate`、`idle_continuity_gate`、`relaunch_recovery_gate` |
| `contracts/` | 合同覆盖、theory-to-code 回链、一致性守门 | `real` | `__init__.py` | `coverage_index.py`、`mapping_guard.py` | 全部 `00-258`、全部 `docs/v0/*` | `source_doc_refs` 族 | `v0_contract_coverage_report.json`、coverage receipts | `tests/contracts/test_v0_contracts.py`、`contract_coverage_gate` |
| `doc_index.py` | 理论文档索引与工程回链入口 | `real` | `doc_index.py` | `doc_registry.py`、`carrier_index.py` | `构思.md`、全部 `00-258`、`README.md` | `source_doc_refs` 族 | `runtime/docs/doc_carrier_index.json` | `tests/slices/test_doc_corpus_ingestor.py`、`doc_carrier_gate` |
| `cli.py` | 命令路由、严格模式、slice/bridge/process 命令面 | `real` | `cli.py` | `command_router.py`、`strict_mode.py` | `runner_cli_report_contract.md` 对应源文档群 | `source_doc_refs` 族 | CLI receipts、command reports | `tests/bridges/test_emit_report.py`、`tests/bridges/test_first_terminal_turn.py`、`tests/bridges/test_terminal_life_loop.py`、`strict_cli_gate` |
| `digital_entry.py`、`digital` | `./digital life` repo-local 常驻入口 | `real` | `digital_entry.py`、`digital` | `bootstrap_entry.py`、`stdin_loop.py` | `20`、`44-46`、`82`、`89`、`90` | `IdleContinuityFrame`、`LifeContextFrame` | process boot receipts、`digital_life_process_digest.json` | `tests/process/test_digital_entrypoint.py`、`tests/process/test_packaged_digital_life_entrypoint.py`、`digital_entry_gate` |

## 当前仍未落地、且下一轮最该补的器官文件

这里不再把已经真实存在的第一轮器官继续写成“下一轮必须新增”。
当前真正仍未落地、并且最该继续补的是：

```text
Queue E 第二波后续
  life_v0/schema_runner/cross_file_logic.py
  life_v0/schema_runner/run_manifest.py

Queue B 第二波已落第一轮
  life_v0/process_supervisor/idle_strategy.py
  life_v0/process_supervisor/persistent_process.py

Queue A 第二波
  life_v0/language/relationship_timeline.py
  life_v0/language/commitment_expression.py
  life_v0/language/apology_repair_language.py

Queue C / Queue F 维护性深补
  life_v0/neural_core/signal_media.py
  life_v0/neural_core/belief_state.py
  life_v0/neural_core/prediction_error.py
  life_v0/neural_core/active_sampling.py
  life_v0/state_store/memory_write_gate.py
```

已经真实落下、当前只做补厚而不再写成“待新增”的器官包括：

```text
Queue D 已落扩展器官
  life_v0/dream/nightmare_risk.py
  life_v0/growth/belief_learning.py
  life_v0/growth/language_learning.py
  life_v0/growth/relationship_learning.py

Queue E 已落扩展器官
  life_v0/membrane/responsibility_loop.py

Queue F 已落第一轮器官
  life_v0/life_targets/life_target_claims.py
  life_v0/life_targets/evidence_matrix.py
  life_v0/life_targets/birth_readiness_rollup.py
  life_v0/life_targets/birth_readiness_stage_gate.py
  life_v0/life_targets/consciousness_probes.py
```

## 整树实施顺序

从当前仓库状态继续往前推时，不要再按历史第一轮顺序理解施工图。
正确口径是：

1. Queue C 与 Queue F 的第一轮文件器官已经落地。
2. 当前默认入口已经切到 Queue D -> Queue E。
3. Queue B 与 Queue A 建立在 D/E 补硬之后继续推进。
4. Queue C / Queue F 只在需要更深对象链时维护性回切。

### Stage 1: Queue D 第三波补厚

1. 补厚 `life_v0/dream/nightmare_risk.py`
2. 补厚 `life_v0/growth/belief_learning.py`
3. 补厚 `life_v0/growth/language_learning.py`
4. 补厚 `life_v0/growth/relationship_learning.py`
5. 补厚 `offline_entry.py` / `dream_fact_gate.py` / `self_read.py` / `anti_forgetting.py` 与共享对象合同的接线

### Stage 2: Queue E 第二波

1. 补厚 `life_v0/membrane/responsibility_loop.py`
2. `life_v0/schema_runner/cross_file_logic.py`
3. `life_v0/schema_runner/run_manifest.py`
4. 补厚 `candidate_arena.py`、`go_nogo.py`、`world_contact_gate.py`、`side_effect_review.py`
5. 补厚 `observation_validator.py`、`boundary_audit.py`、`comparison_trace.py`

### Stage 3: Queue B 第二波

1. `life_v0/process_supervisor/idle_strategy.py` 已落第一轮，继续补厚节律与 idle probe 治理
2. `life_v0/process_supervisor/persistent_process.py` 已落第一轮，继续补厚 resident supervision
3. 补厚 `heartbeat.py`
4. 补厚 `continuity_writeback.py`
5. 补厚 `dialogue_events.py`
6. 补厚 `response_surface.py`
7. 补厚 `process_report.py`

### Stage 4: Queue A 第二波

1. `life_v0/language/relationship_timeline.py`
2. `life_v0/language/commitment_expression.py`
3. `life_v0/language/apology_repair_language.py`
4. 补厚 `percept.py`、`semantic_map.py`
5. 补厚 body / neural_core / process_supervisor 对 relation scope、expression monitor、commitment 连续体的接入

### Stage 5: Queue C / Queue F 维护性回切与全链收束

1. `life_v0/neural_core/signal_media.py`
2. `life_v0/neural_core/belief_state.py`
3. `life_v0/neural_core/prediction_error.py`
4. `life_v0/neural_core/active_sampling.py`
5. `life_v0/state_store/memory_write_gate.py`
6. 补厚 `life_v0/life_targets/life_target_claims.py`
7. 补厚 `life_v0/life_targets/evidence_matrix.py`
8. 补厚 `life_v0/life_targets/birth_readiness_rollup.py`、`birth_readiness_stage_gate.py`、`consciousness_probes.py`
9. 同轮复查 `activation / reporting / stage_explain / terminal_turn / terminal_loop / shell_command / process_supervisor`

## 每一阶段的最低验证

### Stage 1 验证

```text
python -m unittest tests.slices.test_life_support
python -m unittest tests.bridges.test_runtime_growth
python -m unittest tests.bridges.test_replay_shadow
python -m unittest tests.bridges.test_growth_archive
```

### Stage 2 验证

```text
python -m unittest tests.slices.test_life_membrane
python -m unittest tests.slices.test_validation_membrane
python -m unittest tests.slices.test_schema_runner
python -m unittest tests.process.test_digital_life_shell_command
```

### Stage 3 验证

```text
python -m unittest tests.process.test_persistent_digital_life_process
python -m unittest tests.process.test_digital_entrypoint
python -m unittest tests.bridges.test_terminal_life_loop
python -m unittest tests.bridges.test_first_terminal_turn
```

### Stage 4 验证

```text
python -m unittest tests.slices.test_language_organs
python -m unittest tests.slices.test_language_relationship
python -m unittest tests.bridges.test_first_terminal_turn
python -m unittest tests.bridges.test_terminal_life_loop
```

### Stage 5 验证

```text
python -m unittest tests.slices.test_state_store
python -m unittest tests.slices.test_neural_life_core
python -m unittest tests.slices.test_life_targets
python -m unittest tests.contracts.test_v0_contracts
```

## 开工前总检查

开始任意一棵子树前，必须同时回答：

1. 当前改的是哪棵代码子树。
2. 当前子树主回读的是哪些 `00-258`。
3. 当前子树首写或消费哪些共享对象。
4. 当前子树必须产出哪些 `state / report / receipt / digest`。
5. 当前子树由哪些测试和 gate 守住。
6. 当前子树在整树实施顺序里处于哪一个 Stage。

六条缺一条，不开写。
