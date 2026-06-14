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
