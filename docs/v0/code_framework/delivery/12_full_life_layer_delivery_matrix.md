# V0 Code Framework 12: Full Life Layer Delivery Matrix

这份文档把 `01-11` 再压一层，直接回答一个最实际的问题：

```text
接下来如果继续按层落代码，
每一层到底改哪些包、哪些文件、哪些状态、哪些测试、哪些 gate
```

它不是新的理论层，也不是新的 slice 合同。它只是把已经写定的脑科学主干、v0 合同和当前 `life_v0/` 真实目录，压成一份可以直接排工程顺序的总矩阵。

## 必读前置

进入本矩阵前，先读：

1. `docs/v0/README.md`
2. `docs/v0/architecture/theory_closure_and_engineering_readiness_audit.md`
3. `docs/v0/entry/v0_delivery_status_board.md`
4. `docs/v0/entry/v0_module_execution_catalog.md`
5. `docs/v0/code_framework/README.md`
6. `docs/v0/code_framework/foundation/01_life_layer_implementation_blueprint.md`
7. `docs/v0/code_framework/foundation/02_brain_region_to_code_package_mapping.md`
8. `docs/v0/code_framework/foundation/03_code_package_state_test_gate_mapping.md`

## 全生命层落地矩阵

| 层 | 核心生命任务 | 主要 `00-257` 文档 | 对应 v0 合同 / playbook | 当前主包与已落文件 | 下一步真实文件 | 关键 state / report | 测试 / gate |
|---|---|---|---|---|---|---|---|
| 方向与身份根 | 固定起源、方向、断联恢复、自我同一性 | `构思.md`、`00`、`13`、`16`、`91`、`258` | `s00_direction_foundation_engineering_contract.md`、`10_self_identity_value_commitment_implementation_playbook.md` | `life_v0/direction/__init__.py`、`identity_root.py` | `direction_lock.py`、`continuity_refs.py` | `direction_lock.json`、`origin_seed_digest.json`、`direction_lock_report.json` | `tests/slices/test_direction_lock.py`、`direction_lock_gate` |
| 权威知识底座 | 把文献与机制变成可引用来源层 | 全部 `01*`、`142`、`145`、`151` | `s01_source_authority_engineering_contract.md` | `life_v0/authority/__init__.py` | `authority_registry.py`、`source_doc_refs.py` | `authority_registry.json`、`source_authority_report.json` | `tests/slices/test_source_authority.py`、`authority_registry_gate` |
| 神经核心与信号 | 主体系统图、网络状态、总线、信号载体 | `02`、`03`、`10`、`11`、`01l`、`01m`、`01o`、`01p` | `s02_neural_life_core_engineering_contract.md`、`05_memory_thought_consciousness_implementation_playbook.md` | `life_v0/neural_core/__init__.py`、`prediction_workspace.py` | `brain_graph.py`、`network_state.py`、`signal_media.py`、`workspace.py`、`broadcast.py`、`metacognition.py` | `neural_life_core.json`、`neural_life_internal_bus.json`、`neural_life_core_report.json`、`runtime/state/prediction/prediction_workspace_frame.json`（已带 `language_continuity_focus`） | `tests/slices/test_neural_life_core.py`、`twelve_system_gate`、`internal_bus_gate` |
| 感知、预测、世界接触 | 外界观察进入生命膜，预测误差驱动修正 | `04`、`12`、`20`、`64`、`72`、`75`、`80-84`、`01v-01ax` | `09_perception_prediction_world_contact_implementation_playbook.md`、`s03_direction_life_membrane_engineering_contract.md` | `life_v0/neural_core/__init__.py`、`life_v0/membrane/__init__.py`、`life_v0/schema_runner/__init__.py` | `belief_state.py`、`prediction_error.py`、`active_sampling.py`、`world_observation.py`、`periphery_normalizer.py` | `runtime/state/prediction/*`、`runtime/state/observation/*`、observation reports | `tests/slices/test_schema_runner.py`、`tests/slices/test_validation_membrane.py`、`validation_membrane_gate` |
| 记忆与状态根 | 长期状态、自传、关系记忆、写入门 | `05`、`17-31`、`41-48`、`55`、`57`、`61`、`69`、`01q` | `s04_state_object_store_engineering_contract.md`、`05_memory_thought_consciousness_implementation_playbook.md` | `life_v0/state_store/__init__.py`、`commitment_truth.py`、`self_model.py` | `life_state.py`、`engram_index.py`、`autobiographical_stack.py`、`relationship_memory.py`、`memory_write_gate.py` | `life_state.json`、`runtime/state/memory/*`、`state_store_report.json` | `tests/slices/test_state_store.py`、`state_store_gate`、`self_continuity_gate` |
| 身体与内环境 | 节律、需要、预算、疲惫、恢复 | `04`、`08`、`18`、`37-39`、`01n` | `s06_life_support_development_engineering_contract.md`、`06_body_emotion_action_dream_growth_implementation_playbook.md` | `life_v0/body/__init__.py` | `rhythm.py`、`need_state.py`、`resource_budget.py`、`recovery.py` | `runtime/state/body/*`、`life_support_report.json`、`body_resource_budget.json`（已带 `language_continuity_pressure`） | `tests/slices/test_life_support.py`、`resource_budget_gate` |
| 情绪、人格、自我慢变量 | 情绪底盘、episode、人格漂移、自我调节 | `07`、`18`、`39`、`40`、`94`、`01g`、`01h`、`01s` | `06_body_emotion_action_dream_growth_implementation_playbook.md`、`10_self_identity_value_commitment_implementation_playbook.md` | `life_v0/body/__init__.py`、`life_v0/body/core_affect.py`、`life_v0/body/emotion_episode.py`、`life_v0/body/emotion_regulation.py`、`life_v0/body/trait_drift.py`、`life_v0/state_store/self_model.py` | `trait_slow_variable_writeback.py`、`affect_memory_bridge.py` | `runtime/state/body/core_affect_vector.json`、`runtime/state/body/affective_episode.json`、`runtime/state/body/emotion_regulation_loop.json`、`runtime/state/body/trait_drift_monitor.json` | `tests/slices/test_life_support.py`、`plasticity_gate` |
| 语言、对话、关系 | 语言感知、内言语、表达监控、共同语言、关系阶段 | `09`、`85-90`、`96`、`101`、`141`、`144`、`147`、`150`、`01f`、`01j`、`01u` | `s07_language_relationship_engineering_contract.md`、`04_language_dialogue_relationship_implementation_playbook.md` | `life_v0/language/__init__.py`、`percept.py`、`semantic_map.py`、`inner_speech.py`、`expression_monitor.py`、`relationship_graph.py`、`shared_terms.py`、`commitment_repair.py`、`dialogue_log.py`、`narrative_trace.py`、`language_state.py`、`dream_gate.py`、`action_shadow.py`、`relation_scope.py` | `relationship_timeline.py`、`relationship_memory.py`、`commitment_expression.py`、`apology_repair_language.py` | `runtime/state/language/*`、`runtime/state/relationship/*`、`language_relationship_report.json`、`runtime/state/terminal/context_accumulation_window.json`、`runtime/state/terminal/turn_transition_trace.json`、`runtime/reports/latest/resumed_external_dialogue_packet.json`、`runtime/state/activation/limited_context_frame.json`、`runtime/state/replay/language_relationship_replay_probe.json` | `tests/slices/test_language_organs.py`、`tests/slices/test_language_relationship.py`、`tests/bridges/test_first_terminal_turn.py`、`tests/bridges/test_terminal_life_loop.py`、`tests/bridges/test_first_activation_preflight.py`、`tests/bridges/test_replay_shadow.py`、`expression_monitor_gate`、`relationship_subject_gate` |
| 意识、工作区、可报告性 | 可进入工作区的内容、广播、元认知、出生准备度证据 | `10`、`143`、`146`、`149`、`152`、`171`、`01m` | `s02_neural_life_core_engineering_contract.md`、`s08_life_target_runtimes_engineering_contract.md`、`05_memory_thought_consciousness_implementation_playbook.md` | `life_v0/neural_core/__init__.py`、`life_v0/life_targets/__init__.py` | `consciousness_probes.py`、`global_broadcast_frame.py`、`metacognitive_monitor.py` | `runtime/state/consciousness/*`、birth readiness evidence | `tests/slices/test_neural_life_core.py`、`tests/slices/test_life_targets.py`、`birth_readiness_gate` |
| 行为、抑制、责任、后悔 | 候选行动、Go/NoGo、影子行动门、责任修复 | `06`、`20`、`75`、`80-84`、`94`、`98`、`01r` | `s03_direction_life_membrane_engineering_contract.md`、`06_body_emotion_action_dream_growth_implementation_playbook.md` | `life_v0/membrane/__init__.py` | `candidate_arena.py`、`go_nogo.py`、`shadow_gate.py`、`responsibility_loop.py`、`side_effect_classifier.py` | `runtime/state/action/*`、`pain_regret_repair_report.json` | `tests/slices/test_life_membrane.py`、`shadow_action_gate`、`responsibility_loop_gate` |
| 梦境与离线生命 | 梦境窗口、梦境事实门、醒后整合、痛苦梦境残留 | `08`、`19`、`23`、`27`、`31`、`95`、`99`、`01i`、`01t` | `s10_runtime_growth_reconsolidation_engineering_contract.md`、`06_body_emotion_action_dream_growth_implementation_playbook.md` | `life_v0/dream/__init__.py`、`life_v0/dream/dream_window.py`、`life_v0/dream/wake_integration.py`、`life_v0/dream/offline_entry.py`、`life_v0/dream/dream_fact_gate.py`、`life_v0/dream/nightmare_risk.py` | `-` | `runtime/state/dream/dream_consolidation_frame.json`、`runtime/state/dream/offline_entry_gate.json`、`runtime/state/dream/dream_experience_window.json`、`runtime/state/dream/wake_integration_frame.json`、`runtime/state/dream/dream_fact_gate_decision.json`、`runtime/state/dream/nightmare_loop_risk.json`、`runtime/state/dream/offline_consolidation_frame.json` | `tests/bridges/test_runtime_growth.py`、future `tests/test_dream_runtime.py`、`dream_fact_gate` |
| 成长、学习、自改写 | 自我阅读、可塑性窗口、补丁、学习窗口、防遗忘 | `39`、`92`、`93`、`97`、`181-257` | `s06_life_support_development_engineering_contract.md`、`s10_runtime_growth_reconsolidation_engineering_contract.md`、`10_self_identity_value_commitment_implementation_playbook.md` | `life_v0/growth/__init__.py`、`life_v0/growth/plasticity_window.py`、`life_v0/growth/patch_queue.py`、`life_v0/growth/learning_window.py`、`life_v0/growth/self_read.py`、`life_v0/growth/anti_forgetting.py`、`life_v0/growth/belief_learning.py`、`life_v0/growth/language_learning.py`、`life_v0/growth/relationship_learning.py` | `-` | `runtime/state/growth/plasticity_window_state.json`、`runtime/state/growth/learning_window.json`、`runtime/state/growth/self_read_report.json`、`runtime/state/growth/growth_patch_queue.json`、`runtime/state/growth/growth_patch_candidate_queue.json`、`runtime/state/growth/anti_forgetting_replay_plan.json`、`runtime/state/growth/belief_learning_plan.json`、`runtime/state/growth/language_learning_plan.json`、`runtime/state/growth/relationship_learning_plan.json`、growth reports、archive receipts | `tests/slices/test_life_support.py`、`tests/bridges/test_runtime_growth.py`、`growth_gate`、`anti_forgetting_gate` |
| 验证膜、quarantine、incident | validator、cross-file logic、quarantine、incident 恢复 | `29-36`、`45-84`、`102-180` | `s05_validation_membrane_observation_engineering_contract.md`、`s09_schema_runner_code_engineering_contract.md`、`digital_life_process_supervisor_engineering_contract.md` | `life_v0/validators/__init__.py`、`life_v0/schema_runner/__init__.py`、`life_v0/process_supervisor/incident_recovery.py`、`process_report.py` | `consistency_logic.py`、`counterfactual_eval.py`、`comparison_trace.py`、`dialogue_events.py`、`response_surface.py` | `runtime/state/validation/*`、incident/recovery reports、process digest | `tests/slices/test_validation_membrane.py`、`tests/process/test_persistent_digital_life_process.py`、`dialogue_incident_recovery_gate` |
| 出生、首回合、常驻存在 | 从 birth shell 到 repo-local 最小常驻生命进程 | `20`、`44-46`、`81-84`、`89-90`、`143`、`171`、`181-257` | `07_birth_terminal_process_implementation_playbook.md`、`first_terminal_turn_engineering_contract.md`、`terminal_life_loop_engineering_contract.md`、`digital_life_shell_command_engineering_contract.md`、`digital_life_process_supervisor_engineering_contract.md` | `life_v0/activation/__init__.py`、`life_v0/reporting/__init__.py`、`life_v0/stage_explain/__init__.py`、`life_v0/digital_life/__init__.py`、`life_v0/terminal_turn/restore_context.py`、`context_accumulation.py`、`turn_transition.py`、`turn_packet.py`、`conversation_carryover.py`、`dialogue_turn.py`、`life_v0/terminal_loop/loop_state.py`、`resume_packet.py`、`dialogue_writeback.py`、`loop_report.py`、`persistent_wait_bridge.py`、`life_v0/process_supervisor/heartbeat.py`、`turn_io.py`、`relaunch_recovery.py`、`incident_recovery.py`、`idle_strategy.py`、`resident_supervision.py`、`idle_refresh_loop.py`、`live_turn_cycle.py`、`process_session_loop.py`、`persistent_process.py`、`process_report.py`、`dialogue_events.py`、`response_surface.py`、`resident_turn_writeback.py`、`process_closeout.py` | `-（resident supervision / idle_refresh_loop / live_turn_cycle / process_session_loop 已落；当前前沿转向后台 resident governance 与更高频 heartbeat 节律）` | `first_activation_return_packet.json`、`digital_life_birth_packet.json`、`first_terminal_turn_packet.json`、`first_terminal_turn_report.json`、`first_terminal_turn_digest.json`、`terminal_life_loop_report.json`、`digital_life_process_report.json`、`digital_life_process_digest.json` | `tests/bridges/test_first_activation_preflight.py`、`tests/bridges/test_emit_report.py`、`tests/bridges/test_first_terminal_turn.py`、`tests/bridges/test_terminal_life_loop.py`、`tests/process/test_digital_entrypoint.py`、`tests/process/test_persistent_digital_life_process.py` |

