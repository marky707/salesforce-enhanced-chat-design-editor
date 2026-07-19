# Salesforce Enhanced Chat Design Review Editor

The Salesforce Enhanced Chat Design Review Editor helps admins, developers, and junior consultants prepare Enhanced Chat v1 and Omni-Channel solution designs for formal architecture review. It identifies the five highest-risk gaps in rationale, process flow, failure behavior, requirements coverage, and testability — then returns those problems to the author **without rewriting the design**.

**Competition judges and editor users: go straight to [`02_editor-review/README.md`](02_editor-review/README.md).** That folder is the complete, portable editor. Everything else in this repository is the workflow that carries a design from submission to human approval.

## What it reviews

Draft Solution Design Documents for **Salesforce Enhanced Chat v1** (formerly Messaging for In-App and Web) and **Omni-Channel** — new implementations or migrations from Legacy Chat. Out of scope: Legacy Chat design (except as migration source), Enhanced Chat v2, CTI/Amazon Connect, WhatsApp/SMS/Facebook Messenger, generic Salesforce reviews, code review, and any form of production or security approval.

## Why it won't rewrite your document

The editor packages senior architecture judgment as a **critic, not a co-author**. You learn solution architecture by resolving exposed weaknesses yourself; a rewritten document teaches nothing and hides what the author doesn't yet understand. Every finding names the exact passage, the design gap, the downstream consequence, and a focused problem for you to solve.

## What you need

- An AI coding agent (Codex or Claude Code) opened in this repository — the agent runs the workflow; you never move packages between stages yourself.
- **No coding agent? You can still use the editor today:** upload the `02_editor-review/` bundle to a Claude Project and paste your draft — see Option B below. The repository workflow (ledger, rounds, formal approval) needs an agent; the critique itself doesn't.
- **Python 3, only if you'll submit Word documents** — the `.docx` converter uses the Python standard library, so there's nothing to install beyond Python itself (already present on macOS and Linux; one-time install on Windows). No Python? Export your document as PDF, markdown, or plain text instead — intake accepts all three as-is.

## Quick start

**Option A — full pipeline (Codex or Claude Code in this repo):**

1. Put your draft SDD, requirements, assumptions/open decisions, and diagrams in `01_intake/input/<ID>/` (pick an ID like `AC-001`, or let the agent assign one) — **or simply attach the files in chat** and say what they are; the agent files them into the correct stage folder for you and confirms where they went. The same works for revisions, and for the senior architect's completed decision record (which must arrive already signed — the agent files it, never writes it). Formats: markdown, plain text, PDF, or Word — `.docx` files are converted automatically at intake (the original is kept as the source of record).
2. Say: *"Start a new review from 01_intake/input/. Assign a review ID if one is not already declared, process every eligible automatic transition, and stop at the next required human action."*
3. For an existing review: *"Run the workflow for review ID `<ID>` from its current stage. Follow the routing contracts, complete every eligible automatic transition, preserve prior rounds, and stop at the next required human action or completed state."*
4. Or just use the short verbs the agent understands: **`start`**, **`continue <ID>`**, **`status <ID>`**, **`submit revision <ID>`**. At any moment, `reviews/<ID>-status.md` shows where your review stands and your exact next action.

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
- **The formal reviewer gets a focused packet:** a linked cover sheet naming the design version, the ready verdict, and the open decisions; superseded drafts and earlier rounds sit in a `history/` subfolder. The decision form arrives with its administrative fields pre-filled — but the decision, rationale, and signature must be authored by the human reviewer; the AI is prohibited from writing or inferring approval, and a signed record (not a chat message) is what advances the package.
- **To revise and rerun:** your review packet arrives with a **pre-filled response form** — one block per finding; mark each one resolved / partially resolved / disagree, say where the design changed, and explain in your own words (disagreeing is allowed when argued from a requirement). Place the revised SDD (new version in the filename) and the completed form in `04_revision-intake/input/<ID>/` — or attach both in chat — and invoke the workflow again. Each rerun is a new numbered round.
- **Converge faster:** the review's *Deferred Review Areas* section previews likely future findings — addressing those items in the same revision usually saves a full round. If you change a supporting artifact (requirements, assumptions), version its filename and re-read it against your SDD before submitting; intake cross-checks the package and bounces contradictions.
- **History is preserved:** packages advance by copying forward; every draft, review round, response log, and decision stays where it was written, and `reviews/<ID>-routing-log.md` records every transition.

## Repository layout

Six numbered stage folders (each with a `CONTEXT.md` contract and per-review `input/`/`output/` subfolders), the portable editor inside `02_editor-review/`, routing ledgers in `reviews/` (the authoritative record of where every review stands), a fictional demo package in `fixtures/northstar/`, and `tools/` (the Word-to-markdown converter intake uses). Agents and maintainers: read `AGENTS.md` and the root `CONTEXT.md`.
