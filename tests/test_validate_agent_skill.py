"""Regression checks for structural validation, not agent-quality benchmarks."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.dont_write_bytecode = True
SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_agent_skill.py"
spec = importlib.util.spec_from_file_location("skill_validator", SCRIPT)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.workspace = Path.cwd().resolve()
        self.temporary = tempfile.TemporaryDirectory(prefix=".skill-validator-test-", dir=self.workspace)
        self.root = Path(self.temporary.name).resolve()
        self.assertTrue(self.root.is_relative_to(self.workspace))

    def tearDown(self):
        # Only remove the generated test directory inside the verified workspace.
        self.assertTrue(self.root.is_relative_to(self.workspace))
        self.assertTrue(self.root.name.startswith(".skill-validator-test-"))
        self.temporary.cleanup()

    def write(self, relative="sample/SKILL.md", frontmatter="name: sample\ndescription: Test a sample workflow.", body="# Sample\n"):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"---\n{frontmatter}\n---\n{body}", encoding="utf-8")
        return path

    def rules(self, path):
        return {issue["rule"] for issue in validator.validate_file(path)}

    def cli(self, *args):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            status = validator.main(["--root", str(self.root), "--json", *args])
        return status, json.loads(output.getvalue())

    def test_rejects_unterminated_yaml_quote_with_file_line(self):
        path = self.write(frontmatter='name: sample\ndescription: "unclosed quote')
        issues = validator.validate_file(path)
        self.assertEqual(issues[0]["rule"], "frontmatter-yaml")
        self.assertGreaterEqual(issues[0]["line"], 3)

    def test_rejects_duplicate_keys_at_root_and_nested(self):
        for extra in ("description: Replaced silently.", "metadata:\n  owner: one\n  owner: two"):
            with self.subTest(extra=extra):
                path = self.write(frontmatter="name: sample\ndescription: Original.\n" + extra)
                self.assertIn("frontmatter-duplicate-key", self.rules(path))

    def test_yaml_conversion_failure_keeps_file_location_and_other_findings(self):
        self.write(".github/agents/a.agent.md", "name: first\ndescription: First agent.\nskills: [forbidden]")
        self.write(".github/agents/c.agent.md", "name: last\ndescription: Last agent.\ntools: [vscode]")
        for value in ("2026-13-27", "2026-02-30", "2026-10-27T25:00:00Z"):
            with self.subTest(value=value):
                self.write(".github/agents/b.agent.md", f"name: middle\ndescription: Middle agent.\nmetadata:\n  date: {value}")
                status, result = self.cli()
                self.assertEqual(status, 1)
                self.assertEqual((result["total_files"], result["errors"]), (3, 3))
                findings = {issue["file"]: issue for issue in result["findings"]}
                self.assertEqual(findings[".github/agents/a.agent.md"]["rule"], "unsupported-frontmatter")
                self.assertEqual(findings[".github/agents/c.agent.md"]["rule"], "broad-tool-permission")
                bad_value = findings[".github/agents/b.agent.md"]
                self.assertEqual((bad_value["rule"], bad_value["line"]), ("frontmatter-yaml", 5))
                self.assertIn("Invalid YAML value", bad_value["message"])

    def test_valid_timestamp_and_quoted_invalid_date_remain_accepted(self):
        for value in ("2026-10-27", '"2026-13-27"'):
            with self.subTest(value=value):
                path = self.write(frontmatter=f"name: sample\ndescription: Sample workflow.\nmetadata:\n  date: {value}")
                self.assertEqual(self.rules(path), set())

    def test_accepts_folded_description_and_optional_metadata(self):
        path = self.write(frontmatter="name: sample\ndescription: >-\n  Handle reports\n  with audited totals.\nmetadata:\n  owner: team\nallowed-tools: Read")
        self.assertEqual(self.rules(path), set())

    def test_rejects_empty_and_wrong_type_required_values(self):
        for value in ('""', "null", "[]", "42"):
            with self.subTest(value=value):
                path = self.write(frontmatter=f"name: sample\ndescription: {value}")
                self.assertIn("frontmatter-description", self.rules(path))

    def test_requires_mapping_frontmatter(self):
        self.assertIn("frontmatter-mapping", self.rules(self.write(frontmatter="- sample\n- description")))

    def test_distinguishes_real_filename_patterns_from_scaffold_descriptions(self):
        path = self.write(frontmatter='name: sample\ndescription: "Write api-<slug>.md for a confirmed contract."')
        self.assertEqual(self.rules(path), set())
        path = self.write(frontmatter='name: sample\ndescription: "<Capability and activation context>."')
        self.assertIn("scaffold-placeholder", self.rules(path))

    def test_yaml_merge_overrides_are_valid_and_inherited_rules_are_checked(self):
        path = self.write(frontmatter='metadata: &defaults\n  name: sample\n  description: Original.\n<<: *defaults\ndescription: Updated.')
        self.assertEqual(self.rules(path), set())
        path = self.write("sample.agent.md", 'metadata: &defaults\n  name: sample\n  description: Original.\n  skills: [sample]\n<<: *defaults')
        self.assertIn("unsupported-frontmatter", self.rules(path))

    def test_checks_quoted_inline_tools_without_rejecting_scoped_names(self):
        path = self.write("sample.agent.md", 'name: sample\ndescription: A scoped agent.\ntools: ["vscode", "read"]')
        self.assertIn("broad-tool-permission", self.rules(path))
        path = self.write("sample.agent.md", 'name: sample\ndescription: A scoped agent.\ntools: ["vscode/askQuestions", "read"]')
        self.assertEqual(self.rules(path), set())

    def test_rejects_invalid_tool_shape_and_agent_skills_key(self):
        path = self.write("sample.agent.md", 'name: sample\ndescription: A sample agent.\ntools: 42\nskills: [sample]')
        self.assertTrue({"frontmatter-tools", "unsupported-frontmatter"}.issubset(self.rules(path)))

    def test_description_brevity_is_warning_not_failure(self):
        self.write(frontmatter="name: sample\ndescription: " + "a" * 240)
        status, result = self.cli("--path", "sample/SKILL.md")
        self.assertEqual(status, 0)
        self.assertEqual((result["errors"], result["warnings"]), (0, 1))

    def test_rejects_invalid_utf8_and_replacement_character(self):
        path = self.write()
        path.write_bytes(b"\xff\xfe")
        self.assertIn("encoding-integrity", self.rules(path))
        path = self.write(body="A corrupted character: \ufffd\n")
        self.assertIn("encoding-integrity", self.rules(path))

    def test_resolves_percent_encoded_and_angle_bracket_links(self):
        path = self.write(body='[one](notes%20and%20figures.md#section)\n[two](<notes and figures.md>)\n[web](https://example.com)\n')
        (path.parent / "notes and figures.md").write_text("# Notes\n", encoding="utf-8")
        self.assertEqual(self.rules(path), set())

    def test_ignores_example_links_and_headings_in_code_fences(self):
        path = self.write(body='```markdown\n## When to Use\n[missing](absent.md)\n```\n~~~markdown\n[missing](absent.md)\n~~~\n`[example](absent.md)`\n')
        self.assertEqual(self.rules(path), set())
        path = self.write(body="## When to Use\n[missing](absent.md)\n")
        self.assertTrue({"ssot-trigger", "broken-link"}.issubset(self.rules(path)))

    def test_package_checks_references_without_linting_template_placeholders(self):
        self.write()
        self.write("sample/assets/agent.template.md", "name: <agent-name>\ndescription: <description>")
        reference = self.root / "sample" / "references" / "guide.md"
        reference.parent.mkdir()
        reference.write_text("[missing](absent.md)\n", encoding="utf-8")
        status, result = self.cli("--path", "sample")
        self.assertEqual(status, 1)
        self.assertEqual(result["total_files"], 3)
        self.assertEqual(result["findings"][0]["file"], "sample/references/guide.md")

    def test_empty_scope_and_missing_target_fail_explicitly(self):
        for args in ([], ["--path", "missing.md"]):
            with self.subTest(args=args):
                status, result = self.cli(*args)
                self.assertEqual(status, 2)
                self.assertEqual(result["findings"][0]["rule"], "input-path")

    def test_missing_yaml_dependency_does_not_report_success(self):
        with patch.object(validator, "yaml", None):
            status, result = self.cli()
        self.assertEqual(status, 2)
        self.assertEqual(result["findings"][0]["rule"], "yaml-dependency")

    def test_default_scope_discovers_workspace_entrypoints(self):
        self.write(".github/skills/sample/SKILL.md")
        self.write(".github/agents/sample.agent.md")
        self.write(".github/skills/sample/references/guide.md")
        status, result = self.cli()
        self.assertEqual(status, 0)
        self.assertEqual(result["total_files"], 2)

    def native(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_claude_preload_is_valid_but_not_in_vscode_format(self):
        metadata = 'name: reviewer\ndescription: Review a supplied artifact.\ntools: "Read, Grep, Glob"\nskills: [artifact-review]'
        claude = self.write(".claude/agents/reviewer.md", metadata)
        self.assertEqual(self.rules(claude), set())
        vscode = self.write(".github/agents/reviewer.agent.md", metadata)
        self.assertIn("unsupported-frontmatter", self.rules(vscode))
        bad = self.write(".claude/agents/reviewer.md", metadata.replace("[artifact-review]", "artifact-review"))
        self.assertIn("frontmatter-skills", self.rules(bad))

    def test_native_codex_toml_requires_instructions_and_rejects_foreign_tools(self):
        content = 'name = "reviewer"\ndescription = "Review supplied changes."\ndeveloper_instructions = "Report concrete findings with evidence."\n'
        path = self.native(".codex/agents/reviewer.toml", content)
        self.assertEqual(self.rules(path), set())
        path.write_text(content.replace('developer_instructions = "Report concrete findings with evidence."', 'tools = ["Read"]'), encoding="utf-8")
        self.assertTrue({"agent-instructions", "runtime-field"}.issubset(self.rules(path)))

    def test_kiro_json_and_markdown_profiles_accept_native_resources(self):
        content = {"name": "reviewer", "description": "Review a supplied artifact.",
                   "tools": ["read"], "prompt": "Return evidence-backed findings.",
                   "resources": ["skill://.kiro/skills/artifact-review/SKILL.md"],
                   "permissions": {"rules": []}}
        path = self.native(".kiro/agents/reviewer.json", json.dumps(content))
        self.assertEqual(self.rules(path), set())
        self.assertEqual(self.rules(self.write(".kiro/agents/reviewer.md",
            'name: reviewer\ndescription: Review supplied changes.\ntools: [read]\nresources: []\npermissions: {rules: []}')), set())
        content["resources"] = "not-a-list"
        path.write_text(json.dumps(content), encoding="utf-8")
        self.assertIn("agent-resources", self.rules(path))

    def test_native_format_mismatches_are_not_reported_as_valid(self):
        path = self.write(".codex/agents/reviewer.md")
        self.assertIn("runtime-format", self.rules(path))
        path = self.native(".claude/agents/reviewer.json", '{"name":"reviewer","description":"Review changes."}')
        self.assertIn("runtime-format", self.rules(path))

    def test_malformed_toml_and_duplicate_json_keep_diagnostics(self):
        toml = self.native(".codex/agents/broken.toml", 'name = "unterminated\n')
        duplicate = self.native(".kiro/agents/duplicate.json", '{"name":"first","name":"second"}')
        self.assertIn("structured-syntax", self.rules(toml))
        self.assertIn("structured-syntax", self.rules(duplicate))
        status, result = self.cli()
        self.assertEqual(status, 1)
        self.assertEqual((result["total_files"], result["errors"]), (2, 2))

    def test_missing_toml_parser_is_an_explicit_dependency_failure(self):
        self.native(".codex/agents/reviewer.toml", 'name = "reviewer"')
        with patch.object(validator, "tomllib", None):
            status, result = self.cli()
        self.assertEqual(status, 2)
        self.assertEqual(result["findings"][0]["rule"], "toml-dependency")

    def test_explicit_profile_handles_relocated_native_agent(self):
        self.native("reviewer.toml", 'name = "reviewer"\ndescription = "Review changes."\ndeveloper_instructions = "Return findings."')
        status, result = self.cli("--runtime", "codex", "--path", "reviewer.toml")
        self.assertEqual((status, result["errors"]), (0, 0))

    def test_relocated_wrong_agent_formats_fail_with_explicit_runtime(self):
        cases = (("codex", "reviewer.json", '{"name":"reviewer","description":"Review changes.","prompt":"Return findings."}'),
                 ("claude-code", "reviewer.toml", 'name="reviewer"\ndescription="Review changes."\ndeveloper_instructions="Return findings."'))
        for runtime, name, content in cases:
            with self.subTest(runtime=runtime):
                self.native(name, content)
                status, result = self.cli("--runtime", runtime, "--path", name)
                self.assertEqual(status, 1)
                self.assertEqual(result["findings"][0]["rule"], "runtime-format")

    def test_explicit_resource_role_preserves_supporting_file_validation(self):
        self.native("schema.json", '{"type":"object"}')
        status, result = self.cli("--runtime", "codex", "--kind", "resource", "--path", "schema.json")
        self.assertEqual((status, result["errors"]), (0, 0))

    def test_kiro_yaml_is_a_resource_not_a_native_agent_wrapper(self):
        for suffix in ("yaml", "yml"):
            with self.subTest(suffix=suffix):
                name = f"reviewer.{suffix}"
                self.native(name, "name: reviewer\ndescription: Review supplied changes.\nprompt: Return findings.")
                status, result = self.cli("--runtime", "kiro", "--path", name)
                self.assertEqual(status, 1)
                self.assertEqual(result["findings"][0]["rule"], "runtime-format")
                status, result = self.cli("--runtime", "kiro", "--kind", "resource", "--path", name)
                self.assertEqual((status, result["errors"]), (0, 0))

    def test_folder_runtime_does_not_treat_supporting_resources_as_agents(self):
        self.write("package/SKILL.md")
        self.native("package/references/schema.json", '{"type":"object"}')
        status, result = self.cli("--runtime", "codex", "--path", "package")
        self.assertEqual((status, result["total_files"], result["errors"]), (0, 2, 0))

    def test_all_native_project_roots_are_discovered(self):
        self.write(".github/agents/reviewer.agent.md")
        self.write(".claude/agents/reviewer.md")
        self.native(".codex/agents/reviewer.toml", 'name="reviewer"\ndescription="Review changes."\ndeveloper_instructions="Return findings."')
        self.native(".kiro/agents/reviewer.json", '{"name":"reviewer","description":"Review changes.","prompt":"Return findings."}')
        for root in (".github", ".claude", ".agents", ".kiro"):
            self.write(f"{root}/skills/sample/SKILL.md")
        status, result = self.cli()
        self.assertEqual((status, result["total_files"], result["errors"]), (0, 8, 0))

    def test_runtime_templates_instantiate_to_valid_native_files(self):
        assets = SCRIPT.parents[1] / "assets" / "runtimes"
        destinations = {
            "copilot": ".github/agents/reviewer.agent.md",
            "claude-code": ".claude/agents/reviewer.md",
            "codex": ".codex/agents/reviewer.toml",
            "kiro": ".kiro/agents/reviewer.md",
        }
        for profile, destination in destinations.items():
            with self.subTest(profile=profile):
                suffix = Path(destination).suffix
                template_content = (assets / profile / f"agent.template{suffix}").read_text(encoding="utf-8")
                template_content = template_content.replace("<agent-name>", "reviewer")
                template_content = re.sub(r"<[^>]+>", "Review supplied artifacts and return evidence-backed findings", template_content)
                self.assertEqual(self.rules(self.native(destination, template_content)), set())

    def test_skill_templates_work_in_each_native_discovery_root(self):
        template = SCRIPT.parents[1] / "assets" / "skill.template.md"
        content = template.read_text(encoding="utf-8")
        content = content.replace("<skill-name>", "sample")
        content = re.sub(r"<[^>]+>", "Review supplied artifacts with evidence", content)
        roots = (".github", ".claude", ".agents", ".kiro", "skills")
        for root in roots:
            with self.subTest(root=root):
                self.assertEqual(self.rules(self.native(f"{root}/skills/sample/SKILL.md", content)), set())

    def test_native_template_profile_takes_precedence_over_builder_host_path(self):
        path = Path(".github/skills/craft-agent-skill/assets/runtimes/claude-code/agent.template.md")
        self.assertEqual(validator.runtime_for(path), "claude-code")

    @unittest.skipUnless(shutil.which("powershell"), "PowerShell is not installed")
    def test_powershell_entrypoint_preserves_json_flags_paths_and_exit_code(self):
        path = self.write("folder with spaces/SKILL.md", 'name: sample\ndescription: "unterminated')
        result = subprocess.run(
            ["powershell", "-NoProfile", "-File", str(SCRIPT.with_suffix(".ps1")),
             "--root", str(self.root), "-Path", str(path), "-Json"],
            capture_output=True, text=True, encoding="utf-8", timeout=20,
        )
        self.assertEqual(result.returncode, 1, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual(report["findings"][0]["rule"], "frontmatter-yaml")


if __name__ == "__main__":
    unittest.main()
