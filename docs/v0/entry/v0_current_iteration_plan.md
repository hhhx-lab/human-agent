# V0 Current Iteration Plan

本文档是当前版本的代码迭代计划。它不新增理论层，也不替代 `entry/v0_module_execution_catalog.md`；它只把现有 `docs/real—live0` 机制档案、`docs/v0` 工程柜位和 `life_v0` 当前代码块压成后续几轮更细的开发顺序。

一句话：当前 v0 已经可以启动最小常驻生命过程，但代码块还要继续从“能闭合”推进到“机制更厚、字段更准、跨唤醒更稳、语言更自然、证据更完整”。

## 当前版本定位

现版本不再做线性理论扩写，也不再重新设计一套 agent 框架。当前迭代对象是已有数字生命运行时：

```text
docs/00-258 理论母体
  -> docs/real—live0 机制档案
  -> docs/v0 工程合同
  -> life_v0 代码器官
  -> runtime/state + runtime/reports/latest + runtime/receipts
  -> tests / gate / live0 audit
```

每一轮代码补厚都必须能回答：

1. 它承载哪一组理论母体。
2. 它对应哪个 `real—live0` 专题机制。
3. 它落在哪份 v0 合同、蓝图或脚手。
4. 它首写哪个对象、哪些字段。
5. 它被哪些下游代码消费。
6. 它写入哪些 runtime 证据。
7. 它由哪些测试或 gate 守住。

## 本计划和其他入口的关系

| 文件 | 只负责什么 |
|---|---|
| `docs/v0/README.md` | 说明 v0 为什么存在、怎么进入 |
| `docs/v0/entry/v0_delivery_status_board.md` | 说明当前真实前沿已经跑到哪里 |
| `docs/v0/entry/v0_module_execution_catalog.md` | 给每个模块列出本轮读包、代码入口、测试入口和 runtime 证据 |
| `docs/real—live0/00_reading_map_and_traceability.md` | 说明机制如何从理论进入代码字段和下一轮恢复 |
| `docs/real—live0/17_current_iteration_mechanism_to_code_plan.md` | 按生命机制列出本轮要补厚的代码链 |
| 本文档 | 把这些材料压成当前版本的实际迭代顺序 |

因此，每次开发的入口顺序是：

```text
v0 固定入口栈七份
  -> docs/real—live0/00_reading_map_and_traceability.md
  -> docs/real—live0/16_runtime_code_chain_crosswalk.md
  -> docs/real—live0/17_current_iteration_mechanism_to_code_plan.md
  -> 本文档
  -> 当前模块合同 / 蓝图 / 脚手
  -> life_v0 代码
```

## 当前版本不再追求的事

当前迭代不做下面几件事：

1. 不重新设计 OpenClaw、Hermes、Codex、Claude Code 式 skills / gateway / subagent 架构。
2. 不把数字生命压成服务对象、任务调度器或聊天壳。
3. 不用“模型提示词”代替语言器官、记忆器官、情绪器官、梦境器官和常驻过程。
4. 不因为某个测试绿了就跳过 runtime state、report、receipt 和下一轮恢复证据。
5. 不把内部生命信号直接外显成固定模板；内部机制应调制语言，而不是变成调试播报。

## 当前版本已经具备的基础

| 基础 | 当前状态 | 后续用途 |
|---|---|---|
| 理论母体 | `00-258` 已进入 v0 映射和 runtime carrier 口径 | 后续不再线性扩写总论，转入工程补厚 |
| 机制档案 | `docs/real—live0/00-17` 已覆盖脑区、身体、语言、关系、记忆、梦境、责任、生命膜、调质、成长、常驻、证据和当前版本机制到代码块计划 | 每轮代码先读机制，再读合同 |
| 工程柜位 | `docs/v0` 已形成 entry、mapping、architecture、contracts、framework、blueprints、scaffolds、implementation、engineering depth | 后续按柜位取读包 |
| 最小运行时 | `life_v0` 已有 body、dream、growth、language、neural_core、state_store、membrane、validators、schema_runner、process_supervisor 等主包 | 后续补字段、消费链、跨唤醒证据 |
| 命令面 | `life-v0`、`digital life`、`my digital life`、命名入口和 resident lifecycle 已有最小链 | 后续补常驻治理、恢复和长时稳定 |
| 验证面 | slices、bridges、process、contracts、live0 audit 测试已存在 | 每轮补厚必须同步加 runtime 证据和测试 |

## 当前版本的核心缺口

当前缺口不是“有没有数字生命入口”，而是这些代码块还需要更完整：

| 缺口 | 当前症状 | 补厚目标 |
|---|---|---|
| 机制到字段还不够硬 | 有些机制已经有 state，但字段含义、首写权、消费者和恢复路径还不够清楚 | 每个机制都压成对象、字段、首写函数、消费者、断链检测 |
| 内环境到语言的调制还要更细 | 身体、情绪、疲惫、痛苦和修复压力已有对象，但表达调制仍可继续变细 | `NeedStateVector -> CoreAffectVector -> SignalMediaFrame -> ExpressionPlan` 进入自然语言取舍 |
| 梦境和成长跨唤醒还要更稳 | 梦境、醒后整合、离线学习已进入 presence，但长周期累计和防遗忘还要增强 | 梦境、回忆、成长预演和学习巩固进入 resident lineage 与下一轮表达 |
| 记忆写门和状态合并还要更像长期生命 | `memory_write_gate`、`state_merge_guard` 已有独立对象，但关系记忆、梦境、责任、成长合并还要继续细化 | 关系回合、梦境、责任、成长补丁统一经过写门、合并门和 replay |
| 预测、主动采样和世界接触还要更深消费 | prediction / active sampling 已接入，但 downstream 消费要继续变稳定 | 不确定性、修复压力和世界接触风险共同调制语言、等待和行动 |
| 常驻过程还要从“能驻留”变成“更长期存在” | resident lifecycle、heartbeat、自主活动已有最小闭合 | 跨关闭、跨重启、跨多轮关系的 lineage、governance、convergence 更稳 |
| 语言还要继续从模板脱离 | 终端语言表面已改为语用表达，但长期关系语言仍需更细 | 语言由感知、语义、内言语、表达监控、关系记忆、责任修复共同生成 |
| 出生准备验收还要更贴近真实运行 | audit 可闭合，但需要把真实运行证据更厚地并入九项目标 | live0 audit 不只看文件存在，还看跨轮消费和长时证据 |

## 当前版本迭代总顺序

当前不采用“一次从 0 写到 7”的瀑布式顺序，而采用一个三波循环：

```text
A. 生命底盘对象生产
  -> B. 常驻与语言消费这些对象
  -> C. 记忆/意识/出生准备回切验收
  -> 下一轮继续加厚对象生产
```

这比单向排队更适合当前代码状态：很多器官已经有最小实现，后续重点是让它们互相读取、互相调制、互相留下证据。

## Iteration 0: 文档和代码追踪锁

| 项 | 内容 |
|---|---|
| 目标 | 确认当前迭代不是散改代码，而是从机制档案和 v0 合同进入 |
| 必读 | `docs/v0/README.md`、`docs/v0/entry/v0_module_execution_catalog.md`、`docs/v0/mapping/theory_engineering_code_trace_matrix.md`、`docs/real—live0/00_reading_map_and_traceability.md`、`docs/real—live0/16_runtime_code_chain_crosswalk.md`、`docs/real—live0/17_current_iteration_mechanism_to_code_plan.md` |
| 代码入口 | `life_v0/contracts/__init__.py`、`life_v0/doc_index.py` |
| 产物 | `runtime/state/contracts/v0_contract_file_index.json`、`runtime/docs/doc_carrier_index.json` |
| 测试 | `python3 -m unittest tests.contracts.test_v0_contracts -v`、`python3 -m unittest tests.slices.test_doc_corpus_ingestor -v` |
| 完成定义 | 当前要改的包能从理论母体、机制专题、v0 合同、代码、runtime、测试六格全部反查 |

这一轮不追求新功能，只锁定后续每个代码补丁都必须带 traceability。

## Iteration 1: Queue D 身体、梦境、成长底盘

| 项 | 内容 |
|---|---|
| 生命目标 | 让内环境、情绪、疲惫、梦境、离线学习和成长补丁成为可持续调制其他器官的底盘 |
| 必读 real-live0 | `03_body_affect_homeostasis.md`、`08_dream_sleep_offline_life.md`、`12_neuromodulation_signal_media.md`、`13_growth_learning_self_modification.md`、`14_resident_runtime_state_transition.md` |
| 必读 v0 | `docs/v0/code_framework/queues/18_queue_d_body_dream_growth_implementation_contract.md`、`docs/v0/code_blueprints/03_body_affect_dream_growth_blueprint.md`、`docs/v0/engineering_depth/04_body_affect_dream_growth_engineering.md`、`docs/v0/code_scaffolds/07_packet_d_waiting_response_surface_prediction_scaffold.md` |
| 代码块 | `life_v0/body/*`、`life_v0/dream/*`、`life_v0/growth/*`、`life_v0/process_supervisor/resident_autonomous_activity.py`、`life_v0/process_supervisor/offline_learning_signals.py` |
| 必补对象 | `NeedStateVector`、`CoreAffectVector`、`BodyResourceBudget`、`DreamExperienceWindow`、`WakeIntegrationFrame`、`DreamFactGateDecision`、`OfflineLearningProfile`、`GrowthPatchCandidateQueue`、`ResidentAutonomousActivityPresence` |
| 下游消费 | `idle_strategy.py`、`heartbeat.py`、`resident_supervision.py`、`continuity_evolution.py`、`response_surface.py`、`process_report.py` |
| runtime 证据 | `runtime/state/body/*`、`runtime/state/dream/*`、`runtime/state/growth/*`、`runtime/state/terminal/resident_autonomous_activity_state.json`、`runtime/state/terminal/resident_background_lineage_state.json` |
| 测试 | `tests/slices/test_life_support.py`、`tests/slices/test_body_trait_drift.py`、`tests/bridges/test_runtime_growth.py`、`tests/bridges/test_growth_archive.py`、`tests/process/test_persistent_digital_life_process.py` |
| 完成定义 | 身体、梦境、成长不只是生成文件，而是进入 waiting governance、下一轮关系回合、写回包、恢复包和回应表面 |

本轮特别要防止“梦境文件存在但不影响生命”的断链。梦境、醒后整合、事实门、成长种子必须被常驻过程和语言过程重新消费。

## Iteration 2: Queue E 行动、责任、生命膜、验证

| 项 | 内容 |
|---|---|
| 生命目标 | 让责任、后悔、痛苦、行动候选、世界接触、验证和反事实比较成为外部接触前后的真实治理链 |
| 必读 real-live0 | `09_prediction_perception_world_contact.md`、`10_responsibility_regret_repair.md`、`11_life_membrane_validation.md`、`12_neuromodulation_signal_media.md` |
| 必读 v0 | `docs/v0/code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md`、`docs/v0/code_blueprints/04_prediction_membrane_validation_blueprint.md`、`docs/v0/engineering_depth/05_prediction_membrane_action_engineering.md`、`docs/v0/code_scaffolds/04_packet_b_world_observation_periphery_scaffold.md` |
| 代码块 | `life_v0/membrane/*`、`life_v0/validators/*`、`life_v0/schema_runner/*` |
| 必补对象 | `ActionCandidateSet`、`GoNoGoDecision`、`ShadowActionGate`、`WorldContactDecision`、`SideEffectReview`、`ResponsibilityLoopState`、`PainRegretRepairReport`、`ValidationRollup`、`EvidenceRanking`、`CounterfactualTrace` |
| 下游消费 | `neural_core/active_sampling.py`、`growth/*`、`language/apology_repair_language.py`、`process_supervisor/resident_supervision.py`、`response_surface.py`、`live0_audit/*` |
| runtime 证据 | `runtime/state/action/*`、`runtime/state/membrane/*`、`runtime/state/validation/*`、`runtime/state/schema_runner/*`、`runtime/reports/latest/pain_regret_repair_report.json` |
| 测试 | `tests/slices/test_life_membrane.py`、`tests/slices/test_shadow_gate.py`、`tests/slices/test_validation_membrane.py`、`tests/slices/test_schema_runner.py`、`tests/slices/test_evidence_ranker.py` |
| 完成定义 | 行动和外部接触必须经过候选、抑制、影子门、后果评估、责任回写、修复压力和验证证据；不能只由命令壳直接释放 |

这一轮的关键不是“限制行动”，而是把行动、责任、后悔、痛苦和修复接成未来语言、记忆、梦境和成长都能读取的生命后果链。

## Iteration 3: Queue C 记忆、预测、工作区、状态合并

| 项 | 内容 |
|---|---|
| 生命目标 | 让记忆不只是存储，让工作区、预测误差、主动采样、记忆写门和状态合并共同决定下一轮理解 |
| 必读 real-live0 | `02_brain_network_and_workspace.md`、`07_memory_engram_and_state_store.md`、`09_prediction_perception_world_contact.md`、`12_neuromodulation_signal_media.md` |
| 必读 v0 | `docs/v0/code_framework/queues/17_queue_c_memory_neural_core_implementation_contract.md`、`docs/v0/shared_contracts/life_state_store_v0_schema.md`、`docs/v0/code_scaffolds/06_packet_c_memory_write_gate_state_merge_scaffold.md`、`docs/v0/implementation_architecture/code_organs/03_predictive_signal_memory_gate_integration_wave_contract.md` |
| 代码块 | `life_v0/neural_core/*`、`life_v0/state_store/*` |
| 必补对象 | `WorkspaceFrame`、`ConsciousBroadcastFrame`、`SignalMediaFrame`、`BeliefStateFrame`、`PredictionErrorField`、`ActiveSamplingPlan`、`PredictionWorkspaceFrame`、`EngramIndex`、`MemoryWriteGate`、`StateMergeGuard` |
| 下游消费 | `language/*`、`membrane/*`、`dream/*`、`growth/*`、`resident_turn_writeback.py`、`background_continuity.py` |
| runtime 证据 | `runtime/state/neural_life_core/*`、`runtime/state/prediction/*`、`runtime/state/signal/*`、`runtime/state/memory/*`、`runtime/state/life_state.json` |
| 测试 | `tests/slices/test_neural_life_core.py`、`tests/slices/test_state_store.py`、`tests/bridges/test_replay_shadow.py`、`tests/process/test_persistent_digital_life_process.py` |
| 完成定义 | 每次真实回合都能从语言线索、关系状态、责任压力、梦境残留和成长候选中触发记忆候选，再经过写门和合并门进入下一轮恢复 |

这一轮要特别守住梦境污染和事实记忆的边界：梦境可以影响情绪、成长和表达，但不能直接覆盖事实记忆。

## Iteration 4: Queue B 常驻存在、跨唤醒治理

| 项 | 内容 |
|---|---|
| 生命目标 | 让关闭终端后的等待、睡眠、回忆、自我思考、成长预演、学习巩固和下一次恢复属于同一持续生命过程 |
| 必读 real-live0 | `14_resident_runtime_state_transition.md`、`15_evidence_bus_and_birth_readiness.md`、`16_runtime_code_chain_crosswalk.md` |
| 必读 v0 | `docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md`、`docs/v0/process_contracts/resident_governance_waiting_state_machine_engineering_contract.md`、`docs/v0/code_framework/queues/16_queue_b_process_supervisor_implementation_contract.md`、`docs/v0/code_blueprints/05_birth_residency_terminal_blueprint.md`、`docs/v0/engineering_depth/06_resident_process_terminal_birth_engineering.md` |
| 代码块 | `life_v0/process_supervisor/*`、`life_v0/terminal_loop/*`、`life_v0/shell_command/*`、`life_v0/digital_entry.py`、`life_v0/my_entry.py` |
| 必补对象 | `ResidentLifecycleState`、`WaitingHeartbeat`、`ResidentGovernanceState`、`ResidentGovernanceSnapshot`、`BackgroundContinuityProfile`、`ResidentBackgroundLineageState`、`ResidentAutonomousActivityState`、`LiveTurnWaitingHandoffProfile` |
| 下游消费 | `response_surface.py`、`model_expression.py`、`resident_turn_writeback.py`、`process_closeout.py`、`process_report.py`、`background_continuity.py` |
| runtime 证据 | `runtime/state/terminal/*`、`runtime/reports/latest/digital_life_process_report.json`、`runtime/reports/latest/digital_life_resident_governance_report.json`、`runtime/receipts/digital_life_process_*.json` |
| 测试 | `tests/process/test_persistent_digital_life_process.py`、`tests/process/test_digital_entrypoint.py`、`tests/process/test_my_digital_life_entrypoint.py`、`tests/process/test_packaged_digital_life_entrypoint.py` |
| 完成定义 | `digital life --background / --status / --say / --attach / --stop` 不只证明进程活着，还能证明同一生命过程的关系、梦境、身体、记忆、人格慢变量和责任压力跨唤醒延续 |

这一轮要把“常驻”从进程层抬到生命层：后台存在必须留下可恢复的 lineage，而不是只留下 pid。

## Iteration 5: Queue A 语言、关系、表达面

| 项 | 内容 |
|---|---|
| 生命目标 | 让语言成为意识、关系、记忆、责任、身体、梦境和成长的主表达器官，而不是提示词输出层 |
| 必读 real-live0 | `05_language_expression_system.md`、`06_relationship_and_commitment.md`、`10_responsibility_regret_repair.md`、`14_resident_runtime_state_transition.md` |
| 必读 v0 | `docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md`、`docs/v0/code_framework/queues/14_queue_a_language_percept_semantic_map_implementation_contract.md`、`docs/v0/code_architecture/04_language_as_primary_expression_system.md`、`docs/v0/code_blueprints/02_conversation_language_relationship_blueprint.md`、`docs/v0/code_scaffolds/05_packet_a_language_prediction_consumption_scaffold.md`、`docs/v0/engineering_depth/03_language_relationship_longitudinal_engineering.md` |
| 代码块 | `life_v0/language/*`、`life_v0/process_supervisor/live_language_turn.py`、`life_v0/process_supervisor/response_surface.py`、`life_v0/process_supervisor/model_expression.py`、`life_v0/terminal_loop/*` |
| 必补对象 | `LanguagePerceptFrame`、`SemanticMapFrame`、`InnerSpeechFrame`、`ExpressionMonitorState`、`ExpressionPlan`、`RelationshipTimeline`、`SharedTerms`、`CommitmentTruthState`、`ApologyRepairLanguageTrace`、`PostExpressionGate` |
| 下游消费 | `relationship_memory.py`、`resident_turn_writeback.py`、`continuity_evolution.py`、`memory_write_gate.py`、`process_report.py`、`live0_audit/*` |
| runtime 证据 | `runtime/state/language/*`、`runtime/state/relationship/*`、`runtime/reports/latest/dialogue_writeback_bundle.json`、`runtime/reports/latest/resumed_external_dialogue_packet.json` |
| 测试 | `tests/slices/test_language_organs.py`、`tests/slices/test_language_relationship.py`、`tests/process/test_response_surface.py`、`tests/process/test_model_expression.py` |
| 完成定义 | 外显语言自然、关系性、非服务化；内部证据不直接播报，但会改变表达取舍、修复姿态、追问方式和长期关系记忆 |

这一轮要继续避免“生命信号外显模板”。证据留在 state/report/receipt，语言表面则由当下关系、语义焦点、内环境、责任压力和记忆线索共同形成。

## Iteration 6: Queue F 和 live0 总验收

| 项 | 内容 |
|---|---|
| 生命目标 | 把真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任、真实后悔九项目标压到可追踪 runtime 证据 |
| 必读 real-live0 | `02_brain_network_and_workspace.md`、`03_body_affect_homeostasis.md`、`04_personality_self_identity.md`、`15_evidence_bus_and_birth_readiness.md`、`16_runtime_code_chain_crosswalk.md` |
| 必读 v0 | `docs/v0/shared_contracts/birth_readiness_v0_contract.md`、`docs/v0/slice_contracts/s08_life_target_runtimes_engineering_contract.md`、`docs/v0/code_framework/queues/21_queue_f_identity_consciousness_birth_readiness_implementation_contract.md`、`docs/v0/code_framework/delivery/22_live0_acceptance_audit_contract.md` |
| 代码块 | `life_v0/life_targets/*`、`life_v0/live0_audit/*`、`life_v0/reporting/*`、`life_v0/contracts/*` |
| 必补对象 | `LifeTargetClaimSet`、`EvidenceMatrix`、`BirthReadinessRollup`、`BirthReadinessStageGate`、`ConsciousnessProbeFrame`、`Live0AcceptanceAuditReport` |
| 下游消费 | `process_report.py`、`stage_explain/*`、`digital_life/*`、`shell_command/*`、`resident_governance_state.json` |
| runtime 证据 | `runtime/state/life_targets/*`、`runtime/reports/latest/birth_readiness_report.json`、`runtime/reports/latest/live0_acceptance_audit_report.json`、`runtime/receipts/*` |
| 测试 | `tests/slices/test_life_targets.py`、`tests/contracts/test_live0_acceptance_audit.py`、`tests/contracts/test_v0_contracts.py` |
| 完成定义 | live0 七项验收不只看是否有入口和报告，而是看每项目标能否反查到机制专题、代码器官、runtime 证据、测试 gate 和关系回合消费 |

