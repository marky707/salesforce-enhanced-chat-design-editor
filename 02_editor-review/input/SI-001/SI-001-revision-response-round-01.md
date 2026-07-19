# Revision Response Log — SI-001 — Round 01

- **Review ID:** SI-001
- **Responding to:** `SI-001-review-round-01.md`
- **Revised document version:** v2 (`solstice-sdd-draft-v2.md`)
- **Author (human actor):** P. Okafor
- **Date (ISO 8601):** 2026-07-18

---

## Finding 1: The routing decision flow and its failure branches are absent

- **Disposition:** resolved
- **Where the design changed:** Section 4 rewritten; new Sections 4.1 (decision sequence table), 4.2 (capacity and push timeout), 4.3 (VIP enforcement and fallback), 4.4 (queue overflow); Section 3 updated to remove the Appendix A reference.
- **What changed / rationale:** Routing is now explicitly queue-based, with the skills alternative documented and rejected for launch (small agent pool, A-02). The decision table defines input order, queue mapping, priority, missing-input default, push timeout (30s), VIP 60-second fallback with supervisor alert and callback offer (R-03), after-hours behavior (R-06), and overflow behavior. The contradictory "general queue" statement from v1 is withdrawn.

## Finding 2: Unverified email is treated as sufficient customer identity

- **Disposition:** resolved
- **Where the design changed:** New Section 9.1; Section 6 updated to gate the Booking__c link on verification.
- **What changed / rationale:** Pre-chat email is now explicitly an unverified claim. Booking data, TravelPort lookups, and Summit priority all require OTP confirmation against the booking email via the existing portal OTP service. No-match and multi-match cases never auto-link. Unverified chats continue as general conversations.

## Finding 3: The synchronous TravelPort boundary has no failure design

- **Disposition:** resolved
- **Where the design changed:** Section 7 rewritten.
- **What changed / rationale:** Synchronous choice now has a rationale with the async alternative weighed. Defined: 5-second timeout, one retry, agent error banner with manual fallback to the existing TravelPort portal, integration log object with a named weekly reviewer. A-03 validation is scheduled as a build-week-1 contract test with a defined fallback path if it fails.

## Finding 4: Conversation and Case lifecycle behavior is undefined and untestable

- **Disposition:** partially resolved
- **Where the design changed:** Section 5 rewritten; Section 6 updated.
- **What changed / rationale:** The three end conditions are now defined with owners, inactivity closure is set to 30 minutes enforced by the deployment's session inactivity setting, and Case creation is pinned to session start via a record-triggered flow. Not yet addressed: behavior when Case creation fails, and how a returning traveler's conversation is distinguished from a new chat. These need input from the platform team and will be resolved in the next revision.

## Finding 5: The reporting and test plan cannot prove the stated requirements

- **Disposition:** partially resolved / disagree in part
- **Where the design changed:** Section 8 rewritten with per-metric source object and lifecycle boundaries, including a new R-03 attainment metric; Section 11 rewritten as a requirement-to-test table with acceptance criteria.
- **What changed / rationale:** Wait time, handle time, chats per agent, CSAT, and VIP attainment now each name a source and boundary. **Disagreement on R-02:** the 30% phone-volume reduction is a business-program outcome measured in the existing phone reporting system over six months; it cannot be proven by chat-side objects and does not belong in this SDD's proof section. We propose R-02 be tracked by the support operations scorecard, with this design's contribution limited to the chat adoption metrics in R-07. If the reviewer disagrees, we request guidance on what chat-side evidence would be acceptable.

---

## New material introduced this round

- Section 4.1 routing decision table; Sections 4.2–4.4
- Section 9.1 identity verification model (OTP via existing portal service)
- Section 11 requirement-to-test traceability table
- Withdrawal of the v1 Appendix A diagram reference (replaced by the Section 4.1 table)
