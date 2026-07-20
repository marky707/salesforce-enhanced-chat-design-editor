<!-- Expected editor output for fixtures/northstar round 1.
     Mirrors the sample review in 02_editor-review/examples.md — keep the two in sync.
     Used to validate editor behavior: verdict, ≤5 anchored findings, no rewriting. -->

# Design Review

## Verdict
Revise Before Formal Review

Three blocking gaps — an undefined direct-to-owner failure path, an unfollowable routing decision, and a deployment contradiction — prevent a formal reviewer from responsibly evaluating this design.

> This verdict measures document readiness, not architecture approval. Final design approval remains with the accountable human architect and governance reviewers.

## Priority Findings

### 1. Direct-to-owner routing has no availability, timeout, or fallback behavior

- Severity: Blocking
- Lens: Failure
- Location: Section 5.2, "Returning Customer Routing"
- Evidence: "Returning customers with an open case will be routed directly to their case owner for continuity."
- Design gap: No behavior is defined when the case owner is offline, at capacity, out of office, or declines the work. No timeout bounds the wait; no fallback target exists.
- Consequence: A returning customer's chat can wait unbounded on an unavailable agent — invisible to queue dashboards because it never entered a queue. With R-05 promising a 2-minute first response, this is the design's most operationally dangerous path.
- Author's task: When the case owner cannot accept within a bounded time, where does the work item route, what is the bound, and how does this path still satisfy R-05?

### 2. Language and priority routing cannot be followed as a decision sequence

- Severity: Blocking
- Lens: Flow
- Location: Section 5.1, "Routing Overview"
- Evidence: "Chats will be routed based on language, product line, and customer priority to the appropriate queue."
- Design gap: Three routing inputs are named but no artifact — prose or diagram — shows their evaluation order, the queue matrix they produce, or the outcome when inputs conflict (a Spanish-speaking Pro-tier customer for a queue with no bilingual coverage) or are missing. Section 5.3's "answered first" names no mechanism.
- Consequence: The Omni-Channel Flow builder must invent the precedence rules, and every conflict case becomes an undocumented behavior discovered in production.
- Author's task: Produce the decision sequence a reviewer can walk: input order, the input-to-queue mapping for all three queues, and the routing outcome for missing or conflicting inputs.

### 3. Sections 4 and 9 contradict each other on Embedded Service deployments

- Severity: Blocking
- Lens: Flow
- Location: Section 4, "Proposed Architecture" vs. Section 9, "Deployment Plan"
- Evidence: Section 4: "A single Embedded Service deployment will serve both the website and the Northstar mobile app." Section 9, deployment table: "Cut over the web deployment" (Week 1) / "Cut over the mobile deployment (app release)" (Week 3).
- Design gap: The architecture describes one deployment; the migration plan cuts over two independently. Both cannot be true, and every deployment-scoped setting (pre-chat, branding, routing entry) is ambiguous until resolved.
- Consequence: The build team cannot configure the org, and the wave plan may be operationally impossible as written — a single deployment cannot be partially migrated by channel.
- Author's task: Decide the deployment topology, state the requirement driving it, and reconcile every section that references deployments.

### 4. The custom Chat_Interaction__c object has no rationale against native relationships

- Severity: High
- Lens: Why
- Location: Section 7, "Data Model"
- Evidence: "A custom object Chat_Interaction__c will link each MessagingSession to its Case and store interaction details."
- Design gap: No requirement is cited — R-07 requires only that conversations create or attach to a Case — and the native path, MessagingSession's own Case relationship, is never weighed. "Interaction details" are not enumerated, so it is unclear what the custom object stores that standard fields do not.
- Consequence: The org inherits a permanent custom object, duplicate relationship data that can disagree with the native lookup, and reporting that must choose between two sources of truth.
- Author's task: Which requirement can the native relationship not satisfy, what exactly does the junction store, and what tradeoff makes the customization worth its maintenance cost?

### 5. Reporting metrics name no source objects or lifecycle boundaries

- Severity: High
- Lens: Proof
- Location: Section 10, "Reporting and KPIs"
- Evidence: "Dashboards will show average wait time, abandonment rate, and agent handle time."
- Design gap: No metric names its source object, fields or metric type, population, or bounding lifecycle events. MessagingSession, MessagingSessionMetrics, and AgentWork answer different questions; none is chosen. A response-time metric is not automatically queue wait, "abandonment" is undefined for sessions that end before routing, and R-06 demands continuity with Legacy Chat KPIs measured on LiveChatTranscript — no mapping exists.
- Consequence: Dashboards will be built on whichever object the report builder picks, operations will manage staffing against undefined numbers, and R-06's "without loss of the current KPIs" cannot be demonstrated.
- Author's task: For each KPI: source object, fields or metric type, population, lifecycle meaning, and how the definition maps to the LiveChatTranscript metric it replaces.

## Open Decisions for the Senior Architect

- Whether owner-continuity routing (Section 5.2, R-04) is worth its operational risk against the R-05 response-time SLA at current staffing — a business tradeoff beyond document readiness. Note R-04 requires reaching "someone with their case context," which is broader than the case owner specifically.

## Deferred Review Areas

Deferred until the blocking findings are resolved:

- Proactive invitation expiration enforcement and its time authority (Section 6) — *likely next-round finding*
- Mobile wrapper versioning, payload contract, and ownership (Section 8) — *likely next-round finding*
- Absence of monitoring, retry, and rollback definitions, including the undefined fate of in-flight legacy chats when "Legacy Chat will be disabled at the start of Week 1" (Sections 9–12) — *build-entry validation*
- Testing depth: Section 12 defers test design to the build phase — *valuable improvement*
