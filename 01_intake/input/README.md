# 01_intake/input/ — New submissions

The easiest first-time path is to attach the documents in chat and say `start`; the agent assigns/checks the review ID, files the package, and reports every rename. Manual filing remains available when you want full visibility.

## Before you start

- **Required:** one readable draft SDD with a declared version and identifiable Enhanced Chat v1 / Omni-Channel scope.
- **Required:** the requirements source, either embedded in the SDD or supplied separately.
- **Required when applicable:** assumptions/open decisions and external sources the design depends on.
- **Optional:** available diagrams and supporting evidence. Missing author-produced diagrams pass through for the editor to critique.
- **Do not submit:** expected-review fixtures, prior workflow outputs, unsigned decision records, or files from another review ID.

## Manual filing

1. Use an unused ID shaped like `NS-001`. If unsure, ask the agent to assign one; do not reuse an existing ledger or package folder.
2. Create `01_intake/input/<ID>/` and place the source documents there. Recommended names: `<project>-sdd-draft-v1.md`, `<project>-requirements.md`, and `<project>-assumptions-open-decisions.md`.
3. Run `python3 tools/review_state.py preflight start <ID>` or ask the agent: `preflight start <ID>`.
4. If the preflight is acceptable, say `start <ID>`. Preflight does not create the ledger or advance the package.

Accepted formats: markdown, plain text, PDF, or Word. Intake converts `.docx` to markdown automatically and keeps the Word file as the source of record; see `../CONTEXT.md`.

What happens next: intake checks reviewability, the critic reviews the design, and the workflow stops either for author revision or accountable human formal review.
