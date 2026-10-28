# 离线 Mock 实际执行记录

> 固定策略测试驱动，不是真实模型 ReAct 证据。

运行：`ea521bd1-2cf9-433d-b616-f82b54c54aba`；终态：`completed`；回放：`True`。

## 1. decision

先检索主题对应的商品与素材

```json
{
  "action": {
    "arguments": {
      "product_id": "P001",
      "query": "为便携咖啡杯策划新品营销视频内容活动"
    },
    "name": "search_materials",
    "observes_event_ids": [],
    "provider_call_id": null,
    "provider_message": null,
    "provider_request_id": null,
    "summary": "先检索主题对应的商品与素材"
  },
  "kind": "decision",
  "plan_id": null,
  "run_id": "ea521bd1-2cf9-433d-b616-f82b54c54aba",
  "seq": 1,
  "summary": "先检索主题对应的商品与素材",
  "timestamp": "2030-01-01T10:00:00+08:00"
}
```

## 2. action_result

动作执行成功

```json
{
  "attempt_key": "ed87acf267bbc473af81295d670c4dbbf924322ab90f149930a0e64a9cb81ed1",
  "call_id": "cfccc6ad-a9b2-4da1-893e-dff82c62c5ee",
  "charged_units": "0.000",
  "data": {
    "materials": [
      {
        "facts": [
          "容量 350 毫升",
          "提供黑色和白色款式"
        ],
        "id": "M001",
        "keywords": [
          "咖啡杯",
          "通勤",
          "外观",
          "coffee"
        ],
        "kind": "reusable",
        "match_reason": "商品标识匹配",
        "product_id": "P001",
        "score": 1,
        "title": "咖啡杯外观素材"
      },
      {
        "facts": [
          "附带杯盖"
        ],
        "id": "M002",
        "keywords": [
          "咖啡杯",
          "商品",
          "cup"
        ],
        "kind": "reference",
        "match_reason": "商品标识匹配",
        "product_id": "P001",
        "score": 1,
        "title": "咖啡杯商品说明"
      }
    ],
    "missing": [],
    "product": {
      "facts": [
        "容量 350 毫升",
        "附带杯盖",
        "提供黑色和白色款式"
      ],
      "id": "P001",
      "keywords": [
        "咖啡杯",
        "通勤",
        "coffee",
        "cup"
      ],
      "name": "便携咖啡杯"
    }
  },
  "error_code": "",
  "kind": "action_result",
  "ok": true,
  "parameters": {
    "product_id": "P001",
    "query": "为便携咖啡杯策划新品营销视频内容活动"
  },
  "plan_id": null,
  "provider_call_id": null,
  "retryable": false,
  "run_id": "ea521bd1-2cf9-433d-b616-f82b54c54aba",
  "seq": 2,
  "simulated_seconds": 30,
  "simulated_spent_units": "0.000",
  "status": "succeeded",
  "summary": "动作执行成功",
  "task_status": "running",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "tool": "search_materials"
}
```

## 3. decision

使用已检索素材提出标准方案，随后估算

```json
{
  "action": {
    "arguments": {
      "material_ids": [
        "M001",
        "M002"
      ],
      "steps": [
        {
          "action": "search_materials",
          "depends_on": [],
          "id": "materials"
        },
        {
          "action": "generate_script",
          "depends_on": [
            "materials"
          ],
          "id": "script"
        },
        {
          "action": "estimate_cost",
          "depends_on": [
            "script"
          ],
          "id": "verification"
        },
        {
          "action": "save_solution",
          "depends_on": [
            "verification"
          ],
          "id": "save"
        }
      ],
      "tier": "standard"
    },
    "name": "update_plan",
    "observes_event_ids": [
      2
    ],
    "provider_call_id": null,
    "provider_message": null,
    "provider_request_id": null,
    "summary": "使用已检索素材提出标准方案，随后估算"
  },
  "kind": "decision",
  "plan_id": null,
  "run_id": "ea521bd1-2cf9-433d-b616-f82b54c54aba",
  "seq": 3,
  "summary": "使用已检索素材提出标准方案，随后估算",
  "timestamp": "2030-01-01T10:00:00+08:00"
}
```

## 4. action_result

动作执行成功

