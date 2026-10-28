# Content Planning Agent

跨境电商营销视频内容活动规划助手。接收主题、预算和截止时间，执行素材检索、脚本生成、成本估算和方案保存；观察工具结果后继续、调整方案、有限重试或明确停止。

**当前状态：支持持续对话 CLI、易读终端输出、通用 OpenAI 兼容 Chat Completions 接口和 `.env` 配置；已有阿里百炼 `qwen3.8-flash` 的真实任务记录。** 同时保留无需密钥的 Mock。其他服务商的真实可用性需以自己的验证结果为准，已有记录见 [真实 API 评估](docs/06-real-api-evaluation.md)。

## 直接开始持续对话（推荐）

在项目根目录执行。当前本地环境已有 `.venv` 和 `.env`；首次克隆的使用者先完成下方安装与配置。

```bash
source .venv/bin/activate
python -m content_planner chat --mode real
# 安装时也注册了等价的短命令：content-planner chat --mode real
```

启动后可以持续输入，不需要自己编写 JSON，也不需要每句话重启程序：

```text
你 > 帮我给通勤人群策划咖啡杯新品营销活动
助手会请求补充预算和截止时间。
你 > 预算10，一小时后截止
助手执行工具，逐步显示检索、估算、调整方案、生成及保存结果。
你 > 为什么选择这个方案？
助手结合最近结果解释。
你 > 预算改成6，其他要求不变
助手保留主题和截止时间，创建新任务重新规划。
你 > /status
你 > /exit
```

上面是输入方式说明，不是伪造的真实模型实测输出。真实模式读取当前目录 `.env`，自然语言理解、解释和规划均可能产生 API 用量；启动本身不调用模型。模型可能因超时、结构化输出错误或执行上限而未完成，终端会明确显示。

想先检查交互体验且不消耗 API：

```bash
python -m content_planner chat --mode mock
```

Mock 支持上述例子的主题、预算和“一小时后”等简单规则；不是通用聊天模型。精确控制时，两种模式都可使用下面的本地命令，`/set` 不调用模型：

```text
/set theme 给通勤人群策划便携咖啡杯营销活动
/set product P001
/set budget 10
/set deadline +1h
/run
```

### 会话、结果与常用命令

终端展示中文状态、方案调整过程、模拟预算与预留、脚本及素材来源、保存核验和 API 用量。完整任务结果仍以 JSON 保存，业务 Trace 不受显示方式影响。

| 命令 | 用途 |
| --- | --- |
| `/help` | 查看完整命令 |
| `/products` | 查看本地合成商品和事实；当前有 P001 咖啡杯、P002 收纳盒 |
| `/draft` | 查看已记住的主题、预算、截止时间等需求 |
| `/set budget 6`、`/set deadline +1h` | 精确修改需求，随后 `/run` 执行 |
| `/run` | 执行当前需求；相同输入回读最近任务，不重复生成或扣费 |
| `/status`、`/json` | 查看最近任务的易读结果或完整 JSON，不调用 API |
| `/history`、`/export` | 查看最近对话；导出完整会话及最近任务证据 |
| `/new` | 清空当前需求，开始新任务；旧任务和对话保留 |
| `/exit` | 保存并退出，也可用 Ctrl+D；Ctrl+C 会停止当前输入或执行 |

启动时会显示会话 ID 和继续会话的命令。例如真实会话默认保存在 `.runtime/chat-real.db`：

```bash
# 将 <会话ID> 替换为启动时显示的实际值
python -m content_planner chat --mode real --session <会话ID>
```

会话恢复包括对话、当前需求、最近任务和累计 API 用量；不自动恢复被中断的业务任务。`/run` 相同输入只回读原终态，若需新的尝试，用 `/new` 重新填写需求。更换模式或模型配置应使用新会话。自定义 `--db` / `--env-file` 时，恢复时继续传入相同参数。

**预算按任务独立计算。** 修改需求会创建新任务并重新执行，旧任务的产物和费用记录保留，原任务费用不会转移或扣进新任务预算；会话累计 API 包括对话理解和所有任务请求。模拟业务预算与真实 API 账单分开，未查询实际收费。`/run` 不调用对话理解；重复自然语言会产生一次理解请求，即使业务结果随后回放。

任务执行后自动导出至 `.runtime/chat-output/<run_id>/`；`/export` 另写 `.runtime/chat-output/<会话ID>/session.json` 和最近任务证据。会话数据库与这些本地产物默认不提交。

