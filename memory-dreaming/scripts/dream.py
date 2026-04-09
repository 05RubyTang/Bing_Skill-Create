#!/usr/bin/env python3
"""
dream.py — 轻量版 Dreaming 记忆巩固脚本

读取近期每日日志（memory/YYYY-MM-DD.md），
为 AI 代理提供结构化的候选内容和评分上下文，
由代理决定哪些内容值得提炼到 MEMORY.md。

用法：
  python3 dream.py [--days N] [--workspace PATH]

输出：
  JSON 到 stdout，包含候选条目和当前 MEMORY.md 摘要
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(description="轻量版 Dreaming 记忆分析")
    parser.add_argument("--days", type=int, default=7, help="回顾最近 N 天（默认 7）")
    parser.add_argument(
        "--workspace",
        type=str,
        default=os.path.expanduser("~/.openclaw/workspace"),
        help="工作区路径",
    )
    return parser.parse_args()


def load_daily_logs(workspace: Path, days: int) -> list[dict]:
    """加载最近 N 天的每日日志"""
    memory_dir = workspace / "memory"
    logs = []
    today = datetime.now()

    for i in range(days):
        date = today - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        log_path = memory_dir / f"{date_str}.md"

        if log_path.exists():
            content = log_path.read_text(encoding="utf-8")
            logs.append(
                {
                    "date": date_str,
                    "age_days": i,
                    "path": str(log_path),
                    "content": content,
                    "size": len(content),
                }
            )

    return logs


def load_extra_memory_files(workspace: Path) -> list[dict]:
    """加载非日期命名的记忆文件（常青文件）"""
    memory_dir = workspace / "memory"
    extras = []
    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}\.md$")

    if memory_dir.exists():
        for f in memory_dir.iterdir():
            if f.is_file() and f.suffix == ".md" and not date_pattern.match(f.name):
                content = f.read_text(encoding="utf-8")
                extras.append(
                    {
                        "name": f.name,
                        "path": str(f),
                        "content": content[:2000],  # 截断，仅供参考
                        "truncated": len(content) > 2000,
                    }
                )

    return extras


def load_memory_md(workspace: Path) -> dict:
    """加载当前 MEMORY.md"""
    memory_path = workspace / "MEMORY.md"
    if memory_path.exists():
        content = memory_path.read_text(encoding="utf-8")
        return {
            "exists": True,
            "path": str(memory_path),
            "content": content,
            "size": len(content),
        }
    return {"exists": False, "path": str(memory_path)}


def extract_sections(content: str) -> list[dict]:
    """提取 Markdown 二级标题段落"""
    sections = []
    lines = content.split("\n")
    current = None

    for line in lines:
        if line.startswith("## "):
            if current:
                sections.append(current)
            current = {"title": line[3:].strip(), "lines": []}
        elif current is not None:
            current["lines"].append(line)

    if current:
        sections.append(current)

    return [
        {
            "title": s["title"],
            "content": "\n".join(s["lines"]).strip(),
            "word_count": len(" ".join(s["lines"]).split()),
        }
        for s in sections
    ]


def score_candidate(log: dict) -> float:
    """
    简单评分：
    - 内容越长、越新，基础分越高
    - 有「重要」「关键」「教训」等关键词加分
    """
    base = min(log["size"] / 500, 3.0)  # 0~3 分，每 500 字 1 分
    recency = max(0, 1.0 - log["age_days"] * 0.1)  # 最近的权重高
    keywords = ["重要", "关键", "教训", "洞察", "发现", "Ruby", "确认", "决定", "结论"]
    keyword_hits = sum(1 for k in keywords if k in log["content"])
    keyword_score = min(keyword_hits * 0.15, 1.0)
    return round(base * recency + keyword_score, 3)


def main():
    args = parse_args()
    workspace = Path(args.workspace)

    if not workspace.exists():
        print(json.dumps({"error": f"工作区不存在: {workspace}"}), file=sys.stderr)
        sys.exit(1)

    # 加载数据
    daily_logs = load_daily_logs(workspace, args.days)
    extra_files = load_extra_memory_files(workspace)
    memory_md = load_memory_md(workspace)

    # 对每日日志评分
    candidates = []
    for log in daily_logs:
        score = score_candidate(log)
        sections = extract_sections(log["content"])
        candidates.append(
            {
                "date": log["date"],
                "age_days": log["age_days"],
                "score": score,
                "size": log["size"],
                "path": log["path"],
                "sections": sections,
                "content_preview": log["content"][:800],  # 前 800 字预览
                "full_content": log["content"],
            }
        )

    # 按评分排序
    candidates.sort(key=lambda x: x["score"], reverse=True)

    result = {
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "workspace": str(workspace),
        "days_reviewed": args.days,
        "daily_log_count": len(daily_logs),
        "candidates": candidates,
        "extra_memory_files": extra_files,
        "current_memory_md": memory_md,
        "instructions": (
            "请根据以上候选内容，判断哪些信息值得提炼到 MEMORY.md。"
            "评分仅供参考，最终由你判断。"
            "常青层（关于 Ruby 和核心机制）只在信息有实质更新时才修改；"
            "近期层按月回顾，值得留的升级为常青，过时的清除；"
            "工具层随时更新。"
        ),
    }

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
