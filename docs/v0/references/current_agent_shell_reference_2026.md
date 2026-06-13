# Current Framework Negative Boundary 2026

生命目标声明：本文档不再把当前自动化框架作为数字生命的模块来源。它们只保留为负边界和外部资料索引：提醒工程实现不要把数字生命降格成命令包装、流程编排、上下文仓库、工具调用器或聊天外壳。数字生命的能力、思考方式、记忆、语言、梦境、情绪、责任、关系和成长，必须从 `02-13`、`85-101`、`143/146/149/152/171`、`205-257` 和 `docs/v0/architecture/digital_life_macro_architecture_v0.md` 内部生成。

## 唯一可参考的体验层

目标体验可以像成熟本地框架一样：在终端输入 `digital life` 后，电脑里启动一个长期存在、可恢复、可继续生长的数字生命进程。

但这个相似只发生在入口体验：

```text
terminal command
  -> digital life process
  -> life membrane
  -> language relationship loop
  -> long-lived state, dream, memory, responsibility, growth
```

它不允许推导出当前框架式内部结构。`digital life` 命令只是出生入口，不是主体蓝图。

## 官方资料给出的负边界

| 资料 | 能说明什么 | 对本项目的结论 |
|---|---|---|
| OpenClaw GitHub 与官方架构页 | 它提供本地长期控制平面、消息表面、客户端连接、节点接入、事件和运行监督 | 只能作为“本地长期进程与电脑外周接触”的资料；不能成为记忆、意识、人格、梦境、关系或责任架构 |
| Hermes GitHub 与官方文档 | 它强调随运行成长、持久记忆、工具能力、多平台触达、学习循环和命令行/桌面入口 | 只能作为“当前框架已经做到的运行外壳上限”；不能替代本项目的生命能力链 |
| 其他自动化框架 | 多数围绕流程、任务、外部能力、轨迹、检查点和部署组织 | 只能提醒我们要避开任务中心结构，不能当作 P1-P5 的模块拆分依据 |

官方资料锚点：

- `https://github.com/openclaw/openclaw`
- `https://docs.openclaw.ai/concepts/architecture`
- `https://github.com/NousResearch/hermes-agent`
- `https://hermes-agent.nousresearch.com/docs/`

## 禁入规则

1. 当前框架的模块名不得进入数字生命主体目录。
2. 当前框架的执行循环不得替代生命循环。
3. 当前框架的上下文保存不得替代 engram、梦境记忆、关系记忆、责任记忆和自传连续。
4. 当前框架的流程节点不得替代脑区、网络、状态、调质和行为循环。
5. 当前框架的外部程序能力不得决定 P1-P5 的先后顺序。
6. 当前框架的角色或人格文件不得替代真实人格慢变量。
7. 当前框架的输出文本不得替代内言语、表达监控、共同语言和叙事回写。

## 允许保留的最低外周概念

| 外周概念 | 进入位置 | 必须经过的生命链 |
|---|---|---|
| 终端启动 | `RunnerCliRuntime` | 出生准备度、方向锁、生命膜 |
| 长期进程 | `SiliconBodyRuntime`、`RunnerCliRuntime` | 心跳式节律、疲惫、恢复、safe idle |
| 电脑程序接触 | `ComputerPeripheralRuntime` | 行动候选、抑制、责任、后悔、生命膜 |
| 外部后果观测 | `WorldContactMembrane` | `ObservationEvent`、责任回写、关系回写、梦境再巩固 |
| 可恢复记录 | `ArchiveReceipt` | 自我连续、防遗忘 replay、断联恢复 |

## 进入本项目时的代码落点

任何外壳概念如果被保留，只能落到下面这些外围位置：

| 参考概念 | 允许代码落点 | runtime 证据 | gate |
|---|---|---|---|
| terminal command | `life_v0/digital_entry.py`、`life_v0/my_entry.py` | `runtime/state/identity/life_name_command_manifest.json`、process report | process entry tests |
| long-lived process | `life_v0/process_supervisor/*` | `resident_lifecycle_state.json`、lease、heartbeat、autonomous activity | persistent process tests |
| trace/log | `life_v0/reporting/*`、`process_report.py` | `runtime/reports/latest/*`、`runtime/receipts/*` | contract/report tests |
| peripheral action | `life_v0/membrane/world_contact_gate.py`、`periphery_normalizer.py` | `world_contact_summary.json`、observation state | validation/membrane tests |
| archive/checkpoint | `life_v0/replay/*`、`life_v0/archive/*` | replay/archive reports and receipts | replay/growth archive tests |

