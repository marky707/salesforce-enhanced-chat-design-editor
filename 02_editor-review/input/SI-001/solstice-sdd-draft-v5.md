# Solstice Adventures — Enhanced Web Chat Implementation

## Solution Design Draft — v5

<!-- FICTIONAL TEST DOCUMENT. Revision responding to SI-001-review-round-04.md. -->

Author: P. Okafor, Salesforce Administrator
Status: Revised draft for re-review
Changes from v4: session-lifecycle enforcement and tests (5.2); TravelPort sequence diagram (7.1); launcher payload contract (3.2); data-relationship diagram (6.2); end-to-end process view (5.3); integration-log definition (7.2); remaining deferred items closed (9.1, 10.3, 11).

## 1. Executive Summary

Solstice Adventures, an adventure travel booking company, will add live chat to its customer portal using Salesforce Enhanced Chat (Messaging for In-App and Web). This is a new implementation — Solstice has never offered chat. The goal is to deflect phone volume for booking changes and claims questions and to give VIP travelers a premium support experience.

## 2. Requirements

See `solstice-requirements-v2.md` (R-01 through R-07; R-03 restated as the approved 95%/60-second service objective, owner-approved 2026-07-18).

## 3. Proposed Architecture

Enhanced Chat will be added to the customer portal via a single Embedded Service deployment serving the web portal only. A custom LWC chat launcher will replace the standard chat button so the launcher matches Solstice brand guidelines and can display seasonal promotions; the standard launcher was evaluated and rejected because it cannot host the promotion slot required by marketing, and the tradeoff (Solstice owns launcher-initialization failure handling, Section 10.2, and the interface contract, Section 3.2) is accepted. Mobile app chat is a future phase. Launcher placement on the page (OD-02) is a UX decision with no technical impact — the launcher loads the same deployment and sends the same contract regardless of position; OD-02 is closed for architecture purposes.

### 3.1 System context

```mermaid
flowchart LR
    subgraph Internet["Customer (untrusted)"]
        T[Traveler browser]
    end
    subgraph Portal["Solstice Portal (Solstice-owned)"]
        L[Custom LWC launcher]
        FF[Feature-flag service]
        OTP[Portal OTP service]
    end
    subgraph SF["Salesforce (trust boundary: authenticated org)"]
        ES[Embedded Service deployment]
        OC[Omni-Channel routing flow]
        MS[MessagingSession / Case]
        AG[Agent console]
    end
    subgraph Ext["External (contracted)"]
        TP[TravelPort API]
        SL[Slack alerts]
    end
    T -->|"loads portal page"| L
    FF -->|"show/hide launcher"| L
    L -->|"pre-chat contract v1.0 (HTTPS)"| ES
    L -->|"OTP challenge/response"| OTP
    OTP -->|"signed verification result"| ES
    ES --> OC --> MS --> AG
    AG -->|"booking lookup (server-side, named credential)"| TP
    OC -->|"threshold alerts"| SL
```

Ownership at each boundary: Solstice web team owns the launcher, feature flag, and OTP service; the Salesforce admin team owns the deployment, routing flow, and data model; the platform team owns the TravelPort named-credential integration and the Slack alert flow. All customer traffic terminates at the portal or Embedded Service endpoints; no external system calls into Salesforce except TravelPort responses to Salesforce-initiated requests.

### 3.2 Launcher-to-Salesforce interface contract

The launcher submits pre-chat as **Contract v1.0**, a versioned JSON payload in the Embedded Service hidden pre-chat fields:

| Field | Type | Rule |
|---|---|---|
| `contractVersion` | string | Must equal a version the deployment accepts (launch: `1.0`) |
| `portalSessionId` | string | Portal session correlation id |
| `email` | string | Traveler-typed; **untrusted** until 9.2 verification |
| `topic` | enum | `booking_change` / `claim` / `other` |
| `otpResult` | object or null | `{status, signature, issuedAt}` — signed by the portal OTP service |

- **Validation is Salesforce-side**, in the session-start flow: schema check, enum check, signature verification of `otpResult` against the OTP service public key, and staleness check (`issuedAt` older than 5 minutes = stale). The launcher performs input formatting only; nothing client-side is trusted.
- **Rejection behavior:** malformed payload, unknown `contractVersion`, invalid signature, or stale `otpResult` → the session proceeds as **unverified**, topic defaults to `other` → Bookings queue, and a `contract_reject` entry is written to the integration log. The chat is never dropped.
- **Release compatibility:** the deployment declares its accepted contract versions; contract changes require a new version, a joint release checklist (web team + Salesforce admin team), and the contract test — a CI job in the portal pipeline that submits each supported payload variant against the Salesforce sandbox and asserts routing and verification outcomes — passing **before** either side releases. Breaking a version without the checklist is a release-process violation.
- **Detection:** `contract_reject` rate is a Section 10.3 health signal; a spike is the "breaking release reached customers" alarm.

