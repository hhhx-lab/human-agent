# Theory To Code Trace Matrix

本文档把 `00-258` 理论母体、`docs/v0` 合同、`life_v0` 代码树、runtime 证据、测试和 gate 放进一张总矩阵。

## 总矩阵

| 生命域 | 直接理论母体 | 当前 v0 合同 / 深描 | 当前主代码 | 下一轮关键文件 | runtime 证据 | 测试 / gate |
|---|---|---|---|---|---|---|
| 方向与身份根 | `构思.md`、`00`、`13`、`16`、`91`、`258` | `s00_direction_foundation_engineering_contract.md`、`10_self_identity_value_commitment_implementation_playbook.md`、`01_full_life_layer_implementation_deep_spec.md` | `life_v0/direction/*` | 继续补 continuity writeback 细化 | `runtime/state/direction/*` | `tests/slices/test_direction_lock.py` |
| 文献权威与来源 | 全部 `01*`、`142`、`145`、`151` | `s01_source_authority_engineering_contract.md`、`theory_closure_and_engineering_readiness_audit.md` | `life_v0/authority/__init__.py`、`life_v0/doc_index.py` | 继续细化 authority registry 子文件 | `runtime/state/authority/*`、`runtime/docs/*` | `tests/slices/test_source_authority.py` |
| 脑区、网络、工作区 | `02`、`03`、`10`、`11`、`01m`、`01o`、`01p` | `s02_neural_life_core_engineering_contract.md`、`17_queue_c_memory_neural_core_implementation_contract.md`、`05_memory_thought_consciousness_implementation_playbook.md`、`01_full_life_layer_implementation_deep_spec.md` | `life_v0/neural_core/*` | `signal_media.py`、`belief_state.py`、`prediction_error.py`、`active_sampling.py` | `runtime/state/neural_life_core/*`、`runtime/state/prediction/*` | `tests/slices/test_neural_life_core.py` |
| 身体、内环境、节律 | `04`、`08`、`18`、`37-39`、`01n` | `s06_life_support_development_engineering_contract.md`、`18_queue_d_body_dream_growth_implementation_contract.md`、`04_body_affect_dream_growth_engineering.md` | `life_v0/body/*` | 继续补节律与 heartbeat 直接同步 | `runtime/state/body/*` | `tests/slices/test_life_support.py` |
| 记忆与状态根 | `05`、`17-31`、`41-48`、`55`、`57`、`61`、`69`、`01q` | `s04_state_object_store_engineering_contract.md`、`life_state_store_v0_schema.md`、`02_state_object_runtime_evidence_map.md` | `life_v0/state_store/*` | `memory_write_gate.py` | `runtime/state/life_state.json`、`runtime/state/memory/*` | `tests/slices/test_state_store.py` |
| 语言与关系 | `09`、`85-90`、`94`、`96`、`101`、`141`、`144`、`147`、`150`、`01f`、`01j`、`01u` | `s07_language_relationship_engineering_contract.md`、`14_queue_a_language_percept_semantic_map_implementation_contract.md`、`03_language_relationship_longitudinal_engineering.md` | `life_v0/language/*`、`terminal_turn/*`、`terminal_loop/dialogue_writeback.py` | `relationship_timeline.py`、`commitment_expression.py`、`apology_repair_language.py` | `runtime/state/language/*`、`runtime/state/relationship/*` | `tests/slices/test_language_organs.py`、`tests/slices/test_language_relationship.py` |
| 行为、抑制、世界接触、责任 | `06`、`20`、`75`、`80-84`、`94`、`98`、`01r` | `s03_direction_life_membrane_engineering_contract.md`、`20_queue_e_membrane_validator_logic_implementation_contract.md`、`05_prediction_membrane_action_engineering.md` | `life_v0/membrane/*` | `shadow_gate.py` | `runtime/state/membrane/*`、`runtime/state/action/*` | `tests/slices/test_life_membrane.py` |
| 逻辑、验证、反事实 | `22`、`29-36`、`49-84`、`102-118`、`01v-01ax` | `s05_validation_membrane_observation_engineering_contract.md`、`s09_schema_runner_code_engineering_contract.md`、`05_prediction_membrane_action_engineering.md` | `life_v0/validators/*`、`life_v0/schema_runner/*` | `evidence_ranker.py` | `runtime/state/validation/*`、`runtime/state/schema_runner/*` | `tests/slices/test_validation_membrane.py`、`tests/slices/test_schema_runner.py` |
| 梦境与离线生命 | `08`、`19`、`23`、`27`、`31`、`95`、`99`、`01i`、`01t` | `s10_runtime_growth_reconsolidation_engineering_contract.md`、`18_queue_d_body_dream_growth_implementation_contract.md`、`04_body_affect_dream_growth_engineering.md` | `life_v0/dream/*` | 继续补梦境残留和 dream-body-language 接线 | `runtime/state/dream/*` | `tests/bridges/test_runtime_growth.py`、`tests/bridges/test_growth_archive.py` |
| 成长、学习、自改写 | `39`、`92`、`93`、`97`、`181-257` | `s06_life_support_development_engineering_contract.md`、`s10_runtime_growth_reconsolidation_engineering_contract.md`、`04_body_affect_dream_growth_engineering.md` | `life_v0/growth/*` | 继续补 patch 审查和 promotion 轨迹 | `runtime/state/growth/*` | `tests/bridges/test_runtime_growth.py` |
| 生命目标、意识证据、出生准备 | `10`、`91-101`、`143`、`146`、`149`、`152`、`171`、`174` | `s08_life_target_runtimes_engineering_contract.md`、`birth_readiness_v0_contract.md`、`21_queue_f_identity_consciousness_birth_readiness_implementation_contract.md` | `life_v0/life_targets/*` | 继续补长期 evidence rollup | `runtime/state/life_targets/*` | `tests/slices/test_life_targets.py` |
| 激活链与出生壳 | `20`、`44-46`、`89-90`、`181-257` | `first_activation_protocol.md`、`runner_cli_report_contract.md`、`07_birth_terminal_process_implementation_playbook.md`、`06_resident_process_terminal_birth_engineering.md` | `life_v0/activation/`、`reporting/`、`stage_explain/`、`digital_life/` | 持续补 report bundle 与 stage handoff 细节 | `first_activation_return_packet.json`、`digital_life_birth_packet.json` | `tests/bridges/test_first_activation_preflight.py`、`test_emit_report.py`、`test_digital_life_birth.py` |
| 第一回合、终端循环、常驻过程 | `20`、`81-84`、`86`、`89-90`、`96`、`101`、`181-257` | `first_terminal_turn_engineering_contract.md`、`terminal_life_loop_engineering_contract.md`、`digital_life_process_supervisor_engineering_contract.md`、`06_resident_process_terminal_birth_engineering.md` | `life_v0/terminal_turn/*`、`terminal_loop/*`、`shell_command/*`、`process_supervisor/*`、`digital_entry.py` | `idle_strategy.py`、`persistent_process.py` | `session_envelope.json`、`terminal_life_loop_state.json`、`digital_life_waiting_heartbeat.json`、process reports | `tests/bridges/test_first_terminal_turn.py`、`tests/bridges/test_terminal_life_loop.py`、`tests/process/test_persistent_digital_life_process.py` |

## 当前最关键的文件级补洞总表

| 队列 | 最关键文件 |
|---|---|
| Queue D 第三波 | `nightmare_risk.py`、`belief_learning.py`、`language_learning.py`、`relationship_learning.py` 的进一步联动补厚 |
| Queue E 第二波 | `shadow_gate.py`、`evidence_ranker.py` |
| Queue B 第二波 | `idle_strategy.py`、`persistent_process.py` |
| Queue A 第二波 | `relationship_timeline.py`、`commitment_expression.py`、`apology_repair_language.py` |
| Queue C / F 维护性回切 | `signal_media.py`、`belief_state.py`、`prediction_error.py`、`active_sampling.py`、`memory_write_gate.py` |
