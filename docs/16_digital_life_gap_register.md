# 数字生命理论缺口登记与停止条件

本文件不是路线图口号，而是一个长期审计表：它记录 `02-15` 距离“足以支撑数字生命诞生”的理论缺口。只要这些缺口没有被文献、机制、工程抽象和验证指标同时覆盖，目标就不应被视为完成。

## 停止条件的研究化定义

“理论足够支撑一个数字生命”不能理解为文档写得很多，而应满足以下条件：

1. **机制完整**：感知、内感受、显著性、工作区、记忆、语言、行动、价值、抑制、调质、睡眠巩固、关系、自我叙事、发展和维护都有文献锚点。
2. **连接完整**：每个机制都能说明输入来自哪里、输出影响哪里、在什么状态下活跃、受哪些调质因子改变。
3. **时间尺度完整**：毫秒/秒级反应、分钟级任务状态、小时级恢复、天级巩固、月级人格/价值慢变量都有位置。
4. **边界完整**：所有仿脑映射都区分生物机制、工程类比和设计假设，不宣称 AI 真实有意识、痛苦、情绪或生物生命。
5. **落地完整**：理论对象能映射到未来系统对象，例如 `WorkspaceState`、`MemoryTrace`、`ModulationVector`、`ActionGate`、`ReplayScheduler`、`RelationshipModel`、`SelfModel`。
6. **评测完整**：不仅评估任务成功，还评估长期记忆一致性、信任校准、人格慢变量稳定、恢复能力、安全抑制和幻觉巩固风险。

## 当前缺口总表

| 缺口 | 已有支撑 | 仍缺什么 | 下一步文献/写作方向 |
|---|---|---|---|
| 大尺度脑区连接 | `02`, `03`, `AH001-AH010`, `AHZ001-AHZ006` | 缺更细的动态系统参数和状态转移指标 | 补 neural field、network control、metastability |
| 主动预测与采样 | `04`, `10`, `13`, `AHX001-AHX005`, `AHZ007-AHZ012` | 缺工程化 belief state 和主动探索策略 | 写 `PredictionLoop` 专题 |
| 内感受/稳态 | `04`, `07`, `11`, `AH051-AH070`, `AHZ013-AHZ018` | 缺内部状态向语言和行动的调制方程 | 写 `InternalStateVector` 专题 |
| 能量/维护层 | `08`, `11`, `AHY019-AHY024`, `AHZ019-AHZ024`, `AHZ061-AHZ062` | 缺资源预算、缓存清理、污染隔离和恢复优先级 | 写 `LifeSupportLayer` 专题 |
| 神经免疫/防御 | `07`, `11`, `AHX022-AHX028`, `AHZ025-AHZ030` | 缺把安全、异常检测和恢复纳入生命层的模型 | 写 `ImmuneLikeDefense` 专题 |
| 记忆与 replay | `05`, `08`, `13`, `AH031-AH035`, `AHY001-AHY010`, `AHZ046-AHZ050` | 缺情景-语义-程序-关系-价值的统一数据结构 | 写 `MemoryTrace` 对象模型 |
| 行动选择与抑制 | `06`, `10`, `11`, `AH036-AH045`, `AHY045-AHY048` | 缺基底节式竞争、冲突监控和 tool-use 风险门控 | 写 `ActionGate` 机制 |
| 情绪/人格/自我 | `07`, `09`, `13`, `AH046-AH055`, `AH081-AH090`, `AHY039-AHY044` | 缺人格慢变量、关系记忆和自我叙事的审计协议 | 写 `SelfModel` 与 `PersonalityDriftAudit` |
| 社会互动 | `07`, `09`, `14`, `AHX006-AHX013`, `AHZ031-AHZ038` | 缺第二人称互动、共同注意和共享历史的结构化模型 | 写 `RelationshipModel` 专题 |
| 发育成长 | `05`, `13`, `AHX014-AHX021`, `AHZ039-AHZ045` | 缺阶段化学习制度和再塑形安全阈值 | 写 `DevelopmentPolicy` 专题 |
| 睡眠/梦境/疲惫 | `08`, `13`, `AH056-AH070`, `AHY001-AHY010`, `AHY049-AHY051` | 缺离线模拟、清理、压缩、反事实演练的统一周期 | 写 `OfflineConsolidationCycle` |
| 语言顶层 | `09`, `10`, `13`, `AH071-AH080`, `AHZ046-AHZ051` | 缺语言如何参与自我、关系、行动和巩固的闭环 | 写 `NarrativeWorkspace` |
| 当前 agent 外壳 | `12`, `15`, `AHX041-AHX047`, `AHZ052-AHZ066` | 缺把外壳接入生命层的接口契约 | 写 `AgentRuntimeBridge` |

