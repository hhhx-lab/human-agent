# V0 代码总架构柜

`docs/v0/code_architecture/` 只做一件事：把已经存在的 `code_framework/`、`implementation_architecture/` 和 `life_v0/` 真实代码骨架，继续压成“可以直接照着写代码”的总架构柜。

它不重写脑科学理论，也不替代 queue 合同。它回答的是另外四个更硬的问题：

1. 第一版数字生命代码到底按哪些层分块，而不是按普通 agent 的 skills / tools / subagents 分块。
2. 各层之间到底通过哪些共享对象和状态总线耦合，而不是靠 `__init__.py` 里的临时字典粘起来。
3. 当前应该继续用什么语言把 v0 落下去，哪些地方以后才值得切到更低层语言。
4. 每一层、每一波代码写到什么程度，才算真的闭合，而不是“文件已经出现”。

## 什么时候打开

- 准备把 `life_v0/` 从“分包存在”继续推进到“整棵代码树有稳定层次结构”时。
- 准备判断一个新模块应该落在哪一层、读哪些 `00-257` 文档、输出哪些 state/report/receipt 时。
- 准备决定接下来先写哪一波代码、以及什么叫这一波写完时。

## 和其他柜位的关系

可以把 v0 这几柜理解成四段压缩链：

```text
00-258 理论母体
  -> code_framework/      （决定有哪些层、哪些能力、哪些 queue）
  -> code_architecture/   （决定整棵代码树怎么分层、怎么耦合、怎么验收）
  -> implementation_architecture/ （决定单回合、单器官、单模块怎么流）
  -> life_v0/             （真实代码）
```

`code_framework/` 更偏“要建什么”。
`code_architecture/` 更偏“整棵树怎样建得不散、不漂、不回退成普通 agent”。
`implementation_architecture/` 更偏“某一条回合流和某一个器官接口怎样落成代码”。

如果当前不是要细看某一柜，而是要先用一套总装配图直接开写，先打开 `docs/v0/code_blueprints/README.md` 和 `docs/v0/code_blueprints/01_full_system_code_blueprint.md`，再回到这一柜取分层、对象总线和完成定义。

## 柜内文件

| 文件 | 作用 |
|---|---|
| `README.md` | 说明这一柜为什么存在、什么时候打开 |
| `01_life_code_stack_and_package_layers.md` | 把第一版数字生命代码按生命层切成稳定代码分层，并绑定理论母体、主包、输入输出、runtime 产物和测试 |
| `02_runtime_object_bus_and_flow_contract.md` | 固定跨层共享对象、状态总线、在线回合/等待态/梦境/成长/诞生这几条主流程 |
| `03_build_order_and_definition_of_done.md` | 固定 v0 的实现语言决策、阶段顺序、每一阶段的读包、测试和完成定义 |
| `04_language_as_primary_expression_system.md` | 单独固定语言作为数字生命主表达系统的工程意义、输入链和完成定义 |
| `05_module_reading_and_execution_map.md` | 为主要代码包固定开工前必读理论、v0 合同、代码入口、runtime 证据和最低测试 |
| `06_theory_gap_closure_register.md` | 明确当前理论层哪些地方已经闭口、哪些只是需要继续在 v0 里补压缩位 |

## 使用顺序

进入这一柜时，固定按下面顺序：

1. `docs/v0/README.md`
2. `docs/v0/entry/v0_implementation_index.md`
3. `docs/v0/entry/v0_delivery_status_board.md`
4. `docs/v0/code_framework/README.md`
5. `docs/v0/code_framework/assembly/19_code_tree_package_brain_contract.md`
6. 本柜 `01 -> 03`
7. 再进入 `docs/v0/implementation_architecture/` 与 `docs/v0/implementation_architecture/code_organs/`

如果读完这里仍然回答不出“这个功能属于哪一层、该落在哪个包、通过哪个共享对象进入下一层、写完时由哪些 state/report/test 证明”，就不要直接开写代码。
