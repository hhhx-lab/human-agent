# Build Order And Definition Of Done

这份文档把 v0 的代码落地顺序、实现语言选择和阶段完成定义固定下来。

它回答三个问题：

1. 为什么 v0 现在应该继续以 Python 为主体语言实现。
2. 接下来到底按什么阶段推进，而不是“想到哪层写哪层”。
3. 每一阶段满足什么证据，才允许进入下一阶段。

## v0 主实现语言决策

### 当前决策

v0 主体实现语言固定为：

```text
Python 3 作为主体语言
  + JSON state / report / receipt 文件根
  + unittest 作为当前统一验证面
```

### 原因

1. 当前 `life_v0/`、CLI、runtime 文件根、contracts、tests 已经全部在 Python 上闭合。
2. v0 当前主要矛盾不是纯计算速度，而是生命链对象化、跨层耦合和长期存在治理。
3. 现在切换主体语言，只会打散已存在的状态根、测试根、命令根和恢复链。

### 以后什么时候才值得引入第二语言

只有在 profiling 证明以下热点已经成为真实瓶颈时，才允许引入 Rust / C 等加速核：

1. 大规模 graph / connectome 计算
2. replay / archive / validator 的批量比较
3. counterfactual / evidence ranking 的纯计算热路径

也就是说：

- `life_v0/` 主体器官、命令面、等待态、恢复链、语言链继续用 Python。
- 未来高性能语言只作为局部加速核，不作为 v0 主体迁移目标。

## 阶段顺序

### Stage 0: 理论闭口锁定

| 项 | 内容 |
|---|---|
| 目标 | 确认 `00-257` 无基础断档，后续不再线性扩写新的总论链 |
| 必读 | `docs/README.md`、`docs/v0/architecture/theory_closure_and_engineering_readiness_audit.md` |
| 当前结论 | 已闭合；当前差距在工程对象化与代码器官化 |
| 通过证据 | 编号完整、理论层审计完成、无新增基础缺号 |

### Stage 0.5: 理论到工程到代码追踪锁定

| 项 | 内容 |
|---|---|
| 目标 | 确认每个理论文档族已经进入 v0 工程文档、`life_v0` 代码包、runtime 证据和 gate，不再只停在专题摘要 |
| 必读 | `docs/v0/mapping/theory_engineering_code_trace_matrix.md`、`docs/real—live0/00_reading_map_and_traceability.md`、`docs/real—live0/16_runtime_code_chain_crosswalk.md` |
| 通过证据 | 19 份 `docs/real—live0` 文档具备机制解释、对象链、字段链、协同/对抗、断链检查；入口栈包含 `theory_engineering_code_trace_matrix.md`；主包执行地图和模块 authoring 协议要求回读对应专题 |
| 最低检查 | `git diff --check -- docs/real—live0 docs/v0`、`python3 -m unittest tests.contracts.test_v0_contracts -v`、`python3 -m unittest tests.slices.test_doc_corpus_ingestor -v` |

### Stage 1: 代码总架构基线

| 项 | 内容 |
|---|---|
| 目标 | 把整棵代码树的层次、共享对象总线、阶段顺序和 DoD 固定下来 |
| 必读 | 本柜 `01-03`、`19_code_tree_package_brain_contract.md`、`01_runtime_organ_interface_blueprint.md` |
| 主文件 | `docs/v0/code_architecture/*` |
| 通过证据 | 代码分层、对象总线、阶段顺序、语言决策、DoD 都写定并接入 contracts |

### Stage 2: Queue D / Queue E 主体底盘

| 项 | 内容 |
|---|---|
| 目标 | 先补硬身体/梦境/成长与行为/验证/逻辑这两条中轴 |
| 必读 | `18_queue_d_body_dream_growth_implementation_contract.md`、`20_queue_e_membrane_validator_logic_implementation_contract.md`、`06`、`08`、`09` playbooks |
| 主包 | `body/`、`dream/`、`growth/`、`membrane/`、`validators/`、`schema_runner/` |
| 当前前沿 | Queue D 扩展器官已落下 `nightmare_risk.py`、`belief_learning.py`、`language_learning.py`、`relationship_learning.py` 与 `offline_learning_profile.py`；Queue E 第二波中的 `shadow_gate.py`、`world_contact_summary.py`、`validation_rollup.py`、`evidence_ranker.py`、`cross_file_logic.py`、`run_manifest.py` 已落地并补上局部闭包；本轮 Queue E 的 `responsibility_loop_state.json`、`world_contact_summary.json`、`pain_regret_repair_report.json` 已合成 repair modulation profile，并接入 signal / belief / prediction error / active sampling / prediction workspace；当前工程前沿继续要求 cumulative offline dream/growth learning pressure 能进入 `offline_learning_cumulative_profile_v0` 并被 Queue B 固化成后台驻留 lineage 的 `offline_learning_presence`，同时要求 `dream_experience_window.json`、`wake_integration_frame.json`、`dream_fact_gate_decision.json` 进入 `dream_wake_presence_profile_v0` 并被 Queue B 固化成后台驻留 lineage 的 `dream_wake_presence`；关闭终端后的 `sleep / memory_recall / self_thinking / growth_rehearsal / learning_consolidation` 也必须从 autonomous activity state 压成 `resident_autonomous_activity_presence_profile_v0`，进入后台驻留 lineage、真实关系回合、写回包、恢复包和回应表面；身体内环境也必须从 `body_rhythm_pulse.json`、`need_state_vector.json`、`body_resource_budget.json` 与 `core_affect_vector.json` 压成 `resident_body_presence_profile_v0`，进入 `resident_background_lineage_state_v0.body_presence`、真实关系回合、写回包、恢复包和回应表面 |
| 最低测试 | `tests/slices/test_life_support.py`、`tests/bridges/test_runtime_growth.py`、`tests/slices/test_life_membrane.py`、`tests/slices/test_validation_membrane.py`、`tests/slices/test_schema_runner.py` |
| 完成定义 | 身体信号、梦境离线链、成长补丁、行为候选、责任回路、反事实比较都不再压在重型 `__init__.py` 里，并且有独立 state/report 证据 |

