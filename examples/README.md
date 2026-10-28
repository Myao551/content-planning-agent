# 离线案例索引

这些是 Mock 驱动下的实际程序运行，真实模型决策尚未验证。

| 案例 | 预期 / 实际 | 通过 | 输出 | Trace |
| --- | --- | --- | --- | --- |
| 01-normal | completed / completed | True | [JSON](mock/01-normal/e33f1f06-dd4a-4105-b79a-edab4bf4547c/output.json) | [记录](mock/01-normal/e33f1f06-dd4a-4105-b79a-edab4bf4547c/trace.md) |
| 02-missing-budget | needs_input / needs_input | True | [JSON](mock/02-missing-budget/19e3669a-37ed-4142-a1ea-496d1dac9995/output.json) | [记录](mock/02-missing-budget/19e3669a-37ed-4142-a1ea-496d1dac9995/trace.md) |
| 03-missing-deadline | needs_input / needs_input | True | [JSON](mock/03-missing-deadline/18389245-93d3-4b72-8611-3245bba2e6b5/output.json) | [记录](mock/03-missing-deadline/18389245-93d3-4b72-8611-3245bba2e6b5/trace.md) |
| 04-budget-replan | completed / completed | True | [JSON](mock/04-budget-replan/8f43846d-8927-4b11-977a-744f8ff9ba89/output.json) | [记录](mock/04-budget-replan/8f43846d-8927-4b11-977a-744f8ff9ba89/trace.md) |
| 05-infeasible | incomplete / incomplete | True | [JSON](mock/05-infeasible/6079885f-ec6b-4f61-a328-417c64d4133f/output.json) | [记录](mock/05-infeasible/6079885f-ec6b-4f61-a328-417c64d4133f/trace.md) |
| 06-tool-failure | completed / completed | True | [JSON](mock/06-tool-failure/6287a28f-7355-422a-97db-fb34017c48e6/output.json) | [记录](mock/06-tool-failure/6287a28f-7355-422a-97db-fb34017c48e6/trace.md) |
| 07-repeat | completed / completed | True | [JSON](mock/07-repeat/e33f1f06-dd4a-4105-b79a-edab4bf4547c/output.json) | [记录](mock/07-repeat/e33f1f06-dd4a-4105-b79a-edab4bf4547c/trace.md) |
| 08-save-failure | incomplete / incomplete | True | [JSON](mock/08-save-failure/ad150b05-4330-4cd0-966f-15aa5a510233/output.json) | [记录](mock/08-save-failure/ad150b05-4330-4cd0-966f-15aa5a510233/trace.md) |
| 09-deadline | completed / completed | True | [JSON](mock/09-deadline/9694964b-06c3-44d6-9bcd-08527d68c706/output.json) | [记录](mock/09-deadline/9694964b-06c3-44d6-9bcd-08527d68c706/trace.md) |
| 10-missing-material | needs_input / needs_input | True | [JSON](mock/10-missing-material/6903a308-cf10-4095-bace-8a01483af585/output.json) | [记录](mock/10-missing-material/6903a308-cf10-4095-bace-8a01483af585/trace.md) |
| 11-request-conflict | invalid_input / invalid_input | True | [JSON](mock/11-request-conflict/0d24a242-70f3-4e83-adc8-12f054b17361/output.json) | [记录](mock/11-request-conflict/0d24a242-70f3-4e83-adc8-12f054b17361/trace.md) |
| 12-step-limit | incomplete / incomplete | True | [JSON](mock/12-step-limit/58a53dab-c11f-4b7c-85be-225c7348ce7f/output.json) | [记录](mock/12-step-limit/58a53dab-c11f-4b7c-85be-225c7348ce7f/trace.md) |
| 13-charged-failure | completed / completed | True | [JSON](mock/13-charged-failure/53b5bab9-c65c-42db-8179-99b1a548b6de/output.json) | [记录](mock/13-charged-failure/53b5bab9-c65c-42db-8179-99b1a548b6de/trace.md) |
| 14-changed-prices | completed / completed | True | [JSON](mock/14-changed-prices/ce53abe8-750d-4331-90aa-3d580fa0abf4/output.json) | [记录](mock/14-changed-prices/ce53abe8-750d-4331-90aa-3d580fa0abf4/trace.md) |
