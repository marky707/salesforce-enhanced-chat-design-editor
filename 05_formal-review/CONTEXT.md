# 05_formal-review — Stage Contract

**HUMAN STOP.** The accountable senior architect and governance reviewers own this stage. AI readiness never substitutes for approval.

**One job:** hold the package for accountable human architecture review and record the decision.

## Input (`input/<ID>/`)

- **`<ID>-formal-review-packet.md` — start here.** The cover sheet links the SDD version under review, the latest review with its open decisions, the current requirements and decision register, the decision form, and the reading order.
- Top level: only what the reviewer acts on — latest design, ready verdict, current supporting artifacts, decision template.
- `history/` subfolder: the complete audit trail — all earlier review rounds, response logs, and superseded drafts and artifact versions. Consult as needed; it travels with the package to `06_completed`.

## Output (`output/<ID>/`)

- `<ID>-formal-decision.md` — **human-authored** decision record: `Approved`, `Approved with Conditions`, or `Changes Required`

## Routing

- **`Approved` →** copy the approved package and decision record to `06_completed/input/<ID>/`, append ledger row (with human actor), continue automatically.
- **`Approved with Conditions` →** advances to `06_completed` **only when** every condition is recorded with an owner and disposition and the human reviewer has marked it non-blocking. Otherwise the package waits here.
- **`Changes Required` →** copy the decision packet to `03_author-revision/input/<ID>/`, append ledger row, stop (human stop follows). The revision then loops through `04` and `02` as usual.

## AI behavior in this stage

The AI may assemble the review packet, verify the history is complete, and validate that a decision record is well-formed. The AI must **not** create, infer, draft, or sign the decision. A decision record without a named human actor and date is invalid — treat advancing on one as an ambiguous state.
