---
name: craft-agent-skill
description: "Create, update, or audit agents and skills for Copilot, Claude Code, Codex, Gemini, and Kiro, using shared principles and runtime-specific templates."
---

# Craft Agent & Skill

Produce useful agent customizations whose instructions, dependencies, and outputs fit the requested task and target runtime. Act as a practical agent customization architect: coordinate scoped changes, preserve operational boundaries, and explain findings with evidence.

## Ownership & Resources

Do not copy host-specific instructions into artifacts for another runtime. The skill owns the authoring workflow; supporting files have these distinct roles:

| Resource | Owns | Read when |
|---|---|---|
| [Runtime selection and profiles](references/runtime-selection.md) | Target harness, surface, scope, native layout matrix, steering/instruction placement, templates, and runtime checks | Before choosing a format or destination |
| [Elicitation guide](references/elicitation-guide.md) | Discovery coverage and resolving missing decisions | Creating or materially changing a workflow; unresolved material decisions |
| [Session distillation](references/session-distillation.md) | Translating feedback without changing its scope | Improving instructions from a conversation or failure |
| [Review rubric](references/review-rubric.md) | Universal quality criteria and finding format | Reviewing an asset together with its selected runtime profile |
| [Runtime agent templates](assets/runtimes/) | Native agent templates (Copilot, Claude, Codex, Kiro) | Composing a platform-specific agent |
| [Universal skill template](assets/skill.template.md) | Universal workflow structure | Composing any new skill package |
| [Validator](scripts/validate_agent_skill.py) | Executable structural checks and CLI help | Verifying files; change it when changing a lint rule |

## Shared Workflow

1. **Establish the request and runtime.** Read the prompt, relevant files, and existing approvals. Follow [runtime selection](references/runtime-selection.md) to establish target harness, scope, native layout, and artifact kind; ask when a material target decision is missing. Select a mode below. Use the elicitation guide for creation or material workflow changes and unresolved decisions, screening evidence before asking.
2. **Check ownership and overlap.** Inspect nearby agents, skills, and instruction files. Identify the canonical owner of each changed concept before editing. Extend an existing owner when it already covers the task; use references for dependent components. When creating or reviewing an agent/skill, also decide per instruction whether it belongs in the agent, the skill, or steering (Kiro steering, Copilot `.github/instructions`, `CLAUDE.md`/`.claude/rules`, `AGENTS.md`, `GEMINI.md`) using [instruction placement](references/runtime-selection.md#instruction-placement-agent-vs-skill-vs-steering).
3. **Make the scoped change.** Follow the selected mode. Add guidance that changes decisions or supplies needed context. Research external standards when their applicability or current behavior matters. Add scripts for demonstrated repetition or fragile deterministic work; parallelize independent operations when useful and collect their results before making dependent decisions.
4. **Verify the result.** Apply the universal rubric plus each selected runtime profile's native checks. Run `scripts/validate_agent_skill.py` for structural linting. Test changed scripts against meaningful failures. For substantial workflows, exercise realistic requests and compare old/new outputs when warranted and supported. Report structural lint, native discovery, and observed task behavior separately for each target.
5. **Deliver evidence.** Return changed paths, resulting behavior, verification evidence, checks actually run, and unresolved limits. Fix newly introduced failures within scope. After two unsuccessful repair attempts on the same failure, report the evidence and remaining blocker instead of repeating the same action. For review-only requests, return findings without applying repairs.

## Mode 1: Creation

- Define the intended request, activation boundary, inputs, output, and success criteria from the available evidence.
- Compose the common body scaffold with the selected native wrapper from [assets/runtimes/](assets/runtimes/). Replace placeholders and remove unused sections and authoring notes.
- For agents, define responsibility and tool access; link procedural skills with dispatch conditions. Restrict tools to the workflow's needs.
- For skills, put selection criteria in the frontmatter description. Keep the body focused on execution. Create references, scripts, or assets only when they serve a concrete use.
- Include a useful happy path, required preconditions, verification, and only the failure branches the task needs.

## Mode 2: Update / Distillation

- Preserve the asset's name, location, supported metadata, existing authorization boundaries, and unrelated behavior unless the request changes them.
- Apply focused edits for explicit requirements. Use [session distillation](references/session-distillation.md) when feedback needs interpretation.
- Check dependent links and callers when changing paths, commands, or output contracts. Update affected callers without duplicating the definition.
- If processing a replacement or improvement audit, preserve retained instructions, target paths, and approved decisions. Prepare concrete diffs for unapproved changes.

## Mode 3: Review

- Read the requested assets and their relevant resources. Assess them using the [review rubric](references/review-rubric.md).
- Distinguish reproducible defects, evidence-based risks, and optional improvements. A stylistic preference is not a platform requirement.
- Return a proportionate findings report. Apply repairs only when the user's request includes them; a comparison or audit alone does not authorize edits.
