# Google Gemini & Antigravity

Official documentation checked: 2026-10-28. This profile covers Google Gemini CLI and the Antigravity Agent runtime.

## Native Layout and Semantics

- Project skills: `skills/<name>/SKILL.md` or `.agents/skills/<name>/SKILL.md`.
- Personal / User skills: `~/.gemini/antigravity/skills/<name>/SKILL.md`.
- Skills use standard Markdown with YAML frontmatter (`name`, `description`).
- Custom agents & subagents: Defined via plugin bundles or conversation subagent configurations.
- Native tools: File operations, shell execution, subagent dispatch, MCP tools.

## Templates

- [Skill wrapper](../../assets/runtimes/gemini/skill.template.md)
- Body scaffolds: [agent](../../assets/agent.template.md), [skill](../../assets/skill.template.md).

## Runtime Review

Ensure frontmatter contains `name` and a concise `description` for routing. Verify tool execution permissions and paths relative to the active workspace.

Validate files with `--runtime gemini` or `--runtime universal`.

