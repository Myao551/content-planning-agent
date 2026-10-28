# 离线 Mock 实际执行记录

> 固定策略测试驱动，不是真实模型 ReAct 证据。

运行：`ea521bd1-2cf9-433d-b616-f82b54c54aba`；终态：`completed`；回放：`False`。

## 1. decision

先检索主题对应的商品与素材

```json
{
  "seq": 1,
  "kind": "decision",
  "run_id": "ea521bd1-2cf9-433d-b616-f82b54c54aba",
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
  "run_id": "ea521bd1-2cf9-433d-b616-f82b54c54aba",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": null,
  "call_id": "cfccc6ad-a9b2-4da1-893e-dff82c62c5ee",
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
  "run_id": "ea521bd1-2cf9-433d-b616-f82b54c54aba",
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
  "run_id": "ea521bd1-2cf9-433d-b616-f82b54c54aba",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-1",
  "call_id": "6def3691-92df-4d0a-a0b8-dc44567ce412",
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
  "run_id": "ea521bd1-2cf9-433d-b616-f82b54c54aba",
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
  "run_id": "ea521bd1-2cf9-433d-b616-f82b54c54aba",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-1",
  "call_id": "77e4a7f2-b8e4-40b1-b05b-324333541c16",
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
  "run_id": "ea521bd1-2cf9-433d-b616-f82b54c54aba",
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

动作执行成功

```json
{
  "seq": 8,
  "kind": "action_result",
  "run_id": "ea521bd1-2cf9-433d-b616-f82b54c54aba",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-1",
  "call_id": "7a439944-e9f5-492a-9659-6980b07e1ba4",
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
    "artifact_id": "12ad726d-d885-4bbd-a4ab-89a5a318669c",
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
      "id": "12ad726d-d885-4bbd-a4ab-89a5a318669c",
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

## 9. decision

计划或执行状态变化，重新核算预算与截止时间

```json
{
  "seq": 9,
  "kind": "decision",
  "run_id": "ea521bd1-2cf9-433d-b616-f82b54c54aba",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-1",
  "action": {
    "name": "estimate_cost",
    "arguments": {
      "plan_id": "plan-1"
    },
    "summary": "计划或执行状态变化，重新核算预算与截止时间",
    "observes_event_ids": [
      8
    ],
    "provider_call_id": null,
    "provider_request_id": null,
    "provider_message": null
  },
  "summary": "计划或执行状态变化，重新核算预算与截止时间"
}
```

## 10. action_result

动作执行成功

```json
{
  "seq": 10,
  "kind": "action_result",
  "run_id": "ea521bd1-2cf9-433d-b616-f82b54c54aba",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-1",
  "call_id": "ed0a2721-ace4-4aa9-8334-dd1854cd8d08",
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
    "signature": "194dc00ef2befcc4f892216dc89455cdfdca395f8b4c09018e0da4db983884ff",
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

## 11. decision

脚本存在且复核可行，尝试保存方案

```json
{
  "seq": 11,
  "kind": "decision",
  "run_id": "ea521bd1-2cf9-433d-b616-f82b54c54aba",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-1",
  "action": {
    "name": "save_solution",
    "arguments": {
      "plan_id": "plan-1",
      "artifact_id": "12ad726d-d885-4bbd-a4ab-89a5a318669c"
    },
    "summary": "脚本存在且复核可行，尝试保存方案",
    "observes_event_ids": [
      10
    ],
    "provider_call_id": null,
    "provider_request_id": null,
    "provider_message": null
  },
  "summary": "脚本存在且复核可行，尝试保存方案"
}
```

## 12. action_result

动作执行成功

```json
{
  "seq": 12,
  "kind": "action_result",
  "run_id": "ea521bd1-2cf9-433d-b616-f82b54c54aba",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-1",
  "call_id": "db45d645-6551-4e96-8877-453be4afb067",
  "tool": "save_solution",
  "parameters": {
    "plan_id": "plan-1",
    "artifact_id": "12ad726d-d885-4bbd-a4ab-89a5a318669c"
  },
  "provider_call_id": null,
  "attempt_key": "a5167cb6b8d5b52eb3b676ce33b0a146c2bf7981e71f7702a89c07f0af200216",
  "ok": true,
  "retryable": false,
  "error_code": "",
  "summary": "动作执行成功",
  "data": {
    "solution_id": "ec8ae0a2-96d9-43d9-a58b-4503838a0518",
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

## 13. decision

观察到保存回执，申请结束任务

```json
{
  "seq": 13,
  "kind": "decision",
  "run_id": "ea521bd1-2cf9-433d-b616-f82b54c54aba",
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
      12
    ],
    "provider_call_id": null,
    "provider_request_id": null,
    "provider_message": null
  },
  "summary": "观察到保存回执，申请结束任务"
}
```

## 14. action_result

动作执行成功

```json
{
  "seq": 14,
  "kind": "action_result",
  "run_id": "ea521bd1-2cf9-433d-b616-f82b54c54aba",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-1",
  "call_id": "92eb03a1-9ee0-477f-825b-8b88346ce430",
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

## 15. terminal

方案及脚本已保存并可回读；未制作视频或投放广告

```json
{
  "seq": 15,
  "kind": "terminal",
  "run_id": "ea521bd1-2cf9-433d-b616-f82b54c54aba",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-1",
  "status": "completed",
  "reason_code": "",
  "summary": "方案及脚本已保存并可回读；未制作视频或投放广告"
}
```
