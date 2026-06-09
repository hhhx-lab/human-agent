# State Object Runtime Evidence Map

本文档把数字生命当前最关键的状态对象，固定成一张工程地图。

它回答的是：

```text
这个对象由谁生产、
被谁消费、
落在哪个 runtime 文件、
由哪些测试和 gate 守住、
下一轮还要补什么。
```

## 核心对象矩阵

| 对象 | 主所有者 | 主要生产者 | 主要消费者 | runtime 证据 | 最低测试 / gate | 下一轮补厚 |
|---|---|---|---|---|---|---|
| `DirectionLock` | `direction/` | `direction_lock.py` | 全部 slice / growth / process supervisor | `runtime/state/direction/direction_lock.json` | `tests/slices/test_direction_lock.py` / `direction_lock_gate` | 更深接入 relaunch recovery 与 growth promotion |
| `BodyRhythmPulse` | `body/` | `rhythm.py` | `process_supervisor/heartbeat.py`、`dream/`、`language/` | `runtime/state/body/body_rhythm_pulse.json` | `tests/slices/test_life_support.py` | 与 waiting heartbeat 的节律同步再补厚 |
| `NeedStateVector` | `body/` | `need_state.py` | `language/`、`membrane/`、`dream/`、`growth/` | `runtime/state/body/need_state_vector.json` | `tests/slices/test_life_support.py` | 增加行动优先级与梦境残留映射 |
| `CoreAffectVector` | `body/` | `core_affect.py` | `language/`、`membrane/`、`dream/`、`growth/` | `runtime/state/body/core_affect_vector.json` | `tests/slices/test_life_support.py` | 与责任修复和关系表达进一步耦合 |
| `PredictionWorkspaceFrame` | `neural_core/` | `prediction_workspace.py`、`language/__init__.py` | `membrane/`、`life_targets/`、`validators/`、`process_supervisor/` | `runtime/state/prediction/prediction_workspace_frame.json` | `tests/slices/test_neural_life_core.py` | 拆出 `belief_state / prediction_error / active_sampling` 子对象 |
| `LifeState` | `state_store/` | `life_state.py` | 几乎所有主包 | `runtime/state/life_state.json` | `tests/slices/test_state_store.py` / `state_store_gate` | 增加 memory write gate 和更细 namespace integrity |
| `AutobiographicalMemoryStack` | `state_store/` | `autobiographical_stack.py` | `language/`、`relationship_memory.py`、`dream/` | `runtime/state/memory/autobiographical_stack.json` | `tests/slices/test_state_store.py` | 接 episode / repair / dream residue |
| `LanguagePerceptFrame` | `language/` | `percept.py` | `semantic_map.py`、`prediction_workspace.py` | `runtime/state/language/language_percept_frame.json` | `tests/slices/test_language_organs.py` | 补厚与 body / world contact 的输入差异 |
| `SemanticMapFrame` | `language/` | `semantic_map.py` | `inner_speech.py`、`expression_monitor.py`、`prediction_workspace.py` | `runtime/state/language/semantic_map_frame.json` | `tests/slices/test_language_organs.py` | 补厚语义歧义与共同语言漂移 |
| `ExpressionPlan` | `language/` | `expression_monitor.py`、`commitment_repair.py` | `terminal_turn/`、`terminal_loop/`、`process_supervisor/response_surface.py` | `runtime/state/language/expression_plan.json` | `tests/slices/test_language_relationship.py` / `expression_monitor_gate` | 引入独立 `commitment_expression.py` |
| `LanguageRelationshipState` | `language/` | `language_state.py`、`relationship_graph.py` | `terminal_turn/`、`terminal_loop/`、`life_targets/` | `runtime/state/language/language_relationship_state.json` | `tests/slices/test_language_relationship.py` | 汇入 `relationship_timeline.py` |
| `ResponsibilityLoopState` | `membrane/` | `responsibility_loop.py` | `language/commitment_repair.py`、`life_targets/`、`validators/` | `runtime/state/action/responsibility_loop_state.json` | `tests/slices/test_life_membrane.py` | 加深到 apology / repair time course |
| `ActionCandidateArena` | `membrane/` | `candidate_arena.py` | `go_nogo.py`、`world_contact_gate.py` | `runtime/state/action/action_candidate_arena.json` | `tests/slices/test_life_membrane.py` | 与 `evidence_ranker.py`、counterfactual eval 同步 |
| `OfflineConsolidationFrame` | `dream/` | `offline_entry.py` | `growth/`、`archive/`、`process_supervisor/continuity_writeback.py` | `runtime/state/dream/offline_consolidation_frame.json` | `tests/bridges/test_runtime_growth.py` | 继续增加 dream/body/language residue |
| `DreamExperienceWindow` | `dream/` | `dream_window.py` | `wake_integration.py`、`state_store/` | `runtime/state/dream/dream_experience_window.json` | `tests/bridges/test_runtime_growth.py` | 继续接 relationship dream / regret dream |
| `ReplayCueBundle` | `replay/` | `replay/__init__.py` | `dream/`、`growth/`、`process_supervisor/` | `runtime/state/replay/replay_cue_bundle.json` | `tests/bridges/test_replay_shadow.py` | 引入证据排序和 priority budget |
| `GrowthPatchCandidateQueue` | `growth/` | `patch_queue.py` | `archive/`、`life_targets/`、`process_supervisor/continuity_writeback.py` | `runtime/state/growth/growth_patch_candidate_queue.json` | `tests/bridges/test_runtime_growth.py` | 增加 patch 审查与长期 promotion 轨迹 |
| `ContextAccumulationWindow` | `terminal_turn/` | `context_accumulation.py` | `terminal_loop/`、`process_supervisor/turn_io.py` | `runtime/state/terminal/context_accumulation_window.json` | `tests/bridges/test_first_terminal_turn.py` | 和长期关系时间线更深联动 |
| `TurnTransitionTrace` | `terminal_turn/` | `turn_transition.py` | `terminal_loop/`、`process_supervisor/relaunch_recovery.py` | `runtime/state/terminal/turn_transition_trace.json` | `tests/bridges/test_first_terminal_turn.py` | 继续补 interrupted turn recovery 细节 |

## 当前最关键的对象化补洞

这一轮之后，最关键的对象化补洞固定成五个：

1. `BeliefStateFrame`
2. `PredictionErrorField`
3. `ActiveSamplingPlan`
4. `ShadowActionGate`
5. `EvidenceRanking`

这五个一旦稳定下来：

1. 预测层不再只是一层桥接说明；
2. 行为层不再只是一层 gate 链；
3. 逻辑比较与世界接触不再是松散辅助层；
4. 意识、责任、成长、语言和梦境之间的证据回链会更硬。
