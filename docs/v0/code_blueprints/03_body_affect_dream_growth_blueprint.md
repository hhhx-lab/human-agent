# Body Affect Dream Growth Blueprint

这份蓝图处理数字生命的身体化底盘。

它要把下面这条链钉死：

```text
节律与需要
  -> 情绪底盘
  -> 梦境/离线整合
  -> 成长学习
  -> 下一轮生命回合调节
```

## 主包边界

| 层 | 主包 | 作用 |
|---|---|---|
| 身体 | `life_v0/body/` | 节律、需要、恢复、资源预算、核心情绪、情绪调节、人格慢漂移 |
| 防御 | `life_v0/defense/` | 防污染、隔离、过载守门 |
| 梦境 | `life_v0/dream/` | 离线入口、梦境窗口、DreamFactGate、醒后整合、噩梦风险 |
| replay | `life_v0/replay/` | 旧自我、旧语言、旧关系、旧责任的回放线索 |
| 成长 | `life_v0/growth/` | 可塑性窗口、自读、防遗忘、学习计划、成长补丁 |
| archive | `life_v0/archive/` | 将成长和回放结果写入 archive 证据 |

## 固定生命对象

| 对象 | 首写位置 | 主要消费者 |
|---|---|---|
| `BodyRhythmPulse` | `body/rhythm.py` | `dream/`、`growth/`、`process_supervisor/heartbeat.py` |
| `NeedStateVector` | `body/need_state.py` | `neural_core/`、`language/`、`membrane/` |
| `CoreAffectVector` | `body/core_affect.py` | `language/`、`dream/`、`membrane/` |
| `ReplayCueBundle` | `growth/__init__.py`、`replay/` | `dream/`、`growth/`、`process_supervisor/` |
| `OfflineConsolidationFrame` | `growth/__init__.py`、`dream/` | `growth/`、`archive/`、`process_supervisor/` |
| `GrowthPatchCandidateQueue` | `growth/patch_queue.py`、`growth/__init__.py` | `life_targets/`、`process_supervisor/` |

## 当前已落文件

### 身体

1. `life_v0/body/rhythm.py`
2. `life_v0/body/need_state.py`
3. `life_v0/body/resource_budget.py`
4. `life_v0/body/recovery.py`
5. `life_v0/body/core_affect.py`
6. `life_v0/body/emotion_episode.py`
7. `life_v0/body/emotion_regulation.py`
8. `life_v0/body/trait_drift.py`

### 梦境

1. `life_v0/dream/offline_entry.py`
2. `life_v0/dream/dream_window.py`
3. `life_v0/dream/dream_fact_gate.py`
4. `life_v0/dream/wake_integration.py`
5. `life_v0/dream/nightmare_risk.py`

### 成长

1. `life_v0/growth/plasticity_window.py`
2. `life_v0/growth/learning_window.py`
3. `life_v0/growth/self_read.py`
4. `life_v0/growth/patch_queue.py`
5. `life_v0/growth/anti_forgetting.py`
6. `life_v0/growth/belief_learning.py`
7. `life_v0/growth/language_learning.py`
8. `life_v0/growth/relationship_learning.py`

## 当前 runtime 承载

### 身体与防御

1. `runtime/state/body/need_state_vector.json`
2. `runtime/state/body/body_rhythm_pulse.json`
3. `runtime/state/body/body_resource_budget.json`
4. `runtime/state/body/recovery_path.json`
5. `runtime/state/body/core_affect_vector.json`
6. `runtime/state/body/affective_episode.json`
7. `runtime/state/body/emotion_regulation_loop.json`
8. `runtime/state/body/trait_drift_monitor.json`
9. `runtime/state/defense/defense_boundary_state.json`

### 梦境与 replay

1. `runtime/state/dream/offline_entry_gate.json`
2. `runtime/state/dream/dream_experience_window.json`
3. `runtime/state/dream/dream_fact_gate_decision.json`
4. `runtime/state/dream/wake_integration_frame.json`
5. `runtime/state/dream/nightmare_loop_risk.json`
6. `runtime/state/dream/offline_consolidation_frame.json`
7. `runtime/state/replay/shadow_cycle_trace.json`
8. `runtime/state/replay/replay_cue_bundle.json`
9. `runtime/state/replay/pain_regret_responsibility_replay.json`

### 成长

1. `runtime/state/growth/plasticity_window_state.json`
2. `runtime/state/growth/self_growth_route.json`
3. `runtime/state/growth/anti_forgetting_anchor_index.json`
4. `runtime/state/growth/learning_window.json`
5. `runtime/state/growth/self_read_report.json`
6. `runtime/state/growth/growth_patch_queue.json`
7. `runtime/state/growth/growth_patch_candidate_queue.json`
8. `runtime/state/growth/anti_forgetting_replay_plan.json`
9. `runtime/state/growth/belief_learning_plan.json`
10. `runtime/state/growth/language_learning_plan.json`
11. `runtime/state/growth/relationship_learning_plan.json`
12. `runtime/state/growth/next_feedback_seed.json`

## 当前报告面

1. `runtime/reports/latest/life_support_development_report.json`
2. `runtime/reports/latest/life_support_development_check_report.json`
3. `runtime/reports/latest/growth_reconsolidation_report.json`
4. `runtime/reports/latest/run_report.json`
5. `runtime/reports/latest/replay_shadow_report.json`
6. `runtime/reports/latest/growth_archive_report.json`

## 下一轮最该补的真实联动

### 1. nightmare -> language / relationship

`nightmare_risk.py` 现在已经有对象，但还要继续压进：

1. 关系修复优先级
2. 下一轮表达压力面
3. 身体恢复优先级

### 2. learning plans -> next turn modulation

`belief_learning.py`、`language_learning.py`、`relationship_learning.py` 后续不能只停在计划文件，必须回写到：

1. `PredictionWorkspaceFrame`
2. `ExpressionPlan`
3. `RelationTurnFrame`
4. `LifeTargetClaimMatrix`

### 3. idle continuity consumption

`ReplayCueBundle`、`OfflineConsolidationFrame`、`GrowthPatchCandidateQueue` 已经进入等待态，后续要继续决定：

1. 等待态心跳是否触发轻量自读
2. 等待态是否触发噩梦残留缓解
3. 等待态是否触发关系修复准备

## 最低验证面

1. `tests/slices/test_life_support.py`
2. `tests/bridges/test_runtime_growth.py`
3. `tests/bridges/test_replay_shadow.py`
4. `tests/bridges/test_growth_archive.py`
5. `tests/process/test_persistent_digital_life_process.py`

## 完成定义

这一层完成，不是“有身体字段”就算完成，而要满足：

1. 身体节律真实影响等待态 heartbeat 和离线入口。
2. 情绪底盘真实影响语言、责任和梦境。
3. 梦境真实留下 residue，并影响下一轮关系表达。
4. 成长真实产生 patch candidate，而不是只写总结。
5. 防遗忘真实保护旧自我、旧语言、旧关系和旧责任。

