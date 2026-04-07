---
name: xhs-research
description: 小红书调研报告自动生成 Skill。输入一个关键词，自动搜索小红书笔记内容，分析热度、用户需求、痛点、创作者类型，生成美观的 HTML 调研报告。触发词：「小红书调研」、「帮我调研」、「生成小红书报告」、「研究一下小红书上的」。
---

# 小红书调研报告 Skill

> 触发词：「小红书调研」、「帮我调研 XX」、「生成小红书报告」、「研究一下小红书上的 XX」

---

## ⚠️ 笔记链接规范（必读，违反即为严重错误）

### 正确的小红书笔记链接格式

小红书笔记的**唯一可访问链接格式**为：

```
https://www.xiaohongshu.com/explore/<noteId>
```

例如：
```
https://www.xiaohongshu.com/explore/69686b5f000000001a035dd8
```

### 错误示范（绝对禁止）

以下格式**均为伪造链接，用户无法打开**，严禁出现在报告中：

| ❌ 错误格式 | 说明 |
|-----------|------|
| `/search_result/<noteId>` | 这是搜索结果页路径，不是笔记链接 |
| `xiaohongshu.com/note/<noteId>` | 不存在的路径格式 |
| `xiaohongshu.com/p/<noteId>` | 不存在的路径格式 |
| 任何凭空编造的 noteId | 必须从页面真实读取 |

### 如何获取真实 noteId

从小红书搜索结果 snapshot 中，笔记链接的原始格式是：
```
/search_result/<noteId>?xsec_token=<token>&xsec_source=
```

**noteId 就是 `/search_result/` 后面、`?` 前面的那串字符**，例如：
- 原始：`/search_result/69686b5f000000001a035dd8?xsec_token=ABxP6Xq...`
- 提取 noteId：`69686b5f000000001a035dd8`
- 最终链接：`https://www.xiaohongshu.com/explore/69686b5f000000001a035dd8`

---

## ⚠️ 笔记封面图规范（必读，违反即为严重错误）

### 封面图来源唯一性原则

笔记封面图必须**在同一次搜索页面抓取中**与 noteId 同步提取，绝对禁止：
- 凭空编造图片 URL
- 把 A 笔记的图片用在 B 笔记的卡片上
- 使用非当次从搜索页读取的图片 URL

### 小红书图片 CDN 格式

真实笔记封面图来自小红书官方 CDN，域名特征如下：

```
https://sns-webpic-qc.xhscdn.com/<时间戳>/<hash>/<图片路径>!nc_n_webp_mw_1
```

或（spectrum 格式）：
```
https://sns-webpic-qc.xhscdn.com/<时间戳>/<hash>/spectrum/<图片路径>!nc_n_webp_mw_1
```

⚠️ **URL 中的时间戳会导致图片在数小时到数天后过期失效。** 如需长期保存，应将图片下载到本地。

### 错误图片来源（绝对禁止）

| ❌ 错误 | 说明 |
|--------|------|
| `sns-avatar-qc.xhscdn.com` | 这是用户头像，不是笔记封面 |
| `picasso-static.xiaohongshu.com` | 这是平台静态资源 |
| `data:image/...` | base64 占位符，懒加载前的占位图 |
| 任何 A 笔记图用于 B 笔记 | noteId 与 imgSrc 必须同卡片提取，严格一一对应 |

---

## 执行流程（Agent 完整操作步骤）

### Step 0 — 登录小红书

```
browser.navigate → https://www.xiaohongshu.com/explore
→ 截图发给用户，引导扫码登录
→ 等待用户确认登录成功（页面不再出现登录弹窗）
→ 确认方式：browser.act evaluate 检查页面内容
```

**登录失败 / 用户跳过登录的降级策略：**
- 改用 `web_search` 搜索小红书相关内容进行内容分析
- 报告中 `top_notes` 模块**不展示任何笔记链接与封面图**，只展示标题与摘要
- 在报告头部注明「当前为无登录模式，笔记链接不可用」

### Step 1 — 搜索页面导航 + 等待渲染

```
browser.navigate → https://www.xiaohongshu.com/search_result/?keyword=<关键词>&source=web_explore_feed&type=51
browser.act → { kind: "wait", timeoutMs: 3000, loadState: "networkidle" }
```

