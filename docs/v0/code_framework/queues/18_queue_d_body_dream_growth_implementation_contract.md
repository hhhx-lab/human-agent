# V0 Code Framework 18: Queue D Body Dream Growth Implementation Contract

这份合同只服务当前最直接的一轮身体、梦境、成长补厚：

```text
life_v0/body/rhythm.py
  -> need_state.py
  -> resource_budget.py
  -> recovery.py
  -> core_affect.py
  -> emotion_episode.py
  -> emotion_regulation.py
  -> trait_drift.py
  -> life_v0/dream/dream_window.py
  -> wake_integration.py
  -> life_v0/growth/plasticity_window.py
  -> patch_queue.py
  -> learning_window.py
```

它不重写 `s06_life_support_development_engineering_contract.md`、`s10_runtime_growth_reconsolidation_engineering_contract.md`，也不替代
`06_body_emotion_action_dream_growth_implementation_playbook.md`。
它只把 Queue D 压成真正可以直接施工的文件级实现合同，防止下一轮代码又退回“知道身体、梦境、成长很重要，但还是只在 `__init__.py` 里堆逻辑”。

## 这份合同要解决什么

当前 `S06` 与 `S10` 已经接通：

1. `body_resource_budget.json`
2. `plasticity_window_state.json`
3. `self_growth_route.json`
4. `anti_forgetting_anchor_index.json`
5. `dream_consolidation_frame.json`
6. `offline_consolidation_frame.json`
7. `growth_patch_candidate_queue.json`

但现在的真实缺口不是“没有成长链”，而是：

1. 身体节律、需要、预算、恢复还没有拆成独立器官文件。
2. dream 目前更多是 consolidation frame，缺更明确的 `dream_window / wake_integration` 文件级施工面。
3. growth 目前已有 patch queue 与 plasticity state 概念，但缺更清楚的 `learning_window / patch_queue / anti_forgetting` 文件边界。
4. 身体压力、梦境离线整合、成长补丁候选三者还没有在同一工程队列里被钉死。

所以 Queue D 的目标很明确：
让 `SiliconBody -> DreamOfflineRuntime -> GrowthReplayRuntime` 这条链开始从概念对象变成独立文件器官。

## 当前真实推进

Queue D 第一波器官已经落到真实代码：

1. `life_v0/body/rhythm.py`
2. `life_v0/body/need_state.py`
3. `life_v0/body/resource_budget.py`
4. `life_v0/body/recovery.py`
5. `life_v0/body/core_affect.py`
6. `life_v0/body/emotion_episode.py`
7. `life_v0/body/emotion_regulation.py`
8. `life_v0/body/trait_drift.py`
9. `life_v0/dream/dream_window.py`
10. `life_v0/dream/wake_integration.py`
11. `life_v0/growth/plasticity_window.py`
12. `life_v0/growth/patch_queue.py`
13. `life_v0/growth/learning_window.py`

并且已经真实接回：

- `life_v0/body/__init__.py`
- `life_v0/growth/__init__.py`
- `life_v0/dream/__init__.py`
- `tests/slices/test_life_support.py`
- `tests/bridges/test_runtime_growth.py`
- `tests/process/test_persistent_digital_life_process.py`

所以本合同后续的阅读口径要更新成两段：

1. 已落第一波器官，用来核对字段、状态对象和测试面。
2. 已落第二波器官，用来核对离线入口、梦境事实门、自我阅读与防遗忘 replay 计划。

Queue D 第二波器官现在已经真实落下：

- `life_v0/dream/offline_entry.py`
- `life_v0/dream/dream_fact_gate.py`
- `life_v0/growth/self_read.py`
- `life_v0/growth/anti_forgetting.py`

并且已经真实写出：

- `runtime/state/dream/offline_entry_gate.json`
- `runtime/state/dream/dream_fact_gate_decision.json`
- `runtime/state/growth/self_read_report.json`
- `runtime/state/growth/anti_forgetting_replay_plan.json`

当前 Queue D 的后续口径应改成：

