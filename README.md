# Content Planning Agent

跨境电商营销视频内容活动规划助手。接收主题、预算和截止时间，执行素材检索、脚本生成、成本估算和方案保存；观察工具结果后继续、调整方案、有限重试或明确停止。

**当前状态：已接通阿里百炼 `qwen3.8-flash`，正常规划、预算重规划和工具失败处理的真实模型路径已运行通过。** 同时保留无需密钥的确定性 Mock 入口。业务素材、费用与保存工具是本地合成实现，未接真实视频服务。结果、限制和用量见 [真实 API 评估](docs/06-real-api-evaluation.md)。

## 安装与快速运行

要求 Python 3.12+，本次验证环境为 Python 3.12.14。先在仓库根目录安装依赖；首次安装需要访问包源，安装后业务运行与测试不访问网络。

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pip install --no-build-isolation --no-deps -e .

python -m pytest -q
python -m content_planner run --mode mock --input examples/inputs/01-normal.json --demo-config examples/inputs/demo-config.json --db .runtime/demo.db --output-dir .runtime/demo-output
```

示例配置将业务时钟固定在 `2030-01-01T10:00:00+08:00`，因此长期可复现；无 `--demo-config` 时使用实际时间。模拟业务耗时只推进时间游标，不实际等待。

查看、回放和导出同一任务：

```bash
python -m content_planner inspect --request-id 01-normal --db .runtime/demo.db
python -m content_planner run --mode mock --input examples/inputs/01-normal.json --demo-config examples/inputs/demo-config.json --db .runtime/demo.db
python -m content_planner export --request-id 01-normal --db .runtime/demo.db --output-dir .runtime/export
```

第二次相同请求返回 `replayed=true`，不增加工具记录、模拟费用或驱动调用。修改主题、预算等输入时使用新 `request_id`；相同标识对应不同输入会返回冲突。尚未完成的请求只回放已有结果，本阶段没有跨进程续跑命令。

预算调整与故障示例：

```bash
python -m content_planner run --mode mock --input examples/inputs/04-budget-replan.json --demo-config examples/inputs/demo-config.json --db .runtime/demo.db
python -m content_planner run --mode mock --input examples/inputs/06-tool-failure.json --demo-config examples/inputs/06-tool-failure.demo.json --db .runtime/demo.db
```

stdout 为 JSON，证据目录提示写入 stderr。退出码：`0` 完成；`2` 需补信息；`3` 业务未完成；`4` 输入错误/请求冲突；`5` 配置错误或真实模式尚未接入。预期业务失败案例返回非零码属于正确行为。

## 最短评审路径

| 检查内容 | 入口 |
| --- | --- |
| 用户、范围、成功标准 | [需求](docs/01-requirements.md) |
| 调用链、约束、状态和技术取舍 | [方案](docs/02-solution.md) |
| 测试结果及每例实际输出/Trace | [评估](docs/03-evaluation.md)、[案例索引](examples/README.md) |
| 真实模型路径、用量与观察到的问题 | [真实 API 评估](docs/06-real-api-evaluation.md)、[真实记录](examples/real/README.md) |
| AI 辅助范围和验证边界 | [AI 使用](docs/04-ai-usage.md) |
| 已解决问题、限制和下一步 | [复盘](docs/05-retrospective.md) |
| 原始技术规划与阶段调整 | [开发方案](docs/00-development-plan.md) |

重新执行测试并生成一批新的实际证据：

```bash
python scripts/verify.py
```

该命令更新测试结果、案例索引和评估文档；每批运行使用新的本地数据库，证据按运行 ID 保存。普通 `pytest` 使用临时目录，不修改已提交案例。

## 真实百炼模型运行

支持阿里导出的纵向字段/值 CSV，自动读取其中的 `apiKey` 与 `openAiCompatible`。密钥只在内存中使用，不进入任务、Trace 或请求日志。CSV 和 `.env` 均应保留在本地。

```bash
# 使用未来的真实截止时间、新 request_id；真实模式不接受固定演示时钟
python -m content_planner run --mode real --model qwen3.8-flash --api-key-file /path/to/local-export.csv --input /path/to/real-request.json --db .runtime/real.db --output-dir .runtime/real-output

# 有请求次数和累计 token 停止阈值的真实评估；会产生实际 API 用量
python scripts/evaluate_real.py --api-key-file /path/to/local-export.csv --model qwen3.8-flash
```

也可使用进程环境变量 `DASHSCOPE_API_KEY` 和 `DASHSCOPE_BASE_URL`，程序不会自动加载 `.env`。目前验证的是千问非思考模式，其他供应商参数未适配。HTTP 失败不自动重试、换模型或回退 Mock。状态相同但运行模式/模型配置不同的请求标识会被拒绝复用。

真实评估每个用例后检查累计用量；达到阈值时跳过后续收费案例，仍可验证无需 API 的缺参数和历史回放。阈值不是供应商账单硬限额，最后一个用例可能使累计量略超阈值。实际金额与免费额度扣减没有查询，以供应商账单为准。

## 技术与业务边界

- Python 原生单 Agent 循环、Pydantic 2、argparse、SQLite，依赖版本在 `requirements.txt` 固定。
- Mock 根据当前状态和工具返回选择动作，只用于离线验证；真实适配器通过百炼 HTTP 原生 Function Calling 选择工具并回传调用结果，无需模型 SDK。
- 计划可以在标准、复用、简化三个档位间调整；素材前置条件、费用和时间由程序校验。
- 预算总额 = 已发生模拟费用 + 剩余工具费用 + 最终方案资源预留。资源预留尚未支付；真实 API 用量单独统计，不与模拟单位相加。
- `completed` 仅指方案和脚本已通过约束检查并保存、回读成功，不代表视频已制作或广告已投放。
- SQLite 事务保护本地结果与账本，运行上限防止循环；不提供生产级并发、分布式执行或崩溃后自动恢复。
- 当前脚本采用严格事实引用：Mock 或真实模型都须逐条引用给定事实，不具备已验证的开放式创意生成、翻译或转化效果能力。

主要目录为 `src/`、`tests/`、`data/`、`examples/`、`docs/` 和 `scripts/`。合成数据随 Python 包分发，安装后从其他工作目录也能运行。

## 仓库与提交

目标仓库：[Myao551/content-planning-agent](https://github.com/Myao551/content-planning-agent)。材料组织参考 [项目交付示例](https://github.com/lwz1357/agent-campus-submission-example)。题目原文、公司参考 PDF、密钥、虚拟环境和运行数据库保留在本地；合成数据及实际验证材料纳入版本管理。

已保留不同真实执行路径；正式笔试提交仍需候选人据实补充个人贡献、个人用时与解释，并提交正式题号、仓库 URL 和最终 commit SHA。小样例通过不代表未测场景都可靠。
