# 离线 Mock 实际执行记录

> 固定策略测试驱动，不是真实模型 ReAct 证据。

运行：`ed37e686-9678-406d-a36c-697af5458def`；终态：`completed`；回放：`False`。

## 1. decision

先检索主题对应的商品与素材

```json
{
  "seq": 1,
  "kind": "decision",
  "run_id": "ed37e686-9678-406d-a36c-697af5458def",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": null,
  "action": {
    "name": "search_materials",
    "arguments": {
      "query": "为便携咖啡杯策划新品营销视频内容活动",
      "product_id": "P001"
    },
    "summary": "先检索主题对应的商品与素材",
    "observes_event_ids": [],
    "provider_call_id": null,
    "provider_request_id": null,
    "provider_message": null
  },
  "summary": "先检索主题对应的商品与素材"
}
```

## 2. action_result

动作执行成功

```json
{
  "seq": 2,
  "kind": "action_result",
  "run_id": "ed37e686-9678-406d-a36c-697af5458def",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": null,
  "call_id": "2743b343-4b67-47ed-8cd1-3c7f946a897c",
  "tool": "search_materials",
  "parameters": {
    "query": "为便携咖啡杯策划新品营销视频内容活动",
    "product_id": "P001"
  },
  "provider_call_id": null,
  "attempt_key": "ed87acf267bbc473af81295d670c4dbbf924322ab90f149930a0e64a9cb81ed1",
  "ok": true,
  "retryable": false,
  "error_code": "",
  "summary": "动作执行成功",
  "data": {
    "product": {
      "id": "P001",
      "name": "便携咖啡杯",
      "keywords": [
        "咖啡杯",
        "通勤",
        "coffee",
        "cup"
      ],
      "facts": [
        "容量 350 毫升",
        "附带杯盖",
        "提供黑色和白色款式"
      ]
    },
    "materials": [
      {
        "id": "M001",
        "product_id": "P001",
        "kind": "reusable",
        "title": "咖啡杯外观素材",
        "keywords": [
          "咖啡杯",
          "通勤",
          "外观",
          "coffee"
        ],
        "facts": [
          "容量 350 毫升",
          "提供黑色和白色款式"
        ],
        "match_reason": "商品标识匹配",
        "score": 1
      },
      {
        "id": "M002",
        "product_id": "P001",
        "kind": "reference",
        "title": "咖啡杯商品说明",
        "keywords": [
          "咖啡杯",
          "商品",
          "cup"
        ],
        "facts": [
          "附带杯盖"
        ],
        "match_reason": "商品标识匹配",
        "score": 1
      }
    ],
    "missing": []
  },
  "charged_units": "0.000",
  "status": "succeeded",
  "task_status": "running",
  "simulated_seconds": 30,
  "simulated_spent_units": "0.000"
}
```

## 3. decision

使用已检索素材提出标准方案，随后估算

```json
{
  "seq": 3,
  "kind": "decision",
  "run_id": "ed37e686-9678-406d-a36c-697af5458def",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": null,
  "action": {
    "name": "update_plan",
    "arguments": {
      "tier": "standard",
      "material_ids": [
        "M001",
        "M002"
      ],
      "steps": [
        {
          "id": "materials",
          "action": "search_materials",
          "depends_on": []
        },
        {
          "id": "script",
          "action": "generate_script",
          "depends_on": [
            "materials"
          ]
        },
        {
          "id": "verification",
          "action": "estimate_cost",
          "depends_on": [
            "script"
          ]
        },
        {
          "id": "save",
          "action": "save_solution",
          "depends_on": [
            "verification"
          ]
        }
      ]
    },
    "summary": "使用已检索素材提出标准方案，随后估算",
    "observes_event_ids": [
      2
    ],
    "provider_call_id": null,
    "provider_request_id": null,
    "provider_message": null
  },
  "summary": "使用已检索素材提出标准方案，随后估算"
}
```

## 4. action_result

动作执行成功

