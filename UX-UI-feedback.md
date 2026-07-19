# UX / UI Feedback — Salesforce Enhanced Chat Design Review Editor

**Author:** Senior UI/UX review (orchestrated end-to-end walkthrough)  
**Date:** 2026-07-19  
**Scope:** Product and interaction experience of the repository workflow — not folder-structure redesign  
**Method:** Live end-to-end simulation as review **UX-001** (Northstar fixture), with role-separated agents and friction journals  
**Constraint honored:** No recommendations that restructure the six stage folders or the ICM stage map

---

## 1. Executive summary

This product is **excellent as an architecture-review operating system** and **weak as a first-time user interface**.

The critic contracts, human authority boundaries, pre-filled response log, formal packet cover sheet, and copy-forward history model are unusually strong. In the live run, a deliberately flawed SDD went:

**Submit → Intake → Review (Revise) → Author revision → Revision intake → Review (Ready with Open Decisions) → Formal Approved with Conditions → Completed**

in **two review rounds**, with coherent findings and a usable senior-architect packet.

What is *not* seamless is everything around those contracts: **state visibility, next action, submission as a first-class event, version/round mental model, and progress feedback**. Today the “UI” is a distributed stack of markdown contracts plus filesystem ceremony. Experts and agents can run it; junior authors and busy senior architects will constantly ask *“did I do the right thing?”*

**Verdict:** Do **not** rewrite the pipeline architecture. Invest in **interaction layer** improvements that sit *on top of* the existing structure: status cards, next-action covers, submission receipts, round/version legends, and a single operator skill/command surface.

**Overall score (as product UX):** **6.5 / 10**  
**Score of the critique engine itself:** **9 / 10**  
**Score of first-session onboarding / handoff clarity:** **4 / 10**

---

## 2. How this feedback was produced

| Role | Actor (simulation) | What they did | Journal |
|---|---|---|---|
| Pipeline operator | Workflow agent | Filed Northstar as UX-001, intake → review → stop at 03 | `reviews/UX-001-agent-journal-workflow-round-01.md` |
| Design author | J. Rivera | Wrote SDD v2 + response log, dropped package into 04 | `reviews/UX-001-agent-journal-author-round-01.md` |
| Pipeline operator | Workflow agent | Revision intake → round-02 review → formal packet | `reviews/UX-001-agent-journal-workflow-round-02.md` |
| Senior SA | A. Chen | Reviewed packet, **Approved with Conditions** | `reviews/UX-001-agent-journal-formal-reviewer.md` |
| Pipeline operator | Workflow agent | Validated decision → 06 completed | `reviews/UX-001-agent-journal-completion.md` |

**Artifacts of the run:** `reviews/UX-001-routing-log.md`, stage folders under `*/input|output/UX-001/`, terminal package in `06_completed/`.  
**Demo:** yes. Fictional Northstar content only.

Folder structure was not changed. Only user-class files (submissions, revisions, decisions, journals, this report) were created.

---

## 3. Journey map (what users actually feel)

```text
[Author has 3 files]
        │  "Where do these go? What is my ID?"
        ▼
   01 Intake  ──────────────────────────────  silent / expert
        │  "Did intake pass? Why did a missing diagram not fail?"
        ▼
   02 Editor review  ───────────────────────  high quality output when run
        │  "What do I tell the author?"
        ▼
   03 Author revision  ─────────────────────  HUMAN STOP (highest anxiety)
        │  "I fixed it — did I submit?"
        ▼
   04 Revision intake  ─────────────────────  invisible until ledger row
        │
        ▼
   02 Round 2+  ────────────────────────────  good when response log exists
        │
        ▼
   05 Formal review  ───────────────────────  best packet UX in the product
        │  "I signed — is anyone watching this folder?"
        ▼
   06 Completed  ───────────────────────────  terminal but uncelebrated
```

**Primary UX failure mode:** work is complete in the *content* sense long before it is complete in the *state* sense. Submission, signature, and readiness are side effects of file placement, not first-class actions.

---

## 4. What is already excellent (preserve)