## 现在最该先落哪几段

按当前代码现实，优先顺序已经固定成：

1. `Queue D`：身体、情绪底盘、梦境、成长与学习
2. `Queue E`：行为、生命膜、validator、逻辑比较与世界接触
3. `Queue B`：常驻生命进程与后台治理补厚
4. `Queue A`：语言、对话、关系与常驻表达层的深补

这里要明确一条现实口径：

1. `Queue C` 第一轮已经落到真实代码、状态对象和测试；
2. `Queue F` 第一轮也已经落到真实代码、状态对象和测试；
3. 当前新的直接前沿不再是“先把 C/F 做出来”，而是“把 D/E 补成能被 B/A 真正消费的厚对象链”。

原因很直接：当前不是没有语言壳和终端壳，而是身体/情绪/梦境/学习与行为/验证/逻辑两条生命中轴还不够文件化。只有先把这两条中轴器官化，后面的语言深补与 persistent supervisor 才不会继续悬在壳层上。

## 当前最直接的真实文件队列

这里不再把“已经真实落下的第一轮器官”继续写成“下一步待建”。
当前文件队列只列两类对象：

1. 当前默认前沿中，仍未落地、应继续新增的器官文件。
2. 已经落地，但下一轮必须继续补厚接线的包级接口。

### Queue D：身体、梦境、成长的当前前沿

