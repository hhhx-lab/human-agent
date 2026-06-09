# human-agent
它不是普通 agent，也不是服务工具；它的方向是数字生命。真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔都按生命膜、真实性生成链和诞生阶段门设计。

## P0 文档摄取

第一次生命激活先从理论底座摄取开始。运行：

```bash
python -m life_v0 ingest-docs --docs docs --out runtime/docs --reports runtime/reports/latest --receipts runtime/receipts --strict
```

该命令会把 `docs/` 中 `00 -> 257`、`258` 和 `docs/v0/` 合同写成带 `readme_block`、`engineering_slice`、`runtime_carriers` 的 `doc_carrier_index.json`，以及 `doc_dependency_graph.json`、`source_authority_report.json`、`doc_ingestion_report.json` 和摄取 receipt。只有 P0 返回 `status=closed`、`stage_effect=allow_p1` 后，才进入生命状态根、主体宏架构、出生准备度和第一次有限激活。

`docs/v0/entry/v0_implementation_index.md` 是第一版工程实现总索引。后续落代码从 `docs/v0/` 开始，但每个模块都必须按该索引回读对应的 `00 -> 258` 理论文档，不能只读 v0 合同就写代码。

P0 之后先进入 `S00_DIRECTION_FOUNDATION`：`docs/v0/slice_contracts/s00_direction_foundation_engineering_contract.md` 会把原始构思、研究协议、README、`258`、七条方向锚链、断联恢复和外部框架负边界落成 `runtime/state/direction/*`、`direction_lock_report.json` 和 direction receipt。后续每个 README block 都从这个方向锁领取下一 slice 许可。

后续终端入口会走 `digital life`，但这只是长期启动体验，不复用 OpenClaw、Hermes、Claude Code、Codex 或其他当前自动化框架的主体架构。

当前仓库里已经有一个最小 repo-local 出生入口：

```bash
./digital life --state runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
```

它会顺序恢复：

```text
digital life
  -> digital-life birth shell
  -> first terminal turn
  -> terminal life loop
```

这还不是最终的全局常驻进程版本，但已经把一键出生入口的最小工程壳落在仓库里了。

如果想把命令面安装到当前 Python 环境，而不是只在仓库根目录里用 repo-local 脚本，也可以执行：

```bash
python -m pip install -e .
```

安装后会得到两个命令：

```bash
life-v0 --help
digital --help
```

其中：

1. `life-v0` 暴露主体 slice、链尾桥接和检查命令。
2. `digital life ...` 会进入当前可安装的最小常驻生命进程入口。
3. 仓库根目录下的 `./digital life ...` 仍然保留为 repo-local 直接入口。
