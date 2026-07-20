# Revision Response Log — UX-015 — Round 01

- **Review ID:** UX-015
- **Responding to:** `UX-015-review-round-01.md`
- **Revised document version:** v2 (`northstar-sdd-draft-v2.md`)
- **Author (human actor):** J. Rivera, Associate Consultant (fictional demo persona)
- **Date (ISO 8601):** 2026-07-19

---

## Finding 1: Direct-to-owner routing has no availability, timeout, or fallback behavior

- **Disposition (mark one):** [x] resolved  [ ] partially resolved  [ ] disagree
- **Where the design changed:** SDD v2 Sections 5.2, 6.5, 6.6, 11.2, and 14
- **What changed / why (your own words):** I changed direct-to-owner routing into a preference, not a hard destination. The owner gets 30 seconds only when eligible, present, and under capacity; then the conversation moves through the normal pool, expands at 75 seconds, and alerts at 90 seconds so an agent still has 30 seconds to respond inside R-05.

---

## Finding 2: Language, product, and priority routing cannot be followed as a decision sequence

- **Disposition (mark one):** [x] resolved  [ ] partially resolved  [ ] disagree
- **Where the design changed:** SDD v2 Sections 6.1–6.7 and the routing tests in Section 14
- **What changed / why (your own words):** I wrote the evaluation order, normalization rules, target matrix, priority values, fallback timers, no-capacity behavior, and after-hours path. I also compared both OD-01 candidates and made sure neither option can silently drop the Spanish requirement or skip the same timeout and escalation rules.

---

## Finding 3: The architecture and migration plan contradict each other on deployment topology

- **Disposition (mark one):** [x] resolved  [ ] partially resolved  [ ] disagree
- **Where the design changed:** SDD v2 Sections 1, 2.3, 4, and 10
- **What changed / why (your own words):** I selected two deployments because web and mobile have different identity, release, feature-flag, branding, and rollback needs. Both use one governed routing flow, and the diagrams, release waves, configuration ownership, health checks, and rollback steps now use the same topology.

---

## Finding 4: The custom Chat_Interaction__c object has no requirement or tradeoff rationale

- **Disposition (mark one):** [x] resolved  [ ] partially resolved  [ ] disagree
- **Where the design changed:** SDD v2 Sections 1, 2.3, 5.2, 8, and the R-07 test in Section 14
- **What changed / why (your own words):** I removed `Chat_Interaction__c` because R-07 can use the native MessagingSession-to-Case relationship. The revised model makes that relationship the one source of truth and uses controlled fields on MessagingSession only where a normalized reporting value is needed.

---

## Finding 5: Reporting metrics have no source objects or lifecycle boundaries

- **Disposition (mark one):** [x] resolved  [ ] partially resolved  [ ] disagree
- **Where the design changed:** SDD v2 Sections 7, 8.2, 11, and the R-05/R-06 tests in Section 14
- **What changed / why (your own words):** I defined the source records and start/end events for wait, abandonment, handle time, first response, and R-05 compliance. The rules now say how reroutes, multiple AgentWork records, never-accepted sessions, after-hours traffic, proactive invitation expiry, and missing timestamps are counted, plus how the new measures are reconciled to Legacy Chat.

---

## New material introduced this round

- `northstar-sdd-draft-v2.md` — revised architecture with system-context, end-to-end, routing, lifecycle, data, integration, migration, rollback, security, KPI, and verification detail; Mermaid diagrams are embedded in the SDD.
- `northstar-assumptions-open-decisions-v2.md` — new version because the assumptions now include validation/ownership constraints and the decision register includes recommendations, alternatives, and consequences.
- Deferred review areas addressed proactively: lifecycle clocks and recovery; mobile and OrderService validation/timeouts/ownership; in-flight cutover and rollback signals; requirement-to-test traceability; identity collision, access, retention, and sensitive-data behavior; six architecture views represented through tables and Mermaid diagrams.
- `northstar-requirements.md` was re-read against SDD v2 and did not change, so it was not versioned or included in the revision submission.
