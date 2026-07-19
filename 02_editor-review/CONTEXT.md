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

- **`Revise Before Formal Review` or `Insufficient Context` →** copy the package plus the new review report to `03_author-revision/input/<ID>/`, append ledger row, stop (human stop follows).
- **`Ready for Formal Review` or `Ready for Formal Review with Open Decisions` →** copy the package, review history, and response logs to `05_formal-review/input/<ID>/`, append ledger row, stop (human stop follows).

## Prohibitions

Do not rewrite, complete, or generate design content or diagrams. Do not approve. Do not re-run intake validation as a substitute for critique. Do not exceed five findings.