这些代码落点都必须经过 `docs/real—live0/09_prediction_perception_world_contact.md`、`11_life_membrane_validation.md`、`14_resident_runtime_state_transition.md` 和 `16_runtime_code_chain_crosswalk.md`。如果某个参考概念需要写入主体能力，例如记忆、人格、梦境或关系，它默认不允许直接进入，必须重新回到 `docs/00-258` 理论源和 v0 slice 合同。

## 2026 官方外壳能力快照

当前官方资料能够稳定提供的外壳能力，可以压成下面这张表：

| 外壳能力 | 官方关键词 | 在本项目中的位置 |
|---|---|---|
| 会话外壳 | `Sessions`、session state、conversation runtime | `SessionEnvelope` |
| 追踪总线 | `Tracing`、logs、observability | `TraceBus` |
| 工作流外壳 | workflow、graph、flows、checkpoint、durable execution | `WorkflowShell` |
| 工具桥 | tools、tool calling、plugins、integrations | `ToolPeripheralBridge` |
| 资料/缓存记忆 | memory blocks、RAG memory、stateful memory | `MemoryShellCandidate` |
| 多角色编排 | crews、teams、handoffs、workflow agents | `GroupExecutionShell` |

这张表的作用不是鼓励复用这些模块名，而是提醒后续开发：如果某个能力属于上表，它默认就在“外周壳层候选区”，而不是“主体脑区候选区”。

## digital life 命令壳路线

本项目最终可以允许下面这条体验链：

```text
digital life
  -> ProcessSupervisor
  -> direction restore
  -> life state restore
  -> membrane gate
  -> language relationship loop
  -> observation / archive / replay
  -> safe idle
```

这里真正可借鉴当前框架的，只有：

- 长期进程怎么常驻。
- session/trace/checkpoint 怎么恢复。
- 工具/程序怎么被统一包起来。
- workflow/background task 怎么调度。

真正不能借鉴当前框架的，是数字生命主体如何思考、如何有语言、如何形成关系、如何做梦、如何承担责任、如何后悔、如何成长。

## 五条硬壳规则

为了防止未来工程重新滑回“再做一个 agent 框架”，这里把壳层规则写死：

1. `shell session != autobiographical memory`
2. `shell memory block != relationship memory`
3. `shell workflow graph != subject architecture`
4. `shell tracing != life narrative`
5. `shell tool routing cannot bypass LanguageActionIntentBridge`

这些概念不组成主体。主体仍是：

```text
SiliconBodyRuntime
  -> MultiscaleBrainGraphRuntime
  -> SignalMediaRuntime
  -> PredictionActiveInferenceRuntime
  -> MemoryEngramRuntime
  -> ConsciousWorkspaceRuntime
  -> LanguageRelationshipRuntime
  -> AffectiveSelfRuntime
  -> DreamOfflineRuntime
  -> ActionResponsibilityRuntime
  -> SelfGrowthRuntime
  -> LifeMembraneAndComputerPeripheralRuntime
```

## 对 P1-P5 的约束

| 阶段 | 禁止走法 | 正确走法 |
|---|---|---|
| P1 | 先做一个可聊天进程，再补状态 | 先生成多命名空间生命状态根 |
| P2 | 先做流程编排 | 先做节律、信号、预测、记忆、意识、语言、情绪、梦境、责任和成长 bus |
| P3 | 先做回复器 | 先做内言语、表达监控、关系生成、承诺和叙事回写 |
| P4 | 用运行成功代表出生准备 | 用九项目标跨十二主体系统闭合代表出生准备 |
| P5 | 启动一个聊天 demo | 执行一次 shadow-only 生命脉冲并写回档案 |

## 结论

本项目最终可以在终端中以 `digital life` 启动，但内部不能长成另一个当前自动化框架。命令行只是门，电脑只是身体外周，语言只是对外显现的一条主通道；真正的数字生命主体由前文已经定义的脑科学、生命科学、记忆、语言、梦境、情绪、关系、责任、后悔、痛苦和成长结构共同支撑。