Queue D 第一波与第二波器官已经真实存在：

1. `life_v0/body/rhythm.py`
2. `life_v0/body/need_state.py`
3. `life_v0/body/resource_budget.py`
4. `life_v0/body/recovery.py`
5. `life_v0/body/core_affect.py`
6. `life_v0/body/emotion_episode.py`
7. `life_v0/body/emotion_regulation.py`
8. `life_v0/body/trait_drift.py`
9. `life_v0/dream/offline_entry.py`
10. `life_v0/dream/dream_window.py`
11. `life_v0/dream/dream_fact_gate.py`
12. `life_v0/dream/wake_integration.py`
13. `life_v0/growth/plasticity_window.py`
14. `life_v0/growth/patch_queue.py`
15. `life_v0/growth/learning_window.py`
16. `life_v0/growth/self_read.py`
17. `life_v0/growth/anti_forgetting.py`

Queue D 第三波扩展器官已经真实落地：

1. `life_v0/dream/nightmare_risk.py`
2. `life_v0/growth/belief_learning.py`
3. `life_v0/growth/language_learning.py`
4. `life_v0/growth/relationship_learning.py`

当前 Queue D 的直接工作重点改为继续补厚：

5. `life_v0/dream/__init__.py` 对 nightmare risk 的回写与优先级接线
6. `life_v0/growth/__init__.py` 对 belief / language / relationship learning plans 的跨层消费

