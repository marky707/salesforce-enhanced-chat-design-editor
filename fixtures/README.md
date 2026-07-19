# fixtures/ — Fictional Demo Material

Everything here is **fictional**, created to demonstrate and test the editor. Northstar is not a real company; no employer, client, or personal data appears. Fixture content never enters `reviews/` or the stage folders except when a user explicitly starts a demo run — and demo ledgers must be marked `Demo: yes`.

## Contents

- `northstar/northstar-sdd-draft-v1.md` — a flawed Legacy Chat → Enhanced Chat migration SDD, seeded with realistic weaknesses
- `northstar/northstar-requirements.md` — its requirements list
- `northstar/northstar-assumptions-open-decisions.md` — its assumptions and open decisions
- `northstar/expected-review-round-01.md` — the expected editor output for round 1 (mirrors the sample review in `02_editor-review/examples.md`)

## Run the demo

1. Copy the three submission files (not the expected review) into `01_intake/input/NS-001/`.
2. Say: *"Start a new demo review for ID NS-001 from 01_intake/input/. Follow the routing contracts, complete every eligible automatic transition, preserve prior rounds, and stop at the next required human action."* (The agent creates `reviews/NS-001-routing-log.md` with `Demo: yes`.)
3. The package should pass intake, receive a `Revise Before Formal Review` verdict with five findings, and stop at `03_author-revision/` awaiting the author.
4. Compare the generated review with `expected-review-round-01.md` — findings should match in substance and form: exact anchors, consequences, author tasks, **no rewritten design content**.

## Validation use

Maintainers: run this demo after any change to `rules.md`, `identity.md`, or `reference/`. Deviations to check — generic critique, replacement wording, generated diagrams, more than five findings, or any implication of approval. The eight acceptance routes in the root `CONTEXT.md` stage table can all be exercised from this package by simulating the author's and reviewer's actions.
