# Agent & Skill Review

Use the checks relevant to the requested change: a narrow wording edit needs focused contract and caller review; a new workflow needs broader end-to-end evidence.

## Universal Principles and Runtime Overlays

Establish the actual consumer using [runtime selection](runtime-selection.md), then apply its native profile checks alongside the universal criteria below. Review each requested runtime separately; the builder's host editor or model vendor does not determine the generated artifact's consumer.

Distinguish shared authoring conventions, verified native requirements, and version/surface-dependent capabilities. Keep unsupported migration requirements visible rather than claiming success after syntax conversion alone.

Judge revisions by correctness, task completion, and preservation of useful operational knowledge. **File length is not a quality target.** Remove duplication and irrelevant material, but retain decision criteria, causal explanations, examples, and recovery guidance when they help execution. Offload detail for discoverability rather than deleting it to meet an arbitrary size goal.

Treat persona style, Markdown layout, script use, description brevity, and parallelism as design choices unless the task or an authoritative contract makes them requirements. Do not claim percentage savings, zero-token execution, or improved model quality without measurements.

## Coverage by Change Type

| Review context | Coverage |
|---|---|
| New asset or substantial redesign | Inspect the end-to-end request, workflow, resources, runtime fit, expected outputs, and relevant failure paths. |
| Focused update | Establish the current contract before editing; inspect the changed decisions and affected callers afterward. Broaden review when evidence exposes a dependency or regression. |
| Diagnostic review | Trace the reported symptom through the relevant instructions, tool calls, and outputs. Consider alternative causes before proposing another prompt rule. |
| Comparative audit | Use the same task scope and distinguish source-level differences from measured differences in execution. Identify capabilities and limitations on both sides. |

Mark an unexercised capability as *unverified*; mark a genuinely irrelevant dimension as *not applicable*. Neither is a demonstrated pass.

## Detailed Review Checks

### 1. Intent, Selection, and Responsibility
- Does the description identify a useful capability and distinguishing activation context? Test nearby requests, not only phrases that repeat its exact keywords.
- Do overlapping agents or skills have a practical selection rule? Overlap alone is not a defect when the caller can reliably choose the appropriate owner.
- Are role, responsibility, and relevant domain assumptions clear without relying on an authoritative-sounding title?
- Where an agent mounts skills, are links and selection conditions discoverable? Keep skill selection criteria in frontmatter and execution details in the body or references.
- If coordination exists, are ownership and return conditions clear and free of cyclic delegation? An asset with no handoffs does not need a handoff section.

### 2. Ownership (DRY / SSOT), Consistency, and Change Impact
- **Single Source of Truth:** Is the authoritative owner of each rule, schema, parameter contract, or procedure identifiable? Do callers reference that owner, and do generated examples or enforcement checks agree with it?
- **Semantic redundancy & overlapping logic:** Look beyond verbatim copy-paste for rules worded differently that pursue the same goal (e.g., an entrypoint, a reference, and a template each paraphrasing the same workflow steps, validation rule, or output constraint). Consolidate paraphrased duplicates into the canonical owner so rules cannot drift.
- **Intra-file & cross-artifact conflicts:** Check for contradictory instructions *within the same file* (e.g., conflicting step ordering, question limits, or fallback rules) AND *across all referenced artifacts* (`SKILL.md`, `references/`, `assets/` templates, `scripts/` CLI flags/defaults, and sibling/global instructions). Verify that paths, field names, exit codes, permissions, and output schemas match everywhere they appear.
- Distinguish a subordinate reference, example, or enforcement check from a second independent definition that can drift. Check whether narrative prose merely repeats a template rather than explaining a non-obvious decision.
- Does an update preserve required names, metadata, identifiers, and exceptions? Are changed links or CLI contracts reflected in their actual callers?
- For session-derived changes, use [session-distillation.md](session-distillation.md) to check scope preservation, causal reasoning, and placement rather than treating one example as a universal requirement.

