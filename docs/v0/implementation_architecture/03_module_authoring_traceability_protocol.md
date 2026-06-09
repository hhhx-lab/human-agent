# Module Authoring Traceability Protocol

本文档规定：后续每一个新模块，必须怎样从理论进入代码，并留下可审计映射。

它的目的只有一个：

```text
不让任何一个新文件
变成“能跑，但不知道承载哪条理论、改了哪条生命链、留下了什么证据”的黑盒。
```

## 适用范围

本协议适用于：

- `life_v0/` 下所有新增 Python 文件
- 现有重型 `__init__.py` 的器官拆分
- 新增 tests
- 新增 runtime state / report / receipt
- 与之对应的 `docs/v0/*` 更新

## 每个新模块的五重来源

任意一个新模块，都必须同时能回答下面五个问题：

1. 它回读了哪些 `00-258` 理论文档？
2. 它属于哪一份 v0 合同或哪一柜实现蓝图？
3. 它首写或首读哪个共享对象？
4. 它写出哪份 state/report/receipt？
5. 它由哪个测试和 gate 守住？

五个问题里答不上任意一个，就不能合并这个模块。

## 新模块必须同时更新的文档位

新增一个真实模块时，默认至少同步更新下面三处：

| 文档位 | 作用 |
|---|---|
| 对应 Queue 合同或 slice 合同 | 说明这个模块为什么存在、属于哪条生命链 |
| `implementation_architecture/01_runtime_organ_interface_blueprint.md` | 说明它和其他器官怎样接线 |
| `implementation_architecture/02_turn_and_cycle_lifecycle_contract.md` 或本文件 | 说明它在外部回合或离线环的哪一步发生作用 |

如果模块改变了当前前沿，再额外更新：

- `docs/v0/entry/v0_delivery_status_board.md`
- `docs/v0/entry/v0_module_execution_catalog.md`

## Python 模块最小骨架

每个器官模块至少应具备下面这些东西：

```python
from __future__ import annotations

from typing import Any

SOURCE_DOC_REFS = [
    "docs/..理论文档..md",
    "docs/v0/..合同文档..md",
]

def build_xxx(... ) -> dict[str, Any]:
    ...

def check_xxx(payload: dict[str, Any]) -> list[str]:
    ...
```

### 硬要求

1. `SOURCE_DOC_REFS` 必须出现。
2. `build_*` 与 `check_*` 成对出现，除非它是纯数据变换器官。
3. 输出对象必须有 `schema_version`。
4. 如果对象代表独立器官或独立状态，还必须有 `object_kind`。
5. 所有输出都要带 `run_id`、`generated_at`。

## Runtime 输出最小协议

### State 文件

每份 state 至少包含：

- `schema_version`
- `run_id`
- `generated_at`
- `source_doc_refs`
- 当前器官的关键字段

### Report 文件

每份 report 至少包含：

- `schema_version`
- `engineering_slice_ref`
- `status`
- `readme_block_refs`
- `runtime_carrier_refs`
- `state_refs`
- `archive_receipt_ref` 或下一步 receipt ref

### Receipt 文件

每份 receipt 至少包含：

- `schema_version`
- `receipt_id`
- `run_id`
- `command`
- `input_hashes`
- `output_hashes`
- `stage_effect`

## 测试最小协议

新增模块时，默认至少做一层直接测试，必要时再做桥接测试。

| 模块类型 | 最小测试位 |
|---|---|
| 主体器官 | `tests/slices/` |
| 桥接链器官 | `tests/bridges/` |
| 常驻过程与命令面 | `tests/process/` |
| 合同/入口层更新 | `tests/contracts/` |

### 测试内容最低要求

1. 断言 `schema_version`
2. 断言关键字段存在
3. 断言关键 gate 能闭合
4. 断言新 state/report/receipt 路径真的写出
5. 断言新对象被当前回合链真正吃到，而不是孤立文件

## 新模块落地步骤

后续每次写一个新模块，都按下面顺序：

1. 先在对应 Queue 合同里确认它的职责和输入输出。
2. 回 `00-258` 找到理论母体，写入 `SOURCE_DOC_REFS`。
3. 在测试里先要求它写出目标 state/report/receipt。
4. 再写最小 `build_* / check_*`。
5. 接入当前 `__init__.py` 或 orchestration file。
6. 跑最小测试。
7. 回写 `implementation_architecture/01` 的器官接口行。
8. 如果它改变了回合流，再回写 `implementation_architecture/02`。

## 当前最值得继续按本协议推进的模块

### Queue E

- `life_v0/membrane/shadow_gate.py`
- `life_v0/schema_runner/evidence_ranker.py`

`life_v0/membrane/responsibility_loop.py` 已经落地，当前把它视为“继续补厚的已落器官”，而不是默认新增文件。

### Queue B

- `life_v0/process_supervisor/idle_strategy.py`
- `life_v0/process_supervisor/persistent_process.py`

### Queue A

- `life_v0/language/relationship_timeline.py`
- `life_v0/language/commitment_expression.py`
- `life_v0/language/apology_repair_language.py`

## 合并前检查清单

每次提交前，至少过一遍这张表：

| 检查项 | 必须满足 |
|---|---|
| 理论回链 | 新模块 `SOURCE_DOC_REFS` 能回到 `00-258` 和 v0 合同 |
| 共享对象 | 能说明首写/首读哪个共享对象 |
| runtime 证据 | 新 state/report/receipt 已写出且路径稳定 |
| 测试 | 对应 `tests/*` 已覆盖 |
| 文档映射 | 本柜与对应 Queue 合同已更新 |
| 前沿同步 | 如果改变当前最优先队列，状态板和执行目录已同步 |

## 不允许出现的退化

1. 只写 Python 文件，不写 runtime 产物路径。
2. 只写 runtime 文件，不给测试。
3. 只给测试，不写 `SOURCE_DOC_REFS`。
4. 只在 `__init__.py` 堆逻辑，不把器官拆出来。
5. 把“关系对象”重新写回“用户输入处理”。
6. 把梦境/成长/责任回路写成注释或 TODO，而不真正进回合流。
