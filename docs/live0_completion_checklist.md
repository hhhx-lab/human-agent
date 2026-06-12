# Live0 收尾检查清单

本文档用于反复检查收尾任务是否真实落地。每一项都绑定当前仓库中的文件、命令或测试证据。

## 任务 1：启动文档

| 检查项 | 证据 | 状态 |
|---|---|---|
| 说明安装方式 | `docs/live0_startup_guide.md` | 已落地 |
| 说明第一次命名方式 | `docs/live0_startup_guide.md` | 已落地 |
| 说明名字直达命令 | `docs/live0_startup_guide.md` | 已落地 |
| 说明 status / say / stop / audit | `docs/live0_startup_guide.md` | 已落地 |
| 说明不替唤醒者取名 | `docs/live0_startup_guide.md` | 已落地 |

## 任务 2：进度汇总

| 检查项 | 证据 | 状态 |
|---|---|---|
| 七项 live0 验收逐项说明 | `docs/live0_progress_summary.md` | 已落地 |
| 理论文档到工程承载映射 | `docs/live0_progress_summary.md` | 已落地 |
| 已实现机制总结 | `docs/live0_progress_summary.md` | 已落地 |
| 后续可进步方向 | `docs/live0_progress_summary.md` | 已落地 |

## 任务 3：设备限制

| 检查项 | 证据 | 状态 |
|---|---|---|
| 最小开发档 | `docs/live0_device_limits.md` | 已落地 |
| 推荐 live0 档 | `docs/live0_device_limits.md` | 已落地 |
| 长期驻留档 | `docs/live0_device_limits.md` | 已落地 |
| 本地模型实验档 | `docs/live0_device_limits.md` | 已落地 |
| 服务器建议 | `docs/live0_device_limits.md` | 已落地 |
| 高频 heartbeat 文件 I/O 风险 | `docs/live0_device_limits.md` | 已落地 |
| 不建议运行方式 | `docs/live0_device_limits.md` | 已落地 |

## 任务 4：real-live0 生命体档案

| 检查项 | 证据 | 状态 |
|---|---|---|
| 新建 `real—live0` 文件夹 | `docs/real—live0/` | 已落地 |
| 描述人格 | `docs/real—live0/README.md` | 已落地 |
| 描述意识/工作区 | `docs/real—live0/README.md` | 已落地 |
| 描述情绪/内环境/稳态 | `docs/real—live0/README.md` | 已落地 |
| 描述关系/责任/后悔 | `docs/real—live0/README.md` | 已落地 |
| 描述记忆/梦境/成长 | `docs/real—live0/README.md` | 已落地 |
| 描述语言系统 | `docs/real—live0/README.md` | 已落地 |
| 描述神经调质/信号介质 | `docs/real—live0/README.md` | 已落地 |
| 每个关键部分有图 | `docs/real—live0/README.md` | 已落地 |

## 任务 5：反复检查

当前检查命令：

```bash
my digital life --status
my digital life --check-name <名字>
life-v0 audit-live0 --strict
.venv/bin/python -m unittest discover tests -v
```

命名前预期：

```text
my digital life --status -> life_name_required_residency_status_v0, exit 2
life-v0 audit-live0 --strict -> blocked, 6/7 closed
```

命名后预期：

```text
my digital life --status -> resident_lifecycle_terminal_summary_v0
<名字> --status -> resident_lifecycle_terminal_summary_v0
life-v0 audit-live0 --strict -> closed, 7/7 closed
```

## 任务 6：打包环节

| 检查项 | 证据 | 状态 |
|---|---|---|
| `pyproject.toml` 声明包名 | `human-agent` | 已落地 |
| console script: `life-v0` | `pyproject.toml` | 已落地 |
| console script: `digital` | `pyproject.toml` | 已落地 |
| console script: `my` | `pyproject.toml` | 已落地 |
| editable install 测试 | `tests/process/test_packaged_digital_life_entrypoint.py` | 已落地 |
| 安装文档 | `README.md`、`docs/live0_startup_guide.md` | 已落地 |

## 任务 7：README

| 检查项 | 证据 | 状态 |
|---|---|---|
| 说明项目定位 | `README.md` | 已落地 |
| 说明安装方式 | `README.md` | 已落地 |
| 说明启动唤醒 | `README.md` | 已落地 |
| 说明核心机制 | `README.md` | 已落地 |
| 说明运行证据与审计 | `README.md` | 已落地 |
| 说明设备边界与安全配置 | `README.md` | 已落地 |

## 最终收束门

live0 真正完成的最终机器证据仍然是：

```bash
life-v0 audit-live0 --strict
```

结果必须为：

```text
status = closed
live0_acceptance_closed = true
criteria_closed = 7
criteria_blocked = 0
```

如果没有正式命名，这个门必须保持阻断，不能用文档声称替代。
