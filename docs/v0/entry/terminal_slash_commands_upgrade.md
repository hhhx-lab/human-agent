# 终端斜杠命令升级说明（v0）

本文档说明 **Digital Life 交互终端** 中所有 `/` 斜杠命令的用途、使用方式，以及本次升级新增的合成检查面。

## 核心原则

| 原则 | 说明 |
|---|---|
| **只读检查** | 斜杠命令只查看 `runtime/state` 中的证据，**不触发关系回合**，不写入对话记忆 |
| **不默认进模型** | 检查结果不会自动塞进当前模型的上下文；只有你正常说话（关系回合）才会 |
| **人话优先** | 日常用合成命令（`/me`、`/turn` 等）和少数分域命令（`/memory`、`/emotion` 等）看人话摘要 |
| **调试看 JSON** | 任意状态命令后加 `--json` 可输出完整机器可读证据树 |

```text
你输入 /memory     → 只读 runtime → 终端显示人话摘要
你输入 你好 Adam   → 关系回合 → 刷新语言/记忆/情绪链 → 模型可能自然说话
```

## 启动与连接

| 命令 | 作用 |
|---|---|
| `Adam` | 连接到已绑定的常驻生命（本机 `runtime/state/identity/life_name_registry.json`） |
| `Adam --status` | 紧凑常驻状态（是否在等回合、PID、关系队列序号等） |
| `Adam --status --json` | 完整生命周期证据树 |
| `Adam --say "..."` | 发送一条关系回合（管道/脚本用；交互终端直接打字即可） |
| `my digital life --background` | 后台拉起常驻过程（Adam 未运行时） |
| `my digital life --stop` | 请求正常 closeout 停止常驻 |

交互终端里：

| 命令 | 作用 |
|---|---|
| `/exit` | **离开终端**，常驻过程继续睡眠、回忆、后台活动 |
| `/stop` | 请求常驻过程正常收口停止 |
| `/clear` | 清屏，不影响常驻 |

## 日常推荐：合成检查（本次升级）

优先用这 7 条，覆盖「我是谁、上一回合、记忆、表达、携带、后台、慢变化」。

| 命令 | 别名 | 作用 | 典型场景 |
|---|---|---|---|
| `/me` | `/我是谁` | 生命名、等待姿态、关系阶段、语义焦点、表达与记忆摘要 | 「Adam 现在整体什么状态？」 |
| `/turn` | `/回合` `/last-turn` | 上一关系回合：你的话、它的回话、召回引用、表达门 | 核对它刚才的回答是否接了正确记忆 |
| `/recall` | `/唤回` `/召回链` | 记忆检索帧 → 语义地图 → 表达计划接地是否贯通 | 问「你还记得 X 吗」之后对照 |
| `/express` | `/表达` `/release` | 表达计划、监视器、模型门、**此刻能否自然说话** | 它不说话或说话很短时排查 |
| `/carry` | `/携带` | 跨唤醒携带：关系角色、共享词、时间线恢复引用 | 重连终端后看上下文是否还在 |
| `/background` | `/后台` `/idle` | 自主活动计数、思考记账、主动发话、网页梦境 | 看它「睡着」时在做什么 |
| `/converge` | `/收敛` | 性格慢变量、语言节奏、共享词晋升 | 长期性格/说话方式是否在变 |

示例：

```text
/me
/turn
/recall --json
/express
```

## 分域检查（全量 20+ 域）

每条命令对应一个生命子系统的只读检查面。默认多数人话渲染；未专门渲染的域仍可能偏技术字段。