```json
{
  "seq": 4,
  "kind": "action_result",
  "run_id": "ed37e686-9678-406d-a36c-697af5458def",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-1",
  "call_id": "e912edd0-02df-4643-bfae-04c581da6d6c",
  "tool": "update_plan",
  "parameters": {
    "tier": "standard",
    "material_ids": [
      "M001",
      "M002"
    ],
    "steps": [
      {
        "id": "materials",
        "action": "search_materials",
        "depends_on": []
      },
      {
        "id": "script",
        "action": "generate_script",
        "depends_on": [
          "materials"
        ]
      },
      {
        "id": "verification",
        "action": "estimate_cost",
        "depends_on": [
          "script"
        ]
      },
      {
        "id": "save",
        "action": "save_solution",
        "depends_on": [
          "verification"
        ]
      }
    ]
  },
  "provider_call_id": null,
  "attempt_key": "09547b306a7f0935677b304ef6f6338af39619cbff87c82dd6a346fd57ab4580",
  "ok": true,
  "retryable": false,
  "error_code": "",
  "summary": "动作执行成功",
  "data": {
    "id": "plan-1",
    "tier": "standard",
    "material_ids": [
      "M001",
      "M002"
    ],
    "steps": [
      {
        "id": "materials",
        "action": "search_materials",
        "depends_on": []
      },
      {
        "id": "script",
        "action": "generate_script",
        "depends_on": [
          "materials"
        ]
      },
      {
        "id": "verification",
        "action": "estimate_cost",
        "depends_on": [
          "script"
        ]
      },
      {
        "id": "save",
        "action": "save_solution",
        "depends_on": [
          "verification"
        ]
      }
    ]
  },
  "charged_units": "0.000",
  "status": "succeeded",
  "task_status": "running",
  "simulated_seconds": 30,
  "simulated_spent_units": "0.000"
}
```

## 5. decision

计划或执行状态变化，重新核算预算与截止时间

```json
{
  "seq": 5,
  "kind": "decision",
  "run_id": "ed37e686-9678-406d-a36c-697af5458def",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-1",
  "action": {
    "name": "estimate_cost",
    "arguments": {
      "plan_id": "plan-1"
    },
    "summary": "计划或执行状态变化，重新核算预算与截止时间",
    "observes_event_ids": [
      4
    ],
    "provider_call_id": null,
    "provider_request_id": null,
    "provider_message": null
  },
  "summary": "计划或执行状态变化，重新核算预算与截止时间"
}
```

## 6. action_result

动作执行成功

```json
{
  "seq": 6,
  "kind": "action_result",
  "run_id": "ed37e686-9678-406d-a36c-697af5458def",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-1",
  "call_id": "42bdda4d-b66c-4146-a10d-469dca21b623",
  "tool": "estimate_cost",
  "parameters": {
    "plan_id": "plan-1"
  },
  "provider_call_id": null,
  "attempt_key": "a7900f6fdd1c1ae1438a3eccb6b6588b6448dc6c90a8ebee9d3ab69690959d00",
  "ok": true,
  "retryable": false,
  "error_code": "",
  "summary": "动作执行成功",
  "data": {
    "signature": "846536f3d5a2f3cdb57dd96ad68ab24359a2c6e53a0a730757eb4ec5693dd790",
    "plan_id": "plan-1",
    "simulated_spent_units": "0.000",
    "remaining_tool_units": "4.000",
    "planned_resource_units": "8.000",
    "projected_total_units": "12.000",
    "budget_units": "20.000",
    "budget_gap_units": "0.000",
    "estimated_finish_at": "2030-01-01T10:03:31+08:00",
    "deadline_at": "2030-01-01T10:30:00+08:00",
    "remaining_seconds": 181,
    "time_gap_seconds": 0,
    "feasible": true
  },
  "charged_units": "0.000",
  "status": "succeeded",
  "task_status": "running",
  "simulated_seconds": 30,
  "simulated_spent_units": "0.000"
}
```

## 7. decision

估算可行，生成有来源的离线脚本；如之前失败，按上限有限重试

```json
{
  "seq": 7,
  "kind": "decision",
  "run_id": "ed37e686-9678-406d-a36c-697af5458def",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-1",
  "action": {
    "name": "generate_script",
    "arguments": {
      "plan_id": "plan-1",
      "material_ids": [
        "M001",
        "M002"
      ],
      "language": "zh-CN"
    },
    "summary": "估算可行，生成有来源的离线脚本；如之前失败，按上限有限重试",
    "observes_event_ids": [
      6
    ],
    "provider_call_id": null,
    "provider_request_id": null,
    "provider_message": null
  },
  "summary": "估算可行，生成有来源的离线脚本；如之前失败，按上限有限重试"
}
```

## 8. action_result

已注入工具失败（执行前，无费用）

