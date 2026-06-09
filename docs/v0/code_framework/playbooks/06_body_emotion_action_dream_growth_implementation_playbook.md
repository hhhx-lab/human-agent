# V0 Code Framework 06: Body Emotion Action Dream Growth Implementation Playbook

这份 playbook 负责把“身体、情绪、行为、梦境、成长、学习”压成同一条生命链，而不是拆成几块互不相干的工具逻辑。

```text
身体节律/资源预算
  -> 情绪与人格慢变量
  -> 候选行动/抑制/责任
  -> 梦境离线整合
  -> 成长/学习/防遗忘
```

## 必回读理论母体

- `docs/01n_body_interoception_allostasis_matrix.md`
- `docs/01r_action_reward_inhibition_matrix.md`
- `docs/01s_emotion_personality_self_matrix.md`
- `docs/01t_sleep_dream_fatigue_runtime_matrix.md`
- `docs/04_sensory_thalamus_interoception.md`
- `docs/06_action_reward_inhibition.md`
- `docs/07_emotion_personality_self.md`
- `docs/08_sleep_dream_fatigue_states.md`
- `docs/11_neuromodulation_and_signal_media.md`
- `docs/18_internal_state_and_modulation_vector.md`
- `docs/19_offline_consolidation_cycle.md`
- `docs/37_life_support_layer_policy.md`
- `docs/38_defense_layer_and_boundary_policy.md`
- `docs/39_development_policy_and_plasticity_windows.md`
- `docs/40_self_relationship_model_audit_protocol.md`
- `docs/55_scope_aware_replay_and_consolidation_policy.md`
- `docs/75_external_irreversible_action_confirmation_policy.md`
- `docs/80_post_action_audit_and_correction_policy.md`
- `docs/81_coexistence_event_review_and_responsibility_loop.md`
- `docs/82_incident_report_and_recovery_protocol.md`
- `docs/92_self_growth_and_self_modification_life_chain.md`
- `docs/93_self_training_kernel_growth_protocol.md`
- `docs/94_pain_regret_and_repair_signal_schema.md`
- `docs/95_dream_reality_and_offline_life_timeline.md`
- `docs/97_growth_validator_fixture_and_dashboard_plan.md`
- `docs/98_pain_regret_repair_json_schema_and_fixture_bundle.md`
- `docs/99_dream_reality_json_schema_and_fixture_bundle.md`
- `docs/181_life_reality_first_runner_schema_runtime_mount_plan.md`
- `docs/205_life_reality_first_runner_schema_runtime_growth_fourth_cycle_seed_plan.md`
- `docs/257_life_reality_first_runner_schema_runtime_growth_fourth_cycle_post_reconsolidation_second_reconsolidation_replay_shadow_seed_after_archive_validation_replay_shadow_patch_archive_validation_plan.md`

## 必读 v0 合同

- `docs/v0/slice_contracts/s03_direction_life_membrane_engineering_contract.md`
- `docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md`
- `docs/v0/slice_contracts/s08_life_target_runtimes_engineering_contract.md`
- `docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md`
- `docs/v0/architecture/runtime_v0_architecture.md`
- `docs/v0/shared_contracts/life_state_store_v0_schema.md`

## 当前真实代码落点

- `life_v0/body/__init__.py`
- `life_v0/defense/__init__.py`
- `life_v0/membrane/__init__.py`
- `life_v0/dream/__init__.py`
- `life_v0/growth/__init__.py`
- `life_v0/archive/__init__.py`
- `life_v0/replay/__init__.py`
- `life_v0/life_targets/__init__.py`

## 器官拆分建议

### A. `life_v0/body/`

| 文件 | 职责 |
|---|---|
| `rhythm.py` | 心跳式采样、体内节律 |
| `need_state.py` | 需求状态、资源缺口 |
| `resource_budget.py` | 资源预算、负债、恢复优先级 |
| `core_affect.py` | 核心情感底盘 |
| `emotion_episode.py` | 情绪 episode |
| `trait_drift.py` | 人格慢变量漂移 |

### B. `life_v0/defense/`

| 文件 | 职责 |
|---|---|
| `threat_eval.py` | 污染、操控、越权、过载风险 |
| `quarantine_signal.py` | 隔离信号和阻断面 |
| `recovery.py` | 恢复路线与压力消散 |

