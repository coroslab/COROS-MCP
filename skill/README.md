# COROS MCP Skills

[Repository](../README.md) | [中文 README](../README.zh.md)

This directory contains Agent Skill modules for connecting AI agents and local clients to COROS MCP.

## Available Skills

| Skill | Description |
| --- | --- |
| [`coros_mcp_login_gateway`](coros_mcp_login_gateway/) | Enters through `mcp.coros.com`, completes regional login, configures OpenClaw, and discovers and calls tools for private data queries, training plans, library workouts and scheduled workouts. |

## Usage

Open the skill directory for detailed instructions:

```text
skill/coros_mcp_login_gateway/
```

Agents that support skills can read the skill's `SKILL.md` file and use its helper script to log in, refresh local auth state, list tools, and configure OpenClaw.

The helper discovers tools dynamically; newly available server tools do not require a hardcoded Python tool list. Refresh with `list-tools --refresh` after a server update and inspect each unfamiliar tool with `describe-tool` before calling it.

The skill also explains how to create and update training safely: library templates, standalone scheduled copies and workouts inside a training plan are different objects. Read the [training-request instructions](coros_mcp_login_gateway/SKILL.md#training-requests) before a write. Saving, updating and scheduling require the user's request; a draft or advice alone is not authorization.

Repository documentation changes do not publish a new npm package. If installing through npm, the installed skill content follows the package's published version.
