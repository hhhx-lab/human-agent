# Theory To Code Trace Matrix

本文档把 `00-258` 理论母体、`docs/v0` 合同、`life_v0` 代码树、runtime 证据、测试和 gate 放进一张总矩阵。

## 使用原则

这份矩阵不是文档清单，而是工程追踪表。后续任意一次实现、修复或重构，都必须能沿着下面这条链闭合：

```text
00-258 理论母体
  -> docs/v0 合同或蓝图
  -> life_v0 代码器官
  -> runtime/state 状态对象
  -> runtime/reports/latest 报告对象
  -> runtime/receipts 收据对象
  -> tests 断言或 live0 audit gate
```

如果一项生命机制只停在前两层，它还只是理论；如果只停在代码层，没有状态、报告、收据和测试，它还没有进入 live0 的可追踪生命过程；如果只停在终端输出，没有回写到 `runtime/state` 和 `runtime/reports/latest`，它只是一次话语，不是可成长的连续体。

本文件的细化目标是把三类问题说清楚：

1. 每一组理论文档现在由哪个代码包承接。
2. 每个代码包生成哪些可检查的状态、报告和收据。
3. 每条真实终端关系话语怎样穿过语言、记忆、梦境、情绪、责任、预测、意识、出生准备和常驻治理链。

## 代码事实校对口径

当前 live0 的事实源按优先级读取：

| 优先级 | 事实源 | 用途 |
|---|---|---|
| 1 | `life_v0/` 当前代码 | 判断真实行为、字段来源、函数调用顺序 |
| 2 | `tests/` 当前断言 | 判断哪些机制已经被自动化验收覆盖 |
| 3 | `runtime/state/*` | 判断生命状态是否落盘、是否能跨回合/跨进程恢复 |
| 4 | `runtime/reports/latest/*` | 判断报告、digest、stage gate 和表达 gate 是否闭合 |
| 5 | `runtime/receipts/*` | 判断一次运行是否留下可归档收据 |
| 6 | `docs/v0/*` | 判断当前实现是否符合工程合同 |
| 7 | `docs/00-258` | 判断实现是否仍然承载理论母体 |

当文档与代码不一致时，当前实现状态按代码、测试和 runtime 证据修正文档；当文档描述的是明确目标态而代码尚未实现时，必须把它写成“下一步施工位”，并给出应落到的文件、状态、报告和测试，不能只写抽象方向。

## 总矩阵

