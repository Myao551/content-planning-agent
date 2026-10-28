# 验收案例索引

按题目要求保留实际输入、输出和 Trace。离线材料覆盖全部必验收情形；真实记录单独展示模型根据工具结果调整动作的路径。历史重复批次和开发临时记录已清理，原运行文件未改写。

## 离线 Mock

| 案例 | 预期 / 实际 | 通过 | 输出 | Trace |
| --- | --- | --- | --- | --- |
| 01-normal | completed / completed | True | [JSON](mock/01-normal/ea521bd1-2cf9-433d-b616-f82b54c54aba/output.json) | [记录](mock/01-normal/ea521bd1-2cf9-433d-b616-f82b54c54aba/trace.md) |
| 02-missing-budget | needs_input / needs_input | True | [JSON](mock/02-missing-budget/67afec4f-138b-473d-a7e4-43d4a03552ff/output.json) | [记录](mock/02-missing-budget/67afec4f-138b-473d-a7e4-43d4a03552ff/trace.md) |
| 03-missing-deadline | needs_input / needs_input | True | [JSON](mock/03-missing-deadline/809f0ad4-958d-4a92-8b12-b5a18d677b7c/output.json) | [记录](mock/03-missing-deadline/809f0ad4-958d-4a92-8b12-b5a18d677b7c/trace.md) |
| 04-budget-replan | completed / completed | True | [JSON](mock/04-budget-replan/0f625d5c-7676-44d3-941c-80b40783232b/output.json) | [记录](mock/04-budget-replan/0f625d5c-7676-44d3-941c-80b40783232b/trace.md) |
| 05-infeasible | incomplete / incomplete | True | [JSON](mock/05-infeasible/c4cdcc0a-7ef5-41d2-9a2a-6cda76c83fbd/output.json) | [记录](mock/05-infeasible/c4cdcc0a-7ef5-41d2-9a2a-6cda76c83fbd/trace.md) |
| 06-tool-failure | completed / completed | True | [JSON](mock/06-tool-failure/374a9f07-16fe-46e5-9fd0-6c6bad92de66/output.json) | [记录](mock/06-tool-failure/374a9f07-16fe-46e5-9fd0-6c6bad92de66/trace.md) |
| 07-repeat | completed / completed | True | [JSON](mock/07-repeat/ea521bd1-2cf9-433d-b616-f82b54c54aba/output.json) | [记录](mock/07-repeat/ea521bd1-2cf9-433d-b616-f82b54c54aba/trace.md) |

共 7 个保留案例；Mock 不证明真实模型决策能力。边界与故障注入的可执行检查继续保留在 tests/，完整输入保留在 inputs/。

## 真实模型

[两条不同模型执行路径与回放](real/README.md)。本次清理没有新调用真实 API。

[自动化测试输出](test-results.txt)、[测试元信息](test-results.json)、[离线逐项断言](evaluation-results.json)。
