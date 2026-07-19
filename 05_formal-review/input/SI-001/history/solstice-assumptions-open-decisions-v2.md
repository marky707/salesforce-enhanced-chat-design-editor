# Solstice Enhanced Chat — Assumptions and Open Decisions — v2

<!-- FICTIONAL TEST DOCUMENT. v2: OD-02 dispositioned; OD-01 remains open for the accountable architect; assumptions unchanged. -->

## Assumptions

- A-01: Expected volume is 400–600 chats/week at launch, based on current call topics.
- A-02: Eight service agents will be chat-certified at launch; four more within 90 days.
- A-03: The mobile app team can include the messaging SDK in a scheduled release without delaying the migration. *(Superseded in scope: v1 wording; chat-time reuse of the TravelPort API contract is validated per SDD Section 7.)*
- A-04: Summit-tier status is already available on the Contact record.

## Open decisions

- OD-01: Whether Claims topic routing must require a claims-licensed agent skill. **Open — reserved for the accountable senior architect at formal review.**

## Dispositioned decisions

- OD-02: Chat launcher placement (floating vs. header). **Architecture impact closed 2026-07-19** — the launcher loads the same deployment and sends the same Contract v1.0 regardless of position (SDD Section 3). Remaining scope is UX-only, owned by the e-commerce team. Reopening condition: a placement requiring markup or load-order changes that affect launcher initialization re-enters design review.
