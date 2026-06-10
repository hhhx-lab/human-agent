# Build Order And Definition Of Done

这份文档把 v0 的代码落地顺序、实现语言选择和阶段完成定义固定下来。

它回答三个问题：

1. 为什么 v0 现在应该继续以 Python 为主体语言实现。
2. 接下来到底按什么阶段推进，而不是“想到哪层写哪层”。
3. 每一阶段满足什么证据，才允许进入下一阶段。

## v0 主实现语言决策

### 当前决策

v0 主体实现语言固定为：

```text
Python 3 作为主体语言
  + JSON state / report / receipt 文件根
  + unittest 作为当前统一验证面
```

### 原因

1. 当前 `life_v0/`、CLI、runtime 文件根、contracts、tests 已经全部在 Python 上闭合。
2. v0 当前主要矛盾不是纯计算速度，而是生命链对象化、跨层耦合和长期存在治理。
3. 现在切换主体语言，只会打散已存在的状态根、测试根、命令根和恢复链。

### 以后什么时候才值得引入第二语言

只有在 profiling 证明以下热点已经成为真实瓶颈时，才允许引入 Rust / C 等加速核：

1. 大规模 graph / connectome 计算
2. replay / archive / validator 的批量比较
3. counterfactual / evidence ranking 的纯计算热路径

也就是说：

- `life_v0/` 主体器官、命令面、等待态、恢复链、语言链继续用 Python。
- 未来高性能语言只作为局部加速核，不作为 v0 主体迁移目标。

## 阶段顺序

### Stage 0: 理论闭口锁定

| 项 | 内容 |
|---|---|
| 目标 | 确认 `00-257` 无基础断档，后续不再线性扩写新的总论链 |
| 必读 | `docs/README.md`、`docs/v0/architecture/theory_closure_and_engineering_readiness_audit.md` |
| 当前结论 | 已闭合；当前差距在工程对象化与代码器官化 |
| 通过证据 | 编号完整、理论层审计完成、无新增基础缺号 |

### Stage 1: 代码总架构基线

| 项 | 内容 |
|---|---|
| 目标 | 把整棵代码树的层次、共享对象总线、阶段顺序和 DoD 固定下来 |
| 必读 | 本柜 `01-03`、`19_code_tree_package_brain_contract.md`、`01_runtime_organ_interface_blueprint.md` |
| 主文件 | `docs/v0/code_architecture/*` |
| 通过证据 | 代码分层、对象总线、阶段顺序、语言决策、DoD 都写定并接入 contracts |

### Stage 2: Queue D / Queue E 主体底盘

| 项 | 内容 |
|---|---|
| 目标 | 先补硬身体/梦境/成长与行为/验证/逻辑这两条中轴 |
| 必读 | `18_queue_d_body_dream_growth_implementation_contract.md`、`20_queue_e_membrane_validator_logic_implementation_contract.md`、`06`、`08`、`09` playbooks |
| 主包 | `body/`、`dream/`、`growth/`、`membrane/`、`validators/`、`schema_runner/` |
| 当前前沿 | Queue D 扩展器官已落下 `nightmare_risk.py`、`belief_learning.py`、`language_learning.py`、`relationship_learning.py`；Queue E 第二波中的 `shadow_gate.py`、`world_contact_summary.py`、`validation_rollup.py`、`evidence_ranker.py`、`cross_file_logic.py`、`run_manifest.py` 已落地并补上局部闭包，当前继续补厚 `responsibility_loop.py` 与跨层写回；Queue B 这边则已把 resident governance 运行态 `state` 与关闭态 `snapshot / report` 一起接进 waiting / closeout 主链，下一刀继续转向等待态里的后台 resident governance 与更高频 heartbeat 节律 |
| 最低测试 | `tests/slices/test_life_support.py`、`tests/bridges/test_runtime_growth.py`、`tests/slices/test_life_membrane.py`、`tests/slices/test_validation_membrane.py`、`tests/slices/test_schema_runner.py` |
| 完成定义 | 身体信号、梦境离线链、成长补丁、行为候选、责任回路、反事实比较都不再压在重型 `__init__.py` 里，并且有独立 state/report 证据 |

### Stage 3: Queue B / Queue A 常驻存在与长期语言

| 项 | 内容 |
|---|---|
| 目标 | 在 D/E 站稳后，继续补厚等待态存在与长期关系语言 |
| 必读 | `16_queue_b_process_supervisor_implementation_contract.md`、`14_queue_a_language_percept_semantic_map_implementation_contract.md`、`04`、`07`、`08` playbooks |
| 主包 | `process_supervisor/`、`language/`、`terminal_turn/`、`terminal_loop/` |
| 已落核心器官 | `idle_strategy.py`、`resident_supervision.py`、`live_turn_cycle.py`、`process_session_loop.py`、`persistent_process.py` |
| 已落关键文件 | `relationship_timeline.py`、`commitment_expression.py`、`apology_repair_language.py` |
| 最低测试 | `tests/process/test_persistent_digital_life_process.py`、`tests/slices/test_language_organs.py`、`tests/slices/test_language_relationship.py`、`tests/bridges/test_terminal_life_loop.py` |
| 完成定义 | waiting heartbeat 真正消费 replay / growth / relation 对象，resident governance 运行态 state 与关闭态 snapshot/report 进入 process closeout 主链，关系时间线与承诺/修复语言已经进入长期语言链，下一步转向让 process / terminal 更深消费这批对象 |