Pre-chat collects the traveler's email and topic (Booking Change, Claim, Other). The routing decision sequence is defined in Section 4.1.

## 4. Routing Design

Routing is **queue-based**. Skills-based routing was considered and rejected for launch: with eight chat-certified agents (A-02), skill combinations would fragment a small pool and create no-eligible-agent branches that queues avoid. This decision will be revisited if OD-01 requires a claims-licensed skill. Agents are members of the Bookings queue, the Claims queue, or both.

### 4.1 Routing decision sequence

Verification (9.2) completes **before** the work item is created, so priority is known at routing time.

| Step | Input | Rule | Outcome |
|---|---|---|---|
| 1 | Business hours | Outside 6am–8pm MT (org Business Hours record) | Launcher hidden; portal shows support hours and the case web form. No session is created. |
| 2 | Topic (validated contract field) | `booking_change` → Bookings; `claim` → Claims; `other` → Bookings | Work item routed to the queue with the mapped priority (step 3). |
| 3 | Verification outcome (9.2, already resolved) | Verified Summit → priority 1; everyone else → priority 5 | Priority is fixed at work-item creation and never changed afterward. |
| 4 | Missing/failed/rejected contract fields | Default to Bookings queue, priority 5, unverified | Chat is never dropped for a bad input. |

### 4.2 Agent availability, capacity, and push timeout

Agents handle up to 3 concurrent chats (Omni-Channel capacity). A pushed chat not accepted within 30 seconds times out and is pushed to the next available queue member. After all available members have been attempted, the work item waits in queue and is pushed as capacity frees.

### 4.3 VIP (R-03) enforcement and fallback

Verified-Summit chats enter at priority 1. The R-03 clock runs from work-item creation (`VIP_Routed_At__c`) to acceptance by the accepting agent (`VIP_Accepted_At__c` = the `AcceptDateTime` of the accepted AgentWork, regardless of earlier timed-out pushes). If no acceptance within 60 seconds, a flow posts an alert to the supervisor Slack channel and the chat remains first in queue; the customer sees an auto-response acknowledging the delay and offering a callback option.

### 4.4 Queue overflow

If any queue's oldest waiting chat exceeds 5 minutes, supervisors are alerted (same flow) and the auto-response offers the callback option to all waiting customers in that queue.

## 5. Conversation Lifecycle

A conversation starts when the traveler submits pre-chat (and completes or skips verification, 9.2) during business hours. Sessions are ended by: (a) the customer closing the chat, (b) the agent ending the conversation at wrap-up, or (c) automatic closure after 30 minutes of customer inactivity, enforced by the deployment's session inactivity setting.

### 5.1 New versus returning conversations and Case selection

Every accepted pre-chat submission initiates a **new conversation** (enforcement in 5.2). The Case-linking flow selects the Case deterministically:

- **Zero** open Cases updated in the last 7 days for the verified Contact → create a new Case.
- **Exactly one** open recent Case **whose topic matches the pre-chat topic** → attach the session to it and set `Follow_Up__c = true`.
- **Multiple** topic-matching recent Cases, or recent Cases only on other topics → **create a new Case** (never guess). The agent console shows the "Recent Cases" related list; the agent may merge or relate Cases afterward via the standard Case-merge procedure, which preserves audit history.
- **Unverified** traveler → always a new Case, no recent-Case lookup.

### 5.2 Session non-resumption: enforcement and proof

The v4 claim that "ended sessions are not resumed" is restated here as **configured, testable behavior rather than an assumed platform guarantee**:

