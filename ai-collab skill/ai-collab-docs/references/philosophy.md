# Why This System Exists — Philosophy & Rationale

> This document is for humans who want to understand the design thinking behind the collaboration docs system. If you just want to use it, read SKILL.md instead.

---

## The Problem

AI is stateless. Every new conversation starts from a blank slate. This creates three compounding problems:

### 1. The Context Tax

Every session, you spend the first 10-15 minutes re-explaining:
- What the project is
- What you've already built
- What decisions you've made
- Where you left off

This isn't just annoying — it's expensive. It eats into context window, burns tokens, and mentally drains the human who has to reconstruct everything from memory.

### 2. Decision Drift

Without a persistent record, AI will happily re-propose something you rejected last week. Worse, it might quietly undo a design choice you carefully made three sessions ago while "improving" something nearby. You end up playing whack-a-mole with your own decisions.

### 3. The Blast Radius Problem

When you say "make the header feel more spacious," a helpful AI might adjust padding, font size, line height, margin, and border radius all at once. If the result looks wrong, you can't tell which change caused it. You revert everything and start over. Progress turns into loops.

---

## The Solution: Four Documents, Four Jobs

The insight is simple: **if AI is stateless, give it state through files.**

But not one giant file — that becomes a dumping ground nobody maintains. Instead, four small files, each with exactly one purpose:

```
HANDOFF.md    →  HOW we work together     (the contract)
CONTEXT.md    →  WHERE the project is now  (the snapshot)
DECISIONS.md  →  WHAT has been decided     (the constitution)
conversations/ →  WHAT happened when       (the memory)
```

### Why four and not one?

Because they change at different speeds:

- **HANDOFF.md** changes rarely — maybe once or twice in a project's lifetime. It's your working agreement.
- **CONTEXT.md** changes every session. It's always a live snapshot of "right now."
- **DECISIONS.md** only grows. Each entry is append-only (unless explicitly revised). It's your source of truth.
- **conversations/** is write-once-read-maybe. You rarely go back to old logs, but when you need them, they're there.

Putting all of this in one file means everything changes at the frequency of the fastest-changing part, which makes the stable parts feel unreliable.

---

## Design Principles

### 1. Files over memory, structure over volume

AI can read files reliably. It cannot reliably remember what you said three sessions ago. By putting context into files, you're using the one mechanism that actually persists across sessions.

But structure matters more than volume. A 200-line CONTEXT.md that's disorganized is worse than a 20-line one with clear sections. The documents are designed to be scannable — AI should be able to read all four in under 10 seconds and know exactly where to pick up.

### 2. Decisions are append-only

The single most impactful rule in this system is: **DECISIONS.md entries cannot be silently overridden.** 

This mimics how good human teams work. You don't revisit every decision every meeting — you trust that past decisions stand unless someone explicitly brings them up for revision. AI needs the same constraint, because without it, every session is a potential reset.

### 3. Checkpoint rhythm over batch freedom

The default workflow is: break task into steps → confirm → execute one → report → wait → next.

This feels slow, but it's actually faster. Here's why:
- Catching a wrong direction after 1 step costs 2 minutes to fix
- Catching a wrong direction after 10 steps costs 30 minutes to untangle
- The overhead of confirming each step is ~5 seconds

The math heavily favors checkpoints, especially for design-sensitive work where "correct" is subjective.

### 4. Change reports are mandatory, not optional

"Done" is not a valid status report. The rule is: after every change, state what changed, from what to what.

This isn't bureaucracy — it's the difference between a collaborator and a black box. When AI says "I changed the header padding from 16px to 24px and the font weight from 400 to 500," the human can instantly judge whether that's right. When AI says "I updated the header styling," the human has to go look at the diff themselves.

### 5. The human decides, AI executes and suggests

AI should absolutely suggest approaches, flag potential issues, and offer alternatives. But the decision to proceed is always the human's. This is especially important for:
- Anything that touches visual design (subjective)
- Anything that changes data structures (hard to reverse)
- Anything that adds scope (easy to bloat)

AI that acts autonomously in these areas isn't being helpful — it's creating review work.

---

## Why Markdown?

- **Zero dependencies**: No special tools, no database, no hosting. Just files.
- **Universally readable**: Every AI model, every text editor, every platform can handle Markdown.
- **Version-controllable**: Lives in git alongside the code. Changes are trackable.
- **Human-editable**: When the AI is wrong, the human can just open the file and fix it.
- **Portable**: Switching AI tools? The documents come with you. They're not locked into any platform.

---

## Common Objections

### "This is overhead — I just want to code"

The setup takes ~5 minutes. The time saved per session is ~10-15 minutes. By session 2, you're net positive. By session 10, you've saved over an hour of re-explaining.

### "AI should just remember things"

Even AI tools with built-in memory struggle with structured project state. Memory is great for preferences ("I like terse responses") but terrible for "here are the 12 decisions we've made about the data model." Files are more reliable, more reviewable, and more portable.

### "I'll forget to maintain the docs"

That's why maintenance is built into the workflow. The AI is instructed to offer updates at natural pauses. You just say "yes" or "not now." The human's job is to decide; the AI's job is to write.

### "Isn't CLAUDE.md enough?"

CLAUDE.md is great for static project-level instructions. But it's not designed for evolving state (CONTEXT.md), locked decisions (DECISIONS.md), or session history (conversations/). The two systems complement each other — CLAUDE.md handles "how this codebase works" while the collab docs handle "how we're building it together."

---

## Lineage

This system was developed through real-world vibe coding projects where a designer (non-coder) collaborated with AI to build iOS apps. The pain points were discovered empirically:

- Context re-explanation was burning 30%+ of each session
- AI kept reverting visual decisions the designer had carefully tuned
- Multi-change requests led to "which change broke it?" debugging loops
- Conversation history was lost between sessions, leading to circular discussions

The four-document system emerged as the minimal structure that solves all four problems without becoming a burden to maintain.