- **Placement (agent vs. skill vs. steering):** Using [instruction placement](runtime-selection.md#instruction-placement-agent-vs-skill-vs-steering), does each instruction live in the right layer? Flag standing conventions buried in a skill/agent (they may not load, or are duplicated across assets), always-needed rules that depend on a skill activating, and long procedures bloating steering. An instruction that is present and works but sits in a less ideal layer is a 🟢 recommendation, not a defect. Raise to 🟡 only with concrete impact (e.g., the rule is duplicated and has drifted, or it depends on a skill that may not activate); raise higher only after a demonstrated failure. Propose the move without applying it unless authorized.

### 3. Instruction Clarity, Usefulness, and Progressive Disclosure
- **Ambiguity & decision clarity:** Flag vague or underspecified instructions where two reasonable executions could make opposite choices (e.g., unclear pronouns, unstated precedence when sources disagree, undefined thresholds like "large" or "substantial", or ambiguous authority boundaries between asking vs. proceeding). Every branch or condition should resolve to a concrete action.
- Does each instruction change a decision, supply needed context, or establish a real constraint? Remove generic advice and canned dialogue only when they add no operational value.
- Preserve explanations that help the model choose among valid approaches. Do not replace a useful example or failure branch with an unsupported instruction to "handle appropriately."
- Are mode-specific references linked with clear read conditions? Can an agent discover the details without loading unrelated material or following a chain with no clear destination?
- Does the skill retain enough context to use a referenced schema, script, or template correctly? Moving text into another file is not an improvement if the caller cannot find or interpret it.
- Are negative constraints tied to a plausible failure mode, contract, or authority boundary? Avoid restating every positive step as a prohibition, but retain a constraint when its risk warrants explicit emphasis.

### 4. Execution Flow, Clarification, and Recovery
- Can the main path be followed in a meaningful order? Are dependencies satisfied before actions that rely on them, and can the caller recognize success or failure?
- Are relevant exceptional conditions handled explicitly?
- Does clarification distinguish an unknown material fact from a reversible implementation choice? Apply [elicitation-guide.md](elicitation-guide.md) for question mechanics and progressive discovery.
- When a tool, required input, or dependency is unavailable, is there an authorized fallback or an actionable unresolved-input result? A fallback must preserve the required result; do not invent a substitute tool or weaken a contract silently.
- Where retries, recursion, polling, or delegation occur, are their termination and escalation conditions defined?
- Are repeated reads or lookups justified by changed state or needed evidence? Are results from independent operations collected before dependent synthesis or mutation?
- Can a non-interactive caller handle unresolved inputs and failures without waiting indefinitely or interpreting missing answers as approval?

### 5. Runtime, Tools, and Domain Grounding
- Validate syntax and supported metadata for the intended consumer against the [native layout matrix](runtime-selection.md#supported-profiles--native-layout-matrix) and current official docs. Separate platform requirements from editorial conventions.
- Preserve existing locations for updates unless a move or rename is authorized, and check affected callers when paths change.
- Verify declared tools against the actual environment. Review capabilities and permissions rather than assuming a tool name guarantees availability or authority.
- Are executable commands, paths, runtime dependencies, and argument names grounded in the actual helper or native `--help`? Do documented invocations work with spaces, missing inputs, and expected error statuses where relevant?
- Are shell assumptions and environment limitations explicit? A fallback is useful only when it exists and meets the required contract.
- Is domain guidance applicable to this workflow and supported by an authoritative source? Avoid importing a methodology, standard, or provider-specific behavior into unrelated tasks.

### 6. Output Contracts, Verification, and Hallucination Resilience
- **AI consumer:** Provide the context, identifiers, permissions, and structure the receiving task actually needs.
- **Compiler, script, or pipeline:** Validate syntax, types, schema, paths, and error/completion signals against the consuming interface.
- **Human reader:** Make conclusions, evidence, trade-offs, and next actions easy to find. Use stable finding IDs when several issues need discussion or selective remediation.
- **Mixed consumers:** Keep machine-readable contracts distinguishable from explanatory prose. Verify actual artifacts rather than accepting a transcript's self-report.
- **Hallucination resilience:** Are unknown facts, inferred explanations, proposals, and approved decisions distinguishable? Address the underlying hallucination mechanism (e.g., an undiscoverable command reference) rather than merely adding stronger persona language. Disclose any remaining placeholders or omitted checks.

### 7. Automation, Coordination, and Evolution
- Prefer helper scripts for repeated transformations, reliable parsing or validation, multi-file aggregation, indexing, or deterministic mechanics that benefit from executable checks. Keep interpretation and domain judgment with the model or user. Compare reliability, setup, and maintenance costs before adding a new script wrapper.
- Are concurrent operations independent, and is their shared state isolated or coordinated? Do dependent steps wait for the evidence they require?
- For delegated tasks, is the minimum necessary context transferred (inputs, decisions, permissions, outputs, completion signals, and failure reporting)? Do not require delegation where ordinary execution suffices.
- Can a new provider, version, or task variant be added without breaking established contracts or copying the entire workflow? Keep conditional differences discoverable without designing speculative abstractions.

### 8. Script Performance and Output Bounds
Apply these checks when scripts process substantial data, repeatedly access files/services, or produce output that scales with repository size:
- **Work avoided & early filtering:** Does the script reuse retrieved data, batch compatible operations, and apply file scope/filters/limits early enough to avoid unnecessary scans, parsing, or subprocess startup? A result limit must not produce incorrect totals or pass off partial validation as complete.
- **Bounded resources & retries:** Are large inputs processed safely, concurrency bounded where used, and external calls/retries bounded with observable failure behavior rather than silent background work? If caching is justified, ensure its key and invalidation prevent stale cross-context results.
- **Default output & explicit bounds:** Prefer a useful summary and selected detail for human/exploratory review while preserving full payloads when a downstream parser requires them. Document record/line/byte bounds and continuation/paging mechanisms in `--help` when output can exceed one response.
- **Truncation transparency & channel separation:** Explicitly report partial coverage, returned count, and continuation instructions—never present a preview as the full result. Keep progress/diagnostic chatter on `stderr` separate from machine-parsed `stdout` data, and preserve actionable errors and exit codes even in terse modes.
- **Measurement & verification:** Test newly changed behavior, invalid bounds, and large/empty result sets. For efficiency claims, compare the same representative input and output contract; label unmeasured benefits as expectations and observed bottlenecks as evidence.

## Behavioral Evidence

For a substantial skill revision, choose realistic requests that could reveal a regression:
- A typical in-scope request with a concrete expected artifact.
- A nearby out-of-scope request that should use another workflow.
- A missing material input and a routine mechanical choice, to distinguish necessary clarification from avoidable interruption.
- A previous failure, if the revision addresses one.

Check artifact content and task completion, not merely filenames, required headings, or the agent's self-report. When comparing versions, use the same inputs and permissions, preserve the baseline, and note assertions that pass or fail in both versions. Use actual runtime telemetry for token/time claims and label estimates explicitly. When no agent execution was performed, state that structural checks alone do not prove runtime behavior.

## Findings, Severity, and Report Completeness

| Severity | Meaning | Example |
|---|---|---|
| 🔴 | A defect with credible severe consequences requiring immediate containment | Unauthorized destructive action or a demonstrated unbounded execution cycle with consequential side effects |
| 🟠 | Demonstrated task failure, lost user constraint, material authority expansion, or a likely workflow blocker | A required decision is silently invented, or a supported execution mode cannot complete |
| 🟡 | Material ambiguity, duplication, or dependency risk with a concrete impact | Conflicting caller instructions or an unavailable command with no valid recovery path |
| 🟢 | Optional clarity or maintainability improvement | Wording can be clearer without changing correct behavior |

Assign severity from consequences, reach, and recoverability. Record confidence separately (*verified behavior*, *source-supported risk*, or *hypothesis*). A large file, missing persona block, or fixed number of supposedly wasted tokens does not determine severity.

Scale the report to the assignment:
1. **Assessment and coverage:** Main conclusion, useful strengths worth preserving, files or capabilities inspected, and material areas not verified.
2. **Findings:** Use stable IDs when multiple issues need tracking, distinguishing platform/contract requirements from reviewer preference or optional improvements:

| ID | Severity | File / line | Evidence and impact | Suggested correction |
|---|---|---|---|---|
| F-01 | `<emoji> <severity>` | `<location>` | `<observed defect or explicitly labeled risk>` | `<scoped change>` |

3. **Cross-file ownership & improvement options (when relevant):** Map duplicated concepts to their canonical owner and affected callers. Present optional design/automation improvements with benefits, trade-offs, and how they could be measured.
4. **Remediation and verification:** State what is authorized, provide concrete diffs when approval is pending, and report checks actually performed. For review-only requests, return findings without applying edits.
