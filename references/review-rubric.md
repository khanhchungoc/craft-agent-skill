# Agent & Skill Review

Use the checks relevant to the requested change. A narrow wording edit needs focused review; a new workflow needs broader evidence. Follow the authoring workflow in [SKILL.md](../SKILL.md).

## Universal Principles and Runtime Overlays

Apply the criteria below across supported runtimes. Establish the actual consumer using [runtime selection](runtime-selection.md), then add its native checks for format, paths, fields, tools, permissions, discovery, and verification. Review each requested runtime separately; the builder's host, editor, or model vendor does not determine the generated artifact's consumer.

Distinguish shared authoring conventions, verified native requirements, and version/surface-dependent capabilities. A Copilot-specific restriction is not universal: Claude Code supports agent skill preload, Codex uses TOML agents, and Kiro has native resource/permission fields. Keep unsupported migration requirements visible rather than claiming success after syntax conversion alone.

## Review Criteria

| Dimension | Evidence to inspect |
|---|---|
| Intent and scope | Instructions support the requested task, preserve permissions, and distinguish unknown facts from routine implementation choices. |
| Discovery and routing | Description distinguishes real positive requests from nearby requests that belong elsewhere; handoffs have clear conditions and do not cycle. |
| Ownership | Definitions have a canonical home; callers link to it. Templates demonstrate structure without repeating shared policy. |
| Instruction quality | Guidance adds non-obvious value, explains important constraints, and loads conditional detail only when needed. |
| Runtime fit | Metadata, tools, commands, paths, and dependencies match the target environment. Current platform claims have authoritative support when uncertain. |
| Output and recovery | Deliverables meet their consumer's contract; meaningful failure branches and stopping conditions cover the actual workflow. |
| Verification | Checks exercise observable results. Reports distinguish syntax lint, human inspection, and executed agent behavior. |
| Maintenance | Feedback retains its original scope and exact limits; scripts are justified by repetition or correctness needs. |

Judge revisions by correctness, task completion, and preservation of useful operational knowledge. File length is not a quality target. Remove duplication and irrelevant material, but retain decision criteria, causal explanations, examples, and recovery guidance when they help execution. Offload detail for discoverability rather than deleting it to meet an arbitrary size goal.

Treat persona style, Markdown layout, script use, description brevity, and parallelism as design choices unless the task or an authoritative contract makes them requirements. Do not claim percentage savings, zero-token execution, or improved model quality without measurements.

## Coverage by Change Type

| Review context | Coverage |
|---|---|
| New asset or substantial redesign | Inspect the end-to-end request, workflow, resources, runtime fit, expected outputs, and relevant failure paths. |
| Focused update | Establish the current contract before editing; inspect the changed decisions and affected callers afterward. Broaden review when evidence exposes a dependency or regression. |
| Diagnostic review | Trace the reported symptom through the relevant instructions, tool calls, and outputs. Consider alternative causes before proposing another prompt rule. |
| Comparative audit | Use the same task scope and distinguish source-level differences from measured differences in execution. Identify capabilities and limitations on both sides. |

Select relevant checks from the dimensions below. Mark an unexercised capability as unverified; mark a genuinely irrelevant dimension as not applicable. Neither is a demonstrated pass.

## Detailed Review Checks

### 1. Intent, Selection, and Responsibility

- Does the description identify a useful capability and distinguishing activation context? Test nearby requests, not only phrases that repeat its exact keywords.
- Do overlapping agents or skills have a practical selection rule? Overlap alone is not a defect when the caller can reliably choose the appropriate owner.
- Are role, responsibility, and relevant domain assumptions clear without relying on an authoritative-sounding title?
- Where an agent mounts skills, are links and selection conditions discoverable? Keep skill selection criteria in frontmatter and execution details in the body or references.
- If coordination exists, are ownership and return conditions clear and free of cyclic delegation? An asset with no handoffs does not need a handoff section.

### 2. DRY, SSOT, Consistency, and Change Impact

