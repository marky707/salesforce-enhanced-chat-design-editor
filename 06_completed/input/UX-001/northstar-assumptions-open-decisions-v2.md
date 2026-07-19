# Northstar Migration — Assumptions and Open Decisions

## Version 2

<!-- FICTIONAL DEMO DOCUMENT. Revision aligned with northstar-sdd-draft-v2.md / UX-001 round 01. -->

## Assumptions

- A-01: Current chat volume (~900/week) grows no more than 20% after adding the mobile channel in year one.
- A-02: The 14 existing chat agents will handle both web and in-app conversations without headcount change.
- A-03: The mobile app team can include the messaging SDK in a scheduled release without delaying the migration.
- A-04: Spanish-language coverage continues with the current four bilingual agents.
- A-05: Omni-Channel preferred-agent push supports a 30-second accept timeout for Case-owner continuity routing (Section 5.2 of the SDD).
- A-06: Web team can implement proactive invitation client-side expiry (5 minutes) on support pages for `ES-Web-Support`.

## Open decisions

- OD-01: **Closed (2026-07-19).** Pro Gear uses a dedicated queue for launch (not skills-based routing). Skills-based routing may be revisited post-launch if skill combinations justify it. Decision owner: Support operations. Documented in SDD Section 5.1.
- OD-02: Whether chat transcripts should be attached to the Case as files or referenced only via MessagingSession.
- OD-03: **Partially closed.** Invitation **duration** (5 minutes) and **enforcement** (client timer + reject stale activation) are defined in SDD Section 6.1. **Final wording** and **exact page-targeting rules** for the proactive invitation remain open with the e-commerce team.