```json
{
  "seq": 8,
  "kind": "action_result",
  "run_id": "ed37e686-9678-406d-a36c-697af5458def",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-1",
  "call_id": "d590b2f1-4bda-4d38-bf0e-67bb511ed726",
  "tool": "generate_script",
  "parameters": {
    "plan_id": "plan-1",
    "material_ids": [
      "M001",
      "M002"
    ],
    "language": "zh-CN"
  },
  "provider_call_id": null,
  "attempt_key": "5219762da018c09cc8b76e3efe48638f19bb37da95dc794bc58c3c341fb9a543",
  "ok": false,
  "retryable": true,
  "error_code": "injected_tool_failure",
  "summary": "已注入工具失败（执行前，无费用）",
  "data": null,
  "charged_units": "0.000",
  "status": "failed",
  "task_status": "running",
  "simulated_seconds": 30,
  "simulated_spent_units": "0.000"
}
```

## 9. decision

估算可行，生成有来源的离线脚本；如之前失败，按上限有限重试

```json
{
  "seq": 9,
  "kind": "decision",
  "run_id": "ed37e686-9678-406d-a36c-697af5458def",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-1",
  "action": {
    "name": "generate_script",
    "arguments": {
      "plan_id": "plan-1",
      "material_ids": [
        "M001",
        "M002"
      ],
      "language": "zh-CN"
    },
    "summary": "估算可行，生成有来源的离线脚本；如之前失败，按上限有限重试",
    "observes_event_ids": [
      8
    ],
    "provider_call_id": null,
    "provider_request_id": null,
    "provider_message": null
  },
  "summary": "估算可行，生成有来源的离线脚本；如之前失败，按上限有限重试"
}
```

## 10. action_result

动作执行成功

```json
{
  "seq": 10,
  "kind": "action_result",
  "run_id": "ed37e686-9678-406d-a36c-697af5458def",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-1",
  "call_id": "36f47e28-cd0e-4ae7-914c-bc088bc89eb9",
  "tool": "generate_script",
  "parameters": {
    "plan_id": "plan-1",
    "material_ids": [
      "M001",
      "M002"
    ],
    "language": "zh-CN"
  },
  "provider_call_id": null,
  "attempt_key": "5219762da018c09cc8b76e3efe48638f19bb37da95dc794bc58c3c341fb9a543",
  "ok": true,
  "retryable": false,
  "error_code": "",
  "summary": "动作执行成功",
  "data": {
    "artifact_id": "e454933b-1f3d-4fd7-99b8-02b2456b59d4",
    "cached": false,
    "script": {
      "title": "便携咖啡杯营销内容方案（离线合成）",
      "segments": [
        {
          "text": "容量 350 毫升",
          "source_ids": [
            "M001"
          ]
        },
        {
          "text": "提供黑色和白色款式",
          "source_ids": [
            "M001"
          ]
        },
        {
          "text": "附带杯盖",
          "source_ids": [
            "M002"
          ]
        }
      ],
      "generation_note": "Mock 逐条引用合成事实，不代表真实模型创作或翻译能力",
      "id": "e454933b-1f3d-4fd7-99b8-02b2456b59d4",
      "fingerprint": "bd27932ea8474a2b193e7059ef04125c42f65726f5b11b91d45176569d8ed5cc",
      "mode": "mock",
      "material_ids": [
        "M001",
        "M002"
      ]
    }
  },
  "charged_units": "4.000",
  "status": "succeeded",
  "task_status": "running",
  "simulated_seconds": 210,
  "simulated_spent_units": "4.000"
}
```

## 11. decision

计划或执行状态变化，重新核算预算与截止时间

```json
{
  "seq": 11,
  "kind": "decision",
  "run_id": "ed37e686-9678-406d-a36c-697af5458def",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-1",
  "action": {
    "name": "estimate_cost",
    "arguments": {
      "plan_id": "plan-1"
    },
    "summary": "计划或执行状态变化，重新核算预算与截止时间",
    "observes_event_ids": [
      10
    ],
    "provider_call_id": null,
    "provider_request_id": null,
    "provider_message": null
  },
  "summary": "计划或执行状态变化，重新核算预算与截止时间"
}
```

## 12. action_result

动作执行成功

