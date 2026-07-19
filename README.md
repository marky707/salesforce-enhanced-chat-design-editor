# Salesforce Enhanced Chat Design Review Editor

The Salesforce Enhanced Chat Design Review Editor helps admins, developers, and junior consultants prepare Enhanced Chat v1 and Omni-Channel solution designs for formal architecture review. It identifies the five highest-risk gaps in rationale, process flow, failure behavior, requirements coverage, and testability — then returns those problems to the author **without rewriting the design**.

**Competition judges and editor users: go straight to [`02_editor-review/README.md`](02_editor-review/README.md).** That folder is the complete, portable editor. Everything else in this repository is the workflow that carries a design from submission to human approval.

## What it reviews

Draft Solution Design Documents for **Salesforce Enhanced Chat v1** (formerly Messaging for In-App and Web) and **Omni-Channel** — new implementations or migrations from Legacy Chat. Out of scope: Legacy Chat design (except as migration source), Enhanced Chat v2, CTI/Amazon Connect, WhatsApp/SMS/Facebook Messenger, generic Salesforce reviews, code review, and any form of production or security approval.

## Why it won't rewrite your document

The editor packages senior architecture judgment as a **critic, not a co-author**. You learn solution architecture by resolving exposed weaknesses yourself; a rewritten document teaches nothing and hides what the author doesn't yet understand. Every finding names the exact passage, the design gap, the downstream consequence, and a focused problem for you to solve.

## Quick start

**Option A — full pipeline (Codex or Claude Code in this repo):**

1. Put your draft SDD, requirements, assumptions/open decisions, and diagrams in `01_intake/input/<ID>/` (pick an ID like `AC-001`, or let the agent assign one).
2. Say: *"Start a new review from 01_intake/input/. Assign a review ID if one is not already declared, process every eligible automatic transition, and stop at the next required human action."*
3. For an existing review: *"Run the workflow for review ID `<ID>` from its current stage. Follow the routing contracts, complete every eligible automatic transition, preserve prior rounds, and stop at the next required human action or completed state."*

**Option B — standalone in a Claude Project (no repo needed):** see the *Standalone use* section of [`02_editor-review/README.md`](02_editor-review/README.md).

**Try the demo:** copy `fixtures/northstar/` contents (except the expected review) into `01_intake/input/NS-001/`, then say: *"Start a new demo review for ID NS-001 from 01_intake/input/, process every eligible automatic transition, and stop at the next required human action."* Compare the editor's output with `fixtures/northstar/expected-review-round-01.md`.

## The workflow

```text
01 Intake ──complete──▶ 02 Editor Review ──ready──▶ 05 Formal Review ──approved──▶ 06 Completed
   │ incomplete            │ changes required           │ changes required
   ▼ (stays, human fixes)  ▼                            ▼
                        03 Author Revision ◀────────────┘
                           │ author submits (HUMAN)
                           ▼
                        04 Revision Intake ──complete──▶ back to 02 (next round)
                           │ incomplete ──▶ back to 03
```

- **What the editor returns:** a verdict (`Revise Before Formal Review`, `Ready for Formal Review with Open Decisions`, `Ready for Formal Review`, or `Insufficient Context`) plus at most five prioritized findings, each anchored to an exact passage with its consequence and a question for you to resolve.
- **"Ready for Formal Review" means** the document is coherent enough for a human architecture review. It is **not** architecture approval — that decision belongs to the accountable human reviewer in `05_formal-review/`.
- **The workflow stops for people twice:** at `03_author-revision/` (you revise and deliberately resubmit) and at `05_formal-review/` (a human records the decision). Everything else advances automatically during an invoked run.
- **To revise and rerun:** answer every finding in the response log template, place the revised SDD and log in `04_revision-intake/input/<ID>/`, and invoke the workflow again. Each rerun is a new numbered round.
- **History is preserved:** packages advance by copying forward; every draft, review round, response log, and decision stays where it was written, and `reviews/<ID>-routing-log.md` records every transition.

## Repository layout

Six numbered stage folders (each with a `CONTEXT.md` contract and per-review `input/`/`output/` subfolders), the portable editor inside `02_editor-review/`, routing ledgers in `reviews/`, and a fictional demo package in `fixtures/northstar/`. Agents and maintainers: read `AGENTS.md` and the root `CONTEXT.md`.
