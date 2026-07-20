# Salesforce Enhanced Chat Design Review Editor — Portable Editor

A critic-only design review editor for **Salesforce Enhanced Chat v1** (formerly Messaging for In-App and Web) and **Omni-Channel** Solution Design Documents. It finds the five highest-risk readiness gaps and returns them to you to solve. It will not rewrite your document, generate your diagrams, or approve your architecture.

**Who it's for:** Salesforce admins, developers, and junior consultants preparing a Service Cloud solution design for formal architecture review.

## The five parts

| File | Job |
|---|---|
| `identity.md` | Who the editor is and the limit of its authority |
| `rules.md` | Critique behavior, verdicts, and the output contract |
| `examples.md` | What acceptable critique looks like vs. generic feedback and rewriting |
| `reference/` | Salesforce domain frameworks the editor consults (see `reference/CONTEXT.md`) |
| `README.md` | This guide |

## See it work first

[`fixtures/northstar/sample-run.md`](../fixtures/northstar/sample-run.md) is an **actual, unedited review** the editor produced against a deliberately flawed demo SDD — model, date, and exact invocation recorded. Read that to see the real output before you run your own.

## What to submit

- Your draft SDD — markdown, plain text, PDF, or Word (in the pipeline, intake converts `.docx` automatically; in a Claude Project, upload the Word file directly or paste the text) — covering, ideally: requirements, architecture, routing, conversation lifecycle, integrations, data relationships, reporting, security, testing, deployment, and operational support
- Your requirements list
- Your assumptions and open decisions
- Your diagrams (exports or embedded)

A missing piece won't block the review — its absence becomes a finding.

## Standalone use — Claude Project or any capable assistant (no repository needed)

The editor is five plain markdown files — any assistant that can hold them as context works: a Claude Project, a ChatGPT Project or Custom GPT, a Gemini Gem, or a coding agent pointed at this folder. Claude Project steps shown; the pattern is identical elsewhere (upload the same files as knowledge, set the same instructions).

1. Create a Claude Project and upload: `identity.md`, `rules.md`, `examples.md`, and every file in `reference/`. **Do not upload** `CONTEXT.md` or the `input/`/`output/` folders — those are pipeline-only.
2. Set the Project instructions to: *"You are the design review editor defined in identity.md. Obey rules.md completely. Review submitted Salesforce Enhanced Chat v1 / Omni-Channel solution designs using the output contract in rules.md."*
3. Paste or attach your draft and say: *"Review this solution design for formal-review readiness."*
4. The review comes back as a chat response. Ignore any stage-routing language you encounter — in a Project there are no folders; the revision loop is simply **revise your document and submit it again**, telling the editor what changed.

## Pipeline use

Inside the full repository, this folder is stage `02_editor-review/` — packages arrive in `input/<ID>/` from intake and reviews are written to `output/<ID>/`. See the repository root `README.md` and `CONTEXT.md`; you never invoke this stage directly.

## What you'll get back

Exactly the contract in `rules.md`:

- A **verdict** — `Revise Before Formal Review`, `Ready for Formal Review with Open Decisions`, `Ready for Formal Review`, or `Insufficient Context`
- **At most five findings**, each with severity, lens (Why/Flow/Failure/Proof), exact location, quoted evidence, the design gap, its consequence, and a focused task for you
- **Open decisions** needing senior human judgment, and **deferred areas** — specific lower-priority items it will otherwise raise in later rounds; treating them as a to-do list alongside the findings usually saves you a round

The editor's goal is a **ready verdict, not endless critique**: once your revisions resolve the material gaps, remaining judgment calls travel forward to your human reviewers as open decisions — `Ready for Formal Review with Open Decisions` is a normal, successful outcome.

Compact example finding:

> **Direct-to-owner routing has no fallback** — Blocking / Failure — Section 5.2 — "Returning customers will be routed directly to their case owner." No behavior exists when the owner is offline or at capacity, so a chat can wait unbounded, invisible to queue dashboards. *Your task: when the owner can't accept within a bounded time, where does the work go, and what is the bound?*

## Why it won't rewrite your document

You are the architect. The editor's value is exposing what a formal review board would catch — while you can still fix it yourself. A document someone else repaired teaches you nothing and hides what you don't yet understand from the people accountable for approving it.

## Limitations

- Scope: Enhanced Chat v1 + Omni-Channel only. No Legacy Chat design (except as migration source), no Enhanced Chat v2, no CTI/Amazon Connect, no WhatsApp/SMS/Facebook Messenger, no generic Salesforce review, no code review.
- **"Ready for Formal Review" is document readiness, not approval.** Approval belongs to your accountable human architect and governance reviewers.
- It won't certify security or compliance, and it won't speak for Salesforce behavior beyond well-established platform behavior — unverifiable claims in your draft get flagged, not corrected.
- Five findings per pass, by design. Fix the big ones; rerun; the next tier surfaces — and the *Deferred Review Areas* list tells you in advance what that next tier is.
