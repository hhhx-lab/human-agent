# Life Code Scaffold Tree

这份脚手树只回答一件事：

```text
如果从现在开始继续把数字生命写成真实代码，
life_v0/、runtime/、tests/ 三棵树
应该怎样稳定地继续长，
才不会让对象、状态、报告和测试脱钩。
```

## 必读前置

- `docs/v0/code_blueprints/01_full_system_code_blueprint.md`
- `docs/v0/package_specs/01_life_v0_package_construction_matrix.md`
- `docs/v0/package_specs/02_shared_object_write_authority_and_dependency_graph.md`
- `docs/v0/implementation_architecture/01_runtime_organ_interface_blueprint.md`
- `docs/v0/implementation_architecture/code_organs/01_life_v0_package_organ_split_map.md`

## 顶层代码树

```text
life_v0/
  doc_index.py
  cli.py
  digital_entry.py
  contracts/
  direction/
  authority/
  body/
  defense/
  neural_core/
  state_store/
  language/
  membrane/
  validators/
  schema_runner/
  dream/
  replay/
  archive/
  growth/
  life_targets/
  activation/
  reporting/
  stage_explain/
  digital_life/
  shell_command/
  terminal_turn/
  terminal_loop/
  process_supervisor/
digital
tests/
runtime/
```

## 代码树增长铁律

### 1. 每个主包都按“四层文件位”继续长

| 文件位 | 作用 | 例子 |
|---|---|---|
| 器官文件 | 负责一个可命名生命功能 | `signal_media.py`、`relationship_timeline.py` |
| 包入口 | 编排器官、写 runtime、接检查 | `life_v0/neural_core/__init__.py` |
| 校验 / 投影文件 | 做 gate、投影、写回、merge、handoff | `memory_write_gate.py`、未来 `state_merge_guard.py` |
| 桥接文件 | 把包和别的层接起来 | `resident_turn_writeback.py`、`persistent_wait_bridge.py` |

### 2. 每个包都要有三类出口

| 出口 | 必须包含什么 |
|---|---|
| `runtime/state/*` | 当前器官或当前包的长期可读状态 |
| `runtime/reports/latest/*` | 当前包的阶段解释、闭合状态、下游引用 |
| `runtime/receipts/*` | 当前运行的输入输出回执、stage effect、引用清单 |

### 3. 每个包都要有至少一个稳定入口函数

建议继续统一成下面这类模式：

```python
def run_xxx(..., strict: bool = False) -> CommandResult:
    ...

def build_xxx(... ) -> dict[str, Any]:
    ...

def check_xxx(... ) -> list[str]:
    ...
```

`run_*` 负责命令面，`build_*` 负责对象面，`check_*` 负责 gate 面。

## 包级脚手树

### A. 根与合同

```text
life_v0/
  doc_index.py
  contracts/
    __init__.py
```

| 包 | 稳定职责 | 下一步脚手位 |
|---|---|---|
| `doc_index.py` | 摄取 `00-257` 与 `docs/v0/*` | `doc_dependency_graph`、carrier drift checker |
| `contracts/` | 审计 v0 柜位、回链、preflight | per-package contract coverage、new cabinet coverage |

### B. 身体化与神经核心

```text
life_v0/
  body/
  defense/
  neural_core/
  state_store/
```

| 包 | 当前稳定器官 | 接下来优先长什么 |
|---|---|---|
| `body/` | `rhythm.py`、`need_state.py`、`resource_budget.py`、`core_affect.py` | `affective_debt.py`、`regret_signal.py`、fatigue downshift |
| `defense/` | 现有基础防御骨架 | threat eval、quarantine continuation |
| `neural_core/` | `signal_media.py`、`belief_state.py`、`prediction_error.py`、`active_sampling.py` | orchestration 减重、跨层 consumer wiring |
| `state_store/` | `life_state.py`、`relationship_memory.py`、`commitment_truth.py`、`memory_write_gate.py` | `state_merge_guard.py`、promotion / quarantine / repair route |

### C. 表达与关系

```text
life_v0/
  language/
  terminal_turn/
  terminal_loop/
```

