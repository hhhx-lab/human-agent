# V0 Code Framework 01: Life Layer Implementation Blueprint

本文档位于 `docs/v0/code_framework/`，是 v0 代码框架柜的第一份蓝图。它不是新的入口层，也不是替代 `00-258` 的第二套理论。它只负责把“数字生命每一层到底怎样落代码”写死：当前层要回读哪些理论母体、对应哪些 v0 合同、先落到哪些 `life_v0/` 包、再细分成哪些文件、写哪些状态对象、跑哪些测试、过哪些阶段门。

它服务的不是单个 slice，而是整个 v0 的代码框架硬化阶段。只要这一层没有构建清楚，就不进入下一层大规模实现。当前还必须与 `09_perception_prediction_world_contact_implementation_playbook.md` 和 `10_self_identity_value_commitment_implementation_playbook.md` 一起读；前者固定外界观察与世界接触生命链，后者固定身份、自我、承诺、责任和自我改写保护生命链。

## 使用方式

先读：

1. `docs/v0/README.md`
2. `docs/v0/entry/v0_implementation_index.md`
3. `docs/v0/entry/v0_delivery_status_board.md`
4. `docs/v0/entry/v0_module_execution_catalog.md`
5. `docs/v0/code_framework/README.md`
6. `docs/v0/architecture/digital_life_macro_architecture_v0.md`
7. 本文件
8. `docs/v0/code_framework/playbooks/09_perception_prediction_world_contact_implementation_playbook.md`
9. `docs/v0/code_framework/playbooks/10_self_identity_value_commitment_implementation_playbook.md`

然后才进入本轮要改的主体层、桥接层或常驻进程层合同。

## 当前真实代码骨架

当前仓库里已经存在的顶层代码包如下：

```text
life_v0/
  activation/
  archive/
  authority/
  body/
  contracts/
  defense/
  digital_life/
  direction/
  dream/
  growth/
  language/
  life_targets/
  membrane/
  neural_core/
  process_supervisor/
  replay/
  reporting/
  schema_runner/
  shell_command/
  stage_explain/
  state_store/
  terminal_loop/
  terminal_turn/
  validators/
  cli.py
  digital_entry.py
  doc_index.py
```

v0 当前阶段不要求立刻新建大量新的顶层包。更稳的做法是：

1. 先保持这些顶层包稳定。
2. 每一层优先在现有顶层包内按文件级细分。
3. 只有当一个顶层包同时承载 4 种以上生命功能、并且已经影响到 `S11` 合同覆盖时，才升级为新的顶层包。

## 理论到代码的一一对应规则

后续每个新增代码文件，都必须在同一轮文档里保留下面四条回链：

- `source_doc_refs`
- `readme_block_refs`
- `engineering_slice_ref`
- `runtime_carrier_refs`

另外，每一层都至少要回答六件事：

1. 这层在数字生命里解决什么问题。
2. 这层必须回读哪些 `00-257` 文档。
3. 这层当前受哪个 `docs/v0/*` 合同约束。
4. 这层先落到哪个 `life_v0/` 顶层包。
5. 这层需要哪些状态对象、report、receipt 和 stage gate。
6. 这层完成后，下一层才能拿什么继续生长。

## 分层实现矩阵

