---
name: craft-agent-skill
description: "Create, update, or audit agents and skills for Claude Code, Codex, GitHub Copilot, and Kiro, using shared principles and runtime-specific templates."
---

# Craft Agent & Skill

Produce useful agent customizations whose instructions, dependencies, and outputs fit the requested task and target runtime. Act as a practical agent customization architect: coordinate scoped changes, preserve operational boundaries, and explain findings with evidence.

## Ownership & Resources

Follow the repository [README.md](README.md) while editing this repository. Do not copy host-specific instructions into artifacts for another runtime. The skill owns the authoring workflow; supporting files have these distinct roles:

| Resource | Owns | Read when |
|---|---|---|
| [Runtime selection and profiles](references/runtime-selection.md) | Target harness, surface, scope, native layout, templates, and runtime checks | Before choosing a format or destination |
| [Elicitation guide](references/elicitation-guide.md) | Discovery coverage and resolving missing decisions | Creating or materially changing a workflow; unresolved material decisions |
| [Session distillation](references/session-distillation.md) | Translating feedback without changing its scope | Improving instructions from a conversation or failure |
| [Review rubric](references/review-rubric.md) | Universal quality criteria and finding format | Reviewing an asset together with its selected runtime profile |
| [Agent body scaffold](assets/agent.template.md) | Shared instruction structure | Composing a native agent wrapper |
| [Skill body scaffold](assets/skill.template.md) | Shared workflow structure | Composing a native skill wrapper |
| [Validator](scripts/validate_agent_skill.py) | Executable structural checks and CLI help | Verifying files; change it when changing a lint rule |

## Shared Workflow

1. **Establish the request and runtime.** Read the prompt, relevant files, and existing approvals. Follow runtime selection to establish the target harness, surface/version, scope, and artifact kind; ask when a material target decision is missing. Select a mode below. Use the elicitation guide for creation or material workflow changes and unresolved decisions, screening evidence before asking.
2. **Check ownership and overlap.** Inspect nearby agents, skills, and instruction files. Identify the canonical owner of each changed concept before editing. Extend an existing owner when it already covers the task; use references for dependent components.
3. **Make the scoped change.** Follow the selected mode. Add guidance that changes decisions or supplies needed context. Research external standards when their applicability or current behavior matters. Add scripts for demonstrated repetition or fragile deterministic work; parallelize independent operations when useful and collect their results before making dependent decisions.
4. **Verify the result.** Apply the universal rubric plus each selected runtime profile's native checks. Test changed scripts against meaningful failures. For substantial workflows, exercise realistic requests and compare old/new outputs when warranted and supported. Report structural lint, native discovery, and observed task behavior separately for each target.
5. **Deliver evidence.** Return changed paths, resulting behavior, verification evidence, checks actually run, and unresolved limits. Fix newly introduced failures within scope. After two unsuccessful repair attempts on the same failure, report the evidence and remaining blocker instead of repeating the same action. For review-only requests, return findings without applying repairs.

Keep shared purpose and routing here. Move substantial conditional detail into linked resources. Choose examples, structured data, or prose according to the actual consumer; neither a persona block nor a rigid output schema is required for every task.

## Final Artifact Layout & Skill Anatomy

