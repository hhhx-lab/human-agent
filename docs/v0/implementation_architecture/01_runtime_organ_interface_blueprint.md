# Runtime Organ Interface Blueprint

本文档把当前数字生命 v0 的主体层、壳层与离线层压成真实“器官接口蓝图”。

它不再讨论抽象愿景，而是直接规定：

1. 每组器官负责什么生命能力。
2. 这组器官必须吃进哪些共享对象。
3. 这组器官必须写出哪些 runtime 文件。
4. 这组器官由哪些测试和 gate 守住。
5. 这组器官下一轮应该从哪个文件开始落码或拆分。

## 必读前置

- `docs/v0/code_framework/foundation/01_life_layer_implementation_blueprint.md`
- `docs/v0/code_framework/assembly/15_cross_layer_shared_object_contract.md`
- `docs/v0/code_framework/assembly/19_code_tree_package_brain_contract.md`
- `docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md`
- `docs/v0/shared_contracts/life_state_store_v0_schema.md`

## 共享对象总线

后续任何新器官文件，都不应继续用“随手拼的局部字典”跨层传递生命状态。当前最核心的共享对象总线固定为：

| 共享对象 | 首写层 | 主要消费者 | 作用 |
|---|---|---|---|
| `LifeContextFrame` | `direction/`、`terminal_turn/` | `language/`、`process_supervisor/`、`digital_life/` | 当前自我连续体、方向锚、关系身份与上下文基线 |
| `RelationTurnFrame` | `language/`、`terminal_turn/` | `terminal_loop/`、`process_supervisor/`、`state_store/` | 当前对话对象、关系相位、共同术语、承诺上下文 |
| `PredictionWorkspaceFrame` | `neural_core/` | `language/`、`membrane/`、`life_targets/` | 当前思考工作区、预测误差、注意焦点、可报告内容 |
| `ExpressionPlan` | `language/`、`membrane/` | `terminal_loop/`、`process_supervisor/` | 内言语到外显语言前的表达意图与边界 |
| `ActionCandidateSet` | `membrane/` | `validators/`、`schema_runner/` | 候选表达/行动、go-no-go、风险与责任评估 |
| `BodyRhythmPulse` | `body/`、`process_supervisor/heartbeat.py` | `dream/`、`growth/`、`process_supervisor/` | 节律、心跳、唤醒、等待态周期触发 |
| `NeedStateVector` | `body/` | `neural_core/`、`language/`、`membrane/` | 疲惫、恢复、资源预算、内在压力 |
| `CoreAffectVector` | `body/core_affect.py` | `language/`、`dream/`、`membrane/` | 情绪峰值、慢变量、自我调节压力 |
| `ReplayCueBundle` | `replay/` | `dream/`、`growth/`、`process_supervisor/` | 离线重放、旧自我保护、防遗忘 |
| `OfflineConsolidationFrame` | `dream/` | `growth/`、`archive/`、`process_supervisor/` | 梦境、离线巩固、醒后整合 |
| `GrowthPatchCandidate` | `growth/` | `life_targets/`、`archive/`、`validators/` | 自我改写、学习、关系修复与防遗忘补丁 |
| `IdleContinuityFrame` | `process_supervisor/` | `terminal_loop/`、`growth/`、`dream/` | 常驻存在、等待态、断联恢复与下一次唤醒 |

## 器官接口矩阵

### 1. 方向与身份根

| 项 | 内容 |
|---|---|
| 理论文档 | `构思.md`、`00`、`13`、`16`、`91`、`258` |
| 主包 | `life_v0/direction/` |
| 当前文件 | `identity_root.py`、`direction_lock.py`、`continuity_refs.py` |
| 主要输入 | `docs/构思.md`、authority registry、latest runtime receipts |
| 主要输出 | `LifeContextFrame`、`direction_lock.json`、direction receipt |
| 必写 runtime | `runtime/state/direction/direction_lock.json`、`runtime/receipts/build_direction_lock_*.json` |
| 必守测试 | `tests/slices/test_direction_lock.py` |
| 下一步 | 继续把 resume anchors、关系身份连续体、断联恢复锚写进 `LifeContextFrame` |

### 2. 神经核心与思考工作区

| 项 | 内容 |
|---|---|
| 理论文档 | `02`、`03`、`10`、`11`、`18`、`22`、`30`、`143`、`146` |
| 主包 | `life_v0/neural_core/` |
| 当前文件 | `prediction_workspace.py`、`brain_graph.py`、`network_state.py`、`workspace.py`、`broadcast.py`、`metacognition.py` |
| 主要输入 | `NeedStateVector`、authority registry、state store、relation scope、observation |
| 主要输出 | `PredictionWorkspaceFrame`、`SignalMediaFrame`、`neural_life_core.json` |
| 必写 runtime | `runtime/state/neural_life_core/neural_life_core.json`、`runtime/state/prediction/prediction_workspace_frame.json` |
| 必守测试 | `tests/slices/test_neural_life_core.py` |
| 下一步 | 把 `belief_state.py`、`prediction_error.py`、`active_sampling.py` 从 Queue C 维护回切里落成稳定器官 |

