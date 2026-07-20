# Conversation Lifecycle & Reporting Semantics — Review Reference

The object lifecycle knowledge needed to catch reporting findings — the most common defect class in Enhanced Chat designs.

## MessagingSession — the conversation

The session record tracks the conversation from creation through end. A ready design defines, for its own configuration:

- When a session is created relative to pre-chat completion and routing
- The states it passes through (e.g. started/active, waiting, ended variants) **as the design uses them** — including inactivity handling and whether ended conversations can resume/reopen
- Who or what ends a session: customer close, agent close, inactivity timeout, business rule — and how each end type is distinguishable in data
- How the session links to Case (or other work record) and to the customer identity (MessagingEndUser → Contact)

Enhanced Chat conversations can be asynchronous: a customer can return later. Designs that assume Legacy-Chat-style "closed means finished" get lifecycle, staffing, and metrics wrong.

## AgentWork — the routing unit

AgentWork represents one routing attempt of one work item to one agent, with its own lifecycle (assigned → opened/accepted, or declined / timed out) and timestamps. Key review consequences:

- One session can have **multiple AgentWork records** (transfers, declines, re-routes). Reports counting AgentWork count routing attempts, not conversations.
- AgentWork timestamps measure the routing/acceptance window; MessagingSession timestamps measure the conversation. They answer different questions.
- Work that never routes (abandoned before routing, after-hours) may have a session but no AgentWork — invisible to AgentWork-based reports.

## MessagingSessionMetrics — response-time and message-count facts

For enhanced Messaging and Messaging for In-App and Web sessions created after September 30, 2024, Salesforce generates six `MessagingSessionMetrics` records when a session is completed. They represent:

- Average end-user response time
- Average agent response time
- Maximum end-user response time
- Maximum agent response time
- Agent message count
- End-user message count

Salesforce's reporting pattern uses a custom report type with `MessagingSession` as the primary object and `MessagingSessionMetrics` as the secondary object. The **Messaging Session Metric Type** distinguishes which of the six measures a row contains. Agent and end-user message counts are also populated on `MessagingSession` for these channels.

These records answer response-cadence and message-volume questions. Their existence does **not** define queue wait, abandonment, transfer rate, or handle time for the design. A reviewer must still require the document to name the exact object, field or metric type, population, and lifecycle meaning for every KPI rather than treating `MessagingSessionMetrics` as a generic reporting answer.

## Metric definition discipline

Every KPI must name: **source object, fields or metric type, population, and lifecycle meaning.** For derived duration metrics, the design must also name the two events that bound the clock. Common ambiguities the editor should catch:

| Metric | The ambiguity |
|---|---|
| Wait time | Session creation → agent joins? AgentWork created → accepted? Queue entry → first agent message? A `MessagingSessionMetrics` response-time row is not automatically any of these. |
| Abandonment | Ended before routing? Before acceptance? Before first response? Does after-hours count? |
| Handle time | Accept → session end? Accept → agent close? Does async idle time between messages count? For resumed conversations, per-session or per-conversation? |
| First response time | From session creation or from routing? Does an auto-response count as a response? |
| Transfer rate | AgentWork count per session > 1 — but declines and push timeouts also create records. Are they transfers? |

A design that names a metric without resolving its ambiguity has a Proof finding.

## Choosing the reporting source — a major decision

Choosing the reporting source is a documented tradeoff, not an accident of report-building:

- **MessagingSession** sees sessions, including demand that never produced an agent assignment, and carries session-level lifecycle and relationship data.
- **MessagingSessionMetrics** supplies the six completed-session response-time and message-count measures above, but not a universal definition for wait, abandonment, or handle time.
- **AgentWork** sees individual routing assignments and handle-time behavior, but multiplies on transfers/re-routes and misses demand that never routed.

Ready designs choose per metric, state the object plus field or metric type, and define the population and lifecycle boundaries that make the number meaningful.

## Migration reporting continuity

Legacy Chat metrics came from LiveChatTranscript and its events. Every migrated KPI needs an explicit mapping: old definition → new object plus fields or `MessagingSessionMetrics` metric type → population and lifecycle meaning → whether the number remains comparable. "Same dashboard, new data source" without remapping is a High finding — success against baseline cannot be measured.

## Official sources and currency

- [Report on Messaging Activity](https://help.salesforce.com/s/articleView?id=sf.messaging_reporting.htm&language=en_US) — supported reporting objects, custom report-type patterns, and KPI examples
- [Track Your KPIs with More Messaging Session Metrics](https://help.salesforce.com/s/articleView?id=release-notes.rn_messaging_session_metrics.htm&language=en_US&release=252&type=5) — six generated metric records and the October 2024 availability boundary
- [Messaging Object Model](https://developer.salesforce.com/docs/service/messaging-object-model/guide/messaging-object-model.html) — current object-model placement

Last verified against official Salesforce documentation: **2026-07-20**.
