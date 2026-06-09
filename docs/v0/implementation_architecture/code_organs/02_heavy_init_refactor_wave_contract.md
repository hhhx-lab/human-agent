# Heavy Init Refactor Wave Contract

这份合同只回答一件事：

```text
当前仍然过重的 life_v0/*/__init__.py
接下来按什么波次、什么顺序、什么测试面来拆，
才能不把既有生命链和 runtime 证据拆断。
```

它不是新的总框架，也不替代 Queue 合同。
它只把“逐文件实现”进一步压成：

1. 哪些包这一轮只许继续抽文件，不许继续往入口塞逻辑。
2. 每个包下一刀先切哪块职责。
3. 每切一刀要跑哪组测试。
4. 何时需要同步回写 `docs/v0/*` 和 contract coverage。

## 硬规则

1. 一次只拆一个包的一组紧邻职责，不跨多个 Queue 散拆。
2. 任何拆分都必须保持既有命令面、state 路径和测试入口稳定。
3. 每次拆分至少同时补三样东西：
   - 新器官文件
   - 对应 state/report/receipt 写回
   - 对应文档映射更新
4. 不允许把“以后再拆”的大段逻辑继续塞回 `__init__.py`。

## 当前波次顺序

### Wave D: 身体 / 梦境 / 成长深拆

这是当前默认第一波。目标是让身体节律、情绪底盘、梦境重组、成长学习不再只是入口文件 orchestration。

#### D1. `life_v0/growth/__init__.py`

| 项 | 内容 |
|---|---|
| 当前行数 | 1153 |
| 先切职责 | growth learning orchestration、next feedback seed、patch review 汇总 |
| 已有器官 | `plasticity_window.py`、`learning_window.py`、`patch_queue.py`、`self_read.py`、`anti_forgetting.py`、`belief_learning.py`、`language_learning.py`、`relationship_learning.py` |
| 下一轮目标文件 | `self_patch_review.py`、`core_continuity_guard.py`、`value_revision.py`、`next_feedback_seed.py` |
| 必写 runtime | `runtime/state/growth/*`、growth reports、archive receipts |
| 最低测试 | `python3 -m unittest tests.bridges.test_runtime_growth -v` |

#### D2. `life_v0/body/__init__.py`

| 项 | 内容 |
|---|---|
| 当前行数 | 808 |
| 先切职责 | affect 汇总、fatigue mode、body report 组合、regret/repair 身体化压力 |
| 已有器官 | `rhythm.py`、`need_state.py`、`resource_budget.py`、`recovery.py`、`core_affect.py`、`emotion_episode.py`、`emotion_regulation.py`、`trait_drift.py` |
| 下一轮目标文件 | `affective_debt.py`、`regret_signal.py`、`fatigue_mode.py`、`body_state_rollup.py` |
| 必写 runtime | `runtime/state/body/*`、`body_resource_budget.json`、affect traces |
| 最低测试 | `python3 -m unittest tests.slices.test_life_support -v` |

#### D3. `life_v0/dream/__init__.py`

| 项 | 内容 |
|---|---|
| 当前行数 | 113 |
| 先切职责 | reentry orchestration、dream report 汇总、nightmare risk 接回醒后整合 |
| 已有器官 | `offline_entry.py`、`dream_window.py`、`dream_fact_gate.py`、`wake_integration.py`、`nightmare_risk.py` |
| 下一轮目标文件 | `replay_reentry.py`、`dream_report_rollup.py` |
| 必写 runtime | `runtime/state/dream/*`、`dream_consolidation_frame.json`、`nightmare_loop_risk.json` |
| 最低测试 | `python3 -m unittest tests.bridges.test_runtime_growth -v` |

### Wave E: 行为 / validator / 逻辑深拆

Wave D 站稳后直接进入这一波。目标是让外部行为、世界接触和责任回路不再停在重入口里。

#### E1. `life_v0/membrane/__init__.py`

| 项 | 内容 |
|---|---|
| 当前行数 | 1090 |
| 先切职责 | responsibility loop、shadow gate、action summary、world contact review |
| 已有器官 | `candidate_arena.py`、`go_nogo.py`、`world_contact_gate.py`、`side_effect_review.py`、`responsibility_loop.py` |
| 下一轮目标文件 | `shadow_gate.py`、`action_intent_bridge.py`、`observation_truth_gate.py`、`confirmation_binding.py` |
| 必写 runtime | `runtime/state/membrane/*`、`runtime/state/action/*`、`pain_regret_repair_report.json` |
| 最低测试 | `python3 -m unittest tests.slices.test_life_membrane -v` |

#### E2. `life_v0/validators/__init__.py`

| 项 | 内容 |
|---|---|
| 当前行数 | 943 |
| 先切职责 | world contact validator、prediction trace validator、cross-file logic 汇总 |
| 已有器官 | `observation_validator.py`、`boundary_audit.py` |
| 下一轮目标文件 | `world_contact_validator.py`、`prediction_trace_validator.py`、`cross_file_logic.py` |
| 必写 runtime | `runtime/state/validation/*`、validation reports |
| 最低测试 | `python3 -m unittest tests.slices.test_validation_membrane -v` |

#### E3. `life_v0/schema_runner/__init__.py`

