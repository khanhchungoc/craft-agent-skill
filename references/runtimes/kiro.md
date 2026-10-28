# Kiro

Official documentation checked: 2026-10-27. The current template baseline is IDE 1.x / CLI V3. Identify the surface and version; do not silently convert a CLI 2.x or IDE 0.x deployment using current assumptions.

## Native Layout and Semantics

- Project agents: `.kiro/agents/<name>.json` or `.kiro/agents/<name>.md`; personal equivalents live in `~/.kiro/agents/`. JSON configuration and YAML-frontmatter/Markdown profiles have corresponding fields; the JSON template below uses an inline `prompt`.
- Project skills: `.kiro/skills/<name>/SKILL.md`; personal: `~/.kiro/skills/<name>/SKILL.md`. Skills activate through matching or explicit slash invocation. Steering and powers are different customization mechanisms.
- Agent `resources` can use `skill://` for progressive skill loading and `file://` for startup context. A `prompt` file URI resolves relative to the agent config directory. Do not assume resource schemes are portable to another runtime.
- Current permission configuration uses `permissions.rules`. Legacy `allowedTools`/`toolsSettings` profiles may require the documented upgrade path. Do not introduce broad preapprovals as part of authoring.
- Project agent selection differs by surface: local IDE/CLI can select a primary custom agent; Web delegation and Mobile availability have documented limits.

## Templates

- [Current JSON agent](../../assets/runtimes/kiro/agent.template.json)
- [Current Markdown agent](../../assets/runtimes/kiro/agent.template.md)
- [Skill wrapper](../../assets/runtimes/kiro/skill.template.md)
- Body scaffolds: [agent](../../assets/agent.template.md), [skill](../../assets/skill.template.md).

## Runtime Review

Check actual field support, selected tools, resource discovery, workspace trust, and parent policy for the selected version/surface. Do not transplant VS Code aliases, Claude preload fields, or Codex TOML settings. Preserve existing permission decisions and flag unsupported legacy migration items explicitly.

Use `--runtime kiro` for basic syntax/structural checks. Verify native loading and skill activation separately; a schema-shaped JSON file does not prove that its resources are available or its permissions behave as intended. When a legacy target is requested, inspect its matching official reference and adapt the template before generating final files.

## Sources

- [Agent formats, paths, surface support, and version differences](https://kiro.dev/docs/custom-agents/)
- [Configuration and resource semantics](https://kiro.dev/docs/custom-agents/configuration-reference/)
- [Skill locations and activation](https://kiro.dev/docs/skills/)
