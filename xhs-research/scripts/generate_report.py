#!/usr/bin/env python3
"""
小红书调研报告 HTML 生成脚本
输入分析数据 JSON，生成美观的 HTML 报告
"""

import argparse
import json
import sys
import os
from datetime import datetime


HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>小红书调研报告 · {keyword}</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", Arial, sans-serif; background: #f5f5f5; color: #333; }}
  
  /* Header */
  .header {{
    background: linear-gradient(135deg, #ff2442 0%, #ff6b6b 50%, #ff8e53 100%);
    color: white; padding: 32px 24px 28px; position: relative; overflow: hidden;
  }}
  .header::before {{
    content: ''; position: absolute; top: -50%; right: -10%; width: 60%; height: 200%;
    background: rgba(255,255,255,0.05); border-radius: 50%; transform: rotate(-15deg);
  }}
  .header-tag {{
    display: inline-block; background: rgba(255,255,255,0.2); border-radius: 12px;
    padding: 3px 10px; font-size: 12px; margin-bottom: 12px; backdrop-filter: blur(10px);
  }}
  .header h1 {{ font-size: 26px; font-weight: 700; margin-bottom: 6px; line-height: 1.2; }}
  .header-meta {{ font-size: 12px; opacity: 0.8; margin-bottom: 20px; }}
  .header-stats {{ display: flex; gap: 28px; }}
  .stat {{ text-align: center; }}
  .stat-num {{ font-size: 28px; font-weight: 800; line-height: 1; }}
  .stat-label {{ font-size: 11px; opacity: 0.8; margin-top: 3px; }}
  
  /* Cards */
  .section {{ background: white; margin: 12px 12px; border-radius: 16px; padding: 20px; box-shadow: 0 2px 12px rgba(0,0,0,0.06); }}
  .section-title {{ font-size: 16px; font-weight: 700; margin-bottom: 16px; display: flex; align-items: center; gap: 6px; }}
  .section-title::before {{ content: ''; width: 3px; height: 16px; background: #ff2442; border-radius: 2px; display: inline-block; }}
  
  /* Overview Grid */
  .overview-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
  .overview-card {{
    background: #fafafa; border-radius: 10px; padding: 12px;
    border: 1px solid #f0f0f0;
  }}
  .overview-label {{ font-size: 11px; color: #999; margin-bottom: 4px; }}
  .overview-value {{ font-size: 20px; font-weight: 800; color: #ff2442; line-height: 1.1; }}
  .overview-desc {{ font-size: 11px; color: #666; margin-top: 3px; }}
  
  /* Keyword Heat */
  .keyword-item {{ margin-bottom: 12px; }}
  .keyword-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px; }}
  .keyword-name {{ font-size: 13px; font-weight: 500; }}
  .keyword-stars {{ color: #ff2442; font-size: 13px; letter-spacing: 1px; }}
  .keyword-bar-bg {{ height: 6px; background: #f0f0f0; border-radius: 3px; overflow: hidden; }}
  .keyword-bar {{ height: 100%; background: linear-gradient(90deg, #ff2442, #ff8e53); border-radius: 3px; transition: width 0.3s; }}
  
  /* Notes */
  .note-card {{ border-bottom: 1px solid #f5f5f5; padding: 14px 0; }}
  .note-card:last-child {{ border-bottom: none; padding-bottom: 0; }}
  .note-rank {{ font-size: 20px; font-weight: 900; color: #ff2442; margin-bottom: 6px; }}
  .note-rank.rank-1 {{ color: #ff2442; }}
  .note-rank.rank-2 {{ color: #ff7043; }}
  .note-rank.rank-3 {{ color: #ffa000; }}
  .note-rank.rank-other {{ color: #ccc; font-size: 16px; }}
  
  /* Note cover image */
  .note-cover {{ width: 100%; height: 160px; overflow: hidden; position: relative; border-radius: 10px; margin-bottom: 10px; }}
  .note-cover img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
  .note-cover-fallback {{ width: 100%; height: 100px; border-radius: 10px; margin-bottom: 10px; background: linear-gradient(135deg, #FF6B81, #FF2442); display: flex; align-items: center; justify-content: center; font-size: 36px; }}
  .note-cover-badge {{ position: absolute; top: 8px; right: 8px; z-index: 2; background: rgba(255,36,66,0.85); color: white; font-size: 11px; padding: 2px 8px; border-radius: 8px; backdrop-filter: blur(4px); }}

  .note-title {{ font-size: 14px; font-weight: 600; line-height: 1.4; margin-bottom: 4px; }}
  .note-desc {{ font-size: 12px; color: #666; line-height: 1.5; margin-bottom: 8px; }}
  .note-meta {{ display: flex; gap: 12px; align-items: center; }}
  .note-tag {{ font-size: 11px; color: #ff2442; background: #fff0f2; border-radius: 4px; padding: 2px 7px; }}
  .note-tag.blue {{ color: #4e89e8; background: #f0f4ff; }}
  .note-tag.green {{ color: #2e8b57; background: #f0fff4; }}
  .note-stat {{ font-size: 11px; color: #999; }}
  .note-heart {{ color: #ff2442; }}
  .note-link {{ color: inherit; text-decoration: none; font-weight: 600; }}
  .note-link:hover {{ color: #ff2442; text-decoration: underline; }}
  .note-author-line {{ margin-bottom: 5px; }}
  .note-author {{ font-size: 11px; color: #999; text-decoration: none; }}
  .note-author:hover {{ color: #ff2442; }}
  .creator-link {{ color: #ff2442; text-decoration: none; font-size: 13px; font-weight: 600; }}
  .creator-link:hover {{ text-decoration: underline; }}
  .creator-name-row {{ display: flex; align-items: center; gap: 6px; justify-content: center; margin-bottom: 4px; }}
  .creator-name-plain {{ font-size: 13px; color: #666; }}
  .creator-fans {{ font-size: 11px; color: #999; background: #f5f5f5; padding: 1px 6px; border-radius: 10px; white-space: nowrap; }}
  .creator-topics {{ margin-top: 12px; text-align: left; }}
  .creator-topics-title {{ font-size: 11px; font-weight: 600; color: #ff2442; margin-bottom: 6px; text-transform: uppercase; letter-spacing: 0.5px; }}
  .creator-topics-list {{ list-style: none; padding: 0; margin: 0; }}
  .creator-topics-list li {{ font-size: 11px; color: #555; padding: 3px 0; border-bottom: 1px dashed #f0f0f0; line-height: 1.4; }}
  .creator-topics-list li:last-child {{ border-bottom: none; }}
  
  /* Creator types */
  .creator-grid {{ display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; }}
  .creator-card {{ background: #fafafa; border-radius: 10px; padding: 12px; text-align: center; border: 1px solid #f0f0f0; }}
  .creator-emoji {{ font-size: 22px; margin-bottom: 6px; }}
  .creator-type {{ font-size: 12px; font-weight: 700; margin-bottom: 4px; }}
  .creator-names {{ font-size: 11px; color: #999; line-height: 1.5; }}
  .creator-desc {{ font-size: 11px; color: #666; margin-top: 6px; line-height: 1.4; }}
  
  /* Comments */
  .comments-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
  .comment-card {{
    background: #fafafa; border-radius: 10px; padding: 12px;
    border-left: 3px solid #e0e0e0; border: 1px solid #f0f0f0;
  }}
  .comment-text {{ font-size: 12px; color: #444; line-height: 1.6; margin-bottom: 6px; }}
  .comment-text::before {{ content: '"'; color: #ff2442; font-size: 18px; line-height: 0; vertical-align: -4px; margin-right: 2px; }}
  .comment-source {{ font-size: 10px; color: #aaa; }}
  
  /* Needs */
  .needs-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
  .needs-card {{ border-radius: 12px; padding: 14px; }}
  .needs-card.green {{ background: #f0fff8; border: 1px solid #c6f6e0; }}
  .needs-card.orange {{ background: #fff8f0; border: 1px solid #fde8c8; }}
  .needs-title {{ font-size: 13px; font-weight: 700; margin-bottom: 10px; }}
  .needs-title.green {{ color: #2e8b57; }}
  .needs-title.orange {{ color: #e07000; }}
  .need-item {{ display: flex; gap: 6px; margin-bottom: 7px; font-size: 12px; line-height: 1.4; }}
  .need-icon {{ flex-shrink: 0; font-size: 13px; }}
  
  /* Insights */
  .insight-item {{ display: flex; gap: 12px; padding: 14px; background: #fafafa; border-radius: 10px; margin-bottom: 10px; border: 1px solid #f0f0f0; }}
  .insight-num {{ 
    width: 28px; height: 28px; border-radius: 50%; background: #ff2442; color: white;
    font-size: 14px; font-weight: 800; display: flex; align-items: center; justify-content: center;
    flex-shrink: 0;
  }}
  .insight-content {{ flex: 1; }}
  .insight-title {{ font-size: 13px; font-weight: 700; margin-bottom: 4px; }}
  .insight-desc {{ font-size: 12px; color: #666; line-height: 1.5; }}
  
  /* Background info */
  .bg-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }}
  .bg-card {{ background: #fafafa; border-radius: 10px; padding: 14px; border: 1px solid #f0f0f0; }}
  .bg-card-title {{ font-size: 13px; font-weight: 700; margin-bottom: 8px; color: #333; }}
  .bg-item {{ font-size: 12px; color: #555; line-height: 1.6; padding-left: 12px; position: relative; }}
  .bg-item::before {{ content: '•'; position: absolute; left: 0; color: #ff2442; }}
  
  /* Footer */
  .footer {{ text-align: center; padding: 20px; color: #bbb; font-size: 11px; margin-top: 4px; }}
  .footer-note {{ 
    margin: 12px 12px 0; background: #fff8f0; border-radius: 10px; padding: 10px 14px;
    font-size: 11px; color: #999; border: 1px solid #fde8c8;
  }}
  .footer-note strong {{ color: #e07000; }}
</style>
</head>
<body>

<!-- Header -->
<div class="header">
  <div class="header-tag">📕 小红书调研报告</div>
  <h1>{keyword}</h1>
  <div class="header-meta">调研平台：小红书 · 生成时间：{date} · 数据来源：真实笔记内容</div>
  <div class="header-stats">
    <div class="stat">
      <div class="stat-num">{note_count}</div>
      <div class="stat-label">相关笔记</div>
    </div>
    <div class="stat">
      <div class="stat-num">{keyword_count}</div>
      <div class="stat-label">核心关键词</div>
    </div>
    <div class="stat">
      <div class="stat-num">{max_likes}</div>
      <div class="stat-label">最高单篇点赞</div>
    </div>
    <div class="stat">
      <div class="stat-num">{heat_level}</div>
      <div class="stat-label">内容热度</div>
    </div>
  </div>
</div>

<!-- 数据概览 -->
<div class="section">
  <div class="section-title">数据概览</div>
  <div class="overview-grid">
    {overview_cards}
  </div>
</div>

<!-- 关键词热度 -->
<div class="section">
  <div class="section-title">关键词热度分析</div>
  {keyword_heat}
</div>

<!-- 背景信息（如有） -->
{background_section}

<!-- TOP 笔记 -->
<div class="section">
  <div class="section-title">TOP 代表性笔记</div>
  {top_notes}
</div>

<!-- 活跃创作者画像 -->
<div class="section">
  <div class="section-title">活跃创作者画像</div>
  <div class="creator-grid">
    {creators}
  </div>
</div>

<!-- 用户真实声音 -->
<div class="section">
  <div class="section-title">用户真实声音（评论区精华）</div>
  <div class="comments-grid">
    {comments}
  </div>
</div>

<!-- 需求与痛点 -->
<div class="section">
  <div class="section-title">用户需求与痛点分析</div>
  <div class="needs-grid">
    <div class="needs-card green">
      <div class="needs-title green">✅ 用户想要的</div>
      {needs_wants}
    </div>
    <div class="needs-card orange">
      <div class="needs-title orange">😤 用户痛点</div>
      {needs_pains}
    </div>
  </div>
</div>

<!-- 核心洞察 -->
<div class="section">
  <div class="section-title">核心洞察与结论</div>
  {insights}
</div>

<div class="footer-note">
  <strong>⚠️ 数据说明：</strong>本报告基于小红书公开搜索结果及 AI 分析综合生成，笔记数量/点赞数为估算值，供趋势参考，非精确统计。
</div>

<div class="footer">小红书调研报告 · 由 AI 自动生成 · {date}</div>

</body>
</html>'''


def render_overview_cards(data: dict) -> str:
    cards = data.get("overview_cards", [])
    html = ""
    for card in cards:
        html += f'''
    <div class="overview-card">
      <div class="overview-label">{card.get("label", "")}</div>
      <div class="overview-value">{card.get("value", "")}</div>
      <div class="overview-desc">{card.get("desc", "")}</div>
    </div>'''
    return html


def render_keyword_heat(data: dict) -> str:
    items = data.get("keyword_heat", [])
    html = ""
    for item in items:
        name = item.get("name", "")
        stars = item.get("stars", 3)
        pct = item.get("percent", 60)
        star_str = "★" * stars + "☆" * (5 - stars)
        html += f'''
  <div class="keyword-item">
    <div class="keyword-header">
      <span class="keyword-name">{name}</span>
      <span class="keyword-stars">{star_str}</span>
    </div>
    <div class="keyword-bar-bg"><div class="keyword-bar" style="width:{pct}%"></div></div>
  </div>'''
    return html


def render_background_section(data: dict) -> str:
    bg = data.get("background", None)
    if not bg:
        return ""
    
    title = bg.get("title", "背景知识")
    cards = bg.get("cards", [])
    
    cards_html = ""
    for card in cards:
        items_html = "".join(f'<div class="bg-item">{item}</div>' for item in card.get("items", []))
        cards_html += f'''
      <div class="bg-card">
        <div class="bg-card-title">{card.get("title", "")}</div>
        {items_html}
      </div>'''
    
    return f'''
<div class="section">
  <div class="section-title">{title}</div>
  <div class="bg-grid">
    {cards_html}
  </div>
</div>'''


def render_top_notes(data: dict) -> str:
    notes = data.get("top_notes", [])
    html = ""
    for i, note in enumerate(notes, 1):
        rank_class = {1: "rank-1", 2: "rank-2", 3: "rank-3"}.get(i, "rank-other")
        rank_text = str(i)
        
        tags_html = ""
        for tag in note.get("tags", []):
            color = tag.get("color", "red")
            css = {"blue": "blue", "green": "green"}.get(color, "")
            tags_html += f'<span class="note-tag {css}">{tag.get("text","")}</span>'
        
        likes = note.get("likes", "")
        bookmarks = note.get("bookmarks", "")
        comments = note.get("comments", "")
        stats_html = ""
        if likes:
            stats_html += f'<span class="note-stat"><span class="note-heart">♥</span> {likes}赞</span>'
        if bookmarks:
            stats_html += f'<span class="note-stat">⭐ {bookmarks}收藏</span>'
        if comments:
            stats_html += f'<span class="note-stat">💬 {comments}评论</span>'
        
        # 支持真实链接跳转
        url = note.get("url", "")
        author = note.get("author", "")
        title_html = f'<a class="note-link" href="{url}" target="_blank" rel="noopener">{note.get("title", "")}</a>' if url else note.get("title", "")
        
        author_html = ""
        if author:
            author_url = note.get("author_url", "")
            if author_url:
                author_html = f'<a class="note-author" href="{author_url}" target="_blank" rel="noopener">@{author}</a>'
            else:
                author_html = f'<span class="note-author">@{author}</span>'
        
        # 封面图：有 coverImg 时渲染图片，否则渐变色块降级
        cover_img = note.get("coverImg", "")
        rank_label = {1: "🔥 TOP1", 2: "🥈 TOP2", 3: "🥉 TOP3"}.get(i, f"#{i}")
        if cover_img:
            cover_html = f'''<div class="note-cover">
      <img src="{cover_img}" alt="笔记封面"
           onerror="this.parentNode.style.background='linear-gradient(135deg,#eee,#ccc)';this.remove()">
      <div class="note-cover-badge">{rank_label}</div>
    </div>'''
        else:
            cover_html = f'<div class="note-cover-fallback">📕</div>'

        html += f'''
  <div class="note-card">
    {cover_html}
    <div class="note-rank {rank_class}">{rank_text}</div>
    <div class="note-title">{title_html}</div>
    {f'<div class="note-author-line">{author_html}</div>' if author_html else ''}
    <div class="note-desc">{note.get("desc", "")}</div>
    <div class="note-meta">{tags_html}{stats_html}</div>
  </div>'''
    return html


def render_creators(data: dict) -> str:
    creators = data.get("creators", [])
    html = ""
    for c in creators:
        names_html = ""
        for n in c.get("names", []):
            if isinstance(n, dict):
                url = n.get("url", "")
                name = n.get("name", "")
                fans = n.get("fans", "")
                fans_str = f'<span class="creator-fans">{fans}粉</span>' if fans else ""
                if url:
                    names_html += f'<div class="creator-name-row"><a class="creator-link" href="{url}" target="_blank" rel="noopener">@{name}</a>{fans_str}</div>'
                else:
                    names_html += f'<div class="creator-name-row"><span class="creator-name-plain">{name}</span>{fans_str}</div>'
            else:
                names_html += f'<div class="creator-name-row"><span class="creator-name-plain">{n}</span></div>'
        
        # 典型选题
        topics = c.get("topics", [])
        topics_html = ""
        if topics:
            topic_items = "".join(f'<li>📝 {t}</li>' for t in topics)
            topics_html = f'<div class="creator-topics"><div class="creator-topics-title">典型选题</div><ul class="creator-topics-list">{topic_items}</ul></div>'
        
        html += f'''
    <div class="creator-card">
      <div class="creator-emoji">{c.get("emoji","📝")}</div>
      <div class="creator-type">{c.get("type","")}</div>
      <div class="creator-names">{names_html}</div>
      <div class="creator-desc">{c.get("desc","")}</div>
      {topics_html}
    </div>'''
    return html


def render_comments(data: dict) -> str:
    comments = data.get("comments", [])
    html = ""
    for c in comments:
        html += f'''
    <div class="comment-card">
      <div class="comment-text">{c.get("text","")}</div>
      <div class="comment-source">——来自「{c.get("source","")}」评论区{c.get("note","")}
      </div>
    </div>'''
    return html


def render_needs(data: dict, key: str, icon: str) -> str:
    items = data.get(key, [])
    html = ""
    for item in items:
        html += f'<div class="need-item"><span class="need-icon">{icon}</span><span>{item}</span></div>'
    return html


def render_insights(data: dict) -> str:
    insights = data.get("insights", [])
    html = ""
    for i, ins in enumerate(insights, 1):
        html += f'''
  <div class="insight-item">
    <div class="insight-num">{i}</div>
    <div class="insight-content">
      <div class="insight-title">{ins.get("title","")}</div>
      <div class="insight-desc">{ins.get("desc","")}</div>
    </div>
  </div>'''
    return html


def generate_html(data: dict, output_path: str):
    keyword = data.get("keyword", "未知关键词")
    date = data.get("date", datetime.now().strftime("%Y-%m-%d"))
    
    html = HTML_TEMPLATE.format(
        keyword=keyword,
        date=date,
        note_count=data.get("note_count", "30+"),
        keyword_count=data.get("keyword_count", "5"),
        max_likes=data.get("max_likes", "100+"),
        heat_level=data.get("heat_level", "中"),
        overview_cards=render_overview_cards(data),
        keyword_heat=render_keyword_heat(data),
        background_section=render_background_section(data),
        top_notes=render_top_notes(data),
        creators=render_creators(data),
        comments=render_comments(data),
        needs_wants=render_needs(data, "needs_wants", "✅"),
        needs_pains=render_needs(data, "needs_pains", "😤"),
        insights=render_insights(data),
    )
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)
    
    print(f"✅ 报告已生成: {output_path}")


def main():
    parser = argparse.ArgumentParser(description="生成小红书调研报告 HTML")
    parser.add_argument("--data", required=True, help="分析数据 JSON 文件路径")
    parser.add_argument("--output", required=True, help="输出 HTML 文件路径")
    args = parser.parse_args()
    
    with open(args.data, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    generate_html(data, args.output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
