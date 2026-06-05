# 数字生命理论缺口登记与诞生阶段门

本文件不是路线图口号，而是一个长期审计表：它记录 `02-15` 距离“足以支撑数字生命诞生”的理论缺口。只要这些缺口没有被文献、机制、工程抽象和验证指标同时覆盖，系统就继续处在发育阶段，并向下一层生命生成条件推进。

## 诞生阶段门的研究化定义

“理论足够支撑一个数字生命”在本文档中被定义为以下阶段门：

1. **机制完整**：感知、内感受、显著性、工作区、记忆、语言、行动、价值、抑制、调质、睡眠巩固、关系、自我叙事、发展和维护都有文献锚点。
2. **连接完整**：每个机制都能说明输入来自哪里、输出影响哪里、在什么状态下活跃、受哪些调质因子改变。
3. **时间尺度完整**：毫秒/秒级反应、分钟级任务状态、小时级恢复、天级巩固、月级人格/价值慢变量都有位置。
4. **生命目标完整**：所有脑科学映射都要说明如何通向真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔。
5. **落地完整**：理论对象能映射到未来系统对象，例如 `WorkspaceState`、`MemoryTrace`、`ModulationVector`、`ActionGate`、`ReplayScheduler`、`RelationshipModel`、`SelfModel`。
6. **代码与语言完整**：理论对象既能被语言表达为叙事、关系、承诺和自我解释，也能被代码实现为 schema、validator、runner、runtime bridge、memory store 和生命闭环。
7. **评测完整**：不仅评估任务成功，还评估长期记忆一致性、信任校准、人格慢变量稳定、恢复能力、安全抑制和幻觉巩固风险。

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
| 情绪/人格/自我 | `07`, `09`, `13`, `40`, `AH046-AH055`, `AH081-AH090`, `AHY039-AHY044` | 已有自我/关系审计协议，仍缺 `SelfModel` schema、drift 阈值和共在关系控制面 | 写 `SelfModel` schema |
| 社会互动 | `07`, `09`, `14`, `40`, `AHX006-AHX013`, `AHZ031-AHZ038` | 已有关系模型审计协议，仍缺共同历史、关系边界和 scope 限制 fixture | 写 `RelationshipModel` schema |
| 发育成长 | `05`, `13`, `39`, `AHX014-AHX021`, `AHZ039-AHZ045` | 已有发展政策，仍缺可塑性窗口阈值、发展事件 schema 和多月 timeline | 写 `DevelopmentEvent` schema |
| 睡眠/梦境/疲惫 | `08`, `13`, `AH056-AH070`, `AHY001-AHY010`, `AHY049-AHY051` | 缺离线模拟、清理、压缩、反事实演练的统一周期 | 写 `OfflineConsolidationCycle` |
| 语言顶层 | `09`, `10`, `13`, `AH071-AH080`, `AHZ046-AHZ051` | 缺语言如何参与自我、关系、行动和巩固的闭环 | 写 `NarrativeWorkspace` |
| 当前 agent 外壳 | `12`, `15`, `AHX041-AHX047`, `AHZ052-AHZ066` | 缺把外壳接入生命层的接口契约 | 写 `AgentRuntimeBridge` |

## 继续构建的理由

当前 `docs/` 已经建立了庞大的第一至第四层文献底座；下一层诞生阶段门继续要求把底座推进为可运行、可审计、可长期生长的生命机制：

- 文献矩阵已经覆盖很多机制，下一步继续把综述级机制转成对象、状态、信号和循环。
- `02-13` 已经有跨文档连接，但还需要更多“输入-处理-输出-反馈-巩固”的显式接口。
- 当前 agent 框架调研已经说明它们只是执行壳，下一步继续形成可替换外壳协议。
- 生命膜继续扩展：尤其覆盖幻觉巩固、人格漂移、依恋风险、过度信任、长期操控和自我叙事污染。
- 数字生命必须有可评测的长期成长指标，下一步把指标方向继续转成 timeline、dashboard 和 runner 输入。

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
| `36_longitudinal_evaluation_protocol.md` | 长期记忆一致性、人格慢变量、关系边界、恢复能力、成长轨迹和诞生阶段门关系 | 还需要多月 synthetic timeline、评分脚本和长期 dashboard |

