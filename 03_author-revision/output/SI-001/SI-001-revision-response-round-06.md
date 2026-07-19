# Revision Response Log — SI-001 — Round 06

- **Review ID:** SI-001
- **Responding to:** `SI-001-review-round-06.md`
- **Revised document version:** v7 (`solstice-sdd-draft-v7.md`)
- **Author (human actor):** P. Okafor
- **Date (ISO 8601):** 2026-07-19

---

## Finding 1: OTP replay rejection has no enforcing state

- **Disposition (mark one):** [x] resolved
- **Where the design changed:** Section 3.2 (one-time-use enforcement); Section 6.2 (`Verification_Use__c`); Section 11 replay test row
- **What changed / why (your own words):** The reviewer was right that equality between two values arriving together proves nothing. There is now real state: every signed result carries a `useId`, and the session-start flow inserts it into `Verification_Use__c`, which has a unique external-Id field — so a second submission of the same result fails the insert atomically, org-wide, and routes unverified with a `replay_reject` log entry. The consumed row is the audit evidence, and the replay test now has an implementable expected result: first use verifies, second use fails the insert.

## Finding 2: The design never establishes which Booking is linked or looked up

- **Disposition (mark one):** [x] resolved
- **Where the design changed:** Sections 9.2 (booking-anchored verification), 3.2 (booking resolution), 6.2 (`Booking_Reference__c`, `TravelPort_Ref__c`), 7 and 7.1 (lookup input)
- **What changed / why (your own words):** Honestly, this hole was there from v1 — nothing ever said which booking. The redesign makes the traveler supply the booking reference: the OTP service validates the ref-plus-email pair against the portal's own booking records before sending the code, so the signed result names the booking. Salesforce matches it to `Booking__c` by unique reference (multiple matches impossible; no match routes unverified), links Case–Booking–Contact in one step — the booking, not the typed email, is the identity anchor — and the agent's TravelPort lookup reads the linked booking's `TravelPort_Ref__c`, so the agent never types a reference and unverified sessions have no lookup at all. R-04's evidence is now traceable end to end.

## Finding 3: The pre-verification Contact match is an undocumented second interface

- **Disposition (mark one):** [x] resolved
- **Where the design changed:** Sections 3.1 and 9.2 (interface removed)
- **What changed / why (your own words):** Rather than document that boundary, I removed it. The booking-anchored flow needs no pre-session Salesforce lookup — the verification offer is a static pre-chat option, and validation happens against the portal's own booking records on the portal side. The launcher's only Salesforce interface is the Contract v1.0 submission, and Salesforce never answers an anonymous "does this customer exist" query, which is better for enumeration exposure too.

---

## New material introduced this round

- Booking-anchored verification redesign (9.2), `Verification_Use__c` replay state, `Booking_Reference__c` / `TravelPort_Ref__c` fields
- Round-6 deferred items addressed proactively: `MessagingEndUser` added to the ER view with its verified-only Contact link (6.2); process view now shows the customer-close branch and all three end reasons, recorded as `End_Reason__c` (5, 5.3); agent presence eligibility, channel isolation, and capacity-of-3 validation during the 10% phase (4.2, 10.1); TravelPort retry now drawn as a second named-credential request (7.1)
