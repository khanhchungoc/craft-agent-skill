# Resolving Missing Decisions

Read the request, relevant workspace evidence, and existing decisions first. Do not repeat questions already answered in the prompt or workspace.

This reference owns discovery coverage and questioning direction for defining an executable workflow. Use [SKILL.md](../SKILL.md) for authoring and verification, [runtime selection](runtime-selection.md) for target harness and layout decisions, and [session-distillation.md](session-distillation.md) for interpreting session feedback.

## Questioning Direction

- **Ask vs. proceed:** Ask only when a missing answer changes scope, intended behavior, an input/output contract, authority, or an irreversible action. Use established repository conventions for reversible mechanics (Markdown layout, helper organization) and state the choice when it materially affects review.
- **Inspect evidence before asking:** Check target files, tool definitions, CLI `--help`, templates, and callers before asking the user to supply information already in the workspace. Treat existing code as evidence of current behavior, not automatic proof of intended behavior.
- **Order and batching:** Progress in dependency order (Objective & Scope → Workflow & Contracts → Execution Details). Start with the most consequential blocker, ask **1–3 related questions per turn** (or honour an explicit user limit), and ask about detailed branches only after a branch is selected.
- **Question framing:** State the decision and why it matters. For a choice between viable approaches, offer 2–3 options with a **recommended default** and concise trade-offs, and allow a free-text override. For a missing fact or external contract, ask for the fact or its authoritative source rather than inventing options.
- **Non-interactive or delegated runs:** Do not invent business rules or treat silence as approval. Continue independent work where possible; if a material blocker remains and no authorized default exists, report the missing input, the affected operation, and what the caller must supply to resume.

## Discovery Coverage

For creation or a material workflow change, assess the applicable areas below in dependency order. Establish answers from the request and workspace evidence first; ask only about unresolved material decisions. Record resolved decisions in the working plan and carry them into their canonical owners in the resulting asset.

### Layer 1: Objective, Scope, and Activation

#### 1. Objective, Bottleneck, and Domain Constraints
- **Task and outcome:** The practical task, intended user, current friction, and observable completion outcome. Distinguish the agent's responsibility from the artifacts its skills produce.
- **Domain rules and standards:** Applicable repository conventions and external standards (e.g., BABOK/IREB, INVEST/BDD, OpenAPI, OWASP) grounded in authoritative sources when relevant; never impose an unrelated methodology.
- **Boundaries:** Explicit scope exclusions and preserved behavior.

#### 2. Activation, Preconditions, and Existing Owners
- **Trigger boundary:** Concrete positive requests/contexts that activate the asset versus adjacent requests that belong to another workflow.
- **Ownership check:** Overlap with existing agents, skills, and instructions — whether to extend an existing owner or create a distinct capability, plus any required routing rule.
- **Preconditions and unmet-condition behavior:** Required source files, tools, services, runtime dependencies, and permissions, plus whether an unmet precondition triggers scoped recovery, a targeted question, or an actionable failure.

### Layer 2: Contracts and Workflow

#### 3. Input Contract
For each input consumed (user-supplied, repository file, upstream caller payload, or external service), resolve:
- **Source and authority:** Exact path, tool, service, or artifact, and precedence when sources disagree.
- **Structure and examples:** Format, schema/fields, identifiers, version, and representative examples when needed.
- **Requirement level:** Blocking versus optional inputs, and any explicitly authorized defaults.
- **Access and validation:** Required permissions/dependencies and how missing, malformed, conflicting, or stale input is detected and reported.

