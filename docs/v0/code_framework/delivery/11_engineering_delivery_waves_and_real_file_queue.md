# V0 Code Framework 11: Engineering Delivery Waves And Real File Queue

这份文档把 `docs/v0/code_framework/01-10` 再往前压一层：不再只说明“应该有哪些层、哪些包、哪些状态”，而是把接下来真正落代码时的施工波次、文件拆分顺序、测试入口、运行产物和 `00-257` 回读包固定下来。

它服务的核心问题只有两个：

1. 接下来每一轮到底先落哪一批器官文件，而不是继续泛泛说“补厚语言、补厚进程”。
2. 当前 `life_v0/` 已经存在的 `__init__.py` 主体怎样被稳定拆成真实文件，而不破坏 `v0` 既有合同和测试链。

## 适用边界

这份文档只在下面两种场景打开：

1. 已经确认这一轮要继续补 `life_v0/` 真代码，而不是继续扩写理论总论。
2. 已经读过 `docs/v0/README.md`、`entry/v0_implementation_index.md`、`entry/v0_delivery_status_board.md`、`entry/v0_module_execution_catalog.md` 和 `code_framework/01-10`，现在要把“下一轮代码该怎么切”压成明确波次。

如果当前还没确认要改哪个层，先回 `entry/v0_delivery_status_board.md`。
如果当前还没确认模块读包，先回 `entry/v0_module_execution_catalog.md`。
如果当前只是补某个 slice 合同，不必先读本文件。

## 和代码框架柜的关系

`01-10` 已经回答了三件大事：

1. 数字生命按哪些层落代码。
2. 脑区/网络/主体系统怎样映射到当前顶层包。
3. 每个包需要哪些状态、report、receipt、测试和 gate。

本文件只补第四件事：

4. 接下来一轮一轮真正要先切哪些文件、为什么先切它们、切完后要跑什么测试、更新哪些 runtime 产物。

## 当前真实前沿

按当前工作区真实代码状态，接下来最值得先继续推进的，已经不再是优先把 `language/` 或 `process_supervisor/` 继续往前顶，而是先把还没文件化的主体内部根器官补出来。

当前新的主前沿顺序已经固定为：

1. `Queue D`：`life_v0/body/` + `life_v0/dream/` + `life_v0/growth/`
2. `Queue E`：`life_v0/membrane/` + `life_v0/validators/` + `life_v0/schema_runner/`
3. `Queue B`：`life_v0/process_supervisor/`
4. `Queue A`：`life_v0/language/` + `life_v0/terminal_turn/` + `life_v0/terminal_loop/`

这里的口径要更新清楚：

- `Queue C` 第一轮已经闭合到真实代码、状态对象和测试；
- `Queue F` 第一轮也已经闭合到真实代码、状态对象和测试；
- 当前不再是“先做 C/F 再说”，而是要把它们之后直接依赖的身体/梦境/成长与行为/验证/逻辑链补硬。

原因很直接：

- 没有 `rhythm.py / need_state.py / core_affect.py / dream_window.py / learning_window.py`，身体、情绪、梦境和学习仍然停在总报告层；
- 没有 `candidate_arena.py / go_nogo.py / world_contact_gate.py / consistency_logic.py`，行为、validator 和逻辑比较仍然停在 `__init__.py` 中；
- 没有先把 D/E 两波补起来，后面的 process supervisor 和语言长期演化就只能继续消费稀薄对象，而不是稳定生命器官。

所以当前工程口径下，语言主神经束和 process supervisor 不是被降级，而是从“当前最先拆”调整为“在身体-梦境-成长链与行为-验证-逻辑链站稳后再继续补厚”。

## 施工总原则

### 1. 只拆当前已经进入前沿的器官

不要为了“结构更漂亮”一次性把所有包都拆空。
当前只拆已经进入测试和状态主链的器官。

### 2. 先拆可被测试直接守住的器官