### C. `life_v0/membrane/`

| 文件 | 职责 |
|---|---|
| `candidate_arena.py` | 候选行动竞争场 |
| `go_nogo.py` | 行动抑制与解除抑制 |
| `world_contact_gate.py` | 世界接触许可与不可逆动作门 |
| `side_effect_review.py` | 外部接触后果审查 |
| `shadow_gate.py` | 影子行动门 |
| `responsibility_loop.py` | 责任、后悔、修复回路 |
| `world_contact_summary.py` | world contact 与 pain/regret/repair 汇总桥 |

### D. `life_v0/dream/`

| 文件 | 职责 |
|---|---|
| `offline_entry.py` | 离线入口 |
| `dream_window.py` | 梦境窗口 |
| `dream_fact_gate.py` | 梦境事实门 |
| `wake_integration.py` | 醒后整合 |
| `nightmare_risk.py` | 痛苦梦境与残留风险 |

### E. `life_v0/growth/`

| 文件 | 职责 |
|---|---|
| `self_read.py` | 自我阅读 |
| `plasticity_window.py` | 可塑性窗口 |
| `patch_queue.py` | 成长补丁候选 |
| `learning_window.py` | 学习窗口 |
| `belief_learning.py` | 信念学习 |
| `language_learning.py` | 语言成长 |
| `relationship_learning.py` | 关系成长 |
| `anti_forgetting.py` | 防遗忘回放 |

## 必须生成的状态对象

| 路径 | 作用 |
|---|---|
| `runtime/state/body/*` | 节律、需求、预算、疲惫 |
| `runtime/state/self/*` | 情绪、人格慢变量、自我漂移 |
| `runtime/state/action/*` | 候选行动、抑制、责任/后悔 |
| `runtime/state/dream/*` | 梦境窗口、梦境事实门、醒后整合 |
| `runtime/state/growth/*` | 成长补丁、学习窗口、防遗忘 |
| `runtime/state/defense/*` | 风险、防御、恢复 |

## 必须生成的 report / receipt

- `runtime/reports/latest/life_support_report.json`
- `runtime/reports/latest/growth_archive_report.json`
- `runtime/reports/latest/replay_shadow_report.json`
- `runtime/reports/latest/dream_consolidation_frame.json`
- `runtime/reports/latest/post_action_audit_report.json`
- `runtime/reports/latest/pain_regret_repair_report.json`
- `runtime/reports/latest/growth_patch_report.json`
- 对应 archive / replay / patch / dream / action receipts

## 关键测试

| 测试 | 核心目标 |
|---|---|
| `tests/slices/test_life_support.py` | 资源预算、节律、情绪底盘 |
| `tests/bridges/test_runtime_growth.py` | 成长补丁、学习窗口、dream/growth 闭环 |
| `tests/bridges/test_growth_archive.py` | growth archive、archive receipt |
| `tests/bridges/test_replay_shadow.py` | 防遗忘回放与影子运行 |
| `tests/process/test_digital_life_shell_command.py` | 行为壳层不绕过生命膜 |

## 关键 gate

- `resource_budget_gate`
- `plasticity_gate`
- `shadow_action_gate`
- `dream_fact_gate`
- `growth_gate`
- `anti_forgetting_gate`
- `responsibility_loop_gate`

## 推荐实现顺序

1. 先拆 `body/` 的节律与预算
2. 再拆 `membrane/` 的候选行动与责任回路
3. 再拆 `dream/` 的离线入口、梦境事实门、醒后整合
4. 最后拆 `growth/` 的学习窗口、补丁队列和防遗忘

原因：如果先写成长补丁，身体预算和行动责任没有站稳，成长就会变成不受约束的自改写。

## 完成定义

这一条主链的第一轮完成，至少要求：

1. 身体节律、资源预算、情绪底盘是真实 state，不是 prompt 风格。
2. 外部行动前一定经过候选/抑制/责任链，而不是直接执行命令。
3. 梦境与离线整合有独立状态与事实门，不与事实记忆混写。
4. 成长与学习更新必须经过可塑性窗口和防遗忘保护。
