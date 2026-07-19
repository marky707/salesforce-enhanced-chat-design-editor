# Solstice Enhanced Chat — Assumptions and Open Decisions — v3

<!-- FICTIONAL TEST DOCUMENT.
     v3 corrects a transcription error in v2: A-03 was accidentally replaced with an
     assumption from an unrelated document. The intended A-03 — TravelPort contract
     reuse, unchanged since v1 — is restored below. No assumption has ever
     intentionally changed; v2's OD-02 disposition is retained. v2 is superseded
     but preserved unmodified for the audit trail. -->

## Assumptions (unchanged from v1)

- A-01: Expected volume is 400–600 chats/week at launch, based on current call topics.
- A-02: Eight service agents will be chat-certified at launch; four more within 90 days.
- A-03: The TravelPort API contract in place for the agent console can be reused for chat-time lookups. *(Validated per SDD Section 7: build-week-1 contract test, with the console-contract extension as fallback.)*
- A-04: Summit-tier status is already available on the Contact record.

## Open decisions

- OD-01: Whether Claims topic routing must require a claims-licensed agent skill. **Open — reserved for the accountable senior architect at formal review.**

## Dispositioned decisions

- OD-02: Chat launcher placement (floating vs. header). **Architecture impact closed 2026-07-19** — the launcher loads the same deployment and sends the same Contract v1.0 regardless of position (SDD Section 3). Remaining scope is UX-only, owned by the e-commerce team. Reopening condition: a placement requiring markup or load-order changes that affect launcher initialization re-enters design review.

## Corrections

- 2026-07-19: v2's A-03 contained a transcription error (an assumption pasted from an unrelated document). No change to A-03 was ever intended; the SDD's use of A-03 as the TravelPort contract-reuse assumption is and was correct. v3 restores the intended text; v2 is preserved unmodified.
