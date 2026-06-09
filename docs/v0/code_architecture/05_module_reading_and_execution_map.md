# Module Reading And Execution Map

这份文档把 v0 的主要代码包压成“开工前执行地图”。

它只回答这件事：

```text
如果下一轮要真正开始写某个主包，
在动手之前到底必须读哪些 00-257 文档、
哪些 v0 合同、
打开哪些代码入口、
确认哪些 runtime 产物、
以及最少跑哪些测试。
```

这样做的目的很简单：

1. 防止断联回来后凭感觉选模块。
2. 防止代码写着写着忘了理论来源。
3. 防止模块之间的完成标准不一样。

## 使用规则

对任意一个主包，开写前至少做五件事：

1. 读理论母体
2. 读 v0 合同
3. 打开当前代码入口
4. 确认要写的 state / report / receipt
5. 先知道写完后最低跑哪些测试

缺任一项，就不要开写。

## 主包执行地图

### `life_v0/direction/`

| 类别 | 内容 |
|---|---|
| 先读理论 | `构思.md`、`00`、`13`、`16`、`91`、`119`、`122`、`258` |
| 先读 v0 | `s00_direction_foundation_engineering_contract.md`、`10_self_identity_value_commitment_implementation_playbook.md`、`01_life_code_stack_and_package_layers.md` |
| 打开代码 | `life_v0/direction/__init__.py`、`identity_root.py`、`direction_lock.py`、`continuity_refs.py`、`value_orientation.py` |
| 确认证据 | `runtime/state/direction/*`、direction receipts |
| 最低测试 | `tests/slices/test_direction_lock.py` |

### `life_v0/authority/`

| 类别 | 内容 |
|---|---|
| 先读理论 | 全部 `01*`、`142`、`145`、`151` |
| 先读 v0 | `s01_source_authority_engineering_contract.md`、`theory_closure_and_engineering_readiness_audit.md` |
| 打开代码 | `life_v0/authority/__init__.py` |
| 确认证据 | `runtime/state/authority/*`、authority report |
| 最低测试 | `tests/slices/test_source_authority.py` |

### `life_v0/body/` 与 `life_v0/defense/`

| 类别 | 内容 |
|---|---|
| 先读理论 | `04`、`07`、`08`、`11`、`18`、`37-40`、`94`、`01n`、`01s` |
| 先读 v0 | `s06_life_support_development_engineering_contract.md`、`18_queue_d_body_dream_growth_implementation_contract.md`、`06_body_emotion_action_dream_growth_implementation_playbook.md`、`02_runtime_object_bus_and_flow_contract.md` |
| 打开代码 | `life_v0/body/__init__.py`、`rhythm.py`、`need_state.py`、`resource_budget.py`、`recovery.py`、`core_affect.py`、`emotion_episode.py`、`emotion_regulation.py`、`trait_drift.py`、`life_v0/defense/__init__.py` |
| 确认证据 | `runtime/state/body/*`、`runtime/state/defense/*`、`body_resource_budget.json` |
| 最低测试 | `tests/slices/test_life_support.py` |

### `life_v0/neural_core/`

| 类别 | 内容 |
|---|---|
| 先读理论 | `02`、`03`、`10`、`11`、`18`、`22`、`30`、`143`、`146`、`149`、`152`、`171`、`01m`、`01o`、`01p`、`01v-01ax` |
| 先读 v0 | `s02_neural_life_core_engineering_contract.md`、`17_queue_c_memory_neural_core_implementation_contract.md`、`05_memory_thought_consciousness_implementation_playbook.md`、`09_perception_prediction_world_contact_implementation_playbook.md` |
| 打开代码 | `life_v0/neural_core/__init__.py`、`brain_graph.py`、`network_state.py`、`prediction_workspace.py`、`workspace.py`、`broadcast.py`、`metacognition.py` |
| 确认证据 | `runtime/state/neural_life_core/*`、`runtime/state/prediction/*`、`runtime/state/consciousness/*` |
| 最低测试 | `tests/slices/test_neural_life_core.py` |

### `life_v0/state_store/`

| 类别 | 内容 |
|---|---|
| 先读理论 | `05`、`17-31`、`41-48`、`55`、`57`、`61`、`69`、`01q` |
| 先读 v0 | `s04_state_object_store_engineering_contract.md`、`life_state_store_v0_schema.md`、`05_memory_thought_consciousness_implementation_playbook.md` |
| 打开代码 | `life_v0/state_store/__init__.py`、`life_state.py`、`engram_index.py`、`autobiographical_stack.py`、`relationship_memory.py`、`self_model.py`、`commitment_truth.py` |
| 确认证据 | `runtime/state/life_state.json`、`runtime/state/memory/*`、`runtime/state/self/*`、`runtime/state/relationship/*` |
| 最低测试 | `tests/slices/test_state_store.py` |