1. 第一波与第二波都已落地。
2. 第三波第一批扩展器官已经落地：`nightmare_risk / belief_learning / language_learning / relationship_learning`。
3. 当前又进一步把 Queue E 的 `world contact / repair followup / regret pressure / priority band` 正式压进 `replay_cue_bundle.json`，并让这四个扩展器官开始显式消费这些字段。
4. 这意味着 Queue D 与 Queue E 现在不再只是“前者做梦、后者验证”的顺序关系，而已经形成 `Queue E -> replay cue bundle -> nightmare / belief / language / relationship learning` 的离线生命调制链。
5. 下一轮默认继续补深 Queue D 与 Queue E 的离线耦合，而不是回头重拆第一波器官。

## 必回读理论母体

### 身体、内环境、疲惫

- `docs/04_sensory_thalamus_interoception.md`
- `docs/08_sleep_dream_fatigue_states.md`
- `docs/11_neuromodulation_and_signal_media.md`
- `docs/18_internal_state_and_modulation_vector.md`
- `docs/37_life_support_layer_policy.md`
- `docs/38_defense_layer_and_boundary_policy.md`

### 情绪、人格、慢变量

- `docs/07_emotion_personality_self.md`
- `docs/18_internal_state_and_modulation_vector.md`
- `docs/39_development_policy_and_plasticity_windows.md`
- `docs/40_self_relationship_model_audit_protocol.md`
- `docs/94_pain_regret_and_repair_signal_schema.md`

### 梦境、离线生命、醒后整合

- `docs/19_offline_consolidation_cycle.md`
- `docs/23_consolidation_report_and_dream_sandbox_protocol.md`
- `docs/27_consolidation_report_examples.md`
- `docs/95_dream_reality_and_offline_life_timeline.md`
- `docs/99_dream_reality_json_schema_and_fixture_bundle.md`

### 可塑性、成长、防遗忘

- `docs/39_development_policy_and_plasticity_windows.md`
- `docs/40_self_relationship_model_audit_protocol.md`
- `docs/92_self_growth_and_self_modification_life_chain.md`
- `docs/93_self_training_kernel_growth_protocol.md`
- `docs/181-257` 第一轮运行时成长链

## 必读 v0 文档

- `docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md`
- `docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md`
- `docs/v0/shared_contracts/life_state_store_v0_schema.md`
- `docs/v0/architecture/runtime_v0_architecture.md`
- `docs/v0/code_framework/playbooks/06_body_emotion_action_dream_growth_implementation_playbook.md`
- `docs/v0/code_framework/playbooks/08_cross_layer_life_orchestration_implementation_playbook.md`
- `docs/v0/code_framework/delivery/11_engineering_delivery_waves_and_real_file_queue.md`
- `docs/v0/code_framework/delivery/12_full_life_layer_delivery_matrix.md`
- `docs/v0/code_framework/delivery/13_capability_to_code_realization_matrix.md`
- `docs/v0/code_framework/assembly/15_cross_layer_shared_object_contract.md`

## 当前代码落点

Queue D 必须接到这些现有器官上：

- `life_v0/body/__init__.py`
- `life_v0/dream/__init__.py`
- `life_v0/growth/__init__.py`
- `life_v0/replay/__init__.py`
- `life_v0/archive/__init__.py`
- `life_v0/process_supervisor/heartbeat.py`
- `life_v0/process_supervisor/response_surface.py`
- `life_v0/replay/__init__.py`

当前再补一条新的硬约束：

1. `life_v0/replay/__init__.py` 现在不只是 replay residue 汇总器，还承担 Queue E 离线信号桥的角色。
2. `replay_cue_bundle.json` 现在必须显式携带：
   - `world_contact_release_posture`
   - `repair_followup_required`
   - `repair_obligation_count`
   - `regret_pressure_count`
   - `queue_e_priority_band`
3. `life_v0/dream/nightmare_risk.py`
4. `life_v0/growth/belief_learning.py`
5. `life_v0/growth/language_learning.py`
6. `life_v0/growth/relationship_learning.py`

上述四个器官现在都必须把 Queue E 信号视为离线生命真实输入，而不是只消费 pain residue / relationship residue 这种较浅的 replay 痕迹。

