# 离线评估与实际证据

**本页仅统计离线 Mock 流程，真实 API 结果在独立评估中报告。**

本页下方 72 项测试和 14 个案例是此前审查修复批次。后续交互扩展新增测试后共 82 项通过，持续对话真实验证、原始用量及版本边界见 [交互验证记录](../examples/chat/README.md)，不将新测试数量附着到旧结果文件。

案例使用固定业务时钟、本地合成数据和确定性 Mock；所有输出与 Trace 来自实际程序执行。
预期业务失败返回 needs_input / incomplete / invalid_input 是正确结果，不等于这些任务已完成。

## 自动化测试

实际执行 `python -m pytest -q`，退出码 0，72 项通过。
[原始测试输出](../examples/test-results.txt)、[测试元信息](../examples/test-results.json)。

覆盖输入、费用、时限、错误动作、上限、事务回滚、重复请求、脚本复用、无依据事实、规则变化、已有支出保留和 CLI。

## 案例结果

本批 14 个离线案例，14 个满足各自预期与程序断言。
这不是任务全部完成的比例，也不代表真实模型成功率。

| 案例 | 预期 | 实际 | 检查通过 | 实际输出 | 实际 Trace |
| --- | --- | --- | --- | --- | --- |
| 01-normal | completed | completed | True | [JSON](../examples/mock/01-normal/ea521bd1-2cf9-433d-b616-f82b54c54aba/output.json) | [记录](../examples/mock/01-normal/ea521bd1-2cf9-433d-b616-f82b54c54aba/trace.md) |
| 02-missing-budget | needs_input | needs_input | True | [JSON](../examples/mock/02-missing-budget/67afec4f-138b-473d-a7e4-43d4a03552ff/output.json) | [记录](../examples/mock/02-missing-budget/67afec4f-138b-473d-a7e4-43d4a03552ff/trace.md) |
| 03-missing-deadline | needs_input | needs_input | True | [JSON](../examples/mock/03-missing-deadline/809f0ad4-958d-4a92-8b12-b5a18d677b7c/output.json) | [记录](../examples/mock/03-missing-deadline/809f0ad4-958d-4a92-8b12-b5a18d677b7c/trace.md) |
| 04-budget-replan | completed | completed | True | [JSON](../examples/mock/04-budget-replan/0f625d5c-7676-44d3-941c-80b40783232b/output.json) | [记录](../examples/mock/04-budget-replan/0f625d5c-7676-44d3-941c-80b40783232b/trace.md) |
| 05-infeasible | incomplete | incomplete | True | [JSON](../examples/mock/05-infeasible/c4cdcc0a-7ef5-41d2-9a2a-6cda76c83fbd/output.json) | [记录](../examples/mock/05-infeasible/c4cdcc0a-7ef5-41d2-9a2a-6cda76c83fbd/trace.md) |
| 06-tool-failure | completed | completed | True | [JSON](../examples/mock/06-tool-failure/374a9f07-16fe-46e5-9fd0-6c6bad92de66/output.json) | [记录](../examples/mock/06-tool-failure/374a9f07-16fe-46e5-9fd0-6c6bad92de66/trace.md) |
| 07-repeat | completed | completed | True | [JSON](../examples/mock/07-repeat/ea521bd1-2cf9-433d-b616-f82b54c54aba/output.json) | [记录](../examples/mock/07-repeat/ea521bd1-2cf9-433d-b616-f82b54c54aba/trace.md) |
| 08-save-failure | incomplete | incomplete | True | [JSON](../examples/mock/08-save-failure/12ee3364-d66e-4cfc-b1c9-c914d0f5857f/output.json) | [记录](../examples/mock/08-save-failure/12ee3364-d66e-4cfc-b1c9-c914d0f5857f/trace.md) |
| 09-deadline | completed | completed | True | [JSON](../examples/mock/09-deadline/33244561-17ea-477d-ac3d-54ec6fa7e3a1/output.json) | [记录](../examples/mock/09-deadline/33244561-17ea-477d-ac3d-54ec6fa7e3a1/trace.md) |
| 10-missing-material | needs_input | needs_input | True | [JSON](../examples/mock/10-missing-material/dec701ab-5f36-4b48-928a-8b6addb3bd61/output.json) | [记录](../examples/mock/10-missing-material/dec701ab-5f36-4b48-928a-8b6addb3bd61/trace.md) |
| 11-request-conflict | invalid_input | invalid_input | True | [JSON](../examples/mock/11-request-conflict/5d7aef65-079e-4bef-a248-0e2393c98176/output.json) | [记录](../examples/mock/11-request-conflict/5d7aef65-079e-4bef-a248-0e2393c98176/trace.md) |
| 12-step-limit | incomplete | incomplete | True | [JSON](../examples/mock/12-step-limit/88eb49eb-c96e-4c2b-8fe8-dab641c73f17/output.json) | [记录](../examples/mock/12-step-limit/88eb49eb-c96e-4c2b-8fe8-dab641c73f17/trace.md) |
| 13-charged-failure | completed | completed | True | [JSON](../examples/mock/13-charged-failure/cbc58a0e-cbfa-4e6c-b7e6-2dbe2a824e8e/output.json) | [记录](../examples/mock/13-charged-failure/cbc58a0e-cbfa-4e6c-b7e6-2dbe2a824e8e/trace.md) |
| 14-changed-prices | completed | completed | True | [JSON](../examples/mock/14-changed-prices/23361df1-816f-4653-a0f3-7ac2311eefcb/output.json) | [记录](../examples/mock/14-changed-prices/23361df1-816f-4653-a0f3-7ac2311eefcb/trace.md) |

[逐项断言及结果](../examples/evaluation-results.json)；运行元信息与输入在每个案例目录中。

## 结果解释与限制

- 正常与预算调整分别运行四工具核心链路；预算 10 的示例实际观察标准 12 后改为复用 8。
- 替换费用表使复用方案不再可行，离线策略改为简化方案，避免把参考金额硬编码为结果。
- 缺预算与缺截止时间分别返回待补信息；工具失败案例保留已完成检索，并有限重试。
- 重复请求回读同一方案；输入冲突不覆盖原结果。事务回滚通过自动化测试另行注入。
- 保存持续失败保留脚本与已发生费用；已扣费再失败的案例保留旧费用，再估算可行替代方案。
- 截止时间和步数上限均有实际案例；其他边界由自动化测试覆盖。
- 本页离线案例没有发起真实 API 请求；Mock 动作说明不是真实模型推理过程或决策证据。
- 没有测量真实创作质量、实际转化效果、供应商性能、分布式并发或跨进程恢复。

## 复现

在仓库根目录安装后运行 `python scripts/verify.py`，生成新的一批结果。
单例命令、固定时钟和退出码说明见 [README](../README.md)。真实 API 结果使用独立目录和评估入口。

## 安装检查

另在全新虚拟环境安装构建的 wheel，并从仓库外运行 CLI。
[安装检查结果](../examples/installation-check.json)、[wheel 环境测试输出](../examples/wheel-test-results.txt)。

## 独立真实模型验证

真实 API 接入和实际记录见 [真实评估](06-real-api-evaluation.md)。本页重新生成不会改变这些记录。
