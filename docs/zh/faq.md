# COROS MCP 常见问题

[English](../en/faq.md) | [中文](faq.md) | [接入指南](getting-started.md) | [返回首页](../../README.zh.md)

## 1. COROS MCP 支持在哪些平台上使用？

MCP 是一种连接外部系统的开源标准，可以把 MCP 理解成 AI 应用的 “USB 接口”。能否接入，取决于该平台是否支持添加 MCP 服务，以及是否支持 COROS MCP 所需的认证方式。

目前建议优先使用已验证支持的平台，如 ChatGPT、Claude、OpenClaw、Workbuddy、Hermes 等。

如果你使用的平台暂未支持 MCP，可以关注该平台后续更新。只要平台开放兼容的 MCP 接入能力，即可按平台规则连接 COROS。

## 2. 使用 COROS MCP 需要付费吗？

COROS MCP 本身不收取费用。你可以在支持 MCP 的 AI 平台中授权连接 COROS 账号并使用已开放的功能。

但请注意，部分 AI 平台可能会对 MCP、外部工具连接、高级模型或开发者模式设置会员、订阅或额度限制。这些费用由对应的 AI 平台收取，并非 COROS 决定。请以你所用平台的最新规则为准。

## 3. 无法完成授权？

请先确认你的 COROS 账号可以在 COROS App 中正常登录和使用，并且账号内已有可查看的数据。

如果仍无法授权，请检查：

1. 授权页面是否已完整打开，浏览器是否拦截了弹窗或跳转。

2. 是否使用了正确的 COROS 账号登录。

3. AI 平台内是否已删除旧连接并重新授权。

如果多次重试仍失败，请保存报错截图，并联系 COROS 客服排查。

## 4. MCP URL 无效？

当前 COROS MCP 使用了域名跳转技术（[https://mcp.coros.com/mcp](https://mcp.coros.com/mcp)），会根据您账号所在的实际区域自动切换至最佳服务器。但部分 AI 平台不支持域名重定向，从而导致报错或连接失效。

如果遇到 URL 无效，请根据您**账号所在的实际地区**，直接复制并填写对应的独立分流 URL：

<table width="100%">
  <thead>
    <tr>
      <th align="left" width="320" nowrap>账号地区</th>
      <th align="left" width="600">独立分流 URL</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td nowrap>中国大陆</td>
      <td nowrap><code>https://mcpcn.coros.com/mcp</code></td>
    </tr>
    <tr>
      <td nowrap>欧洲</td>
      <td nowrap><code>https://mcpeu.coros.com/mcp</code></td>
    </tr>
    <tr>
      <td nowrap>美国及其他地区</td>
      <td nowrap><code>https://mcpus.coros.com/mcp</code></td>
    </tr>
  </tbody>
</table>

## 5. MCP 更新后，如何刷新工具列表？

当 COROS MCP 新增或更新工具后，请在 AI 平台中刷新 MCP 工具列表，让 AI 助手看到最新可用能力。不同平台的刷新入口可能不同。

如果新工具仍未出现，可以尝试新建对话，或重新连接 COROS MCP。

## 6. 使用 Skill 时提示 session 过期？

这通常是因为你通过 Skill 方式登录 COROS，并且本地仍在使用旧版 Skill。此前的 Skill 使用依赖 `Mcp-Session-Id` 会话编号的 MCP 连接流程；现在 COROS MCP 已切换到新版无状态 MCP 流程，最新版 Skill 已完成适配。

请先更新本地 Skill 包：

```bash
npm install -g coros-mcp@latest
```

更新后，重新连接 COROS MCP 或重新发起 Skill 登录流程，再重试你的请求。

## 7. AI 无法拉取到 COROS 数据？

如果已成功连接 COROS MCP，但 AI 没有拉取到数据，可以按以下步骤排查：

1. 确认 COROS App 内已有对应数据。设备数据需要先同步到 COROS App，再上传至云端。如果 App 内本身就没有这条数据，AI 也是无法读取到的。

2. 新建一个对话窗口，或在支持的客户端中发送 /new 后重新提问。

3. 使用更明确的指令，例如：“请调用 COROS MCP，查看我最近 7 天的运动记录。”

## 8. 为什么 AI 回答不准确？

AI 的回答质量会受到模型能力、提问方式、可访问数据范围等因素影响。

如果回答明显不准确，可以尝试换一个新对话，明确要求“调用 COROS MCP”，并指定时间范围和数据类型，例如“请调用 COROS MCP，分析我过去 4 周的跑步训练负荷变化”。

推荐使用deepseek V4 flash及以上能力的模型，工具调用能力较弱的模型可能会漏用工具，或使用错误参数。

## 9. 能否拉取 .fit 文件？

**支持。** COROS MCP 支持拉取运动记录的 `.fit` 文件，以便您进行更深入的数据分析。

同时，通过这种方式可以避免大量秒级数据直接挤爆 AI 的上下文窗口。

我们提供以下两种获取方式：

- **直接获取：** 直接读取 `.fit` 文件实体。

- **链接获取：** 获取文件的下载链接。

<strong>注：</strong> AI 助手是否能直接为您展示或处理文件实体，取决于您当前使用的 AI 平台自身的能力与权限控制。如果遇到文件无法下载或读取，建议咨询对应的 AI 平台客服。

**下载限制：** 文件获取与下载链接获取共用固定 **24 小时**窗口内 **50 个文件**的额度，按连接的平台用户计算；后续调用不会延长该窗口。

## 10. 我的数据会被谁看到？安全吗？

只有在你主动授权后，AI 应用才可以通过 COROS MCP 访问授权范围内的数据。你的 COROS 数据仍受 COROS 账号体系和隐私政策保护；AI 对话内容和模型处理方式则受你所使用 AI 平台的政策约束。建议只在你信任的平台上连接 COROS MCP。

## 11. 授权多久有效？需要定期重新登录吗？

访问令牌有效期为 30 天。到期后，支持自动刷新的 AI 客户端可使用刷新令牌续期，通常无需手动登录。

刷新令牌有效期为 180 天，每次成功刷新都会签发新的刷新令牌，因此不代表每隔 180 天必须重新登录。