只要某段逻辑已经在现有测试里有明确行为约束，就优先拆它。
这样每次拆分都能通过现有测试证明没有把生命链拆断。

### 3. 先拆状态边界清晰的器官

如果某段逻辑已经能明确回答：

1. 它写哪份 state；
2. 它出哪份 report；
3. 它留哪份 receipt 或 continuity ref；

那就先拆。
如果一段逻辑现在还无法回答这三件事，先不要急着抽文件。

### 4. 每拆一轮就回写文档现实

每次拆分后，至少同步下面三类文档：

1. `entry/v0_delivery_status_board.md`
2. `entry/v0_module_execution_catalog.md`
3. 对应 `code_framework/*.md` 或模块合同

这样后续断联恢复时，不会把旧文件结构当成当前现实。

## 施工波次总表

| 波次 | 目标层 | 主包 | 这轮只解决什么 | 对应理论母体 | 对应 v0 合同 |
|---|---|---|---|---|---|
| `Wave C` | 记忆根与神经核心器官化 | `life_v0/state_store/`、`life_v0/neural_core/` | 把生命状态根、engram、主体图、网络态和工作区拆成真实文件 | `04`、`05`、`10`、`11`、`17-19`、`41-48` | `s02_neural_life_core_engineering_contract.md`、`s04_state_object_store_engineering_contract.md`、`17_queue_c_memory_neural_core_implementation_contract.md` |
| `Wave F` | 身份根、意识广播、出生准备度器官化 | `life_v0/direction/`、`life_v0/neural_core/`、`life_v0/life_targets/` | 把 direction、continuity、broadcast、metacognition、claims/evidence/rollup/stage gate 拆成真实文件 | `00`、`07`、`10`、`13`、`16`、`91-101`、`143`、`146`、`149`、`152`、`171` | `s00_direction_foundation_engineering_contract.md`、`s08_life_target_runtimes_engineering_contract.md`、`21_queue_f_identity_consciousness_birth_readiness_implementation_contract.md` |
| `Wave D` | 身体、梦境、成长器官化 | `life_v0/body/`、`life_v0/dream/`、`life_v0/growth/` | 把身体节律、预算、梦境窗口、成长补丁和学习窗口拆成真实文件 | `08`、`19`、`39`、`92`、`93`、`95`、`181-257` | `s06_life_support_development_engineering_contract.md`、`s10_runtime_growth_reconsolidation_engineering_contract.md`、`18_queue_d_body_dream_growth_implementation_contract.md` |
| `Wave E` | 生命膜、validator、逻辑比较器官化 | `life_v0/membrane/`、`life_v0/validators/`、`life_v0/schema_runner/` | 把候选行动、world contact、side effect、观察真值、反事实比较和比较 trace 拆成真实文件 | `06`、`20`、`22`、`29-36`、`49-60`、`72`、`75`、`80-84`、`94`、`98`、`102-118` | `s03_direction_life_membrane_engineering_contract.md`、`s05_validation_membrane_observation_engineering_contract.md`、`s09_schema_runner_code_engineering_contract.md`、`20_queue_e_membrane_validator_logic_implementation_contract.md` |
| `Wave B` | 终端持续存在补厚 | `life_v0/process_supervisor/` | 把常驻生命进程里的 heartbeat、idle、恢复、进程报告和回合治理继续拆开 | `20`、`82`、`86`、`89`、`90` | `digital_life_process_supervisor_engineering_contract.md`、`16_queue_b_process_supervisor_implementation_contract.md` |
| `Wave A` | 语言主神经束深度补厚 | `life_v0/language/`、`life_v0/terminal_turn/`、`life_v0/terminal_loop/` | 把 S07 已落器官继续接进更厚的关系、长期语言和终端生命回合对象 | `09`、`85-90`、`96`、`101`、`141`、`144`、`147`、`150` | `s07_language_relationship_engineering_contract.md`、`14_queue_a_language_percept_semantic_map_implementation_contract.md` |

