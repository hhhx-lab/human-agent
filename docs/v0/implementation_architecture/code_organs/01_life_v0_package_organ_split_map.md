# Life V0 Package Organ Split Map

这份文档把 `life_v0/` 当前真实包结构压成逐包器官装配总图。

它不再回答“应该有哪些生命层”，而是直接回答：

1. 当前每个顶层包里已经有哪些真实器官文件。
2. 当前还压在 `__init__.py` 里的职责有哪些。
3. 下一轮最该新增或继续拆哪些器官文件。
4. 每个包要回读哪些 `00-258` 理论文档和 `docs/v0/*` 合同。
5. 每个包必须守住哪些 runtime 产物、测试和 gate。

## 使用原则

读这份图时，不要问“这个包像不像某个外部 agent 模块”。
只问下面五件事：

1. 这个包承载哪条生命链。
2. 当前已经落下了哪些真实器官。
3. 当前还剩哪些职责不该继续留在 `__init__.py`。
4. 拆出来后写哪份 `state / report / receipt`。
5. 哪组测试最先证明它没有把生命链拆断。

## 当前重型入口热区

下面这些 `__init__.py` 仍然是当前最重的真实入口，后续逐文件施工要优先盯住它们：

| 包 | `__init__.py` 行数 | 当前判断 |
|---|---:|---|
| `life_v0/contracts/` | 1304 | 合同登记中心，暂不随意拆散，但要受新增文档同步更新约束 |
| `life_v0/neural_core/` | 1155 | 主体工作区和预测链过重，后续继续做 Queue C 维护回切 |
| `life_v0/growth/` | 1153 | 学习/成长/防遗忘链仍偏集中，继续按 Queue D 第三波补厚与跨层回写拆 |
| `life_v0/life_targets/` | 1100 | 目标闭合、证据矩阵、出生准备度仍需更细分 |
| `life_v0/membrane/` | 1090 | 候选行动、抑制、责任回路、世界接触逻辑还需要继续抽出 |
| `life_v0/language/` | 1081 | 已经完成第一轮器官化，但长期关系/修复表达仍未独立出来 |
| `life_v0/authority/` | 1077 | 文献权威、机制证据和 intake/checker 还可继续细分 |
| `life_v0/state_store/` | 1048 | 状态根、自传、关系真值虽然已有器官，但 write gate 仍需补硬 |
| `life_v0/validators/` | 943 | 观察真值、world contact 和 cross-file 逻辑还可继续抽离 |
| `life_v0/schema_runner/` | 815 | 结构化执行与反事实比较仍可继续拆 manifest/ranker 侧器官 |
| `life_v0/body/` | 808 | 第二波对象已落，但 affect/fatigue 与语言/膜联动还需继续整理 |
| `life_v0/replay/` | 773 | replay cue / shadow replay / reentry 逻辑仍偏集中 |

## 逐包总图

### 1. `life_v0/direction/`

| 项 | 内容 |
|---|---|
| 生命职责 | 身份根、方向锁、断联恢复、自我连续体锚 |
| 必回读理论 | `构思.md`、`00`、`13`、`16`、`91`、`119`、`122`、`258` |
| 必回读 v0 | `s00_direction_foundation_engineering_contract.md`、`10_self_identity_value_commitment_implementation_playbook.md` |
| 已落器官 | `identity_root.py`、`direction_lock.py`、`continuity_refs.py`、`value_orientation.py` |
| 仍压在入口的职责 | direction receipt 汇总、resume anchor 组合、identity continuity 解释 |
| 下一轮优先拆分 | 保持现有文件，优先补 `LifeContextFrame` 装配与长期 continuity refs 的写回逻辑，不再继续长新顶层包 |
| runtime 产物 | `runtime/state/direction/direction_lock.json`、direction receipts、direction lock report |
| 测试 / gate | `tests/slices/test_direction_lock.py`、`direction_lock_gate` |