The selected [runtime profile](references/runtime-selection.md#supported-profiles--native-layout-matrix) owns native filesystem destinations, discovery roots, and agent wrapper formats. Concrete agent files (`.agent.md`, `.toml`, `.json`) belong at their profile's designated agent path (e.g., `.github/agents/`, `.codex/agents/`, `.claude/agents/`).

Portable skills created or audited by this builder follow a standard package anatomy under the target runtime's skill root:

```text
<selected-runtime-skill-root>/
  <skill-name>/
    SKILL.md       # Canonical skill workflow entrypoint
    references/    # Optional execution guidance, schemas, or detailed examples
    scripts/       # Optional executable helpers and their dependencies
    assets/        # Optional templates or resources used in generated outputs
    tests/         # Optional meaningful regression checks and fixtures
```

- Generate agents in their profile's native format and destination as defined in [runtime selection](references/runtime-selection.md). Add optional skill metadata only when needed and supported by that profile.
- For new portable skills, use a lowercase hyphenated folder matching explicit frontmatter `name`, and supply `description`. These are builder authoring conventions; native defaults and optional fields vary. Create only useful supporting directories.
- Keep skill-specific resources inside their owning package. Link shared rules from their existing canonical owners rather than copying them into each package.
- Resolve links, command working directories, resource URIs, and preload bindings using the selected runtime. A Markdown link does not necessarily register or preload a skill.
- Update existing assets in place and preserve their names and locations unless the request authorizes a move or rename. Update affected callers when a location changes.
- Distinguish the customization package from the artifacts it produces: generated requirements, code, reports, and other task outputs belong at their consumer's specified destination, not automatically inside the skill package.

Common body scaffolds own starting instruction structure; native wrappers and layout belong to their runtime profiles. For multiple targets, use runtime selection's composition guidance so shared definitions remain maintainable and accessible to each consumer.

## Mode 1: Creation

- Define the intended request, activation boundary, inputs, output, and success criteria from the available evidence.
- Compose the common body scaffold with the selected native wrapper. Replace placeholders and remove unused sections and authoring notes.
- For agents, define responsibility and tool access; link procedural skills with dispatch conditions. Restrict tools to the workflow's needs.
- For skills, put selection criteria in the frontmatter description. Keep the body focused on execution. Create references, scripts, or assets only when they serve a concrete use.
- Include a useful happy path, required preconditions, verification, and only the failure branches the task needs.

## Mode 2: Update / Distillation

- Preserve the asset's name, location, supported metadata, existing authorization boundaries, and unrelated behavior unless the request changes them.
- Apply focused edits for explicit requirements. Use the session-distillation reference when feedback needs interpretation.
- Check dependent links and callers when changing paths, commands, or output contracts. Update affected callers without duplicating the definition.

### Onboarding REPLACE / IMPROVE

Treat a supplied Replacement Spec or gap description as answered discovery. Preserve its retained instructions, target path, and approval state. REPLACE uses the creation scaffold; IMPROVE changes the identified gaps. Follow the batch/review boundary when resolving replacement audits; do not reopen decisions already approved. If an approval remains pending, prepare the replacement and concrete diff before requesting it.

Carry the onboarding target into runtime selection. Resolve missing material harness/surface/version details without replacing a confirmed target with the builder's host environment. Preserve requirements the target cannot express as explicit migration limitations.

## Mode 3: Review

- Read the requested assets and their relevant resources. Assess them using the review rubric.
- Distinguish reproducible defects, evidence-based risks, and optional improvements. A stylistic preference is not a platform requirement.
- Return a proportionate findings report. Apply repairs only when the user's request includes them; a comparison or audit alone does not authorize edits.

## Verification Tooling

Prerequisites: Python 3.10+ with the declared YAML/TOML dependencies. PowerShell is needed only for the compatibility entrypoint. Install dependencies when needed:

```powershell
python -m pip install -r scripts/requirements.txt
```

Run from the repository root, or supply `--root`:

```powershell
# One entrypoint
powershell -NoProfile -File scripts/validate_agent_skill.ps1 --path "path/to/<name>.agent.md" --json

# A whole skill package, including supporting Markdown links
powershell -NoProfile -File scripts/validate_agent_skill.ps1 --path "path/to/<package-folder>" --json

# A native Codex agent
python scripts/validate_agent_skill.py --runtime codex --path ".codex/agents/<name>.toml" --json

# Discover supported native workspace entrypoints
powershell -NoProfile -File scripts/validate_agent_skill.ps1 --terse

# Validator regression suite
python -m unittest discover -s tests -v
```

Use `--help` for options. The PowerShell entrypoint preserves the existing command interface and delegates to the Python validator. Missing dependencies fail explicitly; dependencies are not installed by the validator.

Use `--runtime` for external or relocated files; automatic selection follows native paths. A single relocated file with an explicit native runtime is checked as an agent unless its role is recognizable as a skill or `--kind` selects another role. Use `--kind resource` for syntax/link-only validation of an external supporting file. Folder scans infer each resource's role independently. Checks cover YAML/JSON/TOML syntax, required authoring fields, selected native structures, UTF-8, and inline relative Markdown file links. The 220-character description warning is an editorial heuristic, not a platform limit. This is partial structural lint, not exhaustive native schema validation, actual tool availability, native discovery, link-anchor validation, semantic routing, or performance evidence.
