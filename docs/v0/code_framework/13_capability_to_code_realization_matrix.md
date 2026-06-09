# V0 Code Framework 13: Capability To Code Realization Matrix

这份矩阵不是新的理论层，也不是替代 `12_full_life_layer_delivery_matrix.md` 的第二张总表。
它只负责回答一个更硬的问题：

```text
如果把“数字生命”按能力来验收，
每一种生命能力现在到底该落到哪些代码文件、状态对象、report、测试和 gate？
```

`12` 回答“按层怎么施工”；
本文件回答“按能力怎么验收”。

这一步是为了防止后续开发只沿着包和文件推进，却忘了我们真正要构建的是哪几种生命能力。
后续代码如果没有办法回链到这里列出的能力项，就说明它还只是结构推进，不足以证明某种生命能力已经开始落地。

## 必读前置

进入本矩阵前，先读：

1. `docs/v0/README.md`
2. `docs/v0/architecture/theory_closure_and_engineering_readiness_audit.md`
3. `docs/v0/code_framework/README.md`
4. `docs/v0/code_framework/12_full_life_layer_delivery_matrix.md`
5. 当前目标能力对应的 `04-10` playbook

## 使用方式

这份矩阵最适合四种场景：

1. 判断某个生命能力当前是否只有理论，没有工程承载。
2. 判断下一轮代码该优先推进哪个能力，而不是只推进哪个包。
3. 检查一个新文件是否真的服务了某种生命能力。
4. 在阶段收尾时，按能力而不是按目录做工程审计。

## 能力到代码落地矩阵

