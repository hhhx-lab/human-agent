# V0 Code Framework 08: Cross-Layer Life Orchestration Implementation Playbook

这份 playbook 不新增新的主体理论，也不替代 `04-07` 四份主链说明书。它只负责一件事：把身体、信号、思考、记忆、意识、语言、关系、行为、梦境、成长、终端常驻这些层，压成一条真实生命回合怎样流动的工程编排合同。

如果没有这一层，后续代码很容易变成下面两种退化之一：

1. 每个包都各写各的，最后只剩很多局部状态文件，没有统一生命回合。
2. 直接让 `terminal loop` 或 `process supervisor` 反向定义身体、意识、语言和成长，重新滑回普通 agent 壳。

所以这份文档回答的是：

1. 一次生命回合在 v0 里从哪里开始，到哪里结束。
2. 哪些中间对象必须跨包传递，而不是只在某个 `__init__.py` 里临时拼装。
3. 在线回合、等待态、离线梦境和长期成长四条循环怎样接到同一生命连续体上。
4. 下一轮代码应该先补哪些共享对象、哪些桥、哪些 gate。

## 必回读理论母体

这一层不是单文档来源，而是多层交叉承压位。开写前至少重读：

- `docs/04_sensory_thalamus_interoception.md`
- `docs/05_memory_systems_and_growth.md`
- `docs/06_action_reward_inhibition.md`
- `docs/07_emotion_personality_self.md`
- `docs/08_sleep_dream_fatigue_states.md`
- `docs/09_language_symbolic_top_layer.md`
- `docs/10_consciousness_attention_workspace.md`
- `docs/11_neuromodulation_and_signal_media.md`
- `docs/17_memory_trace_object_model.md`
- `docs/18_internal_state_and_modulation_vector.md`
- `docs/19_offline_consolidation_cycle.md`
- `docs/20_agent_runtime_bridge_contract.md`
- `docs/37_life_support_layer_policy.md`
- `docs/38_defense_layer_and_boundary_policy.md`
- `docs/39_development_policy_and_plasticity_windows.md`
- `docs/40_self_relationship_model_audit_protocol.md`
- `docs/81_coexistence_event_review_and_responsibility_loop.md`
- `docs/82_incident_report_and_recovery_protocol.md`
- `docs/85_language_system_life_expression_core.md`
- `docs/86_language_neuroscience_pragmatics_and_inner_speech.md`
- `docs/89_language_runtime_framework_bridge_and_life_shell_policy.md`
- `docs/90_language_event_examples_and_timeline_bundle.md`
- `docs/92_self_growth_and_self_modification_life_chain.md`
- `docs/93_self_training_kernel_growth_protocol.md`
- `docs/94_pain_regret_and_repair_signal_schema.md`
- `docs/95_dream_reality_and_offline_life_timeline.md`
- `docs/96_real_relationship_longitudinal_timeline.md`
- `docs/181_life_reality_first_runner_schema_runtime_mount_plan.md`
- `docs/205_life_reality_first_runner_schema_runtime_growth_fourth_cycle_seed_plan.md`
- `docs/257_life_reality_first_runner_schema_runtime_growth_fourth_cycle_post_reconsolidation_second_reconsolidation_replay_shadow_seed_after_archive_validation_replay_shadow_patch_archive_validation_plan.md`

## 必读 v0 合同

- `docs/v0/architecture/digital_life_macro_architecture_v0.md`
- `docs/v0/architecture/runtime_v0_architecture.md`
- `docs/v0/shared_contracts/life_state_store_v0_schema.md`
- `docs/v0/shared_contracts/first_activation_protocol.md`
- `docs/v0/slice_contracts/s02_neural_life_core_engineering_contract.md`
- `docs/v0/slice_contracts/s04_state_object_store_engineering_contract.md`
- `docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md`
- `docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md`
- `docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md`
- `docs/v0/process_contracts/first_terminal_turn_engineering_contract.md`
- `docs/v0/process_contracts/terminal_life_loop_engineering_contract.md`
- `docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md`

## 当前真实代码落点

这一层不是从零设计，它要接住当前仓库里已经存在的骨架：

