# Morrow Peak Unseen Evaluation

A compact second demonstration that tests whether the portable editor generalizes beyond the Northstar examples.

## What was evaluated

[`morrow-peak-sdd-draft.md`](morrow-peak-sdd-draft.md) is a fictional Salesforce Enhanced Chat and Omni-Channel design for a public support site and authenticated customer portal. Codex authored the synthetic input before the evaluation with a risk profile distinct from Northstar. No Morrow Peak expected review, golden answer, response, or revision was written.

The isolated reviewer received only:

- the portable editor's `README.md`, `identity.md`, `rules.md`, and `examples.md`;
- every Markdown file under the portable editor's `reference/` directory; and
- the Morrow Peak draft.

It did not receive repository instructions, workflow state, standalone Northstar fixture files, or any pre-authored Morrow Peak findings. `examples.md` retained its normal bundled Northstar example because it is one of the required five editor parts. The execution trace showed reads only from the copied editor bundle and the new input.

## Recorded run

- **Model:** `gpt-5.5`
- **Codex CLI:** `0.142.5`
- **Date:** 2026-07-20
- **Session:** ephemeral and non-persistent
- **Sandbox:** read-only
- **Configuration:** user configuration and execution-policy rules ignored; no Git repository context
- **Invocation:** *"Read editor/README.md, editor/identity.md, editor/rules.md, editor/examples.md, and every Markdown file under editor/reference/. Then review input/morrow-peak-sdd-draft.md for formal-review readiness. Treat this as an unseen submission. Obey the output contract in editor/rules.md completely. Critique the design; do not rewrite it, generate missing content, or approve the architecture. Return only the completed design review."*
- **Output SHA-256:** `3974077ff225027ce3b237592747f501ee4e837aa61fb821afbb7ee04fc850b5`
- **Editing:** none; [`observed-review.md`](observed-review.md) is the exact final model message.

## What the result demonstrates

The editor independently returned five evidence-anchored findings covering identity exposure, a routing-SLA contradiction, channel-specific rollback, legal-hold/privacy deletion, and undefined reporting proof. It also preserved ERP duplicate/retry behavior and after-hours acknowledgment as likely next-round findings rather than exceeding the five-finding cap.

Every finding names an exact location and passage, explains the consequence, and returns a focused problem to the author. The output contains no replacement design, generated diagram, invented implementation, or architecture approval.

This is synthetic evaluation evidence, not formal architecture approval or proof of production Salesforce behavior.
