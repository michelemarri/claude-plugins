---
name: ux-heuristics
description: >
  Apply Nielsen's 10 Usability Heuristics to evaluate a UI screen or flow. Use this skill
  whenever the user shares a screenshot, describes an interface, or asks for a heuristic
  evaluation, usability audit, UX scoring, or expert review of a UI. Also trigger when the
  user mentions "heuristic", "Nielsen", "usability review", "expert walkthrough", or wants
  to score/compare interfaces systematically. Always use this skill for any structured
  UX evaluation request, even if the user just says "analyze this screen" or "what's wrong
  with this UI".
---

# UX Heuristics – Nielsen's 10 Usability Heuristics

## Purpose
Deliver a structured heuristic evaluation of a UI screen or flow, scoring each of Nielsen's
10 heuristics and surfacing actionable findings. Useful for expert reviews, comparative
audits, and tracking improvements across design iterations.

---

## Evaluation Protocol

### Step 1 — Gather context (if missing)
Before evaluating, confirm:
- **Platform**: iOS / Android / Web / Desktop
- **User type**: Target audience and their expected expertise level
- **Task context**: What is the user trying to accomplish on this screen?
- **Scope**: Single screen, multi-screen flow, or full app audit?

If the screenshot or description makes the context obvious, proceed directly. Only ask if
ambiguity would change the evaluation meaningfully.

---

### Step 1b — Choose output mode
Default to **Quick** unless the user explicitly requests a full audit.

| Mode | When to use | Content |
|------|-------------|---------|
| **Quick** | Default, single screen, fast feedback | Only heuristics scoring 1–7, plus summary |
| **Full** | Deep audits, client reports, multi-screen flows | All 10 heuristics scored, full findings, summary |

If the user says "full audit", "detailed review", "client report", or similar → use Full.
If the user just shares a screenshot with no extra instructions → use Quick.

---

### Step 2 — Score each heuristic
Always evaluate all 10 heuristics internally regardless of mode. For each one:
- Assign a **score from 1 to 10** (1 = completely violated, 10 = fully satisfied)
- Write a **1–2 sentence finding** grounded in what you observe
- In Quick mode, only surface heuristics scoring 1–7 in the output
- In Full mode, include all 10 — for scores 8–10 briefly note why it works well

#### The 10 Heuristics

| # | Heuristic | Core question |
|---|-----------|---------------|
| H1 | **Visibility of system status** | Does the UI keep users informed about what's happening? |
| H2 | **Match between system and real world** | Does it speak the user's language, not system language? |
| H3 | **User control and freedom** | Can users easily undo, exit, or recover from mistakes? |
| H4 | **Consistency and standards** | Are conventions followed? Is behavior predictable? |
| H5 | **Error prevention** | Does the design prevent problems before they occur? |
| H6 | **Recognition over recall** | Are options visible? Does the user need to memorize? |
| H7 | **Flexibility and efficiency of use** | Are there shortcuts or accelerators for expert users? |
| H8 | **Aesthetic and minimalist design** | Is irrelevant or rarely-needed info absent? |
| H9 | **Help users recognize, diagnose, and recover from errors** | Are error messages clear and constructive? |
| H10 | **Help and documentation** | Is support available and easy to find when needed? |

---

### Step 3 — Output format

#### Score guide (used in both modes)
- ✅ 9–10 — Fully satisfied
- 🟡 7–8 — Minor gaps
- 🟠 5–6 — Noticeable issues, should fix
- 🔴 3–4 — Significant problems, fix before launch
- 🚨 1–2 — Critical violation, blocks or misleads users

---

#### Quick mode template
Use this by default. Concise, scannable, action-focused.

```
**Quick Heuristic Review — [Screen/Flow Name]**
*Platform: [X] | Context: [Y]*

**Issues found** (heuristics scoring < 8 only):

H[N] — [Heuristic Name] · [score]/10 [emoji]
[1–2 sentence finding. What's wrong and why it matters.]
→ [One specific, actionable recommendation.]

[Repeat for each heuristic scoring 1–7]

**Top priority:** [Single most impactful fix in one sentence.]
```

---

#### Full mode template
Use when explicitly requested. Complete coverage, suitable for reports.

```
**Heuristic Evaluation — [Screen/Flow Name]**
*Platform: [X] | Context: [Y] | Mode: Full Audit*

**H[N] — [Heuristic Name]** · [score]/10 [emoji]
[1–2 sentence finding grounded in observation.]
*Recommendation:* [Specific fix — omit if score ≥ 8.]

[Repeat for all 10 heuristics]

---
**Priority Issues** — scores 1–4, ranked by impact (max 5)
**Areas to Watch** — scores 5–6 (max 3)
**What works well** — scores 8–10 worth preserving (max 3)
```

---

## Multi-screen / Flow Evaluation
When evaluating a flow (2+ screens):
1. Evaluate each screen individually using the protocol above
2. Add a **Cross-screen consistency section** at the end noting:
   - Inconsistencies in patterns, terminology, or visual language
   - Flow-level issues (dead ends, missing progress indicators, context loss)
   - Whether the overall journey aligns with user mental models

---

## Comparative Audit Mode
If the user provides two versions of the same screen (A vs B):
- Score both using the same protocol
- Add a **Comparison Summary** table: heuristic | Version A score | Version B score | Delta
- Give a clear recommendation on which version to proceed with and why
