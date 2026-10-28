# Runtime Selection and Composition

This reference owns target-runtime discovery, profile selection, and native artifact layout. The [shared rubric](review-rubric.md) owns universal quality principles; each profile owns native layout, templates, and runtime-specific review checks.

## Establish the Target Before Choosing a Format

Recover an explicit target from the request or approved specification. Existing files identify the source format, not necessarily the intended destination. The editor, model provider, and agent harness are separate choices: using a Claude model in Copilot does not make the consumer Claude Code, and using Codex in VS Code does not make the consumer Copilot.

If unresolved, ask a focused question such as: "Where will these customizations run: GitHub Copilot, Claude Code, Codex, Kiro, or another harness?" For multiple targets, identify every target explicitly. An existing asset's location is evidence to confirm, not permission to choose a new destination silently.

For a narrow in-place update without a migration request, retain an established consumer supported by the existing asset and caller context; do not reopen runtime selection merely to edit wording. Ask when destination, format, or required capabilities are materially uncertain.

Resolve these material details from evidence or clarification:

| Decision | Record |
|---|---|
| Harness and surface | Product, CLI/IDE/desktop/cloud surface, and selected harness when hosted in another editor |
| Version and capabilities | Installed version when available; documented baseline otherwise, plus relevant preview flags or organization restrictions |
| Scope and destination | Project, personal, or managed distribution; actual installation/discovery paths and any existing asset being updated |
| Artifact kind | Selectable/session agent, delegated subagent, reusable skill, or persistent project instructions |
| Activation | User selection, explicit skill invocation, automatic matching, preload, or delegation; supported by that exact surface |
| Tools and authority | Available native/MCP tools, script execution environment, and inherited versus configurable permissions |
| Resource resolution | Skill discovery, instruction precedence, relative paths, working directory, and access to shared resources |
| Verification | Available native discovery/configuration checks, harmless test request, and what remains unverified |

Pause only dependent scaffolding when the harness or another material contract is unknown. Continue collecting shared workflow requirements. Do not install runtimes, alter global configuration, grant permissions, or activate generated agents merely to author templates.

## Supported Profiles & Native Layout Matrix

Each profile owns the exact file formats and native filesystem destinations for agents and skills:

| Profile ID | Consumer | Project Agent Path & Format | Project Skill Root | Personal / User Scope | Native Profile Details |
|---|---|---|---|---|---|
| `github-copilot` | GitHub Copilot (VS Code / Local) | `.github/agents/<name>.agent.md` (Markdown + YAML) | `.github/skills/<name>/` | `~/.copilot/agents/<name>.agent.md` | [GitHub Copilot profile](runtimes/github-copilot.md) |
| `claude-code` | Claude Code CLI & Desktop | `.claude/agents/<name>.md` (Markdown + YAML) | `.claude/skills/<name>/` | `~/.claude/agents/`, `~/.claude/skills/` | [Claude Code profile](runtimes/claude-code.md) |
| `codex` | OpenAI Codex | `.codex/agents/<name>.toml` (TOML format) | `.agents/skills/<name>/` | `~/.codex/agents/`, `~/.agents/skills/` | [Codex profile](runtimes/codex.md) |
| `kiro` | Kiro IDE / CLI | `.kiro/agents/<name>.json` (or `.md`) | `.kiro/skills/<name>/` | Surface-dependent | [Kiro profile](runtimes/kiro.md) |

For another runtime, inspect its current official customization documentation and add a profile/templates before claiming support. Do not reinterpret another profile's metadata as equivalent. For a legacy version, verify that version's contract; current templates are not evidence of backward compatibility.

## Compose Shared Logic with Native Wrappers

1. Establish the shared task, input/output contracts, discovery decisions, and verification using [elicitation-guide.md](elicitation-guide.md).
2. Read only the selected runtime profiles. Use the common body scaffolds plus that profile's agent/skill wrapper; remove authoring notes and placeholders from the deliverable.
3. Apply the shared rubric and each selected profile's native checks. Preserve a requirement that the target cannot express as an explicit limitation or unresolved migration item, rather than silently dropping it.
4. For multiple targets, keep one maintained owner for shared procedural rules when all selected consumers can actually access it. Use supported links, discovery locations, or a deliberate packaging process. Do not assume a Markdown link installs a skill or that every runtime follows the same symlinks, resource URIs, or preload fields.
5. Report validation per runtime. Syntax/structural lint, native discovery, and observed task behavior are separate evidence. A pass for one wrapper does not establish compatibility for the others.

The builder authors customizations for target environments regardless of where the builder itself is executed. Preserve existing host files unless migration is explicitly requested.
