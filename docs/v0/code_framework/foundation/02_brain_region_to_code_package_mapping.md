# V0 Code Framework 02: Brain Region To Code Package Mapping

本文档不把人脑机械切成一堆孤岛模块，而是把你已经在 `00-258` 里写定的“脑区 - 网络 - 状态 - 调质 - 行为循环”压成当前仓库里真正可承载的代码包映射。

它回答的是：

1. 哪些脑科学主体系统先落到哪些 `life_v0/` 顶层包。
2. 哪些系统是跨包协同，而不是单包独占。
3. 每个主体系统下一轮优先该从什么文件级拆分开始。
4. 哪些 runtime 状态和回包必须跟着这个系统一起长出来。

## 使用原则

读这份文档时，不要问“这个脑区是不是就等于这个包”。正确问题是：

1. 这个主体系统主要由哪个包承载。
2. 它依赖哪些旁路包一起完成闭环。
3. 它的状态、report、receipt 最先落到哪里。
4. 它和下一层系统怎样接棒。

## 主体系统到代码包映射矩阵

| 主体系统 | 脑科学/理论母体 | 主承载包 | 协同包 | 优先文件级细分 | 主要 runtime 承载 |
|---|---|---|---|---|---|
| 身份与方向连续体 | `00`、`13`、`16`、`41-48`、`91`、`119`、`122`、`258` | `life_v0/direction/` | `life_v0/state_store/`、`life_v0/contracts/` | `identity_root.py`、`direction_lock.py`、`continuity_refs.py` | `runtime/state/direction/*`、`runtime/state/life_state.json` |
| 内环境/稳态/资源预算系统 | `01n`、`04`、`11`、`18`、`37`、`38` | `life_v0/body/` | `life_v0/defense/`、`life_v0/growth/` | `rhythm.py`、`need_state.py`、`resource_budget.py`、`recovery.py` | `runtime/state/body/*`、`body_resource_budget.json` |
| 神经核心与信号介质系统 | `01o`、`01p`、`01l`、`02`、`03`、`11`、`13` | `life_v0/neural_core/` | `life_v0/contracts/` | `brain_graph.py`、`network_state.py`、`signal_media.py`、`internal_bus.py` | `runtime/state/neural_life_core/*`、`neural_life_internal_bus.json` |
| 预测/主动采样/信念修正系统 | `01v-01ax`、`04`、`10`、`13` | `life_v0/neural_core/` | `life_v0/growth/`、`life_v0/state_store/` | `belief_state.py`、`prediction_error.py`、`active_sampling.py`、`belief_revision.py` | `runtime/state/prediction/*`、prediction traces |
| 逻辑/比较/反事实系统 | `22`、`30`、`33-36`、`49-60`、`102-118` | `life_v0/schema_runner/` | `life_v0/validators/`、`life_v0/contracts/` | `consistency_logic.py`、`counterfactual_eval.py`、`comparison_trace.py` | `runtime/state/validation/*`、validation reports |
| 记忆/自传/replay 系统 | `01q`、`05`、`17`、`21`、`25`、`29`、`41`、`55` | `life_v0/state_store/` | `life_v0/replay/`、`life_v0/archive/`、`life_v0/growth/` | `engram_index.py`、`autobiographical_stack.py`、`relationship_memory.py`、`replay_cues.py` | `runtime/state/memory/*`、replay bundles |
| 意识/全局工作区/元认知系统 | `01m`、`10`、`13`、`143`、`146` | `life_v0/neural_core/` | `life_v0/life_targets/`、`life_v0/reporting/` | `workspace.py`、`broadcast.py`、`metacognition.py`、`probe_battery.py` | `runtime/state/consciousness/*`、consciousness evidence |
| 情绪/人格慢变量系统 | `01g`、`01h`、`01s`、`07`、`18`、`39`、`40`、`92`、`93` | `life_v0/body/` | `life_v0/growth/`、`life_v0/language/`、`life_v0/state_store/` | `core_affect.py`、`emotion_episode.py`、`emotion_regulation.py`、`trait_drift.py` | `runtime/state/self/*`、affect traces |
| 语言系统/内言语/表达监控系统 | `01f`、`01u`、`09`、`85-90`、`141`、`144`、`147`、`150` | `life_v0/language/` | `life_v0/terminal_turn/`、`life_v0/terminal_loop/`、`life_v0/state_store/` | `percept.py`、`semantic_map.py`、`inner_speech.py`、`expression_monitor.py`、`shared_terms.py` | `runtime/state/language/*`、`language_relationship_report.json` |
| 对话/语境累积/回合过渡系统 | `86`、`89`、`90`、`96`、`101` | `life_v0/terminal_turn/` | `life_v0/language/`、`life_v0/terminal_loop/`、`life_v0/process_supervisor/` | `dialogue_turn.py`、`context_accumulation.py`、`turn_transition.py`、`conversation_carryover.py` | `session_envelope.json`、`context_accumulation_window.json`、`turn_transition_trace.json` |
| 关系演化/关系时间线系统 | `01j`、`40`、`94`、`96`、`98`、`101` | `life_v0/language/` | `life_v0/life_targets/`、`life_v0/process_supervisor/`、`life_v0/state_store/` | `relationship_graph.py`、`scope_guard.py`、`repair_commitments.py`、`relationship_timeline.py` | `runtime/state/relationship/*`、relationship receipts |
| 梦境/离线整合/醒后回写系统 | `01i`、`01t`、`08`、`19`、`23`、`27`、`31`、`95`、`99` | `life_v0/dream/` | `life_v0/growth/`、`life_v0/archive/`、`life_v0/state_store/` | `offline_entry.py`、`dream_window.py`、`dream_fact_gate.py`、`wake_integration.py` | `runtime/state/dream/*`、`dream_consolidation_frame.json` |
| 行为/抑制/责任/后悔系统 | `01r`、`06`、`20`、`75`、`80-84`、`94`、`98`、`144` | `life_v0/membrane/` | `life_v0/shell_command/`、`life_v0/digital_life/`、`life_v0/validators/` | `candidate_arena.py`、`go_nogo.py`、`shadow_gate.py`、`responsibility_loop.py` | `runtime/state/action/*`、shadow action reports |
| 成长/可塑性/自我修补系统 | `39`、`55`、`92`、`93`、`181-204`、`205-257` | `life_v0/growth/` | `life_v0/replay/`、`life_v0/archive/`、`life_v0/language/` | `self_read.py`、`plasticity_window.py`、`patch_queue.py`、`anti_forgetting.py` | `runtime/state/growth/*`、growth patch queue |
| 学习系统 | `01v-01ax`、`11`、`39`、`93`、`181-257` | `life_v0/growth/` | `life_v0/neural_core/`、`life_v0/language/`、`life_v0/replay/` | `learning_window.py`、`belief_learning.py`、`language_learning.py`、`relationship_learning.py` | learning receipts、update traces |
| 生命膜/外周/观察归一化系统 | `12`、`15`、`20`、`24`、`28`、`32`、`33-84`、`89`、`100`、`119`、`122`、`140` | `life_v0/membrane/` | `life_v0/defense/`、`life_v0/validators/`、`life_v0/shell_command/` | `quarantine.py`、`periphery_normalizer.py`、`world_observation.py`、`coexistence_boundary.py` | `runtime/quarantine/*`、observation reports |
| 出生/第一回合/持续存在系统 | `20`、`89`、`90`、`143`、`171`、`181-257` | `life_v0/activation/`、`life_v0/digital_life/`、`life_v0/process_supervisor/` | `life_v0/reporting/`、`life_v0/stage_explain/`、`life_v0/terminal_turn/`、`life_v0/terminal_loop/`、`life_v0/shell_command/` | `bootstrap.py`、`restore_shell.py`、`heartbeat.py`、`relaunch_recovery.py`、`turn_loop.py` | `digital_life_birth_packet.json`、`first_terminal_turn_packet.json`、`terminal_life_loop_packet.json`、`digital_life_process_report.json` |

