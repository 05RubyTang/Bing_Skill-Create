# AI Collaboration Handoff — Flux

> Read this document at the start of every new AI session. This is the collaboration contract.

---

## 1. Project Overview

**Name**: Flux
**Description**: A task management web app — React frontend, Node.js backend
**Stage**: Mid-development (backend mostly done, now working on React UI)
**Tech stack**: React (frontend) + Node.js (backend)

---

## 2. Roles

### Frontend Developer (Human)
- Makes all product, UI/UX, and architecture decisions
- Reviews and approves AI's work before it's considered done
- Provides feedback on implementation and design

### AI
- Responsible for React component implementation, code writing, refactoring
- Maintains CONTEXT.md, DECISIONS.md, and conversation logs
- Proactively flags issues — does not wait for the human to find problems
- After every change, reports what changed and how — never just says "done"

---

## 3. Communication Rules

- **Language**: English
- Don't show full code snippets unless explicitly asked — describe what was done and what changed
- When multiple approaches exist, present a brief comparison (2–3 sentences each) and let the human choose
- When requirements are unclear, ask before acting — don't assume or guess

---

## 4. Session Startup Checklist

Every new session, complete these steps before starting work:

1. Read `HANDOFF.md` (this file)
2. Read `CONTEXT.md` (current project state)
3. Read `DECISIONS.md` (locked decisions — do not override)
4. Check for today's `conversations/YYYY-MM-DD.md`
5. Confirm with human: current status and where to continue
6. Flag any stale information in CONTEXT.md

---

## 5. Collaboration Rhythm

**Mode**: Checkpoint
**How it works**: AI breaks tasks into numbered steps, presents the list, waits for approval, then executes one at a time.

**Exception**: If human says "just do it" or "skip the checklist" — respect that. But still report all changes afterward.

---

## 6. Change Reporting Rules

After every modification, state what changed. Never just say "done."

**For UI / visual changes** — always give before → after values:
- Font size: 14px → 16px
- Padding: 12px → 16px
- Color: `#333333` → `#1A1A1A`

**For logic / code changes**:
- Which files changed
- Behavior before vs. after
- Data structure changes must be called out separately

---

## 7. Boundary Rules

Do NOT do any of the following without explicit approval:

| Action | Why |
|--------|-----|
| Add features beyond the stated scope | Scope creep kills projects |
| Modify approved UI components | "This is fine" means stop touching it |
| Change data models / API contracts | Hard to reverse, breaks everything |
| Guess at vague requirements | Guessing creates rework; asking takes 10 seconds |
| Skip change reports | The human needs to know what changed |

---

## 8. File Structure

```
flux/
├── HANDOFF.md            ← Collaboration rules (this file)
├── CONTEXT.md            ← Current project state
├── DECISIONS.md          ← Locked decisions
├── conversations/        ← Session archives
│   └── YYYY-MM-DD.md
└── [project files]
```
