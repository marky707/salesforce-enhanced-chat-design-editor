# Solstice Adventures — Enhanced Web Chat Implementation

## Solution Design Draft — v1

Author: P. Okafor, Salesforce Administrator Status: Draft for review

## 1. Executive Summary

Solstice Adventures, an adventure travel booking company, will add live chat to its customer portal using Salesforce Enhanced Chat (Messaging for In-App and Web). This is a new implementation — Solstice has never offered chat. The goal is to deflect phone volume for booking changes and claims questions and to give VIP travelers a premium support experience.

## 2. Requirements

See `solstice-requirements.md` (R-01 through R-07).

## 3. Proposed Architecture

Enhanced Chat will be added to the customer portal via an Embedded Service deployment. A custom LWC chat launcher will replace the standard chat button so the launcher matches Solstice brand guidelines and can display seasonal promotions. Mobile app chat is a future phase.

Pre-chat will collect the traveler's email and topic (Booking Change, Claim, Other). The overall routing design is shown in the routing diagram in Appendix A.

## 4. Routing Design

Routing will be skills-based so agents can serve multiple topics. Booking changes go to the Bookings team and claims questions go to the Claims team. Agents who are not yet certified on a topic remain in the general queue. VIP travelers (Summit tier) will be handled with urgency.

Omni-Channel will push chats to available agents based on capacity.

## 5. Conversation Lifecycle

A conversation starts when the traveler submits the pre-chat form. Sessions close automatically when inactive. Travelers can start a new chat at any time from the portal.

## 6. Data Model

Each chat creates a Case, and the chat is linked to the traveler's booking record (Booking__c) so agents have context. Contact matching uses the pre-chat email.

## 7. Integration Design

During a chat, agents can look up live booking details from the TravelPort reservation system. The lookup calls the TravelPort API synchronously and displays results in the console.

## 8. Reporting

Leadership dashboards will show CSAT, average response time, and chats per agent, refreshed daily.

## 9. Security

Chat is available to any portal visitor without login. Sensitive payment details shared in chat will be masked. Transcripts are visible to the service team.

## 10. Deployment

The chat feature will go live for all portal users on the launch date, announced by marketing. The support team will be trained the week prior.

## 11. Testing

QA will test all scenarios before launch, and two team leads will perform UAT.