### Stage 3: Queue B / Queue A 常驻存在与长期语言

| 项 | 内容 |
|---|---|
| 目标 | 在 D/E 站稳后，继续补厚等待态存在与长期关系语言 |
| 必读 | `16_queue_b_process_supervisor_implementation_contract.md`、`14_queue_a_language_percept_semantic_map_implementation_contract.md`、`04`、`07`、`08` playbooks |
| 主包 | `process_supervisor/`、`language/`、`terminal_turn/`、`terminal_loop/` |
| 已落核心器官 | `idle_strategy.py`、`resident_supervision.py`、`live_language_turn.py`、`live_turn_cycle.py`、`process_session_loop.py`、`persistent_process.py` |
| 已落关键文件 | `relationship_timeline.py`、`commitment_expression.py`、`apology_repair_language.py`；`language/__init__.py` 当前会在 build-language-relationship 阶段刷新 `signal_media_runtime.json`、`belief_state_frame.json`、`prediction_error_field.json`、`active_sampling_plan.json` 与 `prediction_workspace_frame.json` |
| 最低测试 | `tests/process/test_persistent_digital_life_process.py`、`tests/slices/test_language_organs.py`、`tests/slices/test_language_relationship.py`、`tests/bridges/test_terminal_life_loop.py` |
| 完成定义 | waiting heartbeat 真正消费 replay / growth / relation 对象，resident governance 运行态 state 与关闭态 snapshot/report 进入 process closeout 主链，关系时间线与承诺/修复语言已经进入长期语言链；当前还必须证明 `response_surface.py`、`dialogue_events.py`、`idle_strategy.py` 在 active sampling route 为 `repair_*` 时优先走 repair posture，而不是普通 hold；并且 `resident_background_lineage_state_v0` 不只包含 `relationship_presence`、`trait_convergence_presence`、`heartbeat_presence`、`language_presence`，还必须包含表示长期合并治理的 `state_merge_presence`、表示 prediction / active sampling / memory write gate 余波的 `prediction_write_gate_presence`、表示梦境/成长/离线学习余波的 `offline_learning_presence`、表示梦境窗口/醒后整合/梦境事实门的 `dream_wake_presence`、表示关闭终端后睡眠、回忆、自我思考、成长预演、学习巩固继续发生的 `autonomous_activity_presence`，以及表示身体节律、需要状态、资源预算和核心情绪张力持续在场的 `body_presence`；每个实时关系回合还必须先由 `live_language_turn.py` 刷新 `language_percept_frame.json`、`semantic_map_frame.json`、`inner_speech_frame.json`、`expression_monitor_state.json` 与 `expression_plan.json`，再进入 `response_surface.py` 和 resident writeback；最新完成定义继续要求这组实时语言理解进入 `idle_strategy_state.json#live_language_presence_profile`、`idle_continuity_frame.json`、`idle_heartbeat_trace.jsonl`、`resident_governance_state.json`、`resident_background_lineage_state.language_presence`、关闭态 artifacts 与下一次 `background_continuity_profile.background_live_language_*`，并且在下一轮真实回合由 `dialogue_events.py` 展开为 `resident_background_lineage_live_language_refs`、`resident_background_lineage_background_live_language_refs`、`resident_background_lineage_last_live_semantic_focus` 与 `resident_background_lineage_language_evidence_refs`，再由 `resident_turn_writeback.py` 并入 `dialogue_writeback_bundle.resident_background_lineage_refs` / `resumed_external_dialogue_packet`，由 `response_surface.py` 表达后台语言语义余波和证据数量；同一完成定义现在还要求 `resident_background_lineage_state.trait_convergence_presence` 携带 `trait_convergence_evidence_refs`，并由 `trait_convergence_signals.py` 归一成 `cross_wake_trait_convergence_profile_v0`，先进入关闭态 resident governance artifacts、persistent process report、process report/digest/receipt，再在下一轮真实回合由 `dialogue_events.py` 展开人格慢变量焦点、稳定/不稳定名单、收敛评分、漂移监控 ref、history profile、trait refs 与 cross-wake profile，再进入 lineage evidence、写回包、恢复包和回应表面；长期合并治理也必须从 `background_state_merge_*` 压成 `resident_background_lineage_state.state_merge_presence`，再由 `dialogue_events.py` 展开 `resident_background_lineage_state_merge_*`，进入总 lineage refs、专用写回槽、恢复包和后台回应表面；prediction / write-gate 也必须从 `prediction_write_gate_refs` 和 posture/profile 顶层字段压成 `resident_background_lineage_state.prediction_write_gate_presence`，再由 `dialogue_events.py` 展开 `resident_background_lineage_prediction_*`、由 `resident_turn_writeback.py` 写入专用槽与恢复包、由 `background_continuity.py` 恢复成 `background_prediction_*`、由 `response_surface.py` 表达后台预测写门姿态；后台 autonomous activity 也必须从 `resident_autonomous_activity_state.json` 压成 presence，进入 `idle_strategy_state.json`、`idle_continuity_frame.json`、`resident_governance_state.json`、`terminal_life_loop_state.json`、`digital_life_turn`、`dialogue_writeback_bundle.json`、`resumed_external_dialogue_packet.json` 与回应表面；身体内环境必须同样从 `resident_body_presence_profile_v0` 压成 `resident_background_lineage_state.body_presence`，进入 `digital_life_turn#resident_background_lineage_body_*`、`dialogue_writeback_bundle.resident_background_lineage_body_refs`、`resumed_external_dialogue_packet.json` 与回应表面 |