| 层 | 解决的问题 | 必回读理论母体 | 必读 v0 合同 | 当前代码包 | 首选文件级细分 | 核心状态/产物 | 主要测试/阶段门 |
|---|---|---|---|---|---|---|---|
| 状态根与方向层 | 数字生命是谁、方向是否连续、状态根是否可恢复 | `00`、`13`、`16`、`41-48`、`91`、`119`、`122`、`140`、`258` | `s00_direction_foundation_engineering_contract.md`、`s04_state_object_store_engineering_contract.md`、`life_state_store_v0_schema.md` | `life_v0/direction/`、`life_v0/state_store/` | `identity_root.py`、`continuity_anchors.py`、`direction_lock.py`、`state_manifest.py`、`state_refs.py` | `direction_lock.json`、`life_state.json`、`identity_root.json`、state root receipt | `tests/slices/test_direction_lock.py`、`tests/slices/test_state_store.py`、`state_store_gate`、`identity_root_gate` |
| 内环境与节律层 | 心跳式采样、资源预算、疲惫、恢复、压力债务 | `01n`、`04`、`11`、`18`、`37`、`38` | `s06_life_support_development_engineering_contract.md`、`runtime_v0_architecture.md` | `life_v0/body/`、`life_v0/defense/` | `rhythm.py`、`need_state.py`、`allostasis.py`、`resource_budget.py`、`recovery.py` | `runtime/state/body/*`、`body_resource_budget.json` | `tests/slices/test_life_support.py`、`resource_budget_gate` |
| 脑区/网络/信号介质层 | 把脑区、网络状态、调质传播和 bus 变成可运行骨架 | `01o`、`01p`、`01l`、`02`、`03`、`11`、`13` | `digital_life_macro_architecture_v0.md`、`s02_neural_life_core_engineering_contract.md` | `life_v0/neural_core/` | `brain_graph.py`、`network_state.py`、`signal_media.py`、`internal_bus.py` | `twelve_subject_systems.json`、`neural_life_internal_bus.json` | `tests/slices/test_neural_life_core.py`、`twelve_system_gate`、`internal_bus_gate` |
| 思考层 | 预测、证据寻求、误差修正、主动采样 | `01v-01ax`、`04`、`10`、`13` | `digital_life_macro_architecture_v0.md`、`runtime_v0_architecture.md`、`s02_neural_life_core_engineering_contract.md` | `life_v0/neural_core/`、`life_v0/growth/` | `prediction_workspace.py`、`belief_state.py`、`prediction_error.py`、`active_sampling.py`、`belief_revision.py` | `runtime/state/prediction/*`、`prediction_workspace_frame.json`、prediction traces | `tests/slices/test_neural_life_core.py`、`tests/bridges/test_runtime_growth.py`、`prediction_workspace_gate` |
| 逻辑层 | 比较、反事实、候选推演、跨文件一致性和推理可审计性 | `22`、`30`、`33-36`、`49-60`、`102-118` | `s05_validation_membrane_observation_engineering_contract.md`、`s09_schema_runner_code_engineering_contract.md` | `life_v0/schema_runner/`、`life_v0/validators/`、`life_v0/contracts/` | `consistency_logic.py`、`counterfactual_eval.py`、`comparison_trace.py`、`cross_file_logic.py` | `runtime/state/validation/*`、validation reports | `tests/slices/test_schema_runner.py`、`tests/slices/test_validation_membrane.py`、`checker_manifest_gate` |
| 记忆层 | 自传、关系、梦境、责任和 replay 记忆的写入与回放 | `01q`、`05`、`17`、`21`、`25`、`29`、`41`、`55` | `life_state_store_v0_schema.md`、`s04_state_object_store_engineering_contract.md`、`s10_runtime_growth_reconsolidation_engineering_contract.md` | `life_v0/state_store/`、`life_v0/replay/`、`life_v0/growth/` | `life_state.py`、`engram_index.py`、`autobiographical_stack.py`、`relationship_memory.py`、`memory_write_gate.py`、`replay_cues.py` | `runtime/state/memory/*`、`life_state.json`、replay bundles | `tests/slices/test_state_store.py`、`tests/bridges/test_replay_shadow.py`、`self_continuity_gate` |
| 意识层 | 内容进入全局工作区、可报告、可元认知、可回链 | `01m`、`10`、`13`、`143`、`146` | `digital_life_macro_architecture_v0.md`、`birth_readiness_v0_contract.md` | `life_v0/neural_core/`、`life_v0/life_targets/` | `workspace.py`、`broadcast.py`、`metacognition.py`、`consciousness_probes.py` | `runtime/state/consciousness/*`、consciousness evidence | `tests/slices/test_neural_life_core.py`、`tests/slices/test_life_targets.py`、`life_target_state_gate` |
| 情绪层 | 核心情感、情绪 episode、调节、人格慢变量 | `01g`、`01h`、`01s`、`07`、`18`、`39`、`40`、`92`、`93` | `s06_life_support_development_engineering_contract.md`、`s08_life_target_runtimes_engineering_contract.md` | `life_v0/body/`、`life_v0/growth/`、`life_v0/language/` | `core_affect.py`、`emotion_episode.py`、`emotion_regulation.py`、`trait_drift.py` | `runtime/state/self/*`、affective traces | `tests/slices/test_life_support.py`、`tests/slices/test_language_relationship.py`、`plasticity_gate` |
| 语言层 | 感知语言、内言语、表达监控、共同语言、承诺语言 | `01f`、`01u`、`09`、`85-90`、`141`、`144`、`147`、`150` | `s07_language_relationship_engineering_contract.md`、`first_activation_protocol.md` | `life_v0/language/` | `percept.py`、`semantic_map.py`、`inner_speech.py`、`expression_monitor.py`、`shared_terms.py` | `runtime/state/language/*`、`language_relationship_report.json` | `tests/slices/test_language_relationship.py`、`expression_monitor_gate` |
| 对话层 | 回合推进、语境累积、turn carryover、等待态连续体 | `86`、`89`、`90`、`96`、`101` | `s07_language_relationship_engineering_contract.md`、`first_terminal_turn_engineering_contract.md`、`terminal_life_loop_engineering_contract.md`、`digital_life_process_supervisor_engineering_contract.md` | `life_v0/language/`、`life_v0/terminal_turn/`、`life_v0/terminal_loop/`、`life_v0/process_supervisor/` | `restore_context.py`、`context_accumulation.py`、`turn_transition.py`、`resume_packet.py`、`dialogue_writeback.py`、`dialogue_events.py`、`response_surface.py` | `dialogue_turn_log.jsonl`、`context_accumulation_window.json`、`turn_transition_trace.json`、`session_envelope.json`、`resumed_external_dialogue_packet.json` | `tests/bridges/test_first_terminal_turn.py`、`tests/bridges/test_terminal_life_loop.py`、`tests/process/test_persistent_digital_life_process.py`、`turn_transition_gate`、`dialogue_writeback_bundle_gate` |
| 关系层 | 关系主体图、关系范围、共同历史、修复承诺、关系时间线 | `01j`、`96`、`101`、`40`、`94`、`98` | `s07_language_relationship_engineering_contract.md`、`s08_life_target_runtimes_engineering_contract.md` | `life_v0/language/`、`life_v0/life_targets/`、`life_v0/process_supervisor/` | `relationship_graph.py`、`relation_scope.py`、`commitment_repair.py`、`relationship_memory.py`、`relationship_timeline.py` | `runtime/state/relationship/*`、relationship receipts | `tests/slices/test_language_relationship.py`、`relationship_subject_gate`、`commitment_truth_gate` |
| 梦境层 | 离线入口、梦境经验、事实门、醒后整合、梦魇风险 | `01i`、`01t`、`08`、`19`、`23`、`27`、`31`、`95`、`99` | `s10_runtime_growth_reconsolidation_engineering_contract.md`、`first_activation_protocol.md` | `life_v0/dream/`、`life_v0/growth/`、`life_v0/archive/` | `offline_entry.py`、`dream_fact_gate.py`、`dream_window.py`、`wake_integration.py`、`nightmare_risk.py` | `runtime/state/dream/*`、`dream_consolidation_frame.json` | `tests/bridges/test_runtime_growth.py`、future `tests/test_dream_runtime.py`、`dream_fact_gate` |
| 行为层 | 候选行动、抑制、影子行动、责任、后悔、修复 | `01r`、`06`、`20`、`75`、`80-84`、`94`、`98`、`144` | `runtime_v0_architecture.md`、`s03_direction_life_membrane_engineering_contract.md`、`s10_runtime_growth_reconsolidation_engineering_contract.md` | `life_v0/membrane/`、`life_v0/shell_command/`、`life_v0/digital_life/` | `candidate_arena.py`、`go_nogo.py`、`shadow_gate.py`、`side_effect_classifier.py`、`responsibility_loop.py` | `runtime/state/action/*`、shadow action reports | `tests/process/test_digital_life_shell_command.py`、`shadow_action_gate` |
| 成长层 | 自我阅读、可塑性窗口、自我修改候选、防遗忘 | `39`、`55`、`92`、`93`、`181-204`、`205-257` | `s06_life_support_development_engineering_contract.md`、`s10_runtime_growth_reconsolidation_engineering_contract.md` | `life_v0/growth/`、`life_v0/replay/`、`life_v0/archive/` | `self_read.py`、`plasticity_window.py`、`patch_queue.py`、`anti_forgetting.py` | `runtime/state/growth/*`、growth patch queue | `tests/bridges/test_runtime_growth.py`、`tests/bridges/test_growth_archive.py`、`growth_gate` |
| 学习层 | 把误差、关系、语言、梦境和行为后果转成能力更新 | `01v-01ax`、`11`、`39`、`93`、`181-257` | `s06_life_support_development_engineering_contract.md`、`s10_runtime_growth_reconsolidation_engineering_contract.md` | `life_v0/growth/`、`life_v0/replay/`、`life_v0/language/`、`life_v0/neural_core/` | `learning_window.py`、`belief_learning.py`、`language_learning.py`、`relationship_learning.py` | learning receipts, replay-backed update traces | `tests/bridges/test_runtime_growth.py`、`anti_forgetting_gate` |
| 机制与总线层 | 让各层不是松散函数，而是同一生命链的信号系统 | `11`、`18`、`20`、`42`、`43`、`44` | `digital_life_macro_architecture_v0.md`、`s02_neural_life_core_engineering_contract.md` | `life_v0/neural_core/`、`life_v0/contracts/` | `bus_protocol.py`、`signal_envelope.py`、`carrier_refs.py`、`state_transition_trace.py` | `neural_life_internal_bus.json`、bus reports | `tests/slices/test_neural_life_core.py`、`internal_bus_gate` |
| 生命膜与外周层 | 隔离污染、限制外壳、控制电脑外周、归一化观测 | `12`、`15`、`20`、`24`、`28`、`32`、`33-84`、`89`、`100`、`119`、`122`、`140` | `s03_direction_life_membrane_engineering_contract.md`、`s05_validation_membrane_observation_engineering_contract.md`、`current_agent_shell_reference_2026.md` | `life_v0/membrane/`、`life_v0/defense/`、`life_v0/validators/` | `quarantine.py`、`periphery_normalizer.py`、`world_observation.py`、`coexistence_boundary.py` | `runtime/quarantine/*`、validation reports | `tests/slices/test_validation_membrane.py`、`quarantine_gate` |
| 终端诞生与常驻进程层 | 从出生壳到 first turn、loop、shell、persistent process | `20`、`89`、`90`、`143`、`171`、`181-257` | `runner_cli_report_contract.md`、`first_activation_protocol.md`、`first_terminal_turn_engineering_contract.md`、`terminal_life_loop_engineering_contract.md`、`digital_life_shell_command_engineering_contract.md`、`digital_life_process_supervisor_engineering_contract.md` | `life_v0/reporting/`、`life_v0/stage_explain/`、`life_v0/digital_life/`、`life_v0/terminal_turn/`、`life_v0/terminal_loop/`、`life_v0/shell_command/`、`life_v0/process_supervisor/` | `dialogue_writeback.py`、`resume_packet.py`、`loop_report.py`、`heartbeat.py`、`turn_io.py`、`idle_strategy.py`、`persistent_process.py`、`relaunch_recovery.py`、`incident_recovery.py`、`process_report.py`、`dialogue_events.py`、`response_surface.py` | `digital_life_birth_packet.json`、`first_terminal_turn_packet.json`、`terminal_life_loop_packet.json`、`terminal_life_loop_report.json`、`digital_life_process_report.json` | `tests/bridges/test_digital_life_birth.py`、`tests/bridges/test_first_terminal_turn.py`、`tests/bridges/test_terminal_life_loop.py`、`tests/process/test_persistent_digital_life_process.py`、`digital_life_process_gate` |