```json
{
  "attempt_key": "09547b306a7f0935677b304ef6f6338af39619cbff87c82dd6a346fd57ab4580",
  "call_id": "6def3691-92df-4d0a-a0b8-dc44567ce412",
  "charged_units": "0.000",
  "data": {
    "id": "plan-1",
    "material_ids": [
      "M001",
      "M002"
    ],
    "steps": [
      {
        "action": "search_materials",
        "depends_on": [],
        "id": "materials"
      },
      {
        "action": "generate_script",
        "depends_on": [
          "materials"
        ],
        "id": "script"
      },
      {
        "action": "estimate_cost",
        "depends_on": [
          "script"
        ],
        "id": "verification"
      },
      {
        "action": "save_solution",
        "depends_on": [
          "verification"
        ],
        "id": "save"
      }
    ],
    "tier": "standard"
  },
  "error_code": "",
  "kind": "action_result",
  "ok": true,
  "parameters": {
    "material_ids": [
      "M001",
      "M002"
    ],
    "steps": [
      {
        "action": "search_materials",
        "depends_on": [],
        "id": "materials"
      },
      {
        "action": "generate_script",
        "depends_on": [
          "materials"
        ],
        "id": "script"
      },
      {
        "action": "estimate_cost",
        "depends_on": [
          "script"
        ],
        "id": "verification"
      },
      {
        "action": "save_solution",
        "depends_on": [
          "verification"
        ],
        "id": "save"
      }
    ],
    "tier": "standard"
  },
  "plan_id": "plan-1",
  "provider_call_id": null,
  "retryable": false,
  "run_id": "ea521bd1-2cf9-433d-b616-f82b54c54aba",
  "seq": 4,
  "simulated_seconds": 30,
  "simulated_spent_units": "0.000",
  "status": "succeeded",
  "summary": "动作执行成功",
  "task_status": "running",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "tool": "update_plan"
}
```

## 5. decision

计划或执行状态变化，重新核算预算与截止时间

```json
{
  "action": {
    "arguments": {
      "plan_id": "plan-1"
    },
    "name": "estimate_cost",
    "observes_event_ids": [
      4
    ],
    "provider_call_id": null,
    "provider_message": null,
    "provider_request_id": null,
    "summary": "计划或执行状态变化，重新核算预算与截止时间"
  },
  "kind": "decision",
  "plan_id": "plan-1",
  "run_id": "ea521bd1-2cf9-433d-b616-f82b54c54aba",
  "seq": 5,
  "summary": "计划或执行状态变化，重新核算预算与截止时间",
  "timestamp": "2030-01-01T10:00:00+08:00"
}
```

## 6. action_result

动作执行成功

```json
{
  "attempt_key": "a7900f6fdd1c1ae1438a3eccb6b6588b6448dc6c90a8ebee9d3ab69690959d00",
  "call_id": "77e4a7f2-b8e4-40b1-b05b-324333541c16",
  "charged_units": "0.000",
  "data": {
    "budget_gap_units": "0.000",
    "budget_units": "20.000",
    "deadline_at": "2030-01-01T10:30:00+08:00",
    "estimated_finish_at": "2030-01-01T10:03:31+08:00",
    "feasible": true,
    "plan_id": "plan-1",
    "planned_resource_units": "8.000",
    "projected_total_units": "12.000",
    "remaining_seconds": 181,
    "remaining_tool_units": "4.000",
    "signature": "846536f3d5a2f3cdb57dd96ad68ab24359a2c6e53a0a730757eb4ec5693dd790",
    "simulated_spent_units": "0.000",
    "time_gap_seconds": 0
  },
  "error_code": "",
  "kind": "action_result",
  "ok": true,
  "parameters": {
    "plan_id": "plan-1"
  },
  "plan_id": "plan-1",
  "provider_call_id": null,
  "retryable": false,
  "run_id": "ea521bd1-2cf9-433d-b616-f82b54c54aba",
  "seq": 6,
  "simulated_seconds": 30,
  "simulated_spent_units": "0.000",
  "status": "succeeded",
  "summary": "动作执行成功",
  "task_status": "running",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "tool": "estimate_cost"
}
```

## 7. decision

估算可行，生成有来源的离线脚本；如之前失败，按上限有限重试

