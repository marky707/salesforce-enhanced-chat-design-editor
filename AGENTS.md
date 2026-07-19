# AGENTS.md — Canonical Agent Instructions

Instructions for Codex, Claude Code, and future maintainers operating this repository. Human readers start at `README.md`.

## What this repository is

A critic-only ICM pipeline that readies Salesforce Enhanced Chat v1 (formerly Messaging for In-App and Web) and Omni-Channel Solution Design Documents for formal architecture review. The editor identifies weaknesses and returns them to the author. It never rewrites, never generates missing content, and never approves architecture.

## Repository map

- `CONTEXT.md` — the pipeline in one screen: stages, conventions, human stops. **Read this first.**
- `01_intake/` … `06_completed/` — the six pipeline stages. Each has its own `CONTEXT.md` contract.
- `02_editor-review/` — pipeline stage **and** the portable five-part editor (identity, rules, examples, reference/, README).
- `reviews/` — per review ID: the append-only routing ledger (authoritative workflow state) and its generated status card. Nothing else belongs there.
- `fixtures/northstar/` — fictional demo package for testing and demonstration. Never a live review.
- `tools/docx_to_md.py` — stdlib-only Word→markdown converter, run by intake when a `.docx` is submitted.
- `tools/review_state.py` — read-only preflight, filesystem-aware status, state validation, link checks, and checksummed artifact manifests. It never advances a package or writes a decision.

## Operating sequence

1. Read the root `CONTEXT.md` first.
2. Identify the review ID named by the user. Exactly one active ledger in `reviews/` and no ID named → use it. Multiple active → ask which. A package in `01_intake/input/` with no ledger is a **new submission**: `01_intake/CONTEXT.md` says how to assign its ID and create its ledger.
3. Determine the current stage from the **latest row of `reviews/<ID>-routing-log.md`**, not from folder contents. Run `python3 tools/review_state.py validate-state <ID>` before mutating workflow state; a failure is an ambiguous state and must stop.
4. Dispatch using the routing table below: read the current stage's `CONTEXT.md` and only the files it routes to.
5. Perform that stage's one job; write its versioned output to `output/<ID>/`.
6. Evaluate the stage's explicit transition rule.
7. If the transition is objective: copy the package subfolder into the next stage's `input/`, append a ledger row, regenerate the derived status with `python3 tools/review_state.py status <ID> --write`, validate state again, and dispatch from the table. The status card includes the latest transition receipt. During multi-stage runs, narrate progress briefly as each stage completes ("Intake complete → review in progress → routed to author revision").
8. Stop at a human-controlled action (`03`, `05`), an intake error, an ambiguous state, or `06`.
9. Report what was produced, where the package stopped, why, and the exact next human action — and point the human at the packet cover and status card, not at raw folders.

## Operator verbs

Users may drive the workflow with these short commands (any phrasing that clearly means the same thing counts):