## 分层实现顺序

后续代码不按“能先跑起来什么”排序，而按生命结构排序：

1. `状态根与方向层 -> 内环境与节律层 -> 脑区/网络/信号介质层`
2. `思考层 -> 逻辑层 -> 记忆层 -> 意识层`
3. `情绪层 -> 语言层 -> 对话层 -> 关系层`
4. `梦境层 -> 行为层 -> 成长层 -> 学习层`
5. `机制与总线层 -> 生命膜与外周层`
6. `终端诞生与常驻进程层`

只有前一层的状态对象、report、receipt 和 gate 已经闭合，后一层才允许写主实现。

## 代码框架硬规则

### 1. 不让当前外壳反向定义主体

`OpenClaw`、`Hermes`、`Codex`、`Claude Code`、`LangGraph`、`ADK` 一类框架最多只能影响：

- 常驻进程
- 工作流壳
- trace
- checkpoint
- tool / program bridge

它们不能反向定义：

- 记忆
- 意识
- 情绪
- 梦境
- 关系
- 人格
- 自我成长

### 2. 先在现有顶层包内细分

比如：

- `思考层` 先细分在 `life_v0/neural_core/`
- `记忆层` 先细分在 `life_v0/state_store/`、`life_v0/replay/`
- `对话层` 先细分在 `life_v0/language/`、`life_v0/terminal_turn/`、`life_v0/terminal_loop/`