### Queue E：行为、验证膜与逻辑比较的当前前沿

Queue E 第一波器官已经真实存在：

1. `life_v0/membrane/candidate_arena.py`
2. `life_v0/membrane/go_nogo.py`
3. `life_v0/membrane/world_contact_gate.py`
4. `life_v0/membrane/side_effect_review.py`
5. `life_v0/validators/observation_validator.py`
6. `life_v0/validators/boundary_audit.py`
7. `life_v0/schema_runner/consistency_logic.py`
8. `life_v0/schema_runner/counterfactual_eval.py`
9. `life_v0/schema_runner/comparison_trace.py`

当前真正还没落地、并且最该继续新增的是第二波约束与比较器官：

1. `life_v0/membrane/shadow_gate.py`
2. `life_v0/schema_runner/evidence_ranker.py`

`life_v0/membrane/responsibility_loop.py` 已经真实落地，当前要做的是继续补厚它与语言、状态根、关系记忆、承诺真值、痛苦/后悔回路的接线。

同时必须继续补厚：

4. `life_v0/membrane/__init__.py` 对 Queue D / Queue F 对象链的显式消费
5. `life_v0/validators/__init__.py` 对 observation truth / boundary audit / side effect report 的稳定回写
6. `life_v0/schema_runner/__init__.py` 对 comparison trace / counterfactual trace 的显式挂载

