# 04_revision-intake — Stage Contract

**One job:** validate that a resubmission is complete and traceable to the prior findings. Nothing else.

## Input (`input/<ID>/`)

- Revised SDD (new document version)
- Completed revision-response log for the round being answered
- Any new or changed supporting artifacts

## Output (`output/<ID>/`)

- `<ID>-revision-intake-manifest-round-<NN>.md` (from `revision-intake-manifest-template.md`), always
- `<ID>-revision-intake-errors-round-<NN>.md`, only when incomplete

## Completion criteria

A resubmission is complete when:

- The revised SDD is present, readable, and carries a new declared document version
- The response log answers **every** finding of the review round it names (resolved, partially resolved, or documented disagreement — disagreement does not fail intake)
- The response log names the correct review round
- New artifacts the revised draft references are present or their absence is explained

## Routing

- **Complete →** copy `input/<ID>/` to `02_editor-review/input/<ID>/`, **increment the review round**, append ledger row, continue automatically.
- **Incomplete →** copy the errors report to `03_author-revision/input/<ID>/`, append ledger row, stop (human stop).

## Prohibitions

Do not decide whether the author actually **solved** a design finding — that judgment belongs to `02_editor-review/`. A response log entry that says "resolved" with a named location passes here even if the fix is weak; the editor will judge it next round.