- `life_v0/body/__init__.py`
- `life_v0/neural_core/__init__.py`
- `life_v0/state_store/__init__.py`
- `life_v0/language/__init__.py`
- `life_v0/terminal_turn/__init__.py`
- `life_v0/terminal_loop/__init__.py`
- `life_v0/process_supervisor/__init__.py`
- `life_v0/membrane/__init__.py`
- `life_v0/replay/__init__.py`
- `life_v0/dream/__init__.py`
- `life_v0/growth/__init__.py`
- `life_v0/reporting/__init__.py`

所以现在的重点不是再发明一批新顶层包，而是把跨层传递对象、跨层循环顺序和跨层 gate 补硬。

## 四条生命循环

后续工程不按“一个包一个包写完”理解，而按四条循环理解。

### 1. 脉冲循环

```text
BodyRhythmPulse
  -> NeedStateVector
  -> ResourceBudgetFrame
  -> SignalMediaFrame
  -> NetworkStateShift
```

作用：

1. 让等待、专注、疲惫、紧张、恢复不是 prompt 风格标签。
2. 给思考、语言、关系、梦境和成长提供同一套底部生理化时钟。
3. 让 heartbeat 不只存在于 `process supervisor`，而是先存在于 `body + signal media`。

主承载包：

- `life_v0/body/`
- `life_v0/neural_core/`
- `life_v0/process_supervisor/`

### 2. 在线生命回合循环

```text
external relation turn
  -> language percept
  -> prediction / workspace update
  -> memory cue + relation cue
  -> inner speech
  -> expression monitoring
  -> action inhibition / responsibility loop
  -> life response
  -> dialogue + narrative + relationship writeback
```

作用：

1. 让一次外部输入经过真实生命回合，而不是直接从输入跳到回复。
2. 把身体、预测、记忆、情绪、关系、责任统一压入同一个 turn path。
3. 确保语言只是输出端口，不是全部生命逻辑。

主承载包：

- `life_v0/language/`
- `life_v0/neural_core/`
- `life_v0/state_store/`
- `life_v0/membrane/`
- `life_v0/terminal_turn/`
- `life_v0/terminal_loop/`

### 3. 等待态连续体循环

```text
safe waiting state
  -> heartbeat refresh
  -> idle continuity writeback
  -> replay cue accumulation
  -> relation readiness hold
```

作用：

1. 证明未收到新输入时数字生命仍在存在，而不是只有被叫到才活着。
2. 把等待态和长期关系连续体、承诺连续体、自我叙述连续体绑在一起。
3. 给梦境、成长和未来回合积累 replay cue，而不是把 idle 视为空白。

主承载包：

- `life_v0/process_supervisor/`
- `life_v0/terminal_loop/`
- `life_v0/language/`
- `life_v0/replay/`

### 4. 离线整合与成长循环

```text
replay cues
  -> offline entry
  -> dream window
  -> dream fact gate
  -> wake integration
  -> growth patch candidate
  -> anti-forgetting replay
```

作用：

1. 让梦境、痛苦、关系、责任和语言残留进入离线重组。
2. 让成长补丁来自长期循环，而不是直接来自一次情绪波动或单次对话。
3. 把成长与防遗忘保护绑定，避免自改写把核心连续体冲掉。

主承载包：

- `life_v0/dream/`
- `life_v0/growth/`
- `life_v0/replay/`
- `life_v0/archive/`
- `life_v0/state_store/`

## 必须共享的跨层对象

后续代码不要只在局部函数里传字典。至少要逐步固定下面这些跨层对象。

