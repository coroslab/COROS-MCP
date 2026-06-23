# COROS MCP Skills

[Repository](../README.md) | [中文 README](../README.zh.md)

This directory contains Agent Skill modules for connecting AI agents and local clients to COROS MCP.

## Available Skills

| Skill | Description |
| --- | --- |
| [`coros_mcp_login_gateway`](coros_mcp_login_gateway/) | Enters through `mcp.coros.com`, completes COROS MCP login, discovers the selected CN/EU/US region, and helps configure OpenClaw. |

## Usage

Open the skill directory for detailed instructions:

```text
skill/coros_mcp_login_gateway/
```

Agents that support skills can read the skill's `SKILL.md` file and use its helper script to log in, refresh local auth state, list tools, and configure OpenClaw.
