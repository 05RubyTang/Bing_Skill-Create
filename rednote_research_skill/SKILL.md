# SKILL.md · 小红书自动调研 — Agent 标准操作手册

> **版本**：v2.0（2026-04-03）  
> **适用场景**：用户说「小红书调研」「帮我调研 XX」「研究一下小红书上的 XX」  
> **输出物**：一份完整的 HTML 调研报告，存入 `research_claw/` 目录

---

## 一、前置准备

### 1.1 确认关键词和参数

从用户输入中提取：

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `keyword` | 用户指定 | 核心调研关键词，如「咖啡赛道」 |
| `min_likes` | 1万 | 代表性笔记最低点赞门槛 |
| `min_fans` | 3万 | 活跃创作者最低粉丝门槛 |
| `creator_types` | 4种 | 头部/身材细分/干货/垂直痛点 |

### 1.2 检查浏览器状态

```
browser(action="status", target="host")
```

如果浏览器未运行，先启动：
```
browser(action="start", target="host")
```

---

## 二、Step 1 — 扫码登录小红书

> ⚠️ **必须步骤**：搜索结果页需登录态，否则会被重定向到首页。

### 2.1 打开登录页

```
browser(action="navigate", url="https://www.xiaohongshu.com/explore", target="host")
```

等待 2 秒后截图，确认登录弹窗出现。

### 2.2 引导用户扫码

截图后发给用户：

> "登录弹窗已出现，请用小红书 App 扫码：  
> 📱 打开小红书 App → 右上角相机/扫一扫 → 扫描页面二维码  
> 扫完告诉我，我立刻开始搜索！"

### 2.3 确认登录成功

用户回复扫码完成后，导航一次确认：

```javascript
// 在浏览器执行，检查是否已登录
() => {
  return document.querySelector('[class*=avatar],[class*=user-info]') !== null
    || document.cookie.includes('web_session')
    || document.body.innerText.includes('我的');
}
```

如果仍未登录，截图再次确认状态。

> **记录 targetId**：后续所有步骤使用同一 targetId，不要切换标签页。

---

## 三、Step 2 — 多维度关键词搜索

### 3.1 搜索策略

每次调研使用 **3-5 个关键词变体**，分别搜索，覆盖不同细分人群：

| 搜索类型 | URL 模板 | 说明 |
|----------|---------|------|
| 热度排序笔记 | `/search_result?keyword=XXX&type=51&sort=popularity_descending` | 找高赞内容 |
| 用户搜索 | `/search_result?keyword=XXX&source=web_search_result_users&type=61` | 找活跃博主 |

**关键词变体示例**（以「穿搭痛点」为例）：
- `穿搭痛点`（核心词）
- `显瘦穿搭`（功能词）
- `梨形身材穿搭`（人群词）
- `穿搭技巧干货`（内容类型词）
- 视情况添加：`矮个子穿搭`、`微胖穿搭` 等

### 3.2 抓取笔记列表

每个关键词搜索后，执行 JS 抓取笔记：

```javascript
() => {
  const items = [];
  document.querySelectorAll('a[href*="/explore/"]').forEach(a => {
    const id = a.href.match(/explore\/([a-f0-9]{24})/)?.[1];
    if (!id) return;
    const section = a.closest('section') || a.closest('[class*=note]') || a.closest('div[class]');
    const title = section?.querySelector('[class*=title],[class*=desc],[class*=footer]')?.innerText?.trim()?.slice(0, 80);
    const likes = section?.querySelector('[class*=like],[class*=count],[class*=interact]')?.innerText?.trim();
    if (title && likes) items.push({
      id,
      url: 'https://www.xiaohongshu.com/explore/' + id,
      title,
      likes
    });
  });
  // 去重，按点赞数排序
  return [...new Map(items.map(r => [r.id, r])).values()]
    .sort((a, b) => {
      const toNum = s => {
        if (!s) return 0;
        if (s.includes('万')) return parseFloat(s) * 10000;
        return parseFloat(s) || 0;
      };
      return toNum(b.likes) - toNum(a.likes);
    }).slice(0, 20);
}
```

### 3.3 筛选高赞笔记

从结果中筛选点赞数 ≥ `min_likes` 的笔记，记录：
- 笔记 ID（24位十六进制）
- 笔记 URL
- 标题
- 点赞数

---

## 四、Step 3 — 获取真实笔记数据和博主信息

> ⚠️ **核心步骤**：必须访问真实页面，不能估算或构造数据。

### 4.1 进入高赞笔记详情页

```
browser(action="navigate", url="https://www.xiaohongshu.com/explore/{笔记ID}", target="host")
```

等待加载后，执行 JS 获取完整互动数据：

