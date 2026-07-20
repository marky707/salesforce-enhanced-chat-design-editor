# Morrow Peak Equipment — Enhanced Chat Solution Design

> Fictional evaluation fixture. Morrow Peak Equipment, its requirements, systems, and people are invented for this repository.

- **Document version:** 0.1
- **Author:** A. Chen, Salesforce Administrator (fictional persona)
- **Status:** Draft for architecture-readiness review

## 1. Purpose and context

Morrow Peak Equipment provides maintenance contracts for commercial landscaping equipment. It wants to replace a basic website contact form with Salesforce Enhanced Chat on the public support site and authenticated customer portal. Fourteen service coordinators and six certified equipment specialists work from one Service Cloud org.

Customers currently call for service-order status, warranty questions, and equipment troubleshooting. Service-order data is mastered in the RidgeLine ERP platform. Salesforce stores Accounts, Contacts, Assets, Cases, and contract tier.

## 2. Requirements

| ID | Requirement |
|---|---|
| R-01 | Anonymous public-site visitors may receive generic support, but no account, asset, contract, or service-order information until their identity is verified. |
| R-02 | Authenticated portal customers should begin with their Account, active Assets, and open service-order context available to the assigned agent. |
| R-03 | During support hours, Priority contract customers must reach a certified equipment specialist within 90 seconds. |
| R-04 | A chat may request current service-order status from RidgeLine ERP without creating duplicate ERP inquiries or exposing another customer's order. |
| R-05 | Outside support hours, capture the customer's intent and contact preference and acknowledge a next-business-day response. |
| R-06 | Retain chat transcripts for 12 months, preserve records under legal hold, and honor approved privacy-deletion requests. |
| R-07 | Release public-site chat first and authenticated-portal chat two weeks later, with a channel-specific rollback option. |
| R-08 | Operations needs weekly measures for first response, Priority-contract routing, identity failures, after-hours capture, and ERP lookup success. |

Support hours are Monday–Friday, 06:00–18:00 Mountain Time, excluding company holidays.

## 3. Proposed architecture

One Enhanced Chat deployment will serve the public support site and customer portal. Both entry points start the same Omni-Channel Flow. The flow identifies the customer, retrieves relevant service context, selects a routing target, and creates or links a Case.

```text
Public support site ─┐
                     ├─> Enhanced Chat deployment ─> Omni-Channel Flow ─> Agent / specialist
Customer portal ─────┘                         │              │
                                              │              └─> RidgeLine ERP API
                                              └─> MessagingSession ─> Case
```

The Digital Support team owns the Embedded Service configuration and Omni-Channel Flow. The ERP team owns the RidgeLine endpoint. Service Operations owns queues, skills, presence statuses, and staffing.

## 4. Customer identity and context

The public pre-chat form asks for name, email address, equipment serial number, and reason for contact. The portal wrapper passes the signed-in user's email and Account number. Both channels use the same matching subflow so customers receive a consistent experience.

The subflow looks up Contact by email. If one Contact matches, the flow treats the customer as identified and retrieves the Contact's Account, active Assets, contract tier, and three most recent service orders. This context appears in the agent's utility panel. If no Contact matches, the flow creates a new Contact and continues without service-order history. If multiple Contacts match, it uses the most recently modified record.

Portal sessions normally include a signed portal user ID. If that value is absent or cannot be resolved, the flow falls back to the email-matching behavior so the customer is not blocked from support. Agents may share service-order status as soon as the context panel loads.

## 5. Routing and capacity

Standard customers route to the Service Coordination queue using most-available routing. Spanish-language chats require the `Spanish Support` skill.

Priority contract customers route directly to the available user with the highest `Certified Equipment Specialist` proficiency. Priority work uses routing priority 1; Standard work uses priority 5. If no certified specialist is available, the work remains pending until one becomes available so R-03 is not diluted by sending it to a general coordinator.

Specialists may transfer a chat to Service Coordination after diagnosing the equipment issue. The receiving coordinator inherits the Case and transcript context. Supervisor dashboards show open work by queue and agent.

## 6. RidgeLine ERP integration

At session start, the Omni-Channel Flow calls the RidgeLine `GET /service-orders` endpoint using the equipment serial number and email address. The response supplies service-order number, status, scheduled technician, and appointment window. The returned values are displayed in the agent utility and summarized in the Case description.

If RidgeLine times out, the flow retries the request up to three times. Agents can also press **Refresh Order Status**, which runs the same request again. The integration uses a named credential owned by the ERP integration user. RidgeLine writes every request to its existing API log.

If all retries fail, the chat still routes to an agent and the utility displays `Order status unavailable`. The agent may ask the customer to wait while trying Refresh again.

## 7. Conversation lifecycle and after-hours behavior

During support hours, the session enters routing immediately after the pre-chat and context steps. An agent closes the Case when the issue is resolved and ends the MessagingSession from the service console.

Outside support hours, the same flow places the work in the Service Coordination queue. The customer can type the issue and contact preference, then close the browser. Coordinators review the queue the next morning and respond to the customer using the information in the transcript.

An inactivity timeout ends a session after 30 minutes without a customer message. A customer who returns later starts a new session and the agent can search for the prior Case.

## 8. Data, privacy, and retention

MessagingSession relates to the Case created or selected during the flow. The Case description stores the latest ERP service-order summary so agents can see it after the chat ends. Transcript bodies remain in Salesforce and are available to service coordinators, specialists, supervisors, and administrators.

A nightly scheduled flow deletes MessagingSession records whose end date is more than 12 months old. Legal places a `Legal Hold` checkbox on the related Case when preservation is required. Privacy-deletion requests are completed by deleting the Contact and associated Cases through the existing privacy process.

The solution does not store payment information. Customers who need to pay an invoice receive a link to the RidgeLine payment portal.

## 9. Reporting and operations

Operations dashboards use MessagingSession and Case report types to show average first response, sessions by contract tier, identity-match failures, after-hours chats, and ERP lookup success. Contract tier and ERP outcome are written to fields on MessagingSession for reporting.

Supervisors review the dashboard each Monday. Digital Support monitors Omni-Channel Flow errors and the ERP team monitors its API log. A shared support channel is used to coordinate incidents.

## 10. Release and rollback

Week 1 enables the deployment on the public support site. Week 3 adds the same deployment to the authenticated portal wrapper. Digital Support promotes the flow and deployment configuration through the normal sandbox-to-production change set process.

If chat causes a production issue, Digital Support deactivates the Enhanced Chat deployment and restores the public contact form. The portal support link is hidden in the next portal configuration release. Existing Cases remain available for agents.

## 11. Verification

UAT will cover one anonymous customer, one authenticated portal customer, one Standard customer, one Priority customer, one Spanish chat, one ERP response, one ERP timeout, and one after-hours chat. Testers confirm that the correct agent receives the chat, service-order context appears, the Case is related, and dashboard records are created.

Service Operations approves routing and dashboard results. Digital Support approves deployment behavior, and the ERP team approves the API response. Open defects are recorded in the implementation backlog before production release.