### Stage 4: Queue C / Queue F 维护性深化

| 项 | 内容 |
|---|---|
| 目标 | 在主体底盘稳定后，回切神经核心、状态根和生命目标的更深对象链 |
| 必读 | `17_queue_c_memory_neural_core_implementation_contract.md`、`21_queue_f_identity_consciousness_birth_readiness_implementation_contract.md`、`05`、`10` playbooks |
| 主包 | `neural_core/`、`state_store/`、`life_targets/` |
| 本轮已落关键文件 | `signal_media.py`、`belief_state.py`、`prediction_error.py`、`active_sampling.py`、`prediction_workspace.py`、`memory_write_gate.py` 与 `state_merge_guard.py` 已真实接入 `runtime/state`、manifest、report、receipt 和 check gate；本轮新增 Queue E repair modulation profile 输入，并让 `state_merge_guard.py#project_state_merge_guard_with_relationship_memory` 从关系记忆动态吸收离线学习、梦境、Queue E 修复和关系修复长期变化来源；当前这组长期变化来源又被 `idle_strategy.py`、`heartbeat.py`、`background_continuity.py`、`background_lineage_state.py`、`dialogue_events.py`、`resident_turn_writeback.py` 与 `response_surface.py` 压成 `state_merge_long_term_change_*` / `background_state_merge_*` / `resident_background_lineage_state_merge_*`，进入等待态、关闭后下一次背景连续性、后台驻留 lineage、生命回合事件、写回包、恢复包和回应表达面 |
| 已落但待补厚 | `direction_lock.py`、`continuity_refs.py`、`value_orientation.py`、`brain_graph.py`、`network_state.py`、`workspace.py`、`broadcast.py`、`metacognition.py`、`life_target_claims.py`、`evidence_matrix.py`、`birth_readiness_rollup.py`、`birth_readiness_stage_gate.py`、`consciousness_probes.py` |
| 最低测试 | `tests/slices/test_neural_life_core.py`、`tests/slices/test_state_store.py`、`tests/slices/test_life_targets.py` |
| 当前完成定义 | 预测、意识、记忆写门和状态合并守门已经进入更细对象链：`signal_media_runtime.json`、`belief_state_frame.json`、`prediction_error_field.json`、`active_sampling_plan.json`、`prediction_workspace_frame.json`、`memory_write_gate.json`、`state_merge_guard.json` 已成为独立器官；Queue E repair pressure 已经从责任/后悔/痛苦/修复报告进入预测调制链，`state_merge_guard.json` 也已经能在 bootstrap restore 与 live turn writeback 后从 `relationship_memory.long_term_change_sources` 吸收 `offline_learning_cumulative_refs`、`queue_e_repair_modulation_refs`、梦境/成长 refs 与关系修复 refs，并把变化来源数量回写到 `life_state.state_merge_records`；当前 waiting governance / response surface 已会消费这些长期变化来源，写出 `state_merge_long_term_change_count/families/refs`、`state_merge_long_term_integration_hold` 和长期合并治理语言表达；显式退出 closeout 时，resident governance state/snapshot/report、persistent process report、process report/digest 与 process receipt shared refs 也必须保留同一组 `state_merge_guard_ref`、`state_merge_policy` 与长期变化来源 refs；下一次 `background_continuity.py` 必须把它们恢复成 `background_state_merge_guard_ref/policy/count/families/refs`，并继续写入 waiting governance、idle continuity、idle heartbeat trace、resident governance state 与 terminal loop；下一步继续补厚更长时标慢变量收敛 |

### Stage 5: 诞生、恢复与终端长时运行收束