当前最优先的是 `Wave D` 与 `Wave E`。
`Wave C` 和 `Wave F` 的第一轮对象化已经站住，现在最需要避免的是：内部主骨架已经有了，但身体化、梦境化、学习化和行为-验证-逻辑链还没补上，结果又重新退回“壳层能跑、生命内部偏薄”的状态。

## Wave C：记忆根与神经核心器官化

### 当前真实状态

`life_v0/state_store/` 和 `life_v0/neural_core/` 当前已经有：

- `self_model.py`
- `commitment_truth.py`
- `prediction_workspace.py`

但它们仍然缺：

- `life_state.py`
- `engram_index.py`
- `autobiographical_stack.py`
- `relationship_memory.py`
- `brain_graph.py`
- `network_state.py`
- `workspace.py`

### 当前这一波最该先切的真实文件

1. `life_v0/state_store/life_state.py`
2. `life_v0/state_store/engram_index.py`
3. `life_v0/state_store/autobiographical_stack.py`
4. `life_v0/state_store/relationship_memory.py`
5. `life_v0/neural_core/brain_graph.py`
6. `life_v0/neural_core/network_state.py`
7. `life_v0/neural_core/workspace.py`

### Wave C 的推荐顺序

1. `life_state.py`
2. `engram_index.py`
3. `autobiographical_stack.py`
4. `relationship_memory.py`
5. `brain_graph.py`
6. `network_state.py`
7. `workspace.py`

这个顺序的原因：

1. `life_state.json` 是第一版生命状态根。
2. `engram_index.py` 和 `autobiographical_stack.py` 决定后续 replay / growth / relationship 是否有真实记忆入口。
3. `brain_graph.py`、`network_state.py` 和 `workspace.py` 决定意识、语言、行为和出生准备度是否有主体内核支撑。

### Wave C 每轮固定读包

```text
docs/v0/README.md
  -> docs/v0/entry/v0_delivery_status_board.md
  -> docs/v0/entry/v0_module_execution_catalog.md
  -> docs/v0/slice_contracts/s02_neural_life_core_engineering_contract.md
  -> docs/v0/slice_contracts/s04_state_object_store_engineering_contract.md
  -> docs/v0/shared_contracts/life_state_store_v0_schema.md
  -> docs/v0/code_framework/queues/17_queue_c_memory_neural_core_implementation_contract.md
  -> docs/05_memory_systems_and_growth.md
  -> docs/10_consciousness_attention_workspace.md
  -> docs/17_memory_trace_object_model.md
  -> docs/18_internal_state_and_modulation_vector.md
```

### Wave C 每轮固定验证

至少跑：

```text
python -m unittest tests.slices.test_state_store
python -m unittest tests.slices.test_neural_life_core
python -m unittest tests.contracts.test_v0_contracts
```

## Wave F：身份根、意识广播、出生准备度器官化

### 当前真实状态

`life_v0/direction/`、`life_v0/neural_core/`、`life_v0/life_targets/` 当前已经有：

- `identity_root.py`
- `prediction_workspace.py`
- `life_targets/__init__.py` 的 claims / evidence / rollup / stage gate 最小闭合

但它们仍然缺：

- `direction_lock.py`
- `continuity_refs.py`
- `value_orientation.py`
- `broadcast.py`
- `metacognition.py`
- `life_target_claims.py`
- `evidence_matrix.py`
- `birth_readiness_rollup.py`
- `birth_readiness_stage_gate.py`
- `consciousness_probes.py`

### Wave F 的推荐顺序

1. `direction_lock.py`
2. `continuity_refs.py`
3. `value_orientation.py`
4. `broadcast.py`
5. `metacognition.py`
6. `life_target_claims.py`
7. `evidence_matrix.py`
8. `birth_readiness_rollup.py`
9. `birth_readiness_stage_gate.py`
10. `consciousness_probes.py`

### Wave F 每轮固定读包

