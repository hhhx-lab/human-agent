# 产品级终端 TUI 使用说明（product_split_pane_v2）

本文档说明 **Adam 交互终端** 的产品级三区布局：每个区域显示什么、怎么操作、读哪些 runtime 证据。斜杠命令的完整列表见 [terminal_slash_commands_upgrade.md](./terminal_slash_commands_upgrade.md)。

## 运行前准备

### 依赖

`prompt-toolkit` 已写入 `pyproject.toml`（`>=3.0.52`）。在本仓库根目录执行：

```bash
uv sync
uv run python -c "import prompt_toolkit; print(prompt_toolkit.__version__)"
```

应输出类似 `3.0.52`。交互终端请始终用 **`uv run`** 启动，避免系统 Python 找不到依赖：

```bash
uv run Adam          # 或项目约定的 digital / my 入口
```

若未装 `prompt_toolkit`，TTY 下 `Adam` 会报错并提示先 `uv sync`。

### 布局版本

当前体验标识：`layout_profile = product_split_pane_v2`

## Codex/Grok 对标计划表

| 阶段 | 能力 | 状态 | 快捷键 / 入口 |
|------|------|------|----------------|
| P0 | Application 真分栏（顶栏 / 对话 / 侧栏 / 输入） | ✅ 已完成 | `uv run Adam` |
| P1 | 异步回合 + typing 指示器 | ✅ 已完成 | 提交后后台执行，底栏显示「回合进行中…」 |
| P2 | 流式 token（SSE 实时 + 非流式模拟打字） | ✅ 已完成 | 模型 SSE 经 `terminal_stream_bridge` 推送 |
| P3 | 富 markdown（标题 / 列表 / 链接 / 代码块） | ✅ 已完成 | 消息正文自动渲染 |
| P4 | 多 session tab | ✅ 已完成 | `Ctrl-T` 新建 · `Ctrl-Tab` / `Shift-Tab` 切换 · `Ctrl-1..9` 跳转 |
| P5 | 主题 + resize 自适应 | ✅ 已完成 | `Ctrl-Y` 轮换主题 · `DIGITAL_LIFE_TUI_THEME` · 终端缩放自动刷新 |
实现文件：

| 模块 | 路径 |
|------|------|
| 布局渲染 | `life_v0/process_supervisor/terminal_layout.py` |
| 分栏 Application 壳 | `life_v0/process_supervisor/prompt_toolkit_split_terminal_app.py` |
| 入口兼容层 | `life_v0/process_supervisor/prompt_toolkit_terminal_app.py` |
| 纯文本渲染辅助 | `life_v0/process_supervisor/terminal_ui.py` |
| 输入/补全合同 | `life_v0/process_supervisor/terminal_input.py` |
| 会话 transcript | `life_v0/process_supervisor/terminal_session_transcript.py` |

---

## 整体布局

```text
┌─ Adam  background_active  ITR A·B·C·D·E·F·V ─────────────┐  ← 顶栏（固定行）
├──────────────────────────────────────┬───────────────────┤
│ 会话恢复 + carry 摘要 + transcript    │  live 侧栏        │  ← 左：可滚动对话
│ [12:34] 你                           │  band 0.42        │     右：Ctrl-B 展开
│   你好                               │  load 0.31        │
│ [12:35] Adam  released               │  …                │
│   自然语言回复…                       │                   │
├──────────────────────────────────────┴───────────────────┤
│ slash panel / 引用预览（条件显示）                         │  ← 内联辅助条
│ Adam ┃ pos 4/12  ←→编辑  /命令  @文件  Ctrl-B侧栏  Ctrl-Q离开 │
╭─ Adam                                                     │  ← 底输入框
╰─› _                                                       │
```

| 区域 | 默认可见 | 快捷键 / 触发 |
|------|----------|----------------|
| 会话恢复区 | 启动时一次 | 自动 |
| 顶栏 | 是 | 固定顶行，0.5s 刷新 |
| 对话消息块 | 是 | 每轮输入/回复 |
| Live 侧栏 | **否** | **Ctrl-B** 展开（右侧固定列） |
| Slash 命令面板 | 输入 `/` 且无后续字符 | 自动 |
| @ 引用预览 | 输入含 `@` | 自动 |
| 底工具栏 | 是 | 常驻 |
| 底输入框 | 是 | 常驻 |

---

## 1. 会话恢复区（启动时）

**作用：** 重新打开终端时，恢复「上次聊到哪」的上下文感，**不**把内容注入当前模型回合。

**显示内容：**

- **carry 摘要**：关系阶段、召回焦点等（来自 `relationship_timeline`、`memory_retrieval_frame`）
- **最近会话列表**：`terminal_session_transcript.jsonl` 中最近 2 个 session 的条数与时间范围
- **最近内容摘录**：当前 session 或跨 session 最近若干条 transcript（纯展示）

**边界：**

