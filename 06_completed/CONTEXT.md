# 06_completed — Stage Contract

**Terminal stage.** Read-only record of approved designs and their review history. No routing out.

**One job:** preserve the final approved package and its complete review history.

## Input vs output here

- `input/<ID>/` receives the approved package copied from `05_formal-review`: final SDD, formal decision record, all review rounds, all response logs, all manifests.
- `output/<ID>/` holds only the generated `<ID>-completion-manifest.md` inventorying that package.

## Admission rule

A package may enter **only** with a valid human-authored formal decision record: decision `Approved` (or `Approved with Conditions` with every condition owned, dispositioned, and marked non-blocking), a named human actor, and a signature date. Anything else — including an editor "Ready" verdict alone — is rejected: append a ledger row noting the rejection and treat it as an ambiguous state.

## Output (`output/<ID>/`)

- `<ID>-completion-manifest.md` (from `completion-manifest-template.md`)

## Prohibitions

Do not place unapproved or superseded drafts here. Do not modify anything after completion — corrections to an approved design are a **new review** with a new review ID that references this one.
