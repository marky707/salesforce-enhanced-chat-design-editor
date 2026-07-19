# Formal Architecture Review Decision — UX-001

- **Review ID:** UX-001
- **Document version reviewed:** v2 (`northstar-sdd-draft-v2.md`)
- **Review rounds completed:** 2 (verdict trajectory: Revise ×1 → Ready for Formal Review with Open Decisions)
- **Date (ISO 8601):** 2026-07-19

## Open decisions awaiting your judgment

- **OD-02:** whether chat transcripts should be attached to the Case as files or referenced only via MessagingSession.
- **OD-03 residual:** final proactive invitation wording and exact page-targeting rules (duration and expiry enforcement are already designed).
- **Owner-continuity tradeoff:** whether Section 5.2 preferred-owner push (30s + queue fallback) remains justified against R-05 staffing risk, given R-04 is satisfiable by queue-with-context alone.

Resolve these in your Rationale, or carry them as Conditions with owners.

## Decision

`Approved with Conditions`

## Rationale

v2 is architecturally coherent and ready to build against. Dual Embedded Service deployments (`ES-Web-Support`, `ES-Mobile-App`) correctly separate channel cutover, identity, and config risk. The Section 5.1 routing sequence is deterministic, failure-bounded, and platform-real (queue map + Omni-Channel priority 1/5 + Spanish preferred-push with flag fallback). Dropping `Chat_Interaction__c` in favor of native `MessagingSession.CaseId` is the right data-model call for R-07. KPI definitions in Section 10.1 are source-object-bound and map Legacy LiveChatTranscript metrics with an explicit baseline-break note. Wave plan, cutover, rollback, and the testing matrix are sufficient for design approval.

**OD-02 — Transcript attachment (dispositioned: MessagingSession reference only at launch).** Do **not** attach chat transcripts as Case files for launch. Enhanced Chat keeps the transcript and session lifecycle on `MessagingSession`; the Case link is `MessagingSession.CaseId`. Case file attachments would duplicate content, create permission/retention drift vs Messaging, and add storage without a stated compliance requirement. Agents and reporting reach the conversation through the related MessagingSession and standard console surfaces. Revisit only if Legal/Compliance later requires a Case-attached export (PDF or similar) for long-term Case-centric retention outside Messaging retention policy; that would be a separate design decision with retention and permission owners. OD-02 is **closed** on this basis for launch.

**OD-03 residual — Invitation wording and page targeting (dispositioned: non-architecture; condition below).** Architecture for R-08 is closed: 5-minute client-side expiry, web-only proactive for launch, deployment-scoped to `ES-Web-Support`. Final marketing copy and exact high-intent page list are e-commerce product decisions, not Service Cloud routing or data-model choices. They must land before Week 1 web go-live but do not require SDD redesign. Carried as Condition 1 (non-blocking for architecture approval).

**Owner-continuity tradeoff vs R-05 (dispositioned: keep Section 5.2 as designed).** Preferred-agent push to the Case owner for **30 seconds**, with **immediate** fallback when the owner is offline, at capacity, OOO, declines, or times out, plus a Case feed context note and native Case linkage, is worth the modest operational complexity. R-04 is satisfied on the fallback path alone (“someone with their case context”), so continuity is best-effort CX, not a hard dependency. R-05 alignment is credible: the owner attempt is hard-bounded; offline/capacity owners skip without burning wait; queue staffing remains the R-05 control plane (A-02: 14 agents, ~900 chats/week). Always-queue-only would be simpler but would discard low-cost continuity when the owner is Available. I am **not** directing removal of preferred-owner routing. Support ops should monitor owner-accept rate and first-response under the owner path in the first 30 days and may simplify to queue-only if R-05 breaches correlate with owner-push contention—that is an ops change, not a design rejection.

**Deferred areas (round-02):** Case-create failure/retry/logging, server-side stale-invitation enforcement claims, Omni skill-requirement detail for Spanish preferred push, post-queue wait messaging, and transcript permission/retention depth are build-time or security-review elaborations, not architecture blockers. Conditions 2–3 capture the two items that must be closed before production cutover without sending the package back through author revision.

*Provenance: this is a **fictional UX simulation formal decision** of the Northstar demo package (same demo provenance pattern as SI-001). Accountable reviewer persona: A. Chen (UX simulation). Decision recorded 2026-07-19.*

## Conditions (only for Approved with Conditions)

| # | Condition | Owner | Disposition | Blocking? |
|---|---|---|---|---|
| 1 | Finalize proactive invitation **wording** and **exact page-targeting rules** for high-intent support pages before Week 1 web cutover; keep Section 6.1 duration (5 min) and client-side expiry. Document targets in e-commerce runbook or linked config note (not a full SDD redesign). | E-commerce team (primary); Support ops (copy review) | Accepted — complete before Week 1 go-live; architecture approved without waiting for copy. | no |
| 2 | Before production build exit: harden the MessagingSession → Case create/attach automation with explicit failure path (retry or re-run), platform logging, and agent-visible recovery when `CaseId` cannot be set; name the operational owner for failed attaches. | Salesforce platform team (automation); Support ops (agent recovery) | Accepted — implement in build; verify in UAT (R-07 row of Section 12 matrix). | no |
| 3 | Confirm R-08 stale-invitation behavior against platform capabilities: either prove server-side rejection of expired invitation activation, or document client-side timer as the sole authority for expiry and adjust Section 6.1 wording accordingly before go-live. | Salesforce platform team (config/proof); Web team (client timer) | Accepted — resolve in build/config validation; does not reopen architecture of proactive chat. | no |

All conditions are **non-blocking**. Package may advance to `06_completed` under the stage contract once the workflow agent validates this record.

## Required changes (only for Changes Required)

Not applicable.

## Signature

- **Accountable reviewer (human actor):** A. Chen (UX simulation)
- **Role:** Senior Solution Architect
- **Date signed (ISO 8601):** 2026-07-19
