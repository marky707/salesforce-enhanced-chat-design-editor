# Required Diagrams

An Enhanced Chat / Omni-Channel design normally needs six diagrams. The editor reviews each for clarity, completeness, and consistency with the prose — the existence of an image is not the standard. When a diagram is missing or insufficient, the finding states **what relationship or behavior the diagram must clarify**; the editor never creates it.

## 1. System context diagram

Must show: end users (web and/or in-app), Salesforce, the frontend applications hosting the chat, external systems, and the trust boundaries between them.
Insufficient when: external systems appear without direction of data flow; the wrapper/host app is missing; trust boundaries are undrawn so security review has no surface to assess.

## 2. End-to-end process flow

Must show: customer actions, agent actions, system handoffs, decision points, and exception paths from chat initiation to conversation end.
Insufficient when: only the happy path appears; decisions have one exit; the diagram ends at "agent accepts" and skips wrap-up, transfer, and end states; prose describes steps the diagram lacks.

## 3. Omni routing decision flow

Must show: routing inputs, evaluation order, eligibility, priority, availability and capacity checks, timeout values, and every fallback branch — including "no eligible target."
Insufficient when: inputs are named but not ordered; timeout branches are absent; fallback is a label ("escalate") with no target; the queue/skill matrix implied by prose is not derivable from the diagram.

## 4. Conversation lifecycle / state diagram

Must show: session states from creation through routing, acceptance, active handling, inactivity, reopening where applicable, ending, and invalid states — with the events that cause each transition.
Insufficient when: states appear without transition triggers; inactivity and expiration are missing; the "reopened" path exists in prose but not in the diagram; end states don't distinguish customer-ended, agent-ended, and system-ended.

## 5. Data relationship diagram

Must show: MessagingSession, AgentWork, Case (or the related record), MessagingEndUser/contact linkage, and every custom object or relationship the design proposes.
Insufficient when: custom objects appear without cardinality; the native relationships the customization duplicates are omitted, hiding the redundancy; reporting sections reference relationships the diagram doesn't show.

## 6. Integration sequence diagram

Required when external systems participate. Must show: ordered calls and events, acknowledgements, timeout and retry behavior, and which side owns each step.
Insufficient when: arrows lack direction or order; failures/timeouts have no return path; ownership at each hop is unlabeled; asynchronous steps are drawn as synchronous.

## Cross-diagram consistency

The same actor, system, queue, and state names must appear across all diagrams and the prose. A queue that exists in the routing flow but not the process flow, or a state in prose absent from the lifecycle diagram, is a contradiction finding — often the highest-value finding in the document.
