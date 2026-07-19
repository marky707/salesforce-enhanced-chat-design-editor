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

## Metric definition discipline

Every KPI must name: **source object, fields, and the two lifecycle events that bound it.** Common ambiguities the editor should catch:

| Metric | The ambiguity |
|---|---|
| Wait time | Session creation → agent joins? AgentWork created → accepted? Queue entry → first agent message? All different numbers. |
| Abandonment | Ended before routing? Before acceptance? Before first response? Does after-hours count? |
| Handle time | Accept → session end? Accept → agent close? Does async idle time between messages count? For resumed conversations, per-session or per-conversation? |
| First response time | From session creation or from routing? Does an auto-response count as a response? |
| Transfer rate | AgentWork count per session > 1 — but declines and push timeouts also create records. Are they transfers? |

A design that names a metric without resolving its ambiguity has a Proof finding.

## MessagingSession vs. AgentWork as reporting source — a major decision

Choosing the reporting source is a documented tradeoff, not an accident of report-building: session-based reporting sees conversations (including never-routed ones) but not per-attempt agent behavior; AgentWork-based reporting sees agent performance but multiplies on transfers and misses never-routed demand. Ready designs choose per metric, and say so.

## Migration reporting continuity

Legacy Chat metrics came from LiveChatTranscript and its events. Every migrated KPI needs an explicit mapping: old definition → new object/fields → whether the number is comparable. "Same dashboard, new data source" without remapping is a High finding — success against baseline cannot be measured.
