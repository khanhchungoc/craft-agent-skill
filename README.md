# Craft Agent & Skill

A universal, cross-runtime skill and toolkit to **create**, **update**, **distill**, and **audit** AI agents and skills for **Claude Code**, **OpenAI Codex**, **GitHub Copilot / VS Code**, **Kiro**, **Antigravity / Gemini**, and other modern AI harnesses.

---

## Overview

`craft-agent-skill` equips an AI agent with the procedural expertise to act as a **practical agent customization architect**:
* **Runtime-Agnostic Core**: Shared authoring principles (DRY, SSOT, progressive disclosure, deterministic helpers).
* **Native Layouts & Scaffolds**: Dedicated profiles, scaffolds, and wrappers for each target platform.
* **Structural Linting & Verification**: Standalone Python/PowerShell validator checking frontmatter schemas, link integrity, and platform compatibility.
* **Lossless Maintenance**: Distills conversational feedback into targeted instruction updates without scope drift.

---

## Quick Installation by Runtime

### 1. Claude Code
Install globally or in a specific project:
```bash
# Global
git clone https://github.com/khanhchungoc/craft-agent-skill.git ~/.claude/skills/craft-agent-skill

# Project
git clone https://github.com/khanhchungoc/craft-agent-skill.git .claude/skills/craft-agent-skill
```

### 2. GitHub Copilot / VS Code
Mount the skill inside your repository:
```powershell
# Submodule or direct clone
git submodule add https://github.com/khanhchungoc/craft-agent-skill.git .github/skills/craft-agent-skill
```
> **Optional Agent Wrapper**: If you also want a dedicated `@agent-skill-builder` chat participant in Copilot, copy [assets/runtimes/github-copilot/agent-skill-builder.agent.md](assets/runtimes/github-copilot/agent-skill-builder.agent.md) into `.github/agents/agent-skill-builder.agent.md`.

### 3. OpenAI Codex
```bash
git clone https://github.com/khanhchungoc/craft-agent-skill.git .agents/skills/craft-agent-skill
```

### 4. Antigravity / Gemini CLI
```powershell
git clone https://github.com/khanhchungoc/craft-agent-skill.git skills/craft-agent-skill
```

---

## Repository Structure

```text
craft-agent-skill/
├── SKILL.md                          # Universal skill entrypoint
├── README.md                         # Documentation and runtime quickstart
├── assets/                           # Runtime scaffolds and body templates
│   ├── agent.template.md             # Shared agent body scaffold
│   ├── skill.template.md             # Shared skill workflow scaffold
│   └── runtimes/                     # Native wrappers per platform
│       ├── claude-code/              # Claude Code agent and skill wrappers
│       ├── codex/                    # Codex TOML and YAML agent/skill wrappers
│       ├── kiro/                     # Kiro JSON and Markdown wrappers
│       └── github-copilot/           # VS Code Copilot agent and skill wrappers
├── references/                       # In-depth architectural & review guides
│   ├── elicitation-guide.md          # Progressive discovery and decision trees
│   ├── review-rubric.md              # Quality dimensions and audit checklist
│   ├── runtime-selection.md          # Matrix of runtime profiles and paths
│   ├── session-distillation.md       # Distilling feedback into instruction edits
│   └── runtimes/                     # Native surface constraints per runtime
├── scripts/                          # Structural linting and validation tools
│   ├── requirements.txt              # PyYAML & tomli dependencies
│   ├── validate_agent_skill.py       # Core cross-runtime validator CLI
│   └── validate_agent_skill.ps1      # PowerShell compatibility wrapper
└── tests/                            # Comprehensive regression suite
    └── test_validate_agent_skill.py  # 35+ test cases for validator rules
```

---

## Validator & CLI Usage

### Prerequisites
Python 3.10+ is required. Install validator dependencies:
```bash
python -m pip install -r scripts/requirements.txt
```

### Running the Validator
Run structural linting against any agent file, skill package, or entire workspace:

```powershell
# Validate a single agent or skill
python scripts/validate_agent_skill.py --path "path/to/my-agent.agent.md"

# Validate an entire skill folder (including internal relative Markdown links)
python scripts/validate_agent_skill.py --path "path/to/skill-package" --json

# Run against native Codex configuration
python scripts/validate_agent_skill.py --runtime codex --path ".codex/agents/dev.toml"

# PowerShell wrapper
powershell -NoProfile -File scripts/validate_agent_skill.ps1 --path "path/to/asset"
```

### Running the Test Suite
```bash
python -m unittest discover -s tests -v
```

---

## License
MIT (or your preferred repository license).