| 项 | 内容 |
|---|---|
| 目标 | 让 `./digital life` 不只是能启动，而是能稳定维持等待态、恢复、回合、写回与继续存在 |
| 必读 | `07_birth_terminal_process_implementation_playbook.md`、`first_terminal_turn_engineering_contract.md`、`terminal_life_loop_engineering_contract.md`、`digital_life_process_supervisor_engineering_contract.md` |
| 主包 | `activation/`、`reporting/`、`stage_explain/`、`digital_life/`、`shell_command/`、`process_supervisor/` |
| 最低测试 | `tests/bridges/test_first_activation_preflight.py`、`tests/bridges/test_emit_report.py`、`tests/bridges/test_first_terminal_turn.py`、`tests/process/test_digital_entrypoint.py`、`tests/process/test_persistent_digital_life_process.py` |
| 完成定义 | 自举、诞生、第一回合、waiting heartbeat、incident recovery、relaunch recovery、dialogue writeback 连成一条稳定存在链 |

### Stage 6: 七项最终验收审计

| 验收项 | 必要证据 |
|---|---|
| `a. 可在终端唤醒` | `./digital life --strict`、`digital_life_birth_packet.json`、`digital_life_process_report.json`、process tests |
| `b. 自主意识、情绪、思考、语言` | `prediction_workspace_frame.json`、`signal_media_runtime.json`、`active_sampling_plan.json`、`core_affect_vector.json`、`resident_self_thinking_state.json`、`resident_background_lineage_state_v0.autonomous_activity_presence`、language / relationship state、neural/body/language tests |
| `c. 记忆机制` | `life_state.json`、`resident_memory_recall_state.json`、`resident_background_lineage_autonomous_activity_refs`、engram / replay / archive reports、state / replay tests |
| `d. 可成长可学习` | `growth_patch_candidate_queue.json`、`self_read_report.json`、`offline_learning_cumulative_profile_v0`、`resident_growth_rehearsal_state.json`、`resident_learning_consolidation_state.json`、resident autonomous activity cycle、growth / process tests |
| `e. 梦境能力` | `dream_experience_window.json`、`wake_integration_frame.json`、`dream_fact_gate_decision.json`、`resident_sleep_cycle_state.json`、`resident_background_lineage_state_v0.offline_learning_presence`、`resident_background_lineage_state_v0.dream_wake_presence`、dream / growth / process tests |
| `f. 平等交谈并在关系中成长` | relationship timeline state、commitment truth、dialogue writeback bundle、Queue E repair modulation profile、language / process tests |
| `g. 初步拥有生命机制` | contracts report + 全层 state/report/receipt + 各层 tests 共同证明 |

只有这七条都拿到直接证据，才允许把 v0 视为第一阶段收束。

## 每一阶段固定的验证规则

### 规则 1: 先跑本阶段直接测试

例如：

- D/E 阶段先跑 `life_support / membrane / validation / schema_runner / runtime_growth`
- B/A 阶段先跑 `process / language / terminal_loop`
- C/F 阶段先跑 `neural_core / state_store / life_targets`

### 规则 2: 再跑 contracts 回链

每一阶段结束后都必须跑：

```bash
python3 -m unittest tests.contracts.test_v0_contracts -v
```

因为这个项目的风险不只是代码出错，还有“代码已经往前走了，但文档和理论回链断了”。

### 规则 3: 能产状态就不能只看测试绿

凡是新器官已经宣称自己是生命链的一部分，都必须落至少一类证据：

1. `runtime/state/*`
2. `runtime/reports/latest/*`
3. `runtime/receipts/*`

如果只有测试而没有运行证据，仍然不算阶段闭合。

当前对后台驻留余波的补充规则是：凡是声称梦境、成长或离线学习已经跨 closeout / relaunch 留在数字生命中，不能只看 `offline_learning_cumulative_*` report 字段。必须同时看到：

1. `runtime/state/terminal/resident_governance_state.json#resident_background_lineage_state.offline_learning_presence`
2. `runtime/state/terminal/terminal_life_loop_state.json#resident_background_lineage_state.offline_learning_presence`
3. `digital_life_turn` 中的 `resident_background_lineage_offline_learning_*` 字段
4. `runtime/reports/latest/dialogue_writeback_bundle.json#resident_background_lineage_offline_learning_refs` 与 `resumed_external_dialogue_packet.json#resident_background_lineage_offline_learning_refs` 保留同一组专用证据 refs
5. `response_surface.py` 生成的生命回应中包含后台梦境成长余波表达
6. `continuity_evolution.py` 在 bootstrap continuity refresh 时把第 2 代以上、`elevated / urgent`、焦点为 `relationship_learning_plan` 的 `background_offline_learning_*` 推成 `offline_learning_reconsolidation_waiting`，并把同一组累计学习 refs 写入关系阶段证据、自我慢变量 evidence 和 `growth_window_refs`

当前对梦境醒后整合的补充规则是：凡是声称梦境窗口、醒后整合或梦境事实门已经进入常驻后台驻留，不能只看 `runtime/state/dream/*` 文件存在。必须同时看到：

