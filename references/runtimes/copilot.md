# GitHub Copilot (VS Code)

Official documentation checked: 2026-10-27. Select the installed harness and verify capabilities against its current version.

## Native Layout and Semantics

- Project agent: `.github/agents/<name>.agent.md`. Personal Copilot agent: `~/.copilot/agents/<name>.agent.md`. Use YAML frontmatter plus a Markdown body.
- Project skill: prefer `.github/skills/<name>/SKILL.md` for this repository. Current VS Code also discovers `.claude/skills/` and `.agents/skills/`; personal locations differ by harness.
- Header fields, tools, model selection, hooks, and delegation vary between Local and Copilot. A model vendor is not the harness selector, and `target` is not that selector either.
- VS Code-format agents use body links to procedural skills; do not transfer Claude's agent `skills` preload field into this format. Scope tools to the selected harness's available names. Local UI handoffs are not portable to Copilot.

## Templates

- [Agent wrapper](../../assets/runtimes/copilot/agent.template.md)
- [Skill wrapper](../../assets/runtimes/copilot/skill.template.md)
- Body scaffolds: [agent](../../assets/agent.template.md), [skill](../../assets/skill.template.md).

## Runtime Review

Check the chosen harness's tool inventory, actual skill discovery, picker visibility, invocation policy, and relative resource resolution. Do not infer that a Local tool name or UI feature works in a Copilot, Claude, or Codex session hosted in the same editor. Broad tool-bundle checks are local authoring conventions, not a cross-runtime schema.

Validate the selected files structurally with `--runtime copilot`, then inspect the installed VS Code customization UI and use a harmless representative request if authorized and available. Record unavailable tool or discovery checks as unverified. Keep the common workflow and output requirements intact when adapting an existing asset.

## Sources

- [Agent locations and selection](https://code.visualstudio.com/docs/agent-customization/custom-agents)
- [Fields, tool syntax, and harness differences](https://code.visualstudio.com/docs/agents/reference/custom-agent-file-reference)
- [Skill discovery and invocation](https://code.visualstudio.com/docs/agent-customization/agent-skills)
