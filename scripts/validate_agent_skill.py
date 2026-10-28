#!/usr/bin/env python3
"""Partially lint native agent/skill files for the selected runtime.

Exit codes: 0 = no errors (warnings allowed), 1 = validation errors,
2 = dependency or input failure. Use --path for a file or a package folder.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote

try:
    import tomllib
except ImportError:
    try:
        import tomli as tomllib
    except ImportError:
        tomllib = None

try:
    import yaml
except ImportError:
    yaml = None

RUNTIMES = ("auto", "universal", "github-copilot", "vscode-copilot", "claude-code", "codex", "kiro")
AGENT_ROOTS = {".github": "github-copilot", ".claude": "claude-code",
               ".codex": "codex", ".kiro": "kiro"}
SKILL_ROOTS = (".github", ".claude", ".agents", ".kiro")


def runtime_for(path: Path, selected: str = "auto") -> str:
    if selected != "auto":
        return "github-copilot" if selected == "vscode-copilot" else selected
    parts = path.parts
    # Authoring assets live under assets/runtimes but target their named native profile.
    for index, part in enumerate(parts[:-1]):
        if part == "runtimes" and parts[index + 1] in RUNTIMES:
            target = parts[index + 1]
            return "github-copilot" if target == "vscode-copilot" else target
    for root, runtime in AGENT_ROOTS.items():
        if root in parts:
            return runtime
    if ".agents" in parts:
        return "codex"
    return "github-copilot" if path.name.endswith(".agent.md") else "universal"


def artifact_kind(path: Path, runtime: str) -> str:
    if path.name in ("SKILL.md", "skill.template.md"):
        return "skill"
    native_agent = any(path.parts[i] in AGENT_ROOTS and path.parts[i + 1] == "agents"
                       for i in range(len(path.parts) - 1))
    native_template = "runtimes" in path.parts and path.name.startswith("agent.template.")
    if native_agent or native_template or path.name.endswith(".agent.md"):
        return "agent"
    return "resource"


if yaml is not None:
    class DuplicateKeyError(yaml.constructor.ConstructorError):
        """Reject silent replacement of an explicitly repeated YAML key."""

    class UniqueSafeLoader(yaml.SafeLoader):
        def construct_object(self, node, deep=False):
            try:
                return super().construct_object(node, deep=deep)
            except (ValueError, TypeError, OverflowError) as exc:
                # PyYAML's scalar constructors can raise ordinary conversion
                # errors (for example an invalid implicit timestamp). Preserve
                # the failing node's source mark for the per-file diagnostic.
                raise yaml.constructor.ConstructorError(
                    None, None, f"Invalid YAML value: {exc}", node.start_mark
                ) from exc

        def construct_mapping(self, node, deep=False):
            seen = set()
            for key_node, _ in node.value:
                if key_node.tag == "tag:yaml.org,2002:merge":
                    continue
                key = self.construct_object(key_node, deep=deep)
                try:
                    duplicate = key in seen
                    seen.add(key)
                except TypeError as exc:
                    raise yaml.constructor.ConstructorError(
                        None, None, "Unhashable YAML mapping key", key_node.start_mark
                    ) from exc
                if duplicate:
                    raise DuplicateKeyError(
                        None, None, f"Duplicate YAML key: {key!r}", key_node.start_mark
                    )
            return super().construct_mapping(node, deep=deep)


def finding(path: Path, line: int, rule: str, message: str,
            severity: str = "error") -> dict:
    return {"file": str(path), "line": line, "severity": severity,
            "rule": rule, "message": message}


def frontmatter_findings(path: Path, content: str, runtime: str = "auto",
                         kind: str | None = None, template: bool = False) -> list[dict]:
    runtime = runtime_for(path, runtime)
    kind = kind or artifact_kind(path, runtime)
    match = re.match(r"\A---[ \t]*\n(.*?)\n---[ \t]*(?:\n|\Z)", content, re.S)
    if not match:
        return [finding(path, 1, "frontmatter-missing",
                        "Expected a YAML frontmatter block delimited by ---.")]
    if yaml is None:
        return [finding(path, 1, "yaml-dependency", "Install PyYAML from scripts/requirements.txt.")]
    frontmatter = match.group(1)
    try:
        data = yaml.load(frontmatter, Loader=UniqueSafeLoader)
    except yaml.YAMLError as exc:
        mark = getattr(exc, "problem_mark", None)
        rule = "frontmatter-duplicate-key" if isinstance(exc, DuplicateKeyError) else "frontmatter-yaml"
        return [finding(path, mark.line + 2 if mark else 1, rule,
                        getattr(exc, "problem", None) or str(exc))]
    if not isinstance(data, dict):
        return [finding(path, 2, "frontmatter-mapping", "Frontmatter must be a YAML mapping.")]
    node = yaml.compose(frontmatter, Loader=yaml.SafeLoader)
    key_lines = {key.value: key.start_mark.line + 2 for key, _ in node.value}
    return metadata_findings(path, data, key_lines, runtime, kind, template,
                             content[match.end():])


def metadata_findings(path: Path, data: dict, key_lines: dict, runtime: str,
                      kind: str, template: bool = False, body: str = "") -> list[dict]:
    issues = []
    for key in ("name", "description"):
        value = data.get(key)
        if not isinstance(value, str) or not value.strip():
            issues.append(finding(path, key_lines.get(key, 1), f"frontmatter-{key}",
                                  f"{key!r} must be a non-empty string."))
        elif not template and re.fullmatch(r"\s*<[^>]+>\.?\s*", value):
            issues.append(finding(path, key_lines.get(key, 1), "scaffold-placeholder",
                                  f"Replace the scaffold placeholder in {key!r}."))
    name = data.get("name")
    if kind == "skill" and not template and isinstance(name, str) and name.strip():
        if len(name) > 64 or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name):
            issues.append(finding(path, key_lines.get("name", 1), "skill-name",
                                  "Skill names use lowercase letters/digits and single hyphens, up to 64 characters."))
    description = data.get("description")
    if isinstance(description, str) and len(description.strip()) > 220:
        issues.append(finding(path, key_lines.get("description", 1), "description-length",
                              "Description exceeds the local 220-character brevity guideline; this is not a platform limit.",
                              "warning"))
    if kind == "agent":
        if runtime in ("github-copilot", "vscode-copilot") and "skills" in data:
            issues.append(finding(path, key_lines.get("skills", 1), "unsupported-frontmatter",
                                  "Link procedural skills in the agent body instead of a 'skills' field."))
        tools = data.get("tools", [])
        if isinstance(tools, str) and runtime in ("claude-code", "github-copilot", "vscode-copilot"):
            tools = [part.strip() for part in tools.split(",")]
        if runtime == "codex" and "tools" in data:
            issues.append(finding(path, key_lines.get("tools", 1), "runtime-field",
                                  "Codex custom agents inherit tools; do not use a Copilot/Claude tools field."))
        elif not isinstance(tools, list) or any(not isinstance(tool, str) or not tool.strip() for tool in tools):
            issues.append(finding(path, key_lines.get("tools", 1), "frontmatter-tools",
                                  "Agent tools must be a list of non-empty strings."))
        elif runtime in ("github-copilot", "vscode-copilot") and "vscode" in tools:
            issues.append(finding(path, key_lines.get("tools", 1), "broad-tool-permission",
                                  "Use the required vscode tool names instead of the broad 'vscode' bundle."))
        if runtime == "claude-code" and "skills" in data:
            skills = data["skills"]
            if not isinstance(skills, list) or any(not isinstance(item, str) or not item.strip() for item in skills):
                issues.append(finding(path, key_lines.get("skills", 1), "frontmatter-skills",
                                      "Claude agent skills preload must be a list of skill names."))
        if runtime == "codex":
            instructions = data.get("developer_instructions")
            if not isinstance(instructions, str) or not instructions.strip():
                issues.append(finding(path, key_lines.get("developer_instructions", 1), "agent-instructions",
                                      "Codex agents require non-empty developer_instructions."))
        if runtime == "kiro" and "skills" in data:
            issues.append(finding(path, key_lines.get("skills", 1), "runtime-field",
                                  "Kiro skill bindings use resources with skill://, not a Claude skills field."))
        if runtime == "kiro":
            prompt = data.get("prompt", body)
            if not isinstance(prompt, str) or not prompt.strip():
                issues.append(finding(path, key_lines.get("prompt", 1), "agent-instructions",
                                      "Supply Kiro prompt instructions or a supported prompt file URI."))
            if "resources" in data and not isinstance(data["resources"], list):
                issues.append(finding(path, key_lines.get("resources", 1), "agent-resources",
                                      "Kiro resources must be a list of native resource entries."))
            if "permissions" in data and not isinstance(data["permissions"], dict):
                issues.append(finding(path, key_lines.get("permissions", 1), "agent-permissions",
                                      "Kiro permissions must be a mapping; verify native rules in the target runtime."))
    return issues


def structured_findings(path: Path, content: str, runtime: str, kind: str,
                        template: bool) -> list[dict]:
    try:
        if path.suffix == ".toml":
            if tomllib is None:
                return [finding(path, 1, "toml-dependency", "Python 3.10 requires the declared tomli dependency.")]
            data = tomllib.loads(content)
        elif path.suffix == ".json":
            def unique_object(pairs):
                result = {}
                for key, value in pairs:
                    if key in result:
                        raise ValueError(f"Duplicate JSON key: {key}")
                    result[key] = value
                return result
            data = json.loads(content, object_pairs_hook=unique_object)
        else:
            data = yaml.load(content, Loader=UniqueSafeLoader)
    except (ValueError, TypeError, OverflowError, yaml.YAMLError) as exc:
        mark = getattr(exc, "problem_mark", None)
        line = mark.line + 1 if mark else getattr(exc, "lineno", None)
        if not line:
            match = re.search(r"line (\d+)", str(exc))
            line = int(match.group(1)) if match else 1
        return [finding(path, line, "structured-syntax", str(exc))]
    if not isinstance(data, dict):
        return [finding(path, 1, "structured-mapping", "Configuration must be an object/mapping.")]
    if kind != "agent":
        return []
    if (runtime == "codex" and path.suffix != ".toml") or (runtime != "codex" and path.suffix == ".toml"):
        return [finding(path, 1, "runtime-format", "Agent format does not match the selected runtime.")]
    if runtime == "kiro" and path.suffix != ".json":
        return [finding(path, 1, "runtime-format", "Structured Kiro agent profiles use JSON; Markdown profiles use .md frontmatter.")]
    if runtime not in ("codex", "kiro"):
        return [finding(path, 1, "runtime-format", "This runtime's agent wrapper uses Markdown with YAML frontmatter.")]
    keys = {}
    for key in data:
        for number, line in enumerate(content.splitlines(), 1):
            if re.match(r'\s*["\']?' + re.escape(str(key)) + r'["\']?\s*[:=]', line):
                keys[key] = number
                break
    return metadata_findings(path, data, keys, runtime, kind, template)


def markdown_findings(path: Path, content: str) -> list[dict]:
    issues = []
    fence = None
    for number, line in enumerate(content.splitlines(), 1):
        marker = re.match(r"^\s{0,3}(`{3,}|~{3,})(.*)$", line)
        if marker:
            run, suffix = marker.groups()
            if fence is None:
                fence = run
            elif run[0] == fence[0] and len(run) >= len(fence) and not suffix.strip():
                fence = None
            continue
        if fence:
            continue
        # Inline code is an example, not a live Markdown link or heading.
        line = re.sub(r"(`+).*?\1", "", line)
        if path.name == "SKILL.md" and re.match(r"^##\s+When to Use\b", line):
            issues.append(finding(path, number, "ssot-trigger",
                                  "Keep skill selection criteria in the frontmatter description."))
        for match in re.finditer(r"!?\[[^\]]*\]\((<[^>\n]+>|[^)\n]+)\)", line):
            target = match.group(1).strip()
            if target.startswith("<") and target.endswith(">"):
                target = target[1:-1]
            else:
                target = re.split(r'\s+["\']', target, maxsplit=1)[0]
            if target.startswith("#"):
                continue
            windows_path = re.match(r"^[a-zA-Z]:[\\/]", target)
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) and not windows_path:
                continue
            target = unquote(target.split("#", 1)[0])
            if not target:
                continue
            try:
                resolved = path.parent / target
                if not resolved.exists():
                    issues.append(finding(path, number, "broken-link",
                                          f"Relative Markdown target does not exist: {target}"))
            except (OSError, ValueError) as exc:
                issues.append(finding(path, number, "broken-link", f"Invalid Markdown target: {exc}"))
    return issues


def validate_file(path: Path, runtime: str = "auto", kind: str = "auto") -> list[dict]:
    try:
        content = path.read_text(encoding="utf-8-sig")
    except UnicodeError:
        return [finding(path, 1, "encoding-integrity", "File is not valid UTF-8.")]
    except OSError as exc:
        return [finding(path, 1, "file-read", str(exc))]
    issues = [finding(path, number, "encoding-integrity", "Unicode replacement character found.")
              for number, line in enumerate(content.splitlines(), 1) if "\ufffd" in line]
    profile = runtime_for(path, runtime)
    kind = artifact_kind(path, profile) if kind == "auto" else kind
    template = ".template." in path.name
    if kind == "skill" and path.suffix != ".md":
        return issues + [finding(path, 1, "runtime-format", "Skill entrypoints use Markdown with YAML frontmatter.")]
    if path.suffix in (".json", ".toml", ".yaml", ".yml"):
        issues.extend(structured_findings(path, content, profile, kind, template))
    else:
        if kind in ("agent", "skill"):
            if kind == "agent" and profile == "codex":
                issues.append(finding(path, 1, "runtime-format", "Codex custom agents use TOML, not Markdown frontmatter."))
            else:
                issues.extend(frontmatter_findings(path, content, profile, kind, template))
        issues.extend(markdown_findings(path, content))
    return issues


def find_root(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if any((candidate / marker).exists() for marker in (".git", ".agent-artifacts", "package.json")):
            return candidate
    return start


def collect_files(root: Path, target: str | None) -> list[Path]:
    if target:
        path = Path(target)
        if not path.is_absolute():
            path = root / path
        if not path.exists():
            raise ValueError(f"Target does not exist: {path}")
        if path.is_file():
            if path.suffix.lower() not in (".md", ".json", ".toml", ".yaml", ".yml"):
                raise ValueError("Select Markdown, JSON, TOML, YAML, or a customization package folder.")
            files = [path]
        else:
            files = sorted(item for item in path.rglob("*") if item.is_file()
                           and item.suffix.lower() in (".md", ".json", ".toml", ".yaml", ".yml"))
    else:
        files = []
        for directory, profile in AGENT_ROOTS.items():
            suffixes = {"codex": (".toml",), "kiro": (".json", ".md")}.get(profile, (".md",))
            files.extend(item for item in (root / directory / "agents").rglob("*")
                         if item.is_file() and item.suffix in suffixes)
        for directory in SKILL_ROOTS:
            files.extend((root / directory / "skills").rglob("SKILL.md"))
        files = sorted(set(files))
    if not files:
        raise ValueError("No agent, skill, or supporting Markdown files found in the selected scope.")
    return files


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--runtime", choices=RUNTIMES, default="auto",
                        help="Native profile; auto uses paths (not the editor or model provider)")
    parser.add_argument("--kind", choices=("auto", "agent", "skill", "resource"), default="auto",
                        help="Artifact role; a relocated single file with an explicit native runtime defaults to agent. Use resource for syntax/link-only checks.")
    parser.add_argument("--root", "-root", "-Root", "-r", help="Workspace root (default: discover from current directory)")
    parser.add_argument("--path", "-path", "-Path", "-p", help="Customization file or package folder, relative to root or absolute")
    parser.add_argument("--json", "-json", "-Json", action="store_true", help="Machine-readable summary and findings")
    parser.add_argument("--terse", "-terse", "-Terse", action="store_true", help="Omit the success line; keep findings and error totals")
    args = parser.parse_args(argv)
    root = Path(args.root).resolve() if args.root else find_root(Path.cwd())
    files = []
    status = 0
    if yaml is None:
        issues = [finding(Path(__file__), 1, "yaml-dependency",
                          "PyYAML is required. Install the dependency in scripts/requirements.txt.")]
        status = 2
    else:
        try:
            if not root.is_dir():
                raise ValueError(f"Workspace root is not a directory: {root}")
            files = collect_files(root, args.path)
        except (OSError, ValueError) as exc:
            issues = [finding(root, 1, "input-path", str(exc))]
            status = 2
        else:
            # File-content failures belong to the affected file, not the scope
            # selector. Keep diagnostics from every file in the selected scope.
            kind = args.kind
            if (kind == "auto" and args.path and (root / args.path).is_file()
                    and args.runtime not in ("auto", "universal")):
                detected = artifact_kind(files[0], args.runtime)
                kind = "agent" if detected == "resource" else detected
            issues = [issue for path in files for issue in validate_file(path, args.runtime, kind)]
            if any(issue["rule"] == "toml-dependency" for issue in issues):
                status = 2
    for issue in issues:
        try:
            issue["file"] = Path(issue["file"]).relative_to(root).as_posix()
        except ValueError:
            pass
    errors = sum(issue["severity"] == "error" for issue in issues)
    warnings = sum(issue["severity"] == "warning" for issue in issues)
    result = {"total_files": len(files), "errors": errors, "warnings": warnings, "findings": issues}
    if args.json:
        print(json.dumps(result, ensure_ascii=True, indent=2))
    else:
        for issue in issues:
            print(f"{issue['file']}:L{issue['line']}: [{issue['severity'].upper()}] [{issue['rule']}] {issue['message']}")
        if issues:
            print(f"TOTALS: {errors} errors, {warnings} warnings across {len(files)} files.")
        elif not args.terse:
            print(f"VALIDATION PASSED: {len(files)} files, 0 errors, 0 warnings (structural checks only).")
    return status or (1 if errors else 0)


if __name__ == "__main__":
    raise SystemExit(main())