### 2. `life_v0/authority/`

| 项 | 内容 |
|---|---|
| 生命职责 | 权威来源层、机制证据图、文献 intake 与 carrier patch |
| 必回读理论 | 全部 `01*`、`142`、`145`、`151` |
| 必回读 v0 | `s01_source_authority_engineering_contract.md`、`theory_closure_and_engineering_readiness_audit.md` |
| 已落器官 | 当前主要集中在 `__init__.py` |
| 下一轮优先拆分 | `authority_registry.py`、`mechanism_evidence_map.py`、`doc_authority_patch_index.py`、`authority_intake.py` |
| runtime 产物 | `runtime/state/authority/authority_registry.json`、`mechanism_evidence_map.json`、source authority report |
| 测试 / gate | `tests/slices/test_source_authority.py`、`authority_registry_gate` |

### 3. `life_v0/state_store/`

| 项 | 内容 |
|---|---|
| 生命职责 | 生命状态根、自传连续体、关系记忆、承诺真值、记忆索引 |
| 必回读理论 | `05`、`17-31`、`41-48`、`55`、`57`、`61`、`69`、`01q` |
| 必回读 v0 | `s04_state_object_store_engineering_contract.md`、`life_state_store_v0_schema.md`、`05_memory_thought_consciousness_implementation_playbook.md` |
| 已落器官 | `life_state.py`、`self_model.py`、`relationship_memory.py`、`autobiographical_stack.py`、`engram_index.py`、`commitment_truth.py` |
| 仍压在入口的职责 | 统一 writeback、merge/correct policy、memory write gate、migration glue |
| 下一轮优先拆分 | `memory_write_gate.py`、`state_merge_guard.py`、`relationship_memory_writeback.py` |
| runtime 产物 | `runtime/state/life_state.json`、`runtime/state/self/*`、`runtime/state/relationship/*`、memory receipts |
| 测试 / gate | `tests/slices/test_state_store.py`、`state_store_gate`、`commitment_truth_gate` |

### 4. `life_v0/neural_core/`

| 项 | 内容 |
|---|---|
| 生命职责 | 主体图、网络态、信号介质、工作区、预测、元认知 |
| 必回读理论 | `02`、`03`、`10`、`11`、`18`、`22`、`30`、`143`、`146`、`01l`、`01m`、`01o`、`01p`、`01v-01ax` |
| 必回读 v0 | `s02_neural_life_core_engineering_contract.md`、`17_queue_c_memory_neural_core_implementation_contract.md`、`09_perception_prediction_world_contact_implementation_playbook.md` |
| 已落器官 | `brain_graph.py`、`network_state.py`、`workspace.py`、`broadcast.py`、`metacognition.py`、`prediction_workspace.py` |
| 仍压在入口的职责 | signal media 总线、belief state、prediction error、active sampling、workspace orchestration |
| 下一轮优先拆分 | `signal_media.py`、`belief_state.py`、`prediction_error.py`、`active_sampling.py` |
| runtime 产物 | `runtime/state/neural_life_core/neural_life_core.json`、`neural_life_internal_bus.json`、`runtime/state/prediction/*` |
| 测试 / gate | `tests/slices/test_neural_life_core.py`、`internal_bus_gate`、`prediction_coherence_gate` |

### 5. `life_v0/body/` 与 `life_v0/defense/`

