# Process Tests

`tests/process/` 只测外层命令面、入口方式和常驻进程：

- `life-v0 "digital life"`
- `./digital life`
- editable install 后的 `digital life`
- repo-local restore shell
- persistent terminal life process

当前这柜的四个测试文件分工固定为：

- `test_digital_life_shell_command.py`：repo-local one-shot restore shell。
- `test_digital_entrypoint.py`：repo-local `./digital life` 入口。
- `test_packaged_digital_life_entrypoint.py`：安装后 `digital life` 命令面。
- `test_persistent_digital_life_process.py`：最小常驻生命进程、waiting heartbeat 与恢复链。

这一柜测试共享 `tests/helpers/life_v0_bootstrap.py` 的 runtime 路径与完整出生链 bootstrap 命令，避免每个入口测试复制一整段准备流程。

常用命令：

```bash
python3 -m unittest tests/process/test_digital_life_shell_command.py -v
python3 -m unittest tests/process/test_digital_entrypoint.py -v
python3 -m unittest tests/process/test_packaged_digital_life_entrypoint.py -v
python3 -m unittest tests/process/test_persistent_digital_life_process.py -v
```