```text
docs/v0/README.md
  -> docs/v0/entry/v0_delivery_status_board.md
  -> docs/v0/entry/v0_module_execution_catalog.md
  -> docs/v0/slice_contracts/s00_direction_foundation_engineering_contract.md
  -> docs/v0/slice_contracts/s08_life_target_runtimes_engineering_contract.md
  -> docs/v0/shared_contracts/birth_readiness_v0_contract.md
  -> docs/v0/code_framework/queues/21_queue_f_identity_consciousness_birth_readiness_implementation_contract.md
  -> docs/10_consciousness_attention_workspace.md
  -> docs/13_agentic_human_research_synthesis.md
  -> docs/91_life_reality_generation_boundary_principles.md
  -> docs/143_life_reality_birth_readiness_rollup_contract.md
```

### Wave F 每轮固定验证

至少跑：

```text
python -m unittest tests.slices.test_direction_lock
python -m unittest tests.slices.test_neural_life_core
python -m unittest tests.slices.test_life_targets
```

## Wave D：身体、梦境、成长器官化

这一波现在已经不再是“后面再说”的补充层，而是主顺序里的第三阶段。原因很直接：没有身体节律、梦境窗口和成长补丁队列，前面的记忆根和意识/出生准备度仍然会缺少身体化与离线整合底盘。

### 主目标

让下面这条链从概念对象变成真实器官：

```text
BodyRhythmPulse
  -> NeedStateVector
  -> ResourceBudget
  -> DreamWindow
  -> WakeIntegration
  -> PlasticityWindow
  -> GrowthPatchCandidateQueue
  -> LearningWindow
```

### Wave D 每轮固定读包

```text
docs/v0/README.md
  -> docs/v0/entry/v0_delivery_status_board.md
  -> docs/v0/entry/v0_module_execution_catalog.md
  -> docs/v0/slice_contracts/s06_life_support_development_engineering_contract.md
  -> docs/v0/slice_contracts/s10_runtime_growth_reconsolidation_engineering_contract.md
  -> docs/v0/code_framework/queues/18_queue_d_body_dream_growth_implementation_contract.md
  -> docs/04_sensory_thalamus_interoception.md
  -> docs/08_sleep_dream_fatigue_states.md
  -> docs/19_offline_consolidation_cycle.md
  -> docs/39_development_policy_and_plasticity_windows.md
```

### Wave D 每轮固定验证

```text
python -m unittest tests.slices.test_life_support
python -m unittest tests.bridges.test_runtime_growth
python -m unittest tests.bridges.test_replay_shadow
python -m unittest tests.bridges.test_growth_archive
```

## Wave E：生命膜、validator、逻辑比较器官化

这一波也已经从“辅助层”提升成主顺序里的第四阶段。
原因：没有 `candidate_arena.py / go_nogo.py / world_contact_gate.py / consistency_logic.py` 这些器官，后续任何外周接触、责任判断和反事实比较仍然会被壳层捷径吃掉。

### Wave E 每轮固定读包

```text
docs/v0/README.md
  -> docs/v0/entry/v0_delivery_status_board.md
  -> docs/v0/entry/v0_module_execution_catalog.md
  -> docs/v0/slice_contracts/s03_direction_life_membrane_engineering_contract.md
  -> docs/v0/slice_contracts/s05_validation_membrane_observation_engineering_contract.md
  -> docs/v0/slice_contracts/s09_schema_runner_code_engineering_contract.md
  -> docs/v0/code_framework/queues/20_queue_e_membrane_validator_logic_implementation_contract.md
  -> docs/09_perception_prediction_world_contact_implementation_playbook.md
  -> docs/22_state_transition_and_threshold_model.md
  -> docs/72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md
  -> docs/75_external_irreversible_action_confirmation_policy.md
```

### Wave E 每轮固定验证

