# Kiro

Official documentation checked: 2026-10-27. Confirm the target Kiro version and verify whether it uses structured JSON or frontmatter Markdown for custom agents.

## Native Layout and Semantics

- Project agent: `.kiro/agents/<name>.json` (or `.kiro/agents/<name>.md`). Current versions configure tools, resource URIs, and permission rules within the profile.
- Project skills: prefer `.kiro/skills/<name>/SKILL.md`. Discoverable locations also include parent working directories.
- Current permission configuration uses `permissions.rules`. Legacy `allowedTools`/`toolsSettings` profiles may require the documented upgrade path. Do not introduce broad preapprovals as part of authoring.
- Project agent selection differs by surface: local IDE/CLI can select a primary custom agent; Web delegation and Mobile availability have documented limits.

## Templates

- [Current JSON agent](../../assets/runtimes/kiro/agent.template.json)
- [Current Markdown agent](../../assets/runtimes/kiro/agent.template.md)
- [Universal skill template](../../assets/skill.template.md)

## Runtime Review

Check actual field support, selected tools, resource discovery, workspace trust, and parent policy for the selected version/surface. Do not transplant VS Code aliases, Claude preload fields, or Codex TOML settings. Preserve existing permission decisions and flag unsupported legacy migration items explicitly.

Use `--runtime kiro` for basic syntax/structural checks. Verify native loading and skill activation separately; a schema-shaped JSON file does not prove that its resources are available or its permissions behave as intended. When a legacy target is requested, inspect its matching official reference and adapt the template before generating final files.

## Sources

- [Agent schemas, fields, tools, and permissions](https://kiro.dev/docs/custom-agents)
- [Skill discovery and resource binding](https://kiro.dev/docs/skills)
