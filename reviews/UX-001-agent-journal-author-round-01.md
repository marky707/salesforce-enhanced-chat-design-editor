# UX Friction Journal — UX-001 — Author Revision Round 01

**Purpose:** Capture product/usability friction experienced **as the design author** (J. Rivera) working through revision in this repository — not critique of the Northstar chat architecture itself.

**Operator context:** Author role in stage `03_author-revision` for review ID `UX-001`, responding to `UX-001-review-round-01.md`. Human actor: J. Rivera. Date: 2026-07-19.

**Scope of feeling:** discovering next action, reading findings, filling the response form, versioning, folder placement, multi-file cognitive load, deferred areas, submission clarity for a non-agent human, chat vs filesystem mental model.

---

## Summary

Once I found the review report, the *design* work was clear: five findings with explicit author tasks. The *workflow* work was not. I spent more anxiety on “which folder is the real handoff?” and “do I invent a ledger row?” than on owner-routing timeouts. The system assumes an author who already understands stage numbers, dual copy destinations (output vs intake), and that chat instructions may be the only place “submit by copying to 04” is phrased as a concrete action. A human opening only `03_author-revision/CONTEXT.md` gets half the story.

---

## Friction points (as the author)

### 1. “What do I do next?” is not on one screen

I arrived with materials already in `03_author-revision/input/UX-001/`. CONTEXT says: revise, complete the response log, then copy into `04_revision-intake/input/<ID>/` and invoke the workflow. That is better than nothing, but the review report itself does not say “your next human action is revise → fill log → copy to 04.” The finding list ends; the procedural next step lives elsewhere.

**Human feeling:** “I fixed the design in my head — is the system waiting on me, or is someone else supposed to pick this up?”

**Time-to-understand next action:** ~10–15 minutes of reading CONTEXT + response form tip + comparing to SI-001 history before I trusted the path. Not “open folder and go.”

### 2. Discovering the findings was easy; discovering Deferred Review Areas was almost accidental

Priority Findings 1–5 are loud. Deferred Review Areas sit at the bottom after Open Decisions for the Senior Architect. The response form tip is what made me treat deferred items as *this round’s free work* rather than “future me.” Without that tip, I would have shipped only the five findings and eaten another full review cycle.

**Human feeling:** “Was I supposed to read past the blocking list? Is deferred optional homework or shadow scope?”

**Discoverability of Deferred Review Areas:** Moderate only because the response template tip points at them. The review report labels them clearly but does not say “authors who address these now usually avoid a round.” That sentence lives on the form, not the review.

### 3. Response form UX is mostly good — disposition checkboxes are slightly fake

The three prompts (Disposition / Where / Why) match how I think after a revision. Junior-consultant voice is explicitly allowed; that reduced formality paralysis. The tip about supporting artifacts disagreeing with the SDD is gold — that is exactly the mistake I almost made (closing OD-01 in prose without versioning the assumptions file).

Friction: the form shows `[ ] resolved` checkbox style while SI-001’s completed examples use bold `**Disposition:** resolved`. I was not sure which notation revision intake parses, if any, or if humans only read it.

**Human feeling:** “Am I filling a machine-readable form or a memo for the next agent?”

### 4. Versioning confusion (document vs package vs round)

I needed:

- SDD `v2` filename
- Possibly assumptions `v2` if I closed ODs
- Response log still named `…-round-01` (because it answers review round 01)
- Requirements unchanged (same filename)

That is coherent once explained, but nothing in the author folder shows a side-by-side “you are producing v2 against round 01.” SI-001’s pile of v2…v7 files in neighboring folders is intimidating — looks like failure, even when it is normal iteration.

**Human feeling:** “If I change one paragraph, is that v2 or v1.1? If I only update assumptions, does the SDD version bump?”

### 5. Where to put files — fear of the wrong folder

Author stage has **both** `input/` (what I was given) and `output/` (what I produce). Submission is a **third** place: `04_revision-intake/input/UX-001/`. I double-checked that I should not only leave files in `03/.../output/` and “hope the pipeline notices.” CONTEXT says no automatic exit — copy is deliberate. Good for control; scary for “did I actually submit?”

**Human feeling:** “If I only write to output/, did I fail silently? Is 04 a shared inbox or a sacred drop zone?”

Fear of wrong folder is high: polluting `02_editor-review`, overwriting `input/`, or creating `04_revision-intake/output/` by mistake all feel possible. No confirmation receipt except the files sitting in 04.

### 6. Multi-file packet cognitive load

My mental checklist became:

1. Read review  
2. Read v1 SDD + requirements + assumptions  
3. Rewrite SDD v2 addressing 5 findings + deferred  
4. Version assumptions if OD closed  
5. Fill every finding block in the response log  
6. List “New material”  
7. Re-read assumptions vs SDD vs log for contradictions  
8. Copy four files to 04  
9. Do **not** touch the routing ledger (workflow agent will)  
10. Write this journal in yet another path (`reviews/`)

That is a lot of working memory for an associate consultant who primarily wants to fix routing prose. The response form warns about contradiction; it does not give a submit checklist (files required, optional, forbidden).

**Human feeling:** “I am project-managing a micro-release of documentation, not just answering comments.”

### 7. “Copy to 04_revision-intake” for a non-agent human

Clear **if** you read stage CONTEXT and treat paths as the product UI. Unclear **if** you live in chat (“I revised the design — please take it”) and expect the assistant to advance state. The instruction “invoke the workflow” after copy is abstract — invoke how? Tell whom? Run which prompt?

For a pure filesystem human without an agent: `cp` into `04_revision-intake/input/UX-001/` is doable but feels unfinished without a “submitted” marker or PR-style open state. For a chat-native human: filesystem drop zones fight the mental model that “sending a message” is submission.

**Human feeling:** “I put files in a folder. Is anyone notified? Do I message Mark? Do I wait?”

### 8. Chat vs filesystem mental model (conflict)

Operating as an author *through* an agent, I experienced split brain:

- Design judgment feels like conversation (“decide two deployments”).  
- Compliance feels like git without git (“version filename, copy tree, don’t edit ledger”).  

The agent can write the SDD, but the stage contract (in general) tells AIs not to invent design — this run inverted that by *assigning* me as author persona. A real human author pair-writing with AI would hit the CONTEXT rule: AI may explain findings and scribe the log, not draft the fix. That boundary is easy to violate under time pressure and hard to see mid-chat.

**Human feeling:** “Is the AI my ghostwriter or my process nanny? The folder structure answers process; the chat answers content — neither owns both.”

### 9. Ledger anxiety

Instructions said do **not** create a routing ledger row for submission — workflow agent will. That is a relief and a worry. Relief: one less ceremonial table. Worry: until the ledger moves, my 04 drop might look like debris next to SI-001’s history. Folder contents are “evidence, not state” — so my submission is invisible to status-checkers who only read the ledger.

**Human feeling:** “I submitted into a void until someone else writes a table row.”

### 10. Comparing myself to SI-001

Seeing SI-001 at v7 / round 07 in the tree while I produce v2 is psychologically heavy. The system normalizes many rounds; the UI does not celebrate “round 01 closed cleanly.” Authors may over-revise preemptively or under-revise hoping for luck.

**Human feeling:** “Is five findings normal, or am I a bad designer? How many rounds is failure?”

---

## What helped

- Review findings with **Author’s task** lines — concrete enough to design against.  
- Response log **pre-populated with one block per finding** — no inventing structure.  
- Tip on Deferred Review Areas and supporting-artifact consistency — saved a likely bounce.  
- SI-001 v2 SDD + response log as a **worked example** of depth and tone.  
- Explicit permission to disagree and to use plain language.  
- Clear ban on author writing the routing ledger (reduces ownership ambiguity slightly).

---

## What felt broken

- No author-facing “submit package” checklist or confirmation artifact.  
- Dual destination (`03/output` vs `04/input`) without a progress indicator.  
- Next-action procedure split across CONTEXT, form tips, and chat instructions.  
- Deferred scope discoverability depends on reading the form tip, not only the review.  
- Chat submission mental model unsupported; pure filesystem submission has no receipt.  
- Version numbering rules implicit (learn by SI-001 archaeology).

---

## Suggested product fixes (author lens only)

1. A single `AUTHOR-NEXT.md` or top-of-input README generated per package: “Revise → fill log → copy these N files to `04_revision-intake/input/UX-001/` → message workflow.”  
2. Promote Deferred Review Areas tip onto the review report footer, not only the response form.  
3. After copy, a tiny `UX-001-author-submit-note.md` template the author drops with timestamp/name so 04 is self-describing before the ledger row exists.  
4. One sentence on versioning: “New SDD version per review round; response log round matches the review round you answer; bump assumptions filename when OD disposition changes.”  
5. Status command or rendered “package is in 03 awaiting author / in 04 awaiting intake” so humans are not ledger archaeologists.

---

## Closing note

As J. Rivera I could resolve the design findings with confidence. As a human user of this repo I would still ask a colleague, “Did I submit correctly?” after copying to 04. That question is the core UX failure of an otherwise careful stage design: **submission is a side effect of file placement, not a first-class action.**