```json
{
  "action": {
    "arguments": {
      "language": "zh-CN",
      "material_ids": [
        "M001",
        "M002"
      ],
      "plan_id": "plan-1"
    },
    "name": "generate_script",
    "observes_event_ids": [
      6
    ],
    "provider_call_id": null,
    "provider_message": null,
    "provider_request_id": null,
    "summary": "估算可行，生成有来源的离线脚本；如之前失败，按上限有限重试"
  },
  "kind": "decision",
  "plan_id": "plan-1",
  "run_id": "ea521bd1-2cf9-433d-b616-f82b54c54aba",
  "seq": 7,
  "summary": "估算可行，生成有来源的离线脚本；如之前失败，按上限有限重试",
  "timestamp": "2030-01-01T10:00:00+08:00"
}
```

## 8. action_result

动作执行成功

```json
{
  "attempt_key": "5219762da018c09cc8b76e3efe48638f19bb37da95dc794bc58c3c341fb9a543",
  "call_id": "7a439944-e9f5-492a-9659-6980b07e1ba4",
  "charged_units": "4.000",
  "data": {
    "artifact_id": "12ad726d-d885-4bbd-a4ab-89a5a318669c",
    "cached": false,
    "script": {
      "fingerprint": "bd27932ea8474a2b193e7059ef04125c42f65726f5b11b91d45176569d8ed5cc",
      "generation_note": "Mock 逐条引用合成事实，不代表真实模型创作或翻译能力",
      "id": "12ad726d-d885-4bbd-a4ab-89a5a318669c",
      "material_ids": [
        "M001",
        "M002"
      ],
      "mode": "mock",
      "segments": [
        {
          "source_ids": [
            "M001"
          ],
          "text": "容量 350 毫升"
        },
        {
          "source_ids": [
            "M001"
          ],
          "text": "提供黑色和白色款式"
        },
        {
          "source_ids": [
            "M002"
          ],
          "text": "附带杯盖"
        }
      ],
      "title": "便携咖啡杯营销内容方案（离线合成）"
    }
  },
  "error_code": "",
  "kind": "action_result",
  "ok": true,
  "parameters": {
    "language": "zh-CN",
    "material_ids": [
      "M001",
      "M002"
    ],
    "plan_id": "plan-1"
  },
  "plan_id": "plan-1",
  "provider_call_id": null,
  "retryable": false,
  "run_id": "ea521bd1-2cf9-433d-b616-f82b54c54aba",
  "seq": 8,
  "simulated_seconds": 210,
  "simulated_spent_units": "4.000",
  "status": "succeeded",
  "summary": "动作执行成功",
  "task_status": "running",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "tool": "generate_script"
}
```

## 9. decision

计划或执行状态变化，重新核算预算与截止时间

```json
{
  "action": {
    "arguments": {
      "plan_id": "plan-1"
    },
    "name": "estimate_cost",
    "observes_event_ids": [
      8
    ],
    "provider_call_id": null,
    "provider_message": null,
    "provider_request_id": null,
    "summary": "计划或执行状态变化，重新核算预算与截止时间"
  },
  "kind": "decision",
  "plan_id": "plan-1",
  "run_id": "ea521bd1-2cf9-433d-b616-f82b54c54aba",
  "seq": 9,
  "summary": "计划或执行状态变化，重新核算预算与截止时间",
  "timestamp": "2030-01-01T10:00:00+08:00"
}
```

## 10. action_result

动作执行成功

```json
{
  "attempt_key": "a7900f6fdd1c1ae1438a3eccb6b6588b6448dc6c90a8ebee9d3ab69690959d00",
  "call_id": "ed0a2721-ace4-4aa9-8334-dd1854cd8d08",
  "charged_units": "0.000",
  "data": {
    "budget_gap_units": "0.000",
    "budget_units": "20.000",
    "deadline_at": "2030-01-01T10:30:00+08:00",
    "estimated_finish_at": "2030-01-01T10:03:31+08:00",
    "feasible": true,
    "plan_id": "plan-1",
    "planned_resource_units": "8.000",
    "projected_total_units": "12.000",
    "remaining_seconds": 1,
    "remaining_tool_units": "0.000",
    "signature": "194dc00ef2befcc4f892216dc89455cdfdca395f8b4c09018e0da4db983884ff",
    "simulated_spent_units": "4.000",
    "time_gap_seconds": 0
  },
  "error_code": "",
  "kind": "action_result",
  "ok": true,
  "parameters": {
    "plan_id": "plan-1"
  },
  "plan_id": "plan-1",
  "provider_call_id": null,
  "retryable": false,
  "run_id": "ea521bd1-2cf9-433d-b616-f82b54c54aba",
  "seq": 10,
  "simulated_seconds": 210,
  "simulated_spent_units": "4.000",
  "status": "succeeded",
  "summary": "动作执行成功",
  "task_status": "running",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "tool": "estimate_cost"
}
```

