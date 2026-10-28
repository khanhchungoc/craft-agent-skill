# Claude Code

Official documentation checked: 2026-10-27. This profile covers local Claude Code authoring; account-synced, Cowork, and cloud skill availability require their own surface checks.

## Native Layout and Semantics

- Project subagent: `.claude/agents/<name>.md`; personal subagent: `~/.claude/agents/<name>.md`. The YAML header configures the agent; the Markdown body supplies its instructions. Subagents are distinct from repository-wide `CLAUDE.md` guidance.
- Project skill: `.claude/skills/<name>/SKILL.md`; personal skill: `~/.claude/skills/<name>/SKILL.md`. Skills support explicit slash invocation and description-based selection.
- Native tool names such as `Read`, `Grep`, and `Glob` are case-sensitive identities to verify, not Copilot aliases. `tools` supports a string or list. Omission inherits available subagent tools.
- Agent `skills` is supported for preloading skill content. It is not a Copilot agent field. Preserve the distinction between preload, on-demand skill access, and a skill's `context: fork` execution. Check versions and invocation policy before adding optional fields.

## Templates

- [Subagent wrapper](../../assets/runtimes/claude-code/agent.template.md)
- [Skill wrapper](../../assets/runtimes/claude-code/skill.template.md)
- Body scaffolds: [agent](../../assets/agent.template.md), [skill](../../assets/skill.template.md).

## Runtime Review

Establish whether the deliverable is a main-session customization or a delegated subagent, what context it receives, and which operations it can actually perform. With an explicit tool list, provide `Skill` when on-demand skill invocation is needed, or deliberately preload the needed skills. A prompt saying "read-only" is not an operating-system security boundary. Preserve existing permission modes and preload decisions unless the requested change addresses them.

For new portable packages, author explicit `name` and `description` even where Claude can infer them; this is the builder's authoring convention, not a claim that every native skill field is required. Do not introduce model-specific settings, command substitutions, hooks, or permission grants without a task-driven need and version check.

Use `--runtime claude-code` for structural checks. When the CLI is available, inspect `/agents` and the skill command listing, then exercise an appropriate harmless request. Discovery alone does not prove correct delegation or artifact quality.

## Sources

- [Subagent format, fields, tools, context, and preload](https://code.claude.com/docs/en/sub-agents)
- [Skill locations, fields, invocation, and hosted-surface differences](https://code.claude.com/docs/en/skills)
