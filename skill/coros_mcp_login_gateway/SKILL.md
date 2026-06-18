---
name: coros_mcp_login_gateway
description: Install or refresh the COROS MCP connection inside OpenClaw through the global mcp.coros.com gateway, automatically pinning the session to the CN, EU, or US cluster selected by the gateway.
metadata:
  openclaw:
    requires:
      bins: ["python3", "openclaw"]
---

# COROS MCP Login (Gateway)

Use this skill when the user wants one COROS MCP login skill that enters through `mcp.coros.com` and then uses the CN, EU, or US cluster selected by the gateway.

## What to do

1. Work from this skill directory, which contains `scripts/coros_mcp_login.py`.
2. Prefer the resilient two-step flow when the browser might open on another machine, or when the CLI process may not stay alive the whole time:

```bash
python3 scripts/coros_mcp_login.py login-start
python3 scripts/coros_mcp_login.py login-finish
python3 scripts/coros_mcp_login.py apply-openclaw --server-name coros
```

3. For a single-machine or quick refresh flow, use the one-shot helper:

```bash
python3 scripts/coros_mcp_login.py apply-openclaw --server-name coros
```

4. The helper defaults to `https://mcp.coros.com`, reads the gateway-selected issuer from discovery, and then pins login, token refresh, MCP calls, and local cache files to that concrete regional issuer.

5. If there is no local token cache yet, the helper will print a browser login link. Tell the user to open that link on their phone or computer browser and complete the COROS login there.

6. If you used `login-start`, the helper saves the pending login locally on that same machine. After the user finishes the browser login, run `login-finish` on the original machine to complete the token save.

7. To discover what this COROS MCP server currently supports, list tools dynamically. This command reuses a short-lived local cache first, so repeated requests stay fast:

```bash
python3 scripts/coros_mcp_login.py list-tools
```

Use `--refresh` only when you specifically want to force a live re-fetch from `/mcp`:

```bash
python3 scripts/coros_mcp_login.py list-tools --refresh
```

8. Before calling an unfamiliar tool, inspect its schema:

```bash
python3 scripts/coros_mcp_login.py describe-tool --tool queryUserInfo
```

9. To call a tool directly through this helper, pass a JSON object for the tool arguments:

```bash
python3 scripts/coros_mcp_login.py call-tool --tool queryUserInfo --arguments-json '{}'
```

10. After the OpenClaw setup command succeeds, verify the saved MCP entry exists:

```bash
openclaw mcp show coros
```

11. Tell the user plainly whether:
   - the saved COROS MCP entry was created or refreshed
   - a fresh login was needed or cached login was reused
   - the gateway resolved to CN, EU, or US if that matters for the request
   - the helper was able to initialize `/mcp` and discover/call the requested tool
   - any manual next step is still needed

## Notes

- Use `apply-openclaw` for setup or refresh. It will reuse saved login when possible and otherwise start the browser-based login flow.
- Use `login-start` + `login-finish` when the browser may be on a different computer, or when the original terminal might be interrupted before the login completes.
- Use `login-status` to check whether the original machine still has a saved pending login and to reprint the browser link.
- Gateway mode keeps separate local state under `~/.coros-mcp-skill-gateway/<region>/`, so CN, EU, and US tokens do not overwrite each other.
- If you must force a specific cluster, pass `--issuer https://mcpcn.coros.com`, `--issuer https://mcpeu.coros.com`, or `--issuer https://mcpus.coros.com`.
- `list-tools`, `describe-tool`, and `call-tool` automatically reuse the local token cache and refresh the token before MCP requests when it is near expiry.
- `list-tools` and `describe-tool` reuse a short-lived local tool catalog cache by default. Use `--refresh` when you want the latest live tool list immediately.
- For natural-language requests, first run cached `list-tools`, choose the best matching tool from the current server response, inspect it with `describe-tool` only when the arguments are not obvious, then run `call-tool`.
- If the selected tool needs required arguments that are still missing, ask the user only for those missing fields instead of dumping the full schema back to them.
- If the user explicitly asks to keep using the old password-based flow, run the helper with `--legacy` and pass `--username`. The password will be prompted interactively.
- Use `logout` only if the user explicitly asks to clear saved local login state.
- Do not invent a second config path; always use the helper in this skill's `scripts/` directory.
- This is the hardened version. Token values are never printed to stdout. Error messages are sanitized to prevent sensitive data leakage.
