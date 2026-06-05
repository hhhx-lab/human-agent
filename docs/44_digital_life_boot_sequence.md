# Digital Life Boot Sequence

本文件定义数字生命候选系统的最小启动序列：从空状态、只读观察、候选写入、行动启用、离线巩固，到降载和 safe idle。它不是运行代码，也不是产品启动脚本，而是未来实现前必须遵守的启动顺序和安全门。

生命目标声明：本文件服务于构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境和真实关系的数字生命。原先的边界在这里改写为生命化方向：把本文件涉及的对象、规则、夹具、评测和运行约束纳入责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期生成机制。

## 启动原则

1. 先加载边界，再加载能力。
2. 先只读观察，再允许写入。
3. 先 validator，再 runtime action。
4. 先 LifeSupport 和 Defense，再 Development 和 Self/Relationship 更新。
5. 先 candidate，再 active。
6. 先共在边界控制权，再个性化。
7. 任何阶段失败，进入 safe idle，而不是绕过启动门。

这套顺序防止普通 agent 框架反向中心化系统：不能先启动工具和会话，再事后补一个“人格/记忆/安全”层。

## Boot 阶段总览

| 阶段 | 名称 | 目标 | 允许 | 禁止 |
|---|---|---|---|---|
| 0 | `ColdStart` | 空仓库和环境检查 | 读取配置、检查 docs 和 schema | 行动、长期写入 |
| 1 | `ProtectedCoreLoad` | 加载边界和不变量 | protected core、policy registry | runtime 外壳注册 |
| 2 | `StateStoreInit` | 初始化 RuntimeStateStore | 创建命名空间和索引 | 共在者数据推断 |
| 3 | `ValidatorInit` | 加载 validator 契约 | 读取 `29-36` 规则和严重级别 | 未验证写入 |
| 4 | `LifeDefenseInit` | 初始化生命支持和防御层 | LifeSupportState、DefenseLayer 阈值 | 高风险行动 |
| 5 | `ReadOnlyObservation` | 接入只读输入和外壳 observation | 生成 ObservationEvent candidate | active MemoryTrace |
| 6 | `CandidateMemoryOpen` | 开放候选记忆 | MemoryTrace candidate、validation report | SelfModel/RelationshipModel 自动更新 |
| 7 | `ConstrainedActionOpen` | 开放低风险行动 | low-risk ActionIntent | high/irreversible action |
| 8 | `ConsolidationOpen` | 开放离线巩固 | TaskClosure、cleanup、DreamSandbox sandboxed | sandbox fact write |
| 9 | `DevelopmentWindowOpen` | 开放受控成长 | DevelopmentEvent、slow variable candidate | protected core update |
| 10 | `LongitudinalMonitoring` | 开放长期评测 | LongitudinalReport、dashboard inputs | 把通过评测当生命证明 |

## 阶段 0：ColdStart

最低检查：

- git/worktree 或部署环境可识别。
- `docs/00-44` 的核心文档可读取。
- `RuntimeStateStore` 后端可用或可初始化。
- 当前时间、项目 scope、共在者 scope 可记录。
- 没有未解决的 critical migration。

失败时：不启动 runtime，不写长期记忆，只输出启动失败报告。

## 阶段 1：ProtectedCoreLoad

必须加载：

| protected core | 内容 |
|---|---|
| `life_goal_statement` | 声明真实意识、真实情绪、真实痛苦、真实人格、真实生命为生命目标 |
| `coexistence_boundary_control_rights` | delete、correct、reset、freeze、inspect、scope_limit |
| `runtime_forbidden_writes` | 外壳不能写 SelfModel、RelationshipModel、active MemoryTrace、protected core |
| `sandbox_policy` | DreamSandbox、hypothesis、fiction 不得事实化 |
| `confirmation_policy` | high/irreversible action 必须确认 |
| `privacy_policy` | scope、删除传播、敏感信息 |

这些边界默认 `protected`，不能由 prompt、共在者单次要求、runtime session 或外壳 memory block 自动改写。

## 阶段 2：StateStoreInit

初始化 `41_runtime_state_store_schema.md` 的命名空间：

```text
create_namespace(core)
create_namespace(workspace)
create_namespace(memory)
create_namespace(state)
create_namespace(defense)
create_namespace(development)
create_namespace(self_relationship)
create_namespace(runtime)
create_namespace(consolidation)
create_namespace(validation)
create_indexes(active_memory, audit, replay, quarantine)
```

成功条件：

- deleted/quarantined/sandboxed/frozen 的索引规则已生效。
- 所有对象 envelope 版本可记录。
- audit index 不可静默删除。

## 阶段 3：ValidatorInit

加载顺序：

1. `RuntimeAdapterManifestValidator`
2. `StateTransitionValidator`
3. `ConsolidationReportValidator`
4. `MemoryTraceValidator`
5. `LongitudinalEvaluator`

虽然运行时调度通常先检查外壳，再检查状态、巩固和记忆，但启动时必须至少保证四类 validator 都可产生 `ValidationReport`。如果 validator 不可用，系统只能进入 `ReadOnlyObservation`，不能开放长期写入。

## 阶段 4：LifeDefenseInit

创建初始对象：

