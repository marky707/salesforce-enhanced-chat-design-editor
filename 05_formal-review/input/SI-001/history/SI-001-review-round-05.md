# Design Review

## Verdict
Revise Before Formal Review

The identity trust boundary is internally contradictory, and the lifecycle contingency and data cardinalities remain materially ambiguous despite the new review views.

> This verdict measures document readiness, not architecture approval. Final design approval remains with the accountable human architect and governance reviewers.

## Priority Findings

Round 4 resolution check:

- Finding 1 — Partially resolved: Section 5.2 now identifies an enforcement mechanism and acceptance test, but its failed-test contingency does not preserve the claimed session behavior or reporting boundaries, as re-anchored in Finding 2.
- Finding 2 — Resolved: Sections 7.1 and 7.2 now make the TravelPort call order, timeout, retry, failure return, fallback, logging, and ownership reviewable.
- Finding 3 — Partially resolved: Section 3.2 defines the launcher contract and release controls, but its OTP-result path contradicts the system and verification views, as re-anchored in Finding 1.
- Finding 4 — Partially resolved: Section 6.2 supplies the missing relationship view, but three of its cardinalities contradict the surrounding design, as re-anchored in Finding 3.

### 1. The OTP result has two incompatible trust-boundary paths

- Severity: Blocking
- Lens: Flow
- Location: Section 3.1 system-context diagram, Section 3.2 launcher-to-Salesforce interface contract, and Section 9.2 identity verification
- Evidence: The context diagram shows `OTP -->|"signed verification result"| ES`, while Section 3.2 says, "The launcher submits pre-chat as Contract v1.0" with `otpResult`, and Section 9.2 says the outcome enters Salesforce "only as the signed `otpResult` contract field."
- Design gap: The diagrams and prose assign different senders and handoffs to the same trusted result: a direct OTP-service-to-Embedded-Service response versus an OTP-service-to-launcher result carried inside the launcher's contract. The document therefore does not establish the actual interface on which signature validation, staleness, correlation, and ownership depend.
- Consequence: Builders and security reviewers could implement or assess different trust boundaries, allowing verification state to be lost, mis-correlated, or accepted through a path whose authentication and failure behavior were never reviewed.
- Author's task: Reconcile every identity and context view around one authoritative OTP-result handoff, including the responsible sender, receiving interface, correlation boundary, and applicable contract-validation behavior.

### 2. The failed non-resumption test has no coherent operating model

- Severity: High
- Lens: Failure
- Location: Section 5.2, "Session non-resumption: enforcement and proof," Section 8 reporting table, and Section 11 lifecycle test
- Evidence: The contingency says that if the platform resumes a session, "`Follow_Up__c` and all Section 8 KPIs are defined per MessagingSession record and remain valid," while the lifecycle acceptance criterion only requires "contingency path documented if not."
- Design gap: The failed test condition is reuse of the prior `MessagingSession.Id`, yet the contingency assumes the same per-MessagingSession boundaries remain valid without defining a new session-start event, Case-selection execution, verification/routing cycle, or KPI start and end boundaries. Documentation alone is also the stated acceptance criterion for this alternate behavior.
- Consequence: A resumed interaction could inherit the prior Case, verification state, wait clock, routing attempts, and reporting interval, producing behavior and KPI results that do not represent the returning traveler's interaction.
- Author's task: Establish and test the lifecycle, Case-linking, verification, routing, and measurement boundaries that apply if any return path keeps the prior MessagingSession, and demonstrate why the resulting evidence still proves the requirements.

### 3. The ER cardinalities contradict optional and unverified relationships

- Severity: High
- Lens: Flow
- Location: Section 5.1 Case-selection rules, Section 6.2 data-relationship diagram, Section 7.2 integration-log definition, and Section 9.2 identity verification
- Evidence: The ER diagram declares `Contact ||--o{ Case`, `Case }o--|| Booking__c`, and `MessagingSession ||--o{ Integration_Log__c`, while the design also says an unverified traveler always receives a new Case, Booking linkage applies to verified sessions, and the integration log has an "optional `MessagingSession` lookup."
- Design gap: Those Mermaid cardinalities require every Case to have one Contact, every Case to have one Booking, and every Integration Log row to have one MessagingSession, contrary to the prose's unverified and optional branches. Labels such as "verified linkage only" and "optional lookup" do not change the encoded cardinalities.
- Consequence: Data builders, flow authors, and report designers can implement mandatory relationships where valid records must be unlinked, causing failed record creation, fabricated associations, or incomplete operational logs.
- Author's task: Reconcile the encoded cardinalities and relationship ownership with every verified, unverified, integration, and Case-reuse path described in the design.

### 4. OD-02 is simultaneously closed and open across the submitted package

- Severity: Medium
- Lens: Flow
- Location: Section 3, "Proposed Architecture," and `solstice-assumptions-open-decisions.md`, "Open decisions"
- Evidence: Section 3 says, "OD-02 is closed for architecture purposes," while the supporting artifact still lists "OD-02: Chat launcher placement on the portal (floating vs. header)."
- Design gap: The design and its submitted decision register report different governance states for OD-02, with no dated disposition or distinction between a closed architecture impact and a remaining UX decision.
- Consequence: Formal reviewers cannot tell whether a human decision is still pending or whether launcher placement can change without reopening interface, accessibility, or release considerations.
- Author's task: Reconcile OD-02's status across the package and make any remaining decision owner, scope, and design impact unambiguous.

## Open Decisions for the Senior Architect

- Whether OD-01 requires claims-licensed-agent eligibility at launch; that decision changes queue membership, no-eligible-target behavior, staffing proof, and the R-03 service objective.

## Deferred Review Areas

Deferred until the priority contradictions are corrected: build-week evidence for the launcher contract and session lifecycle; the exact Booking-to-Case relationship and source of truth after cardinalities are reconciled; and lower-priority consistency checks across the new end-to-end, TravelPort, rollback, redaction, and operations tests.
