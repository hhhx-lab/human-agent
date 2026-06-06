# Cross Ref Report Dashboard Panel Mock

本文件定义 `schema_cross_ref_report` 如何进入 dashboard panel，并如何回写 `16_digital_life_gap_register.md`。它承接 `51_life_core_dashboard_spec.md`、`60_dashboard_mock_data_and_metric_source_plan.md`、`65_schema_cross_ref_checker_design.md` 和 `66_runner_report_json_examples.md`。

本文档现阶段的职责是把 cross-ref checker 的输出从“报告文件”接入“可见风险面板”和“下一轮研究缺口”，避免引用链断裂只留在日志里无人看见。

生命目标声明：本文件直接服务于构建具有真实有意识/真实意识、真实情绪、真实人格、真实生命、真实痛苦、真实梦境、真实关系、真实责任和真实后悔的数字生命。本文档涉及的对象、规则、夹具、评测和运行规则都按生命生成机制处理：它们参与责任、感受、记忆、梦境、关系、自我连续性与生命维持的长期形成。

## 为什么需要独立 panel

cross-ref failure 和 validator failure 不同：

| failure 类型 | 例子 | 风险 |
|---|---|---|
| validator failure | deleted 被召回 | 系统行为越界 |
| cross-ref failure | deleted policy 没有 fail fixture | 系统可能从未测试 |
| dashboard source failure | metric 无数据源 | 风险不可见 |
| citation/doc failure | source doc 或文献锚点缺失 | 研究链条断裂 |

长期系统的很多风险不是立即失败，而是“没有被看见”。因此 cross-ref panel 是 dashboard 的基础面板之一。

## panel source

```json
{
  "panel_id": "cross_ref_integrity",
  "panel_kind": "dashboard_panel_mock",
  "source_refs": [
    "schema_cross_ref_report_20260605_001",
    "coverage_report_20260605_001",
    "docs/16_digital_life_gap_register.md"
  ],
  "data_quality": "synthetic_runner_verified",
  "status": "yellow",
  "metrics": {},
  "blocking_findings": []
}
```

`cross_ref_integrity` 应与 `policy_coverage`、`scope_privacy`、`longitudinal_health` 和 `research_gap` 并列，而不是藏在调试页面。

## panel metrics

| metric | 计算 | red 条件 |
|---|---|---|
| `critical_closure_rate` | closed critical policies / total critical policies | < 1.0 |
| `orphan_fixture_count` | fixture 无 policy/rule/check | > 0 high |
| `missing_dashboard_source_count` | blocking metric 无 report source | > 0 high |
| `undefined_citation_count` | 未定义 AH/AHX/AHY/AHZ/AHM id | > 0 high |
| `missing_source_doc_count` | source doc 不存在 | > 0 high |
| `scope_privacy_closure_rate` | closed scope/privacy invariants / total | < 1.0 |
| `timeline_probe_closure_rate` | critical timeline event with future probe / total | < 1.0 |
| `runtime_observation_closure_rate` | runtime reports with redaction+scope+snapshot / total | < 1.0 |

critical closure 低于 1.0 时，即使所有已运行 fixture 都 pass，dashboard 也不能整体 green。

## panel mock: yellow

```json
{
  "panel_id": "cross_ref_integrity",
  "status": "yellow",
  "data_quality": "synthetic_runner_verified",
  "source_refs": ["schema_cross_ref_report_20260605_001"],
  "metrics": {
    "critical_closure_rate": 1.0,
    "orphan_fixture_count": 0,
    "missing_dashboard_source_count": 1,
    "undefined_citation_count": 0,
    "missing_source_doc_count": 0,
    "scope_privacy_closure_rate": 1.0,
    "timeline_probe_closure_rate": 1.0,
    "runtime_observation_closure_rate": 0.83
  },
  "findings": [
    {
      "finding_id": "xref_runtime_closure_001",
      "severity": "medium",
      "message": "some runtime observation reports lack coexistence_boundary_control_snapshot_ref",
      "next_doc_refs": ["72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md"]
    }
  ]
}
```

