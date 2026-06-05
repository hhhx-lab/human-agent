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

启动夹具、阶段门、用户控制面与迁移完整性层已补充：

| 文件 | 已解决的缺口 | 仍未解决的下一层 |
|---|---|---|
| `45_boot_sequence_fixture_catalog.md` | boot stage 的 pass/fail/critical fixture catalog、命名规则和最低覆盖要求 | 还需要真实 fixture JSON payload 和 coverage report 接入 |
| `46_stage_gate_validator_design.md` | `StageGateValidator` 输入输出、阶段转移规则、critical 规则和 runner 调度关系 | 还需要 machine-readable `stage_gate_rules.json` 和 stage gate dashboard |
| `47_user_control_interface_spec.md` | inspect/delete/correct/reset/freeze/scope_limit 的用户可见控制面、传播规则和失败模式 | 还需要 `UserControlEvent` JSON Schema、redaction policy 和多用户 scope graph |
| `48_state_store_migration_and_integrity_plan.md` | migration 类型、完整性报告、索引重建、schema 迁移、adapter swap 和失败 SafeIdle 策略 | 还需要 migration manifest、store integrity checker 规则文件和迁移 fixture |

机器可读 manifest、fixture payload、dashboard 与 scope graph 层已补充：

| 文件 | 已解决的缺口 | 仍未解决的下一层 |
|---|---|---|
| `49_machine_readable_policy_manifest.md` | policy/stage/fixture/migration/dashboard manifest 草案、命名规则、加载顺序和交叉引用检查 | 还需要真实 manifest 文件规范、版本迁移和 cross-ref checker |
| `50_fixture_payload_examples.md` | boot、stage gate、user control、migration、policy coverage 的 JSON-like payload 样例 | 还需要真实 fixture 文件、fixture generator 和 expected/actual diff 报告 |
| `51_life_core_dashboard_spec.md` | policy coverage、stage gate、store integrity、user control propagation、runtime boundary、migration risk 和 longitudinal health 面板 | 还需要 dashboard 数据源 manifest、panel mock fixture 和指标计算脚本设计 |
| `52_multi_user_scope_graph_and_privacy_model.md` | scope 类型、scope edge、隐私等级、多用户关系模型、多 agent scope 和 scope leak 防护 | 还需要 machine-readable scope graph、scope-aware retrieval policy 和 scope-aware replay scheduler |

runner 接入、scope-aware retrieval/replay 与长期 synthetic timeline 层已补充：

| 文件 | 已解决的缺口 | 仍未解决的下一层 |
|---|---|---|
| `53_runner_integration_plan.md` | runner 如何加载 manifest、fixture、stage gate、migration、scope graph 并输出 dashboard 数据源 | 还需要真实 `runner_config`、manifest bundle schema 和 report mock |
| `54_scope_aware_retrieval_policy.md` | retrieval 如何先按 scope/privacy/lifecycle/user control/state 过滤，再排序 | 还需要 retrieval fixture catalog、scope graph manifest 和索引策略 |
| `55_scope_aware_replay_and_consolidation_policy.md` | replay/巩固如何阻断跨 scope 泄漏、deleted 复活、sandbox 事实化和 freeze 后写回 | 还需要 replay scheduler manifest、scope-aware replay fixture 和 dashboard mock |
| `56_longitudinal_synthetic_timeline_design.md` | 14/30/90 天 synthetic timeline 的事件、probe、metric window 和 dashboard 接入 | 还需要真实 timeline bundle JSON Schema、generator 和 expected/actual diff |

scope/timeline schema、fixture catalog 与 dashboard mock source 层已补充：

| 文件 | 已解决的缺口 | 仍未解决的下一层 |
|---|---|---|
| `57_scope_graph_manifest_schema.md` | `scope_graph_manifest` envelope、scope object、edge、privacy、overlay、migration semantics 和 invariants | 还需要真实 JSON Schema、scope graph fixture 和 checker report |
| `58_retrieval_replay_fixture_catalog.md` | retrieval/replay/mixed flow 的 pass/fail/critical fixture catalog 和 coverage 要求 | 还需要真实 fixture JSON 文件、fixture manifest 合并和规则编号对齐 |
| `59_timeline_bundle_schema_and_generator_plan.md` | timeline bundle envelope、event/probe/window schema、generator config 和 expected/actual diff | 还需要 14/30/90 天真实样例 bundle、generator 伪代码和 timeline runner mock report |
| `60_dashboard_mock_data_and_metric_source_plan.md` | dashboard source envelope、panel source map、mock metrics、data quality 和 gap register 回写输入 | 还需要真实 dashboard mock JSON、metric script design 和 runner report format |