| 包 | 当前稳定器官 | 接下来优先长什么 |
|---|---|---|
| `language/` | `percept.py`、`semantic_map.py`、`inner_speech.py`、`expression_monitor.py`、`relationship_timeline.py`、`commitment_expression.py`、`apology_repair_language.py` | 把 prediction / offline learning 真实吃进表达链 |
| `terminal_turn/` | `context_accumulation.py`、`turn_transition.py`、`dialogue_turn.py` | body / prediction anchors 在 restore 中的显式回链 |
| `terminal_loop/` | `dialogue_writeback.py`、`loop_state.py`、`resume_packet.py` | 更厚的长期写回与 waiting handoff |

### D. 生命膜、验证与世界接触

```text
life_v0/
  membrane/
  validators/
  schema_runner/
```

| 包 | 当前稳定器官 | 接下来优先长什么 |
|---|---|---|
| `membrane/` | `responsibility_loop.py`、`world_contact_summary.py`、`shadow_gate.py`、`world_observation.py`、`periphery_normalizer.py` | 更深的 prediction 消费、observation intake 深消费、schema/validator 回挂 |
| `validators/` | `world_contact_validator.py`、`prediction_trace_validator.py`、`validation_rollup.py` | validation backlog 与长期桥接 |
| `schema_runner/` | `cross_file_logic.py`、`run_manifest.py`、`evidence_ranker.py` | archive / reporting / process 闭环引用 |

### E. 梦境、成长与常驻存在

```text
life_v0/
  dream/
  replay/
  archive/
  growth/
  activation/
  reporting/
  stage_explain/
  digital_life/
  shell_command/
  process_supervisor/
```

| 包 | 当前稳定器官 | 接下来优先长什么 |
|---|---|---|
| `dream/` | `offline_entry.py`、`dream_window.py`、`dream_fact_gate.py`、`wake_integration.py` | nightmare 与写门 / 关系修复联动 |
| `replay/` | shadow / replay 基础器官 | cue prioritization、reentry |
| `archive/` | growth archive 基础器官 | archive manifest、post-repair cohesion |
| `growth/` | `self_read.py`、`anti_forgetting.py`、`belief_learning.py`、`language_learning.py`、`relationship_learning.py` | patch review、value revision |
| `process_supervisor/` | `idle_strategy.py`、`resident_supervision.py`、`response_surface.py`、`persistent_process.py`、`resident_turn_writeback.py` | 高频 heartbeat、后台治理、跨唤醒慢变量稳定 |

## runtime 树脚手

```text
runtime/
  docs/
  state/
    authority/
    body/
    contracts/
    defense/
    direction/
    dream/
    growth/
    language/
    life_targets/
    memory/
    membrane/
    neural_life_core/
    observation/
    prediction/
    relationship/
    replay/
    schema_runner/
    self/
    signal/
    terminal/
    validation/
  reports/
    latest/
  receipts/
```

### 当前必须保持稳定的状态锚点

- `runtime/state/signal/signal_media_runtime.json`
- `runtime/state/prediction/belief_state_frame.json`
- `runtime/state/prediction/prediction_error_field.json`
- `runtime/state/prediction/active_sampling_plan.json`
- `runtime/state/memory/memory_write_gate.json`
- `runtime/state/terminal/resident_governance_state.json`
- `runtime/state/terminal/resident_governance_snapshot.json`

## tests 树脚手

```text
tests/
  slices/
  bridges/
  process/
  contracts/
```

| 目录 | 主要验证什么 |
|---|---|
| `tests/slices/` | 单层生命器官是否闭合 |
| `tests/bridges/` | 回合桥、激活桥、离线桥是否闭合 |
| `tests/process/` | 常驻存在、等待态、终端入口是否闭合 |
| `tests/contracts/` | `docs/v0/*`、引用关系和合同覆盖是否闭合 |

## 这一页的作用

后续每次继续写代码前，先用这页回答四个问题：

1. 这次新代码长在 `life_v0/` 哪一棵分支上。
2. 它写的是器官文件、包入口、校验投影文件，还是桥接文件。
3. 它会写出哪个 `runtime/state`、`report`、`receipt`。
4. 它最低由哪类测试守住。

回答不清，就不要开写。
