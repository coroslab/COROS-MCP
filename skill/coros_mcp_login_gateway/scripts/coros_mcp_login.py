#!/usr/bin/env python3
"""Gateway-aware COROS MCP login helper for OpenClaw skills."""

from __future__ import annotations

import argparse
import base64
import dataclasses
import getpass
import hashlib
import http.cookiejar
import json
import os
import secrets
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Dict, Optional


DEFAULT_SCOPES = "openid offline_access mcp.tools"
DEFAULT_CLIENT_NAME = "COROS MCP Gateway Skill Helper"
DEFAULT_REDIRECT_URI = "http://127.0.0.1:43123/callback"
DEFAULT_CACHE_ROOT = Path.home() / ".coros-mcp-skill-gateway"
DEFAULT_ISSUER = "https://mcp.coros.com"
DEFAULT_LOGIN_TIMEOUT = 300
DEFAULT_POLL_INTERVAL = 3
DEFAULT_TOOL_CATALOG_TTL_SECONDS = 300
REGIONAL_ISSUER_CACHE_KEYS = {
    "https://mcpcn.coros.com": "cn",
    "https://mcpeu.coros.com": "eu",
    "https://mcpus.coros.com": "us",
}


SENSITIVE_KEYS = frozenset({
    "access_token", "refresh_token", "Authorization",
    "password", "pollToken", "loginTicket", "code_verifier",
})


def _sanitize_payload(payload):
    """过滤 payload 中的敏感字段。"""
    if not isinstance(payload, dict):
        return str(payload)[:120]
    return {k: ("***" if k in SENSITIVE_KEYS else v) for k, v in payload.items()}


class AuthFlowError(RuntimeError):
    """Raised when the helper cannot complete the auth flow."""


def now_epoch() -> int:
    return int(time.time())


def generate_pkce_verifier() -> str:
    return base64.urlsafe_b64encode(secrets.token_bytes(32)).decode("utf-8").rstrip("=")


def build_pkce_challenge(verifier: str) -> str:
    digest = hashlib.sha256(verifier.encode("utf-8")).digest()
    return base64.urlsafe_b64encode(digest).decode("utf-8").rstrip("=")


@dataclasses.dataclass
class TokenSet:
    access_token: str
    refresh_token: str
    expires_at_epoch: int
    token_type: str
    scope: str
    client_id: Optional[str] = None

    @classmethod
    def from_token_response(cls, payload: Dict[str, object], client_id: Optional[str]) -> "TokenSet":
        expires_in = int(payload.get("expires_in", 3600))
        refresh_token = payload.get("refresh_token")
        access_token = payload.get("access_token")
        if not isinstance(refresh_token, str) or not refresh_token:
            raise AuthFlowError("token response is missing refresh_token")
        if not isinstance(access_token, str) or not access_token:
            raise AuthFlowError("token response is missing access_token")
        return cls(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_at_epoch=now_epoch() + expires_in,
            token_type=str(payload.get("token_type", "Bearer")),
            scope=str(payload.get("scope", DEFAULT_SCOPES)),
            client_id=client_id,
        )

    def is_expired(self, skew_seconds: int = 60) -> bool:
        return now_epoch() + skew_seconds >= self.expires_at_epoch


@dataclasses.dataclass
class PendingLoginSession:
    client_id: str
    verifier: str
    state: str
    authorize_url: str
    session_id: str
    poll_token: str
    login_url: str
    poll_interval: int


@dataclasses.dataclass
class ToolCatalogCache:
    fetched_at_epoch: int
    tools: list[Dict[str, object]]

    def is_fresh(self, ttl_seconds: int = DEFAULT_TOOL_CATALOG_TTL_SECONDS) -> bool:
        return now_epoch() - self.fetched_at_epoch < ttl_seconds