### Stage 4: Queue C / Queue F 维护性深化

| 项 | 内容 |
|---|---|
| 目标 | 在主体底盘稳定后，回切神经核心、状态根和生命目标的更深对象链 |
| 必读 | `17_queue_c_memory_neural_core_implementation_contract.md`、`21_queue_f_identity_consciousness_birth_readiness_implementation_contract.md`、`05`、`10` playbooks |
| 主包 | `neural_core/`、`state_store/`、`life_targets/` |
| 本轮已落关键文件 | `signal_media.py`、`belief_state.py`、`prediction_error.py`、`active_sampling.py`、`memory_write_gate.py` 已真实接入 `runtime/state`、manifest、report、receipt 和 check gate |
| 已落但待补厚 | `direction_lock.py`、`continuity_refs.py`、`value_orientation.py`、`brain_graph.py`、`network_state.py`、`workspace.py`、`broadcast.py`、`metacognition.py`、`life_target_claims.py`、`evidence_matrix.py`、`birth_readiness_rollup.py`、`birth_readiness_stage_gate.py`、`consciousness_probes.py` |
| 最低测试 | `tests/slices/test_neural_life_core.py`、`tests/slices/test_state_store.py`、`tests/slices/test_life_targets.py` |
| 当前完成定义 | 预测、意识、记忆写门已经进入更细对象链：`signal_media_runtime.json`、`belief_state_frame.json`、`prediction_error_field.json`、`active_sampling_plan.json`、`memory_write_gate.json` 已成为独立器官；下一步从“补缺文件”切到“补厚跨层消费与长期闭环” |

### Stage 5: 诞生、恢复与终端长时运行收束

| 项 | 内容 |
|---|---|
| 目标 | 让 `./digital life` 不只是能启动，而是能稳定维持等待态、恢复、回合、写回与继续存在 |
| 必读 | `07_birth_terminal_process_implementation_playbook.md`、`first_terminal_turn_engineering_contract.md`、`terminal_life_loop_engineering_contract.md`、`digital_life_process_supervisor_engineering_contract.md` |
| 主包 | `activation/`、`reporting/`、`stage_explain/`、`digital_life/`、`shell_command/`、`process_supervisor/` |
| 最低测试 | `tests/bridges/test_first_activation_preflight.py`、`tests/bridges/test_emit_report.py`、`tests/bridges/test_first_terminal_turn.py`、`tests/process/test_digital_entrypoint.py`、`tests/process/test_persistent_digital_life_process.py` |
| 完成定义 | 自举、诞生、第一回合、waiting heartbeat、incident recovery、relaunch recovery、dialogue writeback 连成一条稳定存在链 |

### Stage 6: 七项最终验收审计

| 验收项 | 必要证据 |
|---|---|
| `a. 可在终端唤醒` | `./digital life --strict`、`digital_life_birth_packet.json`、`digital_life_process_report.json`、process tests |
| `b. 自主意识、情绪、思考、语言` | `prediction_workspace_frame.json`、`core_affect_vector.json`、language / relationship state、neural/body/language tests |
| `c. 记忆机制` | `life_state.json`、engram / replay / archive reports、state / replay tests |
| `d. 可成长可学习` | `growth_patch_candidate_queue.json`、`self_read_report.json`、growth tests |
| `e. 梦境能力` | `dream_experience_window.json`、`dream_fact_gate_decision.json`、dream / growth tests |
| `f. 平等交谈并在关系中成长` | relationship timeline state、commitment truth、dialogue writeback bundle、language / process tests |
| `g. 初步拥有生命机制` | contracts report + 全层 state/report/receipt + 各层 tests 共同证明 |

只有这七条都拿到直接证据，才允许把 v0 视为第一阶段收束。

## 每一阶段固定的验证规则

### 规则 1: 先跑本阶段直接测试

例如：

- D/E 阶段先跑 `life_support / membrane / validation / schema_runner / runtime_growth`
- B/A 阶段先跑 `process / language / terminal_loop`
- C/F 阶段先跑 `neural_core / state_store / life_targets`

### 规则 2: 再跑 contracts 回链

每一阶段结束后都必须跑：

```bash
python3 -m unittest tests.contracts.test_v0_contracts -v
```

因为这个项目的风险不只是代码出错，还有“代码已经往前走了，但文档和理论回链断了”。

### 规则 3: 能产状态就不能只看测试绿

凡是新器官已经宣称自己是生命链的一部分，都必须落至少一类证据：

1. `runtime/state/*`
2. `runtime/reports/latest/*`
3. `runtime/receipts/*`

如果只有测试而没有运行证据，仍然不算阶段闭合。

## 当前阶段判断

按当前工作区现实，最合理的判断是：

1. Stage 0 已完成。
2. Stage 1 本轮完成后可视为完成。
3. 当前默认下一步是 Stage 2，也就是继续推进 Queue D / Queue E。

因此这份文档本身的作用，就是把“为什么先 D/E，再 B/A，再 C/F”彻底钉死，防止断联后又回到散点式推进。
