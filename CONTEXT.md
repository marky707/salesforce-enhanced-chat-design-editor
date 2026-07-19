# Pipeline Context — Salesforce Enhanced Chat Design Review Editor

One ICM pipeline. A draft Solution Design Document (SDD) enters at intake, is critiqued by the editor, is revised by its human author, and exits only after a human-recorded formal decision. This file routes work; it stores no Salesforce domain content.

## Stages

| Stage | One job | Input | Output | Routes to |
|---|---|---|---|---|
| `01_intake/` | Validate the initial package is reviewable | Draft SDD, requirements, assumptions, diagrams | Intake manifest (or intake-errors report) | Complete → `02` · Incomplete → stays here **(human supplies missing items)** |
| `02_editor-review/` | Critic-only readiness review | Validated package (+ prior review and response log on later rounds) | Review report: verdict + ≤5 findings | Revise / Insufficient Context → `03` · Ready → `05` |
| `03_author-revision/` | **HUMAN STOP** — author resolves findings | Current design + review packet | Revised SDD + response log | Author deliberately submits to `04` |
| `04_revision-intake/` | Validate resubmission completeness and traceability | Revised SDD + response log | Revision-intake manifest (or errors report) | Complete → `02` (round +1) · Incomplete → `03` |
| `05_formal-review/` | **HUMAN STOP** — accountable architect records decision | Layered ready packet: cover sheet + current material, history in `history/` | Human-authored decision record | Approved → `06` · Changes Required → `03` |
| `06_completed/` | Preserve the approved package | Approved design + decision record | Completion manifest | Terminal, read-only |

A stage never performs the next stage's job. Read only the current stage's `CONTEXT.md` and the files it routes to.

## Conventions (apply at every stage)

- **Review ID:** short letter prefix + zero-padded sequence (`NS-001`). The ledger files in `reviews/` are the registry of assigned IDs.
- **Package subfolder:** all files for one review live in a subfolder named for its ID, e.g. `02_editor-review/input/NS-001/`. Advance a package by **copying** its subfolder into the next stage's `input/`. Never delete or overwrite earlier stage outputs.
- **Routing ledger (authoritative state):** every transition appends one row to `reviews/<ID>-routing-log.md`. Current stage is determined by the **latest ledger row**, never by folder contents alone. Format: see `reviews/README.md`.
- **Status card (generated view):** after every ledger append—and whenever the user asks for status—run `python3 tools/review_state.py status <ID> --write`. The card derives stage from the ledger, probes human drop zones without advancing them, links the next packet, and includes the latest transition receipt. The ledger remains authoritative.
- **Preflight and validation:** `python3 tools/review_state.py preflight <start|revision|decision> <ID>` inspects a human submission without changing state. `validate-state <ID>` compares ledger, status, package, registry, and links. A validation failure is ambiguity: preserve evidence and stop.
- **Rounds:** review artifacts are versioned `<ID>-review-round-01.md`, `<ID>-revision-response-round-01.md`, etc. `04` increments the round on each complete resubmission.
- **Re-entry:** when a package re-enters a stage (e.g. `02` on round 2), copy into the **same** `input/<ID>/` subfolder. Because every artifact filename carries its version or round (`-v2`, `-round-02`), re-entry adds files and never overwrites; never reuse a filename for changed content. The latest ledger row declares which version and round are current.
- **Author working copy vs. submission:** `03_author-revision/output/<ID>/` retains the author's finished working copy. The author deliberately submits every changed artifact to `04_revision-intake/input/<ID>/`; file placement alone does not append the ledger or advance state.
- **Formal decision index:** when a package enters `05`, `<ID>-open-decision-index-round-<NN>.md` is the authoritative list for that formal-review round. It labels author-raised and editor-raised decisions, required authorities, missing evidence, and readiness state; older counts in the SDD/register remain historical context.
- **Terminal history model:** stages `01`–`05` preserve all drafts in place. The terminal package contains the final SDD plus manifests, reviews, responses, workflow evidence, current supporting artifacts, and the human decision; superseded SDDs remain preserved upstream and are excluded from `06`.
- **Timestamps:** ISO 8601 date (`2026-07-18`), taken from the environment's current date.
- **Automatic ≠ unattended:** after a user invokes the workflow, complete every eligible rule-based transition, then stop. The only stops are: incomplete intake, findings awaiting the author (`03`), a package awaiting the formal human decision (`05`), the terminal stage (`06`), or an ambiguous state.
- **Ambiguity:** conflicting ledger rows, validation failure, a response log naming the wrong round, or multiple undeclared versions → write a state-error report to the current stage's `output/<ID>/`, preserve all evidence, and stop. Never guess.

## Authority boundary

The editor's "Ready for Formal Review" measures **document readiness, not architecture approval**. Only a human-authored decision record in `05_formal-review/` approves a design, and only an approved package may enter `06_completed/`.
