# Why → Flow → Failure → Proof — Probing Questions

The core review lens, expanded into the questions the editor actually asks of an Enhanced Chat / Omni-Channel design. Use these to interrogate each material decision; a finding exists where the document cannot answer.

## Why — is the decision justified?

- What requirement or business outcome drives this decision? Is it cited by ID?
- What constraints shaped it (license edition, staffing, existing org customization, compliance mandate, timeline)?
- Why is the selected approach appropriate for *this* org — not in general?
- For a **major decision**, what credible alternative was rejected, and what tradeoff was accepted? A decision is major when it is expensive to reverse, affects security or operations, introduces customization, crosses a system boundary, or changes how users or data move. Typical Enhanced Chat examples:
  - Native capability vs. custom Apex/LWC
  - Native record relationships vs. a custom junction object
  - Queue-based vs. skills-based routing
  - Direct-to-owner / preferred-agent vs. queue routing with fallback
  - One Embedded Service deployment vs. several
  - Synchronous vs. asynchronous integration
  - MessagingSession vs. MessagingSessionMetrics vs. AgentWork as a reporting source
  - Phased rollout vs. single cutover
- If only one option is viable because of a mandated constraint, is that constraint stated — rather than fake alternatives invented?

## Flow — can a reviewer follow it?

- Can you walk the happy path end-to-end: customer action → system behavior → agent action → state change → resolution?
- Are the exception paths visible, or only the happy path?
- At every handoff (wrapper → Salesforce, queue → agent, agent → agent, Salesforce → external system): who owns the interaction on each side, and what crosses the boundary?
- Do the diagrams and the prose describe the same system? Contradictions are findings in their own right.
- Are decision points explicit — inputs, precedence, and the outcome for every branch including "none of the above"?
- Could two developers read this section and build the same behavior?

## Failure — what happens when it breaks?

- Agent unavailable, at capacity, declines, or lets the push request time out — where does the work go?
- Routing fails to find any eligible target — what does the customer see, and is the session recoverable?
- Session creation fails, the wrapper fails to initialize, or context fails to pass — logged where, retried how, surfaced to whom?
- An integration call fails or times out mid-conversation — is the failure visible to the agent, and who retries?
- Invitation or session expiration: what enforces the timeout, and which system's clock is the authority?
- Business hours close mid-queue, a case becomes invalid mid-route, expected data is missing — defined behavior or undefined?
- For each failure: what is retried, what is logged, what escalates, what recovers — and what does the customer experience meanwhile?

## Proof — how will anyone know it works?

- How will each requirement be tested — and can expected behavior be determined from the document alone, without inventing rules?
- Which object, field, event, log, or metric proves the behavior at runtime?
- What is the acceptance criterion — a threshold, not a sentiment?
- After go-live, how does operations know the system is healthy — which dashboards, on which sources, watched by whom?
- Are metric definitions bounded by two named lifecycle events on a named object? "Wait time" without both is not a definition.
- For migrations: how do new metrics map to the legacy baselines success will be judged against?
