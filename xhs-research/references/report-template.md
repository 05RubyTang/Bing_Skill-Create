# 小红书调研报告数据 Schema

> 本文件供 Agent 在填充报告 JSON 时参考。`generate_report.py --data <json>` 读入此结构后生成 HTML 报告。

---

## 顶层字段

```json
{
  "keyword":       "龙虾养殖",          // 报告主标题关键词（必填）
  "date":          "2026-04-07",        // 调研日期，默认今日
  "note_count":    "200+",              // 搜索到的相关笔记估算总量
  "keyword_count": "6",                 // 分析覆盖的核心子话题数
  "max_likes":     "1.2万",             // 采集到的最高单篇点赞
  "heat_level":    "高",                // 整体热度：低 / 中 / 高 / 极热
  ...各模块见下方
}
```

---

## overview_cards（数据概览卡片）

4 张卡片，呈 2×2 网格。建议填：笔记增长趋势、内容类型占比、平均互动率、创作者活跃度等。

```json
"overview_cards": [
  {
    "label": "内容增长趋势",
    "value": "↑38%",
    "desc":  "近30天新增笔记同比估算"
  },
  {
    "label": "图文 vs 视频",
    "value": "7:3",
    "desc":  "图文笔记仍占主导"
  },
  {
    "label": "平均点赞",
    "value": "312",
    "desc":  "TOP20笔记均值"
  },
  {
    "label": "活跃创作者",
    "value": "50+",
    "desc":  "近期持续发布的账号"
  }
]
```

---

## keyword_heat（关键词热度）

每项对应一个子话题，`stars` 1-5，`percent` 0-100（控制进度条长度）。建议 5-8 条。

```json
"keyword_heat": [
  { "name": "小龙虾怎么养",   "stars": 5, "percent": 95 },
  { "name": "龙虾养殖基地",   "stars": 4, "percent": 72 },
  { "name": "养龙虾日记",     "stars": 3, "percent": 55 },
  { "name": "龙虾病害防治",   "stars": 3, "percent": 48 },
  { "name": "龙虾养殖成本",   "stars": 2, "percent": 30 }
]
```

---

## background（背景知识模块）— 可选

**触发条件：见 SKILL.md「背景模块触发规则」。**

适合填入领域基础知识、行业背景、平台政策等，帮助读者理解调研语境。

```json
"background": {
  "title": "🦞 养殖背景知识",
  "cards": [
    {
      "title": "主要养殖品种",
      "items": ["克氏原螯虾（小龙虾）最主流", "澳洲淡水龙虾近年兴起", "南美白对虾常与龙虾混养"]
    },
    {
      "title": "产业规模",
      "items": ["2023年全国产量超350万吨", "湖北、安徽、湖南为主产区", "小红书相关笔记以家庭/小规模养殖为主"]
    }
  ]
}
```

若无需背景模块，**直接省略 `background` 字段**（不要填 `null`）。

---

## top_notes（TOP 代表性笔记）

建议 5-8 条，按互动量排序。**noteId 和 coverImg 必须从 browser evaluate 同步提取，严禁编造。**

```json
"top_notes": [
  {
    "noteId":    "69686b5f000000001a035dd8",
    "url":       "https://www.xiaohongshu.com/explore/69686b5f000000001a035dd8",
    "coverImg":  "https://sns-webpic-qc.xhscdn.com/202604070247/.../1040g00831...!nc_n_webp_mw_1",
    "title":     "养了3年龙虾，分享最全养殖心得",
    "author":    "虾农日记",
    "author_url":"",
    "desc":      "从选苗、喂食到防病，手把手教你少走弯路...",
    "likes":     "1061",
    "bookmarks": "432",
    "comments":  "89",
    "tags": [
      { "text": "🔥 热门", "color": "red" },
      { "text": "干货", "color": "blue" }
    ]
  }
]
```

### coverImg 字段说明

- 来源：与 `noteId` 同一次 browser evaluate 从 `<a>` 内部的 `<img>` 提取
- 格式：`https://sns-webpic-qc.xhscdn.com/...!nc_n_webp_mw_1`（去除 `?` 后的 query 参数）
- 降级：若该笔记无图可提取，**省略 `coverImg` 字段**，HTML 模板自动以渐变色块替代
- 禁止：头像域名（`sns-avatar-qc`）、base64 占位（`data:`）、跨笔记借用

---

## creators（创作者画像）

建议 3 种类型（图文 3 列），每种给 1-3 个代表账号。

```json
"creators": [
  {
    "emoji": "📖",
    "type":  "干货型博主",
    "desc":  "长期输出养殖技术，粉丝黏性高",
    "names": [
      { "name": "虾农日记",   "url": "https://www.xiaohongshu.com/user/profile/xxx", "fans": "2.3万" },
      { "name": "水产养殖说", "url": "",  "fans": "8500" }
    ],
    "topics": ["龙虾病害自救指南", "如何判断龙虾缺氧", "冬季保苗方法"]
  },
  {
    "emoji": "🎥",
    "type":  "vlog记录型",
    "desc":  "记录日常养殖过程，真实感强",
    "names": [{ "name": "乡村虾兄弟", "url": "", "fans": "1.1万" }],
    "topics": ["今天捕了300斤", "暴雨后的养殖池"]
  },
  {
    "emoji": "🏢",
    "type":  "机构/品牌号",
    "desc":  "饲料/种苗企业推广为主",
    "names": [{ "name": "正大水产", "url": "", "fans": "3.6万" }],
    "topics": ["新品饲料测评", "基地直播捕捞"]
  }
]
```

---

## comments（评论区精华）

建议 4-6 条，2 列网格。来源填笔记标题摘要。

```json
"comments": [
  {
    "text":   "水温超过32度就很难存活，这个血泪教训花了我5000块",
    "source": "养了3年龙虾分享心得",
    "note":   ""
  },
  {
    "text":   "有没有人知道苗从哪里买靠谱？网上乱七八糟的",
    "source": "龙虾养殖新手求助",
    "note":   "（高赞问题）"
  }
]
```

---

## needs_wants / needs_pains（需求与痛点）

各 4-6 条，字符串数组。

```json
"needs_wants": [
  "系统的入门养殖教程（从选塘到出售）",
  "可靠的种苗购买渠道推荐",
  "病害识别与用药指南",
  "小规模（1-5亩）的盈利核算参考"
],
"needs_pains": [
  "种苗质量参差不齐，死苗率高",
  "水质管理缺乏科学指导",
  "市场价格波动大，不知何时出售",
  "夏季高温期管理难度极大"
]
```

---

## insights（核心洞察）

建议 3-5 条。

```json
"insights": [
  {
    "title": "入门门槛感知高，教程需求旺盛",
    "desc":  "新手用户占比大，「从零开始」系列内容互动率远超平均，是最大的内容机会点。"
  },
  {
    "title": "痛点集中在种苗与病害两环节",
    "desc":  "超过60%的求助类笔记涉及苗源质量或疾病诊断，具备垂直解决方案的创作者更受信任。"
  },
  {
    "title": "视频内容渗透率上升但图文仍主导",
    "desc":  "视频能展示真实养殖场景，但技术干货类内容依然以长图文为主，两者定位差异化明显。"
  }
]
```
