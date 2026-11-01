# Agent & Skill Review

Use the checks relevant to the requested change: a narrow wording edit needs focused contract and caller review; a new workflow needs broader end-to-end evidence.

## Universal Principles and Runtime Overlays

Establish the consumer via [runtime selection](runtime-selection.md), then apply its native profile checks alongside the criteria below. Review each requested runtime separately; the builder's host editor or model vendor does not determine the artifact's consumer.

Distinguish shared conventions, verified native requirements, and version/surface-dependent capabilities. Keep unsupported migration requirements visible rather than claiming success after syntax conversion.

Judge revisions by correctness, task completion, and preservation of operational knowledge. Do not delete decision criteria, causal explanations, examples, or recovery guidance to hit an arbitrary line count, but keep Markdown files within single-read tool limits (`< 14 KB`) by splitting mutually exclusive routes, worked examples, and schemas into `references/` or `assets/`, and deleting superseded rules or inline changelogs.

Treat persona style, Markdown layout, script use, description brevity, and parallelism as design choices unless the task or an authoritative contract requires them. Do not claim percentage savings, zero-token execution, or improved model quality without measurements.

## Coverage by Change Type

| Review context | Coverage |
|---|---|
| New asset or redesign | Inspect the end-to-end request, workflow, resources, runtime fit, outputs, and failure paths. |
| Focused update | Establish the current contract before editing; inspect changed decisions and callers afterward, broadening review if regressions appear. |
| Diagnostic review | Trace the reported symptom through instructions, tool calls, and outputs; consider alternative causes before adding another rule. |
| Comparative audit | Use the same task scope and separate source-level differences from measured execution differences, noting strengths and limits on both sides. |

Mark an unexercised capability as *unverified* and an irrelevant dimension as *not applicable*; neither is a demonstrated pass.

## Detailed Review Checks

### 1. Intent, Selection, and Responsibility
- Does the description identify a useful capability and distinguishing activation context? Test nearby requests, not only exact keyword matches.
- Do overlapping agents or skills have a practical selection rule? Overlap alone is not a defect when the caller can reliably choose the owner.
- Are role, responsibility, and domain assumptions clear without relying on an authoritative title?
- Where an agent mounts skills, are links and selection conditions discoverable? Keep selection criteria in frontmatter and execution details in the body or references.
- If coordination exists, are ownership and return conditions clear and free of cyclic delegation? Omit handoff sections when none exist.

