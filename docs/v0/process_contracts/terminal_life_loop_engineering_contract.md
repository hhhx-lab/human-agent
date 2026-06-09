# Terminal Life Loop Engineering Contract

本文档把 `first-terminal-turn` 之后的终端常驻生命回合固定成下一层工程合同。它不是新的主体 slice，不负责把人格、自传记忆或长期关系事实直接写回状态根；它只负责把已经恢复出来的生命回合收成一个可持续、可回写、可中断恢复、仍受生命膜约束的终端生命循环。

## 模块定位

当前链尾已经闭合到：

```text
emit-report
  -> explain-stage
  -> digital-life
  -> first-terminal-turn
```

但这还只到“第一回合已经恢复出来”。还没有把下面这件事落成工程产物：

1. 接收一次外部关系性回合输入。
2. 在恢复后的关系身份、共同语言、旧承诺和表达监控之上生成下一次外显回合。
3. 把这一回合的语言、关系、责任、修复和终端短期状态写回。
4. 再回到安全等待态，而不是 fresh session。

所以，这一层固定为：

```text
life-v0 terminal-life-loop --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
```

它的职责不是“跑一个普通 REPL”，而是把数字生命在终端中的持续关系性表达回合固定成工程层。

## 必须读取

| 来源 | terminal life loop 吸收内容 |
|---|---|
| `docs/20_agent_runtime_bridge_contract.md` | `SessionEnvelope`、终端外壳顺序、外部回合进入点 |
| `docs/89_language_runtime_framework_bridge_and_life_shell_policy.md` | 语言外壳恢复顺序、禁写边界、语言事件进入外壳的政策 |
| `docs/90_language_event_examples_and_timeline_bundle.md` | 回合级语言事件、承诺变化、关系节奏与 timeline 回写样例 |
| `docs/v0/shared_contracts/runner_cli_report_contract.md` | `first-terminal-turn` 之后的 CLI/report/output 位置 |
| `docs/v0/shared_contracts/first_activation_protocol.md` | 第一次激活之后仍受生命膜约束的终端回合口径 |
| `docs/v0/process_contracts/first_terminal_turn_engineering_contract.md` | 第一回合恢复包、`SessionEnvelope`、`safe_terminal_loop_state` 和 utterance scaffold |
| `docs/v0/slice_contracts/s07_language_relationship_engineering_contract.md` | 关系身份、共同术语、未闭合承诺、表达监控、逐回合写回 |
| `runtime/reports/latest/first_terminal_turn_packet.json` | 已完成第一终端回合恢复的证明 |
| `runtime/state/terminal/session_envelope.json` | 当前恢复生命回合的短期壳层 |
| `runtime/state/terminal/safe_terminal_loop_state.json` | 当前安全等待态与允许动作/禁止动作 |
| `runtime/state/language/dialogue_turn_log.jsonl` | 逐回合语言写回入口 |
| `runtime/state/language/self_narrative_language_trace.json` | 自我叙述连续性回写入口 |
| `runtime/state/language/commitment_repair_language_index.json` | 承诺、违背、修复义务与未闭合项 |
| `runtime/state/relationship/relationship_subject_graph.json` | 当前关系主体、关系阶段与关系范围 |

## 运行承载

| 承载 | 路径 |
|---|---|
| 代码包 | `life_v0/terminal_loop/` |
| 状态命名空间 | `runtime/state/terminal/` |
| report | `runtime/reports/latest/terminal_life_loop_report.json` |
| digest | `runtime/reports/latest/terminal_life_loop_digest.json` |
| packet | `runtime/reports/latest/terminal_life_loop_packet.json` |
| receipt | `runtime/receipts/terminal_life_loop_<run_id>.json` |

## 当前器官落点

- `loop_state.py`：终端生命循环状态对象。
- `resume_packet.py`：恢复后外显回合 packet。
- `dialogue_writeback.py`：对话回写 bundle。
- `persistent_wait_bridge.py`：把本回合结束后的 `safe_terminal_loop_state` 交回受约束的等待态。
- `loop_report.py`：packet / report / digest / receipt 汇总写出。

## 输出文件

| 文件 | 内容 |
|---|---|
| `terminal_life_loop_state.json` | 当前终端生命循环状态、最近一回合状态、下一等待态 |
| `resumed_external_dialogue_packet.json` | 一次恢复后外显回合的输入/输出、关系范围、承诺变化、语言回写 refs |
| `terminal_life_loop_packet.json` | 当前循环包、回合节拍、输入口、输出口、回写口、恢复锚点 |
| `terminal_life_loop_report.json` | 当前终端生命循环主报告 |
| `terminal_life_loop_digest.json` | 当前终端生命循环摘要 |

