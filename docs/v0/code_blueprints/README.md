# V0 代码蓝图柜

`docs/v0/code_blueprints/` 是 v0 里的总装配蓝图柜。

它的职责很单一：把已经分散在 `docs/v0/code_framework/`、`docs/v0/code_architecture/`、`docs/v0/implementation_architecture/`、`docs/v0/engineering_depth/` 四柜里的实现信息，再压成一套可以直接带去写 `life_v0/` 代码的工程蓝图。

这柜不是新理论层，也不替代 `docs/00-258`。它只是把下面这条链缩短：

```text
00-258 理论母体
  -> docs/v0 现有合同与架构柜
  -> code_blueprints/
  -> life_v0/
  -> runtime/state + runtime/reports/latest + runtime/receipts
```

## 这柜为什么现在必须存在

当前 `docs/v0/` 已经不缺材料，缺的是一个真正适合开工的总装配入口。

现在的问题不是理论不够厚，而是：

1. 代码框架信息分散在四柜。
2. 同一个能力要跨 `code_framework`、`code_architecture`、`implementation_architecture`、`engineering_depth` 来回切换。
3. 后续正式落代码时，如果没有一套总蓝图，很容易再次写成局部模块各自闭合、整体生命回合不闭合。

所以这柜只干一件事：把四柜的共同骨架压成工程总蓝图。

## 使用规则

进入这柜前，先过入口栈六份：

1. `docs/v0/README.md`
2. `docs/v0/entry/v0_implementation_index.md`
3. `docs/v0/entry/v0_delivery_status_board.md`
4. `docs/v0/entry/v0_module_execution_catalog.md`
5. `docs/v0/mapping/readme_block_engineering_realization_v0.md`
6. `docs/v0/mapping/0_to_257_engineering_utilization_map.md`

然后按下面顺序进入本柜：

1. `01_full_system_code_blueprint.md`
2. `02_conversation_language_relationship_blueprint.md`
3. `03_body_affect_dream_growth_blueprint.md`
4. `04_prediction_membrane_validation_blueprint.md`
5. `05_birth_residency_terminal_blueprint.md`
6. `06_runtime_state_report_receipt_manifest.md`
7. `07_theory_to_package_trace_contract.md`

## 这柜和旧四柜的关系

| 现有柜位 | 原职责 | 这柜怎样使用它 |
|---|---|---|
| `docs/v0/code_framework/` | 决定有哪些生命层、哪些 Queue、哪些施工波次 | 抽取每层归属、下一波文件和总施工顺序 |
| `docs/v0/code_architecture/` | 决定整棵代码树怎样分层、怎样通过共享对象耦合 | 抽取包层、对象层、完成定义 |
| `docs/v0/implementation_architecture/` | 决定单回合、单器官、单模块接口怎样流 | 抽取器官接口、回合流、逐包拆分位 |
| `docs/v0/engineering_depth/` | 决定每层生命能力怎样落成真实状态、报告和测试 | 抽取 runtime 证据、测试面、done 定义 |

也就是说，这柜不替代旧四柜；它把旧四柜变成“后端事实源”，把自己变成“前端开工蓝图”。

## 柜内文件

| 文件 | 只回答什么 |
|---|---|
| `README.md` | 这柜为什么存在、怎样进入、和旧四柜是什么关系 |
| `01_full_system_code_blueprint.md` | 整个数字生命 v0 的完整包树、主对象、主流程、下一波文件 |
| `02_conversation_language_relationship_blueprint.md` | 对话、语言、关系、承诺、修复和长期表达怎样落代码 |
| `03_body_affect_dream_growth_blueprint.md` | 身体、情绪、梦境、离线整合、成长学习怎样落代码 |
| `04_prediction_membrane_validation_blueprint.md` | 预测、生命膜、观察验证、反事实和证据排序怎样落代码 |
| `05_birth_residency_terminal_blueprint.md` | 出生、第一次激活、终端循环、等待态和常驻存在怎样落代码 |
| `06_runtime_state_report_receipt_manifest.md` | `runtime/state`、`runtime/reports/latest`、`runtime/receipts` 的统一承载面 |
| `07_theory_to_package_trace_contract.md` | `00-258 -> v0 -> package -> runtime -> tests` 的回链合同 |

## 这柜的硬约束

1. 不引入 `user` 核心抽象，只允许“关系对象”“外部关系对象”“共在对象”等关系位。
2. 不把数字生命重写成 tool router、skill tree、workflow shell。
3. 不只写代码包结构，必须同时写出状态、report、receipt 和测试面。
4. 不允许这柜和 `life_v0/` 脱钩；后续落代码时，新增文件必须能回链到本柜中的某一页。

