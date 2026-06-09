# Tests Layout

`tests/` 现在按工程层分四组，不再平铺在根目录：

- `tests/slices/`：P0 与 `S00-S11` 主体 slice 测试。
- `tests/bridges/`：first activation、replay、archive、report、terminal loop 等桥接链测试。
- `tests/process/`：repo-local shell、`digital` 入口、常驻进程测试。
- `tests/contracts/`：v0 合同覆盖与工程回链测试。

默认全量验证命令：

```bash
python3 -m unittest discover -s tests -p 'test_*.py'
```
