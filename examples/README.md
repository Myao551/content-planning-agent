# 离线案例索引

本页只统计 Mock 实际运行，不能代替真实模型决策验证。独立的真实记录见 [真实案例](real/README.md)。

| 案例 | 预期 / 实际 | 通过 | 输出 | Trace |
| --- | --- | --- | --- | --- |
| 01-normal | completed / completed | True | [JSON](mock/01-normal/ea521bd1-2cf9-433d-b616-f82b54c54aba/output.json) | [记录](mock/01-normal/ea521bd1-2cf9-433d-b616-f82b54c54aba/trace.md) |
| 02-missing-budget | needs_input / needs_input | True | [JSON](mock/02-missing-budget/67afec4f-138b-473d-a7e4-43d4a03552ff/output.json) | [记录](mock/02-missing-budget/67afec4f-138b-473d-a7e4-43d4a03552ff/trace.md) |
| 03-missing-deadline | needs_input / needs_input | True | [JSON](mock/03-missing-deadline/809f0ad4-958d-4a92-8b12-b5a18d677b7c/output.json) | [记录](mock/03-missing-deadline/809f0ad4-958d-4a92-8b12-b5a18d677b7c/trace.md) |
| 04-budget-replan | completed / completed | True | [JSON](mock/04-budget-replan/0f625d5c-7676-44d3-941c-80b40783232b/output.json) | [记录](mock/04-budget-replan/0f625d5c-7676-44d3-941c-80b40783232b/trace.md) |
| 05-infeasible | incomplete / incomplete | True | [JSON](mock/05-infeasible/c4cdcc0a-7ef5-41d2-9a2a-6cda76c83fbd/output.json) | [记录](mock/05-infeasible/c4cdcc0a-7ef5-41d2-9a2a-6cda76c83fbd/trace.md) |
| 06-tool-failure | completed / completed | True | [JSON](mock/06-tool-failure/374a9f07-16fe-46e5-9fd0-6c6bad92de66/output.json) | [记录](mock/06-tool-failure/374a9f07-16fe-46e5-9fd0-6c6bad92de66/trace.md) |
| 07-repeat | completed / completed | True | [JSON](mock/07-repeat/ea521bd1-2cf9-433d-b616-f82b54c54aba/output.json) | [记录](mock/07-repeat/ea521bd1-2cf9-433d-b616-f82b54c54aba/trace.md) |
| 08-save-failure | incomplete / incomplete | True | [JSON](mock/08-save-failure/12ee3364-d66e-4cfc-b1c9-c914d0f5857f/output.json) | [记录](mock/08-save-failure/12ee3364-d66e-4cfc-b1c9-c914d0f5857f/trace.md) |
| 09-deadline | completed / completed | True | [JSON](mock/09-deadline/33244561-17ea-477d-ac3d-54ec6fa7e3a1/output.json) | [记录](mock/09-deadline/33244561-17ea-477d-ac3d-54ec6fa7e3a1/trace.md) |
| 10-missing-material | needs_input / needs_input | True | [JSON](mock/10-missing-material/dec701ab-5f36-4b48-928a-8b6addb3bd61/output.json) | [记录](mock/10-missing-material/dec701ab-5f36-4b48-928a-8b6addb3bd61/trace.md) |
| 11-request-conflict | invalid_input / invalid_input | True | [JSON](mock/11-request-conflict/5d7aef65-079e-4bef-a248-0e2393c98176/output.json) | [记录](mock/11-request-conflict/5d7aef65-079e-4bef-a248-0e2393c98176/trace.md) |
| 12-step-limit | incomplete / incomplete | True | [JSON](mock/12-step-limit/88eb49eb-c96e-4c2b-8fe8-dab641c73f17/output.json) | [记录](mock/12-step-limit/88eb49eb-c96e-4c2b-8fe8-dab641c73f17/trace.md) |
| 13-charged-failure | completed / completed | True | [JSON](mock/13-charged-failure/cbc58a0e-cbfa-4e6c-b7e6-2dbe2a824e8e/output.json) | [记录](mock/13-charged-failure/cbc58a0e-cbfa-4e6c-b7e6-2dbe2a824e8e/trace.md) |
| 14-changed-prices | completed / completed | True | [JSON](mock/14-changed-prices/23361df1-816f-4653-a0f3-7ac2311eefcb/output.json) | [记录](mock/14-changed-prices/23361df1-816f-4653-a0f3-7ac2311eefcb/trace.md) |