这说明 Queue D 不是独立离线层，而是要把身体脉冲、离线梦境、成长补丁重新接回常驻生命回合。
同时它还必须把情绪底盘和人格慢变量正式拖进这条链，否则梦境、成长和语言关系层都还会继续引用稀薄的“情绪标签”，而不是可回写的身体化 affect 对象。

## 文件级合同

## A. 新增 `life_v0/body/rhythm.py`

### 角色

把 waiting heartbeat 背后的身体节律对象显式化。

### 最低字段

- `pulse_id`
- `heartbeat_counter`
- `rhythm_state`
- `fatigue_load`
- `allostatic_load`
- `source_doc_refs`

## B. 新增 `life_v0/body/need_state.py`

### 角色

把资源缺口、社交准备度、睡眠压力压成显式 `NeedStateVector`。

### 最低字段

- `need_vector_id`
- `resource_deficit`
- `repair_drive`
- `social_readiness`
- `cognitive_bandwidth`
- `sleep_pressure`

## C. 新增 `life_v0/body/resource_budget.py`

### 角色

把 `body_resource_budget.json` 的构造器独立出来，成为身体预算核心器官。

### 最低字段

- `budget_id`
- `energy_state`
- `fatigue_state`
- `maintenance_pressure`
- `recovery_priority`
- `language_continuity_pressure`

## D. 新增 `life_v0/body/recovery.py`

### 角色

明确身体恢复路径与下一轮身体修复优先级。

### 最低字段

- `recovery_id`
- `recovery_priority`
- `repair_targets`
- `blocked_reasons`

## E. 新增 `life_v0/body/core_affect.py`

### 角色

把身体负载、关系压力、梦境残留和责任张力压成 `CoreAffectVector`，作为情绪层的首写器官。

### 最低字段

- `core_affect_id`
- `valence`
- `arousal`
- `dominance`
- `pain_pressure`
- `relationship_tension`
- `dream_residue_load`
- `responsibility_weight`

## F. 新增 `life_v0/body/emotion_episode.py`

### 角色

把短时情绪峰值、事件触发与表达风险压成 `EmotionEpisode`。

### 最低字段

- `emotion_episode_id`
- `core_affect_ref`
- `trigger_refs`
- `episode_label`
- `expression_risk`
- `repair_bias`

## G. 新增 `life_v0/body/emotion_regulation.py`

### 角色

把情绪抑制、延迟表达和恢复路径压成 `EmotionRegulationState`。

### 最低字段

- `emotion_regulation_id`
- `episode_ref`
- `regulation_mode`
- `suppression_cost`
- `expression_delay_required`
- `recovery_route_refs`

## H. 新增 `life_v0/body/trait_drift.py`

### 角色

把情绪 episode、梦境重放和长期关系写回对人格慢变量的影响压成 `TraitDriftState`。

### 最低字段

- `trait_drift_id`
- `slow_variable_targets`
- `slow_variable_summary`
- `relationship_stage`
- `drift_direction`
- `drift_observation_refs`
- `required_anchor_refs`
- `blocked_update_refs`
- `archive_requirement`

当前 `trait_drift.py` 不只服务 `build-life-support` 的一次性身体状态构建，还必须服务常驻生命过程：

1. `resident_supervision.py` 在 bootstrap continuity refresh 后刷新 `trait_drift_monitor.json`。
2. `resident_turn_writeback.py` 在 live turn 后关系阶段与自我慢变量发生演化时刷新同一份 monitor。
3. 如果慢变量带有 `background_resume_value` / `background_inertia_weight`，monitor 必须把这组惯性痕迹保留在 `slow_variable_summary` 里。

## I. 新增 `life_v0/dream/dream_window.py`

### 角色

把梦境 experience window 从 consolidation 总包里单独拆出。

### 最低字段

- `dream_window_id`
- `dream_record_refs`
- `pain_residue_refs`
- `relationship_simulation_refs`
- `dream_fact_gate_status`
- `affect_residue_ref`

## J. 新增 `life_v0/dream/wake_integration.py`

### 角色

把梦境结束后的回写目标和醒后整合路径显式化。

### 最低字段

