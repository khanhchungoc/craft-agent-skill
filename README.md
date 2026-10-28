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

## Installation

### Method 1: The Universal `skills` CLI (Recommended)

Using the open agent skills package manager ([skills.sh](https://skills.sh/)), you can install with a single command without even cloning:

```bash
# 📦 Project-level installation (into current repository)
npx skills add khanhchungoc/craft-agent-skill

# 🌍 User-level installation (global across all projects)
npx skills add khanhchungoc/craft-agent-skill -g

# Target a specific agent harness (e.g. Claude Code or GitHub Copilot)
npx skills add khanhchungoc/craft-agent-skill -a claude-code
npx skills add khanhchungoc/craft-agent-skill -a github-copilot
```

---

### Method 2: Native Zero-Dependency Scripts (PowerShell & Bash)

If you have already cloned the repository or are working in a terminal without Node.js:

#### Windows (PowerShell)
```powershell
# 🌍 User-level (global) for all detected agents (uses NTFS directory junctions)
.\scripts\install.ps1 -Scope User

# 📦 Project-level for a specific runtime (e.g., GitHub Copilot)
.\scripts\install.ps1 -Scope Project -Runtime github-copilot

# 📦 Project-level with the optional @agent-skill-builder Copilot agent wrapper
.\scripts\install.ps1 -Scope Project -Runtime github-copilot -WithAgent

# Install as standalone copy instead of symlink
.\scripts\install.ps1 -Scope Project -Runtime all -Mode Copy
```

#### macOS / Linux (Bash)
```bash
# 🌍 User-level (global)
./scripts/install.sh --scope user

# 📦 Project-level
./scripts/install.sh --scope project --runtime claude-code
```

---

### Method 3: Git Submodule (For Version-Controlled Repos)

If you want to pin this skill directly in your project's Git repository:

```bash
# GitHub Copilot
git submodule add https://github.com/khanhchungoc/craft-agent-skill.git .github/skills/craft-agent-skill

# Claude Code
git submodule add https://github.com/khanhchungoc/craft-agent-skill.git .claude/skills/craft-agent-skill

# OpenAI Codex
git submodule add https://github.com/khanhchungoc/craft-agent-skill.git .agents/skills/craft-agent-skill
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
│       ├── github-copilot/           # GitHub Copilot agent and skill wrappers
│       └── kiro/                     # Kiro JSON and Markdown wrappers
├── references/                       # In-depth architectural & review guides
│   ├── elicitation-guide.md          # Progressive discovery and decision trees
│   ├── review-rubric.md              # Quality dimensions and audit checklist
│   ├── runtime-selection.md          # Matrix of runtime profiles and paths
│   ├── session-distillation.md       # Distilling feedback into instruction edits
│   └── runtimes/                     # Native surface constraints per runtime
├── scripts/                          # Structural linting, installer, and validation tools
│   ├── install.ps1                   # Native PowerShell installer
│   ├── install.sh                    # Native Bash installer
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
