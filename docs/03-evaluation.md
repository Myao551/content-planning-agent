# 离线评估与实际证据

**验证范围：离线流程已验证，真实模型决策待验证。**

案例使用固定业务时钟、本地合成数据和确定性 Mock；所有输出与 Trace 来自实际程序执行。
预期业务失败返回 needs_input / incomplete / invalid_input 是正确结果，不等于这些任务已完成。

## 自动化测试

实际执行 `python -m pytest -q`，退出码 0，45 项通过。
[原始测试输出](../examples/test-results.txt)、[测试元信息](../examples/test-results.json)。

覆盖输入、费用、时限、错误动作、上限、事务回滚、重复请求、脚本复用、无依据事实、规则变化、已有支出保留和 CLI。

## 案例结果

本批 14 个离线案例，14 个满足各自预期与程序断言。
这不是任务全部完成的比例，也不代表真实模型成功率。

| 案例 | 预期 | 实际 | 检查通过 | 实际输出 | 实际 Trace |
| --- | --- | --- | --- | --- | --- |
| 01-normal | completed | completed | True | [JSON](../examples/mock/01-normal/e33f1f06-dd4a-4105-b79a-edab4bf4547c/output.json) | [记录](../examples/mock/01-normal/e33f1f06-dd4a-4105-b79a-edab4bf4547c/trace.md) |
| 02-missing-budget | needs_input | needs_input | True | [JSON](../examples/mock/02-missing-budget/19e3669a-37ed-4142-a1ea-496d1dac9995/output.json) | [记录](../examples/mock/02-missing-budget/19e3669a-37ed-4142-a1ea-496d1dac9995/trace.md) |
| 03-missing-deadline | needs_input | needs_input | True | [JSON](../examples/mock/03-missing-deadline/18389245-93d3-4b72-8611-3245bba2e6b5/output.json) | [记录](../examples/mock/03-missing-deadline/18389245-93d3-4b72-8611-3245bba2e6b5/trace.md) |
| 04-budget-replan | completed | completed | True | [JSON](../examples/mock/04-budget-replan/8f43846d-8927-4b11-977a-744f8ff9ba89/output.json) | [记录](../examples/mock/04-budget-replan/8f43846d-8927-4b11-977a-744f8ff9ba89/trace.md) |
| 05-infeasible | incomplete | incomplete | True | [JSON](../examples/mock/05-infeasible/6079885f-ec6b-4f61-a328-417c64d4133f/output.json) | [记录](../examples/mock/05-infeasible/6079885f-ec6b-4f61-a328-417c64d4133f/trace.md) |
| 06-tool-failure | completed | completed | True | [JSON](../examples/mock/06-tool-failure/6287a28f-7355-422a-97db-fb34017c48e6/output.json) | [记录](../examples/mock/06-tool-failure/6287a28f-7355-422a-97db-fb34017c48e6/trace.md) |
| 07-repeat | completed | completed | True | [JSON](../examples/mock/07-repeat/e33f1f06-dd4a-4105-b79a-edab4bf4547c/output.json) | [记录](../examples/mock/07-repeat/e33f1f06-dd4a-4105-b79a-edab4bf4547c/trace.md) |
| 08-save-failure | incomplete | incomplete | True | [JSON](../examples/mock/08-save-failure/ad150b05-4330-4cd0-966f-15aa5a510233/output.json) | [记录](../examples/mock/08-save-failure/ad150b05-4330-4cd0-966f-15aa5a510233/trace.md) |
| 09-deadline | completed | completed | True | [JSON](../examples/mock/09-deadline/9694964b-06c3-44d6-9bcd-08527d68c706/output.json) | [记录](../examples/mock/09-deadline/9694964b-06c3-44d6-9bcd-08527d68c706/trace.md) |
| 10-missing-material | needs_input | needs_input | True | [JSON](../examples/mock/10-missing-material/6903a308-cf10-4095-bace-8a01483af585/output.json) | [记录](../examples/mock/10-missing-material/6903a308-cf10-4095-bace-8a01483af585/trace.md) |
| 11-request-conflict | invalid_input | invalid_input | True | [JSON](../examples/mock/11-request-conflict/0d24a242-70f3-4e83-adc8-12f054b17361/output.json) | [记录](../examples/mock/11-request-conflict/0d24a242-70f3-4e83-adc8-12f054b17361/trace.md) |
| 12-step-limit | incomplete | incomplete | True | [JSON](../examples/mock/12-step-limit/58a53dab-c11f-4b7c-85be-225c7348ce7f/output.json) | [记录](../examples/mock/12-step-limit/58a53dab-c11f-4b7c-85be-225c7348ce7f/trace.md) |
| 13-charged-failure | completed | completed | True | [JSON](../examples/mock/13-charged-failure/53b5bab9-c65c-42db-8179-99b1a548b6de/output.json) | [记录](../examples/mock/13-charged-failure/53b5bab9-c65c-42db-8179-99b1a548b6de/trace.md) |
| 14-changed-prices | completed | completed | True | [JSON](../examples/mock/14-changed-prices/ce53abe8-750d-4331-90aa-3d580fa0abf4/output.json) | [记录](../examples/mock/14-changed-prices/ce53abe8-750d-4331-90aa-3d580fa0abf4/trace.md) |

[逐项断言及结果](../examples/evaluation-results.json)；运行元信息与输入在每个案例目录中。

## 结果解释与限制

- 正常与预算调整分别运行四工具核心链路；预算 10 的示例实际观察标准 12 后改为复用 8。
- 替换费用表使复用方案不再可行，离线策略改为简化方案，避免把参考金额硬编码为结果。
- 缺预算与缺截止时间分别返回待补信息；工具失败案例保留已完成检索，并有限重试。
- 重复请求回读同一方案；输入冲突不覆盖原结果。事务回滚通过自动化测试另行注入。
- 保存持续失败保留脚本与已发生费用；已扣费再失败的案例保留旧费用，再估算可行替代方案。
- 截止时间和步数上限均有实际案例；其他边界由自动化测试覆盖。
- 所有真实 API 请求为零；Mock 动作说明不是真实模型推理过程或决策证据。
- 没有测量真实创作质量、实际转化效果、供应商性能、分布式并发或跨进程恢复。

## 复现

在仓库根目录安装后运行 `python scripts/verify.py`，生成新的一批结果。
单例命令、固定时钟和退出码说明见 [README](../README.md)。真实模型接入留到下一阶段。

## 安装检查

另在全新虚拟环境安装构建的 wheel，并从仓库外运行 CLI。
[安装检查结果](../examples/installation-check.json)、[wheel 环境测试输出](../examples/wheel-test-results.txt)。
