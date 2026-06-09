# Contract Tests

`tests/contracts/` 负责验证 `docs/v0` 与当前工程实现之间的硬回链。

当前主入口：

```bash
python3 -m unittest tests/contracts/test_v0_contracts.py -v
```

它的职责不是替代 slice/bridge/process 测试，而是检查文档入口、合同覆盖和工程回链有没有断。
