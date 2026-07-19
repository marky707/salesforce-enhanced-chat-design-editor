# Design Review

## Verdict
Revise Before Formal Review

One blocking sequence gap and four high-severity gaps still leave VIP routing, returning-Case selection, retry-aware reporting, transcript controls, and cross-system flows insufficiently reviewable.

> This verdict measures document readiness, not architecture approval. Final design approval remains with the accountable human architect and governance reviewers.

## Priority Findings

Round 2 resolution check:

- Finding 1 — Resolved: requirements v2 records the R-03 owner's approved 95% objective, and Sections 4.3, 8, and 11 use the same threshold and breach behavior.
- Finding 2 — Partially resolved: Section 6.1 defines Case-flow failure recovery and Section 5.1 defines new-session behavior, but ambiguous recent-Case selection reappears as Finding 2 below.
- Finding 3 — Resolved: Section 9.1 now prohibits Contact association before verification and defines linkage method, correction, and audit history.
- Finding 4 — Partially resolved: the KPI table adds fields, owners, and multi-AgentWork intent, but its wait-time formula fails on the documented re-push path and reappears as Finding 3 below.
- Finding 5 — Resolved: Sections 10.1–10.3 now define phased exposure, gate owners, rollback, degraded behavior, health thresholds, and alert paths.

### 1. OTP verification is not sequenced before or after VIP routing

- Severity: Blocking
- Lens: Flow
- Location: Sections 4.1 and 4.3, "Routing Design," and Section 9.1, "Identity verification"
- Evidence: Section 4.1 assigns Summit priority only for a "verified Contact," while Section 9.1 says, "On success, the flow links Contact and Case, stamps `Verified_Via__c = OTP`, and grants Summit priority for the remainder of the session if applicable."
- Design gap: The document never states whether OTP occurs before session creation and work-item routing or after the chat has already entered a queue. It also does not define what happens to the routing target, priority, or `VIP_Routed_At__c` clock when verification succeeds after initial routing.
- Consequence: Two builders can implement opposite sequences; a genuine Summit traveler may enter at priority 5, start the 60-second clock late or not at all, and disappear from R-03 attainment despite successful verification.
- Author's task: Make the customer-verification, session-creation, Case-linking, work-item-creation, priority-assignment, and R-03 timer sequence unambiguous, including late success, timeout, failure, and any re-prioritization behavior.

### 2. The seven-day returning-Case rule has no outcome for multiple eligible Cases

- Severity: High
- Lens: Flow
- Location: Section 5.1, "New versus returning conversations"
- Evidence: "For a verified traveler (9.1) with a Case updated in the last 7 days, the Case-linking flow attaches the new session to that open Case rather than creating another."
- Design gap: The rule assumes one qualifying Case. It defines no selection input, precedence, or agent decision when the verified traveler has multiple open Cases updated within seven days, potentially across Booking Change and Claim topics.
- Consequence: The flow must guess which Case receives the session, causing incorrect case history, topic ownership, follow-up classification, and R-05 audit results.
- Author's task: Resolve the zero-, one-, and multiple-eligible-Case outcomes and the evidence used to select or defer association without silently attaching the session to the wrong work record.

### 3. Average wait time cannot be calculated when the first push times out

- Severity: High
- Lens: Proof
- Location: Section 4.2, "Agent availability, capacity, and push timeout," and Section 8 KPI table, "Average wait time"
- Evidence: Section 4.2 states that an unaccepted push "times out and is pushed to the next available queue member." The KPI uses, "First AgentWork per session: `AcceptDateTime − RequestDateTime`. Subsequent AgentWork (transfers, re-pushes) excluded from wait."
- Design gap: On the documented timeout path, the first AgentWork has no acceptance event, while the accepted timestamp belongs to a later AgentWork that the metric excludes. The formula therefore cannot produce the end-to-end wait for precisely the delayed sessions it needs to measure.
- Consequence: Re-pushed sessions can be omitted, null, or systematically understated, distorting both staffing decisions and the comparison between ordinary and VIP wait performance.
- Author's task: Define a reproducible wait boundary across multiple routing attempts and specify how timed-out, declined, transferred, abandoned, and ultimately accepted sessions enter or leave the calculation.

### 4. Transcript access, payment-data handling, and retention remain unowned

- Severity: High
- Lens: Failure
- Location: Section 9, "Security"
- Evidence: "Transcripts are visible to the service team. Payment card numbers must never be requested in chat; agents are trained to direct payment to the secure portal flow. (Automated masking is deferred — see round-01 response log.)"
- Design gap: "Service team" names no permission boundary, and the design defines no transcript/ConversationEntry retention rule or policy owner. Agent training prevents requests but does not address customers voluntarily pasting payment or other sensitive data; the explicitly deferred masking decision has no accountable acceptance, compensating control, or incident response.
- Consequence: Sensitive transcript data can be retained or exposed more broadly than intended without a reviewable access model, deletion obligation, detection path, or response owner.
- Author's task: Obtain the accountable security/data-owner decisions for transcript access, retention, unsolicited sensitive data, masking or compensating controls, and incident handling, then make those controls and owners testable in the design.

### 5. External-system and trust-boundary flows are still prose-only

- Severity: High
- Lens: Flow
- Location: Sections 3, 7, 9.1, and 10, covering the custom LWC, TravelPort, portal OTP and feature-flag services, Salesforce, and Slack alerts
- Evidence: Section 3 introduces "a custom LWC chat launcher"; Section 7 introduces the TravelPort API; Section 9.1 introduces the portal OTP service; and Section 10 uses the portal feature-flag service and Slack alert channels. No system-context or integration-sequence diagram is supplied.
- Design gap: The design now crosses several system and trust boundaries, but no artifact shows call direction, authentication handoffs, context payload ownership, ordered acknowledgements, or which component owns each failure between the portal, Salesforce, OTP, TravelPort, feature flag, and Slack.
- Consequence: Formal reviewers cannot assess the complete attack surface or verify that initialization, identity, routing context, retries, and alert failures have one consistent owner across the prose sections.
- Author's task: Supply the system-context and integration-sequence views needed to make the cross-system boundaries, ordered handoffs, ownership, and exception paths reviewable without changing the design through inference.

## Open Decisions for the Senior Architect

- Whether OD-01 requires claims-licensed-agent eligibility at launch; selecting that constraint changes queue membership, no-eligible-target behavior, staffing proof, and the R-03 service objective.
- Whether training-only prevention is an acceptable interim control for unsolicited payment data, and which security/data owner accepts the residual risk if automated masking remains deferred.

## Deferred Review Areas

Deferred until the priority findings are corrected: verifying the unsupported claim that ended Enhanced Chat sessions will never resume in this configuration; custom-launcher payload validation and version-compatibility ownership; the integration-log object's fields and retention; whether OD-02's launcher placement affects technical behavior; and detailed test coverage for OTP delivery timeout, feature-flag failure, Slack alert failure, and rollback during active routing.
