# Salesforce Enhanced Chat Design Review Editor

An end-to-end, critic-only review workflow for **Salesforce Enhanced Chat and Omni-Channel Solution Design Documents**. Attach a draft and its supporting material in chat; the workflow validates and files the submission, identifies the highest-risk design gaps, returns them to the author to solve, checks the revision, and prepares a ready design for accountable human review.

**[View the visual portfolio →](https://marky707.github.io/salesforce-enhanced-chat-editor-portfolio/)**

> **The complete repository is the editor system.** Its numbered folders provide the intake-to-completion workflow and audit trail. Stage [`02_editor-review/`](02_editor-review/) contains the portable five-part critique engine—the interpretable-context methodology—which can also run independently in a Claude Project.

## The complete workflow

```text
Submit documents in chat
          │
          ▼
01 Intake and validation
          │
          ▼
02 Critic-only editor review ── revision needed ──▶ 03 Author revision
          ▲                                               │
          │                                               │ author submits
          └────────────── 04 Revision validation ◀─────────┘
          │
          │ ready for human judgment
          ▼
05 Accountable human review ── changes required ──▶ 03 Author revision
          │
          │ approved by the human reviewer
          ▼
06 Completed record
```

Each folder has one responsibility:

| Stage | One job |
|---|---|
| [`01_intake/`](01_intake/) | Validate, normalize, and inventory the submitted design package |
| [`02_editor-review/`](02_editor-review/) | Critique the design without rewriting it or claiming approval |
| [`03_author-revision/`](03_author-revision/) | Return prioritized findings and a response form to the author |
| [`04_revision-intake/`](04_revision-intake/) | Validate the author's dispositions, revised document, and version change |
| [`05_formal-review/`](05_formal-review/) | Assemble a focused packet for accountable human judgment |
| [`06_completed/`](06_completed/) | Preserve the approved design, decision record, and review history as read-only evidence |

## Start an end-to-end review

> **Chat is the front door.** You do not need to place files into stage folders yourself. With this repository open in Codex or Claude Code, attach the draft SDD, requirements, assumptions/open decisions, and diagrams in chat. After validation, the agent files each artifact under the correct review ID and stage, reports what it accepted or renamed, advances every eligible automatic step, and stops whenever a person must act.

1. Attach the draft and supporting material, then say **`start`**. Missing requirements, diagrams, assumptions, or evidence become specific findings; the editor does not invent them or silently fill the gaps.
2. Read the generated review and author packet. Revise the SDD yourself, disposition each finding, attach the new version and response, then say **`submit revision <ID>`**.
3. Use **`status <ID>`** for orientation and **`continue <ID>`** after a human action. The next review reads the response first, acknowledges resolved findings, and re-anchors only the issues that remain.
4. When the document is ready, an accountable human architect receives the formal packet. You may attach an already-written and signed decision for filing, but the agent will never choose, write, complete, or sign that decision.

The workflow accepts markdown, plain text, PDF, and Word. Its Python helpers use only the standard library and are run by the agent; [`tools/README.md`](tools/README.md) documents the optional CLI for maintainers.

## See the workflow improve a design

- **One-pass evidence:** the [real, unedited Northstar sample review](fixtures/northstar/sample-run.md) records the model, date, invocation, and exact critique produced from a deliberately flawed fictional design.
- **Complete feedback loop:** the reusable [Northstar Review Cycle](fixtures/northstar/review-cycle/) preserves a five-artifact sequence: flawed draft, round-one critique, pre-authored fictional response, submitted revision, and a round-two review that reaches readiness without the editor rewriting the design.
- **Unseen generalization evidence:** the [Morrow Peak evaluation](fixtures/morrow-peak/) records a fresh isolated review of a distinct fictional design with no Morrow Peak expected answer or pre-authored findings supplied to the model.
- **Maintained reference:** [`expected-review-round-01.md`](fixtures/northstar/expected-review-round-01.md) defines the substantive and structural behavior expected from the editor; outputs should match its anchors, consequences, author-owned tasks, and critic-only boundary rather than its exact wording.

## What you get back

- **One readiness verdict:** `Revise Before Formal Review`, `Ready for Formal Review with Open Decisions`, `Ready for Formal Review`, or `Insufficient Context`.
- **At most five prioritized findings:** each includes severity, review lens, exact location, quoted evidence, the design gap, its consequence, and a focused task for the author.
- **Open decisions for the senior architect:** business tradeoffs, risk acceptances, and choices requiring accountable human judgment rather than AI inference.
- **Deferred review areas:** specific lower-priority weaknesses and when they are likely to matter, so the author can address them before the next pass.

The goal is **readiness, not endless criticism**. Once the document is coherent enough for a competent builder and QA team, non-blocking judgment calls travel forward to the accountable human architect instead of forcing unnecessary revision cycles. A ready verdict measures document quality—it is never architecture or production approval.

## How the critique engine works

Every review applies **Why → Flow → Failure → Proof**:

- **Why:** Which requirement and tradeoff justify the decision?
- **Flow:** Can a builder follow actors, systems, handoffs, decisions, and state changes?
- **Failure:** What happens when routing, integrations, staffing, or session behavior fails?
- **Proof:** Which test, event, object, field, log, or metric proves the requirement was met?

Every finding must identify an exact location and quoted passage, explain the specific design gap and downstream consequence, and end with a focused problem for the author. The editor never writes replacement content, generates missing diagrams, invents requirements or implementation details, or claims architecture approval.

### The portable five-part engine

| Part | One job |
|---|---|
| [`identity.md`](02_editor-review/identity.md) | Defines the senior Salesforce editor, its audience, scope, tone, and authority boundary |
| [`rules.md`](02_editor-review/rules.md) | Defines critique behavior, convergence, prohibitions, verdicts, and the output contract |
| [`examples.md`](02_editor-review/examples.md) | Distinguishes specific critique from generic feedback and forbidden rewriting |
| [`reference/`](02_editor-review/reference/) | Supplies focused Salesforce architecture checklists and domain guidance |
| [`README.md`](02_editor-review/README.md) | Explains inputs, setup, output, and standalone use |

## Use only the portable editor in a Claude Project

The critique engine works without the surrounding workflow when folder routing and status history are unnecessary:

1. Create a Claude Project and upload `identity.md`, `rules.md`, `examples.md`, and the files under `reference/` from [`02_editor-review/`](02_editor-review/). Do not upload the folder's top-level, pipeline-only `CONTEXT.md`, `input/`, or `output/` content.
2. Attach the draft SDD and, when available, its requirements, assumptions/open decisions, and diagrams.
3. Set the Project instruction to: *"You are the design review editor defined in identity.md. Obey rules.md completely. Review submitted Salesforce Enhanced Chat and Omni-Channel solution designs using the output contract in rules.md."*
4. Ask: *"Review this solution design for formal-review readiness. Critique it; do not rewrite it."* Revise the document yourself and resubmit it with what changed.

Documents attached to a standalone Claude Project are reviewed directly in chat. Repository routing, ledgers, status cards, revision intake, formal packets, and completion history are available only with the full repository workflow. See [`02_editor-review/README.md`](02_editor-review/README.md) for the complete standalone instructions.

## Scope

The editor reviews Solution Design Documents for **Salesforce Enhanced Chat** and **Omni-Channel**, including new implementations and migrations from Legacy Chat.

Enhanced Chat capabilities vary by deployment surface, configuration, and release. A design that relies on version-specific behavior must name and verify that behavior; the editor flags unsupported claims instead of guessing.

**In scope:** requirements, architecture, routing, conversation lifecycle, integrations, data relationships, reporting, security, testing, deployment, and operational support.

**Out of scope:** Legacy Chat design except as a migration source, CTI/Amazon Connect, WhatsApp/SMS/Facebook Messenger, generic Salesforce reviews, code review, and any form of production or security certification.

## Workflow behavior and human boundaries

- **People own the work:** the author creates every design revision; the accountable architect creates every formal decision. The AI critiques, packages, validates, and routes—it does not take either person's authority.
- **The workflow stops for people twice:** at `03_author-revision/` for an author-created revision and at `05_formal-review/` for a human decision. Everything else advances only during an invoked agent run.
- **The formal reviewer receives a focused packet:** current design and review material stay prominent; superseded drafts and prior rounds remain preserved as history.
- **Responses are traceable:** every prior finding requires a disposition, change location, and explanation. A requirement-based disagreement is allowed and evaluated on its reasoning rather than treated as noncompliance.
- **History is preserved:** packages copy forward instead of moving destructively. Every accepted draft, review, response, manifest, and decision remains traceable upstream.
- **Completion is read-only:** later design changes require a new review ID that references the completed review.

## Reproduce the fictional demo

- **Follow the complete loop:** open the [Northstar Review Cycle](fixtures/northstar/review-cycle/) and read its artifacts in numbered order.
- **Standalone:** attach [`northstar-sdd-draft-v1.md`](fixtures/northstar/northstar-sdd-draft-v1.md) and [`northstar-requirements.md`](fixtures/northstar/northstar-requirements.md), then compare the result with the [observed sample](fixtures/northstar/sample-run.md) and [maintained expected review](fixtures/northstar/expected-review-round-01.md).
- **Full workflow:** copy the fictional Northstar submission files into `01_intake/input/NS-001/`, say *"Start a new demo review for ID NS-001,"* and follow the generated status card. Demo ledgers must remain marked `Demo: yes`.

## Under the hood

The agent runs the read-only helper [`tools/review_state.py`](tools/review_state.py) before and after workflow operations. It checks submissions, detects dropped-off files before accepting them, derives status from the routing ledger, validates packet links and state consistency, and generates checksummed artifact inventories. It never critiques a design, moves a package, or creates approval.

The repository contains six numbered stage folders with explicit `CONTEXT.md` contracts, [`reviews/`](reviews/) for authoritative routing ledgers and derived status cards, [`fixtures/`](fixtures/) for fictional demonstrations, and [`tools/`](tools/) for deterministic validation and Word-to-markdown conversion. Agents and maintainers should read [`AGENTS.md`](AGENTS.md) and the root [`CONTEXT.md`](CONTEXT.md) before operating the workflow.
