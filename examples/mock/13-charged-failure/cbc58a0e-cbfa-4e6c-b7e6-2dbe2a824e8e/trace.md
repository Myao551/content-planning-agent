# 离线 Mock 实际执行记录

> 固定策略测试驱动，不是真实模型 ReAct 证据。

运行：`cbc58a0e-cbfa-4e6c-b7e6-2dbe2a824e8e`；终态：`completed`；回放：`False`。

## 1. decision

先检索主题对应的商品与素材

```json
{
  "seq": 1,
  "kind": "decision",
  "run_id": "cbc58a0e-cbfa-4e6c-b7e6-2dbe2a824e8e",
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
  "run_id": "cbc58a0e-cbfa-4e6c-b7e6-2dbe2a824e8e",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": null,
  "call_id": "408f895f-74f8-4096-a66d-97fc3187a3c2",
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
  "run_id": "cbc58a0e-cbfa-4e6c-b7e6-2dbe2a824e8e",
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
  "run_id": "cbc58a0e-cbfa-4e6c-b7e6-2dbe2a824e8e",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-1",
  "call_id": "56b74def-180c-4b88-8360-8c43a969a264",
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
  "run_id": "cbc58a0e-cbfa-4e6c-b7e6-2dbe2a824e8e",
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
  "run_id": "cbc58a0e-cbfa-4e6c-b7e6-2dbe2a824e8e",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-1",
  "call_id": "e9c61928-88c7-4d25-91e8-6c76faa9da89",
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
    "budget_units": "12.000",
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
  "run_id": "cbc58a0e-cbfa-4e6c-b7e6-2dbe2a824e8e",
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

已注入工具失败（模拟费用已发生）

```json
{
  "seq": 8,
  "kind": "action_result",
  "run_id": "cbc58a0e-cbfa-4e6c-b7e6-2dbe2a824e8e",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-1",
  "call_id": "f867bd13-22d3-4fac-a93c-444fcb08d6a7",
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
  "summary": "已注入工具失败（模拟费用已发生）",
  "data": null,
  "charged_units": "4.000",
  "status": "failed",
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
  "run_id": "cbc58a0e-cbfa-4e6c-b7e6-2dbe2a824e8e",
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
  "run_id": "cbc58a0e-cbfa-4e6c-b7e6-2dbe2a824e8e",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-1",
  "call_id": "76bc891f-813e-41b1-a5df-0caa605760c0",
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
    "signature": "88261cda78e9deb537e33aa565b07bc73c5535b64a79adffe1ef22acc1d0586c",
    "plan_id": "plan-1",
    "simulated_spent_units": "4.000",
    "remaining_tool_units": "4.000",
    "planned_resource_units": "8.000",
    "projected_total_units": "16.000",
    "budget_units": "12.000",
    "budget_gap_units": "4.000",
    "estimated_finish_at": "2030-01-01T10:06:31+08:00",
    "deadline_at": "2030-01-01T10:30:00+08:00",
    "remaining_seconds": 181,
    "time_gap_seconds": 0,
    "feasible": false
  },
  "charged_units": "0.000",
  "status": "succeeded",
  "task_status": "running",
  "simulated_seconds": 210,
  "simulated_spent_units": "4.000"
}
```

## 11. decision

工具估算不可行（预算缺口 4.000，时间缺口 0 秒），调整为 reuse 后再估算

```json
{
  "seq": 11,
  "kind": "decision",
  "run_id": "cbc58a0e-cbfa-4e6c-b7e6-2dbe2a824e8e",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-1",
  "action": {
    "name": "update_plan",
    "arguments": {
      "tier": "reuse",
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
    "summary": "工具估算不可行（预算缺口 4.000，时间缺口 0 秒），调整为 reuse 后再估算",
    "observes_event_ids": [
      10
    ],
    "provider_call_id": null,
    "provider_request_id": null,
    "provider_message": null
  },
  "summary": "工具估算不可行（预算缺口 4.000，时间缺口 0 秒），调整为 reuse 后再估算"
}
```

## 12. action_result

动作执行成功

```json
{
  "seq": 12,
  "kind": "action_result",
  "run_id": "cbc58a0e-cbfa-4e6c-b7e6-2dbe2a824e8e",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-2",
  "call_id": "de429a10-140e-4a7d-a5f7-6c6958f84d2e",
  "tool": "update_plan",
  "parameters": {
    "tier": "reuse",
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
  "attempt_key": "d59cbb5cf0afbe68c46f2d1dd8cc832c7e9dfd62c03d015964cbc843fa25e730",
  "ok": true,
  "retryable": false,
  "error_code": "",
  "summary": "动作执行成功",
  "data": {
    "id": "plan-2",
    "tier": "reuse",
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
  "simulated_seconds": 210,
  "simulated_spent_units": "4.000"
}
```

## 13. decision

计划或执行状态变化，重新核算预算与截止时间

```json
{
  "seq": 13,
  "kind": "decision",
  "run_id": "cbc58a0e-cbfa-4e6c-b7e6-2dbe2a824e8e",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-2",
  "action": {
    "name": "estimate_cost",
    "arguments": {
      "plan_id": "plan-2"
    },
    "summary": "计划或执行状态变化，重新核算预算与截止时间",
    "observes_event_ids": [
      12
    ],
    "provider_call_id": null,
    "provider_request_id": null,
    "provider_message": null
  },
  "summary": "计划或执行状态变化，重新核算预算与截止时间"
}
```

## 14. action_result

动作执行成功

```json
{
  "seq": 14,
  "kind": "action_result",
  "run_id": "cbc58a0e-cbfa-4e6c-b7e6-2dbe2a824e8e",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-2",
  "call_id": "96b405f5-a799-4518-bf67-5f6fc05416eb",
  "tool": "estimate_cost",
  "parameters": {
    "plan_id": "plan-2"
  },
  "provider_call_id": null,
  "attempt_key": "46dbd3e12abfd1cfe8869a2869b040afd657b602fdcda481471c30efa83db785",
  "ok": true,
  "retryable": false,
  "error_code": "",
  "summary": "动作执行成功",
  "data": {
    "signature": "03e8f8cf5e60d8d2122aebff2dcf845ef2a3e424c0418cbcccca2f39bff75977",
    "plan_id": "plan-2",
    "simulated_spent_units": "4.000",
    "remaining_tool_units": "2.000",
    "planned_resource_units": "6.000",
    "projected_total_units": "12.000",
    "budget_units": "12.000",
    "budget_gap_units": "0.000",
    "estimated_finish_at": "2030-01-01T10:05:01+08:00",
    "deadline_at": "2030-01-01T10:30:00+08:00",
    "remaining_seconds": 91,
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

## 15. decision

估算可行，生成有来源的离线脚本；如之前失败，按上限有限重试

```json
{
  "seq": 15,
  "kind": "decision",
  "run_id": "cbc58a0e-cbfa-4e6c-b7e6-2dbe2a824e8e",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-2",
  "action": {
    "name": "generate_script",
    "arguments": {
      "plan_id": "plan-2",
      "material_ids": [
        "M001",
        "M002"
      ],
      "language": "zh-CN"
    },
    "summary": "估算可行，生成有来源的离线脚本；如之前失败，按上限有限重试",
    "observes_event_ids": [
      14
    ],
    "provider_call_id": null,
    "provider_request_id": null,
    "provider_message": null
  },
  "summary": "估算可行，生成有来源的离线脚本；如之前失败，按上限有限重试"
}
```

## 16. action_result

动作执行成功

```json
{
  "seq": 16,
  "kind": "action_result",
  "run_id": "cbc58a0e-cbfa-4e6c-b7e6-2dbe2a824e8e",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-2",
  "call_id": "4dbe231e-a367-4004-b8c1-07938b4d4658",
  "tool": "generate_script",
  "parameters": {
    "plan_id": "plan-2",
    "material_ids": [
      "M001",
      "M002"
    ],
    "language": "zh-CN"
  },
  "provider_call_id": null,
  "attempt_key": "306c638d23cfc0dc14f6a66b136d60d4faffdfd574a49a220fdad85e4adb3475",
  "ok": true,
  "retryable": false,
  "error_code": "",
  "summary": "动作执行成功",
  "data": {
    "artifact_id": "592828ec-0bc1-4e79-aaa8-b3c0c2e2aa13",
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
      "id": "592828ec-0bc1-4e79-aaa8-b3c0c2e2aa13",
      "fingerprint": "84f655dcf18fd0d7e077d413584b2263fd15c358711638861de6b5d074b74c66",
      "mode": "mock",
      "material_ids": [
        "M001",
        "M002"
      ]
    }
  },
  "charged_units": "2.000",
  "status": "succeeded",
  "task_status": "running",
  "simulated_seconds": 300,
  "simulated_spent_units": "6.000"
}
```

## 17. decision

计划或执行状态变化，重新核算预算与截止时间

```json
{
  "seq": 17,
  "kind": "decision",
  "run_id": "cbc58a0e-cbfa-4e6c-b7e6-2dbe2a824e8e",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-2",
  "action": {
    "name": "estimate_cost",
    "arguments": {
      "plan_id": "plan-2"
    },
    "summary": "计划或执行状态变化，重新核算预算与截止时间",
    "observes_event_ids": [
      16
    ],
    "provider_call_id": null,
    "provider_request_id": null,
    "provider_message": null
  },
  "summary": "计划或执行状态变化，重新核算预算与截止时间"
}
```

## 18. action_result

动作执行成功

```json
{
  "seq": 18,
  "kind": "action_result",
  "run_id": "cbc58a0e-cbfa-4e6c-b7e6-2dbe2a824e8e",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-2",
  "call_id": "57e8e605-54ab-4cbe-b723-81d861283c47",
  "tool": "estimate_cost",
  "parameters": {
    "plan_id": "plan-2"
  },
  "provider_call_id": null,
  "attempt_key": "46dbd3e12abfd1cfe8869a2869b040afd657b602fdcda481471c30efa83db785",
  "ok": true,
  "retryable": false,
  "error_code": "",
  "summary": "动作执行成功",
  "data": {
    "signature": "1c834c5f1d807f50c14e46f3595a9f347e29ac94ce274a4a82847aea74ba8355",
    "plan_id": "plan-2",
    "simulated_spent_units": "6.000",
    "remaining_tool_units": "0.000",
    "planned_resource_units": "6.000",
    "projected_total_units": "12.000",
    "budget_units": "12.000",
    "budget_gap_units": "0.000",
    "estimated_finish_at": "2030-01-01T10:05:01+08:00",
    "deadline_at": "2030-01-01T10:30:00+08:00",
    "remaining_seconds": 1,
    "time_gap_seconds": 0,
    "feasible": true
  },
  "charged_units": "0.000",
  "status": "succeeded",
  "task_status": "running",
  "simulated_seconds": 300,
  "simulated_spent_units": "6.000"
}
```

## 19. decision

脚本存在且复核可行，尝试保存方案

```json
{
  "seq": 19,
  "kind": "decision",
  "run_id": "cbc58a0e-cbfa-4e6c-b7e6-2dbe2a824e8e",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-2",
  "action": {
    "name": "save_solution",
    "arguments": {
      "plan_id": "plan-2",
      "artifact_id": "592828ec-0bc1-4e79-aaa8-b3c0c2e2aa13"
    },
    "summary": "脚本存在且复核可行，尝试保存方案",
    "observes_event_ids": [
      18
    ],
    "provider_call_id": null,
    "provider_request_id": null,
    "provider_message": null
  },
  "summary": "脚本存在且复核可行，尝试保存方案"
}
```

## 20. action_result

动作执行成功

```json
{
  "seq": 20,
  "kind": "action_result",
  "run_id": "cbc58a0e-cbfa-4e6c-b7e6-2dbe2a824e8e",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-2",
  "call_id": "ac42ab2b-4d7e-4531-a6e8-3d79d30ed145",
  "tool": "save_solution",
  "parameters": {
    "plan_id": "plan-2",
    "artifact_id": "592828ec-0bc1-4e79-aaa8-b3c0c2e2aa13"
  },
  "provider_call_id": null,
  "attempt_key": "1edb07941366a3dbbffcd4d7099f1e9c3929dde1ad379e58389ce34ae40cbb85",
  "ok": true,
  "retryable": false,
  "error_code": "",
  "summary": "动作执行成功",
  "data": {
    "solution_id": "e50e0583-ea3c-4de2-91e5-34ae46a4dc55",
    "saved_at": "2030-01-01T10:05:01+08:00",
    "saved": true
  },
  "charged_units": "0.000",
  "status": "succeeded",
  "task_status": "running",
  "simulated_seconds": 301,
  "simulated_spent_units": "6.000"
}
```

## 21. decision

观察到保存回执，申请结束任务

```json
{
  "seq": 21,
  "kind": "decision",
  "run_id": "cbc58a0e-cbfa-4e6c-b7e6-2dbe2a824e8e",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-2",
  "action": {
    "name": "finish_task",
    "arguments": {
      "status": "completed",
      "explanation": "方案及脚本已保存并可回读；未制作视频或投放广告"
    },
    "summary": "观察到保存回执，申请结束任务",
    "observes_event_ids": [
      20
    ],
    "provider_call_id": null,
    "provider_request_id": null,
    "provider_message": null
  },
  "summary": "观察到保存回执，申请结束任务"
}
```

## 22. action_result

动作执行成功

```json
{
  "seq": 22,
  "kind": "action_result",
  "run_id": "cbc58a0e-cbfa-4e6c-b7e6-2dbe2a824e8e",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-2",
  "call_id": "c9ae9838-f4db-471b-b7ee-5e7e4869bc54",
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
  "simulated_seconds": 301,
  "simulated_spent_units": "6.000"
}
```

## 23. terminal

方案及脚本已保存并可回读；未制作视频或投放广告

```json
{
  "seq": 23,
  "kind": "terminal",
  "run_id": "cbc58a0e-cbfa-4e6c-b7e6-2dbe2a824e8e",
  "timestamp": "2030-01-01T10:00:00+08:00",
  "plan_id": "plan-2",
  "status": "completed",
  "reason_code": "",
  "summary": "方案及脚本已保存并可回读；未制作视频或投放广告"
}
```