Do not dilute these. They are the product’s moat.

| Strength | Why it works |
|---|---|
| **Critic-only invariant** | Multi-layer enforcement (rules, stage prohibitions, formal human-only decision) correctly prevents the AI from “fixing” the SDD. |
| **Why → Flow → Failure → Proof** | Authors get architecture mentorship, not style nits. Round-01 findings on UX-001 were specific, anchored, and actionable. |
| **≤5 findings + Deferred** | Focuses effort; deferred tip on the response form is high leverage. |
| **Pre-filled revision response log** | Best author affordance in the system when generated. |
| **Intake ≠ readiness** | Missing author diagrams pass through as findings — prevents false intake failures. |
| **Copy-forward + versioned filenames** | History survives; SI-001/UX-001 remain auditable. |
| **Routing ledger as source of truth** | Correct systems design once you know it exists. |
| **Formal review packet cover** | Suggested reading order, open decisions, readiness≠approval footer — senior-architect grade. |
| **Conditions table with Blocking?** | Makes “Approved with Conditions” operationally meaningful. |
| **Fixtures + expected review** | Real demo/regression path (`fixtures/northstar/`). |
| **Convergence rule** | Ready with Open Decisions in round 02 for a solid v2 — system can say yes. |

**Bottom line:** the *judgment product* is largely right. The *interaction product* around it is under-built.

---

## 5. Priority recommendations (no folder restructure)

Recommendations assume the six stages, `reviews/`, `fixtures/`, and `02_editor-review` knowledge bundle stay put. Improvements are **overlays, generated files, prompts, and optional scripts**.

### P0 — Make “where am I / what next?” first-class

#### P0.1 Status card per review (generated, not a new stage)

After every ledger append, generate or refresh:

`reviews/<ID>-status.md`

Suggested contents:

- Current stage (from latest ledger row)
- Round + document version
- Last verdict
- **Exact next human action** (1–3 bullets)
- Links to the packet the human must open
- Demo flag

**Why:** Every persona hit the same wall: folders multiply; state lives only in a table most people never open.

#### P0.2 Author next-action cover at stage 03 (mirror formal packet)

When routing to `03_author-revision`, generate:

`03_author-revision/input/<ID>/<ID>-author-packet.md`

Include:

1. Verdict + link to review report  
2. “Do these three things” checklist  
3. Versioning rules in one sentence  
4. Exact file list to place in `04_revision-intake/input/<ID>/`  
5. “Do not edit the routing ledger”  
6. “Submission is complete when files are in 04 **and** you invoke the workflow”

**Why:** Formal review already has a “start here” cover. Author stop does not. Authors described 10–15 minutes just to trust the path.

#### P0.3 Submission receipt (author-owned, tiny)

Ship a one-line template authors drop into 04 with the package:

`<ID>-submission-note.md` → name, date, doc version, “responding to review-round-NN”

**Why:** Until a ledger row exists, 04 looks like debris. A receipt makes submission self-describing.

#### P0.4 Post-sign next step on the decision form

On the formal decision FORM footer, state in plain language:

1. Save as `<ID>-formal-decision.md` under `05_formal-review/output/<ID>/`  
2. Invoke the workflow (or notify the operator)  
3. Do **not** create `06_completed` yourself  
4. You are done when the status card says Completed

**Why:** Senior SA signed with residual “is the system watching this path?” anxiety.

---

### P1 — Collapse cognitive load without changing stages

#### P1.1 Single operator chat skill / runbook prompt (already half-promised)

Root README already has magic sentences. Promote them to a **named skill** (or pinned “commands” section) with four verbs only:

| Verb | Meaning |
|---|---|
| `start` | New package → ID, folders, ledger, intake… |
| `continue <ID>` | Run every automatic transition to next human stop |
| `status <ID>` | Print status card |
| `submit revision <ID>` | Validate 04 drop zone, write submission ledger row, continue |

**Why:** Operators re-read AGENTS + root CONTEXT + stage CONTEXT + templates every time. That is documentation, not UI.

#### P1.2 Round / version legend (one place, repeated)

