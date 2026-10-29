# Kiro

Official documentation checked: 2026-10-27.

## Native Layout & Semantics

- **Project agent:** Prefer `.kiro/agents/<name>.md` (YAML frontmatter with `tools`, `resources`, `permissions` + Markdown body). Also accepts `.kiro/agents/<name>.json` for machine generation.
- **Project skill:** `.kiro/skills/<name>/SKILL.md`. **Personal:** `~/.kiro/skills/<name>/SKILL.md`.
- **Bindings & permissions:** Bind skills via `resources: ["skill://..."]` (not a `skills` frontmatter key). Current permission configuration uses `permissions.rules` (legacy `allowedTools`/`toolsSettings` require migration); do not add broad preapprovals by default.
- **Surface limits:** Primary custom agent selection works in local IDE/CLI; Web delegation and Mobile surfaces have documented restrictions.

## Templates & Validation

- **Agent template:** [agent.template.md](../../assets/runtimes/kiro/agent.template.md)
- **Lint:** `python scripts/validate_agent_skill.py --runtime kiro --path <target>`

## Sources

- [Custom agents](https://kiro.dev/docs/custom-agents)
- [Skills & resource binding](https://kiro.dev/docs/skills)
