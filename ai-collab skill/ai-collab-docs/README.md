# AI Collaboration Docs

A lightweight system that gives AI persistent memory across sessions — so you never have to re-explain your project again.

---

## The Problem

Every new AI session starts from a blank slate. This creates three compounding problems:

1. **Context tax** — 10–15 minutes re-explaining the project every time
2. **Decision drift** — AI re-proposes things you already rejected, or quietly reverses choices you made
3. **Blast radius** — "make it more polished" triggers 15 changes at once; you can't tell which one broke things

## The Solution

Four small Markdown files in your project root. AI reads them at session start, updates them as you work.

```
your-project/
├── HANDOFF.md      # HOW we work together (the contract)
├── CONTEXT.md      # WHERE the project is right now (the snapshot)
├── DECISIONS.md    # WHAT has been decided (the constitution)
└── conversations/  # WHAT happened when (the memory)
    └── 2026-04-01.md
```

No special tools. No database. No hosting. Just files that live next to your code.

---

## Quick Start

### If you're using Claude (Claude Code or Claude.ai with this skill)

Just say any of the following to get started:

- "Help me set up collaboration docs for this project"
- "Init project docs"
- "I keep having to re-explain things to AI — help me fix that"
- "帮我建立AI协作文档"
- "初始化项目协作文档"

Claude will ask you a few questions and generate the docs in about 5 minutes.

**After that, it's automatic** — whenever you open a project with a `HANDOFF.md`, Claude detects it and picks up from where you left off.

### If you're setting up manually

Run the setup script:

```bash
bash scripts/setup.sh
```

Follow the prompts. Your four files will be created in the current directory.

---

## How It Works Session-to-Session

**Session 1** (setup): Claude asks questions, generates the four files, writes a session log.

**Session 2** (next day, new conversation): Claude detects `HANDOFF.md`, reads all four files automatically, opens with:

> "I've read the project docs. Here's where we are: [summary]. Ready to continue with [next step]?"

You say "yes" and immediately get to work.

**Session N**: A decision you made three sessions ago comes up. Claude checks DECISIONS.md and says: "Heads up — this conflicts with [T-2]: we decided no external libraries without approval. Want to revise that, or work around it?"

---

## The Four Documents

### HANDOFF.md — The Contract
Defines how you and AI work together. Roles, communication style, workflow tempo, change reporting rules. Read at the start of every session.

**Changes rarely** — maybe once or twice per project.

### CONTEXT.md — The Snapshot
The current state of the project: what's done, what's in progress, what's next, what's deferred. Updated at the end of each session.

**Changes every session** — always a live view of "right now."

### DECISIONS.md — The Constitution
A structured log of every confirmed decision, with reasons and dates. Organized by category (Product, Technical, Design, etc.).

**Append-only** — entries are never silently deleted, only explicitly revised.

### conversations/YYYY-MM-DD.md — The Memory
A structured summary of each working session: key decisions, work completed, open questions, where to pick up. Created at the end of each session.

**Write-once** — you rarely go back to old logs, but when you need them, they're there.

---

## Works For Any Project Type

The system adapts to the language of your domain:

| Project type | "Data model" becomes | "Refactoring" becomes |
|---|---|---|
| iOS / mobile app | Data model | Refactoring |
| Web app | Schema / API structure | Restructuring |
| Design project | Content structure | Reorganizing |
| Research / writing | Argument structure | Revising |
| Any non-code project | Whatever fits | Whatever fits |

---

## Why Markdown?

- **Zero dependencies** — no setup, no tools, just files
- **Universally readable** — every AI, every editor, every platform handles Markdown
- **Version-controllable** — lives in git alongside your code; changes are tracked
- **Human-editable** — when AI gets something wrong, just open the file and fix it
- **Portable** — switching AI tools? The documents come with you

---

## FAQ

**Q: How long does setup take?**  
About 5 minutes. The time saved per session is 10–15 minutes. By session 2 you're net positive.

**Q: Do I have to maintain these manually?**  
No. AI updates them for you — CONTEXT.md at session end, DECISIONS.md when you confirm a choice, conversation logs automatically. You just say "yes" or "not now."

**Q: What if I forget to open with the collab docs?**  
If HANDOFF.md exists in your project, Claude detects it automatically and enters maintenance mode. You don't have to remember.

**Q: Is this the same as CLAUDE.md?**  
Complementary, not the same. CLAUDE.md handles static project-level instructions ("how this codebase works"). These docs handle evolving state ("how we're building it together right now"). If you already have CLAUDE.md, Claude will offer to integrate rather than duplicate.

**Q: What if two people are both using AI on the same project?**  
Add both roles to HANDOFF.md, a "Confirmed by" column to DECISIONS.md, and note who was present in conversation logs. The docs become shared project memory.

---

## File Reference

```
ai-collab-docs/
├── SKILL.md              # Skill instructions for Claude
├── README.md             # This file
├── references/
│   ├── templates.md      # Document templates (customizable starting points)
│   ├── examples.md       # Good vs. bad patterns with real examples
│   └── philosophy.md     # Design rationale ("why does this system work?")
└── scripts/
    └── setup.sh          # CLI setup script for manual initialization
```
