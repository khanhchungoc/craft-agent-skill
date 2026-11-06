#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REPO_ROOT = path.resolve(__dirname, '..');
const USER_HOME = os.homedir();

// High-contrast ANSI colors
const c = {
  reset: '\x1b[0m',
  bold: '\x1b[1m',
  dim: '\x1b[2m',
  cyan: '\x1b[96m',          // bright cyan (high visibility)
  green: '\x1b[92m',         // bright green
  yellow: '\x1b[93m',        // bright yellow
  red: '\x1b[91m',           // bright red
  gray: '\x1b[90m',          // muted gray
  white: '\x1b[97m',         // bright white
  border: '\x1b[38;5;39m'    // vivid sky blue
};

const args = process.argv.slice(2);
let scope = 'user';
let runtime = 'all';
let mode = 'symlink';
let targetPath = process.cwd();

// Detect if running from a temporary npx cache
const isNpxCache = REPO_ROOT.includes('_npx') || 
                   REPO_ROOT.includes('npm-cache') || 
                   REPO_ROOT.includes('.npm') || 
                   REPO_ROOT.toLowerCase().includes('temp') || 
                   REPO_ROOT.includes('/tmp/');

if (isNpxCache) {
  mode = 'copy';
}

for (let i = 0; i < args.length; i++) {
  const arg = args[i];
  if (arg === '-g' || arg === '--global') {
    scope = 'user';
  } else if (arg === '-p' || arg === '--project') {
    scope = 'project';
  } else if (arg === '--scope' || arg === '-s') {
    const val = args[++i]?.toLowerCase();
    scope = val === 'project' ? 'project' : 'user';
  } else if (arg === '--runtime' || arg === '-r' || arg === '-a' || arg === '--agent') {
    runtime = args[++i]?.toLowerCase() || 'all';
  } else if (arg === '--mode' || arg === '-m') {
    mode = args[++i]?.toLowerCase() === 'copy' ? 'copy' : 'symlink';
  } else if (arg === '--copy') {
    mode = 'copy';
  } else if (arg === '--symlink') {
    mode = 'symlink';
  } else if (arg === '--target-path' || arg === '-t') {
    targetPath = path.resolve(args[++i] || process.cwd());
  } else if (arg === '--help' || arg === '-h') {
    printHelp();
    process.exit(0);
  }
}

function printHelp() {
  console.log(`
${c.cyan}${c.bold}Skill Craft Installer${c.reset}
${c.dim}Universal AI skill that teaches AI coding assistants to build, refine, and audit custom agents and skills.${c.reset}

${c.bold}Usage:${c.reset}
  npx khanhchungoc/craft-agent-skill [options]

${c.bold}Options:${c.reset}
  -g, --global              Install globally in user home directory (default)
  -p, --project             Install in current project / workspace directory
  -a, -r, --runtime <name>  Target runtime: copilot, claude, codex, gemini, antigravity, kiro, or all (default: all)
  -m, --mode <symlink|copy> Installation method (auto-detected: copy for npx, symlink for local clones)
  -h, --help                Show this help message

${c.bold}Supported Runtimes:${c.reset}
  • ${c.cyan}antigravity${c.reset}  Antigravity IDE (with slash command support)
  • ${c.cyan}copilot${c.reset}      GitHub Copilot / VS Code
  • ${c.cyan}claude${c.reset}       Claude Code CLI
  • ${c.cyan}codex${c.reset}        OpenAI Codex
  • ${c.cyan}gemini${c.reset}       Gemini CLI
  • ${c.cyan}kiro${c.reset}         Kiro CLI & IDE
`);
}

const destinations = {
  user: {
    antigravity: path.join(USER_HOME, '.gemini', 'config', 'skills', 'craft-agent-skill'),
    claude: path.join(USER_HOME, '.claude', 'skills', 'craft-agent-skill'),
    copilot: path.join(USER_HOME, '.copilot', 'skills', 'craft-agent-skill'),
    codex: path.join(USER_HOME, '.agents', 'skills', 'craft-agent-skill'),
    gemini: path.join(USER_HOME, '.gemini', 'skills', 'craft-agent-skill'),
    kiro: path.join(USER_HOME, '.kiro', 'skills', 'craft-agent-skill')
  },
  project: {
    antigravity: path.join(targetPath, '.agents', 'skills', 'craft-agent-skill'),
    claude: path.join(targetPath, '.claude', 'skills', 'craft-agent-skill'),
    copilot: path.join(targetPath, '.github', 'skills', 'craft-agent-skill'),
    codex: path.join(targetPath, '.agents', 'skills', 'craft-agent-skill'),
    gemini: path.join(targetPath, '.gemini', 'skills', 'craft-agent-skill'),
    kiro: path.join(targetPath, '.kiro', 'skills', 'craft-agent-skill')
  }
};

