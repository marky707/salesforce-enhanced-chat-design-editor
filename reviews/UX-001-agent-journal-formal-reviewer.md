# UX Friction Journal — UX-001 — Formal Reviewer (Senior Architect)

**Purpose:** Capture product/usability friction experienced **as the accountable senior architect** opening and deciding the formal-review package — not a second design critique of Northstar Enhanced Chat (except where presentation affects judgment confidence).

**Operator context:** Human formal-review role simulation in stage `05_formal-review` for review ID `UX-001`. Persona: A. Chen, Senior Solution Architect (UX simulation). Date: 2026-07-19.

**Scope of feeling:** packet entry, reading order, open-decision presentation, form clarity, relative links, history usefulness, save-location ambiguity, decision-option clarity, confidence that signing advances the workflow, missing summary chrome a real SA would want.

---

## Summary

The layered packet is genuinely better than a flat dump of every version: cover sheet → ready verdict → SDD → register → form is a sane order, and `history/` is correctly demoted. Decision authority is also clear once you read the footer (“readiness ≠ approval”). The remaining pain is **senior-architect operational chrome**: residual-risk one-pager, v1→v2 diff, time estimate, and an unambiguous “write the signed file here, then stop” confirmation path. Relative path `../../output/UX-001/` is correct for agents and brittle for a human who lives in Finder or a browser preview.

---

## Friction and delight points (as the formal reviewer)

### 1. Packet cover sheet — strong entry (delight)

`UX-001-formal-review-packet.md` as **start here** works. Links are relative and clickable in-repo; open decisions are listed on the cover so I did not have to hunt the full SDD first. Footer correctly separates editor readiness from my approval authority — that sentence prevented me from rubber-stamping “Ready” as “Approved.”

**Human feeling:** “I know what I’m holding and what I’m being asked to decide.”

### 2. Suggested reading order quality (delight, mild length friction)

Order is right: cover → round-02 verdict → SDD v2 → assumptions v2 → form. Round-02 resolution check is the highest-value 30 seconds: I could see all five prior findings closed before deep-reading architecture. Cost: the SDD is still a full design doc; there is no “architect brief” between verdict and Section 4–10.

**Time-to-first-judgment readiness:** ~15–20 minutes with skim of SDD architecture/routing/deployment/KPIs; ~45+ for a careful SA who re-reads deferred areas.

### 3. Open decisions presentation (good, slightly uneven)

Three items are called out consistently on the packet, the ready review, and the FORM. Labels are stable (OD-02, OD-03 residual, owner-continuity). Friction: only two are numbered ODs; owner-continuity is a “business tradeoff” without an OD-id, so it feels like it might fall off the decision register if someone only updates the assumptions file. I had to disposition it in rationale without a clean OD-xx slot.

**Human feeling:** “Two are register items; one is a hallway conversation that got promoted — am I supposed to invent OD-04?”

### 4. Form clarity — Decision / Conditions / Changes (mostly clear)

Three outcomes are explicit: `Approved` / `Approved with Conditions` / `Changes Required`. Conditions table columns (Owner, Disposition, Blocking?) match how I think about gated work. The FORM comment that the package advances only when **every** condition is filled and **non-blocking** is critical — without it I might mark a “blocking” condition and wonder why 06 never fires.

Mild friction: “Circle one” in a markdown file is metaphorical; I typed backticks around one option. Also, when Conditions apply, Required changes is “Not applicable” vs empty — template does not say which empty-state is preferred.

**Human feeling:** “I know Approved with Conditions is the middle path; I’m less sure of the exact empty-section etiquette.”

### 5. Relative links and path to save the signed file (friction)

Packet says: save as `UX-001-formal-decision.md` in `../../output/UX-001/`. That resolves correctly from `05_formal-review/input/UX-001/` but:

