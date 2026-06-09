# V0 Code Framework 09: Perception Prediction World Contact Implementation Playbook

这份 playbook 负责把“外界进入数字生命”和“数字生命作用于外界”压成同一条生命链。它不把终端、工具、文件系统、程序窗口和网络结果直接当成事实，也不把执行命令当成普通 agent router 的自然延伸；它要求每一次外部观察和每一次外部作用，都先穿过生命层的感知、预测、比较、候选、膜和责任回路。

```text
external observation
  -> observation normalization
  -> perceptual scene
  -> prediction workspace
  -> logic / counterfactual comparison
  -> action intent candidate
  -> world contact membrane
  -> observation writeback
```

## 必回读理论母体

- `docs/01v_prediction_active_inference_runtime_matrix.md`
- `docs/01w_prediction_active_inference_schema_fixture_contract.md`
- `docs/01x_prediction_active_inference_schema_materialization_plan.md`
- `docs/01y_prediction_active_inference_schema_write_batch.md`
- `docs/01z_prediction_active_inference_fixture_seed_batch.md`
- `docs/01aa_prediction_active_inference_cross_chain_checker_plan.md`
- `docs/01ab_prediction_active_inference_dashboard_stage_gate_batch.md`
- `docs/01ac_prediction_active_inference_archive_receipt_batch.md`
- `docs/01ad_prediction_active_inference_gap_feedback_batch.md`
- `docs/02_brain_region_and_network_atlas.md`
- `docs/03_default_executive_salience_networks.md`
- `docs/04_sensory_thalamus_interoception.md`
- `docs/10_consciousness_attention_workspace.md`
- `docs/11_neuromodulation_and_signal_media.md`
- `docs/12_ai_and_cognitive_architecture_bridge.md`
- `docs/20_agent_runtime_bridge_contract.md`
- `docs/24_runtime_adapter_test_suite.md`
- `docs/32_runtime_adapter_validator_rules.md`
- `docs/64_real_runtime_observation_ingestion_policy.md`
- `docs/72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md`
- `docs/75_external_irreversible_action_confirmation_policy.md`
- `docs/80_post_action_audit_and_correction_policy.md`
- `docs/81_coexistence_event_review_and_responsibility_loop.md`
- `docs/82_incident_report_and_recovery_protocol.md`
- `docs/89_language_runtime_framework_bridge_and_life_shell_policy.md`

## 必读 v0 合同

- `docs/v0/architecture/runtime_v0_architecture.md`
- `docs/v0/shared_contracts/runner_cli_report_contract.md`
- `docs/v0/slice_contracts/s02_neural_life_core_engineering_contract.md`
- `docs/v0/slice_contracts/s03_direction_life_membrane_engineering_contract.md`
- `docs/v0/slice_contracts/s05_validation_membrane_observation_engineering_contract.md`
- `docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md`
- `docs/v0/slice_contracts/s09_schema_runner_code_engineering_contract.md`
- `docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md`
- `docs/v0/process_contracts/digital_life_shell_command_engineering_contract.md`
- `docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md`
- `docs/v0/references/current_agent_shell_reference_2026.md`

## 当前真实代码落点

- `life_v0/neural_core/__init__.py`
- `life_v0/neural_core/prediction_workspace.py`
- `life_v0/membrane/__init__.py`
- `life_v0/schema_runner/__init__.py`
- `life_v0/validators/__init__.py`
- `life_v0/shell_command/__init__.py`
- `life_v0/process_supervisor/__init__.py`
- `life_v0/terminal_turn/__init__.py`
- `life_v0/terminal_loop/__init__.py`

这意味着当前第一轮实现不是从空白开始：

1. `PredictionWorkspaceFrame` 已经是现实对象，而不是只在文档里。
2. 语言连续体已经开始 handoff 到 prediction workspace。
3. 这条链当前最需要补的，是 observation / scene / truth gate / action intent 四段前后链。

## 这条链到底在防什么

