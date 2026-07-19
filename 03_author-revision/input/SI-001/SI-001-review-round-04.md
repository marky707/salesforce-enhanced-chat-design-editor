# Design Review

## Verdict
Revise Before Formal Review

Four high-severity gaps remain in lifecycle proof, TravelPort sequencing, custom-launcher interface ownership, and the data-relationship view required for consistent implementation and formal review.

> This verdict measures document readiness, not architecture approval. Final design approval remains with the accountable human architect and governance reviewers.

## Priority Findings

Round 3 resolution check:

- Finding 1 — Resolved: Sections 4.1, 4.3, and 9.2 now sequence OTP before work-item creation and define every verification outcome, fixed priority, timer start, and mid-chat verification behavior.
- Finding 2 — Resolved: Section 5.1 now defines zero, one, multiple, topic-mismatch, and unverified Case-selection outcomes without guessing.
- Finding 3 — Resolved: Section 8 now measures session wait to the accepting AgentWork and separately reports never-accepted sessions, including R-03 breaches.
- Finding 4 — Resolved: Section 9.1 now names transcript access, retention, redaction, incident, policy, review, and residual-risk owners.
- Finding 5 — Partially resolved: the system-context and OTP/routing sequence views establish major trust boundaries, but the external TravelPort sequence and data-relationship views remain incomplete below.

### 1. The non-resuming session behavior remains an unsupported lifecycle claim

- Severity: High
- Lens: Proof
- Location: Section 5.1, "New versus returning conversations and Case selection," and Section 11, "Testing"
- Evidence: "Every portal chat starts a new MessagingSession; ended sessions are not resumed."
- Design gap: The document does not identify the platform setting, launcher behavior, or other enforcing mechanism that guarantees ended sessions cannot resume, and the test table contains no reopen/return scenario that proves the claim. Because Enhanced Chat lifecycle behavior can be asynchronous, this must remain an unsupported claim until the configured behavior is cited or tested.
- Consequence: If the deployed lifecycle resumes a prior session, the seven-day Case-selection flow, `Follow_Up__c`, one-Case expectation, wait-time boundaries, and transcript history can all behave differently from the approved design.
- Author's task: Establish the configured mechanism and acceptance evidence for new-versus-resumed sessions, including what the customer, Case-linking flow, and reporting layer do when a traveler returns after each end condition.

### 2. The TravelPort integration still lacks the required ordered sequence

- Severity: High
- Lens: Flow
- Location: Section 3.1 system-context diagram and Section 7, "Integration Design"
- Evidence: The context diagram reduces the integration to `AG -->|"booking lookup (server-side, named credential)"| TP`, while Section 7 defines a five-second timeout, automatic retry, error banner, manual portal fallback, and integration logging.
- Design gap: The system-context arrow shows direction but not the ordered Salesforce-side invocation, acknowledgement, timeout, retry, agent response, fallback, or log handoffs. No integration-sequence view identifies which component owns each step and failure return.
- Consequence: The console, server-side integration, logging, and fallback can be implemented with inconsistent retry timing or ownership, and formal security/operations reviewers cannot verify the complete external-call path.
- Author's task: Provide the TravelPort integration sequence needed to make call order, trust boundary, acknowledgement, timeout, retry, agent fallback, logging, and ownership reviewable against Section 7.

### 3. The custom launcher has no payload or release-compatibility contract

- Severity: High
- Lens: Failure
- Location: Section 3, "Proposed Architecture," Section 3.1 system context, and Section 9.2 verification sequence
- Evidence: The custom LWC sends `"pre-chat + session start (HTTPS)"` to Embedded Service and receives a signed OTP result, but the document defines no field-level interface or version ownership.
- Design gap: The design does not state the pre-chat/hidden-field payload contract, which side validates email, topic, verification status, and signed OTP data, what malformed or stale values do, or how portal-LWC and Salesforce deployment changes are versioned and compatibility-tested.
- Consequence: A portal or Salesforce release can silently drop or misinterpret routing and identity context, sending travelers to the wrong queue or treating unverified data as trusted despite the documented happy-path sequence.
- Author's task: Define ownership and proof for the launcher-to-Salesforce contract, validation and rejection behavior, signed-result handling, version compatibility, and the failure signals that catch a breaking release before customers do.

### 4. The design has no reviewable data-relationship model

- Severity: High
- Lens: Flow
- Location: Sections 5.1, 6, 8, and 9.1
- Evidence: The design relies on MessagingSession, multiple AgentWork records, Case, Contact, Booking__c, an integration log object, `Follow_Up__c`, `Verified_Via__c`, and `VIP_*` fields, but the only context node combines "MessagingSession / Case."
- Design gap: No data-relationship view shows cardinality, lookup direction, source of truth, or where the custom fields live across session creation, Case reuse, verification, multiple routing attempts, TravelPort logging, and reporting.
- Consequence: Builders and report authors can implement different relationships or duplicate sources of truth, undermining the deterministic Case selection, identity audit, and KPI definitions that v4 otherwise clarifies.
- Author's task: Supply the data-relationship view needed to make native and custom objects, cardinalities, linkage events, field ownership, and reporting sources reviewable without inference.

## Open Decisions for the Senior Architect

- Whether OD-01 requires claims-licensed-agent eligibility at launch; selecting that constraint changes queue membership, no-eligible-target behavior, staffing proof, and the R-03 service objective.

## Deferred Review Areas

Deferred until the priority findings are corrected: the end-to-end customer/agent process view through wrap-up and transfer; detailed integration-log fields and retention; whether OD-02's launcher placement changes technical behavior; proof that supervisor redaction is supported for the retained transcript data; and tests for feature-flag failure, Slack alert failure, purge-job failure, and rollback while routing work is active.