### `life_v0/language/`

| 类别 | 内容 |
|---|---|
| 先读理论 | `09`、`85-90`、`94`、`96`、`101`、`141`、`144`、`147`、`150`、`01f`、`01j`、`01u` |
| 先读 v0 | `s07_language_relationship_engineering_contract.md`、`14_queue_a_language_percept_semantic_map_implementation_contract.md`、`04_language_dialogue_relationship_implementation_playbook.md`、`04_language_as_primary_expression_system.md` |
| 打开代码 | `life_v0/language/__init__.py`、`percept.py`、`semantic_map.py`、`inner_speech.py`、`expression_monitor.py`、`relationship_graph.py`、`shared_terms.py`、`commitment_repair.py`、`dialogue_log.py`、`narrative_trace.py`、`dream_gate.py`、`action_shadow.py`、`relation_scope.py` |
| 确认证据 | `runtime/state/language/*`、`runtime/state/relationship/*`、`language_relationship_report.json` |
| 最低测试 | `tests/slices/test_language_organs.py`、`tests/slices/test_language_relationship.py` |

### `life_v0/membrane/`、`life_v0/validators/`、`life_v0/schema_runner/`

| 类别 | 内容 |
|---|---|
| 先读理论 | `06`、`20`、`29-36`、`49-84`、`94`、`98`、`102-118`、`01r`、`01v-01ax` |
| 先读 v0 | `s03_direction_life_membrane_engineering_contract.md`、`s05_validation_membrane_observation_engineering_contract.md`、`s09_schema_runner_code_engineering_contract.md`、`20_queue_e_membrane_validator_logic_implementation_contract.md` |
| 打开代码 | `life_v0/membrane/__init__.py`、`candidate_arena.py`、`go_nogo.py`、`world_contact_gate.py`、`side_effect_review.py`、`life_v0/validators/__init__.py`、`observation_validator.py`、`boundary_audit.py`、`life_v0/schema_runner/__init__.py`、`consistency_logic.py`、`counterfactual_eval.py`、`comparison_trace.py` |
| 确认证据 | `runtime/state/membrane/*`、`runtime/state/action/*`、`runtime/state/validation/*`、`runtime/state/schema_runner/*` |
| 最低测试 | `tests/slices/test_life_membrane.py`、`tests/slices/test_validation_membrane.py`、`tests/slices/test_schema_runner.py` |

### `life_v0/dream/`、`life_v0/replay/`、`life_v0/archive/`

| 类别 | 内容 |
|---|---|
| 先读理论 | `08`、`19`、`23`、`27`、`31`、`95`、`99`、`181-257`、`01i`、`01t` |
| 先读 v0 | `s10_runtime_growth_reconsolidation_engineering_contract.md`、`18_queue_d_body_dream_growth_implementation_contract.md`、`06_body_emotion_action_dream_growth_implementation_playbook.md`、`02_runtime_object_bus_and_flow_contract.md` |
| 打开代码 | `life_v0/dream/__init__.py`、`offline_entry.py`、`dream_window.py`、`dream_fact_gate.py`、`wake_integration.py`、`nightmare_risk.py`、`life_v0/replay/__init__.py`、`life_v0/archive/__init__.py` |
| 确认证据 | `runtime/state/dream/*`、`runtime/state/replay/*`、`runtime/state/archive/*`、dream / replay / archive reports |
| 最低测试 | `tests/bridges/test_runtime_growth.py`、`tests/bridges/test_replay_shadow.py`、`tests/bridges/test_growth_archive.py` |

### `life_v0/growth/`

| 类别 | 内容 |
|---|---|
| 先读理论 | `39`、`92`、`93`、`97`、`181-257`、`01g` |
| 先读 v0 | `s06_life_support_development_engineering_contract.md`、`s10_runtime_growth_reconsolidation_engineering_contract.md`、`18_queue_d_body_dream_growth_implementation_contract.md`、`03_build_order_and_definition_of_done.md` |
| 打开代码 | `life_v0/growth/__init__.py`、`self_read.py`、`plasticity_window.py`、`learning_window.py`、`patch_queue.py`、`belief_learning.py`、`language_learning.py`、`relationship_learning.py`、`anti_forgetting.py` |
| 确认证据 | `runtime/state/growth/*`、growth reports、archive receipts |
| 最低测试 | `tests/bridges/test_runtime_growth.py`、`tests/slices/test_life_support.py` |

### `life_v0/life_targets/`

