# Claude Code

Official documentation checked: 2026-10-27. Covers local Claude Code CLI/Desktop authoring (Cowork and cloud surfaces have separate availability rules).

## Native Layout & Semantics

- **Project subagent:** `.claude/agents/<name>.md` (YAML frontmatter + Markdown body; distinct from repo-wide `CLAUDE.md`). **Personal:** `~/.claude/agents/<name>.md`.
- **Project skill:** `.claude/skills/<name>/SKILL.md` (supports `/skill-name` slash invocation and description matching). **Personal:** `~/.claude/skills/<name>/SKILL.md`.
- **Tools:** Native tool names (e.g., `Read`, `Grep`, `Glob`, `Edit`, `Bash`) are case-sensitive. `tools` accepts a comma-separated string or YAML list; omitting `tools` inherits available subagent tools. Include `Skill` when an explicit tool list needs on-demand skill invocation.
- **Skill preload & execution:** Frontmatter `skills: [<skill-name>]` preloads skill content into a subagent (distinct from on-demand skill invocation and skill `context: fork` execution). Always include explicit `name` and `description` in portable packages.

## Templates & Validation

- **Subagent template:** [agent.template.md](../../assets/runtimes/claude-code/agent.template.md)
- **Lint:** `python scripts/validate_agent_skill.py --runtime claude-code --path <target>` (verify discovery via `/agents` in CLI when available).

## Sources

- [Subagents](https://code.claude.com/docs/en/sub-agents)
- [Skills](https://code.claude.com/docs/en/skills)