### 2. Ownership (DRY / SSOT), Consistency, and Change Impact
- **Single Source of Truth:** Is the authoritative owner of each rule, schema, parameter contract, or procedure identifiable? Do callers reference that owner, and do examples or checks agree with it?
- **Semantic redundancy:** Consolidate differently worded rules pursuing the same goal (e.g., an entrypoint, reference, and template paraphrasing the same workflow steps, validation rule, or output constraint) into the canonical owner.
- **Intra-file & cross-artifact conflicts:** Check for contradictions *within the same file* and *across referenced artifacts* (`SKILL.md`, `references/`, `assets/`, `scripts/` CLI flags/defaults, and sibling/global instructions). Verify paths, field names, exit codes, permissions, and schemas match everywhere.
- Distinguish a subordinate reference, example, or check from a second independent definition that can drift. Check whether prose merely repeats a template rather than explaining a non-obvious decision.
- Preserve required names, metadata, identifiers, and exceptions, and update affected callers when links or CLI contracts change.
- For session-derived changes, use [session-distillation.md](session-distillation.md) to check scope preservation, causal reasoning, and placement rather than treating one example as a universal requirement.
- **Placement (agent vs. skill vs. steering):** Using [instruction placement](runtime-selection.md#instruction-placement-agent-vs-skill-vs-steering), flag standing conventions buried in a skill/agent, always-needed rules that depend on a skill activating, and long procedures bloating steering. Working instructions in a less ideal layer are a 🟢 recommendation; raise to 🟡 only with concrete impact (duplication drift or unactivated skill dependency) and higher only after a demonstrated failure. Propose the move without applying it unless authorized.

### 3. Instruction Clarity, Usefulness, and Progressive Disclosure
- **Ambiguity & decision clarity:** Flag vague or underspecified instructions where two reasonable executions could make opposite choices (unclear pronouns, unstated precedence when sources disagree, undefined thresholds like "large", or ambiguous authority between asking vs. proceeding). Every branch should resolve to a concrete action.
- Does each instruction change a decision, supply context, or establish a real constraint? Remove generic advice, canned dialogue, withdrawn rules, and inline changelogs when they add no operational value.
- Preserve explanations that help choose among valid approaches; do not replace a useful example or failure branch with "handle appropriately."
- **Single-read modularity (`< 14 KB`) & lost-in-the-middle resilience:** Split references by step/topic (`< 14 KB` each) with clear read conditions so only active material loads, and anchor critical constraints and verification near the start or end of the active file rather than burying them behind long examples or templates.
- Retain enough context to use a referenced schema, script, or template correctly; moving text is not an improvement if the caller cannot find or interpret it.
- Tie negative constraints to a plausible failure mode, contract, or authority boundary rather than restating every positive step as a prohibition.

### 4. Execution Flow, Clarification, and Recovery
- Can the main path be followed in order, with dependencies satisfied before dependent actions and observable success/failure criteria?
- Are relevant exceptional conditions handled explicitly?
- Does clarification separate an unknown material fact from a reversible implementation choice? Apply [elicitation-guide.md](elicitation-guide.md) for question mechanics and progressive discovery.
- When a tool, input, or dependency is unavailable, provide an authorized fallback or an actionable unresolved-input result without inventing a substitute tool or weakening a contract.
- Define termination and escalation conditions where retries, recursion, polling, or delegation occur.
- Justify repeated reads or lookups by changed state or needed evidence, and collect independent results before dependent synthesis or mutation.
- Ensure non-interactive callers handle unresolved inputs and failures without waiting indefinitely or treating missing answers as approval.

### 5. Runtime, Tools, and Domain Grounding
- Validate syntax and supported metadata for the intended consumer against the [native layout matrix](runtime-selection.md#supported-profiles--native-layout-matrix) and official docs, separating platform requirements from editorial conventions.
- Preserve existing locations for updates unless a move or rename is authorized, and check affected callers when paths change.
- Verify declared tools, capabilities, and permissions against the environment rather than assuming a tool name guarantees availability.
- Ground executable commands, paths, dependencies, and argument names in the actual helper or native `--help` (handling spaces, missing inputs, and error statuses).
- Make shell assumptions and environment limits explicit; a fallback is useful only when it exists and meets the contract.
- **Domain standards & best practices:** Benchmark domain guidance against recognized industry standards, specifications, established principles, and common failure modes (via targeted web research on domain-specific tasks) rather than unverified assumptions or unrelated methodologies.

### 6. Output Contracts, Verification, and Hallucination Resilience
- **AI consumer:** Provide the context, identifiers, permissions, and structure the receiving task needs.
- **Compiler, script, or pipeline:** Validate syntax, types, schema, paths, and error/completion signals against the consuming interface.
- **Human reader:** Make conclusions, evidence, trade-offs, and next actions easy to find; use stable finding IDs when tracking multiple issues.
- **Mixed consumers:** Keep machine-readable contracts distinguishable from explanatory prose, and verify actual artifacts rather than self-reports.
- **Hallucination resilience:** Keep unknown facts, inferred explanations, proposals, and approved decisions distinguishable. Fix the underlying hallucination mechanism (e.g., an undiscoverable command reference) rather than adding stronger persona language, and disclose remaining placeholders or omitted checks.

### 7. Automation, Coordination, and Evolution
- Prefer helper scripts for repeated transformations, parsing/validation, multi-file aggregation, indexing, or deterministic mechanics. Keep interpretation and domain judgment with the model or user; weigh reliability, setup, and maintenance costs before adding a wrapper.
- Keep concurrent operations independent, with shared state isolated or coordinated and dependent steps waiting for required evidence.
- Transfer only necessary context to delegated tasks (inputs, decisions, permissions, outputs, completion signals, and failure reporting); avoid delegation where ordinary execution suffices.
- Support new providers, versions, or task variants without breaking contracts or copying the workflow, keeping conditional differences discoverable without speculative abstractions.

### 8. Script Performance and Output Bounds
Apply when scripts process substantial data, repeatedly access files/services, or scale output with repository size:
- **Work avoided & filtering:** Reuse retrieved data, batch compatible operations, and apply scope/limits early to avoid unnecessary scans, parsing, or subprocess startup. A limit must not produce false totals or pass off partial validation as complete.
- **Bounded resources & retries:** Process large inputs safely, bound concurrency, and bound external calls/retries with observable failure behavior rather than silent work. Ensure cache keys prevent stale cross-context results.
- **Default output & bounds:** Prefer a summary and selected detail for review while preserving full payloads for downstream parsers. Document record/line/byte bounds and paging in `--help` when output can exceed one response.
- **Truncation transparency:** Report partial coverage, returned count, and continuation instructions—never present a preview as the full result. Keep diagnostic chatter on `stderr` separate from machine-parsed `stdout`, preserving actionable exit codes.
- **Measurement:** Test changed behavior, invalid bounds, and large/empty result sets. Compare the same input/output contract for efficiency claims; label unmeasured benefits as expectations and bottlenecks as evidence.

## Behavioral Evidence

For a substantial skill revision, choose realistic requests that could reveal a regression:
- A typical in-scope request with a concrete expected artifact, plus a nearby out-of-scope request that should route elsewhere.
- A missing material input and a routine mechanical choice, separating necessary clarification from avoidable interruption.
- A previous failure case, if the revision addresses one.

Check artifact content and task completion, not merely filenames, headings, or self-reports. Compare versions using the same inputs, permissions, and baseline, noting assertions that pass or fail in both. Use runtime telemetry for token/time claims and label estimates explicitly. State when structural checks alone were run without live agent execution.

## Findings, Severity, and Report Completeness

| Severity | Meaning | Example |
|---|---|---|
| 🔴 | Defect with credible severe consequences requiring immediate containment | Unauthorized destructive action or unbounded execution cycle with side effects |
| 🟠 | Demonstrated task failure, lost user constraint, authority expansion, or workflow blocker | A required decision is silently invented, or a supported mode cannot complete |
| 🟡 | Material ambiguity, duplication, or dependency risk with concrete impact | Conflicting caller instructions or an unavailable command with no valid recovery |
| 🟢 | Optional clarity or maintainability improvement | Wording can be clearer without changing correct behavior |

Assign severity from consequences, reach, and recoverability; record confidence separately (*verified behavior*, *source-supported risk*, or *hypothesis*). Missing persona blocks or unmeasured token claims do not determine severity; flag oversized files (`> 14 KB`) when they exceed single-read limits or mix unrelated routes/examples.

Scale the report to the assignment:
1. **Assessment and coverage:** Main conclusion, strengths to preserve, files/capabilities inspected, and unverified areas.
2. **Findings:** Use stable IDs when tracking multiple issues, separating platform/contract requirements from optional improvements:

| ID | Severity | File / line | Evidence and impact | Suggested correction |
|---|---|---|---|---|
| F-01 | `<emoji> <severity>` | `<location>` | `<observed defect or explicitly labeled risk>` | `<scoped change>` |

3. **Cross-file ownership & options (when relevant):** Map duplicated concepts to their canonical owner and callers; present optional design/automation improvements with trade-offs and measurement criteria.
4. **Remediation and verification:** State what is authorized, provide concrete diffs when approval is pending, and report checks performed. For review-only requests, return findings without edits.
