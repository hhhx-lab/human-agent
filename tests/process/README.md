# Process Tests

`tests/process/` 只测外层命令面、入口方式和常驻进程：

- `life-v0 "digital life"`
- `./digital life`
- editable install 后的 `digital life`
- repo-local restore shell
- persistent terminal life process

常用命令：

```bash
python3 -m unittest tests/process/test_digital_life_shell_command.py -v
python3 -m unittest tests/process/test_digital_entrypoint.py -v
python3 -m unittest tests/process/test_packaged_digital_life_entrypoint.py -v
python3 -m unittest tests/process/test_persistent_digital_life_process.py -v
```
