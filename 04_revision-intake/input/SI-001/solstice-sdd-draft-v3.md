# Solstice Adventures — Enhanced Web Chat Implementation

## Solution Design Draft — v3

<!-- FICTIONAL TEST DOCUMENT. Revision responding to SI-001-review-round-02.md. -->

Author: P. Okafor, Salesforce Administrator
Status: Revised draft for re-review
Changes from v2: Sections 5, 6, 8, 9.1, 10, and 11 revised; new Sections 5.1, 6.1, 10.1–10.3; requirements artifact updated to v2 (R-03 restated with owner approval).

## 1. Executive Summary

Solstice Adventures, an adventure travel booking company, will add live chat to its customer portal using Salesforce Enhanced Chat (Messaging for In-App and Web). This is a new implementation — Solstice has never offered chat. The goal is to deflect phone volume for booking changes and claims questions and to give VIP travelers a premium support experience.

## 2. Requirements

See `solstice-requirements-v2.md` (R-01 through R-07). **R-03 was restated in v2 of the requirements artifact:** the VP Customer Experience (requirement owner) approved on 2026-07-18 restating R-03 from an unqualified 60-second outcome to a service objective — *"95% of Summit-tier chats are accepted by an agent within 60 seconds during business hours, measured weekly; every breach triggers the Section 4.3 alert and callback offer."* Routing (4.3), testing (Section 11), and reporting (Section 8) all use this single approved target.

## 3. Proposed Architecture

Enhanced Chat will be added to the customer portal via a single Embedded Service deployment serving the web portal only. A custom LWC chat launcher will replace the standard chat button so the launcher matches Solstice brand guidelines and can display seasonal promotions; the standard launcher was evaluated and rejected because it cannot host the promotion slot required by marketing, and the tradeoff (Solstice owns launcher-initialization failure handling, Section 10.2) is accepted. Mobile app chat is a future phase.

Pre-chat will collect the traveler's email and topic (Booking Change, Claim, Other). The routing decision sequence is defined in Section 4.1.

## 4. Routing Design

Routing is **queue-based**. Skills-based routing was considered and rejected for launch: with eight chat-certified agents (A-02), skill combinations would fragment a small pool and create no-eligible-agent branches that queues avoid. This decision will be revisited if OD-01 requires a claims-licensed skill. Agents are members of the Bookings queue, the Claims queue, or both.

### 4.1 Routing decision sequence

| Step | Input | Rule | Outcome |
|---|---|---|---|
| 1 | Business hours | Outside 6am–8pm MT (org Business Hours record) | Launcher hidden; portal shows support hours and the case web form. No session is created. |
| 2 | Topic (pre-chat) | Booking Change → Bookings queue; Claim → Claims queue; Other → Bookings queue | Work item routed to the queue with the mapped priority (step 3). |
| 3 | Summit tier (verified Contact only — Section 9.1) | Summit → routing priority 1; all others → priority 5 | Priority 1 work is pushed ahead of priority 5 within the queue. |
| 4 | Missing/failed pre-chat topic | Default to Bookings queue, priority 5 | Chat is never dropped for a missing input. |

### 4.2 Agent availability, capacity, and push timeout

Agents handle up to 3 concurrent chats (Omni-Channel capacity). A pushed chat not accepted within 30 seconds times out and is pushed to the next available queue member. After all available members have been attempted, the work item waits in queue and is pushed as capacity frees.

### 4.3 VIP (R-03) enforcement and fallback

Summit-tier chats enter at priority 1. If no agent has accepted within 60 seconds of routing, a flow posts an alert to the supervisor Slack channel and the chat remains first in queue; the customer sees an auto-response acknowledging the delay and offering a callback option. The 60-second timer runs from work-item creation; the flow stamps `VIP_Routed_At__c` and `VIP_Accepted_At__c` on the MessagingSession (Section 8) so attainment against the approved 95% objective is measured from persisted fields.

### 4.4 Queue overflow

