# Solstice Adventures — Enhanced Web Chat Implementation

## Solution Design Draft — v2

<!-- FICTIONAL TEST DOCUMENT. Revision responding to SI-001-review-round-01.md. -->

Author: P. Okafor, Salesforce Administrator
Status: Revised draft for re-review
Changes from v1: Sections 4, 5, 6, 7, and 9 substantially revised; Sections 8 and 11 updated; new Sections 4.1–4.4 and 9.1.

## 1. Executive Summary

Solstice Adventures, an adventure travel booking company, will add live chat to its customer portal using Salesforce Enhanced Chat (Messaging for In-App and Web). This is a new implementation — Solstice has never offered chat. The goal is to deflect phone volume for booking changes and claims questions and to give VIP travelers a premium support experience.

## 2. Requirements

See `solstice-requirements.md` (R-01 through R-07).

## 3. Proposed Architecture

Enhanced Chat will be added to the customer portal via a single Embedded Service deployment serving the web portal only. A custom LWC chat launcher will replace the standard chat button so the launcher matches Solstice brand guidelines and can display seasonal promotions. Mobile app chat is a future phase.

Pre-chat will collect the traveler's email and topic (Booking Change, Claim, Other). The routing decision sequence is defined in Section 4.1; the Appendix A diagram reference from v1 has been removed and replaced by the decision table below.

## 4. Routing Design

Routing is **queue-based**. Skills-based routing was considered and rejected for launch: with eight chat-certified agents (A-02), skill combinations would fragment a small pool and create no-eligible-agent branches that queues avoid. This decision will be revisited if OD-01 requires a claims-licensed skill. The v1 statement that uncertified agents "remain in the general queue" is withdrawn; there is no general queue. Agents are members of the Bookings queue, the Claims queue, or both.

### 4.1 Routing decision sequence

Evaluated in order for every chat request:

| Step | Input | Rule | Outcome |
|---|---|---|---|
| 1 | Business hours | Outside 6am–8pm MT (org Business Hours record) | Launcher is hidden; portal shows support hours and the case web form. No session is created. |
| 2 | Topic (pre-chat) | Booking Change → Bookings queue; Claim → Claims queue; Other → Bookings queue | Work item routed to the queue with the mapped priority (step 3). |
| 3 | Summit tier (on matched, verified Contact — Section 9.1) | Summit → routing priority 1; all others → priority 5 | Priority 1 work is pushed ahead of priority 5 within the queue. |
| 4 | Missing/failed pre-chat topic | Default to Bookings queue, priority 5 | Chat is never dropped for a missing input. |

### 4.2 Agent availability, capacity, and push timeout

Agents handle up to 3 concurrent chats (Omni-Channel capacity). A pushed chat not accepted within 30 seconds times out and is pushed to the next available queue member. After all available members have been attempted, the work item waits in queue and is pushed as capacity frees.

### 4.3 VIP (R-03) enforcement and fallback

Summit-tier chats enter at priority 1. If no agent has accepted within 60 seconds of routing, a flow posts an alert to the supervisor Slack channel and the chat remains first in queue; the customer sees an auto-response acknowledging the delay and offering a callback option. The 60-second timer is measured by the routing flow from work-item creation.

### 4.4 Queue overflow

If any queue's oldest waiting chat exceeds 5 minutes, supervisors are alerted (same flow) and the auto-response offers the callback option to all waiting customers in that queue.

## 5. Conversation Lifecycle

A conversation starts when the traveler submits the pre-chat form during business hours. Sessions are ended by: (a) the customer closing the chat, (b) the agent ending the conversation at wrap-up, or (c) automatic closure after 30 minutes of customer inactivity, enforced by the Enhanced Chat session inactivity setting on the deployment. Travelers can start a new chat at any time from the portal.

## 6. Data Model

Each chat creates a Case at session start via a record-triggered flow on MessagingSession. The Case is linked to the traveler's booking record (Booking__c) only after identity verification succeeds (Section 9.1). Contact matching uses the pre-chat email; match handling is defined in Section 9.1.

## 7. Integration Design

During a chat, agents can look up live booking details from the TravelPort reservation system from the console. The call is synchronous with a 5-second timeout and one automatic retry. Synchronous was chosen over asynchronous because the agent needs the answer within the conversation turn and projected volume (A-01) is well under the API's rated capacity; an async callout would add queuing complexity with no user benefit. On failure or timeout, the agent sees an error banner with a "retry" action and falls back to the existing TravelPort agent portal (the current manual process); the failure is logged to an integration log object reviewed by the platform team weekly. Assumption A-03 (contract reuse) will be validated by a contract test against the TravelPort sandbox during build week 1; if it fails, the existing console API contract is extended before UAT.

## 8. Reporting

- **Average wait time:** MessagingSession, from session start to agent acceptance, daily dashboard.
- **Handle time:** AgentWork, from accept to close, per agent, daily.
- **Chats per agent:** count of accepted AgentWork per agent per day.
- **CSAT:** post-chat survey (existing survey tool), weekly.
- **VIP 60-second attainment (R-03):** percentage of Summit-tier chats accepted within 60 seconds, from routing flow timestamps, weekly.

Phone-volume reduction (R-02) is intentionally not a chat dashboard metric — see the response log, Finding 5 disagreement.

## 9. Security

Chat is available to any portal visitor without login for general questions. Booking-specific context requires verification (9.1). Transcripts are visible to the service team. Payment card numbers must never be requested in chat; agents are trained to direct payment to the secure portal flow. (Automated masking is deferred — see response log.)

### 9.1 Identity verification

Pre-chat email alone is treated as an **unverified claim**. Contact matching behavior:

- No match or multiple matches → no Contact is auto-linked; the agent may associate manually after verification.
- Single match → the Contact is linked to the Case for context, but **no booking data is shared and Summit priority is not granted** until the traveler confirms a one-time code sent to the booking email address (existing portal OTP service).
- Verification failure or decline → the chat continues as a general, unverified conversation; no Booking__c link, no TravelPort lookup, no Summit priority.

## 10. Deployment

The chat feature will go live for all portal users on the launch date, announced by marketing. The support team will be trained the week prior.

## 11. Testing

Each requirement maps to test cases with expected results, built during UAT preparation:

| Req | Test approach | Acceptance criterion |
|---|---|---|
| R-01 | End-to-end chat on portal for both topics | Session created, routed per 4.1, Case created |
| R-03 | Summit chat during staffed hours | Accepted ≤ 60s in 95% of test runs; alert fires on breach |
| R-04 | Verified traveler booking lookup | Current TravelPort data displayed; failure shows banner + manual fallback |
| R-05 | Every test chat | Exactly one Case per session, correctly linked |
| R-06 | Chat attempted at 5:59am and 8:01pm MT | Launcher hidden; case web form offered |
| R-07 | Dashboard review | All Section 8 metrics populated after test week |

QA executes these in the partial sandbox; two team leads perform UAT against the same table.
