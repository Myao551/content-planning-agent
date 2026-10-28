# 阿里百炼真实 API 评估

> 本页下方保留初次接入的历史评估。最新冻结版本的真实回归与执行/导出版本一致性验证，见 [修复回执](08-review-resolution.md) 和 [版本检查](../examples/provenance-regression.json)。


## 范围与结论

使用用户指定的本地 CSV 接入其北京业务空间的 OpenAI 兼容 HTTP 接口，请求模型为 `qwen3.8-flash`，关闭思考模式。密钥与业务空间地址未写入仓库。

**3 个需要模型决策的任务均完成，2 个无需新增模型调用的检查符合预期；1 个真实预算无解用例因用量阈值未运行。** 这只是小规模功能验证，不是模型普遍成功率或完整基准。

四个业务工具使用本地合成资料与计费规则；模型选择动作及严格事实脚本生成通过真实 API 完成，不是 Mock。

## 实际结果

| 场景 | 实际结果 | API 请求 | token | 实际墙钟耗时 | 输出 | Trace |
| --- | --- | --- | --- | --- | --- | --- |
| 正常规划 | completed | 9 | 46536 | 22.99 秒 | [JSON](../examples/real/2b26551a-36bb-468c-a4c1-6cf3f8c930da/normal/df1c4a3c-6913-4f85-993f-bebe0adfcafd/output.json) | [Trace](../examples/real/2b26551a-36bb-468c-a4c1-6cf3f8c930da/normal/df1c4a3c-6913-4f85-993f-bebe0adfcafd/trace.md) |
| 预算超限调整 | completed | 10 | 56815 | 27.15 秒 | [JSON](../examples/real/2b26551a-36bb-468c-a4c1-6cf3f8c930da/replan/fd51c3ba-8338-42ca-91f3-ccefa6b64558/output.json) | [Trace](../examples/real/2b26551a-36bb-468c-a4c1-6cf3f8c930da/replan/fd51c3ba-8338-42ca-91f3-ccefa6b64558/trace.md) |
| 工具失败后恢复 | completed | 9 | 47061 | 23.73 秒 | [JSON](../examples/real/2b26551a-36bb-468c-a4c1-6cf3f8c930da/failure/ddfcbd91-ee43-4562-a602-5a30f598f0ee/output.json) | [Trace](../examples/real/2b26551a-36bb-468c-a4c1-6cf3f8c930da/failure/ddfcbd91-ee43-4562-a602-5a30f598f0ee/trace.md) |
| 缺预算预检查 | needs_input | 0 | 0 | 未单独测量 | [JSON](../examples/real/2b26551a-36bb-468c-a4c1-6cf3f8c930da/missing/bc1a8c34-fa60-4046-b6d8-2db41d7318f3/output.json) | [Trace](../examples/real/2b26551a-36bb-468c-a4c1-6cf3f8c930da/missing/bc1a8c34-fa60-4046-b6d8-2db41d7318f3/trace.md) |
| 相同请求历史回放 | completed | 0 | 0 | 未单独测量 | [JSON](../examples/real/2b26551a-36bb-468c-a4c1-6cf3f8c930da/repeat/df1c4a3c-6913-4f85-993f-bebe0adfcafd/output.json) | [Trace](../examples/real/2b26551a-36bb-468c-a4c1-6cf3f8c930da/repeat/df1c4a3c-6913-4f85-993f-bebe0adfcafd/trace.md) |
| 预算无可行方案 | 未运行，用量阈值停止 | 0 | 0 | 未测 | — | — |

[批次报告](../examples/real/2b26551a-36bb-468c-a4c1-6cf3f8c930da/report.json)、[真实记录索引](../examples/real/README.md)。报告 `all_passed=false` 反映有用例跳过，不表示已执行五项检查有失败。

## 关键观察

- 正常任务使用标准方案，模拟工具支出 4、资源预留 8，总额 12，保存与回读成功。模型曾未先估算就申请生成，程序以 `stale_estimate` 拒绝；模型观察错误后补做估算，随后完成。不能把这次运行描述为全程没有错误动作。
- 预算 10 的任务先估算标准方案为 12，模型改选复用方案、重新估算为 8，再生成、复核、保存。最终模拟工具支出 2，资源预留 6，未擅自提高预算。
- 脚本工具注入一次执行前失败后，模型观察失败返回并重试，保留此前素材检索结果，最终保存。该故障是本地注入，不是阿里服务故障。
- 缺预算在预检查结束，未调用模型；历史回放返回同一方案，未增加 API 请求。回放输出中的原运行时间不能作为本次回放延迟。
- 真实预算无解用例未继续请求；离线测试覆盖该逻辑，但不能据此声称已经验证其真实模型行为。

## 用量与边界

三项模型任务共 28 次请求、150412 token；最小连通性检查另为 1 次、30 token，已取得有效响应的合计为 29 次、150442 token。统计来自 API usage，未查询账单、免费额度扣减或实时余额，实际金额未知。

批次在各用例之间检查 150000 token 阈值；最后一个完整用例使累计量略高于阈值，之后没有增加付费模型案例。缺参数与回放随后通过零新增请求检查。此阈值不是供应商账单硬限额。

初次在网络受限沙盒中的请求未取得供应商有效响应；在授权网络环境重跑后完成。该连接错误批次不纳入模型任务效果统计，[原始网络受限记录](../examples/real/9a205f8b-92b7-4c3e-a04a-8cffcf64a111/report.json) 仍保留以区别环境失败和模型行为。

当前每个模型任务约 4.7—5.7 万 token，工具 schema、多轮历史和重复状态有上下文开销。尚未进行压缩上下文后的对比实验，也没有测试其他图片中模型，因此不作模型间优劣结论。

脚本采用严格事实引用，文本须逐字来自所选素材并附来源 ID；这验证了真实生成调用与约束，不证明开放式营销文案质量、翻译、视频生成或商业转化效果。

## 复现与单元测试

后续已将入口推广为通用 OpenAI 兼容协议，并支持自动读取 `.env`，不再依赖 CSV。[无 CSV 参数的真实连接检查](../examples/env-connection-probe.json) 已成功。该检查是在原三条任务验证之外额外执行的 1 次、30 token；其他供应商仅通过协议模拟测试，未宣称逐一真实调用。

见 [README 的真实模式命令](../README.md)。应使用新 request_id 与未来截止时间；真实模式不允许固定演示时钟，可显式注入工具故障。缺凭据或 HTTP 失败不会静默回退 Mock。

[自动化测试结果](../examples/test-results.txt) 还包含 HTTP 协议桩测试：原生工具调用 ID 回传、密钥不进入状态、内部思考字段不进入 Trace、累计用量与回放、多个原生调用拒绝等。这些单元测试使用假传输，不计入上表的真实 API 次数。

## 官方依据

[阿里百炼 Function Calling](https://help.aliyun.com/zh/model-studio/qwen-function-calling)、[OpenAI Chat 接口兼容](https://help.aliyun.com/zh/model-studio/compatibility-of-openai-with-dashscope)：使用业务空间专属接口，保留工具调用关联并回传执行结果。实际支持性以上述运行证据为准。