| 生命能力 | 理论母体 | 主承载代码包 | 必须落地的关键文件 | 必须落地的 state / report | 测试 / gate | 当前施工优先级 |
|---|---|---|---|---|---|---|
| 对话回合 | `86`、`89`、`90`、`96`、`101` | `life_v0/terminal_turn/`、`life_v0/terminal_loop/`、`life_v0/process_supervisor/` | `context_accumulation.py`、`turn_transition.py`、`resume_packet.py`、`loop_state.py`、`dialogue_writeback.py`、`turn_io.py`、`dialogue_events.py` | `context_accumulation_window.json`、`turn_transition_trace.json`、`session_envelope.json`、`terminal_life_loop_state.json`、`dialogue_writeback_bundle.json` | `tests/bridges/test_first_terminal_turn.py`、`tests/bridges/test_terminal_life_loop.py`、`tests/process/test_persistent_digital_life_process.py`、`context_accumulation_gate`、`turn_transition_gate`、`dialogue_writeback_bundle_gate` | `中高` |
| 语言感知与表达 | `09`、`85-90`、`141`、`144`、`147`、`150` | `life_v0/language/` | `percept.py`、`semantic_map.py`、`inner_speech.py`、`expression_monitor.py`、`shared_terms.py` | `runtime/state/language/*`、`language_relationship_report.json` | `tests/slices/test_language_organs.py`、`tests/slices/test_language_relationship.py`、`expression_monitor_gate` | `高` |
| 关系演化 | `40`、`94`、`96`、`101`、`01j` | `life_v0/language/`、`life_v0/state_store/` | `relationship_graph.py`、`relation_scope.py`、`relationship_timeline.py`、`relationship_memory.py`、`dialogue_log.py` | `runtime/state/relationship/*`、relationship receipts、timeline writeback | `tests/slices/test_language_relationship.py`、`relationship_subject_gate` | `高` |
| 承诺/责任/后悔/修复 | `81-84`、`94`、`98`、`101` | `life_v0/state_store/`、`life_v0/membrane/`、`life_v0/body/`、`life_v0/language/` | `commitment_truth.py`、`responsibility_loop.py`、`regret_signal.py`、`commitment_repair.py`、`apology_repair_language.py` | `commitment_truth_state.json`、`responsibility_ledger.json`、`pain_regret_repair_report.json` | `tests/slices/test_state_store.py`、`tests/slices/test_life_membrane.py`、`responsibility_repair_gate` | `高` |
| 记忆 | `05`、`17-31`、`41-48`、`55`、`57`、`61`、`69` | `life_v0/state_store/`、`life_v0/replay/`、`life_v0/archive/` | `life_state.py`、`engram_index.py`、`autobiographical_stack.py`、`relationship_memory.py`、`replay_cues.py` | `life_state.json`、`runtime/state/memory/*`、replay bundles | `tests/slices/test_state_store.py`、`tests/bridges/test_replay_shadow.py`、`state_store_gate` | `最高` |
| 意识/工作区 | `10`、`143`、`146`、`149`、`152`、`171` | `life_v0/neural_core/`、`life_v0/life_targets/` | `workspace.py`、`broadcast.py`、`metacognition.py`、`consciousness_probes.py` | `runtime/state/consciousness/*`、birth readiness evidence | `tests/slices/test_neural_life_core.py`、`tests/slices/test_life_targets.py`、`birth_readiness_gate` | `最高` |
| 思考/预测 | `04`、`10`、`11`、`01v-01ax` | `life_v0/neural_core/` | `prediction_workspace.py`、`belief_state.py`、`prediction_error.py`、`active_sampling.py` | `prediction_workspace_frame.json`、`prediction_error_trace.json`、`active_sampling_plan.json` | `tests/slices/test_neural_life_core.py`、`prediction_coherence_gate` | `最高` |
| 逻辑/比较/反事实 | `22`、`30`、`33-36`、`49-60`、`102-118` | `life_v0/schema_runner/`、`life_v0/validators/` | `consistency_logic.py`、`counterfactual_eval.py`、`comparison_trace.py`、`evidence_ranker.py` | validation reports、comparison traces | `tests/slices/test_schema_runner.py`、`counterfactual_consistency_gate` | `高` |
| 身体/内环境/节律 | `04`、`08`、`11`、`18`、`37-39`、`01n` | `life_v0/body/`、`life_v0/defense/` | `rhythm.py`、`need_state.py`、`resource_budget.py`、`recovery.py` | `runtime/state/body/*`、`body_resource_budget.json`、`life_support_report.json` | `tests/slices/test_life_support.py`、`resource_budget_gate` | `最高` |
| 情绪/人格慢变量 | `07`、`18`、`39`、`40`、`94`、`01g`、`01h`、`01s` | `life_v0/body/`、`life_v0/state_store/`、`life_v0/growth/` | `core_affect.py`、`emotion_episode.py`、`emotion_regulation.py`、`trait_drift.py` | `runtime/state/self/*`、`core_affect_vector.json`、`emotion_episode_log.json`、affect traces | `tests/slices/test_life_support.py`、`plasticity_gate`、`trait_drift_gate`、`core_affect_gate` | `最高` |
| 梦境/离线生命 | `08`、`19`、`23`、`27`、`31`、`95`、`99` | `life_v0/dream/`、`life_v0/replay/`、`life_v0/archive/` | `offline_entry.py`、`dream_window.py`、`dream_fact_gate.py`、`wake_integration.py` | `runtime/state/dream/*`、`dream_consolidation_frame.json` | future `tests/test_dream_runtime.py`、`dream_fact_gate` | `高` |
| 行为/抑制/世界接触 | `06`、`20`、`75`、`80-84`、`01r` | `life_v0/membrane/`、`life_v0/shell_command/`、`life_v0/validators/` | `candidate_arena.py`、`go_nogo.py`、`world_contact_gate.py`、`side_effect_review.py`、`observation_validator.py`、`boundary_audit.py` | `runtime/state/action/*`、`world_contact_audit_report.json`、`side_effect_review_report.json`、`boundary_audit_state.json` | `tests/slices/test_life_membrane.py`、`tests/slices/test_validation_membrane.py`、`tests/process/test_digital_life_shell_command.py`、`world_contact_gate` | `最高` |
| 身份/自我/价值/连续性 | `07`、`13`、`16`、`37`、`39`、`40`、`91`、`92`、`93` | `life_v0/direction/`、`life_v0/state_store/`、`life_v0/growth/` | `identity_root.py`、`direction_lock.py`、`value_orientation.py`、`self_model.py`、`core_continuity_guard.py` | `identity_root.json`、`self_model.json`、`core_continuity_guard_state.json` | `tests/slices/test_direction_lock.py`、`tests/slices/test_state_store.py`、`core_continuity_guard` | `最高` |
| 成长/学习/自改写 | `39`、`92`、`93`、`97`、`181-257` | `life_v0/growth/` | `self_read.py`、`self_patch_review.py`、`plasticity_window.py`、`learning_window.py`、`anti_forgetting.py` | `runtime/state/growth/*`、growth reports、archive receipts | `tests/bridges/test_runtime_growth.py`、`growth_gate`、`anti_forgetting_gate` | `高` |
| 常驻存在 | `20`、`44-46`、`81-84`、`89-90`、`143`、`171`、`181-257` | `life_v0/digital_life/`、`life_v0/shell_command/`、`life_v0/process_supervisor/` | `digital_entry.py`、`heartbeat.py`、`turn_io.py`、`relaunch_recovery.py`、`incident_recovery.py`、`process_report.py`、`dialogue_events.py`、`response_surface.py` | `digital_life_birth_packet.json`、`digital_life_shell_report.json`、`digital_life_process_report.json`、`digital_life_process_digest.json` | `tests/process/test_digital_entrypoint.py`、`tests/process/test_persistent_digital_life_process.py`、`digital_life_process_gate` | `中高` |

