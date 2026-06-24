import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_SCRIPT = SKILL_ROOT / "scripts" / "coros_mcp_login.py"
SKILL_MARKDOWN = SKILL_ROOT / "SKILL.md"


class FakeResponse:
    def __init__(self, *, status: int = 200, headers=None, body: bytes = b"{}"):
        self.status = status
        self.headers = headers or {}
        self._body = body

    def read(self):
        return self._body


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

    def test_list_tools_uses_stateless_mcp_without_initialized_notification(self):
        helper = self.module.CorosMcpLoginHelper(
            issuer="https://mcpcn.coros.com",
            mcp_url="https://mcpcn.coros.com/mcp",
            cache_path=Path("/tmp/token.json"),
            pending_login_path=Path("/tmp/pending-login.json"),
            tool_catalog_path=Path("/tmp/tools.json"),
        )
        helper.token_store.load = mock.Mock(return_value=self.module.TokenSet(
            access_token="access-token",
            refresh_token="refresh-token",
            expires_at_epoch=9999999999,
            token_type="Bearer",
            scope="openid mcp.tools offline_access",
            client_id="client-1",
        ))
        helper.tool_catalog_store.load = mock.Mock(return_value=None)
        helper.tool_catalog_store.save = mock.Mock()
        helper.http.request = mock.Mock(side_effect=[
            FakeResponse(
                status=200,
                headers={},
                body=json.dumps({
                    "jsonrpc": "2.0",
                    "id": 1,
                    "result": {"protocolVersion": "2025-06-18", "capabilities": {"tools": {}}},
                }).encode("utf-8"),
            ),
            FakeResponse(
                status=200,
                headers={"Content-Type": "application/json"},
                body=json.dumps({
                    "jsonrpc": "2.0",
                    "id": 2,
                    "result": {"tools": [{"name": "queryUserInfo"}]},
                }).encode("utf-8"),
            ),
        ])

        tools = helper.list_tools(refresh=True)

        self.assertEqual([{"name": "queryUserInfo"}], tools)
        self.assertEqual(2, helper.http.request.call_count)
        init_call = helper.http.request.call_args_list[0]
        self.assertEqual("initialize", init_call.kwargs["json_body"]["method"])
        list_call = helper.http.request.call_args_list[1]
        self.assertEqual("tools/list", list_call.kwargs["json_body"]["method"])
        self.assertNotIn("Mcp-Session-Id", list_call.kwargs["headers"])

    def test_call_tool_uses_stateless_mcp_without_session_header(self):
        helper = self.module.CorosMcpLoginHelper(
            issuer="https://mcpcn.coros.com",
            mcp_url="https://mcpcn.coros.com/mcp",
            cache_path=Path("/tmp/token.json"),
            pending_login_path=Path("/tmp/pending-login.json"),
            tool_catalog_path=Path("/tmp/tools.json"),
        )
        helper.token_store.load = mock.Mock(return_value=self.module.TokenSet(
            access_token="access-token",
            refresh_token="refresh-token",
            expires_at_epoch=9999999999,
            token_type="Bearer",
            scope="openid mcp.tools offline_access",
            client_id="client-1",
        ))
        helper.http.request = mock.Mock(side_effect=[
            FakeResponse(
                status=200,
                headers={},
                body=json.dumps({
                    "jsonrpc": "2.0",
                    "id": 1,
                    "result": {"protocolVersion": "2025-06-18", "capabilities": {"tools": {}}},
                }).encode("utf-8"),
            ),
            FakeResponse(
                status=200,
                headers={"Content-Type": "application/json"},
                body=json.dumps({
                    "jsonrpc": "2.0",
                    "id": 2,
                    "result": {
                        "content": [{"type": "text", "text": "ok"}],
                        "isError": False,
                    },
                }).encode("utf-8"),
            ),
        ])

        result = helper.call_tool("queryUserInfo", {})

        self.assertEqual("ok", result["content"][0]["text"])
        self.assertEqual(2, helper.http.request.call_count)
        call_call = helper.http.request.call_args_list[1]
        self.assertEqual("tools/call", call_call.kwargs["json_body"]["method"])
        self.assertEqual("queryUserInfo", call_call.kwargs["json_body"]["params"]["name"])
        self.assertNotIn("Mcp-Session-Id", call_call.kwargs["headers"])


if __name__ == "__main__":
    unittest.main()