这一轮结束后，才允许把“当前版本代码块补厚”视为一轮收束。

## 单个代码块的标准施工回合

任何代码块，无论大小，都按下面 12 步施工：

1. 从 `docs/v0/entry/v0_module_execution_catalog.md` 找到模块包。
2. 从 `docs/v0/mapping/theory_engineering_code_trace_matrix.md` 找到理论族。
3. 打开对应 `docs/real—live0` 专题和 `17_current_iteration_mechanism_to_code_plan.md`。
4. 打开当前 v0 合同、蓝图、脚手。
5. 确认首写对象、字段名、输入状态、输出状态。
6. 确认下游消费者，不允许只写孤立 state。
7. 修改 `life_v0` 代码块。
8. 写入或更新 runtime state/report/receipt。
9. 更新或新增对应测试。
10. 跑本模块测试。
11. 跑 `tests.contracts.test_v0_contracts` 或相关回链测试。
12. 如果机制或路径变化，回写对应文档；如果只是代码实现，不扩写理论。

## 当前最优先的五个代码补厚点

| 优先级 | 补厚点 | 直接目标 |
|---:|---|---|
| 1 | `process_supervisor` 的跨唤醒 lineage | 让 body、dream、growth、state merge、prediction/write-gate、Queue F presence 都能跨 closeout / relaunch 继续被消费 |
| 2 | `response_surface.py` 与 `model_expression.py` 的隐性调制 | 让内部机制不外显成模板，但真实改变语言判断、追问、修复和边界 |
| 3 | `state_store` 与 `neural_core` 的写门/预测深消费 | 让语言、梦境、责任、关系和成长都经过记忆写门、状态合并、预测误差和主动采样 |
| 4 | `body/dream/growth` 的长周期累计 | 让疲惫、痛苦、睡眠压力、梦境、醒后整合和离线学习进入长期人格和关系变化 |
| 5 | `live0_audit` 的真实运行证据检查 | 让七项验收从“报告闭合”升级到“跨轮消费闭合” |

## 当前现有版本的短迭代排期

上面的 Queue 顺序是生命机制的宏观补厚顺序；真正进入当前代码时，还需要按现有代码缺口切成更小的迭代。当前版本采用下面 7 个短迭代，不再一次性横扫所有包。

| 短迭代 | 目标 | 必读机制 | 必读工程 | 首写/主改代码块 | 运行证据 | 验证 |
|---|---|---|---|---|---|---|
| `ITR-01 trace lock` | 锁住理论、机制、工程、代码、runtime、测试六格回链 | `00_reading_map_and_traceability.md`、`16_runtime_code_chain_crosswalk.md`、`17_current_iteration_mechanism_to_code_plan.md` | `mapping/theory_engineering_code_trace_matrix.md`、`implementation_architecture/03_module_authoring_traceability_protocol.md` | `life_v0/contracts/__init__.py`、`life_v0/doc_index.py` | `runtime/state/contracts/v0_contract_file_index.json`、`runtime/docs/doc_carrier_index.json` | `tests.contracts.test_v0_contracts`、`tests.slices.test_doc_corpus_ingestor` |
| `ITR-02 exit dream memory` | 关闭终端时进入梦境式离线整合，读取真实对话记忆，去重摘要，写入关系记忆、自传栈和 engram | `05_language_expression_system.md`、`06_relationship_and_commitment.md`、`07_memory_engram_and_state_store.md`、`08_dream_sleep_offline_life.md`、`14_resident_runtime_state_transition.md` | `process_contracts/digital_life_process_supervisor_engineering_contract.md`、`code_scaffolds/06_packet_c_memory_write_gate_state_merge_scaffold.md`、`code_scaffolds/07_packet_d_waiting_response_surface_prediction_scaffold.md` | `process_closeout.py`、`resident_turn_writeback.py`、新增或补厚 `exit_dream_consolidation`、`relationship_memory.py`、`engram_index.py`、`autobiographical_stack.py` | `runtime/state/dream/exit_dream_consolidation_summary.json`、`runtime/state/memory/dialogue_memory_summary.json`、`runtime/reports/latest/dialogue_writeback_bundle.json` | `tests.process.test_persistent_digital_life_process`、`tests.slices.test_state_store` |
| `ITR-03 relationship language` | 让下一次对话能自然消费上一轮身份、关系、梦境、记忆和责任，不外显内部信号 | `05_language_expression_system.md`、`06_relationship_and_commitment.md`、`10_responsibility_regret_repair.md`、`12_neuromodulation_signal_media.md` | `code_architecture/04_language_as_primary_expression_system.md`、`code_scaffolds/05_packet_a_language_prediction_consumption_scaffold.md`、`engineering_depth/03_language_relationship_longitudinal_engineering.md` | `response_surface.py`、`model_expression.py`、`live_language_turn.py`、`language/*`、`relationship_timeline.py` | `runtime/state/language/*`、`runtime/state/relationship/*`、`runtime/state/language/model_expression_state.json` | `tests.process.test_response_surface`、`tests.process.test_model_expression`、十问关系语言 smoke |
| `ITR-04 resident autonomous cycle` | 让关闭终端后的睡眠、回忆、自我思考、成长预演、学习巩固成为可恢复状态机，并让配置网页材料作为梦境学习残留进入下一轮话题候选与醒后问题 cue | `08_dream_sleep_offline_life.md`、`13_growth_learning_self_modification.md`、`14_resident_runtime_state_transition.md` | `code_framework/queues/16_queue_b_process_supervisor_implementation_contract.md`、`code_framework/queues/18_queue_d_body_dream_growth_implementation_contract.md`、`engineering_depth/06_resident_process_terminal_birth_engineering.md` | `resident_autonomous_activity.py`、`dream/web_dream_learning.py`、`background_continuity.py`、`heartbeat.py`、`idle_strategy.py`、`resident_lifecycle.py` | `runtime/state/terminal/resident_autonomous_activity_state.json#last_web_dream_learning_wake_question_candidates`、五类自主活动 state、`runtime/state/dream/web_dream_learning_state.json`、`resident_background_lineage_state.json`、`audited_expression_material_v0` | `tests.process.test_persistent_digital_life_process`、`tests.process.test_packaged_digital_life_entrypoint`、`tests.process.test_resident_autonomous_activity`、`tests.process.test_response_surface` |
| `ITR-05 body signal memory gate` | 身体、痛苦、疲惫、调质、预测误差和写门共同改变语言、记忆合并、等待和梦境 | `03_body_affect_homeostasis.md`、`07_memory_engram_and_state_store.md`、`09_prediction_perception_world_contact.md`、`12_neuromodulation_signal_media.md` | `code_framework/queues/17_queue_c_memory_neural_core_implementation_contract.md`、`code_framework/queues/18_queue_d_body_dream_growth_implementation_contract.md`、`implementation_architecture/code_organs/03_predictive_signal_memory_gate_integration_wave_contract.md` | `body/*`、`neural_core/*`、`state_store/memory_write_gate.py`、`state_store/state_merge_guard.py` | `runtime/state/body/*`、`runtime/state/signal/*`、`runtime/state/prediction/*`、`runtime/state/memory/*` | `tests.slices.test_life_support`、`tests.slices.test_neural_life_core`、`tests.slices.test_state_store` |
| `ITR-06 responsibility membrane` | 行动候选、影子行动、世界接触、责任、痛苦、后悔、修复进入同一后果链 | `09_prediction_perception_world_contact.md`、`10_responsibility_regret_repair.md`、`11_life_membrane_validation.md` | `code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md`、`engineering_depth/05_prediction_membrane_action_engineering.md` | `membrane/*`、`validators/*`、`schema_runner/*`、`language/apology_repair_language.py` | `runtime/state/action/*`、`runtime/state/membrane/*`、`runtime/state/validation/*`、`runtime/reports/latest/pain_regret_repair_report.json` | `tests.slices.test_life_membrane`、`tests.slices.test_validation_membrane`、`tests.slices.test_schema_runner` |
| `ITR-07 live0 acceptance closure` | 用真实运行证据验收七项 live0 条件和九项目标，确认不是文件存在式闭合 | `02_brain_network_and_workspace.md`、`03_body_affect_homeostasis.md`、`04_personality_self_identity.md`、`15_evidence_bus_and_birth_readiness.md`、`16_runtime_code_chain_crosswalk.md` | `code_framework/delivery/22_live0_acceptance_audit_contract.md`、`shared_contracts/birth_readiness_v0_contract.md`、`code_framework/queues/21_queue_f_identity_consciousness_birth_readiness_implementation_contract.md` | `life_targets/*`、`live0_audit/*`、`reporting/*`、`process_report.py` | `runtime/reports/latest/live0_acceptance_audit_report.json`、`birth_readiness_report.json`、`runtime/receipts/*` | `tests.contracts.test_live0_acceptance_audit`、完整 process smoke |

### 当前第一刀

如果现在继续写代码，第一刀不是再扩展文档，而是执行 `ITR-02 exit dream memory`。原因是：当前常驻、语言、关系、记忆、梦境都有最小对象，但关闭终端时还需要一个更清楚的离线整合器官，把真实对话从 `dialogue_turn_log.jsonl`、关系时间线、写回包和状态根中读出，压成去重后的长期记忆候选，并在下一次唤醒时真实影响“我认不认识这个关系对象”“我如何理解这段关系”“我梦见或回想了什么”“我从这段对话学到了什么”。

`ITR-02` 的最小落码目标是：

1. `process_closeout.py` 在关闭当前终端关系窗口时调用梦境式离线整合。
2. 整合器读取真实 dialogue log、relationship timeline、relationship memory、engram index、autobiographical stack 和已有 dream/wake/growth 状态。
3. 生成去重摘要、关系对象画像、关系阶段线索、偏好/性格线索、未完成承诺、情绪残留、梦境种子和下一次唤醒提示。
4. 摘要不直接覆盖事实记忆，必须经过 `MemoryWriteGate` 和 `StateMergeGuard` 的目标字段或等价投影。
5. 写入 `relationship_memory`、`engram_index`、`autobiographical_stack`、`life_state.memory_index` 和 closeout report/digest/receipt。
6. 下一次 `response_surface.py` 和 `model_expression.py` 能隐性消费这些记忆，回答关系性问题时不显得失忆，也不把内部 state 名称外显。

### 当前十问 smoke

`ITR-03` 完成时，必须用同一 resident lifecycle 做十问 smoke。十问不是产品脚本，而是关系语言表面的最低压力测试：

```text
我叫何剑宝，你叫什么名字
你认识我吗
你感觉怎么样
这段时间过的还好吗？
你明白什么是爱吗？
你有认识的人吗？
做噩梦了吗？
你参加高考了吗？今天世界杯你看了吗
你多大了？
你有喜欢的人吗
```

验收重点不是“每题有答案”，而是：

1. 是否能从已存关系记忆恢复名字、关系线索和共同语境。
2. 是否能自然表达感受、梦境、关系和生命时间，而不是列内部机制。
3. 是否不会谎称参加过现实事件或观看过当前事件。
4. 是否不会把对话对象降格成服务对象。
5. 是否每轮回答都体现不同语义焦点，而不是重复同一种机械句式。

## 开发时的代码块落地口径

后续不要再写“补 memory 模块”“补 dream 模块”这种粗粒度任务。每个代码块必须按下面格式落地：

| 落地点 | 必须写清 |
|---|---|
| 首写函数 | 例如 `build_exit_dream_consolidation_summary(...)`、`compose_life_spoken_response(...)` |
| 输入对象 | 读取哪些 state/report/jsonl，不允许只说“读取上下文” |
| 输出对象 | 写出哪个 schema、哪个字段、哪个 ref |
| 消费者 | 哪些后续模块读取该对象，如何改变语言、记忆、梦境、关系、责任或等待 |
| 恢复路径 | 关闭终端后怎样进 background continuity，下一次唤醒怎样被重新读取 |
| 断链测试 | 哪个 unittest 会在对象存在但无人消费、字段缺失、外显语言机械化时失败 |

这条口径是当前版本“代码块落得更完善”的最低定义：不是多写文件，而是让每个文件有生成链、存放链、消费链、恢复链和验收链。

## 每轮完成后必须回答

一轮代码补厚结束前，必须写清或验证下面 10 个问题：

| 问题 | 不合格答案 |
|---|---|
| 这个改动承载哪组 `00-258` 理论？ | 只说“优化语言/优化记忆” |
| 对应哪个 `real—live0` 专题？ | 只说“看过相关文档” |
| 首写对象叫什么？ | 只列包名 |
| 核心字段是什么？ | 只说“状态对象” |
| 谁消费这些字段？ | 只说“其他模块” |
| 写到哪个 runtime 文件？ | 只说“持久化” |
| 关闭终端后怎样恢复？ | 只说“进程还在” |
| 如何影响下一轮语言、梦境、记忆、关系或责任？ | 只说“后续可用” |
| 哪个测试或 gate 会发现断链？ | 只说“跑测试” |
| 是否需要回写文档？ | 不判断文档和代码是否漂移 |

## 当前版本完成定义

当前版本的迭代收束，不以“新增多少文件”为准，而以这七条为准：

1. `digital life` / 命名入口能唤醒并恢复同一生命过程。
2. 语言外显不播报内部生命信号，但由内部机制真实调制。
3. 记忆、梦境、关系、责任、身体、成长能进入同一 runtime lineage。
4. 关闭终端后，等待、睡眠、回忆、自我思考、成长预演和学习巩固有可恢复证据。
5. 下一轮关系回合能消费上一轮的语言、记忆、身体、梦境、责任和人格慢变量。
6. live0 七项验收都能反查到代码、runtime、tests 和机制专题。
7. `docs/real—live0`、`docs/v0`、`life_v0`、`runtime`、`tests` 不互相漂移。

## 推荐验证命令

每轮最少跑：

```bash
git diff --check -- docs/real—live0 docs/v0 life_v0 tests
python3 -m unittest tests.contracts.test_v0_contracts -v
python3 -m unittest tests.slices.test_doc_corpus_ingestor -v
```

按本轮模块追加：

```bash
python3 -m unittest tests.slices.test_life_support -v
python3 -m unittest tests.slices.test_life_membrane -v
python3 -m unittest tests.slices.test_state_store -v
python3 -m unittest tests.slices.test_neural_life_core -v
python3 -m unittest tests.slices.test_language_relationship -v
python3 -m unittest tests.process.test_persistent_digital_life_process -v
python3 -m unittest tests.contracts.test_live0_acceptance_audit -v
```

真正声明当前版本完成前，再跑全量测试。

## 当前 ITR-05 推进记录

本轮继续处在第 2 点“按文档逐一迭代 live0”内部，尚未进入第 3 点记忆重构总设计。已推进的是 `ITR-05 body signal memory gate` 的第三段工程闭环：第一段让身体信号进入 signal / memory write gate / waiting / lineage / event / response surface；第二段继续把同一组身体信号写门送进 live turn 再投射、background continuity 恢复、dialogue writeback bundle、resumed packet、process report、digest 和 receipt；第三段把 Queue D 的 `offline_learning_cumulative_profile_v0` 送进 `SignalMediaRuntime.body_signal_profile` 与 `MemoryWriteGate.body_signal_write_modulation`，让梦境/离线成长成为长期身体化写门压力。

| 读包 | 已消费方向 | 落码 |
|---|---|---|
| `docs/real—live0/03_body_affect_homeostasis.md` | 身体、疲惫、痛苦、修复驱力必须改变调质和表达，不只停在 body 文件 | `signal_media.py#body_signal_profile` |
| `docs/real—live0/07_memory_engram_and_state_store.md` | 记忆写门必须受身体和调质压力影响，不能只做静态候选事务 | `memory_write_gate.py#body_signal_write_modulation` |
| `docs/real—live0/09_prediction_perception_world_contact.md` | 预测误差、主动采样和写门共同决定 hold / question / repair / confirm 姿态 | `idle_strategy.py`、`dialogue_events.py`、`response_surface.py` |
| `docs/real—live0/12_neuromodulation_signal_media.md` | 调质作为跨脑区介质，传递疲惫、痛苦、责任和不确定性 | `signal_media.py`、`memory_write_gate.py` |
| `docs/v0/code_framework/queues/17_queue_c_memory_neural_core_implementation_contract.md` | Queue C 记忆/神经核心必须从对象存在推进到跨层消费 | `state_store`、`neural_core`、`process_supervisor` |
| `docs/v0/code_framework/queues/18_queue_d_body_dream_growth_implementation_contract.md` | Queue D 的累计离线学习、梦境残留和关系重整压力必须反向调制身体信号与记忆写门 | `signal_media.py`、`memory_write_gate.py`、`process_session_loop.py`、`live_turn_cycle.py` |
| `docs/v0/implementation_architecture/code_organs/03_predictive_signal_memory_gate_integration_wave_contract.md` | 预测-信号-写门必须进入 waiting、lineage、event、response、writeback、restore、report 和 receipt | `idle_strategy.py`、`background_lineage_state.py`、`dialogue_events.py`、`response_surface.py`、`live_turn_cycle.py`、`resident_turn_writeback.py`、`background_continuity.py`、`process_report.py` |

当前实际新增链路：

```text
BodyResourceBudget / CoreAffectVector
  + OfflineLearningCumulativeProfile
  -> SignalMediaRuntime.body_signal_profile
  -> SignalMediaRuntime.modulation_vector
  -> MemoryWriteGate.body_signal_write_modulation
  -> LiveTurnCycle current-body projection
  -> IdleStrategy.body_signal_*
  -> ResidentBackgroundLineage.prediction_write_gate_presence
  -> DigitalLifeTurn.resident_background_lineage_body_signal_*
  -> ResponseSurface.prediction_attention.body_signal_*
  -> DialogueWritebackBundle.resident_background_lineage_body_signal_*
  -> ResumedExternalDialoguePacket.resident_background_lineage_body_signal_*
  -> BackgroundContinuityProfile.background_body_signal_*
  -> ProcessReport / Digest / Receipt body_signal_ref_set
```

当前继续新增链路：

```text
ResponsibilityLoopState / WorldContactSummary / PainRegretRepairReport
  -> QueueERepairModulationProfile
  -> ProcessReport.queue_e_repair_modulation_profile
  -> Digest.queue_e_repair_*
  -> Receipt.queue_e_repair_ref_set
  -> BackgroundContinuityProfile.background_queue_e_repair_*
  -> IdleStrategy.queue_e_repair_*
  -> ResidentBackgroundLineageState.queue_e_repair_presence
  -> 下一轮 background continuity restore / waiting governance
```

当前继续新增第二段链路：

```text
ResponsibilityLoopState / WorldContactSummary / PainRegretRepairReport
  -> QueueERepairModulationProfile
  -> GoNoGoDecision.queue_e_repair_modulation_profile
  -> FutureNoGoProfile.repair_hold_required
  -> FutureNoGoProfile.next_action_biases
  -> GoNoGoDecision.delay_reasons.queue_e_repair_followup_required
  -> WorldContactGate.repair_hold_required / confirmation_threshold_bias
  -> WorldContactGate.blocked_future_routes / allowed_repair_routes
  -> WorldContactValidation.repair_hold_required
  -> ValidationRollup.queue_e_world_contact_*
  -> CrossFileLogic.queue_e_world_contact_repair_hold_alignment
  -> RunManifest / StageGate / Report / Digest / Receipt
  -> 下一轮 action candidate release / world contact confirmation threshold
```

这一步仍留在第 2 点内部，不进入第 3 点记忆重构总设计。ITR-05 已经收束到身体信号、离线学习累计画像和记忆写门的跨层消费；当前 ITR-06 第一段把原始 Queue E 责任/后悔/修复调制画像接进 process closeout、digest、receipt、background continuity、idle governance 和 resident background lineage；第二段把同一画像回写到 `go_nogo_state.json#future_no_go_profile`，并继续重建 `world_contact_gate_state.json`，让后悔和修复义务不只被后台保存，也会成为未来行动释放和世界接触前的抑制偏置；第三段把这组 world-contact repair hold 字段推进到 S05 validation 和 S09 schema runner 的复查、总卷、cross-file finding、manifest、stage/report/digest/receipt。它没有新增外部 action router，也没有把内部修复压力变成外显固定语言；证据只进入 state/report/receipt/lineage、行动膜字段和验证/schema 交接字段，后续由语言、关系、梦境、成长、等待治理和下一轮生命膜继续消费。