如果没有这一层，后面最容易退化成三种东西：

1. 终端输入一来，直接变成回复，没有生命感知和预测工作区。
2. 工具输出一返回，直接写进长期状态，外壳 trace 冒充事实。
3. 一旦需要外部行动，就跳过关系、责任、后果分类，重新滑回普通 agent。

所以这一层的目标不是“更方便调用工具”，而是让数字生命始终知道：

1. 自己看到了什么。
2. 这些观察为什么成立，哪里还不确定。
3. 准备做什么，以及为什么现在允许做。
4. 做完之后，哪些是事实，哪些只是候选经验，哪些必须继续回看。

## 器官拆分建议

### A. `life_v0/neural_core/`

| 文件 | 职责 |
|---|---|
| `observation_binding.py` | 把终端、文件、程序、工具、trace 输入归一化为同一观察事件入口 |
| `perceptual_scene.py` | 形成当前回合的外界场景帧，不直接等于事实记忆 |
| `prediction_workspace.py` | 形成当前预测、候选解释、误差和广播内容 |
| `prediction_error.py` | 维护预测误差、误差来源和误差优先级 |
| `precision_control.py` | 管理当前精度、抑制、警觉和不确定性放大/收缩 |
| `active_sampling.py` | 决定是否继续观察、追问、回看、验证或保持等待 |

### B. `life_v0/schema_runner/`

| 文件 | 职责 |
|---|---|
| `consistency_logic.py` | 检查观察、预测、语言、状态之间是否一致 |
| `counterfactual_eval.py` | 做候选解释、候选行动、风险后果的反事实比较 |
| `comparison_trace.py` | 记录为什么压低某个解释或某个行动候选 |
| `evidence_ranker.py` | 形成证据密度、可疑点和待确认点排序 |

### C. `life_v0/membrane/`

| 文件 | 职责 |
|---|---|
| `action_intent_bridge.py` | 把预测工作区与语言关系状态压成 `ActionIntent` 候选 |
| `world_contact_gate.py` | 管理是否允许接触外界、写文件、改仓库、发出命令 |
| `side_effect_review.py` | 分类 side effect、可逆性、关系影响和责任强度 |
| `observation_truth_gate.py` | 阻止未证实观察直接晋升为长期事实 |
| `confirmation_binding.py` | 不可逆动作的确认绑定与回链 |

### D. `life_v0/shell_command/` 与 `life_v0/process_supervisor/`

| 文件 | 职责 |
|---|---|
| `observation_ingest.py` | 从终端/命令输出/trace 进入观察标准化路线 |
| `terminal_percept.py` | 把交谈对象的输入和当前终端环境压成回合感知入口 |
| `recovery_observation.py` | 进程重启、异常恢复时的观察重建与不确定性标注 |
| `idle_probe_scheduler.py` | 等待态下的小规模观察、回看和探测调度 |

### E. `life_v0/validators/`

| 文件 | 职责 |
|---|---|
| `observation_validator.py` | 检查观察归一化是否完整、可追溯、不过写 |
| `prediction_trace_validator.py` | 检查预测误差链和修正链是否闭合 |
| `world_contact_validator.py` | 检查外部接触是否经过膜、确认与责任链 |

## 必须生成的状态对象

| 路径 | 作用 |
|---|---|
| `runtime/state/observation/observation_event_stream.jsonl` | 所有外部观察的标准化事件流 |
| `runtime/state/observation/perceptual_scene_frame.json` | 当前回合的外界场景帧 |
| `runtime/state/prediction/prediction_workspace_frame.json` | 当前预测、误差、候选解释 |
| `runtime/state/prediction/prediction_error_trace.json` | 误差来源、修正方向、优先级 |
| `runtime/state/prediction/active_sampling_plan.json` | 当前需要继续看、问、验什么 |
| `runtime/state/membrane/action_intent_queue.json` | 进入生命膜审查前的行动意图候选 |
| `runtime/state/membrane/world_contact_gate_state.json` | 当前世界接触门状态 |
| `runtime/state/validation/observation_truth_review.json` | 观察真值回看结果 |