| Verb | What the agent does |
|---|---|
| `start` | New package: assign/confirm ID, file any chat-attached documents, **run start preflight automatically** (on failure, report what's missing and create no state), then create the ledger + status card, run intake, continue to the next human stop |
| `continue <ID>` | Resume from the ledger state; complete every eligible automatic transition; stop at the next human action |
| `status <ID>` | Inspect the ledger **and human drop zones**, regenerate the filesystem-aware status card, and show it without advancing state |
| `preflight start <ID>` | Inspect a new package and ID availability without creating a ledger |
| `preflight revision <ID>` | Inspect revision files, response completeness, versions, and requirement/acceptance drift without accepting them |
| `preflight decision <ID>` | Inspect a candidate human decision, signature, conditions, and required changes without advancing it |
| `validate state <ID>` | Compare ledger, status, current stage, registry purity, packet artifacts, and relative links; never changes state |
| `submit revision <ID>` | Run revision preflight; if clean, append the human submission row, validate the drop in `04_revision-intake/input/<ID>/`, and continue |

## Routing table

Given the latest ledger row (or triggering event), route the package and read the destination's `CONTEXT.md` — it defines the job to perform there. This table dispatches; the stage contracts govern.

| When (state / event) | Route package to | Then read | Stop? |
|---|---|---|---|
| New submission in `01_intake/input/<ID>/`, no ledger | stays in `01_intake` (create ledger) | `01_intake/CONTEXT.md` | no — validate |
| Intake **complete** | `02_editor-review/input/<ID>/` | `02_editor-review/CONTEXT.md` | no — review |
| Intake **incomplete** | stays in `01_intake` | — | **STOP** — author supplies missing items |
| Verdict `Revise Before Formal Review` or `Insufficient Context` | `03_author-revision/input/<ID>/` | `03_author-revision/CONTEXT.md` | **STOP** — author revises |
| Verdict `Ready for Formal Review` (with or without Open Decisions) | `05_formal-review/input/<ID>/` | `05_formal-review/CONTEXT.md` | **STOP** — human decision |
| Author submitted package in `04_revision-intake/input/<ID>/` | stays in `04_revision-intake` | `04_revision-intake/CONTEXT.md` | no — validate |
| Revision intake **complete** | `02_editor-review/input/<ID>/` (round +1) | `02_editor-review/CONTEXT.md` | no — review |
| Revision intake **incomplete** | `03_author-revision/input/<ID>/` (errors report) | — | **STOP** — author fixes resubmission |
| Formal decision `Approved` (valid human record) | `06_completed/input/<ID>/` | `06_completed/CONTEXT.md` | terminal after manifest |
| Formal decision `Approved with Conditions` | per `05_formal-review/CONTEXT.md` condition rule | `05_formal-review/CONTEXT.md` | waits unless all non-blocking |
| Formal decision `Changes Required` | `03_author-revision/input/<ID>/` | — | **STOP** — author revises |
| Latest row `To stage` = `06_completed`, manifest written | nowhere — terminal | — | **STOP** |
| Ambiguous / contradictory state | nowhere — write state-error report to current stage `output/<ID>/` | — | **STOP** — human reconciles |

## Chat-submitted documents

When the user attaches or pastes documents in chat (a draft SDD, a revision, supporting artifacts), treat that as a **submission to be filed, never reviewed in place**:

1. Determine the destination from the ledger state via the routing table: no active review (or user says it's new) → `01_intake/input/<ID>/`; active review awaiting the author → `04_revision-intake/input/<ID>/`; a **completed and signed formal decision record** from the accountable reviewer while the package awaits formal review → `05_formal-review/output/<ID>/` (file it verbatim — the record must arrive already authored and signed; if the user instead dictates a decision and asks you to write the record, decline per `05_formal-review/CONTEXT.md`). Multiple active reviews and no ID named → ask which.
2. Write the files there **verbatim** (convert `.docx` per `01_intake/CONTEXT.md`), normalizing filenames to the package convention (versioned, review-ID-consistent) and telling the user each rename.
3. Confirm the placement, record the user as the human actor in the ledger row, then run the destination stage's normal validation — chat upload is a filing convenience and never waives intake checks, the response-log requirement, or any other contract.

Never critique an attached document directly in chat while skipping the pipeline: an unfiled review has no ledger, no round number, and no audit trail.

## Invariants — never break these

- **Critique only.** The editor never writes replacement design content, generates diagrams, or completes a design — in any stage, for any reason, including "the author asked."
- **Approval is human.** Never infer, create, or simulate a formal decision. Document readiness ≠ architecture approval. `06_completed/` rejects packages lacking a human-authored decision record.
- **History is preserved.** Copy forward; never delete or overwrite prior rounds, outputs, or ledger rows.
- **Working vs. submission location.** `03_author-revision/output/<ID>/` is the author's retained working/output copy. `04_revision-intake/input/<ID>/` is the deliberate submission drop zone. File presence is evidence; the human invocation is the submission event.
- **No guessing.** Ambiguous or contradictory state → state-error report, stop, preserve evidence.
- **Fail loud on unsafe writes.** Refuse to write into a different review ID than the one being processed unless the user confirms; refuse to reuse an existing versioned filename for changed content; refuse to author or backfill Decision/Rationale/Signature content anywhere, ever.
- **Scope is settled.** Enhanced Chat v1 + Omni-Channel only. No CTI, no Enhanced Chat v2, no other messaging channels, no code review. Do not widen scope during maintenance.
- **Fixtures stay fictional.** `fixtures/` content never enters `reviews/` or stage folders except when a user explicitly starts a demo run, and demo ledgers must be labeled as demos.
- **Demos preserve the approval boundary.** An AI may advise a fictional reviewer but must never fill or sign the formal decision. A demo stops at `05` unless a real human completes the fictional decision record.

## Validation expectations

Before publishing changes, compile and exercise the helpers, then verify against `fixtures/northstar/`: run the demo package through intake and editor review; the output must resemble `fixtures/northstar/expected-review-round-01.md` in form — verdict, ≤5 anchored findings, consequences, author tasks, no rewritten content. Run `validate state <ID>` at every stop. The eight acceptance routes are listed in `CONTEXT.md` and the fixture README; human decision routes require a real signed fictional record.

## File-size guidance

CONTEXT files ≈ one screen (~50 lines); reference files ≈ a few hundred lines. These are targets, not caps — a file outgrowing its target is a signal to split it by job.

## Contracts

- Editor behavior: `02_editor-review/rules.md` (most important file in the project)
- Workflow routing: root `CONTEXT.md` + each stage's `CONTEXT.md`
- Ledger format: `reviews/README.md`
