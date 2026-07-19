# 03_author-revision — Stage Contract

**HUMAN STOP.** This is the author's workspace. The workflow does not advance until the author deliberately submits a revision package.

**One job:** give the human author a controlled place to resolve findings.

## Input (`input/<ID>/`)

- The current design package
- The latest editor review report (or formal-review decision packet with required changes)
- `revision-response-template.md` (copy from this folder)

## Output (`output/<ID>/`)

- Revised SDD (new document version)
- `<ID>-revision-response-round-<NN>.md` — one traceable response per finding: the location changed, the rationale, or a documented disagreement

## Routing

**No automatic exit.** When finished, the author copies the revised SDD, completed response log, and any new or changed supporting artifacts into `04_revision-intake/input/<ID>/` and invokes the workflow. That submission is a human action — record the human actor in the ledger row.

## AI behavior in this stage

The AI may **explain** a finding — what the gap is, why the consequence follows, what kind of information would resolve it. The AI must **not** write replacement design content, propose specific wording, draft the diagram, or fill in the response log's design answers. If the author asks the AI to write the fix, decline and point to this contract.
