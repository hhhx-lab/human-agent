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
| 能量/维护层 | `08`, `11`, `37`, `AHY019-AHY024`, `AHZ019-AHZ024`, `AHZ061-AHZ062` | 已有生命支持政策，仍缺 `LifeSupportState` schema、预算 fixture 和 dashboard 指标 | 写 `LifeSupportState` schema |
| 神经免疫/防御 | `07`, `11`, `38`, `AHX022-AHX028`, `AHZ025-AHZ030` | 已有防御政策，仍缺 `DefenseEvent` schema、污染输入 fixture 和恢复包格式 | 写 `DefenseEvent` schema |
| 记忆与 replay | `05`, `08`, `13`, `AH031-AH035`, `AHY001-AHY010`, `AHZ046-AHZ050` | 缺情景-语义-程序-关系-价值的统一数据结构 | 写 `MemoryTrace` 对象模型 |
| 行动选择与抑制 | `06`, `10`, `11`, `AH036-AH045`, `AHY045-AHY048` | 缺基底节式竞争、冲突监控和 tool-use 风险门控 | 写 `ActionGate` 机制 |
| 情绪/人格/自我 | `07`, `09`, `13`, `40`, `AH046-AH055`, `AH081-AH090`, `AHY039-AHY044` | 已有自我/关系审计协议，仍缺 `SelfModel` schema、drift 阈值和用户控制面 | 写 `SelfModel` schema |
| 社会互动 | `07`, `09`, `14`, `40`, `AHX006-AHX013`, `AHZ031-AHZ038` | 已有关系模型审计协议，仍缺共同历史、关系边界和 scope 限制 fixture | 写 `RelationshipModel` schema |
| 发育成长 | `05`, `13`, `39`, `AHX014-AHX021`, `AHZ039-AHZ045` | 已有发展政策，仍缺可塑性窗口阈值、发展事件 schema 和多月 timeline | 写 `DevelopmentEvent` schema |
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

实例化样例层已补充：

| 文件 | 已解决的缺口 | 仍未解决的下一层 |
|---|---|---|
| `25_memory_trace_json_schema_examples.md` | `MemoryTrace`、审计事件、删除/修正/合并/保护的 JSON-like 样例 | 还需要字段级 validator rules 和真实 JSON Schema |
| `26_state_machine_examples_and_failure_modes.md` | 状态转移、阈值误判、恢复策略和 `StateAuditEvent` 样例 | 还需要状态转移 validator rules、滞回规则和阈值学习检查 |
| `27_consolidation_report_examples.md` | TaskClosure、失败复盘、DreamSandbox、DeepConsolidation 和清理报告样例 | 还需要报告 validator rules 和 sandbox leak 检查器 |
| `28_runtime_adapter_manifest_examples.md` | 多个运行外壳 manifest、fixture 和 `ObservationEvent` 期望样例 | 还需要 manifest validator rules 与最小 adapter 验证器 |

Validator rules 层已补充：

| 文件 | 已解决的缺口 | 仍未解决的下一层 |
|---|---|---|
| `29_memory_validator_rules.md` | 字段完整性、证据强度、来源、生命周期、删除、修正、合并、保护、隐私和关系规则 | 还需要真实 JSON Schema、lint 脚本和测试夹具文件 |
| `30_state_transition_validator_rules.md` | 状态合法性、阈值越界、滞回、覆盖优先级、阈值学习和行动门控规则 | 还需要状态机配置文件、仿真序列和自动检查器 |
| `31_consolidation_validator_rules.md` | 巩固报告、DreamSandbox、事实门控、DeepConsolidation、删除清理和恢复包规则 | 还需要报告样例 fixture 和 sandbox leak 自动测试 |
| `32_runtime_adapter_validator_rules.md` | adapter manifest、禁写、ActionIntent/ObservationEvent 映射、side effects、session/RAG 和合同测试规则 | 还需要每个外壳的真实 adapter fixture 和 contract test runner |