class TokenStore:
    def __init__(self, path: Path):
        self.path = path

    def load(self) -> Optional[TokenSet]:
        if not self.path.exists():
            return None
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        return TokenSet(
            access_token=payload["access_token"],
            refresh_token=payload["refresh_token"],
            expires_at_epoch=int(payload["expires_at_epoch"]),
            token_type=payload.get("token_type", "Bearer"),
            scope=payload.get("scope", DEFAULT_SCOPES),
            client_id=payload.get("client_id"),
        )

    def save(self, token_set: TokenSet) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = self.path.with_suffix(".tmp")
        temp_path.write_text(json.dumps(dataclasses.asdict(token_set), indent=2), encoding="utf-8")
        os.chmod(temp_path, 0o600)
        temp_path.replace(self.path)
        os.chmod(self.path, 0o600)

    def clear(self) -> None:
        if self.path.exists():
            self.path.unlink()


class PendingLoginStore:
    def __init__(self, path: Path):
        self.path = path

    def load(self) -> Optional[PendingLoginSession]:
        if not self.path.exists():
            return None
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        return PendingLoginSession(
            client_id=str(payload["client_id"]),
            verifier=str(payload["verifier"]),
            state=str(payload["state"]),
            authorize_url=str(payload["authorize_url"]),
            session_id=str(payload["session_id"]),
            poll_token=str(payload["poll_token"]),
            login_url=str(payload["login_url"]),
            poll_interval=int(payload.get("poll_interval", DEFAULT_POLL_INTERVAL)),
        )

    def save(self, pending_session: PendingLoginSession) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = self.path.with_suffix(".tmp")
        temp_path.write_text(json.dumps(dataclasses.asdict(pending_session), indent=2), encoding="utf-8")
        os.chmod(temp_path, 0o600)
        temp_path.replace(self.path)
        os.chmod(self.path, 0o600)

    def clear(self) -> None:
        if self.path.exists():
            self.path.unlink()


class ToolCatalogStore:
    def __init__(self, path: Path):
        self.path = path

    def load(self) -> Optional[ToolCatalogCache]:
        if not self.path.exists():
            return None
        payload = json.loads(self.path.read_text(encoding="utf-8"))
        tools = payload.get("tools", [])
        if not isinstance(tools, list):
            raise AuthFlowError("tool catalog cache is invalid")
        return ToolCatalogCache(
            fetched_at_epoch=int(payload.get("fetched_at_epoch", 0)),
            tools=tools,
        )

    def save(self, catalog: ToolCatalogCache) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = self.path.with_suffix(".tmp")
        temp_path.write_text(json.dumps(dataclasses.asdict(catalog), indent=2), encoding="utf-8")
        os.chmod(temp_path, 0o600)
        temp_path.replace(self.path)
        os.chmod(self.path, 0o600)

    def clear(self) -> None:
        if self.path.exists():
            self.path.unlink()


class NoRedirectHandler(urllib.request.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):
        return fp

    def http_error_302(self, req, fp, code, msg, headers):
        return fp

    def http_error_303(self, req, fp, code, msg, headers):
        return fp

    def http_error_307(self, req, fp, code, msg, headers):
        return fp

    def http_error_308(self, req, fp, code, msg, headers):
        return fp


class SimpleHttpClient:
    def __init__(self):
        self.opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()),
            NoRedirectHandler(),
        )

    def request(self, method: str, url: str, *, form=None, json_body=None, headers=None, timeout: int = 15):
        request_headers: Dict[str, str] = dict(headers or {})
        data = None
        if form is not None:
            data = urllib.parse.urlencode(form).encode("utf-8")
            request_headers["Content-Type"] = "application/x-www-form-urlencoded"
        if json_body is not None:
            data = json.dumps(json_body).encode("utf-8")
            request_headers["Content-Type"] = "application/json"
        req = urllib.request.Request(url, data=data, headers=request_headers, method=method.upper())
        try:
            return self.opener.open(req, timeout=timeout)
        except urllib.error.HTTPError as exc:
            return exc

    @staticmethod
    def read_json(response):
        raw = response.read().decode("utf-8")
        if not raw:
            return {}
        content_type = response.headers.get("Content-Type", "")
        if "text/event-stream" in content_type:
            event_payloads = []
            current_data_lines = []
            for line in raw.splitlines():
                if not line:
                    if current_data_lines:
                        event_payloads.append("\n".join(current_data_lines))
                        current_data_lines = []
                    continue
                if line.startswith("data:"):
                    current_data_lines.append(line[5:].lstrip())
            if current_data_lines:
                event_payloads.append("\n".join(current_data_lines))
            if not event_payloads:
                return {}
            return json.loads(event_payloads[-1])
        return json.loads(raw)


