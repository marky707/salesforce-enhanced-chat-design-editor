# Design Review

## Verdict
Revise Before Formal Review

Multiple blocking gaps leave the review board unable to verify identity protection, routing SLA behavior, rollback topology, and retention compliance on critical paths.

> This verdict measures document readiness, not architecture approval. Final design approval remains with the accountable human architect and governance reviewers.

## Priority Findings

### 1. Email matching is treated as identity verification for protected data

- Severity: Blocking
- Lens: Failure
- Location: Section 4, "Customer identity and context"
- Evidence: "If one Contact matches, the flow treats the customer as identified and retrieves the Contact's Account, active Assets, contract tier, and three most recent service orders."
- Design gap: R-01 prohibits account, asset, contract, or service-order information until identity is verified, but the public flow treats an email match as identification and retrieves protected context. The portal fallback also downgrades unresolved signed-in identity to email matching instead of defining a verified-session failure path.
- Consequence: A public visitor who knows or guesses another customer's email and equipment serial number could expose account or service-order context, and agents are told they may share status once the panel loads.
- Author's task: What evidence constitutes verified identity for each entry point, and what context and agent disclosures are allowed when that evidence is absent or ambiguous?

### 2. Priority routing contradicts the 90-second specialist requirement

- Severity: Blocking
- Lens: Failure
- Location: Section 5, "Routing and capacity"
- Evidence: "If no certified specialist is available, the work remains pending until one becomes available so R-03 is not diluted by sending it to a general coordinator."
- Design gap: R-03 says Priority contract customers must reach a certified equipment specialist within 90 seconds during support hours, but the design defines an unbounded pending state when no specialist is available. No timeout, fallback, overflow behavior, staffing assumption, or failure outcome preserves or explicitly exceptions the requirement.
- Consequence: Priority chats can wait indefinitely while the design still claims alignment to R-03, leaving builders, QA, and operations without a testable expected result for the most time-sensitive route.
- Author's task: When no certified specialist can accept within 90 seconds, what exactly happens to the work item and customer experience, and who owns any requirement exception or risk acceptance?

### 3. Deployment topology conflicts with channel-specific rollback

- Severity: Blocking
- Lens: Flow
- Location: Section 3, "Proposed architecture" and Section 10, "Release and rollback"
- Evidence: "One Enhanced Chat deployment will serve the public support site and customer portal." / "If chat causes a production issue, Digital Support deactivates the Enhanced Chat deployment and restores the public contact form. The portal support link is hidden in the next portal configuration release."
- Design gap: R-07 requires public-site chat first, portal chat two weeks later, and a channel-specific rollback option, but the architecture uses one deployment and the rollback plan deactivates that shared deployment. The portal rollback also depends on a later configuration release, not an immediate channel-specific rollback.
- Consequence: The build team cannot know whether rollback is deployment-scoped, entry-point-scoped, or release-scoped, and a public-site incident could disable portal chat or leave portal rollback unavailable inside the required decision window.
- Author's task: What rollback unit is required by R-07, and how does the deployment topology support rolling back one channel without unintentionally changing the other?

### 4. Retention design can delete records under legal hold and leaves privacy deletion scope ambiguous

- Severity: Blocking
- Lens: Failure
- Location: Section 8, "Data, privacy, and retention"
- Evidence: "A nightly scheduled flow deletes MessagingSession records whose end date is more than 12 months old. Legal places a `Legal Hold` checkbox on the related Case when preservation is required. Privacy-deletion requests are completed by deleting the Contact and associated Cases through the existing privacy process."
- Design gap: The scheduled deletion rule does not exclude sessions whose related Case has legal hold, even though R-06 requires preservation. The privacy-deletion process names Contact and Case deletion but does not state what happens to MessagingSession, transcript bodies, ConversationEntry data, ERP summaries copied into Case description, or deletion exceptions.
- Consequence: The implementation could automatically delete legally preserved chat records or leave transcript data behind after an approved deletion request, creating a compliance failure that the formal review cannot responsibly waive.
- Author's task: Which records are retained, exempted, deleted, or preserved for legal hold and privacy deletion, and what owner or policy authorizes those behaviors?

### 5. Reporting and verification do not define measurable proof for R-08

- Severity: High
- Lens: Proof
- Location: Section 9, "Reporting and operations" and Section 11, "Verification"
- Evidence: "Operations dashboards use MessagingSession and Case report types to show average first response, sessions by contract tier, identity-match failures, after-hours chats, and ERP lookup success."
- Design gap: R-08 requires weekly measures for first response, Priority-contract routing, identity failures, after-hours capture, and ERP lookup success, but the design does not define source fields or metric types, populations, lifecycle boundaries, or pass/fail thresholds. "Dashboard records are created" in UAT proves record creation, not metric correctness.
- Consequence: Operations may manage staffing and incident response from numbers whose meaning is undefined, and QA cannot prove whether Priority routing, identity failures, after-hours capture, or ERP success are measured correctly.
- Author's task: For each R-08 measure, what object and field or metric type supplies it, what population is counted, what lifecycle events bound it, and what acceptance criterion proves it works?

## Open Decisions for the Senior Architect

- Whether email matching may ever satisfy the business meaning of "identity verified" for service-order, account, asset, or contract data. This needs accountable security/privacy judgment because the current design uses email matching to unlock protected context.

- Whether Priority customers should wait only for certified specialists or receive another bounded service path when no specialist is available. This is a business SLA and staffing tradeoff that Service Operations and the accountable architect must own.

- Whether a single Embedded Service deployment can satisfy R-07's channel-specific rollback requirement, or whether the rollback requirement changes the deployment topology. This needs architectural ownership because it affects release control, rollback speed, and deployment-scoped settings.

## Deferred Review Areas

- Section 6, RidgeLine ERP integration: retry count is stated, but timeout duration, duplicate-inquiry prevention, response authorization, and retry ownership are not tied back to R-04 — *likely next-round finding*

- Section 7, Conversation lifecycle and after-hours behavior: after-hours acknowledgment for next-business-day response is required by R-05 but not evidenced in the flow — *likely next-round finding*

- Section 3 diagram: the system context is too compressed to show trust boundaries, wrapper ownership, data direction, or exception paths across public site, portal, Salesforce, and RidgeLine — *likely next-round finding*

- Section 9, operations: monitoring names teams and dashboards but not health signals, thresholds, alert paths, or incident owners per signal — *build-entry validation*

- Section 11, Verification: one example per scenario is too thin to validate routing precedence, missing data, multiple contacts, specialist unavailability, rollback, and retention exceptions — *valuable improvement*

> Tip for the author: addressing these now usually saves a full review round.