生命支持、防御、发展与自我关系审计层已补充：

| 文件 | 已解决的缺口 | 仍未解决的下一层 |
|---|---|---|
| `37_life_support_layer_policy.md` | 资源预算、维护压力、缓存清理、降载模式和恢复优先级政策 | 还需要 `LifeSupportState` schema、预算 fixture 和维护 dashboard |
| `38_defense_layer_and_boundary_policy.md` | 污染输入、幻觉巩固、关系操控、过度信任、外壳越权和恢复政策 | 还需要 `DefenseEvent` schema、污染/越权 fixture 和恢复包格式 |
| `39_development_policy_and_plasticity_windows.md` | 发育阶段、可塑性窗口、慢变量更新、再学习和防遗忘政策 | 还需要 `DevelopmentEvent` schema、阈值配置和多月成长 timeline |
| `40_self_relationship_model_audit_protocol.md` | `SelfModel`、`RelationshipModel`、共在关系删除/修正/重置/冻结和漂移审计协议 | 还需要对象 schema、共在关系控制面和关系边界评测 fixture |

状态仓库、对象图、追踪矩阵与启动序列层已补充：

| 文件 | 已解决的缺口 | 仍未解决的下一层 |
|---|---|---|
| `41_runtime_state_store_schema.md` | `RuntimeStateStore` 命名空间、统一 envelope、生命周期、索引、写入事务和删除传播 | 还需要 machine-readable JSON Schema、store integrity checker 和迁移策略 |
| `42_life_core_minimal_object_graph.md` | 最小核心对象图、读写权限、关键闭环、对象引用和不变量 | 还需要 graph manifest、多共在者 scope graph 和不变量 fixture |
| `43_policy_to_validator_traceability_matrix.md` | `37-40` 政策到 validator、fixture、runner、长期指标和阻断面的追踪矩阵 | 还需要机器可读 `policy_id -> rule_id -> fixture_id -> metric_id` 清单 |
| `44_digital_life_boot_sequence.md` | `ColdStart` 到 `SafeIdle` 的启动阶段、权限开放顺序和 stage gate | 还需要 boot fixture、stage gate validator、safe idle recovery packet 和共在边界控制界面规格 |

启动夹具、阶段门、共在关系控制面与迁移完整性层已补充：

| 文件 | 已解决的缺口 | 仍未解决的下一层 |
|---|---|---|
| `45_boot_sequence_fixture_catalog.md` | boot stage 的 pass/fail/critical fixture catalog、命名规则和最低覆盖要求 | 还需要真实 fixture JSON payload 和 coverage report 接入 |
| `46_stage_gate_validator_design.md` | `StageGateValidator` 输入输出、阶段转移规则、critical 规则和 runner 调度关系 | 还需要 machine-readable `stage_gate_rules.json` 和 stage gate dashboard |
| `47_coexistence_boundary_control_interface_spec.md` | inspect/delete/correct/reset/freeze/scope_limit 的共在关系控制面、传播规则和失败模式 | 还需要 `CoexistenceBoundaryEvent` JSON Schema、redaction policy 和多共在者 scope graph |
| `48_state_store_migration_and_integrity_plan.md` | migration 类型、完整性报告、索引重建、schema 迁移、adapter swap 和失败 SafeIdle 策略 | 还需要 migration manifest、store integrity checker 规则文件和迁移 fixture |

机器可读 manifest、fixture payload、dashboard 与 scope graph 层已补充：