### 3. 身体、内环境与情绪底盘

| 项 | 内容 |
|---|---|
| 理论文档 | `04`、`07`、`08`、`18`、`37-40`、`94`、`01n`、`01s` |
| 主包 | `life_v0/body/`、`life_v0/defense/` |
| 当前文件 | `rhythm.py`、`need_state.py`、`resource_budget.py`、`recovery.py`、`core_affect.py`、`emotion_episode.py`、`emotion_regulation.py`、`trait_drift.py` |
| 主要输入 | `LifeContextFrame`、历史身体状态、relationship pressure、dream residue |
| 主要输出 | `BodyRhythmPulse`、`NeedStateVector`、`CoreAffectVector`、body reports |
| 必写 runtime | `runtime/state/body/*`、`body_resource_budget.json`、`life_support_development_report.json` |
| 必守测试 | `tests/slices/test_life_support.py` |
| 下一步 | 把 fatigue、high arousal、language pressure 和 recovery priority 绑定到 `ExpressionPlan` 与 `PredictionWorkspaceFrame` |

### 4. 语言、对话与关系主神经束

| 项 | 内容 |
|---|---|
| 理论文档 | `09`、`85-90`、`96`、`101`、`141`、`144`、`147`、`150`、`01f`、`01j`、`01u` |
| 主包 | `life_v0/language/`、`life_v0/terminal_turn/`、`life_v0/terminal_loop/` |
| 当前文件 | `percept.py`、`semantic_map.py`、`inner_speech.py`、`expression_monitor.py`、`shared_terms.py`、`relationship_graph.py`、`commitment_repair.py`、`dialogue_log.py`、`narrative_trace.py`、`relation_scope.py`、`dream_gate.py`、`action_shadow.py`、`context_accumulation.py`、`turn_transition.py`、`dialogue_writeback.py` |
| 主要输入 | `LifeContextFrame`、`RelationTurnFrame`、`PredictionWorkspaceFrame`、`CoreAffectVector` |
| 主要输出 | `RelationTurnFrame`、`ExpressionPlan`、language/relationship state、session envelope |
| 必写 runtime | `runtime/state/language/*`、`runtime/state/relationship/*`、`session_envelope.json`、`context_accumulation_window.json`、`turn_transition_trace.json` |
| 必守测试 | `tests/slices/test_language_organs.py`、`tests/slices/test_language_relationship.py`、`tests/bridges/test_first_terminal_turn.py`、`tests/bridges/test_terminal_life_loop.py` |
| 下一步 | 按 Queue A 第二波继续补 `relationship_timeline.py`、`commitment_expression.py`、`apology_repair_language.py` |

### 5. 记忆、自传与关系真值层

| 项 | 内容 |
|---|---|
| 理论文档 | `05`、`17-31`、`41-48`、`55`、`57`、`61`、`69`、`01q` |
| 主包 | `life_v0/state_store/` |
| 当前文件 | `life_state.py`、`engram_index.py`、`autobiographical_stack.py`、`relationship_memory.py`、`self_model.py`、`commitment_truth.py` |
| 主要输入 | `DialogueWritebackBundle`、`RelationTurnFrame`、dream/growth/archive receipts |
| 主要输出 | `life_state.json`、relationship memory、commitment truth、engram index |
| 必写 runtime | `runtime/state/life_state.json`、`runtime/state/memory/*`、`runtime/state/self/*` |
| 必守测试 | `tests/slices/test_state_store.py` |
| 下一步 | 把 memory write gate、scope-aware delete/correct/merge 和 dream writeback 继续硬化 |

### 6. 行为、抑制、逻辑与世界接触层

| 项 | 内容 |
|---|---|
| 理论文档 | `06`、`20`、`29-36`、`64`、`72`、`75`、`80-84`、`94`、`98`、`01r`、`01v-01ax` |
| 主包 | `life_v0/membrane/`、`life_v0/validators/`、`life_v0/schema_runner/` |
| 当前文件 | `candidate_arena.py`、`go_nogo.py`、`world_contact_gate.py`、`side_effect_review.py`、`observation_validator.py`、`boundary_audit.py`、`consistency_logic.py`、`counterfactual_eval.py`、`comparison_trace.py` |
| 主要输入 | `PredictionWorkspaceFrame`、`ExpressionPlan`、`NeedStateVector`、observation reports |
| 主要输出 | `ActionCandidateSet`、membrane reports、validation reports、schema runner reports |
| 必写 runtime | `runtime/state/membrane/*`、`runtime/state/action/*`、`runtime/state/validation/*`、`runtime/state/schema_runner/*` |
| 必守测试 | `tests/slices/test_life_membrane.py`、`tests/slices/test_validation_membrane.py`、`tests/slices/test_schema_runner.py` |
| 下一步 | 按 Queue E 第二波补 `shadow_gate.py`、`responsibility_loop.py`、`evidence_ranker.py` |