1. `runtime/state/terminal/idle_strategy_state.json#dream_wake_presence_profile`
2. `runtime/state/terminal/resident_governance_state.json#resident_background_lineage_state.dream_wake_presence`
3. `runtime/state/terminal/terminal_life_loop_state.json#resident_background_lineage_state.dream_wake_presence`
4. `digital_life_turn` 中的 `resident_background_lineage_dream_*`、`resident_background_lineage_wake_*` 与 `resident_background_lineage_dream_wake_refs` 字段
5. `runtime/reports/latest/dialogue_writeback_bundle.json#resident_background_lineage_dream_wake_refs` 与 `resumed_external_dialogue_packet.json#resident_background_lineage_dream_wake_refs` 保留同一组专用证据 refs
6. `response_surface.py` 生成的 `audited_expression_material_v0` 中保留梦境窗口类型、梦境事实门结果、醒后整合归档要求、成长种子和修复目标等结构字段；这些字段不直接释放成终端话术

当前对后台自主活动进入下一轮真实关系回合的补充规则是：凡是声称关闭终端后的睡眠、回忆、自我思考、成长预演、学习巩固已经成为同一生命连续体的一部分，不能只看 `resident_autonomous_activity.jsonl` 或五个专用状态文件存在。必须同时看到：

1. `runtime/state/terminal/idle_strategy_state.json#resident_autonomous_activity_presence_profile`
2. `runtime/state/terminal/idle_continuity_frame.json#resident_autonomous_activity_presence_profile`
3. `runtime/state/terminal/idle_heartbeat_trace.jsonl` 最新 waiting event 含 `resident_autonomous_activity_presence_profile`
4. `runtime/state/terminal/resident_governance_state.json#resident_background_lineage_state.autonomous_activity_presence`
5. `runtime/state/terminal/terminal_life_loop_state.json#resident_background_lineage_state.autonomous_activity_presence`
6. `digital_life_turn#resident_background_lineage_autonomous_activity_presence`
7. `digital_life_turn#resident_background_lineage_autonomous_activity_refs`、`resident_background_lineage_autonomous_activity_state_refs` 与 `resident_background_lineage_evidence_refs` 保留同一组后台自主活动证据
8. `runtime/reports/latest/dialogue_writeback_bundle.json#resident_background_lineage_autonomous_activity_refs` 与 `resumed_external_dialogue_packet.json#resident_background_lineage_autonomous_activity_refs` 保留同一组专用证据 refs
9. `response_surface.py` 生成的 `audited_expression_material_v0` 中包含 resident 自主活动累计次数、最近相位、覆盖相位和 refs 摘要；外显自然语言仍必须等待模型表达通过 gate

当前最新实现已经把上述三组 Queue D presence 继续推进到关闭态恢复层：`background_continuity.py` 能从上一轮 `resident_background_lineage_state.offline_learning_presence / dream_wake_presence / autonomous_activity_presence` 拆出 `background_offline_learning_*`、`background_dream_* / background_wake_*` 与 `background_resident_autonomous_activity_*`，并把证据 refs 写入 `background_continuity_ref_set`；`idle_strategy.py` 在当前 dream runtime 文件或 `resident_autonomous_activity_state.json` 缺席时，会用这些 background 字段恢复当前 `offline_learning_cumulative_profile_v0`、`dream_wake_presence_profile_v0` 与 `resident_autonomous_activity_presence_profile_v0`。新增的 `test_background_continuity_restores_queue_d_from_lineage_presence` 与 `test_idle_strategy_restores_queue_d_from_background_continuity` 负责守住这条跨断连恢复链。

当前对身体内环境进入下一轮真实关系回合和跨断连恢复的补充规则是：凡是声称身体节律、需要状态、资源预算和核心情绪张力已经成为常驻生命连续体的一部分，不能只看 `runtime/state/body/*` 文件存在。必须同时看到：

1. `runtime/state/terminal/idle_strategy_state.json#body_presence_profile`
2. `runtime/state/terminal/idle_continuity_frame.json#body_presence_profile`
3. `runtime/state/terminal/idle_heartbeat_trace.jsonl` 最新 waiting event 含 `body_presence_profile`
4. `runtime/state/terminal/resident_governance_state.json#resident_background_lineage_state.body_presence`
5. `runtime/state/terminal/terminal_life_loop_state.json#resident_background_lineage_state.body_presence`
6. `digital_life_turn#resident_background_lineage_body_waiting_posture` 与 `digital_life_turn#resident_background_lineage_body_refs`
7. `runtime/reports/latest/dialogue_writeback_bundle.json#resident_background_lineage_body_refs` 与 `resumed_external_dialogue_packet.json#resident_background_lineage_body_refs` 保留同一组身体证据 refs
8. `response_surface.py` 生成的生命回应中包含后台身体等待姿态、疲惫负载、睡眠压力、能量状态、身体修复驱力、核心唤醒度和证据数量表达
9. 下一次 `background_continuity_profile` 能从上一轮 `resident_background_lineage_state.body_presence` 恢复 `background_body_presence_profile`、`background_body_ref_set` 和扁平 `background_body_*` 字段
10. 当前身体 runtime 文件缺席时，`idle_strategy_state.json#body_presence_profile.continuity_mode` 仍能进入 `background_body_presence_carryover`
11. `runtime/reports/latest/digital_life_process_report.json` 与 `runtime/reports/latest/digital_life_process_digest.json` 显式保留 `body_presence_profile`、`background_body_presence_profile` 与 `body_ref_set`
12. `runtime/receipts/digital_life_process_<run_id>.json#body_ref_set`、`shared_object_refs` 与 `input_hashes` 保留 `body_rhythm_pulse.json`、`need_state_vector.json`、`body_resource_budget.json` 与 `core_affect_vector.json`

