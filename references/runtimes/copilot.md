# GitHub Copilot (VS Code)

Official documentation checked: 2026-10-27.

## Native Layout & Semantics

- **Project agent:** `.github/agents/<name>.agent.md` (YAML frontmatter + Markdown body). **Personal:** `~/.copilot/agents/<name>.agent.md`.
- **Project skill:** `.github/skills/<name>/SKILL.md` (VS Code also discovers `.claude/skills/` and `.agents/skills/`). **Personal:** `~/.copilot/skills/<name>/SKILL.md`.
- **Harness differences:** Header fields, tool names, model selection, hooks, and delegation vary between VS Code Local and GitHub Copilot. Neither the model vendor nor `target` selects the harness.
- **Skill linking & tools:** Link procedural skills in the agent Markdown body; do not use a frontmatter `skills` preload key. Scope `tools` to specific available tool names rather than the broad `vscode` bundle. Local UI handoffs are not portable to cloud Copilot.

## Templates & Validation

- **Agent template:** [agent.template.md](../../assets/runtimes/copilot/agent.template.md)
- **Lint:** `python scripts/validate_agent_skill.py --runtime copilot --path <target>`

## Sources

- [Custom agents](https://code.visualstudio.com/docs/agent-customization/custom-agents)
- [Custom agent file reference](https://code.visualstudio.com/docs/agents/reference/custom-agent-file-reference)
- [Agent skills](https://code.visualstudio.com/docs/agent-customization/agent-skills)
