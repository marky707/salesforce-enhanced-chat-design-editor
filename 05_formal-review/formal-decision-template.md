# Formal Architecture Review Decision — <REVIEW-ID>

<!-- Stable template: contains no run-specific facts. Fill a copy in output/<ID>/.
     THIS RECORD MUST BE AUTHORED BY THE ACCOUNTABLE HUMAN REVIEWER.
     The routing agent may pre-fill administrative metadata, decision IDs/questions,
     and source links only. An AI agent must never select options, write rationale,
     supply concurrence, create conditions/required changes, or sign. -->

- **Review ID:**
- **Document version reviewed:**
- **Review rounds completed:**
- **Date (ISO 8601):**

## Decision

<!-- Circle one. This is architecture approval authority — human judgment only. -->

`Approved` / `Approved with Conditions` / `Changes Required`

- `Approved` → the validated final package advances to read-only completion.
- `Approved with Conditions` → advances only when every condition is owned, dispositioned, and explicitly non-blocking.
- `Changes Required` → the workflow creates an author packet and returns through revision intake and editor review.

## Open decision dispositions

<!-- The generated FORM repeats one blank block per ID from the authoritative
     open-decision index. The agent pre-fills ID, question, state, and source only.
     An entry whose index state is `content missing` cannot be approved — there is
     nothing to approve yet; disposition it as a required change or an owned deferral. -->

### <OD-ID> — <decision title/question>

- **State from decision index:**
- **Source:**
- **Selected option / disposition (human):**
- **Reviewer rationale (human):**
- **Required concurrence and evidence (human):**
- **Condition or required change (human):**
- **Blocking? (human):** yes / no / n-a

## Rationale

<!-- The reviewer's reasoning, in their own words. -->

## Conditions (only for Approved with Conditions)

| # | Condition | Owner | Disposition | Blocking? |
|---|---|---|---|---|
| 1 | | | | yes/no |

<!-- The package advances to 06_completed only when every row is filled and the
     reviewer has marked every condition non-blocking. -->

## Required changes (only for Changes Required)

<!-- Specific changes the author must make. These route back to 03_author-revision. -->

-

## Residual risk dispositions

| Risk | Owner | Required evidence | Due gate | Blocking? | Human disposition |
|---|---|---|---|---|---|
| | | | architecture / build entry / UAT / production entry | yes/no | |

## Signature

- **Accountable reviewer (human actor):**
- **Role:**
- **Date signed (ISO 8601):**

---

**After signing — three steps, then you're done:**

1. Save this file as `<ID>-formal-decision-round-<NN>.md` in `05_formal-review/output/<ID>/`, using the current ledger round for `<NN>` (create the folder if needed, or attach the signed file in chat and ask the agent to file it).
2. Tell the agent: *"I've recorded my formal decision for `<ID>`. Please continue the workflow."* The agent validates the record first and reports anything to correct — missing decision IDs, concurrence, conditions, required changes, or signature fields. (Power users can run the check themselves: see `tools/README.md`.)
3. Do **not** move anything into `06_completed/`; you are done only when status shows **Completed** or names the next author action.

## Human completeness checklist

- [ ] Every ID in `<ID>-open-decision-index-round-<NN>.md` has a disposition and rationale
- [ ] Required co-owner/concurrence evidence is named
- [ ] Conditions have owners, dispositions, and blocking status
- [ ] `Changes Required` includes specific author-action bullets
- [ ] Residual risks have an owner/evidence gate or an explicit disposition
- [ ] Decision, accountable reviewer, role, and signature date are complete