- **DRY (Don't Repeat Yourself):** does repeated procedural logic, validation, or instruction text have one maintained implementation or definition? Reuse the existing helper, template, or rule when it fits; avoid multiple versions that must be updated independently.
- **SSOT (Single Source of Truth):** is the authoritative owner of a rule, schema, parameter contract, or decision identifiable? Do callers reference that owner, and do generated examples or enforcement checks agree with it? DRY and SSOT do not forbid useful examples, summaries, or tests; those must remain subordinate to the authoritative definition.
- Identify the canonical source for each changed rule and inspect affected consumers. Compare sibling instructions and global guidance for conflicting limits, paths, permissions, or output contracts.
- Distinguish a useful reference, example, or enforcement check from a second independent definition that can drift. Check whether narrative prose repeats a template rather than explaining a non-obvious decision.
- Does an update preserve required names, metadata, identifiers, and exceptions? Are changed links or CLI contracts reflected in their actual callers?
- For session-derived changes, use [session-distillation.md](session-distillation.md) to check scope preservation, causal reasoning, and placement rather than treating one example as a universal requirement.

### 3. Instruction Usefulness and Progressive Disclosure

- Does each instruction change a decision, supply needed context, or establish a real constraint? Remove generic advice and canned dialogue only when they add no operational value.
- Preserve explanations that help the model choose among valid approaches. Do not replace a useful example or failure branch with an unsupported instruction to "handle appropriately."
- Are mode-specific references linked with clear read conditions? Could a future agent discover the details without loading unrelated material or following a chain with no clear destination?
- Does the skill retain enough context to use a referenced schema, script, or template correctly? Moving text into another file is not an improvement if the caller cannot find or interpret it.
- Are negative constraints tied to a plausible failure mode, contract, or authority boundary? Avoid restating every positive step as a prohibition, but retain a constraint when its risk warrants explicit emphasis.

### 4. Execution Flow, Clarification, and Recovery

- Can the main path be followed in a meaningful order? Are dependencies satisfied before actions that rely on them, and can the caller recognize success or failure?
- Are relevant exceptional conditions handled explicitly? Plain prose or conditional steps are both acceptable when the resulting decision is clear.
- Does clarification distinguish an unknown material fact from a reversible implementation choice? Apply [elicitation-guide.md](elicitation-guide.md) for question mechanics and progressive discovery.
- When a tool, required input, or dependency is unavailable, is there an authorized fallback or an actionable unresolved-input result? A fallback must preserve the required result; do not invent a substitute tool or weaken a contract silently.
- Where retries, recursion, polling, or delegation occur, are their termination and escalation conditions defined? Use the shared workflow's repair policy for this skill; choose task-specific limits for other workflows when necessary.
- Are repeated reads or lookups justified by changed state or needed evidence? Are results from independent operations collected before dependent synthesis or mutation?
- Can a non-interactive caller handle unresolved inputs and failures without waiting indefinitely or interpreting missing answers as approval?

### 5. Runtime, Tools, and Domain Grounding

- Validate syntax and supported metadata for the intended consumer. Separate platform requirements from editorial conventions; use authoritative current documentation when a platform claim is uncertain.
- Check new customization destinations and package ownership against the [artifact layout](../SKILL.md#final-artifact-layout). Preserve existing locations for updates unless a move or rename is authorized, and check affected callers when paths change.
- Verify declared tools against the actual environment. Review capabilities and permissions rather than assuming a tool name guarantees availability or authority.
- Are executable commands, paths, runtime dependencies, and argument names grounded in the actual helper or native help? Do documented invocations work with spaces, missing inputs, and expected error statuses where relevant?
- If scripts are introduced, do they provide useful native help, validate inputs, report errors clearly, and avoid unintended side effects? Check newly changed behavior, not only the happy path.
- Are shell assumptions and environment limitations explicit? A generic fallback is useful only when it exists and meets the required contract.
- Is domain guidance applicable to this workflow and supported by the right source? Avoid importing a methodology, standard, or provider-specific behavior into unrelated tasks.

### 6. Output Contracts and Verification

- For an AI consumer, provide the context, identifiers, and structure the receiving task actually needs; do not assume every AI-facing artifact requires JSON or a rigid table.
- For a compiler, script, or pipeline, validate syntax, types, schema, paths, and error/completion signals against the consuming interface.
- For a human reader, make conclusions, evidence, trade-offs, and next actions easy to find. Use stable finding IDs when several issues need discussion or selective remediation.
- For mixed consumers, keep machine-readable contracts distinguishable from explanatory prose. Verify actual artifacts rather than accepting a transcript's claim that they were produced correctly.
- Do checks distinguish correct content from a file with the right name or an output with the right headings? Are important outcomes left unchecked?
- Can the reported verification support the claim being made? Lint, a script regression suite, manual inspection, and a runtime agent evaluation establish different things.

### 7. Usability and Hallucination Resilience

- Does the workflow make necessary decisions clear without imposing repeated approvals or low-value questions? Does it carry forward confirmed answers accurately?
- Are unknown facts, inferred explanations, proposals, and approved decisions distinguishable? Check for invented source citations, schemas, paths, arguments, or success claims.
- Does the guidance address the observed hallucination mechanism, such as an undiscoverable command reference, instead of merely adding stronger persona language?
- Are remaining placeholders, incomplete artifacts, or omitted checks disclosed and consistent with the requested deliverable?

### 8. Automation, Coordination, and Evolution

- Is repeated or fragile deterministic work better implemented in an existing helper? Compare reliability, setup, maintenance, and invocation costs before adding a script.
- Prefer scripts for repeated transformations, reliable parsing or validation, multi-file aggregation, indexing, or other deterministic mechanics that benefit from executable checks. Keep interpretation and unresolved domain decisions with the model or user. A one-off command may be sufficient; a new wrapper is not automatically an improvement.
- Are concurrent operations independent, and is their shared state isolated or coordinated? Do dependent steps wait for the evidence they require?
- For delegated tasks, is the minimum necessary context transferred, including inputs, decisions, permissions, outputs, and completion signals? Check how failures return to the caller. Do not require delegation where ordinary execution suffices.
- Can a new provider, version, or task variant be added without breaking established contracts or copying the entire workflow? Keep conditional differences discoverable without designing speculative abstractions.
- Identify useful improvements beyond the reported symptom when evidence supports them. Present optional improvements with benefits and costs, and keep them distinct from defects and authorized repairs.

### 9. Script Performance and Resource Use

Apply these checks when scripts process substantial data, repeatedly access files or services, or are introduced to improve efficiency. Scale verification to the operation's expected workload.

- **Work avoided:** does the script reuse retrieved data, batch compatible operations, and avoid repeated directory scans, parsing, or subprocess startup where that repetition is a material cost? Consider the whole calling workflow, not only the helper's inner loop.
- **Selection before expansion:** are file scope, filters, projections, and result limits applied early enough to avoid unnecessary reads, transfers, or parsing when the required result permits it? A result limit must not produce incorrect totals or incomplete validation passed off as complete.
- **Memory and data volume:** can large inputs be streamed or processed in bounded chunks where necessary? Check whether sorting, buffering, or aggregating the entire input is justified by the contract and expected size.
- **Concurrency:** is parallelism bounded and useful for this workload? Account for ordering, shared state, connection/rate limits, process startup, and synchronization overhead; more workers are not inherently faster.
- **Timeouts and retry cost:** are external calls, polling, and expensive retries bounded, with observable failure and cancellation behavior where needed? Repeated failure must not become silent background work.
- **Caches and freshness:** if caching is justified, are its key, scope, reuse conditions, and invalidation sufficient to avoid stale or cross-context results? Do not add a cache when its maintenance costs exceed its value.
- **Measurement:** for an efficiency claim, compare the same representative input, environment, output contract, and correctness checks. Record relevant wall-clock time, input size, peak memory or request count when material, and output volume. Distinguish startup versus steady-state costs and cold versus warm caches when they affect the result.
- **Conclusion:** label unmeasured benefits as expectations and observed bottlenecks as evidence. A shorter transcript, fewer script lines, or a smaller response alone does not prove faster execution or lower total cost.

### 10. Script Output Volume, Paging, and Limits

Apply these checks to scripts whose output can grow with repository size, record count, matches, errors, or remote results. The output contract should let the consumer obtain sufficient evidence without accidentally flooding its context or silently losing results.

- **Default output:** is the normal response appropriate for its consumer? Prefer a useful summary and selected detail for exploratory or human review. Preserve the complete payload when a downstream parser explicitly requires it; use an appropriate artifact or stream for large data.
- **Explicit bounds:** where output can be large, are relevant record, line, byte, or excerpt limits available and documented through native help? Choose defaults from expected use rather than imposing a universal character cap. Distinguish output limits from limits on the work performed.
- **Filtering and projection:** can the caller select the relevant scope, fields, matches, or severity before requesting full detail? Does a summary include the counts or status needed to decide whether deeper inspection is required?
- **Paging or continuation:** when all results cannot fit in one response, is there a supported page, offset, cursor, chunk, or full-artifact mechanism? Verify how the caller requests the next portion and recognizes completion. A script with inherently bounded output need not invent paging.
- **Ordering and consistency:** for paged results, is ordering stable enough to avoid duplicate or missing entries under the supported data-change assumptions? Define or report what happens when the underlying input changes between requests.
- **Truncation transparency:** if detail is omitted, does the response explicitly report partial coverage, returned count, and whether more results exist? Include total counts only when known. Provide a continuation instruction or artifact location when available; never present a preview as the full result.
- **Logs versus data:** can a machine consumer parse the selected format without progress messages or diagnostic chatter mixed into it? Keep logs on an appropriate separate channel, and preserve actionable failures and meaningful exit statuses even in terse or limited-output modes.
- **Parameter semantics:** are bounds validated and their interactions clear, including defaults, invalid values, end-of-results behavior, and any supported request for full output? Full-output mode must be deliberate and preserve established caller contracts.
- **Verification:** exercise a result larger than one response, the final or empty page, and invalid bounds where those modes exist. Check that every expected record remains retrievable and that limits do not hide a failing validation or change a failure into success.

Use the actual script's parameter names and response fields when reviewing an implementation. The concepts above are checks, not a new shared CLI schema that every helper must adopt.

## Behavioral Evidence

For a substantial skill revision, choose realistic requests that could reveal a regression:

- A typical in-scope request with a concrete expected artifact.
- A nearby out-of-scope request that should use another workflow.
- A missing material input and a routine mechanical choice, to distinguish necessary clarification from avoidable interruption.
- A previous failure, if the revision addresses one.

Add relevant permission boundaries, unavailable dependencies, changed contracts, or non-interactive execution to the cases when those behaviors are part of the asset. Subjective quality may need human review; do not force a numerical assertion onto a judgment it cannot represent.

Check artifact content and task completion, not merely filenames, required headings, or the agent's self-report. When comparing versions, use the same inputs and permissions, preserve the baseline, and retain the outputs and observable checks. Independent or blind evaluation can help when available and authorized; it is not required for every edit.

Use actual runtime telemetry for token/time claims. Label estimates and proxies. When no agent execution was performed, say so; structural checks alone do not prove better runtime behavior.

Inspect the assertions themselves: a condition that passes for clearly incorrect outputs provides weak evidence. In a comparison, note assertions that pass or fail in both versions, inconsistent outcomes, and differences in execution cost. Repeat runs when variability could change the conclusion; do not imply statistical confidence from a single small sample.

## Findings & Severity

| Severity | Meaning | Example |
|---|---|---|
| Critical | A defect with credible severe consequences requiring immediate containment | Unauthorized destructive action or a demonstrated unbounded execution cycle with consequential side effects |
| High | Demonstrated task failure, lost user constraint, material authority expansion, or a likely workflow blocker | A required decision is silently invented, or a supported execution mode cannot complete |
| Medium | Material ambiguity, duplication, or dependency risk with a concrete impact | Conflicting caller instructions or an unavailable command with no valid recovery path |
| Low | Optional clarity or maintainability improvement | Wording can be clearer without changing correct behavior |

Assign severity from consequences, reach, and recoverability. Record confidence separately: verified behavior, source-supported risk, or hypothesis. A large file, missing persona block, or fixed number of supposedly wasted tokens does not determine severity.

Return a short assessment and, when multiple findings need tracking, a table:

| ID | Severity | File / line | Evidence and impact | Suggested correction |
|---|---|---|---|---|
| F-01 | <severity> | <location> | <observed defect or explicitly labeled risk> | <scoped change> |

Separate verified defects from hypotheses. Use an unmeasured health label only if useful; do not invent numeric quality scores. Include verification performed and relevant limits. Provide diffs when requested or needed for an approval still pending under the shared workflow.

## Report Completeness

Scale the report to the assignment, retaining information needed to act on its conclusions:

1. **Assessment and coverage:** the main conclusion, useful strengths worth preserving, files or capabilities inspected, and material areas not verified.
2. **Findings:** stable IDs where helpful, severity, confidence, exact location, supporting evidence, expected versus observed behavior, and a scoped correction. Distinguish requirements from reviewer preference.
3. **Cross-file ownership, when relevant:** map a duplicated concept to its canonical owner and affected callers. Do not propose a new copy in each consumer.
4. **Improvement options, when relevant:** identify the actual operation, proposed mechanism, benefits, trade-offs, dependencies, and how improvement could be measured. Avoid unsupported speed or token-saving estimates.
5. **Remediation and verification:** state what is authorized, provide a concrete diff when approval is pending, and report checks actually performed. Recheck affected contracts and relevant findings after repairs; report unresolved failures explicitly.

For a single clear issue, concise prose can carry this information. A broad audit may need separate tables and examples. Completeness and reviewability take priority over a prescribed section count or report length.