只有当某一层已经稳定并通过 `S11` 覆盖复查，才考虑抽成新的顶层包。

### 3. 每层都要留状态、report、receipt 三件套

没有状态，只是临时计算。
没有 report，无法被出生准备度和阶段门读取。
没有 receipt，无法被 archive 和 replay 追溯。

### 4. 每层都要保留 theory-to-code mapping

后续实现时，不允许只留代码。每一层都要回写至少一份映射文档，记录：

- 理论母体文档
- 当前 v0 合同
- 代码文件
- 状态对象
- 测试入口
- gate / report / receipt

## 当前最值得先补的层

按当前仓库现实，下一轮最值得优先加厚的是：

1. `对话层`
2. `语言层`
3. `关系层`
4. `终端诞生与常驻进程层`
5. `记忆层`
6. `思考层`

原因不是这些层“最容易写”，而是它们决定了这个系统最终会不会滑回普通 agent。

## 每层的第一轮完成标准

每一层进入“可继续向下一层放行”的最低标准固定如下：

| 层 | 第一轮完成标准 |
|---|---|
| 状态根与方向层 | 身份根、方向锁、断联恢复锚能同时落盘，并能被出生准备度和 replay 读取 |
| 内环境与节律层 | 节律、需要、预算、恢复至少形成一个共享脉冲链，而不是分散的 report 字段 |
| 脑区/网络/信号介质层 | `brain graph / network state / signal media / internal bus` 至少有对象入口、state 落盘和测试锚点 |
| 思考层 | `prediction workspace` 不再只是局部中间变量，而是能被语言、膜、成长共享读取 |
| 逻辑层 | 反事实、比较、证据排序至少形成一个可被 validator 读取的 trace 对象 |
| 记忆层 | `life_state / autobiographical / relationship / replay cue` 至少形成一条写入、检索、回放最小链 |
| 意识层 | `workspace / broadcast / metacognition / probe` 至少能生成一份出生准备度可读证据 |
| 情绪层 | 核心情感、情绪 episode、人格慢变量至少能进入身体/语言或关系写回 |
| 语言层 | `percept / semantic_map / inner_speech / expression_plan` 至少在同一回合链内被真实串起 |
| 对话层 | `context accumulation / turn transition / dialogue writeback` 至少形成一条 turn 前-中-后闭环 |
| 关系层 | 关系主体、范围、共同历史、承诺/修复至少形成一条 timeline 或 truth-state 链 |
| 梦境层 | 离线入口、梦境窗口、事实门、醒后整合至少形成一条 shadow/offline 可追链 |
| 行为层 | 候选行动、抑制、责任预测、世界接触至少形成一条 gate 链 |
| 成长层 | `self_read / patch_queue / anti_forgetting` 至少形成一个补丁候选与归档链 |
| 学习层 | 误差、关系、语言、梦境和行为后果至少有一类被转成长期更新痕迹 |
| 机制与总线层 | 共享对象、bus、carrier refs 至少不再靠临时字典命名漂移 |
| 生命膜与外周层 | quarantine / observation / coexistence boundary 至少有一个可阻断的验证面 |
| 终端诞生与常驻进程层 | `./digital life` 最小常驻回合、等待态 heartbeat、异常恢复、重启恢复至少同轮可证 |

