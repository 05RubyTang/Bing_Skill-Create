---
name: memory-dreaming
description: 轻量版 Dreaming 记忆巩固。在 OpenClaw 升级到支持原生 Dreaming 之前，手动触发或通过 heartbeat 自动运行，读取近期每日日志、提炼有价值的信息、更新 MEMORY.md。触发词："整理记忆"、"做梦"、"记忆巩固"、"更新 MEMORY"、"dreaming"、"提炼今天的记忆"。也可由 heartbeat 按计划自动触发（每周一次）。
---

# memory-dreaming · 轻量版记忆巩固

模拟 OpenClaw Dreaming 的三阶段流程（Light → REM → Deep），将短期日志提炼为长期记忆。

## MEMORY.md 三层结构

详见 `references/memory-structure.md`（三层定义 + 评分权重 + 提炼判断原则）。

---

## 执行流程

### Step 1：Light 阶段 — 收集与评分

运行分析脚本，扫描近 7 天的每日日志：

```bash
python3 ~/.openclaw/workspace/skills/memory-dreaming/scripts/dream.py --days 7
```

读取输出的 JSON，重点关注：
- `candidates`：按评分排序的日志列表
- `current_memory_md.content`：当前 MEMORY.md 完整内容

### Step 2：REM 阶段 — 主题识别

阅读候选日志，识别跨多天重复出现的主题：
- 同一个产品方向被多次提及 → 升级为近期层
- Ruby 明确说出的偏好 → 升级为常青层
- 发现新的工具 Bug 或路径变化 → 更新工具层

跳过不需要提炼的内容（见 `references/memory-structure.md` 末尾判断原则）。

### Step 3：Deep 阶段 — 写入 MEMORY.md

根据三层结构决定写入位置：

**写入规则：**
- 🌲 常青层：只在有实质新信息时追加或修改，不轻动已有内容
- 📅 近期层：追加新认知；同时检查是否有过时内容需要清除
- ♻️ 工具层：有变更就更新，保持准确

写入后运行验证：

```bash
# 确认文件写入成功，字数合理
wc -l ~/.openclaw/workspace/MEMORY.md
```

### Step 4：记录梦境日志

在 `memory/YYYY-MM-DD.md` 末尾追加本次巩固记录：

```markdown
## 🌙 Dreaming 记录（HH:MM）
- 扫描日志：N 天，M 篇
- 本次提炼：[简述主要变更]
- 下次建议：[可选，下次重点关注的主题]
```

---

## 触发方式

### 手动触发
用户说「整理记忆」、「做梦」、「提炼今天的记忆」等词时执行完整流程。

### Heartbeat 自动触发（每周一次）
在 `HEARTBEAT.md` 中加入：
```
每周日晚 22:00 触发一次 memory-dreaming，巩固本周记忆。
```

---

## 注意事项

- **不轻易删除常青层内容**：除非 Ruby 明确说不再需要
- **近期层的「月度回顾」**：每月第一次 dreaming 时检查上月近期层，过时的清除
- **不写入一次性技术细节**：如小红书笔记 ID、浏览器 targetId 等，不进 MEMORY.md
- **保持 MEMORY.md 精练**：它是精华提炼，不是日志搬运；每次写入都问「未来的我真的需要记住这个吗？」