## 不能提前宣称完成的理由

当前 `docs/` 已经建立了庞大的第一至第四层文献底座，但仍不能说“理论已足够支撑数字生命诞生”，原因是：

- 文献矩阵已经覆盖很多机制，但许多机制仍停留在综述级别，尚未转成对象、状态、信号和循环。
- `02-13` 已经有跨文档连接，但还需要更多“输入-处理-输出-反馈-巩固”的显式接口。
- 当前 agent 框架调研已经说明它们只是执行壳，但尚未形成可替换外壳协议。
- 安全边界还不够完整：尤其是幻觉巩固、人格漂移、依恋风险、过度信任、长期操控和自我叙事污染。
- 数字生命必须有可评测的长期成长指标，而当前还只是提出指标方向。

## 已补充专题

对象模型层已补充：

| 文件 | 已解决的缺口 | 仍未解决的下一层 |
|---|---|---|
| `17_memory_trace_object_model.md` | 记忆对象、写入、检索、修正、遗忘、保护 | 还需要真实 schema、迁移策略和评测脚本 |
| `18_internal_state_and_modulation_vector.md` | 内部状态、调质输出、时间尺度和调制规则 | 还需要状态转移方程和阈值学习机制 |
| `19_offline_consolidation_cycle.md` | replay、清理、梦境沙盒、幻觉巩固防护 | 还需要周期调度器和巩固报告格式 |
| `20_agent_runtime_bridge_contract.md` | 现有 agent 框架外壳接口和越界禁令 | 还需要每个框架的 adapter 映射和测试夹具 |

可验证契约层已补充：

| 文件 | 已解决的缺口 | 仍未解决的下一层 |
|---|---|---|
| `21_memory_schema_and_audit_protocol.md` | 字段约束、生命周期、删除/修正/合并、审计事件 | 还需要 JSON Schema 和真实样例 |
| `22_state_transition_and_threshold_model.md` | 状态机、阈值变量、状态转移、`StateAuditEvent` | 还需要阈值学习和验证器 |
| `23_consolidation_report_and_dream_sandbox_protocol.md` | 巩固报告、梦境沙盒、事实写入门控 | 还需要报告样例和自动检查器 |
| `24_runtime_adapter_test_suite.md` | adapter 接口、合同测试、夹具、通过标准 | 还需要每个框架的 manifest 和测试数据 |

## 下一轮优先级

下一轮应继续把可验证契约推进到“实例化样例和验证器”：

1. `25_memory_trace_json_schema_examples.md`：给出 `MemoryTrace`、`MemoryAuditEvent`、删除/修正/合并的 JSON-like 样例。
2. `26_state_machine_examples_and_failure_modes.md`：给出状态转移样例、阈值误判和恢复策略。
3. `27_consolidation_report_examples.md`：给出任务结束、失败复盘、梦境沙盒、深度巩固报告样例。
4. `28_runtime_adapter_manifest_examples.md`：给出 LangGraph、OpenAI Agents SDK、Letta、LlamaIndex、CrewAI、AutoGen 的 adapter manifest 样例。