- A human in an IDE must mentally walk up two directories.
- Output README still says AI must never author files here (true for the pipeline; confusing when a UX simulation asks an agent to role-play the human).
- FORM and packet both state the path; neither provides an absolute path, a “done when file exists” checklist, or a “do not also write under 06” warning on the form itself (CONTEXT has routing rules; the form does not).

**Ambiguity score:** Medium. I found the destination, but I double-checked CONTEXT and SI-001’s output layout before writing. Fear of writing into `input/` or prematurely into `06_completed` is real.

### 6. History folder usefulness (delight when needed; correct default ignore)

`history/` with round-01, response log, SDD v1, prior assumptions is right for audit. I only needed it for “what changed from v1?” and there is **no generated diff or changelog summary** — only the SDD’s own “Changes from v1” paragraph and the round-02 resolution table. For formal approval I mostly trusted the resolution check and did not re-read all of v1.

**Human feeling:** “History is there if Legal asks; I still wish for a one-screen delta.”

### 7. Confidence that signing advances the workflow (mixed)

CONTEXT is clear: Approved or Approved with Conditions (all non-blocking) → 06; Changes Required → back to 03. The reviewer is told **not** to copy to 06 themselves in the simulation instructions (workflow agent does it). That split is good for control and bad for “I’m done” dopamine: after signing, the folder still sits in 05 with no status badge, no next-actor name, no expected SLA for the workflow agent.

**Human feeling:** “I signed. Is the system watching this path, or do I Slack someone?”

### 8. What a real SA would still want (missing UI chrome)

Missing or weak in the packet (not blocking this decision, but product gaps):

| Wanted | Why |
|---|---|
| Residual risk summary (top 5) | Deferred areas in round-02 are buried; I re-surfaced two as conditions myself |
| Explicit non-blocking conditions checklist pre-filled as optional prompts | Faster than inventing table rows |
| Time estimate for review | Calendar block; packet is silent |
| Diff / changelog v1→v2 | Faster than reading full SDD + history |
| Requirements↔design traceability matrix one-pager | R-01–R-08 to section map exists only via testing table (Section 12) |
| Decision option definitions (one sentence each) | Especially “Conditions” vs send back |
| Absolute or copy-button path for signed output | Reduce wrong-folder risk |
| Post-sign confirmation contract | “Workflow will move to 06 when valid; do not create 06 yourself” on the form |

### 9. Multi-file cognitive load vs SI-001 pattern (mild)

Compared to SI-001’s long revision history, UX-001 after two rounds is light — good. Still, simultaneous open of packet + round-02 + SDD + assumptions + form + optional history is five+ files. No single “decision workspace” view.

### 10. Provenance / demo honesty (delight for this exercise)

Packet and SDD mark fictional demo content. Signing as a named persona with an explicit “UX simulation formal decision” note matches SI-001 demo provenance and avoids false audit claims. That is the right pattern when humans are simulated.

---

## Top 8 friction / delight (condensed)

1. **Delight:** Cover packet + open decisions + readiness≠approval footer — clear mandate.
2. **Delight:** Round-02 resolution check substitutes for full re-audit of five findings.
3. **Delight:** Conditions table with Blocking? and advance rule — decision mechanics are legible.
4. **Friction:** Save path `../../output/UX-001/` and “who advances 06?” split — post-sign uncertainty.
5. **Friction:** No residual-risk one-pager; deferred areas easy to under-weight.
6. **Friction:** Owner-continuity tradeoff lacks OD-id; uneven vs OD-02/OD-03.
7. **Friction:** No v1→v2 diff / time estimate / R↔section matrix for busy SA.
8. **Friction:** Markdown “circle one” + empty-section etiquette slightly under-specified.

---

## Decision recorded (journal note only)

- **Outcome:** `Approved with Conditions` (all conditions non-blocking)
- **Signed file:** `05_formal-review/output/UX-001/UX-001-formal-decision.md`
- **Did not** copy package to `06_completed` (left for workflow agent)

---

*End of formal-reviewer UX journal for UX-001.*
