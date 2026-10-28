# Distilling Session Feedback

Improve future execution from evidence in a session: failures, corrections, avoidable work, and successful techniques worth reusing. Preserve the scope and exact constraints of the original instruction.

## Method

1. Audit the execution trajectory using the checks below, including sessions that completed successfully. Identify the relevant action, result, and evidence. Separate the user's instruction from an inferred explanation.
2. Diagnose the cause and choose a remedy using the causal check below. A prompt change is one possible remedy, not the default for every failure.
3. Determine applicability: personal preference, repository convention, contract-specific behavior, or a demonstrated reusable pattern. One incident alone does not establish a universal rule.
4. Remove incidental identities and transient markers while preserving exact limits, exceptions, relevant contract details, and authorization boundaries. Retain a concrete example when it makes the lesson testable.
5. Select the canonical owner using the routing table below and the shared workflow in [SKILL.md](../SKILL.md). Make the smallest change that fully addresses the cause. An explicit request to apply an understood correction authorizes that edit; ask only if the intended meaning remains unresolved.
6. Check the correction against the original case and a nearby case that should remain unaffected. Use the verification record below to state the evidence and remaining uncertainty.

## Execution Trajectory Audit

Inspect the relevant sequence of decisions, tool calls, artifacts, and user feedback. A correct final artifact can still hide avoidable work or unreliable execution. Use targeted transcript excerpts; expand the inspection when the cause or sequence is unclear.

| Lens | What to inspect | Evidence to retain |
|---|---|---|
| Explicit corrections and failures | Ignored requirements, tool errors, incorrect artifacts, broken contracts, or user intervention | The original requirement, the conflicting action or output, and its consequence |
| Inefficiencies | Repeated searches or reads, unnecessary full-file ingestion, repeated deterministic work, or independent operations serialized without a reason | Which work repeated, what information it contributed, and any measured time or token cost |
| Unnecessary steps | Questions already answered by the prompt, unrelated inspection, redundant approvals, or narration that obstructed progress | The information already available and the step it made unnecessary |
| Wrong decisions or ordering | Invented arguments or facts, action before required evidence arrived, skipped verification, premature success claims, or cyclic retries | The decision point, missing evidence, and the resulting failure or risk |
| Successful techniques | A reusable check, helper, example, or recovery path that demonstrably improved completion | The conditions under which it helped and the observable result |

Do not classify all sequential work as inefficient or all repeated reads as waste. A dependency, changed file, failed lookup, or necessary verification can justify them. Treat unmeasured optimization ideas as hypotheses; script offloading and parallelism have setup and coordination costs.

## Causal Check & Remedy Selection

For each candidate lesson, connect **observation -> supported cause -> proposed remedy -> expected observable result**. Explain why the remedy should address that cause and under which conditions it applies.

- Distinguish a missing instruction from failure to follow an existing instruction. Check whether the existing rule was discoverable, contradictory, or obscured before adding another copy.
- Check whether the issue belongs to an input, script, environment, tool contract, or stale reference. Fixing a broken helper or dependency may be more effective than adding a prompt restriction.
- Consider alternative explanations. If the transcript supports only a hypothesis, label it and choose a check that could confirm or disprove it; do not encode it as an established rule.
- Prefer a mechanism that addresses recurrence in the intended scope. A one-off recovery action need not become a permanent instruction.
- For an optimization, preserve correctness and required evidence. Compare the work avoided with the setup cost; do not claim savings from fewer lines or tool calls alone.

Example: an invented CLI flag may result from unavailable command help, outdated documentation, or an ignored command example. Inspect which occurred. Update the command source, improve its discovery, or correct the helper as appropriate; a blanket instruction to ask the user for every flag would add friction without addressing all of these causes.

## Canonical Owner Routing

Inspect existing owners and callers before selecting a destination. These are placement criteria, not instructions to create a new file for each lesson.

| Lesson concerns | Preferred owner | Keep elsewhere |
|---|---|---|
| Language conventions, formatting, or repository-wide coding rules | Existing shared coding instructions | References from affected workflows |
| Test conventions, fixtures, or environment preconditions | Shared testing guidance or the affected test runner, according to what is broken | Task-specific invocation and required inputs |
| Architecture or a cross-workflow development policy | Existing shared architecture or development instructions | Links from the workflows that consume it |
| Agent responsibility, selection, or coordination | The relevant agent definition, or a shared router if several agents consume the same rule | Procedural details in the owning skill; no mandatory handoff section for every agent |
| Task procedure, mode selection, or workflow-specific recovery | The owning skill or its conditional reference | A short routing link from its entrypoint when detail is offloaded |
| Schemas, detailed examples, or substantial lookup material | The relevant reference or asset, according to whether it guides execution or becomes output | A discoverable link with a read/use condition |
| Deterministic behavior, argument validation, or repeated transformation logic | The existing helper script, with an appropriate regression check | The invocation in the calling skill |
| Contract-specific data or behavior | That contract and its fixtures, within its declared scope | Broader guidance only when evidence supports a broader rule |

If a suitable owner already exists, update it and adjust affected callers. Put independently useful rules in their respective owners when a correction spans concerns; do not duplicate one rule across all affected files. A temporary workaround can remain in the task report rather than entering the reusable instruction set.

## Scope-Preserving Examples

| Feedback or evidence | Faithful instruction | Avoid |
|---|---|---|
| One consumer requires `null` for an absent optional collection | Preserve that consumer's declared absence semantics; distinguish missing and empty according to the contract | Requiring `null` for all optional collections in every API |
| User says "at most two questions" | Ask at most two questions per turn in the stated scope | Rewriting the limit as two to three |
| A named test dependency was stopped | Verify the dependencies declared by the selected test suite before running it | Starting every local service or inventing a container name |
| Two components drifted after copying the same standard | Keep the standard in its canonical owner and link affected callers | Adding another paraphrase to each component |
| A user supplies an exact identifier required by an output contract | Preserve it in the relevant contract or fixture | Removing required identifiers merely because they look session-specific |

## Verification Record

For a consequential correction, include these facts in the task's normal report; use a table or prose according to what is easiest to review:

- **Observation and evidence:** the relevant request, execution step, output, or user correction.
- **Cause and confidence:** what the evidence establishes, alternative explanations, and any unresolved hypothesis.
- **Applicability and owner:** where the lesson applies, where it does not, and the authoritative file or helper.
- **Change and rationale:** what changes and why it should address the cause, including any trade-off or retained exception.
- **Verification:** the original case, a nearby unaffected case, expected versus observed results, and checks actually performed.

Report inspection, an executed script check, and an actual agent run distinctly. A passing linter establishes structure, not that a workflow correction works in practice. If behavioral execution is unavailable, state that limit and the unverified expectation.

Store a durable fixture when it will support meaningful future regression checks. If verification contradicts the proposed cause or exposes a regression, revise or withdraw the correction rather than accumulating exceptions to defend it.