```javascript
() => {
  const e = document.querySelector('[class*=engage],[class*=interact]')?.innerText || '';
  const title = document.querySelector('#detail-title')?.innerText || '';
  // 数字在文本末尾：{赞}\n{收藏}\n{评论}
  const nums = e.match(/(\d+[\d\.]*万?)/g) || [];
  const likes = nums[nums.length - 3] || '';
  const bookmarks = nums[nums.length - 2] || '';
  const comments = nums[nums.length - 1] || '';
  // 获取作者链接
  const authorLinks = [...document.querySelectorAll('a[href*="/user/profile"]')];
  const authorLink = authorLinks.find(a => !['我'].includes(a.innerText.trim()) && a.innerText.trim().length > 0);
  return {
    title,
    likes, bookmarks, comments,
    authorName: authorLink?.innerText?.trim(),
    authorId: authorLink?.href?.match(/user\/profile\/([\w]+)/)?.[1],
    authorUrl: authorLink?.href?.split('?')[0]  // 去掉 query 参数保持干净
  };
}
```

### 4.2 验证作者粉丝数

```
browser(action="navigate", url="https://www.xiaohongshu.com/user/profile/{authorId}", target="host")
```

```javascript
() => {
  const t = document.body.innerText;
  // 粉丝数提取
  const fans = t.match(/关注\s*\n\s*([\d\.]+万?)\s*\n\s*粉丝/)?.[1];
  // 获赞与收藏
  const likes = t.match(/粉丝\s*\n\s*([\d\.]+万?\+?)\s*\n\s*获赞与收藏/)?.[1];
  // 近期笔记标题（前5条）
  const name = t.match(/\n([^\n]{2,15})\n小红书号/)?.[1];
  return { name, fans, totalLikes: likes };
}
```

**筛选规则**：
- 粉丝数 ≥ `min_fans`（默认3万）→ 纳入「活跃创作者」
- 粉丝数 < `min_fans` → 记录但不放入创作者画像（可作备注）

### 4.3 批量验证策略

效率优化：
1. 先从热度排序结果中取前 10 条笔记
2. 按点赞数从高到低依次进入，获取作者 uid
3. 每个作者主页访问一次，核实粉丝数
4. 目标：每种创作者类型找到 **至少 2 个** 满足粉丝门槛的博主

如需扩充某类型博主，用「用户搜索」关键词：

```
/search_result?keyword=梨形穿搭博主&source=web_search_result_users&type=61
```

再批量抓取列表中的 uid：

```javascript
() => {
  const items = [];
  document.querySelectorAll('a[href*="/user/profile/"]').forEach(a => {
    const uid = a.href.match(/user\/profile\/([\w]+)/)?.[1];
    if (!uid) return;
    const t = a.innerText?.trim();
    if (t && t.length > 1 && t.length < 20 && !['我', '关注'].includes(t))
      items.push({ uid, url: 'https://www.xiaohongshu.com/user/profile/' + uid, name: t });
  });
  return [...new Map(items.map(r => [r.uid, r])).values()].slice(0, 20);
}
```

### 4.4 抓取高赞笔记评论

进入高赞笔记详情页后，评论区前几条可直接读取：

```javascript
() => {
  const comments = [];
  document.querySelectorAll('[class*=comment]').forEach(el => {
    const text = el?.innerText?.trim();
    if (text && text.length > 10 && text.length < 200) comments.push(text);
  });
  return comments.slice(0, 10);
}
```

---

## 五、Step 4 — 整合数据，AI 分析补全

### 5.1 数据整理

将浏览器采集到的真实数据整理为 JSON：

```json
{
  "keyword": "穿搭痛点",
  "date": "YYYY-MM-DD",
  "top_notes": [
    {
      "title": "...",
      "url": "https://www.xiaohongshu.com/explore/{ID}",
      "author": "博主昵称",
      "author_url": "https://www.xiaohongshu.com/user/profile/{uid}",
      "likes": "10万",
      "bookmarks": "2.5万",
      "comments": "5479",
      "desc": "...(AI分析该笔记为什么爆款，写2-3句话)",
      "tags": [{"text": "标签名", "color": "red|blue|green"}]
    }
  ],
  "creators": [
    {
      "emoji": "🌸",
      "type": "头部潮流博主",
      "names": [
        {"name": "博主名", "url": "https://www.xiaohongshu.com/user/profile/{uid}", "fans": "368.2万"},
        {"name": "博主名2", "url": "...", "fans": "36.3万"}
      ],
      "desc": "简要描述这类博主的特点（1-2句）",
      "topics": [
        "典型选题1（从其笔记列表真实提取）",
        "典型选题2",
        "典型选题3"
      ]
    }
  ]
}
```

> 完整字段说明见 `data-schema.md`

### 5.2 AI 补全分析模块

以下模块可由 AI 综合分析生成（无需完全依赖爬取数据）：

- `overview_cards`：数据概览卡片（赛道规模、增速、核心人群 — 标注为AI估算）
- `keyword_heat`：关键词热度排行（结合搜索量判断）
- `background.cards`：赛道背景知识（趋势、爆款要素）
- `comments`：用户声音（从真实评论中提炼 + AI补充典型评论类型）
- `needs_wants` / `needs_pains`：需求与痛点（AI综合分析）
- `insights`：核心洞察（3-5条，结合真实数据）

