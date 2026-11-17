"""Regression tests for skill version control, bump script, and terminal installers."""

import importlib.util
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.dont_write_bytecode = True

REPO_ROOT = Path(__file__).resolve().parents[1]
INSTALL_PY = REPO_ROOT / "scripts" / "install.py"
INSTALL_JS = REPO_ROOT / "bin" / "install.js"
BUMP_JS = REPO_ROOT / "scripts" / "bump-version.js"

spec = importlib.util.spec_from_file_location("skill_installer", INSTALL_PY)
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


def read_frontmatter_version(skill_path: Path) -> str:
    content = skill_path.read_text(encoding="utf-8")
    fm = re.match(r"\A---\r?\n(.*?)\r?\n---", content, re.S)
    assert fm is not None, "SKILL.md must have YAML frontmatter"
    match = re.search(r'^\s*version:\s*["\']?([^"\'\r\n]+)["\']?\s*$', fm.group(1), re.M)
    assert match is not None, "SKILL.md frontmatter must declare version"
    return match.group(1).strip()


class VersioningTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="craft-agent-skill-version-test-")
        self.root = Path(self.temporary.name).resolve()

    def tearDown(self):
        self.temporary.cleanup()

    def test_skill_md_and_package_json_versions_match_semver(self):
        skill_version = read_frontmatter_version(REPO_ROOT / "SKILL.md")
        pkg = json.loads((REPO_ROOT / "package.json").read_text(encoding="utf-8"))
        self.assertRegex(skill_version, r"^\d+\.\d+\.\d+$")
        self.assertEqual(skill_version, pkg["version"])
        self.assertEqual(installer.read_skill_version(REPO_ROOT), skill_version)

    def test_python_installer_displays_version_in_terminal(self):
        expected = read_frontmatter_version(REPO_ROOT / "SKILL.md")
        ver_run = subprocess.run(
            [sys.executable, str(INSTALL_PY), "--version"],
            capture_output=True, text=True, encoding="utf-8", timeout=20,
        )
        self.assertEqual(ver_run.returncode, 0, ver_run.stderr)
        self.assertIn(f"craft-agent-skill v{expected}", ver_run.stdout)

        target = self.root / "project"
        target.mkdir()
        install_run = subprocess.run(
            [sys.executable, str(INSTALL_PY), "--scope", "project", "--runtime", "codex",
             "--mode", "copy", "--target-path", str(target)],
            capture_output=True, text=True, encoding="utf-8", timeout=20,
        )
        self.assertEqual(install_run.returncode, 0, install_run.stderr)
        self.assertIn(f"Installing craft-agent-skill v{expected}", install_run.stdout)
        self.assertIn(f"Successfully installed craft-agent-skill v{expected}", install_run.stdout)

    @unittest.skipUnless(shutil.which("node"), "Node.js is not installed")
    def test_node_installer_displays_version_in_terminal(self):
        expected = read_frontmatter_version(REPO_ROOT / "SKILL.md")
        ver_run = subprocess.run(
            ["node", str(INSTALL_JS), "--version"],
            capture_output=True, text=True, encoding="utf-8", timeout=20,
        )
        self.assertEqual(ver_run.returncode, 0, ver_run.stderr)
        self.assertEqual(ver_run.stdout.strip(), f"v{expected}")

        target = self.root / "project-node"
        target.mkdir()
        install_run = subprocess.run(
            ["node", str(INSTALL_JS), "--scope", "project", "--runtime", "codex",
             "--mode", "copy", "--target-path", str(target)],
            capture_output=True, text=True, encoding="utf-8", timeout=20,
        )
        self.assertEqual(install_run.returncode, 0, install_run.stderr)
        plain_stdout = re.sub(r"\x1b\[[0-9;]*m", "", install_run.stdout)
        self.assertIn(f"v{expected}", plain_stdout)
        self.assertIn(f"Installation Successful! (v{expected})", plain_stdout)

    @unittest.skipUnless(shutil.which("node"), "Node.js is not installed")
    def test_bump_version_updates_skill_and_package_for_minor_and_major(self):
        skill_path = self.root / "SKILL.md"
        pkg_path = self.root / "package.json"
        skill_path.write_text(
            '---\nname: craft-agent-skill\ndescription: "Sample."\nmetadata:\n  version: "1.0.0"\n---\n# Body\n',
            encoding="utf-8",
        )
        pkg_path.write_text('{\n  "name": "craft-agent-skill",\n  "version": "1.0.0"\n}\n', encoding="utf-8")

        for arg, expected in (("minor", "1.1.0"), ("patch", "1.1.1"), ("major", "2.0.0")):
            with self.subTest(arg=arg):
                res = subprocess.run(
                    ["node", str(BUMP_JS), arg, "--root", str(self.root)],
                    capture_output=True, text=True, encoding="utf-8", timeout=20,
                )
                self.assertEqual(res.returncode, 0, res.stderr)
                self.assertEqual(read_frontmatter_version(skill_path), expected)
                self.assertEqual(json.loads(pkg_path.read_text(encoding="utf-8"))["version"], expected)

        pkg_path.write_text('{\n  "name": "craft-agent-skill",\n  "version": "2.4.0"\n}\n', encoding="utf-8")
        sync = subprocess.run(
            ["node", str(BUMP_JS), "--sync-from-package", "--root", str(self.root)],
            capture_output=True, text=True, encoding="utf-8", timeout=20,
        )
        self.assertEqual(sync.returncode, 0, sync.stderr)
        self.assertEqual(read_frontmatter_version(skill_path), "2.4.0")


if __name__ == "__main__":
    unittest.main()