Add a 4-line legend to author packet, revision-intake template, and status card:

```text
• SDD version bumps when design content changes (v1 → v2)
• Response log round = the review round you are answering
• Next editor review round = previous + 1 after complete revision intake
• Assumptions/requirements get a new filename only when their content changes
```

**Why:** Authors and operators consistently confuse `response-round-01` with `review-round-02`.

#### P1.3 Promote Deferred Review Areas on the review report

Move the “addressing these usually saves a round” tip from the response form onto the **review report footer**.

**Why:** Authors nearly miss deferred work; form tip saved a cycle in this run. Put the tip where eyes already are.

#### P1.4 Stage job banner in every stage CONTEXT (one line at top)

Examples already almost exist; make them banner-loud:

- 01: “Completeness only — not design quality”  
- 02: “Critic only — never rewrite”  
- 03: “Human stop — you own design content”  
- 04: “Traceability only — do not judge fix quality”  
- 05: “Human stop — you own architecture approval”  
- 06: “Terminal — read-only”

**Why:** Job boundaries are sharp in contracts and invisible in the “UI” of folders.

#### P1.5 Formal packet “architect brief” section (optional block on cover)

Add a short optional section to the formal cover sheet:

- Residual risks (top deferred items)  
- v1→v2 change bullets (from author “New material” + resolution check)  
- Suggested review time (e.g. 20 / 45 min)  
- Requirements coverage pointer (link to testing table if present)

**Why:** SA loved the packet but still wanted residual-risk chrome and a delta view.

---

### P2 — Polish, confidence, and delight

#### P2.1 Progress markers during multi-stage auto-runs

When chaining intake → review → route, write brief lines to the status card (or chat) as each stage completes:

`Intake complete → Review in progress → Routed to author revision`

**Why:** Long silent runs feel broken.

#### P2.2 Completion “done” surface

On enter 06, generate `<ID>-DONE.md` (or expand completion manifest top) with:

- Final decision + signer  
- Final SDD version  
- Open conditions (if AWC)  
- “This package is read-only; changes need a new review ID”

**Why:** Terminal state is correct but uncelebrated; authors never get closure feedback.

#### P2.3 Disposition notation consistency

Pick one: markdown checkboxes **or** free-text `resolved` / `partially resolved` / `disagree`. Document it on the form. Intake can remain human-readable; consistency still reduces anxiety.

#### P2.4 Open decisions always get IDs

Editor “business tradeoffs” (e.g. owner-continuity) should receive `OD-xx` slots so formal disposition is register-shaped, not hallway-shaped.

#### P2.5 Demo kit one-command path (docs only if no scripts)

Fixtures README is good. Add a copy-paste block that creates `NS-001` / `UX-001` input in one shot and the exact `start` utterance. Optionally a small shell script *outside* stage folders if you want zero friction — not required if docs are excellent.

#### P2.6 Guardrails as soft product rules (agent-facing)

Without changing folders:

- Refuse writes into a different review ID unless confirmed  
- Refuse to fill Decision/Rationale/Signature except when the user explicitly role-plays formal reviewer  
- Refuse to overwrite versioned SDD filenames  

These are already prose rules; make them fail-loud in AGENTS operating sequence.

#### P2.7 Name and framing consistency

Working title “Architecture Readiness Editor” vs repo “Design Review Editor” vs product language in README. Pick one user-facing name for onboarding. Not a structure change — pure labeling.

#### P2.8 SI-001 as “worked example,” not intimidation

Add a short note in README or author packet:

> Multi-round history (e.g. SI-001 at v7) is normal for hard packages. One clean revise → ready cycle (like UX-001) is also normal. Round count is not a grade.

**Why:** Authors psych themselves out seeing long histories.

---

## 6. Findings by persona

### 6.1 First-time submitter / demo operator

| Pain | Severity | Fix |
|---|---|---|
| No single “start a review” action | High | P0.1 + P1.1 |
| ID prefix meaning is tribal | Medium | Document in status + start flow |
| Easy to copy `expected-review` into intake | Medium | Fixture README checklist / start skill filters |
| Instruction stack spans many files | High | Operator skill + status card |
| Missing progress UI during auto-chain | Medium | P2.1 |

