# Formal Review Packet — UX-001

**For the accountable senior architect. Start here. Your review material is in this folder; the full audit trail is in [history/](history/).**

- **Design under review:** [northstar-sdd-draft-v2.md](northstar-sdd-draft-v2.md) (v2 — the version that earned the ready verdict)
- **Ready verdict:** [UX-001-review-round-02.md](UX-001-review-round-02.md) — *Ready for Formal Review with Open Decisions* (2026-07-19, review round 2)
- **Current requirements:** [northstar-requirements.md](northstar-requirements.md) (R-01–R-08; unchanged from initial submission)
- **Current decision register:** [northstar-assumptions-open-decisions-v2.md](northstar-assumptions-open-decisions-v2.md) (OD-01 closed; OD-03 partially narrowed)
- **Your decision form:** [UX-001-formal-decision-FORM.md](UX-001-formal-decision-FORM.md) — administrative fields pre-filled; complete the Decision, Rationale, and Signature yourself, then save it as `UX-001-formal-decision.md` in `../../output/UX-001/`

## Open decisions requiring your judgment

1. **OD-02 — Transcript attachment:** whether chat transcripts should be attached to the Case as files or referenced only via MessagingSession. (Context: [northstar-assumptions-open-decisions-v2.md](northstar-assumptions-open-decisions-v2.md); design data model in [northstar-sdd-draft-v2.md](northstar-sdd-draft-v2.md) Section 7.)
2. **OD-03 residual — Proactive invitation wording and page targeting:** duration (5 minutes) and client-side expiry enforcement are designed in Section 6.1; final invitation copy and exact page-targeting rules remain with the e-commerce team. (Context: [northstar-sdd-draft-v2.md](northstar-sdd-draft-v2.md) Section 6.1; [northstar-assumptions-open-decisions-v2.md](northstar-assumptions-open-decisions-v2.md).)
3. **Owner-continuity tradeoff vs R-05:** whether preferred-agent routing to the Case owner (Section 5.2, 30-second bound, queue fallback with Case context) is still worth operational complexity at current staffing versus always queue-routing with Case context — R-04 requires "someone with their case context," which the fallback path alone can satisfy. (Context: [UX-001-review-round-02.md](UX-001-review-round-02.md); [northstar-sdd-draft-v2.md](northstar-sdd-draft-v2.md) Section 5.2.)

## Suggested reading order

1. This cover sheet
2. [UX-001-review-round-02.md](UX-001-review-round-02.md) — the verdict, the resolution check, and the open decisions
3. [northstar-sdd-draft-v2.md](northstar-sdd-draft-v2.md) — the design itself
4. [northstar-assumptions-open-decisions-v2.md](northstar-assumptions-open-decisions-v2.md) — open and closed decisions
5. [UX-001-formal-decision-FORM.md](UX-001-formal-decision-FORM.md) / [formal-decision-template.md](formal-decision-template.md) — record and sign your decision

## Audit trail — [history/](history/) (consult only as needed)

One earlier review round (verdict trajectory: Revise ×1 → Ready with Open Decisions), one per-finding response log ([history/UX-001-revision-response-round-01.md](history/UX-001-revision-response-round-01.md)), superseded draft v1 ([history/northstar-sdd-draft-v1.md](history/northstar-sdd-draft-v1.md)), and prior decision register ([history/northstar-assumptions-open-decisions.md](history/northstar-assumptions-open-decisions.md)). Full transition history: [reviews/UX-001-routing-log.md](../../../reviews/UX-001-routing-log.md).

---

*This packet summarizes and points; it is not a recommendation. The approval decision is yours alone — the editor's verdict measures document readiness, not architecture approval.*