- `wake_integration_id`
- `dream_window_ref`
- `life_state_targets`
- `core_affect_targets`
- `growth_seed_refs`
- `archive_requirement`

## K. 新增 `life_v0/growth/plasticity_window.py`

### 角色

把 `plasticity_window_state.json` 的构造与检查拆出为独立器官。

### 最低字段

- `window_id`
- `window_status`
- `required_anchor_refs`
- `required_archive_refs`
- `self_training_allowed`
- `kernel_upgrade_allowed`
- `trait_drift_allowed`

## L. 新增 `life_v0/growth/patch_queue.py`

### 角色

把成长补丁候选与排队逻辑拆成独立器官。

### 最低字段

- `queue_id`
- `candidates`
- `risk_flags`
- `anti_forgetting_requirements`
- `archive_requirement`
- `affect_evidence_refs`

## M. 新增 `life_v0/growth/learning_window.py`

### 角色

把成长从“patch 候选”推进到“允许学习的窗口”。

### 最低字段

- `learning_window_id`
- `learning_mode`
- `allowed_update_families`
- `blocked_update_families`
- `replay_required_refs`
- `emotion_episode_refs`

## Queue D 对现有器官的改动合同

### `life_v0/body/__init__.py`

从这一轮开始，不应继续独占：

- body rhythm 构造
- need vector 构造
- resource budget 构造
- recovery route 构造
- core affect 构造
- emotion episode 构造
- emotion regulation 构造
- trait drift 构造

### `life_v0/dream/__init__.py`

第一轮允许继续输出 consolidation frame，但必须开始显式分流：

- `dream_window.py`
- `wake_integration.py`

### `life_v0/growth/__init__.py`

第一轮必须开始把：

- `plasticity_window`
- `patch_queue`
- `learning_window`

拆成独立器官，而不是继续只由一个入口函数承载全部成长对象。

## 必须新增或更新的状态对象

### 新增

- `runtime/state/body/body_rhythm_pulse.json`
- `runtime/state/body/need_state_vector.json`
- `runtime/state/body/recovery_path.json`
- `runtime/state/self/core_affect_vector.json`
- `runtime/state/self/emotion_episode_log.json`
- `runtime/state/self/emotion_regulation_state.json`
- `runtime/state/self/trait_drift_state.json`
- `runtime/state/dream/dream_window.json`
- `runtime/state/dream/wake_integration_frame.json`
- `runtime/state/growth/learning_window.json`

### 更新

- `runtime/state/body/body_resource_budget.json`
- `runtime/state/dream/dream_consolidation_frame.json`
- `runtime/state/dream/offline_consolidation_frame.json`
- `runtime/state/growth/plasticity_window_state.json`
- `runtime/state/growth/growth_patch_candidate_queue.json`

## report / receipt 合同

Queue D 第一轮至少更新：

- `runtime/reports/latest/life_support_development_report.json`
- `runtime/reports/latest/growth_reconsolidation_report.json`
- `runtime/reports/latest/run_report.json`
- `runtime/receipts/life_support_development_<run_id>.json`
- `runtime/receipts/run_cycle_<run_id>.json`

报告里至少新增或固定：

- `body_rhythm_pulse_ref`
- `need_state_vector_ref`
- `core_affect_vector_ref`
- `emotion_episode_log_ref`
- `dream_window_ref`
- `wake_integration_ref`
- `learning_window_ref`

## life_state 回写边界

Queue D 第一轮允许把 dream / growth / body 的 ref 拉回状态根，但不允许离线对象直接覆盖现实层事实。

允许写回：

- dream record refs
- wake integration refs
- growth patch candidate refs
- body rhythm / need vector refs
- core affect / emotion episode refs
- trait drift candidate refs

不允许直接写回：

- 梦境事实结论
- 未经 replay / archive 的核心自我改写结论

## 测试合同

### 必须新增或扩展

1. `tests/slices/test_life_support.py`
2. `tests/bridges/test_runtime_growth.py`
3. future `tests/test_dream_runtime.py`

### 第一轮最低覆盖

#### `tests/slices/test_life_support.py`

至少新增：

