# COROS MCP 接入指南

[English](../en/getting-started.md) | [中文](getting-started.md) | [返回首页](../../README.zh.md)

连接 COROS MCP 后，你可以在 AI 助手中使用 COROS。

## 1. 准备工作

- 准备一个可以正常登录的 COROS 账号。
- 将设备数据同步到 COROS App。
- 选择支持 MCP 或 Skill 的 AI 平台。

## 2. 连接 COROS

选择适合你所用平台的接入方式。

### 从插件／连接器目录添加

COROS 已上架以下平台的插件或连接器目录。推荐优先通过官方目录添加，无需手动填写 MCP 地址。

| 平台 | 添加入口 |
|---|---|
| ChatGPT | [打开插件目录](https://chatgpt.com/plugins/plugin_asdk_app_6a0694cbb2608191bbefb74ba810ab68) |
| Claude | [打开连接器目录](https://claude.ai/directory/coros) |
| 豆包工作 | 在插件目录中搜索 COROS |
| Workbuddy | 在连接器目录中搜索 COROS |

选择 COROS，点击添加或连接，按页面提示登录 COROS 账号并完成授权。

### 手动添加 MCP

如果平台支持自定义 MCP，可以在添加 MCP 服务的入口填写：

[https://mcp.coros.com/mcp](https://mcp.coros.com/mcp)

保存后，按提示登录 COROS 账号并完成授权。

如果平台提示地址无效，可根据 **COROS 账号所属地区**使用对应地址：

| 账号地区 | MCP 地址 |
|---|---|
| 中国大陆 | `https://mcpcn.coros.com/mcp` |
| 欧洲 | `https://mcpeu.coros.com/mcp` |
| 美国 | `https://mcpus.coros.com/mcp` |

### 通过 Skill 接入

如果你的 AI 助手支持安装和使用 Skill，可以向它发送：

> 请帮我安装 COROS MCP Skill：`npm install -g coros-mcp`，并引导我完成登录。

## 3. 开始使用

连接后，向 AI 助手发送：

> 请调用 COROS MCP，查看我最近 7 天的运动记录。

如果能够返回与你的 COROS App 一致的记录，即可开始使用。也可以继续尝试：

- “分析我最近一个月的跑步训练。”
- “根据我的体能和目标，创建一个 8 周训练计划。”
- “帮我在明天安排一节 30 分钟轻松跑。”
