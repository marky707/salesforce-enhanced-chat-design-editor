# Security & Operations — Review Reference

What a ready design says about identity, data handling, monitoring, deployment, and rollback. The editor reviews for presence, specificity, and testability — it never certifies security or compliance.

## Identity and authentication

- **Verified vs. unverified users:** is user verification in scope? If chat serves logged-in customers, the design must show the token/handoff flow and the fallback experience for unverified sessions. If unverified, the design must state what identity claims are trusted (none) and how sessions link to Contact records without trusting customer-typed input.
- **Agent-side access:** which profiles/permission sets see MessagingSession, transcripts, and linked records; is transcript visibility appropriate for the data customers paste into chats?

## Data handling and retention

- What sensitive data can enter via chat (customers type anything) and whether masking/redaction rules are in scope
- Retention: how long ConversationEntry/transcript data lives, driven by which policy — a named policy owner, not "TBD"
- Encryption/Shield claims: flag as unsupported unless the design states what is licensed and verified

The editor's job is to confirm these questions are **answered and owned**, not to judge the answers' compliance.

## Monitoring — the most commonly missing section

A ready design names, before go-live:

- **Health signals:** queue depth/wait beyond threshold, routing failures, no-eligible-agent occurrences, integration error rate, session-creation failures from the wrapper
- **Where each signal lives:** which dashboard/report on which object, or which log — and its refresh reality
- **Who watches:** the operational owner per signal, and what threshold triggers action
- **Alerting path:** how a breach reaches a human outside the dashboard

"Supervisors will monitor dashboards" without signals, thresholds, and owners is a finding, not a monitoring design.

## Failure operations

- Retry ownership for failed integrations (system retries? agent retries? nobody?)
- Degraded-mode behavior: chat down → what does the website show; routing down → what happens to created sessions
- Escalation: how a systemic failure (not one chat) reaches the team that can fix it

## Deployment and rollback

- **Cutover shape:** phased (by region/channel/population) vs. single cutover — a major decision needing rationale and different rollback stories
- **In-flight work:** what happens to active legacy chats (migration) or active sessions (config changes) at the moment of change
- **Rollback:** the concrete path back if go-live fails — what is restored, what data is stranded, how long the decision window stays open, who decides
- **Parallel running:** if legacy and enhanced run simultaneously, how demand is split and metrics kept separate

A migration design with no rollback section leaves the org one bad go-live from an unrecoverable state; treat its absence as High at minimum.

## Post-go-live proof

The Proof lens applied to operations: which numbers, at what time after launch, will demonstrate the system is healthy — and against what baseline? For migrations, the legacy baseline mapping in `lifecycle-and-reporting.md` is the comparator.
