# Resolving Missing Decisions

Read the request, relevant workspace evidence, and existing decisions first. Do not repeat questions already answered in the prompt or workspace.

## Questioning Direction

- **Ask vs. proceed:** Ask only when a missing answer changes scope, intended behavior, an input/output contract, authority, or an irreversible action. Use established repository conventions for reversible mechanics (Markdown layout, helper organization) and state the choice when it materially affects review.
- **Inspect evidence before asking:** Check target files, tool definitions, CLI `--help`, templates, and callers first. Treat existing code as evidence of current behavior, not automatic proof of intended behavior.
- **Order and batching:** Progress in dependency order (`Objective & Scope` → `Workflow & Contracts` → `Execution Details`). Start with the most consequential blocker, ask **1–3 related questions per turn** (or honor an explicit user limit), and ask about detailed branches only after a branch is selected.
- **Question framing:** State the decision and why it matters. For viable alternatives, offer 2–3 options with a **recommended default**, concise trade-offs, and a free-text override. For a missing fact or external contract, ask for the fact or its authoritative source rather than inventing options.
- **Non-interactive or delegated runs:** Do not invent business rules or treat silence as approval. Continue independent work where possible; if a material blocker remains without an authorized default, report the missing input, affected operation, and what the caller must supply to resume.

## Discovery Coverage

For creation or a material workflow change, resolve applicable areas from workspace evidence first and ask only about unresolved material decisions. Place resolved decisions in their canonical owners (`SKILL.md`, `references/`, `assets/`, or `scripts/`).

### 1. Objective, Scope, and Activation
- **Task and boundaries:** Practical task, observable completion outcome, explicit scope exclusions, preserved behavior, and applicable repository or external standards.
- **Trigger and ownership:** Positive requests/contexts that activate the asset versus adjacent requests belonging elsewhere; whether to extend an existing owner or create a distinct capability.
- **Preconditions:** Required files, tools, services, runtime dependencies, permissions, and unmet-condition behavior (scoped recovery, targeted question, or actionable failure).

### 2. Input & Output Contracts
- **Inputs:** Source path/tool/service, precedence when sources disagree, schema/format, blocking vs. optional inputs, and detection of missing, malformed, or stale data.
- **Outputs and consumers:** Concrete deliverables, destination paths (using the [native layout matrix](runtime-selection.md#supported-profiles--native-layout-matrix) for agent/skill files), preservation rules, and content-level acceptance criteria shaped to the consumer:
  - **AI agent / delegated task:** Context, decisions, source references, permissions, and handoff schema needed to continue without prior chat history.
  - **Code, script, or CI:** Syntax, schema, exact paths, encoding, and exit/error signals.
  - **Human stakeholder:** Conclusions, evidence, trade-offs, and next actions.
  - **Mixed consumers:** Clear separation between machine-parsed sections and human prose.

### 3. Workflow, Automation, and Recovery
- **Process and failure paths:** End-to-end steps, decision gates, verification checkpoints, stopping conditions for loops/retries/delegation, and state preservation on partial failure.
- **Prompt vs. script boundary:** Keep interpretation and domain judgment in the prompt. Reuse or add a helper under `scripts/` only when repetition, fragile deterministic mechanics, or executable validation justify code.
- **Helper contract (when scripting):** Define script path, CLI arguments (verified against `--help`), input/output formats, exit codes, idempotency, and output bounds/filtering for large workloads using [script performance and output bounds](review-rubric.md#8-script-performance-and-output-bounds).

## Component-Specific Decisions

- **Agents:** Responsibility boundary (coordination vs. procedural skills), working guardrails, mounted skills with dispatch conditions, required tool/MCP permissions, and handoff payload (only when handoffs are used).
- **Skills:** Task-specific procedure beyond baseline model capability, and progressive disclosure (what belongs in `references/`, `assets/`, or `scripts/` with explicit read/use conditions in `SKILL.md`).

## Focused Delta Check (Updates & Reviews)

For updates or reviews, do not run a full creation interview. Clarify only unresolved blockers across:
- **Updates:** Driver/symptom, preserved contracts and user limits, caller impact, feedback scope (via [session-distillation.md](session-distillation.md)), and verification replay cases.
- **Reviews:** Target scope (single file vs. package), findings-only vs. authorized repairs, consuming runtime(s), and any restrictions on executing scripts or tests.
