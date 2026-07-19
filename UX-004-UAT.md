# UX-004 Independent UAT Report

- **Date:** 2026-07-19
- **Tester role:** Independent UAT analyst
- **Run:** UX-004
- **Mode:** Fictional demo based on `fixtures/northstar/`
- **Final authoritative state:** `05_formal-review`, round 02, SDD v2
- **Overall result:** **PASS after one High-severity parser defect was fixed and regression-tested**
- **Human boundary:** Preserved. No formal decision was created, inferred, selected, or signed. The package correctly stops at the accountable human decision gate.

## Scope and test data provenance

The test started from the three Northstar fixture artifacts as a new UX-004 demo submission. Round-01 author revision used the already-existing fictional human-authored UX-003 revision package as the permitted canned test submission. The only transformation was the mechanical review-ID substitution `UX-003` → `UX-004`; the SDD, response content, and decision-register content were otherwise unchanged. File-copy integrity was verified across the author output, revision-intake, editor-review, and formal-review stages.

The run exercised:

1. New-ID and package preflight
2. Ledger and generated status creation
3. Intake and automatic route to editor review
4. Round-01 critic-only review and author packet
5. Author-stop file detection and revision preflight
6. Deliberate human submission event and revision intake
7. Round-02 re-review with requirement/acceptance drift carried forward
8. Round-versioned formal packet, decision index, blank FORM, checksum manifest, status, and link/state validation
9. Missing and invalid formal-decision failure behavior
10. Validation of an existing completed package (`UX-002`)

## End-to-end result

| Checkpoint | Expected | Evidence | Result |
|---|---|---|---|
| Start preflight | Inspect without reserving ID | 5 passes, diagram warning; ledger remained absent | PASS |
| Initial ledger/status | Demo state at `01_intake`, round 01, v1 | `validate-state UX-004`: 7 passes, 0 failures | PASS |
| Intake | Reviewable package routes to `02` despite missing separate diagrams | Intake manifest plus ledger transition | PASS |
| Editor round 01 | Critic-only report, ≤5 findings, no design rewrite | Three Blocking + two High findings; route to `03` | PASS |
| Author stop | Cover, finding index, blank response blocks, exact next action | Status links and packet links validated | PASS |
| Missing revision | Must fail without state change | Preflight returned 1 failure: no files in `04` | PASS |
| Candidate revision detection | Status notices files but does not advance | “Revision files detected … not yet accepted” | PASS |
| Revision preflight | New SDD + all response blocks accepted; drift surfaced | 6 passes, 1 R-05 warning, 0 failures | PASS |
| Revision submission | Human actor recorded before automated intake | Ledger transition `03` → `04` names fictional human author and canned provenance | PASS |
| Revision intake | Round increments only after completeness passes | Round 02/v2 route to `02`; warning retained in manifest | PASS |
| Editor round 02 | Prior findings evaluated; readiness separated from approval | Ready with five structured open decisions; no priority findings | PASS |
| Formal packet | Current material at top; history below; round-versioned artifacts | Cover, index, FORM, and manifest use `round-02`; links validate | PASS |
| Artifact manifest | SHA-256 inventory is stable and excludes itself | Two renders compared byte-for-byte equal | PASS |
| Missing decision | Must fail and remain at `05` | 1 deterministic failure; ledger unchanged | PASS |
| Blank/invalid decision | Must reject every blank judgment/signature field | Post-fix: 24 failures, including decision, actor, role, date, and four fields for each of five IDs | PASS |
| Existing completion | A known completed package still validates | `validate-state UX-002`: 6 passes, 0 failures | PASS |
| Registry purity | Exactly ledger + status for UX-004 | File count = 2; validator pass | PASS |
| Final stop | No decision output; no premature completion | `validate-state UX-004`: 10 passes, 0 failures | PASS |

## Exact helper and verification commands

The following commands were executed from the repository root. Commands were rerun after relevant ledger transitions and after the parser fix.

```bash
python3 -m py_compile tools/review_state.py tools/test_review_state.py
python3 -m unittest tools/test_review_state.py

python3 tools/review_state.py preflight start UX-004
python3 tools/review_state.py status UX-004 --write
python3 tools/review_state.py validate-state UX-004

python3 tools/review_state.py preflight revision UX-004
python3 tools/review_state.py status UX-004 --write
python3 tools/review_state.py validate-state UX-004

python3 tools/review_state.py manifest UX-004 --write
python3 tools/review_state.py status UX-004 --write
python3 tools/review_state.py validate-state UX-004

python3 tools/review_state.py preflight decision UX-004
python3 tools/review_state.py validate-state UX-002
```

Additional deterministic checks:

```bash
cmp -s /tmp/ux004-manifest-first.md /tmp/ux004-manifest-second.md
cmp -s 02_editor-review/input/UX-004/northstar-sdd-draft-v1.md 03_author-revision/input/UX-004/northstar-sdd-draft-v1.md
cmp -s 02_editor-review/output/UX-004/UX-004-review-round-01.md 03_author-revision/input/UX-004/UX-004-review-round-01.md
cmp -s 03_author-revision/output/UX-004/northstar-sdd-draft-v2.md 04_revision-intake/input/UX-004/northstar-sdd-draft-v2.md
cmp -s 04_revision-intake/input/UX-004/northstar-sdd-draft-v2.md 02_editor-review/input/UX-004/northstar-sdd-draft-v2.md
cmp -s 02_editor-review/input/UX-004/northstar-sdd-draft-v2.md 05_formal-review/input/UX-004/northstar-sdd-draft-v2.md
test $(find reviews -maxdepth 1 -type f -name 'UX-004-*' | wc -l | tr -d ' ') -eq 2
```

Final automated test evidence:

```text
Ran 13 tests in 0.009s
OK

Validate state — UX-004
Result: 0 failure(s), 0 warning(s), 10 pass(es)

Validate state — UX-002
Result: 0 failure(s), 0 warning(s), 6 pass(es)
```

## Defects found

### UAT-001 — Blank formal fields were interpreted as populated — High — Fixed and verified

**Observed:** A byte-identical blank decision FORM placed temporarily at the expected human-output filename correctly failed overall, but the preflight parser initially reported the following false passes:

- Accountable human actor appeared to be `- **Role:**`
- Reviewer role appeared to be `- **Date signed (ISO 8601):**`
- Selected option, rationale, and concurrence fields appeared filled because the next markdown label was consumed as the field value

**Risk:** A partially completed human record could receive misleading field-level validation. Although other failures prevented this particular blank form from advancing, the parser was not reliably enforcing the human accountability boundary field by field.

**Cause:** Field patterns allowed newline-crossing whitespace before capturing the value.

**Correction applied by implementation owner:** Parsing was restricted to same-line/horizontal whitespace for response fields, decision dispositions, signature actor/role/date, and review-ID metadata. Placeholder handling and explicit concurrence semantics were also hardened, with targeted regressions added.

**Retest:** PASS. The blank FORM now returns 24 explicit failures: no selected decision, actor, role, date, and missing selected disposition, rationale, concurrence/evidence, and blocking status for each of OD-01, OD-02, OD-03, OD-E01, and OD-E02. The final full unit suite passes 13/13.

**Cleanup:** The temporary blank candidate was removed after the negative test. No formal decision file remains in `05_formal-review/output/UX-004/`.

## UX observations and recommended follow-ups

### 1. Clarify the revision-preflight moment — Low — Resolved after UAT

The original `04_revision-intake/CONTEXT.md` wording could be read as calling preflight after the ledger had already advanced. It now states the exact sequence: while the ledger remains at `03`, run preflight; on human invocation append the `03` → `04` submission row; then perform stage-04 validation and carry warnings forward.

### 2. Give automated-stage status cards more specific microcopy — Low — Resolved after UAT

Automated-stage status now names the work in progress. Editor state reports `automated editor review round <NN>` / `Editor review round <NN> is in progress`; revision intake reports `automated revision-intake validation` / `Revision submitted; revision-intake validation is in progress`.

### 3. Consider optional cross-stage copy-integrity validation — Low / defense in depth

`validate-state` verifies the active location, registry, packet links, and gate artifacts, but it does not compare the hashes of a source artifact and its copied destination across transitions. Manual `cmp` checks passed in UX-004. An optional transition-receipt checksum comparison would detect accidental copy truncation or substitution earlier.

### 4. Keep requirement-drift detection advisory — Working as designed

The R-05 warning successfully caught the unqualified requirement versus “at least 95%” acceptance criterion and carried it to OD-E02. The warning remains appropriately non-blocking because only the requirement owner and accountable architect can reconcile it.

### 5. Preserve the current formal-review layering — Working well

The top-level current/actionable material, separate `history/`, authoritative decision index, round-versioned FORM, and generated checksummed manifest made the human gate materially easier to understand than the legacy unversioned packets. No folder-structure change is recommended.

## Final regression addendum

The two Low-severity UX changes made after the main UAT were independently regressed without altering any core file:

| Regression | Evidence | Result |
|---|---|---|
| Revision submission order | `04_revision-intake/CONTEXT.md` line 28 explicitly orders preflight at `03`, human invocation and `03` → `04` ledger row, then stage-04 validation | PASS |
| Editor automated-stage status | Synthetic `02_editor-review`, round 02 render says “automated editor review round 02” and “Editor review round 02 is in progress” | PASS |
| Revision-intake automated-stage status | Synthetic `04_revision-intake` render says “automated revision-intake validation” and “Revision submitted; revision-intake validation is in progress” | PASS |
| Full helper regression | `python3 -m unittest tools/test_review_state.py`: 13 tests, all pass | PASS |
| Live package regression | `validate-state UX-004`: 10 passes, 0 warnings, 0 failures | PASS |

No new defects were found. These checks close Low-severity observations 1 and 2 above.

## Final UAT disposition

**Accepted for the automatable workflow through the formal human-decision gate.** No unresolved Critical, High, or Medium defects remain from this UAT. UX-004 is intentionally stopped at `05_formal-review` with no decision output and no `06_completed` package. A real accountable human reviewer is the only valid actor who can continue this demo run.