| 生命域 | 直接理论母体 | 当前 v0 合同 / 深描 | 当前主代码 | 下一轮关键文件 | runtime 证据 | 测试 / gate |
|---|---|---|---|---|---|---|
| 方向与身份根 | `构思.md`、`00`、`13`、`16`、`91`、`258` | `s00_direction_foundation_engineering_contract.md`、`10_self_identity_value_commitment_implementation_playbook.md`、`01_full_life_layer_implementation_deep_spec.md` | `life_v0/direction/*` | 继续补 continuity writeback 细化 | `runtime/state/direction/*` | `tests/slices/test_direction_lock.py` |
| 文献权威与来源 | 全部 `01*`、`142`、`145`、`151` | `s01_source_authority_engineering_contract.md`、`theory_closure_and_engineering_readiness_audit.md` | `life_v0/authority/__init__.py`、`life_v0/doc_index.py` | 继续细化 authority registry 子文件 | `runtime/state/authority/*`、`runtime/docs/*` | `tests/slices/test_source_authority.py` |
| 脑区、网络、工作区 | `02`、`03`、`10`、`11`、`01m`、`01o`、`01p` | `s02_neural_life_core_engineering_contract.md`、`17_queue_c_memory_neural_core_implementation_contract.md`、`05_memory_thought_consciousness_implementation_playbook.md`、`01_full_life_layer_implementation_deep_spec.md` | `life_v0/neural_core/*` | `signal_media.py`、`belief_state.py`、`prediction_error.py`、`active_sampling.py` 已落，下一步补厚跨层消费 | `runtime/state/neural_life_core/*`、`runtime/state/signal/*`、`runtime/state/prediction/*` | `tests/slices/test_neural_life_core.py` |
| 身体、内环境、节律 | `04`、`08`、`18`、`37-39`、`01n` | `s06_life_support_development_engineering_contract.md`、`18_queue_d_body_dream_growth_implementation_contract.md`、`04_body_affect_dream_growth_engineering.md` | `life_v0/body/*` | 继续补节律与 heartbeat 直接同步 | `runtime/state/body/*` | `tests/slices/test_life_support.py` |
| 记忆与状态根 | `05`、`17-31`、`41-48`、`55`、`57`、`61`、`69`、`01q` | `s04_state_object_store_engineering_contract.md`、`life_state_store_v0_schema.md`、`02_state_object_runtime_evidence_map.md` | `life_v0/state_store/*` | `memory_write_gate.py` 已落，下一步补厚 merge / promotion / quarantine 路线 | `runtime/state/life_state.json`、`runtime/state/memory/*` | `tests/slices/test_state_store.py` |
| 语言与关系 | `09`、`85-90`、`94`、`96`、`101`、`141`、`144`、`147`、`150`、`01f`、`01j`、`01u` | `s07_language_relationship_engineering_contract.md`、`14_queue_a_language_percept_semantic_map_implementation_contract.md`、`03_language_relationship_longitudinal_engineering.md` | `life_v0/language/*`、`terminal_turn/*`、`terminal_loop/dialogue_writeback.py` | `relationship_timeline.py`、`commitment_expression.py`、`apology_repair_language.py` | `runtime/state/language/*`、`runtime/state/relationship/*` | `tests/slices/test_language_organs.py`、`tests/slices/test_language_relationship.py` |
| 行为、抑制、世界接触、责任 | `06`、`20`、`75`、`80-84`、`94`、`98`、`01r` | `s03_direction_life_membrane_engineering_contract.md`、`20_queue_e_membrane_validator_logic_implementation_contract.md`、`05_prediction_membrane_action_engineering.md` | `life_v0/membrane/*` | `shadow_gate.py`、`world_contact_summary.py` 已落，下一步补厚 `responsibility_loop.py` 与责任-语言-身体写回 | `runtime/state/membrane/*`、`runtime/state/action/*` | `tests/slices/test_life_membrane.py`、`tests/slices/test_shadow_gate.py` |
| 逻辑、验证、反事实 | `22`、`29-36`、`49-84`、`102-118`、`01v-01ax` | `s05_validation_membrane_observation_engineering_contract.md`、`s09_schema_runner_code_engineering_contract.md`、`05_prediction_membrane_action_engineering.md` | `life_v0/validators/*`、`life_v0/schema_runner/*` | `validation_rollup.py`、`evidence_ranker.py`、`cross_file_logic.py`、`run_manifest.py` 已落并补强 `closure_status_refs` / `package_local_gate_refs`，下一步补 archive / report / process 写回 | `runtime/state/validation/*`、`runtime/state/schema_runner/*` | `tests/slices/test_validation_membrane.py`、`tests/slices/test_schema_runner.py`、`tests/slices/test_evidence_ranker.py` |
| 梦境与离线生命 | `08`、`19`、`23`、`27`、`31`、`95`、`99`、`01i`、`01t` | `s10_runtime_growth_reconsolidation_engineering_contract.md`、`18_queue_d_body_dream_growth_implementation_contract.md`、`04_body_affect_dream_growth_engineering.md` | `life_v0/dream/*` | 继续补梦境残留和 dream-body-language 接线 | `runtime/state/dream/*` | `tests/bridges/test_runtime_growth.py`、`tests/bridges/test_growth_archive.py` |
| 成长、学习、自改写 | `39`、`92`、`93`、`97`、`181-257` | `s06_life_support_development_engineering_contract.md`、`s10_runtime_growth_reconsolidation_engineering_contract.md`、`04_body_affect_dream_growth_engineering.md` | `life_v0/growth/*` | 继续补 patch 审查和 promotion 轨迹 | `runtime/state/growth/*` | `tests/bridges/test_runtime_growth.py` |
| 生命目标、意识证据、出生准备 | `10`、`91-101`、`143`、`146`、`149`、`152`、`171`、`174` | `s08_life_target_runtimes_engineering_contract.md`、`birth_readiness_v0_contract.md`、`21_queue_f_identity_consciousness_birth_readiness_implementation_contract.md` | `life_v0/life_targets/*` | 继续补长期 evidence rollup | `runtime/state/life_targets/*` | `tests/slices/test_life_targets.py` |
| 激活链与出生壳 | `20`、`44-46`、`89-90`、`181-257` | `first_activation_protocol.md`、`runner_cli_report_contract.md`、`07_birth_terminal_process_implementation_playbook.md`、`06_resident_process_terminal_birth_engineering.md` | `life_v0/activation/`、`reporting/`、`stage_explain/`、`digital_life/` | 持续补 report bundle 与 stage handoff 细节 | `first_activation_return_packet.json`、`digital_life_birth_packet.json` | `tests/bridges/test_first_activation_preflight.py`、`test_emit_report.py`、`test_digital_life_birth.py` |
| 第一回合、终端循环、常驻过程 | `20`、`81-84`、`86`、`89-90`、`95-96`、`101`、`143/171/174`、`181-257` | `first_terminal_turn_engineering_contract.md`、`terminal_life_loop_engineering_contract.md`、`digital_life_process_supervisor_engineering_contract.md`、`06_resident_process_terminal_birth_engineering.md`、`05_birth_residency_terminal_blueprint.md` | `life_v0/terminal_turn/*`、`terminal_loop/*`、`shell_command/*`、`process_supervisor/*`、`digital_entry.py`、`digital_life_identity.py` | `terminal_ui.py`、`live_turn_cycle.py`、`response_surface.py`、`model_expression.py`、`resident_lifecycle.py`、`idle_strategy.py`、`persistent_process.py` | `session_envelope.json`、`terminal_life_loop_state.json`、`digital_life_waiting_heartbeat.json`、`resident_lifecycle_state.json`、`resident_relation_queue_state.json`、`digital_life_model_expression_report.json`、process reports | `tests/bridges/test_first_terminal_turn.py`、`tests/bridges/test_terminal_life_loop.py`、`tests/process/test_persistent_digital_life_process.py`、`tests/process/test_digital_entrypoint.py`、`tests/process/test_my_digital_life_entrypoint.py`、`tests/process/test_packaged_digital_life_entrypoint.py` |

