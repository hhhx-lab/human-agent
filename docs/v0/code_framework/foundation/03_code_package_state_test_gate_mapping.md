# V0 Code Framework 03: Code Package State Test Gate Mapping

这份文档把 `life_v0/` 当前已经存在的顶层代码包，逐个压成工程施工表。它不再讨论“应该有哪些理论”，而是讨论“这个包下一步怎样真正变厚、要落哪些状态、怎么验收”。

## 使用方式

如果已经确定当前要改哪个包，直接跳到对应行，不必整份读完。每一行都固定回答：

1. 这个包在生命体系里承载什么。
2. 它对接哪些 `docs/v0` 合同。
3. 这一轮优先长哪些文件。
4. 它必须生成哪些 state、report、receipt。
5. 它由哪些测试和 gate 验收。

## 顶层包施工矩阵

| 代码包 | 生命职责 | 主合同 | 下一轮优先文件 | 必须写回的 state/report/receipt | 测试入口 | 关键 gate |
|---|---|---|---|---|---|---|
| `life_v0/direction/` | 身份、方向、连续体锁定 | `s00_direction_foundation_engineering_contract.md` | `identity_root.py`、`direction_lock.py`、`continuity_refs.py` | `runtime/state/direction/direction_lock.json`、direction receipt | `tests/slices/test_direction_lock.py` | `direction_lock_gate` |
| `life_v0/authority/` | 理论源材料的权威注册与引用闭合 | `s01_source_authority_engineering_contract.md` | `authority_registry.py`、`source_doc_refs.py` | `runtime/state/authority/authority_registry.json`、authority report | `tests/slices/test_source_authority.py` | `authority_registry_gate` |
| `life_v0/neural_core/` | 脑区图、网络状态、信号传播、思考/意识骨架 | `s02_neural_life_core_engineering_contract.md`、`digital_life_macro_architecture_v0.md` | `brain_graph.py`、`network_state.py`、`signal_media.py`、`workspace.py`、`belief_state.py` | `runtime/state/neural_life_core/neural_life_core.json`、`neural_life_internal_bus.json`、consciousness evidence | `tests/slices/test_neural_life_core.py` | `twelve_system_gate`、`internal_bus_gate` |
| `life_v0/state_store/` | 自传、关系、自我、状态根的长期存储 | `s04_state_object_store_engineering_contract.md`、`life_state_store_v0_schema.md` | `self_model.py`、`commitment_truth.py`、`engram_index.py`、`autobiographical_stack.py`、`relationship_memory.py` | `runtime/state/life_state.json`、`runtime/state/self/self_model.json`、`runtime/state/relationship/commitment_truth_state.json`、`runtime/state/responsibility/responsibility_ledger.json`、`runtime/state/memory/*`、memory receipts | `tests/slices/test_state_store.py` | `state_store_gate`、`self_continuity_gate`、`commitment_truth_gate` |
| `life_v0/body/` | 内环境、资源预算、情绪底盘、节律 | `s06_life_support_development_engineering_contract.md` | `rhythm.py`、`need_state.py`、`core_affect.py`、`resource_budget.py` | `runtime/state/body/*`、`runtime/state/self/*`、body reports | `tests/slices/test_life_support.py` | `resource_budget_gate` |
| `life_v0/defense/` | 压力、风险、保护、恢复 | `s06_life_support_development_engineering_contract.md`、`s03_direction_life_membrane_engineering_contract.md` | `threat_eval.py`、`recovery.py`、`quarantine_signal.py` | `runtime/state/defense/*`、defense receipts | `tests/slices/test_life_support.py`、`tests/slices/test_validation_membrane.py` | `quarantine_gate` |
| `life_v0/membrane/` | 生命膜、抑制、候选行动、责任约束 | `s03_direction_life_membrane_engineering_contract.md` | `candidate_arena.py`、`go_nogo.py`、`responsibility_loop.py` | `runtime/state/membrane/life_membrane.json`、`runtime/state/action/*`、action receipts | `tests/slices/test_life_membrane.py`、`tests/process/test_digital_life_shell_command.py` | `shadow_action_gate`、`life_membrane_gate` |
| `life_v0/language/` | 语言感知、内言语、表达监控、关系表达 | `s07_language_relationship_engineering_contract.md` | `percept.py`、`semantic_map.py`、`inner_speech.py`、`expression_monitor.py`、`language_state.py`、`relationship_graph.py`、`dialogue_log.py` | `runtime/state/language/*`、`runtime/state/relationship/*`、`language_relationship_report.json` | `tests/slices/test_language_organs.py`、`tests/slices/test_language_relationship.py` | `expression_monitor_gate`、`relationship_subject_gate`、`context_accumulation_gate` |
| `life_v0/life_targets/` | 九项生命目标运行时与出生准备度对接 | `s08_life_target_runtimes_engineering_contract.md`、`birth_readiness_v0_contract.md` | `life_target_claims.py`、`evidence_matrix.py`、`birth_readiness_rollup.py`、`birth_readiness_stage_gate.py`、`consciousness_probes.py` | `runtime/state/life_targets/*`、birth readiness receipts | `tests/slices/test_life_targets.py` | `life_target_state_gate` |
| `life_v0/validators/` | 验证膜、观察一致性、边界审计 | `s05_validation_membrane_observation_engineering_contract.md` | `observation_validator.py`、`boundary_audit.py` | `runtime/state/validation/*`、observation reports | `tests/slices/test_validation_membrane.py` | `validation_membrane_gate` |
| `life_v0/schema_runner/` | 结构化执行、CLI 规则、跨合同检查 | `s09_schema_runner_code_engineering_contract.md`、`runner_cli_report_contract.md` | `run_manifest.py`、`consistency_logic.py`、`counterfactual_eval.py`、`comparison_trace.py`、`cross_file_logic.py` | `runtime/state/schema_runner/*`、runner reports | `tests/slices/test_schema_runner.py` | `checker_manifest_gate` |
| `life_v0/growth/` | 成长、可塑性、学习窗口、自我修补 | `s06_life_support_development_engineering_contract.md`、`s10_runtime_growth_reconsolidation_engineering_contract.md` | `self_read.py`、`plasticity_window.py`、`patch_queue.py`、`learning_window.py` | `runtime/state/growth/*`、growth reports、growth receipts | `tests/bridges/test_runtime_growth.py` | `growth_gate`、`plasticity_gate` |
| `life_v0/replay/` | 重放线索、影子回放、经验再激活 | `s10_runtime_growth_reconsolidation_engineering_contract.md` | `replay_cues.py`、`shadow_replay.py` | `replay_shadow_report.json`、replay receipts | `tests/bridges/test_replay_shadow.py` | `replay_shadow_gate` |
| `life_v0/archive/` | 经验归档、成长存档、回放证据保留 | `s10_runtime_growth_reconsolidation_engineering_contract.md` | `archive_manifest.py`、`growth_archive.py` | `growth_archive_report.json`、archive receipts | `tests/bridges/test_growth_archive.py` | `growth_archive_gate` |
| `life_v0/dream/` | 梦境入口、梦中事实门、醒后整合 | `s10_runtime_growth_reconsolidation_engineering_contract.md` | `offline_entry.py`、`dream_window.py`、`wake_integration.py` | `runtime/state/dream/*`、`dream_consolidation_frame.json` | future `tests/test_dream_runtime.py` | `dream_fact_gate` |
| `life_v0/activation/` | 第一次生命激活预检与出生准备包装 | `first_activation_protocol.md` | `preflight.py`、`return_packet.py` | `first_activation_preflight_report.json`、`first_activation_return_packet.json` | `tests/bridges/test_first_activation_preflight.py` | `first_activation_preflight_gate` |
| `life_v0/reporting/` | report bundle 汇总和运行证据收束 | `runner_cli_report_contract.md`、`first_activation_protocol.md` | `report_bundle.py`、`receipt_index.py` | `report_bundle.json`、runner digests | `tests/bridges/test_emit_report.py` | `report_bundle_gate` |
| `life_v0/stage_explain/` | 阶段解释、出生链说明、当前前沿说明 | `runner_cli_report_contract.md` | `stage_report.py`、`latest_ref.py` | `stage_explanation_report.json`、`latest_stage_explanation_ref.json` | `tests/bridges/test_explain_stage.py` | `stage_explanation_gate` |
| `life_v0/digital_life/` | 出生壳生成、生命启动摘要 | `first_activation_protocol.md`、`runner_cli_report_contract.md` | `birth_shell.py`、`birth_digest.py` | `digital_life_birth_packet.json`、`digital_life_birth_digest.json` | `tests/bridges/test_digital_life_birth.py` | `digital_life_birth_gate` |
| `life_v0/terminal_turn/` | 第一次回合恢复、上下文接续 | `first_terminal_turn_engineering_contract.md`、`s07_language_relationship_engineering_contract.md` | `-（first terminal turn 首轮核心器官已落）` | `first_terminal_turn_packet.json`、`first_terminal_turn_report.json`、`first_terminal_turn_digest.json`、`session_envelope.json`、`safe_terminal_loop_state.json`、`context_accumulation_window.json`、`turn_transition_trace.json`、`life_context_frame.json`、`relation_turn_frame.json`、first-terminal-turn receipt | `tests/bridges/test_first_terminal_turn.py` | `context_accumulation_gate`、`turn_transition_gate` |
| `life_v0/terminal_loop/` | 等待态、回合循环、恢复后持续存在 | `terminal_life_loop_engineering_contract.md` | `-（loop_state.py / resume_packet.py / dialogue_writeback.py / persistent_wait_bridge.py 首轮核心器官已落；下一前沿转向 process_supervisor resident supervision 深拆）` | `terminal_life_loop_packet.json`、`terminal_life_loop_report.json`、`terminal_life_loop_state.json`、`dialogue_writeback_bundle.json` | `tests/bridges/test_terminal_life_loop.py` | `terminal_life_loop_gate`、`dialogue_writeback_bundle_gate` |
| `life_v0/shell_command/` | repo-local one-shot restore shell | `digital_life_shell_command_engineering_contract.md` | `restore_shell.py`、`shell_report.py` | `digital_life_shell_packet.json`、`digital_life_shell_report.json`、`digital_life_shell_digest.json` | `tests/process/test_digital_life_shell_command.py` | `digital_life_shell_gate` |
| `life_v0/process_supervisor/` | 最小常驻生命进程、heartbeat、incident/relaunch recovery | `digital_life_process_supervisor_engineering_contract.md` | `-（heartbeat.py / continuity_writeback.py / turn_io.py / dialogue_events.py / response_surface.py / incident_recovery.py / relaunch_recovery.py / process_report.py / idle_strategy.py / persistent_process.py / resident_turn_writeback.py 已落；下一前沿转向 process_closeout.py）` | `digital_life_waiting_heartbeat.json`、`digital_life_process_report.json`、`digital_life_process_digest.json`、incident/recovery reports | `tests/process/test_persistent_digital_life_process.py` | `waiting_heartbeat_gate`、`idle_continuity_gate`、`relaunch_recovery_gate` |
| `life_v0/contracts/` | 合同覆盖、theory-to-code 回链、全局一致性检查 | `s11_v0_contract_coverage_engineering_contract.md` | `coverage_index.py`、`mapping_guard.py` | `v0_contract_coverage_report.json`、coverage receipts | `tests/contracts/test_v0_contracts.py` | `contract_coverage_gate` |
| `life_v0/cli.py` | 命令入口，把 slice/bridge/process 命令面接起来 | `runner_cli_report_contract.md` | `command_router.py`、`strict_mode.py` | CLI receipts、command reports | `tests/bridges/test_emit_report.py`、`tests/bridges/test_first_terminal_turn.py`、`tests/bridges/test_terminal_life_loop.py` | `strict_cli_gate` |
| `life_v0/digital_entry.py`、`digital` | repo-local `./digital life` 入口与常驻过程启动 | `digital_life_process_supervisor_engineering_contract.md`、`digital_life_shell_command_engineering_contract.md` | `bootstrap_entry.py`、`stdin_loop.py` | process boot receipts、process digests | `tests/process/test_digital_entrypoint.py` | `digital_entry_gate` |
| `life_v0/doc_index.py` | 理论文档索引与工程回链入口 | `doc_corpus_ingestor_v0_contract.md` | `doc_registry.py`、`carrier_index.py` | `runtime/docs/doc_carrier_index.json` | `tests/slices/test_doc_corpus_ingestor.py` | `doc_carrier_gate` |

