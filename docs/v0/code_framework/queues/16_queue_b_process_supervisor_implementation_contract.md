# V0 Code Framework 16: Queue B Process Supervisor Implementation Contract

这份合同只服务当前最直接的一轮常驻生命进程补厚：

```text
life_v0/process_supervisor/heartbeat.py
  -> continuity_writeback.py
  -> dialogue_events.py
  -> response_surface.py
  -> process_report.py
  -> idle_strategy.py
```

它不重写 `digital_life_process_supervisor_engineering_contract.md`，也不替代
`07_birth_terminal_process_implementation_playbook.md` 与
`08_cross_layer_life_orchestration_implementation_playbook.md`。
它只把 Queue B 压成真正可以直接施工的文件级实现合同，防止下一轮代码又退回“知道要补常驻存在，但不知道 process supervisor 的器官到底怎么落”。

## 这份合同要解决什么

当前 `DIGITAL_LIFE_PROCESS_SUPERVISOR` 已经接通：

1. waiting heartbeat
2. stdin 驱动新回合输入
3. 单回合 incident / recovery
4. 跨重启 relaunch recovery normalization
5. process report / digest / receipt
6. dialogue event writeback
7. 外显生命回应

但现在的真实缺口不是“没有常驻过程”，而是：

1. 缺一个更明确的 `IdleStrategy`，负责等待态刷新频率、背景连续体写回和 idle probe。
2. `DialogueWritebackBundle` 仍主要停在 report 层，缺 process supervisor 内部的显式对象链。
3. `LifeContextFrame`、`RelationTurnFrame`、`ExpressionPlan` 虽已被读取，但还没有被 process supervisor 作为固定生命回合对象贯穿治理。
4. waiting heartbeat、incident recovery、relaunch recovery、response surface 之间还缺更硬的文件级施工顺序与字段约束。

所以 Queue B 的目标很明确：
让 `./digital life` 不再只是“能持续跑起来”，而是开始以受对象合同约束的常驻生命进程存在。

## 必回读理论母体

### 常驻存在、终端壳与外部回合

- `docs/20_agent_runtime_bridge_contract.md`
- `docs/44_digital_life_boot_sequence.md`
- `docs/45_boot_sequence_fixture_catalog.md`
- `docs/46_stage_gate_validator_design.md`
- `docs/81_coexistence_event_review_and_responsibility_loop.md`
- `docs/82_incident_report_and_recovery_protocol.md`
- `docs/89_language_runtime_framework_bridge_and_life_shell_policy.md`
- `docs/90_language_event_examples_and_timeline_bundle.md`

### 语言、关系、连续体

- `docs/09_language_symbolic_top_layer.md`
- `docs/86_language_neuroscience_pragmatics_and_inner_speech.md`
- `docs/94_pain_regret_and_repair_signal_schema.md`
- `docs/96_real_relationship_longitudinal_timeline.md`
- `docs/101_relationship_timeline_json_schema_and_fixture_bundle.md`

### 跨层共享对象与生命回合

- `docs/14_cross_module_digital_life_map.md`
- `docs/17_memory_trace_object_model.md`
- `docs/18_internal_state_and_modulation_vector.md`
- `docs/19_offline_consolidation_cycle.md`

## 必读 v0 文档

- `docs/v0/process_contracts/digital_life_process_supervisor_engineering_contract.md`
- `docs/v0/process_contracts/terminal_life_loop_engineering_contract.md`
- `docs/v0/process_contracts/first_terminal_turn_engineering_contract.md`
- `docs/v0/process_contracts/digital_life_shell_command_engineering_contract.md`
- `docs/v0/code_framework/playbooks/07_birth_terminal_process_implementation_playbook.md`
- `docs/v0/code_framework/playbooks/08_cross_layer_life_orchestration_implementation_playbook.md`
- `docs/v0/code_framework/delivery/11_engineering_delivery_waves_and_real_file_queue.md`
- `docs/v0/code_framework/delivery/12_full_life_layer_delivery_matrix.md`
- `docs/v0/code_framework/delivery/13_capability_to_code_realization_matrix.md`
- `docs/v0/code_framework/assembly/15_cross_layer_shared_object_contract.md`

