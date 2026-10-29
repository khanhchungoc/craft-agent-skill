# Runtime Selection and Composition

## Establish the Target Before Choosing a Format

Recover an explicit target from the request or approved specification. Existing files identify the source format, not necessarily the intended destination. The editor, model provider, and agent harness are separate choices: using a Claude model in Copilot does not make the consumer Claude Code, and using Codex in VS Code does not make the consumer Copilot.

If unresolved, ask a focused question such as: *"Where will these customizations run: Copilot, Claude Code, Codex, Gemini / Antigravity, Kiro, or another harness?"* For multiple targets, identify every target explicitly. For a narrow in-place update without a migration request, retain the established consumer rather than reopening runtime selection.

Pause only dependent scaffolding when the harness or a material contract (scope, artifact kind, activation, or tool authority) is unknown; continue collecting shared workflow requirements. Do not install runtimes, alter global configuration, grant permissions, or activate generated agents merely to author templates.

## Supported Profiles & Native Layout Matrix

Each profile owns the exact file formats and native filesystem destinations for agents and skills:

| Profile ID | Consumer | Project Agent Path & Format | Project Skill Root | Personal / User Scope | Native Profile Details |
|---|---|---|---|---|---|
| `copilot` | GitHub Copilot (VS Code / Local) | `.github/agents/<name>.agent.md` (Markdown + YAML) | `.github/skills/<name>/` | `~/.copilot/agents/<name>.agent.md`, `~/.copilot/skills/<name>/` | [Copilot profile](runtimes/copilot.md) |
| `claude-code` | Claude Code CLI & Desktop | `.claude/agents/<name>.md` (Markdown + YAML) | `.claude/skills/<name>/` | `~/.claude/agents/`, `~/.claude/skills/` | [Claude Code profile](runtimes/claude-code.md) |
| `codex` | OpenAI Codex | `.codex/agents/<name>.toml` (TOML format) | `.agents/skills/<name>/` | `~/.codex/agents/`, `~/.agents/skills/` | [Codex profile](runtimes/codex.md) |
| `gemini` | Google Gemini & Antigravity | Subagent definitions / Custom | `.gemini/skills/<name>/`, `.agents/skills/<name>/` | `~/.gemini/config/skills/<name>/`, `~/.gemini/skills/<name>/` | [Gemini profile](runtimes/gemini.md) |
| `kiro` | Kiro IDE / CLI | `.kiro/agents/<name>.md` (or `.json`) | `.kiro/skills/<name>/` | `~/.kiro/skills/<name>/` | [Kiro profile](runtimes/kiro.md) |

For another runtime, inspect its current official customization documentation and add a profile/templates before claiming support. For a legacy version, verify that version's contract rather than assuming current templates are backward compatible.

## Multi-Target & Cross-Runtime Rules

- Read only the selected runtime profiles. Preserve any requirement that a target cannot express as an explicit limitation or unresolved migration item rather than silently dropping it.
- For multiple targets, keep one maintained owner for shared procedural rules when all selected consumers can access it via supported links, discovery locations, or packaging. Do not assume a Markdown link installs a skill or that every runtime follows the same symlinks, resource URIs, or preload fields.
- Validate and report per runtime. A pass for one wrapper does not establish compatibility for others.