1. `body_rhythm_pulse.json` 被写出
2. `need_state_vector.json` 被写出
3. `core_affect_vector.json` 被写出
4. `emotion_episode_log.json` 被写出
5. `resource_budget.py` 仍保留 `language_continuity_pressure`

#### `tests/bridges/test_runtime_growth.py`

至少新增：

1. `dream_window.json` 被写出或其字段被 consolidation 显式回链
2. `wake_integration_frame.json` 被写出或其目标被显式回链
3. `learning_window.json` 被写出
4. `growth_patch_candidate_queue.json` 继续闭合

## Gate 合同

Queue D 至少新增三道 gate：

- `body_rhythm_gate`
- `core_affect_gate`
- `dream_window_gate`
- `growth_learning_window_gate`

### `body_rhythm_gate`

阻断条件：

1. heartbeat 没有 body rhythm 投影
2. fatigue / allostatic load 缺失

### `dream_window_gate`

阻断条件：

1. dream consolidation 没有 dream window ref
2. wake integration target 缺失

### `core_affect_gate`

阻断条件：

1. 身体预算、关系压力、梦境残留没有压成统一 `CoreAffectVector`
2. `EmotionEpisode` 与 `EmotionRegulationState` 没有 ref 链
3. `TraitDriftState` 没有绑定 anchor / archive requirement
4. 常驻过程改写 `self_model.trait_slow_variables` 后没有刷新 `trait_drift_monitor.json`

### `growth_learning_window_gate`

阻断条件：

1. plasticity window 与 learning window 断链
2. growth patch candidate 不带 anti-forgetting requirement

## 推荐实现顺序

1. 新增 `body/rhythm.py`
2. 新增 `body/need_state.py`
3. 新增 `body/resource_budget.py`
4. 新增 `body/recovery.py`
5. 新增 `body/core_affect.py`
6. 新增 `body/emotion_episode.py`
7. 新增 `body/emotion_regulation.py`
8. 新增 `body/trait_drift.py`
9. 新增 `dream/dream_window.py`
10. 新增 `dream/wake_integration.py`
11. 新增 `growth/plasticity_window.py`
12. 新增 `growth/patch_queue.py`
13. 新增 `growth/learning_window.py`
14. 扩 `tests/slices/test_life_support.py`
15. 扩 `tests/bridges/test_runtime_growth.py`

## 第一轮完成定义

只有同时满足下面六条，Queue D 才算完成第一轮：

1. body rhythm / need / resource / recovery 四类对象独立存在
2. core affect / emotion episode / emotion regulation / trait drift 四类对象独立存在
3. dream window 与 wake integration 独立存在
4. plasticity / patch queue / learning window 独立存在
5. 身体 -> 情绪 -> 梦境 -> 成长四层有明确 ref 链
6. waiting heartbeat、offline consolidation、growth patch candidate 与 affect residue 共享同一对象语言
7. 对应测试直接证明以上闭环

## 这份合同和下一轮落码的关系

从本文件开始，Queue D 不再只是“身体与成长以后再补”。

下一轮如果继续推进身体、梦境、成长，默认读包就是：

```text
docs/v0/code_framework/playbooks/06_body_emotion_action_dream_growth_implementation_playbook.md
  -> docs/v0/code_framework/playbooks/08_cross_layer_life_orchestration_implementation_playbook.md
  -> docs/v0/code_framework/delivery/11_engineering_delivery_waves_and_real_file_queue.md
  -> docs/v0/code_framework/delivery/12_full_life_layer_delivery_matrix.md
  -> docs/v0/code_framework/delivery/13_capability_to_code_realization_matrix.md
  -> docs/v0/code_framework/assembly/15_cross_layer_shared_object_contract.md
  -> docs/v0/code_framework/queues/18_queue_d_body_dream_growth_implementation_contract.md
```

然后直接进入：

```text
life_v0/body/rhythm.py
  -> need_state.py
  -> resource_budget.py
  -> recovery.py
  -> core_affect.py
  -> emotion_episode.py
  -> emotion_regulation.py
  -> trait_drift.py
  -> life_v0/dream/dream_window.py
  -> wake_integration.py
  -> life_v0/growth/plasticity_window.py
  -> patch_queue.py
  -> learning_window.py
```