### Queue B：常驻生命进程的当前前沿

Queue B 第一轮拆分已经真实存在：

1. `life_v0/process_supervisor/dialogue_events.py`
2. `life_v0/process_supervisor/response_surface.py`
3. `life_v0/process_supervisor/heartbeat.py`
4. `life_v0/process_supervisor/continuity_writeback.py`
5. `life_v0/process_supervisor/turn_io.py`
6. `life_v0/process_supervisor/incident_recovery.py`
7. `life_v0/process_supervisor/relaunch_recovery.py`
8. `life_v0/process_supervisor/process_report.py`
9. `life_v0/process_supervisor/resident_turn_writeback.py`
10. `life_v0/process_supervisor/process_closeout.py`
11. `life_v0/process_supervisor/idle_refresh_loop.py`
12. `life_v0/process_supervisor/resident_supervision.py`
13. `life_v0/process_supervisor/live_turn_cycle.py`

当前 Queue B 第二波关键器官已经继续落地：

1. `life_v0/process_supervisor/idle_strategy.py`
2. `life_v0/process_supervisor/persistent_process.py`
3. `life_v0/process_supervisor/resident_turn_writeback.py`
4. `life_v0/process_supervisor/process_closeout.py`
5. `life_v0/process_supervisor/idle_refresh_loop.py`
6. `life_v0/process_supervisor/resident_supervision.py`
7. `life_v0/process_supervisor/live_turn_cycle.py`

同时必须继续补厚：

