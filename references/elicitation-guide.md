# Resolving Missing Decisions

Read the request, relevant workspace evidence, and existing decisions first. Do not repeat questions already answered in a prompt, handoff, or approved plan.

This reference owns discovery coverage, clarification mechanics, and the decisions needed to define an executable workflow. Use the shared workflow in [SKILL.md](../SKILL.md) for authoring and verification, and [session-distillation.md](session-distillation.md) for interpreting session feedback.

## Ask or Proceed

Ask when the missing answer changes scope, intended behavior, an output contract, authority, or an irreversible action. Continue independent work while waiting where possible. Do not invent business facts, stakeholder decisions, or runtime capabilities to fill a gap.

For reversible implementation mechanics such as Markdown layout or helper organization, use established conventions. State a choice when it materially affects review; do not turn every routine choice into an approval gate.

For an interactive workflow, begin with the most consequential unresolved decision. Default to one to three related questions; preserve an explicit user question limit exactly. Ask about detailed branches only after the branch becomes relevant.

When concrete alternatives exist, give a recommended option and concise pros/cons. Use a focused factual question when the missing information is a fact rather than a choice; do not invent options for an unknown value. Use the available question tool, or plain chat if the runtime has none.

## Pre-Question Evidence Check

For each consequential decision, distinguish:

| State | Treatment |
|---|---|
| Explicitly supplied or approved | Carry it forward with its exact scope, limits, and exceptions. |
| Verified in existing artifacts | Use the relevant source; check whether it still applies to this target. |
| Routine implementation choice | Use a compatible convention when it does not decide business behavior or expand authority. |
| Proposed default | Label it as a proposal. It is not a confirmed requirement or permission unless already authorized. |
| Material unknown or conflict | Ask the focused question that resolves it; identify conflicting sources when present. |

Inspect tool definitions, command help, templates, and callers before asking the user to supply information those sources already contain. Existing implementation is evidence of current behavior, not automatic proof of intended behavior. Research an external standard when its applicability, current contract, or interpretation affects the decision; do not select a methodology merely to fill a questionnaire field.

## Progressive Discovery

First establish the target harness, surface/version, scope, and artifact kind using [runtime selection](runtime-selection.md). An editor or model name alone does not establish its consuming harness. Carry an explicitly confirmed target forward without asking again.

Progress through the unresolved layers in dependency order. Skip a layer whose decisions are already established, and avoid asking about branches the user has not selected.

| Layer | Establish | Move on when |
|---|---|---|
| Objective and scope | Desired outcome, practical bottleneck, intended users, activation context, exclusions, and applicable constraints | The artifact's purpose and decision boundaries are sufficiently clear to choose a workflow |
| Workflow and contracts | Inputs, current process where relevant, output consumer, success criteria, dependencies, and impact on existing callers | The proposed procedure and preserved contracts are understood |
| Execution details | Available tools, exact commands, required permissions, relevant failure branches, verification, and recovery | The remaining choices can be implemented without inventing a material fact |

When capturing an existing process, ask for a representative start-to-finish example if the process cannot be recovered from evidence. Identify its decisions and verification points before proposing automation. When designing a new process, present viable approaches with trade-offs; do not assume a manual process exists.

After a consequential answer, briefly reflect what changed and identify the next dependent decision. Ask for confirmation only when ambiguity remains or an approval is actually pending. A repeated summary-and-approval ritual is not needed after every answer.

## Question Construction

State the decision and why it matters. For a choice, offer only viable alternatives, normally two or three, and identify the recommended one with its reason. Include material costs or limitations as well as benefits. Permit a free-text correction instead of forcing a false choice.

Example choice, when both workflows are feasible:

> **How should this skill handle unavailable inputs?**
>
> - **Ask interactively (recommended for a chat workflow):** resolves missing facts immediately; requires a user to be present.
> - **Return a structured unresolved-input result:** works in batch execution; the caller must handle the blocked result.

For an unknown fact, ask for the fact or its authoritative source, such as which output schema an existing caller requires. Do not recommend an invented schema as though it were already that caller's contract.

Keep unanswered material questions pending. Silence or elapsed time does not select an option or grant approval. Continue only work independent of that answer, or use an existing authorized default.

## Required Discovery Coverage

For creation or a material workflow change, assess each applicable area below. Establish answers from the request and available evidence first; ask only about unresolved material decisions. Covering an area does not mean asking the user a question about it.

Record the resolved decisions in the task's normal plan or working summary and carry them into the resulting asset. Identify material unknowns and explain any area treated as not applicable. Do not create a separate discovery artifact unless the workflow needs one.