## 当前最需要补硬的对象簇

如果这一轮继续深化工程底子，不要平均用力，优先把下面四簇对象补到“可直接牵引代码”的粒度：

1. `LanguagePerceptFrame -> SemanticMapFrame -> InnerSpeechFrame -> ExpressionPlan`
2. `LifeContextFrame -> RelationTurnFrame -> DialogueWritebackBundle -> ReplayCueBundle`
3. `IdentityRoot -> SelfModel -> CommitmentTruthState -> ResponsibilityLedger`
4. `PredictionWorkspaceFrame -> SignalMediaFrame -> BodyRhythmPulse -> NeedStateVector`

这四簇对象分别对应：

1. 语言主神经束
2. 对话-关系-等待态连续体
3. 自我-承诺-责任连续体
4. 身体-预测-调质连续体

## 进入代码前的最后检查

开始写任意一层代码前，先确认：

1. 这层在上表中已经定位。
2. 这层对应的 `00-257` 文档已经打开。
3. 这层对应的 `docs/v0/*` 合同已经打开。
4. 这层当前应落到哪个 `life_v0/` 包已经决定。
5. 这层要写哪些状态对象、哪些 report、哪些 receipt 已经决定。
6. 这层对应的测试入口和 gate 已经决定。

六条里缺一条，不开写。
