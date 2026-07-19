# Revision Intake Manifest — <REVIEW-ID> — Round <NN>

<!-- Stable template: contains no run-specific facts. Fill a copy in output/<ID>/. -->

- **Review ID:**
- **Prior review answered:** `<ID>-review-round-<NN>.md`
- **New document version:**
- **New review round (on completion):**
- **Submitted by (human actor):**
- **Date (ISO 8601):**

## Resubmission inventory

| Item | Present | Path | Notes |
|---|---|---|---|
| Revised SDD, new declared version | yes/no | | |
| Response log for the correct round | yes/no | | |
| Every prior finding answered | yes/no | | List any unanswered finding numbers |
| New/changed artifacts present or explained | yes/no/n-a | | |
| Preflight revision result | pass/fail | | Record warning count and exact command |
| Requirement/acceptance drift warnings | none/list | | Pass warnings to editor; intake does not disposition them |

## Traceability check

| Finding # | Disposition claimed | Location named | Traceable (yes/no) |
|---|---|---|---|
| 1 | | | |

## Result

- **Status:** complete / incomplete
- **Next stage:** 02_editor-review (round incremented) / 03_author-revision
- **Reason:**
- **Errors report:** none / `<ID>-revision-intake-errors-round-<NN>.md`

## Transition receipt (when complete)

- **Accepted files:**
- **Unchanged current artifacts retained from prior package:**
- **Round change:** answering round `<NN>` → next editor round `<NN+1>`
- **State validation:** pass / fail (`python3 tools/review_state.py validate-state <ID>` after ledger append)