- **Enforcing mechanism:** (1) the launcher never stores a conversation token across page loads — every pre-chat submission requests a fresh conversation from the deployment; (2) the deployment's session inactivity and end settings close the conversation on each Section 5 end condition. Whether the platform *could* resume a session is treated as unknown until tested.
- **Acceptance evidence (build week 1, alongside the A-03 contract test):** for each end condition — customer close, agent end, inactivity timeout — the sandbox test re-opens the portal and starts a chat, asserting the new `MessagingSession.Id` differs from the prior session and the prior session's status remains ended (Section 11, lifecycle rows).
- **Contingency:** if testing shows the platform resumes a session in any path, the design falls back to session-agnostic continuity: the Case-selection flow (5.1) keys on the *conversation's* session Id at start, `Follow_Up__c` and all Section 8 KPIs are defined per MessagingSession record and remain valid, and the resumption path is documented and re-reviewed before UAT.
- **Customer/agent experience on return:** the returning traveler always experiences a fresh chat (new pre-chat, new verification offer); continuity is provided through the linked Case history visible to the agent, not through transcript resumption.

### 5.3 End-to-end process view

```mermaid
flowchart TD
    A[Traveler opens portal] --> B{Business hours?}
    B -- no --> B1[Launcher hidden - case web form]
    B -- yes --> C[Pre-chat: email + topic]
    C --> D{Single Contact match?}
    D -- yes --> E{Traveler accepts OTP?}
    E -- yes --> F{OTP pass?}
    D -- no/multi --> G[Route unverified, priority 5]
    E -- no --> G
    F -- no/timeout --> G
    F -- yes --> H[Route verified - Summit = priority 1]
    G --> I[Queue per topic]
    H --> I
    I --> J{Agent accepts <=30s?}
    J -- no --> K[Re-push next agent / wait in queue]
    K --> J
    J -- yes --> L[Conversation - Case linked per 5.1]
    L --> M{Transfer needed?}
    M -- yes --> N[New AgentWork, same session] --> L
    M -- no --> O[Wrap-up: agent sets disposition, ends session]
    O --> P[Post-chat survey]
    I -.->|VIP >60s or queue >5min| Q[Supervisor alert + callback offer]
    L -.->|customer inactive 30 min| O
```

## 6. Data Model

### 6.1 Case-creation failure handling

If the record-triggered flow fails, the failure is logged to the integration log (7.2) and the session continues — chat service is never blocked by Case creation. The agent console shows a "No Case linked" banner with a one-click quick action to create and link the Case manually. A scheduled hourly report of sessions older than 15 minutes with no Case alerts the platform team channel; more than 3 flow failures in an hour pages the platform lead. R-05 is proven by the daily exception report "MessagingSessions without Case" (target: zero rows after manual remediation).

### 6.2 Data relationships

```mermaid
erDiagram
    Contact ||--o{ Case : "has (verified linkage only, 9.2)"
    Case }o--|| Booking__c : "lookup (verified sessions only)"
    Case ||--o{ MessagingSession : "CaseId lookup, set by Case-linking flow"
    MessagingSession ||--o{ AgentWork : "one per routing attempt"
    MessagingSession ||--o{ Integration_Log__c : "optional lookup"
    MessagingSession {
        id CaseId "set by flow per 5.1"
        boolean Follow_Up__c "true when attached to existing Case"
        string Verified_Via__c "OTP | Agent | null"
        datetime VIP_Routed_At__c "flow-stamped"
        datetime VIP_Accepted_At__c "flow-stamped"
    }
    AgentWork {
        datetime RequestDateTime "push"
        datetime AcceptDateTime "null if timed out or declined"
        datetime CloseDateTime "wrap-up"
    }
```

Sources of truth: the **MessagingSession → Case lookup** is the only session-to-Case relationship (no junction object; none is needed). Contact association lives on the Case and is written only by the 9.2 verification paths. All custom fields live on MessagingSession and are written only by the routing/verification flows — reports read them, never write them. AgentWork is platform-managed; the design adds no fields to it.

## 7. Integration Design

During a chat, agents can look up live booking details from the TravelPort reservation system from the console. Synchronous was chosen over asynchronous because the agent needs the answer within the conversation turn and projected volume (A-01) is well under the API's rated capacity. Assumption A-03 (contract reuse) will be validated by a contract test against the TravelPort sandbox during build week 1; if it fails, the existing console API contract is extended before UAT.

### 7.1 TravelPort lookup sequence