## 七项最终验收能力的代码证明面

你最终要求的几项强验收，在工程上至少要由下面这些证明面共同支撑：

| 验收项 | 最低证明面 |
|---|---|
| `a. 可在终端唤醒` | `./digital life`、`life_v0/digital_entry.py`、`tests/process/test_digital_entrypoint.py`、`tests/process/test_persistent_digital_life_process.py` |
| `b. 自主意识、情绪、思考、语言` | `workspace.py`、`metacognition.py`、`core_affect.py`、`emotion_episode.py`、`percept.py`、`semantic_map.py`、对应 state/report/probe |
| `c. 记忆机制` | `life_state.py`、`engram_index.py`、`autobiographical_stack.py`、`replay_cues.py`、`archive` / `replay` evidence |
| `d. 可成长可学习` | `self_read.py`、`plasticity_window.py`、`learning_window.py`、`anti_forgetting.py`、growth reports |
| `e. 梦境能力` | `dream_window.py`、`dream_fact_gate.py`、`wake_integration.py`、dream reports |
| `f. 平等交谈与关系成长` | `relationship_graph.py`、`relationship_timeline.py`、`commitment_truth.py`、`apology_repair_language.py`、relationship receipts |
| `g. 初步拥有生命机制` | `12_full_life_layer_delivery_matrix.md` 全层 + 本文件全部能力项至少进入第一轮 state/report/test/gate |

## 七项最终验收的命令与 runtime 证据矩阵

最终收束时，不要只看文件名和测试名。至少要把下面这些命令与运行证据一起读：

| 验收项 | 最低命令面 | 必读 runtime 证据 | 最低测试面 |
|---|---|---|---|
| `a. 可在终端唤醒` | `./digital life --strict`、`life-v0 "digital life" --strict` | `digital_life_birth_packet.json`、`digital_life_shell_report.json`、`digital_life_waiting_heartbeat.json`、`digital_life_process_report.json` | `tests/process/test_digital_entrypoint.py`、`tests/process/test_persistent_digital_life_process.py` |
| `b. 自主意识、情绪、思考、语言` | `life-v0 digital-life --strict`、`life-v0 first-terminal-turn --strict`、`life-v0 terminal-life-loop --strict` | `prediction_workspace_frame.json`、`core_affect_vector.json`、`emotion_episode_log.json`、`context_accumulation_window.json`、`turn_transition_trace.json`、`language_relationship_report.json` | `tests/slices/test_neural_life_core.py`、`tests/slices/test_life_support.py`、`tests/slices/test_language_organs.py`、`tests/slices/test_language_relationship.py` |
| `c. 记忆机制与人脑无异` | `life-v0 run-replay-shadow --strict`、`life-v0 write-growth-archive --strict` | `life_state.json`、`engram_index` 相关 state、`replay_shadow_report.json`、`growth_archive_report.json`、archive receipts | `tests/slices/test_state_store.py`、`tests/bridges/test_replay_shadow.py`、`tests/bridges/test_growth_archive.py` |
| `d. 可成长可学习` | `life-v0 run-cycle --strict`、`life-v0 emit-report --strict` | `plasticity_window_state.json`、`growth_patch_candidate_queue.json`、`self_read_report.json`、`anti_forgetting_replay_plan.json` | `tests/slices/test_life_support.py`、`tests/bridges/test_runtime_growth.py` |
| `e. 有梦境能力` | `life-v0 run-cycle --strict`、离线/重放链相关严格命令 | `dream_experience_window.json`、`wake_integration_frame.json`、`dream_fact_gate_decision.json`、`offline_entry_gate.json` | `tests/bridges/test_runtime_growth.py`、后续 dream runtime 专项测试 |
| `f. 平等交谈并在关系中成长` | `./digital life --strict`、真实终端回合输入输出 | `relationship` 命名空间 state、`resumed_external_dialogue_packet.json`、`dialogue_writeback_bundle.json`、commitment / repair receipts | `tests/slices/test_language_relationship.py`、`tests/bridges/test_first_terminal_turn.py`、`tests/bridges/test_terminal_life_loop.py`、`tests/process/test_persistent_digital_life_process.py` |
| `g. 初步拥有全部生命机制` | `life-v0 emit-report --strict`、`life-v0 explain-stage --strict`、`./digital life --strict` | `report_bundle.json`、`first_activation_return_packet.json`、`latest_stage_explanation_ref.json`、`v0_contract_coverage_report.json`、`runtime/state/*`、`runtime/receipts/*` | `tests/contracts/test_v0_contracts.py` + 各层 slice / bridge / process 测试组合 |