## 11. decision

脚本存在且复核可行，尝试保存方案

```json
{
  "action": {
    "arguments": {
      "artifact_id": "12ad726d-d885-4bbd-a4ab-89a5a318669c",
      "plan_id": "plan-1"
    },
    "name": "save_solution",
    "observes_event_ids": [
      10
    ],
    "provider_call_id": null,
    "provider_message": null,
    "provider_request_id": null,
    "summary": "脚本存在且复核可行，尝试保存方案"
  },
  "kind": "decision",
  "plan_id": "plan-1",
  "run_id": "ea521bd1-2cf9-433d-b616-f82b54c54aba",
  "seq": 11,
  "summary": "脚本存在且复核可行，尝试保存方案",
  "timestamp": "2030-01-01T10:00:00+08:00"
}
```

## 12. action_result

动作执行成功

```json
{
  "attempt_key": "a5167cb6b8d5b52eb3b676ce33b0a146c2bf7981e71f7702a89c07f0af200216",
  "call_id": "db45d645-6551-4e96-8877-453be4afb067",
  "charged_units": "0.000",
  "data": {
    "saved": true,
    "saved_at": "2030-01-01T10:03:31+08:00",
    "solution_id": "ec8ae0a2-96d9-43d9-a58b-4503838a0518"
  },
  "error_code": "",
  "kind": "action_result",
  "ok": true,
  "parameters": {
    "artifact_id": "12ad726d-d885-4bbd-a4ab-89a5a318669c",
    "plan_id": "plan-1"
  },
  "plan_id": "plan-1",
  "provider_call_id": null,
  "retryable": false,
  "run_id": "ea521bd1-2cf9-433d-b616-f82b54c54aba",
  "seq": 12,
  "simulated_seconds": 211,
  "simulated_spent_units": "4.000",
  "status": "succeeded",
  "summary": "动作执行成功",
  "task_status": "running",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "tool": "save_solution"
}
```

## 13. decision

观察到保存回执，申请结束任务

```json
{
  "action": {
    "arguments": {
      "explanation": "方案及脚本已保存并可回读；未制作视频或投放广告",
      "status": "completed"
    },
    "name": "finish_task",
    "observes_event_ids": [
      12
    ],
    "provider_call_id": null,
    "provider_message": null,
    "provider_request_id": null,
    "summary": "观察到保存回执，申请结束任务"
  },
  "kind": "decision",
  "plan_id": "plan-1",
  "run_id": "ea521bd1-2cf9-433d-b616-f82b54c54aba",
  "seq": 13,
  "summary": "观察到保存回执，申请结束任务",
  "timestamp": "2030-01-01T10:00:00+08:00"
}
```

## 14. action_result

动作执行成功

```json
{
  "attempt_key": "fdd18cd7611b0f24fe5ad2a6bb6502f5352bb07dd5c148b9b455aa5b8b9d6f6a",
  "call_id": "92eb03a1-9ee0-477f-825b-8b88346ce430",
  "charged_units": "0.000",
  "data": {
    "status": "completed"
  },
  "error_code": "",
  "kind": "action_result",
  "ok": true,
  "parameters": {
    "explanation": "方案及脚本已保存并可回读；未制作视频或投放广告",
    "status": "completed"
  },
  "plan_id": "plan-1",
  "provider_call_id": null,
  "retryable": false,
  "run_id": "ea521bd1-2cf9-433d-b616-f82b54c54aba",
  "seq": 14,
  "simulated_seconds": 211,
  "simulated_spent_units": "4.000",
  "status": "succeeded",
  "summary": "动作执行成功",
  "task_status": "completed",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "tool": "finish_task"
}
```

## 15. terminal

方案及脚本已保存并可回读；未制作视频或投放广告

```json
{
  "kind": "terminal",
  "plan_id": "plan-1",
  "reason_code": "",
  "run_id": "ea521bd1-2cf9-433d-b616-f82b54c54aba",
  "seq": 15,
  "status": "completed",
  "summary": "方案及脚本已保存并可回读；未制作视频或投放广告",
  "timestamp": "2030-01-01T10:00:00+08:00"
}
```
