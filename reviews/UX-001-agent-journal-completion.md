# UX Friction Journal — UX-001 — Completion (Post-Signature Automation)

**Purpose:** Capture product/usability friction for the post-signature path: detecting a signed formal decision, validating Approved-with-Conditions rules, packaging into `06_completed`, and whether completion feels terminal and clear.

**Operator context:** Demo run advancing UX-001 from `05_formal-review` (Ready for Formal Review with Open Decisions; signed decision already in `output/`) to terminal `06_completed`. Decision actor: `A. Chen (UX simulation)`.

**Date:** 2026-07-19

---

## Summary

Once the signed decision exists, the advance rule is mechanically clear — **but discovery is passive, condition validation is prose-table parsing, and packaging is a multi-source assembly job with no checklist file**. Completion is accurate for operators who know SI-001's shape; it is not celebratory or self-explaining for authors waiting outside the repo.

---

## Friction points (this pass)

### 1. Detecting a signed decision has no event surface

The formal decision lands as `05_formal-review/output/UX-001/UX-001-formal-decision.md`. Ledger still said package was at `05_formal-review` with Ready for Formal Review. Correct procedure: notice the decision file (or be told by chat), validate it, copy to `06`, append the ledger row.

Nothing emits "decision signed." Folder presence + filename convention is the signal. A human author who emails "approved" without filing the record leaves the pipeline stuck forever at the human stop.

**Human feeling:** "I signed off — is the package done, or is someone still supposed to click something?"

**What you must already know:** Chat-submitted *completed* decision records go to `05_formal-review/output/<ID>/` (`AGENTS.md`); the agent must not draft Decision/Rationale/Signature; ledger does not advance until the file exists and validates.

### 2. Validating Approved with Conditions is careful table reading, not a schema

Advance is allowed only when every condition has **owner**, **disposition**, and **Blocking? = no** (or equivalent non-blocking mark). UX-001 had three rows, all `no`, with multi-owner cells and prose dispositions. Validation is:

1. Decision value is exactly one of the three allowed tokens.
2. Named human actor + date on Signature (and decision date).
3. If AWC: scan the conditions table; reject blank owners, missing dispositions, or any `yes`/blocking.

There is no machine-checkable form. A missing "Blocking?" column or free-text "non-blocking" buried only in a summary sentence could be misread either way. The decision's closing line ("All conditions are **non-blocking**. Package may advance…") helps agents but is optional convention, not contract.

**Human feeling:** "Approved with Conditions — am I blocked until conditions close, or free to build?"

**What works:** Explicit Blocking column + table completeness made this package unambiguous once read carefully.

### 3. Packaging for 06 is multi-stage archaeology

`06_completed/CONTEXT.md` says copy the approved package and complete review history. Actual sources are scattered:

| Need | Source stage |
|---|---|
| Final SDD, requirements, assumptions, packet | `05_formal-review/input/<ID>/` (top level only) |
| Formal decision | `05_formal-review/output/<ID>/` |
| Intake + revision-intake manifests | `01` and `04` outputs |
| All review rounds | `02` outputs (or `05` history + top-level ready review) |
| Response logs | `03` / `04` / `05` history |
| Routing ledger snapshot | `reviews/` after the completion row is appended |

SI-001's completed tree (top-level current + `history/{manifests,reviews,responses,workflow}`) is the de facto template. Superseded drafts and blank FORM/template copies are **excluded** — but that exclusion is learned from SI-001 integrity language, not a one-line "include X exclude Y" inventory in `06`.

**Human feeling:** "Do I zip the whole formal-review folder, or rebuild a clean archive?"

**Risk:** Over-copy (blank decision FORM, v1 drafts) or under-copy (missing intake manifest / routing log) without an automated package script.

### 4. Ledger timing vs package copy order

The completion ledger row should cite both the decision and the completion manifest. Practical order used:

1. Validate decision.
2. Copy immutable package into `06_completed/input/`.
3. Write `06_completed/output/<ID>/<ID>-completion-manifest.md`.
4. Append ledger row (05 → 06, status Approved with Conditions, human actor from signature).
5. Snapshot ledger into `history/workflow/` so the terminal package includes the terminal row.

If the ledger snapshot is taken before the append, the archive ends mid-flight. Nothing enforces step order.

### 5. Completion is terminal but not celebratory

After the last row, `To stage` = `06_completed` and AGENTS says stop. There is:

- No status badge or README "Approved" banner in `06_completed/input/UX-001/`.
- No author-facing summary of what was approved vs what conditions remain for build.
- Conditions live in the decision record and are **optionally** restated in the completion manifest (this run restated them for operator clarity — SI-001 had no conditions so no parallel).

For an author, "done" is only discoverable by reading the ledger's last row and opening the decision. A productized UX would surface: **Approved with Conditions · 3 non-blocking · terminal · do not edit**.

**Human feeling:** "Is this the finish line, or another wait state like formal review?"

### 6. What a human would not know without multiple contracts

Without reading at least:

1. `05_formal-review/CONTEXT.md` — AWC advance rule (owner + disposition + non-blocking)
2. `06_completed/CONTEXT.md` — admission rule, terminal/read-only, manifest-only output
3. `AGENTS.md` routing table — 05 Approved / AWC → 06; terminal after manifest
4. SI-001 completed package — real inventory shape and "no superseded drafts"
5. `reviews/README.md` — human actor required on formal-decision row

…a careful operator will either stall after signature or invent an incomplete archive.

---

## What went smoothly

- Decision record was well-formed on first read: named actor, ISO dates, single decision token, conditions table complete, all Blocking = no.
- Open decisions from the Ready verdict were dispositioned in Rationale (OD-02 closed; OD-03 residual → Condition 1; owner-continuity retained).
- SI-001 provided a concrete packaging pattern; two-round UX-001 history is small and easy to place.
- Stage contracts for 05/06 are short and decisive once found — the gap is discovery and packaging choreography, not ambiguous policy.

---

## Product implications (for a future operator UI)

1. **Decision-received event** when a signed record appears under `05/.../output/` (or chat-file placement).
2. **Condition checklist validator** with hard fail on missing owner/disposition/blocking flag before any copy to 06.
3. **One-command complete package** that gathers final artifacts + history buckets and refuses blank FORMs / superseded drafts.
4. **Terminal card** in UI: decision value, actor, date, conditions summary, link to completion manifest — so authors do not re-read the ledger.
5. **Celebrate lightly:** "Package UX-001 is complete and read-only" is enough; avoid implying build conditions are closed.