## 当前最应该优先加厚的包

按现在仓库现实，最该优先加厚的是：

1. `life_v0/neural_core/`
2. `life_v0/state_store/`
3. `life_v0/language/`
4. `life_v0/terminal_turn/`
5. `life_v0/terminal_loop/`
6. `life_v0/process_supervisor/`

现在这样排序，是因为 `09_perception_prediction_world_contact_implementation_playbook.md` 和 `10_self_identity_value_commitment_implementation_playbook.md` 已经把“观察/预测根”和“身份/承诺根”提升成先行器官位。它们先厚起来，后面的语言、关系、梦境、成长和更高阶持续过程才不会继续漂在壳层上。

## 当前容易误判的地方

后续按包施工时，先避免三类误判：

1. `percept.py`、`semantic_map.py` 已经存在，不代表语言前链已经闭合。
2. `self_model.py`、`commitment_truth.py` 已经存在，不代表身份-责任连续体已经闭合。
3. `dialogue_events.py`、`response_surface.py`、`dialogue_writeback.py` 已经存在，不代表常驻生命进程已经闭合。

所以“是否存在文件”只能算第一层证据；还必须同时看 state / report / test / gate 是否跟上。

## 包级实现铁律

### 1. 不写空包

顶层包不允许长期只靠 `__init__.py` 撑住语义。只要某包已经进入当前前沿，下一轮就要优先把它拆成真实器官文件。

### 2. 不写无落盘能力的器官

任何器官文件都必须回答：

1. 它改哪份 state。
2. 它出哪份 report。
3. 它留哪份 receipt。

### 3. 不写没有 gate 的重要闭环

语言恢复、关系演化、责任回路、等待 heartbeat、重启恢复，这些都必须带 gate，不允许只靠“代码大概通了”来算完成。