### 6.2 Design author (highest friction persona)

| Pain | Severity | Fix |
|---|---|---|
| Next action not on one screen | **Critical** | P0.2 author packet |
| Submission = silent folder copy | **Critical** | P0.3 receipt + status “awaiting intake” |
| Dual destinations (`03/output` vs `04/input`) | High | Author packet checklist |
| Version vs round confusion | High | P1.2 legend |
| Deferred areas easy to miss | Medium | P1.3 |
| Chat “I revised it” vs filesystem submit | High | Chat skill that files + submits |
| SI-001 multi-round intimidation | Low–Med | P2.8 framing |

**Author quote (paraphrased from journal):**  
*I could resolve the design findings with confidence. I would still ask a colleague “Did I submit correctly?” after copying to 04.*

### 6.3 Pipeline / agent operator

| Pain | Severity | Fix |
|---|---|---|
| Resubmission has no event | High | Status + `submit revision` verb |
| Round numbering easy to get wrong | High | P1.2 + auto-naming |
| Copy-forward overwrite is discipline-only | Medium | Soft guardrails P2.6 |
| Formal packet assembly is choreography | Medium | Ready-packet checklist in 02 CONTEXT (already prose; make it a template list) |
| Easy to overshoot Ready into fake approval | High | Hard stop messaging + P2.6 |

### 6.4 Senior solution architect (formal reviewer)

| Pain | Severity | Fix |
|---|---|---|
| Packet entry is strong | — | Preserve |
| Resolution check is excellent | — | Preserve |
| Save path `../../output/` is brittle | Medium | Absolute path + P0.4 |
| Residual risks buried in deferred | Medium | P1.5 architect brief |
| Post-sign “who advances 06?” | High | P0.4 + status card |
| Missing v1→v2 delta / time estimate | Medium | P1.5 |
| Uneven OD IDs | Low–Med | P2.4 |

**SA quote (paraphrased):**  
*I know what I’m holding and what I’m being asked to decide — then I signed into a folder and hoped the workflow was watching.*

---

## 7. Interaction design principles for this product

If you only remember five principles for future polish:

1. **State is a product surface.** The ledger is correct infrastructure; humans need a status card derived from it.  
2. **Every human stop needs a cover sheet.** 05 has one; 03 needs one; completion needs a “done” surface.  
3. **Submission and signature are events, not side effects.** Receipts + invoke instructions beat silent `cp`.  
4. **One job, one banner.** Stage contracts are clear; make the job impossible to miss at a glance.  
5. **Teach version/round once, show it everywhere.** This is the #1 recurring cognitive tax after “what next?”

---

## 8. Chat / agent UX (this is half the real UI)

Most users will not browse six stage trees. They will talk to an agent in this repo. Treat **chat as the primary UI** and folders as the audit backend.

### Recommended chat responses at each stop

| Stop | Agent should always say |
|---|---|
| After intake complete | “Package valid. Starting design review…” |
| After review → 03 | “Stopped for you (author). Open `…-author-packet.md`. I will not rewrite your SDD.” |
| After author says “I revised it” | “I’ll file these into `04_revision-intake/input/<ID>/` and run revision intake. Confirm?” |
| After Ready → 05 | “Document is ready for formal review — not approved. Open the formal packet. I will not sign.” |
| After signed decision filed | “Valid decision found. Completing package to `06_completed`…” |
| At 06 | “Done. Decision: … Final version: … Conditions: …” |

### Anti-patterns to ban in product copy

- “Just revise the design” without path + form + submit step  
- “Ready for Formal Review” without the readiness≠approval sentence in human-facing summaries  
- Offering to “clean up section 5 for you” in stage 02/03  

---

## 9. Content & microcopy suggestions