---

## 六、Step 5 — 生成 HTML 报告

### 6.1 保存数据 JSON

```python
import json
data = { ... }  # 整理好的数据
with open('/tmp/xhs_{keyword}_data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
```

### 6.2 调用生成脚本

```bash
python3 ~/.openclaw/workspace/skills/xhs-research/scripts/generate_report.py \
  --data /tmp/xhs_{keyword}_data.json \
  --output ~/.openclaw/workspace/research_claw/小红书调研报告_{keyword}.html
```

### 6.3 预览报告

```
canvas(action="present", url="file:///home/node/.openclaw/workspace/research_claw/小红书调研报告_{keyword}.html")
```

或告知用户文件路径，由用户在本地浏览器打开。

---

## 七、创作者类型分类参考

| 类型 | Emoji | 典型特征 | 典型搜索词 |
|------|-------|----------|----------|
| 头部潮流博主 | 🌸 | 粉丝50万+，有独特审美视角，跨界内容（IP/动画/老钱风） | `穿搭 热门` |
| 身材细分型 | 🍐 | 粉丝10-100万，聚焦特定身材（梨形/微胖/矮个子），内容高度垂直 | `梨形穿搭博主` |
| 干货方法论型 | 🎓 | 粉丝3-50万，系统性穿搭教程，收藏率高 | `穿搭干货技巧` |
| 垂直痛点答疑型 | 🎀 | 粉丝1-10万，聚焦特定场景/问题（JK/通勤/素颜），互动密度高 | `穿搭痛点解决` |

---

## 八、data-schema.md 参考（数据字段说明）

见 `data-schema.md` 文件。

---

## 九、质量检查清单

生成报告前，逐项确认：

```
✅ top_notes 中每条笔记的 url 已经过浏览器实际访问验证
✅ 每条笔记的 likes/bookmarks/comments 来自页面真实数据
✅ 每个 creator.names 中的 url 已验证可访问（uid 真实存在）
✅ 每个 creator 的 fans 通过访问主页实时核实
✅ 每种 creator type 有 ≥ 2 个博主（粉丝满足门槛）
✅ HTML 输出文件 >25KB（说明内容足够丰富）
✅ 报告存入 research_claw/ 目录
✅ 数据概览卡片标注「AI估算值，非精确统计」
```

---

## 十、常见问题 & 处理方案

| 问题 | 原因 | 解决方案 |
|------|------|---------|
| 搜索页跳转回首页 | 未登录 | 重新引导用户扫码登录 |
| 笔记 url 打不开 | ID错误或内容已删除 | 换其他高赞笔记 |
| 博主主页粉丝数无法提取 | 页面结构变化 | 截图手动查看，手动填入 |
| 找不到满足粉丝门槛的某类博主 | 该细分类型门槛偏高 | 适当降低该类型门槛至1万，或补充其他细分方向 |
| 生成脚本报错 | JSON 字段缺失 | 检查 data-schema.md，补全必填字段 |

---

## 十一、关键 URL 模板速查

```
# 热度排序笔记搜索
https://www.xiaohongshu.com/search_result?keyword={词}&type=51&sort=popularity_descending

# 用户搜索（找博主）
https://www.xiaohongshu.com/search_result?keyword={词}&source=web_search_result_users&type=61

# 笔记详情页
https://www.xiaohongshu.com/explore/{24位笔记ID}

# 博主主页
https://www.xiaohongshu.com/user/profile/{uid}
```

---

## 十二、附录：已验证的穿搭痛点赛道博主库

可在「穿搭」相关调研中直接复用，无需重新爬取：

| 博主 | 粉丝数 | 类型 | uid | 验证时间 |
|------|--------|------|-----|---------|
| 白昼小熊 | 368.2万 | 头部潮流 | `5a8cf39111be10466d285d6b` | 2026-04-03 |
| 快把柚子带走 | 56.9万 | 身材细分(微胖) | `616d641800000000020203f2` | 2026-04-03 |
| 我不是小胖友 | 40.3万 | 身材细分(微胖) | `5dd4d0e60000000001005b27` | 2026-04-03 |
| 大米饭的大米 | 36.3万 | 头部/干货 | `5ad40517e8ac2b07694d0f3e` | 2026-04-03 |
| 肉梨咕噜 | 34.1万 | 身材细分(梨形) | `621bd17c0000000021026917` | 2026-04-03 |
| 典点子 | 13.1万 | 综合型 | `5984b1705e87e728aead557b` | 2026-04-03 |
| 一直鹿仔 | 9万 | 身材细分(梨形粗腿) | `5fae36dc000000000101fc83` | 2026-04-03 |
| 一只万万 | 4万 | 干货方法论 | `5dbe8db20000000001004dcb` | 2026-04-03 |
| Jinn | 2.9万 | 造型师/干货 | `55d7cb34b7ba22627cf3c8f7` | 2026-04-03 |
| 张不透透 | 1.2万 | 垂直痛点 | `633af6e3000000001802b33b` | 2026-04-03 |
