# UX Friction Journal — UX-001 — Workflow Round 01

**Purpose:** Capture product/usability friction a human would feel operating this repository workflow via chat/agent — not architecture critique of the Northstar design.

**Operator context:** Demo run of the full pipeline from new submission through first automatic stop at author revision (`03`). Review ID `UX-001`. Human actor on submission: `J. Rivera (UX simulation)`.

**Date:** 2026-07-19

---

## Summary

The contracts are rigorous and consistent once you already know the system. The first-time path from "I have three files" to "I am waiting on the author" is **expert-only**: state lives in a ledger you must invent before you understand why, file placement is pure filesystem ceremony with no progress UI, and "what do I do next?" is distributed across AGENTS.md, root CONTEXT.md, stage CONTEXT.md, and templates.

---

## Friction points (chronological)

### 1. No single "start a review" action

To begin, an operator must invent a review ID, create a folder under `01_intake/input/<ID>/`, copy three files, create a routing ledger with a specific table schema, then invoke the agent again (or hope the agent notices). There is no `start-review` script, checklist UI, or interactive prompt that asks "new package or continue?"

**Human feeling:** "Where do I put my documents so the system notices them?"

### 2. ID assignment is tribal knowledge

`reviews/README.md` explains the prefix+sequence scheme and says to list ledgers before assigning. The mission named `UX-001` explicitly; without that, a human would not know whether to use `NS-`, `UX-`, `SI-`, or something else. Prefix meaning is undocumented in one place.

**Human feeling:** "Am I allowed to pick UX-001? What do the letters mean?"

### 3. Demo labeling is easy to miss

Demo runs must set `Demo: yes` and only use fixtures when explicitly requested. That rule lives in AGENTS.md and reviews/README — not on the intake form itself. A rushed operator could process fixture content as a live review.

**Human feeling:** "How do I mark this as practice so nobody treats it as real?"

### 4. Fixture copy is manual and easy to get wrong

The correct move is: copy **three** northstar files, **not** `expected-review-round-01.md`. Nothing in the intake folder structure prevents dropping the expected review into input and contaminating the run. The fixtures README exists, but the happy path is still shell `cp`.

**Human feeling:** "Which files from fixtures/ am I supposed to submit?"

### 5. Multi-document instruction stack (high cognitive load)

Correct operation requires reading, in roughly this order:

1. `AGENTS.md` (operating sequence + routing table)
2. Root `CONTEXT.md` (stages, conventions)
3. `reviews/README.md` (ledger format)
4. Current stage `CONTEXT.md`
5. Templates for that stage
6. For editor review: `identity.md` + `rules.md` + selective reference/

There is no one-screen "do these 5 things now" for a first submission. Root CONTEXT says "one screen" but the *procedure* still spans many files.

**Human feeling:** "I read three files and still don't know whether I create the ledger before or after the files."

### 6. Ledger is authoritative but invisible

Current stage is defined only by the **latest row** of `reviews/<ID>-routing-log.md`. Folder contents are evidence, not state. There is no status banner, no dashboard, no `status UX-001` command. To answer "where is this package?" you open a markdown table and interpret it.

**Human feeling:** "Is my package stuck? Did intake finish? I see files in three folders."

### 7. Copy-forward is pure ceremony

Advancing stages means `cp` of an entire package subfolder into the next stage's `input/`. SI-001 already shows how this multiplies files over rounds. No confirmation that the copy is complete; no checksum; no "package advanced to 02" receipt except the ledger row you must remember to write.

**Human feeling:** "Did I copy everything? Did I forget the review report? Did I overwrite something?"

### 8. Human-actor field is inconsistently memorable

Human actor is required on submission/decision rows and `—` on rule-based transitions. Easy to forget on the first row, or to invent a name when operating as the agent on behalf of a demo. The format is in reviews/README, not echoed in the intake template's guidance beyond a blank field.

**Human feeling:** "Do I put my name, the author's name, or the agent?"

### 9. Intake "pass through" vs "fail" distinction is subtle

Missing diagrams pass; missing **external** referenced source material fails. The SI-001 history shows this boundary was re-litigated (Appendix A). For a human running intake by hand, the boundary is easy to misapply without re-reading `01_intake/CONTEXT.md` carefully.