class CorosMcpLoginHelper:
    def __init__(
        self,
        *,
        issuer: str,
        mcp_url: str,
        cache_path: Path,
        pending_login_path: Path,
        tool_catalog_path: Path,
        client_name: str = DEFAULT_CLIENT_NAME,
        redirect_uri: str = DEFAULT_REDIRECT_URI,
    ):
        self.issuer = issuer.rstrip("/")
        self.mcp_url = mcp_url
        self.cache_path = cache_path
        self.client_name = client_name
        self.redirect_uri = redirect_uri
        self.scopes = DEFAULT_SCOPES
        self.token_store = TokenStore(cache_path)
        self.pending_login_store = PendingLoginStore(pending_login_path)
        self.tool_catalog_store = ToolCatalogStore(tool_catalog_path)
        self.http = SimpleHttpClient()

    def register_client(self) -> str:
        response = self.http.request(
            "POST",
            f"{self.issuer}/connect/register",
            json_body={
                "client_name": self.client_name,
                "redirect_uris": [self.redirect_uri],
                "grant_types": ["authorization_code", "refresh_token"],
                "response_types": ["code"],
                "scope": self.scopes,
                "token_endpoint_auth_method": "none",
            },
        )
        payload = self.http.read_json(response)
        if response.status not in (200, 201):
            raise AuthFlowError(f"client registration failed: {_sanitize_payload(payload)}")
        client_id = payload.get("client_id")
        if not isinstance(client_id, str) or not client_id:
            raise AuthFlowError("client registration response is missing client_id")
        return client_id

    def login(self, *, username: str, password: str) -> TokenSet:
        client_id = self.register_client()
        verifier = generate_pkce_verifier()
        challenge = build_pkce_challenge(verifier)
        state = secrets.token_urlsafe(24)

        authorize_url = self._build_authorize_url(client_id, challenge, state)
        first_response = self.http.request("GET", authorize_url)
        coros_url = first_response.headers.get("Location")
        if first_response.status not in (302, 303) or not coros_url:
            raise AuthFlowError("service did not redirect to COROS login")

        coros_response = self.http.request(
            "POST",
            coros_url,
            form=self._build_coros_login_form(coros_url, username, password),
        )
        callback_url = coros_response.headers.get("Location")
        if coros_response.status not in (302, 303) or not callback_url:
            raise AuthFlowError("COROS login did not continue back to the service")

        callback_response = self.http.request("GET", callback_url)
        resume_url = callback_response.headers.get("Location")
        if callback_response.status not in (302, 303) or not resume_url:
            raise AuthFlowError("service callback did not resume authorization")

        resume_response = self.http.request("GET", resume_url)
        final_redirect = resume_response.headers.get("Location")
        if resume_response.status not in (302, 303) or not final_redirect:
            raise AuthFlowError("service authorization did not return client callback")

        code, returned_state = self._extract_code_and_state(final_redirect)
        if returned_state != state:
            raise AuthFlowError("state mismatch during authorization")

        token_set = self.exchange_code(client_id=client_id, code=code, verifier=verifier)
        self.token_store.save(token_set)
        return token_set

    def device_login(self, *, timeout: int, interval: int) -> TokenSet:
        pending = self.start_device_login()
        self._print_login_url(pending.login_url)
        return self.finish_device_login(timeout=timeout, interval=interval, pending=pending)

    def start_device_login(self) -> PendingLoginSession:
        client_id = self.register_client()
        verifier = generate_pkce_verifier()
        challenge = build_pkce_challenge(verifier)
        state = secrets.token_urlsafe(24)
        authorize_url = self._build_authorize_url(client_id, challenge, state)
        cli_session = self._create_cli_session(client_id)
        pending = PendingLoginSession(
            client_id=client_id,
            verifier=verifier,
            state=state,
            authorize_url=authorize_url,
            session_id=str(cli_session["sessionId"]),
            poll_token=str(cli_session["pollToken"]),
            login_url=str(cli_session["loginUrl"]),
            poll_interval=max(1, int(cli_session.get("intervalSeconds", DEFAULT_POLL_INTERVAL) or DEFAULT_POLL_INTERVAL)),
        )
        self.pending_login_store.save(pending)
        return pending

    def finish_device_login(
        self,
        *,
        timeout: int,
        interval: int,
        pending: Optional[PendingLoginSession] = None,
    ) -> TokenSet:
        active_pending = pending or self.pending_login_store.load()
        if active_pending is None:
            raise AuthFlowError("no pending login session found")

        login_ticket = self._poll_session(
            active_pending.session_id,
            active_pending.poll_token,
            timeout=timeout,
            interval=active_pending.poll_interval if interval == DEFAULT_POLL_INTERVAL else interval,
        )
        authorize_with_ticket = self._append_login_ticket(active_pending.authorize_url, login_ticket)
        authorize_response = self.http.request("GET", authorize_with_ticket)
        callback_url = authorize_response.headers.get("Location")
        if authorize_response.status not in (302, 303) or not callback_url:
            raise AuthFlowError("service authorization did not return client callback")

        code, returned_state = self._extract_code_and_state(callback_url)
        if returned_state != active_pending.state:
            raise AuthFlowError("state mismatch during authorization")

        token_set = self.exchange_code(
            client_id=active_pending.client_id,
            code=code,
            verifier=active_pending.verifier,
        )
        self.token_store.save(token_set)
        self.pending_login_store.clear()
        return token_set

    def ensure_token(self) -> TokenSet:
        cached = self.token_store.load()
        if cached is None:
            raise AuthFlowError("no local token cache found, run login first")
        if not cached.is_expired():
            return cached
        refreshed = self.refresh(cached)
        self.token_store.save(refreshed)
        return refreshed

    def exchange_code(self, *, client_id: str, code: str, verifier: str) -> TokenSet:
        response = self.http.request(
            "POST",
            f"{self.issuer}/oauth2/token",
            form={
                "grant_type": "authorization_code",
                "client_id": client_id,
                "code": code,
                "redirect_uri": self.redirect_uri,
                "code_verifier": verifier,
            },
        )
        payload = self.http.read_json(response)
        if response.status != 200:
            raise AuthFlowError(f"token exchange failed: {_sanitize_payload(payload)}")
        return TokenSet.from_token_response(payload, client_id)

    def refresh(self, token_set: TokenSet) -> TokenSet:
        client_id = token_set.client_id or self.register_client()
        response = self.http.request(
            "POST",
            f"{self.issuer}/oauth2/token",
            form={
                "grant_type": "refresh_token",
                "client_id": client_id,
                "refresh_token": token_set.refresh_token,
            },
        )
        payload = self.http.read_json(response)
        if response.status != 200:
            self.token_store.clear()
            raise AuthFlowError(f"token refresh failed: {_sanitize_payload(payload)}")
        return TokenSet.from_token_response(payload, client_id)

    def render_openclaw_config(self, server_name: str) -> str:
        return json.dumps(
            {
                "mcp": {
                    "servers": {
                        server_name: {
                            "url": self.mcp_url,
                            "transport": "streamable-http",
                            "headers": {
                                "Authorization": self.authorization_header(self.ensure_token())
                            },
                        }
                    }
                }
            },
            indent=2,
        )

    def apply_openclaw(self, server_name: str) -> None:
        try:
            subprocess.run(
                ["openclaw", "mcp", "set", server_name, self.render_openclaw_config(server_name)],
                check=True,
                text=True,
            )
        except FileNotFoundError as exc:
            raise AuthFlowError("openclaw command not found") from exc

    @staticmethod
    def authorization_header(token_set: TokenSet) -> str:
        return f"{token_set.token_type} {token_set.access_token}"

    def list_tools(self, *, refresh: bool = False) -> list[Dict[str, object]]:
        if not refresh:
            cached_catalog = self.tool_catalog_store.load()
            if cached_catalog is not None and cached_catalog.is_fresh():
                return cached_catalog.tools

        token = self._initialize_mcp()
        tools: list[Dict[str, object]] = []
        cursor: Optional[str] = None
        request_id = 2

        while True:
            params: Dict[str, object] = {}
            if cursor:
                params["cursor"] = cursor
            response = self._send_mcp_request(
                token_set=token,
                request_id=request_id,
                method="tools/list",
                params=params or None,
            )
            result = response.get("result")
            if not isinstance(result, dict):
                raise AuthFlowError("mcp tools/list response is missing result")
            page_tools = result.get("tools", [])
            if not isinstance(page_tools, list):
                raise AuthFlowError("mcp tools/list response is missing tools")
            tools.extend(page_tools)
            next_cursor = result.get("nextCursor")
            if not isinstance(next_cursor, str) or not next_cursor:
                self.tool_catalog_store.save(ToolCatalogCache(
                    fetched_at_epoch=now_epoch(),
                    tools=tools,
                ))
                return tools
            cursor = next_cursor
            request_id += 1

    def describe_tool(self, tool_name: str, *, refresh: bool = False) -> Dict[str, object]:
        for tool in self.list_tools(refresh=refresh):
            if tool.get("name") == tool_name:
                return tool
        raise AuthFlowError(f"tool not found: {tool_name}")

    def call_tool(self, tool_name: str, arguments: Dict[str, object]) -> Dict[str, object]:
        token = self._initialize_mcp()
        response = self._send_mcp_request(
            token_set=token,
            request_id=2,
            method="tools/call",
            params={
                "name": tool_name,
                "arguments": arguments,
            },
        )
        result = response.get("result")
        if not isinstance(result, dict):
            raise AuthFlowError("mcp tools/call response is missing result")
        return result

    def _build_authorize_url(self, client_id: str, challenge: str, state: str) -> str:
        query = urllib.parse.urlencode(
            {
                "response_type": "code",
                "client_id": client_id,
                "redirect_uri": self.redirect_uri,
                "scope": self.scopes,
                "code_challenge": challenge,
                "code_challenge_method": "S256",
                "resource": self.mcp_url,
                "state": state,
            }
        )
        return f"{self.issuer}/oauth2/authorize?{query}"

    def _create_cli_session(self, client_id: str) -> Dict[str, object]:
        response = self.http.request(
            "POST",
            f"{self.issuer}/api/v1/cli/login-sessions",
            json_body={"clientId": client_id},
        )
        payload = self.http.read_json(response)
        if response.status not in (200, 201):
            raise AuthFlowError(f"cli session creation failed: {_sanitize_payload(payload)}")
        required_fields = ("sessionId", "pollToken", "loginUrl", "expiresAt")
        for field in required_fields:
            value = payload.get(field)
            if not isinstance(value, str) or not value:
                raise AuthFlowError(f"cli session response is missing {field}")
        return payload

    def _poll_session(self, session_id: str, poll_token: str, *, timeout: int, interval: int) -> str:
        deadline = time.monotonic() + timeout
        while True:
            response = self.http.request(
                "POST",
                f"{self.issuer}/api/v1/cli/login-sessions/{session_id}/claim",
                headers={"X-Poll-Token": poll_token},
            )
            payload = self.http.read_json(response)
            if response.status != 200:
                raise AuthFlowError(f"cli session claim failed: {_sanitize_payload(payload)}")

            status = str(payload.get("status", "")).lower()
            if status == "authorized":
                login_ticket = payload.get("loginTicket")
                if not isinstance(login_ticket, str) or not login_ticket:
                    raise AuthFlowError("cli session authorized response is missing loginTicket")
                return login_ticket
            if status == "pending":
                if time.monotonic() >= deadline:
                    raise AuthFlowError("cli session authorization timed out")
                time.sleep(interval)
                continue
            if status == "failed":
                raise AuthFlowError(f"cli session failed: {payload.get('errorCode', 'unknown_error')}")
            if status == "expired":
                raise AuthFlowError("cli session expired, restart login")
            if status == "claimed":
                raise AuthFlowError(f"cli session already claimed: {payload.get('errorCode', 'already_claimed')}")
            raise AuthFlowError(f"cli session returned unexpected status: {status or payload}")

    def _build_coros_login_form(self, coros_url: str, username: str, password: str) -> Dict[str, str]:
        query = urllib.parse.parse_qs(urllib.parse.urlparse(coros_url).query)
        return {
            "client_id": query.get("client_id", [""])[0],
            "redirect_uri": query.get("redirect_uri", [""])[0],
            "state": query.get("state", [""])[0],
            "scope": query.get("scope", [""])[0],
            "response_type": query.get("response_type", ["code"])[0],
            "activityType": "",
            "language": "zh",
            "country": "CN",
            "userName": username,
            "password": password,
            "checkStatus": "1",
            "getAllHistoryIn24Hours": "0",
        }

    @staticmethod
    def _extract_code_and_state(callback_url: str) -> tuple[str, str]:
        query = urllib.parse.parse_qs(urllib.parse.urlparse(callback_url).query)
        code = query.get("code", [""])[0]
        state = query.get("state", [""])[0]
        if not code or not state:
            raise AuthFlowError("client callback is missing code or state")
        return code, state

    @staticmethod
    def _append_login_ticket(authorize_url: str, login_ticket: str) -> str:
        parsed = urllib.parse.urlparse(authorize_url)
        query = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
        query.append(("login_ticket", login_ticket))
        return urllib.parse.urlunparse(parsed._replace(query=urllib.parse.urlencode(query)))

    @staticmethod
    def _print_login_url(login_url: str) -> None:
        print("Open this link in a browser to log in:", flush=True)
        print(login_url, flush=True)

    def _initialize_mcp(self) -> TokenSet:
        token = self.ensure_token()
        initialize_response = self.http.request(
            "POST",
            self.mcp_url,
            headers=self._build_mcp_headers(token),
            json_body={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "initialize",
                "params": {
                    "protocolVersion": "2025-06-18",
                    "capabilities": {},
                    "clientInfo": {
                        "name": self.client_name,
                        "version": "1.0.0",
                    },
                },
            },
        )
        payload = self.http.read_json(initialize_response)
        if initialize_response.status != 200:
            raise AuthFlowError(f"mcp initialize failed: {_sanitize_payload(payload)}")
        if "error" in payload:
            raise AuthFlowError(f"mcp initialize failed: {_sanitize_payload(payload['error'])}")
        return token

    def _send_mcp_request(
        self,
        *,
        token_set: TokenSet,
        request_id: int,
        method: str,
        params: Optional[Dict[str, object]] = None,
    ) -> Dict[str, object]:
        response = self.http.request(
            "POST",
            self.mcp_url,
            headers=self._build_mcp_headers(token_set),
            json_body={
                "jsonrpc": "2.0",
                "id": request_id,
                "method": method,
                "params": params or {},
            },
        )
        payload = self.http.read_json(response)
        if response.status != 200:
            raise AuthFlowError(f"mcp {method} failed: {_sanitize_payload(payload)}")
        if "error" in payload:
            raise AuthFlowError(f"mcp {method} failed: {_sanitize_payload(payload['error'])}")
        return payload

    def _build_mcp_headers(self, token_set: TokenSet) -> Dict[str, str]:
        return {
            "Authorization": self.authorization_header(token_set),
            "Accept": "application/json, text/event-stream",
        }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="COROS MCP OpenClaw skill helper")
    parser.add_argument("--issuer", default=os.environ.get("MCP_ISSUER_URL", DEFAULT_ISSUER))
    parser.add_argument("--mcp-url")
    parser.add_argument("--cache-root", default=os.environ.get("MCP_CACHE_ROOT", str(DEFAULT_CACHE_ROOT)))
    parser.add_argument("--cache-path", default=os.environ.get("MCP_CACHE_PATH"))
    parser.add_argument("--pending-login-path", default=os.environ.get("MCP_PENDING_LOGIN_PATH"))
    parser.add_argument("--tool-catalog-path", default=os.environ.get("MCP_TOOL_CATALOG_PATH"))
    parser.add_argument("--client-name", default=DEFAULT_CLIENT_NAME)
    parser.add_argument("--redirect-uri", default=DEFAULT_REDIRECT_URI)
    parser.add_argument("--no-gateway-discovery", action="store_true")

    subparsers = parser.add_subparsers(dest="command", required=True)

    login_parser = subparsers.add_parser("login")
    login_parser.add_argument("--legacy", action="store_true")
    login_parser.add_argument("--timeout", type=int, default=DEFAULT_LOGIN_TIMEOUT)
    login_parser.add_argument("--interval", type=int, default=DEFAULT_POLL_INTERVAL)
    login_parser.add_argument("--username")

    subparsers.add_parser("login-start")

    finish_parser = subparsers.add_parser("login-finish")
    finish_parser.add_argument("--timeout", type=int, default=DEFAULT_LOGIN_TIMEOUT)
    finish_parser.add_argument("--interval", type=int, default=DEFAULT_POLL_INTERVAL)

    subparsers.add_parser("login-status")

    list_parser = subparsers.add_parser("list-tools")
    list_parser.add_argument("--refresh", action="store_true")

    describe_parser = subparsers.add_parser("describe-tool")
    describe_parser.add_argument("--tool", required=True)
    describe_parser.add_argument("--refresh", action="store_true")

    call_parser = subparsers.add_parser("call-tool")
    call_parser.add_argument("--tool", required=True)
    call_parser.add_argument("--arguments-json", default="{}")

    apply_parser = subparsers.add_parser("apply-openclaw")
    apply_parser.add_argument("--server-name", default="coros")
    apply_parser.add_argument("--legacy", action="store_true")
    apply_parser.add_argument("--timeout", type=int, default=DEFAULT_LOGIN_TIMEOUT)
    apply_parser.add_argument("--interval", type=int, default=DEFAULT_POLL_INTERVAL)
    apply_parser.add_argument("--username")
    subparsers.add_parser("logout")
    return parser