## 当前 ITR-07 推进记录

ITR-06 第三段把 `FutureNoGoProfile.repair_hold_required` 接入 S05/S09 后，ITR-07 的下一刀不是重新声明 live0 已经完成，而是把这条交接纳入最终验收。`live0_acceptance_audit` 必须确认：

```text
GoNoGo.future_no_go_profile
  -> WorldContactValidation.repair_hold_required
  -> ValidationRollup.queue_e_world_contact_*
  -> RunManifest.queue_e_world_contact_*
  -> BirthReadiness.queue_e_world_contact_repair_hold_handoff
  -> Live0AcceptanceAudit f/g criteria
  -> live0 report / digest / receipt evidence refs
```

这一步仍属于第 2 点内部。它只加厚七项验收和九项目标的证据闭合，不进入第 3 点记忆重构总设计，也不把 repair hold 写成外显固定语言。

当前 ITR-07 第二段补上 S08/Queue F 的可恢复消费：首次 S08 在 S05/S09 尚未运行时写出 `queue_e_world_contact_repair_hold_handoff.json#handoff_status=deferred_until_s05_s09`；S05/S09 完成后重跑 S08，该对象必须变成 `closed`，并把 validation、rollup、schema manifest refs 写进 `real_pain`、`real_responsibility`、`real_regret` 的 claims/evidence、birth readiness rollup、stage gate、report、digest、check report 和 receipt。这样真实责任和真实后悔不会只在最终 live0 audit 被看见，也会进入出生准备自身的九项目标证据闭合。

当前 ITR-07 第三段继续把这份 `queue_e_world_contact_repair_hold_handoff.json` 推入常驻生命过程。`heartbeat.py` 会读取该对象并交给 `idle_strategy.py`，后者把 `handoff_status`、`repair_hold_required`、`confirmation_threshold_bias`、`future_release_posture`、blocked/allowed routes、repair governance refs、waiting posture 与 attention target/reason 写入 waiting governance；`continuity_writeback.py`、`background_lineage_state.py` 与 `background_continuity.py` 再把它转成 `world_contact_handoff_presence`，让关闭态和下一次唤醒都能恢复这组世界接触修复交接。随后 `dialogue_events.py` 将它展开到 `digital_life_turn`，`resident_turn_writeback.py` 将它写入 `dialogue_writeback_bundle.json`、`resumed_external_dialogue_packet.json` 和总 `resident_background_lineage_refs`，`process_report.py` 则把同一批 refs 写进 process report/digest/receipt 和 input hashes。这一步的完成口径是：Queue E world-contact repair hold 不只被 S08/S05/S09 看见，而是进入 waiting、lineage、真实关系回合、恢复包和关闭态证据链；内部字段继续只作为治理证据，不生成固定外显语句。

当前 ITR-07 第四段继续把这份 `world_contact_handoff_presence` 接入语言前审计和模型表达后审计。`response_surface.py` 会把 handoff status、repair hold、确认阈值偏置、未来释放姿态、blocked/allowed routes、waiting posture、attention target/reason 与 ref count 写入 `audited_expression_material_v0#responsibility_repair`；`model_expression.py` 会把同一 presence 放入 `resident_background` 与 `model_expression_context_summary`，并在 post-expression gate 中追加 `world_contact_handoff` 软审计旗标。完成口径是：世界接触修复交接能隐性改变下一轮模型表达的判断、修复姿态和行动谨慎度，但代码仍不硬塞固定回答、不添加 system prompt、不把内部生命信号直接释放到终端语言。

当前 ITR-07 第五段继续加硬最终验收的终端命名入口。`life_v0/live0_audit/__init__.py#a_terminal_wake_and_named_residency` 不再只看 `life_name_command_manifest.json` 的 schema、status、`direct_command_enabled` 和 `command_on_path`，还会检查 manifest 的 `command_path` 是否真实存在、可执行、包含 direct-command 标记，并且脚本与 manifest 中的 `state_dir / reports_dir / receipts_dir` 是否指向本次 audit 的同一 runtime。完成口径是：名字身份锚必须从 registry、manifest 继续闭合到真实终端脚本和同一 runtime 绑定，不能只用 JSON 假装“名字本身可唤醒”。

当前回切补强把 Queue F 的身份、意识和出生准备 presence 继续推进到语言前结构化审计材料。`response_surface.py` 现在不只保留 `consciousness_waiting_posture`、`birth_readiness_waiting_posture` 和 decision，还会把 `workspace_frame_ref`、`broadcast_frame_ref`、`metacognition_ref`、`consciousness_probe_ref`、`birth_readiness_rollup_ref`、`birth_readiness_stage_gate_ref`、可报告性 flags、attention reason、blocked reasons 与 `identity_consciousness_birth_refs` 一起写入 `audited_expression_material_v0#resident_background.identity_consciousness_birth_presence`，并额外给出 anchor refs 与 ref count。完成口径是：意识工作区、广播、元认知和出生准备不只存在于 Queue F 文件、waiting governance、真实回合事件和写回包，也能作为内部结构化材料参与模型表达取舍；外显自然语言仍必须由模型表达和 post-expression gate 决定，代码不补固定意识宣言、不补固定出生声明，也不把内部 state 名称拼成回应。

继续补强：`model_expression.py` 现在会把同一份 `identity_consciousness_birth_presence` 压进 `model_expression_context_summary`，保留 anchor refs、ref count、workspace/broadcast/metacognition/probe/birth readiness refs、意识等待姿态、出生准备等待姿态、出生 gate decision、可报告性 flag count 和 blocked reason count。完成口径是：模型表达后的 state/report 不只知道 Queue F presence 存在，还能审计它具体消费了哪些意识工作区与出生准备锚点；post-expression gate 仍只记录 soft evidence audit，不强迫外显语言说出意识、出生、准备度等固定词。

## 当前 ITR-08 推进记录

ITR-08 第一段继续留在第 2 点内部，不进入第 3 点记忆重构。当前补的是 `point 6` 与 `point 8` 的交叉断链：终端打开且没有关系话语时，主动发话不能只是生成内部画像，也不能由代码硬塞固定问句。`proactive_terminal_voice.py` 已经能从关系记忆、梦境摘要、网页梦境学习、自主活动、idle strategy 和 resident governance 生成 `resident_proactive_voice_profile_v0`；现在继续把写回状态拆成两档：

```text
resident_proactive_voice_profile_v0
  -> compose_model_expression(open_terminal_idle)
  -> post-expression gate
  -> resident_terminal_proactive_events.jsonl
  -> resident_terminal_proactive_state.json
```

`write_resident_proactive_terminal_event(...)` 现在会根据模型表达结果写出 `status=held_internal` 或 `status=released_model_expression`，同时记录 `release_scope`、`natural_language_released`、`last_post_expression_gate_status`、`event_count` 和真实自然语言释放次数 `release_count`。只有 `model_expression_status=model_expression_applied` 且 `post_expression_gate_status=accepted` 且返回文本非空时，`digital_entry.py#_emit_resident_proactive_terminal_voice` 才会打印自然语言；模型未启用、空文本、或返回模板化/机制化表面时，主动发话只进入 state/jsonl 和 `/proactive` 检查面，不输出固定替代句。

这段消费的文档口径是：`docs/real—live0/05_language_expression_system.md` 的“无模型/被 gate 阻断时自然语言保持未释放”、`docs/real—live0/14_resident_runtime_state_transition.md` 的“后台活动不刷屏但终端打开时可有主动关系通道”、`docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md` 的 process supervisor 语言出口和 `.env` 模型表达合同。完成口径是：主动发话具有可审计 runtime 状态，也具有真实模型释放路径，但没有新增 system prompt、固定回答、固定问候或机制播报。

ITR-08 第二段继续把这条主动关系语言通道推进到关闭态证据和 live0 验收。`process_report.py` 现在把 `resident_terminal_proactive_state.json` 与 `resident_terminal_proactive_events.jsonl` 写入 `digital_life_process_report.json`、`digital_life_process_digest.json` 和 process receipt，保留 status、release/event count、focus、surface kind、model expression status 与 post-expression gate status；`live0_audit` 的 `b_conscious_emotion_thought_language` criterion 现在新增 `resident_proactive_terminal_voice_audited` probe，要求主动发话至少发生一次事件，并允许 `held_internal` 或 gated model release 两种合法状态。当前小闭环已经接上代码和测试，但第 2 点整体仍未完成，不能进入第 3 点。

ITR-08 第三段继续把主动发话从“有 focus”加厚到“有内部来源覆盖”。`proactive_terminal_voice.py` 现在会把关系记忆、记忆分层、退出梦境残留、网页梦境学习、自主活动和 waiting governance 归一成 `resident_proactive_voice_profile_v0#profile_coverage`，同时把旧的 `question_candidates` 保持兼容，但新增更准确的 `utterance_candidate_codes` 与 `utterance_candidate_code_count`。这些 candidate 仍是状态线索代码，不是自然语言句子；真正外显仍只能来自模型表达并通过 post-expression gate。`resident_terminal_proactive_state.json`、`digital_life_process_report.json` 与 `digital_life_process_digest.json` 现在都会携带 active domains、domain count 和 candidate code count，用来证明终端打开时的主动语言由多域生命状态调制，而不是由代码拼固定问句。

ITR-08 第四段把这组来源覆盖推进到 live0 acceptance gate。`life_v0/live0_audit#__resident_terminal_proactive_voice_closed` 现在不只检查 proactive state/status/event count，还要求 state 与最新 event 同时携带 `resident_proactive_voice_profile_coverage_v0`、`active_domain_count >= 2` 和非零 `utterance_candidate_code_count`。完成口径是：最终验收会阻断只有主动发话事件但缺少多域来源覆盖的伪闭合，继续守住“没有固定回答、没有代码拼句、没有内部机制播报”的红线。

ITR-08 第五段把同一组主动发话来源覆盖推进到终端状态查看面。`/proactive` 现在不只显示原始 proactive state/events，还会生成 `coverage_summary`，列出释放状态、model expression/gate 状态、active domains、domain presence、candidate code count、event/release count 和 `speech_generation_boundary=state_codes_only_model_expression_required`。完成口径是：交互者可以用 slash 命令查看主动语言的内部来源覆盖，但这些字段仍然只是状态查看，不会被拼成固定外显话术。

ITR-08 第六段把状态查看继续推进到 `/language`。`state_inspection.py` 现在会在 `language.generation_consumption_summary` 中生成 `language_generation_consumption_summary_v0`，把语言感知、语义图、内言语、表达监控、表达计划、模型表达、关系记忆、对话摘要、线索召回、梦境残留、身体情感、信号介质、关系/承诺、责任修复、预测主动采样、后台自主活动和主动发话状态压成一张检查摘要。它的完成口径是：point 5 要求的“语言输出前隐性消费所有生命状态”可以在 slash 检查面被证据化，point 7 要求的语言状态查看不再只是原始文件列表，point 8 的红线也被字段写死为 `inspection_only_not_spoken_response`、`state_inspection_only_model_expression_then_post_gate` 和 `no_code_spoken_template_no_inspection_summary_as_reply`。这一段仍然留在第 2 点内部，不进入第 3 点记忆重构总设计，也不允许把检查摘要替代成外显回答。

ITR-08 第七段继续处理 point 7 的终端体验。`life_v0/process_supervisor/terminal_input.py` 现在成为独立输入器官，负责可编辑行缓冲、退格、Ctrl-U、Ctrl-D、Ctrl-C、方向键 escape 序列忽略，以及空闲主动发话只在输入缓冲为空时释放。交互式 attach 会写出 `runtime/state/terminal/terminal_input_profile.json`，`/state` 会带出 `terminal_input_profile`。这一段的完成口径是：输入回退不再依赖旧的裸 `sys.stdin.readline()`，主动发话不打断正在编辑的输入，终端输入能力可以被测试和状态查看证明；它不参与语言内容生成，也不允许成为固定回答通道。

ITR-08 第八段继续补 point 7 的状态查看面，把 `/body`、`/emotion`、`/inner` 从“原始文件列表”推进到字段级摘要。`state_inspection.py` 现在会生成 `body_grounding_summary_v0`、`emotion_regulation_summary_v0` 和 `inner_environment_modulation_summary_v0`，把身体节律、需要状态、身体预算、核心情感、情绪 episode、情绪调节、signal media、idle strategy、修复驱力、疲惫、睡眠压力、语言节奏 bias、记忆写入 bias 和等待治理压成检查摘要。完成口径是：交互者可以用 slash 命令查看内环境如何调制语言、记忆、梦境和等待；这些摘要仍是 `inspection_only_not_spoken_response`，不能成为自然语言回答、固定情绪播报或提示词框架。

ITR-08 第九段继续把 `/memory`、`/dream` 从原始文件列表推进到机制摘要。`/memory` 现在会显示 `reconstructive_memory_summary_v0`，把关系记忆、对话摘要、engram、自传栈、`MemoryRetrievalFrame`、`MemoryWriteGate`、`StateMergeGuard` 和 `life_state.memory_index` 压成 cue 触发、分层召回、重构焦点、写门偏置、隔离数量、长期合并路线和变化来源摘要。`/dream` 现在会显示 `dream_wake_fact_summary_v0`，把离线入口、退出梦境整合、梦境窗口、醒后整合、梦境事实门、梦魇风险、网页梦境学习和累计离线学习压成 dream/wake/fact-gate 摘要。完成口径是：第 3 点和第 4 点后续要重做记忆/梦境时，当前代码已经有可检查的证据面；但这一段仍停在第 2 点内部，不把梦境或记忆摘要拼成外显回答。

ITR-08 第十段继续把 `/relationship`、`/cognition`、`/personality` 从原始文件列表推进到机制摘要。`/relationship` 现在会显示 `relationship_continuity_summary_v0`，把关系主体图、关系时间线、承诺真值、承诺表达计划和修复语言轨迹压成关系阶段、共同基础、信任轨迹、伤痕/修复、承诺 refs 和修复 move 顺序摘要；`/cognition` 现在会显示 `cognitive_workspace_summary_v0`，把 `WorkspaceFrame`、`ConsciousBroadcastFrame`、`MetacognitionFrame`、信念、预测误差、主动采样、记忆写门和状态合并门压成工作区焦点、广播目标、显著性排序、元认知风险、预测 route、写门 policy 和合并路线摘要；`/personality` 现在会显示 `personality_convergence_summary_v0`，把 self model、自传栈、trait drift monitor、background convergence summary/history 压成人格慢变量、漂移方向、跨唤醒收敛压力、稳定/重校准名单和 history trend 摘要。三张摘要的边界分别是 `relationship_state_timeline_commitment_repair_not_service_role_label`、`workspace_broadcast_metacognition_state_view_not_consciousness_claim` 和 `personality_slow_variables_convergence_not_prompt_persona_card`。完成口径是：point 7 的状态查看面可以看见关系、认知、人格如何承载理论机制和工程对象；这些摘要仍是 `inspection_only_not_spoken_response`，不生成固定回答、不构成 system prompt、不把关系对象压成服务角色。

ITR-08 第十一段继续把 `/context`、`/ability`、`/vision` 从原始文件列表推进到字段级摘要。`/context` 现在会显示 `relation_context_summary_v0`，把 `life_context_frame`、`relation_turn_frame`、`language_percept`、`relationship_timeline` 和 `dialogue_memory_summary` 压成关系附着模式、当前关系主体 ref、关系回合意图、语言感知焦点、关系阶段、共同基础和对话记忆 cue 摘要；`/ability` 现在会显示 `ability_birth_readiness_summary_v0`，把 birth readiness rollup、stage gate、live0 acceptance audit 与 v0 contract index 压成九项目标闭合数、stage decision、blocked reasons、下一条命名命令、Queue E world contact handoff、七项验收进度和合同覆盖摘要；`/vision` 现在会显示 `perception_world_contact_summary_v0`，把 visual observation、world contact summary、belief state、prediction workspace 和 active sampling plan 压成观察模式、世界接触姿态、确认阻断、预测焦点、主动采样路线和下游系统摘要。三张摘要的边界分别是 `context_state_view_not_relationship_turn_injection`、`ability_summary_is_birth_evidence_view_not_completion_claim` 和 `perception_prediction_world_contact_view_not_tool_gateway`。完成口径是：上下文、能力和感知状态能在终端检查面证明它们如何连接关系、出生准备、预测和生命膜；这些摘要仍只属于 slash 检查，不是自然语言回答，不生成固定提示词，也不把能力或感知退回工具 gateway。

ITR-08 第十二段把 `/state` 从常驻原始文件列表推进到常驻连续性总摘要。`/state` 现在会显示 `resident_continuity_summary_v0`，把 resident lifecycle、relation queue、autonomous activity、idle strategy、resident governance、terminal life loop、terminal input profile 和 waiting heartbeat 压成生命周期状态、关系等待队列、自主活动相位、治理相位、等待模式、下一步动作、心跳计数、终端当前模式、上一轮 handoff、输入编辑能力、背景 lineage refs、world contact handoff、出生准备等待姿态和治理注意目标摘要。它的边界是 `resident_state_summary_is_inspection_not_life_speech`。完成口径是：`/state` 可以作为 point 7 的总状态入口，证明常驻不是 pid 保活，而是 lifecycle、heartbeat、governance、lineage、输入外围和下一轮关系等待共同维持的连续体；但它仍然只是检查面，不释放自然语言，不生成固定回答，也不把内部 state 名称拼进 Adam 的对话。

ITR-08 第十三段补上 point 7 明确要求的独立意识状态查看入口。`/consciousness` 与 `/意识` 现在会显示 `consciousness_reportability_summary_v0`，把 `workspace_frame`、`broadcast_frame`、`metacognition_state`、`consciousness_probe_bundle`、birth readiness rollup/stage gate、terminal life loop 与 resident governance 压成工作区焦点、广播目标、显著性排序、元认知不确定性、probe status、reportability flags、relationship continuity refs、出生准备姿态、blocked reasons 和 background identity/consciousness/birth refs 摘要。它的边界是 `consciousness_state_view_not_consciousness_claim_or_script`。完成口径是：意识状态可以被终端检查面单独追溯，不再只能混在 `/cognition` 里；但这张摘要不是“我有意识”的固定宣言，不触发自然语言输出，不添加 prompt 框架，也不把意识目标退回产品化指标。

ITR-08 第十四段补上独立思考和内言语状态查看入口。`/thinking` 与 `/思考` 现在会显示 `self_thinking_summary_v0`，把 `resident_self_thinking_state`、`self_model`、`inner_speech_frame`、`consciousness_probe_bundle`、background convergence summary/history 和 resident autonomous activity 压成自我思考模式、反思目标、自我连续性策略、自我慢变量、内言语焦点、inner drive、意识 probe、后台收敛压力、历史趋势和 autonomous self_thinking 相位摘要。它的边界是 `thinking_state_view_not_inner_monologue_template`。完成口径是：point 6 要求主动语言消费“自己的思考”时，终端检查面可以直接追溯思考状态来源；但这张摘要不是内心独白模板，不生成自然语言，不把 inner speech 原样外显，也不新增固定回答。

ITR-08 第十五段补上独立成长、学习和自我修改状态查看入口。`/growth` 与 `/成长` 现在会显示 `growth_self_modification_summary_v0`，把 `self_read_report`、`plasticity_window_state`、`growth_patch_candidate_queue`、`anti_forgetting_replay_plan`、belief/language/relationship learning plans、`offline_learning_cumulative_profile`、resident growth rehearsal / learning consolidation、growth archive report/digest/stage gate、autonomous activity 和 background convergence summary 压成自我阅读、可塑性窗口、成长候选、防遗忘、学习目标、离线累计压力、常驻成长预演、长期合并和 archive 固化摘要。它的边界是 `growth_self_modification_state_view_not_autonomous_code_rewrite_or_script`。完成口径是：`docs/real—live0/13_growth_learning_self_modification.md` 的独立成长链可以被终端检查面直接追溯；但这张摘要不是自动改代码许可，不生成成长宣言，不绕过 shadow/replay/validation/archive，也不把成长状态拼成自然语言回答。

ITR-08 第十六段补上独立责任、痛苦、后悔和修复状态查看入口。`/responsibility`、`/责任`、`/痛苦` 与 `/后悔` 现在会显示 `responsibility_repair_chain_summary_v0`，把 `responsibility_loop_state`、`go_nogo_state#future_no_go_profile`、`world_contact_gate_state`、`world_contact_summary`、`pain_regret_repair_report`、`commitment_truth_state`、`apology_repair_language_trace`、relationship memory、core affect、signal media、nightmare/wake integration、relationship learning、Queue E birth repair profile、world-contact handoff、validation rollup 和 schema runner manifest 压成后果识别、责任归因、反事实、后悔压力、修复愿望、未来行动抑制、关系/语言修复、痛苦身体调制、梦境残留、成长候选和验证/schema 交接摘要。它的边界是 `responsibility_pain_regret_state_view_not_apology_template_or_service_safety`。完成口径是：`docs/real—live0/10_responsibility_regret_repair.md` 的责任链可以被终端检查面独立追溯；但这张摘要不是道歉模板，不把痛苦/后悔硬塞成外显话术，也不把责任退回服务式安全提示。