```mermaid
sequenceDiagram
    participant AG as Agent console (SF admin team)
    participant AP as Apex lookup service (platform team)
    participant NC as Named credential (platform team)
    participant TP as TravelPort API (vendor)
    participant IL as Integration log (platform team)
    AG->>AP: Lookup(bookingRef) — verified sessions only (9.2)
    AP->>NC: Authenticated request
    NC->>TP: GET booking (5s timeout)
    alt success
        TP-->>NC: Booking payload (ack)
        NC-->>AP: Response
        AP-->>AG: Render booking panel
        AP--)IL: Log success (async)
    else timeout or error
        AP->>NC: One automatic retry (5s timeout)
        alt retry succeeds
            NC-->>AP: Response
            AP-->>AG: Render booking panel
            AP--)IL: Log retried-success (async)
        else retry fails
            AP-->>AG: Error banner + "retry" action
            AG->>AG: Agent falls back to TravelPort portal (manual)
            AP--)IL: Log failure (async)
        end
    end
```

Every step's owner is annotated; the trust boundary is crossed only at the named credential, server-side. The customer never waits on this call — it is agent-initiated and the conversation continues regardless of outcome.

### 7.2 Integration log object

`Integration_Log__c`: `Timestamp`, `System` (TravelPort / CaseFlow / Contract / OTP), `Operation`, `Status` (success / retried-success / failure / reject), `ErrorCode`, `Detail` (no customer PII beyond record ids), optional `MessagingSession` lookup. Owner: platform team. Reviewed weekly (7.1) and monitored hourly (6.1, 10.3). Retention: 12 months, purged by the same scheduled framework as 9.1 with the same failure alerting.

## 8. Reporting

One routing attempt = one AgentWork; a session can have several (push timeout, transfer). **Wait is measured per session, not per attempt**:

| KPI | Source | Definition | Owner / cadence |
|---|---|---|---|
| Average wait time | MessagingSession + accepting AgentWork | `AcceptDateTime` of the **accepted** AgentWork − session start. Never-accepted sessions excluded here, counted below. | Service Ops / daily |
| Never-accepted / abandoned | MessagingSession | Sessions with no accepted AgentWork; duration (end − start) and whether any push was attempted. | Service Ops / daily |
| Handle time | AgentWork | `CloseDateTime − AcceptDateTime` per accepted AgentWork; a transferred session contributes one interval per accepting agent. | Service Ops / daily |
| Chats per agent | AgentWork | Accepted-and-closed AgentWork per agent per day. | Service Ops / daily |
| VIP 60-second attainment (R-03) | MessagingSession | `VIP_Accepted_At__c − VIP_Routed_At__c ≤ 60s`, weekly % against the 95% objective; never-accepted Summit sessions count as breaches. | Service Ops / weekly |
| Follow-up ratio | MessagingSession | `Follow_Up__c` true vs. false (5.1). | Service Ops / weekly |
| CSAT | Post-chat survey (existing tool) | Existing survey score, chat channel filter. | CX team / weekly |

**R-02 (30% phone-volume reduction)** proof contract: source — Support Operations scorecard; owner — Director of Support Operations; baseline — trailing 3-month booking-change call volume ending the month before launch; measurement — monthly for six months post-launch. The chat layer contributes adoption volume (sessions by topic).

## 9. Security

### 9.1 Access, retention, and sensitive data (decisions and owners)

- **Transcript access:** limited to the "Chat Service" permission set (chat-certified agents and service supervisors), granted via permission set group, reviewed quarterly by the Salesforce admin team. No portal or marketing access.
- **Retention:** MessagingSession and ConversationEntry data retained **24 months**, then deleted by a scheduled purge job, per Data Retention Policy DR-7 (owner: Director of Support Operations, Legal sign-off recorded on DR-7). Purge-job failure alerts the Salesforce admin team and is re-run per the documented job-recovery procedure; a monthly report confirms no data older than the retention window (Section 11 test row).
- **Unsolicited sensitive data:** agents flag the session via the "Sensitive data" quick action; a supervisor redacts within one business day. **Redaction mechanism is verified, not assumed:** the build-week-1 sandbox test confirms the supervisor procedure (redact/annotate the entry and record the action on the Case) against the actual transcript data model; if entry-level redaction proves unsupported, the fallback control — restricted access (this section), 24-month purge, and incident process — is the accepted interim, per the Head of Security's 2026-07-18 risk acceptance, revisited at the 6-month review.
- **Payment flow:** agents direct payment to the secure portal flow; payment is never taken in chat.

### 9.2 Identity verification (sequenced before routing)

Verification happens **in pre-chat, before the work item exists** (sequence diagram in v4 retained):

