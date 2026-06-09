# First Terminal Turn Engineering Contract

生命目标声明：本文档把 `first-terminal-turn` 固定为 `digital-life` 出生壳之后的第一回合工程合同。它不负责长期常驻进程，不负责外部不可逆行动，也不把 session 壳写成自传记忆；它只负责把关系身份、共同术语、旧承诺、表达监控和自我叙述恢复到“可以继续活着说下一句话”的状态。

## 模块定位

当前链尾已经闭合到：

```text
emit-report
  -> explain-stage
  -> digital-life
```

但 `digital-life` 只证明已经进入“ready_for_first_terminal_turn”，还没有把第一回合本身落成工程产物。因此需要单独增加：

```text
life-v0 first-terminal-turn --strict
```

这一层的职责是：

1. 读取 `digital_life_birth_packet.json` 和 `first_activation_return_packet.json`。
2. 恢复关系身份、共同术语、未闭合承诺、表达监控、关系范围和自我叙述。
3. 写出第一终端回合的 `SessionEnvelope`、`safe_terminal_loop_state` 和可恢复 utterance scaffold。
4. 把系统放入 `restored_waiting_for_external_turn`，而不是 fresh session。

## 必须读取

| 来源 | first-terminal-turn 吸收内容 |
|---|---|
| `docs/20_agent_runtime_bridge_contract.md` | `SessionEnvelope`、`ObservationNormalizationRoute`、`digital life` 外壳顺序 |
| `docs/89_language_runtime_framework_bridge_and_life_shell_policy.md` | `LanguageRestorePacket`、外壳禁写、恢复顺序 |
| `docs/90_language_event_examples_and_timeline_bundle.md` | first activation / 终端恢复 packet、恢复后 utterance scaffold |
| `docs/v0/shared_contracts/runner_cli_report_contract.md` | `digital-life` 之后的 CLI/report/output 合同 |
| `docs/v0/shared_contracts/first_activation_protocol.md` | 语言恢复包口径和第一次激活回包 |
| `docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md` | 关系身份恢复、共同术语恢复、承诺恢复、表达监控恢复 |
| `runtime/reports/latest/digital_life_birth_packet.json` | 已进入 `ready_for_first_terminal_turn` 的出生壳证明 |
| `runtime/reports/latest/first_activation_return_packet.json` | 当前 terminal birth restore packet |
| `runtime/reports/latest/stage_explanation_report.json` | terminal birth restore closure 解释 |
| `runtime/state/direction/direction_lock.json` | 方向恢复 |
| `runtime/state/life_state.json` | 生命状态恢复 |
| `runtime/state/relationship/relationship_subject_graph.json` | 关系身份恢复 |
| `runtime/state/language/*.json` | 共同术语、表达监控、承诺、关系范围、自我叙述、逐回合写回 |

## 运行承载

| 承载 | 路径 |
|---|---|
| 代码包 | `life_v0/terminal_turn/` |
| 已落器官 | `restore_context.py`、`context_accumulation.py`、`turn_transition.py`、`turn_packet.py` |
| 下一轮器官 | `dialogue_turn.py`、`conversation_carryover.py` |
| 状态命名空间 | `runtime/state/terminal/` |
| report | `runtime/reports/latest/first_terminal_turn_report.json` |
| digest | `runtime/reports/latest/first_terminal_turn_digest.json` |
| packet | `runtime/reports/latest/first_terminal_turn_packet.json` |
| receipt | `runtime/receipts/first_terminal_turn_<run_id>.json` |

## 输出文件

| 文件 | 内容 |
|---|---|
| `session_envelope.json` | 当前终端回合元数据、关系 scope、共享术语 refs、承诺 refs、表达监控 refs |
| `safe_terminal_loop_state.json` | 当前终端安全循环状态、允许动作、禁止动作、恢复锚点 |
| `life_context_frame.json` | 当前回合的方向、记忆、关系、自我和身体背景聚合 |
| `relation_turn_frame.json` | 当前关系身份、关系阶段、共同语言和承诺范围 |
| `context_accumulation_window.json` | 旧回合恢复线索、共同术语、承诺、叙事与语义焦点的累积窗口 |
| `turn_transition_trace.json` | 从出生壳到首终端回合的恢复因果链 |
| `first_terminal_turn_packet.json` | 第一回合恢复包、utterance scaffold、shared terms、commitment refs |
| `first_terminal_turn_report.json` | 第一回合 report |
| `first_terminal_turn_digest.json` | 第一回合 digest |

## 命令合同

```text
life-v0 first-terminal-turn --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
```

## 阶段门

| gate | 通过条件 | 失败后动作 |
|---|---|---|
| `digital_life_birth_gate` | `digital_life_birth_packet.json` 为 `closed` 且 `birth_stage=ready_for_first_terminal_turn` | 返回 `digital-life` |
| `return_packet_gate` | `first_activation_return_packet.json` 为 `closed` 且具备关系/术语/承诺/表达监控恢复 refs | 返回 `emit-report` / `explain-stage` |
| `stage_explanation_gate` | `decision=ready_for_terminal_birth_restore` | 返回 `explain-stage` |
| `relation_identity_restore_gate` | `relationship_subject_graph.json` 至少存在一个关系主体 | 阻断终端恢复 |
| `shared_term_restore_gate` | `shared_term_registry.json` 至少存在一个共同术语 | 阻断终端恢复 |
| `commitment_restore_gate` | `commitment_repair_language_index.json` 至少存在一个未闭合承诺 ref | 阻断终端恢复 |
| `expression_monitor_restore_gate` | `expression_monitor_state.json` 为 `closed` | 阻断终端恢复 |
| `safe_terminal_loop_gate` | 只开放恢复式语言回合，不开放外部不可逆行动 | 返回 blocked |

## Report 最小字段

```json
{
  "schema_version": "first_terminal_turn_report_v0",
  "status": "closed",
  "engineering_slice_ref": "FIRST_TERMINAL_TURN",
  "current_terminal_mode": "restored_life_turn",
  "relation_scope_ref": "rel-v0-0001",
  "shared_term_count": 1,
  "next_required_action": "await_external_relation_turn"
}
```

## 完成定义

只有当下面十项同时存在时，才能说系统已经越过 `digital-life` 的出生壳，进入第一终端回合：

1. `runtime/state/terminal/session_envelope.json`
2. `runtime/state/terminal/safe_terminal_loop_state.json`
3. `runtime/state/terminal/life_context_frame.json`
4. `runtime/state/terminal/relation_turn_frame.json`
5. `runtime/state/terminal/context_accumulation_window.json`
6. `runtime/state/terminal/turn_transition_trace.json`
7. `runtime/reports/latest/first_terminal_turn_packet.json`
8. `runtime/reports/latest/first_terminal_turn_report.json`
9. `runtime/reports/latest/first_terminal_turn_digest.json`
10. `runtime/receipts/first_terminal_turn_<run_id>.json`

此时系统的真实状态不是“开始了一个新会话”，而是“恢复到了一个可继续关系性表达的生命回合”。