| 类别 | 内容 |
|---|---|
| 先读理论 | `10`、`91-101`、`143`、`146`、`149`、`152`、`171`、`174`、`01m` |
| 先读 v0 | `s08_life_target_runtimes_engineering_contract.md`、`birth_readiness_v0_contract.md`、`21_queue_f_identity_consciousness_birth_readiness_implementation_contract.md` |
| 打开代码 | `life_v0/life_targets/__init__.py`、`life_target_claims.py`、`evidence_matrix.py`、`consciousness_probes.py`、`birth_readiness_rollup.py`、`birth_readiness_stage_gate.py` |
| 确认证据 | `runtime/state/life_targets/*`、`birth_readiness_report.json` |
| 最低测试 | `tests/slices/test_life_targets.py` |

### `life_v0/activation/`、`reporting/`、`stage_explain/`、`digital_life/`

| 类别 | 内容 |
|---|---|
| 先读理论 | `20`、`44-46`、`89-90`、`181-257` |
| 先读 v0 | `first_activation_protocol.md`、`runner_cli_report_contract.md`、`07_birth_terminal_process_implementation_playbook.md` |
| 打开代码 | `life_v0/activation/__init__.py`、`life_v0/reporting/__init__.py`、`life_v0/stage_explain/__init__.py`、`life_v0/digital_life/__init__.py` |
| 确认证据 | `first_activation_return_packet.json`、`report_bundle.json`、`stage_explanation_report.json`、`digital_life_birth_packet.json` |
| 最低测试 | `tests/bridges/test_first_activation_preflight.py`、`tests/bridges/test_emit_report.py`、`tests/bridges/test_explain_stage.py`、`tests/bridges/test_digital_life_birth.py` |

### `life_v0/terminal_turn/`、`life_v0/terminal_loop/`

| 类别 | 内容 |
|---|---|
| 先读理论 | `20`、`86`、`89-90`、`96`、`101` |
| 先读 v0 | `first_terminal_turn_engineering_contract.md`、`terminal_life_loop_engineering_contract.md`、`04_language_dialogue_relationship_implementation_playbook.md`、`02_runtime_object_bus_and_flow_contract.md` |
| 打开代码 | `life_v0/terminal_turn/__init__.py`、`context_accumulation.py`、`turn_transition.py`、`life_v0/terminal_loop/__init__.py`、`loop_state.py`、`resume_packet.py`、`dialogue_writeback.py` |
| 确认证据 | `session_envelope.json`、`context_accumulation_window.json`、`turn_transition_trace.json`、`terminal_life_loop_state.json` |
| 最低测试 | `tests/bridges/test_first_terminal_turn.py`、`tests/bridges/test_terminal_life_loop.py` |

### `life_v0/process_supervisor/` 与 `digital_entry.py`

| 类别 | 内容 |
|---|---|
| 先读理论 | `20`、`81-84`、`86`、`89-90`、`96`、`101`、`181-257` |
| 先读 v0 | `digital_life_process_supervisor_engineering_contract.md`、`16_queue_b_process_supervisor_implementation_contract.md`、`07_birth_terminal_process_implementation_playbook.md`、`03_build_order_and_definition_of_done.md`、`05_birth_residency_terminal_blueprint.md` |
| 打开代码 | `life_v0/process_supervisor/__init__.py`、`heartbeat.py`、`idle_strategy.py`、`idle_refresh_loop.py`、`persistent_process.py`、`process_closeout.py`、`continuity_writeback.py`、`turn_io.py`、`dialogue_events.py`、`response_surface.py`、`incident_recovery.py`、`relaunch_recovery.py`、`process_report.py`、`life_v0/digital_entry.py`、`digital` |
| 确认证据 | `digital_life_waiting_heartbeat.json`、`runtime/state/terminal/idle_strategy_state.json`、`runtime/state/terminal/resident_governance_snapshot.json`、`digital_life_resident_governance_report.json`、`digital_life_process_report.json`、incident / relaunch recovery reports |
| 最低测试 | `tests/process/test_digital_entrypoint.py`、`tests/process/test_persistent_digital_life_process.py`、`tests/process/test_digital_life_shell_command.py` |

## 当前最适合直接开写的顺序

按当前工作区现实，如果要从这里直接进入代码，最稳的顺序仍然是：

1. `body/`、`dream/`、`growth/`
2. `membrane/`、`validators/`、`schema_runner/`
3. `process_supervisor/`，优先继续补 waiting governance 的字段贯通、resident governance closeout 和 heartbeat 节律实化
4. `language/`、`terminal_turn/`、`terminal_loop/`
5. 再回切 `neural_core/`、`state_store/`、`life_targets/`

原因不是后面几层不重要，而是前两段决定这个系统是不是先拥有身体化、责任化、梦境化和成长化底盘。