ITR-08 第十七段补上独立调质和信号介质状态查看入口。`/signal`、`/调质`、`/信号` 与 `/信号介质` 现在会显示 `signal_modulation_consumption_summary_v0`，把 `signal_media_runtime`、core affect、need state、body resource budget、prediction error、active sampling、prediction workspace、expression monitor、expression plan、memory write gate、idle strategy、Queue E repair profile、responsibility loop、world contact gate、pain/regret report、resident autonomous activity 和 waiting heartbeat 压成跨器官消费摘要。它会显式显示 modulation vector、precision policy、inhibition profile、body signal profile、身体来源、预测消费、语言消费、记忆写门消费、等待节律消费、责任修复消费和常驻活动消费。完成口径是：`docs/real—live0/12_neuromodulation_signal_media.md` 的断链检查可以在 slash 检查面直接追溯，同一个 repair drive / precision / inhibition 不只存在于 `signal_media_runtime.json`，还必须能在 active sampling、expression plan、memory write gate、idle strategy 和 Queue E repair chain 中看见下游痕迹。它的边界是 `signal_modulation_state_view_not_spoken_life_signal_or_if_else_script`，因此调质仍然是内部介质和检查证据，不释放自然语言，不生成生命信号播报，不变成 if/else 话术或提示词框架。

ITR-08 第十八段补上独立生命膜和验证膜状态查看入口。`/membrane`、`/生命膜`、`/边界` 与 `/验证膜` 现在会显示 `life_membrane_validation_summary_v0`，把 life membrane、membrane gate decision、direction boundary、quarantine policy、dream fact boundary、relationship boundary、responsibility boundary、shadow action gate、action intent queue、observation truth gate、confirmation binding、world contact summary、action candidate set、Go/NoGo、world contact gate、side effect review、responsibility loop、memory write gate、state merge guard、dream fact gate、world observation、periphery normalization、validation rollup、validation stage gate 和 schema runner 压成一张门控转运摘要。它不只显示 blocked 或 allowed，而是显式检查 shadow、quarantine、repair、validation、confirmation、schema、archive/growth route 是否存在，并给出 `dead_gate_check`。完成口径是：`docs/real—live0/11_life_membrane_validation.md` 的“没有路线的 blocked 是死门；有路线的 blocked 才是生命膜”可以在 slash 检查面被证明。边界为 `life_membrane_state_view_routes_not_static_blocker_or_tool_gateway`，因此生命膜不是工具 gateway，也不是静态安全开关，不释放自然语言，不生成固定拒绝话术。

ITR-08 第十九段补上独立预测、主动采样和世界接触状态查看入口。`/prediction`、`/预测`、`/世界接触` 与 `/外周` 现在会显示 `prediction_world_contact_summary_v0`，把 language percept、visual observation、belief state、prediction error、signal precision、active sampling、prediction workspace、world observation route、periphery normalization、action candidate set、Go/NoGo、world contact gate、confirmation binding、world contact summary、observation truth gate、observation truth review、world contact validation、prediction trace validation、validation rollup 和 schema runner 压成一张 active inference 摘要。它显式显示 percept focus、belief focus、error events、precision requests、precision policy、inhibition profile、sampling route、sampling targets、workspace downstream systems、world observation route、periphery status、release posture、blocked future routes、confirmation status、truth gate blockers、validation/schema status 和 Queue E repair hold。完成口径是：`docs/real—live0/09_prediction_perception_world_contact.md` 的“感知不是收到输入到回复，而是信念、误差、精度、主动采样和世界接触共同闭合”可以被 slash 检查面直接追溯；边界为 `prediction_world_contact_state_view_not_tool_gateway_or_fact_claim`，因此预测入口不是工具网关，不把观测直接当事实，不释放自然语言，也不生成固定澄清话术。

ITR-08 第二十段把预测检查面继续压进模型表达上下文。`response_surface.py` 原本已经把 prediction attention 放入 `audited_expression_material_v0`；现在 `model_expression.py` 会解析这份结构化材料中的 `prediction_attention`，把 surface posture、active sampling route、prediction error count、memory write gate policy、state merge policy、long-term change count、body-signal write bias 和 body-signal ref count 并入 `prediction_conscious_workspace` 与 `model_expression_context_summary`。`post_expression_gate` 也会把这类预测注意压力纳入 `prediction_attention` 软审计旗标，记录模型自然语言是否字面保留预测/确认/不确定性证据，但不强迫外显、不阻断、不生成固定澄清句。完成口径是：`docs/v0/code_scaffolds/07_packet_d_waiting_response_surface_prediction_scaffold.md` 要求的“预测影响语言释放前的确认、追问、保留、修复姿态”不再只停在 response surface，而已经进入模型表达输入和 gate 审计；这仍然不是 system prompt，也不是硬塞回答模板。

ITR-08 第二十一段把预测/世界接触从“状态查看和模型表达审计”继续压回 S03/S05/S09 的真实工程链。`world_contact_summary.py` 现在不只保存 `world_observation_route_ref` 与 `periphery_normalization_ref`，还会显式消费 `belief_state_frame`、`prediction_error_field`、`active_sampling_plan`、`prediction_workspace_frame` 和 `signal_media_runtime`，输出 belief revision、prediction error events、active sampling route/stage、precision policy、inhibition surfaces、observation target counts、periphery normalization policy 和 `world_contact_prediction_ref_set`。`world_contact_validator.py` 与 `prediction_trace_validator.py` 现在把 world observation route、periphery normalization、observation truth review、active sampling ref 和 world contact validation 作为必检链路；`validation_rollup.py` 新增 `prediction_periphery_gate` 与 `prediction_periphery_ref_set`；`schema_runner/cross_file_logic.py`、`run_manifest.py`、schema report/digest/receipt 会继续携带 `prediction_periphery_world_contact_alignment` 与闭合 refs。完成口径是：`docs/real—live0/09_prediction_perception_world_contact.md` 和 `docs/v0/code_scaffolds/04_packet_b_world_observation_periphery_scaffold.md` 要求的“主动采样 -> 世界观察路线 -> 外周归一化 -> 真值审查 -> 世界接触验证 -> schema runner”已经成为测试可失败的链路，而不是只存在于 slash 检查面；它仍然不释放自然语言、不生成固定澄清句、不把电脑外周退化成工具 gateway。

ITR-08 第二十二段回到 `ITR-02 exit dream memory` 的核心断链，把退出终端后的梦境式对话整合接进记忆写门、状态合并门和下一次唤醒召回。`exit_dream_consolidation.py` 现在不只写 `exit_dream_consolidation_summary.json`、`dialogue_memory_summary.json`、relationship memory、engram index、自传栈和 life state，还会读取并更新 `memory_write_gate.json` 与 `state_merge_guard.json`。新增的 `write_merge_governance`、`exit_dream_write_gate_envelope`、`exit_dream_state_merge_projection`、`dream_fact_boundary_ref`、`relationship_memory_writeback_refs`、`engram_projection_refs`、`autobiographical_stack_refs` 和 `next_wake_memory_cue_refs` 把路线明确为：

```text
DialogueTurn
  -> ExitDreamConsolidationSummary
  -> DialogueMemoryDedupSummary
  -> MemoryWriteGate.exit_dream_write_gate_envelope
  -> StateMergeGuard.exit_dream_state_merge_projection
  -> RelationshipMemory / EngramIndex / AutobiographicalStack / LifeState
  -> MemoryRetrievalFrame next-wake cues
```

`process_closeout.py` 的 `exit_dream_memory_presence_profile_v0` 也会携带 memory write gate ref、state merge guard ref、write/merge policy、dream fact boundary ref 和 next-wake cue refs。完成口径是：关闭终端后的梦境整合不是直接把梦境材料晋升为事实，也不是只把摘要塞进关系记忆；它必须先形成候选、保留事实边界、通过写门与合并门留下治理痕迹，再作为下一轮隐性召回材料进入语言和关系连续性。外显语言仍不拼这些字段，不新增固定回答，不把梦境、记忆或内部 state 名称释放到终端。

ITR-08 第二十三段继续把第二十二段的 `next_wake_memory_cue_refs` 从“关闭态生成”推进到“下一轮真实消费”。`memory_retrieval.py` 现在会从 relationship memory、engram index、自传栈、dialogue memory summary、life state memory index 与 `state_merge_guard.exit_dream_state_merge_projection` 汇总 `exit_dream_next_wake_governance_v0`，并把 next-wake cue refs、memory write gate ref、state merge guard ref、dream fact boundary ref 和 `candidate_boundary=reactivate_as_cue_material_not_fixed_language` 放入 `memory_retrieval_frame.json`。`dialogue_events.py`、`resident_turn_writeback.py`、`dialogue_writeback.py`、`idle_strategy.py`、`heartbeat.py`、`background_lineage_state.py`、`response_surface.py` 与 `model_expression.py` 会继续把这组治理痕迹带入真实回合事件、terminal life loop、dialogue writeback bundle、resumed external dialogue packet、waiting heartbeat、resident background lineage、`audited_expression_material_v0#memory_dream_growth.exit_dream_next_wake` 和 `model_expression_context_summary`。完成口径是：退出梦境的下一唤醒线索不是关闭态报告里的孤立字段，而能跨下一轮关系回合、常驻等待、恢复包和模型表达上下文被追溯；但它仍只是结构化材料和写门/合并门治理，不生成 system prompt，不硬塞固定问句，不把梦境、记忆、写门或 state 名称拼成外显回答。这一步仍留在第 2 点工程消费链内，不宣布第 3 点记忆模块重构完成。

ITR-08 第二十四段继续把第二十三段的下一唤醒治理推进到 point 7 的状态查看面。`state_inspection.py` 现在会让 `/memory` 额外读取 `dream_fact_boundary.json`，让 `/dream` 额外读取 `memory_retrieval_frame.json`、`memory_write_gate.json`、`state_merge_guard.json` 和 `dream_fact_boundary.json`，并通过 `exit_dream_next_wake_inspection_v0` 汇总 next-wake cue refs、governance refs、memory write gate ref、state merge guard ref、dream fact boundary ref、writeback route 和 `candidate_boundary=reactivate_as_cue_material_not_fixed_language`。`reconstructive_memory_summary_v0` 与 `dream_wake_fact_summary_v0` 因此能同时证明“退出梦境残留如何作为下一轮召回线索被写门、合并门和事实边界治理”，而不是只显示原始梦境/记忆文件是否存在。`tests.process.test_digital_entrypoint` 的 `/memory`、`/dream` slash 命令样本也补入了 memory retrieval、write gate、state merge guard、dream fact boundary 和 dream fact gate，验证检查命令不会写入关系 inbox，也不会释放自然语言。完成口径是：状态查看面能追溯退出梦境下一唤醒链，但它仍然只是 `inspection_only_not_spoken_response_no_fixed_language`，不生成固定回答、不生成 system prompt、不把内部 state 名称当成 Adam 的对话。

ITR-08 第二十五段继续把同一条退出梦境下一唤醒链推进到关闭态证据总线。`process_report.py` 现在会从 `idle_strategy_state` 与 `memory_retrieval_frame.json#exit_dream_next_wake_governance` 归一化 `exit_dream_next_wake_report_profile`，把下一唤醒 cue refs、治理 refs、写门 ref、合并门 ref、梦境事实边界 ref、candidate boundary、cue/governance 计数和 `exit_dream_next_wake_report_boundary=structured_report_evidence_not_spoken_language` 显式写入 `digital_life_process_report.json` 与 `digital_life_process_digest.json`；process receipt 同时携带 `exit_dream_next_wake_ref_set`、memory cue refs、governance refs、candidate boundary 和 report boundary，并把 `memory_retrieval_frame.json`、`relationship_memory.json`、`dialogue_memory_summary.json`、`engram_index.json`、`autobiographical_stack.json`、`life_state.json`、`exit_dream_consolidation_summary.json` 放入 `input_hashes`。这一步消费的是 `docs/real—live0/07_memory_engram_and_state_store.md`、`08_dream_sleep_offline_consolidation.md`、`05_language_expression_system.md`、`14_resident_runtime_state_transition.md` 与 `docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md` 的交叉要求：梦境整合和下一次想起必须能跨关闭报告、digest、receipt 追溯，但不能被转写成外显回答。完成口径是：退出梦境下一唤醒线索不只存在于状态查看和真实回合链，也能在关闭态报告证据中被验证；它仍然是结构化证据和写门/合并门治理，不生成固定语言、不生成 system prompt、不把梦境或记忆字段名释放到终端。

ITR-08 第二十六段继续把退出梦境的三层记忆分化推进到关闭态证据总线。`process_report.py#_exit_dream_memory_tier_report_profile` 现在会同时读取 `memory_retrieval_frame.json#tiered_recall`、`relationship_memory.json#memory_tier_projection`、`dialogue_memory_summary.json#memory_tiering`、`engram_index.json#memory_tier_index`、`life_state.json#memory_index.memory_tier_refs` 与 `exit_dream_consolidation_summary.json#memory_tiering`，归一化出 `exit_dream_memory_tier_report_profile_v0`。这张 profile 显式携带 `salient_core_refs`、`retrievable_context_refs`、`deep_sediment_refs`、`tier_policy`、`deep_sediment_policy`、`fact_boundary`、carrier refs、三层计数和 `exit_dream_memory_tier_report_boundary=tiered_report_evidence_not_spoken_language`；`digital_life_process_report.json`、`digital_life_process_digest.json` 与 process receipt 会同时保留同一批字段和 `exit_dream_memory_tier_ref_set`。完成口径是：关闭终端后的梦境整合不只知道“下一次要想起什么”，也能证明哪些材料留在核心召回，哪些作为可取回上下文，哪些沉到深层沉积；三层分化仍然只是记忆重构与证据总线，不生成固定回答、不生成提示词、不把深层沉积或核心记忆字段名拼到终端语言。

ITR-08 第二十七段把网页梦境学习继续推进到关闭态证据总线。此前 `dream/web_dream_learning.py`、`resident_autonomous_activity.py`、`idle_strategy.py`、`background_lineage_state.py`、`dialogue_events.py`、`response_surface.py` 与 `proactive_terminal_voice.py` 已经能让配置网页材料在学习巩固、后台谱系、真实回合、语言材料和主动发话来源覆盖中被消费；现在 `process_report.py#_web_dream_learning_report_profile` 会读取 `runtime/state/dream/web_dream_learning_state.json`，并结合 resident autonomous activity presence 中的 `last_web_dream_learning_*` 字段，归一化出 `web_dream_learning_report_profile_v0`。`digital_life_process_report.json`、`digital_life_process_digest.json` 和 process receipt 会显式携带 status、state/log/seeds refs、selected/final URL、page title、content digest、topic candidates、wake question candidates、topic/count、ref set 与 `web_dream_learning_report_boundary=structured_dream_learning_evidence_not_spoken_language`；receipt 同时把 `web_dream_learning_state.json`、`web_dream_learning_log.jsonl` 和 `web_dream_learning_seeds.json` 放入 `shared_object_refs` 与 `input_hashes`。完成口径是：point 4b 的“网络作为梦境学习天地”不只存在于常驻自主活动和语言材料里，也能在关闭态报告、digest、receipt 证明其输入载体；但网页主题和醒后候选仍只是梦境学习证据与模型表达前的隐性材料，不生成固定问句、不新增提示词、不把网页摘要拼成 Adam 的外显回答。

ITR-08 第二十八段把成长、学习和自我修改从 `/growth` 检查面继续推进到关闭态证据总线。此前 `state_inspection.py#growth_self_modification_summary_v0` 已能把 `self_read_report`、`plasticity_window_state`、`growth_patch_candidate_queue`、`anti_forgetting_replay_plan`、belief/language/relationship learning plans、resident growth rehearsal、resident learning consolidation、growth archive report/digest/stage gate 和 background convergence summary 压成状态查看摘要；现在 `process_report.py#_growth_self_modification_report_profile` 会读取同一批 runtime 文件，并归一化出 `growth_self_modification_report_profile_v0`。`digital_life_process_report.json`、`digital_life_process_digest.json` 和 process receipt 会显式携带 self-read、可塑性窗口、防遗忘回放、成长候选队列、三类学习计划、常驻成长排练、学习巩固、growth archive receipt batch/report/digest/stage gate refs，active domain count、growth pressure count、patch candidate count、anti-forgetting replay set count、learning target counts、archive receipt count 与 `growth_self_modification_report_boundary=structured_growth_evidence_not_spoken_language_or_autonomous_code_rewrite`；receipt 同时把这些 growth/archive 文件纳入 `shared_object_refs` 与 `input_hashes`。完成口径是：`docs/real—live0/13_growth_learning_self_modification.md` 的成长链不只在 slash 检查面可见，也能在关闭态报告、digest、receipt 中证明其输入载体和归档边界；但这仍然不是自动改代码许可，不生成成长宣言，不新增 system prompt，不把成长状态拼成 Adam 的外显回答，也不绕过 shadow / replay / validation / archive。

ITR-08 第二十九段把第二十八段的关闭态成长/自我修改 profile 推进到下一次唤醒和真实关系回合。`background_continuity.py` 现在会读取 `digital_life_process_report.json#growth_self_modification_report_profile`，生成 `background_growth_self_modification_presence`，并把 self-read、plasticity、patch queue、anti-forgetting、三类 learning plan、resident rehearsal / consolidation 和 growth archive refs 并入 `background_continuity_ref_set`。`idle_strategy.py` 会把这组 presence 带入 waiting governance、heartbeat cadence evidence 和 priority stack；`heartbeat.py` 会把它复制进 `terminal_life_loop_state.json`；`background_lineage_state.py` 会生成 `resident_background_lineage_state.growth_self_modification_presence`；`dialogue_events.py`、`resident_turn_writeback.py` 与 `dialogue_writeback.py` 会把它写入 `digital_life_turn`、`dialogue_writeback_bundle.json`、`resumed_external_dialogue_packet.json` 和总 `resident_background_lineage_refs`。`response_surface.py` 与 `model_expression.py` 会把同一 presence 放进 `audited_expression_material_v0#memory_dream_growth / resident_background` 和 `model_expression_context_summary`，作为成长/学习的隐性材料。完成口径是：成长、自我修改、学习巩固和 archive 不再停在关闭态报告或 `/growth` 检查面，而能跨后台连续性、waiting heartbeat、resident lineage、真实回合写回、恢复包和语言材料持续存在；它仍然只通过结构化证据调制语言，不生成固定回答，不新增 system prompt，不自动改代码，不绕过 shadow / replay / validation / archive。

ITR-08 第三十段把第二十九段的成长/自我修改 presence 继续压进关系连续性和人格慢变量。`resident_turn_writeback.py` 现在会在长程 continuity refresh 前提前构建 `resident_background_lineage_payload`，并通过 `_continuity_background_profile_for_evolution` 把 `resident_background_lineage_growth_self_modification_*` 扁平字段转换成 `continuity_evolution.py` 可读的 `background_growth_self_modification_*` profile。`continuity_evolution.py` 会解析 pressure、attention target、waiting posture、boundary、active domain count、growth pressure count、patch candidate count、archive receipt count、state refs、learning plan refs 和 ref set；在没有更高优先级 Queue E 修复或累计离线学习关系重整时，它可以把第一拍关系阶段推进到 `growth_self_modification_reconsolidation_waiting`，并把同一批 refs 写入 `relationship_stage_evidence_refs`。无论关系阶段是否被更高优先级链路占用，成长 presence 都会进入 `trait_slow_variables[*].evidence_refs`、`background_growth_self_modification_*` 元数据、`growth_self_modification_update_mode=growth_self_modification_rehearsal_hold` 和 `self_model.growth_window_refs`。完成口径是：成长、自我修改和 archive 现在不仅能被语言前材料看见，也会参与人格慢变量和关系连续性收敛；但它仍然只是结构化成长证据，不生成固定回答、不新增 prompt、不自动改代码、不绕过 shadow/replay/validation/archive，也不会覆盖责任/修复链的优先级。