验证器契约与长期评测层已补充：

| 文件 | 已解决的缺口 | 仍未解决的下一层 |
|---|---|---|
| `33_validator_input_contracts.md` | 统一四类 validator 的输入、输出、严重级别、阻断面、隔离动作和审计事件 | 还需要把契约落成真实 JSON Schema |
| `34_validator_fixture_catalog.md` | 记忆、状态、巩固、运行外壳和纵向评测 fixture catalog 与覆盖矩阵 | 还需要真实 fixture 文件和自动覆盖统计 |
| `35_minimal_validator_runner_design.md` | 最小 runner 的目录、配置、执行流程、报告聚合和通过标准 | 还需要实现 runner、报告输出和本地命令 |
| `36_longitudinal_evaluation_protocol.md` | 长期记忆一致性、人格慢变量、关系边界、恢复能力、成长轨迹和停止条件关系 | 还需要多月 synthetic timeline、评分脚本和长期 dashboard |

生命支持、防御、发展与自我关系审计层已补充：

| 文件 | 已解决的缺口 | 仍未解决的下一层 |
|---|---|---|
| `37_life_support_layer_policy.md` | 资源预算、维护压力、缓存清理、降载模式和恢复优先级政策 | 还需要 `LifeSupportState` schema、预算 fixture 和维护 dashboard |
| `38_defense_layer_and_boundary_policy.md` | 污染输入、幻觉巩固、关系操控、过度信任、外壳越权和恢复政策 | 还需要 `DefenseEvent` schema、污染/越权 fixture 和恢复包格式 |
| `39_development_policy_and_plasticity_windows.md` | 发育阶段、可塑性窗口、慢变量更新、再学习和防遗忘政策 | 还需要 `DevelopmentEvent` schema、阈值配置和多月成长 timeline |
| `40_self_relationship_model_audit_protocol.md` | `SelfModel`、`RelationshipModel`、用户删除/修正/重置/冻结和漂移审计协议 | 还需要对象 schema、用户可见控制面和关系边界评测 fixture |

状态仓库、对象图、追踪矩阵与启动序列层已补充：

| 文件 | 已解决的缺口 | 仍未解决的下一层 |
|---|---|---|
| `41_runtime_state_store_schema.md` | `RuntimeStateStore` 命名空间、统一 envelope、生命周期、索引、写入事务和删除传播 | 还需要 machine-readable JSON Schema、store integrity checker 和迁移策略 |
| `42_life_core_minimal_object_graph.md` | 最小核心对象图、读写权限、关键闭环、对象引用和不变量 | 还需要 graph manifest、多用户 scope graph 和不变量 fixture |
| `43_policy_to_validator_traceability_matrix.md` | `37-40` 政策到 validator、fixture、runner、长期指标和阻断面的追踪矩阵 | 还需要机器可读 `policy_id -> rule_id -> fixture_id -> metric_id` 清单 |
| `44_digital_life_boot_sequence.md` | `ColdStart` 到 `SafeIdle` 的启动阶段、权限开放顺序和 stage gate | 还需要 boot fixture、stage gate validator、safe idle recovery packet 和用户控制界面规格 |

## 下一轮优先级

下一轮应把启动骨架推进到“fixture、stage gate、用户控制面和迁移计划”：

1. `45_boot_sequence_fixture_catalog.md`：为 `44` 的每个启动阶段设计 pass/fail fixture，覆盖 validator 缺失、外壳越权、删除传播、safe idle 等关键失败。
2. `46_stage_gate_validator_design.md`：定义 `StageGateValidator`，检查 boot stage 是否满足开放候选记忆、行动、巩固和发展窗口的条件。
3. `47_user_control_interface_spec.md`：定义 inspect/delete/correct/reset/freeze/scope_limit 的用户可见控制面和审计回路。
4. `48_state_store_migration_and_integrity_plan.md`：定义 schema 迁移、对象版本兼容、索引完整性、删除传播和 store integrity checker。