const runtimeLabels = {
  antigravity: 'Antigravity IDE',
  claude: 'Claude Code',
  copilot: 'GitHub Copilot',
  codex: 'OpenAI Codex',
  gemini: 'Gemini CLI',
  kiro: 'Kiro IDE'
};

let normalizedRuntime = runtime;
if (normalizedRuntime === 'github-copilot' || normalizedRuntime === 'vscode-copilot') {
  normalizedRuntime = 'copilot';
} else if (normalizedRuntime === 'claude-code') {
  normalizedRuntime = 'claude';
}

const allRuntimes = ['antigravity', 'claude', 'copilot', 'codex', 'gemini', 'kiro'];
const runtimesToInstall = normalizedRuntime === 'all' ? allRuntimes : [normalizedRuntime];

for (const rt of runtimesToInstall) {
  if (!allRuntimes.includes(rt)) {
    console.error(`\n${c.red}✖ Error: Unknown runtime "${rt}". Available: ${allRuntimes.join(', ')}${c.reset}\n`);
    process.exit(1);
  }
}

// Ultra High-Contrast Solid 3D Block Banner for "SKILL CRAFT"
const asciiArt = [
  '███████╗██╗  ██╗██╗██╗     ██╗      ██████╗██████╗  █████╗ ███████╗████████╗',
  '██╔════╝██║ ██╔╝██║██║     ██║     ██╔════╝██╔══██╗██╔══██╗██╔════╝╚══██╔══╝',
  '███████╗█████╔╝ ██║██║     ██║     ██║     ██████╔╝███████║█████╗     ██║   ',
  '╚════██║██╔═██╗ ██║██║     ██║     ██║     ██╔══██╗██╔══██║██╔══╝     ██║   ',
  '███████║██║  ██╗██║███████╗███████╗╚██████╗██║  ██║██║  ██║██║        ██║   ',
  '╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝        ╚═╝   '
];

console.log('');
console.log(`${c.cyan}${c.bold}${asciiArt.join('\n')}${c.reset}`);
console.log(`${c.dim}   Universal AI Skill Builder for Coding Assistants • v1.0.0${c.reset}\n`);

// Configuration Section
console.log(`${c.cyan} ⚙  CONFIGURATION${c.reset}`);
console.log(`    ${c.gray}•${c.reset} Scope:    ${c.white}${scope === 'user' ? 'Global' : 'Project'}${c.reset} ${c.dim}(${scope === 'user' ? 'User Home' : targetPath})${c.reset}`);
console.log(`    ${c.gray}•${c.reset} Mode:     ${c.white}${mode === 'symlink' ? 'Symlink' : 'Copy'}${c.reset} ${c.dim}(${mode === 'symlink' ? 'auto-updating junction' : 'standalone copy'})${c.reset}`);
console.log(`    ${c.gray}•${c.reset} Target:   ${c.white}${normalizedRuntime === 'all' ? 'All Runtimes' : (runtimeLabels[normalizedRuntime] || normalizedRuntime)}${c.reset} ${c.dim}(${runtimesToInstall.length} runtime${runtimesToInstall.length > 1 ? 's' : ''})${c.reset}\n`);

console.log(`${c.cyan} ✦  INSTALLING RUNTIMES${c.reset}`);

const canonicalRepo = path.resolve(REPO_ROOT).toLowerCase();

function formatDisplayPath(targetDest) {
  if (targetDest.startsWith(USER_HOME)) {
    return `~${targetDest.slice(USER_HOME.length)}`;
  }
  return targetDest;
}

function copySkillDirectory(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  const entries = fs.readdirSync(src, { withFileTypes: true });

  const ignored = new Set(['.git', 'node_modules', '.github', 'agent', '.agents', '.claude', 'skills-lock.json']);

  for (const entry of entries) {
    if (ignored.has(entry.name)) continue;
    const srcPath = path.join(src, entry.name);
    const destPath = path.join(dest, entry.name);

    if (entry.isDirectory()) {
      copySkillDirectory(srcPath, destPath);
    } else {
      fs.copyFileSync(srcPath, destPath);
    }
  }
}

