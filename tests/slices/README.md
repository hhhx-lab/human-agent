# Slice Tests

`tests/slices/` 覆盖 `P0` 与 `S00-S11` 主体 slice。

按职责大致分成：

- 方向、权威、神经核心
- 状态根、生命膜、验证膜
- 语言与关系
- 生命目标、schema runner
- 身体、成长支持

当前这一柜里有两类语言测试，角色不同但都保留：

- `test_language_organs.py`：盯器官级对象和字段闭合，防止语言层重新退回临时字典拼装。
- `test_language_relationship.py`：盯 S07 主链与 runtime 写回，确保语言、关系、预测和责任压力一起闭合。

常用命令：

```bash
python3 -m unittest tests/slices/test_language_relationship.py -v
python3 -m unittest tests/slices/test_life_support.py -v
python3 -m unittest tests/slices/test_neural_life_core.py -v
```
