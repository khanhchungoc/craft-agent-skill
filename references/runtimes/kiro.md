# Kiro

Official documentation checked: 2026-10-27. Use frontmatter Markdown as the standard agent format for readability.

## Native Layout and Semantics

- **Project agent**: Prefer `.kiro/agents/<name>.md`. Markdown frontmatter (`tools`, `resources`, `permissions`) combined with a Markdown body for instructions avoids escaping newlines in JSON strings. Kiro also accepts `.kiro/agents/<name>.json` (primarily used for machine generation).
- **Project skills**: Prefer `.kiro/skills/<name>/SKILL.md`. Personal skills reside in `~/.kiro/skills/<name>/SKILL.md`. Discoverable locations also include parent working directories.
- Current permission configuration uses `permissions.rules`. Legacy `allowedTools`/`toolsSettings` profiles may require the documented upgrade path. Do not introduce broad preapprovals as part of authoring.
- Project agent selection differs by surface: local IDE/CLI can select a primary custom agent; Web delegation and Mobile availability have documented limits.

## Templates

- [Agent Markdown template](../../assets/runtimes/kiro/agent.template.md) (Standard)
- [Universal skill template](../../assets/skill.template.md)

## Runtime Review

Check actual field support, selected tools, resource discovery, workspace trust, and parent policy for the selected version/surface. Do not transplant VS Code aliases, Claude preload fields, or Codex TOML settings. Preserve existing permission decisions and flag unsupported legacy migration items explicitly.

Use `--runtime kiro` for basic syntax/structural checks. Verify native loading and skill activation separately; a valid template file does not prove that its resources are available or its permissions behave as intended. When a legacy target is requested, inspect its matching official reference and adapt the template before generating final files.

## Sources

- [Agent schemas, fields, tools, and permissions](https://kiro.dev/docs/custom-agents)
- [Skill discovery and resource binding](https://kiro.dev/docs/skills)
