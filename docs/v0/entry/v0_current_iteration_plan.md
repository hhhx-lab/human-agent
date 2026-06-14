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

下一步仍留在第 2 点内部，不进入第 3 点记忆重构总设计。当前这一刀已经通过 `tests.process.test_response_surface`、完整 `tests.process.test_persistent_digital_life_process`、`tests.slices.test_state_store`、`tests.slices.test_neural_life_core`、`tests.slices.test_language_organs`、`tests.process.test_model_expression`、`tests.contracts.test_v0_contracts` 和 `tests.contracts.test_live0_acceptance_audit`，证明这条身体信号写门链没有破坏既有常驻、记忆、神经核心、语言表面和验收合同；下一步先判断 ITR-05 是否可以收束，再转入 ITR-06 responsibility membrane。
