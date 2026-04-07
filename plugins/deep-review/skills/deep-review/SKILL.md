---
name: deep-review
description: Use when the user asks to "review code", "deep review", "/deep-review", "review approfondita", or wants a thorough multi-pass code review of recent implementation work.
---

# Deep Review — Controller Skill

Orchestrate a thorough multi-pass code review by dispatching the `deep-review:deep-reviewer` agent, gating on results, and presenting a consolidated report.

The review covers 5 passes: **correctness**, **security**, **architecture**, **performance**, **completeness**. Each pass can produce issues at three severities: critical, important, minor. Critical issues trigger a gate — the user decides how to proceed.

---

## Arguments

Parse the user's invocation for these optional flags. If a flag is not provided, use the default.

| Flag | Default | Effect |
|------|---------|--------|
| `--base <ref>` | `HEAD` | Git ref for diff comparison (e.g. `main`, `HEAD~5`) |
| `--skip <passes>` | none | Comma-separated passes to skip |
| `--only <passes>` | all | Comma-separated passes to run exclusively |
| `--quick` | off | Shortcut for `--only correctness,security` |
| `--spec <path>` | auto-detect | Path to spec/plan for correctness verification |

Valid pass names: `correctness`, `security`, `architecture`, `performance`, `completeness`

If `--quick` is present, it overrides `--only` and `--skip` — set passes to `correctness,security` only.

If both `--only` and `--skip` are provided, `--only` wins (ignore `--skip`).

---

## Step 1 — Scope Detection

Determine which files to review.

**If `--base` is provided**, run:

```bash
git diff --name-only {BASE_REF}...HEAD
```

**If `--base` is NOT provided**, run all three commands and collect the union of unique file paths:

```bash
git diff --name-only
git diff --cached --name-only
git log --oneline HEAD...origin/$(git branch --show-current) --name-only 2>/dev/null
```

Deduplicate the file list. Filter out deleted files (run `git diff --diff-filter=D --name-only` to identify them, and remove them from the list).

**If no files are found**, tell the user:

> Nessun file modificato trovato. Specifica `--base` per confrontare con un altro ref.

Then stop. Do not proceed to Step 2.

---

## Step 2 — Gather Context

### Spec/Plan

1. If `--spec <path>` is provided, note the absolute path. The agent will read it.
2. If no `--spec` but there is an active plan in the current conversation context (e.g. from a previous planning phase), reference it.
3. If neither, the review is general-purpose. Pass "Nessuna spec fornita. Review general-purpose." to the agent.

### CLAUDE.md Paths

Always include the root CLAUDE.md of the project (find it by looking for CLAUDE.md in the git root via `git rev-parse --show-toplevel`).

Additionally, scan the directories of each modified file for CLAUDE.md files:

```bash
# For each unique parent directory of modified files, check for CLAUDE.md
```

Collect all unique CLAUDE.md paths found.

### Determine Passes

Start with the full list: `correctness, security, architecture, performance, completeness`.

- If `--quick`: set to `correctness, security`
- If `--only <passes>`: set to only those passes
- If `--skip <passes>`: remove those passes from the full list
- Validate that all pass names are valid. If an invalid name is provided, warn the user and ignore it.

---

## Step 3 — Dispatch Agent

Dispatch the `deep-review:deep-reviewer` agent using the Agent tool. Use the following prompt template exactly, filling in the variables:

```
## Review Context

**FILES:**
{one file path per line, relative to project root}

**PASSES:** {comma-separated pass names to execute}

**BASE_REF:** {the git ref, default HEAD}

**SPEC:**
{absolute path to spec file if available, otherwise "Nessuna spec fornita. Review general-purpose."}

**CLAUDE_MD_PATHS:**
{one CLAUDE.md absolute path per line}
```

Wait for the agent to complete. The agent returns a single JSON code block.

---

## Step 4 — Gate Logic

Parse the JSON report from the agent. The structure is:

```json
{
  "passes": [
    {
      "name": "...",
      "status": "pass | warn | fail",
      "issues": [...],
      "summary": "..."
    }
  ],
  "verdict": "pass | warn | fail",
  "verdictSummary": "..."
}
```

