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
  npx khanhchungoc/craft-agent-skill -a claude-code
  npx khanhchungoc/craft-agent-skill -a copilot
  ```

---

## 💬 How to Use

Once installed, your AI assistant automatically gains this skill. You don't need to memorize any special commands—just talk to your AI agent in chat:

* **Create a new skill:**
  > *"Create a new skill named `format-json` that cleans up and formats JSON files."*
* **Create a custom agent:**
  > *"Build a custom GitHub Copilot agent for code reviews with strict security guidelines."*
* **Review & improve existing skills or agents:**
  > *"Audit our `.claude/skills/` folder and tell me if any instructions or links are broken."*
* **Convert between platforms:**
  > *"Convert this GitHub Copilot agent into a Claude Code subagent."*

The skill handles all platform-specific folder structures, templates, and file conventions automatically.

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
* **Windows (PowerShell):** `.\scripts\install.ps1 -Scope User -Runtime claude-code` (options: `all`, `copilot`, `claude-code`, `codex`, `gemini`, `antigravity`, `kiro`)
* **macOS / Linux:** `./scripts/install.sh --scope user --runtime claude-code` (options: `all`, `copilot`, `claude-code`, `codex`, `gemini`, `antigravity`, `kiro`)

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
