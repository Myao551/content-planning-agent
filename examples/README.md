# 离线案例索引

这些是 Mock 驱动下的实际程序运行，真实模型决策尚未验证。

| 案例 | 预期 / 实际 | 通过 | 输出 | Trace |
| --- | --- | --- | --- | --- |
| 01-normal | completed / completed | True | [JSON](mock/01-normal/8d0687fa-4aea-41a7-b7cb-d8fe968d14d0/output.json) | [记录](mock/01-normal/8d0687fa-4aea-41a7-b7cb-d8fe968d14d0/trace.md) |
| 02-missing-budget | needs_input / needs_input | True | [JSON](mock/02-missing-budget/8d9a00a3-2352-4851-b346-541ac08949c5/output.json) | [记录](mock/02-missing-budget/8d9a00a3-2352-4851-b346-541ac08949c5/trace.md) |
| 03-missing-deadline | needs_input / needs_input | True | [JSON](mock/03-missing-deadline/7491183a-153b-4b5d-969d-b8338c7a011a/output.json) | [记录](mock/03-missing-deadline/7491183a-153b-4b5d-969d-b8338c7a011a/trace.md) |
| 04-budget-replan | completed / completed | True | [JSON](mock/04-budget-replan/aed4f7ff-406d-4113-a026-701bb9227902/output.json) | [记录](mock/04-budget-replan/aed4f7ff-406d-4113-a026-701bb9227902/trace.md) |
| 05-infeasible | incomplete / incomplete | True | [JSON](mock/05-infeasible/4acc483d-f342-4528-b6fb-b09f72e307a1/output.json) | [记录](mock/05-infeasible/4acc483d-f342-4528-b6fb-b09f72e307a1/trace.md) |
| 06-tool-failure | completed / completed | True | [JSON](mock/06-tool-failure/ed37e686-9678-406d-a36c-697af5458def/output.json) | [记录](mock/06-tool-failure/ed37e686-9678-406d-a36c-697af5458def/trace.md) |
| 07-repeat | completed / completed | True | [JSON](mock/07-repeat/8d0687fa-4aea-41a7-b7cb-d8fe968d14d0/output.json) | [记录](mock/07-repeat/8d0687fa-4aea-41a7-b7cb-d8fe968d14d0/trace.md) |
| 08-save-failure | incomplete / incomplete | True | [JSON](mock/08-save-failure/bc55ae82-22e0-441d-acd6-8f28077319d0/output.json) | [记录](mock/08-save-failure/bc55ae82-22e0-441d-acd6-8f28077319d0/trace.md) |
| 09-deadline | completed / completed | True | [JSON](mock/09-deadline/ed96d8bd-7502-4bde-b704-a2d359f209ef/output.json) | [记录](mock/09-deadline/ed96d8bd-7502-4bde-b704-a2d359f209ef/trace.md) |
| 10-missing-material | needs_input / needs_input | True | [JSON](mock/10-missing-material/2fc9abd6-aa92-4ae6-9d5f-b55d1a099d4a/output.json) | [记录](mock/10-missing-material/2fc9abd6-aa92-4ae6-9d5f-b55d1a099d4a/trace.md) |
| 11-request-conflict | invalid_input / invalid_input | True | [JSON](mock/11-request-conflict/8bf5a91b-5b37-4ed9-8d51-dd4787d580a6/output.json) | [记录](mock/11-request-conflict/8bf5a91b-5b37-4ed9-8d51-dd4787d580a6/trace.md) |
| 12-step-limit | incomplete / incomplete | True | [JSON](mock/12-step-limit/388fd0e5-e0e3-4ecd-bb2b-cf9dcb0bff31/output.json) | [记录](mock/12-step-limit/388fd0e5-e0e3-4ecd-bb2b-cf9dcb0bff31/trace.md) |
| 13-charged-failure | completed / completed | True | [JSON](mock/13-charged-failure/c8277345-87b2-47a6-adab-eb4c380e428d/output.json) | [记录](mock/13-charged-failure/c8277345-87b2-47a6-adab-eb4c380e428d/trace.md) |
| 14-changed-prices | completed / completed | True | [JSON](mock/14-changed-prices/9d3d5c63-601e-4fb9-85e5-0816d9a01268/output.json) | [记录](mock/14-changed-prices/9d3d5c63-601e-4fb9-85e5-0816d9a01268/trace.md) |
