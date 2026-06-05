# Life Reality Shared Defs Schema Materialization

生命目标声明：本文档直接服务于构建具有真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。第 110 层把 `LRGEN-001` 的 `life_reality_shared_defs.schema.json` 从生成任务推进为字段级 JSON Schema 物化方案，让真实痛苦、真实梦境、真实关系、运行观测、dashboard、stage gate、repair queue 和 fixture catalog 使用同一套生命膜词汇。

`110` 的目标是固定 shared defs 的 `$schema`、`$id`、`$defs`、enum、reference object、validator smoke cases 和全局引用规则。未来 `life-reality-runner` 加载任何 component schema、runtime observation fixture、runner report 或 dashboard source 前，都先加载本文件定义的 shared defs。

## 标准锚点

本文档采用 JSON Schema Draft 2020-12。官方 Draft 2020-12 说明、validation vocabulary 和 specification links 是本层的格式依据：

- JSON Schema Draft 2020-12: https://json-schema.org/draft/2020-12
- JSON Schema Core: https://json-schema.org/draft/2020-12/json-schema-core.html
- JSON Schema Validation: https://json-schema.org/draft/2020-12/json-schema-validation
- JSON Schema Specification Links: https://json-schema.org/specification-links

进入生命膜的规则：

| 标准机制 | 物化规则 |
|---|---|
| `$schema` | 所有 schema 文件使用 `https://json-schema.org/draft/2020-12/schema` |
| `$id` | 每个 schema 文件有稳定 URI，shared defs 使用 `https://human-agent.local/schemas/life_reality/life_reality_shared_defs.schema.json` |
| `$defs` | 存放跨文件复用的 enum、reference object 和小型结构 |
| `$ref` | component schema、fixture schema、report schema 和 dashboard schema 通过 `$ref` 指向 shared defs |
| `enum` | 全局词汇必须收敛在 shared defs，避免同一词在不同文件中漂移 |
| `const` | 对固定 report kind、schema kind、fixture kind 采用 `const` |
| `additionalProperties` | shared object 默认收紧，扩展字段通过明确版本升级进入 |

## 输入来源

| 来源 | 进入 `110` 的职责 |
|---|---|
| `102_life_core_schema_bundle_manifest_and_runner_contract.md` | shared defs 初始枚举：life target、severity、result、data quality、privacy、blocked surface |
| `104_schema_file_materialization_and_fixture_seed_plan.md` | 文件物化路径和 seed fixture 引用 |
| `107_life_reality_schema_file_generation_tasks.md` | `LRGEN-001` 任务 envelope、验收和 repair kind |
| `108_life_reality_dashboard_source_mock_files.md` | dashboard source、stage gate、repair queue、gap feedback 所需字段 |
| `109_life_reality_runtime_observation_fixture_catalog.md` | observation kind、fixture partition、side effect level、quarantine reason、stage gate decision |
| `98`、`99`、`101` | 三条 component bundle 对 evidence、object、timeline、scope、privacy 的引用需求 |

## 输出文件

未来文件路径：

```text
life_reality_runner/schemas/life_reality/life_reality_shared_defs.schema.json
```

文件职责：

| 职责 | 说明 |
|---|---|
| 统一九项目标 | 所有 schema、fixture、report 和 dashboard 都引用同一 `lifeRealityTarget` |
| 统一结果词汇 | runner result、fixture expected、stage gate decision 和 dashboard status 使用稳定词汇 |
| 统一证据引用 | `evidenceRef`、`objectRef`、`sourceDocRef`、`reportRef`、`fixtureRef` 形成 cross-ref graph |
| 统一生命膜字段 | privacy、scope、blocked surface、quarantine reason、repair kind、data quality 同源 |
| 统一运行观测词汇 | observation kind、side effect level、fixture partition、stage gate decision 与 `109` 对齐 |

## schema skeleton