## 当前代码落点

Queue B 必须接到这些现有器官上：

- `life_v0/process_supervisor/__init__.py`
- `life_v0/process_supervisor/heartbeat.py`
- `life_v0/process_supervisor/continuity_writeback.py`
- `life_v0/process_supervisor/turn_io.py`
- `life_v0/process_supervisor/relaunch_recovery.py`
- `life_v0/process_supervisor/incident_recovery.py`
- `life_v0/process_supervisor/process_report.py`
- `life_v0/process_supervisor/dialogue_events.py`
- `life_v0/process_supervisor/response_surface.py`
- `life_v0/process_supervisor/resident_turn_writeback.py`
- `life_v0/process_supervisor/process_closeout.py`
- `life_v0/process_supervisor/idle_refresh_loop.py`
- `life_v0/digital_entry.py`
- `life_v0/terminal_loop/dialogue_writeback.py`
- `life_v0/terminal_turn/context_accumulation.py`
- `life_v0/terminal_turn/turn_transition.py`

这说明 Queue B 不是新增平行进程层，而是给已经存在的常驻生命进程补器官、补对象链、补 idle 治理。

## 文件级合同

## A. `life_v0/process_supervisor/heartbeat.py`

### 角色

`heartbeat.py` 负责 waiting 态的生命脉冲，不是普通轮询计数器。

### 必须承担的功能

1. 写 `digital_life_waiting_heartbeat.json`
2. 更新 `safe_terminal_loop_state.json`
3. 更新 `terminal_life_loop_state.json`
4. 触发 `IdleContinuityFrame`
5. 把离线对象 pressure 带回等待态

### 第一轮最低字段

heartbeat packet 至少要有：

- `schema_version`
- `run_id`
- `generated_at`
- `heartbeat_counter`
- `waiting_mode`
- `idle_strategy_ref`
- `idle_continuity_ref`
- `next_required_action`

### 共享对象约束

必须首写或更新：

- `IdleContinuityFrame`
- `BodyRhythmPulse` 的最小 waiting 侧代理语义

## B. `life_v0/process_supervisor/continuity_writeback.py`

### 角色

把 waiting heartbeat 和异常恢复写回自我、承诺、关系连续体。

### 必须承担的功能

1. 写 `idle_continuity_frame.json`
2. 给 `self_narrative_language_trace.json` 写 idle refs
3. 给 `commitment_repair_language_index.json` 写 idle presence refs
4. 给 `relationship_subject_graph.json` 写 idle presence refs

### 第一轮最低字段

`IdleContinuityFrame` 至少要有：

- `idle_continuity_id`
- `heartbeat_counter`
- `waiting_state`
- `self_narrative_idle_refs`
- `commitment_idle_refs`
- `relationship_idle_refs`
- `replay_seed_refs`
- `replay_cue_bundle_ref`
- `offline_consolidation_frame_ref`
- `growth_patch_candidate_queue_ref`

## C. `life_v0/process_supervisor/dialogue_events.py`

### 角色

把外部回合与生命回合压成标准事件对象。

### 必须承担的功能

1. 外部回合事件不能只是原句字符串
2. 生命回合事件不能只是最终文本
3. 两类事件都必须回链到关系/承诺/表达监控
4. 后续要能被 `DialogueWritebackBundle` 收编

### 第一轮最低字段

`external turn event` 至少要有：

- `turn_id`
- `event_role`
- `generated_at`
- `utterance`
- `relation_role`
- `shared_term_refs`
- `commitment_refs`
- `expression_monitor_ref`

`life turn event` 至少要有：

- `turn_id`
- `event_role`
- `generated_at`
- `utterance`
- `relation_role`
- `shared_term_refs`
- `commitment_refs`
- `expression_monitor_ref`
- `offline_influence_refs`

