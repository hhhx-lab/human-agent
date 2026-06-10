# Packet B 世界观察与外周归一化施工脚手

这份脚手页只服务一个前沿包：

```text
life_v0/membrane/world_observation.py
life_v0/membrane/periphery_normalizer.py
```

它的职责不是重讲 Queue E，而是把 `Packet B` 压成真正能直接动代码、动测试、动 runtime 的施工单。

## 为什么先做这一包

当前预测五件套已经落盘：

- `runtime/state/signal/signal_media_runtime.json`
- `runtime/state/prediction/belief_state_frame.json`
- `runtime/state/prediction/prediction_error_field.json`
- `runtime/state/prediction/active_sampling_plan.json`
- `runtime/state/prediction/prediction_workspace_frame.json`

但生命膜还缺一个真实的“看哪里、怎么筛”的器官层。

如果这一层不落：

1. `active_sampling_plan.json` 只是建议，不是世界观察路线。
2. `prediction_error_field.json` 只能停在内部裂口，不会变成外周权重。
3. `responsibility_loop.py` 和 `world_contact_summary.py` 仍然更像 action 末端摘要，而不是带着 observation 路径工作的生命膜。

## 必读材料

### `00-257` 母体

- `docs/04_sensory_thalamus_interoception.md`
- `docs/22_state_transition_and_threshold_model.md`
- `docs/64_real_runtime_observation_ingestion_policy.md`
- `docs/68_runtime_observation_report_mock_and_redaction_fixture.md`
- `docs/72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md`

### v0 合同

- `docs/v0/code_scaffolds/03_frontier_module_build_packets.md`
- `docs/v0/implementation_architecture/code_organs/03_predictive_signal_memory_gate_integration_wave_contract.md`
- `docs/v0/slice_contracts/s03_direction_life_membrane_engineering_contract.md`
- `docs/v0/slice_contracts/s05_validation_membrane_observation_engineering_contract.md`
- `docs/v0/engineering_depth/05_prediction_membrane_action_engineering.md`

## 文件落点

| 文件 | 本轮职责 |
|---|---|
| `life_v0/membrane/world_observation.py` | 把主动采样计划压成真实 observation route |
| `life_v0/membrane/periphery_normalizer.py` | 把信念帧、误差场、调质向量压成外周升权/降权/延迟轨迹 |
| `life_v0/membrane/responsibility_loop.py` | 显式吸收 observation / normalization refs |
| `life_v0/membrane/world_contact_summary.py` | 显式带 observation route 与 normalization trace 摘要 |
| `life_v0/membrane/__init__.py` | 在 S03 真实写出 observation state，并把它们接进 manifest/report/receipt |
| `life_v0/validators/observation_validator.py` | 在 S05 吃到这批 observation route refs |
| `life_v0/validators/__init__.py` | 把 observation intake 从抽象壳升级成能回链 Packet B state 的 intake |

## 输入 ref

这一包默认只吃下面这些固定 ref，不自造平行输入：

- `runtime/state/prediction/belief_state_frame.json`
- `runtime/state/prediction/prediction_error_field.json`
- `runtime/state/prediction/active_sampling_plan.json`
- `runtime/state/prediction/prediction_workspace_frame.json`
- `runtime/state/signal/signal_media_runtime.json`
- `runtime/state/body/need_state_vector.json`
- `runtime/state/body/core_affect_vector.json`

## 输出 ref

本轮固定写出：

- `runtime/state/observation/world_observation_route.json`
- `runtime/state/observation/periphery_normalization_trace.json`

并要求至少继续投影到：

- `runtime/state/membrane/world_contact_summary.json`
- `runtime/state/action/responsibility_loop_state.json`
- `runtime/state/observation/runtime_observation_intake.json`

## 施工算法

### 1. `world_observation.py`

最小算法：

1. 读取 `active_sampling_plan.selected_route`
2. 合并：
   - `expected_observation_refs`
   - `scope_refs`
   - `prediction_workspace_frame.workspace_contents.language_continuity_focus`
3. 去重形成 `observation_targets`
4. 依据：
   - `unexpected_uncertainty`
   - `relationship_pressure`
   - `selected_route`
   给每个 target 打 `priority` 与 `reason`
5. 固定写回：
   - `active_sampling_plan_ref`
   - `belief_state_ref`
   - `prediction_error_ref`
   - `prediction_workspace_ref`
   - `signal_media_ref`

### 2. `periphery_normalizer.py`

最小算法：

1. 读取 `world_observation_route.prioritized_channels`
2. 用：
   - `fatigue_load`
   - `relationship_pressure`
   - `error_focus_ids`
   判断每个 channel 是：
   - `promote`
   - `defer`
   - `suppress`
3. 固定写出：
   - `normalized_channels`
   - `promoted_channels`
   - `suppressed_channels`
   - `deferred_channels`
   - `body_pressure`
4. 明确写明 downstream write targets，不能只写结果不写去向

## 跨层接线

### 接回 S03

- `responsibility_loop.py`
  - 新增 `belief_state_ref`
  - 新增 `prediction_error_ref`
  - 新增 `signal_media_ref`
  - 新增 `world_observation_route_ref`
  - 新增 `periphery_normalization_ref`

- `world_contact_summary.py`
  - 新增 `world_observation_route_ref`
  - 新增 `periphery_normalization_ref`
  - 摘出 `observation_route_mode`
  - 摘出 `deferred_channel_count`

### 接回 S05

- `runtime_observation_intake.json` 不能再只是抽象 observation 壳
- 必须带上：
  - `runtime/state/observation/world_observation_route.json`
  - `runtime/state/observation/periphery_normalization_trace.json`

## 测试面

这一包最少要跑：

1. `python3 -m unittest tests.slices.test_life_membrane -v`
2. `python3 -m unittest tests.slices.test_validation_membrane -v`
3. `python3 -m unittest tests.contracts.test_v0_contracts -v`

## 完成定义

只有同时满足下面六条，这一包才算真正落地：

1. `world_observation.py` 与 `periphery_normalizer.py` 成为真实文件，而不是只留在合同里。
2. S03 运行后，`runtime/state/observation/` 真实出现两份新 state。
3. `responsibility_loop_state.json` 与 `world_contact_summary.json` 显式带 observation refs。
4. S05 运行后，`runtime_observation_intake.json` 与 `observation_truth_review.json` 能回链这两份新 state。
5. `life_membrane_report.json` / manifest / receipt 三处都带 observation refs。
6. 相关测试闭合，不出现“文件写了但 gate 没认”的断层。