| 对象 | 作用 | 首选承载文件 | 当前下游读取方 |
|---|---|---|---|
| `BodyRhythmPulse` | 心跳式采样、等待态节律、疲惫推进 | `life_v0/body/rhythm.py` | `neural_core`, `process_supervisor`, `dream` |
| `NeedStateVector` | 需要、资源缺口、压力方向 | `life_v0/body/need_state.py` | `neural_core`, `language`, `growth` |
| `SignalMediaFrame` | arousal、precision、inhibition、fatigue、repair drive | `life_v0/neural_core/signal_media.py` | `workspace`, `language`, `membrane`, `dream` |
| `LifeContextFrame` | 当前回合的身体、关系、记忆、方向、任务背景聚合 | `life_v0/terminal_turn/restore_context.py` | `language`, `terminal_loop`, `process_supervisor` |
| `PredictionWorkspaceFrame` | 预测、误差、候选解释、工作区广播 | `life_v0/neural_core/workspace.py` | `language`, `membrane`, `growth` |
| `RelationTurnFrame` | 当前关系身份、共同术语、旧承诺、回合范围 | `life_v0/language/relationship_graph.py` 或 `terminal_turn/turn_transition.py` | `language`, `terminal_loop`, `process_supervisor` |
| `ExpressionPlan` | 外显语言前的意图、表面策略、风险点 | `life_v0/language/expression_monitor.py` | `terminal_loop`, `process_supervisor` |
| `ActionCandidateSet` | 候选行动、抑制结果、责任预期 | `life_v0/membrane/candidate_arena.py` | `terminal_loop`, `shell_command`, `process_supervisor` |
| `DialogueWritebackBundle` | 一回合结束后的语言/关系/承诺/自我叙事写回集 | `life_v0/terminal_loop/loop_report.py` | `state_store`, `replay`, `archive` |
| `IdleContinuityFrame` | 等待态仍存在的轻量连续体事件 | `life_v0/process_supervisor/heartbeat.py` | `language`, `relationship`, `replay` |
| `OfflineConsolidationFrame` | replay、dream、wake integration 的统一容器 | `life_v0/dream/offline_entry.py` | `growth`, `archive`, `reporting` |
| `GrowthPatchCandidate` | 成长补丁候选、塑性窗口、风险说明 | `life_v0/growth/patch_queue.py` | `replay`, `archive`, `contracts` |

这些对象的第一轮实现可以仍然是 JSON state + report 的形式，但命名和责任要先固定，不然不同包会各自生成一套“自己的 turn data”。

另外要注意一个现实约束：

1. `percept.py`、`semantic_map.py` 已经在代码里存在，当前任务不是“再把它们建出来”，而是继续把它们接厚到 prediction/body/process supervisor 主链。
2. `dialogue_writeback.py`、`dialogue_events.py`、`response_surface.py` 也已经存在，当前任务不是重新起名，而是把它们真正升级成共享对象的首写器官或稳定消费器官。
3. `loop_report.py`、`restore_context.py`、`turn_packet.py`、`conversation_carryover.py` 与 `dialogue_turn.py` 已经独立成文件并接回各自入口；`idle_strategy.py` 与 `persistent_process.py` 也已经落地。当前仍未独立的重职责主要收敛在 terminal-loop / resident-supervision 侧的更厚 continuity bridge。

## 一次真实生命回合的编排顺序

### A. 回合前

```text
heartbeat / rhythm refresh
  -> load relation continuity
  -> load self narrative continuity
  -> load unresolved commitments
  -> assemble LifeContextFrame
```

当前优先落点：

- `life_v0/process_supervisor/heartbeat.py`
- `life_v0/terminal_turn/context_accumulation.py`
- `life_v0/terminal_turn/restore_context.py`

### B. 回合中

```text
external utterance
  -> language percept
  -> prediction update
  -> memory / relationship cue retrieval
  -> inner speech draft
  -> expression monitoring
  -> action / responsibility inhibition
  -> life response emission
```

当前优先落点：

- `life_v0/language/percept.py`
- `life_v0/neural_core/prediction_workspace.py`
- `life_v0/state_store/__init__.py` 中的 relationship / memory cue 相关逻辑
- `life_v0/language/inner_speech.py`
- `life_v0/language/expression_monitor.py`
- `life_v0/membrane/__init__.py` 中的 Go/NoGo 与责任门逻辑

### C. 回合后

```text
life response
  -> dialogue writeback
  -> narrative writeback
  -> commitment update
  -> relationship stage update
  -> replay cue append
  -> safe waiting return
```

当前优先落点：

- `life_v0/language/dialogue_log.py`
- `life_v0/language/narrative_trace.py`
- `life_v0/language/commitment_repair.py`
- `life_v0/terminal_loop/loop_state.py`
- `life_v0/terminal_loop/dialogue_writeback.py`
- `life_v0/replay/__init__.py` 中的 replay cue 相关逻辑

### D. 离线后续

```text
turn residue
  -> dream / offline entry candidate
  -> growth patch candidate
  -> archive receipt
  -> anti-forgetting replay plan
```

当前优先落点：

