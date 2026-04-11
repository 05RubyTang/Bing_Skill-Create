# Flux — Decision Log

> This file records all confirmed decisions.
> AI must follow these decisions and must not override them silently.
> New entries are added only after the human explicitly confirms.

---

## How to Read This File

- **#**: Category prefix + number (T-1 = Technical #1, P-1 = Product #1)
- **Decision**: What was decided
- **Reason**: Why — critical for judging edge cases later
- **Date**: When confirmed

---

## Product Direction

| # | Decision | Reason | Date |
|---|----------|--------|------|
| P-1 | Task management app focused on core CRUD operations for MVP | Establish a working product before adding advanced features | 2026-04-11 |

---

## Technical Architecture

| # | Decision | Reason | Date |
|---|----------|--------|------|
| T-1 | React (frontend) + Node.js (backend) | Already in use; backend mostly complete | 2026-04-11 |
| T-2 | Backend API is the source of truth — no duplicate logic in frontend | Clear separation of concerns | 2026-04-11 |

---

## Visual / Design

| # | Decision | Reason | Date |
|---|----------|--------|------|
| V-1 | (No visual decisions locked yet) | — | — |

---

## Pending — AI Must Not Decide Independently

The following items have NOT been decided. If encountered during development, ask the human first:

- State management approach (Context API vs Redux vs Zustand vs other)
- Styling solution (Tailwind vs CSS Modules vs styled-components)
- UI component library (MUI vs Chakra vs build from scratch)
- Component folder structure (by feature vs by type)
- Authentication approach
- Error handling strategy