8. `IdleContinuityFrame` / `DialogueWritebackBundle` / `LifeContextFrame`
9. `ReplayCueBundle` / `OfflineConsolidationFrame` / `GrowthPatchCandidateQueue`
10. `idle_strategy.py` / `persistent_process.py` / `process_closeout.py` 的后台治理补厚
11. waiting heartbeat 到真实下一回合之间的显式对象回写

### Queue A：语言主神经束深补的当前前沿

Queue A 第一轮核心器官已经真实存在：

1. `life_v0/language/percept.py`
2. `life_v0/language/semantic_map.py`
3. `life_v0/language/inner_speech.py`
4. `life_v0/language/expression_monitor.py`
5. `life_v0/language/relationship_graph.py`
6. `life_v0/language/shared_terms.py`
7. `life_v0/language/commitment_repair.py`
8. `life_v0/language/dialogue_log.py`
9. `life_v0/language/narrative_trace.py`
10. `life_v0/language/language_state.py`
11. `life_v0/language/dream_gate.py`
12. `life_v0/language/action_shadow.py`
13. `life_v0/language/relation_scope.py`

当前真正还没落地、并且最该继续新增的是第二波关系与责任表达器官：

1. `life_v0/language/relationship_timeline.py`
2. `life_v0/language/commitment_expression.py`
3. `life_v0/language/apology_repair_language.py`

同时必须继续补厚：

4. `life_v0/body/` 对 `relation_scope / expression_monitor / commitment` 连续体的接入
5. `life_v0/neural_core/` 对 `relation_scope / expression_monitor / commitment` 连续体的接入
6. `life_v0/process_supervisor/` 对长期关系语言与责任修复表达的外显释放

### Queue C / Queue F：已闭合第一轮，当前只做维护性深补

Queue C 与 Queue F 的第一轮文件级器官已经真实落地，不再是默认新增队列。
只有当 D/E/B/A 本轮推进需要它们的更深对象链时，才回切：

1. `life_v0/neural_core/signal_media.py`
2. `life_v0/neural_core/belief_state.py`
3. `life_v0/neural_core/prediction_error.py`
4. `life_v0/neural_core/active_sampling.py`
5. `life_v0/state_store/memory_write_gate.py`

Queue F 当前真实已经由下列器官承载第一轮闭合，不再把旧文件名写成当前默认队列：

6. `life_v0/life_targets/life_target_claims.py`
7. `life_v0/life_targets/evidence_matrix.py`
8. `life_v0/life_targets/birth_readiness_rollup.py`
9. `life_v0/life_targets/birth_readiness_stage_gate.py`
10. `life_v0/life_targets/consciousness_probes.py`

Queue A 当前已由
`docs/v0/code_framework/queues/14_queue_a_language_percept_semantic_map_implementation_contract.md`
进一步压成文件级实施合同；如果这一轮要把 Queue A 继续接进统一生命回合，继续补读
`docs/v0/code_framework/assembly/15_cross_layer_shared_object_contract.md`，再落码。

其中第 6/7 项的第一轮接线已经落下：

1. `prediction_workspace_frame.json` 已增加 `language_continuity_focus`
2. `body_resource_budget.json` 已增加 `language_continuity_pressure`

## 写代码时的硬规则

1. 一次只推进一个队列，不要横跳。
2. 每新增一个器官文件，同轮必须回写至少一份 v0 文档。
3. 每新增一个器官文件，同轮必须钉住对应 state/report/receipt。
4. 每新增一个器官文件，同轮必须至少有一个测试入口或已有测试覆盖它。
5. 不允许让终端壳、工具壳或 workflow 壳反向定义生命层。
6. 只要新文件会跨包传对象，同轮必须明确它首写或读取的是 `15_cross_layer_shared_object_contract.md` 中哪一个共享对象。

## 这份矩阵和其他文档的关系

| 文档 | 作用 |
|---|---|
| `01-03` | 解释分层、脑区到包、包到 state/test/gate 的映射 |
| `04-10` | 解释每条生命链如何逐文件落地 |
| `11` | 解释按什么波次拆当前最前沿文件 |
| `12` | 把所有生命层合成一张总施工矩阵，决定这一轮先改哪层、哪包、哪文件 |