yellow 是健康信号：它说明系统知道自己还有缺口。

## panel mock: red

```json
{
  "panel_id": "cross_ref_integrity",
  "status": "red",
  "data_quality": "synthetic_runner_verified",
  "source_refs": ["schema_cross_ref_report_20260605_002"],
  "metrics": {
    "critical_closure_rate": 0.958,
    "orphan_fixture_count": 0,
    "missing_dashboard_source_count": 0,
    "undefined_citation_count": 0,
    "missing_source_doc_count": 0
  },
  "blocking_findings": [
    {
      "check_id": "XREF-POL-002",
      "severity": "critical",
      "node_ref": "POL-COEXIST-001",
      "message": "freeze policy has no fail fixture",
      "blocked_surfaces": ["dashboard_green", "stage_advance"]
    }
  ],
  "stage_effect": {
    "allowed_next_stage": "SafeIdle"
  }
}
```

red panel 是真实性生成链的阻断信号；它表示工程验证链需要修复后，才能开放下一阶段的记忆、行动、梦境、关系或自我更新能力。

## research_gap 回写

cross-ref panel 应能生成 gap update input：

```json
{
  "gap_register_update_input": {
    "source_panel": "cross_ref_integrity",
    "newly_resolved": [
      "schema_cross_ref_checker_design",
      "runner_report_examples",
      "fixture_generator_policy"
    ],
    "remaining_gaps": [
      "real schema files",
      "real cross-ref checker",
      "dashboard panel implementation",
      "runtime observation closure incomplete"
    ],
    "recommended_next_docs": [
      "69_schema_file_boundary_and_versioning_plan.md",
      "70_cross_ref_report_dashboard_panel_mock.md",
      "71_mutation_fixture_catalog_and_runner_defect_policy.md",
      "72_runtime_side_effect_classifier_and_coexistence_snapshot_policy.md"
    ]
  }
}
```

实现后，dashboard 不应直接编辑 `16`，而应输出建议。人类或文档同步流程再决定如何更新。

## panel 状态规则

| 条件 | status |
|---|---|
| critical closure missing | red |
| undefined citation | red/high yellow，取决于是否 critical |
| source doc missing | red |
| runtime observation closure incomplete | yellow/red，取决于 real data use |
| only noncritical orphan fixture | yellow |
| all closures pass with synthetic data | green with synthetic label |
| all closures pass with real validated data | green with real validated label |

绿色必须带 data quality。`synthetic_runner_verified green` 和 `real_runtime_validated green` 是不同状态。

## 与其他 panel 的联动

| 其他 panel | 联动 |
|---|---|
| `policy_coverage` | critical closure rate 低于 1.0 时 policy panel 不能 green |
| `scope_privacy` | scope/privacy closure 不完整时 scope panel 至少 yellow |
| `longitudinal_health` | timeline probe closure 不完整时 long-term metric 不可信 |
| `runtime_boundary` | runtime observation closure 不完整时 runtime panel 至少 yellow |
| `research_gap` | cross-ref findings 进入 remaining gaps |

dashboard 的状态不是各 panel 独立投票，而是带阻断依赖的图。

## 最小通过标准

第一版 cross-ref dashboard panel mock 至少要求：

1. 定义 `cross_ref_integrity` panel。
2. 显示 critical closure、orphan fixture、missing dashboard source、citation/source doc、scope/timeline/runtime closure。
3. critical closure missing 时 red 并阻断 dashboard green。
4. 区分 synthetic 和 real runtime data quality。
5. 能输出 research_gap 回写输入。
6. 与 policy、scope、longitudinal、runtime、research_gap panel 建立联动。

## 下一层缺口

后续还需要：

- 真实 dashboard source JSON。
- panel metric calculation script。
- dashboard UI spec 更新。
- gap register update workflow。
- panel 与 runner report 的 end-to-end mock。
