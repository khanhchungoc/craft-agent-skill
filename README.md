# Craft Agent & Skill 🛠️

A universal AI skill that teaches your AI coding assistant how to **build**, **refine**, and **audit** custom agents and skills.

Works seamlessly with **GitHub Copilot**, **Claude Code**, **OpenAI Codex**, **Cursor**, **Antigravity**, and **Kiro**.

---

## ⚡ Quick Install

Run this in your terminal to install across all your AI assistants:

```bash
npx khanhchungoc/craft-agent-skill
```

### Options:

* **Current project workspace only:**
  ```bash
  npx khanhchungoc/craft-agent-skill -p
  ```
* **Target a specific assistant:**
  ```bash
  npx khanhchungoc/craft-agent-skill -a antigravity
  npx khanhchungoc/craft-agent-skill -a claude
  npx khanhchungoc/craft-agent-skill -a copilot
  ```

---

## 💬 How to Use

Once installed, your AI assistant automatically gains this skill. You don't need to micromanage instructions, folder layouts, or technical schemas—just express your goal naturally in chat. The skill works out the architecture, elicits missing details, and enforces platform best practices across three core modes:

### 🚀 Mode 1: Creation (Build from Scratch)
Provide high-level intent; the skill elicits requirements, conducts web research for existing skills and industry standards, designs tool boundaries, and scaffolds production-ready agents and skills.

* **Build a custom agent:**
  > *"Create a security review agent for Copilot."*
* **Build a reusable skill:**
  > *"Create a skill for formatting API specs."*
* **Design multi-agent workflows:**
  > *"Set up a delivery workflow in Claude Code with planning and implementation agents."*

---

### 🔄 Mode 2: Update, Distillation & Migration
Evolve instructions safely; the skill audits past runs, preserves behavior boundaries, and ports across platforms without scope drift.

* **Learn from chat failures (Session Distillation):**
  > *"The agent struggled in our last run—distill the lessons into our skill."*
* **Cross-platform migration:**
  > *"Convert this Copilot agent to Claude Code."*
  > *"Port our skills to work with Codex and Kiro."*
* **Placement & refactoring:**
  > *"Organize our repo rules between agents, skills, and steering."*
  > *"Clean up this skill so it's modular and under single-read limits."*

---

### 🔍 Mode 3: Review & Audit
Ask for an evaluation; the skill benchmarks against domain standards and best practices, runs rubric grading, and checks for contradictions and structural errors automatically.

* **Quality & rubric review:**
  > *"Review our release skill."*
* **Syntax & structural validation:**
  > *"Check our customization files for any errors or broken links."*
* **Contradiction & redundancy check:**
  > *"Check if our agents and skills contradict each other."*

---

## 🧭 Supported Platforms

| Platform | What It Generates |
| :--- | :--- |
| **GitHub Copilot / VS Code** | `.github/agents/*.agent.md`, `.github/skills/*/SKILL.md` |
| **Claude Code** | `.claude/agents/*.md`, `.claude/skills/*/SKILL.md` |
| **OpenAI Codex** | `.codex/agents/*.toml`, `.agents/skills/*/SKILL.md` |
| **Cursor / Antigravity / Kiro** | Standard `SKILL.md` packages |

---

## 🛠️ Advanced Options

<details>
<summary>Click to view interactive install, Git submodule, local scripts, and validator CLI</summary>

### Interactive Agent Picker
If you want to manually select which agents to install to from the interactive CLI menu:

```bash
npx skills add khanhchungoc/craft-agent-skill
```

### Git Submodule (for team repositories)
```bash
git submodule add https://github.com/khanhchungoc/craft-agent-skill.git .github/skills/craft-agent-skill
```

### PowerShell / Bash Script Installers
If you have cloned this repository locally, you can target specific runtimes:
* **Windows (PowerShell):** `.\scripts\install.ps1 -Scope User -Runtime claude` (options: `all`, `copilot`, `claude`, `codex`, `gemini`, `antigravity`, `kiro`)
* **macOS / Linux:** `./scripts/install.sh --scope user --runtime claude` (options: `all`, `copilot`, `claude`, `codex`, `gemini`, `antigravity`, `kiro`)

### Built-in Linter & Validator
Validate any agent or skill folder for syntax errors, platform compatibility, and broken links:
```bash
pip install -r scripts/requirements.txt
python scripts/validate_agent_skill.py --path <your-file-or-folder>
python -m unittest discover -s tests -v
```
</details>

---

## License
MIT
