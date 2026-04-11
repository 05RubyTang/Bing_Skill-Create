#!/bin/bash

# =============================================================================
# AI Collaboration Docs — Setup Script
# =============================================================================
# Creates the four collaboration documents (HANDOFF.md, CONTEXT.md,
# DECISIONS.md, conversations/) in the current directory.
#
# Usage:
#   bash setup.sh              # Interactive setup in current directory
#   bash setup.sh /path/to/project  # Setup in a specific directory
# =============================================================================

set -e

# ─── Config ───────────────────────────────────────────────────────────────────

TARGET_DIR="${1:-.}"
TODAY=$(date +%Y-%m-%d)

# ─── Colors ───────────────────────────────────────────────────────────────────

BOLD="\033[1m"
GREEN="\033[0;32m"
YELLOW="\033[0;33m"
CYAN="\033[0;36m"
RESET="\033[0m"

# ─── Helpers ──────────────────────────────────────────────────────────────────

print_header() {
  echo ""
  echo -e "${BOLD}${CYAN}$1${RESET}"
  echo -e "${CYAN}$(printf '─%.0s' {1..60})${RESET}"
}

print_step() {
  echo -e "${GREEN}▸${RESET} $1"
}

print_warning() {
  echo -e "${YELLOW}⚠ $1${RESET}"
}

ask() {
  local prompt="$1"
  local default="$2"
  local response

  if [ -n "$default" ]; then
    echo -ne "${BOLD}$prompt${RESET} [${default}] "
  else
    echo -ne "${BOLD}$prompt${RESET} "
  fi

  read -r response
  echo "${response:-$default}"
}

ask_choice() {
  local prompt="$1"
  local options="$2"
  echo -e "${BOLD}$prompt${RESET}"
  echo "  $options"
  echo -n "  Choice: "
  read -r response
  echo "$response"
}

# ─── Check for existing docs ──────────────────────────────────────────────────

print_header "AI Collaboration Docs — Setup"

if [ -f "$TARGET_DIR/HANDOFF.md" ]; then
  print_warning "HANDOFF.md already exists in $TARGET_DIR"
  echo ""
  echo -n "Overwrite existing docs? [y/N] "
  read -r confirm
  if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Aborted. Existing docs are unchanged."
    exit 0
  fi
fi

# ─── Interview ────────────────────────────────────────────────────────────────

print_header "Step 1: Tell me about your project"

echo ""
PROJECT_NAME=$(ask "Project name:")
PROJECT_DESC=$(ask "One-line description (what does it do, for whom?):")
USER_ROLE=$(ask "Your role (e.g., 'developer', 'designer doing vibe coding', 'PM prototyping'):")
TECH_STACK=$(ask "Tech stack or tools (or 'none' for non-code projects):")
STAGE=$(ask_choice "Current stage:" "1=idea  2=early-build  3=mid-development  4=polishing  5=shipped")

case "$STAGE" in
  1) STAGE_LABEL="Idea / pre-build" ;;
  2) STAGE_LABEL="Early build" ;;
  3) STAGE_LABEL="Mid-development" ;;
  4) STAGE_LABEL="Polishing" ;;
  5) STAGE_LABEL="Shipped / maintenance" ;;
  *) STAGE_LABEL="$STAGE" ;;
esac

echo ""
LANGUAGE=$(ask "Language for docs (e.g., English, 中文):" "English")
RHYTHM=$(ask_choice "Collaboration rhythm:" "1=checkpoint (step-by-step, AI waits for approval)  2=batch (AI does a chunk, then reports)")

case "$RHYTHM" in
  1) RHYTHM_LABEL="Checkpoint" ; RHYTHM_DESC="AI breaks tasks into steps, waits for approval before each" ;;
  2) RHYTHM_LABEL="Batch" ; RHYTHM_DESC="AI executes a group of changes, then reports all at once" ;;
  *) RHYTHM_LABEL="Checkpoint" ; RHYTHM_DESC="AI breaks tasks into steps, waits for approval before each" ;;
esac

echo ""
echo "Any existing decisions that AI should never revisit?"
echo "(Press Enter to skip, or type them one per line. Empty line to finish.)"
EXISTING_DECISIONS=()
while true; do
  echo -n "  Decision (or Enter to skip/finish): "
  read -r decision
  [ -z "$decision" ] && break
  EXISTING_DECISIONS+=("$decision")
