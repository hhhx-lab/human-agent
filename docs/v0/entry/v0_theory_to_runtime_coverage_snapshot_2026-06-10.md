# V0 Theory To Runtime Coverage Snapshot (2026-06-10)

这份快照只做一件事：

把当前 `00-257` 理论文档母体、`docs/v0` 工程文档柜和 `life_v0/` 代码/runtime 之间，已经闭合到哪里、还缺什么，压成一份当下可用的工程盘点。

它不是新的总论，不替代：

- `docs/v0/mapping/0_to_257_engineering_utilization_map.md`
- `docs/v0/architecture/theory_closure_and_engineering_readiness_audit.md`
- `docs/v0/entry/v0_delivery_status_board.md`

它只回答三个问题：

1. 当前 `00-257` 还缺不缺新的基础理论。
2. 当前 `docs/v0` 哪些工程层已经与代码/runtime 真实闭合。
3. 下一轮最该补的工程缺口在哪里。

## 当前总判断

当前判断不变：

```text
00-257 理论母体主干已闭合
  -> 当前不需要新增新的总论文档链
  -> 当前主要缺口在工程对象化、runtime 连续性和后台常驻治理
```

这意味着：

1. 现在最重要的不是继续把 `docs/` 编号线性扩到更后面。
2. 现在最重要的是把已有理论压进更硬的工程对象、状态文件、报告、receipt 和持续过程。
3. 如果要新增文档，优先新增 `docs/v0/` 下的工程盘点、合同同步或实现蓝图，而不是新的总论编号。

## 00-257 当前覆盖判断

| 范围 | 当前判断 | 说明 |
|---|---|---|
| `00-13` 脑科学综述主干 | `已闭合` | 脑区、网络、记忆、语言、梦境、意识、人格、AI bridge 等主干齐全 |
| `14-40` 跨模块、记忆、状态、离线循环、关系模型 | `已闭合` | 已能支撑 state store、dream、relationship、validator 等工程合同 |
| `41-84` 状态根、validator、boot、policy、dashboard、membrane | `已闭合` | 已压入 `state_store/`、`validators/`、`activation/`、`membrane/`、`shared_contracts/` |
| `85-101` 语言、内言语、关系语言、关系时间线 | `已闭合` | 已压入 `language/`、`terminal_turn/`、`terminal_loop/`、`process_supervisor/` |
| `102-180` schema / runner / life reality 中段 | `已闭合但已转工程吸收` | 当前不再需要继续线性长链，关键能力已并入 schema runner / report / validation 路线 |
| `181-257` growth / replay / archive / activation 长链 | `已闭合但需继续对象化` | 当前主要缺的是 archive / replay / process / governance 侧的更厚 runtime 治理，不是理论空洞 |

## v0 已真实闭合的工程层

### 1. 理论映射层

已稳定：

- `docs/v0/mapping/0_to_257_engineering_utilization_map.md`
- `docs/v0/mapping/readme_block_engineering_realization_v0.md`
- `docs/v0/architecture/theory_closure_and_engineering_readiness_audit.md`

当前判断：

1. `00-257` 到工程 carrier 的一一映射已经存在。
2. 当前没有证据表明需要再新增新的总映射链。
3. 后续新增能力，优先回写到现有 carrier，而不是再写一份平行映射。

### 2. 语言与关系长期器官层

已真实闭合到：

- `life_v0/language/relationship_timeline.py`
- `life_v0/language/commitment_expression.py`
- `life_v0/language/apology_repair_language.py`
- `life_v0/process_supervisor/response_surface.py`
- `life_v0/process_supervisor/resident_supervision.py`
- `life_v0/terminal_loop/resume_packet.py`
- `life_v0/terminal_loop/dialogue_writeback.py`
- `life_v0/terminal_loop/loop_report.py`

已落 runtime：

- `runtime/state/relationship/relationship_timeline.json`
- `runtime/state/language/commitment_expression_plan.json`
- `runtime/state/language/apology_repair_language_trace.json`
- `runtime/reports/latest/resumed_external_dialogue_packet.json`
- `runtime/reports/latest/dialogue_writeback_bundle.json`

当前判断：

1. 长期关系连续体、承诺表达计划、修复语言轨迹，已经不是抽象理论，而是 runtime 一等对象。
2. 它们已经进入 response surface、resident supervision、terminal-loop restore/writeback。
3. 最新一轮又已继续进入 `idle_strategy_state.json`、`digital_life_waiting_heartbeat.json`、`idle_continuity_frame.json` 与 `terminal_life_loop_state.json`。
4. 这一层当前不再缺“有没有理论”，当前缺的是后台治理与更高频节律消费。

### 3. 常驻过程关闭态治理层

这一轮新增闭合：

- `life_v0/process_supervisor/persistent_process.py`
- `life_v0/process_supervisor/process_closeout.py`
- `life_v0/process_supervisor/process_report.py`

