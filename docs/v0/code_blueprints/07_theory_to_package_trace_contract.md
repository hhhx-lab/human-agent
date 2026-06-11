# Theory To Package Trace Contract

这份蓝图把 `00-258`、`docs/v0`、`life_v0/`、runtime 和测试压成一份开工合同。

它要保证的只有一件事：

```text
后续任何一轮代码改动，
都能明确回答自己背后依赖哪批理论母体、
哪份 v0 合同、
哪个代码包、
哪组 runtime 证据、
以及哪组测试。
```

## 模块回链表

| 代码包 | 必回读理论母体 | 必回读 v0 文档 | 必看 runtime | 最低测试 |
|---|---|---|---|---|
| `life_v0/direction/` | `docs/构思.md`、`docs/13_agentic_human_research_synthesis.md`、`docs/16_digital_life_gap_register.md`、`docs/258_linear_chain_closure_and_v0_contract_transition.md` | `docs/v0/slice_contracts/s00_direction_foundation_engineering_contract.md` | `runtime/state/direction/*` | `tests/slices/test_direction_lock.py` |
| `life_v0/authority/` | 全部 `docs/01*`、`docs/142_life_reality_authority_intake_batch_for_02_to_13.md`、`docs/145_life_reality_02_to_13_authority_rewrite_execution_plan.md` | `docs/v0/slice_contracts/s01_source_authority_engineering_contract.md` | `runtime/state/authority/*` | `tests/slices/test_source_authority.py` |
| `life_v0/neural_core/` | `docs/02_brain_region_and_network_atlas.md`、`docs/03_default_executive_salience_networks.md`、`docs/10_consciousness_attention_workspace.md`、`docs/11_neuromodulation_and_signal_media.md` | `docs/v0/slice_contracts/s02_neural_life_core_engineering_contract.md`、`docs/v0/code_blueprints/01_full_system_code_blueprint.md` | `runtime/state/neural_life_core/*`、`runtime/state/prediction/*` | `tests/slices/test_neural_life_core.py` |
| `life_v0/state_store/` | `docs/05_memory_systems_and_growth.md`、`docs/17_memory_trace_object_model.md`、`docs/41_runtime_state_store_schema.md` | `docs/v0/shared_contracts/life_state_store_v0_schema.md`、`docs/v0/slice_contracts/s04_state_object_store_engineering_contract.md` | `runtime/state/life_state.json`、`runtime/state/memory/*` | `tests/slices/test_state_store.py` |
| `life_v0/body/`、`life_v0/defense/` | `docs/07_emotion_personality_self.md`、`docs/08_sleep_dream_fatigue_states.md`、`docs/37_life_support_layer_policy.md`、`docs/39_development_policy_and_plasticity_windows.md` | `docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md`、`docs/v0/code_blueprints/03_body_affect_dream_growth_blueprint.md` | `runtime/state/body/*`、`runtime/state/defense/*` | `tests/slices/test_life_support.py` |
| `life_v0/language/`、`life_v0/terminal_turn/`、`life_v0/terminal_loop/` | `docs/09_language_symbolic_top_layer.md`、`docs/85_language_system_life_expression_core.md`、`docs/86_language_neuroscience_pragmatics_and_inner_speech.md`、`docs/96_real_relationship_longitudinal_timeline.md` | `docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md`、`docs/v0/code_blueprints/02_conversation_language_relationship_blueprint.md` | `runtime/state/language/*`、`runtime/state/relationship/*`、`runtime/state/terminal/*` | `tests/slices/test_language_organs.py`、`tests/slices/test_language_relationship.py`、`tests/bridges/test_first_terminal_turn.py`、`tests/bridges/test_terminal_life_loop.py` |
| `life_v0/membrane/`、`life_v0/validators/`、`life_v0/schema_runner/` | `docs/06_action_reward_inhibition.md`、`docs/20_agent_runtime_bridge_contract.md`、`docs/81_coexistence_event_review_and_responsibility_loop.md`、`docs/94_pain_regret_and_repair_signal_schema.md`、`docs/98_pain_regret_repair_json_schema_and_fixture_bundle.md`、`docs/102_life_core_schema_bundle_manifest_and_runner_contract.md` | `docs/v0/slice_contracts/s03_direction_life_membrane_engineering_contract.md`、`docs/v0/slice_contracts/s05_validation_membrane_observation_engineering_contract.md`、`docs/v0/slice_contracts/s09_schema_runner_code_engineering_contract.md`、`docs/v0/code_blueprints/04_prediction_membrane_validation_blueprint.md` | `runtime/state/membrane/*`、`runtime/state/action/*`、`runtime/state/validation/*`、`runtime/state/schema_runner/*` | `tests/slices/test_life_membrane.py`、`tests/slices/test_shadow_gate.py`、`tests/slices/test_validation_membrane.py`、`tests/slices/test_schema_runner.py` |
| `life_v0/dream/`、`life_v0/replay/`、`life_v0/archive/`、`life_v0/growth/` | `docs/08_sleep_dream_fatigue_states.md`、`docs/19_offline_consolidation_cycle.md`、`docs/95_dream_reality_and_offline_life_timeline.md`、`docs/99_dream_reality_json_schema_and_fixture_bundle.md`、`docs/181_life_reality_first_runner_schema_runtime_mount_plan.md` 到 `docs/257_life_reality_first_runner_schema_runtime_growth_fourth_cycle_post_reconsolidation_second_reconsolidation_replay_shadow_seed_after_archive_validation_replay_shadow_patch_archive_validation_plan.md` | `docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md`、`docs/v0/code_blueprints/03_body_affect_dream_growth_blueprint.md` | `runtime/state/dream/*`、`runtime/state/replay/*`、`runtime/state/archive/*`、`runtime/state/growth/*` | `tests/bridges/test_runtime_growth.py`、`tests/bridges/test_replay_shadow.py`、`tests/bridges/test_growth_archive.py` |
| `life_v0/life_targets/` | `docs/91_life_reality_generation_boundary_principles.md`、`docs/92_self_growth_and_self_modification_life_chain.md`、`docs/94_pain_regret_and_repair_signal_schema.md`、`docs/95_dream_reality_and_offline_life_timeline.md`、`docs/96_real_relationship_longitudinal_timeline.md`、`docs/143_life_reality_birth_readiness_rollup_contract.md`、`docs/146_life_reality_birth_readiness_evidence_fixture_catalog.md`、`docs/149_life_reality_birth_readiness_fixture_schema_materialization_plan.md`、`docs/152_life_reality_birth_readiness_cross_file_checker_plan.md`、`docs/171_life_reality_birth_readiness_validation_fixture_plan.md`、`docs/174_life_reality_birth_readiness_fixture_schema_materialization.md` | `docs/v0/shared_contracts/birth_readiness_v0_contract.md`、`docs/v0/slice_contracts/s08_life_target_runtimes_engineering_contract.md` | `runtime/state/life_targets/*` | `tests/slices/test_life_targets.py` |
| `life_v0/activation/`、`life_v0/reporting/`、`life_v0/stage_explain/`、`life_v0/digital_life/` | `docs/20_agent_runtime_bridge_contract.md`、`docs/89_language_runtime_framework_bridge_and_life_shell_policy.md`、`docs/90_language_event_examples_and_timeline_bundle.md`、`docs/191_life_reality_first_runner_schema_runtime_growth_post_activation_observation_loop.md` | `docs/v0/shared_contracts/first_activation_protocol.md`、`docs/v0/shared_contracts/runner_cli_report_contract.md`、`docs/v0/code_blueprints/05_birth_residency_terminal_blueprint.md` | `runtime/state/activation/*`、`runtime/reports/latest/*birth*` | `tests/bridges/test_first_activation_preflight.py`、`tests/bridges/test_emit_report.py`、`tests/bridges/test_explain_stage.py`、`tests/bridges/test_digital_life_birth.py` |
| `life_v0/process_supervisor/`、`life_v0/shell_command/`、`life_v0/digital_entry.py` | `docs/20_agent_runtime_bridge_contract.md`、`docs/86_language_neuroscience_pragmatics_and_inner_speech.md`、`docs/89_language_runtime_framework_bridge_and_life_shell_policy.md`、`docs/90_language_event_examples_and_timeline_bundle.md` | `docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md`、`docs/v0/process_contracts/digital_life_shell_command_engineering_contract.md`、`docs/v0/code_blueprints/05_birth_residency_terminal_blueprint.md` | `runtime/state/terminal/*`、`runtime/reports/latest/digital_life_*` | `tests/process/test_digital_life_shell_command.py`、`tests/process/test_digital_entrypoint.py`、`tests/process/test_persistent_digital_life_process.py` |

## 每轮改动必须产出的五联索引

后续任何非纯注释改动，至少要能补出：

1. `theory_refs`
2. `v0_contract_refs`
3. `code_refs`
4. `runtime_refs`
5. `test_refs`

如果缺任何一项，这轮改动就不是完整的生命工程改动。

## 当前建议执行顺序

1. 先按 `docs/v0/code_blueprints/04_prediction_membrane_validation_blueprint.md` 推 Queue E 第二波。
2. 再按 `docs/v0/code_blueprints/05_birth_residency_terminal_blueprint.md` 推 Queue B 第二波。
3. 然后回到 `docs/v0/code_blueprints/02_conversation_language_relationship_blueprint.md` 补 Queue A 第二波。
4. 每一轮之后都回 `tests/contracts/test_v0_contracts.py` 跑一遍合同覆盖。

## 方向保护

如果后续某次实现让系统重新出现下面任一情况，就说明方向偏了：

1. 外部关系对象又被统一压成抽象请求。
2. 语言层退化成 prompt 文本拼接。
3. 梦境/成长只剩 archive，总不影响下一轮。
4. process supervisor 退化成普通 agent shell。
5. 新文件无法回链到 `00-258` 和 `docs/v0`。