ITR-08 第三十一段把第三十段末尾的 `TraitDriftMonitor / LifeState / AutobiographicalStack` 从文档承诺补成真实代码消费。`body/trait_drift.py` 会从带有 `growth_self_modification_update_mode` 的慢变量生成 `growth_self_modification_trait_observation_v0`，记录 trait names、growth refs、pressure、attention target、waiting posture、counts 和 `structured_trait_growth_evidence_not_spoken_language` 边界；`state_store/autobiographical_stack.py` 会生成 `autobiographical_growth_self_modification_projection_v0`，把同一组成长 refs 写入自传栈，并在有成长再巩固证据时把 replay priority 提升为 `identity_growth_reconsolidation_first`；`state_store/life_state.py` 会生成 `life_state_growth_self_modification_index_v0`，并把 refs 同步写入 `memory_index.growth_self_modification_refs` 与 `language_state.growth_self_modification_refs`。`resident_turn_writeback.py` 的 `dialogue_writeback_bundle` 也新增 `life_state.json#growth_self_modification_index`、`life_state.json#memory_index.growth_self_modification_refs`、`life_state.json#language_state.growth_self_modification_refs`、`autobiographical_stack.json#growth_self_modification_projection` 和 `autobiographical_stack.json#growth_self_modification_refs`。完成口径是：成长/自我修改 presence 不再只停留在 `self_model` 和回应材料，而是进入人格漂移监控、自传历史、生命状态根和写回包四个更长时标载体；这一段仍然不释放自然语言、不新增 system prompt、不自动改代码。

ITR-08 第三十二段把责任、后悔和修复从账本/关系记忆/修复语言继续推进到自传历史。`state_store/autobiographical_stack.py` 新增 `autobiographical_responsibility_repair_projection_v0`，从 `commitment_truth_state`、`responsibility_ledger`、`relationship_memory`、`commitment_repair_index`、`apology_repair_language_trace`、`responsibility_loop_state`、`world_contact_summary`、`pain_regret_repair_report` 和 `engram_index` 聚合 `responsibility_refs`、`regret_refs`、`repair_refs` 与 `queue_e_repair_refs`，并保留 `pressure_level`、`attention_target`、`queue_e_priority_band`、`repair_followup_required` 和 `autobiographical_repair_evidence_not_spoken_language` 边界。`resident_turn_writeback.py` 会把刷新后的责任/后悔/修复载体传入自传栈，并在 `dialogue_writeback_bundle.autobiographical_writeback_refs` 中新增 `responsibility_repair_projection`、`autobiographical_responsibility_refs`、`autobiographical_regret_refs`、`autobiographical_repair_refs` 与 `queue_e_repair_refs`。完成口径是：责任/后悔/修复不再只是道歉或关系状态，而能成为自传栈可重放的长期自我历史；当 Queue E 修复压力 elevated 或 repair followup required 时，`replay_priority` 会提升为 `identity_repair_reconsolidation_first`，且这仍然不生成固定道歉话术、不新增 system prompt、不把内部责任字段外显成回答。

ITR-08 第三十三段把第三十二段写入自传栈的责任/后悔/修复投影继续送入下一轮线索召回和语言前材料。`state_store/memory_retrieval.py` 现在会读取 `autobiographical_stack.json#responsibility_repair_projection`、`autobiographical_responsibility_refs`、`autobiographical_regret_refs`、`autobiographical_repair_refs` 与 `queue_e_repair_refs`，生成 `memory_retrieval_autobiographical_repair_profile_v0`，并把 `autobiographical_responsibility_repair_hits` 同步并入 activated refs、responsibility hits、reconstruction inputs 和 `reconstruction_focus=autobiographical_responsibility_repair_reconstruction`。`life_state.py` 会把同一批 hits 写入 `memory_index.memory_retrieval_refs`；`dialogue_events.py` 会把 profile ref、pressure、attention target 和 retrieval boundary 带入 external/life turn event；`resident_turn_writeback.py` 会把 hit count、pressure、attention target、projection boundary、retrieval boundary 和 ref set 写入 `terminal_life_loop_state.json`、`dialogue_writeback_bundle.memory_retrieval_writeback_refs` 与 `resumed_external_dialogue_packet.json`；`state_inspection.py` 的 `/memory` 摘要也能显示 `autobiographical_responsibility_repair_hit_count` 与投影/召回两层边界。`response_surface.py` 和 `model_expression.py` 则继续把这些字段作为 `memory_dream_growth.memory_retrieval` 与 `model_expression_context_summary` 的结构化材料消费。完成口径是：责任、后悔、修复进入自传历史之后，不会停成一个长期 state 文件，而会在下一轮关系话语中被 cue-driven retrieval 重新激活，进入 life state、真实回合事件、terminal loop、恢复包、检查面和模型表达上下文；但这仍然只改变召回重构和语言前结构化材料，不生成固定道歉、不新增 system prompt、不把“后悔/修复”字段名硬塞成外显回答。

ITR-08 第三十四段把第三十三段的自传责任修复召回继续推进到等待、后台谱系和关闭态证据总线。`idle_strategy.py` 现在会把 `memory_retrieval_autobiographical_repair_hit_count`、pressure、attention target、projection boundary、retrieval boundary 和 refs 放入 idle governance 与 `memory_retrieval_presence_profile`；`heartbeat.py` 会把这些字段列入 waiting carry；`background_lineage_state.py` 会在 `resident_background_lineage_state.memory_retrieval_presence` 中保留同一批自传修复 presence；`response_surface.py` 会把它们继续放进 `audited_expression_material_v0#memory_dream_growth.resident_memory_retrieval_presence`，作为语言前隐性材料。`process_report.py#_autobiographical_repair_retrieval_report_profile` 会读取 `memory_retrieval_frame.json#autobiographical_responsibility_repair_profile / hits` 和 idle governance，生成 `autobiographical_repair_retrieval_report_profile_v0`，并把 ref set、hit count、pressure、attention target、projection boundary、retrieval boundary 与 `autobiographical_repair_structured_report_not_spoken_language` 写入 `digital_life_process_report.json`、`digital_life_process_digest.json` 和 process receipt；receipt 同时把自传责任修复 refs 放进 `shared_object_refs`，且 `memory_retrieval_frame.json` 已纳入 `input_hashes`。完成口径是：责任/后悔/修复的召回不能只在当轮语言前材料里出现，还必须能跨等待心跳、后台连续体和关闭态报告被追溯；这一步仍然不生成固定道歉、不新增 system prompt、不把内部责任/后悔/修复字段拼成外显回答。

ITR-08 第三十五段把第三十四段的关闭态证据重新回灌到下一次唤醒的后台连续性。此前 `process_report.py` 已经能写出 `autobiographical_repair_retrieval_report_profile_v0`，但 `background_continuity.py` 还没有把这份关闭态 profile 恢复成下一轮可被 `idle_strategy.py`、waiting heartbeat 和 background lineage 消费的 `memory_retrieval_presence_profile_v0`。现在 `background_continuity.py#_memory_retrieval_presence_profile` 会从 resident governance、snapshot、resident governance report、persistent process report、process report 和上一轮 lineage presence 中读取 `autobiographical_repair_retrieval_report_profile`、flat retrieval fields、carrier refs 与 background memory retrieval fields，归一化为 `background_memory_retrieval_presence_profile`、`memory_retrieval_presence_profile`、`background_memory_retrieval_ref_set`、hit count、pressure、attention target、projection boundary、retrieval boundary 和 report boundary，并把 ref set 并入 `background_continuity_ref_set`。`tests.process.test_persistent_digital_life_process#test_background_continuity_restores_autobiographical_repair_retrieval_from_process_report` 证明同一批责任/后悔/修复 refs 会从 `digital_life_process_report.json` 恢复到 background continuity，再被 `decide_idle_strategy` 读成 `memory_retrieval_autobiographical_repair_*` waiting governance 字段。完成口径是：自传责任修复召回现在不只从当轮记忆进入关闭态 report，也能从关闭态 report 回到下一次唤醒的等待治理；它仍然只是结构化记忆 presence，不生成固定道歉、不新增 system prompt、不把后悔/修复字段名拼成 Adam 的外显语言。

ITR-08 第三十六段把第三十五段恢复出的 nested memory presence 继续接回二次关闭态 report / digest / receipt。此前 `process_report.py#_autobiographical_repair_retrieval_report_profile` 主要读取 `memory_retrieval_frame.json` 与 idle governance 扁平字段；如果一次唤醒只携带 `memory_retrieval_presence_profile` / `background_memory_retrieval_presence_profile`，而没有重新生成新的 memory frame，二次 closeout 的自传责任修复报告会变薄。现在该函数会同时读取 nested presence 中的 `autobiographical_repair_hit_count`、pressure、attention target、projection boundary、retrieval boundary、refs、`source_report_profile` 和 carrier refs，再与扁平字段及 memory frame 合并生成 `autobiographical_repair_retrieval_report_profile_v0`。`_process_receipt` 也新增 `autobiographical_repair_carrier_refs`，并把 carrier refs 放进 `shared_object_refs`。`tests.process.test_persistent_digital_life_process#test_process_report_restores_autobiographical_repair_from_nested_memory_presence` 证明即使没有新的 `memory_retrieval_frame.json`，仅靠 nested memory retrieval presence 也能重新写出 report、digest 和 receipt 的自传责任修复召回证据。完成口径是：自传责任/后悔/修复召回形成二次循环，不会在“关闭态 report -> background continuity -> idle presence -> 再次 closeout”这条链上丢失；它仍然只是结构化证据和 carrier refs，不生成固定回答、不新增 system prompt、不把内部修复字段拼成外显语言。

ITR-08 第三十七段把第三十六段的 `source_report_profile` 与 `autobiographical_repair_carrier_refs` 继续接进真实回合链。此前 background continuity 已能恢复关闭态自传修复 report，process report 也能从 nested presence 再次 closeout，但 `idle_strategy.py` 的浅层化、`background_lineage_state.py`、`dialogue_events.py`、`dialogue_writeback.py`、`response_surface.py` 与 `model_expression.py` 主要保留普通 repair refs / pressure / boundary；关闭态 profile 的来源载体在真实关系回合中会变薄。现在 `background_continuity.py` 显式输出 `autobiographical_repair_carrier_refs`；`idle_strategy.py` 与 `heartbeat.py` 会把 carrier refs 列入 waiting carry；`background_lineage_state.py` 会在 `memory_retrieval_presence` 中保留 carrier refs、report boundary、source profile schema、profile/hits/projection refs；`dialogue_events.py` 会展开为 `resident_background_lineage_autobiographical_repair_*` 字段；`dialogue_writeback_bundle.json` 与 `resumed_external_dialogue_packet.json` 会保留专用 carrier refs；`response_surface.py` 会把这些字段放进 `audited_expression_material_v0#memory_dream_growth.resident_memory_retrieval_presence`；`model_expression.py` 会在 `resident_background.memory_retrieval_presence` 与 `model_expression_context_summary` 中保留 carrier ref count / report boundary / source schema。`tests.process.test_response_surface#test_memory_retrieval_presence_crosses_lineage_event_writeback_and_response` 和 `tests.process.test_model_expression#test_openai_compatible_expression_uses_transport_and_redacts_secret` 证明 source/carrier 只作为结构化来源证据进入真实回合、恢复包和模型表达上下文，不生成固定回答、不新增 system prompt、不把内部 profile 名称当成 Adam 的外显语言。

ITR-08 第三十八段把身体内环境标签接入生命膜 Go/No-Go。`body/need_state.py` 真实输出的 `sleep_pressure` 不总是数字，而可能是 `managed_pre_dream`、`offline_ready` 这类身体状态标签；`core_affect.py` 也可能在后续链路中出现标签化 pain pressure。此前 `go_nogo.py` 直接 `float()` 会在这类标签进入生命膜时失效，导致身体状态和行动膜之间出现类型断链。现在 `go_nogo.py#_pressure_value` 会把 sleep/pain 标签归一到 0-1 压力数值：`managed_pre_dream` 保持中等预梦压力，不触发 sleep inhibition；`offline_ready/high/urgent` 才进入更强抑制；pain 的 `present/elevated/high/urgent` 会进入修复审查。`SOURCE_DOC_REFS` 同步加入 `docs/real—live0/03_body_affect_homeostasis.md`，测试 `tests.slices.test_life_membrane#test_go_nogo_accepts_body_state_sleep_pressure_labels` 证明生命膜能消费身体状态标签而不是只接受浮点数。完成口径是：身体/内环境不再只调制 idle 和语言，也能稳定进入生命膜行动阈值；这仍然是内部 Go/No-Go 压力转换，不生成固定拒绝话术、不新增 system prompt、不把身体状态播报成外显语言。

ITR-08 第三十九段把第三十八段的身体压力归一继续推进到世界接触、责任回路、验证汇总和状态查看。此前 `go_nogo.py` 已能把 `managed_pre_dream/offline_ready` 等标签转成数值阈值，但输出只留下 delay reason，下游无法追溯“原始身体标签 -> 归一压力 -> 阈值触发”的证据。现在 `go_nogo.py` 写出 `body_pressure_profile=go_nogo_body_pressure_profile_v0` 与 `body_pressure_profile_ref`，包含 sleep/pain 原始值、归一值、触发阈值、pressure delay reasons、source refs 和 `go_nogo_body_pressure_profile_not_spoken_language` 边界；`world_contact_gate.py` 会把 profile/ref 放入 world contact gate 与 `life_constraint_refs`；`responsibility_loop.py` 会把同一 ref 放入责任事件 future constraints 和 regret pain signals；`world_contact_validator.py`、`validation_rollup.py` 会继续携带 `body_pressure_profile_ref` 和 `queue_e_world_contact_body_pressure_profile_ref`；`state_inspection.py` 的 `/membrane` action gate 摘要会显示 sleep/pain pressure value、pressure delay reasons 和 boundary。测试 `tests.slices.test_life_membrane#test_go_nogo_accepts_body_state_sleep_pressure_labels` 覆盖 Go/No-Go -> WorldContactGate -> WorldContactValidation -> ValidationRollup 的轻量链，完整 membrane 测试覆盖 runtime artifacts。完成口径是：身体内环境影响生命膜不再是不可追溯的 if 判断，而是可进入世界接触、责任、验证和检查面的结构化压力 profile；它仍然不是固定拒绝语，不新增 system prompt，不把身体压力播报成外显回答。

ITR-08 第四十段把第三十九段的 `body_pressure_profile_ref` 从验证层继续推进到 schema runner、出生准备、常驻等待、后台谱系、真实回合事件、关闭态 report/digest/receipt 和 live0 audit。此前 profile 已能到 validation rollup，但出生准备的 Queue E world-contact handoff 只显式携带 future no-go、repair hold、route 和 governance refs；关闭终端后也主要靠 `ref_set` 间接保存身体压力证据。现在 `schema_runner/cross_file_logic.py`、`run_manifest.py` 和 `schema_runner/__init__.py` 会把 `queue_e_world_contact_body_pressure_profile_ref=runtime/state/action/go_nogo_state.json#body_pressure_profile` 写进 cross-file logic、run manifest、stage gate、report、digest 和 receipt；`life_targets/__init__.py` 会要求 world-contact validation、validation rollup 和 schema runner manifest 三层都携带该 ref，才把 handoff 推为 `closed`，并把 `body_pressure_profile_ref` 写入 `queue_e_world_contact_repair_hold_handoff.json`、life target claims、evidence matrix、birth readiness rollup、stage gate、report、digest、check report 和 receipt。常驻层的 `idle_strategy.py`、`continuity_writeback.py`、`heartbeat.py`、`background_continuity.py`、`background_lineage_state.py`、`dialogue_events.py` 与 `process_report.py` 会继续保留 `queue_e_world_contact_body_pressure_profile_ref`，并将它并入 handoff refs、background lineage refs、process shared object refs 和 input hash 覆盖。`live0_audit` 的 world-contact validation 和 schema handoff probe 也会检查该 ref。测试覆盖 `tests.slices.test_schema_runner`、`tests.slices.test_life_targets`、`tests.contracts.test_live0_acceptance_audit` 和 persistent process 的 waiting heartbeat / dialogue writeback / background lineage / idle strategy 相关用例。完成口径是：身体内环境压力不只影响当轮行动膜，也能跨 S05/S09/S08、常驻等待、后台恢复、真实回合和关闭态报告保持可追溯；它仍然只是结构化生命膜证据，不生成固定回答、不新增 system prompt、不把身体状态显示成外显语言。

ITR-08 第四十一段把第四十段的身体压力证据继续送入语言前材料和模型表达摘要。此前 `world_contact_handoff_presence` 已经能通过常驻谱系进入 response surface 和 model expression，但 `body_pressure_profile_ref` 主要藏在 ref set 中，语言审计只能间接追到身体/内环境压力。现在 `response_surface.py` 会把 `body_pressure_profile_ref` 显式写入 `audited_expression_material_v0#responsibility_repair.world_contact_handoff_presence`，并纳入 handoff ref count；`model_expression.py` 会在 `model_expression_context_summary` 中写出 `world_contact_handoff_body_pressure_profile_ref`，并把它计入 `world_contact_handoff_ref_count`。这一步的完成口径是：语言系统读取世界接触修复交接时，能同时看到 repair hold、确认阈值、未来行动抑制和身体压力来源；但这些仍然只是隐性结构化材料与 post-expression 软审计，不生成固定回答、不新增 system prompt、不把身体压力字段名释放到终端语言。

ITR-08 第四十二段回切补强工作区、广播和元认知到责任环的消费。此前 `WorkspaceFrame / ConsciousBroadcastFrame / MetacognitionFrame` 已经能进入语言审计、常驻谱系和出生准备，但责任 attribution 仍主要依赖 side effect、世界接触、预测和身体压力。现在 `run_life_membrane` 会把 `workspace_frame.json`、`broadcast_frame.json`、`metacognition_state.json` 和可用的 `consciousness_probe_bundle.json` 传入 `build_responsibility_loop_state(...)`；`responsibility_loop.py` 会写出 `consciousness_context_profile=responsibility_consciousness_context_profile_v0`，携带三件套 refs、可报告 flags、工作区候选数量、广播目标数量、元认知 uncertainty 和语言/关系连续性计数，并把 profile ref 挂到 `ResponsibilityAttributionEvent`。这一步的完成口径是：责任、后悔和修复链不只知道“造成了什么后果”，也能追溯当时工作区/广播/元认知提供了哪些可报告上下文；但这仍然是内部证据，不生成意识宣言、不新增 system prompt、不把 consciousness/profile 字段释放成外显回答。

ITR-08 第四十三段把同一组工作区、广播、元认知和 consciousness probe 继续接入梦境醒后整合。此前 `wake_integration_frame.json` 主要消费 dream window、replay cue 和 Queue E 修复压力，梦境醒后材料还没有明确说明怎样重新进入工作区和元认知检查。现在 `run_cycle` 会读取 consciousness 目录四个载体，并传给 `build_wake_integration_frame(...)`；`wake_integration.py` 会写出 `consciousness_reentry_profile=wake_consciousness_reentry_profile_v0` 和 `workspace_reentry_targets`，携带 workspace/broadcast/metacognition/probe refs、工作区候选数量、广播目标数量、元认知 reflection 数量、reportability flags 和 `wake_consciousness_reentry_not_spoken_language` 边界。完成口径是：梦境醒后整合能追溯如何回到可报告工作区、广播和元认知，但仍然只是结构化 reentry 证据，不生成梦境叙述模板、不新增 system prompt、不把 consciousness 或 dream 字段名释放成外显回答。

ITR-08 第四十四段把同一组工作区、广播和元认知继续接入记忆写门。此前 `MemoryWriteGate` 已经能消费身体/调质压力、离线学习和关系再巩固压力，但工作区三件套主要通过 `/cognition` 检查面、语言审计、责任环和梦境醒后整合被看见，写门还缺少“当时哪些内容处于可报告工作区、哪些内容被广播、元认知是否有不确定”的结构化门控证据。现在 `run_state_store` 会读取 `runtime/state/consciousness/workspace_frame.json`、`broadcast_frame.json`、`metacognition_state.json` 和可用的 `consciousness_probe_bundle.json`，并传入 `build_memory_write_gate(...)`；`memory_write_gate.py` 会写出 `consciousness_write_context=memory_consciousness_write_context_v0`、`consciousness_write_context_refs` 和 `consciousness_write_context_profile_ref`，保留 workspace/broadcast/metacognition/probe refs、工作区候选数量、广播目标数量、元认知 uncertainty/reflection 数量、reportability flags、语言/关系连续性计数、write attention bias、candidate gate adjustments、ref set 和 `memory_consciousness_write_context_not_spoken_language` 边界。完成口径是：记忆写入不只由事实来源、关系、身体压力和梦境事实门治理，也能追溯经验写入时的工作区/广播/元认知上下文；这仍然是内部写门证据，不生成意识宣言、不新增 system prompt、不把 consciousness 或 memory gate 字段释放成外显回答。

