# Omni-Channel Routing — Review Reference

What a complete routing design must define. Use this to find the undefined branch, the missing timeout, and the fallback that is a label rather than a target.

## Routing model — a major decision requiring rationale

- **Queue-based:** work routes to a queue; members with capacity receive pushes. Simple, coarse-grained; eligibility is membership.
- **Skills-based:** work carries skill requirements matched against agent skills. Finer-grained; adds skill-maintenance operational cost and a harder no-match question.
- **Omni-Channel Flow:** flow logic evaluates inputs and hands work to queue/skill/agent targets. Most flexible; the flow's decision logic becomes design surface that must itself be documented and testable.
- **Direct-to-agent / preferred agent:** routes to a specific person. Highest continuity, highest failure risk — see below.

A ready design states which model, why, and what alternative was rejected. "We will use Omni-Channel" is a product name, not a routing design.

## Every routing design must define

- **Inputs and precedence:** which attributes (language, product, priority, customer tier…) are evaluated, in what order, and the input-to-target matrix they produce
- **Conflict and missing-input behavior:** the branch for "Spanish VIP, no Spanish VIP queue" and for absent pre-chat data
- **Availability semantics:** what makes an agent eligible — presence status, channel capacity, queue/skill membership
- **Capacity model:** how much messaging work an agent carries concurrently and whether messaging work is interruptible by other channels; staffing math depends on it
- **Push timeout:** what happens when an agent doesn't accept — timeout value, next target, retry count
- **Queue overflow:** behavior at depth/wait thresholds — is there a threshold, and what changes when it's crossed?
- **No-eligible-target:** the terminal fallback when nothing matches — what does the customer see?
- **After-hours:** business-hours source of truth and the closed-hours experience per entry point

## Direct-to-owner / preferred-agent — the recurring blocking finding

Routing to a specific person requires all of:

1. Availability check semantics (what if offline, out of office, at capacity?)
2. A bounded wait — a timeout with a number and an owner for choosing it
3. A fallback target after the bound
4. Reporting visibility — a chat waiting on one person never appears in queue metrics unless the design makes it visible

A design with owner-routing and none of these has an unbounded, invisible wait state. Severity is almost always Blocking.

## Timeout inventory

A ready design owns a value and a next-action for every clock it introduces: push acceptance timeout, customer inactivity, agent inactivity, invitation/session expiration, and any flow-level waits. For each: the enforcing mechanism (platform setting, flow logic, custom code) and which system's clock is authoritative. "Invitations expire after N minutes" with no enforcing mechanism is an undefined behavior, not a design statement.

## What routing choices do to reporting

Routing model choices silently define metric semantics: skills-based routing makes "queue wait time" partially meaningless; owner-routing bypasses queue metrics entirely; flow-based routing can create AgentWork later than session creation, changing what "wait" measures. Cross-check every routing decision against `lifecycle-and-reporting.md`.