- 只读；与 `/resume` 命令同源数据，但启动时自动展示摘要
- 策略写在 `terminal_session_index.json`：`context_policy = stored_for_resume_view_not_injected_into_current_model_context`

**相关命令：** `/resume`、`/resume 5`、`/carry`

---

## 2. 顶栏（Top Bar）

**作用：** 固定显示「谁在说话、常驻是否活着、动力学微段是否开启」。

**字段：**

| 字段 | 来源 | 示例 |
|------|------|------|
| 生命名 | `life_name_registry` / 启动参数 | `Adam` |
| Resident 状态 | `resident_lifecycle_state.json` 或 `terminal_life_loop_state.json` | `background_active` |
| ITR-09 摘要 | 环境变量 `DIGITAL_LIFE_*` | `ITR A✓B·C·D·E·F·V` |

**ITR 字母含义：**

| 字母 | 环境变量 | 含义 |
|------|----------|------|
| A | `DIGITAL_LIFE_BODY_INTEGRATE` | 身体连续积分 |
| B | `DIGITAL_LIFE_PREDICTION_REFRESH` | 预测栈回合刷新 |
| C | `DIGITAL_LIFE_MEMORY_SALIENCE_TICK` | 记忆 salience 加厚 |
| D | `DIGITAL_LIFE_WORKSPACE_TOPK` | 工作区 top-K |
| E | `DIGITAL_LIFE_EXPRESSION_SLOTS` | 表达槽位加厚 |
| F | `DIGITAL_LIFE_INTEGRATOR_PARAMETER_PATCH` | 成长参数 shadow |
| V | `DIGITAL_LIFE_VISUAL_ENCODER` | 可选视觉编码 |

`✓` = 已开启，`·` = 默认关闭。

**边界：** 顶栏不显示情绪 valence、意识 workspace 等细粒度内部信号（避免默认机制外露）。

---

## 3. 对话滚动区（Message Blocks）

**作用：** 产品级消息流——时间、说话人、释放状态、正文分层。

**单条格式：**

```text
[HH:MM] 说话人  released|unreleased
  正文第一行
  正文第二行
```

**说话人：**

| speaker | 显示 |
|---------|------|
| `relation` | `你` |
| `life` / `proactive` | 生命名（如 `Adam`） |
| `command` | `command` |
| `command_result` | `result` |

**释放徽章（仅生命侧）：**

- `released`：`model_expression_state` 中 gate `accepted` 且 `model_expression_applied`
- `unreleased`：gate 阻断或 `completed_unreleased`，或回复为 JSON 结构

徽章来自 `resolve_release_badge()`，写入 transcript 的 `metadata.release_badge`。

**持久化：** 每条消息追加到 `runtime/state/terminal/terminal_session_transcript.jsonl`。

**边界：** 徽章反映**表达释放门**结果，不是「模型好不好」的评分。

---

## 4. Live 侧栏（Ctrl-B）

**作用：** 可选查看当前 live 动力学标量，给开发/调试用的「仪表盘」，**默认关闭**。

**展开方式：** `Ctrl-B` 切换；展开时标量显示在**右侧固定侧栏列**（28 列），不再挤在底工具栏。

**显示字段（有 state 才显示）：**

| 标量 | 来源文件 | 含义 |
|------|----------|------|
| `band` | `body_integrator_state.json` → `continuous.cognitive_bandwidth` | 认知带宽 |
| `load` | `continuous.allostatic_load` | 稳态负荷 |
| `sleep` | `continuous.sleep_pressure` | 睡眠压力 |
| `topk` | `expression_plan.json` → `workspace_topk_k` | 工作区竞争 K |
| `focus` | `workspace_primary_focus` / `workspace_frame` | 当前工作区焦点 |
| `drive` | `proactive_drive_scalar` | 主动发话驱动 |

**边界（红线）：**

- 侧栏关闭时，底栏**不**出现 `guarded`、`valence` 等情绪原文
- 侧栏是 opt-in，不是对话内容的一部分，Adam 不会主动播报这些数字

**相关斜杠：** `/express`、`/body`、`/consciousness`、`/state`

---

## 5. Slash 命令面板（内联）

**作用：** 输入 `/` 且尚未键入子命令时，在底栏上方显示分组命令表，等价于「命令_palette」。

**分组：**

- `常用`：`/me`、`/turn`、`/recall`、`/express`、`/features`…
- `状态`：`/memory`、`/relationship`、`/context`…
- `生命机制`：`/body`、`/growth`、`/dream`…
- `梦境网页`：`/dream-web on|off|status`

**操作：**

- 继续输入筛选（如 `/mem` → `/memory`）
- `↑` `↓` 在补全菜单中选择，`Enter` 确认
- 提交后执行只读检查（不进关系 inbox），详见斜杠命令文档

**实现：** `build_slash_panel_lines()` + prompt_toolkit `CompleteStyle.COLUMN` 补全菜单。

---

## 6. @ 文件引用预览（内联）