#### 4. Output Contract and Intended Consumers
List concrete deliverables separately from the overall goal. Resolve whether each output is created, updated, returned in chat, or passed to a tool; its format/schema, identifiers, and content-preservation rules; and its destination (using the [native layout matrix](runtime-selection.md#supported-profiles--native-layout-matrix) for agent/skill files, and resolving generated artifact paths separately).

Shape each output to its actual consumer:

| Consumer | Establish | Evidence of a usable output |
|---|---|---|
| AI agent or delegated task | Context, decisions, source references, unresolved inputs, permissions, and required handoff schema | Receiving task can continue without inventing decisions or relying on unavailable chat history |
| Code, compiler, script, or CI | Syntax, types, schema, exact paths, required fields, encoding, and exit/error signals | Parser, build, validator, or consuming command accepts the output |
| Human engineer or stakeholder | Purpose, detail level, presentation format, terminology, evidence, and next actions | Reader can understand and act on the deliverable |
| Multiple consumers | Which sections are machine-parsed versus human-reviewed; backward compatibility with callers | Both machine contract and human review needs are met |

Define content-level acceptance evidence (not merely file existence or headings), including a rejected or incomplete example when helpful.

#### 5. Workflow, Decisions, and Recovery
- **Process sequence:** End-to-end steps, decision gates, intermediate artifacts, and verification checkpoints recovered from evidence or a representative example (or recommended with trade-offs when designing a new workflow).
- **Work classification:** Which steps are deterministic mechanics, domain judgment, user decisions, or external side effects.
- **Failure and recovery paths:** Relevant exceptional conditions (unavailable tools, invalid input, partial completion, conflicting sources, failed checks), state preservation, authorized recovery, and failure reporting.

### Layer 3: Execution, Automation, and Verification

#### 6. Scripting and Automation Design
Inspect the workflow for repeatable deterministic work (multi-file lookup, entity extraction, scaffolding/CRUD, index sync, schema/link validation, repetitive checks). Separate deterministic retrieval/validation from model judgment:

| Option | Prefer when | Benefit | Cost or limitation |
|---|---|---|---|
| Reuse an existing helper or CLI | Existing behavior and contract fit the task | Avoids duplicate logic and maintenance | May need a supported invocation or scoped extension |
| Add or extend a helper under `scripts/` | Repetition, fragile mechanics, or reliable validation justify code | Repeatable execution and testable checks | Implementation, dependencies, testing, and maintenance |
| Keep the step with the model or user | Step requires interpretation/judgment or is too small to justify code | Flexibility and zero setup | Less repeatable; relies on prompt adherence and review |

When a helper is justified, define its execution contract before authoring its caller:
- **Responsibility and owner:** Exact deterministic operation and script path.
- **Inputs, outputs, and state:** CLI arguments (verified against `--help` or source), input streams/files, produced artifacts, structured output/error format, exit codes, and idempotency/cleanup behavior.
- **Runtime and verification:** Language/runtime, dependencies, working-directory assumptions, and valid/invalid test inputs.
- **Scale and output bounds:** For large or repeated workloads, resolve expected input volume, filtering/projection, paging or truncation reporting, and log-versus-data separation using [script performance and output checks](review-rubric.md#9-script-performance-and-resource-use).

#### 7. Parallel Execution, Loop Limits, and Read Strategy
- **Concurrency and sync:** Independent operations that can run in parallel, shared-state protection, and the synchronization point where results and failures are collected before dependent decisions.
- **Bounded loops:** Stopping conditions and escalation outcomes for retries, polling, recursive search, or delegation.
- **Read strategy:** Which files require full reads versus targeted search, excerpts, or cached indexes, and when state changes require cache refresh.

#### 8. Discovery Completion & Ownership Placement
Before drafting or materially changing a workflow, verify that purpose, activation, inputs, outputs/consumers, procedure, automation, failure paths, and verification checks are resolved. Place agreed decisions in their canonical owners: contracts with the procedure/schema, invocations in the calling workflow, parameter docs in the script's `--help`, and large lookup material in linked references.

## Component-Specific Discovery

Assess these component-specific decisions alongside the shared coverage above:

### Agents
- **Responsibility boundary:** Judgment and coordination owned by the agent versus procedural work owned by skills or workspace instructions.
- **Working principles:** Domain focus, communication style, or operational guardrails (e.g., verify before mutation, cite evidence) that change task decisions.
- **Skill selection:** Existing skills to mount and the distinguishing conditions that dispatch each one.
- **Tools and authority:** Required read, write, execute, web, or MCP capabilities inspected against actual tool definitions, plus operations requiring user approval.
- **Coordination and context:** Handoff triggers, payload, and next-step owner (only when handoffs are actually used), and whether the agent runs interactively, as a subagent, or in a pipeline.

### Skills
- **Task-specific procedure:** Steps and decision rules needed beyond the model's baseline capability.
- **Progressive disclosure:** Which schemas, checklists, templates, or scripts belong in `references/`, `assets/`, or `scripts/`, and the exact read/use conditions linked from `SKILL.md`.

## Update: Clarify the Delta

Start from the existing asset and requested change rather than running a full creation interview. Resolve only missing decisions across:

1. **Driver and target behavior:** Observed failure, new capability, or changed constraint, and the expected result.
2. **Preservation:** Existing user limits, metadata, names, paths, output contracts, and unrelated behaviors that must remain intact.
3. **Caller impact:** Affected callers, sibling assets, CLI contracts, or references, and whether coordination is required.
4. **Feedback scope:** Whether session feedback reflects a narrow preference, a contract requirement, or a reusable rule (apply [session-distillation.md](session-distillation.md)).
5. **Verification cases:** The original case to replay, a nearby case that must remain unaffected, and any execution constraints.
6. **Automation delta:** Repeated model operations that should move to a helper, or changes to script arguments, bounds, sync points, or read strategy.

## Review: Establish Scope and Intended Use

Recover target files, baseline, symptoms, and deliverable expectations from the prompt first. Ask only if an unresolved answer materially changes the review:

- **Target and mode:** Single file, package, or ecosystem; specific failure diagnosis versus general quality audit; findings-only report versus authorized repairs.
- **Runtime and contracts:** Consuming harness(es), real input/output examples, callers, and scripts that establish contract validity.
- **Verification bounds:** Constraints on running tests, exercising scripts, or triggering side effects, and whether design/automation alternatives are requested.

Apply [review-rubric.md](review-rubric.md) immediately when the supplied files already support concrete findings.
