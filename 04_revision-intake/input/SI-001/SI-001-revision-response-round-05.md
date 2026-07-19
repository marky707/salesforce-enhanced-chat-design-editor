# Revision Response Log — SI-001 — Round 05

- **Review ID:** SI-001
- **Responding to:** `SI-001-review-round-05.md`
- **Revised document version:** v6 (`solstice-sdd-draft-v6.md`)
- **Author (human actor):** P. Okafor
- **Date (ISO 8601):** 2026-07-19

---

## Finding 1: The OTP result has two incompatible trust-boundary paths

- **Disposition (mark one):** [x] resolved
- **Where the design changed:** Sections 3.1 (diagram corrected), 3.2 (correlation field added), 9.2 (sequence diagram re-included and corrected)
- **What changed / why (your own words):** The reviewer caught a real contradiction — my context diagram showed the OTP service talking straight to Salesforce while the contract said the result rides in the launcher payload. One path now, everywhere: OTP service signs the result, hands it back to the launcher, and it enters Salesforce only inside Contract v1.0, validated server-side. I also added the correlation rule (the signed result carries the portalSessionId and must match the payload's) so a signed result can't be replayed into a different session, and the 9.2 sequence diagram now shows the same handoffs as 3.1 and 3.2.

## Finding 2: The failed non-resumption test has no coherent operating model

- **Disposition (mark one):** [x] resolved
- **Where the design changed:** Section 5.2 rewritten; Section 11 lifecycle row; Section 8 closing note
- **What changed / why (your own words):** I was trying to have it both ways — claiming the invariant while hand-waving a fallback. Non-resumption is now a design invariant enforced by a launch gate: if any return path reuses a session Id, the acceptance test fails and launch preparation stops until the invariant is restored or the design formally returns to review. There is no "documented contingency" acceptance path anymore, because Case selection, verification, and every KPI boundary genuinely depend on one pre-chat equals one session.

## Finding 3: The ER cardinalities contradict optional and unverified relationships

- **Disposition (mark one):** [x] resolved
- **Where the design changed:** Section 6.2 diagram and sources-of-truth notes
- **What changed / why (your own words):** Corrected the encodings to match the prose: Contact and Booking are 0..1 per Case (unverified Cases have neither), a session's Case is 0..1 (temporarily none on flow failure until 6.1 remediation), and a log row's session lookup is 0..1. Also stated that the Case is the single source of truth for both associations, written exactly once by the verification paths.

## Finding 4: OD-02 is simultaneously closed and open across the submitted package

- **Disposition (mark one):** [x] resolved
- **Where the design changed:** Section 3 disposition paragraph; new supporting artifact `solstice-assumptions-open-decisions-v2.md`
- **What changed / why (your own words):** The decision register and the SDD now say the same thing: OD-02's architecture impact is closed with a dated disposition, the remaining scope is UX-only with a named owner, and there's an explicit reopening condition if a placement change ever touches launcher initialization. OD-01 stays open on purpose — that one belongs to the senior architect.

---

## New material introduced this round

- `solstice-assumptions-open-decisions-v2.md` (changed supporting artifact — OD-02 dispositioned, OD-01 explicitly reserved)
- No new architectural content: v6 is a consistency pass. Deferred items from round 5 addressed where possible now: build-week evidence remains scheduled (it cannot exist before build; the 5.2 and 3.2 gates define what it must show), Booking-to-Case source of truth is stated in 6.2, and the consistency sweep across process/TravelPort/rollback/redaction/operations tests is this revision.
