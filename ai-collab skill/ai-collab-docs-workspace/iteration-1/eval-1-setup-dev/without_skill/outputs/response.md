# AI Response — Eval 1 (without skill / baseline)

That's a common frustration with AI-assisted development! The issue is that AI doesn't have memory between sessions, so you have to re-establish context each time.

Here are a few approaches that can help:

## Option 1: Keep a project summary file

Create a `PROJECT_SUMMARY.md` in your repo with key info:
- What the project is
- Current status  
- What you're working on
- Key decisions made

Paste it at the start of each session.

## Option 2: Use a project context prompt

Write a reusable "system prompt" or introduction you copy-paste at session start. Something like:

> "I'm working on Flux, a React + Node.js task management app. The backend is mostly done, I'm now building the React UI. We were working on [X] last time."

## Option 3: CLAUDE.md (if using Claude Code)

If you're using Claude Code, you can add a `CLAUDE.md` to your repo. Claude reads it automatically at session start.

---

## For your Flux project specifically

Since you're a frontend developer building the React UI on an existing Node.js backend, I'd recommend starting with a brief project doc. Want me to help you write one now?

What are the main things you'd want an AI to know at the start of each session? Things like:
- The core features of the app
- Which features are done vs. in progress
- Any technical decisions you've made (state management, etc.)
- What you were last working on

Tell me more and I can help you structure something useful.