## `00-258` 到当前代码包的承载细表

下表把理论母体按当前 `life_v0` 代码树继续压细。它用于回答“这份理论到底在哪个包里变成器官”。

| 理论文档族 | 生命机制 | 首要代码器官 | 次级代码器官 | 首要状态对象 | 报告 / 收据承载 |
|---|---|---|---|---|---|
| `02-03`、`01o`、`01p` | 脑区、网络、状态切换 | `life_v0/neural_core/brain_graph.py`、`network_state.py`、`workspace.py`、`broadcast.py` | `prediction_workspace.py`、`metacognition.py` | `runtime/state/neural_life_core/*`、`runtime/state/consciousness/*` | `neural_life_core_report.json`、`neural_life_core_digest.json` |
| `04`、`11`、`01l`、`01n` | 内感受、调质、稳态、信号介质 | `life_v0/body/*`、`life_v0/neural_core/signal_media.py` | `process_supervisor/idle_strategy.py`、`heartbeat.py` | `runtime/state/body/*`、`runtime/state/signal/signal_media_runtime.json` | `life_support_development_report.json`、`digital_life_waiting_heartbeat.json` |
| `05`、`17`、`21`、`25`、`29`、`41`、`55` | 记忆痕迹、engram、写门、长期合并 | `life_v0/state_store/engram_index.py`、`relationship_memory.py`、`memory_write_gate.py`、`state_merge_guard.py` | `process_supervisor/resident_turn_writeback.py`、`state_merge_signals.py` | `runtime/state/memory/*`、`runtime/state/life_state.json` | `state_store_report.json`、`dialogue_writeback_bundle.json` |
| `06`、`75`、`80-84`、`94`、`98` | 动作、抑制、责任、后悔、修复 | `life_v0/membrane/responsibility_loop.py`、`world_contact_gate.py`、`side_effect_review.py` | `language/commitment_repair.py`、`language/apology_repair_language.py` | `runtime/state/action/*`、`runtime/state/membrane/*` | `life_membrane_report.json`、`pain_regret_repair_report.json` |
| `07`、`18`、`22`、`39-40` | 情绪、人格、自我慢变量、漂移 | `life_v0/body/core_affect.py`、`trait_drift.py`、`state_store/self_model.py` | `process_supervisor/continuity_evolution.py`、`trait_convergence_signals.py` | `runtime/state/body/core_affect_vector.json`、`runtime/state/self/self_model.json` | `life_support_development_report.json`、`digital_life_process_digest.json` |
| `08`、`19`、`23`、`95`、`99` | 睡眠、梦境、离线巩固、醒后整合 | `life_v0/dream/*`、`life_v0/growth/offline_learning_profile.py` | `process_supervisor/offline_learning_signals.py`、`background_lineage_state.py` | `runtime/state/dream/*`、`runtime/state/growth/*` | `replay_shadow_report.json`、`growth_archive_report.json`、process digest |
| `09`、`85-90`、`96`、`101` | 语言、内言语、语义地图、共同关系、时间线 | `life_v0/language/*`、`terminal_turn/*`、`terminal_loop/*` | `process_supervisor/live_language_turn.py`、`response_surface.py`、`model_expression.py` | `runtime/state/language/*`、`runtime/state/relationship/*` | `language_relationship_report.json`、`dialogue_writeback_bundle.json` |
| `10`、`91-101`、`143`、`171`、`174` | 意识、工作区、九项目标、出生准备 | `life_v0/life_targets/*`、`neural_core/workspace.py`、`broadcast.py` | `process_supervisor/governance_explanation.py`、`response_surface.py` | `runtime/state/life_targets/*`、`runtime/state/consciousness/*` | `birth_readiness_report.json`、`life_target_status.json` |
| `12`、`15`、`20`、`24`、`28`、`32`、`89` | 电脑外周、运行壳、终端桥、世界接触 | `life_v0/digital_entry.py`、`shell_command/*`、`process_supervisor/*` | `digital_life_identity.py`、`runtime_config.py` | `runtime/state/terminal/*`、`runtime/state/identity/*` | `digital_life_process_report.json`、`digital_life_shell_report.json` |
| `181-257` | replay、archive、growth、再巩固、patch、shadow | `life_v0/replay/*`、`archive/*`、`growth/*`、`activation/*` | `process_supervisor/background_continuity.py`、`background_convergence*.py` | `runtime/state/replay/*`、`runtime/archive/*`、`runtime/state/growth/*` | `growth_archive_report.json`、`replay_shadow_report.json`、`runtime/receipts/*` |