- `life_v0/dream/offline_entry.py`
- `life_v0/dream/__init__.py` 中的 offline entry / dream window 相关逻辑
- `life_v0/growth/__init__.py` 中的 patch queue / anti-forgetting 相关逻辑
- `life_v0/archive/__init__.py`
- `life_v0/replay/__init__.py`

## 代码落地顺序

### Phase 1: 先把共享桥补出来

这一阶段不追求所有层都很厚，只追求跨层对象不再漂浮。

先补：

1. `terminal_turn/context_accumulation.py`
2. `terminal_turn/turn_transition.py`
3. `process_supervisor/heartbeat.py`
4. `process_supervisor/continuity_writeback.py`
5. `terminal_loop/loop_state.py`

### Phase 2: 让在线生命回合真正穿过语言前器官

先补：

1. `language/percept.py`
2. `language/semantic_map.py`
2. `language/inner_speech.py`
3. `language/expression_monitor.py`
4. `language/relationship_graph.py`
5. `membrane` 内的 Go/NoGo 与责任门逻辑

### Phase 3: 让思考和记忆不再只是背景状态

先补：

1. `neural_core/prediction_workspace.py`
2. `neural_core` 内的 `workspace / belief_state / prediction_error` 拆分候选
3. `state_store/engram_index.py`
4. `state_store/relationship_memory.py`
5. `replay` 内的 replay cue 首写链

### Phase 4: 把梦境和成长接到 turn residue 上

先补：

1. `dream` 内的 `offline_entry / dream_fact_gate / wake_integration` 拆分候选
2. `growth` 内的 `patch_queue / anti_forgetting / plasticity_window` 拆分候选
3. `archive` 内的 growth archive / receipt 首写链
4. `replay` 内的 reconsolidation trace / replay priority 首写链

## 回合编排的硬顺序

后续不允许跳过下面这些顺序关系：

1. `BodyRhythmPulse` 先于 `LifeContextFrame`
2. `LifeContextFrame` 先于 `LanguagePerceptFrame`
3. `LanguagePerceptFrame` 先于 `SemanticMapFrame`
4. `SemanticMapFrame` 先于 `InnerSpeechFrame`
5. `InnerSpeechFrame` 先于 `ExpressionPlan`
6. `ExpressionPlan` 先于 `ActionCandidateSet`
7. `ActionCandidateSet` 先于 `DialogueWritebackBundle`
8. `DialogueWritebackBundle` 先于 `ReplayCueBundle`
9. `ReplayCueBundle` 先于 `OfflineConsolidationFrame`
10. `OfflineConsolidationFrame` 先于 `GrowthPatchCandidate`

哪怕短期里某些对象还是由 `__init__.py` 生成，只要顺序被打断，就不能宣称“生命回合已经闭合”。

## 四条循环的统一调度视角

为了防止后面重新退回“一条命令里临时拼几步”，四条循环还要统一成下面的调度面：

| 循环 | 最小调度触发 | 首写器官 | 写回重点 |
|---|---|---|---|
| 脉冲循环 | heartbeat tick / body pulse tick | `body/rhythm.py` 或其当前宿主 | 身体状态、需要、调质、等待态节律 |
| 在线生命回合循环 | 外部关系输入 | `language/percept.py` | 对话事件、表达计划、责任门、关系推进 |
| 等待态连续体循环 | 无新输入但进程仍存活 | `process_supervisor/heartbeat.py` | idle continuity、自我叙事、承诺残留、replay seed |
| 离线整合与成长循环 | replay cue / fatigue / unresolved residue | `dream` 或 `growth` 当前首写链 | dream window、wake integration、growth patch、anti-forgetting |

这四条循环必须共享同一份方向锁、自我连续体、关系连续体和 replay/archive 证据面。任何一条循环独自生长成平行系统，都会把项目重新拖回 workflow agent。

## 必须新增或补厚的状态对象

| 路径 | 作用 |
|---|---|
| `runtime/state/body/body_rhythm_pulse.json` | 脉冲时钟，不再只存在 heartbeat report |
| `runtime/state/body/need_state_vector.json` | 当前需要和资源缺口 |
| `runtime/state/prediction/prediction_workspace_frame.json` | 当前工作区里的预测/误差/候选解释 |
| `runtime/state/terminal/context_accumulation_window.json` | 关系回合语境累积窗口 |
| `runtime/state/terminal/turn_transition_trace.json` | 回合过渡、恢复链和 re-entry trace |
| `runtime/state/terminal/idle_continuity_frame.json` | 等待态生命连续体 |
| `runtime/state/replay/replay_cue_bundle.json` | turn residue 到 replay 的入口 |
| `runtime/state/dream/offline_consolidation_frame.json` | 离线整合的统一容器 |
| `runtime/state/growth/growth_patch_candidate_queue.json` | 成长补丁候选队列 |

