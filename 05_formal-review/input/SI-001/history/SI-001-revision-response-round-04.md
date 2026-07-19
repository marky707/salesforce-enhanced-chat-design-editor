# Revision Response Log — SI-001 — Round 04

- **Review ID:** SI-001
- **Responding to:** `SI-001-review-round-04.md`
- **Revised document version:** v5 (`solstice-sdd-draft-v5.md`)
- **Author (human actor):** P. Okafor
- **Date (ISO 8601):** 2026-07-18

---

## Finding 1: The non-resuming session behavior remains an unsupported lifecycle claim

- **Disposition (mark one):** [x] resolved
- **Where the design changed:** New Section 5.2; Section 11 lifecycle test row
- **What changed / why (your own words):** Fair — I was asserting platform behavior I hadn't proven. It's now stated as configured behavior with a mechanism (launcher never persists a conversation token; deployment end/inactivity settings), a build-week-1 test for every end condition asserting a new session Id, and a written contingency: if the platform does resume sessions somewhere, Case-based continuity and the per-session KPI definitions still hold, and that path gets documented and re-reviewed before UAT.

## Finding 2: The TravelPort integration still lacks the required ordered sequence

- **Disposition (mark one):** [x] resolved
- **Where the design changed:** New Section 7.1 (sequence diagram); Section 7.2 (integration log definition)
- **What changed / why (your own words):** Added the full ordered sequence — console to Apex service to named credential to TravelPort — with the timeout, single retry, both failure returns, the agent's manual fallback, async logging, and the owning team annotated on every participant. Also defined the integration log object itself since it kept being referenced without fields.

## Finding 3: The custom launcher has no payload or release-compatibility contract

- **Disposition (mark one):** [x] resolved
- **Where the design changed:** New Section 3.2; Section 4.1 step 4; Section 10.3 (contract-reject signal)
- **What changed / why (your own words):** Defined Contract v1.0 field by field: Salesforce validates everything server-side (schema, enums, OTP signature, staleness) and trusts nothing from the client. Bad payloads route unverified to Bookings and log a contract_reject — never drop the chat. Release safety is a joint checklist plus a CI contract test that must pass before either the portal or the deployment ships a change, and the contract-reject rate is a health signal so a breaking release announces itself.

## Finding 4: The design has no reviewable data-relationship model

- **Disposition (mark one):** [x] resolved
- **Where the design changed:** New Section 6.2 (ER diagram with sources of truth)
- **What changed / why (your own words):** Added the entity diagram: Contact to Case to MessagingSession to AgentWork with cardinalities, the Booking__c lookup, where every custom field lives, and who writes what — flows write, reports read, AgentWork stays stock. Also stated explicitly that the session-to-Case lookup is the only relationship and no junction object exists.

---

## New material introduced this round

- Sections 3.2, 5.2, 5.3 (end-to-end process view), 6.2, 7.1, 7.2
- Deferred-list closures, addressed proactively this round: end-to-end customer/agent process view through wrap-up and transfer (5.3); integration-log fields and retention (7.2); OD-02 closed as UX-only (Section 3); redaction mechanism verification with fallback (9.1); tests for feature-flag failure, Slack alert failure, purge-job failure, and rollback during active routing (10.2, 10.3, Section 11)
