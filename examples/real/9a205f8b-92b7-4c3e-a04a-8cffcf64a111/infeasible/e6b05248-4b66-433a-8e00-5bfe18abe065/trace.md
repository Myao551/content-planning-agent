# 真实百炼模型执行记录

> 模型经原生工具调用作决策；业务工具使用本地合成数据。

运行：`e6b05248-4b66-433a-8e00-5bfe18abe065`；终态：`incomplete`；回放：`False`。

## 1. terminal

决策驱动未返回有效动作：百炼连接或请求超时，未获得有效响应

```json
{
  "seq": 1,
  "kind": "terminal",
  "run_id": "e6b05248-4b66-433a-8e00-5bfe18abe065",
  "timestamp": "2026-10-28T09:59:18.915548+00:00",
  "plan_id": null,
  "status": "incomplete",
  "reason_code": "driver_error",
  "summary": "决策驱动未返回有效动作：百炼连接或请求超时，未获得有效响应"
}
```
