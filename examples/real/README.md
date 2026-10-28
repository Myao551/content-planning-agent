# 冻结修复版本的真实回归

执行代码：[提交 036a6db](https://github.com/Myao551/content-planning-agent/commit/036a6db33bbec097591e5cfb7eda6876c13723e2)。源码摘要 `f4fbda4435ad2e3753873477acf95db817ec8b9dcaeeb0b4fa787a8f90cc181e`。

| 场景 | 结果 | 新增 API 请求 | token | 输出 | Trace |
| --- | --- | --- | --- | --- | --- |
| normal | completed | 8 | 39853 | [JSON](81a3428d-5d8f-4c76-a66f-53e24b94b1d5/normal/625f7e35-c963-4adf-8592-96164f4493bd/output.json) | [Trace](81a3428d-5d8f-4c76-a66f-53e24b94b1d5/normal/625f7e35-c963-4adf-8592-96164f4493bd/trace.md) |
| replan | completed | 10 | 56641 | [JSON](81a3428d-5d8f-4c76-a66f-53e24b94b1d5/replan/c817acbb-aacd-4707-88ba-171dc949ccd8/output.json) | [Trace](81a3428d-5d8f-4c76-a66f-53e24b94b1d5/replan/c817acbb-aacd-4707-88ba-171dc949ccd8/trace.md) |
| repeat | completed | 0 | 0 | [JSON](81a3428d-5d8f-4c76-a66f-53e24b94b1d5/repeat/625f7e35-c963-4adf-8592-96164f4493bd/output.json) | [Trace](81a3428d-5d8f-4c76-a66f-53e24b94b1d5/repeat/625f7e35-c963-4adf-8592-96164f4493bd/trace.md) |

[批次报告](81a3428d-5d8f-4c76-a66f-53e24b94b1d5/report.json)、[版本一致性检查](../provenance-regression.json)。本批只有两条新的模型任务，repeat 是零新增请求的原任务回放。

以下保留先前批次；旧元信息 v1 的 implementation_hash 是导出时摘要，执行版本未知，不能等同于本次冻结回归。

---

# 真实 API 执行记录

模型：`qwen3.8-flash`；业务工具使用本地合成资料。

模型任务 3 个完成；另有缺参数、历史回放 2 个零新增 API 检查。真实预算无解用例因批次用量阈值跳过。

| 场景 | 结果 | 本次 API 次数 | token | 输出 | Trace |
| --- | --- | --- | --- | --- | --- |
| normal | completed | 9 | 46536 | [JSON](2b26551a-36bb-468c-a4c1-6cf3f8c930da/normal/df1c4a3c-6913-4f85-993f-bebe0adfcafd/output.json) | [Trace](2b26551a-36bb-468c-a4c1-6cf3f8c930da/normal/df1c4a3c-6913-4f85-993f-bebe0adfcafd/trace.md) |
| replan | completed | 10 | 56815 | [JSON](2b26551a-36bb-468c-a4c1-6cf3f8c930da/replan/fd51c3ba-8338-42ca-91f3-ccefa6b64558/output.json) | [Trace](2b26551a-36bb-468c-a4c1-6cf3f8c930da/replan/fd51c3ba-8338-42ca-91f3-ccefa6b64558/trace.md) |
| failure | completed | 9 | 47061 | [JSON](2b26551a-36bb-468c-a4c1-6cf3f8c930da/failure/ddfcbd91-ee43-4562-a602-5a30f598f0ee/output.json) | [Trace](2b26551a-36bb-468c-a4c1-6cf3f8c930da/failure/ddfcbd91-ee43-4562-a602-5a30f598f0ee/trace.md) |
| missing | needs_input | 0 | 0 | [JSON](2b26551a-36bb-468c-a4c1-6cf3f8c930da/missing/bc1a8c34-fa60-4046-b6d8-2db41d7318f3/output.json) | [Trace](2b26551a-36bb-468c-a4c1-6cf3f8c930da/missing/bc1a8c34-fa60-4046-b6d8-2db41d7318f3/trace.md) |
| repeat | completed | 0 | 0 | [JSON](2b26551a-36bb-468c-a4c1-6cf3f8c930da/repeat/df1c4a3c-6913-4f85-993f-bebe0adfcafd/output.json) | [Trace](2b26551a-36bb-468c-a4c1-6cf3f8c930da/repeat/df1c4a3c-6913-4f85-993f-bebe0adfcafd/trace.md) |
| infeasible | 未运行：用量阈值 | 0 | 0 | — | — |

[完整批次报告](2b26551a-36bb-468c-a4c1-6cf3f8c930da/report.json)。`all_passed=false` 表示请求的全部用例未都执行；已执行的 5 项检查均符合预期。

[连通性检查](connection-probe.json) 另消耗 30 token；未查询实际账单或剩余额度。
