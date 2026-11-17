#!/usr/bin/env node

/**
 * Bump or sync the skill version across SKILL.md (metadata.version) and package.json.
 *
 * Usage:
 *   node scripts/bump-version.js <major|minor|patch|X.Y.Z> [--dry-run] [--root <dir>]
 *   node scripts/bump-version.js --sync-from-package [--dry-run] [--root <dir>]
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const DEFAULT_ROOT = path.resolve(__dirname, '..');
const SEMVER_RE = /^(\d+)\.(\d+)\.(\d+)$/;

function printHelp() {
  console.log(`Usage:
  node scripts/bump-version.js <major|minor|patch|X.Y.Z> [--dry-run] [--root <dir>]
  node scripts/bump-version.js --sync-from-package [--dry-run] [--root <dir>]

Options:
  --sync-from-package  Copy package.json "version" into SKILL.md metadata.version
  --dry-run            Print the planned change without modifying files
  --root <dir>         Repository root (default: parent of scripts/)
  -h, --help           Show this help message`);
}

function parseSemver(value) {
  const match = String(value).trim().match(SEMVER_RE);
  if (!match) return null;
  return match.slice(1).map((part) => Number.parseInt(part, 10));
}

function computeNextVersion(current, target) {
  const parsed = parseSemver(current);
  if (!parsed) {
    throw new Error(`Current version "${current}" is not valid X.Y.Z semver.`);
  }
  const [major, minor, patch] = parsed;
  if (target === 'major') return `${major + 1}.0.0`;
  if (target === 'minor') return `${major}.${minor + 1}.0`;
  if (target === 'patch') return `${major}.${minor}.${patch + 1}`;
  if (!parseSemver(target)) {
    throw new Error(`Invalid bump target "${target}". Use major, minor, patch, or X.Y.Z.`);
  }
  return target.trim();
}

function readSkillVersion(skillText) {
  const fmMatch = skillText.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!fmMatch) {
    throw new Error('SKILL.md is missing YAML frontmatter.');
  }
  const verMatch = fmMatch[1].match(/^\s*version:\s*["']?([^"'\r\n]+)["']?\s*$/m);
  if (!verMatch) {
    throw new Error('SKILL.md frontmatter is missing a version field.');
  }
  return verMatch[1].trim();
}

function replaceSkillVersion(skillText, nextVersion) {
  const fmMatch = skillText.match(/^(---\r?\n)([\s\S]*?)(\r?\n---)/);
  if (!fmMatch) {
    throw new Error('SKILL.md is missing YAML frontmatter.');
  }
  const lineRe = /^(\s*version:\s*)(["']?)[^"'\r\n]+\2(\s*)$/m;
  if (!lineRe.test(fmMatch[2])) {
    throw new Error('SKILL.md frontmatter is missing a version field.');
  }
  const updatedFrontmatter = fmMatch[2].replace(lineRe, `$1"${nextVersion}"$3`);
  return fmMatch[1] + updatedFrontmatter + fmMatch[3] + skillText.slice(fmMatch[0].length);
}

function main() {
  const args = process.argv.slice(2);
  let target = null;
  let syncFromPackage = false;
  let dryRun = false;
  let root = DEFAULT_ROOT;

  for (let i = 0; i < args.length; i += 1) {
    const arg = args[i];
    if (arg === '--sync-from-package') {
      syncFromPackage = true;
    } else if (arg === '--dry-run') {
      dryRun = true;
    } else if (arg === '--root') {
      if (!args[i + 1]) throw new Error('--root requires a directory path.');
      root = path.resolve(args[++i]);
    } else if (arg === '-h' || arg === '--help') {
      printHelp();
      return;
    } else if (arg.startsWith('-')) {
      throw new Error(`Unknown option: ${arg}`);
    } else if (!target) {
      target = arg;
    } else {
      throw new Error(`Unexpected argument: ${arg}`);
    }
  }

  const skillPath = path.join(root, 'SKILL.md');
  const pkgPath = path.join(root, 'package.json');
  const skillText = fs.readFileSync(skillPath, 'utf8');
  const pkgText = fs.readFileSync(pkgPath, 'utf8');
  const pkg = JSON.parse(pkgText);
  const currentSkillVersion = readSkillVersion(skillText);

  let nextVersion;
  if (syncFromPackage) {
    if (!parseSemver(pkg.version)) {
      throw new Error(`package.json version "${pkg.version}" is not valid X.Y.Z semver.`);
    }
    nextVersion = String(pkg.version).trim();
  } else {
    if (!target) {
      printHelp();
      process.exitCode = 1;
      return;
    }
    nextVersion = computeNextVersion(currentSkillVersion, target);
  }

  const nextSkillText = replaceSkillVersion(skillText, nextVersion);
  const pkgLineRe = /^(\s*"version"\s*:\s*")[^"]*(")/m;
  if (!pkgLineRe.test(pkgText)) {
    throw new Error('package.json is missing a "version" field.');
  }
  const nextPkgText = pkgText.replace(pkgLineRe, `$1${nextVersion}$2`);

  if (!dryRun) {
    if (nextSkillText !== skillText) fs.writeFileSync(skillPath, nextSkillText, 'utf8');
    if (nextPkgText !== pkgText) fs.writeFileSync(pkgPath, nextPkgText, 'utf8');
  }

  const verb = dryRun ? 'Would set' : 'Updated';
  console.log(`${verb} craft-agent-skill: ${currentSkillVersion} -> ${nextVersion}`);
}

try {
  main();
} catch (err) {
  console.error(`Error: ${err.message}`);
  process.exit(1);
}
