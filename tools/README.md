# tools/

Standard-library-only helpers for the repository workflow. They do not replace the stage contracts or the accountable human roles.

## `docx_to_md.py`

Converts a Word SDD into reviewable markdown while retaining the original `.docx` as source of record. See `01_intake/CONTEXT.md`.

## `review_state.py`

Makes the markdown workflow observable without changing authoritative state.

```bash
python3 tools/review_state.py preflight start NS-001
python3 tools/review_state.py preflight revision NS-001
python3 tools/review_state.py preflight decision NS-001
python3 tools/review_state.py status NS-001
python3 tools/review_state.py status NS-001 --write
python3 tools/review_state.py validate-state NS-001
python3 tools/review_state.py manifest NS-001
python3 tools/review_state.py manifest NS-001 --write
```

### Guarantees

- `preflight` never creates a ledger or accepts a submission.
- `status` derives stage/round/version from the ledger and probes human drop zones without advancing.
- `validate-state` checks ledger/status alignment, registry purity, current-stage artifacts, packet links, and premature completion.
- `manifest` inventories the current package with SHA-256 checksums.
- Requirement/acceptance drift is a warning for accountable review, never an automated decision.
- The helper never critiques design content, appends a ledger row, copies packages, supplies human decision content, or approves architecture.

Exit status is nonzero when a preflight or validation has failures. Warnings preserve human judgment and return success when no deterministic failure exists.