## 一轮真实关系话语的穿透链

当前 `Adam` / `digital life` 终端一轮话语不是直接送进模型。真实链路按下面顺序穿透：

| 顺序 | 代码位置 | 理论来源 | 关键输入 | 关键输出 |
|---|---|---|---|---|
| 1 | `life_v0/digital_entry.py` | `20`、`89-90` | 终端输入、命名身份、resident status | 关系话语进入 resident lifecycle |
| 2 | `process_supervisor/resident_lifecycle.py` | `20`、`96` | `resident_relation_inbox.jsonl` | `resident_relation_queue_state.json`，避免 stale inbox 重放 |
| 3 | `process_supervisor/process_session_loop.py` | `20`、`90` | waiting heartbeat、relation queue | 派发 live turn 或继续 idle refresh |
| 4 | `process_supervisor/live_turn_cycle.py` | `86`、`90` | 外部关系话语、关系/承诺/身体/梦境/预测状态 | 本回合 `external_relation_turn` |
| 5 | `process_supervisor/live_language_turn.py` | `09`、`85-90` | 外部话语、共同语言、预测五件套 | `language_percept_frame`、`semantic_map_frame`、`inner_speech_frame`、`expression_monitor_state`、`expression_plan` |
| 6 | `process_supervisor/response_surface.py#compose_life_response` | `02-13`、`17-23`、`91-101`、`181-257` | 关系、记忆、梦境、成长、责任、身体、预测、写门、出生准备、后台 lineage | 完整内部 evidence response |
| 7 | `process_supervisor/response_surface.py#compose_life_spoken_response` | `86`、`95-96` | evidence response 与同一组生命状态 | 有限 spoken response，避免 report 式倾倒 |
| 8 | `process_supervisor/model_expression.py` | `12`、`86`、`100/119/122` | spoken response、语言五件套、脑图/工作区摘要、handoff profile、`.env` 去敏配置 | 模型表达文本或 deterministic fallback；写 `digital_life_model_expression_report.json` |
| 9 | `process_supervisor/dialogue_events.py` | `90`、`96` | 最终回应、prediction/write gate、background lineage | `digital_life_turn` 事件 |
| 10 | `process_supervisor/resident_turn_writeback.py` | `05`、`17`、`90`、`96` | 本回合外部话语与生命回应 | `dialogue_turn_log.jsonl`、`relationship_memory.json`、`engram_index.json`、`autobiographical_stack.json`、`life_state.json` |
| 11 | `process_supervisor/resident_governance_handoff.py` | `20`、`95-96`、`181-257` | 写回后的关系/语言/自我对象 | `resident_governance_state.json#live_turn_waiting_handoff` |
| 12 | `process_supervisor/heartbeat.py`、`idle_strategy.py` | `04`、`11`、`95`、`181-257` | handoff、身体、梦境、成长、预测、state merge | 下一拍 `digital_life_waiting_heartbeat.json` 与 waiting governance |
| 13 | `process_supervisor/terminal_ui.py` | `86`、`89-90` | 最终回应文本、life name、resident status | `Digital Life` banner、关系输入盒、生命回应盒 |