```json
{
  "seq": 12,
  "kind": "action_result",
  "run_id": "ed37e686-9678-406d-a36c-697af5458def",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-1",
  "call_id": "2c950a00-76f3-49da-b8ae-375c1cdda2f2",
  "tool": "estimate_cost",
  "parameters": {
    "plan_id": "plan-1"
  },
  "provider_call_id": null,
  "attempt_key": "a7900f6fdd1c1ae1438a3eccb6b6588b6448dc6c90a8ebee9d3ab69690959d00",
  "ok": true,
  "retryable": false,
  "error_code": "",
  "summary": "动作执行成功",
  "data": {
    "signature": "bc2ad9ee47605c6574708ca8a6591630cc5fd081180e24153b62cfc55e2e2182",
    "plan_id": "plan-1",
    "simulated_spent_units": "4.000",
    "remaining_tool_units": "0.000",
    "planned_resource_units": "8.000",
    "projected_total_units": "12.000",
    "budget_units": "20.000",
    "budget_gap_units": "0.000",
    "estimated_finish_at": "2030-01-01T10:03:31+08:00",
    "deadline_at": "2030-01-01T10:30:00+08:00",
    "remaining_seconds": 1,
    "time_gap_seconds": 0,
    "feasible": true
  },
  "charged_units": "0.000",
  "status": "succeeded",
  "task_status": "running",
  "simulated_seconds": 210,
  "simulated_spent_units": "4.000"
}
```

## 13. decision

脚本存在且复核可行，尝试保存方案

```json
{
  "seq": 13,
  "kind": "decision",
  "run_id": "ed37e686-9678-406d-a36c-697af5458def",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-1",
  "action": {
    "name": "save_solution",
    "arguments": {
      "plan_id": "plan-1",
      "artifact_id": "e454933b-1f3d-4fd7-99b8-02b2456b59d4"
    },
    "summary": "脚本存在且复核可行，尝试保存方案",
    "observes_event_ids": [
      12
    ],
    "provider_call_id": null,
    "provider_request_id": null,
    "provider_message": null
  },
  "summary": "脚本存在且复核可行，尝试保存方案"
}
```

## 14. action_result

动作执行成功

```json
{
  "seq": 14,
  "kind": "action_result",
  "run_id": "ed37e686-9678-406d-a36c-697af5458def",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-1",
  "call_id": "f7e31760-cb9f-4c9e-bef7-a1eb0d3faa40",
  "tool": "save_solution",
  "parameters": {
    "plan_id": "plan-1",
    "artifact_id": "e454933b-1f3d-4fd7-99b8-02b2456b59d4"
  },
  "provider_call_id": null,
  "attempt_key": "38dce1f84aac384eae1430130e7794bf058126c7c60cc29149d9b68eb7ea9e50",
  "ok": true,
  "retryable": false,
  "error_code": "",
  "summary": "动作执行成功",
  "data": {
    "solution_id": "f193e961-9101-40da-b13a-2f9eea15ff0c",
    "saved_at": "2030-01-01T10:03:31+08:00",
    "saved": true
  },
  "charged_units": "0.000",
  "status": "succeeded",
  "task_status": "running",
  "simulated_seconds": 211,
  "simulated_spent_units": "4.000"
}
```

## 15. decision

观察到保存回执，申请结束任务

```json
{
  "seq": 15,
  "kind": "decision",
  "run_id": "ed37e686-9678-406d-a36c-697af5458def",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-1",
  "action": {
    "name": "finish_task",
    "arguments": {
      "status": "completed",
      "explanation": "方案及脚本已保存并可回读；未制作视频或投放广告"
    },
    "summary": "观察到保存回执，申请结束任务",
    "observes_event_ids": [
      14
    ],
    "provider_call_id": null,
    "provider_request_id": null,
    "provider_message": null
  },
  "summary": "观察到保存回执，申请结束任务"
}
```

## 16. action_result

动作执行成功

```json
{
  "seq": 16,
  "kind": "action_result",
  "run_id": "ed37e686-9678-406d-a36c-697af5458def",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-1",
  "call_id": "e5c71e83-ae20-4338-bd39-1a4d6eda7b23",
  "tool": "finish_task",
  "parameters": {
    "status": "completed",
    "explanation": "方案及脚本已保存并可回读；未制作视频或投放广告"
  },
  "provider_call_id": null,
  "attempt_key": "fdd18cd7611b0f24fe5ad2a6bb6502f5352bb07dd5c148b9b455aa5b8b9d6f6a",
  "ok": true,
  "retryable": false,
  "error_code": "",
  "summary": "动作执行成功",
  "data": {
    "status": "completed"
  },
  "charged_units": "0.000",
  "status": "succeeded",
  "task_status": "completed",
  "simulated_seconds": 211,
  "simulated_spent_units": "4.000"
}
```

## 17. terminal

方案及脚本已保存并可回读；未制作视频或投放广告

```json
{
  "seq": 17,
  "kind": "terminal",
  "run_id": "ed37e686-9678-406d-a36c-697af5458def",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-1",
  "status": "completed",
  "reason_code": "",
  "summary": "方案及脚本已保存并可回读；未制作视频或投放广告"
}
```
