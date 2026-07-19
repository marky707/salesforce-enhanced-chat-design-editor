# AGENTS.md — Canonical Agent Instructions

Instructions for Codex, Claude Code, and future maintainers operating this repository. Human readers start at `README.md`.

## What this repository is

A critic-only ICM pipeline that readies Salesforce Enhanced Chat v1 (formerly Messaging for In-App and Web) and Omni-Channel Solution Design Documents for formal architecture review. The editor identifies weaknesses and returns them to the author. It never rewrites, never generates missing content, and never approves architecture.

## Repository map

- `CONTEXT.md` — the pipeline in one screen: stages, conventions, human stops. **Read this first.**
- `01_intake/` … `06_completed/` — the six pipeline stages. Each has its own `CONTEXT.md` contract.
- `02_editor-review/` — pipeline stage **and** the portable five-part editor (identity, rules, examples, reference/, README).
- `reviews/` — one append-only routing ledger per review ID. Authoritative workflow state.
- `fixtures/northstar/` — fictional demo package for testing and demonstration. Never a live review.

## Operating sequence

1. Read the root `CONTEXT.md` first.
2. Identify the review ID named by the user. Exactly one active ledger in `reviews/` and no ID named → use it. Multiple active → ask which. A package in `01_intake/input/` with no ledger is a **new submission**: `01_intake/CONTEXT.md` says how to assign its ID and create its ledger.
3. Determine the current stage from the **latest row of `reviews/<ID>-routing-log.md`**, not from folder contents.
4. Dispatch using the routing table below: read the current stage's `CONTEXT.md` and only the files it routes to.
5. Perform that stage's one job; write its versioned output to `output/<ID>/`.
6. Evaluate the stage's explicit transition rule.
7. If the transition is objective: copy the package subfolder into the next stage's `input/`, append a ledger row, and dispatch again from the table.
8. Stop at a human-controlled action (`03`, `05`), an intake error, an ambiguous state, or `06`.
9. Report what was produced, where the package stopped, why, and the exact next human action.

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

## Invariants — never break these

- **Critique only.** The editor never writes replacement design content, generates diagrams, or completes a design — in any stage, for any reason, including "the author asked."
- **Approval is human.** Never infer, create, or simulate a formal decision. Document readiness ≠ architecture approval. `06_completed/` rejects packages lacking a human-authored decision record.
- **History is preserved.** Copy forward; never delete or overwrite prior rounds, outputs, or ledger rows.
- **No guessing.** Ambiguous or contradictory state → state-error report, stop, preserve evidence.
- **Scope is settled.** Enhanced Chat v1 + Omni-Channel only. No CTI, no Enhanced Chat v2, no other messaging channels, no code review. Do not widen scope during maintenance.
- **Fixtures stay fictional.** `fixtures/` content never enters `reviews/` or stage folders except when a user explicitly starts a demo run, and demo ledgers must be labeled as demos.

## Validation expectations

Before publishing changes, verify against `fixtures/northstar/`: run the demo package through intake and editor review; the output must resemble `fixtures/northstar/expected-review-round-01.md` in form — verdict, ≤5 anchored findings, consequences, author tasks, no rewritten content. The eight acceptance routes are listed in `CONTEXT.md` stage table and tested in the fixture README.

## File-size guidance

CONTEXT files ≈ one screen (~50 lines); reference files ≈ a few hundred lines. These are targets, not caps — a file outgrowing its target is a signal to split it by job.

## Contracts

- Editor behavior: `02_editor-review/rules.md` (most important file in the project)
- Workflow routing: root `CONTEXT.md` + each stage's `CONTEXT.md`
- Ledger format: `reviews/README.md`
