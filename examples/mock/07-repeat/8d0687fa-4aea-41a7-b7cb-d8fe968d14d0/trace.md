# 离线 Mock 实际执行记录

> 固定策略测试驱动，不是真实模型 ReAct 证据。

运行：`8d0687fa-4aea-41a7-b7cb-d8fe968d14d0`；终态：`completed`；回放：`True`。

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
  "run_id": "8d0687fa-4aea-41a7-b7cb-d8fe968d14d0",
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
  "call_id": "fc382a24-04d9-42d0-a4f7-8a5f2d507161",
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
  "run_id": "8d0687fa-4aea-41a7-b7cb-d8fe968d14d0",
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
  "run_id": "8d0687fa-4aea-41a7-b7cb-d8fe968d14d0",
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
  "call_id": "9b7445da-69b2-4c00-a191-b301693d71ee",
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
  "run_id": "8d0687fa-4aea-41a7-b7cb-d8fe968d14d0",
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
  "run_id": "8d0687fa-4aea-41a7-b7cb-d8fe968d14d0",
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
  "call_id": "cef8de64-3d6d-4198-a2d4-0bb48b6a81ac",
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
  "run_id": "8d0687fa-4aea-41a7-b7cb-d8fe968d14d0",
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
  "run_id": "8d0687fa-4aea-41a7-b7cb-d8fe968d14d0",
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
  "call_id": "c27889e5-0843-4232-9d0d-7a275df09ea3",
  "charged_units": "4.000",
  "data": {
    "artifact_id": "b979332e-52e3-427f-9b74-da2cecda974e",
    "cached": false,
    "script": {
      "fingerprint": "bd27932ea8474a2b193e7059ef04125c42f65726f5b11b91d45176569d8ed5cc",
      "generation_note": "Mock 逐条引用合成事实，不代表真实模型创作或翻译能力",
      "id": "b979332e-52e3-427f-9b74-da2cecda974e",
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
  "run_id": "8d0687fa-4aea-41a7-b7cb-d8fe968d14d0",
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
  "run_id": "8d0687fa-4aea-41a7-b7cb-d8fe968d14d0",
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
  "call_id": "36b97211-98b3-42d9-a10f-b49b273251fd",
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
    "signature": "3bbc2c1c973f6ca628480ba881250ea6f70eebb9a777aa814e4b600206931ed0",
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
  "run_id": "8d0687fa-4aea-41a7-b7cb-d8fe968d14d0",
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
      "artifact_id": "b979332e-52e3-427f-9b74-da2cecda974e",
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
  "run_id": "8d0687fa-4aea-41a7-b7cb-d8fe968d14d0",
  "seq": 11,
  "summary": "脚本存在且复核可行，尝试保存方案",
  "timestamp": "2030-01-01T10:00:00+08:00"
}
```

## 12. action_result

动作执行成功

```json
{
  "attempt_key": "38a4bf274a1f0d22e5270d873048995b0041540bd7b54504d35f60aafbf8a76f",
  "call_id": "1498504f-ff0a-45e3-9e33-c635f55c2f24",
  "charged_units": "0.000",
  "data": {
    "saved": true,
    "saved_at": "2030-01-01T10:03:31+08:00",
    "solution_id": "be0d8df5-bcdb-4a01-8333-2ed1a3a73cf3"
  },
  "error_code": "",
  "kind": "action_result",
  "ok": true,
  "parameters": {
    "artifact_id": "b979332e-52e3-427f-9b74-da2cecda974e",
    "plan_id": "plan-1"
  },
  "plan_id": "plan-1",
  "provider_call_id": null,
  "retryable": false,
  "run_id": "8d0687fa-4aea-41a7-b7cb-d8fe968d14d0",
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
  "run_id": "8d0687fa-4aea-41a7-b7cb-d8fe968d14d0",
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
  "call_id": "94b03c6d-ff03-465b-8b0e-9ea5280c630c",
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
  "run_id": "8d0687fa-4aea-41a7-b7cb-d8fe968d14d0",
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
  "run_id": "8d0687fa-4aea-41a7-b7cb-d8fe968d14d0",
  "seq": 15,
  "status": "completed",
  "summary": "方案及脚本已保存并可回读；未制作视频或投放广告",
  "timestamp": "2030-01-01T10:00:00+08:00"
}
```
