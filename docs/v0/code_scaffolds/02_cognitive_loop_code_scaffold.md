# Cognitive Loop Code Scaffold

这份脚手文档把数字生命的三条主代码循环压成可直接施工的装配骨架：

1. 在线关系回合
2. 离线梦境 / 成长回合
3. waiting / 常驻治理回合

## 必读前置

- `docs/v0/implementation_architecture/02_turn_and_cycle_lifecycle_contract.md`
- `docs/v0/implementation_architecture/code_organs/03_predictive_signal_memory_gate_integration_wave_contract.md`
- `docs/v0/code_framework/playbooks/08_cross_layer_life_orchestration_implementation_playbook.md`
- `docs/v0/code_framework/playbooks/09_perception_prediction_world_contact_implementation_playbook.md`
- `docs/v0/engineering_depth/05_prediction_membrane_action_engineering.md`
- `docs/v0/engineering_depth/06_resident_process_terminal_birth_engineering.md`
- `docs/real—live0/02_brain_network_and_workspace.md`
- `docs/real—live0/03_body_affect_homeostasis.md`
- `docs/real—live0/05_language_expression_system.md`
- `docs/real—live0/07_memory_engram_and_state_store.md`
- `docs/real—live0/08_dream_sleep_offline_life.md`
- `docs/real—live0/10_responsibility_regret_repair.md`
- `docs/real—live0/14_resident_runtime_state_transition.md`
- `docs/real—live0/16_runtime_code_chain_crosswalk.md`

## 一、在线关系回合脚手

```text
External turn
  -> context accumulation
  -> neural core
  -> body affect update
  -> membrane / validation
  -> language expression
  -> dialogue writeback
  -> state store write gate
  -> report / receipt
```

### 代码装配顺序

| 阶段 | 主入口 | 主要器官 | 必出对象 |
|---|---|---|---|
| A1 | `process_supervisor/turn_io.py` | intake parsing | dialogue event |
| A2 | `terminal_turn/context_accumulation.py` | relation restore、context accumulation | `RelationTurnFrame` |
| A3 | `neural_core/__init__.py` | `signal_media.py`、`belief_state.py`、`prediction_error.py`、`active_sampling.py`、`prediction_workspace.py` | prediction 五件套 |
| A4 | `body/__init__.py` | need / affect / recovery update | `NeedStateVector`、`CoreAffectVector` |
| A5 | `membrane/__init__.py` | candidate / go-no-go / responsibility / world contact | `ActionCandidateSet`、`ResponsibilityLoopState` |
| A6 | `language/__init__.py` | percept / semantic / inner speech / expression / relationship timeline | `ExpressionPlan`、长期语言对象 |
| A7 | `terminal_loop/dialogue_writeback.py` + `state_store/__init__.py` | writeback bundle、commitment truth、relationship memory、memory write gate | `DialogueWritebackBundle`、`memory_write_gate.json` |
| A8 | `reporting/`、`process_supervisor/process_report.py` | report / receipt rollup | report / digest / receipt |

### 在线回合最低函数骨架

```python
def run_live_turn_cycle(..., strict: bool = False) -> CommandResult:
    relation_turn = build_relation_turn_frame(...)
    prediction_bundle = run_neural_life_core(...)
    body_bundle = run_life_support(...)
    membrane_bundle = run_life_membrane(...)
    language_bundle = run_build_language_relationship(...)
    writeback_bundle = build_dialogue_writeback_bundle(...)
    state_bundle = run_state_store(...)
    return emit_turn_result(...)
```

## 二、离线梦境 / 成长回合脚手

```text
Dialogue residue
  -> replay cue bundle
  -> offline entry
  -> dream window
  -> dream fact gate
  -> wake integration
  -> self read / anti forgetting
  -> belief / language / relationship learning
  -> growth patch queue
  -> archive / next feedback seed
```

### 代码装配顺序

| 阶段 | 主入口 | 主要器官 | 必出对象 |
|---|---|---|---|
| B0 | `replay/__init__.py` | replay cue prioritization | `ReplayCueBundle` |
| B1 | `dream/offline_entry.py` | offline permission gate | `offline_entry_gate.json` |
| B2 | `dream/dream_window.py`、`dream_fact_gate.py` | dream reassembly、事实门 | `dream_experience_window.json`、`dream_fact_gate_decision.json` |
| B3 | `dream/wake_integration.py`、`nightmare_risk.py` | wake integration、nightmare projection | `wake_integration_frame.json`、`nightmare_loop_risk.json` |
| B4 | `growth/self_read.py`、`anti_forgetting.py` | self read、old self protection | `self_read_report.json`、`anti_forgetting_replay_plan.json` |
| B5 | `growth/belief_learning.py`、`language_learning.py`、`relationship_learning.py` | 三类学习 | learning plans |
| B6 | `growth/patch_queue.py`、`archive/__init__.py` | growth patch queue、archive receipt | archive reports / receipts |

