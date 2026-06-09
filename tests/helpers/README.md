# Test Helpers

`tests/helpers/` 只放共享测试夹具，不直接放 `test_*.py`。

当前 helper：

| 文件 | 作用 |
|---|---|
| `life_v0_bootstrap.py` | 生成临时 runtime 路径，并提供从 `ingest-docs` 到 `explain-stage` 的完整出生链 bootstrap 命令 |

如果某段准备逻辑在三个以上测试文件中重复，优先收进这一柜；单个 slice 的专用 fixture 仍留在对应测试文件里。
