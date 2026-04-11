# AI 回应 — Eval 2（without skill / baseline）

这个问题很常见！AI 默认没有跨会话记忆，所以每次都要重新解释。

## 解决方案

**方案一：在项目里建一个 README 或 PROJECT.md**

把常用背景信息写进去，每次开新会话时把内容粘贴过来就行。

**方案二：用 CLAUDE.md（如果你用 Claude Code）**

在项目根目录创建 `CLAUDE.md`，Claude 每次启动会自动读取。

你可以写：
```
这是一个小红书笔记生成工具，Python 实现，CLI 输出。
技术决策：
- 使用 OpenAI API
- 输出格式为 Markdown  
- 只做命令行，不做 UI
```

**方案三：自定义指令/系统提示**

在 Claude 设置里设置自定义指令，写入你的常用背景。

---

你想我帮你写一个项目背景文件的模板吗？你的项目用的是哪个 AI 工具？
