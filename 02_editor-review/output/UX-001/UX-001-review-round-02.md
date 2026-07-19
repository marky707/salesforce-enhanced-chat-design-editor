# Design Review

## Verdict
Ready for Formal Review with Open Decisions

All five round-01 findings are resolved with coherent, failure-bounded, and testable critical flows; remaining items are accountable senior-architect judgment calls (OD-02, OD-03 residual wording/targeting, and the owner-continuity business tradeoff).

> This verdict measures document readiness, not architecture approval. Final design approval remains with the accountable human architect and governance reviewers.

## Priority Findings

Round 1 resolution check:

- Finding 1 — Resolved: Section 5.2 defines a 30-second preferred-agent push to the Case owner, immediate fallback to the topic queue when the owner is offline, at capacity, OOO, declines, or times out, and a Case feed context note so R-04 is met by case context rather than only the named owner; R-05 budget alignment is stated.
- Finding 2 — Resolved: Section 5.1 provides a fixed decision sequence (business hours → language → topic queue → Pro-tier priority → Spanish coverage conflict), input defaults for missing language and topic, a mermaid flowchart, and an explicit Omni-Channel priority 1 vs 5 mechanism for Pro-tier; OD-01 is closed for a dedicated Pro Gear queue at launch.
- Finding 3 — Resolved: Section 4.1 commits to dual Embedded Service deployments (`ES-Web-Support`, `ES-Mobile-App`) with requirement-driven rationale; Section 9's wave table names each deployment and timing consistently.
- Finding 4 — Resolved: Section 7.1 drops `Chat_Interaction__c`, adopts native `MessagingSession.CaseId` for R-07, enumerates where interaction detail lives, and records the tradeoff against a custom junction.
- Finding 5 — Resolved: Section 10.1 defines wait time, abandonment, handle time, and first response with source objects, fields/formulas, lifecycle bounds, and LiveChatTranscript mapping notes for R-06 continuity.

No material readiness findings remain.

## Open Decisions for the Senior Architect

- **OD-02:** Whether chat transcripts should be attached to the Case as files or referenced only via MessagingSession (decision register remains open).
- **OD-03 residual:** Invitation duration and client/server expiry enforcement are designed in Section 6.1; final invitation wording and exact page-targeting rules remain open with the e-commerce team.
- Whether owner-continuity preferred-agent routing (Section 5.2, R-04) is still worth its operational complexity against the R-05 response-time SLA at current staffing, now that the path is bounded (30s) and falls back to queue-with-context — a business tradeoff beyond document readiness. R-04 requires "someone with their case context," which the design already satisfies on the fallback path alone.

## Deferred Review Areas

- Sections 4.2 and 7: the record-triggered Case create/attach flow on MessagingSession has no explicit failure, retry, logging owner, or agent-visible recovery when `CaseId` cannot be set — harden before build if platform risk assessment requires it.
- Section 6.1: server-side "stale invitation token rejected by configuration" is an unsupported platform claim relative to the clear client-side 5-minute timer; confirm enforceable mechanism or rely on the documented client authority for R-08.
- Section 5.1 Spanish preferred-push path: bilingual skill preference within shared topic queues is described operationally; detailed Omni-Channel Flow skill-requirement configuration remains a build-time elaboration.
- Section 5.4: work remaining in queue after all Available members are attempted has no customer-visible wait messaging or supervisor escalation threshold beyond the Section 9.2 / Section 10 monitoring posture.
- Section 11: transcript permission sets, retention, and mobile authenticated-context assurance depth are out of readiness scope for this pass but should be confirmed under security review.