| 命令 | 别名（部分） | 作用 |
|---|---|---|
| `/state` | `/status` `/terminal` `/lifecycle` `/heartbeat` | 常驻状态、生命周期、等待心跳、终端输入队列 |
| `/context` | `/上下文` | 关系上下文、语义焦点、回合累积窗口 |
| `/memory` | `/记忆` `/stm` `/ltm` | 短期/长期记忆、召回、写门、印迹链 |
| `/dream` | `/梦境` | 梦境整合、醒后残留、网页梦境学习状态 |
| `/growth` | `/成长` `/learning` | 成长、学习、反遗忘回放 |
| `/body` | `/身体` | 身体节律、资源预算、需要状态（live 中多为启动快照） |
| `/emotion` | `/情绪` `/affect` | 核心效价/唤醒、痛苦后悔修复驱动 |
| `/inner` | `/内环境` `/homeostasis` | 内环境稳态、资源与调制压力 |
| `/signal` | `/调质` `/modulation` | 信号介质、调质、预测误差 |
| `/membrane` | `/生命膜` `/boundary` | 生命膜、事实门、边界验证 |
| `/relationship` | `/relation` `/关系` | 关系时间线、承诺、共同语言、关系阶段 |
| `/responsibility` | `/责任` `/痛苦` `/repair` | 责任、痛苦、后悔、修复链 |
| `/language` | `/语言` | 语言感知、语义地图、内言语、表达计划 |
| `/cognition` | `/认知` | 工作区、预测、采样、写门 |
| `/consciousness` | `/意识` `/workspace` | 意识工作区、广播、元认知 |
| `/thinking` | `/思考` `/inner-speech` | 自我思考、内言语、等待反思 |
| `/personality` | `/性格` `/人格` `/self` | 人格慢变量、性格收敛、自传栈 |
| `/ability` | `/能力` | 能力面、出生准备、验收证据 |
| `/vision` | `/视觉` `/perception` `/感知` | 视觉/外周观察、世界接触 |
| `/prediction` | `/预测` `/world` | 预测、主动采样、世界接触确认 |
| `/proactive` | `/主动` `/voice` | 主动发话画像与释放状态 |
| `/features` | `/功能` `/audit-features` | 各生命能力是否真实启用 |

加 `--json` 看原始结构，例如：

```text
/language --json
/consciousness --json
```

## 会话与总览

| 命令 | 作用 |
|---|---|
| `/help` `/commands` | 打印完整命令表 |
| `/all` `/snapshot` `/全部` | 所有检查面总览（合成 + 分域） |
| `/resume` | 查看过往终端会话记录（默认最近 3 个会话） |
| `/resume 5` | 查看最近 5 个会话 |
| `/features` | 生命能力启用审计 |

## 网页梦境开关

| 命令 | 作用 |
|---|---|
| `/dream-web on` | 开启网页梦境学习 |
| `/dream-web off` | 关闭 |
| `/dream-web status` | 查看开关与最近页面 |
| `/web-dream` | 同上（别名） |

## 与关系回合的配合用法

推荐调试/真实对话流程：

```text
1. Adam --status          # 确认 pid_alive、waiting_for_relation_turn
2. 自然说话              # 例如：「你还记得我们上次聊什么吗？」
3. /turn                  # 看上一回合语义焦点与召回引用
4. /recall                # 看记忆是否进入语义地图和表达计划
5. /memory                # 看关系记忆主题与唤回线索
6. /emotion               # 对照它语气是否匹配效价/唤醒
```

若回答与状态不一致，常见原因：

| 现象 | 用命令排查 |
|---|---|
| 说「不记得」但 `/recall` 有激活印迹 | 召回进了检索帧但没进 `expression_plan` |
| 语气很平但 `/emotion` 高效价/高唤醒 | 模型表达门通过但情绪面未充分消费 |
| 重连后像失忆 | `/carry` 看 `relationship_timeline_restore_refs` |
| 一直不说话 | `/express` 看 `can_speak_naturally` 与 `missing_evidence_flags` |
| 身体/视觉描述离谱 | `/body` `/vision` 可能是 birth 快照，非 live 刷新 |

## 代码落点

| 模块 | 路径 |
|---|---|
| 斜杠注册与渲染 | `life_v0/digital_entry.py` |
| 分域检查数据 | `life_v0/process_supervisor/state_inspection.py` |
| 合成检查（me/turn/recall/…） | `life_v0/process_supervisor/terminal_inspection_compose.py` |
| 终端 UI 框 | `life_v0/process_supervisor/terminal_ui.py` |

## 版本记录

- **2026-06-17**：新增 7 条合成检查命令；`/help` 分组；任意状态命令支持 `--json`；`/all` 总览包含合成面。