| 项 | 内容 |
|---|---|
| 生命职责 | 节律、需要、资源预算、恢复、情绪底盘、风险保护 |
| 必回读理论 | `04`、`07`、`08`、`18`、`37-40`、`94`、`01g`、`01h`、`01n`、`01s` |
| 必回读 v0 | `s06_life_support_development_engineering_contract.md`、`18_queue_d_body_dream_growth_implementation_contract.md`、`08_cross_layer_life_orchestration_implementation_playbook.md` |
| 已落器官 | `rhythm.py`、`need_state.py`、`resource_budget.py`、`recovery.py`、`core_affect.py`、`emotion_episode.py`、`emotion_regulation.py`、`trait_drift.py` |
| 仍压在入口的职责 | affect 汇总、fatigue mode 切换、defense summary、跨回合 body report 组合 |
| 下一轮优先拆分 | `affective_debt.py`、`regret_signal.py`、`threat_eval.py`、`quarantine_signal.py` |
| runtime 产物 | `runtime/state/body/*`、`runtime/state/defense/*`、`body_resource_budget.json`、life support reports |
| 测试 / gate | `tests/slices/test_life_support.py`、`resource_budget_gate`、`core_affect_gate`、`quarantine_gate` |

### 6. `life_v0/language/`

| 项 | 内容 |
|---|---|
| 生命职责 | 语言感知、语义图、内言语、表达监控、关系表达、承诺修复 |
| 必回读理论 | `09`、`85-90`、`94`、`96`、`101`、`141`、`144`、`147`、`150`、`01f`、`01j`、`01u` |
| 必回读 v0 | `s07_language_relationship_engineering_contract.md`、`14_queue_a_language_percept_semantic_map_implementation_contract.md`、`04_language_dialogue_relationship_implementation_playbook.md` |
| 已落器官 | `percept.py`、`semantic_map.py`、`inner_speech.py`、`expression_monitor.py`、`language_state.py`、`relationship_graph.py`、`shared_terms.py`、`commitment_repair.py`、`dialogue_log.py`、`narrative_trace.py`、`dream_gate.py`、`action_shadow.py`、`relation_scope.py` |
| 仍压在入口的职责 | language report 组合、relation bridge 汇总、长期关系演化、修复表达独立输出 |
| 下一轮优先拆分 | `relationship_timeline.py`、`commitment_expression.py`、`apology_repair_language.py` |
| runtime 产物 | `runtime/state/language/*`、`runtime/state/relationship/*`、`language_relationship_report.json` |
| 测试 / gate | `tests/slices/test_language_organs.py`、`tests/slices/test_language_relationship.py`、`expression_monitor_gate`、`repair_language_gate` |

### 7. `life_v0/membrane/`、`life_v0/validators/`、`life_v0/schema_runner/`

| 项 | 内容 |
|---|---|
| 生命职责 | 候选行动、go/no-go、责任回路、观察真值、validator、反事实比较 |
| 必回读理论 | `06`、`20`、`22`、`29-36`、`49-84`、`94`、`98`、`102-118`、`01r`、`01v-01ax` |
| 必回读 v0 | `s03_direction_life_membrane_engineering_contract.md`、`s05_validation_membrane_observation_engineering_contract.md`、`s09_schema_runner_code_engineering_contract.md`、`20_queue_e_membrane_validator_logic_implementation_contract.md` |
| 已落器官 | `candidate_arena.py`、`go_nogo.py`、`world_contact_gate.py`、`side_effect_review.py`、`shadow_gate.py`、`observation_validator.py`、`boundary_audit.py`、`consistency_logic.py`、`counterfactual_eval.py`、`comparison_trace.py`、`evidence_ranker.py` |
| 仍压在入口的职责 | responsibility loop 装配、world contact summary、cross-file logic、run manifest 汇总 |
| 下一轮优先拆分 | `responsibility_loop.py` 补厚、`cross_file_logic.py`、`run_manifest.py`、`idle_strategy.py` |
| runtime 产物 | `runtime/state/membrane/*`、`runtime/state/action/*`、`runtime/state/validation/*`、`runtime/state/schema_runner/*` |
| 测试 / gate | `tests/slices/test_life_membrane.py`、`tests/slices/test_validation_membrane.py`、`tests/slices/test_schema_runner.py` |

### 8. `life_v0/dream/`、`life_v0/replay/`、`life_v0/archive/`