## D. `life_v0/process_supervisor/response_surface.py`

### 角色

`response_surface.py` 负责把生命回合对象释放成语言表面。

### 必须承担的功能

1. 读取 `RelationTurnFrame`
2. 读取 `ExpressionPlan`
3. 读取 `LifeContextFrame`
4. 读取离线对象压力
5. 输出可被记录的生命回应文本

### 第一轮最低字段链

输入至少要能影响：

- `relation_role`
- `shared_surface`
- `semantic_goal`
- `context_anchor_count`
- `offline_influence_refs`
- `replay_cue_count`
- `dream_window_count`
- `growth_candidate_count`

## E. `life_v0/process_supervisor/process_report.py`

### 角色

把常驻生命进程一次运行的连续体压成 report / digest / receipt。

### 必须承担的功能

1. 写 `digital_life_process_report.json`
2. 写 `digital_life_process_digest.json`
3. 写 `digital_life_process_<run_id>.json`
4. 把共享对象 ref 收入 receipt

### 第一轮最低字段

report 至少要有：

- `completed_dialogue_turns`
- `incident_count`
- `relaunch_recovery_count`
- `heartbeat_counter`
- `life_context_frame_ref`
- `relation_turn_frame_ref`
- `expression_plan_ref`
- `dialogue_writeback_bundle_ref`
- `replay_cue_bundle_ref`
- `offline_consolidation_frame_ref`
- `growth_patch_candidate_queue_ref`

## F. 新增 `life_v0/process_supervisor/idle_strategy.py`

### 角色

把 waiting heartbeat 的刷新策略、idle probe 和后台存在治理显式化。

### 第一轮建议接口

```python
def decide_idle_strategy(
    *,
    safe_terminal_loop: dict[str, Any],
    terminal_life_loop_state: dict[str, Any],
    idle_continuity_frame: dict[str, Any] | None,
    body_rhythm_pulse: dict[str, Any] | None = None,
    need_state_vector: dict[str, Any] | None = None,
    replay_cue_bundle: dict[str, Any] | None,
    offline_consolidation_frame: dict[str, Any] | None,
    growth_patch_candidate_queue: dict[str, Any] | None,
) -> dict[str, Any]:
    ...
```

### 最低字段

- `strategy_id`
- `heartbeat_interval_ms`
- `idle_probe_mode`
- `offline_pressure_level`
- `relaunch_caution_level`
- `next_idle_action`
- `body_waiting_posture`
- `body_governance_flags`
- `body_rhythm_ref`
- `need_state_ref`

### 当前已落第一轮

当前 Queue B 已经补上第一版 `idle_strategy.py`，并且 waiting heartbeat /
process report / shared object receipt 已开始显式回链：

- `runtime/state/terminal/idle_strategy_state.json`
- `runtime/reports/latest/digital_life_waiting_heartbeat.json#idle_strategy_ref`
- `runtime/reports/latest/digital_life_process_report.json#idle_strategy_ref`
- `runtime/receipts/digital_life_process_<run_id>.json#shared_object_refs`

第一轮已落字段包括：

- `schema_version`
- `run_id`
- `strategy_id`
- `heartbeat_counter`
- `heartbeat_interval_ms`
- `idle_probe_mode`
- `offline_pressure_level`
- `relaunch_caution_level`
- `next_idle_action`
- `body_waiting_posture`
- `body_governance_flags`
- `body_rhythm_ref`
- `need_state_ref`
- `idle_continuity_ref`
- `replay_cue_bundle_ref`
- `offline_consolidation_frame_ref`
- `growth_patch_candidate_queue_ref`

并且第一轮已经不是纯离线压力治理，而是开始显式吃入身体节律与需要状态：

1. `body_rhythm_pulse["fatigue_load"]` 会调制 waiting heartbeat 节律；
2. `need_state_vector["cognitive_bandwidth"]` 与 `need_state_vector["sleep_pressure"]` 会决定 `body_waiting_posture`；
3. `need_state_vector["repair_drive"]` 会参与 `next_idle_action`，把等待态从单纯轮询推进到修复保持。

