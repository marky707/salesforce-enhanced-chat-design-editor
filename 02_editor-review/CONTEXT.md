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

- **`Revise Before Formal Review` or `Insufficient Context` →** copy the package plus the new review report to `03_author-revision/input/<ID>/`. Also generate `<ID>-revision-response-round-<NN>.md` there from `03_author-revision/revision-response-template.md`, pre-populated with one block per finding (number and title filled in; answer lines left blank — pre-filling titles is administrative, answering them is the author's). Append ledger row, stop (human stop follows).
- **`Ready for Formal Review` or `Ready for Formal Review with Open Decisions` →** copy the package, review history, and response logs to `05_formal-review/input/<ID>/`, and generate `<ID>-formal-review-packet.md` there — a one-page cover sheet for the human reviewer naming: the current SDD version to review, the latest review (verdict + open decisions), the decision template, a suggested reading order, and a one-line inventory of the history files. **Reference every file as a relative markdown link** (`[name](name.md)`) so the reviewer clicks rather than searches, and state that everything is in the same folder. The cover sheet summarizes and points; it must not argue for approval. Append ledger row, stop (human stop follows).

## Prohibitions

Do not rewrite, complete, or generate design content or diagrams. Do not approve. Do not re-run intake validation as a substitute for critique. Do not exceed five findings.
