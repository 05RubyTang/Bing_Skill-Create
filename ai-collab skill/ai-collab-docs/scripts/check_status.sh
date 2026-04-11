#!/bin/bash

# =============================================================================
# AI Collaboration Docs — Status Checker
# =============================================================================
# Checks whether collaboration docs exist and whether they're up to date.
# Designed to be run at the start of a session (or called from CLAUDE.md).
#
# Usage:
#   bash check_status.sh              # Check current directory
#   bash check_status.sh /path/to/project  # Check a specific directory
#
# Exit codes:
#   0 — docs exist and look healthy
#   1 — docs missing or have issues (details printed to stdout)
# =============================================================================

TARGET_DIR="${1:-.}"
TODAY=$(date +%Y-%m-%d)

# ─── Colors ───────────────────────────────────────────────────────────────────

BOLD="\033[1m"
GREEN="\033[0;32m"
RED="\033[0;31m"
YELLOW="\033[0;33m"
RESET="\033[0m"

# ─── State tracking ───────────────────────────────────────────────────────────

ISSUES=()
WARNINGS=()
HEALTHY=()

check_ok() { HEALTHY+=("$1"); }
check_warn() { WARNINGS+=("$1"); }
check_fail() { ISSUES+=("$1"); }

# ─── Checks ───────────────────────────────────────────────────────────────────

# Check required files exist
for file in "HANDOFF.md" "CONTEXT.md" "DECISIONS.md"; do
  if [ -f "$TARGET_DIR/$file" ]; then
    check_ok "$file exists"
  else
    check_fail "$file is missing"
  fi
done

# Check conversations directory
if [ -d "$TARGET_DIR/conversations" ]; then
  check_ok "conversations/ directory exists"

  # Count session logs
  LOG_COUNT=$(find "$TARGET_DIR/conversations" -name "*.md" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$LOG_COUNT" -gt 0 ]; then
    check_ok "$LOG_COUNT session log(s) found"

    # Find most recent log
    LATEST_LOG=$(find "$TARGET_DIR/conversations" -name "*.md" | sort | tail -1)
    LATEST_DATE=$(basename "$LATEST_LOG" .md 2>/dev/null)

    # Check if it's older than 7 days
    if command -v python3 &>/dev/null; then
      DAYS_OLD=$(python3 -c "
from datetime import datetime, date
try:
    d = datetime.strptime('$LATEST_DATE', '%Y-%m-%d').date()
    print((date.today() - d).days)
except:
    print(-1)
" 2>/dev/null)
      if [ "$DAYS_OLD" -gt 14 ]; then
        check_warn "Last session log is $DAYS_OLD days old ($LATEST_DATE) — CONTEXT.md may be stale"
      elif [ "$DAYS_OLD" -ge 0 ]; then
        check_ok "Last session: $LATEST_DATE ($DAYS_OLD days ago)"
      fi
    else
      check_ok "Last session log: $LATEST_DATE"
    fi
  else
    check_warn "conversations/ exists but no session logs yet"
  fi
else
  check_fail "conversations/ directory is missing"
fi

# Check CONTEXT.md last-updated date
if [ -f "$TARGET_DIR/CONTEXT.md" ]; then
  LAST_UPDATED=$(grep -m1 "Last updated:" "$TARGET_DIR/CONTEXT.md" 2>/dev/null | sed 's/.*Last updated: //' | tr -d '> \r')
  if [ -n "$LAST_UPDATED" ]; then
    if command -v python3 &>/dev/null; then
      DAYS_STALE=$(python3 -c "
from datetime import datetime, date
try:
    d = datetime.strptime('$LAST_UPDATED', '%Y-%m-%d').date()
    print((date.today() - d).days)
except:
    print(-1)
" 2>/dev/null)
      if [ "$DAYS_STALE" -gt 14 ]; then
        check_warn "CONTEXT.md was last updated $DAYS_STALE days ago ($LAST_UPDATED) — may be outdated"
      elif [ "$DAYS_STALE" -ge 0 ]; then
        check_ok "CONTEXT.md updated $DAYS_STALE days ago ($LAST_UPDATED)"
      fi
    else
      check_ok "CONTEXT.md last updated: $LAST_UPDATED"
    fi
  else
    check_warn "CONTEXT.md has no 'Last updated' date"
  fi
fi

# Check for placeholder text not replaced
if [ -f "$TARGET_DIR/HANDOFF.md" ]; then
  PLACEHOLDERS=$(grep -c "{.*}" "$TARGET_DIR/HANDOFF.md" 2>/dev/null || echo "0")
  if [ "$PLACEHOLDERS" -gt 0 ]; then
    check_warn "HANDOFF.md still has $PLACEHOLDERS unfilled placeholder(s) — run setup or edit manually"
  else
    check_ok "HANDOFF.md has no unfilled placeholders"
  fi
fi

# Check for today's session log
if [ -f "$TARGET_DIR/conversations/${TODAY}.md" ]; then
  check_ok "Today's session log exists (conversations/${TODAY}.md)"
fi

# ─── Output ───────────────────────────────────────────────────────────────────

echo ""
echo -e "${BOLD}AI Collaboration Docs — Status Report${RESET}"
echo -e "${BOLD}Directory: ${TARGET_DIR}${RESET}"
echo "$(printf '─%.0s' {1..50})"

if [ ${#HEALTHY[@]} -gt 0 ]; then
  for item in "${HEALTHY[@]}"; do
    echo -e "  ${GREEN}✓${RESET} $item"
  done
fi

if [ ${#WARNINGS[@]} -gt 0 ]; then
  echo ""
  for item in "${WARNINGS[@]}"; do
    echo -e "  ${YELLOW}⚠${RESET} $item"
  done
fi

if [ ${#ISSUES[@]} -gt 0 ]; then
  echo ""
  for item in "${ISSUES[@]}"; do
    echo -e "  ${RED}✗${RESET} $item"
  done
  echo ""
  echo -e "  ${RED}${BOLD}Docs are incomplete.${RESET} Run: bash scripts/setup.sh"
  exit 1
fi

if [ ${#WARNINGS[@]} -gt 0 ]; then
  echo ""
  echo -e "  ${YELLOW}Docs exist but may need attention.${RESET}"
  exit 0
fi

echo ""
echo -e "  ${GREEN}${BOLD}All good. AI can read these docs and pick up from where you left off.${RESET}"
echo ""
exit 0