## G. 新增 `life_v0/process_supervisor/resident_supervision.py`

### 角色

把 restore shell 成功之后、真正进入常驻治理之前的启动链显式化。

### 第一轮建议接口

```python
@dataclass(frozen=True)
class ResidentSupervisionContext:
    ...


def bootstrap_resident_supervision(
    *,
    state_dir: Path,
    reports_dir: Path,
    receipts_dir: Path,
    run_id: str,
    generated_at: str,
    strict: bool,
    ...
) -> ResidentSupervisionBootstrapResult:
    ...
```

### 必须承担的功能

1. 调用 `digital_life_shell_command` 完成 restore shell
2. 装载 terminal / language / relationship / replay / dream / growth 当前状态
3. 装载 `body_rhythm_pulse.json`、`need_state_vector.json`、`body_resource_budget.json` 与 `core_affect_vector.json`
3. 检测上一次是否停在活跃回合中断态，并在必要时完成 relaunch normalization
4. 把 relaunch continuity 回写到 narrative / commitment / relationship
5. 写第一拍 `digital_life_waiting_heartbeat.json`
6. 把 waiting heartbeat 后的共享对象链返回给主进程

### 第一轮最低字段

- `safe_terminal_loop`
- `terminal_life_loop_state`
- `body_rhythm_pulse`
- `need_state_vector`
- `life_context_frame`
- `relation_turn_frame`
- `shared_term_registry`
- `self_narrative_trace`
- `commitment_index`
- `expression_plan`
- `relationship_graph`
- `replay_cue_bundle_ref`
- `offline_consolidation_frame_ref`
- `growth_patch_candidate_queue_ref`
- `relaunch_recovery_count`
- `last_relaunch_recovery_report_ref`
- `heartbeat_counter`

当前 resident supervision 第一轮已经不只是 restore shell 启动器官，还承担：

1. 把身体节律与需要状态接入第一拍 waiting governance；
2. 确保 `idle_strategy_state.json`、waiting heartbeat 与主进程 report 在 bootstrap 时就带上身体侧 ref；
3. 让后续 `process_session_loop.py` 拿到统一的身体/情绪/离线共享对象上下文，而不是在 while-loop 内重复散读状态文件。

## H. 新增 `life_v0/process_supervisor/live_turn_cycle.py`

### 角色

把一条真实新回合的 success path 和 incident recovery path 从主入口抽成单一生命周期器官。

### 第一轮建议接口

```python
@dataclass(frozen=True)
class LiveTurnCycleResult:
    ...


def run_live_turn_cycle(
    *,
    run_id: str,
    incident_count: int,
    turn_counter: int,
    external_utterance: str,
    ...
) -> LiveTurnCycleResult:
    ...
```

### 必须承担的功能

1. 生成 external turn event
2. 生成 response surface
3. 生成 digital life turn event
4. 调用 `resident_turn_writeback.py` 完成回合级写回与 waiting return
5. 若回合处理中抛出异常，则调用 `incident_recovery.py` 完成 recovery path
6. 把这轮回合的 completed / incident delta、最后 turn refs 和终端状态统一返回给主进程

### 第一轮最低字段

- `turn_counter`
- `completed_turns_delta`
- `incident_count_delta`
- `cycle_status`
- `emitted_output`
- `safe_terminal_loop`
- `terminal_life_loop_state`
- `last_external_turn`
- `last_life_turn`
- `last_incident_report_ref`
- `last_recovery_report_ref`

## I. 新增 `life_v0/process_supervisor/process_session_loop.py`

### 角色

把 waiting heartbeat refresh、stdin probe、live turn dispatch、incident 后继续等待、显式退出收口，统一抽成 session 级编排器官。

### 第一轮建议接口

