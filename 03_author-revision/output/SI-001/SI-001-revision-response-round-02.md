# Revision Response Log — SI-001 — Round 02

- **Review ID:** SI-001
- **Responding to:** `SI-001-review-round-02.md`
- **Revised document version:** v3 (`solstice-sdd-draft-v3.md`)
- **Author (human actor):** P. Okafor
- **Date (ISO 8601):** 2026-07-18

---

## Finding 1: The R-03 requirement and its acceptance criterion contradict each other

- **Disposition (mark one):** [x] resolved
- **Where the design changed:** Section 2; Sections 4.3, 8 (VIP attainment row), 11 (R-03 row); new requirements artifact `solstice-requirements-v2.md`
- **What changed / why (your own words):** I took this to the VP Customer Experience, who owns R-03, and got the requirement itself restated as a 95%-within-60-seconds service objective with mandatory breach handling. The requirements doc is now v2 with the approval noted, and routing, testing, and reporting all point at that one approved target instead of two different ones.

## Finding 2: Case-creation failure and returning-conversation behavior remain undefined

- **Disposition (mark one):** [x] resolved
- **Where the design changed:** New Sections 5.1 and 6.1; Section 11 R-05 row
- **What changed / why (your own words):** Platform team input came back. Flow failure now logs, never blocks the chat, gives the agent a banner plus a quick action to link the Case manually, and an hourly exception report catches anything missed — that report is also our R-05 proof. For returning travelers: sessions are never resumed, but verified travelers with a Case touched in the last 7 days get the new session attached to that Case instead of a duplicate, and a `Follow_Up__c` flag keeps reporting honest about first-contact vs. follow-up.

## Finding 3: A typed email still links an unverified Contact to the Case

- **Disposition (mark one):** [x] resolved
- **Where the design changed:** Section 9.1 rewritten
- **What changed / why (your own words):** Accepted — no Contact association at all before verification now, no matter how clean the match looks. Linking happens only after OTP success or after the agent runs the existing phone verification procedure manually, and every link records how it was made (`Verified_Via__c` plus Case field history), so mislinks are correctable and auditable.

## Finding 4: The revised metrics still name labels, not reproducible evidence sources

- **Disposition (mark one):** [x] resolved
- **Where the design changed:** Section 8 rewritten as a KPI table; Section 4.3 (persisted `VIP_*` timestamp fields)
- **What changed / why (your own words):** Every KPI now names its object, fields, boundary events, owner, and cadence, including how multiple AgentWork records are treated for wait vs. handle vs. counts, and a never-routed metric for sessions that die before acceptance. VIP attainment reads from timestamps the routing flow persists, not from flow memory. And the R-02 external proof contract the reviewer asked for is written into the SDD: source, owner, baseline, and six-month measurement window.

## Finding 5: The all-user launch has no operational control or recovery design

- **Disposition (mark one):** [x] resolved
- **Where the design changed:** Section 10 rewritten (10.1 phased rollout, 10.2 rollback and degraded behavior, 10.3 health model); Section 3 (launcher tradeoff)
- **What changed / why (your own words):** Launch is now 10% behind the portal feature flag for two weeks, a gate review against the health thresholds, then 100% — marketing announces after the gate, not before. Rollback is the flag turned off with named owners and a four-week window, and a failed launcher renders nothing so the portal never breaks. The health model table gives each systemic signal a threshold, an alert path, and an owner.

---

## New material introduced this round

- `solstice-requirements-v2.md` — R-03 restated with owner approval (changed supporting artifact)
- Sections 5.1, 6.1, 10.1–10.3; Section 8 KPI table with persisted VIP timestamp fields; `Follow_Up__c` and `Verified_Via__c` fields
