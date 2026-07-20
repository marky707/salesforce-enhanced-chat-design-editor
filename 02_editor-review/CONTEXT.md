# 02_editor-review — Stage Contract

**One job:** perform the critic-only readiness review. Nothing else.

## Persona activation

Entering this stage, adopt the editor identity in `identity.md` and obey `rules.md` completely. Load selectively:

1. `identity.md` — who is reviewing (always)
2. `rules.md` — critique behavior, verdicts, output contract (always)
3. `reference/CONTEXT.md` — router to the domain reference that answers the current review question (load referenced files on demand, not all at once)
4. `examples.md` — consult when unsure whether a draft finding is specific enough

The persona and references load **only** in this stage. Leaving this stage, drop them.

## Input (`input/<ID>/`)

- The latest validated package (draft SDD, requirements, assumptions, diagrams)
- On round 2+: the previous review report and the author's revision-response log

## Output (`output/<ID>/`)

- `<ID>-review-round-<NN>.md` — verdict plus at most five prioritized findings, in the exact output contract of `rules.md`

## Routing

- **`Revise Before Formal Review` or `Insufficient Context` →** copy the package plus the new review report to `03_author-revision/input/<ID>/`. Also generate there:
  1. `<ID>-revision-response-round-<NN>.md` from `03_author-revision/revision-response-template.md`, pre-populated with one block per finding (number and title filled in; answer lines left blank — pre-filling titles is administrative, answering them is the author's).
  2. `<ID>-author-packet.md` — the author's cover sheet ("Your turn — revise, respond, submit"), with every file as a relative markdown link: the verdict + link to the review report; a compact finding index (`#`, severity, lens, location, response-form anchor); a three-step checklist (1. finish your revision wherever you work — chat users just attach the finished files at step 3 and the agent retains author copies in `03_author-revision/output/<ID>/` for the audit trail; folder users may work there directly, 2. complete the pre-filled response form, 3. **attach every changed submission artifact in chat and say `submit revision <ID>`** — the agent files them and preflights automatically (or copy them into `04_revision-intake/input/<ID>/` yourself first; either path works)); the round/version legend below, verbatim; the exact candidate file list; the deferred-area timing labels; "do not edit the routing ledger"; and "file placement is detected evidence, but submission is complete only when the files are in 04 **and** you invoke the workflow." Author-facing packets are **chat-first** (attach + verbs as the primary path, folders as the alternative) and use operator verbs only — never raw CLI commands.

  Round/version legend (include verbatim in every author packet):
  ```text
  • SDD version bumps when design content changes (v1 → v2)
  • Response log round = the review round you are answering
  • Next editor review round = previous + 1, after complete revision intake
  • Requirements/assumptions get a new versioned filename only when their content changes
  ```
  Append ledger row, regenerate the status card, stop (human stop follows).
- **`Ready for Formal Review` or `Ready for Formal Review with Open Decisions` →** deliver a **layered packet** to `05_formal-review/input/<ID>/`. At the top level include only actionable current material: current SDD, ready review, current requirements and decision register, `<ID>-formal-review-packet-round-<NN>.md`, `<ID>-open-decision-index-round-<NN>.md`, `<ID>-formal-decision-round-<NN>-FORM.md`, and `<ID>-current-artifacts-round-<NN>.md`. Do **not** copy the stable `formal-decision-template.md`; it remains in the stage root as the source template. Everything superseded (earlier rounds, responses, prior drafts and artifact versions) goes in `history/`. Round-versioned names prevent a later formal-review cycle from overwriting its predecessor.

  Generate the formal artifacts as follows:
  1. **Cover:** current material, suggested reading order, link to the authoritative decision index, structured residual-risk table (risk, source, proposed owner/required concurrence, evidence, due gate, blocking level), outcome-specific next-step microcopy, and a one-paragraph history summary. It summarizes and points; it never argues for approval. Next-step microcopy uses operator verbs only and matches the status card: after signing, the reviewer just says `continue <ID>` — validation happens automatically.
  2. **Decision index:** one row per open decision using `05_formal-review/open-decision-index-template.md`: ID, source, raised when, state, required authority, missing evidence, bounded decision question, and SDD/requirement link. This index is authoritative for this formal-review round and must explicitly say when it supersedes older counts embedded in the submitted SDD/register.
  3. **Decision FORM:** create from the stable template with administrative fields and one blank disposition block per decision (selected option, reviewer rationale, required concurrence, condition/required change, blocking status). Decision, overall Rationale, Conditions, Required changes, and Signature stay blank for the human.
  4. **Artifact manifest:** after the ledger routes to `05`, run `python3 tools/review_state.py manifest <ID> --write` to create a checksummed inventory; then regenerate status and run `validate-state <ID>`.

  Reference every file with relative markdown links. Append the ledger row, generate the manifest/status, validate, and stop for the human.

## Prohibitions

Do not rewrite, complete, or generate design content or diagrams. Do not approve. Do not re-run intake validation as a substitute for critique. Do not exceed five findings.
