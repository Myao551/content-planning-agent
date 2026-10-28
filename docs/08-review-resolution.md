# 符合性审查修复回执

原审查见 [历史报告](06-compliance-review.md)。本回执更新处理状态，保留原审查作为历史基线。

## 技术修复

| 问题 | 处理 |
| --- | --- |
| 执行版本被导出时版本覆盖 | 新任务创建时固定 execution_version 并写入 SQLite；导出单独记录 exporter_version / exported_at |
| 旧任务缺少执行快照 | 标记 unknown_legacy、执行摘要为 null，不使用当前代码补写历史 |
| 同一 run_id 的回放版本不同 | 新格式回放原执行快照；回归测试模拟源码变化后重新导出并核对执行版本不变 |
| 文档和生成脚本仍声称真实模式未实现 | 明确区分本页离线结果与独立真实评估；同时修正生成器，避免下次 verify 覆盖回旧说法 |
| 早期网络错误被当作预算无解通过 | 历史报告已标记环境失败及 passed=false，不纳入模型行为成功统计 |
| 真实接入、配置和证据未提交 | 已在后续提交中纳入；目前支持通用 OpenAI 兼容接口与 .env |
| 个人信息与正式题号未知 | 用户确认稍后提供，列入提交清单，不编造 |

## 已完成的验证

自动化测试 72 项通过，14 组离线案例符合预期；安装包环境也通过 72 项测试。冻结提交后从新进程运行 `--require-clean --cases normal replan repeat`，三项检查均符合预期。

冻结实现提交：[`036a6db33bbec097591e5cfb7eda6876c13723e2`](https://github.com/Myao551/content-planning-agent/commit/036a6db33bbec097591e5cfb7eda6876c13723e2)。执行摘要：`f4fbda4435ad2e3753873477acf95db817ec8b9dcaeeb0b4fa787a8f90cc181e`。

| 检查 | 结果 |
| --- | --- |
| 正常真实规划 | completed，保存和回读成功 |
| 真实预算重规划 | 观察标准方案 12 后改为复用 8，completed |
| 原任务回放 | 原执行快照逐字段相同；新增 API 请求为 0 |
| 执行与导出版本 | execution_version 固定，exporter_version / exported_at 单独记录 |
| 冻结实现一致性 | 实现、数据、脚本、测试与依赖无变更；源码摘要与两条执行记录一致 |

实际记录：[真实批次报告](../examples/real/81a3428d-5d8f-4c76-a66f-53e24b94b1d5/report.json)、[可读案例索引](../examples/real/README.md)、[逐项版本一致性检查](../examples/provenance-regression.json)。

本次新增真实 API 请求 18 次、96494 token，未查询实际账单金额。repeat 的 wall_seconds 是来源运行的时间，不用作本次回放延迟。没有重跑全部历史真实场景；原故障案例仍是历史行为证据，不宣称为本次同版本回归。

最终证据提交可以晚于冻结代码提交；证据和文档变化不改变实现摘要。最终提交 SHA 从 `git rev-parse HEAD` 获取，官方题号和本人记录仍待提供。

## 解释边界

- 新元信息 v2 的顶层 implementation_hash 指执行时源码快照；Python/依赖版本也来自执行快照。
- exporter_version 描述导出器；它可以比执行版本更新。
- git_dirty 检查实现、数据、脚本、测试与依赖；git_worktree_dirty 描述完整工作区，新增证据文件可能使后者为 true。
- 历史 v1 记录未回填为当前执行版本。旧真实记录仍有参考价值，但不能当作最终代码的同版本回归。
- 本人贡献、用时和官方题号仍待提供，详见 [正式提交清单](07-submission.md)。
