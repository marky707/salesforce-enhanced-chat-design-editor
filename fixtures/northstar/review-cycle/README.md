# Northstar Review Cycle

A reusable, end-to-end example of the editor's core learning loop:

```text
flawed draft → specific critique → pre-authored fictional response and revision → re-review → ready for human judgment
```

This example shows how the editor improves a design without becoming its author. It stops at document readiness; it does not include or imply formal architecture approval.

## Provenance and boundaries

- Northstar, its organization, requirements, design, and people are fictional.
- These five artifacts are preserved verbatim from the repository's `UX-015` demo run; only their filenames were simplified for reading order.
- `J. Rivera` is a fictional demo persona. The repository does not independently establish who wrote the canned response or revised SDD, so this example describes them as **pre-authored fictional artifacts**, not verified human-authored work.
- The editor produced the two review artifacts. The response and revised SDD were submitted as inputs for the next round; the editor did not generate them during either review.
- No formal decision, signature, approval, routing ledger, or completion artifact is included.

## Read in this order

| Step | Artifact | What to observe |
|---|---|---|
| 1 | [`01-northstar-sdd-v1.md`](01-northstar-sdd-v1.md) | A short draft with realistic routing, deployment, data, and reporting weaknesses |
| 2 | [`02-editor-review-round-01.md`](02-editor-review-round-01.md) | Five prioritized findings anchored to exact evidence, with consequences and author-owned tasks |
| 3 | [`03-pre-authored-fictional-response.md`](03-pre-authored-fictional-response.md) | One disposition per finding, locations changed, and explanations in the fictional author's voice |
| 4 | [`04-northstar-sdd-v2.md`](04-northstar-sdd-v2.md) | The submitted revision that attempts to resolve the findings and proactively address deferred areas |
| 5 | [`05-editor-review-round-02.md`](05-editor-review-round-02.md) | Resolved findings acknowledged without re-litigation; remaining judgment calls routed forward as open decisions |

## What the cycle demonstrates

- The editor identifies specific defects instead of returning generic advice.
- It explains why each weakness matters but does not supply replacement design content.
- The author may resolve, partially resolve, or disagree with each finding.
- A later round reads the response first and evaluates the submitted revision against the prior findings.
- The editor converges: once material readiness gaps are resolved, it stops sending the document back merely because more questions could be asked.
- `Ready for Formal Review with Open Decisions` means the document is ready for accountable human judgment—not that the architecture is approved.

## Reuse the pattern

For another design, preserve the same separation of responsibilities:

1. Submit the draft and supporting material to the editor.
2. Give the critique to the document's author.
3. Have the author revise the document and disposition every finding.
4. Resubmit the response and revised document together.
5. Let the editor acknowledge resolved findings, re-anchor unresolved ones, and inspect new or changed content at the same materiality bar.

The portable editor instructions are in [`../../../02_editor-review/README.md`](../../../02_editor-review/README.md).