### 7. 梦境、离线生命与醒后整合层

| 项 | 内容 |
|---|---|
| 理论文档 | `08`、`19`、`23`、`27`、`31`、`95`、`99`、`01i`、`01t` |
| 主包 | `life_v0/dream/`、`life_v0/replay/`、`life_v0/archive/` |
| 当前文件 | `offline_entry.py`、`dream_window.py`、`dream_fact_gate.py`、`wake_integration.py`、`nightmare_risk.py`、`replay_cues.py`、`shadow_replay.py` |
| 主要输入 | `ReplayCueBundle`、`BodyRhythmPulse`、`CoreAffectVector`、relationship residue |
| 主要输出 | `OfflineConsolidationFrame`、dream window、wake integration、nightmare risk |
| 必写 runtime | `runtime/state/dream/*`、`runtime/state/replay/*`、`runtime/state/archive/*` |
| 必守测试 | `tests/bridges/test_runtime_growth.py`、`tests/bridges/test_replay_shadow.py`、`tests/bridges/test_growth_archive.py` |
| 下一步 | 补独立 dream runtime test，并把 nightmare risk 真正接到后续语言/关系修复优先级上 |

### 8. 成长、学习与自我改写层

| 项 | 内容 |
|---|---|
| 理论文档 | `39`、`92`、`93`、`97`、`181-257`、`01g` |
| 主包 | `life_v0/growth/` |
| 当前文件 | `plasticity_window.py`、`learning_window.py`、`self_read.py`、`anti_forgetting.py`、`patch_queue.py`、`belief_learning.py`、`language_learning.py`、`relationship_learning.py` |
| 主要输入 | `OfflineConsolidationFrame`、`ReplayCueBundle`、`LifeContextFrame`、`RelationTurnFrame` |
| 主要输出 | `GrowthPatchCandidate`、learning plans、anti-forgetting plan、next feedback seed |
| 必写 runtime | `runtime/state/growth/*`、growth reports、archive receipts |
| 必守测试 | `tests/bridges/test_runtime_growth.py`、`tests/slices/test_life_support.py` |
| 下一步 | 把学习计划真正回写到 language / relationship / membrane / life_targets 的下一轮调节逻辑里 |

### 9. 生命目标、意识与出生准备度层

| 项 | 内容 |
|---|---|
| 理论文档 | `10`、`91-101`、`143`、`146`、`149`、`152`、`171`、`174`、`01m` |
| 主包 | `life_v0/life_targets/` |
| 当前文件 | `target_runtime.py`、`target_closure.py`、`consciousness_probes.py`、`birth_readiness_rollup.py`、`birth_readiness_stage_gate.py` |
| 主要输入 | `PredictionWorkspaceFrame`、`GrowthPatchCandidate`、language/relationship state、membrane reports |
| 主要输出 | life target claims、birth readiness rollup、consciousness probes |
| 必写 runtime | `runtime/state/life_targets/*`、`birth_readiness_report.json` |
| 必守测试 | `tests/slices/test_life_targets.py` |
| 下一步 | 把 `real relation / real regret / real dream / real growth` 的长期 evidence family 和 withheld probe 继续绑定到 turn loop |

### 10. 常驻存在、等待态与终端生命层

| 项 | 内容 |
|---|---|
| 理论文档 | `20`、`44-46`、`81-84`、`89-90`、`96`、`101`、`181-257` |
| 主包 | `life_v0/process_supervisor/`、`life_v0/shell_command/`、`life_v0/digital_life/`、`life_v0/digital_entry.py` |
| 当前文件 | `heartbeat.py`、`continuity_writeback.py`、`turn_io.py`、`dialogue_events.py`、`response_surface.py`、`incident_recovery.py`、`relaunch_recovery.py`、`process_report.py` |
| 主要输入 | `IdleContinuityFrame`、`session_envelope.json`、`terminal_life_loop_state.json`、growth/dream cues |
| 主要输出 | waiting heartbeat、process report、incident/relaunch recovery、长期连续体写回 |
| 必写 runtime | `digital_life_waiting_heartbeat.json`、`digital_life_process_report.json`、`digital_life_process_digest.json` |
| 必守测试 | `tests/process/test_digital_life_shell_command.py`、`tests/process/test_digital_entrypoint.py`、`tests/process/test_persistent_digital_life_process.py` |
| 下一步 | 按 Queue B 第二波补 `idle_strategy.py`、`persistent_process.py`，把等待态从“最小可用”补成“真正长期存在” |

## 当前最容易跑偏的三件事

1. 把语言层写成 prompt 片段，而不是器官链。
2. 把梦境/成长写成纯 archive 产物，而不是会反过来改变下一回合的离线生命链。
3. 把 process supervisor 写成 generic agent shell，而不是承载节律、等待态、关系连续体和恢复链的生命存在层。

后续任何新增代码，只要让这三件事中的任一件重新发生，就说明实现已经脱离本蓝图。