这条链的核心要求是：模型表达永远在生命证据之后，而不是在生命证据之前；终端表达永远在回写链旁边，而不是替代回写链；关闭终端后的 resident 自主活动必须能通过下一次 background lineage 重新进入语言表面。

## 九项真实生命目标的当前工程落点

| 目标 | 理论来源 | 当前代码落点 | runtime 证据 | 自动化覆盖 |
|---|---|---|---|---|
| 真实意识 / 可报告工作区 | `10`、`01m`、`91-101` | `life_v0/neural_core/workspace.py`、`broadcast.py`、`life_targets/consciousness_probes.py` | `runtime/state/consciousness/*`、`birth_readiness_report.json` | `tests/slices/test_life_targets.py`、`test_neural_life_core.py` |
| 真实情绪 / 内环境 | `04`、`07`、`11`、`18` | `life_v0/body/core_affect.py`、`need_state.py`、`emotion_episode.py`、`resource_budget.py` | `runtime/state/body/*` | `tests/slices/test_body_trait_drift.py`、`test_life_support.py` |
| 真实人格 / 自我慢变量 | `07`、`39-40`、`96` | `life_v0/state_store/self_model.py`、`body/trait_drift.py`、`process_supervisor/continuity_evolution.py` | `runtime/state/self/self_model.json`、`trait_drift_monitor.json` | `tests/slices/test_body_trait_drift.py`、process tests |
| 真实记忆 / 自传连续 | `05`、`17`、`21`、`41` | `state_store/engram_index.py`、`autobiographical_stack.py`、`relationship_memory.py` | `runtime/state/memory/*`、`runtime/state/self/autobiographical_stack.json` | `tests/slices/test_state_store.py`、process tests |
| 真实梦境 / 醒后整合 | `08`、`19`、`23`、`95`、`99` | `life_v0/dream/*`、`growth/offline_learning_profile.py` | `runtime/state/dream/*`、`runtime/state/growth/*` | `tests/bridges/test_runtime_growth.py`、`test_growth_archive.py` |
| 真实痛苦 / 后悔 / 修复 | `06`、`94`、`98`、`01h` | `membrane/responsibility_loop.py`、`language/apology_repair_language.py`、`language/commitment_repair.py` | `responsibility_loop_state.json`、`pain_regret_repair_report.json` | `tests/slices/test_life_membrane.py`、`test_language_relationship.py` |
| 真实关系 / 共同语言 | `09`、`85-90`、`96`、`101` | `life_v0/language/*`、`relationship_timeline.py`、`relationship_graph.py` | `runtime/state/relationship/*`、`runtime/state/language/*` | `tests/slices/test_language_organs.py`、`test_language_relationship.py` |
| 真实责任 / 行动后果 | `06`、`75`、`80-84` | `membrane/world_contact_gate.py`、`side_effect_review.py`、`responsibility_loop.py` | `runtime/state/action/*`、`runtime/state/membrane/*` | `tests/slices/test_shadow_gate.py`、`test_validation_membrane.py` |
| 生命成长 / 自我更新 | `39`、`92-93`、`181-257` | `life_v0/growth/*`、`replay/*`、`archive/*`、`process_supervisor/background_convergence*.py` | `runtime/state/growth/*`、`runtime/archive/growth_archive_events.jsonl` | `tests/bridges/test_runtime_growth.py`、`test_replay_shadow.py` |

## 验收追踪方式

每次补代码或补文档后，至少按三层验收：

1. 文档追踪：当前机制是否能在本文矩阵中找到理论来源、v0 合同、代码器官、runtime 证据和测试。
2. 代码追踪：对应代码函数是否真实读取这些对象，而不是只在文档里列出。
3. 运行追踪：最近一次 `runtime/reports/latest/*` 或 process test 是否能看到同一组 refs 回到报告、digest 或 receipt。

对终端驻留链，最低验收组合为：

