# 真实百炼模型执行记录

> 模型经原生工具调用作决策；业务工具使用本地合成数据。

运行：`bc1a8c34-fa60-4046-b6d8-2db41d7318f3`；终态：`needs_input`；回放：`False`。

## 1. terminal

缺少预算或截止时间，未执行业务工具

```json
{
  "seq": 1,
  "kind": "terminal",
  "run_id": "bc1a8c34-fa60-4046-b6d8-2db41d7318f3",
  "timestamp": "2026-10-28T10:03:42.985878+00:00",
  "plan_id": null,
  "status": "needs_input",
  "reason_code": "missing_information",
  "summary": "缺少预算或截止时间，未执行业务工具"
}
```