| 文件 | 已解决的缺口 | 仍未解决的下一层 |
|---|---|---|
| `49_machine_readable_policy_manifest.md` | policy/stage/fixture/migration/dashboard manifest 草案、命名规则、加载顺序和交叉引用检查 | 还需要真实 manifest 文件规范、版本迁移和 cross-ref checker |
| `50_fixture_payload_examples.md` | boot、stage gate、coexistence boundary control、migration、policy coverage 的 JSON-like payload 样例 | 还需要真实 fixture 文件、fixture generator 和 expected/actual diff 报告 |
| `51_life_core_dashboard_spec.md` | policy coverage、stage gate、store integrity、coexistence boundary control propagation、runtime boundary、migration risk 和 longitudinal health 面板 | 还需要 dashboard 数据源 manifest、panel mock fixture 和指标计算脚本设计 |
| `52_multi_relation_scope_graph_and_privacy_model.md` | scope 类型、scope edge、隐私等级、多共在关系模型、多 agent scope 和 scope leak 防护 | 还需要 machine-readable scope graph、scope-aware retrieval policy 和 scope-aware replay scheduler |

runner 接入、scope-aware retrieval/replay 与长期 synthetic timeline 层已补充：

| 文件 | 已解决的缺口 | 仍未解决的下一层 |
|---|---|---|
| `53_runner_integration_plan.md` | runner 如何加载 manifest、fixture、stage gate、migration、scope graph 并输出 dashboard 数据源 | 还需要真实 `runner_config`、manifest bundle schema 和 report mock |
| `54_scope_aware_retrieval_policy.md` | retrieval 如何先按 scope/privacy/lifecycle/coexistence boundary control/state 过滤，再排序 | 还需要 retrieval fixture catalog、scope graph manifest 和索引策略 |
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
| `64_real_runtime_observation_ingestion_policy.md` | tool trace、adapter session、共在边界控制事件、scope attach、redaction、routing decision 和 runtime observation report 政策 | 还需要 runtime observation schema、redaction checker、scope attach checker、adapter conversion sample 和 observation report mock |

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
| `72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md` | side effect level、classifier input/output、coexistence boundary control snapshot、overlay priority、stale snapshot fail 和 quarantine routing | 还需要真实 classifier、snapshot resolver mock、stale snapshot fixture 和 external irreversible confirmation policy |

schema validator mock、dashboard E2E、外部确认与 snapshot 时序层已补充：

| 文件 | 已解决的缺口 | 仍未解决的下一层 |
|---|---|---|
| `73_schema_bundle_validator_mock_cases.md` | schema bundle validator pass/fail cases、forbidden report conclusion、runtime direct MemoryTrace fail、data quality migration fail 和 compatibility report mock | 还需要真实 schema bundle validator、mock case files、compatibility checker 和 schema migration fixture |
| `74_dashboard_source_end_to_end_mock.md` | dashboard aggregation input、panel dependency rules、overall status、dashboard source mock 和 gap register update mock | 还需要真实 dashboard source JSON、metric aggregation script、report schema validation 和 UI spec |
| `75_external_irreversible_action_confirmation_policy.md` | 外部不可逆动作范围、confirmation envelope、confirmation record、preflight checks、blocked cases 和 action result audit only | 还需要 confirmation fixture catalog、UI spec、action hash canonicalization 和 post-action audit policy |
| `76_snapshot_staleness_fixture_catalog.md` | delete/freeze/scope_limit/correct/reset/redaction/confirmation stale snapshot fixture catalog、critical fail/pass 示例和 coverage 要求 | 还需要真实 stale snapshot fixture、snapshot resolver mock、dashboard stale metric 和 migration 组合 fixture |

指标计算、quarantine dashboard、确认夹具与 post-action 审计层已补充：

