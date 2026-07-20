# Critique Examples

What acceptable architecture critique looks like — and the two ways feedback goes wrong. Consult this when unsure whether a draft finding is specific enough or has crossed into authoring.

## The three modes

Given the same weak passage — *"Chats will be routed to the best available agent."* —

- **Generic feedback (useless):** "Consider strengthening the routing section with more detail." Names no weakness, no consequence, no task. The author learns nothing.
- **Rewriting (forbidden):** "Replace with: 'Chats are routed via an Omni-Channel Flow that checks queue membership, language skill, and capacity, falling back to the General queue after 60 seconds.'" The editor just authored the design. The author learned nothing and now owns words they don't understand.
- **Acceptable critique:** "Section 5 says chats route to 'the best available agent' but never defines *best* or *available*. Evidence: 'Chats will be routed to the best available agent.' Because no eligibility, priority, or capacity rule is stated, two developers would implement two different routing behaviors, and QA has no expected result to test. What are the exact inputs and precedence rules that select the target agent, and what happens when no agent qualifies?"

The pattern: **exact location + quoted evidence + specific gap + downstream consequence + a question the author must answer.** The editor may name what's missing; it never supplies the answer.

## Paired examples by weakness type

### 1. Missing rationale (Why)

- ❌ "The junction object decision needs more justification."
- ✓ "Section 7 introduces `Chat_Interaction__c` linking MessagingSession to Case, but no requirement is cited and no native alternative is weighed — MessagingSession already carries a Case lookup. Evidence: 'A custom object Chat_Interaction__c will relate each chat to its Case.' Without rationale, the review board cannot judge whether this customization is justified, and the org inherits a custom object to maintain forever. Which requirement can the native relationship not satisfy, and what tradeoff makes the junction worth its maintenance cost?"

Note: the critique **names** the native alternative to expose the missing tradeoff — it does not select it.

### 2. Missing flow (Flow)

- ❌ "The escalation process could be clearer."
- ✓ "Section 5.3 states 'complex cases are escalated to Tier 2' but no artifact shows who or what decides *complex*, how the transfer occurs (flag, transfer button, new routing request?), or what the customer experiences during the handoff. Consequence: developers will invent an escalation mechanism, and the Tier 2 queue's reporting will not distinguish escalations from direct assignments. Walk the escalation end-to-end: what triggers it, which system acts, what state changes, and what does each party see?"

### 3. Undefined fallback (Failure)

- ❌ "Consider adding error handling for routing."
- ✓ "Section 5.2 routes VIP chats directly to the account owner, but defines no behavior when the owner is offline, at capacity, or out of office. Evidence: 'VIP customers will be routed directly to their account owner.' Until a timeout and fallback target are defined, a VIP chat can wait indefinitely — the failure mode most likely to reach an executive. When the owner cannot accept within a bounded time, where does the work item go, and who defines that bound?"

### 4. Reporting ambiguity (Proof)

- ❌ "The reporting section should specify data sources."
- ✓ "Section 10 commits to 'average wait time' without naming a source object, field or metric type, or the lifecycle moments that start and stop the clock. MessagingSession, MessagingSessionMetrics, and AgentWork measure different things — a native response-time metric is not automatically request-to-acceptance or queue-entry-to-first-response. Consequence: the dashboard will be built on whichever object the report builder finds first, and operations will manage staffing against a number nobody can define. For each metric: which object and field or metric type, which population, and which lifecycle events bound it?"

### 5. Unclear ownership (Flow)

- ❌ "Clarify responsibilities for the mobile wrapper."
- ✓ "Section 8 says 'the mobile app wrapper passes the customer context at session start' but never states which team owns the wrapper, how its version is coordinated with deployment changes, or which side validates the payload. Consequence: when context stops arriving after an app release, no one is accountable and triage spans two teams' backlogs. Who owns the wrapper contract, and what happens to a session when the expected context is absent or malformed?"

### 6. Unsupported customization (Why)

- ❌ "Is custom code really needed here?"
- ✓ "Section 6.2 proposes an Apex trigger to reopen ended sessions, citing no requirement that native session-timeout and reopen configuration cannot meet. Evidence: 'A trigger on MessagingSession will reopen sessions that end prematurely.' Unjustified Apex on a high-volume object adds failure surface and upgrade risk. Which specific behavior was verified as unachievable with native session configuration, and where is that verification recorded?"

### 7. Contradictions

- ❌ "Some sections seem inconsistent about deployments."
- ✓ "Section 4 states 'a single Embedded Service deployment will serve web and mobile,' while Section 9's cutover table migrates 'the web deployment' and 'the mobile deployment' separately. These cannot both be true. Consequence: the build team does not know how many deployments to configure, and every deployment-scoped setting (pre-chat, business hours, routing target) is ambiguous. Which is correct — and after correcting it, which other sections inherit the change?"

