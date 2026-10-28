# 离线 Mock 实际执行记录

> 固定策略测试驱动，不是真实模型 ReAct 证据。

运行：`e33f1f06-dd4a-4105-b79a-edab4bf4547c`；终态：`completed`；回放：`True`。

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
    "summary": "先检索主题对应的商品与素材"
  },
  "kind": "decision",
  "plan_id": null,
  "run_id": "e33f1f06-dd4a-4105-b79a-edab4bf4547c",
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
  "call_id": "a6aeca0d-fab2-4b4b-8dfd-dc619af38330",
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
  "retryable": false,
  "run_id": "e33f1f06-dd4a-4105-b79a-edab4bf4547c",
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
    "summary": "使用已检索素材提出标准方案，随后估算"
  },
  "kind": "decision",
  "plan_id": null,
  "run_id": "e33f1f06-dd4a-4105-b79a-edab4bf4547c",
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
  "call_id": "bc70077d-fd2d-4d94-8836-a71c14482674",
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
  "retryable": false,
  "run_id": "e33f1f06-dd4a-4105-b79a-edab4bf4547c",
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
    "summary": "计划或执行状态变化，重新核算预算与截止时间"
  },
  "kind": "decision",
  "plan_id": "plan-1",
  "run_id": "e33f1f06-dd4a-4105-b79a-edab4bf4547c",
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
  "call_id": "ddb17695-8669-4654-b828-f0396c0a2972",
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
  "retryable": false,
  "run_id": "e33f1f06-dd4a-4105-b79a-edab4bf4547c",
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
    "summary": "估算可行，生成有来源的离线脚本；如之前失败，按上限有限重试"
  },
  "kind": "decision",
  "plan_id": "plan-1",
  "run_id": "e33f1f06-dd4a-4105-b79a-edab4bf4547c",
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
  "call_id": "273754f7-c56c-437c-a39b-e2951940ce4f",
  "charged_units": "4.000",
  "data": {
    "artifact_id": "793bbd10-6e46-45aa-a675-a80223c7b9f1",
    "cached": false,
    "script": {
      "fingerprint": "bd27932ea8474a2b193e7059ef04125c42f65726f5b11b91d45176569d8ed5cc",
      "generation_note": "Mock 逐条引用合成事实，不代表真实模型创作或翻译能力",
      "id": "793bbd10-6e46-45aa-a675-a80223c7b9f1",
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
  "retryable": false,
  "run_id": "e33f1f06-dd4a-4105-b79a-edab4bf4547c",
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
    "summary": "计划或执行状态变化，重新核算预算与截止时间"
  },
  "kind": "decision",
  "plan_id": "plan-1",
  "run_id": "e33f1f06-dd4a-4105-b79a-edab4bf4547c",
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
  "call_id": "a618c6ab-6fd1-4455-919b-2f0431020571",
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
    "signature": "8432131341f634ff88d5285e7ebc7bff52303f351dcd1f58a96efc30c28d553b",
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
  "retryable": false,
  "run_id": "e33f1f06-dd4a-4105-b79a-edab4bf4547c",
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
      "artifact_id": "793bbd10-6e46-45aa-a675-a80223c7b9f1",
      "plan_id": "plan-1"
    },
    "name": "save_solution",
    "observes_event_ids": [
      10
    ],
    "summary": "脚本存在且复核可行，尝试保存方案"
  },
  "kind": "decision",
  "plan_id": "plan-1",
  "run_id": "e33f1f06-dd4a-4105-b79a-edab4bf4547c",
  "seq": 11,
  "summary": "脚本存在且复核可行，尝试保存方案",
  "timestamp": "2030-01-01T10:00:00+08:00"
}
```

## 12. action_result

动作执行成功

```json
{
  "attempt_key": "436e3a74154e1eac3e25c8783c62062b240aeddb36b882808271876081daa7e1",
  "call_id": "7a6efe91-1357-4687-a4bb-c3d96a1d4dac",
  "charged_units": "0.000",
  "data": {
    "saved": true,
    "saved_at": "2030-01-01T10:03:31+08:00",
    "solution_id": "f2c22b81-fe8c-4df9-9ef6-e6915bfb5ad6"
  },
  "error_code": "",
  "kind": "action_result",
  "ok": true,
  "parameters": {
    "artifact_id": "793bbd10-6e46-45aa-a675-a80223c7b9f1",
    "plan_id": "plan-1"
  },
  "plan_id": "plan-1",
  "retryable": false,
  "run_id": "e33f1f06-dd4a-4105-b79a-edab4bf4547c",
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
    "summary": "观察到保存回执，申请结束任务"
  },
  "kind": "decision",
  "plan_id": "plan-1",
  "run_id": "e33f1f06-dd4a-4105-b79a-edab4bf4547c",
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
  "call_id": "ef1793c5-8d61-4629-9a27-e40f3d950811",
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
  "retryable": false,
  "run_id": "e33f1f06-dd4a-4105-b79a-edab4bf4547c",
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
  "run_id": "e33f1f06-dd4a-4105-b79a-edab4bf4547c",
  "seq": 15,
  "status": "completed",
  "summary": "方案及脚本已保存并可回读；未制作视频或投放广告",
  "timestamp": "2030-01-01T10:00:00+08:00"
}
```