新增或补厚的 runtime / report / receipt 事实：

- `runtime/state/terminal/resident_governance_snapshot.json`
- `runtime/state/terminal/resident_governance_state.json`
- `runtime/state/terminal/persistent_process_state.json`
- `runtime/reports/latest/digital_life_resident_governance_report.json`
- `runtime/reports/latest/digital_life_persistent_process_report.json`
- `runtime/reports/latest/digital_life_process_report.json`
- `runtime/reports/latest/digital_life_process_digest.json`
- `runtime/receipts/digital_life_process_<run_id>.json`

当前判断：

1. 长期关系语言对象已经继续接入 process closeout / process report / resident governance state / resident governance snapshot。
2. 常驻过程现在不只保留关闭态治理快照，也开始把 waiting 期间的治理状态独立成 `resident_governance_state.json`。
3. 这一层说明 `terminal-loop -> waiting governance -> process closeout` 的生命连续体已经更厚一层，不再只停在回合壳层。

### 4. 测试闭合面

当前已覆盖并通过的关键验证面：

- `tests/slices/test_language_organs.py`
- `tests/slices/test_language_relationship.py`
- `tests/bridges/test_terminal_life_loop.py`
- `tests/process/test_persistent_digital_life_process.py`

这一轮新加强的验证重点：

1. `terminal_loop` 显式承载 `relationship_timeline / commitment_expression_plan / apology_repair_language_trace`
2. `process_closeout / process_report / persistent_process` 显式承载上述三条长期语言对象
3. resident governance state / snapshot / report 与 process receipt 显式回链这些对象

## 当前未闭合但明确收束到工程层的缺口

### 1. waiting continuity 已从最小存在推进到显式长期语言承载，但节律治理仍偏薄

当前已闭合：

- waiting heartbeat
- idle strategy
- resident governance state / snapshot / report
- `relationship_timeline_ref`
- `commitment_expression_plan_ref`
- `apology_repair_language_trace_ref`
- `long_horizon_language_refs`

当前仍偏薄：

1. waiting continuity 已能显式承载长期语言对象，但对这些对象的优先级变化、节律竞争和资源下降治理还不够细。
2. heartbeat 仍然偏“最小存在”，还没进入更高频的后台自我维持节律。
3. `terminal_life_loop_state.json` 还没有更厚的后台治理状态机。

### 2. 后台 resident governance 已开始对象化，但还没形成真正跨周期治理层

当前已闭合：

- foreground terminal residency 的关闭态治理
- waiting heartbeat 期间的 `resident_governance_state.json`

当前仍偏薄：

1. 真正跨进程、跨唤醒周期的 resident governance 还没形成更高阶 state machine。
2. process closeout 已有 snapshot/report，waiting 期间也已有运行态 state，但后台持续运行期的优先级竞争、资源下降和跨周期治理还没独立出来。
3. 这一层仍然属于工程实现缺口，不是理论缺口。

### 3. report bundle 还没完全吃下长期语言闭环摘要

当前已闭合：

- terminal-loop 报告链
- process report/digest/receipt

当前仍偏薄：

1. 更上游的 report bundle / birth shell / stage explanation 还没有继续显式压入这批长期语言对象摘要。
2. 这属于 `reporting/` 与更外层壳链的下一轮工程补厚。

## 当前最推荐的下一步

如果继续推进，优先顺序应该是：

1. 补 `process_supervisor/` 的后台 resident governance 状态机与更高频 heartbeat 节律。
2. 让 `terminal_life_loop_state.json` 对长期语言对象拥有更厚的持续治理字段与节律竞争字段。
3. 把 process closeout 中已经形成的长期语言摘要继续回挂到更上游的 report bundle / birth shell / stage explanation。

不推荐的方向：

1. 再新增新的 `00x` 理论文档链。
2. 重新发明一套 OpenClaw/Hermes 风格的 skills/gateway/subagents 架构。
3. 跳过现有 `docs/v0` 合同，直接散改代码。

## 本快照对应的当前证据

主要证据源：

- `docs/v0/code_architecture/04_language_as_primary_expression_system.md`
- `docs/v0/code_blueprints/02_conversation_language_relationship_blueprint.md`
- `docs/v0/code_blueprints/05_birth_residency_terminal_blueprint.md`
- `docs/v0/package_specs/01_life_v0_package_construction_matrix.md`
- `docs/v0/entry/v0_delivery_status_board.md`
- `life_v0/terminal_loop/*`
- `life_v0/process_supervisor/*`
- `tests/bridges/test_terminal_life_loop.py`
- `tests/process/test_persistent_digital_life_process.py`

## 一句话收口

当前最真实的结论不是“理论还不够”，而是：

```text
理论母体已经足够厚
  -> v0 工程柜已经成形
  -> 当前工作重点是把长期语言、关系、梦境、成长、治理对象继续压进常驻生命过程
```