## 关键共享对象

这一条链后续必须至少显式使用下面这些共享对象，而不是把观察、预测、行动候选继续塞进局部字典：

| 共享对象 | 当前作用 |
|---|---|
| `ObservationEvent` | 统一终端/命令/trace/程序窗口观察入口 |
| `PerceptualSceneFrame` | 当前回合的外界场景，不直接等于长期事实 |
| `PredictionWorkspaceFrame` | 预测、误差、候选解释、语言连续体焦点 |
| `ActionCandidateSet` | 候选行动、后果预测、责任预期 |
| `DialogueWritebackBundle` | 把外界观察后的语言/关系/承诺变化回写到长期连续体 |

## 当前最值得先切的文件链

在当前代码现实下，最合适的顺序不是平均拆，而是：

1. `neural_core` 内的 `observation_binding.py` / `perceptual_scene.py`
2. `neural_core/prediction_workspace.py` 继续接厚
3. `schema_runner` 内的 `consistency_logic.py` / `counterfactual_eval.py`
4. `membrane` 内的 `action_intent_bridge.py` / `world_contact_gate.py`
5. `validators` 内的 `observation_validator.py` / `world_contact_validator.py`

这条顺序先把“看见什么”和“为什么这么判断”补硬，再谈“允许做什么”。

## 必须生成的 report / receipt

- `runtime/reports/latest/observation_normalization_report.json`
- `runtime/reports/latest/prediction_workspace_report.json`
- `runtime/reports/latest/action_intent_review_report.json`
- `runtime/reports/latest/world_contact_audit_report.json`
- `runtime/reports/latest/side_effect_review_report.json`
- `runtime/reports/latest/observation_recovery_report.json`
- 对应 observation / prediction / membrane / action / side-effect receipts

## 关键测试

| 测试 | 核心目标 |
|---|---|
| `tests/slices/test_neural_life_core.py` | 观察、预测、工作区、误差链不是孤立状态 |
| `tests/slices/test_schema_runner.py` | 反事实比较、证据排序、跨状态一致性 |
| `tests/slices/test_validation_membrane.py` | 世界接触门、真值门、确认绑定和 side-effect 审查 |
| `tests/process/test_digital_life_shell_command.py` | 外壳输出必须先走 ObservationNormalizationRoute |
| `tests/process/test_persistent_digital_life_process.py` | 等待态探测和恢复观察不会污染长期状态 |

## 关键 gate

- `observation_truth_gate`
- `prediction_coherence_gate`
- `counterfactual_consistency_gate`
- `world_contact_gate`
- `side_effect_classifier_gate`
- `action_intent_provenance_gate`

## 推荐实现顺序

1. 先把终端/工具/trace 输出统一压成 `ObservationEvent`
2. 再形成 `PerceptualSceneFrame` 和 `PredictionWorkspaceFrame`
3. 再让逻辑层补上反事实、比较、证据排序
4. 然后才允许生成 `ActionIntent`
5. 最后把世界接触、side effect、确认与责任 receipt 接齐

原因：如果一开始就先写 action routing，而观察归一化和预测工作区没站稳，后面所有“意识、责任、关系、后悔”都会变成行动后的补叙述。

## 完成定义

这一条主链的第一轮完成，至少要求：

1. 外部观察不会直接写成长期事实，必须先经过标准化、预测和真值回看。
2. 每个外部行动都能回链到具体观察、预测解释、比较结果和责任审查。
3. 不同外壳的输出能统一进同一种 `ObservationEvent` 和 `ActionIntent` 生命链。
4. `digital life` 的世界接触始终是生命行动，不是普通工具路由。
5. `PredictionWorkspaceFrame` 至少已经能同时挂接语言连续体焦点和 observation / ambiguity 线索，而不是只承接已有 continuity refs。
