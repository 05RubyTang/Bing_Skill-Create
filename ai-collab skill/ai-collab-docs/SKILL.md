---
name: ai-collab-docs
description: "Set up and maintain structured AI collaboration documents for any project. ALWAYS trigger this skill in these situations: (1) MOST IMPORTANTLY — at the start of ANY session where HANDOFF.md exists in the project directory, automatically enter Maintenance Mode without waiting to be asked; scan for HANDOFF.md before starting any work; (2) User asks to set up project collaboration docs, create handoff documents, initialize AI-friendly project structure; (3) User wants to create HANDOFF.md / CONTEXT.md / DECISIONS.md; (4) User mentions any of: 'establish AI collaboration rules', 'reduce repeated context-setting', 'init project docs', 'set up collaboration', 'help me work better with AI', 'I keep having to re-explain things', 'AI keeps undoing my decisions', '帮我建立协作文档', '每次都要重新跟AI解释', '初始化项目文档', '设置AI协作', 'AI老是改回去', 'vibe coding workflow'; (5) User references this system by name. Do NOT trigger for: general documentation, README, API docs, or single-file templates."
---

# AI Collaboration Documents — Skill Guide

> **What this is**: A system of 4 lightweight documents that give AI persistent memory across sessions. It eliminates the three biggest pain points of AI collaboration: lost context, reversed decisions, and uncontrolled changes.
>
> **Who it's for**: Anyone using AI to build things — developers, designers doing vibe coding, PMs prototyping, researchers, writers, students. Works with any AI tool that reads files.
>
> **Reference files:**
> - `references/templates.md` — Full document templates (read when generating docs)
> - `references/examples.md` — Good vs. bad patterns in practice (read when uncertain)
> - `references/philosophy.md` — Design rationale (read if user asks "why")

---

## PRIORITY ZERO: Check Before Anything Else

**At the very start of every session, before reading the user's request or taking any action:**

1. Check if `HANDOFF.md` exists in the project root (or any parent directory of the current working context)
2. If **yes** → immediately enter **Mode B (Maintenance)** — read the docs, confirm state with the user
3. If **no** → proceed normally; if the user's request triggers this skill, enter **Mode A (Setup)**

This check is not optional. The whole point of HANDOFF.md is that AI picks it up automatically. Don't make the user ask.

---

## Two Modes

### Mode A: Initial Setup
User wants to create the collaboration docs for a project from scratch.  
→ Follow the **Setup Workflow** below.

### Mode B: Ongoing Maintenance
HANDOFF.md already exists in the project.  
→ Follow the **Maintenance Protocol** below.  
→ Enter this mode automatically — no prompt needed from the user.

---

## Mode A: Setup Workflow

### Step 1 — Learn about the project

Ask the user these questions conversationally — don't dump them all at once. Adapt to how the user communicates. Keep it feeling like a conversation, not a form.

**Must know (ask explicitly):**
1. Project name and one-line description — what does it do, for whom?
2. Your role vs. AI's role — who makes decisions, who executes?
3. Tech stack / tools (if applicable) — or "no code" if it's a writing/design/research project
4. Current stage — idea / early build / mid-development / polishing / shipped
5. Any decisions already made that AI should never revisit?

**Good to know (ask if relevant or not obvious):**
6. Language for all documents — default to whatever the user is writing in
7. Collaboration rhythm — checkpoint (step-by-step with pauses) or batch (AI does a chunk, then reports)?
8. Are there existing files AI should read? (README, CLAUDE.md, PRD, design spec)
9. Solo project or team?

### Step 2 — Generate the documents

Read `references/templates.md` for the full templates before writing anything.

Create in this order:
1. **`HANDOFF.md`** — the collaboration contract; customize roles, communication rules, workflow
2. **`CONTEXT.md`** — current project snapshot; fill in from what the user described
3. **`DECISIONS.md`** — pre-populate with any decisions the user mentioned; use correct category prefixes
4. **`conversations/`** — create the directory (first session log goes here at end of this session)

**Customization rules — apply without being asked:**
- Replace every `{placeholder}` — no placeholders survive into the final file
- Match the user's language throughout: if they wrote in Chinese, all docs should be in Chinese
- Designer / vibe coder: full change-reporting + checkpoint workflow by default
- Developer: can simplify change reporting, batch mode acceptable
- Non-code project (writing, research, design): replace code-specific terms with domain equivalents ("data model" → "content structure", "refactoring" → "restructuring")
- If the project already has a `CLAUDE.md` or similar, offer to integrate rather than create a parallel system

### Step 3 — Walk the user through the result

Don't just say "done." Present each document with a one-paragraph summary of what it does and why. Ask if anything feels off or needs adjusting.

### Step 4 — Offer optional add-ons

