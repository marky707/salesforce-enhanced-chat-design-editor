# Enhanced Chat Architecture — Review Reference

What a reviewer needs to know about Enhanced Chat to judge a design's plausibility. This supports critique; it is not product documentation, and claims beyond well-established behavior should be flagged as unsupported rather than corrected from memory.

Enhanced Chat behavior can differ by web or in-app surface, deployment version, enabled features, and Salesforce release. When a design depends on a version-specific capability, require it to name the applicable surface/version and cite documentation or target-environment verification. Do not assume that a capability or limitation applies identically across every Enhanced Chat experience.

## Core components a design must account for

- **Messaging channel** — the channel definition (Messaging for In-App and Web type) that conversations arrive through.
- **Embedded Service deployment** — the deployment configuration binding a channel to a surface: web (snippet on a site) or mobile (SDK in an app). Deployment-scoped settings include pre-chat, branding, and routing entry. A design must state **how many deployments** exist and which surface each serves; many settings cannot differ within one deployment.
- **Omni-Channel entry** — routing is configured per channel/deployment via queues, skills, or an Omni-Channel Flow. See `omni-channel-routing.md`.
- **MessagingSession** — the conversation record; the anchor for lifecycle and most reporting. See `lifecycle-and-reporting.md`.
- **MessagingEndUser / MessagingChannel consent** — identity of the person messaging, linkable to Contact/Lead; designs handling returning customers must say how identity is established (verified vs. unverified).
- **ConversationEntry** — the message-level data; relevant to transcript, compliance, and some metrics.
- **Pre-chat and hidden pre-chat fields** — structured data collected or passed before routing; a common carrier for context from the host application.
- **Auto-responses / messaging components** — system messages, acknowledgements, and structured content the design may rely on for expectation-setting.

## Frontend wrapper responsibilities

For in-app chat (and custom web integrations), a host-application wrapper embeds the SDK/snippet. A ready design assigns ownership for each of:

- Initializing the deployment and handling initialization failure (what does the user see?)
- Passing context (pre-chat/hidden fields): payload contract, validation side, behavior when absent or malformed
- Version coordination: SDK/app releases vs. Salesforce-side deployment changes — who owns compatibility, and how is a breaking change caught before customers do?
- Authentication handoff when user verification is in scope

Unowned wrapper responsibilities are a recurring source of unclear-ownership findings.

## Migration from Legacy Chat — what changes

Designs migrating from Legacy Chat (Live Agent) must not assume equivalence. Reviewable differences include:

- **Object model:** Legacy `LiveChatTranscript` vs. `MessagingSession`/`ConversationEntry` — reporting continuity requires explicit metric remapping, not renamed dashboards.
- **Session persistence:** Enhanced Chat conversations can be asynchronous/resumable; Legacy Chat sessions were ended-when-closed. Lifecycle, staffing, and metric definitions all shift.
- **Routing:** Legacy Chat buttons/skills vs. Omni-Channel queues/flows — routing logic must be redesigned, not transcribed.
- **Deployment surface:** Legacy snippet/button configuration vs. Embedded Service deployments — settings do not map one-to-one.
- **Cutover:** a design must state what happens to in-flight legacy chats at cutover and whether the two systems run in parallel; "single cutover" and "phased by channel/region" have very different failure profiles and rollback stories.

## Plausibility red flags

- A single deployment claimed to serve surfaces with different pre-chat, branding, or routing needs
- Custom Apex/LWC proposed for behavior the platform provides (session timeout, auto-response, transfer) with no verification the native path fails
- Context passing asserted with no payload contract or failure behavior
- Legacy Chat concepts (buttons, chat hours on buttons, transcript object) carried into the Enhanced Chat design unchanged
- Any specific numeric platform limit quoted without citation — treat as an unsupported claim for the author to verify