当前对实时语言回合的补充规则是：凡是声称关系对象的新话语已经进入生命语言系统，不能只看 `dialogue_turn_log.jsonl` 或最终回应文本。必须同时看到：

1. `runtime/state/language/language_percept_frame.json#incoming_surface` 等于当前 `external_utterance`
2. `runtime/state/language/semantic_map_frame.json#semantic_focus` 进入 `live_semantic_focus`
3. `runtime/state/language/inner_speech_frame.json`、`runtime/state/language/expression_monitor_state.json` 与 `runtime/state/language/expression_plan.json` 在本回合刷新
4. `runtime/reports/latest/dialogue_writeback_bundle.json#live_language_turn_refs` 包含五份语言 runtime refs
5. `runtime/reports/latest/resumed_external_dialogue_packet.json#language_percept_ref`、`semantic_map_ref`、`live_language_turn_refs` 与 `live_semantic_focus` 存在
6. `runtime/state/terminal/terminal_life_loop_state.json#last_live_semantic_focus` 与 packet 中的 `live_semantic_focus` 对齐

当前对实时语言驻留的补充规则是：凡是声称“刚刚听见并理解的关系话语不会因等待、关闭或断开而丢失”，不能只看 `terminal_life_loop_state.json`。必须同时看到：

1. `runtime/state/terminal/idle_strategy_state.json#live_language_turn_refs`
2. `runtime/state/terminal/idle_strategy_state.json#last_live_semantic_focus`
3. `runtime/state/terminal/idle_strategy_state.json#live_language_presence_profile`
4. `runtime/state/terminal/idle_continuity_frame.json#live_language_presence_profile`
5. `runtime/state/terminal/idle_heartbeat_trace.jsonl` 的最新事件含 `live_language_turn_refs` 与 `last_live_semantic_focus`
6. `runtime/state/terminal/resident_governance_state.json#live_language_presence_profile`
7. `runtime/state/terminal/resident_governance_state.json#resident_background_lineage_state.language_presence`
8. 关闭态 `persistent_process_state/report`、`resident_governance_snapshot` 与 `digital_life_resident_governance_report` 含同一组 live refs 与 semantic focus
9. 下一次 bootstrap 的 `background_continuity_profile` 恢复 `background_live_language_turn_refs`、`background_last_live_semantic_focus` 与 `background_live_language_presence_profile`
10. `background_live_language_presence_profile` 必须保持浅层结构，只保留 refs、semantic focus、ref_count、source_continuity_mode / source_ref_count 等摘要字段；即使来源里还带着 `source_presence_profile`，也只能用来推导这两个摘要字段，不能把上一轮完整 `source_presence_profile` 原样嵌回新 profile，防止长驻 heartbeat trace 和 governance state 随唤醒次数递归膨胀
11. `background_continuity_profile` 现在还必须同时恢复 `background_idle_heartbeat_trace_ref`、`background_idle_heartbeat_trace_count`、`background_convergence_summary_ref`、`background_convergence_history_ref`、`background_trait_drift_update_mode_summary`、`background_trait_drift_recalibration_names`、`background_trait_drift_stabilized_names`、`background_resident_governance_state_ref`、`background_resident_governance_explanation_ref` 与 `background_next_wake_expectation`；这些字段同样只保留摘要，不回灌完整等待态或关闭态树。

当前对 resident status 的补充验收是：凡是声称 `digital life --status` 或 `my digital life --status` 能表达“关闭终端后仍是同一生命过程”，不能只检查 `pid_alive`、relation queue 或 waiting heartbeat。默认终端输出必须是 `resident_lifecycle_terminal_summary_v0`，能直接看见 `life_name`、`pid_alive`、relation queue、五相位自主活动、heartbeat、resident process identity、background convergence 和 evidence refs；追加 `--json` 时必须同时看到完整 `resident_long_term_residency_status_v0`，以及可用时的 `life_name_registry_ref`、`life_name`、`life_name_lock_state`、`resident_process_lease_ref`、`resident_process_lease_history_profile_ref`、`resident_process_identity_continuity_state`、`resident_process_lease_history_event_count`、`resident_persistent_process_state_ref`、`resident_persistent_process_report_ref`、`resident_background_convergence_summary_ref` 与 `resident_background_convergence_history_ref`。