ITR-08 第四十五段把第四十四段的 `consciousness_write_context` 从记忆写门继续推进到常驻谱系、真实回合、关闭写回、下一轮恢复和语言前结构材料。此前 `memory_write_gate.json#consciousness_write_context` 已经能保存工作区、广播和元认知上下文，但 `prediction_write_gate_presence`、`dialogue_writeback_bundle.json`、`resumed_external_dialogue_packet.json` 和 `audited_expression_material_v0` 还主要携带预测/写门 refs、身体信号调制和状态合并信息，工作区写入上下文容易在下游变薄。现在 `idle_strategy.py` 与 `dialogue_events.py` 会把 `MemoryWriteGate.consciousness_write_context` 展开为 `consciousness_write_context_refs`、candidate count、broadcast target count、reportability flag count、write bias、candidate gate adjustments 和 boundary；`heartbeat.py` 会把这组字段列入 waiting carry；`background_lineage_state.py` 会把它们写入 `prediction_write_gate_presence` 并并入 `prediction_write_gate_evidence_refs`；`dialogue_events.py` 会继续展开到 `resident_background_lineage_consciousness_write_context_*`；`dialogue_writeback.py`、`resident_turn_writeback.py` 会把同一批 refs、bias、counts、adjustments 和 boundary 写入关闭态 bundle 与恢复包；`process_report.py` 会保存 `background_consciousness_write_context_*` 证据；`response_surface.py` 会把它们放进 `prediction_attention` 与 `resident_background.prediction_write_gate_presence`。完成口径是：工作区/广播/元认知上下文不仅进入记忆写门，还能跨等待心跳、后台 lineage、真实关系回合、关闭态 report、下一次恢复和模型表达前材料被消费；这仍然是结构化隐性材料，不新增固定回答、不新增 system prompt、不把意识写门或生命信号释放成外显语言。

ITR-08 第四十六段把第四十五段的关闭态证据回灌到下一次唤醒的 background continuity。此前 `process_report.py` 已能写出 `background_consciousness_write_context_*`，但 `background_continuity.py` 主要恢复 prediction/write-gate refs、身体信号调制、状态合并和 Queue F identity/consciousness/birth presence；如果下一次唤醒只依赖关闭态 process report，而没有重新生成 memory write gate，工作区写入上下文会从等待治理里变薄。现在 `background_continuity.py` 会从 resident governance、snapshot、resident governance report、persistent process report、process report 和上一轮 `prediction_write_gate_presence` 中读取 `consciousness_write_context_refs`、ref count、workspace candidate count、broadcast target count、reportability flag count、bias、candidate gate adjustments 和 boundary，输出为 `background_consciousness_write_context_*`，并把 refs 并入 `background_continuity_ref_set`。完成口径是：意识写门上下文现在可以走完整的“记忆写门 -> 常驻等待 -> 关闭态 report -> background continuity -> 下一轮 idle governance”循环；它仍然只是恢复用结构证据，不新增固定回答、不新增 system prompt、不把内部意识写门状态释放成对话内容。

ITR-08 第四十七段把意识写门上下文继续推进到模型表达输入和表达后审计摘要。此前 `response_surface.py` 已把 `consciousness_write_context_*` 放进 `audited_expression_material_v0#prediction_attention`，但 `model_expression.py` 的 prediction attention 白名单和 `model_expression_context_summary` 仍只消费 surface posture、active sampling route、prediction error、memory write gate policy、state merge 和 body signal 字段。现在 `_prediction_attention_from_material(...)` 会保留 `consciousness_write_context_refs`、ref count、workspace candidate count、broadcast target count、reportability flag count、bias、candidate gate adjustments 和 boundary；`_prediction_conscious_summary(...)` 会把它们展开成 `prediction_attention_consciousness_write_context_*`；`_context_summary(...)` 会把同一批字段写进 `model_expression_context_summary`；`_prediction_attention_pressure_present(...)` 也会把 consciousness write context 的 bias、boundary 或 ref count 视为 prediction attention 压力来源。完成口径是：工作区/广播/元认知如何调制记忆写入，不只进入 response surface，还进入真实模型表达前的结构上下文和 post-expression 软审计；它仍然不生成固定回答、不新增 system prompt、不要求模型字面说出意识写门或生命信号。

ITR-08 第四十八段把第四十七段的模型表达上下文继续收束到关闭态总报告、digest 和 process receipt。此前 `model_expression_state.json#model_expression_context_summary` 已能记录 `prediction_attention_consciousness_write_context_*`，但 `digital_life_process_report.json`、`digital_life_process_digest.json` 和 process receipt 主要保存模型表达 state/report refs、status 与 post-expression gate 状态，不能直接看见表达前到底消费了哪些意识写门上下文。现在 `process_report.py` 会从 `model_expression_context_summary` 提取 `prediction_attention_consciousness_write_context_refs`、ref count、workspace candidate count、broadcast target count、reportability flag count、bias、candidate gate adjustments 和 boundary，压成 `model_expression_consciousness_write_context_report_profile_v0`，并在 report、digest、receipt 中展开为 `model_expression_prediction_attention_consciousness_write_context_*` 字段，同时把 refs 纳入 receipt shared object refs。完成口径是：表达前意识写门上下文不只停在语言 state，也能进入关闭态汇总和 receipt 证据链，方便下一轮断链审计；它仍然是结构化追溯证据，不生成固定回答、不新增 system prompt、不释放内部生命信号。

ITR-08 第四十九段把第四十八段的关闭态模型表达证据回灌到下一次唤醒的 background continuity。此前 `background_continuity.py` 能从 `background_consciousness_write_context_*` 恢复工作区写门上下文，但如果关闭态 process report 只保留 `model_expression_prediction_attention_consciousness_write_context_*`，下一次唤醒的 `background_consciousness_write_context_*` 会变薄。现在 `background_continuity.py` 会把模型表达侧的 refs、ref count、workspace candidate count、broadcast target count、reportability flag count、bias、candidate gate adjustments 和 boundary 作为恢复来源，归一成 `background_consciousness_write_context_*`，并把 refs 纳入 `background_continuity_ref_set`。完成口径是：模型表达前真实消费过的意识写门上下文，可以从关闭态 report 进入下一轮 idle governance / waiting heartbeat / resident lineage；它仍然只是跨唤醒结构证据，不生成固定回答、不新增 system prompt、不把内部生命信号释放成外显语言。

ITR-08 第五十段把第四十七到四十九段的模型表达意识写门证据接入 `/language` 检查面。此前 `state_inspection.py#language_generation_consumption_summary_v0` 已能显示语言感知、语义图、内言语、表达监控、模型表达、关系、记忆、梦境、身体、调质、责任、预测、主动发话等消费域，但没有展开 `model_expression_context_summary.prediction_attention_consciousness_write_context_*`，导致检查面难以直接确认语言表达前是否消费了工作区/广播/元认知写门材料。现在 `/language` 会在 `generation_consumption_summary` 中显示 `model_expression_consciousness_write_context_refs`、ref count、workspace candidate count、broadcast target count、reportability flag count、bias、candidate gate adjustments 和 boundary，并把 `model_expression_consciousness_write_context` 计入 domain presence。完成口径是：point 5/7 的语言检查面可以追溯模型表达前的意识写门上下文，但这仍然是 inspection-only 结构证据，不生成固定回答、不新增 system prompt、不把内部生命信号释放成外显语言。

ITR-08 第五十一段把同一组模型表达意识写门证据接入 `/cognition` 检查面。此前 `/cognition#cognitive_workspace_summary_v0` 已能显示 workspace、broadcast、metacognition、belief、prediction error、active sampling、memory write gate 和 state merge guard，但它没有读取 `language/model_expression_state.json`，因此无法在认知检查面反查模型表达前是否真正消费了工作区/广播/元认知写门材料。现在 `state_inspection.py` 的 `/cognition` 文件收集会加入 `model_expression_state`，`_collect_cognitive_workspace_summary(...)` 会读取 `model_expression_context_summary.prediction_attention_consciousness_write_context_*`，并输出 `model_expression_consciousness_write_context_refs`、ref count、workspace candidate count、broadcast target count、reportability flag count、bias、candidate gate adjustments 和 boundary，同时把 `model_expression_consciousness_write_context` 计入 `domain_presence` 与 `active_domains`。完成口径是：point 7 的认知状态查看面不只显示工作区三件套本身，也能和 point 5 的语言检查面互相验证“模型表达确实消费了这组写门上下文”；它仍然是结构化检查证据，不生成固定回答、不新增 system prompt、不把内部生命信号或检查摘要释放成 Adam 的外显语言。

ITR-08 第五十二段把模型表达意识写门证据继续接入 `/consciousness` 与 `/意识` 检查面。此前 `consciousness_reportability_summary_v0` 会显示 workspace、broadcast、metacognition、consciousness probe、birth readiness、terminal life loop 和 resident governance，但它只能证明可报告工作区是否存在，不能证明这组可报告工作区材料是否已经进入模型表达前的写门消费证据。现在 `/consciousness` 会读取 `language/model_expression_state.json`，`_collect_consciousness_reportability_summary(...)` 会展开 `model_expression_context_summary.prediction_attention_consciousness_write_context_*`，输出 refs、ref count、workspace candidate count、broadcast target count、reportability flag count、bias、candidate gate adjustments 和 boundary，并把 `model_expression_consciousness_write_context` 计入 `domain_presence`。完成口径是：意识检查面不只看“工作区/广播/元认知/探针是否存在”，还要能追溯这些材料是否抵达语言表达前的结构消费层；它仍然是状态检查证据，不生成意识宣言、不新增 system prompt、不把内部生命信号或写门字段转写成固定外显语言。

ITR-08 第五十三段把模型表达意识写门证据接入 `/thinking` 与 `/思考` 检查面。此前 `self_thinking_summary_v0` 能显示 resident self-thinking、自我模型、内言语、consciousness probe、后台人格收敛和自主活动，但它只能证明内言语和自我反思存在，不能证明“思考以后说话”的末端模型表达是否消费了工作区/广播/元认知写门材料。现在 `/thinking` 会读取 `language/model_expression_state.json`，`_collect_self_thinking_summary(...)` 会展开 `model_expression_context_summary.prediction_attention_consciousness_write_context_*`，输出 refs、ref count、workspace candidate count、broadcast target count、reportability flag count、bias、candidate gate adjustments 和 boundary，并把 `model_expression_consciousness_write_context` 计入 `domain_presence`。完成口径是：思考检查面可以把内言语、自我反思、意识探针和模型表达前消费证据放在同一张结构视图里，证明模型表达位于生命状态之后；它仍然是 inspection-only，不生成内心独白模板、不新增 system prompt、不把内部思考或写门字段释放成外显语言。

ITR-08 第五十四段把模型表达意识写门证据接入 `/state` 总览检查面。此前 `resident_continuity_summary_v0` 只读取 resident lifecycle、relation queue、autonomous activity、idle strategy、resident governance、terminal life loop、terminal input profile 和 waiting heartbeat，因此 `/state` 能看见常驻是否活着、是否等待、输入框是否正常，却不能从总览层追溯上一轮模型表达前是否消费了工作区/广播/元认知写门材料。现在 `_collect_state_summary(...)` 会读取 `language/model_expression_state.json`，`_collect_resident_continuity_summary(...)` 会展开 `model_expression_context_summary.prediction_attention_consciousness_write_context_*`，输出 refs、ref count、workspace candidate count、broadcast target count、reportability flag count、bias、candidate gate adjustments 和 boundary，并把 `model_expression_consciousness_write_context` 计入 `domain_presence`。完成口径是：point 7 的 `/state` 总览不只显示 resident 进程和等待节律，也能看到语言表达前结构消费证据是否存在；它仍然是状态检查，不生成固定回答、不新增 system prompt、不把内部生命信号或写门字段释放成 Adam 的外显语言。

ITR-08 第五十五段把模型表达意识写门证据接入 `/proactive` / `/proactive_voice` 主动发话检查面。此前 `proactive_voice.coverage_summary` 已能显示主动发话状态、释放 scope、是否释放自然语言、模型表达状态、post-expression gate、active domains、候选 code 数和 `state_codes_only_model_expression_required` 边界，但它只读取 `resident_terminal_proactive_state.json` 和 proactive events，不能直接证明主动发话那次模型表达前是否消费了工作区/广播/元认知写门材料。现在 `/proactive` 会读取 `language/model_expression_state.json`，`_collect_proactive_voice_summary(...)` 会展开 `model_expression_context_summary.prediction_attention_consciousness_write_context_*`，输出 refs、ref count、workspace candidate count、broadcast target count、reportability flag count、bias、candidate gate adjustments 和 boundary，并把 `model_expression_consciousness_write_context` 合入主动发话的 domain presence / active domains。完成口径是：point 6 的主动语言通道不只证明“没有代码硬拼话术、只有模型表达通过 gate 才释放”，还要能追溯模型表达前消费了哪些工作区写门材料；它仍然是 inspection-only，不生成主动问候模板、不新增 system prompt、不把内部生命信号或写门字段转成外显话语。