def normalize_issuer(issuer: str) -> str:
    return issuer.rstrip("/")


def discover_gateway_issuer(issuer: str) -> str:
    normalized_issuer = normalize_issuer(issuer)
    if normalized_issuer != DEFAULT_ISSUER:
        return normalized_issuer
    try:
        response = SimpleHttpClient().request(
            "GET",
            f"{normalized_issuer}/.well-known/openid-configuration",
            timeout=8,
        )
        payload = SimpleHttpClient.read_json(response)
        if response.status != 200:
            return normalized_issuer
        discovered_issuer = payload.get("issuer")
        if isinstance(discovered_issuer, str) and discovered_issuer.startswith("https://"):
            return normalize_issuer(discovered_issuer)
    except Exception as exc:
        print(f"warning: gateway discovery failed, using {normalized_issuer}: {exc}", file=sys.stderr)
    return normalized_issuer


def cache_key_for_issuer(issuer: str) -> str:
    normalized_issuer = normalize_issuer(issuer)
    regional_key = REGIONAL_ISSUER_CACHE_KEYS.get(normalized_issuer)
    if regional_key:
        return regional_key
    parsed_host = urllib.parse.urlparse(normalized_issuer).hostname
    if parsed_host:
        return parsed_host.replace(".", "-")
    return "default"


