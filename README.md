# Salesforce Enhanced Chat Design Review Editor

The Salesforce Enhanced Chat Design Review Editor helps admins, developers, and junior consultants prepare Enhanced Chat v1 and Omni-Channel solution designs for formal architecture review. It identifies the five highest-risk gaps in rationale, process flow, failure behavior, requirements coverage, and testability — then returns those problems to the author **without rewriting the design**.

**Competition judges and editor users: go straight to [`02_editor-review/README.md`](02_editor-review/README.md).** That folder is the complete, portable editor. Everything else in this repository is the workflow that carries a design from submission to human approval.

## What it reviews

Draft Solution Design Documents for **Salesforce Enhanced Chat v1** (formerly Messaging for In-App and Web) and **Omni-Channel** — new implementations or migrations from Legacy Chat. Out of scope: Legacy Chat design (except as migration source), Enhanced Chat v2, CTI/Amazon Connect, WhatsApp/SMS/Facebook Messenger, generic Salesforce reviews, code review, and any form of production or security approval.

## Why it won't rewrite your document

The editor packages senior architecture judgment as a **critic, not a co-author**. You learn solution architecture by resolving exposed weaknesses yourself; a rewritten document teaches nothing and hides what the author doesn't yet understand. Every finding names the exact passage, the design gap, the downstream consequence, and a focused problem for you to solve.

## What you need

- An AI coding agent (Codex or Claude Code) opened in this repository — the agent runs the workflow; you never move packages between stages yourself.
- **No coding agent? You can still use the editor today:** upload the `02_editor-review/` bundle to a Claude Project, ChatGPT Project/Custom GPT, or similar and paste your draft — see Option B below. The repository workflow (ledger, rounds, formal approval) needs an agent; the critique itself runs on any capable assistant.
- **Python 3, only for the built-in helpers the agent runs on your behalf** (the Word-document converter and the state-validation checks). Standard library only — nothing to install beyond Python itself, and **you never need to type a Python command yourself** (a CLI path exists for power users — see [`tools/README.md`](tools/README.md)). No Python? Submit PDF/markdown/plain text instead of Word, and the pipeline simply runs with fewer automatic safety checks.

## Quick start

**Option A — full pipeline (Codex or Claude Code in this repo):**

1. Attach your draft SDD, requirements, assumptions/open decisions, and diagrams in chat and say **`start`** — the agent checks the package first (and tells you what's missing before anything is created), files everything, and runs the review to the first human stop. Prefer folders? Place the files in `01_intake/input/<ID>/` yourself and say `start <ID>`. Formats: markdown, plain text, PDF, or Word (`.docx` is converted automatically; the original is kept).
2. From then on you only need three more words: **`continue <ID>`** to resume, **`status <ID>`** to see where things stand and your next action, **`submit revision <ID>`** when you've revised. (Power users: dry-run and consistency checks are described in [`tools/README.md`](tools/README.md).)
3. **You never have to touch the folders.** At every step — the first draft, revision files, changed supporting artifacts, even the senior architect's signed decision record — you can simply attach the files in chat and say what they are; the agent files each one in the right place, tells you every rename, and still runs all the normal checks before accepting anything. The folders are the audit trail; chat is the front door. (One rule never bends: the decision record must arrive already written and signed — the agent files it, never writes it.)
4. The long-form equivalent, if you prefer a sentence: *"Run the workflow for review ID `<ID>` from its current stage, complete every eligible automatic transition, preserve prior rounds, and stop at the next required human action."*

**Option B — standalone in a Claude Project (no repo needed):** see the *Standalone use* section of [`02_editor-review/README.md`](02_editor-review/README.md).

**Try the demo:** copy `fixtures/northstar/` contents (except the expected review) into `01_intake/input/NS-001/`, then say: *"Start a new demo review for ID NS-001 from 01_intake/input/, process every eligible automatic transition, and stop at the next required human action."* Compare the editor's output with `fixtures/northstar/expected-review-round-01.md`. **Standalone demo (no repo):** paste `fixtures/northstar/northstar-sdd-draft-v1.md` into your Project and compare the review you get with the expected one — matching in substance and form (anchored findings, consequences, no rewriting), not word-for-word.

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
- **The formal reviewer gets a focused packet:** a linked "start here" cover naming the design version to review, what needs your judgment (every open decision and residual risk, each with its own entry), and a decision form with the clerical fields already filled in. Superseded drafts and earlier rounds sit in a `history/` subfolder, out of your way. The decision itself — every selection, rationale, condition, and the signature — must be authored by the human reviewer; the AI cannot write or infer approval, even in demos, and a signed record (not a chat message) is what advances the package.
- **To revise and rerun:** your review packet arrives with a **pre-filled response form** — one block per finding; mark each resolved / partially resolved / disagree, say where the design changed, and explain in your own words (disagreeing is allowed when argued from a requirement). Put the revised SDD (new version in the filename), the completed form, and any changed supporting artifact into `04_revision-intake/input/<ID>/` — or attach them in chat — and say **`submit revision <ID>`**. The agent checks completeness before accepting; each accepted submission starts the next review round.
- **Converge faster:** the review's *Deferred Review Areas* section previews likely future findings — addressing those items in the same revision usually saves a full round. If you change a supporting artifact (requirements, assumptions), version its filename and re-read it against your SDD before submitting; intake cross-checks the package and bounces contradictions.
- **History is preserved:** packages advance by copying forward; every draft remains in its upstream stage, and every review, response, manifest, and decision remains traceable. Completion contains the final design and full review/decision evidence but intentionally excludes superseded SDDs.

## Under the hood: automatic safety checks

The agent runs a read-only helper (`tools/review_state.py`) at every step on your behalf: it verifies packages before anything is created, detects files you've dropped off before they're accepted, and cross-checks the ledger, status, and packet integrity. It never critiques a design, moves a package, or creates approval — and you never need to run it yourself. Curious or debugging? See [`tools/README.md`](tools/README.md).

## Repository layout

Six numbered stage folders (each with a `CONTEXT.md` contract and per-review `input/`/`output/` subfolders), the portable editor inside `02_editor-review/`, routing ledgers in `reviews/` (the authoritative record of where every review stands), a fictional demo package in `fixtures/northstar/`, and `tools/` (the Word-to-markdown converter intake uses). Agents and maintainers: read `AGENTS.md` and the root `CONTEXT.md`.