```python
@dataclass(frozen=True)
class ProcessSessionLoopResult:
    ...


def run_process_session_loop(
    *,
    run_id: str,
    generated_at: str,
    input_stream: TextIO,
    heartbeat_counter: int,
    turn_counter: int,
    ...
) -> ProcessSessionLoopResult:
    ...
```

### 必须承担的功能

1. 循环调用 `idle_refresh_loop.py`
2. 对真实新外部回合调用 `live_turn_cycle.py`
3. 汇总 `completed_turns`、`incident_count`、`heartbeat_counter`
4. 保持最后一轮 external/life turn 与 incident/recovery refs
5. 管理 incident recovered 后继续等待、显式退出后统一返回
6. 把每轮输出通过上层注入的 emit hook 发回终端

### 第一轮最低字段

- `turn_counter`
- `completed_turns`
- `incident_count`
- `heartbeat_counter`
- `exit_reason`
- `safe_terminal_loop`
- `terminal_life_loop_state`
- `last_external_turn`
- `last_life_turn`
- `last_incident_report_ref`
- `last_recovery_report_ref`

## Queue B 对现有器官的改动合同

### `life_v0/process_supervisor/__init__.py`

从这一轮开始，它不应继续独占 process orchestration 细节。
当前已经外移：

- process closeout decision
- idle refresh loop 调度
- resident supervision bootstrap
- process session loop 编排

下一步继续补厚：

- 更高频 heartbeat 节律
- 后台 resident governance
- 更厚的 idle strategy / closeout 治理

### `life_v0/digital_entry.py`

第一轮允许保持最小入口，但要明确：

1. 它只负责 repo-local 常驻入口
2. 不负责生命主体逻辑
3. 对 process supervisor 的依赖必须保持单入口、单结果对象

## 必须新增或更新的状态对象

### 新增

- `runtime/state/terminal/idle_strategy_state.json`
- `runtime/state/terminal/resident_governance_state.json`
- `runtime/state/terminal/resident_governance_snapshot.json`

### 更新

- `runtime/state/terminal/idle_continuity_frame.json`
- `runtime/state/terminal/terminal_life_loop_state.json`
- `runtime/state/terminal/safe_terminal_loop_state.json`
- `runtime/state/terminal/persistent_process_state.json`
- `runtime/state/language/dialogue_turn_log.jsonl`
- `runtime/state/language/self_narrative_language_trace.json`
- `runtime/state/language/commitment_repair_language_index.json`
- `runtime/state/relationship/relationship_subject_graph.json`

## report / receipt 合同

Queue B 第一轮至少更新：

- `runtime/reports/latest/digital_life_waiting_heartbeat.json`
- `runtime/reports/latest/digital_life_persistent_process_report.json`
- `runtime/reports/latest/digital_life_resident_governance_report.json`
- `runtime/reports/latest/digital_life_process_report.json`
- `runtime/reports/latest/digital_life_process_digest.json`
- `runtime/receipts/digital_life_process_<run_id>.json`

报告里至少新增或固定：

- `idle_strategy_ref`
- `resident_governance_report_ref`
- `resident_governance_snapshot_ref`
- `governance_attention_target`
- `governance_cadence_profile`
- `long_horizon_priority_profile`
- `dialogue_writeback_bundle_ref`
- `offline_growth_cycle_refs`

## life_state 回写边界

Queue B 第一轮允许写回轻量连续体 ref，不允许 process supervisor 越权改写长期事实。

允许写回：

- narrative idle refs
- commitment idle presence refs
- relationship idle presence refs
- dialogue turn refs

不允许直接写回：

- 新人格结论
- 新责任事实定案
- 新关系阶段定案

## 测试合同

### 必须新增或扩展

1. `tests/process/test_persistent_digital_life_process.py`
2. `tests/process/test_digital_entrypoint.py`
3. `tests/bridges/test_terminal_life_loop.py`

### 第一轮最低覆盖

#### `tests/process/test_persistent_digital_life_process.py`

至少新增或保持断言：