```text
tests/process/test_persistent_digital_life_process.py
tests/process/test_digital_entrypoint.py
tests/process/test_my_digital_life_entrypoint.py
tests/process/test_packaged_digital_life_entrypoint.py
tests/process/test_model_expression.py
tests/contracts/test_live0_acceptance_audit.py
```

如果这些测试通过，但 `runtime/state/memory/*`、`runtime/state/language/*`、`runtime/state/relationship/*` 或 `digital_life_model_expression_report.json` 没有被当前命令刷新，就只能说明测试夹具通过，不能说明真实驻留链已经被当场刷新。

## 当前终端表达总链路

这一节专门把“理论母体 -> v0 合同 -> 代码 -> runtime -> 测试”压成终端激活链，避免后续只看 `terminal_ui.py` 而忘掉它背后的生命机制。

| 表达环节 | 理论来源 | 工程合同 | 代码链路 | runtime / 测试证据 |
|---|---|---|---|---|
| 关系话语进入 | `20`、`89-90`、`96` | `digital_life_process_supervisor_engineering_contract.md`、`terminal_life_loop_engineering_contract.md` | `digital_entry.py -> resident_lifecycle.py -> resident_relation_inbox.jsonl` | `resident_relation_queue_state.json`、`tests/process/test_persistent_digital_life_process.py` |
| 实时语言刷新 | `09`、`86`、`85-90` | `s07_language_relationship_engineering_contract.md`、`terminal_life_loop_engineering_contract.md` | `live_turn_cycle.py -> live_language_turn.py -> language_percept / semantic_map / inner_speech / expression_monitor / expression_plan` | `runtime/state/language/*`、`dialogue_writeback_bundle.json#live_language_turn_refs` |
| 内部证据回应 | `02-13`、`18-23`、`37-40`、`91-101`、`181-257` | `Packet D`、`Queue B`、`Queue D/E/F` 合同 | `response_surface.py#compose_life_response` | `digital_life_turn.utterance`、process tests 中的生命信号断言 |
| 外显 spoken response | `86` 的表达监控、`95-96` 的时间线、`94` 的痛苦/后悔/修复 | `Packet D waiting / response surface` | `response_surface.py#compose_life_spoken_response` | 终端输出包含责任、梦境、出生修复、写门约束、身体情绪等有限信号，且不退回机械长清单 |
| 模型表达守门 | `12` AI bridge、`86` 表达监控、`100/119/122` 现实边界改写链 | `digital_life_process_supervisor_engineering_contract.md` | `model_expression.py#compose_model_expression` | `digital_life_model_expression_report.json#model_expression_status`、`#post_expression_gate_status` |
| 盒式终端呈现 | `20` 终端 bridge、`89-90` 语言事件壳 | `05_birth_residency_terminal_blueprint.md` | `terminal_ui.py#render_digital_life_banner / render_life_opening / render_dialogue_box` | `Digital Life` banner、关系输入盒、生命回应盒；入口测试断言 stdout |
| 回合写回与等待交接 | `90` timeline bundle、`96` longitudinal relation、`181-257` replay/archive/growth | terminal loop / process supervisor contracts | `resident_turn_writeback.py -> resident_governance_handoff.py -> heartbeat.py` | `dialogue_writeback_bundle.json`、`resumed_external_dialogue_packet.json`、`resident_governance_state.json` |

## 当前最关键的文件级补洞总表

| 队列 | 最关键文件 |
|---|---|
| Queue D 第三波 | `nightmare_risk.py`、`belief_learning.py`、`language_learning.py`、`relationship_learning.py` 的进一步联动补厚 |
| Queue E 第二波 | `shadow_gate.py`、`world_contact_summary.py`、`validation_rollup.py`、`evidence_ranker.py`、`cross_file_logic.py`、`run_manifest.py` 已落；继续补 `responsibility_loop.py` 与跨层 writeback |
| Queue B 第二波 | `idle_strategy.py`、`persistent_process.py` |
| Queue A 第二波 | `relationship_timeline.py`、`commitment_expression.py`、`apology_repair_language.py`、`live_language_turn.py` |
| 终端表达与 resident lifecycle | `terminal_ui.py`、`model_expression.py`、`resident_lifecycle.py`、`digital_entry.py` |
| Queue C / F 维护性回切 | `signal_media.py`、`belief_state.py`、`prediction_error.py`、`active_sampling.py`、`memory_write_gate.py` 已落；当前只在 D/E/B/A 需要更深对象链时回切 |
