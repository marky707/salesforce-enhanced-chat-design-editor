# Revision Response Log — <REVIEW-ID> — Round <NN>

<!-- Stable template: contains no run-specific facts.
     PIPELINE NOTE: the agent routing a review to 03_author-revision generates a
     pre-populated copy of this form in the author's packet — one block per finding,
     with the finding number and title already filled in. The author only completes
     the three answer lines in each block. -->

## How to fill this out (takes ~10 minutes after you've revised your document)

For **each finding** below, answer three things:

1. **Disposition** — mark one: `resolved` / `partially resolved` / `disagree`
2. **Where** — the section, table, or diagram of your revised document that changed (or "no change" if you disagree)
3. **Why** — 2–3 sentences **in your own words**. Plain language is fine; you are explaining, not writing a formal document. If you disagree, say why — disagreement is allowed when you argue it from a requirement or constraint.

Do this **after** you've finished revising. Every finding must have a block, including ones you disagree with. Honesty beats polish: "I couldn't resolve the Case-failure part yet, need platform team input" is a *good* answer.

**Tip:** the review's *Deferred Review Areas* section is a preview of likely future findings. Addressing those items in this same revision usually saves you a full review round — note anything you tackled under "New material introduced this round."

**If you changed a supporting artifact** (requirements list, assumptions/decisions register): give it a new versioned filename, list it under "New material introduced this round," and **re-read it once against your revised SDD before submitting** — the most common resubmission failure is a supporting artifact that quietly disagrees with the SDD or with this log (e.g. text pasted from the wrong document, or a register still calling "open" a decision your SDD closed). Revision intake cross-checks all three and will bounce a contradictory package.

- **Review ID:**
- **Responding to:** `<ID>-review-round-<NN>.md`
- **Revised document version:**
- **Author (human actor):**
- **Date (ISO 8601):**

---

## Finding <N>: <finding title, pre-filled by the agent from the review>

- **Disposition (mark one):** [ ] resolved  [ ] partially resolved  [ ] disagree
- **Where the design changed:**
- **What changed / why (your own words):**

<!-- The generated copy repeats this block once per finding, titles pre-filled. -->

---

### Example of a completed block (delete from your copy)

## Finding 2: Push timeout behavior is undefined

- **Disposition (mark one):** [x] resolved
- **Where the design changed:** Section 4.2
- **What changed / why (your own words):** I added a 30-second push timeout — if the agent doesn't accept, it goes to the next available agent. I picked 30 seconds because that's what our phone team uses for ring time.

---

## New material introduced this round

<!-- New sections, diagrams, or supporting files the editor has not seen before. -->

-
