# Design Review

## Verdict
Revise Before Formal Review

Two blocking gaps and three high-severity gaps still prevent the document from establishing a coherent service target, failure-complete lifecycle, trusted identity linkage, defensible metrics, and controlled go-live.

> This verdict measures document readiness, not architecture approval. Final design approval remains with the accountable human architect and governance reviewers.

## Priority Findings

Round 1 resolution check:

- Finding 1 — Resolved: Sections 4.1–4.4 now define the queue model, decision order, capacity, push timeout, overflow, and after-hours branches.
- Finding 2 — Partially resolved: OTP now gates booking data, TravelPort access, and Summit priority, but Contact association still occurs before verification and reappears as Finding 3 below.
- Finding 3 — Resolved: Section 7 now documents the synchronous rationale, timeout, retry, agent fallback, logging owner, and A-03 validation step.
- Finding 4 — Partially resolved: end conditions and inactivity enforcement are defined, while the admitted Case-creation and returning-conversation gaps reappear as Finding 2 below.
- Finding 5 — Partially resolved: the revision adds metric boundaries and requirement tests, but the R-03 threshold and evidence-source gaps reappear as Findings 1 and 4 below.

### 1. The R-03 requirement and its acceptance criterion contradict each other

- Severity: Blocking
- Lens: Proof
- Location: Requirement R-03; Section 4.3, "VIP (R-03) enforcement and fallback"; Section 11 test table, R-03 row
- Evidence: R-03 states, "Summit-tier (VIP) travelers reach an agent within 60 seconds during business hours." The test table accepts, "Accepted ≤ 60s in 95% of test runs; alert fires on breach."
- Design gap: The requirements artifact states an unqualified 60-second outcome, while the design converts it to a 95% test threshold without a documented requirement change or accountable owner accepting the remaining breaches. The alert and callback describe breach handling; they do not reconcile the service target.
- Consequence: Staffing, routing capacity, UAT, and post-launch reporting can all pass a threshold that the governing requirement still defines as failure.
- Author's task: Reconcile R-03 and the 95% criterion through an accountable requirement decision, then align the routing behavior, breach handling, test acceptance, and production metric to the same approved service target.

### 2. Case-creation failure and returning-conversation behavior remain undefined

- Severity: Blocking
- Lens: Failure
- Location: Section 5, "Conversation Lifecycle," and Section 6, "Data Model"
- Evidence: "Travelers can start a new chat at any time from the portal." Section 6 states, "Each chat creates a Case at session start via a record-triggered flow on MessagingSession."
- Design gap: The document still does not define what happens when the Case-creation flow fails or how the system distinguishes a resumed/returning conversation from a genuinely new chat. The response log explicitly leaves both issues for later platform-team input.
- Consequence: R-05 can fail without recovery or operational visibility, and a returning traveler can create duplicate Cases or receive inconsistent lifecycle and reporting treatment.
- Author's task: Resolve the Case-creation failure path and the new-versus-returning conversation decision, including the enforcing event, recovery owner, customer/agent experience, and evidence that exactly one appropriate Case is tracked.

### 3. A typed email still links an unverified Contact to the Case

- Severity: High
- Lens: Failure
- Location: Section 9.1, "Identity verification," single-match branch
- Evidence: "Single match → the Contact is linked to the Case for context, but no booking data is shared and Summit priority is not granted until the traveler confirms a one-time code sent to the booking email address."
- Design gap: The OTP appropriately gates booking data and priority, but an anonymous visitor's unverified email still causes a Contact-to-Case association before identity is proven. No rationale, correction path, or audit treatment is defined for a mistyped or malicious single-match email.
- Consequence: Cases and transcripts can be attributed to the wrong Contact, corrupting customer history, service-team context, audit evidence, and downstream reporting even when Booking__c and TravelPort access remain blocked.
- Author's task: Decide when Contact association becomes trusted and define how pre-verification context, failed verification, incorrect linkage, correction, and audit history are handled.

### 4. The revised metrics still name labels, not reproducible evidence sources

- Severity: High
- Lens: Proof
- Location: Section 8, "Reporting," and Section 11 test table
- Evidence: "Average wait time: MessagingSession, from session start to agent acceptance" and "VIP 60-second attainment (R-03): percentage of Summit-tier chats accepted within 60 seconds, from routing flow timestamps."
- Design gap: The metrics still name no fields or persisted flow-timestamp location. The document does not show how a MessagingSession supplies the agent-acceptance boundary, how multiple AgentWork attempts affect handle time and chats-per-agent counts, or which evidence supports never-routed work. The R-02 disagreement is reasonable in principle, but the SDD delegates it to the response log instead of naming the external scorecard, owner, baseline, and six-month measurement boundary in the design.
- Consequence: Report builders can implement different formulas from the same text, producing incompatible wait, handle, volume, VIP-attainment, and phone-deflection results.
- Author's task: Make each KPI reproducible by identifying its actual fields or persisted events, multi-AgentWork treatment, inclusion/exclusion rules, and owner; record the external proof contract for R-02 in the SDD even if the source system is outside chat.

### 5. The all-user launch has no operational control or recovery design

- Severity: High
- Lens: Failure
- Location: Section 10, "Deployment," with Sections 3, 4.3–4.4, and 7
- Evidence: "The chat feature will go live for all portal users on the launch date, announced by marketing. The support team will be trained the week prior."
- Design gap: The single all-user cutover has no rationale, readiness gate, rollback decision window, rollback owner, or degraded portal behavior if the custom launcher or session initialization fails. Queue alerts and weekly TravelPort log review cover individual signals, but no production health model defines systemic routing, session-creation, integration, or wrapper-failure thresholds and escalation ownership.
- Consequence: A launcher, session, routing, or integration defect can reach the full portal population with no documented way to detect the systemic failure quickly, limit exposure, or restore service.
- Author's task: Establish the rollout and rollback decision, launch gates, degraded customer experience, health signals, thresholds, alert paths, and accountable owners needed to control an all-user release.

## Open Decisions for the Senior Architect

- Whether R-03 is an absolute 60-second requirement or a percentage-based service objective with an approved breach allowance; the requirements owner must accept the same target used by routing, UAT, and reporting.
- Whether OD-01 requires claims-licensed-agent eligibility at launch; that decision changes the queue model's eligibility, staffing, no-match behavior, and test coverage.
- Whether R-02 proof may remain in the support-operations scorecard rather than the chat reporting layer; if accepted, the formal design still needs the named external evidence contract and owner.

## Deferred Review Areas

Deferred until the priority findings are corrected: the requirement and tradeoff for the custom LWC versus the standard launcher; launcher initialization, pre-chat payload, OTP-service contract, and version-compatibility ownership; payment-data controls beyond agent training; transcript permission sets and retention policy; the integration-log data model; and OD-02's launcher placement decision.