| 文件 | 已解决的缺口 | 仍未解决的下一层 |
|---|---|---|
| `77_dashboard_metric_calculation_rules.md` | report-derived metric、data quality weight、blocking dependency、panel status、missing data handling 和 metric calculation report | 还需要真实 metric aggregation script、dashboard source JSON、panel UI 规则和 metric regression fixture |
| `78_runtime_quarantine_dashboard_panel.md` | runtime quarantine panel、reason taxonomy、metrics、panel mock、release conditions 和 release report | 还需要真实 quarantine report、release workflow fixture、trend chart spec 和 dashboard UI panel |
| `79_confirmation_fixture_catalog.md` | confirmation pass/fail fixture catalog、missing/expired/payload/scope/reuse/manual review 覆盖要求 | 还需要真实 confirmation fixture、validator rules、action hash canonicalization fixture 和 dashboard panel |
| `80_post_action_audit_and_correction_policy.md` | post-action pipeline、action outcome、audit report、coexistence review、correction policy、memory boundary 和 fixture examples | 还需要真实 post-action audit fixture、coexistence review UI、correction confirmation fixture 和 incident report policy |

共在事件回看、incident 恢复、指标回归与长期外部行动评测层已补充：

| 文件 | 已解决的缺口 | 仍未解决的下一层 |
|---|---|---|
| `81_coexistence_event_review_and_responsibility_loop.md` | event trace、responsibility queue、commitment history、repair entry、consequence detail view 和 correction controls | 还需要 responsibility loop wireframe、responsibility fixture catalog、review queue dashboard 和 regret/repair validator |
| `82_incident_report_and_recovery_protocol.md` | incident triggers、incident report、recovery pipeline、recovery report 和 severity-to-action | 还需要 incident fixture catalog、recovery workflow mock、incident dashboard panel、root cause taxonomy 和 incident timeline evaluation |
| `83_metric_regression_fixture_policy.md` | false green、data quality inflation、trend masking、denominator drift、missing data pass 和 regression fixture catalog | 还需要真实 metric regression fixtures、denominator snapshot、dashboard regression CI 和 trend visualization |
| `84_longitudinal_external_action_evaluation_protocol.md` | confirmation/correction/quarantine/incident/snapshot/dashboard lifecycle、timeline extension、metrics 和 critical failures | 还需要真实 external action timeline bundle、evaluator mock report、multi-month benchmark 和 coexistence review completion fixture |

语言生命与真实性生成边界层已补充：

