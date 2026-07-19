# Design Review

## Verdict
Revise Before Formal Review

The revised views are more consistent, but the design still cannot prove replay rejection or trace the pre-verification Contact match and Booking selection through their required interfaces.

> This verdict measures document readiness, not architecture approval. Final design approval remains with the accountable human architect and governance reviewers.

## Priority Findings

Round 5 resolution check:

- Finding 1 — Partially resolved: Sections 3.1, 3.2, and 9.2 now show one consistent OTP-result handoff, but the new correlation rule does not establish the replay rejection claimed by the design and test, as re-anchored in Finding 1.
- Finding 2 — Resolved: Sections 5.2, 8, and 11 now make non-resumption a tested launch gate rather than asserting that per-session behavior survives a resumed session.
- Finding 3 — Partially resolved: Section 6.2 corrects the optional cardinalities, but its new Booking source-of-truth statement has no corresponding selection or linkage flow, as re-anchored in Finding 2.
- Finding 4 — Resolved: assumptions/open-decisions v3 preserves the corrected audit history and aligns OD-02's architecture disposition, UX owner, and reopening condition with Section 3.

### 1. OTP replay rejection has no enforcing state

- Severity: Blocking
- Lens: Proof
- Location: Section 3.2 launcher-to-Salesforce interface contract and Section 11 identity test
- Evidence: Section 3.2 says matching `otpResult.portalSessionId` to the payload means "a signed result cannot be replayed into a different portal session," and Section 11 requires "replayed and cross-session `otpResult`" values to be rejected.
- Design gap: Both `portalSessionId` values arrive together from the untrusted launcher, so equality proves that the signed result and payload carry the same identifier but does not show that the identifier belongs to the current Salesforce interaction or that the same valid signed pair has not already been used. The document defines signature, age, and equality checks, but no state or acceptance rule that makes same-pair reuse within the five-minute window fail.
- Consequence: A previously valid result can satisfy every documented check when replayed with its original `portalSessionId`, potentially causing the wrong interaction to inherit verified Contact, Booking, and Summit treatment while the stated replay test has no implementable expected result.
- Author's task: Establish the authoritative interaction binding and testable reuse rule that makes a previously accepted signed result fail on a later submission, including its owner, validity boundary, rejection behavior, and audit evidence.

### 2. The design never establishes which Booking is linked or looked up

- Severity: Blocking
- Lens: Flow
- Location: Section 3.2 Contract v1.0, Section 6.2 data relationships, Section 7.1 TravelPort sequence, and Section 9.2 identity verification
- Evidence: Section 6.2 says the Case-to-Booking association is "written once at verification," Section 9.2's pass outcome links only Contact and Case, and Section 7.1 begins with `Lookup(bookingRef)` even though Contract v1.0 carries no booking reference.
- Design gap: No view identifies where `bookingRef` originates, how one current Booking is selected when an email or Contact has zero or multiple bookings, or which verification/manual-verification event writes the Case association. The declared Booking source of truth therefore has no traceable input or state transition.
- Consequence: Builders must invent the Booking-selection rule and may link or expose the wrong travel record, while QA cannot determine which booking must appear to prove R-04.
- Author's task: Make the Booking identity, zero/one/multiple selection outcomes, verified and manual-verification linkage events, TravelPort input, and R-04 evidence traceable without relying on an inferred booking reference.

### 3. The pre-verification Contact match is an undocumented second interface

- Severity: High
- Lens: Failure
- Location: Section 3.1 system context, Section 3.2 launcher contract, and Section 9.2 verification sequence
- Evidence: Section 9.2 sends `L->>ES: Match check (email)` and receives `ES-->>L: Offer verification` before the later Contract v1.0 submission, while the system context shows only the Contract v1.0 launcher-to-Embedded-Service handoff and Section 3.2 defines only that final payload.
- Design gap: The match check is a separate pre-session Salesforce boundary with no defined interface, caller authentication or authorization posture, response-data limit, timeout/error behavior, monitoring signal, or version ownership. The untrusted email and match-cardinality response therefore bypass the contract and failure controls documented for the final submission.
- Consequence: Verification initiation can fail or disclose whether a customer record exists without a reviewable degraded path, and the launcher and Salesforce teams can implement incompatible assumptions about when a session or identity lookup begins.
- Author's task: Define and reconcile the pre-verification match boundary across the context, interface, failure, monitoring, and test views, including what the anonymous caller may learn and how every failure outcome proceeds.

## Open Decisions for the Senior Architect

- Whether OD-01 requires claims-licensed-agent eligibility at launch; that decision changes queue membership, no-eligible-target behavior, staffing proof, and the R-03 service objective.

## Deferred Review Areas

- Section 6.2 data relationships: the diagram still omits MessagingEndUser and its verified or unverified relationship to MessagingSession and Contact.
- Sections 5 and 5.3 lifecycle views: the process diagram lacks the customer-close branch and does not expose session states or distinguish customer-, agent-, and inactivity-ended evidence.
- Section 4.2 routing: agent presence eligibility, interaction with other-channel capacity, and concurrency evidence for the chosen capacity of three remain unstated.
- Section 7.1 TravelPort sequence: the retry branch does not draw the second named-credential-to-TravelPort request that the prose calls an automatic retry.