function safeRemove(dest) {
  try {
    const stat = fs.lstatSync(dest);
    if (stat.isSymbolicLink() || (process.platform === 'win32' && stat.isDirectory())) {
      fs.rmSync(dest, { recursive: true, force: true });
    } else {
      fs.rmSync(dest, { recursive: true, force: true });
    }
  } catch {
    if (fs.existsSync(dest)) {
      fs.rmSync(dest, { recursive: true, force: true });
    }
  }
}

for (const rt of runtimesToInstall) {
  const dest = destinations[scope][rt];
  const canonicalDest = path.resolve(dest).toLowerCase();
  const label = (runtimeLabels[rt] || rt).padEnd(16, ' ');
  const displayDest = formatDisplayPath(dest);

  // Self-deletion check
  if (canonicalDest === canonicalRepo) {
    console.log(`    ${c.yellow}ℹ${c.reset}  ${c.white}${label}${c.reset} ${c.yellow}Skipped (source repo)${c.reset}`);
    continue;
  }

  const parentDir = path.dirname(dest);
  if (!fs.existsSync(parentDir)) {
    fs.mkdirSync(parentDir, { recursive: true });
  }

  if (fs.existsSync(dest)) {
    safeRemove(dest);
  }

  if (mode === 'symlink') {
    const symlinkType = process.platform === 'win32' ? 'junction' : 'dir';
    try {
      fs.symlinkSync(REPO_ROOT, dest, symlinkType);
      console.log(`    ${c.green}✔${c.reset}  ${c.white}${label}${c.reset} ${c.gray}→${c.reset} ${c.dim}${displayDest}${c.reset}`);
    } catch (err) {
      copySkillDirectory(REPO_ROOT, dest);
      console.log(`    ${c.green}✔${c.reset}  ${c.white}${label}${c.reset} ${c.gray}→${c.reset} ${c.dim}${displayDest}${c.reset} ${c.yellow}(copy fallback)${c.reset}`);
    }
  } else {
    copySkillDirectory(REPO_ROOT, dest);
    console.log(`    ${c.green}✔${c.reset}  ${c.white}${label}${c.reset} ${c.gray}→${c.reset} ${c.dim}${displayDest}${c.reset}`);
  }
}

// Compute display width accounting for emojis and wide symbols
function visualLength(str) {
  const stripped = str.replace(/\x1b\[[0-9;]*m/g, '');
  let width = 0;
  for (const ch of stripped) {
    const cp = ch.codePointAt(0);
    if ((cp >= 0x1F300 && cp <= 0x1FAFF) || (cp >= 0x2600 && cp <= 0x27BF)) {
      width += 2;
    } else {
      width += 1;
    }
  }
  return width;
}

const boxWidth = 72;
function boxLine(content) {
  const vLen = visualLength(content);
  const pad = Math.max(0, boxWidth - 4 - vLen);
  return `│  ${content}${' '.repeat(pad)}│`;
}

const topBorder    = `╭${'─'.repeat(boxWidth - 2)}╮`;
const bottomBorder = `╰${'─'.repeat(boxWidth - 2)}╯`;
const emptyLine    = `│${' '.repeat(boxWidth - 2)}│`;

console.log('');
console.log(`${c.border}${topBorder}${c.reset}`);
console.log(`${c.border}${boxLine(`${c.green}✨ Installation Successful!${c.reset}`)}${c.reset}`);
console.log(`${c.border}${emptyLine}${c.reset}`);
console.log(`${c.border}${boxLine(`${c.bold}${c.white}How to use:${c.reset}`)}${c.reset}`);
console.log(`${c.border}${boxLine(`  Type ${c.cyan}/craft-agent-skill${c.reset}${c.white} in your AI assistant chat${c.reset}`)}${c.reset}`);
console.log(`${c.border}${emptyLine}${c.reset}`);
console.log(`${c.border}${boxLine(`${c.dim}Repository: https://github.com/khanhchungoc/craft-agent-skill${c.reset}`)}${c.reset}`);
console.log(`${c.border}${bottomBorder}${c.reset}\n`);
