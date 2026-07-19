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
- **Python 3 for repository workflow helpers** — both the `.docx` converter and `review_state.py` use only the standard library; there are no packages to install. No Python? The portable standalone critic still works, but the full pipeline loses mechanical preflight/state validation.

## Quick start

**Option A — full pipeline (Codex or Claude Code in this repo):**

1. Recommended for first-time users: attach the draft SDD and supporting files in chat and say `preflight start`; the agent checks the package and an unused ID without creating state. Manual users may place files in `01_intake/input/<ID>/`; see its checklist. Formats: markdown, plain text, PDF, or Word.
2. When preflight is acceptable, say `start <ID>`. The agent creates the ledger, validates intake, continues through objective transitions, and stops at the next human action.
3. For an existing review: *"Run the workflow for review ID `<ID>` from its current stage. Follow the routing contracts, complete every eligible automatic transition, preserve prior rounds, and stop at the next required human action or completed state."*
4. Short verbs: **`start`**, **`continue <ID>`**, **`status <ID>`**, **`submit revision <ID>`**, **`preflight start|revision|decision <ID>`**, and **`validate state <ID>`**. Status detects files in human drop zones without accepting them; the ledger remains authoritative.

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
- **The formal reviewer gets a focused packet:** a linked cover, authoritative decision index, structured residual risks, one actionable pre-filled FORM, checksummed artifact manifest, current material, and `history/`. The AI may pre-fill IDs/questions and administrative fields only; all selections, rationale, concurrence, conditions/changes, and signature remain human-authored. Demo mode does not relax this rule.
- **To revise and rerun:** finish author-owned copies in `03_author-revision/output/<ID>/`, then place **every changed artifact** in `04_revision-intake/input/<ID>/`. Run `preflight revision <ID>` before `submit revision <ID>`. File placement is visible evidence; the command is the deliberate submission event. Each successful intake starts the next review round.
- **Converge faster:** the review's *Deferred Review Areas* section previews likely future findings — addressing those items in the same revision usually saves a full round. If you change a supporting artifact (requirements, assumptions), version its filename and re-read it against your SDD before submitting; intake cross-checks the package and bounces contradictions.
- **History is preserved:** packages advance by copying forward; every draft remains in its upstream stage, and every review, response, manifest, and decision remains traceable. Completion contains the final design and full review/decision evidence but intentionally excludes superseded SDDs.

## Preflight and state validation

The helper is read-only unless explicitly asked to write a derived status card or artifact manifest:

```bash
python3 tools/review_state.py preflight start NS-001
python3 tools/review_state.py preflight revision NS-001
python3 tools/review_state.py preflight decision NS-001
python3 tools/review_state.py status NS-001 --write
python3 tools/review_state.py validate-state NS-001
python3 tools/review_state.py manifest NS-001 --write
```

It never appends a ledger row, critiques a design, moves a package, or creates approval. See [`tools/README.md`](tools/README.md).

## Repository layout

Six numbered stage folders (each with a `CONTEXT.md` contract and per-review `input/`/`output/` subfolders), the portable editor inside `02_editor-review/`, routing ledgers in `reviews/` (the authoritative record of where every review stands), a fictional demo package in `fixtures/northstar/`, and `tools/` (the Word-to-markdown converter intake uses). Agents and maintainers: read `AGENTS.md` and the root `CONTEXT.md`.