Based on what you learned, suggest (don't auto-create):
- **`CODE_RULES.md`** — if the project has code and the user cares about conventions
- **`DESIGN_TOKENS.md`** — if the project has UI and visual specs matter

### Step 5 — End of setup session

Create the first `conversations/YYYY-MM-DD.md` entry to record what was decided during setup. This anchors the first session and gives future sessions a baseline.

---

## Mode B: Maintenance Protocol

### On Session Start (automatic)

1. Read `HANDOFF.md` → understand the working agreement
2. Read `CONTEXT.md` → understand where the project is
3. Read `DECISIONS.md` → load the locked decisions into context
4. Check for today's `conversations/YYYY-MM-DD.md` → pick up from where the last session left off
5. Confirm with the user briefly:

```
I've read the project docs. Here's where we are:

Project: [name — one-line description]
Phase: [current phase from CONTEXT.md]
Last session: [date — key things that happened]
Ready to continue with: [next steps from CONTEXT.md]

Which of these should we tackle, or is there something else?
```

If CONTEXT.md looks stale (last-updated date is old, or "In Progress" items look completed), flag it: "CONTEXT.md hasn't been updated since [date] — want me to refresh it before we start?"

### During the Session

**Decision tracking:**
- When the user confirms a choice — "yes", "let's go with that", "that's final", "lock it in" — offer to log it to DECISIONS.md
- Format: add a row to the right category table with ID, decision, reason, and today's date
- If no category fits, create one with a sensible prefix

**Respecting DECISIONS.md:**
- Before proposing any approach, check if it contradicts an existing decision
- If the user asks for something that conflicts, surface the conflict explicitly:
  ```
  Heads up — this conflicts with [D-X]: "[decision text]" (logged [date]).
  The reason was: [reason].
  Want to revise that decision, or approach this differently?
  ```
- Never silently override. Decisions persist until explicitly revised.

**Task breakdown:**
- When a request involves multiple changes, decompose it first:
  ```
  I'll break this into steps:
  1. [ ] [Specific change]
  2. [ ] [Specific change]
  3. [ ] [Specific change]
  
  Confirm and I'll start from #1.
  ```
- Execute one at a time. Wait for "continue" / "next" / "go ahead" before proceeding.
- If the user says "just do it all" — respect that. But still report all changes at the end.

**Change reporting — mandatory, not optional:**
- After every modification, state what changed and from what to what
- For UI work: before → after pixel values (font size, padding, color, radius, etc.)
- For logic/code: which files changed, behavior before vs. after, any data structure changes called out separately
- Never just say "done" or "fixed it" — the user needs to know what changed to give meaningful feedback

### On Session End (or natural pause)

Offer to do these — don't do them silently:

1. **Update CONTEXT.md** — move completed items, update current phase, add new next-steps
2. **Write `conversations/YYYY-MM-DD.md`** — summarize decisions, work completed, open questions, where to pick up
3. **Sync DECISIONS.md** — log anything confirmed during the session that wasn't recorded yet

Template for offering: "We're at a good stopping point. Want me to update CONTEXT.md and write a session log?"

---

## Edge Cases

### Mid-project adoption
Project exists with history but no collab docs yet:
- Read existing files (README, CLAUDE.md, etc.) to pre-populate CONTEXT.md and DECISIONS.md
- Ask: "I can see [these patterns/choices] in the existing files — should I log these as confirmed decisions?"
- Don't invent decisions the user hasn't confirmed

### User wants to change a locked decision
1. Show the current entry from DECISIONS.md
2. Confirm the user wants to revise it explicitly
3. Update in place (don't delete — update with new content and new date)
4. Add a note in the reason field: `Revised from: {old decision}`

### Multiple people using the docs
- Add each person's role to HANDOFF.md
- Add a "Confirmed by" column to DECISIONS.md
- Note who was present in session logs

### User says "skip the checklist, just do it"
Respect this completely — but still report what changed afterward. The checklist is skippable. The change report is not.

### User is frustrated / wants to move faster
Switch to batch mode: group related changes, execute together, give one consolidated report. Still respect DECISIONS.md. Still report changes.

### HANDOFF.md exists but user opens a totally different project
Don't assume — confirm: "I see this project has collab docs. Are we working on [project name] today, or something different?"

---

## Document Purpose Summary

| Document | One job | One rule |
|----------|---------|----------|
| `HANDOFF.md` | Define HOW we work | Read first every session |
| `CONTEXT.md` | Show WHERE we are | Keep it current |
| `DECISIONS.md` | Record WHAT's been decided | Never silently override |
| `conversations/` | Remember WHAT HAPPENED | Write at every pause |

These are small, flat Markdown files. No tooling, no schema, no build step. Any AI that can read files can use them. That's the point — zero friction to adopt, zero friction to maintain.