| 项 | 内容 |
|---|---|
| 生命职责 | replay cue、离线入口、梦境窗口、梦中事实门、醒后整合、归档 |
| 必回读理论 | `08`、`19`、`23`、`27`、`31`、`95`、`99`、`01i`、`01t`、`181-257` |
| 必回读 v0 | `s10_runtime_growth_reconsolidation_engineering_contract.md`、`18_queue_d_body_dream_growth_implementation_contract.md`、`08_cross_layer_life_orchestration_implementation_playbook.md` |
| 已落器官 | `offline_entry.py`、`dream_window.py`、`dream_fact_gate.py`、`wake_integration.py`、`nightmare_risk.py`、`shadow_replay.py` |
| 仍压在入口的职责 | replay cue 汇总、archive manifest、dream report 组合、reentry logic |
| 下一轮优先拆分 | `replay_cues.py`、`archive_manifest.py`、`growth_archive.py`、`replay_reentry.py` |
| runtime 产物 | `runtime/state/dream/*`、`runtime/state/replay/*`、`runtime/state/archive/*`、growth/archive reports |
| 测试 / gate | `tests/bridges/test_runtime_growth.py`、`tests/bridges/test_replay_shadow.py`、`tests/bridges/test_growth_archive.py` |

### 9. `life_v0/growth/`

| 项 | 内容 |
|---|---|
| 生命职责 | 可塑性、自我阅读、学习窗口、防遗忘、关系/语言/信念学习 |
| 必回读理论 | `39`、`92`、`93`、`97`、`181-257`、`01g` |
| 必回读 v0 | `s06_life_support_development_engineering_contract.md`、`s10_runtime_growth_reconsolidation_engineering_contract.md`、`18_queue_d_body_dream_growth_implementation_contract.md`、`10_self_identity_value_commitment_implementation_playbook.md` |
| 已落器官 | `plasticity_window.py`、`learning_window.py`、`patch_queue.py`、`self_read.py`、`anti_forgetting.py`、`belief_learning.py`、`language_learning.py`、`relationship_learning.py` |
| 仍压在入口的职责 | growth route orchestration、patch review 汇总、next feedback seed、cross-package learning writeback |
| 下一轮优先拆分 | `self_patch_review.py`、`core_continuity_guard.py`、`value_revision.py`、`next_feedback_seed.py` |
| runtime 产物 | `runtime/state/growth/*`、growth reports、archive receipts |
| 测试 / gate | `tests/bridges/test_runtime_growth.py`、`tests/slices/test_life_support.py`、`growth_gate`、`anti_forgetting_gate` |

### 10. `life_v0/life_targets/`

| 项 | 内容 |
|---|---|
| 生命职责 | 九项目标 claim/evidence/rollup、出生准备度、意识 probe |
| 必回读理论 | `10`、`91-101`、`143`、`146`、`149`、`152`、`171`、`174`、`01m` |
| 必回读 v0 | `s08_life_target_runtimes_engineering_contract.md`、`birth_readiness_v0_contract.md`、`21_queue_f_identity_consciousness_birth_readiness_implementation_contract.md` |
| 已落器官 | `life_target_claims.py`、`evidence_matrix.py`、`birth_readiness_rollup.py`、`birth_readiness_stage_gate.py`、`consciousness_probes.py` |
| 仍压在入口的职责 | target runtime orchestration、probe 汇总、claim/evidence 交叉验证 |
| 下一轮优先拆分 | `target_runtime.py`、`target_closure.py`、`probe_battery.py` |
| 当前说明 | `life_target_claims.py`、`evidence_matrix.py`、`birth_readiness_rollup.py`、`birth_readiness_stage_gate.py`、`consciousness_probes.py` 已经落下，上一行列的是下一轮若继续细分 `__init__.py` 时的候选位 |
| runtime 产物 | `runtime/state/life_targets/*`、`birth_readiness_report.json` |
| 测试 / gate | `tests/slices/test_life_targets.py`、`birth_readiness_gate` |

