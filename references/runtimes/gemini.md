# Google Gemini & Antigravity

Official documentation checked: 2026-10-28. Covers Google Gemini CLI and the Antigravity IDE/Agent runtime.

## Native Layout & Semantics

- **Project skill:** `.gemini/skills/<name>/SKILL.md` (Gemini CLI), `.agents/skills/<name>/SKILL.md` (Antigravity/universal), or `skills/<name>/SKILL.md`.
- **Personal skill:** `~/.gemini/config/skills/<name>/SKILL.md` (Antigravity), `~/.gemini/skills/<name>/SKILL.md` (Gemini CLI), or `~/.gemini/antigravity/skills/<name>/SKILL.md`.
- **Project instructions & agents:** Repo-wide instructions live in `GEMINI.md` or workspace rules. Custom agents/subagents use `.gemini/agents/<name>.md`, plugin bundles, or conversation subagent tools (`define_subagent` / `invoke_subagent`).

## Templates & Validation

- **Skill template:** [skill.template.md](../../assets/skill.template.md)
- **Lint:** `python scripts/validate_agent_skill.py --runtime gemini --path <target>` (or `--runtime antigravity`).

## Sources

- [Antigravity Documentation](https://cloud.google.com)
- [Gemini CLI Documentation](https://ai.google.dev)
