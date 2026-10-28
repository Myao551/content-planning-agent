# 持续对话 CLI 实际验证

2026-10-28 使用用户本地 `.env` 与 `qwen3.8-flash`，完整转录及结构化结果均由 CLI 实际运行产生。模拟工具仍使用合成业务数据。

| 检查 | 实际结果 | 证据 |
| --- | --- | --- |
| 分轮补充需求 | 首轮仅给主题，追问预算和截止时间；第二轮补齐后执行 | [输入](chat-live-78b4688b1a/user-input.txt)、[终端转录（仅去除行尾空格）](chat-live-78b4688b1a/transcript.txt) |
| 预算 10 | 完成，方案总额 8，保存并回读通过 | [结果](chat-live-78b4688b1a/budget-10/ba162d33-16eb-4229-8893-f894483566a0/output.json)、[Trace](chat-live-78b4688b1a/budget-10/ba162d33-16eb-4229-8893-f894483566a0/trace.md) |
| 连续查询解释 | 根据前一方案解释标准 12 超预算而改为复用 8 | [会话结构化记录](chat-live-78b4688b1a/session.json) |
| 预算改成 6 | 保留主题和截止时间，独立新任务完成，总额 3 | [结果](chat-live-78b4688b1a/budget-6/291a10ab-5182-42cd-a231-001d5b361b3e/output.json)、[Trace](chat-live-78b4688b1a/budget-6/291a10ab-5182-42cd-a231-001d5b361b3e/trace.md) |
| `/run` 重复执行 | 回放同一任务，本次 API 为 0 | [回放结果](chat-live-78b4688b1a/repeat/291a10ab-5182-42cd-a231-001d5b361b3e/output.json) |
| 更新显示层后恢复会话 | 显示已保存脚本与结构化截止时间，不新增 API | [实际终端输出](chat-live-78b4688b1a/readable-resume.txt) |
| 自动化测试 | 82 项通过 | [pytest 输出](test-results.txt) |

[检查报告](chat-live-78b4688b1a/report.json)。本批合计 27 次真实请求、151297 token，其中包含对话理解、解释及两个规划任务。API 实际收费和免费额度扣减没有查询。

完整真实对话执行时使用本地干净冻结提交 `f66e3f05cca1ab0fc105d3919c605b6125d61b1a`，其完整 Git tree 为 `92d3e9bb7f68ac157e8907126a2f98ba3e1c4e78`，与[公开提交 5c5cec6](https://github.com/Myao551/content-planning-agent/commit/5c5cec621e5ce6aa8f63e9e5f2cb0504e46f5e79)完全相同；两个提交因提交者时间等元信息不同而 SHA 不同。原执行版本和原转录未改写。

该批发现模型自由说明把一次截止月份复述为 8 月，结构化字段始终为 10 月。随后将完成摘要改为从结构化结果渲染，并新增回归测试；最终显示层仅对已有真实结果重新展示和恢复会话，没有重复整批收费决策。最新 `terminal-result.txt`、`readable-resume.txt` 不冒充原始终端输出；导出器版本与原执行版本分开记录。

这是小样例验证，不代表任意对话理解或模型选择都可靠。`/set` 提供不请求模型的精确需求输入方式；未实现 token 流式输出和崩溃业务任务续跑。
