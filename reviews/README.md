# reviews/ — Routing Ledgers and Status Cards

The workflow state registry. **Exactly two files may exist here per review ID — nothing else:**

1. `<ID>-routing-log.md` — the append-only ledger; its **latest row is the authoritative workflow state**
2. `<ID>-status.md` — the generated status card, regenerated after every ledger append and every `status` request

Agent working notes, journals, analyses, or any other artifacts do **not** belong in this folder — put them outside the repository or in a scratch location. This folder only works as a registry if its contents are exactly predictable.

## File naming

Review IDs are a short letter prefix plus a zero-padded sequence (`NS-001`, `NS-002`). This folder is the registry of assigned IDs — before assigning a new ID, list the ledgers here.

## Status card behavior

Generate it with:

```bash
python3 tools/review_state.py status NS-001 --write
```

The ledger supplies authoritative stage/round/version. The generator also probes the two human drop zones without changing state:

- At `03`: files in `04_revision-intake/input/<ID>/` → “Revision files detected — not yet accepted.”
- At `05`: `<ID>-formal-decision-round-<NN>.md` in formal-review output → “Decision file detected — not yet validated.”

The card must also contain the latest transition receipt and operator verbs. A file probe never appends a ledger row or advances a package.

## Status card format

```markdown
# Status — NS-001                      <!-- regenerated; ledger is authoritative -->

- **Where:** 03_author-revision (round 01, SDD v1) — Demo: no
- **Last verdict:** Revise Before Formal Review (5 findings)
- **Waiting on:** the author
- **Submission check:** No revision files detected yet in `04_revision-intake/input/NS-001/`

## Your next action
1. Open [03_author-revision/input/NS-001/NS-001-author-packet.md](../03_author-revision/input/NS-001/NS-001-author-packet.md)
2. Revise the SDD as a new version and complete the pre-filled response form
3. Say `submit revision NS-001` — the agent runs the revision preflight first

## Latest transition receipt

- **Transition:** 02_editor-review → 03_author-revision
- **Status:** Revise Before Formal Review
- **Reason:** five material findings require author action
- **Source artifacts:** 02_editor-review/output/NS-001/NS-001-review-round-01.md
```

Useful waiting-state lines: *"No revision files detected yet"* · *"Revision files detected — not yet accepted; say submit revision"* · *"Decision file detected — not yet validated; say continue"* · *"Completed — package is read-only; new changes need a new review ID."*

## Ledger format

Each ledger is one markdown table. Append one row per transition; never edit or delete prior rows.

```markdown
# Routing Ledger — NS-001

Demo: no    <!-- "yes" when the package originates from fixtures/ -->

| Date | Round | Doc version | From stage | To stage | Status / verdict | Reason | Source artifacts | Human actor |
|---|---|---|---|---|---|---|---|---|
| 2026-07-18 | 01 | v1 | — | 01_intake | received | new submission | 01_intake/input/NS-001/ | J. Author |
| 2026-07-18 | 01 | v1 | 01_intake | 02_editor-review | intake complete | all required items present | 01_intake/output/NS-001/NS-001-intake-manifest.md | — |
```

- **Human actor** is required for every row representing a human decision or submission (intake submission, revision submission, formal decision); use `—` for rule-based transitions.
- A row with **To stage** = current stage and no later row means the package is sitting in that stage.
- Ambiguity (conflicting rows, missing rows for files that exist) → do not repair the ledger; write a state-error report and stop.
- Before and after a state-changing operation, run `python3 tools/review_state.py validate-state <ID>`. Status drift, broken packet links, unexpected registry files, or premature completed artifacts are state errors.