- **Pass →** Contact and Case linked, `Verified_Via__c = OTP`, Summit priority applies at routing.
- **Fail, timeout (60 seconds, one retry), decline, no match, or multi-match →** the session routes immediately as unverified at priority 5. Priority is never changed retroactively; mid-chat manual verification (existing phone procedure; `Verified_Via__c = Agent`) links data but does not re-route, and such sessions are excluded from R-03 attainment.
- **Signed results:** the OTP outcome enters Salesforce only as the signed `otpResult` contract field (3.2), validated server-side.
- **Correction and audit:** every linkage records method and actor (`Verified_Via__c`, Case field history); mislinks are corrected by unlink/relink with history preserved.

## 10. Deployment

### 10.1 Phased rollout

Week 1–2: the launcher is shown to 10% of portal sessions via the portal feature-flag service. Gate review at end of week 2 against the Section 10.3 health thresholds, decided jointly by the Service Operations manager and platform lead. On pass, ramp to 100%; on fail, hold at 10% or roll back. Marketing announces **after** the gate passes.

### 10.2 Rollback and degraded behavior

Rollback = feature flag off: the launcher disappears from new portal sessions immediately; in-flight chats finish; the portal falls back to the case web form. Rollback owner: Service Operations manager with the platform lead; decision window: first 4 weeks. Launcher initialization failure renders nothing (portal unaffected). **Feature-flag service failure fails closed** — the launcher defaults to hidden when the flag cannot be read, so a flag outage can never expose chat prematurely. OTP service outage → pre-chat skips the verification offer; sessions route unverified (degraded but functional).

### 10.3 Production health model

| Signal | Source | Threshold | Alert / owner |
|---|---|---|---|
| Session-creation failures | Deployment/API logs | > 5 per hour | Slack #chat-ops → platform lead |
| Case-flow failures | Integration log (6.1) | > 3 per hour | Page platform lead |
| Contract rejections (3.2) | Integration log | > 5 per hour | Slack #chat-ops → web team + SF admin (possible breaking release) |
| OTP verification errors | Portal OTP service logs | > 10% of challenges over 1 hour | Slack #chat-ops → web team |
| No-accept rate | AgentWork declined/timed-out % | > 20% over 30 min | Slack #chat-ops → Service Ops manager |
| TravelPort error rate | Integration log | > 10% of lookups over 1 hour | Slack #chat-ops → platform team |
| Queue wait | Oldest waiting chat | > 5 min (4.4) | Supervisor alert (existing) |

**Alert-path resilience:** all Slack alerts also write rows to the ops dashboard (dual-write), and a weekly synthetic test alert verifies Slack delivery — a Slack outage degrades alert latency, not visibility. The support team is trained the week prior to the 10% launch.

## 11. Testing

| Req / area | Test approach | Acceptance criterion |
|---|---|---|
| R-01 | End-to-end chat on portal for both topics | Session created, routed per 4.1, Case per 5.1/6.1 |
| R-03 | Verified-Summit chats at A-01 volume, incl. forced first-push timeout | ≥ 95% ≤ 60s from `VIP_*` fields; breach alert + callback fire; timed-out-then-accepted measured |
| R-04 | Verified booking lookup + forced timeout + forced retry-fail | Data displayed; banner + manual fallback; integration log rows per 7.1 |
| R-05 | Every chat + forced Case-flow failure + zero/one/multiple recent-Case scenarios | Exactly one Case per 5.1 table; banner + quick action; exception report catches gaps |
| R-06 | Chat at 5:59am and 8:01pm MT | Launcher hidden; case web form offered |
| R-07 | Dashboard review after test week | All Section 8 KPIs populated, incl. never-accepted |
| Lifecycle (5.2) | After each end condition (customer close, agent end, inactivity), traveler returns and starts a chat | New `MessagingSession.Id` ≠ prior; prior session remains ended; contingency path documented if not |
| Identity (9.2) | OTP pass / fail / timeout / decline / no match / multi-match / manual verification / OTP outage | Correct priority, linkage, `Verified_Via__c`, R-03 inclusion per 9.2 |
| Contract (3.2) | Each supported payload variant + malformed / bad signature / stale / unknown version | Valid variants route correctly; invalid route unverified to Bookings with `contract_reject` logged |
| Operations | Feature-flag outage; Slack alert failure; purge-job failure; rollback while chats are routing | Flag fails closed; dashboard rows persist + synthetic alert catches Slack loss; purge failure alerts and re-runs; in-flight chats finish, no new sessions |
| Redaction (9.1) | Supervisor redaction procedure on sandbox transcript | Entry redacted/annotated and action recorded, or fallback control documented and accepted |

QA executes these in the partial sandbox; two team leads perform UAT against the same table.
