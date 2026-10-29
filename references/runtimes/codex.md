# OpenAI Codex

Official documentation checked: 2026-10-27.

## Native Layout & Semantics

- **Project custom agent:** `.codex/agents/<name>.toml`. **Personal:** `~/.codex/agents/<name>.toml`. Requires `name`, `description`, and `developer_instructions` (distinct from repo-wide `AGENTS.md` instructions).
- **Project skill:** `.agents/skills/<name>/SKILL.md` (discovered up the directory ancestor chain). **Personal:** `~/.agents/skills/<name>/SKILL.md`.
- **Optional skill UI metadata:** `<skill-folder>/agents/openai.yaml` (`display_name`, `short_description`, `default_prompt`, invocation policy). Include only when custom UI metadata or explicit-only `$skill-name` invocation is needed.
- **Inherited permissions:** Custom agents inherit parent permissions, provider, and MCP config. Do not add a `tools` array or sandbox policy to agent TOML files; leave model/effort inherited unless requested.

## Templates & Validation

- **Agent template:** [agent.template.toml](../../assets/runtimes/codex/agent.template.toml)
- **Skill UI metadata template:** [openai.template.yaml](../../assets/runtimes/codex/openai.template.yaml)
- **Lint:** `python scripts/validate_agent_skill.py --runtime codex --path <target>` (requires `tomli` on Python 3.10).

## Sources

- [Custom agents & subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Build skills](https://learn.chatgpt.com/docs/build-skills)
- [AGENTS.md project instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
