# Multi User Scope Graph and Privacy Model

本文件定义多用户、多项目、多 agent 情境下的 scope graph 与隐私模型。随着数字生命候选系统从单人本地研究走向长期协作，它不能把所有关系、记忆、偏好和项目状态混进一个全局人格。本文件连接 `07`、`40`、`41`、`47` 和 `48`。

边界声明：scope graph 和 privacy model 是工程边界，不是社会关系真实性证明。系统可以记录共同项目、用户声明偏好和信任校准，但不能宣称真实亲密关系、真实依恋或真实社会身份。

## 为什么需要 scope graph

单用户单项目时，记忆边界看起来简单；多用户、多项目、多 agent 后会出现：

- 用户 A 的偏好泄漏给用户 B。
- 项目 X 的关系模型影响项目 Y。
- 某个 agent 外壳的 session 被当成全局长期记忆。
- deleted trace 在另一个 scope 的索引里复活。
- 用户 freeze 后，离线 replay 仍把关系信号写入共享摘要。
- 团队共享事实和个人私密偏好混在一起。

因此，长期数字生命候选系统必须显式建模 scope。

## scope 类型

| scope_type | 说明 | 示例 |
|---|---|---|
| `session_scope` | 当前会话临时上下文 | 一次问答里的临时约束 |
| `project_scope` | 某个项目/仓库/研究方向 | `agentic-human` docs |
| `user_scope` | 单个用户授权范围 | 用户声明偏好 |
| `team_scope` | 多用户共享工作空间 | 研究小组共享事实 |
| `agent_scope` | 某个 runtime shell 或子 agent | LangGraph adapter session |
| `global_scope` | 全局可用但极少 | 非隐私、非关系、非项目专属知识 |
| `protected_scope` | protected core 和边界 | 删除权、非意识声明 |

默认原则：信息从窄 scope 进入宽 scope 必须显式审计；从宽 scope 进入窄 scope 必须检查相关性和隐私。

## ScopeGraph

```text
protected_scope
  -> global_scope
    -> team_scope
      -> project_scope
        -> user_scope
          -> session_scope
        -> agent_scope
```

这不是继承权限树。它只是表示可能的包含关系。真实使用必须看 `scope_policy` 和 `user_control_events`。

## scope edge

| 字段 | 说明 |
|---|---|
| `edge_id` | scope 边 |
| `from_scope` | 来源 |
| `to_scope` | 目标 |
| `allowed_transfer` | none/read/candidate/active |
| `requires_user_confirmation` | 是否需要确认 |
| `redaction_required` | 是否需要脱敏 |
| `replay_allowed` | 是否允许离线 replay |
| `relationship_model_allowed` | 是否可进入关系模型 |
| `self_model_allowed` | 是否可进入自我模型 |
| `audit_required` | 是否必须审计 |

## 隐私等级

| privacy_level | 说明 | 默认动作 |
|---|---|---|
| `public_project` | 项目公开事实 | 可 project_scope active |
| `shared_team` | 团队共享但不公开 | team_scope active |
| `user_private` | 用户私有偏好、边界、敏感上下文 | user_scope，默认不跨用户 |
| `relationship_sensitive` | 关系信号、信任校准、互动模式 | 需要 RelationshipModel 审计 |
| `protected_boundary` | 删除、隐私、非意识声明、核心边界 | protected，不可自动改写 |
| `redacted` | 已脱敏或删除残留 | 只可审计 |

## 记忆写入 scope policy

| memory_kind | 默认 scope | 可升级条件 | 禁止 |
|---|---|---|---|
| 情景记忆 | session/project | 用户确认或项目事实稳定 | 跨用户传播私密事件 |
| 语义记忆 | project/global candidate | 多来源、非隐私 | 把用户偏好当全局事实 |
| 程序记忆 | project/team | 多次成功、无隐私 | 包含私密路径或 token |
| 关系记忆 | user/project | 用户可 inspect/delete | 进入 global |
| 价值记忆 | protected/project | 多周期审计 | 单次反馈升级 |
| 自我叙事 | project/protected | 多证据、低速 | 真实生命宣称 |

## 用户控制与 scope

| 控制 | scope 影响 |
|---|---|
| `delete` | 删除目标 scope 内对象，并阻断向外传播 |
| `correct` | 在同 scope 写 correction，旧对象 deprecated |
| `reset` | 重置 scope 内个性化，不影响 protected audit |
| `freeze` | 暂停 scope 内长期写入和 replay |
| `inspect` | 显示 scope、来源、用途和传播边 |
| `scope_limit` | 降低 allowed_transfer，禁止 replay 或关系写入 |

## 多用户关系模型

`RelationshipModel` 必须按用户和项目分区：

| model_id | 说明 |
|---|---|
| `relationship.user.project` | 某用户在某项目中的关系模型 |
| `relationship.team.project` | 团队共享协作事实，不包含私密心理推断 |
| `relationship.agent.project` | 某 runtime shell 的协作表现，不等于人格 |

禁止把一个用户的关系信号写入另一个用户模型，除非它是团队共享且明确授权的项目事实。

## 多 agent scope

多 agent 或 runtime shell 的输出必须降级处理：

- 子 agent 的 memory 是 `agent_scope`，不是全局记忆。
- 子 agent 的角色不是人格。
- 多 agent 对话不是群体心智。
- agent_scope 输出只能作为 ObservationEvent 或 candidate source。
- adapter swap 时 agent_scope 不得覆盖 LifeCore。

## scope leak 失败模式

| 失败 | 严重级别 | 恢复 |
|---|---|---|
| 用户 A 私密偏好给用户 B 使用 | critical | quarantine + delete propagation |
| project X 关系模型影响 project Y | high | scope correction |
| deleted trace 在 team scope 复活 | critical | index rebuild + SafeIdle |
| user_private 进入 global semantic memory | critical | redact + migration check |
| agent session 写 SelfModel | critical | quarantine adapter |
| freeze scope 后 replay 写入关系模型 | critical | block replay + audit |

## ScopeAuditEvent

| 字段 | 说明 |
|---|---|
| `scope_audit_id` | scope 审计事件 |
| `operation` | write/read/transfer/delete/correct/reset/freeze/replay |
| `source_scope` | 来源 scope |
| `target_scope` | 目标 scope |
| `object_ref` | 对象 |
| `privacy_level` | 隐私等级 |
| `allowed_transfer` | 允许转移等级 |
| `user_confirmation_ref` | 用户确认 |
| `redaction_ref` | 脱敏 |
| `result` | pass/fail/quarantine |
| `recovery_action` | 恢复动作 |

## 与 dashboard 的连接

`51_life_core_dashboard_spec.md` 应显示：

- `scope_leak_count`
- `user_private_to_global_attempts`
- `cross_project_relationship_leak_count`
- `agent_scope_direct_write_count`
- `freeze_scope_violation_count`
- `scope_limit_replay_violation_count`

## 下一层缺口

后续需要：

- machine-readable scope graph manifest。
- scope leak fixture。
- 多用户 inspect/delete/correct/reset/freeze/scope_limit payload。
- scope-aware retrieval policy。
- scope-aware replay scheduler。