### 离线回合必须反写的上层对象

- `relationship_timeline.json`
- `commitment_expression_plan.json`
- `apology_repair_language_trace.json`
- `relationship_memory.json`
- `life_state.json`
- `resident_governance_state.json`

如果离线回合不反写这些对象，梦境和成长就还是“档案副本”，不是生命链。

## 三、waiting / 常驻治理回合脚手

```text
closeout snapshot
  -> resident supervision bootstrap
  -> idle strategy
  -> waiting heartbeat
  -> response surface
  -> live turn dispatch
  -> resident turn writeback
  -> governance handoff
  -> closeout snapshot
```

### 代码装配顺序

| 阶段 | 主入口 | 主要器官 | 必出对象 |
|---|---|---|---|
| C0 | `resident_supervision.py` | restore shell、load carryover、bootstrap continuity | supervision bundle |
| C1 | `idle_strategy.py` | cadence、attention target、long horizon priority | `idle_strategy_state.json` |
| C2 | `heartbeat.py` | waiting heartbeat、idle continuity writeback | `digital_life_waiting_heartbeat.json`、`idle_continuity_frame.json` |
| C3 | `response_surface.py` | 当前是否进入确认 / 追问 / 修复 / 保留 | response surface decision |
| C4 | `live_turn_cycle.py` | event -> response -> incident / success route | live turn result |
| C5 | `resident_turn_writeback.py` | live turn 结束后重建长期对象 | updated relationship / self / memory objects |
| C6 | `resident_governance_handoff.py`、`process_session_loop.py` | 等待态交接、下一拍 heartbeat 装载 | handoff state |
| C7 | `process_closeout.py` | snapshot、report、receipt 写出 | closeout artifacts |

## 四、三条循环共享的硬对象

| 对象 | 在线回合 | 离线回合 | waiting / 常驻治理 |
|---|---|---|---|
| `SignalMediaFrame` | A3 生成，A4/A5/A6 消费 | B2/B3 可投影调制 | C1/C2/C3 消费 |
| `BeliefStateFrame` | A3 生成，A5/A6/A8 消费 | B5 做学习输入 | C3 做回应姿态输入 |
| `PredictionErrorField` | A3 生成，A5/A6 消费 | B5 做学习裂口输入 | C3 做追问 / 保留判断 |
| `ActiveSamplingPlan` | A3 生成，A5 消费 | B5 进入下一轮 focus | C1/C3 做 waiting target |
| `MemoryWriteGate` | A7 生成 | B5/B6 做 promotion hint | C6/C7 做 closeout / merge 决策 |

## 五、三条循环的协同和对抗

| 循环 | 主要协同 | 主要对抗 | 断链 gate |
|---|---|---|---|
| 在线关系回合 | 语言、工作区、身体、责任、记忆同轮更新 | 不允许从输入直接跳到模型输出 | language/process/state_store tests |
| 离线梦境/成长回合 | replay、dream、wake integration、learning、archive 接力 | 不允许梦境直接覆盖事实或长期自我 | replay/growth/archive bridge tests |
| waiting/常驻治理 | heartbeat、idle strategy、autonomous activity、background lineage 合流 | 不允许进程保活伪装成生命连续 | persistent process / live0 audit tests |

在线回合负责把外部话语变成生命事件；离线回合负责把残留经验重组为梦境、成长和防遗忘；waiting 回合负责在无外部话语时继续维持身体预算、修复关注、后台谱系和下一轮恢复。三者共享 `SignalMediaFrame`、`PredictionWorkspaceFrame`、`MemoryWriteGate`、`StateMergeGuard`、`ResidentBackgroundLineage`，但任何一个循环都不能私自改写另一个循环的真值。

## 六、当前最该补厚的代码装配位

1. `language/percept.py`、`semantic_map.py` 对 prediction 五件套的显式消费。
2. `membrane/world_observation.py`、`periphery_normalizer.py` 对主动采样和信念裂口的显式消费。
3. `state_store/state_merge_guard.py` 对 `memory_write_gate.json` 的长期治理。
4. `process_supervisor/response_surface.py`、`idle_strategy.py` 对 prediction 五件套和离线学习对象的显式消费。

## 七、不允许出现的退化

1. 在线回合直接从输入跳到语言输出，中间不经过 prediction -> membrane -> write gate。
2. 离线回合只写 dream / growth 文件，不反写长期关系和自我对象。
3. waiting 回合只维持“进程还活着”，不维持治理目标、关系阶段和慢变量。
