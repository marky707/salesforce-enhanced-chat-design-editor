# Observed Sample Run — Northstar draft

This is an **actual, unedited review** produced by loading the five-part editor
(`identity.md`, `rules.md`, `examples.md`, `reference/`) as context and reviewing
`northstar-sdd-draft-v1.md`. It is real evidence of the editor's behavior, distinct
from `expected-review-round-01.md` (which is the maintained golden reference the
sample is checked against).

- **Model:** Claude Opus 4.8
- **Date:** 2026-07-20
- **Invocation:** *"You are the design review editor defined in identity.md. Obey rules.md completely. Review this solution design for formal-review readiness."* — with `northstar-sdd-draft-v1.md` and `northstar-requirements.md` attached.
- **Editing:** none. The output below is reproduced verbatim.

---

# Design Review

## Verdict
Revise Before Formal Review

Three blocking gaps — a deployment topology the document contradicts itself on, an unbounded direct-to-owner routing path, and a routing decision no builder could follow — prevent a responsible formal review of this migration design.

> This verdict measures document readiness, not architecture approval. Final design approval remains with the accountable human architect and governance reviewers.

## Priority Findings

### 1. Sections 4 and 9 contradict each other on deployment topology

- Severity: Blocking
- Lens: Flow
- Location: Section 4, "Proposed Architecture" vs. Section 9, "Deployment Plan"
- Evidence: Section 4: "A single Embedded Service deployment will serve both the website and the Northstar mobile app." Section 9's wave table: "Cut over the web deployment" (Week 1) and "Cut over the mobile deployment (app release)" (Week 3).
- Design gap: One deployment cannot be cut over as two independent channel-scoped deployments on different weeks. The architecture and the migration plan describe structurally different designs, and every deployment-scoped setting (pre-chat, branding, routing entry, business hours) is ambiguous until this is resolved.
- Consequence: The build team cannot determine how many deployments to configure, and the phased-cutover plan may be physically impossible as written — a single deployment has no "web half" to migrate in Week 1.
- Author's task: Decide the deployment topology, state the requirement that drives one-versus-two deployments, and reconcile every section that references a deployment.

### 2. Direct-to-owner routing (Section 5.2) has no availability, timeout, or fallback

- Severity: Blocking
- Lens: Failure
- Location: Section 5.2, "Returning Customer Routing"
- Evidence: "Returning customers with an open case will be routed directly to their case owner for continuity."
- Design gap: No behavior is defined when the case owner is offline, at capacity, out of office, or simply does not accept. No timeout bounds the wait and no fallback target exists, so a returning customer can wait indefinitely on one person — a wait that never enters a queue and is therefore invisible to Omni-Channel queue dashboards.
- Consequence: The design's most relationship-sensitive customers get its least reliable path, and operations cannot even see the failure to intervene.
- Author's task: When the case owner cannot accept within a bounded time, what is that bound, where does the work item route next, and how does that path stay visible to supervisors?

### 3. The Section 5.1 routing decision cannot be followed

- Severity: Blocking
- Lens: Flow
- Location: Section 5.1, "Routing Overview" (with Section 5.3)
- Evidence: "Chats will be routed based on language, product line, and customer priority to the appropriate queue." Section 5.3 adds only that "Pro-tier customers are high priority and should be answered first."
- Design gap: Three routing inputs are named with no evaluation order, no input-to-queue matrix, and no behavior for missing or conflicting inputs (e.g. a Spanish-preferring Pro-tier customer when the Pro Gear queue has no bilingual coverage). "Answered first" names a goal, not a priority mechanism.
- Consequence: The Omni-Channel Flow builder must invent the precedence rules, and every conflict case becomes an undocumented behavior discovered in production.
- Author's task: Provide the decision sequence a reviewer can walk — input order, the input-to-queue mapping, the priority mechanism, and the outcome for missing or conflicting inputs.

### 4. The Chat_Interaction__c custom object has no rationale against the native relationship

- Severity: High
- Lens: Why
- Location: Section 7, "Data Model"
- Evidence: "A custom object Chat_Interaction__c will link each MessagingSession to its Case and store interaction details."
- Design gap: MessagingSession already carries a native Case relationship; no requirement is cited that it cannot meet, and "interaction details" is not enumerated, so it is unclear what the custom object stores that standard fields do not.
- Consequence: The org inherits a permanent custom object, a second relationship that can disagree with the native lookup, and reporting that must choose between two sources of truth for the same link.
- Author's task: Which requirement can the native MessagingSession–Case relationship not satisfy, what exactly does the junction store, and what tradeoff makes it worth its maintenance cost?

### 5. Reporting names no source objects, and the migration breaks KPI continuity

- Severity: High
- Lens: Proof
- Location: Section 10, "Reporting and KPIs" (with Section 3 and requirement R-06)
- Evidence: "Dashboards will show average wait time, abandonment rate, and agent handle time. The existing weekly dashboard will be rebuilt on the new data." Section 3 notes the current dashboards are built on LiveChatTranscript.
- Design gap: No metric names its source object, fields, or the two lifecycle events that bound it. Wait time on MessagingSession and on AgentWork are different numbers; "abandonment" is undefined for sessions that end before routing. The design moves off LiveChatTranscript with no mapping to the new object model, so R-06's "continue without loss of the current KPIs" cannot be demonstrated.
- Consequence: Dashboards get built on whichever object the report builder reaches first, operations manages staffing against undefined numbers, and the migration cannot be proven to preserve the metrics leadership already watches.
- Author's task: For each KPI, name the source object, fields, and the two lifecycle events that bound it, and show how each maps to the LiveChatTranscript metric it replaces.

## Open Decisions for the Senior Architect

- Whether owner-continuity routing (Section 5.2) is worth its operational risk at Northstar's 14-agent staffing once a bounded fallback is defined — a business tradeoff, not a document-readiness gap. Note the requirement behind it (reaching "someone with their case context") is broader than the case owner specifically, so the architect may prefer a context-qualified pool over a single named owner.

## Deferred Review Areas

Deferred until the blocking findings are resolved:

- Proactive invitation expiration enforcement and its time authority (Section 6) — *likely next-round finding*
- Mobile wrapper payload contract, versioning, and ownership (Section 8) — *likely next-round finding*
- Chat available to all site visitors without login (Section 11) while Contact matching uses the unverified pre-chat email (Section 7) — an identity/data-exposure gap — *likely next-round finding*
- Absence of monitoring, retry, and rollback, including the fate of in-flight legacy chats when "Legacy Chat will be disabled at the start of Week 1" (Sections 9–11) — *build-entry validation*
- Testing defers all test design to the build phase with no requirement-to-test traceability (Section 12) — *valuable improvement*

---

## How this compares to the golden reference

The run independently reproduced all five priority findings in `expected-review-round-01.md` (deployment contradiction, direct-to-owner fallback, unfollowable routing, unjustified junction object, reporting/proof) at the same severities, and surfaced the same owner-continuity open decision. The one notable difference: this run pushed the login/identity gap (Section 11 vs. Section 7) into Deferred as a likely next-round finding, where the golden reference folds it into the security discussion — a reasonable prioritization difference within the five-finding budget, not a miss. No finding rewrote the design, generated a diagram, or produced replacement wording; every finding ends in a question handed back to the author.

**Reference currency note (added after the preserved output):** the reporting reference now also requires designs to consider `MessagingSessionMetrics` for completed-session response-time and message-count measures. The verbatim output above remains unchanged; the maintained golden reference reflects the current three-source reporting guidance.