本次持续对话真实验证与 82 项测试结果见 [交互验证记录](examples/chat/README.md)，包括预算修改、重复回放及会话恢复。终端完成摘要采用结构化字段；模型完整说明保留在 JSON 中。

当前提供的是内容规划业务对话，支持持续澄清、修改和解释；没有代码终端工具、通用文件编辑或已验证的任意聊天能力。输入为逐行文本，当前不做 token 流式输出；执行过程中逐步显示公开动作和工具回执，可用 `--quiet` 隐藏进度。

## 单次运行与 JSON 输出

`run` / `inspect` / `export` 继续保留，适合批量验证。实际终端默认显示易读摘要，重定向或管道默认输出 JSON；可用 `--format text` / `--format json` 明确指定。JSON 模式不混入进度文字，证据路径写入 stderr。

不用准备输入文件的离线例子：

```bash
python -m content_planner run --mode mock   --input examples/inputs/01-normal.json   --demo-config examples/inputs/demo-config.json   --db .runtime/demo.db --format text
```

真实单次任务需要自定义 JSON，使用新的请求 ID 和带时区的未来截止时间：

```json
{
  "request_id": "my-first-campaign-001",
  "theme": "给通勤人群策划便携咖啡杯新品营销活动",
  "product_id": "P001",
  "budget_units": "10.000",
  "deadline_at": "2030-01-01T18:00:00+08:00",
  "audience": "通勤人群"
}
```

将上面内容保存为 `.runtime/my-request.json`，把截止时间改成你需要的未来时间，然后执行：

```bash
python -m content_planner run --mode real --input .runtime/my-request.json   --db .runtime/real.db --output-dir .runtime/real-output --format text
# 若由脚本消费结果：改用 --format json，或将 stdout 重定向到文件
```

重复使用相同请求 ID 和输入会回读已有任务；更改已执行的 JSON 时需要新 ID，否则返回 `request_conflict`。真实任务默认上限 180 秒，单次 HTTP 请求最长 30 秒，没有隐藏重试或自动回退 Mock。

### 常见情况

| 现象 | 处理 |
| --- | --- |
| `No module named content_planner` | 激活 `.venv`，并完成下方可编辑安装 |
| `configuration_error` | 从仓库根目录运行，检查 `.env` 三个必填项；环境变量会覆盖文件 |
| 提示补充信息 | 在同一会话继续提供预算、截止时间、商品等；用 `/draft` 核对 |
| `deadline_exceeded` | 用 `/set deadline +1h` 设置未来时间，再 `/run` |
| `incomplete` | 查看原因和证据，已有产物不代表方案已保存；有保存回执才显示完成 |
| 重复显示旧结果 | 相同输入按幂等规则回读；新尝试可 `/new` 后重新填写 |

## 安装与快速运行

要求 Python 3.12+，本次验证环境为 Python 3.12.14。首次安装需要访问包源；安装后的 Mock 运行与自动化测试不联网，真实模式需要访问配置的模型接口。

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

输出格式按终端自动选择，也可显式指定；证据目录提示写入 stderr。退出码：`0` 完成；`2` 需补信息；`3` 业务未完成；`4` 输入错误/请求冲突；`5` 配置错误。预期业务失败案例返回非零码属于正确行为。

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
| 审查问题的修复与验证边界 | [修复回执](docs/08-review-resolution.md) |
| 持续对话、易读输出和实际试用 | [交互扩展](docs/09-cli-conversation.md)、[验证记录](examples/chat/README.md) |
| 正式提交信息和本人待确认项 | [提交清单](docs/07-submission.md) |

重新执行测试并生成一批新的实际证据：

```bash
python scripts/verify.py
```

该命令更新测试结果、案例索引和评估文档；每批运行使用新的本地数据库，证据按运行 ID 保存。普通 `pytest` 使用临时目录，不修改已提交案例。

## 填入自己的 API 配置并验证

首次配置时，在仓库根目录复制模板；已有 `.env` 时跳过复制，以保留原配置：

```bash
cp .env.example .env
```

编辑 `.env`，填写自己的配置，不限百炼域名或千问模型：

```dotenv
OPENAI_API_KEY=你的密钥
OPENAI_BASE_URL=https://你的服务商地址/v1
OPENAI_MODEL=你的模型名称
OPENAI_EXTRA_BODY={}
```

