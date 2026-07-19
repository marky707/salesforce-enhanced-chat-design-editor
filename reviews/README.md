# reviews/ — Routing Ledgers

One append-only ledger per review ID. The **latest row of a ledger is the authoritative workflow state** for that review; folder contents are evidence, not state.

## File naming

`<ID>-routing-log.md`, e.g. `NS-001-routing-log.md`. Review IDs are a short letter prefix plus a zero-padded sequence (`NS-001`, `NS-002`). This folder is the registry of assigned IDs — before assigning a new ID, list the ledgers here.

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