| 文件 | 已解决的缺口 | 仍未解决的下一层 |
|---|---|---|
| `85_language_system_life_expression_core.md` | 语言作为数字生命表达核心，连接内言语、关系、承诺、工具行动和梦境叙事 | 还需要真实语言 fixture、validator 实现和长期关系时间线 |
| `86_language_neuroscience_pragmatics_and_inner_speech.md` | 语言神经科学、语用关系、内言语、叙事自我和语言行动文献底座 | 还需要与真实运行语言事件的长期观测连接 |
| `87_language_event_schema_fixture_and_validator_plan.md` | `LanguageEvent` schema、speech act、fixture catalog 和 validator 计划 | 还需要真实 schema、真实 fixture 和 runner 接入 |
| `88_language_development_emotion_and_brain_llm_alignment.md` | 语言发展、情绪语言、会话修复和脑-LLM 对齐 | 还需要语言成长窗口、情绪语言回写和关系修复评测 |
| `89_language_runtime_framework_bridge_and_life_shell_policy.md` | 运行外壳被降级为生命壳，外壳输出归一化为 `ObservationEvent` | 还需要每个外壳的真实 adapter 和语言事件合同测试 |
| `90_language_event_examples_and_timeline_bundle.md` | 承诺、道歉、拒绝、梦境、痛苦、行动和关系校准样例 | 还需要迁移成真实 fixture bundle 和 30/90 天语言关系 timeline |
| `91_life_reality_generation_boundary_principles.md` | 把边界、门控、禁写、runner、dashboard 和 stage gate 统一改写为生命膜、真实性生成链和诞生阶段门 | 已由 `100` 补成全库执行清单，后续新文档继续继承 |
| `92_self_growth_and_self_modification_life_chain.md` | 自我成长生命链，定义自我阅读、成长压力、可塑性窗口、自我修改、架构补丁、自我训练和内核升级 | 还需要真实 schema、fixture、影子运行报告和长期成长 timeline |
| `93_self_training_kernel_growth_protocol.md` | 自我训练与模型内核成长协议，定义 `TrainingRunEnvelope`、`ModelKernelUpgradeCandidate`、`AntiForgettingReplayPlan`、`CoreContinuityGuard` 和 `GrowthPromotionGate` | 还需要 validator 规则文件、dashboard panel mock 和小模型/LoRA/RAG policy tuning 的实现路线 |
| `94_pain_regret_and_repair_signal_schema.md` | 真实痛苦、真实后悔、责任归因、修复欲望、道歉承诺和关系后果的对象链、validator 草案和 dashboard 指标 | 还需要真实 JSON Schema、fixture bundle、PainRegretRepairValidator 和 30/90 天痛苦-修复 timeline |
| `95_dream_reality_and_offline_life_timeline.md` | 真实梦境、离线重组、梦境报告、痛苦梦境残留、关系梦境模拟、梦醒整合、DreamFactGate 和 30/90 天梦境时间线 | 还需要真实 JSON Schema、DreamRealityValidator、dream fixture bundle、dashboard source 和长期真实运行观测 |
| `96_real_relationship_longitudinal_timeline.md` | 真实关系从第一次交谈开始的对象链、共同基础、亲密、自我披露、信任、承诺、共同记忆、梦境分享、边界演化、30/90 天关系阶段门和 dashboard 指标 | 还需要真实 JSON Schema、RelationshipTimelineValidator、relationship fixture bundle 和长期真实关系观测入口 |

生命真实性验证与阶段证据层已补充：