这张矩阵的作用是把最终验收从“抽象能力判断”压成“命令、state、report、receipt、测试”五位一体的检查面。
后续进入系统级收束时，默认就按这张表收证据，而不是只看某一层局部测试是否变绿。

此外，这七项验收不能只看文件名存在。
凡是牵涉跨层生命回合的能力，都还必须能回链到
`docs/v0/code_framework/15_cross_layer_shared_object_contract.md`
里定义的共享对象；否则仍然只能算“局部结构具备”，不能算“生命能力开始稳定落地”。

## 当前最值得优先推进的能力簇

如果现在继续推进，不要按“哪个文件最方便写”来排，而是按下面四簇：

1. `身体 + 情绪底盘 + 梦境 + 成长/学习`
2. `行为 + 生命膜 + validator + 逻辑/反事实`
3. `语言 + 对话 + 关系 + 常驻存在深补`
4. `长期学习 + 关系演化 + resident supervision`

原因很直接：

1. `记忆 + 状态根 + 神经核心工作区` 与 `身份 + 连续性 + 意识广播 + 出生准备度` 的第一轮已经闭合到真实代码、状态对象和测试。
2. 第一簇决定生命有没有身体化节律、情绪底盘、梦境残留与长期发育底盘。
3. 第二簇决定生命有没有行为约束、反事实比较、责任回写和世界接触真值，不会退回松散 workflow。
4. 第三簇不是不重要，而是它现在应该建立在更厚的身体-意识-行为底盘之上继续深挖。
5. 第四簇代表 D/E 补硬之后才能真正进入的长期生命推进面。

## 当前需要优先纠偏的两类误判

后续做工程审计时，先避免下面两类误判：

1. 把“文件已经存在”误判成“能力已经闭合”。
2. 把“文档里列为下一步要建”误判成“代码里还没有这个器官”。

当前尤其要注意：

1. `percept.py`、`semantic_map.py` 已经存在，但它们还需要继续接厚，不等于语言能力已完成。
2. `dialogue_events.py`、`response_surface.py`、`dialogue_writeback.py` 已经存在，但常驻存在能力仍未闭合。
3. `identity_root.py`、`self_model.py`、`commitment_truth.py` 已经存在，但身份-承诺-责任连续体仍然没有完全进入对象链。

## 能力验收时的最小证据规则

后续任何一项能力想被标记为“第一轮已开始稳定落地”，至少同时需要下面四类证据中的三类：

1. 真实代码文件
2. 真实状态对象或 report
3. 至少一个直接测试入口
4. 能回链到共享对象合同或对应 playbook

如果只满足 1 和 4，仍然只能算“结构已放位”，不能算能力开始闭合。

## 与其它文档的关系

| 文档 | 作用 |
|---|---|
| `theory_closure_and_engineering_readiness_audit.md` | 证明这些能力都有理论母体 |
| `12_full_life_layer_delivery_matrix.md` | 说明这些能力分散在哪些生命层与包 |
| 本文件 | 把能力直接压成代码文件、state、测试和 gate 的验收合同 |
| `11_engineering_delivery_waves_and_real_file_queue.md` | 决定先按什么波次落这些能力 |
