#!/usr/bin/env node

import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const REPO_ROOT = path.resolve(__dirname, '..');
const USER_HOME = os.homedir();

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
\x1b[1mCraft Agent & Skill Installer\x1b[0m

Usage:
  npx khanhchungoc/craft-agent-skill [options]

Options:
  -g, --global              Install globally in user home directory (default)
  -p, --project             Install in current project / workspace directory
  -a, -r, --runtime <name>  Target runtime: copilot, claude, codex, gemini, antigravity, kiro, or all (default: all)
  -m, --mode <symlink|copy> Installation method (auto-detected: copy for npx, symlink for local clones)
  -h, --help                Show this help message

Supported Runtimes:
  • \x1b[36mantigravity\x1b[0m  Antigravity IDE (with slash command support)
  • \x1b[36mcopilot\x1b[0m      GitHub Copilot / VS Code
  • \x1b[36mclaude\x1b[0m      Claude Code CLI
  • \x1b[36mcodex\x1b[0m        OpenAI Codex
  • \x1b[36mgemini\x1b[0m       Gemini CLI
  • \x1b[36mkiro\x1b[0m         Kiro CLI & IDE
`);
}

const destinations = {
  user: {
    copilot: path.join(USER_HOME, '.copilot', 'skills', 'craft-agent-skill'),
    claude: path.join(USER_HOME, '.claude', 'skills', 'craft-agent-skill'),
    codex: path.join(USER_HOME, '.agents', 'skills', 'craft-agent-skill'),
    gemini: path.join(USER_HOME, '.gemini', 'skills', 'craft-agent-skill'),
    antigravity: path.join(USER_HOME, '.gemini', 'config', 'skills', 'craft-agent-skill'),
    kiro: path.join(USER_HOME, '.kiro', 'skills', 'craft-agent-skill')
  },
  project: {
    copilot: path.join(targetPath, '.github', 'skills', 'craft-agent-skill'),
    claude: path.join(targetPath, '.claude', 'skills', 'craft-agent-skill'),
    codex: path.join(targetPath, '.agents', 'skills', 'craft-agent-skill'),
    gemini: path.join(targetPath, '.gemini', 'skills', 'craft-agent-skill'),
    antigravity: path.join(targetPath, '.agents', 'skills', 'craft-agent-skill'),
    kiro: path.join(targetPath, '.kiro', 'skills', 'craft-agent-skill')
  }
};

let normalizedRuntime = runtime;
if (normalizedRuntime === 'github-copilot' || normalizedRuntime === 'vscode-copilot') {
  normalizedRuntime = 'copilot';
} else if (normalizedRuntime === 'claude-code') {
  normalizedRuntime = 'claude';
}

const allRuntimes = ['copilot', 'claude', 'codex', 'gemini', 'antigravity', 'kiro'];
const runtimesToInstall = normalizedRuntime === 'all' ? allRuntimes : [normalizedRuntime];

for (const rt of runtimesToInstall) {
  if (!allRuntimes.includes(rt)) {
    console.error(`\x1b[31mError: Unknown runtime "${rt}". Available: ${allRuntimes.join(', ')}\x1b[0m`);
    process.exit(1);
  }
}

console.log('\x1b[36m==> Installing craft-agent-skill\x1b[0m');
console.log(`    Source:  ${REPO_ROOT}`);
console.log(`    Scope:   ${scope.toUpperCase()}`);
console.log(`    Mode:    ${mode.toUpperCase()}`);
console.log(`    Target:  ${normalizedRuntime.toUpperCase()}`);

const canonicalRepo = path.resolve(REPO_ROOT).toLowerCase();

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

  // Self-deletion check
  if (canonicalDest === canonicalRepo) {
    console.log(`\x1b[33m    Target (${rt}) -> ${dest} is the source repository; skipping to prevent self-deletion.\x1b[0m`);
    continue;
  }

  const parentDir = path.dirname(dest);
  if (!fs.existsSync(parentDir)) {
    fs.mkdirSync(parentDir, { recursive: true });
  }

  if (fs.existsSync(dest)) {
    console.log(`\x1b[33m    Removing existing target at ${dest}\x1b[0m`);
    safeRemove(dest);
  }

  if (mode === 'symlink') {
    const symlinkType = process.platform === 'win32' ? 'junction' : 'dir';
    try {
      fs.symlinkSync(REPO_ROOT, dest, symlinkType);
      console.log(`\x1b[32m    Linked (${rt}) -> ${dest}\x1b[0m`);
    } catch (err) {
      console.log(`\x1b[33m    Symlink failed (${err.message}); falling back to copy.\x1b[0m`);
      copySkillDirectory(REPO_ROOT, dest);
      console.log(`\x1b[32m    Copied (${rt}) -> ${dest}\x1b[0m`);
    }
  } else {
    copySkillDirectory(REPO_ROOT, dest);
    console.log(`\x1b[32m    Copied (${rt}) -> ${dest}\x1b[0m`);
  }
}

console.log('\x1b[36m==> Installation complete!\x1b[0m');

