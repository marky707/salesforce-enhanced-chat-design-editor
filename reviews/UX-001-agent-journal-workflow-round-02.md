# UX Friction Journal — UX-001 — Workflow Round 02

**Purpose:** Capture product/usability friction a human (or agent operator) would feel moving a package from "author finished a revision" through revision intake, re-review, and formal-packet assembly — not architecture critique of the Northstar design.

**Operator context:** Demo run continuing UX-001 from `03_author-revision` stop through automatic stop at `05_formal-review`. Human actor on resubmission: `J. Rivera (UX simulation)`.

**Date:** 2026-07-19

---

## Summary

The revision loop works if you already internalized round-01 mechanics — but **detecting a waiting resubmission**, knowing **which stage job is intake vs critique**, and **assembling a formal packet without overwriting history** still require reading multiple CONTEXT files and copying SI-001 conventions by eye. Round numbering is especially easy to get wrong at the 03→04→02 boundary.

---

## Friction points (this pass)

### 1. Detecting a waiting resubmission has no event surface

Author work lands as files under `04_revision-intake/input/UX-001/`. Nothing pings the workflow agent. The ledger still said package was at `03_author-revision`. Correct procedure: notice filesystem contents that contradict the "awaiting author" ledger stop, then **append a human-submission row** (03→04) before running revision intake.

**Human feeling:** "I finished my revision — does the system know? Do I message someone, drop files somewhere, or wait?"

**What you must already know:** Chat-submitted docs go to `04` when the review is awaiting the author (`AGENTS.md`); human actor is required on that ledger row; folder presence alone is not state until the row is written.

### 2. Revision intake vs editor review is a sharp but invisible job boundary

`04` only checks: new version present, response log names the right prior review, every finding has a disposition + location, new artifacts present or explained. It **must not** judge whether the design actually fixed anything.

`02` reads the response log first, judges resolutions, then critiques new/changed content (≤5 findings).

An operator who "just reviews the new SDD" in `04` or who re-runs full critique before the manifest is written breaks the audit model. The boundary is clear in two short CONTEXT files — and almost nowhere else in the UI of the repo.

**Human feeling:** "I can see the fixes — why am I filling a checklist instead of reviewing?"

### 3. Round numbering jumps at counterintuitive moments

- Author answers **round 01** findings with `UX-001-revision-response-round-01.md`.
- Revision-intake manifest is `…-manifest-round-01.md` (the round **answered**).
- On completion, **review round increments to 02** before editor review.
- Editor output is `UX-001-review-round-02.md`.
- Ledger row for submission still shows Round `01` / Doc `v2` on the 03→04 transition; the 04→02 row is Round `02`.

SI-001's ledger is the only working example of this pattern. A human alone can easily name the response log `round-02` because "this is the second time through."

**Human feeling:** "Is this round 1 or round 2? My response file and the next review disagree."

### 4. Copy-forward without overwrite is pure discipline

`02_editor-review/input/UX-001/` already held v1 SDD and assumptions v1. Rules: **add** v2 files and the response log; **do not** delete or overwrite prior versioned artifacts. `cp -n` helps for new names; same-named requirements files are a judgment call (refresh vs leave). Nothing enforces non-overwrite.

Later, formal packet assembly **splits** current vs history: v2 at top level, v1 and round-01 artifacts into `history/`. That split is specified in `02_editor-review/CONTEXT.md` routing prose — not in a script, not in `05`'s folder README.

**Human feeling:** "Am I supposed to replace the old draft or keep both? Why does formal review reorganize everything again?"

### 5. Packet assembly for formal review is multi-file choreography

Ready verdict requires delivering:

| Top level (act on these) | `history/` (audit only) |
|---|---|
| Current SDD v2 | Prior SDD v1 |
| Ready review round 02 | Review round 01 |
| Current requirements | Prior assumptions v1 |
| Current decision register v2 | Response log round 01 |
| Cover sheet with **relative** markdown links | |
| Decision FORM (admin fields only; Decision/Rationale/Signature blank) | |
| Blank decision template copy | |

Also: do **not** write the formal decision; do **not** fill Decision/Rationale/Signature. One wrong fill invents architecture approval.

**Human feeling:** "I got a Ready verdict — am I done? Who signs what? Which file is the actual approval?"

### 6. What a human would not know without many CONTEXT files

Without reading (at least) all of the following, a careful human will stall or invent procedure:

1. `AGENTS.md` — routing table (revision submitted → 04; complete → 02 round+1; Ready → 05 stop)
2. Root `CONTEXT.md` — human stops at 03 and 05
3. `reviews/README.md` — ledger is authoritative state; human actor on submissions
4. `04_revision-intake/CONTEXT.md` + `revision-intake-manifest-template.md` — completeness only
5. `02_editor-review/CONTEXT.md` — persona, routing to 03 vs 05, **packet layering rules**
6. `02_editor-review/rules.md` + `identity.md` — critique constraints, round 2+ resolution check, ≤5 findings, readiness vs perfection
7. `05_formal-review/CONTEXT.md` + `formal-decision-template.md` — human-only decision
8. SI-001 ledger + `05_formal-review/input/SI-001/*` — **the only end-to-end worked example** of ready-packet shape and FORM pre-fill style

Missing any one of these produces a common failure mode: overwriting history, wrong round numbers, judging design quality at intake, or drafting a fake formal decision to "finish the workflow."

### 7. "Automatic stop" is easy to overshoot

Mission says process through the next automatic stop. After Ready, the correct stop is **05** with a blank decision form. Momentum wants to complete the pipeline (06). Only the prohibition "Do NOT write formal decision" and stage contracts prevent overshoot. There is no hard gate in software.

**Human feeling:** "The system said Ready — I'll just mark it Approved so we can archive."

---

## What worked smoothly this pass

- SI-001 ledger rows are an excellent template for "revision submitted" / "revision intake complete" / "Ready … Open Decisions" wording.
- Response log structure made 04's traceability table mechanical (findings 1–5, locations named).
- Author package already sat in `04_revision-intake/input/UX-001/` with completed log — no chat-filing ambiguity this round.
- Dual versioned artifacts (`northstar-sdd-draft-v1.md` + `v2`, assumptions v1 + v2) made non-overwrite intent obvious once both existed in the same folder.

---

## Implications for product UX (if this pipeline were a product)

1. **Inbox / work queue:** "UX-001 waiting at 03 — 4 files detected in 04 input — Submit revision?" one-click ledger transition.
2. **Round assistant:** auto-name response log and next review round from ledger; prevent `round-02` response for unanswered `round-01` findings.
3. **Stage job banner:** "You are validating completeness (not design quality)" vs "You are the critic (≤5 findings)."
4. **Copy-forward wizard:** add files, never silent overwrite; show diff of folder before/after.
5. **Ready → packet button:** build top-level + history/ + cover sheet + FORM blanks from a single action; lock Decision fields from agents.
6. **Single "operator runbook" screen** for the revision loop (detect → ledger → 04 → 02 → route) instead of eight files.

---

## Paths produced this pass

| Artifact | Path |
|---|---|
| Ledger | `reviews/UX-001-routing-log.md` |
| Revision intake manifest | `04_revision-intake/output/UX-001/UX-001-revision-intake-manifest-round-01.md` |
| Editor review round 02 | `02_editor-review/output/UX-001/UX-001-review-round-02.md` |
| Formal packet cover | `05_formal-review/input/UX-001/UX-001-formal-review-packet.md` |
| Decision FORM (admin only) | `05_formal-review/input/UX-001/UX-001-formal-decision-FORM.md` |
| This journal | `reviews/UX-001-agent-journal-workflow-round-02.md` |
