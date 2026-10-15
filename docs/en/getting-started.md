# COROS MCP Setup Guide

[English](getting-started.md) | [中文](../zh/getting-started.md) | [Back to README](../../README.md)

Connect COROS MCP to use COROS in your AI assistant.

## 1. Before You Start

- Have a COROS account that you can sign in to.
- Sync your device data to the COROS app.
- Choose an AI platform that supports MCP or Skills.

## 2. Connect COROS

Choose the connection method that works with your platform.

### Add from a Plugin or Connector Directory

COROS is available in the following plugin or connector directories. We recommend this option because you don’t need to enter an MCP URL manually.

| Platform | Where to Add |
|---|---|
| ChatGPT | [Open the plugin directory](https://chatgpt.com/plugins/plugin_asdk_app_6a0694cbb2608191bbefb74ba810ab68) |
| Claude | [Open the connector directory](https://claude.ai/directory/coros) |
| Doubao Work | Search for COROS in the plugin directory |
| Workbuddy | Search for COROS in the connector directory |

Select COROS, choose **Add** or **Connect**, then follow the prompts to sign in to your COROS account and authorize access.

### Add MCP Manually

If your platform supports custom MCP connections, enter the following URL when adding an MCP service:

[https://mcp.coros.com/mcp](https://mcp.coros.com/mcp)

Save the connection, then follow the prompts to sign in to your COROS account and authorize access.

If the platform reports an invalid URL, use the address that matches your **COROS account region**:

| Account Region | MCP URL |
|---|---|
| Mainland China | `https://mcpcn.coros.com/mcp` |
| Europe | `https://mcpeu.coros.com/mcp` |
| United States | `https://mcpus.coros.com/mcp` |

### Connect Using a Skill

If your AI assistant supports installing and using Skills, send it this message:

> Please install the COROS MCP Skill using `npm install -g coros-mcp` and guide me through signing in.

## 3. Start Using COROS

After connecting, send your AI assistant:

> Use COROS MCP to show my workout records from the last 7 days.

If the returned records match those in your COROS app, you’re ready to go. You can also try:

- “Analyze my running training over the past month.”
- “Create an 8-week training plan based on my fitness and goals.”
- “Schedule a 30-minute easy run for tomorrow.”
