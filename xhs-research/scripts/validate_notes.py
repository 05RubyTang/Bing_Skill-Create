#!/usr/bin/env python3
"""
小红书笔记数据校验工具
在 Agent 将 browser evaluate 提取的笔记数据写入报告前，调用此脚本做格式校验。

用法：
  python validate_notes.py --data /tmp/xhs_notes.json
  python validate_notes.py --data /tmp/xhs_notes.json --strict

输出：
  - 标准输出：每条笔记的校验结果（PASS / WARN / FAIL）
  - 退出码：0=全部通过，1=有警告，2=有严重错误
"""

import argparse
import json
import re
import sys
from urllib.parse import urlparse


# ── 校验规则常量 ──────────────────────────────────────────────────────────────

NOTE_ID_PATTERN = re.compile(r'^[0-9a-f]{16,32}$')

VALID_COVER_DOMAINS = (
    "sns-webpic-qc.xhscdn.com",
    "sns-webpic.xhscdn.com",
    "ci.xiaohongshu.com",
)
INVALID_COVER_DOMAINS = (
    "sns-avatar-qc.xhscdn.com",
    "sns-avatar.xhscdn.com",
    "picasso-static.xiaohongshu.com",
)
COVER_REQUIRED_KEYWORDS = ("webpic", "spectrum", "/note/")


# ── 单条笔记校验 ──────────────────────────────────────────────────────────────

def validate_note_id(note_id: str) -> tuple[bool, str]:
    """校验 noteId 格式"""
    if not note_id:
        return False, "noteId 为空"
    if not NOTE_ID_PATTERN.match(note_id):
        return False, f"noteId 格式错误（应为16-32位十六进制字符串）: {note_id!r}"
    return True, "OK"


def validate_explore_url(url: str, note_id: str) -> tuple[bool, str]:
    """校验 explore 链接格式及与 noteId 的一致性"""
    if not url:
        return False, "exploreUrl 为空"
    expected = f"https://www.xiaohongshu.com/explore/{note_id}"
    if url != expected:
        return False, f"exploreUrl 与 noteId 不匹配: {url!r} != {expected!r}"
    return True, "OK"


def validate_cover_img(cover_img: str) -> tuple[str, str]:
    """
    校验封面图 URL。
    返回 ("PASS"|"WARN"|"FAIL", 说明)
    """
    if not cover_img:
        return "WARN", "coverImg 为空（报告将使用渐变色块降级展示）"

    # base64 占位图
    if cover_img.startswith("data:"):
        return "FAIL", "coverImg 是 base64 占位图，页面可能未完全渲染"

    parsed = urlparse(cover_img)
    domain = parsed.netloc

    # 明确禁止的域名
    for bad in INVALID_COVER_DOMAINS:
        if bad in domain:
            return "FAIL", f"coverImg 来自禁止域名（头像/静态资源）: {domain}"

    # 必须来自合法 CDN
    is_valid_domain = any(good in domain for good in VALID_COVER_DOMAINS)
    has_valid_keyword = any(kw in cover_img for kw in COVER_REQUIRED_KEYWORDS)

    if not is_valid_domain and not has_valid_keyword:
        return "FAIL", f"coverImg 不是有效的小红书笔记封面 CDN 地址: {cover_img[:80]}"

    # 包含 query 参数警告（可能带 token）
    if parsed.query:
        return "WARN", f"coverImg 含 query 参数（建议去除 ?{parsed.query[:40]}...）"

    return "PASS", "OK"


def validate_note(note: dict, index: int) -> dict:
    """校验单条笔记，返回结构化结果"""
    note_id = note.get("noteId", "")
    explore_url = note.get("exploreUrl", "")
    cover_img = note.get("coverImg", "")

    errors = []
    warnings = []

    # 1. noteId
    ok, msg = validate_note_id(note_id)
    if not ok:
        errors.append(f"[noteId] {msg}")

    # 2. exploreUrl
    if note_id:  # noteId 合法时才校验 URL 一致性
        ok, msg = validate_explore_url(explore_url, note_id)
        if not ok:
            errors.append(f"[exploreUrl] {msg}")
    elif explore_url:
        errors.append("[exploreUrl] noteId 无效，无法验证 URL 一致性")

    # 3. coverImg
    level, msg = validate_cover_img(cover_img)
    if level == "FAIL":
        errors.append(f"[coverImg] {msg}")
    elif level == "WARN":
        warnings.append(f"[coverImg] {msg}")

    # 4. 基本字段完整性（非强制，只警告）
    for field in ("title", "likes"):
        if not note.get(field):
            warnings.append(f"[{field}] 字段缺失或为空")

    status = "FAIL" if errors else ("WARN" if warnings else "PASS")
    return {
        "index": index + 1,
        "noteId": note_id or "(空)",
        "status": status,
        "errors": errors,
        "warnings": warnings,
    }


# ── 主流程 ────────────────────────────────────────────────────────────────────

def print_result(r: dict, verbose: bool = True):
    icon = {"PASS": "✅", "WARN": "⚠️ ", "FAIL": "❌"}.get(r["status"], "?")
    print(f"{icon} [{r['index']:02d}] noteId={r['noteId'][:24]}  →  {r['status']}")
    if verbose:
        for e in r["errors"]:
            print(f"       🔴 {e}")
        for w in r["warnings"]:
            print(f"       🟡 {w}")


def main():
    parser = argparse.ArgumentParser(description="小红书笔记数据校验工具")
    parser.add_argument("--data", required=True, help="笔记 JSON 文件路径（数组格式）")
    parser.add_argument("--strict", action="store_true", help="严格模式：警告也视为失败")
    parser.add_argument("--quiet", action="store_true", help="静默模式：只输出汇总")
    args = parser.parse_args()

    with open(args.data, "r", encoding="utf-8") as f:
        notes = json.load(f)

    if isinstance(notes, dict):
        # 兼容 {notes: [...]} 格式
        notes = notes.get("notes", notes.get("results", [notes]))

    print(f"\n📋 共 {len(notes)} 条笔记待校验\n{'─' * 50}")

    results = [validate_note(n, i) for i, n in enumerate(notes)]

    pass_count = sum(1 for r in results if r["status"] == "PASS")
    warn_count = sum(1 for r in results if r["status"] == "WARN")
    fail_count = sum(1 for r in results if r["status"] == "FAIL")

    for r in results:
        print_result(r, verbose=not args.quiet)

    print(f"\n{'─' * 50}")
    print(f"汇总：✅ {pass_count} 通过  ⚠️  {warn_count} 警告  ❌ {fail_count} 失败")

    # 输出适合 Agent 读取的结构化汇总
    summary = {
        "total": len(notes),
        "pass": pass_count,
        "warn": warn_count,
        "fail": fail_count,
        "ok_to_proceed": fail_count == 0 and (warn_count == 0 if args.strict else True),
        "failed_ids": [r["noteId"] for r in results if r["status"] == "FAIL"],
        "warned_ids": [r["noteId"] for r in results if r["status"] == "WARN"],
    }
    print(f"\n📊 机器可读汇总:\n{json.dumps(summary, ensure_ascii=False, indent=2)}")

    if fail_count > 0:
        print("\n🚫 存在严重错误，禁止将上述笔记写入报告！")
        return 2
    if args.strict and warn_count > 0:
        print("\n⚠️  严格模式：存在警告，请处理后再生成报告。")
        return 1
    print("\n✅ 校验通过，可安全生成报告。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
