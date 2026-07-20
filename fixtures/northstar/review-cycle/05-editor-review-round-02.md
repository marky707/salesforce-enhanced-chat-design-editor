# Design Review — UX-015 — Round 02

## Verdict

Ready for Formal Review with Open Decisions

The v2 design resolves all five round-01 readiness gaps and is coherent and testable enough for formal review; five explicit business, operating, security, and requirements-governance choices remain for accountable human judgment.

> This verdict measures document readiness, not architecture approval. Final design approval remains with the accountable human architect and governance reviewers.

## Prior Finding Dispositions

- Finding 1 resolved: Sections 6.5–6.6 replace unbounded owner routing with eligibility checks, a 30-second owner offer, defined pool/overflow fallbacks, 75/90-second escalation points, and operational visibility.
- Finding 2 resolved: Sections 6.1–6.7 define input precedence, normalization, eligibility, target matrices, priority values, fallback timing, no-eligible-target behavior, and after-hours handling for both OD-01 candidates.
- Finding 3 resolved: Sections 4 and 10 consistently define two channel-specific deployments, shared routing governance, separate release waves, ownership, health signals, and rollback paths.
- Finding 4 resolved: Sections 2.3 and 8 remove `Chat_Interaction__c`, choose the native MessagingSession-to-Case relationship, and document the maintenance/reporting tradeoff.
- Finding 5 resolved: Section 11 names lifecycle sources and boundaries for each KPI, handles multiple AgentWork and exception populations, maps Legacy Chat comparison, and makes R-05/R-06 testable. The separate R-05 threshold-governance question is carried as OD-E02 below.

## Priority Findings

No priority findings. The remaining items are bounded judgment calls or implementation-verification details that do not require another author revision before formal review.

## Open Decisions for the Senior Architect

### OD-01 — Pro Gear routing model
- **Raised by:** author register
- **State:** ready for architect disposition
- **Required authority:** accountable senior architect + Support Operations
- **Missing evidence:** explicit concurrence on staffing-governance tradeoff
- **Decision question:** Select skills-based routing or a dedicated queue after accepting the documented capacity-flexibility versus skill/queue-governance tradeoff in Sections 6.3 and 6.7.

### OD-02 — Case transcript access
- **Raised by:** author register
- **State:** Security/Privacy concurrence needed
- **Required authority:** accountable senior architect + Security/Privacy
- **Missing evidence:** concurrence on access, duplication, retention, legal hold, encryption, deletion
- **Decision question:** Select native-transcript reference or file attachment after Security/Privacy accepts the documented consequences in Section 12.

### OD-03 — Proactive invitation wording
- **Raised by:** author register
- **State:** content missing
- **Required authority:** e-commerce product owner + accountable architect
- **Missing evidence:** final customer-facing invitation wording artifact/snippet to approve
- **Decision question:** Approve or change the page allowlist, 30-second trigger, seven-day dismissal suppression, five-minute expiry, **and final customer wording** described in Section 13. Because no draft invitation wording is present, this entry cannot be dispositioned as an approval until content exists or the question is reframed to policy parameters only.

### OD-E01 — Returning-customer continuity
- **Raised by:** editor this round (carried from round 01)
- **State:** ready for architect disposition
- **Required authority:** accountable senior architect + Support Operations
- **Missing evidence:** acceptance of continuity benefit versus timing risk
- **Decision question:** Decide whether the bounded 30-second owner preference in Section 6.5 provides enough continuity value to justify its remaining R-05 timing risk, or whether all work should route directly to the context-qualified pool.

### OD-E02 — R-05 acceptance interpretation
- **Raised by:** editor this round
- **State:** requirement-owner confirmation needed
- **Required authority:** R-05 requirement owner + accountable senior architect
- **Missing evidence:** written reconciliation of unqualified requirement and 95% criterion
- **Decision question:** Reconcile requirement R-05's unqualified statement that customers receive a first response within two minutes with Section 14's acceptance threshold of “at least 95%.” Confirm whether 95% is an accepted SLA interpretation or whether the requirement/acceptance criterion must change.

## Deferred Review Areas

- Section 7.1: Verify in the target Salesforce release the stated same-session resume behavior and the exact supported configuration for the 15-minute inactive / 24-hour close model before build sign-off (`build-entry validation`).
- Section 8.2 and Section 11.1: The document intentionally defers physical API-field mapping to target-org validation; retain that mapping test as an implementation entry criterion (`build-entry validation`).
- Assumptions A-02 and A-04: Load testing and operational staffing validation remain necessary because four bilingual agents and unchanged headcount may constrain the documented 90-second acceptance target (`build-entry validation`).
- Assumption A-06 and Section 12: Legal/Privacy must confirm or replace the proposed 24-month transcript retention period before production configuration (`build-entry validation`).

> Tip for the author: addressing these now usually saves a full review round.
