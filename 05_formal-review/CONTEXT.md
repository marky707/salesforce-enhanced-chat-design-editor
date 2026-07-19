# 05_formal-review — Stage Contract

**HUMAN STOP.** The accountable senior architect and governance reviewers own this stage. AI readiness never substitutes for approval.

**One job:** hold the package for accountable human architecture review and record the decision.

## Input (`input/<ID>/`)

- **`<ID>-formal-review-packet.md` — start here.** The cover sheet names the SDD version under review, the latest review with its open decisions, the decision form, and the reading order; everything else in the folder is history you consult only as needed.
- Latest design (the version that earned the ready verdict)
- The latest ready verdict and complete review history (all rounds)
- All revision-response logs
- Open decisions surfaced by the editor
- `formal-decision-template.md` (copy from this folder)

## Output (`output/<ID>/`)

- `<ID>-formal-decision.md` — **human-authored** decision record: `Approved`, `Approved with Conditions`, or `Changes Required`

## Routing

- **`Approved` →** copy the approved package and decision record to `06_completed/input/<ID>/`, append ledger row (with human actor), continue automatically.
- **`Approved with Conditions` →** advances to `06_completed` **only when** every condition is recorded with an owner and disposition and the human reviewer has marked it non-blocking. Otherwise the package waits here.
- **`Changes Required` →** copy the decision packet to `03_author-revision/input/<ID>/`, append ledger row, stop (human stop follows). The revision then loops through `04` and `02` as usual.

## AI behavior in this stage

The AI may assemble the review packet, verify the history is complete, and validate that a decision record is well-formed. The AI must **not** create, infer, draft, or sign the decision. A decision record without a named human actor and date is invalid — treat advancing on one as an ambiguous state.