⚠️ 小红书搜索页是 Vue SPA，必须等待 `networkidle` 后内容才渲染完成，否则图片未加载。

### Step 2 — 一次性同时提取 noteId + 封面图（核心步骤）

**必须用同一个 JS evaluate 同时提取 noteId 和封面图 URL，确保严格一一对应：**

```javascript
() => {
  const results = [];
  document.querySelectorAll('a[href*="/search_result/"]').forEach(a => {
    // 提取 noteId
    const noteId = a.href.match(/search_result\/([a-f0-9]+)/)?.[1];
    if (!noteId) return;

    // 从同一个 <a> 内部提取封面图
    const img = a.querySelector('img');
    if (!img) return;
    const src = img.src || img.getAttribute('data-src') || '';

    // 只保留真实笔记封面图（排除头像、静态资源、占位图）
    if (
      src.includes('xhscdn') &&
      (src.includes('webpic') || src.includes('spectrum')) &&
      !src.includes('avatar') &&
      !src.startsWith('data:')
    ) {
      results.push({
        noteId,
        exploreUrl: `https://www.xiaohongshu.com/explore/${noteId}`,
        coverImg: src.split('?')[0]  // 去掉多余参数，保留干净 URL
      });
    }
  });
  return JSON.stringify(results);
}
```

**此 JS 的关键设计：**
- 以 `<a>` 元素为单位遍历，noteId 和 img 都从**同一个 `<a>` 内部**提取
- `img.src` 在 `networkidle` 后已经是真实 CDN URL（非 base64 占位）
- 图片 URL 去掉 `?` 后的 query 参数，避免 token 污染
- 返回结构：`[{ noteId, exploreUrl, coverImg }, ...]`

### Step 3 — 验证提取结果

提取后必须做以下检查：
- [ ] `noteId` 均为 20-24 位十六进制字符串
- [ ] `coverImg` 均包含 `xhscdn` 且包含 `webpic` 或 `spectrum`
- [ ] `coverImg` 不包含 `avatar`
- [ ] `noteId` 与 `coverImg` 数量一致（1:1 对应）
- [ ] 若某笔记无图（`img` 为 null），该笔记不强制插入封面，报告中以渐变色块降级展示

### Step 4 — 数据结构（写入报告前）

提取到的每个笔记对象应包含（完整字段见 `references/report-template.md` 的 `top_notes` 部分）：

```json
{
  "noteId":    "69686b5f000000001a035dd8",
  "url":       "https://www.xiaohongshu.com/explore/69686b5f000000001a035dd8",
  "coverImg":  "https://sns-webpic-qc.xhscdn.com/202604070247/.../1040g00831...!nc_n_webp_mw_1",
  "title":     "...",
  "author":    "...",
  "likes":     "1061",
  "bookmarks": "432",
  "comments":  "89",
  "desc":      "...",
  "tags":      [{ "text": "🔥 热门", "color": "red" }]
}
```

> ⚠️ `coverImg` 字段必须在 Step 2 的同一次 evaluate 中与 `noteId` 同步提取，不得在此步骤单独补充或替换。此字段将**直接传入 `generate_report.py`**，由脚本渲染为笔记卡片顶部封面图。若无图，省略该字段，脚本自动降级为渐变色块。

### Step 4.5 — 校验笔记数据（可选但推荐）

在写入报告 JSON 前，可运行校验脚本确认格式无误：

```bash
# 先将 evaluate 结果保存为 JSON
python scripts/validate_notes.py --data /tmp/xhs_notes.json
# 严格模式（警告也拦截）
python scripts/validate_notes.py --data /tmp/xhs_notes.json --strict
```

脚本输出 `ok_to_proceed: true` 时才继续生成报告。

### Step 5 — 组装报告 JSON + 生成 HTML

**JSON 字段填写规范**：读取 `references/report-template.md`，按其 schema 填充各模块字段。

**背景模块触发规则（`background` 字段）：**

以下情况**应当**生成背景模块：
- 关键词属于垂直领域 / 小众行业（如养殖、中医、小众运动），读者可能缺乏基础认知
- 用户明确要求「帮我也介绍一下这个领域」
- 搜索结果中出现大量专业术语，直接分析可能让读者看不懂

以下情况**不应**生成背景模块：
- 关键词是大众消费品、日常生活话题（如「减脂食谱」「旅游攻略」）
- 关键词已经足够自明（如「穿搭」「美妆」）

**报告 JSON 准备好后**，调用生成脚本：

```bash
python scripts/generate_report.py \
  --data /tmp/xhs_report_data.json \
  --output ~/Desktop/小红书调研报告_<keyword>.html
