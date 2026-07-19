# 01_intake — Stage Contract

**One job:** validate that an initial submission is sufficiently complete to be reviewed. Nothing else.

## Input (`input/<ID>/`)

- Draft Solution Design Document (SDD)
- Requirements list
- Assumptions and open decisions
- Available diagrams (embedded or as files)
- Any supporting references the draft cites

## Output (`output/<ID>/`)

- `<ID>-intake-manifest.md` (from `intake-manifest-template.md`), always
- `<ID>-intake-errors.md`, only when incomplete — naming each missing or unusable item precisely

## Completion criteria

Intake completeness is **not** design readiness. A package passes intake even with a missing or weak diagram — that absence is an editor finding, recorded in the manifest and allowed through. Intake fails only when a responsible review cannot begin:

- No readable design document
- The intended scope cannot be identified
- Files the draft references are unavailable with no explanation
- The package cannot be associated with a review ID and document version

## Routing

- **New submission with no ledger →** confirm or assign the review ID (scheme in root `CONTEXT.md`; check `reviews/` for taken IDs), then create `reviews/<ID>-routing-log.md` with a `received` row naming the human submitter. Then validate.
- **Complete →** copy `input/<ID>/` to `02_editor-review/input/<ID>/`, append ledger row, continue automatically.
- **Incomplete →** package remains here; write the errors report; append ledger row (`intake incomplete`); stop for the author to supply missing material.

## Prohibitions

Do not critique the architecture, improve the design, or comment on design quality. Judging the design is `02_editor-review/`'s job.