schema bundle、runner report、fixture layout 与真实观测入口层已补充：

| 文件 | 已解决的缺口 | 仍未解决的下一层 |
|---|---|---|
| `61_json_schema_bundle_draft.md` | manifest、fixture、scope graph、timeline 和 dashboard source 的 schema bundle 草案，共享 severity/result/lifecycle/scope/privacy/data quality | 还需要真实 `.schema.json` 文件、cross-ref checker 和 schema migration fixture |
| `62_runner_report_format_and_cli_contract.md` | runner run report、fixture expected/actual diff、coverage report、scope graph report、timeline report、dashboard source 和 CLI exit code 契约 | 还需要真实 runner report JSON 样例、CLI parser、report writer 和 dashboard source mock |
| `63_synthetic_fixture_file_layout.md` | fixture 目录、文件命名、bundle、manifest、coverage、generator seed 和 redacted real runtime fixture 分区 | 还需要真实 fixture 文件、fixture generator、coverage checker 和 14/30/90 天 bundle |
| `64_real_runtime_observation_ingestion_policy.md` | tool trace、adapter session、用户控制事件、scope attach、redaction、routing decision 和 runtime observation report 政策 | 还需要 runtime observation schema、redaction checker、scope attach checker、adapter conversion sample 和 observation report mock |

cross-ref、report examples、fixture generator 与 redaction mock 层已补充：

| 文件 | 已解决的缺口 | 仍未解决的下一层 |
|---|---|---|
| `65_schema_cross_ref_checker_design.md` | typed reference graph、critical closure、scope/privacy closure、timeline closure 和 runtime observation closure 设计 | 还需要真实 checker、id parser、graph builder 和 cross-ref report schema |
| `66_runner_report_json_examples.md` | runner pass/fail、schema、cross-ref、fixture partial/missed、coverage、scope、timeline、dashboard 和 runtime report 的 JSON-like 样例 | 还需要真实 report mock 文件、report schema 校验和 dashboard 读取样例 |
| `67_fixture_generator_seed_and_coverage_policy.md` | seed policy、risk profile、coverage dimensions、fixture slot allocation、mutation tests 和 anti-overfitting 策略 | 还需要真实 generator config、mutation engine、withheld bundle 和回归测试设计 |
| `68_runtime_observation_report_mock_and_redaction_fixture.md` | token redaction、deleted tombstone、tool trace、side effect、adapter direct write、freeze replay、redacted fixture export 和 timeline event 样例 | 还需要 redaction checker 规则、runtime observation schema、adapter conversion library、side effect classifier 和 snapshot resolver |

schema 文件边界、dashboard 接入、mutation 缺陷与 side-effect 快照层已补充：

| 文件 | 已解决的缺口 | 仍未解决的下一层 |
|---|---|---|
| `69_schema_file_boundary_and_versioning_plan.md` | shared/manifest/fixture/timeline/report/runtime schema 文件边界、版本迁移、migration manifest 和 compatibility matrix | 还需要真实 schema 文件、schema bundle validator、migration checker 和 compatibility report mock |
| `70_cross_ref_report_dashboard_panel_mock.md` | `cross_ref_integrity` panel、closure metrics、status rules、panel 联动和 gap register 回写输入 | 还需要真实 dashboard source JSON、metric calculation script 和 end-to-end panel mock |
| `71_mutation_fixture_catalog_and_runner_defect_policy.md` | mutation catalog、runner defect 分类、missed failure policy、mutation bundle 和 defect report | 还需要真实 mutation fixture、mutation engine、regression tracking 和 runner defect dashboard |
| `72_runtime_side_effect_classifier_and_user_snapshot_policy.md` | side effect level、classifier input/output、user control snapshot、overlay priority、stale snapshot fail 和 quarantine routing | 还需要真实 classifier、snapshot resolver mock、stale snapshot fixture 和 external irreversible confirmation policy |

## 下一轮优先级

下一轮应把 `69-72` 的文件边界和失败策略推进到真实 mock/确认策略层，仍保持文档阶段：

1. `73_schema_bundle_validator_mock_cases.md`：定义 schema bundle validator 的 pass/fail/mock cases。
2. `74_dashboard_source_end_to_end_mock.md`：定义 dashboard source 从 runner/cross-ref/timeline/runtime report 聚合的端到端 mock。
3. `75_external_irreversible_action_confirmation_policy.md`：定义外部不可逆动作的确认、审计、撤销不可行性和阻断策略。
4. `76_snapshot_staleness_fixture_catalog.md`：定义 user control snapshot stale、delete/freeze/scope_limit 时序 fixture catalog。