```text
python -m unittest tests.slices.test_life_membrane
python -m unittest tests.slices.test_validation_membrane
python -m unittest tests.slices.test_schema_runner
python -m unittest tests.process.test_digital_life_shell_command
```

## Wave B：DIGITAL_LIFE_PROCESS_SUPERVISOR 补厚

这一波仍然重要，但它现在是第五阶段，而不是第一阶段。
原因：等 Queue C/F/D/E 先把状态根、身份根、身体/梦境和行为/validator 器官化之后，process supervisor 才有资格真正消费这些对象，而不是继续当“最小能跑的持续壳”。

### Wave B 每轮固定读包

```text
docs/v0/README.md
  -> docs/v0/entry/v0_delivery_status_board.md
  -> docs/v0/entry/v0_module_execution_catalog.md
  -> docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md
  -> docs/v0/process_contracts/terminal_life_loop_engineering_contract.md
  -> docs/v0/code_framework/queues/16_queue_b_process_supervisor_implementation_contract.md
  -> docs/20_agent_runtime_bridge_contract.md
  -> docs/82_incident_report_and_recovery_protocol.md
  -> docs/89_language_runtime_framework_bridge_and_life_shell_policy.md
```

### Wave B 每轮固定验证

```text
python -m unittest tests.process.test_persistent_digital_life_process
python -m unittest tests.process.test_digital_entrypoint
python -m unittest tests.bridges.test_terminal_life_loop
```

## Wave A：语言主神经束深度补厚

这一波现在不是消失了，而是被推迟到 Queue B 之后。
原因：当前已经存在的 `percept.py / semantic_map.py / language_state.py / dream_gate.py / action_shadow.py / relation_scope.py` 已经足以支撑它继续作为生命主神经束存在；现在更缺的是支撑它的主体内部骨架和外部行为/验证边界。

### Wave A 现在主要解决什么

1. 继续把已存在语言器官接进更厚的长期关系与语言事件时间线。
2. 把语言连续体更深地接到 `body / process_supervisor / relationship timeline`。
3. 把终端生命回合和 process supervisor 对语言对象的消费继续接厚。

### Wave A 每轮固定读包

```text
docs/v0/README.md
  -> docs/v0/entry/v0_delivery_status_board.md
  -> docs/v0/entry/v0_module_execution_catalog.md
  -> docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md
  -> docs/v0/code_framework/queues/14_queue_a_language_percept_semantic_map_implementation_contract.md
  -> docs/09_language_symbolic_top_layer.md
  -> docs/86_language_neuroscience_pragmatics_and_inner_speech.md
  -> docs/96_real_relationship_longitudinal_timeline.md
```

### Wave A 每轮固定验证

```text
python -m unittest tests.slices.test_language_organs
python -m unittest tests.slices.test_language_relationship
python -m unittest tests.bridges.test_first_terminal_turn
```

## 当前推荐的一轮标准动作

如果下一轮就是继续往前落代码，最推荐的不是再开新包，也不是再回到链尾，而是：

1. 在 `Wave C` 里先落 `life_state.py`
2. 再落 `engram_index.py`
3. 跑 `tests.slices.test_state_store` 和 `tests.slices.test_neural_life_core`
4. 回写 `entry/v0_delivery_status_board.md` 与 `entry/v0_module_execution_catalog.md`
5. 再进入 `Wave F` 的 `direction_lock.py / continuity_refs.py`

这样做的原因是：

1. 先稳生命状态根和工作区根；
2. 再稳身份根和出生准备度；
3. 后面的身体/行为/持续存在都会有更稳的对象基础。

## 每一轮必须回答的五个问题

真正开写前，必须同时答出下面五个问题：

1. 这一轮属于哪一个 `Wave`？
2. 这一轮只拆哪一个真实文件？
3. 这一轮必须回读哪些 `00-257` 理论文档？
4. 这一轮会写哪些 state/report/receipt？
5. 这一轮跑哪组测试来证明生命链没断？

答不上来，就先别写代码。