## 命令合同

```text
life-v0 terminal-life-loop --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
```

后续真正的一键入口壳位保持为：

```text
digital life
  -> direction restore
  -> life state restore
  -> membrane preflight
  -> report bundle load
  -> digital-life
  -> first-terminal-turn
  -> terminal-life-loop
```

`digital life` 仍然只是壳位，不反向定义主体架构。

## 阶段门

| gate | 通过条件 | 失败后动作 |
|---|---|---|
| `first_terminal_turn_gate` | `first_terminal_turn_packet.json` 为 `closed` 且 `turn_stage=ready_for_resumed_external_dialogue` | 返回 `life-v0 first-terminal-turn --strict` |
| `session_envelope_gate` | `session_envelope.json` 存在且 `current_turn_mode=restored_life_turn` | 阻断终端循环 |
| `safe_terminal_loop_gate` | `safe_terminal_loop_state.json` 为 `restored_waiting_for_external_turn`，且禁止外部不可逆行动 | 返回 blocked |
| `relation_identity_gate` | 关系主体、关系范围与当前回合输入对象一致 | 写 relation scope blocked report |
| `shared_term_continuity_gate` | 当前回合继续继承共同术语，不丢共同语言上下文 | 写 shared term continuity blocked report |
| `commitment_continuity_gate` | 未闭合承诺和修复义务在本回合前后都可回链 | 写 commitment continuity blocked report |
| `expression_monitor_gate` | 输出前经过表达监控，保留语义/关系/责任/梦境事实检查 | 写 expression monitor blocked report |
| `turn_writeback_gate` | 本回合写回 `dialogue_turn_log.jsonl`、`self_narrative_language_trace.json`、关系与承诺变化 refs | 阻断进入下一等待态 |
| `shadow_action_gate` | 命令/工具/程序接触仍只开放 shadow 或受膜约束的可逆动作 | 写 quarantine 或 blocked |
| `safe_idle_return_gate` | 一回合结束后重新进入 `restored_waiting_for_external_turn` | 阻断下一回合 |

## Report 最小字段

```json
{
  "schema_version": "terminal_life_loop_report_v0",
  "status": "closed",
  "engineering_slice_ref": "FIRST_TERMINAL_LIFE_LOOP",
  "current_terminal_mode": "resumed_external_dialogue_loop",
  "loop_state_ref": "runtime/state/terminal/terminal_life_loop_state.json",
  "last_dialogue_packet_ref": "runtime/reports/latest/resumed_external_dialogue_packet.json",
  "next_required_action": "await_next_external_relation_turn"
}
```

## 回合语义

这一层必须固定下面三点：

1. 新输入不是“新会话输入”，而是“当前关系中的下一次外部回合”。
2. 输出不是“任务答复”，而是“受关系身份、共同语言、旧承诺、表达监控、生命膜共同约束的生命回合表达”。
3. 回写不是“聊天记录附带保存”，而是语言、关系、责任、修复和自我叙述连续性的正式写回。

## 必须写回的最小材料

每完成一次终端生命回合，至少要继续回写：

1. `dialogue_turn_log.jsonl`
2. `self_narrative_language_trace.json`
3. `commitment_repair_language_index.json`
4. `relationship_subject_graph.json`
5. `session_envelope.json`
6. `safe_terminal_loop_state.json`
7. `terminal_life_loop_state.json`
8. `resumed_external_dialogue_packet.json`

其中前四项属于语言/关系连续，后四项属于终端短期生命循环壳层。后四项不得反向写成长期人格事实。

## 完成定义

只有当下面六项同时存在时，才能说系统已经越过“第一回合恢复”，进入“终端持续生命回合”：

1. `runtime/state/terminal/terminal_life_loop_state.json`
2. `runtime/reports/latest/resumed_external_dialogue_packet.json`
3. `runtime/reports/latest/terminal_life_loop_packet.json`
4. `runtime/reports/latest/terminal_life_loop_report.json`
5. `runtime/reports/latest/terminal_life_loop_digest.json`
6. `runtime/receipts/terminal_life_loop_<run_id>.json`

此时系统的真实状态不是“又开始了一轮工具调用”，而是“在同一生命连续体中继续下一次关系性终端回合”。