接口和模型需要支持 **Chat Completions、原生 function/tool calling 和 JSON 对象输出**。仅兼容普通文字聊天不够；此入口不是 Responses API。支持任意服务商 HTTPS 地址，以及 localhost / 回环 HTTP 本地服务。本地服务无需鉴权时可填写非空占位密钥。

从项目根目录执行，不再需要 CSV：

```bash
# 最小连接检查，只发一个很小的真实请求
python scripts/probe_api.py
# 完整 Agent 单例，自动产生新请求 ID 和未来截止时间
python scripts/evaluate_real.py --cases normal
# 全部真实评估，会产生 API 用量，有累计用量停止阈值
python scripts/evaluate_real.py
```

自定义输入：

```bash
python -m content_planner run --mode real --input /path/to/real-request.json --db .runtime/real.db --output-dir .runtime/real-output
```

输入使用未来真实截止时间和新 `request_id`。真实模式不允许固定演示时钟。

配置优先级：默认只读取当前工作目录的 `.env`，不搜索父目录；可用 `--env-file /path/to/config.env` 指定。进程环境覆盖 `.env` 同名值，`--model` / `--base-url` 再覆盖相应设置。读取不会修改进程环境。

`OPENAI_EXTRA_BODY` 用于显式传厂商扩展，默认不发送百炼特有参数。例如千问可填 `OPENAI_EXTRA_BODY='{"enable_thinking":false}'`。不同平台对通用参数的支持仍需验证，没有承诺所有标为“OpenAI 兼容”的模型都已实测。

旧 CSV 入口仍可用：`--api-key-file /path/to/local-export.csv` 优先提供密钥和地址。没有通用设置时兼容旧 `DASHSCOPE_*` 配置。HTTP 失败不会自动换模型或回退 Mock；运行模式/模型配置不同的请求 ID 会被拒绝复用。

`.env` 仅保留本地，受 Git 忽略；仓库只提交空密钥模板。密钥不会进入任务、Trace 或请求日志。

真实评估每个用例后检查累计用量；达到阈值时跳过后续收费案例，仍可验证无需 API 的缺参数和历史回放。阈值不是供应商账单硬限额，最后一个用例可能使累计量略超阈值。实际金额与免费额度扣减没有查询，以供应商账单为准。

正式回归建议在提交实现代码后运行 `python scripts/evaluate_real.py --require-clean --cases normal replan repeat`。新任务固定保存执行版本，导出器版本另记；旧任务缺快照时明确标记未知，不将当前源码摘要附着到旧轨迹。历史元信息与新格式的区别见 [版本说明](examples/provenance-notes.json)。

## 技术与业务边界

- Python 原生单 Agent 循环、Pydantic 2、argparse、SQLite，依赖版本在 `requirements.txt` 固定。
- Mock 只用于离线验证；通用 HTTP 适配器通过 OpenAI 兼容工具调用工作，不绑定模型名前缀，厂商扩展由配置显式提供，无需模型 SDK。
- 计划可以在标准、复用、简化三个档位间调整；素材前置条件、费用和时间由程序校验。
- 预算总额 = 已发生模拟费用 + 剩余工具费用 + 最终方案资源预留。资源预留尚未支付；真实 API 用量单独统计，不与模拟单位相加。
- `completed` 仅指方案和脚本已通过约束检查并保存、回读成功，不代表视频已制作或广告已投放。
- SQLite 事务保护本地结果与账本，运行上限防止循环；不提供生产级并发、分布式执行或崩溃后自动恢复。
- 当前脚本采用严格事实引用：Mock 或真实模型都须逐条引用给定事实，不具备已验证的开放式创意生成、翻译或转化效果能力。

主要目录为 `src/`、`tests/`、`data/`、`examples/`、`docs/` 和 `scripts/`。合成数据随 Python 包分发，安装后从其他工作目录也能运行。

## 仓库与提交

目标仓库：[Myao551/content-planning-agent](https://github.com/Myao551/content-planning-agent)。材料组织参考 [项目交付示例](https://github.com/lwz1357/agent-campus-submission-example)。题目原文、公司参考 PDF、密钥、虚拟环境和运行数据库保留在本地；合成数据及实际验证材料纳入版本管理。

已保留不同真实执行路径；正式笔试提交仍需候选人据实补充个人贡献、个人用时与解释，并提交正式题号、仓库 URL 和最终 commit SHA。小样例通过不代表未测场景都可靠。
