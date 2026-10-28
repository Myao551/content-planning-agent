# 真实模型验收记录

模型：`qwen3.8-flash`；模型经真实 API 选择工具与生成严格事实脚本，业务工具使用本地合成数据。

| 场景 | 结果 | 本次 API 请求 | token | 输出 | Trace |
| --- | --- | --- | --- | --- | --- |
| normal | completed | 8 | 39853 | [JSON](81a3428d-5d8f-4c76-a66f-53e24b94b1d5/normal/625f7e35-c963-4adf-8592-96164f4493bd/output.json) | [Trace](81a3428d-5d8f-4c76-a66f-53e24b94b1d5/normal/625f7e35-c963-4adf-8592-96164f4493bd/trace.md) |
| replan | completed | 10 | 56641 | [JSON](81a3428d-5d8f-4c76-a66f-53e24b94b1d5/replan/c817acbb-aacd-4707-88ba-171dc949ccd8/output.json) | [Trace](81a3428d-5d8f-4c76-a66f-53e24b94b1d5/replan/c817acbb-aacd-4707-88ba-171dc949ccd8/trace.md) |
| repeat | completed | 0 | 0 | [JSON](81a3428d-5d8f-4c76-a66f-53e24b94b1d5/repeat/625f7e35-c963-4adf-8592-96164f4493bd/output.json) | [Trace](81a3428d-5d8f-4c76-a66f-53e24b94b1d5/repeat/625f7e35-c963-4adf-8592-96164f4493bd/trace.md) |

[原始批次报告](81a3428d-5d8f-4c76-a66f-53e24b94b1d5/report.json)。本批合计 18 次请求、96494 token；repeat 回读原结果，本次无 API 请求。未查询实际账单或免费额度扣减。

执行代码：[036a6db](https://github.com/Myao551/content-planning-agent/commit/036a6db33bbec097591e5cfb7eda6876c13723e2)，源码摘要 `f4fbda4435ad2e3753873477acf95db817ec8b9dcaeeb0b4fa787a8f90cc181e`。这是该历史版本的实际执行记录，不冒充后续交互扩展或本次清理提交的新执行结果；每个目录保留原执行和导出元信息。

normal 使用标准方案，总额 12；replan 观察标准方案 12 超出预算 10 后，改选复用方案 8 并重新估算。保存前后校验及回放版本检查见报告。

工具失败和缺预算/截止时间的保留案例见 [离线验收索引](../README.md)。这些 Mock 检查不能替代对应真实模型效果证据。复现与配置见 [README](../../README.md)。