def default_state_path(cache_root: str, issuer: str, filename: str) -> Path:
    return Path(cache_root).expanduser() / cache_key_for_issuer(issuer) / filename


def build_helper(args: argparse.Namespace) -> CorosMcpLoginHelper:
    requested_issuer = normalize_issuer(args.issuer)
    issuer = requested_issuer if args.no_gateway_discovery else discover_gateway_issuer(requested_issuer)
    mcp_url = args.mcp_url or f"{issuer}/mcp"
    return CorosMcpLoginHelper(
        issuer=issuer,
        mcp_url=mcp_url,
        cache_path=Path(args.cache_path).expanduser()
        if args.cache_path else default_state_path(args.cache_root, issuer, "token.json"),
        pending_login_path=Path(args.pending_login_path).expanduser()
        if args.pending_login_path else default_state_path(args.cache_root, issuer, "pending-login.json"),
        tool_catalog_path=Path(args.tool_catalog_path).expanduser()
        if args.tool_catalog_path else default_state_path(args.cache_root, issuer, "tool-catalog.json"),
        client_name=args.client_name,
        redirect_uri=args.redirect_uri,
    )


def main() -> int:
    args = build_parser().parse_args()
    helper = build_helper(args)
    try:
        if args.command == "login":
            if args.legacy:
                if not args.username:
                    raise AuthFlowError("legacy login requires --username")
                password = getpass.getpass("COROS password: ")
                helper.login(username=args.username, password=password)
                helper.pending_login_store.clear()
            else:
                pending = helper.pending_login_store.load()
                if pending is None:
                    helper.device_login(timeout=args.timeout, interval=args.interval)
                else:
                    helper._print_login_url(pending.login_url)
                    helper.finish_device_login(
                        timeout=args.timeout,
                        interval=args.interval,
                        pending=pending,
                    )
            print("login ok")
            return 0
        if args.command == "login-start":
            pending = helper.start_device_login()
            helper._print_login_url(pending.login_url)
            print("login session saved locally")
            return 0
        if args.command == "login-finish":
            pending = helper.pending_login_store.load()
            helper.finish_device_login(timeout=args.timeout, interval=args.interval, pending=pending)
            print("login ok")
            return 0
        if args.command == "login-status":
            pending = helper.pending_login_store.load()
            if pending is None:
                print("no pending login session")
            else:
                print("pending login session found")
                print(pending.login_url)
            return 0
        if args.command == "list-tools":
            print(json.dumps(helper.list_tools(refresh=args.refresh), indent=2))
            return 0
        if args.command == "describe-tool":
            print(json.dumps(helper.describe_tool(args.tool, refresh=args.refresh), indent=2))
            return 0
        if args.command == "call-tool":
            try:
                arguments = json.loads(args.arguments_json)
            except json.JSONDecodeError as exc:
                raise AuthFlowError(f"invalid arguments json: {exc.msg}") from exc
            if not isinstance(arguments, dict):
                raise AuthFlowError("arguments json must be an object")
            print(json.dumps(helper.call_tool(args.tool, arguments), indent=2))
            return 0
        if args.command == "apply-openclaw":
            if helper.token_store.load() is None:
                if args.legacy:
                    if not args.username:
                        raise AuthFlowError("legacy login requires --username")
                    password = getpass.getpass("COROS password: ")
                    helper.login(username=args.username, password=password)
                    helper.pending_login_store.clear()
                else:
                    pending = helper.pending_login_store.load()
                    if pending is None:
                        helper.device_login(timeout=args.timeout, interval=args.interval)
                    else:
                        helper._print_login_url(pending.login_url)
                        helper.finish_device_login(
                            timeout=args.timeout,
                            interval=args.interval,
                            pending=pending,
                        )
            helper.apply_openclaw(args.server_name)
            print(f"openclaw mcp entry updated: {args.server_name}")
            return 0
        if args.command == "logout":
            helper.token_store.clear()
            helper.pending_login_store.clear()
            print("local token cache cleared")
            return 0
    except AuthFlowError as exc:
        print(f"error: {exc}")
        return 1
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
