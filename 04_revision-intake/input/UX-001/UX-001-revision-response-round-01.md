# Revision Response Log — UX-001 — Round 01

## How to fill this out (takes ~10 minutes after you've revised your document)

For **each finding** below, answer three things:

1. **Disposition** — mark one: `resolved` / `partially resolved` / `disagree`
2. **Where** — the section, table, or diagram of your revised document that changed (or "no change" if you disagree)
3. **Why** — 2–3 sentences **in your own words**. Plain language is fine; you are explaining, not writing a formal document. If you disagree, say why — disagreement is allowed when you argue it from a requirement or constraint.

Do this **after** you've finished revising. Every finding must have a block, including ones you disagree with. Honesty beats polish: "I couldn't resolve the Case-failure part yet, need platform team input" is a *good* answer.

**Tip:** the review's *Deferred Review Areas* section is a preview of likely future findings. Addressing those items in this same revision usually saves you a full review round — note anything you tackled under "New material introduced this round."

**If you changed a supporting artifact** (requirements list, assumptions/decisions register): give it a new versioned filename, list it under "New material introduced this round," and **re-read it once against your revised SDD before submitting** — the most common resubmission failure is a supporting artifact that quietly disagrees with the SDD or with this log (e.g. text pasted from the wrong document, or a register still calling "open" a decision your SDD closed). Revision intake cross-checks all three and will bounce a contradictory package.

- **Review ID:** UX-001
- **Responding to:** `UX-001-review-round-01.md`
- **Revised document version:** v2 (`northstar-sdd-draft-v2.md`)
- **Author (human actor):** J. Rivera
- **Date (ISO 8601):** 2026-07-19

---

## Finding 1: Direct-to-owner routing has no availability, timeout, or fallback behavior

- **Disposition (mark one):** [x] resolved  [ ] partially resolved  [ ] disagree
- **Where the design changed:** Section 5.2 rewritten as "Returning customer (owner) routing — availability, timeout, fallback"; capacity/push defaults in Section 5.4; R-04/R-05 test rows in Section 12.
- **What changed / why (your own words):** I added a hard 30-second preferred-agent push to the Case owner, and if they're offline, at capacity, OOO, or just don't accept, we fall straight to the topic queue with a Case feed note so whoever picks it up has context. That way we still aim at the 2-minute first response (R-05) instead of parking chats on an unavailable owner. R-04 is met by "someone with case context," not only the named owner — which the review called out as the broader reading.

---

## Finding 2: Language and priority routing cannot be followed as a decision sequence

- **Disposition (mark one):** [x] resolved  [ ] partially resolved  [ ] disagree
- **Where the design changed:** Section 5.1 decision table + mermaid flowchart; Section 5.3 priority mechanism; OD-01 closed in assumptions v2 (dedicated Pro Gear queue for launch).
- **What changed / why (your own words):** I wrote the actual order: business hours → language (missing = English) → topic to one of three queues (Orders / Returns / Pro Gear) → Pro-tier priority bump. Spanish isn't its own queue — if no bilingual agent is free we still put them in the topic queue and flag the Case. Priority is Omni-Channel priority 1 vs 5, not hand-wavy "answered first."

---

## Finding 3: Sections 4 and 9 contradict each other on Embedded Service deployments

- **Disposition (mark one):** [x] resolved  [ ] partially resolved  [ ] disagree
- **Where the design changed:** Section 4.1 (dual deployments + rationale); Section 9 wave table names each deployment; mobile vs web ownership in Section 8.
- **What changed / why (your own words):** We are going with **two** Embedded Service deployments (`ES-Web-Support` and `ES-Mobile-App`), not one. Web and mobile ship on different dates and need different identity/pre-chat behavior, so one shared deployment couldn't match the Week 1 / Week 3 plan. Section 4 and Section 9 now both say two deployments and the same wave timing.

---

## Finding 4: The custom Chat_Interaction__c object has no rationale against native relationships

- **Disposition (mark one):** [x] resolved  [ ] partially resolved  [ ] disagree
- **Where the design changed:** Section 7 and new 7.1 — drop Chat_Interaction__c; native `MessagingSession.CaseId`; Spanish flag only as a Case checkbox.
- **What changed / why (your own words):** I dropped the custom junction. R-07 only needs create/attach to Case, and MessagingSession already has CaseId. Building a second link would just give us two sources of truth and messier reports. Interaction detail lives on standard session/work/feed objects unless a future requirement forces something structured.

---

## Finding 5: Reporting metrics name no source objects or lifecycle boundaries

- **Disposition (mark one):** [x] resolved  [ ] partially resolved  [ ] disagree
- **Where the design changed:** Section 10 rewritten; Section 10.1 definition table for wait, abandonment, handle time, and first response; LiveChatTranscript mapping column; Section 10.2 continuity notes.
- **What changed / why (your own words):** Each KPI now names the object, the fields/formula, what starts and ends the clock, and how it maps off LiveChatTranscript. Wait and handle time are AgentWork-based; abandonment is MessagingSession with no accepted work; R-05 gets an explicit first-response definition that doesn't count bots. I also noted the baseline won't be perfectly 1:1 with Legacy so ops doesn't pretend the series is continuous without a break label.

---

## New material introduced this round

- Section 4.1 dual Embedded Service deployment topology (`ES-Web-Support`, `ES-Mobile-App`)
- Section 5.1 routing decision table + mermaid decision flow
- Section 5.2 owner 30s push + topic-queue fallback + Case context note
- Section 5.4 capacity (3) and standard 30s push timeout
- Section 6.1 proactive invitation expiry (5 min, client timer + reject stale click); web-only proactive
- Section 7.1 drop of Chat_Interaction__c; native CaseId justification
- Section 8.2 mobile wrapper ownership, payload contract, versioning
- Sections 9.1–9.2 in-flight Legacy handling, monitoring, retry, web/mobile rollback
- Section 10.1–10.2 KPI definitions with LiveChatTranscript mapping
- Section 12 requirement-to-test matrix (replaces "write tests during build")
- Supporting artifact: `northstar-assumptions-open-decisions-v2.md` (OD-01 closed; OD-03 partially narrowed)
- Requirements file unchanged: `northstar-requirements.md` (R-01–R-08)