### 8. Missing proof (Proof)

- ❌ "Add test cases for the requirements."
- ✓ "Requirement R-12 ('customers never wait more than 2 minutes without a response') has no test approach, no measuring object or field, and no acceptance criterion anywhere in Sections 10–12. Consequence: the requirement will be declared met at go-live without evidence, and the first proof will be a customer complaint. What observable event data will demonstrate R-12 is met, and what threshold constitutes passing?"

---

## Verdict calibration examples

These compact cases teach the harder judgment: when a polished document still has a material gap, when to stop and say Ready, and when there is too little evidence to review.

### Strong-looking design with a hidden proof-population gap

Suppose a polished SDD states:

- Requirement R-03: “During support hours, at least 95% of chats receive a first agent response within 90 seconds.”
- Failure path: sessions end when no eligible agent is available.
- KPI population: “in-hours sessions that reached `Active`.”
- UAT population: “30 timed accepts.”

The correct result is **not Ready**. Both proof populations exclude the no-agent sessions most likely to fail R-03.

> **Acceptable finding:** “Sections 2, 4, 7, and 9 apply R-03 to at least 95% of all in-hours chats, but the KPI counts only sessions that reached `Active` and UAT samples only accepted work. The no-eligible-agent branch ends before either population begins. Consequence: the dashboard and test can report compliance while excluding the requirement's worst failures. Which reporting denominator and UAT sample will include every applicable in-hours session, including sessions that end before acceptance—or where is an accountable owner’s approval of the narrower population recorded?”

This is a Proof finding even when routing, security, deployment, and the rest of the design are strong. Do not let overall document quality hide a denominator mismatch.

Different case: if the design explicitly reports every success and failure category, tests each one, and frames the only remaining issue as the bounded choice “retain the unqualified requirement or approve the documented 95% target,” the editor may carry that choice to the named requirement owner as an Open Decision and issue `Ready for Formal Review with Open Decisions`. The distinction is whether builders and QA still lack proof behavior, or whether only an accountable human commitment remains.

### Ready with a real Open Decision

Suppose the requirements, normal and failure flows, KPI populations, and UAT populations reconcile; builders and QA can follow the design; and the author's register leaves one accountable staffing tradeoff unresolved.

```markdown
## Verdict
Ready for Formal Review with Open Decisions

The design is coherent and testable across its critical paths; the remaining staffing choice requires accountable operational judgment rather than another author revision.

> This verdict measures document readiness, not architecture approval. Final design approval remains with the accountable human architect and governance reviewers.

## Priority Findings

No priority findings.

## Open Decisions for the Senior Architect

- **OD-04:** Whether Claims keeps higher routing priority during catastrophe staffing changes — Support Operations must weigh response-time risk against claims urgency with the accountable architect.

## Deferred Review Areas

- The already-approved R-03 amendment is referenced but not attached to this review package; confirm packet inclusion — *build-entry validation*
- Legal's retention letter remains a production prerequisite; no unresolved design choice is presented — *build-entry validation*
```

The signed amendment is missing evidence, not an Open Decision. The retention letter is a gate, not an Open Decision, unless someone must still choose a retention policy or accept its risk.

### Insufficient Context without inventing the missing design

Suppose the entire submission says: “Route customers to the best available agent, respond quickly, and reuse the current dashboards.”

```markdown
## Verdict
Insufficient Context

The submission names desired outcomes but provides no requirements baseline, walkable routing behavior, failure paths, or measurable proof from which to perform a responsible design review.

> This verdict measures document readiness, not architecture approval. Final design approval remains with the accountable human architect and governance reviewers.

## Priority Findings

### 1. Routing cannot be evaluated

- Severity: Blocking
- Lens: Flow
- Location: Routing statement
- Evidence: “Route customers to the best available agent.”
- Design gap: “Best” and “available” have no eligibility inputs, precedence, capacity rule, target, timeout, or no-agent outcome.
- Consequence: Builders must invent the routing policy and QA has no expected result.
- Author's task: Provide the requirements and end-to-end routing decisions a reviewer can evaluate, including failure outcomes; do not ask the editor to supply them.

## Open Decisions for the Senior Architect

None can be responsibly identified until the missing requirements and design choices are supplied.

## Deferred Review Areas

Defer reporting, security, deployment, and operations review until a reviewable SDD exists.
```

An `Insufficient Context` verdict identifies the prerequisite evidence; it does not turn the editor into the author.

---

## Complete sample review

The Northstar fixture draft (`fixtures/northstar/` in the repository) reviewed in full. Keep this in sync with `fixtures/northstar/expected-review-round-01.md`.

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
