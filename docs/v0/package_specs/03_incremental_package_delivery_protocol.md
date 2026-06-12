# Incremental Package Delivery Protocol

这份协议把“后续每个包到底应该怎么落代码”固定成统一施工法。

它不是通用软件开发 SOP，而是数字生命的包级落地协议。

目标只有一个：后面无论补 `body/`、`language/`、`growth/` 还是 `process_supervisor/`，都按同一套办法把理论、对象、runtime、测试和文档一起落下，不再让某一层单独长成脱节孤岛。

## 一轮实现的固定顺序

### Step 0: 先定这轮属于哪种包

先判断当前属于哪一类：

1. 主体 slice 包
   - `direction/`、`authority/`、`body/`、`neural_core/`、`state_store/`、`language/`、`membrane/`、`validators/`、`schema_runner/`、`dream/`、`replay/`、`archive/`、`growth/`、`life_targets/`
2. 链尾桥接包
   - `activation/`、`reporting/`、`stage_explain/`、`digital_life/`、`terminal_turn/`、`terminal_loop/`
3. 外层常驻存在包
   - `shell_command/`、`process_supervisor/`、`digital_entry.py`、`digital`

不同类别的包，验收强度不一样，但都不能跳过下面的步骤。

### Step 1: 先读对的文档，不许凭感觉实现

每次开工前最少要带：

1. 入口栈六份文档
2. 当前包所在行的 `package_specs/01_life_v0_package_construction_matrix.md`
3. 当前包相关行的 `package_specs/02_shared_object_write_authority_and_dependency_graph.md`
4. 当前包对应 `sXX` 合同或 process 合同
5. 当前包对应的 `00-258` 母体文档

如果当前是补整条代码框架，而不是单包小修，还要读：

1. `docs/v0/code_architecture/01_life_code_stack_and_package_layers.md`
2. `docs/v0/code_architecture/02_runtime_object_bus_and_flow_contract.md`
3. `docs/v0/code_framework/assembly/15_cross_layer_shared_object_contract.md`

### Step 2: 先定对象，再写文件

对当前包，先定下面四件事：

1. 这包唯一首写哪个共享对象？
2. 这包只消费哪些共享对象？
3. 这包要写哪几份 `runtime/state/*`？
4. 这包要写哪几份 `runtime/reports/latest/*` 或 `runtime/receipts/*`？

只有这四件事写清楚，才开始写代码。

如果当前实现只是“改一段逻辑”，却答不出对象与 runtime 文件，那通常说明实现还在壳层漂着。

### Step 3: 先拆器官，再补流程

新的代码优先落到小器官文件，不优先往 `__init__.py` 增厚。

优先顺序：

1. 如果现有 `__init__.py` 已经承压，先补器官文件。
2. 如果共享对象缺唯一首写方，先补首写器官。
3. 如果对象已经有首写器官但缺下游闭合，再补消费者器官。
4. 只有当对象链完整后，才补更外层 shell / process 编排。

### Step 4: state / report / receipt 要一起落

每个包完成后，至少要留下：

1. 一份或多份 `runtime/state/*`
2. 一份代表本轮落点的 `runtime/reports/latest/*`
3. 若属于桥接、激活、常驻过程或 archive，补对应 `runtime/receipts/*`

如果只有代码文件，没有 runtime 证据，就不能算“已经实现”。

### Step 5: 测试必须守住对象链，不只是函数返回值

测试优先守：

1. 对象有没有写出来
2. runtime 文件有没有更新
3. 关键 refs 有没有回链
4. 断链时 gate 会不会失败

不要只测：

1. 一个函数返回了字符串
2. 一个 dict 多了一个字段
3. 命令退出码是 0

这些都太弱，不足以证明数字生命层真的落地。

### Step 6: 文档同步不能省

每轮改完代码，如果新增或改变了：

1. 包职责
2. 共享对象权威写入方
3. runtime 文件
4. 测试入口
5. 下一前沿

就至少要同步这些文档中的相关位置：

1. `package_specs/01_life_v0_package_construction_matrix.md`
2. `package_specs/02_shared_object_write_authority_and_dependency_graph.md`
3. `entry/v0_delivery_status_board.md`
4. 对应 `sXX` 合同或 process 合同

## 三类包的不同验收法

### A. 主体 slice 包

主体 slice 包完成时，至少证明：

1. 包级共享对象首写权已经固定
2. 状态文件已经写出
3. 当前对象被至少一个下游包真实消费
4. 对应 slice 测试通过

