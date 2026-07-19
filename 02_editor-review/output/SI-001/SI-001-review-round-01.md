# Design Review

## Verdict
Revise Before Formal Review

Five blocking gaps leave the routing, customer identity, external integration, conversation lifecycle, and requirement validation too ambiguous for formal architecture review.

> This verdict measures document readiness, not architecture approval. Final design approval remains with the accountable human architect and governance reviewers.

## Priority Findings

### 1. The routing decision flow and its failure branches are absent

- Severity: Blocking
- Lens: Flow
- Location: Section 3, "Proposed Architecture," and Section 4, "Routing Design"
- Evidence: "The overall routing design is shown in the routing diagram in Appendix A." No Appendix A or routing diagram is present; the prose states only, "VIP travelers (Summit tier) will be handled with urgency."
- Design gap: The document names topic, skills, team, general-queue, VIP, availability, and capacity concepts but does not show their evaluation order, eligibility rules, capacity model, or outcomes for missing inputs, no eligible agent, push timeout, overflow, or closed support hours. The relationship between skills-based routing and the "general queue" is also undefined.
- Consequence: Builders must invent the routing logic and failure behavior, while reviewers cannot determine whether the design can meet R-03's 60-second VIP target or R-06's 6am–8pm MT availability rule.
- Author's task: Provide a routing decision flow that makes the input precedence, target-selection rules, capacity and availability behavior, and every timeout, fallback, and after-hours outcome reviewable against R-03 and R-06.

### 2. Unverified email is treated as sufficient customer identity

- Severity: Blocking
- Lens: Failure
- Location: Section 6, "Data Model," and Section 9, "Security"
- Evidence: "Contact matching uses the pre-chat email." Section 9 states, "Chat is available to any portal visitor without login."
- Design gap: The design does not state what identity claim is trusted, how typed email is verified, how ambiguous or missing Contact matches behave, or what authorizes linking the conversation to a booking and exposing live booking details. A-04 makes Summit status dependent on the matched Contact, but the trust boundary is unresolved.
- Consequence: A mistyped or deliberately supplied email could associate a Case and chat with the wrong Contact or Booking__c, misclassify VIP priority, and expose another traveler's booking information to an unverified visitor.
- Author's task: Resolve the identity and authorization model for anonymous visitors, including match ambiguity and failure behavior, before Contact, Summit-tier, Booking__c, or TravelPort context is trusted.

### 3. The synchronous TravelPort boundary has no failure design

- Severity: Blocking
- Lens: Failure
- Location: Section 7, "Integration Design," and assumption A-03
- Evidence: "The lookup calls the TravelPort API synchronously and displays results in the console." A-03 assumes that "The TravelPort API contract in place for the agent console can be reused for chat-time lookups."
- Design gap: The synchronous choice has no requirement-based rationale or documented contract, timeout, retry ownership, error visibility, degraded agent experience, logging, or recovery path. The reusable-contract claim remains an assumption with no validation method.
- Consequence: TravelPort latency or failure can block the agent's handling path without a defined customer experience, operational owner, or evidence that R-04 was met.
- Author's task: Validate the reuse assumption and define the integration decision, ownership, bounded failure behavior, recovery, and proof needed to show current booking details are safely available during chat.

### 4. Conversation and Case lifecycle behavior is undefined and untestable

- Severity: Blocking
- Lens: Failure
- Location: Section 5, "Conversation Lifecycle," and Section 6, "Data Model"
- Evidence: "Sessions close automatically when inactive. Travelers can start a new chat at any time from the portal." Section 6 adds, "Each chat creates a Case."
- Design gap: No inactivity value, enforcing mechanism, time authority, state transitions, end ownership, resume/reopen behavior, or distinction between a returning conversation and a new chat is defined. The event that creates a Case and the behavior on creation or linking failure are also absent.
- Consequence: The build can create duplicate Cases, end sessions while work is still active, or treat resumed conversations inconsistently; reporting cannot distinguish customer-ended, agent-ended, inactive, reopened, or newly created work.
- Author's task: Define the conversation, session, and Case lifecycle as testable state transitions, including the events and owners for creation, inactivity, end, return, failure, and any new-versus-resumed decision.

### 5. The reporting and test plan cannot prove the stated requirements

- Severity: Blocking
- Lens: Proof
- Location: Section 8, "Reporting," Section 11, "Testing," and requirements R-02, R-03, and R-07
- Evidence: "Leadership dashboards will show CSAT, average response time, and chats per agent, refreshed daily." Section 11 states, "QA will test all scenarios before launch."
- Design gap: The KPIs name no source objects, fields, lifecycle boundaries, baseline, or acceptance criteria. The listed dashboard does not define proof for the 30% phone-volume reduction in R-02, the 60-second Summit-tier target in R-03, or weekly adoption and quality in R-07. "All scenarios" has no requirement traceability or expected results.
- Consequence: QA, operations, and leadership can calculate different numbers from MessagingSession and AgentWork and still have no objective way to determine whether launch requirements passed or production is healthy.
- Author's task: Establish requirement-to-test and requirement-to-metric traceability, with a named evidence source, lifecycle boundary, acceptance criterion, cadence, and operational owner for each material requirement.

## Open Decisions for the Senior Architect

- OD-01 requires accountable human judgment on whether Claims routing must enforce a claims-licensed skill; that decision changes agent eligibility, staffing sufficiency, fallback behavior, and the routing proof needed for formal review.

## Deferred Review Areas

Deferred until the five blocking findings are resolved: the requirement and tradeoff for replacing the standard launcher with a custom LWC, including initialization and context-passing ownership; masking enforcement, transcript permissions, data retention, and security ownership; deployment phasing, rollback, and active-session handling; production monitoring signals, thresholds, alerting, and owners; and whether OD-02's launcher placement affects architecture or remains a UX decision.
