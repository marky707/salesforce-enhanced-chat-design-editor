# Northstar Customer Support — Legacy Chat to Enhanced Chat Migration

## Solution Design Draft — v1

<!-- FICTIONAL DEMO DOCUMENT. Deliberately seeded with design weaknesses for editor testing. -->

Author: J. Rivera, Associate Consultant
Status: Draft for review

## 1. Executive Summary

Northstar Outdoor Equipment currently supports customers through Salesforce Legacy Chat on its e-commerce website. Salesforce has announced Legacy Chat retirement, and Northstar will migrate to Enhanced Chat (Messaging for In-App and Web), extending chat to the Northstar mobile app for the first time. This document describes the target architecture, routing design, data model, and migration plan.

## 2. Requirements

See `northstar-requirements.md` for the full list (R-01 through R-08).

## 3. Current State

Legacy Chat serves the website only, with three chat buttons (Orders, Returns, Pro Gear) mapped to three agent skills. Roughly 900 chats per week are handled by 14 agents across two shifts. Reporting is built on LiveChatTranscript: weekly dashboards show average wait time, abandonment rate, and agent handle time.

## 4. Proposed Architecture

Enhanced Chat will replace Legacy Chat on the website and add in-app messaging in the Northstar mobile app. A single Embedded Service deployment will serve both the website and the Northstar mobile app. Pre-chat will collect the customer's email, topic, and preferred language. Conversations will create a Case automatically via a record-triggered flow.

Customers browsing key support pages will see a proactive chat invitation offering help.

## 5. Routing Design

### 5.1 Routing Overview

Chats will be routed based on language, product line, and customer priority to the appropriate queue. Omni-Channel will push work to available agents. Queues will mirror the current skill groups: Orders, Returns, and Pro Gear.

### 5.2 Returning Customer Routing

Returning customers with an open case will be routed directly to their case owner for continuity. This preserves the relationship the customer already has and avoids repeating context.

### 5.3 Priority Handling

Pro-tier customers are high priority and should be answered first.

## 6. Conversation Lifecycle

Sessions begin when the customer submits the pre-chat form. Proactive chat invitations presented to customers browsing the support site will expire after five minutes. Ended conversations remain visible to agents for reference. Inactive conversations will be closed.

## 7. Data Model

Conversations are recorded as MessagingSession records. A custom object Chat_Interaction__c will link each MessagingSession to its Case and store interaction details. Contact matching will use the pre-chat email address.

## 8. Integration Design

The Northstar mobile app wrapper passes the customer context at session start, including the customer identifier and current screen. The website snippet will be added to the support pages by the web team. Order lookups during a chat use the existing OrderService API that agents already use in the console.

## 9. Deployment Plan

The migration will proceed in two waves to limit risk:

| Wave | Scope | Timing |
|---|---|---|
| Week 1 | Cut over the web deployment | After business hours Friday |
| Week 3 | Cut over the mobile deployment (app release) | With app store release |

Legacy Chat will be disabled at the start of Week 1. Agent training occurs the week before each wave.

## 10. Reporting and KPIs

Dashboards will show average wait time, abandonment rate, and agent handle time. The existing weekly dashboard will be rebuilt on the new data. Supervisors will review the dashboards weekly as they do today.

## 11. Security

Chat will be available to all site visitors without login. Transcripts are stored in Salesforce and visible to the support team. The mobile app passes the customer identifier for logged-in users.

## 12. Testing

Each requirement will be tested in a partial sandbox before go-live. UAT will be performed by two senior agents. Test cases will be written during the build phase.
