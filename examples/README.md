# 离线案例索引

这些是 Mock 驱动下的实际程序运行，真实模型决策尚未验证。

| 案例 | 预期 / 实际 | 通过 | 输出 | Trace |
| --- | --- | --- | --- | --- |
| 01-normal | completed / completed | True | [JSON](mock/01-normal/8fd9f9b4-591f-46c1-91ef-e4608412fe4e/output.json) | [记录](mock/01-normal/8fd9f9b4-591f-46c1-91ef-e4608412fe4e/trace.md) |
| 02-missing-budget | needs_input / needs_input | True | [JSON](mock/02-missing-budget/e60b727d-0eab-4044-b775-5bf628c3811a/output.json) | [记录](mock/02-missing-budget/e60b727d-0eab-4044-b775-5bf628c3811a/trace.md) |
| 03-missing-deadline | needs_input / needs_input | True | [JSON](mock/03-missing-deadline/4efefbe2-acd0-45b3-9e6a-93cf8473790b/output.json) | [记录](mock/03-missing-deadline/4efefbe2-acd0-45b3-9e6a-93cf8473790b/trace.md) |
| 04-budget-replan | completed / completed | True | [JSON](mock/04-budget-replan/6c878ce5-2eb3-43ca-875e-2bbb15ebe0f3/output.json) | [记录](mock/04-budget-replan/6c878ce5-2eb3-43ca-875e-2bbb15ebe0f3/trace.md) |
| 05-infeasible | incomplete / incomplete | True | [JSON](mock/05-infeasible/539fa0a3-b73e-47e4-847f-b98796a71fd7/output.json) | [记录](mock/05-infeasible/539fa0a3-b73e-47e4-847f-b98796a71fd7/trace.md) |
| 06-tool-failure | completed / completed | True | [JSON](mock/06-tool-failure/30824501-f187-474c-8af4-da2dc84f7ef6/output.json) | [记录](mock/06-tool-failure/30824501-f187-474c-8af4-da2dc84f7ef6/trace.md) |
| 07-repeat | completed / completed | True | [JSON](mock/07-repeat/8fd9f9b4-591f-46c1-91ef-e4608412fe4e/output.json) | [记录](mock/07-repeat/8fd9f9b4-591f-46c1-91ef-e4608412fe4e/trace.md) |
| 08-save-failure | incomplete / incomplete | True | [JSON](mock/08-save-failure/54b41758-7e77-4c99-a670-94eb19d4323f/output.json) | [记录](mock/08-save-failure/54b41758-7e77-4c99-a670-94eb19d4323f/trace.md) |
| 09-deadline | completed / completed | True | [JSON](mock/09-deadline/4a9daf1e-a220-4ecd-bcc6-4a1ba2213cc2/output.json) | [记录](mock/09-deadline/4a9daf1e-a220-4ecd-bcc6-4a1ba2213cc2/trace.md) |
| 10-missing-material | needs_input / needs_input | True | [JSON](mock/10-missing-material/c4768c43-df78-45c4-939f-cc07ec9aeeb0/output.json) | [记录](mock/10-missing-material/c4768c43-df78-45c4-939f-cc07ec9aeeb0/trace.md) |
| 11-request-conflict | invalid_input / invalid_input | True | [JSON](mock/11-request-conflict/9e25d534-ccc7-44e3-ade2-a3b2d310d7f3/output.json) | [记录](mock/11-request-conflict/9e25d534-ccc7-44e3-ade2-a3b2d310d7f3/trace.md) |
| 12-step-limit | incomplete / incomplete | True | [JSON](mock/12-step-limit/ff58e34c-e6fa-4ca4-8b51-d3865d468d07/output.json) | [记录](mock/12-step-limit/ff58e34c-e6fa-4ca4-8b51-d3865d468d07/trace.md) |
| 13-charged-failure | completed / completed | True | [JSON](mock/13-charged-failure/56f94475-979d-40a8-b17c-4cc638175749/output.json) | [记录](mock/13-charged-failure/56f94475-979d-40a8-b17c-4cc638175749/trace.md) |
| 14-changed-prices | completed / completed | True | [JSON](mock/14-changed-prices/038e7d34-5c17-4db6-96d1-705236031389/output.json) | [记录](mock/14-changed-prices/038e7d34-5c17-4db6-96d1-705236031389/trace.md) |