If any queue's oldest waiting chat exceeds 5 minutes, supervisors are alerted (same flow) and the auto-response offers the callback option to all waiting customers in that queue.

## 5. Conversation Lifecycle

A conversation starts when the traveler submits the pre-chat form during business hours. Sessions are ended by: (a) the customer closing the chat, (b) the agent ending the conversation at wrap-up, or (c) automatic closure after 30 minutes of customer inactivity, enforced by the Enhanced Chat session inactivity setting on the deployment.

### 5.1 New versus returning conversations

Every portal chat starts a new MessagingSession; ended sessions are not resumed. Case linkage prevents fragmentation instead: for a **verified** traveler (9.1) with a Case updated in the last 7 days, the Case-linking flow attaches the new session to that open Case rather than creating another; the agent sees prior session transcripts through the Case. Unverified chats always create a new Case. Reporting distinguishes first-contact from follow-up sessions via `Follow_Up__c`, set by the flow when it attaches to an existing Case.

## 6. Data Model

Each chat creates or links a Case at session start via a record-triggered flow on MessagingSession, per Section 5.1. The Case is linked to the traveler's booking record (Booking__c) only after identity verification succeeds (Section 9.1).

### 6.1 Case-creation failure handling

If the record-triggered flow fails, the failure is logged to the integration log object and the session continues — chat service is never blocked by Case creation. The agent console shows a "No Case linked" banner with a one-click quick action to create and link the Case manually. A scheduled hourly report of sessions older than 15 minutes with no Case alerts the platform team channel; more than 3 flow failures in an hour pages the platform lead. R-05 is proven by the daily exception report "MessagingSessions without Case" (target: zero rows after manual remediation).

## 7. Integration Design

During a chat, agents can look up live booking details from the TravelPort reservation system from the console. The call is synchronous with a 5-second timeout and one automatic retry. Synchronous was chosen over asynchronous because the agent needs the answer within the conversation turn and projected volume (A-01) is well under the API's rated capacity; an async callout would add queuing complexity with no user benefit. On failure or timeout, the agent sees an error banner with a "retry" action and falls back to the existing TravelPort agent portal (the current manual process); the failure is logged to the integration log object reviewed by the platform team weekly. Assumption A-03 (contract reuse) will be validated by a contract test against the TravelPort sandbox during build week 1; if it fails, the existing console API contract is extended before UAT.

## 8. Reporting

Each KPI names its object, fields, boundaries, and treatment of multiple routing attempts. One routing attempt = one AgentWork; a session can have several (push timeout, transfer).

| KPI | Source | Definition | Owner / cadence |
|---|---|---|---|
| Average wait time | AgentWork | First AgentWork per session: `AcceptDateTime − RequestDateTime`. Subsequent AgentWork (transfers, re-pushes) excluded from wait. | Service Ops / daily |
| Handle time | AgentWork | `CloseDateTime − AcceptDateTime` per accepted AgentWork; a transferred session contributes one handle-time interval per accepting agent. | Service Ops / daily |
| Chats per agent | AgentWork | Count of AgentWork with status Closed per agent per day. | Service Ops / daily |
| Never-routed / abandoned | MessagingSession | Sessions with no AgentWork, ended before acceptance. | Service Ops / daily |
| VIP 60-second attainment (R-03) | MessagingSession | `VIP_Accepted_At__c − VIP_Routed_At__c ≤ 60s` for Summit sessions; weekly % against the approved 95% objective. | Service Ops / weekly |
| Follow-up ratio | MessagingSession | `Follow_Up__c` true vs. false (Section 5.1). | Service Ops / weekly |
| CSAT | Post-chat survey (existing tool) | Existing survey score, chat channel filter. | CX team / weekly |

**R-02 (30% phone-volume reduction)** is proven outside the chat layer, and the proof contract is recorded here: source — Support Operations scorecard (existing phone reporting); owner — Director of Support Operations; baseline — trailing 3-month booking-change call volume ending the month before launch; measurement — monthly for six months post-launch against that baseline. The chat layer contributes adoption volume (sessions by topic) to that scorecard; it does not restate the phone metric.

