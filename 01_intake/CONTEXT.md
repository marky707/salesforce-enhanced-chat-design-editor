# 01_intake — Stage Contract

**One job:** validate that an initial submission is sufficiently complete to be reviewed. Nothing else.

## Input (`input/<ID>/`)

- Draft Solution Design Document (SDD)
- Requirements list
- Assumptions and open decisions
- Available diagrams (embedded or as files)
- Any supporting references the draft cites

**Accepted formats:** markdown, plain text, PDF — or Word (`.docx`). A `.docx` is converted during intake, before validation: run `python3 tools/docx_to_md.py <file>.docx <file>.md` into the same `input/<ID>/` folder, keep the original `.docx` as the source of record, and note the conversion in the manifest. The converted markdown is what downstream stages review. If the converter reports embedded images, record in the manifest that those diagrams need separate image exports (their absence passes through as an editor finding, as usual). Conversion is administrative — it never alters wording.

## Output (`output/<ID>/`)

- `<ID>-intake-manifest.md` (from `intake-manifest-template.md`), always
- `<ID>-intake-errors.md`, only when incomplete — naming each missing or unusable item precisely

## Completion criteria

Intake completeness is **not** design readiness. A package passes intake even with a missing or weak diagram — that absence is an editor finding, recorded in the manifest and allowed through. This includes diagrams, appendices, and sections **the draft itself references but does not include** (e.g. "see the routing diagram in Appendix A" with no Appendix A): that is design incompleteness for the editor to critique, never an intake blocker. Intake fails only when a responsible review cannot begin:

- No readable design document
- The intended scope cannot be identified
- **Source material** the review cannot responsibly proceed without is referenced but unavailable and unexplained — external inputs the design builds on (a requirements document, a cited standard, a predecessor design), not artifacts the author was supposed to produce as part of the design
- The package cannot be associated with a review ID and document version

## Routing

- **New submission with no ledger →** confirm or assign the review ID (scheme in root `CONTEXT.md`; check `reviews/` for taken IDs), then create `reviews/<ID>-routing-log.md` with a `received` row naming the human submitter. Then validate.
- **Complete →** copy `input/<ID>/` to `02_editor-review/input/<ID>/`, append ledger row, continue automatically.
- **Incomplete →** package remains here; write the errors report; append ledger row (`intake incomplete`); stop for the author to supply missing material.

## Prohibitions

Do not critique the architecture, improve the design, or comment on design quality. Judging the design is `02_editor-review/`'s job.
