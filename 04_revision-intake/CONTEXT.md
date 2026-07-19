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
- Material requirement wording and SDD acceptance criteria have been compared; any silent quantifier/population/threshold change is recorded for editor review rather than accepted administratively

## Routing

- **Submission order →** while the ledger still waits at `03_author-revision`, run `python3 tools/review_state.py preflight revision <ID>`. A failure stops with no ledger change. When preflight passes and the human invokes `submit revision <ID>`, append the human submission row (`03` → `04`), then perform this stage's validation. Record warnings—including requirement/acceptance drift—in the manifest and pass them to the editor.
- **Complete →** copy `input/<ID>/` to `02_editor-review/input/<ID>/`, retain unchanged current supporting artifacts from the prior package, **increment the review round**, append ledger row, regenerate status, validate state, and continue automatically.
- **Incomplete →** copy the errors report to `03_author-revision/input/<ID>/`, append ledger row, stop (human stop).

## Prohibitions

Do not decide whether the author actually **solved** a design finding — that judgment belongs to `02_editor-review/`. A response log entry that says "resolved" with a named location passes here even if the fix is weak; the editor will judge it next round.
