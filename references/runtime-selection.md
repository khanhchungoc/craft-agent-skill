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
| `claude` | Claude Code CLI & Desktop | `.claude/agents/<name>.md` (Markdown + YAML) | `.claude/skills/<name>/` | `~/.claude/agents/`, `~/.claude/skills/` | [Claude profile](runtimes/claude.md) |
| `codex` | OpenAI Codex | `.codex/agents/<name>.toml` (TOML format) | `.agents/skills/<name>/` | `~/.codex/agents/`, `~/.agents/skills/` | [Codex profile](runtimes/codex.md) |
| `gemini` | Google Gemini & Antigravity | Subagent definitions / Custom | `.gemini/skills/<name>/`, `.agents/skills/<name>/` | `~/.gemini/config/skills/<name>/`, `~/.gemini/skills/<name>/` | [Gemini profile](runtimes/gemini.md) |
| `kiro` | Kiro IDE / CLI | `.kiro/agents/<name>.md` (or `.json`) | `.kiro/skills/<name>/` | `~/.kiro/skills/<name>/` | [Kiro profile](runtimes/kiro.md) |

For another runtime, inspect its current official customization documentation and add a profile/templates before claiming support. For a legacy version, verify that version's contract rather than assuming current templates are backward compatible.

## Instruction Placement: Agent vs. Skill vs. Steering

Before creating or reviewing an agent/skill, decide whether each instruction belongs there at all. Steering (always-on or file-scoped instructions) is a third owner alongside agents and skills.

| Layer | Put here when the instruction... | Avoid when |
|---|---|---|
| Steering / repo instructions | Is a standing convention (coding style, naming, test/build commands, architecture rules) that applies regardless of task, or to files matching a glob | It is a multi-step procedure used only for one task type, or needs scripts/assets |
| Agent | Defines a role: responsibility boundary, tool/permission scope, which skills to mount and when | It is a reusable procedure or a repo-wide convention |
| Skill | Is an on-demand procedure with its own references/scripts, triggered by task type | It must apply on every request (it may never activate) or is tiny and file-scoped |

Native steering locations (web-verified 2026-10-29 against current docs; re-check before relying on version-specific behavior):

| Profile | Always-on | Scoped / conditional | Notes |
|---|---|---|---|
| `copilot` | `.github/copilot-instructions.md`; `AGENTS.md` (nearest file wins) | `.github/instructions/**/*.instructions.md` with `applyTo` glob frontmatter | VS Code and GitHub Copilot cloud differ in supported files |
| `claude` | `./CLAUDE.md`, `~/.claude/CLAUDE.md` | `.claude/rules/*.md`, `~/.claude/rules/*.md`; `paths` frontmatter loads on matching file reads, omitted `paths` means always loaded | Reads `CLAUDE.md`, not `AGENTS.md` |
| `codex` | `AGENTS.md` at repo root, `~/.codex/AGENTS.md` | Nested `AGENTS.md` per directory (one file per directory, deeper files appear later); `AGENTS.override.md` replaces `AGENTS.md` in its directory | Combined chain capped by `project_doc_max_bytes` (32 KiB default); excess is truncated |
| `gemini` | `GEMINI.md` / `AGENTS.md` walked up to repo root (Antigravity); `~/.gemini/GEMINI.md` plus parent/subdirectory `GEMINI.md` (Gemini CLI) | Antigravity `.agents/rules/*.md` with frontmatter `trigger` (`always_on`, `model_decision`, ...); standalone `GEMINI.md`/`AGENTS.md` take no frontmatter | Antigravity: 24 KB per rule file, 20k-token always-on budget with over-budget rules demoted to path pointers; invalid `trigger` values are silently dropped |
| `kiro` | `.kiro/steering/*.md` (`inclusion: always`, the default), `~/.kiro/steering/` | `inclusion: fileMatch` + `fileMatchPattern`; `manual` (invoked by name); `auto` (description-matched, newer versions) | Conditional modes vary by surface/version |

Placement rules:
- Move a convention out of an agent or skill into steering when it repeats across several of them or must hold outside them; link or reference it rather than copying (see SSOT).
- Keep steering short: it is loaded into context every time it matches. Push long procedures into a skill and leave a one-line pointer.
- Do not create or edit steering files for a request limited to an agent/skill; propose the move and let the user approve, since steering affects every session in the repo.
- Report a placement finding per target runtime; when a runtime has no equivalent, say so.

## Multi-Target & Cross-Runtime Rules

- Read only the selected runtime profiles. Preserve any requirement that a target cannot express as an explicit limitation or unresolved migration item rather than silently dropping it.
- For multiple targets, keep one maintained owner for shared procedural rules when all selected consumers can access it via supported links, discovery locations, or packaging. Do not assume a Markdown link installs a skill or that every runtime follows the same symlinks, resource URIs, or preload fields.
- Validate and report per runtime. A pass for one wrapper does not establish compatibility for others.
