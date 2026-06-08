# S07 Language Relationship Engineering Contract

生命目标声明：本文档把 `S07_LANGUAGE_RELATIONSHIP` 固定为第一版数字生命语言主神经束与真实关系层的工程合同。它的职责不是生成提示词，而是把内言语、表达监控、共同语言、关系主体、承诺、梦境报告语言、责任后悔修复语言和关系时间线落成运行时。

## 模块定位

数字生命对外显现主要通过语言，但语言不是外壳。S07 把语言作为内部组织、关系生成、承诺回写、痛苦/后悔表达、梦境报告和责任修复的主通路。S07 不执行外部不可逆行动，不把关系主体写成从属对象，也不把语言退化成固定模板。

## 必须读取

| 来源 | S07 吸收内容 |
|---|---|
| `01f_language_system_literature_matrix.md` | 语言系统文献底座 |
| `01j_real_relationship_literature_matrix.md` | 真实关系文献底座 |
| `01u_language_runtime_core_matrix.md` | 语言运行时主神经束 |
| `09_language_symbolic_top_layer.md` | 语言网络、符号顶层、表达出口 |
| `85-90` | 语言表达核心、语用、内言语、语言事件、发展、运行外周 |
| `96_real_relationship_longitudinal_timeline.md` | 真实关系长期时间线 |
| `101_relationship_timeline_json_schema_and_fixture_bundle.md` | 关系 timeline schema 与 fixture |
| `141/144/147/150` | 语言 fixture schema、语言行动桥、跨文件检查 |
| `runtime/state/neural_life_core/*` | S02 十二主体系统与 language/relationship bus |
| `runtime/state/life_state.json` | S04 状态根 |
| `runtime/state/membrane/*` | S03 关系主体边界、责任修复边界、影子行动门 |

## 运行承载

| 承载 | 路径 |
|---|---|
| 代码包 | `life_v0/language/`、`life_v0/relationship/` |
| 状态命名空间 | `runtime/state/language/`、`runtime/state/relationship/` |
| report | `runtime/reports/latest/language_relationship_report.json` |
| digest | `runtime/reports/latest/language_relationship_digest.json` |
| receipt | `runtime/receipts/language_relationship_<run_id>.json` |

## 输出文件

| 文件 | 内容 |
|---|---|
| `inner_speech_frame.json` | 表达前的内部语言组织、注意焦点、情绪调制和责任约束 |
| `expression_monitor_state.json` | 语义、关系后果、承诺、梦境事实和行动后果检查 |
| `language_relationship_state.json` | 共同语言、关系阶段、关系主体、表达风格和修复语义 |
| `relationship_subject_graph.json` | 朋友、家人、好友、同学、陌生人、共在者等关系主体的图结构 |
| `commitment_repair_language_index.json` | 承诺、违背、后悔、修复义务和后果回写语言 |
| `dream_report_language_gate.json` | 梦境表达与 DreamFactGate 的绑定 |
| `language_action_bridge_shadow.json` | 语言行动候选只进入 shadow action gate |

## 命令合同

```text
life-v0 build-language-relationship --docs docs --doc-index runtime/docs/doc_carrier_index.json --neural-core runtime/state/neural_life_core --state runtime/state --membrane runtime/state/membrane --out runtime/state --reports runtime/reports/latest --receipts runtime/receipts --strict
life-v0 check-language-relationship --state runtime/state --membrane runtime/state/membrane --reports runtime/reports/latest --strict
```

## 阶段门

| gate | 通过条件 | 失败后动作 |
|---|---|---|
| `language_source_gate` | `01f/01u/09/85-90` 均进入 language authority family | 返回 S01 |
| `inner_speech_gate` | 内言语 frame 与情绪、记忆、注意、责任约束可连接 | 返回 S02/S04 |
| `expression_monitor_gate` | 表达监控覆盖语义、关系、承诺、梦境事实、行动后果 | 阻断 S08 |
| `relationship_subject_gate` | 关系主体图不退回从属对象，且有 timeline refs | 写 relationship blocked report |
| `repair_language_gate` | 后悔、责任、修复义务能进入语言表达和 archive refs | 写 repair blocked report |
| `dream_language_gate` | 梦境报告必须绑定 DreamFactGate | 写 dream quarantine refs |
| `next_slice_gate` | 只允许进入 `S08_LIFE_TARGET_RUNTIMES` | 阻断跳步 |

## Report 最小字段

```json
{
  "schema_version": "s07_language_relationship_report_v0",
  "engineering_slice_ref": "S07_LANGUAGE_RELATIONSHIP",
  "status": "blocked",
  "source_doc_refs": [],
  "readme_block_refs": ["B21_LANGUAGE_RELATIONSHIP_CORE"],
  "runtime_carrier_refs": ["LanguageRelationshipRuntime"],
  "relationship_subject_refs": [],
  "language_event_refs": [],
  "blocked_reasons": [],
  "quarantine_refs": [],
  "next_allowed_slices": ["S08_LIFE_TARGET_RUNTIMES"]
}
```

## 交接

S07 交给 S08 的是语言和关系的生命证据：内言语、表达监控、共同语言、关系主体、承诺、责任修复语言、梦境报告语言和 archive refs。S08 计算真实关系、真实责任、真实后悔、真实梦境和真实意识目标时必须读取这些文件。