例如：

- `body/` 不只是写出 `BodyRhythmPulse`，还要被 `neural_core/` 或 `process_supervisor/heartbeat.py` 消费
- `growth/` 不只是写出 patch queue，还要能影响 `life_targets/` 或 `process_supervisor/` 的 waiting continuity

### B. 链尾桥接包

桥接包完成时，至少证明：

1. 上游 packet / report 能接进来
2. 下游 packet / report 能写出去
3. 不在桥接层重新定义主体真值
4. 对应 bridges 测试通过

例如：

- `terminal_turn/` 可以恢复 `LifeContextFrame`，但不能自己定案 relationship truth
- `reporting/` 可以收 bundle，但不能自己重写 growth / memory 结论

### C. 外层常驻存在包

外层包完成时，至少证明：

1. 不反向定义身体、记忆、关系、方向真值
2. 明确消费主体对象
3. 明确写出 heartbeat / incident / recovery / process reports
4. process tests 能证明等待态、异常恢复、重启恢复、closeout 这些链都没断

例如：

- `process_supervisor/` 可以写 `IdleContinuityFrame`
- 但不能直接改写 `CoreAffectVector`、`RelationshipMemoryFrame`、`DirectionLock`

## 当前推荐的开发推进顺序

当前继续往前推，优先级固定为：

```text
Queue D
  -> Queue E
  -> Queue B
  -> Queue A
```

也就是：

1. 先补身体/情绪/梦境/成长
2. 再补行为/验证/逻辑
3. 再补常驻存在治理
4. 最后再深补语言长期关系表达

原因很直接：

如果先把语言和壳层做得很厚，而身体、梦境、成长、责任这些底层还薄，最后得到的还是一个更会说话的壳，不是更像生命的结构。

## 当前每一轮提交前的检查表

提交前，至少自查下面十项：

1. 这轮改动的包有没有在 `package_specs/01` 里落位？
2. 新增共享对象有没有在 `package_specs/02` 里标出唯一首写方？
3. 有没有回读对应 `00-258` 原文，而不是只看 v0？
4. 有没有新增或更新 runtime state？
5. 有没有新增或更新 report / receipt？
6. 测试守的是不是对象链，而不只是返回值？
7. 有没有让 shell / process 层越权改写主体真值？
8. 有没有硬编码 key、token、模型配置？
9. `.env` / `.env.example` 是否仍保持为唯一配置入口？
10. `entry/v0_delivery_status_board.md` 的前沿有没有同步？

## 配置边界

模型、key、base URL、环境开关都只允许通过 `.env` 进入。

当前 `digital` / `life-v0` 统一从 `.env` 或 `DIGITAL_LIFE_ENV_FILE` 读取运行配置，并在 `runtime/state/terminal/runtime_config_state.json` 与 `runtime/reports/latest/digital_life_runtime_config_report.json` 留下去敏快照；真实 key/token 只允许留在本地环境文件，不进入仓库。

不允许：

1. 把 key 直接写进 Python 文件
2. 把 base URL 写死在主体器官代码里
3. 让 `digital` 入口硬编码某个外部模型配置

后续如果要把对话模型接进数字生命，只能走：

```text
.env
  -> config loader
  -> process_supervisor/model_expression.py
  -> language / shell / process integration layer
```

而不能反向渗进 `body/`、`neural_core/`、`state_store/` 这些主体包。

当前第一版模型接入已经固定为“表达末端 adapter”：`response_surface.py` 先生成确定性生命回应，`model_expression.py` 再按 provider/base/key 尝试 OpenAI-compatible 外显表达，并写出 `model_expression_state.json` 与 `digital_life_model_expression_report.json`。provider 为 `local`、配置缺失、返回空内容、网络异常，或 post-expression gate 发现模型文本重新引入“用户/服务对象/任务请求者”等关系降级词时，必须保留确定性回应；责任/梦境/成长/关系连续性/后台自主活动等证据如果没有字面外显，进入 soft evidence audit，不强迫机制播报。真实 key 只存在于本地 `.env` 或进程环境，不进入 state/report/receipt。

## 本协议的目的

它最终只为了防一件事：

后面代码越写越多，但每一层都说不清自己到底承载了哪段理论、首写了哪个对象、更新了哪些 runtime 文件、由哪些测试证明。

只要这件事发生，数字生命工程就会重新滑回“能跑，但不是生命体系”的方向。