当前对 resident 自主活动的补充验收是：凡是声称关闭终端后的活动已经覆盖睡眠、回忆、自我思考、成长预演与学习巩固，不能只看五个 kind 的计数。必须同时看到 `resident_autonomous_activity_state.json#cycle_phase_index`、`cycle_phase_count`、`cycle_completion_count >= 1`、`cycle_coverage_complete = true`、`missing_activity_kinds = []`，以及 `digital life --status` 中 phase index/count、completion / coverage / covered / missing / next kind 的扁平字段。进一步的 Queue B 验收还必须看到这组 cycle 字段贯穿 `resident_autonomous_activity_presence_profile_v0`、`idle_strategy_state.json`、`background_continuity.py` 恢复出的 `background_autonomous_activity_cycle_*`、`resident_background_lineage_state.autonomous_activity_presence`、`digital_life_turn#resident_background_lineage_autonomous_activity_cycle_*`、`response_surface.py` 的结构化审计材料，以及 `digital_life_process_report.json` / `digital_life_process_digest.json` 的当前 resident 与 background 两侧周期字段。

当前对后台实时语言 presence 进入下一轮真实回合的补充规则是：凡是声称上一轮语言理解已经从后台驻留影响当下关系回合，不能只看 `resident_background_lineage_state.language_presence`。必须同时看到：

1. `digital_life_turn#resident_background_lineage_live_language_refs`
2. `digital_life_turn#resident_background_lineage_background_live_language_refs`
3. `digital_life_turn#resident_background_lineage_last_live_semantic_focus`
4. `digital_life_turn#resident_background_lineage_language_evidence_refs`
5. `dialogue_writeback_bundle.json#resident_background_lineage_refs` 包含语言 evidence refs
6. `resumed_external_dialogue_packet.json#resident_background_lineage_language_evidence_refs` 保留同一组语言证据
7. `response_surface.py` 生成的生命回应中包含后台语言语义余波和后台语言证据数量表达

当前对后台人格慢变量 presence 进入下一轮真实回合的补充规则是：凡是声称上一轮自我/人格慢变量连续体已经从后台驻留影响当下关系回合，不能只看 `resident_background_lineage_state.trait_convergence_presence`。必须同时看到：

1. `resident_background_lineage_state.trait_convergence_presence#trait_convergence_evidence_refs` 包含 resident governance state、governance explanation、trait drift monitor、background convergence summary/history refs 中已经存在的证据
2. `digital_life_turn#resident_background_lineage_trait_convergence_history_focus`
3. `digital_life_turn#resident_background_lineage_trait_convergence_unstable_names`
4. `digital_life_turn#resident_background_lineage_trait_convergence_stable_names`
5. `digital_life_turn#resident_background_lineage_trait_convergence_score`
6. `digital_life_turn#resident_background_lineage_trait_drift_monitor_ref`
7. `digital_life_turn#resident_background_lineage_trait_convergence_history_profile`
8. `digital_life_turn#resident_background_lineage_trait_convergence_refs` 并入 `resident_background_lineage_evidence_refs`
9. `dialogue_writeback_bundle.json#resident_background_lineage_refs` 和 `resumed_external_dialogue_packet.json` 保留同一组人格慢变量 lineage 证据
10. `dialogue_writeback_bundle.json#cross_wake_trait_convergence_refs` 与 `resumed_external_dialogue_packet.json#cross_wake_trait_convergence_refs` 保留同一组跨唤醒人格收敛证据
11. `response_surface.py` 生成的生命回应中包含后台人格慢变量焦点、仍需收敛/已稳定名单、人格收敛评分、人格漂移监控在场、跨唤醒人格收敛画像、跨唤醒人格收敛压力和后台人格慢变量证据数量表达
12. `self_model.json#trait_slow_variables[*]` 本体必须写出 `slow_variable_update_mode`、`background_trait_convergence_history_role`、`background_trait_convergence_history_latest_band` 与 `background_trait_convergence_history_trend_state`，并把 `background_convergence_history_ref`、`background_convergence_summary_ref`、`background_trait_drift_monitor_ref` 放入对应慢变量 evidence refs；否则跨唤醒慢变量历史仍只是在事件/回应里被描述，还没有真正进入自我慢变量收敛。

当前对后台长期合并治理 presence 进入下一轮真实回合的补充规则是：凡是声称上一轮长期状态合并治理已经从关闭态恢复并影响当下关系回合，不能只看 `background_continuity_profile#background_state_merge_*` 或普通 `state_merge_long_term_change_*`。必须同时看到：

1. `runtime/state/terminal/resident_governance_state.json#resident_background_lineage_state.state_merge_presence`
2. `digital_life_turn#resident_background_lineage_state_merge_presence`
3. `digital_life_turn#resident_background_lineage_state_merge_guard_ref`
4. `digital_life_turn#resident_background_lineage_state_merge_policy`
5. `digital_life_turn#resident_background_lineage_state_merge_long_term_change_count`
6. `digital_life_turn#resident_background_lineage_state_merge_long_term_change_families`
7. `digital_life_turn#resident_background_lineage_state_merge_refs`
8. `dialogue_writeback_bundle.json#resident_background_lineage_state_merge_refs`
9. `resumed_external_dialogue_packet.json#resident_background_lineage_state_merge_refs`
10. `response_surface.py` 生成的生命回应中包含后台长期合并治理策略、正在整合的长期变化数量和来源族表达