### 11. `life_v0/activation/`、`life_v0/reporting/`、`life_v0/stage_explain/`、`life_v0/digital_life/`、`life_v0/shell_command/`

| 项 | 内容 |
|---|---|
| 生命职责 | 出生链、回包、阶段解释、one-shot restore shell |
| 必回读理论 | `20`、`44-46`、`89-90`、`181-257` |
| 必回读 v0 | `first_activation_protocol.md`、`runner_cli_report_contract.md`、`07_birth_terminal_process_implementation_playbook.md` |
| 已落器官 | 对应包中已有最小 bridge 命令和 state/report 组合逻辑 |
| 仍压在入口的职责 | packet/digest 组合、strict route 汇总、receipt index |
| 下一轮优先拆分 | `preflight.py`、`return_packet.py`、`report_bundle.py`、`receipt_index.py`、`birth_shell.py`、`birth_digest.py`、`restore_shell.py` |
| runtime 产物 | `first_activation_return_packet.json`、`report_bundle.json`、`digital_life_birth_packet.json`、`digital_life_shell_report.json` |
| 测试 / gate | `tests/bridges/test_first_activation_preflight.py`、`test_emit_report.py`、`test_explain_stage.py`、`test_digital_life_birth.py`、`tests/process/test_digital_life_shell_command.py` |

### 12. `life_v0/terminal_turn/`、`life_v0/terminal_loop/`、`life_v0/process_supervisor/`

| 项 | 内容 |
|---|---|
| 生命职责 | 第一回合恢复、持续回合、等待态、常驻存在、incident/relaunch recovery |
| 必回读理论 | `20`、`81-82`、`86`、`89-90`、`96`、`101`、`181-257` |
| 必回读 v0 | `first_terminal_turn_engineering_contract.md`、`terminal_life_loop_engineering_contract.md`、`digital_life_process_supervisor_engineering_contract.md`、`16_queue_b_process_supervisor_implementation_contract.md` |
| 已落器官 | `restore_context.py`、`context_accumulation.py`、`turn_transition.py`、`turn_packet.py`、`conversation_carryover.py`、`dialogue_turn.py`、`loop_state.py`、`resume_packet.py`、`dialogue_writeback.py`、`loop_report.py`、`heartbeat.py`、`continuity_writeback.py`、`turn_io.py`、`dialogue_events.py`、`response_surface.py`、`incident_recovery.py`、`relaunch_recovery.py`、`idle_strategy.py`、`persistent_process.py`、`process_report.py` |
| 仍压在入口的职责 | remaining resume orchestration |
| 下一轮优先拆分 | `persistent_wait_bridge.py` |
| runtime 产物 | `session_envelope.json`、`context_accumulation_window.json`、`turn_transition_trace.json`、`terminal_life_loop_state.json`、`digital_life_waiting_heartbeat.json`、`digital_life_process_report.json` |
| 测试 / gate | `tests/bridges/test_first_terminal_turn.py`、`tests/bridges/test_terminal_life_loop.py`、`tests/process/test_digital_entrypoint.py`、`tests/process/test_persistent_digital_life_process.py` |

## 当前施工顺序

后续逐包拆分不要乱序，固定按下面理解：

1. `Queue D`：先补身体、梦境、成长链的剩余器官与跨层 writeback。
2. `Queue E`：再补候选行动、责任回路、validator、evidence rank。
3. `Queue B`：再补 waiting heartbeat、idle strategy、persistent process。
4. `Queue A`：再深补关系时间线、承诺表达、修复语言。
5. `Queue C/F`：作为维护回切，继续细分 neural core / life targets / state store 剩余重职责。

这份顺序的意义不是忽视语言，而是让语言、关系和常驻存在建立在更厚的身体化、梦境化、责任化底盘上。