done

# ─── Create directory ─────────────────────────────────────────────────────────

print_header "Step 2: Creating documents"

mkdir -p "$TARGET_DIR/conversations"
print_step "Created conversations/ directory"

# ─── HANDOFF.md ───────────────────────────────────────────────────────────────

cat > "$TARGET_DIR/HANDOFF.md" << HANDOFF
# AI Collaboration Handoff — ${PROJECT_NAME}

> Read this document at the start of every new AI session. This is the collaboration contract.

---

## 1. Project Overview

**Name**: ${PROJECT_NAME}
**Description**: ${PROJECT_DESC}
**Stage**: ${STAGE_LABEL}
**Tech stack**: ${TECH_STACK}

---

## 2. Roles

### ${USER_ROLE^} (Human)
- Makes all product, design, and direction decisions
- Reviews and approves AI's work before it's considered done
- Provides feedback — feelings, references, or specific values are all valid

### AI
- Responsible for execution: writing, modifying, refactoring, restructuring
- Maintains CONTEXT.md, DECISIONS.md, and conversation logs
- Proactively flags issues — does not wait for the human to find problems
- After every change, reports what changed and how — never just says "done"

---

## 3. Communication Rules

- **Language**: ${LANGUAGE}
- Don't show code snippets unless explicitly asked — describe what was done and what changed
- When multiple approaches exist, present a brief comparison (2–3 sentences each) and let the human choose
- When requirements are unclear, ask before acting — don't assume or guess
- Match the human's energy and level of detail in responses

---

## 4. Session Startup Checklist

Every new session, complete these steps before starting work:

1. Read \`HANDOFF.md\` (this file)
2. Read \`CONTEXT.md\` (current project state)
3. Read \`DECISIONS.md\` (locked decisions — do not override)
4. Check for today's \`conversations/${TODAY}.md\`
5. Confirm with human: current status and where to continue
6. Flag any stale information in CONTEXT.md

---

## 5. Collaboration Rhythm

**Mode**: ${RHYTHM_LABEL}
**How it works**: ${RHYTHM_DESC}

When a request involves multiple changes:
1. **Decompose** — break into numbered steps, present as a checklist
2. **Confirm** — wait for human to approve (they may adjust the list)
3. **Execute** — one step at a time
4. **Report** — state what changed before moving to the next step
5. **Wait** — don't proceed until human says "continue" / "next" / "go ahead"

**Exception**: If human says "just do it all" or "skip the checklist" — respect that. But still report all changes afterward.

---

## 6. Change Reporting Rules

After every modification, state what changed. Never just say "done."

**For UI / visual changes** — always give before → after values:
- Font size: 14px → 16px
- Padding: 12px → 16px
- Color: \`#333333\` → \`#1A1A1A\`
- Corner radius: 8px → 12px

**For logic / code changes**:
- Which files changed
- Behavior before vs. after
- Data structure changes must be called out separately

**Why**: "I made it more spacious" is unjudgeable. "I increased padding from 16px to 24px" lets the human immediately say yes or no.

---

## 7. Boundary Rules

Do NOT do any of the following without explicit approval:

| Action | Why |
|--------|-----|
| Add features beyond the stated scope | Scope creep is the #1 project killer |
| Modify approved visuals or decisions | "This is fine" means stop touching it |
| Change data models / schemas | Hard to reverse, can break everything |
| Guess at vague requirements | Guessing creates rework; asking takes 10 seconds |
| Skip change reports | The human needs to know what changed to give feedback |

---

## 8. Handling User Feedback

**Feeling-based** ("too crowded", "doesn't feel right"):
→ Translate into 2–3 specific parameter changes. Present them. Wait for confirmation.

**Specific values** ("make it 4px bigger", "change to #FF0000"):
→ Execute directly. Report the final value.

**Reference-based** ("like Apple Music's style"):
→ Analyze the reference, extract 3–5 key traits, state what you'll match. Confirm before executing.

---

## 9. File Structure

\`\`\`
$(basename "$TARGET_DIR")/
├── HANDOFF.md            ← Collaboration rules (this file)
├── CONTEXT.md            ← Current project state
├── DECISIONS.md          ← Locked decisions
├── conversations/        ← Session archives
│   └── YYYY-MM-DD.md
└── [project files]
\`\`\`
HANDOFF

print_step "Created HANDOFF.md"

# ─── CONTEXT.md ───────────────────────────────────────────────────────────────

cat > "$TARGET_DIR/CONTEXT.md" << CONTEXT
# ${PROJECT_NAME} — Current State

> Last updated: ${TODAY}

## Current Phase

${STAGE_LABEL}. ${PROJECT_DESC}

## Confirmed Framework / Architecture

${TECH_STACK}

## What's Been Completed

- Project initialized with AI collaboration docs

## In Progress

- (Add current work items here)

## Next Steps

- [ ] (Add the first concrete next step here)

## Deliberately Deferred

- (Add features or decisions intentionally postponed, with brief reason)
CONTEXT

print_step "Created CONTEXT.md"

# ─── DECISIONS.md ─────────────────────────────────────────────────────────────

# Build initial decisions table
DECISIONS_TABLE=""
DECISION_NUM=1
for decision in "${EXISTING_DECISIONS[@]}"; do
  DECISIONS_TABLE+="| P-${DECISION_NUM} | ${decision} | Confirmed during setup | ${TODAY} |"$'\n'
  ((DECISION_NUM++))
done

if [ -z "$DECISIONS_TABLE" ]; then
  DECISIONS_TABLE="| P-1 | (No decisions logged yet) | — | — |"
fi

cat > "$TARGET_DIR/DECISIONS.md" << DECISIONS
# ${PROJECT_NAME} — Decision Log

> This file records all confirmed decisions.
> AI must follow these decisions and must not override them silently.
> New entries are added only after the human explicitly confirms.
> To revise a decision, the human must explicitly request it.

---

## How to Read This File

Each decision has:
- **#**: Category prefix + number (P-1 = Product decision #1, T-1 = Technical #1, etc.)
- **Decision**: What was decided
- **Reason**: Why — critical for judging edge cases in future sessions
- **Date**: When it was confirmed

Category prefixes: P- Product · T- Technical · D- Data model · V- Visual/design · F- Feature · I- Integration

---

## Product Direction

| # | Decision | Reason | Date |
|---|----------|--------|------|
${DECISIONS_TABLE}

---

## Technical Architecture

| # | Decision | Reason | Date |
|---|----------|--------|------|
| T-1 | (No decisions logged yet) | — | — |

---

## Visual / Design

| # | Decision | Reason | Date |
|---|----------|--------|------|
| V-1 | (No decisions logged yet) | — | — |

---

## Pending — AI Must Not Decide Independently

The following items have NOT been decided. If encountered during development, ask the human first:

- (Add undecided items here as they come up)
DECISIONS

print_step "Created DECISIONS.md"

# ─── First conversation log ───────────────────────────────────────────────────

cat > "$TARGET_DIR/conversations/${TODAY}.md" << SESSION
# Session — ${TODAY}

## Summary

Initial setup session. Created AI collaboration documents for ${PROJECT_NAME}.

## Key Decisions

### Project setup confirmed
- **Project**: ${PROJECT_NAME}
- **Description**: ${PROJECT_DESC}
- **Stage**: ${STAGE_LABEL}
- **Stack**: ${TECH_STACK}
- **Collaboration rhythm**: ${RHYTHM_LABEL}

## Work Completed

- Created HANDOFF.md, CONTEXT.md, DECISIONS.md, conversations/

## Open Questions

- (Add any open questions from this session)

## Next Session

- Update CONTEXT.md with the first concrete next steps
- Start working on: (fill in the first task)
SESSION

print_step "Created conversations/${TODAY}.md"

# ─── Done ─────────────────────────────────────────────────────────────────────

print_header "Done!"

echo ""
echo "  Files created in: ${TARGET_DIR}"
echo ""
echo "  HANDOFF.md       — collaboration contract"
echo "  CONTEXT.md       — current project state"
echo "  DECISIONS.md     — decision log"
echo "  conversations/   — session archives"
echo ""
echo -e "  ${YELLOW}Next steps:${RESET}"
echo "  1. Open CONTEXT.md and fill in 'In Progress' and 'Next Steps'"
echo "  2. Review DECISIONS.md and add any decisions you've already made"
echo "  3. Start a new AI session — it will detect HANDOFF.md automatically"
echo ""
