# Revision Response Log — SI-001 — Round 03

- **Review ID:** SI-001
- **Responding to:** `SI-001-review-round-03.md`
- **Revised document version:** v4 (`solstice-sdd-draft-v4.md`)
- **Author (human actor):** P. Okafor
- **Date (ISO 8601):** 2026-07-18

---

## Finding 1: OTP verification is not sequenced before or after VIP routing

- **Disposition (mark one):** [x] resolved
- **Where the design changed:** New Section 9.2 (with sequence diagram); Section 4.1 step 3; Section 4.3
- **What changed / why (your own words):** The reviewer was right — I had verification happening mid-chat while routing needed it up front. Verification now happens in pre-chat, before the work item exists, so priority is known once and never changes. Every outcome is sequenced: pass routes as VIP, and fail/timeout/decline/no-match/multi-match all route immediately as unverified at priority 5. Mid-chat manual verification links data but never re-prioritizes, and those sessions are excluded from R-03 attainment because they were never routed as VIP.

## Finding 2: The seven-day returning-Case rule has no outcome for multiple eligible Cases

- **Disposition (mark one):** [x] resolved
- **Where the design changed:** Section 5.1 rewritten as a selection table
- **What changed / why (your own words):** The flow now handles zero, one, and multiple explicitly: it only auto-attaches when exactly one recent open Case matches the pre-chat topic. Anything ambiguous creates a new Case — never guess — and the agent gets the Recent Cases list to merge or relate afterward through the standard Case-merge procedure, which keeps the audit history.

## Finding 3: Average wait time cannot be calculated when the first push times out

- **Disposition (mark one):** [x] resolved
- **Where the design changed:** Section 8 KPI table (wait time and new never-accepted rows); Section 4.3
- **What changed / why (your own words):** Good catch — my formula measured attempts, not sessions. Wait is now session start to the AcceptDateTime of whichever AgentWork actually got accepted, however many pushes it took, so delayed sessions are measured instead of dropped. Sessions never accepted get their own metric with duration, and never-accepted Summit sessions count as R-03 breaches rather than disappearing.

## Finding 4: Transcript access, payment-data handling, and retention remain unowned

- **Disposition (mark one):** [x] resolved
- **Where the design changed:** New Section 9.1 (access, retention, sensitive data)
- **What changed / why (your own words):** Everything has an owner now: transcript access is the Chat Service permission set with quarterly review by the Salesforce admin team; retention is 24 months under policy DR-7 owned by the Director of Support Operations with Legal sign-off; pasted sensitive data gets a flag-and-redact interim control with a weekly SLA report, and the Head of Security formally accepted the residual risk of deferring automated masking, to revisit at the 6-month review. Incidents follow the existing security process.

## Finding 5: External-system and trust-boundary flows are still prose-only

- **Disposition (mark one):** [x] resolved
- **Where the design changed:** New Section 3.1 (system-context diagram with ownership notes); Section 9.2 (verification/routing sequence diagram); Section 7 (call direction clarified — server-side via named credential)
- **What changed / why (your own words):** Added the system-context diagram showing all six systems, trust boundaries, call directions, and which team owns each boundary, plus a sequence diagram for the verification-to-routing flow, which is the trickiest ordered handoff. TravelPort is now explicit that calls are server-side from Salesforce via named credential, so nothing external ever calls into the org uninvited.

---

## New material introduced this round

- Sections 3.1 and 9.2 diagrams (Mermaid, embedded in the SDD)
- Section 9.1 security decisions with named owners and acceptance record
- Section 8 never-accepted metric; Section 10.3 OTP health signal; Section 11 identity-path and multi-Case test rows
