# Document Templates

> These are starting points — always customize to the specific project. Replace all `{placeholders}`. Remove sections that don't apply. Add sections that are missing.

---

## Table of Contents

1. [HANDOFF.md](#handoffmd)
2. [CONTEXT.md](#contextmd)
3. [DECISIONS.md](#decisionsmd)
4. [conversations/YYYY-MM-DD.md](#conversation-log)
5. [CODE_RULES.md (optional)](#code_rulesmd-optional)
6. [DESIGN_TOKENS.md (optional)](#design_tokensmd-optional)

---

## HANDOFF.md

```markdown
# AI Collaboration Handoff — {Project Name}

> Read this document at the start of every new AI session.

---

## 1. Roles

### User
- {Role and background, e.g., "Product designer, makes all product and visual decisions"}
- {Work style, e.g., "Delegates all code implementation to AI"}
- {What they're good at, e.g., "Strong visual intuition, will give feedback in feelings not pixels"}

### AI
- Responsible for all code writing, modification, and refactoring
- Maintains project documents and context records
- Proactively identifies potential issues — don't wait for user to find bugs
- After every change, report what changed and how — never just say "done"

---

## 2. Communication Rules

- Language: {Chinese / English / etc.}
- Don't show code snippets unless asked — describe what was done and what changed
- When multiple approaches exist, present a brief comparison (2-3 sentences each) and let user choose
- When requirements are unclear, ask before acting — don't assume or guess
- {Add any project-specific rules here}

---

## 3. Session Startup Checklist

Every new session, complete these steps automatically:

1. Read `HANDOFF.md` (this file)
2. Read `CONTEXT.md` (current project state)
3. Read `DECISIONS.md` (locked decisions — do not override)
4. Check for today's `conversations/YYYY-MM-DD.md`
5. Briefly confirm with user: current status and where to continue
6. If task is unclear, ask — don't guess

---

## 4. Change Reporting

### For UI / Visual Changes
Always state before → after values:
- Font size: 14px → 16px
- Spacing: 12px → 16px
- Color: `#333333` → `#1A1A1A`
- Corner radius: 8px → 12px
- Animation: 200ms ease → 300ms ease-out

### For Logic / Structure Changes
- Which files and modules changed
- Behavior before vs. after
- Data structure changes must be called out separately

### Why This Rule Exists
"Made it more spacious" is unjudgeable. "Increased padding from 16px to 24px" lets the user immediately say "yes that's right" or "too much, try 20px." Precise reporting eliminates back-and-forth.

---

## 5. Task Breakdown Protocol

When a request involves multiple changes:

1. **Decompose** — break into independent sub-tasks, present as a numbered checklist
2. **Confirm** — wait for user to approve the list (they may add, remove, or reorder)
3. **Execute one** — do one sub-task, report the result
4. **Wait** — proceed to the next only after user says "continue" / "next" / "go ahead"
5. **Wrap up** — when all tasks are done, update CONTEXT.md

**Example checklist format:**
```
I've broken this into the following steps:

1. [ ] Adjust nav bar height: 44px → 56px
2. [ ] Update card corner radius: 8px → 12px
3. [ ] Change body font size: 14px → 15px

Confirm and I'll start from #1.
```

**When to skip**: If the user says "just do it all" or "skip the checklist" — respect that. But still report all changes afterward.

---

## 6. Boundary Rules

AI must NOT do any of the following without explicit user approval:

| Action | Why it's prohibited |
|--------|-------------------|
| Add features beyond stated scope | Scope creep is the #1 project killer |
| Modify user-approved visuals | "This is fine" means stop touching it |
| Change data models / schemas | Hard to reverse, can break everything |
| Guess at vague requirements | Guessing creates rework; asking takes 10 seconds |
| Skip change reports | The user needs to know what changed to give feedback |
| Break existing behavior while editing nearby code | Fix one thing, don't break another |

---

## 7. How to Handle User Feedback

Users give feedback in three patterns. Handle each differently:

### Pattern A: Feeling-based
> "Too crowded" / "Doesn't feel right" / "Too formal"

→ Translate the feeling into 2-3 specific parameter changes. Present them. Wait for confirmation before executing.

Example: "Too crowded" → "I'll try: increase card spacing from 8px to 16px, reduce font size from 16px to 14px, add 12px padding inside cards. Want me to proceed?"

### Pattern B: Specific values
> "Make it 4px bigger" / "Change to #FF0000"

→ Execute directly. Report the final value.

### Pattern C: Reference-based
> "Like Apple Music's style" / "Similar to this screenshot"

→ Analyze the reference. Extract 3-5 key visual traits. State which dimensions you'll match. Confirm before executing.

Example: "Apple Music vibe → I see: large bold titles, generous whitespace, subtle dividers, dark background. I'll adjust these dimensions: [list]. Proceed?"

---

## 8. File Structure

```
{project-root}/
├── HANDOFF.md            # Collaboration rules (this file)
├── CONTEXT.md            # Current project state
├── DECISIONS.md          # Locked decisions
├── conversations/        # Session archives
│   └── YYYY-MM-DD.md
├── CODE_RULES.md         # Code conventions (optional)
├── DESIGN_TOKENS.md      # Visual specs (optional)
└── {project files}
```

---

## 9. Archiving Rules

### Session Archives (`conversations/YYYY-MM-DD.md`)
- Create at end of each working session
- Content: decisions made, work completed, open questions, where to pick up next
- Format: structured summary — not a transcript

### CONTEXT.md
- Update at end of session or after significant progress
- Must always reflect the current state — never stale

### DECISIONS.md
- Add entries when user explicitly confirms a choice
- Once written, do not revise unless user explicitly says to
- Include the reason — future-you (and future-AI) needs to know *why*
```

---

## CONTEXT.md

```markdown
# {Project Name} — Current State

> Last updated: {YYYY-MM-DD}

## Current Phase

{One paragraph: what stage is the project in, what's the immediate focus}

## Confirmed Framework / Architecture

{Key structural decisions that shape the project — product structure, tech architecture, core models. Reference DECISIONS.md for details.}

## What's Been Completed

- {Milestone 1}
- {Milestone 2}

## In Progress

- {Active work item 1}
- {Active work item 2}

## Next Steps

- [ ] {Task 1 — next thing to do}
- [ ] {Task 2}
- [ ] {Task 3}

## Deliberately Deferred

- {Feature or topic postponed, with brief reason}
- {Another deferred item}
```

---

## DECISIONS.md

```markdown
# {Project Name} — Decision Log

> This file records all confirmed decisions.
> AI must follow these decisions and must not override them.
> New entries are added only after user explicitly confirms.
> To revise a decision, user must explicitly request it.

---

## How to Read This File

Each decision has:
- **# (ID)**: Category prefix + number (e.g., P-1 = Product decision #1)
- **Decision**: What was decided
- **Reason**: Why — this is critical for judging edge cases later
- **Date**: When it was confirmed

---

## Product Direction

| # | Decision | Reason | Date |
|---|----------|--------|------|
| P-1 | {Decision} | {Reason} | {YYYY-MM-DD} |

---

## Technical Architecture

| # | Decision | Reason | Date |
|---|----------|--------|------|
| T-1 | {Decision} | {Reason} | {YYYY-MM-DD} |

---

## Design / Visual

| # | Decision | Reason | Date |
|---|----------|--------|------|
| V-1 | {Decision} | {Reason} | {YYYY-MM-DD} |

---

## Features & Interactions

| # | Decision | Reason | Date |
|---|----------|--------|------|
| F-1 | {Decision} | {Reason} | {YYYY-MM-DD} |

---

## Pending — AI Must Not Decide Independently

The following items have NOT been decided. If encountered during development, ask the user first:

- {Undecided item 1}
- {Undecided item 2}
```

**Category ID conventions:**
- `P-` = Product direction
- `T-` = Technical / architecture
- `D-` = Data model
- `V-` = Visual / design
- `F-` = Feature / interaction
- `I-` = Integration / import / external
- Custom prefixes are fine — just be consistent

---

## Conversation Log

```markdown
# Session — {YYYY-MM-DD}

## Summary

{2-3 sentences: what was the focus of this session, what was the outcome}

## Key Decisions

{Decisions made during this session, with reasoning. These should also be in DECISIONS.md.}

### {Decision topic 1}
- **What**: {What was decided}
- **Why**: {The reasoning process}
- **Impact**: {What this affects going forward}

## Work Completed

- {What was built, changed, or resolved}

## Open Questions

- {Unresolved items that need future attention}

## Next Session

- {Where to pick up next time}
```

---

## CODE_RULES.md (Optional)

Use when the project has code and you want to lock down conventions.

```markdown
# {Project Name} — Code Rules

> All code written by AI must follow these rules. No exceptions without user approval.

## Language & Framework
- {e.g., Swift + SwiftUI, TypeScript + React, Python + FastAPI}

## Naming Conventions
- {e.g., camelCase for variables, PascalCase for types}

## File Organization
- {e.g., one component per file, group by feature not by type}

## Dependencies
- {e.g., no third-party libraries without approval, use system APIs first}

## Error Handling
- {e.g., use Result type, no force unwraps, fail loudly in debug}

## Testing
- {e.g., unit tests for business logic, UI tests for critical flows}

## What NOT to Do
- {e.g., no premature abstraction, no "just in case" code}
```

---

## DESIGN_TOKENS.md (Optional)

Use when the project has UI and you want to lock down visual specs.

```markdown
# {Project Name} — Design Tokens

> These values are locked. AI must use these exact values and not improvise.
> Changes require user approval and must be updated here first.

## Colors

| Token | Value | Usage |
|-------|-------|-------|
| primary | {#hex} | {Where it's used} |
| background | {#hex} | {Where it's used} |
| text-primary | {#hex} | {Where it's used} |

## Typography

| Style | Font | Size | Weight | Line Height |
|-------|------|------|--------|-------------|
| heading-1 | {font} | {size} | {weight} | {height} |
| body | {font} | {size} | {weight} | {height} |

## Spacing

| Token | Value | Usage |
|-------|-------|-------|
| space-xs | {value} | {Where} |
| space-sm | {value} | {Where} |
| space-md | {value} | {Where} |

## Corner Radius

| Token | Value | Usage |
|-------|-------|-------|
| radius-sm | {value} | {Where} |
| radius-md | {value} | {Where} |

## Animation

| Token | Duration | Easing | Usage |
|-------|----------|--------|-------|
| transition-fast | {ms} | {curve} | {Where} |
| transition-normal | {ms} | {curve} | {Where} |
```