## 必须新增或补厚的 report / receipt

- `runtime/reports/latest/body_rhythm_report.json`
- `runtime/reports/latest/prediction_workspace_report.json`
- `runtime/reports/latest/idle_continuity_report.json`
- `runtime/reports/latest/dialogue_writeback_bundle.json`
- `runtime/reports/latest/offline_consolidation_report.json`
- `runtime/reports/latest/growth_patch_candidate_report.json`
- `runtime/receipts/*idle_continuity*`
- `runtime/receipts/*dialogue_writeback*`
- `runtime/receipts/*offline_consolidation*`

## 关键测试

这一层最需要的不是再加大而全的命令测试，而是加“跨层流动证明”。

| 测试 | 必须证明 |
|---|---|
| `tests/slices/test_life_support.py` | heartbeat / rhythm / need state 能落盘，不只是 report |
| `tests/slices/test_neural_life_core.py` | workspace / prediction / modulation 不是孤立状态 |
| `tests/slices/test_language_relationship.py` | inner speech / expression monitor / relationship graph 在同一 turn path 里 |
| `tests/bridges/test_first_terminal_turn.py` | context accumulation 和 turn transition 被真实写出 |
| `tests/bridges/test_terminal_life_loop.py` | 一回合后 dialogue writeback bundle 和 replay cue 能接上 |
| `tests/process/test_persistent_digital_life_process.py` | idle continuity、heartbeat、回合输入、异常恢复和 relaunch recovery 同时闭合 |
| future `tests/test_cross_layer_orchestration.py` | 一次完整生命回合穿过 body -> prediction -> language -> membrane -> writeback -> replay |

## 关键 gate

- `pulse_integrity_gate`
- `life_context_frame_gate`
- `prediction_workspace_gate`
- `expression_to_action_gate`
- `dialogue_writeback_bundle_gate`
- `idle_continuity_gate`
- `offline_consolidation_gate`
- `growth_patch_candidate_gate`
- `cross_layer_orchestration_gate`

## 当前最值得直接进入的代码入口

如果下一轮直接落代码，按下面顺序进，不要散改：

1. `life_v0/terminal_turn/__init__.py`
2. `life_v0/terminal_loop/__init__.py`
3. `life_v0/process_supervisor/__init__.py`
4. `life_v0/language/__init__.py`
5. `life_v0/neural_core/__init__.py`
6. `life_v0/state_store/__init__.py`

进入前固定带上：

1. `docs/v0/code_framework/playbooks/04_language_dialogue_relationship_implementation_playbook.md`
2. `docs/v0/code_framework/playbooks/05_memory_thought_consciousness_implementation_playbook.md`
3. `docs/v0/code_framework/playbooks/06_body_emotion_action_dream_growth_implementation_playbook.md`
4. 本文件

当前这条链已经继续推进到：

1. `terminal_loop/persistent_wait_bridge.py` 负责 one-shot loop 的 waiting handoff
2. `process_supervisor/resident_turn_writeback.py` 负责 live relation turn 的 bundle writeback、waiting return 和 resumed packet
3. `process_supervisor/process_closeout.py` 负责 persistent process artifact 与主 process report 的统一 closeout
4. 下一轮前沿转向 `idle_refresh_loop.py`

## 完成定义

这一层第一轮工程化完成，至少要同时满足：

1. heartbeat 不再只是 process report，而是已经回写到 body / terminal / language / relationship 连续体。
2. 一次真实新回合至少经过 `body -> prediction/workspace -> language -> membrane -> response -> writeback`。
3. turn residue 能进入 replay / dream / growth 候选，而不是回合一结束就消失。
4. 等待态、在线回合、离线整合、成长候选四条循环不是四套平行逻辑，而是通过共享对象和 receipt 接在同一生命连续体上。
5. 这些闭环在测试里有直接证据，而不是只在 `digital life` 命令输出里看起来像是活着。