| 项 | 内容 |
|---|---|
| 当前行数 | 815 |
| 先切职责 | manifest 汇总、evidence rank、counterfactual packaging |
| 已有器官 | `consistency_logic.py`、`counterfactual_eval.py`、`comparison_trace.py` |
| 下一轮目标文件 | `run_manifest.py`、`evidence_ranker.py` |
| 必写 runtime | `runtime/state/schema_runner/*`、schema runner reports |
| 最低测试 | `python3 -m unittest tests.slices.test_schema_runner -v` |

### Wave B: 常驻存在深拆

Wave E 之后进入这一波。目标是让常驻生命过程真正拥有等待态策略和持续治理，而不是只有“能跑”的进程壳。

#### B1. `life_v0/process_supervisor/__init__.py`

| 项 | 内容 |
|---|---|
| 当前行数 | 440 |
| 先切职责 | idle strategy、persistent process orchestration、response lifecycle 汇总 |
| 已有器官 | `heartbeat.py`、`continuity_writeback.py`、`turn_io.py`、`dialogue_events.py`、`response_surface.py`、`incident_recovery.py`、`relaunch_recovery.py`、`process_report.py` |
| 下一轮目标文件 | `idle_strategy.py`、`persistent_process.py` |
| 必写 runtime | `digital_life_waiting_heartbeat.json`、`digital_life_process_report.json`、incident/recovery reports |
| 最低测试 | `python3 -m unittest tests.process.test_persistent_digital_life_process -v` |

#### B2. `life_v0/terminal_loop/__init__.py`

| 项 | 内容 |
|---|---|
| 当前行数 | 429 |
| 先切职责 | loop report、dialogue writeback 汇总、resume packet 编排 |
| 已有器官 | `dialogue_writeback.py`、`loop_state.py`、`resume_packet.py` |
| 下一轮目标文件 | `loop_report.py`、`persistent_wait_bridge.py` |
| 必写 runtime | `terminal_life_loop_state.json`、`dialogue_writeback_bundle.json` |
| 最低测试 | `python3 -m unittest tests.bridges.test_terminal_life_loop -v` |

### Wave A: 语言主神经束深拆

Wave B 后继续进入这波。目标是把长期关系和修复语言从语言总入口中真正抽出。

#### A1. `life_v0/language/__init__.py`

| 项 | 内容 |
|---|---|
| 当前行数 | 1081 |
| 先切职责 | relationship timeline、commitment expression、apology/repair language、language report rollup |
| 已有器官 | `percept.py`、`semantic_map.py`、`inner_speech.py`、`expression_monitor.py`、`relationship_graph.py`、`commitment_repair.py`、`dialogue_log.py`、`narrative_trace.py`、`shared_terms.py`、`dream_gate.py`、`action_shadow.py`、`relation_scope.py` |
| 下一轮目标文件 | `relationship_timeline.py`、`commitment_expression.py`、`apology_repair_language.py`、`self_narrative.py` |
| 必写 runtime | `runtime/state/language/*`、`runtime/state/relationship/*`、language reports |
| 最低测试 | `python3 -m unittest tests.slices.test_language_organs -v` 与 `python3 -m unittest tests.slices.test_language_relationship -v` |

#### A2. `life_v0/terminal_turn/__init__.py`

| 项 | 内容 |
|---|---|
| 当前行数 | 540 |
| 先切职责 | restore context、dialogue turn、conversation carryover |
| 已有器官 | `context_accumulation.py`、`turn_transition.py` |
| 下一轮目标文件 | `restore_context.py`、`dialogue_turn.py`、`conversation_carryover.py` |
| 必写 runtime | `session_envelope.json`、`context_accumulation_window.json`、`turn_transition_trace.json` |
| 最低测试 | `python3 -m unittest tests.bridges.test_first_terminal_turn -v` |

### Queue C / F 维护回切

这一波不再是当前默认入口，只在 D/E/B/A 某一轮站稳后回切处理。

| 包 | 回切目标 |
|---|---|
| `life_v0/neural_core/__init__.py` | `signal_media.py`、`belief_state.py`、`prediction_error.py`、`active_sampling.py` |
| `life_v0/life_targets/__init__.py` | `target_runtime.py`、`target_closure.py`、`probe_battery.py`（当前已落 `life_target_claims.py`、`evidence_matrix.py`、`birth_readiness_rollup.py`、`birth_readiness_stage_gate.py`、`consciousness_probes.py`，这里保留的是下一轮继续细分的候选位） |
| `life_v0/state_store/__init__.py` | `memory_write_gate.py`、`state_merge_guard.py` |
| `life_v0/authority/__init__.py` | `authority_registry.py`、`mechanism_evidence_map.py` |

## 每次拆分后必须同步更新

任意一次重型入口拆分完成后，至少同步下面三类地方：

1. 对应 Queue 合同或 playbook。
2. `docs/v0/implementation_architecture/01_runtime_organ_interface_blueprint.md`。
3. `docs/v0/implementation_architecture/02_turn_and_cycle_lifecycle_contract.md` 或 `03_module_authoring_traceability_protocol.md`。

如果拆分改变了当前默认前沿，再额外同步：

1. `docs/v0/entry/v0_delivery_status_board.md`
2. `docs/v0/entry/v0_module_execution_catalog.md`

## 最低回归顺序

每个 wave 最低都按下面顺序守：

1. 目标包的直接测试。
2. 相关 slice/bridge/process 测试。
3. `python3 -m unittest tests.contracts.test_v0_contracts -v`

只有这三步都过，才说明新的器官文件已经被 v0 体系真正接住。