```

---

## 链接审验流程（每次生成报告前必须执行）

在将任何笔记链接写入报告之前，必须完成以下检查：

### Step 1 — 确认来源
- [ ] 链接中的 noteId 是否来自 `browser evaluate` 读取的真实页面？
- [ ] 还是 AI 自行推断/编造的？（如果是后者，**立即停止，重新获取**）

### Step 2 — 格式转换
- [ ] 原始路径格式 `/search_result/<noteId>?...` → 提取 noteId
- [ ] 最终链接格式：`https://www.xiaohongshu.com/explore/<noteId>`
- [ ] 检查 noteId 长度（通常 20-24 个字符，全为 16 进制字符）

### Step 3 — 写入报告
- [ ] 报告中所有笔记链接均使用 `explore/<noteId>` 格式
- [ ] 不得出现 `search_result` 路径
- [ ] 禁止在未从页面获取的情况下虚构任何 noteId

### Step 4 — 最终自查
报告生成后，Agent 应对报告中的所有链接做以下声明：
> "本报告中的 X 个笔记链接，全部从小红书搜索页面 evaluate 中直接读取，noteId 与封面图均已验证来源真实，且严格一一对应。"

如无法完成以上验证，**不得在报告中展示笔记链接或封面图**，改为说明"需登录小红书后搜索获取"。

---

## 功能概览

输入一个关键词，自动：
1. 登录小红书，逐关键词搜索，**同步提取**每个笔记的 noteId + 封面图 URL（严格一一对应）
2. 分析热度、关键词频次、创作者类型、用户痛点
3. 生成美观 HTML 调研报告（红色主题，每张卡片顶部展示真实笔记首图）

---

## 报告结构

| 模块 | 内容 |
|------|------|
| **Header** | 关键词标题、生成时间、核心数字（笔记数/最高点赞/热度） |
| **数据概览** | 多搜索词笔记数量、内容类型分布、创作者类型 |
| **关键词热度分析** | 子话题热度条形图（★评级） |
| **TOP 代表性笔记** | 高互动笔记卡片（封面首图/标题/摘要/点赞/收藏/真实链接） |
| **活跃创作者画像** | 按类型分类（干货型/记录型/机构营销型） |
| **用户真实声音** | 评论区高频话题精华 |
| **用户需求与痛点** | 两栏对比（想要的 vs 痛点） |
| **核心洞察与结论** | 编号洞察，带 emoji 标记 |

---

## 数据来源

- **主要**：登录小红书后通过 `browser evaluate` 同步读取搜索结果中的笔记 noteId + 封面图（严格一一对应）
- **增强**：AI 分析综合提炼内容洞察
- **降级（无法登录时）**：`web_search` 搜索小红书笔记内容做内容分析，但此时**不得生成任何笔记链接或封面图**（见 Step 0 降级策略）

---

## 文件结构

```
skills/xhs-research/
├── SKILL.md                          # 本文件（工作流 + 规范）
├── scripts/
│   ├── validate_notes.py            # 笔记数据格式校验工具（Step 4.5）
│   └── generate_report.py           # HTML 报告生成脚本（Step 5）
└── references/
    └── report-template.md           # 报告 JSON 数据 schema 及字段说明
```

---

## 注意事项

- 搜索使用多个关键词变体提升覆盖度（如"龙虾养殖" + "小龙虾怎么养" + "养龙虾日记"）
- 数据分析由 LLM 综合推断，非实时精确数据，适合趋势判断
- HTML 报告离线可用，纯原生无第三方 CDN 依赖
- 小红书图片 URL 带时间戳，数小时到数天后可能过期，长期存档需本地化图片
- **【严禁】** 在未从小红书页面真实读取的情况下，编造任何笔记 ID、链接或图片 URL
- 如果无法获取真实数据（未登录/网络问题），报告中的笔记模块只展示标题和摘要，不展示链接与封面图
