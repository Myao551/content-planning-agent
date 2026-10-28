# 效果评估与验收证据

本仓库保留一套题目要求的验收材料：7 个离线案例、2 条不同真实模型执行路径及 1 个零新增请求回放。预期的 needs_input / incomplete 也是正确的业务结果，不将所有案例都描述为任务完成。

## 自动化测试

测试结果与退出码见 [实际 pytest 输出](../examples/test-results.txt) 和 [元信息](../examples/test-results.json)。覆盖输入、费用、时间、依赖、事务失败与回读、有限重试、请求冲突、规则变化、部分成功保留、执行上限、HTTP 协议及持续对话。

## 离线必验收案例

固定业务时钟与合成资料，驱动为确定性 Mock，真实 API 请求为零。保留此前实际运行的一套结果，没有因清理重新编造输出。

| 验收场景 | 预期 | 实际 | 输出 | Trace |
| --- | --- | --- | --- | --- |
| 01-normal | completed | completed | [JSON](../examples/mock/01-normal/ea521bd1-2cf9-433d-b616-f82b54c54aba/output.json) | [Trace](../examples/mock/01-normal/ea521bd1-2cf9-433d-b616-f82b54c54aba/trace.md) |
| 02-missing-budget | needs_input | needs_input | [JSON](../examples/mock/02-missing-budget/67afec4f-138b-473d-a7e4-43d4a03552ff/output.json) | [Trace](../examples/mock/02-missing-budget/67afec4f-138b-473d-a7e4-43d4a03552ff/trace.md) |
| 03-missing-deadline | needs_input | needs_input | [JSON](../examples/mock/03-missing-deadline/809f0ad4-958d-4a92-8b12-b5a18d677b7c/output.json) | [Trace](../examples/mock/03-missing-deadline/809f0ad4-958d-4a92-8b12-b5a18d677b7c/trace.md) |
| 04-budget-replan | completed | completed | [JSON](../examples/mock/04-budget-replan/0f625d5c-7676-44d3-941c-80b40783232b/output.json) | [Trace](../examples/mock/04-budget-replan/0f625d5c-7676-44d3-941c-80b40783232b/trace.md) |
| 05-infeasible | incomplete | incomplete | [JSON](../examples/mock/05-infeasible/c4cdcc0a-7ef5-41d2-9a2a-6cda76c83fbd/output.json) | [Trace](../examples/mock/05-infeasible/c4cdcc0a-7ef5-41d2-9a2a-6cda76c83fbd/trace.md) |
| 06-tool-failure | completed | completed | [JSON](../examples/mock/06-tool-failure/374a9f07-16fe-46e5-9fd0-6c6bad92de66/output.json) | [Trace](../examples/mock/06-tool-failure/374a9f07-16fe-46e5-9fd0-6c6bad92de66/trace.md) |
| 07-repeat | completed | completed | [JSON](../examples/mock/07-repeat/ea521bd1-2cf9-433d-b616-f82b54c54aba/output.json) | [Trace](../examples/mock/07-repeat/ea521bd1-2cf9-433d-b616-f82b54c54aba/trace.md) |

[逐项断言](../examples/evaluation-results.json)。正常与预算重规划执行完整工具链；缺预算/截止时间时请求补充；工具注入一次失败后有限重试；无可行方案时说明缺口；重复请求复用同一方案，不重复扣费。额外边界通过可执行测试覆盖，不再保留每次开发测试生成的重复目录。

## 真实模型决策

| 场景 | 实际 | API 请求 | token | 输出 | Trace |
| --- | --- | --- | --- | --- | --- |
| normal | completed | 8 | 39853 | [JSON](../examples/real/81a3428d-5d8f-4c76-a66f-53e24b94b1d5/normal/625f7e35-c963-4adf-8592-96164f4493bd/output.json) | [Trace](../examples/real/81a3428d-5d8f-4c76-a66f-53e24b94b1d5/normal/625f7e35-c963-4adf-8592-96164f4493bd/trace.md) |
| replan | completed | 10 | 56641 | [JSON](../examples/real/81a3428d-5d8f-4c76-a66f-53e24b94b1d5/replan/c817acbb-aacd-4707-88ba-171dc949ccd8/output.json) | [Trace](../examples/real/81a3428d-5d8f-4c76-a66f-53e24b94b1d5/replan/c817acbb-aacd-4707-88ba-171dc949ccd8/trace.md) |
| repeat | completed | 0 | 0 | [JSON](../examples/real/81a3428d-5d8f-4c76-a66f-53e24b94b1d5/repeat/625f7e35-c963-4adf-8592-96164f4493bd/output.json) | [Trace](../examples/real/81a3428d-5d8f-4c76-a66f-53e24b94b1d5/repeat/625f7e35-c963-4adf-8592-96164f4493bd/trace.md) |

[原始真实批次报告](../examples/real/81a3428d-5d8f-4c76-a66f-53e24b94b1d5/report.json)、[真实索引与版本边界](../examples/real/README.md)。共 18 次请求、96494 token；实际 API 金额未知，不与模拟单位相加。normal 选择标准方案 12；replan 观察费用超出预算 10，改选总额 8 的复用方案并重新估算、生成、复核和保存；repeat 沿用原执行版本且零新增请求。

这批真实结果指向冻结提交 036a6db，而当前实现还包含之后的持续对话与显示层扩展。清理不修改原执行版本，当前代码的自动化验证版本另见 test-results.json。本次文件整理没有重新调用真实 API。

## 失败、观察与限制

- Mock 只能证明流程和不变量；真实材料仅证明已测的模型、配置及有限路径。保留的真实批次不包含工具故障或预算无解的真实模型执行。
- 真实业务仍使用合成资料；脚本严格引用事实，没有验证开放式创意、翻译、视频制作、投放或商业转化。
- 持续对话曾在开发试用中出现模型把截止月份复述错的情况；完成摘要已改为显示程序校验过的结构化字段，原完整说明仍可在任务 JSON 中核对。详细开发试用目录本次不保留。
- 资源预留未支付；未查询真实账单。支持会话恢复，不支持崩溃任务自动续跑或生产级并发。
- 达到执行上限明确返回未完成，已有产物不能替代成功保存回执。

## 复现

安装与单例命令见 [README](../README.md)。`python -m pytest -q` 只用临时目录；`python scripts/verify.py` 会重新执行测试并生成完整 14 个离线检查及新结果，产生新的本地数据库，不会请求真实模型。真实评估须显式运行 `python scripts/evaluate_real.py` 并承担对应 API 用量。