Process passes **in order** (correctness, security, architecture, performance, completeness). For each pass:

### If status is `pass`

Show a checkmark and continue:

> :white_check_mark: **{Pass Name}** -- Nessun problema trovato.

### If status is `warn`

Show a brief summary and continue:

> :warning: **{Pass Name}** -- {summary}

List issues briefly (one line each): `[important] file:line - title` or `[minor] file:line - title`.

### If status is `fail` (critical issues found)

**STOP and gate.** Show the full pass report:

> :x: **{Pass Name}** -- {summary}

List ALL issues for this pass, formatted clearly:

For each issue:
```
**{severity}** | `{file}:{line}`
{title}
{description}
Suggerimento: {suggestion}
```

Then ask the user with exactly these 3 options:

> **Come vuoi procedere?**
>
> 1. Correggo i problemi critici e rilancio la review da questo pass
> 2. Continua la review (vedo tutto alla fine)
> 3. Stop, lavoro sui fix manualmente

**If option 1:**
- Help fix the critical issues in the main session (you can read/edit files, run commands).
- After fixes are applied, re-dispatch the agent with passes from the current pass onward (skip already-completed passes).
- Increment the iteration counter for this pass.
- If iteration count reaches 3, do NOT re-dispatch. Show current results and tell the user:
  > Raggiunto il limite di 3 iterazioni per il pass "{pass name}". Ecco i risultati attuali.

**If option 2:**
- Continue to the next pass. The failed pass results will appear in the final report.

**If option 3:**
- Show the summary of all passes completed so far (including the failed one), then stop. Do not proceed to Step 5.

---

## Step 5 — Final Report

After all passes are processed (or early stop), present the consolidated report.

### Summary Table

```
| Pass          | Status | Critical | Important | Minor |
|---------------|--------|----------|-----------|-------|
| correctness   | ...    | N        | N         | N     |
| security      | ...    | N        | N         | N     |
| architecture  | ...    | N        | N         | N     |
| performance   | ...    | N        | N         | N     |
| completeness  | ...    | N        | N         | N     |
| **Totale**    |        | **N**    | **N**     | **N** |
```

Only include passes that were executed. Use checkmark/warning/x icons for status.

### Issues by Priority

List all issues sorted by priority (critical first, then important, then minor). Group by severity:

**Critical:**
- `file:line` -- title -- suggerimento

**Important:**
- `file:line` -- title -- suggerimento

**Minor:**
- `file:line` -- title -- suggerimento

If a severity group is empty, omit it.

### Verdict

Based on the global verdict from the agent report (accounting for any re-runs):

- If `pass`: :white_check_mark: **Verdetto: Ready** -- Il codice supera tutti i controlli.
- If `warn`: :warning: **Verdetto: Problemi minori** -- Il codice ha issue non critiche da valutare.
- If `fail`: :x: **Verdetto: Problemi critici** -- Il codice ha issue critiche che devono essere risolte.

### Fix Offer

If there are any important or critical issues remaining, ask:

> Vuoi che proceda con i fix?

If the user says yes, proceed to fix issues in the main session (read files, edit, run typecheck/tests as needed). Do NOT re-dispatch the agent for fixes at this stage — work directly.

---

## Anti-Loop Protection

Track iteration count per pass. Maximum **3 iterations** per pass.

After the 3rd iteration of any pass:
- Show the current results for that pass
- Tell the user: "Raggiunto il limite di 3 iterazioni per il pass "{pass name}". Ecco i risultati attuali."
- Do NOT re-dispatch the agent for that pass again
- Continue to the next pass or final report

---

## Notes

- **Report language**: Italian (all user-facing text, issue titles, descriptions, suggestions)
- **Agent reads files on-demand**: Do not include file contents or diffs in the agent prompt. The agent uses Read/Grep/Glob tools to inspect files itself.
- **Agent does NOT modify files**: The agent only analyzes. All fixes are done by the controller (this skill) in the main session.
- **Scope**: Review only the files detected in Step 1. Do not expand scope unless the user explicitly asks.
- **No false positives**: Prefer missing a minor issue over flagging something that is not actually a problem. Precision over recall.