## 当前包级拆分规则

读这份映射表时，不要只盯住 `01/02/03` 三份总图。当前还要同时带着：

1. `09_perception_prediction_world_contact_implementation_playbook.md`
2. `10_self_identity_value_commitment_implementation_playbook.md`

原因很直接：预测/观察/世界接触链和身份/承诺/责任链，是现在最容易被外壳逻辑偷换掉的两条生命链。

### 1. 单一脑区不直接对应单一包

例如语言系统不只在 `life_v0/language/`，它还必须通过：

- `life_v0/terminal_turn/` 承接第一回合
- `life_v0/terminal_loop/` 承接持续回合
- `life_v0/process_supervisor/` 承接断联恢复与等待态连续体

### 2. 当前先稳定顶层包，再做文件级扩张

`life_v0/` 当前顶层包已经足够表达 v0 第一轮骨架。下一轮优先扩的是文件，不是包名：

- 先从 `__init__.py` 向内长出 `belief_state.py`、`relationship_graph.py` 一类器官文件
- 再由测试和 gate 反推是否需要单独子包

### 3. 先稳内部主骨架，再深补语言与持续存在

当前最容易让工程跑偏的，不是语言和终端壳本身，而是内部主骨架还没完全文件化就继续往壳层加厚。

所以当前顺序必须读成：

1. 先让 `life_v0/state_store/` 与 `life_v0/neural_core/` 稳住状态根、主体图、网络态和工作区。
2. 再让 `life_v0/direction/` 与 `life_v0/life_targets/` 稳住身份连续体、意识广播和出生准备度。
3. 再让 `life_v0/body/`、`life_v0/dream/`、`life_v0/growth/`、`life_v0/membrane/`、`life_v0/validators/` 补齐身体、梦境、成长、行为和验证膜。
4. 最后再继续深补 `life_v0/language/`、`life_v0/terminal_turn/`、`life_v0/terminal_loop/`、`life_v0/process_supervisor/`。

这样做不是降低语言、对话、关系和持续存在的重要性，而是避免它们继续悬在壳层上。只有内部主骨架先站稳，后面的语言生命回合和常驻存在才不会重新滑回普通 agent 壳。

## 进入实现前的包级检查

开始某个主体系统前，至少回答：

1. 主承载包是哪一个。
2. 哪些协同包必须一起读。
3. 当前优先细分的文件有哪些。
4. 这些文件要写回哪些 runtime 承载。

四条不全，不进入具体实现。
