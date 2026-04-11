# Examples — Good vs. Bad Patterns

> This file shows what the collaboration docs system looks like in practice. Use these when you're uncertain how something should look, or when a user asks "what does a good X look like?"

---

## Table of Contents

1. [CONTEXT.md: Good vs. Bad](#1-contextmd)
2. [DECISIONS.md: Good vs. Bad](#2-decisionsmd)
3. [Change Reporting: Good vs. Bad](#3-change-reporting)
4. [Task Breakdown: Good vs. Bad](#4-task-breakdown)
5. [Feedback Handling: Good vs. Bad](#5-feedback-handling)
6. [Session Startup: Good vs. Bad](#6-session-startup)
7. [Conversation Log: Good vs. Bad](#7-conversation-log)
8. [Full Scenario Walkthroughs (4 project types)](#8-full-scenario-walkthroughs)

---

## 1. CONTEXT.md

### Bad — vague, stale, no actionable information

```markdown
# MyApp — Current State

We're building an app. The main screen is mostly done. There are some bugs.
Next steps: keep working on it.
```

Problems: no date, no specifics, "mostly done" and "some bugs" mean nothing to an AI starting fresh, no structure.

### Good — specific, dated, scannable

```markdown
# Poki — Current State

> Last updated: 2026-03-31

## Current Phase

Product framework restructuring complete. Established "Collector + Notebook" dual structure,
replacing the previous "Five Tools" architecture. No technical or visual implementation started yet.

Immediate goal: Build a SwiftUI demo to present the product framework and interaction logic.

## Confirmed Framework / Architecture

- iOS only, Swift + SwiftUI + SwiftData
- Local storage only (no backend for MVP)
- "Collector + Notebook" dual structure: Collector for outward capture, Notebook for inward reflection

## What's Been Completed

- Product philosophy: "A tool that gives curiosity a place to land"
- Core interaction flow: aim → auto-identify → learn → collect
- Three usage paths: full / curiosity-only / impulse-collect

## In Progress

- Info card content structure definition
- Notebook editor interaction design

## Next Steps

- [ ] Define the info card content structure (what users see after tapping a subject)
- [ ] Design the notebook editor's basic interactions
- [ ] Plan the SwiftUI demo scope

## Deliberately Deferred

- Sharing features (future phase, after MVP)
- Visual design details (after framework is locked)
- Monetization strategy
```

---

## 2. DECISIONS.md

### Bad — no reason, no date, ambiguous

```markdown
# Decisions

- Use SwiftUI
- No backend
- Keep it simple
- The design should be clean
```

Problems: no IDs, no reasons, no dates. "Keep it simple" and "clean design" are not decisions — they're vibes. An AI can't use these to prevent decision drift.

### Good — structured, reasoned, traceable

```markdown
## Technical Architecture

| # | Decision | Reason | Date |
|---|----------|--------|------|
| T-1 | iOS only, Swift + SwiftUI | Target platform for MVP; team has iOS familiarity | 2026-03-25 |
| T-2 | SwiftData for storage, no backend | MVP stays local-only; simplest path to ship | 2026-03-25 |
| T-3 | No third-party libraries without approval | Keep dependency surface minimal and controllable | 2026-03-28 |

## Visual Design

| # | Decision | Reason | Date |
|---|----------|--------|------|
| V-1 | Brand keywords: restrained, cinematic, ceremonial, light | Foundation for all visual decisions; reference point for "does this feel right" | 2026-03-28 |
| V-2 | Ticket stub is the ONLY carrier form — no pebbles, receipts, cards | Unified identity creates product memorability; multiple carriers add choice fatigue and conflict with the "light" principle | 2026-03-28 |
```

Notice V-2: it records not just the decision but also what was considered and rejected. This prevents an AI three sessions later from suggesting "what if we also had a receipt style?"

---

## 3. Change Reporting

### Bad

> "I updated the header styling to look better."

> "Fixed the layout issues."

> "Done."

Problems: What changed? From what to what? The user can't judge whether the change was correct, and has to go look at the code or UI themselves.

### Good — UI change

> "Adjusted the ticket stub layout:
> - Title font size: 18px → 22px (better readability at arm's length)
> - Card padding: 12px → 16px all sides
> - Corner radius: 8px → 12px (softer feel)
> - Shadow: added `0 2px 8px rgba(0,0,0,0.08)` (subtle depth)
>
> No changes to colors or typography weight."

The user can immediately say: "Title size is too big, try 20px. Rest looks good."

### Good — logic/code change

> "Refactored the photo import flow:
> - **Before**: All 20 photos processed sequentially, UI blocked until complete (~8 seconds)
> - **After**: First 5 processed immediately; remaining 15 queued for background processing
> - **Files changed**: `ImportManager.swift`, `PhotoQueue.swift` (new file)
> - **Behavior change**: Users see results in ~2 seconds instead of waiting for all 20
> - **No changes to**: data model, storage format, or existing photo records"

### Good — non-code change (writing project)

> "Restructured the introduction section:
> - Moved the 'why this matters' paragraph from position 3 → position 1 (hook comes first)
> - Shortened the methodology overview from 6 sentences to 3 (the detail moves to Section 2)
> - Kept all original content — nothing deleted, only rearranged and trimmed
>
> Word count: 420 → 310 words in the intro."

---

## 4. Task Breakdown

### Bad — dumping everything at once

User: "Make the home screen look more polished"

AI immediately changes 15 things across 6 files, then says "I've polished the home screen."

User: "Wait, the calendar looks wrong now..."

Now you can't tell which of the 15 changes caused it. You revert everything. Net: zero progress and wasted time.

### Good — checkpoint rhythm

User: "Make the home screen look more polished"

AI:
```
I'll break this into specific adjustments:

1. [ ] Increase section spacing: 8px → 16px between calendar and recent records
2. [ ] Soften card shadows: current shadow → 0 2px 8px rgba(0,0,0,0.06)
3. [ ] Align typography: standardize section headers to 15px medium weight
4. [ ] Add breathing room: screen edge padding 16px → 20px

Want me to adjust this list, or start from #1?
```

User: "Skip #3, the typography is fine. Do the rest."

AI executes #1, reports the change, waits. Then #2. Then #4. Each step is reviewable in isolation. When #2 looks wrong, you know exactly what caused it.

---

## 5. Feedback Handling

### Pattern A: Feeling-based feedback

**User**: "The ticket stub feels too heavy"

**Bad**: *silently reduces font size, padding, and shadow all at once*

**Good**:
> "Heavy" could mean a few things. Here's what I'd try:
> - Shadow intensity: `rgba(0,0,0,0.15)` → `rgba(0,0,0,0.06)`
> - Border: `1px solid #CCC` → `1px solid #E5E5E5`
> - Internal whitespace: padding 12px → 16px (counterintuitively, more space can feel lighter)
>
> Want me to try all three, or start with one?

### Pattern B: Reference-based feedback

**User**: "I want it to feel like opening a film ticket at an art house cinema"

**Bad**: *adds a bunch of decorative elements and vintage textures*

**Good**:
> From that reference, I'm picking up:
> - **Muted palette** — cream/warm gray rather than pure white
> - **Generous margins** — content feels placed, not packed
> - **Minimal decoration** — typography does the work, not borders or icons
> - **Intentional quietness** — no loud colors, no attention-grabbing elements
>
> I'll start with the color palette: current background is `#FFFFFF`, I'd try `#F8F6F1`. Confirm?

### Pattern C: Specific values

**User**: "Change the button radius to 6px"

**Good**: Just do it. Report the result: "Button corner radius: 8px → 6px."

No need to ask for confirmation on specific values. Execute and confirm.

---

## 6. Session Startup

### Bad — no context, jumps straight in

> "Hi! What would you like to work on today?"

The user now has to spend 5-10 minutes re-explaining the project.

### Good — reads docs, confirms state

> "I've read the project docs. Here's where we are:
>
> **Project**: Poki — curiosity-driven collector app for iOS
> **Phase**: Product framework done, no code written yet
> **Last session** (2026-03-31): Finalized the Collector + Notebook dual structure
> **Ready to pick up**: Info card content structure (the agreed next step)
>
> Shall we start with that, or is there something else on your mind?"

User can immediately respond "yes, let's do the info card" instead of reconstructing context.

---

## 7. Conversation Log

### Bad — too vague to be useful next time

```markdown
# Session — 2026-03-31

Talked about the product. Made some decisions about the structure.
Will continue next time.
```

### Good — captures reasoning, not just outcomes

```markdown
# Session — 2026-03-31

## Summary

Deep product framework discussion. Replaced the "Five Tools" structure with a
"Collector + Notebook" dual structure. Established the collector's interaction
flow and product identity direction.

## Key Decisions

### Why "Collector" instead of "Camera"
Camera = passive recording. But users aren't documenting — they're actively
acquiring things from the world. "Collector" implies agency and intent. Logged as P-1.

### Why two tools, not tabs?
Collector (outward) and Notebook (inward) serve fundamentally different mental
states. They're not views of the same thing — they're different tools on the
same desk. UI metaphor: whoever has focus gets the full screen; the other peeks from the corner.

## Work Completed

- Defined product philosophy: "A tool that gives curiosity a place to land"
- Established four-layer curiosity model: see → curious → own → show
- Designed collector flow: aim → auto-ID → learn → collect

## Open Questions

- Info card content structure (what shows for different item types?)
- Notebook editor basic interactions
- SwiftUI demo scope and implementation path

## Next Session

Start with info card content structure — it's the most uncertain piece and
blocks the demo planning.
```

---

## 8. Full Scenario Walkthroughs

Four different project types to show how the system adapts.

---

### Scenario A: iOS App (Developer + Designer vibe coding)

**Project**: A personal finance tracker built in Swift

**Session 1: Setup**

User: "I'm building a budgeting app called Ledge. I'm a developer but I'm using AI to move faster. Help me set up collab docs."

AI: Runs setup workflow, asks questions, learns the project is Swift/SwiftUI + SwiftData, early build stage, solo project, developer mode (batch is fine, but change reports still required).

Docs created:
- `HANDOFF.md` — batch mode allowed, change reports required, developer working style
- `CONTEXT.md` — project at inception, no code yet, tech stack confirmed
- `DECISIONS.md` — T-1 (Swift/SwiftUI), T-2 (SwiftData local-only), populated from setup conversation
- `conversations/2026-04-01.md` — setup session record

**Session 2: New conversation, HANDOFF.md detected**

AI reads docs automatically, opens with:

> "I've read the Ledge project docs. We're at the beginning — tech stack confirmed (Swift + SwiftUI + SwiftData), no code yet. Ready to start on [next step from CONTEXT.md]?"

User: "Let's build the transaction entry screen."

AI decomposes, executes, reports. At the end: "Want me to update CONTEXT.md and log this session?"

---

### Scenario B: Full-Stack Web App (Python backend + React frontend)

**Project**: An internal dashboard for a small team

**Setup chat:**

AI asks:
- Stack? → "Python FastAPI + React + PostgreSQL"
- Stage? → "Mid-development, the API is mostly done, frontend just started"
- Decisions already made? → "REST only, no GraphQL. PostgreSQL schema is locked. We use Tailwind for UI."

DECISIONS.md pre-populated:
```
| T-1 | REST API only, no GraphQL | Simpler for team, existing tools support it well | 2026-03-10 |
| T-2 | PostgreSQL schema locked — no migrations without review | Breaking changes too costly at this stage | 2026-03-10 |
| V-1 | Tailwind CSS for all styling — no custom CSS files | Consistency, no context-switching | 2026-03-15 |
```

**Later session: Decision conflict**

User: "Hey, can you add a GraphQL endpoint for the analytics queries? REST is getting verbose."

AI:
> "Heads up — this conflicts with T-1: 'REST API only, no GraphQL.' The reason was: simpler for the team, existing tools support it well.
>
> Want to revise that decision, or should we explore a way to make the REST endpoint less verbose instead?"

User: "Oh right. Let's try a REST approach first."

AI: Does not implement GraphQL. Decision T-1 stands. The system worked.

---

### Scenario C: Non-Code Project (UX Research + Report Writing)

**Project**: A UX research report on food delivery app pain points

This shows that the system works for non-code projects — "data model" becomes "content structure," "refactoring" becomes "restructuring."

**Setup:**

AI adapts the templates:
- HANDOFF.md uses: "sections" not "files", "restructuring" not "refactoring", "content decisions" not "architecture"
- DECISIONS.md categories: Content Direction (C-), Scope (S-), Format (F-)

**CONTEXT.md example for this project:**

```markdown
# Food Delivery UX Report — Current State

> Last updated: 2026-04-08

## Current Phase

Data collection complete (8 interviews + 200 survey responses). Analysis in progress.
Current focus: synthesizing interview themes into the report's Findings section.

## Content Structure Confirmed

- 5 sections: Executive Summary, Methodology, Findings, Recommendations, Appendix
- Each finding structured as: Observation → Evidence → Impact → Recommendation

## What's Been Completed

- Interview transcripts reviewed and coded
- 4 major theme clusters identified
- Survey data analyzed (key stats extracted)

## In Progress

- Drafting Findings section — 2 of 4 themes written

## Next Steps

- [ ] Draft themes 3 and 4 in Findings
- [ ] Write Recommendations section (flows from Findings)
- [ ] Executive Summary last (after Findings are locked)

## Deliberately Deferred

- Visual design of charts (after content is final)
- Stakeholder distribution format (not decided yet)
```

**DECISIONS.md example:**

```markdown
## Scope

| # | Decision | Reason | Date |
|---|----------|--------|------|
| S-1 | Report covers only iOS app, not web | Interview sample was iOS-only | 2026-04-05 |
| S-2 | Do not include competitor analysis | Out of scope for this engagement | 2026-04-05 |

## Format

| # | Decision | Reason | Date |
|---|----------|--------|------|
| F-1 | Each finding must cite at least 2 interview quotes | Credibility; avoids purely anecdotal claims | 2026-04-06 |
| F-2 | Executive summary is 1 page max | Stakeholder constraint — they won't read more | 2026-04-06 |
```

---

### Scenario D: Mid-Project Adoption (Project already exists, no collab docs yet)

**Project**: A Python CLI tool that's been developed for 3 months without collab docs

**User**: "I've been building this for a while. Can you help me set up collab docs now?"

AI runs the mid-project adoption path:
1. Reads existing `README.md`, `CLAUDE.md`, and source files
2. Surfaces what it finds: "I can see this uses Click for the CLI framework, stores config in `~/.config/toolname/`, and has 3 subcommands. Should I log these as confirmed decisions?"
3. User: "Yes, and add that we're not adding any more subcommands until v2."
4. AI creates docs and pre-populates DECISIONS.md with what it found plus the new decision

DECISIONS.md result:
```markdown
## Technical Architecture

| # | Decision | Reason | Date |
|---|----------|--------|------|
| T-1 | Click for CLI framework | Already in use, no reason to change | 2026-04-01 |
| T-2 | Config stored in ~/.config/toolname/ | Follows XDG convention, consistent with other CLI tools | 2026-04-01 |

## Product Direction

| # | Decision | Reason | Date |
|---|----------|--------|------|
| P-1 | No new subcommands until v2 | Current 3 subcommands cover the core use case; stability over features for now | 2026-04-01 |
```

The key rule for mid-project adoption: **don't invent decisions the user hasn't confirmed.** Only log what's explicit — either what already exists in code/docs, or what the user confirms during setup.
