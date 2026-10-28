# 真实百炼模型执行记录

> 模型经原生工具调用作决策；业务工具使用本地合成数据。

运行：`6f3f6ef7-ce63-4ae1-a4f9-834524503e25`；终态：`incomplete`；回放：`False`。

## 1. terminal

决策驱动未返回有效动作：百炼连接或请求超时，未获得有效响应

```json
{
  "seq": 1,
  "kind": "terminal",
  "run_id": "6f3f6ef7-ce63-4ae1-a4f9-834524503e25",
  "timestamp": "2026-10-28T09:59:18.866818+00:00",
  "plan_id": null,
  "status": "incomplete",
  "reason_code": "driver_error",
  "summary": "决策驱动未返回有效动作：百炼连接或请求超时，未获得有效响应"
}
```
