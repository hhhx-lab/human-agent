# Tests Layout

`tests/` 现在按工程层分四组，不再平铺在根目录：

- `tests/slices/`：P0 与 `S00-S11` 主体 slice 测试。
- `tests/bridges/`：first activation、replay、archive、report、terminal loop 等桥接链测试。
- `tests/process/`：repo-local shell、`digital` 入口、可安装命令面、常驻进程测试。
- `tests/contracts/`：v0 合同覆盖与工程回链测试。
- `tests/helpers/`：共享测试夹具，不直接放测试用例；当前承载标准 runtime 路径和完整出生链 bootstrap 命令。

整理规则固定如下：

- repo 根目录不再新增零散 `test_*.py`。
- slice/bridge/process/contract 四柜之外的新测试，先判断它属于哪一层，再落到对应目录。
- 像 `tests/slices/test_language_organs.py` 这类“器官级回归测试”仍归 `tests/slices/`，不单独再长一层测试目录。

每个子目录现在各自带一个 `README.md`，只解释这一柜测试在验证哪一层，避免重新翻整仓库文件名。

`__pycache__/`、`.pyc`、`*.egg-info` 都视为生成物，不保留在整理后的工作区里。

默认全量验证命令：

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```