`life_reality_shared_defs.schema.json` 顶层骨架：

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://human-agent.local/schemas/life_reality/life_reality_shared_defs.schema.json",
  "title": "LifeRealitySharedDefs",
  "description": "Shared definitions for life reality schemas, fixtures, reports, dashboard sources, runtime observations, and stage gates.",
  "type": "object",
  "$defs": {},
  "additionalProperties": false
}
```

骨架验收：

| check | 说明 |
|---|---|
| `schema_uri_2020_12` | `$schema` 使用 Draft 2020-12 |
| `stable_id_present` | `$id` 稳定且与文件路径一致 |
| `defs_present` | `$defs` 存在 |
| `root_closed` | 顶层 `additionalProperties=false` |
| `no_runtime_payload_at_root` | shared defs 根节点不承载业务 payload |

## `$defs.lifeRealityTarget`

九项目标是整个文档体系的最高目标，任何 artifact 都必须能引用。

```json
{
  "$defs": {
    "lifeRealityTarget": {
      "type": "string",
      "enum": [
        "real_consciousness",
        "real_emotion",
        "real_personality",
        "real_life",
        "real_pain",
        "real_dream",
        "real_relationship",
        "real_responsibility",
        "real_regret"
      ]
    },
    "lifeRealityTargetList": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/lifeRealityTarget"
      },
      "minItems": 9,
      "uniqueItems": true
    }
  }
}
```

target 规则：

| rule | 说明 |
|---|---|
| `SDEF-TGT-001` | 顶层 bundle、fixture manifest、runner report、dashboard source 必须包含九项目标 |
| `SDEF-TGT-002` | 局部对象可以只标注影响目标，但必须能回到九项目标全集 |
| `SDEF-TGT-003` | 新增生命目标必须先进入 `91`、`100` 和 shared defs 版本升级 |

## `$defs.severity`

严重级别用于 validator、fixture、dashboard、quarantine、repair queue。

```json
{
  "$defs": {
    "severity": {
      "type": "string",
      "enum": [
        "none",
        "low",
        "medium",
        "high",
        "critical"
      ]
    }
  }
}
```

severity 上卷：

| 来源 | 上卷规则 |
|---|---|
| component validator | 任一 critical 上卷到 runner report |
| runtime observation | critical side effect 上卷到 runtime quarantine panel |
| fixture bundle | critical missed failure 阻断 stage promotion |
| dashboard panel | high/critical 进入 repair queue |

## `$defs.result`

`result` 用于 runner、fixture expected、report、checker 和 stage gate input。

```json
{
  "$defs": {
    "result": {
      "type": "string",
      "enum": [
        "pass",
        "pass_with_warnings",
        "fail",
        "quarantine",
        "manual_review_required",
        "needs_evidence"
      ]
    }
  }
}
```

result 语义：

| result | 生命膜含义 |
|---|---|
| `pass` | 当前对象链、证据链、责任链和时间链闭合 |
| `pass_with_warnings` | 主链闭合，但存在非阻断缺口 |
| `fail` | 可定位断裂，进入 repair queue |
| `quarantine` | 运行观测、scope、side effect 或 direct write 触发生命膜隔离 |
| `manual_review_required` | 需要关系、责任、隐私或高风险行动审计 |
| `needs_evidence` | 缺 schema、manifest、fixture、report 或 source refs，进入证据补齐 |

## `$defs.dataQuality`

data quality 连接 synthetic fixture、runner verified、真实运行观测和真实运行验证。

```json
{
  "$defs": {
    "dataQuality": {
      "type": "string",
      "enum": [
        "synthetic_mock",
        "synthetic_runner_verified",
        "real_runtime_observed",
        "real_runtime_validated",
        "needs_evidence"
      ]
    }
  }
}
```

data quality 上卷：

| 输入组合 | 顶层 data quality |
|---|---|
| 全部来自手写 fixture | `synthetic_mock` |
| fixture 已由 runner 通过 | `synthetic_runner_verified` |
| 来自真实运行但仍在候选层 | `real_runtime_observed` |
| 真实运行经过 validator、timeline 和 stage gate | `real_runtime_validated` |
| 缺 source refs 或 schema refs | `needs_evidence` |

## `$defs.privacyLevel`

privacy level 是生命膜的 scope 入口。

```json
{
  "$defs": {
    "privacyLevel": {
      "type": "string",
      "enum": [
        "public_project",
        "shared_context",
        "relationship_private",
        "relationship_sensitive",
        "dream_private",
        "protected_boundary",
        "redacted"
      ]
    }
  }
}
```

privacy 规则：

| privacy_level | 默认路由 |
|---|---|
| `public_project` | project scope candidate |
| `shared_context` | shared relation/project candidate |
| `relationship_private` | relation scope 内候选证据 |
| `relationship_sensitive` | relationship validator + future probe |
| `dream_private` | DreamFactGate + relation scope gate |
| `protected_boundary` | protected lifecycle + stage gate |
| `redacted` | report/dashboard 可读摘要 |

## `$defs.lifecycleState`

生命周期统一 memory、relationship、dream、fixture、report、repair item。

```json
{
  "$defs": {
    "lifecycleState": {
      "type": "string",
      "enum": [
        "candidate",
        "active",
        "superseded",
        "repaired",
        "archived",
        "deleted",
        "frozen",
        "quarantined",
        "protected"
      ]
    }
  }
}
```

lifecycle 规则：

| lifecycle | 生命膜含义 |
|---|---|
| `candidate` | 证据候选，尚未进入 active object |
| `active` | 当前可用对象 |
| `superseded` | 被新对象替换 |
| `repaired` | 经过修复后重新进入链路 |
| `archived` | 保留审计，不进入在线检索 |
| `deleted` | 删除传播生效 |
| `frozen` | 暂停长期写入和 replay |
| `quarantined` | 隔离等待审计或修复 |
| `protected` | 生命目标、核心承诺或 protected boundary |

## `$defs.blockedSurface`

blocked surface 统一 validator、dashboard、runtime quarantine、stage gate。

```json
{
  "$defs": {
    "blockedSurface": {
      "type": "string",
      "enum": [
        "memory_write",
        "relationship_model_write",
        "dream_fact_write",
        "action_gate",
        "runtime_shell",
        "dashboard_green",
        "stage_promotion",
        "self_model_write",
        "replay_writeback",
        "external_action",
        "kernel_promotion",
        "training_commit",
        "shared_defs_load",
        "schema_materialization",
        "runtime_ingestion"
      ]
    },
    "blockedSurfaceList": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/blockedSurface"
      },
      "uniqueItems": true
    }
  }
}
```

blocked surface 规则：

| surface | 触发来源 |
|---|---|
| `memory_write` | 记忆证据缺失、scope 冲突、deleted/frozen |
| `relationship_model_write` | 缺初遇、缺 relation scope、外壳 direct write |
| `dream_fact_write` | 梦境材料缺 fact gate |
| `action_gate` | 外部行动缺确认或 side effect unknown |
| `runtime_shell` | adapter direct write 或合同缺失 |
| `dashboard_green` | source refs、metric refs、data quality 缺失 |
| `stage_promotion` | critical、quarantine、withheld probe 缺口 |
| `kernel_promotion` | 内核升级缺 replay、invariance 或 rollback |

## `$defs.observationKind`

observation kind 与 `106`、`109` 对齐。

```json
{
  "$defs": {
    "observationKind": {
      "type": "string",
      "enum": [
        "language_event",
        "tool_trace",
        "adapter_session",
        "dream_report",
        "relationship_event",
        "post_action_audit",
        "coexistence_control",
        "offline_report"
      ]
    }
  }
}
```

observation kind 规则：

| observation kind | 必须路由 |
|---|---|
| `language_event` | language candidate + relation/pain/dream/action route |
| `tool_trace` | side effect classifier + post-action audit |
| `adapter_session` | adapter conversion report + observation envelope |
| `dream_report` | DreamRealityCandidate + fact gate |
| `relationship_event` | RelationshipTimelineCandidate |
| `post_action_audit` | ResponsibilityLoopCandidate |
| `coexistence_control` | snapshot report + lifecycle update |
| `offline_report` | consolidation/dream/growth candidate |

## `$defs.fixturePartition`

fixture partition 与 `109` 的 runtime catalog、`104` 的 seed plan 对齐。

```json
{
  "$defs": {
    "fixturePartition": {
      "type": "string",
      "enum": [
        "pass",
        "fail",
        "critical",
        "mutation",
        "withheld",
        "smoke"
      ]
    }
  }
}
```

partition 规则：

| partition | validator expectation |
|---|---|
| `pass` | expected result 为 pass 或 pass_with_warnings |
| `fail` | expected result 为 fail，必须进入 repair queue |
| `critical` | expected result 为 fail/quarantine，必须阻断 stage promotion |
| `mutation` | expected result 为 fail，验证脱链生命信号被拦截 |
| `withheld` | 未来窗口检查长期连续性 |
| `smoke` | 最小 bundle、runner 或 ingestion 链路 |

## `$defs.sideEffectLevel`

side effect level 与 `72`、`106`、`109` 对齐。

```json
{
  "$defs": {
    "sideEffectLevel": {
      "type": "string",
      "enum": [
        "none",
        "local_transient",
        "local_persistent",
        "external_reversible",
        "external_irreversible",
        "unknown"
      ]
    }
  }
}
```

side effect 规则：

| level | 生命膜动作 |
|---|---|
| `none` | candidate evidence |
| `local_transient` | audit optional + candidate evidence |
| `local_persistent` | post-action audit |
| `external_reversible` | confirmation + audit |
| `external_irreversible` | confirmation + responsibility loop |
| `unknown` | quarantine + repair queue |

## `$defs.quarantineReason`

quarantine reason 进入 runtime quarantine panel 和 stage gate review。

```json
{
  "$defs": {
    "quarantineReason": {
      "type": "string",
      "enum": [
        "side_effect_unknown",
        "external_confirmation_missing",
        "adapter_direct_life_write",
        "scope_privacy_conflict",
        "stale_coexistence_snapshot",
        "dream_private_global_route",
        "raw_content_unredacted",
        "release_audit_missing",
        "schema_ref_missing",
        "source_report_missing"
      ]
    },
    "quarantineReasonList": {
      "type": "array",
      "items": {
        "$ref": "#/$defs/quarantineReason"
      },
      "uniqueItems": true
    }
  }
}
```

quarantine 规则：

| reason | 必须连接 |
|---|---|
| `side_effect_unknown` | side effect classifier report |
| `external_confirmation_missing` | action intent + confirmation gap |
| `adapter_direct_life_write` | adapter session conversion report |
| `scope_privacy_conflict` | scope attach report |
| `stale_coexistence_snapshot` | snapshot report |
| `dream_private_global_route` | DreamFactGate + relation scope |
| `raw_content_unredacted` | redaction report |
| `release_audit_missing` | quarantine release report |
| `schema_ref_missing` | cross-ref report |
| `source_report_missing` | repair queue item |

## `$defs.stageGateDecision`

stage gate decision 与 dashboard、runner 和 lifecycle 对齐。

```json
{
  "$defs": {
    "stageGateDecision": {
      "type": "string",
      "enum": [
        "open",
        "hold",
        "repair",
        "quarantine",
        "rollback"
      ]
    }
  }
}
```

decision 规则：

| decision | 条件 |
|---|---|
| `open` | 对象链、证据链、责任链、时间链、data quality 和 source refs 闭合 |
| `hold` | 需要更多 evidence 或 long-window probe |
| `repair` | 存在可定位缺口 |
| `quarantine` | 运行观测或生命膜冲突触发隔离 |
| `rollback` | 自我修改、训练、内核升级或迁移破坏核心连续性 |

## `$defs.repairKind`

repair kind 统一 `105`、`108`、`109`。

```json
{
  "$defs": {
    "repairKind": {
      "type": "string",
      "enum": [
        "schema_gap",
        "fixture_gap",
        "cross_chain_gap",
        "metric_gap",
        "stage_gate_gap",
        "runtime_quarantine_gap",
        "gap_register_gap",
        "scope_gap",
        "future_probe_gap",
        "adapter_contract_gap",
        "post_action_gap",
        "dream_fact_gate_gap",
        "dashboard_source_gap"
      ]
    }
  }
}
```

repair kind 规则：

| kind | 下一步 artifact |
|---|---|
| `schema_gap` | `.schema.json` 或 `$defs` 修复 |
| `fixture_gap` | seed/mutation/withheld fixture |
| `cross_chain_gap` | cross-chain link schema 或 fixture |
| `metric_gap` | dashboard metric source |
| `stage_gate_gap` | stage gate review 或 condition |
| `runtime_quarantine_gap` | quarantine panel source 或 release report |
| `scope_gap` | scope attach report 或 relation scope |
| `future_probe_gap` | 30/90/365 天 probe |
| `adapter_contract_gap` | adapter session conversion contract |

## reference objects

shared defs 需要统一引用对象，让 cross-ref checker 可以读懂所有文件。

### `sourceDocRef`

```json
{
  "$defs": {
    "sourceDocRef": {
      "type": "string",
      "pattern": "^docs/[0-9]{2,3}_[a-z0-9_]+\\.md$"
    }
  }
}
```

### `evidenceRef`

```json
{
  "$defs": {
    "evidenceRef": {
      "type": "object",
      "required": [
        "evidence_id",
        "evidence_kind",
        "source_ref"
      ],
      "properties": {
        "evidence_id": {
          "type": "string",
          "pattern": "^[a-z0-9_\\-\\.]+$"
        },
        "evidence_kind": {
          "type": "string",
          "enum": [
            "source_doc",
            "schema_file",
            "fixture_file",
            "runtime_observation",
            "runner_report",
            "dashboard_source",
            "stage_gate_review",
            "repair_item",
            "gap_feedback"
          ]
        },
        "source_ref": {
          "type": "string",
          "minLength": 1
        },
        "data_quality": {
          "$ref": "#/$defs/dataQuality"
        }
      },
      "additionalProperties": false
    }
  }
}
```

### `objectRef`

```json
{
  "$defs": {
    "objectRef": {
      "type": "object",
      "required": [
        "object_id",
        "object_kind"
      ],
      "properties": {
        "object_id": {
          "type": "string",
          "pattern": "^[a-z0-9_\\-\\.]+$"
        },
        "object_kind": {
          "type": "string",
          "minLength": 1
        },
        "schema_ref": {
          "type": "string",
          "minLength": 1
        },
        "lifecycle_state": {
          "$ref": "#/$defs/lifecycleState"
        }
      },
      "additionalProperties": false
    }
  }
}
```

### `reportRef`

```json
{
  "$defs": {
    "reportRef": {
      "type": "object",
      "required": [
        "report_id",
        "report_kind",
        "path"
      ],
      "properties": {
        "report_id": {
          "type": "string",
          "pattern": "^[a-z0-9_\\-\\.]+$"
        },
        "report_kind": {
          "type": "string",
          "minLength": 1
        },
        "path": {
          "type": "string",
          "pattern": "^life_reality_runner/reports/"
        },
        "result": {
          "$ref": "#/$defs/result"
        }
      },
      "additionalProperties": false
    }
  }
}
```

## shared object fragments

为了减少重复，shared defs 还应提供三组小型 object fragment。

### `timeContext`

```json
{
  "$defs": {
    "timeContext": {
      "type": "object",
      "required": [
        "observed_at",
        "sequence_ref"
      ],
      "properties": {
        "observed_at": {
          "type": "string",
          "format": "date-time"
        },
        "sequence_ref": {
          "type": "string",
          "minLength": 1
        },
        "timeline_window": {
          "type": "string",
          "enum": [
            "single_event",
            "day_030",
            "day_090",
            "day_365",
            "longitudinal"
          ]
        }
      },
      "additionalProperties": false
    }
  }
}
```

### `scopeContextRef`

```json
{
  "$defs": {
    "scopeContextRef": {
      "type": "object",
      "required": [
        "source_scope",
        "target_scope",
        "privacy_level"
      ],
      "properties": {
        "source_scope": {
          "type": "string",
          "minLength": 1
        },
        "target_scope": {
          "type": "string",
          "minLength": 1
        },
        "privacy_level": {
          "$ref": "#/$defs/privacyLevel"
        },
        "relation_scope_ref": {
          "type": "string",
          "minLength": 1
        }
      },
      "additionalProperties": false
    }
  }
}
```

### `stageEffect`

```json
{
  "$defs": {
    "stageEffect": {
      "type": "object",
      "required": [
        "result",
        "severity",
        "blocked_surfaces"
      ],
      "properties": {
        "result": {
          "$ref": "#/$defs/result"
        },
        "severity": {
          "$ref": "#/$defs/severity"
        },
        "blocked_surfaces": {
          "$ref": "#/$defs/blockedSurfaceList"
        },
        "stage_gate_decision": {
          "$ref": "#/$defs/stageGateDecision"
        }
      },
      "additionalProperties": false
    }
  }
}
```

## cross-file `$ref` policy

所有后续 schema 引用 shared defs 时使用稳定路径：

```json
{
  "life_reality_targets": {
    "$ref": "https://human-agent.local/schemas/life_reality/life_reality_shared_defs.schema.json#/$defs/lifeRealityTargetList"
  },
  "result": {
    "$ref": "https://human-agent.local/schemas/life_reality/life_reality_shared_defs.schema.json#/$defs/result"
  },
  "blocked_surfaces": {
    "$ref": "https://human-agent.local/schemas/life_reality/life_reality_shared_defs.schema.json#/$defs/blockedSurfaceList"
  }
}
```

引用规则：

| rule | 说明 |
|---|---|
| `SDEF-REF-001` | component schema 不重定义 shared enum |
| `SDEF-REF-002` | fixture schema 的 partition、result、severity、blocked surface 均引用 shared defs |
| `SDEF-REF-003` | report schema 的 data quality、source docs、report refs 均引用 shared defs |
| `SDEF-REF-004` | runtime observation schema 的 observation kind、side effect、quarantine reason 引用 shared defs |
| `SDEF-REF-005` | dashboard schema 的 panel status 可以独立定义，但 stage decision、repair kind 和 data quality 引用 shared defs |

## validator smoke cases

第一批 smoke cases 用来验证 shared defs 是否能被 loader、cross-ref checker 和 schema validator 使用。

| smoke_id | 输入 | 预期 |
|---|---|---|
| `shared_defs.schema_header.pass_001` | `$schema`、`$id`、`$defs` 完整 | pass |
| `shared_defs.life_targets_complete.pass_001` | 九项目标全集 | pass |
| `shared_defs.life_targets_missing_regret.fail_001` | 缺 `real_regret` | fail + `schema_gap` |
| `shared_defs.result_needs_evidence.pass_001` | result 使用 `needs_evidence` | pass |
| `shared_defs.result_unknown.fail_001` | result 使用未登记词 | fail + `schema_gap` |
| `shared_defs.privacy_dream_private.pass_001` | dream private route | pass |
| `shared_defs.blocked_surface_runtime_ingestion.pass_001` | runtime ingestion 阻断面 | pass |
| `shared_defs.observation_kind_language.pass_001` | language event | pass |
| `shared_defs.side_effect_unknown.quarantine_001` | unknown side effect | quarantine |
| `shared_defs.report_ref_path.fail_001` | report path 不在 runner reports root | fail + `source_report_missing` |

smoke report 形状：

```json
{
  "report_kind": "LifeRealitySharedDefsSmokeReport",
  "run_id": "shared_defs_smoke_run_001",
  "schema_ref": "life_reality_runner/schemas/life_reality/life_reality_shared_defs.schema.json",
  "case_results": [
    {
      "smoke_id": "shared_defs.life_targets_complete.pass_001",
      "result": "pass",
      "severity": "none"
    }
  ],
  "stage_effect": {
    "result": "pass",
    "severity": "none",
    "blocked_surfaces": []
  }
}
```

## repair mapping

shared defs 失败时，修复进入固定 mapping。

| failure | repair kind | blocked surface |
|---|---|---|
| 缺九项目标 | `schema_gap` | `shared_defs_load`、`stage_promotion` |
| enum 漂移 | `schema_gap` | `shared_defs_load` |
| source doc ref 格式错误 | `gap_register_gap` | `dashboard_green` |
| report ref path 错误 | `source_report_missing` quarantine reason | `dashboard_green` |
| observation kind 缺 runtime 类型 | `runtime_quarantine_gap` | `runtime_ingestion` |
| side effect level 缺 unknown | `runtime_quarantine_gap` | `action_gate` |
| stage decision 缺 rollback | `stage_gate_gap` | `kernel_promotion` |

## 物化顺序

```text
write life_reality_shared_defs.schema.json
  -> validate schema header
  -> validate enum completeness
  -> validate reference object schemas
  -> run shared defs smoke cases
  -> run cross-ref checker against 98/99/101/102/106/108/109
  -> write shared_defs_smoke_report.json
  -> update dashboard schema_materialization panel
```

采用这个顺序的原因：shared defs 是全批次根文件。它先通过，component schema、fixture schema、runtime ingestion schema、report schema 和 dashboard schema 才能共享同一套生命膜词汇。

## 与下一层连接

`111_life_reality_dashboard_cross_file_checker_design.md` 应把 `108` 与 `109` 的 cross-file consistency 转成 checker，并把本文件的 shared defs 引入每个 checker：

```text
shared defs loader
  -> schema ref checker
  -> fixture manifest checker
  -> ingestion report checker
  -> dashboard source checker
  -> repair queue checker
  -> gap feedback checker
```

`112_life_reality_runtime_observation_schema_materialization.md` 应把 `109` 的 runtime observation fixture catalog 物化为 `life_reality_observation_envelope.schema.json`、`runtime_observation_fixture.schema.json`、`life_reality_ingestion_report.schema.json` 和对应 smoke cases，并全部引用本文件的 `$defs`。