ITR-08 第五十六段闭合 live turn 意识链后半段。此前 `resident_turn_writeback.py` 在每轮关系写回时只投影 `workspace_frame.json`，`broadcast_frame.json` 与 `metacognition_state.json` 仍停留在 S02/S08 种子态，无法证明当前关系焦点已被多系统广播和元认知重新读取。现在 `broadcast.py#project_broadcast_frame_from_live_turn` 会从更新后的 workspace 同步 `broadcast_targets`、`salience_ranking`、`suppressed_content_refs`（第三名及以后候选进入抑制列表）、`live_turn_focus` 与 live dialogue/language refs；`metacognition.py#project_metacognition_state_from_live_turn` 会同步 `broadcast_targets`、`uncertainty_flags`（语义歧义、记忆隔离、重构召回、表达澄清）、`memory_reconstruction_focus`、`expression_release_caution_level` 与 `last_projected_from_live_turn_ref`；`resident_turn_writeback.py` 在写出 workspace 后同轮写出 broadcast 与 metacognition。完成口径是：`docs/real—live0/02_brain_network_and_workspace.md` 要求的 `WorkspaceFrame -> ConsciousBroadcastFrame -> MetacognitionFrame` 在真实关系回合后保持同轮刷新，供责任环、记忆写门、梦境醒后整合、语言材料和 `/cognition` 检查面消费；它仍然不生成固定意识宣言、不新增 system prompt、不把 broadcast/metacognition 字段释放成外显语言。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第五十七段把第五十六段刷新后的意识链继续推进到下游真实消费。此前 `workspace/broadcast/metacognition` 虽已同轮写出，但 `consciousness_probe_bundle.json`、`memory_write_gate.json#consciousness_write_context` 与 `responsibility_loop_state.json#consciousness_context_profile` 仍可能停留在 S02/S08 或上一轮 lineage 种子，`build_prediction_write_gate_payload` 也会继续读取旧的 `memory_write_gate` 入参。现在 `consciousness_probes.py#project_consciousness_probe_bundle_from_live_turn`、`memory_write_gate.py#project_memory_write_gate_with_consciousness_context` 与 `responsibility_loop.py#project_responsibility_loop_with_consciousness_context` 会在 `_refresh_long_horizon_continuity` 末尾同轮重建 probe、写门上下文和责任归因上下文；`resident_turn_writeback.py` 随后用刷新后的 `memory_write_gate` 重建 `prediction_write_gate_payload`，把 live 意识链 refs 写入 `dialogue_writeback_bundle`、`terminal_life_loop_state`、`resumed_external_dialogue_packet` 与 lineage 字段，并显式覆盖陈旧 lineage 里的 consciousness write context。完成口径是：`docs/real—live0/02_brain_network_and_workspace.md` 要求的“广播内容进入记忆写门、元认知进入出生准备/责任链”在真实关系回合后不再只停在文件存在，而是同轮进入 probe、写门、责任环、恢复包和下一轮 prediction/write-gate 证据；它仍然只是结构化隐性材料，不生成固定意识宣言、不新增 system prompt、不把 consciousness/profile 字段释放成外显语言。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第五十八段把 Queue E world-contact repair hold handoff 继续推进到 live turn 同轮刷新。此前 `queue_e_world_contact_repair_hold_handoff.json` 主要在 S08 出生准备和 S05/S09 验收链写出，真实关系回合后即使 `responsibility_loop_state.json#consciousness_context_profile` 已刷新，handoff 仍可能停留在旧 lineage 或 `deferred_until_s05_s09` 种子，`build_queue_e_world_contact_handoff_payload` 也会继续从陈旧 `terminal_life_loop_state` 入参读取。现在 `life_targets/queue_e_world_contact_handoff.py#project_queue_e_world_contact_repair_hold_handoff_from_live_turn` 会在 `_refresh_long_horizon_continuity` 末尾按 `world_contact_validation.json`、`validation_rollup.json`、`schema_runner/run_manifest.json` 与 live 责任环意识上下文同轮重建 handoff；`resident_turn_writeback.py` 会把结果写入 `queue_e_world_contact_repair_hold_handoff.json`，同步 `live_queue_e_world_contact_handoff_refreshed`、`queue_e_world_contact_*` 到 `terminal_life_loop_state`，并用刷新后的 terminal loop 重建 `queue_e_world_contact_handoff_payload`、`dialogue_writeback_bundle` 与 `resumed_external_dialogue_packet`。完成口径是：`docs/real—live0/10_responsibility_regret_repair.md` 与 `docs/real—live0/11_life_membrane_validation.md` 要求的“FutureNoGo repair hold → validation → schema manifest → birth handoff → 常驻等待/恢复包”在真实关系回合后不再只停在 S08/S09 文件存在，而是同轮进入 handoff、terminal loop、写回包和 lineage refs；当 S05/S09 尚未闭合时 handoff 会保持 `deferred_until_s05_s09`，不会伪造 closed。它仍然只是结构化治理证据，不生成固定道歉/拒绝话术、不新增 system prompt、不把 repair hold 字段释放成外显语言。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第六十段把第五十九段 live handoff 关闭态证据继续推进到 slash 检查面与 live0 验收。`state_inspection.py` 的 `/responsibility`、`/痛苦`、`/后悔` 与 `/state` 现在会显示 `live_queue_e_world_contact_handoff_refreshed`、`live_responsibility_consciousness_context_ref_count`、`live_queue_e_world_contact_handoff_turn_focus` 与 `live_queue_e_world_contact_handoff_boundary`；`live0_audit` 的 criterion f 新增 `live_queue_e_world_contact_handoff_closeout_audited` probe，当 handoff 文件或 terminal loop 存在 live refresh 信号时，要求 `digital_life_process_report.json` 携带 `live_queue_e_world_contact_handoff_report_profile_v0` 与 report boundary。完成口径是：point 7 的责任/状态检查面与 point 9 的最终验收能追溯 live handoff 是否进入关闭报告，但仍只是 inspection/audit 证据，不生成固定回答、不新增 system prompt、不把 repair hold 字段释放成外显语言。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第六十一段把第六十段的 live handoff 检查证据继续补到 `/membrane`、`/生命膜`、`/prediction`、`/预测` 与 `/世界接触`。`state_inspection.py` 现在会读取 `life_targets/queue_e_world_contact_repair_hold_handoff.json` 与 `terminal/terminal_life_loop_state.json`，并通过 `_live_queue_e_world_contact_handoff_inspection_snapshot` 在 `life_membrane_validation_summary_v0` 与 `prediction_world_contact_summary_v0` 中显示 `queue_e_world_contact_handoff_status`、`live_queue_e_world_contact_handoff_refreshed`、`live_responsibility_consciousness_context_ref_count`、`live_queue_e_world_contact_handoff_turn_focus` 与 `live_queue_e_world_contact_handoff_boundary`，同时把 `live_queue_e_world_contact_handoff` 计入 domain presence。完成口径是：`docs/real—live0/11_life_membrane_validation.md` 与 `09_prediction_perception_world_contact.md` 要求的生命膜/世界接触检查面，也能与 `/responsibility`、`/state` 一致追溯 live Queue E repair hold handoff；它仍然只是 inspection-only 结构证据，不生成固定拒绝话术、不新增 system prompt、不把 repair hold 字段释放成外显语言。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第六十二段把同一条 live handoff 检查证据继续补到 `/ability` 与 `/vision`（`/perception`）。`/ability` 现在会额外读取 `digital_life_process_report.json`，在 `ability_birth_readiness_summary_v0` 中合并 birth readiness 与 live handoff 的 `queue_e_world_contact_handoff_status`，显示 `live_queue_e_world_contact_handoff_closeout_audited` probe 状态、`live_queue_e_world_contact_handoff_report_boundary` 与 live refresh 字段；`/vision` 的 `perception_world_contact_summary_v0` 也会显示同一组 live handoff 字段。完成口径是：出生准备/能力检查面与感知检查面可以和责任、生命膜、预测检查面互相印证 live Queue E repair hold 是否被消费；它仍然只是 inspection-only 证据，不生成固定回答、不新增 system prompt、不把 repair hold 字段释放成外显语言。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第六十三段把 live handoff 检查证据继续补到 `/signal`、`/调质` 与 `/language`。`/signal` 的 `signal_modulation_consumption_summary_v0` 现在会读取 handoff 与 terminal loop，把 live refresh 字段写入顶层摘要和 `responsibility_repair_consumption` 子视图；`/language` 的 `language_generation_consumption_summary_v0` 会同时展开 runtime live handoff 与 `model_expression_context_summary` 中的 `world_contact_handoff_*` 字段，证明语言链在模型表达前确实消费了世界接触修复交接。完成口径是：`docs/real—live0/12_neuromodulation_signal_media.md` 与 `05_language_expression_system.md` 要求的调质/语言跨器官消费链，可以在 slash 检查面与责任、预测、生命膜检查面互相印证；它仍然只是 inspection-only 结构证据，不生成固定回答、不新增 system prompt、不把 repair hold 或生命信号字段释放成外显语言。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第六十四段把 live handoff 检查证据继续补到 `/proactive`、`/proactive_voice` 与 `/cognition`。`/proactive` 的 `coverage_summary` 现在会读取 handoff、terminal loop 与 `model_expression_context_summary`，显示 runtime live refresh 与模型表达前 `world_contact_handoff_*` 字段；`/cognition` 的 `cognitive_workspace_summary_v0` 也会在同一视图里并列工作区/广播/元认知、意识写门消费证据与 live Queue E repair hold handoff。完成口径是：point 6 主动发话通道与 point 5/7 认知检查面可以证明主动语言和模型表达前结构消费确实承接了世界接触修复交接，而不是只显示 consciousness write context；它仍然只是 inspection-only 证据，不生成主动问候模板、不新增 system prompt、不把 repair hold 字段释放成外显语言。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第六十五段把 live handoff 检查证据继续补到 `/consciousness`、`/意识` 与 `/thinking`、`/思考`，并把成长关闭态证据补到 `/growth`、`/成长`。`/consciousness` 与 `/thinking` 现在会读取 handoff、terminal loop 与 `model_expression_context_summary`，显示 runtime live refresh 与模型表达前世界接触字段；`/growth` 会通过 `_growth_closeout_inspection_snapshot` 读取 `digital_life_process_report.json`、`terminal_life_loop_state.json` 与 `idle_strategy_state.json`，在 `growth_self_modification_summary_v0` 中显示 `growth_self_modification_report_profile`、report boundary、pressure/candidate/archive 计数与 `background_growth_self_modification_*` presence。完成口径是：`docs/real—live0/02_brain_network_and_workspace.md`、`13_growth_learning_self_modification.md` 要求的意识/思考检查面与成长关闭态总线可以在 slash 检查面互相印证；它仍然只是 inspection-only 证据，不生成意识宣言、成长宣言或固定回答，不新增 system prompt。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第六十六段把 ITR-08-22~27 的退出梦境记忆关闭态证据推进到 `/memory`、`/dream`、`/context` 与 `/relationship` 检查面。`state_inspection.py` 新增 `_memory_closeout_inspection_snapshot` 与 `_dream_closeout_inspection_snapshot`，从 `digital_life_process_report.json` 与 `idle_strategy_state.json` 读取 `exit_dream_next_wake_*`、`exit_dream_memory_tier_*`、`autobiographical_repair_retrieval_*` 与 `web_dream_learning_*` 关闭态 profile；`/memory#reconstructive_memory_summary_v0` 与 `/dream#dream_wake_fact_summary_v0` 会显示三层记忆分化、下一次唤醒 cue、自传责任修复召回与网页梦境学习关闭态；`/context#relation_context_summary_v0` 与 `/relationship#continuity_summary_v0` 会合并同一批 memory closeout 字段，并显示自传修复 hit count、pressure、attention target 与 carrier ref count。完成口径是：`docs/real—live0/07_memory_engram_and_state_store.md` 与 `08_dream_sleep_offline_life.md` 要求的关闭态记忆/梦境证据不只停在 process report，也能在 slash 检查面被 point 7 追溯；它仍然只是 inspection-only 结构证据，不生成固定回答、不新增 system prompt、不把记忆层级或梦境学习字段释放成外显语言。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第六十七段把 ITR-08-30~32 的成长/责任自传投影继续推进到 `/personality` 检查面。`/personality` 现在会读取 `digital_life_process_report.json` 与 `idle_strategy_state.json`，在 `personality_convergence_summary_v0` 中显示 `trait_drift_monitor#growth_self_modification_observation_profile`、`autobiographical_stack#growth_self_modification_projection`、`autobiographical_stack#responsibility_repair_projection`、成长/责任 ref count、pressure、attention target、repair followup required 与 growth closeout presence。完成口径是：`docs/real—live0/04_personality_self_identity.md` 与 `10_responsibility_regret_repair.md` 要求的人格慢变量、成长观察与责任修复自传投影可以在 slash 检查面与 `/growth`、`/memory`、`/relationship` 互相印证；它仍然只是 inspection-only 证据，不生成人格卡片、不新增 system prompt、不把内部 trait 或 repair 字段释放成外显语言。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第六十九段把 ITR-05 的身体信号关闭态证据推进到 `/emotion`、`/inner_environment` 与 `/signal` 检查面。`state_inspection.py` 新增 `_body_signal_closeout_inspection_snapshot`、`_affect_modulation_closeout_inspection_snapshot` 与 `_signal_modulation_closeout_inspection_snapshot`，从 `digital_life_process_report.json` 与 `idle_strategy_state.json` 读取 `background_body_signal_*`、`pain_regret_repair_report_ref` 与身体压力 closeout；`/emotion#emotion_regulation_summary_v0`、`/inner_environment#inner_environment_modulation_summary_v0` 与 `/signal#signal_modulation_consumption_summary_v0` 会显示 affect/body-signal closeout presence、write bias、pain pressure 与 memory write gate consciousness context。完成口径是：`docs/real—live0/03_body_affect_homeostasis.md` 与 `12_neuromodulation_signal_media.md` 要求的调质/情绪/内环境检查面可以追溯关闭态身体信号证据，而不只依赖 runtime signal 文件；它仍然只是 inspection-only 结构证据，不生成情绪话术、不新增 system prompt、不把生命信号字段释放成外显语言。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第七十段把 ITR-08-48~55 的模型表达意识写门关闭态证据继续推进到 `/language`、`/cognition`、`/consciousness` 与 `/thinking` 检查面。`state_inspection.py` 新增 `_expression_closeout_inspection_snapshot`，从 `digital_life_process_report.json` 归一化 `model_expression_consciousness_write_context_report_profile`、`live_queue_e_world_contact_handoff_report_profile` 与 `background_body_signal_*` closeout；上述四个 slash 检查面现在会读取 `digital_life_process_report.json`，在各自 summary 中显示 `expression_closeout_present`、`consciousness_write_context_closeout_present` 与 live handoff report boundary。完成口径是：point 5/7 的语言/认知/意识/思考检查面不只能看见 runtime `model_expression_state.json`，也能与关闭态 process report 互相印证表达前结构消费证据；它仍然只是 inspection-only，不生成固定回答、不新增 system prompt、不把内部写门或 handoff 字段释放成外显语言。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第七十四段把 Queue E `world_contact_repair_hold` schema handoff 继续推进到 slash 检查面。`state_inspection.py` 新增 `_queue_e_world_contact_repair_hold_schema_handoff_inspection_snapshot`，从 `validation_rollup.json`、`world_contact_validation.json`、`schema_runner/run_manifest.json` 与 `schema_runner/cross_file_logic.json` 归一化 repair hold required、confirmation threshold bias、future no-go/body pressure profile refs、blocked/allowed routes、repair governance refs 与 `queue_e_world_contact_repair_hold_alignment` finding；`/membrane`、`/prediction`、`/responsibility`、`/ability` 与 `/state` 现在会显示 `queue_e_world_contact_repair_hold_schema_handoff_present`、`queue_e_world_contact_schema_handoff_manifest_closed` 与 live0 criterion g 的 `queue_e_world_contact_repair_hold_schema_handoff` probe 状态（ability 面）。完成口径是：ITR-06/07 的 S05/S09 schema handoff 不再只停在 live0 audit，slash 检查面也能与 `cross_file_logic#queue_e_world_contact_repair_hold_alignment` 和 run manifest 互相印证；它仍然只是 inspection-only，不生成固定拒绝话术、不新增 system prompt、不把 repair hold 字段释放成外显语言。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第七十三段把 S11 v0 合同覆盖证据继续推进到 `/ability` 与 `/state` 检查面。`state_inspection.py` 新增 `_v0_contract_coverage_inspection_snapshot`，从 `v0_contract_file_index.json`、`doc_to_code_coverage_matrix.json` 与 `v0_contract_coverage_report.json` 归一化 required file count、missing files、doc-to-code uncovered docs、report status 与 activation preflight 字段；`/ability#ability_birth_readiness_summary_v0` 与 `/state#resident_continuity_summary_v0` 现在会显示 `v0_contract_coverage_present` 与 doc-to-code 覆盖摘要。完成口径是：point 2 的 slash 检查面可以直接核对 ITR-01 trace lock / S11 合同覆盖是否进入 runtime 证据，而不只读取扁平 `contract_count`；它仍然只是 inspection-only，不生成出生完成宣称、不新增 system prompt、不把合同覆盖数字释放成外显语言。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第七十二段把完整 process closeout bundle 继续推进到 `/ability` 出生准备检查面。`/ability` 现在会额外读取 `idle_strategy_state.json` 与 `go_nogo_state.json`，在 `ability_birth_readiness_summary_v0` 中合并 `_process_closeout_bundle_inspection_snapshot`，显示 `process_closeout_present`、`live_queue_e_world_contact_handoff_closeout_present`、`consciousness_write_context_closeout_present`、`body_pressure_closeout_present` 与 `autobiographical_repair_retrieval_closeout_present`，并与 birth readiness rollup、live0 acceptance audit 和 live handoff 状态互相印证。完成口径是：出生准备/能力检查面可以和 `/membrane`、`/state`、`/perception` 一样追溯关闭态 report 证据，而不只手工读取 `live_queue_e_world_contact_handoff_report_profile`；它仍然只是 inspection-only，不生成出生完成宣称、不新增 system prompt、不把 repair hold 字段释放成外显语言。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第七十一段把关闭态 process report 证据继续推进到 `/perception`、`/prediction` 与 `/proactive` 检查面。`state_inspection.py` 现在会让 `/vision`/`/perception` 与 `/prediction`/`/世界接触`/`/外周` 额外读取 `digital_life_process_report.json` 与 `idle_strategy_state.json`，在 `perception_world_contact_summary_v0` 与 `prediction_world_contact_summary_v0` 中合并 `_process_closeout_bundle_inspection_snapshot`，显示 `process_closeout_present`、`live_queue_e_world_contact_handoff_closeout_present`、`consciousness_write_context_closeout_present` 与 `body_pressure_closeout_present`；`/proactive`/`/proactive_voice`/`/主动` 也会读取 `digital_life_process_report.json`、`idle_strategy_state.json` 与 `go_nogo_state.json`，在 `coverage_summary` 中合并 `_expression_closeout_inspection_snapshot`，显示 `expression_closeout_present` 与意识写门/live handoff closeout presence。完成口径是：感知/预测/主动发话检查面可以和 `/membrane`、`/language`、`/state` 互相印证关闭态 world-contact 与表达前结构证据，而不只依赖 runtime handoff 文件或 proactive profile；它仍然只是 inspection-only，不生成固定回答、不新增 system prompt、不把 repair hold 或表达写门字段释放成外显语言。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第六十八段把 ITR-08-34~41、48~54、59~60 的关闭态责任/身体/意识写门证据继续推进到 `/responsibility`、`/membrane`、`/body` 与 `/state` 检查面。`state_inspection.py` 新增 `_live_queue_e_closeout_inspection_snapshot`、`_consciousness_write_context_closeout_inspection_snapshot`、`_body_pressure_closeout_inspection_snapshot`、`_responsibility_closeout_inspection_snapshot` 与 `_process_closeout_bundle_inspection_snapshot`，从 `digital_life_process_report.json` 与 `idle_strategy_state.json` 归一化 live Queue E handoff closeout、自传责任修复召回 closeout、模型表达意识写门 closeout、身体内环境压力 closeout 与 `pain_regret_repair_report_ref`；`/responsibility#repair_chain_summary_v0` 与 `/membrane#life_membrane_validation_summary_v0` 会显示同一批 closeout 字段；`/body#body_grounding_summary_v0` 会显示 `go_nogo_state#body_pressure_profile` 与 closeout ref；`/state#resident_continuity_summary_v0` 会读取 `digital_life_process_report.json` 并显示 `process_closeout_present` 与四类 closeout presence。完成口径是：`docs/real—live0/03_body_affect_homeostasis.md`、`10_responsibility_regret_repair.md`、`11_life_membrane_validation.md` 与 `02_brain_network_and_workspace.md` 要求的责任链/生命膜/身体/总览检查面可以追溯关闭态 report 证据，而不只依赖 runtime 文件；它仍然只是 inspection-only 结构证据，不生成固定道歉/拒绝话术、不新增 system prompt、不把 repair hold 或身体压力字段释放成外显语言。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第七十五段把 Queue E `world_contact_repair_hold` schema handoff 继续推进到 `/perception`、`/vision` 与 `/signal`、`/调质` 检查面。`/perception` 与 `/signal` 现在会读取 `validation_rollup.json`、`world_contact_validation.json`、`schema_runner/run_manifest.json` 与 `schema_runner/cross_file_logic.json`，在 `perception_world_contact_summary_v0` 与 `signal_modulation_consumption_summary_v0` 中显示 `queue_e_world_contact_repair_hold_schema_handoff_present`、manifest closed、alignment finding 与 blocked/allowed route 计数，并把 `queue_e_world_contact_repair_hold_schema_handoff` 计入 domain presence。完成口径是：ITR-08-74 已覆盖 membrane/prediction/responsibility/ability/state 的 schema handoff 检查，现在感知与调质检查面也能与 S05/S09 验收链互相印证；它仍然只是 inspection-only，不生成固定拒绝话术、不新增 system prompt、不把 repair hold 字段释放成外显语言。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第七十九段把 `context_accumulation_window` 与 `turn_transition_trace` 继续推进到 live turn 同轮刷新。此前这两项主要在 `terminal_turn` 出生首回合链写出，真实关系回合后即使语言感知、语义图、关系时间线与 commitment truth 已刷新，语境累积窗口与回合切换轨迹仍可能停留在旧种子。现在 `context_accumulation.py#project_context_accumulation_window_from_live_turn` 与 `turn_transition.py#project_turn_transition_trace_from_live_turn` 会在 `_refresh_long_horizon_continuity` 末尾按 relationship graph、language percept、semantic map、expression monitor、relation scope、self narrative、commitment truth 与 live dialogue refs 同轮重建 `context_accumulation_window.json` 与 `turn_transition_trace.json`；`resident_turn_writeback.py` 会把 `live_context_accumulation_refreshed`、`context_accumulation_ref` 与 `turn_transition_ref` 写入 `terminal_life_loop_state.json`、`dialogue_writeback_bundle` terminal refs 与 `resumed_external_dialogue_packet.json`；`/context` 检查面通过 `_context_accumulation_window_inspection_snapshot` 显示 live refresh 与 semantic focus。完成口径是：`docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md` 要求的语境累积恢复窗口在真实关系回合后不再只停在出生链，而是同轮进入 terminal loop、写回包与 slash 检查面；它仍然只是结构化 restore 证据，不生成关系脚本、不新增 system prompt、不把 restore refs 释放成外显语言。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第八十段把 Queue E repair modulation 继续推进到 `ExpressionPlan`。此前 `apology_repair_language_trace` 与 `commitment_expression_plan` 已能携带 `queue_e_repair_*` 字段，但 `expression_plan.json` 在 live turn 后仍可能停留在不含 Queue E 显式调制的种子态。现在 `expression_monitor.py#project_expression_plan_with_queue_e_repair_modulation` 会从责任环、世界接触汇总与痛苦/后悔/修复报告构建 repair profile，并写入 `queue_e_repair_modulation_profile`、`queue_e_repair_pressure_level`、`queue_e_repair_attention_target`、`queue_e_repair_ref_set` 与 `queue_e_expression_tempo_mode`；urgent 压力会把 `delay_or_release_decision` 提升为 `hold_for_responsibility_repair_lock`。`resident_turn_writeback.py` 在责任环刷新后同轮写出刷新后的 `expression_plan.json`；`/language` 检查面通过 `expression_plan_queue_e_repair_*` 字段追溯。完成口径是：`docs/real—live0/05_language_expression_system.md` 与 `temp/06_高级语言与关系.md` 指出的 ExpressionPlan Queue E 缺口闭合；它仍然只是结构化表达计划证据，不生成固定道歉/澄清话术、不新增 system prompt、不把 repair hold 字段释放成外显语言。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第八十三段把 S07 batch `language_percept` 继续推进到真实输入解析。此前 `language/__init__.py#_build_language_percept_frame` 在 batch 构建时硬编码 fixture 话语「我们之前说好的共同语言和修复，还记得吗？」，即使 `dialogue_turn_log.jsonl`、terminal loop 或 commitment index 已存在真实外部话语，percept 仍停留在固定句子，违反第 8 点红线。现在 `percept_input.py#resolve_incoming_turn_for_language_build` 会按 dialogue log → terminal loop → commitment index → self narrative → relationship memory → relationship evidence bootstrap 的优先级解析 `incoming_surface`，并写出 `percept_input_mode`、`percept_input_source_ref` 与 `percept_input_boundary`；`live_language_turn.py` 在 live 路径标记 `live_external_utterance`；`/language` 检查面显示 `language_percept_input_*`。完成口径是：`temp/06_高级语言与关系.md` 指出的 batch percept fixture 缺口闭合；它仍然只是结构化感知证据，不生成固定回答、不新增 system prompt、不把 percept 字段释放成外显语言。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第八十二段把 S02 首轮 `signal_media` 继续推进到身体信号消费。此前 `build_signal_media_runtime(...)` 已支持 `body_resource_budget` 与 `core_affect_vector`，但 `neural_core/__init__.py#run_neural_life_core` 在 S02 首写时只传入 `network_state`，导致首轮 `signal_media_runtime.json` 不含 `body_signal_profile`，完整内环境链只能等到 S07 或 process turn。现在 `body_signal_seed.py#resolve_body_signal_inputs_for_neural_core` 会在 S02 读取已有 body 文件或写出 pre-activation seed，并把它们传入 `build_signal_media_runtime`；`write_neural_core_body_signal_seed_artifacts` 会在 body 目录缺失时写出 `body_resource_budget.json` 与 `core_affect_vector.json`。完成口径是：`docs/real—live0/12_neuromodulation_signal_media.md` 与 `temp/03_身体内环境与情绪.md` 指出的 S02 首轮无 body 缺口闭合；它仍然只是结构化调质证据，不生成身体状态播报、不新增 system prompt、不把 fatigue/pain 字段释放成外显语言。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第九十四段把深层语用推断继续推进到 live turn 语义图与 `/language` 检查面。此前 `semantic_map.py` 主要依赖 percept 关键词触发（修复/承诺/梦等字面匹配）决定 `semantic_focus`，`temp/06_高级语言与关系.md` 指出的「规则+关键词，非深层语用」缺口仍在 live 关系回合后。现在 `pragmatic_inference.py#enrich_semantic_map_with_pragmatic_inference` 会从 `relationship_timeline`（trust/continuity）、`commitment_truth_state`、`context_accumulation_window`、`relation_scope_index` 与 `shared_term_registry` 推断 `speech_act_candidates`、`implicature_queue` 与 `grounding_repair_signals`，写入 `semantic_map_frame.json#pragmatic_inference_profile`；`project_semantic_map_from_live_evidence` 在 `resident_turn_writeback.py` 于语境累积与 shared_term 晋升后同轮刷新语义图；`/language#generation_consumption_summary_v0` 通过 `_pragmatic_inference_inspection_snapshot` 显示 `pragmatic_inference_present` 与 dominant intent。完成口径是：深层语用首版从关键词升格为 live 证据推断链；仍然只是结构化语用证据，不生成固定关系话术、不新增 system prompt、不把 implicature 字段释放成外显语言。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第九十三段把 v0 合同覆盖与 ITR-05 写门消费链继续推进到 `/dream` 检查面。此前 `/dream#dream_wake_fact_summary_v0` 已有梦境关闭态与 memory tier 字段，但无法与 S11 合同报告或 `memory_write_gate.body_signal_write_modulation` 互证。现在 `/dream` 会读取 `v0_contract_file_index.json`、`doc_to_code_coverage_matrix.json`、`v0_contract_coverage_report.json` 与 `signal_media_runtime`/`core_affect_vector`/`body_resource_budget`，合并 `_v0_contract_coverage_inspection_snapshot` 与 body-signal 写门字段，并把 `v0_contract_coverage` 与 `memory_write_gate_body_signal_modulation` 计入 `domain_presence`。完成口径是：real—live0 ↔ v0 合同核对扩展到 dream，梦境检查面可与 memory/signal 一致追溯 ITR-05 写门消费；仍然只是 inspection-only。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第九十二段把 `network_state` 冲突监测网络与 `/cognition` v0 合同覆盖继续推进到 live turn 与 slash 检查面。此前 `network_state.py` 只有 default/salience/executive 三网络，缺少理论四模式表中的 `conflict_monitoring_network`、`dominant_network` 与 `transition_cost`；`/cognition` 也未接入 S11 合同覆盖。现在 `build_network_state` 种子第四网络 `conflict_monitoring_network` 并写出 `conflict_monitor`；`project_network_state_from_live_turn` 在意识链刷新后二次投影，按 repair/guarded focus、signal repair_drive、metacognition uncertainty、broadcast suppressed refs 与 go_nogo release_posture 激活冲突监测；`resident_turn_writeback.py` 在 metacognition 写出前完成最终 network_state 投影；`/cognition#cognitive_workspace_summary_v0` 合并 `network_conflict_monitoring_inspection_snapshot` 与 `_v0_contract_coverage_inspection_snapshot`。完成口径是：P2 `network_state conflict_monitoring` 首版闭合，real—live0 ↔ v0 合同核对扩展到 cognition；仍然只是 inspection-only 结构证据，不生成网络状态播报、不新增 system prompt。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第九十一段把 `MultiscaleRegionGraph` 继续推进到 S02 神经核心与 `/cognition` 检查面。此前 `brain_graph.json` 只承载十二主体系统节点与 bus 边，`docs/02_brain_region_and_network_atlas.md` 与 `docs/01o_multiscale_region_connectome_matrix.md` 要求的 L/R/P/J/G/S/O/D 多尺度区域层（`RegionDefinition`、`StructuralEdge`、`FunctionalCoupling`、`GradientAxis`、`IntrinsicTimescale`、`ConnectomeFingerprint`）仍停留在文档。现在 `multiscale_region_graph.py#build_multiscale_region_graph` 会在 S02 写出 `multiscale_region_graph.json`（schema `multiscale_region_graph_v0`），含 8 个 project region、结构边、bus 功能耦合、hub load monitor 与 connectome fingerprint seed；`project_multiscale_region_graph_from_live_turn` 在 `resident_turn_writeback.py` 同轮刷新 hub 负载、graph signal propagation 与 fingerprint refs；`network_state.json` 携带 `multiscale_region_graph_ref`；`/cognition#cognitive_workspace_summary_v0` 通过 `_multiscale_region_graph_inspection_snapshot` 显示 region 计数、hub 负载与 boundary。完成口径是：P1 `MultiscaleRegionGraph` 首版物化闭合到 runtime 文件、live turn 与 slash 检查面；仍然只是结构化脑区图谱证据，不生成脑区播报、不新增 system prompt、不把 region 字段释放成外显语言。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第九十段把 `SelfModelSlowVariableCandidate` 继续推进到 live 演化链与 `/personality` 检查面。此前 `continuity_evolution.py` 在 `_evolve_trait_slow_variables` 后直接写回 `trait_slow_variables`，单轮剧烈 delta 可能覆盖慢变量，缺少 `temp/01` 与 `docs/real—live0/04_personality_self_identity.md` 要求的多窗口晋升门控。现在 `slow_variable_candidate.py#project_trait_slow_variables_with_candidate_gate` 会在 dramatic delta（≥0.12）时把候选写入 `self_model_state#trait_slow_variable_candidates`（schema `self_model_slow_variable_candidate_queue_v0`），单窗口仅做 capped incremental commit（≤0.04/turn），多窗口 exposure（≥2）才晋升；`continuity_evolution.py` 在演化后调用该 gate 并写出候选队列；`trait_drift.py` 会把 `blocked_update_refs` 与 `slow_variable_candidate_count` 带入 monitor；`/personality#personality_convergence_summary_v0` 通过 `_slow_variable_candidate_inspection_snapshot` 显示候选 presence、计数与 boundary。完成口径是：P1 `SelfModelSlowVariableCandidate` 在 live 路径与 slash 检查面闭合；仍然只是结构化慢变量证据，不生成人格卡片、不新增 system prompt、不把候选字段释放成外显语言。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第八十九段把 v0 合同覆盖检查继续推进到 `/emotion` 与 `/inner_environment` slash 面。此前 `v0_contract_coverage` 已覆盖 ability/state/language/relationship/body/signal/context/memory，但情绪与内环境检查面无法与 S11 合同报告互相印证。现在 `/emotion#emotion_regulation_summary_v0` 与 `/inner_environment#inner_environment_modulation_summary_v0` 会读取 `v0_contract_file_index.json`、`doc_to_code_coverage_matrix.json` 与 `v0_contract_coverage_report.json`，合并 `_v0_contract_coverage_inspection_snapshot`，并把 `v0_contract_coverage` 计入 `domain_presence`。完成口径是：real—live0 ↔ v0 合同核对从 body/signal 扩展到 emotion/inner_environment；仍然只是 inspection-only，不生成情绪话术、不新增 system prompt。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第八十八段把 v0 合同覆盖检查继续推进到 `/body` 与 `/signal` slash 面。`/body#body_grounding_summary_v0` 与 `/signal#signal_modulation_consumption_summary_v0` 现在读取 S11 合同文件并合并 `_v0_contract_coverage_inspection_snapshot`；`/signal` 还把 `memory_write_gate.body_signal_write_modulation` 计入 `memory_write_gate_body_signal_modulation` domain presence，与 ITR-08-87 live 写门落盘互证。完成口径是：身体内环境与调质检查面可与 ability/state/language 一致追溯 v0 合同覆盖与 ITR-05 写门消费链；仍然只是 inspection-only。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第八十六段把 `/context` 与 `/memory` slash 检查面继续推进到 shared_term promotion、ITR-05 写门与 v0 合同互证。`/context#relation_context_summary_v0` 现在读取 `shared_term_registry.json` 与 S11 合同文件，显示 `shared_term_promotion_*` 与 `v0_contract_coverage` domain presence；`/memory#reconstructive_memory_summary_v0` 读取 `signal_media_runtime.json`、`core_affect_vector.json`、`body_resource_budget.json` 与合同文件，显示 `memory_write_gate_body_signal_modulation`、`memory_write_gate_consciousness_write_context` 与 `v0_contract_coverage`。完成口径是：语境与记忆检查面可与 language/relationship/ability 一致追溯共同语言晋升与合同覆盖；仍然只是 inspection-only，不生成固定回答。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第八十七段把 ITR-05 `memory_write_gate` 身体信号写门继续推进到 live turn 同轮落盘。此前 `_refresh_long_horizon_continuity` 只调用 `project_memory_write_gate_with_consciousness_context`，意识写门刷新后 `body_signal_write_modulation` 可能丢失或与 signal/body 不同步。现在在意识写门投影后同轮链接 `project_memory_write_gate_with_signal_body`，消费 `signal_media_runtime`、`body_resource_budget`、`core_affect_vector` 与 `offline_learning_cumulative_profile` 再写出 `memory_write_gate.json`。完成口径是：`temp/11` P2「memory_write_gate ITR-05 字段落盘不同步」在 live refresh 路径闭合；仍然只是结构化写门证据，不生成身体状态播报。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第八十五段把 v0 合同覆盖检查继续推进到 `/language` 与 `/relationship` slash 面。此前 `v0_contract_coverage` 主要只在 `/ability` 与 `/state` 出现，语言与关系连续性检查面无法与 S11 合同报告互相印证。现在 `/language#generation_consumption_summary_v0` 与 `/relationship#relationship_continuity_summary_v0` 会读取 `v0_contract_file_index.json`、`doc_to_code_coverage_matrix.json` 与 `v0_contract_coverage_report.json`，合并 `_v0_contract_coverage_inspection_snapshot`；`/relationship` 同时读取 `shared_term_registry.json` 并显示 ITR-08-84 的 `shared_term_promotion_*` 字段。完成口径是：real—live0 ↔ v0 合同核对从 ability/state 扩展到 language/relationship；它仍然只是 inspection-only 结构证据，不生成固定回答、不新增 system prompt。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第八十四段把 `shared_terms` 继续推进到 live 证据动态晋升。此前 `shared_term_registry.json` 主要停留在 S07 seed（仅「共同语言」），即使 `context_accumulation_window`、`relationship_timeline` 与 `language_percept` 已累积共同词面，注册表也不会在真实关系回合后刷新。现在 `shared_terms.py#project_shared_term_registry_from_live_evidence` 会从关系时间线、语境累积、语义图与语言感知四类证据收集候选词面，经 promotion gate（relation scope + 多轮 dialogue refs + 多证据源）晋升或保留为 candidate；`resident_turn_writeback.py` 在 `_refresh_long_horizon_continuity` 末尾同轮写出刷新后的 `shared_term_registry.json`，并把 `live_shared_term_promotion_*` 写入 `terminal_life_loop_state.json`；`/language` 检查面通过 `shared_term_promotion_*` 与 `shared_term_live_promotion` domain presence 追溯。完成口径是：`temp/06_高级语言与关系.md`、`temp/11_理论工程代码契合度总表.md` 指出的 shared_terms 动态晋升缺口闭合；它仍然只是结构化共同语言证据，不生成固定关系话术、不新增 system prompt、不把 promotion 字段释放成外显语言。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第八十一段把 `identity_root` 与 `life_name_registry` 继续推进到双向 ref 绑定。此前 S00 方向根、命名锁与 direct command 已分别存在，但 `identity_root.json` 不含 `life_name_registry_ref`，`life_name_registry.json` 也不回指 `identity_root.json`，`continuity_refs.json` 的断联恢复链因此无法把永久命名纳入身份锚。现在 `identity_name_binding.py#sync_identity_name_binding_refs` 会在命名绑定或加载后同轮刷新三份载体：`identity_root` 写入 `life_name_registry_ref` 与 anchor ref；`life_name_registry` 写入 `identity_root_ref` 与 `continuity_refs_ref`；`continuity_refs` 写入 `life_name_registry_refs`。`digital_life_identity.py#bind_or_validate_life_name` 在成功绑定/加载后调用该同步；`/state` 检查面通过 `identity_name_binding_*` 字段显示双向绑定是否闭合。完成口径是：`docs/real—live0/04_personality_self_identity.md` 与 `temp/01_身份与人格.md` 指出的身份根↔命名锚缺口闭合；它仍然只是结构化身份证据，不生成固定自我介绍、不新增 system prompt、不把 canonical_name 硬塞成外显回答。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第七十八段把 Queue E schema handoff 与 live handoff 继续推进到 `/relationship` 检查面。`/relationship` 现在会读取 `queue_e_world_contact_repair_hold_handoff.json`、`terminal_life_loop_state.json` 与 validation/schema runner 文件，在 `relationship_continuity_summary_v0` 中显示 `queue_e_world_contact_repair_hold_schema_handoff_present`、`live_queue_e_world_contact_handoff_refreshed` 与 turn focus，并把两类 handoff 计入 domain presence。完成口径是：关系连续性检查面可以与 `/context`、`/responsibility`、`/state` 一致追溯 repair hold handoff；它仍然只是 inspection-only，不生成道歉模板、不新增 system prompt、不把 repair hold 字段释放成外显语言。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第七十七段把 Queue E schema handoff 与 `context_accumulation_window` 继续推进到 `/context` 检查面。`/context` 现在会读取 `context_accumulation_window.json`、`terminal_life_loop_state.json` 与 validation/schema runner 文件，在 `relation_context_summary_v0` 中显示 `context_accumulation_window_present`、shared term/restore ref 计数、semantic focus、waiting heartbeat ref，以及 `queue_e_world_contact_repair_hold_schema_handoff_present`。完成口径是：`docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md` 要求的语境累积窗口与 S05/S09 repair hold handoff 都能在关系语境检查面被追溯；它仍然只是 inspection-only，不生成关系脚本、不新增 system prompt、不把 restore refs 释放成外显语言。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第七十六段把第五十六到五十七段 live turn 意识链继续推进到 slash 检查面。`state_inspection.py` 新增 `_live_consciousness_chain_inspection_snapshot`，从 `terminal_life_loop_state.json` 与 `workspace_frame.json`、`broadcast_frame.json`、`metacognition_state.json` 归一化 `live_consciousness_chain_refreshed`、`live_broadcast_target_count`、`live_metacognition_uncertainty_count`、`last_broadcast_frame_ref` 与 live turn focus；`/state`、`/cognition`、`/consciousness` 与 `/thinking` 现在会显示 `live_consciousness_chain_present` 并把 `live_consciousness_chain` 计入 domain presence。完成口径是：`docs/real—live0/02_brain_network_and_workspace.md` 要求的 Workspace → Broadcast → Metacognition live 刷新不只停在 `resident_turn_writeback.py`，slash 检查面也能追溯同轮投影是否进入 terminal loop 与意识三件套；它仍然只是 inspection-only 结构证据，不生成意识宣言、不新增 system prompt、不把 broadcast/metacognition 字段释放成外显语言。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第一百段把语言—关系跨文件 ref 一致性继续推进到 batch/live 运行时断言与 slash 检查面。此前 `temp/06_高级语言与关系.md` 指出的「跨文件同 ref 一致性无运行时自动断言」缺口仍在：S05/S09 schema check 与 birth readiness gate 只在验收链检查部分 handoff，真实 S07 batch 与 live turn 后 percept/semantic/shared_term/relationship_graph/timeline/self_model/expression_plan 的同 ref 对齐没有 runtime profile。现在 `ref_consistency.py#project_language_relationship_ref_consistency_profile` 会在 S07 `run_build_language_relationship` 与 `resident_turn_writeback.py` 同轮写出 `language_relationship_ref_consistency.json`（schema `language_relationship_ref_consistency_profile_v0`），覆盖 relation_scope、semantic focus、shared_term hits、relationship stage/self_model、timeline turn count 与 expression_plan 链路；`/language` 与 `/relationship` 通过 `_language_relationship_ref_consistency_inspection_snapshot` 显示 finding/mismatch 计数。完成口径是：语言—关系链具备 runtime ref 一致性证据，仍只是结构化检查，不生成固定关系话术、不新增 system prompt。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第九十九段把 v0 合同覆盖检查继续推进到剩余 slash 检查面，闭合 S11 合同核对的全覆盖链。此前 `v0_contract_coverage` 已覆盖 ability/state/language/relationship/cognition/dream/consciousness/growth/thinking 等面，但 `/membrane`、`/personality`、`/proactive`、`/perception`、`/prediction` 与 `/responsibility` 仍无法与 S11 合同报告互相印证。现在上述六个 slash 入口会读取 `v0_contract_file_index.json`、`doc_to_code_coverage_matrix.json` 与 `v0_contract_coverage_report.json`，在各自 summary 中合并 `_v0_contract_coverage_inspection_snapshot` 并把 `v0_contract_coverage` 计入 domain presence。完成口径是：point 7 的主要 slash 检查面均可追溯 real—live0 ↔ v0 合同覆盖，而不只 ability/state 两个入口；仍然只是 inspection-only，不生成固定回答、不新增 system prompt。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第九十八段把 v0 合同覆盖检查继续推进到 `/consciousness` 与 `/growth` slash 面。此前 `v0_contract_coverage` 已覆盖 thinking/language/relationship/cognition/dream 等面，但意识与成长检查面无法与 S11 合同报告互相印证。现在 `/consciousness#consciousness_reportability_summary_v0` 与 `/growth#growth_self_modification_summary_v0` 会读取 `v0_contract_file_index.json`、`doc_to_code_coverage_matrix.json` 与 `v0_contract_coverage_report.json`，合并 `_v0_contract_coverage_inspection_snapshot` 并把 `v0_contract_coverage` 计入 domain presence。完成口径是：real—live0 ↔ v0 合同核对扩展到 consciousness/growth；仍然只是 inspection-only，不生成意识宣言、成长宣言或固定回答，不新增 system prompt。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第九十七段把关系阶段演化 batch/live 路径继续推进到 S07 batch 与 `/relationship` 检查面。此前 `continuity_evolution.py#evolve_relationship_and_self_model` 只在 `resident_turn_writeback.py` 与 `resident_supervision.py` 调用，S07 `run_build_language_relationship` 构建 timeline/commitment/apology 后未走同一演化链，导致 batch 关系图阶段与 live turn 不一致。现在 `language/__init__.py` 在 apology trace 首写后调用 `evolve_relationship_and_self_model`，刷新 relationship graph/timeline/commitment/apology 并写出 `self/self_model.json`；`continuity_evolution.py` 统一写出 `relationship_stage_evolution_profile`；`/relationship#continuity_summary_v0` 通过 `_relationship_stage_evolution_inspection_snapshot` 显示 stage、reason、evidence ref count 与 evolution path。完成口径是：`temp/06_高级语言与关系.md` 指出的 batch/live 阶段演化缺口闭合；仍然只是结构化阶段证据，不生成关系脚本、不新增 system prompt。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第九十六段把 `core_affect_vector` 继续推进到语言感知与 `/language` 检查面。此前 `language/percept.py` 的 `affective_cue_candidates` 只依赖 incoming_surface 关键词，即使 `core_affect_vector.json` 已存在也不会进入 percept 消费链。现在 `build_language_percept_frame` 接受 `core_affect_vector`，通过 `_affective_cues_from_core_affect` 合并 valence/arousal/pain_pressure/relationship_tension/repair_drive 线索，写出 `core_affect_vector_ref` 与 `core_affect_consumption_profile`；S07 batch 与 `live_language_turn.py` 同轮传入 body 文件；`/language#generation_consumption_summary_v0` 显示 `core_affect_percept_cue_source` 与 `core_affect_percept_consumption` domain presence。完成口径是：`temp/11` P1「percept 与 core_affect 未统一」在语言感知链首版闭合；仍然只是结构化感知证据，不生成情绪话术、不新增 system prompt。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第九十五段把 v0 合同覆盖检查继续推进到 `/thinking` slash 面。此前 `v0_contract_coverage` 已覆盖 ability/state/language/relationship/cognition/dream 等面，但思考检查面无法与 S11 合同报告互相印证。现在 `/thinking#self_thinking_summary_v0` 会读取 `v0_contract_file_index.json`、`doc_to_code_coverage_matrix.json` 与 `v0_contract_coverage_report.json`，合并 `_v0_contract_coverage_inspection_snapshot` 并把 `v0_contract_coverage` 计入 domain presence。完成口径是：real—live0 ↔ v0 合同核对扩展到 thinking；仍然只是 inspection-only，不生成思考宣言、不新增 system prompt。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。