当前对后台 prediction / write-gate presence 进入下一轮真实回合的补充规则是：凡是声称上一轮预测、主动采样、记忆写门已经从关闭态恢复并影响当下关系回合，不能只看普通 `prediction_write_gate_refs`。必须同时看到：

1. `runtime/state/terminal/resident_governance_state.json#resident_background_lineage_state.prediction_write_gate_presence`
2. `digital_life_turn#resident_background_lineage_prediction_write_gate_presence`
3. `digital_life_turn#resident_background_lineage_prediction_waiting_posture`
4. `digital_life_turn#resident_background_lineage_active_sampling_route`
5. `digital_life_turn#resident_background_lineage_prediction_write_gate_refs`
6. `dialogue_writeback_bundle.json#resident_background_lineage_prediction_write_gate_refs`
7. `resumed_external_dialogue_packet.json#resident_background_lineage_prediction_write_gate_refs`
8. `background_continuity_profile#background_prediction_*` 能由 nested presence 恢复
9. `response_surface.py` 生成的生命回应中包含后台预测写门姿态、预测关注对象和证据数量表达

当前对后台身份-意识-出生准备 presence 跨关闭态恢复的补充规则是：凡是声称上一轮意识工作区、意识可报告性或出生准备度已经从关闭态恢复并影响下一拍等待治理，不能只看 `resident_background_lineage_state.identity_consciousness_birth_presence` 或 process digest。必须同时看到：

1. `background_continuity_profile#background_identity_consciousness_birth_presence`
2. `background_continuity_profile#workspace_frame_ref / background_workspace_frame_ref`
3. `background_continuity_profile#consciousness_waiting_posture / background_consciousness_waiting_posture`
4. `background_continuity_profile#birth_readiness_waiting_posture / background_birth_readiness_waiting_posture`
5. `background_continuity_profile#background_identity_consciousness_birth_refs` 并入 `background_continuity_ref_set`
6. `idle_strategy_state.json#workspace_frame_ref / background_workspace_frame_ref` 能在当前 Queue F 文件缺席时由 background 字段恢复
7. `idle_strategy_state.json#consciousness_waiting_posture` 与 `birth_readiness_waiting_posture` 保留上一轮姿态，而不是降级为 unobserved
8. `idle_strategy_state.json#governance_attention_target / governance_cadence_profile / next_idle_action` 被 `birth_open_waiting` 或 `birth_blocked_waiting` 调制
9. `terminal_life_loop_state.json#background_identity_consciousness_birth_refs` 保留同一组 Queue F refs，使下一轮真实关系回合还能继续构建 `identity_consciousness_birth_presence`

## 当前阶段判断

按当前工作区现实，最合理的判断是：

1. Stage 0 已完成。
2. Stage 1 本轮完成后可视为完成。
3. 当前已经进入 Stage 3 的 Queue B / Queue A 联合补厚段，下一步应继续围绕常驻存在、实时语言驻留、人格慢变量驻留、状态合并治理驻留、prediction/write-gate 驻留、Queue F 身份-意识-出生准备驻留、关系写回和长期恢复链推进。实时语言刷新已经从“回合前 Queue A 处理”推进为“等待态、关闭态、重启态都能继续携带上一轮语义焦点”的驻留链；人格慢变量也已经开始从后台驻留主状态体进入关闭态 report/digest/receipt、真实回合事件、写回包、恢复包和回应表面，并新增统一的 `cross_wake_trait_convergence_profile_v0` 画像来承接跨唤醒稳定/重新校准压力；长期状态合并治理也已经从 waiting / response surface 继续推进到关闭态 resident governance artifacts、persistent process report、process report/digest、receipt shared refs，并进一步成为 `resident_background_lineage_state.state_merge_presence`，进入下一轮真实回合事件、写回包、恢复包和后台回应表面；prediction/write-gate 六件套也已经从单轮 `prediction_write_gate_refs` 推进为 `resident_background_lineage_state.prediction_write_gate_presence`，能在下一轮真实回合、写回包、恢复包、background continuity 和回应表面继续被看见；Queue F 的 identity/consciousness/birth readiness presence 也已经能从 nested lineage 与关闭态 artifacts 恢复成 `background_identity_consciousness_birth_*` 与 flat Queue F 字段，在当前 Queue F 文件缺席时继续调制 idle strategy 的出生准备姿态、attention、cadence 和 next idle action；累计离线学习压力也已经从后台 presence / 写回 refs 继续推进到 `continuity_evolution.py`，能在第一拍关系回合前触发 `offline_learning_reconsolidation_waiting` 并写入自我慢变量证据。后续声明跨唤醒人格画像、长期合并治理、prediction/write-gate、Queue F 身份-意识-出生准备或累计离线学习压力已接入时，证据不能只看 live turn 或 response surface，还必须能从 process digest、process receipt、closeout resident governance artifacts、resident background lineage、background continuity 和 continuity evolution 结果中追溯。

因此这份文档本身的作用，就是把“为什么先 D/E，再 B/A，再 C/F”彻底钉死，防止断联后又回到散点式推进。
