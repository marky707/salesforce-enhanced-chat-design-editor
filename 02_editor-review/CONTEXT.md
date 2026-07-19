# 02_editor-review — Stage Contract

**One job:** perform the critic-only readiness review. Nothing else.

## Persona activation

Entering this stage, adopt the editor identity in `identity.md` and obey `rules.md` completely. Load selectively:

1. `identity.md` — who is reviewing (always)
2. `rules.md` — critique behavior, verdicts, output contract (always)
3. `reference/CONTEXT.md` — router to the domain reference that answers the current review question (load referenced files on demand, not all at once)
4. `examples.md` — consult when unsure whether a draft finding is specific enough

The persona and references load **only** in this stage. Leaving this stage, drop them.

## Input (`input/<ID>/`)

- The latest validated package (draft SDD, requirements, assumptions, diagrams)
- On round 2+: the previous review report and the author's revision-response log

## Output (`output/<ID>/`)

- `<ID>-review-round-<NN>.md` — verdict plus at most five prioritized findings, in the exact output contract of `rules.md`

## Routing

- **`Revise Before Formal Review` or `Insufficient Context` →** copy the package plus the new review report to `03_author-revision/input/<ID>/`. Also generate there:
  1. `<ID>-revision-response-round-<NN>.md` from `03_author-revision/revision-response-template.md`, pre-populated with one block per finding (number and title filled in; answer lines left blank — pre-filling titles is administrative, answering them is the author's).
  2. `<ID>-author-packet.md` — the author's cover sheet ("Your turn — revise, respond, submit"), with every file as a relative markdown link: the verdict + link to the review report; a three-step checklist (1. revise the SDD as a new version, 2. complete the pre-filled response form, 3. copy both into `04_revision-intake/input/<ID>/` and tell the agent to continue); the round/version legend below, verbatim; the exact file list to submit; "do not edit the routing ledger"; and "submission is complete only when the files are in 04 **and** you invoke the workflow."

  Round/version legend (include verbatim in every author packet):
  ```text
  • SDD version bumps when design content changes (v1 → v2)
  • Response log round = the review round you are answering
  • Next editor review round = previous + 1, after complete revision intake
  • Requirements/assumptions get a new versioned filename only when their content changes
  ```
  Append ledger row, regenerate the status card, stop (human stop follows).
- **`Ready for Formal Review` or `Ready for Formal Review with Open Decisions` →** deliver a **layered packet** to `05_formal-review/input/<ID>/`: at the top level only what the reviewer acts on — the current SDD, the ready review, the current requirements and decision register, the decision template, and the cover sheet; everything superseded (earlier rounds, response logs, prior drafts and artifact versions) goes in a `history/` subfolder. Generate `<ID>-formal-review-packet.md` as the cover sheet: current material, open decisions, a suggested reading order, and a one-paragraph summary of `history/`. Also generate `<ID>-formal-decision-FORM.md` from the decision template with **only the administrative fields pre-filled** (review ID, version, rounds, date) and the open decisions listed — the Decision, Rationale, Conditions, and Signature sections stay blank for the human reviewer, per the `05` prohibition. **Reference every file as a relative markdown link** (`[name](name.md)`) so the reviewer clicks rather than searches. The cover sheet summarizes and points; it must not argue for approval. Append ledger row, stop (human stop follows).

## Prohibitions

Do not rewrite, complete, or generate design content or diagrams. Do not approve. Do not re-run intake validation as a substitute for critique. Do not exceed five findings.
