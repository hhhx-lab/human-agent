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
- `docs/09_language_symbolic_top_layer.md`
- `docs/11_neuromodulation_and_signal_media.md`
- `docs/22_state_transition_and_threshold_model.md`
- `docs/64_real_runtime_observation_ingestion_policy.md`
- `docs/68_runtime_observation_report_mock_and_redaction_fixture.md`
- `docs/72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md`
- `docs/75_external_irreversible_action_confirmation_policy.md`
- `docs/01v_prediction_active_inference_runtime_matrix.md`

### `real—live0` 机制档案

- `docs/real—live0/09_prediction_perception_world_contact.md`
- `docs/real—live0/11_life_membrane_validation.md`
- `docs/real—live0/12_neuromodulation_signal_media.md`
- `docs/real—live0/16_runtime_code_chain_crosswalk.md`

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

## 对象字段最小定义

| 对象 | 必须字段 | 含义 |
|---|---|---|
| `WorldObservationRoute` | `selected_route`、`observation_targets`、`expected_observation_refs`、`priority_reasons`、`source_prediction_refs` | 把主动采样从内部计划变成世界观察路线 |
| `PeripheryNormalizationTrace` | `normalized_channels`、`promoted_channels`、`deferred_channels`、`suppressed_channels`、`body_pressure`、`relationship_pressure` | 把外周输入按身体/关系/预测压力升权、降权或延迟 |
| `RuntimeObservationIntake` | `world_observation_route_ref`、`periphery_normalization_ref`、`truth_gate_ref` | 让 S05 验证膜能读到 Packet B 状态 |
| `WorldContactSummary` | `world_observation_route_ref`、`periphery_normalization_ref`、`release_posture` | 世界接触总结必须带观察路径和外周归一化证据 |

这些对象不能成为工具路由。它们只回答：当前生命需要观察什么、哪些外周信号可信、哪些信号要延迟、哪些观察会进入验证和责任链。

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

## 协同与对抗

| 关系 | 协同 | 对抗 |
|---|---|---|
| 预测 vs 观察 | `ActiveSamplingPlan` 生成观察目标，Packet B 落成 route | 观察结果不能直接变成事实，必须过 `ObservationTruthGate` |
| 内感受 vs 外周 | 疲惫、痛苦、关系压力改变 channel priority | 高 arousal 不能让外周噪声升格为事实 |
| 世界接触 vs 责任 | world contact summary 带 observation refs 进入责任链 | 外部接触不能绕过 confirmation binding |
| 验证膜 vs 记忆写入 | S05 验证后才允许长期写入 | 推断、梦境或未验证外周状态不能污染记忆 |

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