### 1. Objective, Bottleneck, and Domain Constraints

- Establish the practical task, who needs it, the current friction, and the observable outcome that would improve it. Distinguish the agent's responsibility from the artifacts its skills produce.
- Identify applicable domain rules, repository conventions, and external standards from evidence. When applicability or current guidance is uncertain, research the relevant authoritative sources and use them to ground recommendations. Examples include BABOK/IREB for requirements, INVEST/BDD for stories, OpenAPI for API contracts, and OWASP for security; none is a mandatory framework for unrelated tasks.
- Identify scope exclusions and preserved behavior. Do not infer a business policy from the convenience of an implementation.
- Useful unresolved questions: "Which repeated task should this remove?" and "What result would let the intended user consider the task complete?"

### 2. Activation, Preconditions, and Existing Owners

- Identify concrete requests or execution contexts that should activate the asset, plus adjacent requests that should use another workflow. Obtain representative examples when selection is ambiguous.
- Inspect existing agents, skills, and instructions for overlap. Decide whether to extend an existing owner or create a distinct capability; identify any selection or coordination rule actually needed.
- Establish required starting conditions: source files, configured tools, accessible services, runtime dependencies, prior decisions, and authorization. Distinguish a required precondition from a preference or optional enhancement.
- Define what happens when a precondition is unmet: recover within existing authority, request a specific missing input, or return an actionable failure. Do not silently continue with fabricated data.

### 3. Input Contract

Identify each input the workflow consumes, whether supplied by the user, read from a repository, received from a caller, or retrieved from an external source. Resolve:

- **Source and authority:** exact file, directory, tool, service, or upstream artifact; which source prevails if several disagree.
- **Content and structure:** format, schema or required fields, relevant identifiers, version, and representative examples when needed to interpret the input correctly.
- **Required versus optional:** which inputs block the task, which can be absent, and which have an explicitly authorized default.
- **Access and environment:** permissions and dependencies needed to read or retrieve the input; whether it can be verified in the target runtime.
- **Validation and failure:** how to recognize missing, malformed, incompatible, conflicting, or stale input and what the caller needs to correct it.

Inspect actual files and interfaces before asking the user to reconstruct them. If a material contract is unavailable, ask for the contract or its source; do not invent fields from a filename or a familiar domain pattern.

### 4. Output Contract and Intended Consumers