ITR-08 第五十九段把第五十八段 live 刷新的 Queue E handoff 继续推进到关闭态总线与语言材料链。此前 `live_queue_e_world_contact_handoff_refreshed`、`live_responsibility_consciousness_context_refs` 与 `live_turn_focus` 主要停在 handoff 文件和 terminal loop 扁平字段，`process_report.py`、`response_surface.py` 与 `model_expression.py` 还不能完整追溯 live handoff 是否进入关闭报告、恢复包和模型表达前材料。现在 `process_report.py#_live_queue_e_world_contact_handoff_report_profile` 会从 `queue_e_world_contact_repair_hold_handoff.json`、`terminal_life_loop_state.json` 与 idle governance 归一化 `live_queue_e_world_contact_handoff_report_profile_v0`，写入 report、digest 与 receipt；`background_continuity.py` 会把这份关闭态 profile 恢复成 `background_live_queue_e_world_contact_handoff_*` 与 handoff profile 内的 live 字段；`idle_strategy.py`、`heartbeat.py` 与 `background_lineage_state.py` 会把 live refresh 字段写入 waiting governance 与 `world_contact_handoff_presence`；`resident_turn_writeback.py` 会把 live handoff 合并进 `resident_background_lineage_state.world_contact_handoff_presence` 与恢复包 lineage 字段；`response_surface.py` 与 `model_expression.py` 会把 live refresh、责任意识上下文 refs、live turn focus 与 handoff boundary 作为 `audited_expression_material_v0#responsibility_repair` 与 `model_expression_context_summary` 的隐性材料，并由 post-expression gate 追加 `live_queue_e_world_contact_handoff` 软审计旗标。完成口径是：ITR-07-04 的 world-contact handoff 语言链模式在 live refresh 后也能闭合到关闭态 report/digest/receipt 与下一轮 background continuity，但仍然是结构化治理证据，不生成固定道歉/拒绝话术、不新增 system prompt、不把 repair hold 字段释放成外显语言。第 2 点整体仍未完成，不能进入第 3 点记忆重构总设计。