| Location | Suggested microcopy |
|---|---|
| Author packet title | “Your turn — revise, respond, submit” |
| Submit step | “Submit means: files in `04_revision-intake/input/<ID>/` + tell the agent to continue” |
| Deferred footer | “Addressing these now usually saves a full review round.” |
| Formal form | “Save the signed file here: `05_formal-review/output/<ID>/<ID>-formal-decision.md`. Then ask the agent to continue. Do not create Completed yourself.” |
| Status card when waiting on 04 files | “Author has not submitted yet (no files in revision intake).” |
| Status card when 04 has files but ledger still on 03 | “Revision files detected — not yet accepted. Invoke continue / submit revision.” |
| Completion | “Approved package is frozen. New changes → new review ID.” |

---

## 10. Severity-ranked backlog (implementation order)

| # | Item | Effort | Impact |
|---|---|---|---|
| 1 | Generate `reviews/<ID>-status.md` on every ledger write | Low | Very high |
| 2 | Generate author packet cover on route to 03 | Low | Very high |
| 3 | Formal form footer: save path + “invoke continue” + no DIY 06 | Low | High |
| 4 | Named chat verbs: start / continue / status / submit revision | Medium | Very high |
| 5 | Round/version legend (author packet + form + status) | Low | High |
| 6 | Deferred tip on review report footer | Trivial | Medium–High |
| 7 | Submission note template in 04 | Low | Medium |
| 8 | Formal cover “architect brief” block | Low–Med | Medium (SA) |
| 9 | Completion DONE blurb | Low | Medium |
| 10 | OD-id consistency for open decisions | Low | Medium |
| 11 | Soft agent guardrails (wrong ID, no fake signature, no overwrite) | Medium | High (safety) |
| 12 | Demo one-shot copy-paste / optional script | Low | Medium (judges/demo) |

**None of these require rearranging `01`–`06`.**

---

## 11. What not to change

- The six-stage ICM topology  
- Critic-only rules and five-finding cap  
- Human-only formal decision authority  
- Ledger as authoritative state  
- Copy-forward history model  
- Separation of 04 completeness vs 02 critique  
- Formal packet layering (`history/` demotion)  
- Fixtures staying outside live stage paths unless demo-started  

Those are load-bearing. “Seamless” means **better handrails**, not a different pipeline.

---

## 12. Is it perfect the way it is?

**No — and it does not need to be rebuilt.**

As a **judgment and governance system**, it is already high quality. The UX-001 run proved the happy path can converge in one author cycle when findings are clear and the author addresses deferred work.

As a **human product**, it is still a power-user process:

- First-time authors will not feel guided at the 03 stop  
- Submission and signature will feel like putting files in a black hole  
- Status will feel like archaeology  
- Operators will keep re-reading contracts they already trust  

If you implement only the **P0 status card + author packet + formal post-sign footer**, perceived seamlessness jumps dramatically without touching folder structure.

---

## 13. Evidence appendix (live UX-001)

| Milestone | Outcome |
|---|---|
| Round 01 verdict | Revise Before Formal Review (3 Blocking, 2 High) |
| Author | SDD v2 + assumptions v2 + completed response log |
| Round 02 verdict | Ready for Formal Review with Open Decisions |
| Formal decision | Approved with Conditions (3 non-blocking) by A. Chen (UX simulation) |
| Terminal | `06_completed` with completion manifest |

Supporting journals (raw persona notes):

- `reviews/UX-001-agent-journal-workflow-round-01.md`  
- `reviews/UX-001-agent-journal-author-round-01.md`  
- `reviews/UX-001-agent-journal-workflow-round-02.md`  
- `reviews/UX-001-agent-journal-formal-reviewer.md`  
- `reviews/UX-001-agent-journal-completion.md`  

Ledger: `reviews/UX-001-routing-log.md`

---

## 14. Closing recommendation

Treat the next iteration as **UX chrome on a correct engine**:

1. Make state and next action visible.  
2. Give authors the same “start here” love formal reviewers already get.  
3. Make submit/sign events explicit.  
4. Keep the critic pure.

That is the path from “brilliant process documentation you execute by hand” to “seamless design-readiness product” — without changing the folder structure you correctly want to protect.