List the concrete deliverables separately from the overall goal. Establish whether each artifact is created, updated, returned in chat, or passed to a tool; its required name and location; its format or schema; required identifiers and metadata; and the rule for preserving existing content. For final agent/skill files, use the [native layout matrix](runtime-selection.md#supported-profiles--native-layout-matrix) to resolve the destination once runtime and scope are known. Ask about location only when the request introduces a material exception or conflict. Establish destinations for the artifacts the generated customization produces separately.

Identify who or what consumes each output and determine the structure from that consumer's needs:

| Consumer | Establish | Evidence of a usable output |
|---|---|---|
| AI agent or delegated task | Context, decisions, source references, unresolved inputs, permissions, and any schema the receiving workflow actually requires | The receiving task can continue without inventing missing decisions or relying on unavailable chat history |
| Code, compiler, script, or CI pipeline | Syntax, types, schema, exact paths, required fields, encoding, and success/failure signals | The relevant parser, build, validator, or consuming command accepts correct content |
| Human engineer or stakeholder | Purpose, required detail, presentation format, terminology, evidence, and decisions or actions the reader needs | The reader can understand and use the deliverable for its stated purpose |
| Multiple consumers | Which portions are parsed and which explain or support review; compatibility with existing callers | Both the machine contract and human review needs are met |

Ask for an accepted example, template, schema, or consuming command when a required output contract remains unclear. Do not impose JSON, YAML, tables, or an executive summary solely because the recipient belongs to a category.

Define content-level acceptance evidence for each important deliverable. File existence or a prescribed heading alone does not establish correctness. Include a relevant rejected or incomplete example when it clarifies the distinction.

### 5. Workflow, Decisions, and Recovery

- Recover the existing start-to-finish process from evidence or a representative example. Identify actions, decision points, intermediate artifacts, dependencies, and checks between steps. If designing a new process, identify and recommend a feasible sequence instead of presenting an invented current process as fact.
- Distinguish deterministic processing, domain judgment, user decisions, and external side effects. This distinction informs the automation decision below.
- Establish the relevant alternate paths: unavailable tools, invalid input, partial completion, conflicting sources, interrupted execution, and failed verification. Select those that can affect this task; avoid an exhaustive hypothetical incident catalog.
- Determine the allowed recovery, what state must be preserved, and what the caller receives when recovery fails. Identify any required authorization before a side effect rather than requesting repeated permission for ordinary in-scope work.
- Define verification checkpoints that demonstrate a step has succeeded before dependent work proceeds.

### 6. Scripting and Automation Design

Actively inspect the proposed or existing workflow for repeatable deterministic work, even when the user does not explicitly mention automation. Candidate operations include multi-file search and lookup, entity extraction, artifact scaffolding or CRUD, index synchronization, schema checks, link validation, and repetitive review checks. Distinguish automating source retrieval from automating the judgment needed to interpret it.

For each material candidate, make a concrete decision:

| Option | Prefer when | Benefit | Cost or limitation |
|---|---|---|---|
| Reuse an existing helper or CLI | Its behavior and contract fit the task | Avoids duplicate logic and maintenance | May need a supported invocation or a scoped improvement |
| Add or extend a helper under `scripts/` | Repetition, fragile mechanics, or reliable validation justify executable code | Repeatable behavior and reusable checks | Implementation, dependencies, testing, and maintenance |
| Keep the step with the model or user | The work needs interpretation, judgment, or a decision, or is too small to justify a helper | Flexibility and less setup | May be less repeatable; requires appropriate evidence and review |

Do not stop at "consider scripts." Identify the operation and suitable existing helper, propose a specific helper responsibility, or explain why scripting is not useful for this workflow. Derive routine implementation details from the repository; ask the user only when the decision affects the intended process, environment, contract, or authority.

When a helper is justified, establish its execution contract before authoring its caller:

- **Responsibility and owner:** which deterministic operation it performs and where the executable definition lives.
- **Inputs and outputs:** accepted arguments, input files or streams, configuration, produced artifacts, and any machine-readable result or error structure required by the caller.
- **Runtime and dependencies:** language/runtime, libraries, services, working-directory assumptions, and supported environment.
- **Invocation and help:** an exact executable command with placeholders or a compact invocation table for a multi-mode CLI. Verify argument names from native help or source; keep full parameter documentation there rather than maintaining a second independent parameter specification.
- **State and failure behavior:** what can be written, how invalid or partial input is reported, exit statuses, and repeat-run or cleanup behavior where relevant.
- **Verification:** representative valid input, meaningful invalid input, and the observable result that would establish the helper meets its contract.

For potentially large or repeated work, also establish expected input size, resource and response-time constraints, normal output volume, required completeness, and how the consumer obtains additional results. Resolve filtering, paging or continuation, explicit limits, truncation reporting, and log/data separation where applicable. Use the [script performance and output checks](review-rubric.md#9-script-performance-and-resource-use) to identify concrete decisions and verification evidence; do not invent numerical targets absent an agreed requirement or measurement.

Use concrete examples such as a single-pass index updater or a schema-validation command when recommending automation. Explain expected reliability or repeatability benefits; time or token savings remain unverified until measured.

### 7. Parallel Execution, Loop Limits, and Read Strategy

- Identify operations that can run independently, such as unrelated source lookups or validation of independent files. Establish ordering for dependent operations and protect shared state when concurrent work can mutate it.
- Define the synchronization point: collect completion status, results, and failures from all operations required by a dependent decision before synthesizing or acting on that decision. Determine whether a failed branch invalidates the result or can be reported as a limitation.
- Where retrying, polling, recursive search, or delegation exists, establish bounded stopping conditions and the outcome when the bound is reached. Preserve applicable existing limits; inspect the shared workflow rather than inventing a conflicting repair policy.
- Identify which reads need full content and which can use search, excerpts, indexes, or cached metadata. Establish when changed state requires refreshing cached evidence. Read optimization must not omit information needed for a correct decision.
- Do not mandate parallel execution or a cache for work that is dependent, trivial, or sensitive to shared-state ordering.

### 8. Verification and Discovery Completion

Before drafting a new workflow or materially changing one, check that the applicable decisions above are resolved well enough to execute: purpose, activation, inputs, outputs and consumers, procedure, automation approach, dependencies, relevant failure paths, and success evidence. A decision can be established from the prompt or source without another confirmation turn.

If a material item remains unresolved, identify the affected operation and ask only the question needed to resolve it. Do not mark a contract complete because a section has a heading, because the user has not objected, or because a familiar template supplies an unsupported default.

In the resulting asset, place the decisions in their actual owners: input/output contracts with the procedure or relevant schema, commands in the calling workflow, executable parameter behavior in its helper, and substantial lookup material in linked references. Do not leave agreed operational decisions only in the conversation.

## Creation: Component-Specific Discovery

Use these extensions after assessing the shared coverage above. They add component-specific decisions; they do not replace the input/output, consumer, automation, and verification discovery requirements.

### Agents

- **Responsibility:** What judgment or coordination should this agent own, and which work belongs in its skills or existing workspace instructions?
- **Role and communication:** Is domain expertise or a particular communication style necessary for the intended user? Establish relevant working principles, such as verification before mutation or traceability to supplied evidence, where they change task decisions. Define the useful behavior rather than requiring a professional title or a persona block.
- **Skill selection:** Which existing skills support its tasks, and what distinguishing conditions select them? Inspect their descriptions before inventing a new skill.
- **Tools and authority:** Which read, write, execute, web-research, or external-service capabilities are needed and available? Inspect actual tool definitions and determine whether the workflow needs external documentation or research. What operations need authorization in the target environment?
- **Coordination, if used:** What causes a handoff, what evidence and decisions must travel with it, and who owns the next step? Do not create a handoff section for an agent that needs none.
- **Execution context:** Will it run interactively, in a delegated task, or in a pipeline? Which unresolved-input and completion signals can that caller handle?

### Skills

- **Procedure:** What task-specific steps or decisions are needed beyond the model's general capability?
- **Commands and dependencies:** Which exact invocations, inputs, runtime versions, and services are required? Obtain argument details from the actual helper or native help; ask only about unresolved choices.
- **Artifacts:** What files, formats, identifiers, and locations does the consumer require? Which examples distinguish a correct result from superficial compliance?
- **Resources:** Which references, templates, or scripts provide concrete value, and when should each be consulted or used? Identify substantial schemas, contracts, and checklists for progressive disclosure; retain the links and context needed to discover and interpret them.
- **Recovery and completion:** Which failures are plausible, what recovery is authorized, and which observable checks establish success?

## Update: Clarify the Delta

Start with the existing asset and the requested change, not a new creation interview. Resolve only missing decisions about:

1. **Driver and expected result:** the observed failure, new capability, or changed constraint and the behavior the update should produce.
2. **Preservation:** exact user limits, supported metadata, names, paths, output contracts, and unrelated behavior that must remain intact.
3. **Impact:** affected callers, sibling assets, command interfaces, or references; whether a change is compatible or requires coordination.
4. **Interpretation:** whether session feedback describes a scoped preference, a contract requirement, or evidence for a broader lesson. Use the distillation reference for the analysis rather than asking the user to invent a universal rule.
5. **Evidence:** the original case to replay and a nearby case that should remain unaffected; any relevant execution constraints.
6. **Automation and execution changes:** repeated model-driven operations that could use an existing or improved helper; changes to its arguments, dependencies, outputs, synchronization, retry bounds, or read strategy. Revisit the affected shared discovery areas rather than accepting a generic claim that the workflow is now automated.

An approved specification or explicit correction can already answer these questions. Do not reopen it merely because work has entered a different mode.

## Review: Establish Scope and Intended Use

Recover the target files, comparison baseline, reported symptoms, and requested deliverable from the prompt first. Ask only if a missing answer materially changes the review:

- Is the target one package, named files, or a wider ecosystem?
- Is there a specific failure to diagnose, or is this a general quality review?
- Which runtime and consumers determine whether the instructions and outputs are valid?
- Which actual input/output examples, scripts, command invocations, and callers can establish contract correctness or reveal an automation opportunity?
- Does the user want findings only, or have they authorized repairs? A review-only request should still receive useful findings without an extra intake interview.
- Are there particular constraints on running tests, accessing sources, or exercising side effects?
- Are specific design alternatives or automation improvements part of the requested review? Recommend them with their trade-offs and evidence; keep optional improvements distinct from required fixes.

Use [review-rubric.md](review-rubric.md) to select evidence and checks. A review need not wait for anecdotal friction when the supplied files already support a concrete finding.

## Automated or Delegated Contexts

Use the supplied decisions and permissions. If a material answer is unavailable and no authorized default exists, report the unresolved input and stop only the dependent work. Non-interactive execution does not authorize inventing a business rule or expanding the task.

Include the missing input, affected operation, and what the caller can supply to resume. Preserve prior approvals and unanswered decisions in any handoff. If the environment lacks a question tool, use its available reporting channel rather than assuming consent.