**作用：** 输入行含 `@路径` 时，底栏显示引用预览，提交前确认引用了什么。

**支持：**

| 类型 | 预览 |
|------|------|
| 文本文件 | `@path (前 48 字摘要…)` |
| 图片 | `@path (image NNNB)` |
| 目录 | `@path/ (N entries)` |
| 不存在 | `@path (missing)` |
| 越界/禁止 | `@path (blocked)` |

**规则：** 与 `file_reference_turn.py` 一致——禁止 `.git`、`runtime`、`.env`（除 `.env.example`）、超大文件等。

**与 ITR-09-F：** 若 `DIGITAL_LIFE_VISUAL_ENCODER=true` 且引用图片，live turn 会写 `observation/visual_observation.json` 并进入跨模态证据链。

**示例：**

```text
请看 @docs/v0/entry/terminal_product_tui_guide.md
```

底栏：`引用预览: @docs/... (本文档说明 Adam 交互终端…)`

---

## 7. 底输入框（Composer）

**作用：** 关系回合与斜杠命令的统一入口。

**外观：**

```text
╭─ Adam
╰─› _
```

**占位提示：** `输入对话，/ 命令面板，@ 引用文件，Ctrl-B 侧栏`

**输入类型：**

| 输入 | 行为 |
|------|------|
| 普通文字 | 关系回合 → `live_turn_cycle` |
| `/...` | 只读状态/合成检查，不写对话记忆 |
| `@file` | 展开文件引用后进关系回合（最多 4000 字预览） |
| 空行 + Enter | 可能触发 idle 主动发话（若配置） |

**编辑：**

- `←` `→` 光标移动
- `↑` `↓` 历史 / 补全选择
- `Esc` `Enter` 多行插入换行（当前 `multiline=False`，主要用于特殊绑定）
- `Ctrl-Q` 离开终端（resident 继续后台）

---

## 8. 底工具栏（Hints）

**作用：** 常驻快捷键与光标位置，不承载生命机制数值（除非侧栏展开）。

**典型内容：**

```text
Adam ┃ pos 4/12  ←→编辑  ↑↓历史  @文件  /命令  Ctrl-B侧栏  Ctrl-Q离开
```

补全菜单打开时追加：`↑↓ 选择  Enter 确认`，候选过多时：`还有 N 个，继续输入筛选`。

**侧栏关闭时：** 仅显示 `侧栏关闭 · Ctrl-B 展开`（在侧栏片段中，不污染主对话）。

---

## 键盘速查

| 按键 | 功能 |
|------|------|
| `Ctrl-T` | 新建终端 session tab |
| `Ctrl-Tab` / `Shift-Tab` | 下一个 / 上一个 session |
| `Ctrl-1` … `Ctrl-9` | 跳转到对应 tab |
| `Ctrl-Y` | 轮换主题（Adam / Codex / Grok） |
| `Ctrl-B` | 展开/收起 Live 侧栏 |
| `Ctrl-Q` | 退出交互终端（detach） |
| `Ctrl-C` | 中断当前行（prompt_toolkit 默认） |
| `Ctrl-L` | 清屏 |
| `/` | 打开命令补全 + 内联命令面板 |
| `@` | 文件路径补全 + 引用预览 |
| `↑` `↓` | 历史记录，或补全菜单移动 |
| `Enter` | 确认补全或提交行 |

---

## 与斜杠命令的关系

| 你想… | 用 TUI 区域 | 或用命令 |
|--------|-------------|----------|
| 看上一回合表达门 | 消息块 `released` 徽章 | `/turn`、`/express` |
| 看记忆召回 | 启动 carry 摘要 | `/recall`、`/memory` |
| 看能力是否启用 | 顶栏 ITR 摘要 | `/features` |
| 看历史终端记录 | 启动恢复区 | `/resume` |
| 看动力学标量 | Ctrl-B 侧栏 | `/body`、`/express --json` |
| 离开但保持生命活着 | Ctrl-Q | `/exit` |

---

## 验收与测试

```bash
uv run python -m pytest \
  tests/process/test_terminal_layout.py \
  tests/process/test_terminal_ui.py \
  tests/process/test_prompt_toolkit_terminal_app.py \
  tests/process/test_prompt_toolkit_split_terminal_app.py \
  tests/process/test_terminal_input.py -q
```

布局合同字段记录在 `terminal_input_profile.json` → `prompt_toolkit_experience`。

---

## 变更记录

| 日期 | 版本 | 说明 |
|------|------|------|
| 2026-06-18 | product_split_pane_v2 | 异步回合、流式输出、markdown、session tabs、主题与 resize |
| 2026-06-18 | product_split_pane_v1 | Application 真分栏、可滚动对话区、右侧 live 侧栏、代码块渲染 |
| 2026-06-18 | product_three_zone_v1 | 三区布局、消息块、侧栏、slash 面板、引用预览、会话恢复 |