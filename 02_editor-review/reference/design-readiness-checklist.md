# Design Readiness Checklist

The formal-review readiness standard, expanded into checkable items. The document is ready only when all five criteria hold; any blocking condition forces `Revise Before Formal Review`.

## 1. Process flows are understandable

- [ ] Actors and systems are named consistently across prose and diagrams
- [ ] Every handoff shows who gives, who receives, and what crosses
- [ ] Decision points show inputs, precedence, and all outcomes
- [ ] State changes are explicit (session states, work item states, record status)
- [ ] Material exception paths are visible, not just the happy path

## 2. Rationale is documented

- [ ] Every major decision (see `why-flow-failure-proof.md`) cites its requirement
- [ ] Constraints that shaped the decision are stated
- [ ] Credible alternatives and accepted tradeoffs appear — or a mandated constraint explains their absence
- [ ] Implementation and operational consequences are acknowledged

## 3. Requirements coverage is complete

- [ ] Every material requirement maps to a design element
- [ ] Every material requirement appears in a process flow
- [ ] Every material requirement has a validation method
- [ ] No design element exists without a driving requirement (gold-plating check)

## 4. Critical failures are addressed

- [ ] Agent unavailable / at capacity / declines / push timeout
- [ ] Routing failure and no-eligible-target
- [ ] Session creation, wrapper initialization, and context-passing failures
- [ ] Integration failure and timeout, with retry and ownership
- [ ] Expiration behaviors with a named enforcing mechanism and time authority
- [ ] Business-hours closure, invalid-record, and missing-data behaviors
- [ ] Recovery: what is retried, logged, escalated, recovered

## 5. The design is testable

- [ ] Developers and QA can determine expected behavior without inventing rules
- [ ] Each metric names its source object, fields, and bounding lifecycle events
- [ ] Acceptance criteria are thresholds, not sentiments
- [ ] Post-deployment health has named signals and owners

## Blocking conditions — any one forces "Revise Before Formal Review"

1. A critical flow cannot be followed.
2. A major decision has no defensible rationale.
3. A requirement has no design coverage.
4. A high-risk failure has no defined behavior.
5. A design statement cannot be tested.
6. The diagrams, tables, and prose contradict one another.

## Verdict mapping

- Any blocking condition, or multiple High-severity gaps → **Revise Before Formal Review**
- Coherent, but explicit tradeoffs need accountable human judgment → **Ready for Formal Review with Open Decisions**
- No material readiness gaps → **Ready for Formal Review**
- Too little evidence to review responsibly → **Insufficient Context**