## 9. Security

Chat is available to any portal visitor without login for general questions. Booking-specific context requires verification (9.1). Transcripts are visible to the service team. Payment card numbers must never be requested in chat; agents are trained to direct payment to the secure portal flow. (Automated masking is deferred — see round-01 response log.)

### 9.1 Identity verification

Pre-chat email is an **unverified claim**. No Contact is associated with the session or Case before verification, regardless of match count — pre-verification chats carry no Contact, no Summit priority, no booking context.

- **Verification:** on a single Contact match, the traveler is offered a one-time code sent to the booking email (existing portal OTP service). On success, the flow links Contact and Case, stamps `Verified_Via__c = OTP`, and grants Summit priority for the remainder of the session if applicable.
- **No match / multiple matches / failed or declined OTP:** the chat continues as a general unverified conversation. The agent may verify identity in-conversation using the existing phone verification procedure (booking number + name + travel date) and then link the Contact manually; manual linkage stamps `Verified_Via__c = Agent`.
- **Correction and audit:** every linkage records who/what linked it and how (`Verified_Via__c`, standard field history on Case). Mislinked Cases are corrected by the agent unlinking and relinking; field history preserves the audit trail.

## 10. Deployment

### 10.1 Phased rollout

Launch is gated, not all-at-once. Week 1–2: the launcher is shown to 10% of portal sessions via the existing portal feature-flag service. Gate review at end of week 2 against the Section 10.3 health thresholds, decided jointly by the Service Operations manager and platform lead. On pass, ramp to 100%; on fail, hold at 10% or roll back. The launch date is announced by marketing **after** the gate passes.

### 10.2 Rollback and degraded behavior

Rollback = feature flag off: the launcher disappears from new portal sessions immediately; in-flight chats are allowed to finish; the portal falls back to the case web form (its current state). Rollback owner: Service Operations manager, with the platform lead; decision window: any time during the first 4 weeks. If the custom LWC launcher fails to initialize, it renders nothing and the portal's standard "Contact us" links remain — chat failure never blocks the portal.

### 10.3 Production health model

| Signal | Source | Threshold | Alert / owner |
|---|---|---|---|
| Session-creation failures | Deployment/API logs | > 5 per hour | Slack #chat-ops → platform lead |
| Case-flow failures | Integration log (6.1) | > 3 per hour | Page platform lead |
| No-accept rate | AgentWork declined/timed-out % | > 20% over 30 min | Slack #chat-ops → Service Ops manager |
| TravelPort error rate | Integration log | > 10% of lookups over 1 hour | Slack #chat-ops → platform team |
| Queue wait | Oldest waiting chat | > 5 min (4.4) | Supervisor alert (existing) |

The support team is trained the week prior to the 10% launch.

## 11. Testing

| Req | Test approach | Acceptance criterion |
|---|---|---|
| R-01 | End-to-end chat on portal for both topics | Session created, routed per 4.1, Case created or linked per 5.1/6.1 |
| R-03 (as restated) | Summit chats during staffed hours, sandbox load matching A-01 volume | ≥ 95% accepted ≤ 60s from persisted `VIP_*` fields; alert and callback fire on each breach |
| R-04 | Verified traveler booking lookup, plus forced timeout | Current data displayed; failure shows banner + manual fallback; entry in integration log |
| R-05 | Every test chat, plus forced Case-flow failure | Exactly one appropriate Case per 5.1; failure path shows banner, quick action links Case, exception report catches the gap |
| R-06 | Chat attempted at 5:59am and 8:01pm MT | Launcher hidden; case web form offered |
| R-07 | Dashboard review after test week | All Section 8 KPIs populated from their named fields |

QA executes these in the partial sandbox; two team leads perform UAT against the same table. Identity paths (OTP success, failure, manual verification, mislink correction) are tested under R-04/R-05.
