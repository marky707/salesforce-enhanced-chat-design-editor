# 05_formal-review — Stage Contract

**HUMAN STOP.** The accountable senior architect and governance reviewers own this stage. AI readiness never substitutes for approval.

**One job:** hold the package for accountable human architecture review and record the decision.

## Input (`input/<ID>/`)

- **`<ID>-formal-review-packet-round-<NN>.md` — start here.** The cover links the current SDD, latest review, requirements/register, authoritative decision index, residual-risk table, decision form, artifact manifest, and reading order.
- **`<ID>-open-decision-index-round-<NN>.md` — authoritative for this formal-review round.** It reconciles author-raised and editor-raised decisions and explicitly supersedes older counts embedded in source artifacts without rewriting them.
- **`<ID>-formal-decision-round-<NN>-FORM.md` — the only actionable form.** The stable template remains at the stage root and is not copied into the packet.
- **`<ID>-current-artifacts-round-<NN>.md` — checksummed generated inventory.** Use it to distinguish current, history, and required human output.
- Top level: only current/actionable material. `history/`: earlier rounds, responses, prior drafts, and superseded artifact versions for consultation.

## Output (`output/<ID>/`)

- `<ID>-formal-decision-round-<NN>.md` — **human-authored** decision record: `Approved`, `Approved with Conditions`, or `Changes Required`

Use the ledger's current round for `<NN>`. The round suffix preserves every formal-review cycle if a human returns the package for changes and it later comes back to this gate. Existing legacy runs with unversioned names remain readable but should not be used for new cycles.

## Routing

- **Before routing any decision →** run `python3 tools/review_state.py preflight decision <ID>`. A missing signature, undispositioned decision ID, incomplete condition, missing concurrence, or malformed required-change list stops here without ledger change.
- **`Approved` →** copy the final SDD, current supporting artifacts, reviews/responses/manifests/workflow evidence, structured risk dispositions, and decision record to `06_completed/input/<ID>/`; exclude superseded SDDs (they remain preserved upstream). Append ledger row with human actor, regenerate status, validate, and continue.
- **`Approved with Conditions` →** advances to `06_completed` **only when** every condition has an owner and disposition and is explicitly non-blocking; structured residual risks must also have an owner/evidence gate or be dispositioned in rationale. Otherwise the package waits here.
- **`Changes Required` →** copy the decision packet to `03_author-revision/input/<ID>/`, and generate the author packet and pre-filled response form there exactly as `02_editor-review/CONTEXT.md` specifies for a revise verdict — the reviewer's required changes become the finding blocks. Append ledger row, regenerate the status card, stop (human stop follows). The revision then loops through `04` and `02` as usual.

## AI behavior in this stage

The AI may assemble the review packet, generate the non-decisional index/manifest, verify history, and validate a completed human record. The AI must **not** select an option, write reviewer rationale, supply concurrence, create conditions/required changes, infer approval, or sign. A decision record without a named human actor and date is invalid. Demo mode does not relax this boundary.
