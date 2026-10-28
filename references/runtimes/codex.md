# Codex

Official OpenAI documentation checked: 2026-10-27. Confirm the target Codex surface/version and its exposed customization capabilities before using optional settings.

## Native Layout and Semantics

- **Project custom agent**: `.codex/agents/<name>.toml`; personal: `~/.codex/agents/<name>.toml`. A standalone TOML agent requires `name`, `description`, and `developer_instructions`.
- **Repository skills**: `.agents/skills/<name>/SKILL.md`; personal skills: `~/.agents/skills/<name>/SKILL.md`. Codex discovers repository locations along the working-directory ancestor chain. Existing system/plugin locations are separate from this authoring convention.
- **Project instructions**: Belong in `AGENTS.md`, with documented override behavior. A custom agent is a delegation role, not a substitute instruction file or a VS Code picker definition.
- **Skill UI metadata (`openai.yaml`)**: An optional companion file placed at `<skill-folder>/agents/openai.yaml`. Use this ONLY when authoring or packaging a skill for OpenAI Codex/ChatGPT that requires custom UI presentation (`display_name`, `short_description`, `default_prompt`) or custom invocation policy (e.g. disabling implicit triggering so the skill only runs when explicitly requested with `$skill-name`). Standard skills work with `SKILL.md` alone.
- **Inherited permissions**: Custom agents inherit parent permissions/provider/MCP configuration. A native agent TOML file cannot replace those controls with a Copilot `tools` array or a new sandbox policy.

## Templates

- [Agent TOML template](../../assets/runtimes/codex/agent.template.toml) (for `.codex/agents/<name>.toml`)
- [Optional skill UI metadata](../../assets/runtimes/codex/openai.template.yaml) (for `<skill-folder>/agents/openai.yaml`)
- [Universal skill template](../../assets/skill.template.md)

## Runtime Review

Check TOML types, required instructions, documented capabilities, discovery scope, and callable agent/skill identities. Keep model and effort settings inherited unless the request needs an override. Do not rename a Copilot YAML file to `.toml` or assume its keys work unchanged.

Use `--runtime codex` for structural checks; Python 3.10 needs the declared TOML fallback dependency. Verify native discovery and a representative delegated task separately when that surface is available. Preserve inherited authority and distinguish a desired behavioral restriction from a permission mechanism. Leave any unsupported migration requirement visible rather than adding guessed configuration keys.

## Sources

- [Custom agents and inherited controls](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Skills, locations, invocation, and optional metadata](https://learn.chatgpt.com/docs/build-skills)
- [Project instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