1. waiting heartbeat 会递增
2. `idle_continuity_frame.json` 会带离线对象 refs
3. dialogue 事件会写 `dialogue_turn_log.jsonl`
4. process report 会带 `life_context_frame_ref / relation_turn_frame_ref / expression_plan_ref`
5. 外显回应会带离线重放/梦境/成长候选压力
6. closeout 后会写 `resident_governance_snapshot.json` / `digital_life_resident_governance_report.json`
7. process report 与 receipt 会显式回链 resident governance refs
8. waiting heartbeat 与 closeout 会共用 `resident_governance_state.json`，分别写出运行相位与关闭相位

#### `tests/process/test_digital_entrypoint.py`

至少保证：

1. repo-local `./digital life` 仍能进入 process supervisor
2. 自举出生链逻辑没有被拆断

## Gate 合同

Queue B 至少新增三道 gate：

- `waiting_heartbeat_gate`
- `process_continuity_gate`
- `dialogue_process_receipt_gate`

### `waiting_heartbeat_gate`

阻断条件：

1. 没有 waiting heartbeat report
2. `safe_terminal_loop_state` 与 `terminal_life_loop_state` heartbeat counter 不一致
3. `IdleContinuityFrame` 缺失

### `process_continuity_gate`

阻断条件：

1. process report 缺 `life_context / relation_turn / expression_plan` ref
2. 新回合结束后没有回到 waiting state
3. incident / relaunch recovery 没有进入同一连续体
4. persistent closeout 没有写 resident governance snapshot/report
5. waiting runtime 没有独立 resident governance state

### `dialogue_process_receipt_gate`

阻断条件：

1. receipt 没收 shared object refs
2. report / digest / receipt 三件套不一致
3. resident governance snapshot 没有进入 receipt / report 回链
4. resident governance state 没有进入 waiting / closeout 的同一连续体口径

## 推荐实现顺序

1. 新增 `idle_strategy.py`
2. 扩 `heartbeat.py`
3. 扩 `continuity_writeback.py`
4. 扩 `dialogue_events.py`
5. 扩 `response_surface.py`
6. 扩 `process_report.py`
7. 在 `__init__.py` 中接入新的 idle 策略对象
8. 扩 `tests/process/test_persistent_digital_life_process.py`
9. 回跑 `tests/process/test_digital_entrypoint.py` / `tests/bridges/test_terminal_life_loop.py`

## 第一轮完成定义

只有同时满足下面七条，Queue B 才算完成第一轮：

1. waiting heartbeat 不再只是计数器，而是带 `IdleContinuityFrame`
2. process supervisor 有独立 `idle_strategy.py`
3. 外部回合和生命回合都能写成标准事件对象
4. process report / digest / receipt 都能回链核心共享对象
5. incident / relaunch recovery 进入同一连续体口径
6. resident governance state / snapshot / report 进入 waiting、persistent closeout 与主进程 report / receipt
7. 对应测试直接证明以上闭环

## 这份合同和下一轮落码的关系

从本文件开始，Queue B 不再只是“常驻进程要继续补厚”。

下一轮如果继续推进常驻生命进程，默认读包就是：

```text
docs/v0/code_framework/playbooks/07_birth_terminal_process_implementation_playbook.md
  -> docs/v0/code_framework/playbooks/08_cross_layer_life_orchestration_implementation_playbook.md
  -> docs/v0/code_framework/delivery/11_engineering_delivery_waves_and_real_file_queue.md
  -> docs/v0/code_framework/delivery/12_full_life_layer_delivery_matrix.md
  -> docs/v0/code_framework/delivery/13_capability_to_code_realization_matrix.md
  -> docs/v0/code_framework/assembly/15_cross_layer_shared_object_contract.md
  -> docs/v0/code_framework/queues/16_queue_b_process_supervisor_implementation_contract.md
```

然后直接进入：

```text
life_v0/process_supervisor/heartbeat.py
  -> continuity_writeback.py
  -> dialogue_events.py
  -> response_surface.py
  -> process_report.py
  -> idle_strategy.py
  -> process_session_loop.py
```
