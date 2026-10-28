"""Dependency-free terminal rendering; JSON remains available for automation."""
import re


TIERS = {"standard": "标准方案", "reuse": "素材复用方案", "minimal": "简化方案"}
ACTIONS = {"search_materials": "检索素材", "update_plan": "更新计划", "estimate_cost": "核算费用与时间",
           "generate_script": "生成脚本", "save_solution": "保存方案", "ask_user": "请求补充", "finish_task": "结束任务"}
FIELDS = {"theme": "主题", "budget_units": "预算", "deadline_at": "截止时间", "product_id": "商品",
          "audience": "受众", "platform": "平台", "language": "语言"}


def plain(value):
    text = re.sub(r"\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)", "", str(value))
    text = re.sub(r"\x1b\[[0-?]*[ -/]*[@-~]", "", text)
    return "".join(c for c in text if c in "\n\t" or ord(c) >= 32 and not 127 <= ord(c) <= 159)


def render_result(result, task=None):
    status = {"completed": "已完成", "needs_input": "等待补充", "incomplete": "未完成", "invalid_input": "输入有误", "running": "运行中"}
    lines = [f"\n结果：{status.get(result['status'], result['status'])}  |  模式：{result.get('mode', 'mock')}"]
    if result.get("replayed"):
        lines.append("本次回读已有任务，没有重新生成或执行工具。")
    if result.get("request_id"):
        lines.append("请求：" + result["request_id"])
    if task:
        lines.append("主题：" + task["theme"])
    if result.get("explanation"):
        lines.append(result["explanation"])
    if result.get("reason_code"):
        lines.append("原因码：" + result["reason_code"])
    plans = result.get("plan_versions") or []
    if plans:
        lines.append("方案调整：" + " → ".join(TIERS.get(p["tier"], p["tier"]) for p in plans))
    costs = result.get("costs") or {}
    estimate = costs.get("latest_estimate") or {}
    if estimate:
        lines.extend([f"模拟预算：{estimate['budget_units']}  |  方案总额：{estimate['projected_total_units']}",
                      f"  已发生：{costs['simulated_spent_units']}  |  资源预留：{estimate['planned_resource_units']}  |  剩余工具：{estimate['remaining_tool_units']}",
                      f"截止：{estimate['deadline_at']}  |  预计完成：{estimate['estimated_finish_at']}"])
        if not estimate["feasible"]:
            lines.append(f"缺口：预算 {estimate['budget_gap_units']}；时间 {estimate['time_gap_seconds']} 秒")
    solution = result.get("solution") or {}
    if solution.get("saved"):
        lines.append("保存：已提交 SQLite；回读核验" + ("通过" if solution.get("readback_verified") else "未通过"))
    for artifact in result.get("retained_artifacts") or []:
        lines.extend(["", "脚本：" + artifact["title"]])
        for index, segment in enumerate(artifact["segments"], 1):
            lines.append(f"  {index}. {segment['text']}  [来源：{', '.join(segment['source_ids'])}]")
        lines.append("  " + artifact["generation_note"])
    for question in result.get("questions") or []:
        lines.append("待补充：" + question)
    usage = result.get("provider_usage") or {}
    tokens = (usage.get("tokens") or {}).get("total_tokens")
    lines.append(f"本次任务 API：{usage.get('real_api_requests', 0)} 次" + (f"；{tokens} tokens" if tokens is not None else ""))
    lines.append("费用为合成业务模拟单位；API 账单另计。完成指方案与脚本保存，未制作或投放视频。")
    return plain("\n".join(lines))


def progress(event, stream):
    kind = event["kind"]
    if kind == "model_wait":
        text = f"[{event['step']}] 正在请求{'真实模型' if event['mode'] == 'real' else 'Mock'}选择动作…"
    elif kind == "decision":
        action = event["action"]
        text = "  → " + ACTIONS.get(action["name"], action["name"]) + "：" + action["summary"]
    elif kind == "action_result":
        if not event["ok"]:
            text = "  失败：" + event["error_code"] + "；" + event["summary"]
        elif event["tool"] == "estimate_cost":
            data = event["data"]
            text = f"  估算 {data['projected_total_units']} / 预算 {data['budget_units']}；" + ("可行" if data["feasible"] else f"不可行，预算缺口 {data['budget_gap_units']}，时间缺口 {data['time_gap_seconds']} 秒")
        else:
            text = "  已执行：" + ACTIONS.get(event["tool"], event["tool"]) + "；本步模拟费用 " + event["charged_units"]
    else:
        return
    print(plain(text), file=stream, flush=True)
