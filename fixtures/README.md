# fixtures/ — Fictional Demo Material

Everything here is **fictional**, created to demonstrate and test the editor. Northstar is not a real company; no employer, client, or personal data appears. Fixture content never enters `reviews/` or the stage folders except when a user explicitly starts a demo run — and demo ledgers must be marked `Demo: yes`.

## Contents

- `northstar/northstar-sdd-draft-v1.md` — a flawed Legacy Chat → Enhanced Chat migration SDD, seeded with realistic weaknesses
- `northstar/northstar-requirements.md` — its requirements list
- `northstar/northstar-assumptions-open-decisions.md` — its assumptions and open decisions
- `northstar/expected-review-round-01.md` — the expected editor output for round 1 (mirrors the sample review in `02_editor-review/examples.md`)
- `northstar/review-cycle/` — a complete, reusable two-round example showing critique, a pre-authored fictional response and revision, and converged re-review

## See the full review cycle

Start with [`northstar/review-cycle/README.md`](northstar/review-cycle/README.md) to follow a flawed draft through specific critique, fictional author response, submitted revision, and a second review that reaches document readiness with open decisions. It is a general usage example, not competition-specific material and not evidence of formal architecture approval.

## Run the demo

1. Copy the three submission files (not the expected review) into `01_intake/input/NS-001/`.
2. Say: *"Start a new demo review for ID NS-001 from 01_intake/input/. Follow the routing contracts, complete every eligible automatic transition, preserve prior rounds, and stop at the next required human action."* (The agent creates `reviews/NS-001-routing-log.md` with `Demo: yes`.)
3. The package should pass intake, receive a `Revise Before Formal Review` verdict with five findings, and stop at `03_author-revision/` awaiting the author.
4. Compare the generated review with `expected-review-round-01.md` — findings should match in substance and form: exact anchors, consequences, author tasks, **no rewritten design content**.

Before and after each transition, run `python3 tools/review_state.py validate-state NS-001`. Use `preflight revision` before accepting a fictional author revision. A demo may proceed to `05_formal-review`, but an AI must not fill or simulate the signed formal decision; completion requires a real human to sign the fictional form.

## Validation use

Maintainers: run this demo after changes to rules, contracts, templates, status, or helpers. Check generic critique, replacement wording, generated diagrams, more than five findings, false approval, stale status, broken links, registry pollution, round/version drift, requirement-to-acceptance weakening, decision-index drift, and premature completion. To test revision intake, use a pre-authored canned fictional revision or a real human author submission; the editor agent does not write the design fix. Formal signature/approval may never be simulated by an AI.