**Human feeling:** "The SDD mentions a diagram we don't have — does that block me?"

### 10. Editor stage is a persona load with no "you are now the critic" affordance

Entering `02` means load identity + rules + selective reference. Leaving means drop them. In a chat interface there is no mode switch — the operator (or agent) must self-enforce not rewriting design. The prohibition is clear in rules, but the **product** does not prevent pasting a rewritten section.

**Human feeling:** "Can the AI just fix section 5.2 for me?" (and the answer is only in prose contracts)

### 11. Output contract is exact but not machine-checked

Findings must match the rules.md template fields. Nothing validates ≤5 findings, required severity/lens fields, or the verbatim boundary statement before routing continues. Quality depends on agent discipline.

**Human feeling:** "How do I know my review is in the right format before I send it to the author?"

### 12. Pre-filled revision response is a good idea, poorly discoverable as a product feature

Generating `UX-001-revision-response-round-01.md` with titles filled and answers blank is excellent UX for the author. It is specified only in stage CONTEXT / template comments — an operator who skips those might drop the author a bare review with no form.

**Human feeling (author):** "What am I supposed to fill out? Is there a form?"

### 13. First automatic stop has no "you're done for now" surface

After routing to `03`, the correct agent behavior is STOP. There is no author-facing packet cover sheet (unlike formal review's packet), no email template, no "next human action" file written into `03_author-revision/input/UX-001/`. The operator must re-derive the next step from CONTEXT.

**Human feeling:** "The AI stopped. What do I tell the author?"

### 14. README promise vs operational reality

The repo promises a clear pipeline and stage contracts. What a non-expert experiences is: many markdown contracts, manual file placement, an append-only ledger, and chat as the runtime. That gap is fine for maintainers; it is high friction for a first-time design author or a PM trying a demo.

**Human feeling:** "I thought this was a review tool. It feels like a process documentation repo I have to execute by hand."

### 15. Shell / path friction (agent-side, user-visible)

Even when an agent runs the demo, a failed first `cp` from the wrong cwd, absolute paths with spaces (`Salesforce Enhanced Chat Architecture Readiness Editor`), and parallel stage folders make mistakes easy. Users copying the agent transcript would hit the same.

**Human feeling:** "The path is long and everything has the same filename pattern — one wrong folder and I pollute SI-001."

### 16. No progress feedback during multi-stage auto-run

When the agent correctly chains intake → review → author-revision stop, the human watching chat gets a wall of activity then a summary. There is no intermediate "Intake complete ✓ / Review in progress…" status artifact they can open in the repo mid-run.

**Human feeling:** "Is it still working? How long does a review take?"

### 17. Collision risk with live reviews

`SI-001` occupies most stage folders. A demo ID `UX-001` is safe only because the operator chose a free ID. Nothing in the tools prevents writing into the wrong `<ID>/` subfolder if the agent is given an ambiguous "continue the review" instruction.

**Human feeling:** "Please don't touch Solstice while I demo Northstar."

---

## What worked well (for contrast)

- Stage `CONTEXT.md` one-job framing is clear once you open the right stage.
- Pre-populated revision response (titles filled, answers blank) is the right author UX when it is generated.
- Verdict boundary statement is forced by rules — reduces over-claiming.
- Copy-forward + versioned filenames preserve history without overwriting.
- Fixtures + expected review give a real acceptance target for demo validation.
- Routing table in AGENTS.md is the right dispatch mental model after you have seen it once.

---

## Highest-impact product fixes (observations only — not implemented)

1. A single **start / status / advance** command or chat skill that owns ID assignment, ledger rows, and package copies.
2. A per-review **status card** (`reviews/UX-001-status.md` or generated) with current stage, last verdict, and exact next human action.
3. An **author packet cover** at `03` analogous to formal-review's cover sheet.
4. Intake wizard questions: Demo? Migration vs new? Confirm three required files.
5. Guardrails: refuse to write into another ID's folders; refuse to rewrite SDD content in stage 02.

---

## Journal metadata

- Review ID: UX-001
- Stages executed: `01_intake` → `02_editor-review` → `03_author-revision` (stop)
- Verdict: Revise Before Formal Review
- Operator mode: chat/agent pipeline workflow demo