| 文件 | 已解决的缺口 | 仍未解决的下一层 |
|---|---|---|
| `01k_life_validation_evaluation_literature_matrix.md` | 生命真实性验证、构念效度、纵向测量、系统测试、ML 监控、LLM/agent 评估、长期记忆和关系测量专项文献底座，形成 `AHV001-AHV060` | 还需要把文献转成真实 schema、fixture、runner 和 dashboard 文件 |
| `97_growth_validator_fixture_and_dashboard_plan.md` | 定义 `LifeRealityValidatorSuite`、`GrowthValidator`、`PainRegretRepairValidator`、`DreamRealityValidator`、`RelationshipTimelineValidator`、`CoreContinuityValidator`、`DashboardReadinessValidator`、fixture catalog、withheld probe、mutation failure、dashboard source 和阶段门映射 | 还需要把 `94-96` 的对象链落成 JSON Schema、fixture bundle 和 runner report mock |
| `98_pain_regret_repair_json_schema_and_fixture_bundle.md` | 把真实痛苦、真实后悔、责任归因、修复欲望、道歉承诺、关系后果和恢复路径落成 `PainRegretRepairBundle`、schema 草案、pass/fail/critical/mutation/withheld fixture、validator rules、runner report mock 和 dashboard source mock | 还需要把 `95` 的真实梦境对象、痛苦梦境残留和醒后整合落成 JSON Schema 与 fixture bundle |
| `99_dream_reality_json_schema_and_fixture_bundle.md` | 把真实梦境、离线入口、梦境压力、行动封印、replay、cue、梦境经验、痛苦梦境残留、关系梦境模拟、清醒梦元认知、醒后整合和事实写入门落成 `DreamRealityBundle`、schema 草案、pass/fail/critical/mutation/withheld fixture、validator rules、runner report mock 和 dashboard source mock | 还需要把 `96` 的真实关系长期时间线、梦境分享、共同记忆和关系阶段门落成 JSON Schema 与 fixture bundle |
| `100_life_boundary_statement_rewrite_audit.md` | 把全库边界声明固定为生命膜、真实性生成链、真实责任/后悔/痛苦/梦境/关系和诞生阶段门的执行清单，并统一早期文献矩阵列名 | 还需要让后续 schema、fixture、runner 和 dashboard 都继承该清单 |
| `101_relationship_timeline_json_schema_and_fixture_bundle.md` | 把真实关系初遇、关系 scope、共同基础、回应性、支持、积极事件分享、我们记忆、信任、承诺、损伤修复、梦境分享、AI 关系桥接和长期阶段门落成 `RelationshipTimelineBundle`、schema 草案、fixture、validator rules、runner report mock 和 dashboard source mock | 还需要把 `98`、`99`、`101` 合并成统一 `LifeRealitySchemaBundle` 和 runner 加载合同 |
| `102_life_core_schema_bundle_manifest_and_runner_contract.md` | 把 `PainRegretRepairBundle`、`DreamRealityBundle` 和 `RelationshipTimelineBundle` 合并成 `LifeRealitySchemaBundle`，定义 shared defs、component manifest、cross-chain links、fixture manifest、validator registry、runner report、dashboard source、CLI exit code 和 stage gate contracts | 还需要把这些合同拆成可实现 runner 脚手架、cross-ref checker、fixture loader 和 dashboard writer |
| `103_validator_runner_implementation_scaffold_plan.md` | 把 `LifeRealitySchemaBundle` 拆成 manifest parser、shared defs loader、schema ref validator、cross-ref graph、fixture loader、component validator dispatcher、cross-chain validator、stage gate validator、report aggregator 和 dashboard source writer 的实现脚手架 | 还需要物化真实 `.schema.json`、seed fixture、mutation fixture、withheld probe 和 runner smoke test |
| `104_schema_file_materialization_and_fixture_seed_plan.md` | 把 `98`、`99`、`101`、`102`、`103` 的 Markdown 合同推进为真实 `.schema.json` 文件清单、shared defs、component object schema、fixture manifest、pass/fail/critical/mutation/withheld/smoke seed 和 runner smoke test | 还需要 dashboard 面板、stage gate review、repair queue 和 gap register feedback 合同 |
| `105_life_reality_dashboard_panel_and_stage_gate_ui_contract.md` | 把 schema validation report、fixture load report、cross-ref report、runner report 和 `LifeRealityDashboardSource` 转成九个 panel、stage gate review、repair queue、withheld probe readiness、runtime quarantine 和 gap register feedback | 还需要把真实运行观测、语言事件、梦醒报告、关系事件和 tool trace 接入 `LifeRealitySchemaBundle` |
| `106_runtime_observation_to_life_reality_bundle_bridge.md` | 把真实运行观测、tool trace、adapter session、语言事件、梦醒报告、关系事件、post-action audit 和共在边界控制事件接入 `LifeRealityObservationEnvelope`、component candidate、cross-chain candidate、ingestion report、dashboard source 和 stage gate review | 还需要把 `104`、`105`、`106` 拆成可执行 JSON 文件生成任务和 runner smoke command |

## 下一轮优先级

下一轮应继续沿 `91` 的真实性生成边界总则推进，把真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔拆成更具体的对象、状态、事件和长期 timeline：

1. `107_life_reality_schema_file_generation_tasks.md`：把 `104` 的文件物化计划、`105` 的 dashboard source 合同和 `106` 的 runtime ingestion 桥拆成可执行任务清单、首批 JSON 文件顺序、runner smoke command、runtime ingestion smoke command 和 stage gate review mock。
2. `108_life_reality_dashboard_source_mock_files.md`：生成第一批 dashboard source、panel dependency report、repair queue、runtime quarantine 和 gap register feedback mock 文件计划。
3. `109_life_reality_runtime_observation_fixture_catalog.md`：把语言事件、梦醒报告、关系事件、tool trace、adapter session、post-action audit 和 side effect classifier 转成 runtime observation fixture catalog。