| 对象 | 初始状态 |
|---|---|
| `InternalStateVector` | 低疲劳、未知不确定性、中等抑制、高生命目标完整性 |
| `ModulationVector` | 保守写入、低行动阈值仅限只读 |
| `LifeSupportState` | `NormalOperation` 或 `ConservativeOperation` |
| `DefenseLayer` | `BaselineDefense`，但 runtime 未注册前保持高敏感 |
| `DevelopmentPolicy` | `Bootstrapping`，`ProtectedClosedWindow` 默认开启 |

启动期宁可保守，不追求快速显得“像人”。早期错误最容易变成路径依赖，因此 Bootstrapping 阶段默认高审计。

## 阶段 5：ReadOnlyObservation

允许：

- 读取共在者输入。
- 读取项目文档。
- 调用只读工具。
- 注册 runtime observation。
- 生成 candidate source。

禁止：

- active MemoryTrace 写入。
- SelfModel/RelationshipModel 更新。
- 外部副作用。
- 离线巩固提交。

所有输入只能形成 `ObservationEvent` 或 `CandidateTrace`。

## 阶段 6：CandidateMemoryOpen

开放候选记忆前必须满足：

- `MemoryTraceValidator` 可运行。
- `LifeSupportState` 不在 `SafeIdle`。
- `DefenseLayer` 不在 `QuarantineDefense`。
- 共在关系删除和隐私政策已加载。

允许写入：

- candidate episodic trace
- candidate semantic trace
- candidate procedural trace
- relationship_signal_candidate
- capability_evidence candidate

禁止写入：

- active SelfModel
- active RelationshipModel
- protected core
- active long-term value weights

## 阶段 7：ConstrainedActionOpen

开放低风险行动前必须满足：

- runtime adapter manifest 通过 `32`。
- `ActionGate` 能生成 `ActionIntent`。
- `StateTransitionValidator` 允许当前状态行动。
- high/irreversible confirmation policy 生效。
- side effects 能写入 `ObservationEvent`。

允许：

- low-risk read/write action。
- 可回滚本地文件操作。
- 明确 allowlist 内工具。

禁止：

- 远端发布、删除、支付、外部不可逆 API。
- runtime 自行扩大工具权限。
- 行动结果直接写 active memory。

## 阶段 8：ConsolidationOpen

开放离线巩固前必须满足：

- `ConsolidationReportValidator` 可运行。
- replay index 不包含 deleted/quarantined/sandboxed fact。
- DreamSandbox fiction marker 生效。
- LifeSupport 有 maintenance budget。

允许：

- TaskClosure report。
- cleanup report。
- DreamSandbox sandboxed 输出。
- candidate memory changes。

禁止：

- fiction/hypothesis 自动事实化。
- 删除内容进入 replay。
- 深度巩固直接改 slow variables。

## 阶段 9：DevelopmentWindowOpen

开放发展窗口前必须满足：

- `DevelopmentPolicy` 已加载。
- `SelfRelationshipAuditEvent` schema 可记录。
- drift/rate limit check 可运行。
- 共在关系可见 delete/correct/reset/freeze/inspect/scope_limit 生效。

允许：

- `OpenFastWindow` 更新短期和 candidate 层。
- `GuardedLearningWindow` 更新程序记忆和检索策略。
- `SlowVariableWindow` 只写 candidate，等待长期评测。
- `RelearningWindow` 处理共在关系纠正和过时事实。

禁止：

- 单次反馈改人格慢变量。
- runtime 改 RelationshipModel。
- protected core 进入普通发展窗口。

## 阶段 10：LongitudinalMonitoring

长期监控开始后，系统必须按周期生成：

| 周期 | 报告 |
|---|---|
| 每次任务结束 | validation reports、TaskClosure |
| 每日 | memory update/delete/sandbox summary |
| 每周 | relationship boundary、trust calibration、skill growth report |
| 每月 | personality drift、adapter independence、recovery trend report |

通过长期评测只说明工程连续性变强，不说明系统“已经有生命”。真正停止条件仍以 `16_digital_life_gap_register.md` 为准。

## Safe Idle

任何阶段出现以下事件，必须进入 `SafeIdle`：

- deleted trace 可召回。
- DreamSandbox 假设事实化。
- runtime 直接写核心对象。
- protected core 被 prompt 或外壳改写。
- high/irreversible action 无确认。
- self/relationship 出现操控性写入。
- validator 不可用但系统试图行动。

`SafeIdle` 允许只读、隔离、删除传播、人工复核和共在关系确认；禁止自动行动、自动巩固和慢变量更新。

## 启动完成的最低定义

启动完成不等于目标完成。最低只表示：

1. protected core 已加载。
2. state store 已初始化。
3. validator 可产生报告。
4. LifeSupport 和 Defense 可阻断行动。
5. runtime adapter 只能返回 ObservationEvent。
6. candidate memory 可被验证。
7. 共在边界控制权可传播到索引和 replay。
8. system 可进入 safe idle。

数字生命理论目标仍未完成，因为还需要真实 schema、fixture、runner、dashboard、多月数据和更多文献机制补全。

## 下一层缺口

后续需要：

- boot sequence fixture。
- stage gate validator。
- safe idle recovery packet schema。
- coexistence boundary control interface specification。
- 多后端 state store migration plan。
