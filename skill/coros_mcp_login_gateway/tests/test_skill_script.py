import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_SCRIPT = SKILL_ROOT / "scripts" / "coros_mcp_login.py"
SKILL_MARKDOWN = SKILL_ROOT / "SKILL.md"


def load_skill_module():
    spec = importlib.util.spec_from_file_location("coros_mcp_login_gateway_script", SKILL_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


class SkillScriptSmokeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_skill_module()

    def test_help_command_is_available(self):
        completed = subprocess.run(
            ["python3", str(SKILL_SCRIPT), "--help"],
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(0, completed.returncode)
        self.assertIn("apply-openclaw", completed.stdout)

    def test_help_command_works_without_secure_sibling_directory(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_root = Path(temp_dir)
            isolated_gateway_root = temp_root / "coros_mcp_login_gateway"
            isolated_scripts = isolated_gateway_root / "scripts"
            isolated_scripts.mkdir(parents=True)
            isolated_script = isolated_scripts / "coros_mcp_login.py"
            isolated_script.write_text(SKILL_SCRIPT.read_text(encoding="utf-8"), encoding="utf-8")

            completed = subprocess.run(
                ["python3", str(isolated_script), "--help"],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(0, completed.returncode)
        self.assertIn("apply-openclaw", completed.stdout)

    def test_parser_defaults_to_gateway_issuer_and_cache_root(self):
        parser = self.module.build_parser()

        args = parser.parse_args(["login"])

        self.assertEqual("https://mcp.coros.com", args.issuer)
        self.assertIsNone(args.cache_path)
        self.assertIn(".coros-mcp-skill-gateway", args.cache_root)
        self.assertEqual("COROS MCP Gateway Skill Helper", args.client_name)

    def test_build_helper_pins_gateway_to_discovered_regional_issuer(self):
        parser = self.module.build_parser()
        original_discover = self.module.discover_gateway_issuer
        self.module.discover_gateway_issuer = lambda issuer: "https://mcpus.coros.com"
        self.addCleanup(lambda: setattr(self.module, "discover_gateway_issuer", original_discover))

        args = parser.parse_args(["login-status"])
        helper = self.module.build_helper(args)

        self.assertEqual("https://mcpus.coros.com", helper.issuer)
        self.assertEqual("https://mcpus.coros.com/mcp", helper.mcp_url)
        self.assertIn(".coros-mcp-skill-gateway/us/token.json", str(helper.cache_path))

    def test_explicit_regional_issuer_uses_matching_regional_cache(self):
        parser = self.module.build_parser()

        args = parser.parse_args(["--issuer", "https://mcpeu.coros.com", "login-status"])
        helper = self.module.build_helper(args)

        self.assertEqual("https://mcpeu.coros.com", helper.issuer)
        self.assertEqual("https://mcpeu.coros.com/mcp", helper.mcp_url)
        self.assertIn(".coros-mcp-skill-gateway/eu/token.json", str(helper.cache_path))

    def test_custom_cache_path_overrides_regional_default(self):
        parser = self.module.build_parser()
        custom_cache = "/tmp/coros-token.json"

        args = parser.parse_args([
            "--issuer",
            "https://mcpus.coros.com",
            "--cache-path",
            custom_cache,
            "login-status",
        ])
        helper = self.module.build_helper(args)

        self.assertEqual(custom_cache, str(helper.cache_path))

    def test_skill_markdown_references_gateway_and_regional_hosts(self):
        content = SKILL_MARKDOWN.read_text(encoding="utf-8")

        self.assertIn("https://mcp.coros.com", content)
        self.assertIn("https://mcpcn.coros.com", content)
        self.assertIn("https://mcpeu.coros.com", content)
        self.assertIn("https://mcpus.coros.com", content)


if __name__ == "__main__":
    unittest.main()
